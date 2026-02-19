import uuid

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.mixins import TimestampMixin
from app.domains.enums import FindingCode


class AlertFinding(Base, TimestampMixin):
    __tablename__ = "alert_findings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    alert_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("alerts.id"), nullable=False)
    code: Mapped[FindingCode] = mapped_column(
        SAEnum(FindingCode, name="finding_code"), nullable=False
    )
