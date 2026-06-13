import pytest
from sqlalchemy import delete, inspect, text
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
            password_hash="hashed-password-1",
            role=UserRole.VIEWER,
        )
    )
    db_session.commit()

    db_session.add(
        User(
            email="viewer@example.com",
            password_hash="hashed-password-2",
            role=UserRole.VIEWER,
        )
    )

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_users_require_password_hash_and_do_not_require_display_name(db_session):
    db_session.add(
        User(
            email="viewer@example.com",
            password_hash="hashed-password",
            role=UserRole.VIEWER,
        )
    )
    db_session.commit()

    with pytest.raises(IntegrityError):
        db_session.execute(
            text(
                "INSERT INTO users (email, role) "
                "VALUES ('missing-password@example.com', 'viewer')"
            )
        )
        db_session.commit()


def test_users_role_is_constrained_to_known_values(db_session):
    with pytest.raises(IntegrityError):
        db_session.execute(
            text(
                "INSERT INTO users (email, password_hash, role) "
                "VALUES ('bad-role@example.com', 'hashed-password', 'admin')"
            )
        )
        db_session.commit()


def test_relationship_type_is_constrained_to_known_values(db_session):
    source = Person(full_name="Source Person")
    target = Person(full_name="Target Person")
    db_session.add_all([source, target])
    db_session.commit()

    with pytest.raises(IntegrityError):
        db_session.execute(
            text(
                "INSERT INTO relationships "
                "(relationship_type, source_person_id, target_person_id) "
                "VALUES ('sibling', :source_person_id, :target_person_id)"
            ),
            {"source_person_id": source.id, "target_person_id": target.id},
        )
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


def test_relationships_reject_duplicate_pairs(db_session):
    source = Person(full_name="Source Person")
    target = Person(full_name="Target Person")
    db_session.add_all([source, target])
    db_session.commit()

    db_session.add(
        Relationship(
            relationship_type=RelationshipType.PARENT_CHILD,
            source_person_id=source.id,
            target_person_id=target.id,
        )
    )
    db_session.commit()

    db_session.add(
        Relationship(
            relationship_type=RelationshipType.PARENT_CHILD,
            source_person_id=source.id,
            target_person_id=target.id,
        )
    )

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_schema_has_consistent_timestamps(db_session):
    inspector = inspect(db_session.bind)

    for table_name in ("users", "auth_sessions", "people", "relationships"):
        column_names = {column["name"] for column in inspector.get_columns(table_name)}

        assert {"created_at", "updated_at"} <= column_names

    user_column_names = {column["name"] for column in inspector.get_columns("users")}

    assert "password_hash" in user_column_names
    assert "display_name" not in user_column_names
