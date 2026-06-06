---
title: "IT Management Core Topic 761 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Information Technology Governance & Management)는 COBIT 2019, ITIL 4, ISO/IEC 38500 프레임워크를 기반으로 IT 거버넌스·전략·포트폴리오·서비스·프로젝트·위험·성과를 **Value(가치) -> Risk(위험) -> Resource(자원)**의 3축으로 통합 운영하여, 기업의 전략적 목표와 IT 투자·운영·성장을 정렬(Strategic Alignment)시키는 경영 체계이다.
> 2. **가치**: McKinsey 2023 보고 기준 디지털 전환 성공 기업은 IT-Business Alignment 지수(EA Maturity × Strategy Fit)가 상위 25%일 때 EBITDA 마진이 14%p 높고, ITSM 자동화(Ansible+Tower+ServiceNow) 도입 시 MTTR(Mean Time To Restore) 평균 **68%** 단축, ITIL 4 Incident 분류 체계(P1~P4) 적용 시 SLA 준수율 **23%** 향상이 입증되었다.
> 3. **판단 포인트**: 거버넌스 모델 선택 시 **중앙집중형(Federal/Centralized)** vs **분산형(Decentralized/Center-led)** 의 트레이드오프, COBIT 2019의 **40 Governance & Management Objectives** 중 어떤 핵심 도메인(EDM: Evaluate, Direct, Monitor / APO: Align, Plan, Organize / BAI: Build, Acquire, Implement / DSS: Deliver, Service, Support / MEA: Monitor, Evaluate, Assess)을 우선 적용할지, 그리고 **Build vs Buy vs Rent(On-Premise vs Cloud vs SaaS)** 의사결정 시 TCO(5년) · IRR · NPV 분석이 핵심 쟁점이다.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명 시대를 맞아 기업 IT 시스템은 더 이상 비용센터(Cost Center)가 아닌 **전략적 가치 창출 센터(Value Center)**로 재정의되어야 한다. 과거 1990~2000년대 **Mainframe 중심의 단일 시스템**, 2000년대 **ERP(SAP R/3, Oracle EBS) 기반의 프로세스 통합**, 2010년대 **Cloud·Mobile·BigData 중심의 디지털 전환**, 그리고 2020년대 이후 **AI·Generative AI·Hyperautomation** 시대를 거치며 IT 관리 패러다임은 근본적으로 진화해왔다.

특히 한국 정보관리기술사 시험에서 빈번히 출제되는 **"IT 경영 관리"** 영역은 단순한 시스템 운영이 아닌, **거버넌스-전략-포트폴리오-아키텍처-서비스-프로젝트-위험-보안-성과**라는 9대 핵심 영역을 **End-to-End**로 연결하는 통합적 사고를 요구한다. 2024년 시행된 제65회 정보관리기술사 시험에서도 "AI 도입에 따른 IT 거버넌스 재설계" 및 "글로벌 멀티클라우드 환경의 BCP 전략" 등이 출제되어 **단순 암기형이 아닌 상황판단·아키텍처 설계형 문제**가 대세임을 확인시켜 주었다.

