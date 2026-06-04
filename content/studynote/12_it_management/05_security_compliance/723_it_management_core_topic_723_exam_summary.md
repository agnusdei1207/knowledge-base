+++
title = "723. IT 경영 관리 핵심 토픽 723번 시험 요약 (IT Management Core Topic 723 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 COBIT 2019의 거버넌스 체계(EDM: Evaluate-Direct-Monitor)와 ITIL 4의 서비스 가치사슬(SVC)을 결합하여, **전략-투자-운영-성과**의 폐루프를 통해 IT를 Business Value Engine으로 전환하는 통합관리 프레임워크이다.
> 2. **가치**: 적절한 IT 거버넌스 도입 시 IT 투자 대비 ROI를 평균 20~35% 향상시키고, 프로젝트 실패율을 40%에서 15% 이하로 감소시키며, ISO 38500/COBIT 2019 기반 maturity level 3 도달 시 의사결정 속도가 3~5배 개선된다.
> 3. **판단 포인트**: 중앙집중형(Centralized) vs 분산형(Federated) 거버넌스 모델 선택, Three Lines of Defense(3LoD) 내 통제 책임 배분, 그리고 BCM·PIM·DAMA-DMBOK 간의 영역 충돌 시 우선순위 결정이 핵심 Trade-off이다.

---

## Ⅰ. 개요 및 필요성

정보기술이 업무의 전 영역을 지배하는 VUCA(Volatility, Uncertainty, Complexity, Ambiguity) 환경에서, IT는 더 이상 단순 지원 기능이 아닌 **전략적 핵심자산**으로 재정의되어야 한다. 그러나 한국 정보화진흥원의 조사에 따르면 국내 대기업 IT 과제 중 약 60%가 경영전략과 정렬되지 못해 실패하며, IT 투자 대비 실제 비즈니스 성과 도출률은 30% 수준에 불과하다. 이 격차(Gap)를 해소하기 위해 등장한 것이 **IT 거버넌스(IT Governance)**이며, 이는 단순한 IT 관리(IT Management)를 넘어 의사결정권(Decision Rights), 책임(Accountability), 성과측정(Performance Measurement)의 통합체계로 진화했다.

```text
[ IT 경영관리의 진화 패러다임 ]
                  
   1960s              1980s               2000s              2020s
 ┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
 │ EDP 관리  │ → │ MIS/정보화   │ → │ IT 거버넌스  │ → │ 디지털 거버넌스│
 │Data Proc. │    │  System화    │    │  COBIT 도입  │    │AI·ESG 포함  │
 └──────────┘    └──────────────┘    └──────────────┘    └──────────────┘
       │                │                  │                  │
       ▼                ▼                  ▼                  ▼
  하드웨어 중심    SW·DB 중심       거버넌스 체계       데이터·AI·플랫폼
  "데이터 처리"    "정보 지원"      "가치 창출"        "지속가능 가치"
```

기존 IT 관리 패러다임은 **기술 중심(Silo View)**으로, 각 부서별로 독립된 시스템을 운영하여 중복 투자(평균 25% 중복), 데이터 사일로, 보안 사각지대를 야기했다. 반면 현대의 IT 경영관리는 **가치 중심(Value-driven View)**으로 전환되어, 다음과 같은 통합적 요소들을 포괄한다:

- **전략 정렬(Strategic Alignment)**: Henderson & Venkatraman의 SAMM(Strategic Alignment Model) 기반 IT-비즈니스 정렬
- **가치 제공(Value Delivery)**: IT 투자 포트폴리오의 최적 배분 및 ROI 극대화
- **위험 관리(Risk Management)**: ISO 31000, NIST CSF 기반 통합 리스크 관리
- **자원 관리(Resource Management)**: 인력·예산·인프라의 통합 가시성 확보
- **성과 측정(Performance Measurement)**: BSC(Balanced Scorecard) 기반 4관점 KPI 체계

- **📢 섹션 요약 비유**: IT 경영관리는 자동차의 **'통합 계기판(Integrated Dashboard)'**과 같습니다. 엔진(IT 운영), 연료(데이터), 핸들(전략)만으로는 운전할 수 없으며, 속도·연비·엔진온도·타이어공기압을 한눈에 보여주는 통합 계기판이 비로소 안전하고 효율적인 운행(경영)을 가능케 합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 핵심은 **3개 거버넌스 영역(Governance Area)**과 **5개 관리 프로세스(Management Process)**의 교차 매트릭스로 구성된다. 아래 ASCII 다이어그램은 COBIT 2019의 Governance System Architecture를 기반으로 IT 경영관리 전체 구조를 나타낸다.

