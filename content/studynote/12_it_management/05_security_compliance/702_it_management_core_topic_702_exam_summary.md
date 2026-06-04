+++
title = "702. IT 경영 관리 핵심 토픽 702번 시험 요약 (IT Management Core Topic 702 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# 702. IT 경영 관리 핵심 토픽 702번 시험 요약 (IT Management Core Topic 702 Exam Summary)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(COBIT 2019, ISO 38500)와 IT 서비스 관리(ITIL 4), 프로젝트 관리(PMBOK 7th/Agile), 위험 관리(ISO 31000)를 통합적으로 운용하여, 기업의 전략 목표와 IT 성과·리스크·자원(Financial Management for IT Services)을 정렬(Alignment)·실현(Value Delivery)하는 경영 프레임워크 체계.
> 2. **가치**: MOF(Service Operation/Transition/Strategy 단계)와 Balanced ScoreCard 4관점(재무·고객·내부·학습성장) 기반 KPI 운영 시 IT 투자 대비 ROI 평균 25~40% 개선, 서비스 가용성 99.95% 이상 달성, ISO/IEC 20000·ISMS 인증으로 컴플라이언스 위반 비용 60% 절감이 가능한 정량적 효과.
> 3. **판단 포인트**: 중앙집중(CoE: Center of Excellence) vs 분산(Federated) 거버넌스 구조 선택, CMMI Level 1~5 vs Agile@Scale(SAFe/Spotify Model) vs DevOps(DORA 4 Metrics) 트레이드오프, Capex(전통 인프라) vs Opex(Cloud FinOps) 예산 배분 및 Build vs Buy vs SaaS 의사결정 시점의 TCO 3~5년 분석이 핵심 결정 변수.

---

## Ⅰ. 개요 및 필요성

정보화 시대(1970s~1990s)의 EDP(Electronic Data Processing) 중심 관리는 2000년대 이후 ERP/CRM/SCM의 등장과 함께 **IT 거버넌스(Governance)** 개념으로 진화하였으며, 2010년대의 클라우드·모바일·빅데이터, 2020년대의 생성형 AI·양자컴퓨팅·Web3 환경에서는 **디지털 거버넌스(Digital Governance)** 및 **지속가능 IT(Green IT, ESG-IT)** 로 패러다임이 재편되고 있습니다. 전통적 IT 부서는 '비용 센터(Cost Center)'에서 '전략적 파트너(Value Center)' 그리고 '디지털 비즈니스 플랫폼 운영자(Platform Operator)'로 역할이 전환되었으며, 이에 따라 단순한 시스템 운영을 넘어 IT 성과 측정, 위험 통제, 투자 의사결정, 그리고 비즈니스 가치 실현을 통합 관리할 수 있는 **체계적 경영 프레임워크**가 필수 불가결해졌습니다.

특히 ISO/IEC 38500(2015 개정)이 "Evaluate-Direct-Monitor" 3단계 거버넌스 원칙을 천명하면서 IT 의사결정의 책임 소재, 의사결정 구조(Board → Executive → Management → Operational의 4계층 RACI 모델), 그리고 성과 보고 체계의 표준화 요구가 법·제도적으로 강제되었고, EU DORA(Digital Operational Resilience Act, 2023), 한국 전자금융거래법, 클라우드 컴퓨팅 발전 및 이용자 보호에 관한 법률(클라우드 이용자 보호법) 등으로 컴플라이언스 요건이 폭증하고 있습니다. 이에 본 토픽은 ①IT 거버넌스 프레임워크, ②IT 서비스 관리, ③프로젝트·프로그램·포트폴리오 관리(P3O/PMO), ④리스크·컴플라이언스, ⑤디지털 전환 전략의 5대 영역을 통합적으로 다룹니다.

