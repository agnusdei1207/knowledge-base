---
title: "545. IT 경영 관리 핵심 토픽 545번 시험 요약 (IT Management Core Topic 545 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 COBIT 2019, ITIL 4, ISO 38500, Val IT 프레임워크를 통해 IT 전략-투자-운영-평가를 통합 관리하는 체계로, 40개 이상의 거버넌 목표(GO)와 230여 개 관리 실무(Process) 간의 Cascade 구조가 핵심 메커니즘임.
> 2. **가치**: McKinsey 분석에 따르면成熟 IT 거버넌스 도입 기업은 IT ROI 25~40% 향상, 프로젝트 실패율 50% 감소, 의사결정 리드타임 평균 35% 단축(연 1,200시간 절감) 효과를 달성하며, SOX·GDPR 컴플라이언스 비용 20% 절감이 가능함.
> 3. **판단 포인트**: 중앙집중형(Centralized) vs 분산형(Federated) 거버넌스 모델 선택, RACI 매트릭스 내 L1/L2/L3 책임 분리 기준, KPI 포트폴리오 균형(BSC 4관점), 그리고 Tag-Governance(EA Repository 연동) 수준 결정이 아키텍처 선택의 4대 핵심 트레이드오프임.

---

## Ⅰ. 개요 및 필요성

전통적 IT 관리는 1980~90년대 애플리케이션별 **Silo 운영**(각 시스템이 독립적으로 운영되는 구조)으로 인해, 엔터프라이즈 차원의 투자 우선순위 결정, 리스크 통합 관리, 비즈니스-IT 정렬(Business-IT Alignment) 판별이 불가능했습니다. 2002년 SOX법(Sarbanes-Oxley Act), 2008년 금융위기 이후 기업들은 **엔터프라이즈 거버넌스** 요구에 직면하면서, ISACA의 **COBIT(Control Objectives for Information and Related Technologies)** 4.2 -> 5 -> 2019 버전으로 진화해왔습니다. 한국에서는 전자정부법(2007), 공공기관 정보화 사업 수행 가이드라인, 정보시스템 감리·컨설팅 제도를 통해 IT 거버넌스 표준화 요구가 제도화되었습니다.

특히 Gartner 2023 보고서에 따르면 글로벌 IT 예산 중 **Governance, Risk, Compliance(GRC) 지출이 약 8.7%**를 차지하며, 디지털 트랜스포메이션(DX) 가속화로 인해 **AI 거버넌스, 데이터 거버넌스, 클라우드 거버넌스**가 새로운 통제 영역으로 부상하고 있습니다. 이는 단순한 기술 관리를 넘어 **이사회-경영진-실무조직 3계층 의사결정 체계**와 **Value Delivery(가치 전달) 최적화**를 목적으로 합니다.

```text
+------------------------------------------------------------------+
|           엔터프라이즈 IT 거버넌스 4-Layer Reference Model         |
|                                                                  |
|  Layer 4: Corporate Governance (이사회)                           |
|  +----------------------------------------------------+          |
|  |  +--------------+  +--------------+  +----------+ |          |
|  |  | Audit Comm.  |  | Risk Comm.   |  | Strategy | |          |
|  |  +--------------+  +--------------+  +----------+ |          |
|  |  +----------------------------------------------+  |          |
|  |  |  IT Steering Committee (ITSC)                |  |          |
|  |  |  CIO, CFO, COO, 외부자문위원                 |  |          |
|  |  +----------------------------------------------+  |          |
|  +------------------------+---------------------------+          |
|  Layer 3: IT Governance Decision Making                          |
|  +------------------------+---------------------------+          |
|  |  +-------------+ +-------------+ +-------------+  |          |
|  |  |  Strategy   |-| Investment  |-|  Delivery   |  |          |
|  |  |  (ISP/EA)   | |  (Val IT)   | |  (ITIL/PMO) |  |          |
|  |  +-------------+ +-------------+ +-------------+  |          |
|  |  ------------------------------------------------  |          |
|  |  +-------------+ +-------------+ +-------------+  |          |
|  |  |   Risk      | |  Resource   | | Performance |  |          |
|  |  |  (ISO27005) | |  Mgmt(BRFC) | |  (BSC/KPI)  |  |          |
|  |  +-------------+ +-------------+ +-------------+  |          |
|  +----------------------------------------------------+          |
|  Layer 2: IT Management Processes                                |
|  +----------------------------------------------------+          |
|  | EDM(05) | APO(14) | BAI(11) | DSS(06) | MEA(04)  |  <- COBIT |
|  | -------------------------------------------------  |          |
|  |  Plan  | Build  | Run   | Monitor  | (40 Gov Obj) |          |
|  +----------------------------------------------------+          |
|  Layer 1: IT Operation & Infrastructure                          |
|  +----------------------------------------------------+          |
|  |  App  | Data | Infra | Security | Service Desk  |  |          |
|  | --- Legacy  -- Cloud -- On-Prem -- Hybrid (12%)  |  |          |
|  +----------------------------------------------------+          |
+------------------------------------------------------------------+
```

