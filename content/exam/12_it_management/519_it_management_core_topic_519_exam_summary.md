---
title: "IT Management Core Topic 519 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 **COBIT 2019(40개 거버넌스/관리 목적), ISO/IEC 38500(6원칙), ITIL 4(34개 Practice)** 프레임워크를 통해 기업의 IT 의사결정·책임·통제 체계를 수립하는 것이며, 핵심은 **"Value Governance"** 관점에서 **EDM( Evaluate, Direct, Monitor)** 사이클을 구현하는 것이다.
> 2. **가치**: 글로벌 기업 기준 IT 거버넌스成熟도(Level 3->5) 향상 시 **IT 투자 ROI 약 23% -> 41% 개선**(ISACA, 2023), **프로젝트 실패율 40% -> 12% 감소**, **컴플라이언스 위반 비용 평균 USD 4.45M -> USD 1.2M 절감**(IBM Cost of Data Breach Report 기준)이라는 정량적 효과를 창출한다.
> 3. **판단 포인트**: 중앙집중형(Centralized)·분산형(Decentralized)·연합형(Federated)·하이브리드형(Hybrid) 조직 모델 중 **Business-IT Alignment Maturity(Gartner 5단계)** 와 **Enterprise Architecture 성숙도**에 따라 선택하며, **클라우드 전환(FinOps, 3-15% 클라우드 비용 회수)** 과 **AI 거버넌스(EU AI Act Risk-based Tier)** 가 새로운 의사결정 변수가 되었다.

---

## Ⅰ. 개요 및 필요성

정보관리 기술사 시험에서 IT 경영 관리 영역은 단순한 "IT 관리"를 넘어 **"IT가 어떻게 기업 가치를 창출하고 위험을 통제하는가"** 에 대한 체계적 프레임워크를 요구한다. 특히 4차 산업혁명 이후 **DX(Digital Transformation)**, **AI 윤리**, **ESG**, **공급망 보안** 등 새로운 거버넌스 요구사항이 폭증하면서, 전통적인 ITIL/COBIT만으로는 한계가 있어 **"통합 거버넌스(Integrated Governance)"** 패러다임으로 진화하고 있다.

기존 IT 관리는 **"시스템 가용성"** 중심(SLA 99.9% 달성, MTTR 최소화)이었으나, 현재의 IT 경영은 **"비즈니스 Outcomes"** 중심(매출 기여도, 고객 경험 지수 NPS, Time-to-Market 단축, ESG 점수)으로 패러임이 전환되었다. Gartner(2024) 보고서에 따르면 **CEOs의 89%가 "IT는 핵심 사업 자산"** 이라고 응답하며, **CDO(Chief Digital Officer)·CIO·CISO·CDO+CAIO** 등 C-Level 역할 분화도 가속화되었다.

```text
[ IT 경영 관리 패러다임 진화도 ]

+----------------------------------------------------------------------+
|  1980s-1990s       2000s              2010s              2020s~       |
|  +---------+     +---------+       +---------+       +----------+  |
|  | 데이터   | --> | 정보     | -->  | 지식     | -->  | 지혜/     |  |
|  | 처리     |     | 관리     |       | 경영     |       | 가치경영  |  |
|  | (EDP)   |     | (MIS)   |       | (KMS)   |       | (Value)  |  |
|  +---------+     +---------+       +---------+       +----------+  |
|       |              |                  |                 |         |
|    Cost Center   Service Provider  Strategic       Business        |
|                                            Enabler   Value Driver   |
|                                                                      |
|  [핵심 전환 축]                                                       |
|  • Technology Push --------------------------> Business Pull         |
|  • CapEx 중심  ------------------------------> OpEx/Value 기반       |
|  • 단일 시스템  ------------------------------> 생태계(Platform)     |
|  • 내부 통제   ------------------------------> 외부 컴플라이언스+ESG  |
+----------------------------------------------------------------------+
```

