+++
title = "523. IT 경영 관리 핵심 토픽 523번 시험 요약 (IT Management Core Topic 523 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(IT Governance)는 COBIT 2019의 40개 거버넌스·관리 목표와 5개 도메인(EDM/APO/BAI/DSS/MEA)을 통해 IT와 비즈니스 전략을 정렬(Alignment)하고, 의사결정 권한·책임·보고 체계(Decision Rights & Accountability)를 Board-CEO-Executive-Operational 4계층으로 표준화하는 경영 메커니즘이다.
> 2. **가치**: 글로벌 통계(스탠다드앤드푸어스 2023, ISACA 2022)에 따르면 성숙한 IT 거버넌스 도입 조직은 IT 투자 ROI를 평균 **20~35%** 개선하고, 프로젝트 실패율을 **60%->15%** 수준으로 축소하며, 정보보안 사고 대응시간(MTTR)을 **43% 단축**(IBM 2023 Cost of Data Breach Report 기준)한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **① 중앙집중형 vs 분산형 거버넌스 구조(Governance Modality)**, **② COBIT·ITIL·ISO 38500 중 어떤 프레임워크를 메타 거버넌스로 채택할 것인가**, **③ 가치(Value)·리스크(Risk)·자원(Resource)의 3대 균형 축을 어떤 KPI(Run/Grow/Transform)로 측정할 것인가**이며, 조직의 COBIT 성숙도(Level 1~5)와 Bain & Company의 6가지 거버넌스 모달리티(Governance/Business Monarchy, IT Duopoly, IT Monarchy, Federal, Feudal, Anarchy) 중 현재 위치 판별이 의사결정의 출발점이다.

---

## Ⅰ. 개요 및 필요성

정보기술이 단순 비용센터(Cost Center)에서 **전략적 가치 창출 엔진(Value Driver)**으로 전환되면서, IT 투자의 의사결정 권한·성과 책임·리스크 관리를 경영 시스템과 통합해야 할 필요성이 대두되었다. 과거(1980~2000년대)에는 CIO가 **"IT 부서 운영"**에 집중하여 데이터센터·네트워크·ERP의 효율적 가용성(Uptime 99.9%)을 KPI로 삼았으나, 디지털 전환·클라우드·AI·규제강화(전자금융감독규정, DORA, GDPR)가 겹친 2020년대에는 **"IT로 무엇을 창출하는가"**가 이사회(Board) 차원의 의제로 격상되었다.

이에 IT 거버넌스는 **① 전략적 정렬(Strategic Alignment)**, **② 가치 실현(Value Delivery)**, **③ 리스크 관리(Risk Management)**, **④ 자원 최적화(Resource Management)**, **⑤ 성과 측정(Performance Measurement)**의 5대 영역을 다루며, ISACA의 COBIT 2019, AXELOS의 ITIL 4, ISO/IEC 38500, CIS의 18대 Critical Security Controls, NIST CSF 2.0, CMMI v2.0 등 다수의 글로벌 프레임워크를 통합·매핑하는 **메타 거버넌스(Meta-Governance)** 체계를 요구한다.

```text
[ IT 거버넌스 4계층 의사결정 구조와 프레임워크 매핑 ]

 +--------------------------------------------------------------+
 |  Board of Directors (이사회)                                  |
 |  +- IT Strategy Committee (IT 전략위원회)                    |
 |     • 정렬: IT 거버넌스 정책, Risk Appetite, 투자한도          |
 |     • 참조: ISO/IEC 38500 (6 Principles)                     |
 |     •       COBIT 2019 EDM Domain (Evaluate, Direct, Monitor)|
 +------------------------+-------------------------------------+
                          | 정책·지침 하달
 +------------------------v-------------------------------------+
 |  Executive (경영진 / C-Level)                                 |
 |  +- CIO (Chief Information Officer) — IT Portfolio Owner    |
 |  +- CDO (Chief Data Officer) — 데이터 거버넌스              |
 |  +- CISO (Chief Information Security Officer)               |
 |  +- CRO (Chief Risk Officer) — 2nd Line Defense              |
 |     • 정렬: APO Domain (Align, Plan, Organize)               |
 |     • 참조: COBIT 2019, NIST CSF 2.0 Govern Function        |
 +------------------------+-------------------------------------+
                          | KPI·SLA·RACI 위임
 +------------------------v-------------------------------------+
 |  Management (IT 거버넌스 실무조직)                             |
 |  +- IT Steering Committee (주간/월간)                         |
 |  +- Architecture Review Board (ARB) — EA 심의               |
 |  +- Change Advisory Board (CAB) — ITIL 4 Change Enablement  |
 |  +- Risk & Compliance Committee                              |
 |     • 정렬: BAI/DSS Domain                                   |
 +------------------------+-------------------------------------+
                          | Service Level Agreement
 +------------------------v-------------------------------------+
 |  Operational (현업 + IT 실무)                                 |
 |  +- Service Desk (L1) -> Incident Mgmt (L2) -> Problem Mgmt   |
 |  +- DevOps / SRE / Platform Engineering                      |
 |  +- Business Process Owner (BPO)                              |
 |     • 정对齐: MEA Domain (Monitor, Evaluate, Assess)         |
 +--------------------------------------------------------------+
```

