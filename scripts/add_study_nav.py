#!/usr/bin/env python3
"""
Study note에 이전/다음 글 자동 네비게이션 추가.

규칙:
- studynote/ 아래의 .md 파일만 처리
- 파일명 prefix(001_, 002_, ...) 기준으로 정렬
- 각 노트에 "← 이전 | 다음 →" 블록을 본문 끝에 추가
- 이미 있으면 (감지: "## 🔗 이전/다음 글" 존재) 업데이트
"""

import os
import re
from pathlib import Path

CONTENT_DIR = Path("content/studynote")
NAV_HEADER = "## 🔗 이전/다음 글 (Navigation)"


def get_study_notes(folder: Path) -> list[Path]:
    """폴더 내 .md 파일을 prefix 기준으로 정렬해서 반환"""
    notes = []
    for md in folder.rglob("*.md"):
        if md.name == "index.md" or md.name.startswith("_"):
            continue
        notes.append(md)
    # 파일명 prefix (001_, 002_, ...) 기준 정렬
    notes.sort(key=lambda p: p.stem)
    return notes


def prev_next_links(notes: list[Path], current: Path) -> tuple[str | None, str | None]:
    """이전/다음 노트의 wiki 링크와 표시 텍스트 반환"""
    try:
        idx = notes.index(current)
    except ValueError:
        return None, None
    prev_note = notes[idx - 1] if idx > 0 else None
    next_note = notes[idx + 1] if idx < len(notes) - 1 else None
    return prev_note, next_note


def make_nav_block(prev: Path | None, next: Path | None, all_count: int, idx: int) -> str:
    """이전/다음 글 블록 생성"""
    lines = [
        "",
        "---",
        "",
        NAV_HEADER,
        "",
        f"**진행 상황**: {idx + 1} / {all_count}",
        "",
    ]

    if prev is None:
        lines.append("← **이전**: (첫 번째 글입니다)")
    else:
        prev_name = prev.stem
        prev_title = extract_title(prev) or prev_name
        lines.append(f"← **이전**: [[{prev_name}|{prev_title}]]")

    if next is None:
        lines.append("")
        lines.append("✅ **마지막 글입니다.**")
    else:
        next_name = next.stem
        next_title = extract_title(next) or next_name
        if prev is None:
            lines.append("")
        lines.append(f"**다음**: [[{next_name}|{next_title}]] →")

    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def extract_title(md_path: Path) -> str | None:
    """frontmatter에서 title 추출"""
    try:
        text = md_path.read_text(encoding="utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if m:
            fm = m.group(1)
            tm = re.search(r"^title:\s*['\"]?(.+?)['\"]?\s*$", fm, re.MULTILINE)
            if tm:
                return tm.group(1).strip()
    except Exception:
        pass
    return None


def update_note(md_path: Path, nav_block: str) -> bool:
    """노트에 nav 블록 추가 또는 업데이트"""
    text = md_path.read_text(encoding="utf-8")

    # 기존 nav 블록이 있으면 제거
    pattern = re.compile(
        r"\n*---\n*\n+## 🔗 이전/다음 글 \(Navigation\).*?(?=\n*---|\Z)",
        re.DOTALL,
    )
    text = pattern.sub("", text)
    # 끝의 trailing whitespace 정리
    text = text.rstrip() + "\n"

    # 새 nav 블록 추가
    text = text + nav_block

    md_path.write_text(text, encoding="utf-8")
    return True


def main():
    folders = sorted([p for p in CONTENT_DIR.iterdir() if p.is_dir()])
    total_updated = 0
    for folder in folders:
        notes = get_study_notes(folder)
        if not notes:
            continue
        for idx, note in enumerate(notes):
            prev, next = prev_next_links(notes, note)
            nav_block = make_nav_block(prev, next, len(notes), idx)
            update_note(note, nav_block)
            total_updated += 1
        print(f"  ✅ {folder.name}: {len(notes)}개 노트 업데이트")

    print(f"\n🎉 완료: 총 {total_updated}개 노트에 네비게이션 추가")


if __name__ == "__main__":
    main()
