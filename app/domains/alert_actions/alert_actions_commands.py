from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.alert_actions.dtos import (
    AlertActionCreateRequestDto,
    AlertActionResponseDto,
    AlertActionUpdateRequestDto,
)
from app.domains.alert_actions.repo import AlertActionsRepo


class AlertActionNotFoundError(Exception):
    pass


class AlertActionAlreadyExistsError(Exception):
    pass


def create_alert_action(
    session: Session, request: AlertActionCreateRequestDto
) -> AlertActionResponseDto:
    repo = AlertActionsRepo()
    if repo.get_alert_action_by_alert_id(session, request.alert_id):
        raise AlertActionAlreadyExistsError()

    alert_action = repo.insert(
        session,
        alert_id=request.alert_id,
        action=request.action,
        actor_type=request.actor_type,
    )

    try:
        session.commit()
    except Exception:
        session.rollback()
        raise

    return AlertActionResponseDto.model_validate(alert_action)


def get_alert_action(session: Session, alert_action_id: UUID) -> AlertActionResponseDto:
    repo = AlertActionsRepo()
    alert_action = repo.get_by_id(session, alert_action_id)
    if not alert_action:
        raise AlertActionNotFoundError()
    return AlertActionResponseDto.model_validate(alert_action)


def update_alert_action(
    session: Session, alert_action_id: UUID, request: AlertActionUpdateRequestDto
) -> AlertActionResponseDto:
    repo = AlertActionsRepo()
    alert_action = repo.get_by_id(session, alert_action_id)
    if not alert_action:
        raise AlertActionNotFoundError()

    update_data = request.model_dump(exclude_unset=True, exclude_none=True)
    repo.update(alert_action, **update_data)

    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
    return AlertActionResponseDto.model_validate(alert_action)


def delete_alert_action(session: Session, alert_action_id: UUID) -> None:
    repo = AlertActionsRepo()
    alert_action = repo.get_by_id(session, alert_action_id)
    if not alert_action:
        raise AlertActionNotFoundError()
    repo.delete(session, alert_action)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
