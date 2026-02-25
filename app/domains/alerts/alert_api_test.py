from __future__ import annotations

import uuid

from fastapi.testclient import TestClient

from app.domains.enums import AlertSeverity, AlertStatus


def test_create_alert_success(
    client: TestClient, make_user, make_card, make_merchant, make_transaction
):
    user = make_user()
    card = make_card(user_id=user.id)
    merchant = make_merchant()
    transaction = make_transaction(
        user_id=user.id,
        card_id=card.id,
        merchant_id=merchant.id,
    )

    resp = client.post(
        "/api/v1/alerts",
        json={
            "user_id": str(user.id),
            "card_id": str(card.id),
            "transaction_id": str(transaction.id),
            "severity": AlertSeverity.MEDIUM,
            "status": AlertStatus.OPEN,
        },
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()

    assert "id" in data
    assert data["user_id"] == str(user.id)
    assert data["card_id"] == str(card.id)
    assert data["transaction_id"] == str(transaction.id)

    assert data["severity"] in (
        AlertSeverity.MEDIUM,
        AlertSeverity.MEDIUM.value,
    )
    assert data["status"] in (
        AlertStatus.OPEN,
        AlertStatus.OPEN.value,
    )
    assert "created_at" in data
    assert "updated_at" in data


def test_create_alert_duplicate_transaction_id_returns_409(
    client: TestClient, make_user, make_card, make_merchant, make_transaction
):
    user = make_user()
    card = make_card(user_id=user.id)
    merchant = make_merchant()
    transaction = make_transaction(
        user_id=user.id,
        card_id=card.id,
        merchant_id=merchant.id,
    )

    payload = {
        "user_id": str(user.id),
        "card_id": str(card.id),
        "transaction_id": str(transaction.id),
        "severity": AlertSeverity.HIGH,
        "status": AlertStatus.OPEN,
    }

    resp1 = client.post("/api/v1/alerts", json=payload)
    assert resp1.status_code == 201, resp1.text

    resp2 = client.post("/api/v1/alerts", json=payload)
    assert resp2.status_code == 409, resp2.text


def test_get_alert_success(client: TestClient, make_alert):
    alert = make_alert()

    resp = client.get(f"/api/v1/alerts/{alert.id}")
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert data["id"] == str(alert.id)


def test_get_alert_not_found(client: TestClient):
    resp = client.get(f"/api/v1/alerts/{uuid.UUID(int=0)}")
    assert resp.status_code == 404, resp.text


def test_update_alert_success(client: TestClient, make_alert):
    alert = make_alert(status=AlertStatus.OPEN)

    resp = client.patch(
        f"/api/v1/alerts/{alert.id}",
        json={"status": AlertStatus.RESOLVED},
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert data["id"] == str(alert.id)
    assert data["status"] in (
        AlertStatus.RESOLVED,
        AlertStatus.RESOLVED.value,
    )


def test_update_alert_not_found(client: TestClient):
    resp = client.patch(
        f"/api/v1/alerts/{uuid.UUID(int=0)}",
        json={"status": AlertStatus.RESOLVED},
    )
    assert resp.status_code == 404, resp.text


def test_delete_alert_success(client: TestClient, make_alert):
    alert = make_alert()

    resp = client.delete(f"/api/v1/alerts/{alert.id}")
    assert resp.status_code == 204, resp.text
    assert resp.text == ""

    resp2 = client.get(f"/api/v1/alerts/{alert.id}")
    assert resp2.status_code == 404, resp2.text


def test_delete_alert_not_found(client: TestClient):
    resp = client.delete(f"/api/v1/alerts/{uuid.UUID(int=0)}")
    assert resp.status_code == 404, resp.text
