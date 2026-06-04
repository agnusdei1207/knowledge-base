---
title: "547. IT 경영 관리 핵심 토픽 547번 시험 요약 (IT Management Core Topic 547 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 **COBIT 2019(거버넌스/관리 목표 40개), ISO 38500 6원칙, ITIL 4(SVC 34개), ISO/IEC 20000, ISO 27001, PMBOK 7, BSC 4관점**을 통합하여 **IT-비즈니스 가치 정렬(Value Alignment)**과 **엔터프라이즈 위험 통제(ERM+GRC)**를 동시에 달성하는 **3-Layer 거버넌스(전략-전술-운영)** 체계이다.
> 2. **가치**: 성숙도 Level 3 도달 시 **IT 예산 대비 ROI 23~38% 개선**(Gartner 2023), **인시던트 MTTR 62% 단축**, **컴플라이언스 감사 비용 45% 절감**, **프로젝트 성공률(스코프/일정/예산 동시 충족) 71%->89% 상승** 등 정량적 효과와 의사결정 투명성·이해관계자 신뢰의 정성적 가치를 동시에 제공한다.
> 3. **판단 포인트**: **Top-Down 표준 기반(COBIT/ISO) vs Bottom-Up 실무 중심(ITIL/DevOps)** 의 균형, **Centralized(CoE 집중) vs Federated(사업부 자율) vs Hybrid(Hub-and-Spoke) 거버넌스 모델** 선택, **자동화 범위(CMM Level 2->5)** 및 **KPI 측정 단위(Leading vs Lagging, Outcome vs Output)**의 설계가 핵심 트레이드오프이다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX)이 가속화되면서 IT는 단순 비용 센터(Cost Center)에서 **전략적 비즈니스 모션스트레이트(Strategic Business Enabler)**로 변모했다. 그러나 한국 정보시스템감리원의 통계에 따르면 전체 정보화 사업의 약 **34.7%가 실패 또는 부분 실패**(예산 초과, 일정 지연, 성과 미달)하며, 이 중 **62%는 거버넌스 부재 및 이해관계자 정렬 실패**가 근본 원인이다. IT 경영관리는 이러한 실패를 막기 위해 **전략-전술-운영**을 연결하는 통합 통제 체계를 요구한다.

기존의 **"프로젝트 단위 관리(Project-centric)"** 접근은 다음과 같은 한계를 가진다:

- **사일로(Silo) 문제**: 기획부(BA), 개발부(Dev), 운영부(Ops), 보안부(Sec), 감사부(Audit)가 **분절된 KPI**로 작동하여 **데이터 중복**, **통제 공백(Control Gap)**, **책임 전가(FMEA의 RPN 상승)** 야기
- **측정 부재**: IT 성과가 **"시스템 가동률 99.9%"** 같은 Output 지표에만 머물러 비즈니스 **Outcome**(매출 증가, 고객 이탈률 감소, 신시장 진입 시간)과 **Impact**(사회적 가치) 미연결
- **규제 대응의 사후성**: GDPR, 개인정보보호법, ESG 공시, DORA(금융), AI Basic Act(EU AI Act) 등 **컴플라이언스 요구사항 폭증**에 사후 대응 -> **Compounding Penalty**(반복 위반 시 가중처벌)

이에 **COBIT 2019 + ISO 38500 + ITIL 4 + ISO/IEC 20000 + ISO 27001**을 통합한 **3-Layer Governance 체계**가 필수적이다. 이는 **"왜(Why)=거버넌스, 무엇을(What)=관리, 어떻게(How)=운영"**의 3단 계층을 명확히 분리하여 **RACI(Responsible, Accountable, Consulted, Informed)** 책임 구조를 수립하고, **PDCA + Closed-Loop**로 지속 개선을 보장한다.

