---
title: "670. IT 경영 관리 핵심 토픽 670번 시험 요약 (IT Management Core Topic 670 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(Information Technology Governance)는 COBIT 2019의 40개 관리목표(EGM/DMF), ISO/IEC 38500의 6원칙(Direct, Evaluate, Monitor), ITIL 4의 34개 서비스관리 실무(SVP)를 통합하여 **기업의 IT가 비즈니스 전략(Strategic Alignment)을 통해 가치(Value Delivery)를 창출하고 위험(Risk Management)을 최적화하며 자원(Resource Management)을 효율적으로 운용**하는 의사결정 프레임워크다.
> 2. **가치**: McKinsey 2023 보고에 따르면 성숙한 IT 거버넌스 체계 도입 기업은 **IT 투자 대비 ROI가 평균 23~35% 향상**, 프로젝트 실패율 40% 감소, 사이버보안 사고 대응시간(MTTR) 평균 62% 단축, 감사 지적사항 78% 감소 등 정량적 효과를 나타내며, COSO 2013内部控制框架과의 정렬을 통해 ESG 공시 및 컴플라이언스(Regulation: GDPR, 개인정보보호법, 클라우드이용자보호법)를 자동화한다.
> 3. **판단 포인트**: **집중형(Centralized) vs 분산형(Federated) 거버넌스 모델**의 선택, **Three Lines Model(IIA 2020)** 적용 시 1·2·3라인의 역할 경계, COBIT 2019의 Design Factors 11개 항목을 통한 조직 맥락별 거버넌스 시스템 튜닝, 그리고 **프로세스 역량 vs 목표 계단형(Goals Cascade)**의 우선순위 트레이드오프가 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

정보기술의 전략적 가치가 단순 비용센터(Cost Center)에서 비즈니스 전략의 핵심 동력으로 전환되면서, IT 투자의 의사결정 권한과 책임 소재를 명확히 하는 **IT 거버넌스**는 CEO와 이사회(Board)의 직접 관할 영역이 되었다. ISO/IEC 38500:2015는 "이사회가 조직의 IT 사용을 지시·감독·모니터링함으로써 책임지는 통치 구조"라고 정의하며, 단순히 IT 부서의 관리가 아닌 **전사적 거버넌스(Enterprise Governance of IT, EGIT)** 관점을 강조한다.

1990년대 말~2000년대 초반 IT 거버넌스 개념이 정립된 배경에는 **사베린(Sabatext) 사건, 엔론(Enron) 사태, 월드컴(WorldCom) 분식회계** 등 IT 시스템이 회계 부정과 직결된 대형丑闻이 촉매제가 되었다. 이로 인해 SOX법(Sarbanes-Oxley Act, 2002) Section 404가 요구하는 IT 통제 항목이 구체화되었고, ITGI(IT Governance Institute, 현재 ISACA 산하)에서 COBIT이 탄생했다. 한국에서는 **전자정부법(2007)**, **클라우드컴퓨팅법(2012)**, **정보통신망법**, **개인정보보호법(2011)** 등의 규제 환경 변화로 IT 거버넌스의 법적 의무화가 가속화되었다.

```text
   [Board of Directors / 이사회]                  <- 최상위 의사결정 기구
              |
              | 거버넌스 지시 (Direct)
              | 성과 평가 (Evaluate)              <- ISO/IEC 38500 6원칙 적용
              | 모니터링 (Monitor)
              v
   +--------------------------+
   | IT Steering Committee    |                  <- CxO 레벨 거버넌스 회의체
   | (IT전략위원회)             |
   | - CIO, CFO, CEO, COO     |
   | - 주요 안건: 투자우선순위,  |
   |   위험 식별, 컴플라이언스    |
   +--------------------------+
              |
              +----------------------+
              v                      v
   +-----------------+     +------------------+
   | Strategy Layer  |     |  Operating Layer |
   | (전략 계층)       |     |  (운영 계층)        |
   |                  |     |                  |
   | • IT Strategy    |     | • Service Desk   |
   | • Portfolio Mgmt |     | • Incident Mgmt  |
   | • Architecture   |     | • Change Mgmt    |
   | • Innovation     |     | • Problem Mgmt   |
   |   (Digital Twin) |     | • SLA Monitoring |
   +-----------------+     +------------------+
              |                      |
              +----------+-----------+
                         v
              +----------------------+
              |  Three Lines Model    |  <- IIA 2020
              | 1st: Business Ops    |     1라인: 비즈니스 오너
              | 2nd: Risk & Compliance|    2라인: 리스크/컴플라이언스
              | 3rd: Internal Audit  |     3라인: 내부감사
              +----------------------+
```

