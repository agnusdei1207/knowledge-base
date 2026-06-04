+++
title = "798. IT 경영 관리 핵심 토픽 798번 시험 요약 (IT Management Core Topic 798 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# 798. IT 경영 관리 핵심 토픽 — IT 거버넌스(COBIT 2019 기반) 심화

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 ISO/IEC 38500의 6원칙(책임·전략·취득·성과·규율·인간행위)과 COBIT 2019의 40개 Govern/Manage Objective를 통해 **이사회(Govern)->경영진(Manage)->운영(Operate)** 의 3-layer 책임 구조에서 가치창출, 위험최적화, 자원최적화의 3대 균형점(EGT: Enterprise Goals)을 달성하는 의사결정 및 통제 체계이다.
> 2. **가치**: McKinsey(2022) 기준 성숙 IT 거버넌스 도입 기업은 EBITDA 마진 3\~7% 상승, PMI(2021) 프로젝트 성공률 71%->82% 개선, IT 비용 20\~30% 절감, 컴플라이언스 감사 소요시간 50%v(GDPR·ISMS-P 기준), 의사결정 리드타임 40% 단축.
> 3. **판단 포인트**: 중앙집중형(Federal·CoE: Center of Excellence) vs 분산형(Federated·Biz-led IT) 구조 선택, Risk Appetite 설정의 정량화, Agile/DevOps의 거버넌스 통합(Governance-as-Code), CapEx-Heavy vs OpEx-Cloud 전환의 재무구조 영향, ROI·NPV·IRR·TCO 기반의 정량 평가 체계 적용 여부.

---

## Ⅰ. 개요 및 필요성

IT 거버넌스(Information Technology Governance)는 1999년 ITGI(ISACA 산하) 창설 이후 **COSO ERM**(내부통제), **ITIL v4**(서비스관리), **ISO 27001**(보안), **TOGAF/Zachman**(EA) 등 다양한 프레임워크가 혼재하는 환경에서, **단일 의사결정 권위(Decision Rights)와 책임 구조(Accountability Structure)** 를 정의하는 핵심 메타-프레임워크(Meta-Framework)로 진화해 왔다.

특히 2020년 이후 **클라우드·AI·데이터 거버넌스** 가 결합되면서, IT 거버넌스는 단순 IT 통제를 넘어 **Digital Governance·Data Governance·AI Ethics Governance** 까지 확장되었다. COBIT 2019는 이전 COBIT 5(2012)의 Process 모델을 탈피하고, **40개 Governance/Management Objective × 5개 도메인(EDM·APO·BAI·DSS·MEA)** 의 유연한 Focus Area(Focus Area: SME·Risk·Cybersecurity·DevOps·Digital Transformation) 구조로 재설계되었다.

기존 패러다임(Pre-2010)은 **사일로(Silo)형 통제** — 재무·보안·컴플라이언스·IT 운영이 각각 별도 절차로 운영되어 중복 비용 20\~30% 발생, 책임 공백(RACI 미정의) 빈번 발생. 새로운 패러다임(2019~)은 **통합 거버넌스 체계** — 단일 SoR(System of Record: SAP GRC·Archer·ServiceNow GRC)에서 모든 통제·위험·이벤트를 실시간 통합 관리.

