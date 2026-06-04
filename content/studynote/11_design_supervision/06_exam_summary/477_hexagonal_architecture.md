---
title: "477. 헥사고날 아키텍처 포트 어댑터 (Hexagonal Architecture Port Adapter)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 헥사고날 아키텍처(Ports & Adapters)는 알리스테어 콕번(Alistair Cockburn, 2005)이 제안한 패턴으로, 애플리케이션 코어(도메인 + 유스케이스)를 외부 인프라(UI, DB, 메시징, 외부 API)로부터 **포트(인터페이스)**와 **어댑터(구현체)**를 통해 양방향 격리하여, **의존성 역전 원칙(DIP)** 하에서 기술 교체·테스트·배포 독립성을 보장하는 아키텍처 스타일이다.
> 2. **가치**: 동일 도메인 코어로 REST·gRPC·CLI 등 다수 진입점을 동시 운영 가능(Omni-channel), 외부 시스템 교체 시 어댑터만 교체(예: JPA->R2DBC, Kafka->RabbitMQ), 테스트 시 in-memory stub으로 단위 테스트 속도 5~10배 향상, 도메인 순수성 확보로 장기 유지보수 비용 30~60% 절감 효과를 제공한다.
> 3. **판단 포인트**: 모든 도메인에 무조건 적용 시 **오버엔지니어링(Over-engineering)** 발생, 포트 경계 정의의 granularity(UseCase 단위 vs Aggregate 단위)에 따라 복잡도 폭증, 비동기 이벤트 어댑터의 멱등성·트랜잭션 보상·스키마 진화 전략, 그리고 마이크로서비스 분할 시 헥사고날이 도메인 경계(bounded context) 안에서만 의미 있다는 점을 명확히 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 문제의 기원: 전통 계층형 아키텍처의 한계

2000년대 초반 주류였던 **3계층(3-tier) 아키텍처**(Presentation -> Business -> Data Access)는 `Service` 클래스가 `JdbcTemplate`, `Hibernate Session`, `HttpServletRequest` 같은 인프라 API에 직접 결합되어, **데이터베이스 변경·UI 교체·테스트 환경 전환** 시 도메인 코드까지 수정해야 하는 **침투적 결합(invasive coupling)** 문제를 야기했다.

예를 들어, 다음 코드는 `OrderService`라는 도메인이 JDBC, Servlet, Spring 트랜잭션 매니저에 동시에 의존하는 전형적인 안티패턴이다.

```java
// 안티패턴: 도메인이 인프라에 결합
@Service
public class OrderService {
    @Autowired private JdbcTemplate jdbc;        // 인프라
    @Autowired private HttpServletRequest req;   // 인프라
    public void placeOrder() {
        String user = req.getParameter("user");  // 웹 의존
        jdbc.update("INSERT INTO orders ...");    // SQL 의존
    }
}
```

이로 인해 (1) 단위 테스트 시 반드시 Tomcat+H2 구동 필요, (2) Kafka로 메시지를 받으려면 Service 재작성, (3) MySQL->PostgreSQL 변경 시 DAO 전체 재작성 같은 **변경 비용 폭증**이 발생했다.

### 1.2 헥사고날의 등장 동기와 핵심 문제 정의

콕번은 *"The goal is to isolate the application from the outside world, so that the application can be plugged into different environments without changing it"* 라고 정의하며, **외부 환경의 변동성(Volatility)** 으로부터 도메인을 보호하는 것을 1차 목표로 삼았다. 이로부터 도출된 핵심 문제는 다음과 같다.

| # | 문제(Problem) | 비기능 요구사항 |
|:--|:--|:--|
| P1 | 외부 액터(사람·시스템·테스트)의 종류가 다양하고 변화가 빠르다 | 진입점 다변성(Omni-channel) |
| P2 | 데이터 저장소·메시징 기술이 3~5년 주기로 교체된다 | 기술 중립성(Technology neutrality) |
| P3 | 도메인 단위 테스트 시 인프라 구동 비용이 크다 | 테스트 가능성(Testability) |
| P4 | 동일 비즈니스 규칙을 다중 채널에 중복 구현하면 규칙이 분기된다 | 단일 진실 공급원(SSoT) |
| P5 | 외부 API 스펙 변동이 도메인에 전파된다 | 격리(Isolation) |

### 1.3 헥사고날 구조의 시각화

