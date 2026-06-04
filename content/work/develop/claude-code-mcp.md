---
title: "🤖 Claude Code + MCP 운영안"
tags:
  - "work"
---


이 문서는 20명 규모에서 Claude Code와 MCP를 이용해 이 저장소를 단순 문서 창고가 아니라 "지능형 지식베이스"로 쓰기 위한 운영안입니다.

관련 문서:
- [knowledge-pipeline](/work/develop/knowledge-pipeline/)
- [decap-cms](/work/develop/decap-cms/)
- [operations](/work/develop/operations/)
- [codex-sdk-operations](/work/develop/codex-sdk-operations/)

---

## 1. 결론부터

가장 실용적인 구조는 아래입니다.

- 원본: Git + Markdown
- 읽기 포털: Quartz
- 웹 편집: Decap CMS
- AI 작업 런타임: Claude Code 같은 코딩 에이전트
- AI 연결 계층: MCP

여기서 중요한 건 <strong>AI가 Quartz를 읽는 게 아니라, Quartz 뒤에 있는 Markdown 원본과 MCP 툴을 읽는다</strong>는 점입니다.

---

## 2. Claude Code는 어떤 일을 맡기면 좋은가

### 읽기/검색형 작업

- 최신 운영 규칙 문서 찾아 요약
- 특정 사업 문서와 R&D 문서 연결 관계 설명
- 여러 문서에 흩어진 기준을 한 번에 모아 체크리스트 생성

### 초안/정리형 작업

- 회의 메모를 허브 문서에 맞게 재정리
- 사업, 개발, 운영 문서를 공통 템플릿으로 정렬
- 누락된 링크를 찾고 관련 문서 추천

### 검토형 작업

- 정책 문서와 실제 코드/문서가 충돌하는지 점검
- 중복 문서, 오래된 문서, 고아 문서 찾기

---

## 3. 20명 규모에서 충돌을 줄이는 원칙

여기서 가장 중요한 건 <strong>읽기 경로와 쓰기 경로를 분리</strong>하는 것입니다.

### 읽기 경로

- Claude Code는 공용 `knowledgebase-mcp` 서버를 통해 문서를 검색/조회
- 공용 MCP 서버는 기본적으로 읽기 전용

### 쓰기 경로

- 문서 수정은 각자 로컬 작업본 또는 Decap CMS Editorial Workflow를 통해 진행
- 직접 `main`에 동시에 쓰지 않음
- 큰 변경은 PR 기준으로 승인

이렇게 해야 20명이 동시에 AI를 써도 Git 충돌이 급격히 늘지 않습니다.

---

## 4. 왜 공용 MCP 서버가 필요한가

직원마다 AI가 로컬 파일을 직접 긁도록만 두면:

- 각자 작업본 상태가 달라짐
- 최신성이 흔들림
- 권한과 접근 범위를 통제하기 어려움

그래서 공용 읽기 서버를 둡니다.

현재 저장소에는 `knowledgebase-mcp`가 포함되어 있습니다.

역할:
- `search_docs`
- `get_doc`
- `related_docs`
- `top_hubs`

이 서버는 `content/*.md`를 읽어 Claude Code가 공통 컨텍스트로 쓰게 해 줍니다.

---

## 5. Docker Compose로 어떻게 띄우는가

현재 `docker-compose.yml`에는 두 서비스가 있습니다.

- `quartz-server`: 포털 미리보기
- `knowledgebase-mcp`: Claude Code용 공용 MCP 서버

실행:

```bash
docker compose up -d --build
```

확인:

```bash
curl http://127.0.0.1:8090/health
curl http://127.0.0.1:8090/
```

기본 포트:

- Quartz: `8080`
- MCP: `8090`

---

## 6. Claude Code에서 어떻게 연결하는가

공식 문서 기준으로 Claude Code는 stdio 서버와 HTTP MCP 서버를 모두 연결할 수 있습니다.

현재 저장소에는 `.mcp.json.example`가 들어 있습니다.

예시:

```json
{
  "mcpServers": {
    "knowledgebase": {
      "url": "http://127.0.0.1:8090/mcp"
    }
  }
}
```

또는 CLI에서 직접 추가할 수도 있습니다.

```bash
claude mcp add --transport http knowledgebase http://127.0.0.1:8090/mcp
```

이후 Claude Code에서 예를 들어 이렇게 요청할 수 있습니다.

- `knowledgebase에서 운영 관련 문서를 찾아 현재 프로젝트 배포 체크리스트를 작성해줘`
- `business와 sales 문서를 비교해서 고객 제안 메시지 초안을 만들어줘`

---

## 7. Decap CMS는 왜 같이 검토하는가

Claude Code와 MCP만 붙이면 AI는 강해지지만, 비개발자 편집 UX는 여전히 약합니다.

그래서 Decap CMS를 같이 봐야 합니다.

역할 분리:

- Quartz: 읽기
- Decap CMS: 브라우저 편집
- Claude Code: 분석/초안/검토/자동화
- MCP: Claude Code가 공용 지식을 읽는 연결층

특히 Decap CMS의 `editorial_workflow`를 쓰면 초안과 승인 흐름을 PR 기반으로 강제할 수 있습니다.

현재 `/admin/` 경로는 배포되어 있지만, GitHub Pages만으로는 로그인 저장이 끝나지 않습니다.
GitHub backend를 실제로 쓰려면 인증 서버가 추가로 필요합니다.

---

## 8. 권장 운영 단계

### 1단계. 지금 바로 가능한 구조

- Quartz + 공용 MCP 서버
- 직원 일부는 Claude Code 사용
- 원본은 계속 Markdown

### 2단계. 비개발자 편집 도입

- Decap CMS 추가
- 문서 메타데이터와 템플릿 표준화

### 3단계. 검색 고도화

- OpenSearch + pgvector를 파생 인덱스로 추가
- 공용 MCP 서버가 향후 이 인덱스를 조회하도록 확장

---

## 9. 최종 판단

20명 규모에서는 <strong>공용 읽기 MCP 서버 + 개인 또는 승인 기반 쓰기 흐름</strong>이 핵심입니다.

이 원칙만 지키면:

- AI가 같은 지식을 본다
- 충돌이 줄어든다
- 웹 편집과 자동화가 공존한다
- 원본 Markdown 자산이 망가지지 않는다

추가로, 직원이 전부 Codex를 쓰는 환경이라면 내부 자동화 백엔드는 <strong><a href="/work/develop/codex-sdk-operations/">codex-sdk-operations</a></strong>처럼 Python Codex SDK로 분리하는 편이 더 낫습니다.
