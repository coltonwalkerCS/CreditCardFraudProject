from __future__ import annotations

from fastapi.testclient import TestClient


def test_create_user_success(client: TestClient):
    resp = client.post("/api/v1/users", json={"username": "colton"})
    assert resp.status_code == 201, resp.text

    data = resp.json()
    assert data["username"] == "colton"
    assert "id" in data


def test_get_user_success(client: TestClient):
    created = client.post("/api/v1/users", json={"username": "colton"}).json()
    user_id = created["id"]

    resp = client.get(f"/api/v1/users/{user_id}")
    assert resp.status_code == 200, resp.text
    assert resp.json()["id"] == user_id


def test_get_user_not_found(client: TestClient):
    # random UUID
    resp = client.get("/api/v1/users/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


def test_create_user_duplicate_username_conflict(client: TestClient):
    r1 = client.post("/api/v1/users", json={"username": "dup"})
    assert r1.status_code == 201, r1.text

    r2 = client.post("/api/v1/users", json={"username": "dup"})
    # assuming you map UsernameAlreadyExistsError -> 409
    assert r2.status_code == 409, r2.text


def test_update_user_success(client: TestClient):
    created = client.post("/api/v1/users", json={"username": "old"}).json()
    user_id = created["id"]

    resp = client.patch(f"/api/v1/users/{user_id}", json={"username": "new"})
    assert resp.status_code == 200, resp.text
    assert resp.json()["username"] == "new"


def test_delete_user_success(client: TestClient):
    created = client.post("/api/v1/users", json={"username": "todelete"}).json()
    user_id = created["id"]

    resp = client.delete(f"/api/v1/users/{user_id}")
    assert resp.status_code == 204, resp.text

    resp2 = client.get(f"/api/v1/users/{user_id}")
    assert resp2.status_code == 404
