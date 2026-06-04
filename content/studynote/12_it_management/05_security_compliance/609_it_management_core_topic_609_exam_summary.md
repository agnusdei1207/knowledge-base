---
title: "609. IT 경영 관리 핵심 토픽 609번 시험 요약 (IT Management Core Topic 609 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019(거버넌스·관리 목표 40개)**, **ITIL 4(SVS 34개 Practice)**, **ISO 38500(거버넌스 6원칙)**, **ISO 27001(ISMS 93통제항목)**을 통합한 체계로, **IT-Business Alignment(전략적 정렬성), Value Delivery(가치 전달), Risk Optimization(위험 최적화), Resource Optimization(자원 최적화), Performance Measurement(성과 측정)** 5대 핵심 역량을 통해 기업의 디지털 전환과 지속가능 성장을 견인하는 경영과학이다.
> 2. **가치**: McKinsey 조사에서 **COBIT·ITIL 전면 도입 기업은 IT 투자 ROI 28% 향상, IT 사고 MTTR 47% 단축, 컴플라이언스 비용 35% 절감** 효과를 얻으며, **정보관리기술사 관점**에서는 단순 기술 관리를 넘어 **IT 거버넌스 위원회 거버넌스 모델, RACI 매트릭스, Balanced Scorecard 4관점(재무/고객/내부/학습성장) 기반 KPI**를 통해 CEO·CFO·CIO 3자 간 정합성 있는 의사결정 체계를 확립할 수 있다.
> 3. **판단 포인트**: **① In-House vs Outsourcing(Managed Service) vs Hybrid(클라우드 우선)**, **② Centralized vs Federated vs COE(센터오브엑설런스) 조직 모델**, **③ CapEx(전통적 자산투자) vs OpEx(클라우드 구독) 재무 모델**, **④ Agile(DevOps·SAFe) vs Plan-Driven(Waterfall) 거버넌스**, **⑤ Zero Trust vs Defense-in-Depth 보안 전략** 5대 트레이드오프를 조직의 **Digital Maturity Level(DMM 5단계: Initial->Managed->Defined->Quantitatively Managed->Optimizing)**에 맞춰 정합성 있게 설계하는 것이 핵심이다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(Digital Transformation)이 가속화되면서 IT는 **기업의 경쟁력 그 자체**가 되었다. 과거 IT는 **Cost Center(비용 센터)**로 인식되어 단순한 시스템 운영·유지보수에 머물렀으나, 4차 산업혁명(AI·빅데이터·IoT·블록체인·클라우드) 시대에는 **Value Driver(가치 창출 동인)**이자 **Strategic Asset(전략 자산)**으로 재정의되었다. 이러한 패러다임 전환 속에서 **"어떻게 IT를 경영의 핵심 축으로 통합·관리할 것인가"**라는 질문이 등장했고, 그 해답이 바로 **IT 경영 관리(IT Management)**이다.

특히 **COVID-19 이후의 New Normal** 환경에서는 원격근무, 디지털 워크스페이스, 옴니채널 고객 접점이 필수 요구사항이 되었고, **IDC 보고서(2024)에 따르면 전 세계 기업의 67%가 "IT 거버넌스 부재가 디지털 전환 실패의 1순위 원인"이라고 응답**했다. 이는 단순히 좋은 기술을 도입하는 것을 넘어, **누가(Governance)·무엇을(Strategy)·어떻게(Operation)·얼마나(Performance) IT로 관리할 것인가**의 통합 프레임워크가 필수임을 의미한다.

```text
    +-------------------------------------------------------------+
    |            IT 경영 관리 통합 프레임워크 (2024+)              |
    +-------------------------------------------------------------+
                                |
        +-----------------------+-----------------------+
        v                       v                       v
  +----------+            +----------+            +----------+
  | 거버넌스  |            |  전략·계획 |            | 운영·관리 |
  | (WHY)    |            | (WHAT)   |            | (HOW)    |
  +----------+            +----------+            +----------+
        |                       |                       |
   +----+----+             +----+----+             +----+----+
   |COBIT 19 |             |ISP/BPR  |             |ITIL 4   |
   |ISO 38500|             |TOGAF EA |             |DevOps   |
   |COSO ERM |             |Balanced |             |SRE/관측성|
   +---------+             |Scorecard|             +---------+
                           +---------+
                                |
        +-----------------------+-----------------------+
        v                       v                       v
  +----------+            +----------+            +----------+
  | 재무관리  |            | 위험·보안  |            | 성과·측정|
  | TCO/ROI  |            | ISO 27001|             | KPI/SLA |
  | FinOps   |            | Zero Trust|             |BSC/OKR |
  +----------+            +----------+            +----------+
                                |
                                v
                  +--------------------------+
                  |   Business Value Realization |
                  |   (비즈니스 가치 실현)      |
                  +--------------------------+
```

