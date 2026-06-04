---
title: "690. IT 경영 관리 핵심 토픽 690번 시험 요약 (IT Management Core Topic 690 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Information Technology Governance)는 COBIT 2019, ISO/IEC 38500, ITIL 4 프레임워크를 기반으로 기업 목표(Goal Cascade)와 IT 서비스/프로젝트 포트폴리오를 정렬하여, 거버넌스-관리-운영 3계층(Governance/Management/Operations)에서 의사결정·책임·성과측정(CSF/KPI)을 체계화하는 경영 통제 체계이다.
> 2. **가치**: McKinsey 2023 보고에 따르면 성숙한 IT 거버넌스 도입 기업은 IT 투자 대비 ROI가 평균 23% 향상되고, 프로젝트 실패율 35%v, 디지털 전환 속도 2.4배, 사이버 사고 복구 시간(MTTR) 60% 단축, 감사 적발 비용 40% 절감의 정량적 효과를 달성한다.
> 3. **판단 포인트**: 중앙집권형(CoE) vs 분산형(Federated) 거버넌스 모델 선택, BCM/DR 관점에서 RTO/RPO 산정, Build vs Buy vs Cloud(SaaS/PaaS/IaaS) 의사결정 매트릭스 적용, 그리고 Zero Trust·AI 윤리(AI Act 2024)·ESG 공시 의무화(CSRD) 같은 신규 컴플라이언스 요구사항을 아키텍처 레벨에서 어떻게 흡수할지가 핵심 트레이드오프이다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX, Digital Transformation) 가속화, 클라우드 네이티브·생성형 AI(LLM)·양자컴퓨팅 등 신기술의 등장, 그리고 EU AI Act·DORA·ESG 공시 의무화(CSRD 2024) 등 규제 환경의 급격한 변화로 인해, 전통적인 IT 운영 중심 관리로는 더 이상 기업의 전략적 가치를 창출할 수 없게 되었다. 기술사(Professional Engineer) 관점에서 IT 경영 관리란 단순히 시스템 가용성을 유지하는 차원을 넘어, **기업 거버넌스(Board Level) ↔ IT 거버넌스(EDM: Evaluate-Direct-Monitor) ↔ IT 관리(Plan-Build-Run-Monitor) ↔ IT 운영(Service Operation)** 의 4계층 의사결정 구조에서 **책임(RACI), 성과(KPI/CSF), 위험(Risk Register), 가치(Benefit Realization)** 를 통합 관리하는 체계를 의미한다.

과거(2010년대 이전) IT 관리는 "코로케이션(Cooling·Power·Space) 최적화"와 "프로젝트 납기 준수"에 집중하는 Cost Center 관점이었으나, 현재(2024~)는 **Product-centric 운영(FinOps·Platform Engineering), Business Outcome 기반 가치 측정(VOI: Value of Investment), 그리고 실시간 컴플라이언스(Continuous Controls Monitoring)** 중심으로 패러다임이 전환되었다. Gartner 2024 CIO Agenda Survey에 따르면 글로벌 CIO의 89%가 "IT 거버넌스 체계를 24개월 내 재설계해야 한다"고 답하였으며, 이는 AI 거버넌스·클라우드 비용 폭증(FinOps 필요성)·공급망 리스크(SBOM·CRA) 등 신규 위협에 대한 선제적 대응이 필수임을 방증한다.

