+++
title = "646. IT 경영 관리 핵심 토픽 646번 시험 요약 (IT Management Core Topic 646 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 COBIT 2019의 거버넌스 시스템(Governance System)·거버넌스 프레임워크(Governance Framework)·거버넌스 구성요소(Components)로 구성된 체계로서, 40개의 관리목표(Management Objective)와 EDM(평가·지휘·모니터)·Align·Plan·Organize·Build·Acquire·Implement·Deliver·Monitor 5개 도메인을 통해 IT 가치사슬(Value Chain)을 통제한다.
> 2. **가치**: 성숙한 IT 거버넌스 도입 기업은 IT 투자 대비 ROI가 평균 20~35% 향상되고, 프로젝트 실패율(Chaos Report 기준 31.7%→ 14.2%)이 절반 이하로 감소하며, ISO 27001·ISO 20000·컴플라이언스(Compliance) 감사 적격성을 동시 충족한다.
> 3. **판단 포인트**: 거버넌스 설계 시 (a) Centralized vs Federated vs Hybrid 거버넌스 모형, (b) Cascade Goal(전략→사업→IT)의 To-Be Capability Level 결정, (c) BSC 4관점(재무·고객·내부·학습성장) + IT 4관점(사용자·운영·미래·사업기여) 매핑, (d) Agile/DevOps 환경에서의 FAST(Feedback-driven·Autonomous·Streamlined·Technology-aware) 거버넌스 도입 여부를 트레이드오프로 검토해야 한다.

---

## Ⅰ. 개요 및 필요성

정보화 사업의 규모가 GDP 대비 4~7%를 점유하고, 클라우드·AI·데이터 거버넌스 등 신규 통제 영역이 폭증하면서 전통적인 "IT 운영 관리"로는 사업 가치와 컴플라이언스를 동시에 보장하기 어렵다. 2018년 EU GDPR, 2024년 EU AI Act, 2025년 한국 AI 기본법 시행 등으로 인해 통제 의무(Control Obligation)가 기하급수적으로 증가하고 있으며, 이로 인해 COBIT 2019, ITIL 4, ISO 38500, CMMI 등 다중 프레임워크의 통합 거버넌스가 필수적이다.

기존의 ITIL v3(2011) 기반 프로세스 중심(Service Strategy→Design→Transition→Operation)에서는 26개 프로세스의 운영 효율화에 집중했으나, COBIT 2019는 거버넌스 대상(Enterprise)의 목표 달성을 위해 7가지 구성요소(Principles·Policies·Frameworks·Processes·Organizational Structures·Information Flows·People, Skills, Competencies·Culture, Ethics, Behavior)를 시스템적으로 결합한다.

```text
        [ 전통 IT 관리 ]                                  [ 현대 IT 거버넌스 ]

  사업전략  ──▶  IT 부서  ──▶  서비스 운영  ──▶  사용자      사업전략 ⇄ IT 거버넌스 시스템 ⇄ 가치(Value)
   (전략)        (전달)        (효율)            (만족)        │         │  7대 구성요소
                  │                              │            │         │
                  ▼                              ▼            ▼         ▼
              비용 절감                       티켓 처리     컴플라이언스·리스크·자원 최적화·혁신
              (Cost↓)                        (SLA)        (Value↑, Risk↓, Compliance↑)

   ❌ Silo·프로젝트 단위·부서별 최적화        ✅ Enterprise-wide·Value-driven·End-to-end
   ❌ "IT가 무엇을 하는가"                    ✅ "IT가 왜·어떻게 가치를 만드는가"
   ❌ 통제 사후 감사(Post-control)             ✅ 통제 설계·예방·검증·개선(PDCA)
```

기술사 관점에서 IT 경영 관리 핵심 토픽은 단순히 ITIL 프로세스를 묻는 것이 아니라, **"거버넌스 체계가 어떻게 비즈니스 목표와 정합(Alignment)을 유지하면서도 Agile·Digital 시대의 변화 속도(Lead Time 30%)와 규제 준수(예: 개인정보보호법 제29조 안전조치, ISO 38500 6원칙)를 동시에 만족시키는가"**를 평가한다.