기존의 **IT 관리(Management)**가 "기술을 어떻게 효율적으로 굴릴 것인가"의 관점이라면, **IT 거버넌스**는 "기술을 통해 조직의 목적 달성을 어떻게 책임지고 보장할 것인가"의 관점이다. 즉, 관리(Management)는 **효율(Efficiency)**, 거버넌스(Governance)는 **효과(Effectiveness)와 책임(Accountability)**에 초점을 맞춘다. 이는 전통적 IT 운영체제(예: BMC Remedy, Tivoli)에서 탈피해 **GRC(Governance, Risk, Compliance) 통합 플랫폼**(예: SAP GRC, ServiceNow GRC, Archer GRC)으로 진화하는 흐름을 낳았다.

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **배의 키잡이(steering)** 와 같다. 엔진룸(IT 운영)에서는 보일러를 효율적으로 태우지만, 키잡이는 어디로 항해할지(전략), 바람과 조류(리스크)는 어떤지, 항해 규정(컴플라이언스)은 어떻게 지키는지 결정한다. 키잡이가 없으면 보일러는 아무리 강해도 암초에 부딪힌다(프로젝트 실패).

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 거버넌스의 기술적 핵심은 **"누가(Who) 무엇을(What) 언제(When) 어떻게(How) 결정하고, 그 결과를 어떻게 측정(Measure)할 것인가"** 를 메타데이터와 프로세스로 명세화하는 것이다. 이를 위해 COBIT 2019는 5개 도메인 × 40개 관리목표(Management Objective), 7개 컴포넌트(Components), 11개 설계인자(Design Factors)로 구성된 **Governance & Management Objectives 체계**를 제시한다.

```text
            +-------------------------------------+
            |  COBIT 2019 Core Model (40 Objectives)|
            +-------------------------------------+
              |           |           |           |
   +----------+--+  +-----+----+  +---+----+  +--+---------+
   |  EDM Domain |  |  APO     |  |  BAI   |  |  DSS       |  | MEA |
   | (5 Goals)   |  | (14 Goals)|  |(11 Goals)|  | (6 Goals)  |  |(4)|
   |             |  |          |  |        |  |            |  |   |
   | • EDM01     |  | • APO01  |  | • BAI01|  | • DSS01    |  |   |
   |  Governance |  |  IT Mgmt |  |  Progm |  |  Operation |  |   |
   |  Framework  |  |  Framework| |  Mgmt  |  |            |  |   |
   | • EDM02     |  | • APO02  |  | • BAI02|  | • DSS02    |  |   |
   |  Benefits   |  |  Strategy |  |  Reqmt |  |  Service   |  |   |
   |  Delivery   |  |  & Portfolio| |  Mgmt  |  |  Request   |  |   |
   | • EDM03     |  | • APO04  |  | • BAI03|  | • DSS05    |  |   |
   |  Risk Opt   |  |  Innov.  |  |  Sol.  |  |  Security  |  |   |
   | • EDM04     |  | • APO12  |  |  Build |  |   Mgmt     |  |   |
   |  Resource   |  |  Risk    |  | • BAI09|  |            |  |   |
   |  Opt.       |  |  Mgmt    |  |  Asset |  |            |  |   |
   | • EDM05     |  | • APO13  |  |  Mgmt  |  |            |  |   |
   |  Stakeholder|  |  Security|  |        |  |            |  |   |
   |  Transp.    |  |  Mgmt    |  |        |  |            |  |   |
   +-------------+  +----------+  +--------+  +------------+  +---+
            |            |              |              |          |
            +------------+------+-------+--------------+----------+
                                v
                  +--------------------------+
                  |  7 Components of          |
                  |  Governance System        |
                  |  ---------------------    |
                  |  1. Processes             |
                  |  2. Organizational Struct. |
                  |  3. Information Flows     |
                  |  4. People, Skills,       |
                  |     Competencies          |
                  |  5. Policies & Procedures |
                  |  6. Culture, Ethics,      |
                  |     Behavior              |
                  |  7. Services, Infra.,     |
                  |     Applications          |
                  +--------------------------+
                                |
                                v
                  +--------------------------+
                  |  11 Design Factors        |  <- 조직별 맞춤 튜닝
                  |  ---------------------    |
                  |  DF1: Enterprise Strategy |
                  |  DF2: Enterprise Goals    |
                  |  DF3: Risk Profile        |
                  |  DF4: I&T Related Issues  |
                  |  DF5: Threat Landscape    |
                  |  DF6: Compliance Req.    |
                  |  DF7: Role of IT         |
                  |  DF8: IT Sourcing Model   |
                  |  DF9: IT Implementation   |
                  |  DF10: Technology Adopt.  |
                  |  DF11: Size of Enterprise |
                  +--------------------------+
```

핵심 메커니즘을 단계별로 살펴보면 다음과 같다.

**1단계: 거버넌스 시스템 설계(Design)** — 11개 Design Factor를 조직의 맥락(Strategy, Goals, Risk, Compliance 등)에 따라 점수화하고, 이를 40개 관리목표의 **우선순위(Priority)와 역량수준(Target Capability Level: 0~5)** 으로 변환한다. Capability Level은 ISO/IEC 15504-2 SPICE 모델을 차용하여 0(Incomplete)~5(Optimizing) 6단계로 평가한다.

