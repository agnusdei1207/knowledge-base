#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

FENCE_RE = re.compile(r"(^[ \t]*(```|~~~)([^\n]*)\n)(.*?)(^[ \t]*\2[ \t]*$)", re.MULTILINE | re.DOTALL)
TEXT_FENCE_LANGS = {"", "text", "txt", "ascii", "markdown", "md"}
BOX_CHARS = "┌┐└┘├┤┬┴┼─│╭╮╰╯═║╔╗╚╝╠╣╦╩╬"
CONNECTOR_CHARS = set("│|/\\─━═-_=+<>→←↑↓▲▼▶◀┬┴┼┌┐└┘├┤")
ARROW_RE = re.compile(r"(--?>|<--?|<->|={2,}>|→|←|↑|↓|▲|▼|▶|◀|⇄|⇒|⇐)")
BRACKET_NODE_RE = re.compile(r"(\[[^\[\]\n]{1,180}\])")


def is_text_fence(info: str) -> bool:
    lang = info.strip().split(maxsplit=1)[0].lower() if info.strip() else ""
    return lang in TEXT_FENCE_LANGS


def diagram_score(text: str) -> int:
    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) < 2:
        return 0
    box_score = sum(text.count(ch) for ch in BOX_CHARS)
    ascii_boxes = len(re.findall(r"\+[=-]{3,}\+", text))
    pipe_lines = sum(1 for line in lines if line.count("|") >= 2 or line.count("│") >= 2)
    arrows = len(ARROW_RE.findall(text))
    tree = len(re.findall(r"(^|\n)\s*[├└]\S*", text))
    if box_score >= 8:
        return box_score + arrows + pipe_lines
    if ascii_boxes and pipe_lines >= 2:
        return 10 + ascii_boxes + pipe_lines
    if arrows >= 2 and len(lines) >= 3:
        return 8 + arrows
    if tree >= 2:
        return 8 + tree
    return 0


def is_border_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if len(stripped) < 3:
        return False
    return all(ch in CONNECTOR_CHARS or ch.isspace() for ch in stripped) and not re.search(r"[가-힣A-Za-z0-9]", stripped)


def clean_segment(text: str) -> str:
    text = text.strip()
    text = text.strip("│|║┃")
    text = re.sub(r"[┌┐└┘├┤┬┴┼╭╮╰╯╔╗╚╝╠╣╦╩╬]+", " ", text)
    text = re.sub(r"[─━═]{3,}", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def html_attrs(classes: str) -> str:
    return f'class="{classes}"'


def div(classes: str, content: str) -> str:
    return f"<div {html_attrs(classes)}>{content}</div>"


def node(text: str, kind: str = "node") -> str:
    return div(f"kb-diagram-{kind}", html.escape(text, quote=False))


def connector(text: str = "↓") -> str:
    label = clean_segment(text)
    if not label or not re.search(r"[→←↑↓▲▼▶◀<>-]", label):
        label = "↓"
    label = label.replace("-->", "→").replace("->", "→").replace("<--", "←")
    return div("kb-diagram-connector", html.escape(label, quote=False))


def row_from_brackets(line: str) -> str | None:
    parts: list[str] = []
    pos = 0
    matches = list(BRACKET_NODE_RE.finditer(line))
    if not matches:
        return None
    for match in matches:
        between = line[pos:match.start()]
        if ARROW_RE.search(between):
            parts.append(connector(ARROW_RE.search(between).group(0)))
        elif clean_segment(between):
            parts.append(node(clean_segment(between), "note"))
        raw = match.group(0)[1:-1].strip()
        if raw:
            parts.append(node(raw))
        pos = match.end()
    tail = line[pos:]
    arrow = ARROW_RE.search(tail)
    if arrow:
        parts.append(connector(arrow.group(0)))
        remaining = clean_segment(tail[arrow.end():])
        if remaining:
            parts.append(node(remaining, "note"))
    elif clean_segment(tail):
        parts.append(node(clean_segment(tail), "note"))
    return div("kb-diagram-row", "".join(parts)) if parts else None


def row_from_columns(line: str) -> str | None:
    normalized = line.replace("│", "|").strip()
    if normalized.count("|") < 2:
        return None
    cols = [clean_segment(part) for part in normalized.strip("|").split("|")]
    cols = [col for col in cols if col]
    if not cols:
        return None
    return div("kb-diagram-row kb-diagram-grid-row", "".join(node(col, "cell") for col in cols))


def row_from_tree(line: str) -> str | None:
    match = re.match(r"^(\s*)([├└]?[─\-]*[>►]?\s*)(.+)$", line)
    if not match:
        return None
    prefix = match.group(2)
    if not any(ch in prefix for ch in "├└─->►"):
        return None
    depth = min(len(match.group(1).replace("\t", "    ")) // 2, 8)
    text = clean_segment(match.group(3))
    if not text:
        return None
    return f'<div class="kb-diagram-tree-item" style="--depth:{depth}">{html.escape(text, quote=False)}</div>'


def convert_diagram(text: str) -> str:
    rows: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or is_border_line(line):
            continue
        rendered = row_from_brackets(line)
        if rendered is None:
            rendered = row_from_columns(line)
        if rendered is None:
            rendered = row_from_tree(line)
        if rendered is None:
            cleaned = clean_segment(line)
            if not cleaned:
                continue
            if ARROW_RE.fullmatch(cleaned) or set(cleaned) <= CONNECTOR_CHARS:
                rendered = connector(cleaned)
            else:
                rendered = node(cleaned, "note")
        rows.append(rendered)

    if not rows:
        rows.append(node("Diagram", "note"))

    return "\n".join(
        [
            '<div class="kb-diagram" data-diagram="ascii-converted">',
            '<div class="kb-diagram-flow">',
            *rows,
            "</div>",
            "</div>",
        ]
    )


def convert_file(path: Path, limit: int | None = None) -> tuple[bool, int]:
    text = path.read_text(encoding="utf-8")
    converted = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal converted
        opener, _, info, body, _closer = match.groups()
        if limit is not None and converted >= limit:
            return match.group(0)
        if not is_text_fence(info):
            return match.group(0)
        if "kb-diagram" in body:
            return match.group(0)
        if diagram_score(body) < 8:
            return match.group(0)
        converted += 1
        return "\n\n" + convert_diagram(body) + "\n\n"

    new = FENCE_RE.sub(replace, text)
    if new != text:
        path.write_text(new, encoding="utf-8")
    return new != text, converted


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert ASCII-art Markdown fences to responsive HTML diagrams.")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of blocks to convert globally.")
    parser.add_argument("--dry-run", action="store_true", help="Only report candidate count.")
    args = parser.parse_args()

    changed = 0
    converted = 0
    for path in sorted(CONTENT.rglob("*.md")):
        if not path.exists():
            continue
        if args.dry_run:
            text = path.read_text(encoding="utf-8")
            for match in FENCE_RE.finditer(text):
                if is_text_fence(match.group(3)) and diagram_score(match.group(4)) >= 8:
                    converted += 1
            continue
        remaining = None if args.limit is None else max(args.limit - converted, 0)
        if remaining == 0:
            break
        did_change, count = convert_file(path, remaining)
        converted += count
        if did_change:
            changed += 1
    if args.dry_run:
        print(f"ASCII diagram candidates: {converted}")
    else:
        print(f"Converted {converted} ASCII diagram blocks in {changed} files")


if __name__ == "__main__":
    main()
