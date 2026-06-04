+++
title = "771. IT 경영 관리 핵심 토픽 771번 시험 요약 (IT Management Core Topic 771 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019(거버넌스), ITIL 4(서비스), PMBOK 7(프로젝트), ISO 38500(이사회 지침)의 4대 프레임워크를 CSF(Critical Success Factor)와 KPI로 통합 운영하여, 기업의 전략적 목표와 IT 투자·운영을 정렬(Strategic Alignment)하는 학제적 discipline임.
> 2. **가치**: McKinsey 보고에 따르면 효과적인 IT 거버넌스 체계 구축 시 IT 투자 대비 ROI가 평균 23~35% 상승하며, ITIL 도입 기업은 MTTR(Mean Time To Repair) 50% 단축, 변경 실패율 70% 감소, IDC 조사 기준 IT 거버넌스 성숙도 1단계 상승 시 운영 비용 약 15% 절감 효과가 검증됨.
> 3. **판단 포인트**: 중앙집중형(Centralized) vs 분산형(Federated) 거버넌스 구조 선택, COBIT 2019의 40개 Governance/Management Objective 중 우선순위 선정, CapEx(자본) vs OpEx(운영) 비용 분류, Shadow IT 차단 vs 허용 정책, In-house vs Outsourcing의 Build-Operate-Transfer 전략 결정이 핵심 의사결정 포인트임.

---

## Ⅰ. 개요 및 필요성

