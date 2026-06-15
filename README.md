# Family Tree App

A small full-stack family tree application with a FastAPI backend, Vue frontend,
PostgreSQL storage, and Docker Compose for local development.

## Local Setup

Copy the example environment file, build the containers, run migrations, seed the
owner account, and start the app:

```bash
make setup
docker compose build
make migrate
make seed-owner
make up
```

The web app runs at http://localhost:5173 and the API runs at
http://localhost:8000 by default.

## Common Commands

Start the database, API, and web app:

```bash
make up
```

Stop local services:

```bash
make down
```

Follow service logs:

```bash
make logs
```

Run database migrations:

```bash
make migrate
```

Create or refresh the owner user from `OWNER_EMAIL` and `OWNER_PASSWORD`:

```bash
make seed-owner
```

Create an invited user:

```bash
make create-user EMAIL=user@example.com PASSWORD=change-me ROLE=viewer
```

Supported roles are `owner`, `moderator`, and `viewer`.

## Verification

Run API and web unit tests:

```bash
make test
```

Run browser end-to-end tests:

```bash
make test-e2e
```

Run the smoke check, including service startup, migrations, owner seeding, demo
data seeding, and the API health probe:

```bash
make smoke
```

The smoke script uses the normal host ports `8000` for the API and `5173` for the
web service. Override them only if another local service already uses those
ports:

```bash
API_PORT=28000 WEB_PORT=25173 make smoke
```

## Users

Authentication uses server-side sessions with an HTTP-only
`family_tree_session` cookie. Passwords are hashed with Argon2.

The e2e demo seed creates:

- `viewer@example.com` / `viewer-password`
- `moderator@example.com` / `moderator-password`
