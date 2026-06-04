+++
title = "614. IT 경영 관리 핵심 토픽 614번 시험 요약 (IT Management Core Topic 614 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, ISO 38500, ISO 27001 등 글로벌 거버넌스 프레임워크를 기반으로, **전략(Strategy) -> 아키텍처(Architecture) -> 구현(Implementation) -> 운영(Operation) -> 감사(Audit)**의 5단계 가치사슬(Value Chain)을 통해 IT 투자 대비 비즈니스 가치(ROI, NPV, IRR, Payback Period)를 극대화하는 경영 활동입니다.
> 2. **가치**: Gartner에 따르면 효과적인 IT 거버넌스 체계 구축 시 IT 투자 대비 ROI가 평균 **230% 향상**되고, 프로젝트 실패율은 **McKinsey 기준 35% -> 15% 이하**로 감소하며, 정보시스템 감리(IS Audit) 수행 시 보안 사고 예방 효과가 **연간 약 1,400만 달러(IBM Cost of Data Breach 2023 기준)** 규모입니다.
> 3. **판단 포인트**: 기술사는 **"Governance-Body(COBIT 40개 관리목표 중 어디에 매핑) ↔ Process(ITIL 4 34개 실무) ↔ Architecture(TOGAF ADM 8단계) ↔ Risk(ISO 27005 7단계) ↔ Audit(감리 11개 영역)"**의 5축을 어떻게 통합 설계하느냐가 핵심이며, 특히 국내 전자금융감독규정, 개인정보보호법, 클라우드컴퓨팅법, AI 기본법(2026 시행) 등 규제 환경 변화를 아키텍처 결정에 반영해야 합니다.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리(IT Management)는 단순한 IT 운영 관리를 넘어, 기업의 비즈니스 전략과 IT 자산을 통합 관리하여 **가치 창출(Value Creation)**, **리스크 통제(Risk Control)**, **자원 최적화(Resource Optimization)**의 3대 목표를 달성하는 경영 과학입니다. 한국정보통신기술협회(TTA)와 정보통신산업진흥원(NIPA)의 통계에 따르면 국내 기업의 약 68%가 IT 거버넌스 체계 부재로 인한 중복 투자, 프로젝트 실패, 보안 사고를 경험하고 있으며, 디지털 전환(DX) 가속화로 인해 이 비중은 매년 12%씩 증가 추세입니다.

특히 2024년 이후 **AI 거버넌스(AI Governance)**, **클라우드 컴플라이언스**, **ESG-ICT 통합** 등 새로운 경영 이슈가 부상하면서, 전통적인 COBIT 5/ITIL v3 체계에서 **COBIT 2019 + ITIL 4 + ISO 38500 + NIST CSF 2.0 + ISO 42001(AI 경영체계)**의 다중 프레임워크 통합 거버넌스(Hybrid Governance)로 패러다임이 전환되고 있습니다.

```text
+--------------------------------------------------------------------+
|         IT 경영 관리 5단계 가치사슬 (IT Value Chain)                |
|                                                                    |
|   +---------+    +---------+    +---------+    +---------+    +--------+
|   | Strategy| --> |Architecture| -->|Implement| -->|Operation| --> | Audit  |
|   | 전략기획 |    | EA설계    |    | 구축/개발 |    | ITIL운영 |    | 감리   |
|   +---------+    +---------+    +---------+    +---------+    +--------+
|        |              |              |              |              |
|        v              v              v              v              v
|   +------------------------------------------------------------+
|   |  Governance Layer (COBIT 2019 / ISO 38500)                  |
|   |  +---------+  +---------+  +---------+  +---------+        |
|   |  |  EDM    |  |  APO    |  |  BAI    |  |  DSS    |  MEA   |
|   |  | Evaluate|  | Align   |  | Build   |  | Deliver | Monitor|
|   |  | Direct  |  | Plan    |  | Acquire |  | Service |Evaluate|
|   |  | Monitor |  | Organize|  | Implement| | Support |        |
|   |  +---------+  +---------+  +---------+  +---------+        |
|   +------------------------------------------------------------+
|        |              |              |              |              |
|        v              v              v              v              v
|   +------------------------------------------------------------+
|   |  Cross-Cutting Concerns: Risk / Security / Compliance      |
|   |  (ISO 27001, 27005, 31000, NIST CSF 2.0, PIPA, ISMS-P)     |
|   +------------------------------------------------------------+
|        |
|        v
|   +------------------------------------------------------------+
|   |  Stakeholders: CEO / CIO / CISO / CFO / 사업부서 / 고객    |
|   +------------------------------------------------------------+
+--------------------------------------------------------------------+
```

