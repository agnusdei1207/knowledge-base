#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path
from typing import Any
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
OUT = ROOT / "static" / "assets" / "data"
BACKLINKS_OUT = OUT / "backlinks"
BASE = "/knowledge-base"

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]+)?\]\]")
MARKDOWN_INTERNAL_RE = re.compile(r"\[[^\]]+\]\((/knowledge-base/[^)#]+/?)(?:#[^)]+)?\)")


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "+++":
        return {}, text
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "+++":
            raw = "".join(lines[1:idx]).encode("utf-8")
            body = "".join(lines[idx + 1 :])
            return tomllib.loads(raw.decode("utf-8")), body
    return {}, text


def url_for(path: Path) -> str:
    rel = path.relative_to(CONTENT)
    if rel.name == "_index.md":
        parent = rel.parent.as_posix()
        suffix = "" if parent == "." else parent.strip("/") + "/"
    else:
        suffix = rel.with_suffix("").as_posix().strip("/") + "/"
    return f"{BASE}/{suffix}" if suffix else f"{BASE}/"


def path_for(path: Path) -> str:
    url = url_for(path)
    return url.removeprefix(BASE)


def title_for(path: Path, data: dict[str, Any]) -> str:
    title = data.get("title")
    if title:
        return str(title)
    if path.name == "_index.md":
        return path.parent.name.replace("_", " ").replace("-", " ").title() or "Knowledge Base"
    return path.stem.replace("_", " ").replace("-", " ").title()


def get_tags(data: dict[str, Any]) -> list[str]:
    extra = data.get("extra") or {}
    taxonomies = data.get("taxonomies") or {}
    tags = extra.get("tags") or taxonomies.get("tags") or []
    return [str(tag) for tag in tags]


def insert_tree(root: dict[str, Any], segments: list[str], item: dict[str, Any]) -> None:
    node = root
    for segment in segments[:-1]:
      children = node.setdefault("children", [])
      found = next((child for child in children if child.get("segment") == segment and child.get("section")), None)
      if found is None:
          found = {
              "segment": segment,
              "title": segment.replace("_", " ").replace("-", " ").title(),
              "url": f"{BASE}/{'/'.join(segments[:segments.index(segment)+1])}/",
              "section": True,
              "children": [],
          }
          children.append(found)
      node = found
    
    children = node.setdefault("children", [])
    found = next((child for child in children if child.get("segment") == item["segment"]), None)
    if found is not None:
        for k, v in item.items():
            if k != "children":
                found[k] = v
    else:
        children.append(item)


def sort_tree(node: dict[str, Any]) -> None:
    children = node.get("children", [])
    children.sort(key=lambda child: (not child.get("section"), child.get("title", "").lower()))
    for child in children:
        sort_tree(child)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    BACKLINKS_OUT.mkdir(parents=True, exist_ok=True)
    legacy_backlinks = OUT / "backlinks.json"
    if legacy_backlinks.exists():
        legacy_backlinks.unlink()
    for old in BACKLINKS_OUT.glob("*.json"):
        old.unlink()
    docs: list[dict[str, Any]] = []
    by_stem: dict[str, dict[str, Any]] = {}
    by_path: dict[str, dict[str, Any]] = {}

    for path in sorted(CONTENT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        data, body = split_frontmatter(text)
        doc = {
            "file": path.relative_to(CONTENT).as_posix(),
            "path": path_for(path),
            "url": url_for(path),
            "title": title_for(path, data),
            "tags": get_tags(data),
            "section": path.name == "_index.md",
            "body": body,
        }
        docs.append(doc)
        by_path[doc["path"]] = doc
        if not doc["section"]:
            by_stem.setdefault(path.stem, doc)

    tree = {"title": "Knowledge Base", "url": f"{BASE}/", "section": True, "children": []}
    for doc in docs:
        if doc["file"] == "_index.md":
            tree["title"] = doc["title"]
            continue
        rel = Path(doc["file"])
        if rel.name == "_index.md":
            segments = list(rel.parent.parts)
        else:
            segments = list(rel.with_suffix("").parts)
        item = {k: doc[k] for k in ("title", "url", "path", "section")}
        item["segment"] = segments[-1] if segments else ""
        item["children"] = []
        insert_tree(tree, segments, item)
    sort_tree(tree)

    backlinks: dict[str, list[dict[str, str]]] = {}
    links: list[dict[str, str]] = []
    node_ids: dict[str, str] = {}
    for index, doc in enumerate(docs):
        node_ids[doc["path"]] = f"n{index}"

    for doc in docs:
        seen_targets: set[str] = set()
        targets: list[dict[str, Any]] = []
        for match in WIKILINK_RE.finditer(doc["body"]):
            raw_target = match.group(1).strip()
            stem = Path(raw_target).stem
            target = by_stem.get(stem)
            if target:
                targets.append(target)
        for match in MARKDOWN_INTERNAL_RE.finditer(doc["body"]):
            raw_path = match.group(1).removeprefix(BASE)
            if not raw_path.startswith("/"):
                raw_path = "/" + raw_path
            if not raw_path.endswith("/"):
                raw_path += "/"
            target = by_path.get(raw_path)
            if target:
                targets.append(target)
        for target in targets:
            if target["path"] == doc["path"] or target["path"] in seen_targets:
                continue
            seen_targets.add(target["path"])
            backlinks.setdefault(target["path"], []).append({"title": doc["title"], "url": doc["url"]})
            links.append({"source": node_ids[doc["path"]], "target": node_ids[target["path"]]})

    linked_ids: set[str] = set()
    for link in links:
        linked_ids.add(link["source"])
        linked_ids.add(link["target"])
    selected_ids = set(list(linked_ids)[:360])
    nodes = [
        {"id": node_ids[doc["path"]], "title": doc["title"], "url": doc["url"], "section": doc["section"]}
        for doc in docs
        if node_ids[doc["path"]] in selected_ids
    ]
    graph_links = [
        link for link in links
        if link["source"] in selected_ids and link["target"] in selected_ids
    ][:900]

    (OUT / "site-index.json").write_text(json.dumps(tree, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    for doc in docs:
        filename = quote(doc["path"], safe="") + ".json"
        (BACKLINKS_OUT / filename).write_text(
            json.dumps(backlinks.get(doc["path"], [])[:80], ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
    (OUT / "graph.json").write_text(json.dumps({"nodes": nodes, "links": graph_links}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {len(docs)} docs, {len(links)} links")


if __name__ == "__main__":
    main()