```text
[ IT 경영 관리 통합 프레임워크 아키텍처 ]

    ┌──────────────────────────────────────────────────────────┐
    │          이사회(Board) / 전략 거버넌스 위원회             │
    │   ┌──────────────┬──────────────┬───────────────────┐    │
    │   │  IT 전략     │  리스크       │  컴플라이언스     │    │
    │   │  위원회      │  위원회       │  위원회           │    │
    │   └──────┬───────┴──────┬───────┴──────┬────────────┘    │
    │          │              │              │                  │
    │   ───────▼──────────────▼──────────────▼──── Evaluate/Direct/Monitor
    │          │              │              │       (ISO 38500)
    │   ┌──────▼──────────────▼──────────────▼────────────┐
    │   │  CIO / CDO / CISO / CPO 통합 의사결정층         │
    │   │  (전략 정렬: Strategy-Organization-Technology)  │
    │   └──────┬──────────────┬──────────────┬────────────┘
    │          │              │              │
    │   ┌──────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
    │   │ 서비스     │  │ 프로젝트  │  │ 운영·인프라│
    │   │ 운영       │  │ 관리      │  │ 운영       │
    │   │ (ITIL 4)   │  │ (PMBOK 7) │  │ (ITSM)    │
    │   │ SLA: 99.95%│  │ SPI/CPI  │  │ MTTR<30m  │
    │   └──────┬─────┘  └─────┬─────┘  └─────┬─────┘
    │          │              │              │
    │   ───────▼──────────────▼──────────────▼────
    │   ┌──────────────────────────────────────────┐
    │   │  전사적 측정 체계 (Metrics & Reporting)  │
    │   │  • COBIT 2019 Goals Cascade (13 Goals)  │
    │   │  • BSC 4관점 + GRC 대시보드              │
    │   │  • DORA 4 Metrics (DevOps 성능)          │
    │   │  • FinOps 비용 최적화 KPI               │
    │   └──────────────────────────────────────────┘
    └──────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **대형 항공모함의 함교(CIC, Combat Information Center)** 와 같습니다. 항공모함의 함교는 레이더·통신·무장·비행 갑판 운용 등 수십 개 부서의 정보를 통합·분석·판단하여 항공모함 전체의 임무 성공을 좌우합니다. 이사회가 함교라면, COBIT은 **표준 운용 매뉴얼(SOP)**, ITIL은 **일일 비행 스케줄 관리**, PMBOK은 **출격 임무 계획서**, ISO 31000은 **위험 회피 매트릭스**에 해당합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) IT 거버넌스 프레임워크 (COBIT 2019 + ISO 38500)

COBIT 2019는 5개의 도메인(EDM: Evaluate-Direct-Monitor / APO: Align-Plan-Organize / BAI: Build-Acquire-Implement / DSS: Deliver-Service-Support / MEA: Monitor-Evaluate-Assess) 위에 **40개의 관리 목표(Management Objectives)** 와 **이해관계자 니즈 → 목표 연쇄(Goals Cascade) 메커니즘**을 두어, 기업 목표(13개 Enterprise Goals)와 IT 관련 목표(13개 Alignment Goals) 그리고 40개 프로세스 목표를 3단계로 매핑합니다. 핵심은 **"Design Factor"(조직의 거버넌스 시스템을 결정하는 11가지 변수: Enterprise Strategy, Goals, Risk Profile, I&T-Related Issues, Threat Landscape, etc.)** 와 **"Focus Area"(Privacy, Cybersecurity, DevOps, Digital Transformation 등)"** 를 통한 맞춤형 거버넌스 시스템 설계입니다.

ISO/IEC 38500:2015는 **6개의 거버넌 원칙**(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)을 제시하며, 이사회가 "Evaluate(평가) → Direct(지시) → Monitor(모니터)" 사이클을 통해 IT 활용을 감독해야 함을 규정합니다. 한국에서는 전자정부법, 정보통신망법, 개인정보보호법, 그리고 2024년 시행된 인공지능 기본법(AI Basic Act)에 의해 실질적 의무가 부여됩니다.

### 2) ITIL 4 서비스 가치 시스템 (SVS: Service Value System)

ITIL 4(2019)는 기존의 26개 프로세스(v3) → **34개의 관리 실무(Practices)** 체계로 단순화되었으며, **Service Value Chain(SVC)** 의 6개 활동(Plan/Improve/Engage/Design & Transition/Obtain & Build/Deliver & Support)을 통해 Opportunity/Demand → Value로 전환합니다. 핵심 구성요소는 **Guiding Principles(7개)**, **Four Dimensions of Service Management(Organizations & People / Information & Technology / Partners & Suppliers / Value Streams & Processes)**, **Continual Improvement Model(DPI: Define-Where to go / Where are we now / Where do we need to go / Take action / Did we get there / Hold the gains)** 입니다.

### 3) 프로젝트 관리 체계 (PMBOK 7th + Agile)

PMBOK 7th(2021)는 6th의 10개 지식영역 → **8개 Performance Domains**(Stakeholders, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty)과 **12가지 Project Management Principles** 로 전환되며, **Tailoring(맞춤형 조정)** 이라는 새로운 접근을 통해 Predictive(Waterfall), Adaptive(Agile), Hybrid 방식을 모두 포용합니다. **불확실성(Uncertainty)** 이라는 도메인이 별도로 신설되어, 위험(Risk), 모호성(Ambiguity), 복잡성(Complexity)을 다루며, **VUCA 환경** 대응 프레임워크를 제공합니다.

```text
[ IT 서비스 가치 흐름 (ITIL 4 SVC) ]

  Opportunity / Demand
           │
           ▼
   ┌───────────────┐
   │ 1. Plan       │◀──── Continual Improvement (7단계)
   │  (전략/로드맵) │      Define→Analyze→Design→Implement→
   └───────┬───────┘      Evaluate→Hold Gains→Reiterate
           │
           ▼
   ┌───────────────┐
   │ 2. Engage     │   ←─ Stakeholders (내부/외부)
   │  (관계자 참여)│
   └───────┬───────┘
           │
           ▼
   ┌───────────────┐
   │ 3. Design &   │   ←─ SLA/SLO/SLG 합의
   │   Transition  │      Change Enablement
   └───────┬───────┘
           │
           ▼
   ┌───────────────┐
   │ 4. Obtain &   │   ←─ Build vs Buy vs Cloud SaaS
   │   Build       │      거버넌스·계약·라이선스
   └───────┬───────┘
           │
           ▼
   ┌───────────────┐
   │ 5. Deliver &  │   ←─ Incident/Major Incident
   │   Support     │      Service Request/Problem Mgmt
   └───────┬───────┘
           │
           ▼
   ┌───────────────┐
   │ 6. Improve    │──→ Service Value (Outcome/Cost/Risk)
   │   (개선활동)  │    → IT 서비스 가치 실현
   └───────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** | IT 거버넌스·관리 체계의 메타 프레임워크 | 5개 도메인(EDM/APO/BAI/DSS/MEA) × 40개 관리목표; Goals Cascade(이해관계자→Enterprise 13개→IT Alignment 13개→Process 40개); Design Factor 11개 + Focus Area(Privacy, Cyber, DevOps, ESG, Risk) 기반 맞춤 거버넌스 시스템 설계 |
