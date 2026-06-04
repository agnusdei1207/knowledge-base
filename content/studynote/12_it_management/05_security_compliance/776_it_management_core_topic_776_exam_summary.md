+++
title = "776. IT 경영 관리 핵심 토픽 776번 시험 요약 (IT Management Core Topic 776 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019(거버넌스·관리목표 40개), ITIL 4(SVS 34개 실무), PMBOK 7(8개 성과영역), ISO 27001/20000 등 글로벌 표준 프레임워크를 기반으로, **전략-아키텍처-운영-성과**의 4계층 정렬(Strategic Alignment Maturity Model, SAMM)을 통해 비즈니스 가치(Value)와 리스크 통제(Risk Optimization)를 동시 극대화하는 통합 거버넌스 체계이다.
> 2. **가치**: McKinsey & Company(2023) 조사에 따르면 성숙한 IT 거버넌스 기업은 **TCO 23% 절감, Time-to-Market 38% 단축, 디지털 ROI 2.4배 향상**, ISACA(2022) 보고서 기준 COBIT 2019 도입 기업은 **감사 적발 건수 67% 감소, 컴플라이언스 비용 41% 절감**, Gartner(2024) 예측에 따르면 2026년 A등급 거버넌스 기업의 EBITDA는 5.7%p 우위를 보인다.
> 3. **판단 포인트**: **① 거버넌스 vs 관리(Governance vs Management) 경계 설정** — 의사결정 권한(RACI)과 책임 소재 명확화, **② 프레임워크 조합(COBIT+ITIL+ISO) 시 중복 통제 중복 적용 회피**, **③ KPI/KGI 계층화(North Star Metric -> OKR -> KPI)**, **④ 투자 포트폴리오(Run-Grow-Transform 70-20-10) 균형**, **⑤ Shadow IT(연간 IT 지출의 30~40%) 통제 전략**이 기술사의 핵심 판단 영역이다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX) 가속화와 클라우드·AI·데이터 경제의 부상으로, IT 부서는 단순 비용센터(Cost Center)에서 **전략적 가치 창출 센터(Value Driver)**로 역할이 전환되었다. 한국정보화진흥원(KIAT, 2023) 자료에 따르면 국내 중견기업 이상 **87%가 디지털 전환 과제를 진행** 중이나, 이 중 **38%만이 명확한 IT 거버넌스 체계를 보유**하고 있어 투자 대비 성과(ROI)가 미흡한 실정이다.

특히 **DORA(DevOps Research and Assessment)** 지표 — Deploy Frequency, Lead Time for Changes, Change Failure Rate, Time to Restore Service — 와 같은 기술 지표와 **BSC(Balanced Scorecard)** 의 4관점(재무·고객·내부프로세스·학습성장) 지표가 통합되지 않으면, IT 투자의 **5% 중 56%가 "Wealth Wasted"(낭비된 투자)**로 귀결된다(Standish Group CHAOS Report 2020, 성공률 31.1%).

```text
+----------------------------------------------------------------------+
|          IT 경영 관리 4계층 정렬 프레임워크 (SAMM 5단계)            |
+----------------------------------------------------------------------+
|                                                                      |
|   [Layer 1] 전략 계층 (Strategic)                                   |
|   +------------------------------------------------------------+    |
|   |  BSC/OKR -> ISP(정보전략계획) -> 디지털 전환 로드맵          |    |
|   |  KPI: ROI, NPV, EVA(경제적부가가치)                       |    |
|   |  도구: ISO 38500, COBIT 2019 EDM Domain                    |    |
|   +------------------------------------------------------------+    |
|                          ^v 정렬(Alignment)                          |
|   [Layer 2] 아키텍처 계층 (Architectural)                          |
|   +------------------------------------------------------------+    |
|   |  EA(엔터프라이즈 아키텍처) -> TOGAF ADM 8단계              |    |
|   |  Zachman 6x6 프레임워크, FEAF, DoDAF                       |    |
|   |  산출물: SBP/CBP/ASP(Application·Data·Tech·Business)     |    |
|   +------------------------------------------------------------+    |
|                          ^v 정렬(Alignment)                          |
|   [Layer 3] 거버넌스·운영 계층 (Governance & Operation)             |
|   +------------------------------------------------------------+    |
|   |  COBIT 2019 (40 Gov&Mgt Obj) + ITIL 4 SVS (34 Practices) |    |
|   |  PMBOK 7 (8 Performance Domains) + ISO 20000/27001       |    |
|   |  RACI, RACI-VS, RASCI 매트릭스로 권한·책임 정의           |    |
|   +------------------------------------------------------------+    |
|                          ^v 정렬(Alignment)                          |
|   [Layer 4] 성과·리스크 계층 (Performance & Risk)                   |
|   +------------------------------------------------------------+    |
|   |  KPI Tree (CSF->KPI->KPI 측정) + GRC(Governance·Risk·Comp) |    |
|   |  ISO 31000 리스크 관리 + NIST CSF 2.0 + 사이버 보험      |    |
|   |  모니터링: CMMI, COBIT Performance Mgmt (Maturity 0-5)   |    |
|   +------------------------------------------------------------+    |
|                                                                      |
|   ※ SAMM 5단계: Initial(1) -> Repeated(2) -> Defined(3)              |
|                -> Managed(4) -> Optimized(5) (ISACA Capability Model) |
+----------------------------------------------------------------------+
```

