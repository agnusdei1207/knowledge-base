---
title: "677. IT 경영 관리 핵심 토픽 677번 시험 요약 (IT Management Core Topic 677 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, PMBOK 7th, ISO 27001/38500 등 거버넌스·서비스·프로젝트·보안 프레임워크를 BSC·KPI·BPM 체계와 통합하여, **전략(S战略) -> 포트폴리오 -> 아키텍처 -> 운영 -> 가치 실현(Value Realization)** 의 폐루프(Closed-Loop)를 구축하는 활동이다.
> 2. **가치**: 정렬(Alignment) 지수 1단계 상승 시 프로젝트 성공률 약 25% 증가(Standish Group CHAOS Report 2023), TCO 30% 절감, SLA 가용성 99.9% -> 99.99% 향상, ISO 38500 기반 거버넌스 도입 시 이사회 IT 의사결정 속도 약 2.4배 개선 효과를 창출한다.
> 3. **판단 포인트**: **거버넌스(What/Why) vs 관리(How)** 의 경계, **CoE(Center of Excellence) vs Federated vs Decentralized** 조직 모델 선택, **Bottoms-up 요구사항 vs Top-down 전략**의 충돌 조정, **CapEx->OpEx 전환(클라우드/구독형)** 시 TCO 회계 처리 및 SLA 패널티 재설계가 핵심 의사결정 포인트이다.

---

## Ⅰ. 개요 및 필요성

정보관리 기술사 67번~70번대(정보시스템 구축·관리, IT 거버넌스) 출제 범위에서 **"IT 경영 관리"** 는 전략과 실행을 잇는 핵심 축이다. 과거(2000년대)에는 SI(System Integration) 중심의 프로젝트 단위 관리, 즉 **Triple Constraint(일정·비용·품질)** 만 강조했으나, 현재는 디지털 전환 환경에서 **거버넌스(governance)·컴플라이언스·사이버보안·ESG·데이터 주권** 까지 포함된 통합 경영 체계가 요구된다. 정보기술의 비중이 기업 자산·매출의 30~50%를 넘어선 시점에서 IT를 단순 비용(COST)이 아닌 **전략적 자산·레버리지**로 다루지 않는 조직은 경쟁에서 탈락한다. 따라서 COBIT 2019의 거버넌스 시스템, ITIL 4의 서비스 가치 체계(Value Chain), PMBOK 7th의 성과 도메인, ISO/IEC 38500의 6개 거버넌스 원칙, 그리고 BSC·EVA 같은 성과 측정 체계가 통합적으로 운영되어야 한다.

```text
+------------------------------------------------------------------+
|              IT 경영 관리 통합 프레임워크 (Top-Down)              |
+------------------------------------------------------------------+
  전략(Strategy)        --->  Porter 가치사슬, McKinsey 7S, SWOT
  |                          |
  v                          v
  정렬(Alignment)       --->  SAM(Strategic Alignment Model)
  |                          |     Henderson & Venkatraman 4개사분면
  v                          v
  거버넌스(Governance)   --->  COBIT 2019, ISO 38500 6원칙
  |                          |     Evaluate-Direct-Monitor
  v                          v
  포트폴리오(Portfolio)  --->  PIP(Prioritization by Impact/Probability)
  |                          |     BCG Matrix, NPV/IRR/ROIC
  v                          v
  아키텍처(Architecture) --->  TOGAF ADM, FEAF, DoDAF
  |                          |     EA Repository (ArchiMate)
  v                          v
  서비스/프로젝트       --->  ITIL 4 SVC(34 Practice), PMBOK 7th
  |                          |     DevOps, Agile@Scale(SAFe/LeSS)
  v                          v
  운영(Operation)       --->  SLA, OLA, UC,CSI(Continual Service Improvement)
  |                          |
  v                          v
  가치 실현(Value)       --->  BSC(4관점), KPI/KCI,KGI,Benefits Realization
  |                          |     ROI, Payback, EVA, NPS
  v                          v
  모니터링(Monitor)     --->  PDCA + OODA, 내부감사, ISMS-P, GRC
  |                          |
  +---- 피드백(Closed-Loop) -+
```

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **자동차의 계기판·핸들·엔진·브레이크가 하나로 통합된 운전 시스템**과 같다. COBIT은 **도로 교통법규**, ITIL은 **정비 매뉴얼**, PMBOK은 **운전 교본**, BSC는 **계기판의 4가지 다이얼(속도·연비·엔진온도·연료)**에 해당한다. 이 중 어느 하나라도 없으면 시속 200km의 고속도로(디지털 전환)에서 차체는 빠르게 무너진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **"정렬-거버넌스-운영-측정"**의 4계층 모델이다. 1계층(전략 정렬)에서는 **SAM(Henderson & Venkatraman)** 모델의 4사분면—**IT 전략 vs Business 전략의 Fit**, **IT 인프라 vs Business Process·조직 역량의 Integration**—을 통해 미스매치를 진단한다. 2계층(거버넌스)에서는 **COBIT 2019**의 40개 거버넌스/관리 목표(Governance & Management Objectives)와 **ISO/IEC 38500**의 6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)을 이사회(Board) 수준에서 적용하며, **EDM( Evaluate-Direct-Monitor )** 사이클을 분기/반기 단위로 수행한다. 3계층(서비스·프로젝트 운영)에서는 **ITIL 4**의 34개 Practice를 5개 영역(General, Service, Technical, Application, Business Management)으로 분류하고, **Service Value Chain(SVC)** 의 Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve 흐름을 자동화한다. 4계층(가치 측정)에서는 **BSC(Kaplan & Norton)**의 4관점(Financial, Customer, Internal Process, Learning & Growth)에 **IT Balanced Scorecard**의 5번째 관점(미래/IT 기여)을 결합하여, **Leading Indicator(예: 혁신 프로젝트 수)** 와 **Lagging Indicator(예: ROI, 가용성)** 를 동시에 추적한다.

