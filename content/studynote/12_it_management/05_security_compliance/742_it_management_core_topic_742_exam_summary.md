+++
title = "742. IT 경영 관리 핵심 토픽 742번 시험 요약 (IT Management Core Topic 742 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# 742. IT 경영 관리 핵심 토픽 742번 시험 요약 (IT Management Core Topic 742 Exam Summary)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, ISO/IEC 38500 등 글로벌 거버넌스 프레임워크를 기반으로, IT 투자(Engage)-포트폴리오(Portfolio)-운영(Deliver)-성능(Performance) 4대 영역의 가치사슬(Value Chain)을 정량적 KPI(예: ROI, TCO, NPV)와 정성적 역량지표(예: CMMI, BSC 관점)로 통합 관리하는 경영 체계임.
> 2. **가치**: 성숙도 모델(예: COBIT 2019 Capability Level 0~5)을 통한 정량적 평가 시, IT-Business Alignment 지수 1단위 향상 시 기업 ROI 7~12% 개선 효과가 보고되며(Mitrophanous & Siakas, 2019), 거버넌스 부재 시 발생하는 그림자 IT(Shadow IT) 비용은 전체 IT 예산의 30~50%에 달하는 손실을 방지할 수 있음.
> 3. **판단 포인트**: 중앙집중 통제(COE) vs 분산형 거버넌스(Federated), Build vs Buy, Waterfall vs Agile(Bimodal IT), CapEx vs OpEx 전환 시 총소유비용(TCO) 3~7년 분석, 그리고 To-Be 아키텍처 도출 시 As-Is 진단의 정밀도(EA Maturity Level 1~5) 간의 트레이드오프를 의사결정 기준으로 활용해야 함.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX, Digital Transformation) 가속화와 클라우드-데이터 중심 경제로의 이행 속에서, IT 부서는 단순 비용센터(Cost Center)에서 전략적 가치센터(Value Center)로의 역할 전환을 요구받고 있다. 4차 산업혁명 시대의 IT 경영은 "How to do IT"에서 "Why to do IT"으로의 패러다임 전환을 반영하며, 2024년 기준 Gartner의 CIO Survey에 따르면 글로벌 CIO의 89%가 "IT 성과 측정을 비즈니스 가치와 직접 연결"하는 것을 최우선 의제로 제시하고 있다.

기존의 **기능 중심(Function-oriented) IT 운영**(2000년대 이전)에서는 인프라 가용률(Uptime)·장애복구시간(MTTR)·시스템 처리량(TPS)을 KPI로 삼았으나, 현재의 **가치 중심(Value-oriented) IT 경영**에서는 Business Outcome(매출 기여, 신사업 출시 시간 단축, 고객 이탈률 감소)과의 인과관계(Causality) 증명이 핵심이다. 이러한 전환은 COBIT 2019의 11개 거버넌스/관리 목적(40개 Governance/Management Objectives), ITIL 4의 34개 실무 가이드(34 Practices), ISO/IEC 38500의 6개 원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)에 체계적으로 반영되어 있다.

특히 COVID-19 이후의 **하이브리드 업무환경**과 **AI/ML 기반 업무 자동화(Hyperautomation)** 확산으로, IT-Business Alignment(전략적 정합성), Cybersecurity Resilience(사이버 회복탄력성), Sustainable IT(ESG 친화적 그린 IT)가 경영의 3대 축으로 부상했다. McKinsey(2023) 연구에 따르면, IT 거버넌스 성숙도 상위 25% 기업은 EBITDA 마진이 동종업계 평균 대비 14%p 높은 것으로 나타나, IT 경영의 질이 곧 기업 전체의 재무적 성과로 직결됨이 실증되었다.

```text
[IT 경영 4대 영역 가치사슬 (Value Chain)]

+----------------------------------------------------------------------+
|                                                                      |
|   +----------+    +----------+    +----------+    +----------+      |
|   |  ENGAGE  |---->| PORTFOLIO|---->| DELIVER  |---->|PERFORMANCE|     |
|   | (이해관계자)|   | (투자배분)|   | (서비스실행)|   | (성과측정) |     |
|   +----------+    +----------+    +----------+    +----------+      |
|        |              |              |              |               |
|        v              v              v              v               |
|   +----------+    +----------+    +----------+    +----------+      |
|   |CIO/CDO/CTO|    | 투자평가  |    |DevOps/ITIL|    |BSC/OKR  |     |
|   |거버넌스위 |    |우선순위화 |    |Agile/Lean |    |CSF/KPI  |     |
|   +----------+    +----------+    +----------+    +----------+      |
|        |              |              |              |               |
|        +--------------+----- 피드백 루프(PDCA + OODA) -------------+
|                                |                                    |
|                                v                                    |
|              +------------------------------+                       |
|              |  비즈니스 전략(Strategy) &    |                       |
|              |  디지털 전환 로드맵(DX Map)    |                       |
|              +------------------------------+                       |
+----------------------------------------------------------------------+
```