```text
[ IT 거버넌스 의사결정 흐름도: 3-Tier 책임 구조 ]

   +-------------------------------------------------------+
   |  Tier 1: GOVERN  (이사회·감사위원회·CEO)                 |
   |  -----------------------------------------------------  |
   |  • EDMS(EDM01~05) : 전략수립·위험감독·자원배분·성과감시 |
   |  • 책임: "무엇을(What)" 의사결정, 권위(Authority) 보유   |
   |  • 산출물: 전략계획서·위험허용도·예산 한도(Guardrails)  |
   +---------------------+---------------------------------+
                         | 정책·한도·KPI 위임(Delegation)
                         v
   +-------------------------------------------------------+
   |  Tier 2: MANAGE  (CIO·CDO·CISO·BPO)                  |
   |  -----------------------------------------------------  |
   |  • APO(APO01~14) : 전략·포트폴리오·아키텍처·혁신       |
   |  • BAI(BAI01~11) : 변경·수용·구축·전환·성능·모니터     |
   |  • DSS(DSS01~06) : 운영·인시던트·연속성·보안서비스     |
   |  • MEA(MEA01~04) : 성능평가·내부통제·외부감사·컴플     |
   |  • 책임: "어떻게(How)" 계획·자원할당·우선순위화         |
   +---------------------+---------------------------------+
                         | 실행지시(Service Request·Change)
                         v
   +-------------------------------------------------------+
   |  Tier 3: OPERATE  (실무팀·DevOps·SRE·SOC)              |
   |  -----------------------------------------------------  |
   |  • ITIL 4 Service Value Chain : Plan->Engage->Design     |
   |    ->Obtain/Build->Deliver/Support                        |
   |  • 책임: SLA 준수, Incident/Problem 처리, Change 적용  |
   +-------------------------------------------------------+

   [Feedback Loop]  KPI·KRI·KCI -> MEA -> Govern 의사결정 반영
```

- **📢 섹션 요약 비유**: IT 거버넌스는 도시의 **도시계획(Govern) -> 시 행정(Manage) -> 소방·경찰·도로운영(Operate)** 의 3-tier 책임 분배와 같다. 시장은 "어디에 도로를 낼지" 결정하고, 행정은 "예산·설계·발주"하며, 소방관은 "신호·통제·대응"을 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019의 핵심 메커니즘은 **Cascade(연쇄) 원칙** 과 **Components of a Governance System(7가지 구성요소)** 이다. 모든 Governance/Management Objective(GO/MO)는 7개 구성요소의 인스턴스화(Instantiation)로 설계된다.

