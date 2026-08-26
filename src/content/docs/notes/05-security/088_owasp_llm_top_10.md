---
sidebar:
  order: 88
  label: "088. OWASP LLM Top 10 (OWASP LLM Top 10)"
  badge:
    text: "기출 · 85%"
    variant: note
title: "생성형 AI 10대 핵심 보안 위험 및 다층 방어 체계 : OWASP Top 10 for LLM:2025"
date: "2026-08-26T14:53:14+09:00"
tags:
  - "notes-security"
weight: 88
extra:
  question_no: "088"
  source_status: "기출"
  source_history: "137회, 138회"
  priority: 85
  priority_note: "137•138회 반복 기출, OWASP Top 10 for LLM Applications 2025 전면 개정판, 5대 보안 도메인(입출력, 정보지시, 공급학습, 검색행동, 판단자원), LLM01(Prompt Injection)부터 LLM10(Unbounded Consumption) 전수 매핑"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **OWASP Top 10 for LLM Applications 2025 (생성형 AI 보안 표준 규격 / OWASP)**: 글로벌 오픈소스 웹 보안 기구인 OWASP가 생성형 AI, 거대 언어 모델(LLM), 검색 증강 생성(RAG), 자율 에이전트(Agentic AI) 시스템 구축 및 배포 시 조직이 반드시 통제해야 할 최우선 10대 핵심 보안 위험과 대응 아키텍처를 정의한 산업계 표준 프레임워크.
- **자연어 인터페이스 및 비결정론적 추론 위험(Non-deterministic Natural Language Risk)**: 기존 웹 보안(SQLi, XSS)과 달리, 비정형 자연어 프롬프트가 실행 코드로 변환되고 확률론적(Stochastic)으로 출력이 생성되는 AI 아키텍처 고유의 불확실성에서 비롯되는 신종 보안 위협군.

</details>

- 정의/개념: 생성형 AI의 10대 위험을 분류한 **OWASP LLM Top 10**
- 배경/필요성: 웹 보안 기준만으로는 **RAG·에이전트 위험 통제 불가**

#### 한줄 요약
- 생성형 AI와 RAG 및 에이전트 생태계의 10대 핵심 위험을 정의하고 5대 도메인 다층 방어 체계를 수립한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **OWASP LLM 2023 vs 2025 주요 개편 사항**:
  - **LLM07 신설 (System Prompt Leakage)**: 기업의 핵심 IP이자 페르소나 지침인 시스템 프롬프트의 탈취 위험을 독립 항목으로 승격.
  - **LLM08 신설 (Vector and Embedding Weaknesses)**: RAG 벡터 DB 접근 제어(ACL) 부재 및 임베딩 역공학 위협 신설.
  - **LLM09 개편 (Misinformation)**: 환각(Hallucination)에 의한 허위 정보 생성 위험을 법적·윤리적 관점에서 구체화.
  - **LLM10 개편 (Unbounded Consumption)**: 단순 DoS를 넘어 에이전트 무한 루프 및 클라우드 과금 고갈(Sponge Attack)로 확장.

</details>

- **AI 전 생애주기 전방위 포괄**: 프롬프트 입출력뿐만 아니라 HuggingFace 모델 공급망, 벡터 DB, 에이전트 API 실행 및 GPU 자원 소비까지 전주기 커버
- **아키텍처 맞춤형 위협 모델링 (Threat Modeling)**: 단순 챗봇, 사내 RAG 검색, 자율 행동 에이전트 등 자사 서비스 형태에 따라 공격 표면(Attack Surface)을 식별하고 통제 우선순위 차등화
- **정적 점검 탈피 및 런타임 심층 방어 (Defense in Depth)**: 단순 문서 체크리스트를 지양하고, NeMo Guardrails, 독립 PEP, AI 레드팀 회귀 시험 등 런타임 실효적 통제 강제

