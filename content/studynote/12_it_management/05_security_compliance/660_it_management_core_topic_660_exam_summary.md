+++
title = "660. IT 경영 관리 핵심 토픽 660번 시험 요약 (IT Management Core Topic 660 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# 660. IT 경영 관리 핵심 토픽 — 정보시스템 거버넌스 및 전략 계획 (IT Governance & Strategic Planning)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 COBIT 2019, ITIL 4, ISO 38500 프레임워크를 기반으로 **전략-평가-지휘-감시(Monitor-Evaluate-Direct-Monitor)** 의 5원칙을 통해 IT가 비즈니스 목표(Strategy)와 정렬(Alignment)되어 가치를 창출하도록 통제하는 체계이며, 정보시스템 감사를 통해 이를 검증·확보한다.
> 2. **가치**: 효과적인 IT 거버넌스 도입 시 **프로젝트 성공률 약 35% 향상**(PMI 2021), **TCO 20~30% 절감**, **이해관계자 만족도(CSF/KPI) 40% 이상 개선** 효과를 기대할 수 있으며, ISO 38500 인증 기업은 평균 17% 더 높은 ROIT(Return on IT Investment)을 달성한다(ISO Survey 2022).
> 3. **판단 포인트**: 중앙집중형(Centralized) vs 분산형(Decentralized) 거버넌스 모델, COBIT의 40개 관리 목표 중 어떤 것을 우선순위로 채택할지, RACI 매트릭스의 책임·조율 역할 경계, 그리고 Balanced ScoreCard(BSC) 4관점(재무/고객/내부/학습성장) 지표 간 인과관계 모델링이 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX, Digital Transformation) 가속화로 인해 IT는 더 이상 단순한 **지원 기능(Back-office)** 이 아니라 **사업의 핵심 동력(Core Business Driver)** 으로 자리매김했다. 그러나 Forbes(2022)에 따르면 글로벌 기업의 **70%가 디지털 이니셔티브의 성과를 충분히 거두지 못하고 있으며**, 그 원인 중 41%가 **거버넌스 부재**로 분석된다( McKinsey, 2023). 이에 정보관리기술사 Topic 660에서는 **IT 전략 수립 -> 거버넌스 프레임워크 설계 -> 성과 측정 -> 감사 및 개선**으로 이어지는 End-to-End IT 경영 관리 역량을 평가한다.

기존 IT 관리(Traditional IT Management)는 **사일로(Silo) 단위**로 각 부서가 독립적으로 시스템을 운영했으며, CAPEX(자본적 지출) 중심의 **프로젝트 단위 ROI** 만을 평가했다. 반면 현대 IT 거버넌스는 **엔터프라이즈 아키텍처(EA)**, **포트폴리오 관리(PPM)**, **Value Stream 기반의 Agile-Waterfall 하이브리드**, **데이터 드리븐 의사결정** 패러다임으로 전환되었다.

```text
+----------------------------------------------------------------------+
|              Topic 660: IT 경영 관리 핵심 프레임워크 맵                  |
+----------------------------------------------------------------------+
|                                                                      |
|   [Business Strategy]                                                |
|         |                                                            |
|         v                                                            |
|   +----------------+         +------------------+                   |
|   | IT 거버넌스     |<--------->|  IT 전략 기획     |                   |
|   | (Governance)   |         |  (Strategic Plan) |                   |
|   | - COBIT 2019   |         | - SWOT/TOWS       |                   |
|   | - ISO 38500    |         | - BSC 4관점       |                   |
|   +--------+-------+         +--------+---------+                   |
|            |                          |                              |
|            v                          v                              |
|   +----------------+         +------------------+                   |
|   | IT 운영관리     |<--------->|  IT 성과/감사    |                   |
|   | (ITIL 4)       |         |  (Audit)          |                   |
|   | - Service Value |         | - IS Audit        |                   |
|   | - 34 Practices  |         | - COBIT Assurance |                   |
|   +--------+-------+         +--------+---------+                   |
|            |                          |                              |
|            +------------+-------------+                              |
|                         v                                            |
|              +---------------------+                                 |
|              | Continuous Improvement|                              |
|              |  (PDCA + Kaizen)      |                              |
|              +---------------------+                                 |
+----------------------------------------------------------------------+
```

기존 패러다임과 비교하면 다음과 같은 차이가 존재한다.

| 구분 | 전통적 IT 관리(Old) | 현대 IT 거버넌스(New) |
|:-----|:--------------------|:---------------------|
| 관점 | 비용(Cost) 중심 | 가치(Value) 중심 |
| 구조 | 기능별 사일로 | 엔터프라이즈 통합(EA) |
| 의사결정 | CIO 독단적 | 이사회-경영진-IT 3자 협업(ISO 38500) |
| 측정 | ROI(재무적) | BSC 4관점 + 비재무 KPI |
| 리스크 | 사후 대응 | GRC(Governance-Risk-Compliance) 선제적 |
| 변화관리 | 폭포수(Waterfall) | Agile + DevOps + BizDevOps |

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **도시의 종합 계획법**과 같다. 건물(시스템) 하나하나 짓는 것은 개별 개발이지만, 어디에 도로를 내고, 공원을 배치하고, 교통 신호를 관리하는 것은 **도시 전체의 거버넌스**다. IT 거버넌스는 이 '도시 계획도'에 해당한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) ISO 38500 — IT 거버넌스의 국제 표준

