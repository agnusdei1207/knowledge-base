---
title: "501. EA 엔터프라이즈 아키텍처 프레임워크 (EA Enterprise Architecture Framework)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: EA(Enterprise Architecture)는 업무(Business)·데이터(Data)·응용(Application)·기술(Technology) 4계층 모델(BDAT)을 Zachman 6×6 매트릭스나 TOGAF ADM(Architecture Development Method) 사이클로 정렬하여, 조직의 전략-운영-기술 자산을 단일 청사진으로 통합하는 거버넌스 체계이다.
> 2. **가치**: Gartner에 따르면 EA 도입 조직은 IT-Portfolio 중복 제거로 25~40% 인프라 비용 절감, 변경 영향도 분석(Impact Analysis) 시간 60% 단축, 신규 비즈니스 요구사항(Time-to-Market) 대응 속도 2배 향상을 달성하며, ISO/IEC/IEEE 42010 기반의 traceable한 의사결정 체계를 확보한다.
> 3. **판단 포인트**: EA 프레임워크는 만능이 아니며, 조직의 거버넌스 성숙도(CMMI/Gartner 5단계)에 따라 **Top-Down(TOGAF ADM)** vs **Bottom-Up(도메인 EA + 재귀적 통합)** vs **Middle-Out(사전 정의 레퍼런스 모델 + 과제 중심)** 방식을 선택하고, ROI 정량화 모델(NPV, TCO 절감율)과 Change Advisory Board(CAB) 운영 강도를 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

엔터프라이즈 아키텍처는 1987년 Zachman Framework가 IBM 내부에서 출발한 이래, 1995년 미국 연방정부의 Clinger-Cohen Act(정보기술관리혁신법)와 1999년 TOGAF(The Open Group Architecture Framework) 등장으로 체계화되었다. 한국에서는 2000년대 전자정부 표준프레임워크, 2020년대 디지털정부 혁신驱动계획을 통해 공공·금융·통신·제조 분야에 확산되었으며, 현재는 클라우드 전환, MSA(Microservices Architecture), AI/MLOps, 데이터 거버넌스(데이터중심주의, Data Mesh)와 결합한 **"Adaptive EA"** 패러다임으로 진화 중이다.

과거 시스템 환경에서는 단일 벤더(IBM mainframe, Oracle ERP)의 수직 통합 아키텍처가 우세하여 EA의 필요성이 낮았지만, 2010년대 이후 **PaaS·SaaS·IaaS** 혼재, **Multi-Cloud( AWS+Azure+GCP )** 전략, **Open API·핀테크·레귤레이터리 샌드박스** 규제 환경에서는 단일 시스템 단위의 설계 한계가 드러났다. 이에 따라 *"왜(Why) 구축하는가"* 에 대한 정당화(Justification)와 *"어떻게(How) 통합·진화시키는가"* 에 대한 거버넌스 메커니즘이 필수 요구사항이 되었다.

