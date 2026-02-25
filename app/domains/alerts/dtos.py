from __future__ import annotations

from uuid import UUID

from app.domains.enums import AlertSeverity, AlertStatus
from app.shared.dtos.base import BaseDto
from app.shared.dtos.timestamp import TimestampedResponseDto


class AlertCreateRequestDto(BaseDto):
    user_id: UUID
    card_id: UUID
    transaction_id: UUID
    severity: AlertSeverity
    status: AlertStatus


class AlertUpdateRequestDto(BaseDto):
    status: AlertStatus


class AlertResponseDto(TimestampedResponseDto):
    id: UUID
    user_id: UUID
    card_id: UUID
    transaction_id: UUID
    severity: AlertSeverity
    status: AlertStatus
