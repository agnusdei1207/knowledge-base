---
title: "604. IT 경영 관리 핵심 토픽 604번 시험 요약 (IT Management Core Topic 604 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


# 604. IT 거버넌스 프레임워크 및 디지털 전환 전략 (IT Governance Framework & Digital Transformation Strategy)

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 COBIT 2019의 5개 도메인(EDM/APO/BAI/DSS/MEA)과 ISO/IEC 38500의 6원칙(책임·전략·수행·적합성·규율·인간적 행동)을 기반으로, IT가 비즈니스 가치(ROI, NPV, EVA)를 극대화하도록 의사결정·통제 구조를 설계하는 것이다.
> 2. **가치**: McKinsey(2023) 조사에서 성숙한 IT 거버넌스 체계 보유 기업은 디지털 전환 성공률이 67%, Time-to-Market 40% 단축, IT 투자 대비 수익률(ROIT) 평균 2.3배 향상을 달성한다.
> 3. **판단 포인트**: 중앙집중형(Federated) vs 분산형(Decentralized) 거버넌스 모델 선택 시, 조직 규모·규제 강도·문화적 성숙도를 기준으로 결정하며, COBIT 2019의 Focus Area(예: DevOps, Risk, Cybersecurity)와 Design Factor 11종을 활용한 맞춤형 설계가 핵심이다.

---

## Ⅰ. 개요 및 필요성

전통적인 IT 관리는 "시스템 가용성 99.9% 유지"라는 운영 KPI에 머물렀으나, 4차 산업혁명·클라우드·AI 도입으로 인해 **"IT가 어떻게 사업 전략을驱动(구동)하고 Risk-Return 균형을 맞추는가"**라는 거버넌스 질문이 핵심 화두로 부상했다. ISO/IEC 38500:2015의 등장, COBIT 2019의 설계因子(Design Factor) 도입, 그리고 EU DORA·한국 클라우드 보안인증(CSAP) 등 규제가 강제되면서 단순히 "ISO 27001 인증 보유" 수준을 넘어 **Value Creation 중심의 통합 거버넌스 체계**가 요구된다.

특히 한국 정보관리기술사 시험에서 604번 토픽은 △IT 전략 기획 △거버넌스 프레임워크 비교·설계 △디지털 전환(DX) 로드맵 △성과 측정(BSC, KPI cascade) △규제 준수(컴플라이언스) △IT 투자 평가(NPV, TCO, ROI) 등을 통합적으로 다루며, 단순 암기가 아닌 **"왜(Why)·무엇을(What)·어떻게(How)"**의 판단력을 평가한다.

```text
+-------------------------------------------------------------+
|           Digital Transformation Pressure (2020~)          |
|   +--------------+   +--------------+   +--------------+  |
|   |  Customer    |   |  Regulatory  |   |   Cost/Agile |  |
|   |   Expect.    |   |  (DORA/CSAP) |   |   Pressure   |  |
|   +------+-------+   +------+-------+   +------+-------+  |
|          |                  |                  |          |
|          +------------------+------------------+          |
|                             v                             |
|         +------------------------------------+            |
|         |   IT Governance Framework 필요성   |            |
|         |  (단순 ITIL 운영 -> 가치 지향 통합) |            |
|         +----------------+-------------------+            |
|                          v                                 |
|   +--------------------------------------------------+    |
|   |        3-Layer Governance Architecture            |    |
|   |  +------------------------------------------+    |    |
|   |  | Layer 1: Strategic (Board/Steering Cmte)  |    |    |
|   |  |  - IT Strategy, Risk Appetite, Portfolio  |    |    |
|   |  +------------------------------------------+    |    |
|   |  | Layer 2: Tactical (IT Steering / PMO)     |    |    |
|   |  |  - COBIT EDM/APO, Architecture Decision  |    |    |
|   |  +------------------------------------------+    |    |
|   |  | Layer 3: Operational (Service Mgmt)      |    |    |
|   |  |  - ITIL 4 Practices, DevOps, SLA/Monitor |    |    |    |
|   |  +------------------------------------------+    |    |
|   +--------------------------------------------------+    |
+-------------------------------------------------------------+
```

기존(2000년대 초)에는 **"IT는 비용센터"**라는 인식 하에, 감리(Inspection)·컴플라이언스 중심의 사후 통제가 주를 이루었다. 그러나 2010년대 후반 이후 클라우드·SaaS·AI가 보편화되고, 비즈니스 사이클이 월 단위 -> 일 단위로 단축됨에 따라 **"IT는 Value Driver"**라는 인식 전환이 일어났고, 이는 △Agile 거버넌스 △Product-centric 조직 △BizDevOps 협업 구조로 진화했다. 기술사 시험에서는 이 패러다임 전환을 명확히 이해하고, "왜 전통적 ITIL-only 거버넌스는 한계가 있는가"를 비교 설명할 수 있어야 한다.

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **"배의 키(舵) 잡는 시스템"**과 같다. 돛(기술)·바람(데이터)·선원(인재)이 아무리 좋아도, 키(거버넌스)가 없으면 배는 표류하고, 너무 뻣뻣하면 폭풍(변화)에 부서진다. 목적지(사업 목표)·바람 방향(시장)·해류(규제)를 종합해 **균형 잡힌 키 잡기**가 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019는 **Governance & Management Objectives**를 40개로 정의하고, 이를 5개 도메인(EDM, APO, BAI, DSS, MEA)으로 분류한다. 여기에 ISO/IEC 38500의 **6 Principles**와 ITIL 4의 **34 Practices**, 그리고 ISO 27001·NIST CSF가 수평적으로 연계된다. **핵심 메커니즘**은 ①목표 계단식 정렬(Cascade) -> ②설계 인자(Design Factor)로 거버넌스 시스템 맞춤 설계 -> ③중요 목표(Importance Goal)와 성능 측정(Performance Metric) -> ④PDCA 사이클 통합이다.

