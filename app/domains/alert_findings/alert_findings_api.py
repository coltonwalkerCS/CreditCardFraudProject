from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.domains.alert_findings import alert_findings_commands
from app.domains.alert_findings.dtos import (
    AlertFindingCreateRequestDto,
    AlertFindingResponseDto,
    AlertFindingUpdateRequestDto,
)

router = APIRouter(prefix="/alert_findings", tags=["alert_findings"])


@router.post(
    "", response_model=AlertFindingResponseDto, status_code=status.HTTP_201_CREATED
)
def create_alert_finding(
    request: AlertFindingCreateRequestDto,
    session: Session = Depends(get_session),
) -> AlertFindingResponseDto:
    try:
        return alert_findings_commands.create_alert_finding(session, request)
    except alert_findings_commands.AlertFindingAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/{alert_finding_id}", response_model=AlertFindingResponseDto)
def get_alert_finding(
    alert_finding_id: UUID,
    session: Session = Depends(get_session),
) -> AlertFindingResponseDto:
    try:
        return alert_findings_commands.get_alert_finding(session, alert_finding_id)
    except alert_findings_commands.AlertFindingNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{alert_finding_id}", response_model=AlertFindingResponseDto)
def update_alert_finding(
    alert_finding_id: UUID,
    request: AlertFindingUpdateRequestDto,
    session: Session = Depends(get_session),
) -> AlertFindingResponseDto:
    try:
        return alert_findings_commands.update_alert_finding(
            session, alert_finding_id, request
        )
    except alert_findings_commands.AlertFindingNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{alert_finding_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert_finding(
    alert_finding_id: UUID,
    session: Session = Depends(get_session),
) -> None:
    try:
        alert_findings_commands.delete_alert_finding(session, alert_finding_id)
    except alert_findings_commands.AlertFindingNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
