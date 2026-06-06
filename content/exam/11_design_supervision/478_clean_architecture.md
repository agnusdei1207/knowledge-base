---
title: "Clean Architecture Dependency Inversion"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클린 아키텍처의 의존성 역전 원칙(DIP)은 고수준 정책(엔터티·유스케이스)이 저수준 메커니즘(DB·웹·UI)에 의존하지 않고, 양쪽이 모두 추상화(인터페이스·포트)에 의존하도록 강제하여 **"소스 코드 의존성의 방향"을 제어 흐름의 역방향으로 회전**시키는 설계 원칙이다.
> 2. **가치**: 프레임워크 교체 비용 최소화(Spring->Quarkus 마이그레이션 사례에서 평균 60~70% 코드 재사용), 테스트 용이성 향상(유스케이스 레이어의 단위 테스트 커버리지 90% 이상 달성 가능), 그리고 도메인 로직의 비즈니스 불변성 보존을 통한 10년 이상 장기 유지보수 시스템의 기술 부채 누적 속도를 획기적으로 저감한다.
> 3. **판단 포인트**: 모든 계층에 DIP를 무조건 적용하면 추상화 폭증으로 인한 인지 부하·런타임 오버헤드·간접 참조 디버깅 난이도가 증가하므로, **변경 빈도와 변경 사유(Reuse/Release Coupling 관점)**를 기준으로 의존성 역전 적용 범위를 판단하는 것이 기술사의 핵심 역량이다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 시스템이 장기간 운영되면 **변경의 축(axis of change)**이 충돌하면서 아키텍처가 무너진다. 2003년 Robert C. Martin이 기고한 *Designing Object-Oriented C++ Applications*와 1996년 *The Dependency Inversion Principle* 논문에서 출발한 DIP는, 객체지향 설계 5원칙(SOLID) 중 마지막 'D'로서 전통적인 계층형 아키텍처(Layered Architecture)의 고질적 문제—**상위 계층이 하위 계층의 구체 클래스를 직접 import하여 변경에 취약해지는 구조**—를 해결하기 위해 제안되었다.

전통적 3-Tier 아키텍처(Presentation -> Business -> Data Access)에서는 `OrderService`가 `MySQLOrderRepository`를 직접 호출하므로, 데이터 저장소를 PostgreSQL로 교체하거나 ORM을 MyBatis에서 JPA로 변경하는 순간 비즈니스 로직이 위치해야 할 서비스 계층까지 함께 수정되어야 했다. 이는 2000년대 초중반 EJB2 시절의 **EntityBean 의존성 지옥**을 거쳐, 2010년대 들어 마이크로서비스·클라우드 네이티브 환경에서 MSA 간 통신 프로토콜(HTTP/REST -> gRPC -> Kafka) 변경이 빈번해지면서 더욱 두드러진 문제로 부상했다.

특히 **Hexagonal Architecture(Alistair Cockburn, 2005)**, **Onion Architecture(Jeffrey Palermo, 2008)**, 그리고 2012년 Robert C. Martin의 *Clean Architecture* 모두 공통적으로 **"외부로 갈수록 구체적인 메커니즘, 내부로 갈수록 추상적인 정책"**이라는 동일한 의존성 규칙을 채택하고 있다. 이는 결국 "비즈니스가 기술을 선택한다"는 잘못된 전제를 뒤집고 **"기술이 비즈니스에 맞춰 교체 가능해야 한다"**는 엔터프라이즈 아키텍처의 본질적 요구사항을 코드로 강제하는 것이다.

