from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.person import Person
from app.schemas.person import PersonCreate, PersonUpdate


def list_people(db: Session) -> list[Person]:
    return list(db.scalars(select(Person).order_by(Person.id)).all())


def get_person(db: Session, person_id: int) -> Person | None:
    return db.get(Person, person_id)


def create_person(db: Session, person_create: PersonCreate) -> Person:
    person = Person(**person_create.model_dump())
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


def update_person(
    db: Session,
    person: Person,
    person_update: PersonUpdate,
) -> Person:
    for field, value in person_update.model_dump(exclude_unset=True).items():
        setattr(person, field, value)

    db.commit()
    db.refresh(person)
    return person
