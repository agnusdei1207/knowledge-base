#!/usr/bin/env bash
# 정적 사이트 빌드 (로컬 테스트용)
# 사용: bash scripts/build-site.sh
set -euo pipefail

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "Installing npm dependencies..."
npm ci

echo "Building Zola site and Pagefind index..."
npm run build

echo "Built into ${ROOT_DIR}/public"
