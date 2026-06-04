---
title: "781. IT 경영 관리 핵심 토픽 781번 시험 요약 (IT Management Core Topic 781 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019**, **ITIL 4**, **ISO/IEC 38500**, **TOGAF ADM** 등 글로벌 거버넌스 프레임워크를 기반으로, IT 전략-포트폴리오-서비스-리스크-자원을 **가치(Value)** 중심의 통합 거버넌스 체계로 정렬·운영하는 경영학문 영역이다.
> 2. **가치**: ISP(Information Strategy Planning) 기반의 BS(성과)/PI(성과측정) 연동을 통해 IT 투자 ROI를 **연평균 15~25%** 개선하고, IT-비즈니스 정렬도(Strategic Alignment Maturity)를 **Level 1(Ad-hoc)에서 Level 4(Optimized)**로 3단계 향상시키며, COBIT 기반 프로세스 성숙도(Process Capability)를 **Level 2에서 Level 4**까지 도달시켜 거버넌스 비용 대비 컴플라이언스 효율을 **40% 이상** 제고한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **(a) 중앙집중형 COBIT 거버넌스 vs 분산형 페더레이션 거버넌스**, **(b) Waterfall-ISP vs Agile-ISP**, **(c) Build(내부 SI) vs Buy(SaaS) vs Borrow(클라우드)**, **(d) Zero-Base Budgeting vs Incremental Budgeting**의 4대 의사결정 축이며, 조직의 디지털 성숙도(Digital Maturity Level)와 규제 환경(K-ISMS-P, GDPR, DORA)에 따라 최적 거버넌스 모델이 달라진다.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리는 1990년대 후반 **EFFECT(European Framework for Evaluation of IT)**와 **Gartner's IS-LM 모델**을 기점으로 학문적 체계가 정립되었으며, 2000년대 이후 **사이버보안 위협의 고도화**, **클라우드 전환**, **AI 업무 자동화**, **규제 강화**(개인정보보호법, ESG, DORA)로 인해 그 중요성이 비약적으로 증대되었다. 특히 **COVID-19 이후 가속화된 디지털 전환(DX)** 환경에서, 전통적 "Cost Center" 관점의 IT 운영은 "**Value Generator**" 관점으로 전환되었고, IT 거버넌스는 CFO·CDO·CIO가 공동 책임지는 **Board-Level 의사결정 사안**으로 격상되었다.

```text
[ IT 경영 관리 7대 도메인 통합 참조모델 (Integrated IT Governance Reference Model) ]

                        +----------------------------------+
                        |    기업 전략 (Corporate Strategy) |
                        |   - 비전/미션/BSC Balanced Score  |
                        +--------------+-------------------+
                                       | (전략 정렬 Alignment)
            +--------------------------+--------------------------+
            v                          v                          v
   +-----------------+       +-----------------+       +-----------------+
   |  IT 거버넌스    |       |  IT 전략 &      |       | IT 포트폴리오   |
   |  (Governance)   |◄-----►|  거버넌스 체계   |◄-----►|  관리(PfM)      |
   |  - COBIT 2019   |       |  - ISP 방법론   |       | - 응용/인프라/  |
   |  - ISO 38500    |       |  - TOGAF ADM    |       |   투자/프로젝트 |
   |  - 3개역할원칙  |       |  - Ward & Peppard|       | - 5-Tier 분배   |
   +--------+--------+       +---------+-------+       +--------+-------+
            |                          |                         |
            +--------------+-----------+-------------------------+
                           v
   +-----------------------------------------------------------------+
   |                  IT 서비스 운영 및 가치 실현 영역                |
   |  +--------------+ +--------------+ +----------------------+    |
   |  |  ITIL 4 SVS  | | DevOps &    | |  FinOps & 클라우드    |    |
   |  |  - 34 Prac.  | | Agile@Scale | |  경제성 관리          |    |
   |  |  - 4D Model  | | - SAFe/LesS | |  - Showback/Chargeb.  |    |
   |  +------+-------+ +------+------+ +----------+-----------+    |
   |         +----------------+-------------------+                 |
   |                          v                                     |
   |            +------------------------------+                    |
   |            |   IT 리스크 & 컴플라이언스     |                    |
   |            |   - ISO 27001, K-ISMS-P       |                    |
   |            |   - NIST CSF 2.0, DORA        |                    |
   |            |   - 3Lines of Defense (IIA)   |                    |
   |            +------------------------------+                    |
   +-----------------------------------------------------------------+
                                    |
                                    v
                  +------------------------------+
                  |  측정/평가/개선 (MEAL Layer) |
                  |  - KPI/KRI/CSF/BSC          |
                  |  - COBIT Process Capability |
                  |  - CMMI, Balanced Scorecard |
                  +------------------------------+
```

