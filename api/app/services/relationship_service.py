from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.person import Person
from app.models.relationship import Relationship, RelationshipType
from app.schemas.relationship import RelationshipCreate


class RelationshipRuleError(ValueError):
    pass


def get_relationship(db: Session, relationship_id: int) -> Relationship | None:
    return db.get(Relationship, relationship_id)


def list_relationships(db: Session) -> list[Relationship]:
    return list(db.scalars(select(Relationship).order_by(Relationship.id)).all())


def create_relationship(
    db: Session,
    relationship_create: RelationshipCreate,
) -> Relationship:
    relationship_type = relationship_create.relationship_type
    source_person_id = relationship_create.source_person_id
    target_person_id = relationship_create.target_person_id

    if relationship_type == RelationshipType.PARTNER:
        source_person_id, target_person_id = sorted(
            (source_person_id, target_person_id),
        )

    if (
        db.get(Person, source_person_id) is None
        or db.get(Person, target_person_id) is None
    ):
        raise LookupError("Person not found")

    if source_person_id == target_person_id:
        raise RelationshipRuleError("Relationship cannot link a person to themselves")

    if _relationship_exists(db, relationship_type, source_person_id, target_person_id):
        raise RelationshipRuleError("Relationship already exists")

    if relationship_type == RelationshipType.PARENT_CHILD:
        if _parent_count(db, target_person_id) >= 2:
            raise RelationshipRuleError("Child already has two parents")
        if _would_create_cycle(db, source_person_id, target_person_id):
            raise RelationshipRuleError("Parent-child relationship would create a cycle")

    relationship = Relationship(
        relationship_type=relationship_type,
        source_person_id=source_person_id,
        target_person_id=target_person_id,
    )
    db.add(relationship)
    db.commit()
    db.refresh(relationship)
    return relationship


def delete_relationship(db: Session, relationship: Relationship) -> None:
    db.delete(relationship)
    db.commit()


def _relationship_exists(
    db: Session,
    relationship_type: RelationshipType,
    source_person_id: int,
    target_person_id: int,
) -> bool:
    return (
        db.scalar(
            select(Relationship.id).where(
                Relationship.relationship_type == relationship_type,
                Relationship.source_person_id == source_person_id,
                Relationship.target_person_id == target_person_id,
            )
        )
        is not None
    )


def _parent_count(db: Session, child_id: int) -> int:
    return db.scalar(
        select(func.count()).select_from(Relationship).where(
            Relationship.relationship_type == RelationshipType.PARENT_CHILD,
            Relationship.target_person_id == child_id,
        )
    )


def _would_create_cycle(db: Session, source_person_id: int, target_person_id: int) -> bool:
    children_by_parent: dict[int, list[int]] = {}
    rows = db.execute(
        select(Relationship.source_person_id, Relationship.target_person_id).where(
            Relationship.relationship_type == RelationshipType.PARENT_CHILD,
        )
    )
    for parent_id, child_id in rows:
        children_by_parent.setdefault(parent_id, []).append(child_id)

    stack = [target_person_id]
    visited: set[int] = set()

    while stack:
        person_id = stack.pop()
        if person_id == source_person_id:
            return True
        if person_id in visited:
            continue

        visited.add(person_id)
        stack.extend(children_by_parent.get(person_id, []))

    return False
