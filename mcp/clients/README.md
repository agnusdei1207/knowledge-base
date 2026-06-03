# MCP Client Profiles

공용 엔드포인트 규격:

- 서버 이름: `knowledgebase`
- 전송 방식: remote HTTP
- 기본 URL: `http://127.0.0.1:8090/mcp`

포함 파일:

- `codex-config.toml`
- `hermes-config.yaml`
- `opencode.json`
- `claude-code.txt`

빠른 등록:

```bash
python scripts/setup_mcp_clients.py --url http://127.0.0.1:8090/mcp
```
