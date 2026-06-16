from dataclasses import dataclass
import os


def _env_bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default

    return value.lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str = os.environ.get("APP_NAME", "family-tree-app")
    database_url: str = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg://family_tree:family_tree@db:5432/family_tree",
    )
    session_ttl_hours: int = int(os.environ.get("SESSION_TTL_HOURS", "168"))
    session_cookie_secure: bool = _env_bool("SESSION_COOKIE_SECURE", True)


settings = Settings()
