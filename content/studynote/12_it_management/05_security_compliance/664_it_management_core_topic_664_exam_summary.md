+++
title = "664. IT 경영 관리 핵심 토픽 664번 시험 요약 (IT Management Core Topic 664 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019 Governance System은 6단계 Cascade(Governance->Management->Align/Plan/Build->Productivity->Value) 기반으로 40개 Governance/Management Objective을 7개 Component(원리/정책/프레임워크/문화/인력/정보/서비스)로 분해하여 Enterprise I&T 거버넌스를 체계화한 통합 프레임워크
> 2. **가치**: Design Factor 11개(이해관계자 전략, 위협, 규제, IT 이슈, 기술 adopt, 전략 init, 방법론, 기술 adopt)별 Governance System 변형 가능, ISO/IEC 38500·ISO 27001·TOGAF·ITIL 4·NIST CSF·CMMI 5개 표준과 1:1 매핑된 23개 Focus Area로 감사 대응 시간 60% 단축 및 Risk-adjusted ROI 평균 18% 향상
> 3. **판단 포인트**: Audit-First(CMMI/ISO) vs. Value-First(COBIT) vs. Agility-First(SAFe) 트레이드오프, Design Factor 가중치 합계 100% 정규화 시 Strategic Alignment vs. Risk Optimization 간 배분 비율, In-house Build(85% 내재화) vs. SaaS(50% TCOv) vs. Hybrid 거버넌스 도구 도입 전략

---

## Ⅰ. 개요 및 필요성

정보화사업의 규모가 연 5,000억 원 이상 대형화되고, 클라우드·AI·DevSecOps·제로트러스트 등 신기술 도입이 가속화되면서 **Enterprise I&T(Information & Technology)** 자산을 효과적으로 거버넌스하는 통합 관리 체계가 필수 요구사항이 되었다. 2024년 기준 ISACA 글로벌 조사에 따르면, Fortune 500 기업의 73%가 3개 이상의 거버넌스 프레임워크를 병행 운용 중이며, 통합 미흡으로 인한 중복 Compliance 비용이 평균 연 420억 원에 달한다.

특히 국내에서는 **전자정부법 제46조(정보시스템의 효율적 운영)**, **클라우드컴퓨팅법**, **개인정보보호법**, **산업안전보건법**, **ISMS-P 인증제** 등 17개 이상의 규제 체계가 동시 적용되어, 단일 표준만으로는 Audit 대응이 불가능한 상황이다. 이를 해결하기 위해 **COBIT 2019**는 5대 관련 표준을 Focus Area로 통합 매핑하고, 11개 Design Factor 기반으로 조직별 맞춤형 Governance System을 설계할 수 있는 유연성을 제공한다.

기존 COBIT 5(2012)가 Process Capability 중심의 정형화된 5단계 Maturity Model을 제공한 반면, COBIT 2019는 **Open Source Customization** 개념을 도입하여 프로세스 활동(activity) 단위를 조직의 Agility 수준, 전략적 우선순위, 규제 강도에 따라 동적으로 조합·재배치할 수 있다. 이는 Agile·DevOps·Cloud Native 환경에서 요구되는 **Continuous Compliance** 패러다임과 정합하며, 6개월 단위 Governance Review가 아닌 Real-time Dashboard 기반 운영을 가능케 한다.

```text
+--------------------------------------------------------------------+
|          Enterprise I&T Governance Evolution Timeline              |
+--------------------------------------------------------------------+
|                                                                    |
|  COBIT 5 (2012)           COBIT 2019 (2018)         2025+ Target  |
|  +----------+             +--------------+         +----------+  |
|  |Process-  |             |Governance    |         |AI-Aug-   |  |
|  |Capability| -----------> |System +      | -------> |mented    |  |
|  |5-Level   |             |Design Factor |         |Continuous|  |
|  |Maturity  |             |40 Objectives |         |Governance|  |
|  +----------+             +--------------+         +----------+  |
|  • 37 Process         • 40 Objective              • LLM-based    |
|  • 5 Enabler          • 7 Component                 Anomaly       |
|  • PAM 4.0            • 11 Design Factor            Detection     |
|  • Static Mapping     • Focus Area 23               Auto-Remediation
|                                                   • Quantum-safe |
|                                                     Cryptography  |
+--------------------------------------------------------------------+

        3대 거버넌스 패러다임 비교
        +-------------+--------------+--------------+
        |  Audit-First|  Value-First | Agility-First|
        | (CMMI/ISO)  |  (COBIT)     |   (SAFe)     |
        +-------------+--------------+--------------+
        | Compliance  | ROI/         | Time-to-     |
        | 우선        | Risk-adjusted| Market 우선  |
        |             |  Value       |              |
        +-------------+--------------+--------------+
```

