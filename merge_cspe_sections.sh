#!/usr/bin/env bash
# CSPE 키워드 노트를 섹션별로 나눠 작성한 뒤 하나의 파일로 합치는 도구.
#
# 사용법:
#   ./merge_cspe_sections.sh <섹션_폴더> <최종_md_경로> [--keep]
#
# <섹션_폴더>에는 다음 파일들이 있어야 한다(숫자 접두어 순서대로 이어붙임):
#   00_frontmatter.md   (--- title/date/tags/weight --- 블록)
#   01_개요.md           (## Ⅰ. 개요)
#   02_구성요소.md        (## Ⅱ. 구성요소)
#   03_절차.md           (## Ⅲ. 절차)
#   04_문제점.md          (## Ⅳ. 문제점)
#   05_개선방안.md         (## Ⅴ. 개선방안)
#   06_전망.md           (## Ⅵ. 전망)
#
# (골격은 content/exam/cs/model-answer.md 정본을 따른다 — 바뀌면 이 주석도 갱신)
#
# 각 섹션 파일을 서로 다른 에이전트가 개별로 작성해도(같은 파일을 동시에
# 쓰지 않으므로) 충돌이 없다. 합친 뒤 기본적으로 섹션 폴더는 삭제한다
# (--keep을 주면 유지).
#
# 이 스크립트는 zola build/CI에서 호출되지 않는다 — 저장소 구조는 그대로
# 단일 .md 파일이며, 이 스크립트는 작성 중에만 쓰는 보조 도구다.

set -euo pipefail

SRC_DIR="${1:?사용법: $0 <섹션_폴더> <최종_md_경로> [--keep]}"
TARGET="${2:?사용법: $0 <섹션_폴더> <최종_md_경로> [--keep]}"
KEEP="${3:-}"

if [[ ! -d "$SRC_DIR" ]]; then
  echo "오류: 섹션 폴더가 없음: $SRC_DIR" >&2
  exit 1
fi

FILES=$(find "$SRC_DIR" -maxdepth 1 -name '[0-9][0-9]_*.md' | sort)

if [[ -z "$FILES" ]]; then
  echo "오류: $SRC_DIR 안에 NN_이름.md 형식 파일이 없음" >&2
  exit 1
fi

mkdir -p "$(dirname "$TARGET")"
: > "$TARGET"

first=1
while IFS= read -r f; do
  if [[ $first -eq 0 ]]; then
    echo "" >> "$TARGET"
  fi
  cat "$f" >> "$TARGET"
  first=0
done <<< "$FILES"

# 파일 끝에 개행 하나 보장
[[ -s "$TARGET" ]] && [[ "$(tail -c1 "$TARGET")" != "" ]] && echo "" >> "$TARGET"

echo "합침 완료: $TARGET"
echo "$FILES" | sed 's/^/  - /'

if [[ "$KEEP" != "--keep" ]]; then
  rm -rf "$SRC_DIR"
  echo "섹션 폴더 삭제: $SRC_DIR"
fi
