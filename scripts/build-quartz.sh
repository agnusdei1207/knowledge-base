#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${1:-$ROOT_DIR/.quartz-build/public}"
BASE_DIR="${BASE_DIR:-/knowledge-base}"
NODE_IMAGE="${NODE_IMAGE:-node:alpine}"
QUARTZ_REF="${QUARTZ_REF:-v5}"
QUARTZ_TARBALL_URL="https://github.com/jackyzha0/quartz/archive/refs/heads/${QUARTZ_REF}.tar.gz"
TMP_DIR="$(mktemp -d)"

cleanup() {
  chmod -R u+w "$TMP_DIR" 2>/dev/null || true
  rm -rf "$TMP_DIR" 2>/dev/null || true
}

trap cleanup EXIT

echo "Downloading Quartz ${QUARTZ_REF}..."
curl -fsSL "$QUARTZ_TARBALL_URL" | tar -xz -C "$TMP_DIR" --strip-components=1

rm -rf "$TMP_DIR/content"
cp -R "$ROOT_DIR/content" "$TMP_DIR/content"
cp "$ROOT_DIR/quartz.config.yaml" "$TMP_DIR/quartz.config.yaml"

echo "Building Quartz in ${NODE_IMAGE}..."
docker run --rm \
  -e QUARTZ_BASE_DIR="$BASE_DIR" \
  -e HOST_UID="$(id -u)" \
  -e HOST_GID="$(id -g)" \
  -e npm_config_cache=/work/.npm-cache \
  -v "$TMP_DIR:/work" \
  -w /work \
  "$NODE_IMAGE" \
  sh -lc 'apk add --no-cache coreutils git >/dev/null && npm ci && npx quartz plugin install --from-config --concurrency 1 && npx quartz build --baseDir "$QUARTZ_BASE_DIR" --output public && chown -R "$HOST_UID:$HOST_GID" /work'

mkdir -p "$OUTPUT_DIR"
rm -rf "$OUTPUT_DIR"/*
cp -R "$TMP_DIR/public/." "$OUTPUT_DIR/"

if [ -d "$ROOT_DIR/static" ]; then
  cp -R "$ROOT_DIR/static/." "$OUTPUT_DIR/"
fi

echo "Built site into $OUTPUT_DIR"
