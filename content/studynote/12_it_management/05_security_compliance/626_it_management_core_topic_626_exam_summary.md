+++
title = "626. IT 경영 관리 핵심 토픽 626번 시험 요약 (IT Management Core Topic 626 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리(정보시스템 컨설턴트 기술사 시험 626번)는 COBIT 2019, ITIL 4, ISO 38500 등 글로벌 거버넌스 프레임워크를 기반으로 IT 거버넌스·전략 기획·프로젝트 관리·정보시스템 감사·정보보안 거버넌스·IT 서비스 관리(BSM)·정보화 투자대비성과평가(ROI/NPV/IRR)·EA(엔터프라이즈 아키텍처)·DBA·BPR/PI를 통합하는 **이해관계자 가치(Value Delivery) 최적화** 체계이다.
> 2. **가치**: McKinsey 2023 보고 기준 글로벌 디지털 전환 실패율 70% 이상을 거버넌스 부재로 진단하며, COBIT 기반 Maturity Level 1단계->5단계 도달 시 IT 투자 ROI 평균 28%->72% 향상, ITIL 4 실무 적용으로 인시던트 MTTR 47% 단축, BSC 4관점 균형 지표 운영 시 전략 목표 달성률 35% 개선 효과가 보고되고 있다.
> 3. **판단 포인트**: 거버넌스 모델 채택 시 **규모(SMEs vs Enterprise)·규제(전자금융감독규정, 개인정보보호법, DORA)·산업(Banking, Manufacturing, Public)·성숙도**에 따라 COBIT 2019 Design Factors 11개를 활용한 컨텍스트 맞춤 설계가 핵심이며, IT-Business Alignment 수준을 SAMM/CMMI-ACQ 모델로 정량 진단한 뒤 Water-Scrum-Fall, SAFe, LeSS 등 Agile-Scale 방법론을 선택하는 것이 기술사적 판단 기준이다.

---

## Ⅰ. 개요 및 필요성

정보시스템의 복잡성과 비즈니스 환경의 불확실성이 기하급수적으로 증가하면서, IT 부서는 단순 비용센터(Cost Center)에서 **전략적 비즈니스 파트너(Strategic Partner)** 그리고 **가치 창출 엔진(Value Driver)**로 그 역할이 재정의되고 있다. 과거 1980~90년대에는 전산실 중심의 시스템 운영과 데이터 처리(Data Processing)에 머물렀으나, 2000년대 이후 e-Business, Cloud, Mobile, AI/ML, IoT, Blockchain, Generative AI로 이어지는 기술 패러다임의 변곡점마다 IT-Business Alignment 실패, Shadow IT 급증, 프로젝트 실패율 60% 이상(Standish Group CHAOS Report 2020), 정보화 투자 대비 미흡한 성과(情報化投資 效率 分析), 보안 사고로 인한 사회적 비용(KR CERT 2023년 기준 연간 2.3조 원 피해) 등 **시스템적 실패(Systemic Failure)**가 반복되었다.

이에 대한 해법으로 국제 표준화 기구(ISO/IEC), 국제 IT 거버넌스 협회(ISACA), ITIL Foundation(축약형), OGC(영국) 등에서 제정한 거버넌스 프레임워크가 등장했고, 특히 1996년 ISACA의 COBIT(Control Objectives for Information and Related Technologies)이 5개 버전을 거쳐 2019년 40개 거버넌스/관리 목표(Governance & Management Objectives)와 11개 Design Factors로 진화하면서 **원리(Principles)->목표(Goals)->컴포넌트(Components)->맥락(Context)** 의 체계적 설계 체계를 확립했다. 국내에서는 전자정부법, 정보시스템의 효율적 도입 및 운영에 관한 지침(행정안전부), 클라우드 컴퓨팅법(2024년), 데이터 산업법(2022년), 인공지능 기본법(2025년 시행 예정)에 따라 IT 거버넌스가 법적 의무사항이 되었으며, **정보시스템 감리제도**(감리법인 등록·수행)는 IT 프로젝트의 품질·성능·보안·법규준수를 외부 전문가가 검증하는 핵심 통제 장치로 작동한다.

