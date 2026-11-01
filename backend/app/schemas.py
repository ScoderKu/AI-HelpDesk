import re
from datetime import datetime, timezone
from enum import Enum
from typing import Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    SecretStr,
    field_serializer,
    model_validator,
)


EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class UserRegistrationRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=False)

    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=3, max_length=255)
    password: SecretStr = Field(min_length=8, max_length=128)

    @model_validator(mode="after")
    def normalize_and_validate(self) -> Self:
        self.first_name = self.first_name.strip()
        self.last_name = self.last_name.strip()
        self.username = self.username.strip()
        self.email = self.email.strip().lower()

        if not self.first_name:
            raise ValueError("First name is required.")
        if not self.last_name:
            raise ValueError("Last name is required.")
        if len(self.username) < 3:
            raise ValueError("Username must contain at least 3 characters.")
        if not EMAIL_PATTERN.fullmatch(self.email):
            raise ValueError("Enter a valid email address.")

        return self


class UserLoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: SecretStr = Field(min_length=1, max_length=128)

    @model_validator(mode="after")
    def normalize_and_validate(self) -> Self:
        self.email = self.email.strip().lower()
        if not EMAIL_PATTERN.fullmatch(self.email):
            raise ValueError("Enter a valid email address.")
        return self


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    username: str
    email: str


class UserRegistrationResponse(BaseModel):
    user: UserResponse


class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TicketStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class TicketCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    priority: TicketPriority = TicketPriority.MEDIUM

    @model_validator(mode="after")
    def validate_text(self) -> Self:
        if len(self.description.encode("utf-8")) > 65_535:
            raise ValueError("Description exceeds the MySQL TEXT field limit.")
        return self


class TicketUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1)
    priority: TicketPriority | None = None

    @model_validator(mode="after")
    def validate_patch(self) -> Self:
        if not self.model_fields_set:
            raise ValueError("At least one ticket field must be provided.")
        if any(getattr(self, field) is None for field in self.model_fields_set):
            raise ValueError("Ticket fields cannot be null.")
        if self.description is not None and len(self.description.encode("utf-8")) > 65_535:
            raise ValueError("Description exceeds the MySQL TEXT field limit.")
        return self


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime

    @field_serializer("created_at", when_used="json")
    def serialize_created_at(self, value: datetime) -> str:
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


class TicketSummaryResponse(BaseModel):
    total: int
    open: int
    closed: int


class UserProfileUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=3, max_length=100)

    @model_validator(mode="after")
    def validate_profile(self) -> Self:
        if not self.first_name or not self.last_name or len(self.username) < 3:
            raise ValueError("Profile fields are invalid.")
        return self


class UserPasswordChangeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    current_password: SecretStr = Field(min_length=1, max_length=128)
    new_password: SecretStr = Field(min_length=8, max_length=128)
    confirm_new_password: SecretStr = Field(min_length=8, max_length=128)

    @model_validator(mode="after")
    def validate_passwords(self) -> Self:
        if self.new_password.get_secret_value() != self.confirm_new_password.get_secret_value():
            raise ValueError("New password confirmation does not match.")
        if self.current_password.get_secret_value() == self.new_password.get_secret_value():
            raise ValueError("New password must differ from current password.")
        return self
