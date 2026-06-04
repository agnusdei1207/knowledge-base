+++
title = "625. IT 경영 관리 핵심 토픽 625번 시험 요약 (IT Management Core Topic 625 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 핵심 토픽 625번은 정보관리기술사 시험에서 빈출되는 **IT 거버넌스-전략-포트폴리오-아키텍처-운영-감리** 6대 영역을 통합적으로 평가하는 종합 문제로, COBIT 2019, ITIL 4, ISO 27001, TOGAF, PMBOK 7th 등 글로벌 표준 프레임워크의 상호 연계와 실무 적용 역량을 측정한다.
> 2. **가치**: 정답 도출 시 15~20점의 고배점 확보가 가능하며(기술사 1교시/2교시 모두 출제 빈도 상위), 표준 프레임워크 기반의 정형화된 답안 구조(거버넌스 체계 → KPI → 프로세스 → 통제 → 지속적 개선)를 통해 논리적 서술 점수와 전문성 점수를 동시에 극대화할 수 있다.
> 3. **판단 포인트**: 단순 암기형이 아닌 **"문제 상황 → 적합한 프레임워크 선정 → 단계별 적용 절차 → 정량적 효과 산출 → 리스크/제약 조건 보완"**의 5단계 논증 구조가 핵심이며, COBIT의 EDM(평가·지시·모니터링)와 ITIL의 Service Value Chain, TOGAF의 ADM 주기를 어떻게 결합하여 일관된 IT경영 체계로 풀어내느냐가 합격선을 가른다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 시험의 IT 경영 관리 토픽은 21세기 디지털 전환(DX) 가속화, 클라우드·AI·데이터 3법(개인정보 보호법, 정보통신망법, 신용정보법) 개정, ESG·공급망 보안 강화, 그리고 2024년 이후 生成AI 기반 업무 자동화 도입 확대로 인해 **"IT가 경영의 보조수단이 아니라 사업의 핵심驱动力"** 이라는 패러다임 전환을 정확히 이해하고 있는지를 평가한다.

기존의 1980~2000년대 데이터센터 중심, CAPEX 비중 80% 이상, 개별 시스템 단위 운영, 계층적 조직(전산실 → 정보화추진위원회) 기반의 IT 경영 모델은 더 이상 유효하지 않다. 현재의 IT 경영은 OPEX 비중 60% 이상(클라우드·SaaS), 분산·연결형(Connected Enterprise), 데이터·AI 중심 의사결정, 그리고 CDO·CIO·CISO가 이사회에 직접 보고하는 **Tri-CxO 거버넌스 구조**로 진화했다.

시험에서 625번과 같은 통합형 문제는 일반적으로 다음과 같은 **KPI 4종**(IT-BS 핵심 지표)을 요구한다:
- **재무 관점**: IT 투자 ROI, TCO 절감률, IT 예산 / 매출액 비율(벤치마크: 글로벌 평균 3.5%, 업종별 차등)
- **고객 관점**: 시스템 가용성(99.9% SLA), 사용자 만족도(NPS 기반), 인시던트 평균 해결시간(MTTR)
- **내부 프로세스 관점**: 프로젝트 정시 완료율, 변경 관리 성공률, 보안사고 발생건수
- **학습·성장 관점**: IT 인력 역량 등급, 핵심인재 유지율, 교육 투자 시간/인당

