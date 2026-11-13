import asyncio
import calendar
from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager, contextmanager
from datetime import datetime, timezone
from enum import Enum
import hashlib
import hmac
import ipaddress
import logging
import os
import secrets
import time
import threading

from fastapi import Depends, FastAPI, HTTPException, Path, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from redis import Redis
from redis.exceptions import RedisError
from sqlalchemy import case, delete, func, or_, select, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.ai import (
    OLLAMA_TIMEOUT_SECONDS,
    OllamaUnavailableError,
    GenerationCancelledError,
    generate_reply,
    generate_conversation_summary,
    generate_reply_stream,
    generate_ticket_draft,
    password_recovery_guidance,
    preload_model,
)
from app.database import SessionLocal, engine, get_db
from app.knowledge import KnowledgeResult, search_knowledge
from app.models import AuthSession, Conversation, Message, Ticket, User
from app.schemas import (
    ConversationCreateRequest,
    ConversationResponse,
    ConversationTitleUpdateRequest,
    ConversationContinuationPreviewResponse,
    MessageResponse,
    ChatMessageRequest,
    ChatMessageResponse,
    TicketCreateRequest,
    TicketDraftResponse,
    TicketResponse,
    TicketStatus,
    TicketSummaryResponse,
    TicketUpdateRequest,
    UserLoginRequest,
    AuthStatusResponse,
    UserProfileUpdateRequest,
    UserPasswordChangeRequest,
    UserRegistrationRequest,
    UserRegistrationResponse,
    UserResponse,
    KnowledgeSearchRequest,
    KnowledgeSearchResponse,
    KnowledgeSourceResponse,
)
from app.security import hash_password, verify_password

SESSION_COOKIE_NAME = "ai_helpdesk_session"
SESSION_COOKIE_MAX_AGE = 60 * 60 * 8
SESSION_CLEANUP_INTERVAL_SECONDS = 60 * 60
SESSION_CLEANUP_BATCH_SIZE = 500
DATA_RETENTION_MONTHS = 3
DATA_RETENTION_INTERVAL_SECONDS = 24 * 60 * 60
SESSION_COOKIE_SECURE = os.getenv("AUTH_COOKIE_SECURE", "true").lower() == "true"
FRONTEND_ORIGINS = tuple(
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:8088,http://127.0.0.1:8088,"
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
)
DUMMY_PASSWORD_HASH = hash_password("invalid-login-dummy-secret")
LOGIN_IP_ATTEMPT_LIMIT = 20
LOGIN_IP_WINDOW_SECONDS = 60
LOGIN_ACCOUNT_FAILURE_LIMIT = 5
LOGIN_ACCOUNT_WINDOW_SECONDS = 15 * 60
REGISTER_IP_ATTEMPT_LIMIT = 5
REGISTER_IP_WINDOW_SECONDS = 60 * 60
REGISTER_ATTEMPT_SCRIPT = """
local count = redis.call('INCR', KEYS[1])
if count == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
end
return {count, redis.call('TTL', KEYS[1])}
"""
LOGIN_ATTEMPT_CHECK_SCRIPT = """
local ip_count = redis.call('INCR', KEYS[1])
if ip_count == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
end
local account_failures = tonumber(redis.call('GET', KEYS[2]) or '0')
return {
    ip_count,
    account_failures,
    redis.call('TTL', KEYS[1]),
    redis.call('TTL', KEYS[2])
}
"""
RECORD_LOGIN_FAILURE_SCRIPT = """
local account_failures = redis.call('INCR', KEYS[1])
if account_failures == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
end
return {account_failures, redis.call('TTL', KEYS[1])}
"""
TRUSTED_PROXY_NETWORKS = tuple(
    ipaddress.ip_network(value.strip(), strict=False)
    for value in os.getenv("TRUSTED_PROXY_IPS", "").split(",")
    if value.strip()
)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "poro-helpdesk")
OLLAMA_HEALTH_TIMEOUT_SECONDS = 3
CHAT_LOCK_TTL_SECONDS = max(int(OLLAMA_TIMEOUT_SECONDS) + 30, 60)
RELEASE_CHAT_LOCK_SCRIPT = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
    return redis.call('DEL', KEYS[1])
end
return 0
"""
RENEW_CHAT_LOCK_SCRIPT = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
    return redis.call('EXPIRE', KEYS[1], ARGV[2])
end
return 0
"""


class ChatLockLease:
    def __init__(self, key: str, token: str) -> None:
        self.key = key
        self.token = token
        self._stop = threading.Event()
        self._lost = threading.Event()
        self._thread = threading.Thread(target=self._renew_until_stopped, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def _renew_until_stopped(self) -> None:
        interval = max(1, CHAT_LOCK_TTL_SECONDS // 3)
        while not self._stop.wait(interval):
            try:
                renewed = redis_client.eval(
                    RENEW_CHAT_LOCK_SCRIPT, 1, self.key, self.token, CHAT_LOCK_TTL_SECONDS
                )
            except RedisError:
                logger.exception("Could not renew chat lock %s", self.key)
                continue
            if not renewed:
                self._lost.set()
                return

    def assert_owned(self) -> None:
        if self._lost.is_set():
            raise HTTPException(status_code=409, detail="The chat generation lock was lost. Please retry.")
        try:
            renewed = redis_client.eval(
                RENEW_CHAT_LOCK_SCRIPT, 1, self.key, self.token, CHAT_LOCK_TTL_SECONDS
            )
        except RedisError as error:
            raise HTTPException(status_code=503, detail="AI chat lock could not be verified. Please retry.") from error
        if not renewed:
            self._lost.set()
            raise HTTPException(status_code=409, detail="The chat generation lock was lost. Please retry.")

    def stop(self) -> None:
        self._stop.set()
        if self._thread.is_alive():
            self._thread.join(timeout=2)


logger = logging.getLogger(__name__)
redis_client: Redis = Redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)


class GenerationControl:
    """Cancellation handle for one authenticated conversation stream."""

    def __init__(self) -> None:
        self.cancelled = threading.Event()
        self.done = threading.Event()
        self._lock = threading.Lock()
        self._response = None
        self._completed = False

    def attach_response(self, response) -> None:
        with self._lock:
            self._response = response
            should_close = response is not None and self.cancelled.is_set()
        if should_close:
            try:
                response.close()
            except Exception:
                logger.debug("Ollama response was already closed during cancellation.")

    def cancel(self) -> bool:
        with self._lock:
            if self._completed or self.done.is_set():
                return False
            self.cancelled.set()
            response = self._response
        if response is not None:
            try:
                response.close()
            except Exception:
                logger.debug("Ollama response was already closed during cancellation.")
        return True

    def mark_completed(self) -> bool:
        with self._lock:
            if self.cancelled.is_set():
                return False
            self._completed = True
            return True


_active_generations: dict[tuple[int, int], GenerationControl] = {}
_active_generations_lock = threading.Lock()


def require_trusted_origin(request: Request) -> None:
    if request.headers.get("origin") not in FRONTEND_ORIGINS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Request origin is not allowed.",
        )


