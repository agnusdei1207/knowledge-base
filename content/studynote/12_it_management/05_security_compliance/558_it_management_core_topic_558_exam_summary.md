---
title: "IT Management Core Topic 558 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리(Information Technology Management)는 COBIT 2019, ISO/IEC 38500, ITIL 4, CMMI, TOGAF, ISO 27001 등 글로벌 거버넌스 프레임워크를 기반으로, **전략-거버넌스-운영-컴플라이언스-혁신**의 5계층을 통합 관리하여 기업의 디지털 가치사슬(Value Chain)을 최적화하는 경영학문 분야임
> 2. **가치**: McKinsey Digital 연구에 따르면 잘 확립된 IT 거버넌스 체계를 보유한 기업은 EBITDA 마진이 평균 **20~25%** 높고, 디지털 전환(DX) 성공률이 **35% -> 70%**로 2배 이상 상승하며, IT 투자 ROI는 **3.3배**까지 개선됨(전통적 IT 운영 대비)
> 3. **판단 포인트**: 핵심 의사결정 트레이드오프로는 ① **Centralization(집중) vs. Federation(연합)** 거버넌스 모델, ② **Build(자체개발) vs. Buy(패키지) vs. Borrow(클라우드)**, ③ **Stable Core(안정 코어) vs. Agile Edge(민첩 에지)** 이원화 전략, ④ **Bimodal IT** 적용 범위, ⑤ **Zero Trust vs. Defense in Depth** 보안 아키텍처 선택이 있으며, **EA(Enterprise Architecture) 기반의 정합성**과 **BSC(Balanced Scorecard) 기반의 성과 측정**이 판단의 핵심 기준임

---

## Ⅰ. 개요 및 필요성

### 1.1 정의 및 배경

IT 경영관리(IT Management)는 단순한 IT 운영을 넘어 **경영 전략과 IT의 정렬(Strategic Alignment)**을 통해 조직의 디지털 경쟁력을 극대화하는 통합 관리 체계임. 2000년대 이후 클라우드 컴퓨팅, 빅데이터, AI/ML, IoT, 5G/6G, Web3, 생성형 AI(GenAI) 등 **파괴적 기술(Disruptive Technology)**이 등장하면서, IT는 비용센터(Cost Center)에서 **전략적 비즈니스 인에이블러(Strategic Business Enabler)**로 역할이 변화함.

Gartner(2023) 보고서에 따르면, **CEO의 89%가 "기업 성장을 위해 새로운 디지털 비즈니스 모델 채택이 필수"**라고 답했으나, 동시에 **기업의 70%가 DX(Digital Transformation) 프로젝트에서 예상 ROI를 달성하지 못하고 실패**하는 것으로 나타남. 이는 **IT 거버넌스 부재, 사일로(Silo) 조직 문화, 변화관리(Change Management) 실패, 보안 사고**가 주된 원인임.

### 1.2 과거 vs 새로운 패러다임 비교

| 시대 | IT 역할 | 거버넌스 방식 | KPI | 조직 구조 |
|------|--------|---------------|-----|----------|
| 1980~90년대 (전통) | 비용센터(Back-office) | 중앙집중형 통제, IT 관료주의 | 비용 절감, 가용성(Uptime) | 계층형(Functional) |
| 2000년대 (프로세스) | 업무 자동화(BPM) | ITIL v2/v3 기반 ITSM, SLAs | 서비스 가용성, 인시던트 MTTR | 공유서비스(Shared Services) |
| 2010년대 (클라우드) | 디지털 트랜스포메이션 | COBIT 5, DevOps, Agile | Time-to-Market, TCO | 이원화 IT(Bimodal IT) |
| 2020년대 (AI/플랫폼) | 비즈니스 인에이블러 | COBIT 2019, 플랫폼 거버넌스, MLOps | 비즈니스 임팩트, NPS, AI 거버넌스 | 제품/플랫폼 팀(Team Topologies) |
| 2025+ (자율운영) | 자율 시스템(Autonomic) | AI 거버넌스, Ethical AI, AIOps | 자가치유율, 지속가능성(ESG), 신뢰도 | 셀(Cell) 기반 자율 조직 |

### 1.3 ASCII 아키텍처: IT 경영관리 5계층 통합 프레임워크

