---
title: "IT Management Core Topic 644 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 토픽 644번은 COBIT 2019 기반 IT 거버넌스 체계와 BSC(Balanced Scorecard) for IT, KPI/CSF 연계 IT 성과 측정, TCO·NPV·IRR·Payback Period을 활용한 IT 투자 경제성 분석, 그리고 CMMI·COBIT Maturity Model 기반 IT 성숙도 평가 및 Value Realization Framework로 구성되는 IT 가치사슬(From Strategy to Value) 총론 영역이다.
> 2. **가치**: 정량·정성 지표의 균형적 관리로 IT-Business Alignment를 70% 이상 달성하고, IT 투자 회수기간(PP)을 평균 18~24개월로 단축하며, IT 거버넌스 성숙도 Level 2~3에서 Level 4~5로 도약시켜 ROI를 150~300% 개선하는 것이 핵심 KPI다.
> 3. **판단 포인트**: COBIT 2019의 40개 Governance/Management Objective 중 핵심 5~7개를 우선 도출(ESG: Evaluate, Direct, Monitor)할 것인지, BSC 4관점(재무/고객/내부/학습성장) 중 어느 관점을 Lead Indicator로 둘지, CapEx vs OpEx 투자 분류 기준을 어떻게 설정할지가 아키텍처 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

정보시스템의 규모가 SOA(서비스 지향 아키텍처)에서 MSA(마이크로서비스 아키텍처)로 진화하고, 클라우드 네이티브·AI·데이터 플랫폼이 융합되면서 IT 부서는 단순 "비용 센터(Cost Center)"에서 "가치 센터(Value Center)"로 역할이 재정의되었다. 그러나 한국 정보시스템감사통제협회(ISACA) 및 한국정보화진흥원(KIA) 조사에 따르면 국내 대기업 IT 조직의 약 **58%가 IT-Business Alignment 미흡**, **64%가 IT 성과 측정의 정량화 실패**, **71%가 IT 투자 경제성 분석의 신뢰성 부족**을 핵심 애로사항으로 보고하고 있다. 이로 인해 CFO/CEO 관점에서 IT는 "블랙홀"로 인식되며, 디지털 전환(DX) 예산 확보에 구조적 장벽이 발생한다.

기존 패러다임(1990~2010): IT 운영 중심의 기술 성과(가용성 99.9%, 응답시간 < 2초)만 측정하고, 비즈니스 성과(매출 증가, 고객 이탈률 감소, 신제품 출시 단축)와의 **인과 매핑(Causal Mapping)** 부재. 결과적으로 IT는 "성과가 좋다/나쁘다"의 주관적 평가에서 벗어나지 못함.

신규 패러다임(2015~현재): COBIT 2019 + ISO/IEC 38500 + ITIL 4 + ISO/IEC 20000을 통합한 **거버넌스-관리(Governance-Management) 이원 체계**에서 EDM(평가·지시·모니터링)의 5단계 사이클로 비즈니스 목표 -> IT 목표 -> 프로세스 목표 -> 활동 목표의 **4-Layer Goal Cascade**를 구현한다. 여기에 BSC for IT의 4관점 KPI와 Value Office의 Financial/Non-Financial Scorecard가 결합되어 "Strategy -> Measure -> Realize" 루프가 완성된다.

```text
+--------------------------------------------------------------------+
|      IT 경영 관리 통합 프레임워크 (Topic 644 Value Chain)         |
+--------------------------------------------------------------------+
|                                                                    |
|  +--------------+    +--------------+    +--------------+         |
|  |  Strategy    |---->|  Governance  |---->|  Management  |         |
|  | (전략 정렬)  |    |  (거버넌스)  |    |  (관리/운영) |         |
|  +------+-------+    +------+-------+    +------+-------+         |
|         |                   |                    |                 |
|         v                   v                    v                 |
|  +--------------+    +--------------+    +--------------+         |
|  | BSC 4관점    |    | COBIT 2019   |    | ITIL 4 SVS   |         |
|  | • Financial  |    | 40 Governance|    • Service    |         |
|  | • Customer   |    |   /Mgmt Obj  |      Value Sys  |         |
|  | • Internal   |    | • EDM 사이클 |    • 34 Practices|         |
|  | • Learning   |    | • 7 Components|   • 4 Dimensns |         |
|  +------+-------+    +------+-------+    +------+-------+         |
|         |                   |                    |                 |
|         +-------------------+--------------------+                 |
|                             v                                      |
|                  +----------------------+                          |
|                  |  Value Realization   |                          |
|                  |  • Benefit Tracking  |                          |
|                  |  • KPI 모니터링      |                          |
|                  |  • ROI/VOI 분석      |                          |
|                  +----------------------+                          |
+--------------------------------------------------------------------+
```

