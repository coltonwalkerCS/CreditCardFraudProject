# tests/api/v1/alert_actions_api_test.py
from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient

from app.domains.enums import ActorType, AlertActionType

BASE_URL = "/api/v1/alert_actions"  # change if your router is mounted differently


def test_create_alert_action_success(client: TestClient, make_alert):
    alert = make_alert()

    resp = client.post(
        BASE_URL,
        json={
            "alert_id": str(alert.id),
            "action": AlertActionType.ACK,
            "actor_type": ActorType.USER,
        },
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()

    assert "id" in data
    assert data["alert_id"] == str(alert.id)
    assert data["action"] == AlertActionType.ACK
    assert data["actor_type"] == ActorType.USER


def test_get_alert_action_success(client: TestClient, make_alert):
    alert = make_alert()

    create_resp = client.post(
        BASE_URL,
        json={
            "alert_id": str(alert.id),
            "action": AlertActionType.ACK,
            "actor_type": ActorType.SYSTEM,
        },
    )
    assert create_resp.status_code == 201, create_resp.text
    created = create_resp.json()
    alert_action_id = created["id"]

    get_resp = client.get(f"{BASE_URL}/{alert_action_id}")
    assert get_resp.status_code == 200, get_resp.text
    fetched = get_resp.json()

    assert fetched["id"] == alert_action_id
    assert fetched["alert_id"] == str(alert.id)
    assert fetched["action"] == AlertActionType.ACK
    assert fetched["actor_type"] == ActorType.SYSTEM


def test_get_alert_action_not_found(client: TestClient):
    missing_id = uuid.uuid4()
    resp = client.get(f"{BASE_URL}/{missing_id}")
    assert resp.status_code == 404, resp.text


def test_patch_alert_action_partial_update_action_only(client: TestClient, make_alert):
    alert = make_alert()

    create_resp = client.post(
        BASE_URL,
        json={
            "alert_id": str(alert.id),
            "action": AlertActionType.ACK,
            "actor_type": ActorType.ANALYST,
        },
    )
    assert create_resp.status_code == 201, create_resp.text
    created = create_resp.json()

    patch_resp = client.patch(
        f"{BASE_URL}/{created['id']}",
        json={
            "action": AlertActionType.RESOLVE,
        },
    )
    assert patch_resp.status_code == 200, patch_resp.text
    updated = patch_resp.json()

    assert updated["id"] == created["id"]
    assert updated["alert_id"] == created["alert_id"]
    assert updated["action"] == AlertActionType.RESOLVE
    assert updated["actor_type"] == ActorType.ANALYST  # unchanged


def test_patch_alert_action_null_is_ignored_when_exclude_none_true(
    client: TestClient, make_alert
):
    alert = make_alert()

    # Create
    create_resp = client.post(
        BASE_URL,
        json={
            "alert_id": str(alert.id),
            "action": AlertActionType.ACK,
            "actor_type": ActorType.SYSTEM,
        },
    )
    assert create_resp.status_code == 201, create_resp.text
    created = create_resp.json()

    patch_resp = client.patch(
        f"{BASE_URL}/{created['id']}",
        json={
            "action": AlertActionType.ESCALATE,
            "actor_type": None,  # JSON null
        },
    )
    assert patch_resp.status_code == 200, patch_resp.text
    updated = patch_resp.json()

    assert updated["action"] == AlertActionType.ESCALATE
    assert updated["actor_type"] == ActorType.SYSTEM


def test_patch_alert_action_not_found(client: TestClient):
    missing_id = uuid.uuid4()
    resp = client.patch(
        f"{BASE_URL}/{missing_id}",
        json={"action": AlertActionType.RESOLVE},
    )
    assert resp.status_code == 404, resp.text


def test_delete_alert_action_success(client: TestClient, make_alert):
    alert = make_alert()

    create_resp = client.post(
        BASE_URL,
        json={
            "alert_id": str(alert.id),
            "action": AlertActionType.ACK,
            "actor_type": ActorType.USER,
        },
    )
    assert create_resp.status_code == 201, create_resp.text
    created = create_resp.json()

    del_resp = client.delete(f"{BASE_URL}/{created['id']}")
    assert del_resp.status_code == 204, del_resp.text
    assert del_resp.content in (b"", None)

    get_resp = client.get(f"{BASE_URL}/{created['id']}")
    assert get_resp.status_code == 404, get_resp.text


def test_delete_alert_action_not_found(client: TestClient):
    missing_id = uuid.uuid4()
    resp = client.delete(f"{BASE_URL}/{missing_id}")
    assert resp.status_code == 404, resp.text


@pytest.mark.optional
def test_create_alert_action_conflict_409_if_uniqueness_enforced(
    client: TestClient, make_alert
):
    alert = make_alert()

    body = {
        "alert_id": str(alert.id),
        "action": AlertActionType.ACK,
        "actor_type": ActorType.USER,
    }

    resp1 = client.post(BASE_URL, json=body)
    assert resp1.status_code == 201, resp1.text

    resp2 = client.post(BASE_URL, json=body)
    assert resp2.status_code == 409, resp2.text
