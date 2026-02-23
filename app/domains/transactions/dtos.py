from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from app.domains.enums import TransactionStatus
from app.shared.dtos.base import BaseDto
from app.shared.dtos.timestamp import TimestampedResponseDto


class TransactionCreateRequestDto(BaseDto):
    user_id: UUID
    card_id: UUID
    merchant_id: UUID
    amount: Decimal
    occured_at: datetime
    status: TransactionStatus
    idempotency_key: UUID


class TransactionUpdateRequestDto(BaseDto):
    status: TransactionStatus


class TransactionResponseDto(TimestampedResponseDto):
    id: UUID
    user_id: UUID
    card_id: UUID
    merchant_id: UUID
    amount: Decimal
    occured_at: datetime
    status: TransactionStatus
    idempotency_key: UUID