| **ITIL 4 SVS** | IT 서비스 라이프사이클·가치 사슬 관리 | 34개 Practices(Service Mgmt 14 / Tech Mgmt 11 / Business Mgmt 9); Service Value Chain 6활동; 4 Dimension(조직·사람/정보·기술/파트너/가치흐름); Continual Improvement DPI 모델; Value Stream 단위 최적화 |
| **PMBOK 7th** | 프로젝트·프로그램·포트폴리오 통합 관리 | 8개 Performance Domain + 12 Principles; Predictive/Agile/Hybrid Tailoring; 불확실성 도메인(Risk/Ambiguity/Complexity); 7 Tailoring Considerations(개발접근, 라이프사이클, 거버니언스, 불확실성, 복잡성, 자원, 변경관리) |
| **ISO 31000/38500** | 위험·거버넌스 국제 표준 | ISO 31000:2018 Risk Process(Comm.Consult→Scope→Risk Assessment(Identify·Analyze·Evaluate)→Treatment→Monitor→Record·Report); ISO 38500:2015 3단계(Evaluate-Direct-Monitor) + 6원칙; PDCA 통합 |
| **GRC/FinOps/DevOps** | 거버넌스 운영·자동화 영역 | GRC(Governance-Risk-Compliance) 도구(Archer, ServiceNow GRC); FinOps Foundation 6개 원칙(Teams/Visibility/Cost-aware/Optimization/Iteration/Collaboration) + Inform-Analyze-Optimize-M循环; DORA 4 Metric(Deployment Frequency/Lead Time/Change Failure Rate/MTTR) |

