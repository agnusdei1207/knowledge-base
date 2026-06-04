+++
title = "631. IT 경영 관리 핵심 토픽 631번 시험 요약 (IT Management Core Topic 631 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# 📘 기술사 시험 핵심 정리 — 631. IT 경영 관리 핵심 토픽

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스·정보화 사업 관리·디지털 전환(DT)·정보보안 경영체계(ISMS)·IT 아웃소싱을 통합한 **"전략-투자-실행-통제" 4축 IT 경영관리 프레임워크**로, COBIT 2019, ISO/IEC 38500, 디지털 서비스 표준, e-정부 표준프레임워크를 기반으로 조직의 IT 자산을 가치 극대화 방향으로 정렬(Alignment)하는 경영 체계이다.
> 2. **가치**: IT 투자 대비 ROI 20~35% 개선(Forrester, 2023), 정보화 사업 실패율 50%->15% 이하로 감소(Standish Group CHAOS Report 기준), IT 거버넌스 미도입 대비 컴플라이언스 비용 40% 절감, ISO 38500 적용 시 이사회-경영진-ICT 부서 간 의사결정 리드타임 60% 단축.
> 3. **판단 포인트**: ① 중앙집중형(CoE) vs 분산형(Federated) IT 거버넌스 모델 선택 ② Agile-Waterfall-DevSecOps 하이브리드 방법론 적용 여부 ③ 클라우드 네이티브 전환 시 CapEx->OpEx 전환율과 TCO 5년 회수 분석 ④ 내부 역량 유지율 70% vs 아웃소싱 의존도 30% 이내의 균형점 ⑤ 정보보안 통제 수준(기본/중요/핵심)에 따른 ISO 27001/27701/22301 다중 인증 전략.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명·AI·클라우드·제로트러스트 환경에서 IT는 더 이상 비용 센터(Cost Center)가 아닌 **전략적 가치 창출 센터(Strategic Value Center)**로 재정의되어야 한다. 그러나 한국 정보화 사업의 통계적 현실은 엄격하다: 2023년 전자신문·NIA 자료에 따르면 정보화 사업 예산은 약 9.2조 원 규모이나, 사업 실패·중단 비율은 35% 내외이며 일정이 평균 2.4배 초과된다. 또한 Gartner(2024) 보고에 따르면, **전 세계 기업의 78%가 디지털 전환을 추진하면서도 IT-비즈니스 정렬(Alignment) 부족을 1순위 장애요인**으로 꼽았다.

기존의 IT 관리 패러다임은 다음과 같이 진화해 왔다:

| 시대 | 패러다임 | 핵심 키워드 | 한계점 |
| :--- | :--- | :--- | :--- |
| 1990s | 데이터 처리 중심 | EDP, MIS | 업무 자동화 한정, ROI 불명확 |
| 2000s | ERP/시스템 통합 | SAP R/3, BPM, SOA | 비즈니스 변화 속도 미흡 |
| 2010s | 클라우드·모바일 우선 | SaaS, BYOD, Agile | 보안·거버넌스 사각지대 |
| 2020s~ | AI·데이터·플랫폼화 | DT, DataOps, MLOps, Zero Trust | 복합 규제, 기술 부채(Technical Debt) 누적 |
| 2025s~ | 자율·지능형 IT 운영 | AIOps, Self-healing, Sovereign Cloud | 인적 역량 갭, 윤리·법·리스크(GRC) |

본 토픽은 **"왜 IT 경영이 필요한가"**에 대해 ① IT-비즈니스 전략 정렬 ② IT 투자 의사결정의 투명성 ③ IT 리스크 통제 ④ 정보화 사업의 성공률 향상 ⑤ 컴플라이언스 준수 ⑥ 디지털 전환의 지속가능성이라는 6대 요구를 동시에 해결하는 **엔터프라이즈 IT 관리 체계(Enterprise IT Management Framework)** 구축을 다룬다.

