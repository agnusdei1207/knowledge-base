---
title: "IT Management Core Topic 562 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 정보관리기술사 562번 시험은 IT 거버넌스(COBIT 2019), IT 서비스 관리(ITIL 4), 프로젝트 관리(PMBOK 7/EVM), 정보보안관리(ISMS-P), 디지털 전환 전략을 통합한 종합적 IT 경영관리 역량을 평가하는 것으로, 각 프레임워크의 구조·프로세스·성과지표를 정확히 연결하는 능력이 핵심이다.
> 2. **가치**: COBIT 2019의 40개 관리목표와 ITIL 4의 34개 서비스 관행, ISO 27001:2022의 93개 통제항목, PMBOK 7의 8개绩效영역을 상호 매핑하여 IT 투자 대비 ROI 25~40% 향상, 인시던트 MTTR 60% 단축, 보안사고 발생률 70% 감소 등 정량적 가치를 창출한다.
> 3. **판단 포인트**: 거버넌스-관리-운영 계층에서 의사결정 권한 배분(RACI), Balanced Scorecard의 4관점(재무/고객/내부/학습성장) 지표 설계, PMBOK 7의 Tailoring 전략, 그리고 클라우드/AI 시대의 Shadow IT 및 데이터 주권 리스크 통제 여부가 합격/불합격을 가르는 결정적 판단 포인트이다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 562번 시험은 1989년 제정 이래 약 35년간 한국 IT 산업의 성숙단계를 반영하며 진화해 온 국가공인 최고급 IT 전문자격 시험이다. 한국정보통신기술사협회(KAITS) 자료에 따르면 2023년 기준 누적 응시자 약 12만 명 중 합격률은 **2.1~3.4%**(연도별 편차 있음)에 불과하며, 필기 4교시(정보시스템 기반기술, 정보시스템 개발/운영/관리, 신기술 동향 및 활용, 정보시스템 경영관리)와 구술 1교시, 논문작성을 거쳐야 한다. 그중 562번 영역은 **"정보시스템 경영·관리"** 트랙으로, CFO/CEO 레벨의 의사결정자 관점에서 IT를 경영 자산으로 다루는 능력을 검증한다.

```text
+---------------------------------------------------------------------+
|         562번 시험의 4대 핵심 축 (4 Knowledge Pillars)                |
+---------------------------------------------------------------------+
|                                                                     |
|   [1] IT 거버넌스      [2] IT 서비스 운영     [3] 프로젝트 관리    |
|   +----------+         +----------+          +----------+         |
|   | COBIT    |         | ITIL 4   |          | PMBOK 7  |         |
|   | 2019     |◄-------►| SVS/34   |◄--------►| Tailoring|         |
|   | 40 Gov.  |         | Practices|          | 8 Perf.  |         |
|   | Objectives|        |          |          | Domains  |         |
|   +----+-----+         +----+-----+          +----+-----+         |
|        |                    |                     |                |
|        +----------+---------+---------------------+                |
|                   v                                                |
|         [4] 정보보안·컴플라이언스·디지털 전환 통합                      |
|         +-----------------------------------------+                |
|         | ISMS-P(2022) | PIMS | ISO 27001:2022 | DX 전략 |         |
|         +-----------------------------------------+                |
+---------------------------------------------------------------------+
```

기존 1990년대~2000년대 IT 경영은 **"비용 중심(Cost Center)"** 관점으로, IT 부서는 단순히 인프라를 운영·유지하는 후방업무(Function)로 인식되었다. 그러나 2010년대 클라우드·모바일, 2020년대 AI·데이터 경제로 전환되며 Gartner(2023)가 강조한 **"Every Company is a Technology Company"** 패러다임이 정착되었고, 2024년 한국정보화진흥원의 조사에 따르면 국내 100대 기업의 **78%가 CIO/CDO 직위를 이사회급으로 격상**시켰다. 따라서 562번 시험은 단순 암기가 아닌 **"IT 투자 의사결정의 정당화(Business Case)", "위험-가치-자원의 균형(Risk-Value-Resource Triangle)", "규제 준수(Compliance) 체계 설계"** 능력을 요구하게 되었다.

- **📢 섹션 요약 비유**: 562번 시험은 자동차로 치면 "F1 레이서의 종합 코디네이터" 시험과 같습니다. 엔진(기술), 핸들(거버넌스), 브레이크(보안), 연료(예산), 코너링(변화관리)을 모두 통합적으로 다루는 능력이 필요한 것입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) COBIT 2019 — IT 거버넌스의 6계층 구조

