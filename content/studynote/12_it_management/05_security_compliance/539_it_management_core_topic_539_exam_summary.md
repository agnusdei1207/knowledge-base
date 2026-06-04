---
title: "539. IT 경영 관리 핵심 토픽 539번 시험 요약 (IT Management Core Topic 539 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019 기반 IT 거버넌스(Information & Technology Governance)는 40개의 거버넌스/관리 목표(Governance & Management Objectives)와 7대 구성요소(Components)를 통해 IT가 비즈니스 가치를 창출하도록 정렬(Alignment)·최적화(Optimization)하는 **이사회(Board)부터 현장(Operational)까지 단일화된 의사결정 체계**이다.
> 2. **가치**: 글로벌 조사에 따르면 COBIT 도입 조직은 **IT 투자 ROI 평균 18~25% 향상**, 중대한 IT 리스크 **42% 감소**, 컴플라이언스 감사 비용 **30% 절감**(ISACA 2022 Global Survey)하며, **ISO 27001·ISO 20000·PCIDSS·GDPR 다중 인증 매핑 효율**로 통제 항목 중복을 60% 이상 제거한다.
> 3. **판단 포인트**: 거버넌스 vs 관리의 분리(EDM: Evaluate-Direct-Monitor vs PBRM: Plan-Build-Run-Monitor) 적용, **조직 고유 디자인 팩터 11개**(전략, 목표, 위험, 문제, 위협, 컴플라이언스, 역할, IT 이슈, 기술 도입, 데이터, 외부 영향)를 통한 **맞춤형 거버넌스 시스템 설계**가 핵심이며, **커버리지 100% 추구가 아닌 리스크 기반 우선순위 결정**이 실무적 성공 요인이다.

---

## Ⅰ. 개요 및 필요성

기존 IT 관리는 CIO 산하의 **전술적(Tactical) 운영조직**이 애플리케이션·인프라·보안·서비스를 **사일로(Silo)** 단위로 관리해 왔다. 그러나 디지털 트랜스포메이션, 클라우드 전환, GDPR·개인정보보호법 강화, AI·생성형 모델의 도입 등으로 **이사회 수준(Board-level)의 의사결정 단위**가 IT 리스크와 가치를 통합적으로 다뤄야 하는 요구가 폭증했다. 한국에서 2022년 개인정보보호법 개정, 2023년 클라우드 보안인증制度(CSAP) 강화, 2024년 AI 기본법 제정 추진으로 **IT 거버넌스는 법적 컴플라이언스의 핵심축**이 되었다.

COBIT(Control Objectives for Information and Related Technologies)는 1996년 ISACA에서 발표된 이래 5개 메이저 버전(1996->1998 v2->2000 v3->2005 v4.5->2012 v5->**2019 v6**)을 거치며 단순 통제 프레임워크에서 **거버넌스 시스템 + 관리 시스템 + 설계 가이드라인**을 포괄하는 엔터프라이즈 거버넌스 프레임워크로 진화했다.

```text
            +------------------------------------------------------+
            |      Business Strategy & Value Realization          |
            |   (성장률, 시장점유율, EBITDA, ESG, 디지털전환 KPI) |
            +---------------------+--------------------------------+
                                  | Alignment(정렬)
                                  v
   +----------------------------------------------------------------------+
   |              I&T GOVERNANCE SYSTEM (COBIT 2019 Core)                 |
   |                                                                      |
   |   +------------------+         +----------------------+              |
   |   | 5 Governance Obj |         | 32 Management Obj    |              |
   |   |  (EDM: 5ea)      |  ---->   | (PBRM: APO-BAI-DSS-  |              |
   |   |                  |  Link   |  MEA)                |              |
   |   +--------+---------+         +----------+-----------+              |
   |            |                              |                          |
   |            v                              v                          |
   |   +------------------------------------------------------+          |
   |   |          7 Components (Governance System)             |          |
   |   |  ① 프로세스  ② 조직구조  ③ 정보흐름  ④ 사람/역량      |          |
   |   |  ⑤ 정책/원칙  ⑥ 문화/윤리  ⑦ 서비스/인프라/앱         |          |
   |   +------------------------------------------------------+          |
   |                                                                      |
   |   Design Factors (11개)  ->  Focus Areas (5개)  ->  Goal Cascade      |
   |   위험기반 우선순위화  ->  Capability Level (0~5)  ->  Maturity Gap   |
   +----------------------------------------------------------------------+
                                  | Performance Mgmt
                                  v
   +----------------------------------------------------------------------+
   |      Outcomes: Value( Benefit, Risk, Resource Optimization)          |
   +----------------------------------------------------------------------+
```

**기존 vs 신규 패러다임 비교**

