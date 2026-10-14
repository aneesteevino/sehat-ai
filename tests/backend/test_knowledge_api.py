from pathlib import Path

from fastapi.testclient import TestClient
from sehat_api.config import Settings
from sehat_api.main import create_app

ROOT = Path(__file__).resolve().parents[2]


def test_authenticated_search_returns_evidence_not_a_medical_answer() -> None:
    app = create_app(
        Settings(
            app_env="test",
            auth_secret="test-secret-that-is-long-enough-32-bytes",
            knowledge_registry_path=ROOT / "data/source_registry/sources.json",
            _env_file=None,
        )
    )
    with TestClient(app) as client:
        assert client.post(
            "/api/v1/knowledge/search",
            json={"query": "handwashing"},
        ).status_code == 401
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "reader@example.com",
                "display_name": "Reader",
                "password": "long-test-password",
            },
        )
        login = client.post(
            "/api/v1/auth/login",
            json={"email": "reader@example.com", "password": "long-test-password"},
        )
        token = login.json()["access_token"]
        response = client.post(
            "/api/v1/knowledge/search",
            json={"query": "How long should hands be scrubbed?", "limit": 2},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["generated_answer"] is None
    assert payload["evidence"][0]["citation"]["source_id"] == "cdc-handwashing-faq"
    assert payload["evidence"][0]["content_trust"] == "untrusted"