본 토픽은 **①IT 거버넌스 수립·운영 ②전략 기획 및 정보화 투자 분석 ③프로젝트 관리 방법론 ④정보시스템 감리/감사 ⑤정보보안 및 컴플라이언스 ⑥IT 서비스 관리 및 운영 ⑦EA·DBA·BPR**의 7대 영역에 대한 통합적 지식체(Body of Knowledge)를 다루며, 기술사 시험의 근간을 형성한다.

```text
+------------------------------------------------------------------+
|           IT 경영관리 7대 통합 지식 체계 (626번 토픽)            |
+------------------------------------------------------------------+
|                                                                  |
|  +----------+   +----------+   +----------+   +----------+       |
|  | ①거버넌스 |   |②전략기획 |   |③프로젝트 |   | ④감리/   |       |
|  | Governance|   | Strategy |   |  관리    |   |  감사    |       |
|  |  ·COBIT  |◄-►|  ·BSC    |◄-►|  ·PMBOK  |◄-►| ·감리원  |       |
|  |  ·ITIL   |   |  ·KPI    |   |  ·PRINCE2|   | ·ISACA   |       |
|  |  ·ISO    |   |  ·SWOT   |   |  ·Agile  |   |  Audit   |       |
|  +----+-----+   +----+-----+   +----+-----+   +----+-----+       |
|       |              |              |              |             |
|       +------+-------+------+-------+------+-------+             |
|              |              |              |                     |
|              v              v              v                     |
|  +----------+   +----------+   +------------------+              |
|  | ⑤보안/   |   | ⑥IT서비스|   | ⑦ EA·DBA·BPR     |              |
|  | 컴플라이언스|  |   운영    |   |  Enterprise     |              |
|  |  ·ISMS   |◄-►|  ·ITIL 4 |◄-►| Architecture    |              |
|  |  ·PIPC   |   |  ·BSM    |   |  ·TOGAF·Zachman |              |
|  |  ·ISO   |   |  ·AIOps  |   |  ·DBA·BPMN      |              |
|  +----------+   +----------+   +------------------+              |
|              |              |              |                     |
|              +--------------+--------------+                     |
|                             v                                    |
|              +------------------------------+                    |
|              |  IT-Business Alignment &     |                    |
|              |  Value Delivery (가치 창출)   |                    |
|              |  -> 이해관계자 만족(Stakeholder|                    |
|              |    Satisfaction) 최적화      |                    |
|              +------------------------------+                    |
+------------------------------------------------------------------+
```

기존 **Data Processing 시대(1960~1980)**는 EDP 컨트롤러, 시스템 분석가(SA), 프로그래머(PE) 중심의 기술 중심 조직, **MIS 시대(1980~1990)**는 CIO 등장 및 경영정보시스템, **ERP 시대(1990~2000)**는 SAP R/3, Oracle EBS, 국내 더존 iCUBE, 영림원 ERP-K, 한컴인텔리전스 uSales 등의 통합 패키지, **Web 2.0/Cloud 시대(2000~2015)**는 SaaS, IaaS, PaaS, **Digital Transformation 시대(2015~현재)**는 AI-First 전략, Data-Driven 의사결정, ESG 통합, **AI-네이티브 시대(2023~)**는 Generative AI(LLM), MLOps, AIOps, AI 윤리, AI 거버넌스(AI Governance)로 빠르게 진화했다.

