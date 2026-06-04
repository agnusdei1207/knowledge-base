#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import tomllib
import unicodedata
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

STUDY_SUBJECT_TITLES = {
    "01_computer_architecture": "01. Computer Architecture",
    "02_operating_system": "02. Operating System",
    "03_network": "03. Network",
    "04_software_engineering": "04. Software Engineering",
    "05_database": "05. Database",
    "06_ict_convergence": "06. ICT Convergence",
    "07_enterprise_systems": "07. Enterprise Systems",
    "08_algorithm_stats": "08. Algorithms & Statistics",
    "09_security": "09. Security",
    "10_ai": "10. Artificial Intelligence",
    "11_design_supervision": "11. Design & Supervision",
    "12_it_management": "12. IT Management",
    "13_cloud_architecture": "13. Cloud Architecture",
    "14_data_engineering": "14. Data Engineering",
    "15_devops_sre": "15. DevOps & SRE",
    "16_bigdata": "16. Big Data",
}

NAV_PATH_TITLES = {
    "research-and-development": "R&D",
    "studynote": "Study Note",
    "work": "Work",
    "inbox": "Inbox",
}

TITLE_ACRONYMS = {
    "aa",
    "ai",
    "api",
    "arb",
    "ba",
    "bpr",
    "brm",
    "cicd",
    "ci",
    "cmm",
    "cmmi",
    "cpu",
    "cps",
    "crm",
    "da",
    "db",
    "devops",
    "dce",
    "drm",
    "dte",
    "ea",
    "eai",
    "erp",
    "esb",
    "etl",
    "fep",
    "fsk",
    "hdlc",
    "ict",
    "isi",
    "isa",
    "isp",
    "ismp",
    "it",
    "itil",
    "itsm",
    "llm",
    "ml",
    "msa",
    "nlp",
    "npu",
    "os",
    "pcm",
    "psk",
    "qam",
    "rag",
    "sdlc",
    "scm",
    "sre",
    "srm",
    "ta",
    "toc",
    "togaf",
    "trm",
}


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


def strip_emoji(text: str) -> str:
    cleaned = "".join(
        char
        for char in text
        if unicodedata.category(char) != "So"
        and char not in {"\ufe0f", "\u200d"}
    )
    return re.sub(r"\s+", " ", cleaned).strip()


def number_from_segment(segment: str) -> str:
    match = re.match(r"^(\d+)[._-]*", segment)
    return match.group(1) if match else ""


def strip_number_prefix(text: str) -> str:
    return re.sub(r"^\s*\d+\s*[:.)_-]*\s*", "", text).strip()


def title_word(word: str) -> str:
    lower = word.lower()
    if lower == "vs":
        return "vs"
    if lower in TITLE_ACRONYMS or word.isupper() or re.search(r"\d", word):
        return word.upper()
    return word.capitalize()


def readable_ascii_phrase(text: str) -> str:
    text = strip_emoji(text).replace("_", " ").replace("-", " ")
    text = re.sub(r"[가-힣一-龥ぁ-ゟ゠-ヿ]+", " ", text)
    text = re.sub(r"[^A-Za-z0-9+#&./\s]+", " ", text)
    words = [word.strip("./") for word in text.split()]
    words = [word for word in words if word]
    return " ".join(title_word(word) for word in words)


def title_from_segment(segment: str) -> str:
    if segment == "research-and-development":
        return "R&D"
    if segment == "work":
        return "Work"
    if segment == "studynote":
        return "Study Note"
    if segment == "inbox":
        return "Inbox"
    number = number_from_segment(segment)
    rest = re.sub(r"^\d+[._-]*", "", segment)
    label = readable_ascii_phrase(rest)
    if number:
        return f"{number}. {label or 'Topic'}"
    return label or "Topic"


def studynote_nav_title(path: Path, title: str) -> str:
    rel = path.relative_to(CONTENT)
    if rel.as_posix() == "studynote/_index.md":
        return "Study Note"
    if rel.name == "_index.md":
        segment = rel.parts[-2]
    else:
        segment = rel.stem
    if segment in STUDY_SUBJECT_TITLES:
        return STUDY_SUBJECT_TITLES[segment]

    number = number_from_segment(segment)
    title_candidate = strip_number_prefix(readable_ascii_phrase(title))
    segment_candidate = strip_number_prefix(readable_ascii_phrase(segment))
    candidate = title_candidate or segment_candidate or "Topic"
    return f"{number}. {candidate}" if number else candidate


