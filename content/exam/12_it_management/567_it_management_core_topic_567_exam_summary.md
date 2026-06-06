---
title: "IT Management Core Topic 567 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(IT Governance)는 COBIT 2019, ISO/IEC 38500, ITIL 4 등 글로벌 표준 프레임워크를 기반으로 IT 전략-이행-운영-평가를 통합 관리하는 **EDA(Enterprise Governance of IT) 체계**이며, 핵심 메커니즘은 **RACI 매트릭스, KGI/KPI 캐스케이드, 포트폴리오 파이프라인 관리**를 통해 비즈니스 가치 실현을 보장하는 것이다.
> 2. **가치**: 잘 설계된 IT 거버넌스 체계 도입 시 IT 투자 대비 ROI는 평균 **15~25% 향상**, IT 프로젝트 실패율은 McKinsey 기준 평균 30%에서 **10% 미만**으로 감소하며, 규제 준수(컴플라이언스) 비용은 약 **40% 절감**된다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **집중형(Centralized) vs 분산형(Federated) 거버넌스 모델 선택**, **규제 강도(Strict Control) vs 사업 민첩성(Business Agility)**, **표준 프레임워크 채택도(High Alignment) vs 자체 역량 고도화(Native Capability)** 사이의 균형점 설계이며, 조직의 **거버넌스 성숙도(Level 1~5)**에 따라 단계적 도입 전략이 결정된다.

---

## Ⅰ. 개요 및 필요성

21세기 디지털 전환(DX) 환경에서 기업 IT 시스템은 더 이상 단순한 비용센터(Cost Center)가 아닌 **전략적 비즈니스 인에이블러(Strategic Business Enabler)**이자 **가치 창출 플랫폼(Value Creation Platform)**으로 격상되었다. 그러나 한국정보화진흥원(NIA)의 「2023년 국내 정보화 현황」에 따르면, 국내 대기업의 약 **67.4%**가 IT 투자 대비 명확한 가치 측정에 어려움을 겪고 있으며, CIO Survey 2023(Gartner)에선 **89%의 기업**이 IT와 비즈니스 전략의 정렬(Strategic Alignment)에 실패를 경험했다고 보고한다.

특히 2020년 코로나19 이후 급격한 비대면·원격근무 전환, 2023년 생성형 AI(ChatGPT, LLM)의 폭발적 확산, 그리고 2024년 본격화된 **EU AI Act**, **개인정보보호법 4차 개정**, **ISMS-P 인증제 강화** 등 규제 환경의 급변은 전통적인 IT 관리 체계를 근본적으로 재설계할 것을 요구하고 있다. 한국정보관리기술사 시험의 567번 토픽은 바로 이 **IT 거버넌스와 전략 관리 통합 체계**를 다루며, 단순한 IT 운영 관리를 넘어 **전사적 거버넌스(EGP, Enterprise Governance)**와 **IT 가치 실현(Value Realization)** 메커니즘을 종합적으로 평가한다.

과거 1990~2000년대 IT 관리 패러다임은 **기술 중심(Business-Driven IT)**이었으나, 현재는 **IT 주도의 비즈니스 혁신(IT-Driven Business Innovation)**으로 전환되었다. 이는 SOA, MSA(Microservices Architecture), DevOps, Cloud-Native, DataOps, AIOps 등 기술 패러다임의 변화뿐 아니라, **코소(KOSO) 원칙**, **3Lines 모델**, **ISO 37000(거버넌스 국제표준)** 같은 관리 거버넌스 패러다임 변화와 직결된다.

