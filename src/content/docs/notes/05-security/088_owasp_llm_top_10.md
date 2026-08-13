---
sidebar:
  order: 88
  label: "088. OWASP LLM Top 10 (OWASP LLM Top 10)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "OWASP LLM Top 10 (OWASP LLM Top 10)"
date: "2026-08-13T20:58:00+09:00"
tags:
  - "notes-security"
weight: 88
extra:
  question_no: "088"
  source_status: "기출"
  source_history: "137회, 138회"
  priority: 85
  priority_note: "137•138회 반복된 LLM 위험 분류 우산 주제임"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **OWASP(Open Worldwide Application Security Project)**: 오픈소스 웹 및 애플리케이션 보안 가이드라인 표준화 비영리 단체이다.
- **LLM(Large Language Model)**: 대규모 트랜스포머 언어 모델로 문맥을 이해하고 자연어 및 코드를 생성하는 파운데이션 생성형 AI이다.
- **RAG(Retrieval-Augmented Generation)**: 외부 지식베이스(벡터 DB) 조회를 통해 LLM의 환각을 줄이고 정밀 답변을 도출하는 아키텍처이다.
- **OWASP LLM Top 10 2025 (OWASP Top 10 for Large Language Model Applications 2025)**: 생성형 AI, LLM, RAG, 에이전트 시스템 도입 시 발생하는 최우선 핵심 보안 위협 10가지를 수록한 보안 가이드라인 표준 규격이다.
- **LLM 응용 위험(LLM Application Risk / Vulnerabilities)**: 전통적 OWASP Top 10(웹 취약점)과 달리 자연어 인젝션, 환각, 모델 데이터 유출, 과도한 권한 부여 등 생성형 AI의 특수성에서 비롯되는 보안 위험이다.

</details>

- 정의/개념: LLM 응용의 10대 위험과 통제를 제시한
  **OWASP LLM Top 10 2025**
- 배경/필요성: 웹 취약점 분류만으로 다루기 어려운
  **프롬프트·RAG·에이전트 위험**

#### 한줄 요약

- 생성형 AI, RAG 및 LLM 에이전트 애플리케이션의 10대 핵심 보안 위험과 대응책을 정의한 글로벌 대표 보안 표준 규격이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **판본 식별성(Version Determinism & Traceability)**: 기술 진화에 따라 2023년 버전과 2025년 최신 버전 간의 항목 변경(예: LLM07 System Prompt Leakage 신설, LLM10 Unbounded Consumption 추가)을 추적 관리하는 성질이다.
- **서비스별 위협 모델(Service-tailored Threat Model)**: 10대 취약점 표준 목록을 그대로 적용하지 않고, 자사 서비스 아키텍처(챗봇 vs 에이전트 vs RAG)의 위험도에 맞추어 맞춤 재편하는 위협 평가 모델이다.

</details>

- 입출력(Prompt/Output), 모델 공급망(Supply Chain), 데이터/RAG, 에이전트 권한(Agency), 자원 고갈 등 생성형 AI 수명주기 전체를 커버한다.
- 2025년 개정을 통해 System Prompt Leakage(LLM07), Vector & Embedding Weaknesses(LLM08) 등 최신 엣지 취약점을 즉시 반영하여 **판본 식별성**을 유지한다.
- 시스템 아키텍처에 맞춰 **서비스별 위협 모델**을 정립하고 다층 보안 통제(Defense in Depth)를 수립한다.

#### 한줄 요약

