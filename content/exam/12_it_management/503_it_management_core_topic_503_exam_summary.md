---
title: "IT Management Core Topic 503 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 토픽 503은 COBIT 2019 거버넌스 체계, ITIL 4 서비스 가치 체계(34개 실무 가이드, 9개 원칙), ISO 38500 6원칙, TOGAF ADM 10단계, BSC 4관점 KPI 체계를 통합하여 IT-비즈니스 정렬(IT-Business Alignment)을 달성하는 종합 프레임워크 적용 역량을 평가한다.
> 2. **가치**: 적정 거버넌스 체계 수립 시 IT 투자 대비 ROI를 평균 23~35% 개선(Forrester, 2023), EA 기반 중복 투자 제거로 5년간 CapEx 18~27% 절감, IT 인시던트 MTTR 47% 단축(AXELOS Global State of ITSM Report 2024), 정보화 사업 실패율 70%->28% 감소 가능(Standish Group CHAOS Report 2023 기준 적용 시).
> 3. **판단 포인트**: 거버넌스 프레임워크 선택 시 COBIT(제어·감사 중심) vs ITIL(서비스 운영 중심) vs ISO 38500(이사회 거버넌스 원칙) 트레이드오프, Build vs Buy vs Rent, 전사 아키텍처 4종(BA/DA/AA/TA) 적용 우선순위, 사이버보안 ISO 27001:2022 Annex A 93개 통제 항목 중 4개 속성(Preventive/Detective/Corrective/Hybrid) 분류, K-ICTBSM·K-ECS 인증 요건 충족 여부 판단이 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

정보시스템 분야의 기술사(Professional Engineer in Information Systems) 시험에서 IT 경영 관리 토픽은 단순 암기가 아닌 **실무 의사결정 역량과 다층 프레임워크 통합 적용 능력**을 측정한다. 토픽 503번은 IT 거버넌스, IT 전략 기획, IT 서비스 관리(ITSM), 정보화 투자 분석, EA(Enterprise Architecture), 정보보안 거버넌스, IT 위험 관리, IT 성과 측정, IT 아웃소싱, BCP/DRP, 디지털 전환, 그리고 ESG·지속가능성까지 **12개 세부 영역을 망라하는 종합 관리 역량**을 평가한다.

2010년대 이후 디지털 전환(DX), 클라우드 컴플라이언스, AI 거버넌스, ESG 공시 의무화(K-ESG 가이드라인 2021, IFRS S1/S2 2024 시행) 등으로 IT 경영의 복잡도가 기하급수적으로 증가함에 따라, 기술사는 **다수의 글로벌 표준(COBIT 2019, ITIL 4, ISO 38500, ISO 27001:2022, ISO 20000-1:2018, TOGAF 10, CMMI v2.0, PMBOK 7th)을 통합 적용**할 수 있는 능력이 요구된다. 과거(2000년대)에는 ITIL v2/v3 기반의 프로세스 중심 관리가 주류였으나, 현재는 **거버넌스-전략-운영-보안-리스크-성과의 6축 통합 체계**가 필수다.

```text
+-------------------------------------------------------------------------+
|           IT 경영 관리 6대 축 통합 프레임워크 (Topic 503)               |
+-------------------------------------------------------------------------+
|                                                                         |
|   +---------------+    +---------------+    +---------------+         |
|   | ① 거버넌스    |---->| ② 전략/EA     |---->| ③ 서비스 운영 |         |
|   |  - COBIT 2019 |    |  - TOGAF 10   |    |  - ITIL 4     |         |
|   |  - ISO 38500  |    |  - Zachman    |    |  - ISO 20000  |         |
|   |  - King III/IV|    |  - FEA/DODAF  |    |  - SIAM       |         |
|   +---------------+    +---------------+    +---------------+         |
|            |                  |                    |                    |
|            v                  v                    v                    |
|   +---------------+    +---------------+    +---------------+         |
|   | ④ 정보보안    |<---->| ⑤ 리스크/감사 |<---->| ⑥ 성과측정    |         |
|   |  - ISO 27001  |    |  - ISO 31000  |    |  - BSC/OKR    |         |
|   |  - NIST CSF   |    |  - COSO ERM   |    |  - KPI/KRI    |         |
|   |  - ISMS-P     |    |  - ISACA audit|    |  - TCO/ROI    |         |
|   +---------------+    +---------------+    +---------------+         |
|                                                                         |
|   [공통 기반] 정보화진흥법, 개인정보보호법, 클라우드컴퓨팅법,             |
|              전자문서법, 네트워크이용촉진법, 전자상거래법               |
|                                                                         |
+-------------------------------------------------------------------------+

  +- 시나리오: 503번 시험 출제 의도 ---------------------------------+
  |  • "금융기관 클라우드 전환 시 거버넌스 체계 설계"                 |
  |  • "공공기관 EA 수립 시 TOGAF ADM 단계별 산출물 도출"             |
  |  • "ITIL 4 SVS 도입 시 34개 실무 가이드 우선순위 매핑"            |
  |  • "정보화 투자 사업의 NPV/IRR 산출 및 B/C 분석"                 |
  |  • "ISMS-P 인증 심사 시 Annex A 93개 통제 항목 평가"             |
  +-----------------------------------------------------------------+
```

