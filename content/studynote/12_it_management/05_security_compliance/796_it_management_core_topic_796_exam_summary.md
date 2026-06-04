+++
title = "796. IT 경영 관리 핵심 토픽 796번 시험 요약 (IT Management Core Topic 796 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리 796번은 COBIT 2019(40개 거버넌스/관리 목표), ITIL 4(34개 실무 관리 Practice), ISO 38500(6원칙), PMBOK 7(8개绩效域)을 통합적으로 연계하여 **전략(Strategy)–거버넌스(Governance)–운영(Operations)의 3축 정렬(Value Governance)**을 입증하는 시험으로, 단순 암기가 아닌 프레임워크 간 상호운용성(Interoperability)과 실무 적용 판단력을 평가한다.
> 2. **가치**: CSF(Critical Success Factor)–KGI(Key Goal Indicator)–KPI(Key Performance Indicator) 3단 계층으로 연결된 측정 체계와 Balanced Scorecard(재무/고객/내부프로세스/학습성장 관점)를 적용 시 **IT 투자 ROI 20~35% 개선**, **프로젝트 성공률 28% -> 72% 향상**(Standish Group CHAOS Report 2023 기준), **이해관계자 만족도 40% 증가**의 정량 효과를 창출한다.
> 3. **판단 포인트**: **"거버넌스는 과도하게, 관리는 유연하게(Govern Tight, Manage Loose)"** 원칙 하에, (a)Top-Down(거버넌스) ↔ Bottom-Up(운영) 균형, (b)전사 아키텍처(EA-TOGAF) ↔ 현업 Agile(Scrum/Kanban) 공존, (c)내부 통제(SOX/내부감사) ↔ 외부 혁신(Open Innovation) 트레이드오프, (d)Zero Trust 보안 ↔ 사용자 경험(UX) 상충 관계를 어떻게 정량적 위험 매트릭스(5×5 Risk Matrix)로 합리화하느냐가 합격/불합격을 가른다.

---

## Ⅰ. 개요 및 필요성

정보기술의 사회적·경제적 침투율이 GDP 대비 5%대를 넘어선 4차 산업혁명 시대(2016~)에 진입하면서, IT는 단순 지원(Back-office) 기능을 넘어 **비즈니스 모델 그 자체**(예: 카카오뱅크, 토스, 쿠팡의 풀필먼트 IT)를 재정의하는 핵심 자산이 되었다. 이에 발맞추어 과학기술정보통신부는 「정보시스템의 효율적 도입 및 운영에 관한 지침」(2021.12. 개정)을 통해 **EA(Enterprise Architecture, 전사 아키텍처)**, **ISP(Information System Planning, 정보화 전략계획)**, **정보시스템 감리**(발주자 관점)를 3대 축으로 명시화하였고, 행정안전부는 「정부 디지털 전환 추진에 관한 기본법」(2023.05. 시행)을 통해 **디지털 서비스 표준화**, **클라우드 우선 정책(Cloud First)**, **데이터 거버넌스**를 의무화하였다. 이러한 환경에서 IT 경영관리 기술사는 단순히 시스템을 구축하는 엔지니어가 아니라, **CEO/CIO/CTO급 의사결정을 지원**하고, **이사회(Board) 수준에서 IT 가치를 증명**하며, **규제 준수(Compliance)와 혁신을 동시에 달성**할 수 있는 전략적 리더십을 입증해야 한다.

796번 시험은 이러한 배경에서 **단편적 기술 지식**(예: OSI 7계층, SQL 문법)이 아닌 **프레임워크 통합·리스크 기반 의사결정·정성·정량 혼합 평가** 능력을 평가하기 위해 설계되었다. 2020년 이후 출제 경향을 분석하면, 단순 정의형 5지선다(객관식) 10문항(30점) + 주관식 서술형 4~5문항(70점) 구성에서, 주관식 비중이 70%로 압도적이며, 특히 **"OO 프레임워크를 적용하여 ~한 방안을 제시하시오"** 형태의 **솔루션 제시형 논술**이 60% 이상을 차지한다. 따라서 본 토픽은 기술사 1차·2차 전 영역에 걸친 **통합적 사고(Integrated Thinking)** 시험이라 할 수 있다.

