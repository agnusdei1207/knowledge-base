#!/usr/bin/env bash
# ============================================================
# llms.txt 자동 생성 스크립트
# ============================================================
#
# 목적:
#   AI 에이전트(Claude, ChatGPT, Cursor 등)가 사이트를 방문할 때
#   /llms.txt 파일을 읽고 콘텐츠 구조를 빠르게 파악할 수 있도록 한다.
#   robots.txt가 크롤러용이라면, llms.txt는 AI 에이전트용 사이트맵이다.
#
# 표준 참조: https://llmstxt.org/
#
# 실행 시점: Quartz 빌드(npx quartz build) 완료 후
# 출력 위치: public/llms.txt
# ============================================================
set -euo pipefail

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
PUBLIC_DIR="${ROOT_DIR}/public"
CONTENT_DIR="${ROOT_DIR}/content"
OUTPUT="${PUBLIC_DIR}/llms.txt"

# public/ 디렉토리가 없으면 빌드가 안 된 것
if [ ! -d "$PUBLIC_DIR" ]; then
    echo "⚠️  public/ 디렉토리가 없습니다. 먼저 빌드를 실행하세요."
    exit 0
fi

echo "📝 Generating llms.txt..."

cat > "$OUTPUT" << 'HEADER'
# Knowledge Base

> 개인 학습(기술사 스터디 노트) · 사내 업무 문서 · AI 에이전트 지식 검색을 위한 Quartz v5 기반 지식 허브입니다.

## 사이트 정보

- URL: https://agnusdei1207.github.io/knowledge-base/
- 언어: 한국어 (ko-KR)
- 총 문서 수: 9,600+
- 주요 주제: 컴퓨터 구조, OS, 네트워크, SW공학, DB, ICT 융합, 엔터프라이즈, 알고리즘/통계, 보안, AI, 설계/감리, IT 경영, 클라우드, 데이터 엔지니어링, DevOps/SRE, 빅데이터

## 콘텐츠 구조

HEADER

# content/ 하위 1-2단계 디렉토리 구조를 마크다운 목록으로 출력
cd "$CONTENT_DIR"

# 최상위 섹션
for section_dir in $(find . -maxdepth 1 -type d | sort | tail -n +2); do
    section_name=$(basename "$section_dir")
    # _index.md에서 제목 추출 시도
    title=""
    if [ -f "${section_dir}/_index.md" ] || [ -f "${section_dir}/index.md" ]; then
        idx_file="${section_dir}/_index.md"
        [ ! -f "$idx_file" ] && idx_file="${section_dir}/index.md"
        title=$(grep -m1 "^title:" "$idx_file" 2>/dev/null | sed 's/^title:\s*//' | sed 's/^["'"'"']//;s/["'"'"']$//' || true)
    fi
    [ -z "$title" ] && title="$section_name"

    # 파일 수 카운트
    file_count=$(find "$section_dir" -name "*.md" -type f 2>/dev/null | wc -l)

    echo "- **${title}** (\`${section_name}/\`, ${file_count} docs)" >> "$OUTPUT"

    # 하위 섹션 (2단계)
    for sub_dir in $(find "$section_dir" -maxdepth 1 -type d | sort | tail -n +2); do
        sub_name=$(basename "$sub_dir")
        sub_title=""
        if [ -f "${sub_dir}/_index.md" ] || [ -f "${sub_dir}/index.md" ]; then
            sub_idx="${sub_dir}/_index.md"
            [ ! -f "$sub_idx" ] && sub_idx="${sub_dir}/index.md"
            sub_title=$(grep -m1 "^title:" "$sub_idx" 2>/dev/null | sed 's/^title:\s*//' | sed 's/^["'"'"']//;s/["'"'"']$//' || true)
        fi
        [ -z "$sub_title" ] && sub_title="$sub_name"

        sub_count=$(find "$sub_dir" -name "*.md" -type f 2>/dev/null | wc -l)
        echo "  - ${sub_title} (\`${section_name}/${sub_name}/\`, ${sub_count} docs)" >> "$OUTPUT"
    done
done

# 푸터
cat >> "$OUTPUT" << 'FOOTER'

## 접근 방법

- 웹 UI: https://agnusdei1207.github.io/knowledge-base/
- MCP 서버: `search_docs`, `get_doc`, `list_docs` 도구 제공
- 각 문서는 표준 Markdown + YAML frontmatter 형식

## 라이선스

개인 학습 목적으로 작성된 문서입니다.
FOOTER

# 파일 크기 출력
size=$(wc -c < "$OUTPUT")
lines=$(wc -l < "$OUTPUT")
echo "✅ llms.txt 생성 완료: ${lines}줄, ${size}바이트 → ${OUTPUT}"
