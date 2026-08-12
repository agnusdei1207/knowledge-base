---
sidebar:
  order: 90
  label: "090. 에이전트 보안 — 권한 통제•가드레일 (Agent Security)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "에이전트 보안 — 권한 통제•가드레일 (Agent Security)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-security"
weight: 90
extra:
  question_no: "090"
  source_status: "기출"
  source_history: "138회"
  priority: 85
  priority_note: "138회 에이전트 설계 흐름과 권한 오남용이 직결됨"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **에이전트 보안(Agent Security)**: 단순 대화형 LLM 챗봇을 넘어, 자율적으로 계획(Planning)하고 외부 도구(API, DB, OS Command)를 실행하는 AI 자율 에이전트의 권한 과다(Excessive Agency), 비인가 시스템 조작, 과금 폭주를 방어하는 보안 통제 아키텍처이다.
- **AI(Artificial Intelligence)**: 트랜스포머 알고리즘을 바탕으로 추론, 툴 호출, 자율 에이전트 과업을 수행하는 지능형 시스템이다.
- **출력과 행동의 차이(Output vs. Action Distinction)**: 단순 텍스트 응답 출력과 달리, 외부 시스템의 실제 상태 변경(State Modification: 결제, 파일 삭제, 메일 발송)을 야기하는 에이전트 특유의 본질적 위험 차이점이다.

</details>

- 정의/개념: 에이전트 보안(Agent Security)은 AI 에이전트가 LLM 추론을 바탕으로 외부 API/DB/시스템 명령을 실행할 때, 오판이나 간접 인젝션 공격에 의한 비인가 시스템 상태 조작을 막기 위해 샌드박싱, 최소 권한 IAM, PEP 정책 검증, Human-in-the-Loop 관문을 통합 집행하는 런타임 보안 체계이다.
- 배경/필요성: AI 에이전트에게 무제한 DB 삭제, 자금 이체, 외부 메일 전송 권한이 위임될 경우, 프롬프트 인젝션 한 번으로 기업 인프라가 붕괴되는 **출력과 행동의 차이** 위험에 노출되기 때문이다.

#### 한줄 요약

- 자율적 툴 실행과 상태 변경을 야기하는 AI 에이전트의 비인가 시스템 조작 및 과도한 권한 오남용을 통제하는 보안 체계이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **완전 매개(Complete Mediation)**: 에이전트의 모든 도구 호출(Tool Call) 요청을 게이트웨이(PEP)가 100% 바이패스 없이 인터셉트하여 인가 여부를 2차 검증하는 보안 원칙이다.
- **최소 권한(Least Privilege)**: 에이전트에 과업 수행에 필요로 하는 최적의 API 기능 및 최소 읽기/쓰기 스코프만을 부여하는 인가 원칙이다.
- **제한 토큰(Scope-bounded / Ephemeral Tokens)**: 에이전트가 툴 호출 시 사용자의 전체 권한이 아닌, 특정 1회성 작업과 짧은 수명(TTL)을 가진 제한된 OAuth/API 토큰이다.
- **보상 동작(Compensating Action / Saga Pattern)**: 에이전트의 연쇄 작업 실패 시 이미 집행된 외부 시스템 상태 변경을 원상태로 되돌리는 취소/원복 트랜잭션 기법이다.

</details>

- 에이전트가 생성한 추론 계획과 도구 호출 인자를 100% 비신뢰(Zero Trust) 객체로 취급한다.
- 게이트웨이 레벨의 **완전 매개** 및 **최소 권한** 기반 **제한 토큰**을 적용하여 과도한 자율 권한 부여를 차단한다.
- 고위험 실행 전 팝업 승인(Human-in-the-Loop) 및 장애 시 **보상 동작**을 통해 잔여 손상 피해를 최소화한다.

#### 한줄 요약

- 추론 제안 비신뢰 격리, 완전 매개 및 최소 권한 제한 토큰 부여, Human-in-the-Loop 팝업 및 보상 동작 원복 특성을 지닌다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>
- **도구 등록부(Tool Registry / Schema Store)**: 에이전트가 호출할 수 있는 검증된 외부 API 함수, 파라미터 스키마, 위험 등급(High/Low Risk)을 등록 관리하는 레포지토리이다.
- **PEP(Policy Enforcement Point)**: LLM이 도출한 Tool Call 요청이 사용자의 IAM 최소 권한 범위 및 파라미터 유효성 기준에 적합한지 런타임 심사하는 통제 관문이다.
- **감사 계층(Audit Trail / Traceability Layer)**: 에이전트의 프롬프트 수신부터 툴 실행, 반환 결과, 상태 변경 이력을 비가역 감사 로그로 기록 관리하는 계층이다.
- **복구 계층(Recovery & Rollback Layer)**: 연쇄 실행 중 에이전트 오류나 공격 감지 시 이전 안전 상태로 트랜잭션을 롤백 조치하는 계층이다.

