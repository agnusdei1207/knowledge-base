---
title: "560. IT 경영 관리 핵심 토픽 560번 시험 요약 (IT Management Core Topic 560 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, ISO 38500을 축으로 하는 **거버넌스-관리-운영 3계층(Govern-Build-Run)** 프레임워크를 통해, 비즈니스 가치(Value Realization)와 IT 리스크(Goal Cascade) 간의 균형을 체계적으로 추적·통제하는 경영 체계이다.
> 2. **가치**: McKinsey(2023) 기준 전사적 IT 거버넌스 도입 기업의 **Time-to-Market 28% 단축**, **IT 운영비 대비 비즈니스 가치 비율 3.2배 향상**, **프로젝트 실패율 47% -> 19% 감소** 효과를 통해, "IT 비용 센터"에서 "전략적 가치 동인(Value Driver)"으로의 전환을 가능케 한다.
> 3. **판단 포인트**: 중앙집중(CoE) vs 분산(Federated) 거버넌스 모델, **Bimodal IT** (Mode 1 안정성 vs Mode 2 민첩성) 간 자원 배분, 그리고 **RACI 매트릭스**를 통한 의사결정 권한 분배가 핵심 trade-off이며, **CSF(공통 성공 요인)**와 **KGI/KPI** 체인이 IT-비즈니스 정렬(Strategic Alignment)을 좌우한다.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명(AI, IoT, Cloud, BigData) 환경에서 IT는 더 이상 보조 기능이 아닌 **핵심 사업 운영 기반**이다. 그러나 Gartner(2024) 조사에 따르면 CIO의 **73%**가 "디지털 트랜스포메이션 과제"를, **64%**가 "IT-비즈니스 정렬 부재"를, **58%**가 "예산 통제 실패"를 최대 고충으로 보고한다. 이는 기술 도입의 개별 최적화(local optimization) 문제라기보다, **전사적 IT 의사결정 체계 부재**에서 기인한다.

기술사 시험 관점에서 IT 경영 관리는 단순한 IT 운영이 아닌, **이해관계자(Stakeholder)들의 이해(Interest)를 조정하고, IT 자원을 최적 배분하며, 위험을 통제하고, 가치를 측정하는 경영 메커니즘**을 다룬다. 즉, ISACA·AXELOS·ISO가 제시한 글로벌 표준들을 어떻게 한국 조직 환경(공공·금융·제조)에 맞게 적용·통합할 것인가가 평가 핵심이다.

```text
+--------------------------------------------------------------------------+
|                    IT 경영 관리 3계층 통합 프레임워크                       |
+--------------------------------------------------------------------------+
|                                                                          |
|   +-----------------------------------------------------------------+    |
|   |  Layer 1: GOVERNANCE (거버넌스) — "무엇을(What) 할 것인가"      |    |
|   |  +------------+ +------------+ +------------+ +-------------+  |    |
|   |  | COBIT 2019 | | ISO 38500  | | ISO 27001  | | ISO 20000   |  |    |
|   |  | (IT 거버)  | | (IT 거버)  | | (정보보안) | | (서비스)    |  |    |
|   |  +-----+------+ +-----+------+ +-----+------+ +-----+-------+  |    |
|   |        +------+-------+------+--------+------+-------+          |    |
|   +---------------+--------------+---------------+------------------+    |
|                   |              |               |                       |
|   +---------------v--------------v---------------v------------------+    |
|   |  Layer 2: MANAGEMENT (관리) — "어떻게(How) 할 것인가"          |    |
|   |  +------------+ +------------+ +------------+ +-------------+  |    |
|   |  | 전략기획   | | 포트폴리오 | | 프로젝트   | | 위험/보안   |  |    |
|   |  | (ISP/BSP)  | | 관리(PPM)  | | 관리(PMO)  | | 관리(RM)    |  |    |
|   |  +------------+ +------------+ +------------+ +-------------+  |    |
|   +-----------------------------------------------------------------+    |
|                                                                          |
|   +-----------------------------------------------------------------+    |
|   |  Layer 3: OPERATIONS (운영) — "누가(Who) 언제(When) 할 것인가"  |    |
|   |  +------------+ +------------+ +------------+ +-------------+  |    |
|   |  | ITIL 4     | | DevOps     | | SRE        | | FinOps      |  |    |
|   |  | (서비스)   | | (배포)     | | (안정성)   | | (클라우드)  |  |    |
|   |  +------------+ +------------+ +------------+ +-------------+  |    |
|   +-----------------------------------------------------------------+    |
|                                                                          |
|   -> 입력: 비즈니스 요구(Need) / 위험 appetite / 자원 제약               |
|   -> 출력: 가치(Value) / 효율(Efficiency) / 적합성(Conformance)          |
|   -> 피드백: CSF 측정 -> KPI 분석 -> 전략 재조정 (Plan-Do-Check-Act)        |
+--------------------------------------------------------------------------+
```

