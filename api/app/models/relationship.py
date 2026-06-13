import enum
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class RelationshipType(str, enum.Enum):
    PARENT_CHILD = "parent_child"
    PARTNER = "partner"


relationship_type_type = Enum(
    RelationshipType,
    values_callable=lambda types: [type_.value for type_ in types],
    native_enum=False,
    length=32,
)


class Relationship(Base):
    __tablename__ = "relationships"
    __table_args__ = (
        CheckConstraint(
            "source_person_id <> target_person_id",
            name="ck_relationship_not_self",
        ),
        UniqueConstraint(
            "relationship_type",
            "source_person_id",
            "target_person_id",
            name="uq_relationship_pair",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    relationship_type: Mapped[RelationshipType] = mapped_column(
        relationship_type_type,
        nullable=False,
    )
    source_person_id: Mapped[int] = mapped_column(
        ForeignKey("people.id", ondelete="CASCADE"),
        nullable=False,
    )
    target_person_id: Mapped[int] = mapped_column(
        ForeignKey("people.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    source_person: Mapped["Person"] = relationship(foreign_keys=[source_person_id])
    target_person: Mapped["Person"] = relationship(foreign_keys=[target_person_id])
