#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"


def toml_string(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\\", "\\\\").replace('"', '\\"')
    text = text.replace("\n", "\\n")
    return f'"{text}"'


def toml_bool(value: Any) -> str:
    return "true" if bool(value) else "false"


def toml_array(values: Any) -> str:
    if values is None:
        return "[]"
    if not isinstance(values, list):
        values = [values]
    return "[" + ", ".join(toml_string(v) for v in values if v is not None) + "]"


def date_literal(value: Any) -> str | None:
    if isinstance(value, (dt.date, dt.datetime)):
        return value.date().isoformat() if isinstance(value, dt.datetime) else value.isoformat()
    if isinstance(value, str):
        text = value.strip().strip("'\"")
        try:
            dt.date.fromisoformat(text[:10])
            return text[:10]
        except ValueError:
            return None
    return None


def split_frontmatter(text: str) -> tuple[dict[str, Any], str] | None:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None
    end = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end = idx
            break
    if end is None:
        return None
    raw = "".join(lines[1:end])
    body = "".join(lines[end + 1 :])
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        data = {}
    return data, body


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


def normalize_diagram_html_line(line: str) -> str:
    def replace_strong(match: re.Match[str]) -> str:
        rendered = render_strong_inner(match.group(1))
        if rendered is None:
            rendered = match.group(1)
        return f"<strong>{rendered}</strong>"

    line = STRONG_RE.sub(replace_strong, line)
    line = INLINE_CODE_TOKEN_RE.sub(r"<code>\1</code>", line)
    return line


def is_diagram_marker(text: str, index: int) -> bool:
    prev_char = text[index - 1] if index > 0 else ""
    next_index = index + 2
    next_char = text[next_index] if next_index < len(text) else ""
    if prev_char == "*" or next_char == "*":
        return False
    if prev_char.isdigit() and next_char.isdigit():
        return False
    if prev_char in {"/", "-"} or next_char in {"/", "-"}:
        return False
    return True


def normalize_diagram_block(block: str) -> str:
    block = block.replace("<strong>", "").replace("</strong>", "")
    block = STRONG_RE.sub(lambda match: match.group(1), block)
    block = INLINE_CODE_TOKEN_RE.sub(r"<code>\1</code>", block)
    positions = [m.start() for m in re.finditer(r"\*\*", block) if is_diagram_marker(block, m.start())]
    if not positions:
        return block

    out: list[str] = []
    last = 0
    for pos in positions:
        out.append(block[last:pos])
        last = pos + 2
    out.append(block[last:])
    return "".join(out)


def normalize_strong_emphasis(body: str) -> str:
    """Fix Zola/CommonMark emphasis spans that fail next to Korean particles."""
    out: list[str] = []
    in_fence = False
    in_html_block = False
    lines = body.splitlines(keepends=True)
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out.append(line)
            index += 1
            continue

        if not in_fence and stripped.startswith('<div class="kb-diagram"'):
            block: list[str] = []
            depth = 0
            while index < len(lines):
                current = lines[index]
                block.append(current)
                depth += current.count("<div") - current.count("</div>")
                index += 1
                if depth <= 0:
                    break
            out.append(normalize_diagram_block("".join(block)))
            continue

        lower = stripped.lower()
        if lower.startswith(("<div", "<section", "<table", "<pre", "<script", "<style")):
            in_html_block = True
        if in_fence or in_html_block:
            out.append(normalize_diagram_html_line(line) if "kb-diagram-" in line else line)
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


def build_toml(data: dict[str, Any], is_section: bool) -> str:
    lines: list[str] = ["+++"]
    title = data.get("title")
    if not title:
        title = data.get("name")
    if title:
        lines.append(f"title = {toml_string(title)}")

    description = data.get("description")
    if description:
        lines.append(f"description = {toml_string(description)}")

    date_value = date_literal(data.get("date") or data.get("created"))
    if date_value and not is_section:
        lines.append(f"date = {date_value}")

    if data.get("draft") is not None and not is_section:
        lines.append(f"draft = {toml_bool(data.get('draft'))}")

    tags = data.get("tags") or []
    if tags and not is_section:
        lines.append("")
        lines.append("[taxonomies]")
        lines.append(f"tags = {toml_array(tags)}")

    extra: dict[str, Any] = {}
    if tags:
        extra["tags"] = tags
    if data.get("aliases"):
        extra["aliases"] = data.get("aliases")
    if date_value and is_section:
        extra["date"] = date_value
    for key, value in data.items():
        if key in {"title", "name", "description", "date", "created", "draft", "tags", "aliases"}:
            continue
        if isinstance(value, (str, int, float, bool, list)):
            extra[key] = value

    if extra:
        lines.append("")
        lines.append("[extra]")
        for key in sorted(extra):
            value = extra[key]
            if isinstance(value, bool):
                rendered = toml_bool(value)
            elif isinstance(value, (int, float)):
                rendered = str(value)
            elif isinstance(value, list):
                rendered = toml_array(value)
            else:
                rendered = toml_string(value)
            lines.append(f"{key} = {rendered}")

    lines.append("+++")
    return "\n".join(lines) + "\n"


def target_for(path: Path) -> Path:
    name = path.name
    if name == "index.md":
        return path.with_name("_index.md")
    if name.startswith("_") and name != "_index.md":
        return path.with_name(name.lstrip("_"))
    return path


def main() -> None:
    markdown_files = sorted(CONTENT.rglob("*.md"))
    renames: list[tuple[Path, Path]] = []
    converted = 0

    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        split = split_frontmatter(text)
        destination = target_for(path)
        is_section = destination.name == "_index.md"
        if split is None:
            data: dict[str, Any] = {"title": path.stem.replace("_", " ").replace("-", " ").title()}
            body = text
        else:
            data, body = split
        body = normalize_strong_emphasis(body)
        path.write_text(build_toml(data, is_section) + body, encoding="utf-8")
        converted += 1
        if destination != path:
            if destination.exists():
                raise RuntimeError(f"Refusing to overwrite existing file: {destination}")
            renames.append((path, destination))

    for source, destination in renames:
        source.rename(destination)

    print(f"Converted {converted} Markdown files")
    print(f"Renamed {len(renames)} files for Zola section/page rules")


if __name__ == "__main__":
    main()
