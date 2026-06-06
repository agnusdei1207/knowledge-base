---
title: "IT Management Core Topic 548 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

# 548. IT-Portfolio 기반 가치중심 투자관리 및 거버넌스 프레임워크 (Value-Driven IT Investment Management & Governance Framework)

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT-Portfolio Management는 COBIT 2019의 **Align-Plan-Organize(APO) 7개 관리 목적**과 ISO/IEC 38500의 6원칙(Evaluate-Direct-Monitor)을 통합하여, Run-the-Business(70%) / Grow-the-Business(20%) / Transform-the-Business(10%)의 3-Bucket 자원을 NPV·IRR·EVA·옵션가치 기준으로 배분하는 **의사결정 거버넌스 체계**이다.
> 2. **가치**: McKinsey Global Institute 분석 결과 PPM 성숙도 Level 4-5 도달 기업은 IT 투자 회수율 **+28%**, 프로젝트 실패율 **-42%**, Time-to-Market **-35%**를 달성하며, Gartner는 2026년 글로벌 Enterprise PPM 시장이 **$8.9B 규모**로 성장 전망(2024 대비 CAGR 12.3%).
> 3. **판단 포인트**: **Trade-off ① 정량 ROI 모델 vs 정성 전략 정합성 모델** 간 가중치 배분(전형 60:40), **Trade-off ② 중앙집중 포트폴리오 통제(Stage-Gate) vs 분권형 제품 중심 운영(SAFe LPM)** 선택, **Trade-off ③ Capex vs Opex 배분** (Capex 35~45% / Opex 55~65% 적정), 그리고 의사결정 속도(Waterfall 6개월 vs Agile 2주 Cadence)를 사업 Criticality로 분리.

---

## Ⅰ. 개요 및 필요성

2024년 Gartner 보고에 따르면 글로벌 CIO의 78%가 "가장 큰 과제는 IT 예산 대비 가치 입증(ROI Justification)"이라고 답했다. 한국 정보화진흥원의 *2024 디지털 전환 실태조사*에서도 국내 대기업의 64%가 IT 투자 정당화 실패로 프로젝트가 중단된 경험이 있다고 응답했다. 이는 **전통적 Cost-Center 관점의 IT 예산관리**(연간 증분 예산 + 부서별 할당)가 한계에 도달했음을 의미한다.

전통 모델은 "작년에 100억 썼으니 올해도 100억"식의 **증분 예산(Incremental Budgeting)**으로 운영되어, (1) 사후 통제(Ex-post) 중심의 통시적 낭비, (2) 전략-IT 정합성 부재, (3) Value Realization 시점과 예산 확정 시점의 비대칭 문제를 야기한다. 반면 가치 중심 Portfolio 모델은 **사전 우선순위화(Ex-ante Prioritization) + 사후 가치 실현 추적(Value Realization Tracking)**을 통합한다.

```text
+-------------------------------------------------------------------+
|            전통 IT 예산관리 vs Portfolio 가치중심 관리             |
+-------------------------------------------------------------------+
|                                                                   |
|  [전통 모델]                          [Portfolio 모델]            |
|  +------------+                       +-----------------+        |
|  |연간 예산한도|  --증분배분--►        |전략 목표(KPI)  |        |
|  | (Cap 고정) |                       | + Risk Appetite |        |
|  +------------+                       +--------+--------+        |
|        |                                       |                 |
|        v                                       v                 |
|  +------------+                       +-----------------+        |
|  |부서별 할당 |                       |Pool: N개 투자후보|        |
|  | (수동 협상)|                       |(Idea/Project/Ap)|        |
|  +------------+                       +--------+--------+        |
|        |                                       |                 |
|        v                                       v                 |
|  +------------+                       +-----------------+        |
|  |연말 정산   |                       |가중치 점수화     |        |
|  |(예산 vs 실적)|                      |WSM/AHP/TCO+NPV |        |
|  +------------+                       +--------+--------+        |
|        |                                       |                 |
|        v                                       v                 |
|   사후통제 / 낭비                  사전선별 / 포트폴리오 리밸런싱   |
+-------------------------------------------------------------------+
```

```text
Portfolio 구성의 3-Bucket 분류 (Gartner IT Spend Category)

  +----------------------------------------------------------+
  | RTB (Run-the-Business)        ---  70%  --  유지보수, 운영|
  | +- 인프라 운영, Helpdesk, 라이선스, 보안 패치            |
  | +- 평가: 효율성, 안정성, TCO 절감                        |
  +----------------------------------------------------------+
  | GTB (Grow-the-Business)      ---  20%  --  사업 확장     |
  | +- 신규 기능, 채널 확장, CRM 고도화, 데이터 분석         |
  | +- 평가: 매출증대, 점유율, 고객만족(CSAT/NPS)            |
  +----------------------------------------------------------+
  | TTB (Transform-the-Business) ---  10%  --  디지털 전환   |
  | +- AI/ML, Cloud Migration, 플랫폼 재설계, 신규 비즈니스 |
  | +- 평가: 옵션가치, Time-to-Market, Innovation Index     |
  +----------------------------------------------------------+
        ^              ^              ^
   Risk Appetite: 낮음         중립           높음
   투자회수기간: 12개월 이내    18-36개월       36개월+
```

기존의 **IT 재무관리(IT Financial Management, ITSFM)** 관점만으로는 비즈니스 가치·전략·리스크를 동시 최적화할 수 없다. 따라서 본 토픽에서는 COBIT 2019 APO 계열 관리목표(APO05-Managed Portfolio / APO06-Managed Budget & Costs / APO12-Managed Risk)와 ISO 38500 6원칙, PMBOK 7의 Value Focus Principle을 **하나의 거버넌스 프레임워크로 통합**하는 관점을 다룬다.

- **📢 섹션 요약 비유**: "전통 예산관리는 1년 치 식료품을 1월에 한 번에 사서 냉장고에 넣어두는 것이고, Portfolio 관리는 매주 식단표를 짜고 장을 보며 균형을 맞추는 것"

---

## Ⅱ. 아키텍처 및 핵심 원리

본 프레임워크는 **4-Tier 의사결정 계층 + 5-Stage 가치 흐름**으로 구성된다. 의사결정 주체(Decision Rights)와 가치 흐름(Value Flow)를 분리하여 RACI 매트릭스로 연결한다.

```text
+-------------------------------------------------------------+
|           4-Tier IT Portfolio Governance 구조              |
+-------------------------------------------------------------+
|  +-----------------------------------------------------+   |
|  | Tier 1: 전략 거버넌스 (Strategic)                    |   |
|  |  - 의사결정 주체: 이사회, CEO, CIO, CDO              |   |
|  |  - Cadence: Quarterly (분기)                         |   |
|
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 548 / 800

<- **이전**: [547. IT 경영 관리 핵심 토픽 547번 시험 요약](/studynote/12_it_management/05_security_compliance/547_it_management_core_topic_547_exam_summary/)
**다음**: [549. IT 경영 관리 핵심 토픽 549번 시험 요약](/studynote/12_it_management/05_security_compliance/549_it_management_core_topic_549_exam_summary/) ->

---
