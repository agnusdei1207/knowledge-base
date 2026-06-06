---
title: "IT Management Core Topic 616 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019, ITIL 4, ISO 38500 등 글로벌 IT 거버넌스·서비스 관리 프레임워크를 IT-비즈니스 정렬(Strategic Alignment), 가치 전달(Value Delivery), 위험 최적화(Risk Optimization), 자원 관리(Resource Management)의 4대 핵심 도메인에 통합 적용하여, EA(Enterprise Architecture)와 PPM(Project Portfolio Management)을 통해 디지털 전환을 체계화하는 것
> 2. **가치**: 글로벌 Forrester 연구에 따르면成熟한 IT 거버넌스 체계 도입 조직은 IT 투자 ROI를 28~35% 향상시키고, 프로젝트 실패율을 60%에서 12% 이하로 축소하며, 감사 대응 시간을 평균 72% 단축(예: SAP/Oracle ERP 구축 프로젝트 기준)함
> 3. **판단 포인트**: 중앙집중형(Centralized) vs 분산형(Decentralized) 거버넌스 모델 선택, COBIT 2019의 40개 관리목표와 7개 컴포넌트 중 조직 상황에 맞는 핵심 프로세스 선별, Agile/DevOps 환경에서 ITIL 4의 34개 Practices와 SRE(Site Reliability Engineering) 원칙 간 충돌 시 우선순위 결정, 그리고 CapEx/OpEx 균형 및 FinOps 적용 기준

---

## Ⅰ. 개요 및 필요성

IT 경영 관리는 단순한 IT 시스템 운영을 넘어, 기업의 전략적 목표와 IT 역량을 연결하는 **통합 거버넌스 체계**입니다. 4차 산업혁명(AI, IoT, 빅데이터, 클라우드) 시대를 맞아 IT는 더 이상 비용 센터(Cost Center)가 아닌 **전략적 가치 창출 센터(Value Center)**로 진화했습니다. 이에 따라 ISO/IEC 38500(2008년 최초 발행, 2015년 개정)은 이사회(Board) 수준의 IT 의사결정 거버넌스 표준으로 자리잡았으며, ISACA의 COBIT(Control Objectives for Information and Related Technologies)는 1996년 첫 출시 이후 2019년 버전에서 **거버넌스 시스템 5원칙, 40개 관리목표, 7개 컴포넌트**로 진화했습니다.

과거(Pre-2010) IT 관리는 SILO(사일로) 방식의 부서별 독립 운영, CAPEX 중심의 무조건적 인프라 투자, 그리고 "Build and Run" 분리 모델이 지배적이었습니다. 그러나 디지털 전환(DX, Digital Transformation) 시대에는 비즈니스와 IT의 경계가 모호해지면서, **양방향 정렬(Bi-directional Alignment)**이 필수적이 되었으며, 이를 위해 비즈니스 역량 모델(Business Capability Map)과 IT 역량 매핑이 EA(Enterprise Architecture) 기반 TOGAF(The Open Group Architecture Framework) ADM(Architecture Development Method) 사이클을 통해 구현됩니다.

```text
+------------------------------------------------------------------+
|          IT 경영 관리 통합 거버넌스 참조 모델(RGM)               |
+------------------------------------------------------------------+
|                                                                  |
|  +----------------+      +----------------+      +----------+  |
|  |  전략 계층     |      |  거버넌스 계층  |      | 실행계층 |  |
|  |  (Strategy)    | ----> |  (Governance)   | ----> |(Operate) |  |
|  |                |      |                |      |          |  |
|  | • 비즈니스전략 |      | • 이사회        |      |• DevOps  |  |
|  | • IT 전략      |      | • IT steering   |      |• ITIL 4  |  |
|  | • DX 비전      |      |   Committee    |      |• SRE     |  |
|  | • ESG/지속가능 |      | • CIO/CDO/CAIO  |      |• FinOps  |  |
|  +--------+-------+      +--------+-------+      +----+-----+  |
|           |                       |                    |         |
|           v                       v                    v         |
|  +------------------------------------------------------------+ |
|  |         통합 프레임워크 코어 (Integrated Framework Core)   | |
|  |  +----------+  +----------+  +----------+  +----------+  | |
|  |  | COBIT    |  | ITIL 4   |  | ISO      |  | TOGAF    |  | |
|  |  | 2019     |  | SVS      |  | 38500    |  | ADM      |  | |
|  |  |(40 GO)   |  |(34 Prac.)|  |(6 Princ.)|  |(8 Phase) |  | |
|  |  +----------+  +----------+  +----------+  +----------+  | |
|  +------------------------------------------------------------+ |
|                              |                                   |
|                              v                                   |
|  +----------------------------------------------------------+   |
|  |  핵심 가치 흐름(Value Flow) & KPI 대시보드              |   |
|  |  MTTR, MTBF, SLA(99.95%), CSAT, NPS, TCO, ROI, NPV   |   |
|  +----------------------------------------------------------+   |
+------------------------------------------------------------------+
```