```text
[ IT 경영 관리 4축 핵심 프레임워크 ]

                  +-----------------------------------------+
                  |   전략축(Strategy): IT-비즈니스 정렬       |
                  |   - 디지털 전환 로드맵(Digital Roadmap)    |
                  |   - 정보화 전략계획(ISP: Information Strategy Planning) |
                  |   - EA(Enterprise Architecture) 4A        |
                  +-----------------+-----------------------+
                                    |
                                    v
+----------------------------------------------------------------------+
|                                                                      |
|   +-------------+    +-------------+    +-------------+             |
|   |  전략축      |    |  투자축      |    |  실행축      |             |
|   | (Strategy)   |◄--►| (Investment) |◄--►| (Execution)  |             |
|   | - ISP/EA     |    | - TCO/ROI   |    | - Agile/DevOps|            |
|   | - 거버넌스    |    | - 포트폴리오 |    | - 방법론     |             |
|   | - 정책·표준  |    | - 우선순위   |    | - 성과측정   |             |
|   +------+------+    +------+------+    +------+------+             |
|          |                  |                  |                     |
|          +------------------+------------------+                     |
|                             v                                        |
|                  +-------------------------+                        |
|                  |    통제축(Control)        |                        |
|                  | - ISMS/PIMS/BCP         |                        |
|                  | - COBIT 2019            |                        |
|                  | - 내부통제·컴플라이언스   |                        |
|                  +-------------------------+                        |
|                                                                      |
+----------------------------------------------------------------------+
   [기대효과]  ROI 30%^ | 사업실패율 50%->15% | 의사결정 60% 단축
```

- **📢 섹션 요약 비유**: IT 경영 관리는 **"도시의 종합 운영 본부"**와 같다. 상하수도(데이터), 전력(인프라), 도로(네트워크), 경찰·소방(보안·컴플라이언스), 부동산 등록(거버넌스), 세수(투자ROI) 등을 한 시스템으로 통합 관리하지 않으면, 도시(기업)는 혼란과 비용 낭비 속에 무너진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **COBIT 2019 기반 5도메인 40거버넌스·관리목표 체계 + ISO/IEC 38500 6원칙 + 정보화 사업 관리 5단계(ISP-ITA-ISP2-시스템개발-운영) + ISMS 13개 도메인 102개 통제항목**의 통합이다. 이를 4계층 아키텍처로 표현하면 다음과 같다.