```text
[전통적 계층 구조 vs 클린 아키텍처 의존성 방향 비교]

  ❌ 전통적 Layered Architecture            ✅ 클린 아키텍처 (의존성 역전 적용)
  -----------------------------             ----------------------------------
  +---------------------+                  +-------------------------------+
  |  Presentation (UI)  |                  | Frameworks & Drivers (Spring) |
  |   ---- imports ---- |                  |  implements Port Interface   |
  +---------------------+                  +-------------------------------+
  |  Business Service   | <-- 직접참조     | Interface Adapters             |
  |   ---- imports ---- |                  |  (Controller, Repository Impl)|
  +---------------------+                  +-------------------------------+
  |  Data Access (DAO)  |                  | Use Cases (Application)        |
  |   MySQL JDBC 사용   |                  |  정의: Port (Input/Output)    |
  +---------------------+                  +-------------------------------+
       ^ 의존성 방향 = 제어 흐름           | Entities (Domain Model)       |
       (변경 시 상위까지 전파)              +-------------------------------+
                                                ^ 의존성 방향 = 안쪽으로만
                                                (변경 시 바깥쪽만 영향)
```

기존 패러다임은 **"어떤 클래스가 어떤 클래스를 호출하는가"**에 집중했다면, DIP 기반 아키텍처는 **"어떤 모듈이 어떤 인터페이스의 소스 코드를 알고 있는가"**에 집중한다. 이 차이는 단순한 코드 스타일이 아니라, **컴파일 시점 의존성(compile-time dependency)**과 **런타임 의존성(runtime dependency)**을 분리한다는 점에서 아키텍처적 패러다임 전환이라 할 수 있다.

- **📢 섹션 요약 비유**: 의존성 역전이 없는 코드는 마치 **콘크리트로 벽과 가구를 한번에 굳어버린 아파트**와 같다. 가구를 바꾸고 싶어도 벽을 부수지 못한다. 클린 아키텍처는 **벽은 콘크리트지만 모든 가구에 콘센트(인터페이스) 규격**을 미리 매겨두고, 가구를 자유롭게 교체할 수 있도록 설계한 **한옥의 온돌과 같은 모듈식 공간**이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클린 아키텍처의 DIP는 **두 가지 핵심 명제**로 요약된다(원문):

1. *High-level modules should not depend on low-level modules. Both should depend on abstractions.*
2. *Abstractions should not depend on details. Details should depend on abstractions.*

이를 코드로 표현하면, `OrderService`(고수준)는 `OrderRepository`(추상 인터페이스)를 소유하고, `MySQLOrderRepositoryImpl`(저수준)이 이를 구현한다. 의존성 방향은 구현체가 인터페이스로 향하는 **안쪽 방향**이며, 이 점이 **Hollywood Principle("Don't call us, we'll call you")**와 본질적으로 동일하다.

```text
[클린 아키텍처 4계층 + DIP 의존성 흐름 상세도]

         바깥쪽 ------------------------------------------------ 안쪽
         (구체적/변동성 높음)                              (추상적/변동성 낮음)

  +--------------------------------------------------------------+
  | Frameworks & Drivers (외부세계와의 접점)                      |
  | --------------------------------------------------------     |
  | • Spring Boot 3.x, .NET 8, FastAPI, NestJS                 |
  | • MyBatis, JPA/Hibernate, Spring Data JDBC                  |
  | • Kafka Producer, gRPC Client, RestTemplate, WebClient      |
  | • PostgreSQL, Redis, MongoDB, S3                            |
  |                                                              |
  |   [Spring @Configuration] [KafkaTemplate Bean]              |
  |        | implements                                          |
  |        v                                                     |
  +--------------------------------------------------------------+
  | Interface Adapters (컨트롤러·프레젠터·게이트웨이 구현체)      |
  | --------------------------------------------------------     |
  | • REST Controller (@RestController, @GetMapping)            |
  | • DTO ↔ Domain Mapper (MapStruct, AutoMapper)               |
  | • Repository Adapter (MySQLOrderRepository)                 |
  | • 외부 시스템 어댑터 (PaymentGatewayAdapter)                 |
  |                                                              |
  |   [OrderRestController] [MySQLOrderRepositoryImpl]          |
  |        | calls                                               |
  |        v                                                     |
  +--------------------------------------------------------------+
  | Use Cases (애플리케이션 비즈니스 규칙)                        |
  | --------------------------------------------------------     |
  | • Input Port: CancelOrderUseCase (interface)                 |
  | • Output Port: OrderRepository, NotificationPort (interface)|
  | • Service: CancelOrderService implements CancelOrderUseCase |
  | • @Transactional, 도메인 이벤트 발행                        |
  |                                                              |
  |   [CancelOrderUseCase] <--- 의존성 방향 (안쪽 -> 안쪽)         |
  |        | uses                                                |
  |        v                                                     |
  +--------------------------------------------------------------+
  | Entities (엔터프라이즈 비즈니스 규칙 / 도메인 모델)           |
  | --------------------------------------------------------     |
  | • Aggregate Root: Order, Customer, Product                   |
  | • Value Object: Money, Address, OrderId                     |
  | • Domain Event: OrderCancelled, PaymentRequested            |
  | • Pure POJO/POPO (no framework annotation: NO @Entity!)     |
  +--------------------------------------------------------------+
          ^                          ^
          |                          |
   Concrete impl                 Pure abstract
   (변경 가능)                   (변경 빈도 낮음)
```