위 다이어그램은 Henderson & Venkatraman의 **Strategic Alignment Model(SAM, 1993)**과 Luftman의 **Strategic Alignment Maturity Model(SAMM, 2004, 5단계 30개 속성)**을 기반으로, 전략-거버넌스-실행 3계층이 통합 프레임워크 코어(COBIT, ITIL, ISO, TOGAF)를 통해 KPI로 측정되는 구조를 보여줍니다.

**기존 패러다임 vs 신규 패러다임 비교**:
- **Before (2000년대)**: 부서별 독립 IT, CAPEX 중심 투자 70%+, 프로젝트 성공률 32%(CHAOS Report 2014 Standish Group), 평균 TCO 5년 주기 갱신, IT 인력 대비 100:1(사용자) 비율
- **After (2020년대)**: 클라우드 네이티브 + SaaS 중심, OPEX 전환 60%+, Agile/DevOps 적용 프로젝트 성공률 58%, SaaS 기반 지속적 업데이트(Continuous Update), IT 인력 대비 50:1 + 셀프서비스 + AI 자동화, FinOps·GreenOps·DevSecOps 통합 거버넌스

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **도시의 도시계획(Urban Planning)**과 같습니다. 건물 하나(시스템)만 잘 짓는 것이 아니라, 도로·상하수도·전기·통신 인프라(거버넌스)를 전체적으로 설계해야 시민(비즈니스)들이 삶의 질(가치)을 누릴 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 크게 **5개 계층**으로 구성됩니다. 각 계층은 PDCA(Plan-Do-Check-Act) 또는 OODA(Observe-Orient-Decide-Act) 루프를 통해 연속적 개선을 수행합니다.

