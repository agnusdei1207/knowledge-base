---
title: "IT Management Core Topic 571 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Information Technology Governance)는 COBIT 2019, ITIL 4, ISO/IEC 38500, PMBOK 7th, TOGAF 10 등 글로벌 표준 프레임워크를 기반으로, IT 전략(Strategy) ↔ 아키텍처(Architecture) ↔ 운영(Operations) ↔ 거버넌스(Governance) 4대 축을 통합하여 기업 가치를 극대화하는 체계이다.
> 2. **가치**: McKinsey 연구에 따르면 디지털 전환 성공 기업은 매출 성장률 2.5배, EBITDA 마진 1.7배, 주주총수익률(TSR) 2.6배 우위를 확보하며, IT 거버넌스 성숙도 1단계 상승 시 운영 비용 평균 12-18% 절감, 프로젝트 실패율 30%v 효과를 기대할 수 있다.
> 3. **판단 포인트**: Build vs Buy vs Cloud, Agile vs Plan-Driven, Centralized vs Federated 거버넌스 모델, CapEx vs OpEx, Zero Trust vs Perimeter Security 등 Trade-off에서 Balanced Scorecard(BSC) + KPI 트리 + Risk-Adjusted ROI로 의사결정해야 한다.

---

## Ⅰ. 개요 및 필요성

정보기술이 단순 지원(Back-office) 기능을 넘어 핵심 사업 경쟁력의 원천이 되면서, IT 투자 대비 비즈니스 가치 측정(Valuation of IT), IT 리스크 통제, 그리고 디지털 전환(DX, Digital Transformation)의 체계적 관리가 필수 역량으로 부상했다. 2020년 코로나19 이후 원격근무, 클라우드, AI/ML 도입이 가속화되면서 CIO의 역할이 "IT 운영 책임자"에서 "Digital Business Strategist"로 전환되었고, 이에 따라 IT 거버넌스 성숙도가 기업의 생존을 좌우하는 핵심 지표가 되었다.

특히 한국 환경에서는 2024년 전자금융감독규정 개정, 개인정보보호법 강화(가명정보 도입), 클라우드컴퓨팅법(클라우드 컴퓨팅 이용자의 권리 및 보호에 관한 법률, 2025년 시행) 등 규제 환경 변화에 따라 IT 컴플라이언스 대응이 경영 리스크의 1순위 과제로 부상했다. 또한 Gartner는 2026년까지 글로벌 기업 75%가 AI 거버넌스 프레임워크를 도입할 것으로 전망하며, 전통적 IT 관리 패러다임의 근본적 전환을 예고하고 있다.

```text
+---------------------------------------------------------------------+
|           IT 경영 관리 4대 축(4 Pillars) 통합 프레임워크             |
+---------------------------------------------------------------------+
|                                                                     |
|   [1] IT 전략 (Strategy)              [2] IT 아키텍처 (EA)          |
|   +---------------------+             +----------------------+      |
|   | • IT Vision/Mission |             | • TOGAF 10 ADM Cycle  |      |
|   | • 디지털 전환 로드맵 |             | • Zachman Framework  |      |
|   | • BSC(균형성과표)    |◄-----------►| • 업무/데이터/응용    |      |
|   | • IT 투자 우선순위   |   연계      |   /기술 4+1 아키텍처 |      |
|   +---------+-----------+             +----------+-----------+      |
|             |                                    |                  |
|             |   [3] IT 운영 (Operations)          |                  |
|             |   +---------------------+          |                  |
|             |   | • ITIL 4 Service    |          |                  |
|             +----|   Value System(SVS) |----------+                  |
|                 | • 34 Practices       |                             |
|                 | • SLA/OLA/UC         |                             |
|                 | • FinOps, AIOps      |                             |
|                 +---------+-----------+                             |
|                           |                                         |
|                  [4] IT 거버넌스 (Governance)                       |
|                  +-------------------------+                        |
|                  | • COBIT 2019 (40 Obj)   |                        |
|                  | • ISO/IEC 38500 원칙    |                        |
|                  | • 3단계 의사결정 모델    |                        |
|                  | • Risk Mgmt(ISO 31000)  |                        |
|                  +-------------------------+                        |
+---------------------------------------------------------------------+
```

