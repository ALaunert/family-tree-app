# Family Tree App

Bootstrap tooling for the Family Tree App monorepo.

## Included

- `compose.yml` for Postgres, API, and web services
- `Makefile` targets for common local workflows
- `.env.example` with the initial application settings
- Placeholder Dockerfiles for the future FastAPI and Vue/Vite apps

## Quick Start

1. Run `make setup`
2. Review `.env`
3. Run `make up`
4. Run `make seed-owner` to create the owner account from `OWNER_EMAIL` and `OWNER_PASSWORD`

## Users

Authentication uses server-side sessions with an HTTP-only `family_tree_session` cookie.
Passwords are hashed with Argon2.

Create the initial owner account:

```bash
make seed-owner
```

Create invited users from the CLI:

```bash
make create-user EMAIL="viewer@example.com" PASSWORD="change-me" ROLE="viewer"
```

Supported roles are `owner`, `moderator`, and `viewer`.

## Verification

Run `make smoke` to verify the bootstrap files exist and the compose file parses.
