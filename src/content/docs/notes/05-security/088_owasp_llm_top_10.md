---
sidebar:
  order: 88
  label: "088. OWASP LLM Top 10 (OWASP LLM Top 10)"
  badge:
    text: "기출 · 85%"
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

<details><summary>용어 설명</summary>

- **OWASP LLM Top 10 2025 (OWASP Top 10 for Large Language Model Applications 2025)**: 글로벌 애플리케이션 보안 기구인 OWASP가 생성형 AI, LLM, RAG, 에이전트 시스템 도입 시 기업이 직면하게 되는 최우선 핵심 보안 위협 10가지를 정리 선포한 산업계 최고 권위의 보안 가이드라인 표준 규격이다.
- **LLM 응용 위험 (LLM Application Risk / Vulnerabilities)**: SQL 인젝션이나 XSS 등 전통적 OWASP Top 10 웹 취약점과 본질적으로 궤를 달리하는, 자연어 프롬프트 우회 인젝션, 환각 생성, 훈련 데이터 역전 유출, 에이전트 과도 권한 집행 등 생성형 AI만의 특수성에서 비롯되는 신종 보안 위험군이다.

</details>

- 정의: 생성형 AI 생태계에 특화된 10대 최우선 핵심 위험 요소와 이에 대한 방어 통제 원칙을 명확히 제시한 글로벌 AI 보안 표준 규격이다.
- 배경: 단순 웹 취약점 분류만으로는 딥러닝 내부 가중치 조작, **프롬프트 우회**, **RAG 벡터 오염**, **자율 에이전트 오작동 위험** 등 급변하는 AI 고유의 블랙박스 침투 위협을 도저히 포괄 대응할 수 없었기 때문이다.

#### 한줄 요약

- 생성형 AI 파운데이션 모델, RAG 및 LLM 에이전트 애플리케이션의 10대 핵심 보안 위험과 다층 방어 통제책을 정의한 글로벌 대표 보안 표준 규격이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **판본 식별성 (Version Determinism & Traceability)**: 딥러닝 기술 진화에 즉각 발맞추어 2023년 구버전과 2025년 최신 개정 버전 간의 신규 위협 변경 항목(예: LLM07 System Prompt Leakage 신설, LLM10 Unbounded Consumption 추가)을 치밀하게 추적 관리하고 갱신하는 유지보수 성질이다.
- **서비스별 위협 모델 (Service-tailored Threat Model)**: 10대 취약점 표준 목록 전체를 기계적으로 일괄 적용하지 않고, 자사 서비스 아키텍처(단순 챗봇 vs 복합 RAG vs 도구형 에이전트)의 공격 노출도(Attack Surface)에 맞추어 우선순위를 맞춤 재편하는 동적 위협 평가 모델이다.

</details>

- **전주기 생태계 포괄 커버**: 단순 입출력 텍스트(Prompt/Output) 방어를 넘어, 허깅페이스 모델 공급망(Supply Chain), 벡터 RAG 데이터베이스 연동, 에이전트 자율 권한(Agency), 클라우드 자원 고갈 등 생성형 AI 수명주기 생태계 전체 근거를 커버한다.
- **최신 위협 진화 즉시 반영 체계**: 2025년 전면 개정을 통해 페르소나 지침 탈취인 System Prompt Leakage(LLM07), 검색 오염인 Vector & Embedding Weaknesses(LLM08) 등 최신 엣지 취약점을 반영하여 **판본 식별성** 정교히 유지한다.
- **아키텍처 맞춤형 통제**: 획일화된 솔루션 도입을 배제하고, 자사 시스템 아키텍처 특성에 맞춰 **서비스별 위협 모델** 정립한 뒤 심층 다층 보안 통제(Defense in Depth)를 수립하도록 가이드한다.

#### 한줄 요약