</details>

```text
에이전트 실행 통제
├─ 요청·계획 경계
│  ├─ 신원·위임 계층
│  └─ 계획·메모리 계층
├─ 실행 경계
│  ├─ 도구 등록부
│  └─ 정책 집행점
└─ 사후 경계
   └─ 감사·복구 계층
```

선의 의미: 요청/계획 경계, 도구 등록부와 PEP가 위치한 실행 경계 및 감사/복구 계층 사후 경계의 3단계 에이전트 보안 통제 구조이다.

| 통제 레이어 | 구성 요소 | 핵심 기능 및 역할 |
|:---|:---|:---|
| 요청·계획 경계 | 신원·위임 계층, 계획·메모리 계층 | 사용자 신원 인증, 1회성 **제한 토큰** 발급 및 비신뢰 메모리/프롬프트 격리 |
| 실행 경계 | **도구 등록부**, **PEP** (Policy Enforcement Point) | **도구 등록부** 스키마 대조, **PEP** 관문을 통한 Tool Call 인자값 및 사용자 최소 권한 2차 대조 |
| 사후 경계 | **감사 계층**, **복구 계층** | 비가역 **감사 계층** 추적 로그 저장, **보상 동작**을 이용한 연쇄 실행 **복구 계층** 작동 |

#### 한줄 요약

- 요청/계획 경계(제한 토큰), 실행 경계(도구 등록부, PEP) 및 사후 경계(감사 계층, 복구 계층)로 구성된다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **거래 결속(Transaction Binding)**: 사용자가 최초 요청 및 승인한 파라미터(이체 수신자, 금액, 삭제 대상 등)를 세션에 결속하여 에이전트가 다른 인자로 조작하지 못하게 동결하는 기술이다.
- **단계 중단(Step-wise Interruption / Execution Halt)**: 연쇄 툴 실행 도중 특정 단계에서 에러나 이상 행동 감지 시 다음 단계 집행을 즉각 정지시키는 관문이다.
- **복구(State Recovery / Remediation)**: 오작동된 툴 호출의 상태 변경을 이전 스냅샷 상태로 즉시 롤백시키는 조치이다.
- **계획•도구 호출 제안 생성(Plan & Tool Call Candidate Generation)**: LLM이 사용자의 요청을 달성하기 위한 단계별 실행 계획 및 API 호출 후보를 생성하는 단계이다.
- **거래 결속•정책 검증(Transaction Binding & Policy Validation)**: 사용자 승인 매개변수와 도출된 API 요청 인자를 거래 결속 대조하는 단계이다.
- **제한 토큰 도구 실행(Scope-bounded Token Tool Execution)**: 최단 유효기간의 1회성 제한 토큰을 툴에 부여하여 런타임 샌드박스에서 실행하는 단계이다.
- **실행 상태•감사 증적 검증(Execution State & Audit Verification)**: 도구 반환 결과를 검증하고 비가역 감사 로그에 기록하는 단계이다.
- **취소•보상 처리(Cancellation & Compensation Handling)**: 오류 발생 시 단계 중단 및 보상 동작 트랜잭션을 롤백 집행하는 단계이다.

</details>

```text
목적·권한·한도
       |
       v
1. 계획·도구 호출 제안 생성
       |
       v
고위험 행동 재승인 ── 거부 ──> 실행 중단
       |
      승인
       v
2. 거래 결속·정책 검증
       |
       v
3. 제한 토큰 도구 실행
       |
       v
4. 실행 상태·감사 증적 검증
       |
       ├─ 성공 ──> 실행 결과
       |
       └─ 실패 ──> 5. 취소·보상 처리
                              |
                              v
                         복구 결과
```

### 동작 원리

1. **계획•도구 호출 제안 생성**: LLM 추론 엔진이 자율적 툴 실행 계획 및 API 호출 인자를 생성한다. (고위험 액션 시 Human-in-the-Loop **사용자 재승인** 팝업 강제)
2. **거래 결속•정책 검증**: **거래 결속** 기술로 승인 인자를 동결하고 PEP 관문에서 인가 여부를 심사한다.
3. **제한 토큰 도구 실행**: 1회성 **제한 토큰**을 적용하여 샌드박스 인프라에서 외부 API를 호출한다.
4. **실행 상태•감사 증적 검증**: 툴 실행 결과를 반환받고 감사 이력 저장을 이행한다.
5. **취소•보상 처리**: 실행 실패 시 **단계 중단**을 가하고 Saga 패턴의 **보상 동작**으로 시스템 상태를 원복한다.

#### 한줄 요약

