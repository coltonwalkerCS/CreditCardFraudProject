from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.domains.alert_actions import alert_actions_commands
from app.domains.alert_actions.dtos import (
    AlertActionCreateRequestDto,
    AlertActionResponseDto,
    AlertActionUpdateRequestDto,
)

router = APIRouter(prefix="/alert_actions", tags=["alert_actions"])


@router.post(
    "", response_model=AlertActionResponseDto, status_code=status.HTTP_201_CREATED
)
def create_alert_action(
    request: AlertActionCreateRequestDto,
    session: Session = Depends(get_session),
) -> AlertActionResponseDto:
    try:
        return alert_actions_commands.create_alert_action(session, request)
    except alert_actions_commands.AlertActionAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/{alert_action_id}", response_model=AlertActionResponseDto)
def get_alert_action(
    alert_action_id: UUID,
    session: Session = Depends(get_session),
) -> AlertActionResponseDto:
    try:
        return alert_actions_commands.get_alert_action(session, alert_action_id)
    except alert_actions_commands.AlertActionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{alert_action_id}", response_model=AlertActionResponseDto)
def update_alert_action(
    alert_action_id: UUID,
    request: AlertActionUpdateRequestDto,
    session: Session = Depends(get_session),
) -> AlertActionResponseDto:
    try:
        return alert_actions_commands.update_alert_action(
            session, alert_action_id, request
        )
    except alert_actions_commands.AlertActionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{alert_action_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert_action(
    alert_action_id: UUID,
    session: Session = Depends(get_session),
) -> None:
    try:
        alert_actions_commands.delete_alert_action(session, alert_action_id)
    except alert_actions_commands.AlertActionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
