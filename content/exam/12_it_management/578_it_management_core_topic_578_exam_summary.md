---
title: "IT Management Core Topic 578 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

# 578. IT 경영 관리 핵심 토픽 578번 시험 요약 (IT Management Core Topic 578 Exam Summary)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 디지털 전환(DX) 시대의 IT 거버넌스는 **COBIT 2019**의 거버넌스/관리 체계(EDM-evaluate, direct, monitor) 5개 영역 40개 프로세스와 **ITIL 4**의 34개 practices, **ISO/IEC 38500**의 6개 원칙을 통합하여 기업 IT 의사결정 구조(Value-Optimization, Risk-Optimization, Resource-Optimization)를 정합적으로 운영하는 프레임워크 결합 전략이다.
> 2. **가치**: 글로벌 기업 사례(코카콜라 3.0, 마이다스, BMW Digital Twin)에서 검증된 DX-거버넌스 통합 모델은 **ROI 24% 향상**, **TTM(Time-to-Market) 35% 단축**, **EVA(Economic Value Added) 0.8% 개선**, 그리고 **IT 예산 운영 효율 28% 향상**의 정량적 성과를 입증하였다.
> 3. **판단 포인트**: **Bimodal IT(Plan/Build/Run + Explore/Experiment)**와 **Two-Speed Architecture** 간의 트레이드오프, **Centralized CoE(Center of Excellence)**와 **Federated 모델**의 비용/속도/표준화 균형, 그리고 **MSA(Microservices Architecture)** 전환 시 **Conway's Law**에 따른 팀 토폴로지(Team Topologies) 재설계가 핵심 설계 결정 사항이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 디지털 전환 패러다임의 전환

정보관리 기술사 578번은 **IT 거버넌스와 디지털 전환 전략**의 통합적 접근을 평가하는 핵심 문항이다. 2010년대 이후 클라우드, 빅데이터, AI/ML, IoT, Web3.0 등 4차 산업혁명 기술의 폭발적 성장으로 인해 전통적인 IT 관리 체계로는 한계가 명확해졌다.

| 시대 구분 | 기간 | 핵심 패러다임 | 거버넌스 모델 | 기술 스택 |
|:---|:---:|:---|:---|:---|
| **Mainframe Era** | 1960~1980 | 중앙집중형 일괄처리 | 중앙 통제형 | COBOL, JCL, CICS |
| **Client-Server** | 1990~2000 | 분산 컴퓨팅 | IT Steering Committee | ERP, CRM, RDBMS |
| **Web-Centric** | 2000~2010 | 서비스 지향 | ITIL v2/v3 기반 ITSM | SOA, EAI, ESB |
| **Cloud/Mobile** | 2010~2020 | 양방향 확장성 | COBIT 5 + ITIL 2011 | IaaS, SaaS, NoSQL |
| **DX/AI Era** | 2020~현재 | 지능형 자동화 | **COBIT 2019 + ITIL 4 + ISO 38500** 통합 | MSA, Kubernetes, MLOps, AI Governance |

### 1.2 시스템 아키텍처 개념도 (DX 거버넌스 통합 모델)