- **📢 섹션 요약 비유**: 전통 IT 관리는 "자동차의 정기 점검"이었다면, 현대 IT 거버넌스는 "자율주행 차량의 센서·AI·제어 알고리즘 통합 시스템"과 같다. 차가 스스로 목적지(사업 목표)까지 안전·효율·규제 준수(신호·횡단보도) 하에 운행하도록 만드는 것이 거버넌스다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019의 거버넌 시스템(Governance System)은 **Governance Objectives(40개 MGO) + Components(7개) + Focus Areas(맞춤형) + Design Factors(설계변수)**의 4축으로 구성된다. 각 도메인(EDM·APO·BAI·DSS·MEA)은 거버넌스 의사결정(EDM) → 정렬·계획(APO) → 구축·획득(BAI) → 인도·지원(DSS) → 모니터·평가(MEA)의 V-Model을 따른다.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                       COBIT 2019 Core Model                              │
│                                                                          │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌────────┐ │
│  │   EDM    │   │   APO    │   │   BAI    │   │   DSS    │   │  MEA   │ │
│  │ Evaluate │   │ Align·   │   │ Build·   │   │ Deliver· │   │Monitor·│ │
│  │ Direct·  │─▶│   Plan·  │─▶│  Acquire·│─▶│  Support │─▶│Evaluate│ │
│  │ Monitor  │   │ Organize │   │Implement │   │  Service │   │ Assess │ │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘   └───┬────┘ │
│       │  5 MGO       │  14 MGO      │  11 MGO      │  6 MGO      │ 4 MGO│
│       └──────────────┴──────────────┴──────────────┴──────────────┘      │
│                              │                                           │
│                              ▼                                           │
│                7 Components (40개 GO × Component 매핑)                   │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │ ① Principles, Policies, Frameworks  ② Processes (40개)             │ │
│  │ ③ Organizational Structures (RACI)   ④ Information Flows           │ │
│  │ ⑤ People, Skills, Competencies       ⑥ Culture, Ethics, Behavior   │ │
│  │ ⑦ Services, Infrastructure, Apps     (외부 Context)                 │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                              │                                           │
│                              ▼                                           │
│         ┌────────────────────────────────────────────────────┐           │
│         │  Cascade Goal (전략 → 가치 → 위험 → 자원 → 역량)  │           │
│         │  Enterprise Goal 13개 → IT Goal 13개 → MGO 40개    │           │
│         └────────────────────────────────────────────────────┘           │
└──────────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(거버넌스 의사결정)** | IT 가치·리스크·자원 의사결정의 정당성·방향성·감독 책임 | EDM01(거버넌스 체계 수립), EDM02(가치 제공 보장), EDM03(리스크 최적화), EDM04(자원 최적화), EDM05(이해관계자 투명성) — RACI 매트릭스에서 R(Responsible)=이사회·CxO, A(Accountable)=이사회 거버넌스 위원회 |
| **APO(Align·Plan·Organize)** | 전략-전술 정렬, 포트폴리오, 아키텍처, 혁신, 투자, 인적자원 | APO12(리스크 관리) — ISO 31000 연계, APO13(보안 관리) — ISO 27001 통제영역 14개 매핑(93.4%), APO04(혁신) — Stage-Gate + Lean Startup |
| **BAI(Build·Acquire·Implement)** | 솔루션 식별·구축·시험·이행·전이·사용자 수용성 | BAI03(솔루션 관리), BAI11(프로젝트 관리) — PMBOK 7 + PRINCE2 + Agile(Scrum/Kanban) 하이브리드, BAI02(요구사항 관리) — MoSCoW·Kano 모델 |
| **DSS(Deliver·Service·Support)** | 운영·서비스 데스크·연속성·문제·정보 보안 운영 | DSS02(서비스 요청·사고), DSS04(연속성) — ISO 22301 BCMS RTO/RPO, DSS06(보안 운영) — SOC(SIEM/SOAR), ZTA(Zero Trust Architecture) |
| **MEA(Monitor·Evaluate·Assess)** | 성과·내부통제·외부감사·컴플라이언스·보증 | MEA01(성과·동기부여), MEA02(내부통제) — SOX 404, MEA03(컴플라이언스) — ISO 19600 준거, MEA04(보증) — 3LoD(Three Lines of Defense) |
| **Cascade Goal(목표 위계)** | 기업 목표 13개 → IT 목표 13개 → MGO 40개로 분해 | 예: EG01(주주가치 극대화)→ ITG04(정보 기반 의사결정)→ DSS03(문제 관리)·BAI05(조직 변경 관리) |
| **Focus Area(맞춤 영역)** | DevOps·Cybersecurity·Privacy·AI Ethics·ESG 등 신규 영역 확장 | 2023년 COBIT 2019에 추가된 AI·Sustainability·Information Security 패키지 — NIST AI RMF(Govern·Map·Measure·Manage) 매핑 |

