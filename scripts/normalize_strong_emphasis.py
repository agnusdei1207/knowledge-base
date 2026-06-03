#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

STRONG_RE = re.compile(r"(?<!\*)\*\*([^*\n]+?)\*\*(?!\*)")
HANGUL_RE = re.compile(r"[가-힣]")
INLINE_UNSAFE_RE = re.compile(r"(\[[^\]]+\]\([^)]+\)|`|\$|<[^>]+>)")
MARKDOWN_LINK_RE = re.compile(r"^\[([^\]]+)\]\(([^)]+)\)$")
MARKDOWN_LINK_TOKEN_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
INLINE_CODE_TOKEN_RE = re.compile(r"`([^`]+)`")


def render_strong_inner(inner: str) -> str | None:
    if "$" in inner or "<" in inner or ">" in inner:
        return None
    placeholders: list[str] = []

    def put(value: str) -> str:
        placeholders.append(value)
        return f"\u0000{len(placeholders) - 1}\u0000"

    def replace_link(match: re.Match[str]) -> str:
        label, href = match.groups()
        return put(f'<a href="{href}">{label}</a>')

    def replace_code(match: re.Match[str]) -> str:
        return put(f"<code>{match.group(1)}</code>")

    text = MARKDOWN_LINK_TOKEN_RE.sub(replace_link, inner)
    text = INLINE_CODE_TOKEN_RE.sub(replace_code, text)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    for idx, value in enumerate(placeholders):
        text = text.replace(f"\u0000{idx}\u0000", value)
    return text


def normalize_body(text: str) -> str:
    out: list[str] = []
    in_fence = False
    in_html_block = False
    lines = text.splitlines(keepends=True)
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out.append(line)
            index += 1
            continue

        lower = stripped.lower()
        if lower.startswith(("<div", "<section", "<table", "<pre", "<script", "<style")):
            in_html_block = True
        if in_fence or in_html_block:
            out.append(line)
            if in_html_block and re.search(r"</(div|section|table|pre|script|style)>", lower):
                in_html_block = False
            index += 1
            continue

        def replace(match: re.Match[str]) -> str:
            inner = match.group(1)
            next_char = line[match.end()] if match.end() < len(line) else ""
            prev_char = line[match.start() - 1] if match.start() > 0 else ""
            adjacent_to_korean = bool(HANGUL_RE.match(next_char) or HANGUL_RE.match(prev_char))
            contains_structured_inline = bool(MARKDOWN_LINK_TOKEN_RE.search(inner) or INLINE_CODE_TOKEN_RE.search(inner))
            if not adjacent_to_korean and not contains_structured_inline:
                return match.group(0)
            link_match = MARKDOWN_LINK_RE.match(inner)
            if link_match:
                label, href = link_match.groups()
                return f'<strong><a href="{href}">{label}</a></strong>'
            rendered = render_strong_inner(inner)
            if rendered is not None and contains_structured_inline:
                return f"<strong>{rendered}</strong>"
            if INLINE_UNSAFE_RE.search(inner):
                return match.group(0)
            return f"<strong>{inner}</strong>"

        out.append(STRONG_RE.sub(replace, line))
        index += 1

    return "".join(out)


def main() -> None:
    changed = 0
    replacements = 0
    for path in sorted(CONTENT.rglob("*.md")):
        if not path.exists():
            continue
        old = path.read_text(encoding="utf-8")
        new = normalize_body(old)
        if new != old:
            replacements += old.count("**") - new.count("**")
            path.write_text(new, encoding="utf-8")
            changed += 1
    print(f"Normalized strong emphasis in {changed} files")
    print(f"Approximate delimiter pairs removed: {replacements // 2}")


if __name__ == "__main__":
    main()
