from __future__ import annotations

from uuid import UUID

from app.domains.enums import CardBrand, CardStatus
from app.shared.dtos.base import BaseDto
from app.shared.dtos.timestamp import TimestampedResponseDto
from pydantic import Field, field_validator


class CardCreateRequestDto(BaseDto):
    user_id: UUID
    last4: int = Field(ge=0, le=9999)
    brand: CardBrand
    status: CardStatus
    exp_month: int = Field(ge=1, le=12)
    exp_year: int = Field(ge=2025, le=2100)

    @field_validator("last4")
    @classmethod
    def validate_last4(cls, v: int) -> int:
        if v < 0 or v > 9999:
            raise ValueError("last4 must be between 0000 and 9999")

        # Ensure exactly 4 digits
        if len(f"{v:04d}") != 4:
            raise ValueError("last4 must be exactly 4 digits")

        return v


class CardUpdateRequestDto(BaseDto):
    status: CardStatus


class CardResponseDto(TimestampedResponseDto):
    id: UUID
    user_id: UUID
    last4: int
    brand: CardBrand
    status: CardStatus
    exp_month: int
    exp_year: int
