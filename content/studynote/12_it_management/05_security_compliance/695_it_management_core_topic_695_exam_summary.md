+++
title = "695. IT 경영 관리 핵심 토픽 695번 시험 요약 (IT Management Core Topic 695 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# 695. IT 경영 관리 핵심 토픽 - IT 거버넌스 및 정보화 전략(ISP) 요약

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019, ISO/IEC 38500, Balanced Scorecard(BSC) 프레임워크를 기반으로 IT 의사결정권·책임·통제 구조(IEEE Std 12207 기반 프로세스 거버넌스)를 5대 영역(전략·성과·규제·문화·감사)으로 정렬하여 Value Governance Loop를 구현하는 경영 체계
> 2. **가치**: Forbrugerstyrelsen(2015) 연구에 따르면 성숙도 Level 3 도달 시 IT 투자 ROI 평균 27% 개선, 프로젝트 실패율 38%->12% 감소, Time-to-Market 41% 단축, ISO 38500 준수 시 TCO 18% 절감
> 3. **판단 포인트**: 중앙집중형(Centralized) vs 분산형(Decentralized) 거버넌스 모델, RACI 매트릭스의 Responsible·Accountable·Consulted·Informed 4분면, BSC의 4관점(Financial·Customer·Internal Process·Learning&Growth) 간 인과관계 사슬(Strategy Map) 검증, BPR(해머/챔피) vs Six Sigma vs Lean IT 방법론 선택 기준

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX, Digital Transformation) 가속화와 4차 산업혁명 기술(AI, IoT, Blockchain, Cloud, BigData)의 융합으로, 기업의 IT 부서는 단순 비용센터(Cost Center)에서 가치창출센터(Value Center)로 역할이 재정의되고 있다. 한국정보화진흥원(KIAT)의 「2024 정보화 통계조사」에 따르면 국내 300인 이상 기업의 연간 IT 예산은 매출액 대비 평균 3.8%를 차지하며, 이 중 약 23%가 정렬되지 않는(Non-Aligned) 투자로 손실된다. 따라서 IT 거버넌스는 **비즈니스 전략과 IT 투자 간 정렬(Strategic Alignment)**을 보장하고, **이해관계자(Stakeholder) 가치 최적화**를 위한 통제 구조를 제공한다.

기존의 IT 관리는 기술 중심(Siloed, 기술 부서 독자 운영) 패러다임에서 벗어나, **거버넌스-관리-운영(Govern-Build-Run)** 3계층 모델로 진화했다. COBIT 5(2012) -> COBIT 2019(ISACA 발표)로 발전하면서 40개 관리 목표(Management Objective)와 7개 컴포넌트(Principles, Policies, Frameworks...), 포커스 영역(Focus Area) 개념이 추가되어 **맞춤형 거버넌스 시스템(Customized Governance System)** 설계가 가능해졌다.

