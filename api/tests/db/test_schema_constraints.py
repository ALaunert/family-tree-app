import pytest
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from app.db.session import SessionLocal
from app.models.auth_session import AuthSession
from app.models.person import Person
from app.models.relationship import Relationship, RelationshipType
from app.models.user import User, UserRole


@pytest.fixture
def db_session():
    with SessionLocal() as session:
        for model in (Relationship, AuthSession, Person, User):
            session.execute(delete(model))
        session.commit()

        yield session

        session.rollback()
        for model in (Relationship, AuthSession, Person, User):
            session.execute(delete(model))
        session.commit()


def test_users_email_is_unique(db_session):
    db_session.add(
        User(
            email="viewer@example.com",
            display_name="First Viewer",
            role=UserRole.VIEWER,
        )
    )
    db_session.commit()

    db_session.add(
        User(
            email="viewer@example.com",
            display_name="Second Viewer",
            role=UserRole.VIEWER,
        )
    )

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_relationships_reject_self_links(db_session):
    person = Person(full_name="Self Linked Person")
    db_session.add(person)
    db_session.commit()

    db_session.add(
        Relationship(
            relationship_type=RelationshipType.PARENT_CHILD,
            source_person_id=person.id,
            target_person_id=person.id,
        )
    )

    with pytest.raises(IntegrityError):
        db_session.commit()
