---
sidebar:
  order: 90
  label: "090. 에이전트 보안 — 권한 통제•가드레일 (Agent Security)"
  badge:
    text: "기출 · 85%"
    variant: note
title: "자율 에이전트 권한 과다 방지 및 런타임 가드레일 : 에이전트 보안 (OWASP LLM06:2025 & NIST AI 600-1)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-security"
weight: 90
extra:
  question_no: "090"
  source_status: "기출"
  source_history: "138회"
  priority: 85
  priority_note: "138회 최신 기출, OWASP Top 10 for LLM:2025 LLM06(Excessive Agency), 출력(Output) vs 행동(Action/State Change), 완전 매개(Complete Mediation), 거래 결속(Transaction Binding), Human-in-the-loop, 샌드박스(gVisor/Firecracker)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **에이전트 보안(Agent Security / NIST AI 600-1 & OWASP LLM06:2025)**: 단순 텍스트 생성 챗봇을 넘어, 스스로 다단계 실행 계획(Planning)을 수립하고 외부 API 호출, 데이터베이스 수정(SQL Execute), 운영체제 쉘 스크립트 실행 등 외부 환경의 물리적 상태 변경(State Modification)을 자율적으로 집행하는 AI 에이전트(Agentic AI)의 권한 과다(Excessive Agency), 도구 하이재킹(Tool Hijacking), 비인가 시스템 조작 사고를 방어 통제하는 아키텍처 체계.
- **출력과 행동의 본질적 차이(Output vs Action Distinction Defect)**: 단순 텍스트 환각(Hallucination)은 화면에 잘못된 문장을 출력하는 것에 그치지만, 도구 실행 권한을 가진 에이전트의 환각이나 프롬프트 인젝션 감염은 실제 고객 원장 데이터 삭제, 거액 무단 이체, 악성 메일 대량 발송 등 되돌릴 수 없는 불가역적 시스템 파괴(Irreversible State Change)로 직결되는 구조적 위험.

</details>

- 정의/개념: NIST AI 600-1 및 OWASP LLM06:2025에 입각하여 **신원 및 최소 권한 위임 $\rightarrow$ 도구 등록부(Tool Registry) 화이트리스트 스키마 검증 $\rightarrow$ 독립 정책 집행점(PEP)의 완전 매개(Complete Mediation) $\rightarrow$ 거래 결속(Transaction Binding) 및 Human-in-the-loop 승인 $\rightarrow$ 마이크로VM 샌드박스 실행** 을 집행하는 **자율 에이전트 런타임 보안 아키텍처**
- 배경/필요성: AI 에이전트에게 개발 편의를 위해 마스터 어드민(Admin) 권한이나 무제한 API 키를 부여할 경우, 간접 프롬프트 인젝션(Indirect Injection) 한 줄로 사내 인프라 전체가 장악되거나 데이터베이스가 영구 삭제되는 치명적 보안 참사를 방지할 요구

#### 한줄 요약
- 자율 에이전트의 비인가 도구 실행과 시스템 상태 파괴를 막기 위해 독립 PEP와 거래 결속 및 Human-in-the-loop를 적용한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **완전 매개 원칙 (Complete Mediation Principle)**: 에이전트가 생성한 모든 Tool Call(API 호출/SQL 쿼리) 요청을 백엔드 PEP(정책 집행점)가 100% 가로채어, 우회 경로 없이 실제 사용자의 최소 IAM 권한 및 파라미터 무결성을 2차 교차 검증하는 보안 원칙.
- **거래 결속 (Transaction Binding)**: 사용자가 최초 요청한 파라미터(예: 송금 수신자, 이체 금액)를 세션에 암호학적으로 동결 결속(Binding)하여, 에이전트가 인젝션 공격에 속아 임의로 수신 계좌나 금액을 변조하여 호출하는 것을 런타임에 원천 차단하는 기술.

</details>