**구(舊) 패러다임 vs 신(新) 패러다임 비교**:
- **구 패러다임 (1990~2010)**: IT는 비용센터(Cost Center) -> CIO는 시스템 운영자 -> 개별 시스템 단위 관리(Siloed Management) -> 사후 대응적 감리
- **신 패러다임 (2010~현재)**: IT는 가치동반자(Value Co-Creator) -> CIO는 전략 임원 -> EA 기반 통합 거버넌스 -> 실시간 리스크 모니터링(GRC 플랫폼)

- **📢 섹션 요약 비유**: IT 경영 관리는 **배의 항해**와 같습니다. COBIT는 항해 규칙(국제해상충돌예방규칙), TOGAF는 선박 설계도, ITIL은 기관실 운영 매뉴얼, ISO 27001은 안전 장비, 감리는 정기 검사입니다. 항해사(기술사)가 이 모든 것을 조율해야 안전한 항해가 가능합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 **3-레이어 거버넌스 모델(3-Layer Governance Model)**로 구성됩니다. 최상위 **의사결정층(Governance Layer)**에서 이사회/경영진이 정책과 방향을 결정하고, 중간 **관리층(Management Layer)**에서 COBIT 2019의 40개 관리목표(Management Objective)와 ITIL 4의 34개 실무 프로세스를 통해 통제 활동을 수행하며, 최하위 **실행층(Execution Layer)**에서 실제 시스템과 프로세스가 운영됩니다.

```text
+---------------------------------------------------------------------+
|         3-레이어 IT 거버넌스 아키텍처 (Detailed View)              |
|                                                                     |
|  Layer 1: 의사결정층 (Governance / Decision Layer)                  |
|  +---------------------------------------------------------------+ |
|  |  [이사회] -> [IT전략위원회] -> [정보보호위원회] -> [ESG위원회]   | |
|  |     |             |                  |               |       | |
|  |     v             v                  v               v       | |
|  |  +--------+  +----------+    +----------+    +----------+   | |
|  |  |IT정책  |  |투자우선순위|   |보안정책  |    |Green IT  |   | |
|  |  |표준/지침|  |Portfolio  |    |ISMS-P    |    |정책      |   | |
|  |  +--------+  +----------+    +----------+    +----------+   | |
|  +---------------------------------------------------------------+ |
|                              ^                                      |
|                              | (Feedback Loop)                     |
|  Layer 2: 관리층 (Management Layer)                                |
|  +---------------------------------------------------------------+ |
|  |  COBIT 2019 도메인 (5개 도메인 / 40개 관리목표)               | |
|  |  +---------+  +---------+  +---------+  +---------+  +-----+| |
|  |  |  EDM    |  |  APO    |  |  BAI    |  |  DSS    |  | MEA || |
|  |  |  5개    |  |  14개   |  |  11개   |  |  6개    |  | 4개 || |
|  |  +---------+  +---------+  +---------+  +---------+  +-----+| |
|  |  + ITIL 4 Service Value System (SVS)                          | |
|  |  + TOGAF ADM (8단계 사이클)                                   | |
|  |  + ISO 27001/27005 통제 항목 (114개 Annex A 통제)            | |
|  +---------------------------------------------------------------+ |
|                              ^                                      |
|                              |                                      |
|  Layer 3: 실행층 (Execution Layer)                                  |
|  +---------------------------------------------------------------+ |
|  |  +----------+  +----------+  +----------+  +----------+     | |
|  |  |프로젝트  |  |서비스    |  |인프라    |  |데이터    |     | |
|  |  |포트폴리오|  |데스크    |  |(Cloud/   |  |거버넌스  |     | |
|  |  |(PfMP)   |  |(ITSM)   |  | On-Prem) |  |(DAMA)   |     | |
|  |  +----------+  +----------+  +----------+  +----------+     | |
|  |  +----------+  +----------+  +----------+  +----------+     | |
|  |  |DevOps   |  |SecOps    |  |MLOps     |  |FinOps    |     | |
|  |  |파이프라인|  |(SIEM/SOAR)| |(AI거버넌스)| |(클라우드)|     | |
|  |  +----------+  +----------+  +----------+  +----------+     | |
|  +---------------------------------------------------------------+ |
|                              ^                                      |
|                              |                                      |
|  Layer 4: 측정/보고층 (Measurement & Reporting)                     |
|  +---------------------------------------------------------------+ |
|  |  KPI 대시보드 / GRC 플랫폼 / BSC-IT / OKR-IT / Risk Register| |
|  |  (ServiceNow GRC, RSA Archer, SAP GRC, 자체 BI 대시보드)    | |
|  +---------------------------------------------------------------+ |
+---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** | IT 거버넌스/관리 프레임워크 | ISACA 발표, 5개 도메인(EDM/APO/BAI/DSS/MEA) × 40개 관리목표. **Focus Area**(예: 사이버보안, DevOps, 디지털거버넌스)를 통해 조직 상황에 맞게 커스터마이징. **Cascade Goals** 메커니즘으로 기업 목표 -> IT 목표 -> Enabler 목표로 연계 |
| **ITIL 4** | IT 서비스 관리(ITSM) 프레임워크 | AXELOS(현재 PeopleCert) 발표, 7가지 가이드 원칙(Guidance Principle), **34개 실무(Practice)**. **Service Value System(SVS)**은 Opportunity/Demand -> Value -> Service Value Chain(Plan/Engage/Design & Transition/Obtain/Build/Deliver & Support/Improve) 구조 |
| **TOGAF 10** | 엔터프라이즈 아키텍처(EA) 방법론 | The Open Group 발표, **ADM(Architecture Development Method)** 8단계: Preliminary -> Vision -> Business Architecture -> Information Systems -> Technology -> Opportunities & Solutions -> Migration Planning -> Implementation Governance -> Change Management. **ArchiMate 3.2** 표기법 사용 |
| **ISO 38500:2015** | IT 거버넌스 국제표준 | 이사회 수준 거버넌스 표준, 6원칙(책임/전략/획득/성과/규칙/인적행위) × 3모델(Direct/Monitor/Evaluate) 매트릭스. **Evaluate-Direct-Monitor** 사이클이 COBIT EDM과 매핑 |
| **ISO 27001:2022** | 정보보호 경영체계(ISMS) | Annex A 93개 통제 항목(기존 114개에서 통합), 4관점(조직/인적/물리/기술). **PDCA 사이클** + Statement of Applicability(SoA) + Risk Treatment Plan(RTP) 필수 산출물 |
| **PMO(Project Management Office)** | 프로젝트 포트폴리오 관리 | **PfMP(Portfolio Management)** + **PgMP(Program Management)** + **PMP(Project Management)** 3계층. 한국정보화진흥원(KIAT)의 PMO 운영 가이드라인: Strategic/Steering/Operational 3단계 모델 |
| **GRC 플랫폼** | 통합 거버넌스/리스크/컴플라이언스 | ServiceNow GRC, SAP GRC, RSA Archer, OneTrust, LogicGate, IBM OpenPages. **단일 뷰(Single Pane of Glass)**로 리스크/KPI/통제효율성 모니터링 |
| **BSC-IT(Balanced Scorecard)** | IT 성과 측정 | Norton/Kaplan BSC를 IT에 적용, 4관점(재무/고객/내부프로세스/학습성장) × 4~6개 KPI. 예: 시스템 가용성 99.95%, MTTR 30분 이내, CSAT 4.5/5.0, ROI 200% |

**핵심 원리 상세 - COBIT 2019 Cascade Goals 메커니즘**:

```
기업 목표 (13개)
  +- 01 포트폴리오의 경쟁 제품/서비스
  +- 02 리스크 관리
  +- 03 ... (생략)
  +- 13 제품/서비스 비즈니스 기능 디지털화

       v Alignment