@contextmanager
def lock_conversation_chat(conversation_id: int) -> Iterator[ChatLockLease]:
    key = f"chat:conversation:{conversation_id}"
    token = secrets.token_urlsafe(24)
    try:
        acquired = redis_client.set(key, token, nx=True, ex=CHAT_LOCK_TTL_SECONDS)
    except RedisError as error:
        raise HTTPException(status_code=503, detail="AI chat is temporarily unavailable.") from error
    if not acquired:
        raise HTTPException(status_code=409, detail="A response is already being generated for this conversation.")

    lease = ChatLockLease(key, token)
    lease.start()
    try:
        yield lease
    finally:
        lease.stop()
        try:
            redis_client.eval(RELEASE_CHAT_LOCK_SCRIPT, 1, key, token)
        except RedisError:
            logger.exception("Could not release chat lock for conversation %s", conversation_id)


@contextmanager
def lock_ai_generation() -> Iterator[ChatLockLease]:
    """Allow one Ollama generation at a time across backend instances sharing Redis."""
    key = "ai:generation:global"
    token = secrets.token_urlsafe(24)
    try:
        acquired = redis_client.set(key, token, nx=True, ex=CHAT_LOCK_TTL_SECONDS)
    except RedisError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI capacity could not be verified. Please try again.",
        ) from error
    if not acquired:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="The AI assistant is busy. Please try again shortly.",
            headers={"Retry-After": "5"},
        )

    lease = ChatLockLease(key, token)
    lease.start()
    try:
        yield lease
    finally:
        lease.stop()
        try:
            redis_client.eval(RELEASE_CHAT_LOCK_SCRIPT, 1, key, token)
        except RedisError:
            logger.exception("Could not release the global AI generation lock.")


def get_client_ip(request: Request) -> str:
    peer_ip = ipaddress.ip_address(
        request.client.host if request.client is not None else "0.0.0.0"
    )
    if not any(peer_ip in network for network in TRUSTED_PROXY_NETWORKS):
        return str(peer_ip)

    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        try:
            forwarded_ips = [
                ipaddress.ip_address(value.strip())
                for value in forwarded_for.split(",")
            ]
        except ValueError:
            return str(peer_ip)

        for forwarded_ip in reversed(forwarded_ips):
            if not any(
                forwarded_ip in network for network in TRUSTED_PROXY_NETWORKS
            ):
                return str(forwarded_ip)
    return str(peer_ip)


def enforce_registration_rate_limit(request: Request) -> None:
    client_ip_hash = hashlib.sha256(get_client_ip(request).encode()).hexdigest()
    try:
        count, ttl = (
            int(value)
            for value in redis_client.eval(
                REGISTER_ATTEMPT_SCRIPT,
                1,
                f"register-limit:ip:{client_ip_hash}",
                REGISTER_IP_WINDOW_SECONDS,
            )
        )
    except RedisError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Registration is temporarily unavailable.",
        ) from error

    if count > REGISTER_IP_ATTEMPT_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many registration attempts. Please try again later.",
            headers={"Retry-After": str(max(ttl, 1))},
        )


def enforce_login_rate_limit(request: Request, email: str) -> None:
    client_ip_hash = hashlib.sha256(get_client_ip(request).encode()).hexdigest()
    account_key = get_login_account_key(email)

    try:
        counts = redis_client.eval(
            LOGIN_ATTEMPT_CHECK_SCRIPT,
            2,
            f"login-limit:ip:{client_ip_hash}",
            account_key,
            LOGIN_IP_WINDOW_SECONDS,
        )
    except RedisError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Sign-in is temporarily unavailable.",
        ) from error

    ip_count, account_failures, ip_ttl, account_ttl = (
        int(value) for value in counts
    )
    retry_after = 0
    if ip_count > LOGIN_IP_ATTEMPT_LIMIT:
        retry_after = max(retry_after, ip_ttl, 1)
    if account_failures >= LOGIN_ACCOUNT_FAILURE_LIMIT:
        retry_after = max(retry_after, account_ttl, 1)
    if retry_after:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many sign-in attempts. Please try again later.",
            headers={"Retry-After": str(retry_after)},
        )


def get_login_account_key(email: str) -> str:
    account_hash = hmac.new(
        get_session_secret(),
        email.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"login-limit:account:{account_hash}"


def record_failed_login(email: str) -> None:
    try:
        failures, ttl = (
            int(value)
            for value in redis_client.eval(
                RECORD_LOGIN_FAILURE_SCRIPT,
                1,
                get_login_account_key(email),
                LOGIN_ACCOUNT_WINDOW_SECONDS,
            )
        )
    except RedisError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Sign-in is temporarily unavailable.",
        ) from error

    # Normally the pre-check blocks at the threshold. This catches concurrent
    # failures that passed the pre-check before another request reached it.
    if failures > LOGIN_ACCOUNT_FAILURE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many sign-in attempts. Please try again later.",
            headers={"Retry-After": str(max(ttl, 1))},
        )


def clear_login_failures(email: str) -> None:
    try:
        redis_client.delete(get_login_account_key(email))
    except RedisError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Sign-in is temporarily unavailable.",
        ) from error


def get_session_secret() -> bytes:
    secret = os.getenv("JWT_SECRET_KEY", "").encode("utf-8")
    if len(secret) < 32:
        raise RuntimeError("JWT_SECRET_KEY must contain at least 32 characters.")
    return secret


def cleanup_expired_sessions() -> None:
    with SessionLocal() as db:
        while True:
            expiration_cutoff = datetime.now(timezone.utc).replace(tzinfo=None)
            expired_session_ids = db.scalars(
                select(AuthSession.id)
                .where(AuthSession.expires_at <= expiration_cutoff)
                .limit(SESSION_CLEANUP_BATCH_SIZE)
            ).all()
            if not expired_session_ids:
                return

            db.execute(
                delete(AuthSession).where(AuthSession.id.in_(expired_session_ids))
            )
            db.commit()


async def cleanup_expired_sessions_periodically() -> None:
    while True:
        try:
            await asyncio.to_thread(cleanup_expired_sessions)
        except SQLAlchemyError:
            logger.exception("Failed to clean up expired authentication sessions.")
        await asyncio.sleep(SESSION_CLEANUP_INTERVAL_SECONDS)


def data_retention_cutoff(now: datetime | None = None) -> datetime:
    current = now or datetime.now(timezone.utc).replace(tzinfo=None)
    month_index = current.year * 12 + current.month - 1 - DATA_RETENTION_MONTHS
    year, month_index = divmod(month_index, 12)
    month = month_index + 1
    day = min(current.day, calendar.monthrange(year, month)[1])
    return current.replace(year=year, month=month, day=day)


