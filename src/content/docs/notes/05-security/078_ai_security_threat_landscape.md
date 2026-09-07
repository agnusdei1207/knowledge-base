---
sidebar:
  order: 78
  label: "078. AI 보안 위협 전체 구조 (AI Security Threat Landscape)"
  badge:
    text: "기출 · 85%"
    variant: note
title: "인공지능 전주기 위협 모델링 및 4대 계층 보안 : AI Security Threat Landscape (NIST AI RMF & OWASP LLM Top 10)"
date: "2026-09-07T14:00:00+09:00"
tags:
  - "notes-security"
weight: 78
extra:
  question_no: "078"
  source_status: "기출"
  source_history: "135회, 137회, 138회"
  priority: 85
  priority_note: "135•137•138회 반복 기출, NIST AI 100-1(AI RMF 1.0) / AI 600-1(GenAI Profile), OWASP Top 10 for LLM:2025, 4대 계층 위협(Data, Model, Application, Agent/Tool), 3중 신뢰 경계(Prompt, RAG, Tool) 및 Guardrails"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **AI Security Threat Landscape(인공지능 보안 위협 전체 구조 / NIST AI RMF)**: 데이터 수집·정제(Data), 파운데이션 모델 학습·가중치(Model), LLM 추론 애플리케이션(Application), 외부 API 및 DB를 실행하는 자율 에이전트(Agent/Tool)에 이르는 AI 전 생애주기에서 발생하는 고유한 보안 위협을 체계적으로 식별하고 방어하는 종합 보안 체계.
- **확률론적 추론 및 비결정론적 모델 결함(Non-deterministic Model Defect)**: 전통적인 소프트웨어와 달리 AI/LLM은 입력과 출력의 관계가 확률론적으로 동작하므로, 정적 룰셋이나 기존 웹 방화벽(WAF)으로는 프롬프트 인젝션, 환각(Hallucination), 탈옥(Jailbreak), 에이전트 권한 남용을 통제할 수 없는 구조적 한계.

</details>

- 정의/개념: NIST AI 100-1(AI RMF 1.0) 및 AI 600-1 가이드라인에 입각하여 Data(데이터 오염/포이즈닝) $\rightarrow$ Model(가중치 탈취/역공학) $\rightarrow$ Application(프롬프트 인젝션/탈옥) $\rightarrow$ Agent(도구 오용/C2 유출) 의 4대 계층 위협 모델을 정립하고, 3중 신뢰 경계(Prompt, RAG, Tool)와 LLM Guardrails 를 구축하는 AI 신뢰 보증 아키텍처
- 배경/필요성: 생성형 AI 및 LLM 기반 자율 에이전트의 급속한 도입으로 인해, 기존의 결정론적(Deterministic) 소프트웨어 보안 통제(WAF/IPS)로는 자연어 기반의 프롬프트 인젝션, 학습 데이터 포이즈닝, 모델 역공학, 에이전트의 비인가 도구 실행 및 기밀 유출과 같은 비결정론적 AI 위협을 방어하지 못하는 근본 한계가 노출됨에 따라, **NIST AI RMF** 1.0(AI 100-1/600-1) 및 OWASP Top 10 for LLM 표준에 기반하여 Data, Model, Application, Agent의 4대 계층 전주기 위협 모델과 3중 신뢰 경계(Prompt, RAG, Tool) 및 Guardrails를 통합하는 AI 보안 아키텍처를 도입하여 AI 전 생애주기 위협의 체계적 식별, 비신뢰 입력 격리 및 Human-in-the-loop 기반의 신뢰 가능한 인공지능(Trustworthy AI) 거버넌스를 달성할 필요

#### 한줄 요약
- Data, Model, Application, Agent의 4대 계층에 걸쳐 3중 신뢰 경계와 Guardrails를 구축하여 AI 전주기 위협을 방어한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **3중 신뢰 경계(Triple Trust Boundaries)**:
  1. **프롬프트 경계 (Prompt Boundary)**: 시스템 지시어(System Prompt)와 비신뢰 사용자 입력을 구분하는 인라인 검증선.
  2. **RAG 경계 (RAG Boundary)**: 외부 벡터 DB에서 검색된 문서 조각을 프롬프트 명령어로 오인하지 않도록 태깅·격리하는 경계.
  3. **도구 경계 (Tool Boundary)**: AI 에이전트의 API 호출 및 DB 쿼리 실행이 사용자의 인가 범위를 초과하지 못하도록 제어하는 런타임 관문.

</details>

- 전 생애주기 다계층 방어 (Code-to-Agent Defense): 데이터 수집부터 최종 에이전트 액션까지 계층별 맞춤형 보안 통제 적용
- 능동적 적대적 평가 (Continuous Red Teaming): 자동화된 탈옥 프롬프트 및 인젝션 공격 도구를 통해 LLM의 안전성 한계를 지속적 벤치마킹
- Human-in-the-loop 기반 고위험 액션 차단: 금융 이체, DB 레코드 삭제 등 파괴적 에이전트 명령 실행 시 반드시 인간 관리자의 최종 승인 강제