IT 목표 (13개)
  +- 01 IT의 비즈니스 전략과의 정렬
  +- 02 IT 조직 및 역량 관리
  +- 03 ... (생략)
  +- 13 보안 및 컴플라이언스, 데이터 관리

       v Alignment
Enabler 목표 (40개 = 관리목표와 1:1 매핑)
  +- EDM01 거버넌스 프레임워크 설정/유지
  +- APO12 리스크 관리
  +- BAI03 솔루션 아키텍처 관리
  +- DSS02 서비스 요청 및 사고 관리
  +- MEA01 성과 및 컴플라이언스 모니터링
```

**핵심 원리 상세 - ITIL 4 Service Value Chain**:

```
[Opportunity/Demand] -> [Value] -> [Service Value Chain Activity]
                                        |
                +-------------+---------+---------+-------------+
                v             v         v         v             v
              Plan        Engage   Design &   Obtain/Build  Deliver/  Improve
              전략/포트    이해관    Transition  자원/역량   Support
              폴리오     계자와    (설계/검증)                (운영)   (지속개선)
              계획        협상
```

- **📢 섹션 요약 비유**: 3-레이어 거버넌스는 **도시 행정 시스템**과 같습니다. 시议会(Governance)가 법률을 만들고, 시청 관리국(Management)이 부서별로 집행 지침을 내리며
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 614 / 800

<- **이전**: [613. IT 경영 관리 핵심 토픽 613번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/613_it_management_core_topic_613_exam_summary/)
**다음**: [615. IT 경영 관리 핵심 토픽 615번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/615_it_management_core_topic_615_exam_summary/) ->

---