```text
+---------------------------------------------------------------+
|        COBIT 2019 + ITIL 4 + PMBOK 7th 통합 거버넌스         |
+---------------------------------------------------------------+
   [이사회 / 전략위원회]   - EDM01~05 (Evaluate, Direct, Monitor)
        |                  +--> 책임(R), 성과(P), 위험(Risk)
        v
   [CIO / IT Steering]   ---> APO(Align, Plan, Organize) 14개
        |                  +- EDM(거버넌스) 5개
        |                  +- BAI(빌드·획득·구현) 11개
        |                  +- DSS(Delivery·Service·Support) 6개
        |                  +- MEA(Monitor·Evaluate·Assess) 3개
        v
   [서비스 운영 계층]     ---> ITIL 4 SVC
        |                   Plan->Engage->Design&Transition
        |                   ->Obtain/Build->Deliver&Support->Improve
        |                   + 34 Practices(예:IM,Change,Incident,
        |                    Problem,Service Desk,SLA,CSI)
        v
   [프로젝트/애자일 계층] ---> PMBOK 7th 8대 Performance Domain
        |                   Stakeholder, Team, Development Approach,
        |                   Planning, Project Work, Delivery,
        |                   Measurement, Uncertainty
        v
   [가치 측정/BSC]        ---> 4관점 KPI + IT BSC(5관점)
        |                   Financial : ROI, TCO 절감률, EVA
        |                   Customer  : NPS, SLA 준수율, CSAT
        |                   Process   : MTTR, 변경 성공률, 결함 누출
        |                   Learning  : 인력 인증수, 지식공유 횟수
        |                   Future    : 신기술 PoC 수,专利 수
        v
   [GRC 피드백]           ---> GRC Tool(Archer, ServiceNow GRC)
        |                   + ISMS-P, ISO 27001, 38500, PIMS
        v
   [Closed-Loop]          ---> 분기 거버넌스 회의로 환류
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 거버넌스 시스템** | 이사회–경영진–운영의 IT 의사결정 체계 | 40개 Governance/Management Objective, Cascade Goal(연쇄 목표), 11개 Design Factor 기반 맞춤화, **EDM 사이클**, **RACI 차트** |
| **ISO/IEC 38500** | IT 거버넌스 국제표준(6원칙) | Responsibility·Strategy·Acquisition·Performance·Conformance·Human Behavior, **Plan-Do-Check-Act**를 거버넌스 차원으로 확장 |
| **ITIL 4 Service Value System** | IT 서비스의 End-to-End 가치 흐름 | **SVS(SVC+Guiding Principles+Governance+Practices+Continual Improvement)**, 7 Guiding Principle(Focus on Value, Start Where You Are 등), 34 Practice |
| **PMBOK 7th / PRINCE2** | 프로젝트 관리 방법론 | 7th: 8대 Performance Domain + 12 Principle(Agile/Adaptive 친화), PRINCE2: 7 Principle·7 Process·7 Theme, **WBS·OBS·RAM·EV(Earned Value)** 분석 |
| **Balanced Scorecard & KPI** | 전략 실행 및 성과 측정 | 4관점(Financial·Customer·Internal·Learning) + IT BSC 5번째 관점, **SMART KPI**, **KGI/KPI 2단 구조**, **Strategy Map** 통한 인과관계 시각화 |
| **GRC (Governance-Risk-Compliance)** | 통합 리스크·컴플라이언스 | **RSA Archer, ServiceNow GRC, SAP GRC**, ISMS-P 인증, **Three Lines of Model(IIA)**, 리스크 히트맵(Impact×Likelihood 5×5) |
| **ITAM/FinOps** | IT 자산 및 클라우드 비용 최적화 | **CMDB, ITAM**(하드웨어·소프트웨어 라이선스), **FinOps Foundation** framework(Inform->Optimize->Operate), **Showback/Chargeback** 모델 |

### 핵심 알고리즘 및 산식

- **NPV(순현재가치)**: $NPV = \sum_{t=1}^{n}\frac{CF_t}{(1+r)^t} - I_0$ (r=할인율, I₀=초기투자)
- **IRR(내부수익률)**: NPV=0 이 되는 r
- **TCO(총소유비용)**: $TCO = CAPEX + \sum_{t=1}^{n}\frac{OPEX_t}{(1+r)^t} + Disposal Cost$ (H/W·S/W·인력·교육·다운타임 포함)
- **EV(Earned Value)**: $CV = EV - AC$ (Cost Variance), $SV = EV - PV$ (Schedule Variance), $CPI = EV/AC$, $SPI = EV/PV$
- **IT 정렬 지수(Strategic Alignment Maturity)**: SAM 5단계(L1:Initial~L5:Optimized), Luftman(2003) 6개 속성(Communication, Competency, Governance 등) 가중 평균

- **📢 섹션 요약 비유**: 거버넌스 체계는 **인체의 신경계**와 같다. 이사회–척수(COBIT) -> 말초신경–근육(ITIL) -> 손끝–도구(PMBOK) -> 통증 신호–반응(BSC/GRC) 의 사슬이 끊어지면 한쪽이 마비된다. BSC의 4관점은 **심장박동·체온·혈압·산소포화도** 같은 4가지 바이탈 사인이다.

---

## Ⅲ. 비교 및 연결

| 구분 | COBIT 2019 | ITIL 4 | PMBOK 7th / PRINCE2 | ISO 38500 |
| :--- | :--- | :--- | :--- | :--- |
| **계층/관점** | 거버넌스 + 관리(경영진) | 서비스 운영(Service) | 프로젝트 수행(Delivery) | 이사회 거버넌스(Board) |
| **핵심 목적** | 목표·리스크·자원 통합 관리 | IT 서비스 가치 제공 | 일시적 산출물(결과물) 생성 | IT 의사결정의 6원칙 준수 |
| **범위/Scope** | 전사 IT(End-to-End) | 서비스 생애주기 | 프로젝트 수명주기 | IT 거버넌스 결정 전반 |
| **성숙도/측정** | Process Assessment Model(PAM) | 4-Dimension Model, Maturity | 8 Performance Domain Maturity | 6원칙별 KPI |
| **적합 조직** | 대기업·금융·공공 | MSP·IDC·내부 IT | SI·PMO | 모든 조직(표준) |
| **Agile 친화도** | 중(DevOps 통합 가이드 별도) | 중(SVC에 Agile Practice 포함) | **상**(7th: 12 Principle 적응형) | 중(원칙 차원) |
| **연결 관계** | 상위 정책·KPI 정의 | COBIT DSS/MEA 활용 | COBIT BAI·DSS 활용 | COBIT EDM의 표준 토대 |
| **인증/감사** | COBIT 2019 Foundation/Design/Implement | ITIL 4 Foundation/MP/SL | PMP/PRINCE2 Practitioner | ISO 38500 Lead Auditor |
| **가치 측정** | Cascade Goal -> KPI | CSI 등록부 + KPI | EVM + Benefits Realization Plan | 6원칙별 책임 할당 |
| **한계** | 구현 복잡도 높음, 데스크 리스크 | 기술·도구·제품 비종속, 운영 편향 | 프로젝트 종료 후 가치 전이 어려움 | 추상적 원칙, 구현 가이드 미약 |

### 통합 상호연결(Touchpoint)

- **COBIT ↔ ITIL**: COBIT의 **DSS02(서비스 요청·사고), DSS03(문제), DSS04(연속성), DSS05(보안 서비스)** 가 ITIL Incident·Problem·Service Continuity·Information Security Practice와 1:1 매핑
- **COBIT ↔ PMBOK**: **BAI01(프로그램), BAI02(요구사항 정의), BAI03(솔루션 설계/구축)** 이 PMBOK의 Planning·Project Work·Delivery Domain과 매핑
- **ISO 38500 ↔ COBIT**: ISO 38500의 6원칙이 COBIT EDM의 평가 기준(예: Performance->EDM04, Conformance->EDM03)에 직접 반영
- **BSC ↔ COBIT**: BSC 관점별 KPI를 **Cascade
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 677 / 800

<- **이전**: [676. IT 경영 관리 핵심 토픽 676번 시험 요약](/studynote/12_it_management/05_security_compliance/676_it_management_core_topic_676_exam_summary/)
**다음**: [678. IT 경영 관리 핵심 토픽 678번 시험 요약](/studynote/12_it_management/05_security_compliance/678_it_management_core_topic_678_exam_summary/) ->

---