```text
        +---------------------------------------------+
        |      COBIT 2019 + ISO 38500 + ITIL 4        |
        |         Integrated Governance Stack          |
        +---------------------------------------------+
                                |
        +-----------------------+-----------------------+
        v                       v                       v
   +---------+           +----------+            +----------+
   |  ISO    |           |  COBIT   |            |  ITIL 4  |
   | 38500   |           |  2019    |            |          |
   | 6원칙   |           | 5도메인  |            | 34 Prac. |
   |         |           | 40목표   |            |          |
   | - 책임  |           | - EDM(5) |            | - 일반  |
   | - 전략  |           | - APO(14)|            | - 서비스|
   | - 수행  |           | - BAI(11)|            | - 기술  |
   | - 적합  |           | - DSS(6) |            |          |
   | - 규율  |           | - MEA(4) |            |          |
   | - 인간  |           |          |            |          |
   +----+----+           +----+-----+            +----+-----+
        |                     |                       |
        +--------------+------+-----------+-----------+
                       v                  v
        +------------------+   +------------------+
        | Governance System |   |  Component: 7    |
        | Design Factors    |   |  (Process/Org/   |
        |  (11 Factors)     |   |   Info/Flow/     |
        |                   |   |   People/Skill/  |
        |  DF1 Strategy     |   |   Infrastructure)|
        |  DF2 Goals        |   +------------------+
        |  DF3 Risk Profile |            |
        |  ...              |            v
        |  DF11 Threat      |   +------------------+
        +------------------+   | Goals Cascade    |
                               | Stakeholder ->    |
                               | Enterprise ->     |
                               | IT -> Service     |
                               +------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Governance System (거버넌스 체계)** | 의사결정·통제·감시 구조의 총칭 | COBIT 2019의 Design Factor 11종(전략·목표·위험·컴플라이언스·IT 이슈·역할·정보·문화·기술·산업·지형)을 입력으로, 40개 Governance Objective의 우선순위·적용 범위·측정 지표를 동적으로 도출 |
| **Components (7대 구성요소)** | 거버넌스 시스템의 실행 단위 | ①Process(40개 목표의 RACI), ②Organizational Structures(Steer/Co./Oper. 분리), ③Information Flows(보고 체계), ④People·Skills·Competencies(역량 매트릭스), ⑤Policies·Procedures(정책 계층), ⑥Culture·Ethics·Behavior(리더십 메시지), ⑦Services·Infrastructure·Applications(지원 시스템) |
| **Goals Cascade (목표 계단식)** | 이해관계자 Needs -> IT 서비스로 변환 | 13개 Stakeholder Needs -> 13개 Enterprise Goals -> 13개 Alignment Goals -> 13개 IT-related Goals로 매핑. Balanced Scorecard 4관점(Financial/Customer/Internal/Learning)과 직접 연계 |
| **Focus Areas (집중 영역)** | 거버넌스의 우선순위 주제 | COBIT 2019은 11개 FA 제공(DevOps, Cybersecurity, Risk, Privacy, Digital Transformation, 등). 각 FA는 ①Issue·Risk -> ②Target Capability Level -> ③Selected Practices로 구성 |
| **Performance Management** | 성숙도·성과 측정 | CMMI 5단계 + ISO 15504 프로세스 능력 모델. **Process Capability Level(0~5)**과 **Service Capability Level**을 분리 측정, 각 Goal별 Metric(Numeric/Perceived/Fulfillment) 부여 |
| **Regulatory Compliance Hook** | 규제 준수 통합 엔진 | EU DORA, 한국 전자금융감독규정, ISMS-P, CSAP, PCI-DSS 등의 통제항목을 COBIT의 MEA(Monitor/Evaluate/Assess) 도메인에 매핑·자동 검증 |

### 핵심 알고리즘: Design Factor 기반 거버넌스 우선순위 산정

COBIT 2019는 11개 Design Factor의
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 604 / 800

<- **이전**: [603. IT 경영 관리 핵심 토픽 603번 시험 요약](/studynote/12_it_management/05_security_compliance/603_it_management_core_topic_603_exam_summary/)
**다음**: [605. IT 경영 관리 핵심 토픽 605번 시험 요약](/studynote/12_it_management/05_security_compliance/605_it_management_core_topic_605_exam_summary/) ->

---
