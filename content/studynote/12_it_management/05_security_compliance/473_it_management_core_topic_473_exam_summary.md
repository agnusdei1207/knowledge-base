---
title: "473. IT 경영 관리 핵심 토픽 473번 시험 요약 (IT Management Core Topic 473 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


# 📘 IT 경영 관리 핵심 토픽 473번 시험 요약 (IT Management Core Topic 473 Exam Summary)

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **"전략–거버넌스–아키텍처–운영–성과"** 5계층을 하나의 가치 사슬(Value Chain)로 통합하는 체계이며, COBIT 2019·ITIL 4·TOGAF·PMBOK 7th·ISO/IEC 38500을 국제 표준 축으로 융합해 의사결정의 일관성(Governance)과 실행의 유연성(Management)을 동시에 확보하는 것이 본질이다.
> 2. **가치**: 정량적으로는 **IT 비용 대비 사업 가치(ROI/VOI) 20~35% 향상**, 정성적으로는 **의사결정 속도 40% 단축, 리스크 가시화율 90% 이상, 규제 대응 리드타임 50% 축소**를 통해 기업 전체의 디지털 경쟁력과 ESG·컴플라이언스 신뢰도를 동시에 제고한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **(a) 중앙집권형 거버넌스 vs 사업부 자율형 페더레이션**, **(b) 아키텍처 표준화(One-Architecture) vs 도메인별 최적화(Best-of-Breed)**, **(c) 즉시 가치(Quick-Win) vs 기반 투자(Platform Building)** 의 3축이며, 기술사는 **"왜(Why) 이 표준을 채택했는가"의 경영학적 근거**와 **"어떻게(How) 기존 레거시와 공존시키는가"의 이행 청사진**을 모두 논증할 수 있어야 한다.

---

## Ⅰ. 개요 및 필요성

현대 기업은 **"디지털 비즈니스 = IT 비즈니스"** 라는 공식이 성립하는 VUCA(Volatility·Uncertainty·Complexity·Ambiguity) 환경에 직면해 있다. 과거에는 IT가 **비용 센터(Cost Center)** 로 인식되었으나, 클라우드·AI·데이터 분석이 보편화된 2020년대 이후에는 **전략적 가치 창출 센터(Strategic Value Driver)** 로 그 위치가 근본적으로 재정의되었다. 이에 따라 **CFOs와 CDOs(Chief Data Officer)·CIOs·CISOs**가 동등한 자리에서 거버넌스를 논하는 **"Tri-Chair 모델"** 이 글로벌 표준으로 자리 잡고 있으며, 이 변화의 중심에 **"IT 경영 관리(Information Technology Management)"** 가 있다.

IT 경영 관리가 다루는 영역은 단순히 서버·네트워크 운영이 아니라, **① 사업 전략과 IT 전략의 정렬(Strategic Alignment)**, **② IT 투자 의사결정의 합리화(Portfolio Rationalization)**, **③ 거버넌스·리스크·컴플라이언스 통합(GRC)**, **④ 아키텍처·프로세스·서비스의 표준화**, **⑤ 성과 측정과 지속적 개선(Continuous Improvement)** 의 5대 영역을 포괄한다.

```text
[정보화 시대 vs 디지털 시대 패러다임 비교]
+-----------------------------------------------------------------+
|  [정보화 시대 (1990~2010)]                                      |
|  +--------------+      +--------------+      +--------------+  |
|  | 사업 전략    | ----> | IT 전략      | ----> | 시스템 구축  |  |
|  +--------------+      +--------------+      +--------------+  |
|      ^ 단방향, 후행적, 비용 중심                                 |
|                                                                  |
|  [디지털 시대 (2010~현재)]                                       |
|  +----------------------------------------------------------+   |
|  |            전략-거버넌스-아키텍처 동시 공진화              |   |
|  |  +----------+ ⇄ +----------+ ⇄ +----------+ ⇄ +----+  |   |
|  |  | 사업전략 |   | IT전략   |   | EA/플랫폼|   |Ops |  |   |
|  |  +----------+   +----------+   +----------+   +----+  |   |
|  |         ↘  KPI·BSC·리스크·가치  측정 피드백  ↙          |   |
|  +----------------------------------------------------------+   |
|      ^ 양방향, 동시진화, 가치 중심, 데이터 드리븐                 |
+-----------------------------------------------------------------+
```

