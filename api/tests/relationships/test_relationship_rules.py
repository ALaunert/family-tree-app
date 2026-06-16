import pytest
from sqlalchemy.exc import IntegrityError

from app.models.person import Person
from app.models.relationship import Relationship, RelationshipType
from app.models.user import UserRole
from app.services import relationship_service


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
        email="relationship-viewer@example.com",
        role=UserRole.VIEWER,
    )


@pytest.fixture
def authenticated_moderator_client(client, user_factory):
    return _login(
        client,
        user_factory,
        email="relationship-moderator@example.com",
        role=UserRole.MODERATOR,
    )


@pytest.fixture
def authenticated_owner_client(client, user_factory):
    return _login(
        client,
        user_factory,
        email="relationship-owner@example.com",
        role=UserRole.OWNER,
    )


def _person(db_session, full_name: str) -> Person:
    person = Person(full_name=full_name)
    db_session.add(person)
    db_session.commit()
    db_session.refresh(person)
    return person


def _create_relationship(client, *, relationship_type, source_id, target_id):
    return client.post(
        "/api/v1/relationships",
        json={
            "relationshipType": relationship_type,
            "sourcePersonId": source_id,
            "targetPersonId": target_id,
        },
    )


def test_partner_relationship_is_canonicalized(
    authenticated_moderator_client,
    db_session,
):
    first = _person(db_session, "First Partner")
    second = _person(db_session, "Second Partner")

    response = _create_relationship(
        authenticated_moderator_client,
        relationship_type="partner",
        source_id=second.id,
        target_id=first.id,
    )

    assert response.status_code == 201
    assert response.json()["sourcePersonId"] == first.id
    assert response.json()["targetPersonId"] == second.id

    duplicate_response = _create_relationship(
        authenticated_moderator_client,
        relationship_type="partner",
        source_id=first.id,
        target_id=second.id,
    )

    assert duplicate_response.status_code == 409


def test_child_cannot_receive_more_than_two_parents(
    authenticated_moderator_client,
    db_session,
):
    first_parent = _person(db_session, "First Parent")
    second_parent = _person(db_session, "Second Parent")
    third_parent = _person(db_session, "Third Parent")
    child = _person(db_session, "Child")

    for parent in (first_parent, second_parent):
        response = _create_relationship(
            authenticated_moderator_client,
            relationship_type="parent_child",
            source_id=parent.id,
            target_id=child.id,
        )
        assert response.status_code == 201

    response = _create_relationship(
        authenticated_moderator_client,
        relationship_type="parent_child",
        source_id=third_parent.id,
        target_id=child.id,
    )

    assert response.status_code == 409


def test_parent_child_relationship_rejects_cycles(
    authenticated_moderator_client,
    db_session,
):
    grandparent = _person(db_session, "Grandparent")
    parent = _person(db_session, "Parent")
    child = _person(db_session, "Child")

    for source, target in ((grandparent, parent), (parent, child)):
        response = _create_relationship(
            authenticated_moderator_client,
            relationship_type="parent_child",
            source_id=source.id,
            target_id=target.id,
        )
        assert response.status_code == 201

    response = _create_relationship(
        authenticated_moderator_client,
        relationship_type="parent_child",
        source_id=child.id,
        target_id=grandparent.id,
    )

    assert response.status_code == 409


def test_viewer_cannot_create_relationships(
    authenticated_viewer_client,
    db_session,
):
    parent = _person(db_session, "Viewer Parent")
    child = _person(db_session, "Viewer Child")

    response = _create_relationship(
        authenticated_viewer_client,
        relationship_type="parent_child",
        source_id=parent.id,
        target_id=child.id,
    )

    assert response.status_code == 403


def test_unauthenticated_user_cannot_create_relationships(client, db_session):
    parent = _person(db_session, "Anonymous Parent")
    child = _person(db_session, "Anonymous Child")

    response = _create_relationship(
        client,
        relationship_type="parent_child",
        source_id=parent.id,
        target_id=child.id,
    )

    assert response.status_code == 401


def test_viewer_cannot_delete_relationships(
    authenticated_viewer_client,
    db_session,
):
    parent = _person(db_session, "Viewer Delete Parent")
    child = _person(db_session, "Viewer Delete Child")
    relationship = Relationship(
        relationship_type=RelationshipType.PARENT_CHILD,
        source_person_id=parent.id,
        target_person_id=child.id,
    )
    db_session.add(relationship)
    db_session.commit()

    response = authenticated_viewer_client.delete(
        f"/api/v1/relationships/{relationship.id}",
    )

    assert response.status_code == 403


def test_missing_person_relationship_is_rejected(
    authenticated_moderator_client,
    db_session,
):
    parent = _person(db_session, "Known Parent")

    response = _create_relationship(
        authenticated_moderator_client,
        relationship_type="parent_child",
        source_id=parent.id,
        target_id=999999,
    )

    assert response.status_code == 404


def test_self_relationship_is_rejected(authenticated_moderator_client, db_session):
    person = _person(db_session, "Self Linked")

    response = _create_relationship(
        authenticated_moderator_client,
        relationship_type="parent_child",
        source_id=person.id,
        target_id=person.id,
    )

    assert response.status_code == 409


def test_integrity_error_is_mapped_to_conflict(
    authenticated_moderator_client,
    db_session,
    monkeypatch,
):
    parent = _person(db_session, "Race Parent")
    child = _person(db_session, "Race Child")

    def raise_integrity_error(db_session):
        raise IntegrityError(
            statement="INSERT INTO relationships ...",
            params={},
            orig=Exception("duplicate key"),
        )

    monkeypatch.setattr(
        relationship_service,
        "_commit_relationship",
        raise_integrity_error,
    )

    response = _create_relationship(
        authenticated_moderator_client,
        relationship_type="parent_child",
        source_id=parent.id,
        target_id=child.id,
    )

    assert response.status_code == 409


def test_owner_can_delete_relationship(
    authenticated_owner_client,
    db_session,
):
    parent = _person(db_session, "Owner Parent")
    child = _person(db_session, "Owner Child")
    relationship = Relationship(
        relationship_type=RelationshipType.PARENT_CHILD,
        source_person_id=parent.id,
        target_person_id=child.id,
    )
    db_session.add(relationship)
    db_session.commit()
    relationship_id = relationship.id

    response = authenticated_owner_client.delete(
        f"/api/v1/relationships/{relationship_id}",
    )

    assert response.status_code == 204
    db_session.expire_all()
    assert db_session.get(Relationship, relationship_id) is None
