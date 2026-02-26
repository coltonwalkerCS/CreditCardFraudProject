from __future__ import annotations

import uuid

import pytest

from app.domains.alert_findings.alert_findings_commands import (
    AlertFindingAlreadyExistsError,
    AlertFindingNotFoundError,
    create_alert_finding,
    delete_alert_finding,
    get_alert_finding,
    update_alert_finding,
)
from app.domains.alert_findings.dtos import (
    AlertFindingCreateRequestDto,
    AlertFindingUpdateRequestDto,
)
from app.domains.enums import FindingCode


def test_create_alert_finding_success(session, make_alert):
    alert = make_alert()

    created = create_alert_finding(
        session,
        AlertFindingCreateRequestDto(
            alert_id=alert.id,
            code=FindingCode.VELOCITY,
        ),
    )

    assert created.id is not None
    assert created.alert_id == alert.id
    assert created.code == FindingCode.VELOCITY
    assert created.created_at is not None
    assert created.updated_at is not None


def test_create_alert_finding_duplicate_alert_id_raises(session, make_alert):
    alert = make_alert()

    create_alert_finding(
        session,
        AlertFindingCreateRequestDto(
            alert_id=alert.id,
            code=FindingCode.LARGE_AMOUNT,
        ),
    )

    with pytest.raises(AlertFindingAlreadyExistsError):
        create_alert_finding(
            session,
            AlertFindingCreateRequestDto(
                alert_id=alert.id,
                code=FindingCode.IMPOSSIBLE_TRAVEL,
            ),
        )


def test_get_alert_finding_not_found(session):
    with pytest.raises(AlertFindingNotFoundError):
        get_alert_finding(session, uuid.uuid4())


def test_get_alert_finding_success(session, make_alert_finding):
    created = make_alert_finding(code=FindingCode.NEW_MERCHANT)

    fetched = get_alert_finding(session, created.id)

    assert fetched.id == created.id
    assert fetched.alert_id == created.alert_id
    assert fetched.code == FindingCode.NEW_MERCHANT


def test_update_alert_finding_not_found(session):
    with pytest.raises(AlertFindingNotFoundError):
        update_alert_finding(
            session,
            uuid.uuid4(),
            AlertFindingUpdateRequestDto(code=FindingCode.CATEGORY_SPIKE),
        )


def test_update_alert_finding_success(session, make_alert_finding):
    created = make_alert_finding(code=FindingCode.LARGE_AMOUNT)

    updated = update_alert_finding(
        session,
        created.id,
        AlertFindingUpdateRequestDto(code=FindingCode.VELOCITY),
    )

    assert updated.id == created.id
    assert updated.code == FindingCode.VELOCITY

    fetched = get_alert_finding(session, created.id)
    assert fetched.code == FindingCode.VELOCITY


def test_delete_alert_finding_not_found(session):
    with pytest.raises(AlertFindingNotFoundError):
        delete_alert_finding(session, uuid.uuid4())


def test_delete_alert_finding_success(session, make_alert_finding):
    created = make_alert_finding(code=FindingCode.LARGE_AMOUNT)

    delete_alert_finding(session, created.id)

    with pytest.raises(AlertFindingNotFoundError):
        get_alert_finding(session, created.id)
