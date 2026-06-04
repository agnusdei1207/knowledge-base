---
title: "752. IT 경영 관리 핵심 토픽 752번 시험 요약 (IT Management Core Topic 752 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리(Information Technology Governance)는 COBIT 2019, ITIL 4, ISO/IEC 38500 등 글로벌 프레임워크를 기반으로 기업의 IT 자원을 전략·전술·운영 3계층으로 통합·최적화하여 비즈니스 가치(Value Realization)와 리스크 통제(Risk Optimization), 자원 효율(Resource Optimization)을 동시 달성하는 경영 체계임.
> 2. **가치**: McKinsey(2023) 조사에 따르면 성숙한 IT 거버넌스 도입 기업은 디지털 전환 ROI가 평균 35% 높고, 정보화 사업 실패율은 14%(PMBOK 미적용 67%)로 감소하며, IT 비용 대비 비즈니스 기여도(Business Value of IT, BVIT) 지표가 2.3배 향상됨.
> 3. **판단 포인트**: 중앙집중형(Centralized) vs 분산형(Distributed/Federated) 거버넌스 모델 선택, COBIT의 40개 Governance/Management Objective 중 어디까지 적용할지(Design Factors 11개 활용), 그리고 EA(Enterprise Architecture)와의 연계 수준(TOGAF ADM 적용 단계)에 따라 거버넌스 성숙도가 결정됨.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명 시대의 IT는 더 이상 단순 비용센터(COE, Center of Excellence)가 아닌 **전략적 비즈니스 파트너**로 진화했습니다. 2020년 이후 COVID-19 팬데믹,生成系 AI(LLM, MLLM)의 등장, 공급망 재편 등으로 인해 IT와 비즈니스 사이의 융합이 가속화되었고, 한국정보화진흥원(NIA)의 「2023 정보화 사업 시행 실태조사」에 따르면 전체 공공정보화 사업의 27.3%가 초기 계획 대비 예산을 초과하고 14.8%가 성과를 미달성한 것으로 나타났습니다. 이는 IT 투자의 **전략적 정렬(Strategic Alignment)**과 **성과 측정(Performance Measurement)** 부재가 근본 원인입니다.

IT 경영관리(Information Technology Management & Governance)는 이러한 문제를 해결하기 위해 **계획-실행-모니터링-평가**의 폐루프(Closed-loop) 체계를 구축하고, 이사회-경영진-IT 부서 간의 의사결정 구조를 명확히 하는 데 목적이 있습니다. 한국정보통신기술협회(TTA)의 ISMS-P, 정보통신산업진흥원의 IT-Biz-BMP(정보통신사업자 역량강화) 인증, 그리고 공공부문의 DGB(디지털정부혁신) 추진 등이 모두 이 프레임워크 위에서 운영됩니다.

```text
[IT 경영관리 3계층 구조 (전략-전술-운영)]

                    +---------------------------------+
                    |   Board / CEO / 이사회 (전략층)  |
                    |  - IT 전략(IT Strategy) 수립     |
                    |  - 디지털 전환(DX) 비전          |
                    |  - IT 투자 우선순위(Portfolio)    |
                    +---------------+-----------------+
                                    | BSC KPI 연계
                    +---------------v-----------------+
                    |   CIO / IT Steering Committee   |
                    |         (전술/관리층)            |
                    |  - EA(Enterprise Architecture)   |
                    |  - 정보화 사업 계획 및 예산 통제  |
                    |  - SLA/OLA 관리                 |
                    |  - 거버넌스 체계 운영(COBIT)     |
                    +---------------+-----------------+
                                    | Service Design
                    +---------------v-----------------+
                    |   IT Operations / DevOps        |
                    |         (운영층)                |
                    |  - ITIL 4 Service Value System  |
                    |  - Incident/Problem Management  |
                    |  - SIEM/SOC, 백업/DR 운영        |
                    |  - APM(APM Tools, Datadog 등)    |
                    +---------------------------------+
                                    ^
                                    | Monitor & Feedback
                                    | (PDCA: Plan-Do-Check-Act)
```

