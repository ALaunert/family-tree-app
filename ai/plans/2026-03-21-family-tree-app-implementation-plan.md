# Family Tree App Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first private, Dockerized version of the family tree app with login, role-aware tree browsing, moderator editing, and containerized verification.

**Architecture:** Use a small monorepo with a FastAPI backend in `api/`, a Vue + Vite frontend in `web/`, and PostgreSQL in Docker Compose. The API owns authentication, permissions, persistence, relationship validation, and tree payloads; the frontend owns the interactive tree canvas, person details, search, and moderator forms. V1 uses owner-seeded accounts and server-side session cookies instead of a separate account-management UI.

**Tech Stack:** Python 3.13, FastAPI, SQLAlchemy 2.0, Alembic, `pwdlib[argon2]`, PostgreSQL 16, pytest, Node 22, Vue 3 + TypeScript + Vite, Vue Router, Vue Flow, Dagre, Vitest, Vue Testing Library, Playwright, Docker Compose, Make

---

**Execution rules:** Implement each task with `@test-driven-development`. Before marking the repo complete, run `@verification-before-completion` against API, web, e2e, and smoke targets.

## Planning Decisions

- The repo stays self-contained under `~/projects/family-tree-app`, and all AI artifacts live under `ai/`.
- `compose.yml` manages four services: `db`, `api`, `web`, and one-shot `e2e`.
- Authentication uses server-stored sessions plus an HTTP-only cookie; passwords are hashed with Argon2 via `pwdlib`.
- The owner creates users via CLI/Make targets in v1. There is no user-management UI in this increment.
- The backend exposes normalized people and relationship data; the frontend converts that data into Vue Flow nodes and edges.
- The tree layout uses synthetic family-unit nodes plus Dagre so partner pairs and parent-child links can render consistently without adopting a graph database.
- Person editing supports create and update. Relationship editing in v1 is add/remove; there is no person delete flow in this increment.
- Search is client-side because the approved scale is under 100 people.

## Proposed Repository Structure

**Root**

- `compose.yml`: local orchestration for `db`, `api`, `web`, and `e2e`
- `.env.example`: documented environment variables for local and server runs
- `.gitignore`: Python, Node, Docker, and editor ignores
- `Makefile`: thin wrapper over setup, up/down, logs, migrations, tests, seeds, and smoke
- `README.md`: setup, local workflow, account bootstrap, and testing guide
- `scripts/smoke.sh`: container-based startup smoke test

**Backend (`api/`)**

- `api/Dockerfile`: backend dev image
- `api/pyproject.toml`: Python dependencies and pytest config
- `api/app/main.py`: FastAPI app bootstrap
- `api/app/core/config.py`: environment-driven settings
- `api/app/core/security.py`: password hashing, cookie/session helpers
- `api/app/db/session.py`: SQLAlchemy engine and session factory
- `api/app/models/`: `user.py`, `auth_session.py`, `person.py`, `relationship.py`
- `api/app/schemas/`: request/response models for auth, people, relationships, and tree payloads
- `api/app/services/`: auth, people, relationships, and tree orchestration
- `api/app/api/routes/`: `health.py`, `auth.py`, `people.py`, `relationships.py`, `tree.py`
- `api/alembic/`: migration config and versions
- `api/scripts/seed_owner.py`: idempotent owner bootstrap
- `api/scripts/create_user.py`: owner-run CLI user creation helper
- `api/scripts/seed_demo_data.py`: fixture data for UI/e2e flows
- `api/tests/`: API, DB, and service-level tests

**Frontend (`web/`)**

