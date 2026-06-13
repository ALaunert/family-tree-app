import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class UserRole(str, enum.Enum):
    OWNER = "owner"
    MODERATOR = "moderator"
    VIEWER = "viewer"


user_role_type = Enum(
    UserRole,
    values_callable=lambda roles: [role.value for role in roles],
    native_enum=False,
    length=32,
)


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    display_name: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[UserRole] = mapped_column(user_role_type, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    auth_sessions: Mapped[list["AuthSession"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
