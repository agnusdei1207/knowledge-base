---
title: "IT Management Core Topic 768 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 **COBIT 2019 거버넌스·목표 cascade, ITIL 4 Service Value System, ISO 38500 6원칙, EA(TOGAF ADM)**을 통합한 체계로서, 전략(Strategy)->포팅(Funding)->배치(Portfolio)->운영(Operation)->측정(Measurement)의 **5단계 가치사슬(Value Chain)**을 통해 정보기술을 비즈니스 성과와 연결하는 경영과학이다.
> 2. **가치**: 글로벌 연구(McKinsey 2023, Gartner 2024)에 따르면 성숙한 IT 거버넌스 도입 기업은 **정보화 투자 ROI 23~38% 향상**, **프로젝트 실패율 67% 감소**(PMI 2022 대비), **Time-to-Market 41% 단축**, **이행 비용 TCO 30% 절감** 효과를 달성하며, COBIT 2019 Maturity Level 4~5 도달 조직은 EBITDA 대비 IT 예산 비중 5~8% 적정 수준 유지가 가능하다.
> 3. **판단 포인트**: 핵심 의사결정 트레이드오프로 ① **Centralized vs Federated 거버넌스 모델**(COBIT의 집중형/분산형 RACI), ② **Build vs Run 예산 배분**(일반적으로 신규 30:운영 70 비율), ③ **Quick-Win vs Big-Bang 전환 전략**, ④ **Agile vs Plan-Driven** Delivery 모델(SAFe vs PRINCE2), ⑤ **내부 역량 vs 아웃소싱**(Make-or-Buy) 의사결정이 있으며, 이는 모두 **BABOK v3의 Elicitation·Strategy Analysis** 기법과 **Porter의 Value Chain 분석**에 근거한다.

---

## Ⅰ. 개요 및 필요성

IT 경영관리(Information Technology Management)는 1980년대 MIS(경영정보시스템) 시대를 거쳐 2000년대 IT 거버넌스(COBIT 4.0/5.0), 2010년대 디지털 전환, 2020년대 AI·클라우드 네이티브 시대를 거치며 **"IT 비용센터 -> 전략적 가치 동인(Strategic Value Driver)"**으로 패러다임이 전환되었다. 본 토픽(768번)은 정보관리기술사 시험의 핵심 영역으로, **IT 전략 기획 -> 정보화 투자 타당성 분석 -> EA 수립 -> IT 거버넌스 -> IT 성과관리 -> 디지털 전환**까지 엔드투엔드(End-to-End) IT 경영 사이클을 다룬다.

```text
+---------------------------------------------------------------------+
|           IT 경영관리 5단계 가치사슬 (IT Value Chain)                |
|                                                                     |
|  +----------+   +----------+   +----------+   +----------+        |
|  | ① 전략   |--->| ② 포팅  |--->| ③ 배치   |--->| ④ 운영   |--+     |
|  | Strategy |   | Funding  |   | Portfolio|   |Operation |  |     |
|  +----------+   +----------+   +----------+   +----------+  |     |
|       |             |              |              |          |     |
|       v             v              v              v          |     |
|  ·IT전략맵      ·Capex/Opex    ·프로젝트    ·ITIL 4 SVS         |     |
|  ·BSC 연동      ·TCO/ROI      ·우선순위화   ·SLA/SLM   |     |
|  ·EA 원칙       ·CBA 분석     ·PMO 운영    ·DevOps    |     |
|                                                              |     |
|                                              +----------+  |     |
|                                              | ⑤ 측정   |<--+     |
|                                              |Measure   |        |
|                                              +----------+        |
|                                                    |              |
|                                                    v              |
|                                  +--------------------------+    |
|                                  | Balanced Scorecard(BSC) |    |
|                                  | ·재무(Financial)         |    |
|                                  | ·고객(Customer)          |    |
|                                  | ·내부프로세스(Internal)  |    |
|                                  | ·학습성장(L&G)           |    |
|                                  +--------------------------+    |
|                                                                     |
|  +-------------------------------------------------------------+   |
|  | [상위 거버넌스 레이어]                                       |   |
|  |  ISO 38500 (6원칙) | COBIT 2019 (40 Governance              |   |
|  |  Responsibility, Strategy, Acquisition, Performance,        |   |
|  |  Conformance, Human Behavior) | ISO 27001/27002/38500       |   |
|  +-------------------------------------------------------------+   |
+---------------------------------------------------------------------+
```