- `web/Dockerfile`: frontend dev image
- `web/package.json`: web dependencies and scripts
- `web/vite.config.ts`: dev server and `/api` proxy
- `web/playwright.config.ts`: e2e runner config
- `web/src/`: Vue app shell, router, and session guard
- `web/src/lib/fetchJson.ts`: shared API client wrapper
- `web/src/features/auth/`: login page and auth tests
- `web/src/features/tree/`: tree page, canvas, node components, layout logic, and tests
- `web/src/features/person/`: details panel
- `web/src/features/search/`: quick-jump UI
- `web/src/features/editor/`: moderator-only person and relationship forms
- `web/src/styles/index.css`: app styles and Vue Flow theming
- `web/src/test/`: Vitest setup and render helpers
- `web/e2e/`: login, viewer, and moderator journeys

## Data Model Notes

- `users`
  - `id`, `email` (unique), `password_hash`, `role` (`owner`, `moderator`, `viewer`), timestamps
- `auth_sessions`
  - `id`, `user_id`, `token_hash`, `expires_at`, timestamps
- `people`
  - `id`, `full_name`, `birth_date`, `death_date`, `notes`, timestamps
- `relationships`
  - `id`, `relationship_type` (`parent_child`, `partner`), `source_person_id`, `target_person_id`, timestamps
- DB constraints
  - no self-links
  - no duplicate relationship pairs
  - canonical partner ordering (`source_person_id < target_person_id` before insert)
- Service-level rules
  - max two parents per child in v1
  - no ancestry cycles for `parent_child`
  - no duplicate partner pairs even if the request submits the people in reverse order

## API Shape

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`
- `GET /api/v1/people`
- `GET /api/v1/people/{person_id}`
- `POST /api/v1/people`
- `PATCH /api/v1/people/{person_id}`
- `POST /api/v1/relationships`
- `DELETE /api/v1/relationships/{relationship_id}`
- `GET /api/v1/tree`

`GET /api/v1/tree` should return one payload the frontend can render without follow-up requests:

```json
{
  "viewerRole": "moderator",
  "people": [
    {
      "id": 1,
      "fullName": "Ada Example",
      "birthDate": "1951-01-03",
      "deathDate": null,
      "notes": "Tree root"
    }
  ],
  "relationships": [
    {
      "id": 4,
      "type": "partner",
      "sourcePersonId": 1,
      "targetPersonId": 2
    }
  ]
}
```

## Task 1: Bootstrap Repository Tooling

**Files:**
- Create: `.gitignore`
- Create: `.env.example`
- Create: `compose.yml`
- Create: `Makefile`
- Create: `README.md`
- Create: `api/Dockerfile`
- Create: `web/Dockerfile`
- Create: `scripts/smoke.sh`

- [ ] **Step 1: Write the failing bootstrap smoke script**

```bash
#!/usr/bin/env bash
set -euo pipefail

docker compose -f compose.yml config >/dev/null
grep -q '^up:' Makefile
grep -q '^test:' Makefile
test -f api/Dockerfile
test -f web/Dockerfile
```

- [ ] **Step 2: Run the bootstrap smoke script and confirm it fails**

Run: `bash scripts/smoke.sh`
Expected: FAIL because `compose.yml`, `Makefile`, and Dockerfiles do not exist yet.

- [ ] **Step 3: Add the root operator skeleton**

```makefile
up:
	docker compose up -d db api web

down:
	docker compose down --remove-orphans

test:
	$(MAKE) test-api
	$(MAKE) test-web
```

```yaml
services:
  db:
    image: postgres:16
  api:
    build:
      context: ./api
    ports:
      - "8000:8000"
  web:
    build:
      context: ./web
    ports:
      - "5173:5173"