```text
        ┌─────────────────────────────────────────────────────────┐
        │         Stakeholder Needs & Value Realization           │
        │   (이해관계자 니즈 → 가치 실현 목표 → 기업목표 연결)      │
        └────────────────────────┬────────────────────────────────┘
                                 │
        ┌────────────────────────▼────────────────────────────────┐
        │              거버넌스 시스템 (Governance System)          │
        │  ┌────────────────────────────────────────────────────┐  │
        │  │  EDM: Evaluate, Direct, Monitor (5개 거버넌스 목표) │  │
        │  │  ├─ EDM01 Governance Framework Setting             │  │
        │  │  ├─ EDM02 Benefits Delivery                        │  │
        │  │  ├─ EDM03 Risk Optimization                        │  │
        │  │  ├─ EDM04 Resource Optimization                    │  │
        │  │  └─ EDM05 Stakeholder Transparency                 │  │
        │  └────────────────────────────────────────────────────┘  │
        │  ┌──────────────────┐  ┌────────────────────────────┐   │
        │  │ Alignment (정렬) │  │ Plan (계획)                │   │
        │  │ Build (구축)      │  │   APO01-APO14 (14개)        │   │
        │  └──────────────────┘  └────────────────────────────┘   │
        │  ┌──────────────────┐  ┌────────────────────────────┐   │
        │  │ Run (운영)        │  │ Monitor (모니터링)         │   │
        │  │  BAI01-BAI11      │  │  DSS01-DSS06 + MEA01-MEA04 │   │
        │  └──────────────────┘  └────────────────────────────┘   │
        └─────────────────────────────────────────────────────────┘
                                 │
        ┌────────────────────────▼────────────────────────────────┐
        │            핵심 구성 요소 (Components)                     │
        │  Process | Structures | Information | People&Skills      │
        │  Culture&Behavior | Goals | Service Infrastructure      │
        └─────────────────────────────────────────────────────────┘
                                 │
        ┌────────────────────────▼────────────────────────────────┐
        │      적용 도메인 (Design Factors & Focus Areas)            │
        │  Strategy | Risk | Security | DevOps | Privacy | Compliance│
        └─────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate-Direct-Monitor)** | 이사회·경영진의 거버넌스 의사결정 체계 | COBIT 2019의 5개 거버넌스 목표(EDM01~05) — Benefit Delivery, Risk Optimization, Resource Optimization을 KPI로 측정. 이사회 사이버보안위원회(예: 사이버감사)와 직접 연결 |
| **APO (Align, Plan, Organize)** | IT 전략·계획·조직·아키텍처 관리 | 14개 프로세스로 구성. APO02(전략), APO04(혁신), APO05(포트폴리오), APO12(위험관리), APO13(보안관리) 등이 핵심 |
| **BAI (Build, Acquire, Implement)** | 솔루션 도입 및 변경 관리 | BAI03(솔루션 도입), BAI06(변경관리), BAI11(프로젝트관리). PRINCE2/PMP와 연계 |
| **DSS (Deliver, Service, Support)** | IT 서비스 운영 및 지원 | ITIL 4의 Service Value Chain(Engage→Design→Obtain→Deliver→Support)과 1:1 매핑. DSS02(서비스요청), DSS03(장애관리) |
| **MEA (Monitor, Evaluate, Assess)** | 성과 측정 및 컴플라이언스 | MEA01(성과 모니터), MEA02(내부통제), MEA03(컴플라이언스), MEA04(감사). ISACA의 CMMI와 연계 |

**IT-Business 정렬의 핵심 메커니즘 (SAMM 모델):**

Henderson & Venkatraman(1993)의 **Strategic Alignment Model(SAMM)**은 4개 영역의 양방향 정렬을 정의한다:

```
                 ┌─────────────────────┐
                 │   BUSINESS STRATEGY │
                 │  (사업 전략)         │
                 └──────┬──────┬───────┘
                        │      │
        ┌───────────────┘      └────────────────┐
        ▼ (External)                            ▼ (Strategy)
  ┌──────────────┐                       ┌──────────────┐
  │  Organization │                       │ IT Strategy  │
  │  & Processes  │  ◀── (Operational)──▶│ & Infra      │
  │ (조직·프로세스)│                       │(IT 전략·인프라)│
  └──────────────┘                       └──────────────┘
