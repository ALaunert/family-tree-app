from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_session_token,
    hash_password,
    hash_session_token,
    verify_password,
)
from app.models.auth_session import AuthSession
from app.models.user import User, UserRole


SESSION_COOKIE_NAME = "family_tree_session"
SESSION_COOKIE_MAX_AGE = settings.session_ttl_hours * 60 * 60


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.scalar(select(User).where(User.email == email))
    if user is None or not verify_password(password, user.password_hash):
        return None

    return user


def create_auth_session(db: Session, user: User) -> str:
    token = create_session_token()
    session = AuthSession(
        user_id=user.id,
        token_hash=hash_session_token(token),
        expires_at=datetime.now(timezone.utc)
        + timedelta(hours=settings.session_ttl_hours),
    )
    db.add(session)
    db.commit()
    return token


def get_user_by_session_token(db: Session, token: str) -> User | None:
    auth_session = db.scalar(
        select(AuthSession).where(AuthSession.token_hash == hash_session_token(token))
    )
    if auth_session is None:
        return None

    if auth_session.expires_at <= datetime.now(timezone.utc):
        db.delete(auth_session)
        db.commit()
        return None

    return db.get(User, auth_session.user_id)


def delete_auth_session(db: Session, token: str) -> None:
    auth_session = db.scalar(
        select(AuthSession).where(AuthSession.token_hash == hash_session_token(token))
    )
    if auth_session is None:
        return

    db.delete(auth_session)
    db.commit()


def create_user(db: Session, email: str, password: str, role: UserRole) -> User:
    user = User(email=email, password_hash=hash_password(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_or_create_owner(db: Session, email: str, password: str) -> User:
    user = db.scalar(select(User).where(User.email == email))
    if user is not None:
        user.role = UserRole.OWNER
        user.password_hash = hash_password(password)
        db.execute(delete(AuthSession).where(AuthSession.user_id == user.id))
        db.commit()
        db.refresh(user)
        return user

    return create_user(db, email=email, password=password, role=UserRole.OWNER)
