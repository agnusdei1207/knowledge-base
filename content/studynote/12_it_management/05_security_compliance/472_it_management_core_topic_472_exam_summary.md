+++
title = "472. IT 경영 관리 핵심 토픽 472번 시험 요약 (IT Management Core Topic 472 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 핵심 토픽 472번은 **IT 거버넌스(Governance)·IT 전략(Strategy)·IT 성과관리(Performance)·IT 서비스 관리(Service Management)를 통합한 4축 프레임워크**로, COBIT 2019의 40개 거버넌스/관리 목적과 ISO/IEC 38500의 6개 원칙, Balanced Scorecard(BSC)의 4관점을 결합하여 **"Value Governance Loop"**를 형성하는 것이다.
> 2. **가치**: 성숙도 Level 1→5 도달 시 **IT 투자 대비 ROI 평균 240% 향상**(Gartner 2023 기준), IT 인시던트 MTTR **68% 단축**, 주요 의사결정 Lead Time **42% 감축**, 그리고 이사회-경영진-IT 부서 간 **"단일 진실 공급원(SSOT, Single Source of Truth)"** 기반의 정량적 의사결정 체계 확보.
> 3. **판단 포인트**: **"Build vs Buy vs Subscribe"** 의사결정에서 5년 TCO 18% 이내, **"Centralized vs Federated vs Hybrid 거버넌스 모델"** 선택에서 조직의 역량 성숙도와 변경 흡수력(Capacity for Change)을 기준으로, **"Push 거버넌스(규제 중심)" vs "Pull 거버넌스(가치 중심)"** 모델 간 균형점을 찾는 것이 핵심 트레이드오프.

---

## Ⅰ. 개요 및 필요성

**IT 경영 관리**란 단순한 IT 운영 관리를 넘어, **"비즈니스 전략 ↔ IT 전략 ↔ IT 포트폴리오 ↔ IT 운영"** 의 4계층을 일관된 가치 흐름(Value Flow)으로 연결하는 경영학 접목 분야이다. 과거 IT 부서는 **"Cost Center(비용 센터)"** 로 인식되어 왔으나, 디지털 전환(DX, Digital Transformation) 시대에는 **"Value Center(가치 센터)"** 로서의 역할이 요구되며, 이는 **"The IT Value Paradox"** — *"IT 없이는 사업이 불가능하지만, IT의 가치를 화폐로 환산하기는 극히 어렵다"* — 라는 본질적 모순을 안고 있다.

이를 해결하기 위해 등장한 것이 **"통합 IT 경영 관리 프레임워크"** 이며, 본 토픽은 다음 4대 핵심 영역을 다룬다:

1. **IT 거버넌스(Governance)**: 의사결정 권한, 책임, 통제 체계 정의 (RACI 매트릭스, 의사결정 라이트 RACI-VS)
2. **IT 전략 및 포트폴리오 관리(SPM)**: 투자 우선순위 결정, 애플리케이션 포트폴리오 분석(APM), EA(Enterprise Architecture) 정렬
3. **IT 성과 관리(Performance Management)**: KPI/KGI 계층화, OKR 기반 정량 측정, BSC 4관점(재무/고객/내부/학습성장) 적용
4. **IT 서비스 관리(Service Management)**: ITIL 4의 34개 Practice, SLA/OLA/UC 통합 관리, SRE(Service Reliability Engineering) 연계

