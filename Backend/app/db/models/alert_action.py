import uuid

from app.db.base import Base
from app.db.enums import ActorType, AlertActionType
from app.db.models.mixins import TimestampMixin
from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class AlertAction(Base, TimestampMixin):
    __tablename__ = "alert_actions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    alert_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("alerts.id"), nullable=False)
    action: Mapped[AlertActionType] = mapped_column(
        SAEnum(AlertActionType, name="alert_action_type"), nullable=False
    )
    actor_type: Mapped[ActorType] = mapped_column(
        SAEnum(ActorType, name="actor_type"), nullable=False
    )
