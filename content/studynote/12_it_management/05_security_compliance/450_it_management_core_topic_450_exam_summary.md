---
title: "450. IT 경영 관리 핵심 토픽 450번 시험 요약 (IT Management Core Topic 450 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 **COBIT 2019 거버넌스 체계(Governance Objectives Cascade)**, **ITIL 4 서비스 가치 시스템(SVS)**, **ISO/IEC 38500 6원칙**, **PMBOK 7th Performance Domains**을 통합한 경영-거버넌스-관리(EDM: Evaluate, Direct, Monitor) 3계층 의사결정 구조이며, IT가 사업전략(Strategy)->포트폴리오(Portfolio)->프로그램(Program)->프로젝트(Project)->운영(Operation)으로 가치(Value)를 전달하는 사슬을 최적화하는 것임.
> 2. **가치**: McKinsey & Company 연구에 따르면 디지털 성숙도 Top-Quartile 기업은 영업총이익률(ROS) **+26%p**, 매출성장률(YoY) **+9%p**, 시가총액/EVA **+17%** 차이를 보이며, COBIT 2019의 Goals Cascade를 적용한 기업은 IT 투자 대비 ROI를 평균 **2.7배** 향상(정보통신산업진흥원, 2023)시킴.
> 3. **판단 포인트**: 핵심 트레이드오프는 (1) **거버넌스 통제(Control)** vs **민첩성(Agility)** — COBIT의 Design Factor 10개 중 "Risk Profile"과 "Enterprise Size"에 따라 통제 수준 결정, (2) **표준 채택(Standardization)** vs **상황 적합성(Contingency)** — ITIL의 34개 Practice 중 Service Desk, Incident, Change 등은 필수이나, SRE·DevOps 환경에서는 1-tier DevOps Toolchain(예: Backstage, Argo CD)으로 대체 검토, (3) **내부 통제 강화** vs **운영 효율** — ISO 27001 통제 항목 93개 중 중복 통제(예: A.5.1.1 vs A.5.1.2) 통합 여부.

---

## Ⅰ. 개요 및 필요성

IT 경영관리는 **"기술(Technology) × 경영(Management) × 거버넌스(Governance)"** 의 교차점에 있는 학제적 분야로, 1980년대 MIS(경영정보시스템) 연구에서 출발하여 1990년대 ITIL v1(British CCTA, 1989), 1996년 ISACA의 COBIT(Control Objectives for Information and Related Technologies) 초판, 2000년대 ISO 38500(2008)·ITIL v3(2007)를 거치며 **"기술 도입"에서 "가치 실현(Value Realization)"** 으로 패러다임이 전환됨.

특히 4차 산업혁명(Industry 4.0) 이후, 클라우드·AI·IoT가 기업의 **핵심 운영 시스템(SoR, System of Record)** 으로 자리잡으면서, 전통적 IT 관리 방법론만으로는 디지털 비즈니스 대응이 불가해짐. Gartner(2024) 보고서에 따르면 **CEO의 71%가 Digital Transformation를 최우선 과제**로 제시하나, **실패율 75%**(BCG, 2022)의 원인이 **"거버넌스 부재·리스크 관리 미흡·조직 변화 저항"** 으로 분석됨.

```text
[IT 경영관리 3계층 의사결정 구조 (COBIT 2019 EDM Model)]

+----------------------------------------------------------------------+
|  GOVERNANCE LAYER (이사회의사결정)                                     |
|  -----------------------------------------                           |
|  EDM01: 거버넌스 프레임워크 설정    EDM04: 리스크 최적화               |
|  EDM02: 가치 전달 보장             EDM05: 자원 최적화                  |
|  EDM03: 리스크 최적화              EDM: 성과평가(KPI/Cascade)          |
|  책임주체: 이사회, 경영진, 외부감사                                  |
|  의사결정주기: 분기~연간                                              |
+----------------------------------------------------------------------+
                                ^
                                |  거버넌스 지시(Direct)
                                v
+----------------------------------------------------------------------+
|  MANAGEMENT LAYER (CIO·IT경영실)                                    |
|  -----------------------------------------                           |
|  APO (Align, Plan, Organize) 13개 프로세스                            |
|  BAI (Build, Acquire, Implement) 11개 프로세스                        |
|  DSS (Deliver, Service, Support) 6개 프로세스                         |
|  MEA (Monitor, Evaluate, Assess) 4개 프로세스                        |
|  책임주체: CIO, ITPMO, 서비스매니저                                   |
|  의사결정주기: 월~분기                                                |
+----------------------------------------------------------------------+
                                ^
                                | 관리 실행(Manage)
                                v
+----------------------------------------------------------------------+
|  OPERATION LAYER (현업 IT 조직)                                       |
|  -----------------------------------------                           |
|  • 서비스 운영: Service Desk(L1/L2/L3), Incident, Problem            |
|  • 인프라: 하이퍼바이저(vSphere 8, AHV 7), K8s(OpenShift 4.x)        |
|  • DevOps: CI/CD(GitHub Actions, Jenkins 2.4xx), IaC(Terraform)      |
|  • 보안관제: SIEM(Splunk, QRadar), EDR(CrowdStrike, Defender)        |
|  의사결정주기: 일~주간                                                 |
+----------------------------------------------------------------------+

        <------------ Goals Cascade (위->아래 전파) ------------>
        <------------ Feedback Loop (아래->위 성과보고) ---------->
```