def cleanup_retained_data() -> None:
    cutoff = data_retention_cutoff()
    deleted_tickets = 0
    deleted_conversations = 0

    with SessionLocal() as db:
        while True:
            expired_ticket = (
                Ticket.status == TicketStatus.CLOSED.value,
                Ticket.closed_at.is_not(None),
                Ticket.closed_at <= cutoff,
            )
            ticket_ids = db.scalars(
                select(Ticket.id)
                .where(*expired_ticket)
                .order_by(Ticket.id)
                .limit(SESSION_CLEANUP_BATCH_SIZE)
            ).all()
            if not ticket_ids:
                break

            db.execute(
                delete(Ticket).where(Ticket.id.in_(ticket_ids), *expired_ticket)
            )
            db.commit()
            deleted_tickets += len(ticket_ids)

        retained_ticket = (
            select(Ticket.id)
            .where(
                Ticket.conversation_id == Conversation.id,
                or_(
                    Ticket.status != TicketStatus.CLOSED.value,
                    Ticket.closed_at.is_(None),
                    Ticket.closed_at > cutoff,
                ),
            )
            .exists()
        )
        while True:
            conversation_ids = db.scalars(
                select(Conversation.id)
                .where(
                    Conversation.updated_at <= cutoff,
                    ~retained_ticket,
                )
                .order_by(Conversation.id)
                .limit(SESSION_CLEANUP_BATCH_SIZE)
            ).all()
            if not conversation_ids:
                break

            db.execute(
                delete(Conversation).where(
                    Conversation.id.in_(conversation_ids),
                    Conversation.updated_at <= cutoff,
                    ~retained_ticket,
                )
            )
            db.commit()
            deleted_conversations += len(conversation_ids)

    if deleted_tickets or deleted_conversations:
        logger.info(
            "Data retention removed %s closed tickets and %s inactive conversations.",
            deleted_tickets,
            deleted_conversations,
        )


async def cleanup_retained_data_periodically() -> None:
    while True:
        try:
            await asyncio.to_thread(cleanup_retained_data)
        except SQLAlchemyError:
            logger.exception("Failed to clean up retained conversations and tickets.")
        await asyncio.sleep(DATA_RETENTION_INTERVAL_SECONDS)


def create_session_token(user_id: int, expires_at: int, session_id: str) -> str:
    payload = f"{user_id}.{expires_at}.{session_id}"
    signature = hmac.new(
        get_session_secret(),
        payload.encode("ascii"),
        hashlib.sha256,
    ).hexdigest()
    return f"{payload}.{signature}"


def get_session_claims(token: str | None) -> tuple[int, int, str] | None:
    if not token:
        return None

    try:
        user_id_text, expires_at_text, session_id, signature = token.split(".")
        user_id = int(user_id_text)
        expires_at = int(expires_at_text)
    except ValueError:
        return None

    if (
        user_id < 1
        or expires_at <= int(time.time())
        or len(session_id) != 32
        or any(character not in "0123456789abcdef" for character in session_id)
    ):
        return None

    payload = f"{user_id}.{expires_at}.{session_id}"
    expected_signature = hmac.new(
        get_session_secret(),
        payload.encode("ascii"),
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(signature, expected_signature):
        return None
    return user_id, expires_at, session_id


def get_authenticated_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    claims = get_session_claims(request.cookies.get(SESSION_COOKIE_NAME))
    user = None
    if claims is not None:
        user_id, _, session_id = claims
        active_session = db.scalar(
            select(AuthSession.id).where(
                AuthSession.id == session_id,
                AuthSession.user_id == user_id,
                AuthSession.expires_at > datetime.now(timezone.utc).replace(tzinfo=None),
            )
        )
        if active_session is not None:
            user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )
    if user.must_change_password and not (
        request.method == "GET" and request.url.path == "/api/v1/auth/me"
        or request.method == "POST" and request.url.path == "/api/v1/users/me/password"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Password change required before accessing this resource.",
        )
    return user


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    redis_client.ping()
    preload_attempts = 0
    while True:
        try:
            await asyncio.to_thread(preload_model)
            break
        except OllamaUnavailableError as error:
            preload_attempts += 1
            if preload_attempts == 1 or preload_attempts % 12 == 0:
                logger.warning(
                    "Ollama model is not ready yet; retrying startup preload: %s",
                    str(error),
                )
            await asyncio.sleep(5)

    session_cleanup_task = asyncio.create_task(
        cleanup_expired_sessions_periodically()
    )
    retention_cleanup_task = asyncio.create_task(
        cleanup_retained_data_periodically()
    )
    try:
        yield
    finally:
        for task in (session_cleanup_task, retention_cleanup_task):
            task.cancel()
        for task in (session_cleanup_task, retention_cleanup_task):
            try:
                await task
            except asyncio.CancelledError:
                pass
        redis_client.close()


app = FastAPI(
    title="AI HelpDesk API",
    description="REST API for the AI HelpDesk project",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(FRONTEND_ORIGINS),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Content-Type"],
    expose_headers=["X-Chat-Message-Id", "X-Chat-Message-Saved"],
)


@app.middleware("http")
async def apply_api_security_headers(request: Request, call_next):
    if (
        request.method in {"POST", "PUT", "PATCH", "DELETE"}
        and request.url.path.startswith("/api/v1/")
        and request.url.path not in {
            "/api/v1/auth/login",
            "/api/v1/auth/register",
        }
        and request.cookies.get(SESSION_COOKIE_NAME)
        and request.headers.get("origin") not in FRONTEND_ORIGINS
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Request origin is not allowed."},
            headers={
                "Cache-Control": "no-store",
                "X-Content-Type-Options": "nosniff",
                "Referrer-Policy": "strict-origin-when-cross-origin",
                "X-Frame-Options": "DENY",
                "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
            },
        )

    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault(
        "Permissions-Policy",
        "camera=(), microphone=(), geolocation=()",
    )
    if request.url.path.startswith("/api/v1/"):
        response.headers["Cache-Control"] = "no-store"
    return response


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    _ = _request
    errors = [
        {key: value for key, value in error.items() if key != "input"}
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": errors}),
    )