**왜 필요한가?** McKinsey(2023) 보고에 따르면 IT 거버넌스 성숙도 1단계 상승 시 디지털 전환 프로젝트 성공률이 **23% -> 67%**로 약 3배 증가하고, Forbes(2024) 조사에서는 IT 성과관리 체계 보유 기업의 EBITDA가 평균 **4.7%p** 더 높았다. 한국 정보시스템감사통제협회(KISIA)도 "IS-PMS(Information System Performance Management System)" 인증을 통해 공공부문 IT 성숙도 평가 기준을 강화하고 있다.

- **📢 섹션 요약 비유**: IT 경영 관리를 **자동차 계기판**에 비유하면, COBIT는 차체 프레임(규격/표준), BSC는 속도·연비·회전반경 같은 지표(미터), 경제성 분석은 연비·보험료·감가상각 같은 비용표, 성숙도 평가는 차급(경차/중형/수입차)이다. 좋은 차는 모두 균형이 맞아야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019 Governance/Management 체계

COBIT 2019는 2018년 출시되어 2019년 12월 ISO/IEC 33000 패밀리(PAM/Process Assessment Model)와 1:1 매핑되는 **40개 Governance/Management Objective**를 정의한다. 거버넌스 영역 5개(EDM), 관리 영역 35개(EDM 제외)가 존재하며, 각 Objective는 **7개 구성요소(Process, Organizational Structures, Information Flow/Items, People/Skills, Policies/Procedures, Culture/Ethics, Services/Infrastructure/Applications)**로 분해된다.

```text
+------------------------------------------------------------------+
|              COBIT 2019 7-Component Model (예: APO12)           |
+------------------------------------------------------------------+
|                                                                  |
|   +------------+   +------------+   +------------+             |
|   |  1.Process |   | 2.Org Str  |   |  3.Inf.Flow|             |
|   |  Practices |   |  (RACI)    |   |  (Input/   |             |
|   |  Activities|   |  Roles     |   |   Output)  |             |
|   +-----+------+   +-----+------+   +-----+------+             |
|         |                |                |                      |
|         v                v                v                      |
|   +------------+   +------------+   +------------+             |
|   |4.People &  |   |5.Policies  |   |6.Culture & |             |
|   | Skills     |   | Procedures |   | Ethics      |             |
|   +-----+------+   +-----+------+   +-----+------+             |
|         |                |                |                      |
|         +----------------+----------------+                      |
|                          v                                       |
|              +------------------------+                           |
|              | 7.Services/Infra/Apps |                           |
|              |   (기술적 구현체)      |                           |
|              +------------------------+                           |
|                                                                  |
|  <---- 7 Components 모두 "일관성" 있게 설계되어야 함 ---->         |
+------------------------------------------------------------------+
```

### 2. 핵심 4-Layer Goal Cascade (목표 계층화)

COBIT 2019의 가장 중요한 메커니즘은 **Stakeholder Needs -> Enterprise Goals -> Alignment Goals -> Management/Governance Goals -> Process Goals**의 5단계(실무에서는 4-Layer로 약식 표현) 계층이다. 각 단계는 **"이유(Why)"**와 **"방법(How)"**으로 구분되며, CMMI/ISO 15504 PAM의 Process Attribute(PA 1.1~2.2)와 직접 매핑된다.

```text
+-----------------------------------------------------------------+
|                  COBIT 2019 Goal Cascade                        |
+-----------------------------------------------------------------+
|                                                                 |
|  Layer 0: Stakeholder Needs (이해관계자 요구)                    |
|           • 신사업 창출, 비용 최적화, 리스크 관리                 |
|                       |                                         |
|                       v  (Why)                                  |
|  Layer 1: Enterprise Goals (13개, 재무/고객/내부/성장)           |
|           EG01 포트폴리오로 경쟁 우위                            |
|           EG09 정보 처리 비용 최적화                              |
|           EG13 디지털 제품/서비스 비즈니스 강화                  |
|                       |                                         |
|                       v  (Why)                                  |
|  Layer 2: Alignment Goals (13개, IT-Business 정렬)              |
|           AG06 비즈니스 서비스 가용성·신뢰성 향상                |
|           AG12 직원 역량 강화                                    |
|           AG09 정보 기반 의사결정 지원                            |
|                       |                                         |
|                       v  (Why)                                  |
|  Layer 3: Governance/Management Goals (40개)                    |
|           EDM02 Benefits Delivery                                |
|           EDM03 Risk Optimization                                |
|           APO12 Managed Risk                                     |
|                       |                                         |
|                       v  (How)                                  |
|  Layer 4: Process Goals / Process Activities                    |
|           APO12.01 위험 식별, 분석, 평가                        |
|           BAI01.01 프로그램 정의                                |
+-----------------------------------------------------------------+
```

