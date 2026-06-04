+++
title = "452. 마이크로서비스 아키텍처 설계 패턴 심화 (MSA Design Pattern Advanced)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MSA 심화 패턴은 분산 시스템의 4대 난제(① 트랜잭션 경계의 붕괴, ② 네트워크 장애 전제, ③ 데이터 일관성 모델 변경, ④ 관측 가능성 부재)를 해결하기 위한 11가지 핵심 패턴(Decomposition, Integration, Database, Observability, Resiliency, Security, Deployment, Communication, Cross-Cutting, Discovery, Testing)의 체계적 집합이며, **Christopher Richardson(Microsoft)이 "Microservices Patterns"(2018)에서 정의한 분류 체계를 기술사 시험 기준으로 재구성한 것**이다.
> 2. **가치**: Well-Architected SaaS 기준 도메인 간 결합도(Coupling) 0.21 -> 0.08로 60%v, 배포 빈도(DORA) 월 1회 -> 일 12회(1,200%^), 장애 폭발 반경(Blast Radius) 단일 서비스 한정으로 MTTR 평균 4시간 -> 18분(92%v), Netflix/AWS가 1,000+ 마이크로서비스 운영으로 증명한 **가용성 99.99% = 연 52분 다운 허용**을 달성하기 위한 실질적 청사진이다.
> 3. **판단 포인트**: **"언제 동기(REST/gRPC) vs 비동기(Kafka/RabbitMQ)를 선택하는가"**가 첫 번째 분기점이며, **"Choreography vs Orchestration Saga"**로 트랜잭션 복잡도 5단계(Simple->Nested->Parallel->Mixed->Long-Running)를 제어하고, **"Database per Service vs Shared DB"**의 경계에서 Eventual Consistency 허용 SLA(통상 1초~5분)를 도메인별로 차등 적용하는 것이 기술사의 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

### 1.1 모놀리식 아키텍처의 한계와 MSA 전환 압력

2010년대 이후 Netflix(700+ 서비스, 2019), Amazon(1,000+ 서비스, AWS re:Invent 2018), Uber(2,200+ 서비스, 2020) 등 초대형 트래픽 사업자는 모놀리식 아키텍처의 **3대 병목**을 경험했다:

| 병목 | 정량적 임계치 | 영향 |
|:---|:---|:---|
| 빌드/배포 시간 | 코드 100만 라인 초과 시 CI 30분+, 배포 윈도우 4시간+ | 피쳐 릴리즈 주기 6개월 이상 |
| 스케일 비효율 | 전체 인스턴스의 5%만 트래픽 집중(Heat Map 비대칭) | AWS 비용 35~60% 낭비 |
| 장애 격리 불가 | 메모리 누수 1개 -> 전체 JVM Heap 32GB 강제 종료 | 연간 5~10회 P0 장애, 매출 손실 ₩수십억/회 |

### 1.2 분산 시스템의 본질적 복잡성 (Fallacies of Distributed Computing)

Sun Microsystems의 Peter Deutsch(1994)가 정리한 **8가지 오류**(모두 마이크로서비스 적용 시 반드시 검증해야 함):

```
[1] 네트워크는 신뢰할 수 있다          -> Timeout/Retry 필수
[2] 지연(latency)은 0이다              -> Tail Latency(P99) 추적 필수
[3] 대역폭은 무한하다                  -> 직렬화/페이로드 최적화
[4] 네트워크는 보안되어 있다            -> mTLS/JWT 필수
[5] 토폴로지는 변하지 않는다            -> Service Discovery 필수
[6] 관리자는 한 명이다                 -> 분산 Tracing 필수
[7] 전송 비용은 0이다                  -> HTTP/2, gRPC 압축
[8] 네트워크는 균질하다                -> Multi-Region, Multi-AZ 고려
```

### 1.3 Strangler Fig Pattern (Martin Fowler, 2004)

레거시 모놀리스를 단계적으로 MSA로 전환하는 표준 절차. **'외교관 패턴'**이라고도 불리며, Anti-Corruption Layer(ACL)를 두어 신규 서비스가 레거시 도메인 모델에 오염되지 않도록 보호한다.

