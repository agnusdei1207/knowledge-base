---
title: "479. 양파 아키텍처 계층 분리 (Onion Architecture Layer Separation)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 양파 아키텍처(Onion Architecture)는 Jeffrey Palermo(2008)가 제안한 의존성 역전 원칙(DIP) 기반의 계층형 아키텍처로, 모든 의존성 화살표가 중심(Domain Core)을 향해 단방향으로 흐르며 외부 인프라스트럭처(DB·UI·Framework)가 도메인에 의존하지 않고 그 반대만 허용되는 **"Dependency Rule"** 이 핵심이다.
> 2. **가치**: 도메인 모델의 프레임워크·DB·UI 독립성 보장으로 단위 테스트 커버리지를 80% 이상 달성하고, ORM 교체나 Web Framework 전환 시 도메인 코드 수정 0% 보장, AOP·MSA로의 진화 시에도 비즈니스 로직 100% 재사용이 가능해진다.
> 3. **판단 포인트**: 도메인 계층의 추상화 수준(Granularity) 결정이 핵심이며, 지나치게 세분화된 인터페이스는 **"Interface Proliferation"** 안티패턴을, 느슨한 경계는 **"Leaky Abstraction"** 을 야기한다. CRUD 위주의 단순 시스템에서는 오히려 Layered Architecture 대비 약 30% 이상의 보일러플레이트 오버헤드를 감수해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적인 3-Tier Layered Architecture(Presentation -> Business -> DataAccess)에서 빈번히 발생하는 **"영속성 오염(Persistence Ignorance 손실)"** 문제, 즉 도메인 엔터티가 `Entity Framework`, `Hibernate` 같은 ORM의 `DbSet`, `@Entity` 어노테이션에 직결되어 비즈니스 변경이 DB 스키마 변경으로 직행되는 현상을 해결하기 위해 등장했다. 또한 N-Tier 아키텍처는 데이터 접근 계층이 UI 계층에도 노출되는 **"순환 의존성 위험"** 과, **"Smart UI"** 안티패턴으로 빠지기 쉬운 구조적 한계를 내포하고 있다.

양파 아키텍처는 이를 해결하기 위해 **"바깥에서 안으로만 의존한다"** 라는 단 하나의 규칙(Dependency Rule)을 코드로 강제하여, 인프라스트럭처가 도메인의 플러그인이 되도록(Infrastructure as Plugin) 설계한다. 이로써 비즈니스 정책 변경 시 DB·UI·Message Queue를 동시에 바꿔야 하는 **"Shotgun Surgery"** 현상이 근본적으로 차단된다.

```text
        [ 전통 Layered Architecture ]              [ Onion Architecture ]
        --------------------------                -----------------------------
        +----------------------+                  +--------------------------+
        |    Presentation      |                  |  Infrastructure (외피)   |
        |  (UI / Web / API)    |                  |  EF Core, Redis, SMTP    |
        +----------+-----------+                  |  +--------------------+  |
                   | 의존                          |  |   Application      |  |
                   v                              |  |  (UseCase/Service) |  |
        +----------------------+                  |  | +----------------+ |  |
        |     Business         | <--- 영속성 오염!  |  | | Domain Service | |  |
        |  (Entity+Logic 혼재) |                  |  | |+--------------+| |  |
        +----------+-----------+                  |  | || Domain Core  || |  |
                   | 의존                          |  | ||  (Entity,VO) || |  |
                   v                              |  | |+--------------+| |  |
        +----------------------+                  |  | +----------------+ |  |
        |      DataAccess      |                  |  +--------------------+  |
        |   (Repository)       |                  +--------------------------+
        +----------------------+                            ^ 단방향 의존만 허용
              순환의존 위험                                  |
                                                          +--> 모든 화살표가 안쪽
```

```text
양파 아키텍처 전체 구조 (의존성 방향 시각화)

                       +---------------------------------+
                       |   UI / API / gRPC / GraphQL     |  <--- 가장 바깥
                       |   (Controller, DTO, ViewModel)  |
                       +---------------+-----------------+
                                       | implements
                       +---------------v-----------------+
                       |      Infrastructure Layer        |
                       |  +- EF Core / Dapper / JDBC     |
                       |  +- Repository Impl (구현체)     |
                       |  +- External API Client (Http)  |
                       |  +- Message Broker (Kafka)      |
                       |  +- FileSystem / ObjectStorage  |
                       +---------------+-----------------+
                                       | implements
                       +---------------v-----------------+
                       |   Application Service Layer      |
                       |   +- UseCase Orchestrator       |
                       |   +- DTO ↔ Domain Mapper        |
                       |   +- Transaction Script         |
                       |   +- CQRS Command/Query Handler |
                       +---------------+-----------------+
                                       | calls
                       +---------------v-----------------+
                       |   Domain Service Layer           |
                       |   +- Domain Service Interface    |
                       |   +- Repository Interface        |
                       |   +- Specification Pattern       |
                       +---------------+-----------------+
                                       | owns
                       +---------------v-----------------+
                       |   Domain Model (Core)            |
                       |   +- Entity (Aggregate Root)     |
                       |   +- Value Object               |
                       |   +- Domain Event               |
                       |   +- Domain Exception           |
                       +---------------------------------+
                                  ^ 가장 안쪽
                                  | 어떤 외부 의존성도 없음
                                  +--> 순수 C#/Java/Kotlin POJO
```

