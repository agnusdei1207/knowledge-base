+++
title = "715. IT 경영 관리 핵심 토픽 715번 시험 요약 (IT Management Core Topic 715 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, ISO/IEC 38500 등 글로벌 표준 프레임워크를 기반으로 **거버넌스-전략-포트폴리오-서비스-리스크-가치**의 6대 영역을 통합 운영하여, IT를 비용 중심에서 비즈니스 가치 창출의 전략 자산으로 전환하는 경영 패러다임임.
> 2. **가치**: 체계적 IT 경영 체계 도입 시 ROI 25~40% 향상, IT 프로젝트 실패율 30%->10% 감소, IT 운영 비용 20~35% 절감, 의사결정 속도 50% 개선 등 정량적 효과와, 이사회-경영진-IT 삼자 간 책임·권한·소통 체계 확립의 정성적 효과를 동시에 달성.
> 3. **판단 포인트**: **"Standardize vs Customize"**, **"Build vs Buy"**, **"Centralize vs Federate"**, **"Lead vs Follow"** 등 4대 핵심 트레이드오프 하에서, 조직의成熟度(Maturity Level 1~5)와 산업별 규제 강도(금융/공공/의료)를 고려한 **단계적·맞춤형 로드맵** 설계가 기술사의 핵심 판단 기준임.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX) 가속화와 4차 산업혁명 기술(AI, IoT, Blockchain, Cloud, Big Data)의 융합으로, IT는 더 이상 단순 지원(Support) 기능이 아닌 **핵심 경쟁력(Core Competency)**으로 재정의되었습니다. 한국 IT 시장 규모는 2023년 약 250조 원에 달하며, 이 중 65% 이상이 레거시 시스템 유지보수와 신규 디지털 투자로 양분되어 있습니다. 그러나 McKinsey 조사에 따르면 글로벌 IT 프로젝트 실패율은 여전히 30~45%에 달하고, CIO의 70%는 "IT-Business 정렬(IT-Business Alignment)"을 최우선 과제로 보고 있습니다.

본 토픽은 이러한 환경에서 **정보관리기술사**가 기업의 IT 자산을 효과적으로 기획·구축·운영·평가하기 위해 필요한 종합적 관리 체계를 다룹니다.

```text
+------------------------------------------------------------------+
|              IT 경영 관리 6대 도메인 통합 프레임워크               |
+------------------------------------------------------------------+
|                                                                  |
|   +----------+   +----------+   +----------+   +----------+   |
|   | Governance|--->| Strategy |--->|Portfolio |--->| Service  |   |
|   |  거버넌스  |   |   전략   |   | 포트폴리오|   |  서비스  |   |
|   +-----+----+   +-----+----+   +-----+----+   +----+-----+   |
|         |              |              |              |          |
|         |    +---------+--------+     |              |          |
|         |    |  IT-Business     |     |              |          |
|         |    |   Alignment      |     |              |          |
|         |    +------------------+     |              |          |
|         |                            |              |          |
|         +------------+---------------+--------------+          |
|                      v                                          |
|              +--------------+   +--------------+                |
|              |   Risk       |   |   Value      |                |
|              |   리스크     |   |   가치       |                |
|              +--------------+   +--------------+                |
|                                                                  |
|   +------------------------------------------------------+    |
|   |        Global Standards Layer                        |    |
|   |  COBIT 2019 | ITIL 4 | ISO 38500 | CMMI | TOGAF     |    |
|   +------------------------------------------------------+    |
+------------------------------------------------------------------+
```

**레거시 vs 현대 IT 경영 패러다임 비교**

| 항목 | 전통적 IT 경영 (1990~2010) | 현대 IT 경영 (2015~현재) |
|:---|:---|:---|
| 조직 위치 | CIO는 후방 지원 역할, COO/CTO 종속 | CDO·CIO가 경영진(Digital Executive) 참여 |
| 투자 기준 | TCO(Total Cost of Ownership) 중심 | TVO(Total Value of Ownership) + ROI + NPV |
| 의사결정 | 연 1회 CAPEX 예산 사이클 | 지속적·반복적(Bimodal/Agile) 의사결정 |
| 거버넌스 | 계층적·중앙집중 | 분산형·데이터 기반(DDX: Data-Driven eXecution) |
| 기술 스택 | Monolithic (Mainframe, ERP) | Microservices, Cloud-Native, Composable |
| 위험 관리 | 사후 대응(Reactive) | 사전 예방·예측(Predictive)·내회복(Resilient) |
| 평가 체계 | Uptime, MTBF | NPS, MTTR, Customer Journey Score, OKR/KPI |

