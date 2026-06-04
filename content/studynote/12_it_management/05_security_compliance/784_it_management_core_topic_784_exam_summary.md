+++
title = "784. IT 경영 관리 핵심 토픽 784번 시험 요약 (IT Management Core Topic 784 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ISO/IEC 38500, ITIL 4, Balanced Scorecard (BSC) 등 글로벌 거버넌스 프레임워크를 기반으로 비즈니스 전략과 IT 투자·운영·리스크를 정렬(Strategic Alignment)하여 기업 가치(Enterprise Value)를 극대화하는 종합 관리 체계임.
> 2. **가치**: McKinsey & Company(2023) 보고에 따르면 효과적인 IT 거버넌스 체계 구축 조직은 디지털 전환 성공률이 2.4배 높으며, IT 투자 대비 ROI는 평균 27% 향상, 사이버 리스크로 인한 손실은 약 60% 감소 효과를 보임.
> 3. **판단 포인트**: 기술사적 핵심 판단은 (1) 중앙집중형(Centralized) vs 분산형(Distributed) 거버넌스 모델 선택, (2) Agile-Fed-Scaled(SAFe) 기반 운영 모델과의 정합성, (3) ESG(Environmental, Social, Governance) 시대의 IT 비재무 성과 측정 가능성, (4) 생성형 AI 도입에 따른 IT 포트폴리오 재편 전략임.

---

## Ⅰ. 개요 및 필요성

디지털 전환(Digital Transformation)이 기업의 생존 전략이 된 4차 산업혁명 시대에서, IT는 단순 비용 센터(Cost Center)에서 **전략적 비즈니스 인에이블러(Strategic Business Enabler)**로 그 역할이 근본적으로 변화함. 그러나 한국정보화진흥원이 발간한 「2024년 디지털전환 실태조사」에 따르면 국내 대기업 중 68.3%가 "IT-Biz 정렬 실패"를 DX 과제의 1순위 장애요인으로 지목하고 있으며, 중소·중견기업의 경우 이 수치가 81.7%에 달함.

특히 2024~2025년은 (1) EU AI Act(2024.8 시행), (2) 한국 개인정보보호법 개정(2023.9, 가명정보 활용), (3) 클라우드 보안인증制度(CSAP) 고도화, (4) ISO/IEC 42001(AI 경영시스템) 국제표준화 등 IT 거버넌스를 둘러싼 규제 환경이 급변하는 시점임. 이러한 환경에서 IT 경영 관리의 본질은 **"기술 도입"이 아닌 "가치 실현(Value Realization)"**이며, 이를 위해 End-to-End 거버넌스 체계 확립이 필수적임.

```text
┌──────────────────────────────────────────────────────────────────────┐
│           기업 거버넌스 → IT 거버넌스 → IT 운영체계 (3-Layer Model)   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [Layer 1: Enterprise Governance]                                    │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  Board ──→ CEO ──→ CxO(CDO/CIO/CTO/CISO)                       │ │
│  │   │                                                            │ │
│  │   └── ESG·이사회 보고·리스크위원회·감사위원회                  │ │
│  └────────────────────────────────────────────────────────────────┘ │
│         │ 평가(Evaluate) · 지시(Direct) · 모니터(Monitor)            │
│         ▼                                                            │
│  [Layer 2: IT Governance (ISO 38500 / COBIT 2019)]                  │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  ◉ 책임(Responsibility)  ◉ 전략(Strategy)  ◉ 획득(Acquisition)│ │
│  │  ◉ 성능(Performance)     ◉ 적합성(Conformance) ◉ 인적행태      │ │
│  └────────────────────────────────────────────────────────────────┘ │
│         │ 관리·조율                                                    │
│         ▼                                                            │
│  [Layer 3: IT Management (ITIL 4 / DevOps / SRE)]                   │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  Service Value System(SVS) → Value Chain → Practices(34개)    │ │
│  │  Plan → Build → Engage → Design & Transition → Obtain/Build   │ │
│  │  Deliver & Support → Improve                                  │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ※ 기술사 논점: 3계층 간 KPI/RACI/Metric의 정합성 설계             │
└──────────────────────────────────────────────────────────────────────┘
```

**구(舊) vs 신(新) 패러다임 비교**:
- **구(1990~2010)**: ITIL v2/v3 기반 프로세스 중심 → Tier 1·2·3 분리 → SLA(서비스수준협약) 위주 → "IT 부서의 품질 관리" 관점
- **신(2019~현재)**: ITIL 4 + COBIT 2019 + SAFe + SRE 융합 → 가치 흐름(Value Stream) 중심 → SLO/SLI/SLI 기반 경험 품질(QoE) → "전사(全社)의 가치 공학(Value Engineering)" 관점

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **오케스트라의 지휘자**와 같습니다. 바이올린(IT 운영), 첼로(보안), 트럼펫(개발) 등 다양한 악기(부서)가 각자 실력은 출중해도, 지휘자(거버넌스) 없이는 하모니(기업 가치)를 만들 수 없으며, 악보(전략) 없이는 공연(사업) 자체가 불가능합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리 체계는 **5대 핵심 영역(Domain)**과 **3대 메커니즘(Mechanism)**으로 구성됨. 본 절에서는 COBIT 2019의 Governance & Management Objectives를 중심으로 아키텍처를 해부함.

