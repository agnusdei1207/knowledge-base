+++
title = "444. IT 경영 관리 핵심 토픽 444번 시험 요약 (IT Management Core Topic 444 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019(거버넌스·관리 목표 40개), ITIL 4(Service Value System 34개 Practice), TOGAF ADM(8단계 사이클)을 통합 프레임워크로 삼아, **전략-거버넌스-아키텍처-운영-개선** 5계층 간의 정렬(Alignment)을 통해 기업 가치를 극대화하는 종합 학문이다.
> 2. **가치**: McKinsey(2023) 보고에 따르면成熟度 Level 3 이상 기업은 IT 투자 ROI 평균 28%, 디지털 전환 성공률 67%를 달성하며, 미성숙 기업 대비 프로젝트 실패율을 41%p 절감한다. 또한 ISO/IEC 38500 준수 시 이사회-경영진 간 IT 의사결정 리드타임을 평균 35% 단축한다.
> 3. **판단 포인트**: 핵심 Trade-off는 **(1) 거버넌스 강도 vs. 비즈니스 민첩성(Governance vs. Agility)**, **(2) 중앙집권 vs. 페데레이션(CoE vs. BUs)**, **(3) Build vs. Buy**, **(4) CapEx vs. OpEx 전환**이며, 기술사답게 **정량 KPI(ROI, NPV, TCO, EVA, ROIC)**와 **정성 KPI(BSC 4관점, GRC 성숙도)**를 균형 있게 설계할 수 있어야 한다.

---

## Ⅰ. 개요 및 필요성

21세기 들어 IT는 단순 지원(Support) 기능을 넘어 **비즈니스 코어(Core)**, 심지어 **전략 동인(Driver)**으로 자리매김했다. 그러나 한국 정보화진흥원(NIA) 「2023년 디지털 전환 실태조사」에 따르면 국내大中型企業의 62%가 **"IT 투자의 전략적 정렬이 부족하다"**고 응답했고, 47%가 **"투자 대비 효과 측정이 미흡"**하다고 답했다. 이는 Cobit 5.0 Foundation 조사에서 밝힌 **"IT Failure Rate 50~70%"**의 근본 원인과 일치하며, IT 경영 관리 체계 부재가 직접적 원인이다.

특히 **클라우드, AI, 데이터 거버넌스, ESG-IT, 제로트러스트** 등 4차 산업혁명 기술의 도입이 가속화되면서, 단순히 기술 도입을 넘어 **Value Realization(가치 실현)**을 체계적으로 관리할 수 있는 경영 프레임워크가 요구된다. ISO/IEC 38500(2015)이 명시한 **"Evaluate-Direct-Monitor"** 3원칙과 COBIT 2019의 **"Governance System & Components"** 5도메인(EDM, APO, BAI, DSS, MEA) 체계가 이를 뒷받침한다.

```text
┌─────────────────────────────────────────────────────────────────┐
│          IT 경영 관리 5계층 프레임워크 (5-Layer Model)            │
├─────────────────────────────────────────────────────────────────┤
│  L1. 전략(Strategy)    : IT Vision, Portfolio, BAM, Innovation  │
│      │                       (BSC 4관점, OKR, McFarlan Grid)     │
│      ▼                                                          │
│  L2. 거버넌스(Governance): COBIT 2019, ISO 38500, GRC, 정책체계  │
│      │                       (RACI, Three Lines of Defense)      │
│      ▼                                                          │
│  L3. 아키텍처(Architecture): TOGAF ADM, Zachman, FEAF, DoDAF    │
│      │                          (BIZ-APP-DATA-TECH Layering)    │
│      ▼                                                          │
│  L4. 운영(Operation)     : ITIL 4 SVS, DevOps, SRE, FinOps      │
│      │                       (34 Practice, 4D 모델)              │
│      ▼                                                          │
│  L5. 개선(Improvement)   : CSI, Kaizen, Lean IT, TMMi, CMMI     │
│                              (7-Step Improvement Process)        │
└─────────────────────────────────────────────────────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
  Value Realization          Risk Management          Capability Mgmt
  (ROI/NPV/EVA)             (ISO 27005/31000)         (Maturity Model)
```

**구(舊) vs 신(新) 패러다임**:
- **구(舊)**: IT = Cost Center(비용 센터) → 무조건 절감·통제 중심, "No"라는 답이 80%
- **신(新)**: IT = Value Center(가치 센터) → ROI 극대화·혁신 주도, "How"라는 답이 80%
- 예: 과거 "데이터센터 자가 운영" vs 현재 "FinOps 기반 멀티클라우드(비용 최적화 23~37%)"

