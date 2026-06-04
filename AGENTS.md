# Agent Rules

When you need company policy, process, architecture, project history, or document context, use the `knowledgebase` MCP server first.

Usage policy:

- Use `search_docs` before guessing a filename.
- Use `get_doc` before summarizing any policy or workflow.
- Use `related_docs` when the current page may be a hub or partial view.
- Treat `content/*.md` as the canonical source of truth.
- If the MCP server has a relevant document, do not answer from memory alone.

## Study Note (기술사 스터디 노트)

기술 도메인 지식(컴퓨터 구조, OS, 네트워크, SW공학, DB, ICT 융합, 엔터프라이즈, 알고리즘/통계, 보안, AI, 설계/감리, IT 경영, 클라우드, 데이터 엔지니어링, DevOps/SRE, 빅데이터)이 필요할 때 `content/studynote/` 아래 문서들을 우선 참조한다.

- 과목 구성: 01~16번 폴더 (각 폴더에 세부 챕터 및 키워드 목록 포함)
- 허브 문서: `content/studynote/_index.md`
- 검색 예시: `search_docs("캐시 메모리")`, `get_doc("studynote/01_computer_architecture/_index")`

## Quartz Migration

- This repository is now a Quartz site. Do not reintroduce Zola, Pagefind, `templates/`, `static/assets/`, or `config.toml`.
- Keep the Quartz implementation aligned with `../codex-skills`; project-specific changes should be limited to site metadata, CI/CD, deployment paths, and this repository's `content/`.
- Use `npm run build` to verify the site.