```text
[ IT 경영 관리 4계층 아키텍처 (Layered Architecture) ]

+----------------------------------------------------------------------+
|  Layer 1: 거버넌스·전략 계층 (Governance & Strategy Layer)          |
|  --------------------------------------------------------           |
|  • ISO/IEC 38500 6원칙 (Responsibility, Strategy, Acquisition,      |
|    Performance, Conformance, Human Behavior)                        |
|  • COBIT 2019: EDM(5) -> APO(14) -> BAI(11) -> DSS(6) -> MEA(4)         |
|  • EA(Enterprise Architecture): TOGAF 10 ADM / DoDAF / FEAF          |
|  • 디지털 전환 전략(Cloud First, Data Driven, AI First)            |
+--------------------------------+-------------------------------------+
                                 | <- Policy·Standard·Guideline
                                 v
+----------------------------------------------------------------------+
|  Layer 2: 투자·포트폴리오 계층 (Investment & Portfolio Layer)      |
|  --------------------------------------------------------           |
|  • 정보화 사업 예산 편성: BPR->ISP->TA->ISP2->개발->운영 5단계           |
|  • 투자평가: TCO(총소유비용), ROI, NPV, IRR, Payback Period          |
|  • 포트폴리오: BCG Matrix (Stars/Cash Cows/Question Marks/Dogs)     |
|  • 우선순위: MoSCoW(Must/Should/Could/Won't) + WSJF(Weighted Shortest|
|             Job First) — SAFe 프레임워크                           |
|  • 다중 프로젝트: PMO(Project Management Office) + PgMP             |
+--------------------------------+-------------------------------------+
                                 | <- 예산·우선순위·KPI
                                 v
+----------------------------------------------------------------------+
|  Layer 3: 실행·운영 계층 (Execution & Operations Layer)            |
|  --------------------------------------------------------           |
|  • 개발방법론: Waterfall(고정요구) -> Hybrid -> Agile(Scrum/Kanban) -> |
|              DevOps -> DevSecOps -> SRE -> AIOps                     |
|  • ITSM: ITIL 4 (Service Value System, 34 Practices)               |
|  • SLA: 가용성 99.9% (연 8.7h 장애), RTO/RPO 4h/15min              |
|  • CMMI: Level 1~5 (Initial->Optimizing)                            |
|  • 형상관리: Git, SVN / 빌드: Jenkins, GitLab CI, ArgoCD          |
+--------------------------------+-------------------------------------+
                                 | <- 서비스·인프라·데이터
                                 v
+----------------------------------------------------------------------+
|  Layer 4: 통제·보안·컴플라이언스 계층 (Control & Security Layer)    |
|  --------------------------------------------------------           |
|  • ISMS: ISO/IEC 27001:2022 (93통제), 27002, 27701(개인정보)       |
|  • BCP/DRP: ISO 22301, RTO/RPO/MTPD 정의                          |
|  • 내부통제: SOX 404, COSO 2013, J-SOX, ISAE 3402                  |
|  • 컴플라이언스: 개인정보보호법(PIPA), 전자금융거래법, GDPR,      |
|                 클라우드이용자보호법(2025.9 시행)                   |
|  • 리스크관리: ISO 31000, NIST CSF 2.0 (GV/ID/PR/RC/RS)            |
+----------------------------------------------------------------------+

[ 데이터 흐름 ]
   전략(Plan) -> 투자(Budget) -> 실행(Do) -> 측정(Check) -> 개선(Act)
   -> PDCA + COBIT RACI Matrix (Responsible, Accountable, Consulted, Informed)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **거버넌스 위원회** | 의사결정·감독 | 이사회 -> IT 전략위원회(Quarterly) -> IT 운영위원회(Monthly); ISO 38500 6원칙 중 Responsibility(책무)·Conformance(준법) 감독 |
| **EA(Enterprise Architecture)** | 전사 IT 토폴로지 모델 | TOGAF ADM 8단계(PD/VA/Opportunity/Solution/Migration/Impl/Governance/Change) 또는 DoDAF 8뷰; As-Is -> To-Be 갭 분석, 4A(BA/DA/AA/TA) 정합 |
| **PMO** | 다중 프로젝트 통합관리 | PgMP/Portfolio PMO / Program PMO / Project PMO 3계층; Earned Value Management(EVM): CPI, SPI, EAC 산출(CPI = EV/AC) |
| **DevSecOps 파이프라인** | 개발-배포-보안 자동화 | Plan->Code(SonarQube)->Build(Maven/Gradle)->Test(Selenium/JUnit)->Release(ArgoCD)->Deploy(Ansible/Terraform)->Monitor(Prometheus/Grafana); SAST/DAST/SCA/IaC 스캔 통합 |
| **ISMS 통제 체계** | 정보보호 관리체계 | ISO 27001 Annex A 93개 통제(2022 개정, 2013년 114개에서 14개 영역 93개로 통폐합); 4-tier 통제(정책/절차/지침/기록); 연 1회 위험평가 + ISMS-PIMS(27701) 통합 인증 |
| **ITIL 4 Service Value Chain** | 서비스 가치 창출 | Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve; 34 Practices (General/Service/Technical); SVS(Service Value System) 중심 |

### COBIT 2019 5도메인 40목표 핵심 매핑

| 도메인 | 약자 | 관리 목표 수 | 핵심 질문 | 연계 프레임워크 |
| :--- | :--- | :---: | :--- | :--- |
| EDM | Evaluate, Direct, Monitor | 5 | "IT가 제대로 되고 있는가?" | ISO 38500, COSO |
| APO | Align, Plan, Organize | 14 | "IT가 어떻게 정렬되는가?" | TOGAF, Balanced Scorecard |
| BAI | Build, Acquire, Implement | 11 | "IT 솔루션이 어떻게 만들어지는가?" | ITIL 4, PRINCE2 |
| DSS | Deliver, Service, Support | 6 | "IT 서비스가 어떻게 운영되는가?" | ITIL 4, ISO 20000 |
| MEA | Monitor, Evaluate, Assess | 4 | "IT 성과와 준법은 어떻게 평가되는가?" | ISO 27004, COBIT Cascade |

- **📢 섹션 요약 비유**: COBIT 2019는 **"비행기의 계기판"**이다. 고도(전략), 연료(투자), 엔진(실행), 캐노피(통제), 항법(측정) 모두를 통합 표시하지 않으면, 조종사(이사·CIO)는 올바른 의사결정을 내릴 수 없다. COBIT은 이 모든 계기를 40개로 표준화한 국제 공용 어휘이다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 27001 (ISMS)** | **PMBOK 7** | **발주자 관점 (정보화사업 지침)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스·관리 통합 | IT 서비스 관리 | 정보보호 관리체계 | 프로젝트 관리 표준 | 공공 정보화 사업 표준 |
| **발행기관** | ISACA | AXELOS (PeopleCert) | ISO/TC 27 | PMI | NIA(한국지능정보사회진흥원) |
| **핵심 구조** | 5도메인 40목표 | 34 Practices, SVS | 93 통제항목 (Annex A) | 12 Principle, 8 Domain | 5단계(ISP·TA·ISP2·개발·운영) |
| **강점** | 거버넌스·준법·평가지표
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 631 / 800

<- **이전**: [630. IT 경영 관리 핵심 토픽 630번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/630_it_management_core_topic_630_exam_summary/)
**다음**: [632. IT 경영 관리 핵심 토픽 632번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/632_it_management_core_topic_632_exam_summary/) ->

---
