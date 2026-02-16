from __future__ import annotations

import uuid

import pytest
from app.core.config import DATABASE_URL_TEST
from app.db.base import Base
from app.db.session import get_session
from app.domains.cards.cards_commands import create_card
from app.domains.cards.dtos import CardCreateRequestDto
from app.domains.enums import CardBrand, CardStatus
from app.domains.users.dtos import UserCreateRequestDto
from app.domains.users.users_commands import create_user
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker


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
            "DATABASE_URL_TEST=postgresql+psycopg://postgres:password@localhost:5432/fraud_test"
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
