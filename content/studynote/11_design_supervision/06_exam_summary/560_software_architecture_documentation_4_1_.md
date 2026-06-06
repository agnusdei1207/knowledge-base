---
title: "560. SW 아키텍처 문서화 4+1 뷰 (Software Architecture Documentation 4+1 View)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Philippe Kruchten(1995)이 RUP(Rational Unified Process) 컨텍스트에서 제안한 4+1 뷰 모델은 단일 시스템 아키텍처를 **Logical View(논리), Process View(프로세스), Physical View(물리), Development View(개발) + Scenarios(유스케이스)** 의 5개 동시(concurrent) 관점으로 분리 문서화하여, 각 이해관계자(stakeholder)의 관심사(concerns)를 별도의 모델로 충족하는 다중 뷰(multi-view) 기반 아키텍처 표기법이다.
> 2. **가치**: 단일 다이어그램(예: E-R 다이어그램 하나만으로 시스템 표현)으로는 포착 불가능한 4대 아키텍처 품질 속성 — 기능성·유지보수성(Development/Logical), 성능·확장성·가용성(Process/Physical), 배포·운영성(Physical) — 을 별도 모델로 분리하여, IEEE 1471/ISO 42010의 "관심사-뷰-관점" 메타모델을 실질적으로 구현한다.
> 3. **판단 포인트**: 5개 뷰 전체 적용은 대규모 분산 시스템·엔터프라이즈 시스템에서 ROI가 높지만, 단순 MSA·소규모 시스템에서는 **C4 Model**(Simon Brown) 또는 경량 ADR(Architecture Decision Record)로 대체하는 것이 효율적이며, 뷰 간 정합성(view-to-view consistency) 검증 자동화 여부가 실무 적용의 핵심 성공 요인이다.

---

## Ⅰ. 개요 및 필요성

1990년대 객체지향 분석/설계(OOAD) 방법론이 성숙하면서, 단일 UML 다이어그램(예: 클래스 다이어그램)만으로 분산 환경·다층(multi-tier) 시스템의 모든 아키텍처 결정을 표현하는 것이 불가능해졌다. Booch, Rumbaugh, Jacobson이 UML 0.9를 1996년에 통합한 배경에도, Rational Software의 Philippe Kruchten은 1995년 IEEE Software지에 *"The 4+1 View Model of Architecture"* 를 발표하며, 아키텍처는 단일 모델이 아닌 **"여러 동시적 뷰의 집합"** 이라는 관점을 정립했다.

핵심 동기는 **stakeholder 간의 communication gap 해소** 였다. 엔드유저는 기능(what)에만 관심이 있고, 시스템 운영자는 배포·장애 대응(where/how)에 관심을 가지며, 개발자는 모듈 구조·빌드 단위(how)에 집중한다. 이질적인 요구사항을 단일 모델에 우겨넣으면 "모두에게 의미 없고, 누구에게도 완전하지 않은" 다이어그램이 만들어진다.

```text
        4+1 View Model — 이해관계자(Stakeholder) 중심 분리

                          +---------------------+
                          |   +1 Scenarios /    |
                          |   Use-Case View     |  <- End-User, Domain Expert
                          |   (모든 뷰를 검증)   |
                          +----------+----------+
                                     | 일관성 검증
              +----------------------+----------------------+
              |                      |                      |
   +----------v----------+ +--------v--------+ +----------v----------+
   | 1. Logical View     | | 2. Process View  | | 3. Physical View    |
   | (논리 뷰)            | | (프로세스 뷰)     | | (물리/배포 뷰)        |
   | End-User 기능        | | Non-functional   | | System Engineer     |
   | Class·Object 다이어  | | 동시성·성능·가용성 | | Deployment·Topology |
   | 그램, Sequence       | | Activity, State  | | Node 다이어그램       |
   +---------------------+ +-----------------+ +---------------------+
                                     |
                          +----------v----------+
                          | 4. Development View|
                          | (개발/구현 뷰)      |
                          | Programmer·Manager |
                          | 모듈·패키지·컴포넌트|
                          | Component·Package  |
                          +---------------------+
```

**기존 단일 뷰 패러다임 vs 4+1 뷰 패러다임의 비교**:
- **기존(Pre-4+1)**: 클래스 다이어그램 하나가 시스템 구조·동작·배포까지 암묵적으로 표현 -> E-R 다이어그램 + 클래스 다이어그램 + DFD(Data Flow Diagram)가 섞여 있어 가독성 저하, "**big design up front**" 안티패턴 초래
- **4+1 이후**: 뷰별로 **관심사(concerns)** 를 분리하고, 뷰 간 **mapping(예: Logical Class -> Process Component -> Physical Node -> Development Module)** 을 명시적으로 관리. 이는 추후 **C4 Model**(Simon Brown, 2006)·**ArchiMate**(The Open Group)·**arc42**(德国 Gernot Starke)의 토대가 됨

