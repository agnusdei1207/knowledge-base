#!/usr/bin/env bash
# 정적 사이트 빌드 (로컬 테스트용)
# 사용: bash scripts/build-quartz.sh [출력경로]
set -euo pipefail

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${1:-$ROOT_DIR/public}"

cd "$ROOT_DIR"

echo "Installing npm dependencies..."
npm ci

echo "Installing Quartz plugins..."
npx quartz plugin install

echo "Building Quartz..."
NODE_OPTIONS="--max-old-space-size=4096" npx quartz build

echo "✅ Built into $OUTPUT_DIR"