기존 패러다임은 IT를 "지원부서(Back Office)"로 인식하고, 개별 시스템 단위로 예산과 성과를 관리하는 **사일로(Silo)형 투자**였습니다. 그러나 현재는 클라우드 네이티브, SaaS, 데이터 레이크, AI/ML Ops 등 기술 스택이 복잡해지면서, **기업 아키텍처(EA) 기반의 포트폴리오 관리**와 **BizDevOps/GitOps**로 진화했습니다. 이는 Gartner(2024)가 강조한 "Continuous Compliance"와 "Adaptive Governance" 트렌드와도 부합합니다.

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **도시의 도시계획(Urban Planning)**과 같습니다. 건물(시스템) 하나하나 짓는 것이 아니라, 교통(데이터 흐름), 공원(데이터 거버넌스), 소방(보안), 상하수도(네트워크) 등 도시 전체의 인프를总体规划하고, 시민(사용자)에게 가치를 제공하는 것과 같은 원리입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 핵심은 **COBIT 2019**의 Governance System과 **ITIL 4**의 Service Value System(SVS)을 통합적으로 이해하는 것입니다. COBIT 2019는 40개의 관리 목적(Governance & Management Objectives, GMO)을 5개 도메인(EDM, APO, BAI, DSS, MEA)으로 분류하며, 각 목적은 Process Capability를 평가하기 위해 CMMI Institute의 PAM(Process Assessment Model)을 사용합니다.

ITIL 4는 2019년부터 Service Value System 체계를 도입하여 34개 Practice를 Guiding Principles(7개), Governance, Service Value Chain(6개 Activity: Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve), Continual Improvement, Practices로 재편했습니다. 핵심 메커니즘은 **Opportunity/Demand -> Value**로의 변환이며, 이를 위해 Portfolio Management(전략->프로젝트->서비스->자산 4단계)와 Demand Management(파이프라인 패턴)가 작동합니다.

거버넌스 의사결정 구조는 RACI 매트릭스와 의사결정 권한(Decision Rights)에 따라 **R(Responsible), A(Accountable), C(Consulted), I(Informed)**로 명확히 정의되어야 합니다. 특히 정보화 사업의 단계별 의사결정 Gate(예: G1 계획, G2 분석, G3 설계, G4 구축, G5 시험, G6 오픈, G7 안정화)는 한국정보화진흥원 표준 PMO 매뉴얼에서도 강조하는 핵심 절차입니다.