```text
┌─────────────────────────────────────────────────────────────────────┐
│         COBIT 2019 - 40개 Governance & Management Objectives        │
│         + ISO 38500 6원칙 + ITIL 4 SVS 통합 참조 모델               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [Domain 1] EDM ──→ Evaluate, Direct, Monitor (5 Objectives)        │
│       │      거버넌스 의사결정: 투자 우선순위, 리스크 허용수준       │
│       ▼                                                              │
│  [Domain 2] APO ──→ Align, Plan, Organize (14 Objectives)            │
│       │      전략 정렬, 포트폴리오 관리, 예산, 아키텍처, 혁신,       │
│       │      인적자원, 관계, 서비스 합의, 벤더관리, 품질, 리스크,    │
│       │      보안, 데이터, 호환성                                    │
│       ▼                                                              │
│  [Domain 3] BAI ──→ Build, Acquire, Implement (11 Objectives)        │
│       │      프로그램/프로젝트 관리, 요구사항, 솔루션, 품질보증,    │
│       │      변경, 조직변화, 수용, 구성, 자산, 모니터링              │
│       ▼                                                              │
│  [Domain 4] DSS ──→ Deliver, Service, Support (6 Objectives)         │
│       │      운영, 서비스 요청/사고/문제, 연속성, 보안서비스,        │
│       │      비즈니스 프로세스 통제                                  │
│       ▼                                                              │
│  [Domain 5] MEA ──→ Monitor, Evaluate, Assess (4 Objectives)         │
│       │      성과/내부통제/외부보증/규제 준수                        │
│       ▼                                                              │
│  [Continuous] ──→ 프로세스 활동의 7단계 (PGMF: Process Goal Mngmt)  │
│       ① Practice Identification → ② Purpose → ③ Goal Cascade      │
│       → ④ Process Practices → ⑤ Capability Levels(0~5)             │
│       → ⑥ Performance Management → ⑦ Success Factors                │
│                                                                      │
│  ★ 핵심 공식: Capability Level = f(PA: Process Attribute 점수)      │
│    Level 0(불완전) → 1(초기) → 2(관리) → 3(확립) → 4(예측) → 5(최적)│
└─────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(평가·지시·모니터링)** | 이사회·CxO 레벨 의사결정 체계 | COBIT 2019 EDM Domain 5개 Objective(예: EDM02 - Benefits Realization)와 BSC 4관점(재무/고객/내부/학습성장) 연결, 매월/매분기 거버넌스 리뷰 |
| **APO(정렬·계획·조직)** | IT 전략 기획·포트폴리오·예산 | TOGAF ADM(Architecture Development Method) Phase A~F, Stage-Gate 모델, GARTNER Magic Quadrant 기반 벤더 선정, 예산 결정 시 **TCO(Total Cost of Ownership)** 5개년 모델 + **VOI(Value of Investment)** 정성평가 병행 |
| **BAI(구축·획득·구현)** | 솔루션/서비스 구축 및 변경 | SAFe(Scaled Agile Framework) PI Planning 8~12주 단위, DevOps 파이프라인(CI/CD), AIOps 기반 배포 자동화, 무중단 배포(Blue-Green/Canary) |
| **DSS(서비스·지원·운영)** | 일상의 IT 서비스 제공 | ITIL 4 34개 Practices 중 Incident/Change/Release/SLM 등, AIOps(ITSM Tools: ServiceNow, BMC Helix), SRE Golden Signals(Latency, Traffic, Errors, Saturation) |
| **MEA(모니터링·평가·감사)** | 통제 및 컴플라이언스 | ISO 27001(보안), SOX(내부통제), ISMS-P(개인정보), 내부감사(Internal Audit), KPI 대시보드(Power BI/Grafana) |

### 핵심 측정 지표 및 알고리즘

**① IT 운영 성숙도 측정 (COBIT PAM: Process Assessment Model)**

```
Capability Level = Σ(PA 점수 × 가중치) / 7개 Process Attribute
  - PA 1: Process Performance (목표 달성)
  - PA 2: Work Product Management
  - PA 3: Process Definition
  - PA 4: Process Deployment
  - PA 5: Process Measurement
  - PA 6: Process Control
  - PA 7: Process Innovation
  ※ 0~100% 점수 → 5단계(0~5) 매핑
