from __future__ import annotations

from sqlalchemy import UUID, select
from sqlalchemy.orm import Session

from app.db.models.transaction import Transaction
from app.shared.repos.base_repo import BaseRepo


class TransactionsRepo(BaseRepo[Transaction]):
    def __init__(self) -> None:
        super().__init__(Transaction)

    def list_transaction_by_user_id(
        self, session: Session, user_id: UUID
    ) -> list[Transaction]:
        stmt = select(Transaction).where(Transaction.user_id == user_id)
        return list(session.scalars(stmt))

    def list_transaction_by_card_id(
        self, session: Session, card_id: UUID
    ) -> list[Transaction]:
        stmt = select(Transaction).where(Transaction.card_id == card_id)
        return list(session.scalars(stmt))

    def list_transaction_by_merchant_id(
        self, session: Session, merchant_id: UUID
    ) -> list[Transaction]:
        stmt = select(Transaction).where(Transaction.merchant_id == merchant_id)
        return list(session.scalars(stmt))

    def get_by_idempotency_key(
        self, session: Session, idempotency_key: UUID
    ) -> Transaction:
        stmt = select(Transaction).where(Transaction.idempotency_key == idempotency_key)
        return session.scalar(stmt)