```text
+------------------------------------------------------------------+
|        IT 경영 관리 5계층 아키텍처 (5-Layer Architecture)        |
+------------------------------------------------------------------+
|                                                                  |
|  L1. 전략·방향 계층 (Strategy & Direction Layer)                 |
|  +----------------------------------------------------------+   |
|  | 기업 미션·비전 -> IT 원칙 -> IT 전략 맵(Strategy Map)     |   |
|  | BSC 4관점(재무/고객/프로세스/학습성장) + OKR 정렬         |   |
|  | 산출물: IT Strategy Plan, IT Charter, 3-Year Roadmap     |   |
|  +----------------------------------------------------------+   |
|                              v                                   |
|  L2. 거버넌스·의사결정 계층 (Governance & Decision Layer)        |
|  +----------------------------------------------------------+   |
|  | • IT Steering Committee(월 1회, CIO+사업부 이사)         |   |
|  | • Architecture Review Board(분기 1회)                    |   |
|  | • Change Advisory Board(CAB, 주 1회, ITIL)              |   |
|  | • Risk & Compliance Committee(월 1회)                   |   |
|  | 결정 사항: 투자 승인, 표준 채택, 우선순위 조정           |   |
|  +----------------------------------------------------------+   |
|                              v                                   |
|  L3. 프로세스·운영 계층 (Process & Operation Layer)              |
|  +----------------------------------------------------------+   |
|  | +----------------+  +----------------+  +-------------+ |   |
|  | | 계획(Plan)     |  | 구축(Deliver)  |  | 운영(Run)   | |   |
|  | | • PPM          |  | • Agile/DevOps |  | • ITIL 4    | |   |
|  | | • Portfolio    |  | • CI/CD        |  | • SRE       | |   |
|  | | • Demand Mgmt  |  | • IaC(Terraform)| | • Monitoring| |   |
|  | +----------------+  +----------------+  +-------------+ |   |
|  +----------------------------------------------------------+   |
|                              v                                   |
|  L4. 기술·플랫폼 계층 (Technology & Platform Layer)              |
|  +----------------------------------------------------------+   |
|  | 클라우드(AWS/Azure/GCP) + 하이브리드 + 엣지 + SaaS     |   |
|  | 데이터 플랫폼: Lakehouse(Iceberg/Delta/Hudi) + Kafka     |   |
|  | AI/ML: MLOps + LLM Ops + Vector DB(Pinecone/Weaviate) |   |
|  +----------------------------------------------------------+   |
|                              v                                   |
|  L5. 측정·개선 계층 (Measure & Improve Layer)                    |
|  +----------------------------------------------------------+   |
|  | KPI 대시보드 + CMMI/COBIT Maturity Model(5단계)         |   |
|  | PI/Retrospective + PDCA + Continual Improvement         |   |
|  +----------------------------------------------------------+   |
+------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 거버넌스 시스템** | IT 의사결정의 원칙·목표·컴포넌트 제공 | 5개 원칙(Stakeholder Value, Holistic Approach, Dynamic Governance, Distinct Governance vs Management, Fit-for-Purpose), 40개 관리목표(EDM: 5, APO: 14, BAI: 11, DSS: 6, MEA: 4), 7개 컴포넌트(Principles, Policies, Processes, Organizational Structures, Information, People/Skills, Culture), 능력수준 0~5 (PA: Process Attribute 6개, 0~100% 달성률) |
| **ITIL 4 서비스 가치 시스템(SVS)** | 서비스 라이프사이클 전체 통합 관리 | 34개 Practices(General Mgmt: 14, Service Mgmt: 17, Technical Mgmt: 3), Service Value Chain(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support), 4가지 차원(Organization/People, Information/Technology, Partners/Suppliers, Value Streams/Processes), Guiding Principles(7개: Focus on Value, Start Where You Are, Progress Iteratively, etc.) |
| **ISO/IEC 38500 IT 거버넌스** | 이사회 수준의 IT 의사결정 표준 | 6개 원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior), Evaluate->Direct->Monitor(EDM) 3단계 사이클, 2008년 최초->2015년 개정, ISO/IEC 27001(보안), 20000(서비스), 21500(프로젝트)와 연계 |
| **TOGAF ADM** | EA 개발·전환·거버넌스 방법론 | Preliminary Phase -> A(비전) -> B,C,D(BA/DA/TA) -> E,F(Opportunity/Migration) -> G(Implementation) -> H(Change Mgmt) -> Requirements Mgmt(연속), ADM Cycle Iteration 1~N, Architecture Repository(ARB+ABBV+ADR+Solutions Continuum) |
| **KPI 측정 체계** | 정량적 성과 측정 및 의사결정 지원 | BSC 4관점 25~30개 KPI, OKR(Objective+Key Results 분기별), COBIT Goals Cascade(13개 Enterprise Goals -> Alignment Goals -> 40 Mgmt Goals), NPV/IRR/Payback Period(투자), MTTR/MTBF/SLA(운영), CSAT/NPS(고객) |

**핵심 원리 상세**:
- **COBIT 2019의 Goals Cascade**: 13개 Enterprise Goals(예: EG01: Portfolio of competitive products/services) -> 13개 Alignment Goals(예: AG01: IT compliance and support for business) -> 40개 Management Goals -> 이 매트릭스(M)를 통해 Primary(Rank 1) / Secondary(Rank 2~3) 관계를 정의
- **ITIL 4의 4가지 차원 모델**: 모든 서비스는 4가지 차원(Information Technology, Organization People, Value Stream Process, Partner Supplier)을 모두 고려해야 하며, 누락 시 "PESTEL" 등 외부 환경 변화에 취약
- **ISO 38500의 EDM 루프**: Evaluate(현황 평가, 분기) -> Direct(방향 제시, 월간) -> Monitor(성과 모니터링, 주간/일간)으로 실행되며, RACI 매트릭스(Responsible, Accountable, Consulted, Informed)를 통해 책임 소재 명확화
- **TOGAF의 Stakeholder Management**: Preliminary Phase에서 50+ 이해관계자 식별, ADM Phase A~H 각 단계별 Stakeholder Map 갱신, Architecture Views(4종: Business/Application/Data/Technology) 및 Viewpoints(예: Developer, Operator, Security) 분리

- **📢 섹션 요약 비유**: 5계층 아키텍처는 마치 **인간의 신경계**와 같습니다. L1(전략)이 대뇌 피질, L2(거버넌스)가 전두엽 의사결정, L3
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 616 / 800

<- **이전**: [615. IT 경영 관리 핵심 토픽 615번 시험 요약](/studynote/12_it_management/05_security_compliance/615_it_management_core_topic_615_exam_summary/)
**다음**: [617. IT 경영 관리 핵심 토픽 617번 시험 요약](/studynote/12_it_management/05_security_compliance/617_it_management_core_topic_617_exam_summary/) ->

---
