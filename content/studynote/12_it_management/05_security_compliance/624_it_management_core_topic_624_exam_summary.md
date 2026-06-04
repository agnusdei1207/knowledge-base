---
title: "624. IT 경영 관리 핵심 토픽 624번 시험 요약 (IT Management Core Topic 624 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019 거버넌스 체계(EDM: Evaluate-Direct-Monitor)**를 중심으로 **IT 전략-포트폴리오-프로젝트-서비스-운영-리스크**를 통합 관리하는 체계로, 거버넌스(목표설정/지휘)와 관리(계획/구축/운영/모니터링)를 분리하여 의사결정 구조를 확립하는 것이 핵심이다.
> 2. **가치**: 정렬된 IT 투자로 **TCO 20~30% 절감**, 프로젝트 성공률 **전통적 30% -> 거버넌스 적용 시 70% 이상** 도달, 그리고 **ISO 27001/ISMS-P 인증, 컴플라이언스 자동화, KPI 기반 의사결정**으로 정량적 가치 실현.
> 3. **판단 포인트**: **IT-비즈니스 정렬도(Strategic Alignment Maturity)**, 거버넌스 모델 중앙집중형(Centralized) vs 분산형(Decentralized/Federated) 선택, **KPI 분해 구조(CSF->KPI->KGI)** 설계, 그리고 **Agile-Waterfall 하이브리드** 운영 방식 결정이 핵심 Trade-off.

---

## Ⅰ. 개요 및 필요성

정보기술의 단순 비용센터화에서 벗어나, IT가 **전략적 비즈니스 가치**를 창출하는 핵심 동력으로 부상하면서, IT를 어떻게 **투자, 운영, 통제, 측정**할 것인가에 대한 체계적 관리 프레임워크가 요구된다. 과거 2000년대 초반 IT 거버넌스 부재로 인한 대규모 프로젝트 실패(Standish Group 기준 프로젝트 성공률 29%, 1994년)를 계기로, COSO(재무), COBIT(IT), ISO 27001(보안) 등 3대 통합 거버넌스 체계를 기반으로 하는 IT 경영 관리 표준이 정착되었다.

```text
+-----------------------------------------------------------------------------+
|            IT 경영 관리 통합 프레임워크 (Enterprise IT Governance)          |
+-----------------------------------------------------------------------------+
|                                                                             |
|  [최상위 거버넌스]  Board of Directors / IT Steering Committee              |
|          |          (이사회/IT전략위원회: 의사결정, 감독)                     |
|          v                                                                |
|  +-------------------------------------------------------------------+    |
|  |  EDM 단계 (Evaluate-Direct-Monitor) - COBIT 2019 Governance Obj. |    |
|  |  - EDM01 거버넌스 체계 설정 (Governance System Setting)            |    |
|  |  - EDM02 가치 전달 (Benefits Delivery)                            |    |
|  |  - EDM03 리스크 최적화 (Risk Optimization)                        |    |
|  |  - EDM04 자원 최적화 (Resource Optimization)                      |    |
|  |  - EDM05 이해관계자 투명성 (Stakeholder Transparency)             |    |
|  +-------------------------------------------------------------------+    |
|          |                                                                |
|          v                                                                |
|  +-------------------------------------------------------------------+    |
|  |  PBRM 단계 (Plan-Build-Run-Manage) - 40개 관리 목표                |    |
|  |  +----------+  +----------+  +----------+  +----------+          |    |
|  |  | Plan     |  | Build    |  | Run      |  | Monitor  |          |    |
|  |  | 전략/포트 |-> | 설계/구축|-> | 운영/지원|-> | 평가/감사|          |    |
|  |  | 폴리오   |  | 변경관리 |  | 서비스   |  | KPI측정  |          |    |
|  |  +----------+  +----------+  +----------+  +----------+          |    |
|  +-------------------------------------------------------------------+    |
|          |                                                                |
|          v                                                                |
|  [7대 구성요소 (Components) - CSF 7개 영역]                                  |
|   ① 프로세스(Process) ② 조직구조(Structures) ③ 정보흐름(Flows)              |
|   ④ 인력/역량(People) ⑤ 정책원칙(Principles) ⑥ 문화윤리(Culture)           |
|   ⑦ 서비스인프라(Services/Infrastructure/Applications)                     |
|                                                                             |
|  [연결 프레임워크]                                                          |
|   +--------+  +--------+  +--------+  +--------+  +--------+            |
|   | ITIL4  |  |ISO27001|  | TOGAF  |  | PMBOK  |  |BABOK   |            |
|   |서비스  |  |정보보안|  |EA아키텍|  |프로젝트|  |BA업무  |            |
|   |관리    |  |거버넌스|  |처      |  |관리    |  |분석    |            |
|   +--------+  +--------+  +--------+  +--------+  +--------+            |
+-----------------------------------------------------------------------------+
```

