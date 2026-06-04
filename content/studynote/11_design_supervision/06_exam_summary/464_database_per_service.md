+++
title = "464. 데이터베이스 퍼 서비스 독립 저장소 (Database per Service Independent Storage)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 마이크로서비스 아키텍처(MSA)에서 각 마이크로서비스가 **자신만의 전용 데이터 저장소(Database per Service)를 단독 소유**하여, 다른 서비스의 DB에는 직접 접근할 수 없도록 격리하는 패턴으로, **데이터 캡슐화(Data Encapsulation)**, **서비스 자율성(Autonomy)**, **폴리글랏 영속성(Polyglot Persistence)**을 보장하는 핵심 아키텍처 스타일이다.
> 2. **가치**: 서비스 간 **강결합(Tight Coupling)을 제거**하여 배포 독립성·장애 격리·기술 다양성을 확보하며, Netflix·Amazon·Uber 등 대규모 MSA 환경에서 **수천 개 서비스 단위로 수평 확장**을 가능하게 한다. 구체적으로 배포 빈도 200%^, 장애 도메인 격리로 MTTR 60%v, 팀당 자율성 확보로 개발 생산성 30~50% 향상이 보고된다.
> 3. **판단 포인트**: **분산 트랜잭션(2PC) 회피**로 인한 정합성 트레이드오프(CAP의 AP vs CP), **조회 조인(Join) 불가**로 인한 비정규화·CQRS·Saga·Outbox 도입 여부, **데이터 중복 허용 범위**, 그리고 **운영 복잡도(다수 DB 인스턴스 관리·모니터링·백업·DR)** 사이의 균형점이 핵심 의사결정 변수이다.

---

## Ⅰ. 개요 및 필요성

모놀리식 아키텍처에서는 단일 RDBMS(예: Oracle, MySQL)에 모든 도메인 데이터(회원·주문·결제·재고)가 통합되어 저장되고, 애플리케이션 모듈 간에는 동일한 트랜잭션 컨텍스트 안에서 자유롭게 JOIN·FK 참조가 가능했다. 그러나 클라우드 네이티브 시대에 들어 **수백~수천 개의 배포 단위**, **데브옵스(DevOps) 자율 배포**, **무중단 스케일링** 요구사항이 폭증하면서, 다음 세 가지 근본 문제가 대두되었다.

1. **DB 병목**: 단일 RDB에 모든 서비스 트래픽이 집중되어 Connection Pool 고갈·Lock 경합 발생
2. **스키마 결합(Schema Coupling)**: 한 서비스의 컬럼 변경이 동일 DB를 공유하는 다른 서비스 빌드를 깨뜨림
3. **확장성의 비대칭성**: CPU·I/O 집약 서비스(주문·검색)와 경량 서비스(알림)는 스케일링 요구가 다른데, 단일 DB로는 세밀한 분리가 불가능

Database per Service 패턴은 **Chris Richardson**이 저서 *Microservices Patterns*(2018)에서 체계적으로 정립한 패턴으로, **"서비스는 데이터를 다른 서비스의 데이터와 공유하지 않고, 각 서비스가 자신의 데이터를 비공개로 유지한다"**는 원칙에 기반한다. 이를 통해 **Bounded Context**(도메인 주도 설계, Eric Evans 2003) 경계가 데이터 계층까지 강제되며, 진정한 의미의 **느슨한 결합(Loose Coupling)**이 달성된다.