**📢 섹션 요약 비유**: IT 경영 관리는 **자동차의 계기판·핸들·브레이크·엔진**을 통합 제어하는 **차량관리시스템(Vehicle Management System)**과 같다. 핸들(거버넌스)이 없으면 차는 엉뚱한 곳으로 가고, 브레이크(리스크관리)가 없으면 사고가 나고, 계기판(성과측정)이 없으면 현재 속도·연료 상태를 모른다. 이 4가지가 **CAN Bus(통합 통신망)**로 연결되어야 비로소 안전하고 효율적인 주행(=디지털 비즈니스 운영)이 가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 **3-Layer 아키텍처**는 **① Governance Layer(거버넌스 계층)**, **② Management Layer(관리 계층)**, **③ Operational Layer(운영 계층)**으로 구성된다. 각 계층은 **PDCA(Deming Cycle: Plan-Do-Check-Act)**, **Deming 품질경영 14포인트**, **ISO 33000 Process Assessment Model**을 기반으로 한 **연속적 개선 루프(Continuous Improvement Loop)**로 연결된다.

### 1️⃣ 거버넌스 계층 (Governance Layer) - "왜(Why) IT를 운영하는가"

거버넌스 계층은 **이사회·CEO·CFO·CIO**가 참여하는 **의사결정 계층**으로, **ISO 38500(2008년 제정, 2015년 개정) IT 거버넌스 국제표준**의 **6원칙**을 따른다:

| ISO 38500 6원칙 | 의미 | 실무 적용 예시 |
| :--- | :--- | :--- |
| ① Responsibility (책임) | IT 의사결정에 대한 명확한 책임 소재 | IT Steering Committee 구성, CIO 직속 보고 체계 |
| ② Strategy (전략) | IT 전략과 비즈니스 전략의 정렬 | ISP(Information Strategy Planning) 3개년 로드맵 |
| ③ Acquisition (취득) | IT 투자·도입의 합리적 의사결정 | CAPEX 승인 프로세스, Build vs Buy 분석 |
| ④ Performance (성과) | IT 서비스·프로젝트의 성과 측정 | SLA 99.9% 이상, BSC KPI 4관점 |
| ⑤ Conformance (준법) | 법·규정·정책 준수 | 개인정보보호법, 전자금융거래법, ISMS-P 인증 |
| ⑥ Human Behavior (인적행동) | IT 사용자의 행동·문화 고려 | 정보보안 교육, Change Management(ADKAR) |

### 2️⃣ 관리 계층 (Management Layer) - "무엇을(What) 관리할 것인가"

관리 계층은 **CISO·CTO·CDO·각 BU(사업부) IT 담당자**가 수행하며, **COBIT 2019**의 **Governance & Management Objectives(40개)**, **ITIL 4**의 **Service Value System(SVS) - 34개 Practice**, **ISO 27001:2022**의 **93개 통제항목(Annex A)**을 통합 적용한다.

### 3️⃣ 운영 계층 (Operational Layer) - "어떻게(How) 실행할 것인가"

운영 계층은 **SRE(Site Reliability Engineering)**, **DevOps**, **AIOps**, **Observability(3대 신호: Metrics·Logs·Traces)**, **Incident Management(ITIL 4 7단계 프로세스)**를 통해 **Day-2 Operation**을 수행한다.

