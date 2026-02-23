from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.transactions.dtos import (
    TransactionCreateRequestDto,
    TransactionResponseDto,
    TransactionUpdateRequestDto,
)
from app.domains.transactions.repo import TransactionsRepo


class TransactionNotFoundError(Exception):
    pass


class TransactionAlreadyExistsError(Exception):
    pass


def create_transacton(
    session: Session, request: TransactionCreateRequestDto
) -> TransactionResponseDto:
    repo = TransactionsRepo()
    if repo.get_by_idempotency_key(session, request.idempotency_key):
        raise TransactionAlreadyExistsError()

    transaction = repo.insert(
        session,
        user_id=request.user_id,
        card_id=request.card_id,
        merchant_id=request.merchant_id,
        amount=request.amount,
        occured_at=request.occured_at,
        status=request.status,
    )

    try:
        session.commit()
    except Exception:
        session.rollback()
        raise

    return TransactionResponseDto.model_validate(transaction)


def get_transaction(session: Session, transaction_id: UUID) -> TransactionResponseDto:
    repo = TransactionsRepo()
    transaction = repo.get_by_id(session, transaction_id)
    if not transaction:
        raise TransactionNotFoundError()
    return TransactionResponseDto.model_validate(transaction)


def update_transaction(
    session: Session, transaction_id: UUID, request: TransactionUpdateRequestDto
) -> TransactionResponseDto:
    repo = TransactionsRepo()
    transaction = repo.get_by_id(session, transaction_id)
    if not transaction:
        raise TransactionNotFoundError

    repo.update(transaction, status=request.status)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
    return TransactionResponseDto.model_validate(transaction)


def delete_transaction(session: Session, transaction_id: UUID) -> None:
    repo = TransactionsRepo()
    transaction = repo.get_by_id(session, transaction_id)
    if not transaction:
        raise TransactionNotFoundError
    repo.delete(session, transaction)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
