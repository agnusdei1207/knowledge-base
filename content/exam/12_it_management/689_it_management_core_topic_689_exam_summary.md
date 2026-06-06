---
title: "IT Management Core Topic 689 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019**(거버넌스/관리 목표 40개), **ITIL 4**(34개 실무 관행), **ISO/IEC 38500**(6원칙)을 통합한 **3차원 거버넌스 체계(평가-지휘-모니터)**로, Value Creation(가치창출)·Risk Optimization(위험최적화)·Resource Optimization(자원최적화) 균형을 통해 **Business-IT Alignment**를 달성하는 경영과학이다.
> 2. **가치**: 통계적으로 IT 거버넌스 성숙도 상위 25% 기업은 EBITDA 마진이 **평균 3.2%p**, 매출총이익률 **2.8%p** 높으며(소스: PwC 2023 IT Governance Survey), IT 프로젝트 실패율 **38%->15%**, Shadow IT 비용 **연간 23% 절감**, 정보보호 사고 대응시간 **MTTR 71% 단축** 효과를 제공한다.
> 3. **판단 포인트**: **집중형(중앙 거버넌스 위원회) vs 분산형(Federated) vs 하이브리드(Center-of-Excellence)** 모델 선택, **RACI 매트릭스** 기반 책임 소재 명확화, **Stage-Gate 프로세스**에서 Gate 1(전략)->Gate 2(타당성)->Gate 3(설계)->Gate 4(구축)->Gate 5(운영) 별 **Exit Criteria** 수립 여부가 ROI 4배 차이를 만든다.

---

## Ⅰ. 개요 및 필요성

정보기술은 더 이상 **Cost Center(비용 센터)** 가 아닌 **Business Value Driver(사업 가치 동인)** 로서, CFO·CDO·CISO·CDO가 공동 책임을 지는 **C-Suite 거버넌스** 영역으로 격상되었다. 한국 정보화진흥원의 「정보시스템 감리 가이드」와 「디지털정부 구현을 위한 행정정보화법」에 따라 공공부문의 경우 일정 규모 이상 프로젝트는 **법적 감리 의무**가 있으며, 일반 기업도 글로벌 경쟁력 확보를 위해 **ISO/IEC 38500**, **COBIT 2019**, **ISMS-P**, **PIMS** 인증을 요구받고 있다.

**근본적 문제 인식:**
- **사일로(Silo) 현상**: 사업부서별 독립 IT 운영 -> 중복투자 30%+, 통합 시너지 0
- **Shadow IT 증가**: Gartner(2023) 기준 대기업 IT 예산의 **41%가 비인가 IT**에 집행
- **Digital Disruption 대응 지연**: 평균 Legacy 시스템 비중 68%, 신규 서비스 출시까지 14개월 소요
- **규제 환경 강화**: 개인정보보호법, ESG 공시, EU AI Act, Dodd-Frank에 따른 IT 통제 요구 급증

```text
+--------------------------------------------------------------------------+
|            IT 경영 관리 3-축 거버넌스 프레임워크 (Integrated View)         |
+--------------------------------------------------------------------------+
|                                                                          |
|   [Stakeholders]              [Concerns]              [Solutions]       |
|   -------------               ---------               -----------       |
|   • 주주/이사회              • Benefit                • COBIT 2019       |
|   • 임원(CIO, CFO,          • Risk                   • ITIL 4           |
|     CDO, CISO, CRO)         • Resource              • ISO 38500        |
|   • 사업부서                 • Compliance             • PMBOK 7           |
|   • IT 조직                  • Performance            • TOGAF 10         |
|   • 외부 감사/감사원         • Strategic Fit          • ISO 27001        |
|   • 고객/파트너              • Risk Mgmt              • BCM/DR           |
|   • 규제기관                                              v                |
|        |                        |                       |                |
|        +------------+-----------+-----------+-----------+                |
|                     v                       v                            |
|   +-------------------------------------------------------------+        |
|   |     거버넌스 체계(Governance System) — 책임·권한·의사결정      |        |
|   |   +-----------------------------------------------------+  |        |
|   |   | 1) 평가(Evaluate)  ->  2) 지휘(Direct)  ->  3) 모니터  |  |        |
|   |   |    SWOT/CSF          Portfolio Mgmt      KPI/BSC    |  |        |
|   |   +-----------------------------------------------------+  |        |
|   +-------------------------------------------------------------+        |
|                              |                                          |
|                              v                                          |
|   +--------------------------------------------------------------+       |
|   |   관리 체계(Management System) — 계획·빌드·실행·운영(PDCA)    |       |
|   |   +--------+--------+--------+--------+                    |       |
|   |   | Plan  | Build  | Run    | Monitor|   (ITIL 4 SVS)       |       |
|   |   | 전략  | 설계  | 운영  | 개선   |                    |       |
|   |   +--------+--------+--------+--------+                    |       |
|   +--------------------------------------------------------------+       |
|                              |                                          |
|                              v                                          |
|   +--------------------------------------------------------------+       |
|   |   Value Outcome: Benefit Realization + Risk Optimization     |       |
|   |                 + Resource Optimization (COBIT 2019 Goals)    |       |
|   +--------------------------------------------------------------+       |
+--------------------------------------------------------------------------+
```

