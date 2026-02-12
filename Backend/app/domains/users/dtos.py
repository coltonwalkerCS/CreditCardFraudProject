from __future__ import annotations

from datetime import datetime
from uuid import UUID

from app.shared.dtos.base import BaseDto
from app.shared.dtos.timestamp import TimestampedResponseDto
from pydantic import EmailStr, Field


class UserCreateRequestDto(BaseDto):
    username: str = Field(min_length=3, max_length=50)


class UserUpdateRequestDto(BaseDto):
    username: str | None = Field(default=None, min_length=3, max_length=50)


class UserResponseDto(TimestampedResponseDto):
    id: UUID
    username: str
