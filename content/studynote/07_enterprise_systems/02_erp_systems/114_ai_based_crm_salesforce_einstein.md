---
title: 114. AI 기반 CRM (AI-Powered CRM) - Salesforce Einstein·예측 분석·생성형 AI
date: '2026-04-19'
tags:
- studynote-enterprise-systems
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[190_ai_llm_requirements_specification|AI]] 기반 CRM은 운영·분석·협업 CRM에 **[[190_ai_llm_requirements_specification|AI]]/ML 엔진을 내장**하여, 리드 스코어링·이탈 예측·자동 응답·[[105_exploratory_data_analysis|감성 분석]]을 **실시간·자동으로** 수행하는 차세대 CRM이다.
> 2. **가치**: Salesforce Einstein이 대표적이며, "이 거래가 성사될 [[130_probability|확률]] 85%", "이 고객은 다음 달 이탈 위험 72%"와 같은 **예측 인사이트를 [[107_crm_customer_relationship_management|CRM]] 화면에 자동 표시**한다.
> 3. **판단 포인트**: [[087_process_state_transition|생성]]형 [[190_ai_llm_requirements_specification|AI]]([[302_gpt_autoregressive|GPT]]) 결합으로 **상담 요약 자동 [[087_process_state_transition|생성]]·이메일 초안 작성·고객 질문 자동 응답**이 가능해졌으며, 이는 CRM의 패러다임을 "도구"에서 "[[190_ai_llm_requirements_specification|AI]] 에이전트"로 전환시키고 있다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    CRM 진화 단계                                      │
├───────────────────────────────────────────────────────┤
│  [1세대] 수첩·엑셀 — 수동 고객 관리                   │
│  [2세대] 운영 CRM — SFA·MA·CSS 자동화               │
│  [3세대] 분석 CRM — DW + 데이터 마이닝               │
│  [4세대] AI CRM — 예측·생성·자율 에이전트             │
│      └── Einstein: "이 리드 계약 확률 85%"           │
│      └── Copilot: "상담 요약 자동 생성"               │
│      └── Agent: "고객 질문에 AI 자동 응답"            │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 기존 CRM이 영업사원의 수첩을 디지털화한 것이라면, [[190_ai_llm_requirements_specification|AI]] CRM은 수첩이 스스로 "오늘 김 사장에게 전화하세요, 계약 [[130_probability|확률]] 85%"라고 말하는 **[[190_ai_llm_requirements_specification|AI]] 비서**다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[190_ai_llm_requirements_specification|AI]] [[107_crm_customer_relationship_management|CRM]] 핵심 기능

| 기능 | [[190_ai_llm_requirements_specification|AI]] 역할 | 비즈니스 효과 |
|:---|:---|:---|
| **리드 스코어링** | ML로 가망→계약 전환 [[130_probability|확률]] 예측 | 영업 우선순위 자동 정렬 |
| **이탈 예측** | XGBoost로 해지 위험 고객 [[655_ir_detection_analysis|식별]] | 선제적 리텐션 캠페인 |
| **[[105_exploratory_data_analysis|감성 분석]]** | NLP로 이메일·전화 감정 [[104_classification_analysis|분류]] | 불만 고객 즉시 에스컬레이션 |
| **상담 요약** | GenAI로 통화 내용 자동 요약 | 상담원 후처리 시간 80% 감소 |
| **[[190_ai_llm_requirements_specification|AI]] 에이전트** | 고객 질문에 자동 응답·주문 처리 | CS 인건비 30% 절감 |

- **📢 섹션 요약 비유**: [[190_ai_llm_requirements_specification|AI]] CRM은 영업팀의 **자비스(Jarvis)**다. "오늘 뭐 할까요?"라고 물으면 "A고객에게 전화, B고객에게 쿠폰, C고객 이탈 위험"이라고 알아서 정리해준다.

---

## Ⅲ. 비교 및 연결

| 비교 | 전통 [[107_crm_customer_relationship_management|CRM]] | [[190_ai_llm_requirements_specification|AI]] [[107_crm_customer_relationship_management|CRM]] |
|:---|:---|:---|
| **인사이트** | 수동 분석 (리포트) | **자동 예측 (실시간)** |
| **행동 제안** | 없음 ([[001_dikw_pyramid|데이터]]만 제공) | **"지금 전화하세요" 추천** |
| **고객 응대** | 상담원 100% | **[[190_ai_llm_requirements_specification|AI]] 70% + 상담원 30%** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 도입 효과
- **리드 스코어링**: 영업팀이 상위 20% 리드에 집중 → 계약 전환율 30% 향상.
- **[[190_ai_llm_requirements_specification|AI]] 상담**: 단순 문의(주문 조회·배송 추적) → [[190_ai_llm_requirements_specification|AI]] 자동 처리 → 상담원은 복잡한 건만 처리.

---

## Ⅴ. 기대효과 및 결론

[[190_ai_llm_requirements_specification|AI]] CRM은 "[[001_dikw_pyramid|데이터]]를 보여주는 도구"에서 "행동을 제안하고 실행하는 에이전트"로 진화하고 있으며, Salesforce Einstein Copilot·HubSpot [[190_ai_llm_requirements_specification|AI]]·Zoho Zia가 대표적이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Salesforce Einstein** | [[190_ai_llm_requirements_specification|AI]] CRM의 대표 제품 |
| **리드 스코어링** | ML 기반 계약 전환 [[130_probability|확률]] 예측 |
| **이탈 예측** | 해지 위험 고객 선제 [[655_ir_detection_analysis|식별]] |
| **[[087_process_state_transition|생성]]형 [[190_ai_llm_requirements_specification|AI]] (GenAI)** | 상담 요약·이메일 초안 자동 [[087_process_state_transition|생성]] |
| **[[190_ai_llm_requirements_specification|AI]] 에이전트** | 고객 질문 자동 응답·주문 처리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수첩·엑셀 CRM (1990s)]
    │
    ▼
[SaaS CRM (Salesforce, 2000s) — 클라우드 CRM]
    │
    ▼
[분석 CRM + ML (2015~) — 이탈 예측, 리드 스코어링]
    │
    ▼
[Einstein / AI CRM (2018~) — CRM 내장 AI]
    │
    ▼
[현재: GenAI CRM Agent — 자율 고객 응대·행동 실행]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 옛날 CRM은 손님 정보를 **적어두기만** 하는 수첩이었어요.
2. [[190_ai_llm_requirements_specification|AI]] CRM은 수첩이 스스로 **"내일 이 손님이 안 올 것 같으니 쿠폰을 보내세요!"**라고 말해줘요.
3. 심지어 **AI가 직접 손님에게 답장**을 보내주니까, 가게 사장님은 더 중요한 일에 집중할 수 있답니다!