```text
┌────────────────────────────────────────────────────────────────────────────┐
│           IT 경영 관리 통합 프레임워크 (4축 Value Governance Loop)        │
└────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────┐
    │  [1] 이사회·경영진 거버넌스 층 (Governance Layer)            │
    │  · ISO/IEC 38500 6원칙 (Responsibility, Strategy,           │
    │    Acquisition, Performance, Conformance, Human Behavior)   │
    │  · COBIT 2019 EDM 도메인 (EDM01~EDM05)                     │
    │       │                                                     │
    │       ▼                                                     │
    │  [2] IT 전략·포트폴리오 층 (Strategy & Portfolio Layer)     │
    │   · IT 전략 로드맵 (3~5년), Capability Map, Target State EA│
    │   · Portfolio Rationalization (TIRS 2x2 매트릭스)           │
    │   · 투자 분류: Run(60%)/Grow(30%)/Transform(10%)            │
    │       │                                                     │
    │       ▼                                                     │
    │  [3] IT 운영·서비스 층 (Delivery & Service Layer)           │
    │   · ITIL 4 Service Value System (SVS)                       │
    │   · DevOps/SRE 파이프라인, AIOps 기반 인시던트 자동화       │
    │   · SLA 99.95% / MTTR 15분 이내 / MTTD 5분 이내             │
    │       │                                                     │
    │       ▼                                                     │
    │  [4] 측정·피드백 층 (Measurement & Feedback Layer)          │
    │   · KPI/KGI/CSF 계층화 (Strategy Map)                       │
    │   · BSC 4관점, OKR cascade, Real-time Dashboard            │
    │   · PDCA + OODA Loop를 결합한 "Closed-Loop Governance"    │
    │       │                                                     │
    │       └─────── [Feedback / Re-balance] ─────────────────────┘
    └──────────────────────────────────────────────────────────────┘

  [변환 원리]  Governance ──→ Strategy ──→ Execution ──→ Value ──→ Governance'
              (Direction)    (Plan)       (Operate)     (Measure)
```

과거 **"Project-Driven IT"**(프로젝트 중심) 방식은 개별 과제 단위로 ROI를 산정하고 완료 후 폐기되는 **"사일로(Silo)형"** 의사결정이 다수였으나, 본 토픽의 **"Portfolio-Driven IT"**(포트폴리오 중심) 방식은 **"의사결정권자(Decision Owner) → 투자위원회(IIC) → PMO → 실무팀"** 의 계층적 거버넌스를 통해 **의사결정 일관성 85% 이상, 중복 투자 30% 감축** 의 정량적 효과를 달성한다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **"도시의 도시계획(Urban Planning)"** 과 같다. 개별 건물(시스템)만 잘 지을 게 아니라, 상하수도·도로·전기·통신 인프라(거버넌스·표준)까지 통합 설계해야 시민(사업부서)이 불편 없이 살 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. IT 거버넌스 3-모형(Three Models of IT Governance)

Weill & Ross(2004)의 **"IT Governance Three Models"** 가 본 토픽의 이론적 토대이다:

```text
┌────────────────────────────────────────────────────────────────────┐
│        IT 거버넌스 의사결정 5대 영역 (Weill & Ross)              │
│  ① IT 원가/투자 원칙  ② 아키텍처 의사결정                         │
│  ③ IT 인프라 전략    ④ 비즈니스 애플리케이션 needs                │
│  ⑤ IT 투자/우선순위  →  이 5개 영역을 누가, 어떻게 결정하는가?    │
└────────────────────────────────────────────────────────────────────┘

   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
   │  Business    │   │   IT         │   │  Hybrid      │
   │  Monarchy    │   │  Monarchy    │   │  (Feudal/    │
   │  (경영진 독점)│   │  (CIO 독점)  │   │  Federal/    │
   │              │   │              │   │  Duopoly)    │
   │ · 빠른 결정  │   │ · 기술 일관성│   │ · 균형 잡힘  │
   │ · 사업 친화  │   │ · 표준 준수  │   │ · 합의 비용↑ │
   │ · 기술 리스크│   │ · 사업 괴리  │   │ · 최적형     │
   └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             ▼
        ┌──────────────────────────────────────────────┐
        │   의사결정 라이트 (RACI + VS 확장)            │
        │   R: Responsible  A: Accountable              │
        │   C: Consulted   I: Informed                  │
        │   V: Veto 권한   S: Support                   │
        └──────────────────────────────────────────────┘
```

### 2. COBIT 2019 기반 40개 관리 목적의 계층 구조

**Governance Objectives(EDM01~05)** 5개와 **Management Objectives(APO, BAI, DSS, MEA 4도메인)** 35개로 구성된 **40 Governance/Management Objectives** 가 IT 경영 관리의 표준 언어 역할을 한다.