- AI 생명주기 전반 커버, 2025 최신 개정판 반영(System Prompt Leak, Vector 취약점 추가) 및 맞춤형 위협 모델링 기준을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **LLM01(LLM01: Prompt Injection)**: 직접/간접 프롬프트를 주입하여 시스템 프롬프트를 무력화하고 인가되지 않은 조작을 유도하는 최우선 위험이다.
- **LLM02(LLM02: Sensitive Information Disclosure)**: LLM 추론 답변이나 PII 필터링 미비로 인해 민감 개인정보 및 기업 기밀이 노출되는 위험이다.
- **LLM03(LLM03: Supply Chain Risks)**: 허깅페이스 등 제3자 파운데이션 모델, 미검증 데이터셋, 파이썬 라이브러리 공급망 내 악성 백도어가 포함되는 위험이다.
- **LLM04(LLM04: Data and Model Poisoning)**: 학습 데이터 및 RAG 지식베이스에 오염 샘플이나 트리거를 주입하여 모델 결정 경계를 조작하는 위험이다.
- **LLM05(LLM05: Improper Output Handling)**: LLM 출력을 이스케이프 검증 없이 브라우저나 OS Shell로 곧바로 전달하여 XSS, RCE를 야기하는 위험이다.
- **LLM06(LLM06: Excessive Agency)**: 에이전트에 과도한 과업 실행 권한(DB 삭제, 이체 API 호출)을 부여하여 시스템 조작 피해를 확대시키는 위험이다.
- **LLM07(LLM07: System Prompt Leakage)**: 악의적 질의를 통해 기업의 자산이자 비밀 영업 기밀인 시스템 프롬프트(페르소나 지침)를 탈취하는 위험이다.
- **LLM08(LLM08: Vector and Embedding Weaknesses)**: RAG 파이프라인 내 벡터 DB의 Access Control 미비, 임베딩 충돌 공격으로 민감 문맥이 반출되는 위험이다.
- **LLM09(LLM09: Misinformation)**: LLM 환각(Hallucination) 응답을 별도 검증 없이 노출하여 법적, 사업적 손실을 일으키는 위험이다.
- **LLM10(LLM10: Unbounded Consumption)**: 100k 토큰 이상의 대용량 입력 및 무한 툴 루프를 유발해 GPU 연산 자원 및 예산을 마비시키는 서비스 거부 위험이다.

</details>

```text
OWASP LLM Top 10 2025
├─ 입력·출력 경계
├─ 정보·지시 경계
├─ 공급·학습 경계
├─ 검색·행동 경계
└─ 판단·자원 경계
```

선의 의미: 5대 핵심 도메인 경계별로 분류된 OWASP LLM Top 10 2025 보안 위협 매핑 아키텍처이다.

| 5대 핵심 도메인 | 해당 OWASP 2025 위험 항목 | 주요 통제 방안 |
|:---|:---|:---|
| 입력·출력 경계 | **LLM01** (Prompt Injection), **LLM05** (Improper Output Handling) | XML 프롬프트 태그 분리, LLM Output WAF 및 이스케이프 산화 |
| 정보·지시 경계 | **LLM02** (Sensitive Info Disclosure), **LLM07** (System Prompt Leakage) | 런타임 PII Masking 가드레일, 시스템 프롬프트 유출 금지 필터 |
| 공급·학습 경계 | **LLM03** (Supply Chain Risks), **LLM04** (Data and Model Poisoning) | 파운데이션 모델 서명 검증, DVC 데이터 버전 및 수집 격리소 |
| 검색·행동 경계 | **LLM06** (Excessive Agency), **LLM08** (Vector & Embedding) | 최소 권한 IAM, Human-in-the-Loop 승인, RAG 벡터 ACL 조율 |
| 판단·자원 경계 | **LLM09** (Misinformation), **LLM10** (Unbounded Consumption) | Fact-checking 인용 검증, TPM 가중 쿼터 및 Circuit Breaker |

#### 한줄 요약

- LLM01부터 LLM10까지 5대 보안 도메인(입출력, 정보지시, 공급학습, 검색행동, 판단자원)으로 분류 관리한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **공격 경로 매핑(Attack Vector / Path Mapping)**: 10대 위험 항목이 서비스 내 프롬프트 유입, RAG 벡터 탐색, Tool Execution 중 어디서 발생하는지 도면화하는 작업이다.
- **잔여 위험(Residual Risk)**: 방어 가드레일 및 통제를 도입한 후에도 남아 있는 수용 가능한 보안 위험 수준이다.
- **자산•신뢰 경계 확정(Asset & Trust Boundary Identification)**: LLM, DB, 사용자 입력, 외부 API 간의 신뢰 경계를 명확히 긋는 단계이다.
- **LLM01~LLM10 시나리오 매핑(LLM Top 10 Scenario Mapping)**: 자원별로 10개 위협 발생 가능성을 대조 매핑하는 단계이다.
- **예방•탐지•복구 통제 설계(Preventive, Detective & Corrective Control Design)**: 3중 방어 관문(가드레일, 샌드박스, 롤백)을 설계하는 단계이다.
- **실제 공격•잔여 위험 평가(Empirical Attack & Residual Risk Assessment)**: AI 레드팀 평가를 가해 남은 취약점을 검증하는 단계이다.
- **우선순위•통제 갱신(Priority & Control Re-alignment)**: 신종 바이패스 기법 등장 시 통제 룰을 상시 갱신하는 단계이다.

</details>

```text
서비스 자산·경계
        |
        v
1. 자산·신뢰 경계 확정
        |
        v
2. LLM01~LLM10 시나리오 매핑
        |
        v
3. 예방·탐지·복구 통제 설계
        |
        v
4. 실제 공격·잔여 위험 평가
        |
        v
5. 우선순위·통제 갱신
        |
        v
   위험 처리 계획
```

