---
title: "763. IT 경영 관리 핵심 토픽 763번 시험 요약 (IT Management Core Topic 763 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(763번)는 **COBIT 2019, ITIL 4, ISO 38500** 프레임워크를 기반으로 IT 거버넌스·전략·포트폴리오·서비스·리스크를 통합 관리하여, **Value Creation(가치 창출)** 을 비즈니스 목표와 정렬(Alignment)시키는 경영 시스템의 총체
> 2. **가치**: 체계적 적용 시 IT 투자 ROI 평균 **15~25% 향상**, IT 인시던트 **40~60% 감소(MTTR 기준)**, 의사결정 속도 **2~3배 개선**, 컴플라이언스 위반 비용 **최소 70% 절감**(ISO 27001, GDPR, 개인정보보호법 기준)
> 3. **판단 포인트**: **Governance(거버넌스) vs Management(관리)** 의 역할 분리, **Build vs Run** 예산 배분(통상 30:70), **Centralized vs Federated** 거버넌스 모델, **Agile vs Plan-driven** 딜레마, 그리고 **Bimodal IT**(Mode 1 안정성 vs Mode 2 민첩성) 균형점이 핵심

---

## Ⅰ. 개요 및 필요성

현대 기업의 IT 부서는 더 이상 단순한 **Cost Center(비용 센터)** 가 아닌 **Value Center(가치 창출 센터)** 및 **Business Enabler(사업 가능화자)** 로서의 역할을 요구받고 있습니다. 4차 산업혁명(AI, IoT, 빅데이터, 클라우드)이 가속화되면서 IT와 비즈니스 간 경계는 사라졌고, CIO(Chief Information Officer)는 CTO·CDO·CISO와 함께 **CxO 협업 거버넌스** 체계 안에서 전략적 의사결정에 참여해야 합니다.

그러나 현실에서는 다음과 같은 고질적 문제가 반복됩니다:
- IT 투자 대비 성과 측정의 **불가능성(Black Box)**
- 부서별 **Silo(사일로) 시스템** 으로 인한 중복 투자
- 규제 대응(개인정보보호법, EU GDPR, 전자금융거래법)과 **컴플라이언스** 비용 급증
- 디지털 전환(DX) 요구 vs **레거시 시스템** 유지보수 비용
- 사이버 위협 증가에 따른 **IT 리스크 관리** 실패

이를 해결하기 위해 **763번 시험**은 IT 경영 관리 영역에서 거버넌스 프레임워크(COBIT 2019), 서비스 관리 표준(ITIL 4), ISO 국제표준(ISO 38500, ISO 27001), 프로젝트 관리(PMBOK 7th, PRINCE2), 애자일(SAFe, Scrum@Scale), 아키텍처 프레임워크(TOGAF, Zachman) 등을 통합적으로 다룹니다.

```text
+----------------------------------------------------------------------+
|            763번 IT 경영 관리 핵심 토픽 마인드맵                       |
+----------------------------------------------------------------------+
|                                                                      |
|                          +-----------------+                          |
|                          |  IT 거버넌스    | <- 최상위 의사결정 체계    |
|                          | (COBIT 2019)    |                          |
|                          +--------+--------+                          |
|                +------------------+------------------+                |
|                |                  |                  |                |
|        +-------v--------+  +------v------+  +-------v--------+        |
|        |  IT 전략/기획  |  |  IT 서비스  |  |  IT 리스크/    |        |
|        |  (전략수립)    |  |  관리(ITIL) |  |  컴플라이언스  |        |
|        +-------+--------+  +------+------+  +-------+--------+        |
|                |                  |                  |                |
|        +-------v--------+  +------v------+  +-------v--------+        |
|        |  EA / 포트폴리오|  |  ITSM 운영 |  |  정보보안/ISMS |        |
|        |  (TOGAF)        |  |  (인시던트) |  |  (ISO 27001)  |        |
|        +-------+--------+  +------+------+  +-------+--------+        |
|                |                  |                  |                |
|        +-------v------------------v------------------v--------+       |
|        |          프로젝트/프로그램 관리 (PMO 운영)            |       |
|        |  (PMBOK 7, PRINCE2, MSP, SAFe, Agile@Scale)        |       |
|        +------------------------------------------------------+       |
|                                                                      |
|  +------------------------------------------------------------+      |
|  |  지원 프레임워크: ISO 38500, ISO 27001, ISO 20000, CMMI    |      |
|  +------------------------------------------------------------+      |
+----------------------------------------------------------------------+
```

