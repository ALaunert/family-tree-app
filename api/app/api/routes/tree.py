from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.tree import TreeRead
from app.services.tree_service import get_tree


router = APIRouter(prefix="/tree", tags=["tree"])


@router.get("", response_model=TreeRead)
def read_tree(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> TreeRead:
    return get_tree(db, current_user.role)