@app.post(
    "/api/v1/auth/login",
    response_model=AuthStatusResponse,
    tags=["Authentication"],
)
def login_user(
    credentials: UserLoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> AuthStatusResponse:
    enforce_login_rate_limit(request, credentials.email)
    user = db.scalar(
        select(User)
        .where(User.email == credentials.email)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    password_hash = user.password_hash if user is not None else DUMMY_PASSWORD_HASH
    password_is_valid = verify_password(
        credentials.password.get_secret_value(),
        password_hash,
    )
    if user is None or not password_is_valid:
        record_failed_login(credentials.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    clear_login_failures(credentials.email)
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    expires_at = int(time.time()) + SESSION_COOKIE_MAX_AGE
    session_id = secrets.token_hex(16)
    db.add(
        AuthSession(
            id=session_id,
            user_id=user.id,
            expires_at=datetime.fromtimestamp(expires_at, timezone.utc).replace(
                tzinfo=None
            ),
            created_at=now,
        )
    )
    db.commit()

    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=create_session_token(user.id, expires_at, session_id),
        max_age=SESSION_COOKIE_MAX_AGE,
        httponly=True,
        secure=SESSION_COOKIE_SECURE,
        samesite="lax",
        path="/",
    )
    response.headers["Cache-Control"] = "no-store"
    return AuthStatusResponse(must_change_password=user.must_change_password)


@app.get(
    "/api/v1/auth/me",
    response_model=AuthStatusResponse,
    tags=["Authentication"],
)
def get_current_user(
    response: Response,
    user: User = Depends(get_authenticated_user),
) -> AuthStatusResponse:
    response.headers["Cache-Control"] = "no-store"
    return AuthStatusResponse(must_change_password=user.must_change_password)


@app.get(
    "/api/v1/users/me",
    response_model=UserResponse,
    tags=["Users"],
)
def get_current_user_profile(
    response: Response,
    user: User = Depends(get_authenticated_user),
) -> UserResponse:
    response.headers["Cache-Control"] = "no-store"
    return UserResponse.model_validate(user)


@app.patch(
    "/api/v1/users/me",
    response_model=UserResponse,
    tags=["Users"],
)
def update_current_user_profile(
    profile_data: UserProfileUpdateRequest,
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> UserResponse:
    updates = profile_data.model_dump(exclude_unset=True)
    if "username" in updates:
        existing_username = db.scalar(
            select(User.id).where(
                User.username == updates["username"],
                User.id != user.id,
            )
        )
        if existing_username is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username is already registered.",
            )

    for field, value in updates.items():
        setattr(user, field, value)
    user.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already registered.",
        ) from None
    return UserResponse.model_validate(user)


@app.post(
    "/api/v1/users/me/password",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Users"],
)
def change_current_user_password(
    password_data: UserPasswordChangeRequest,
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> Response:
    # Serialize password changes with logins using the same user-row lock.
    # populate_existing ensures this transaction checks the latest committed hash.
    locked_user = db.scalar(
        select(User)
        .where(User.id == user.id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if locked_user is None or not verify_password(
        password_data.current_password.get_secret_value(),
        locked_user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect.",
        )
    locked_user.password_hash = hash_password(
        password_data.new_password.get_secret_value()
    )
    locked_user.must_change_password = False
    db.execute(delete(AuthSession).where(AuthSession.user_id == locked_user.id))
    locked_user.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.commit()
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        httponly=True,
        secure=SESSION_COOKIE_SECURE,
        samesite="lax",
        path="/",
    )
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get(
    "/api/v1/tickets",
    response_model=list[TicketResponse],
    tags=["Tickets"],
)
def list_tickets(
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> list[TicketResponse]:
    tickets = db.scalars(
        select(Ticket)
        .where(Ticket.user_id == user.id)
        .order_by(Ticket.created_at.desc(), Ticket.id.desc())
    ).all()
    return [TicketResponse.model_validate(ticket) for ticket in tickets]


@app.post(
    "/api/v1/tickets",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Tickets"],
)
def create_ticket(
    ticket_data: TicketCreateRequest,
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> TicketResponse:
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    ticket = Ticket(
        user_id=user.id,
        conversation_id=None,
        title=ticket_data.title,
        description=ticket_data.description,
        status=TicketStatus.OPEN.value,
        priority=ticket_data.priority.value,
        created_at=now,
        updated_at=now,
        closed_at=None,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return TicketResponse.model_validate(ticket)


@app.get(
    "/api/v1/tickets/summary",
    response_model=TicketSummaryResponse,
    tags=["Tickets"],
)
def get_ticket_summary(
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> TicketSummaryResponse:
    counts = db.execute(
        select(
            func.count(Ticket.id),
            func.sum(case((Ticket.status == TicketStatus.OPEN.value, 1), else_=0)),
            func.sum(case((Ticket.status == TicketStatus.CLOSED.value, 1), else_=0)),
        ).where(Ticket.user_id == user.id)
    ).one()
    return TicketSummaryResponse(
        total=counts[0],
        open=counts[1] or 0,
        closed=counts[2] or 0,
    )


@app.get(
    "/api/v1/tickets/{ticket_id}",
    response_model=TicketResponse,
    tags=["Tickets"],
)
def get_ticket(
    ticket_id: int = Path(gt=0),
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> TicketResponse:
    ticket = db.scalar(
        select(Ticket).where(
            Ticket.id == ticket_id,
            Ticket.user_id == user.id,
        )
    )
    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found.",
        )
    return TicketResponse.model_validate(ticket)


@app.patch(
    "/api/v1/tickets/{ticket_id}",
    response_model=TicketResponse,
    tags=["Tickets"],
)
def update_ticket(
    ticket_data: TicketUpdateRequest,
    ticket_id: int = Path(gt=0),
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> TicketResponse:
    ticket = db.scalar(
        select(Ticket).where(
            Ticket.id == ticket_id,
            Ticket.user_id == user.id,
        )
    )
    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found.",
        )
    if ticket.status != TicketStatus.OPEN.value:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only open tickets can be updated.",
        )

    updates = ticket_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        if isinstance(value, Enum):
            value = value.value
        setattr(ticket, field, value)
    ticket.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.commit()
    db.refresh(ticket)
    return TicketResponse.model_validate(ticket)


@app.post(
    "/api/v1/tickets/{ticket_id}/close",
    response_model=TicketResponse,
    tags=["Tickets"],
)
def close_ticket(
    ticket_id: int = Path(gt=0),
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> TicketResponse:
    ticket = db.scalar(
        select(Ticket).where(
            Ticket.id == ticket_id,
            Ticket.user_id == user.id,
        )
    )
    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found.",
        )
    if ticket.status != TicketStatus.OPEN.value:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ticket is already closed.",
        )

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    ticket.status = TicketStatus.CLOSED.value
    ticket.closed_at = now
    ticket.updated_at = now
    db.commit()
    db.refresh(ticket)
    return TicketResponse.model_validate(ticket)


@app.post(
    "/api/v1/auth/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Authentication"],
)
def logout_user(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> Response:
    require_trusted_origin(request)

    response.headers["Cache-Control"] = "no-store"
    claims = get_session_claims(request.cookies.get(SESSION_COOKIE_NAME))
    if claims is not None:
        _, _, session_id = claims
        db.execute(delete(AuthSession).where(AuthSession.id == session_id))
        db.commit()
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        httponly=True,
        secure=SESSION_COOKIE_SECURE,
        samesite="lax",
        path="/",
    )
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@app.post(
    "/api/v1/auth/register",
    response_model=UserRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"],
)
def register_user(
    registration: UserRegistrationRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> UserRegistrationResponse:
    enforce_registration_rate_limit(request)
    # Check both fields before returning a conflict
    existing_email = db.scalar(
        select(User.id).where(User.email == registration.email)
    )
    existing_username = db.scalar(
        select(User.id).where(User.username == registration.username)
    )
    conflicts = []
    if existing_email is not None:
        conflicts.append("Email address")
    if existing_username is not None:
        conflicts.append("Username")
    if conflicts:
        verb = "are" if len(conflicts) > 1 else "is"
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{' and '.join(conflicts)} {verb} already registered.",
        )

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    user = User(
        first_name=registration.first_name,
        last_name=registration.last_name,
        username=registration.username,
        email=registration.email,
        password_hash=hash_password(registration.password.get_secret_value()),
        created_at=now,
        updated_at=now,
    )
    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError as error:
        db.rollback()
        if not error.orig.args or error.orig.args[0] != 1062:
            raise
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email address or username is already registered.",
        ) from None

    return UserRegistrationResponse(user=UserResponse.model_validate(user))


@app.get("/api/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "ai-helpdesk-backend",
    }


@app.get("/api/health/db", tags=["Health"])
def database_health_check() -> dict[str, str]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected",
        }
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed",
        )


@app.get("/api/v1/conversations", response_model=list[ConversationResponse], tags=["Conversations"])
def list_conversations(
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> list[ConversationResponse]:
    items = db.scalars(
        select(Conversation).where(Conversation.user_id == user.id)
        .order_by(Conversation.updated_at.desc(), Conversation.id.desc())
    ).all()
    return [ConversationResponse.model_validate(item) for item in items]


@app.post(
    "/api/v1/conversations/{conversation_id}/continuation-preview",
    response_model=ConversationContinuationPreviewResponse,
    tags=["Conversations"],
)
async def preview_conversation_continuation(
    request: Request,
    conversation_id: int = Path(gt=0),
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> ConversationContinuationPreviewResponse:
    require_trusted_origin(request)
    owned_conversation = db.scalar(
        select(Conversation.id).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user.id,
        )
    )
    if owned_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    db.rollback()
    try:
        with lock_conversation_chat(conversation_id) as chat_lock:
            conversation = db.scalar(
                select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user.id,
                )
            )
            if conversation is None:
                raise HTTPException(status_code=404, detail="Conversation not found.")

            messages = db.scalars(
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.asc(), Message.id.asc())
            ).all()
            response_language = conversation.response_language
            context_summary = conversation.context_summary
            if not any(message.role == "USER" for message in messages) and not context_summary:
                raise HTTPException(status_code=400, detail="The conversation has no context to continue.")

            ollama_messages = [
                {"role": "user" if message.role == "USER" else "assistant", "content": message.content}
                for message in messages
            ]
            db.rollback()

            with lock_ai_generation() as ai_lock:
                summary = await asyncio.to_thread(
                    generate_conversation_summary,
                    ollama_messages,
                    response_language,
                    context_summary,
                )
                chat_lock.assert_owned()
                ai_lock.assert_owned()
    except OllamaUnavailableError:
        raise HTTPException(
            status_code=503,
            detail="The AI could not prepare a conversation summary. Please try again.",
        ) from None

    return ConversationContinuationPreviewResponse(
        title=summary.title,
        context_summary=summary.context_summary,
    )

