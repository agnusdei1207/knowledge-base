---
title: "502. IT 경영 관리 핵심 토픽 502번 시험 요약 (IT Management Core Topic 502 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Information Technology Governance & Management)는 COBIT 2019, ITIL 4, ISO 38500, TOGAF, BSC/CSF, ISP(정보화 전략계획) 등 거버넌스·운영·전략 프레임워크를 통합하여 **Biz-IT Alignment(사업·IT 정렬)** 를 달성하고, **IT 가치(Value Delivery)** 와 **리스크 최적화(Risk Optimization)** 를 동시에 추구하는 체계이다.
> 2. **가치**: 엔터프라이즈 거버넌스 수립 시 IT 투자 수익률(ROIT)을 평균 20~35% 향상시키고, IT 부채(Technical Debt)를 GDP 대비 0.5~2.0% 수준에서 통제 가능하며, 정보화 사업의 정시完工率을 78% -> 92% 수준으로 끌어올려(PMI 2023), **디지털 전환(DX) 실패율 70%를 역전**시키는 경영 의사결정 인프라를 제공한다.
> 3. **판단 포인트**: COBIT의 40개 거버넌스/관리 목표와 ITIL 4의 34개 Practice를 1:1 매핑할지, BSC 4관점(재무/고객/내부/학습성장)으로 KPI를 통합할지, 그리고 EA(엔터프라이즈 아키텍처)를 ADM(Architecture Development Method) 4A-Phase로 적용할지 여부가 **조직 성숙도(COBIT PAM 5단계)와 산업별 규제(전자금융감독규정, 개인정보보호법)** 에 따라 결정되는 핵심 트레이드오프이다.

---

## Ⅰ. 개요 및 필요성

정보기술은 더 이상 비용 센터(Cost Center)가 아닌 **전략적 비즈니스 인에이블러(Strategic Business Enabler)** 이며, 동시에 **가장 큰 사업 리스크 소스**이기도 하다. 한국정보화진흥원의 「2024 정보화 실태조사」에 따르면, 국내 500대 기업의 IT 예산은 매출액의 평균 2.8%(금융업 6.4%)를 차지하고 있으나, **이 중 약 30%가 사일로(Silo) 시스템·중복 투자·프로젝트 실패로 회수 불가능(IT Waste)** 한 상태로 추산된다. Gartner(2024)는 글로벌 IT 지출 5.1조 달러 중 **30% 이상이 "Shadow IT" 및 Value-Less Spending** 이라고 진단했다.

이에 따라 기술사 시험에서 요구하는 **IT 경영 관리(502번 토픽)** 는 단순한 "IT 부서 운영"을 넘어서 **① IT 거버넌스(COBIT) ② IT 서비스 관리(ITIL) ③ 엔터프라이즈 아키텍처(EA) ④ IT 전략 기획(ISP) ⑤ IT 투자 및 성과관리(BSC/PPM) ⑥ IT 리스크 및 컴플라이언스(ISO 27001, ISMS-P)** 라는 6대 축을 아우르는 **상위통제체계(Internal Control over IT)** 를 다룬다.

```text
 +---------------------------------------------------------------------+
 |          [501 기술사 1교시] IT 경영 관리 6대 축 통합 프레임워크        |
 +---------------------------------------------------------------------+
 |                                                                     |
 |   ① 거버넌스         ② 서비스관리       ③ 아키텍처                  |
 |   +----------+      +----------+      +----------+                |
 |   | COBIT 19 |<------>|  ITIL 4  |<------>|  TOGAF   |                |
 |   | ISO38500 |      |  ISO20000|      |   EAF    |                |
 |   +----+-----+      +----+-----+      +----+-----+                |
 |        |                 |                  |                       |
 |        +--------+--------+--------+---------+                       |
 |                 v                 v                                  |
 |   ④ 전략기획         ⑤ 투자/성과        ⑥ 리스크/컴플                |
 |   +----------+      +----------+      +----------+                |
 |   | ISP 3.0  |<------>| BSC/CSF  |<------>| ISO27001 |                |
 |   | SWOT/BPM |      |  PPM     |      | ISMS-P   |                |
 |   +----------+      +----------+      +----------+                |
 |                                                                     |
 |        [최상위] IT 거버넌스 위원회 (이사회 산하)                      |
 |        [계층]  CIO -> CISO -> CDO -> EA Architect                      |
 |        [표준]  전자정부법, 개인정보보호법, 클라우드컴퓨팅법           |
 +---------------------------------------------------------------------+
```

