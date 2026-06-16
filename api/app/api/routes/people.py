from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User, UserRole
from app.schemas.person import PersonCreate, PersonRead, PersonUpdate
from app.services.person_service import (
    create_person,
    get_person,
    list_people,
    update_person,
)


router = APIRouter(prefix="/people", tags=["people"])


def require_person_write_role(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.role not in {UserRole.OWNER, UserRole.MODERATOR}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    return current_user


@router.get("", response_model=list[PersonRead])
def read_people(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[PersonRead]:
    return list_people(db)


@router.get("/{person_id}", response_model=PersonRead)
def read_person(
    person_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> PersonRead:
    person = get_person(db, person_id)
    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found",
        )

    return person


@router.post("", response_model=PersonRead, status_code=status.HTTP_201_CREATED)
def create_person_route(
    person_create: PersonCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_person_write_role)],
) -> PersonRead:
    return create_person(db, person_create)


@router.patch("/{person_id}", response_model=PersonRead)
def update_person_route(
    person_id: int,
    person_update: PersonUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_person_write_role)],
) -> PersonRead:
    person = get_person(db, person_id)
    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found",
        )

    return update_person(db, person, person_update)
