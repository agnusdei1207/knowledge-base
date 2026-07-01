---
title: "LLM06 과도한 에이전시 (LLM06 Excessive Agency)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 148
---

# 📖 【암기용】 개념 완전 이해

> 목적: LLM06 과도한 에이전시를 권한·기능·자율성 관점에서 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: LLM Agent에 필요 이상 기능, 권한, 자율 실행을 부여해 피해 행위가 수행되는 취약점
- **왜 필요한가**: Agent는 메일 발송, DB 수정, 결제, 배포, 파일 삭제 같은 실제 시스템 동작을 수행하므로 모델 오류가 즉시 업무 피해로 연결될 수 있다.
- **핵심 직관**: LLM에게 "판단"을 맡기는 것과 "실행 권한"을 맡기는 것은 다른 문제이며, 실행 권한에는 전통 IAM 수준의 통제가 필요하다.

## 깊이 이해
- **배경·문제의식**: LLM 애플리케이션은 단순 답변에서 tool calling, plugin, workflow automation으로 이동하고 있다. 이때 모델은 의도 파악에는 유용하지만 권한 검증 주체로 설계되면 안 된다.
- **작동 원리**: 과도한 기능은 불필요한 도구 노출, 과도한 권한은 SELECT만 필요해도 DELETE 권한을 가진 계정 사용, 과도한 자율성은 고위험 행위를 사용자 확인 없이 실행하는 형태로 나타남.
- **비유**: 신입 직원에게 일정 조회 업무를 맡기면서 회사 법인카드, 인사 DB 삭제 권한, 외부 발송 권한을 모두 주는 상황과 같다.
- **구체 예시**: 회의 요약 Agent가 Gmail 읽기만 필요하지만 쓰기·삭제 권한까지 받으면, 프롬프트 인젝션이 "모든 고객에게 환불 메일 발송"을 유도할 수 있다.
- **흔한 오해·주의점**: Agent 성능 향상을 위해 도구를 많이 붙이는 것이 설계 성숙도는 아니다. 업무 목적별 tool allowlist, scope 제한, 승인 단계가 필요함.

## 연결 개념
- OWASP LLM Top 10 2025 — LLM06 Excessive Agency로 분류
- Zero Trust·Least Privilege — Agent 도구 권한 설계 원칙
- LLM01 Prompt Injection — 인젝션이 과도한 권한과 결합될 때 실제 피해로 확대

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: LLM06은 모델 환각 문제가 아니라 기능·권한·자율성 과다 부여로 인한 실행 통제 실패이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LLM06 Excessive Agency는 Agent가 필요 범위를 넘는 도구 기능, 시스템 권한, 자동 실행 자율성을 가져 비인가 행위를 수행하는 취약점이다.
> 2. **가치**: 최소 권한, tool allowlist, transaction limit, human approval을 적용하면 모델 오류가 실제 변경 작업으로 전파되는 경로를 차단함.
> 3. **판단 포인트**: "모델이 잘 판단"하는지보다 "실행 전에 독립 통제 지점이 있는지"를 기능·권한·자율성 3축으로 점검해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Agent 보안 구조 이해 확인 | excessive functionality, permissions, autonomy 3축 | Agent를 단순 챗봇 보안으로 설명하지 않음 |
| 실행 권한 통제 설계 확인 | RBAC/ABAC, OAuth scope, allowlist, approval workflow | 프롬프트 정책만으로 실행 통제를 대체하지 않음 |
| 운영·감사 기준 확인 | tool call 로그, 승인 이력, transaction limit | 실제 피해 행위와 지표를 연결하지 않으면 감점 |

> 요약: 이 문제는 Agent에 붙은 도구의 권한과 자동 실행 범위를 최소화하는 설계 역량을 확인한다.

---

## Ⅰ. 개요 및 필요성

- 개요: LLM06 권한 과다 위임
- 배경: Agent는 자연어 판단 후 API 호출, DB 변경, 메일 발송, 결제 같은 행위를 수행함.
- 필요성: OWASP LLM06 기준으로 최소권한, human-in-the-loop 승인, 트랜잭션 한도, 실행 로그를 도구별로 적용해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
User Goal -> Planner LLM -> Tool Selector -> Policy Engine
                        +-> Tool Registry / OAuth Scope