과거(1990~2000년대)에는 **사일로형 IT 운영**(각 현업부서가 독자적 시스템 구축, ROI 부재, 프로젝트 70% 실패)이 지배적이었으나, 현재는 **①클라우드·AI·데이터 기반 Biz-IT 융합 ②규제강화(GDPR, 개인정보보호법) ③ESG/지속가능경영 보고 의무화** 로 인해 **전사적 IT 통제(Enterprise-wide IT Control)** 가 생존 조건이 되었다. 기술사 답안에서는 이러한 **"paradigm shift: Cost Center -> Value Center -> Risk Center"** 를 명확히 진술해야 한다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **자동차의 '통합 계기판'** 과 같다. 속도계(BSC/CSF), 연료계(ROI/TCO), 엔진온도계(IT 거버넌스), 브레이크등(ISMS-P), 후방카메라(EA) — 6개 계기판이 동시에 작동해야 안전(가치+리스크 균형) 운행이 가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 메커니즘은 **PDCA + 거버넌스 루프**로 작동한다. **전략(Strategy) -> 포트폴리오(Portfolio) -> 프로그램(Program) -> 프로젝트(Project) -> 운영(Operation) -> 가치(Value)** 로 이어지는 **Value Realization Chain** 이며, 이를 **"Run-Grow-Transform"** 의 3-포트폴리오 모델로 분류·투자배분한다(McKinsey, Gartner 2024).

