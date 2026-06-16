from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User, UserRole
from app.schemas.relationship import RelationshipCreate, RelationshipRead
from app.services.relationship_service import (
    RelationshipRuleError,
    create_relationship,
    delete_relationship,
    get_relationship,
)


router = APIRouter(prefix="/relationships", tags=["relationships"])


def require_relationship_write_role(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.role not in {UserRole.OWNER, UserRole.MODERATOR}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    return current_user


@router.post("", response_model=RelationshipRead, status_code=status.HTTP_201_CREATED)
def create_relationship_route(
    relationship_create: RelationshipCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_relationship_write_role)],
) -> RelationshipRead:
    try:
        return create_relationship(db, relationship_create)
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except RelationshipRuleError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.delete("/{relationship_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_relationship_route(
    relationship_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_relationship_write_role)],
) -> Response:
    relationship = get_relationship(db, relationship_id)
    if relationship is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relationship not found",
        )

    delete_relationship(db, relationship)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