**시대의 변화**:

| 시대 | 1990년대 이전 | 2000년대 | 2010년대 이후 | 2020년대 |
|---|---|---|---|---|
| IT 역할 | 비용센터/백오피스 | 비즈니스 지원/효율화 | 전략 동력/차별화 | 비즈니스 자체의 일부 |
| 관리 방식 | 개별 시스템 단위 | PMO/프로젝트 단위 | IT 거버넌스/서비스 단위 | 플랫폼/생태계 단위 |
| 위험 | 시스템 장애 | 프로젝트 실패 | 사이버보안/규제 | 디지털 신뢰/ESG |
| 핵심 프레임워크 | 없음(자체 기준) | COBIT 4/5, ITIL v2/v3 | COBIT 2019, ITIL 4 | COBIT 2019+ESG, AI 거버넌스 |

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **도시의 도시계획**과 같습니다. 개별 건물(시스템)이 잘 지어져도 교통, 상하수도, 안전, 환경(거버넌스) 등 도시 전체 인프라가 설계되어야 시민(비즈니스)이 살기 좋은 도시가 됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019는 **거버넌스 시스템**과 **목표 계층(Goals Cascade)**이라는 두 가지 핵심 메커니즘으로 작동한다. 목표 계층은 **Stakeholder Needs -> Enterprise Goals -> Alignment Goals -> Management Objectives -> Component -> Process Activity**로 분해되어, 최상위 이해관계자 니즈(예: "IT 비용 절감", "리스크 관리")가 하위 측정 가능한 KPI로 자동 변환되는 **Balanced Scorecard 4관점(재무, 고객, 내부프로세스, 학습성장)** 구조를 따른다.

```text
+--------------------------------------------------------------------------+
|              COBIT 2019 목표 계층 (Goals Cascade) 구조                   |
+--------------------------------------------------------------------------+
|                                                                          |
|  [Layer 1] Stakeholder Needs (이해관계자 니즈)                            |
|     +- 투자자: ROI, 성장성                                                |
|     +- 고객: 서비스 품질, 보안                                            |
|     +- 임직원: 생산성 도구                                                |
|     +- 규제자: 컴플라이언스                                               |
|                |                                                          |
|                v  (매핑)                                                  |
|  [Layer 2] Enterprise Goals (13개)                                        |
|     EG01 포트폴리오의 경쟁 제품/서비스                                     |
|     EG06 비즈니스 서비스 가용성 및 기능성                                  |
|     EG09 정보 기반 의사결정                                               |
|     EG12 디지털 트랜스포메이션 프로그램 관리                               |
|                |                                                          |
|                v  (매핑)                                                  |
|  [Layer 3] Alignment Goals (13개 IT 관련 목표)                            |
|     AG01 IT 준수 및 지원                                                   |
|     AG04 품질 기술정보                                                    |
|     AG06 IT 비용/편익 투명성                                              |
|     AG14 비즈니스 정보의 가용성                                            |
|                |                                                          |
|                v  (매핑)                                                  |
|  [Layer 4] Management Objectives (40개 + EDM 5개)                         |
|     EDM02(거버넌스), BAI01(프로그램관리), DSS02(서비스요청/사고)           |
|                |                                                          |
|                v  (측정)                                                  |
|  [Layer 5] Process Activities -> Component (7대 구성요소)                   |
|     활동 -> 프로세스 메트릭(KPI) -> 구성요소별 평가                          |
|                                                                          |
|  -----------------------------------------------------------------       |
|  [게인-스케줄 모델 적용: 조직별 규모·중요도에 따라 11~52주 진단·구축]      |
+--------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **거버넌스 시스템(Governance System)** | 의사결정 권한/책임 구조 | EDM 5개 목표(Evaluate/Direct/Monitor), 이사회-경영진-CIO 3계층 라페포트 모델(RACI), **R(Responsible)/A(Accountable)/C(Consulted)/I(Informed)** 매트릭스 |
| **목표 계층(Goals Cascade)** | 전략->전술->운영 정렬 | 13 Enterprise Goals × 13 Alignment Goals, **Primary(매우높음)/Secondary(중간)/None(무관)** 매핑 방식, Balanced Scorecard 4관점 통합 |
| **7대 구성요소(Components)** | 거버넌스 구현 토대 | Process(40개), Structures(조직도), Information Flows, People/Skills, Principles/Policies, Culture/Ethics, Services/Infrastructure |
| **설계요인 11개(Design Factors)** | 조직 맞춤 거버넌스 조정 | Enterprise Strategy(4종: Growth/Acquisition/Innovation/Cost), Risk Profile, I&T Issues, Threat Landscape, Compliance Requirements, IT Role(4종), Sourcing(Insource/Outsource/Cloud/Hybrid), IT Implementation Methods(Agile/DevOps/Traditional), Technology Adoption(First Mover/Follower/Slow Adopter), 조직규모(Startup/Small/Large/Enterprise), **중요한 의사결정의 11개 Factor 가중치 합산**으로 시스템 스코어 산정 |
| **KPI/KGI 측정 체계** | 성과/목표 측정 | KGI(Key Goal Indicator): 결과지표 / KPI(Key Performance Indicator): 수행지표 / CSF(Critical Success Factor): 성공 핵심요인 / **SMART 원칙**(Specific/Measurable/Attainable/Relevant/Time-bound) |
| **거버넌스 운영 모드** | 의사결정 분권화 수준 | **Centralized**(표준화^, 일관성^), **Decentralized**(민첩성^), **Federated**(하이브리드, COBIT 기본 권장), **Networked**(생태계/파트너 연동) |

**핵심 파라미터 및 공식**:

```
[거버넌스 성숙도 측정 모델 - COBIT PAM(Process Assessment Model)]
  Maturity Level (0~5):
    Level 0: Incomplete (프로세스 미인식)
    Level 1: Initial/Ad hoc (성공 우연 의존)
    Level 2: Managed (의도적 계획/추적)
    Level 3: Defined (조직 표준화)
    Level 4: Quantitatively Managed (정량 측정/통제)
    Level 5: Optimizing (지속적 개선)

