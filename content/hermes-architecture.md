# 🏛️ 헤르메스 아키텍처 제안

대표가 요청한 헤르메스는 단순한 문서 사이트가 아니라, 여러 직원과 여러 AI 에이전트가 같은 지식 자산을 읽고 쓰는 공용 운영 계층으로 보는 것이 맞습니다.

관련 문서:
- [[knowledgebase-decision-log]]
- [[hermes-agent]]
- [[hermes-pipeline]]
- [[decap-cms]]
- [[quartz-deployment]]

---

## 1. 문제 정의

우리가 실제로 원하는 것은 아래를 동시에 만족하는 구조입니다.

- 직원이 쉽게 읽고 수정할 수 있어야 한다
- AI 에이전트가 특정 CLI에 묶이지 않고 같은 지식을 활용해야 한다
- 검색이 잘 되어야 한다
- 원본은 사람이 읽기 쉬운 포맷이어야 한다
- 운영 복잡도는 낮아야 한다

Quartz는 이 중 "읽기 좋은 웹 포털"은 잘 해결하지만, 다중 사용자 편집과 에이전트 접속 표준화까지 단독으로 해결하진 못합니다.

중요한 전제:

- 여기서 말하는 에이전트는 **Nous Research의 Hermes Agent CLI/TUI 및 Gateway**입니다
- **MCP는 Hermes Agent를 확장하는 연결 표준**이지, Hermes 자체를 대체하는 것이 아닙니다

---

## 2. 결론부터: 추천 조합

현 시점의 추천 조합은 아래입니다.

1. 원본 저장소: GitHub 또는 Forgejo/Gitea
2. 원본 포맷: `content/*.md`
3. 웹 조회 포털: Quartz
4. 웹 편집 UI: Decap CMS
5. 에이전트 런타임: Hermes Agent
6. 검색 인덱스: OpenSearch + pgvector

요약하면:

- **Quartz는 조회와 그래프 탐색**
- **Decap CMS는 웹 편집과 승인 흐름**
- **Git 포지는 권한, 이력, PR**
- **Hermes Agent는 실제 실행 주체**
- **Hermes MCP는 Hermes가 외부 도구를 붙이는 확장 표준**
- **검색엔진과 벡터DB는 파생 인덱스**

---

## 3. 왜 Quartz 단독이 부족한가

Quartz는 Markdown을 정적 웹으로 빌드하는 데 매우 적합합니다.

강점:
- 그래프 뷰가 좋다
- 링크 탐색성이 좋다
- 정적 배포라 단순하다

한계:
- 브라우저 안에서 승인 가능한 편집 워크플로우가 없다
- 사용자 그룹별 권한 모델이 약하다
- 비정형 자료 검색을 위한 별도 인덱싱 계층이 없다
- 에이전트가 붙는 표준 API/MCP 역할을 하지 않는다

따라서 Quartz는 계속 유지하되, "포털 계층"으로 역할을 한정하는 편이 맞습니다.

---

## 4. Decap CMS는 어디에 들어가는가

Decap CMS는 Git 저장소를 백엔드로 쓰는 웹 편집 UI입니다.

이 의미가 중요합니다.

- 별도 DB가 주 저장소가 아님
- 브라우저에서 편집해도 결국 Git에 커밋 또는 PR이 생김
- 원본 Markdown을 계속 유지함

즉, Quartz를 버리고 CMS로 갈아타는 개념이 아니라,

**Quartz 앞단에 편집용 `/admin` 계층을 하나 더 붙이는 방식**으로 이해하면 됩니다.

직원 관점:
- 문서를 본다: Quartz
- 문서를 수정한다: Decap CMS

AI 관점:
- 문서를 읽고 쓴다: Git 또는 MCP

---

## 5. Hermes Agent는 어디에 들어가는가

Hermes Agent는 CLI/TUI에서 직접 실행할 수도 있고, Gateway/API 계층으로 여러 직원에게 열어둘 수도 있습니다.

정리하면:

- `hermes` 또는 `hermes --tui`: 파워유저용 로컬 런타임
- `hermes gateway`: 메신저/다중 사용자 접속용 런타임
- `hermes`의 Web Dashboard/API Server: 운영자용 설정/연동 면

우리 구조에서 Hermes Agent는 **문서를 직접 작성하는 도구이자, 직원 요청을 실행하는 작업 런타임**에 해당합니다.