```text
┌──────────────────────────────────────────────────────────────────┐
│           625번 통합형 문제의 전형적 답안 구조 (5 Layer)           │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [1] 경영환경 분석      [2] IT 전략 수립        [3] 거버넌스 체계  │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐    │
│  │ SWOT/5-Forces│ ───▶ │ Porter/Blue  │ ───▶ │ COBIT EDM    │    │
│  │ PESTEL       │      │ Ocean 전략   │      │ RACI 매트릭스 │    │
│  │ 벤치마킹     │      │ IT-BS 카드   │      │ 의사결정권한 │    │
│  └──────────────┘      └──────────────┘      └──────────────┘    │
│           │                     │                     │           │
│           ▼                     ▼                     ▼           │
│  [4] 아키텍처·프로세스 설계  [5] 통제·측정·개선(CSI)                 │
│  ┌──────────────────────┐  ┌──────────────────────┐                │
│  │ TOGAF ADM (8 Phase) │  │ KPI 대시보드          │                │
│  │ ITIL SVC (6 Activity│  │ 내부통제 (IS Audit)   │                │
│  │ PMBOK 49 Process    │  │ 개선(PDCA/Kaizen)     │                │
│  │ Zero Trust/ISO27001 │  │ Re-audit / Maturity  │                │
│  └──────────────────────┘  └──────────────────────┘                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**왜 이 토픽이 필수인가?**
- 정보화진흥법(2023.6. 개정, 과학기술정보통신부), 클라우드컴퓨팅법(2024. 시행), 인공지능 기본법(2025.1. 시행 예정), 데이터 산업법(2022.4. 시행)에 의해 **법정 거버넌스 의무**가 강화됨
- 정보시스템 감리(전자정부법 §56, 감리원 등록제) 대상이 모든 공공기관 및 1,000억 원 이상 민간 사업자로 확대
- 4차 산업혁명 핵심 기술(AI, IoT, Cloud, BigData, Blockchain, 5G/6G)의 **도입-운영-폐기 전 주기(LCM, Life Cycle Management)** 를 경영 관점에서 통합 관리할 역량 요구

- **📢 섹션 요약 비유**: IT 경영 관리는 **자동차의 계기판과 운전자** 관계와 같다. 계기판(COBIT, ITIL, ISO 표준)이 아무리 정교해도, 운전자(CIO·CDO)가 도로 상황(경영환경)을 정확히 읽고 핸들(전략)을 꺾지 않으면 목적지(사업 목표)에 도달할 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 원리는 **"전략(Strategy) → 거버넌스(Governance) → 운영(Operation) → 통제(Control) → 개선(Improvement)"** 의 5단계 가치사슬(Value Chain)이다. 이는 COBIT 2019의 거버넌스/관리 목적(Governance & Management Objectives, 40개)과 ITIL 4의 Service Value Chain(6개 Activity + 3개 Perspective), ISO 27001의 PDCA(Plan-Do-Check-Act), PMBOK 7th의 Performance Domains(8개) 등이 서로 직교·연결되는 구조다.

```text
┌────────────────────────────────────────────────────────────────────┐
│         IT 경영 관리 5대 영역 × 3계층 통합 아키텍처 (3×5 매트릭스)  │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Tier 3: 거버넌스 ──────────────────────────────────────────────┐  │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐     │  │
│  │COBIT 2019   │ ITIL 4      │ ISO 27001   │ ISO 20000  │     │  │
│  │EDM(5개)     │ SVS         │ ISMS 4단계  │ SMS 6단계  │     │  │
│  │APO(14개)    │ 7 Guiding   │ A.5~A.8 통제│ 5 Process  │     │  │
│  │BAI(11개)    │ Principle   │ 93 통제항목 │ Groups     │     │  │
│  │DSS(6개)     │ 4 Dimension │ (Annex A)   │            │     │  │
│  │MEA(4개)     │ 18 Practice │             │            │     │  │
│  └─────────────┴─────────────┴─────────────┴─────────────┘     │  │
│              │              │              │            │       │  │
│  Tier 2: 프로세스 ──────────────────────────────  │            │  │
│  ┌────────────────────────────────────────────┐ │            │  │
│  │ PMBOK 7th (8 PD) + TOGAF 10 ADM Phase     │◀┘            │  │
│  │ + BPMN 2.0 + CMMI 5 Level                 │              │  │
│  └────────────────────────────────────────────┘              │  │
│              │                                                  │  │
│  Tier 1: 인프라·기술 ───────────────────────────  │              │  │
│  ┌────────────────────────────────────────────┐              │  │
│  │ Cloud (AWS/Azure/GCP) + On-Prem (Hybrid)  │              │  │
│  │ DevSecOps Pipeline + SRE + AIOps          │              │  │
│  │ Data Lake + Lakehouse + AI/ML Platform    │              │  │
│  │ Zero Trust + SASE + XDR                   │              │  │
│  └────────────────────────────────────────────┘              │  │
│                                                                │  │
└────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 거버넌스 (Governance)** | 의사결정 권한·책임·보고 체계 정의 | COBIT 2019 40개 목적 중 EDM 5개(Evaluate-Direct-Monitor), RACI 매트릭스, Three Lines Model(IIA, 2020 개정), 이사회 산하 IT 전략위원회 운영 |
| **IT 전략 (Strategy)** | 사업 목표와 IT의 정렬(Alignment) | Luftman의 IT-Business Alignment 6개 메커니즘(Communication, Competency, Governance, Partnership, Scope, Skills), Henderson-Venkatraman의 SAMM(Strategic Alignment Model), Ward&Peppard의 IS/IT 전략 매트릭스 |
| **EA 아키텍처 (Architecture)** | 전사 차원의 시스템 구조 표준화 | TOGAF 10 ADM 8단계(Preliminary→Vision→B→C→D→E→F→G→Req.Mgmt, ADM Cycle), Zachman 6×6 매트릭스, DoDAF 2.0, FEAF 5계층, Gartner EA Maturity 5단계 |
| **IT 서비스 운영 (Service Operation)** | 서비스 설계-전환-운영-개선 | ITIL 4 Service Value System(Guiding Principles 7개, Governance, Practices 34개, SVC 6 Activity), DevOps(SRE 5 golden signals, Error Budget), AIOps(Anomaly Detection) |
| **정보 보안 (Security)** | CIA(기밀성·무결성·가용성) 및 프라이버시 통제 | ISO 27001:2022(ISMS 4단계 + 93 통제), NIST CSF 2.0(Identify-Protect-Detect-Respond-Recover + Govern), Zero Trust(NIST SP 800-207), GDPR/PIPA 3법 |
| **프로젝트 관리 (PM)** | 일정·품질·비용·리스크·범위·이해관계자 통제 | PMBOK 7th(8 Performance Domains: Stakeholders, Team, Development, Planning, Project Work, Delivery, Measurement, Uncertainty), PRINCE2(7 Principle), 애자일(Scrum 3-5-3, SAFe 4 Config), 혼합형(Water-Scrum-Fall) |
| **IT 감리·내부통제 (Audit)** | 시스템 안전성·효율성·효과성 검증 | 정보시스템 감리(전자정부법 §56), COBIT 2019 MEA 4개(Managed Performance, Managed Internal Control, Managed Compliance, Managed Assurance), IIA의 Three Lines Model, ISACA CISA |
| **IT 성과 측정 (Measurement)** | 정량적 KPI 수집·분석·보고 | IT-BS 4관점 16~20 KPI, BSC 캐스케이딩, OKR(Objective & Key Results), CMMi 5단계, CMMI SVC 2.0 |