- **📢 섹션 요약 비유**: 양파 아키텍처는 마치 **인형의 눈처럼** 겹겹이 둘러싼 구조인데, 바깥 껍질(UI, DB)을 아무리 바꿔도 가장 안쪽의 **"동공(Domain)"** 은 절대 흔들리지 않습니다. 또 양파를 썰어보면 한 방향(중심)으로만 결이 흐르듯, 코드 의존성도 한 방향(중심)으로만 흐릅니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

양파 아키텍처의 핵심 메커니즘은 **"Dependency Inversion Principle(DIP)"** 을 인터페이스(Port)의 형태로 계층 경계에 강제 배치하는 것이다. C#에서는 `interface` 와 `Microsoft.Extensions.DependencyInjection`, Java에서는 `Spring`의 `@Autowired` 와 Java SPI, Python에서는 `dependency-injector` 라이브러리가 이를 실현한다.

```text
의존성 주입(DI) 흐름 상세 시퀀스

    [Client/UI]        [Composition Root]      [App Service]     [Domain]      [Infra]
         |                     |                     |              |             |
         |  1. CreateHost()    |                     |              |             |
         | ------------------->|                     |              |             |
         |                     |  2. Register<IOrder |              |             |
         |                     |     Repository,     |              |             |
         |                     |     OrderRepository |              |             |
         |                     |     >()             |              |             |
         |                     |                     |              |             |
         |  3. GET /orders/42  |                     |              |             |
         | ------------------->|  4. Resolve         |              |             |
         |                     | ------------------->|              |             |
         |                     |                     |  5. order =  |             |
         |                     |                     |   repo.find()|             |
         |                     |                     | -------------------------> |
         |                     |                     |              |  6. SQL실행  |
         |                     |                     | <- Order(Entity)-----------|
         |                     |                     |              |             |
         |                     |                     | 7. domain rules check      |
         |                     |                     | ------------>|             |
         |                     | <- Result(DTO)------|              |             |
         | <- 200 OK + JSON ---|                     |              |             |
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Domain Model (Core)** | 비즈니스 불변식(Invariant) 표현, Aggregate Root 단위의 트랜잭션 일관성 보장 | 순수 POJO/POPO, `Entity<TId>`, `ValueObject` (base class), 도메인 이벤트(`OrderPlaced`), `Specification Pattern`, C#의 `record`/Java의 `record` |
| **Domain Service Interface (Port)** | Repository, 외부 시스템 추상화 인터페이스 정의 | `IOrderRepository`, `IPaymentGateway`, `IEmailSender` — 도메인이 필요로 하는 **계약(Contract)** 만 선언하며 구현은 알지 못함 |
| **Application Service** | UseCase 오케스트레이션, 트랜잭션 경계(`@Transactional` / `TransactionScope`), DTO 변환 | MediatR `IRequestHandler<TCommand, TResult>`, CQRS Command/Query 분리, FluentValidation으로 입력 검증 |
| **Infrastructure Adapter** | Port 인터페이스의 **실제 구현체**, 외부 기술 종속성 격리 | `OrderRepository : IOrderRepository` (EF Core `DbContext` 사용), `HttpPaymentGateway : IPaymentGateway` (HttpClient + Polly), `KafkaEventBus` |
| **UI / Presentation** | HTTP/gRPC/WebSocket 프로토콜 처리, 인증/인가, DTO 직렬화 | ASP.NET Core `Controller`, Spring `@RestController`, FastAPI `router`, gRPC `Service` — 도메인 모델을 직접 노출하지 않고 DTO로 변환 |
| **Composition Root** | 모든 의존성을 와이어링(Wiring)하는 단일 진입점 | `Program.cs`(`Host.CreateDefaultBuilder`), SpringBoot `Application` 클래스, NestJS `AppModule` — DIP 실현의 핵심 |

### 핵심 알고리즘: 의존성 방향 검증(Layered Architecture Linter)

빌드 시 `NetArchTest`(.NET), `ArchUnit`(Java), `deepsource`(TypeScript) 같은 아키텍처 단위 테스트로 **"Domain에서 Infrastructure 참조 시 빌드 실패"** 를 강제할 수 있다.

```csharp
// .NET - NetArchTest 예시
[Fact]
public void Domain_Should_Not_Depend_On_Infrastructure()
{
    var result = Types.InAssembly(typeof(Order).Assembly)
        .ShouldNot()
        .HaveDependencyOn("MyApp.Infrastructure")
        .GetResult();
    Assert.True(result.IsSuccessful);
}
```

```java
// Java - ArchUnit 예시
@ArchTest
static final ArchRule domain_should_not_depend_on_infrastructure =
    noClasses().that().resideInAPackage("..domain..")
        .should().dependOnClassesThat().resideInAPackage("..infrastructure..");
