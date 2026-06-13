from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = os.environ.get("APP_NAME", "family-tree-app")
    database_url: str = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg://family_tree:family_tree@db:5432/family_tree",
    )


settings = Settings()