[목표 매핑 가중치 공식 - 예시 AG06(IT 비용/편익 투명성) 매핑]
  Primary Relationship   = 가중치 1.0 (강한 인과관계)
  Secondary Relationship = 가중치 0.5 (간접 영향)
  None                   = 가중치 0.0

  -> AG06이 Primary인 EG: EG01(경쟁제품), EG06(서비스가용성), EG08(내부운영)
  -> AG06이 Secondary인 EG: EG04(품질재무정보), EG10(임직원역량), EG12(디지털전환)

[IT 정렬도(Strategic Alignment) 측정 - Henderson & Venkatraman 모델]
  Strategic Fit (SF) = f(Business Strategy × IT Strategy)
  Functional Integration (FI) = Business ↔ IT 프로세스 통합
  -> Strategic Alignment Maturity: 4-Level (Initial/Initiated/Established/Optimized)
```

- **📢 섹션 요약 비유**: 목표 계층(Goals Cascade)은 **에베레스트 산 정상(비즈니스 목표)에서 발코니(프로세스 KPI)까지의 등반 지도**와 같습니다. 산 정상에서 1미터씩 단계를 표시하지 않으면 등반객(프로젝트/시스템)이 어디까지 왔는지 알 수 없습니다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리는 단일 표준이 아니라 **다중 프레임워크 융합 영역**이다. 각각의 프레임워크는 **고유 영역(Gap)**이 있으며, 실무에서는 상호 보완적으로 통합 적용된다.

| 구분 | **COBIT 2019** (IT 거버넌스) | **ITIL 4** (IT 서비스 관리) | **ISO 27001/27002** (정보보안) | **PMBOK 7** (프로젝트 관리) | **TOGAF 10** (EA 아키텍처) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **핵심 초점** | IT 거버넌스/관리 체계 | IT 서비스 운영/전달 | 정보보안 관리 시스템 | 프로젝트 일시적 가치 창출 | 기업 아키텍처 정렬 |
| **구조** | EDM + 40 프로세스, 7 컴포넌트 | 34 Practices, SVS(Service Value System) | 93 Control (Annex A) | 12 Principle, 8 Performance Domain | ADM(Architecture Development Method) 8단계 |
| **적용 범위** | 전사 IT 의사결정/통제 | IT 운영/서비스 데스크 | 정보보호 정책/통제 | 개별 프로젝트 라이프사이클 | 전사 아키텍처/표준 |
| **측정 관점** | 거버넌스 성숙도, 목표 달성도 | 서비스 가치(Value), 사용자 경험 | 위험 처리율(Risk Treatment), 통제 효과성 | 프로젝트 성공률, EV(Earned Value) | EA 적합도, 표준 준수율 |
| **주 사용자** | 이사회, CIO, 내부감사 | IT 운영팀, 서비스 매니저 | CISO, 보안팀, 컴플라이언스 | PMO, 프로젝트 매니저 | EA 아키텍트, CIO |
| **
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 624 / 800

<- **이전**: [623. IT 경영 관리 핵심 토픽 623번 시험 요약](/studynote/12_it_management/05_security_compliance/623_it_management_core_topic_623_exam_summary/)
**다음**: [625. IT 경영 관리 핵심 토픽 625번 시험 요약](/studynote/12_it_management/05_security_compliance/625_it_management_core_topic_625_exam_summary/) ->

---
