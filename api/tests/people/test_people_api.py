from datetime import date

import pytest

from app.models.person import Person
from app.models.user import UserRole


def _login(client, user_factory, *, email: str, role: UserRole):
    user = user_factory(email=email, role=role)
    response = client.post(
        "/api/v1/auth/login",
        json={"email": user.email, "password": "secret-password"},
    )
    assert response.status_code == 200
    return client


@pytest.fixture
def authenticated_viewer_client(client, user_factory):
    return _login(
        client,
        user_factory,
        email="viewer@example.com",
        role=UserRole.VIEWER,
    )


@pytest.fixture
def authenticated_moderator_client(client, user_factory):
    return _login(
        client,
        user_factory,
        email="moderator@example.com",
        role=UserRole.MODERATOR,
    )


@pytest.fixture
def authenticated_owner_client(client, user_factory):
    return _login(
        client,
        user_factory,
        email="owner@example.com",
        role=UserRole.OWNER,
    )


def test_viewer_can_list_people(authenticated_viewer_client, db_session):
    first = Person(full_name="Ada Lovelace", birth_date=date(1815, 12, 10))
    second = Person(full_name="Grace Hopper", death_date=date(1992, 1, 1))
    db_session.add_all([first, second])
    db_session.commit()

    response = authenticated_viewer_client.get("/api/v1/people")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": first.id,
            "fullName": "Ada Lovelace",
            "birthDate": "1815-12-10",
            "deathDate": None,
            "notes": None,
        },
        {
            "id": second.id,
            "fullName": "Grace Hopper",
            "birthDate": None,
            "deathDate": "1992-01-01",
            "notes": None,
        },
    ]


def test_viewer_can_get_person(authenticated_viewer_client, db_session):
    person = Person(full_name="Katherine Johnson", notes="Mathematician")
    db_session.add(person)
    db_session.commit()

    response = authenticated_viewer_client.get(f"/api/v1/people/{person.id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": person.id,
        "fullName": "Katherine Johnson",
        "birthDate": None,
        "deathDate": None,
        "notes": "Mathematician",
    }


def test_viewer_cannot_create_people(authenticated_viewer_client):
    response = authenticated_viewer_client.post(
        "/api/v1/people",
        json={"fullName": "New Person"},
    )

    assert response.status_code == 403


def test_unauthenticated_user_cannot_list_people(client):
    response = client.get("/api/v1/people")

    assert response.status_code == 401


def test_viewer_cannot_update_people(authenticated_viewer_client, db_session):
    person = Person(full_name="Read Only")
    db_session.add(person)
    db_session.commit()

    response = authenticated_viewer_client.patch(
        f"/api/v1/people/{person.id}",
        json={"fullName": "Changed"},
    )

    assert response.status_code == 403


def test_moderator_can_create_people(authenticated_moderator_client):
    response = authenticated_moderator_client.post(
        "/api/v1/people",
        json={
            "fullName": "New Person",
            "birthDate": "1980-05-01",
            "notes": "Added by moderator",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": response.json()["id"],
        "fullName": "New Person",
        "birthDate": "1980-05-01",
        "deathDate": None,
        "notes": "Added by moderator",
    }


def test_owner_can_create_people(authenticated_owner_client):
    response = authenticated_owner_client.post(
        "/api/v1/people",
        json={"fullName": "Owner Created"},
    )

    assert response.status_code == 201
    assert response.json()["fullName"] == "Owner Created"


def test_owner_can_update_people(authenticated_owner_client, db_session):
    person = Person(full_name="Owner Editable")
    db_session.add(person)
    db_session.commit()

    response = authenticated_owner_client.patch(
        f"/api/v1/people/{person.id}",
        json={"notes": "Owner update"},
    )

    assert response.status_code == 200
    assert response.json()["notes"] == "Owner update"


def test_moderator_can_update_people(authenticated_moderator_client, db_session):
    person = Person(full_name="Original Name", birth_date=date(1970, 1, 1))
    db_session.add(person)
    db_session.commit()

    response = authenticated_moderator_client.patch(
        f"/api/v1/people/{person.id}",
        json={
            "fullName": "Updated Name",
            "deathDate": "2020-12-31",
            "notes": "Updated by moderator",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": person.id,
        "fullName": "Updated Name",
        "birthDate": "1970-01-01",
        "deathDate": "2020-12-31",
        "notes": "Updated by moderator",
    }


def test_blank_full_name_is_rejected(authenticated_moderator_client):
    response = authenticated_moderator_client.post(
        "/api/v1/people",
        json={"fullName": "   "},
    )

    assert response.status_code == 422


def test_null_full_name_update_is_rejected(
    authenticated_moderator_client,
    db_session,
):
    person = Person(full_name="Existing Person")
    db_session.add(person)
    db_session.commit()

    response = authenticated_moderator_client.patch(
        f"/api/v1/people/{person.id}",
        json={"fullName": None},
    )

    assert response.status_code == 422


def test_full_name_too_long_is_rejected(authenticated_moderator_client):
    response = authenticated_moderator_client.post(
        "/api/v1/people",
        json={"fullName": "A" * 201},
    )

    assert response.status_code == 422
