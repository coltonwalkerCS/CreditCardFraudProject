from __future__ import annotations

import uuid

from fastapi.testclient import TestClient

from app.domains.enums import MerchantCategory


def test_create_merchant_success(client: TestClient):
    resp = client.post(
        "/api/v1/merchants",
        json={
            "name": "Test Grocery",
            "category": MerchantCategory.GROCERY,
        },
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()

    assert "id" in data
    assert data["name"] == "Test Grocery"
    assert data["category"] in (
        MerchantCategory.GROCERY,
        MerchantCategory.GROCERY.value,
    )


def test_get_merchant_success(client: TestClient, make_merchant):
    merchant = make_merchant(name="Acme Grocery")

    resp = client.get(f"/api/v1/merchants/{merchant.id}")
    assert resp.status_code == 200, resp.text
    assert resp.json()["id"] == str(merchant.id)


def test_get_merchant_not_found(client: TestClient):
    resp = client.get(f"/api/v1/merchants/{uuid.UUID(int=0)}")
    assert resp.status_code == 404, resp.text


def test_update_merchant_success(client: TestClient, make_merchant):
    merchant = make_merchant(name="Acme Grocery", category=MerchantCategory.GROCERY)

    resp = client.patch(
        f"/api/v1/merchants/{merchant.id}",
        json={
            "name": "Acme Grocery 2",
            "category": MerchantCategory.GAS,
        },
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert data["id"] == str(merchant.id)
    assert data["name"] == "Acme Grocery 2"
    assert data["category"] in (MerchantCategory.GAS, MerchantCategory.GAS.value)


def test_update_merchant_not_found(client: TestClient):
    resp = client.patch(
        f"/api/v1/merchants/{uuid.UUID(int=0)}",
        json={"name": "Does Not Exist"},
    )
    assert resp.status_code == 404, resp.text


def test_delete_merchant_success(client: TestClient, make_merchant):
    merchant = make_merchant()

    resp = client.delete(f"/api/v1/merchants/{merchant.id}")
    assert resp.status_code == 204, resp.text
    assert resp.text == ""

    resp2 = client.get(f"/api/v1/merchants/{merchant.id}")
    assert resp2.status_code == 404, resp2.text


def test_delete_merchant_not_found(client: TestClient):
    resp = client.delete(f"/api/v1/merchants/{uuid.UUID(int=0)}")
    assert resp.status_code == 404, resp.text
