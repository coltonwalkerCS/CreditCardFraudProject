from __future__ import annotations

from uuid import UUID

from pydantic import Field

from app.domains.enums import ActorType, AlertActionType
from app.shared.dtos.base import BaseDto
from app.shared.dtos.timestamp import TimestampedResponseDto


class AlertActionCreateRequestDto(BaseDto):
    alert_id: UUID
    action: AlertActionType
    actor_type: ActorType


class AlertActionUpdateRequestDto(BaseDto):
    action: AlertActionType | None = Field(default=None)
    actor_type: ActorType | None = Field(default=None)


class AlertActionResponseDto(TimestampedResponseDto):
    id: UUID
    alert_id: UUID
    action: AlertActionType
    actor_type: ActorType
    action: AlertActionType
    actor_type: ActorType