| 항목 | 전통적 IT 운영(Pre-COBIT 2019) | COBIT 2019 기반 거버넌스 |
| :--- | :--- | :--- |
| 의사결정 주체 | CIO / IT 부서장 단독 | 이사회 -> 경영진 -> 운영의 3계층 |
| 목표 기준 | IT KPI (가용성, 성능) | 비즈니스 목표 ↔ IT 목표 Goal Cascade |
| 리스크 관리 | 부서별 개별 대응 | 통합 리스크 매트릭스 + 11개 Design Factor |
| 컴플라이언스 | 사후 점검식 | 설계 단계부터 By-Design 내재화 |
| 평가 체계 | CMMI 단일 모델 | CMMI + COBIT PAM(Process Assessment Model) 다중 |
| 적용 범위 | 온프레미스 단일 | 하이브리드/멀티클라우드/AI/IoT 포함 |
| 문화 | 통제 중심 | 가치·리스크·자원의 균형(Trade-off) |

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **"도시의 도시계획(Urban Planning)"**과 같다. 건물 한 채(애플리케이션)만 잘 짓는 것이 아니라, 상하수도·도로·전기·치안·재난대응(보안·리스크·컴플라이언스)까지 **도시 전체의 지속가능성**을 설계하는 것이 COBIT의 본질이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019의 아키텍처는 **Governance System(거버넌스 체계)** + **Governance Framework(프레임워크)** + **Components(구성요소)**의 3축으로 분리된다. 가장 중요한 구조는 **5단계 캐스케이드(Cascade)**이다: **Stakeholder Needs -> Enterprise Goals -> Alignment Goals -> Governance/Management Objectives -> Enablers(Components)**.

