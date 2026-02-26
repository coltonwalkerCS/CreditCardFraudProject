from __future__ import annotations

import uuid

from fastapi.testclient import TestClient

from app.domains.enums import FindingCode


def test_create_alert_finding_success(client: TestClient, make_alert):
    alert = make_alert()

    resp = client.post(
        "/api/v1/alert_findings",
        json={
            "alert_id": str(alert.id),
            "code": FindingCode.VELOCITY,
        },
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()

    assert "id" in data
    assert data["alert_id"] == str(alert.id)

    assert data["code"] in (
        FindingCode.VELOCITY,
        FindingCode.VELOCITY.value,
    )
    assert "created_at" in data
    assert "updated_at" in data


def test_create_alert_finding_duplicate_alert_id_returns_409(
    client: TestClient, make_alert
):
    alert = make_alert()

    payload = {
        "alert_id": str(alert.id),
        "code": FindingCode.LARGE_AMOUNT,
    }

    resp1 = client.post("/api/v1/alert_findings", json=payload)
    assert resp1.status_code == 201, resp1.text

    resp2 = client.post("/api/v1/alert_findings", json=payload)
    assert resp2.status_code == 409, resp2.text


def test_get_alert_finding_success(client: TestClient, make_alert_finding):
    finding = make_alert_finding(code=FindingCode.NEW_MERCHANT)

    resp = client.get(f"/api/v1/alert_findings/{finding.id}")
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert data["id"] == str(finding.id)
    assert data["alert_id"] == str(finding.alert_id)
    assert data["code"] in (
        FindingCode.NEW_MERCHANT,
        FindingCode.NEW_MERCHANT.value,
    )


def test_get_alert_finding_not_found(client: TestClient):
    resp = client.get(f"/api/v1/alert_findings/{uuid.UUID(int=0)}")
    assert resp.status_code == 404, resp.text


def test_update_alert_finding_success(client: TestClient, make_alert_finding):
    finding = make_alert_finding(code=FindingCode.LARGE_AMOUNT)

    resp = client.patch(
        f"/api/v1/alert_findings/{finding.id}",
        json={"code": FindingCode.IMPOSSIBLE_TRAVEL},
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert data["id"] == str(finding.id)
    assert data["code"] in (
        FindingCode.IMPOSSIBLE_TRAVEL,
        FindingCode.IMPOSSIBLE_TRAVEL.value,
    )


def test_update_alert_finding_not_found(client: TestClient):
    resp = client.patch(
        f"/api/v1/alert_findings/{uuid.UUID(int=0)}",
        json={"code": FindingCode.CATEGORY_SPIKE},
    )
    assert resp.status_code == 404, resp.text


def test_delete_alert_finding_success(client: TestClient, make_alert_finding):
    finding = make_alert_finding(code=FindingCode.VELOCITY)

    resp = client.delete(f"/api/v1/alert_findings/{finding.id}")
    assert resp.status_code == 204, resp.text
    assert resp.text == ""

    resp2 = client.get(f"/api/v1/alert_findings/{finding.id}")
    assert resp2.status_code == 404, resp2.text


def test_delete_alert_finding_not_found(client: TestClient):
    resp = client.delete(f"/api/v1/alert_findings/{uuid.UUID(int=0)}")
    assert resp.status_code == 404, resp.text
