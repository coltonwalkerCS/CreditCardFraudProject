from __future__ import annotations

import uuid

import pytest

from app.domains.alerts.alerts_commands import (
    AlertAlreadyExistsError,
    AlertNotFoundError,
    create_alert,
    delete_alert,
    get_alert,
    update_alert,
)
from app.domains.alerts.dtos import AlertCreateRequestDto, AlertUpdateRequestDto
from app.domains.enums import AlertSeverity, AlertStatus


def test_create_alert_success(
    session, make_user, make_card, make_merchant, make_transaction
):
    user = make_user()
    card = make_card(user_id=user.id)
    merchant = make_merchant()
    transaction = make_transaction(
        user_id=user.id, card_id=card.id, merchant_id=merchant.id
    )

    created = create_alert(
        session,
        AlertCreateRequestDto(
            user_id=user.id,
            card_id=card.id,
            transaction_id=transaction.id,
            severity=AlertSeverity.MEDIUM,
            status=AlertStatus.OPEN,
        ),
    )

    assert created.id is not None
    assert created.user_id == user.id
    assert created.card_id == card.id
    assert created.transaction_id == transaction.id
    assert created.severity == AlertSeverity.MEDIUM
    assert created.status == AlertStatus.OPEN
    assert created.created_at is not None
    assert created.updated_at is not None


def test_create_alert_duplicate_transaction_id_raises(
    session, make_user, make_card, make_merchant, make_transaction
):
    user = make_user()
    card = make_card(user_id=user.id)
    merchant = make_merchant()
    transaction = make_transaction(
        user_id=user.id, card_id=card.id, merchant_id=merchant.id
    )

    create_alert(
        session,
        AlertCreateRequestDto(
            user_id=user.id,
            card_id=card.id,
            transaction_id=transaction.id,
            severity=AlertSeverity.HIGH,
            status=AlertStatus.OPEN,
        ),
    )

    with pytest.raises(AlertAlreadyExistsError):
        create_alert(
            session,
            AlertCreateRequestDto(
                user_id=user.id,
                card_id=card.id,
                transaction_id=transaction.id,
                severity=AlertSeverity.HIGH,
                status=AlertStatus.OPEN,
            ),
        )


def test_get_alert_not_found(session):
    with pytest.raises(AlertNotFoundError):
        get_alert(session, uuid.uuid4())


def test_get_alert_success(session, make_alert):
    created = make_alert(status=AlertStatus.OPEN, severity=AlertSeverity.LOW)

    fetched = get_alert(session, created.id)

    assert fetched.id == created.id
    assert fetched.user_id == created.user_id
    assert fetched.card_id == created.card_id
    assert fetched.transaction_id == created.transaction_id
    assert fetched.status == AlertStatus.OPEN
    assert fetched.severity == AlertSeverity.LOW


def test_update_alert_not_found(session):
    with pytest.raises(AlertNotFoundError):
        update_alert(
            session,
            uuid.uuid4(),
            AlertUpdateRequestDto(status=AlertStatus.ACKED),
        )


def test_update_alert_success(session, make_alert):
    created = make_alert(status=AlertStatus.OPEN)

    updated = update_alert(
        session,
        created.id,
        AlertUpdateRequestDto(status=AlertStatus.RESOLVED),
    )

    assert updated.id == created.id
    assert updated.status == AlertStatus.RESOLVED

    fetched = get_alert(session, created.id)
    assert fetched.status == AlertStatus.RESOLVED


def test_delete_alert_not_found(session):
    with pytest.raises(AlertNotFoundError):
        delete_alert(session, uuid.uuid4())


def test_delete_alert_success(session, make_alert):
    created = make_alert()

    delete_alert(session, created.id)

    with pytest.raises(AlertNotFoundError):
        get_alert(session, created.id)
