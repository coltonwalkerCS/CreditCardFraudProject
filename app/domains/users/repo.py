from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.shared.repos.base_repo import BaseRepo

users_repo = BaseRepo(User)


def get_by_username(session: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return session.execute(stmt).scalar_one_or_none()