```text
           [이사회] IT Steering Committee (Quarterly)
                     |
                     v
        +------------------------------+
        | Layer 1: 거버넌스 (Govern)    |  <- COBIT 2019 EDM
        |  - 평가/지시/모니터링 (EDM)   |     (40 Goals)
        +------------+-----------------+
                     v
        +------------------------------+
        | Layer 2: 전략 기획 (Plan)     |  <- ISP 3.0 / TOGAF ADM
        |  - SWOT, BPM, EA 4A-Phase    |     (Phase A: Vision ~ H)
        +------------+-----------------+
                     v
        +------------------------------+
        | Layer 3: 서비스 운영 (Run)    |  <- ITIL 4 SVS
        |  - Incident/Change/Problem   |     (34 Practices)
        |  - Service Desk, SLA         |
        +------------+-----------------+
                     v
        +------------------------------+
        | Layer 4: 가치 측정 (Measure)  |  <- BSC 4관점 + CSF
        |  - TCO, ROI, NPV, IRR       |     (KPI Cascade)
        |  - Benefit Realization       |
        +------------+-----------------+
                     v
        [성과보고] Business Outcome -> Stakeholder Value
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 Governance System** | IT 거버넌스 최상위 프레임워크 | 5개 도메인(EDM, APO, BAI, DSS, MEA) × 40개 Governance/Management Objective, **CSF(중요성목표) 13개**와 **KPI 40+** 로 구성. Design Factors 11개(기업전략, 위험도, 컴플라이언스 등)로 거버넌스 시스템 **맞춤형 설계** |
| **ITIL 4 Service Value System** | IT 서비스 라이프사이클 관리 | SVS 5대 구성요소(Guiding Principles, Governance, Practices, Continual Improvement, Value). **34개 Practice**(일반 14 + 서비스 17 + 기술 3). **Service Value Chain**(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support) |
| **TOGAF 10 ADM** | 엔터프라이즈 아키텍처 개발방법론 | 8 Phase **A(Architecture Vision) -> B/C/D/E(비즈니스/데이터/응용/기술) -> F(Migration Planning) -> G(Implementation Governance) -> H(Architecture Change Management)**. **ArchiMate 3.2** 표준 표기 |
| **BSC(Balanced Scorecard)** | 전략 KPI 통합관리 | 4관점(재무 25% / 고객 25% / 내부프로세스 30% / 학습성장 20%) 가중치. **Strategy Map** 으로 인과관계 도식화, **CSF -> KPI -> Target -> Initiative** 4단계 계단화 |
| **ISP(정보화 전략계획) 3.0** | 중장기 IT 로드맵 | 환경분석(SWOT/PEST/STEEP) -> 현행 EA 분석(BPM, 서비스, 데이터, 기술) -> To-Be EA -> 구현계획. **5개년 + 단계별(BPR/시스템구축/운영) 3단계** |
| **ISO 38500 / ISMS-P** | IT 거버넌스 국제표준 / 인증 | ISO 38500의 **6원칙(책임, 전략, 획득, 성과, 준수, 인간행위)** 모델. ISMS-P는 **64개 통제항목**(관리 12, 보호 13, 물리 6, 기술 33)으로 한국인터넷진흥원(KISA) 인증 심사 |

**핵심 알고리즘/모델 심화**:
- **CobiT TIPA(Tailoring Process)**: 11개 Design Factor -> 거버넌스 시스템 40개 목표 중 **선택·배분·우선순위 산정**. Focus Area(MFC: Microservice, Cloud, AI, DevOps, Sustainability) 50+개 제공.
- **ITIL 4 Continual Improvement Model**: 7단계(SVC: Start/What is the vision? -> Where are we now? -> Where do we want to be? -> How do we get there? -> Did we get there? -> How do we keep the momentum?)
- **EA Fit-Gap 분석**: Baseline Architecture(현행) vs Target Architecture(목표) 비교, **Δ(차이) 도출** -> Gap Project 도출 -> Migration Plan에 반영
- **BSC 인과관계**: 학습성장(직원 역량) -> 내부프로세스(품질) -> 고객(만족) -> 재무(매출). **Time-lag 보정**(학습->재무 12~24개월) 필수

- **📢 섹션 요약 비유**: IT 경영 관리 6대 축은 **병원 진료 시스템** 과 같다. COBIT은 종합 검진(거버넌스 진단), ITIL은 응급실(서비스 운영), TOGAF는 해부학(아키텍처), BSC는 바이탈사인(KPI), ISP는 진료기록(전략 문서), ISO 38500/ISMS-P는 의료 면허(인증).

---

## Ⅲ. 비교 및 연결

기술사 시험에서 가장 빈출하는 **프레임워크 간 비교** 는 COBIT vs ITIL vs PMBOK vs ISO 27001 vs TOGAF이다. 각 프레임워크는 **Layer(계층)·관점·주체·산출물·적용범위** 가 다르며, 이를 정확히 구분해 답안에서 인용해야 한다.

| 구분 | **COBIT 2019** | **ITIL 4** | **PMBOK 7** | **ISO 27001/ISMS-P** | **TOGAF 10** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **계층** | 거버넌스(상위) | 서비스 운영(중위) | 프로젝트(하위) | 통제(전계층) | 아키텍처(전계층) |
| **관점** | "What & Why" (What should be done) | "How" (How to deliver) | "When" (When & Sequence) | "Risk" (How to secure) | "Design" (How to structure) |
| **주체** | 이사회·CIO·감사인 | ITSM 팀·서비스 매니저 | PMO·프로젝트 매니저 | CISO·정보보호팀 | EA 아키텍트·CDO |
| **핵심 산출물** | Goals Cascade, CSF, KPI Catalog | Service Catalog, SLA/OLA, CI | Charter, WBS, Risk Register | SoA(Statement of Applicability), RTP | ADM 산출물(Architecture Definition Document 등) |
| **적용 범위** | 전사 IT 거버넌스 | IT 서비스 라이프사이클 | 개별 프로젝트 | 정보보호 통제 영역 | EA 4 domains(BA/DA/AA/TA) |
| **인증/표준** | ISACA 공인 (CGEIT, COBIT Foundation) | PeopleCert/Axelos (ITIL Foundation ~ Master) | PMI (PMP, PgMP) | KISA·ISO 인증 | The Open Group (TOGAF Certified) |
| **갱신 주기** | 5~6년(2019->2025 예정) | 5년(2019->2024 v4 갱신) | 5~7년(2021 v7) | 3년(2022) | 2~3년(2022 v10) |
| **연계 프레임워크** | ISO 38500, ITIL, PMBOK | COBIT, DevOps, Lean | COBIT, PRINCE2, Agile | COBIT, NIST CSF, PCI-DSS | ArchiMate, BPMN, UML |
| **성공 KPI** | 거버넌스 성숙도 +0.5 Level/년 | First Call Resolution ≥75% | 정시完工率 ≥90% | ISMS-P 인증 유지 | EA 활용률 ≥80% |
| **비용 규모** | 도입비 1~3억, 컨설팅 6개월 | 구축 2~5억, 12~18개월 | PMO 구축 5천만원~1억 | 인증심사 3~5천만원 | EA 도구(Avolution/ABACUS) 1~2억 |

**다른 시스템과의 연결**:
- **ERP(SAP/Oracle) ↔ ITIL**: SAP Solution Manager + ChaRM(Change Request Management) 로 ITIL Change/Incident Practice 자동화
- **SIEM(Splunk/QRadar) ↔ ISMS-P**: 보안로그 64개 통제영역 중 13개(기술적 보호조치) 실시간 모니터링
- **DevOps(Jenkins/ArgoCD) ↔ COBIT BAI**: BAI03(Manage Solutions), BAI05(Manage Organizational Change) 와 **CI/CD 파이프라인 1:1 매핑**
- **클라우드(AWS Well-Architected) ↔ TOGAF**: AWS 5 pillars(Operational Excellence, Security, Reliability, Performance, Cost) ↔ TOGAF 4A(BA/DA/AA/TA) 매핑 가능
- **AGILE/Scrum ↔ PMBOK Hybrid**: PMBOK 7의 **8 Performance Domain**(Stakeholder, Team
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 502 / 800

<- **이전**: [501. IT 경영 관리 핵심 토픽 501번 시험 요약](/studynote/12_it_management/05_security_compliance/501_it_management_core_topic_501_exam_summary/)
**다음**: [503. IT 경영 관리 핵심 토픽 503번 시험 요약](/studynote/12_it_management/05_security_compliance/503_it_management_core_topic_503_exam_summary/) ->

---