기존 패러다임 대비 새로운 패러다임의 핵심 차이는 **(1) 제어 대상의 확장** — 단순 재정 통제 -> 데이터·AI 거버넌스까지 확장, **(2) 실시간성** — 연간/분기 감사 -> Continuous Controls Monitoring(CCM), **(3) 가치 측정** — 단순 ROI -> Benefits Realization, TCO, NPV, Risk-Adjusted ROI 4축 다변량 평가, **(4) 자동화** — 수기 평가 -> GRC Platform(Archer, ServiceNow GRC, SAP GRC) 기반 워크플로우 자동화로 요약됩니다.

- **📢 섹션 요약 비유**: IT 거버넌스는 자동차의 **ADAS(첨단운전자보조시스템)**와 같습니다. 차량 자체의 엔진·브레이크는 IT 운영이고, ADAS 센서·제어 알고리즘·HUD 표시가 바로 거버넌스입니다. 운전자가 차의 모든 부품을 수동 조작하지 않아도, ADAS가 위험을 감지하고 자동으로 개입하여 사고를 예방하고 최적 경로를 안내하듯, IT 거버넌스는 비즈니스 위험을 자동 감지하고 최적의 가치 실현 경로를 제시합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019 기반 IT 거버넌스 시스템은 **Governance System(거버넌스 체계) + Governance Framework(거버넌스 프레임워크) + Components(구성요소) 7종**으로 구성됩니다. 핵심 메커니즘은 **40개 Governance Objective(거버넌스 목표)**을 5개 도메인(EDM·APO·BAI·DSS·MEA)에 할당하고, 각 목표가 **Process(프로세스), Organizational Structure(조직 구조), Information Flow(정보 흐름), People·Skills·Competencies(인적역량), Policies·Procedures(정책), Culture·Ethics·Behavior(문화), Services·Infrastructure·Applications(서비스 기반구조) 7개 구성요소**로 실현되는 **Cascade 구조**입니다.

예를 들어 **APO12(위험 관리)** 목표는 APO12.01~.06의 6개 Process Practice로 분해되며, 각 Practice는 **RACI 차트**(Responsible, Accountable, Consulted, Informed)로 12~20개 역할의 책임을 명세합니다. IT Steering Committee는 Accountable, CISO는 Responsible for Design, CFO는 Consulted, 사업부장은 Informed 수준의 책임 매트릭스가 표준입니다.

```text
+------------------------------------------------------------------+
|         COBIT 2019 Cascade Mechanism: 목표->구성요소 전파 구조     |
|                                                                  |
|  +-----------------+                                             |
|  | Stakeholder     | (위임)                                     |
|  | Needs & Drivers |------------------+                          |
|  | (이해관계자 니즈)|                  v                          |
|  +-----------------+         +---------------------+            |
|                              |  Enterprise Goals   |            |
|                              |  (13개: EG01~EG13)  |            |
|                              |  • 포트폴리오 성공  |            |
|                              |  • 리스크 최적화    |            |
|                              |  • 자원 최적화      |            |
|                              +----------+----------+            |
|                                         | (정렬)                |
|                                         v                        |
|                              +---------------------+            |
|                              |  Alignment Goals    |            |
|                              |  (13개: AG01~AG13)  |            |
|                              |  AG01: I&T 준수     |            |
|                              |  AG05: 실현된 편익  |            |
|                              |  AG12: 사이버보안   |            |
|                              +----------+----------+            |
|                                         | (전개)                |
|                                         v                        |
|                  +----------------------------------+            |
|                  |     40 Governance Objectives     |            |
|                  |  +----+ +----+ +----+ +----+    |            |
|                  |  |EDM |->|APO |->|BAI |->|DSS |    |            |
|                  |  |05  | |14  | |11  | |06  |    |            |
|                  |  +----+ +----+ +----+ +----+    |            |
|                  |           | MEA04                 |            |
|                  |           +-(피드백 루프)---------+            |
|                  +--------------+-------------------+            |
|                                 v                                |
|  +------------------------------------------------------+       |
|  | 7 Components of Governance System (구성요소 7종)     |       |
|  |                                                       |       |
|  |  +--------------+  +--------------+  +-------------+ |       |
|  |  | ① Process    |  | ② Org.Struct |  | ③ Info Flow | |       |
|  |  |  (230 실무)  |  |  (RACI 차트) |  |  (KPI/DKPI) | |       |
|  |  +--------------+  +--------------+  +-------------+ |       |
|  |  +--------------+  +--------------+  +-------------+ |       |
|  |  | ④ People&Skill| | ⑤ Policy     |  | ⑥ Culture   | |       |
|  |  |  (역량 모델)  |  |  (정책 체계)  |  |  (윤리/행동)| |       |
|  |  +--------------+  +--------------+  +-------------+ |       |
|  |  +--------------+                                    |       |
|  |  | ⑦ Service,   |  <- ServiceNow GRC, Archer,        |       |
|  |  |   Infra, App |    SAP GRC, OpenPages 등 도구      |       |
|  |  +--------------+                                    |       |
|  +------------------------------------------------------+       |
|                                                                  |
|  [Feedback Loop] <--------- MEA04 (관리, 모니터링, 평가) --------|
+------------------------------------------------------------------+
```