```

**성과 측정의 4관점 BSC (Balanced Scorecard, Kaplan & Norton 1992):**

- **재무 관점(Financial)**: IT 투자 ROI, TCO 절감률, OpEx/CapEx 비율
- **고객 관점(Customer)**: 서비스 만족도(CSAT), NPS(Net Promoter Score), SLA 준수율
- **내부 프로세스 관점(Internal Process)**: 변경 성공률, MTTR(Mean Time To Repair), 가용성(Availability)
- **학습·성장 관점(Learning & Growth)**: 직원 역량 지수, 디지털 전환 교육 이수율, 혁신 아이디어 채택률

**📢 섹션 요약 비유**: IT 거버넌스의 EDM-APO-BAI-DSS-MEA 5단계 구조는 **항공기의 비행 사이클(Plan→Build→Fly→Land→Review)**과 같습니다. 이사회가 '비행계획'을 승인(EDM), 파일럿이 '연료·경로 점검'(APO), 정비사가 '기체 조립'(BAI), 조종사가 '운항'(DSS), 관제탑이 '사후 분석'(MEA)을 담당합니다.

---

## Ⅲ. 비교 및 연결

IT 경영관리 영역은 다수의 표준 프레임워크가 공존하며, 실무에서는 이를 **상호 보완적으로 통합**하여 적용한다. 각 프레임워크는 고유한 초점과 적용 범위를 가지므로, 프로젝트 특성에 맞는 조합이 핵심이다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **CMMI / ISO 330xx** |
| :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스·관리 통합 프레임워크 | IT 서비스 관리(SvcM) Best Practice | IT 거버넌스 국제표준(Principles) | 프로세스 성숙도 평가 |
| **대상** | CIO·이사회·감사인 | IT 운영·서비스 데스크 | 경영진·이사회 | 개발·운영 조직 전체 |
| **구조** | EDM + 5개 도메인(40 프로세스) | 34 Practices, 4 Dimension Model | 6 Principles + 5 Tasks | 5단계 Maturity Level |
| **강점** | 컴플라이언스·감사·Risk 통합 | Service Value Chain, 고객가치 중심 | 간결한 원칙(책임·전략·취득·성능·준수·인간행위) | 정량적 성숙도 측정 |
| **약점** | 운영 실무 가이드 부족 | 거버넌스 의사결정 체계 미흡 | 구체적 프로세스 부재 | 거버넌스 측면 결여 |
| **연계 표준** | ISO 27001, NIST CSF, COSO ERM | ISO 20000, DevOps, SIAM | COBIT 2019, King IV | ITIL, TIPA, CMMI-SVC |
| **적용 규모** | 중대규모(Enterprise) | 전 규모 | 전 규모 | 개발조직·IT운영 |

**4대 프레임워크의 통합 관계도:**

```text
        ┌──────────── ISO 38500 ────────────┐
        │  (6 Principles: Responsibility,   │
        │   Strategy, Acquisition,          │
        │   Performance, Conformance,       │
        │   Human Behavior)                 │
        └─────────────┬─────────────────────┘
                      │ 거버넌스 원칙 제공
                      ▼
        ┌──────────── COBIT 2019 ───────────┐  ──▶ 감사·컴플라이언스
        │  (Governance & Management         │       연계: SOX, ISAE 3402
        │   Objectives: 40 Processes)       │
        └─────────────┬─────────────────────┘
                      │ 운영 가이드 제공
                      ▼
        ┌──────────── ITIL 4 ───────────────┐
        │  (Service Value System:           │
        │   Opportunity/Demand/Value)        │
        └─────────────┬─────────────────────┘
                      │ 성숙도 측정
                      ▼
        ┌──────────── CMMI 2.0 ─────────────┐
        │  (Maturity Level 1-5,             │
        │   Performance Areas)              │
        └───────────────────────────────────┘
```

**관련 표준·도구와의 연계:**

- **정보보안**: ISO 27001(보안경영체계) ↔ COBIT DSS05/NIST CSF Identify·Protect·Detect·Respond·Recover
- **프로젝트 관리**: PMBOK 7th, PRINCE2 ↔ COBIT BAI01(Program Mgmt), BAI11(Project Mgmt)
- **아키텍처**: TOGAF 10, ArchiMate 3.2 ↔ COBIT APO03(Managed Architecture)
- **데이터 거버넌스**: DAMA-DMBOK 2.0 ↔ COBIT DSS04(Managed Continuity), APO14(Managed Data)
- **위험 관리**: ISO 31000, COSO ERM 2017 ↔ COBIT EDM03(Managed Risk), APO12

**📢 섹션 요약 비유**: COBIT은 '도시계획도', ITIL은 '도로별 신호체계', ISO 38500은 '헌법 원칙', CMMI는 '발달단계 측정 도구'와 같습니다. 좋은 도시는 이 4가지가 동시에 갖춰질 때 비로소 기능합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

IT 경영관리의 실무 도입은 **거버넌스 성숙도 진단 → 비전 수립
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 723 / 800

← **이전**: [722. IT 경영 관리 핵심 토픽 722번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/722_it_management_core_topic_722_exam_summary/)
**다음**: [724. IT 경영 관리 핵심 토픽 724번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/724_it_management_core_topic_724_exam_summary/) →

---
