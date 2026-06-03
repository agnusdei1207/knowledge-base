#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


DEFAULT_NAME = "knowledgebase"
DEFAULT_URL = "http://127.0.0.1:8090/mcp"
DEFAULT_CLIENTS = ["claude", "codex", "hermes", "opencode"]


def run_command(command: list[str]) -> bool:
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
    except FileNotFoundError:
        return False
    return result.returncode == 0


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def upsert_codex_config(path: Path, server_name: str, url: str) -> None:
    ensure_parent(path)
    block_header = f"[mcp_servers.{server_name}]"
    block_body = f'{block_header}\nurl = "{url}"\n'
    if not path.exists():
        path.write_text(block_body, encoding="utf-8")
        return

    lines = path.read_text(encoding="utf-8").splitlines()
    output: list[str] = []
    skip = False
    for line in lines:
        if line.strip().startswith("[mcp_servers.") and skip:
            skip = False
        if line.strip() == block_header:
            skip = True
            continue
        if not skip:
            output.append(line)
    content = "\n".join(output).rstrip()
    if content:
        content += "\n\n"
    content += block_body
    path.write_text(content, encoding="utf-8")


def upsert_opencode_config(path: Path, server_name: str, url: str) -> None:
    ensure_parent(path)
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        data = {"$schema": "https://opencode.ai/config.json"}
    if not isinstance(data, dict):
        raise ValueError(f"Unsupported JSON structure in {path}")
    data.setdefault("mcp", {})
    data["mcp"][server_name] = {
        "type": "remote",
        "url": url,
        "enabled": True,
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def install_claude(server_name: str, url: str) -> str:
    if shutil.which("claude") is None:
        return "skipped: claude not installed"
    run_command(["claude", "mcp", "remove", server_name])
    ok = run_command(
        [
            "claude",
            "mcp",
            "add",
            "--transport",
            "http",
            "--scope",
            "user",
            server_name,
            url,
        ]
    )
    return "installed" if ok else "failed"


def install_codex(server_name: str, url: str) -> str:
    config_path = Path.home() / ".codex" / "config.toml"
    upsert_codex_config(config_path, server_name, url)
    if shutil.which("codex") is not None:
        run_command(["codex", "mcp", "list"])
    return f"written: {config_path}"


def install_hermes(server_name: str, url: str) -> str:
    if shutil.which("hermes") is None:
        target = Path.home() / ".hermes" / "config.yaml"
        ensure_parent(target)
        snippet = (
            "mcp_servers:\n"
            f'  {server_name}:\n'
            f'    url: "{url}"\n'
            "    enabled: true\n"
        )
        if target.exists():
            current = target.read_text(encoding="utf-8")
            if f"  {server_name}:" not in current:
                if not current.endswith("\n"):
                    current += "\n"
                current += "\n" + snippet
                target.write_text(current, encoding="utf-8")
        else:
            target.write_text(snippet, encoding="utf-8")
        return f"written: {target}"

    run_command(["hermes", "mcp", "remove", server_name])
    ok = run_command(["hermes", "mcp", "add", server_name, "--url", url])
    return "installed" if ok else "failed"


def install_opencode(server_name: str, url: str) -> str:
    config_path = Path.home() / ".config" / "opencode" / "opencode.json"
    upsert_opencode_config(config_path, server_name, url)
    return f"written: {config_path}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Register the knowledgebase MCP server for supported clients.")
    parser.add_argument("--url", default=DEFAULT_URL, help="Remote MCP URL")
    parser.add_argument("--name", default=DEFAULT_NAME, help="MCP server name")
    parser.add_argument(
        "--clients",
        default=",".join(DEFAULT_CLIENTS),
        help="Comma-separated list: claude,codex,hermes,opencode",
    )
    args = parser.parse_args()

    installers = {
        "claude": install_claude,
        "codex": install_codex,
        "hermes": install_hermes,
        "opencode": install_opencode,
    }

    selected = [item.strip() for item in args.clients.split(",") if item.strip()]
    for client in selected:
        if client not in installers:
            raise SystemExit(f"Unsupported client: {client}")

    for client in selected:
        result = installers[client](args.name, args.url)
        print(f"{client}: {result}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