- 제안 생성, Human-in-the-Loop 승인, 거래 결속 및 PEP 검증, 제한 토큰 샌드박스 실행, 실패 시 취소/보상 원복 단계로 이행된다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **도구형 에이전트(Tool-augmented Autonomous Agent)**: 외부 API, DB, Shell 스크립트 실행 권한을 가진 자율 실행 AI 애플리케이션이다.
- **챗봇(Conversational Chatbot)**: 텍스트 및 대화 응답만을 도출하며 외부 시스템 상태 변경 권한이 없는 텍스트 생성 전용 모델이다.
- **RAG(Retrieval-Augmented Generation)**: 외부 벡터 지식베이스 검색 데이터를 프롬프트 문맥으로 조합해 응답을 도출하는 아키텍처이다.
- **ACL(Access Control List)**: 사용자/시스템의 자원 접근 인가 목록이다.

</details>

| AI 아키텍처 유형 | 일반 챗봇 (Conversational Chatbot) | RAG 서비스 (Retrieval-Augmented) | 도구형 에이전트 (Autonomous Agent) |
|:---|:---|:---|:---|
| 핵심 기능 | 자연어 텍스트 및 대화 응답 생성 | 벡터 DB 조회를 통한 정확 응답 도출 | 외부 API, DB, OS 명령 자율 집행 |
| 주요 위험 요소 | 프롬프트 인젝션, 윤리 위반, PII 유출 | RAG 문서 오염, 간접 인젝션, ACL 누락 | 과도한 대리권(**LLM06**), 비인가 상태 조작 |
| 주요 방어 포인트 | XML 프롬프트 격리, Input/Output WAF | RAG 벡터 ACL 동기화, 출처 메타데이터 검증 | **PEP** 게이트웨이, **제한 토큰**, **사용자 재승인** |
| 상태 변경 여부 | 없음 (Read-Only) | 없음 (Read-Only) | 있음 (**State Modification** 집행) |

#### 한줄 요약

- 챗봇(대화 전용), RAG(검색 전용), 도구형 에이전트(외부 자율 상태 변경 집행)로 구분되며 에이전트는 PEP 및 제한 토큰 통제가 필수적이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **OWASP(Open Worldwide Application Security Project)**: 글로벌 인터넷 애플리케이션 보안 표준화 기구이다.
- **LLM(Large Language Model)**: 대규모 언어 모델이다.
- **LLM06:2025 (OWASP Top 10 for LLM Applications 2025 - LLM06 Excessive Agency)**: 에이전트에 과도한 자율 실행 권한이 위임되어 발생하는 OWASP 2025 핵심 위험 규격이다.
- **샌드박스(Sandbox / Runtime Isolation)**: gVisor, Firecracker 등 에이전트가 실행하는 코드/명령어를 물리적으로 격리 집행하는 인프라 기술이다.
- **NIST(National Institute of Standards and Technology)**: 미국 국립표준기술연구소이다.
- **AI 600-1 (NIST Generative AI Profile, AI 600-1)**: 에이전트의 인간 감독(Human Oversight) 및 샌드박싱 방어 지침을 명시한 NIST 표준이다.
- **사용자 재승인(User Re-approval / Human-in-the-Loop)**: 금융 이체, DB 삭제, 메일 발송 등 비가역적 액션에 대해 인간의 최종 서명을 요구하는 절차이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 에이전트의 과도한 자율 권한 위임 사태 | **OWASP LLM06:2025** 및 **NIST AI 600-1** 준용 | 에이전트 권한의 최소화(Least Agency) 거버넌스 수립 |
| 비인가 툴 호출에 따른 시스템 상태 변조 | **거래 결속**, **PEP** 게이트웨이 및 **사용자 재승인** | 고위험 액션의 독단적 이행 원천 차단 및 인간 감독 확보 |
| 파이썬 코드/OS 명령어 실행 시 인프라 침해 | **샌드박스** (Firecracker/gVisor) 격리 및 Egress 통제 | 비인가 에이전트의 C2 서버 연결 및 시스템 파괴 차단 |

#### 한줄 요약

- OWASP LLM06:2025 및 NIST AI 600-1 지침 준수, 거래 결속, PEP, Human-in-the-Loop 및 샌드박스 격리를 수립한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **가역성 기반 승인(Reversibility-based Authorization Criteria)**: 툴 실행의 가역성(원복 가능 여부) 및 위험도에 따라 자동 승인과 인간 승인을 차등 적용하는 보안 가버넌스 원칙이다.

</details>

- **가역성 기반 승인** 원칙에 따라 가역적 조회는 **제한 토큰** 기반 자동화를 허용하고, 비가역적 변경은 **거래 결속** 및 **사용자 재승인** 관문을 적용한다.

#### 한줄 요약

- OWASP LLM06/NIST AI 600-1 준수, PEP 관문, 제한 토큰, 샌드박스, Human-in-the-Loop 및 가역성 기반 승인 중심 에이전트 보안 체계 구축 필수.