```text
        +----------------------------------------------------------+
        |     [Layer 5] 디지털 혁신 & 미래 비즈니스 모델          |
        |  - DX 전략, 생성형 AI 활용, 플랫폼 비즈니스, Web3       |
        |  - KPI: 신규 매출 비중, Time-to-Value, ESG 점수        |
        +-------------------------+--------------------------------+
                                  | Strategic Alignment (IT-Business)
        +-------------------------v--------------------------------+
        |     [Layer 4] IT 거버넌스 & 컴플라이언스 (Governance)    |
        |  - COBIT 2019, ISO 38500, ISO 27001, NIST CSF,        |
        |    개인정보보호법, ESG, EU AI Act, AI 거버넌스          |
        |  - RACI 매트릭스, Risk Appetite, 정책/표준/지침         |
        +-------------------------+--------------------------------+
                                  | Portfolio & Architecture
        +-------------------------v--------------------------------+
        |  [Layer 3] EA & 프로젝트 포트폴리오 관리 (Plan & Build)  |
        |  - TOGAF 10 ADM, ArchiMate 3.2, Zachman, FEAF          |
        |  - P3O, MSP, PMO, SAFe/Spotify/LeSS (Agile 스케일링)   |
        |  - BPA, Cloud Center of Excellence (CCoE)               |
        +-------------------------+--------------------------------+
                                  | Service Delivery
        +-------------------------v--------------------------------+
        |  [Layer 2] IT 서비스 운영 & 데일리 매니지먼트 (Run)      |
        |  - ITIL 4 Service Value System, AIOps, SRE,             |
        |    FinOps, Observability (OpenTelemetry), ITSM 도구     |
        |  - SLA/OLA/UC, 인시던트/문제/변경/릴리스 관리            |
        +-------------------------+--------------------------------+
                                  | Infrastructure & Data
        +-------------------------v--------------------------------+
        |  [Layer 1] 기술 인프라 & 데이터 플랫폼 (Foundation)     |
        |  - Multi/Hybrid Cloud (AWS/Azure/GCP/NAVER Cloud)       |
        |  - Kubernetes, Service Mesh, Data Lakehouse,            |
        |    Kafka, Zero Trust Network, SASE/SSE                  |
        +----------------------------------------------------------+

   [Cross-cutting Concerns]
   +- 사이버보안 (Security)     +- 데이터 거버넌스 (Data Quality)
   +- 리스크 관리 (Risk)        +- 지속가능성 (Green IT/ESG)
   +- 변화 관리 (Change Mgmt)   +- 인재/문화 (People & Culture)
```

### 1.4 왜 IT 경영관리가 필수적인가?

- **규제 환경의 강화**: GDPR(연간 매출의 4%까지 과징금), 개인정보보호법, EU AI Act, 클라우드보안인증(CSAP), ISMS-P, ESG 공시 의무화
- **공급망 복잡화**: 멀티클라우드, SaaS 200개+ 사용(SaaS Sprawl), Shadow IT, 4th Party Risk 증가
- **사이버 위협의 고도화**: 랜섬웨어, APT, 공급망 공격(SolarWinds, Log4j, MOVEit, XZ Utils 사례), 생성형 AI 기반 피싱
- **임시·비정기 프로젝트 폭증**: 78%가 "DX로 인한 프로젝트 수 증가"를 호소(McKinsey 2023)
- **핵심 인재 확보 경쟁**: AI/ML/Cloud 엔지니어 부족, IT-Business 융합 인력 희소성

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **항공우주국의 통합 미션 컨트롤(NASA Mission Control)**과 같음. 수백 명의 엔지니어, 위성, 로켓, 지상국, 과학자를 **단일 콘솔(Governance)**에서 **궤도(전략)**, **비행(운영)**, **안전(보안)**, **통신(데이터)**으로 통합 조정하지 않으면 임무는 실패함.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 IT 거버넌스 3대 프레임워크 상세 비교

#### 2.1.1 COBIT 2019 (Control Objectives for Information and Related Technologies)

ISACA에서 발표(2018/2019)한 **엔터프라이즈 IT 거버넌스 및 관리의 글로벌 표준**으로, 5개 원칙(Principles) 기반으로 설계됨:

1. **Needs(Needs of Stakeholders)** - 이해관계자 니즈를 비즈니스 목표와 정렬
2. **End-to-End(End-to-End)** - 엔드투엔드 거버넌스 시스템
3. **Single Integrated(Apply a Single Integrated Framework)** - 단일 통합 프레임워크
4. **Enabling(Holistic Approach)** - 전체론적 접근
5. **Separation(Distinguish Governance from Management)** - 거버넌스와 관리의 분리

**40개의 관리 목표(Management Objectives)**가 5개 도메인(EDM: Evaluate/Direct/Monitor + APO/BAI/DSS/MEA) 하에 구성되며, **설계 계수(Design Factors)** 11개를 통해 조직별 맞춤 거버넌스 시스템 구축 가능.

#### 2.1.2 ITIL 4 (Information Technology Infrastructure Library)

AXELOS(현재 PeopleCert)에서 2019년 발표, **2019년 ISO 20000:2018과 정렬**됨. 핵심은 **Service Value System(SVS)**:

- **Service Value Chain(SVC)**: Plan -> Engage -> Design & Transition -> Obtain/Build -> Deliver & Support
- **7 Guiding Principles**: Focus on value, Start where you are, Progress iteratively, Collaborate, Think holistically, Keep it simple, Optimize
- **34 Practices**(신규): Service Desk, Incident/Problem/Change Enablement, Service Level, Continual Improvement, Service Request, Monitoring & Event, Release, Deployment, Infrastructure/Platform/Software/Availability/Capacity/Continuity/Security Management 등
- **4 Dimensions of Service Management**: Organizations & People, Information & Technology, Partners & Suppliers, Value Streams & Processes

#### 2.1.3 ISO/IEC 38500:2015 (Corporate governance of IT)