**기존 vs 새로운 패러다임 비교**

| 구분 | 기존(Traditional IT) | 신규(Digital Enterprise IT) |
|:-----|:---------------------|:-----------------------------|
| 역할 | Cost Center | Value Center / Business Partner |
| 예산 | 연간 고정(OpEx) | 분기 단위 Rolling Forecast |
| 구조 | 계층적(CIO -> IT 부서) | Matrix(CIO + CDO + CISO) |
| 방식 | Waterfall | Agile + DevOps + Bimodal |
| KPI | 가용성(Uptime) | TTM, NPS, ROI, Value |
| 시스템 | On-premise Monolith | Cloud-native Microservice |
| 거버넌스 | 통제 중심(Control) | 가치 중심(Value) |

- **📢 섹션 요약 비유**: IT 경영 관리는 **오케스트라 지휘자**와 같습니다. 첼리스트(IT 운영팀), 바이올리니스트(개발팀), 타악기 연주자(보안팀) 각자가 개별 실력만으로는 좋은 연주가 되지 않으며, **COBIT이라는 악보(Governance Framework)**를 따라 **ITIL이라는 호흡(Service Management)**을 맞추고, **PMBOK이라는 리듬(Project Management)**을 통해 하나의 **가치 있는 교향곡(Value Creation)**을 만들어내는 것이 핵심입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 **3-Layer Governance Model**로 구성됩니다: **Direction(방향) -> Management(관리) -> Operations(운영)**. COBIT 2019의 40개 관리 목표(Management Objective)와 5개 도메인(EDM, APO, BAI, DSS, MEA)으로 체계화됩니다.