```

### 핵심 메트릭 및 정량 설계 기준

| 지표 | 권장 기준 | 측정 도구 |
| :--- | :--- | :--- |
| Domain 순환 의존성 수 | **0개** | NDepend, SonarQube, JDepend |
| Domain -> Infrastructure Fan-out | **0%** | ArchUnit, NetArchTest |
| Aggregate Root당 Entity 수 | **≤ 7개** (Vaughn Vernon 권고) | 수동 리뷰 |
| Application Service 평균 LOC | **≤ 200 LOC** | SonarQube Cognitive Complexity |
| Domain 테스트 커버리지 | **≥ 80%** (전체 60% 이상) | Coverlet, JaCoCo, Istanbul |

- **📢 섹션 요약 비유**: 양파 아키텍처의 **Port(인터페이스)** 는 마치 **전용 콘센트 규격** 과 같습니다. 한국 가전(도메인)이 220V 인프라(어댑터)에 직접 꽂히지 않고, **"USB-C 같은 표준 규격(Port)"** 만 알면 됩니다. 어댑터(Repository 구현체)만 바꿔주면 110V 일본, 240V 유럽 어디서도 동작합니다.

---

## Ⅲ. 비교 및 연결

| 구분 | **Layered (N-Tier)** | **Onion** | **Hexagonal (Ports & Adapters)** | **Clean Architecture (Uncle Bob)** |
| :--- | :--- | :--- | :--- | :--- |
| 제안자 | Microsoft/Tanenbaum | Jeffrey Palermo (2008) | Alistair Cockburn (2005) | Robert C. Martin (2012) |
| 의존성 방향 | 위->아래 (강결합) | 바깥->안 (단방향, DIP 강제) | 안->Port, Port<-Adapter | Entities -> UseCases -> InterfaceAdapters -> Frameworks |
| DIP 적용 | ❌ (DataSet 노출) | ✅ (Repository Interface) | ✅ (Port/Adapter) | ✅ (Interface Adapters) |
| DB 교체 용이성 | ❌ Schema 직접 의존 | ✅ Repository 교체 | ✅ Adapter 교체 | ✅ Interface 구현체 교체 |
| 프레임워크 독립성 | ❌ | ✅ | ✅ | ✅✅ (가장 엄격) |
| DDD 친화성 | △ | ✅ | ✅ | ✅✅ |
| 보일러플레이트 | 낮음 | 중~높음 | 높음 | 매우 높음 |
| 적합 시스템 | 단순 CRUD | 중소규모 도메인 | MSA·Event-Driven | 장기 운영 Legacy 대체 |
| 약점 | 도메인 오염, 순환 의존 | 과도한 인터페이스 | 명칭 혼란(Port/Adapter) | 학습 곡선, 오버엔지니어링 위험 |

### 통합 관계

- **DDD (Domain-Driven Design)**: Aggregate Root를 Domain Core에 배치, Bounded Context별로 양파를 분리
- **CQRS + Event Sourcing**: Application Service를 Command/Query Handler로 분리, Domain Event를 통해 인프라 Message Broker로 발행
- **MSA 진화**: 각 Bounded Context를 독립 양파(Independent Onion)로 배포, Inter-Service 통신은 OpenAPI/gRPC로 외부 Port 노출
- **AOP (관점 지향 프로그래밍)**: Cross-cutting Concerns(로깅, 트
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 479 / 600

<- **이전**: [478. 클린 아키텍처 의존성 역전 원칙](/studynote/11_design_supervision/06_exam_summary/478_clean_architecture)
**다음**: [480. CQRS 명령 조회 분리 패턴 심화](/studynote/11_design_supervision/06_exam_summary/480_cqrs_advanced/) ->

---
