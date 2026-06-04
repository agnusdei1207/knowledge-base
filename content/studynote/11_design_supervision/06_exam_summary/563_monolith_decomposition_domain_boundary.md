+++
title = "563. 모놀리스 분해 전략 도메인 경계 (Monolith Decomposition Domain Boundary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 모놀리스 분해의 핵심은 코드 분리(Cut)가 아닌 **도메인 경계(Bounded Context)**와 **응집도/결합도(High Cohesion / Low Coupling)**의 식별이며, 이를 위해 DDD의 Strategic Pattern(Subdomain, Context Map, Anti-Corruption Layer)과 **Team Topologies**(Stream-aligned Team)가 결합되어야 한다.
> 2. **가치**: 올바른 도메인 경계로 분리 시 배포 독립성(Independent Deployability) 확보로 **Lead Time 70%v, MTTR 60%v, Change Failure Rate 50%v**(DORA Report 2023 기준) 효과를 얻으며, 마이크로서비스 전환 실패의 주원인인 **Distributed Monolith 회피**가 가능하다.
> 3. **판단 포인트**: "기술 계층(Controller/Service/DAO) 기준"이 아닌 "**비즈니스 능력(Business Capability)**과 **데이터 트랜잭션 경계(Aggregate Root)**" 기준으로 분리하며, 트레이드오프로 (1) 네트워크 비용 vs 자율성, (2) 데이터 일관성(ACID->BASE) vs 성능, (3) 팀 자율성(Conway's Law) vs 거버넌스 복잡도를 동시에 고려해야 한다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 시스템이 성장하면서 Monolithic Architecture(단일 배포 단위)는 **배포 지연(Deployment Bottleneck)**, **확장성 한계(Scalability Ceiling)**, **기술 부채(Technical Debt)**, **팀 생산성 저하(Brooks' Law: n(n-1)/2 통신 경로)** 문제를 야기한다. 마이크로서비스로의 전환은 단순한 기술적 리팩토링이 아닌 **비즈니스 도메인의 재구조화**이며, 잘못된 경계로 분리할 경우 **Distributed Monolith**(분산된 단일체)라는 더 큰 안티패턴을 초래한다.

