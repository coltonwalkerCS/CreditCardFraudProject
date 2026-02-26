from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.alert_findings.dtos import (
    AlertFindingCreateRequestDto,
    AlertFindingResponseDto,
    AlertFindingUpdateRequestDto,
)
from app.domains.alert_findings.repo import AlertFindingsRepo


class AlertFindingNotFoundError(Exception):
    pass


class AlertFindingAlreadyExistsError(Exception):
    pass


def create_alert_finding(
    session: Session, request: AlertFindingCreateRequestDto
) -> AlertFindingResponseDto:
    repo = AlertFindingsRepo()
    if repo.get_alert_finding_by_alert_id(session, request.alert_id):
        raise AlertFindingAlreadyExistsError()

    alert_finding = repo.insert(session, alert_id=request.alert_id, code=request.code)

    try:
        session.commit()
    except Exception:
        session.rollback()
        raise

    return AlertFindingResponseDto.model_validate(alert_finding)


def get_alert_finding(
    session: Session, alert_finding_id: UUID
) -> AlertFindingResponseDto:
    repo = AlertFindingsRepo()
    alert_finding = repo.get_by_id(session, alert_finding_id)
    if not alert_finding:
        raise AlertFindingNotFoundError()
    return AlertFindingResponseDto.model_validate(alert_finding)


def update_alert_finding(
    session: Session, alert_finding_id: UUID, request: AlertFindingUpdateRequestDto
) -> AlertFindingResponseDto:
    repo = AlertFindingsRepo()
    alert_finding = repo.get_by_id(session, alert_finding_id)
    if not alert_finding:
        raise AlertFindingNotFoundError()

    repo.update(alert_finding, code=request.code)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
    return AlertFindingResponseDto.model_validate(alert_finding)


def delete_alert_finding(session: Session, alert_finding_id: UUID) -> None:
    repo = AlertFindingsRepo()
    alert_finding = repo.get_by_id(session, alert_finding_id)
    if not alert_finding:
        raise AlertFindingNotFoundError()
    repo.delete(session, alert_finding)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
