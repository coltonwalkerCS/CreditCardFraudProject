from __future__ import annotations

import pytest
from app.core.config import DATABASE_URL_TEST
from app.db.base import Base
from app.db.session import get_session
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="session")
def engine():
    """
    Create tables once for the whole test session (Postgres).
    """
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
def db_session(engine):
    """
    Transaction-per-test. Rolls back after each test for isolation.
    """
    connection = engine.connect()
    transaction = connection.begin()

    SessionLocal = sessionmaker(
        bind=connection, autoflush=False, autocommit=False, future=True
    )
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def client(db_session):
    """
    FastAPI TestClient that uses the per-test db_session via dependency override.
    """

    def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
