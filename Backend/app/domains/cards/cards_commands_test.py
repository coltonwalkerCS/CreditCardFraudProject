from __future__ import annotations

import uuid

import pytest
from app.domains.cards.cards_commands import (
    CardAlreadyExistsError,
    CardNotFoundError,
    create_card,
    delete_card,
    get_card,
    list_cards_for_user,
    update_card,
)
from app.domains.cards.dtos import CardCreateRequestDto, CardUpdateRequestDto
from app.domains.enums import CardBrand, CardStatus


def test_create_card_success(session, make_user):
    user = make_user()

    created = create_card(
        session,
        CardCreateRequestDto(
            user_id=user.id,
            last4=1234,
            brand=CardBrand.VISA,
            status=CardStatus.ACTIVE,
            exp_month=12,
            exp_year=2027,
        ),
    )

    assert created.id is not None
    assert created.user_id == user.id
    assert created.last4 == 1234
    assert created.brand == CardBrand.VISA
    assert created.status == CardStatus.ACTIVE
    assert created.exp_month == 12
    assert created.exp_year == 2027
    assert created.created_at is not None
    assert created.updated_at is not None


def test_create_card_duplicate_for_same_user_raises(session, make_user):
    user = make_user()

    create_card(
        session,
        CardCreateRequestDto(
            user_id=user.id,
            last4=1234,
            brand=CardBrand.VISA,
            status=CardStatus.ACTIVE,
            exp_month=12,
            exp_year=2027,
        ),
    )

    with pytest.raises(CardAlreadyExistsError):
        create_card(
            session,
            CardCreateRequestDto(
                user_id=user.id,
                last4=1234,
                brand=CardBrand.MASTERCARD,
                status=CardStatus.ACTIVE,
                exp_month=11,
                exp_year=2028,
            ),
        )


def test_create_card_same_last4_different_user_allowed(session, make_user):
    user1 = make_user()
    user2 = make_user()

    create_card(
        session,
        CardCreateRequestDto(
            user_id=user1.id,
            last4=1234,
            brand=CardBrand.VISA,
            status=CardStatus.ACTIVE,
            exp_month=12,
            exp_year=2027,
        ),
    )

    created2 = create_card(
        session,
        CardCreateRequestDto(
            user_id=user2.id,
            last4=1234,
            brand=CardBrand.VISA,
            status=CardStatus.ACTIVE,
            exp_month=1,
            exp_year=2029,
        ),
    )

    assert created2.id is not None
    assert created2.last4 == 1234


def test_get_card_not_found(session):
    with pytest.raises(CardNotFoundError):
        get_card(session, uuid.uuid4())


def test_get_card_success(session, make_card):
    created = make_card(last4=2222)

    fetched = get_card(session, created.id)

    assert fetched.id == created.id
    assert fetched.user_id == created.user_id
    assert fetched.last4 == 2222


def test_list_cards_for_user_empty(session, make_user):
    user = make_user()

    cards = list_cards_for_user(session, user.id)

    assert cards == []


def test_list_cards_for_user_returns_only_that_users_cards(
    session, make_user, make_card
):
    user1 = make_user()
    user2 = make_user()

    c1 = make_card(user_id=user1.id, last4=1000)
    c2 = make_card(user_id=user1.id, last4=2000)
    make_card(user_id=user2.id, last4=9999)

    cards = list_cards_for_user(session, user1.id)

    assert len(cards) == 2
    assert {c.id for c in cards} == {c1.id, c2.id}
    assert {c.last4 for c in cards} == {1000, 2000}


def test_update_card_not_found(session):
    with pytest.raises(CardNotFoundError):
        update_card(
            session,
            uuid.uuid4(),
            CardUpdateRequestDto(status=CardStatus.FROZEN),
        )


def test_update_card_success(session, make_card):
    created = make_card(status=CardStatus.ACTIVE)

    updated = update_card(
        session,
        created.id,
        CardUpdateRequestDto(status=CardStatus.FROZEN),
    )

    assert updated.id == created.id
    assert updated.status == CardStatus.FROZEN

    fetched = get_card(session, created.id)
    assert fetched.status == CardStatus.FROZEN


def test_delete_card_not_found(session):
    with pytest.raises(CardNotFoundError):
        delete_card(session, uuid.uuid4())


def test_delete_card_success(session, make_card):
    created = make_card()

    delete_card(session, created.id)

    with pytest.raises(CardNotFoundError):
        get_card(session, created.id)