#### 한줄 요약
- 전주기 생태계 포괄, 2025년 개정 최신 위협 반영(System Prompt Leak, Vector 취약점), 맞춤형 위협 모델링을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **OWASP LLM Top 10:2025 전수 목록 (10대 핵심 위험)**:
  1. **LLM01 (Prompt Injection)**: 직접/간접 프롬프트 주입을 통한 시스템 지침 무력화.
  2. **LLM02 (Sensitive Information Disclosure)**: PII 개인정보 및 기업 기밀의 모델 응답 노출.
  3. **LLM03 (Supply Chain Risks)**: 서드파티 파운데이션 모델, 데이터셋, 플러그인 백도어 감염.
  4. **LLM04 (Data and Model Poisoning)**: 학습 데이터 및 RAG 지식베이스 오염을 통한 가중치 왜곡.
  5. **LLM05 (Improper Output Handling)**: 모델 출력을 미검증 상태로 백엔드 OS Shell/브라우저에 전달하여 RCE/XSS 유발.
  6. **LLM06 (Excessive Agency)**: 자율 에이전트에 과도한 권한(DB 삭제, 이체)을 부여하여 파괴적 행동 유발.
  7. **LLM07 (System Prompt Leakage)**: 롤플레이 역공학을 통해 백엔드 시스템 프롬프트 전문 유출.
  8. **LLM08 (Vector and Embedding Weaknesses)**: RAG 벡터 DB의 ACL 미비로 인한 타 부서 문서 무단 노출.
  9. **LLM09 (Misinformation)**: 환각(Hallucination)에 의한 허위 정보 생성으로 인한 법적 피해.
  10. **LLM10 (Unbounded Consumption)**: 초장문 입력 및 에이전트 무한 도구 루프로 인한 GPU/과금 고갈.

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ OWASP Top 10 for LLM:2025 - 5대 핵심 보안 경계 아키텍처 ]            │
├─────────────────────────────────────────────────────────────────────────┤
│ 1. [입력/출력 신뢰 경계]   ➔ LLM01(Prompt Injection), LLM05(Improper Output)    │
│    └─ XML 태깅 분리, Input/Output Guardrails, 터미널 샌드박싱           │
├─────────────────────────────────────────────────────────────────────────┤
│ 2. [정보/지시 권한 경계]   ➔ LLM02(Sensitive Info), LLM07(System Prompt Leak)  │
│    └─ PII 자동 마스킹 필터, 시스템 프롬프트 은닉 가드레일               │
├─────────────────────────────────────────────────────────────────────────┤
│ 3. [공급/학습 무결 경계]   ➔ LLM03(Supply Chain), LLM04(Poisoning)              │
│    └─ 모델 가중치 서명 검증, DVC 데이터 계보 관리, 수집 격리소          │
├─────────────────────────────────────────────────────────────────────────┤
│ 4. [검색/행동 인가 경계]   ➔ LLM06(Excessive Agency), LLM08(Vector & Embed)     │
│    └─ 최소 권한 IAM, Human-in-the-loop 승인, RAG 벡터 전용 ACL 격리     │
├─────────────────────────────────────────────────────────────────────────┤
│ 5. [판단/자원 가용 경계]   ➔ LLM09(Misinformation), LLM10(Unbounded Consump)   │
│    └─ 팩트체크 출처 인용 교차 검증, TPM 가중 쿼터 및 회로 차단기        │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: LLM01부터 LLM10까지의 10대 위험 요소가 입출력, 정보지시, 공급학습, 검색행동, 판단자원의 5대 보안 경계선에 1:1로 매핑되어 통제되는 구조

| 5대 핵심 통제 도메인 | 매핑된 OWASP 2025 위험 항목 | 핵심 보안 대책 및 아키텍처 통제 |
|:---|:---|:---|
| **입력 및 출력 경계** | **LLM01, LLM05** | XML 태그 지침-데이터 분리, NeMo Guardrails, 출력 이스케이프 샌드박스 |
| **정보 및 지시 경계** | **LLM02, LLM07** | 출력단 PII 마스킹 필터, 시스템 프롬프트 유출 방어 룰셋, DLP 연동 |
| **공급 및 학습 경계** | **LLM03, LLM04** | Safetensors 전자서명 검증, DVC 데이터 계보 추적, 수집 격리 버퍼 |
| **검색 및 행동 경계** | **LLM06, LLM08** | 에이전트 최소 권한 IAM, Human-in-the-loop 승인, RAG 벡터 청크별 ACL |
| **판단 및 자원 경계** | **LLM09, LLM10** | RAG 문서 인용(Grounding) 팩트체킹, TPM 가중 쿼터, 런타임 회로 차단기 |

#### 한줄 요약
- 10대 위험 요소가 5대 통제 도메인으로 분류되어 입출력, 지시, 공급망, 에이전트, 자원을 전방위 보호한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **OWASP LLM 보안 아키텍처 설계 5단계 프로세스**:
  1. 서비스 자산 식별 및 신뢰 경계(Trust Boundary) 설정
  2. OWASP LLM01~LLM10 공격 경로 1:1 교차 매핑
  3. 예방(Prevent), 탐지(Detect), 복구(Correct) 3중 통제망 설계
  4. AI 레드팀(Red Teaming) 실전 모의 침투 및 잔여 위험 평가
  5. CI/CD 파이프라인 자동화 회귀 시험 및 가드레일 지속 갱신

</details>

