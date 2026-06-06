---
title: "IT Management Core Topic 509 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019의 Governance System(40개 관리목표·5개 도메인)와 ITIL 4의 Service Value System(34개 Practice)을 ISO 38500의 6개 원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)으로 통합하여, 기업의 IT 자산을 비즈니스 가치로 전환하는 3-Layer 거버넌스 체계(Ecosystem->Governance->Management)의 운영 모델.
> 2. **가치**: McKinsey 2023 Survey 기준 Mature IT Governance 보유 기업은 디지털 전환 성공률 2.6배(26%->68%), IT 투자 ROI 평균 4.7배, ISO 38500 인증 기업의 IT 프로젝트 실패율 38%->12% 감소, COBIT 2019 적용 시 감사 소요시간 평균 47% 단축 효과.
> 3. **판단 포인트**: 중앙집중형(CoE 기반) vs 분산형(Federated) 거버넌스 모델 선택 시 조직 규모(1,000명 임계점), 규제 강도(금융·공공), 클라우드 의존도(>40% 시 FinOps 통합 필요), 그리고 사이버 회복력(Cyber Resilience) 확보를 위한 NIST CSF 2.0과 COBIT 2019 매핑 전략이 핵심 의사결정 변수.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 509번 시험은 IT 경영 관리 영역의 통합적 문제해결 능력을 평가하며, 단일 프레임워크 암기가 아닌 **거버넌스-전략-운영-감리** 4계층의 상호작용과 정량적 의사결정 역량을 요구한다. 과거 2000년대 Silo별(Best-of-Breed) IT 운영 모델은 평균 TCO 23% 중복 투자, Shadow IT 비율 35~50%, 프로젝트 성공률 29%(Standish Group CHAOS Report 2020)를 야기했으며, 이를 극복하기 위해 **COBIT 2019**은 Governance & Management Objectives(EDM->APO->BAI->DSS->MEA) 40개로 통합되었다. 특히 2019 개정에서 추가된 **Focus Area(예: DevOps, RPA, Cybersecurity, Privacy)** 메커니즘은 디지털 전환 시대의 가변적 요구사항을 반영한다.

```text
[ IT 거버넌스 4-Layer 통합 참조 모델 ]

  +----------------------------------------------------------+
  |  Layer 1: 외부 생태계 (Ecosystem & Stakeholders)          |
  |  +--------+  +--------+  +--------+  +--------------+    |
  |  | 규제기관|  | 파트너 |  | 고객   |  | 투자자/이사회 |    |
  |  +---+----+  +---+----+  +---+----+  +------+-------+    |
  |      |           |           |              |             |
  |      +-----------+-----+-----+--------------+             |
  |                        v                                   |
  |  Layer 2: 거버넌스 (ISO 38500 6원칙 + COBIT EDM)           |
  |  +----------------------------------------------+         |
  |  | Evaluate - Direct - Monitor (EDM 5개 목표)   |         |
  |  +--------------------+-------------------------+         |
  |                       v                                   |
  |  Layer 3: 관리 (COBIT 2019 APO/BAI/DSS 35개 목표)          |
  |  +----------+ +----------+ +----------+                  |
  |  | APO Align| | BAI Build | | DSS Run  |                  |
  |  | Plan Org | | Acquire  | | Deliver  |                  |
  |  +----------+ +----------+ +----------+                  |
  |                       v                                   |
  |  Layer 4: 운영/감리 (ITIL 4 SVS + MEA 5개 목표)            |
  |  +----------------------------------------------+         |
  |  | Incident/Change/Service Desk + Internal Audit|         |
  |  +----------------------------------------------+         |
  +----------------------------------------------------------+
```

기존 **COBIT 5(2012)**가 Process 중심(5도메인 37프로세스)이었다면, **COBIT 2019**은 **Components of Governance System**(Process, Organizational Structures, Information Flows, People/Skills, Policies/Procedures, Culture/Behavior, Services/Infrastructure, Applications/Technology) 7요소의 조합으로 재설계되어, 클라우드·AI 환경의 가변적 컴포넌트 조합이 가능하다. 예를 들어 GDPR 대응 시 Process(DSS02 보호) + Structure(Privacy Officer) + Technology(DLP 솔루션) + Skill(Privacy Engineer)을 Design Factor 11로 조합한다.

