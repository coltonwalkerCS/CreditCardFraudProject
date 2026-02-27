from __future__ import annotations

import uuid

import pytest
from sqlalchemy.orm import Session

from app.domains.alert_actions import alert_actions_commands
from app.domains.alert_actions.dtos import (
    AlertActionCreateRequestDto,
    AlertActionUpdateRequestDto,
)
from app.domains.enums import ActorType, AlertActionType


def test_create_alert_action_success(session: Session, make_alert):
    alert = make_alert()

    req = AlertActionCreateRequestDto(
        alert_id=alert.id,
        action=AlertActionType.ACK,
        actor_type=ActorType.SYSTEM,
    )

    resp = alert_actions_commands.create_alert_action(session, req)

    assert resp.id
    assert resp.alert_id == alert.id
    assert resp.action == AlertActionType.ACK
    assert resp.actor_type == ActorType.SYSTEM


def test_create_alert_action_already_exists_raises(session: Session, make_alert):
    alert = make_alert()

    req = AlertActionCreateRequestDto(
        alert_id=alert.id,
        action=AlertActionType.ACK,
        actor_type=ActorType.SYSTEM,
    )

    alert_actions_commands.create_alert_action(session, req)

    # If you enforce uniqueness, second create should raise
    assert hasattr(alert_actions_commands, "AlertActionAlreadyExistsError"), (
        "If you want this test, implement AlertActionAlreadyExistsError "
        "and enforce uniqueness (e.g., unique constraint)."
    )

    with pytest.raises(alert_actions_commands.AlertActionAlreadyExistsError):
        alert_actions_commands.create_alert_action(session, req)


def test_get_alert_action_success(session: Session, make_alert_action):
    created = make_alert_action()

    fetched = alert_actions_commands.get_alert_action(session, created.id)

    assert fetched.id == created.id
    assert fetched.alert_id == created.alert_id
    assert fetched.action == created.action
    assert fetched.actor_type == created.actor_type


def test_get_alert_action_not_found_raises(session: Session):
    missing_id = uuid.uuid4()

    with pytest.raises(alert_actions_commands.AlertActionNotFoundError):
        alert_actions_commands.get_alert_action(session, missing_id)


def test_update_alert_action_full_update_success(session: Session, make_alert_action):
    created = make_alert_action(
        action=AlertActionType.ACK,
        actor_type=ActorType.SYSTEM,
    )

    req = AlertActionUpdateRequestDto(
        action=AlertActionType.RESOLVE,
        actor_type=ActorType.USER,
    )

    updated = alert_actions_commands.update_alert_action(session, created.id, req)

    assert updated.id == created.id
    assert updated.action == AlertActionType.RESOLVE
    assert updated.actor_type == ActorType.USER


def test_update_alert_action_partial_update_action_only(
    session: Session, make_alert_action
):
    """
    Ensures PATCH-like behavior:
    - only provided non-null fields update
    - other fields remain unchanged
    """
    created = make_alert_action(
        action=AlertActionType.ACK,
        actor_type=ActorType.SYSTEM,
    )

    req = AlertActionUpdateRequestDto(
        action=AlertActionType.RESOLVE,
        actor_type=None,
    )

    updated = alert_actions_commands.update_alert_action(session, created.id, req)

    assert updated.action == AlertActionType.RESOLVE
    assert updated.actor_type == ActorType.SYSTEM


def test_update_alert_action_partial_update_actor_type_only(
    session: Session, make_alert_action
):
    created = make_alert_action(
        action=AlertActionType.ACK,
        actor_type=ActorType.SYSTEM,
    )

    req = AlertActionUpdateRequestDto(
        action=None,
        actor_type=ActorType.USER,
    )

    updated = alert_actions_commands.update_alert_action(session, created.id, req)

    assert updated.action == AlertActionType.ACK
    assert updated.actor_type == ActorType.USER


def test_update_alert_action_not_found_raises(session: Session):
    missing_id = uuid.uuid4()

    req = AlertActionUpdateRequestDto(
        action=AlertActionType.ACK,
        actor_type=ActorType.USER,
    )

    with pytest.raises(alert_actions_commands.AlertActionNotFoundError):
        alert_actions_commands.update_alert_action(session, missing_id, req)


def test_delete_alert_action_success(session: Session, make_alert_action):
    created = make_alert_action()

    alert_actions_commands.delete_alert_action(session, created.id)

    with pytest.raises(alert_actions_commands.AlertActionNotFoundError):
        alert_actions_commands.get_alert_action(session, created.id)


def test_delete_alert_action_not_found_raises(session: Session):
    missing_id = uuid.uuid4()

    with pytest.raises(alert_actions_commands.AlertActionNotFoundError):
        alert_actions_commands.delete_alert_action(session, missing_id)
