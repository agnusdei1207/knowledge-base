#!/bin/sh
# 로컬 Docker에서 Quartz 라이브 서버 실행
# docker-compose.yml의 quartz-server 서비스 entrypoint
set -eu

WORKSPACE="${WORKSPACE:-/workspace}"
PORT="${PORT:-8080}"
WS_PORT="${WS_PORT:-3001}"
BASE_DIR="${BASE_DIR:-/}"

cd "$WORKSPACE"

echo "Installing npm dependencies..."
npm ci

echo "Installing Quartz plugins..."
npx quartz plugin install

echo "Starting Quartz on port ${PORT}..."
exec npx quartz build --serve --port "$PORT" --wsPort "$WS_PORT" --baseDir "$BASE_DIR"
