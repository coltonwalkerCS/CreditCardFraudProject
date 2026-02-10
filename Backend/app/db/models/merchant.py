import uuid

from app.db.base import Base
from app.db.enums import MerchantCategory
from app.db.models.mixins import TimestampMixin
from sqlalchemy import Enum as SAEnum
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class Merchant(Base, TimestampMixin):
    __tablename__ = "merchants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[MerchantCategory] = mapped_column(
        SAEnum(MerchantCategory, name="merchant_category"), nullable=False
    )
