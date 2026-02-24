from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.domains.transactions import transactions_commands
from app.domains.transactions.dtos import (
    TransactionCreateRequestDto,
    TransactionResponseDto,
    TransactionUpdateRequestDto,
)

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post(
    "", response_model=TransactionResponseDto, status_code=status.HTTP_201_CREATED
)
def create_transaction(
    request: TransactionCreateRequestDto,
    session: Session = Depends(get_session),
) -> TransactionResponseDto:
    try:
        return transactions_commands.create_transacton(session, request)
    except transactions_commands.TransactionAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/{transaction_id}", response_model=TransactionResponseDto)
def get_transaction(
    transaction_id: UUID,
    session: Session = Depends(get_session),
) -> TransactionResponseDto:
    try:
        return transactions_commands.get_transaction(session, transaction_id)
    except transactions_commands.TransactionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{transaction_id}", response_model=TransactionResponseDto)
def update_transaction(
    transaction_id: UUID,
    request: TransactionUpdateRequestDto,
    session: Session = Depends(get_session),
) -> TransactionResponseDto:
    try:
        return transactions_commands.update_transaction(
            session, transaction_id, request
        )
    except transactions_commands.TransactionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: UUID,
    session: Session = Depends(get_session),
) -> None:
    try:
        transactions_commands.delete_transaction(session, transaction_id)
    except transactions_commands.TransactionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