- **📢 섹션 요약 비유**: IT 경영관리는 **자동차 운전**과 같다. 차량(시스템)의 부품(데이터·네트워크·SW)이 아무리 좋아도, 운전자(거버넌스), 내비게이션(전략), 정비(감리), 신호(컴플라이언스), 목적지(Value Delivery) 설정이 잘못되면 목적지에 도달하지 못한다. 기술사(技術士)는 자동차의 설계자이자 정비사이자 운전 코치의 역할을 통합 수행해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 핵심 아키텍처는 **"원리(Principles) -> 목표(Goals) -> 컴포넌트(Components) -> 통제(Controls) -> 측정(Metrics) -> 개선(Improvement)"** 의 6단계 가치사슬(Value Chain) 구조로 이해할 수 있다. COBIT 2019는 이를 **Governance System(거버넌스 시스템)**과 **Governance Framework(거버넌스 프레임워크)**로 분리하여, EDM(평가·지휘·모니터) 5개 + APO(정렬·계획·조직) 14개 + BAI(구축·획득·구현) 11개 + DSS(전달·지원·운영) 6개 + MEA(모니터링·평가·평가) 4개로 총 **40개 관리 목표**를 제시한다. 각 목표는 **Process(프로세스)·Organizational Structure(조직구조)·Information Flow(정보흐름)·People, Skills and Competencies(인적역량)·Policies and Procedures(정책)·Culture, Ethics and Behavior(문화)·Services, Infrastructure and Applications(서비스)·People, Skills and Competencies(인력)** 의 7개 컴포넌트 변형(Components Variants)을 갖는다.