기존 1990년대 방식(예: **Information Engineering(IE)** + **데이터 중심 주먹구구식 SI**)은 시스템 단위 성과에만 집중하여 사일로(Silo) 현상과 이중 투자(Redundancy Investment)를 양산했다. 새로운 패러다임은 **"Strategy->Capability->Process->Technology"** 의 4-계층(Value Chain)을 따라 자원이 가치 흐름(Value Stream)을 따라 흐르도록 설계하며, 이를 위해 **COBIT 2019의 40개 거버넌스/관리 목적(GO/ME)** 과 **ITIL 4의 34개 운영 실무(Practice)** 가 상호 매핑되어 사용된다. 또한 ESG, AI 윤리(AI Act EU), 데이터 주권(데이터 3법) 등 신규 규제는 IT 거버넌스를 **선택이 아닌 필수**로 만들고 있다.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **도시의 도시계획(Master Plan)**과 같다. 건물(시스템) 하나만 잘 짓는 것이 아니라, 상하수도·도로·전력·치안 인프라를 동시에规划设计하고, 시민(사용자)·기업(사업부)·정부(규제기관) 모두가 만족하는 **"살고 싶은 도시"**를 만드는 것이 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 **ISO/IEC 38500 IT 거버넌스 국제표준**이 제시한 **"3개 영역(Evaluate, Direct, Monitor)"** 원칙을 근간으로, **Ward & Peppard(2002)의 IS 전략 수립 프레임워크**와 **COBIT 2019의 Cascade Goals**가 결합된 다층 구조이다.

```text
[ IT 경영 관리 핵심 원리 - Cascade & Value Realization 메커니즘 ]

  +--------------------------------------------------------------------+
  | Layer 1: 거버넌스 결정 (Governance Decision - 3E 원칙 ISO 38500)  |
  |  +----------+  +----------+  +----------+                         |
  |  | EVALUATE |  | DIRECT   |  | MONITOR  |  <- Board/C-Level 결정  |
  |  | (평가)   |-►| (지휘)   |-►| (모니터) |                         |
  |  +----------+  +----------+  +----------+                         |
  |       |             |              |                              |
  |       +-------------+--------------+                              |
  |                     v                                             |
  |        +--------------------------+                               |
  |        | 책임성(RACI) + 3 Lines  |  Principle 2 (Responsibility) |
  |        | of Defense (IIA 모델)   |                               |
  |        +--------------------------+                               |
  +--------------------------------------------------------------------+
                                  |
                                  v
  +--------------------------------------------------------------------+
  | Layer 2: 전략 정렬 (Strategy Alignment - Ward & Peppard)          |
  |                                                                    |
  |  +---------------------+         +----------------------+          |
  |  | 외부 환경 분석      |         | 내부 환경 분석        |          |
  |  | - PESTEL            | ◄-----► | - Value Chain (Porter)|          |
  |  | - Porter 5-Forces   |         | - McKinsey 7S        |          |
  |  | - SWOT, CSF         |         | - Resource Audit     |          |
  |  +---------+-----------+         +----------+-----------+          |
  |            +--------------+-----------------+                     |
  |                           v                                       |
  |            +------------------------------+                       |
  |            | IT 전략 옵션 도출            |                        |
  |            |  1) Exploit (활용)           |                        |
  |            |  2) Expand (확장)            |                        |
  |            |  3) Explore (탐색)           |  <- McKinsey 3Box       |
  |            +--------------+---------------+                       |
  |                           v                                       |
  |            +------------------------------+                       |
  |            |  IT 전략 청사진 (Blueprint)   |                        |
  |            |  - 응용시스템, 데이터,        |                        |
  |            |    인프라, 조직, 거버넌스     |                        |
  |            +------------------------------+                       |
  +--------------------------------------------------------------------+
                                  |
                                  v
  +--------------------------------------------------------------------+
  | Layer 3: 거버넌스 컴포넌트 (COBIT 2019 Cascade)                   |
  |                                                                    |
  |   기업 목표 (13개) --► 정렬 --► IT 관련 목표(13)                  |
  |   IT 관련 목표  -- 정렬 --► Enabler Goals (7개)                  |
  |   Enabler Goals  -- 정렬 --► Governance/Management Obj. (40)     |
  |                                                                    |
  |   Components of Enablers:                                         |
  |    ① Principles, Policies, Frameworks                              |
  |    ② Processes (40 GO/ME, 7 components: EDM/APO/BAI/DSS/MEA)      |
  |    ③ Organizational Structures (Board->SteerCo->IT->User)             |
  |    ④ Information (Data + Information Flows)                       |
  |    ⑤ Services, Infrastructure, Applications                       |
  |    ⑥ People, Skills, Competencies                                 |
  |    ⑦ Culture, Ethics, Behavior                                    |
  +--------------------------------------------------------------------+
                                  |
                                  v
  +--------------------------------------------------------------------+
  | Layer 4: 운영 실무 (ITIL 4 Service Value System)                  |
  |                                                                    |
  |   Opportunity/Demand -► Value -► Co-Creation                      |
  |                                                                    |
  |   ① Guiding Principles (7개) : Focus on value, Start where you are|
  |   ② Governance (Org/Activities)                                   |
  |   ③ Service Value Chain (Plan->Engage->Design->Obtain->Build->Deliver)|
  |   ④ Practices (34개, 3대 영역: General, Service, Mgmt)            |
  |   ⑤ Continual Improvement (CSI Model: 7-Step)                     |
  +--------------------------------------------------------------------+
                                  |
                                  v
  +--------------------------------------------------------------------+
  | Layer 5: 측정 및 개선 (Measurement & Improvement Layer)           |
  |                                                                    |
  |   +--------------+  +--------------+  +--------------------+      |
  |   | KPI/CSF/PI  |  | CMMI/OPM3    |  | PRM (Performance   |      |
  |   | (BSC 4관점)  |  | Maturity 5Lv |  | Reference Model)   |      |
  |   +--------------+  +--------------+  +--------------------+      |
  |                                                                    |
  |   COBIT Process Capability (0~5, ISO/IEC 33020 PAM)              |
  |   - LV0 Incomplete -> LV1 Performed -> LV2 Managed                 |
  |   - LV3 Defined -> LV4 Quantitatively Managed -> LV5 Optimizing    |
  +--------------------------------------------------------------------+
```