**필요성의 본질**: 한국 정보시스템 감리법(2021년 12월 전면 개정)에 따라 **공공기관·연간 매출 1,500억 원 이상 또는 시스템 구축비 100억 원 이상** 사업은 IS 감리가 의무화되었으며, 특히 **중요정보통신기반시설**(금융·에너지·교통·정보통신·수자원 5대 분야)은 K-ISMS 인증 의무화(2022.6. 시행)에 따라 **IT 거버넌스-리스크-컴플라이언스(GRC) 통합 관리**가 법적으로 요구됨.

- **📢 섹션 요약 비유**: IT 경영관리는 **도시의 도시계획(Urban Planning)** 과 같습니다. 건물(시스템) 하나만 잘 짓는 것이 아니라, 상하수도(인프라), 도로(네트워크), 소방서(보안관제), 시청(거버넌스), 병원(BCP)까지 **도시 전체의 안전·효율·가치**를 통합 설계하는 일이죠. 이게 없으면 건물만 무작정 세워 정체·화재·침수가 발생합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 핵심은 **"가치(Value)"** 라는 정량적 목표를 위해 4개의 메커니즘(Strategy-Alignment, Portfolio Optimization, Risk-Compliance Assurance, Service Excellence)을 결합하는 것임. 아래는 **가치 실현 체인(Value Realization Chain)** 의 상세 아키텍처임.