**왜 필요한가? (Old vs New Paradigm 비교)**

| 구분 | Old Paradigm (1990s) | New Paradigm (2024~) |
|:---|:---|:---|
| 관점 | IT는 비용(Cost Center) | IT는 가치 동인(Value Driver) |
| 구조 | 실리콘 계층(Silo)별 독립 운영 | 전사적 거버넌스 + EA 통합 |
| 결정 | CIO 독단적 의사결정 | RACI 기반 다자 합의(CoP) |
| 측정 | Uptime 단순 지표 | NPV, ROI, BSC 4관점 종합 |
| 변화 | Big-bang 5년 주기 | Agile + Bimodal + Continuous |
| 위험 | 사고 후 대응(Reactive) | 위험 appetite 사전 정의(Proactive) |

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **도시의 종합 도시계획(Urban Planning)**과 같다. 개별 건물(시스템)만 잘 지어도 교통·상하수도·치안(거버넌스)이 엉망이면 도시는 무너진다. 그래서 토지이용계획(EA), 예산(투자), 안전기준(보안) 등을 **하나의 마스터플랜**으로 통합 관리해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 작동 메커니즘은 **"목표 계단(Goals Cascade)"**이다. 즉, **Stakeholder Needs -> Enterprise Goals -> Alignment Goals -> IT Goals -> Enabler Goals**로 변환하는 가치 흐름(Value Chain)을 따른다. COBIT 2019는 이를 **40개 거버넌스/관리 목표(Governance & Management Objectives)**로 구체화하고, **7가지 구성요소(Components: Principles, Policies, Frameworks; Processes; Organizational Structures; People, Skills, Competencies; Culture, Ethics, Behavior; Services, Infrastructure, Applications; Information)**로 실행 가능하도록 설계했다.

```text
+------------------------------------------------------------------------+
|              COBIT 2019 Goals Cascade & Value Flow                      |
+------------------------------------------------------------------------+
|                                                                        |
|  [Stakeholder]    [Enterprise]      [Alignment]      [IT Goals]        |
|  Needs              Goals             Goals           (13 EA)           |
|  +-----+         +-------+         +-------+         +-------+          |
|  |수익 |----+---->|EG01   |----+---->|AG09   |----+---->|ITG11 |          |
|  |성장 |    |    |금융   |    |    |비즈니스|    |   |IT자원|          |
|  |위험 |    |    |가치   |    |    |IT정렬 |    |   |관리  |          |
|  |정보 |    |    +-------+    |    +-------+    |   +-------+          |
|  |     |    |    |EG02   |    |    |AG11   |    |   |ITG01 |          |
|  |     |    +---->|고객   |----+    |거버넌 |----+   |IT준법|          |
|  |     |         |만족   |         |체계   |         |     |          |
|  +-----+         +-------+         +-------+         +-------+          |
|       |                |                 |                 |            |
|       v                v                 v                 v            |
|  +-----------------------------------------------------------------+    |
|  |  Enablers (7 Components) 적용 — "어떻게 달성할 것인가"           |    |
|  |  ① Principles/Policies  ② Processes(40 EDM/MEA/BAI/DSS)        |    |
|  |  ③ Structures  ④ People/Skills  ⑤ Culture                       |    |
|  |  ⑥ Services/Infra/Apps  ⑦ Information(KGI/KPI/KRI)              |    |
|  +-----------------------------------------------------------------+    |
|       |                                                                |
|       v                                                                |
|  +-----------------------------------------------------------------+    |
|  |  -> Benefit Realization(가치 실현)                              |    |
|  |  -> Risk Optimization(위험 최적화)                              |    |
|  |  -> Resource Optimization(자원 최적화)                          |    |
|  |  ⇒ 3가지 Value-Goal Balance로 Stakeholder 만족                  |    |
|  +-----------------------------------------------------------------+    |
+------------------------------------------------------------------------+
```

