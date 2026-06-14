from sqlalchemy.orm import Session

from app.models.user import UserRole
from app.schemas.tree import TreeRead
from app.services.person_service import list_people
from app.services.relationship_service import list_relationships


def get_tree(db: Session, viewer_role: UserRole) -> TreeRead:
    return TreeRead(
        viewerRole=viewer_role,
        people=list_people(db),
        relationships=list_relationships(db),
    )