- **기존 vs 신규 패러다임**:
  - **기존(2010 이전)**: ITIL v3 5단계 전략-설계-전환-운영-개선의 프로세스 흐름, COBIT 5 5원칙 + 7카테고리 37개 프로세스, EA는 Zachman 6×6 매트릭스 단순 적용, 보안은 ISMS-P 12개 분야 80개 통제 항목, 성과측정은 단순 ROI 계산에 머묾.
  - **신규(2024 이후)**: **COBIT 2019**의 Focus Area(예: DevOps, Cyber Security, Privacy, ESG) 50여 개 추가, **ITIL 4**의 Service Value System(4P+7P 원칙) 및 Value Stream 중심 사고, **ISO 27001:2022** Annex A 93개 통제(4개 속성: 예방/탐지/교정/혼합), **TOGAF 10**의 ADM 10단계 + Microservice Architecture 지원, **ISO/IEC 42001:2023 AI 경영시스템**, 디지털 윤리, 클라우드 컴플라이언스(KCS, CSAP, ISMS-C 인증) 등 신규 영역.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **대형 건축물의 설계·시공·유지관리·리모델링을 총괄하는 건축주(CM at Risk)**와 같다. 토대(거버넌스) -> 골조(EA) -> 설비·전기(서비스 운영) -> 방재시설(보안) -> 하자보증(리스크) -> 가치평가(성과측정)가 동시에 맞물려야 흔들리지 않는 빌딩이 완성된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) COBIT 2019 (Control Objectives for Information and Related Technologies)

ISACA가 발표한 IT 거버넌스·관리 프레임워크로, **6개 거버넌스 시스템 원칙**(Each Enterprise, Holistic, Dynamic, Customizable, Managed, Optimized)과 **40개 거버넌스/관리 목적(Goals)**, **4개 도메인**(EDM: Evaluate/Direct/Monitor, APO: Align/Plan/Organize, BAI: Build/Acquire/Implement, DSS: Deliver/Service/Support, MEA: Monitor/Evaluate/Assess) 5개로 구성된 40개 핵심 모델 + 50+ 디자인 팩터(Design Factor) 기반 **맞춤형 거버넌스 시스템(Governance System)** 설계가 핵심이다.

```text
+---------------------- COBIT 2019 거버넌스 시스템 구조 ------------------+
|                                                                         |
|  +-------------------------------------------------------------+       |
|  |        거버넌스 목적 13개 + 관리 목적 27개 (총 40개)        |       |
|  |   EDM: 05 / APO: 14 / BAI: 11 / DSS: 06 / MEA: 04          |       |
|  +-------------------------------------------------------------+       |
|                                |                                         |
|  +--------------+  +--------------+  +--------------+  +-----------+  |
|  |  ① 원칙(6)   |  | ② 목표계단도 |  | ③ 7 컴포넌트 |  |④ 50+ 설계 |  |
|  |  - Stakehold.|  |   Stakeholder|  |  Process     |  |  팩터(DF) |  |
|  |  - Holistic   |  |   Goals(13)  |  |  Information |  |  - Strategy| |
|  |  - Dynamic    |--->|       |      |  Structures  |--->|  - Goals  | |
|  |  - Customiz.  |  |   Goals(13)  |  |  People      |  |  - Risk   | |
|  |  - Managed    |  |       |      |  Culture      |  |  - Size   | |
|  |  - Optimized  |  |   Enabler(40)|  |  Technology  |  |  - Compli.| |
|  +--------------+  +--------------+  +--------------+  +-----------+  |
|                                |                                         |
|  +-------------------------------------------------------------+       |
|  |  ⑤ Focus Area: DevOps, Cyber Security, Privacy, ESG,        |       |
|  |                Cloud, Digital Transformation, AI Governance  |       |
|  |  ⑥ 목표계단도(Goals Cascade): Stakeholder->Enterprise->IT->Enabler |   |
|  +-------------------------------------------------------------+       |
+-------------------------------------------------------------------------+
```

### 2) ITIL 4 (Information Technology Infrastructure Library, Version 4)

AXELOS(현재 PeopleCert)에서 관리하며, **서비스 가치 시스템(SVS: Service Value System)**이 핵심이다. 34개 실무 가이드(1개 Foundation + 8개 Create/Deliver/Support + 7개 Drive Stakeholder Value + 4개 High Velocity IT + 5개 Plan/Implement/Improve + 9개 Manage/Direct 모듈) + **9개 guiding principle**(Focus on Value, Start Where You Are, Progress Iteratively, Collaborate and Promote Visibility, Think and Work Holistically, Keep It Simple and Practical, Optimize and Automate).

