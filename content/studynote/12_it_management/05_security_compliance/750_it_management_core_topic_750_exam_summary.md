+++
title = "750. IT 경영 관리 핵심 토픽 750번 시험 요약 (IT Management Core Topic 750 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리의 핵심은 COBIT 2019, ITIL 4, ISO 38500, TOGAF 등 글로벌 거버넌스 프레임워크를 기반으로 **기업 전략-아키텍처-운영-평가(Value Delivery)**를 하나의 사슬로 통합하여, IT가 사업 목표(Business Goal)에 정렬(Alignment)된 가치(Value)를 창출하도록 통제하는 것이다.
> 2. **가치**: 정량적으로는 IT 투자 대비 ROI 20~30% 개선, 프로젝트 실패율 50% 감소, 인시던트 MTTR 40% 단축, 정성적으로는 의사결정 투명성·이해관계자 신뢰·규제 준수(컴플라이언스)·디지털 전환 가속화를 동시에 달성한다.
> 3. **판단 포인트**: 중앙집중형 vs 분산형 거버넌스 모델 선택, Agile/DevOps 환경에서의 거버넌스 경량화(Governance-as-Code), Cobit의 40개 관리 목표(APO/BAI/DSS/MEA/EDM 5개 도메인) 중 조직 성숙도에 맞는 우선순위 결정, 그리고 사이버보안·ESG·개인정보보호 규제(GDPR, PIPA) 통합 통제 설계가 핵심 trade-off이다.

---

## Ⅰ. 개요 및 필요성

**IT 경영관리(Information Technology Governance & Management)**는 기업이 IT 자원을 전략적 자산으로 활용하여 비즈니스 가치를 극대화하고, 리스크를 통제하며, 이해관계자에게 책임(Accountability)을 이행하도록 하는 **의사결정 및 통제 체계**이다. ISO/IEC 38500:2015는 이를 *"현재 및 미래의 방향 설정(Present and Future Direction Setting)"*을 통해 조직의 IT 활용을 **평가(Evaluate)·지도(Direct)·모니터(Monitor)**하는 3원칙으로 정의한다.

기술사 시험에서 본 토픽이 핵심으로 다뤄지는 이유는, 4차 산업혁명·클라우드 전환·AI 도입이 가속화되면서 전통적인 IT 운영 방식(Waterfall, On-premise, Silo 조직)으로는 **디지털 비즈니스 요구사항에 실시간 대응이 불가능**해졌기 때문이다. 과거에는 IT가 "비용 센터(Cost Center)"였으나, 현재는 **"비즈니스 enable러"이자 "전략적 차별화 수단"**으로 위치가 완전히 재정의되었다. Gartner(2023)에 따르면, 디지털 비즈니스 전환을 추진한 기업의 73%가 IT 거버넌스 미비로 초기 ROI를 달성하지 못했다고 보고된다.

본 토픽은 **전략(Strategy) → 아키텍처(Architecture) → 구축/전이(Build/Transition) → 운영(Operate) → 평가(Evaluate)**로 이어지는 IT 가치사슬(Value Chain) 전체를 포괄하며, 특히 한국 환경에서는 **전자정부법, 클라우드컴퓨팅법, 개인정보보호법, 정보통신망법, ISMS-P 인증** 등 강력한 규제 환경과 결합되어 보다 구조화된 접근을 요구한다.

```text
[IT 경영관리의 3대 축 — 전략·아키텍처·운영의 통합]
┌──────────────────────────────────────────────────────────────┐
│  Enterprise Vision & Mission (기업 비전)                      │
└──────────────────────┬───────────────────────────────────────┘
                       │ ↓ Business Strategy
        ┌──────────────┴──────────────┐
        │                             │
   ┌────▼─────┐                  ┌────▼──────┐
   │ IT       │  ←─Alignment──→  │ Business  │
   │ Strategy │                  │ Capability │
   │ (EA/TOGAF)│                  │ (BPM)      │
   └────┬─────┘                  └────┬───────┘
        │                             │
        │    ┌─────────────────┐      │
        └───►│ Governance Core │◄─────┘
             │  (COBIT 2019)   │
             │  (ISO 38500)    │
             └────────┬────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
   │ Service │   │ Project │   │ Risk &  │
   │ Mgmt    │   │ & Port- │   │ Security│
   │ (ITIL4) │   │ folio   │   │ (ISMS)  │
   │         │   │ (PMO)   │   │         │
   └────┬────┘   └────┬────┘   └────┬────┘
        │             │             │
        └─────────────┼─────────────┘
                      ▼
        ┌────────────────────────────┐
        │  Value Realization (가치실현) │
        │  ROI, NPS, MTTR, SLA, KPI  │
        └────────────────────────────┘
```

