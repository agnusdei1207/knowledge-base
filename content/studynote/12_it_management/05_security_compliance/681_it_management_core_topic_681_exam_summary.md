+++
title = "681. IT 경영 관리 핵심 토픽 681번 시험 요약 (IT Management Core Topic 681 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(IT Governance)는 ISO 38500의 **EDM(Evaluate·Direct·Monitor)** 3대 원칙과 COBIT 2019의 **40개 관리 목표(Governance & Management Objectives)**를 통해 IT가 비즈니스 전략(Strategy)과 정렬(Alignment)되어 가치(Value)를 창출하고 리스크(Risk)를 최적화하도록 **이사회-경영진-IT** 간 의사결정 권한과 책임(Accountability)을 체계화한 통합 프레임워크이다.
> 2. **가치**: McKinsey & Company(2023) 보고에 따르면 체계적 IT 거버넌스 도입 기업은 **디지털 전환 성공률 1.8배**, **IT 투자 ROI 평균 27% 향상**, **보안 사고 대응 시간(MTTR) 62% 단축**, **컴플라이언스 위반 비용 45% 절감**의 정량적 효과를 달성하며, ITIL 4 기반 운영 통합 시 IT 서비스 가용성 **99.95% → 99.99%(Four 9s)** 수준으로 도약한다.
> 3. **판단 포인트**: **①** 중앙집중형(Centralized, CoE) vs 분산형(Decentralized, Federated) 거버넌스 모델, **②** COBIT 2019의 11개 디자인 팩터(Design Factors) 중 핵심 5개(전략, 목표 cascade, 위험 profile, I&T 관련 이슈, 위협 landscape) 우선 적용, **③** IT 비용의 70% 이상을 차지하는 레거시(Mainframe) 유지 vs 클라우드 전환의 TCO 3~5년 회수기 tradeoff, **④** Zero Trust + SASE 도입과 거버넌스 통합 시 NHI(Non-Human Identity) 관리 복잡도 증가에 대한 통제 설계가 핵심 의사결정 분기점이다.

---

## Ⅰ. 개요 및 필요성

정보화 사회의 진화와 4차 산업혁명(AI, IoT, Blockchain, Cloud)의 가속화로 인해 IT는 더 이상 단순한 **지원(Support) 기능**이 아닌 기업의 **핵심 경쟁력(Core Competency)**이자 **생존 인프라**로 자리잡았다. Gartner(2024) 조사 결과 글로벌 Fortune 500 기업의 IT 예산이 전체 매출 대비 평균 **5.8%(금융권 12.4%, 제조업 3.2%)**에 달하며, 이 중 **31%**가 디지털 전환에 투입된다. 그러나 McKinsey(2023)에 따르면 이巨额 투자 중 **70%**가 실패 또는 부분 성공에 그친다. 실패의 근본 원인은 **①IT-Business Alignment 부재, ②이해관계자 간 책임 소재 불명확, ③리스크 관리 체계 부재, ④가치 측정 메커니즘 부재**의 4대 거버넌스 부재로 귀결된다.

**기존 통념 vs 새로운 패러다임**:
| 시대 | IT 인식 | 거버넌스 | 통제 방식 |
|------|---------|----------|-----------|
| 1990s 이전 | **Cost Center** (비용 센터) | 없음(Ad-hoc) | 수작업 Audit |
| 2000s (SOx Act 2002) | **Service Center** | ITIL v2 기반 | 프로세스 매핑 |
| 2010s (Cloud 1.0) | **Strategic Partner** | COBIT 5 + ISO 38500 | Risk-Based Control |
| 2020s (AI/Cloud Native) | **Value Driver** | **COBIT 2019 + NIST CSF 2.0 + ISO 38500:2024** | **Continuous Assurance + AI-Augmented GRC** |

