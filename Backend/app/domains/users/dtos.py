from __future__ import annotations

from uuid import UUID

from app.shared.dtos.base import BaseDto
from app.shared.dtos.timestamp import TimestampedResponseDto
from pydantic import Field


class UserCreateRequestDto(BaseDto):
    username: str = Field(min_length=3, max_length=50)


class UserUpdateRequestDto(BaseDto):
    username: str | None = Field(default=None, min_length=3, max_length=50)


class UserResponseDto(TimestampedResponseDto):
    id: UUID
    username: str
