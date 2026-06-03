#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route


CONTENT_DIR = Path(os.getenv("CONTENT_DIR", "/workspace/content")).resolve()
BASE_URL = os.getenv("KB_BASE_URL", "http://localhost:8080").rstrip("/")
HOST = os.getenv("MCP_HOST", "0.0.0.0")
PORT = int(os.getenv("MCP_PORT", "8090"))

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
WORD_RE = re.compile(r"[A-Za-z0-9_\-]+")


@dataclass
class DocRecord:
    slug: str
    title: str
    path: str
    content: str
    links: list[str]
    backlinks: list[str]
    score: float = 0.0


def normalize_slug(value: str) -> str:
    value = value.strip().replace("\\", "/")
    value = value.removesuffix(".md")
    if "/" in value:
        value = value.split("/")[-1]
    return value.casefold()


def first_heading(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or fallback
    return fallback


def extract_links(markdown: str) -> list[str]:
    links: list[str] = []
    for match in WIKILINK_RE.findall(markdown):
        slug = normalize_slug(match.split("|", 1)[0])
        if slug:
            links.append(slug)
    return sorted(set(links))


def iter_docs() -> list[DocRecord]:
    docs: dict[str, DocRecord] = {}
    if not CONTENT_DIR.exists():
        return []

    for path in sorted(CONTENT_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        slug = normalize_slug(path.stem)
        title = first_heading(content, path.stem)
        docs[slug] = DocRecord(
            slug=slug,
            title=title,
            path=str(path.relative_to(CONTENT_DIR.parent)),
            content=content,
            links=extract_links(content),
            backlinks=[],
        )

    for doc in docs.values():
        for link in doc.links:
            if link in docs:
                docs[link].backlinks.append(doc.slug)

    for doc in docs.values():
        doc.backlinks = sorted(set(doc.backlinks))

    return list(docs.values())


def find_doc(slug: str) -> DocRecord | None:
    target = normalize_slug(slug)
    for doc in iter_docs():
        if doc.slug == target:
            return doc
    return None


def excerpt(content: str, query: str, max_chars: int = 240) -> str:
    flat = " ".join(line.strip() for line in content.splitlines() if line.strip())
    if not flat:
        return ""
    query_lower = query.casefold()
    idx = flat.casefold().find(query_lower)
    if idx == -1:
        return flat[:max_chars]
    start = max(idx - 80, 0)
    end = min(idx + len(query) + 120, len(flat))
    return flat[start:end]


def search_docs_impl(query: str, limit: int) -> list[dict[str, Any]]:
    terms = [term.casefold() for term in WORD_RE.findall(query)]
    if not terms:
        return []

    ranked: list[DocRecord] = []
    for doc in iter_docs():
        haystack = doc.content.casefold()
        title = doc.title.casefold()
        slug = doc.slug.casefold()
        score = 0.0
        for term in terms:
            score += haystack.count(term)
            score += title.count(term) * 4
            score += slug.count(term) * 3
        if score > 0:
            doc.score = score + (len(doc.backlinks) * 0.2) + (len(doc.links) * 0.1)
            ranked.append(doc)

    ranked.sort(key=lambda item: (-item.score, item.title.casefold()))

    return [
        {
            "slug": doc.slug,
            "title": doc.title,
            "path": doc.path,
            "score": round(doc.score, 2),
            "url": f"{BASE_URL}/{doc.slug}",
            "excerpt": excerpt(doc.content, query),
        }
        for doc in ranked[: max(1, min(limit, 20))]
    ]


MCP_INSTRUCTIONS = """
This server is a read-only knowledgebase for company Markdown documents.
Use search_docs first when the exact file name is unknown.
Use get_doc to read the full canonical source before summarizing policy or process details.
Use related_docs when you need surrounding context or hub pages.
Do not assume unpublished draft state exists here; this server reflects the checked-out repository files only.
""".strip()

mcp = FastMCP(
    name="knowledgebase",
    instructions=MCP_INSTRUCTIONS,
    stateless_http=True,
    json_response=True,
    streamable_http_path="/",
)


@mcp.tool()
def list_docs(limit: int = 50) -> list[dict[str, Any]]:
    """List available Markdown documents in the knowledgebase."""
    docs = iter_docs()[: max(1, min(limit, 200))]
    return [
        {
            "slug": doc.slug,
            "title": doc.title,
            "path": doc.path,
            "url": f"{BASE_URL}/{doc.slug}",
        }
        for doc in docs
    ]


@mcp.tool()
def get_doc(slug: str) -> dict[str, Any]:
    """Read the full Markdown source for a document by slug or filename."""
    doc = find_doc(slug)
    if doc is None:
        raise ValueError(f"Document not found: {slug}")
    return {
        "slug": doc.slug,
        "title": doc.title,
        "path": doc.path,
        "url": f"{BASE_URL}/{doc.slug}",
        "links_to": doc.links,
        "linked_from": doc.backlinks,
        "content": doc.content,
    }


@mcp.tool()
def search_docs(query: str, limit: int = 8) -> list[dict[str, Any]]:
    """Keyword-search the knowledgebase and return ranked documents with excerpts."""
    return search_docs_impl(query=query, limit=limit)


@mcp.tool()
def related_docs(slug: str, limit: int = 8) -> list[dict[str, Any]]:
    """Return outgoing links and backlinks around a document."""
    doc = find_doc(slug)
    if doc is None:
        raise ValueError(f"Document not found: {slug}")

    docs_by_slug = {item.slug: item for item in iter_docs()}
    related_slugs = list(dict.fromkeys(doc.links + doc.backlinks))
    results: list[dict[str, Any]] = []
    for related_slug in related_slugs[: max(1, min(limit, 20))]:
        related = docs_by_slug.get(related_slug)
        if related is None:
            continue
        results.append(
            {
                "slug": related.slug,
                "title": related.title,
                "path": related.path,
                "url": f"{BASE_URL}/{related.slug}",
                "connection": (
                    "bidirectional"
                    if related_slug in doc.links and related_slug in doc.backlinks
                    else "outgoing"
                    if related_slug in doc.links
                    else "backlink"
                ),
            }
        )
    return results


@mcp.tool()
def top_hubs(limit: int = 10) -> list[dict[str, Any]]:
    """Return the most connected hub documents by combined in/out link count."""
    docs = iter_docs()
    docs.sort(
        key=lambda item: (-(len(item.links) + len(item.backlinks)), item.title.casefold())
    )
    return [
        {
            "slug": doc.slug,
            "title": doc.title,
            "path": doc.path,
            "link_count": len(doc.links),
            "backlink_count": len(doc.backlinks),
            "url": f"{BASE_URL}/{doc.slug}",
        }
        for doc in docs[: max(1, min(limit, 20))]
    ]


async def homepage(_: Any) -> JSONResponse:
    return JSONResponse(
        {
            "name": "knowledgebase-mcp",
            "transport": "streamable-http",
            "mcp_path": "/mcp",
            "content_dir": str(CONTENT_DIR),
        }
    )


async def health(_: Any) -> JSONResponse:
    return JSONResponse({"status": "ok"})


@contextlib.asynccontextmanager
async def lifespan(_: Starlette):
    async with mcp.session_manager.run():
        yield


app = Starlette(
    routes=[
        Route("/", homepage),
        Route("/health", health),
        Route("/readyz", health),
        Mount("/mcp", app=mcp.streamable_http_app()),
    ],
    lifespan=lifespan,
)


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
