---
title: "592. IT 경영 관리 핵심 토픽 592번 시험 요약 (IT Management Core Topic 592 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019의 40개 Governance & Management Objectives와 EDM-APO-BAI-DSS-MEA 5도메인, 11개 Design Factor, 6개 Component(Process·Structure·Information·People·Culture·Technology)를 결합하여 DX 시대의 IT-Biz Alignment와 Value Delivery를 정량적으로 보장하는 **IT 거버넌스-전략-포트폴리오 3층 통합 통제체계**.
> 2. **가치**: PMI 기준 IT 자원 낭비 11.4% -> 거버넌스 도입 시 240% ROI(통계적 평균), McKinsey 70% DX 실패율 -> Goal-Cascade 적용 시 50% 이하로 하락, ISO/IEC 38500 적용 조직의 Shadow IT 65~70% 감소, 의사결정 리드타임 40% 단축, 컴플라이언스 감사 비용 35% 절감.
> 3. **판단 포인트**: Centralized(예: 1,000인 이하) vs Federated(예: 글로벌 멀티비즈니스) 거버넌스 모델 선택, 11개 Design Factor 가중치 결정, 7단계 Goal Cascade(Stakeholder Needs->Enterprise Goals->Alignment Goals->Management Objectives), Build(자체 SI) vs Buy(MSA·SaaS) 전략 시 TCO 3~5년 분석, IT-Portfolio에서의 Run(70%)-Grow(20%)-Transform(10%) 배분 비율 최적화.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명, 코로나19 이후 가속화된 비대면 경제, 그리고 생성형 AI·클라우드·데이터 기반 서비스의 폭증으로 인해 CIO(Chief Information Officer)의 역할이 단순 "Cost Center 운영"에서 "**Digital Value Creator**"로 급격히 전환되었다. 한국정보화진흥원(KIAT)과 McKinsey Global Institute의 조사에 따르면 전 세계 DX 프로젝트의 약 **70%가 기대 이하의 성과를 거두거나 실패**하며, 그 핵심 원인 중 **52%가 IT-Biz 전략 부조화 및 거버넌스 부재**로 분석된다. Gartner(2024)는 "**Through 2027, 75% of large enterprises will have a CDO(Chief Data Officer) reporting directly to CEO**"라고 전망하며, 거버넌스-데이터-전략을 통합할 새로운 통제 체계의 필요성을 강조한다.

기존 패러다임은 **"기술 중심·프로젝트 단위·비용 회계"**였으나, DX 시대는 **"가치 중심·포트폴리오 단위·성과 회계"**로 전환되어야 한다. COBIT 2019는 이 전환을 체계적으로 지원하기 위해 6개의 거버넌스 원칙(Principle), 40개의 관리목표(Management Objective), 그리고 11개의 설계요인(Design Factor)을 제시한다. 특히 **7단계 Goal Cascade**는 Stakeholder Needs에서 시작해 Enterprise Goal -> Alignment Goal -> Management Objective -> Process -> Practice -> Activity까지의 인과 사슬을 명시하며, 이로 인해 "왜 이 프로젝트인가?"라는 비즈니스 질문에 정량적으로 답할 수 있다.

```text
[DX 시대 IT 거버넌스 패러다임 전환]

   전통적 IT 관리 (1990~2015)              DX 시대 IT 거버넌스 (2016~)
   +----------------------+                +----------------------+
   | • Cost Center 중심   |   --------►     | • Value Creator 중심 |
   | • Project 단위 관리  |    전환요인:    | • Portfolio 단위 관리|
   | • 기술 중심 의사결정 |   • Cloud      | • 비즈니스 가치 연계 |
   | • CapEx 일시성 회계  |   • AI/ML      | • Opex+CapEx 혼합회계|
   | • ITIL v2/v3 운영   |   • Data 규제  | • COBIT 2019 + ITIL 4|
   | • SI 하청 주력      |   • COVID-19   | • In-house+MSA+SaaS |
   +----------------------+   • ESG·PIPA  +----------------------+
            |                          ^
            |         [7단계 Goal Cascade]
            v                          |
   Stakeholder Needs -> Enterprise Goals -> Alignment Goals
   -> Governance/Management Objectives -> Process -> Practice -> Activity
```

