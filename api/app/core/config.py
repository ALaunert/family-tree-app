from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "family-tree-app"


settings = Settings()
