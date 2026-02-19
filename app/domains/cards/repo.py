from __future__ import annotations

from sqlalchemy import UUID, select
from sqlalchemy.orm import Session

from app.db.models.card import Card
from app.domains.enums import CardStatus
from app.shared.repos.base_repo import BaseRepo


class CardsRepo(BaseRepo[Card]):
    def __init__(self) -> None:
        super().__init__(Card)

    def list_card_by_user_id(self, session: Session, user_id: UUID) -> list[Card]:
        stmt = select(Card).where(Card.user_id == user_id)
        return list(session.scalars(stmt))

    def list_active_by_user_id(self, session: Session, user_id: UUID) -> list[Card]:
        stmt = select(Card).where(
            Card.user_id == user_id,
            Card.status == CardStatus.ACTIVE,
        )
        return list(session.scalars(stmt))

    def get_by_user_and_last4(
        self, session: Session, user_id: UUID, last4: int
    ) -> Card | None:
        stmt = select(Card).where(
            Card.user_id == user_id,
            Card.last4 == last4,
        )
        return session.scalar(stmt)