과거(1990~2000년대)에는 IT가 "비용 센터(Cost Center)"로 인식되어 CAPEX 기반의 무계획적 투자, 부서별 독립 정보시스템(Silo System), 사후 통제(Post-audit) 방식이 지배적이었다. 그러나 현재는 IT를 "전략적 자산(Strategic Asset)"이자 "Value Driver"로 인식하며, **Plan -> Build -> Run -> Govern**의闭环(Closed-loop) 관리 체계를 구축해야 한다. 이는 Cobit의 EDM( Evaluate, Direct, Monitor) 사이클과 ISO 38500의 **3 principles (책임Responsibility, 전략Strategy, 획득Acquisition, 성능Performance, 적합성Conformance, 인적행위Human Behavior)** 와 직접 매핑된다.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **대형 의료원의 운영 시스템**과 같다. 진찰(요구사항 분석), 진단(현황 분석), 처방(아키텍처 설계), 수술(구축), 재활(운영), 건강검진(모니터링), 그리고 병원 운영 위원회(거버넌스)까지 모두 유기적으로 돌아가야 환자가 건강해진다. 어느 한环节이 끊기면 시스템 전체가 위험해진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 메커니즘은 **전략-전환-운영-평가** 4단계 가치 사슬(Value Chain)을 통해 비즈니스 요구사항을 IT 서비스로 변환하고, 이를 다시 비즈니스 KPI와 연결하는 것이다. 이를 구현하는 가장 대표적인 방법론이 **COBIT 2019**의 거버넌스 시스템으로, 40개의 관리 목표(Management Objective)를 5개 도메인(EDM, APO, BAI, DSS, MEA)으로 분류한다.

