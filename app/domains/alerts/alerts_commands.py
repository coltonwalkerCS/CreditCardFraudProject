from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.alerts.dtos import (
    AlertCreateRequestDto,
    AlertResponseDto,
    AlertUpdateRequestDto,
)
from app.domains.alerts.repo import AlertsRepo


class AlertNotFoundError(Exception):
    pass


class AlertAlreadyExistsError(Exception):
    pass


def create_alert(session: Session, request: AlertCreateRequestDto) -> AlertResponseDto:
    repo = AlertsRepo()
    if repo.get_alert_by_transaction_id(session, request.transaction_id):
        raise AlertAlreadyExistsError()

    alert = repo.insert(
        session,
        user_id=request.user_id,
        card_id=request.card_id,
        transaction_id=request.transaction_id,
        severity=request.severity,
        status=request.status,
    )

    try:
        session.commit()
    except Exception:
        session.rollback()
        raise

    return AlertResponseDto.model_validate(alert)


def get_alert(session: Session, alert_id: UUID) -> AlertResponseDto:
    repo = AlertsRepo()
    alert = repo.get_by_id(session, alert_id)
    if not alert:
        raise AlertNotFoundError()
    return AlertResponseDto.model_validate(alert)


def update_alert(
    session: Session, alert_id: UUID, request: AlertUpdateRequestDto
) -> AlertResponseDto:
    repo = AlertsRepo()
    alert = repo.get_by_id(session, alert_id)
    if not alert:
        raise AlertNotFoundError

    repo.update(alert, status=request.status)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
    return AlertResponseDto.model_validate(alert)


def delete_alert(session: Session, alert_id: UUID) -> None:
    repo = AlertsRepo()
    alert = repo.get_by_id(session, alert_id)
    if not alert:
        raise AlertNotFoundError
    repo.delete(session, alert)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
