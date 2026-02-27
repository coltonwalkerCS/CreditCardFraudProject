from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.alert_action import AlertAction
from app.shared.repos.base_repo import BaseRepo


class AlertActionsRepo(BaseRepo[AlertAction]):
    def __init__(self) -> None:
        super().__init__(AlertAction)

    def get_alert_action_by_alert_id(
        self, session: Session, alert_id: UUID
    ) -> AlertAction:
        stmt = select(AlertAction).where(AlertAction.alert_id == alert_id)
        return session.scalar(stmt)