```text
+--------------------------------------------------------------------+
|            COBIT 2019 거버넌스 시스템 아키텍처 (40개 목표)         |
+--------------------------------------------------------------------+
|                                                                    |
|  +----------------------------------------------------+            |
|  |  EDM : Evaluate, Direct, Monitor (5개)             |            |
|  |  +-- EDM01 거버넌스 프레임워크 설정/유지           |            |
|  |  +-- EDM02 이해관계자 가치창출 및 실현             |            |
|  |  +-- EDM03 위험 최적화                            |            |
|  |  +-- EDM04 자원 최적화                            |            |
|  |  +-- EDM05 이해관계자 투명성 확보                 |            |
|  +--------------------+-------------------------------+            |
|                       |                                            |
|  +--------------------+-------------------------------+            |
|  |  APO : Align, Plan, Organize (14개)                |            |
|  |  +-- APO01~APO14 (전략, 포트폴리오, 예산,        |            |
|  |       관계, 위험, 아키텍처, 혁신, BCM, ...)        |            |
|  +--------------------+-------------------------------+            |
|                       |                                            |
|  +--------------------+-------------------------------+            |
|  |  BAI : Build, Acquire, Implement (11개)            |            |
|  |  +-- BAI01~BAI11 (솔루션, 데이터, 자산, 변경, ...) |            |
|  +--------------------+-------------------------------+            |
|                       |                                            |
|  +--------------------+-------------------------------+            |
|  |  DSS : Deliver, Service, Support (6개)             |            |
|  |  +-- DSS01~DSS06 (운영, 인시던트, 문제, BC, 보안) |            |
|  +--------------------+-------------------------------+            |
|                       |                                            |
|  +--------------------+-------------------------------+            |
|  |  MEA : Monitor, Evaluate, Assess (4개)             |            |
|  |  +-- MEA01~MEA04 (성능, 컴플라이언스, 내부통제)   |            |
|  +----------------------------------------------------+            |
|                                                                    |
|  7대 컴포넌트 변형: Process / Org.Structure / Information Flow /  |
|  People·Skills / Policies / Culture / Services·Infra·Apps         |
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 (거버넌스 프레임워크)** | IT 거버넌스/관리 목표 40개 정의, 11개 Design Factor로 조직별 맞춤 설계 | Cascade of Goals(13개 기업목표->40개 IT목표->7개 컴포넌트->Risk), 5단계 Maturity Model(0: 불완전~5: 최적화), CMMI(능력성숙도모델) 기반 프로세스 능력 PA(Process Attribute) 6개 |
| **ITIL 4 (IT 서비스 관리)** | 34개 Practise(Value Stream 중심), Service Value System(SVS) 기반 서비스 가치 창출 | SVS: Opportunity/Demand->Value->Service Value Chain(Plan/Improve/Engage/Design&Transition/Obtain&Build/Deliver&Support)->Value, 4D 모델(Direction, Design, Development, Delivery) |
| **ISO/IEC 38500 (거버넌스 표준)** | 이사회/경영진의 IT 활용·평가·지휘·모니터링 원칙 제시 | 6원리(책임, 전략, 획득, 성능, 적합, 인간행동), ITGI의 6개 Govern 프로세스(EDM 모델) |
| **Balanced Scorecard (BSC)** | 4관점(재무·고객·내부프로세스·학습성장) 균형 KPI 운영 | Strategy Map(전략->세부목표->KPI->Target->Initiative), Cause-and-Effect Linkage, Personal BSC -> Team BSC -> Corporate BSC Cascade |
| **PMBOK 7 / PRINCE2 / Agile** | 프로젝트 관리 방법론, 예측형/적응형/하이브리드 | PMBOK 7: 12 Principle + 8 Performance Domain, PRINCE2: 7 Principle+7 Process+7 Theme, Agile: Scrum(Sprint, Product Backlog, Daily Scrum, Review, Retrospective), Kanban, XP, LeSS, SAFe |
| **EA (Enterprise Architecture)** | 비즈니스·데이터·애플리케이션·기술 4계층 통합 정렬 | TOGAF ADM(Architecture Development Method) 8단계 Phase, Zachman Framework 6×6 매트릭스, DoDAF, FEAF, 한국 EA-Framework(KEAF) |
| **정보보안 거버넌스** | 정보자산의 CIA(기밀성·무결성·가용성) 보호 및 위험관리 | ISMS-P(한국, 80개 통제항목), ISO/IEC 27001/27002/27005, NIST CSF(Identify, Protect, Detect, Respond, Recover), PIPC 개인정보 영향평가 |

**핵심 알고리즘 및 정량 분석 기법**:

1. **정보화 투자대비성과평가 (Economic Value Add 기반)**:
   - **ROI(투자대비성과)** = (순이익 / 총투자비용) × 100
   - **NPV(순현재가치)** = Σ[CF_t / (1+r)^t] - I₀, r=할인율, t=기간
   - **IRR(내부수익률)** = NPV=0이 되는 r
   - **TCO(Total Cost of Ownership)** = 하드웨어 + S/W + 설치 + 운영 + 유지보수 + 교육 + 기회비용
   - **Payback Period(투자회수기간)** = 초기투자 / 연평균현금흐름

2. **위험 분석 정량 모델**:
   - **ALE(Annual Loss Expectancy)** = SLE(단일손실기대값) × ARO(연간발생횟수)
   - SLE = Asset Value × Exposure Factor
   - **Risk Heat Map**: 발생가능성(Likelihood) × 영향도(Impact) 5×5 매트릭스
   - **FAIR(Factor Analysis of Information Risk)** 모델: Threat Event Frequency × Vulnerability × Loss Magnitude

3. **BSC Balanced Scorecard 4관점 KPI 예시**:
   - 재무: ROE(자기자본이익률), Economic Value Added(EVA), Revenue/Employee
   - 고객: Net Promoter Score(NPS), Customer Lifetime Value(CLV), Customer Acquisition Cost(CAC)
   - 내부프로세스: Order Fulfillment Cycle Time, Defect Rate(DPM
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 626 / 800

<- **이전**: [625. IT 경영 관리 핵심 토픽 625번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/625_it_management_core_topic_625_exam_summary/)
**다음**: [627. IT 경영 관리 핵심 토픽 627번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/627_it_management_core_topic_627_exam_summary/) ->

---