### 3. 핵심 구성 요소 및 동작 방식

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate-Direct-Monitor)** | 이사회·IT Steering Committee 거버넌스 | EDM01 전략, EDM02 Benefit Delivery, EDM03 Risk, EDM04 Resource, EDM05 Transparency. 이사회가 5단계 사이클(분기/반기/연간)로 의사결정 |
| **APO (Align, Plan, Organize)** | 전략-계획-조직 정렬 | APO01 MOF, APO02 전략, APO03 엔터프라이즈 아키텍처(TOGAF/ArchiMate 연동), APO05 포트폴리오, APO12 리스크, APO13 보안 |
| **BAI (Build, Acquire, Implement)** | 솔루션 도입 및 구현 | BAI01 관리 프로그램, BAI03 솔루션 설계(MSA, IaC, GitOps), BAI09 자산관리, BAI11 품질관리 |
| **DSS (Deliver, Service, Support)** | IT 서비스 운영 | DSS01 운영관리, DSS02 SLA/OLA/UC, DSS03 인시던트/장애, DSS04 문제관리(RCA), DSS05 서비스 연속성(BCM/DR) |
| **MEA (Monitor, Evaluate, Assess)** | 성과 측정 및 감사 | MEA01 성능모니터링(BSC/KPI), MEA02 내부통제, MEA03 외부감사(SOC2/ISAE3402), MEA04 규정준수 |

### 4. BSC for IT (Balanced Scorecard) 핵심 공식

BSC for IT는 Kaplan-Norton(1992) BSC를 IT 영역에 적용한 Norton(1999) 프레임워크로, **4관점(Financial, Customer, Internal Process, Learning & Growth)** 간 **인과 관계(Cause-Effect Chain)**가 핵심이다. 예를 들어 "IT 직원 교육 시간 증가(Learning) -> 인시던트 해결 속도 향상(Internal) -> 고객 만족도 상승(Customer) -> IT 비용 회수율 증가(Financial)"의 사슬이다.

```text
+-------------------------------------------------------------+
|              BSC for IT 4-관점 In-out 모형                  |
+-------------------------------------------------------------+
|                                                             |
|  [관점 1] Financial (재무)  <---- Lag Indicator             |
|   • IT 예산 준수율 (PI1)                                     |
|   • IT 투자 ROI = (IT기인 이익) / (IT 투자비) × 100%        |
|   • Cost per Transaction (CPT)                              |
|           ^                                                 |
|           | (Causal Effect)                                 |
|           |                                                 |
|  [관점 2] Customer (고객) ------ Lead/Lag 혼합              |
|   • 사용자 만족도 (PI2)                                      |
|   • Net Promoter Score (NPS)                                |
|           ^                                                 |
|           |                                                 |
|  [관점 3] Internal Process (내부) ---- Lead Indicator       |
|   • 평균 복구시간 MTTR < 1hr                                 |
|   • SLA 준수율 ≥ 99.5%                                      |
|   • 결함률 Defect Density < 0.5/KLOC                        |
|           ^                                                 |
|           |                                                 |
|  [관점 4] Learning & Growth (학습성장) ---- Lead Indicator  |
|   • 직원 1인당 교육시간 ≥ 40hr/년                            |
|   • 핵심 자격증 취득률 (CISSP, CISM, PMP)                    |
|   • 직원 이직률 < 5%                                         |
|                                                             |
+-------------------------------------------------------------+
```

### 5. IT 투자 경제성 분석 핵심 공식

| 평가 방법 | 수식/정의 | 의사결정 기준 | 적용 시나리오 |
|---|---|---|---|
| **ROI** (투자수익률) | `ROI(%) = (총이익 - 총비용) /
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 644 / 800

<- **이전**: [643. IT 경영 관리 핵심 토픽 643번 시험 요약](/studynote/12_it_management/05_security_compliance/643_it_management_core_topic_643_exam_summary/)
**다음**: [645. IT 경영 관리 핵심 토픽 645번 시험 요약](/studynote/12_it_management/05_security_compliance/645_it_management_core_topic_645_exam_summary/) ->

---