- **고전적 IT 관리(1990~2005)**: ITIL v2 기반의 프로세스 중심, Reactive 운영, 분절된 사일로 조직, CapEx 중심 투자, Technical KPI 위주.
- **현대 IT 경영관리(2020~현재)**: ITIL 4 + COBIT 2019 + SRE/DevOps 통합, Proactive & Predictive, E2E Value Stream, OpEx(클라우드) + CapEx 하이브리드, Business Outcome KPI 통합.

- **📢 섹션 요약 비유**: IT 경영관리는 자동차의 **'통합 계기판(Instrument Cluster) + 자율주행 제어 시스템'**과 같다. 속도(성과), 연료(예산), 엔진온도(리스크), 항로(전략)를 실시간 통합 모니터링하여 운전자가 비즈니스 의도대로 주행하도록 돕는 두뇌 회로이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 기술적 아키텍처는 크게 **4계층(Governance Layer, Management Layer, Operational Layer, Technology Layer)**으로 구성된다. 각 계층은 **RACI 매트릭스(Responsible/Accountable/Consulted/Informed)**와 **정보 흐름(Information Flow)**로 연결된다.

```text
[IT 거버넌스 4계층 아키텍처 및 핵심 프레임워크 매핑]

┌────────────────────────────────────────────────────────────┐
│  L1. Governance Layer — 의사결정 및 책임 (Evaluate/Direct) │
│  ─────────────────────────────────────────────────────────│
│   - 이사회(Board) / IT Steering Committee / CxO            │
│   - 프레임워크: ISO 38500, COBIT 2019 EDM 도메인          │
│   - 산출물: IT 정책(Policy), 표준(Standard), 거버넌스 헌장 │
└─────────────────────────┬──────────────────────────────────┘
                          │ ↑ 보고(Reporting) / ↓ 지시(Direction)
┌─────────────────────────▼──────────────────────────────────┐
│  L2. Management Layer — 계획/조직/통제 (Plan/Build/Run)   │
│  ─────────────────────────────────────────────────────────│
│   - CIO, IT-PMO, EA Office, CISO Office                    │
│   - 프레임워크: COBIT 2019(40 Governance/Management Obj), │
│                 TOGAF ADM, ITIL 4 SVS(34 Practices)        │
│   - 산출물: 전략맵, EA 청사진, 서비스 카탈로그, KPI 대시보드│
└─────────────────────────┬──────────────────────────────────┘
                          │ API/데이터/프로세스 인터페이스
┌─────────────────────────▼──────────────────────────────────┐
│  L3. Operational Layer — 서비스/프로젝트/리스크 운영      │
│  ─────────────────────────────────────────────────────────│
│   - 서비스데스크, 데브옵스팀, SOC, GRC 플랫폼 운영팀       │
│   - 프레임워크: ITIL 4(Service Value Chain), Scrum/SAFe,  │
│                 NIST CSF, ISO 27001, ISO 31000             │
│   - 산출물: Incident/Change Log, 빌드 파이프라인, GRC 리포트│
└─────────────────────────┬──────────────────────────────────┘
                          │ IaC/메트릭/텔레메트리
┌─────────────────────────▼──────────────────────────────────┐
│  L4. Technology Layer — 인프라/플랫폼/데이터             │
│  ─────────────────────────────────────────────────────────│
│   - Multi-Cloud(AWS/Azure/GCP), K8s, Service Mesh(Istio),│
│     Data Lake, Observability(Prometheus/Grafana/ELK)       │
│   - 구현: Terraform, Ansible, ArgoCD, Open Policy Agent    │
│   - 산출물: 인프라 메트릭, 트레이스, 로그, 보안 이벤트     │
└────────────────────────────────────────────────────────────┘
```

### COBIT 2019의 5개 도메인 핵심 메커니즘 (40 Management Objectives)

COBIT 2019는 **EDM(Evaluate, Direct, Monitor) 5개 + APO(Align, Plan, Organize) 14개 + BAI(Build, Acquire, Implement) 11개 + DSS(Deliver, Service, Support) 6개 + MEA(Monitor, Evaluate, Assess) 4개** 총 40개 관리목표로 구성된다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate/Direct/Monitor)** | 거버넌스 의사결정 | 이사회·CxO가 IT 성과와 리스크를 평가·지시·감독. **예: EDM02 (Benefits Realization), EDM03 (Risk Optimization), EDM04 (Resource Optimization), EDM05 (Stakeholder Transparency)** |
| **APO (Align/Plan/Organize)** | 전략 정렬·계획 | **APO01(관리체계)**, APO04(혁신), APO05(포트폴리오), APO12(리스크관리), APO13(보안관리). Balanced Scorecard 4관점(Financial/Customer/Internal/Learning) 기반 KPI 설계 |
| **BAI (Build/Acquire/Implement)** | 솔루션 구축·전이 | **BAI01(관리프로그램)**, BAI02(요구사항정의), BAI03(솔루션설계), BAI11(프로젝트관리). Agile/Safe/PI Planning, CI/CD 파이프라인 통합 |
| **DSS (Deliver/Service/Support)** | 서비스 운영·지원 | **DSS01(운영관리)**, DSS02(서비스요청/사고), DSS03(문제관리), DSS04(연속성), DSS05(보안운영). SLA·OLA·UC(Service Level Agreement/Operational Level Agreement/Underpinning Contract) 3단 구조 |
| **MEA (Monitor/Evaluate/Assess)** | 성과 측정·평가 | **MEA01(성과모니터)**, MEA02(내부통제), MEA03(외부준수), MEA04(문제사항). 내부감사, ISMS-P 인증 심사, GRC(Governance-Risk-Compliance) 도구 |

