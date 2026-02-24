from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.domains.enums import TransactionStatus
from app.domains.transactions.dtos import (
    TransactionCreateRequestDto,
    TransactionUpdateRequestDto,
)
from app.domains.transactions.transactions_commands import (
    TransactionAlreadyExistsError,
    TransactionNotFoundError,
    create_transacton,
    delete_transaction,
    get_transaction,
    update_transaction,
)


def test_create_transaction_success(session, make_user, make_card, make_merchant):
    user = make_user()
    card = make_card(user_id=user.id)
    merchant = make_merchant()

    created = create_transacton(
        session,
        TransactionCreateRequestDto(
            user_id=user.id,
            card_id=card.id,
            merchant_id=merchant.id,
            amount=Decimal("12.34"),
            occurred_at=datetime.now(timezone.utc),
            status=TransactionStatus.APPROVED,
            idempotency_key=uuid.uuid4(),
        ),
    )

    assert created.id is not None
    assert created.user_id == user.id
    assert created.card_id == card.id
    assert created.merchant_id == merchant.id
    assert created.amount == Decimal("12.34")
    assert created.occurred_at is not None
    assert created.status == TransactionStatus.APPROVED
    assert created.created_at is not None
    assert created.updated_at is not None


def test_create_transaction_duplicate_idempotency_key_raises(
    session, make_user, make_card, make_merchant
):
    user = make_user()
    card = make_card(user_id=user.id)
    merchant = make_merchant()
    idem = uuid.uuid4()

    create_transacton(
        session,
        TransactionCreateRequestDto(
            user_id=user.id,
            card_id=card.id,
            merchant_id=merchant.id,
            amount=Decimal("50.00"),
            occurred_at=datetime.now(timezone.utc),
            status=TransactionStatus.APPROVED,
            idempotency_key=idem,
        ),
    )

    with pytest.raises(TransactionAlreadyExistsError):
        create_transacton(
            session,
            TransactionCreateRequestDto(
                user_id=user.id,
                card_id=card.id,
                merchant_id=merchant.id,
                amount=Decimal("50.00"),
                occurred_at=datetime.now(timezone.utc),
                status=TransactionStatus.APPROVED,
                idempotency_key=idem,
            ),
        )


def test_get_transaction_not_found(session):
    with pytest.raises(TransactionNotFoundError):
        get_transaction(session, uuid.uuid4())


def test_get_transaction_success(session, make_transaction):
    created = make_transaction(amount=Decimal("99.99"))

    fetched = get_transaction(session, created.id)

    assert fetched.id == created.id
    assert fetched.user_id == created.user_id
    assert fetched.card_id == created.card_id
    assert fetched.merchant_id == created.merchant_id
    assert fetched.amount == Decimal("99.99")


def test_update_transaction_not_found(session):
    with pytest.raises(TransactionNotFoundError):
        update_transaction(
            session,
            uuid.uuid4(),
            TransactionUpdateRequestDto(status=TransactionStatus.APPROVED),
        )


def test_update_transaction_success(session, make_transaction):
    created = make_transaction(status=TransactionStatus.APPROVED)

    updated = update_transaction(
        session,
        created.id,
        TransactionUpdateRequestDto(status=TransactionStatus.DECLINED),
    )

    assert updated.id == created.id
    assert updated.status == TransactionStatus.DECLINED

    fetched = get_transaction(session, created.id)
    assert fetched.status == TransactionStatus.DECLINED


def test_delete_transaction_not_found(session):
    with pytest.raises(TransactionNotFoundError):
        delete_transaction(session, uuid.uuid4())


def test_delete_transaction_success(session, make_transaction):
    created = make_transaction()

    delete_transaction(session, created.id)

    with pytest.raises(TransactionNotFoundError):
        get_transaction(session, created.id)