ISO/IEC 38500:2015 는 IT 거버넌스의 **근간 표준(Foundation Standard)** 으로, 이사회(Board)가 IT 활용을 **감독(Direct)**·**평가(Evaluate)**·**모니터링(Monitor)** 해야 함을 명시한다.

```text
[ISO 38500 - 3개 영역 / 6원칙 / 5단계 의사결정 모델]

   +-------------------------------------------------------+
   |                    THE BOARD / 이사회                    |
   |              (최종 의사결정 및 책임)                       |
   +------------------------+------------------------------+
                            |
   +--------------+---------+---------+----------------+
   | 1. 책임원칙    |  2. 전략원칙       |  3. 획득원칙     |
   | (Responsibility)| (Strategy)        | (Acquisition)  |
   | 4. 성과원칙    |  5. 적합성원칙     |  6. 인간행위원칙  |
   | (Performance)  | (Conformance)     | (Human Behavior)|
   +--------------+---------+---------+----------------+
                            |
   +--------------+---------+---------+----------------+
   |   Plan       |      Do           |      Check      |
   | (계획)        |    (이행)          |    (검토)        |
   +--------------+---------+---------+----------------+
                            |
   +------------------------+------------------------------+
   |            Act  -->  Monitor  -->  Evaluate              |
   |            (개선)     (모니터링)     (평가)               |
   +-------------------------------------------------------+
```

### 2) COBIT 2019 — 40개 관리목표 체계

COBIT(Control Objectives for Information and Related Technologies) 은 ISACA에서 관리하는 **엔터프라이즈 IT 거버넌스·관리 프레임워크**다. COBIT 2019는 5개 도메인(EDM: Evaluate-Direct-Monitor, APO: Align-Plan-Organize, BAI: Build-Acquire-Implement, DSS: Deliver-Service-Support, MEA: Monitor-Evaluate-Assess) 아래 **40개의 관리목표(Management Objective)** 로 구성된다.

```text
[COBIT 2019 - 5 Domain × 40 Management Objectives 계층]

   +---------------------------------------------------------+
   |         EDM(05) - 거버넌스 (Evaluate/Direct/Monitor)     |
   |   EDM01 거버넌스 프레임워크 설정/유지                    |
   |   EDM02 혜택 실현 관리 / EDM03 리스크 최적화              |
   |   EDM04 리소스 최적화 / EDM05 이해관계자 투명성            |
   +--------------------+------------------------------------+
                        v
   +---------------------------------------------------------+
   |         APO(14) - 관리 (Align/Plan/Organize)            |
   |   APO01~APO14 (전략, 포트폴리오, 아키텍처, 혁신, 인적…)  |
   +--------------------+------------------------------------+
                        v
   +---------------------------------------------------------+
   |     BAI(11)  - Build / Acquire / Implement              |
   |   BAI01~BAI11 (솔루션, 변화, 배포, 전환, 수용성…)        |
   +--------------------+------------------------------------+
                        v
   +---------------------------------------------------------+
   |     DSS(06)  - Deliver / Service / Support              |
   |   DSS01~DSS06 (운영, 서비스 요청, 인시던트, 보안연속성…) |
   +--------------------+------------------------------------+
                        v
   +---------------------------------------------------------+
   |     MEA(04)  - Monitor / Evaluate / Assess             |
   |   MEA01~MEA04 (성과/내부통제/외부/준수)                  |
   +---------------------------------------------------------+
```

### 3) ITIL 4 — 서비스 가치 체계(SVS, Service Value System)

ITIL 4는 **34개의 관리 실무(Practice)** 와 **SVS(Service Value System)** 를 통해 IT 서비스의 End-to-End 가치를 관리한다. 핵심은 **Value Stream**(가치 흐름)을 통해 Opportunity/Demand를 Value로 변환하는 것이다.

```text
[ITIL 4 SVS - Service Value Chain (핵심 활동)]

  Plan -> Engage -> Design & Transition -> Obtain/Build ->
  Deliver & Support -> Improve
       |                                              |
       +------------ (Feedback Loop) ----------------+
                       ^                              |
                  Guiding Principles <----------------+
                  (Focus on Value, Start Where You Are,
                   Progress Iteratively, Collaborate,
                   Think & Work Holistically, Keep It Simple,
                   Optimize & Automate)
```