**핵심 알고리즘·수식 및 평가 기법:**

1. **TCO(Total Cost of Ownership) 산출**: TCO = 직접비(HW·SW·인건비) + 간접비(교육·다운타임·전환) + 운영비(전력·냉각·라이선스·유지보수). CAPEX→OPEX 전환 시 3년 TCO 비교 필수.
2. **NPV(순현재가치)**: NPV = Σ[(B_t - C_t) / (1+r)^t]. 할인율 r은 WACC(가중평균자본비용) 적용, 보통 8~12%.
3. **ROI**: (총 이익 - 총 비용) / 총 비용 × 100. IT 프로젝트 합격선 통상 15% 이상.
4. **Payback Period**: 누적 현금흐름이 0이 되는 시점. IT 인프라 3~5년, ERP 5~7년.
5. **EVA(Economic Value Added)**: NOPAT - (투자자본 × WACC). 음수면 가치 파괴.
6. **BSC 관점별 가중치**: 재무 22%, 고객 24%, 내부 프로세스 28%, 학습·성장 26% (Kaplan-Norton 표준).
7. **Maturity Level 산출**: 각 프로세스의 5단계(Initial→Managed→Defined→Quantitatively Managed→Optimizing) 점수 평균, CMMi에서는 5단계 중 3단계 이상이 도달해야 합격.

- **📢 섹션 요약 비유**: COBIT은 **자동차의 도로교통법**, ITIL은 **운전 매뉴얼**, PMBOK은 **항법(GPS)**, ISO 27001은 **차량 보험**이다. 도로교통법이 있어도 운전자가 매뉴얼을 모르고, GPS가 잘못 잡혀 있으면 목적지에 안전히 도착할 수 없다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 625번 문제에서 가장 빈번하게 출제되는 비교 분석은 **거버넌스 프레임워크 간 상호 관계**와 **전통적 방법론 vs 현대 방법론**이다. 아래는 시험에 자주 등장하는 핵심 비교표다.

| 구분 | COBIT 2019 (거버넌스) | ITIL 4 (서비스 운영) | ISO 27001 (보안) | PMBOK 7th (프로젝트) |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 투자·리스크의 가치 극대화 | IT 서비스 품질·효율 | 정보자산의 CIA 확보 | 프로젝트 성공·가치 실현 |
| **구조** | 40 Governance/Management Objectives, 5 Domain(EDM, APO, BAI, DSS, MEA) | SVS(7 Principles + 4 Dimension + 34 Practice + SVC 6 Activity) | ISMS 요구사항 + Annex A 93 통제 | 8 Performance Domain +
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 625 / 800

← **이전**: [624. IT 경영 관리 핵심 토픽 624번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/624_it_management_core_topic_624_exam_summary/)
**다음**: [626. IT 경영 관리 핵심 토픽 626번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/626_it_management_core_topic_626_exam_summary/) →

---
