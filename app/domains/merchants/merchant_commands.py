from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.enums import MerchantCategory
from app.domains.merchants.dtos import (
    MerchantCreateRequestDto,
    MerchantResponseDto,
    MerchantUpdateRequestDto,
)
from app.domains.merchants.repo import MerchantRepo


class MerchantNotFoundError(Exception):
    pass


class MerchantAlreadyExistsError(Exception):
    pass


def create_merchant(
    session: Session, request: MerchantCreateRequestDto
) -> MerchantResponseDto:
    repo = MerchantRepo()
    if repo.get_by_name(session, request.name):
        raise MerchantAlreadyExistsError

    merchant = repo.insert(session, name=request.name, category=request.category)

    try:
        session.commit()
    except Exception:
        session.rollback()
        raise

    return MerchantResponseDto.model_validate(merchant)


def get_merchant(session: Session, merchant_id: UUID) -> MerchantResponseDto:
    repo = MerchantRepo()
    merchant = repo.get_by_id(session, merchant_id)
    if not merchant:
        raise MerchantNotFoundError
    return MerchantResponseDto.model_validate(merchant)


def list_merchants_by_category(
    session: Session, category: MerchantCategory
) -> list[MerchantResponseDto]:
    repo = MerchantRepo()
    merchants = repo.get_by_merchant_category(session, category)
    return [MerchantResponseDto.model_validate(m) for m in merchants]


def update_merchant(
    session: Session, merchant_id: UUID, request: MerchantUpdateRequestDto
) -> MerchantResponseDto:
    repo = MerchantRepo()
    merchant = repo.get_by_id(session, merchant_id)
    if not merchant:
        raise MerchantNotFoundError
    updates = request.model_dump(exclude_none=True)
    if not updates:
        raise ValueError("No fields provided")
    repo.update(merchant, **updates)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
    return MerchantResponseDto.model_validate(merchant)


def delete_merchant(session: Session, merchant_id: UUID) -> None:
    repo = MerchantRepo()
    merchant = repo.get_by_id(session, merchant_id)
    if not merchant:
        raise MerchantNotFoundError()
    repo.delete(session, merchant)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