- **Zero Trust 기반 도구 제안 비신뢰 취급**: 에이전트의 추론 결과 및 생성된 도구 호출 JSON은 신뢰할 수 없는(Untrusted) 객체로 취급하여 무조건 검증 관문 강제
- **단명 최소 권한 토큰 (Ephemeral Scoped Tokens)**: 마스터 API 키 대신 특정 단일 작업(1회성)에만 유효한 수분짜리 단기 OAuth 2.0 스코프 토큰을 발급하여 권한 남용 격리
- **가역성 기반 차등 승인 (Reversibility-based Control)**: 단순 조회(Read)는 자동 실행을 허용하되, 데이터 삭제/결제 등 비가역적(Irreversible) 상태 변경 액션은 반드시 인간 관리자의 최종 승인(Human-in-the-loop) 강제

#### 한줄 요약
- 완전 매개 통제, 거래 결속(Transaction Binding), 단명 최소 권한 토큰, 가역성 기반 Human-in-the-loop 승인을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **에이전트 보안 4대 통제 계층**:
  1. **Tool Registry & Schema Validator**: 화이트리스트 API 목록 및 파라미터 타입 강제.
  2. **Independent Policy Enforcement Point (PEP)**: 사용자 IAM 및 도구 실행 인가 엔진.
  3. **Human-in-the-loop Authorization Gateway**: 고위험 액션 시 인간 팝업 승인 관문.
  4. **MicroVM Execution Sandbox (gVisor / Firecracker)**: OS 커널 격리 도구 실행 런타임.

</details>

```text
[ 악의적 간접 인젝션 문서 or 사용자 요청 ]
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. 에이전트 추론 및 계획 계층 (Agent Planner: Zero Trust Boundary) ]  │
│  └─ LLM 에이전트가 도구 호출 제안 JSON 생성: `call_api(transfer_funds)`│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (비신뢰 Tool Call 제안 전달)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. 독립 정책 집행점 (Complete Mediation: PEP & Tool Registry) ]       │
│  ├─ 도구 등록부 대조: 허용된 화이트리스트 API 및 JSON 스키마 검증       │
│  ├─ 거래 결속(Binding) 대조: 사용자의 원본 요청 파라미터 일치 여부 확인│
│  └─ [ 권한 검증: 현재 세션의 IAM 최소 스코프(Scoped Token) 대조 ]       │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (고위험 액션: 100만 원 이상 이체 감지)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 3. 인간 개입 승인 관문 (Human-in-the-loop Approval Gateway) ]         │
│  ├─ 관리자 화면에 파라미터 명시적 확인 팝업 요청 (OTP/전자서명)        │
│  └─ [ 관리자 승인 획득 시에만 ➔ 1회성 단명 토큰(TTL: 60s) 발급 ]        │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (승인된 단명 토큰으로 실행)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 4. 격리 샌드박스 런타임 (MicroVM Sandbox: gVisor / Firecracker) ]     │
│  ├─ 호스트 OS 커널과 물리적 격리된 샌드박스에서 파이썬/SQL/API 실행     │
│  └─ [ 아웃바운드 Egress 방화벽: 비인가 외부 C2 서버 통신 원천 차단 ]   │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 에이전트의 비신뢰 도구 제안이 PEP에서 완전 매개 검증을 거치고, 고위험 액션 시 인간 승인을 받아 격리 샌드박스에서 실행되는 다층 방어 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **도구 등록부 (Tool Registry)**| 허용된 API 목록, 입출력 JSON Schema, 위험도 등급(Read/Write/Critical) 관리 | Schema Store |
| **정책 집행점 (PEP)** | 에이전트의 도구 호출을 가로채어 사용자 권한, 파라미터 무결성, 호출률을 2차 검증 | Complete Mediation |
| **거래 결속 엔진 (Binding)** | 사용자가 최초 의도한 인자값과 에이전트가 제출한 파라미터의 변조 여부를 락(Lock) 검증 | Anti-tampering |
| **Human-in-the-loop 관문**| 파괴적 상태 변경(DB Delete/결제) 실행 전 관리자의 명시적 서명 승인 강제 | Human Oversight|
| **마이크로VM 샌드박스** | gVisor, Firecracker를 통해 코드 실행을 호스트 커널로부터 물리적으로 격리 | Sandbox Core |

#### 한줄 요약
- 도구 등록부, 정책 집행점(PEP), 거래 결속 엔진, Human-in-the-loop 관문, 마이크로VM 샌드박스가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **에이전트 안전 도구 실행 5단계 시퀀스**:
  1. 에이전트의 도구 호출 제안 생성
  2. PEP의 스키마 및 거래 결속(Transaction Binding) 검증
  3. 비가역 고위험 액션 판정 시 Human-in-the-loop 승인 요청
  4. 1회성 단명 토큰 발급 및 마이크로VM 샌드박스 실행
  5. 실행 결과 반환 및 불변 감사 원장(Audit Trail) 로깅

</details>

```text
1. [도구 호출 제안 생성] 에이전트가 고객 지원 중 "환불 API 호출 `refund(amount=5000000)`" 제안 생성
            │
            ▼