```text
       +-------------------------------------------------------------+
       |           IT 경영관리 796번 출제 프레임 (3-tier Model)        |
       +-------------------------------------------------------------+
                                 |
        +------------------------+--------------------------------+
        |                        |                                |
   +----v-----+            +-----v------+                  +------v------+
   |  Tier 1  |            |   Tier 2   |                  |   Tier 3    |
   | 거버넌스  |◄----------►|   전략/EA  |◄----------------►|   운영/감리  |
   | (Why)    |            |  (What)    |                  |   (How)     |
   +----+-----+            +-----+------+                  +------+------+
        |                        |                                |
   ISO 38500              TOGAF ADM                  PMBOK 7 / ITIL 4
   COBIT 2019             FEAF / DoDAF               DevOps / SRE
   SOX / J-SOX            Zachman Framework          정보시스템 감리
   ESG/TCFD               데이터 거버넌스(DAMA)        BCP/DR (ISO 22301)
        |                        |                                |
        +------------------------+--------------------------------+
                                 |
                  +--------------v--------------+
                  |   ★ 기술사 1차/2차 합격역량 ★  |
                  |  - 통합적 의사결정 판단력       |
                  |  - 정량·정성 혼합 정당화 능력   |
                  |  - 규제·리스크·가치 균형 감각   |
                  +-----------------------------+
```

| 구분 | 과거(2000년대) 패러다임 | 현재(2020년대) 패러다임 | 시험 요구 역량 변화 |
| :--- | :--- | :--- | :--- |
| **IT 역할** | 비용(Cost Center)·지원(Back-office) | 가치(Value Creator)·사업 동반자(Business Partner) | CFO 관점의 정량 ROI 제시 능력 |
| **관리 방식** | 프로젝트 단위·사일로(Silo) | 포트폴리오·제품 중심·End-to-End | PMBOK -> P3O·SAFe·Agile 포트폴리오 전환 |
| **거버넌스** | 컴플라이언스 중심(SOX 404) | 가치 중심(COBIT 2019 EDM) | 40개 목표 중 5~7개 우선순위 선정 논리 |
| **아키텍처** | 솔루션 아키텍처(SA) | 전사 아키텍처(EA-TOGAF ADM) | Baseline->Target->Transition 3단계 Gap 분석 |
| **데이터** | DBMS·데이터웨어하우스 | 데이터 거버넌스·레이크·메쉬 | 마스터/메타/품질/보안 4축 통합 |
| **보안** | 경계 보안(Perimeter) | Zero Trust·SASE·XDR | NIST CSF 5함수(Identify~Recover) 적용 |
| **인재** | 직무 중심(Specialist) | T자형·π자형·Citizen Developer | 거버넌스 위원회 거버넌스 운영 역량 |

- **📢 섹션 요약 비유**: IT 경영관리를 **"건물의 설계·감리·시공·유지관리 통합 PMO"**에 비유할 수 있다. ISO 38500은 **건축법·도시계획**(상위 원칙), TOGAF는 **설계도**(EA), PMBOK은 **시공 매뉴얼**, ITIL은 **건물 운영·시설 관리 지침**, COBIT는 **감리·점검 체크리스트**에 해당하며, 기술사는 이 모든 도면을 읽고 건축주(경영진)에게 **"어떤 건물을 어떤 비용으로 언제 지을지"**를 정량적으로 조언하는 **CM(Construction Manager)** 역할을 수행해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 4대 핵심 프레임워크는 각각 고유한 추상화 수준과 적용 영역을 가지며, **거버넌스–전략–전환–운영의 4-layer 통합 아키텍처**로 결합된다. 아래 ASCII 다이어그램은 796번 시험에서 가장 빈번하게 출제되는 **"프레임워크 통합 모델"**의 표준 참조 구조(Reference Architecture)를 나타낸다.