기존 정보화 패러다임은 사업 전략이 먼저 결정되면 IT가 이를 **"받아 구현"** 하는 후행적 관계였으나, 오늘날에는 **"Digital First"** 원칙 하에 사업 모델 자체가 IT·데이터·플랫폼을 전제로 설계된다. 예를 들어 카카오의 **"토스(Toss)"** 처럼 금융·인증·결제·커뮤니케이션이 하나의 슈퍼앱으로 통합되는 모델, Netflix의 **"데이터-드리븐 콘텐츠"** 의사결정, 아마존의 **"Two-Pizza Team + API 거버넌스"** 가 이를 상징한다. 이처럼 **IT는 더 이상 사업의 부산물이 아니라, 사업의 전제 조건** 이 되었기에 이를 **통합적으로 경영·관리할 수 있는 체계**가 필수적이다.

특히 **클라우드 전환, 생성형 AI 도입, 데이터 거버넌스, ESG 공시, 개인정보보호법·AI 기본법 등** 규제 환경이 동시에 급변하면서, 사일로(Silo)별로 운영되던 IT 관리 체계는 더 이상 작동하지 않는다. **"One Company, One Architecture, One Data, One Security"** 라는 슬로건 아래 통합 거버넌스를 구축하는 것이 생존의 조건이 되었고, 이때 적용되는 것이 바로 **COBIT 2019, ITIL 4, ISO/IEC 38500, ISO/IEC 27001, NIST CSF, TOGAF, PMBOK 7th** 등 글로벌 표준 프레임워크이다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **"도시의 도시 계획(Urban Planning)"** 과 같다. 도로·상하수도·전기·통신 인프라가 도시의 성장 잠재력을 결정하듯, IT 거버넌스·아키텍처·플랫폼은 기업의 미래 확장성과 회복탄력성을 결정한다. 집 한 채는 혼자 지을 수 있지만, 도시는总体规划 없이 지으면 무너진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리는 **"Strategy -> Governance -> Architecture -> Delivery -> Operation -> Value"** 의 6단계 가치 사슬로 구성되며, 각 단계는 **Cascade(폭포)** 모델로 흘러가면서 동시에 **Feedback Loop** 로 피드백된다. 핵심은 **"Plan-Do-Check-Act(PDCA)"** 가 데밍 사이클로 작동하되, **"Strategy(Plan) -> Delivery(Do) -> Performance(Check) -> Improvement(Act)"** 의 메타-사이클이 한 단계 위에서 전체를 조율하는 **"이중 루프 러닝( Double-Loop Learning)"** 구조라는 점이다.

```text
[IT 경영 관리 6단계 가치 사슬 & 거버넌스·관리 분리(Govern/Manage)]
+---------------------------------------------------------------------+
| 1) Strategy(전략)        : ISP, 디지털 전환 로드맵, IT-BSC          |
|            |                                                        |
|            v  [Governance Layer - 의사결정]                          |
| 2) Governance(거버넌스)  : COBIT 2019, ISO 38500, RACI, 정책체계    |
|            |  -- "What & Why" + 권한·책임·통제                       |
|            v  [Management Layer - 실행]                              |
| 3) Architecture(아키텍처): TOGAF ADM, Zachman, 레퍼런스 모델         |
|            |                                                        |
|            v                                                        |
| 4) Delivery(전달)        : PMBOK 7th, Agile, DevOps, MSP, Prince2    |
|            |                                                        |
|            v                                                        |
| 5) Operation(운영)        : ITIL 4 (SVS·34 Practices), AIOps, SRE    |
|            |                                                        |
|            v                                                        |
| 6) Value(가치)           : BSC, KPI/CSF, ROI/VOI, NPS               |
|            |                                                        |
|            +------- Feedback --+                                    |
|                                v                                    |
|              [Continuous Improvement: Kaizen·Lean·Six-Sigma]        |
+---------------------------------------------------------------------+
```