즉:

- 원본 저장은 Git/Markdown
- 읽기 포털은 Quartz
- 실제 작업을 수행하는 에이전트는 Hermes Agent

---

## 6. Hermes MCP는 왜 필요한가

직원이 Claude Code, Codex, Copilot, 사내 에이전트 등 서로 다른 클라이언트를 써도, 접속 계층은 하나여야 합니다.

그 역할이 Hermes MCP입니다.

MCP 계층이 있으면:
- 클라이언트마다 별도 Git 자동화 스크립트를 만들 필요가 줄어든다
- 문서 검색, 초안 생성, PR 생성, 승인 요청 같은 동작을 공통 툴로 노출할 수 있다
- 나중에 Slack, Drive, DB, CRM도 같은 방식으로 연결할 수 있다

권장 모델:
- 외부/사내 클라이언트는 Hermes MCP에 접속
- Hermes MCP는 Git, 검색 인덱스, 문서 메타데이터를 중개

---

## 7. 저장소/포털/에이전트 계층을 분리해야 하는 이유

이 구조의 핵심은 계층 분리입니다.

### 원본 계층

- `content/*.md`
- Git 이력
- 사람이 읽을 수 있는 진짜 문서

### 포털 계층

- Quartz
- 그래프 뷰
- 링크 탐색

### 편집 계층

- Decap CMS
- 브라우저 편집
- 초안/리뷰/병합 흐름

### 에이전트 계층

- Hermes Agent CLI/TUI
- Hermes Gateway / API Server
- Hermes MCP
- 검색, 초안 작성, PR 생성, 문서 조회

### 인덱스 계층

- OpenSearch
- pgvector
- 파생 메타데이터

이렇게 쪼개면 일부가 고장나도 원본 지식은 안전합니다.

---

## 8. GitHub와 Forgejo/Gitea 중 무엇이 나은가

### GitHub

장점:
- 지금 이미 쓰고 있음
- GitHub Actions/Pages가 바로 연결됨
- GitHub MCP 문서와 원격 구성 지원이 빠름

단점:
- 외부 SaaS 의존
- 사내 통제 요구가 커지면 제약이 생길 수 있음

### Forgejo/Gitea

장점:
- 자가호스팅 가능
- 저장소와 계정을 내부 통제로 운영 가능

단점:
- 초기 운영 부담이 늘어남
- GitHub만큼 생태계 통합이 매끄럽진 않을 수 있음

현재 단계 권장안:
- **1단계는 GitHub**
- **통제/보안 요구가 커지면 Forgejo/Gitea 검토**

---

## 9. 단계별 도입안

### 1단계. 현재 구조 유지

- Markdown + GitHub + Quartz
- AI는 `content/*.md`만 수정

### 2단계. 웹 편집 도입

- Quartz 사이트에 `admin/` 추가
- Decap CMS로 브라우저 편집 지원
- 승인 흐름은 PR 중심

### 3단계. 검색 고도화

- Git 변경을 트리거로 OpenSearch와 pgvector 인덱싱
- 키워드 검색 + 의미 검색 + 링크 기반 재정렬 결합

### 4단계. Hermes MCP 도입

- `search_docs`
- `get_doc`
- `create_draft`
- `open_pr`
- `list_related_docs`

이 정도의 고수준 툴을 제공

---

## 10. 최종 추천

가장 현실적인 권장안은 아래입니다.

**Quartz는 그대로 유지하고, Hermes Agent를 실제 작업 런타임으로 두고, Decap CMS를 웹 편집 계층으로 붙이고, 검색은 별도 인덱스로 분리하고, Hermes는 MCP로 외부 도구를 붙인다.**

이 조합이 다음 네 가지를 가장 잘 지킵니다.

- 원본이 휴먼 리더블하다
- 검색 품질을 고도화할 수 있다
- 직원과 AI가 같은 자산을 공유한다
- 운영 복잡도를 필요 이상으로 올리지 않는다

---

## 11. 참고 메모

이 문서의 판단에는 다음 공식 자료를 참고했습니다.

- Decap CMS 공식 소개: Git 워크플로우를 감싸는 오픈소스 React 앱
- Decap CMS 공식 편집 워크플로우 문서
- Quartz 공식 그래프 뷰 문서
- MCP 공식 transport 문서
- GitHub 공식 MCP 서버 문서