```text
              IT 경영 관리 3-Layer 아키텍처 상세
    +--------------------------------------------------+
    |         거버넌스 계층 (ISO 38500 + COSO ERM)      |
    |  +--------------------------------------------+   |
    |  | Board of Directors / IT Steering Committee |   |
    |  |  +- Audit Committee (내부통제)              |   |
    |  |  +- Risk Committee (리스크 관리)            |   |
    |  |  +- Compensation Committee (IT 인력 보상)   |   |
    |  +--------------------------------------------+   |
    |                       | 정책·예산 승인              |
    |                       v                            |
    +--------------------------------------------------+
    |         관리 계층 (COBIT 2019 + ITIL 4)            |
    |  +--------------+  +--------------+               |
    |  | EDM 5개 목표 |  | APO 14개 목표|               |
    |  | (거버넌스)    |  | (정렬·계획·조직)|              |
    |  +--------------+  +--------------+               |
    |  | BAI 11개 목표|  | DSS 6개 목표 |               |
    |  | (구축·이행)    |  | (서비스·지원) |               |
    |  +--------------+  +--------------+               |
    |  | MEA 4개 목표 |   |  +- Managed Service         |
    |  | (평가·모니터링)|  |  +- In-House Team          |
    |  |              |   |  +- Vendor / MSP            |
    |  +--------------+  +--------------+               |
    |                       | SLA·OLA·UC 합의              |
    |                       v                            |
    +--------------------------------------------------+
    |       운영 계층 (SRE + DevOps + AIOps)             |
    |  +--------------------------------------------+   |
    |  |  SRE Golden Signals (Latency, Traffic,     |   |
    |  |   Errors, Saturation) + USE Method         |   |
    |  |  + RED Method (Rate, Errors, Duration)     |   |
    |  +--------------------------------------------+   |
    |  CI/CD Pipeline: Plan->Code->Build->Test->Release     |
    |                 ->Deploy->Operate->Monitor            |
    |  Incident Mgt: 1차->2차->3차 (P1: 15분 응답)        |
    +--------------------------------------------------+
                                |
                                v
                  +--------------------------+
                  |   Continuous Improvement  |
                  |   (Kaizen + ITIL CSI)    |
                  |   PDCA Loop (4-6주)      |
                  +--------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 거버넌스 위원회** | IT 투자·정책 최종 의사결정 | 분기별 회의, **RACI 매트릭스**(Responsible·Accountable·Consulted·Informed), 의사결정 정족수 2/3 이상 |
| **CIO + CISO + CDO** | 3대 IT 임원 거버넌스 트라이어드 | **CISO(보안)·CIO(인프라·운영)·CDO(데이터·디지털) 간 월간 협의체**, KPI를 BSC 4관점에 매핑 |
| **PMO(Project Management Office)** | 프로젝트 포트폴리오 관리 | **PPM 도구(MS Project Server, Planview, Clarity PPM)**, 프로젝트 단계별 Gate Review(Stage-Gate: Initiation->Planning->Execution->Closure) |
| **SMO(Service Management Office)** | IT 서비스 운영 거버넌스 | **ITIL 4 SVS 7개 컴포넌트(Guiding Principles->Governance->Service Value Chain->Practices->Continual Improvement)**, **Change Advisory Board(CAB)** 운영 |
| **EA(Enterprise Architecture) 팀** | 아키텍처 표준·로드맵 | **TOGAF ADM(Architecture Development Method) 8단계: Preliminary->Vision->Business->Data/App/Technology->Opportunities->Migration->Implementation Governance**, **ArchiMate 3.1** 표기법 |
| **GRC(Governance·Risk·Compliance) 시스템** | 통합 컴플라이언스 | **RSA Archer, ServiceNow GRC, SAP GRC**, 위험 등록부(Risk Register), 통제 매핑 자동화 |
| **FinOps 팀** | 클라우드 비용 최적화 | **AWS Cost Explorer, Azure Cost Management, GCP Billing**, **Reserved Instance vs Savings Plan vs Spot Instance** 최적화, **Showback/Chargeback** 모델 |
| **AIOps 플랫폼** | 운영 자동화·지능화 | **Splunk ITSI, Datadog, Dynatrace, New Relic**, ML 기반 이상탐지(Anomaly Detection), **Event Correlation**, 자동 Remediation |

**📢 섹션 요약 비유**: IT 경영 관리의 3-Layer는 **병원 운영 시스템**과 같다. **이사회(거버넌스)**는 병원의 비전·예산을 결정하고, **진료부장·간호부장(관리 계층)**은 진료과·병동 운영을 관리하며, **의사·간호사·의료기사(운영 계층)**는 실제 환자를 진찰·치료·간호한다. EMR(전자의무기록) 시스템이 이 3계층을 **실시간 데이터로 연결**하여, 경영진은 병원 전체 KPI를, 중간관리자는 진료과별 통계를, 현장 직원은 환자별 처방을 즉시 확인할 수 있다.

---

## Ⅲ. 비교 및 연결

### 1️⃣ IT 거버넌스·관리 프레임워크 비교

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 27001:2022** | **CMMI v2.0** | **TOGAF 10** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 609 / 800

<- **이전**: [608. IT 경영 관리 핵심 토픽 608번 시험 요약](/studynote/12_it_management/05_security_compliance/608_it_management_core_topic_608_exam_summary/)
**다음**: [610. IT 경영 관리 핵심 토픽 610번 시험 요약](/studynote/12_it_management/05_security_compliance/610_it_management_core_topic_610_exam_summary/) ->

---