```text
+-------------------------------------------------------------------------+
|                  Enterprise DX Governance Framework                     |
|                                                                         |
|  +------------------------------------------------------------------+  |
|  |  Layer 1: Strategic Layer (전략 계층)                            |  |
|  |  +--------------+  +--------------+  +--------------+          |  |
|  |  | Board/CxO    |  | Strategy      |  | Enterprise   |          |  |
|  |  | Committee    |<-->| Office        |<-->| Architecture  |          |  |
|  |  | (의사결정)    |  | (BSC/KPI)     |  | (TOGAF/Zachman)|         |  |
|  |  +--------------+  +--------------+  +--------------+          |  |
|  +------------------------------------------------------------------+  |
|                              v^ 방향성/모니터링                          |
|  +------------------------------------------------------------------+  |
|  |  Layer 2: Governance Layer (거버넌스 계층)                        |  |
|  |  +------------------------+  +------------------------+         |  |
|  |  |  COBIT 2019 EDM 5영역  |  |  ISO/IEC 38500 6원칙    |         |  |
|  |  |  • Evaluate(평가)      |  |  • Responsibility       |         |  |
|  |  |  • Direct(지시)        |  |  • Strategy             |         |  |
|  |  |  • Monitor(모니터)     |  |  • Acquisition          |         |  |
|  |  |  EDM01~EDM05           |  |  • Performance          |         |  |
|  |  |  APO/BAI/DSS/MEA 14    |  |  • Conformance          |         |  |
|  |  |  도메인 × 40 Process   |  |  • Human Behavior       |         |  |
|  |  +------------------------+  +------------------------+         |  |
|  +------------------------------------------------------------------+  |
|                              v^ 시행/측정                                |
|  +------------------------------------------------------------------+  |
|  |  Layer 3: Management Layer (관리 계층)                            |  |
|  |  +--------------+  +--------------+  +--------------+          |  |
|  |  | ITIL 4 SVS   |  | ISO 27001    |  | ISO 20000    |          |  |
|  |  | 34 Practices |  | ISMS         |  | ITSM         |          |  |
|  |  | • Service    |  | • A.5~A.18   |  | • 10 clauses |          |  |
|  |  |   Value Sys  |  |   114통제    |  | • PDCA Cycle |          |  |
|  |  | • 7 Guiding  |  | • Risk-based |  | • Service    |          |  |
|  |  |   Principles |  |   Approach   |  |   Lifecycle  |          |  |
|  |  +--------------+  +--------------+  +--------------+          |  |
|  +------------------------------------------------------------------+  |
|                              v^ 실행/자동화                                |
|  +------------------------------------------------------------------+  |
|  |  Layer 4: Operational Layer (운영 계층)                           |  |
|  |  +----------+ +----------+ +----------+ +----------+ +------+ |  |
|  |  | DevOps   | | MLOps    | | DataOps  | | FinOps   | | AIOps| |  |
|  |  | CI/CD    | | Pipeline | | Catalog  | | Cost Opt | |K8s   | |  |
|  |  | ArgoCD   | | Kubeflow | | Unity    | | Cloudability| |Prom | |  |
|  |  +----------+ +----------+ +----------+ +----------+ +------+ |  |
|  +------------------------------------------------------------------+  |
+-------------------------------------------------------------------------+
```

### 1.3 기존 체계 대비 한계점

기존의 **ITIL v3**(2011) 기반의 26개 프로세스는 **서비스 라이프사이클**(Strategy->Design->Transition->Operation->CSI) 중심의 폐쇄형 모델로, **빠른 비즈니스 변화 대응**과 **실시간 가치 측정**에 한계가 있었다. 또한 **COBIT 5**(2012)는 5개 도메인(EDM, APO, BAI, DSS, MEA)의 37개 프로세스로 구성되었으나, **클라우드·AI·자동화** 시대의 거버넌스 요구를 반영하지 못한다는 평가를 받았다.

이에 **COBIT 2019**는 40개 프로세스로 확장하고 **Focus Area**(예: DevOps, Cybersecurity, Digital Transformation, AI) 메커니즘을 도입하여 유연성을 강화하였으며, **ITIL 4**(2019)는 **Service Value System(SVS)** 기반으로 **34개 Practices**(일반 관리 14개 + 서비스 14개 + 기술 6개)를 통해 **Value Co-Creation** 관점으로 전환되었다.

- **📢 섹션 요약 비유**: 거버넌스 통합 모델은 마치 **도시의 교통 시스템**과 같다. 전략 계층은 도시계획위원회, 거버넌스 계층은 경찰청·교통공단, 관리 계층은 도로 설계도, 운영 계층은 실제 신호등·차량이다. 이 중 하나라도 통합되지 않으면 정체와 사고가 발생한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 COBIT 2019 핵심 구조

COBIT 2019는 **Governance System**과 **Governance Framework**의 이중 구조를 가지며, **40개 프로세스**는 다음 5개 도메인에 분포한다.

