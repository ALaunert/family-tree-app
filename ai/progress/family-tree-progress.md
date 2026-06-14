# Family Tree App Progress

Date: 2026-06-13
Branch: `codex/family-tree-implementation`
Worktree: `/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation`
Primary plan: [2026-03-21-family-tree-app-implementation-plan.md](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/ai/plans/2026-03-21-family-tree-app-implementation-plan.md)
Supporting design: [2026-03-20-family-tree-app-design.md](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/ai/specs/2026-03-20-family-tree-app-design.md)

## Summary

Implementation is through Task 5.

- Task 1 is complete.
- Task 2 is complete.
- Task 3 is complete.
- Task 4 is complete.
- Task 5 is complete.
- Tasks 6-10 are still pending.

The plan document remains the source of truth for intended scope, but its checkbox list has not been updated during execution. Use this progress file plus git history for actual state.

## Plan vs Actual

### Task 1: Bootstrap Repository Tooling

Status: complete

Implemented:

- [/.gitignore](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/.gitignore)
- [/.env.example](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/.env.example)
- [/compose.yml](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/compose.yml)
- [/Makefile](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/Makefile)
- [/README.md](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/README.md)
- [/api/Dockerfile](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/api/Dockerfile)
- [/web/Dockerfile](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/web/Dockerfile)
- [/scripts/smoke.sh](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/scripts/smoke.sh)

Completed work:

- Root bootstrap files were created.
- The smoke script from the plan exists unchanged.
- The GitHub remote already pointed at the expected repository and did not need to be created.

Execution-time adjustments against the literal Task 1 skeleton:

- `compose.yml` includes minimal Postgres environment wiring on `db` so the container can start.
- `Makefile` `setup` preserves an existing `.env` without masking real copy failures.
- `.gitignore` was expanded beyond the initial `.worktrees/` entry to cover Python and Node artifacts.

Task 1 completion commits:

- `49d697b` `chore: bootstrap repo tooling`
- `46690aa` `fix: trim compose bootstrap skeleton`
- `b0cb4f1` `fix: wire db env defaults for bootstrap`

### Task 2: Backend App Skeleton and Health Endpoint

Status: complete

Implemented:

- [/api/pyproject.toml](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/api/pyproject.toml)
- [/api/app/__init__.py](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/api/app/__init__.py)
- [/api/app/main.py](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/api/app/main.py)
- [/api/app/core/config.py](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/api/app/core/config.py)
- [/api/app/api/__init__.py](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/api/app/api/__init__.py)
- [/api/app/api/router.py](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/api/app/api/router.py)
- [/api/app/api/routes/health.py](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/api/app/api/routes/health.py)
- [/api/tests/conftest.py](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/api/tests/conftest.py)
- [/api/tests/test_health.py](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/api/tests/test_health.py)
- [/compose.yml](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/compose.yml)
- [/Makefile](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/Makefile)

Completed work:

- FastAPI app bootstrap exists.
- `/api/v1/health` returns `{"status": "ok"}`.
- The exact health test shape from the plan is present in `api/tests/test_health.py`.
- `compose.yml` runs the API with the planned `uvicorn` command, port mapping, working directory, and bind mount.
- `Makefile` `test-api` runs `docker compose run --rm api pytest -q`.

Execution-time adjustments against the literal Task 2 file list:

- `api/Dockerfile` had to be expanded beyond the Task 1 placeholder so the compose-based test flow could actually run.
- The final backend image:
  - installs dependencies from `pyproject.toml`
  - copies `app/` and `tests/`
  - sets `PYTHONPATH=/app`
  - uses a `uvicorn` `CMD`
- `api/tests/conftest.py` is present because the task required the file, but it currently only contains a docstring and no shared fixtures.

Why those adjustments were needed:

- The original placeholder backend image could not run `pytest`.
- After Docker networking was fixed, the exact plan command still failed under the `pytest` entrypoint until `PYTHONPATH=/app` was added.

Task 2 completion commits:

- `e2596d5` `feat: add backend app skeleton`
- `d64b30a` `fix: align api image and tests`
- `95c1f25` `fix: restore health test shape`
- `b458a8f` `fix: add api pythonpath`

### Task 3: Database Wiring and Initial Schema

Status: complete

Planned scope:

- SQLAlchemy session and model layer
- Alembic configuration and initial migration
- Database constraint tests
- Postgres healthcheck and persistent volume
- Real `make migrate`

Completed work:

- Added the failing-first schema constraint tests for unique user emails and rejected self-link relationships.
- Added SQLAlchemy 2.0 database session wiring.
- Added initial models for users, auth sessions, people, and relationships.
- Added Alembic configuration and the initial schema migration.
- Added Postgres healthcheck and persistent `postgres-data` compose volume.
- Replaced the placeholder `make migrate` target with `docker compose run --rm api alembic upgrade head`.
- Review follow-up corrected the user schema to require `password_hash` and removed the unplanned required `display_name`.
- Review follow-up added database check constraints for `users.role` and `relationships.relationship_type`.
- Review follow-up made timestamps consistent with `created_at` and `updated_at` on `users`, `auth_sessions`, `people`, and `relationships`.
- Review follow-up added database constraint coverage for duplicate relationship pairs.
- Review follow-up added `20260321_0002_review_schema_constraints.py` so existing local DBs at `20260321_0001` can be reconciled without deleting the normal compose volume.
- Re-review follow-up made API tests use a dedicated `_test` database derived from `DATABASE_URL` before app DB settings import.
- Re-review follow-up added a guard to the destructive schema-test cleanup fixture so it refuses to delete rows unless the active database name ends with `_test`.
- Re-review follow-up made the `20260321_0002` downgrade a documented no-op so downgrading to the checked-in `20260321_0001` schema does not remove clean-schema columns or constraints.
- Re-review follow-up added Alembic `path_separator = os` to avoid the config deprecation warning surfaced by running migrations from tests.

Current TDD status:

- Original red verification complete:
  - `docker compose run --rm api pytest tests/db/test_schema_constraints.py -q`
  - Result: expected failure, exit 2 during test collection because `sqlalchemy` is not installed yet.
- Original green verification complete:
  - `docker compose run --rm api pytest tests/db/test_schema_constraints.py -q`
  - Result: 2 passed.
- Review follow-up red verification complete:
  - `docker compose run --rm api pytest tests/db/test_schema_constraints.py -q`
  - Result: expected failure, 5 failed and 2 passed. Failures covered missing `password_hash`, missing relationship type check constraint, missing `updated_at`, and stale user shape.
- Review follow-up green verification complete:
  - `docker compose run --rm api pytest tests/db/test_schema_constraints.py -q`
  - Result: 7 passed.
- Re-review red verification complete:
  - `docker compose run --rm api pytest tests/db/test_schema_constraints.py -q`
  - Result: expected failure, 1 failed and 7 passed. Failure showed active database was `family_tree`, not a `_test` database.
- Re-review downgrade reproduction complete:
  - `docker compose -p family-tree-downgrade-red run --rm api alembic upgrade head`
  - `docker compose -p family-tree-downgrade-red run --rm api alembic downgrade 20260321_0001`
  - Result: unsafe old downgrade removed `password_hash` and `updated_at`, re-added `display_name`, and removed enum check constraints.
- Re-review green verification complete:
  - `docker compose run --rm api pytest tests/db/test_schema_constraints.py -q`
  - Result: 8 passed.

Verification:

- `docker compose build api`
  - pass
- `docker compose up -d db`
  - pass
- `docker compose run --rm api alembic upgrade head`
  - pass
- `docker compose exec db psql -U family_tree -d family_tree -c '\dt'`
  - pass; confirmed `users`, `auth_sessions`, `people`, and `relationships` tables exist.
- `make migrate`
  - pass; Alembic no-op after the initial migration had already been applied.
- `docker compose run --rm api pytest -q`
  - pass; 3 passed, 1 existing Starlette/httpx deprecation warning.