- **📢 섹션 요약 비유**: IT 경영 관리는 **자동차의 계기판(Cockpit)**과 같다. 엔진(기술)만 좋다고 차가 잘 달리는 것이 아니라, 속도계·RPM·연료·엔진온도·경고등(지표)을 통합적으로 보여주는 **종합 계기판**이 있어야 운전자가 올바른 판단을 내릴 수 있다. COBIT가 이 계기판의 설계도라면, ITIL은 정비 매뉴얼, TOGAF는 차체 설계도인 셈이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. 핵심 거버넌스 메커니즘: COBIT 2019 Governance System

COBIT 2019는 **40개의 관리 목표(Management Objective)**와 **5개 거버넌스 목표(EDM: Evaluate-Direct-Monitor)**로 구성되며, **연속적 조정(Continuous Adjustment)**을 통해 조직의 7가지 구성요소(Principles, Goals, Components, Focus Areas, Design Factors, Issues/Risk, Performance)를 연결한다.

```text
        ┌────────────────────────────────────────────┐
        │         COBIT 2019 Core Model & Workflow    │
        └────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
  ┌─────────┐         ┌─────────┐         ┌─────────┐
  │  EDM 05 │         │  APO 12 │         │  BAI 11 │
  │Governance│        │ Managed│         │ Managed│
  │ System   │        │ Risk    │         │ Projects│
  └────┬────┘         └────┬────┘         └────┬────┘
       │                   │                   │
       ▼                   ▼                   ▼
   RACI Matrix         ISO 31000            PRINCE2/MSP
   (Responsible,      (Risk=Threat×         (Stage/Work
    Accountable,       Vulnerability×       Boundary)
    Consulted,         Asset Value)
    Informed)
       │                   │                   │
       └───────────────────┼───────────────────┘
                           ▼
              ┌──────────────────────────┐
              │   Performance Management  │
              │  (CSF/KPI, Maturity Level)│
              │  - Lag/Lead Indicator     │
              │  - CMMI 1~5 Level        │
              └──────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(거버넌스 영역)** | Evaluate-Direct-Monitor 5개 프로세스 | 이사회·CIO의 의사결정 체계. Benefit Realization(EDM02), Risk Optimization(EDM03), Resource Optimization(EDM04) |
| **APO(Align, Plan, Organize)** | 14개 관리 목표 | 전략 정렬·포트폴리오·혁신·예산·인력·관계·SLA 설계 (APO04 혁신, APO09 SLA, APO12 위험) |
| **BAI(Build, Acquire, Implement)** | 11개 관리 목표 | 솔루션 도입·변경관리·릴리스·테스트·지식관리 (BAI03 변경, BAI07 도입 수용) |
| **DSS(Deliver, Service, Support)** | 6개 관리 목표 | 서비스 운영·장애·연속성·보안·사용자 지원 (DSS01 운영, DSS02 인시던트, DSS04 연속성) |
| **MEA(Monitor, Evaluate, Assess)** | 4개 관리 목표 | 성과 측정·내부통제·준수·문제 해결 (MEA01 성과, MEA03 컴플라이언스) |

### B. 가치 실현(Value Realization) 핵심 공식

기술사 시험에서 자주 등장하는 정량 가치 평가식:

```
┌──────────────────────────────────────────────────────────┐
│ 1) 총소유비용(TCO) = 직접비 + 간접비 + 기회비용 + 위험비용  │
│    TCO = CapEx + OpEx + Downtime Cost + Risk Exposure    │
│                                                          │
│ 2) 투자수익률(ROI) = (총이익 - 총비용) / 총비용 × 100     │
│    ROI = (Benefit - Cost) / Cost × 100                   │
│                                                          │
│ 3) 순현재가치(NPV) = Σ [CFₜ / (1+r)ᵗ] - 초기투자         │
│    (할인율 r: WACC 가중평균자본비용 6~12% 적용)            │
│                                                          │
│ 4) 내부수익률(IRR): NPV=0이 되는 할인율, r>WACC일 때 수용  │
│                                                          │
│ 5) 경제적부가가치(EVA) = NOPAT - (WACC × 투자자본)        │
│                                                          │
│ 6) Payback Period(투자회수기간) = 초기투자 / 연 현금흐름   │
│                                                          │
│ 7) IT Balanced Scorecard (Kaplan & Norton 4관점)         │
│    - 재무(Financial): TCO 절감률, ROIC                   │
│    - 고객(Customer): SLA 준수율, NPS                     │
│    - 내부프로세스(Internal): MTTR, 변경 성공률           │
│    - 학습성장(Learning): 직원역량지수, 인증 보유율        │
└──────────────────────────────────────────────────────────┘
```

### C. ITIL 4 Service Value System (SVS)

ITIL 4는 **Opportunity/Demand → Value**로 연결하는 7개 컴포넌트 체계를 갖는다:
1. **Guiding Principles**(7원칙: Focus on value, Start where you are, Progress iteratively, etc.)
2. **Governance**(거버넌스)
3. **Service Value Chain**(Plan→Engage→Design&Transition→Obtain/Build→Deliver&Support→Improve 6단계)
4. **Practices**(34개: Incident, Problem, Change Enablement, Service Desk, Continual Improvement 등)
5. **Continual Improvement**(CSI 등록부)
6. **Technologies & Organization**

- **📢 섹션 요약 비유**: COBIT의 40개 관리 목표는 **도시의 zoning 규칙(토지이용 계획)**, ITIL의 Practice는 **도시의 도로·상하수도·전력 등 일상 운영 매뉴얼**, TOGAF ADM은 **도시 마스터플랜(어떤 구역에 무엇을 지을지)**이다. 이 셋이 맞물려야 도시(기업)가 혼란 없이 돌아간다.

---

## Ⅲ. 비교 및 연결

### A. 주요 거버넌스·관리 프레임워크 비교

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 38500** | **PMBOK 7** | **TOGAF 9.2/10** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 | IT 서비스 운영 | IT 의사결정 거버넌스 원칙 | 프로젝트 관리 표준 | EA(엔터프라이즈 아키텍처) |
| **계층** | 전략→운영 전계층 | 운영·서비스 중심 | 원칙·거버넌스 최상위 | 프로젝트 단위 | 아키텍처 단위 |
| **핵심 단위** | 40 Mgmt Objective | 34 Practice | 6 Principles | 12 Principle + 8 Domain | ADM 8 Phase |
| **성숙도 모델** | CMMI 0~5 매핑 | 4D 모델 | 자체 평가 지표 | OPM3 | ARM(Architecture Repository) |
| **강점** | ROI·위험 정량화 | 서비스 운영 노하우 | 법률·컴플라이언스 | 프로젝트 실행 | 비즈니스-기술 정합 |
| **약점** | 복잡·운영 디테일 부족 | 거버넌스 약함 | 추상적 | 거버넌스 약함 | 시간·비용 많이 소요 |
| **적합 기업** | 대기업·금융·공공 | 통신·SI·MSP | 이사회·감사 | 프로젝트 중심 조직 | 전사 디지털 전환 |

### B. 전략 분석 도구 비교

| 구분 | **McFarlan Grid** | **Gartner Hype Cycle** | **Ward & Peppard BSP** | **Henderson Venkatraman** |
| :--- | :--- | :--- | :--- | :--- |
| **축** | 현재/미래 전략적 영향 | 기대 vs. 시간 | 내부/외부 환경 | 전략/운영 vs. IT |
| **사분면** | Strategic / Turnaround / Factory / Support | Innovation Trigger → Peak → Trough → Slope → Plateau | IS/IT 전략 매트릭스 | 4관점(Strategic, Info, Process, Infrastructure) |
| **용도** | IT 포트폴리오 분류 | 기술 투자 타이밍 | 전략적 정보시스템 계획 | 전략적 IT 정렬 |
| **한계** | 정성적, 주관 | 예측 실패 사례 多 | 동적 환경 반영 약함 | 조직 변화 반영 부족 |

### C. 다른 시스템·도구와의 통합

```text
┌────────────────────────────────────────────────────────────┐
│       IT 경영관리 통합 스택 (Integrated IT Management Stack) │
├────────────────────────────────────────────────────────────┤
│  상위 거버넌스: GRC 플랫폼 (RSA Archer, ServiceNow GRC)    │
│        │                                                   │
│        ▼                                                   │
│  전략/포트폴리오:   TracIT, Planview, Clarity PPM            │
│        │                                                   │
│        ▼                                                   │
│  EA/아키텍처:       LeanIX, MEGA HOPEX, BiZZdesign          │
│        │                                                   │
│        ▼                                                   │
│  프로젝트:          MS Project Online, Jira, Azure DevOps   │
│        │                                                   │
│        ▼                                                   │
│  서비스 운영:       ServiceNow, BMC Remedy, Jira SM          │
│        │                                                   │
│        ▼                                                   │
│  모니터링/AIOps:    Datadog, Splunk, Dynatrace, PagerDuty   │
│        │                                                   │
│        ▼                                                   │
│  보안
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 444 / 800

← **이전**: [443. IT 경영 관리 핵심 토픽 443번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/443_it_management_core_topic_443_exam_summary/)
**다음**: [445. IT 경영 관리 핵심 토픽 445번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/445_it_management_core_topic_445_exam_summary/) →

---