```text
+----------------------------------------------------------------------+
|        COBIT 2019 Governance System & Component Mapping              |
+----------------------------------------------------------------------+
|                                                                      |
|  +--------------------------------------------------------------+    |
|  |  EDM (Evaluate, Direct, Monitor) - 5 Objectives               |    |
|  |  +- EDM01: 거버넌스 프레임워크 설정/유지                        |    |
|  |  +- EDM02: 이익 실현(Benefits Realization)                    |    |
|  |  +- EDM03: 리스크 최적화                                      |    |
|  |  +- EDM04: 자원 최적화                                        |    |
|  |  +- EDM05: 이해관계자 투명성 보장                              |    |
|  +----------------+---------------------------------------------+    |
|                   |                                                  |
|  +----------------v---------------------------------------------+    |
|  |  APO (Align, Plan, Organize) - 14 Objectives                  |    |
|  |  +- APO01: IT 관리 프레임워크                                 |    |
|  |  +- APO04: 혁신 관리 (Innovation)                              |    |
|  |  +- APO05: 포트폴리오 관리 (Portfolio)                          |    |
|  |  +- APO12: 리스크 관리                                        |    |
|  |  +- APO13: 정보보안 관리                                      |    |
|  +----------------+---------------------------------------------+    |
|                   |                                                  |
|  +----------------v---------------------------------------------+    |
|  |  BAI (Build, Acquire, Implement) - 11 Objectives              |    |
|  |  +- BAI01: 프로그램/프로젝트 관리                              |    |
|  |  +- BAI02: 요구사항 정의 및 관리                                |    |
|  |  +- BAI03: 솔루션 식별 및 구축                                 |    |
|  |  +- BAI11: 변경 관리 (Change Mgmt)                              |    |
|  +----------------+---------------------------------------------+    |
|                   |                                                  |
|  +----------------v---------------------------------------------+    |
|  |  DSS (Deliver, Service, Support) - 6 Objectives                |    |
|  |  +- DSS01: 운영 관리                                          |    |
|  |  +- DSS02: 서비스 요청 및 사고 관리                            |    |
|  |  +- DSS04: 연속성 관리 (BCM)                                   |    |
|  |  +- DSS05: 보안 서비스 관리                                   |    |
|  +----------------+---------------------------------------------+    |
|                   |                                                  |
|  +----------------v---------------------------------------------+    |
|  |  MEA (Monitor, Evaluate, Assess) - 4 Objectives                |    |
|  |  +- MEA01: 성과 및 적합성 모니터링                              |    |
|  |  +- MEA02: 내부 통제 시스템                                    |    |
|  |  +- MEA03: 외부 요구사항 준수                                  |    |
|  |  +- MEA04: 감사                                                |    |
|  +--------------------------------------------------------------+    |
|                                                                      |
|  [7 Components] Process / Structure / Information / People /       |
|                  Skills / Culture / Services                         |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 전략 (Strategy)** | IT가 비즈니스 목표에 기여하는 방향 정의 | ISO/IEC 38500 6대 원칙 적용, Ward & Peppard IS/IT 전략 방법론(전제조건 분석 -> SWOT -> CSF -> 전략 옵션), BSC 4관점(재무/고객/내부/학습) KPI 매핑 |
| **EA (Enterprise Architecture)** | 비즈니스-IT 간 구조적 정렬 | TOGAF 10 ADM 8단계(Phase A~H) + Requirements Mgmt, Zachman 6x6 매트릭스, FEAF (Federal EA Framework), 4+1 뷰(논리/개발/배치/처리 + 시나리오) |
| **ITSM (IT Service Management)** | IT 서비스의 설계-전환-운영-개선 | ITIL 4 Service Value System(SVS): Opportunity/Demand -> Value -> Guiding Principles(7원칙) -> Governance -> Practices(34) -> Continual Improvement |
| **프로젝트 관리 (PMO)** | IT 투자 프로젝트의 성공적 수행 | PMBOK 7th 12원칙 + 8성능도메인, PRINCE2 7원칙(7 Themes), 애자일 스케일(SAFe/LeSS/Scrum@Scale), Earned Value(EV/AC/PV/CPI/SPI) |
| **거버넌스 & 컴플라이언스** | 의사결정, 책임, 리스크, 감사 체계 | COBIT 2019 40 Objectives, ISO 31000 Risk Mgmt, ISO 27001 ISMS, ISAE 3402(SOC 1/2/3) |
| **정보보안 거버넌스** | 사이버 리스크 통제 및 제로트러스트 | NIST CSF 2.0(Govern 추가), Zero Trust Architecture(NIST SP 800-207), ISO 27001:2022 Annex A 93 통제 항목, K-ISMS-P(2024~) |
| **데이터 거버넌스** | 데이터 자산의 품질, 권한, 수명주기 관리 | DAMA-DMBOK 2(11 지식영역), DGI Data Governance Maturity Model 5단계, 마스터/메타/레퍼런스 데이터 관리, 개인정보 영향평가(PIA) |
| **FinOps & AI 거버넌스** | 클라우드 비용 최적화 및 AI 윤리 | FinOps Foundation Framework(Inform/Optimize/Operate), AI Act(EU), NIST AI RMF 1.0(Govern/Map/Measure/Manage), MLOps/LLMOps |

**핵심 알고리즘/측정 모델 상세:**

- **Balanced Scorecard (BSC) KPI Cascade**: 목표(Objectives) -> 측정지표(Metrics) -> 목표치(Target) -> 실행과제(Action) 4단계. 예: "고객만족 향상" -> NPS ≥ 70 -> 서비스 요청 해결시간 ≤ 4시간.
- **COBIT 2019 Maturity/Capability**: Process Maturity Model(0-Incomplete ~ 5-Optimizing), ISO 33000 PAM 기반.
- **EV( Earned Value) 분석**: `CPI = EV / AC` (Cost Performance Index), `SPI = EV / PV` (Schedule Performance Index), `EAC = BAC / CPI` (Estimate At Completion).
- **Total Economic Impact (TEI)**: Gartner/Forrester 방식. `Benefit - Cost + Flexibility + Risk Reduction`을 NPV로 환산.
- **Risk = Threat × Vulnerability × Impact / Control** (ISO 31000 정성평가), 또는 **ALE = ARO × SLE** (Annual Loss Expectancy).
- **Ward & Peppard IT 포트폴리오 매트릭스**: Impact(Strategic/Operational/Support) × 공급(Strategic/Critical/Commodity)으로 9개 사분면 분류.

- **📢 섹션 요약 비유**: IT 경영 관리는 **도시의 도시계획**과 같다. 상위계획(전략) -> 토지이용(EA) -> 인프라 건설(프로젝트) -> 도로·상하수도 운영(서비스) -> 도시 안전·환경(거버넌스)가 모두 20년 단위 마스터플랜 아래 통합되어야 시민(사용자)이 안전하고 편리한 삶을 영위할 수 있다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리의 글로벌 표준 프레임워크들은 상호 보완적이지만, **초점(Focus), 적용 범위(Scope), 통제 깊이(Control Depth)** 에서 명확한 차이를 보인다. 기술사 시험에서는 각 프레임워크의 **Trade-off**를 정확히 이해하고, 조직 상황에 맞는 **Hybrid 적용**을 판단할 수 있어야 한다.

| 구분 | COBIT 2019 | ITIL 4 | ISO 38500 | PMBOK 7th | TOGAF 10 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주요 초점** | IT 거버넌스/관리 | IT 서비스 운영 | 이사진/거버넌스 원칙 | 프로젝트 관리 표준 | EA 개발방법론 |
| **대상 사용자** | CIO, CISO, C-Level | IT 운영 실무자 | 이사진(Board), CEO | 프로젝트 매니저 | EA 아키텍트 |
| **도메인/구조** | 5도메인/40목표/7컴포넌트 | SVS/34 Practices/7원칙 | 6원칙/3모델(책임-전략-수행) | 12원칙/8성능도메인/5과정그룹 | ADM 8단계 + Repository |
| **컴플라이언스 적합도** | ★★★★★ | ★★★☆☆ | ★★★★★ (법적 책임) | ★★☆☆☆ | ★★☆☆☆ |
| **운영 실무 적합도** | ★★☆☆☆ | ★★★★★ | ★☆☆☆☆ | ★★★★☆ | ★★★☆☆ |
| **생성 주체** | ISACA | AXELOS (PeopleCert) | ISO/IEC | PMI | The Open Group |
| **인증 체계** | COBIT 2019 Foundation/Design/Implement | ITIL 4 Foundation/MP/SL | 비공식 인증 | PMP/CAPM/PfMP | TOGAF Certified |
| **주요 산출물** | Goals Cascade, RACI Matrix | Service Catalog, SLA, CSI Register | Charter, Policy | Project Charter, WBS, Risk Register | Architecture Document, Roadmap |
| **상호보완 관계** | 거버넌스 프레임워크 제공 | 운영 관행 제공 | 거버넌스 원칙 제공 | 프로젝트 성공 보장 | 아키텍처 구조 제공 |

**핵심 연계 및 통합 패턴:**

1. **COBIT ↔ ITIL 통합**: COBIT의 EDM(평가/지시/감독)으로 IT 서비스 거버넌스를 설정하고, ITIL 4의 SVS(Value Chain)로 서비스 운영을 구체화. CMMI(Capability Maturity Model Integration)가 두 프레임워크의 성숙도 측정을 통합.
2. **PMBOK ↔ PRINCE2 ↔ Agile**: PMBOK 7th는 12 Principles 기반으로 Predictive/Agile/Hybrid 모두 수용, PRINCE2는 7 Themes/7 Processes로 Project Mgmt 통제 강조, SAFe/LeSS/Scrum
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 571 / 800

<- **이전**: [570. IT 경영 관리 핵심 토픽 570번 시험 요약](/studynote/12_it_management/05_security_compliance/570_it_management_core_topic_570_exam_summary/)
**다음**: [572. IT 경영 관리 핵심 토픽 572번 시험 요약](/studynote/12_it_management/05_security_compliance/572_it_management_core_topic_572_exam_summary/) ->

---
