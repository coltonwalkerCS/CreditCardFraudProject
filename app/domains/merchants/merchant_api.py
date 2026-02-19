from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.domains.merchants import merchant_commands
from app.domains.merchants.dtos import (
    MerchantCreateRequestDto,
    MerchantResponseDto,
    MerchantUpdateRequestDto,
)

router = APIRouter(prefix="/merchants", tags=["merchants"])


@router.post(
    "", response_model=MerchantResponseDto, status_code=status.HTTP_201_CREATED
)
def create_merchant(
    request: MerchantCreateRequestDto,
    session: Session = Depends(get_session),
) -> MerchantResponseDto:
    try:
        return merchant_commands.create_merchant(session, request)
    except merchant_commands.MerchantAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/{merchant_id}", response_model=MerchantResponseDto)
def get_merchant(
    merchant_id: UUID,
    session: Session = Depends(get_session),
) -> MerchantResponseDto:
    try:
        return merchant_commands.get_merchant(session, merchant_id)
    except merchant_commands.MerchantNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{merchant_id}", response_model=MerchantResponseDto)
def update_merchant(
    merchant_id: UUID,
    request: MerchantUpdateRequestDto,
    session: Session = Depends(get_session),
) -> MerchantResponseDto:
    try:
        return merchant_commands.update_merchant(session, merchant_id, request)
    except merchant_commands.MerchantNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{merchant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_merchant(
    merchant_id: UUID,
    session: Session = Depends(get_session),
) -> None:
    try:
        merchant_commands.delete_merchant(session, merchant_id)
    except merchant_commands.MerchantNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