def general_nav_title(path: Path, title: str) -> str:
    rel = path.relative_to(CONTENT)
    if rel.name == "_index.md":
        segment = rel.parts[-2] if len(rel.parts) > 1 else rel.stem
    else:
        segment = rel.stem
    if segment in NAV_PATH_TITLES:
        return NAV_PATH_TITLES[segment]

    # Extract number prefix if any
    number = number_from_segment(segment)
    
    # Extract English/ASCII from title
    title_candidate = strip_number_prefix(readable_ascii_phrase(title))
    segment_candidate = strip_number_prefix(readable_ascii_phrase(segment))
    
    candidate = title_candidate
    # Fallback to segment if title has no English or is too short
    if not candidate or len(candidate) < len(segment_candidate) * 0.5:
        candidate = segment_candidate or candidate or "Topic"
        
    if number:
        return f"{number}. {candidate}"
    return candidate


def nav_title_for(path: Path, title: str) -> str:
    rel = path.relative_to(CONTENT)
    parts = rel.parts
    if parts and parts[0] == "studynote":
        return studynote_nav_title(path, title)
    return general_nav_title(path, title)


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
              "title": title_from_segment(segment),
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


def _sort_key_tuple(child: dict[str, Any]) -> tuple:
    """이모지·특수문자를 제거한 뒤 숫자 prefix를 숫자로 비교하여 올바르게 정렬.
    만약 title에서 숫자를 찾지 못하면 segment(파일명/폴더명 stem)에서 찾음."""
    import unicodedata
    title = child.get("title", "")
    segment = child.get("segment", "")
    section = child.get("section", False)

    # 이모지 및 기호 카테고리(S*, P*) 문자 제거
    cleaned = "".join(
        c for c in title
        if unicodedata.category(c) not in {"So", "Sm", "Sc", "Sk", "Po", "Ps", "Pe", "Pi", "Pf", "Pd"}
    ).strip()

    # 1. Try to get number prefix from the title
    m = re.match(r"(\d+)", cleaned)
    if m:
        num = int(m.group(1))
    else:
        # 2. Try to get number prefix from the segment (e.g. 050_d_latch)
        m_seg = re.match(r"(\d+)", segment)
        if m_seg:
            num = int(m_seg.group(1))
        else:
            num = 9999

    has_no_number = (num == 9999)
    # Non-numbered items: folders (section=True, not section=False) first, then files (not section=True)
    section_group = (not section) if has_no_number else False

    # Return sorting tuple:
    # 1. has_no_number: Numbered items sort before non-numbered
    # 2. section_group: Folders sort before files for non-numbered items
    # 3. num: Numerical ordering
    # 4. section: Pages/files first, then folders/sections for tie-breakers (e.g., keyword list vs sub-folder)
    # 5. title lowercased: Alphabetical ordering fallback
    return (has_no_number, section_group, num, section, cleaned.lower())


def sort_tree(node: dict[str, Any]) -> None:
    children = node.get("children", [])
    children.sort(key=_sort_key_tuple)
    for child in children:
        sort_tree(child)


def get_parent_path(path_str: str) -> str:
    if path_str == "/":
        return ""
    parts = path_str.strip("/").split("/")
    if len(parts) <= 1:
        return "/"
    return "/" + "/".join(parts[:-1]) + "/"


def graph_group_for(path_str: str) -> str:
    parts = [part for part in path_str.strip("/").split("/") if part]
    if not parts:
        return "root"
    if parts[0] == "studynote" and len(parts) > 1:
        return "/".join(parts[:2])
    return parts[0]


def graph_chapter_for(path_str: str) -> str:
    parts = [part for part in path_str.strip("/").split("/") if part]
    if not parts:
        return "root"
    if parts[0] == "studynote" and len(parts) > 2:
        return "/".join(parts[:3])
    if len(parts) > 1:
        return "/".join(parts[:2])
    return parts[0]


