---
title: "IT Management Core Topic 606 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(606번)는 COBIT 2019 거버넌스·ITIL 4 서비스 운영·PMBOK 7th 프로젝트 관리·ISO 27001/20000 보안·서비스 거버넌스·EA( Zachman/FEAF/TOGAF )를 4대 축으로, **전략(Strategy)->거버넌스(Governance)->운영(Operations)->개선(Improvement)** 의 가치 사슬(value chain)로 통합·최적화하는 경영과학이다.
> 2. **가치**: 정량적 효과로 IT 투자 수익률(ROIT) 15~25% 향상, MTTR 60% 단축, 보안사고 40% 감소, 프로젝트 성공률 30%->75% 개선(Standish Group CHAOS Report 기준), 정성적 효과로 경영진-현업-IT 간 정렬(Strategic Alignment) 및 의사결정 투명성 확보.
> 3. **판단 포인트**: (a) **Governance vs Management** 경계 - COBIT 2019의 EDM(평가·지시·모니터링) vs PBR(계획·빌드·운영·모니터링) 구분, (b) **내부 통제 vs 외부 규제 준수** 트레이드오프, (c) **Agile/DevOps** 도입 시 거버넌스 lightweight화 vs 감사 추적성 확보, (d) **Bimodal IT / Two-speed IT** 적용 여부, (e) **국내 법규(전자금융감독규정, 개인정보보호법, 클라우드컴퓨팅법)** 와 글로벌 표준의 조화.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리는 **1980년대 후반 정보화진흥기본법(1995)** 제정 이래, 2000년대 e-정부 프레임워크, 2010년대 클라우드 전환, 2020년대 디지털 전환(DX)·AI 기반 자동화로 패러다임이 진화해 왔다. 특히 606번 시험은 단순 암기형이 아니라 **"왜(Why) 어떤 프레임워크를 어떤 상황에서 적용해야 하는가"** 를 묻는 시나리오·사례형 문제 위주이므로, 거버넌스 목표-원칙-정책-프로세스-기술-측정(KPI) 의 6계층 사고 체계로 답안 구조를 잡아야 한다.

```text
[IT 경영 관리 4대 영역 통합 아키텍처]
+--------------------------------------------------------------------+
|                    CEO / 이사회 (Board of Directors)                |
|         +--------------+--------------+                           |
|         |  Strategy & Governance      |  <- BSC, SWOT, CSF, KPI    |
|         |  (전략·거버넌스)              |  COBIT 2019 EDM           |
|         +--------------+--------------+                           |
|   +--------------------+--------------------+                     |
|   v                    v                    v                     |
|+---------+        +----------+         +----------+               |
|| Portfolio|        | Enterprise|         |  IT      |               |
||  Mgmt   |        | Architecture|       | Service  |               |
|| (PPM)   |        | (EA)      |         | Mgmt     |               |
||PMBOK7th |        |TOGAF/    |         |ITIL 4 /  |               |
||PRINCE2  |        |Zachman    |         |ISO 20000 |               |
|+----+----+        +-----+----+         +----+-----+               |
|     |                   |                   |                     |
|     +-------------------+-------------------+                     |
|                         v                                         |
|   +----------------------------------------------+                |
|   |  IT Operations · DevOps · SRE · Observability |                |
|   |  (CI/CD, IaC(Terraform/Ansible), AIOps)       |                |
|   +----------------------------------------------+                |
|                         |                                         |
|                         v                                         |
|   +----------------------------------------------+                |
|   |  Security & Compliance (ISMS-P, ISO 27001,    |                |
|   |  PCI-DSS, GDPR/개인정보보호법, NIS2)          |                |
|   +----------------------------------------------+                |
|                         |                                         |
|                         v                                         |
|   +----------------------------------------------+                |
|   |  Improvement (CSI): PDCA, Kaizen, OEC,       |                |
|   |  Six Sigma DMAIC, Retrospective               |                |
|   +----------------------------------------------+                |
+--------------------------------------------------------------------+
```

**기존(전통적 IT 관리) vs 현대(IT 경영 관리) 비교**
- **기존(1990s~2000s)**: 비용 중심(Cost Center) -> "IT는 지출",사일로별 운영, 사후 통제(after-the-fact), 내부 위주
- **현대(2020s~)**: 가치 중심(Value Center) -> "IT는 수익/전략 자산", 통합 거버넌스, 실시간 통제(continuous controls monitoring), 생태계·외부 연계(API, B2B, SaaS)
- **필요성**: (1) **이해관계자 복잡성**(주주·이사회·감독기관·고객) (2) **규제 강화**(ESG, 데이터3법, EU AI Act) (3) **기술 복잡성**(멀티클라우드, AI/ML, IoT) (4) **사이버 위협 고도화**(랜섬웨어, APT, 제로데이)