```text
+---------------------------------------------------------------+
|                  COBIT 2019 Conceptual Framework              |
+---------------------------------------------------------------+
|  계층1: Stakeholders (이해관계자 요구)                          |
|          |  - Shareholders, Regulators, Customers, Employees |
|  계층2: Enterprise Goals (13개 기업목표)                       |
|          |  - EG01: 포트폴리오 경쟁제품/서비스                  |
|          |  - EG05: 고객 중심 서비스 제공                       |
|          |  - EG13: 정보 기반 의사결정                          |
|  계층3: Alignment Goals ↔ Cascade (13개 정렬목표)              |
|          |  - AG01: IT 준법/지원, AG04: 정보/기술 자원 관리     |
|  계층4: Management Objectives (40개 관리목표)                   |
|          |  - EDM(05): 거버넌스 체계 수립/유지                   |
|          |  - DSS(06): 비즈니스 서비스 보안 관리                |
|  계층5: Components (7개 컴포넌트, 40개 상세)                    |
|          |  - Process, Organizational Structures, Information  |
|          |  - People/Skills, Services/Infrastructure/Apps     |
|  계층6: Focus Areas (Focus Area Guide)                        |
|          |  - DevOps, RPA, Cybersecurity, Digital Ethics      |
+---------------------------------------------------------------+
```

**핵심 메커니즘 — Cascade(폭포) 원칙**:
기업목표(EG) 1개당 평균 2.3개의 정렬목표(AG)가 매핑되며, 각 정렬목표는 다시 1~6개의 관리목표(MO)로 분해된다. 기술사 답안에서는 이 **"EG -> AG -> MO -> Process"** 의 4단계 연결 체계를 명확히 보여줘야 한다. 예컨대 "고객 만족도 향상(EG05) -> AG01 IT 준법성 강화 -> DSS02 서비스 요청/사고 관리 -> 8단계 V-model 프로세스"로 연결하는 식이다.

### 2) ITIL 4 — 서비스 가치 시스템(SVS)

```text
+----------------------------------------------------------------------+
|                    ITIL 4 Service Value System (SVS)                  |
+----------------------------------------------------------------------+
|                                                                      |
|   +-------------------------------------------------------------+   |
|   |  Opportunity/Demand ◄--► Value (Co-Creation)                |   |
|   +-------------------------+-----------------------------------+   |
|                              v                                       |
|   +--------------+  +--------------+  +--------------------+        |
|   | Guiding      |  | Governance   |  | Practices (34)     |        |
|   | Principles(7)|-►| (5단계 의사  |-►| • 14 General       |        |
|   | • Focus value|  |  결정 체계)  |  | • 17 Service       |        |
|   | • Start where|  | Evaluate-►   |  | • 3 Technical      |        |
|   |   you are    |  | Direct-►     |  |                    |        |
|   | • Progress   |  | Monitor-►    |  | Service Value Chain |        |
|   |   iteratively|  |              |  | (6 Activity)        |        |
|   | • Collaborate|  +--------------+  | Plan-Improve/Engage|        |
|   | • Think holi.|                   | Design/Obtain/Build |        |
|   | • Keep it    |                   | Deliver/Support     |        |
|   |   simple     |                   +--------------------+        |
|   +--------------+                                                   |
+----------------------------------------------------------------------+
```

### 3) PMBOK 7 — 프로젝트 관리의 8대 성과영역(Performance Domains)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **EDM(거버넌스 5단계)** | Evaluate·Direct·Monitor | 이사회/경영진의 IT 투자 감독, COBIT 2019 EDM01~05와 직접 매핑 |
| **AGL(정렬목표 13개)** | 기업-IT 정렬 | BSC 4관점(재무/고객/내부/학습)과 연계하여 KPI 25~40개 도출 |
| **MO(관리목표 40개)** | 프로세스 실행 | EDM·APO·BAI·DSS·MEA 5도메인, 40개 목표 × 평균 5개 프로세스 = 200+ 활동 |
| **Component(7종)** | 자원·문화 구현 | Process·Structure·Info·People·Skill·Service·Infrastructure |
| **SVC(서비스 가치사슬)** | 가치 창출 흐름 | Plan->Engage->Design->Obtain->Build->Deliver->Support 6개 활동 |
| **34 Practices** | 실무 실행 단위 | 사고관리(8단계), 변경관리(CAB/ECAB), SLA/SLM, CSI 등록 |
| **8 Performance Domains** | 프로젝트 성과 | Stakeholder, Team, Development Approach, Planning, Work, Delivery, Measurement, Uncertainty |
| **Guiding Principles(7)** | 의사결정 원칙 | Value·Context·Engage·Lead·Plan·Quality·Complexity |

