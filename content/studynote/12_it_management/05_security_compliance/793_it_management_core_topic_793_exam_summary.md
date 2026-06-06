---
title: "IT Management Core Topic 793 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스·EA(Enterprise Architecture)·IT 투자관리·ITIL 4/COBIT 2019 기반 운영·디지털 전환(DX)·정보보안 거버넌스를 하나의 통합 프레임워크로 연결해, 기업의 전략-전술-운영 3계층 정렬(Strategic Alignment)을 실현하는 것이 정보관리기술사 793번 영역의 본질이다.
> 2. **가치**: COBIT 2019의 40개 거버넌스/관리 목적(Governance & Management Objectives) 기반 KPI를 적용 시, IT 투자 대비 ROI 평균 25~40% 개선, 프로젝트 실패율 35%->15% 이하로 감소, ISO 38500 6원칙 적용 시 이사회-경영진-현업의 의사결정 지연 60% 단축 효과가 보고된다(예: ISO/IEC 38500:2015, ISACA 2023 State of IT Governance 보고).
> 3. **판단 포인트**: 중앙집중형(CoE) vs 분산형(Federated) 거버넌스 모델 선택, BSC(균형성과표) 4관점(재무/고객/내부/학습성장) vs ESG 3축(환경/사회/지배구조) 가중치, COBIT 2019 설계요인(Design Factors) 11개에 따른 거버넌스 시스템 커스터마이징, 그리고 EA 참조모델(TOGAF ADM vs Zachman) 채택 여부가 기술사 시험에서 핵심 트레이드오프 포인트이다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 793번 토픽은 **"IT 경영 관리의 통합적 이해"**를 다룬다. 단순히 IT 부서의 운영 관리를 넘어, 기업의 **전략적 IT 활용과 가치 실현**을 위한 거버넌스 체계, 아키텍처, 투자, 운영, 보안, 변화관리의 총합이다. 한국정보화진흥원(KIAT)의 「2024 정보화 통계」에 따르면, 국내 500대 기업의 IT 예산 평균은 매출액의 **2.1~3.8%**이며, 이 중 **28~35%가 사일로(Silo) 시스템 유지보수**에 흡수되어 디지털 전환에 제대로 투입되지 못하는 구조적 문제가 있다. 또한 ISACA의 2023 보고에 따르면, 전 세계 CIO의 **67%가 IT-비즈니스 정렬 부재**를 1순위 리스크로 꼽았다.

이러한背景下 793번 토픽은 **ISO/IEC 38500(기업 IT 거버넌스 국제표준)**, **COBIT 2019(ISACA 거버넌스 프레임워크)**, **ITIL 4(서비스 관리 프레임워크)**, **TOGAF 10(EA 방법론)**, **CMMI(능력성숙도모델)**, **ISO 27001/27701(보안/개인정보)**, **PMP/PMBOK 7th(프로젝트 관리)** 등 7대 표준/프레임워크를 통합적으로 이해하고, 한국 기업의 현실(공공부문 EA 4+1 뷰, 한국형 e-정부 프레임워크, DSMM 데이터 성숙도, ISMS-P 인증)에 맞게 응용할 수 있는 역량을 평가한다.

```text
+-------------------------------------------------------------------------+
|         IT 경영 관리 통합 프레임워크 (793번 토픽 스코프)                |
+-------------------------------------------------------------------------+
|                                                                         |
|   [전략 계층]              [전술 계층]              [운영 계층]         |
|   +----------+            +----------+            +----------+          |
|   | ISO 38500|            | COBIT    |            | ITIL 4   |          |
|   | IT 전략  | --------► | 2019     | --------► | Service  |          |
|   | 6원칙    |            | 40 G&M   |            | Value    |          |
|   |          |            | Objectives|           | System   |          |
|   +----+-----+            +----+-----+            +----+-----+          |
|        |                       |                       |                 |
|        v                       v                       v                 |
|   +----------+            +----------+            +----------+          |
|   | BSC/OKR  |            | TOGAF ADM|            | DevOps   |          |
|   | KPI      | --------► | 8 Phase  | --------► | SRE/AIOps|          |
|   | ESG      |            | Zachman  |            | SLA/SLO  |          |
|   +----------+            +----------+            +----------+          |
|        |                       |                       |                 |
|        +-----------------------+-----------------------+                 |
|                                |                                         |
|                                v                                         |
|                +-------------------------------+                         |
|                |  Value Realization (가치실현) |                         |
|                |  - ROI, NPV, EVA, BTO/CTO     |                         |
|                |  - Customer Experience Index  |                         |
|                +-------------------------------+                         |
|                                                                         |
+-------------------------------------------------------------------------+
```

