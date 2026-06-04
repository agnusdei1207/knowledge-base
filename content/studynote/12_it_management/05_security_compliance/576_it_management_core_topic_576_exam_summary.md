---
title: "576. IT 경영 관리 핵심 토픽 576번 시험 요약 (IT Management Core Topic 576 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019(거버넌스·관리 목표 40개)**, **ITIL 4(SVS 34개 Practice)**, **TOGAF ADM(8 Phase)**, **PMBOK 7(8 Performance Domain)** 4대 글로벌 프레임워크를 **ISO 38500(EGov 원칙 6개)** 으로 통합·정렬하여, IT를 **전략->전락화->실행->평가->개선** 의闭环(Closed-loop) Value Chain 으로 운영하는 경영체계이다.
> 2. **가치**: McKinsey(2023) 기준 Well-Governed IT 기업은 **TCO 23% 절감**, **Time-to-Market 38% 단축**, **프로젝트 성공률 67%->89%** 향상, **EBITDA 대비 IT 투자 효율(Return on IT Invested, ROITI) 2.4배** 차이를 보이며, **DORA 4 Metrics(Deployment Frequency, Lead Time, MTTR, Change Failure Rate)** 개선을 통해 **$455M/년(Gartner 2024)** 의 Value Leakage 를 회수할 수 있다.
> 3. **판단 포인트**: ① **거버넌스 모델(중앙집중 CoE vs 분산형 Federated vs 하이브리 DGI)** 선택, ② **Agile/DevOps 채택 시 ITIL 4의 Service Value System 과의 통합 방식**, ③ **클라우드/AI 전환 시 FinOps·AIOps 도입 수준**, ④ **정보기술 감리(전자감리 7단계)와 ISMS-P 인증 갱신 주기 정합**, ⑤ **EA 사일로(Strategy/Segment/Solution)간 정합성 검증** 이 기술사 답안의 핵심 Trade-off 이다.

---

## Ⅰ. 개요 및 필요성

정보관리 기술사 576번(정보시스템 관리)은 **"IT 를 경영 자산으로 보고, 전략적 가치·리스크·성과를 정량 관리"** 하는 종합 영역이다. 4차 산업혁명(AI, Cloud, Data, IoT, Blockchain) 환경에서 IT 예산이 매출 대비 **5~12%(Global 평균 7.2%, Gartner 2024)** 를 점유함에도, **30~40% 의 IT 투자가 실패하거나 Low-Value 프로젝트**(Standish CHAOS Report 2023: 31% Challenged+Failed) 로 회수된다. 이는 ① **IT-Biz Alignment 부재**, ② **거버넌스-관리-운영 계층 간 KPI 불일치**, ③ **프로젝트·서비스·자산의 Lifecycle Fragmentation** 이 주원인이다.

이에 본 토픽은 **Strategy(BSC) -> Architecture(TOGAF/Zachman) -> Governance(COBIT/ISO 38500) -> Service(ITIL 4) -> Delivery(PMBOK/Agile/DevOps) -> Investment(TCO/ROI/NPV/ROITI) -> Security(ISO 27001/ISMS-P) -> Continuity(ISO 22301/BCM) -> Audit(전자감리)** 의 End-to-End Value Chain 을 하나의 **Governance System** 으로 통합 운영하는 체계를 다룬다.

```text
+----------------------------------------------------------------------+
|        IT 경영관리 End-to-End Value Chain (Closed-loop)               |
|                                                                      |
|  [Strategy]        [Architecture]        [Governance]                |
|   BSC/KPI  -------► TOGAF ADM  -------►  COBIT 2019                  |
|   Vision/Mission   EA Repo·Archi       EDM(05)·APO(14)               |
|         |                  |                  |                      |
|         v                  v                  v                      |
|  [Portfolio]      [Service Design]      [Delivery]                   |
|   Demand Mgmt  --►  ITIL 4 SVS   ----►  PMBOK 7 / SAFe / Scrum       |
|   Prioritization     34 Practices        8 Perf. Domain              |
|         |                  |                  |                      |
|         v                  v                  v                      |
|  [Investment]      [Operation]          [Security/BCM]                |
|   TCO/ROI/NPV  --►  AIOps/FinOps  ----►  ISMS-P/ISO 22301            |
|   ROITI·EVA         SRE·SLO            Risk·Continuity               |
|         |                  |                  |                      |
|         +------------------+------------------+                      |
|                            v                                         |
|                  [Measure & Improve]                                  |
|                   KGI/KPI · DORA · CSAT · NPS                        |
|                   +- Internal Audit (전자감리)                        |
|                   +- Continual Improvement (CSI)                      |
+----------------------------------------------------------------------+
```

