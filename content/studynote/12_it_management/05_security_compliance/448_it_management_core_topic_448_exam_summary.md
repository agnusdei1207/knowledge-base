+++
title = "448. IT 경영 관리 핵심 토픽 448번 시험 요약 (IT Management Core Topic 448 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019** 거버넌스 체계, **ITIL 4** 서비스 가치 사슬, **TOGAF** EA 프레임워크를 통합하여 **Strategy -> Portfolio -> Project -> Operation**의 4계층 가치 흐름을 정렬하고, RACI/I&O 거버넌스 체계 하에 **BSC-IT(4관점) + KPI(CSF/KGI)**로 성과 측정하는 체계적 관리 패러다임이다.
> 2. **가치**: 성숙도 기반 IT 운영(예: COBIT 2019 Maturity 3.0->4.5 도달 시 인시던트 MTTR 65% 단축, ITIL Change Success Rate 92%->98% 향상), IT 투자 **ROI 25%^, TCO 30%v**, **TBM(Technology Business Management)** 기반 IT 비용 투명성 확보로 사업부 비용 배분 정당화 및 예산 협상력 강화.
> 3. **판단 포인트**: 🔍 **핵심 트레이드오프**는 (a) **집중형(Centralized) vs 분산형(Federated/CoE) 조직 모델** 선택 — SLA 응답시간 30%v vs 사업부 자율성, (b) **Build vs Buy vs Rent** 의사결정 (TCO 3~5년 분석), (c) **Agile@Scale(SAFe) vs Waterfall-PMI** 혼용 비율, (d) **In-House Cloud vs Public Cloud**의 데이터 주권·컴플라이언스 트레이드오프, (e) **Zero Trust vs Perimeter Security** 보안 아키텍처 패러다임.

---

## Ⅰ. 개요 및 필요성

디지털 트랜스포메이션(DX) 가속화, GDPR·PIPC(개인정보보호법)·ESG 공시 의무화, 그리고 **클라우드·AI·데이터 3대 기술 패러다임 전환**으로 인해 IT는 더 이상 비용 센터(Cost Center)가 아닌 **전략적 사업 능력(Strategic Business Capability)**으로 재정의되어야 한다. 과거(1990~2010년대)에는 CIO가 "시스템 안정성"에 집중했다면, 2020년대 이후의 IT 경영은 **거버넌스-전략-포트폴리오-프로젝트-운영-컴플라이언스**를 end-to-end로 통합 관리하는 **Enterprise-wide IT Management 체계**를 요구한다. 기술사 시험에서는 단순 암기형이 아닌, **"왜 이 프레임워크를 선택했는가?"**에 대한 **맥락 기반 의사결정 능력**을 평가한다.

```text
+----------------------------------------------------------------------+
|           IT 경영 관리 5단계 계층구조 (Layered Governance Model)     |
+----------------------------------------------------------------------+
|  Layer 1: 거버넌스 & 컴플라이언스 (Governance & Compliance)          |
|  +--------------+  +--------------+  +--------------+               |
|  | COBIT 2019   |  |   ISO 38500  |  |  내부통제(K- |               |
|  | 40 Governance |<-->|  IT거버넌스  |<-->|  SOX/ISMS-P) |               |
|  |   Objectives  |  |   표준        |  |   표준       |               |
|  +------+-------+  +------+-------+  +------+-------+               |
|         +-----------------+-----------------+                       |
|                           v                                          |
|  Layer 2: 전략 & 포트폴리오 (Strategy & Portfolio)                    |
|  +------------------------------------------------------+           |
|  |  ISO/IEC 38505 + IT 전략(ISP) + IT-PMF(Performance)  |           |
|  |  Portfolio Mgmt: 프로젝트 NPV/IRR/옵션가격 분석      |           |
|  +--------------------------+---------------------------+           |
|                             v                                       |
|  Layer 3: 프로젝트 & 프로그램 (Delivery)                              |
|  +--------------+  +--------------+  +--------------+               |
|  | PMBOK 7th    |  |   PRINCE2    |  | SAFe 6.0     |               |
|  | (예측형)     |  |  (단계통제)  |  | (Agile@Scale)|               |
|  +------+-------+  +------+-------+  +------+-------+               |
|         +-----------------+-----------------+                       |
|                           v                                          |
|  Layer 4: 서비스 & 운영 (Service & Operation)                        |
|  +------------------------------------------------------+           |
|  |  ITIL 4 (Service Value System: 7원칙·4차원·34실무)   |           |
|  |  + DevOps (CI/CD) + SRE (SLO/Error Budget)            |           |
|  +--------------------------+---------------------------+           |
|                             v                                       |
|  Layer 5: 기술 & 데이터 플랫폼 (Technology Foundation)                |
|  +--------------+  +--------------+  +--------------+               |
|  | Cloud (IaaS/ |  |  Data Lake/  |  |  AI/MLOps    |               |
|  | PaaS/SaaS)   |  |  Lakehouse   |  |  Platform    |               |
|  +--------------+  +--------------+  +--------------+               |
+----------------------------------------------------------------------+
       vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
  [성과측정: BSC-IT 4관점 + KPI 대시보드 -> 경영진 보고]
```

