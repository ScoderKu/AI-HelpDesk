from datetime import datetime, timezone
import os

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.models import User
from app.schemas import (
    UserRegistrationRequest,
    UserRegistrationResponse,
    UserResponse,
)
from app.security import hash_password

app = FastAPI(
    title="AI HelpDesk API",
    description="REST API for the AI HelpDesk project",
    version="0.1.0",
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
    if existing_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email address is already registered.",
        )

    
    if existing_username is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already taken.",
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