```text
┌────────────────────────────────────────────────────────────────────┐
│                  COBIT 2019 40 Objectives 계층도                  │
└────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────┐
  │  Level 0: Stakeholder Needs & Goals                  │
  │           (이해관계자 니즈 - 13개 목표)               │
  └─────────────────────┬────────────────────────────────┘
                        ▼
  ┌──────────────────────────────────────────────────────┐
  │  Level 1: Enterprise Goals (13개)                    │
  │   EG01 포트폴리오, EG05 재무, EG08 내부 최적화,     │
  │   EG09 비용 최적화, EG13 보안·프라이버시              │
  └─────────────────────┬────────────────────────────────┘
                        ▼
  ┌──────────────────────────────────────────────────────┐
  │  Level 2: IT-related Goals (13개, Alignment Goals)   │
  │   01 IT 준수, 04 정보 위험 관리, 06 비즈니스 민첩성, │
  │   08 포트폴리오 최적화, 09 비용 효율                 │
  └─────────────────────┬────────────────────────────────┘
                        ▼
  ┌──────────────────────────────────────────────────────┐
  │  Level 3: Governance/Management Objectives (40개)    │
  │   EDM: Evaluate, Direct, Monitor (5)                 │
  │   APO: Align, Plan, Organize (14)                    │
  │   BAI: Build, Acquire, Implement (11)                │
  │   DSS: Deliver, Service, Support (6)                 │
  │   MEA: Monitor, Evaluate, Assess (4)                 │
  └─────────────────────┬────────────────────────────────┘
                        ▼
  ┌──────────────────────────────────────────────────────┐
  │  Level 4: Process Components (7개)                   │
  │   · Process Practices  · Information Flows           │
  │   · People, Skills     · Policies/Procedures         │
  │   · Culture/Behavior   · Services/Infrastructure    │
  │   · Goals/Metrics                                   │
  └──────────────────────────────────────────────────────┘
```

### 3. 핵심 구성 요소 매트릭스

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **이사회 IT 위원회 (IT Steering Committee)** | 거버넌스 의사결정 최고 기구 | 정족수 2/3, 분기 1회 정례 + 임시, 안건: 투자 5천만원 이상, RACI에서 'A' 보유, Veto 권한 행사 가능자 명시 |
| **CIO/CDO/CTO 트라이어드** | IT·데이터·기술 전략 총괄 | C-Level 3인 합의제, **"Two-in-a-Box"** 모델 (CIO+CTO) 또는 트라이어드 모델, 직접 보고 체계(CEO 직보) 권장 |
| **PMO (Project Mgmt Office)** | 프로젝트·프로그램 포트폴리오 통제 | 3-tier(Strategic/Operational/Tactical), P3O(Portfolio, Programme, Project Office) 기반, **PPM Tool**(ServiceNow SPM, Planview) 활용 |
| **EA (Enterprise Architecture)** | 기술 표준·통합·재사용성 관리 | TOGAF ADM 8단계 + Zachman 6x6 매트릭스, **ArchiMate 3.2** 모델링, **"4-Layer EA"(Business/App/Data/Tech)** 정렬 |
| **SMO (Service Management Office)** | ITIL 프로세스 거버넌스 | ITIL 4 **34 Practices** 중 18개 핵심 운영, **SLA/OLA/UC** 3단 계층, ServiceNow/Remedy ITSM 도구 |
| **KPI/KGI 운영 체계** | 성과 측정·피드백 | Balanced Scorecard 4관점 + OKR Cascade, **"Lead vs Lag"** 지표 구분, **Real-time Dashboard**(Tableau, Power BI, Grafana) |
| **Risk & Security 거버넌스** | IT 리스크·보안 통제 | ISO 27005 리스크 관리, **3-Lines of Defense Model**(1: 운영, 2: 리스크/컴플라이언스, 3: 내부감사) |
| **FinOps & TBM** | IT 비용 최적화 | **"Showback/Chargeback"** 모델, **TBM(Tech Business Management)** Taxonomy, 클라우드 비용 최적화(AWS CUR, Azure Cost Mgmt) |

### 4. IT 성과 측정 계층 (Performance Measurement Hierarchy)

본 토픽의 가장 핵심적인 알고리즘적 원리는 **"KPI Cascade"** 이다.

```
[비즈니스 목표] EG: 매출 15% 성장
        ↓ (alignment)

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 472 / 800

← **이전**: [471. IT 경영 관리 핵심 토픽 471번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/471_it_management_core_topic_471_exam_summary/)
**다음**: [473. IT 경영 관리 핵심 토픽 473번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/473_it_management_core_topic_473_exam_summary/) →

---
