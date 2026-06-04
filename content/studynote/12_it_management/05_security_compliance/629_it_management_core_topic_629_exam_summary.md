---
title: "629. IT 경영 관리 핵심 토픽 629번 시험 요약 (IT Management Core Topic 629 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, ISO 38500 등 글로벌 거버넌스 프레임워크를 기반으로, 비즈니스 전략과 IT 서비스·투자·리스크를 정렬(Strategic Alignment)하여 조직의 디지털 가치 사슬(Value Chain)을 최적화하는 통합 관리 체계이다.
> 2. **가치**: 정량적 효과로 IT 투자 대비 ROI 평균 25~40% 개선, IT 장애로 인한 비즈니스 손실 60% 감소, 프로젝트 성공률 28%->72% 향상(PMI 2023), 정성적 효과로 의사결정 투명성, 규제 준수(Compliance) 및 ESG 대응 역량 강화.
> 3. **판단 포인트**: 중앙집중형(Centralized) vs 분산형(Distributed) 거버넌스 모델 선택, Balanced Scorecard(BSC) 4관점 간 KPI 충돌 시 가중치 재설계, Build vs Buy vs Cloud 의사결정 시 TCO 5개년 분석, Agile-Waterfall 하이브리드(SAFe, LeSS) 적용 범위 결정이 핵심 Trade-off.

---

## Ⅰ. 개요 및 필요성

정보기술이 단순 비용 센터(Cost Center)에서 전략적 비즈니스 인에이블러(Strategic Enabler)로 전환됨에 따라, IT 경영 관리는 더 이상 CIO의 전담 영역이 아니라 CEO·CFO·이사회 수준에서 다뤄야 할 **거버넌스 이슈**로 격상되었다. McKinsey(2022) 보고에 따르면 디지털 전환에 성공한 기업은 실패 기업 대비 EBIT 마진이 1.8배 높고, 시가총액 성장률은 2.3배 빠른 것으로 나타난다. 그러나 한국 정보화진흥원의 조사에 의하면 국내 대기업의 47%가 IT-비즈니스 전략 정렬 실패를 경험했고, 60% 이상이 IT 투자 효과 측정에 어려움을 겪고 있다.

기존 패러다임은 **기술 중심(Technology-Driven)**이었으며, 하드웨어/소프트웨어 도입 자체가 목적이었고 사후 평가(Post-Implementation Review)는 형식적이었다. 반면 새로운 패러다임은 **가치 중심(Value-Driven)**으로, 비즈니스 Outcomes(예: 신규 매출, 고객 이탈률 감소, OPEX 절감) 중심으로 IT 포트폴리오를 관리하며, 실시간 대시보드와 데이터 기반 의사결정(BI, AI/ML Analytics)을 활용한다.