```text
+------------------------------------------------------------------+
|         IT 경영 관리 9대 핵심 영역 통합 프레임워크 (V-Model)       |
+------------------------------------------------------------------+
|                                                                  |
|  1. IT 거버넌스 (Governance)        -+                           |
|     COBIT 2019 / ISO 38500 / KING 4 |                            |
|  2. IT 전략 (Strategy)               |                            |
|     Ward & Peppard / BCG / McKinsey |                            |
|  3. IT 포트폴리오 (Portfolio)        |                            |
|     Application Portfolio Mgmt(APM) |                            |
|  4. EA (Enterprise Architecture)     +- [전략 정렬]                |
|     TOGAF / Zachman / FEAF          |      Alignment              |
|  5. ITSM (Service Management)       |                            |
|     ITIL 4 / ISO 20000             -+                            |
|  6. PMO & 프로젝트 관리              |                            |
|     PMBOK 7th / PRINCE2 / Agile    |                            |
|  7. IT 위험 관리 (Risk)               |                            |
|     ISO 27005 / NIST RMF           |                            |
|  8. 정보보안 거버넌스                 |                            |
|     ISO 27001/27002 / ISMS-P       |                            |
|  9. 성과 측정 (Performance)          -+                            |
|     KPI / BSC / IT Balanced Scorecard                            |
|                                                                  |
|  +---------+                              +---------+           |
|  | VALUE   | --- [Value Delivery] ---->    | RISK   |           |
|  | Benefits| <--- [Risk Optimization] --  | Security|          |
|  +----+----+                              +----+----+           |
|       |                                          |               |
|       +------------[RESOURCE]-------------------+               |
|                  Budget · People · Infra                          |
+------------------------------------------------------------------+
```

기존의 **사일로(Silo)형** IT 운영(개발팀, 운영팀, 보안팀이 독립적 활동)은 2010년대 들어 **"Two-Speed IT"**(Mode 1: 안정적 코어 시스템 / Mode 2: 빠른 디지털 혁신) 개념으로 진화했고, 현재는 **BizDevOps + SRE(Site Reliability Engineering) + FinOps + DevSecOps**가 융합된 **Multi-Modal IT 운영 모델**이 표준이 되었다. 따라서 기술사 응시자는 단순히 "ITIL 모범 사례"가 아닌, **"왜 그 기술을 선택했는가? 어떤 트레이드오프가 있는가? ROI는 어떻게 측정하는가?"**라는 **의사결정 프레임워크(Decision Framework)** 관점으로 사고해야 한다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **도시의 도시계획(Urban Planning)**과 같다. 개별 건물(시스템)만 잘 짓는 것이 아니라, 상하수도(데이터), 도로(네트워크), 치안(보안), 소방(이행), 민원센터(서비스 데스크), 예산(투자우선순위)을 **도시总体规划(Master Plan)** 아래 통합 설계해야 시민(사용자)이 안전하고 편리한 삶을 살 수 있다. COBIT 2019가 바로 도시기본계획이고, TOGAF가 토지이용계획, ITIL이 민원 운영 매뉴얼이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리 시스템은 **"전략 -> 거버넌스 -> 프로세스 -> 운영 -> 측정"**의 5계층 아키텍처로 구성된다. 각 계층은 PDCA(Deming Cycle) + Closed-loop Feedback으로 연결되며, 상위 계층의 정책이 하위 계층의 KPI로, 하위 계층의 측정값이 상위 계층의 의사결정으로 피드백되는 **양방향(Bi-directional) 제어 시스템**이다.

