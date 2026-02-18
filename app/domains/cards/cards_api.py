from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.domains.cards import cards_commands
from app.domains.cards.dtos import (
    CardCreateRequestDto,
    CardResponseDto,
    CardUpdateRequestDto,
)

router = APIRouter(prefix="/cards", tags=["cards"])


@router.post("", response_model=CardResponseDto, status_code=status.HTTP_201_CREATED)
def create_card(
    request: CardCreateRequestDto,
    session: Session = Depends(get_session),
) -> CardResponseDto:
    try:
        return cards_commands.create_card(session, request)
    except cards_commands.CardAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/{card_id}", response_model=CardResponseDto)
def get_card(
    card_id: UUID,
    session: Session = Depends(get_session),
) -> CardResponseDto:
    try:
        return cards_commands.get_card(session, card_id)
    except cards_commands.CardNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{card_id}", response_model=CardResponseDto)
def update_card(
    card_id: UUID,
    request: CardUpdateRequestDto,
    session: Session = Depends(get_session),
) -> CardResponseDto:
    try:
        return cards_commands.update_card(session, card_id, request)
    except cards_commands.CardNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(
    card_id: UUID,
    session: Session = Depends(get_session),
) -> None:
    try:
        cards_commands.delete_card(session, card_id)
    except cards_commands.CardNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
