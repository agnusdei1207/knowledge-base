---
title: "AX Company 자율 AI 팀 시스템 구현계획"
tags:
  - "work"
  - "planning"
  - "ax-company"
  - "ai-agent"
  - "automation"
---

# AX Company 자율 AI 팀 시스템 구현계획

버전: 0.1.0  
작성일: 2026-06-05  
런타임: Node.js LTS 24  
지식베이스: Quartz 5  
인프라: GitHub Actions, GitHub API, GitHub Pages  
현재 기본 모델: MiniMax M3, 중앙 설정으로 교체 가능

## 한 줄 요약

Quartz를 AI가 읽는 운영 두뇌로 삼고, GitHub을 실행 신경망으로, 모델 라우터를 판단 엔진으로 사용해 스스로 감지하고, 판단하고, 실행하고, 학습하는 AX Company용 AI 팀 시스템을 만든다.

## 시스템 철학

이 시스템의 핵심은 코드보다 기록이다. 판단, 대화, 실행 결과, 실패 원인을 모두 Markdown으로 남겨 Quartz에 축적한다. Agent는 이 기록을 다시 읽어 다음 실행의 컨텍스트로 사용한다.

핵심 원칙:

- 데이터는 영구 보존한다. 모든 판단과 결과는 Markdown과 Git에 남긴다.
- 소프트웨어는 교체 가능하게 둔다. 모델과 실행 코드는 바뀌어도 `/brain`의 맥락은 유지한다.
- 모델은 중앙 설정으로 교체한다. `agents/model.config.ts`를 전체 Agent의 단일 모델 설정점으로 둔다.
- 사람은 고위험 작업만 승인한다. LOW/MEDIUM은 자율 실행하고 HIGH는 GitHub Issue 승인 플로우를 탄다.
- 루프는 자동으로 돈다. GitHub Actions Cron으로 센서, 모니터, 자기개선 루프를 운영한다.

## 5-Layer 구조

```text
Layer 5  학습 메커니즘    Quartz KB 자동 업데이트, Skill 개선 PR
Layer 4  품질 게이트      Human Approval, Eval, 위험도 분류
Layer 3  도구 레이어      GitHub, Gmail, Calendar, 외부 API
Layer 2  정책/결정 레이어 Skills, Model Router, Risk Policy
Layer 1  센서 레이어      이메일, PR, Issue, Calendar, RSS, Webhook
```

## 전체 아키텍처

```text
외부 신호
  ├─ Gmail
  ├─ GitHub Issues / PR / Commits
  ├─ Google Calendar
  └─ RSS / Webhook
        |
        v
GitHub Repository
  ├─ content/work 또는 brain
  │   ├─ skills
  │   ├─ context
  │   ├─ memory
  │   ├─ inbox
  │   └─ logs
  ├─ agents
  │   ├─ model.config.ts
  │   ├─ sensor.ts
  │   ├─ orchestrator.ts
  │   ├─ executor.ts
  │   ├─ monitor.ts
  │   └─ self-improver.ts
  └─ .github/workflows
        |
        v
Model Router
  ├─ minimax
  ├─ openai
  ├─ anthropic
  ├─ google
  └─ local
```

## 모델 중앙 교체 시스템

모든 Agent는 Provider를 직접 호출하지 않고 `callModel()`만 사용한다. 모델 교체는 `MODEL_CONFIG` 또는 GitHub Actions Variables로 처리한다.

```ts
export const MODEL_CONFIG = {
  provider: "minimax",
  model: "MiniMax-M3",
  overrides: {
    "code-generation": { provider: "anthropic", model: "claude-sonnet-4-6" },
    summarization: { provider: "minimax", model: "MiniMax-M3" },
    monitoring: { provider: "minimax", model: "MiniMax-M3" },
  },
  defaults: {
    temperature: 0.3,
    max_tokens: 4096,
  },
} satisfies ModelConfig
```

