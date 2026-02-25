from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.domains.alerts import alerts_commands
from app.domains.alerts.dtos import (
    AlertCreateRequestDto,
    AlertResponseDto,
    AlertUpdateRequestDto,
)

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.post("", response_model=AlertResponseDto, status_code=status.HTTP_201_CREATED)
def create_alert(
    request: AlertCreateRequestDto,
    session: Session = Depends(get_session),
) -> AlertResponseDto:
    try:
        return alerts_commands.create_alert(session, request)
    except alerts_commands.AlertAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/{alert_id}", response_model=AlertResponseDto)
def get_alert(
    alert_id: UUID,
    session: Session = Depends(get_session),
) -> AlertResponseDto:
    try:
        return alerts_commands.get_alert(session, alert_id)
    except alerts_commands.AlertNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{alert_id}", response_model=AlertResponseDto)
def update_alert(
    alert_id: UUID,
    request: AlertUpdateRequestDto,
    session: Session = Depends(get_session),
) -> AlertResponseDto:
    try:
        return alerts_commands.update_alert(session, alert_id, request)
    except alerts_commands.AlertNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(
    alert_id: UUID,
    session: Session = Depends(get_session),
) -> None:
    try:
        alerts_commands.delete_alert(session, alert_id)
    except alerts_commands.AlertNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
