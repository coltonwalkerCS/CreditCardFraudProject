from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL_TEST
from app.db.base import Base
from app.db.session import get_session
from app.domains.alerts.alerts_commands import create_alert
from app.domains.alerts.dtos import AlertCreateRequestDto
from app.domains.cards.cards_commands import create_card
from app.domains.cards.dtos import CardCreateRequestDto
from app.domains.enums import (
    AlertSeverity,
    AlertStatus,
    CardBrand,
    CardStatus,
    MerchantCategory,
    TransactionStatus,
)
from app.domains.merchants.dtos import MerchantCreateRequestDto
from app.domains.merchants.merchant_commands import create_merchant
from app.domains.transactions.dtos import TransactionCreateRequestDto
from app.domains.transactions.transactions_commands import create_transacton
from app.domains.users.dtos import UserCreateRequestDto
from app.domains.users.users_commands import create_user
from app.main import app


@pytest.fixture()
def client(session):
    def _override_get_session():
        yield session

    app.dependency_overrides[get_session] = _override_get_session
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def engine():
    if not DATABASE_URL_TEST:
        raise RuntimeError(
            "DATABASE_URL_TEST is not set. Add it to Backend/secrets/.env, e.g.\n"
            "DATABASE_URL_TEST=postgresql+psycopg://postgres:password@localhost:5432/"
            "fraud_test"
        )

    engine = create_engine(DATABASE_URL_TEST, future=True, pool_pre_ping=True)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def session(engine):
    """
    Per-test transaction that survives code calling session.commit()
    by using a nested transaction (SAVEPOINT) pattern.
    """
    connection = engine.connect()
    trans = connection.begin()

    SessionLocal = sessionmaker(
        bind=connection, autoflush=False, autocommit=False, future=True
    )
    s = SessionLocal()

    # Start a SAVEPOINT
    s.begin_nested()

    # Restart SAVEPOINT after each commit/rollback inside the code under test
    @event.listens_for(s, "after_transaction_end")
    def _restart_savepoint(sess, transaction):
        if transaction.nested and not transaction._parent.nested:
            sess.begin_nested()

    try:
        yield s
    finally:
        s.close()
        trans.rollback()
        connection.close()


@pytest.fixture
def make_user(session):
    def _make(username: str | None = None):
        username_request = username or f"user_{uuid.uuid4().hex[:8]}"
        return create_user(session, UserCreateRequestDto(username=username_request))

    return _make


@pytest.fixture
def make_card(session, make_user):
    def _make(
        *,
        user_id: uuid.UUID | None = None,
        last4: int = 1234,
        brand: CardBrand = CardBrand.VISA,
        status: CardStatus = CardStatus.ACTIVE,
        exp_month: int = 12,
        exp_year: int = 2027,
    ):
        if user_id is None:
            user = make_user()
            user_id = user.id

        dto = CardCreateRequestDto(
            user_id=user_id,
            last4=last4,
            brand=brand,
            status=status,
            exp_month=exp_month,
            exp_year=exp_year,
        )
        return create_card(session, dto)

    return _make


@pytest.fixture
def make_merchant(session):
    """
    Fixture that creates a merchant through the command layer
    (so tests cover create + commit behavior).
    """

    def _make(
        *,
        name: str | None = None,
        category: MerchantCategory = MerchantCategory.GROCERY,
    ):
        if name is None:
            name = f"merchant-{uuid.uuid4().hex[:8]}"

        return create_merchant(
            session,
            MerchantCreateRequestDto(name=name, category=category),
        )

    return _make


@pytest.fixture
def make_transaction(session, make_user, make_card, make_merchant):
    """
    Fixture that creates a transaction through the command layer
    (so tests cover create + commit behavior).
    """

    def _make(
        *,
        user_id=None,
        card_id=None,
        merchant_id=None,
        amount: Decimal = Decimal("10.00"),
        occurred_at: datetime | None = None,
        status: TransactionStatus = TransactionStatus.APPROVED,
        idempotency_key=None,
    ):
        # Create defaults if not provided
        if user_id is None:
            user = make_user()
            user_id = user.id

        if card_id is None:
            card = make_card(user_id=user_id)
            card_id = card.id

        if merchant_id is None:
            merchant = make_merchant()
            merchant_id = merchant.id

        if occurred_at is None:
            occurred_at = datetime.now(timezone.utc)

        if idempotency_key is None:
            idempotency_key = uuid.uuid4()

        return create_transacton(
            session,
            TransactionCreateRequestDto(
                user_id=user_id,
                card_id=card_id,
                merchant_id=merchant_id,
                amount=amount,
                occurred_at=occurred_at,
                status=status,
                idempotency_key=idempotency_key,
            ),
        )

    return _make


@pytest.fixture
def make_alert(session, make_user, make_card, make_merchant, make_transaction):
    """
    Fixture that creates an alert through the command layer
    (so tests cover create + commit behavior).
    """

    def _make(
        *,
        user_id=None,
        card_id=None,
        merchant_id=None,
        transaction_id=None,
        severity: AlertSeverity = AlertSeverity.MEDIUM,
        status: AlertStatus = AlertStatus.OPEN,
    ):

        if user_id is None:
            user = make_user()
            user_id = user.id

        if card_id is None:
            card = make_card(user_id=user_id)
            card_id = card.id

        if merchant_id is None:
            merchant = make_merchant()
            merchant_id = merchant.id

        if transaction_id is None:
            transaction = make_transaction(
                user_id=user_id,
                card_id=card_id,
                merchant_id=merchant_id,
            )
            transaction_id = transaction.id

        return create_alert(
            session,
            AlertCreateRequestDto(
                user_id=user_id,
                card_id=card_id,
                transaction_id=transaction_id,
                severity=severity,
                status=status,
            ),
        )

    return _make