```

**② BSC-IT 4관점 KPI 예시**
- **재무**: IT 비용/매출 비율(%), ROI, NPV(순현재가치), Payback Period
- **고객**: 사용자 만족도(CSAT), Net Promoter Score(NPS), 서비스 가용률(%)
- **내부 프로세스**: MTTR(평균복구시간), Change Failure Rate(%), Deployment Frequency
- **학습·성장**: 직원 1인당 교육시간, 핵심 인재 유지율, 기술 스킬 매트릭스 갭

**③ 가치 흐름 최적화 - DORA Metrics + 확장 지표**
- Deployment Frequency → Elite: 1일 다수, High: 주 1~일 1, Medium: 월 1~주 1, Low: 6개월 이상
- Lead Time for Changes, Change Failure Rate, MTTR, Reliability(가용률 99.99%)

- **📢 섹션 요약 비유**: COBIT 2019의 5개 Domain은 마치 **병원 진료 체계**와 같습니다. EDM은 진료 방향을 결정하는 **진료위원회**, APO는 환자별 **치료 계획**, BAI는 **수술/시술**, DSS는 **회복/입원 케어**, MEA는 **사후 검진 및 의료감사**에 해당하며, 이 5단계가 끊김 없이 흘러야 환자의 건강(기업 가치)이 회복됩니다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 영역에서 혼동하기 쉬운 핵심 프레임워크/개념을 명확히 구분함. 기술사 시험에서 가장 빈번하게 출제되는 비교 영역임.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **IT Balanced Scorecard** |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 통합 프레임워크 | IT 서비스 관리(SM) 모범사례 | IT 거버넌스 국제표준(원칙) | 전략적 성과 측정·관리 |
| **관리 범위** | 전사 IT 거버넌스(End-to-End) | 서비스 운영·지원(SVO 중심) | 이사회·경영진 의사결정 원칙 | IT 성과 평가 및 전략 실행 |
| **구성** | 40 Governance/Management Objectives | 34 Practices + SVS(Value Chain) | 6개 원칙 + 모델(Direct/Monitor) | 4관점(재무/고객/내부/학습) |
| **적용 주체** | CIO·IT Manager·감사인 | 서비스 데스크·운영팀 | 이사회·CxO·비IT 임원 | 전략기획·IT 전략팀 |
| **측정 방식** | Capability Level(0~5), KPI 200+ | SLO/SLI, CSI 등록부 | 원칙 준수 여부(Maturity) | 원인-결과 맵 + 인과관계 |
| **핵심 가치** | "I&T 거버넌스 + 관리 + 통제" | "서비스 가치 공학" | "책임·전략·적합성·인적행태" | "전략→측정→실행 정렬" |
| **생성형 AI 대응** | AI 거버넌스 Objective 1.1 추가 | AI Service Desk Practice | ISO/IEC 42001 별도 표준화 | AI ROI 관점 신설 |
| **법적/감사** | SOX, ISMS 감사 연계 | 인증 제도 없음(자발적) | 한국 IT 거버넌스 법(2023) | BSC 자체는 인증 없음 |

### 타 시스템·도구 통합 (Integration)

```text
┌────────────────────────────────────────────────────────────────┐
│        IT 거버넌스 프레임워크 통합 아키텍처                    │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐        │
│   │  ISO 38500  │   │  COBIT 2019 │   │   ITIL 4    │        │
│   │   (원칙)    │◄─►│ (프레임워크)│◄─►│ (운영모범)  │        │
│   └─────────────┘   └──────┬──────┘   └─────────────┘        │
│         │                  │                  │                │
│         └──────────────────┼──────────────────┘                │
│                            ▼                                   │
│                ┌───────────────────────┐                        │
│                │  조직 맞춤형 거버넌스  │                        │
│                │  체계(Governance       │                        │
│                │  System)              │                        │
│                └───────────┬───────────┘                        │
│                            │                                   │
│         ┌──────────────────┼──────────────────┐                │
│         ▼                  ▼                  ▼                │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐         │
│  │  ERP/CRM   │   │  ITSM Tool  │   │  GRC Platform│        │
│  │ (SAP/Oracle)│   │ (ServiceNow)│   │ (Archer/Opt) │         │
│  └─────────────┘   └─────────────┘   └─────────────┘         │
│         │                  │                  │                │
│         └──────────────────┼──────────────────┘                │
│                            ▼                                   │
│                  ┌──────────────────────┐                      │
│                  │  Enterprise Dashboard │                     │
│                  │  (Power BI/Grafana)  │                      │
│                  └────────────────────
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 784 / 800

← **이전**: [783. IT 경영 관리 핵심 토픽 783번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/783_it_management_core_topic_783_exam_summary/)
**다음**: [785. IT 경영 관리 핵심 토픽 785번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/785_it_management_core_topic_785_exam_summary/) →

---
