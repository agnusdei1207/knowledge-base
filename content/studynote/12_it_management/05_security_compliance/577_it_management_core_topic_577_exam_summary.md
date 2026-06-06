---
title: "IT Management Core Topic 577 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

# 577. IT 경영 관리 핵심 토픽 577번 시험 요약 (IT Management Core Topic 577 Exam Summary)

> **Note**: 본 노트는 정보관리 기술사 시험 대비를 위한 IT 경영관리 통합 심화 정리로, COBIT 2019, ITIL 4, ISO/IEC 38500, ISO/IEC 20000, 정보시스템 감리/감사 프레임워크를 핵심 축으로 구성되었습니다.

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 **COBIT 2019(거버넌스/관리 목표 40개), ITIL 4(34개 Practices), ISO 38500(6원칙), ISO 20000(서비스경영시스템)** 등 4대 국제 표준을 기반으로, **Value(가치) ↔ Risk(위험) ↔ Resource(자원)** 3축의 균형을 통해 기업 전략과 IT의 정렬(Strategic Alignment)을 달성하는 통합 프레임워크임
> 2. **가치**: McKinsey 연구에 따르면 성숙한 IT 거버넌스 도입 기업은 **IT 투자 ROI 23% 향상, 프로젝트 실패율 38% 감소, 사이버 사고 대응 시간(MTTR) 67% 단축, 규정 준수 비용 41% 절감** 등 정량적 효과 입증
> 3. **판단 포인트**: **거버넌스 체계(Board-Level vs Executive-Level) 선택**, **프레임워크 통합 수준(별도 운영 vs 매핑 통합)**, **자동화 범위(수동 통제 vs GRC 플랫폼 연계)**, **측정 지표(Leading vs Lagging Indicator 비중)**이 핵심 설계 의사결정 사항

---

## Ⅰ. 개요 및 필요성

디지털 전환(Digital Transformation)이 가속화되면서 IT는 더 이상 단순 비용 센터(COST Center)가 아닌 **전략적 자산이자 사업 경쟁력의 핵심**으로 자리매김했습니다. 그러나 Gartner 2023 보고에 따르면, 전체 IT 예산 중 **30%만이 가치 창출에 기여**하며, CIO의 71%가 "IT-사업 정렬(Alignment) 부족"을 최대 고충으로 보고하고 있습니다. 이러한 환경에서 IT 경영관리(IT Management)는 기술 자체가 아닌 **기술을 통한 가치 실현**을 체계적으로 관리하는 방법론으로 진화했습니다.

특히 4차 산업혁명, 규제 강화(개인정보보호법, ESG 공시), 원격근무 확산, 사이버 위협 고도화 등으로 인해 IT 의사결정의 **투명성·책임성·감사 가능성**이 요구되며, 이를 뒷받침할 **거버넌스(Governance)** 체계의 정착이 필수 불가결해졌습니다.

```text
+-------------------------------------------------------------+
|          IT 경영관리 4-Layer 통합 참조 모델 (4-LIRM)         |
+-------------------------------------------------------------+
|  [Layer 4] 전략/비전        : ESG, Digital Strategy, ROI    |
|        |                                                  |
|        v                                                  |
|  [Layer 3] 거버넌스         : COBIT 2019, ISO 38500         |
|        |   (의사결정/책임)     Board ↔ Executive ↔ Mgmt    |
|        v                                                  |
|  [Layer 2] 관리/운영         : ITIL 4, ISO 20000, DevOps   |
|        |   (서비스/프로세스)     34 Service Value Chain     |
|        v                                                  |
|  [Layer 1] 통제/감사         : IS Audit, 감리, Compliance  |
|            (검증/보고)         SOX, GDPR, ISMS-P           |
+-------------------------------------------------------------+
       |                                    |
       |            [Cross-Cutting]         |
       +--- Security (ISO 27001), Risk (ISO 31000), Architecture (TOGAF) ---+
```

**기존 vs 새로운 패러다임**:
- **기존(2000년대)**: IT는 비용, 개별 프로젝트 단위 관리, 사후 통제
- **현재(2024~)**: IT는 가치, **E2E Value Stream** 관리, **실시간 Risk-based 통제**, **Data-Driven 의사결정**

- **📢 섹션 요약 비유**: IT 경영관리는 **자동차의 계기판·네비게이션·자동주행 시스템**과 같습니다. 엔진(IT 인프라)이 아무리 좋아도, 운전자가 속도·연료·경로를 실시간으로 보지 못하면 목적지에 안전히 도달할 수 없습니다. COBIT은 **계기판**, ITIL은 **운전 매뉴얼**, ISO 38500은 **교통법규**에 해당합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 핵심 프레임워크 아키텍처