### 핵심 아키텍처의 수학적/논리적 모델

**① IT 가치 실현 공식 (Value Realization Equation)** - Ward & Peppard 기반
```
IT Value = Σ (Benefit_realized) - Σ (Cost_IT + Cost_Risk) ± Σ (Option_Value)

여기서:
- Benefit_realized  : 정량적/정성적 비즈니스 이득 (예: 매출 1%^, 비용 5%v)
- Cost_IT           : TCO (Total Cost of Ownership) - HW+SW+인력+교육+운영
- Cost_Risk         : 리스크 발생 시 예상 손실 × 발생 확률
- Option_Value      : 미래 사업기회 옵션 (Black-Scholes 기반, Δ값 적용 가능)
```

**② IT 정렬도 측정 모델 (Strategic Alignment Maturity Model - SAMM, Luftman 2001)**
6개 정렬 요소의 성숙도 1~5 단계 점수 평균:
```
Alignment Score = Avg(Communication, Competency, Governance, Partnership,
                       Scope&Architecture, Skills) ∈ [1.0, 5.0]
- LV1 Ad-hoc / Initial
- LV2 Committed / Planned
- LV3 Established / Implemented
- LV4 Managed / Measurable
- LV5 Optimized / Continuous
```

**③ COBIT 2019 7대 컴포넌트와 40개 목적의 정렬**
| Governance Objectives (5) | Management Objectives (35) | 영역 (Domain) |
|:---|:---|:---|
| EDM01 Ensured Governance Framework | APO, BAI, DSS, MEA 전체 (35) | Evaluate, Direct, Monitor |
| EDM02 Benefits Delivery | | |
| EDM03 Risk Optimization | | |
| EDM04 Resource Optimization | | |
| EDM05 Stakeholder Transparency | | |

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **ISO/IEC 38500** | IT 거버넌스 최상위 원칙(Principle) 표준 | **3E(3 Principles)**: 책임성(Responsibility), 전략(Strategy), 획득(Acquisition), 성과(Performance), 준거(Conformance), 인적행태(Human Behavior) 6대 원칙을 **Board-Level 정책**으로 구현. ISO/IEC 38505(데이터 거버넌스), 38507(AI 거버넌스)와 연계 |
| **COBIT 2019** | 거버넌스-관리 목적 통합 프레임워크 | 40개 GO/ME(Governance/Management Objectives), **7개 Enablers**, **Cascade Goals**(13->13->40), **Focus Area**(예: DevOps, RPA, Cybersecurity) 커스터
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 781 / 800

<- **이전**: [780. IT 경영 관리 핵심 토픽 780번 시험 요약](/studynote/12_it_management/05_security_compliance/780_it_management_core_topic_780_exam_summary/)
**다음**: [782. IT 경영 관리 핵심 토픽 782번 시험 요약](/studynote/12_it_management/05_security_compliance/782_it_management_core_topic_782_exam_summary/) ->

---