**핵심 메커니즘 단계별 설명:**

1. **CSF(공통 성공 요인, Critical Success Factors) 도출**: TOWS Matrix, Porter's Five Forces, SWOT 분석으로 외부·내부 환경 분석 -> Top-Down 접근
2. **KGI(핵무 결과 지표, Key Goal Indicators) 설정**: Enterprise 관점의 "최종 결과". 예: "고객 이탈률 15% -> 8%"
3. **KPI(핵심성과 지표, Key Performance Indicators) 정의**: KGI 달성에 필요한 중간 측정. 예: "콜센터 평균 응답시간 240초 -> 90초"
4. **KRI(핵심 위험 지표, Key Risk Indicators) 모니터링**: 위험의 선제 탐지. 예: "일일 보안 이벤트 발생 건수 > 100건"
5. **RACI 매트릭스 적용**: 의사결정 권한 명확화 (Responsible, Accountable, Consulted, Informed)
6. **PDCA 사이클**: Plan(거버넌스 설계) -> Do(운영 실행) -> Check(성과 측정) -> Act(개선)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **거버넌스 체계(Governance System)** | 의사결정 구조, 책임·권한 배분 | COBIT 2019 EDM(평가·지시·모니터) 5개 프로세스, 이사회-경영진-IT 3자 역할 분리, RACI 매트릭스로 권한 명세 |
| **전략 정렬(Strategic Alignment)** | 비즈니스-IT 목표 일치 | SAMM(Strategic Alignment Maturity Model) 5단계(L1: 초기~L5: 최적화), 핀란드 Kujala 모델, BSP(Business Strategic Planning) -> ISP(Information Strategic Planning) |
| **포트폴리오 관리(PPM)** | IT 투자 우선순위 결정 | BCG Matrix(별/현금/유망/사양), risk-adjusted NPV, Real Options Valuation, Gartner Magic Quadrant 활용 |
| **서비스 관리(Service Mgmt)** | SLA 기반 IT 서비스 제공 | ITIL 4 SVS(Service Value System): Service Value Chain 6활동(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve), 34개 Practice |
| **위험 관리(Risk Management)** | 정성·정량 위험 통제 | ISO 31000 Risk = f(Threat, Vulnerability, Asset Value), ALE = SLE × ARO, FAIR 모델, 위험 appetite/tolerance 한계선 |
| **성과 측정(Performance Mgmt)** | BSC 4관점 정량 측정 | Kaplan-Norton BSC: Financial/Customer/Internal Process/Learning&Growth, IT-BSC(Bititri & Atan), 가중치+목표+임계값 3요소 |
| **보안 거버넌스(Security GRC)** | 정보보안 정책·통제 | ISO 27001/27002(Annex A 93 통제항목), NIST CSF 5기능(Identify-Protect-Detect-Respond-Recover), 3 Lines of Defense 모델 |
| **아키텍처(EA)** | 전사 IT 자산 통합·표준화 | TOGAF ADM 8단계(Phase A: Architecture Vision ~ Phase H: Architecture Change Management), Zachman 6x6, FEAF, DoDAF |

**핵심 파라미터 및 수식:**

- **TCO(Total Cost of Ownership)** = 직접비(HW/SW 구매) + 간접비(운영·인력·교육·폐기)
- **ROI(투자대비성과)** = (Net Benefit / Total Cost) × 100%. 일반적 합격선: 15% 이상
- **NPV(순현재가치)** = Σ[CFt / (1+r)^t] - 초기투자. r=할인율(보통 WACC 8~12%)
- **Payback Period** = 초기투자 / 연 현금흐름. 3년 이내 회수가 일반적 기준
- **ALE(연간 손실 기댓값)** = SLE(단일 손실) × ARO(연간 발생 횟수)
- **Maturity Level(성숙도)** = (현 수준 점수 / 최대 수준 점수) × 5 -> 0~5 Scale (CMMI, COBIT PAM)

- **📢 섹션 요약 비유**: IT 경영 관리는 **비행기의 자동조종 시스템
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 560 / 800

<- **이전**: [559. IT 경영 관리 핵심 토픽 559번 시험 요약](/studynote/12_it_management/05_security_compliance/559_it_management_core_topic_559_exam_summary/)
**다음**: [561. IT 경영 관리 핵심 토픽 561번 시험 요약](/studynote/12_it_management/05_security_compliance/561_it_management_core_topic_561_exam_summary/) ->

---