```text
   +--------------------------------------------------------------------+
   |           엔터프라이즈 아키텍처(EA)의 진화 패러다임                    |
   |                                                                    |
   |  [1980s]              [2000s]              [2020s]                |
   |  Zachman '87 -------> TOGAF v1 '95 -------> Adaptive EA '20+        |
   |  IBM 내부 도구        The Open Group       Cloud-Native + AI       |
   |   |                    |                    |                       |
   |   v                    v                    v                       |
   |  Static Blueprint ---> ADM Cycle ---> Continuous Architecture       |
   |  (One-time 설계)      (반복 사이클)     (CI/CD + EA as Code)        |
   |                                                                    |
   |  +--------------- EA가 해결하는 4대 Pain Point ---------------+    |
   |  |  ① Shadow IT(전사 30~40% 예산 잠식)                          |    |
   |  |  ② Legacy Mainframe + Cloud 이원화(듀얼 트랙 유지비용)        |    |
   |  |  ③ 규제 컴플라이언스(전자금융감독규정, 개인정보보호법) 추적불가 |    |
   |  |  ④ 디지털 전환 ROI 불투명(투자 대비 효과 정량화 실패)          |    |
   |  +------------------------------------------------------------+    |
   +--------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: EA는 마치 **대도시의 도시계획 마스터플랜(토지이용·교통·상하수도·건축허가)** 과 같다. 개별 건물(시스템)만 잘 짓는 것이 아니라, 도시 전체의 도로·전력·용수 인프라가 어디에 어떻게 흐를지 미리 그려야 교통정체·정전·홍수를 막을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

EA는 크게 **① 계층 모델(BDAT/BIZDATA)** , **② 관점/주체 매트릭스(Zachman 6×6)** , **③ 개발 방법론(TOGAF ADM)** , **④ 산출물 레포지토리** 의 4축으로 구성된다. 이 4축은 서로 직교(orthogonal)하여, 같은 정보를 다른 각도에서 바라볼 수 있게 해준다.

### (1) BDAT 4계층 아키텍처 (Federal Enterprise Architecture Reference Model 변형)

| 계층 | 정의 | 핵심 산출물 | 기술사 출제 포인트 |
| :--- | :--- | :--- | :--- |
| **Business (B)** | 조직의 전략·프로세스·조직·역할·KPI | Value Chain Diagram, BPMN 2.0, Org Chart, RACI | BIZ 목표와 IT 정렬(Alignment), BPO(Business Process Outsourcing) 영향도 |
| **Data (D)** | 데이터 주제영역·개념/논리/물리 모델·메타데이터 | ERD(Chen/Crow's Foot), Data Dictionary, DDD Bounded Context, 데이터 카탈로그 | 데이터 거버넌스(마스터/메타/참조/거래 데이터), DAMA-DMBOK 연계 |
| **Application (A)** | 응용시스템 기능·인터페이스·컴포지션·서비스 카탈로그 | C4 Model(Container/Component/Code), API 명세서(OpenAPI 3.0), MSA 토폴로지 | 애플리케이션 포트폴리오 분석(APM: 9-Box: 적합도×중요도) |
| **Technology (T)** | 하드웨어·미들웨어·네트워크·플랫폼 | 인프라 다이어그램, 클라우드 아키텍처(AWS Well-Architected), DR(재해복구) 토폴로지 | 기술 표준(Reference Architecture), Capacity Planning, RTO/RPO |

### (2) Zachman Framework 6×6 매트릭스 (원형 모델)

```text
   +------------------------------------------------------------------+
   |              Zachman Framework for IT Architecture                |
   |                                                                  |
   |              What (데이터)    How (기능)    Where (네트워크)        |
   |            +-------------+--------------+--------------+         |
   |  Planner  | List of      | List of       | List of      |         |
   |  (전략)   | Things       | Processes     | Locations    | ...     |
   |  Row 1    | (Entity)     | (Activity)    | (Node)       |         |
   |            +-------------+--------------+--------------+         |
   |  Owner    | Semantic     | Process Model | Logistics    |         |
   |  (개념)   | Model        | (BPMN)        | Model        |         |
   |  Row 2    | (ERD)        |               | (Network)    |         |
   |            +-------------+--------------+--------------+         |
   |  Designer | Logical Data | Application   | Distributed  |         |
   |  (논리)   | Model        | Architecture  | System       |         |
   |  Row 3    | (정규화)      | (MSA)         | Architecture |         |
   |            +-------------+--------------+--------------+         |
   |  Builder  | Physical     | System        | Tech.        |         |
   |  (물리)   | Data Model   | Design        | Architecture |         |
   |  Row 4    | (DB Schema)  | (Class/Code)  | (HW/SW)     |         |
   |            +-------------+--------------+--------------+         |
   |  Sub-     | Data         | (N/A)         | (N/A)        |         |
   |  contractor| Definition  |              |              |         |
   |  Row 5    | (SQL DDL)   |              |              |         |
   |            +-------------+--------------+--------------+         |
   |  User     | Usable Data  | Working       | Functioning  |         |
   |  (운영)   | (Report/UI)  | System        | Network      |         |
   |  Row 6    |              |               |              |         |
   |            +-------------+--------------+--------------+         |
   |              Who (사람)    When (시간)    Why (동기)              |
   +------------------------------------------------------------------+
```

### (3) TOGAF ADM (Architecture Development Method) 사이클

TOGAF는 **8단계 + Preliminary + Requirements Management** 의 사이클로, *Plan-Do-Check-Act(데밍 사이클)* 와 동일한 연속적 개선 구조를 가진다.

```text
   +--------------------------------------------------------------+
   |                    TOGAF ADM Cycle (8 Phases)                 |
   |                                                               |
   |                  +----------------------+                     |
   |                  | Preliminary Phase    | (프레임워크 정의)     |
   |                  | - 거버넌스/원칙 수립   |                     |
   |                  +----------+-----------+                     |
   |                             v                                  |
   |   +----------+   +--------------+   +--------------+         |
   |   | Phase A  |--->|   Phase B    |--->|   Phase C    |         |
   |   | Vision   |   | Business Arch|   |  Data Arch   |         |
   |   | (비전)    |   | (BA)         |   |  (DA)        |         |
   |   +----------+   +--------------+   +------+-------+         |
   |        ^                                     v                 |
   |   +----+-----+  +--------------+   +--------------+         |
   |   |   Phase H|  |  Phase G     |<---|  Phase D     |         |
   |   | Change   |  | Implementation|  | Technology   |         |
   |   | Mgmt     |  | Governance    |  |  Arch (TA)   |         |
   |   +----+-----+  +------+-------+   +------+-------+         |
   |        |               ^                     |                 |
   |   +----+-----+  +------+-------+   +--------+------+         |
   |   |  Phase F |  |  Phase E     |<---| Requirements  |         |
   |   | Migration|  | Opportunities |  | Management    |         |
   |   | Planning |  | & Solutions   |  | (전 단계)      |         |
   |   +----------+  +--------------+   +---------------+         |
   |                                                               |
   |   ★ 핵심 원리: ADM은 "전체(Whole) EA"를 한 번에 완성하는 것이   |
   |     아니라, Architecture Iteration (A->B->C->D->E->F 반복) 으로     |
   |     점진적 정제(Incremental Refinement) 한다.                   |
   +--------------------------------------------------------------+
