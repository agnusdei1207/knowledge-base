+++
title = "779. IT 경영 관리 핵심 토픽 779번 시험 요약 (IT Management Core Topic 779 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019, ITIL 4, ISO/IEC 38500, BSC(Balanced Scorecard)**를 통합한 거버넌스-전략-성과-ITIL 운영의 4축 구조로, **EA(Enterprise Architecture)**와 **정보화 사업 관리**를 매개로 IT-PMF(KPI) 기반의 가치 실현 사슬을 구축하는 것임.
> 2. **가치**: 효과적인 IT 거버넌스 적용 시 **IT 투자 ROI 20~30% 개선**, 정보화 사업 **성공률 28% -> 65% 향상**(Standish Group CHAOS Report 기준), 의사결정 속도 40% 단축, 그리고 ISO 38500·ISMS-P 인증을 통한 규제 준수 및 대외 신뢰도 확보.
> 3. **판단 포인트**: **거버넌스 성숙도(L1~L5)**, **IT-Portfolio의 Run/Grow/Transform 비율(통상 70:20:10)**, **BSC 4관점(재무/고객/내부/학습성장) KPI 정합성**, 그리고 COBIT 2019의 **40개 거버넌스/관리 목표(GO/MG)** 중 조직 맥락에 맞는 설계 계수가 핵심 의사결정 기준.

---

## Ⅰ. 개요 및 필요성

정보화 사업의 실패율(전통적 waterfall 방식 약 70%)과 IT-Business 정렬 미흡(Gartner survey: CFO의 60%가 IT 가치 입증 불만족) 문제를 해결하기 위해 등장한 통합 IT 경영 관리 패러다임은 단순 시스템 도입을 넘어 **전략-거버넌스-아키텍처-운영-성과**의 End-to-End 관리 체계를 요구합니다. 과거 SI 중심의 **프로젝트 단위 관리**(개별 시스템 납품)와 달리, 현재는 **EA 기반 포트폴리오 관리**(Business Capability -> Application -> Technology 계층) 및 **DevOps + SRE** 기반의 지속적 가치 제공(Continuous Delivery) 모델로 전환되었습니다.

```text
+------------------------------------------------------------------+
|        IT 경영 관리 4대 영역 통합 프레임워크 (Top-Down)         |
+------------------------------------------------------------------+
|                                                                  |
|  [1] 전략기획      [2] 거버넌스      [3] 아키텍처    [4] 운영/성과|
|  +---------+     +----------+     +----------+  +----------+   |
|  |ISP 수립 | ---> |COBIT2019 | ---> |EA(TOGAF) |-->|ITIL 4    |   |
|  |BSC/CSF |     |ISO 38500 |     |FEAF/DODAF|  |SRE/DevOps|   |
|  |SW사업법|     |RACI/Risk |     |ArchiMate |  |IT-PMF    |   |
|  +----+----+     +----+-----+     +----+-----+  +----+-----+   |
|       |               |                |              |         |
|       +---------------+----------------+--------------+         |
|                            v                                     |
|                  +----------------------+                       |
|                  | Value Realization    |                       |
|                  | (ROI/NPV/Payback)   |                       |
|                  +----------------------+                       |
+------------------------------------------------------------------+

  * RACI: Responsible, Accountable, Consulted, Informed
  * CSF: Critical Success Factor / IT-PMF: IT Performance Measurement Framework
```

- **📢 섹션 요약 비유**: IT 경영 관리는 **항공우주 산업의 IMOC(통합 mission operation center)**과 같습니다. 발사(전략), 궤도(거버넌스), 기체설계(아키텍처), 비행제어(운영) 4개 부서가 실시간 데이터로 연결되어야 임무 성공(가치 실현)이 가능합니다. 한 부서라도 정렬이 어긋나면 미션 실패(=사업 실패)로 직결됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **전략-거버넌스-아키텍처-운영-성과** 5계층을 단일 **가치 사슬(Value Chain)**로 통합하는 것이며, **PDCA(Plan-Do-Check-Act)** 사이클을 COBIT 2019의 EDM(Evaluate, Direct, Monitor) -> APO(Align, Plan, Organize) -> BAI(Build, Acquire, Implement) -> DSS(Deliver, Service, Support) -> MEA(Monitor, Evaluate, Assess) 5개 도메인에 매핑합니다.