```

- [ ] **Step 4: Flesh out the root workflow files**

Add these targets to `Makefile`: `setup`, `up`, `down`, `logs`, `migrate`, `seed-owner`, `create-user`, `test-api`, `test-web`, `test-e2e`, `test`, `smoke`.

Add these variables to `.env.example`:

```dotenv
POSTGRES_DB=family_tree
POSTGRES_USER=family_tree
POSTGRES_PASSWORD=family_tree
APP_SECRET_KEY=change-me
SESSION_TTL_HOURS=168
OWNER_EMAIL=owner@example.com
OWNER_PASSWORD=change-me
```

- [ ] **Step 5: Verify or create the GitHub remote**

Run: `gh repo view family-tree-app >/dev/null 2>&1 || gh repo create family-tree-app --public --source=. --remote=origin --push=false`
Expected: `git remote get-url origin` points at the public `family-tree-app` repository.

- [ ] **Step 6: Re-run the bootstrap smoke script**

Run: `bash scripts/smoke.sh`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add .gitignore .env.example compose.yml Makefile README.md api/Dockerfile web/Dockerfile scripts/smoke.sh
git commit -m "chore: bootstrap repo tooling"
```

## Task 2: Create the Backend App Skeleton and Health Endpoint

**Files:**
- Create: `api/pyproject.toml`
- Create: `api/app/__init__.py`
- Create: `api/app/main.py`
- Create: `api/app/core/config.py`
- Create: `api/app/api/__init__.py`
- Create: `api/app/api/router.py`
- Create: `api/app/api/routes/health.py`
- Create: `api/tests/conftest.py`
- Create: `api/tests/test_health.py`
- Modify: `compose.yml`
- Modify: `Makefile`

- [ ] **Step 1: Write the failing health test**

```python
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_healthcheck_returns_ok() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

- [ ] **Step 2: Run the backend health test and confirm it fails**

Run: `docker compose run --rm api pytest tests/test_health.py -q`
Expected: FAIL with import or module errors because the FastAPI app does not exist yet.

- [ ] **Step 3: Add the minimal FastAPI app**

```python
from fastapi import FastAPI

from app.api.router import api_router


app = FastAPI(title="family-tree-app")
app.include_router(api_router, prefix="/api/v1")
```

```python
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
```

- [ ] **Step 4: Add Python dependency and compose wiring**

`api/pyproject.toml` should include `fastapi`, `uvicorn[standard]`, `pytest`, `httpx`, and `pytest-cov`.

`compose.yml` should run the API with:

```yaml
command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
ports:
  - "8000:8000"
working_dir: /app
volumes:
  - ./api:/app
```

- [ ] **Step 5: Re-run the health test**

Run: `docker compose run --rm api pytest tests/test_health.py -q`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add api/pyproject.toml api/app api/tests compose.yml Makefile
git commit -m "feat: add backend app skeleton"
```

## Task 3: Add Database Wiring and the Initial Schema

**Files:**
- Create: `api/app/db/__init__.py`
- Create: `api/app/db/session.py`
- Create: `api/app/models/__init__.py`
- Create: `api/app/models/user.py`
- Create: `api/app/models/auth_session.py`
- Create: `api/app/models/person.py`
- Create: `api/app/models/relationship.py`
- Create: `api/alembic.ini`
- Create: `api/alembic/env.py`
- Create: `api/alembic/script.py.mako`
- Create: `api/alembic/versions/20260321_0001_initial_schema.py`
- Create: `api/tests/db/test_schema_constraints.py`
- Modify: `api/app/core/config.py`
- Modify: `compose.yml`
- Modify: `Makefile`

- [ ] **Step 1: Write the failing schema tests**

```python
def test_users_email_is_unique(db_session):
    ...


def test_relationships_reject_self_links(db_session):
    ...
```

The first test should insert two users with the same email and expect an integrity error.

The second test should insert a relationship where `source_person_id == target_person_id` and expect an integrity error.

- [ ] **Step 2: Run the schema tests and confirm they fail**

Run: `docker compose run --rm api pytest tests/db/test_schema_constraints.py -q`
Expected: FAIL because the DB layer, models, and migrations do not exist yet.

- [ ] **Step 3: Add SQLAlchemy models and migration plumbing**

Use SQLAlchemy 2.0 declarative models and Alembic.

```python
class UserRole(str, enum.Enum):
    OWNER = "owner"
    MODERATOR = "moderator"
    VIEWER = "viewer"


class RelationshipType(str, enum.Enum):
    PARENT_CHILD = "parent_child"
    PARTNER = "partner"
```

