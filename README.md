# 🌌 통합 지식저장소 (Knowledgebase)

개인 학습(기술사 스터디 노트) · 사내 업무 문서 · AI 에이전트 지식 검색을 **하나의 저장소**에서 관리하는 Quartz v5 기반 지식 허브입니다.

---

## 목차

1. [전체 아키텍처](#1-전체-아키텍처)
2. [콘텐츠 구조](#2-콘텐츠-구조)
3. [로컬 실행 (Docker)](#3-로컬-실행-docker)
4. [GitHub Pages 배포](#4-github-pages-배포)
5. [배포 트러블슈팅](#5-배포-트러블슈팅)
6. [MCP 서버 (AI 에이전트 연동)](#6-mcp-서버-ai-에이전트-연동)
7. [설정 파일 설명](#7-설정-파일-설명)

---

## 1. 전체 아키텍처

```
          ┌────────────────────────────────────────────┐
          │            GitHub Repository                │
          │   (content/*.md + quartz.config.yaml)      │
          └──────┬──────────────────────────┬──────────┘
                 │ git push (main)           │ ro mount
                 ▼                           ▼
     ┌───────────────────┐       ┌────────────────────┐
     │  GitHub Actions   │       │   로컬 Docker       │
     │  (deploy.yml)     │       │  docker compose up  │
     │                   │       │                     │
     │  Quartz v5 빌드   │       │  Quartz v5 serve    │
     │  → GitHub Pages   │       │  :8080 (웹 UI)      │
     └───────────────────┘       │  MCP Server :8090   │
                                 └────────────────────┘
                                          │
                                          ▼
                                  [ AI 에이전트 ]
                            (search_docs / get_doc)
```

---

## 2. 콘텐츠 구조

```
content/
├── index.md            ← 메인 허브 대시보드
├── work/               ← 🏢 사내 업무 (비즈니스·개발·운영)
│   ├── _index.md
│   ├── business.md
│   ├── development.md
│   └── ...
├── study/              ← 🎓 학습 & R&D
│   ├── _index.md
│   ├── r-and-d.md
│   └── studynote/      ← 기술사 시험 16과목 스터디 노트 (9,597개)
│       ├── 01_computer_architecture/
│       ├── 02_operating_system/
│       └── ...
└── personal/           ← 🏠 개인 기록 (비공개 가능)
    ├── _index.md
    ├── journal.md
    └── ...
```

> **분리 원칙**: `study/studynote/` 는 기술사 시험 전용 공간입니다. 업무 문서(`work/`)와 절대 혼재하지 않습니다.
> **비공개 처리**: `private/` 폴더나 frontmatter에 `draft: true` 를 쓰면 빌드에서 제외됩니다.

---

## 3. 로컬 실행 (Docker)

### 사전 준비

| 항목 | 최소 버전 |
|------|----------|
| Docker Desktop | 4.x 이상 |
| Docker Compose | v2 (CLI: `docker compose`) |

### 전체 서비스 시작

```bash
# 저장소 클론
git clone https://github.com/agnusdei1207/knowledge-base.git
cd knowledge-base

# 모든 서비스 백그라운드 실행
docker compose up -d
```

| 서비스 | 포트 | 역할 |
|--------|------|------|
| Quartz 웹서버 | http://localhost:8080 | 지식 위키 UI (라이브 리로드) |
| MCP 서버 | http://localhost:8090 | AI 에이전트 API |

> **첫 실행**: `npm ci` + `npx quartz build` 때문에 **2~3분** 소요됩니다. 이후는 캐시로 빠릅니다.

### 서비스 중지 / 재시작

```bash
docker compose down          # 중지
docker compose restart       # 재시작 (코드 변경 후)
docker compose logs -f       # 실시간 로그 확인
```

### 콘텐츠 수정 반영

콘텐츠(`content/`)를 수정하면 Quartz serve 모드가 자동으로 감지해서 리빌드합니다. 브라우저에서 새로고침하면 바로 보입니다.

---

## 4. GitHub Pages 배포

### 저장소 설정 (최초 1회)

1. GitHub 저장소 → **Settings → Pages**
2. Source: **GitHub Actions** 선택
3. `main` 브랜치에 push하면 자동 배포됩니다.

### 배포 URL

```
https://agnusdei1207.github.io/knowledge-base/
```

### 배포 흐름

```
git push origin main
        ↓
GitHub Actions (deploy.yml)
        ↓
① Quartz v5 tarball 다운로드 (캐시 히트 시 스킵)
② npm ci --prefer-offline (npm 캐시 활용)
③ npx quartz plugin install
④ npx quartz build → .quartz-build/public/
⑤ actions/upload-pages-artifact
⑥ actions/deploy-pages → GitHub Pages
        ↓
배포 완료 (캐시 히트 시 약 3~5분)
```

### 캐시 전략

| 캐시 키 | 내용 | 무효화 조건 |
|---------|------|------------|
| `quartz-src-v5-{hash}` | Quartz v5 소스 tarball | `quartz.config.yaml` 변경 시 |
| `quartz-npm-v5-{hash}` | node_modules | `package-lock.json` 변경 시 |

---

## 5. 배포 트러블슈팅

### ❌ 빌드가 30분 이상 걸린다

**원인**: Quartz 소스 재다운로드 + npm 패키지 재설치 (캐시 미적중)

**해결**:
```bash
# GitHub Actions에서 캐시를 강제 초기화하려면:
# 저장소 → Actions → 사이드바 "Caches" → 해당 캐시 삭제
# 또는 quartz.config.yaml 에 공백 한 줄 추가 후 push (캐시 키 변경)
```

---

### ❌ `Some specified paths were not resolved, unable to cache dependencies`

**원인**: `actions/setup-node`의 `cache: 'npm'` 옵션은 프로젝트 루트의 `package-lock.json`을 찾는데,
이 프로젝트는 Quartz를 임시 디렉토리에 다운로드해서 빌드하므로 루트에 `package-lock.json`이 없습니다.

**해결**: 이미 수정됨. `setup-node`에서 `cache: 'npm'` 옵션을 제거하고 `actions/cache@v4`로 직접 캐시 경로를 지정했습니다.
추가 작업 필요 없음.

---

### ❌ `npx quartz plugin install` 실패

**원인 1**: `quartz.config.yaml`에 존재하지 않는 플러그인 소스가 있을 때

**확인**:
```bash
# 로컬에서 먼저 테스트
USE_DOCKER=false bash scripts/build-quartz.sh /tmp/test-build
```

**원인 2**: GitHub API 레이트 리밋 (플러그인을 `github:quartz-community/...`에서 받아오는 경우)

**해결**: 재시도하면 보통 해결됩니다. 반복적이면 Actions Secrets에 `GH_TOKEN`을 추가하세요.

---

### ❌ Docker `quartz-server` 컨테이너가 바로 죽는다

```bash
# 로그 확인
docker compose logs quartz-server

# 대부분 원인: npm ci 중 메모리 부족
# docker-compose.yml에 메모리 제한이 없는지 확인
# 또는 NODE_OPTIONS를 늘려서 재시작
NODE_OPTIONS=--max-old-space-size=4096 docker compose up quartz-server
```

---

### ❌ GitHub Pages에 배포는 됐는데 CSS/이미지가 안 나온다

**원인**: `quartz.config.yaml`의 `baseUrl`이 잘못 설정된 경우

```yaml
# quartz.config.yaml
configuration:
  baseUrl: agnusdei1207.github.io/knowledge-base  # ← 이 값 확인
```

> `https://` 프로토콜과 슬래시 없이 `도메인/경로` 형식으로 작성해야 합니다.

---

### ❌ `content/private/` 파일이 공개된다

**방법 1**: `quartz.config.yaml`의 `ignorePatterns` 확인

```yaml
configuration:
  ignorePatterns:
    - private        # ← 이 줄이 있어야 함
    - templates
    - .obsidian
```

**방법 2**: frontmatter에 `draft: true` 추가

```markdown
---
title: "비공개 문서"
draft: true
---
```

---

### ❌ test (validate) 워크플로우가 실패한다

**확인**:
```bash
# 필수 파일 존재 확인
ls quartz.config.yaml docker-compose.yml \
   scripts/build-quartz.sh scripts/serve-quartz.sh \
   scripts/knowledgebase_mcp_server.py \
   docker/knowledgebase-mcp.Dockerfile \
   content/index.md

# YAML 문법 검사
python3 -c "import yaml; yaml.safe_load(open('quartz.config.yaml'))" && echo OK

# 셸 스크립트 문법 검사
bash -n scripts/build-quartz.sh && echo OK
```

---

## 6. MCP 서버 (AI 에이전트 연동)

### 연결 설정 예시 (Claude Desktop / Cursor 등)

```json
{
  "mcpServers": {
    "knowledgebase": {
      "url": "http://localhost:8090/mcp"
    }
  }
}
```

### 사용 가능한 도구

| 도구 | 설명 | 예시 |
|------|------|------|
| `search_docs` | 키워드 전문 검색 | `search_docs("캐시 메모리")` |
| `get_doc` | 파일 경로로 문서 조회 | `get_doc("study/studynote/01_computer_architecture/cache.md")` |
| `list_docs` | 디렉토리 목록 조회 | `list_docs("work/")` |

### 에이전트 사용 원칙 (AGENTS.md)

- AI 에이전트는 기술 도메인 질문 시 `study/studynote/` 를 **우선** 참조합니다.
- 업무 프로세스·정책은 `work/` 에서 검색합니다.
- **쓰기 권한 없음** — MCP 서버는 읽기 전용(`ro` 마운트)입니다.

---

## 7. 설정 파일 설명

| 파일 | 역할 |
|------|------|
| `quartz.config.yaml` | Quartz v5 전체 설정 (테마, 플러그인, baseUrl) |
| `docker-compose.yml` | 로컬 개발 환경 (Quartz 웹서버 + MCP 서버) |
| `docker/knowledgebase-mcp.Dockerfile` | MCP 서버 Python 컨테이너 이미지 |
| `scripts/build-quartz.sh` | CI/CD 및 로컬 정적 빌드 스크립트 |
| `scripts/serve-quartz.sh` | 로컬 라이브 서버 스크립트 (Docker entrypoint) |
| `scripts/knowledgebase_mcp_server.py` | MCP HTTP 서버 (FastMCP/Starlette) |
| `AGENTS.md` | AI 에이전트 행동 규칙 |
| `.github/workflows/deploy.yml` | GitHub Pages 자동 배포 |
| `.github/workflows/test.yml` | PR/push 구조 검증 (YAML·sh 문법, 필수 파일) |
