---
title: "IT Management Core Topic 686 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스·ITIL 4 서비스 가치 시스템·COBIT 2019·EA·디지털전환을 단일 프레임워크로 통합·조정하여, 전략-설계-구축-운영-평가의 전 라이프사이클을 엔터프라이즈 단위로 통제하는 경영 통치 체계
> 2. **가치**: 도입 기업 평균 IT 비용 20~30% 절감, 서비스 가용성 99.95% 이상 달성, 핵심 프로젝트의 ROI 3년 내 1.8배, 이사회-경영진-실무의 의사결정 지연 70% 단축(AXELOS/ISACA 벤치마크 기준)
> 3. **판단 포인트**: 거버넌스-관리-운영의 3층 분리, Push 거버넌스 vs. Pull 거버넌스, 4-tier balanced scorecard 균형(재무/고객/내부/학습성장), 사이버 리스크 허용한도(Risk Appetite) 설정, Agile/DevOps 문화와 통제 구조의 충돌 조정

---

## Ⅰ. 개요 및 필요성

전통적 IT 관리는 CIO 산하의 비용센터 단위 운영으로, ① 전략과 운영의 괴리, ② 분산된 통제 체계(중복된 SLA/감사/보고), ③ 사이버 위협·규제(개인정보보호법, ISO 27001, DORA, NIS2) 강화에 따른 통제 공백, ④ 클라우드·AI 도입으로 인한 책임 한계 모호화에 직면해 있다. 한국인터넷진흥원(KISA)의 2023년 정보보호 실태조사에서도, 국내 대기업의 64%가 "IT 투자 대비 가치 측정이 어렵다"고 응답했으며, 동일 조사에서 47%가 "IT 거버넌스 체계가 수립되어 있지 않다"고 보고했다.

