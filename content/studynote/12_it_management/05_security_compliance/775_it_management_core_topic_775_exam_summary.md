+++
title = "775. IT 경영 관리 핵심 토픽 775번 시험 요약 (IT Management Core Topic 775 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 핵심 토픽 775번은 **COBIT 2019 거버넌스 체계**, **ITIL 4 서비스 가치 시스템(SVS)**, **ISO 38500 IT 거버넌스 국제표준**을 통합 관점에서 이해하고, **IT-비즈니스 정렬(Strategic Alignment)**, **가치 전달(Value Delivery)**, **리스크 최적화(Risk Optimization)**, **자원 관리(Resource Management)**, **성과 측정(Performance Measurement)**의 5대 도메인 균형점을 설계하는 능력을 평가하는 시험이다.
> 2. **가치**: 체계적 IT 거버넌스 도입 시 **프로젝트 실패율 40% → 15% 감소**(Standish Group CHAOS Report 기준), **IT 투자 대비 ROI 20~35% 향상**, **컴플라이언스 위반 비용 평균 60% 절감**, 그리고 **IT-비즈니스 정렬 성숙도(L成熟度) Level 2(Opens) → Level 4(Managed)** 도달을 통한 의사결정 속도 3배 향상을 달성할 수 있다.
> 3. **판단 포인트**: 가장 큰 트레이드오프는 **중앙집중형 거버넌스(COBIT 5단계 메타러니 모델)** vs **연방형 거버넌스(Federated, RACI 매트릭스 분산)**의 선택이며, 조직 규모·업종·규제 강도에 따라 **디자인 팩터(Design Factors)** 11개 중 우선순위를 결정해야 한다. 또한 **ISO 38500의 6원칙(Evaluate, Direct, Monitor)**과 **COBIT 2019의 40개 관리목표(Management Objective)** 간 매핑 설계가 실무 핵심이다.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리는 단순한 "IT 부서 운영"이 아니라 **기업 전체의 전략적 의사결정 체계**에 IT를 통합하는 경영학문이다. 과거 1990년대까지는 CIO(Chief Information Officer)가 기술 도입에 집중했다면, 2000년대 이후 **사이버보안 위협 증가**(2017년 WannaCry, 2020년 SolarWinds, 2023년 MOVEit), **클라우드 전환 가속화**(AWS, Azure, GCP 3사 시장지배), **규제 강화**(GDPR 2018, 개인정보보호법 2023 개정, DORA 2024), **ESG 공시 의무화**(ISSB S1/S2, 2024년 한국 도입)에 따라 IT는 더 이상 비용센터(Cost Center)가 아닌 **전략적 자산(Strategic Asset)**이자 **리스크 소스(Risk Source)**로 재정의되었다.

시험 775번은 이러한 환경 변화 속에서 **"어떤 IT 거버넌스 프레임워크를 선택하고, 어떻게 조직에 맞게 커스터마이징하며, 어떻게 성과를 측정할 것인가"**를 다룬다. 특히 기술사 답안에서는 단순 암기가 아닌 **상황별 의사결정 논리(Decision Logic)**와 **아키텍처 통합 설계 능력**을 요구한다.

```text
┌────────────────────────────────────────────────────────────────────────┐
│           IT 경영 관리 3대 축 (Three Pillars of IT Management)        │
└────────────────────────────────────────────────────────────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐       ┌──────────────────┐       ┌──────────────────┐
│ ① 거버넌스    │       │ ② 서비스 관리    │       │ ③ 투자/포트폴리오│
│   Governance  │       │   Service Mgmt   │       │   Portfolio Mgmt │
│               │       │                  │       │                  │
│ - COBIT 2019  │       │ - ITIL 4 SVS     │       │ - IT BSC         │
│ - ISO 38500   │       │ - SIAM           │       │ - TCO/ROI        │
│ - KING 4      │       │ - DevOps         │       │ - Real Options   │
│               │       │   (CALMS)        │       │ - Stage-Gate     │
│ 목적: 의사결정│       │ 목적: 가치 전달  │       │ 목적: 자원 배분  │
│ 권한/책임 구조│       │ 프로세스 최적화  │       │ 우선순위 결정    │
└──────┬────────┘       └─────────┬────────┘       └─────────┬────────┘
       │                          │                          │
       └──────────────────────────┼──────────────────────────┘
                                  │
                                  ▼
                ┌──────────────────────────────────┐
                │   비즈니스 목표(Business Goals)  │
                │   - 수익성 25%↑                 │
                │   - 고객만족 NPS +15pt          │
                │   - 컴플라이언스 100%           │
                │   - Time-to-Market -30%         │
                └──────────────────────────────────┘
```