```text
        +-----------------------------------------------------+
        |  Tier 1: Strategic Governance (이사회 / IT전략위원회) |
        |  +- ISO 38500 6 Principles (책임, 전략, 획득, 성과,  |
        |  |  적합, 인적요소)                                   |
        |  +- COBIT 2019 EDM(5) - Evaluate, Direct, Monitor    |
        |  +- Portfolio Mgmt + Investment Mgmt                 |
        +--------------------+--------------------------------+
                             | 연계 (Strategy Map / Cascading KPI)
        +--------------------v--------------------------------+
        |  Tier 2: Tactical Management (CIO / IT-GRC Office)   |
        |  +- COBIT 2019 40 Governance/Management Objectives   |
        |  |   (EDM5 + APO14 + BAI11 + DSS06 + MEA04)         |
        |  +- Risk Mgmt(ISO 31000) + Compliance Mgmt          |
        |  +- Performance Mgmt: BSC 4 Perspective              |
        |  |  (Financial/Customer/Internal/Learning)          |
        |  +- EA Framework: TOGAF ADM(8 Phase) / FEA / DoDAF  |
        +--------------------+--------------------------------+
                             | 연계 (SLA / OLA / UC)
        +--------------------v--------------------------------+
        |  Tier 3: Operational Service Delivery (Service Desk) |
        |  +- ITIL 4: SVS(34 Practices) + 4 Dimensions         |
        |  |  (Org/People/InfoSys/Partners/Value Streams)      |
        |  +- ISO/IEC 20000 (Service Mgmt System)              |
        |  +- ISO 27001 ISMS + 27002 (114 Controls)           |
        |  +- DevOps + SRE + AIOps (자동화·관측가능성)         |
        |  +- PMBOK 7 (8 Performance Domains) / PRINCE2       |
        +-----------------------------------------------------+
                    <-> 양방향 피드백 (KPI / KRI / KCI 대시보드)
```

- **📢 섹션 요약 비유**: IT 경영관리는 **"건물의 내진설계 + 소방시설 + 에너지관리시스템"**의 통합이다. 내진설계(거버넌스)만 강해도 안 되고, 소방시설(ISMS)만 잘 갖춰도 정전(인시던트)에는 무력하다. **3개 시스템이 BIM(통합 모델)으로 연결**되어야 진정한 "스마트 빌딩"이 되듯, COBIT·ITIL·ISO 27001이 **단일 거버넌스 OS** 위에서 동작해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### (1) 3-Layer 거버넌스 아키텍처의 구성 요소

| 계층 | 핵심 프레임워크 | 의사결정 주체 | 주요 산출물 | KPI 종류 |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: 전략(Governance)** | ISO 38500, COBIT 2019 EDM | 이사회, IT전략위원회 | IT 전략 맵, 거버넌스 헌장, 투자 포트폴리오 | ROIC, NPV, IRR, TCO |
| **Tier 2: 전술(Management)** | COBIT 2019(40 목표), TOGAF, ISO 31000, BSC | CIO, IT-GRC Office, EA팀 | EA BluePrint, GRC 대시보드, 정책/표준, 리스크 등록부 | KPI(Outcome), KRI(위험), KCI(통제) |
| **Tier 3: 운영(Operational)** | ITIL 4(34 Practice), ISO/IEC 20000, ISO 27001, PMBOK 7 | 서비스 데스크, DevOps팀, SOC, PMO | SLA, 변경관리 기록, 인시던트 로그, 보안 로그, 성과 보고서 | MTTR, MTBF, SLA 준수율, 결함밀도, 배포 빈도 |

### (2) COBIT 2019 핵심 메커니즘 (단계별 동작)

```text
   입력(Inputs)                    COBIT 2019 Cascade                  출력(Outputs)
   ----------                       --------------                      ----------
   +-------------+  +------------------------------------+  +--------------------+
   | Stakeholder |  | 1. Enterprise Strategy -> Goals    |  +------------------+|
   | Needs (VOI) |--->|    (13 Generic Goals -> Cascade)    |--->| IT-Related Goals ||
   +-------------+  | 2. Goals -> Processes (40 Obj.)     |  | (13 Goals)       ||
   +-------------+  |    EDM(5) APO(14) BAI(11)         |  +------+-----------+|
   | Risk Profile|--->|    DSS(6) MEA(4)                   |         |              |
   +-------------+  | 3. Processes -> Risk/Ctrl Objective |  +------v-----------+|
   +-------------+  |    (Inherent/Residual Risk)        |  | Cascading KPIs   ||
   | Compliance  |--->| 4. Risk -> Mgmt Practice            |--->| (Lead/Lag)       ||
   | Req.(PIPL,  |  |    (Capability Level 0~5)           |  +------+-----------+|
   | GDPR)       |  +------------------------------------+         |              |
   +-------------+                                                 v              |
                                                          +------------------+   |
                                                          | Stakeholder Value|   |
                                                          | (Realized Value) |   |
                                                          +------------------+   |
                                                                                  |
   5 Focus Areas × 7 Components × 40 Objectives = 약 1,400 통제 항목               |
```