- Review follow-up `docker compose run --rm api alembic upgrade head`
  - pass; applied `20260321_0002`.
- Review follow-up `docker compose run --rm api pytest tests/db/test_schema_constraints.py -q`
  - pass; 7 passed.
- Review follow-up `docker compose build api`
  - pass.
- Review follow-up `docker compose run --rm api pytest -q`
  - pass; 8 passed, 1 existing Starlette/httpx deprecation warning.
- Review follow-up fresh migration verification:
  - `docker compose -p family-tree-task3-verify up -d db`
  - `docker compose -p family-tree-task3-verify run --rm api alembic upgrade head`
  - `docker compose -p family-tree-task3-verify exec db psql ...`
  - Result: both revisions applied from scratch; confirmed all four app tables, required `password_hash`, no `display_name`, non-null timestamps, role/type check constraints, and relationship/user unique constraints.
  - Cleanup: `docker compose -p family-tree-task3-verify down -v --remove-orphans` removed only the temporary project resources.
- Re-review `docker compose build api`
  - pass.
- Re-review `docker compose run --rm api pytest tests/db/test_schema_constraints.py -q`
  - pass; 8 passed.
- Re-review `docker compose run --rm api pytest -q`
  - pass; 9 passed, 1 existing Starlette/httpx deprecation warning.
- Re-review isolated downgrade verification:
  - `docker compose -p family-tree-downgrade-final up -d db`
  - `docker compose -p family-tree-downgrade-final run --rm api alembic upgrade head`
  - `docker compose -p family-tree-downgrade-final run --rm api alembic downgrade 20260321_0001`
  - Result: after downgrade, clean schema remained intact: app tables exist, `password_hash` remains, `display_name` remains absent, timestamps remain on all four app tables, and role/type/relationship/user constraints remain.
  - Cleanup: `docker compose -p family-tree-downgrade-final down -v --remove-orphans` removed only the temporary project resources.

Note:

- Necessary plan deviation: added `alembic`, `SQLAlchemy>=2.0`, and `psycopg[binary]` to `api/pyproject.toml`, which was not listed in the Task 3 file list but was required for the database layer and migrations.
- Environment note: after some successful Docker runs, sandboxed Docker access began returning permission errors for `/Users/launert/.docker/run/docker.sock`. Docker worked with escalated access, so final Docker-based verification was completed that way without repo code changes.
- Review follow-up migration approach: kept the original revision history and added a second idempotent reconciliation revision. The initial revision now also reflects the corrected schema, so fresh databases get the reviewed shape immediately; the second revision no-ops when it is already true.
- Re-review migration downgrade decision: `20260321_0002` downgrade is intentionally a no-op because checked-in `20260321_0001` already defines the clean schema. Reversing `0002` should only move Alembic's version marker, not mutate the database back to the pre-review shape.
- Re-review test database decision: pytest derives the test database name by appending `_test` to the configured database name and creates/migrates it automatically through the Postgres admin database. This keeps test cleanup away from non-test data while preserving the normal compose database.

### Task 4: Implement Session Auth and Owner Bootstrapping

Status: complete

Planned scope:

- Session authentication with server-stored `auth_sessions` rows and an HTTP-only `family_tree_session` cookie.
- Password hashing with Argon2 through `pwdlib[argon2]`.
- Auth routes for login, logout, and current-user lookup.
- Owner bootstrap and invited-user CLI scripts.
- Make targets and README updates.

Completed work:

- Added failing-first auth tests for login cookie creation, unauthenticated `/me`, authenticated `/me`, and logout cookie/session cleanup.
- Added password hashing and verification helpers in `api/app/core/security.py`.
- Added DB and current-user dependencies in `api/app/api/deps.py`.
- Added auth request/response schemas in `api/app/schemas/auth.py`.
- Added auth service functions for login verification, session creation, session lookup, session deletion, user creation, and idempotent owner creation.
- Added `POST /api/v1/auth/login`, `POST /api/v1/auth/logout`, and `GET /api/v1/auth/me`.
- Added owner and user creation scripts under `api/scripts/`.
- Replaced placeholder `seed-owner` and `create-user` Make targets.
- Updated README with owner bootstrap and CLI user creation instructions.
- Wired `SESSION_TTL_HOURS`, `OWNER_EMAIL`, and `OWNER_PASSWORD` into the API container environment so the required compose-run owner smoke command works.
- Spec-review follow-up made owner bootstrap promote an existing same-email user to `owner`.
- Code-review follow-up made owner bootstrap reset the password hash from `OWNER_PASSWORD` when ensuring an existing owner email.
- Code-review follow-up added `SESSION_COOKIE_SECURE` and marks auth cookies as `Secure` by default.
- Code-review follow-up invalidates existing sessions when owner bootstrap resets an existing account password.

Current TDD status:

- Red verification complete:
  - `docker compose run --rm api pytest tests/auth/test_login.py -q`
  - Result: expected failure, 4 failed. All failures were 404s because auth routes were not implemented yet.
- First green attempt:
  - `docker compose run --rm api pytest tests/auth/test_login.py -q`
  - Result: failed during import because the existing API image did not yet include newly declared `pwdlib`.
  - Follow-up: `docker compose build api` installed the new dependency.
- Second green attempt:
  - `docker compose run --rm api pytest tests/auth/test_login.py -q`
  - Result: failed during import because `EmailStr` required the optional `email-validator` package.
  - Follow-up: auth schemas were simplified to plain `str` emails to avoid an unneeded extra dependency.
- Third green attempt:
  - `docker compose run --rm api pytest tests/auth/test_login.py -q`
  - Result: 1 failed and 3 passed. Logout returned a response with no status code.
  - Follow-up: logout now explicitly sets HTTP 204 before returning the injected response.
- Final green verification:
  - `docker compose run --rm api pytest tests/auth/test_login.py -q`
  - Result: 4 passed, 1 existing Starlette/httpx deprecation warning.
- Spec-review follow-up red verification complete:
  - `docker compose run --rm api pytest tests/auth/test_login.py -q`
  - Result: expected failure, 1 failed and 4 passed. Existing same-email viewer was not promoted to `owner`.
- Spec-review follow-up green verification complete:
  - `docker compose run --rm api pytest tests/auth/test_login.py -q`
  - Result: 5 passed, 1 existing Starlette/httpx deprecation warning.
- Code-review follow-up red verification complete:
  - `docker compose run --rm api pytest tests/auth/test_login.py -q`
  - Result: expected failure, 2 failed and 3 passed. Session cookie lacked `Secure`, and owner promotion did not reset the password hash.
- Code-review follow-up green verification complete:
  - `docker compose run --rm api pytest tests/auth/test_login.py -q`
  - Result: 5 passed, 1 existing Starlette/httpx deprecation warning.
- Session-invalidation follow-up red verification complete:
  - `docker compose run --rm api pytest tests/auth/test_login.py -q`
  - Result: expected failure, 1 failed and 4 passed. Existing owner session remained valid after password reset.
- Session-invalidation follow-up green verification complete:
  - `docker compose run --rm api pytest tests/auth/test_login.py -q`
  - Result: 5 passed, 1 existing Starlette/httpx deprecation warning.

Verification:

- `docker compose run --rm api pytest tests/auth/test_login.py -q`
  - pass; 4 passed, 1 existing Starlette/httpx deprecation warning.
- `docker compose run --rm api python scripts/seed_owner.py`
  - pass; printed `Owner user ready: owner@example.com`.
- `docker compose run --rm api python scripts/seed_owner.py`
  - pass on second run; printed `Owner user ready: owner@example.com`.
- `docker compose exec db psql -U family_tree -d family_tree -tAc "SELECT count(*) FROM users WHERE email = 'owner@example.com' AND role = 'owner';"`
  - pass; returned `1`.
- `docker compose run --rm api pytest -q`
  - pass; 13 passed, 1 existing Starlette/httpx deprecation warning.