**왜 지금 IT 경영 관리가 필수인가?**

| 시대 | 패러다임 | 핵심 이슈 | 대표 실패 사례 |
|:---:|:---:|:---|:---|
| 1980~90 | **데이터 처리 중심**<br>(DP Era) | 메인프레임 TCO, Y2K | London Ambulance Service (1992) |
| 2000~10 | **프로세스 자동화**<br>(ERP Era) | ERP 통합 실패율 70% | Hershey's SAP 프로젝트 (1999, $112M 손실) |
| 2010~20 | **디지털 전환**<br>(DX Era) | 클라우드 마이그레이션, 모바 우선 | Healthcare.gov (2013, 장애 6주) |
| 2020~현재 | **AI·데이터·지속가능성**<br>(AI-Native Era) | 생성형 AI 거버넌스, ESG, 회복탄력성 | SolarWinds (2020, 18,000고객 침해) |

- **📢 섹션 요약 비유**: IT 경영 관리는 **자동차의 핸들·브레이크·내비게이션**과 같다. 핸들(거버넌스)이 없으면 차는 방향 없이 달리고, 브레이크(리스크관리)가 없으면 사고가 나며, 내비게이션(전략) 없이는 목적지에 도달하지 못한다. 775번 시험은 이 세 가지가 어떻게 맞물려 작동하는지를 묻는 시험이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 **COBIT 2019의 거버넌스 시스템(Governance System) + ITIL 4의 서비스 가치 체인(SVC) + ISO 38500의 3과업 모델**을 통합한 **"3-Layer IT Management Reference Model"**로 이해할 수 있다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│                Layer 1: 전략 거버넌스 계층 (Strategic)              │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  이사회/IT 전략위원회 → COBIT 2019 EDM(평가·지시·모니터)  │   │
│   │   ├─ EDM01: 거버넌스 프레임워크 설정 (RACI: 이사 100%)    │   │
│   │   ├─ EDM02: 가치 전달 보장 (Portfolio Prioritization)     │   │
│   │   └─ EDM03: 리스크 최적화 (Risk Appetite 정의)            │   │
│   │   ─ ISO 38500 6원칙 매핑 ─                                │   │
│   │   Responsibility(책무) | Strategy(전략) | Acquisition(획득)│   │
│   │   Performance(성과) | Conformance(준수) | Human(인적행위) │   │
│   └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼ (Cascade: 전략 → 목표)
┌─────────────────────────────────────────────────────────────────────┐
│               Layer 2: 운영 관리 계층 (Operational)                  │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  CIO/IT 부서장 → COBIT 2019 APO/BPO/MEA + ITIL 4 SVS       │   │
│   │   ├─ APO(Align, Plan, Organize) 14개 관리목표              │   │
│   │   │   • APO01: IT 관리 프레임워크 (IASA CISA 매핑)        │   │
│   │   │   • APO04: 혁신 관리 (TOGAF ADM 연계)                 │   │
│   │   │   • APO12: 리스크 관리 (ISO 27005 연계)               │   │
│   │   ├─ BPO(Build, Procure, Implement) 11개 관리목표         │   │
│   │   │   • BAI01: 관리 프로그램 (Stage-Gate 모델)            │   │
│   │   │   • BAI03: 투자 결정 관리 (NPV/IRR 분석)             │   │
│   │   └─ MEA(Monitor, Evaluate, Assess) 5개 관리목표         │   │
│   │       • MEA01: 성과/준거성 모니터링 (KPI/SLA 대시보드)   │   │
│   └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼ (Cascade: 목표 → 실행)
┌─────────────────────────────────────────────────────────────────────┐
│                Layer 3: 서비스 실행 계층 (Execution)                 │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  서비스 팀/엔지니어 → ITIL 4 Service Value Chain (SVC)     │   │
│   │   Plan → Improve → Engage → Design&Transition             │   │
│   │   → Obtain/Build → Deliver&Support (34개 실무 프로세스)   │   │
│   │                                                             │   │
│   │   ├─ DevOps 파이프라인 (CI/CD: Jenkins, GitLab, ArgoCD)    │   │
│   │   ├─ AIOps 플랫폼 (Datadog, Dynatrace, Splunk)            │   │
│   │   └─ FinOps 도구 (CloudHealth, Kubecost)                  │   │
│   └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **이사회·IT거버넌스위원회 (ISG/ITSC)** | 최고 의사결정 기구, 정렬·감독 책임 | 연 4회 정례회의, COBIT EDM 3개 관리목표, **RACI 매트릭스에서 Accountable(A)** |
| **COBIT 2019 Core Model** | 40개 관리목표(Management Objective) + 5개 도메인 | **카스케이드(Goals Cascade)**: 기업목표 13개 → 정렬목표 13개 → 관리목표 40개. **디자인 팩터 11개**로 조직별 맞춤 설계 (예: DF1: 전략, DF3: 위험도, DF11: IT 도입 방식) |
| **ITIL 4 Service Value System (SVS)** | 서비스 가치 창출을 위한 운영 프레임워크 | **서비스 가치 사슬(SVC) 6활동**: Plan→Improve→Engage→Design&Transition→Obtain/Build→Deliver&Support. **34개 실무 프로세스** (예: 인시던트 관리, 변경 관리, 서비스 데스크) |
| **ISO 38500 IT Governance** | 국제표준 기반 거버넌스 원칙 | **6원칙** (Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior) + **3과업 모델**: Evaluate(평가) → Direct(지시) → Monitor(모니터링) |
| **IT Balanced Scorecard (IT BSC)** | 전략 실행을 위한 4관점 성과 측정 | **Nolan/Norton 4관점**: 기업기여(71%)·사용자(15%)·운영(8%)·미래(6%) 가중치. **예시 KPI**: Time-to-Market, IT 비용/매출 비율, 사용자 만족도(CSI), 시스템 가용성(99.95%) |

