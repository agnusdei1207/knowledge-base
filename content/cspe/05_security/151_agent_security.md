---
title: "에이전트 보안 — 권한 통제·가드레일 (Agent Security)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 151
---

# 📖 【암기용】 개념 완전 이해

> 목적: 에이전트 보안을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: AI 에이전트가 도구·데이터·권한을 사용할 때 오남용을 막는 통제 체계
- **왜 필요한가**: 에이전트는 LLM 답변 생성에서 끝나지 않고 API 호출, 파일 수정, 결제, 코드 실행까지 수행한다. 프롬프트 인젝션 한 줄이 실제 시스템 변경으로 이어질 수 있다.
- **핵심 직관**: 사람 직원에게 사원증·업무범위·결재선을 주듯, 에이전트에도 신원·권한·승인·감사를 부여해야 한다.

## 깊이 이해
- **배경·문제의식**: 기존 챗봇 보안은 입력 필터링과 출력 검증 중심이었다. 에이전트는 장기 목표, 메모리, 도구 호출, 다단계 계획을 가지므로 OWASP LLM01 Prompt Injection, LLM06 Excessive Agency, LLM08 Vector and Embedding Weaknesses가 결합된다.
- **작동 원리**: 요청은 정책 엔진에서 목적·권한·데이터 등급을 평가하고, 도구 호출은 allowlist, 최소권한, human approval, 실행 로그를 거친다. 출력은 민감정보·정책 위반·명령 실행 결과를 다시 검사한다.
- **비유**: 신입 사원이 회계 시스템을 쓸 때 조회는 허용하고 송금은 결재자를 요구하는 방식과 같다. 에이전트도 읽기·쓰기·외부전송을 분리해야 한다.
- **구체 예시**: 고객지원 에이전트는 CRM 조회 권한만 갖고, 환불 API는 10만 원 이하 자동 처리, 10만 원 초과는 관리자 승인, 모든 호출은 trace id로 1년 보관한다.
- **흔한 오해·주의점**: "시스템 프롬프트를 숨기면 충분함"은 틀렸다. 모델은 지시를 해석하는 구성요소일 뿐이며, 실제 통제는 IAM, 정책 엔진, 도구 프록시, 감사 로그에서 수행해야 한다.

## 연결 개념
- 에이전트 샌드박스 격리 - 코드·파일·네트워크 실행 범위 제한
- OWASP Top 10 for LLM Applications - 프롬프트 인젝션·과도한 권한·공급망 위험 분류
- Zero Trust - 사용자·에이전트·도구 호출을 매번 인증·인가·기록

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 에이전트 보안은 프롬프트 필터가 아니라 신원, 권한, 도구, 메모리, 감사 로그를 묶은 실행 통제 문제임.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 에이전트 보안은 AI 에이전트의 목표 수립, 도구 호출, 데이터 접근, 결과 실행을 정책 기반으로 제한하는 보안 아키텍처임.
> 2. **가치**: 프롬프트 인젝션이 API 호출·파일 변경·외부 전송으로 확산되는 경로를 IAM, PDP/PEP, 승인 워크플로, 감사 로그로 차단함.
> 3. **판단 포인트**: 자율성 수준이 높을수록 권한 수명, 네트워크 egress, tool allowlist, human-in-the-loop 기준을 수치화해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| AI 에이전트 공격면 식별 | Prompt Injection, Tool Misuse, Excessive Agency, Memory Poisoning | 챗봇 입력 필터만 적고 도구 권한을 누락 |
| 권한 통제 설계 역량 확인 | Agent Identity, OAuth 2.1, RBAC/ABAC, PDP/PEP, JIT 권한 | 관리자 토큰 공유, 장기 토큰 사용을 허용 |
| 운영·감사 판단 확인 | 승인 임계값, trace id, tamper-evident log, red team 평가 | 로그 보관·사후 추적 지표 누락 |

> 요약: 이 문제는 에이전트 자율성을 권한·도구·감사 통제로 분해해 실행 위험을 줄이는 설계 역량을 요구함.

---

## Ⅰ. 개요 및 필요성

- 개요: AI 에이전트 실행권한 통제 체계
- 배경: LLM 기반 에이전트는 검색·코드 실행·결제·업무시스템 변경을 수행하므로 프롬프트 공격이 실제 행위로 전이된다.
- 필요성: Zero Trust 원칙에 따라 도구 호출별 신원·권한·승인·감사로그를 분리해 오동작과 권한 오남용을 추적 가능하게 해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
User Request -> Agent Runtime -> Policy Enforcement Point -> Tool Proxy -> Enterprise API
                    +-> Memory Guard
                    +-> Human Approval
                    +-> Audit Log
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Agent Identity | 에이전트별 서비스 계정·목적·소유자 식별 | OAuth 2.1, mTLS, short-lived token |
| Policy Engine | 요청 목적·데이터 등급·도구 위험도 평가 | OPA/Rego, ABAC, deny-by-default |
| Tool Proxy | API 호출 allowlist, 파라미터 검증, egress 제한 | 읽기/쓰기 분리, rate limit |
| Guardrail | 입력·출력·중간 계획 검증 | PII 탐지, 명령 실행 차단, jailbreak 탐지 |
| Audit Layer | 행위 로그·승인 이력·재현 정보 저장 | trace id, WORM log, SIEM 연동 |