- AI 생명주기 생태계 전반 커버, 2025 개정판 최신 위협 반영(System Prompt Leak, Vector 취약점 추가 신설) 및 맞춤형 동적 위협 모델링 기준을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **LLM01 (Prompt Injection)**: 공격자가 직접/간접 교묘한 프롬프트를 주입하여 개발자가 정의한 시스템 안전 지침 가중치를 무력화하고 비인가 조작을 유도하는 최상위 1위 위험이다.
- **LLM02 (Sensitive Information Disclosure)**: LLM 추론 답변 내 PII 필터링 샌드박스 미비로 인해 민감 개인정보 및 타사 영업 기밀이 외부에 무단 노출 반출되는 프라이버시 위험이다.
- **LLM03 (Supply Chain Risks)**: 허깅페이스 등 제3자 파운데이션 모델 다운로드, 미검증 무단 데이터셋, 서드파티 파이썬 플러그인 공급망 파이프라인 내부에 치명적 악성 백도어가 은닉 포함되는 감염 위험이다.
- **LLM04 (Data and Model Poisoning)**: 모델 재학습 데이터 및 RAG 지식베이스 DB에 악성 오염 샘플이나 잠복 트리거를 몰래 주입하여 모델 분류 결정 경계 자체를 물리적으로 조작 파괴하는 위험이다.
- **LLM05 (Improper Output Handling)**: 오염된 LLM의 출력을 적절한 이스케이프 검증 절차 없이 일반 브라우저 DOM이나 백엔드 OS Shell 터미널로 곧바로 전달 인가하여 XSS, RCE 대형 사고를 야기하는 연쇄 위험이다.
- **LLM06 (Excessive Agency)**: 자율 에이전트에게 팝업 승인 없이 과도한 과업 실행 권한(핵심 DB 삭제, 거액 이체 API 자율 호출)을 무분별하게 부여하여 시스템 조작 파손 피해를 천문학적으로 확대시키는 인가 통제 위험이다.
- **LLM07 (System Prompt Leakage)**: 2025 신설 항목으로, 공격자의 집요한 악의적 롤플레이 질의를 통해 기업의 핵심 지적 자산이자 비밀 영업 기밀 알고리즘인 백엔드 시스템 프롬프트(페르소나 지침서) 전문을 원문 그대로 탈취 반출하는 위험이다.
- **LLM08 (Vector and Embedding Weaknesses)**: 2025 신설 항목으로, RAG 파이프라인 내 벡터 DB의 세밀한 사용자 접근통제(ACL) 미비 및 임베딩 쿼리 충돌 공격으로 타 부서의 민감 내부 문맥이 무단 교차 반출되는 권한 위험이다.
- **LLM09 (Misinformation)**: 구 LLM08 Insecure Design을 대체한 위험으로, 거짓을 그럴싸하게 꾸며내는 LLM 환각(Hallucination) 응답을 별도의 근거체크 교차 검증 로직 없이 일반 사용자에게 그대로 노출하여 심각한 법적 소송 및 브랜드 손실을 일으키는 위험이다.
- **LLM10 (Unbounded Consumption)**: 구 LLM09 Model DoS를 구체화한 항목으로, 100k 토큰 이상의 무의미한 대용량 문맥 입력 및 에이전트의 종료 조건 없는 무한 툴 루프 반복을 고의 유발해 초고가 GPU 연산 자원 및 클라우드 예산을 파탄 마비시키는 서비스 거부 위험이다.

</details>

```text
[OWASP LLM Top 10 2025 핵심 보안 경계 아키텍처 매핑]

├─ [입력/출력 신뢰 경계]   -->  Prompt Injection (01), Improper Output Handling (05)
├─ [정보/지시 권한 경계]   -->  Sensitive Info Disclosure (02), System Prompt Leakage (07)
├─ [공급/학습 무결 경계]   -->  Supply Chain Risks (03), Data/Model Poisoning (04)
├─ [검색/행동 인가 경계]   -->  Excessive Agency (06), Vector & Embedding Weaknesses (08)
└─ [판단/자원 가용 경계]   -->  Misinformation (09), Unbounded Consumption (10)
```

| 5대 핵심 통제 도메인 | 해당 OWASP 2025 위험 항목 | 최우선 방어 보안 통제 가이드라인 |
|:---|:---|:---|
| **입력 및 출력 경계** | **LLM01**(Prompt Injection), **LLM05**(Improper Output) | 시스템 지시어와 사용자 XML 프롬프트 태그 분리 통제, 강력한 LLM Output WAF 필터 및 터미널 이스케이프 산화 처리 |
| **정보 및 지시 경계** | **LLM02**(Sensitive Info), **LLM07**(System Prompt Leak) | 출력 런타임 구간 정밀 PII Masking 가드레일 가동, 시스템 프롬프트 소스코드 탈취 금지 내부 필터 룰 강제 집행 |
| **공급 및 학습 경계** | **LLM03**(Supply Chain), **LLM04**(Poisoning) | 외부 파운데이션 모델 해시 서명 무결성 검증 락, DVC 데이터 버전 추적 보존 및 스크래핑 수집 격리소 운영 |
| **검색 및 행동 경계** | **LLM06**(Excessive Agency), **LLM08**(Vector & Embed) | 최소 권한(Least Privilege) 에이전트 IAM 부여, Human-in-the-Loop 비가역 팝업 승인 체계, RAG 벡터 전용 ACL 권한 조율 |
| **판단 및 자원 경계** | **LLM09**(Misinformation), **LLM10**(Unbounded Consump) | 문서 출처 인용(Fact-checking) 2차 자동 검증 파이프라인, TPM 가중 쿼터 제한 및 런타임 루프 회로 차단기(Circuit Breaker) 발동 |

#### 한줄 요약

