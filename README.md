# Knowledgebase

개인 학습(기술사 스터디 노트), 업무 문서, AI 에이전트 지식 검색을 하나의 저장소에서 관리하는 Zola + Pagefind 기반 지식 허브입니다.

## Architecture

```text
content/*.md
  -> scripts/build_zola_data.py
  -> zola build
  -> scripts/generate-llms-txt.sh
  -> pagefind --site public --output-subdir _pagefind
  -> GitHub Pages
```

`../brainscience`는 Zola 설정, Pagefind 빌드 스크립트, GitHub Actions 배포 구조를 참고한 대상입니다. 현재 사이트의 HTML/CSS 디자인은 knowledgebase의 기존 Quartz UI/UX를 Zola Tera 템플릿과 로컬 CSS로 재구현합니다.

## Content

```text
content/
├── _index.md
├── work/
├── personal/
├── study/
├── studynote/
└── research-and-development/
```

Zola 규칙에 따라 섹션 문서는 `_index.md`를 사용합니다. 일반 문서는 TOML frontmatter(`+++`)를 사용하며, 검색 인덱스는 Zola 내장 검색이 아니라 Pagefind가 생성합니다.

## Local Build

```bash
npm ci
PATH=/tmp/zola-bin:$PATH npm run build
```

로컬에 Zola가 없으면 GitHub Actions와 같은 버전을 설치합니다.

```bash
mkdir -p /tmp/zola-bin
curl -sSL https://github.com/getzola/zola/releases/download/v0.19.2/zola-v0.19.2-x86_64-unknown-linux-gnu.tar.gz \
  | tar xzf - -C /tmp/zola-bin
```

간단한 로컬 빌드는 다음 스크립트로 실행할 수 있습니다.

```bash
bash scripts/build-site.sh
```

## Deployment

GitHub Pages 배포는 `.github/workflows/deploy.yml`에서 수행합니다.

1. Node.js 24 설치
2. `npm ci`
3. Zola 0.19.2 설치
4. `npm run build`
5. `public/` 업로드
6. `actions/deploy-pages`

배포 URL:

```text
https://agnusdei1207.github.io/knowledge-base/
```

## Runtime Assets

`scripts/build_zola_data.py`는 다음 정적 데이터를 생성합니다.

| Path | Purpose |
| --- | --- |
| `static/assets/data/site-index.json` | Explorer 트리 |
| `static/assets/data/backlinks/*.json` | 페이지별 백링크 |
| `static/assets/data/graph.json` | 축약 그래프 뷰 |

이 파일들은 빌드 시 생성되므로 저장소에 커밋하지 않습니다.

## Key Files

| File | Role |
| --- | --- |
| `config.toml` | Zola 설정 |
| `templates/base.html` | Quartz형 레이아웃 재구현 |
| `static/assets/css/style.css` | Quartz형 테마/레이아웃 스타일 |
| `static/assets/js/site.js` | 검색 모달, 다크 모드, Explorer, graph/backlinks |
| `scripts/build_zola_data.py` | Explorer/backlinks/graph 데이터 생성 |
| `scripts/convert_frontmatter_to_zola.py` | YAML frontmatter를 TOML로 변환 |
| `scripts/convert_wikilinks_for_zola.py` | 위키링크를 Zola가 렌더링 가능한 링크로 변환 |
| `scripts/knowledgebase_mcp_server.py` | MCP HTTP 서버 |
| `AGENTS.md` | AI 에이전트 행동 규칙 |

## MCP Server

AI 에이전트는 `knowledgebase` MCP 서버를 통해 문서를 검색하고 읽을 수 있습니다.

주요 도구:

| Tool | Description |
| --- | --- |
| `search_docs` | 키워드 검색 |
| `get_doc` | 문서 조회 |
| `list_docs` | 문서 목록 조회 |