**기존 vs 새로운 패러다임 비교:**
- **기존 (2000년대 이전)**: IT는 백오피스 지원, CapEx 중심(자체 인프라 60%+), **사일로(Silo) 조직** — 개발팀·운영팀·보안팀 간 책임 전가, 연간 예산 1회 결정, TCO 기준 5년 ROI 미달 시 손절.
- **신규 (2020년대 이후)**: IT는 사업 핵심, **OpEx + CapEx 혼합**(클라우드 60%+), **DevSecOps + SRE + Platform Engineering** 통합 조직, **Product-centric P&L**(제품 단위 손익), **FinOps**(클라우드 비용 최적화), 연속적(Continuous) 투자 결정.

- **📢 섹션 요약 비유**: IT 경영 관리는 **자동차의 계기판 + 운전면허 시스템**과 같습니다. COBIT은 도로교통법(규칙), ITIL은 정비 매뉴얼(운영), PMBOK은 네비게이션(프로젝트), ISO 27001은 블랙박스(보안)입니다. 이 네 가지가 동시에 작동해야 차(기업)가 목적지(전략)까지 사고 없이(리스크 통제) 연비 좋게(비용 효율) 도착합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **4대 글로벌 프레임워크의 상호운용성**과 **5단계 성숙도 모델**을 통한 점진적 고도화이다.

