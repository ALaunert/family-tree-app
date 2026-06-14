from sqlalchemy import select

from app.models.auth_session import AuthSession


def test_login_sets_session_cookie(client, user_factory):
    user = user_factory(email="viewer@example.com")

    response = client.post(
        "/api/v1/auth/login",
        json={"email": user.email, "password": "secret-password"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "user": {"id": user.id, "email": user.email, "role": "viewer"}
    }
    assert response.cookies.get("family_tree_session")


def test_me_requires_authentication(client):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_me_returns_current_user_when_authenticated(client, user_factory):
    user = user_factory(email="owner@example.com", role="owner")
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": user.email, "password": "secret-password"},
    )

    response = client.get("/api/v1/auth/me")

    assert login_response.status_code == 200
    assert response.status_code == 200
    assert response.json() == {
        "user": {"id": user.id, "email": user.email, "role": "owner"}
    }


def test_logout_clears_cookie_and_deletes_server_session(
    client, user_factory, db_session
):
    user = user_factory(email="viewer@example.com")
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": user.email, "password": "secret-password"},
    )
    assert login_response.status_code == 200
    assert db_session.scalar(select(AuthSession)) is not None

    response = client.post("/api/v1/auth/logout")

    assert response.status_code == 204
    assert response.cookies.get("family_tree_session") is None
    assert "Max-Age=0" in response.headers["set-cookie"]
    assert db_session.scalar(select(AuthSession)) is None