```text
+-------------------------------------------------------------+
|           IT 경영 관리 패러다임 전환 (Evolution)            |
+-------------------------------------------------------------+
|                                                             |
|  [구패러다임: Technology-Driven]                            |
|   +----------+    +----------+    +----------+              |
|   | HW 도입  | ->  | SW 구축  | ->  | 운영/유지| -> (형식적)  |
|   +----------+    +----------+    +----------+   평가     |
|       v                v               v                    |
|   CAPEX 중심      일회성 프로젝트   예산 소진               |
|                                                             |
|                           ⇩ TRANSFORMATION                  |
|                                                             |
|  [신패러다임: Value-Driven]                                 |
|   +----------+    +----------+    +----------+    +------+|
|   | 전략정렬 | ->  | 포트폴리오| ->  | 실행/Agile| ->  | 측정 ||
|   | Alignment|    | Prioritize|   | Delivery |    | KPI  ||
|   +----------+    +----------+    +----------+    +------+|
|       v                v               v            v      |
|   OKR/BSC         WSJF, NPV      MVP, Scrum   실시간 대시보드|
|   ROI, Payback    Risk-Adjusted  DevOps, SRE  EBITDA 기여도  |
|                                                             |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 경영 관리는 자동차의 계기판(Strategy) + 핸들(Governance) + 내비게이션(Portfolio Mgmt)이 통합된 **운전석 전체**와 같다. 엔진(IT 인프라)만 좋다고 좋은 차가 아니듯, 전략-거버넌스-실행이 조화롭게 돌아야 목적지에 도달한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 표준 아키텍처는 **3-Layer Governance Model**로 구성된다. 최상위에는 의사결정 권한과 책임을 정의하는 **거버넌스 층(Governance Layer)**, 중간의 **관리 층(Management Layer)**은 프레임워크와 방법론을 적용하며, 최하위의 **운영 층(Operational Layer)**은 실제 IT 서비스 전달과 성능 측정을 담당한다.

```text
+------------------------------------------------------------------+
|         IT 경영 관리 통합 아키텍처 (Zachman + COBIT 기반)        |
+------------------------------------------------------------------+
|                                                                  |
|  [Layer 1] 의사결정/거버넌스 (What & Why)                        |
|   +-------------------------------------------------------+      |
|   |  +-----+   +------+   +------+   +--------------+    |      |
|   |  |Board|--->| IT   |--->|전략위|--->|감사/컴플라이언|    |      |
|   |  |이사회|   |Steer |   |사위 |   |내부통제     |    |      |
|   |  +-----+   |Comm. |   +------+   +--------------+    |      |
|   |            +------+                                   |      |
|   |  • ISO 38500 원칙(책임, 전략, 획득, 성능, 준수, 행동)|      |
|   |  • RACI Matrix: 의사결정 권한 매트릭스               |      |
|   +-------------------------------------------------------+      |
|                              v 委譲(委任)                         |
|  [Layer 2] 관리/프레임워크 (How)                                 |
|   +-------------------------------------------------------+      |
|   |  COBIT 2019  | ITIL 4  | TOGAF  | PMBOK 7  | ISO 27001|    |
|   |  (40 Gov.)   | (34 Prac| (ADM)  | (8 Perf.)| (Annex A)|    |
|   |              |  +SVS)  |        |          |          |    |
|   |  +--------------------------------------------+       |      |
|   |  | IT 전략맵 | 서비스 포트폴리오 | 프로젝트   |       |      |
|   |  | (Strategy)|   Mgmt (SPM)     | 포트폴리오 |       |      |
|   |  | BSC 4관점 |   Pipeline       |   (PfM)    |       |      |
|   |  +--------------------------------------------+       |      |
|   +-------------------------------------------------------+      |
|                              v 실행                              |
|  [Layer 3] 운영/서비스 전달 (Do & Measure)                      |
|   +-------------------------------------------------------+      |
|   |  +--------+ +--------+ +--------+ +--------+ +-----+ |      |
|   |  |DevOps |->|CI/CD   |->|모니터링|->|Incident|->|개선 | |      |
|   |  |Plan   | |Pipeline| |AIOps   | |Mgmt    | |CAPA | |      |
|   |  +--------+ +--------+ +--------+ +--------+ +-----+ |      |
|   |  SLA(99.95%) | MTTR | MTBF | CSAT/NPS |               |      |
|   +-------------------------------------------------------+      |
|                                                                  |
+------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 거버넌스 위원회 (IT Steering Committee)** | 전략-실행 정렬, 투자 승인, 우선순위 조정 | 월 1회 정기 회의, RACI 매트릭스 기반 Decision Rights, Portfolio Stop/Go/Kill 의사결정 |
| **전략 정렬 (Strategic Alignment)** | 비즈니스 목표 ↔ IT 로드맵 매핑 | Henderson & Venkatraman 4관점 모델(Strategy, Infrastructure, Process, IS) + SAMM(SAM Maturity Model) |
| **서비스 포트폴리오 관리 (SPM)** | IT 서비스·프로젝트 우선순위화 | WSJF(Weighted Shortest Job First) = CoD/BvF × Job Duration, NPV/IRR/Payback Period 분석 |
| **성능 측정 (Performance Measurement)** | KPI 모니터링 및 보고 | Balanced Scorecard 4관점(Financial, Customer, Internal Process, Learning/Growth), OKR(Objective & Key Results) |
| **리스크 & 컴플라이언스 (GRC)** | 사이버 리스크, 규제 준수 | ISO 31000 리스크 프로세스, ISO 27001 ISMS, NIST CSF 5개 Function, GDPR/개인정보보호법 매핑 |
| **IT 재무 관리 (ITFM)** | IT 비용 가시화, 차지백(Chargeback) | TCO(Total Cost of Ownership) 5개년 분석, ITFM Maturity Model(Nolan Norton Level 1~5), Showback/Chargeback |

### 핵심 알고리즘 및 의사결정 공식

**1) IT 투자 우선순위 평가 - 다기준 의사결정(MCDA)**
```
우선순위 점수 = Σ(Wi × Si) / ΣWi
  Wi: i번째 기준의 가중치 (ΣWi = 1.0)
  Si: i번째 기준의 점수 (0~10)

예) 신규 CRM 시스템 평가
  - 전략적 적합성: 9 × 0.30 = 2.7
  - 재무적 수익률: 7 × 0.25 = 1.75
  - 기술적 실현가능성: 8 × 0.20 = 1.6
  - 리스크 수준:    6 × 0.15 = 0.9
  - 규제 준수:      10× 0.10 = 1.0
  ------------------------------
  총점 = 7.95 / 10.0 -> 79.5% -> 우선 투자 대상
```

**2) SLA(Service Level Agreement) 가용성 계산**
```
가용성(%) = (총 운영시간 - 다운타임) / 총 운영시간 × 100
          = (MTBF / (MTBF + MTTR)) × 100

99.9% (Three-9) : 월 43.83분, 연 8.77시간
99.95%          : 월 21.92분, 연 4.38시간
99.99% (Four-9) : 월 4.38분, 연 52.60분
99.999% (Five-9): 월 26.30초, 연 5.26분 (Tier IV)
```