### 동작 원리

1. **자산·신뢰 경계 확정**: 데이터·도구의 보안 경계 식별
2. **LLM01~LLM10 시나리오 매핑**: 자산별 위협 경로 연결
3. **예방·탐지·복구 통제 설계**: 다층 방어 통제 배치
4. **실제 공격·잔여 위험 평가**: 레드팀 기반 잔여 위험 측정
5. **우선순위·통제 갱신**: 신종 우회에 맞춰 통제 보정

#### 한줄 요약

- 자산 경계 확정, Top 10 시나리오 매핑, 다층 통제 설계, 레드팀 기반 잔여 위험 평가 및 통제 상시 갱신 절차로 이행된다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **LLM 응용 경계(LLM Application Boundary)**: 프롬프트 입력, 모델 추론, RAG 벡터 검색이 이루어지는 영역이다.
- **웹 응용 경계(Web Application Boundary)**: HTTP/HTTPS 프론트엔드 및 백엔드 REST API의 통신 영역이다.
- **에이전트 권한 경계(Agent Privilege / Action Boundary)**: AI 에이전트가 시스템 명령(OS Command, DB Query)을 집행하는 자율 실행 영역이다.
- **HTTP(Hypertext Transfer Protocol)**: 웹 클라이언트와 서버 간의 데이터를 주고받는 표준 통신 프로토콜이다.

</details>

| 보안 분석 영역 | 기존 Web OWASP Top 10 | OWASP LLM Top 10 2025 |
|:---|:---|:---|
| 주 타격 대상 | **HTTP** 요청 파라미터, SQL 쿼리, 세션 토큰 | 자연어 프롬프트 지침, RAG 벡터 문맥, 에이전트 Tool Call 인자 |
| 핵심 위협 매커니즘 | SQL Injection, XSS, Broken Auth | Prompt Injection (LLM01), System Prompt Leak (LLM07), Vector Risk (LLM08) |
| 주 방어 메커니즘 | Input Sanitization, WAF, Role-based ACL | XML Tagging, LLM Input/Output Guardrails, **에이전트 권한 경계** 통제 |
| 공격 결과 | DB 정보 유출, 세션 탈취, RCE | 비인가 시스템 조작, 백도어 실행, 과금 폭탄 DoS (LLM10) |

#### 한줄 요약

- 기존 Web OWASP는 HTTP 텍스트 파라미터 타격 중심이며, LLM OWASP 2025는 자연어 지시/RAG 문맥 및 에이전트 자율권 방어에 집중한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **목록식 점검 한계(Checklist-driven Inspection Pitfalls)**: 단순 체크리스트만 확인하고 실제 인젝션/탈옥 런타임 가드레일을 구축하지 않는 수동적 위험성이다.
- **레드팀(Adversarial Red Teaming)**: AI 시스템을 대상으로 인젝션, 탈옥, PII 유출 공격을 가해 취약점을 발굴하는 평가 활동이다.
- **회귀 시험(Regression Testing)**: 보안 보정 후 과거 공격 시나리오의 차단 성공 여부를 지속 자동화 검증하는 시험이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단순 체크리스트형 점검의 한계 | **목록식 점검 한계** 탈피 및 **공격 경로 매핑** | 서비스 아키텍처에 맞춘 실질적 AI 보안 통제 구현 |
| 2025 개정 항목(Vector, System Prompt) 대응 미비 | **OWASP LLM Top 10 2025** 최신 표준 준용 | RAG 벡터 DB ACL 강화 및 시스템 프롬프트 유출 방지 |
| 통제 실효성 부족 및 사후 유출 사고 | AI **레드팀** 및 자동화 **회귀 시험** 지속 집행 | 신종 바이패스 기법의 실시간 모니터링 및 즉시 보정 |

#### 한줄 요약

- OWASP LLM 2025 표준 준수, 단순 체크리스트를 넘어선 AI 레드팀 평가 및 회귀 시험 자동화를 수립한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **위험 분류의 활용 원칙(Risk Taxonomy Utilization Principles)**: OWASP Top 10을 고정 규제로 보지 않고 조직의 AI 보안 거버넌스 및 가드레일 설계의 출발점으로 활용하는 원칙이다.

</details>

- 서비스별 **위협 모델**에 맞춰 통제하고 **레드팀**으로 검증

#### 한줄 요약

- OWASP LLM Top 10 2025 표준 준수, 5대 도메인 다층 통제, AI 레드팀 회귀 시험 및 가드레일 체계 구축 필수.