**핵심 공식 — COBIT 2019의 Maturity Level**:
- **Level 0 (Incomplete)**: 프로세스 미수행
- **Level 1 (Initial)**: 1~2년차, 성공 의존
- **Level 2 (Managed)**: 기본 관리 체계 구축
- **Level 3 (Defined)**: 표준 프로세스화, KPI 80% 달성
- **Level 4 (Quantitative)**: 통계적 기법(SPC, 6σ) 활용, Cp/Cpk ≥ 1.33
- **Level 5 (Optimizing)**: 지속적 개선, ROI 30% 이상 향상

기술사 답안 작성 시 이 6단계를 "현재 위치 -> 목표 위치 -> Gap Analysis" 형태로 수치화하여 제시하는 것이 고득점 전략이다.

- **📢 섹션 요약 비유**: COBIT 2019는 회사의 "내비게이션 시스템(어디로 가는지)", ITIL 4는 "엔진룸(어떻게 굴러가는지)", PMBOK은 "운전 매뉴얼(프로젝트별로 어떻게 운전하는지)"이며, ISMS-P는 "보안벨트와 airbags"입니다.

---

## Ⅲ. 비교 및 연결

### 1) 5대 프레임워크 비교 매트릭스

| 구분 | **COBIT 2019** | **ITIL 4** | **PMBOK 7** | **ISMS-P(2022)** | **ISO 27001:2022** |
|:---|:---|:---|:---|:---|:---|
| **주 목적** | IT 거버넌스 & 목표 달성 | IT 서비스 운영 효율화 | 프로젝트 성공률 제고 | 정보보호 관리체계 | 국제 정보보호 표준 |
| **핵심 단위** | 관리목표 40개 | 관행(Practice) 34개 | 성과영역 8개 | 통제항목 80개 | 통제항목 93개(Annex A) |
| **계층 수** | 6계층 | SVS 5요소 | 원칙+영역+모델 | 관리체계 4단계 | PDCA 4단계 |
| **측정 방식** | Maturity 0~5 | KPI/SLA/SLM | Earned Value(EVM) | 위험도 R = L × I | KPI/KRI |
| **적용 대상** | CIO/이사회 | 서비스 운영팀 | PMO/PM | CISO/보안팀 | 전사/감사팀 |
| **갱신 주기** | 2019(2018->2019) | 2019(4.0, 2020 갱신) | 2021(6th->7th) | 2022(KISA) | 2022(2013->2022) |
| **상호연동** | EDM↔Governance | SVC↔Service Ops | Stakeholder↔Engage | A.5~A.8 통제 | 93 통제 |
| **산출물** | RACI Matrix | Service Catalog | Charter, Risk Register | 보호대책 선정서 | SoA(Statement of Applicability) |
| **성공 지표** | Cascade 완성도 | CSAT ≥ 4.5/5 | SPI ≥ 1.0, CPI ≥ 1.0 | 취약점 0건 유지 | 인증 유지 갱신 |
| **도구 예시** | SAP GRC, Archer | ServiceNow, BMC Remedy | MS Project, Jira | AhnLab, Penta Security | ISMS-P 인증원 |

### 2) 프레임워크 간 통합 적용 사례

```text
[기업 전략] --► COBIT EG/AG (13개 목표)
                |
                v
[IT 전략] --► COBIT APO(Align, Plan, Organize) 5개 관리목표
                |
                v
[프로젝트] --► PMBOK 7의 8대 성과영역 (Tailoring)
                |   - Business Case 작성
                |   - Risk Register 10~15개 도출
                v
[서비스 운영] --► ITIL 4 SVC 6개 활동 + 34 관행
                |   - Incident->Problem->Known Error DB
                |   - Change Advisory Board (CAB)
                v
[정보보호] --► ISMS-P 80개 통제 + ISO 27001:2022 93개 통제
                |   - 정보자산 식별(가용성/무결성/기밀성)
                |   - 위험평가 L(likelihood) × I(impact) = 1~5×1~5 = 25 matrix
                v
[측정/개선] --► BSC 4관점 + KPI 25~40개
                |   - 재무관점: ROI, NPV, IRR
                |   - 고객관점: CSAT, NPS
                |   - 내부관점: MTTR ≤ 4hr, 가용성 ≥ 99.9%

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 562 / 800

<- **이전**: [561. IT 경영 관리 핵심 토픽 561번 시험 요약](/studynote/12_it_management/05_security_compliance/561_it_management_core_topic_561_exam_summary/)
**다음**: [563. IT 경영 관리 핵심 토픽 563번 시험 요약](/studynote/12_it_management/05_security_compliance/563_it_management_core_topic_563_exam_summary/) ->

---
