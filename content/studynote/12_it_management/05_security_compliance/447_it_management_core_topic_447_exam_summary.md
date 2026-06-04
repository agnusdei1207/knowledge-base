---
title: "447. IT 경영 관리 핵심 토픽 447번 시험 요약 (IT Management Core Topic 447 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019(거버넌스·관리 목표 40개), ITIL 4(Service Value System 7가지 가이드 원칙, 34개 실무 프로세스), ISO 27001(ISMS-P 102개 통제 항목), ISO 20000(서비스경영시스템 9개 클러스스)을 통합한 IT 거버넌스 체계는 비즈니스 목표 ↔ IT 투자 ↔ 리스크 ↔ 자원 배분을 단일 가치 흐름(Value Chain)으로 연결하는 경영 관리 프레임워크이다.
> 2. **가치**: 효과적인 통합 거버넌스 적용 시 IT 투자 대비 ROI 15~25% 개선, 주요 IT 장애 회복시간(MTRS) 60% 단축, 규제 컴플라이언스(개인정보보호법, 전자금융감독규정) 대응 비용 30~40% 절감이 가능하며, 이사회-경영진-IT 조직 간 의사결정 투명성을 정량적으로 보장한다.
> 3. **판단 포인트**: 프레임워크 선정 시 **조직 성숙도(COBIT PAM 5단계)**, **규제 환경(국내: 개인정보보호법·전자금융거래법 / 글로벌: GDPR·SOX·HIPAA)**, **클라우드 전환율(40% 이상 시 ITIL 4 Practices 우선 적용)**, **산업별 특성(금융: FFIEC·DORA, 공공: EA 표준프레임, 제조: IEC 62443)**에 따라 가중치를 차등 적용해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적 IT 운영은 **기술 중심·부서 단위·사일로(Silo)형 관리**로 CFO·CEO·CIO가 동일한 KPI를 공유하지 못해 Shadow IT 비용이 전체 IT 예산의 30~40%를 잠식하고, 동일 사안이 이사회(Board)·감사위원회·IT위원회에 중복 보고되는 비효율이 발생했다. 2010년대 후반 이후 디지털 전환(DX), GDPR·개인정보보호법 강화, 클라우드 1st 전략, AI·데이터 기반 의사결정이 보편화되면서 IT를 **"비용 센터(Cost Center)"**가 아닌 **"전략적 비즈니스 파트너(Value Driver)"**로 재정의해야 할 필요성이 대두되었다.

이에 ISACA의 COBIT 2019, AXELOS의 ITIL 4, ISO/IEC의 27001·20000·38500(거버넌스)·27014(거버넌스) 표준이 등장했고, **"단일 프레임워크만으로는 모든 요구사항을 충족할 수 없다"**는 합의 하에 **통합 거버넌스(Integrated Governance Framework)** 개념이 정착되었다. 즉, **COBIT으로 거버넌스(누가 무엇을 결정하는가)를, ITIL 4로 서비스 운영(어떻게 가치를 전달하는가)을, ISO 27001/20000으로 통제와 인증(어떻게 검증하는가)을, EA로 구조적 정렬(어떻게 맞추는가)을** 담당하도록 역할 분담하는 것이 핵심 패러다임 전환이다.

```text
+--------------------------------------------------------------------------+
|                    통합 IT 거버넌스 4-Layer Reference Model              |
+--------------------------------------------------------------------------+
|                                                                          |
|   [Layer 1: 전략·거버넌스]  COBIT 2019 -+                               |
|     - 5개 거버넌스 시스템(EDM)            |                              |
|     - 40개 관리 목표(Governance/Manage)   |  +----------------------+   |
|     - PAM(능숙도 평가 6단계)             |  |  비즈니스 목표(Goals) |   |
|                                          +-->|  · ROI, TSR, Risk    |   |
|   [Layer 2: 가치 전달]    ITIL 4 --------+  |  · Time-to-Market    |   |
|     - SVS(Service Value System)          |  |  · Compliance        |   |
|     - 34개 Practices(18 General + 3 Svc) |  +----------------------+   |
|     - 4D 모델(Diagnose->Design->...)       |            ^                  |
|                                          |            | 정렬(Alignment)|
|   [Layer 3: 통제·인증]    ISO 27001/20000 |            |               |
|     - ISMS-P 102개 통제(Annex A)         |   +--------------------+    |
|     - SMS 9개 클러스스(ISO 20000)         |   |  Enterprise        |    |
|     - ISO 38500 이사회 거버넌스 원칙      |   |  Architecture (EA) |    |
|                                          |   |  · TOGAF ADM       |    |
|   [Layer 4: 구조·아키텍처] EA-TOGAF -----+   |  · FEAF, DoDAF    |    |
|     - ADM 8단계                          |   |  · 정부 EA 참조모형|    |
|     - 비즈니스↔데이터↔애플리케이션↔기술  |   +--------------------+    |
|                                                                          |
+--------------------------------------------------------------------------+
```

**왜 필요한가?** — 전통적 IT 관리의 **5대 실패 요인**을 해결하기 위함이다.

