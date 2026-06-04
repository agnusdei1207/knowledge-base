+++
title = "639. IT 경영 관리 핵심 토픽 639번 시험 요약 (IT Management Core Topic 639 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# 639. IT 경영 관리 핵심 토픽 639번 시험 요약

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, PMBOK 7th, ISO 38500 등 글로벌 거버넌스/관리 프레임워크를 통합 적용하여 **전략-거버넌스-운영-전환**의 4계층으로 IT 가치를 극대화하는 경영 활동이다.
> 2. **가치**: 프레임워크 정착 시 IT 투자 대비 ROI 평균 23% 향상(McKinsey 2023), IT 부서 응답시간 65% 단축, 보안사고 47% 감소 등 정량적 효과가 입증되었으며, ESG·DX 시대의 경쟁력 핵심 자산이 된다.
> 3. **판단 포인트**: 조직의 성숙도(CMMI 5단계, COBIT 7단계)와 산업별 규제 요건(금융 ISMS-P, 의료 HIPAA, 공공 EA)을 고려한 **"프레임워크 조합 전략"**, 그리고 코스트센터->프로핏센터 전환 여부, 내부 통제 vs 외부 감사 비중 등이 핵심 의사결정 변수다.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명·DX·AI 전환 가속화로 IT는 더 이상 단순 지원 기능이 아니라 **"전략적 핵심 자산"**이 되었다. 그러나 한국 기업 통계(KISA 2023)에 따르면, Fortune 500 한국 기업 중 IT 거버넌스 체계가 **"체계적(Established)"** 이상인 비율은 18%에 불과하며, 정보화 사업 실패율(요구사항 미충족 또는 예산 초과)은 평균 42%에 달한다. 이는 **"IT 투자의 비가시성"**과 **"경영진과 IT 조직 간 인식 격차"**가 근본 원인이다.

IT 경영 관리의 핵심 과제는 다음 5가지로 압축된다:

1. **전략 정렬(Strategic Alignment)**: 비즈니스 목표 ↔ IT 전략의 양방향 추적성 확보
2. **가치 실현(Value Realization)**: IT 투자 수익률(ROIT, Return on IT Investment) 측정·관리
3. **리스크 관리(Risk Management)**: 사이버 리스크, 컴플라이언스 리스크, 운영 리스크 통합 관리
4. **자원 최적화(Resource Optimization)**: 인력·예산·인프라의 균형적 배분
5. **성과 측정(Performance Measurement)**: KPI/KRI 기반의 데이터 기반 의사결정

```text
+---------------------------------------------------------------------+
|         IT 경영 관리 4계층 통합 프레임워크 (Top-Down View)          |
+---------------------------------------------------------------------+
|                                                                     |
|  +----------------------------------------------------------+       |
|  | L1. 전략계층(Strategy)                                   |       |
|  |  • IT 전략 로드맵(3~5년)  • 디지털 전환(DX) 비전        |       |
|  |  • TOGAF / FEAF 기반 EA(Enterprise Architecture) 수립   |       |
|  +----------------------------------------------------------+       |
|                          v  Cascade                                  |
|  +----------------------------------------------------------+       |
|  | L2. 거버넌스계층(Governance)                             |       |
|  |  • COBIT 2019 (40 Governance/Management Objectives)     |       |
|  |  • ISO 38500 (6 Principles)  • ISMS-P / ISO 27001       |       |
|  |  • IT Steering Committee 운영 (분기 1회)                |       |
|  +----------------------------------------------------------+       |
|                          v  Translate                               |
|  +----------------------------------------------------------+       |
|  | L3. 운영계층(Operations)                                 |       |
|  |  • ITIL 4 Service Value System (SVS)                    |       |
|  |  • ITSM 도구(ServiceNow, BMC Helix)                     |       |
|  |  • SLA / OLA / UC × 4관점(조직,정보,기술,파트너십)      |       |
|  +----------------------------------------------------------+       |
|                          v  Execute                                 |
|  +----------------------------------------------------------+       |
|  | L4. 프로젝트/전환계층(Project & Transformation)         |       |
|  |  • PMBOK 7th (8 Performance Domains)                    |       |
|  |  • 애자일/SAFe, DevOps, FinOps                         |       |
|  |  • 예산 배분·TCO/ROI 추적·내부통제 체계                  |       |
|  +----------------------------------------------------------+       |
|                                                                     |
|  [Cross-cutting] 데이터 거버넌스(DAMA-DMBOK2), 보안, ESG, BCM      |
+---------------------------------------------------------------------+
```

