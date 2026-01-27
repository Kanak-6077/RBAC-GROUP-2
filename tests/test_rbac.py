from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_login_success():
    response = client.post(
        "/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure():
    response = client.post(
        "/login",
        json={"username": "admin", "password": "wrongpass"}
    )
    assert response.status_code == 401


def test_access_without_token():
    response = client.get("/users")
    assert response.status_code == 401


from jose import jwt
from datetime import datetime, timedelta, timezone

def test_expired_token_access():
    expired_payload = {
        "sub": "admin",
        "role": "C-Level",
        "department": "General",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=5)
    }

    token = jwt.encode(
        expired_payload,
        "ce3mc4ejwrn4vi534932c42394",
        algorithm="HS256"
    )

    response = client.get(
        "/users",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401