```text
+------------------------------------------------------------------+
|           IT 경영 관리 4계층 의사결정 프레임워크 (COBIT 2019)      |
+------------------------------------------------------------------+
|  Layer 1: 기업 거버넌스 (Board / Executive)                       |
|  +----------------------------------------------------------+    |
|  |  • 전략적 목표(SG) 수립: 시장점유율, ESG, 고객만족도      |    |
|  |  • Risk Appetite 선언 · 책임 한계 설정(Risk Tolerance)   |    |
|  |  • IT 투자 한도(IT Budget Cap) 승인 · 준법 감시          |    |
|  +----------------------------------------------------------+    |
|                              |                                   |
|                              v (Goal Cascade)                     |
|  Layer 2: IT 거버넌스 (EDM Domain - 5개)                         |
|  +----------------------------------------------------------+    |
|  |  EDM01: Governance Framework 수립·유지                   |    |
|  |  EDM02: Benefit Delivery 보장                            |    |
|  |  EDM03: Risk Optimization 최적화                         |    |
|  |  EDM04: Resource Optimization 자원 최적화                |    |
|  |  EDM05: Stakeholder Transparency 이해관계자 투명성        |    |
|  +----------------------------------------------------------+    |
|                              |                                   |
|                              v (Alignment)                       |
|  Layer 3: IT 관리 (Align-Plan-Organize / Build-Acquire-Implement |
|           / Deliver-Service-Support / Monitor-Evaluate-Assess)   |
|  +----------------------------------------------------------+    |
|  |  APO(14) · BAI(11) · DSS(6) · MEA(4) = 35개 Process      |    |
|  |  RACI Matrix · Process Capability Assessment(0~5)        |    |
|  +----------------------------------------------------------+    |
|                              |                                   |
|                              v (Execution)                        |
|  Layer 4: IT 운영 (Service Operation & Technical Operation)      |
|  +----------------------------------------------------------+    |
|  |  Incident·Problem·Change·Service Desk (ITIL 4 Practices) |    |
|  |  SRE: SLO/SLI/SLI, Error Budget, Toil Management         |    |
|  +----------------------------------------------------------+    |
+------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 경영 관리는 "건물의 내진설계(Seismic Design)"와 같다. 일상적 환경(일상 운영)에서는 그 존재감이 없지만, 지진(규제 변화·시장 변동성·보안 위협) 발생 시 건물의 붕괴를 막는 핵심 안전장치이며, 평소에는 보이지 않는 곳(거버넌스·정책·리스크 관리)에서 규격·재료·구조를 엄격히 관리해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 **PDCA(Plan-Do-Check-Act) 사이클**, **Cascading Goals(목표 위계)**, **RACI(Responsible·Accountable·Consulted·Informed) 매트릭스**, 그리고 **3 Lines of Defense(3LoD) 모델**로 구성된다. 기술사 시험에서 빈출되는 핵심 메커니즘을 COBIT 2019의 **Governance & Management Objectives(40개)** 구조를 기준으로 분해하면 다음과 같다.

```text
+--------------------------------------------------------------------+
|        IT 거버넌스 시스템 아키텍처 (End-to-End Control Flow)        |
+--------------------------------------------------------------------+
|                                                                    |
|   [Board]                                                          |
|      | ① Strategy & Risk Appetite 설정                             |
|      v                                                             |
|   +--------------+    ② Cascading                                       |
|   |  EDM (5)     |<-----------------+                              |
|   |  Governance   |                  | ⑦ Reporting                  |
|   +------+-------+                  |   (KPI Dashboard)            |
|          |                          |                              |
|          | ③ Direction                |                              |
|          v                          |                              |
|   +--------------+                  |                              |
|   |  Management   |   ④ Execution    |                              |
|   |  40 Objectives|------------------+                              |
|   |  APO/BAI/DSS  |                                                 |
|   |  /MEA         |                                                 |
|   +------+-------+                                                 |
|          |                                                          |
|          | ⑤ Operating                                              |
|          v                                                          |
|   +--------------+     ⑥ Performance Data                            |
|   |  Operations   |----------------------------------+              |
|   |  Service Desk |                                  |              |
|   |  SRE/DevOps   |                                  v              |
|   +--------------+                          +--------------+       |
|                                              |  MEA (4)     |       |
|                                              |  Monitor &   |       |
|                                              |  Evaluate    |       |
|                                              +------+-------+       |
|                                                     |               |
|                                                     v               |
|                                              +--------------+      |
|                                              | Continuous   |       |
|                                              | Improvement  |       |
|                                              | (CSF/KPI)    |       |
|                                              +--------------+      |
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM( Evaluate, Direct, Monitor )** | 이사회·경영진 레벨 거버넌스 의사결정 | 5개 목표(EDM01~05), `RACI` 상 Accountable=Board, 평가 주기: 분기(Q1~Q4) + 연 1회 외부 감사, 산출물: Governance Charter, Risk Appetite Statement, Investment Portfolio Review |
| **APO(Align, Plan, Organize)** | IT 전략 정렬·계획·조직 설계 | 14개 프로세스(APO01~14), 핵심: APO02(Strategy), APO05(Portfolio), APO12(Risk), APO13(Security), 도구: Jira Align·Planview·ServiceNow SPM, KPI: 전략 정렬률(%) = (전략 연계 프로젝트 수)/(전체 프로젝트 수) |
| **BAI( Build, Acquire, Implement )** | 솔루션 도입·구현·변경 관리 | 11개 프로세스(BAI01~11), 핵심: BAI03(솔루션 아키텍처), BAI06(변경 관리=CAB 승인), BAI11(프로젝트 관리), 방법론: Waterfall·Agile(Scrum/Kanban)·SAFe·Hybrid, 도구: GitHub Actions·ArgoCD·Jenkins(X-as-Code) |
| **DSS( Deliver, Service, Support )** | 서비스 운용·지원·보안 운영 | 6개 프로세스(DSS01~06), 핵심: DSS02(Incident), DSS03(Problem), DSS04(Continuity), DSS05(Security), SLA: 99.9%(Three 9s) -> 연간 8.76h, 99.99%(Four 9s) -> 52.6min 다운타임 허용 |
| **MEA( Monitor, Evaluate, Assess )** | 성과 측정·내부 통제·감사 | 4개 프로세스(MEA01~04), 핵심: MEA01(성과 모니터링), MEA02(내부 통제), MEA03(컴플라이언스), MEA04(감사), 도구: SAP GRC·ServiceNow GRC·RSA Archer |
| **CSF/KPI 체계** | 목표-지표-측정 연결 | Goal Cascade(13 Enterprise Goals ↔ 13 Alignment Goals ↔ 40 Process Goals), KPI 예: Incident MTTR < 30min, Change Success Rate > 95%, Patch Compliance > 98%, Audit Finding Close Rate > 90% (90일 내) |
| **3 Lines of Defense(3LoD)** | 리스크 통제 책임 분리 | 1st Line: 운영팀(Own risk), 2nd Line: Risk/Compliance/InfoSec(oversight), 3rd Line: Internal Audit(independent assurance), ISO 31000·COSO ERM과 연계, RACI 매트릭스로 책임 명확화 |