### 핵심 메커니즘: Goals Cascade (목표 연쇄)

COBIT 2019의 가장 중요한 원리는 **13개 기업목표 ↔ 13개 IT 정렬목표 ↔ 40개 관리목표**를 1:N:M으로 매핑하는 것이다. 예를 들어:

- **기업목표 #01: 고객만족도 향상** → **정렬목표 #07: 고객 서비스 품질** → **관리목표 DSS02**(서비스 요청 처리), **DSS03**(인시던트 해결) → **KPI**: First Call Resolution Rate(70%↑), MTTR(Mean Time To Restore, 4시간→30분)

### COBIT 2019 디자인 팩터 11개 (시험 핵심)

| 번호 | 디자인 팩터 | 영향받는 관리목표 수 | 적용 시나리오 |
|:---:|:---|:---:|:---|
| DF1 | **전략(Enterprise Strategy)** | 전체 | 성장전략(Aggressive) vs 안정전략(Conservative)에 따라 우선순위 변경 |
| DF2 | **목표(Enterprise Goals)** | 전체 | 13개 기업목표 중 상위 5개 선정 → 관련 관리목표 집중 |
| DF3 | **리스크 프로파일(Risk Profile)** | APO12, DSS05 등 | 사이버 리스크 High 조직 → EDM03, APO12, DSS05 강화 |
| DF4 | **이슈/문제 관련 우려** | APM/DSS 전반 | 레거시 시스템 비중 40%↑ → BAI03(투자결정) 강화 |
| DF5 | **규제 준수(Compliance)** | MEA02, MEA03 | 금융업(PIPL, GLBA, DORA) → 컴플라이언스 관리목표 100% 적용 |
| DF6 | **IT 도입 방식(Technology Adoption)** | BAI, DSS | 클라우드 네이티브 vs 하이브리드에 따라 BAI09(SLA) 변경 |
| DF7 | **IT 운영 모델** | DSS 전체 | 인하우스 vs 아웃소싱(SIAM) → DSS01(계약관리) 조정 |
| DF8 | **IT 도입 전략** | BAI03, BAI11 | Greenfield(신규) vs Brownfield(전환) |
| DF9 | **기업 규모** | 전체 조직계수 | 중소기업 → APO01 단순화, 대기업 → APO05(투자포트폴리오) 정교화 |
| DF10 | **자원 가용성
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 775 / 800

← **이전**: [774. IT 경영 관리 핵심 토픽 774번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/774_it_management_core_topic_774_exam_summary/)
**다음**: [776. IT 경영 관리 핵심 토픽 776번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/776_it_management_core_topic_776_exam_summary/) →

---
