+++
title = "414. ArchiMate 아키텍처 모델링 언어 (ArchiMate Architecture Modeling Language)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ArchiMate는 The Open Group이 제정한 엔터프라이즈 아키텍처(EA) 전용 시각화 모델링 언어로, **비즈니스 계층(Business Layer)**, **애플리케이션 계층(Application Layer)**, **기술 계층(Technology Layer)**의 3계층 구조와 **동기(Motivation)**, **구현 및 마이그레이션(Implementation & Migration)** 확장으로 TOGAF ADM과 1:1로 매핑되는 구조적 설계를 가능하게 한다.
> 2. **가치**: ArchiMate 3.2 기반으로 약 70여 개의 표준화된 요소(Element)와 11개의 관계(Relationship)를 제공하여, 조직 내 **이해관계자 간의 공통 어휘(Common Vocabulary)** 확립과 **아키텍처 의사결정의 추적성(Traceability)** 보장을 통해 EA 산출물의 재사용성과 일관성을 40~60% 향상시킨다.
> 3. **판단 포인트**: **관심사 분리(Separation of Concerns)** 측면에서 UML의 4+1뷰, BPMN의 프로세스 중심, ArchiMate의 다중 계층 간사 교차(Cross-Layer) 매핑 중 어느 것을 채택할지, **ArchiMate 3.0의 `Composition`, `Aggregation`, `Assignment`, `Realization` 등 구조적 관계의 의미 중첩** 문제를 어떻게 뷰(Viewpoint)로 정제할지가 핵심 설계 결정 사항이다.

---

## Ⅰ. 개요 및 필요성

전통적인 시스템 설계는 UML 클래스 다이어그램, ERD, 네트워크 토폴로지 다이어그램 등 **기술 사일로(Silo)** 별로 분절된 표기법을 사용해 왔다. 그러나 2000년대 들어 Zachman Framework, TOGAF, FEAF 등 **엔터프라이즈 아키텍처(EA)** 프레임워크가 보편화되면서, **"비즈니스 전략 -> 애플리케이션 서비스 -> IT 인프라"** 로 이어지는 End-to-End 가시성(Traceability) 확보가 필수 요구사항이 되었다. 이러한 배경에서 2004년 네덜란드 Telematica Instituut를 중심으로 출발한 ArchiMate는 2008년 The Open Group의 공식 표준(OGC 표준)으로 채택되었으며, 2024년 현재 **ArchiMate 3.2** 버전이 EA 모델링의 사실상 표준(De Facto Standard) 위치를 점유하고 있다.

기존 1990년대 말 ~ 2000년대 초의 EA 모델링 환경은 Zachman Matrix의 셀(Cell)마다 상이한 표기법(각각 30여 종의 도구 종속 표기법)을 사용해 동일 산출물의 **수직·수평 일관성** 붕괴라는 치명적 문제가 있었다. ArchiMate는 이를 **단일 메타모델(Single Metamodel)** 기반의 통일된 그래픽 문법으로 해소하며, TOGAF ADM(Architecture Development Method)의 Preliminary, A(아키텍처 비전), B(비즈니스), C(정보시스템/데이터·애플리케이션), D(기술), E(기회 및 솔루션), F(마이그레이션 계획), G(구현 거버넌스), H(아키텍처 변경 관리), Requirements Management 9단계 산출물을 직접 모델링할 수 있는 53개(3.1 기준) -> 70여 개(3.2 기준)의 요소와 11종 관계로 정형화한다.

```text
[ArchiMate 3계층 + 2확장 구조 개요도]
+------------------------------------------------------------------+
|                    MOTIVATION (동기 확장)                        |
|   [Stakeholder]->[Driver]->[Goal]->[Principle]->[Requirement]      |
|       +-------------------+-----------------------+             |
|                           v                                     |
|  +-------------+   +-------------+   +-------------+           |
|  |  BUSINESS   |--->| APPLICATION |--->|  TECHNOLOGY |           |
|  |   LAYER     |   |    LAYER    |   |   LAYER     |           |
|  |  비즈니스   |   | 애플리케이션|   |    기술     |           |
|  |  +-------+  |   |  +-------+  |   |  +-------+  |           |
|  |  |Business|  |   |  |App    |  |   |  |Node   |  |           |
|  |  |Actor   |  |   |  |Comp   |  |   |  |Device |  |           |
|  |  |Service |  |   |  |Service|  |   |  |SystemS |  |           |
|  |  |Process |  |   |  |Data   |  |   |  |Artifact|  |           |
|  |  +-------+  |   |  +-------+  |   |  +-------+  |           |
|  +-------------+   +-------------+   +-------------+           |
|       ^                  |                  |                  |
|       | Realization      | Realization      |                  |
|       +------------------+------------------+                  |
|                           v                                     |
|   IMPLEMENTATION & MIGRATION (구현/마이그레이션 확장)           |
|   [WorkPackage]->[Deliverable]->[Gap]->[Plateau]->[Transition]    |
+------------------------------------------------------------------+
```