- LLM01 인젝션부터 LLM10 자원 폭주까지 5대 보안 도메인(입출력, 정보지시, 공급학습, 검색행동, 판단자원)으로 구조화 분류 관리하는 체계이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **공격 경로 매핑 (Attack Vector / Path Mapping)**: OWASP 10대 위험 항목 지표가 실제 자사 운영 서비스 내의 사용자 프롬프트 유입 구간, RAG 벡터 탐색 질의 구간, 에이전트 Tool Execution 샌드박스 구간 중 정확히 어디서 어떻게 촉발 발생하는지 시각적 도면화하는 선행 작업 특징이다.
- **잔여 위험 평가 (Empirical Residual Risk Assessment)**: 사내 보안팀이 방어 가드레일 및 PEP 통제 관문을 겹겹이 도입한 후에도 여전히 교묘하게 남아 시스템을 뚫어내는 수용 가능한 보안 위험 수준을 수치화하는 평가이다.

</details>

```text
[안전한 LLM 애플리케이션 보안 설계 프로세스 전개]
         |
         v
1. 자사 서비스 핵심 운영 자산 및 컴포넌트 간 신뢰 경계(Trust Boundary) 명확 확정
         |
         v
2. 도출된 자산 식별 구간에 OWASP LLM01~LLM10 공격 취약 시나리오 1:1 교차 매핑
         |
         v
3. 구간별 방어 예방(Prevent), 실시간 탐지(Detect), 긴급 복구(Correct) 3중 통제 관문 설계
         |
         v
4. 적대적 모의 AI 레드팀 공격 수행을 통한 실제 공격 방어력 측정 및 잔여 위험 평가
         |
         v
5. 신규 취약점 및 바이패스 기법 등장에 맞춘 위험 우선순위 조정 및 통제 룰 런타임 상시 갱신
         |
         v
[안정성과 프라이버시가 보장된 LLM 운영 서비스 배포 유지]
```

### 동작 원리

1. 자산 경계 확정: LLM 모델, 벡터 DB, 사용자 입력, 외부 툴 API 간의 데이터 흐름 보안 통제선을 식별한다.
2. OWASP 10 시나리오 매핑: 식별된 구간별로 어떤 LLM 10대 위협 경로가 치명타를 입힐 수 있는지 정밀 매핑 연결한다.
3. 3중 다층 통제 설계: 입력 가드레일(예방), 런타임 모니터링(탐지), 롤백 샌드박스(복구) 방어막을 겹겹이 배치한다.
4. 레드팀 잔여 위험 평가: 화이트해커 레드팀 기반의 가혹한 공격을 가해 뚫리지 않고 남은 방어율과 잔여 위험을 산출한다.
5. 통제망 상시 갱신: 신종 우회 탈옥 기법 등장 시 지체 없이 룰셋을 보정하고 가중치를 패치한다.

#### 한줄 요약

- 핵심 자산 경계 확정, Top 10 매핑 구조화, 다층 통제 설계망 구축, AI 레드팀 모의 침투 기반 잔여 위험 평가 및 통제룰 상시 갱신 절차로 이행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **LLM 응용 경계 (LLM Application Boundary)**: 비정형 자연어 프롬프트가 입력되고, 딥러닝 모델 추론이 일어나며, RAG 벡터 유사도 검색 매핑이 일어나는 통제 불확실성이 극히 높은 블랙박스 영역이다.
- **기존 웹 응용 경계 (Traditional Web Application Boundary)**: 100% 정형화된 HTTP/HTTPS 프론트엔드 및 백엔드 REST API의 통신 영역으로, 패턴 매칭 WAF로 쉽게 원천 차단이 가능한 화이트박스 영역이다.
- **에이전트 권한 경계 (Agent Privilege / Action Boundary)**: AI 에이전트가 텍스트 생성을 넘어 외부 시스템 명령(OS Command, DB Insert/Delete Query)을 자율적으로 집행하고 변경하는 최고 위험도의 액션 영역이다.

</details>

| 보안 패러다임 분석 영역 | **기존 Web OWASP Top 10 (Web/API 보안)** | **신규 OWASP LLM Top 10 2025 (생성형 AI 보안)** |
|:---|:---|:---|
| 시스템 주 타격 대상 | 정형화된 **HTTP** 요청 파라미터, SQL 쿼리문, 고정 세션 토큰 값 | 비정형 자연어 프롬프트 텍스트, RAG 벡터 문맥 뭉치, 에이전트 자율 Tool Call 인자 |
| 핵심 치명적 위협 매커니즘 | 고전적 SQL Injection, XSS, Broken Auth 세션 하이재킹 | 지능적 Prompt Injection (LLM01), System Prompt Leak (LLM07), 검색 오염 Vector Risk (LLM08) |
| 주 방어 체계 및 메커니즘 | 입력 Input Sanitization 정규식 룰, 정적 WAF 필터, Role-based 정적 ACL | 논리적 XML Tagging 샌드박싱, 동적 LLM Input/Output Guardrails, **에이전트 실행 권한 경계 PEP 통제** |
| 방어 실패 시 공격 결과 | 고객 DB 정보 대량 유출, 관리자 세션 탈취, 서버 RCE 장악 통제 | 의도되지 않은 비인가 툴 조작 파손, 가중치 잠복 백도어 실행, 과금 폭탄 DoS (LLM10) 마비 사태 |

