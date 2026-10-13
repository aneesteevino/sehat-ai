from fastapi.testclient import TestClient
from sehat_api.config import Settings
from sehat_api.main import create_app


def make_client() -> TestClient:
    return TestClient(create_app(Settings(app_env="test", _env_file=None)))


def test_liveness_contract_and_generated_request_id() -> None:
    response = make_client().get("/health/live")

    assert response.status_code == 200
    assert response.headers["X-Request-ID"]
    assert response.json() == {
        "status": "ok",
        "service": "sehat-ai-api",
        "version": "0.1.0",
        "environment": "test",
        "checks": {
            "process": {"status": "ok", "detail": "API process is responsive"}
        },
    }


def test_valid_request_id_is_preserved() -> None:
    response = make_client().get("/health/ready", headers={"X-Request-ID": "test-request-42"})

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-request-42"
    assert response.json()["checks"]["database"]["status"] == "not_configured"


def test_unsafe_request_id_is_replaced() -> None:
    response = make_client().get("/health/live", headers={"X-Request-ID": "bad id\nvalue"})

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] != "bad id\nvalue"
    assert " " not in response.headers["X-Request-ID"]


def test_cors_allows_only_configured_frontend() -> None:
    client = make_client()
    response = client.options(
        "/health/live",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
