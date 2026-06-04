+++
title = "502. TOGAF ADM 아키텍처 개발 방법 (TOGAF ADM Architecture Development Method)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TOGAF ADM(Architecture Development Method)은 엔터프라이즈 아키텍처(EA)를 8개 단계(Preliminary, A~H)와 Requirements Management로 구성된 반복적(Iterative) 사이클로 개발하는 Open Group의 표준 방법론으로, Business/Data/Application/Technology 4개 도메인을 아키텍처 뷰(View)와 뷰포인트(Viewpoint)로 추상화하여 전략-전환-거버넌스 흐름을 통합 관리한다.
> 2. **가치**: ADM 적용 시 아키텍처 산출물 재사용률 40~60% 향상, 프로젝트 중복 투자 20~30% 절감, 의사결정 속도 3~5배 개선(실제 Gartner/Forrester 사례 기준)되며, Architecture Repository 기반의 통제된 거버넌스로 전사 IT 정합성을 확보한다.
> 3. **판단 포인트**: 프로젝트 특성에 따라 **Iteration 패턴**(전체 사이클 반복 vs Phase G/H 중심 vs Phase A 중심)을 선택하고, **ADM Baseline vs Target vs Transition** 시점의 경계 정의, 그리고 **SBB(Solution Building Block)** 적용 시 ABB(Architecture Building Block)와의 매핑 정밀도가 아키텍처 ROI의 결정적 변수가 된다.

---

## Ⅰ. 개요 및 필요성

TOGAF ADM은 1995년 The Open Group의 전신인 The Open Group consortium에서 출발하여, 기존 Zachman Framework이 제공하는 분류 체계(What/How/Where/Who/When/Why)는 있으나 **"어떻게 만들어야 하는가"**에 대한 프로세스가 부재한 한계를 해결하기 위해 등장했다. ADM은 단순 문서 템플릿이 아니라, **"전략적 목표 -> 아키텍처 비전 -> 상세 설계 -> 이행 -> 거버넌스"**로 이어지는 엔터프라이즈 아키텍처 라이프사이클 전체를 정의하는 **반복적-점진적(Iterative-Incremental) 개발 방법론**이다.

기존 2000년대 초반까지의 엔터프라이즈 아키텍처는 **Big-Bang Approach**(수년 단위 일회성 문서화)에 의존하여, 비즈니스 환경 변화 시 산출물이 즉각 obsolete 처리되거나, 문서는 존재하지만 실제 프로젝트와 괴리가 큰 **"Drawerware(서랍속 아키텍처)"** 현상이 빈번했다. ADM은 **Requirements Management**를 사이클 중앙에 배치하여 사이클 외부의 새로운 요구사항을 흡수하고, Phase A~H 각 단계의 **Statement of Architecture Work**를 통해 점진적으로 정제하는 방식을 채택한다. 또한 **TOGAF 9.2 -> 10(2024~2025 발행 예정)**의 흐름에서는 **Agile/Lean 통합**, **Digital Transformation 가속화**, **Practical EA** 트랙을 통해 경량화(Lean ADM) 지원을 강화하고 있다.

```text
[ TOGAF ADM 사이클 전체 구조 ]

                     +--------------------------------+
                     |  Preliminary Phase             |
                     |  (프레임워크/거버넌스 정의)    |
                     +-------------+------------------+
                                   |
                                   v
              +-----------------------------------------+
              |   Requirements Management (중앙 허브)   |◄------+
              |   (요구사항 변경 흡수)                  |       |
              +----+------+------+------+------+--------+       |
                   |      |      |      |      |                |
                   v      v      v      v      v                |
              Phase A  Phase B Phase C Phase D Phase E ...------+
              (Vision) (Biz)  (Info)  (App)  (Tech)
                   |      |      |      |      |
                   +------+------+------+------+
                              |  Gap 분석
                              v
                       Phase F (Migration Planning)
                              |
                              v
                       Phase G (Implementation Governance)
                              |
                              v
                       Phase H (Architecture Change Management)
                              |
                              v
              (전체 사이클 재진입 / 신규 사이클 시작)
```

