SHELL := /bin/bash

.PHONY: setup up down logs migrate seed-owner create-user test-api test-web test-e2e test smoke

setup:
	if [ ! -f .env ]; then cp .env.example .env; fi

up:
	docker compose up -d db api web

down:
	docker compose down --remove-orphans

logs:
	docker compose logs -f

migrate:
	docker compose run --rm api alembic upgrade head

seed-owner:
	docker compose run --rm api python scripts/seed_owner.py

create-user:
	docker compose run --rm api python scripts/create_user.py --email "$(EMAIL)" --password "$(PASSWORD)" --role "$(ROLE)"

test-api:
	docker compose run --rm api pytest -q

test-web:
	docker compose exec web echo "TODO: run web tests"

test-e2e:
	docker compose exec web echo "TODO: run end-to-end tests"

test:
	$(MAKE) test-api
	$(MAKE) test-web

smoke:
	bash scripts/smoke.sh
