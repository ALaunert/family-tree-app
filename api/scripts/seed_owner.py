import os

from app.db.session import SessionLocal
from app.services.auth_service import get_or_create_owner


def main() -> None:
    email = os.environ.get("OWNER_EMAIL")
    password = os.environ.get("OWNER_PASSWORD")
    if not email or not password:
        raise SystemExit("OWNER_EMAIL and OWNER_PASSWORD are required")

    with SessionLocal() as db:
        owner = get_or_create_owner(db, email=email, password=password)
        print(f"Owner user ready: {owner.email}")


if __name__ == "__main__":
    main()