- **📢 섹션 요약 비유**: COBIT 2019는 자동차로 비유하면 **"운전자가 11가지 Design Factor(도로 상태, 날씨, 연료, 승객 수, 목적지 등)에 따라 자동으로 서스펜션·엔진·타이어 공압을 재조정하는 Adaptive Chassis Control"**와 같다. 과거 COBIT 5가 5단 기어 수동변속기였다면, COBIT 2019는 11단 DCT 자동변속기에 해당한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019는 6단계 Cascade 구조로 거버넌스를 운영한다. ① **Stakeholder Needs & Drivers**에서 시작해 ② **Enterprise Goals**(13개, Balanced Scorecard 4관점) -> ③ **Alignment Goals**(13개 I&T 관련) -> ④ **Governance Objectives**(5개, EDM: Evaluate/Direct/Monitor) -> ⑤ **Management Objectives**(35개, APO/BAI/DSS/MEA 4도메인) -> ⑥ **Component Variants**(7개 Component별 Practice)로 전개된다. 각 단계는 1:N 매핑되며, Traceability Matrix로 양방향 추적 가능하다.

핵심 7개 **Governance & Management Components**는 ① Principles(원리·가이드라인), ② Policies(정책·절차), ③ Frameworks(산업 표준·방법론), ④ Culture·Ethics·Behavior(조직문화), ⑤ People·Skills·Competencies(인적역량), ⑥ Information(정보·데이터), ⑦ Services·Infrastructure·Applications(기술서비스)이며, 각 Component는 4-7단계의 **Capability Level**(0:Incomplete ~ 5:Optimizing)로 Maturity 평가한다. **Performance Management** 체계는 ISACA의 **CMMI 5-Level**과 **ISO/IEC 33020 Process Capability**를 통합한 7-Level 모델을 채택했다.

아래는 40개 Objective의 도메인별 분류와 핵심 KPI이다.

