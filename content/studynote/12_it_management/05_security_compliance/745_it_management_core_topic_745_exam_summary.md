+++
title = "745. IT 경영 관리 핵심 토픽 745번 시험 요약 (IT Management Core Topic 745 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 COBIT·ITIL·ISO 27001·BSC·EA를 통합한 **거버넌스-전략-투자-성과-리스크-보안-서비스** 7대 축으로, IT가 사업 가치(Strategic Alignment, Value Delivery)를 창출하도록 통제·조정하는 경영 체계이다.
> 2. **가치**: McKinsey·Gartner 연구에 따르면成熟된 IT 거버넌스 도입 기업은 **IT 투자 ROI 25~40% 향상, IT 비용 15~30% 절감, 프로젝트 실패율 50%↓, 보안사고 대응시간 70%↓**의 정량 효과를 달성한다.
> 3. **판단 포인트**: 기술사 시험의 핵심은 **① COBIT 2019(40개 Governance/Management Objectives)와 ISO 38500의 관계, ② BSC의 4관점(재무·고객·내부프로세스·학습성장) KPI 설계, ③ EA 4-layer(BA/DA/AA/TA) 정합성, ④ In-house vs Outsourcing의 Total Cost of Ownership(TCO) 비교, ⑤ ISMS-P 인증 갱신 주기(3년)와 통제항목(102개)** 간의 통합적 판단 능력이다.

---

## Ⅰ. 개요 및 필요성

정보기술은 단순 비용(Cost)에서 **전략적 자산(Strategic Asset), 더 나아가 사업의 생존 기반**으로 그 역할이 변화했다. 그러나 한국 정보화진흥원의 조사에 따르면 국내 기업의 약 **68%가 IT-Biz 정렬 실패, 62%가 투자 대비 효과 미흡, 71%가 IT 부서의 역할 모호**를 핵심 애로사항으로 지적한다. 이는 IT 부서가 기술 중심(Technology-driven)으로 운영되면서 경영 목표(Strategy-driven)와 괴리가 발생했기 때문이다.

이에 IT 경영관리는 **"IT에 대한 경영(Governance of IT)"** 이라는 관점에서 ISO 38500, COBIT 2019을 통해 의사결정·책임·평가 체계를 수립하고, ITIL로 서비스 운영을, BSC로 성과를, EA로 구조를, ISMS로 보안을 통합 관리하는 체계적 접근을 요구한다. 기술사 시험에서 745번 토픽은 단순 암기가 아닌 **"Why(왜 도입) → What(무엇을) → How(어떻게) → So What(어떤 가치)"** 의 4단계 논리 전개 능력을 평가한다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│         IT 경영관리 7대 축 통합 프레임워크 (IT Management 7-Axis)     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   [사업전략]  ────①Strategic Alignment────►  [IT 전략/포트폴리오]     │
│       │                                          │                  │
│       │  ②Value Delivery    ③Risk Management    │                  │
│       │       │                    │              │                  │
│       ▼       ▼                    ▼              ▼                  │
│   ┌───────────────────────────────────────────────────────┐         │
│   │              IT 거버넌스 의사결정 체계 (COBIT 2019)      │         │
│   │   ┌──────────┬──────────┬──────────┬──────────┐        │         │
│   │   │전략/목표  │성과측정  │리스크관리  │자원관리   │        │         │
│   │   └──────────┴──────────┴──────────┴──────────┘        │         │
│   └───────────────────────────────────────────────────────┘         │
│       │       │                    │              │                  │
│       │  ④Performance Mgmt  ⑤Resource Mgmt  ⑥Service Mgmt          │
│       │       │                    │              │                  │
│       ▼       ▼                    ▼              ▼                  │
│   [BSC/KPI] [조직/인력]    [ITIL/서비스]    [ISMS/보안]              │
│       │       │                    │              │                  │
│       └───────┴────────►  ⑦EA(아키텍처)  ◄────────┘                  │
│                          BA / DA / AA / TA                          │
│                                │                                     │
│                                ▼                                     │
│                    [정보시스템 구현·운영]                              │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