**2단계: 목표 계단(Goals Cascade) 연결** — 13개 Enterprise Goals -> 13개 Alignment Goals(예: AG01: I&T compliance & support for business) -> 40개 Management Objective로 위계적 연계. 이를 통해 **"비즈니스 KPI ↔ IT KPI"** 의 인과관계가 명확해진다. 예: Enterprise Goal "Portfolio of competitive products/services" -> AG09 "Delivering programs on time, on budget, meeting quality" -> BAI01 "Managed Programs" -> KPI: % On-Time Delivery, Cost Variance Index(CVI), Defect Density.

**3단계: 프로세스 평가(Process Assessment)** — COBIT PAM(Process Assessment Model)을 활용하여 **Process Capability Rating**(0~5)을 측정하고 갭 분석(Gap Analysis) 후 개선 로드맵 도출. PA 2.1 ~ 2.5(Governance) 및 EDM 5개 영역을 우선 점검.

**4단계: 모니터링 및 개선(Measure & Monitor)** — MEA 도메인의 MEA01(Performance & Conformance Monitoring), MEA02(System of Internal Control), MEA03(Compliance with External Requirements), MEA04(Assurance)을 통해 **CSF(Critical Success Factors)와 KGI(Key Goal Indicators), KPI(Key Performance Indicators)** 를 설정하고 CSF/KGI/KPI 트리거 기반 보고 체계 운영.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(Evaluate, Direct, Monitor)** | 거버넌스 의사결정 | 이사회·IT전략위원회에서 수행. 비즈니스-기술 정렬, ROI/ROA 산정(예: BSM: Benefit Satisfaction Metric), RTO/RPO 기준 위험허용수준(Tolerance) 결정 |
| **APO(Align, Plan, Organize)** | 전략 정렬·계획 | I&T 전략 3~5년 로드맵, 포트폴리오 우선순위(점수화 모델: 전략적 적합성 30% + 재무성과 25% + 위험 20% + 규제 15% + 시급성 10%), 아키텍처(TOGAF 10 ADM), 재무관리(ITFM: IT Financial Management - TBM 기반) |
| **BAI(Build, Acquire, Implement)** | 솔루션 수명주기 | 요구사항(BABOK v3), 설계, 개발(SAFe/DevOps), 테스트(테스트 피라미드, Mutation Testing), 배포(CI/CD: Jenkins/GitHub Actions), 변경관리(CAB: Change Advisory Board) |
| **DSS(Deliver, Service, Support)** | 운영·서비스 | ITIL 4 Service Value System(SVS): Service Desk(생성형 AI 챗봇), Incident/Problem Mgmt(ITIL 4 2nd Shift Left), Service Level Mgmt(SLA 99.9% / XL Deploy 99.99%) |
| **MEA(Monitor, Evaluate, Assess)** | 성과·컴플라이언스 | 내부통제(SOX 404, ISAE 3402), ISO 27001 통제 매핑, 성과보고 대시보드(예: Power BI + CMMI 성과 지표), 감사 자동화 |
| **Three Lines Model (IIA 2020)** | 책임·리스크 분리 | 1라인: 업무 수행(제1방어선, Operational Mgmt), 2라인: 리스크·컴플라이언스·IT 거버넌스 부서(제2방어선, Risk Mgmt), 3라인: 내부감사(제3방어선, Internal Audit) — 독립성 보장을 위한 **임원보고 라인** 명세 |
| **Risk & Security Overlay** | 위험·보안 통합 | ISO 27005 위험평가, NIST CSF 2.0(2024)의 Govern/GI/ID/PR/DE/RS/RC, Zero Trust Architecture(NIST SP 800-207) |
| **Design Factor Tuner** | 조직 맞춤 튜닝 | 11개 DF에 가중치 적용, RACI 매트릭스 자동 생성, 우선관리목표(Priority) 산출 -> 40개 목표 중 **상위 10~15개** 집중 |

특히 **TBM(Technology Business Management)** 프레임워크(TBM Council)는 IT 비용을 4계층 모델(Layer 1: IT Cost ~ Layer 4: Business Value)로 분해하여 **Cost per 사용자, Cost per 거래, Cost per 서비스** 등 서비스 단위 원가회계(Activity-Based Costing, ABC)를 가능케 한다. 이를 통해 **"어떤 IT 서비스가 어떤 사업부(LOB)에 얼마의 가치를 제공하는가"** 를 정량화할 수 있다.

- **📢 섹션 요약 비유**: COBIT의 40개 관리목표는 마치 **종합병원 40개 임상과** 와 같다. EDM은 원
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 670 / 800

<- **이전**: [669. IT 경영 관리 핵심 토픽 669번 시험 요약](/studynote/12_it_management/05_security_compliance/669_it_management_core_topic_669_exam_summary/)
**다음**: [671. IT 경영 관리 핵심 토픽 671번 시험 요약](/studynote/12_it_management/05_security_compliance/671_it_management_core_topic_671_exam_summary/) ->

---
