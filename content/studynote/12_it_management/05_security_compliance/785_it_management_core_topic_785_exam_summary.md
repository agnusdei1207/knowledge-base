+++
title = "785. IT 경영 관리 핵심 토픽 785번 시험 요약 (IT Management Core Topic 785 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019(거버넌스·관리 목표 40개)**, **ITIL 4(SVS 34개 실무 가이드)**, **TOGAF ADM(8단계 아키텍처 개발 방법론)**, **PMBOK 7(12가지 원칙·8개 성능 도메인)** 등 4대 글로벌 프레임워크를 **전략 정렬(Strategic Alignment)** 축으로 통합하여, IT 투자 ROI 평균 5~15% 향상 및 ITIL 도입 기업에서 평균 **인시던트 MTTR 40~60%**, **서비스 가용성 99.9%->99.95%** 수준의 운영 성숙도를 달성하는 통합 거버넌스 체계이다.
> 2. **가치**: McKinsey(2023) 기준 전사적 IT 거버넌스 도입 시 **IT 비용 20~30% 절감, 프로젝트 실패율 35%->12%로 감소, Time-to-Market 50% 단축, 의사결정 속도 3배 향상** 등 정량적 효과를 창출하며, ISMS-P 인증 기업은 보안사고 발생 시 **평균 복구비용 58% 절감**(한국인터넷진흥원 2022) 효과를 얻는다.
> 3. **판단 포인트**: **프레임워크 무분별한 Full-Implementation vs. 조직 성숙도 기반 단계적 도입**, **중앙집중 거버넌스(CoE) vs. 분산형 페데레이션 거버넌스(Federated COBIT)**, **전통적 Waterfall vs. 애자일/하이브리드(SAFe, Spotify Model)**, **내부 통제 우선 vs. 클라우드·외부 SaaS 확장 시 제3자 위험관리(TPRM) 강화**의 4대 트레이드오프가 핵심 의사결정 변수이며, 기술사 시험에서는 **CMMI 5단계 vs. ITIL Maturity Model**, **Balanced Scorecard 4관점**, **KPI 트리 및 CSF(핵심성공요인) 도출** 능력을 평가한다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX) 시대에 IT는 단순 비용센터(Cost Center)에서 **전략적 비즈니스 인에이블러(Strategic Enabler)**로 그 위상이 근본적으로 변화했다. 과거 2000년대 초반까지 IT 부서는 시스템 개발·운영에만 집중했으나, 2010년대 클라우드·모바일·AI가 보편화되면서 IT 자원의 73%가 외부 SaaS·PaaS·IaaS로 전환(Statista 2024)되었고, 그에 따라 **"누가, 무엇을, 어떻게 통제하는가"**라는 거버넌스 문제가 핵심 경영 이슈로 부상했다. Gartner(2023) 조사에 따르면 CIO의 67%가 "IT 성과의 비가시성"을 최대 고통 포인트로 응답했으며, board-level에서 IT 가치·위험을 정량적으로 보고·의사결정하기 위한 프레임워크의 필요성이 폭발적으로 증가했다.

