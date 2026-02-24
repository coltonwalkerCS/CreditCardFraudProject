from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal

from fastapi.testclient import TestClient

from app.domains.enums import TransactionStatus


def test_create_transaction_success(
    client: TestClient, make_user, make_card, make_merchant
):
    user = make_user()
    card = make_card(user_id=user.id)
    merchant = make_merchant()

    resp = client.post(
        "/api/v1/transactions",
        json={
            "user_id": str(user.id),
            "card_id": str(card.id),
            "merchant_id": str(merchant.id),
            "amount": "12.34",
            "occurred_at": datetime.now(timezone.utc).isoformat(),
            "status": TransactionStatus.APPROVED,
            "idempotency_key": str(uuid.uuid4()),
        },
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()

    assert "id" in data
    assert data["user_id"] == str(user.id)
    assert data["card_id"] == str(card.id)
    assert data["merchant_id"] == str(merchant.id)
    assert Decimal(str(data["amount"])) == Decimal("12.34")
    assert data["occurred_at"] is not None
    assert data["status"] in (
        TransactionStatus.APPROVED,
        TransactionStatus.APPROVED.value,
    )
    assert "created_at" in data
    assert "updated_at" in data


def test_create_transaction_duplicate_idempotency_key_returns_409(
    client: TestClient, make_user, make_card, make_merchant
):
    user = make_user()
    card = make_card(user_id=user.id)
    merchant = make_merchant()
    idem = uuid.uuid4()

    payload = {
        "user_id": str(user.id),
        "card_id": str(card.id),
        "merchant_id": str(merchant.id),
        "amount": "12.34",
        "occurred_at": datetime.now(timezone.utc).isoformat(),
        "status": TransactionStatus.APPROVED,
        "idempotency_key": str(idem),
    }

    resp1 = client.post("/api/v1/transactions", json=payload)
    assert resp1.status_code == 201, resp1.text

    resp2 = client.post("/api/v1/transactions", json=payload)
    assert resp2.status_code == 409, resp2.text


def test_get_transaction_success(client: TestClient, make_transaction):
    tx = make_transaction(amount=Decimal("99.99"))

    resp = client.get(f"/api/v1/transactions/{tx.id}")
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert data["id"] == str(tx.id)
    assert Decimal(str(data["amount"])) == Decimal("99.99")


def test_get_transaction_not_found(client: TestClient):
    resp = client.get(f"/api/v1/transactions/{uuid.UUID(int=0)}")
    assert resp.status_code == 404, resp.text


def test_update_transaction_success(client: TestClient, make_transaction):
    tx = make_transaction(status=TransactionStatus.APPROVED)

    resp = client.patch(
        f"/api/v1/transactions/{tx.id}",
        json={"status": TransactionStatus.DECLINED},
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert data["id"] == str(tx.id)
    assert data["status"] in (
        TransactionStatus.DECLINED,
        TransactionStatus.DECLINED.value,
    )


def test_update_transaction_not_found(client: TestClient):
    resp = client.patch(
        f"/api/v1/transactions/{uuid.UUID(int=0)}",
        json={"status": TransactionStatus.DECLINED},
    )
    assert resp.status_code == 404, resp.text


def test_delete_transaction_success(client: TestClient, make_transaction):
    tx = make_transaction()

    resp = client.delete(f"/api/v1/transactions/{tx.id}")
    assert resp.status_code == 204, resp.text
    assert resp.text == ""

    resp2 = client.get(f"/api/v1/transactions/{tx.id}")
    assert resp2.status_code == 404, resp2.text


def test_delete_transaction_not_found(client: TestClient):
    resp = client.delete(f"/api/v1/transactions/{uuid.UUID(int=0)}")
    assert resp.status_code == 404, resp.text