| 도메인 | 코드 범위 | 프로세스 수 | 핵심 목적 | 기술사 출제 빈도 |
|:---|:---:|:---:|:---|:---:|
| **EDM** (Evaluate, Direct, Monitor) | EDM01~05 | 5 | 거버넌스 의사결정 | ★★★★★ |
| **APO** (Align, Plan, Organize) | APO01~14 | 14 | 전략 정렬 및 계획 | ★★★★★ |
| **BAI** (Build, Acquire, Implement) | BAI01~11 | 11 | 솔루션 구축 및 도입 | ★★★★☆ |
| **DSS** (Deliver, Service, Support) | DSS01~06 | 6 | 서비스 제공 및 지원 | ★★★☆☆ |
| **MEA** (Monitor, Evaluate, Assess) | MEA01~04 | 4 | 성과 측정 및 평가 | ★★★★☆ |

### 2.2 ITIL 4 Service Value System (SVS) 아키텍처

```text
                    +------------------------------+
                    |   Opportunity/Demand (기회/수요)|
                    |   (Market, Customer, Tech)   |
                    +--------------+---------------+
                                   v
        +-------------------------------------------------+
        |          Service Value System (SVS)               |
        |  +---------------------------------------------+  |
        |  | 1. Plan (계획)                                |  |
        |  |    - Vision, Mission, Strategy              |  |
        |  |    - Portfolio Prioritization (WSJF)        |  |
        |  +---------------------------------------------+  |
        |  | 2. Engage (참여)                             |  |
        |  |    - Stakeholder Management                  |  |
        |  |    - Customer Journey Mapping                |  |
        |  +---------------------------------------------+  |
        |  | 3. Design & Transition (설계·전환)           |  |
        |  |    - Service Blueprint                       |  |
        |  |    - SLO/SLI/SLA 설계                        |  |
        |  |    - Change Enablement                       |  |
        |  +---------------------------------------------+  |
        |  | 4. Obtain/Build (획득·구축)                   |  |
        |  |    - Sourcing Strategy (Build/Buy/Borrow)    |  |
        |  |    - Architecture (Cloud, MSA, Serverless)   |  |
        |  +---------------------------------------------+  |
        |  | 5. Deliver & Support (제공·지원)             |  |
        |  |    - Incident/Problem Mgmt (4-3-3 가이드)   |  |
        |  |    - Service Desk (AI Chatbot)               |  |
        |  |    - Monitoring (SRE Golden Signal)          |  |
        |  +---------------------------------------------+  |
        |  | 6. Improve (개선)                             |  |
        |  |    - CSI Register                            |  |
        |  |    - Continual Improvement Model             |  |
        |  +---------------------------------------------+  |
        |              ^ 7 Guiding Principles ^            |
        |  ① Focus on Value  ② Start Where You Are        |
        |  ③ Progress Iteratively  ④ Collaborate           |
        |  ⑤ Think & Work Holistically  ⑥ Keep It Simple  |
        |  ⑦ Optimize & Automate                            |
        +------------------+------------------------------+
                           v
        +-------------------------------------------------+
        |           Value (가치) Outcome                    |
        |  +---------+ +---------+ +---------+ +--------+|
        |  | Current | | Future  | | Utility | |Warranty||
        |  | Org.    | | Org.    | |(기능)   | |(보증)  ||
        |  +---------+ +---------+ +---------+ +--------+|
        +-------------------------------------------------+
                           v
                    +------------------------------+
                    |  Stakeholder Value (이해관계자)|
                    |  Customer / User / Sponsor   |
                    +------------------------------+
```

### 2.3 핵심 구성 요소 및 기술 상세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 | 정량 지표 (KPI) |
|:---|:---|:---|:---|
| **Strategy Office (전략실)** | IT-비즈니스 정렬 | **BSC(Balanced Scorecard)** 4관점(Financial/Customer/Internal/Learning) + **OKR(Objectives & Key Results)** 계층화, **
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 578 / 800

<- **이전**: [577. IT 경영 관리 핵심 토픽 577번 시험 요약](/studynote/12_it_management/05_security_compliance/577_it_management_core_topic_577_exam_summary/)
**다음**: [579. IT 경영 관리 핵심 토픽 579번 시험 요약](/studynote/12_it_management/05_security_compliance/579_it_management_core_topic_579_exam_summary/) ->

---