**왜 IT 경영 관리가 필수적인가?** 다음 5가지 핵심 동인이 존재한다:
1. **규제 환경 복잡화**: GDPR(€20M 또는 매출 4%), 개인정보보호법(과징금 5%), EU AI Act(€35M 또는 7%), 클라우드 보안인증(CSAP) 등 다중 규제 동시 준수
2. **사이버 위협 고도화**: 랜섬웨어 피해 평균 복구비용 **USD 1.85M**(2023, Sophos), APT 공격 시 평균 **287일 잠복**(Mandiant)
3. **IT 투자 효율성 요구**: 글로벌 IT 지출 **USD 5.1T(2024, Gartner)** 중 약 **30%가 실패/저효율** 투자로 추정
4. **이해관계자 다변화**: 주주, 고객, 임직원, 감독기관, 협력사 등 **"Stakeholder Capitalism"** 시대
5. **기술 융합 가속**: AI·클라우드·블록체인·양자컴퓨팅이 동시에 의사결정에 영향 -> **"Decision Velocity"** 요구

- **📢 섹션 요약 비유**: IT 경영 관리는 **"배의 키잡이"** 와 같습니다. 파도(기술 변화, 규제, 시장)는 끊임없이 거세지고, 선박(기업)의 화물(데이터·비즈니스)을 안전한 항구(가치 창출)로 이끌기 위해서는 **나침반(프레임워크), 해도(아키텍처), 배의 상태 점검(감사)** 이 모두 갖춰져야 합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 **3-Layer Governance Model**(거버넌스-관리-운영)과 **4-Pillar Framework**(전략·조직·프로세스·기술)로 구성된다. 가장 널리 쓰이는 참조 모델은 **COBIT 2019 + ISO 38500 + ITIL 4 + ISO 27001 + TOGAF** 의 **"Integrated Governance Framework"** 이다.