```ts
export async function callModel(task: TaskType, messages: Message[], systemPrompt: string) {
  const config = getConfigForTask(task)
  return PROVIDERS[config.provider].call({
    model: config.model,
    messages,
    system: systemPrompt,
    ...config.defaults,
  })
}
```

## 지식베이스 구조

초기 구현은 현재 Quartz 저장소의 `content/work` 아래에 AX Company 운영 문서를 축적하고, Agent 전용 실행 로그와 장기 기억이 커지면 `/brain` 또는 `content/brain`으로 분리한다.

권장 구조:

```text
brain
├─ skills
│  ├─ email-triage.md
│  ├─ pr-review.md
│  ├─ daily-report.md
│  └─ task-prioritize.md
├─ context
│  ├─ ax-company.md
│  ├─ current-goals.md
│  ├─ tech-stack.md
│  └─ people.md
├─ memory
│  ├─ decisions
│  ├─ patterns
│  └─ failed
├─ inbox
│  ├─ emails
│  ├─ issues
│  └─ signals
└─ logs
```

운영 원칙:

- 원본 맥락은 Markdown과 Git을 소스 오브 트루스로 둔다.
- 검색 인덱스와 벡터 DB는 언제든 재생성 가능한 파생 데이터로 둔다.
- Agent가 실행한 작업은 `logs`와 `memory`에 반드시 남긴다.
- 사람에게 보여야 하는 의사결정은 Work 문서로 승격한다.

## Agent 역할 분담

### 1. Sensor

트리거: GitHub Actions Cron, 30분 주기

역할:

- Gmail API로 미읽은 이메일 수집
- GitHub API로 새 Issue, PR, Mention 수집
- Google Calendar로 오늘/내일 일정 수집
- RSS, Webhook, 외부 API 신호 수집
- 수집 결과를 `inbox/signals/YYYY-MM-DD-HH.md`로 저장

### 2. Orchestrator

트리거: Sensor 완료 후 실행

역할:

- `skills`, `context`, `memory`를 읽어 실행 컨텍스트 구성
- 수집 신호를 작업 목록으로 변환
- 작업별 위험도를 LOW, MEDIUM, HIGH로 분류
- LOW/MEDIUM은 Executor에 위임
- HIGH는 승인 요청 Issue를 생성

### 3. Executor

트리거: Orchestrator 위임 또는 승인 완료

역할:

- 이메일 초안 생성
- 코드 변경 브랜치 생성 및 PR 오픈
- 문서 요약, 분류, 링크 정리
- 데일리 리포트 생성
- 일정 및 리마인더 생성
- 실행 결과를 logs에 기록

초기 안전장치:

- 이메일은 발송이 아니라 Draft 생성까지만 허용한다.
- main 직접 push는 금지하고 PR 중심으로 실행한다.
- 외부 발송, 결제, 삭제, 권한 변경은 HIGH로 분류한다.

### 4. Monitor

트리거: 매일 새벽 2시

역할:

- 전날 실행 결과 분석
- 성공/실패 패턴 추출
- 실패 원인과 부족한 Skill 식별
- Skill 개선 PR 생성
- `memory/patterns` 업데이트

### 5. Self-Improver

트리거: Monitor PR 머지 후 또는 주 1회

역할:

- 장기 기억 분석
- 낡은 context 갱신 제안
- 새 Skill 초안 생성
- 모델 성능 비교 리포트 작성
- Quartz 구조 개선 PR 생성

## GitHub Actions 설계

```yaml
name: AI Team

on:
  schedule:
    - cron: "*/30 * * * *"
    - cron: "0 2 * * *"
  issues:
    types: [labeled]
  workflow_dispatch:

jobs:
  sensor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with:
          node-version: "24"
      - run: npm ci
      - run: npm run ai:sensor
        env:
          GMAIL_TOKEN: ${{ secrets.GMAIL_TOKEN }}
          GCAL_TOKEN: ${{ secrets.GCAL_TOKEN }}
          MODEL_PROVIDER: ${{ vars.MODEL_PROVIDER }}
          MODEL_NAME: ${{ vars.MODEL_NAME }}
          MINIMAX_API_KEY: ${{ secrets.MINIMAX_API_KEY }}

  orchestrator:
    needs: sensor
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - run: npm ci
      - run: npm run ai:orchestrator

  executor:
    needs: orchestrator
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - run: npm ci
      - run: npm run ai:executor
```