- **📢 섹션 요약 비유**: IT 경영 관리는 **도시의 통합 관제 시스템**과 같다. 도로(인프라)·건축물(시스템)·치안(보안)·교통(운영)·재무(예산)·환경(규제)을 별도로 관리하지 않고, **도시 계획(EA) -> 예산 배정(거버넌스) -> 시민 서비스(ITIL) -> 안전 관리(ISMS) -> 성과 평가(BSC)** 가 한 지붕 아래 돌아가야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리는 **국제 표준(ISO/IEC 38500, ISO/IEC 33000)** 과 **프레임워크(COBIT, ITIL, TOGAF)** 그리고 **방법론(PMBOK, PRINCE2, Scrum)** 의 3-Layer로 구성된다.

```text
[IT 경영 관리 표준-프레임워크-방법론 3-Layer 구조]
+---------------------------------------------------------------+
|  L1: 거버넌스 원칙 (Governance Principles)                      |
|  - ISO/IEC 38500: "Responsibility, Strategy, Acquisition,     |
|    Performance, Conformance, Human Behavior" (6대 원칙)        |
|  - COBIT 2019: 40 Governance & Management Objectives           |
+---------------------------------------------------------------+
|  L2: 운영 프레임워크 (Operating Frameworks)                    |
|  - ITIL 4: 34 Practices, Service Value System (SVS)            |
|  - TOGAF 10: ADM(Architecture Development Method) 8 Phases    |
|  - Zachman: 6W × 5视角 (What/How/Where/Who/When/Why) ×       |
|              (Planner/Owner/Designer/Builder/Operator)         |
+---------------------------------------------------------------+
|  L3: 실무 방법론 (Practical Methodologies)                     |
|  - PMBOK 7th: 12 Principles, 8 Performance Domains            |
|  - PRINCE2 7th: 7 Themes, 7 Processes                         |
|  - Scrum: 3 Roles(PO/SM/Team), 5 Events, 3 Artifacts          |
|  - DevOps: CALMR (Culture, Automation, Lean, Measurement,     |
|            Sharing)                                            |
+---------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** | IT 거버넌스 & 관리 체계 (40개 목표) | EDM(평가·지시·모니터링) 5단계 + PBR(Plan·Build·Run·Monitor) 4영역, **Cascade Goals**: 기업 목표 -> 정렬 목표 -> IT 목표 -> 프로세스 목표(-> 활동 목표). 7개 컴포넌트(원리·정책·프레임워크·조직·정보·인력·서비스·인프라). 11개 디자인 팩터(전략·역할·비전·이슈·리스크·기존시스템 등) 기반 맞춤형 거버넌스 시스템 설계 |
| **ITIL 4 (2019)** | IT 서비스 관리(34 Practices) | Service Value System(SVS): 기회·수요 -> 가치(Value) 창출. 핵심: **Service Value Chain**(Plan->Improve->Engage->Design&Transition->Obtain/Build->Deliver&Support). 4개 차원(Organizations & People, Information & Technology, Partners & Suppliers, Value Streams & Processes) |
| **PMBOK 7th (2021)** | 프로젝트 관리 원칙/도메인 | 12 Principle(예: Be a diligent, respectful, and caring steward 등), 8 Performance Domain(Team, Development Approach, Planning, Work, Delivery, Measurement, Uncertainty, Sat). 프로세스 기반(49개) -> **원칙 기반(Principle-based)** + **원리(Principle)·도메인(Domain)·방법론 선택**의 트라이앵글 |
| **TOGAF 10** | EA(Enterprise Architecture) 개발 방법론 | ADM(Architecture Development Method) 8 Phases: **Preliminary -> A: Architecture Vision -> B: Business -> C: Information Systems -> D: Technology -> E: Opportunities & Solutions -> F: Migration Planning -> G: Implementation Governance -> H: Architecture Change Management -> Requirements Management** (전 단계 공통). ADM Cycle 반복, Architecture Repository(작업/표준/참조/비전) |
| **BSC (Balanced Scorecard)** | 전략적 성과 측정 | 4 관점(재무·고객·내부 프로세스·학습과 성장), 전략 맵(Strategy Map), 인과관계(Causality)·TOC(Theory of Constraints) 기반 KPI 도출, 16~25개 KPI 권고 |

**핵심 알고리즘·원리 심화**

1. **COBIT 2019의 Cascade Goals 메커니즘**:
   ```
   기업 목표(13개) -> 매핑 표 -> 정렬 목표(Alignment Goals, 13개) ->
   매핑 표 -> IT 관련 목표(40개 중 선택) -> 프로세스 목표 자동 도출
   ```
   - 예: 기업 목표 "포트폴리오의 경쟁 제품/서비스" -> 정렬 목표 "전략적 옵션 실현" -> IT 목표 "Managed Portfolio" -> 프로세스 목표 "APO05(관리된 포트폴리오)"
   - **핵심**: 거버넌스 진단 시 "현재 IT 목표와 기업 목표 정렬도 측정"이 첫 단계

2. **ITIL 4 Service Value Chain**:
   - Demand -> **Engage**(고객/이해관계자 참여) -> **Plan**(전략·포트폴리오) -> **Design & Transition**(서비스 설계) -> **Obtain/Build**(구축) -> **Deliver & Support**(운영) -> **Improve**(지속 개선) -> Value
   - **핵심**: 더 이상 v3의 26 프로세스가 아닌 **34 Practices** + **Value Stream** 중심. **Service Desk -> Service Request Management -> Incident Management** 등은 '일반 관리 관행'으로 재편

3. **TOGAF ADM Iteration**:
   - **Iteration vs Phase**: ADM은 8단계(Phase)지만, 실제 프로젝트에서는 **수평 Iteration**(여러 단계 동시 진행) + **수직 Iteration**(Phase G-H의 Implementation Support 반복). **Preliminary Phase**에서 **Architecture Capability**(거버넌스·조직·역할) 정의 필수

4. **PMBOK 7th의 Tailoring**:
   - 프로젝트 특성(규모·복잡성·중요성·불확실성·거버넌스·문화)에 따라 12 Principle + 8 Domain + 적절한 방법론(예측형/적응형/하이브리드) 선택
   - **Predictive, Adaptive, Hybrid** 3 Development Approach

- **📢 섹션 요약 비유**: **COBIT 2019**는 도시의 **헌법**, **ITIL 4**는 **민원 처리 매뉴얼**, **TOGAF**는 **도시계획법**, **PMBOK 7**은 **건축 시공 가이드**, **BSC**는 **성과 평가 KPI 시스템**이다. 이 5종 세트가 한 도시에 동시에 운영되어야 효율적이다.

---

## Ⅲ. 비교 및 연결

### A. 프레임워크 간 비교

| 구분 | **COBIT 2019** | **ITIL 4** | **PMBOK 7th** | **TOGAF 10** | **ISO 38500** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스 & 관리 | IT 서비스 관리 | 프로젝트 관리 | EA 개발 | IT 거버넌스 원칙 |
| **대상 영역** | 전략 ↔ 운영 (End-to-End) | 서비스 운영 (Service) | 단위 프로젝트 | 아키텍처 (4 Layer) | 거버넌스 (상위 원칙) |
| **구조** | 40 목표 + 7 컴포넌트 | 34 Practice + SVS | 12 Principle + 8 Domain | 8 Phase ADM | 6 원칙(모델) |
| **범위** | What/Why (무엇을 왜) | How (어떻게) | How (어떻게) | How (어떻게) | What (무엇을) |
| **측정 지표** | Process Capability(0~5) | Practice 지표(CSF/KPI) | Performance Domain KPI | Architecture Maturity | 거버넌스 준수도 |
| **업데이트** | 2018/19(2019) | 2019(4th) | 2021(7th) | 2022(10th) | 2015 |
| **적용 사례** | 감사·이해관계자 보고 | 헬프데스크·운영 | SW 개발·ERP 구축 | 디지털 전환·표준화 | 이사회 의사결정 |

### B. 연결 관계

```text
[5대 프레임워크 통합 맵]
이사회 거버넌스 --- ISO/IEC 38500 (6대 원칙)
       |
       v