> 요약: 에이전트 보안 구조는 모델 앞 필터가 아니라 런타임과 도구 사이의 정책 집행 지점이 중심임.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 -> 목적/권한 평가 -> 계획 생성 -> 도구 호출 심사
-> 승인/차단/실행 -> 출력 검증 -> 로그 저장
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 사용자·에이전트·세션 신원 확인 | mTLS, OAuth scope, MFA 연계 |
| 2 | 작업 목표와 데이터 등급 매핑 | 공개/내부/기밀/개인정보 등급 |
| 3 | 도구 호출 전 파라미터·위험도 검사 | allowlist, schema validation, egress policy |
| 4 | 고위험 행위 승인 또는 차단 | 금액 10만 원 초과, 삭제·배포·외부전송 승인 |
| 5 | 결과 출력과 행위 로그 보존 | PII masking, trace id, 1년 이상 감사 |

> 요약: 에이전트 실행은 신원 확인에서 시작해 도구 호출 전후 정책 평가와 감사 로그로 폐쇄 루프를 구성함.

---

## Ⅳ. 특징

| 구분 | 기존 챗봇 보안 | 에이전트 보안 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 공격면 | 입력·출력 텍스트 | 도구, 메모리, API, 파일, 네트워크 | OWASP LLM01·LLM06·LLM07 |
| 권한 | 사용자 세션 중심 | 에이전트 identity와 delegated scope | OAuth 2.1, RBAC/ABAC |
| 통제 위치 | 프롬프트 필터 | PEP, Tool Proxy, Sandbox | deny-by-default, allowlist 100% |
| 검증 | 답변 품질 평가 | 행위 추적·재현·승인 이력 | trace coverage 100%, audit retention 1년 |

> 요약: 에이전트 보안은 답변 검열보다 실행 권한과 도구 호출을 정책으로 제한하는 점이 기존 챗봇 보안과 다름.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 프롬프트 기반 금지문 | IAM+PDP/PEP+Tool Proxy | 외부 API·파일 쓰기 권한이 있으면 필수 |
| 권한 | 장기 API Key | short-lived token, JIT scope | 토큰 TTL 15분 이하, scope 최소화 |
| 운영 | 사후 장애 대응 | red team, policy test, audit replay | 월 1회 공격 시나리오 30개 이상 검증 |

> 요약: 에이전트가 업무시스템을 변경하면 프롬프트 규칙이 아니라 실행 경로의 정책 집행으로 통제해야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Prompt Injection | 외부 문서가 에이전트 지시를 덮어씀 | system/user/tool context 분리, instruction hierarchy 검사 | injection 성공률 1% 이하 |
| Tool Misuse | 과도한 API 권한과 파라미터 검증 누락 | tool allowlist, schema validation, dry-run | 차단된 위험 호출 수 |
| Memory Poisoning | 장기 메모리에 악성 지시 저장 | memory write approval, TTL, source tagging | 검증 없는 메모리 0건 |
| 감사 불가 | 중간 계획·도구 호출 로그 누락 | trace id, immutable log, SIEM 전송 | trace coverage 100% |

> 요약: 주요 리스크는 지시 오염과 과도한 실행권한이며, 호출 전 검증과 호출 후 감사로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 권한 최소화 | scope당 API 5개 이하, TTL 15분 이하 | IAM 정책 점검, 토큰 샘플링 |
| 가드레일 탐지 | jailbreak·PII 테스트 100개 중 탐지율 95% 이상 | red team dataset, offline eval |
| 실행 추적 | tool call, approval, output 로그 100% 연결 | trace id join, SIEM query |
| 운영 복구 | 오동작 차단 후 MTTR 30분 이하 | runbook drill, incident ticket |

> 요약: 도입 성공은 권한 범위, 공격 탐지율, 실행 추적률, 복구 시간으로 검증해야 함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. Agent Gateway 구성: 모든 도구 호출을 단일 PEP로 통과시키고 OPA 정책, schema validation, egress allowlist 적용
2. 권한 모델 분리: 사용자 권한과 에이전트 권한을 분리하고 OAuth scope, JIT token, 금액·삭제·배포 승인 기준 수립
3. 검증 체계 운영: OWASP LLM Top 10 기반 red team 30개 시나리오, trace coverage 100%, WORM 로그 1년 보관

**결론 (2줄):**
- 기술사 판단: 읽기 전용 보조 에이전트는 guardrail 중심, 쓰기·배포·결제 에이전트는 IAM+PEP+승인 워크플로를 필수로 둠
- 향후 방향: 에이전트 보안은 MCP 도구 권한, 기업 IAM, 감사 표준을 결합한 런타임 거버넌스로 발전함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "에이전트 보안을 설명하시오", "기술하시오" | 신원 확인, 정책 평가, 도구 호출, 감사 흐름 | 챗봇 보안과 에이전트 실행 통제 차이 |
| 요구사항 명시형 | "권한 통제 방안을 제시하시오", "설계하시오" | PDP/PEP, Tool Proxy, human approval 설계 | scope, TTL, 승인 임계값, 로그 지표 |

> 요약: 설명형은 공격면과 구조를 넓게 쓰고, 설계형은 권한 범위와 정책 집행 지점을 수치로 제시함.