```text
[ Monolithic DB vs Database per Service ]

   +------ Monolithic (Single Shared DB) ------+
   |                                            |
   |  +--------+  +--------+  +--------+        |
   |  |회원Svc |  |주문Svc |  |결제Svc |        |
   |  +---+----+  +---+----+  +---+----+        |
   |      | JOIN/FK  | JOIN/FK  |              |
   |      v          v          v              |
   |  +------------------------------+          |
   |  |  Shared RDBMS (Single Schema)|          |
   |  |  USER -- ORDER -- PAYMENT    |          |
   |  +------------------------------+          |
   +--------------------------------------------+
   ⚠ 스키마 변경이 전체 빌드 폭주, 단일 장애점,
     Lock 경합, Connection Pool 고갈

   -----------------------------------------------

   +------ Database per Service (MSA) ----------+
   |                                            |
   |  +--------+    +--------+    +--------+    |
   |  |회원Svc |    |주문Svc |    |결제Svc |    |
   |  |  (API) |    |  (API) |    |  (API) |    |
   |  +---+----+    +---+----+    +---+----+    |
   |      |  REST/gRPC  |  REST/gRPC |  Event   |
   |      v             v            v          |
   |  +--------+    +--------+    +--------+    |
   |  |Postgres|    |MongoDB |    |Cassandra|   |
   |  | (회원) |    | (주문) |    | (결제로그)|  |
   |  +--------+    +--------+    +--------+    |
   |   독립 스키마     비정규화    Wide-Column   |
   |   트랜잭션 격리   Polyglot Persistence     |
   +--------------------------------------------+
   ✅ 독립 배포, 폴리글랏, 장애 격리, 자율 스케일
```

기존 패러다임은 **"데이터 중복은 최소화(3정규화)하고, 무결성을 DB가 보장"**이었지만, MSA 시대에는 **"서비스는 자신의 데이터를 자율적으로 관리하고, 다른 서비스에는 API·이벤트만 노출"**으로 대전환된다. 이는 2000년대 SOA(Service-Oriented Architecture)에서도 부분적으로 시도되었으나, ESB(Enterprise Service Bus) 중앙화·공유 XML 스키마로 인해 결합이 재발했다. Database per Service는 ESB의 실패를 학습하여 **분산 이벤트 기반(EDA) + 비공유 데이터(Shared-Nothing)** 원칙을 극단까지 밀어붙인 형태이다.

- **📢 섹션 요약 비유**: 가족이 함께 쓰던 **공용 냉장고**(모놀리식 DB)에서는 누가 뭐 꺼갔는지 추적하기 힘들고, 냉장고가 고장나면 가족 전체가 굶게 됩니다. **Database per Service**는 각 가족 구성원에게 **개인 미니냉장고**를 지급하여, 내가 먹을 건 내가 사고·관리하되, 필요한 식재료는 **문서(API)나 가족 단톡방(이벤트)**을 통해 공유하는 것과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Database per Service 패턴은 단순히 "DB를 쪼갠다"가 아니라, **데이터 접근의 모든 경로**(CRUD·조회·이벤트 발행·트랜잭션 조정)를 **서비스 경계 너머로 강제**하는 아키텍처 원칙이다. 핵심 메커니즘은 다음 4단계 흐름으로 작동한다.