### ITIL 4 Service Value System (SVS)

ITIL 4의 핵심은 7가지 **Guiding Principle**(Focus on value, Start where you are, Progress iteratively, Collaborate, Think holistically, Keep it simple, Optimize) 및 **34개 Practice**(Service Management Practice 17 + Technical/General/Organization Management Practice 17)를 **Service Value Chain(SVC)**: Plan→Improve→Engage→Design&Transition→Obtain/Build→Deliver&Support의 6개 Activity로 연결하는 것이다.

### Value Goal Cascade (BMC, Capability, Practices → Outcome)

COBIT 2019의 **가치 흐름(Value Goal Cascade)** 메커니즘은 다음 수식으로 표현된다:

```
Stakeholder Needs → Enterprise Goals(13EA) → Alignment Goals(13AG) →
IT Goals(13IT) → Governance Objectives(40) → Process Activities(250+)
```

**핵심 KPI 산출 공식** (기술사 시험 빈출):
- **TCO (Total Cost of Ownership)**: `TCO = CapEx + OpEx + 간접비(Indirect Cost)`. 평균 IT 자산의 TCO 중 HW 27%, SW 19%, 운영인력 35%, Down-time 19% 비율 (Gartner 2022).
- **ROI**: `ROI(%) = (Net Benefit / Total Cost) × 100`. 정보화 사업의 경우 평균 ROI는 3년 기준 145%(KISD 2023).
- **NPV (순현재가치)**: `NPV = Σ [CFₜ / (1+r)ᵗ] - Initial Investment`. 할인율(r) 산정 시 WACC(Weighted Avg Cost of Capital) 적용.
- **SLA 가용성(Availability)**: `Availability(%) = (MTBF / (MTBF + MTTR)) × 100`. 99.99% (Four Nine) = 연간 downtime 52.6분.

### 정보 흐름 및 의사결정 사이클

```text
[Plan-Do-Check-Act(PDCA) 기반 IT 거버넌스 사이클]

        ┌─────────────── Plan ───────────────┐
        │ 전략수립, EA 로드맵, 포트폴리오 우선순위화│
        └───────────────────┬──────────────┘
                            ▼
        ┌─────────────── Do ──────────────────┐
        │ 프로젝트 착수, 솔루션 구축, 서비스 제공│
        └───────────────────┬──────────────┘
                            ▼
        ┌─────────────── Check ───────────────┐
        │ KPI 모니터링, 내부감사, SLA 측정      │
        └───────────────────┬──────────────┘
                            ▼
        ┌─────────────── Act ─────────────────┐
        │ 시정조치, 지속적 개선(Kaizen), 학습전파│
        └───────────────────┬──────────────┘
                            │
                            └──────→ (Plan으로 피드백 루프)
```

- **📢 섹션 요약 비유**: COBIT 2019의 5개 도메인은 마치 **비행기의 5대 핵심 시스템(EDM=조종석, APO=비행계획, BAI=엔진·동체조립, DSS=운항, MEA=블랙박스·진단장비)**과 같다. 각 시스템이 고장나면 비행(사업)에 치명적 영향을 주며, 이들을 통합 운영하는 것이 CIO의 임무다.

---

## Ⅲ. 비교 및 연결

### IT 거버넌스 프레임워크 비교

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **TOGAF 10** | **CMMI v2.0** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | 거버넌스 + 관리 통합 (What/Why) | 서비스 관리 실무 (How) | 이사회 수준 거버넌스 원칙 | 엔터프라이즈 아키텍처 방법론 | 프로세스 성숙도 평가·개선 |
| **대상 계층** | CxO/이사회~현장 | 서비스 운영/매니저 | 이사회·최고경영진 | EA 아키텍트·전략기획 | SW/서비스 개발조직 |
| **핵심 구조** |
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 750 / 800

← **이전**: [749. IT 경영 관리 핵심 토픽 749번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/749_it_management_core_topic_749_exam_summary/)
**다음**: [751. IT 경영 관리 핵심 토픽 751번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/751_it_management_core_topic_751_exam_summary/) →

---