`relationships` must include:

```python
CheckConstraint("source_person_id <> target_person_id", name="ck_relationship_not_self")
UniqueConstraint("relationship_type", "source_person_id", "target_person_id", name="uq_relationship_pair")
```

- [ ] **Step 4: Add Postgres and migration commands**

`compose.yml` should give `db` a healthcheck and a persistent volume.

`Makefile` should include:

```makefile
migrate:
	docker compose run --rm api alembic upgrade head
```

- [ ] **Step 5: Apply the migration**

Run: `docker compose up -d db`
Run: `docker compose run --rm api alembic upgrade head`
Expected: PASS and all four tables exist.

- [ ] **Step 6: Re-run the schema tests**

Run: `docker compose run --rm api pytest tests/db/test_schema_constraints.py -q`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add api/app/db api/app/models api/alembic api/tests/db api/app/core/config.py compose.yml Makefile
git commit -m "feat: add initial database schema"
```

## Task 4: Implement Session Auth and Owner Bootstrapping

**Files:**
- Create: `api/app/core/security.py`
- Create: `api/app/api/deps.py`
- Create: `api/app/schemas/auth.py`
- Create: `api/app/services/auth_service.py`
- Create: `api/app/api/routes/auth.py`
- Create: `api/scripts/seed_owner.py`
- Create: `api/scripts/create_user.py`
- Create: `api/tests/auth/test_login.py`
- Modify: `api/app/api/router.py`
- Modify: `api/tests/conftest.py`
- Modify: `Makefile`
- Modify: `README.md`

- [ ] **Step 1: Write the failing auth tests**

```python
def test_login_sets_session_cookie(client, user_factory):
    ...


def test_me_requires_authentication(client):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401
```

Also add a logout test that expects the cookie to be cleared and the server-side session row deleted.

- [ ] **Step 2: Run the auth tests and confirm they fail**

Run: `docker compose run --rm api pytest tests/auth/test_login.py -q`
Expected: FAIL because auth routes and session helpers do not exist yet.

- [ ] **Step 3: Add password hashing and session cookies**

Use `pwdlib[argon2]` for password hashing.

```python
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)
```

Store a random session token hash in `auth_sessions`, and set an HTTP-only cookie named `family_tree_session`.

- [ ] **Step 4: Add auth routes**

Implement:

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`

Use `Cookie(...)` in FastAPI dependencies to read the session cookie.

- [ ] **Step 5: Add owner and invited-user bootstrap scripts**

`api/scripts/seed_owner.py` should idempotently create the owner from `OWNER_EMAIL` and `OWNER_PASSWORD`.

`api/scripts/create_user.py` should accept CLI args: `--email`, `--password`, `--role`.

Add Make targets:

```makefile
seed-owner:
	docker compose run --rm api python scripts/seed_owner.py

create-user:
	docker compose run --rm api python scripts/create_user.py --email "$(EMAIL)" --password "$(PASSWORD)" --role "$(ROLE)"
```

- [ ] **Step 6: Re-run the auth tests**

Run: `docker compose run --rm api pytest tests/auth/test_login.py -q`
Expected: PASS.

- [ ] **Step 7: Smoke-test owner bootstrap**

Run: `docker compose run --rm api python scripts/seed_owner.py`
Expected: PASS and one owner user exists.

- [ ] **Step 8: Commit**

```bash
git add api/app/core/security.py api/app/api/deps.py api/app/schemas/auth.py api/app/services/auth_service.py api/app/api/routes/auth.py api/scripts/seed_owner.py api/scripts/create_user.py api/tests/auth/test_login.py api/tests/conftest.py api/app/api/router.py Makefile README.md
git commit -m "feat: add session auth"
```

## Task 5: Implement People CRUD and Role Checks