### (3) ITIL 4 Service Value System (SVS)

- **Opportunity/Demand -> Value**: **34개 Practice**(중심 7: Incident, Problem, Change Enablement, Service Desk, Service Request, Service Level, Monitoring & Event Management; **기술 5**: Deployment, Infra/Platform Mgmt, Software Dev, Service Validation/Test; **일반 14**: Architecture, Continual Improvement, Information Security, Risk, Supplier, Workforce/Talent Mgmt 등)
- **4 Dimensions of Service Management**:
  1. **Organizations & People**: 문화, 구조, 역량
  2. **Information & Technology**: 데이터·AI·자동화
  3. **Partners & Suppliers**: SaaS, MSP, 클라우드 계약 거버넌스
  4. **Value Streams & Processes**: E2E 흐름(예: Idea -> Code -> Deploy -> Operate)
- **Guiding Principles(7)**: Focus on Value, Start Where You Are, Progress Iteratively, Collaborate, Think & Work Holistically, Keep It Simple, Optimize & Automate

### (4) 주요 KPI/KRI/KCI 계산식

| 지표 | 수식 | 임계치/목표 | 의미 |
| :--- | :--- | :--- | :--- |
| **ROI** | (Net Benefit / Cost) × 100 | ≥ 15% | IT 투자 회수율 |
| **NPV** | Σ(CFₜ / (1+r)ᵗ) − Initial Cost | ≥ 0 | 순현재가치 |
| **Schedule Variance (SV)** | EV − PV (Earned Value) | ≥ 0 | 일정 진척 |
| **Cost Variance (CV)** | EV − AC | ≥ 0 | 비용 효율 |
| **SPI** | EV / PV | ≥ 1.0 | 일정 성과지수 |
| **CPI** | EV / AC | ≥ 1.0 | 비용 성과지수 |
| **MTTR** | Σ(복구시간) / 인시던트 수 | ≤ 1h (Critical) | 평균 복구 시간 |
| **MTBF** | Σ(가용시간) / 장애 횟수 | ≥ 720h | 평균 고장 간격 |
| **Change Failure Rate** | (실패 변경 / 전체 변경) × 100 | ≤ 15% (DORA Elite) | 변경 품질 |
| **SLA Compliance** | (SLA 충족 건 / 전체) × 100 | ≥ 99.9% | 서비스 수준 |
| **Risk Score** | Impact(1~5) × Likelihood(1~5) | High ≥ 15 | 리스크 우선순위 |
| **Control Coverage** | (적용 통제 / 필요 통제) × 100 | ≥ 95% | 통제 적용률 |

- **📢 섹션 요약 비유**: 3-Layer 거버넌스는 **"도시의 행정 체계"**와 같다. **시議会(Tier 1)**가 도시 기본계획과 조례를 제정하고, **구청(Tier 2)**이 실행 계획과 예산 배분을 관리하며, **동 주민센터·소방서·경찰서(Tier 3)**가 민원·소방·치안을 실서비스로 제공한다. **CCTV 통합관제센터(GRC 대시보드)**가 3계층을 실시간으로 연결해야
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 547 / 800

<- **이전**: [546. IT 경영 관리 핵심 토픽 546번 시험 요약](/studynote/12_it_management/05_security_compliance/546_it_management_core_topic_546_exam_summary/)
**다음**: [548. IT 경영 관리 핵심 토픽 548번 시험 요약](/studynote/12_it_management/05_security_compliance/548_it_management_core_topic_548_exam_summary/) ->

---