**왜 필요한가? (Old vs New Paradigm)**

| 구분 | Old Paradigm (2010 이전) | New Paradigm (2024 이후) |
| :--- | :--- | :--- |
| **IT 역할** | 비용 센터(Back-office) | 가치 창출 파트너(Value Driver) |
| **관리 대상** | 서버·네트워크·SW | 서비스·데이터·경험(DX) |
| **아키텍처** | 모놀리식(On-premise) | 클라우드 네이티브 + 하이브리드 |
| **지표** | 가용성(Uptime), MTBF | NPS, TTM, ROI, CO₂e(그린IT) |
| **보안 모델** | 경계 기반(Perimeter) | Zero Trust + SASE |
| **인력 모델** | 전문화(Silo) | T자형 + DevSecOps 융합 |
| **거버넌스** | 사후 통제(Audit) | 실시간 리스크 기반(Continuous) |
| **컴플라이언스** | 체크리스트 | 자동화 + RegTech |

- **📢 섹션 요약 비유**: IT 경영 관리는 **도시의 통합 관제 시스템**과 같습니다. 개별 건물(시스템)만 관리하는 게 아니라, 교통·상하수도·전력·보안·재정·법규를 한 화면에 통합 보여줘야 시민(사업부)이 안전하고 효율적으로 생활할 수 있습니다. COBIT이 "도시 헌장", ITIL이 "일상 운영 매뉴얼", PMBOK이 "건축 공사 감독", TOGAF가 "도시계획 청사진" 역할을 합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **"전략(Strategy) -> 실행(Execution) -> 측정(Measurement) -> 학습(Learning)"**의 폐루프(Closed-loop) 가치 사슬을 구축하는 것이다. 이를 위해 **COBIT 2019의 40 Governance & Management Objectives**를 최상위 통제 목표로 삼고, 이를 **ITIL 4 Service Value Chain(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve)**으로 매핑한 후, **BSC-IT Balanced Scorecard**로 4관점 성과를 측정한다.

```text
+----------------------------------------------------------------------+
|         IT 경영 폐루프 가치 사슬 (Closed-Loop IT Value Chain)        |
+----------------------------------------------------------------------+
                              [STEP 0] 환경 분석
   +--------------------------------------------------------+
   |  PESTEL + 5-Forces + SWOT + 외부 벤치마킹(Gartner MQ) |
   |  -> IT 전략적 맥락(Strategic Context) 정의              |
   +----------------------------+---------------------------+
                                v
   [STEP 1] 전략 정렬(Strategy Alignment) -- COBIT EDM(평가·지시·모니터)
   +--------------------------------------------------------+
   |  • SAM(Strategic Alignment Model) : Henderson & Venkatraman|
   |    - Strategy Fit: 사업전략 ↔ IT전략 양방향 정렬        |
   |    - 4 domain: Business Strategy, IT Strategy,          |
   |                 Organization, Infrastructure          |
   |  • IT-PMF(Performance & Maturity Framework)             |
   |    4-Layer: Strategy -> Process -> Capability -> Contrib. |
   +----------------------------+---------------------------+
                                v
   [STEP 2] 거버넌스 의사결정 -- RACI + Steering Committee
   +--------------------------------------------------------+
   |  +-------------+----------+----------+----------+      |
   |  | 의사결정    |  R(집행) |  A(책임) |  C(자문) | I(통보)|
   |  +-------------+----------+----------+----------+------+
   |  | IT 투자 승인 |   CIO    |   CEO    | 사업부문장| CFO   |
   |  | 아키텍처 결정|   EA팀   |   CTO    |   CIO    | CEO   |
   |  | 인시던트 에스| SRE팀장  |   COO    | 법무·보안| 임원  |
   |  +-------------+----------+----------+----------+------+      |
   +----------------------------+---------------------------+
                                v
   [STEP 3] 포트폴리오 최적화 (PPM: Project Portfolio Mgmt)
   +--------------------------------------------------------+
   |  프로젝트 분류 매트릭스:                                |
   |  • Strategic(전략) - Run(운영) - Grow(성장) - Transform |
   |  • 평가기법: NPV, IRR, Payback, Real Options, RAROC    |
   |  • 제약이론(ToC): 병목 자원 기준 우선순위 결정         |
   +----------------------------+---------------------------+
                                v
   [STEP 4] 프로젝트 실행 (Delivery)
   +--------------+--------------+------------------+
   |  Waterfall   |   Agile      |   Hybrid(SAFe)   |
   |  PMBOK 7th   |   Scrum/     |   PI Planning    |
   |  계획중심    |   Kanban     |   5-10 Agile팀   |
   |  회계·ERP 등  |   SW개발     |   전사 DX         |
   +--------------+--------------+------------------+
                                v
   [STEP 5] 서비스 운영 -- ITIL 4 + SRE + DevSecOps
   +--------------------------------------------------------+
   |  Service Value Chain:                                  |
   |  Demand -> Engage -> Design -> Obtain -> Deliver -> Support|
   |           -> Improve(CSI) <- 7 SVS Principles           |
   |  34 Management Practices / 26 Service Value Chain 등  |
   +----------------------------+---------------------------+
                                v
   [STEP 6] 성과 측정 (BSC-IT + KPI)
   +--------------------------------------------------------+
   |  4관점:                                                |
   |  ① 재무(FCI, ROI) ② 고객(NPS, SLA)                   |
   |  ③ 내부프로세스(MTTR, Change Success) ④ 학습/성장     |
   |  CSF(Critical Success Factor) -> KPI -> KGI 계층화      |
   +----------------------------+---------------------------+
                                v
   [STEP 7] 지속적 개선 -- CSI + Lean + Kaizen
                                | (피드백 루프)
                                +--------------► STEP 1
```