2. [PEP 인터셉트 및 거래 결속 검증]
    ├─ PEP가 도구 등록부 스키마 확인 ➔ 정상 포맷 확인
    └─ 거래 결속 대조: 사용자가 요청한 환불 금액(50,000원)과 에이전트 제안(5,000,000원) 불일치 감지
            │
            ▼ (인젝션 공격 또는 파라미터 오염 시 즉각 거부)
    ├─ [파라미터 변조 감지 시 ➔ 도구 호출 즉시 중단(Abort) & 보안 관제 경보]
            │
            ▼ (정상 파라미터 일치 시 고위험 비가역 액션 판정)
3. [Human-in-the-loop 인간 승인 요청]
    ├─ 시스템이 재무 담당자에게 "50,000원 환불 승인 요청" 팝업 및 OTP 입력 요청
    └─ [담당자가 최종 승인 버튼 클릭 ➔ 1회성 임시 OAuth 토큰(TTL 60초) 발급]
            │
            ▼
4. [샌드박스 격리 실행]
    ├─ gVisor 샌드박스 컨테이너 내부에서 백엔드 결제 게이트웨이 환불 API 1회 안전 실행
    └─ 외부 비인가 C2 도메인 연결 시도는 Egress 방화벽에서 즉시 드롭
            │
            ▼
