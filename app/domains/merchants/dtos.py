from __future__ import annotations

from uuid import UUID

from pydantic import Field

from app.domains.enums import MerchantCategory
from app.shared.dtos.base import BaseDto
from app.shared.dtos.timestamp import TimestampedResponseDto


class MerchantCreateRequestDto(BaseDto):
    name: str = Field(min_length=3, max_length=255)
    category: MerchantCategory


class MerchantUpdateRequestDto(BaseDto):
    name: str | None = Field(default=None)
    category: MerchantCategory | None = Field(default=None)


class MerchantResponseDto(TimestampedResponseDto):
    id: UUID
    name: str
    category: MerchantCategory
