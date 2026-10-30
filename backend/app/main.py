from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import hashlib
import hmac
import ipaddress
import os
import secrets
import time

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from redis import Redis
from redis.exceptions import RedisError
from sqlalchemy import delete, select, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.models import AuthSession, User
from app.schemas import (
    UserLoginRequest,
    UserRegistrationRequest,
    UserRegistrationResponse,
    UserResponse,
)
from app.security import hash_password, verify_password

SESSION_COOKIE_NAME = "ai_helpdesk_session"
SESSION_COOKIE_MAX_AGE = 60 * 60 * 8
SESSION_COOKIE_SECURE = os.getenv("AUTH_COOKIE_SECURE", "true").lower() == "true"
DUMMY_PASSWORD_HASH = hash_password("invalid-login-dummy-secret")
LOGIN_IP_ATTEMPT_LIMIT = 20
LOGIN_IP_WINDOW_SECONDS = 60
LOGIN_ACCOUNT_ATTEMPT_LIMIT = 5
LOGIN_ACCOUNT_WINDOW_SECONDS = 15 * 60
LOGIN_RATE_LIMIT_SCRIPT = """
local ip_count = redis.call('INCR', KEYS[1])
if ip_count == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
end
local account_count = redis.call('INCR', KEYS[2])
if account_count == 1 then
    redis.call('EXPIRE', KEYS[2], ARGV[2])
end
return {
    ip_count,
    account_count,
    redis.call('TTL', KEYS[1]),
    redis.call('TTL', KEYS[2])
}
"""
TRUSTED_PROXY_IPS = frozenset(
    ipaddress.ip_address(value.strip())
    for value in os.getenv("TRUSTED_PROXY_IPS", "").split(",")
    if value.strip()
)
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
    if peer_ip not in TRUSTED_PROXY_IPS:
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
        if forwarded_ips:
            return str(forwarded_ips[-1])
    return str(peer_ip)


def enforce_login_rate_limit(request: Request, email: str) -> None:
    client_ip_hash = hashlib.sha256(get_client_ip(request).encode()).hexdigest()
    account_hash = hmac.new(
        get_session_secret(),
        email.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    try:
        counts = redis_client.eval(
            LOGIN_RATE_LIMIT_SCRIPT,
            2,
            f"login-limit:ip:{client_ip_hash}",
            f"login-limit:account:{account_hash}",
            LOGIN_IP_WINDOW_SECONDS,
            LOGIN_ACCOUNT_WINDOW_SECONDS,
        )
    except RedisError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Sign-in is temporarily unavailable.",
        ) from error

    ip_count, account_count, ip_ttl, account_ttl = (
        int(value) for value in counts
    )
    retry_after = 0
    if ip_count > LOGIN_IP_ATTEMPT_LIMIT:
        retry_after = max(retry_after, ip_ttl)
    if account_count > LOGIN_ACCOUNT_ATTEMPT_LIMIT:
        retry_after = max(retry_after, account_ttl)
    if retry_after:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many sign-in attempts. Please try again later.",
            headers={"Retry-After": str(retry_after)},
        )


def get_session_secret() -> bytes:
    secret = os.getenv("JWT_SECRET_KEY", "").encode("utf-8")
    if len(secret) < 32:
        raise RuntimeError("JWT_SECRET_KEY must contain at least 32 characters.")
    return secret


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
    AuthSession.__table__.create(bind=engine, checkfirst=True)
    redis_client.ping()
    try:
        yield
    finally:
        redis_client.close()


app = FastAPI(
    title="AI HelpDesk API",
    description="REST API for the AI HelpDesk project",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv(
            "FRONTEND_ORIGINS",
            "http://localhost:8088,http://127.0.0.1:8088",
        ).split(",")
        if origin.strip()
    ],
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    expires_at = int(time.time()) + SESSION_COOKIE_MAX_AGE
    session_id = secrets.token_hex(16)
    db.execute(delete(AuthSession).where(AuthSession.expires_at <= now))
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
