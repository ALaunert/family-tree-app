from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.schemas.auth import AuthUserResponse, LoginRequest, UserRead
from app.services.auth_service import (
    SESSION_COOKIE_MAX_AGE,
    SESSION_COOKIE_NAME,
    authenticate_user,
    create_auth_session,
    delete_auth_session,
)
from app.models.user import User


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AuthUserResponse)
def login(
    login_request: LoginRequest,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
) -> AuthUserResponse:
    user = authenticate_user(db, login_request.email, login_request.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_auth_session(db, user)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        max_age=SESSION_COOKIE_MAX_AGE,
        path="/",
    )
    return AuthUserResponse(user=UserRead(id=user.id, email=user.email, role=user.role))


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    db: Annotated[Session, Depends(get_db)],
    family_tree_session: Annotated[str | None, Cookie()] = None,
) -> Response:
    if family_tree_session is not None:
        delete_auth_session(db, family_tree_session)

    response.status_code = status.HTTP_204_NO_CONTENT
    response.delete_cookie(SESSION_COOKIE_NAME, path="/")
    return response


@router.get("/me", response_model=AuthUserResponse)
def me(current_user: Annotated[User, Depends(get_current_user)]) -> AuthUserResponse:
    return AuthUserResponse(
        user=UserRead(
            id=current_user.id,
            email=current_user.email,
            role=current_user.role,
        )
    )