한국 정보화진흥법(2023 개정)에 따라 **연 매출 1,000억 원 이상 또는 정보화투자 100억 원 이상** 공공기관은 **ISMS-P 인증 의무**(3년 주기) + **정보기술 감리**(5년 주기)가 강제되며, **클라우드 이용 통계조사** 결과 2024년 공공·금융권 **SaaS 도입률 78.4%** 로 급증하면서 **클라우드 거버넌스(CCM/CSA STAR)** 와 **FinOps** 가 필수 역량으로 부상했다.

- **📢 섹션 요약 비유**: IT 경영관리는 **자동차의 CAN Bus(Controller Area Network)** 와 같다. 엔진(Strategy), 변속기(Architecture), 계기판(Governance), 동력전달(Service), ABS(보안), 에어백(BCM) 이 각각 독립 부품이지만, **CAN 버스를 통해 실시간으로 신호를 주고받지 않으면 차는 굴러가지만 엉망** 이 된다. 4대 프레임워크(COBIT/ITIL/TOGAF/PMBOK) 는 그 **표준 통신 프로토콜** 이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 거버넌스 3層 모델 (Governance Layer)

```text
+-------------------------------------------------------------------+
| L1: Board/CxO (전략)        - Enterprise Governance               |
|     • ISO 38500 6원칙: 책임·전략·수행·적합성·규율·행동              |
|     • BSC 4관점: Financial·Customer·Internal·Learning/Growth     |
|     • KPI/KGI 연결: Strategy Map -> Scorecard -> Initiative         |
+-------------------------------------------------------------------+
| L2: Steering Committee (조율)- IT Governance (COBIT 2019)         |
|     • 5 Governance Domain: EDM(01~05): Benefits·Risk·Resource·    |
|       Compliance·Stakeholder                                     |
|     • 5 Management Objective : APO·BAI·DSS·MEA·(EDM)              |
|     • 40 Process · 7 Component : Process·Structure·People·        |
|       Skill·Culture·Tech·Evidence                                 |
+-------------------------------------------------------------------+
| L3: PMO/Service Owner (운영) - IT Management (ITIL 4)             |
|     • SVS(Value Chain): Plan->Engage->Design·Transition->Obtain·    |
|       Build->Deliver->Support                                       |
|     • 34 Practice: Service Desk·Incident·Problem·Change·SLM·CSI  |
|     • 4 Dimension: Org·People·Info·Tech·Partners·Value Streams   |
+-------------------------------------------------------------------+
```

### 2. 핵심 프레임워크 매핑

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** | 거버넌스·관리 통합 프레임워크 | **Cascade Goals**: Enterprise Goal(13) -> Alignment Goal(13) -> Management Objective(40) 으로 KPI 자동 매핑. **Design Factor 11개**로 조직 상황별 거버넌스 시스템 맞춤 설계. **Focus Area**(예: DevOps, Risk, Cyber) 별 목표 패키지 제공 |
| **ITIL 4** | 서비스 라이프사이클 관리 | **Service Value System(SVS)**: Opportunity/Demand -> Value -> Guiding Principle(7) -> Governance->Practice->Continual Improvement. **4 Dimension Model**: 조직·사람·정보·기술·파트너·가치흐름. **4P of Service Design**: People·Process·Product·Partner |
| **TOGAF 10** | EA 방법론 | **ADM(Architecture Development Method) 8 Phase**: Preliminary->A:비전->B:비즈니스->C:정보시스템->D:기술->E:기회->F:마이그레이션->G:구현거버넌스->H:변경관리. **Content Framework**: 델리버러블(32)·아티팩트(49)·빌딩블록(96) |
| **PMBOK 7 / SAFe 6** | 프로젝트·프로그램·포트폴리오 | PMBOK: **8 Performance Domain**(Stakeholder·Team·Development Approach·Planning·Work·Delivery·Measurement·Uncertainty). SAFe: **4 Config**(Essential·Large Solution·Portfolio·Full)·**5 Core Value**(Alignment·Build-in Quality·Transparency·Program Execution·Leadership)·**PI Planning 10주 Cadence** |
| **ISO 38500** | IT 거버넌스 국제표준 | **6 Principle**: Responsibility·Strategy·Acquisition·Performance·Conformance·Human Behavior. **3 Task**: Evaluate->Direct->Monitor(반복적, **EDM** 과 동일) |
| **ISO 27001 / ISMS-P** | 정보보안 관리체계 | **Annex A 93 통제 항목**(2022 개정) + **Statement of Applicability(SoA)** 의무화. **리스크 처리 방식 4종**: Modify·Retain·Avoid·Share. **PDCA 6단계** |
| **ISO 22301 / BCM** | 사업연속성 관리 | **BIA**(Business Impact Analysis)->**RTO/RPO/MTPD** 산정->**전략 선택**(Hot/Warm/Cold Site, DRaaS)->**BCP**->**연 1회 이상 훈련** |
| **DORA / SPACE** | DevOps 성과 측정 | DORA 4 Metric: **Deployment Freq·Lead Time for Change·MTTR·Change Failure Rate**(Elite/High/Medium/Low 4단계). SPACE: **S**atisfaction·**P**erformance·**A**ctivity·**C**ommunication·**E**fficiency |

