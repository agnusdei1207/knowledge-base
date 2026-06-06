---
title: "IT Management Core Topic 722 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, ISO/IEC 38500 등 글로벌 거버넌스 프레임워크를 기반으로, **IT 거버넌스(Governance) -> IT 전략(Strategy) -> IT 포트폴리오 관리(Portfolio) -> IT 서비스 운영(Service) -> 가치 측정(Value)**의 5계층 구조를 통해 비즈니스 가치와 IT 투자 간의 정렬(Alignment)을 실현하는 통합 관리 체계이다.
> 2. **가치**: McKinsey & Company(2023) 조사에 따르면 성숙한 IT 거버넌스 체계 도입 기업은 **IT 투자 대비 ROI 23~35% 향상**, **프로젝트 실패율 40% 감소**, **Time-to-Market 28% 단축** 효과를 달성하며, ISO 38500 적용 시 이사회-경영진-IT 부서 간 책임 소재 명확화로 의사결정 리드타임을 평균 45% 단축한다.
> 3. **판단 포인트**: 프레임워크 선택 시 **COBIT vs ITIL vs TOGAF 간 중첩 영역(예: 변경관리, 위험관리)**의 중복 투자 회피, **Bimodal IT(Mode 1 안정성 vs Mode 2 민첩성)** 균형점, **Quantitative vs Qualitative KPI 혼용 비율(70:30 권고)**, 그리고 **클라우드 전환 시 CapEx->OpEx 모델 변경에 따른 TCO 재계산 주기(통상 3년)**가 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

정보기술의 단순한 도입을 넘어, **"IT가 비즈니스 전략의 동등한 파트너(Strategic Partner)"**로 기능하기 위한 체계적 관리 체계의 필요성이 대두되면서 IT 경영 관리(Information Technology Governance & Management)는 2000년대 초 **ISACA의 COBIT 4.0/5.0**, **영국 OGC의 ITIL v2/v3**, **ISO/IEC 38500(2008 제정, 2015 개정)**의 등장과 함께 학문적·실무적으로 확립되었다. 한국에서도 2009년 정보시스템감리법 개정, 2013년 클라우드컴퓨팅법, 2021년 데이터 산업법 등 IT 거버넌스 관련 법·제도가 정비되며 기술사 시험에서도 **IT 성과측정, EA(Enterprise Architecture) 정렬, 디지털 전환 전략**이 핵심 출제 영역으로 부상했다.

```text
[전통적 IT 운영 vs 현대적 IT 경영 관리 패러다임 비교]

  +-------------------------+         +------------------------------+
  | [기존: IT as Cost Center]|         | [현재: IT as Value Enabler] |
  | ----------------------- |   ->->->   | --------------------------  |
  | • CapEx 중심 HW 투자    |         | • OpEx+Subscription 모델    |
  | • 부서별 독립 시스템     |         | • 전사 통합 EA-TOGAF 적용   |
  | • 사후 장애 대응(Reactive)|        | • 사전 예방·예측(Proactive) |
  | • 개별 프로젝트 단위 성과 |         | • 포트폴리오+BSC+KPI 통합   |
  | • CFO 관점 비용 최소화   |         | • CEO 관점 가치 극대화     |
  +-------------------------+         +------------------------------+
                  |                              |
                  +------+-----------------------+
                         v
        +--------------------------------------+
        |  IT 경영 관리 5대 핵심 영역(5 Pillars)|
        |  ---------------------------------  |
        |  ① 거버넌스(Governance)               |
        |  ② 전략·계획(Strategy & Planning)    |
        |  ③ 포트폴리오(Portfolio Management)  |
        |  ④ 서비스(Service Management)        |
        |  ⑤ 가치·리스크(Value & Risk)         |
        +--------------------------------------+
```

기존 IT 운영은 **"시스템이 다운되면 복구하는"** 사후 대응형이었으나, 클라우드, AI, 데이터 경제 시대에는 **"IT가 비즈니스 기회를 만드는"** 사전 기획형으로 전환되어야 한다. 이는 단순한 기술 도입이 아닌 **문화(Culture)·조직(Organization)·프로세스(Process)·기술(Technology)**의 4차원 변화이며, **John Zachman의 EA 프레임워크(1987)**, **Henderson & Venkatraman의 Strategic Alignment Model(1993)**, **Weill & Ross의 IT Governance 연구(MIT Sloan, 2004)**가 이론적 토대를 제공한다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **"건물의 설계도(Zachman EA)와 관리 규정(COBIT), 입주자 서비스 매뉴얼(ITIL), 회계 감사 기준(ISO 38500)을 한 권의 도시계획 헌법으로 통합한 것"**과 같다. 건물이 아무리 높아도(기술이 우수해도) 설계도가 없으면(거버넌스 부재) 무너진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 5대 계층은 **상위 의사결정(거버넌스) -> 전략 매핑(전략) -> 자원 배분(포트폴리오) -> 실행·운영(서비스) -> 측정·환류(가치)**의 순환 구조(Closed-loop)를 형성한다. 각 계층은 아래와 같이 연결된다.