**핵심 메커니즘 — 목표 위계(Cascade Goal)와 성숙도 모델(Maturity)**:
기업 목표(EG) 13개는 재무 5 + 고객 5 + 내부 3으로 구분되며, 각 EG는 1:1 또는 N:1로 IT 목표(ITG) 13개에 매핑된다. 예시로 EG06(고객 서비스 품질·가용성) → ITG08(서비스·인프라 제공·지원) → DSS02, DSS05, BAI03, DSS01(운영 관리)가 핵심 MGO가 된다.

성숙도 평가는 CMMI 5단계 또는 ISO 33000 시리즈의 6단계(0:불완전, 1:초기, 2:관리, 3:정의, 4:정량적, 5:최적화)로 측정한다. `Capability Level = Σ(PA Rating × Weight) / Σ(Weight)` 산식으로 산출하며, COBIT 2019는 목표 Capability Level vs 현재 Capability Level의 Gap을 우선순위화하기 위해 **Design Factor(설계변수)**를 사용한다.

- **📢 섹션 요약 비유**: COBIT 2019의 40개 MGO는 병원의 **40개 진료과**와 같다. 환자(기업)가 방문하면 내과(APO), 외과(BAI), 응급실(DSS), 검진센터(MEA), 원무과(EDM)가 협력해서 진단·치료·사후관리를 한다. 거버넌스 설계는 어떤 진료과를 강화하고 어디에 인력을 배치할지 결정하는 "병원장"의 판단과 같다.

---

## Ⅲ. 비교 및 연결

IT 거버넌스를 둘러싼 4대 프레임워크(COBIT 2019, ITIL 4, ISO 38500, CMMI)는 역할·범위·관점이 모두 다르며, 실무에서는 이들을 계층적으로 결합한 **"Layered Governance Model"**이 적용된다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500 (2015)** | **CMMI-DEV v2.0** |
| :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스·관리 통합 프레임워크 | IT 서비스 관리(SM) 모범 사례 | IT 의사결정의 6원칙(책임·전략·수행·규율·적합성·인간행태) | 프로세스 성숙도 평가·개선 |
| **관점** | Enterprise-wide, Business-IT Alignment | Service Value System(SVS), Value Stream 중심 | 3-Tier(거버넌스-관리-운영) | 5-Level Maturity(Initial→Optimizing) |
| **범위** | 거버넌스+관리 (전사) | 서비스 운영·디자인·전환 | 거버넌스 (의사결정) | 개발·운영 프로세스 |
| **구성요소** | 40 MGO + 7 Components + Cascade | 34 Practice, 4D(Discover→Engage→Design→Transition) | 6 Principles(Principle 1~6) | 5 Category, 16 PA(Process Area) |
| **측정** | Capability/Maturity Level (0~5), Goal Cascade | KPI(CSI), Value Stream KPI | Self-Assessment, Maturity Indicator | SCAMPI Appraisals, Benchmark |
| **장점** | 1) 다중 프레임워크 통합 허브 2) 컴플라이언스 매핑(
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 646 / 800

← **이전**: [645. IT 경영 관리 핵심 토픽 645번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/645_it_management_core_topic_645_exam_summary/)
**다음**: [647. IT 경영 관리 핵심 토픽 647번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/647_it_management_core_topic_647_exam_summary/) →

---