기존 패러다임(Pre-2000)에서는 **IT 부서 중심의 수직적(Vertical) IT 관리**가 주류를 이루었으며, CIO(Chief Information Officer)가 **"데이터 처리 비용 최소화"**에 초점을 맞추었다. 그러나 2000년대 **사베인-옥스법(Sarbanes-Oxley Act, 2002)**과 **한국의 전자정부법(2001)/공공기관 정보화 사업 감리 규정**이 도입되면서 **컴플라이언스·리스크·투명성**이 핵심 화두로 부상하였고, 이후 **클라우드·모바일·빅데이터·AI** 등 4차 산업혁명 기술의 등장으로 **"디지털 비즈니스 플랫폼"** 기반의 새로운 IT 경영 프레임워크가 요구되고 있다.

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **대형 항공모함의 함교(CIC, Combat Information Center)**와 같습니다. 함교에서는 레이더(IS), 통신(IT), 무장(EA), 항공단(Service), 예산(Funding) 등 모든 것을 통합하여 **"최적의 진격 경로"**를 결정하며, IT 경영관리도 전략·예산·포트폴리오·운영·측정을 통합하여 **"비즈니스 가치 극대화 경로"**를 설계합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 핵심 아키텍처는 **3-Layer Governance Model**로 구성된다. 1) **최상위 의사결정 레이어**(이사회·CEO·CISO), 2) **중간 관리 레이어**(CIO·CDO·PMO·EA팀), 3) **실행 레이어**(프로젝트 매니저·DevOps 팀·IT 운영자)이다. 각 레이어는 **RACI Matrix**(Responsible, Accountable, Consulted, Informed)에 따라 책임이 명확히 분배되며, **COBIT 2019의 40개 거버넌스/관리 목표(Governance & Management Objectives)**가 이를 체계적으로 뒷받침한다.

