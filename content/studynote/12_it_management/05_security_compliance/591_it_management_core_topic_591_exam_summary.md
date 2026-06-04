+++
title = "591. IT 경영 관리 핵심 토픽 591번 시험 요약 (IT Management Core Topic 591 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT·ITIL·ISO 38500·BSC Balanced Scorecard 등 글로벌 프레임워크를 기반으로 **거버넌스-전략-포트폴리오-성과-리스크**의 5대 축을 통합 운영하여, IT가 기업 가치(Value)와 전략적 정합성(Strategic Alignment)을 창출하도록 만드는 경영 체계임.
> 2. **가치**: 정량적으로는 IT 투자 대비 ROI 15~30% 개선, 프로젝트 성공률 28%->74% 향상(PMI 2021), 운영 비용 20~35% 절감, 정성적으로는 이사회-경영진-현업 간 IT 의사결정 투명성·책임성·예측 가능성 확보.
> 3. **판단 포인트**: ① **Build vs Buy vs Cloud** 의사결정, ② 중앙집중식(COE) vs 분산형(Federated) vs 하이브리드 IT 조직 모델 선택, ③ Agile ↔ Waterfall ↔ Bimodal IT의 프로젝트 거버넌스 분리 전략, ④ CapEx vs OpEx의 재무적 영향(TCO 5년 분석) 및 ⑤ 사이버 리스크·규제 준수(컴플라이언스) 리스크의 Trade-off.

---

## Ⅰ. 개요 및 필요성

**기술사 591번(IT 경영 관리)** 영역은 단순한 IT 운영 관리가 아니라, 기업의 **전략적 의사결정 체계(Strategic Decision System)** 속에서 IT를 어떻게 **가치사슬(Value Chain)**에 통합할 것인가를 다룬다. 4차 산업혁명·Digital Transformation(DX)·ESG 경영 시대를 맞아 IT는 더 이상 **Cost Center**(비용 센터)가 아닌 **Value Center**(가치 센터)로 재정의되어야 하며, 이를 뒷받침할 **거버넌스 프레임워크**와 **성과 측정 체계**가 핵심 평가 항목이 된다.

기존(1990~2000년대)의 **IT 관리**는 시스템 가용성·장애 대응·SLA 준수 등 **Operational Excellence** 중심이었다. 그러나 2010년대 이후 클라우드·AI·데이터 분석이 보편화되면서, IT의 **전략적 포트폴리오 관리(IT Portfolio Management)**, **Agile 거버넌스**, **FinOps**(클라우드 재무 운영), **Green IT/ESG** 통합 등 보다 광범위한 경영 차원의 의사결정 요구가 폭증했다.

```text
+------------------------------------------------------------------+
|                IT 경영 관리 패러다임의 진화 (Evolution)             |
+------------------------------------------------------------------+
|                                                                  |
|  [Past]  IT 운영관리           [Present]  IT 거버넌스               |
|   (1990s)                          (2020s)                         |
|   +-------------+                  +------------------+          |
|   |  장애 관리   |                  | 가치(Value) 중심   |          |
|   |  비용 절감   |      --►        | 전략 정합성        |          |
|   |  가용성 SLA  |                  | 리스크·규제 통합   |          |
|   |  데이터센터  |                  | DX·AI·Cloud·ESG  |          |
|   +-------------+                  +------------------+          |
|          |                                 |                      |
|          v                                 v                      |
|     Cost Center                       Value Center                |
|   (TCO 최소화)                    (ROI + ROA + NPV 최대화)         |
|                                                                  |
|  +------------------------------------------------------+        |
|  |  [미래]  2026~ : Autonomous IT Governance            |        |
|  |   AI-Driven 의사결정 · 실시간 Digital Twin · Zero-Touch|        |
|  |   ESG 통합 리포팅 · Quantum-Safe 보안 · 지속가능 IT  |        |
|  +------------------------------------------------------+        |
+------------------------------------------------------------------+
```

**필요성의 핵심 동인 4가지**:
1. **전략적 정합성(Strategic Alignment)**: Henderson & Venkatraman의 **SAM(Strategic Alignment Model)** — Business Strategy ↔ IT Strategy ↔ Organizational Infrastructure ↔ IT Infrastructure의 4분면 정합 필요.
2. **규제·컴플라이언스 강화**: GDPR(2018), 개인정보보호법(2023 전면개정), EU AI Act(2024), 클라우드 보안인증制度(CSAP), ESG 공시 의무화로 거버넌스 부재 시 **과태료·신뢰도 하락** 직결.
3. **투자 효율성 증대**: McKinsey(2022) 보고에 따르면 글로벌 IT 예산의 **30% 이상**이 "잠재적浪费(Digital Waste)"로 분류되며, Portf/BizCleanser(Zero-Based Budgeting) 방식 도입이 필수.
4. **사이버 리스크의 경영 위협화**: SolarWinds(2020), Log4j(2021), Kakao 장애(2022), SK C&C(2023) 등 대형 사고 -> **Gartner 예측 2026년 사이버 리스크가 기업 CEO의 1순위 관심사**로 부상.

