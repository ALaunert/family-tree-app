from datetime import date, datetime

from sqlalchemy import Date, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Person(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    death_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
