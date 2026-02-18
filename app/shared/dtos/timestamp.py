from datetime import datetime

from app.shared.dtos.base import BaseDto


class TimestampedResponseDto(BaseDto):
    created_at: datetime
    updated_at: datetime
