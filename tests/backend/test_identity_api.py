from fastapi.testclient import TestClient
from sehat_api.config import Settings
from sehat_api.main import create_app


def make_client() -> TestClient:
    return TestClient(
        create_app(
            Settings(
                app_env="test",
                auth_secret="test-secret-that-is-long-enough-32-bytes",
                _env_file=None,
            )
        )
    )


def test_registration_login_session_and_logout_flow() -> None:
    client = make_client()
    registration = client.post(
        "/api/v1/auth/register",
        json={
            "email": "person@example.com",
            "display_name": "Aneesa",
            "password": "long-test-password",
        },
    )
    assert registration.status_code == 201
    assert registration.json()["role"] == "patient"
    assert "password" not in registration.text

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "PERSON@example.com", "password": "long-test-password"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    assert login.json()["token_type"] == "bearer"

    authenticated = client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert authenticated.status_code == 200
    assert authenticated.json()["email"] == "person@example.com"

    logout = client.post(
        "/api/v1/auth/logout", headers={"Authorization": f"Bearer {token}"}
    )
    assert logout.status_code == 200
    assert client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
    ).status_code == 401


def test_self_registration_cannot_select_a_privileged_role() -> None:
    response = make_client().post(
        "/api/v1/auth/register",
        json={
            "email": "person@example.com",
            "display_name": "Aneesa",
            "password": "long-test-password",
            "role": "admin",
        },
    )
    assert response.status_code == 422


def test_login_error_does_not_reveal_account_existence() -> None:
    client = make_client()
    missing = client.post(
        "/api/v1/auth/login",
        json={"email": "missing@example.com", "password": "wrong-password"},
    )
    assert missing.status_code == 401
    assert missing.json()["detail"] == "The email or password is incorrect."


def test_registration_rejects_whitespace_only_display_name() -> None:
    response = make_client().post(
        "/api/v1/auth/register",
        json={
            "email": "person@example.com",
            "display_name": "   ",
            "password": "long-test-password",
        },
    )

    assert response.status_code == 422
