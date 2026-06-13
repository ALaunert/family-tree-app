"""initial schema

Revision ID: 20260321_0001
Revises:
Create Date: 2026-03-21 00:01:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260321_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("display_name", sa.String(length=200), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_table(
        "people",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=200), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("death_date", sa.Date(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "auth_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token_hash", sa.String(length=128), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_hash"),
    )
    op.create_table(
        "relationships",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("relationship_type", sa.String(length=32), nullable=False),
        sa.Column("source_person_id", sa.Integer(), nullable=False),
        sa.Column("target_person_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "source_person_id <> target_person_id",
            name="ck_relationship_not_self",
        ),
        sa.ForeignKeyConstraint(["source_person_id"], ["people.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["target_person_id"], ["people.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "relationship_type",
            "source_person_id",
            "target_person_id",
            name="uq_relationship_pair",
        ),
    )


def downgrade() -> None:
    op.drop_table("relationships")
    op.drop_table("auth_sessions")
    op.drop_table("people")
    op.drop_table("users")