- **📢 섹션 요약 비유**: IT 거버넌스 통합 모델은 마치 **오케스트라 지휘자**와 같다. COBIT는 악보(40개 목표), ISO 38500은 연주 원칙(6원칙), ITIL 4는 각 악기 연주법(34 Practice), 기업 아키텍처는 악보의 배치(TOGAF ADM)이며, 지휘자(CDO/CIO)는 이 모든 것을 실시간으로 조율해 하나의 심포니를 만들어야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019 Design Factor 기반 맞춤형 거버넌스 시스템

COBIT 2019의 핵심 차별점은 **11개 Design Factor**(Enterprise Strategy, Enterprise Goals, Risk Profile, I&T-Related Issues, Threat Landscape, Compliance Requirements, Role of IT, Sourcing Model, IT Implementation Methods, Technology Adoption, Size)에 따라 우선순위 관리목표를 동적으로 산출하는 메커니즘이다. 시험에서는 **"금융기관, 클라우드 70% 사용, AI 도입 초기"** 같은 시나리오에서 Design Factor 매핑과 우선 Governance Objective 도출을 묻는 문제가 빈출한다.

```text
[ COBIT 2019 Governance System 설계 플로우 ]

  +-----------------+
  | Step 1: Context |  <- 11 Design Factor 입력
  |  (기업 맥락)     |     (Strategy, Risk, Compliance 등)
  +--------+--------+
           v
  +-----------------+
  | Step 2: Refine  |  <- Cascading Goals(13 Enterprise Goal->40 IT Goal)
  |  (목표 정렬)     |     매핑 (Primary/Secondary 관계)
  +--------+--------+
           v
  +------------------------------+
  | Step 3: Component Selection  |  <- 7 Component 중 필요한 요소만
  | (컴포넌트 선정)               |     조합 (예: Agile + DevOps Focus Area)
  +--------+---------------------+
           v
  +------------------------------+
  | Step 4: Risk & Priority      |  <- Risk Map 4×5 Matrix
  | (위험·우선순위)               |     (Impact×Likelihood)
  +--------+---------------------+
           v
  +------------------------------+
  | Step 5: Implementation       |  <- 7-Phased Implementation
  | (단계적 적용)                 |     Lifecycle (POPIF)
  +--------------------------------+
```

### 2. 핵심 구성 요소 매트릭스

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate/Direct/Monitor)** | 이사회·경영진 거버넌스 의사결정 | 5개 목표: EDM01(Governance Framework), EDM02(Benefits Delivery), EDM03(Risk Optimization), EDM04(Resource Optimization), EDM05(Stakeholder Transparency) — RACI 표에서 Accountable은 이사회 |
| **APO (Align/Plan/Organize)** | 전략 정렬·계획·조직 설계 | 14개 목표: APO01(Managed I&T Management Framework) ~ APO14(Managed Data) — Balanced Scorecard, Sourcing Model(Make/Buy/Cloud), Target Operating Model 설계 포함 |
| **BAI (Build/Acquire/Implement)** | 솔루션 구축·도입·배포 | 11개 목표: BAI01~BAI11 — Agile/DevOps/CMMI 통합, Phase-Gate 검토, Architecture Review Board 운영 |
| **DSS (Deliver/Service/Support)** | 서비스 운영·지원 | 6개 목표: DSS01(Managed Operations), DSS02(Managed Service Requests & Incidents), DSS03(Managed Problems), DSS04(Managed Continuity), DSS05(Managed Security Services), DSS06(Managed Business Process Controls) — ITIL 4 Practice와 1:1 매핑 가능 |
| **MEA (Monitor/Evaluate/Assess)** | 성과 측정·감사·평가 | 4개 목표: MEA01(Performance & Conformance Monitoring), MEA02(System of Internal Control), MEA03(Compliance with External Requirements), MEA04(Assurance) — 내부감사 및 ISAE 3402 보고 |

### 3. ISO 38500 IT 거버넌스 6원칙 적용 모델