**기존 패러다임 대비 진화**:
- **전통적 IT 관리(2000년대)**: CIO 중심, CapEx 위주, 부서 단위 운영, 사후 통제
- **현代的 IT 경영 관리(2020년대~)**: CEO·이사회 거버넌스, OpEx+CapEx 혼합, EA 기반 통합, 실시간 리스크·컴플라이언스 자동화, **"BizDevOps + FinOps + SecOps"** 트리렐릭스(Trirelaux) 모델

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **"도시의 도시계획(Urban Planning)"**과 같다. 건물(시스템) 하나만 잘 지으면 안 되고, 도로(네트워크), 상하수도(데이터), 교통(프로세스), 소방(보안), 재무(예산)를 한 도면에서 동시에 설계해야 도시가 살듯이, IT도 **4계층 통합 도면** 위에서 경영되어야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 작동 메커니즘은 **"전략->거버넌스->운영->프로젝트"로 내려가는 캐스케이드(Cascade)**와 **"측정->평가->피드백"으로 올라가는 피드백 루프(Feedback Loop)**의 결합이다. 이 4+1 흐름을 구현하는 핵심 컴포넌트는 다음과 같다.

```text
+--------------------------------------------------------------------+
|      IT 경영 관리 핵심 컴포넌트 인터랙션 다이어그램                |
+--------------------------------------------------------------------+
                          +------------------+
                          |  Board / CEO     | (의사결정)
                          |  Risk Committee  |
                          +--------+---------+
                                   | 거버넌스 지휘
                                   v
            +------------------------------------------+
            |   IT Steering Committee (분기 1회)        |
            |   • Portfolio Prioritization             |
            |   • Budget Allocation (CapEx/OpEx)       |
            +--------+---------------------+-----------+
                     |                     |
        전략/정책     |                     |    운영 보고
                     v                     v
   +----------------------+    +-------------------------+
   |  COBIT 2019          |◄--►|  ITIL 4 SVS             |
   |  - 40 Objectives     |    |  - 34 Practices         |
   |  - 7 Components      |    |  - Service Value Chain  |
   |  - Focus Areas       |    |  - 4 Dimensions         |
   +----------+-----------+    +--------+----------------+
              |                          |
              |     +----------+         |
              +---►|  Metrics |◄--------+
                    |  & KPI   |
                    | Platform|
                    +----+-----+
                         | Data -> Analytics -> Insights
                         v
        +--------------------------------------+
        |  Decision Support / Continuous Improve|
        |  • PDCA + OODA Loop                  |
        |  • BPM(Camunda) + BI(Power BI)        |
        +--------------------------------------+
                         ^
                         | 실행/완료 보고
        +----------------+-----------------------+
        |  Project/Transformation Layer          |
        |  PMO(Program Management Office)        |
        |  - PMBOK / PRINCE2 / SAFe              |
        |  - 내부통제(SoX, J-SOX), IS Audit       |
        |  - PMIS(Microsoft Project, Jira, etc.) |
        +----------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **전략·EA 모듈** | 중장기 IT 비전·로드맵 수립 | TOGAF ADM(Architecture Development Method) 8단계 — Preliminary->Vision->Business Architecture->Information Systems->Technology->Opportunities->Migration->Governance Cycle. **EA Repository(Hopex, BiZZdesign, Sparx EA)**에 As-Is/To-Be 모델 등록, 변경 시 영향도 분석 자동화. |
| **거버넌스·컴플라이언스 모듈** | 의사결정·통제·감사 체계 운영 | COBIT 2019의 **40 Governance & Management Objectives**를 조직의 우선순위 5~7개에 맞춰 Tailoring. **RACI 차트**(Responsible, Accountable, Consulted, Informed)로 역할 명확화. ISMS-P 인증 심사 연 1회, 내부 심사 분기 1회. |
| **운영·서비스 모듈** | IT 서비스의 기획-설계-전환-운영-개선 | ITIL 4의 **Service Value System(SVS)** — Opportunity/Demand->Value->7단계 Value Chain(Plan/Improve->Engage/Design/Transition/Obtain/Build->Deliver/Support). 인시던트 MTTR, 변경 성공률, 첫 접촉 해결률(FCR) 등 **9대 핵심 KPI** 운영. |
| **프로젝트·전환 모듈** | 개별 사업의 계획-실행-종료 관리 | PMBOK 7th의 **8 Performance Domains**(Stakeholders, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty). 애자일의 경우 **Scrum(3~9명, 2~4주 스프린트)**, 대규모는 **SAFe(4단계: Team->Program->Large Solution->Portfolio)** 적용. 예산은 **EVM(Earned Value Management)** — CPI, SPI, EAC, ETC로 추적. |

**핵심 작동 원리 — "3대 정렬(Alignment) 원칙"**:
1. **전략 정렬(Strategy-Business Alignment)**: Henderson & Venkatraman의 **SAM(Strategic Alignment Model)** — 외부(Industry, Environment) ↔ 내부(Organization, IS/IT Strategy) 4관점 정렬
2. **프로세스 정렬(Process-Goal Alignment)**: **Cascading Goals Tree** — 전사 KPI -> IT KPI -> 팀/개인 KPI로 3~4단계 분해
3. **자원 정렬(Resource-Demand Alignment)**: **Capacity vs Demand** 예측 — IT 재무관리의 5단계(Plan->Budget->Chargeback/Showback->Analyze->Report)

**정량 모델**:
- **TCO(Total Cost of Ownership)**: `TCO = 직접비(하드웨어·소프트웨어·인건비) + 간접비(다운타임·교육·지원·전환)` — Gartner 모델 기준 5년 TCO에서 운영비가 60~70% 차지
- **ROIT(Return on IT Investment)**: `ROIT = (IT 투자로 인한 이익 증가분 + 비용 절감) / IT 투자액 × 100` — 우수 기업 평균 15~25%
- **NPV(순현재가치)**: `NPV = Σ[CFₜ/(1+r)ᵗ] - 초기투자`, 할인율 r은 WACC(가중평균자본비용) 적용, IRR > r일 때 사업 승인

- **📢 섹션 요약 비유**: IT 경영 관리의 4계층은 **"비행기의 조종석"**과 같다. L1(전략)은 **비행계획서(노선·고도)**, L2(거버넌스)는 **관제탑의 교통관제 지시**, L3(운영)은 **자동조종·엔진 제어 시스템**, L4(프로젝트)는 **실제 출발·착륙·급유 절차**다. 어느 하나라도 계기판(Metrics Platform)이 없으면 추락한다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리에서 혼동하기 쉬운 핵심 프레임워크/개념을 명확히 구분한다. 기술사 시험에서는 **"무엇이 다르고, 언제 무엇을 쓰는지"**를 구분할 수 있어야 한다.

| 구분 | **COBIT 2019** | **ITIL 4** | **PMBOK 7th** | **ISO 38500** |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 목표(40개) 프레임워크 | IT 서비스 운영·관리 베스트 프랙티스 | 프로젝트 관리 지식 체계 | IT 의사결정·거버넌스 국제표준 |
| **적용 범위** | 전사(Enterprise) IT | IT 서비스 조직·프로세스 | 개별 프로젝트 | 이사회·경영진 |
| **핵심 구조** | 40 Objectives × 7 Components × Focus Areas | Service Value System, 34 Practices, 4 Dimensions | 8 Performance Domains, 12 Principles | 6 Principles(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior) |
| **산출물** | Maturity Model(0~5), Goals Cascade | Service Catalogue, SLA, Value Stream | Project Charter, WBS, Risk Register | Policy, Decision Log, Assurance Report |
| **관계/연계** | **상위 거버넌스** — 전체 IT 평가·지휘 | **하위 운영** — 일일 서비스 실행 | **횡단** — 거버넌스·운영 안에서 프로젝트 수행 | **최상위 원칙** — COBIT보다 추상적, 이사회 원칙 |
| **적용 시점** | 연 1회 거버넌스 점검, 분기별 성과 평가 | 매일·매주 운영 활동 | 프로젝트 라이프사이클(Initiation~Closing) | 이사회 결의 시, 전략 결정 시 |
| **측정 기준** | Process Capability(0~5) | Service KPI(MTBF, MTTR, SLA%) | Schedule/Cost/Scope/Quality | 원칙 준수 여부(Audit) |
| **인증/감사** | COBIT Certified Assessor | ITIL Foundation/Managing Professional | PMP, CAPM | ISO 인증(BSI, KAB) |
| **도구 예** | SAP GRC, RSA Archer, ServiceNow GRC | ServiceNow ITSM, BMC Helix, Jira Service Management | MS Project, Primavera P6, Monday.com | 내부 감사, KPMG/삼일PwC 등 컨설팅 |
| **적합 조직** | 대기업·공공·금융(규제 강함) | 모든 IT 운영 조직 | 모든 프로젝트 수행 조직 | 이사회 거버넌스 의무 조직 |

**연계 관계** — 실무에서는 단일 프레임워크만 쓰지 않고 **"겹쳐서(Overlay)"** 사용한다:

```text
   +--------------------------------------------------+
   |  ISO 38500 (이사회 원칙 — 최상위)               |
   |  "IT는 사업의 성과에 책임진다"                    |
   +--------------------+-----------------------------+
                        |
   +--------------------v-----------------------------+
   |  COBIT 2019 (거버넌스·관리 목표 40개)            |
   |  "어떤 목표를 달성할 것인가"                      |
   |  (예: EDM02, APO12, BAI01, DSS02, MEA01 등)    |
   +-----+--------------------------
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 639 / 800

<- **이전**: [638. IT 경영 관리 핵심 토픽 638번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/638_it_management_core_topic_638_exam_summary/)
**다음**: [640. IT 경영 관리 핵심 토픽 640번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/640_it_management_core_topic_640_exam_summary/) ->

---
