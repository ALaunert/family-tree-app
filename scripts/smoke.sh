#!/usr/bin/env bash
set -euo pipefail

docker compose -f compose.yml config >/dev/null
grep -q '^up:' Makefile
grep -q '^test:' Makefile
test -f api/Dockerfile
test -f web/Dockerfile