#### 한줄 요약

- 기존 Web OWASP는 정형화된 HTTP 텍스트 파라미터 방어 중심이며, 최신 LLM OWASP 2025는 비정형 자연어 지시 통제, RAG 벡터 격리 및 자율 에이전트 행동 권한 통제에 집중하는 차이가 있다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **목록식 점검의 한계 (Checklist-driven Inspection Pitfalls)**: OWASP 문서를 단순 체크리스트 표로만 대충 형식적 확인하고, 막상 런타임 환경에서 실시간 방어하는 인젝션/탈옥 차단 가드레일 인프라는 전혀 구축하지 않는 수동적이고 무책임한 보안 행정 위험성이다.
- **AI 레드팀 평가 (Adversarial Red Teaming Assessment)**: 단순 자동화 취약점 스캐너에 의존하지 않고 인간 보안 전문가가 직접 조직의 AI 시스템을 타깃으로 교묘한 인젝션, 탈옥, PII 유출 공격을 가해 심층 블랙박스 취약점을 발굴해 내는 평가 활동이다.
- **자동화 회귀 시험 (Automated Regression Testing)**: 발견된 취약점에 방어 패치를 적용한 후, 과거에 뚫렸던 동일 공격 시나리오를 자동 스크립트로 지속 반복 투입하여 차단 방어막이 다시 열리지 않는지 영구적으로 자동 검증하는 파이프라인이다.

</details>

| 장애/위험 요소 | 원인 분석 | 실무 대책 및 해결방안 | 기대 효과 |
|:---|:---|:---|:---|
| **문서 위주의 단순 체크리스트형 보안 점검의 한계 노출** | 실효적 차단 가드레일 없는 서류상 탁상행정 보안 한계 | **목록식 점검 한계** 탈피 및 철저한 실제 아키텍처 **공격 경로 매핑** 집행 | 실 운영 서비스 아키텍처 맥락에 완벽히 부합하는 런타임 실효적 AI 보안 통제 구현 달성 |
| **2025년 개정 신규 엣지 항목 (Vector 쿼리, System Prompt 유출) 대응 전무** | 과거 2023 구버전 기준표에 머물러 있는 나태한 보안 체계 유지 | 신규 **OWASP LLM Top 10 2025** 최신 글로벌 표준 지침 즉각 전면 준용 | RAG 벡터 DB 접근제어(ACL) 정밀 분리 강화 및 핵심 영업 기밀 시스템 프롬프트 소스 유출 완전 방지 |
| **런타임 통제 방어망 실효성 부족 및 사후 프라이버시 2차 유출 사고 발생** | 배포 후 지속적인 적대적 해킹 시나리오 방어 검증 파이프라인 부재 | 고강도 AI **레드팀 모의침투** 강제 및 365일 CI/CD 자동화 **회귀 시험** 지속 집행 | 끊임없이 진화하는 신종 프롬프트 바이패스 기법의 실시간 모니터링 적발 및 방어 룰 즉시 보정 |

#### 한줄 요약

- 최신 OWASP LLM 2025 표준 철저 준수, 단순 체크리스트 서류 점검을 넘어선 고강도 AI 레드팀 실전 모의 평가 및 런타임 회귀 시험 파이프라인 자동화를 전사 수립한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **위험 분류의 탄력적 활용 원칙 (Risk Taxonomy Utilization Principles)**: OWASP Top 10 규격을 맹목적으로 지켜야 할 고정된 규제 틀로 보지 않고, 조직 특유의 창의적 AI 보안 거버넌스 수립 및 런타임 가드레일 다층 방어 설계의 튼튼한 출발점 뼈대로 유연하게 활용하는 최적화 원칙이다.

</details>

- AI 보안은 정적인 리스트 점검이 아니므로, 서비스별 동적 **위협 모델** 대상 맞춰 아키텍처를 유연 통제하고 철저한 AI **레드팀 모의침투** 기반 방어망을 런타임 철저한 검증해야 한다.

#### 한줄 요약

- 최신 OWASP LLM Top 10 2025 표준 준수, 5대 도메인 런타임 다층 통제망, AI 레드팀 고강도 회귀 시험 및 탄력적 위험 분류 거버넌스 가드레일 체계 구축 필수.