def graph_label_for_key(key: str) -> str:
    if key == "root":
        return "Knowledge Base"
    parts = key.split("/")
    segment = parts[-1]
    if len(parts) == 2 and parts[0] == "studynote" and segment in STUDY_SUBJECT_TITLES:
        return STUDY_SUBJECT_TITLES[segment]
    return title_from_segment(segment)


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
        doc["nav_title"] = nav_title_for(path, doc["title"])
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
        item = {k: doc[k] for k in ("url", "path", "section")}
        item["title"] = doc["nav_title"]
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
        body_for_links = doc["body"]
        for marker in ("## 🔗 이전/다음 글", "### 🔗 이전/다음 글"):
            if marker in body_for_links:
                body_for_links = body_for_links.split(marker)[0]
                break
        for match in WIKILINK_RE.finditer(body_for_links):
            raw_target = match.group(1).strip()
            stem = Path(raw_target).stem
            target = by_stem.get(stem)
            if target:
                targets.append(target)
        for match in MARKDOWN_INTERNAL_RE.finditer(body_for_links):
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

    edge_pairs = {(link["source"], link["target"]) for link in links}

    # Programmatically add directory hierarchy links (parent-child folder links)
    for doc in docs:
        current_path = doc["path"]
        if current_path == "/":
            continue
        parent_path = get_parent_path(current_path)
        if parent_path and parent_path in by_path:
            parent_doc = by_path[parent_path]
            existing_backlinks = backlinks.setdefault(parent_path, [])
            if not any(b["url"] == doc["url"] for b in existing_backlinks):
                existing_backlinks.append({"title": doc["title"], "url": doc["url"]})
                
            p_nid = node_ids[parent_path]
            c_nid = node_ids[current_path]
            if (p_nid, c_nid) not in edge_pairs:
                links.append({"source": p_nid, "target": c_nid})
                edge_pairs.add((p_nid, c_nid))

    degrees: dict[str, int] = {}
    for link in links:
        degrees[link["source"]] = degrees.get(link["source"], 0) + 1
        degrees[link["target"]] = degrees.get(link["target"], 0) + 1

    # Adjacency list for neighbors (undirected)
    nid_to_path = {nid: path for path, nid in node_ids.items()}
    adj: dict[str, set[str]] = {doc["path"]: set() for doc in docs}
    for link in links:
        u_path = nid_to_path[link["source"]]
        v_path = nid_to_path[link["target"]]
        adj[u_path].add(v_path)
        adj[v_path].add(u_path)

    # Global graph.json with hierarchy nodes for zoomable exploration.
    sorted_linked_ids = sorted(degrees.keys(), key=lambda x: degrees[x], reverse=True)
    docs_by_nid = {node_ids[doc["path"]]: doc for doc in docs}

    ranked_ids = {nid: rank for rank, nid in enumerate(sorted_linked_ids)}
    linked_ids = set(sorted_linked_ids[:3200])
    selected_ids = set(node_ids.values())

    nodes = [
        {
            "id": "cluster:root",
            "title": "Knowledge Base",
            "type": "root",
            "level": 0,
            "degree": len(docs),
            "group": "root",
            "chapter": "root",
        }
    ]
    cluster_keys = sorted({graph_group_for(doc["path"]) for doc in docs})
    chapter_keys = sorted({graph_chapter_for(doc["path"]) for doc in docs})
    for key in cluster_keys:
        nodes.append({
            "id": f"cluster:{key}",
            "title": graph_label_for_key(key),
            "type": "cluster",
            "level": 1,
            "degree": sum(1 for doc in docs if graph_group_for(doc["path"]) == key),
            "group": key,
            "chapter": key,
        })
    for key in chapter_keys:
        if key in cluster_keys:
            continue
        group = "/".join(key.split("/")[:2]) if key.startswith("studynote/") else key.split("/")[0]
        nodes.append({
            "id": f"chapter:{key}",
            "title": graph_label_for_key(key),
            "type": "chapter",
            "level": 2,
            "degree": sum(1 for doc in docs if graph_chapter_for(doc["path"]) == key),
            "group": group,
            "chapter": key,
        })

    for nid in sorted(selected_ids, key=lambda x: degrees.get(x, 0), reverse=True):
        if nid in docs_by_nid:
            doc = docs_by_nid[nid]
            group = graph_group_for(doc["path"])
            chapter = graph_chapter_for(doc["path"])
            nodes.append({
                "id": nid,
                "title": doc["title"],
                "url": doc["url"],
                "type": "section" if doc["section"] else "doc",
                "level": 2 if doc["section"] else 3,
                "section": doc["section"],
                "degree": degrees.get(nid, 0),
                "rank": ranked_ids.get(nid, 999999),
                "group": group,
                "chapter": chapter,
            })

    graph_links = [
        {**link, "type": "doc"}
        for link in links
        if link["source"] in linked_ids and link["target"] in linked_ids
    ][:9000]

    hierarchy_links = [{"source": "cluster:root", "target": f"cluster:{key}", "type": "hierarchy"} for key in cluster_keys]
    for key in chapter_keys:
        if key in cluster_keys:
            continue
        group = "/".join(key.split("/")[:2]) if key.startswith("studynote/") else key.split("/")[0]
        hierarchy_links.append({"source": f"cluster:{group}", "target": f"chapter:{key}", "type": "hierarchy"})
    for nid in selected_ids:
        doc = docs_by_nid.get(nid)
        if not doc:
            continue
        chapter = graph_chapter_for(doc["path"])
        parent_id = f"chapter:{chapter}" if chapter not in cluster_keys else f"cluster:{chapter}"
        hierarchy_links.append({"source": parent_id, "target": nid, "type": "membership"})

    graph_links = hierarchy_links + graph_links

    (OUT / "site-index.json").write_text(json.dumps(tree, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    for doc in docs:
        filename = doc["path"].replace("/", "_") + ".json"
        (BACKLINKS_OUT / filename).write_text(
            json.dumps(backlinks.get(doc["path"], [])[:80], ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
    (OUT / "graph.json").write_text(json.dumps({"nodes": nodes, "links": graph_links}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {len(docs)} docs, {len(links)} links")


if __name__ == "__main__":
    main()