```text
+-----------------------------------------------------------------+
|        IT 거버넌스 진화 패러다임 (Evolution of IT Governance)     |
+-----------------------------------------------------------------+
|                                                                 |
|  [1980s]        [2000s]         [2010s]         [2024+]         |
|   IT관리         ITIL v2/v3      COBIT 5        COBIT 2019     |
|   데이터         BSC for IT      ISO 38500       ISO 37000     |
|  처리센터       (1996)          (2008)          (2021)         |
|   |              |               |               |              |
|   v              v               v               v              |
|  기술중심 ---> 프로세스중심 ---> 가치중심 ---> 생태계중심           |
|  (Tech-      (Process-        (Value-        (Ecosystem-     |
|   Centric)    Centric)         Centric)       Centric)        |
|                                                                 |
|  +----------+    +----------+    +----------+    +----------+  |
|  | COBIT    |---->| COBIT    |---->| COBIT    |---->| COBIT    |  |
|  | 4.1      |    | 5        |    | 2019     |    | 2019+    |  |
|  | (2005)   |    | (2012)   |    | (2018)   |    | AI/ESG   |  |
|  +----------+    +----------+    +----------+    +----------+  |
|                                                                 |
|  [핵심 변화] : Control Objective -> Management System ->          |
|               Value Governance System (VGS)                     |
+-----------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **도시의 종합 교통체계**와 같습니다. 도로(인프라), 신호등(규제), 경찰(컴플라이언스), 내비게이션(전략) 모두가 조화롭게 작동해야 시민(비즈니스)이 안전하고 빠르게 목적지에 도달할 수 있습니다. 신호등만 강화하면 정체, 도로만 깔면 사고 — 이 균형이 핵심입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 거버넌스의 핵심 아키텍처는 **COBIT 2019의 거버넌스 시스템 컴포넌트(Governance System Components, 40개)**와 **ISO/IEC 38500의 6원칙(Principle)**을 결합한 **통합 거버넌스 레퍼런스 모델(IGRM, Integrated Governance Reference Model)**로 구성된다. 크게 **5개 계층**으로 분류할 수 있다.

```text
+----------------------------------------------------------------------+
|            IT 거버넌스 5계층 아키텍처 (5-Layer Architecture)            |
+----------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------+    |
|  | Layer 1: 원칙 및 정책 (Principles & Policies)               |    |
|  |  • ISO 38500 6원칙 (Responsibility, Strategy, Acquisition, |    |
|  |    Performance, Conformance, Human Behavior)                |    |
|  |  • COBIT 2019 Governance/Management Objectives (40개)      |    |
|  |  • 조직 고유 IT 정책 (Information Security Policy, AUP)     |    |
|  +------------------------------------------------------------+    |
|                              ^                                       |
|  +------------------------------------------------------------+    |
|  | Layer 2: 의사결정 및 구조 (Decision & Structure)            |    |
|  |  • 이사회(Board) -> IT 전략위원회(ISC) -> IT운영위원회(IOC)   |    |
|  |  • 3 Lines 모델 (Business, Risk/Compliance, Internal Audit) |    |
|  |  • RACI 매트릭스 (Responsible, Accountable, Consulted,     |    |
|  |    Informed)                                                |    |
|  +------------------------------------------------------------+    |
|                              ^                                       |
|  +------------------------------------------------------------+    |
|  | Layer 3: 프로세스 및 통제 (Process & Control)               |    |
|  |  • EDM(05) - Evaluate, Direct, Monitor                    |    |
|  |  • APO(14) - Align, Plan, Organize                         |    |
|  |  • BAI(11) - Build, Acquire, Implement                     |    |
|  |  • DSS(06) - Deliver, Service, Support                     |    |
|  |  • MEA(04) - Monitor, Evaluate, Assess                    |    |
|  |   -------- COBIT 2019 : 40개 프로세스 --------              |    |
|  +------------------------------------------------------------+    |
|                              ^                                       |
|  +------------------------------------------------------------+    |
|  | Layer 4: 역량 및 자원 (Capability & Resources)             |    |
|  |  • 7가지 구성요소 (Components): Process, Structure, Info,   |    |
|  |    People/Skills, Culture/Behavior, Service/Infrastructure, |    |
|  |    Goals/Metrics                                            |    |
|  |  • 성숙도 모델 (CMMI 5단계 / COBIT PAM 0~5단계)             |    |
|  +------------------------------------------------------------+    |
|                              ^                                       |
|  +------------------------------------------------------------+    |
|  | Layer 5: 측정 및 개선 (Measure & Improve)                  |    |
|  |  • KGI(Key Goal Indicators) - EDM 계층                     |    |
|  |  • KPI(Key Performance Indicators) - Process 계층          |    |
|  |  • CSF(Critical Success Factors)                           |    |
|  |  • CSF -> KGI -> KPI 캐스케이드 매핑                          |    |
|  |  • Balanced Scorecard 4관점 (Financial, Customer, Internal, |    |
|  |    Learning/Growth)                                        |    |
|  +------------------------------------------------------------+    |
|                                                                      |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate, Direct, Monitor)** | 이사회·경영진의 IT 거버넌스 의사결정 | 5개 프로세스(EDM01~05)로 구성, GRC(Governance-Risk-Compliance) 도구 연동, **연간 거버넌스 회의 주기** 및 **의사결정 임계값(threshold)** 기반 자동 알림 |
| **APO (Align, Plan, Organize)** | IT 전략-비즈니스 전략 정렬, 포트폴리오 관리 | 14개 프로세스(APO01~14), **전략 정렬 매트릭스(SAM, Strategy Alignment Matrix)** 활용, **TOGAF ADM(Architecture Development Method)**과의 통합, **IT 투자 포트폴리오**를 BCG 매트릭스 형태로 분류(Star/Cash Cow/Question Mark/Dog) |
| **BAI (Build, Acquire, Implement)** | IT 솔루션 도입 및 배포 | 11개 프로세스(BAI01~11), **PMBOK 7th**, **PRINCE2**, **SAFe(Scaled Agile Framework)** 통합, **DevSecOps 파이프라인** (Plan-Code-Build-Test-Release-Deploy-Monitor) |
| **DSS (Deliver, Service, Support)** | IT 서비스 운영 및 사용자 지원 | 6개 프로세스(DSS01~06), **ITIL 4 Service Value System(SVS)** 기반, **SLA 99.9%/99.99%** 단계별 관리, **AIOps**를 통한 이상 탐지(MTTR 50% 단축) |
| **MEA (Monitor, Evaluate, Assess)** | 성과 측정 및 컴플라이언스 | 4개 프로세스(MEA01~04), **Balanced Scorecard**, **COSO ERM 2017**, **ISO 31000**과 연계, **내부통제**(Internal Control) 평가 및 **ISMS-P**, **PIMS** 인증 심사 |
| **KGI/KPI 캐스케이드** | 목표-성과 연계 측정 | **CSF(임계 성공 요인) -> KGI(핵심 목표 지표) -> KPI(핵심 성과 지표)** 3단계 계층, **예**: CSF "고객 만족" -> KGI "NPS 60 이상" -> KPI "1차 해결률 85%, 응답시간 30초 이내" |

