#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
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