### IT 경영 핵심 프레임워크 상세 비교

| 프레임워크 | 주요 영역 | 핵심 구성 | 적용 시점 | 산출물 |
| :--- | :--- | :--- | :--- | :--- |
| **COBIT 2019** | 거버넌스·관리 | 40 Obj, 5 Domains (EDM, APO, BAI, DSS, MEA) | 전사 IT 통제 체계 | RACI, Maturity Model, Policies |
| **ITIL 4** | 서비스 운영·개선 | SVS(7원칙·4차원), 34 Practices, Value Chain | 일일 운영·CSI | SLA, SLO, Runbook, Catalog |
| **TOGAF 10** | EA(엔터프라이즈 아키텍처) | ADM(8단계) Cycle, Content Metamodel | 중장기 아키텍처 청사진 | Architecture Roadmap, Gap Analysis |
| **PMBOK 7th** | 프로젝트 관리 | 8 Performance Domains + 12 Principles | 프로젝트 단위 | Charter, WBS, Risk Register |
| **SAFe 6.0** | Agile@Scale | 4 Configurations, ART, PI Planning | 전사 Agile 전환 | PI Roadmap, Features, Stories |
| **ISO 38500** | IT 거버넌스 표준 | 6 원칙(Evaluate·Direct·Monitor) | 이사회 수준 의사결정 | Governance Charter |
| **IT4IT** | IT Value Chain 참조 | 4 Streams(Strategy->Plan->Build->Run) | IT 운영 모델 재설계 | Backlog, Service Backlog |
| **CMMI 2.0** | 프로세스 성숙도 | 5 Maturity Levels, 20 Practice Areas | 프로세스 표준화 | Appraisal 결과서 |

### 핵심 원리 심층 분석

**(1) IT-사업 전략 정렬 메커니즘 — Henderson-Venkatraman SAM 모델**

```text
                  [비즈니스 전략]                      [IT 전략]
   +-------------------------------------+
   |  Business Strategy (사업 전략)      | <- SC(Strategy)  -> IT Strategy
   |  - 시장확대, M&A, 제품혁신, 원가경쟁  |    Fit
   +--------------+----------------------+
                  | Execution Fit
                  v
   +--------------------------------------+
   |  Organization & Process              | <- Infrastructure Fit
   |  - 조직구조, KPI, 보상체계            |
   +--------------+----------------------+
                  | Infrastructure Fit
                  v
   +--------------------------------------+
   |  IT Infrastructure & Processes       |
   |  - HW/SW/네트워크, DB, 어플리케이션  |
   +--------------------------------------+
```

SAM은 **3개 정합(Fit)**: SC(Strategy Fit), EF(Execution Fit), IF(Infrastructure Fit)을 모두 만족해야 IT가 전략적 기여자로 기능한다. 기술사 시험에서는 "우리 회사 OO 전략에 맞는 IT 정렬 수준을 어떻게 측정할 것인가"를 묻는 빈도가 높다.

**(2) BSC-IT 4관점 KPI 계층화**

```text
   Vision: "IT를 통한 사업 경쟁력 우위 확보"
        |
        v
   Mission: "안정적·혁신적 IT 서비스 제공"
        |
        v
   +-------------------------------------------------+
   |
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 448 / 800

<- **이전**: [447. IT 경영 관리 핵심 토픽 447번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/447_it_management_core_topic_447_exam_summary/)
**다음**: [449. IT 경영 관리 핵심 토픽 449번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/449_it_management_core_topic_449_exam_summary/) ->

---