@app.post(
    "/api/v1/conversations",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Conversations"],
)
def create_conversation(
    conversation_data: ConversationCreateRequest,
    request: Request,
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> ConversationResponse:
    require_trusted_origin(request)
    parent_id = conversation_data.parent_conversation_id
    if parent_id is not None:
        parent = db.scalar(
            select(Conversation.id).where(
                Conversation.id == parent_id,
                Conversation.user_id == user.id,
            )
        )
        if parent is None:
            raise HTTPException(status_code=404, detail="Parent conversation not found.")
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    item = Conversation(
        user_id=user.id,
        title=conversation_data.title,
        parent_conversation_id=parent_id,
        context_summary=conversation_data.context_summary,
        created_at=now,
        updated_at=now,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return ConversationResponse.model_validate(item)


@app.patch(
    "/api/v1/conversations/{conversation_id}/title",
    response_model=ConversationResponse,
    tags=["Conversations"],
)
def update_conversation_title(
    title_data: ConversationTitleUpdateRequest,
    request: Request,
    conversation_id: int = Path(gt=0),
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> ConversationResponse:
    require_trusted_origin(request)
    item = db.scalar(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user.id,
        )
    )
    if item is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    item.title = title_data.title
    item.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.commit()
    db.refresh(item)
    return ConversationResponse.model_validate(item)


@app.get("/api/v1/conversations/{conversation_id}",
         response_model=ConversationResponse, tags=["Conversations"])
def get_conversation(
    conversation_id: int = Path(gt=0),
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> ConversationResponse:
    item = db.scalar(select(Conversation).where(
        Conversation.id == conversation_id, Conversation.user_id == user.id
    ))
    if item is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    return ConversationResponse.model_validate(item)


@app.get("/api/v1/conversations/{conversation_id}/messages",
         response_model=list[MessageResponse], tags=["Conversations"])
def list_conversation_messages(
    conversation_id: int = Path(gt=0),
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> list[MessageResponse]:
    owned_id = db.scalar(select(Conversation.id).where(
        Conversation.id == conversation_id, Conversation.user_id == user.id
    ))
    if owned_id is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    items = db.scalars(select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc(), Message.id.asc())).all()
    return [MessageResponse.model_validate(item) for item in items]


@app.post(
    "/api/v1/conversations/{conversation_id}/ticket-draft",
    response_model=TicketDraftResponse,
    tags=["Tickets"],
)
async def create_conversation_ticket_draft(
    request: Request,
    conversation_id: int = Path(gt=0),
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> TicketDraftResponse:
    require_trusted_origin(request)
    conversation = db.scalar(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user.id,
        )
    )
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    messages = db.scalars(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc(), Message.id.desc())
        .limit(20)
    ).all()
    messages.reverse()
    if not any(message.role == "USER" for message in messages):
        raise HTTPException(status_code=400, detail="The conversation has no user messages.")
    ollama_messages = [
        {"role": "user" if message.role == "USER" else "assistant", "content": message.content}
        for message in messages
    ]
    response_language = conversation.response_language
    context_summary = conversation.context_summary
    db.rollback()
    try:
        with lock_ai_generation() as ai_lock:
            generated = await asyncio.to_thread(
                generate_ticket_draft,
                ollama_messages,
                response_language,
                context_summary,
            )
            ai_lock.assert_owned()
    except OllamaUnavailableError as error:
        logger.warning("AI ticket draft generation failed: %s", str(error))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI could not prepare the support ticket. Please try again.",
        ) from None
    return TicketDraftResponse(title=generated.title, description=generated.description)


@app.post(
    "/api/v1/conversations/{conversation_id}/tickets",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Tickets"],
)
def create_ticket_from_conversation(
    ticket_data: TicketCreateRequest,
    conversation_id: int = Path(gt=0),
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> TicketResponse:
    conversation = db.scalar(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user.id,
        )
    )
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    ticket = Ticket(
        user_id=user.id,
        conversation_id=conversation.id,
        title=ticket_data.title,
        description=ticket_data.description,
        status=TicketStatus.OPEN.value,
        priority=ticket_data.priority.value,
        created_at=now,
        updated_at=now,
        closed_at=None,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return TicketResponse.model_validate(ticket)


def build_knowledge_context(query: str) -> tuple[list[KnowledgeResult], str, list[str]]:
    """Retrieve bounded excerpts and assign request-local IDs for validated citations."""
    results = search_knowledge(query, limit=3)
    source_ids = [f"kb-{index}" for index in range(1, len(results) + 1)]
    excerpts = []
    for source_id, item in zip(source_ids, results):
        excerpts.append(
            f"ID: {source_id} | Source: {item['title']} | {item['source']} | "
            f"Section: {item['section']} | Status: {item['status']}\n"
            f"{item['content'][:2200]}"
        )
    context = (
        "\n\n".join(excerpts)[:7000]
        if excerpts
        else "No matching local Knowledge Base source was retrieved. "
             "Do not imply that local documentation supports the answer. "
             "Give safe general guidance only when appropriate."
    )
    return results, context, source_ids


def format_knowledge_sources(
    results: list[KnowledgeResult],
    source_ids: tuple[str, ...] | list[str],
) -> str:
    """Render only retrieved sources explicitly selected by the model."""
    selected = set(source_ids)
    lines = [
        f"- {item['title']} — {item['source']} "
        f"(section: {item['section']}; status: {item['status']})"
        for index, item in enumerate(results, start=1)
        if f"kb-{index}" in selected
    ]
    return "\n\nSources / Lähteet:\n" + "\n".join(lines) if lines else ""


def build_effective_chat_history(
    db: Session,
    conversation_id: int,
    through_message_id: int,
    context_limit: int = 20,
) -> tuple[list[dict[str, str]], str]:
    """Use recent answered context and combine all pending user messages."""
    last_answer_id = db.scalar(
        select(Message.id)
        .where(
            Message.conversation_id == conversation_id,
            Message.id < through_message_id,
            Message.role == "ASSISTANT",
        )
        .order_by(Message.id.desc())
        .limit(1)
    )
    pending_query = select(Message).where(
        Message.conversation_id == conversation_id,
        Message.id <= through_message_id,
        Message.role == "USER",
    )
    if last_answer_id is not None:
        pending_query = pending_query.where(Message.id > last_answer_id)
    pending = db.scalars(pending_query.order_by(Message.id.asc())).all()

    context = []
    if last_answer_id is not None:
        context_query = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.id <= last_answer_id,
            )
            .order_by(Message.id.desc())
            .limit(context_limit)
        )
        context = list(reversed(db.scalars(context_query).all()))

    effective_user_content = "\n\n".join(item.content for item in pending)
    messages = [
        {"role": "user" if item.role == "USER" else "assistant", "content": item.content}
        for item in context
    ]
    if effective_user_content:
        messages.append({"role": "user", "content": effective_user_content})
    return messages, effective_user_content