```text
[COBIT 2019 + ITIL 4 통합 거버넌스 흐름도]

  +----------+    +-------------+    +--------------+
  | Strategy |---->| Engagement  |---->| Design &     |
  | (전략)   |    | (관계/이해) |    | Transition   |
  | EDM      |    | APO/DSS     |    | (BAI)        |
  +----+-----+    +------+------+    +------+-------+
       |                  |                   |
       |                  |                   v
       |                  |           +--------------+
       |                  |           | Obtain/Build |
       |                  |           | (BAI03-04)   |
       |                  |           +------+-------+
       |                  |                  |
       |                  v                  v
       |           +-------------+    +--------------+
       |           | Deliver &   |<----|  Improve     |--+
       |           | Support     |    |  (Continual) |  |
       |           | (DSS)       |    +--------------+  |
       |           +------+------+                       |
       |                  |                              |
       v                  v                              |
  +-------------------------------------------------+    |
  |   MEA (Monitor, Evaluate, Assess) --------------+----+
  |   - KPI/CSF 측정 -> BSC 4관점(재무/고객/내부/학습)|
  |   - Internal Control & Audit Trail              |
  |   - Compliance (ISMS-P, GDPR, 개인정보보호법)     |
  +-------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Governance Body (이사회/CIO)** | 의사결정·감독·책임(RACI의 A) | IT Steering Committee 운영, Digital Ethics Charter 수립, Risk Appetite 정의(예: RTO 4hr, RPO 1hr) |
| **COBIT 2019 EDM(5개)** | 거버넌스 5대 영역(EDM01~05) | EDM01 Governance Framework Setting, EDM02 Benefits Delivery, EDM03 Risk Optimization, EDM04 Resource Optimization, EDM05 Stakeholder Transparency |
| **EA Framework (TOGAF ADM)** | 기업 아키텍처 8단계(ADM Cycle) | Preliminary->Vision->Business->Data/App/Technology->Opportunities->Migration->Implementation Governance->Change Management, ArchiMate 3.2 표기법 |
| **ITIL 4 SVS (34 Practice)** | 서비스 가치 사슬 운영 | Incident Mgmt(P1~P4 SLA), Change Enablement(CAB/ECAB), Service Desk(AI Chatbot + L1/L2), Problem Mgmt(Known Error DB) |
| **정보화 사업 PMO** | 사업 관리·품질·예산 통제 | 단계별 Gate Review(7단계), EV(Earned Value) 분석(CPI, SPI), WBS 기반 RAM(Responsibility Assignment Matrix) |
| **보안/컴플라이언스** | ISMS-P, PIMS, SOC2 | ISO/IEC 27001:2022(Annex A 93통제항목), ISO 27701, NIST CSF 2.0, K-ISMS-P 인증(3년 주기, 매년 감시) |
| **성과 측정(BSC)** | IT-BSC 4관점 KPI | 재무관점(ROI, TCO), 고객관점(CSAT, NPS), 내부프로세스(MTTR, 가용성 99.99%), 학습/성장(직원자격, 교육시간) |

핵심 알고리즘·산식으로는 **TCO(Total Cost of Ownership)**, **ROI(Return on Investment)**, **NPV(Net Present Value)**, **IRR(Internal Rate of Return)**, **EV(원가획득가치)**, **SPI/CPI** 등이 있습니다. EV 분석의 핵심은 EV = BAC × 완료율(%), CPI = EV/AC, SPI = EV/PV이며, CPI<1이면 예산 초과, SPI<1이면 일정 지연으로 판정합니다. 또한 정보화 사업의 성공 확률을 높이기 위해 **PMP/PMBOK 7th Edition**의 12 Principle과 **PRINCE2**의 7 Principle/7 Process를 적용합니다.

- **📢 섹션 요약 비유**: COBIT는 **헌법**, ITIL은 **행정절차법**, TOGAF는 **도시계획법**, ISMS는 **형법**과 같습니다. 기업이라는 나라에서 IT는 이 모든 법 체계의 지배를 받으며, 기술사(技術士)는 이 법들 사이의 충돌을 조율하고 최적의 운영체계를 설계하는 역할입니다.

---

## Ⅲ. 비교 및 연결

IT 경영관리 영역에서 자주 혼동되는 프레임워크 간 차이를 명확히 이해하는 것이 시험의 핵심입니다. COBIT 2019는 **거버넌스·관리 목적 달성**에 초점을 맞추고, ITIL 4는 **서비스 운영 최적화**, TOGAF는 **아키텍처 설계**, PMBOK은 **프로젝트 관리**, ISO 27001은 **보안 통제**에 집중합니다.

| 구분 | COBIT 2019 | ITIL 4 | TOGAF 10 | PMBOK 7th |
| :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스·리스크·컴플라이언스 | IT 서비스 관리(ITSM) | 기업 아키텍처(EA) 설계 | 프로젝트 관리 방법론 |
| **대상** | 이사회·CIO·감사인 | IT 운영·서비스 매니저 | EA 아키텍트·전략기획 | PM·PMO·사업팀 |
| **핵심 모델** | 40개 GMO, 11 Design Factors, 7 Component | SVS, 34 Practice, 7 Guiding Principle | ADM(8단계), Architecture Content Framework | 12 Principle, 8 Performance Domain |
| **측정 체계** | Process Capability(0~5), Maturity | SLA/OLA, KPI/CSF | ADM Phase Deliverable, Migration Plan | Earned Value(EV, CPI, SPI) |
| **도구 연계** | Process Assessment(PAM), Risk IT | ServiceNow, Jira Service Mgmt, BMC Helix | Archi(ArchiMate 도구), BiZZdesign, Avolution | MS Project, Primavera P6, OpenText PPM |
| **적용 시점** | 전략 수립·연간 거버넌스 리뷰 | 일일 운영·연속 개선 | 신규 사업·중장기 EA 로드맵 | 단위 프로젝트(임시적) |
| **컴플라이언스** | SOX, K-ICS, ISO 38500 연계 | ISO 20000:2018 | JTK(공공 EA), FEAF(연방 EA) | ISO 21502, ISO 21500 |
| **리스크 관리** | EDM03(Risk Optimization) 핵심 | Practice: Risk Mgmt | Migration Plan Risk | Risk Domain |
| **핵심 산출물** | Policies, Control Objectives | Service Catalogue, SLAs | Architecture Vision, Target Architecture | Project Charter, WBS, Risk Register |
| **성숙도 모델** | CMMI 5단계 + ISO 330xx PAM | ITIL Maturity Model | TOGAF Maturity Model | OPM3(Organizational PM Maturity) |

**다른 시스템과의 연계**는 다음과 같이 설계됩니다. 첫째, **Biz-DevOps 파이프라인**에서 COBIT의 BAI(Build, Acquire, Implement)와 ITIL의 Change Enablement가 GitLab CI/CD, ArgoCD, Jenkins와 연결됩니다. 둘째, **데이터 거버넌스**는 DAMA-DMBOK 2.0의 11개 지식 영역(Data Architecture, Data Modeling, Data Quality, Metadata, Data Security 등)과 COBIT의 APO14(Data Management)가 융합됩니다. 셋째, **클라우드 거버넌스**는 AWS Well-Architected Framework(5대 Pillars: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization), Azure CAF(Greenfield/Brownfield), GCP CAF와 COBIT이 매핑됩니다. 넷째, **AI 거버넌스**는 EU AI Act(2024), NIST AI RMF 1.0, 한국 AI 기본법(2026 시행 예정)과 연계됩니다.

```text
[IT 거버넌스 프레임워크 상호 연계 구조]

        +-----------------+
        |  ISO/IEC 38500  | <--- 최상위 거버넌스 원칙
        |  (Governance)   |
        +--------+--------+
                 |
     +-----------+-----------+
     v           v           v
  COBIT 2019  ISO 27001   ISO 20000
  (관리목표)   (보안통제)   (서비스관리)
     |           |           |
     +-----+-----+-----+-----+
           |           |
           v           v
      +--------+   +--------+
      | TOGAF  |   | ITIL 4 |
      |  (EA)  |   | (SVS)  |
      +----+---+   +---+----+
           |           |
           +-----+-----+
                 v
         +--------------+
         |   실행/운영    |
         | DevOps, SRE  |
         | AIOps, MLOps |
         +--------------+
```

- **📢 섹션 요약 비유**: COBIT, ITIL, TOGAF, PMBOK, ISMS는 마치 **오케스트라의 악기들**과 같습니다. COBIT은 지휘자(거버넌스), ITIL은 바이올린(서비스 운영), TOGAF는 작곡가(아키텍처
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 752 / 800

<- **이전**: [751. IT 경영 관리 핵심 토픽 751번 시험 요약](/studynote/12_it_management/05_security_compliance/751_it_management_core_topic_751_exam_summary/)
**다음**: [753. IT 경영 관리 핵심 토픽 753번 시험 요약](/studynote/12_it_management/05_security_compliance/753_it_management_core_topic_753_exam_summary/) ->

---
