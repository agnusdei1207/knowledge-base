---
title: "572. IT 경영 관리 핵심 토픽 572번 시험 요약 (IT Management Core Topic 572 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 토픽 572번은 **IT 거버넌스(COBIT 2019) ↔ IT 서비스 관리(ITIL 4) ↔ 디지털 전환 전략**의 3축을 ISO 38500/EITA/엔터프라이즈 아키텍처로 통합하는 프레임워크로, **Value Creation(가치 창출)**을 위한 의사결정-실행-측정-개선의 폐루프(Closed-loop) 거버넌스 체계 구축이 핵심이다.
> 2. **가치**: 정량적으로는 IT 투자 대비 ROI(Return on IT, RIT) 15~25% 개선, 디지털 전환 성공률(McKinsey 기준 35% -> 체계적 거버넌스 적용 시 70% 이상) 향상, 정성적으로는 이사회-임원-현업 간 IT 정렬(IT-Business Alignment) 수준을 L2(의사결정 정렬)에서 L5(동적 역량 정렬)로 격상시킬 수 있다.
> 3. **판단 포인트**: **① 거버넌스 모델 선택**(Centralized vs Federated vs Hybrid CoE), **② 프레임워크 통합 수준**(단일 vs 매핑 통합), **③ 측정 지표**(Lagging KPI vs Leading KRI), **④ Change Adoption Curve**(ADKAR/Kotter 8단계) 적용 여부가 실무 적용의 핵심 Trade-off 이다.

---

## Ⅰ. 개요 및 필요성

한국의 정보관리기술사 및 IT 컨설팅 현업에서 **토픽 572번**은 "IT 경영 관리"의 핵심 통합 영역으로, **IT 거버넌스·서비스 운영·디지털 혁신·IT 성과관리**를 아우르는 메타 프레임워크 영역을 다룬다. 이는 단순한 이론 정리가 아닌, **COSO ERM 2017**, **COBIT 2019**, **ITIL 4**, **ISO/IEC 38500**, **TOGAF 10**, **Zachman Framework**, **K-ICT BS(국가 ICT 표준 프레임워크)**를 실무적으로 통합 적용하는 능력을 측정하는 영역이다.

과거(2010년대 이전)의 IT 관리는 **프로젝트 단위 투자 -> 완료 후 사후 관리**의 선형(Linear) 모델이 주류였으나, **클라우드 전환, 생성형 AI, 규제 강화(개인정보보호법, EU AI Act, ESG 공시)**로 인해 **"Always-On, AI-Augmented, Continuously Compliant"** IT 운영 모델이 요구된다. 또한 McKinsey(2023) 보고에 따르면 디지털 전환 프로젝트의 **65%가 ROI 미달** 상태이며, Gartner(2024)에서는 **75%의 CEO가 AI 거버넌스 부재를 핵심 리스크**로 지목했다. 이러한 환경에서 **토픽 572번**은 "기술 도입"이 아닌 **"기술을 통한 가치 실현"**을 보장하는 경영 관리 체계의 설계·운영·평가를 다룬다.

```text
+--------------------------------------------------------------------------+
|           IT 경영 관리 핵심 토픽 572번 — 통합 거버넌스 체계 (EITA)        |
|                                                                          |
|   +----------------+    +----------------+    +------------------+      |
|   | Board / 이사회 |◄--►|  CEO / CIO     |◄--►|  Business Units  |      |
|   | (감사/리스크)  |    | (전략 포트폴리오)|    | (현업 수요/우선순위)|   |
|   +--------+-------+    +--------+-------+    +--------+---------+      |
|            |                     |                     |                |
|            v                     v                     v                |
|   +-------------------------------------------------------------+        |
|   |  ① Governance Layer (ISO 38500 / COBIT 2019 EDM)            |        |
|   |     - Evaluate(평가)·Direct(지시)·Monitor(모니터링)          |        |
|   |     - 목표: 책임성·전략·수탁·능력·성공·규정 준수              |        |
|   +----------------------------+--------------------------------+        |
|                                |                                         |
|                                v                                         |
|   +-------------------------------------------------------------+        |
|   |  ② Management Layer (ITIL 4 / COBIT 2019 BAI/MEA)           |        |
|   |     - SVS(Service Value System)·Value Chain·34 Practices     |        |
|   |     - 전략->포트폴리오->아키텍처->전환->운영->지속적개선             |        |
|   +----------------------------+--------------------------------+        |
|                                |                                         |
|                                v                                         |
|   +-------------------------------------------------------------+        |
|   |  ③ Execution Layer (기술/플랫폼: 클라우드·AI·데이터·보안)    |        |
|   |     - Multi/Hybrid Cloud · AIOps · Zero Trust · Data Mesh   |        |
|   +----------------------------+--------------------------------+        |
|                                |                                         |
|                                v                                         |
|   +-------------------------------------------------------------+        |
|   |  ④ Assurance Layer (감리·인증·측정)                          |        |
|   |     - ISACA 감리 · ISO 27001/27701 · TISAX · K-ISMS         |        |
|   |     - KPI: ROI, TCO, NPV, SLA, CX, NPS, RTO/RPO            |        |
|   +-------------------------------------------------------------+        |
|                                                                          |
+--------------------------------------------------------------------------+
```