```text
+---------------------------------------------------------------------+
|       IT 경영 관리 5계층 아키텍처 (COBIT-Aligned V-Model)            |
+---------------------------------------------------------------------+
|  +----------------------------------------------------------+       |
|  | Tier 1: 전략 계층 (Strategy Layer)                       |       |
|  |  - Business Vision/Mission -> IT Vision/Mission           |       |
|  |  - IS Strategy(3~5yr) -> IT Roadmap -> Annual Plan        |       |
|  |  - Portfolio Prioritization(BCG Matrix)                  |       |
|  +-----------------+----------------------------------------+       |
|                    | Cascade (Balanced Scorecard)                    |
|  +-----------------v----------------------------------------+       |
|  | Tier 2: 거버넌스 계층 (Governance Layer)                 |       |
|  |  - COBIT 2019 EDM(EDM01~EDM05) + 35 MGMT Objectives     |       |
|  |  - Steering Committee(CEO+CTO+CFO+CDO)                   |       |
|  |  - 의사결정 권한 매트릭스(RACI)                          |       |
|  +-----------------+----------------------------------------+       |
|                    | Translate to Process                            |
|  +-----------------v----------------------------------------+       |
|  | Tier 3: 프로세스 계층 (Process Layer)                     |       |
|  |  - 10개 COBIT 도메인(EDM×5, APO×14, BAI×11, DSS×6, MEA×4)|      |
|  |  - 32개 ITIL 4 Practices(General×3, Service×17,         |       |
|  |                       Technical×7, Management×5)         |       |
|  |  - 핵심 프로세스: Change/Incident/Problem/Release/        |       |
|  |                  Service Level/Capacity/Availability     |       |
|  +-----------------+----------------------------------------+       |
|                    | Operationalize                                  |
|  +-----------------v----------------------------------------+       |
|  | Tier 4: 운영/기술 계층 (Operation/Tech Layer)             |       |
|  |  - ITSM 도구: ServiceNow, Jira Service Mgmt, BMC Helix  |       |
|  |  - 자동화: Ansible, Terraform, GitHub Actions, ArgoCD    |       |
|  |  - 모니터링: Datadog, Prometheus+Grafana, Splunk, ELK    |       |
|  |  - APM: New Relic, Dynatrace, AppDynamics                |       |
|  +-----------------+----------------------------------------+       |
|                    | Measure & Report                                |
|  +-----------------v----------------------------------------+       |
|  | Tier 5: 측정/개선 계층 (Measure/Improve Layer)            |       |
|  |  - KPI Tree: CSF -> KPI -> KGI(Goal Indicator)             |       |
|  |  - Maturity: CMMI(1~5), COBIT Maturity(0~5)             |       |
|  |  - Balanced Scorecard 4관점(Financial/Customer/         |       |
|  |     Internal Process/Learning & Growth)                  |       |
|  +----------------------------------------------------------+       |
+---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IS Steering Committee** | IT 거버넌스 최고 의사결정 기구 | CEO(의장), CIO, CFO, CISO, CDO, 사업본부장 구성, **월 1회 회의**, RACI 매트릭스 기반 의사결정, 주요 안건: 투자우선순위·M&A·리스크·규제 |
| **COBIT 2019 목표 체계** | 거버넌스/관리 목표의 40개 핵심영역 | **EDM(5개)**: Evaluate/Direct/Monitor / **APO(14)**: Align/Plan/Organize / **BAI(11)**: Build/Acquire/Implement / **DSS(6)**: Deliver/Service/Support / **MEA(4)**: Monitor/Evaluate/Assess, 각 목표는 **Process Practice + Activity + Metric** 3단위 |
| **ITIL 4 Service Value Chain** | 운영 서비스 가치 흐름 | 6개 Activity(**Plan->Improve->Engage->Design&Transition->Obtain/Build->Deliver&Support**)를 34개 Practices가 지원, **SVS(Service Value System)** 중심으로 4가지 차원(Organizations/People/Information/Technology/Partners/Value Streams) 고려 |
| **EA Repository (ArchiMate)** | 전사 아키텍처 통합 저장소 | **ArchiMate 3.2** 3 Layer(Business/Application/Technology) × 6 Aspect(Active/Behavior/Passive/Structure/Composition/Motivation), TOGAF ADM(8+1 Phase) 방법론, **메타모델 기반으로 EA-TO-BE -> EA-AS-IS Gap 분석** |
| **ITSM Tool (ServiceNow)** | 통합 서비스 운영 자동화 | CMDB(설정관리 DB) + Incident/Change/Problem + Knowledge Mgmt + Service Catalog + Service Portal을 **단일 PWA**로 통합, **IntegrationHub**로 200+ SaaS 커넥트, **Now Assist GenAI**로 자동 요약/해결 |
| **KPI 대시보드 (BSC)** | 성과 측정 및 의사결정 | 4관점(Financial/Process/Customer/Learning) × 4단계(CSF->KPI->Target->Actual) Cascade, **Power BI / Tableau** 시각화, **Grafana + Prometheus**로 실시간 DevOps 메트릭(CFR/Lead Time/MTTR/Change Fail Rate) |

이 5계층 아키텍처의 핵심 메커니즘은 **"Closed-Loop Feedback"**이다. 예를 들어 **"서비스 가용성 99.9% 미달"**이라는 사건이 발생하면:

1. **Tier 5(측정)**: KPI Breach Alarm 발생 -> MEA02(Monitor, Evaluate, Assess) 프로세스 트리거
2. **Tier 4(운영)**: APM(Datadog) + ITSM(ServiceNow)가 Incident 자동 생성, P1 Classification
3. **Tier 3(프로세스)**: DSS02(Manage Service Requests & Incidents) -> DSS04(Manage Continuity) -> DSS05(Manage Security Services) 실행
4. **Tier 2(거버넌스)**: EDM02(Ensure Benefits Delivery) -> EDM03(Ensure Risk Optimization) -> RACI에 따라 CISO/CIO에게 보고
5. **Tier 1(전략)**: 분기별 Steering Committee에서 재발방지 대책 및 포트폴리오 조정 의사결정

이 순환 구조는 **SLA Penalty/Incentive** 모델과 결합되어 운영팀의 **행동강령(Behavioral Contract)**으로 작동한다. 예: SLA 99.95% 달성 시 **연간 계약금의 5% 인센티브**, 미달 시 **1%p당 0.5% 패널티**.

- **📢 섹션 요약 비유**: IT 경영 관리 5계층은 **병원 시스템**과 같다. ① **전략 계층** = 병원장·이사회(장기적 의료 정책), ② **거버넌스** = 의료윤리위원회(품질·안전 의사결정), ③ **프로세스** = 진료·수술·입원 절차 매뉴얼(IL-4, COBIT), ④ **운영** = 실제 의사·간호사·의료장비(MRI/수술로봇), ⑤ **측정** = 환자 만족도·재입원율·감염률 지표(BSC). 병원평가(인증)가 5계층을 모두 통과해야 좋은 병원이듯, IT도 5계층이 모두 healthy해야 **Resilient & Sustainable** 하다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 영역에서 자주 혼동되는 **"거버넌스/관리/운영"**의 차이, 그리고 **"COBIT vs ITIL vs TOGAF vs PMBOK vs ISO 27001"** 프레임워크 간의 역할 분담을 명확히 이해해야 한다.

| 구분 | **COBIT 2019** (거버넌스) | **ITIL 4** (서비스 관리) | **TOGAF 10** (아키텍처) | **PMBOK 7th** (프로젝트) | **ISO 27001** (보안) |
|:---|:---|:---|:---|:---|:---|
| **핵심 목적** | IT 의사결정·책임·통제 (What/Why) | IT 서비스 운영·개선 (How for Ops) | 전사 아키텍처 설계 (How to design) | 프로젝트 성공 달성 (How to execute) | 정보보호 관리체계 (P-D-C-A for Security) |
| **대상 범위** | 전사 IT 전체 | 서비스 운영 조직 | Business/App/Data/Tech Layer | 단위 프로젝트 | 정보자산(ISMS) |
| **수직/수평** | 수직 (Top-Down) | 수평 (Service Value Chain) | 수직 (4 Layer) | 수평 (Project Lifecycle) | 수평 (Annex A 93 Controls) |
| **핵심 산출물** | 40 Governance/Management Objectives, Maturity Profile | 34 Practices
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 761 / 800

<- **이전**: [760. IT 경영 관리 핵심 토픽 760번 시험 요약](/studynote/12_it_management/05_security_compliance/760_it_management_core_topic_760_exam_summary/)
**다음**: [762. IT 경영 관리 핵심 토픽 762번 시험 요약](/studynote/12_it_management/05_security_compliance/762_it_management_core_topic_762_exam_summary/) ->

---