- **📢 섹션 요약 비유**: ADM은 마치 **도시계획 수립-시공-유지보수**의 전 과정을 다루는 마스터플랜과 같다. 한 번 도시를 짓고 끝나는 것이 아니라, 신축·재개발·재정비의 순환 과정을 거쳐 도시가 진화하듯, ADM도 **"지금의 도시(As-Is) -> 5년 후的理想 도시(To-Be) -> 단계별 재개발(Transition)"** 사이클을 끊임없이 반복한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ADM의 핵심 메커니즘은 **Architecture Development Cycle**과 이를 둘러싼 3개 컴포넌트(Architecture Content, Capability, Governance & Repository)의 상호작용이다. 8단계 + Requirements Management + Preliminary = 총 10개 컴포넌트가 **Architecture Repository**라는 단일 진실 공급원(Source of Truth)을 중심으로 협업한다.

ADM의 8개 Phase는 다음의 역할을 수행한다:
- **Preliminary**: TOGAF 프레임워크 자체를 조직에 맞춤(Customization)하고 Architecture Capability, Board, Principles를 정의
- **Phase A (Architecture Vision)**: 이해관계자(Stakeholder) 식별, Architecture Vision 문서, Stakeholder Map 작성, Request for Architecture Work 검토
- **Phase B (Business Architecture)**: Baseline/Target Business Architecture, 조직·역할·프로세스·기능 모델링(BPMN, ARIS, UML Activity)
- **Phase C (Information Systems Architectures)**: Data Architecture(CIA - Conceptual/Logical/Physical)와 Application Architecture 매핑
- **Phase D (Technology Architecture)**: 물리적/논리적 컴포넌트 배치, 플랫폼(OS, 미들웨어, 네트워크) 정의
- **Phase E (Opportunities & Solutions)**: SBB 식별, Work Package/Architecture Building Block(ABB) -> SBB 매핑
- **Phase F (Migration Planning)**: Transition Architecture, Implementation & Migration Plan, Project Portfolio 매핑
- **Phase G (Implementation Governance)**: 실제 이행 프로젝트의 아키텍처 적합성 검증(Compliance Review)
- **Phase H (Architecture Change Management)**: 새로운 요구·기술 변화에 대한 Architecture Repository 업데이트 및 사이클 재시작 트리거

**ADM Iteration**은 4가지 패턴으로 분류된다:
1. **Architecture Iteration**: 전체 ADM 사이클을 처음부터 반복
2. **Development Iteration**: 단일 Phase 내에서의 산출물 정제
3. **Transition Iteration**: Phase G/H 사이의 이행 사이클
4. **Platform Iteration**: 동일 Phase에서 플랫폼/OS 별 변형