### 핵심 정량 산식 및 파라미터

1. **서비스 가용성 가중치(Composite Availability)**
   - $A_{composite} = 1 - \sum_{i=1}^{n}(1-A_i) \times W_i$
   - 예: 인증서비스(A=99.95%, W=0.3) + 결제서비스(A=99.99%, W=0.5) + 부가서비스(A=99.5%, W=0.2)
   - $A_{composite} = 1 - (0.0005 \times 0.3 + 0.00001 \times 0.5 + 0.005 \times 0.2) = 1 - 0.001152 = 99.885\%$

2. **프로젝트 가치 실현률(Benefit Realization Rate, BRR)**
   - $BRR = \dfrac{\sum_{i=1}^{n} RealizedBenefit_i}{\sum_{i=1}^{n} PlannedBenefit_i} \times 100\%$
   - PMBOK 7th의 Measure Performance Domain에서 강조, 일반적 기준: BRR ≥ 80% (성공), 60~80% (부분 성공), < 60% (실패)

3. **TCO(Total Cost of Ownership) 5개년 모델**
   - $TCO = CAPEX + \sum_{t=1}^{5}\frac{OPEX_t}{(1+r)^t} + DecommissioningCost$
   - CAPEX: HW/SW/License, OPEX: 인건비·전력·콜로케이션·라이선스 갱신·관리고, 할인율(r): 일반 8~10%, 공공 4.5%(KDI guideline), Decommissioning: 데이터 마이그레이션·폐기·감사 비용

4. **RTO/RPO 결정 매트릭스 (ISO 22301)**
   - Tier 1(Mission Critical): RTO ≤ 1h, RPO ≤ 5min, 동기식 복제(Metro DR), 비용: CAPEX의 30~50%
   - Tier 2(Business Critical): RTO ≤ 4h, RPO ≤ 1h, 비동기 복제(Cross-Region DR)
   - Tier 3(Operational): RTO ≤ 24h, RPO ≤ 24h, 백업 기반 복구(Backup Restore)
   - Tier 4(Administrative): RTO ≤ 72h, RPO ≤ 72h, Cold Standby

- **📢 섹션 요약 비유**: IT 거버넌스의 4계층은 "자동차의 자동 운전 시스템"과 같다. 1계층(Board)은 운전자(전략·방향), 2계층(EDM)은 차선 유지 보조 시스템(거버넌스), 3계층(Management)은 ECU 전자제어유닛(실시간 조정), 4계층(Operations)은 엔진·브레이크·타이어(실제 실행)이며, CAN 버스(데이터 통신)를 통해 4계층의 센서 데이터가 1계층의 결정으로 실시간 피드백된다.

---

## Ⅲ. 비교 및 연결

기술사 시험에서는 유사·대안 프레임워크 간 비교, 그리고 다른 아키텍처 레이어(EA·보안·프로젝트관리)과의 통합 관계를 묻는 문제가 빈출된다. 아래는 핵심 비교 매트릭스이다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 38500** | **CMMI v2.0** |
| :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스·관리 프레임워크 | IT 서비스 관리(SM) 모범 실무 | IT 거버넌스 국제표준(경영진 대상) | 조직 프로세스 성숙도 모델 |
| **대상 계층** | Board~Operations 전계층 | Service Operation~Delivery 중심 | Board / Director (EDM 레벨) | 프로젝트·프로세스·조직 |
| **구조** | 40 Governance & Management Objectives | 34 Practices + 4D 모델 | 6 Principles + 6 Principles 준수 모델 | 5 Level(1~5) + 6 Category |
| **측정/평가** | Process Capability(0~5), CSF/KPI Maturity | Service Value Chain + Continual Improvement | Conformance Audit(원칙 충족 여부) | SCAMPI Appraisal(공식 평가) |
| **인증** | COBIT 2019 Foundation/Design&Implementation | ITIL 4 Foundation/MP/SL | ISO 38500 Lead Auditor | CMMI-DEV/SVC v2.0 Maturity Level 2
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 690 / 800

<- **이전**: [689. IT 경영 관리 핵심 토픽 689번 시험 요약](/studynote/12_it_management/05_security_compliance/689_it_management_core_topic_689_exam_summary/)
**다음**: [691. IT 경영 관리 핵심 토픽 691번 시험 요약](/studynote/12_it_management/05_security_compliance/691_it_management_core_topic_691_exam_summary/) ->

---