따라서 "어떻게 쪼갤 것인가(How to split)"보다 "**무엇을 기준으로 쪼갤 것인가(What defines a boundary)**"가 핵심 의사결정이며, 이는 도메인 주도 설계(DDD)의 Bounded Context, Bounded Context 간 관계(Context Map), 그리고 조직 구조(Conway's Law -> Inverse Conway Maneuver)의 관점에서 접근해야 한다.

```text
+-----------------------------------------------------------------------------+
|            Monolith -> Microservices 전환 시 발생하는 실패 패턴 (변형)        |
+-----------------------------------------------------------------------------+

   [기대]                              [현실 - Distributed Monolith]
   +----------+                         +------+  +------+  +------+
   | Service A| --async event--►        | Svc A|--| Svc B|--| Svc C|
   | Service B|                         |  ↕   |  |  ↕   |  |  ↕   |
   | Service C|                         | DB A |  | DB B |  | DB C |
   +----------+                         +------+  +------+  +------+
   독립 배포·독립 스케일                    동기 호출 다수, 공동 배포 필요,
                                          장애 전파(Cascading Failure)

   ★ 실패 원인: 도메인 경계 없이 "기술 계층"만 분리 (Controller/Service/DAO 단위)
```

**Old vs New Paradigm 비교**
- **Old**: "DB 중심 분리" — 하나의 RDBMS 스키마를 모듈별로 나누기 (e.g., Schema per Service) -> 강한 결합 잔존, 분산 트랜잭션 과다 발생
- **New**: "도메인/능력 중심 분리" — Bounded Context별로 자체 DB·자체 API·자체 팀 보유 -> 자율성 극대화, 데이터 중복 허용(Eventual Consistency)

- **📢 섹션 요약 비유**: 모놀리스를 뜯어 고치는 건 마치 **한 덩어리의 떡 케이크**를 자르는 것과 같습니다. 칼질을 아무리 잘해도 **자르는 기준선(도메인 경계)**이 잘못되면, 케이크가 부서지거나(장애) 한 조각을 자르면 옆 조각이 무너집니다(결합). "손님(비즈니스 요구사항)이 누구에게 줄 것인가"가 자르는 기준선이 되어야 합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

도메인 경계 식별은 크게 4단계로 수행된다: (1) **Event Storming**으로 비즈니스 프로세스 도출 -> (2) **Subdomain 분류**(Core/Supporting/Generic) -> (3) **Bounded Context 매핑**(언어적 경계 식별, Ubiquitous Language) -> (4) **Context Map 작성**(BC 간 관계 명시). 이후 **Aggregate Root** 단위로 트랜잭션 일관성 경계를 확정하고, 이를 **Service/API 경계**로 승격한다.

```text
+------------------------------------------------------------------------------+
|        도메인 경계 식별 -> 서비스 분리 4단계 아키텍처 (End-to-End)            |
+------------------------------------------------------------------------------+

  [Stage 1: Event Storming]            [Stage 2: Subdomain 분류]
  +----------------------+            +--------------------------------+
  |  Domain Event 식별    |            |  ● Core Subdomain (경쟁력)     |
  |  +----------------+  |            |    - 추천 알고리즘, 결제 엔진  |
  |  | OrderPlaced    |  |   --►      |  ● Supporting Subdomain        |
  |  | PaymentCompleted|  |            |    - 재고관리, 회원 등급       |
  |  | ItemShipped    |  |            |  ● Generic Subdomain (외주화)  |
  |  +----------------+  |            |    - 알림, 파일저장소, 인증   |
  +----------------------+            +--------------------------------+
            |                                      |
            v                                      v
  [Stage 3: Bounded Context 매핑]     [Stage 4: Context Map]
  +----------------------+            +--------------------------------+
  | 같은 단어, 다른 의미! |            |  [Order] --Customer/Supplier--►|
  |  "Product" in Sales  |            |  [Order] --Conformist---------►|
  |   = 가격·프로모션 중심|            |  [Pay]   ◄--ACL--------[Legacy]|
  |  "Product" in Stock  |            |  [User]  --Shared Kernel------►|
  |   = SKU·재고·창고 중심|            +--------------------------------+
  +----------------------+
            |
            v
  [Stage 5: Aggregate & Service 경계 확정]
  +------------------------------------------------------------------+
  |  Order Aggregate (Root: Order)                                   |
  |   +- OrderItem                                                  |
  |   +- ShippingInfo                                               |
  |   +- Payment (별도 Aggregate - ID 참조만, 강한 일관성 X)        |
  |                                                                  |
  |  트랜잭션 경계 = Aggregate 경계                                  |
  |  서비스 경계 = 1개 또는 n개의 Aggregate를 포함하는 BC             |
  +------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Bounded Context (BC)** | 동일 모델이 일관되게 적용되는 언어적·모델적 경계. 한 BC 안에서는 **Ubiquitous Language**가 단일하게 유지됨 | 예: `Catalog BC`의 "Product"(price·desc)와 `Inventory BC`의 "Product"(SKU·stockQty)는 별도 모델로 취급. 구현 시 **Maven/Gradle 모듈**, **별도 패키지 root**, **별도 Schema/DB**로 격리 |
| **Aggregate** | 트랜잭션 일관성(ACID)의 단위. **Aggregate Root**만이 외부에서 참조 가능 | ID 참조(다른 Aggregate는 ID만 보유) + Domain Event 발행(`OrderConfirmed`, `PaymentCompleted`). Spring: `@DomainEvents`, Axon: `AggregateLifecycle.apply()` |
| **Context Map** | BC 간 통합 패턴(Relationship)을 명시. 9가지 패턴 사용 | **Customer-Supplier**, **Conformist**, **Anti-Corruption Layer(ACL)**, **Shared Kernel**, **Open Host Service(OHS)**, **Published Language(PL)** 등. ACL 구현: Adapter/Translator Layer, Kafka Consumer + DTO 변환 |
| **Subdomain** | 비즈니스 문제 공간(Problem Space)의 분할. 조직의 실제 경쟁력·전략 반영 | **Core**(자체 개발, 고투입), **Supporting**(자체 개발, 중투입), **Generic**(패키지/SaaS 활용, 저투입) — **Core Domain에 개발자 집중 배치** |
| **팀 토폴로지(Team Topologies)** | BC 경계 = 팀 경계로 매핑 (Conway's Law 역이용) | **Stream-aligned Team**(BC 1~2개 전담), **Platform Team**(내부 플랫폼 제공), **Enabling Team**(기술 코칭), **Complicated Subsystem Team**(Core Domain 전담) |

**핵심 식별 휴리스틱 (Heuristics for Boundary Discovery)**
1. **언어적 경계(Linguistic Boundary)**: 동일 용어가 다른 의미로 쓰이는 지점 = BC 분리 신호
2. **데이터 소유권(Data Ownership)**: "누가 이 데이터를 수정하는 유일한 권한을 가져야 하는가?" -> 그 팀/BC가 Owner
3. **트랜잭션 빈도/결합도 분석**: 같은 트랜잭션에 자주 함께 묶이는 Entity -> 같은 Aggregate, 함께 묶이지 않으면 분리
4. **변경 빈도(Volatility)**: 함께 자주 변경되는 코드 = 같은 BC
5. **성능/확장 요구 차이**: 트래픽 패턴이 다른 컴포넌트(예: 결제 vs 상품조회) -> 분리 우선 후보
6. **Neuron Boundary (Eberhard Wolff)**: 비즈니스 객체의 **불변식(Invariant)**이 어디까지 유지되는가 = 경계

- **📢 섹션 요약 비유**: 도메인 경계 찾기는 **학교에서 학과 나누기**와 같습니다. "학생"이라는 단어가 있어도 **경영학과 학생**과 **컴퓨터학과 학생**이 배우는 내용(언어·모델)이 다르듯, "Product"라는 단어도 **영업팀의 Product**와 **물류팀의 Product**는 다루는 속성이 다릅니다. 같은 강의를 듣지 않는 학생들을 같은 과에 묶어두면, 한 명만 전과하고 싶어도 전체가 흔들립니다.

---

## Ⅲ. 비교 및 연결

| 구분 | **기능 계층 분리 (Technical Layer Split)** | **도메인 경계 분리 (BC-based Split)** | **데이터베이스 스키마 분리 (Schema-per-Service)** |
| :--- | :--- | :--- | :--- |
| **분리 기준** | Controller / Service / Repository 계층 | 비즈니스 능력(Business Capability)·Ubiquitous Language | 테이블/스키마 단위 |
| **결합도** | 높음 (여전히 동일 도메인 로직 공유) | 낮음 (BC 간 ACL/이벤트로만 통신) | 중간 (스키마는 분리되어도 로직 결합 잔존) |
| **데이터 일관성** | 단일 DB로 강제 가능 (모놀식 ACID) | BC별 독립 DB, **Saga/Eventual Consistency** 필수 | DB 내부는 ACID, BC 간은 분산 트랜잭션 |
| **배포 독립성** | 낮음 (전체 또는 큰 단위로 배포) | **높음 (각 BC가 독립 빌드·배포)** | 낮음 (서비스 간 의존성 큼) |
| **조직 영향** | 기존 팀 구조 유지 | **Team Topologies 재편 필요** (Conway's Law) | DB 분할만 수행, 조직 변화 미미 |
| **적합 시나리오** | Legacy 최소 분리, 단계적 Strangler Fig 초기 단계 | **MSA 본 목적 달성**, 진정한 자율적 팀 | DB 종속성이 강한 시스템의 과도기 |
| **실패 위험** | Distributed Monolith 가능성 높음 | 초기에 분석 비용 큼, Event Storming 필요 | 분산 트랜잭션 과다, 2PC 성능 저하 |

**연계 기술 및 패턴**
- **Bounded Context ↔ Service Mesh (Istio/Linkerd)**: BC 단위 Service Mesh 구성으로 mTLS·트래픽 제어·관찰 가능
- **Bounded Context ↔ Data Mesh**: BC가 데이터의 **Domain Owner**가 되어 Data Product 발행 (Zalando, Intuit 사례)
- **Aggregate ↔ Event Sourcing (Axon, EventStoreDB)**: Aggregate의 모든 상태 변경을 Domain Event로 저장 -> BC 간 비동기 통합 단순화
- **Context Map ↔ API Gateway / BFF**: OHS(Open Host Service) 패턴을 API Gateway로 구현, 각 BFF가 특정 BC에 맞춤 API 제공
- **Strangler Fig Pattern (Martin Fowler)**: 기존 모놀리스의 트래픽을 점진적으로 새 BC로 라우팅(API Gateway 기반), 위험 최소화

- **📢 섹션 요약 비유**: "기능 계층 분리"는 마치 **아파트 단지에서 1층은 주방, 2층은 거실, 3층은 침실**로 나누는 것과 같습니다(층별 분리). 사는 사람(도메인)은 계속 같이 다니며 함께 밥을 먹고 자야 하니 결국 분리 효과가 없습니다. 반면 "도메인 경계 분리"는 **각 가족(비즈니스 능력)이 자기 집(서비스)을 가져 요리·취침을 독립적으로 하는 것**입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **Event Storming을 수행했는가?** — 도메인 전문가(DA·BA·Product Owner)와 개발자가 함께 **Domain Event**, **Command**, **Aggregate**, **Policy(반응 규칙)**를 화이트보드에 도출했는지. 산출물: Event Map, BC 후보 리스트, Subdomain 분류표
2. **Bounded Context 간 통합 패턴(Context Map)을 명시했는가?** — 모든 BC 쌍에 대해 **Customer-Supplier / Conformist / ACL / Shared Kernel / OHS / PL / Partnership / Separate Ways** 중 하나를 의도적으로 선택했는지. 미정의 = 암묵적 Conformist -> 향후 Legacy 오염
3. **Aggregate 경계에서 트랜잭션 일관성을 검증했는가?** — "어떤 불변식(Invariant)이 같은 트랜잭션 안에서 강제되어야 하는가?" 기준. 예: "주문 총액 = 주문 항목 합계" -> 같은 Aggregate. "주문-결제"는 다른 Aggregate -> Saga
4. **팀 토폴로지와 BC가 1:1(또는 1:N 허용)로 매핑되는가?** — **Cognitive Load** 1팀당 BC 1~2개 권장(Team Topologies). 1팀이 5개 BC 담당 = 모놀식 사고 잔존. 팀 경계와 BC 불일치 시 Conways's Law에 의해 코드가 다시 결합됨
5. **분리 우선순위(Migration Roadmap)가 데이터에 기반하는가?** — **"Impact × Isolation × Strangler-readiness"** 점수화. 보통 (1) Generic -> (2) Supporting -> (3) Core 순서. Core는 가장 마지막에 분리(또는 분리하지 않을 수도 있음 — Modular Monolith 유지)

### 피해야 할 안티패턴

- **Distributed Monolith (분산된 단일체)**: 동기 HTTP 호출 체인(A->B->C), DB 직접 조회, 통합 배포 필요. "모놀리스의 모든 단점을 가지면서 운영 복잡성만 더한 시스템"
- **Entity Service / Anemic Microservice**: Aggregate 전체가 아닌 Entity 1개당 서비스 1개. 트랜잭션·통신 비용 폭증
- **Shared Kernel 과다 사용**: 여러 BC가 동일 라이브러리/테이블 공유 -> 배포 시 동기화 필요, BC 의미 소실. **공유는 면적당 ≤ 1~2개 BC로 제한**
- **기술 계층 기준 분리**: "Controller 마이크로서비스"식 분리 -> 진정한 비즈니스 자율성 부재
- **무분별
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 563 / 600

<- **이전**: [562. 아키텍처 패턴 레이어드 이벤트 파이프](/knowledge-base/studynote/11_design_supervision/06_exam_summary/563_architecture_pattern_layered_event_pipe/)
**다음**: [564. API 설계 RESTful GraphQL gRPC](/knowledge-base/studynote/11_design_supervision/06_exam_summary/564_api_design_restful_graphql_grpc/) ->

---
