# 🧠 Hermes Agent는 우리 구조에서 무엇인가

이 문서는 `CLI에서 돌아가는 Hermes Agent`를 기준으로, 우리 지식베이스 구조와 어떻게 결합해야 하는지 정리한 문서입니다.

관련 문서:
- [[hermes-architecture]]
- [[hermes-pipeline]]
- [[decap-cms]]
- [[operations]]

---

## 1. 핵심 정리

Hermes Agent는 우리 구조에서 **지식 저장소 자체**가 아닙니다.

역할은 아래처럼 보는 것이 맞습니다.

- 지식 저장소: Git + Markdown
- 지식 조회 포털: Quartz
- 웹 편집기: Decap CMS
- 에이전트 런타임: Hermes Agent
- 외부 도구 연결 표준: MCP

즉, Hermes는 "문서를 담는 통"이 아니라 **문서를 읽고 쓰고 검색하고 자동화하는 작업 주체**입니다.

---

## 2. CLI에서 도는 Hermes를 어떻게 써야 하나

공식 문서 기준으로 Hermes Agent는 CLI/TUI에서 직접 실행하는 사용 패턴을 기본으로 제공합니다.

우리 관점에서는 이걸 두 가지로 나눠 쓰는 게 좋습니다.

### 개인 작업용

- 직원 또는 운영자가 자기 PC에서 `hermes` 또는 `hermes --tui` 실행
- 로컬 작업본에서 문서를 정리하거나 초안 작성
- Git commit / PR까지 연결

### 공용 서비스용

- 전용 운영 서버에서 `hermes gateway` 실행
- Slack, Discord, Telegram 같은 채널로 직원 요청 수신
- 같은 지식베이스와 같은 MCP 도구를 공유

즉, 개인용은 CLI, 조직용은 Gateway가 맞습니다.

---

## 3. 우리에게 맞는 추천 운영 방식

대표가 원하는 "여러 직원이 쓰는 구조"를 기준으로 하면 아래 조합이 현실적입니다.

### 1단계

- 문서 원본은 GitHub 저장소
- Quartz는 읽기 포털
- 핵심 담당자는 로컬에서 Hermes CLI 사용

### 2단계

- Hermes Agent Gateway를 운영 서버에 올림
- 직원은 메신저나 API로 Hermes에 요청
- Hermes는 같은 지식베이스를 읽고, 허용된 범위에서 초안이나 PR 생성

### 3단계

- MCP로 GitHub, 검색엔진, 내부 API를 연결
- 필요하면 Decap CMS로 비개발자 웹 편집 추가

---

## 4. MCP는 Hermes와 어떤 관계인가

이 부분을 헷갈리면 안 됩니다.

- Hermes Agent: 실제로 추론하고 행동하는 에이전트
- MCP: Hermes가 외부 도구를 붙일 때 쓰는 표준 프로토콜

공식 문서 기준으로 Hermes는:

- 로컬 `stdio` MCP 서버
- 원격 `HTTP` MCP 서버

를 같은 설정에서 함께 다룰 수 있습니다.

즉, MCP만 따로 보는 게 아니라, **Hermes를 중심에 두고 MCP를 붙이는 구조**가 맞습니다.

---

## 5. 직원들이 어떻게 쓰게 할 것인가

여러 직원이 쓰게 하려면 CLI를 전 직원에게 강제할 필요는 없습니다.

권장 분리:

- 문서 담당자/파워유저: Hermes CLI
- 일반 직원: Hermes Gateway 또는 웹 편집 UI
- 운영자: Web Dashboard / config 관리

이렇게 나누면 학습비용이 낮아집니다.

---

## 6. Quartz와 같이 쓰는 게 맞나

맞습니다. 오히려 같이 써야 역할이 분리됩니다.

- Quartz만 쓰면: 읽기 포털은 좋지만 작업 자동화가 약함
- Hermes만 쓰면: 작업 자동화는 되지만 조직 전체 열람 포털이 약함

둘을 같이 두면:

- Quartz는 읽기/탐색
- Hermes는 작성/검색/자동화

로 역할이 명확해집니다.

---

## 7. 최종 추천

현재 가장 실용적인 조합은 이겁니다.

**Git + Markdown을 원본으로 두고, Quartz를 조회 포털로 유지하고, Hermes Agent를 실제 작업 런타임으로 두고, MCP는 Hermes 확장용으로 붙인다.**

그리고 비개발자 편집이 필요해지면 그때 Decap CMS를 추가합니다.

이렇게 해야:

- 원본이 단순하고
- CLI 기반 자동화가 가능하고
- 직원 전체 공유도 가능하고
- 유지보수 복잡도도 과하게 올라가지 않습니다
