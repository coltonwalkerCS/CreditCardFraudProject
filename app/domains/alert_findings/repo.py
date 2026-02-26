from __future__ import annotations

from sqlalchemy import UUID, select
from sqlalchemy.orm import Session

from app.db.models.alert_finding import AlertFinding
from app.shared.repos.base_repo import BaseRepo


class AlertFindingsRepo(BaseRepo[AlertFinding]):
    def __init__(self) -> None:
        super().__init__(AlertFinding)

    def get_alert_finding_by_alert_id(
        self, session: Session, alert_id: UUID
    ) -> AlertFinding:
        stmt = select(AlertFinding).where(AlertFinding.alert_id == alert_id)
        return session.scalar(stmt)
