"""Pytest configuration for API tests."""

import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url


def _test_database_url(database_url: str) -> str:
    url = make_url(database_url)
    database_name = url.database or ""
    test_database_name = (
        database_name if database_name.endswith("_test") else f"{database_name}_test"
    )

    return url.set(database=test_database_name).render_as_string(hide_password=False)


def _ensure_test_database(database_url: str) -> None:
    url = make_url(database_url)
    database_name = url.database
    if database_name is None or not database_name.endswith("_test"):
        raise RuntimeError("Refusing to prepare a database that does not end with _test")

    admin_url = url.set(database="postgres")
    admin_engine = create_engine(
        admin_url.render_as_string(hide_password=False),
        isolation_level="AUTOCOMMIT",
    )

    with admin_engine.connect() as connection:
        exists = connection.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :database_name"),
            {"database_name": database_name},
        ).scalar_one_or_none()
        if exists is None:
            quoted_name = admin_engine.dialect.identifier_preparer.quote(database_name)
            connection.execute(text(f"CREATE DATABASE {quoted_name}"))

    admin_engine.dispose()


def _run_migrations(database_url: str) -> None:
    api_dir = Path(__file__).resolve().parents[1]
    alembic_config = Config(str(api_dir / "alembic.ini"))
    alembic_config.set_main_option("script_location", str(api_dir / "alembic"))
    alembic_config.set_main_option("sqlalchemy.url", database_url)

    command.upgrade(alembic_config, "head")


def _prepare_test_database() -> None:
    database_url = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg://family_tree:family_tree@db:5432/family_tree",
    )
    test_database_url = _test_database_url(database_url)
    os.environ["DATABASE_URL"] = test_database_url

    _ensure_test_database(test_database_url)
    _run_migrations(test_database_url)


_prepare_test_database()