위 다이어그램에서 가장 중요한 점은 **안쪽 동그라미에 있는 어떤 것도 바깥쪽 동그라미에 있는 어떤 것에 대해서도 그 이름을 언급해서는 안 된다**는 *The Dependency Rule*이다. 즉 `Order` 엔터티는 `MySQL`, `JPA`, `Spring`이라는 단어 자체를 import 구문에 포함하면 안 되며, 이를 위해 **Domain에서 Framework를 의존성 자체에서 제외**(Spring이 아닌 jakarta.persistence를 Domain에서 격리하는 등의 작업)하는 것이 핵심이다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Entity (도메인 모델)** | 엔터프라이즈 전사적 핵심 규칙 캡슐화. 가장 변하지 않는 비즈니스 불변식(invariant) 표현 | JPA·Spring 등 외부 프레임워크 무관한 POJO. DDD Aggregate Root·Value Object·Domain Event로 구성. 예: `Order.cancel()`은 상태 전이 규칙을 내부에 강제 |
| **Use Case (Interactor)** | 애플리케이션 특화 비즈니스 규칙. 시스템의 의도된 사용 시나리오를 캡슐화 | 순수 자바/코틀린 인터페이스(`Input Port`)와 그 구현체(`Service`)로 분리. `Order` 엔터티를 조작하며 `Output Port`를 호출 |
| **Interface Adapter** | 외부 세계(DB·UI·웹) 형식 ↔ 내부 도메인 형식 변환 | `Controller`, `Presenter`, `Gateway`, `Repository Impl`이 위치. DTO ↔ Domain 매핑은 **순수 함수형 매퍼**(MapStruct 등)로 분리 |
| **Frameworks & Drivers** | 가장 바깥쪽. 외부 시스템과의 물리적 I/O 담당 | Spring, .NET, DB 드라이버, Kafka Client, gRPC Stub 등. **여기만 교체 가능**하도록 설계. `@Configuration` 클래스에서 DI로 어댑터 바인딩 |

DIP가 의존성 주입(DI: Dependency Injection)과 종종 혼동되지만, 이 둘은 **원칙 vs 메커니즘**의 관계이다. DIP는 *설계 원칙*이고, 이를 구현하는 **메커니즘**에는 다음 세 가지가 있다:

1. **Constructor Injection** — 생성자를 통한 주입(Spring `@Autowired` 기본, .NET `IServiceCollection`). 불변성 보장, 테스트 용이성 최상.
2. **Setter Injection** — 선택적 의존성에 적합. Spring `@Autowired(required=false)`.
3. **Interface Injection (Callback)** — Avalon Framework 스타일. 의존하는 객체가 injector에 자신을 전달.

추가로 DIP를 만족시키기 위한 **패턴적 메커니즘**으로 Factory Pattern, Abstract Factory Pattern, Service Locator Pattern(단, 안티패턴으로 분류되기도 함), Strategy Pattern, Template Method Pattern, Adapter Pattern이 활용된다. Spring Framework는 내부적으로 `ApplicationContext`라는 **IoC(Inversion of Control) Container**를 통해 DIP를 자동으로 와이어링하는데, 이를 **IoC 컨테이너 = DIP의 런타임 구현체**라고 이해해야 한다.