#### 한줄 요약
- 4대 계층 모델링, **3중 신뢰 경계**(Prompt/RAG/Tool), 지속적 레드팀 평가, Human-in-the-loop 승인을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **AI 보안 4대 도메인 및 Guardrails**:
  - **Data Security**: 학습 데이터 계보(Lineage) 추적 및 PII 비식별화.
  - **Model Security**: 모델 가중치 암호화 및 TEE(기밀 컴퓨팅) 구동.
  - **Prompt Guardrails**: NeMo Guardrails, Llama Guard 등을 통한 입력/출력 실시간 검사.
  - **Agent Sandbox**: 에이전트 도구 실행을 제한하는 격리 샌드박스 및 Egress 통제.

</details>

```text
[AI 보안 위협 및 방어 아키텍처]
├─ 데이터 및 모델 공급망 계층
│  ├─ 데이터 계보 추적 및 정제 (Poisoning 방지)
│  └─ 가중치 암호화 및 기밀 컴퓨팅 (TEE)
├─ 추론 및 애플리케이션 계층 (3중 신뢰 경계)
│  ├─ 프롬프트 경계 (Guardrails 인젝션 필터링)
│  ├─ RAG 경계 (권한 기반 문서 선별 및 태깅)
│  └─ 시스템 지시어와 비신뢰 문맥 격리
└─ 에이전트 및 도구 실행 계층
   ├─ 도구 파라미터 유효성 검증 (Policy)
   ├─ 고위험 액션 인간 승인 (Human-in-the-loop)
   └─ 격리 샌드박스 런타임 및 Egress 통제
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| 데이터 보안 계층 | 학습 데이터 오염(Poisoning)을 방지하기 위한 계보 검증, 정제 및 PII 마스킹 |
| 모델 보안 계층 | 모델 역공학 및 가중치 탈취를 차단하는 가중치 암호화와 TEE 기밀 컴퓨팅 적용 |
| 애플리케이션 보안 계층 | 프롬프트 인젝션과 탈옥을 방어하는 시스템 프롬프트 격리 및 가드레일 필터링 |
| 에이전트 보안 계층 | 도구 오용과 데이터 유출을 막는 최소 권한 부여, 샌드박스 격리 및 인간 승인 강제 |
| AI 거버넌스 체계 | 편향, 환각, 규제 미준수에 대응하는 NIST AI RMF 준수 및 상시 레드팀 평가 |

#### 한줄 요약
- Data, Model, Application, Agent 계층별 통제와 Guardrails 및 지속적 거버넌스가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **안전한 AI 에이전트 추론 및 실행 5단계 흐름**:
  1. 사용자 신원/권한 확인 및 프롬프트 인젝션 가드레일 검사
  2. 사용자 ACL에 기반한 RAG 벡터 데이터 선별 및 문맥 격리
  3. LLM 모델 추론 및 응답/도구 호출 제안 생성
  4. 도구 호출 정책 검증 및 고위험 액션 Human 승인
  5. 샌드박스 내부 안전 실행 및 출력 데이터 PII 마스킹

</details>

```text
1. [입력 검증 및 가드레일] 사용자 프롬프트 수신 ➔ LLM Guardrails가 탈옥/인젝션 시그니처 검사
            │
            ▼
2. [권한 기반 RAG 검색 (ACL Retrieval)]
    ├─ 사용자 IAM 권한 범위 내의 사내 문서만 벡터 DB에서 선별 추출
    └─ 검색된 텍스트를 `<context>` 태그로 감싸 시스템 명령어와 명확히 격리
            │
            ▼
3. [LLM 모델 추론] LLM이 문맥을 참조하여 "결제 DB 환불 API 호출" 도구 실행 JSON 생성
            │
            ▼
4. [도구 경계 정책 및 Human 승인]
    ├─ Policy Engine이 환불 금액 파라미터 검증 (100만 원 초과 확인)
    └─ [고위험 트랜잭션 판정 ➔ 재무 관리자 화면에 승인 팝업 요청 (Human-in-the-loop)]
            │
            ▼
5. [샌드박스 실행 및 안전 응답]
    ├─ 관리자 승인 획득 후 격리된 샌드박스에서 백엔드 환불 API 실행
    └─ 모델 출력 텍스트의 PII/기밀 노출 여부를 최종 검사한 후 사용자에게 응답 반환
