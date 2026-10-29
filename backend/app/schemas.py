import re
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator


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


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    username: str
    email: str


class UserRegistrationResponse(BaseModel):
    user: UserResponse