async def generate_assistant_for_message(
    conversation_id: int,
    user_message_id: int,
    db: Session,
    chat_lock: ChatLockLease,
) -> MessageResponse:
    ollama_messages, latest_user_content = build_effective_chat_history(
        db, conversation_id, user_message_id
    )

    conversation = db.get(Conversation, conversation_id)
    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )
    response_language = conversation.response_language
    context_summary = conversation.context_summary
    db.rollback()
    retrieved_knowledge, knowledge_context, knowledge_source_ids = build_knowledge_context(
        latest_user_content
    )
    recovery_guidance = password_recovery_guidance(latest_user_content)
    saved_response_language = None
    if recovery_guidance is not None:
        _, answer_content = recovery_guidance
        source_ids = [
            f"kb-{index}"
            for index, item in enumerate(retrieved_knowledge, start=1)
            if item["source"] == "knowledge/11-account-access-and-password-recovery.md"
        ]
    else:
        with lock_ai_generation() as ai_lock:
            generated_reply = await asyncio.to_thread(
                generate_reply,
                ollama_messages,
                response_language,
                knowledge_context,
                knowledge_source_ids,
                context_summary=context_summary,
            )
            ai_lock.assert_owned()
        answer_content = generated_reply.content.strip()
        saved_response_language = generated_reply.response_language
        source_ids = list(generated_reply.source_ids)
    if not answer_content:
        raise OllamaUnavailableError("Ollama returned an empty reply")
    answer_content += format_knowledge_sources(retrieved_knowledge, source_ids)

    chat_lock.assert_owned()
    assistant_message = Message(
        conversation_id=conversation_id,
        role="ASSISTANT",
        content=answer_content,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
    )
    with SessionLocal() as persistence_db:
        conversation = persistence_db.get(Conversation, conversation_id)
        if conversation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found.",
            )
        latest_message = persistence_db.scalar(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.id.desc())
            .limit(1)
        )
        if latest_message is None or latest_message.id != user_message_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The unanswered message has changed. Please reload the conversation.",
            )
        chat_lock.assert_owned()
        persistence_db.add(assistant_message)
        conversation.response_language = saved_response_language
        conversation.updated_at = assistant_message.created_at
        chat_lock.assert_owned()
        persistence_db.commit()
        persistence_db.refresh(assistant_message)

    return MessageResponse.model_validate(assistant_message)


@app.post(
    "/api/v1/conversations/{conversation_id}/messages/stop",
    tags=["Conversations"],
)
async def stop_chat_generation(
    request: Request,
    conversation_id: int = Path(gt=0),
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> dict[str, bool]:
    require_trusted_origin(request)
    owned = db.scalar(
        select(Conversation.id).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user.id,
        )
    )
    if owned is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")

    key = (user.id, conversation_id)
    with _active_generations_lock:
        control = _active_generations.get(key)
    if control is None:
        return {"cancelled": False}
    cancelled = control.cancel()
    if cancelled:
        finished = await asyncio.to_thread(control.done.wait, OLLAMA_TIMEOUT_SECONDS + 5)
        if not finished:
            raise HTTPException(
                status_code=503,
                detail="The generation is still shutting down. Please wait before sending another message.",
            )
    return {"cancelled": cancelled}