- **📢 섹션 요약 비유**: 전통 IT 관리가 **"건물의 수도·전기만 점검하는 건물 관리사"**였다면, DX 시대 거버넌스는 **"도시 전체의 토지이용·교통·환경까지规划设计하는 도시계획가"**에 가깝다. 개별 시설(프로젝트)이 아니라 도시 전체(포트폴리오)의 가치를 최적화한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019는 **Governance System(거버넌스 체계)**와 **Governance Framework(거버넌스 프레임워크)** 두 트랙으로 구성된다. 핵심은 최상위 의사결정체인 **EDM(Evaluate-Direct-Monitor) 5개 Governance Objective**이며, 이를 4개 Management Domain(APO/BAI/DSS/MEA) 35개 Management Objective가 직접 지원한다. 모든 Management Objective는 6대 Component(Process·Organizational Structure·Information Flow·People·Culture·Technology)와 7단계 Goal Cascade에 의해 정의된다.

**11개 Design Factor**는 조직의 컨텍스트에 따라 거버넌스 시스템을 맞춤형으로 조정하는 변수이다: (1) Enterprise Strategy, (2) Enterprise Goals, (3) Risk Profile, (4) I&T-related Issues, (5) Threat Landscape, (6) Compliance Requirements, (7) Role of IT, (8) Sourcing Model for IT, (9) IT Implementation Methods, (10) Technology Adoption Strategy, (11) Enterprise Size. 각 DF는 0~100 사이의 우선순위 가중치로 환산되어, 35개 Management Objective별 우선순위 점수가 자동 산출된다.

**40개 Governance & Management Objective의 분포**는 EDM 5, APO 14, BAI 11, DSS 6, MEA 4로 구성되며, 각 Objective는 Purpose -> Practices (Base/Basic/High) -> Inputs/Outputs -> Activities -> Responsible(R)/Accountable(A)/Consulted(C)/Informed(I) RACI의 표준 구조를 가진다. Capability Level은 0~5(PA 1.1~5.2)의 6단계로 측정되며, ISO/IEC 15504 PAM(Process Assessment Model)에 기반한다.

```text
[COBIT 2019 5도메인 + 40 Objectives 구조도]

                    +---------------------------------+
                    |     Stakeholder Needs (VC-Value) |
                    |   • Benefits Realization 30%     |
                    |   • Risk Optimization    25%     |
                    |   • Resource Optimization 25%     |
                    |   • Stakeholder Transparency 20% |
                    +-------------+-------------------+
                                  v
                    +---------------------------------+
                    |   13 Enterprise Goals (EG)       |
                    |  + 13 Alignment Goals (AG)       |
                    +-------------+-------------------+
                                  v
  +--------------------------------------------------------------+
  |                   40 Governance & Management Objectives        |
  +--------------+--------------+--------------+-----------------+
  |   EDM (5)    |   APO (14)   |   BAI (11)   |   DSS (6) + MEA |
  |  (거버넌스)   |  (계획·조직)  |  (구축·구입)  |  (운영) (4)     |
  |              |              |              |                 |
  | EDM01 거버넌스| APO01 관리체계| BAI01 관리프로| DSS01 운영관리  |
  |   Framework  | APO02 전략    |   그램       | DSS02 서비스    |
  | EDM02 Benefit| APO03 엔터프라이| BAI03 관리투자|   요청·사고    |
  |   Delivery   |   아키텍처 EA | BAI04 가용성· | DSS03 문제관리  |
  | EDM03 Risk   | APO04 혁신    |   용량관리   | DSS04 연속성    |
  |   Optimization| APO05 포트폴리오| BAI05 조직변화| DSS05 보안서비스|
  | EDM04 Resrc. | ...           | BAI07 도입·이행| DSS06 비지니스|
  |   Optimizat. | APO08 관계    | BAI08 지식    |   통제         |
  | EDM05 Stake. | APO09 SLA     | BAI09 자산    | MEA01 성과/내부|
  |   Transparen.| APO10 공급자   | BAI10 구성관리| MEA02 내부통제  |
  |              | APO11 품질     | BAI11 프로젝트| MEA03 외부감사  |
  |              |
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 592 / 800

<- **이전**: [591. IT 경영 관리 핵심 토픽 591번 시험 요약](/studynote/12_it_management/05_security_compliance/591_it_management_core_topic_591_exam_summary/)
**다음**: [593. IT 경영 관리 핵심 토픽 593번 시험 요약](/studynote/12_it_management/05_security_compliance/593_it_management_core_topic_593_exam_summary/) ->

---