```text
+------------------------------------------------------------------+
|             IT 거버넌스 진화 패러다임 비교 (Legacy vs Modern)      |
+------------------------------------------------------------------+
|                                                                  |
|  [Legacy: 1990s~2000s]                [Modern: 2019~현재]        |
|  +---------------------+              +---------------------+    |
|  |  IT Department Silo |   --->        |  Enterprise-Wide    |    |
|  |  (Cost Center)      |              |  Value Governance   |    |
|  +----------+----------+              +----------+----------+    |
|             |                                    |              |
|  +----------v----------+              +----------v----------+    |
|  |  Reactive Operation |   --->        |  Proactive Strategy |    |
|  |  (Break-Fix)        |              |  (AI-Driven)        |    |
|  +----------+----------+              +----------+----------+    |
|             |                                    |              |
|  +----------v----------+              +----------v----------+    |
|  |  Technical KPIs     |   --->        |  Balanced Scorecard |    |
|  |  (Uptime, MTBF)     |              |  4 Perspectives     |    |
|  +----------+----------+              +----------+----------+    |
|             |                                    |              |
|  +----------v----------+              +----------v----------+    |
|  |  Project-Funded IT  |   --->        |  Portfolio Mgmt     |    |
|  |  (Tactical)         |              |  (Strategic)        |    |
|  +---------------------+              +---------------------+    |
|                                                                  |
|  문제점:                                             해결책:      |
|  • Shadow IT 35%                                     • RACI Matrix|
|  • 정렬 실패 60%                                     • COBIT 2019 |
|  • ROI 측정 불가 72%                                  • BSC 4관점  |
+------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **"배의 키잡이(Rudder)"**와 같다. 엔진 파워(기술력)가 아무리 강해도 키잡이 없이 표류하면 난파당하고, 키잡이(거버넌스)가 있어야 항구(경영 목표)까지 안전하게 도달한다. COBIT이 나침반이라면 RACI는 갑판 위 승무원들의 역할 분담표다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 거버넌스의 3대 핵심 축은 **(1) 의사결정 구조(Decision Rights)**, **(2) 정렬 메커니즘(Alignment Mechanism)**, **(3) 통제 프로세스(Control Process)**이다. COBIT 2019는 이를 **Governance System Principle 6(Governance System Tailored to Enterprise Needs)**에 따라 5개 도메인(EDM: Evaluate, Direct, Monitor / BAI: Build, Acquire, Implement / DSS: Deliver, Service, Support / MEA: Monitor, Evaluate, Assess)의 **40개 관리목표(Management Objective)**로 분해한다.

### 거버넌스-관리-운영 3계층 (Govern-Build-Run)

```text
+--------------------------------------------------------------------+
|         COBIT 2019 3-Layer Architecture: EDM-BAI-DSS-MEA           |
+--------------------------------------------------------------------+
|                                                                    |
|  +--------------------------------------------------------------+  |
|  |  Layer 1: GOVERN (EDM - 5개 목표)                            |  |
|  |  +------+------+------+------+------+                       |  |
|  |  |EDM01 |EDM02 |EDM03 |EDM04 |EDM05 |  Board/CIO           |  |
|  |  |거버넌|거버넌|거버넌|자원  |위험  |  Level 의사결정       |  |
|  |  |프레임|요구사항|이해관|관리  |관리  |                       |  |
|  |  |워크  |정의   |계자  |      |      |                       |  |
|  |  +------+------+------+------+------+                       |  |
|  +--------------------------------------------------------------+  |
|                              |                                     |
|                              v (Direct & Monitor)                  |
|  +--------------------------------------------------------------+  |
|  |  Layer 2: BUILD (BAI - 11개 목표)                            |  |
|  |  +------+------+------+------+------+------+                 |  |
|  |  |BAI01 |BAI02 |BAI03 |BAI04 |BAI05 |...   |  PMO/Architect |  |
|  |  |관리프|요구사|솔루션|가용성|조직  |      |  Level 구현     |  |
|  |  |로그램|항정의|구축  |관리  |변화  |      |                 |  |
|  |  +------+------+------+------+------+      |                 |  |
|  +--------------------------------------------------------------+  |
|                              |                                     |
|                              v (Plan & Execute)                     |
|  +--------------------------------------------------------------+  |
|  |  Layer 3: RUN (DSS + MEA - 24개 목표)                       |  |
|  |  +------+------+------+------+------+------+                 |  |
|  |  |DSS01 |DSS02 |DSS03 |DSS04 |MEA01 |MEA02 |  Ops/Service   |  |
|  |  |운영  |서비스|성능  |연속성|성과  |내부  |  Level 운영     |  |
|  |  |관리  |요청  |문제  |      |모니터|감사  |                 |  |
|  |  +------+------+------+------+------+------+                 |  |
|  +--------------------------------------------------------------+  |
|                                                                    |
|  Workflow:                                                        |
|  +---------+    +---------+    +---------+    +---------+         |
|  |Strategy |---->|Portfolio|---->|Project  |---->|Service  |         |
|  |Planning |    |Mgmt     |    |Mgmt     |    |Delivery |         |
|  +---------+    +---------+    +---------+    +---------+         |
|       |              |              |              |              |
|       v              v              v              v              |
|  [BSC 4관점]   [NPV/IRR]    [Earned Value]   [SLA 99.9%]          |
|  Strategy Map  Portfolio     EVM, CPI,SPI     MTTR, MTTF          |
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate/Direct/Monitor)** | 이사회/CIO 레벨 거버넌스 의사결정 | EDM01~05 5개 목표. BSC Strategy Map으로 4관점 인과관계 사슬 정의: 학습·성장(직원 역량 20%^) -> 내부 프로세스(주문처리 40%v) -> 고객(NPS 30%^) -> 재무(매출 25%^). 분기별 거버넌스 위원회 거버넌스 리뷰(GRC: Governance-Risk-Compliance 통합) |
| **BAI (Build/Acquire/Implement)** | PMO/아키텍처 레벨 솔루션 구현 | BAI01~11 11개 목표. PMI PMBOK 7th(2021)의 12개 Principle 적용, Earned Value Management(EVM): CPI(Cost Performance Index)=EV/AC, SPI(Schedule Performance Index)=EV/PV. 임계값 CPI<0.9 또는 SPI<0.85 시 옐로우 플래그 |
| **DSS (Deliver/Service/Support)** | 운영/서비스 레벨 IT 서비스 제공 | DSS01~06 6개 목표. ITIL 4(2019)의 34개 Practice 중 Incident, Problem, Change, Service Desk 활용. SLA 가용성 99.9% = 연간 downtime ≤ 8.76시간, 99.99% = ≤ 52.6분 (Four Nine) |
| **MEA (Monitor/Evaluate/Assess)** | 감사/품질 레벨 통제 및 측정 | MEA01~04 4개 목표. ISO/IEC 27001(정보보호), ISO 9001(품질), SOX 404(재무 통제), ISAE 3402 통제 감사. RACI Matrix로 감사 책임 할당 |
| **RACI Matrix** | 역할·책임·의사결정권 명확화 | Responsible(수행), Accountable(책임, 1인 단독), Consulted(자문, 양방향), Informed(통보, 단방향). 거버넌스 위원회: A=CIO, R=IT Manager, C=CFO·CHRO, I=이사회 |