**Files:**
- Create: `api/app/schemas/person.py`
- Create: `api/app/services/person_service.py`
- Create: `api/app/api/routes/people.py`
- Create: `api/tests/people/test_people_api.py`
- Modify: `api/app/api/router.py`

- [ ] **Step 1: Write the failing people API tests**

```python
def test_viewer_can_list_people(authenticated_viewer_client):
    ...


def test_viewer_cannot_create_people(authenticated_viewer_client):
    response = authenticated_viewer_client.post("/api/v1/people", json={"fullName": "New Person"})

    assert response.status_code == 403
```

Also add moderator create and update tests, plus validation for blank `fullName`.

- [ ] **Step 2: Run the people API tests and confirm they fail**

Run: `docker compose run --rm api pytest tests/people/test_people_api.py -q`
Expected: FAIL because people schemas, services, and routes do not exist yet.

- [ ] **Step 3: Implement read and write schemas**

```python
class PersonCreate(BaseModel):
    full_name: str
    birth_date: date | None = None
    death_date: date | None = None
    notes: str | None = None
```

Add matching response models with `from_attributes=True`.

- [ ] **Step 4: Implement the people routes**

Add:

- `GET /api/v1/people`
- `GET /api/v1/people/{person_id}`
- `POST /api/v1/people`
- `PATCH /api/v1/people/{person_id}`

Use route-level role checks so viewers are read-only and moderators/owners can write.

- [ ] **Step 5: Re-run the people API tests**

Run: `docker compose run --rm api pytest tests/people/test_people_api.py -q`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add api/app/schemas/person.py api/app/services/person_service.py api/app/api/routes/people.py api/tests/people/test_people_api.py api/app/api/router.py
git commit -m "feat: add people api"
```

## Task 6: Implement Relationship Rules and the Tree Payload

**Files:**
- Create: `api/app/schemas/relationship.py`
- Create: `api/app/schemas/tree.py`
- Create: `api/app/services/relationship_service.py`
- Create: `api/app/services/tree_service.py`
- Create: `api/app/api/routes/relationships.py`
- Create: `api/app/api/routes/tree.py`
- Create: `api/tests/relationships/test_relationship_rules.py`
- Create: `api/tests/tree/test_tree_api.py`
- Modify: `api/app/api/router.py`

- [ ] **Step 1: Write the failing relationship rule tests**

```python
def test_partner_relationship_is_canonicalized(authenticated_moderator_client):
    ...


def test_child_cannot_receive_more_than_two_parents(authenticated_moderator_client):
    ...


def test_parent_child_relationship_rejects_cycles(authenticated_moderator_client):
    ...
```

Add one more test that verifies deleting a relationship removes it from the tree payload.

- [ ] **Step 2: Run the relationship and tree tests and confirm they fail**

Run: `docker compose run --rm api pytest tests/relationships/test_relationship_rules.py tests/tree/test_tree_api.py -q`
Expected: FAIL because the services and routes do not exist yet.

- [ ] **Step 3: Implement relationship validation**

`relationship_service.py` should:

- normalize partner pairs so lower ID is always `source_person_id`
- reject duplicate partner pairs
- reject duplicate parent-child pairs
- reject more than two parents per child
- perform a DFS before insert to reject ancestry cycles

Core shape:

```python
def assert_no_parent_cycle(session: Session, parent_id: int, child_id: int) -> None:
    if parent_id == child_id:
        raise RelationshipRuleError("A person cannot be their own parent.")
```

- [ ] **Step 4: Implement the routes**

Add:

- `POST /api/v1/relationships`
- `DELETE /api/v1/relationships/{relationship_id}`
- `GET /api/v1/tree`

`GET /api/v1/tree` should return `viewerRole`, `people`, and `relationships` in one response.

- [ ] **Step 5: Re-run the relationship and tree tests**

Run: `docker compose run --rm api pytest tests/relationships/test_relationship_rules.py tests/tree/test_tree_api.py -q`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add api/app/schemas/relationship.py api/app/schemas/tree.py api/app/services/relationship_service.py api/app/services/tree_service.py api/app/api/routes/relationships.py api/app/api/routes/tree.py api/tests/relationships/test_relationship_rules.py api/tests/tree/test_tree_api.py api/app/api/router.py
git commit -m "feat: add relationship rules and tree api"
```

