from __future__ import annotations

from collections.abc import Generator

from app.db.engine import SessionLocal  # wherever you create sessionmaker()
from sqlalchemy.orm import Session


def get_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