기존의 **"IT = 시스템 구축 + 운영"** 패러다임은 프로젝트 종료 시점에 가치가 소멸했으나, 현대의 **"IT = 사업 enablement + value creation"** 패러다임은 전사적 거버넌스·지속적 성과측정·리스크 통제·서비스 품질 보증을 통해 **IT가 비즈니스 KPI(매출증가율, 고객만족도, 시장점유율, Time-to-Market)에 직접 기여**하도록 요구한다.

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **"배(船)의 선장"** 과 같습니다. 엔진(IT 기술)만 좋다고 목적지(사업 목표)에 도달하는 것이 아니라, 항해도(전략), 나침반(거버넌스), 측량장치(성과측정), 뱃사람 조직(인력), 안전장비(보안), 그리고 선체 설계도(아키텍처)가 모두 맞아야 항해가 성공합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리는 **7대 축(Governance, Strategy, Investment, Performance, Resource, Service, Security & Architecture)** 이 위계적으로 연결된 구조로, 각 축은 고유한 프레임워크와 산출물을 가진다.

```text
┌──────────────── IT 경영관리 계층구조 (4-Tier Governance Model) ────────────────┐
│                                                                              │
│  Tier 1: 의사결정 (Decision) ──── 이사회 / IT Steering Committee             │
│            │  (연 4회, 의사결정 권한: 예산 승인, 포트폴리오 우선순위)            │
│            ▼                                                                 │
│  Tier 2: 통제 (Control) ──────── IT 거버넌스 위원회 / CIO                    │
│            │  (월 1회, COBIT 2019 40개 목표 평가, Risk Appetite 설정)          │
│            ▼                                                                 │
│  Tier 3: 관리 (Management) ───── PMO / 프로세스 오너 / 서비스 매니저          │
│            │  (주 1회, 프로젝트/서비스/보안 운영 통제)                          │
│            ▼                                                                 │
│  Tier 4: 실행 (Execution) ───── 현업 + IT 실무 + 외부 파트너                 │
│            (일일, SLA 준수, 변경관리, 인시던트 대응)                           │
│                                                                              │
│  ┌─────────────── 횡단(Transversal) Layer ───────────────┐                  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │                  │
│  │  │  EA     │ │  ISMS   │ │  ITIL   │ │  BSC/   │    │                  │
│  │  │ 4-Layer │ │ 102항목 │ │ Service │ │ KPI    │    │                  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘    │                  │
│  └──────────────────────────────────────────────────────┘                  │
└──────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** (Control Objectives for Information and Related Technologies) | IT 거버넌스·관리의 통합 프레임워크. **5개 도메인(EDM: Evaluate/Direct/Monitor + 4 Domains: APO/BAI/DSS/MEA) × 40개 Governance & Management Objectives** 구조 | EDM01(거버넌스 체계 수립), EDM02(가치 전달 보장), EDM03(리스크 최적화), EDM04(자원 최적화), EDM05(이해관계자 투명성); **Design Factors 11개(전략, 목표, 위험, 문제, 규모 등)**로 거버넌스 시스템 맞춤 설계 |
| **ITIL 4** (Information Technology Infrastructure Library) | IT 서비스 관리(Service Management) 라이프사이클. **SVS(Service Value System): 34개 Practice + Value Chain(6단계: Plan→Engage→Design→Obtain→Deliver→Improve)** | Incident/PROBLEM/Change Enablement, Service Desk, SLA 99.9% 설정, CSI(Continual Service Improvement) 7단계 프로세스, **SVC(Service Value Chain)** 통해 Value Co-Creation |
| **ISO 27001 / ISMS-P** | 정보보안 경영체계. **Plan-Do-Check-Act(PDCA) + 102개 통제항목(Annex A: A.5~A.18, 14개 영역)** | ISMS-P 인증 3년 갱신, 매년 사후심사, 리스크 평가(Risk Assessment) 필수, **자산 식별 → 위협/취약점 분석 → 영향도/발생가능성 매트릭스 → 통제선택 → SoA(Statement of Applicability) 작성** |
| **BSC (Balanced Scorecard)** | 성과관리 4관점(재무·고객·내부프로세스·학습성장) 균형 KPI. **Kaplan & Norton(1992)** 제안 | Cause-and-Effect 관계, Strategic Map(전략맵), **예: 고객관점(NPS↑) → 내부프로세스(처리시간↓) → 학습성장(교육시간↑) → 재무(매출↑)** 의 전략적 연계 |

### 핵심 메커니즘 (Deep Dive)

**① IT 투자평가 5단계 절차 (Stage-Gate Process)**
1. **아이디어 도출**: 현업/IT가 Business Case 초안 작성
2. **타당성 분석(Feasibility Study)**: B/C 분석, NPV, IRR, Payback Period 산출
   - NPV = Σ[CF_t / (1+r)^t] - I₀
   - IRR: NPV=0 되는 할인율 r
3. **우선순위 결정**: AHP(Analytic Hierarchy Process), Portfoli Matrix(필수/희망/선택)
4. **승인 및 예산 배정**: IT Steering Committee 의결, TCO(Total Cost of Ownership) 산정 (HW+SW+인력+교육+유지보수 5개 영역)
5. **사후평가(Post-Implementation Review, PIR)**: KPI 대 실적 비교, ROI = (Benefits - Costs) / Costs × 100

**② COBIT 2019의 11개 Design Factor**
- DF1~DF3: 기업전략, 목표, 위험 프로파일
- DF4: IT 관련 문제(I&T Related Issues)
- DF5~DF7: 위험원천, 위협, 컴플라이언스 요구
- DF8: 거버넌스 시스템의 역할
- DF9: 정보기술 구현 방식(Cloud, On-premise)
- DF10: IT 채택 전략(First Mover, Follower)
- DF11: 기업 규모

**③ IT 아웃소싱 의사결정 모형 (Make or Buy)**
- **핵심 역량(Core Competency) 보존 원칙**: 차별화 역량은 In-house, 비핵심은 Outsource
- **거래비용 경제학(Transaction Cost Economics)**: 시장거래비용 vs 내부조직비용 비교
- **에이전트 이론**: 도덕적 해이(Moral Hazard) 방지 위한 SLA/계약서 상세화
- **Vendor Lock-in 방지**: Multi-vendor, Open API, Exit Strategy 수립

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **"오케스트라의 지휘자"** 와 같습니다. 바이올린(개발), 트럼펫(운영), 첼로(보안) 등 다양한 악기(IT 기능)가 있지만, 지휘자(거버넌스)가 없으면 불협화음만 나옵니다. 악보(전략), 박자(성과측정), 연습(ITIL), 무대설계(EA), 안전관리(보안)가 조화를 이루어야 아름다운 음악(사업 가치)이 탄생합니다.

---

## Ⅲ. 비교 및 연결

IT 경영관리 영역에서 자주 혼동되는 개념들과 비교를 통해 차이를 명확히 한다.

| 구분 | **COBIT 2019** | **ITIL 4** | **PMBOK 7** | **ISO 27001** |
| :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스·관리 (What/Why) | IT 서비스 관리 (How) | 프로젝트 관리 (How) | 정보보안 경영체계 (What) |
| **적용 범위** | 전사 IT (Enterprise-wide) | IT 서비스 운영 | 단일 프로젝트 | 정보자산 전사 |
| **핵심 산출물** | 40 Goals, Maturity Model | 34 Practice, SVS | 12 Principles, 49 Processes | ISMS 문서, SoA, 102 통제 |
| **관계주체** | 이사회, CIO, 감사 | 서비스 매니저, 운영자 | PM, PMO, Sponsor | CISO, 보안담당 |
| **평가/인증** | Maturity Level 1~5 | ISO 20000 인증 가능 | PMP 자격증 | ISMS-P 국가공인 인증 |
| **PDCA 적용** | EDM(평가/지시/모니터) + APO/BAI/DSS/MEA | Service Value Chain | 5 Process Group + 49 Process | Plan-Do-Check-Act |
| **연계 관계** | 거버넌스 결정 → ITIL 실행 | 서비스 운영 결과 → COBIT 보고 | 프로젝트 성과 → COBIT MEA | 보안 통제 → ITIL 변경관리 |
| **시너지** | **COBIT이 "What", ITIL이 "How"** 를 담당하며 상호보완 | COBIT의 DSS(Deliver, Service, Support) 영역과 중첩 | 프로젝트 이니셔티브가 COBIT의 BAI(Build, Acquire, Implement)에 포함 | COBIT의 EDM03(리스크 최적화) 및 DSS05(보안서비스)와 연계 |

**EA(Enterprise Architecture) 4-Layer 모델과의 통합**

| EA 계층 | 정의 | IT 경영관리 연계 |
| :--- | :--- | :--- |
| **BA (Business Architecture)** | 업무/조직/프로세스 | BPR, BSC 내부프로세스관점 |
| **DA (Data Architecture)** | 데이터 모델, 마스터플랜 | 데이터 거버넌스, MDM(Master Data
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 745 / 800

← **이전**: [744. IT 경영 관리 핵심 토픽 744번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/744_it_management_core_topic_744_exam_summary/)
**다음**: [746. IT 경영 관리 핵심 토픽 746번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/746_it_management_core_topic_746_exam_summary/) →

---