### 4) 핵심 메커니즘: 전략 정렬(Strategic Alignment) 모델

Henderson & Venkatraman의 **Strategic Alignment Model(SAM)** 은 4개 영역—Business Strategy, IT Strategy, Organization Infrastructure & Processes, IT Infrastructure & Processes—의 양방향(Fit) 정렬을 강조합니다. **Strategic Fit(외부: Industry → IT strategy)** 과 **Operational Integration(내부: Organization ↔ IT infra)** 의 두 축을 통해 **Execution(전략 실행)**, **Technology(기술 활용)**, **Competitive Potential(경쟁우위)**, **Service Level(서비스 수준)** 의 4관점 균형을 추구합니다. Luftman(2000~2005)의 **SAM Maturity Model** 6개 속성(Communications/Competency/Governance/Partnership/Scope/Architecture) 및 5단계(Level 1: Ad-hoc → Level 5: Optimized) 점수 산정(5점 척도, 30점 만점)으로 정렬 성숙도 측정.

### 5) 가치 측정: IT BSC(Balanced ScoreCard) & VBM(Value Based Management)

IT 투자 가치를 정량화하기 위해 Kaplan-Norton BSC를 IT에 적용한 **IT BSC 4관점**(①재무: ROI, NPV, TCO / ②고객: 만족도, SLA 준수율 / ③내부 프로세스: 변경 성공률, 장애 복구시간 MTTR / ④학습·성장: 직원 역량, 혁신 지수) 프레임워크를 활용합니다. 추가적으로 **Information Economics**(출판: Parker & Benson, 1988) 의 5가지 가치 차원(ROI / Strategic Match / Competitive Advantage / Management Information / Architectural Risk) 및 **Total Cost of Ownership(TCO)** 의 3~5년 분석(HW+SW+인력+설치+교육+운영+다운타임) 을 결합하여 의사결정합니다.

- **📢 섹션 요약 비유**: COBIT과 ITIL, PMBOK은 마치 **자동차의 브레이크(COBIT, 통제), 엔진(ITIL, 서비스), 핸들(PMBOK, 방향성)** 과 같습니다. 좋은 차는 세 가지가 정밀하게 맞물려야 하며, ISO 31000은 **도로 교통 법규(위험 회피)**, IT BSC는 **계기판(성과 측정)**, 그리고 CIO/CDO는 **운전사**에 해당합니다.

---

## Ⅲ. 비교 및 연결

### 1) 주요 거버넌스/관리 프레임워크 비교

| 구분 | **COBIT 201
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 702 / 800

← **이전**: [701. IT 경영 관리 핵심 토픽 701번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/701_it_management_core_topic_701_exam_summary/)
**다음**: [703. IT 경영 관리 핵심 토픽 703번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/703_it_management_core_topic_703_exam_summary/) →

---
