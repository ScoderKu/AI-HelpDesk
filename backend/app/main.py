import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
import hashlib
import hmac
import ipaddress
import logging
import os
import secrets
import time

from fastapi import Depends, FastAPI, HTTPException, Path, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from redis import Redis
from redis.exceptions import RedisError
from sqlalchemy import case, delete, func, select, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, get_db
from app.models import AuthSession, Ticket, User
from app.schemas import (
    TicketCreateRequest,
    TicketResponse,
    TicketStatus,
    TicketSummaryResponse,
    TicketUpdateRequest,
    UserLoginRequest,
    UserProfileUpdateRequest,
    UserPasswordChangeRequest,
    UserRegistrationRequest,
    UserRegistrationResponse,
    UserResponse,
)
from app.security import hash_password, verify_password

SESSION_COOKIE_NAME = "ai_helpdesk_session"
SESSION_COOKIE_MAX_AGE = 60 * 60 * 8
SESSION_CLEANUP_INTERVAL_SECONDS = 60 * 60
SESSION_CLEANUP_BATCH_SIZE = 500
SESSION_COOKIE_SECURE = os.getenv("AUTH_COOKIE_SECURE", "true").lower() == "true"
FRONTEND_ORIGINS = tuple(
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:8088,http://127.0.0.1:8088",
    ).split(",")
    if origin.strip()
)
DUMMY_PASSWORD_HASH = hash_password("invalid-login-dummy-secret")
LOGIN_IP_ATTEMPT_LIMIT = 20
LOGIN_IP_WINDOW_SECONDS = 60
LOGIN_ACCOUNT_FAILURE_LIMIT = 5
LOGIN_ACCOUNT_WINDOW_SECONDS = 15 * 60
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
logger = logging.getLogger(__name__)
redis_client: Redis = Redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)


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
    return user


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    redis_client.ping()
    session_cleanup_task = asyncio.create_task(
        cleanup_expired_sessions_periodically()
    )
    try:
        yield
    finally:
        session_cleanup_task.cancel()
        try:
            await session_cleanup_task
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
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    response_model=UserResponse,
    tags=["Authentication"],
)
def login_user(
    credentials: UserLoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> UserResponse:
    enforce_login_rate_limit(request, credentials.email)
    user = db.scalar(select(User).where(User.email == credentials.email))
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
    return UserResponse.model_validate(user)


@app.get(
    "/api/v1/auth/me",
    response_model=UserResponse,
    tags=["Authentication"],
)
def get_current_user(
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
    existing_username = db.scalar(
        select(User.id).where(
            User.username == profile_data.username,
            User.id != user.id,
        )
    )
    if existing_username is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already registered.",
        )

    user.first_name = profile_data.first_name
    user.last_name = profile_data.last_name
    user.username = profile_data.username
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
    if not verify_password(
        password_data.current_password.get_secret_value(),
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect.",
        )
    user.password_hash = hash_password(password_data.new_password.get_secret_value())
    db.execute(delete(AuthSession).where(AuthSession.user_id == user.id))
    user.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
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
    if request.headers.get("origin") not in FRONTEND_ORIGINS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Request origin is not allowed.",
        )

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
    db: Session = Depends(get_db),
) -> UserRegistrationResponse:
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