**6원칙(Principles)**: Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior
**5단계 거버넌스 모델(Evaluate-Direct-Monitor)**: Gartner의 EIAM(직무 기반)과 유사

### 2.2 ASCII 다이어그램: COBIT 2019 거버넌스 시스템 구조

```text
         +---------------------------------------------+
         |      이해관계자 니즈 & Concerns              |
         |   (Shareholders, Customers, Regulators,     |
         |    Employees, Partners, Society)            |
         +----------------------+----------------------+
                                | Translate
         +----------------------v----------------------+
         |       기업 목표 (Enterprise Goals)          |
         |  EG01: 포트폴리오 경쟁력 강화                |
         |  EG05: 고객 중심 서비스 제공                 |
         |  EG12: 디지털 트랜스포메이션 관리             |
         |  EG13: 정보 보안 & 프라이버시                |
         +----------------------+----------------------+
                                | Cascade + Align
         +----------------------v----------------------+
         |       조정 목표 (Alignment Goals)            |
         |  AG01: IT 준법성 & 지원                     |
         |  AG04: 기술 혁신 & 트렌드                   |
         |  AG06: Agile & DevOps 전환                  |
         |  AG15: 정보 보안 인시던트 대응              |
         +----------------------+----------------------+
                                | Map (COBIT 2019: 40 MOs)
         +----------------------v----------------------+
         |   거버넌스 & 관리목표 (Gov/Management Obj.) |
         |  EDM01~05  |  APO01~14  |  BAI01~11        |
         |  DSS01~06  |  MEA01~04                       |
         +----------------------+----------------------+
                                | Components of GRC
         +----------------------v----------------------+
         | Process / Organizational Structures / Info  |
         | People/Skills/Competencies / Policies/Std    |
         | Culture/Ethics/Behavior / Services/Infr/Apps |
         |        [목표 계단식 - Cascade]                |
         +---------------------------------------------+
         ※ 11개 설계 계수(Design Factors)가 위 모든 단계를 조직별로 맞춤화함
         ※ Example: D1 Enterprise Strategy, D3 Risk Profile,
           D6 Industry Compliance, D9 Enterprise Size...
```

### 2.3 IT 전략 정렬 모델: Henderson & Venkatraman (1993) SAM

| 구분 | Business | IT |
|------|----------|-----|
| **External** | ① Industry/SCOPE | ③ IT-SCOPE (시스템, 표준) |
| **Internal** | ② Business Strategy (Porter 등) | ④ IT Strategy (인프라, 인력) |
| **Execution** | Business Implementation | IT Implementation |
| **거버넌스** | <--> Strategic Fit (전략적 정합) & Functional Integration (기능적 통합) <--> | |

**SAM 활용 단계**:
1. Business Strategy & IT Strategy 동시 분석
2. Strategic Fit 검증 (4사분면 정합)
3. **Strategic Alignment Maturity (SAMm)**: 5단계(L1 초기 -> L2 계획 -> L3 통합 -> L4 전략적 -> L5 최적화)

### 2.4 Enterprise Architecture (EA) - TOGAF 10

The Open Group Architecture Framework(TOGAF) 10(2022)은 **ADM(Architecture Development Method)**을 통해 8단계 사이클로 EA를 수립:

| Phase | 명칭 | 핵심 산출물 |
|------|------|-----------|
| **Preliminary** | Framework & Principles | 조직 원칙 21개, 거버넌스 프레임워크 |
| **A: Architecture Vision** | 비전 정의 | Statement of Architecture Work |
| **B: Business Architecture** | 비즈니스 구조 | Capability Map, Value Stream |
| **C: Information Systems** | 데이터/앱 | Logical Data Model, App Portfolio |
| **D: Technology** | 기술 인프라 | Infra Diagram, Platform Map |
| **E: Opportunities & Solutions** | 이행 계획 | Project/Portfolio Roadmap |
| **F: Migration Planning** | 이행 로드맵 | Transition Architecture (T-0 -> T-N) |
| **G: Implementation Governance** | 이행 거버넌스 | Architecture Contract |
| **H: Architecture Change Mgmt** | 변경 관리 | Change Request 절차 |
| **Requirements Mgmt** | 요구사항 | Requirements Repository |

**ArchiMate 3.2**(2022): EA 표기 표준언어. **Application/Data/Business/Technology/Motivation/Strategy/Implementation/Physical/Compound** 등 9개 레이어의 시각화

### 2.5 IT 서비스 운영 메커니즘 (ITIL 4 SVC 상세)

```text
        +--------------+  Engage  +------------------+
        |    Plan      |◄--------►|    Engage        |
        +------+-------+          +--------+---------+
               |                            |
               v                            v
        +--------------+
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 558 / 800

<- **이전**: [557. IT 경영 관리 핵심 토픽 557번 시험 요약](/studynote/12_it_management/05_security_compliance/557_it_management_core_topic_557_exam_summary/)
**다음**: [559. IT 경영 관리 핵심 토픽 559번 시험 요약](/studynote/12_it_management/05_security_compliance/559_it_management_core_topic_559_exam_summary/) ->

---