```text
[ 7 Components of Governance System — 정보 흐름 ]

   +----------------------------------------------------------+
   |                    CASCADE FLOW                          |
   |                                                          |
   |  Enterprise Goals (13) — Stakeholder Value                |
   |         |   Alignment Risk-Treated to Value              |
   |         v                                                |
   |  Alignment Goals (13 IT-related)                         |
   |         |                                                |
   |         v                                                |
   |  Governance/Management Objectives (40)                   |
   |    EDM(5) | APO(14) | BAI(11) | DSS(6) | MEA(4)         |
   |         |                                                |
   |         v                                                |
   |  Components (7 categories) ------+                       |
   |    1. Process                      |                      |
   |    2. Organizational Structures    |                      |
   |    3. Information Flows            |   Purposes          |
   |    4. People, Skills & Competence  |  (내부연결)         |
   |    5. Policies & Procedures        |                      |
   |    6. Culture, Ethics & Behavior    |                      |
   |    7. Services, Infrastructure & Apps|                    |
   |         |                                                |
   |         v                                                |
   |  Focus Areas (SME, Risk, Cyber, DevOps, Privacy, AI...)   |
   +----------------------------------------------------------+

   [핵심 공식: 거버넌스 = 가치창출 × 위험최적화 × 자원최적화 / 책임공백 ]
   [검증: Capability Level 0~5 (ISO/IEC 15504 PAM 기반, 0=Incomplete~5=Optimizing)]
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Process (40 GO/MO)** | 통제 활동·책임·실무 절차 | COBIT 2019 Process Reference Model. 각 Process는 6\~7개 Practice(과거 Activity), 각 Practice는 Input/Output(Base Practice)을 가짐. 예: DSS02(보안서비스) -> DSS02.01~.06 |
| **Organizational Structure** | 의사결정 권위·보고 계층 정의 | 이사회-감사위-CEO-CIO-CISO-CDO. **RACI**(Responsible·Accountable·Consulted·Informed) 차트로 역할 매핑. RACI 충돌 시 Decision Rights(Who decides what) 매트릭스 병행 |
| **Information Flow** | 데이터·보고서·KPI·이벤트 흐름 | 양방향·실시간·자동화. 데이터 SoR 단일화: SAP GRC(ServiceNow GRC·RSA Archer) -> EDW(Snowflake·BigQuery) -> 시각화(Power BI·Tableau). KPI 예: IT 비용매출비율·시스템가용성·MTTR·MTBF·Change Success Rate |
| **People, Skills & Competency** | 역량 정의·교육·자격 | **Skills Framework for the Information Age(SFIA)** v8(2023): 6단계 레벨, 28개 Category, 102 Skill. 필수 인증: CGEIT·CRISC·CISM·CISA·PMP·ITIL4 MP·TOGAF |
| **Policies & Procedures** | 정책·표준·지침 계층 | Policy Pyramid: Corporate Policy(2-3p) -> IT Policy(5-10p) -> Standards(SOP·STD: 10-30p) -> Guidelines -> Procedures. 예: 정보보안정책(ISMS-P 인증의 최상위 문서) |
| **Culture, Ethics & Behavior** | 조직문화·윤리·Tone at the Top | CobiT의 Soft Component. 측정: **Tone at the Top Index**(매년 이사 설문), Code of Ethics(ISACA·IEEE·ACS), 비윤리 행위 신고 채널(Whistleblowing)·Hotline |
| **Services, Infrastructure & Applications** | 기술 자산·서비스 카탈로그 | CMDB(Configuration Management DB) — ServiceNow CMDB·BMC Helix·Device42. 자동화: IaC(Terraform·Pulumi), Policy-as-Code(OPA·Sentinel), Compliance-as-Code(Chef InSpec·Open Policy Agent) |

### 핵심 산식 및 평가 모델

- **거버넌스 성숙도**: $M = \frac{\sum_{i=1}^{N} w_i \cdot L_i}{N}$ (단, $w_i$ = 가중치, $L_i$ = Process Capability Level 0\~5)
- **TCO(Total Cost of Ownership)**: $\text{TCO} = C_{\text{acq}} + C_{\text{impl}} + \sum_{t=1}^{T} \frac{C_{\text{op},t} + C_{\text{maint},t}}{(1+r)^t}$
- **NPV 순현재가치**: $\text{NPV} = \sum_{t=0}^{T} \frac{(\text{Benefit}_t - \text{Cost}_t)}{(1+r)^t}$ — 거버넌스 ROI 산출 시 적용
- **가용성(Availability)**: $\text{Availability} = \frac{\text{MTBF}}{\text{MTBF} + \text{MTTR}} \times 100\%$ — 99.99% = Four Nine(연간 52.6분 다운 허용)
- **KRI(Key Risk Indicator) 임계치**: $K = \mu + 2\sigma$(노란등) -> $K = \mu + 3\sigma$(빨간등) — 통계적 통제 한계

- **📢 섹션 요약 비유**: 7 Components는 자동차의 **7대 핵심 부품**과 같다. Process(엔진), Org Structure(차체·핸들), Information(전장배선), People(운전자), Policy(도로 신호), Culture(운전 매너), Services(연료·윤활유). 어느 하나가 어긋나면 사고가 발생한다.

---

## Ⅲ. 비교 및 연결

### 거버넌스/관리 프레임워크 비교

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 38500** | **CMMI v2.0** | **ISO 27001** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스·관리 통합 | IT 서비스 관리(ITSM) | 이사회 수준 IT 거버넌스 원칙 | 프로세스·조직 성숙도 | 정보보안 경영체계(ISMS) |
| **적용 범위** | Enterprise-wide(End-to-End) | Service Operation·Delivery | Strategic·Top Management | SW·조직 개발 | 정보보안 통제 |
| **핵심 산출물** | 40 GO/MO + 7 Components | 34 Practices + SVC | 6 Principles | 5-Level Maturity Model | 93 Annex A Controls |
| **구조** | Cascade·Focus Area | 4 Dimension·SVC | 3-Layer(Review·Direct·Monitor) | PAM·ARC | Plan-Do-Check-Act(PDCA) |
| **성숙도 모델** | PAM(0-5) | Maturity Model(1-5) | Maturity(5단계 자가평가) | CMMI Level 1-5 | Statement of Applicability(SoA) |
| **거버넌
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 798 / 800

<- **이전**: [797. IT 경영 관리 핵심 토픽 797번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/797_it_management_core_topic_797_exam_summary/)
**다음**: [799. IT 경영 관리 핵심 토픽 799번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/799_it_management_core_topic_799_exam_summary/) ->

---