```text
   +--------------------------------------------------------------------+
   |  1. Stakeholder Needs  (이해관계자 요구)                            |
   |     "이익, 위험, 자원, 최적화의 균형"                                |
   +----------------------------+---------------------------------------+
                                v
   +--------------------------------------------------------------------+
   |  2. Enterprise Goals (13개 AG)                                      |
   |     AG01: 포트폴리오 경쟁제품 서비스  AG05: 고객서비스 제공         |
   |     AG08: 내부 비즈니스 프로세스 최적화  AG12: 디지털 변혁 관리     |
   |     AG13: 정보기반 자산 활용 극대화                                   |
   +----------------------------+---------------------------------------+
                                v
   +--------------------------------------------------------------------+
   |  3. Alignment Goals (13개 AG 연계)                                  |
   |     AG01↔비즈니스 I&T 만족  AG05↔I&T 서비스 품질  AG12↔변혁 역량    |
   +----------------------------+---------------------------------------+
                                v
   +--------------------------------------------------------------------+
   |  4. G&O Objectives (40개: EDM 5 + APO 14 + BAI 11 + DSS 6 + MEA 4)|
   |     EDM01: 거버넌스 프레임워크 설정/유지                             |
   |     EDM02: Benefit Delivery  EDM03: Risk Optimization              |
   |     EDM04: Resource Optimization  EDM05: Stakeholder Transparency  |
   |     APO12: Managed Risk  DSS02: Managed Service Requests & Incidents|
   |     DSS04: Managed Continuity  DSS05: Managed Security Services    |
   |     MEA01: Managed Performance & Conformance                        |
   |     MEA03: Managed Compliance with External Requirements            |
   +----------------------------+---------------------------------------+
                                v
   +--------------------------------------------------------------------+
   |  5. Components(7대 구성요소)가 Objective를 실현                       |
   |     ① 프로세스  ② 조직구조  ③ 정보  ④ 사람/기술/역량               |
   |     ⑤ 정책/원칙  ⑥ 문화/윤리/행동  ⑦ 서비스/인프라/애플리케이션    |
   +--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **① 프로세스 (Process)** | 40개 목표별 **Practice 4~6개**, Activity 단계별 정의 | **PAM(Process Assessment Model)** 기반 **Capability Level 0~5** 측정 (Level 0: 불완전 -> 1: 수행 -> 2: 관리 -> 3: 확립 -> 4: 예측 -> 5: 혁신). 예: APO12 위험관리 프로세스 = RA1 위험식별·분석 -> RA2 위험프로파일 작성 -> RA3 위험대응 계획 -> RA4 위험통신·보고 |
| **② 조직구조 (Organizational Structures)** | 의사결정권·책임·역할 정의 | **RACI 차트** 기반 Board, Audit Committee, CIO, CISO, CRO, Process Owner, Service Manager 책임 분배. **3 Lines of Defense** (1st: 운영라인, 2nd: 리스크/컴플라이언스, 3rd: 내부감사) 매핑 |
| **③ 정보 (Information Flows)** | 거버넌스 데이터 흐름 | **Input -> Process -> Output** 메타모델. 예: EDM02 Benefit Delivery의 Input=Enterprise Goals/Investment Portfolio, Output=Benefit Realization Report, KPI Dashboard |
| **④ 사람·기술·역량 (People, Skills, Competencies)** | BSC(Business Skills Continuum)와 **Skills & Capabilities Matrix** | COBIT 2019의 **7단계 Knowledge Area** (Governance/Management, Risk, Security, Audit, Quality 등). **SFIA 8** 또는 **e-CF(European e-Competence Framework)** 매핑으로 인력 스킬 매니페스트 작성 |
| **⑤ 정책·원칙 (Policies and Frameworks)** | 조직 정책과 절차서 | **Policy Hierarchy**: Corporate Policy -> IT Policy -> Standard -> Procedure -> Guideline 5계층. 예: 정보보안정책 -> 접근통제 표준 -> DB 권한 부여 절차 |
| **⑥ 문화·윤리·행동 (Culture, Ethics, Behavior)** | 거버넌스 성숙도 결정의 **연성요인** | **Tone at the Top**, **Code of Ethics**, **Whistle-blowing System**. 동기부여·리더십·협업·공정성 측정: 조직문화 진단(OCAI 모델) 연동 |
| **⑦ 서비스·인프라·앱 (Services, Infrastructure, Applications)** | 거버넌스 실현 기술 플랫폼 | GRC 도구(**Archer**, **ServiceNow GRC**, **SAP GRC**), ITSM(**Jira SM**, **ServiceNow**), 모니터링(**Splunk**, **Datadog**), IAM(**Okta**, **Keycloak**) 등 |

**핵심 알고리즘 및 산식**

- **Goal Cascade 점수화**: 각 AG(Enterprise Goal)와 Alignment Goal의 우선순위는 **Importance × Relevance 매트릭스**로 산정. Primary(1.0)/Secondary(0.8)/Tertiary(0.4) 가중치.
- **Capability Level 산정**: 각 Process의 NMG(Nominal Maturity Goal) = Σ(Process Activity Practice Score × Weight) / 7
- **Maturity Gap 분석**: Current Maturity(N) vs Target Maturity(M). Gap ≥ 2일 경우 우선 개선 대상으로 분류
- **Design Factor 가중치**: 11개 팩터의 영향력(I, Influence) 값 0~5 스케일, 임계값 3.0 이상 시 **고우선순위 Focus Area** 선정

- **📢 섹션 요약 비유**: 7대 구성요소는 **"오케스트라의 7개 악기 파티"**와 같다. 바이올린(프로세스)·드럼(조직)·악보(정보)·연주자(사람)·작곡가 지휘(정책)·무대 분위기(문화)·콘서트홀(서비스/인프라)이 모두 조화롭게 연주되어야 **교향곡(거버넌스 가치)**이 완성된다.

---

## Ⅲ. 비교 및 연결

IT 거버넌스는 단일 프레임워크로 완성되지 않는다. **COBIT이 "What"을**, **TOGAF가 "How to design"**을, **ITIL이 "How to operate"**를, **ISO 27001이 "How to secure"**를, **CMMI가 "How to mature"**를 정의한다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 27001:2022** | **CMMI-DEV v2.0** | **TOGAF 10** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **목적** | I&T 거버넌스/관리 | ITSM 실무 운영 | 정보보안 관리체계(ISMS) | 프로세스 성숙도 | EA 방법론 |
| **구조** | 40 G&O + 7 Components | 34 Practices (SVS) | Annex A 통제 93개 | 5 Maturity Level | ADM 8단계 사이클 |
| **평가** | COBIT PAM (Process) | Service Maturity | 인증 심사 (인증/유지) | SCAMPI A/B/C | Architecture Maturity |
| **강점** | 거버넌스 통합 뷰, 디자인 팩터 | Service Value Chain, 사용자 경험 | 글로벌 컴플라이언스, 법적 효력 | 엔지니어링 정량관리 | 비즈니스-기술 정렬 |
| **약점** | 구현 도구 미약, 학습 곡선 큼 | 거버넌스 레이어 부재 | 보안 외 영역 약함 | IT 도메인 외 적용 어려움 | 복잡, EA 산출물 표준화 어려움 |
| **연계
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 539 / 800

<- **이전**: [538. IT 경영 관리 핵심 토픽 538번 시험 요약](/studynote/12_it_management/05_security_compliance/538_it_management_core_topic_538_exam_summary/)
**다음**: [540. IT 경영 관리 핵심 토픽 540번 시험 요약](/studynote/12_it_management/05_security_compliance/540_it_management_core_topic_540_exam_summary/) ->

---