- **📢 섹션 요약 비유**: IT 경영 관리는 자동차의 **'통합 계기판(Integrated Dashboard)'**과 같습니다. RPM(프로세스), 속도(성과), 연료(예산), 엔진온도(리스크), 내비게이션(전략)을 실시간으로 통합 모니터링하여 운전자가 한눈에 차량 상태를 파악하고 최적 경로로 목적지에 도달하도록 돕는 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. IT 거버넌스 아키텍처 (3-Layer Governance Model)

```text
+--------------------------------------------------------------------+
|                   3-Layer IT Governance Architecture                |
+--------------------------------------------------------------------+
|                                                                      |
|  +-------------------------------------------------------------+   |
|  |  L1: Board-Level Governance (이사회·경영진)                  |   |
|  |  ---------------------------------------------              |   |
|  |  • 이사회의 IT 거버넌스 위원회 (IT Steering Committee)       |   |
|  |  • CIO/CDO 보고 체계 (Monthly/Quarterly Review)             |   |
|  |  • 전략적 방향성 (IT Strategy Alignment)                     |   |
|  |  • 책임 분담 (RACI Matrix)                                   |   |
|  +------------------------+------------------------------------+   |
|                           v                                         |
|  +-------------------------------------------------------------+   |
|  |  L2: Management-Level Governance (IT 관리조직)               |   |
|  |  -----------------------------------------                |   |
|  |  • IT PMO (Project Management Office)                       |   |
|  |  • IT Steering Committee (Cross-functional)                 |   |
|  |  • Architecture Review Board (ARB)                          |   |
|  |  • Change Advisory Board (CAB)                                |   |
|  +------------------------+------------------------------------+   |
|                           v                                         |
|  +-------------------------------------------------------------+   |
|  |  L3: Operational-Level Governance (운영 현장)               |   |
|  |  -----------------------------------------                |   |
|  |  • DevOps Teams / Scrum Teams                                |   |
|  |  • Service Desk / NOC / SOC                                 |   |
|  |  • Service Level Management                                  |   |
|  |  • Continuous Compliance Monitoring                          |   |
|  +-------------------------------------------------------------+   |
|                                                                      |
|  <--- Feedback Loop: Audit · Performance Review · Risk Report --->   |
+--------------------------------------------------------------------+
```

### 2. 핵심 프레임워크별 구성 요소

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **COBIT 2019** | IT 거버넌스·관리 체계 | 40개 관리 목표(Management Objective)와 5개 도메인(EDM: Evaluate-Direct-Monitor; APO: Align-Plan-Organize; BAI: Build-Acquire-Implement; DSS: Deliver-Service-Support; MEA: Monitor-Evaluate-Assess). **Cascade of Goals** 메커니즘으로 Stakeholder Needs -> Enterprise Goals -> Alignment Goals -> Management Goals 계층 정렬. CMMI 기반 성숙도(0~5단계) 적용 |
| **ITIL 4** | IT 서비스 관리 (ITSM) | **Service Value System (SVS)** 중심의 34개 Practice. Opportunity/Demand -> Value로 전환하는 **Value Chain** 활동(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve). SRE(Site Reliability Engineering)와 AIOps 통합 |
| **ISO/IEC 38500** | IT 거버넌스 국제 표준 | 6개 원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior). **Governance->Management->Operational** 3계층 분리. PDCA 사이클 기반 Monitor 메커니즘 |
| **TOGAF 10** | EA(Enterprise Architecture) | **ADM (Architecture Development Method)** 10단계 사이클. Phase A(Architecture Vision) -> H(Architecture Change Management) -> Requirements Management(전 단계 공통). **Architecture Repository** (Architecture Meta-model, Capability Framework, Reference Model) |
| **PMBOK 7 / PRINCE2** | 프로젝트 관리 | PMBOK 7: 12 Principle + Performance Domain(Project, Planning, Uncertainty, etc.). PRINCE2: 7 Principles, 7 Themes, 7 Processes. Agile-PMBOK 통합 |

### 3. IT 가치 측정 모델 (Valuation Framework)

```text
+----------------------------------------------------------+
|           IT Value Measurement Hierarchy                  |
+----------------------------------------------------------+
|                                                            |
|  Level 1: Financial Value (재무적 가치)                  |
|  +-- Cost Reduction: TCO 절감 (Hard Benefit)             |
|  +-- Revenue Growth: IT-enabled 매출 (ROI 계산)          |
|  +-- NPV/IRR: 5~7년 Cash Flow 기반                       |
|                                                            |
|  Level 2: Operational Value (운영적 가치)                |
|  +-- Productivity: FTE당 처리량 (Throughput/Head)        |
|  +-- Quality: 결함률 0.05% 이하, 가용성 99.99%          |
|  +-- Agility: Time-to-Market 50% 단축                   |
|                                                            |
|  Level 3: Strategic Value (전략적 가치)                  |
|  +-- Innovation Index: 신규 서비스 출시 수              |
|  +-- Customer Satisfaction: NPS 50+                     |
|  +-- Brand Value: Digital Brand Equity                  |
|                                                            |
|  Level 4: Information Value (정보 가치)                 |
|  +-- Data-driven Decision: 의사결정 속도·정확도         |
|  +-- Insight-to-Action Cycle Time                       |
|                                                            |
+----------------------------------------------------------+
```