```text
[ IT 경영 관리 통합 거버넌스 아키텍처 ]

                    +------------------------------------+
                    |  Stakeholders                      |
                    |  (Board, CEO, Regulator, Customer) |
                    +--------------+---------------------+
                                   | Accountability
                                   v
        +--------------------------------------------------+
        |  L1: GOVERNANCE LAYER (거버넌스 계층)              |
        |  - ISO 38500 6 Principles (Responsibility,       |
        |    Strategy, Acquisition, Performance,           |
        |    Conformance, Human Behavior)                  |
        |  - COBIT 2019 EDM: Evaluate-Direct-Monitor      |
        |  - Board IT Committee + Steering Committee       |
        +----------------------+---------------------------+
                               | Direction
                               v
        +--------------------------------------------------+
        |  L2: MANAGEMENT LAYER (관리 계층)                 |
        |  - COBIT 2019: 40 Governance/Management Obj.    |
        |    · EDM(5), APO(14), BAI(11), DSS(6), MEA(4)   |
        |  - ITIL 4 Service Value System (SVS)             |
        |    · Opportunity/Demand/Value                     |
        |  - PMBOK 7 / PRINCE2 / Agile(Scrum, SAFe 6.0)   |
        |  - EA: TOGAF ADM(8 Phase), Zachman 6x6          |
        +----------------------+---------------------------+
                               | Operation
                               v
        +--------------------------------------------------+
        |  L3: OPERATION LAYER (운영 계층)                  |
        |  - ITIL 4: 34 Practices (Change, Incident,       |
        |    Problem, Service Desk, Monitoring, etc.)      |
        |  - DevOps/Platform Engineering/GitOps            |
        |  - Observability (Prometheus+Grafana+ELK+Loki)  |
        |  - SRE: SLO/SLI/SLI, Error Budget                |
        +--------------------------------------------------+
                                   |
                                   v
                    +------------------------------------+
                    |  Cross-cutting Concerns            |
                    |  - Security: ISMS/ISO 27001         |
                    |  - Privacy: PIMS/ISO 27701          |
                    |  - Risk: ISO 31000                 |
                    |  - BCM: ISO 22301                  |
                    |  - AI Ethics: NIST AI RMF, EU AI Act|
                    +------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **ISO/IEC 38500** | IT 거버넌스 최상위 국제표준 | 6원칙(책임, 전략, 획득, 성과, 적합, 인간행동) 기반 **"Governance-Management-Operational" 3계층 분리**; **"Direct, Evaluate, Monitor"** 의 **PDCA-EDM** 사이클 적용 |
| **COBIT 2019** | IT 거버넌스·관리 목적 체계 | **40개 Governance/Management Objective**(EDM 5, APO 14, BAI 11, DSS 6, MEA 4)와 **7개 컴포넌트(원리, 정책, 구조, 프로세스, 정보, 인력, 역량)** 의 **"Components-Model"** 5단계 능력평가(0-5) |
| **ITIL 4** | IT 서비스 관리 프레임워크 | **Service Value System(SVS)**: Opportunity->Demand->Value 흐름; **34개 Practice** (General Mgmt 14, Service Mgmt 17, Technical Mgmt 3); **"4 Dimension Model"**(조직/정보/파트너/가치흐름/기술); **"Guiding Principles"** 7개(Focus on value, Start where you are, etc.) |
| **TOGAF ADM** | Enterprise Architecture 개발 방법론 | **Architecture Development Method 8 Phase**(Preliminary->A:비전->B:비즈니스->C:정보시스템->D:기술->E:기회->F:마이그레이션->G:구현관리->H:변경관리); **ADM Cycle 반복(Iteration)** 과 **Architecture Repository(ABB, AS-IS, TO-BE, Gap)** |
| **PMBOK 7 / PRINCE2 / SAFe** | 프로젝트/프로그램/포트폴리오 관리 | **PMBOK 7**: 12 Project Management Principle + 8 Performance Domain; **PRINCE2**: 7 Principle(Continued Business Justification, Learn from Experience, Defined Roles, Manage by Stages, Manage by Exception, Focus on Products, Tailor to Suit); **SAFe 6.0**: Essential/Lean/Large/Full 4 Config, PI Planning, ART |
| **BSC( Balanced Scorecard)** | 전략 성과 측정 | **4 관점(재무/고객/내부/학습성장)** KPI 설계; **Kaplan-Norton 전략맵** 연결; IT-BSC는 **McDonald, Van Grembergen(1997)** 모델로 **"Business Contribution"·"Future Orientation"** 2축 추가 |
| **정보기술 감리 제도** | 한국 IT 프로젝트 품질 보증 | **공공부문 5억/민간 30억 이상** 의무; **5단계 감리**: 일반/상세/최종/사후/연차; **PMO·감리법인** 독립성 확보(중립성 원칙); **감리 기준**: 시스템 개발·운영·정보보호·사업관리 4개 영역 |
| **ISMS / PIMS** | 정보보호/개인정보 관리체계 | **ISMS-P**: 한국인터넷진흥원(KISA) 인증, 13개 영역 80여개 통제항목; **ISMS(2024 개편)**: 관리체계/보호대책/사고대응 3개 영역; **ISO 27001:2022**: 93개 통제(Organizational 37, People 8, Physical 14, Technological 34) |

**핵심 원리 심층 분석**:

1. **Ward & Peppard(2002) Strategic Alignment Model**: **"Business Strategy ↔ IT Strategy"** 와 **"Business Infrastructure & Process ↔ IT Infrastructure & Process"** 의 **"Strategic Fit"** + **"Functional Integration"** 으로 4가지 정렬(Execution, Transformation, Alignment, Lever) 도출.

2. **Henderson & Venkatraman(1993) SAM**: **"External"** vs **"Internal"**, **"IT Impact"** vs **"Strategy"** 의 2×2 매트릭스로 4가지 관점(Strategy Execution, Technology Potential, Competitive Potential, Service Level) 제공.

3. **IT 투자 가치 평가 3대 지표**:
   - **TCO(Total Cost of Ownership)**: Gartner 모델 기준 5년 누적 비용(하드웨어 20% + 소프트웨어 15% + 인건비 50% + 기타 15%)
   - **ROI(Return on Investment)**: `(총效益 - 총비용) / 총비용 × 100`
   - **NPV(Net Present Value)**: `Σ [CF_t / (1+r)^t] - 초기투자` (할인율 r 통상 8-12%)
   - **Payback Period**: 누적 현금흐름이 0이 되는 시점 (보통 3-5년 이내 권장)
   - **BSC 4관점 KPI**: 재무(ROA, EVA), 고객(NPS, 만족도), 내부(처리속도, 품질), 학습(직원 역량지수)

4. **Enterprise Architecture 4A 모델**: **BA(비즈니스) -> DA(데이터) -> AA(응용) -> TA(기술)** 의 계층적 정렬, **Zachman Framework 6x6 = 36
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 519 / 800

<- **이전**: [518. IT 경영 관리 핵심 토픽 518번 시험 요약](/studynote/12_it_management/05_security_compliance/518_it_management_core_topic_518_exam_summary/)
**다음**: [520. IT 경영 관리 핵심 토픽 520번 시험 요약](/studynote/12_it_management/05_security_compliance/520_it_management_core_topic_520_exam_summary/) ->

---
