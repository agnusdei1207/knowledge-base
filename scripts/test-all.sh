#!/usr/bin/env bash
# scripts/test-all.sh
# This script runs all build verification tests to ensure changes do not break the project.
set -euo pipefail

# Locate repository root
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==========================================="
echo "  Running Project Build Tests"
echo "==========================================="

# 1. Build MCP server docker image
echo "⏳ [1/2] Testing MCP Server Docker build..."
if docker build -f "$ROOT_DIR/docker/knowledgebase-mcp.Dockerfile" -t knowledgebase-mcp:test "$ROOT_DIR"; then
  echo "✅ MCP Server Docker build succeeded!"
else
  echo "❌ MCP Server Docker build failed!"
  exit 1
fi

echo "-------------------------------------------"

# 2. Build Quartz static site
echo "⏳ [2/2] Testing Quartz static site build..."
if bash "$ROOT_DIR/scripts/build-quartz.sh" "$ROOT_DIR/.quartz-build/public"; then
  echo "✅ Quartz static site build succeeded!"
else
  echo "❌ Quartz static site build failed!"
  exit 1
fi

echo "==========================================="
echo "🎉 All build tests passed successfully!"
echo "==========================================="