**왜 필요한가? — 패러다임 비교**

| 시대 | 1980~2000 (전통) | 2010~2020 (클라우드 전환) | 2024~ (AI-Native, Regulated) |
| :--- | :--- | :--- | :--- |
| **IT의 위치** | 비용(Cost Center) | 전략 자산(Strategic Asset) | 사업 핵심(Core Business) |
| **관리 주체** | CIO 독점, 실리콘벽 | CIO-CDMO-CTO 분리 | 통합 C-Suite + CISO + CDO |
| **가치 측정** | 가용성(99.9%) | TCO 절감 | 가치 흐름(Value Stream) + ESG |
| **규제** | 내부 통제 | SOX, ISMS | AI Act, DORA, ESG, 데이터3법 |
| **변화 속도** | 분기/반기 단위 | 월/주 단위 | 실시간/지속적(CI/CD) |

- **📢 섹션 요약 비유**: 토픽 572번은 마치 **"도시의 종합 교통관제 시스템"**과 같다. 이사회(국정위원회), CIO(교통부장관), 운영(지하철·도로·공항), 감시(CCTV·신호등)가 **표준 신호 체계(COBIT/ITIL)**로 연결되어야 시민(현업/고객)이 안전하고 빠르게 이동할 수 있다. 신호 체계가 없으면 아무리 좋은 차(기술)가 있어도 정체·사고만 늘어난다.

---

## Ⅱ. 아키텍처 및 핵심 원리

토픽 572번의 **아키텍처 4계층 모델**은 국제 표준 기반의 의사결정-실행-측정 체계를 나타낸다. 각 계층은 **RACI 매트릭스**(Responsible, Accountable, Consulted, Informed)와 **3 Lines Model**(IIA, 2020)을 통해 책임 소재가 명확해진다.

```text
   +--------------- 거버넌스 의사결정 흐름 (Top-Down + Bottom-Up) ----------+
   |                                                                        |
   |   Board -► CEO -► CIO -► PMO/CoE -► Squad/Tribe -► Product/Service   |
   |     ^                              |                                   |
   |     |            ^                 |                                   |
   |     |            |                 v                                   |
   |   감사위원회 ◄-- 리스크위원회 ◄-- KPI/KRI 대시보드                      |
   |                                                                        |
   |   +---------+   +---------+   +---------+   +---------+              |
   |   |전략(Str)|--►|포트폴리오|--►|프로그램  |--►|프로젝트  |              |
   |   | SBP/ISP |   | PfM     |   | PgM     |   | Delivery|              |
   |   +----+----+   +----+----+   +----+----+   +----+----+              |
   |        |             |             |             |                    |
   |        v             v             v             v                    |
   |   [BCP/DR]      [FinOps/ITFM]  [Agile/SAFe]  [DevSecOps]              |
   |                                                                        |
   +------------------------------------------------------------------------+
```

**표준 프레임워크 매핑 구조 (COBIT 2019 × ITIL 4 × ISO 38500)**

| 구성 요소 (Layer) | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **① ISO/IEC 38500** (거버넌스 원칙) | 이사회-경영진의 IT 의사결정 6원칙 | **R**esponsibility(책임), **A**ccountability(설명), **S**trategy(전략 정렬), **A**cquisition(수탁), **P**erformance(성과), **C**onformance(규정 준수) — RACI를 E(평가)·D(지시)·M(모니터링) 사이클로 운영 |
| **② COBIT 2019** (관리 목표 체계) | 40개 관리목표(EDM 5 + APO 14 + BAI 11 + DSS 6 + MEA 4) + 7대 구성요소 | **Cascade of Goals**(전략적 목표->이해관계자 요구->기업 목표->정렬 목표->관리목표->주요 프로세스) — 설계 요인 11개로 조직별 맞춤화 |
| **③ ITIL 4** (서비스 가치 시스템) | 34개 Practice(실무)·Value Chain·7-Guiding Principle | SVS(Value chain: Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support) + **Service Value Chain(SVC)** + Four Dimensions(조직/정보/파트너/가치흐름) |
| **④ TOGAF 10** (아키텍처) | ADM(Architecture Development Method) 8단계 사이클 | **Phase A~H**: Vision->Business->IS->Tech->Opportunity->Migration->Impl. Governance->Change Mgmt — **Architecture Repository**(ABB·SBB·ARB) |
| **⑤ K-ICT BS / EA-Reference Model** | 한국 공공 EA 표준 | 업무/데이터/응용/기술/보안 5개 아키텍처 도메인, eTOM·FEAF 매핑 |
| **⑥ 3 Lines of Defense (IIA 2020)** | 리스크/통제 책임 분리 | 1st Line(운영·소유), 2nd Line(리스크·컴플), 3rd Line(내부감사) + 외부감사(4th) |

