import pytest

from app.models.person import Person
from app.models.relationship import Relationship, RelationshipType
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
        email="tree-viewer@example.com",
        role=UserRole.VIEWER,
    )


@pytest.fixture
def authenticated_moderator_client(client, user_factory):
    return _login(
        client,
        user_factory,
        email="tree-moderator@example.com",
        role=UserRole.MODERATOR,
    )


def _person(db_session, full_name: str) -> Person:
    person = Person(full_name=full_name)
    db_session.add(person)
    db_session.commit()
    db_session.refresh(person)
    return person


def test_tree_requires_authenticated_user(client):
    response = client.get("/api/v1/tree")

    assert response.status_code == 401


def test_tree_returns_viewer_role_people_and_relationships(
    authenticated_viewer_client,
    db_session,
):
    parent = _person(db_session, "Tree Parent")
    child = _person(db_session, "Tree Child")
    relationship = Relationship(
        relationship_type=RelationshipType.PARENT_CHILD,
        source_person_id=parent.id,
        target_person_id=child.id,
    )
    db_session.add(relationship)
    db_session.commit()

    response = authenticated_viewer_client.get("/api/v1/tree")

    assert response.status_code == 200
    assert response.json() == {
        "viewerRole": "viewer",
        "people": [
            {
                "id": parent.id,
                "fullName": "Tree Parent",
                "birthDate": None,
                "deathDate": None,
                "notes": None,
            },
            {
                "id": child.id,
                "fullName": "Tree Child",
                "birthDate": None,
                "deathDate": None,
                "notes": None,
            },
        ],
        "relationships": [
            {
                "id": relationship.id,
                "type": "parent_child",
                "sourcePersonId": parent.id,
                "targetPersonId": child.id,
            },
        ],
    }


def test_deleting_a_relationship_removes_it_from_tree_payload(
    authenticated_moderator_client,
    db_session,
):
    parent = _person(db_session, "Deleted Parent")
    child = _person(db_session, "Deleted Child")
    relationship = Relationship(
        relationship_type=RelationshipType.PARENT_CHILD,
        source_person_id=parent.id,
        target_person_id=child.id,
    )
    db_session.add(relationship)
    db_session.commit()

    delete_response = authenticated_moderator_client.delete(
        f"/api/v1/relationships/{relationship.id}",
    )
    tree_response = authenticated_moderator_client.get("/api/v1/tree")

    assert delete_response.status_code == 204
    assert tree_response.status_code == 200
    assert tree_response.json()["relationships"] == []