```text
+----------------------------------------------------------------------+
|         4대 프레임워크 통합 참조 모델 (Integrated Reference Model)   |
+----------------------------------------------------------------------+
|                                                                      |
|        +--------------+      +--------------+                       |
|        |   COBIT 2019 |◄----►|    ITIL 4    |                       |
|        | (거버넌스)   |      |  (서비스운영)|                       |
|        | 40 Obj/5 Dom |      | 34 Practices |                       |
|        +------+-------+      +------+-------+                       |
|               |                     |                                |
|               |   +--------------+  |                                |
|               +--►|   PMBOK 7    |◄-+                                |
|               |   |(프로젝트관리)|                                   |
|               |   |8 Perf Domain |                                   |
|               |   +------+-------+                                   |
|               |          |                                            |
|               |   +------v-------+                                   |
|               +--►| ISO 27001/  |                                    |
|                   |   20000     |                                    |
|                   | (보안/품질) |                                    |
|                   +-------------+                                    |
|                                                                      |
|   공통 프로세스 매핑:                                                 |
|   • 변경 관리(Change Mgmt): COBIT BAI03 ↔ ITIL CHG ↔ PMBOK IC ↔  |
|                              ISO 20000 SM 9.5                       |
|   • 인시던트 관리: COBIT DSS02 ↔ ITIL INC ↔ ISO 20000 IM           |
|   • 리스크 관리: COBIT EDM03 ↔ PMBOK Risk ↔ ISO 27005/31000       |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 (거버넌스)** | IT 투자·리스크·자원 최적화를 이사회 수준에서 통제 | **40 Governance/Management Objectives**를 5개 도메인(EDM, APO, BAI, DSS, MEA)으로 분할. **Capability Level 0~5** 모델(PA 1.1~5.2, 7단계 PAM 프로세스 능력 모델)로 성숙도 측정. **Design Factors 11개**(전략, 목표, 리스크, 이슈, 위험사태, 컴플라이언스, 역할, IT 이슈, 아키텍처, 기술, 규모)를 5단계로 매핑하여 거버넌스 시스템 맞춤 설계. |
| **ITIL 4 (서비스 운영)** | IT 서비스의 end-to-end 라이프사이클 관리 및 가치 공동창조 | **Service Value System (SVS)** 구조 — Opportunity/Demand -> Value -> Organization/People/Partners/Information/Technology -> **Value Chain(Plan->Engage->Design->Obtain->Build->Transition->Deliver->Support) -> Continual Improvement**. 34개 관리 실무(14 General + 17 Service + 3 Technical Practice) 적용. |
| **PMBOK 7 (프로젝트 관리)** | 프로젝트의 성공적 수행 및 비즈니스 가치 실현 | **8개 성과영역**(Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty). **12가지 원칙**(Stewardship, Team, Development, Planning, Uncertainty, Value, Quality, Complexity, Risk, Adaptability, Change, Effectiveness). **Adaptive(Agile/Hybrid)/Predictive** 두 가지 개발 접근법. |
| **ISO 27001/20000 (보안/품질)** | 정보보안경영시스템(ISMS) 및 IT 서비스경영시스템(ITSMS) 인증 | **ISO 27001:2022**: 93개 통제 항목(Annex A), 4가지 테마(조직 37, 사람 8, 물리적 14, 기술 34), **Statement of Applicability(SoA)** 필수. **ISO 20000-1:2018**: 10개 프로세스 그룹, PDCA 사이클(Plan-Do-Check-Act), 서비스 카탈로그·SLA·연속성·릴리스 관리. **감사 주기 3년(재인증)+연간 서베이랑스**. |
| **PMO (프로젝트관리사무국)** | 프로젝트·프로그램·포트폴리오 통합 거버넌스 | **3가지 유형**: Supportive(자문형), Controlling(통제형), Directive(지시형). **P3O(Portfolio, Programme, Project Office)** 모델, **EVA(Earned Value Analysis)** CPI/SPI 지표(CPI>1.0 양호, SPI>1.0 일정 양호) 적용. |

**핵심 메커니즘 — Capability Maturity Model 통합 (CMMI 2.0 + COBIT PAM):**
- **Level 0: Incomplete** — 프로세스 미식별
- **Level 1: Performed** — 프로세스 식별
- **Level 2: Managed** — 작업 산출물 관리
- **Level 3: Defined** — 조직 표준화
- **Level 4: Quantitatively Managed** — 통계적 통제(SPC, Six Sigma)
- **Level 5: Optimizing** — 지속적 혁신

공식: **Process Capability = (목표 달성률 × 품질 지수) / 자원 투입량**
- 목표 달성률: 계획 대비 실제(%) = EV(분해완료가치) / PV(계획가치) × 100
- 품질 지수: 결함밀도(Defect/KLOC) 역수, MTBF(평균고장간격) / MTTR(평균수리시간)

- **📢 섹션 요약 비유**: 4대 프레임워크는 **의료 시스템**과 같습니다. COBIT은 **병원장**(전략), ITIL은 **진료 프로세스**(운영), PMBOK은 **수술 팀**(프로젝트), ISO는 **감염관리·JCI 인증**(보안/품질)입니다. 이 4자가 동시에 작동해야 환자가(기업이) 건강하게(지속가능하게) 유지됩니다.

---

## Ⅲ. 비교 및 연결

각 프레임워크의 적용 범위, 통제 강도, 적합 조직 규모는 명확히 다르다.

| 구분 | **COBIT 2019** | **ITIL 4** | **PMBOK 7** | **ISO 27001** |
| :--- | :--- | :--- | :--- | :--- |
| **적용 범위** | 거버넌스(전사) + 관리(전사) | IT 서비스 운영(중심) | 단일 프로젝트/프로그램 | 정보보안(전사) |
| **핵심 초점** | IT-비즈니스 정렬, 가치 제공, 리스크 최적화 | 서비스 가치 공동창조(Value Co-Creation) | 프로젝트 성공 기준(목표 달성) | CIA(기밀성·무결성·가용성) |
| **성숙도 모델** | PAM 7단계 (0~5) | Maturity Model 5단계 | Process Group 별 | 4 Tier(Policy-Process-Implementation-Measurement) |
| **인증 가능 여부** | ❌(자격증만: COBIT 2019 Foundation/Design/Implement) | ❌(자격증: ITIL Foundation/Master) | ❌(자격증: PMP, CAPM) | ✅(인증: ISMS 인증서 3년) |
| **적합 조직 규모** | 중견·대기업(500인+) | 전 규모(스타트업~대기업) | 프로젝트 단위 | 전 규모(규제 산업 필수) |
| **국내 도입률** | 23%(KISA 2022) | 41%(ITSM 도구 연계) | 65%(PMP 자격증 보유) | 89%(정보통신망법 의무) |
| **연계 표준** | ISO 38500, 27001 | ISO 20000, 27001 | PRINCE2, ISO 21500 | ISO 27017(클라우드), 27701(프라이버시) |

**기타 비교 프레임워크:**
- **vs Six Sigma/Lean**: 품질
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 776 / 800

<- **이전**: [775. IT 경영 관리 핵심 토픽 775번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/775_it_management_core_topic_775_exam_summary/)
**다음**: [777. IT 경영 관리 핵심 토픽 777번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/777_it_management_core_topic_777_exam_summary/) ->

---