## 추천 스택

| 영역          | 선택                                             |
| ------------- | ------------------------------------------------ |
| 지식베이스    | Quartz 5, GitHub Pages                           |
| 원본 저장     | Markdown, Git                                    |
| 컨텍스트 검색 | 초기: Markdown 검색, 확장: LanceDB 또는 pgvector |
| 단기 메모리   | GitHub Issues                                    |
| 장기 메모리   | `brain/memory/*.md`                              |
| 스케줄러      | GitHub Actions Cron                              |
| 승인 플로우   | GitHub Issues + Label                            |
| 알림          | Gmail Draft / 자기 자신에게 이메일               |
| 모델          | MiniMax M3 기본, 중앙 라우터로 교체              |
| 런타임        | Node.js 24 + TypeScript                          |

## 구현 로드맵

### Phase 1. 두뇌 만들기

- `agents/model.config.ts` 작성
- Provider 인터페이스와 MiniMax 호출 테스트
- `brain` 또는 `content/work/ax-company` 구조 확정
- 초기 Skill 문서 작성
- 수동 실행용 `workflow_dispatch` 파이프라인 구성

### Phase 2. 센서 붙이기

- Gmail API 수집
- GitHub Issues, PR, Mention 수집
- Calendar 수집
- 수집 결과 Markdown 저장
- 30분 Cron 검증

### Phase 3. 판단과 실행

- Orchestrator 위험도 분류 구현
- Executor 이메일 Draft 생성
- 문서 정리 및 리포트 생성
- HIGH 작업 승인 Issue 생성
- Label 승인 후 실행 플로우 연결

### Phase 4. 자기개선 루프

- Monitor 실행 결과 분석
- 실패 패턴 메모리화
- Skill 개선 PR 자동 생성
- LanceDB 또는 pgvector 기반 검색 확장
- 모델별 비용/품질 비교 리포트 자동화

## 리스크와 대응

| 리스크                        | 대응                                          |
| ----------------------------- | --------------------------------------------- |
| GitHub Actions 무료 한도 초과 | Cron 주기 조정, Cloudflare Workers 보조 검토  |
| API 키 노출                   | GitHub Secrets만 사용, 로그 마스킹            |
| Agent 오작동                  | Draft/PR 중심 운영, 직접 발송/삭제 금지       |
| 비용 폭주                     | max token 제한, 일일 사용량 로그              |
| 지식베이스 빌드 실패          | Agent 로그와 Quartz 배포를 분리 가능하게 설계 |
| 잘못된 자동 승인              | HIGH 작업은 Issue label 승인 없이는 실행 금지 |

## AX Company 제작 관점의 우선순위

1. 현재 Work 문서 체계를 AX Company의 운영 두뇌로 정리한다.
2. Agent가 읽을 수 있는 `skills`, `context`, `memory`, `logs` 경계를 만든다.
3. 모델 라우터와 Sensor를 먼저 만든다.
4. Executor는 이메일 Draft, 문서 정리, 리포트처럼 되돌리기 쉬운 작업부터 시작한다.
5. Monitor와 Self-Improver는 실행 로그가 쌓인 뒤 붙인다.

## 다음 액션

- [ ] `agents/` 디렉토리와 `model.config.ts` 스캐폴딩
- [ ] `ai:sensor`, `ai:orchestrator`, `ai:executor` npm script 추가
- [ ] `content/work/planning/projects.md`에서 AX Company 프로젝트를 활성 프로젝트로 관리
- [ ] 초기 Skill 4종 작성: 이메일 분류, PR 리뷰, 데일리 리포트, 작업 우선순위
- [ ] GitHub Actions `workflow_dispatch`로 수동 실행부터 검증
