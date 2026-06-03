#!/bin/sh
set -eu

WORKSPACE="${WORKSPACE:-/workspace}"
BUILD_DIR="${BUILD_DIR:-/tmp/quartz-preview}"
PORT="${PORT:-8080}"
WS_PORT="${WS_PORT:-3001}"
BASE_DIR="${BASE_DIR:-/}"
QUARTZ_REF="${QUARTZ_REF:-v5}"
QUARTZ_TARBALL_URL="https://github.com/jackyzha0/quartz/archive/refs/heads/${QUARTZ_REF}.tar.gz"

apk add --no-cache coreutils curl git tar >/dev/null

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

echo "Downloading Quartz ${QUARTZ_REF}..."
curl -fsSL "$QUARTZ_TARBALL_URL" | tar -xz -C "$BUILD_DIR" --strip-components=1

rm -rf "$BUILD_DIR/content"
cp -R "$WORKSPACE/content" "$BUILD_DIR/content"
cp "$WORKSPACE/quartz.config.yaml" "$BUILD_DIR/quartz.config.yaml"

cd "$BUILD_DIR"
echo "Starting Quartz preview on port ${PORT}..."
export npm_config_cache="$BUILD_DIR/.npm-cache"
npm ci
npx quartz plugin install --from-config --concurrency 1

if [ -d "$WORKSPACE/static" ]; then
  (
    while true; do
      if [ -d "$BUILD_DIR/public" ]; then
        cp -R "$WORKSPACE/static/." "$BUILD_DIR/public/"
      fi
      sleep 2
    done
  ) &
fi

npx quartz build --serve --port "$PORT" --wsPort "$WS_PORT" --baseDir "$BASE_DIR"
