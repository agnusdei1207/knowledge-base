---
title: "🔌 MCP 클라이언트 설정 규격"
tags:
  - "work"
---


이 문서는 Claude Code, Codex, OpenCode가 같은 공용 MCP 서버를 보도록 맞추는 표준 설정 문서입니다.

관련 문서:
- [claude-code-mcp](/work/develop/claude-code-mcp/)
- [operations](/work/develop/operations/)

---

## 1. 공용 규격

직원들에게는 아래 두 가지만 전달하면 됩니다.

- 서버 이름: `knowledgebase`
- 서버 URL: `http://127.0.0.1:8090/mcp`

원칙:

- 모든 클라이언트는 같은 이름을 쓴다
- 읽기 전용 공용 서버를 먼저 붙인다
- 문서 수정은 각 클라이언트의 Git 작업 흐름으로 분리한다

---

## 2. 저장소에 포함된 구현물

이 저장소에는 다음이 포함되어 있습니다.

- 공용 MCP 서버 구현: `scripts/knowledgebase_mcp_server.py`
- 컨테이너 이미지 정의: `docker/knowledgebase-mcp.Dockerfile`
- Compose 서비스: `docker-compose.yml`
- 클라이언트 템플릿: `mcp/clients/*`
- 자동 등록 스크립트: `scripts/setup_mcp_clients.py`
- 에이전트 공통 규칙: `AGENTS.md`

---

## 3. 빠른 적용

서버 기동:

```bash
docker compose up -d --build knowledgebase-mcp
```

클라이언트 등록:

```bash
python scripts/setup_mcp_clients.py --url http://127.0.0.1:8090/mcp
```

특정 클라이언트만:

```bash
python scripts/setup_mcp_clients.py --clients claude,codex
```

---

## 4. 클라이언트별 설정 방식

### Claude Code

공식 CLI 방식:

```bash
claude mcp add --transport http --scope user knowledgebase http://127.0.0.1:8090/mcp
claude mcp list
```

저장소 템플릿:

- `mcp/clients/claude-code.txt`

### Codex

공식 문서 기준으로 Codex는 CLI 또는 `~/.codex/config.toml`로 MCP를 등록할 수 있습니다.

저장소 템플릿:

- `mcp/clients/codex-config.toml`

자동 등록 스크립트는 `~/.codex/config.toml`에 `knowledgebase` 엔트리를 넣습니다.

### OpenCode

공식 문서 기준으로 OpenCode는 `~/.config/opencode/opencode.json`의 `mcp` 아래에 원격 서버를 추가합니다.

저장소 템플릿:

- `mcp/clients/opencode.json`

자동 등록 스크립트는 해당 JSON에 `knowledgebase` 원격 MCP 엔트리를 병합합니다.

---

## 5. 왜 이름을 통일하는가

이름이 클라이언트마다 다르면:

- 프롬프트 가이드가 흩어짐
- 직원 교육이 복잡해짐
- 에이전트 규칙 문서도 클라이언트별로 갈라짐

그래서 `knowledgebase` 하나로 통일합니다.

예시 규칙:

- 문서나 정책을 찾을 때는 `knowledgebase`를 먼저 사용한다
- 관련 문서가 더 필요한 경우 `related_docs`를 사용한다
- 확실하지 않으면 `search_docs` 후 `get_doc`으로 원문을 읽는다

---

## 6. 권장 사용 규칙

읽기:

- `search_docs`
- `get_doc`
- `related_docs`
- `top_hubs`

쓰기:

- 로컬 작업본에서 문서 수정
- Decap CMS Editorial Workflow 사용
- PR 승인 후 반영

즉, MCP는 공용 읽기 컨텍스트 계층으로 두고, 쓰기는 Git 흐름으로 분리하는 것이 안전합니다.
