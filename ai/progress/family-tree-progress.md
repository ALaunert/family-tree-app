# Family Tree App Progress

Date: 2026-06-13
Branch: `codex/family-tree-implementation`
Worktree: `/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation`
Primary plan: [2026-03-21-family-tree-app-implementation-plan.md](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/ai/plans/2026-03-21-family-tree-app-implementation-plan.md)
Supporting design: [2026-03-20-family-tree-app-design.md](/Users/launert/projects/family-tree-app/.worktrees/family-tree-implementation/ai/specs/2026-03-20-family-tree-app-design.md)

## Summary

Implementation is through Task 3.

- Task 1 is complete.
- Task 2 is complete.
- Task 3 is complete.
- Tasks 4-10 are still pending.

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

Note:

- Necessary plan deviation: added `alembic`, `SQLAlchemy>=2.0`, and `psycopg[binary]` to `api/pyproject.toml`, which was not listed in the Task 3 file list but was required for the database layer and migrations.
- Environment note: after some successful Docker runs, sandboxed Docker access began returning permission errors for `/Users/launert/.docker/run/docker.sock`. Docker worked with escalated access, so final Docker-based verification was completed that way without repo code changes.
- Review follow-up migration approach: kept the original revision history and added a second idempotent reconciliation revision. The initial revision now also reflects the corrected schema, so fresh databases get the reviewed shape immediately; the second revision no-ops when it is already true.

### Tasks 4-10

Status: not started

Remaining planned work:

- Task 4: session auth and owner bootstrapping
- Task 5: people CRUD and role checks
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

- `docker compose run --rm api alembic upgrade head`
  - pass; applied review follow-up migration `20260321_0002`.
- `docker compose exec db psql -U family_tree -d family_tree -c '\dt'`
  - pass; confirmed `users`, `auth_sessions`, `people`, and `relationships` tables exist.
- `docker compose run --rm api pytest tests/db/test_schema_constraints.py -q`
  - pass; 7 passed.
- `docker compose build api`
  - pass.
- `docker compose run --rm api pytest -q`
  - pass; 8 passed, 1 existing Starlette/httpx deprecation warning.
- `docker compose -p family-tree-task3-verify run --rm api alembic upgrade head`
  - pass; applied `20260321_0001` and `20260321_0002` from scratch in a temporary project.
- Isolated fresh DB catalog checks:
  - pass; confirmed `users`, `auth_sessions`, `people`, and `relationships`.
  - pass; confirmed `users.password_hash` is non-null and `users.display_name` is absent.
  - pass; confirmed `created_at` and `updated_at` are non-null on all four app tables.
  - pass; confirmed `ck_users_role_valid`, `ck_relationship_type_valid`, `ck_relationship_not_self`, `uq_relationship_pair`, and `uq_users_email`.
- `docker compose -p family-tree-task3-verify down -v --remove-orphans`
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
- no auth layer yet
- no frontend app files yet beyond `web/Dockerfile`

Diff against the pre-implementation branch point:

- Task 3 database schema was committed in `cf79957`.
- Review follow-up fixes are recorded in a separate follow-up commit after `cf79957`.

## Recommended Next Step

Begin Task 4: session auth and owner bootstrapping.

## Quick Resume Notes

If resuming in a new dialogue, the next implementation step is:

- Task 4: Add Session Auth and Owner Bootstrapping

If resuming in the same environment, first check Docker availability:

```bash
docker context show
ls -la ~/.docker/run
docker compose build api
docker compose run --rm api pytest -q
```
