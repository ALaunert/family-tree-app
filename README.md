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

## Verification

Run `make smoke` to verify the bootstrap files exist and the compose file parses.