```text
+----------------------------------------------------------------------+
|                    IT 경영 관리 4대 프레임워크 통합 모델                |
|                                                                      |
|   +-------------------------------------------------------------+    |
|   |         비즈니스 전략 (Corporate Strategy)                   |    |
|   |  • Porter 5 Forces  • BCG Matrix  • Ansoff Grid             |    |
|   |  • Vision/Mission  • Hoshin Kanri                            |    |
|   +------------------------+------------------------------------+    |
|                            | Ward & Peppard IS 전략 정렬              |
|   +------------------------v------------------------------------+    |
|   |              IT 거버넌스 (Governance) 최상위 계층              |    |
|   |  +--------------+  +--------------+  +------------------+   |    |
|   |  |  COBIT 2019  |  |   ISO 38500  |  |  ISO/IEC 27014   |   |    |
|   |  | 40 Governance|  | (IT Gov 국제 |  |  (거버넌스 개념)  |   |    |
|   |  |  & Management|  |   표준)      |  |                  |   |    |
|   |  |   Objectives  |  | 6 Principles  |  |  6 메커니즘       |   |    |
|   |  +-------+------+  +------+-------+  +---------+--------+   |    |
|   +----------+----------------+---------------------+------------+    |
|              |                |                     |                 |
|   +----------v----------------v---------------------v------------+    |
|   |          아키텍처 & 서비스 계층 (Middle Layer)                |    |
|   |  +------------+  +------------+  +----------+  +---------+  |    |
|   |  |  TOGAF 10  |  |   ITIL 4   |  |  CMMI v2 |  |  PMBOK 7|  |    |
|   |  | ADM 8단계  |  |  SVS·34실무|  | 5성숙단계 |  | 12원칙  |  |    |
|   |  | (Phase A-H)|  | 4D 모델    |  | 20+영역  |  | 8성능  |  |    |
|   |  +-----+------+  +-----+------+  +----+-----+  +----+----+  |    |
|   +--------+---------------+---------------+--------------+-------+    |
|            |               |               |              |            |
|   +--------v---------------v---------------v--------------v-------+    |
|   |          운영 & 실행 계층 (Operational Layer)                  |    |
|   |   DevOps | SRE | AIOps | FinOps | MLOps | SecOps | GitOps    |    |
|   +--------------------------------------------------------------+    |
|                                                                      |
|   +--------------------------------------------------------------+    |
|   |           통제 & 인증 계층 (Assurance Layer)                  |    |
|   |  ISMS-P | PIMS(ISO 27701) | PCI-DSS | SOC 2 | GDPR | PIPC  |    |
|   +--------------------------------------------------------------+    |
+----------------------------------------------------------------------+
```

**전통적 vs. 현대적 IT 관리 패러다임 비교:**

| 구분 | 2000년대 전통 모델 | 2024+ 디지털 시대 모델 |
|:---|:---|:---|
| 조직구조 | 기능별 수직 (Dev/QA/Ops 분리) | **SRE·Platform Engineering·E2E Squad** |
| 거버넌스 | 프로젝트 단위 사후 통제 | **수시·실시간 Risk-based Continuous Audit** |
| 투자관점 | CAPEX 중심 (On-Premise) | **OPEX·Subscription·Pay-as-you-go** |
| 아키텍처 | 모놀리식·소프트웨어 일체형 | **MSA(Microservices)·EKS·Service Mesh(Istio)** |
| KPI | 예산 준수율·납기 준수율 | **TTM·DORA 4대 지표·Flow Metrics** |
| 위험관리 | BCP/DRM(연 1회 훈련) | **Chaos Engineering·GameDay·Continuous DR** |
| 인력모델 | SI 아웃소싱 80% | **In-House Platform Team + AI-Augmented Dev** |

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **"도시의 통합 관제 시스템"**과 같습니다. 과거에는 각 구역(부서)이 자체적으로 전기·상하수도·소방을 관리했다면, 지금은 **지능형 교통관제(COBIT), 도시계획(TOGAF), 민원서비스 ITIL, 건설안전 PMBOK**이 4대 축으로 통합되어 실시간 통합 운영되는 스마트시티와 같은 개념입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리 시스템은 **"전략-거버넌스-아키텍처-운영-측정"**의 5계층 모델로 구성되며, 각 계층은 **PDCA(Plan-Do-Check-Act) + OODA(Observe-Orient-Decide-Act)** 사이클을 통해 지속 개선된다. 핵심 메커니즘은 **① 비즈니스 요구 -> ② IT 전략 -> ③ 거버넌스 의사결정 -> ④ 아키텍처 설계 -> ⑤ 서비스/프로젝트 실행 -> ⑥ 가치 측정 -> ⑦ 피드백**의 폐루프(Closed-Loop) 구조다.