```text
                         헥사고날 아키텍처 (Ports & Adapters)
                         ---------------------------------

                          [ Driving Adapters (Inbound) ]
                          +--------------+  +--------------+
                          |  REST        |  |   gRPC       |
                          | Controller   |  |  ServerStub  |
                          | (Spring MVC) |  |  (GrpcJava)  |
                          +------+-------+  +------+-------+
                                 |  HTTP/JSON        |  Protobuf
                                 |                   |
                       +---------v-------------------v----------+
                       |         Inbound Ports (UseCase I/F)    |
                       |  +----------------------------------+  |
                       |  |  PlaceOrderUseCase               |  |
                       |  |  GetOrderUseCase                 |  |
                       |  |  CancelOrderUseCase              |  |
                       |  +----------------------------------+  |
                       |              ^                         |
                       |              | 호출 (Driving)          |
                       |  +-----------+----------------------+  |
                       |  |   Application Service Layer      |  |
                       |  |   (트랜잭션·보안·오케스트레이션)  |  |
                       |  +-----------+----------------------+  |
                       |              | 호출                    |
                       |  +-----------v----------------------+  |
                       |  |   Domain Model (순수 POJO)       |  |
                       |  |   Order, OrderLine, Money        |  |
                       |  |   Domain Event, Aggregate Root   |  |
                       |  +-----------+----------------------+  |
                       |              | 호출                    |
                       |  +-----------v----------------------+  |
                       |  |   Outbound Ports (SPI I/F)       |  |
                       |  |  LoadOrderPort / SaveOrderPort   |  |
                       |  |  PublishEventPort / PayPort      |  |
                       |  +----------------------------------+  |
                       |              ^                         |
                       |              | 구현 제공               |
                       +------+-------+--------+---------------+
                              |                |
                +-------------v-+  +-----------v--------+  +----v----------+
                | JPA Adapter   |  |  Kafka Producer    |  | Toss Payments  |
                | (Hibernate)   |  |  (Spring Kafka)    |  | HTTP Adapter   |
                +---------------+  +--------------------+  +----------------+
                          [ Driven Adapters (Outbound) ]
```

### 1.4 패러다임 전환: 계층형 -> 헥사고날

```text
   [Legacy Layered]                       [Hexagonal]
   +-------------+  <- DB/SQL 누수         +-------------+
   | Controller  |                        | Driving     |
   +-------------+                        | Adapters    |
   | Service ⚠   |  <- 인프라+도메인 혼재    +-------------+
   +-------------+                        | Inbound Port|  <- 기술 중립
   | Repository  |  <- JPA 누수            +-------------+
   +-------------+                        |  Domain     |  <- 순수 도메인
   |   DB        |                        +-------------+
   +-------------+  <- 단방향 침투          | Outbound    |
                                          |  Port       |  <- 인터페이스
                                          +-------------+
                                          | Driven      |
                                          | Adapters    |  <- 교체 가능
                                          +-------------+
```

핵심 차이는 **의존 방향**이다. 계층형은 *상위->하위*로 흐르며 하위 모듈이 상위에 누수되고, 헥사고날은 *어댑터->포트(인터페이스)* 방향이며 **포트 자체가 도메인 영역에 위치**한다. 이것이 OCP(Open-Closed Principle)와 DIP의 실체적 구현이다.

- **📢 섹션 요약 비유**: 헥사고날은 도메인 코어가 "**방탄 조끼**"를 입고, 외부 기술들은 "**호환 어댑터(돼지코/HDMI)**"처럼 쉽게 끼웠다 뺐다 하는 **보급형 충전 케이스** 구조와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 핵심 구성요소와 정적/동적 책임

헥사고날은 5개 계층(또는 동심원)으로 분해되며, 각 계층의 책임은 다음 표와 같다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 | 코드 예시 (Java/Spring) |
|:--|:--|:--|:--|
| **Driving Adapter (Primary/Active)** | 외부 액터 요청을 받아 **Inbound Port(UseCase)** 호출 | Spring MVC `@RestController`, gRPC `@GrpcService`, Kafka `@KafkaListener`, CLI `picocli`, WebSocket `WebSocketHandler` | `@RestController class OrderController { OrderFacade facade; }` |
| **Inbound Port (UseCase Interface)** | 도메인이 외부에 노출하는 **유스케이스 계약**, **Application Layer**에 위치 | `interface PlaceOrderUseCase { OrderId execute(PlaceOrderCommand cmd); }` | Java interface, Kotlin fun interface, TypeScript interface |
| **Application Service (UseCase Impl)** | 트랜잭션 경계, 보안 체크, 도메인 객체 협력 조율, `@Transactional`, `@DomainEvents` 발행 | Spring `@Service`, `@Transactional`, `ApplicationEventPublisher` | `@Service class PlaceOrderService implements PlaceOrderUseCase` |
| **Domain Model** | 엔터티·값 객체·도메인 서비스·도메인 이벤트·집합 루트, **순수 POJO**(Framework 무관) | JPA Entity는 *별도*이며, 도메인은 JPA 어노테이션 없음 | `class Order { fun place(...): OrderPlaced {...} }` |
| **Outbound Port (Repository/SPI Interface)** | 도메인이 필요로 하는 외부 자원 **계약(추상)**, 도메인 영역에 위치 | `interface OrderRepository { Optional<Order> findById(OrderId); void save(Order); }` | Spring Data는 *구현체*에 한정, 도메인은 인터페이스만 의존 |
| **Driven Adapter (Secondary/Passive)** | Outbound Port의 **기술 구현체**, 외부 라이브러리 캡슐화 | `OrderJpaRepository implements OrderRepository` (Hibernate), `OrderDynamoDbAdapter`, `KafkaOrderEventPublisher implements DomainEventPublisher` | `@Repository class OrderJpaRepository implements OrderRepository` |
| **Composition Root** | 모든 빈 와이어링, **main() 또는 @Configuration** | Spring `@SpringBootApplication`, Micronaut `BeanContext`, Quarkus CDI | `@Bean UseCase orderFacade(Repo, Pub){...}` |