```text
[ Database per Service 아키텍처 & 데이터 흐름 ]

   +----------------------------------------------------+
   |                   API Gateway / BFF                 |
   |  (Kong, Spring Cloud Gateway, AWS API Gateway)      |
   +------+----------+----------+----------+------------+
          |          |          |          |
          v          v          v          v
   +----------+ +----------+ +----------+ +----------+
   | User Svc | |Order Svc | |Payment  | |Inventory |
   |  (Java)  | |  (Node)  | |  Svc    | |  Svc     |
   |          | |          | | (Go)    | | (Python) |
   | +------+ | | +------+ | | +------+ | | +------+ |
   | |JPA   | | | |Mongoid| | | |GORM  | | | |SQLAlc | |
   | +--+---+ | | +--+---+ | | +--+---+ | | +--+---+ |
   |    | X   | |    | X   | |    | X   | |    | X   |
   +----+-----+ +----+-----+ +----+-----+ +----+-----+
        |            |            |            |
        v            v            v            v
   +----------+ +----------+ +----------+ +----------+
   |PostgreSQL| |  MongoDB | |  MySQL   | |  Redis   |
   |  16.x    | |   7.x    | |   8.0    | |  Cluster |
   | (RDB)    | |(Document)| | (RDB)    | | (Cache)  |
   +----------+ +----------+ +----------+ +----------+
        |            |            |            |
        |            |            |            |
        +-----► Kafka / Pulsar / RabbitMQ ◄----+
              (Event Backbone: outbox + CDC)
              +----------------------------+
              |  Event Topics:             |
              |  • user.created            |
              |  • order.placed            |
              |  • payment.completed       |
              |  • inventory.reserved      |
              +----------------------------+
                        |
              +---------+---------+
              v                   v
         [Eventual          [Read Model
         Consistency]       (CQRS Query DB)]
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **서비스 (Service)** | 비즈니스 로직 캡슐화, 트랜잭션 경계 정의 | Java/Spring Boot, Node.js/NestJS, Go/Kratos, Python/FastAPI 등 **언어/프레임워크 자유 선택**(Polyglot Programming) |
| **Private DB (사유 DB)** | 서비스가 **유일하게 SELECT/INSERT/UPDATE/DELETE 권한**을 보유 | PostgreSQL(MySQL/MariaDB)·MongoDB·Cassandra·DynamoDB·Redis·ClickHouse 등 **데이터 모델에 따라 자유 선택**(Polyglot Persistence) |
| **API Contract** | 서비스 간 데이터 공유의 **유일한 공식 통로** | REST/OpenAPI 3.1, **gRPC + Protocol Buffers v3**(고성능 내부 통신), GraphQL(BFF/클라이언트 조회) |
| **Event Backbone** | 비동기 데이터 전파 및 **최종 일관성(Eventual Consistency)** 달성 | **Apache Kafka**(Partition·Exactly-Once Semantics), RabbitMQ, Apache Pulsar, NATS JetStream |
| **Outbox Pattern** | DB 트랜잭션과 이벤트 발행의 **원자성 보장** | 같은 DB 트랜잭션 내에서 `outbox` 테이블에 이벤트 레코드 INSERT -> Debezium CDC로 캡처하여 Kafka 발행 |
| **Saga Orchestrator** | 서비스 간 분산 트랜잭션 조율 | **Orchestration Saga**(Camunda, Temporal, Axon) 또는 **Choreography Saga**(이벤트 체인) |
| **Data API Gateway** | 클라이언트 측 다중 서비스 조회 합성 | GraphQL Federation(Apollo Router), BFF Pattern(Backend for Frontend) |

### 핵심 원리 심층 분석

**① 데이터 사유화(Encapsulation) 강제**
서비스 외부에서 DB에 직접 접속하는 행위는 **아키텍처 위반**이다. 이를 기술적으로 차단하기 위해 (a) DB 사용자 계정을 서비스별로 분리하고 GRANT를 `current_schema`로 한정, (b) Private Subnet에 DB를 배치하여 서비스 VPC/Pod 내부 IP만 라우팅 허용, (c) Schema Registry + DB 방화벽(예: AWS RDS Security Group, GCP Cloud SQL Authorized Networks) 이중 잠금이 권장된다.

**② 트랜잭션 경계의 재정의**
기존 단일 RDB의 ACID 트랜잭션은 **BASE(Basic Availability, Soft state, Eventual consistency)** 로 대체된다. Saga Pattern은 N단계 작업을 **N개의 로컬 트랜잭션**으로 분해하고, 실패 시 **보상 트랜잭션(Compensating Transaction)** 으로 롤백한다. 예: `주문 생성 -> 결제 -> 재고 차감` 중 결제 실패 시 -> `주문 취소(자동) + 재고 원복(자동)`.

**③ 폴리글랏 영속성(Polyglot Persistence)**
- 회원 프로필: PostgreSQL(트랜잭션·정합성 중요)
- 상품 카탈로그: MongoDB(스키마 유연성, 다양한 속성)
- 결제 원장: Cassandra / CockroachDB(쓰기 집약·다중 리전 복제)
- 세션/캐시: Redis Cluster(저지연 Key-Value)
- 검색/로그: Elasticsearch / OpenSearch(전문 검색·분석)
- 시계열 메트릭: InfluxDB / TimescaleDB / Prometheus TSDB

각 DB는 **해당 서비스의 트래픽 특성·정합성 요구·쿼리 패턴**에 맞춰 독립 튜닝·확장된다.

**④ 데이터 일관성 전략 (3가지 선택지)**
1. **Choreography Saga**: 서비스가 이벤트를 발행·구독하여 자율적으로 다음 단계 진행 (단순·결합 낮음·흐름 추적 어려움)
2. **Orchestration Saga**: 중앙 Orchestrator(Temporal·Camunda)가 단계별 호출·실패 보상 관리 (가시성·제어 용이·Orchestrator SPOF 위험)
3. **Outbox + CDC + Event Sourcing**: 서비스 DB의 `outbox` 테이블을 Debezium이 tail하여 Kafka로 발행, 다운스트림 서비스는 Read Model(CQRS)을 갱신 (강력한 신뢰성·Replay 가능)

**⑤ 조회(Read) 처리의 한계와 대응**
서비스 간 JOIN이 금지되므로, **집계(aggregation) 조회**는 다음 중 선택한다:
- **API Composition**: 클라이언트 또는 API Gateway가 여러 서비스 API를 호출 후 합성
- **CQRS(Command Query Responsibility Segregation)**: Query 전용 Read DB(예: MySQL->Elasticsearch 동기화) 유지
- **Event-Driven Projection**: Kafka 스트림을 KSQL/ksqlDB·Apache Flink로 변환하여 Read Model 생성

- **📢 섹션 요약 비유**: Database per Service는 **각 가게의 금고**가 각자 다른 곳에 있고, **현금 흐름은 봉투(API)나 라디오 신호(이벤트)**로만 전달되는 **복합 상점가**와 같습니다. 주인이 직접 금고를 관리(Polyglot)하고, 거래 내역은 라디오로 모두에게 알려지며(Event), 큰 거래는 가게 간 **에스크로(Saga Orchestrator)**가 중재합니다.

---

## Ⅲ. 비교 및 연결

Database per Service는 MSA 데이터 관리의 3대 대표 패턴 중 하나이며, **Shared Database**·**Saga + 이벤트**·**CQRS** 등 다양한 패턴과 결합 또는 대체 관계에 있다.

| 구분 | **Shared Database (공유 DB)** | **Database per Service** | **Event Sourcing + CQRS** |
| :--- | :--- | :--- | :--- |
| **데이터 소유권** | 모든 서비스가 동일 DB 스키마 공유 | 각 서비스가 자기 DB만 접근 | 서비스가 **이벤트 로그**만 진실의 원천(SoT) |
| **결합도** | 스키마·트랜잭션 **강결합** | 데이터 계층 **완전 격리** | 이벤트 **느슨 결합** |
| **트랜잭션** | 단일 ACID 트랜잭션 | Saga + 보상 트랜잭션 (BASE) | 이벤트 Append-Only, Replay |
| **조회** | 자유로운 JOIN·SQL | JOIN 불가, API 합성 또는 CQRS | **Projection View**로 비정규화 조회 |
| **기술 다형성** | 단일 RDBMS 강제 | Polyglot Persistence (DB 종류 자유) | Event Store(Axon·EventStoreDB) + Read DB 다양 |
| **적합 환경** | 소규모 모놀리식, 트랜잭션 필수 도메인 | **중·
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 464 / 600

<- **이전**: [463. 아웃박스 패턴 메시지 보장](/knowledge-base/studynote/11_design_supervision/06_exam_summary/464_outbox_pattern/)
**다음**: [465. 분산 추적 상관 관계 ID 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/465_distributed_tracing/) ->

---