```

1. 입력 검증 및 가드레일: 인젝션 입력 검사
2. 권한 기반 RAG 검색: 사용자 ACL로 문서 선별
3. LLM 모델 추론: 응답과 도구 호출 제안 생성
4. 도구 경계 정책 및 Human 승인: 고위험 실행 인가
5. 샌드박스 실행 및 안전 응답: 출력 민감정보 검사

#### 한줄 요약
- 검사 지점을 늘릴수록 응답 지연과 정상 요청 오차단이 함께 늘어나므로, 되돌릴 수 있는 출력에는 자동 가드레일을 두고 비가역 도구 실행에만 사람 승인을 배치하는 편이 비용 대비 실익이 크다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **AI 4대 계층별 대표 위협 및 대응 비교**: Data, Model, Application, Agent의 비교.

</details>

| 계층 | 대표적 공격 기법 | 침해 파급력 및 위험 | 핵심 보안 대책 |
|:---|:---|:---|:---|
| Data Level | 데이터 오염(Poisoning), 백도어 주입 | 모델 전체가 악성 의도대로 오동작 | 데이터 계보 검증, PII 필터링 |
| Model Level| 가중치 탈취, 모델 역공학(Inversion) | 수백억 원 규모의 AI 지적재산권 유출 | 가중치 암호화, TEE 기밀 컴퓨팅 |
| App Level | 직접/간접 프롬프트 인젝션, 탈옥 | 시스템 프롬프트 무력화 및 환각 오용 | 3중 신뢰 경계, NeMo Guardrails |
| Agent Level| 도구 실행 하이재킹, C2 데이터 유출 | 실제 인프라 파괴, 비인가 DB 삭제 | 최소 권한, Human-in-the-loop |

#### 한줄 요약
- Data는 오염 방지, Model은 가중치 암호화, App은 프롬프트 격리, Agent는 권한 통제와 Human 승인으로 방어한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NIST AI 100-1(AI RMF 1.0) & AI 600-1(Generative AI Profile)**: AI 시스템의 거버넌스(Govern), 매핑(Map), 측정(Measure), 관리(Manage) 4대 기능과 생성형 AI 특화 위험(인젝션, 환각, 탈옥) 대응 가이드라인.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 전사 AI 거버넌스 체계 부재로 인해 임직원이 비인가 생성형 AI에 기업 핵심 소스코드를 입력하여 발생하는 기밀 유출 사고 | **NIST AI 100-1** AI RMF 1.0 프레임워크 전사 준용 및 CASB/DLP 연동 기반 엔터프라이즈 AI 보안 게이트웨이 구축 | 기업 내부 기밀의 외부 AI 전송 100% 원천 차단 및 전사 AI 위험 가시성 확보 |
| LLM을 활용한 RAG 애플리케이션에서 비신뢰 문서를 파싱하다 간접 프롬프트 인젝션(Indirect Prompt Injection)에 의한 탈옥 발생 | NIST AI 600-1 가이드라인 준수, 프롬프트/RAG 3중 신뢰 경계 수립 및 NeMo Guardrails 입력/출력 검증 강제 | 악의적인 프롬프트 인젝션 및 시스템 지시어 무력화 100% 선제 차단 |
| AI 자율 에이전트가 비인가 명령을 생성하여 프로덕션 데이터베이스의 핵심 테이블을 삭제하거나 비인가 송금을 실행하는 대형 사고 | 에이전트 도구에 최소 권한(Least Privilege) 적용 및 파괴적/금융 고위험 액션 시 Human-in-the-loop 승인 강제 | 에이전트의 독단적 파괴 명령 실행 원천 차단 및 시스템 무결성 100% 보장 |

#### 한줄 요약
- AI RMF로 거버넌스를 확립하고, 3중 신뢰 경계로 인젝션을 막으며, Human-in-the-loop로 에이전트 사고를 방지한다.

## Ⅶ. 결론

- 전통적인 IT 인프라 보안을 넘어 비결정론적 확률 모델과 자율 에이전트의 전 생애주기 위험을 포괄적으로 관리하는 현대 생성형 AI 보안 및 신뢰성 거버넌스(NIST AI RMF / OWASP LLM Top 10)의 최상위 종합 프레임워크로 확고히 자리 잡았으며, AI 레드티밍(Red Teaming) 자동화 및 멀티모달 가드레일로 진화하는 가운데, 실무 엔터프라이즈 AI 시스템 구축 시에는 학습 데이터 계보(Lineage) 및 TEE 기반 모델 가중치 암호화, 시스템 지시어와 비신뢰 RAG 문맥을 분리하는 3중 신뢰 경계(Triple Trust Boundaries) 구축, NeMo Guardrails/Llama Guard 기반 입출력 실시간 필터링, 파괴적 도구 호출에 대한 Human-in-the-loop 최종 승인 파이프라인 강제를 결합하여 완벽한 AI 보안 전주기 무결성을 완성

#### 한줄 요약
- 4대 계층 방어와 3중 신뢰 경계 및 Human-in-the-loop 승인을 결합하여 전주기 AI 보안을 완성한다.