```text
[ ADM Phase별 산출물 및 핵심 기법 흐름 ]

 Preliminary          Phase A             Phase B             Phase C/D
+----------+      +----------+       +----------+       +----------+
| 원칙     |      | 비전     |       | Baseline |       | Baseline |
| 거버넌스 |------>| 이해관계 |------->| Target   |------->| Target   |
| 표준     |      | 자 맵    |       | Biz Mod  |       | Data/App |
| Repository|     | SOW 초안 |       | Gap      |       | Tech Mod |
+----------+      +----------+       +----------+       +----------+
                                                                |
                                                                v
                          Phase E <------  Phase F  <------ Gap 분석
                       +----------+    +----------+      +----------+
                       | SBB 식별 |    | 이행계획 |      | Gap      |
                       | WP 정의  |    | Portfolio|      | Statement|
                       | ROA/CBA  |    | Transition|     | Impact   |
                       +----------+    +----------+      +----------+
                              |              |
                              v              v
                          Phase G  <------ Implementation
                       +----------+
                       | Architecture
                       | Contract
                       | Compliance
                       | Review
                       +----------+
                              |
                              v
                          Phase H
                       +----------+
                       | Change   |
                       | Repository|
                       | Update   |
                       +----------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Architecture Repository** | 통합 저장소 | Architecture MetaModel(코어+확장), **Architecture Landscape(0~3번 영역)**: 0.Architectural Repository, 1.Standards Information Base, 2.Reference Architectures, 3.Populated Architectures, 4.Governance Logs |
| **Architecture Content Framework** | 산출물 메타모델 | Deliverable/Artifact/Building Block(ABB/SBB/ARB/SRB) 구분, **ABB(Architecture Building Block)**는 논리적/추상적, **SBB(Solution Building Block)**는 구현 가능한 시스템 컴포넌트 |
| **ADM Guidelines & Techniques** | 35+ 보조 기법 | Stakeholder Management, Architecture Patterns, Business Scenarios, Gap Analysis, Migration Planning Techniques, Interoperability Requirements, Risk/Cost Assessment, **Business Transformation Readiness Assessment**, Capability-Based Planning |
| **Architecture Capability Framework** | 조직 역량 | Architecture Board(ARB), Architecture Governance(Compliance/Survey/Reviews), Architecture Skills Framework(Role: Sponsor/Architect/Designer/Implementer) |

**핵심 메커니즘 - Gap 분석 & Transition Architecture**:
ADM의 진정한 차별점은 **Gap Analysis**를 통해 Baseline(현재 상태) - Target(목표 상태) 차이를 도출하고, 이를 **Transition Architecture**(중간 단계)로 분해하여 Work Package 단위로 이행 가능하게 만드는 것이다. Gap = {Target Capability} - {Baseline Capability} + {Transition delta}, 이 공식이 **Implementation Factor, Cost %, Time %**로 분해되어 Phase F의 **Implementation & Migration Plan(IMP)**을 산출한다. 여기서 **Cost% = f(Delta Capability, Complexity Factor)**로 산정되며, 일반적으로 Phase F에서 CBA(Cost-Benefit Analysis)와 함께 ROA(Return on Architecture Investment)를 측정한다.

**ArchiMate 3.2와의 매핑**:
TOGAF ADM 산출물은 **ArchiMate** 언어와 1:1 매핑된다. 예) Phase A의 Architecture Vision은 ArchiMate의 **Motivation Layer(Goal, Driver, Stakeholder)**, Phase B의 Business Architecture는 **Business Layer(Process, Service, Function, Actor)**, Phase C/D는 **Application/Technology Layer**로 표현된다. 이는 **TOGAF Series Guide: ArchiMate 3.0 Bridge** 문서에 상세히 명세되어 있다.

- **📢 섹션 요약 비유**: ADM Phase A~H는 마치 **집 짓기 공정도**와 같다. A(설계 컨셉 도출) -> B(거실·주방 배치) -> C(배관·전기 배선) -> D(자재·규격 확정) -> E(인테리어 옵션 선정) -> F(시공 일정표) -> G(시공 감리) -> H(완공 후 증축·개조). 각 공정마다 도면(Deliverable)이 쌓여 결국 **건축물 증명서(Architecture Contract)**로 귀결된다.

---

## Ⅲ. 비교 및 연결

TOGAF ADM은 EA 프레임워크 시장에서 다른 표준들과 비교되며 상호보완적으로 사용된다. 특히 Zachman은 **분류 체계(Classification)**, TOGAF ADM은 **프로세스(Process)**, FEAF는 **성과관리(Performance Reference Model)**, DoDAF는 **국방 도메인 뷰(View)**, Gartner은 **방법론 통찰(Methodology Insights)**을 강조한다.

| 구분 | **TOGAF ADM** | **Zachman Framework** | **FEAF (Federal EA)** | **DoDAF 2.0** |
| :--- | :--- | :--- | :--- |
| **핵심 초점** | 아키텍처 개발 프로세스(How) | 분류 체계/관점 매트릭스(What) | 미국 연방정부 표준 + PRM | 국방 도메인 All-View 모델링 |
| **반복성** | Iterative(8+1 Phase Cycle) | 비반복적(분류 메타모델) | 비반복적(5개 Reference Model) | 비반복적(8개 View) |
| **산출물** | Deliverables, Artifacts, Building Blocks | 셀(Cell) 6×5=30개 매트릭스 | PRM, BRM, SRM, DRM, ARM | AV, OV, SV, TV, DIV, StdV, SvcV 등 8 View |
| **거버넌스** | Architecture Board, Compliance Review | 미정의(메타모델만 제공) | EA Assessment, A-EMAF | FITBWG, Configuration Management |
| **표현 언어** | ArchiMate 3.2(연동) | 미정의(중립) | DoDAF/DM2(일부) | DoDAF Meta Model(DM2) |
| **기술사 활용** | 민간 SI/공공 EA 사업의 **사실상 표준** | 분류 기준 제시 시 인용 | 공공부문 RFP 응답 시 | 국방 M&S, C4I 시스템 설계 시 |

**상호운용성 및 통합 패턴**:
- **TOGAF + ArchiMate**: Open Group 통합 전략으로, ADM Phase B는 ArchiMate Business Layer로, Phase C/D는 Application/Technology Layer로 매핑. **TOGAF-ArchiMate Mapping Guide** 참조
- **TOGAF + BPMN**: Phase B의 비즈니스 프로세스 모델링 시 BPMN 2.0을 사용, ArchiMate Business Process와 1:1 매핑
- **TOGAF + UML**: Phase C의 Application/Component 설계 시 UML Class/Component/Deployment Diagram 활용
- **TOGAF + SAFe/Agile**: Phase E~G에서 **SAFe Program Increment(PI)** 단위로 Work Package 매핑, **Agile ADM** 경량화 패턴(TOGAF 9.2 Supplement)
- **TOGAF + ITIL 4**: Phase G의 거버넌스 단계에서 Service Value System과의 연계(SVS) - Change Enablement, Service Design

- **📢 섹션 요약 비유**: EA 프레임워크를 **의료 시스템**에 비유하면, TOGAF ADM은 **진료 절차 매뉴얼(어떤 검사를 어떤 순서로 할지)**, Zachman은 **환자 정보 분류 체계(체온·혈압·혈액형 어디에 기록할지)**, FEAF은 **미국 의료보험 청구 표준 양식**, DoDAF는 **군진 병원 특수 프로토콜**이라고 할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

EA 사업을 수행하는 기술사는 ADM의 **적용 범위(Scope)**, **Iteration 주기**, **거버넌스 깊이**를 비즈니스 임팩트와 조직 성숙도에 맞춰 결정해야 한다. **Gartner EA Maturity Model(0~5 레벨)**에서 Level 2~3 조직은 ADM Core + Iteration + Architecture Repository 구축이 필수, Level 4 이상은 Lean ADM + Agile + Real-Time Architecture Health Check로 진화한다.

### 기술사형 판단 체크리스트

1. **Iteration Depth 결정**: 단일 프로젝트 EA vs 전사 EA에 따라 Phase 반복 깊이를 결정했는가? (예: Digital Transformation SI는 Phase A+B 집중, Legacy Modernization은 Phase D~G 반복)
2. **Baseline 정밀도 검증**: As-Is Architecture를 정량적 지표(응답시간, 가용성, ROI)로 측정 가능한 수준으로 작성했는가? (단순 org chart ❌ -> 정량 KPI 매핑 ⭕)
3. **Gap 분석의 Work Package 분해 정밀도**: Gap -> Transition Architecture -> Work Package로 3단계 이상 분해했는가? WP가 6개월 이내 1팀 단위 수행 가능한 크기(<= 50 person-month)인가?
4. **SBB-ABB 매핑 검증**: Phase E에서 정의한 SBB가 기존 SI Vendor 솔루션과 **100% 1:1 매핑** 가능한지, 또는 커스터마이징 발생 시 Architecture Contract에 반영했는가?
5. **Architecture Governance 활성화**: Phase G의 Compliance Review가 단순 체크리스트 ❌, 실제 프로젝트 Board 승인 게이트 ⭕로 작동하는가? 비준수 시 Architecture Exception Process가 운영되는가?

### 피해야 할
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 502 / 600

<- **이전**: [501. EA 엔터프라이즈 아키텍처 프레임워크](/knowledge-base/studynote/11_design_supervision/06_exam_summary/502_ea_enterprise_architecture_framework/)
**다음**: [503. Zachman 프레임워크 분류 체계](/knowledge-base/studynote/11_design_supervision/06_exam_summary/503_zachman_framework_classification/) ->

---