**전통적 IT 운영(As-Is)** vs **현대 IT 경영(To-Be)**:
- As-Is: 시스템 단위 단편적 관리, IT 예산 80%가 현업유지(BAU), CAPEX 중심 투자, SLI/SLO 부재
- To-Be: 서비스/포트폴리오 단위 통합 관리, Run 50% : Grow 30% : Transform 20% 예산 배분(Gartner Run-Grow-Transform 모델), OPEX 우선, E2E Observability(예: OpenTelemetry, Datadog, Dynatrace)

- **📢 섹션 요약 비유**: IT 경영은 "배(서비스)를 운항하는 해운회사"와 같다. 갑판(인프라)·선원(운영자)·항로(프로세스)·화물(데이터)·항구(거버넌스) 모두가 CAPTAIN(거버넌스 위원회)의 나침반과 항해도(EA) 없이는 안전하게 목적지에 도착할 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영의 핵심 메커니즘은 **거버넌스 체계(Governance Layer) -> 운영 체계(Management Layer) -> 실행 체계(Operational Layer)**의 3계층 의사결정 구조로 분해된다. 상위 거버넌스는 이사회-경영진-IT steering committee가, 중간 관리영역은 PMO(Program Management Office)와 EA(Enterprise Architecture) 팀이, 최하위 실행은 DevOps/Service Desk가 담당한다. 핵심은 **Feedback Loop(피드백 루프)**의 밀도와 정밀도이며, COBIT 2019의 CSF(Critical Success Factor)->KGI(Key Goal Indicator)->KPI(Key Performance Indicator) 3단계 계측 체계가 이를 구현한다.