@app.post(
    "/api/v1/conversations/{conversation_id}/messages/stream",
    tags=["Conversations"],
)
def stream_chat_message(
    message_data: ChatMessageRequest,
    request: Request,
    conversation_id: int = Path(gt=0),
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> StreamingResponse:
    require_trusted_origin(request)
    authenticated_user_id = user.id
    owned_conversation = db.scalar(
        select(Conversation.id).where(
            Conversation.id == conversation_id,
            Conversation.user_id == authenticated_user_id,
        )
    )
    if owned_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    db.rollback()

    generation_key = (authenticated_user_id, conversation_id)
    generation_control = GenerationControl()
    with _active_generations_lock:
        if generation_key in _active_generations:
            raise HTTPException(status_code=409, detail="A response is already being generated.")
        _active_generations[generation_key] = generation_control

    def event_stream():
        user_message_id: int | None = None

        def event(name: str, payload: dict[str, object]) -> str:
            import json
            return json.dumps({"event": name, **payload}, ensure_ascii=False) + "\n"

        try:
            with lock_conversation_chat(conversation_id) as chat_lock:
                with SessionLocal() as message_db:
                    conversation = message_db.scalar(
                        select(Conversation).where(
                            Conversation.id == conversation_id,
                            Conversation.user_id == authenticated_user_id,
                        ).with_for_update()
                    )
                    if conversation is None:
                        yield event("error", {"detail": "Conversation not found."})
                        return
                    now = datetime.now(timezone.utc).replace(tzinfo=None)
                    user_message = Message(
                        conversation_id=conversation_id,
                        role="USER",
                        content=message_data.content,
                        created_at=now,
                    )
                    message_db.add(user_message)
                    if not conversation.title:
                        conversation.title = message_data.content[:80]
                    conversation.updated_at = now
                    message_db.commit()
                    message_db.refresh(user_message)
                    user_message_id = user_message.id
                    user_message_payload = MessageResponse.model_validate(user_message).model_dump(mode="json")

                    ollama_messages, effective_user_content = build_effective_chat_history(
                        message_db, conversation_id, user_message_id
                    )
                    response_language = conversation.response_language
                    context_summary = conversation.context_summary
                    message_db.rollback()

                yield event("user_message", {"message": user_message_payload})
                if generation_control.cancelled.is_set():
                    yield event("cancelled", {})
                    return
                chunks: list[str] = []
                saved_language = response_language
                ticket_recommended = False
                validated_source_ids: list[str] = []
                try:
                    if generation_control.cancelled.is_set():
                        raise GenerationCancelledError()
                    retrieved_knowledge, knowledge_context, knowledge_source_ids = build_knowledge_context(
                        effective_user_content
                    )
                    if generation_control.cancelled.is_set():
                        raise GenerationCancelledError()
                    recovery_guidance = password_recovery_guidance(
                        effective_user_content
                    )
                    if recovery_guidance is not None:
                        _, guidance_text = recovery_guidance
                        saved_language = None
                        chunks.append(guidance_text)
                        yield event("token", {"content": guidance_text})
                        validated_source_ids = [
                            f"kb-{index}"
                            for index, item in enumerate(retrieved_knowledge, start=1)
                            if item["source"] == "knowledge/11-account-access-and-password-recovery.md"
                        ]
                    else:
                        with lock_ai_generation() as ai_lock:
                            for kind, value in generate_reply_stream(
                                ollama_messages,
                                response_language,
                                knowledge_context,
                                knowledge_source_ids,
                                cancel_event=generation_control.cancelled,
                                on_response=generation_control.attach_response,
                                context_summary=context_summary,
                            ):
                                chat_lock.assert_owned()
                                ai_lock.assert_owned()
                                if kind == "language":
                                    saved_language = value
                                elif kind == "ticket_recommendation":
                                    ticket_recommended = value is True
                                elif kind == "sources":
                                    validated_source_ids = value
                                elif kind == "content":
                                    chunks.append(value)
                                    yield event("token", {"content": value})
                                elif kind == "usage":
                                    context_tokens = value["context_tokens"]
                                    with SessionLocal() as usage_db:
                                        usage_conversation = usage_db.get(Conversation, conversation_id)
                                        if usage_conversation is not None and usage_conversation.user_id == authenticated_user_id:
                                            usage_conversation.last_context_tokens = context_tokens
                                            usage_db.commit()
                                    yield event("context_usage", value)
                except GenerationCancelledError:
                    yield event("cancelled", {})
                    return
                except OllamaUnavailableError:
                    yield event("error", {
                        "detail": "AI assistant is temporarily unavailable. Your message was saved.",
                        "saved_message_id": user_message_id,
                    })
                    return

                if generation_control.cancelled.is_set():
                    yield event("cancelled", {})
                    return
                full_content = "".join(chunks).strip()
                if not full_content:
                    yield event("error", {
                        "detail": "AI assistant returned an empty response. Your message was saved.",
                        "saved_message_id": user_message_id,
                    })
                    return

                full_content += format_knowledge_sources(retrieved_knowledge, validated_source_ids)
                chat_lock.assert_owned()
                if not generation_control.mark_completed():
                    yield event("cancelled", {})
                    return
                assistant_message = Message(
                    conversation_id=conversation_id,
                    role="ASSISTANT",
                    content=full_content,
                    created_at=datetime.now(timezone.utc).replace(tzinfo=None),
                )
                with SessionLocal() as persistence_db:
                    conversation = persistence_db.get(Conversation, conversation_id)
                    if conversation is None or conversation.user_id != authenticated_user_id:
                        yield event("error", {"detail": "Conversation not found."})
                        return
                    latest_message = persistence_db.scalar(
                        select(Message)
                        .where(Message.conversation_id == conversation_id)
                        .order_by(Message.id.desc())
                        .limit(1)
                    )
                    if latest_message is None or latest_message.id != user_message_id:
                        yield event("error", {
                            "detail": "The unanswered message has changed. Please reload the conversation.",
                            "saved_message_id": user_message_id,
                        })
                        return
                    chat_lock.assert_owned()
                    persistence_db.add(assistant_message)
                    conversation.response_language = saved_language
                    conversation.updated_at = assistant_message.created_at
                    chat_lock.assert_owned()
                    persistence_db.commit()
                    persistence_db.refresh(assistant_message)
                    assistant_payload = MessageResponse.model_validate(assistant_message).model_dump(mode="json")
                yield event("done", {
                    "assistant_message": assistant_payload,
                    "ticket_recommended": ticket_recommended,
                })
        except HTTPException as error:
            payload: dict[str, object] = {"detail": error.detail}
            if user_message_id is not None:
                payload["saved_message_id"] = user_message_id
            yield event("error", payload)
        except Exception:
            logger.exception("Unexpected error while streaming chat for conversation %s", conversation_id)
            payload: dict[str, object] = {
                "detail": "The AI response could not be completed. Your message may have been saved."
            }
            if user_message_id is not None:
                payload["saved_message_id"] = user_message_id
            yield event("error", payload)
        finally:
            with _active_generations_lock:
                if _active_generations.get(generation_key) is generation_control:
                    _active_generations.pop(generation_key, None)
            generation_control.done.set()

    return StreamingResponse(
        event_stream(),
        media_type="application/x-ndjson",
        headers={"Cache-Control": "no-cache, no-transform", "X-Accel-Buffering": "no"},
    )


@app.post(
    "/api/v1/conversations/{conversation_id}/messages",
    response_model=ChatMessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Conversations"],
)
async def send_chat_message(
    message_data: ChatMessageRequest,
    request: Request,
    conversation_id: int = Path(gt=0),
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> ChatMessageResponse:
    require_trusted_origin(request)
    authenticated_user_id = user.id

    owned_conversation = db.scalar(
        select(Conversation.id).where(
            Conversation.id == conversation_id,
            Conversation.user_id == authenticated_user_id,
        )
    )
    if owned_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    db.rollback()

    with lock_conversation_chat(conversation_id) as chat_lock:
        conversation = db.scalar(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == authenticated_user_id,
            ).with_for_update()
        )
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found.")

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        user_message = Message(
            conversation_id=conversation.id,
            role="USER",
            content=message_data.content,
            created_at=now,
        )
        db.add(user_message)
        if not conversation.title:
            conversation.title = message_data.content[:80]
        conversation.updated_at = now
        db.commit()
        db.refresh(user_message)
        user_message_id = user_message.id
        user_message_response = MessageResponse.model_validate(user_message)

        try:
            assistant_message_response = await generate_assistant_for_message(
                conversation_id,
                user_message_id,
                db,
                chat_lock,
            )
        except OllamaUnavailableError as error:
            logger.warning("Ollama chat request failed: %s", str(error))
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI assistant is temporarily unavailable. Your message was saved.",
                headers={
                    "X-Chat-Message-Saved": "true",
                    "X-Chat-Message-Id": str(user_message_id),
                },
            ) from None

        return ChatMessageResponse(
            conversation_id=conversation_id,
            user_message=user_message_response,
            assistant_message=assistant_message_response,
        )


