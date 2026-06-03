#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
BASE = "/knowledge-base"
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(#[^\]|]+)?(?:\|([^\]]+))?\]\]")


def url_for(path: Path) -> str:
    rel = path.relative_to(CONTENT)
    if rel.name == "_index.md":
        parent = rel.parent.as_posix()
        suffix = "" if parent == "." else parent.strip("/") + "/"
    else:
        suffix = rel.with_suffix("").as_posix().strip("/") + "/"
    return f"{BASE}/{suffix}" if suffix else f"{BASE}/"


def markdown_escape_label(text: str) -> str:
    return text.replace("[", "\\[").replace("]", "\\]")


def build_lookup() -> dict[str, str]:
    lookup: dict[str, str] = {}
    for path in CONTENT.rglob("*.md"):
        if path.name == "_index.md":
            lookup.setdefault(path.parent.name, url_for(path))
        else:
            lookup.setdefault(path.stem, url_for(path))
    return lookup


def convert_line(line: str, lookup: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        raw_target = match.group(1).strip()
        anchor = match.group(2) or ""
        label = match.group(3) or Path(raw_target).stem
        label = markdown_escape_label(label)
        target_key = Path(raw_target).stem
        url = lookup.get(target_key)
        if not url:
            return label
        return f"[{label}]({url}{anchor})"

    return WIKILINK_RE.sub(replace, line)


def main() -> None:
    lookup = build_lookup()
    changed = 0
    for path in sorted(CONTENT.rglob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        out: list[str] = []
        in_fence = False
        for line in lines:
            stripped = line.lstrip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = not in_fence
                out.append(line)
                continue
            out.append(line if in_fence else convert_line(line, lookup))
        new_text = "".join(out)
        old_text = "".join(lines)
        if new_text != old_text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
    print(f"Converted wikilinks in {changed} files")


if __name__ == "__main__":
    main()