```text
-----------------------------------------------------------------------
   Strangler Fig Pattern: Monolith -> MSA 점진적 전환 (24~36개월)
-----------------------------------------------------------------------

  [Legacy Monolith]                  [Target MSA]
  +------------------+               +------------------+
  |  UI (JSP/Thymeleaf)|               |  Web BFF (GraphQL)|
  +------------------+  <---Router--->  +------------------+
  |  Order Service   |   (Nginx/      |  Order Service   | <- 신규
  |  Inventory       |    Envoy)      |  Inventory       | <- 신규
  |  Payment         |               |  Payment         | <- 미이관
  |  Member          |               |  Member          | <- 미이관
  |  (5,000 Classes) |               |  Notification    | <- 신규
  +------------------+               +------------------+
                                            ^
                                            | Event Bus (Kafka)
                                            | topic: order.created
                                            v
                                   +------------------+
                                   | Anti-Corruption  |
                                   | Layer (ACL)      |
                                   | - Domain Mapper  |
                                   | - Schema Adapter |
                                   | - Legacy Gateway |
                                   +------------------+

  Phase 1 (0~6M)  : 1개 도메인 신규 + Router에서 1% 트래픽 라우팅
  Phase 2 (6~12M) : 3개 도메인 신규 + 트래픽 50% -> 카나리 배포
  Phase 3 (12~24M): 7개 도메인 신규 + 모놀리스 read-only 전환
  Phase 4 (24~36M): 모놀리스 폐기 + 모든 트래픽 MSA 전환
-----------------------------------------------------------------------
```

- **📢 섹션 요약 비유**: 거대한 떡 케이크(모놀리식)를 한 번에 자르려 하면 뭉개지므로, **케이크를 한 조각씩 떼어내어 개별 도시락(MSA)에 담는 과정**이 Strangler Fig 패턴이다. 이때 도시락에 옮긴 조각이 원래 케이크와 섞이지 않게 **랩(ACL)**으로 감싸는 것이 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 MSA 심화 패턴의 6대 영역 분류

Christopher Richardson의 분류를 실무 기준으로 재구성하면 다음과 같다:

| 대영역 | 핵심 패턴 수 | 대표 패턴 | 적용 시점 |
|:---|:---:|:---|:---|
| **Decomposition** | 3 | 비즈니스 능력/하위 도메인/Strangler | MSA 도입 초기 |
| **Communication** | 5 | API Gateway/gRPC/Event-Driven/Pub-Sub/GraphQL | 서비스 간 호출 발생 시 |
| **Data** | 4 | DB-per-Service/Saga/CQRS/Event Sourcing | 트랜잭션/조회 발생 시 |
| **Resiliency** | 6 | Circuit Breaker/Bulkhead/Retry/Timeout/Rate Limit/Sidecar | 운영 단계 |
| **Observability** | 5 | Health Check/Log Aggregation/Metrics/Tracing/Audit | 운영 전 단계 필수 |
| **Security/Cross-Cutting** | 4 | mTLS/OAuth2/Service Discovery/Config Server | 초기 설계 단계 |

### 2.2 Saga Pattern (가장 빈출 기술사 출제 패턴)

**분산 트랜잭션**을 ACID가 아닌 **BASE**(Basically Available, Soft state, Eventual consistency)로 해결하는 패턴. 1987년 Hector Garcia-Molina가 논문으로 최초 제안, Chris Richardson이 2018년 MSA 컨텍스트로 정형화.

```text
-----------------------------------------------------------------------
   Saga Pattern: Choreography vs Orchestration 비교 시퀀스
-----------------------------------------------------------------------

  [A] Choreography (이벤트 기반, 서비스 자율 조정)
  -----------------------------------------------------------
  OrderSvc ---> [order.created] ---> InventorySvc
                                      |
                                      +---> [inventory.reserved] ---> PaymentSvc
                                      |                                  |
                                      |                                  +---> [payment.completed] ---> OrderSvc(완료)
                                      |                                  |
                                      |                                  +---> [payment.failed] ---> InventorySvc
                                      |                                                       |
                                      |                                                       +---> [inventory.released] (보상)
                                      |
                                      +---> [inventory.out_of_stock] ---> OrderSvc(취소)

  장점: 단일 장애점(SPOF) 없음, 느슨한 결합
  단점: 5개+ 서비스 후 추적 난이도 급상승, EventStorming 필요


  [B] Orchestration (중앙 조정자, 명시적 제어)
  -----------------------------------------------------------
  [Saga Orchestrator (e.g., Temporal/Camunda/Axon)]
      |
      +-- Step 1: InventorySvc.reserve()    -- 성공 -> Step 2
      |                                  +-- 실패 -> 보상 트랜잭션 없음 (시작점)
      |
      +-- Step 2: PaymentSvc.charge()       -- 성공 -> Step 3
      |                                  +-- 실패 -> Step 1 보상: InventorySvc.release()
      |
      +-- Step 3: ShippingSvc.schedule()    -- 성공 -> Saga 완료
      |                                  +-- 실패 -> Step 2 보상: PaymentSvc.refund()
      |                                            -> Step 1 보상: InventorySvc.release()
      |
      +-- State: PENDING -> RESERVED -> PAID -> SCHEDULED -> COMPLETED

  장점: 흐름 가시성, 타임아웃/재시도 명시적 제어, BPMN 매핑 용이
  단점: Orchestrator가 SPOF 가능성, 도메인 결합도 상승

-----------------------------------------------------------------------
```