1. **정렬 실패(Alignment Failure)**: IT KPI 70%가 기술 지표(가용성 99.9%, 응답시간 < 2초)일 뿐 비즈니스 KPI(고객 이탈률, 신규 ARR)와 연계되지 않음 -> **COBIT Cascade Goals**로 매핑.
2. **Shadow IT**: 클라우드 SaaS 도입 시 IT 부서 인지 없이 부서가 직접 계약(예: 영업팀의 Salesforce, 마케팅팀의 HubSpot) -> **COBIT APO04(혁신) + APO12(리스크)** 통제.
3. **규제 비대응**: 2023년 개인정보보호법 개정(가명정보 도입), EU AI Act(2024), DORA(2025 금융) 등 규제 패러다임 변화에 ISMS-P 인증만으로는 한계 -> **ISO 27001:2022(Annex A 93->93개 통제, 4개 영역 재편)** 적용.
4. **사고 대응 지연**: 2017년 Equifax(1.4억 명 정보유출, 7억 달러 배상), 2023년 MOVEit(2,600개 조직, 1,000만 명 피해) 등 공급망·제로데이 공격에 대한 **BCM/DR(ITIL 4 Continual Improvement + ISO 22301)** 부재.
5. **ROI 불명확**: McKinsey(2023) 조사에 따르면 CIO의 65%가 이사회에 IT 투자 ROI를 정량적으로 증명하지 못함 -> **Balanced Scorecard for IT(BSC-IT) + COBIT Performance Management** 필요.

- **📢 섹션 요약 비유**: **"통합 IT 거버넌스는 마치 오케스트라의 지휘자(COBIT)·악보(ITIL)·음악원 리허설실(ISO 인증)·무대 디자인(EA)처럼, 각자 다른 역할을 하면서도 하나의 symphony(사업 가치)를 연주하도록 만드는 시스템이다."**

---

## Ⅱ. 아키텍처 및 핵심 원리

통합 IT 거버넌스는 **거버넌스 목표(Governance Objective) -> 관리 실무(Management Practice) -> 운영 통제(Operational Control) -> 성과 측정(Performance Measurement)**의 4계층 구조로 동작하며, 각 계층은 **Goal Cascade(목표 연쇄)**, **Process Reference Model(프로세스 참조 모델)**, **RACI Matrix(책임 할당)**, **CSF/KPI(성과지표)**로 연결된다.