## Task 7: Scaffold the Vue Frontend and Auth Flow

**Files:**
- Create: `web/package.json`
- Create: `web/tsconfig.json`
- Create: `web/tsconfig.node.json`
- Create: `web/vite.config.ts`
- Create: `web/index.html`
- Create: `web/src/main.ts`
- Create: `web/src/App.vue`
- Create: `web/src/router.ts`
- Create: `web/src/app/session.ts`
- Create: `web/src/lib/fetchJson.ts`
- Create: `web/src/styles/index.css`
- Create: `web/src/features/auth/LoginPage.vue`
- Create: `web/src/features/auth/LoginPage.test.ts`
- Create: `web/src/test/setup.ts`
- Create: `web/src/test/renderApp.ts`
- Modify: `compose.yml`
- Modify: `Makefile`

- [ ] **Step 1: Write the failing login-page test**

```ts
it("submits credentials and redirects to /tree on success", async () => {
  render(LoginPage, {
    global: {
      plugins: [router],
    },
  });

  await user.type(screen.getByLabelText(/email/i), "owner@example.com");
  await user.type(screen.getByLabelText(/password/i), "secret");
  await user.click(screen.getByRole("button", { name: /sign in/i }));

  expect(mockPush).toHaveBeenCalledWith("/tree");
});
```

- [ ] **Step 2: Run the frontend auth test and confirm it fails**

Run: `docker compose run --rm web npm run test -- --run src/features/auth/LoginPage.test.ts`
Expected: FAIL because the Vite app and test runner do not exist yet.

- [ ] **Step 3: Add the frontend app shell**

`package.json` should include `vue`, `vue-router`, `typescript`, `vite`, `@vitejs/plugin-vue`, `vitest`, `@testing-library/vue`, `@testing-library/user-event`, `@vue/test-utils`, and `vue-tsc`.

`vite.config.ts` should proxy `/api` to `http://api:8000`.

- [ ] **Step 4: Add the login page and protected routing**

Implement:

- `/login`
- `/tree`
- a session bootstrap call to `GET /api/v1/auth/me`
- redirect unauthenticated users to `/login`

`fetchJson` must use `credentials: "include"`.

- [ ] **Step 5: Re-run the frontend auth test**