**핵심 원리 ① — 거버넌스와 관리의 분리(Separation of Governance & Management, ISO/IEC 38500)**
- **거버넌스(Govern)**: 이사회·경영진이 **"무엇을(What), 왜(Why), 누구의 책임으로(Who)"** 의사결정하는 것 (Evaluate·Direct·Monitor)
- **관리(Manage)**: 실무조직이 **"어떻게(How), 언제(When), 어디서(Where)"** 실행하는 것 (Plan·Build·Run·Monitor)
- 기술사 논술에서 가장 빈번하게 출제되는 **"정통 통제"** 와 **"현장 자율"** 의 긴장 관계를 푸는 열쇠.

**핵심 원리 ② — COBIT 2019의 5도메인 / 40 Govern/Manage Objective**
- **EDM( Evaluate, Direct, Monitor) 5개** + **APO(Align, Plan, Organize) 14개** + **BAI(Build, Acquire, Implement) 11개** + **DSS(Deliver, Service, Support) 6개** + **MEA(Monitor, Evaluate, Assess) 4개** = 총 40개 거버넌스/관리 목표
- **Design Factors 11개** (전략·목표·리스크·컴플라이언스·위험도·역할·IT 이슈·랜드스케이프·기술采纳성·기업규모·역량)를 조합해 **"맞춤형 거버넌스 시스템(Tailored Governance System)"** 설계

**핵심 원리 ③ — 포트폴리오·프로그램·프로젝트의 3계층(Portfolio->Program->Project)**
- **포트폴리오**: 사업·재무·리스크 기준의 **"어떤 IT 투자를 할 것인가"** (전략)
- **프로그램**: 관련 프로젝트 묶음의 **"어떤 순서·의존성으로"** (전환)
- **프로젝트**: 단위 **"어떻게 일정·품질·비용 내"** (실행)
- PMBOK 7th는 **8개 Performance Domain**(Stakeholder·Team·Development Approach·Planning·Project Work·Delivery·Measurement·Uncertainty) + **12가지 Principle**로 재구성.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **전략(Strategy)** | 사업·IT 목표 정렬 | ISP(정보화전략계획), SWOT/PEST, IT-BSC, 디지털 전환 로드맵, BMC(Business Model Canvas), Wardley Maps |
| **거버넌스(Governance)** | 의사결정·통제·리스크 | COBIT 2019, ISO/IEC 38500, Three Lines Model(IIA), RACI, 정책·표준·지침 3단 위계, Risk Register·KRI |
| **아키텍처(Architecture)** | 청사진·표준·재사용 | TOGAF ADM 8단계( Prelim->A->B->C->D->E->F->G->Req.Mgmt), Zachman 6x6, FEAF, DoDAF, C4 Model |
| **전달(Delivery)** | 가치 실현·빌드 | PMBOK 7th, PRINCE2, MSP, SAFe, Scrum/Kanban, DevOps, SRE, FinOps, SecDevOps |
| **운영(Operation)** | 서비스 안정성·지속성 | ITIL 4 SVS(34 Practices), AIOps, Observability(Prometheus·Grafana·ELK), CMDB, SLO/SLI/SLA |
| **가치 측정(Value)** | ROI·VOI·성과 | KPI/CSF, IT-BSC(4관점), TCO, NPV·IRR, ROSI(정보보안 ROI), NPS, OKR |
| **컴플라이언스·보안** | 규제·리스크 관리 | ISO 27001/27002, NIST CSF, ISMS-P, GDPR·PIPC, AI 기본법, ISO 31000, BCM·DR(ISO 22301) |
| **데이터 거버넌스** | 데이터 자산화·품질 | DAMA-DMBOK, 데이터 카탈로그·품질·메타·마스터·계보, Data Mesh·Fabric, K-Anonymity·차등 프라이버시 |