```text
+------------------------------------------------------------------------+
|         COBIT 2019 ↔ ITIL 4 ↔ ISO 27001 매핑 아키텍처                 |
+------------------------------------------------------------------------+
|                                                                        |
|  +--- COBIT 2019 (5개 EDM + 35개 Process) -------------------------+ |
|  |                                                                   | |
|  |  EDM01 거버넌스 프레임워크 설정 및 유지                           | |
|  |    +---> ITIL 4: "Governance" Practice(조직·문화)                | |
|  |                                                                   | |
|  |  EDM02 혜택 전달(Delivery of Benefits)                           | |
|  |    +---> ITIL 4: Service Value Chain(Engage->Design->Transition->   | |
|  |                 Obtain/Build->Deliver&Support) + 6 Activities     | |
|  |                                                                   | |
|  |  EDM03 리스크 최적화                                              | |
|  |    +---> ISO 27001: A.5~A.8 통제 93개 + 리스크 처리(RSA/RTP)      | |
|  |                                                                   | |
|  |  EDM04 자원 최적화                                                | |
|  |    +---> ITIL 4: SVC(Information & Technology, Partners &         | |
|  |                 Suppliers, Value Streams & Processes)            | |
|  |                                                                   | |
|  |  EDM05 이해관계자 투명성                                          | |
|  |    +---> ISO 38500: 이사회 6개 원칙(책임·전략·취득·성과·규율·인간)| |
|  +-------------------------------------------------------------------+ |
|                              <-> 양방향 매핑                              |
|  +--- ISO 27001:2022 (Annex A 통제 영역) --------------------------+ |
|  |  A.5 조직 통제(37개) | A.6 인적 통제(8개)                        | |
|  |  A.7 물리적 통제(14개) | A.8 기술 통제(34개) = 총 93개 통제     | |
|  +-------------------------------------------------------------------+ |
|                              <-> Evidence (증거)                         |
|  +--- RACI Matrix ------------------------------------------------+ |
|  |  R(Responsible): 프로세스 실무자  | A(Accountable): 최종 책임자 | |
|  |  C(Consulted): 협의 부서          | I(Informed): 통보 대상     | |
|  +-------------------------------------------------------------------+ |
|                                                                        |
+------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 Cascade Goals** | 비즈니스 목표 ↔ 정렬(IT↔비즈니스) ↔ 거버넌스/관리 목표 간 5단계 연쇄 | 13개 비즈니스 목표 -> 13개 정렬 목표 -> 40개 거버넌스·관리 목표 매핑. 우선순위는 **Design Factors 11개**(전략, 목표, 리스크, 위협, 규제, 역할, IT 채택, 기술, 지리, 산업, 조직 규모)로 결정 |
| **ITIL 4 Service Value System (SVS)** | 가치 공동창조(Value Co-Creation) 및 7개 가이드 원칙 적용 | 7대 원칙: Focus on Value, Start Where You Are, Progress Iteratively, Collaborate, Think and Work Holistically, Keep It Simple, Optimize and Automate. 34개 Practices(14 General, 17 Service, 3 Technical) |
| **ISO 27001:2022 ISMS** | 정보보호경영시스템 인증(Annex SL HLS 10조 + Annex A 93개 통제) | PDCA 사이클 + Statement of Applicability(SoA) + Risk Treatment Plan(RTP). 4개 통제 영역(조직·인적·물리·기술) 재편, **공급망 보안(A.5.19~A.5.23)·클라우드(A.8.16)·데이터 마스킹(A.8.11)** 등 신규 통제 11개 추가 |
| **ISO 20000-1:2018 SMS** | IT 서비스경영시스템 9개 클러스스 인증 (Plan/Do/Check/Act 사이클) | 9개 클러스스: 거버넌스·전략·제품·파트너·수요·서비스 디자인·전환·운영·개선. ISO 27001과 통합 인증 가능(연결성 70%) |
| **EA-TOGAF ADM** | 8단계 개발 방법론(ADM Cycle) | Preliminary Phase -> A(비즈니스 아키텍처) -> B(데이터) -> C(애플리케이션) -> D(기술) -> E(기회/솔루션) -> F(마이그레이션) -> G(구현 거버넌스) -> H(아키텍처 변경 관리). **ArchiMate 3.1** 표기법으로 시각화 |

### 핵심 원리 — Goal Cascade(목표 연쇄) 알고리즘

```text
+-------------------------------------------------------------+
|         COBIT 2019 Goal Cascade 5-Stage Mapping             |
+-------------------------------------------------------------+
|                                                             |
|  Stage 1: 비즈니스 목표 (13개)                              |
|   BMG01 신사업 수익 | BMG02 시장 점유율 | BMG03 고객 경험    |
|   BMG04 통합·간소화 | BMG05 비용 최적화 | BMG06 규제 준수   |
|            v 양방향 매핑                                     |
|  Stage 2: 정렬 목표 (13개)                                  |
|   AGM01 IT 준수·지원 | AGM02 IT 거버넌스 | AGM03 비즈니스   |
|           모빌리티 | AGM04 IT 비용 | AGM05 비즈니스 응답성  |
|            v 우선순위 적용 (PAM 6단계로 측정)               |
|  Stage 3: 거버넌스 목표 (5개 EDM) + 관리 목표 (32개)        |
|   EDM01~05 + BAI/DSS/MEA/APO/EDM Process (총 40개)         |
|            v 프로세스 활동(Activity)                        |
|  Stage 4: 관리 실무 (Management Practice, ~250+ 활동)      |
|            v 입력/출력/역할/메트릭                           |
|  Stage 5: 기술 컴포넌트 & 서비스                            |
|                                                             |
+-------------------------------------------------------------+
```

### CSF(Kritikal 성공 요인) & KPI 설정 원리

- **CSF 1: 가치 실현(Value Realization)**: KPI = `Realized Benefits / Planned Benefits` (목표 ≥ 80%)
- **CSF 2: 서비스 가용성**: KPI = `MTBF / (MTBF + MTTR) × 100` (목표 ≥ 99.95% for Tier-1)
- **CSF 3: 보안 사고율**: KPI = `Confirmed Incidents / Total Workforce × 1,000` (금융업 ≤ 0.5)
- **CSF 4: 프로젝트 정시율**: KPI = `On-Time Delivery %` (목표 ≥ 85%)
- **CSF 5: ROI**: KPI = `(Net Benefit / Total Cost) × 100` (목표 ≥ 연 12%)

- **📢 섹션 요약 비유**: **"Goal Cascade는 마치 회계의 '이익 -> 매출 -> 거래 -> 재무제표 항목'처럼 거시 목표가 미시 통제 항목으로 흘러내려가게 만드는 '도립 깔때기(Inverted Funnel)' 구조이다."**

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4 (2019)** | **ISO 27001:2022** | **ISO 20000-1:2018** | **TOGAF 10 (2022)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주체/소유** | ISACA(미국) | AXELOS -> PeopleCert(영국) | ISO/TC 262 | ISO/TC 260 | The Open Group |
| **주요 목적** | 거버넌스(누가 무엇을 결정) | 서비스 관리(어떻게 가치를 전달) | 정보보호 통제(보안 인증
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 447 / 800

<- **이전**: [446. IT 경영 관리 핵심 토픽 446번 시험 요약](/studynote/12_it_management/05_security_compliance/446_it_management_core_topic_446_exam_summary/)
**다음**: [448. IT 경영 관리 핵심 토픽 448번 시험 요약](/studynote/12_it_management/05_security_compliance/448_it_management_core_topic_448_exam_summary/) ->

---
