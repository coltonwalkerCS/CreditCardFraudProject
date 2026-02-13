from __future__ import annotations

from uuid import UUID

from app.domains.cards.dtos import (
    CardCreateRequestDto,
    CardResponseDto,
    CardUpdateRequestDto,
)
from app.domains.cards.repo import CardsRepo
from sqlalchemy.orm import Session


class CardNotFoundError(Exception):
    pass


class CardAlreadyExistsError(Exception):
    pass


def create_card(session: Session, request: CardCreateRequestDto) -> CardResponseDto:
    repo = CardsRepo()
    if repo.get_by_user_and_last4(session, request.user_id, request.last4):
        raise CardAlreadyExistsError()

    card = repo.insert(
        session,
        user_id=request.user_id,
        last4=request.last4,
        brand=request.brand,
        status=request.status,
        exp_month=request.exp_month,
        exp_year=request.exp_year,
    )

    try:
        session.commit()
    except Exception:
        session.rollback()
        raise

    return CardResponseDto.model_validate(card)


def get_card(session: Session, card_id: UUID) -> CardResponseDto:
    repo = CardsRepo()
    card = repo.get_by_id(session, card_id)
    if not card:
        raise CardNotFoundError()
    return CardResponseDto.model_validate(card)


def list_cards_for_user(session: Session, user_id: UUID) -> list[CardResponseDto]:
    repo = CardsRepo()
    cards = repo.list_card_by_user_id(session, user_id)
    return [CardResponseDto.model_validate(c) for c in cards]


def update_card(
    session: Session, card_id: UUID, request: CardUpdateRequestDto
) -> CardResponseDto:
    repo = CardsRepo()
    card = repo.get_by_id(session, card_id)
    if not card:
        raise CardNotFoundError()

    repo.update(card, status=request.status)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
    return CardResponseDto.model_validate(card)


def delete_card(session: Session, card_id: UUID) -> None:
    repo = CardsRepo()
    card = repo.get_by_id(session, card_id)
    if not card:
        raise CardNotFoundError()
    repo.delete(session, card)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