### 4) 핵심 프레임워크 4종 비교

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:----------|:-----|:---------------------|
| **COBIT 2019** | IT 거버넌스·관리 **프레임워크** | 5도메인·40관리목표·감사가능 통제목표. Design Factors(10개)와 Focus Area로 기업이 자사 환경에 맞게 커스터마이징 |
| **ISO 38500** | IT 거버넌스 **원칙 표준** | 이사회의 Direct·Monitor·Evaluate 의무. 6대 원칙(책임·전략·획득·성과·적합성·인간행위) 기반 |
| **ITIL 4** | IT **서비스 관리**(ITSM) | 34개 Practice + Service Value Chain. Incident, Change, Problem, Service Desk 등 운영 실무 |
| **ISO 27001/27002** | **정보보호** 경영체계(ISMS) | Plan-Do-Check-Act 기반 93개 통제 항목(Annex A 2022). 위험평가(Risk Treatment) 기반 |
| **BSC(균형성과표)** | 전략 -> KPI **연결 도구** | 4관점(재무·고객·내부프로세스·학습성장) 인과관계. 전략맵(Strategy Map)으로 시각화 |
| **RACI Matrix** | 역할·책임 **분배 매트릭스** | Responsible(집행), Accountable(책임), Consulted(자문), Informed(통보) — 4글자 매트릭스 |
| **EA(TOGAF)** | **엔터프라이즈 아키텍처** | ADM(Architecture Development Method) 8단계 Phase — Preliminary->A(비전)->B(비즈)->C(앱/데이터)->D(기술)->E(기회)->F(계획)->G(거버넌스)->H(변화관리) |

#### 핵심 공식 및 평가 모델

**① COBIT 2019 Capability/Maturity 산정**: Process Assessment Model (PAM) 은 5단계로 평가한다.
- Level 0: Incomplete / Level 1: Initial / Level 2: Managed / Level 3: Defined / Level 4: Quantitatively Managed / Level 5: Optimizing
- 핵심 산식: `Capability Level = Σ(PA: Process Attribute 점수[0~100]) ÷ 7` (PA 2.1~2.7)

**② BSC 인과관계 인덱스**: 전략목표는 4관점 간 **인과 사슬(Driver -> Outcome)** 로 연결되며, 보통 **Lead Indicator(선행지표)** 와 **Lag Indicator(결과지표)** 의 비율을 4:6 정도로 구성한다(Kaplan & Norton, 1996).

**③ TCO(Total Cost of Ownership) 산정**: TCO = 직접비(하드웨어·소프트웨어 라이선스) + 간접비(운영·유지보수·교육·다운타임 손실). 일반적으로 직접비 대비 간접비가 **3~5배** 높음(Gartner, 2019).

**④ ISO 38500 RACI 기본 매트릭스** (예: CIO-이사회-IT위원회-내부감사):
- 거버넌스 의사결정: **A**(이사회) / **R**(CIO) / **C**(외부자문) / **I**(전사 임직원)

- **📢 섹션 요약 비유**: ISO 38500은 **헌법**, COBIT 2019는 **행정 절차법**, ITIL 4는 **민원 처리 매뉴얼**, BSC는 **성과 평가표**에 비유할 수 있다. 정보관리기술사는 이 4종을 동시에 이해하고 적절히 조합할 수 있어야 한다.

---

## Ⅲ. 비교 및 연결

### 1) 프레임워크 간 비교

| 구분 | COBIT 2019 | ITIL 4 | ISO 38500 | ISO 27001 |
|:-----|:-----------|:-------|:----------|:----------|
| **적용 범위** | 거버넌스 + 관리 | 서비스 운영 관리 | 거버넌스 원칙 | 정보보호 |
| **구조** | 5도메인/40목표 | 34 Practice | 6원칙 | Annex A 통제항목 |
| **대상** | 전사 IT 전부담당 | 서비스 운영팀 | 이사회/경영진 | CISO/ISMS 담당자 |
| **감사 적합성** | ◎ (IS감사 표준) | △ | ○ | ◎ |
| **측정 방식** | PAM 0~5 Level | KPI/SLA | 6원칙 점검 | Statement of Applicability |
| **인증 가능** | Yes (Certified) | Yes (Foundation/Master) | No (원칙 제시) | Yes (ISMS 인증) |
| **연계 표준** | ITIL, ISO 27001, TOGAF | COBIT, SIAM, DevOps | COBIT, ISO 37000 (거버넌스 일반) | COBIT 2019(DSS06) |
| **DX/클라우드 대응** | ◎ (Cloud Focus Area 추가) | ◎ (Digital/IT 4.0 반영) | △ | △ (2022 보완) |
| **한국 활용도** | 매우 높음 (감사용) | 높음 (관공서/대기업) | 보통 (원칙) | 매우 높음 (PIMS 인증) |

### 2) 다른 시스템/도구와의 연결

```text
[Topic 660 IT 거버넌스 생태계 통합 아키텍처]

        +--------------------------------------+
        |
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 660 / 800

<- **이전**: [659. IT 경영 관리 핵심 토픽 659번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/659_it_management_core_topic_659_exam_summary/)
**다음**: [661. IT 경영 관리 핵심 토픽 661번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/661_it_management_core_topic_661_exam_summary/) ->

---