또한 ArchiMate는 **단일 뷰가 아닌 뷰포인트(Viewpoint) 기반 다중 뷰**를 지원한다. ArchiMate 3.1 사양(ArchiMate 3.1 Specification, OGC, 2019)에서는 **내장 31종 + 사용자 정의 가능**의 표준 뷰포인트(예: Layered Viewpoint, Service Realization Viewpoint, Application Cooperation Viewpoint, Migration Viewpoint, Stakeholder Viewpoint, Goal Realization Viewpoint 등)를 정의하여, 동일 메타모델에서 다양한 이해관계자(임원, 아키텍트, 개발자, 운영자)별 슬라이스(Slice)를 추출할 수 있다.

- **📢 섹션 요약 비유**: ArchiMate는 마치 **도시계획의 GIS 지도**와 같다. 도시 전체의 토지이용(비즈니스), 건물용도(애플리케이션), 도로·상하수도(기술)를 한 장의 통합 지도에 색깔별로 표기함으로써, "왜 이 건물이 이 도로 위에 지어졌는가"를 과거 -> 현재 -> 미래로 추적할 수 있게 해준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ArchiMate의 메타모델은 **구조(Structure) - 행동(Behavior) - 정보(Information)**의 3분류와 **능동/수동/외부**의 행위자 분류로 이루어진다. 핵심적으로 **3개의 핵심 엔터티 타입**(Active Structure, Behavior, Passive Structure)이 직교적으로 결합되어 모든 요소를 표현한다.

```text
[ArchiMate 핵심 메타모델: 행위자(Active/Behavior/Passive) 교차 구조]
+------------------------------------------------------------------+
|  [Active Structure]     [Behavior]           [Passive Structure]|
|   능동 구조             행동(서비스)          수동 구조          |
|   +----------+         +----------+          +----------+       |
|   | Business |         | Business |          | Business |       |
|   |  Actor   |<---[A]--->| Service  |<---[A]---->|  Object  |       |
|   +----------+         +----------+          +----------+       |
|                            |                                     |
|   +----------+         +----------+          +----------+       |
|   | Applica- |         | Applica- |          | Applica- |       |
|   |  tion    |<---[A]--->|  tion    |<---[A]---->|  tion    |       |
|   |Component |         | Service  |          | Interface|       |
|   +----------+         +----------+          +----------+       |
|                            |                                     |
|   +----------+         +----------+          +----------+       |
|   |   Node   |         | Techno-  |          | Artifact |       |
|   |  (Device,|<---[A]--->|  logy    |<---[A]---->|  (File)  |       |
|   |  SystemS)|         | Service  |          |          |       |
|   +----------+         +----------+          +----------+       |
|                                                                    |
|   [A] = Assignment (행위자 ↔ 행동 간 행동 주체/객체 지정)         |
|   계층 간 연결: [Realization] (상위 -> 하위 실현)                 |
|                  [Used By]    (하위 -> 상위 사용)                  |
+------------------------------------------------------------------+
```

### ArchiMate 관계(Relationship) 11종

| 관계 종류 | 표기 | 의미 | 사용 가능 계층 | 예시 |
| :--- | :--- | :--- | :--- | :--- |
| **Composition** | ◆---- | 강한 전체-부분 (합집합) | 모든 계층 | "은행계좌"는 "고객정보"를 합성 |
| **Aggregation** | ◇---- | 약한 전체-부분 (집합) | 모든 계층 | "팀"이 여러 "직원"으로 구성 |
| **Assignment** | -----> | 능동구조가 행동을 책임짐 | 동 계층 내 | "영업사원"이 "영업활동"을 담당 |
| **Realization** | - - -> | 하위 요소가 상위를 실현 | Cross-Layer | "주문시스템"이 "주문서비스" 실현 |
| **Used By** | -----> | 하위 요소가 상위를 사용 | Cross-Layer | "DB"가 "데이터서비스"를 사용 |
| **Serving** | ->---- | 하위 서비스가 상위에 제공 | Cross-Layer | "API"가 "업무서비스"에 제공 |
| **Access** | ---> | 수동구조에 대한 읽기/쓰기 | 동 계층 내 | "결제요청"이 "주문데이터"에 접근 |
| **Influence** | - - -> | 동기 요소 간 정/부정 영향 | Motivation | "GDPR규정"이 "보안목표"에 +영향 |
| **Association** | --- | 기타 약한 의미적 연결 | 모든 계층 | 그룹화, 비정형 관계 |
| **Triggering** | ---> | 시간적/인과적 흐름 | 동 계층 내 | "주문이송"이 "결제처리"를 트리거 |
| **Flow** | ---> | 동적/물리적 흐름 | 동 계층 내 | "데이터"가 "프로세스" 간 흐름 |