Run: `docker compose run --rm web npm run test -- --run src/features/auth/LoginPage.test.ts`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add web/package.json web/tsconfig.json web/tsconfig.node.json web/vite.config.ts web/index.html web/src compose.yml Makefile
git commit -m "feat: add frontend app shell"
```

## Task 8: Build the Tree Viewer and Person Details Panel

**Files:**
- Create: `web/src/features/tree/types.ts`
- Create: `web/src/features/tree/api.ts`
- Create: `web/src/features/tree/TreePage.vue`
- Create: `web/src/features/tree/components/FamilyTreeCanvas.vue`
- Create: `web/src/features/tree/components/PersonNode.vue`
- Create: `web/src/features/tree/layout/buildFamilyGraph.ts`
- Create: `web/src/features/tree/layout/buildFamilyGraph.test.ts`
- Create: `web/src/features/tree/layout/applyDagreLayout.ts`
- Create: `web/src/features/person/PersonDetailsPanel.vue`
- Create: `web/src/features/tree/TreePage.test.ts`
- Modify: `web/src/router.ts`
- Modify: `web/package.json`

- [ ] **Step 1: Write the failing tree layout and selection tests**

```ts
it("creates a synthetic family-unit node for a partner pair with children", () => {
  const graph = buildFamilyGraph(peopleFixture, relationshipsFixture);

  expect(graph.nodes.some((node) => node.type === "family-unit")).toBe(true);
});
```

```ts
it("opens the details panel when a person node is selected", async () => {
  render(TreePage);

  await user.click(await screen.findByRole("button", { name: /ada example/i }));

  expect(screen.getByText(/tree root/i)).toBeInTheDocument();
});
```

- [ ] **Step 2: Run the tree tests and confirm they fail**

Run: `docker compose run --rm web npm run test -- --run src/features/tree/layout/buildFamilyGraph.test.ts src/features/tree/TreePage.test.ts`
Expected: FAIL because tree code does not exist yet.

- [ ] **Step 3: Add the tree data pipeline**

`buildFamilyGraph.ts` should:

- group partner pairs into synthetic `family-unit` nodes
- connect `family-unit` nodes to child people
- create single-parent `family-unit` nodes when no partner edge exists

Core shape:

```ts
export function buildFamilyGraph(people: PersonDto[], relationships: RelationshipDto[]) {
  return {
    nodes: [],
    edges: [],
  };
}
```

- [ ] **Step 4: Add the canvas and details UI**

Use `@vue-flow/core`, `@vue-flow/background`, and `@vue-flow/controls` plus `dagre`.

`FamilyTreeCanvas.vue` should render:

- `<VueFlow />`
- `<Controls />`
- `<Background />`

`PersonDetailsPanel.vue` should show:

- full name
- birth/death dates
- notes
- partner and parent/child context inferred from loaded relationships

- [ ] **Step 5: Re-run the tree tests**

Run: `docker compose run --rm web npm run test -- --run src/features/tree/layout/buildFamilyGraph.test.ts src/features/tree/TreePage.test.ts`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add web/src/features/tree web/src/features/person/PersonDetailsPanel.vue web/src/router.ts web/package.json
git commit -m "feat: add tree viewer"
```

## Task 9: Add Moderator Editing and Quick-Jump Search

**Files:**
- Create: `web/src/features/search/PersonSearch.vue`
- Create: `web/src/features/editor/moderatorApi.ts`
- Create: `web/src/features/editor/EditPersonDrawer.vue`
- Create: `web/src/features/editor/RelationshipForm.vue`
- Create: `web/src/features/editor/EditPersonDrawer.test.ts`
- Modify: `web/src/features/tree/TreePage.vue`
- Modify: `web/src/features/person/PersonDetailsPanel.vue`

- [ ] **Step 1: Write the failing moderator UI tests**

```ts
it("shows moderator controls only for moderator sessions", async () => {
  render(TreePage, { sessionRole: "moderator" });

  expect(await screen.findByRole("button", { name: /add person/i })).toBeVisible();
});
```

```ts
it("filters the quick-jump list by deferred search text", async () => {
  render(PersonSearch, { props: { people: peopleFixture } });

  await user.type(screen.getByRole("searchbox"), "ada");

  expect(screen.getByRole("option", { name: /ada example/i })).toBeVisible();
});
```

- [ ] **Step 2: Run the moderator UI tests and confirm they fail**

Run: `docker compose run --rm web npm run test -- --run src/features/editor/EditPersonDrawer.test.ts`
Expected: FAIL because moderator components do not exist yet.

- [ ] **Step 3: Implement quick-jump search**

Use a reactive search `ref` plus a `computed` filtered list against the already-loaded `people` array. Do not add debounce logic in v1; the approved scale is under 100 people.

- [ ] **Step 4: Implement moderator-only forms**

`EditPersonDrawer.vue` should support create and update.

`RelationshipForm.vue` should support:

- add partner
- add parent-child
- remove existing relationship

On successful submit, refetch `GET /api/v1/tree`.

- [ ] **Step 5: Re-run the moderator UI tests**

