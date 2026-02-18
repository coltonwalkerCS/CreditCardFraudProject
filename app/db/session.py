from __future__ import annotations

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.engine import SessionLocal  # wherever you create sessionmaker()


def get_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
