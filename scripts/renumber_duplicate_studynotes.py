#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUDYNOTE = ROOT / "content" / "studynote"
NUMBER_RE = re.compile(r"^(\d+)_")
TITLE_RE = re.compile(r'^(title\s*=\s*")(\d+)(\.\s*)', re.MULTILINE)
HEADING_RE = re.compile(r"^(#\s+)(\d+)(\.\s*)", re.MULTILINE)


def numbered_files(subject: Path) -> dict[int, list[Path]]:
    files_by_no: dict[int, list[Path]] = {}
    for path in subject.rglob("*.md"):
        if path.name == "_index.md":
            continue
        match = NUMBER_RE.match(path.name)
        if match:
            files_by_no.setdefault(int(match.group(1)), []).append(path)
    return files_by_no


def url_for(path: Path) -> str:
    rel = path.relative_to(STUDYNOTE).with_suffix("").as_posix()
    return f"/knowledge-base/studynote/{rel}/"


def replace_number_markers(text: str, old_no: int, new_no: int) -> str:
    text = TITLE_RE.sub(lambda m: f"{m.group(1)}{new_no}{m.group(3)}", text, count=1)
    text = HEADING_RE.sub(lambda m: f"{m.group(1)}{new_no}{m.group(3)}", text, count=1)
    return text


def build_renames(subject: Path) -> dict[Path, tuple[Path, int, int]]:
    files_by_no = numbered_files(subject)
    if not files_by_no:
        return {}
    next_no = max(files_by_no) + 1
    renames: dict[Path, tuple[Path, int, int]] = {}
    for old_no, paths in sorted(files_by_no.items()):
        if len(paths) < 2:
            continue
        for path in sorted(paths)[1:]:
            suffix = path.name.split("_", 1)[1]
            width = max(3, len(str(next_no)))
            new_path = path.with_name(f"{next_no:0{width}d}_{suffix}")
            if new_path.exists():
                raise FileExistsError(f"target already exists: {new_path}")
            renames[path] = (new_path, old_no, next_no)
            next_no += 1
    return renames


def apply_renames(renames: dict[Path, tuple[Path, int, int]], dry_run: bool) -> None:
    url_map = {url_for(old): url_for(new) for old, (new, _, _) in renames.items()}

    for old, (new, old_no, new_no) in renames.items():
        text = old.read_text(encoding="utf-8")
        text = replace_number_markers(text, old_no, new_no)
        if not dry_run:
            old.write_text(text, encoding="utf-8")
            old.rename(new)

    if dry_run:
        return

    for path in sorted(STUDYNOTE.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        updated = text
        for old_url, new_url in url_map.items():
            updated = updated.replace(old_url, new_url)
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Renumber duplicate study note files after each subject range.")
    parser.add_argument("subjects", nargs="+", help="Subject directory names, e.g. 04_software_engineering")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    all_renames: dict[Path, tuple[Path, int, int]] = {}
    for name in args.subjects:
        subject = STUDYNOTE / name
        if not subject.is_dir():
            raise NotADirectoryError(subject)
        renames = build_renames(subject)
        all_renames.update(renames)
        print(f"{name}: {len(renames)} duplicate files to renumber")
        for old, (new, old_no, new_no) in list(renames.items())[:20]:
            print(f"  {old.relative_to(STUDYNOTE)} {old_no} -> {new_no} ({new.name})")
        if len(renames) > 20:
            print(f"  ... (+{len(renames) - 20})")

    apply_renames(all_renames, args.dry_run)


if __name__ == "__main__":
    main()