**핵심 작동 원리 — 목표 연쇄(Goals Cascade) 알고리즘**

COBIT 2019의 가장 중요한 메커니즘은 **Cascade of Goals**이다. 이는 아래의 **연쇄 방정식**으로 표현할 수 있다.

```
[비즈니스 목표 달성도] = Σ (IT 관리목표 성숙도 × Cascade 가중치 × Risk Premium)
       v
[IT 거버넌스 효과성]  =  Σ (KGI × Benefit Realization Rate) / Σ (Investment TCO)
       v
[엔터프라이즈 가치]   =  (Revenue IT_Impacted + Cost Avoidance + Risk Mitigation) − Σ IT Spend
```

**핵심 측정 지표 체계 (Balanced Scorecard 4관점 × 3-Tier)**

| 관점 | Lagging KGI (결과) | Leading KPI (선행) | KRI (리스크) |
| :--- | :--- | :--- | :--- |
| **Financial** | RIT(Return on IT), TCO 절감률, NPV | 예산 편성 정확도, FinOps 절감률 | CapEx/Opex 비율, Shadow IT 비용 |
| **Customer** | NPS, CSAT, 디지털 채널 점유율 | 사용성 점수, First Contact Resolution | 데이터 유출 건수, 인시던트당 영향도 |
| **Internal Process** | SLA 달성률, Change Success Rate, MTTR | Deployment Frequency, Lead Time, MTTD, CFR(Change Failure Rate) | 취약점 평균 노출 기간, Patch 지연 |
| **Learning & Growth** | 직원 디지털 역량 지수, Cert 보유율 | 학습 시간, CoE 활용 건수 | 핵심 인력 이직률, Single Point of Failure |

**핵심 알고리즘/공식 (실무 산식)**

1. **RIT(Return on IT)** = `(IT 기여 이익 − IT 총비용) / IT 총비용 × 100`  (목표: ≥ 25%)
2. **TCO 산정** = `직접비(HW/SW/Lic) + 운영비(인건비/외주) + 간접비(다운타임/Shadow IT)`
3. **COBIT Maturity Level**: 0(부재) -> 1(초기) -> 2(관리) -> 3(정의) -> 4(정량) -> 5(최적) (ISO/IEC 15504 PAM 기반)
4. **DORA 4 Metrics**: Deployment Freq, Lead Time for Change, MTTR, Change Failure Rate (Elite Performers 기준)
5. **Value Realization Rate** = `실제 실현 가치 / 계획 가치 × 100` (목표 ≥ 80%)

- **📢 섹션 요약 비유**: 이 아키텍처는 **"의료 시스템"**과 같다. 이사회(보건복지부) = 정책, COBIT(의학 용어집) = 진단 기준, ITIL(진료 프로세스) = 치료, TOGAF(해부학) = 몸의 구조, KPI 대시보드(바이탈 사인) = 환자 상태 모니터링. 각 계층이 정확히 작동해야 "건강한 기업"이 유지된다.

---

## Ⅲ. 비교 및 연결

**주요 거버넌스/관리 프레임워크 비교 (기술사 빈출 비교 문제)**

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **CMMI v2.0** | **TOGAF 10** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **핵심 목적** | IT 거버넌스/관리 목표 | IT 서비스 관리(Svc Mgmt) | IT 거버넌스 원칙 | 프로세스 성숙도 | EA 개발 방법론 |
| **관점** | 경영진/감사용 | 실무자/운영자용 | 이사회/거버넌스 | 프로세스 개선 | 아키텍트 |
| **구조** | 40 EDM/APO/BAI/DSS/MEA | 34 Practices + SVS | 6 Principles | 5 Maturity Level | ADM 8 Phase |
| **측정** | 목표-지표 연쇄 | 4D + SVC Value | E/D/M 사이클 | PAM
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 572 / 800

<- **이전**: [571. IT 경영 관리 핵심 토픽 571번 시험 요약](/studynote/12_it_management/05_security_compliance/571_it_management_core_topic_571_exam_summary/)
**다음**: [573. IT 경영 관리 핵심 토픽 573번 시험 요약](/studynote/12_it_management/05_security_compliance/573_it_management_core_topic_573_exam_summary/) ->

---