```text
+----------------------------------------------------------------+
|                IT 경영관리 4대 표준 통합 아키텍처              |
|                                                                |
|   +---------------+         +-----------------+                |
|   |  ISO/IEC      | 원칙    |  COBIT 2019     | 목표/지표     |
|   |   38500       |--------->|                 |                |
|   |  (거버넌스)   |         |  (40 Governance |                |
|   |  Responsibility|        |  & Mgmt Obj)    |                |
|   |  Strategy      |        |                 |                |
|   |  Acquisition   |        |  5 Domains:     |                |
|   |  Performance   |        |  EDM,APO,BAI,   |                |
|   |  Conformance   |        |  DSS,MEA        |                |
|   |  Human Behav.  |         +--------+--------+                |
|   +---------------+                  |                         |
|                                      | 매핑                    |
|   +---------------+                  v                         |
|   |  ISO/IEC      |         +-----------------+                |
|   |   20000       |<---------|  ITIL 4         |                |
|   |  (SMS 인증)   | 프로세스 |  (34 Practices) |                |
|   |               |         |                 |                |
|   |  Plan-Do-     |         |  SVS:           |                |
|   |  Check-Act    |         |  Opportunity->   |                |
|   |  10 Process   |         |  Demand->Value->  |                |
|   |  Group        |         |  SVC            |                |
|   +---------------+         +-----------------+                |
|                                                                |
|   [상시 협업]  Risk(ISO 31000)  ·  Security(ISO 27001)         |
+----------------------------------------------------------------+
```

### 구성 요소별 상세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **이사회/거버넌스 위원회** | 최종 의사결정 및 책임 | **RACI 매트릭스** 활용, **이사회 IT 위원회** 분기별 운영, CIO 보고 체계 수립, ISO 38500 **6원칙** 적용 (Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior) |
| **CISO/GRC 조직** | 위험·규정·컴플라이언스 통합 | **GRC 플랫폼**(Archer, ServiceNow GRC, SAP GRC) 활용, **Risk Register** 운영, **KRI(핵심위험지표)** 실시간 모니터링, Three Lines of Defense 모델 적용 |
| **IT 서비스 운영팀** | 서비스 가치 전달 | **ITIL 4 Service Value System(SVS)** 운영: Opportunity & Demand -> Value -> **Service Value Chain**(Plan/Improve/Engage/Design&Transition/Obtain/Build/Deliver&Support), **CSI(지속적 서비스 개선)** 등록부 운영 |
| **정보시스템 감사/감리** | 독립적 검증 및 보증 | **ISACA CISA/CRISC** 자격 기반 감사, **Risk-Based Audit Planning**, **CAATs(컴퓨터 감사 기법)** 활용, **데이터 분석**(ACL, IDEA, Python), **TPN(Third Party Notification)** 평가 |
| **전략기획/PMO** | IT-사업 정렬 | **포트폴리오 관리**(PPM 도구: Planview, Clarity), **Benefits Realization Plan** 수립, **BSC(Balanced Scorecard)** 4관점(재무/고객/내부/학습성장) KPI 설계 |
| **아키텍처 거버넌스** | 표준 및 기술 정합성 | **TOGAF 10 ADM**(Preliminary->A->B->C->D->E->F->G->H->Requirements Mgmt), **ArchiMate 3.2** 모델링, Architecture Review Board 운영 |

### 핵심 메커니즘: COBIT 2019의 **Governance System Principles**

COBIT 2019는 **6개의 Governance System Principles**와 **5개의 Governance Framework Principles**를 통해 IT 거버넌스 체계를 설계합니다:

1. **각기 다른 이해관계자에게 차별적 가치 제공**(Stakeholder Value)
2. **전사적 통합 거버넌스 시스템**(Holistic Approach) - 5도메인(EDM/APO/BAI/DSS/MEA) × 7콤포넌트(Principles/Processes/Organizational Structures/Flows/People/Information/Culture)
3. **단일 통합 프레임워크 적용**(Integrated System)
4. **요구사항에 맞춰 범위 조정 가능**(Scalable)
5. **사업 환경 변화에 대응**(Dynamic)
6. **거버넌스 시스템 자체의 평가 및 개선 가능**(Governance over Governance)

**핵심 공식**:
$$\text{거버넌스 성숙도} = f(\text{목표 달성률}, \text{위험 통제 효과성}, \text{자원 활용 효율}) = \frac{\sum_{i=1}^{n}(KPI_i \times W_i)}{\sum Risk\ Exposure}$$

**중요 지표(NGF)**:
- **Process Capability Level**(0~5): ISO/IEC 15504 기반 PAM(Process Assessment Model) 적용
- **Maturity Level**(1~5): GAPP(Generally Accepted Process Principles)
- **Risk Appetite vs Tolerance**: 위험 식욕 vs 위험 허용도 차이 명확화