### ArchiMate 뷰포인트(Viewpoint) 분류

| 뷰포인트 그룹 | 표준 뷰포인트 수 | 주요 산출 목적 | TOGAF ADM 단계 |
| :--- | :--- | :--- | :--- |
| **Organization** | 5종 | 액터, 역할, 협업 구조 | Phase B (비즈니스) |
| **Business Process** | 3종 | 프로세스, 이벤트, 서비스 흐름 | Phase B |
| **Application Structure** | 6종 | 컴포넌트, 인터페이스, 데이터 | Phase C (정보시스템) |
| **Application Usage** | 4종 | 애플리케이션 협업, 사용성 | Phase C |
| **Infrastructure** | 4종 | 노드, 디바이스, 네트워크, 인프라서비스 | Phase D (기술) |
| **Strategy** | 3종 | 역량, 가치, 자원 | Phase A (아키텍처 비전) |
| **Motivation** | 3종 | 이해관계자, 목표, 원칙 | Requirements Mgmt |
| **Implementation/Migration** | 3종 | 작업패키지, 갭, 마이그레이션 | Phase E~F |
| **Composite** | 3종 | Layered, Service Realization 등 | 전체 |

### 핵심 메커니즘: Cross-Layer Realization Chain

```text
[서비스 실현 사슬 (Service Realization Chain) - ArchiMate 3.1의 핵심]

   +--------------+
   | Business     |   "주문 처리 서비스"
   | Service      |  (고객에게 가치 제공)
   +------+-------+
          | Realization (Dashed)
          v
   +--------------+
   | Business     |   "주문 처리 프로세스"
   | Process      |  (실제 비즈니스 활동)
   +------+-------+
          | Assignment (Solid)
          v
   +--------------+
   | Business     |   "주문 처리 액터"
   | Actor / Role |  (영업사원)
   +--------------+
          | Realization (Cross-Layer)
          v
   +--------------+
   | Application  |   "주문 관리 애플리케이션 컴포넌트"
   | Component    |
   +------+-------+
          | Realization
          v
   +--------------+
   | Application  |   "주문 서비스 (API)"
   | Service      |
   +------+-------+
          | Used By (Cross-Layer)
          v
   +--------------+
   | Technology   |   "WAS, Node, JDBC, SystemSW"
   | Service      |
   +--------------+

   * 위 사슬을 통해 "왜 WAS가 필요한가" 추적:
     비즈니스 목표 -> 주문 서비스 -> 주문 컴포넌트 -> WAS
```

**핵심 알고리즘/원리**:

1. **메타모델 제약(Metamodel Conformance)**: ArchiMate 도구(BiZZdesign Architect, Sparx EA, Archi)는 OCL(Object Constraint Language) 기반의 메타모델 제약을 적용한다. 예를 들어 `Assignment`는 반드시 Active Structure ↔ Behavior 사이에서만 발생하며, `Composition`은 동 계층 내 동일 추상화 레이어(예: Business ↔ Business)에서만 허용된다. **Cross-Layer는 Realization, Used By, Serving만 허용**된다.

2. **뷰(View) 도출 알고리즘**: 도구는 내부적으로 그래프 DB(Neo4j 등) 또는 관계형 DB에 메타모델 인스턴스를 저장하고, 뷰포인트 명세에 따라 노드 타입, 관계 타입, 깊이(Depth), 추상화 레벨 필터링을 적용해 뷰를 추출한다.

3. **동기(Motivation) -> 비즈니스 -> 애플리케이션 -> 기술 인과 추론**: Influence 관계는 부호(+, -)와 가중치(%)를 가져, AHP(Analytic Hierarchy Process) 유사한 영향도 분석이 가능하다. 예: "GDPR 규정(+90%)" -> "개인정보 보호 목표(+80%)" -> "데이터 암호화 요구사항(+100%)" -> "암호화 애플리케이션 서비스" -> "HSM 기술 서비스".

- **📢 섹션 요약 비유**: ArchiMate의 Active-Behavior-Passive 3분류는 마치 **영화 촬영**과 같다. **배우(Active Structure)**가 **대본/행동(Behavior)**을 수행하고, 이 과정에서 **소품·세트(Passive Structure)**가 사용된다. ArchiMate는 이 세 가지를 명시적으로 분리해, "누가(Active) 무엇을(Behavior)
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 414 / 800

<- **이전**: [413. TOGAF ADM 아키텍처 개발 방법론](/knowledge-base/studynote/12_it_management/05_security_compliance/413_togaf_adm_architecture_development_method/)
**다음**: [415. BPM 프로세스 관리 BPMN 모델링](/knowledge-base/studynote/12_it_management/05_security_compliance/415_bpm_process_management_bpmn_modeling/) ->

---