### RACI 매트릭스 상세 패턴 (Critical IT 의사결정)

```text
+--------------------+------+------+------+------+------+------+
|   IT 의사결정 항목  | 이사회|  CIO | CFO  | PMO  | 보안 | 사업부|
+--------------------+------+------+------+------+------+------+
| IT 전략수립         |  A   |  R   |  C   |  C   |  I   |  C   |
| 연 5억+ 프로젝트    |  A   |  R   |  C   |  R   |  C   |  C   |
| IT 예산 편성        |  I   |  A   |  R   |  C   |  C   |  I   |
| 보안사고 대응       |  I   |  A   |  I   |  R   |  R   |  I   |
| SLA 변경 승인       |  I   |  A   |  I   |  R   |  C   |  C   |
| 신규 기술 도입      |  I   |  A   |  C   |  R   |  C   |  C   |
+--------------------+------+------+------+------+------+------+
(A=Accountable, R=Responsible, C=Consulted, I=Informed)
```

### 핵심 알고리즘: BSC 관점 간 인과관계 가중치 산출

Strategy Map에서 4관점 간 가중치(Weight)는 **DEMATEL(Decision Making Trial and Evaluation Laboratory) 기법**으로 산출한다. 이때의 인과 그래프는 다음 식으로 표현된다:

$$T = D(I-D)^{-1}, \quad D=[d_{ij}], \quad d_{ij}=\frac{\text{영향도 점수}}{\max\text{영향도}}$$

여기서 D는 직접 영향 매트릭스, T는 총 영향 매트릭스. $(r_i - c_i)$
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 695 / 800

<- **이전**: [694. IT 경영 관리 핵심 토픽 694번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/694_it_management_core_topic_694_exam_summary/)
**다음**: [696. IT 경영 관리 핵심 토픽 696번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/696_it_management_core_topic_696_exam_summary/) ->

---
