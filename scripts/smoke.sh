#!/usr/bin/env bash
set -euo pipefail

export API_PORT="${API_PORT:-8000}"
export WEB_PORT="${WEB_PORT:-5173}"

docker compose up -d db api web
docker compose run --rm api alembic upgrade head
docker compose run --rm api python scripts/seed_owner.py
docker compose run --rm api python scripts/seed_demo_data.py

for _ in {1..30}; do
  if curl -fsS "http://localhost:${API_PORT}/api/v1/health" >/dev/null; then
    exit 0
  fi
  sleep 1
done

curl -fsS "http://localhost:${API_PORT}/api/v1/health" >/dev/null