- **📢 섹션 요약 비유**: COBIT 2019의 5도메인은 **병원 운영 체계**와 같습니다. EDM(원장/이사회)이 정책을 정하고, APO(진료과)가 계획을 세우며, BAI(치료/수술)가 변화를 만들어내고, DSS(입원/간호)가 서비스를 지속 제공하며, MEA(검사/평가)가 성과를 측정합니다. 모든 과정이 **환자 가치(Stakeholder Value)** 중심으로 연결됩니다.

---

## Ⅲ. 비교 및 연결

### 1) COBIT 2019 vs ITIL 4 vs ISO 38500

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** |
| :--- | :--- | :--- | :--- |
| **핵심 목적** | IT 거버넌스 & 관리 목표 | IT 서비스 관리(Service Management) | IT 거버넌스 원칙(Governance) |
| **범위** | 전사(Enterprise-wide) | 서비스 수명주기(End-to-End Service) | 이사회(Board) 거버넌스 |
| **구조** | 5도메인, 40 Governance/Management Objectives | SVS, 34 Practices, 9 Guiding Principles | 6원칙, 3-Tier Model |
| **대상 독자** | CIO, 이사, 감사인, 위험관리자 | IT 운영자, 서비스 매니저, DevOps | 이사회, 경영진, 준법감시인 |
| **측정** | Process Capability / Maturity Level | KPI, SLO, SLA, CSI 등록부 | 원칙 준수 평가(Conformance Review) |
| **인증** | COBIT Certified(Foundation/Design/Implementation) | ITIL Foundation/Master/Strategic Leader | ISO 38500 Lead Auditor |
| **통합성** | 정책/지표/통제 중심 | 프로세스/활동/도구 중심 | 원칙/가이드라인 중심 |
| **최신 버전** | 2019 (2018 발표) | 4 (2019, 2024 갱신) | 2015 (현재 revision 진행) |
| **강점** | 거버넌스-관리-통제 통합 | Agile/DevOps 친화적 Value Stream | 이사회 관점의 가치·위험 균형 |
| **약점** | 구현 복잡도 높음, 학습곡선 | 거버넌스 측면 약함 | 구체적 프로세스 부재 |

### 2) 전통적 IT 관리 vs 현대 IT 경영관리

| 구분 | **전통적(2010 이전)** | **현대적(2020 이후)** |
| :--- | :--- | :--- |
| 관점 | **ITIL v3** (26 Process, 5 Lifecycle) | **ITIL 4**(Service Value System, 34 Practice) |
| 거버넌스 | COBIT 4.1/5 (Maturity Level 중심) | COBIT 2019 (목표/위험/자원, Flex Framework) |
| 보안 통제 | 보안은 별도 영역 | **DevSecOps**, Zero Trust, NIST CSF 통합 |
| 위험 관리 | 사후 통제, 보험 중심 | **Risk-Based**, KRIs 실시간 모니터링, ISO 31000 |
| 측정 | 가용성(Availability) 위주 | **VBC(Value-Based Care)**, **VSM(Value Stream Management)** |
| 컴플라이언스 | 개별 규정 대응 | **통합 GRC**, Control Mapping (한 통제 -> 다 규정) |
| 자동화 | 수동 CMDB, 티켓 시스템 | **AIOps**, **Observability**, **GitOps**, **Policy-as-Code** |

### 3) 다른 시스템과의 통합 포인트

- **프로젝트 관리(PMP/PMBOK 7)**: **Benefits Realization** 단계에서 COBIT EDM02(Ensured Benefits Delivery) 연계
- **애자일/SAFe**: **ITIL 4 Practices**(Service Desk, Incident, Change)와 **DevOps CALMR**(Culture/Automation/Lean/Measurement/Recovery) 융합
- **보안(ISO 27001)**: **Statement of Applicability(SOA)**를 COBIT 관리 목표와 매핑
- **아키텍처(TOGAF)**: **Architecture Repository**를 COBIT의 Information Flow로 활용
- **재무(ESG/IFRS S1·S2)**: **IT 관련 ESG 지표**(탄소, 데이터 거버넌스, 사이버 회복력) 보고 체계 연계

- **📢 섹션 요약 비유**: COBIT은 **헌법(원칙)**, ITIL은 **행정 절차**(서비스 운영), ISO 38500은 **대통령 훈령(거버넌스 원칙)**과 같습니다. 이 셋은 서로 모순되지 않고 **계층적으로 상호보완**하며, **보안(ISO 27001)**과 **위험(ISO 31000)**은 횡
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 577 / 800

<- **이전**: [576. IT 경영 관리 핵심 토픽 576번 시험 요약](/studynote/12_it_management/05_security_compliance/576_it_management_core_topic_576_exam_summary/)
**다음**: [578. IT 경영 관리 핵심 토픽 578번 시험 요약](/studynote/12_it_management/05_security_compliance/578_it_management_core_topic_578_exam_summary/) ->

---