**핵심 메커니즘 ① — Cascade(폭포) 모델**
- 사업 목표 -> IT 목표 -> 거버넌스/관리 목표 -> 프로세스 -> KPI 로 단계별 분해. COBIT의 **Goals Cascade** 가 대표적이며, 기술사는 "사업 KPI 매출 성장률 20% -> IT 목표 신규 서비스 출시 시간 50% 단축 -> 프로세스 목표 DevOps 배포 빈도 4배 향상 -> KPI 배포 리드타임 1일"과 같이 정량적 연쇄를 보여줘야 함.

**핵심 메커니즘 ② — RACI 매트릭스**
- Responsible(실행)·Accountable(책임)·Consulted(자문)·Informed(통보)의 4문자 매트릭스로, **"A는 반드시 1명"** 원칙과 **"현업-IT 공동 책임(Joint Accountability)"** 이 최근 트렌드.

**핵심 메커니즘 ③ — Three Lines Model(IIA, 2020)**
- **1st Line**: 사업부(Operational Management, 위험의 주체)
- **2nd Line**: IT·보안·리스크·컴플라이언스(Support & Oversight)
- **3rd Line**: 내부감사(Internal Audit, 독립적 assurance)
- 4자 구도에서 2nd Line의 "Risk Champion" 역할이 핵심.

**핵심 메커니즘 ④ — Continuous Improvement(CSI) Model**
- ITIL 4의 **CSI Approach 7단계**: (1) Vision 정의 -> (2) 현 상태 측정 -> (3) 상세 분석 -> (4) 개선 아이디어 도출 -> (5) 비즈니스 케이스 -> (6) 개선 실행 -> (7) 효과 측정. **"무엇을 측정할 것인가"** 가 성공의 80%를 좌우.

- **📢 섹션 요약 비유**: 이 6단계는 **"항공우주 산업의 미션 통제(Mission Control)"** 와 같다. 발사(전략)->궤도계산(거버넌스)->우주선 설계(아키텍처)->발사(Delivery)->궤도상 운영(Operation)->임무 성과 평가(Value)->다음 임무(Improvement) 로, 매 순간 텔레메트리(측정 데이터)가 의사결정자에게 흘러야 한다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 영역에서 자주 혼동되거나 비교되는 핵심 쌍(pair)들을 명확히 구분할 수 있어야 한다.

| 구분 | COBIT 2019(거버넌스 프레임워크) | ITIL 4(서비스 관리 프레임워크) |
| :--- | :--- | :--- |
| **목적** | IT가 사업 목표를 달성하도록 **의사결정·통제·책임**을 체계화 | IT **서비스의 설계-전환-운영-개선**을 최적화 |
| **관점** | **전사 거버넌스·이사회·CIO 관점**(상위) | **서비스 운영·실무 관점**(하위) |
| **핵심 개념** | 40 Governance/Management Objective, 11 Design Factor, Cascade | 34 Practices, Service Value System(SVS), 4D Model |
| **측정** | 목표 성숙도, 지표(Process·Outcome) | SLO/SLI, KPI, CSI Register |
| **적용 대상** | 모든 IT 거버넌스 의사결정, 감사, 컴플라이언스 | 서비스 데스크, 변경·릴리스, 인시던트, 문제 관리 |
| **관계** | **"What & Why
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 473 / 800

<- **이전**: [472. IT 경영 관리 핵심 토픽 472번 시험 요약](/studynote/12_it_management/05_security_compliance/472_it_management_core_topic_472_exam_summary/)
**다음**: [474. IT 경영 관리 핵심 토픽 474번 시험 요약](/studynote/12_it_management/05_security_compliance/474_it_management_core_topic_474_exam_summary/) ->

---