Run: `docker compose run --rm web npm run test -- --run src/features/editor/EditPersonDrawer.test.ts`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add web/src/features/search/PersonSearch.vue web/src/features/editor web/src/features/tree/TreePage.vue web/src/features/person/PersonDetailsPanel.vue
git commit -m "feat: add moderator editing tools"
```

## Task 10: Add End-to-End Journeys, Smoke Coverage, and Final Docs

**Files:**
- Create: `web/playwright.config.ts`
- Create: `web/e2e/login.spec.ts`
- Create: `web/e2e/tree-viewer.spec.ts`
- Create: `web/e2e/moderator.spec.ts`
- Create: `api/scripts/seed_demo_data.py`
- Modify: `scripts/smoke.sh`
- Modify: `compose.yml`
- Modify: `Makefile`
- Modify: `README.md`

- [ ] **Step 1: Write the failing e2e and smoke checks**

Create Playwright specs for:

- login redirect
- empty-state tree render
- selecting a person opens details
- moderator adds a person and a relationship

Update `scripts/smoke.sh` to expect:

```bash
docker compose up -d db api web
docker compose run --rm api alembic upgrade head
docker compose run --rm api python scripts/seed_owner.py
docker compose run --rm api python scripts/seed_demo_data.py
curl -fsS http://localhost:8000/api/v1/health >/dev/null
```

- [ ] **Step 2: Run the e2e suite and confirm it fails**

Run: `docker compose run --rm e2e npm run e2e`
Expected: FAIL because Playwright config, seeded data, and/or service wiring are incomplete.

- [ ] **Step 3: Add the e2e service and scripts**

`compose.yml` should define `e2e` using the official Playwright Docker image pinned to the same version as `@playwright/test`.

`Makefile` should include:

```makefile
test-e2e:
	docker compose run --rm e2e npm run e2e

smoke:
	bash scripts/smoke.sh
```

- [ ] **Step 4: Re-run the e2e suite**

Run: `docker compose run --rm e2e npm run e2e`
Expected: PASS.

- [ ] **Step 5: Re-run the smoke script**

Run: `bash scripts/smoke.sh`
Expected: PASS.

- [ ] **Step 6: Update the README**

Document:

- local setup
- `make up` / `make down`
- `make migrate`
- `make seed-owner`
- `make create-user EMAIL=... PASSWORD=... ROLE=viewer`
- `make test`
- `make test-e2e`
- `make smoke`

- [ ] **Step 7: Run final verification**

Run: `make test`
Expected: PASS.

Run: `make test-e2e`
Expected: PASS.

Run: `make smoke`
Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add web/playwright.config.ts web/e2e api/scripts/seed_demo_data.py scripts/smoke.sh compose.yml Makefile README.md
git commit -m "test: add end-to-end and smoke coverage"
```

## Verification Checklist

- `docker compose config` passes
- `docker compose run --rm api pytest -q` passes
- `docker compose run --rm web npm run test -- --run` passes
- `docker compose run --rm e2e npm run e2e` passes
- `bash scripts/smoke.sh` passes
- `make test && make test-e2e && make smoke` passes

## References Used For Stack Choices

- FastAPI testing: https://fastapi.tiangolo.com/tutorial/testing/
- FastAPI cookie parameters: https://fastapi.tiangolo.com/tutorial/cookie-params/
- FastAPI security/password hashing: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- FastAPI Docker deployment: https://fastapi.tiangolo.com/deployment/docker/
- SQLAlchemy 2.0 ORM and tutorial: https://docs.sqlalchemy.org/20/tutorial/index.html
- PostgreSQL constraint guidance: https://www.postgresql.org/docs/current/ddl-constraints.html
- Vite guide and TypeScript notes: https://vite.dev/guide/ and https://vite.dev/guide/features
- Vue 3 introduction and SFC guidance: https://vuejs.org/guide/introduction
- Vue Router introduction: https://router.vuejs.org/introduction
- Vue Flow docs: https://vueflow.dev/
- Dagre project: https://github.com/dagrejs/dagre
- Playwright intro, Docker, and best practices: https://playwright.dev/docs/intro , https://playwright.dev/docs/docker , https://playwright.dev/docs/best-practices