```text
+----------------------------------------------------------------------+
|       IT 경영 관리 5계층 + RACI + CSF + KPI 연동 아키텍처             |
|                                                                      |
|  L5 +------------------------------------------------------------+   |
|     | 전략 계층  :  Hoshin Kanri X-Matrix, BSC 4관점, OKR       |   |
|     |            (재무/고객/내부프로세스/학습성장)                  |   |
|     |   CSF: "고객만족"-> KPI: "NPS ≥ 50, CSAT ≥ 4.5/5"          |   |
|     +------------------------------------------------------------+   |
|                                <-> (Cascade)                          |
|  L4 +------------------------------------------------------------+   |
|     | 거버넌스 계층 : COBIT 2019 EDM(평가/지휘/모니터) 5단계     |   |
|     |   • Evaluate(1회/년)  • Direct(정책)  • Monitor(분기)      |   |
|     |   이사회-감사-리스크-윤리위원회 RACI 매트릭스 운영           |   |
|     +------------------------------------------------------------+   |
|                                <-> (Align)                            |
|  L3 +------------------------------------------------------------+   |
|     | 아키텍처 계층 : TOGAF ADM Phase A->B->C->D->E->F->G->H           |   |
|     |   Phase A: Architecture Vision -> H: Architecture Change    |   |
|     |   Architecture Repository (ABB, SBB, ARB) 관리              |   |
|     +------------------------------------------------------------+   |
|                                <-> (Translate)                        |
|  L2 +------------------------------------------------------------+   |
|     | 서비스·프로젝트 계층 : ITIL 4 SVS + PMBOK 7                |   |
|     |   34 Practices (전략/설계/전환/운영/지원)                    |   |
|     |   8 Performance Domains: Team/Plan/Work/Delivery/Measure   |   |
|     |   Agile/Waterfall/Hybrid, SAFe 6.0 구성                     |   |
|     +------------------------------------------------------------+   |
|                                <-> (Execute)                          |
|  L1 +------------------------------------------------------------+   |
|     | 운영 계층 : DevOps + SRE + AIOps + FinOps + MLOps         |   |
|     |   SLI/SLO/Error Budget, CI/CD, GitOps(Argo CD), Chaos     |   |
|     |   DORA Metrics: DF/MTBF/MTTR/CFR                           |   |
|     +------------------------------------------------------------+   |
|                                                                      |
|  +--------------------------------------------------------------+    |
|  |  횡단(Transversal) 계층: Risk·Security·Compliance·Audit      |    |
|  |  ISO 31000(Risk) + ISO 27001(Sec) + ISO 22301(BCM) + SOX    |    |
|  +--------------------------------------------------------------+    |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **COBIT 2019** | **Governance System** (40 Objectives) | 5개 도메인(EDM, APO, BAI, DSS, MEA) × 40 Governance/Management Objectives로 구성. **EDM(평가·지휘·모니터) 5단계 사이클**이 의사결정 구조. Capability/Maturity 측정(0~5단계, ISO/IEC 15504 PAM 기반). |
| **ITIL 4** | **Service Management** (34 Practices) | **SVS(Service Value System)**: Opportunity/Demand -> Value -> Guiding Principles(7) -> Governance -> Practices(34) -> Continual Improvement. **4D 모델**(조직·정보·기술·파트너십·价值 흐름). |
| **TOGAF 10** | **Enterprise Architecture** | **ADM(Architecture Development Method) 8 Phase**: Preliminary -> A(Vision)-> B(Business)-> C(IS/App/Data)-> D(Technology)-> E(Opportunities)-> F(Migration)-> G(Implementation)-> H(Change). **Architecture Repository**: ABB(빌딩블록)·SBB(솔루션)·ARB(참조). |
| **PMBOK 7** | **Project Management** | 12
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 785 / 800

<- **이전**: [784. IT 경영 관리 핵심 토픽 784번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/784_it_management_core_topic_784_exam_summary/)
**다음**: [786. IT 경영 관리 핵심 토픽 786번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/786_it_management_core_topic_786_exam_summary/) ->

---