- **📢 섹션 요약 비유**: 4+1 뷰는 마치 **건물의 설계도면 세트**와 같다 — 건축주는 인테리어 평면도(Logical View), 소방관은 스프링클러·피난 동선도(Process View), 시공업체는 배관·전기 배선도(Physical View), 구조 엔지니어는 기둥·보 배치도(Development View)만 각각 필요로 한다. 모든 도면을 한 장에 그리면 전문가 모두가 혼란에 빠진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

4+1 뷰 모델의 핵심 메커니즘은 **5개 뷰의 동시성(concurrency)** 과 **scenarios에 의한 교차 검증** 이다. 즉, 5개 뷰는 동일한 시스템의 5개 "투영(projection)"이며, 시스템의 진실은 단일 뷰가 아닌 뷰들의 일관성(consistency)에 있다.

```text
        4+1 뷰의 상호작용 및 매핑(Mapping) 구조

   +----------------------------------------------------------+
   |              +1 Scenarios (Use-Case View)                |
   |   +--------+ +--------+ +--------+ +--------+          |
   |   | UC-01  | | UC-02  | | UC-03  | | UC-04  | ...      |
   |   |결제처리 | |주문취소 | |재고동기화| |장애복구 |          |
   |   +---+----+ +---+----+ +----+---+ +----+---+          |
   +-------+----------+-----------+-----------+--------------+
           |          |           |           |
   +-------v----+ +---v----+ +---v-----+ +---v-----+
   |  Logical   | |Process | |Physical | |Develop- |
   |  View      | | View   | |  View   | |ment View|
   |            | |        | |         | |         |
   |Class:Pay-  | |Process:| |Node:    | |Module:  |
   |mentService | |Settle- | |order-db | |payment- |
   | Class:Order| |ment-   | | Node:   | |service  |
   | Class:Stock| |Worker  | |kafka-   | | (Gradle |
   |            | |Thread  | |broker   | | multi-  |
   |            | |  Pool  | | Node:   | | module) |
   |            | |        | |pay-gw   | |         |
   +------------+ +--------+ +---------+ +---------+
        ^                ^           ^             ^
        |                |           |             |
        +----------------+-----------+-------------+
                  Traceability / View-Mapping
                  (예: Eclipse EMF, Sparx EA, Structurizr DSL)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **1. Logical View (논리 뷰)** | 시스템이 **무엇**(what)을 제공할지 모델링. 도메인 개념·핵심 기능·객체 간 정적·동적 관계 표현. End-User 및 도메인 분석가 대상. | UML **Class Diagram**(도메인 모델: Order, Payment, Inventory), **Sequence Diagram**(시나리오별 메시지 교환), **State Machine Diagram**(엔티티 라이프사이클). EA(Enterprise Architect)에서 "Logical" 패키지 명명 규약 적용. |
| **2. Process View (프로세스 뷰)** | 시스템의 **런타임 동작 특성**(동시성, 성능, 가용성, 분산 트랜잭션) 모델링. 시스템이 Non-functional 요구사항을 어떻게 충족하는지 표현. | UML **Activity Diagram**(비즈니스 워크플로우), **Sequence Diagram** with `par`/`alt`/`loop` 프래그먼트, **Communication Diagram**. **Saga Pattern**(MSA), **2PC/3PC**, **Circuit Breaker**(Resilience4j, Hystrix) 등 런타임 메커니즘 표현. |
| **3. Physical View (물리/배포 뷰)** | 소프트웨어 아티팩트가 **하드웨어 노드**(서버, 컨테이너, 클라우드 리소스)에 어떻게 매핑되는지 모델링. 시스템 엔지니어·SRE·DevOps 대상. | UML **Deployment Diagram**(Node, Artifact, CommunicationPath), **Component Diagram**(물리적 배포 가능한 단위). AWS·GCP·Azure 아키텍처 아이콘과의 매핑(Kubernetes Pod ↔ Node, Service Mesh ↔ Process), Terraform/Pulumi 코드와 동기화. |
| **4. Development View (개발/구현 뷰)** | **소프트웨어 모듈·패키지·라이브러리**의 정적 조직과 빌드 의존성 모델링. 프로그래머·프로젝트 매니저 대상. | UML **Component Diagram**(소프트웨어 컴포넌트·인터페이스), **Package Diagram**(계층화: `com.company.{domain, infra, app}`), 빌드 도구 그래프(**Gradle/Maven/CMake dependency graph**), 모노레포(예: Nx, Bazel) 모듈 경계. |
| **+1. Scenarios (유스케이스 뷰)** | 위 4개 뷰를 **연결(binding)·검증(validating)** 하는 시나리오 집합. "아키텍처가 살아있는지" 확인. | UML **Use-Case Diagram**, **Sequence Diagram**의 `ref` 다이어그램 간 참조. 각 시나리오는 Logical 클래스의 협업 -> Process 컴포넌트 호출 -> Physical 노드 간 통신 -> Development 모듈 빌드 산출물로 추적 가능해야 함. |

**View-Mapping(뷰 간 정합성) 메커니즘**:
실무에서는 4개 뷰가 독립적으로 작성되면 **"이 클래스는 어느 프로세스에서 실행되고, 어느 노드에 배포되며, 어느 모듈에 속하는가?"** 라는 매핑 정보가 소실된다. 이를 해결하기 위해:
1. **ArchiMate**(The Open Group 표준)는 `ApplicationComponent` ↔ `Node` ↔ `CommunicationPath` 간의 **realization/assignment/usedBy** 관계로 뷰 간 매핑을 형식화
2. **Structurizr DSL**(Simon Brown)은 코드 기반(`workspace.dsl`)으로 4개 뷰를 단일 진실 공급원(SSOT)에서 자동 생성
3. **Sparx EA·Visual Paradigm**은 `Traceability Window`로 클래스 ↔ 컴포넌트 ↔ 노드 간 링크를 추적
4. **현대적 대안**: C4 Model(`Context/Container/Component/Code`)은 4+1을 단순화·현대화한 모델로, Markdown + 코드 DSL로 GitOps 친화적

**주요 파라미터·결정 기준**:
- **뷰 적용 깊이**: 5개 전체 / 3개(Logical + Physical + Development) / 1개(C4의 Container+Context만) — 시스템 복잡도와 팀 규모에 따라 결정
- **표현 표기법**: UML 2.5(정통) vs C4(경량) vs ArchiMate(엔터프라이즈 EA) vs arc42(독일식, 12섹션 템플릿)
- **자동화 수준**: 수동 다이어그램(Visio/draw.io) / 코드 기반(Structurizr, PlantUML, Mermaid) / 양방향 추적(Sparx EA, Cameo Systems Modeler)
- **갱신 주기**: Sprint 단위(애자일) / 릴리스 단위 / ADR(Architecture Decision Record) 단위

- **📢 섹션 요약 비유**: 4+1 뷰는 **의료 진단의 5가지 검사**와 같다 — X-ray(Logical: 뼈의 구조), 혈액검사(Process: 순환·대사), CT(Physical: 장기 배치), MRI(Development: 연부조직), 청진(Scenarios: 실제 호흡·심음). 한 가지 검사만으로 종합 진단이 불가능하듯, 단일 뷰로 아키텍처 전체를 판단할 수 없다.

---

## Ⅲ. 비교 및 연결

| 구분 | **4+1 View Model (Kruchten, 1995)** | **C4 Model (Simon Brown, 2006·개정 2018)** | **ArchiMate (The Open Group, 2009~3.2)** | **arc42 (Gernot Starke, 2010~)** |
| :--- | :--- | :--- | :--- | :--- |
| **목적** | 객체지향 분산 시스템의 이해관계자별 관점 분리 | 소프트웨어 아키텍처의 계층적·현대적 단순화 | 엔터프라이즈 아키텍처(EA) 전체(Business·Application·Technology) 통합 모델 | 아키텍처 문서화 템플릿(문서 구조 강조) |
| **표기법** | UML 2.5 다이어그램(Class/Component/Deployment/Use-Case) | 4단계 다이어그램(Context/Container/Component/Code) + 보충 뷰(Deployment 등) | 자체 그래픽 표기법(Layer: Business·Application·Technology·Physical, Aspect: Active·Structure·Behavior·Composite·Motivation) | 다이어그램 표기법 무관(UML/C4/ArchiMate 자유 선택) |
| **적용 규모** | 중·대규모 OO 시스템, RUP 프로젝트 | MSA·컨테이너·클라우드 네이티브 환경에 최적 | 엔터프라이즈 전체(업무·애플리케이션·인프라 통합) | 소규모~대규모 모두, 12섹션 템플릿 |
| **도구 지원** | Sparx EA, MagicDraw, Rational Rose, PlantUML | Structurizr DSL, draw.io, Mermaid, PlantUML | BiZZdesign, Sparx EA(ArchiMate 플러그인), Archi(오픈소스) | asciidoctor
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 560 / 600

<- **이전**: [559. 아키텍처 거버넌스 원칙 가이드라인](/studynote/11_design_supervision/06_exam_summary/559_architecture_governance_principles_guide)
**다음**: [561. 아키텍처 평가 ATAM CBAM 트레이드오프](/studynote/11_design_supervision/06_exam_summary/561_architecture_evaluation_atam_cbam_tradeo/) ->

---