**핵심 측정 메커니즘 - RACI & 3 Lines 모델**

```text
+--------------------------------------------------------------+
|              Three Lines of Defense (3 Lines 모델)             |
+--------------------------------------------------------------+
|                                                              |
|  +------------------------------------------------------+   |
|  | 1st Line : 사업부서 / IT 운영팀 (Owners of Risk)      |   |
|  |  • 일상적 IT 통제 운영                                |   |
|  |  • RACI에서 R(Responsible) 역할                       |   |
|  |  • 예: 시스템 운영자, 개발자, 서비스 데스크           |   |
|  +------------------------------------------------------+   |
|                          ^                                    |
|  +------------------------------------------------------+   |
|  | 2nd Line : 리스크관리·컴플라이언스·정보보안 (CISO,    |   |
|  |             CRO, DPO)                                 |   |
|  |  • 정책·표준 수립, 모니터링                            |   |
|  |  • RACI에서 A(Accountable), C(Consulted) 역할         |   |
|  |  • 예: 정보보안팀, 개인정보보호팀, IT감사팀            |   |
|  +------------------------------------------------------+   |
|                          ^                                    |
|  +------------------------------------------------------+   |
|  | 3rd Line : 내부감사 (Internal Audit)                   |   |
|  |  • 독립적 검증, assurance 제공                         |   |
|  |  • RACI에서 I(Informed) 역할                          |   |
|  |  • 외부감사(External Audit) 조정                       |   |
|  +------------------------------------------------------+   |
|                                                              |
|  ※ IIA(Institute of Internal Auditors) 2020 갱신본 적용     |
+--------------------------------------------------------------+
```

**핵심 파라미터 및 수식**:

- **IT 거버넌스 성숙도 (Capability Level)**: COBIT PAM(Process Assessment Model) 기준 0~5단계
  - Level 0: 불완전(Incomplete) -> Level 1: 초기(Initial) -> Level 2: 관리(Managed) -> Level 3: 정의(Defined) -> Level 4: 정량적 관리(Quantitatively Managed) -> Level 5: 최적화(Optimizing)
- **가치 실현률(Value Realization Rate, VRR)**:
  ```
  VRR = (실제 실현 가치 / 계획된 가치) × 100 (%)
  ※ 목표: 80% 이상
  ```
- **IT ROI 계산식**:
  ```
  IT ROI = (IT 투자로 인한 순이익 - IT 투자비용) / IT 투자비용 × 100 (%)
  ```
- **TCO(Total Cost of Ownership)**:
  ```
  TCO = 직접비(하드웨어+소프트웨어) + 간접비(운영+유지보수+교육+다운타임)
  ```
- **NPS(Net Promoter Score) 기반 IT 만족도**: 촉진자(%) - 비추천자(%)

- **📢 섹션 요약 비유**: IT 거버넌스의 5계층은 **의료 시스템**과 같습니다. Layer 1(원칙)은 헌법·의료법, Layer 2(의사결정)는 병원장·의료진 회의, Layer 3(프로세스)는 진단·수술 절차,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 567 / 800

<- **이전**: [566. IT 경영 관리 핵심 토픽 566번 시험 요약](/studynote/12_it_management/05_security_compliance/566_it_management_core_topic_566_exam_summary/)
**다음**: [568. IT 경영 관리 핵심 토픽 568번 시험 요약](/studynote/12_it_management/05_security_compliance/568_it_management_core_topic_568_exam_summary/) ->

---
