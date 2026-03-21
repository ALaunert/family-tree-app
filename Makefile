SHELL := /bin/bash

.PHONY: setup up down logs migrate seed-owner create-user test-api test-web test-e2e test smoke

setup:
	cp -n .env.example .env || true

up:
	docker compose up -d db api web

down:
	docker compose down --remove-orphans

logs:
	docker compose logs -f

migrate:
	docker compose exec api echo "TODO: run API migrations"

seed-owner:
	docker compose exec api echo "TODO: seed owner user"

create-user:
	docker compose exec api echo "TODO: create an application user"

test-api:
	docker compose exec api echo "TODO: run API tests"

test-web:
	docker compose exec web echo "TODO: run web tests"

test-e2e:
	docker compose exec web echo "TODO: run end-to-end tests"

test:
	$(MAKE) test-api
	$(MAKE) test-web

smoke:
	bash scripts/smoke.sh