- `docker compose build api`
  - pass.
- Spec-review follow-up `docker compose run --rm api pytest tests/auth/test_login.py -q`
  - pass; 5 passed, 1 existing Starlette/httpx deprecation warning.
- Spec-review follow-up `docker compose run --rm api pytest -q`
  - pass; 14 passed, 1 existing Starlette/httpx deprecation warning.
- Code-review follow-up `docker compose run --rm api pytest tests/auth/test_login.py -q`
  - pass; 5 passed, 1 existing Starlette/httpx deprecation warning.
- Code-review follow-up `docker compose run --rm api pytest -q`
  - pass; 14 passed, 1 existing Starlette/httpx deprecation warning.
- Verification note: DB-mutating pytest commands must not be run in parallel against the shared `_test` database. A parallel auth-suite/full-suite run raced on cleanup and produced transient integrity errors; rerunning the auth suite alone passed.
- Session-invalidation follow-up `docker compose run --rm api pytest tests/auth/test_login.py -q`
  - pass; 5 passed, 1 existing Starlette/httpx deprecation warning.
- Session-invalidation follow-up `docker compose run --rm api pytest -q`
  - pass; 14 passed, 1 existing Starlette/httpx deprecation warning.

Execution-time adjustments against the literal Task 4 file list:

- Added `pwdlib[argon2]` to `api/pyproject.toml`; this was required by the task but not listed in the Task 4 file list.
- Added `session_ttl_hours` to `api/app/core/config.py`; this keeps the existing `SESSION_TTL_HOURS` setting wired into the auth session lifetime.
- Modified `compose.yml` to pass `SESSION_TTL_HOURS`, `OWNER_EMAIL`, and `OWNER_PASSWORD` into the API container. This was required for the exact owner smoke command to pass using the repo's existing `.env.example` defaults.
- Used plain `str` email fields in auth schemas instead of Pydantic `EmailStr` to avoid adding an unrelated optional validation dependency for this task.
- Added `SESSION_COOKIE_SECURE` to `.env.example`, `compose.yml`, and API settings as a security-hardening follow-up from code review. The default is `true`.
- Updated the API test client to use an HTTPS base URL so secure cookies are sent during authenticated route tests.
- Avoid running DB-mutating API pytest commands in parallel unless they use isolated database names.

### Task 5: Implement People CRUD and Role Checks

Status: complete

Planned scope:

- Person create/update/read schemas with camelCase JSON aliases.
- Person service layer for list, get, create, and update.
- People API routes for:
  - `GET /api/v1/people`
  - `GET /api/v1/people/{person_id}`
  - `POST /api/v1/people`
  - `PATCH /api/v1/people/{person_id}`
- Role checks so viewers can read, while moderators and owners can write.
- People API tests written before implementation.

Completed work:

- Added failing-first people API tests in `api/tests/people/test_people_api.py`.
- Added authenticated viewer, moderator, and owner test clients that log in through the real auth endpoint.
- Added `api/app/schemas/person.py` with Pydantic aliases for `fullName`, `birthDate`, and `deathDate`, plus blank-name validation.
- Added `api/app/services/person_service.py` for SQLAlchemy-backed people operations.
- Added `api/app/api/routes/people.py` with authenticated read routes and moderator/owner write checks.
- Included the people router from `api/app/api/router.py`.

Current TDD status:

- Red verification complete:
  - `docker compose run --rm api pytest tests/people/test_people_api.py -q`
  - Result: expected failure, 7 failed. All failures were `404 Not Found` because people routes were not implemented yet.
- Green verification complete:
  - `docker compose run --rm api pytest tests/people/test_people_api.py -q`
  - Result: 7 passed, 1 existing Starlette/httpx deprecation warning.

Verification:

- `docker compose build api`
  - pass.
- `docker compose run --rm api pytest tests/people/test_people_api.py -q`
  - pass; 7 passed, 1 existing Starlette/httpx deprecation warning.