**구시대(Pre-2010) vs 신시대(2024+) IT 경영 패러다임 비교:**
- **과거(1세대)**: 데이터센터 운영 중심, ITIL v2 기반 **프로세스·티켓(Service Desk) 관리**, CAPEX 위주
- **현재(2세대)**: Agile/DevOps + ITIL 4 **Value Stream** 관점, OPEX 전환, FinOps
- **미래(3세대)**: **AI-Augmented Governance**(AIOps, RPA, GenAI), Autonomous IT, **Digital Ethics**, AI 거버넌스 통합

- **📢 섹션 요약 비유**: IT 경영 관리는 **배의 키(舵)** 와 같습니다. 돛(기술)과 노(인력)는 아무리 좋아도, 키가 어긋나면 목적지에 도달하지 못합니다. **COBIT**는 이 키의 설계도, **ITIL**은 노 젓는 법, **ISO 38500**은 항해 규칙에 비유됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **3-Layer Architecture** — **전략층(Governance)** · **전술층(Portfolio/Program)** · **운영층(Delivery/Service)** — 이다. 각 계층은 **CSF(핵심성공요인)** 와 **KGI/KPI** 로 연결되며, **Stage-Gate** 프로세스로 의사결정 시점을 통제한다.

```text
+------------------------------------------------------------------------+
|                    IT 경영 관리 계층 구조 (Layered Architecture)         |
+------------------------------------------------------------------------+
|                                                                        |
|  +----------------------------------------------------------------+   |
|  |  Layer 1: GOVERNANCE (전략/이사회)                              |   |
|  |  -----------------------------------                            |   |
|  |  • 이사회 -> IT Steering Committee -> IT Audit Committee        |   |
|  |  • 책임 원리: 책임(Account) ≠ 권한(Authority) ≠ 실행(Do)        |   |
|  |  • 산출물: IT Charter, Policies, Risk Appetite Statement        |   |
|  |  • Frameworks: ISO 38500(6원칙), COBIT 2019(EDF+Cascade)       |   |
|  +----------------------------------------------------------------+   |
|                              | RACI 매트릭스                           |
|                              v                                         |
|  +----------------------------------------------------------------+   |
|  |  Layer 2: PORTFOLIO/PROGRAM MANAGEMENT (전술/CIO)              |   |
|  |  -----------------------------------                            |   |
|  |  • IT 전략(IT Strategy Map) ↔ Business Strategy 연결           |   |
|  |  • Portfolio: 투자-성과-위험 3축 균형                            |   |
|  |  • Stage-Gate: G1(전략) G2(타당성) G3(설계) G4(구축) G5(운영)    |   |
|  |  • 도구: Lean Portfolio Mgmt(LPM), PPM Tool, EA Repository     |   |
|  +----------------------------------------------------------------+   |
|                              | Resource Allocation                      |
|                              v                                         |
|  +----------------------------------------------------------------+   |
|  |  Layer 3: DELIVERY/SERVICE (실행/IT조직+사업협력)               |   |
|  |  -----------------------------------                            |   |
|  |  • 프로젝트(Projects): PMBOK, PRINCE2, Agile(Scrum/Kanban)     |   |
|  |  • 서비스(Services): ITIL 4 SVS(34 Practices), SLO/SLA        |   |
|  |  • 운영(Ops): SRE, AIOps, Observability(Prometheus/Grafana)    |   |
|  |  • 변화(Change): CAB, CAB/ECAB, Normal/Standard/Emergency      |   |
|  +----------------------------------------------------------------+   |
|                                                                        |
|  ---------------- 횡단(Transversal) 지원 체계 ----------------         |
|  • 아키텍처 거버넌스: TOGAF 10 ADM(8단계) + ArchiMate 3.2             |
|  • 보안 거버넌스: ISO 27001(Annex A 93 통제), ISMS-P, Zero-Trust     |
|  • 데이터 거버넌스: DAMA-DMBOK 2(11 지식영역), 데이터 카탈로그       |
|  • 위험 거버넌스: ISO 31000, NIST RMF(Identify-Protect-Detect...)    |
|  • 공급사 거버넌스: SLM(Service Level Mgmt), VMO(Vendor Mgmt Office) |
+------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT Steering Committee (이사회 산하)** | 거버넌스 최고 의사결정 기구 | 분기 1회 정기회의 + 임시회의, **의사정족수 2/3 이상**, 안건: 전략·예산·리스크·중대 투자(>$1M). 의사록은 **감사 추적(Audit Trail)** 위해 7년 이상 보존. |
| **COBIT 2019 Governance System** | 40개 거버넌스/관리 목표 프레임워크 | **Cascade Goals(연쇄 목표)**: Stakeholder Needs->Enterprise Goals(13개)->Alignment Goals(13개)->Management Objectives(40개). **Design Factors 11개**로 시스템 맞춤 설계. **Focus Area**(예: 사이버보안, DevOps, 위험)별 추가 목표 활성화. |
| **RACI 매트릭스** | 책임·권한·협의·정보제공 명확화 | **R**(Responsible: 실행)·**A**(Accountable: 최종결정, 1인)·**C**(Consulted: 자문, 양방향)·**I**(Informed: 통보, 단방향). **Accountable은 반드시 1명**이어야 하며, 기술사 시험 단골 출제 포인트. |
| **Stage-Gate Process** | 단계별 의사결정 Gate를 통한 Go/Kill 통제 | **G1 전략 적합성**->**G2 사업 타당성(BCR≥1.5, NPV≥0, IRR≥Hurdle Rate)**->**G3 아키텍처 적합성**->**G4 구축 준비도**->**G5 운영 이관 준비도(Benefit Realization Plan 수립)**. 각 Gate별 **Exit Criteria** 명확화 필수. |
| **Balanced Scorecard (BSC)** | 전략 실행도 4관점 균형 측정 | **Financial**(ROI, Cost Reduction)·**Customer**(NPS, SLA)·**Internal Process**(MTTR, Change Success Rate ≥95%)·**Learning/Growth**(직원 역량, Innovation Index). **Strategy Map**으로 인과관계 도식화. |
| **EA(Enterprise Architecture) Repository** | 아키텍처 자산 통합 관리 | **TOGAF 10 ADM**: Preliminary->A(비전)->B/C/D/E(4개 영역: Biz/Data/App/Tech)->F(마이그레이션)->G(구현 거버넌스)->H(변경 관리)->**Requirements Mgmt(중심 허브)**. **ArchiMate 3.2** 모티프: 3 Layers × 3 Aspects = 9개 셀. |
| **ITIL 4 Service Value System (SVS)** | 가치 공동창출 활동 체계 | **Service Value Chain**(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve) + **34 Practices**(일반 14, 서비스 9, 기술 7, 경영 4). **Continual Improvement Model**(DPI: Define-Engage-Design-Transition-Operate + Where to look/What to do/How to do/Immediate/Sustained steps). |

**핵심 알고리즘 및 산식 — IT 투자평가 3대 기법 (기술사 빈출):**

1. **NPV (순현재가치)**: NPV = Σ[CFt / (1+r)^t] − I0
   - 양수일수록 수용, 할인율(r)은 **WACC(가중평균자본비용)** 적용
   - 공공부문은 **사회적 할인율**(한국: 4.5%) 적용

2. **IRR (내부수익률)**: NPV=0이 되는 r
   - IRR ≥ Hurdle Rate(통상 WACC+α)일 때 수용
   - 한계: 상호배타적 프로젝트 비교 부적합 -> NPV 우선

3. **BCR (편익비용비)**: BCR = Σ(Bt / (1+r)^t) / Σ(Ct / (1+r)^t)
   - BCR ≥ 1.0(또는 공공부문 1.5)일 때 수용
   - **TCO(총소유비용)** 기반
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 689 / 800

<- **이전**: [688. IT 경영 관리 핵심 토픽 688번 시험 요약](/studynote/12_it_management/05_security_compliance/688_it_management_core_topic_688_exam_summary/)
**다음**: [690. IT 경영 관리 핵심 토픽 690번 시험 요약](/studynote/12_it_management/05_security_compliance/690_it_management_core_topic_690_exam_summary/) ->

---