**기존 패러다임 vs 신규 패러다임**:
- *AS-IS (2000~2015)*: 부서별 ERP/CRM 독립 구축, ITSM은 ITIL v3, 거버넌스는 형식적 IT감사 위주, EA는 문서화 산출물 중심, 보안은 방화벽/IDS 장비 도입 위주 -> 프로젝트 평균 성공률 29% (CHAOS Report 2015).
- *TO-BE (2016~2025)*: 클라우드 네이티브(MSA, Kubernetes), 거버넌스는 COBIT 2019 40목표+11설계요인 기반, EA는 TOGAF ADM 반복+연속(Iteration), 보안을 Zero Trust·SASE로 전환, 데이터 거버넌스(DAMA-DMBOK 2.0) 통합 -> DevOps 도입 조직은 배포 빈도 208배, 변경 실패율 7배 감소(DORA 2023).

- **📢 섹션 요약 비유**: IT 경영 관리는 **도시의 도시계획(Urban Planning)**과 같다. 도로(네트워크), 건물(애플리케이션), 상하수도(데이터 파이프라인), 교통규칙(거버넌스/정책), 소방(보안)가 따로 노는 것이 아니라, **도시기본계획(EA)**에 따라 **토지이용규제(거버넌스)**로 묶이고, **일일 교통관제(ITIL)**가 돌아가야 시민(사용자)에게 가치를 준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) COBIT 2019 거버넌스 시스템의 5개 도메인 및 40개 목적

COBIT 2019는 **거버넌스 5개 목적(EDM: Evaluate, Direct, Monitor) + 관리 35개 목적(APO, BAI, DSS, MEA)**의 계층 구조로 구성된다. 핵심은 **11개 설계요인(Design Factors)**을 통해 조직 상황에 최적화된 거버넌스 시스템(Governance System)을 커스터마이징한다는 점이다.

```text
+-----------------------------------------------------------------+
|              COBIT 2019 Core Model (40 Objectives)              |
+-----------------------------------------------------------------+
| EDM Domain (거버넌스 - 5개)                                     |
|  +- EDM01 거버넌스 체계 설정 (Ensuring Governance Framework)    |
|  +- EDM02 이익 실현 (Benefits Realization)                     |
|  +- EDM03 위험 최적화 (Risk Optimization)                       |
|  +- EDM04 자원 최적화 (Resource Optimization)                   |
|  +- EDM05 이해관계자 투명성 (Stakeholder Transparency)          |
|                                                                 |
| Management Domain (관리 - 35개)                                 |
|  +- APO (Align, Plan, Organize) 14개                           |
|  |   +- APO01~14: 전략, 포트폴리오, 예산, 조직, 인적자원 등     |
|  +- BAI (Build, Acquire, Implement) 11개                        |
|  |   +- BAI01~11: 프로젝트, 솔루션, 변경, 배포, 전이 등        |
|  +- DSS (Deliver, Service, Support) 6개                         |
|  |   +- DSS01~06: 운영, 서비스요청, 인시던트, 보안, 데이터 등   |
|  +- MEA (Monitor, Evaluate, Assess) 4개                        |
|      +- MEA01~04: 성과모니터링, 내부통제, 외부감사, 컴플라이언스|
|                                                                 |
|  ★ Focus Area: 사이버보안(CSF NIST 매핑), DevOps, 위험,         |
|                개인정보(GDPR/PIPA), 클라우드, 데이터거버넌스 등  |
+-----------------------------------------------------------------+
```

### 2) 11개 설계요인(Design Factors) 의사결정 트리

설계요인 중 가장 시험에 자주 출제되는 5개는: **DF1(Enterprise Strategy), DF2(Enterprise Goals), DF3(Risk Profile), DF4(Compliance), DF5(Threat Landscape)**이다.

### 3) ITIL 4 Service Value System (SVS)

ITIL 4는 **Opportunity/Demand -> Value -> Value** 흐름을 중심으로, 7가지 guiding principle(Focus on value, Start where you are, Progress iteratively, Collaborate, Think holistically, Keep it simple, Optimize) 및 **34개 Practice**(구 26 Process + 3 추가 영역)를 운영한다.