- `docker compose run --rm api pytest -q`
  - pass; 21 passed, 1 existing Starlette/httpx deprecation warning.

Execution-time adjustments against the literal Task 5 file list:

- Added a viewer get-person test to cover `GET /api/v1/people/{person_id}` from the planned route list.
- Added an owner create test to verify owners share moderator write permissions.

### Tasks 6-10

Status: not started

Remaining planned work:

- Task 6: relationship rules and tree payload
- Task 7: Vue frontend and auth flow
- Task 8: tree viewer and person details panel
- Task 9: moderator editing and quick-jump search
- Task 10: end-to-end journeys, smoke coverage, and final docs

## Verification Snapshot

### Verified in prior execution

These checks were successfully run after Task 2 was fixed:

- `docker compose build api`
- `docker compose run --rm api pytest tests/test_health.py -q`
- `make test-api`

At that point, the exact Task 2 health test passed in-container.

### Verified in the current session

- `docker compose build api`
  - pass.
- `docker compose run --rm api pytest tests/people/test_people_api.py -q`
  - pass; 7 passed, 1 existing Starlette/httpx deprecation warning.
- `docker compose run --rm api pytest tests/db/test_schema_constraints.py -q`
  - pass; 8 passed.
- `docker compose run --rm api pytest -q`
  - pass; 21 passed, 1 existing Starlette/httpx deprecation warning.
- `docker compose -p family-tree-downgrade-final run --rm api alembic upgrade head`
  - pass; applied `20260321_0001` and `20260321_0002` from scratch in a temporary project.
- `docker compose -p family-tree-downgrade-final run --rm api alembic downgrade 20260321_0001`
  - pass; no-op downgrade preserved the clean schema.
- Isolated downgrade DB catalog checks:
  - pass; confirmed `users`, `auth_sessions`, `people`, and `relationships`.
  - pass; confirmed `users.password_hash` is non-null and `users.display_name` is absent.
  - pass; confirmed `created_at` and `updated_at` are non-null on all four app tables.
  - pass; confirmed `ck_users_role_valid`, `ck_relationship_type_valid`, `ck_relationship_not_self`, `uq_relationship_pair`, and `uq_users_email`.
- `docker compose -p family-tree-downgrade-final down -v --remove-orphans`
  - pass; removed only the temporary project resources.

## Environment Notes

Two environment issues came up during execution:

### 1. Docker Desktop DNS issue

Observed during Task 2 work:

- Host network could resolve PyPI.
- Plain Docker containers could not resolve `pypi.org`.
- Containers only worked when explicitly given public DNS.

The engine daemon DNS was changed during execution to:

```json
["1.1.1.1", "8.8.8.8"]
```

This was a Docker Desktop environment fix, not a repo change.

### 2. Docker socket sandbox issue

Current session state:

- Docker context is `desktop-linux`
- `~/.docker/run/docker.sock` exists
- sandboxed Docker commands began returning permission errors partway through Task 3
- escalated Docker access worked and confirmed the project database container was healthy

This appears to be a sandbox permission issue, not a repo code issue.

## Current File Surface vs Plan

Present in the branch now:

- root bootstrap files from Task 1
- backend skeleton files from Task 2
- database layer, initial models, Alembic migration plumbing, and schema tests from Task 3
- session auth, owner bootstrap, invited-user CLI, and auth tests from Task 4
- no frontend app files yet beyond `web/Dockerfile`

Diff against the pre-implementation branch point:

- Task 3 database schema was committed in `cf79957`.
- Review follow-up fixes are recorded in a separate follow-up commit after `cf79957`.
- Task 4 session auth was committed in `3d80324`.

## Recommended Next Step

Begin Task 6: relationship rules and tree payload.

## Quick Resume Notes

If resuming in a new dialogue, the next implementation step is:

- Task 6: relationship rules and tree payload

If resuming in the same environment, first check Docker availability:

```bash
docker context show
ls -la ~/.docker/run
docker compose build api
docker compose run --rm api pytest -q
```