Policy Engine -> Approval / Sandbox -> Execution API -> Audit Log
```

| 구성요소 | 역할 | 통제 포인트 |
|:---|:---|:---|
| Planner LLM | 목표를 작업 계획으로 분해 | 고위험 intent 분류, step limit |
| Tool Registry | Agent가 호출 가능한 도구 목록 | 업무별 allowlist, 미사용 tool 제거 |
| 권한 범위 | API·DB·파일 시스템 접근 권한 | OAuth scope, RBAC/ABAC, read-only 기본값 |
| Policy Engine | 실행 전 정책 판단 | 금액 한도, 삭제 차단, 승인 조건 |
| Audit Log | 계획·승인·실행 결과 기록 | tool call ID, actor, before/after 값 |

> 요약: LLM06 방어 구조는 Agent 판단 뒤에 정책 엔진과 승인 단계를 두어 실제 실행 권한을 분리하는 방식이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
사용자 목표 입력 -> 작업 계획 생성 -> 도구 선택
-> 권한·위험도 평가 -> 승인/샌드박스 실행 -> 실제 API 호출 -> 감사 로그 저장
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 사용자 요청을 intent와 risk level로 분류 | read/write/delete/payment 구분 |
| 2 | 필요한 도구와 파라미터 생성 | tool schema, allowlist 일치 |
| 3 | 권한 범위와 transaction limit 검증 | OAuth scope, 금액·건수·시간 한도 |
| 4 | 고위험 행위 승인 또는 dry-run 수행 | approval ID, diff preview |
| 5 | 실행 후 결과와 로그 보존 | before/after hash, 실패 rollback |

> 요약: Agent 실행은 계획-선택-검증-승인-실행 순서로 분리해야 하며, LLM은 최종 권한 판정 주체가 아니다.

---

## Ⅳ. 특징

| 구분 | 단순 LLM 챗봇 | LLM06 과도한 에이전시 | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 영향 범위 | 잘못된 답변 | 파일 삭제, 결제, 메일 발송, DB 변경 | write/delete/payment API |
| 위험 원인 | 환각·오답 | 기능 과다, 권한 과다, 자율성 과다 | OWASP LLM06 3축 |
| 통제 방식 | 출력 검증 | IAM, policy engine, approval workflow | OAuth scope, RBAC/ABAC |
| 감사 기준 | 대화 로그 | 계획·도구·승인·실행 로그 | tool call trace 100% |

> 요약: LLM06은 답변 품질 문제가 아니라 권한 있는 도구 실행을 통제하지 못하는 애플리케이션 보안 문제이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 사람이 UI에서 직접 실행 | Agent가 API를 자동 호출 | write/delete/payment 포함 시 정책 엔진 필수 |
| 권한 | 단일 서비스 계정 | 사용자 위임 토큰+scope 제한 | 사용자별 감사가 필요하면 위임 토큰 선택 |
| 운영 | 사후 로그 확인 | 사전 승인+실시간 차단 | 고위험 행위 월 1건 이상이면 approval workflow 적용 |

> 요약: Agent가 읽기만 수행하면 scope 제한 중심, 변경·결제·삭제를 수행하면 승인과 실행 한도가 필수이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 불필요한 도구 호출 | tool registry 과다 | 업무별 allowlist, 미사용 tool 제거 | unused tool 0개 |
| 권한 초과 변경 | 서비스 계정 권한 과다 | read-only 기본값, scope별 토큰 | denied write call 건수 |
| 무승인 고위험 실행 | 자율성 과다 | 금액·건수 limit, 2단계 승인 | high-risk approval rate 100% |

> 요약: 기능·권한·자율성 과다를 각각 도구 수, 거부된 쓰기 호출, 고위험 승인율로 측정한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 최소 권한 | Agent scope와 업무 권한 1:1 매핑 | IAM review, OAuth consent audit |
| 실행 통제 | delete/payment 승인율 100% | approval log, policy decision log |
| 복구 가능성 | rollback 가능한 변경 95% 이상 | transaction log, backup restore test |

> 요약: LLM06 통제 효과는 권한 매핑, 고위험 승인율, rollback 가능 변경 비율로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 기능 축소: Agent별 tool registry를 업무 단위로 분리하고 읽기 전용 Agent와 변경 Agent를 별도 배포
2. 권한 제한: OAuth scope를 `read`, `write`, `delete`, `payment`로 분리하고 기본 토큰은 `read`만 허용
3. 자율성 통제: 삭제·송금·외부 발송은 dry-run diff와 승인 ID를 요구하고, 실행 건수·금액·시간대 limit 적용

**결론 (2줄):**
- 기술사 판단: 검색·요약 Agent는 최소 권한으로 충분하나, 업무 실행 Agent는 정책 엔진·승인·rollback 체계를 전제해야 함
- 향후 방향: 멀티 Agent와 MCP 기반 도구 연동 확산에 따라 Agent IAM과 tool call 감사 표준화가 필요함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "과도한 에이전시를 설명하시오", "기술하시오" | 기능·권한·자율성 3축 동작 흐름 | 챗봇과 Agent 실행 위험 차이 |
| 요구사항 명시형 | "Agent 보안 방안을 제시하시오", "설계하시오", "비교하시오" | 정책 엔진·승인·rollback 흐름 | 최소 권한·승인 기준·감사 지표 |

> 요약: 설명형은 3축 개념을, 설계형은 실행 전 통제와 감사 가능성을 중심으로 목차를 전환한다.