이에 2018년 이후 ISACA의 **COBIT 2019**(목표 계단식 Cascade of Goals + 40개의 관리/거버넌스 목표), AXELOS의 **ITIL 4**(Service Value System, 4 P's 모델), 그리고 **TOGAF 10**(ADM 사이클)을 통합적으로 운용하는 '통합 거버넌스' 패러다임이 글로벌 표준으로 자리 잡았다.

기존 COBIT 5(2012)에서는 프로세스 중심의 5개 도메인(EDM, APO, BAI, DSS, MEA)이었으나, COBIT 2019부터는 ① 40개의 Governance/Management Objectives, ② 7가지 컴포넌트(원칙/정책/프레임워크/문화/인적자원/정보/서비스/구조/기술), ③ Focus Area(예: 사이버보안, DevOps, 위험) 단위 맞춤형 설계로 전환되었다.

```text
+----------------------------------------------------------------------+
|            통합 IT 거버넌스 패러다임 (Enterprise View)                |
+----------------------------------------------------------------------+
|                                                                      |
|   +------------------- 전략 계층(Strategy) ---------------------+   |
|   |  BSC/OKR · 이사회 KPI · ISO/IEC 38500 · 코비트 EDM 5대목표  |   |
|   +-------------------------+------------------------------------+   |
|                             | Cascade of Goals                       |
|   +----------------------- 설계 계층(Design) -------------------+   |
|   |  TOGAF ADM · EA Repository(ArchiMate) · 용어/원칙/표준      |   |
|   +-------------------------+------------------------------------+   |
|                             | Architecture Contract                  |
|   +----------------------- 구축·운영 계층(Build·Run) ------------+   |
|   |  ITIL 4 SVS · 34개 Practice · DevOps/CI/CD · AIOps            |   |
|   +-------------------------+------------------------------------+   |
|                             | SLA/OLA/UC                            |
|   +----------------------- 통제 계층(Control) ------------------+   |
|   |  COBIT 2019 · 40 Gov/Mgt Objectives · NIST CSF · ISMS-P    |   |
|   +-------------------------------------------------------------+   |
|                                                                      |
|   +--------------- 외부 정합성(External Alignment) -------------+   |
|   |  GDPR/PIPA · PCI-DSS · ESG · K-IFRS · DORA/NIS2/AI Act     |   |
|   +-------------------------------------------------------------+   |
+----------------------------------------------------------------------+
```

종래의 COBIT 5(프로세스 -> 목표 -> 메트릭 -> maturity level의 단방향 구조)와 달리, COBIT 2019 이후의 거버넌스는 **양방향 피드백(Governance ↔ Management) + Focus Area별 맞춤형**으로 작동하며, 이는 디지털 전환(AI, 클라우드, 데이터) 시나리오에 따라 거버넌스 체계를 재구성할 수 있게 한다. 즉, "One-Size-Fits-All" 거버넌스에서 "Composable Governance"로 패러다임이 이동했다.

- **📢 섹션 요약 비유**: 거버넌스는 마치 **도시의 종합 계획**(토지이용·교통·환경·재정)이 한 장의 도면 위에서 조정되는 것과 같다. 빌딩 하나(시스템)를 잘 세우는 것보다, 도시 전체의 조화(엔터프라이즈 정합)를 설계하는 것이 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019의 6단계 거버넌스 시스템(Governance System Design Workflow)

```text
[1단계] 경영 문제·동기 식별 ---> [2단계] 비전·전략·도전과제 정렬
       |                                       |
       v                                       v
[3단계] 거버넌스 시스템 설계 <---- 정렬된 목표
       |   (Scope, Components, Focus Areas)
       v
[4단계] 거버넌스 목표 연결(Goal Cascade)
       |   Enterprise Goal -> Alignment Goal -> Mgmt Goal
       v
[5단계] 관리/거버넌스 목표 선정(40개 중 우선순위)
       |   Primary/Secondary, Rating: 0~100
       v
[6단계] 컴포넌트별 상세화 + KPI 설정
           |
           v
       구현/모니터링
```

**핵심 메커니즘 – 목표 계단식(Cascade of Goals)**

- **엔터프라이즈 목표 13개** -> **정렬 목표(Alignment) 13개** -> **거버넌스/관리 목표 40개**로 분해
- 각 단계는 **라커(Likert) 스케일 매핑**(0=Not, 1=Initial, 2=Managed, 3=Defined, 4=Quantitative, 5=Optimized)으로 우선순위 산정
- 예시: EG01 *재무 포트폴리오의 경쟁 우위* -> AG11 *IT 거버넌스 프레임워크* -> MGD02 *관리 시스템에 대한 책임·의사결정·역할 정의* -> EDM(evaluate, direct, monitor) 5대 활동

### 2. ITIL 4 Service Value System (SVS) 7개 구성요소

```text
        Opportunity/Demand (외부)
              |
              v
   +-------------------------+
   |   ITIL SVS 핵심      | <---- Guiding Principles(7개 원칙)
   |  +----------------+    |       • Focus on value
   |  | Service Value  |    |       • Start where you are
   |  |   Chain(6활동) |    |       • Progress iteratively
   |  | Plan->Engage->   |    |       • Collaborate & promote visibility
   |  | Design->Obtain-> |    |       • Think and work holistically
   |  | Deliver->Improve|    |       • Keep it simple & practical
   |  +----------------+    |       • Optimize & automate
   +-------------------------+
              |
              v
        Value(가치) ----> Customer/공급자/소유자
              ^
              |
   +-------------------------+
   |  Practices (34개)      |
   |  • General Mgmt(15)    |
   |  • Service Mgmt(17)    |
   |  • Technical Mgmt(3)   |
   +-------------------------+
              |
   +-------------------------+
   |  Continual Improvement | <---- 7-step CI Model
   +-------------------------+
```

### 3. 거버넌스/관리 목표 40개 중 핵심 매핑 사례

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(EDM01~05)** | 이사회 거버넌스 5대 활동 | Evaluate(현황평가) -> Direct(방향결정) -> Monitor(성과모니터링); 예: EDM04 *Resource Optimization*(BSC 연계) |
| **APO(APO01~14)** | Align-Plan-Organize | 전략-수요-예산-포트폴리오 정렬; APO05 *Portfolio Mgmt*는 Stage-Gate + BCG Matrix 활용 |
| **BAI(BAI01~11)** | Build-Acquire-Implement | 프로그램/프로젝트 관리 + 변경관리; BAI03 *Manage Solutions*는 ArchiMate 모델로 영향도 분석 |
| **DSS(DSS01~06)** | Deliver-Service-Support | 운영 SLA/OLA, Incident/Problem/Request Fulfilment; DSS02 *Service Requests*의 90% 표준화 목표 |
| **MEA(MEA01~04)** | Monitor-Evaluate-Assess | Internal Control + Compliance + Performance; MEA03 *Compliance*는 ISMS-P 인증 + 통제 자체평가(83개 통제기준) |
| **Focus Area: DevOps** | 문화+자동화 통합 | COBIT 2019 DevOps Focus Area(2019.04 발표)로 Agile/DevOps에 11개 통제 제공 |
| **Focus Area: Cyber Security** | 사이버 리스크 통합 | NIST CSF(Identify/Protect/Detect/Respond/Recover) + COBIT 통제 매핑 1:1 |
| **Focus Area: Risk** | 리스크 정량화 | FAIR(ISO/IEC 31000) 기반 ALE(연간예상손실), Appetite·Tolerance 설정 |

**주요 메트릭 및 알고리즘**

- **CMMI 성숙도 모델(5단계)**: Initial(0~30점) -> Managed(31~60) -> Defined(61~80) -> Quantitatively Managed(81~90) -> Optimizing(91~100)
- **가치 흐름 매핑(VSM)**: Lead Time = Process Time + Wait Time; ITIL SVS Value Chain의 6개 활동별 Lead Time 측정
- **BSC 4 관점 가중치**: 재무 25% / 고객 25% / 내부 프로세스 30% / 학습성장 20% (대형 SI 표준안)
- **리스크 정량화**: NPV-at-Risk(95% VaR) = Σ(연간 ALE × 발생확률 × 영향도)
- **자동화 지수(AIX)**: (자동화 처리 건수 / 전체 처리 건수) × 100; COBIT 2019 BAI08의 KPI

- **📢 섹션 요약 비유**: COBIT는 **건물의 구조도**, ITIL은 **건물 안의 서비스 운영 매뉴얼**, TOGAF는 **건축가의 설계도**, BSC는 **입주자 만족도 조사표**라고 할 수 있다. 네 가지가 같은 도면 좌표(목표·메트릭·프로세스)를 공유해야 진정한 통합 거버넌스가 된다.

---

## Ⅲ. 비교 및 연결

### 1. 핵심 프레임워크 비교

| 구분 | **COBIT 2019** | **ITIL 4** | **TOGAF 10** | **CMMI v2.0** | **ISO/IEC 38500** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 | IT 서비스 관리 | 엔터프라이즈 아키텍처 | 프로세스 성숙도 | IT 거버넌스 원칙 |
| **구조** | 40 Gov/Mgt Obj. + 7 Component | SVS + 34 Practice + Value Chain | ADM 10단계 | 5/6 단계(Level 1~5) | 6 원칙(책임/전략/획득/성과/규정/인간) |
| **중심 축** | 목표(Goal) | 가치(Value) | 아키텍처(ADM) | 성숙도(Maturity) | 원칙(Principle) |
| **대상** | CIO·이사회·감사 | 서비스 매니저·운영 | 아키텍트·전략기획 | 품질·개발조직 | 이사회·최고 의사결정자 |
| **산출물** | Goals Cascade Matrix | Service Catalog, SLA, Value Stream | Architecture Repository | Maturity Profile | Governance Charter |
| **측정** | Process Capability 0~5 | SLA/MTTR/MTBF/AHT | Architecture Compliance | Maturity Score 1~5 | Principle Compliance Index |
| **연계 방식** | 다른 프레임워크의 통제 매핑 | COBIT의 BAI/DSS 영역 | COBIT의 APO/BAI 영역 | 프로세스 측정 보완 | 상위 거버넌스 헌장 |

### 2. 통합 연계 매핑 사례

- **COBIT APO05(Portfolio) ↔ TOGAF ADM Phase A(Architecture Vision)**: 둘 다 비즈니스 동기·제약조건·Stakeholder Needs를 입력으로 사용
- **COBIT BAI02(Manage Requirements) ↔ TOGAF ADM Phase B/C**: 아키텍처 요구사항 정의 단계에서 BAI02의 *Requirements Definition Mgmt* Practice 활용
- **ITIL Change Enablement ↔ COBIT BAI03 ↔ TOGAF ADM Phase H**: 변경관리를 3중으로 통제(서비스 영향, 거버넌스 영향, 아키텍처 영향)
- **BSC 4 관점 ↔ COBIT 40 목표 ↔ KPI**: 13개 Enterprise Goal 각각을 4 관점에 매핑, 각 목표당 1~4개의 Lead Indicator + 1개의 Lag Indicator 설정

```text
   [전략 의도] ---  ISO/IEC 38500 6
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 686 / 800

<- **이전**: [685. IT 경영 관리 핵심 토픽 685번 시험 요약](/studynote/12_it_management/05_security_compliance/685_it_management_core_topic_685_exam_summary/)
**다음**: [687. IT 경영 관리 핵심 토픽 687번 시험 요약](/studynote/12_it_management/05_security_compliance/687_it_management_core_topic_687_exam_summary/) ->

---