```text
[IT 경영 관리 5계층 순환 구조 및 프레임워크 매핑]

  +------------------------------------------------------------+
  |  Layer 1: 거버넌스 (Governance)                             |
  |  +- 주체: 이사회(Board) / IT steering Committee            |
  |  +- 프레임워크: COBIT 2019 + ISO/IEC 38500                 |
  |  +- 핵심 원칙: 책임(R)·전략(S)·획득(A)·성과(P)·준수(C)·인간(B)|
  +----------------------+-------------------------------------+
                         v (Strategy Translation)
  +------------------------------------------------------------+
  |  Layer 2: 전략·계획 (Strategy & Planning)                  |
  |  +- 주체: CIO / EA 팀 / 전략기획                          |
  |  +- 프레임워크: TOGAF 9.2 ADM + Zachman + SAM              |
  |  +- 핵심 산출물: EA Blueprint, IT Roadmap, Sourcing Strategy|
  +----------------------+-------------------------------------+
                         v (Investment Decision)
  +------------------------------------------------------------+
  |  Layer 3: 포트폴리오 (Portfolio Management)                |
  |  +- 주체: PMO / IT Finance / CFO                            |
  |  +- 프레임워크: COBIT EDM + PMI PfM / Stage-Gate          |
  |  +- 핵심 산출물: Project Charter, Business Case, Prioritization|
  +----------------------+-------------------------------------+
                         v (Execution & Operations)
  +------------------------------------------------------------+
  |  Layer 4: 서비스 (Service Management)                       |
  |  +- 주체: ITSM 팀 / DevOps / SRE                           |
  |  +- 프레임워크: ITIL 4 (SVS+34 Practices) + DevOps         |
  |  +- 핵심 산출물: SLA, Change Mgmt, Incident/Problem Catalog|
  +----------------------+-------------------------------------+
                         v (Measure & Feedback)
  +------------------------------------------------------------+
  |  Layer 5: 가치·리스크 (Value & Risk)                        |
  |  +- 주체: CRO / CISO / CIO / CDO                            |
  |  +- 프레임워크: ISO 31000 + ISO 27001 + Balanced Scorecard|
  |  +- 핵심 산출물: KPI/CSF, Risk Register, Value Realization |
  +----------------------+-------------------------------------+
                         |
                         +-----(Continuous Improvement: Kaizen)-+
                                                                   |
       +-----------------------------------------------------------+
       |  ※ 핵심 순환: Plan -> Build -> Run -> Measure -> Improve
       |  ※ TOGAF Preliminary Phase ↔ COBIT EDM ↔ ITIL SVS
       |     세 프레임워크가 같은 의도를 다른 언어로 표현함
       +-----------------------------------------------------------
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Layer 1: 거버넌스 (Governance)** | 이사회 및 경영진의 IT 의사결정 권한·책임·통제 구조 정의 | **COBIT 2019 Governance System**: 40개 관리목표(Objective)와 5개 도메인(EDM: Evaluate, Direct, Monitor + APO/BAI/DSS/MEA)을 통해 IT 활동을 "지휘-평가-감독" 사이클로 운영. **ISO/IEC 38500**: "RACI 행위자 모델(Directors, Management, Owners, Users, IT Professionals)"로 책임 소재 명확화. 한국 정보시스템감리법 제13조(감리기준)와 연계. |
| **Layer 2: 전략·계획 (Strategy & Planning)** | 비즈니스 전략과 IT 역량 간의 정렬(Gap Analysis) | **TOGAF 9.2 ADM 8단계**(Preliminary->A:Architecture Vision->B:Business->C:Data/Application/Technology->D:Opportunities->E:Migration->F:Implementation->G:Change Management)로 EA 수립. **Henderson-Venkatraman SAM(Strategic Alignment Model)**: Business Strategy ↔ IT Strategy 양방향 매트릭스. **Zachman 6x6 매트릭스**(What/How/Where/Who/When/Why × Planner/Owner/Designer/Builder/Subcontractor/Operational). |
| **Layer 3: 포트폴리오 (Portfolio Management)** | 제한된 IT 자원(예산·인력)의 최적 배분 및 프로젝트 우선순위 결정 | **PMI Portfolio Management 표준** + **Stage-Gate+ 프로세스**(Discovery->Scoping->Business Case->Development->Testing->Launch) + **NPV/IRR/Payback Period** 재무 분석. Gartner의 **Run-Grow-Transform(RGT)** 예산 배분 모델: 통상 70% Run, 20% Grow, 10% Transform. **Bimodal IT** 전략으로 Mode 1(안정성·예측가능성)과 Mode 2(민첩성·실험성) 분리 운영. |
| **Layer 4: 서비스 (Service Management)** | IT 서비스의 설계-전환-운영-개선 전 과정 관리 | **ITIL 4 Service Value System(SVS)**: 7개 GUIDING PRINCIPLES + 4개 DIMENSIONS(Organizations & People, Information & Technology, Partners & Suppliers, Value Streams & Processes) + 34개 PRACTICE(이전 26개 프로세스 확장). **DevOps CALMS** 모델(Culture, Automation, Lean, Measurement, Sharing). SRE의 **SLI/SLO/Error Budget** 개념. 주요 프로세스: Incident, Problem, Change Enablement, Service Request, Service Level, Continual Improvement. |
| **Layer 5: 가치·리스크 (Value & Risk)** | IT 투자의 비즈니스 가치 정량 측정 및 리스크 통제 | **Kaplan & Norton Balanced Scorecard(BSC)**: 4관점(Financial/Customer/Internal Process/Learning & Growth)에 IT KPI 매핑. **ISO 31000 Risk Management Process**(Context->Risk Identification->Analysis->Evaluation->Treatment->Monitoring). **Value Realization Office(VRO)**: Pre-Mortem(사전 실패 분석) + Post-Mortem(사후 회고). **TCO(Total Cost of Ownership)** 모델: 직접비(20%)+간접비(40%)+은닉비(40%) 구조. |

**핵심 알고리즘 및 공식**:

1. **SAM(Strategic Alignment Model) 정렬도 측정**:
   ```
   Alignment Score = Σ(Wi × (IT_Capability_i - Business_Need_i)^)^(-1)
   -> 정렬도가 높을수록(=값이 작을수록) IT-Business Gap이 적음
   ```
2. **IT 투자 ROI 계산(수정된 정보경제 모델)**:
   ```
   IT_ROI = (Tangible_Benefit + Intangible_Benefit × Conversion_Factor) / (Total_IT_Cost) × 100
   ※ Conversion_Factor: 무형效益 유상가치 환산율(통상 0.4~0.6)
   ```
3. **서비스 수준 종합 점수(SLCS)**:
   ```
   SLCS = Σ(SLA_Weight_i × Achievement_i) / Σ(SLA_Weight_i)
   -> 통상 95% 이상이면 정상, 90% 미만 시 서비스 개선 계획 수립
   ```
4. **리스크 우선순위(RPN, Risk Priority Number)**:
   ```
   RPN = Severity(1~10) × Occurrence(1~10) × Detection_Difficulty(1~10)
   -> RPN > 150 시 즉시 완화(Mitigation) 조치 필요
   ```
5. **EA 성숙도(TOGAF Maturity Model)**:
   ```
   Level 0: None -> Level 1: Initial -> Level 2: Under Development
   -> Level 3: Defined -> Level 4: Managed -> Level 5: Optimized
   -> 통상 한국 공공기관 평균 Level 2.3, 글로벌 우수기업 Level 4.5
   ```

- **📢 섹션 요약 비유**: 5계층 구조는 **"도시의 5단계 행정 체계"**와 같다. **Layer 1(국무회의)**에서 큰 방향을 정하고, **Layer 2(도시계획청)**가 청사진을 그으며, **Layer 3(재정관청)**이 예산을 배분하고, **Layer 4(시 공무국)**이 도로·상하수도를 운영하며, **Layer 5(평가원·감사원)**이 성과를
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 722 / 800

<- **이전**: [721. IT 경영 관리 핵심 토픽 721번 시험 요약](/studynote/12_it_management/05_security_compliance/721_it_management_core_topic_721_exam_summary/)
**다음**: [723. IT 경영 관리 핵심 토픽 723번 시험 요약](/studynote/12_it_management/05_security_compliance/723_it_management_core_topic_723_exam_summary/) ->

---