### 4. 핵심 파라미터 및 계산식

**① TCO (Total Cost of Ownership) 산정**
```
TCO = ∑(Direct Cost: HW + SW + Network + Datacenter)
    + ∑(Indirect Cost: 인건비 + 교육 + 유지보수 + 다운타임 손실)
    + ∑(Hidden Cost: 통합·마이그레이션·컴플라이언스)
    - ∑(Benefit: 생산성 향상 + 매출 증대)
```

**② IT 포트폴리오 최적화 (Bohanec-Marković 의사결정)**
- **필수 제약**: 예산 한도(B ≤ B_max), 인력 한도, 컴플라이언스 필수 투자
- **목적함수**: Maximize Σ(V_i × x_i) - Σ(C_i × x_i) [V: 가치, C: 비용, x: 0/1 선택]
- **DEcision EXperiment (DEX) 다기준 의사결정 트리** 활용

**③ 가용성(Availability) 계산**
```
Availability = MTBF / (MTBF + MTTR) = Uptime / (Uptime + Downtime)
Tier III: 99.982% (연 1.6시간 장애)
Tier IV: 99.995% (연 26분 장애)
5-Nines: 99.999% (연 5분 15초)
```

- **📢 섹션 요약 비유**: IT 거버넌스 3계층은 **'비행기 조종 시스템'**과 같습니다. L1(파일럿/이사회)은 비행 방향을 결정하고, L2(자동조종장치/PMO)는 경로를 최적화하며, L3(엔진/운영팀)는 실제 추력을 제공합니다. 자동조종장치가 없으면 파일럿의 미세한 진동도 비행 안전을 위협합니다.

---

## Ⅲ. 비교 및 연결

### 1. 핵심 프레임워크 비교

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **CMMI v2.0** |
|:---|:---|:---|:---|:---|
| **주 목적** | 거버넌스 + 관리 | 서비스 관리 | 거버넌스 원칙 | 프로세스 성숙도 |
| **대상** | CIO·이사회·감사 | IT 운영·서비스팀 | 이사회·경영진 | 개발·운영 조직 |
| **구조** | 40 Management Objective | 34 Practice, SVS | 6 Principle | 5 Maturity Level(0~5) |
| **강점** | 컴플라이언스·감사 친화 | 실제 운영·고객가치 | 원칙 중심·간결 | 단계적 개선 경로 |
| **약점** | 구현 복잡도 높음 | 거버넌스 관점 부족 | 구체성 부족 | 측정·인증 비용 큼 |
| **적합 조직** | 금융·공공·대기업 | 서비스 중심 기업 | 모든 조직 | SW 개발·운영 조직 |

### 2. IT 투자 전략 비교

| 구분 | **Lead (선도주자)** | **Fast Follower** | **Slow Follower** | **Laggard (후발주자)** |
|:---|:---|:---|:---|:---|
| 시장점유율 | 30~40% | 40~50% | 10~20% | 5% 이하 |
| 리스크 | 매우 높음 | 중간 | 낮음 | 매우 낮음 |
| R&D 투자 | 매출의 15~20% | 8~12% | 4~6% | 1~3% |
| ROI 예측성 | 불확실 | 보통 | 높음 | 매우 높음 |
| 적합 기업 | GAFA, BAT, 토종 빅테크 | 금융·통신·제조 대기업 | 전통 제조·중견기업 | SMB·공공기관 |
| 사례 | Apple Vision Pro | 카카오 AI | 포스코 스마트팩토리 | 전통 서점, 화폐거래소 |

### 3. Build vs Buy vs Rent 의사결정 매트릭스

| 평가 기준 | **Build (자체개발)** | **Buy (패키지 구매)** | **Rent (SaaS/Cloud)** |
|:---|:---|:---|:---|
| 초기 투자 | 매우 높음 (CAPEX 집중) | 중간 (라이선스) | 낮음 (OPEX) |
| 구현 기간 | 12~24개월 | 3~6개월 | 1~3개월 |
| 맞춤화 수준 | 100% 자유 | 70~80% 가능 | 20~30
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 715 / 800

<- **이전**: [714. IT 경영 관리 핵심 토픽 714번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/714_it_management_core_topic_714_exam_summary/)
**다음**: [716. IT 경영 관리 핵심 토픽 716번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/716_it_management_core_topic_716_exam_summary/) ->

---