```text
+--------------------------------------------------------------------+
|         IT 경영관리 통합 참조 모델 (Integrated Reference Model)   |
+--------------------------------------------------------------------+

[Layer 1: 전략·거버넌스 레이어]
+--------------------------------------------------------------+
|  Board of Directors / CEO / Audit Committee                  |
|  +- IT Steering Committee (ITSC)                              |
|  |  ·분기 1회 거버넌스 회의                                   |
|  |  ·BABOK v3 의사결정 분석                                   |
|  |  ·King III/IV 보고 원칙 준수                                |
|  +- Enterprise Risk Committee                                 |
|     ·ISO 31000, COSO ERM 2017 연계                           |
+--------------------------------------------------------------+
                              |
                              v
[Layer 2: 관리·조정 레이어]
+--------------------------------------------------------------+
|  CIO / CDO / CFO 협업 거버넌스                                |
|  +- IT 전략기획팀 (ISP, Information Strategy Planning)        |
|  |  ·3~5년 중장기 로드맵                                      |
|  |  ·SWOT, PEST, Porter's Five Forces                         |
|  |  ·CSF(Kritische Erfolgsfaktoren) 도출                     |
|  +- EA(Enterprise Architecture) 팀                            |
|  |  ·TOGAF ADM 10단계                                         |
|  |  ·ArchiMate 3.2 모델링                                     |
|  |  ·FEAF/DODAF 참조 모델                                     |
|  +- PMO(Project Management Office)                            |
|  |  ·PRINCE2 / PMBOK 7th / SAFe 6.0                          |
|  |  ·포트폴리오 Kanban 보드                                    |
|  |  ·Earned Value Management (EVM)                            |
|  +- 정보화 사업 감리 (감리법 제50조)                            |
|     ·사전·중간·사후감리                                         |
|     ·AaG(중요정보통신기반시설) 취약점 분석                       |
+--------------------------------------------------------------+
                              |
                              v
[Layer 3: 실행·운영 레이어]
+--------------------------------------------------------------+
|  비즈니스 부서 / 프로젝트팀 / 운영팀                           |
|  +- Agile Squad (Scrum/SAFe/LeSS)                              |
|  |  ·Product Owner, Scrum Master, Dev Team                    |
|  |  ·Jira/Confluence/ADO 협업툴                              |
|  +- DevOps/Platform Engineering                                |
|  |  ·CI/CD(GitHub Actions, GitLab CI, Jenkins X)             |
|  |  ·IaC(Terraform, Ansible, Pulumi)                          |
|  |  ·SRE(Site Reliability Engineering) - SLI/SLO/Error Budget|
|  +- IT 운영 (ITIL 4 SVS)                                       |
|  |  ·26가지 Practice (Change, Incident, Problem 등)           |
|  |  ·CMDB / Service Catalog / Knowledge Management           |
|  +- 보안/컴플라이언스 (ISO 27001/27701)                        |
|     ·ISMS-P / PIPL / GDPR / 개인정보보호법                    |
+--------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 거버넌스 프레임워크 (COBIT 2019)** | 이사회~운영까지 IT 의사결정 권한·책임·보고 체계 표준화 | 5개 도메인(EDM: Evaluate/Direct/Monitor + 4개 Align/Plan/Organize, Build/Acquire/Implement, Deliver/Service/Support, Monitor/Evaluate/Assess) + 40개 거버넌스/관리 목표 + **Focus Area**(예: 사이버보안, DevOps, 위험) 커스터마이징 + **Cascade Goal**(기업목표->정렬목표->거버넌스목표) |
| **IT 전략 기획 (ISP)** | 3~5년 중장기 정보화 전략·계획 수립 | u-ISMS, 전자정부법, 정보화진흥법 기반; **BPMN 2.0**으로 As-Is/To-Be 모델링; **Balanced Scorecard 4관점**(재무/고객/내부/L&G)으로 KPI 도출; **TOWS Matrix**로 전략 매트릭스 |
| **정보화 투자 분석 (CBA)** | 신규/대규모 정보화 사업의 경제성·정책·기술적 타당성 분석 | **NPV(순현재가치)**, **IRR(내부수익률)**, **B/C(편익/비용)비**, **Payback Period**; **TCO**(Total Cost of Ownership) 산정; 한국 정보화진흥원의 **시스템 비용 산정 가이드**(FP(Function Point)법, COCOMO II); AHP(Analytic Hierarchy Process) 의사결정 |
| **EA(Enterprise Architecture)** | 비즈니스·데이터·애플리케이션·기술 4계층의 통합 청사진 | **TOGAF ADM 8단계**(Preliminary->A: Vision->B: Business->C: IS->D: Technology->E: Opportunity->F: Migration->G: Implementation->H: Change Mgmt) + **ArchiMate 3.2**(Business/Application/Technology/Physical Layer); **Zachman Framework 6×6 매트릭스** |
| **IT 서비스 관리 (ITIL 4)** | IT 서비스의 기획·전환·운영·개선 End-to-End 거버넌스 | **Service Value System(SVS)**: Opportunity/Demand->Value->SVS(Plan/Improve/Engage/Design&Transition/Obtain/Build/Deliver&Support) + **34개 Practice**(Change, Incident, Problem, Service Desk, Continual Improvement 등) + **Four Dimensions**(Organization/People/Information/Technology/Partners/Value Streams) |
| **IT 성과 관리 (BSC & KPI)** | IT 성과 측정을 재무·비재무적으로 균형 있게 평가 | **BSC 4관점 KPI**; **IT Balanced Scorecard**(Nolan/Norton 2003); **Process Maturity Model**(CMMI 2.0 5단계); **COBIT Process Capability** (0~5 단계); **PRINCE2's Business Case** 지속 업데이트 |
| **프로젝트 포트폴리오 관리 (PPM)** | 다수 프로젝트의 우선순위화·자원배분·위험관리 | **SAFe Lean Portfolio Mgmt**; **PMI PfMP**; **Stage-Gate**(Cooper 1990) 모델; **MOSCOW**(Must/Should/Could/Won't) 우선순위; **Weighted Shortest Job First(WSJF)** = Cost of Delay / Job Duration |

각 구성 요소는 **King III/IV 보고 원칙**, **OECD 기업지배구조 원칙**, **한국 상법 제382조(이사회)**, **전자정부법 제11조(정보화 사업 추진)** 등의 법적·규범적 토대 위에 동작한다. 특히 **정보통신비 및 회계처리에 관한 지침**(미래창조과학부 고시)에서는 IT 자산을 **무형자산(Software)·유형자산(Hardware)·비용(인건비)**으로 분류하고, **회계감사 시 ICoFR(Internal Control over Financial Reporting)**을 요구한다.

- **📢 섹션 요약 비유**: IT 경영관리 아키텍처는 **신체 신경계(Neurological System)**와 같습니다. 대뇌(거버넌스)가 명령을 내리면 척수(중간관리)가 신경 신호를 변환하고, 말단 신경(실행레이어)이 근육(프로젝트)을 움직이며, 감각 기관(측정/KPI)이 피드백을 다시 대뇌로 전달합니다. 이 중 하나라도 망가지면 **온몸이 비틀어진 듯** 전체 비즈니스에 영향을 미칩니다.

---

## Ⅲ. 비교 및 연결

IT 경영관리 영역은 다수의 유사·경쟁 프레임워크가 존재하며, 기술사 시험에서는 이들의 **정확한 차이점과 상호 보완 관계**를 묻는 문제가 빈출된다.

| 구분 | **COBIT 2019** | **ITIL 4 (2019)** | **ISO 38500 (2014)** | **CMMI 2.0 (2018)** | **TOGAF 10 (2022)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스 & 관리 목표 체계 | IT 서비스 운영·전환·개선 | 이사회 수준 IT 거버넌스 6원칙 | 조직·프로세스 성숙도 평가 | EA 개발 방법론 (ADM) |
| **범위** | 전사 IT (End-to-End) | IT 서비스 운영 중심 | 상위 거버넌스 (전략 원칙) | 소프트웨어/시스템 공학 프로세스 | 4 EA 레이어(BM
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 768 / 800

<- **이전**: [767. IT 경영 관리 핵심 토픽 767번 시험 요약](/studynote/12_it_management/05_security_compliance/767_it_management_core_topic_767_exam_summary/)
**다음**: [769. IT 경영 관리 핵심 토픽 769번 시험 요약](/studynote/12_it_management/05_security_compliance/769_it_management_core_topic_769_exam_summary/) ->

---