@app.post(
    "/api/v1/conversations/{conversation_id}/messages/{message_id}/retry",
    response_model=ChatMessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Conversations"],
)
async def retry_chat_message(
    request: Request,
    conversation_id: int = Path(gt=0),
    message_id: int = Path(gt=0),
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> ChatMessageResponse:
    require_trusted_origin(request)
    authenticated_user_id = user.id

    owned_conversation = db.scalar(
        select(Conversation.id).where(
            Conversation.id == conversation_id,
            Conversation.user_id == authenticated_user_id,
        )
    )
    if owned_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    db.rollback()

    with lock_conversation_chat(conversation_id) as chat_lock:
        conversation = db.scalar(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == authenticated_user_id,
            ).with_for_update()
        )
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found.")

        failed_message = db.scalar(
            select(Message).where(
                Message.id == message_id,
                Message.conversation_id == conversation_id,
                Message.role == "USER",
            )
        )
        latest_message = db.scalar(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.id.desc())
            .limit(1)
        )
        if failed_message is None or latest_message is None or latest_message.id != message_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Only the latest unanswered message can be retried.",
            )
        user_message_response = MessageResponse.model_validate(failed_message)

        try:
            assistant_message_response = await generate_assistant_for_message(
                conversation_id,
                message_id,
                db,
                chat_lock,
            )
        except OllamaUnavailableError as error:
            logger.warning("Ollama chat retry failed: %s", str(error))
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI assistant is temporarily unavailable. Your message is still saved.",
                headers={
                    "X-Chat-Message-Saved": "true",
                    "X-Chat-Message-Id": str(message_id),
                },
            ) from None

        return ChatMessageResponse(
            conversation_id=conversation_id,
            user_message=user_message_response,
            assistant_message=assistant_message_response,
        )


@app.post(
    "/api/v1/knowledge/search",
    response_model=KnowledgeSearchResponse,
    tags=["Knowledge"],
)
def search_knowledge_endpoint(
    search_data: KnowledgeSearchRequest,
    request: Request,
    _user: User = Depends(get_authenticated_user),
) -> KnowledgeSearchResponse:
    require_trusted_origin(request)
    results = search_knowledge(search_data.query, search_data.limit)
    return KnowledgeSearchResponse(
        query=search_data.query,
        results=[
            KnowledgeSourceResponse(
                title=item["title"],
                source=item["source"],
                section=item["section"],
                status=item["status"],
                excerpt=item["excerpt"],
                score=item["score"],
            )
            for item in results
        ],
    )


def get_running_model_context() -> int | None:
    import json
    from urllib.request import urlopen

    try:
        with urlopen(f"{OLLAMA_BASE_URL}/api/ps", timeout=OLLAMA_HEALTH_TIMEOUT_SECONDS) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception:
        logger.debug("Could not retrieve the running Ollama model context length.")
        return None

    models = payload.get("models", []) if isinstance(payload, dict) else []
    for model in models:
        if not isinstance(model, dict):
            continue
        name = model.get("name") or model.get("model")
        if isinstance(name, str) and (name == OLLAMA_MODEL or name.startswith(f"{OLLAMA_MODEL}:")):
            context_length = model.get("context_length")
            if isinstance(context_length, int) and context_length > 0:
                return context_length
    return None


@app.get("/api/v1/ai/context", tags=["AI"])
async def get_ai_context_status(
    _user: User = Depends(get_authenticated_user),
) -> dict[str, int | str | None]:
    context_length = await asyncio.to_thread(get_running_model_context)
    return {"model": OLLAMA_MODEL, "context_length": context_length}


@app.get("/api/v1/ai/health", tags=["AI"])
async def ollama_health_check(
    _user: User = Depends(get_authenticated_user),
) -> dict[str, object]:
    """Check Ollama availability and whether the configured model is installed."""
    import json
    from urllib.error import URLError
    from urllib.request import urlopen

    def fetch_ollama_status() -> tuple[str | None, list[str] | None]:
        version: str | None = None
        model_names: list[str] | None = None

        with urlopen(
            f"{OLLAMA_BASE_URL}/api/version",
            timeout=OLLAMA_HEALTH_TIMEOUT_SECONDS,
        ) as response:
            version_payload = json.loads(response.read().decode("utf-8"))
            version = version_payload.get("version")

        with urlopen(
            f"{OLLAMA_BASE_URL}/api/tags",
            timeout=OLLAMA_HEALTH_TIMEOUT_SECONDS,
        ) as response:
            tags_payload = json.loads(response.read().decode("utf-8"))
            model_names = [
                item.get("name", "")
                for item in tags_payload.get("models", [])
                if isinstance(item, dict)
            ]
        return version, model_names

    try:
        version, model_names = await asyncio.to_thread(fetch_ollama_status)
    except (OSError, URLError, TimeoutError, ValueError) as error:
        logger.warning("Ollama health check failed: %s", type(error).__name__)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unavailable",
                "provider": "ollama",
                "connected": False,
                "model": OLLAMA_MODEL,
                "model_available": False,
            },
        ) from None

    available_models = set(model_names or [])
    model_available = any(
        name == OLLAMA_MODEL or name.startswith(f"{OLLAMA_MODEL}:")
        for name in available_models
    )
    result: dict[str, object] = {
        "status": "ok" if model_available else "degraded",
        "provider": "ollama",
        "connected": True,
        "version": version,
        "model": OLLAMA_MODEL,
        "model_available": model_available,
    }
    if not model_available:
        result["available_models"] = sorted(available_models)

    if not model_available:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=result,
        )
    return result