- **📢 섹션 요약 비유**: IT 경영 관리 아키텍처는 **대형 병원 시스템**과 같다. 이사회(Governance)는 의료진 윤리위원회, 관리층(Management)은 진료 과장장 회의, 운영층(Operational)은 실제 의사·간호사·의료기기에 이른다. 이 세 층 간의 **핫라인(보고 체계)**이 명확해야 환자가(비즈니스가) 제때 치료받는다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리에서 혼동되기 쉬운 핵심 프레임워크 간 비교는 매우 중요하다. 각 프레임워크는 **다른 목적과 범위**를 가지며, 실무에서는 상호 보완적으로 사용된다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **PMBOK 7** |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스 & 관리 | IT 서비스 관리 (ITSM) | IT 의사결정 지침 (Governance) | 프로젝트 관리 |
| **초점** | Value Creation, Risk Optimization | Service Value System (SVS) | 6 Principles (책임, 전략, 획득...) | 8 Performance Domains, 12 Principles |
| **대상 범위** | Enterprise IT (End-to-End) | IT Service Lifecycle | Board & Executive Level | Project-level |
| **구조** | 40 Governance/Management Objectives | 34 Practices, 4 Dimensions | 6 Principles + Model | Principles + Domains |
| **측정 도구** | Process Assessment Model (PAM) | Maturity Model | Maturity 체크리스트 | KPI, Earned Value Mgmt |
| **강점** | 컴플라이언스, Audit, Risk 연동 | Service Desk, Incident/Problem | 윤리적·법적 책임 강조 | WBS, Schedule, Cost 관리 |
| **약점** | 구현 복잡도 높음, 무거움 | 거버넌스 측면 약함 | 추상적, 구체적 도구 부족 | 프로젝트 종료 후 운영 연계 약함 |
| **적용 단계** | Layer 1 (Governance) | Layer 3 (Operational) | Layer 1 (Principle) | Layer 2~3 (Execution) |
| **인증 체계** | COBIT 2019 Foundation/Design/Implement | ITIL 4 Foundation/MP/SL | ISO 인증(BSI) | PMP, CAPM (PMI) |
| **업데이트** | 2018년 (2019 발표) | 2019년 (4th Ed.) | 2015년 (2nd Ed.) | 2021년 (7th Ed.) |

### 연계 아키텍처: 4-Framework 통합 적용

```text
+--------------------------------------------------------+
|     IT 경영 관리 프레임워크 통합 (Integrated Stack)     |
+--------------------------------------------------------+
|                                                        |
|  +----------- ISO 38500 -----------+ <- 원칙/윤리       |
|  | "Direct, Monitor, Evaluate"     |   (이사회 레벨)   |
|  +--------------+------------------+                   |
|                 v 매핑                                 |
|  +----------- COBIT 2019 ----------+ <- 거버넌스       |
|  | EDM(평가, 지시, 모니터)         |   (경영진 레벨)   |
|  | APO(정렬, 계획, 조직)            |                   |
|  | BAI(구축, 인수, 변경)            |                   |
|  | DSS(전달, 지원, 서비스)          |                   |
|  | MEA(모니터, 평가, 평가)          |                   |
|  +--------------+------------------+                   |
|                 v 구현 가이드                          |
|  +----------- ITIL 4 --------------+ <- 서비스 운영     |
|  | SVS(Value Chain)                |   (현장 레벨)     |
|  | 34 Practices                     |                   |
|  | 4 Dimensions(O,C,VT,P)         |                   |
|  +--------------+------------------+                   |
|                 v 프로젝트 단위 적용                   |
|  +----------- PMBOK 7 / SAFe ------+ <- 실행           |
|  | 8 Performance Domains            |   (팀 레벨)      |
|  | ART, PI Planning                  |                   |
|  +----------------------------------+                   |
|                                                        |
+--------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 네 프레임워크의 관계는 **건축의 4개 층위**와 같다. ISO 38500은 헌법(원칙), COBIT 2019은 도시계획(거버넌스), ITIL 4는 건물 운영 매뉴얼, PMBOK 7은 시공 매뉴얼이다. 이 네 가지가 조화롭게 통합되어야 견고한 IT 조직이라는 '건물'이 완성된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

IT 경영 관리 실무에서는 이론보다 **상황 판단**이 핵심이다. 기술사 시험에서는 CFO, CEO, CIO의 의사결정 시점에서 합리적 트레이드오프를 설명할 수 있어야 한다. 다음은 실제 컨설팅 현장에서 빈번히 마주치는 의사결정 시나리오다.

### 기술사형 판단 체크리스트

1. **투자 의사결정 시 NPV, IRR, Payback Period를 모두 산출했
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 629 / 800

<- **이전**: [628. IT 경영 관리 핵심 토픽 628번 시험 요약](/studynote/12_it_management/05_security_compliance/628_it_management_core_topic_628_exam_summary/)
**다음**: [630. IT 경영 관리 핵심 토픽 630번 시험 요약](/studynote/12_it_management/05_security_compliance/630_it_management_core_topic_630_exam_summary/) ->

---
