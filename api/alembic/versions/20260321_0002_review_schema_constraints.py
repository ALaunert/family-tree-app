"""review schema constraints

Revision ID: 20260321_0002
Revises: 20260321_0001
Create Date: 2026-03-21 00:02:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260321_0002"
down_revision: Union[str, None] = "20260321_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_names(table_name: str) -> set[str]:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return {column["name"] for column in inspector.get_columns(table_name)}


def _check_constraint_names(table_name: str) -> set[str]:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return {constraint["name"] for constraint in inspector.get_check_constraints(table_name)}


def _add_updated_at(table_name: str) -> None:
    if "updated_at" not in _column_names(table_name):
        op.add_column(
            table_name,
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.func.now(),
                nullable=False,
            ),
        )


def upgrade() -> None:
    user_columns = _column_names("users")

    if "password_hash" not in user_columns:
        op.add_column("users", sa.Column("password_hash", sa.String(length=255)))
        op.execute(
            "UPDATE users "
            "SET password_hash = 'legacy-unset-password-hash' "
            "WHERE password_hash IS NULL"
        )
        op.alter_column("users", "password_hash", nullable=False)

    if "display_name" in user_columns:
        op.drop_column("users", "display_name")

    for table_name in ("users", "auth_sessions", "relationships"):
        _add_updated_at(table_name)

    user_checks = _check_constraint_names("users")
    if "ck_users_role_valid" not in user_checks:
        op.create_check_constraint(
            "ck_users_role_valid",
            "users",
            "role IN ('owner', 'moderator', 'viewer')",
        )

    relationship_checks = _check_constraint_names("relationships")
    if "ck_relationship_type_valid" not in relationship_checks:
        op.create_check_constraint(
            "ck_relationship_type_valid",
            "relationships",
            "relationship_type IN ('parent_child', 'partner')",
        )


def downgrade() -> None:
    relationship_checks = _check_constraint_names("relationships")
    if "ck_relationship_type_valid" in relationship_checks:
        op.drop_constraint(
            "ck_relationship_type_valid",
            "relationships",
            type_="check",
        )

    user_checks = _check_constraint_names("users")
    if "ck_users_role_valid" in user_checks:
        op.drop_constraint("ck_users_role_valid", "users", type_="check")

    for table_name in ("relationships", "auth_sessions", "users"):
        if "updated_at" in _column_names(table_name):
            op.drop_column(table_name, "updated_at")

    user_columns = _column_names("users")
    if "display_name" not in user_columns:
        op.add_column(
            "users",
            sa.Column(
                "display_name",
                sa.String(length=200),
                server_default="",
                nullable=False,
            ),
        )
        op.alter_column("users", "display_name", server_default=None)

    if "password_hash" in user_columns:
        op.drop_column("users", "password_hash")
