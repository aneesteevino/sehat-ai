from pathlib import Path

from fastapi.testclient import TestClient
from sehat_api.config import Settings
from sehat_api.main import create_app

ROOT = Path(__file__).resolve().parents[2]


def make_app():
    return create_app(
        Settings(
            app_env="test",
            auth_secret="test-secret-that-is-long-enough-32-bytes",
            knowledge_registry_path=ROOT / "data/source_registry/sources.json",
            _env_file=None,
        )
    )


def register_and_login(client: TestClient, email: str) -> dict[str, str]:
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "display_name": "Tester", "password": "long-test-password"},
    )
    login = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "long-test-password"},
    )
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_safety_and_workflow_routes_are_authenticated() -> None:
    with TestClient(make_app()) as client:
        safety = client.post("/api/v1/safety/check", json={"text": "severe chest pain"})
        assert safety.status_code == 401
        assert client.post(
            "/api/v1/workflows",
            json={"kind": "symptom_questionnaire", "idempotency_key": "start-key"},
        ).status_code == 401


def test_api_emergency_precedence_and_controlled_questionnaire() -> None:
    with TestClient(make_app()) as client:
        headers = register_and_login(client, "workflow@example.com")
        emergency = client.post(
            "/api/v1/answers",
            json={"question": "Someone is unresponsive and cannot breathe"},
            headers=headers,
        )
        assert emergency.status_code == 200
        assert emergency.json()["status"] == "escalated"
        assert emergency.json()["usage"]["attempts"] == 0
        assert emergency.json()["evidence"] == []

        started = client.post(
            "/api/v1/workflows",
            json={"kind": "symptom_questionnaire", "idempotency_key": "api-start-key"},
            headers=headers,
        )
        assert started.status_code == 201
        workflow_id = started.json()["id"]
        begin = client.post(
            f"/api/v1/workflows/{workflow_id}/transitions",
            json={"action": "begin", "idempotency_key": "api-begin-key"},
            headers=headers,
        )
        assert begin.json()["state"] == "collecting"
        review = client.post(
            f"/api/v1/workflows/{workflow_id}/transitions",
            json={
                "action": "submit",
                "idempotency_key": "api-submit-key",
                "payload": {"concern": "fever", "duration": "days", "severity": "mild"},
            },
            headers=headers,
        )
        assert review.json()["state"] == "review"
        assert review.json()["summary"] == [
            "concern:fever",
            "duration:days",
            "severity:mild",
        ]