### 3) ISO/IEC 38500:2015 (이사회 수준 IT 거버넌스 국제표준)

이사회가 준수해야 할 **6원칙**(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)과 **3개 태스크**(Evaluate, Direct, Monitor)로 구성된 ISO 표준으로, 전 세계 IT 거버넌스 국제 인증(ISO 38500 Lead IT Governance Manager) 시험의 근간.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 Governance System** | 전사 IT 통제·관리·감사 통합 프레임워크 | 40개 목적(13 거버넌스+27 관리) + 5개 도메인(EDM/APO/BAI/DSS/MEA) + 7개 컴포넌트 + 50+ 설계 팩터 기반 맞춤형 거버넌스 시스템. **목표계단도(Cascade)**로 13개 Stakeholder Goal -> 13개 Enterprise Goal -> 13개 IT-related Goal -> 40개 Enabler Goal을 정량적 매핑 |
| **TOGAF 10 ADM** | 전사 아키텍처(EA) 개발 방법론 | **ADM(Architecture Development Method) 10단계**: Preliminary -> A(비전) -> B(비즈니스) -> C(데이터+애플리케이션) -> D(기술) -> E(기회/솔루션) -> F(구현 거버넌스) -> G(구현) -> H(아키텍처 변경관리) -> R(요구사항 관리). **무용한 ADM(Iterative ADM)** 4종(기술/데이터/능력/비즈니스), **4개 영역(BA/DA/AA/TA)** 통합 |
| **ITIL 4 SVS** | 서비스 가치 창출·제공·지원 통합 체계 | **5개 Activity 체인**: Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support + **7개 guiding principle**. **34개 실무 가이드**, 4개 차원(Organizations & People, Information & Technology, Partners & Suppliers, Value Streams & Processes) 기반 서비스 설계 |
| **ISO 27001:2022 ISMS** | 정보보호 경영시스템 | **93개 Annex A 통제 항목**(5개 속성: Organisational 37, People 8, Physical 14, Technological 34). **4가지 통제 속성**(Preventive 53 / Detective 15 / Corrective 3 / Hybrid 22). PDCA + 위험평가(Risk Assessment) + Statement of Applicability(SoA) 작성 |
| **BSC 4관점 KPI** | 전략 실행을 위한 균형 성과표 | **4관점 KPI**: Financial(ROA, EVA, Cash Flow) / Customer(CSI, NPS) / Internal Process(Cycle Time, Defect Rate) / Learning&Growth(직원 만족도, Retention). **Strategy Map** 인과관계 + **KPI 가중치(SMART 원칙)** 산정 |
| **K-ISMS / ISMS-P** | 국내 정보보호·개인정보 관리체계 인증 | 과학기술정보통신부 고시. K-ISMS 64개 통제영역 / ISMS-P 80개 통제영역, 인증 심사 주기 3년, **인증 등급 4단계(우수/적합/부분적합/미흡)**, 금융·공공·의료 등 19개업종 의무 |
| **TCO/ROI/PPNP 모델** | 정보화 투자 정량 분석 | **TCO**(Total Cost of Ownership): 직접(하드웨어/소프트웨어)+간접(교육/다운타임/지원) 비용. **ROI** = (총편익-총비용)/총비용 × 100. **NPV** = Σ[(Bₜ-Cₜ)/(1+r)ᵗ] - I₀. **B/C Ratio** ≥ 1.0, **IRR** ≥ 사회적할율율(현재 4.5%) |

**핵심 알고리즘·수식**:

- **CobiT 2019 목표계단도 정량 매핑**: Stakeholder Goal G1(Profitability) ↔ Enterprise Goal EG01(Portfolio of competitive products/services) ↔ IT Goal ITG05(Realized business benefits) ↔ Enabler Goal(예: APO12.01: Manage risk). 매핑 시 가중치 0~100% 부여 후 정합성 검증.
- **BIA(Business Impact Analysis) RTO/RPO 산정**: RTO(Recovery Time Objective) = MTPD(Maximum Tolerable Period of Disruption) - MTRS(Mean Time to Restore Service). RPO = MTPDF - MLOS. 예: 24시간 업무 중단 시 손실 1억원 -> MTPD 24h, RTO 6h, RPO 1h 목표 설정.
-
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 503 / 800

<- **이전**: [502. IT 경영 관리 핵심 토픽 502번 시험 요약](/studynote/12_it_management/05_security_compliance/502_it_management_core_topic_502_exam_summary/)
**다음**: [504. IT 경영 관리 핵심 토픽 504번 시험 요약](/studynote/12_it_management/05_security_compliance/504_it_management_core_topic_504_exam_summary/) ->

---