- **📢 섹션 요약 비유**: DIP의 의존성 방향은 마치 **고속도로 톨게이트**와 같다. 차(구체 구현체)는 톨게이트(인터페이스)를 통과하여야 요금소 안쪽(도메인)에 도달할 수 있다. 톨게이트 위치·구조는 바깥에서 결정되지만, 안쪽 도시(도메인)의 건물 배치에는 영향을 주지 않는다. 도시를 재개발하려면 톨게이트만 옮기면 된다.

---

## Ⅲ. 비교 및 연결

DIP는 다른 아키텍처 원칙·패턴·프레임워크 워크와 명확히 구분되어야 한다. 기술사 시험에서는 이 구분에 대한 정밀한 비교를 자주 요구한다.

| 구분 | 의존성 역전 원칙 (DIP) | 의존성 주입 (DI) | 제어의 역전 (IoC) | 헥사고날 아키텍처 (Ports & Adapters) |
| :--- | :--- | :--- | :--- | :--- |
| **분류** | SOLID의 'D' 설계 원칙 | GoF가 아닌 Fowler의 패턴(2004) | 더 일반적인 소프트웨어 설계 원리 | Alistair Cockburn의 아키텍처 스타일(2005) |
| **핵심 의도** | 추상화가 구체에 의존하도록 의존성 방향 역전 | 의존 객체를 외부에서 전달(주입) | 프레임워크가 사용자 코드를 호출 | 포트(인터페이스)로 도메인을 격리 |
| **추상화 단위** | 인터페이스/추상 클래스 | 주입 대상 인터페이스 | 프레임워크 콜백·이벤트 | Port (Input/Output) |
| **구현 메커니즘** | 언어 차원의 추상화(Java interface 등) | 생성자/세터/필드 주입, @Autowired | Template Method, Strategy, DI 컨테이너 | DIP + Adapter 패턴의 아키텍처 적용 |
| **의존성 흐름** | 고수준 <- 인터페이스 <- 저수준 | 클라이언트 <- 주입자(injector) | 호출자 -> 피호출자 -> 프레임워크 | 도메인 <- Port <- Adapter |
| **적용 범위** | 클래스·모듈·패키지 레벨 | 객체 생성·결합 레벨 | 프레임워크·런타임 전반 | 시스템·서브시스템 레벨 |
| **대표 구현** | Java interface, C# interface, Go interface | Spring, Guice, Dagger, .NET Core DI, Koin | Spring IoC, EJB Container, .NET Hosting | Netflix Hystrix, Lightbend Akka, 순수 구현 사례 다수 |
| **DIP와의 관계** | 원칙 그 자체 | DIP를 구현하는 한 가지 메커니즘 | DIP보다 상위 추상화 (DI ⊂ IoC) | DIP를 아키텍처 차원으로 확대 적용 |

위 표에서 핵심은 **DIP는 원칙, DI는 메커니즘, IoC는 패러다임, Hexagonal은 아키텍처 스타일**이라는 계층 관계다. 많은 실무자가 이 셋을 동일시하지만, 시험장·기술사 논술에서는 "DIP는 IoC의 일부분이며, DI는 DIP의 한 구현 수단"이라는 정밀한 표현이 요구된다.

**연계 기술**:
- **Domain-Driven Design (Eric Evans, 2003)**: DIP는 DDD의 `Repository`, `Domain Service` 같은 패턴에서 도메인이 영속성·메시징 기술로부터 자유로워지도록 강제하는 역할을 한다. Aggregate Root의 Pure POJO 유지는 곧 DIP 적용의 결과다.
- **MSA(Microservices Architecture
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 478 / 600

<- **이전**: [477. 헥사고날 아키텍처 포트 어댑터](/studynote/11_design_supervision/06_exam_summary/477_hexagonal_architecture)
**다음**: [479. 양파 아키텍처 계층 분리](/studynote/11_design_supervision/06_exam_summary/479_onion_architecture/) ->

---
