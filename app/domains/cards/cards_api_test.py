from __future__ import annotations

import uuid

from fastapi.testclient import TestClient

from app.domains.enums import CardBrand, CardStatus


def test_create_card_success(client: TestClient, make_user):
    user = make_user()

    resp = client.post(
        "/api/v1/cards",
        json={
            "user_id": str(user.id),
            "last4": 1234,
            "brand": CardBrand.VISA,
            "status": CardStatus.ACTIVE,
            "exp_month": 12,
            "exp_year": 2027,
        },
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()

    assert "id" in data
    assert data["user_id"] == str(user.id)
    assert data["last4"] == 1234
    assert data["brand"] in (CardBrand.VISA, CardBrand.VISA.value)
    assert data["status"] in (CardStatus.ACTIVE, CardStatus.ACTIVE.value)
    assert data["exp_month"] == 12
    assert data["exp_year"] == 2027


def test_get_card_success(client: TestClient, make_card):
    card = make_card(last4=1111)

    resp = client.get(f"/api/v1/cards/{card.id}")
    assert resp.status_code == 200, resp.text
    assert resp.json()["id"] == str(card.id)


def test_get_card_not_found(client: TestClient):
    resp = client.get(f"/api/v1/cards/{uuid.UUID(int=0)}")
    assert resp.status_code == 404, resp.text


def test_update_card_success(client: TestClient, make_card):
    card = make_card(status=CardStatus.ACTIVE)

    resp = client.patch(
        f"/api/v1/cards/{card.id}",
        json={
            "status": CardStatus.FROZEN,
        },
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert data["id"] == str(card.id)
    assert data["status"] == CardStatus.FROZEN


def test_update_card_not_found(client: TestClient):
    resp = client.patch(
        f"/api/v1/cards/{uuid.UUID(int=0)}",
        json={"status": CardStatus.FROZEN},
    )
    assert resp.status_code == 404, resp.text


def test_delete_card_success(client: TestClient, make_card):
    card = make_card()

    resp = client.delete(f"/api/v1/cards/{card.id}")
    assert resp.status_code == 204, resp.text
    assert resp.text == ""

    resp2 = client.get(f"/api/v1/cards/{card.id}")
    assert resp2.status_code == 404, resp2.text


def test_delete_card_not_found(client: TestClient):
    resp = client.delete(f"/api/v1/cards/{uuid.UUID(int=0)}")
    assert resp.status_code == 404, resp.text