```text
   COBIT 2019 40 Governance/Management Objectives Architecture
   +----------------------------------------------------------+
   |  Governance Domain (5)              EDM                  |
   |  +-- EDM01 Governance Framework    RACI=Board          |
   |  +-- EDM02 Benefits Delivery       RACI=Board          |
   |  +-- EDM03 Risk Optimization       RACI=Risk Committee |
   |  +-- EDM04 Resource Optimization   RACI=CIO/CTO        |
   |  +-- EDM05 Stakeholder Transparency RACI=Audit Comm.   |
   |                                                            |
   |  Management Domain - Align, Plan, Organize (APO, 14)     |
   |  +-- APO01-14: Strategy/Portfolio/Architecture/         |
   |  |   Innovation/Workforce/Budget/Suppliers/Quality/      |
   |  |   Risk/Security/...                                   |
   |  Management Domain - Build, Acquire, Implement (BAI, 11) |
   |  +-- BAI01-11: Programs/Requirements/Solutions/         |
   |  |   Availability/Changes/Transition/Acceptance/...      |
   |  Management Domain - Deliver, Service, Support (DSS, 6)  |
   |  +-- DSS01-06: Operations/Service Requests/Incidents/  |
   |  |   Continuity/Security Services/Business Controls    |
   |  Management Domain - Monitor, Evaluate, Assess (MEA, 4) |
   |  +-- MEA01-04: Performance/Compliance/Internal/Issues  |
   +----------------------------------------------------------+

   Goal Cascade Traceability (Example: Goal 01 재무성과)
   Stakeholder: Shareholder -> EG01 (재무 자산 growth) -> AG01
   (I&T Compliance & Support) -> EDM02 (Benefits Delivery)
   -> APO05 (Portfolio Mgmt) -> BAI01 (Programs) -> DSS04 (Continuity)

   Capability Rating: PAM 4.0 (Process Assessment Model)
   Level 0: Incomplete -- Level 1: Initial -- Level 2: Managed
   Level 3: Defined -- Level 4: Quantitative -- Level 5: Optimizing
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Design Factor (11개)** | 조직별 Governance System 자동 맞춤 설계 | Strategy Profile, Enterprise Goals, Risk Profile, I&T Issues, Threat Landscape, Compliance Requirements, IT Architecture, Sustainability, Role of IT, Sourcing Model, IT Methods. 각 Factor는 가중치 0~100% 할당 후 우선순위 도출 |
| **Focus Area (23개)** | 특정 주제별 Best Practice 번들 | DevOps·Cybersecurity·Digital Transformation·Cloud·Risk·Privacy·ESG·Small/Medium Enterprise 등. 각 FA는 평균 3-5개 Management Objective를 묶어 5-7개 Component별로 가이드 제공 |
| **Goals Cascade** | Stakeholder->Enterprise->Alignment->Governance 4단계 정렬 | 13 EG × 13 AG = 169개 Primary 매핑 + 12개 Secondary, I&T Balanced Scorecard 4관점(Financial/Customer/Internal/Learning) 적용 |
| **7 Components** | 거버넌스 구성요소 7축 | ①Principles ②Policies ③Frameworks ④Culture ⑤People ⑥Information ⑦Services. 각 Component별 4-7단계 Capability Rating, ISO/IEC 33020 Process Capability와 1:1 매핑 |
| **Performance Mgmt (PAM 4.0)** | 프로세스 성숙도 평가 | 7-Level Rating(ISO/IEC 33020), 40 Objective별 Process Goal 산정, Base Practice 7-13개×Work Product 5-8개로 평가 |
| **Risk Optimization (EDM03)** | IT 리스크 정량화 | FAIR(Factor Analysis of Information Risk) 모델 통합, ALE(Annual Loss Expectancy) × Risk Tolerance 한계선, 0-100점 Risk Score로 우선순위 도출 |

**핵심 파라미터 및 산식**:
- **Capability Level 산정**: `CL = Σ(Process Attribute Rating × Weight) / Σ(Weight)`, PA 9개(PA1.1~2.2) × 6-Level Rating
- **Risk Score**: `RS = Probability (1-5) × Impact (1-5) × Velocity (1-3)`, 최댓값 75
- **IT Cost 최적화 비율**: `TCO = CapEx + OpEx × 5년`, Industry 평균: CapEx 35% / OpEx 65%
- **Design Factor 우선순위**: `Priority = Σ(Factor Score × Weight)`, 가중치 합 100% 정규화

- **📢 섹션 요약 비유**: 7개 Component는 **"오케스트라의 7개 악기 섹션(원리=지휘자, 정책=악보, 프레임워크=편곡, 문화=무대 매너, 인력=연주자, 정보=음표, 서비스=악기)"**이며, Design Factor는 **"연주할 곡의 장르(클래식/재즈/팝)"**를 정하는 Conductor의 판단에 해당한다.

---

## Ⅲ. 비교 및 연결

COBIT 2019는 단독으로 운영되기보다 다른 거버넌스·관리 프레임워크와 상호 보완적으로 적용된다. 특히 5대 핵심 표준인 ITIL 4(Service Management), ISO 27001(ISMS), TOGAF(Architecture), CMMI(Development), NIST CSF(Cybersecurity)와의 매핑이 중요하다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 38500** | **PMBOK 7** | **SAFe 6.0** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **핵심 목적** | Enterprise I&T 거버넌스 | IT 서비스 운영 관리 | IT 의사결정 거버넌스 원칙 | 프로젝트·프로그래임 관리 | 대규모 Agile 스케일링 |
| **대상 계층** | Board/CIO/Audit Committee | Service Manager/운영팀 | Board/이사회 | PMO/Project Manager | ART/Release Train |
| **주요 구성** | 40 GO/MO + 7 Component | 34 Practice + 4D Model | 6 Principles + 5 Governance Model | 12 Principle + 8 Performance Domain | 7 Core Value + 7 Config |
| **평가 체계** | CMMI 5-Level + ISO 33020 6-Level | 4D Maturity(초기->적응->최적->변혁) | Conformance 체크리스트 | PMO Maturity 5-Level | Business Agility 5-Level |
| **Cycle** | Annual Review + Continuous | Value Stream 기반 Continuous | 6개월 Board Review | Project Lifecycle | PI(Program Increment) 8-12주 |
| **ITIL 매핑** | 전체 도메인(DSS/APO/BAI) | 100% 자기 영역 | Service Delivery 부분 | MEA03(Monitor) | Agile Service Mgmt |
| **적용 사례** | 금융·공공·통신 ISMS-P | IDC 운영·헬프데스크 | EU 정부 IT 의사결정 | SI 프로젝트 | SI/뱅킹 디지털전환 |
| **도구 예시** | ServiceNow GRC, SAP GRC, Archer | ServiceNow ITSM, Jira SM, Ivanti | 자체 체크리스트, Power BI | MS Project, Primavera P6 | Jira Align, Azure DevOps |
| **인증 비용** | COBIT 2019 Foundation 50만원 | ITIL 4 Foundation 60만원 | ISO 38500 Lead 80만원 | PMP/PgMP 90만원 | SAFe SA 70만원 |
| **통합 시너지** | EDM + APO = 상위 Governance | Service 운영의 표준화 | Board 거버넌스 원칙 | 프로젝트 정렬 | Agile Delivery |

**다른 시스템·도구와의 연결**:
- **ERP/SAP GRC**: APO01(Strategy), MEA02(Compliance) 영역을 SAP GRC 12.0 Process Control과 양방향 API 연동 (OData v4)
- **SIEM/Splunk/QRadar**: DSS05(Security Services) -> MEA01(Performance) -> Splunk SPL 쿼리 200개 표준 매핑
- **DevOps Toolchain**: BAI03(Solutions) -> Jenkins/GitLab CI, ArgoCD GitOps 연동, DORA Metrics 자동 수집
- **Cloud(AWS/Azure/GCP)**: APO04(Innovation), DSS01(Operations) -> Cloud Custodian Policy 50+ 자동 매핑
- **Zero Trust Architecture**: DSS05 -> NIST SP 800-207, BeyondCorp, SDP Controller 1:1 매핑

```text
   Multi-Framework Integration Architecture
   +------------------------------------------------------+
   |  Strategic Layer (Board)                             |
   |  +-------------+
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 664 / 800

<- **이전**: [663. IT 경영 관리 핵심 토픽 663번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/663_it_management_core_topic_663_exam_summary/)
**다음**: [665. IT 경영 관리 핵심 토픽 665번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/665_it_management_core_topic_665_exam_summary/) ->

---
