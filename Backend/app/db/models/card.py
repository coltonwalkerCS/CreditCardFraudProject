import uuid

from app.db.base import Base
from app.db.enums import CardBrand, CardStatus
from app.db.models.mixins import TimestampMixin
from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class Card(Base, TimestampMixin):
    __tablename__ = "cards"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    last4: Mapped[int] = mapped_column(Integer, nullable=False)
    brand: Mapped[CardBrand] = mapped_column(
        SAEnum(CardBrand, name="card_brand"), nullable=False
    )
    status: Mapped[CardStatus] = mapped_column(
        SAEnum(CardStatus, name="card_status"), nullable=False
    )
    exp_month: Mapped[int] = mapped_column(Integer, nullable=False)
    exp_year: Mapped[int] = mapped_column(Integer, nullable=False)