디지털 전환(Digital Transformation) 시대를 맞아 IT는 단순 지원 조직을 넘어 **전략적 핵심 자산**으로 재정의되었습니다. 과거(1980~2000년대)에는 IT 운영이 기술 중심의 비용 센터(Cost Center)로 인식되어 폐쇄형·사일로(Silo) 구조로 운영되었으나, 클라우드·AI·데이터 분석의 보편화로 인해 **거버넌스·서비스·프로젝트·재무·보안**을 아우르는 통합적 경영 체계가 필수 요구사항이 되었습니다. Gartner는 2024년 보고에서 "전 세계 CIO의 89%가 IT 비용 최적화와 비즈니스 가치 실현 간의 균형을 최우선 과제로 인식한다"고 발표했으며, 이는 IT 경영 관리 체계 부재 시 발생하는 중복 투자(연간 약 18~25%), Shadow IT로 인한 보안 사고(전체 침해 사고의 38% 차지), 프로젝트 실패율(Standish Group CHAOS Report 기준 31.1% challenged + 16.4% failed) 문제를 정량적으로 뒷받침합니다. 기술사 관점에서는 단순한 IT 운영을 넘어 **ISO/IEC 38500 이사회 거버넌스 원칙(책임·전략·획득·성과·준수·인간행위)**, **COBIT 2019의 40개 거버넌스/관리 목표**, **ITIL 4의 34개 실무 가이드**, **PMBOK 7의 8개 Performance Domain**을 통합적으로 이해하고 조직 맥락에 맞게 설계·운영·감사하는 능력이 핵심 역량입니다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│            IT 경영 관리 4대 핵심 축 및 프레임워크 매핑              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   [전략·거버넌스]              [서비스 운영]                         │
│   ┌──────────────┐             ┌──────────────┐                    │
│   │ COBIT 2019   │◄───────────►│ ITIL 4 (SVS) │                    │
│   │ ISO 38500    │  정렬(Align) │ ISO 20000   │                    │
│   │ 40 G/M Obj.  │             │ 34 Practices │                    │
│   └──────┬───────┘             └──────┬───────┘                    │
│          │                             │                            │
│          │  CSF/KPI Cascade            │  SLA/OLA/UC                │
│          ▼                             ▼                            │
│   ┌──────────────────────────────────────────────────┐             │
│   │      IT Strategy & Portfolio Management          │             │
│   │   (Ward-Peppard, Balanced Scorecard, TOGAF)      │             │
│   └──────────────────────┬───────────────────────────┘             │
│                          │                                          │
│   [프로젝트·변화관리]      │      [재무·위험·컴플라이언스]            │
│   ┌──────────────┐        │      ┌──────────────┐                 │
│   │ PMBOK 7      │◄───────┴─────►│ TBM / FinOps │                 │
│   │ PRINCE2/Agile│               │ ISO 27001    │                 │
│   │ SAFe/LEAN    │               │ BCP/DRP NIST │                 │
│   └──────────────┘               └──────────────┘                 │
│                                                                     │
│   [Board]──[CFO/CIO/CDO/CISO]──[PMO]──[Service Desk]──[End User] │
└─────────────────────────────────────────────────────────────────────┘
```

전통적 IT 조직(폐쇄형·기능별 수직 구조)과 현대적 IT 경영 체계(수평적·가치사슬 기반)의 차이는 다음과 같습니다. 과거에는 네트워크팀·서버팀·DB팀·개발팀이 각각 KPI를 보유하고 독립 운영되어 통합 가시성 부족, 평균 변경 처리 시간 14일, SLA 미달률 40% 이상의 문제를 야기했습니다. 현대 IT 경영 체계는 **End-to-End 서비스 흐름**(요청→승인→변경→배포→모니터링→개선)을 통합 관제하며, CMDB(Configuration Management Database)를 단일 정보원(Source of Truth)으로 활용하여 자산·구성·서비스 간 의존 관계를 자동 매핑합니다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **도시의 종합 관제탑**과 같습니다. COBIT은 도시계획 마스터플랜, ITIL은 교통·상하수도·전력 운영 매뉴얼, PMBOK은 새 건물 건설 공정표, ISO 27001은 치안·소방 안전 규정이며, 이 모든 것을 **도시의 시장(CIO)**이 **시议会(이사회)**의 감독하에 통합 운영하는 체계입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리 아키텍처는 **거버넌스 계층 → 관리 계층 → 운영 계층 → 지원 계층**의 4-tier 구조로 설계되며, 각 계층은 RACI 매트릭스(Responsible, Accountable, Consulted, Informed)로 책임 소재를 명확히 합니다. 최상위 거버넌스 계층은 이사회·CIO·CDO·감사위원회로 구성되며 ISO/IEC 38500의 6대 원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)을 준수합니다. COBIT 2019의 **40개 Governance/Management Objectives**는 EDM(5개), Align/Plan/Organize(14개), Build/Acquire/Implement(11개), Deliver/Service/Support(6개), Monitor/Evaluate/Manage(4개) 5개 도메인으로 분류되며, 이를 **Cascade Goal**(연계 목표) 체계를 통해 기업 목표 → IT 관련 목표 → Enabler 목표 → Management Practice 지표로 하향 변환합니다. 서비스 운영 계층은 ITIL 4의 **Service Value System(SVS)** 기반으로 Opportunity/Demand → Value → Service Value Chain(Plan/Engage/Design&Transition/Obtain/Build/Deliver&Support) → Value Outcome 흐름을 따르며, 34개 Service Management Practice를 적용합니다. 프로젝트 계층은 PMBOK 7의 8개 Performance Domain(Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty)과 12개 Project Management Principle을 적용하고, Agile/Scrum·SAFe·Lean Portfolio Management와 혼합 운영(Hybrid)합니다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│            IT 경영 관리 4-tier 아키텍처 및 데이터 흐름              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  TIER 1: 거버VERNANCE LAYER (정책·감독)                              │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │ Board / Audit Committee / CEO / CIO / CDO / CISO          │    │
│  │ ─ ISO 38500 6대 원칙 ─ COBIT 2019 EDM(5개)              │    │
│  │ ─ Risk Appetite Statement / IT Charter / 정책/표준        │    │
│  └────────────┬───────────────────────────────────────────────┘    │
│               │ Policy & Strategy Cascade                           │
│               ▼                                                     │
│  TIER 2: MANAGEMENT LAYER (계획·조직·통제)                          │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  PMO / SMO(Service Mgt Office) / EPMO(Enterprise PMO)     │    │
│  │  ─ Portfolio Mgmt ─ Demand Mgmt ─ Architecture(TOGAF)    │    │
│  │  ─ FinOps / TBM(Tech Business Mgmt) ─ Vendor/SAM         │    │
│  │  ─ BCP/DRP ─ GRC(Governance Risk Compliance)             │    │
│  └────────────┬───────────────────────────────────────────────┘    │
│               │ Process & Resource Allocation                       │
│               ▼                                                     │
│  TIER 3: OPERATIONAL LAYER (서비스·프로젝트 실행)                    │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Incident / Problem / Change / Release / Service Request  │    │
│  │  ─ SLA(99.9~99.99%) ─ OLA ─ Underpinning Contract(UC)   │    │
│  │  ─ CI/CD Pipeline ─ IaC(Terraform/Ansible) ─ SRE         │    │
│  │  ─ Agile Scrum/SAFe ─ Sprint/Kanban ─ Definition of Done │    │
│  └────────────┬───────────────────────────────────────────────┘    │
│               │ CMDB / Observability / ITSM Data                    │
│               ▼                                                     │
│  TIER 4: SUPPORT LAYER (기술·인력·데이터)                            │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Infra(Cloud/On-prem) ─ DB ─ Network ─ Sec(SIEM/SOAR)   │    │
│  │  ─ HR/Capability(SFIA) ─ Fin/ITFM ─ Compliance(SOX/PIPA)│    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ◄──── KPI/Dashboard Feedback Loop (Power BI / ServiceNow PA) ────  │
└──────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **거버넌스 위원회 (IT Steering Committee)** | 전략 정렬, 투자 우선순위 결정, Risk Appetite 승인 | 분기별 정례 회의, Portfolio KPI 리뷰(ROI ≥ 15%, NPV ≥ 0), Project Pipeline ≥ 80% Utilization 기준 의사결정, 의결 정족수 2/3 이상 |
| **PMO (Project Management Office)** | 프로젝트 표준·방법론 통제, Portfolio 통합 관리, Resource Pool 최적화 | PMBOK 7/Prince2/Agile/SAFe 다중 방법론 지원, Earned Value Management(EAC, BAC, SPI/CPI ≥ 0.95), Atlassian Jira·MS Project·Planview 통합, 요청 Gate(Stage Gate) 5단계(Idea→Feasibility→Design→Build→Operate) |
| **SMO (Service Management Office)** | ITIL 프로세스 거버넌스, SLA/OLA 관리, Continual Improvement | ITIL 4 34개 Practice 매핑, Incident MTTR ≤ 4h/P1 1h, Change Success Rate ≥ 95%, First Call Resolution ≥ 70%, CSAT ≥ 4.2/5.0, ServiceNow/Remedy/BMC Helix ITSM 도구 활용 |
| **CMDB (Configuration Management Database)** | IT 자산·구성 항목(CI)·관계의 단일 정보원, 영향도 분석 | 자동 Discovery(ServiceNow CMDB, BMC Atrium, Device42), CI 6가지 속성(Technical/Owner/Status/Version/Relationship/Financial), Reconciliation 99.5% 정확도 목표, Service Dependency Mapping |
| **FinOps / TBM** | IT 비용 가시성·최적화, 클라우드 비용 거버넌스 | TBM(Tech Business Mgmt) Taxonomy v4.0, FinOps Foundation Framework(Inform/Optimize/Operate), Showback/Chargeback 모델, Reserved Instance/Savings Plan 활용, Unit Economics(매출 1억당 IT 비용) KPI |
| **GRC Platform** | 정책·리스크·컴플라이언스 통합 관리 | ISO 27001/27701, NIST CSF 2.0, PCI-DSS, SOX, 개인정보보호법 PIPA, GDPR 통합 매핑, 리스크 Heat Map(5x5 매트릭스), Control 자동 테스트(Archer/RSA/LogicGate) |
| **보안 관제 (SOC + SIEM/SOAR)** | 위협 탐지·대응, 취약점 관리, 제로 트러스트 | SIEM(Splunk/QRadar/Sentinel) → SOAR(Phantom/Demisto) 자동 오케스트레이션, MTTD ≤ 15분, MTTR ≤ 1시간, NIST CSF 5대 함수(Identify/Protect/Detect/Respond/Recover), Zero Trust(ZTNA, mTLS, BeyondCorp) |

핵심 메커니즘은 **Goal Cascade + KPI Hierarchy**입니다. COBIT 2019의 13개 Enterprise Goal(EG01~13)은 IT 관련 13개 Alignment Goal(AG01~13)과 매핑되며, 이는 다시 40개 Management Objective와 256개 Practice의 Process Activity Level KPI로 분해됩니다. 예를 들어 "EG01: 포트폴리오의 경쟁 제품 및 서비스" 달성을 위해 "AG04: 품질 관리된 IT 관련 솔루션" → "EDM02: Benefit Delivery" → "BAI01: Managed Programs" → KPI "프로젝트 정시 완료율 ≥ 90%, 예산 준수율 ±10%, 사용자 만족도 ≥ 4.0/5.0"으로 cascade됩니다. **Process Capability Assessment**는 COBIT PAM(Process Assessment Model) 기반으로 ISO/IEC 15504(SPICE) 6단계 레벨(0~5: Incomplete~Optimizing)로 측정하며, 목표 레벨 3(Defined) 이상 달성이 거버넌스 성숙도 기준입니다.

- **📢 섹션 요약 비유**: IT 경영 관리 아키텍처는 **자동차의 계기판과 ECU 시스템**과 같습니다. 거버넌스 계층은 운전대(이사회)·내비게이션(전략), 관리 계층은 ECU(PMO/SMO), 운영 계층은 엔진·변속기(서비스·프로젝트), 지원 계층은 도로·연료(인프라·인력)에 해당하며, OBD-II 진단 포트가 CMDB/관제 시스템 역할로 모든 데이터를 통합 분석합니다.

---

## Ⅲ. 비교 및 연결
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 771 / 800

← **이전**: [770. IT 경영 관리 핵심 토픽 770번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/770_it_management_core_topic_770_exam_summary/)
**다음**: [772. IT 경영 관리 핵심 토픽 772번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/772_it_management_core_topic_772_exam_summary/) →

---