```text
                    +---------------------+
                    |  Opportunity/Demand |
                    +----------+----------+
                               |
                               v
   +--------------------------------------------------------------+
   |           Service Value System (SVS) - ITIL 4                 |
   |                                                              |
   |  +-------------------------------------------------------+  |
   |  |  Guiding Principles (7) + Governance (3) + Practice(34)|  |
   |  +-------------------------------------------------------+  |
   |                              |                               |
   |                              v                               |
   |  +-------------+  +-------------+  +-------------+          |
   |  | Plan &      |  | Design &    |  | Transition  |          |
   |  | Improve     |-►| Transition  |-►| & Support   |          |
   |  | (P&I)       |  | (D&T)       |  | (T&S)       |          |
   |  +-------------+  +-------------+  +-------------+          |
   |              |              |              |                  |
   |              +--------------+--------------+                  |
   |                              |                               |
   |                              v                               |
   |                +----------------------------+                 |
   |                |  Service Value Chain (6단계)|                 |
   |                |  Engage->Design->Obtain->     |                 |
   |                |  Deliver->Support->Improve    |                 |
   |                +----------------------------+                 |
   +--------------------------------------------------------------+
                               |
                               v
                    +---------------------+
                    |      Value          |  <- Co-creation with
                    |   (Utility+Warranty)|     all stakeholders
                    +---------------------+
```

### 4) 핵심 구성요소 표

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **ISO/IEC 38500** | 이사회-경영진 IT 거버넌스 국제표준 | 6원칙(책임, 전략, 획득, 성과, 준수, 인간행동) + 모델(Plan-Do-Check-Act 기반 정책 수립·이행·모니터링). 영국의 표준 BS 7799 -> ISO 27001 진화의 거버넌스 상위 표준. |
| **COBIT 2019** | IT 거버넌스/관리 목표 체계 | 40개 EDM/APO/BAI/DSS/MEA 목적, 11개 설계요인(DF1~11), 7개 컴포넌트(Process/Organizational Structures/Information/Flows/People/Skills/Culture). Power/Interest Grid로 이해관계자 분석. |
| **ITIL 4** | IT 서비스 관리 운영 프레임워크 | SVS(Service Value System), 34개 Practice(예: Incident, Change Enablement, Service Desk, Service Request, Problem, Continual Improvement), 4P(Product/Partner/People/Process), Service Value Chain 6단계. |
| **TOGAF 10 (ADM)** | EA 구축 방법론 | 8단계 ADM Cycle(Phase A: Vision -> B: Business -> C: Information Systems -> D: Technology -> E: Opportunities&Solutions -> F: Migration Planning -> G: Implementation Governance -> H: Architecture Change Management) + Preliminary + Requirements Management. ADM Iteration, Content Metamodel(39개 산출물), Architecture Repository. |
| **Zachman Framework** | EA 분류 체계 | 5W1H × 5관점(Planner/Owner/Designer/Builder/Subcontractor/Enterprise) = 36셀 매트릭스. 6개 추상화 질문(What, How, Where, Who, When, Why)과 5개 Audience-관점. |
| **BSC(균형성과표)** | 전략 실행 KPI 도구 | Kaplan & Norton 4관점(재무/고객/내부프로세스/학습성장), 4단계(Strategic Map -> BSC -> Target Setting -> Initiative Portfolio), Strategy Map 인과관계 맵. |
| **PPM(Project Portfolio Mgmt)** | IT 투자 포트폴리오 관리 | APO05(COBIT) + MoP(Management of Portfolio) + PMBOK Portfolio Mgmt, 3단계(Pre-project: Strategy -> In-flight: Performance -> Post-project: Benefit), Value Office(PMO->VfMO 진화). |

### 5) 핵심 알고리즘/수식

**IT 투자 우선순위 의사결정 시 사용되는 정량 모델**:
- **NPV(순현재가치)**: $NPV = \sum_{t=0}^{n} \frac{CF_t}{(1+r)^t} - I_0$, 여기서 $r$은 WACC(가중평균자본비용, IT 프로젝트는 통상 8~12%), $CF_t$는 t기 현금흐름.
- **Total Economic Impact(TEI, Forrester 모델)**: $TEI = Benefits_{NPV} - Costs_{NPV} + RiskCosts_{NPV}$
- **TCO(총소유비용)**: $TCO = Acquisition + Implementation + Operations + Maintenance + Decommission$ (Gartner 5단계 모델
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 793 / 800

<- **이전**: [792. IT 경영 관리 핵심 토픽 792번 시험 요약](/studynote/12_it_management/05_security_compliance/792_it_management_core_topic_792_exam_summary/)
**다음**: [794. IT 경영 관리 핵심 토픽 794번 시험 요약](/studynote/12_it_management/05_security_compliance/794_it_management_core_topic_794_exam_summary/) ->

---