```text
            +---------------------------------------------+
            |  Stakeholder Needs & Strategic Objectives   |
            +----------------------+----------------------+
                                   v
   +---------------------------------------------------------+
   |  EDM: 거버넌스 의사결정 (Board/CxO)                      |
   |  - 목표설정, Risk Appetite, Resource Optimization        |
   +----------------------+----------------------------------+
                          v
   +---------------------------------------------------------+
   |  APO: 전략/계획/조직 정렬                                |
   |  - APO01~14: 전략연계, 포트폴리오, 예산, 인력, 위험      |
   +-----+----------+----------+----------+-----------------+
         v          v          v          v
       BAI(구축)  DSS(운영)  MEA(평가)  (반복 루프)
         |          |          |
         +----------+----------+
                v
   +---------------------------------------------------------+
   |  성과지표(IT-PMF) -> BSC 4관점 KPI -> Value Realization  |
   +---------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **전략기획 (ISP)** | 3~5년 중장기 IT 로드맵 | MECE 원칙의 SWOT/Cross-Impact 분석, **CSF-->KPI-->KPI Tree** 도출, **정보화사업 추진계획 수립 가이드라인(행정안전부)** 기반 중기계획 |
| **거버넌스(COBIT 2019)** | IT 의사결정·통제 구조 | **40 Governance/Management Objectives(5 domains × 평균 8 GO/MG)**, RACI Chart, **Design Factors 11개**(전략, 목표, 위험, 이슈, 위협, 적격성, 역할, IT 이슈, 적응력, 위험관리방법, 준수비용) -> 40개 목표 중 약 25~30개 우선적용 |
| **EA(Enterprise Architecture)** | 현행/목표 아키텍처 모델링 | **TOGAF ADM(Architecture Development Method) 8단계**(Preliminary->A:비전->B:비즈니스->C:데이터/앱->D:기술->E:기회->F:마이그레이션->G:구현관리), **ArchiMate 3.1**(3 Layers: Business/Application/Technology × 6 Aspects: Active/Structure/Behavior/Passive/Composite) |
| **IT 운영(ITIL 4)** | 서비스 가치 사슬(SVC) | **34 Practices**(일반 14, 서비스 17, 기술 3), **Service Value Chain**(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve), **4D 모델(Dimension)**: 조직/정보/파트너/가치흐름 |
| **성과측정(IT-PMF/BSC)** | IT 가치 정량화 | **BSC 4관점**(Financial/Customer/Internal Process/Learning & Growth) × **IT-PMF 5관점**(IT investment, IT user, IT operation, IT capability, IT contribution), **KPI 예**: 시스템 가용성 99.9%, MTTR 30분, CSAT ≥ 4.2/5 |

**핵심 원리 심화**

- **COBIT 2019의 Cascade Goals**: Stakeholder needs -> Enterprise goals(13개) -> Alignment goals(13개) -> Governance/Management objectives(40개)의 **4단계 인과 사슬**. 예: Stakeholder "성장" -> Enterprise Goal 01(포트폴리오 경쟁제품 80%) -> Alignment Goal 02(전략적 신기술 투자) -> EDM02(가치 최적화), APO05(포트폴리오 관리), APO12(위험 관리).
- **BSC 4관점 KPI 설계 공식**: `KPI = 기준값 + 측정공식 + 목표치 + 측정주기 + Data Source`. 예: "프로젝트 성공률 ≥ 85% = (성공 프로젝트 수 / 전체 프로젝트 수) × 100, 월간 측정, PMO 데이터".
- **IT 투자 우선순위 모델**: **AHP(Analytic Hierarchy Process)**, **TOPSIS**(다기준 의사결정), **NVP/IRR/Payback Period**, 그리고 **BOCR**(Benefit-Opportunity-Cost-Risk) 분석. 공공부문은 **정보시스템 사업 대가산정 가이드**, **예산·성과 연동 성과관리** 적용.
- **EA와 프로젝트 연결**: Capability 기반 로드맵 -> GAPS 분석(현행 AS-IS vs 목표 TO-BE) -> **Transition Architectures(단계별)** -> **Work Package** -> Project Charter로 BAI 단계 진입.

- **📢 섹션 요약 비유**: IT 경영 관리의 5계층은 **인체의 신경계**와 같습니다. **전략(대뇌피질, 의도)** -> **거버넌스(변연계, 의사결정)** -> **아키텍처(골격·근육, 구조)** -> **운영(자율신경계, 생명유지)** -> **성과(행동 출력, KPI)**. 어느 하나라도 손상되면 전체 시스템이 마비됩니다.

---

## Ⅲ. 비교 및 연결

| 구분 | COBIT 2019 (거버넌스) | ITIL 4 (운영) | ISO/IEC 38500 (이사회 거버넌스) | TOGAF (EA) |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 통합 프레임 | IT 서비스 운영 최적화 | 이사회 수준 IT 의사결정 원칙 | 아키텍처 개발 방법론 |
| **적용 범위** | End-to-End(전략->폐기) | 운영·서비스 중심 | 거버넌스 6원칙(책임, 전략, 획득, 성과, 적합, 인적) | 아키텍처 4계층(BDAT) |
| **주 사용자** | CxO, CIO, IT 감사, 컨트롤러 | Service Desk, ITSM 실무자, SRE | 이사회, 감사위원, 비-IT 임원 | EA Architect, PMO |
| **핵심 산출물** | Goals Cascade, RACI, MGF | SVC, 34 Practices, CSI | 6 Principles, 6 Model | ADM 8단계, ArchiMate |
| **성숙도/측정** | Performance Management(Process Capability CMMI 0~5) | Maturity Model(5단계) | 점검 체크리스트(원칙별) | ADM Phase Gate |

**통합 연계 아키텍처**: 실무에서는 **COBIT 2019를 Backbone**으로, **ITIL 4 Practices를 운영 레이어**로, **ISO 38500을 이사회/감사 레이어**로, **TOGAF를 아키텍처 레이어**로 매핑하여 사용합니다. 예: "신규 CRM 도입" -> TOGAF Phase B/C(요구사항·앱아키텍처) -> COBIT BAI02(요구사항관리), BAI03(솔루션 선정) -> ITIL 4 Service Design(Change Enablement) -> ISO 38500 Principle 3(Acquisition: 명확한 의사결정).

| 연계 영역 | 연결 도구/원리 | 실무 적용 |
| :--- | :--- | :--- |
| 전략-거버넌스 | COBIT Cascade Goals + BSC 4관점 | KPI Tree 도출 시 Alignment Goals를 BSC 관점에 매핑 |
| 거버넌스-EA | COBIT EDM02 + TOGAF Preliminary/Phase A | 거버넌스 위원의 EA 승인 권한을 RACI에 명시 |
| EA-운영 | TOGAF Phase E/F + ITIL 4 DSI(Value Chain) | 마이그레이션 계획을 ITIL Change Enablement Practice로 구현 |
| 운영-성과 | ITIL 4 CSI + IT-PMF | Incident/Problem/Change KPI -> IT-PMF 5관점 KPI로 집계 |
| 거버넌스-보안 | COBIT EDM03(위험최적화) + ISMS-P 122개 통제항목 | 위험 등록부(Risk Register) 기반 통제 매핑 |

- **📢 섹션 요약 비유**: 이 4대 프레임워크의 관계는 **의료진 협진**과 같습니다. **COBIT은 주치의(전체 조율)**, **ITIL은 임상간호사(일상 운영)**, **ISO 38500은 의료윤리위원회(원칙 준수)**, **TOGAF은 영상의학과 의사(구조 진단)**입니다. 환자(조직)의 건강(가치) 회복을 위해 모두 같은 EMR(EAM) 데이터를 공유합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **사업 성공률 진단**: 현행 정보화 사업의 Standish Group 기준 **성공(30%)/도전(50%)/실패(20%) 분포**를 분석하고, 실패 원인(요구사항 불명확 35%, 사용자 참여 부족 23%, 자원/일정 부족, 부실계획 등)별 개선 KPI를 도출했는가? 또한 **Chaos Report의 Resolution Factor**(잘 정의된 목적, 경영진 지원, 최적 요구사항 등 8개 항목)에 자사를 대입했는가?
2. **거버넌스 성숙도 측정**: COBIT 2019의 **Process Assessment Model(PAM)** 기반 ISO/IEC 15504 SPICE 0~5 등급을 측정하고, L0(불완전)->L1(초기)->L2(관리)->L3(설정)->L4(예측)->L5(최적화) 중 현 위치를 정량화했는가? **Design Factor 11개** 중 자사에 영향력이 큰 상위 5개를 선정하여 목표 GO/MG를 도출했는가?
3. **EA 정합성 검증**: 현행(AS-IS) 및 목표(TO-BE) 아키텍처 간 **Gap Analysis**를 수행하고, **Application Rationalization**(Tolerate/Invest/Migrate/Eliminate 4-Quadrant)을 통해 레거시 30~50%를 정리했는가? **ArchiMate**로 Business-Application-Technology 3계층 동기(Motivation) 요소를 포함하여 표현했는
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 779 / 800

<- **이전**: [778. IT 경영 관리 핵심 토픽 778번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/778_it_management_core_topic_778_exam_summary/)
**다음**: [780. IT 경영 관리 핵심 토픽 780번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/780_it_management_core_topic_780_exam_summary/) ->

---
