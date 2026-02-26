from __future__ import annotations

from uuid import UUID

from app.domains.enums import FindingCode
from app.shared.dtos.base import BaseDto
from app.shared.dtos.timestamp import TimestampedResponseDto


class AlertFindingCreateRequestDto(BaseDto):
    alert_id: UUID
    code: FindingCode


class AlertFindingUpdateRequestDto(BaseDto):
    code: FindingCode


class AlertFindingResponseDto(TimestampedResponseDto):
    id: UUID
    alert_id: UUID
    code: FindingCode
