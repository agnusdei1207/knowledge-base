#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUDYNOTE = ROOT / "content" / "studynote"

NUMBER_RE = re.compile(r"^(\d+)_")
SUBJECT_RE = re.compile(r"^\d{2}_")
TEMPLATE_PATTERNS = [
    "현대 정보시스템에서 점점 중요성이 커지고 있는 기술이다",
    "기존 방식에서는 수동적이고 반응적인 대응이 주를 이루었으나",
    "건물의 기초 공사와 같다",
    "자동 발송 시스템이다",
    "실행 효율을 높이는 기반 기술이다",
]
BOX_CHARS = set("┌┐└┘├┤┬┴┼─│╭╮╰╯═║╔╗╚╝╠╣╦╩╬▶▼▲◀→←↑↓")


def subject_dirs() -> list[Path]:
    return sorted(path for path in STUDYNOTE.iterdir() if path.is_dir() and SUBJECT_RE.match(path.name))


def numbered_files(subject: Path) -> dict[int, list[Path]]:
    result: dict[int, list[Path]] = {}
    for path in subject.rglob("*.md"):
        if path.name == "_index.md":
            continue
        match = NUMBER_RE.match(path.name)
        if not match:
            continue
        result.setdefault(int(match.group(1)), []).append(path)
    return result


def extract_code_blocks(text: str) -> list[tuple[int, str, str]]:
    blocks: list[tuple[int, str, str]] = []
    lines = text.splitlines()
    start = None
    fence = ""
    buf: list[str] = []
    for index, line in enumerate(lines, start=1):
        if line.startswith("```"):
            if start is None:
                start = index
                fence = line
                buf = []
            else:
                blocks.append((start, fence, "\n".join(buf)))
                start = None
                fence = ""
                buf = []
        elif start is not None:
            buf.append(line)
    if start is not None:
        blocks.append((start, fence, "\n".join(buf)))
    return blocks


def has_box_drawing(block: str) -> bool:
    return any(char in block for char in BOX_CHARS)


def likely_broken_ascii(block: str) -> bool:
    return has_box_drawing(block)


def audit_numbers() -> list[str]:
    rows = []
    for subject in subject_dirs():
        files_by_no = numbered_files(subject)
        if not files_by_no:
            rows.append(f"{subject.name}: no numbered files")
            continue
        numbers = sorted(files_by_no)
        missing = [no for no in range(numbers[0], numbers[-1] + 1) if no not in files_by_no]
        duplicates = {no: paths for no, paths in files_by_no.items() if len(paths) > 1}
        miss_preview = ", ".join(map(str, missing[:40]))
        if len(missing) > 40:
            miss_preview += f", ... (+{len(missing) - 40})"
        dup_preview = ", ".join(
            f"{no}x{len(paths)}:{'|'.join(path.relative_to(STUDYNOTE).as_posix() for path in paths[:3])}"
            for no, paths in sorted(duplicates.items())[:12]
        )
        rows.append(
            f"{subject.name}: files={sum(len(v) for v in files_by_no.values())} "
            f"unique={len(numbers)} range={numbers[0]}-{numbers[-1]} "
            f"missing={len(missing)} [{miss_preview}] duplicates={len(duplicates)} [{dup_preview}]"
        )
    return rows


def audit_templates(limit: int) -> list[str]:
    rows = []
    for path in sorted(STUDYNOTE.rglob("*.md")):
        if path.name == "_index.md":
            continue
        text = path.read_text(encoding="utf-8")
        hits = [pattern for pattern in TEMPLATE_PATTERNS if pattern in text]
        if hits:
            rows.append(f"{path.relative_to(ROOT)}: template_hits={len(hits)}")
            if len(rows) >= limit:
                break
    return rows


def audit_ascii(limit: int) -> list[str]:
    rows = []
    for path in sorted(STUDYNOTE.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        blocks = extract_code_blocks(text)
        for start, fence, block in blocks:
            if likely_broken_ascii(block):
                rows.append(f"{path.relative_to(ROOT)}:{start}: possible broken box ({fence})")
                break
        if len(rows) >= limit:
            break
    return rows


def audit_box_diagrams(limit: int) -> list[str]:
    rows = []
    for path in sorted(STUDYNOTE.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        blocks = extract_code_blocks(text)
        for start, fence, block in blocks:
            if has_box_drawing(block):
                width = max((len(line) for line in block.splitlines()), default=0)
                rows.append(f"{path.relative_to(ROOT)}:{start}: width={width} ({fence})")
                break
        if len(rows) >= limit:
            break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit study note numbering and quality markers.")
    parser.add_argument("--template-limit", type=int, default=80)
    parser.add_argument("--ascii-limit", type=int, default=80)
    parser.add_argument("--box-limit", type=int, default=0)
    args = parser.parse_args()

    print("## Numbering")
    print("\n".join(audit_numbers()))
    print("\n## Template candidates")
    template_rows = audit_templates(args.template_limit)
    print("\n".join(template_rows) if template_rows else "none")
    print("\n## ASCII box candidates")
    ascii_rows = audit_ascii(args.ascii_limit)
    print("\n".join(ascii_rows) if ascii_rows else "none")
    if args.box_limit:
        print("\n## Box drawing diagrams")
        box_rows = audit_box_diagrams(args.box_limit)
        print("\n".join(box_rows) if box_rows else "none")


if __name__ == "__main__":
    main()