- **📢 섹션 요약 비유**: IT 경영 관리는 자동차의 **'통합 차량 제어 시스템(Vehicle Dynamics Control)'**과 같다. 과거에는 각 부품(엔진·브레이크·핸들)을 따로 관리했지만, 지금은 ECU·ADAS·자율주행처럼 **전략·거버넌스·리스크·성과를 하나의 통합 시스템**으로 운영해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 **5대 핵심 축**과 이를 뒷받침하는 **거버넌스 레이어 구조**는 다음과 같다.

```text
+---------------------------------------------------------------------+
|        IT 경영 관리 5대 축 통합 아키텍처 (5-Pillar Architecture)      |
+---------------------------------------------------------------------+
|                                                                     |
|  +------------------------------------------------------------+    |
|  |  [Layer 1] 이사회·경영진 의사결정 (Board / Executive)        |    |
|  |   IT 전략위원회 · CIO 리포트 · 디지털 거버넌스 위원회         |    |
|  +------------------------------------------------------------+    |
|                              ^                                     |
|  +------------------------------------------------------------+    |
|  |  [Layer 2] 거버넌스 프레임워크 (Governance Framework)        |    |
|  |   COBIT 2019 · ISO/IEC 38500 · ITIL 4 · TOGAF · CMMI       |    |
|  |   --► 40+ Governance & Management Objectives 정렬            |    |
|  +------------------------------------------------------------+    |
|                              ^                                     |
|  +------+------+----------+----------+----------------------+     |
|  | P1   | P2   |   P3     |   P4     |     P5               |     |
|  |전략  |포트  |성과·BSC  | 리스크·  |  운영·서비스          |     |
|  |기획  |폴리오|측정·KPI  | 컴플라이 |  (ITIL/FinOps)        |     |
|  |      |관리  |          | 언스     |                       |     |
|  |SAM   |PPM   |IT BSC    |ISO27001  |ITIL4·DevOps·SRE      |     |
|  |TOGAF |Agile |CMMI      |PIMS·GDPR |FinOps·AIOps          |     |
|  +--+---+--+---+----+-----+----+-----+----+------------------+     |
|     |      |        |          |          |                          |
|  +--+------+--------+----------+----------+------------------+      |
|  |  [Layer 3] 실행 체계 — 프로젝트·서비스·데이터·인프라 운영     |      |
|  |   Agile/Scrum · SAFe · CI/CD · IaC(Terraform/Ansible)       |      |
|  |   Observability(Prometheus/Grafana/OpenTelemetry)           |      |
|  +-------------------------------------------------------------+    |
|                              ^                                     |
|  +-------------------------------------------------------------+    |
|  |  [Layer 4] 측정·모니터링 (Feedback Loop)                      |    |
|  |   KPI 대시보드 · GANTT · 임원용 Cockpit · ESG 리포트         |    |
|  |   PDCA -> OODA Loop -> Continuous Improvement                 |    |
|  +-------------------------------------------------------------+    |
|                                                                     |
+---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **P1. IT 전략 기획** | 비즈니스 전략과 IT 전략의 정합성 확보 | SAM(Henderson·Venkatraman), Ward & Peppard의 **IS 전략 방법론**(5단계: Business·IS·IT·Implementation·Action Plan), **TOGAF ADM**(Architecture Development Method) — Preliminary->A(비전)->B/C/D/E->F(이행)->G(구현거버넌스)->H(변화관리)->Requirements Management |
| **P2. IT 포트폴리오 관리(PPM/ITPM)** | 한정된 IT 자원(예산·인력)의 최적 배분 | **3-버킷 포트폴리오**(McKinsey): Run-the-Business(60~70%) / Grow-the-Business(20~30%) / Transform-the-Business(5~10%) — **Project Portfolio Office(PPO)** 중심 의사결정. 평가 기준: NPV, IRR, Payback Period, Strategic Fit Score |
| **P3. IT 성과 측정·BSC** | 정량적 성과 가시화 및 책임성 확보 | **IT BSC** 4관점 — Financial(ROI·TCO) / Customer(Satisfaction·NPS) / Internal Process(Defect Rate·MTTR) / Learning & Growth(Skill Index). **CobiT의 7단계 Cascade Goals** 적용 |
| **P4. IT 리스크·컴플라이언스** | IT 위험의 식별·평가·대응·모니터링 | **ISO 27001/27002**, **ISO 31000**, **NIST CSF**(Identify·Protect·Detect·Respond·Recover), **PCI-DSS**, **PIMS(BS 10012)**, **GDPR/DSA/DMA**, **ESG 공시(TCFD/SASB)**. 위험 매트릭스(Likelihood × Impact) 및 **KRI(Key Risk Indicator)** 운영 |
| **P5. IT 운영·서비스 관리** | 서비스 가용성·효율성 극대화 | **ITIL 4 Service Value System(SVS)** — Opportunity/Demand->Value->Service Value Chain(Plan/Engage/Design&Transition/Obtain/Build/Deliver&Support/Improve)->Continual Improvement. **DevOps·SRE·AIOps** 통합, **FinOps**(클라우드 비용 최적화) |

### 핵심 원리 심화

1. **COBIT 2019의 거버넌스 시스템**: 40개의 관리 목적(Management Objectives)을 **EDM(평가·지시·모니터) 5개** + **Plan/Build/Run/Monitor 35개**로 분리. **Design Factors 11개**로 조직 상황에 맞춘 거버넌 시스템 커스터마이징.
2. **BSC Cascade**: 임원 BSC -> 사업부 BSC -> IT BSC -> 프로젝트 BSC -> 개인 BSC로 **전략 연쇄(Strategic Cascade)** — SMART KPI + Lead/Lag Indicator 균형.
3. **Agile@Scale 거버넌스**: **SAFe**(Scaled Agile Framework) — Team PI Planning -> ART -> Solution Train -> Portfolio Level의 **Lean Portfolio Management(LPM)** — Epic -> Feature -> Story -> Task, **WSJF(Weighted Shortest Job First)** 우선순위 알고리즘.
4. **FinOps 수식**: `TCO 5년 = CapEx(HW+SW+Facility) + OpEx(인건비+전력+라이선스) - 잔존가치`. 클라우드의 경우 `On-Demand vs Reserved(1~3y) vs Savings Plan`의 트레이드오프, **사용률(Utilization)**과 **Reserved Coverage Ratio** 최적화.
5. **전략 정합성 측정 지표**: Luftman의 **SAM 성숙도 6개 차원**(Communication·Competency·Governance·Partnership·Scope·Skills) 평균 점수(0~5)로 정량화.

- **📢 섹션 요약 비유**: 5대 축은 **오케스트라의 5악기단**(전략=작곡가, 포트폴리오=지휘자, 성과=청중 평가, 리스크=보험 설계자, 운영=무대 스태프)이며, **거버넌스 프레임워크**는 이들이 같은 악보를 연주하도록 만드는 **지휘자(Conductor)의 악보**이다.

---

## Ⅲ. 비교 및 연결

### 1. 주요 거버넌스·경영 프레임워크 비교

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 38500** | **CMMI v2.0** | **Balanced Scorecard** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스·관리 체계 | IT 서비스 관리(Service Management) | IT 의사결정 거버넌스 원칙 | 프로세스/조직 성숙도 | 전략적 성과 관리 |
| **대상** | CIO·이사회·IT 감사 | IT 운영·서비스 데스크 | 이사회·경영진 | 개발·운영 조직 | 전사(임원·현업) |
| **구조** | 40 Governance & Mgmt Objectives, 7 Component | 34 Practices, SVS | 6 Principles(책임·전략·수행·규율·투명성·적합성) | 5-Level Maturity + View-by-View | 4관점(Financial·Customer·Internal·L&G) |
| **강점** | 거버넌스 의사결정·컴플라이언스·감사 | 서비스 가치·실무 운영·Agile 통합 | 원칙 기반·법적 책임·국제 표준 | 정량적 성숙도·벤치마킹 | 전략 cascade·정합성 |
| **약점** | 구현 복잡도·도구 의존성 | 거버넌스 약함·도구 다양 | 추상적 원칙·세부 절차 부재 | IT 외 영역 약함 | KPI 설계 난이도·과잉 지표 |
| **적합 조직** | 대기업·금융·공공·규제 산업 | 서비스 중심 기업·통신·공공 | 모든 조직(거버넌스 기본) | SW 공장·SI·품질 중심 | 전략 정렬이 핵심인 조직 |

### 2. 다른 영역과의 연결

- **연결 ① (기술사 581번·정보시스템 구축)**: IT 전략 기획 -> 정보시스템 전략 계획(ISSP) -> 시스템 분석·설계 -> 구축·운영의 **SDLC Value Chain** 연결. Waterfall -> Agile -> DevOps -> Platform Engineering으로 진화.
- **연결 ② (기술사 591번 내 데이터 거버넌스)**: **DAMA-DMBOK 2.0**(Data Management Body of Knowledge) 11개 지식 영역을 IT 거버넌스의 P3·P5에 통합. **데이터 카탈로그·메타데이터 관리·Data Quality Score**가 BSC의 Internal Process KPI로 활용.
- **연결 ③ (보안·컴플라이언스)**: **Zero Trust Architecture(NIST SP 800-207)** + **SASE**(Secure Access Service Edge) + **XDR** -> IT 리스크 관리 P4와 직결. **컴플라이언스 자동화(RegTech)**로 GRC(Governance·Risk·Compliance) 툴 통합(예: Archer·ServiceNow GRC).
- **연결 ④
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 591 / 800

<- **이전**: [590. IT 경영 관리 핵심 토픽 590번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/590_it_management_core_topic_590_exam_summary/)
**다음**: [592. IT 경영 관리 핵심 토픽 592번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/592_it_management_core_topic_592_exam_summary/) ->

---
