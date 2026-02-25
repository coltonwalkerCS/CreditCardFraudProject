from __future__ import annotations

from sqlalchemy import UUID, select
from sqlalchemy.orm import Session

from app.db.models.alert import Alert
from app.shared.repos.base_repo import BaseRepo


class AlertsRepo(BaseRepo[Alert]):
    def __init__(self) -> None:
        super().__init__(Alert)

    def get_alert_by_transaction_id(
        self, session: Session, transaction_id: UUID
    ) -> Alert:
        stmt = select(Alert).where(Alert.transaction_id == transaction_id)
        return session.scalar(stmt)