전략/포트폴리오 --- COBIT 2019 EDM(5단계) + BSC(4관점)
       |
       +--> 아키텍처 정의 --- TOGAF ADM(8Phase)
       |
       +--> 프로젝트 실행 --- PMBOK 7 / PRINCE2 7 / Scrum
       |              |
       |              +--> 개발·테스트 --- DevOps/CI-CD
       |
       +--> 서비스 운영 --- ITIL 4 SVS(34 Practices) + ISO 20000
                          |
                          +--> 보안·컴플라이언스 --- ISO 27001 / ISMS-P
```

- **📢 섹션 요약 비유**: 위 다이어그램은 **오케스트라**에 비유할 수 있다. **ISO 38500=지휘자(Conductor)**, **COBIT=악보(Score)**, **TOGAF=악보 구조(Arrangement)**, **PMBOK=각 파트 연습**, **ITIL=공연 당일 운영**, **ISMS=보안 요원** — 모두 한 무대 위에서 조화롭게 울려야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **"이 상황에서 어떤 프레임워크를 선택해야 하는가?"**
   - 거버넌스 감사·이해관계자 보고 -> **COBIT 2019 + ISO 38500**
   - 서비스 운영 표준화·민원 처리 -> **ITIL 4 + ISO 20000**
   - EA 통합·표
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 606 / 800

<- **이전**: [605. IT 경영 관리 핵심 토픽 605번 시험 요약](/studynote/12_it_management/05_security_compliance/605_it_management_core_topic_605_exam_summary/)
**다음**: [607. IT 경영 관리 핵심 토픽 607번 시험 요약](/studynote/12_it_management/05_security_compliance/607_it_management_core_topic_607_exam_summary/) ->

---
