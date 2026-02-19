from __future__ import annotations

import uuid

import pytest
from sqlalchemy.orm import Session

from app.domains.enums import MerchantCategory
from app.domains.merchants.dtos import (
    MerchantCreateRequestDto,
    MerchantUpdateRequestDto,
)
from app.domains.merchants.merchant_commands import (
    MerchantAlreadyExistsError,
    MerchantNotFoundError,
    create_merchant,
    delete_merchant,
    get_merchant,
    list_merchants_by_category,
    update_merchant,
)


def test_create_merchant_success(session: Session):
    resp = create_merchant(
        session,
        MerchantCreateRequestDto(name="Whole Foods", category=MerchantCategory.GROCERY),
    )

    assert resp.id is not None
    assert resp.name == "Whole Foods"
    assert resp.category == MerchantCategory.GROCERY
    assert resp.created_at is not None
    assert resp.updated_at is not None


def test_create_merchant_duplicate_name_raises(session: Session):
    create_merchant(
        session,
        MerchantCreateRequestDto(name="Shell", category=MerchantCategory.GAS),
    )

    with pytest.raises(MerchantAlreadyExistsError):
        create_merchant(
            session,
            MerchantCreateRequestDto(name="Shell", category=MerchantCategory.GAS),
        )


def test_get_merchant_success(session: Session, make_merchant):
    created = make_merchant(name="Starbucks", category=MerchantCategory.RESTAURANT)
    fetched = get_merchant(session, created.id)

    assert fetched.id == created.id
    assert fetched.name == "Starbucks"
    assert fetched.category == MerchantCategory.RESTAURANT


def test_get_merchant_not_found(session: Session):
    missing_id = uuid.uuid4()
    with pytest.raises(MerchantNotFoundError):
        get_merchant(session, missing_id)


def test_list_merchants_by_category_returns_only_that_category(
    session: Session, make_merchant
):
    g1 = make_merchant(category=MerchantCategory.GROCERY)
    g2 = make_merchant(category=MerchantCategory.GROCERY)
    _r = make_merchant(category=MerchantCategory.RESTAURANT)

    results = list_merchants_by_category(session, MerchantCategory.GROCERY)
    ids = {m.id for m in results}

    assert g1.id in ids
    assert g2.id in ids
    assert _r.id not in ids


def test_update_merchant_partial_name_only(session: Session, make_merchant):
    created = make_merchant(name="Target", category=MerchantCategory.ONLINE_RETAIL)

    updated = update_merchant(
        session,
        created.id,
        MerchantUpdateRequestDto(name="Target (Updated)", category=None),
    )

    assert updated.id == created.id
    assert updated.name == "Target (Updated)"
    assert updated.category == MerchantCategory.ONLINE_RETAIL  # unchanged


def test_update_merchant_partial_category_only(session: Session, make_merchant):
    created = make_merchant(name="Hy-Vee", category=MerchantCategory.GROCERY)

    updated = update_merchant(
        session,
        created.id,
        MerchantUpdateRequestDto(name=None, category=MerchantCategory.RESTAURANT),
    )

    assert updated.id == created.id
    assert updated.name == "Hy-Vee"  # unchanged
    assert updated.category == MerchantCategory.RESTAURANT


def test_update_merchant_not_found(session: Session):
    with pytest.raises(MerchantNotFoundError):
        update_merchant(
            session,
            uuid.uuid4(),
            MerchantUpdateRequestDto(name="Doesn't matter", category=None),
        )


def test_update_merchant_empty_update_raises(session: Session, make_merchant):
    """
    This test assumes you added:
        if not updates: raise ValueError(...)
    If you decide to allow no-op updates, delete this test.
    """
    created = make_merchant()

    with pytest.raises(ValueError):
        update_merchant(
            session,
            created.id,
            MerchantUpdateRequestDto(name=None, category=None),
        )


def test_delete_merchant_success(session: Session, make_merchant):
    created = make_merchant()

    delete_merchant(session, created.id)

    with pytest.raises(MerchantNotFoundError):
        get_merchant(session, created.id)


def test_delete_merchant_not_found(session: Session):
    with pytest.raises(MerchantNotFoundError):
        delete_merchant(session, uuid.uuid4())