### 3. IT 투자평가 핵심 수식

```
+--------------------------------------------------------------+
| ① TCO (Total Cost of Ownership)                              |
|    TCO = Direct Cost (HW·SW·인력·외주)                        |
|        + Indirect Cost (Downtime·Training·전환·감가상각)       |
|                                                              |
| ② ROI (Return on Investment)                                 |
|    ROI = (Total Benefit - Total Cost) / Total Cost × 100    |
|    ※ Benefit = Tangible(절감액·매출증대)                       |
|              + Intangible(만족도·이미지)·할인율 적용 30~70%     |
|                                                              |
| ③ NPV (Net Present Value)                                    |
|    NPV = Σ [CFₜ / (1+r)ᵗ] - Initial Investment              |
|    r=할인율(WACC), t=기간. NPV>0 이면 투자 타당                |
|                                                              |
| ④ ROITI (Return on IT Invested - Gartner 2022)               |
|    ROITI = (매출·이익 기여분 - IT 운영비) / IT 운영비         |
|    우수기업 4.5x, 평균 1.9x                                   |
|                                                              |
| ⑤ EVA (Economic Value Added)                                 |
|    EVA = NOPAT - (WACC × Invested Capital)                    |
|    ※ IT 프로젝트는 보통 3~5년 회수기간 분석                    |
|                                                              |
| ⑥ BCR (Benefit-Cost Ratio) = PV(Benefit) / PV(Cost)         |
|    BCR > 1.0 시 사업 채택                                      |
+--------------------------------------------------------------+
```

### 4. BSC-IT 4관점 + Strategy Map 패턴

```text
[Financial]     ROI·ROITI·EVA·OPEX Ratio·IT Cost per User
     ^
     | (lag indicator)  v (lead indicator)
[Customer]      CSAT·NPS·Service Availability·MTTR
     ^
[Internal Process]  DORA 4종·Change Success Rate·Incident MTTR
     ^
[Learning/Growth]  직원 이직률·인증 보유율·Training Hours·AI 리터러시
```

- **📢 섹션 요약 비유**: 이 4층 모델은 **"회사의 건강검진"** 과 같다. ① 재정(Financial) = 혈액검사, ② 고객(Customer) = 활력징후, ③ 내부프로세스(Internal) = CT/MRI, ④ 학습·성장(Learning) = 면역력. **Lag 지표**(결과)는 이미 늦고, **Lead 지표**(선행)가 개선돼야 결과가 따라온다. COBIT 의 **Cascade Goals** 가 바로 이 Lag-Lead 인과관계 사슬을 자동 추적해준다.

---

## Ⅲ. 비교 및 연결

### 1. 4대 프레임워크 정합 매트릭스

| 구분 | **COBIT 2019** | **ITIL 4** | **TOGAF 10** | **PMBOK 7** |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | 거버넌스·관리 목표 | 서비스 가치 창출 | EA 개발·적
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 576 / 800

<- **이전**: [575. IT 경영 관리 핵심 토픽 575번 시험 요약](/studynote/12_it_management/05_security_compliance/575_it_management_core_topic_575_exam_summary/)
**다음**: [577. IT 경영 관리 핵심 토픽 577번 시험 요약](/studynote/12_it_management/05_security_compliance/577_it_management_core_topic_577_exam_summary/) ->

---