**📢 섹션 요약 비유**: IT 거버넌스는 **비행기의 조종석 계기판(PFD, Primary Flight Display)**과 같다. 기장(CEO) 혼자 모든 스위치를 만지는 것이 아니라, 부기장·기관사·탑승객 안내원(CIO, CISO, BPO)에게 정해진 역할(Role)과 교차 점검(Cross-check)을 부여하고, 1,000개의 센서(40개 COBIT 목표)로부터 데이터를 받아 단일 계기판으로 의사결정을 통합하는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019 5대 도메인과 40개 거버넌스·관리 목표

COBIT 2019는 **Governance Objectives(EDM 5개)**와 **Management Objectives(APO 14 + BAI 11 + DSS 6 + MEA 4 = 35개)**, 총 **40개 목표**를 제공한다. 각 목표는 **Process(프로세스) + Organizational Structure(조직) + Information Flows(정보흐름) + People/Skills(역량) + Policies(정책) + Culture/Behavior(문화)**의 7대 구성요소(Components of the Governance System)로 분해된다.

```text
[ COBIT 2019 Cascade: Need -> Goals -> Enterprise -> Alignment ]

              +------------------------------------+
              |  Stakeholder Needs (이해관계자 요구) |
              |  • Benefit Realization(가치실현)     |
              |  • Risk Optimization(리스크최적화)   |
              |  • Resource Optimization(자원최적화) |
              +------------+-----------------------+
                           v
              +------------------------------------+
              |  Enterprise Goals (13개)            |
              |  EG01 포트폴리오, EG05 재무,        |
              |  EG09 정보처리, EG13 디지털혁신     |
              +------------+-----------------------+
                           v (13 -> 40 매핑)
              +------------------------------------+
              |  Alignment Goals (13개)             |
              |  AG01 I&T 준수, AG05 리스크관리,    |
              |  AG09 시스템 적정, AG13 지식역량    |
              +------------+-----------------------+
                           v (13 -> 40 매핑)
              +------------------------------------+
              |  Governance & Management Objectives |
              |  EDM01~05, APO01~14, BAI01~11,     |
              |  DSS01~06, MEA01~04 = 40개         |
              +------------+-----------------------+
                           v
              +------------------------------------+
              |  7대 구성요소 (Components)          |
              |  Process · Structure · Flow ·      |
              |  People · Policy · Culture · Infra  |
              +------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate·Direct·Monitor)** | 이사회 거버넌스 의사결정 | EDM01 거버넌스체계, EDM02 수익/리스크 균형, EDM03 Risk Appetite 정의(예: 사이버사고 손실 < 매출의 0.5%), EDM04 자원전략, EDM05 투명성 보고 |
| **APO (Align·Plan·Organize)** | IT 전략·포트폴리오·아키텍처·혁신 관리 | APO01 I&T 관리체계, APO02 전략, APO04 조직, APO05 포트폴리오, APO12 리스크관리, APO13 보안(ISO 27001 연계) |
| **BAI (Build·Acquire·Implement)** | 시스템 구축·변경·도입 관리 | BAI01 프로그램, BAI02 요구사항(Re-engineering), BAI03 솔루션설계(MSA 기반), BAI11 시스템관리(DevOps) |
| **DSS (Deliver·Service·Support)** | IT 서비스 운영·지원 | DSS01~05 ITIL 4 매핑(Incident·Problem·Change·Service Request·Service Desk), DSS06 보안운영(SIEM·SOAR) |
| **MEA (Monitor·Evaluate·Assess)** | 성과측정·내부감사·컴플라이언스 | MEA01 성과, MEA02 내부통제(SOX 404), MEA03 컴플라이언스, MEA04 이슈·개선 |
| **7대 Components** | 거버넌스 시스템 구성단위 | Process(5단계: Plan->Acquire->Deliver->Support->Monitor), Structure(Board->Committee->PMO), Skills(SFIA 8), Policy(3-tier), Culture(톤프레임워크) |
| **Focus Area (중점영역)** | 산업·사안에 특화된 거버넌스 | DevOps, 사이버보안, 디지털윤리, 클라우드, BCP, GDPR, AI(ISO/IEC 42001) |
| **Design Factor (설계인자)** | 거버넌스 체계를 조직에 맞춤 | 11개 인자(전략, 위험, 이슈, 위협, 컴플라이언스, 역할, IT 도입, 사이버보안계획, 사이버사고, 기술신규, 조직구성) -> 40개 목표 우선순위 결정 |

### 2. ITIL 4 Service Value System (SVS)와 34개 Practice

ITIL 4(2019, AXELOS)는 **Service Value Chain(SVC) 6단계(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve)**을 통해 34개 Practice(14 General + 17 Service + 3 Technical)를 운영한다. COBIT 2019와 ITIL 4의 매핑은 DSS01~05(Incident, Problem, Change, Service Request, Service Desk) 영역이 가장 밀접하다.

### 3. ISO/IEC 38500 IT 거버넌스 6원칙

이 국제표준은 **① Responsibility(책임)**, **② Strategy(전략)**, **③ Acquisition(획득)**, **④ Performance(성과)**, **⑤ Conformance(준수)**, **⑥ Human Behavior(인적행동)**의 6원칙을 제시하며, **Govern** 모델(Direct->Evaluate->Monitor)을 통해 이사회가 IT 의사결정에 개입하도록 명시한다. 영국(BS 31100), 호주(AS 8015), 일본(JIS X 0166)에 흡수되어 한국에서는 TTAS(Korean TTA 표준)로 도입 검토 중이다.

### 4. 거버넌스 KPI: Run/Grow/Transform 균형

McKinsey & Gartner가 제시하는 **70-20-10 모델**(70% 운영, 20% 성장, 10% 혁신)을 기준으로, 균형적 IT 포트폴리오 KPI를 산정한다.

- **Run KPI**: 시스템 가용성(99.95%), MTTR(Mean Time To Repair < 30분), MTTD(Mean Time To Detect < 1분), 변경 성공률(>97%), 1차 해결률(FCR > 70%), CSAT(>4.5/5)
- **Grow KPI**: 신규 기능 출시 리드타임(Lead Time for Changes < 1일), 배포 빈도(Deployment Frequency > 일 1회), NPS(Net Promoter Score)
- **Transform KPI**: 디지털 매출 비중(>20%), 신규 사업 Time-to-Market(<6개월), A/B 테스트 비율, AI 모델 운영 비율

**📢 섹션 요약 비유**: COBIT 5대 도메인은 **자동차의 5개 계기판(연료·속도·엔진회전수·온도·주행거리)**과 같다. EDM은 속도계(위에서 결정), APO는 네비게이션(경로 계획), BAI는 공장(차량 제작), DSS는 도로(운행 환경), MEA는 정비소(성능 점검)다. 40개 목표는 40개의 세부 센서 신호이며, 7대 구성요소는 차체, 엔진, 연료, 운전자, 운행규칙, 도로문화를 모두 고려하는 통합 시스템이다.

---

## Ⅲ. 비교 및 연결

### 1. COBIT 2019 vs ITIL 4 vs ISO 38500 vs PMBOK 7

| 구분 | COBIT 2019 | ITIL 4 | ISO/IEC 38500 | PMBOK 7 / PRINCE2 |
| :--- | :--- | :--- | :--- | :--- |
| **주체** | ISACA(정보시스템 감시·통제 협회) | AXELOS(PeopleCert) | ISO/IEC | PMI / AXELOS |
| **관점** | 거버넌스 + 관리 통합 | IT 서비스 운영(Value Co-Creation) | 이사회 거버넌스 6원칙 | 프로젝트 단위 실행관리 |
| **단위** | 40개 Governance/Management Objectives | 34개 Practice (3 카테고리) | 6 Principles + Govern Model | 8 Performance Domains / 7 Themes |
| **적용 범위** | 전사 IT + 비즈니스 |
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 523 / 800

<- **이전**: [522. IT 경영 관리 핵심 토픽 522번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/522_it_management_core_topic_522_exam_summary/)
**다음**: [524. IT 경영 관리 핵심 토픽 524번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/524_it_management_core_topic_524_exam_summary/) ->

---