```text
+----------------------------------------------------------------------+
|         COBIT 2019 Governance System 아키텍처 (5 Domains)           |
+----------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------+      |
|  |  EDM: Evaluate, Direct and Monitor (거버넌스 영역)         |      |
|  |  +- EDM01: 거버넌스 체계 설정 (Governance Framework)        |      |
|  |  +- EDM02: 이득 전달 보장 (Benefits Delivery)               |      |
|  |  +- EDM03: 리스크 최적화 (Risk Optimization)                |      |
|  |  +- EDM04: 자원 최적화 (Resource Optimization)              |      |
|  |  +- EDM05: 이해관계자 투명성 (Stakeholder Transparency)     |      |
|  +--------------------------+---------------------------------+      |
|                             |                                        |
|  +--------------------------v---------------------------------+      |
|  |  APO: Align, Plan and Organize (전략 정렬)                  |      |
|  |  +- APO01: IT 관리 프레임워크 (IT Management Framework)    |      |
|  |  +- APO02: 전략 (Strategy)                                  |      |
|  |  +- APO04: 혁신 (Innovation)                                |      |
|  |  +- APO05: 포트폴리오 (Portfolio)                            |      |
|  |  +- APO12: 리스크 관리 (Risk Management)                    |      |
|  |  +- APO13: 보안 관리 (Security Management)                  |      |
|  +--------------------------+---------------------------------+      |
|                             |                                        |
|  +--------------------------v---------------------------------+      |
|  |  BAI: Build, Acquire and Implement (구축)                   |      |
|  |  +- BAI01: 프로그램/프로젝트 관리 (Programs/Projects)      |      |
|  |  +- BAI02: 요구사항 정의 (Requirements)                     |      |
|  |  +- BAI03: 솔루션 설계 및 구현                              |      |
|  |  +- BAI11: 변경 관리 (Change Management)                    |      |
|  +--------------------------+---------------------------------+      |
|                             |                                        |
|  +--------------------------v---------------------------------+      |
|  |  DSS: Deliver, Service and Support (서비스 지원)            |      |
|  |  +- DSS01: 운영 관리 (Operations Management)                |      |
|  |  +- DSS02: 서비스 요청/인시던트 관리                        |      |
|  |  +- DSS03: 문제 관리 (Problem Management)                   |      |
|  |  +- DSS04: 연속성 관리 (Continuity Management)             |      |
|  |  +- DSS05: 보안 서비스 관리                                 |      |
|  +--------------------------+---------------------------------+      |
|                             |                                        |
|  +--------------------------v---------------------------------+      |
|  |  MEA: Monitor, Evaluate and Assess (모니터링/평가)         |      |
|  |  +- MEA01: 성과/동기부여 관리                               |      |
|  |  +- MEA02: 내부통제 시스템                                  |      |
|  |  +- MEA04: 외부 요건 준수 (Compliance)                      |      |
|  +------------------------------------------------------------+      |
|                                                                      |
|  ※ Cascading Goals: Stakeholder Needs -> Enterprise Goals ->        |
|    IT-related Goals -> Enabler Goals (4단계 연계)                     |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Governance Committee** | IT 거버넌스 최고 의사결정 기구 (이사회 산하) | 연 4회 정례 회의, 투자심의위원회(ISC), Risk Appetite 설정, KPI 검토 및 의사결정 |
| **PMO(Project Management Office)** | 프로젝트/프로그램/포트폴리오 통합 관리 | P3O(Portfolio, Programme, Project Office) 모델, EPMO(Enterprise) / DPMO(Domain) 계층 구조, 단계별 Gate Review |
| **ITSM 도구** | 서비스 데스크, 인시던트, 변경, 문제, 자산 통합 관리 | ServiceNow, BMC Remedy, Jira Service Management, Freshservice 등. CMDB(Configuration Management Database) 연동 |
| **EA(Enterprise Architecture)** | 비즈니스·데이터·애플리케이션·기술 4계층 아키텍처 통제 | TOGAF ADM(Architecture Development Method) 8단계(Phase A~H), Zachman 6×6 매트릭스, FEAF(联邦EA Framework) |
| **정보보안관리체계(ISMS)** | 정보자산 기밀성·무결성·가용성 통제 | ISO 27001:2022(Annex A 93개 통제항목), NIST CSF(Identify-Protect-Detect-Respond-Recover 5단계), Zero Trust Architecture |
| **BSC & KPI 대시보드** | IT 성과 측정 및 균형점수표 | Balanced Scorecard 4관점(Financial, Customer, Internal Process, Learning & Growth), OKR(Objectives & Key Results) 연계 |
| **Risk Register** | IT 리스크 식별·평가·대응·모니터링 | ISO 31000 Risk Management Process, Risk = Likelihood × Impact 매트릭스, KRI(Key Risk Indicator) 추적 |

**핵심 원리 — IT Value Chain 및 Cascading Goals**

COBIT 2019의 가장 중요한 메커니즘은 **Cascading Goals(연계 목표)** 입니다. 이 메커니즘은 **Stakeholder Needs -> Enterprise Goals -> IT-related Goals -> Enabler Goals**의 4단계를 거치며, 각 단계에서 "Why -> What -> How"의 논리적 연결을 제공합니다.

```
Step 1. Stakeholder Needs (Why) — 가치/이해관계자 요구
   |      예: "시장 출시 시간 단축", "규제 준수", "비용 절감"
   v
Step 2. Enterprise Goals (What) — 13개 기업 목표
   |      예: EG01 포트폴리오 경쟁력, EG08 내부 운영 효율
   v