ISO/IEC 38500:2015의 6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)은 COBIT의 EDM 계층과 직접 매핑되며, 각 원칙은 **Plan->Implement->Monitor** 3단 사이클로 운영된다. 예를 들어 **Conformance(준법성)** 원칙은 Plan(COBIT MEA03) -> Implement(DSS05 보안 통제) -> Monitor(내부감사 ISAE 3402 보고)의 3단 구조로 구현된다.

### 4. ITIL 4 Service Value System (SVS)

ITIL 4(2019)는 기존 ITIL v3의 26 프로세스를 **34개 Practice**(14 General + 17 Service + 3 Technical)로 재편하고, **SVS(Service Value System)**를 통해 Opportunity/Demand -> Value로 변환한다. 핵심은 **Value Chain**(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve) 6활동이며, COBIT DSS 6개 목표와 1:1 매핑된다.

- **📢 섹션 요약 비유**: COBIT 2019의 Design Factor는 마치 **맞춤형 셔츠 재단사**와 같다. 표준 패턴(40개 목표)은 정해져 있지만, 11가지 체형(Design Factor) 측정 후 어깨·소매 길이를 개인별 조정해 입히는 것처럼, 각 기업 상황에 맞게 거버넌스 요소를 조합한다.

---

## Ⅲ. 비교 및 연결

### 1. 주요 IT 관리 프레임워크 비교

| 구분 | COBIT 2019 | ITIL 4 | ISO 38500 | PMBOK 7 / PRINCE2 |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | 거버넌스+관리 통합 | IT 서비스 운영 | IT 거버넌스 원칙 | 프로젝트/프로그램 관리 |
| **계층** | 5도메인 40목표 | 34 Practice | 6원칙 | 8 Performance Domain |
| **적용 범위** | Enterprise 전체 IT | 서비스 라이프사이클 | 이사회 의사결정 | 단위 프로젝트 |
| **성숙도 모델** | CMMI 기반 0~5 | 1~5 단계 (Maturity) | 평가 인증 없음 | OPM3 (5단계) |
| **연계 프레임워크** | TOGAF, ITIL, NIST CSF | COBIT(특히 DSS), DevOps | COBIT EDM | COBIT BAI01~03 |
| **최근 개정** | 2019 (Focus Area 추가) | 2019 (SVS 도입) | 2015 | 2021 (Principles 기반) |
| **주 사용자** | CIO, CAE, CDO | Service Desk Manager, SRE | 이사회, 비전임 이사 | PMO, PgMO |
| **측정 지표** | Process Capability(0~5) | KPI/SLA (CSF->KPI->PI) | 원칙 준수 점검표 | SPI/CPI, Earned Value |

### 2. 프레임워크 간 통합 패턴

**TOGAF ADM ↔ COBIT 2019** 매핑이 실무 핵심이다. TOGAF Phase A(Architecture Vision) ↔ COBIT APO02(Strategy), Phase B~D(BSD) ↔ BAI02~BAI05(Architecture/Build), Phase E~F(Opportunities/Migration) ↔ BAI06~BAI11(Transition), Phase G~H(Governance/Change) ↔ DSS01/DSS03, Phase ADM(Requirements Management) ↔ APO04(Innovation). 또한 **NIST CSF 2.0(2024)**의 Govern 카테고리는 COBIT EDM 5개와 1:1 매핑되며, Identify->APO/BAI, Protect->DSS05, Detect->MEA01, Respond->DSS02/03, Recover->DSS04와 연계된다.

### 3. 디지털 전환 연계 모델

**Digital Transformation(가트너 2024)**의 4축(고객/운영/모델/비즈니스)과 IT 거버넌스 연결은:
- **고객 경험**: CO
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 509 / 800

<- **이전**: [508. IT 경영 관리 핵심 토픽 508번 시험 요약](/studynote/12_it_management/05_security_compliance/508_it_management_core_topic_508_exam_summary/)
**다음**: [510. IT 경영 관리 핵심 토픽 510번 시험 요약](/studynote/12_it_management/05_security_compliance/510_it_management_core_topic_510_exam_summary/) ->

---