5. [불변 감사 로깅 및 완료] 전체 트랜잭션의 입출력 및 승인자 정보를 SHA-256 감사 로그로 영구 보존
```

**동작 원리**

1. **대리권의 구조적 박탈**: 에이전트는 결정을 "제안"할 뿐 시스템에 직접 접근할 수 있는 영구 권한을 보유하지 않음
2. **파라미터 위변조 방어**: 거래 결속을 통해 LLM 환각이나 인젝션에 의한 파라미터 조작을 런타임 탐지
3. **인간 최후의 방어선**: 복구 불가능한 금융/인프라 변경 시 기계의 판단을 중단시키고 인간의 서명을 강제
4. **런타임 폭주 봉쇄**: 샌드박스 단에서 OS 시스템 콜(syscall)을 필터링하여 호스트 서버 장악 원천 방어
5. **사후 무결성 감사**: 어떤 에이전트가 어떤 프롬프트에 의해 해당 API를 호출했는지 완벽한 추적성(Traceability) 확보

#### 한줄 요약
- 도구 제안 생성, PEP 거래 결속 검증, Human-in-the-loop 승인, 샌드박스 격리 실행, 불변 감사 로깅 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **AI 시스템 3대 유형 비교**: 단순 챗봇(Chatbot), RAG 검색(RAG), 자율 행동 에이전트(Action Agent)의 비교.

</details>

| 비교 항목 | 단순 일반 챗봇 (Chatbot) | 사내 검색 RAG 서비스 (RAG) | 자율 행동 에이전트 (Action Agent) |
|:---|:---|:---|:---|
| **시스템 주 목적** | **대화 및 텍스트 생성 (Read-only)** | **사내 지식 검색 및 요약 (Read-only)**| **외부 API/DB/OS 자율 실행 (Action)**|
| **상태 변경 (State)** | **없음 (영구 변경 불가능)** | **없음 (단순 문서 조회 한정)** | **있음 (불가역적 State Modification)**|
| **주요 핵심 위협** | 프롬프트 인젝션, 단순 PII 노출 | RAG 지식베이스 오염, 벡터 ACL 누락 | **과도한 권한(LLM06), 비인가 DB 파괴** |
| **핵심 방어 대책** | **XML 태깅 격리, Input/Output WAF** | **벡터 청크별 ACL, 메타데이터 검증** | **독립 PEP, 거래 결속, Human 승인** |

#### 한줄 요약
- 챗봇은 텍스트 생성, RAG는 사내 지식 조회, 에이전트는 실제 시스템 상태를 변경하므로 엄격한 PEP와 승인이 필수이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **OWASP LLM06:2025 (Excessive Agency) & NIST AI 600-1**: 자율 에이전트에 대한 과도한 권한 부여 방지, 인간 감독(Human Oversight), 실행 샌드박싱 국제 표준.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| AI 에이전트에게 마스터 API 키를 부여하여 **간접 프롬프트 인젝션에 속은 에이전트가 고객 데이터베이스 테이블 전체를 삭제하는 참사** | **OWASP LLM06:2025** 준수, **에이전트 권한을 읽기 전용으로 제한하고 쓰기 액션 시 독립 PEP 및 최소 스코프 단명 토큰 강제** | 에이전트의 독단적 데이터 파괴 100% 원천 차단 및 시스템 무결성 완벽 보장 |
| 인젝션 공격자가 프롬프트를 조작하여 **에이전트가 관리자가 의도한 수신자가 아닌 공격자 계좌로 거액을 이체하도록 파라미터 변조** | **사용자가 최초 요청한 파라미터를 세션에 동결하는 거래 결속(Transaction Binding) 및 Human-in-the-loop 승인 강제** | 파라미터 변조 공격 100% 실시간 인라인 탐지 및 비인가 금융 이체 차단 |
| 에이전트가 실행하는 파이썬 코드 및 쉘 스크립트가 **호스트 운영체제의 루트 권한을 장악하고 사내 내부망으로 횡적 이동(Lateral Movement)** | **NIST AI 600-1** 준수, **gVisor/Firecracker 기반 마이크로VM 샌드박스 격리 및 아웃바운드 Egress 방화벽 통제** | 호스트 OS 침투 및 외부 공격자 C2 서버 통신 100% 물리적 원천 격리 |

#### 한줄 요약
- 단명 토큰으로 파괴를 막고, 거래 결속과 Human 승인으로 변조를 차단하며, 마이크로VM 샌드박스로 커널을 보호한다.

## Ⅶ. 결론

- AI가 자율적으로 판단하고 행동하는 에이전틱 AI(Agentic AI) 시대의 가장 중대한 방어선인 **에이전트 보안(Agent Security) 아키텍처**는 시스템의 생사여탈권을 지키는 핵심 인프라이며, 실무 구현 시 **OWASP LLM06:2025 및 NIST AI 600-1 표준 준수**, **독립 PEP 기반의 완전 매개(Complete Mediation) 집행**, **파라미터 변조를 원천 차단하는 거래 결속(Transaction Binding)**, **비가역 고위험 액션에 대한 Human-in-the-loop 승인 관문**, **마이크로VM(gVisor/Firecracker) 기반 격리 샌드박스**를 통합 구축하여 최고 수준의 안전성과 신뢰성을 갖춘 자율 에이전트 생태계를 완성

#### 한줄 요약
- 완전 매개 PEP와 거래 결속 및 Human-in-the-loop 승인과 마이크로VM 샌드박스를 통해 자율 에이전트 보안을 완성한다.