Step 3. IT-related Goals (What for IT) — 13개 IT 연계 목표
   |      예: ITG04 관리된 비즈니스 혁신, ITG09 IT 비용 최적화
   v
Step 4. Enabler Goals (How) — 7개 Enabler별 목표
          (People, Process, Technology, Information, Service,
           Organization Structure, Principles/Policy)
```

**RACI Matrix (Responsibility Assignment)**

| 역할 | 책임 | 설명 |
|:-----|:-----|:-----|
| **R**esponsible | 실행 | 실제 활동 수행 |
| **A**ccountable | 최종 책임 | 의사결정 및 승인 (1명) |
| **C**onsulted | 자문 | 양방향 의견 교환 |
| **I**nformed | 통보 | 일방향 보고 |

**거버넌스 vs 매니지먼트 구분 (핵심)**
- **Governance**: 이사회·경영진의 **의사결정·감독·평가**(Evaluate, Direct, Monitor)
- **Management**: 실무진의 **계획·실행·운영·모니터링**(Plan, Build, Run, Monitor)
- 두 기능의 **분리(Segregation of Duties)** 가 ISO 38500 및 SOX 컴플라이언스의 핵심 통제 요건

- **📢 섹션 요약 비유**: COBIT의 **Cascading Goals**는 **번개(Lightning)가 땅에 도달하는 과정**과 같습니다. 구름(Stakeholder Needs)에서 시작된 번개가 단계적으로 좁아지며 최종적으로 **땅(Enabler Goals)에 닿아** 구체적 행동을 만들어내며, 5개 도메인(EDM, APO, BAI, DSS, MEA)은 **대기권->지면까지의 5개 층**이라 할 수 있습니다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 영역에서 혼동하기 쉬운 핵심 프레임워크들을 명확히 비교합니다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **TOGAF 9.2/10** | **PMBOK 7th** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 | IT 서비스 관리 | IT 거버넌스 국제표준 | EA 개발 방법론 | 프로젝트 관리 |
| **대상** | CIO/이사회 | 서비스 운영자 | 이사진/이사 | 아키텍트 | PM/PMO |
| **범위** | 엔드투엔드(End-to-End) | 서비스 라이프사이클 | 거버넌스 6원칙 | 아키텍처 4계층 | 프로젝트 12원리 |
| **핵심 개념** | 40개 관리목표, 7 Enabler | 34 Practices, SVS | 6 원칙, 3-Tier Model | ADM 8 Phase | 8 Performance Domain |
| **접근법** | 원칙·정책 기반 | Practice 기반 | 원칙 기반 | 반복 점진(Iteration) | 가치 중심(Value) |
| **연계 관계** | 상위 거버넌스 체계 | 서비스 운영 실행 | 거버넌스 윤리/책임 | 아키텍처 산출물 | 프로젝트 수행 방법 |
| **인증** | COBIT 2019 Foundation/Design/Implement | ITIL Foundation/MP/SL | ISO 38500 Lead IT Governance | TOGAF 9 Certified | PMP, CAPM |
| **생성 기관** | ISACA | AXELOS(PeopleCert) | ISO | The Open Group | PMI |
| **업데이트** | 2018년 12월 | 2019년 2월 | 2015년 (현재 유효) | 2022년 10월 (10판) | 2021년 8월 |
| **약점** | 실행 도구 부족 | 거버넌스 약함 | 추상적 원칙 | 거버넌스/PM 미흡 | 거버넌스 약함 |

**ITIL 4 Service Value System
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 763 / 800

<- **이전**: [762. IT 경영 관리 핵심 토픽 762번 시험 요약](/studynote/12_it_management/05_security_compliance/762_it_management_core_topic_762_exam_summary/)
**다음**: [764. IT 경영 관리 핵심 토픽 764번 시험 요약](/studynote/12_it_management/05_security_compliance/764_it_management_core_topic_764_exam_summary/) ->

---
