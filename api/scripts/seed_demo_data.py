from datetime import date
import os

from sqlalchemy import select, text

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.person import Person
from app.models.relationship import Relationship, RelationshipType
from app.models.user import User, UserRole


DEMO_USERS = [
    ("viewer@example.com", "viewer-password", UserRole.VIEWER),
    ("moderator@example.com", "moderator-password", UserRole.MODERATOR),
]


def upsert_user(db, email: str, password: str, role: UserRole) -> User:
    user = db.scalar(select(User).where(User.email == email))
    if user is None:
        user = User(email=email, role=role, password_hash=hash_password(password))
        db.add(user)
    else:
        user.role = role
        user.password_hash = hash_password(password)
    return user


def upsert_person(
    db,
    *,
    full_name: str,
    birth_date: date | None = None,
    notes: str | None = None,
) -> Person:
    person = db.scalar(select(Person).where(Person.full_name == full_name))
    if person is None:
        person = Person(full_name=full_name)
        db.add(person)

    person.birth_date = birth_date
    person.notes = notes
    return person


def ensure_relationship(
    db,
    *,
    relationship_type: RelationshipType,
    source_person: Person,
    target_person: Person,
) -> None:
    relationship = db.scalar(
        select(Relationship).where(
            Relationship.relationship_type == relationship_type,
            Relationship.source_person_id == source_person.id,
            Relationship.target_person_id == target_person.id,
        )
    )
    if relationship is None:
        db.add(
            Relationship(
                relationship_type=relationship_type,
                source_person_id=source_person.id,
                target_person_id=target_person.id,
            )
        )


def main() -> None:
    with SessionLocal() as db:
        if os.getenv("RESET_DEMO_DATA") == "true":
            db.execute(
                text(
                    "TRUNCATE relationships, people, auth_sessions, users "
                    "RESTART IDENTITY CASCADE"
                )
            )
            db.commit()

        for email, password, role in DEMO_USERS:
            upsert_user(db, email, password, role)

        ada = upsert_person(
            db,
            full_name="Ada Demo",
            birth_date=date(1815, 12, 10),
            notes="Seeded demo root person",
        )
        grace = upsert_person(
            db,
            full_name="Grace Demo",
            birth_date=date(1906, 12, 9),
            notes="Seeded demo child person",
        )
        db.commit()
        db.refresh(ada)
        db.refresh(grace)

        ensure_relationship(
            db,
            relationship_type=RelationshipType.PARENT_CHILD,
            source_person=ada,
            target_person=grace,
        )
        db.commit()

        print("Demo users and family tree data ready")


if __name__ == "__main__":
    main()