```text
[3계층 의사결정 구조 및 데이터 흐름]

    +-------------------------------------------------------------+
    | L1: 거버넌스 계층 (Board / Steering Committee)              |
    |  +-----------------+  +-----------------+  +------------+  |
    |  | 전략위원회(SoR) |  | 리스크위원회   |  | 감사위원회  |  |
    |  | - 중기 IT 전략  |  | - 사이버보안   |  | - ITGC     |  |
    |  | - 투자한도 설정 |  | - 컴플라이언스 |  | - 내부통제 |  |
    |  +--------+--------+  +--------+--------+  +-----+------+  |
    +-----------+---------------------+----------------+---------+
                |  Cascade/Directive  |                |
    +-----------v---------------------v----------------v---------+
    | L2: 관리 계층 (PMO / EA / Service Owner)                   |
    |  +--------------+  +--------------+  +--------------+     |
    |  |  포트폴리오  |  |  서비스 카탈로그| |  아키텍처 거버|    |
    |  |  관리(PPM)   |  |  (ServiceNow) |  |  넌스(TOGAF)  |    |
    |  |  Run/Grow/Tr |  |  SLI/SLO/SLA |  |  ADM 8 Phase  |    |
    |  +---+----------+  +------+-------+  +------+-------+     |
    +------+---------------------+------------------+------------+
           | 할당/모니터링       |                  |
    +------v---------------------v------------------v------------+
    | L3: 실행 계층 (DevOps / SRE / Service Desk)                |
    |  +----------+  +----------+  +----------+  +----------+    |
    |  | Plan     |-->| Develop  |-->| Deploy   |-->| Operate  |    |
    |  |(Backlog) |  |(CI/Git)  |  |(CD/Auto) |  |(K8s/Obs) |    |
    |  +----------+  +----------+  +----------+  +----+-----+    |
    |                                                  |          |
    |                                            Monitor->Feedback |
    +--------------------------------------------------+---------+
                                                       |
                       [데이터: SLO 위반, Inc, Cost, NPS]
                                                       |
                       +-------------------------------v---------+
                       |  분석/리포팅 계층 (BI/DWH/Forecast)       |
                       |  - Apptio / Tableau / PowerBI / Looker  |
                       |  - FinOps(FOCUS 1.0)/TBM(Tech-Bus-Mgmt) |
                       +------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 거버넌스 위원회 (ISC)** | 이사회의 위임받아 IT 전략·투자·리스크의사결정 | 분기별 정례회의, RACI 매트릭스 의사결정, eTOM(Enhanced Telecom Operations Map) 또는 COBIT EDM(Evaluate, Direct, Monitor) 3단계 사이클 적용. 의결 정족수 2/3 이상, 안건별 Voting Log 보존 |
| **EA(Enterprise Architecture)** | 비즈니스-데이터-애플리케이션-기술 4개 레이어 통합 모델 | TOGAF ADM(Architecture Development Method) 8단계(Phase A~H) 또는 DoDAF 8개 Viewpoint(Zachman Framework 6W) 활용. As-Is 0->To-Be Gap 분석, 이행 로드맵(Transition Architecture) 12~36개월 수립 |
| **PMO/PPM (Project Portfolio Mgmt)** | IT 투자 우선순위화 및 실행 감독 | Gartner Run(60~70%)/Grow(20~25%)/Transform(10~15%) 예산 배분, NPV/IRR/Payback Period/ROIC 기반 정량 평가, 정성적 평가는 Strategic Fit·Risk·Urgency의 5점 척도 AHP(Analytic Hierarchy Process) 기법 |
| **ITSM (IT Service Mgmt)** | 서비스 카탈로그·인시던트·변경·문제 관리 | ITIL 4의 34 Practices 중 Incident Mgmt(MTTR ≤ 30분, FTTR ≤ 4hr), Change Mgmt(CAB 주간회의, ECR/ECAB), Problem Mgmt(RCA 5-Whys·Ishikawa), Service Desk(L1/L2/L3 에스컬레이션, 1st Contact Resolution FCR ≥ 75%) |
| **DevOps/SRE** | 지속적 인도(Continuous Delivery) 및 Site Reliability | Four Keys(DORA Metrics): Lead Time for Change(우수 ≤ 1hr), Deployment Frequency(우수 ≥ 1일 1회), Change Failure Rate(우수 ≤ 15%), MTTR(우수 ≤ 1hr). SRE의 Error Budget(예: 99.9% SLO = 월 43.83분 downtime 허용) |
| **FinOps / TBM** | 클라우드/IT 비용 최적화 및 Tech Business Management | FinOps Framework(Inform->Optimize->Operate) 3단계, FOCUS 1.0 표준 데이터 스키마, Showback/Chargeback 모델, 단위당 비용(예: API Call 1,000건당 $, 거래 1건당 $) 원가 계산 |
| **GRC (Governance-Risk-Compliance)** | 사이버보안·규제·내부통제 통합 | ISO 27001(정보보호), SOC 2 Type II, NIST CSF(Identify-Protect-Detect-Respond-Recover), ISMS-P/K-ISMS(국내), RCM(Risk Control Matrix) + SOX 404 ITGC(Information Technology General Controls) |

**핵심 측정 지표 및 공식**:
- **TCO(Total Cost of Ownership)** = CAPEX(하드웨어+소프트웨어 라이선스+구축) + OPEX(인건비+유지보수+전력+교육+장애처리) × 5년/7년
- **ROI(Return on Investment)** = (Benefits - Costs) / Costs × 100 (%) ; Benefits = (생산성 향상+매출 증가+비용 절감) - 운영비
- **NPV(Net Present Value)** = Σ (CFt / (1+r)^t) - C0 (r: 할인율, 통상 WACC 8~12%, CFt: t년 현금흐름)
- **Payback Period** = 초기투자액 / 연평균 순현금흐름 (Target: 통상 3년 이내)
- **PI(Profitability Index)** = Σ PV(Benefit) / Σ PV(Cost) ≥ 1.0 기준 채택
- **Capability Level (COBIT 2019)** = PA(Process Attribute) 6개 항목 × 6단계(0~5) = 최대 30점 만점, 2.5점 이상 시 달성 인정
- **서비스 가용성(Availability)** = MTBF / (MTBF + MTTR) × 100(%), 99.99% (Four-Nine) = 연간 52.6분 이내 downtime

- **📢 섹션 요약 비유**: 이 3계층 구조는 "병원 진료 시스템"과 같다. 1층(거버넌스) 이사진·의료진 회의, 2층(관리) 진료과·간호부·원무과, 3층(실행) 담당의·간호사·의료기사가 EMR(전자의무기록) 데이터로 연결되어 환자를 치료한다. KPI가 없으면 이 병원도 위기에 처한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 38500** | **ISO 27001** |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스+관리 통합 프레임워크 | IT 서비스 운영 실무 가이드라인 | 이사회 수준 IT 거버넌스 원칙 | 정보보호 관리체계(ISMS) |
| **대상** | CIO·감사인·컨설턴트·이사회 | Service Desk·운영자·DevOps | 이사진·최고경영자 | CISO·정보보호담당자 |
| **구성** | 40개 Governance/Management Objectives, 7개 컴
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 742 / 800

<- **이전**: [741. IT 경영 관리 핵심 토픽 741번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/741_it_management_core_topic_741_exam_summary/)
**다음**: [743. IT 경영 관리 핵심 토픽 743번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/743_it_management_core_topic_743_exam_summary/) ->

---