```text
[IT 가치 실현 아키텍처 - V-Model + COBIT Cascade]

    사업전략(Strategy)        <------ Balanced Scorecard(BSC) 4관점
            |                 ------ OKR(Objectives & Key Results)
            v
    +-----------------+
    |  IT 전략 (IT    |  -> SWOT 분석, Critical Success Factor(CSF)
    |  Strategy Map)  |  -> Porter's Value Chain 분석
    +--------+--------+
             v
    +-----------------+
    |  포트폴리오     |  -> BCG Matrix(Star·Cash Cow·Question·Dog)
    |  (Portfolio)    |  -> Ward & Peppard(2016) IS Portfolio
    |                 |  -> 정량평가: NPV, IRR, TCO 3~5년
    +--------+--------+
             v
    +-----------------+
    |  프로그램/프로젝트|  -> PMBOK 7th 8 Performance Domain
    |  (Program/Pjt)  |  -> PRINCE2 7 Principles
    |                 |  -> 애자일: Scrum, SAFe 6.0, LeSS
    +--------+--------+
             v
    +-----------------+
    |  서비스 운영    |  -> ITIL 4 SVS, 34개 Practice
    |  (Service Ops)  |  -> ISO/IEC 20000-1:2018
    |                 |  -> SRE(SRE Workbook, Google)
    +--------+--------+
             v
    +-----------------+
    |  가치 측정/보고|  -> KPI Tree: Benefits Realization
    |  (Value Meas.)  |  -> EVA(경제부가가치), ROS, ROI
    +-----------------+
             ^
             |  <-- 피드백: Benefits Realization Plan(BRP)
             +----------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **거버넌스 체계(Governance System)** | 이사회-경영진의 IT 의사결정 프레임 제공 | COBIT 2019: **40 Governance & Management Objectives**, **11 Design Factors**(Enterprise Strategy, Goals, Risk Profile, Compliance, Role of IT, Sourcing, IT Methods, Tech Adoption, Org Size, etc.), **5 Focus Area** 체계. **Goals Cascade**: Stakeholder Needs -> Enterprise Goals(13개) -> Alignment Goals(13개) -> Management Objectives(40개) |
| **서비스 관리(Service Management)** | IT 서비스를 SLA 기반으로 설계·전달·지원 | ITIL 4 **Service Value System(SVS)**: 5 Components(Offering, Value, Demand, Governing Org, Practices, Information & Technology) × **7 Guiding Principles**(Focus on Value, Start Where You Are, Progress Iteratively, Collaborate, Think Holistically, Keep It Simple, Optimize & Automate). **34 Practices** (General 14, Service 17, Technical 3) |
| **프로젝트 관리(Project Management)** | 일정·품질·원가·리스크 통제 하에 결과물 도출 | **PMBOK 7th 8 Performance Domains**: Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty. **12 Principles of Project Management**. **Predictive(Waterfall) vs Adaptive(Agile)**: 프로젝트 특성(Volatility·Complexity·Ambiguity) 따라 **Tuk & Wilkinson의 Stacey Matrix**로 접근법 선택 |
| **리스크·컴플라이언스(GRC)** | IT 리스크 식별·평가·대응·모니터링 | **ISO 31000:2018** 리스크관리 프로세스(6단계: Establish Context -> Risk Assessment -> Treatment -> Monitoring -> Communication). **ISO 27001:2022** 93개 통제항목(4개 영역: Organizational 37, People 8, Physical 14, Technological 34). **K-ISMS** 인증 기준 102개 항목, 인증심사 주기 **3년 갱신 + 1년 사후심사** |
| **성과 측정(Performance Measurement)** | IT 투자 대비 가치 정량화 | **BSC 4관점**(Financial·Customer·Internal Process·Learning/Growth) × **IT BSC**(Nolan & McFarlan, 2003). **Benefits Realization Plan(BRP)**: Cost->Capability->Outcome->Benefit 4단계. **TBM(Technology Business Management)**: 4계층 Cost Model(Layer 1~4)을 통한 IT 비용 투명화, Apptio/Freewheel 등 도구 활용 |
| **엔터프라이즈 아키텍처(EA)** | 업무·정보·시스템·기술의 통합 청사진 | **TOGAF 10th** ADM(Architecture Development Method) 10단계(Phase A~H + Preliminary + Requirements Management). **Zachman Framework** 6×6 매트릭스(What·How·Where·Who·When·Why × Planner·Owner·Designer·Builder·Subcontractor·Operation). **ArchiMate 3.2**: Business·Application·Technology 3 Layer + Strategy·Motivation·Implementation&Migration Extension |
| **BCP/DR(연속성)** | 재해 시 RTO/RPO 내 서비스 복구 | **ISO 22301:2019** BCMS 요구사항. **DR 전략 4유형**: Backup&Restore(RTO 24h+, RPO 24h, 비용 1x), Pilot Light(RTO 4h, RPO 분), Warm Standby(RTO 분, RPO 초), Multi-Site Active-Active(RTO 0, RPO 0, 비용 20x). 금융권 DR 가이드라인(금융위원회, 2022): **RTO 1시간, RPO 5분** 이내 |
| **보안 거버넌스(Security Governance)** | CIA(기밀성·무결성·가용성) 및 제로트러스트 실현 | **NIST CSF 2.0**(2024.2 발표, 6 Function: Govern·Identify·Protect·Detect·Respond·Recover, 22 Category). **Zero Trust Architecture**(NIST SP 800-207): **3대 원칙**(Never Trust, Always Verify; Least Privilege; Assume Breach), **3대 컴포넌트**(Policy Engine PE, Policy Administrator PA, Policy Enforcement Point PEP). **SASE**(Gartner, 2019): SD-WAN + SWG + CASB + ZTNA + FWaaS 통합 |

**핵심 원리 심층 분석**:

1. **Goals Cascade(목표 연쇄)**: COBIT 2019의 가장 핵심 메커니즘으로, 기업 이해관계자(Stakeholder) 요구 -> 13개 Enterprise Goal -> 13개 Alignment Goal -> 40개 Management Objective로 **위에서 아래로 전파**되고, **성과 측정은 아래에서 위로 보고**됨. 각 단계 간 **M:M(Many-to-Many) 매핑**이 가능하며, **RACI 차트**로 책임 할당.

2. **Design Factor 11개**: COBIT 2019는 One-size-fits-all을 배격하고, **조직의 상황 변수**(Enterprise Size, Risk Appetite, Compliance Requirements, Role of IT
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 450 / 800

<- **이전**: [449. IT 경영 관리 핵심 토픽 449번 시험 요약](/studynote/12_it_management/05_security_compliance/449_it_management_core_topic_449_exam_summary/)
**다음**: [451. IT 경영 관리 핵심 토픽 451번 시험 요약](/studynote/12_it_management/05_security_compliance/451_it_management_core_topic_451_exam_summary/) ->

---