```text
┌──────────────────────────────────────────────────────────────────────┐
│         IT 거버넌스 3-레이어 통합 참조 모델(Reference Model)         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ╔═══════════════════ Tier 1: 전략 의사결정 계층 ═══════════════╗  │
│  ║  Board of Directors → IT Steering Committee(ISC)             ║  │
│  ║  ├─ CEO  ├─ CIO  ├─ CFO  ├─ CISO  ├─ CDO(Chief Data Officer)║  │
│  ║  역할: EDM 원칙 (ISO 38500)                                  ║  │
│  ║   E: Evaluate(평가) → D: Direct(지시) → M: Monitor(모니터)  ║  │
│  ╚════════════════════════════════════════════════════════════╝  │
│                              ↓ Policy & Strategy                    │
│  ╔═══════════════════ Tier 2: 거버넌스 시스템 계층 ═══════════╗   │
│  ║  ┌─────────────┬─────────────┬─────────────┬────────────┐   ║   │
│  ║  │  COBIT 2019 │   ITIL 4    │  ISO 38500  │ NIST CSF   │   ║   │
│  ║  │  40 Gov&Mgt │  34 Practices│  EDM 원칙   │  6 Functions│   ║   │
│  ║  │  Objectives │  SVS 모형    │  6 Principles│ Govern~Recover║  │
│  ║  └─────────────┴─────────────┴─────────────┴────────────┘   ║   │
│  ║   + TOGAF(EA), ISO 27001(ISMS), PCI-DSS, GDPR/PIPA         ║   │
│  ╚════════════════════════════════════════════════════════════╝   │
│                              ↓ Control Objectives                    │
│  ╔═══════════════════ Tier 3: 운영·실행 계층 ═════════════════╗   │
│  ║  DevOps Pipeline │ AIOps Platform │ GRC Tool(Archer/SAP GRC)║  │
│  ║  Cloud(AWS/Azure)│ SAP/ERP Core  │ ITSM(ServiceNow/BMC)     ║  │
│  ║  ZTA/SASE        │ Data Lake     │ K8s/Container Platform   ║  │
│  ╚════════════════════════════════════════════════════════════╝   │
│                              ↑ Feedback (Telemetry & Audit)        │
└──────────────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: IT 거버넌스는 **도시의 도시계획(Urban Planning)**과 같다. 건물(IT 시스템) 하나하나가 아무리 좋아도, 도시 전체의 **상하수도(데이터 흐름), 도로(네트워크), 소방(이사 대응), 세무(컴플라이언스)** 설계가 부재하면 도시는 무너진다. COBIT는 도시기본계획, ISO 38500는 도시헌장, ITIL은 도로교통 운영매뉴얼에 해당한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 거버넌스의 핵심은 **"누가(Who) 무엇을(What) 어떻게(How) 결정하고 측정할 것인가"**의 3원칙을 정의하는 것이다. **ISO/IEC 38500:2024**(IT 거버넌스 국제표준, 1차 2008 → 2차 2015 → 리비전 2024)는 이를 6대 원칙으로 명시한다: **①Responsibility(책임성), ②Strategy(전략), ③Acquisition(취득), ④Performance(성과), ⑤Conformance(준수), ⑥Human Behavior(인적 행동)**. COBIT 2019는 이를 5개 도메인(**EDM, APO, BAI, DSS, MEA**)과 **40개 관리 목표(Governance Objectives 5 + Management Objectives 35)**로 구체화한다.

### COBIT 2019 5개 도메인 상세 동작 메커니즘

```text
   ┌──────────────────────────────────────────────────────────┐
   │              COBIT 2019 Core Model 계층 구조              │
   ├──────────────────────────────────────────────────────────┤
   │                                                          │
   │   ┌─────── EDM (Evaluate, Direct, Monitor) ──────┐      │
   │   │  EDM01: 거버넌스 체계 설정 및 유지              │      │
   │   │  EDM02: 가치가 전달되도록 보장                 │      │
   │   │  EDM03: 리스크 최적화 보장                     │      │
   │   │  EDM04: 자원 최적화 보장                       │      │
   │   │  EDM05: 이해관계자 투명성 보장                 │      │
   │   └─────────────┬────────────────────────────────┘      │
   │                 ↓ (Direct)                                │
   │   ┌─────── APO (Align, Plan, Organize) ────────────┐      │
   │   │  APO01~14: 14개 관리 목표 (전략 정렬, 계획, 조직) │      │
   │   └─────────────┬────────────────────────────────┘      │
   │                 ↓ (Plan)                                  │
   │   ┌─────── BAI (Build, Acquire, Implement) ────────┐      │
   │   │  BAI01~11: 11개 관리 목표 (구축, 도입, 구현)     │      │
   │   └─────────────┬────────────────────────────────┘      │
   │                 ↓ (Implement)                             │
   │   ┌─────── DSS (Deliver, Service, Support) ────────┐      │
   │   │  DSS01~06: 6개 관리 목표 (서비스 운영·지원)     │      │
   │   └─────────────┬────────────────────────────────┘      │
   │                 ↓ (Measure)                               │
   │   ┌─────── MEA (Monitor, Evaluate, Assess) ────────┐      │
   │   │  MEA01~04: 4개 관리 목표 (모니터링, 평가, 감리)  │      │
   │   └────────────────────────────────────────────────┘      │
   └──────────────────────────────────────────────────────────┘
```

| 구성 요소 (도메인) | 역할 (거버넌스 관점) | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (거버넌스)** | 이사회/경영진 차원의 의사결정·감독 | RACI Matrix 기반 책임 할당, ISO 38500 EDM 사이클(연 4회 분기별 회의), GRC 플랫폼(Archer, ServiceNow GRC) 통합 |
| **APO (정렬·계획)** | 전략과 IT 목표의 Cascade 및 조직 설계 | Balanced Scorecard 4관점(재무/고객/내부/학습), **Porter 전략 분석 + Ward & Peppard EA 방법론**, I&T 목표를 사업 KPI에 1:N 매핑 |
| **BAI (구축·도입)** | 솔루션 설계·개발·테스트·전환 | **DevSecOps 파이프라인**(GitOps, SAST/DAST, SBOM), TOGAF ADM(Architecture Development Method) Phase B-F, Change Advisory Board(CAB) 운영 |
| **DSS (운영·지원)** | 일상의 IT 서비스 전달 및 사용자 지원 | **ITIL 4 Service Value System(SVS)**: 34개 Best Practice(Service Desk, Incident, Problem, Change Enablement), **AIOps** (Moogsoft, Splunk ITSI) anomaly detection |
| **MEA (모니터링)** | 성과 측정·
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 681 / 800

← **이전**: [680. IT 경영 관리 핵심 토픽 680번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/680_it_management_core_topic_680_exam_summary/)
**다음**: [682. IT 경영 관리 핵심 토픽 682번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/682_it_management_core_topic_682_exam_summary/) →

---
