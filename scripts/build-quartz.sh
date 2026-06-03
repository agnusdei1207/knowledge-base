#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${1:-$ROOT_DIR/.quartz-build/public}"
BASE_DIR="${BASE_DIR:-/knowledge-base}"
NODE_IMAGE="${NODE_IMAGE:-node:24-alpine}"
QUARTZ_REF="${QUARTZ_REF:-v5}"
QUARTZ_TARBALL_URL="https://github.com/jackyzha0/quartz/archive/refs/heads/${QUARTZ_REF}.tar.gz"

# GitHub Actions 캐시 디렉토리 지원 (QUARTZ_SRC_CACHE 환경변수로 제어)
SRC_CACHE_DIR="${QUARTZ_SRC_CACHE:-}"
NPM_CACHE="${NPM_CACHE_DIR:-}"

# 임시 디렉토리 결정: 캐시 디렉토리가 있으면 재사용, 없으면 mktemp
if [ -n "$SRC_CACHE_DIR" ]; then
  TMP_DIR="$(realpath "$SRC_CACHE_DIR")"
  mkdir -p "$TMP_DIR"
  # 캐시 히트 여부 확인 (QUARTZ_SRC_CACHED=true 이면 재다운로드 스킵)
  SKIP_DOWNLOAD="${QUARTZ_SRC_CACHED:-false}"
else
  TMP_DIR="$(mktemp -d)"
  SKIP_DOWNLOAD="false"
fi

cleanup() {
  # 캐시 디렉토리 사용 시에는 삭제하지 않음
  if [ -z "$SRC_CACHE_DIR" ]; then
    chmod -R u+w "$TMP_DIR" 2>/dev/null || true
    rm -rf "$TMP_DIR" 2>/dev/null || true
  fi
}
trap cleanup EXIT

# Quartz 소스 다운로드 (캐시 히트 시 스킵)
if [ "$SKIP_DOWNLOAD" = "true" ] && [ -f "$TMP_DIR/package.json" ]; then
  echo "✅ Using cached Quartz ${QUARTZ_REF} source..."
else
  echo "⬇️  Downloading Quartz ${QUARTZ_REF}..."
  # 기존 소스 정리 (content/npm-cache 제외)
  find "$TMP_DIR" -mindepth 1 -maxdepth 1 \
    ! -name 'content' \
    ! -name '.npm-cache' \
    ! -name 'node_modules' \
    -exec rm -rf {} + 2>/dev/null || true
  curl -fsSL "$QUARTZ_TARBALL_URL" | tar -xz -C "$TMP_DIR" --strip-components=1
fi

# 콘텐츠 최신화 (항상 덮어씀)
rm -rf "$TMP_DIR/content"
cp -R "$ROOT_DIR/content" "$TMP_DIR/content"
cp "$ROOT_DIR/quartz.config.yaml" "$TMP_DIR/quartz.config.yaml"

USE_DOCKER="${USE_DOCKER:-true}"

if [ "$USE_DOCKER" = "true" ]; then
  echo "🐳 Building Quartz in ${NODE_IMAGE}..."
  docker run --rm \
    -e QUARTZ_BASE_DIR="$BASE_DIR" \
    -e HOST_UID="$(id -u)" \
    -e HOST_GID="$(id -g)" \
    -e npm_config_cache=/work/.npm-cache \
    -v "$TMP_DIR:/work" \
    -w /work \
    "$NODE_IMAGE" \
    sh -lc 'apk add --no-cache coreutils git >/dev/null && npm ci && npx quartz plugin install --from-config --concurrency 1 && npx quartz build --baseDir "$QUARTZ_BASE_DIR" --output public && chown -R "$HOST_UID:$HOST_GID" /work'
else
  echo "🔨 Building Quartz (Native Mode)..."
  cd "$TMP_DIR"

  # npm 캐시 경로 설정 (GitHub Actions 캐시 연동)
  if [ -n "$NPM_CACHE" ]; then
    mkdir -p "$ROOT_DIR/$NPM_CACHE"
    npm ci --cache "$ROOT_DIR/$NPM_CACHE" --prefer-offline
  else
    npm ci
  fi

  npx quartz plugin install --from-config --concurrency 1
  npx quartz build --baseDir "$BASE_DIR" --output public
  cd "$ROOT_DIR"
fi

mkdir -p "$OUTPUT_DIR"
rm -rf "$OUTPUT_DIR"/*
cp -R "$TMP_DIR/public/." "$OUTPUT_DIR/"

if [ -d "$ROOT_DIR/static" ]; then
  cp -R "$ROOT_DIR/static/." "$OUTPUT_DIR/"
fi

echo "✅ Built site into $OUTPUT_DIR"