```text
1. [자산 식별 및 경계 설정] LLM 모델, RAG 벡터 DB, 에이전트 도구, 사용자 입력 간 신뢰 경계 도면화
            │
            ▼
2. [OWASP Top 10 위협 매핑]
    ├─ RAG 구간 ➔ LLM08(Vector ACL 취약점) 및 LLM04(지식베이스 오염) 매핑
    └─ 에이전트 구간 ➔ LLM06(과도한 권한) 및 LLM10(무한 루프 DoS) 매핑
            │
            ▼
3. [3중 다층 방어 통제망 구축]
    ├─ 예방(Prevent): Input Guardrails, XML 태깅, 최소 권한 IAM 적용
    ├─ 탐지(Detect): 런타임 PII 스캐너, 에이전트 실행 모니터링, 벡터 쿼리 이상 탐지
    └─ 복구(Correct): 런타임 회로 차단기(Circuit Breaker), DVC 스냅샷 롤백
            │
            ▼
4. [AI 레드팀 적대적 모의 침투]
    ├─ 화이트해커가 탈옥(Jailbreak), 시스템 프롬프트 유출(LLM07), C2 유출 시도
    └─ [잔여 위험(Residual Risk) 측정 ➔ 가드레일 차단율 99.9% 확인]
            │
            ▼
5. [지속적 회귀 평가 파이프라인] 배포 후 매일 자동화 Fuzzer를 실행하여 방어막 무결성 상시 유지
```

**동작 원리**

1. **자산 식별 및 경계 설정**
2. **OWASP Top 10 위협 매핑**
3. **3중 다층 방어 통제망 구축**
4. **AI 레드팀 적대적 모의 침투**
5. **지속적 회귀 평가 파이프라인**

#### 한줄 요약
- 자산 식별, Top 10 매핑, 3중 통제 설계, AI 레드팀 모의 침투, 지속적 회귀 평가 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **기존 Web OWASP Top 10 vs OWASP LLM Top 10:2025 비교**:
  - Web OWASP: 정형화된 HTTP 요청 및 데이터베이스 쿼리 공격 중심.
  - LLM OWASP: 비정형 자연어 프롬프트, 딥러닝 가중치, RAG 벡터, 에이전트 자율 행동 중심.

</details>

| 비교 항목 | 전통적 Web OWASP Top 10 | OWASP Top 10 for LLM:2025 |
|:---|:---|:---|
| **주요 공격 매개체** | **정형화된 HTTP 파라미터, SQL 쿼리, 세션 쿠키**| **비정형 자연어 프롬프트, RAG 벡터, 에이전트 Tool Call**|
| **핵심 위협 메커니즘**| SQL Injection, XSS, Broken Access Control | **Prompt Injection(01), System Prompt Leak(07), Vector(08)**|
| **방어 아키텍처** | **정규식 WAF, 파라미터 바인딩, 정적 RBAC** | **NeMo Guardrails, Dual-LLM, RAG ACL, 에이전트 PEP** |
| **침해 결과 양상** | 데이터베이스 탈취, 웹 쉘 업로드, 계정 탈취 | **비인가 자율 조작(이체/삭제), 모델 백도어, 클라우드 DoS**|

#### 한줄 요약
- 전통적 웹은 정형화된 파라미터 방어, LLM Top 10은 비정형 자연어 통제와 자율 에이전트 권한 제어이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **체크리스트형 행정 보안의 한계**: OWASP 문서를 서류 점검용으로만 취급하고, 실제 런타임 트래픽을 인라인 차단하는 가드레일 및 PEP 인프라를 구축하지 않아 실전 공격에 무방비 노출되는 결함.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| OWASP 문서를 단순 체크리스트로만 취급하여 **실제 런타임 환경에서 프롬프트 인젝션 및 시스템 프롬프트 유출이 발생하는 탁상행정 결함** | **OWASP Top 10 for LLM:2025** 기준, **NeMo/Llama Guard 기반 런타임 입출력 Guardrails 및 XML 구조적 격리 강제** | 자연어 인젝션 및 시스템 프롬프트 탈취(LLM07) 100% 실시간 인라인 차단 |
| RAG 벡터 데이터베이스에 부서별 권한 분리가 적용되지 않아 **일반 직원이 사내 챗봇을 통해 임원진 인사 고과 및 재무 기밀을 조회하는 사고** | **LLM08(Vector & Embedding)** 통제 준수, **벡터 청크 메타데이터에 사용자 IAM 접근제어(ACL) 결속 및 권한 기반 검색 강제** | 비인가 RAG 문서 검색 및 민감 정보 노출(LLM02) 100% 원천 차단 |
| AI 자율 에이전트에게 쓰기/삭제 권한을 무분별하게 부여하여 **인젝션 공격에 넘어간 에이전트가 백엔드 데이터베이스를 삭제하는 대형 참사** | **LLM06(Excessive Agency)** 통제 준수, **최소 권한 IAM 적용 및 파괴적/금융 고위험 도구 호출 시 Human-in-the-loop 승인 강제** | 에이전트의 독단적 파괴 명령 실행 원천 차단 및 인프라 무결성 완벽 보장 |

#### 한줄 요약
- 런타임 Guardrails로 인젝션을 막고, RAG ACL로 기밀 조회를 차단하며, Human-in-the-loop로 에이전트 참사를 방지한다.

## Ⅶ. 결론

- 챗봇은 **입출력 가드레일**, 에이전트는 **독립 PEP** 우선 적용

#### 한줄 요약
- 2025년 최신 10대 위험을 5대 도메인 다층 방어선과 AI 레드팀 평가로 통제하여 안전한 생성형 AI를 완성한다.