### 2.2 의존성 흐름과 패키지 구조

헥사고날의 정적/동적 의존성은 **단방향(Single Direction)** 이다.

```text
[Driving Adapter]   --->  [Inbound Port]   --->  [Application Service]
                                                      |
                                                      v
                                                [Domain Model]
                                                      |
                                                      ^
                                                      | (DIP: 인터페이스 통해 호출)
                                                      |
[Driven Adapter]    --->  [Outbound Port]   <----------+
       |
       v
   (JPA / Kafka / 외부API)
```

**컴파일 시점 의존성**: Adapter -> Port (Interface) -> Domain
**런타임 제어 흐름**: Adapter -> Application Service -> Domain -> Port (구현체 호출)

Maven/Gradle 모듈 구조 예시는 다음과 같다.

```
order-service/
+-- order-domain/         (순수 도메인, 외부 라이브러리 0개)
|   +-- model/            (Order, OrderLine, Money)
|   +-- port/in/          (PlaceOrderUseCase)
|   +-- port/out/         (OrderRepository, EventPublisher)
|   +-- event/            (OrderPlaced)
+-- order-application/    (UseCase 구현, spring-tx 의존)
|   +-- service/          (PlaceOrderService)
+-- order-adapter-in/     (inbound 어댑터)
|   +-- web/              (REST, gRPC)
|   +-- messaging/        (Kafka consumer)
+-- order-adapter-out/    (outbound 어댑터)
    +-- persistence-jpa/  (Hibernate)
    +-- persistence-mongo/ (Mongo)
    +-- messaging-kafka/  (Kafka producer)
```

이 모듈 분리는 *아키텍처 테스트(ArchUnit)* 로 강제할 수 있다.

```java
@AnalyzeClasses(packages = "com.example.order")
public class HexagonalArchitectureTest {
    @ArchTest
    static final ArchRule domain_should_not_depend_on_adapters =
        noClasses().that().resideInAPackage("..domain..")
            .should().dependOnClassesThat().resideInAPackage("..adapter..");

    @ArchTest
    static final ArchRule ports_are_interfaces =
        classes().that().resideInAPackage("..port.out..")
            .should().beInterfaces();
}
```

### 2.3 Inbound / Outbound Port의 의미적 구분

헥사고날에서 "Driving"과 "Driven"의 구분은 **누가 누구를 호출하는가(Who calls whom)** 에 있다.

| 구분 | 호출 주체 | 호출 대상 | 포트 명명 관행 | 예시 |
|:--|:--|:--|:--|:--|
| **Driving (Inbound)** | 외부 액터(Controller, Scheduler) | Application Service | `XxxUseCase`, `XxxFacade`, `CommandService` | `PlaceOrderUseCase` |
| **Driven (Outbound)** | Application Service / Domain | 외부 자원 | `XxxRepository`, `XxxPort`, `XxxGateway`, `XxxPublisher` | `OrderRepository`, `NotificationGateway` |

DDD(도메인 주도 설계)에서는 Inbound Port를 **Command/Query Service**라고도 부르며, Outbound Port는 **Repository**·**Anti-Corruption Layer(ACL)** 와 의미가 겹친다. 헥사고날은 DDD의 *전략적 패턴(Bounded Context, ACL)* 과 *전술적 패턴(Aggregate, Domain Service)* 을 동시에 수용하는 **컨테이너 아키텍처**다.

### 2.4 핵심 메커니즘: 양방향 격리와 의존성 역전

기술사 관점에서 헥사고날이 "**왜 동작하는가**"의 메커니즘은 다음 4가지다.

1. **포트 = 도메인 영역의 추상 인터페이스**: 도메인이 "나는 주문 저장이 필요하다"를 `OrderRepository` 인터페이스로 표현한다. 도메인은 JDBC, Mongo, FileSystem을 **모른다**.
2. **어댑터 = 포트의 기술 구현체**: `OrderJpaRepository`가 Hibernate를 캡슐화한다. 교체 시 `OrderMongoRepository`로 갈아치우면 끝.
3. **컴파일 시점 격리**: 도메인 모듈의 `pom.xml`에는 `spring-data-jpa`,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 477 / 600

<- **이전**: [476. 유비쿼터스 언어 도메인 모델링](/studynote/11_design_supervision/06_exam_summary/477_ubiquitous_language/)
**다음**: [478. 클린 아키텍처 의존성 역전 원칙](/studynote/11_design_supervision/06_exam_summary/478_clean_architecture/) ->

---
