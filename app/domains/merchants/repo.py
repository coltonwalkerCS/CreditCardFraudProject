from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.merchant import Merchant
from app.domains.enums import MerchantCategory
from app.shared.repos.base_repo import BaseRepo


class MerchantRepo(BaseRepo[Merchant]):
    def __init__(self) -> None:
        super().__init__(Merchant)

    def get_by_name(
        self,
        session: Session,
        name: str,
    ) -> Merchant | None:
        stmt = select(Merchant).where(
            Merchant.name == name,
        )
        return session.scalar(stmt)

    def get_by_merchant_category(
        self, session: Session, merchant_category: MerchantCategory
    ) -> list[Merchant]:
        stmt = select(Merchant).where(
            Merchant.category == merchant_category,
        )
        return session.scalars(stmt).all()
