import argparse

from app.db.session import SessionLocal
from app.models.user import UserRole
from app.services.auth_service import create_user


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a family-tree app user.")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--role", choices=[role.value for role in UserRole], required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with SessionLocal() as db:
        user = create_user(
            db,
            email=args.email,
            password=args.password,
            role=UserRole(args.role),
        )
        print(f"Created user: {user.email} ({user.role.value})")


if __name__ == "__main__":
    main()
