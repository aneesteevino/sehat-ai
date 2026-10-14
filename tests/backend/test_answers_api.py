from pathlib import Path

from fastapi.testclient import TestClient
from sehat_api.config import Settings
from sehat_api.main import create_app

ROOT = Path(__file__).resolve().parents[2]


def authenticated_client() -> tuple[TestClient, dict[str, str]]:
    client = TestClient(
        create_app(
            Settings(
                app_env="test",
                auth_secret="test-secret-that-is-long-enough-32-bytes",
                knowledge_registry_path=ROOT / "data/source_registry/sources.json",
                _env_file=None,
            )
        )
    )
    client.__enter__()
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "answer-reader@example.com",
            "display_name": "Answer Reader",
            "password": "long-test-password",
        },
    )
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "answer-reader@example.com", "password": "long-test-password"},
    )
    return client, {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_answer_route_requires_authentication() -> None:
    app = create_app(
        Settings(
            app_env="test",
            auth_secret="test-secret-that-is-long-enough-32-bytes",
            knowledge_registry_path=ROOT / "data/source_registry/sources.json",
            _env_file=None,
        )
    )
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/answers",
            json={"question": "How long should hands be scrubbed with soap?"},
        )
    assert response.status_code == 401


def test_answer_route_retrieves_then_returns_grounded_claims() -> None:
    client, headers = authenticated_client()
    try:
        response = client.post(
            "/api/v1/answers",
            json={"question": "How long should hands be scrubbed with soap?"},
            headers=headers,
        )
    finally:
        client.__exit__(None, None, None)

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "answered"
    evidence_ids = {item["chunk_id"] for item in payload["evidence"]}
    assert set(payload["claims"][0]["evidence_ids"]) <= evidence_ids
    assert payload["usage"]["provider"] == "mock"
    assert payload["usage"]["estimated_cost_usd"] == 0
    assert "diagnosis" in payload["safety_notice"]


def test_answer_route_abstains_when_approved_evidence_is_missing() -> None:
    client, headers = authenticated_client()
    try:
        response = client.post(
            "/api/v1/answers",
            json={"question": "What is the orbital period of a distant exoplanet?"},
            headers=headers,
        )
    finally:
        client.__exit__(None, None, None)

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "abstained"
    assert payload["claims"] == []
    assert payload["abstention_reason"] == "insufficient_evidence"
    assert payload["usage"]["attempts"] == 0