```

### 구성 요소별 역할 및 기술

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Architecture Repository (저장소)** | EA 자산의 단일 진실 공급원(SSOT) | Ardoq, LeanIX, Bizzdesign, Avolution, MEGA Hopex, iServer, EA-as-Code (Structurizr DSL, C4-PlantUML) |
| **Architecture Board (거버넌스 위원회)** | 아키텍처 결정, 예외 승인, 표준화 | Architecture Review Board(ARB), Change Advisory Board(CAB), 디자인 리뷰(DR) |
| **Architecture Capability (인재/조직)** | EA 수행 조직·역할 정의 | Chief Architect, Domain Architect, Solution Architect, Enterprise Architect, TOGAF/PMP/CISSP 인증 |
| **Architecture Content Framework** | 산출물 메타모델·템플릿 | ADM 산출물 카탈로그(Deliverable/Artifact), 메타모델(엔티티-속성-관계), ArchiMate 3.2 표준 |
| **Architecture Governance** | 표준 준수 검증·예외 관리 | Architecture Compliance Review(ADR: Architecture Decision Record), TOGAF Architecture Repository |
| **Reference Models & Patterns** | 재사용 가능한 참조 아키텍처 | AWS Well-Architected, Azure CAF, Google Cloud CAF, Gartner Magic Quadrant, EA 패턴 카탈로그 |

### ArchiMate 3.2 핵심 요소 (표준 EA 표기 언어)

```text
   ArchiMate 3.2 계층별 핵심 요소
   +--------------------------------------------------------+
   |  Business Layer    : Actor, Role, Process, Service,    |
   |                      Function, Event, Goal, Outcome    |
   |  Application Layer : Component, Interface, Service,     |
   |                      Data Object, Function             |
   |  Technology Layer  : Node, Device, System Software,    |
   |                      Artifact, Communication Path,     |
   |                      Infrastructure Interface          |
   |  Strategy Layer    : Resource, Capability,             |
   |                      Course of Action, Value Stream     |
   |  Physical Layer    : Equipment, Facility, Material      |
   |  Implementation & Migration : Work Package, Deliverable|
   |                          , Gap, Plateau                |
   |                                                        |
   |  ★ 구조적 관계: Composition, Aggregation, Assignment,  |
   |    Realization, Serving, Access, Influence, Triggering,|
   |    Flow, Specialization, Association                    |
   +--------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Zachman의 6×6 매트릭스는 **도시계획의 '주체-대상-관점' 매트릭스** 와 같다. 시장을 꿈꾸는 사람(Perspective=Planner), 토목기술자(Designer), 시공자(Builder), 입주자(User) 모두 같은 도시를 다른 시점에서 바라보지만, **모두 같은 데이터(도로·건물·수도관)** 를 다루므로 매트릭스 셀이 일관되게 채워져야 한다.

---

## Ⅲ. 비교 및 연결

### 1. EA 프레임워크 간 비교 (TOGAF vs Zachman vs FEAF vs DoDAF)

| 구분 | **TOGAF** | **Zachman** | **FEAF** | **DoDAF** | **Gartner** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **기원** | The Open Group (1995) | John Zachman (IBM, 1987) | 미국 연방정부 OMB (1999) | 미국 국방성 (1995) | Gartner Research (2003) |
| **구조** | ADM 8단계 + Repository | 6×6 매트릭스(분류체계) | 5계층(전략->기술) | 8 Viewpoint(AV/CV/DV 등) | 4A(Application·Integration· ...) |
| **강점** | 방법론(How)·반복적 ADM·ArchiMate 연계 | 메타모델(What)·완전성 보장 | 정부 컴플라이언스·PRM | 군사·임무 중심·CV(현황/목표) | 비즈니스 전략 연계·거버넌스 강조 |
| **약점** | 정량화 도구 부족 | 방법론 부재(분류만 제공) | 민영 적용 어려움 | 민간 적용 시 과잉 엔지니어링 | 프레임워크라기보다 평가/조언 중심 |
| **산출물 수** | ADM 산출물 50+ | 36 셀 매트릭스 | 5 PRM 모델 | 8 Viewpoint × 52 모델 | Continuous Architecture Flow |
| **표준 연계** | ArchiMate 3.2, BPMN, UML | 독립적 | FEAF DRM/BRM/SRM/ARM/IRM/TRM | DoDAF Meta-Model (DM2) | EA as Code, BIAN,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 501 / 600

<- **이전**: [500. 정보화 전략 수립 ISP 방법론](/studynote/11_design_supervision/06_exam_summary/500_isp_information_strategy_planning_method)
**다음**: [502. TOGAF ADM 아키텍처 개발 방법](/studynote/11_design_supervision/06_exam_summary/502_togaf_adm_architecture_development_metho/) ->

---