핵심 수치·파라미터: **CMMI(능력성 성숙도) Level 0~5 평가**에서 GO별 Process Capability Rating을 산출하며, PRM(Process Reference Model)의 **PA(Process Attribute)** 9개 항목(PA 1.1~5.2)을 0~100% 척도로 측정합니다. 목표는 **Level 3(Defined) 이상**, 차상위는 **Level 4(Managed)**, 최상위 **Level 5(Optimizing)**입니다. 예: BAI03(솔루션 구축) 목표의 PA 2.1(성과관리) 80% 이상, PA 3.1(프로세스 정의) 90% 이상을 일반 벤치마크로 봅니다.

**거버넌스 설계 시 핵심 공식:**
- **Risk-Adjusted ROI = (총 편익 - 총 비용) / (총 비용 × 리스크 확률)**
- **TCO = CapEx + OpEx(5년) + 종료비용**
- **EA Compliance Index = 준수 시스템 수 / 전체 시스템 수 × 100**

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(Evaluate, Direct, Monitor)** | 이사회·ITSC 의사결정 | 5개 Process: 거버넌스 체계 수립·운영, 편익 인도, 리스크 최적화, 자원 최적화, 이해관계자 투명성. 회의체 분기 1회, KPI 분기 보고, eGRC 대시보드 실시간 |
| **APO(Align, Plan, Organize)** | 전략-투자-포트폴리오 정렬 | 14개 Process: 관리 프레임워크, 전략, 엔터프라이즈 아키텍처, 혁신, 포트폴리오, 예산, HR, 관계, 서비스 합의, 공급자, 품질, 리스크, 보안. ISP/EA·BRP·ISP Alignment 연동 |
| **BAI(Build, Acquire, Implement)** | 솔루션 수명주기 관리 | 11개 Process: 거버넌스 요구사항 정의, 설계, 솔루션 선정, 가용성·용량, 변경, 수용, 도입, 지식, 자산, 구성, 프로젝트. PMBOK/Agile/Safe 통합 |
| **DSS(Deliver, Service, Support)** | 운영·서비스 인도 | 6개 Process: 운영, 서비스 요청/사고, 문제, 연속성, 보안 서비스, 비즈니스 프로세스 통제. ITIL 4 Service Value System, SIAM 멀티 공급자 관리 |
| **MEA(Monitor, Evaluate, Assess)** | 성능 측정·컴플라이언스 | 4개 Process: 성능·준수 모니터링, 거버넌스 체계 자체 평가, 외부 요구사항 준수. CCM(Continuous Controls Monitoring) 도구, 내부감사, ISO/IEC 38500 준거 평가 |

**설계 시 핵심 고려사항 5가지**:
1. **Focus Area(중점 영역)**: 11개 표준 FA(예: 사이버보안, DevOps, 디지털 윤리) 중 3~5개 선별 -> 총 40개 GO와 매핑
2. **Design Factor 10종**: 기업 전략, 목표 달성, 리스크, 리스크 이슈,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 545 / 800

<- **이전**: [544. IT 경영 관리 핵심 토픽 544번 시험 요약](/studynote/12_it_management/05_security_compliance/544_it_management_core_topic_544_exam_summary/)
**다음**: [546. IT 경영 관리 핵심 토픽 546번 시험 요약](/studynote/12_it_management/05_security_compliance/546_it_management_core_topic_546_exam_summary/) ->

---