| Saga 보상 트랜잭션 5가지 핵심 규칙 (Chris Richardson) | 설명 | 예시 |
|:---|:---|:---|
| **1. 보상 가능성 (Compensable)** | 모든 트랜잭션은 의미상 취소 가능해야 함 | `PaymentSvc.charge()` ↔ `PaymentSvc.refund()` |
| **2. 멱등성 (Idempotent)** | 동일 요청을 N번 실행해도 결과 동일 | 멱등키(Idempotency-Key) UUIDv7 사용 |
| **3. 교환 가능성 (Swappable)** | 비순차 실행 가능 (병렬 처리) | `OrderSaga`의 결제/쿠폰 차감 병렬화 |
| **4. 재시도 가능 (Retriable)** | Transient Failure 시 자동 재시도 | Resilience4j `@Retry(maxAttempts=3)` |
| **5. 순서 의존성 검증 (Testable)** | 단위 테스트로 검증 가능 | Pact/Spring Cloud Contract |

### 2.3 Circuit Breaker & Bulkhead (Netflix Hystrix -> Resilience4j 마이그레이션)

```text
-----------------------------------------------------------------------
   Circuit Breaker State Machine + Bulkhead 분리
-----------------------------------------------------------------------

                  +------------------------------------+
                  |  Circuit Breaker States            |
                  +------------------------------------+

  +----------+   failureRate ≥ 50%    +----------+
  |  CLOSED  | ------------------>    |   OPEN   |
  | (정상)   |   (sliding window     | (차단)   |
  |  카운터  |    10s, 100 req)      | 10s 대기 |
  | 증가     |                       |          |
  +----------+                       +----------+
        ^                                  |
        | success                          | waitDurationInOpenState
        | rate ≥ 80%                      | 10s 경과
        |                                 v
        |                          +----------+
        +--------------------------|HALF_OPEN |
                                   |(시험)    |
                                   | 5 req    |
                                   +----------+
                                         |
                                         | 5 req 중 4 req 실패
                                         v
                                    다시 OPEN (10s)

  -----------------------------------------------------------
  Bulkhead: Thread Pool / Semaphore 분리

  +------------------------------------------------------+
  |  ThreadPool Bulkhead (기본값: maxThreadPoolSize=20)  |
  |  +----------+  +----------+  +----------+            |
  |  | Payment  |  | Search   |  | External |            |
  |  | (20 스레드)|  | (30 스레드)|  | API(10)  |            |
  |  +----------+  +----------+  +----------+            |
  |  -> 한 영역 고갈이 다른 영역으로 전파되지 않음 (격리)  |
  +------------------------------------------------------+
-----------------------------------------------------------------------
```

| Resilience4j 모듈 | 기본 임계값 (Netflix Hystrix 기준) | 실무 권장 값 |
|:---|:---|:---|
| CircuitBreaker | failureRateThreshold=50%, slidingWindowSize=100, waitDurationInOpenState=10s | 결제: 30%, 검색: 70% (트래픽 변동성 고려) |
| Retry | maxAttempts=3, waitDuration=500ms, exponentialBackoff | 비핵심 API: 3회, 결제: 1회 (중복 결제 방지) |
| Bulkhead | maxThreadPoolSize=20, maxWaitDuration=0ms | 결제: 50, 알림: 10, 외부 API: 5 |
| RateLimiter | limitForPeriod=50, limitRefreshPeriod=500ms | 사용자 단위 Token Bucket |
| TimeLimiter | timeoutDuration=2s | 외부 API: 1s, 내부: 500ms |

### 2.4 CQRS + Event Sourcing (검색/명령 분리 + 이벤트 저장)

```text

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 452 / 600

<- **이전**: [451. 451. 정보관리·시스템 감리 평가 빈출 키워드 100% 매핑 요약 연결망 (High-Frequency Information Management and System Audit Keyword Mapping Network)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/451_audit/)
**다음**: [453. 이벤트 소싱 CQRS 설계 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/453_event_sourcing_cqrs/) ->

---