```text
        +----------------------------------------------------------------+
        |                Enterprise Mission & Vision (경영 비전)          |
        +-----------------------------+----------------------------------+
                                      |  전략 정렬(Strategy Alignment)
        +-----------------------------v----------------------------------+
        |  [Layer 1: GOVERNANCE]  ----  ISO 38500 6원칙, COBIT 2019 EDM  |
        |   +- Evaluate(평가) -> Direct(지휘) -> Monitor(모니터링)            |
        |   +- 40개 Governance/Management Objectives 중 5~7개 우선순위화   |
        |   +- RACI Matrix (Responsible/Accountable/Consulted/Informed)    |
        +-----------------------------+----------------------------------+
                                      |  Balanced Scorecard 4관점
        +-----------------------------v----------------------------------+
        |  [Layer 2: STRATEGY/EA]  ----  TOGAF ADM, Zachman, FEAF        |
        |   +- Preliminary Phase(비전) -> Phase A(Architecture Vision)      |
        |   +- B~D: Business/Data/Application/Technology Architecture      |
        |   +- E: Opportunities & Solutions -> F: Migration Planning       |
        |   +- G: Implementation Governance -> H: Architecture Change Mgmt |
        |   +- Requirements Management(요구사항 전생애 주기)                |
        +-----------------------------+----------------------------------+
                                      |  Business Case / 투자 포트폴리오
        +-----------------------------v----------------------------------+
        |  [Layer 3: DELIVERY]   ----  PMBOK 7, PRINCE2, SAFe, Scrum     |
        |   +- 8대 Performance Domain: Stakeholders/Team/Development       |
        |   |     Planning/Project Work/Delivery/Measurement/Complexity    |
        |   |     Risk (구 10 Knowledge Area 대체)                          |
        |   +- Predictive(Waterfall) ↔ Adaptive(Agile) ↔ Hybrid(SAFe)     |
        |   +- DevOps CALMS: Culture/Automation/Lean/Measurement/Sharing    |
        +-----------------------------+----------------------------------+
                                      |  SLA / OLA / UC(Service Charter)
        +-----------------------------v----------------------------------+
        |  [Layer 4: OPERATIONS]  ----  ITIL 4 SVS, SRE, AIOps           |
        |   +- 34개 Service Management Practices (변경관리, 인시던트,      |
        |   |     문제관리, 서비스데스크, SLM, 가용성/용량, 보안, 지속성)   |
        |   +- SVS: Service Value System(가치공동창출/원리/거버넌스/         |
        |   |     실무/지속적개선) + 4P(Product/Partner/People/Process)     |
        |   +- AIOps: 이상탐지·자동복구·예측분석(Event->Insight->Action)    |
        +----------------------------------------------------------------+

        ★ Cross-Layer 핵심 기제(Key Mechanisms) ★
        +--------------------------------------------------------------+
        | • CSF-KGI-KPI 3단 연결 (위에서 아래로 인과, 아래에서 위로 측정)|
        | • Risk Matrix (5×5 Impact×Likelihood) -> Risk Register         |
        | • Business Case: NPV, IRR, Payback Period, TCO, ROI           |
        | • Capability Maturity Model: CMM 5단계 or CMMI v2.0 5단계     |
        | • Control Objective (COBIT) ↔ Control Activity (SOX 404) 매핑 |
        +--------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **ISO 38500 (2008->2015)** | **상위 거버넌스 원칙 프레임워크** | 6원칙(책임Responsibility, 전략Strategy, 인수Acquisition, 성능Performance, 준거Conformance, 인간행태Human Behavior) + 3계층(Evaluate–Direct–Monitor, **EDM 모델**). 비영리 단체가 만든 표준으로 COBIT·ITIL과 달리 인증/감사 도구 없이 **이사회 거버넌스 원칙**만 제공. 시험에서는 "ISO 38500과 COBIT 2019의 관계"가 빈출. |
| **COBIT 2019 (구 5->2019)** | **거버넌스-관리 통합 프레임워크** | **40개 목표(20 Gov + 20 Mgmt)** + **5개 도메인**(EDM/APO/BAI/DSS/MEA) + **7개 컴포넌트**(원리/정책/구조/프로세스/정보/문화/인력/기술) + **중심축: Goals Cascade**(Stakeholder Needs->Enterprise Goals->Alignment Goals->Component Goals). **2019 신규: Focus Area**(예: DevOps, 위험, 보안, BCS, 디지털거버넌스) + **Design Factor 11개**로 맞춤형 거버넌스 시스템 설계. |
| **TOGAF (10세대, 2022)** | **전사 아키텍처 개발 방법론** | **ADM(Architecture Development Method)** 8단계 + Requirements Management(중심 허브) + **ADM Guidelines**(무/무, 이 단계/표준화, 단계 간 적용 가능). 시험 출제 빈도: "Phase H(거버넌스)의 필요성", "Baseline vs Target Architecture Gap 분석 절차", "Architecture Repository(Architecture/Standards/Capability/Project/Governance Board)". |
| **ITIL 4 (2019, AXELOS->PeopleCert)** | **서비스 운영·관리 실무 프레임워크** | **SVS(Service Value System)** 5컴포넌트(Op
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 796 / 800

<- **이전**: [795. IT 경영 관리 핵심 토픽 795번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/795_it_management_core_topic_795_exam_summary/)
**다음**: [797. IT 경영 관리 핵심 토픽 797번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/797_it_management_core_topic_797_exam_summary/) ->

---
