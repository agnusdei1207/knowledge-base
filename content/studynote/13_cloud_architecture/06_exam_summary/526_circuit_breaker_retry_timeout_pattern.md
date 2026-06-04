---
title: "526. 서킷 브레이커 재시도 타임아웃 패턴 (Circuit Breaker Retry Timeout Pattern)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 서킷 브레이커 재시도 타임아웃 패턴은 **CLOSED -> OPEN -> HALF_OPEN 3상태 유한 상태 머신(FSM)**으로 장애를 격리하고, **지수 백오프(Exponential Backoff) + 풀/이퀄/디커플드 지터(Jitter)**로 재시도 동시성을 분산하며, **Connect·Read·Write·Overall 다층 타임아웃**으로 동기 호출의 자원 점유 상한을 명시화하는 회복탄력성(Resilience) 3종 세트이다.
> 2. **가치**: 카스케이드 페일러(Cascading Failure)로 인한 다운스트림 Thread Pool 고갈을 차단하여 **MTTR을 80~95% 단축**(Netflix Hystrix 사례: 의존성 장애 시 전체 시스템 가용성 99.99% 유지), SLA 99.9% 이상 달성, **Thundering Herd 문제로 인한 2차 장애 방지**.
> 3. **판단 포인트**: `failureRateThreshold`(기본 50%), `slidingWindowSize`(10~100 call), `waitDurationInOpenState`(30~60s), `permittedNumberOfCallsInHalfOpenState`(5~10회), `maxRetryAttempts`(3~5회) 등 임계값 설정에 따라 **flapping(상태 진동)** 발생 여부가 결정되며, 멱등성(Idempotency) 미보장 API에 대한 재시도 적용은 **중복 결제·중복 주문** 등 데이터 정합성 사고를 유발하므로 결제 트랜잭션에는 적용 금지라는 판단 기준이 핵심이다.

---

## Ⅰ. 개요 및 필요성

마이크로서비스 아키텍처(MSA)로 전환되면서 서비스 간 호출이 동기 HTTP/REST·gRPC 위주로 구성되면, 단일 의존성의 응답 지연이 전체 시스템의 Thread Pool을 고갈시키는 **카스케이드 페일러(Cascading Failure)**가 빈번해진다. Netflix는 2011년 AWS 리전 장애 시 캐스케이이딩 타임아웃으로 24시간 장애를 경험한 후, 2012년 **Hystrix**를 오픈소스로 공개하며 서킷 브레이커 패턴을 업계 표준으로 확립했다.

기존 모놀리식 환경에서는 In-Process 호출이므로 ThreadLocal로 추적이 가능하고 DB Connection Pool과 JVM Heap 내부에서만 자원 경쟁이 발생했다. 반면 MSA 환경에서는 네트워크 I/O가 기본이므로 **요청당 1개 스레드가 평균 200~500ms 점유**되며, 페일오버(Failover), 다중 AZ(Availability Zone) 라우팅, 서비스 디스커버리(Eureka, Consul) 등이 추가된다. 이때 다운스트림이 1초 지연되면 1,000 TPS 기준 **1,000개 스레드가 동시 점유**되어 HikariCP·Tomcat ThreadPool의 MaxPoolSize를 즉시 초과한다.

**서킷 브레이커 + 재시도 + 타임아웃** 3종 패턴은 이 문제를 다음과 같이 분담 해결한다:
- **타임아웃**: 각 호출의 최대 대기 시간을 명시하여 **무한 대기 방지** (e.g., OkHttp `connectTimeout=1s, readTimeout=3s`)
- **재시도**: 일시적 장애(Transient Failure, 5xx·네트워크 단절)에 대해 **자동 복구 시도**하되 동시성을 분산
- **서킷 브레이커**: 일정 실패율 누적 시 **호출 자체를 차단(Fast Fail)**하여 다운스트림 복구 시간 확보

```text
[모놀리식 시대]                          [MSA 시대 - 문제 발생]
+-------------+                          +---------+   sync HTTP    +---------+   sync HTTP    +---------+
|   Client    |  In-Proc Call             | Client  | -----HTTP----► | Order   | -----HTTP----► |Payment  |
|   (UI)      | ◄----------------------►  |   UI    |                | Service |                | Service |
|             |   (JVM Heap 내)           |         | ◄-----200----  | (Tomcat)| ◄----503----- |  (DB지연)|
+-------------+  ThreadLocal 추적        +---------+                +---------+                +---------+
                                          Thread1 OK                Thread2 OK                  Thread3 PENDING
                                                                                                    |
                                                                                                    v
                                                                            [Payment 응답 지연 30s]
                                                                                    |
                                                                                                    v
                                                                       Order Service의 Tomcat ThreadPool
                                                                       Max=200 -> 200개 모두 PENDING
                                                                                    |
                                                                                                    v
                                                                       Health Check 실패 -> ALB 503
                                                                                    |
                                                                                                    v
                                                                       Client UI 전체 5xx -> Cascading Failure!
```

```text
[해결: 3종 패턴 적용]
       Client(UI)
           |
           |  +--- [Timeout] Connect=1s, Read=3s ---+
           v  v                                       |
   +---------------+     +---------------+    FastFail|
   | Retry(3회)    |----►| CircuitBreaker|----►[OPEN]  |
   | Exp Backoff   |     | CLOSED 50%    |            |
   | 100ms->200ms   |     | Window 100    |   +--------+--------+
   | + Jitter(±)   |     | OPEN 60s      |   | Fallback 응답    |
   +---------------+     | HALF_OPEN 5회 |   | - 캐시 데이터     |
                         +-------+-------+   | - 기본값          |
                                 |            | - "잠시 후 재시도"|
                                 v            +-----------------+
                         +---------------+
                         | Order Service |
                         | (정상 응답)     |
                         +-------+-------+
                                 v
                         +---------------+
                         | Payment Service| <- 장애 격리됨
                         | (복구 시간 확보)|
                         +---------------+
```

- **📢 섹션 요약 비유**: 회로차단기(서킷 브레이커)는 **집의 누전차단기**와 같다. 가전제품(의존 서비스)이 합선(장애)되면 전체 집이 정전되지 않도록 해당 회로만 차단하고, 일정 시간(타입아웃) 후 재시도(리셋 버튼)하여 안전을 확보하는 원리다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) 서킷 브레이커 상태 머신(State Machine)

서킷 브레이커는 **CLOSED, OPEN, HALF_OPEN** 3가지 상태로 동작한다. 카운트 기반(Count-Based) 또는 시간 기반(Time-Based) 슬라이딩 윈도우로 실패율을 집계한다.

```text
                    +-----------------------------------------+
                    |              CLOSED State                |
                    |  • 정상 호출 허용                         |
                    |  • 슬라이딩 윈도우(100 calls) 내 실패 집계  |
                    |  • 실패율 ≥ 50% (min 10 calls)           |
                    |    ------------ 트리거 ---------►         |
                    +-----------------------------------------+
                                       |
                                       v
                    +-----------------------------------------+
                    |               OPEN State                 |
                    |  • 즉시 실패 (Fast Fail, no remote call) |
                    |  • waitDurationInOpenState 동안 대기      |
                    |  • Fallback 메서드 호출 (e.g., 캐시 반환) |
                    |    ------ 60초 경과 ------►              |
                    +-----------------------------------------+
                                       |
                                       v
                    +-----------------------------------------+
                    |            HALF_OPEN State               |
                    |  • permittedNumberOfCallsInHalfOpen=5개만 |
                    |    실제 원격 호출 허용 (Trial Calls)       |
                    |  • 5개 중 실패율 < 50% -> CLOSED 복귀     |
                    |  • 5개 중 실패율 ≥ 50% -> OPEN 재전이       |
                    +-----------------------------------------+
```

### 2) 재시도(Retry) 알고리즘

```text
[지수 백오프 + 지터 알고리즘 비교]

1) Pure Exponential Backoff (지터 없음)
   Attempt 1: 100ms
   Attempt 2: 200ms
   Attempt 3: 400ms
   ⚠ 1000개 클라이언트가 동시에 재시도 -> t=200ms에 1000개 동시 요청 (Thundering Herd)

2) Full Jitter (AWS 권장)
   delay = random(0, base * 2^attempt)
   Attempt 1: random(0, 200ms)   -> 평균 100ms
   Attempt 2: random(0, 400ms)   -> 평균 200ms
   Attempt 3: random(0, 800ms)   -> 평균 400ms
   ✓ 요청이 시간축에 균일 분산됨

3) Equal Jitter
   delay = (base * 2^attempt / 2) + random(0, base * 2^attempt / 2)
   최소 지연 보장 + 일부분만 랜덤

4) Decorrelated Jitter (AWS Architecture Blog 2015)
   delay = min(cap, random(base, prev_sleep * 3))
   ✓ 가장 부드러운 분포, 권장 방식

        시간축(ms) -----------------------------------------►
Pure:     |■■■■|                  |■■■■|                  |■■■■|
          t=200ms                t=400ms                t=800ms
          ^ 동시 도달

Full:     |·■·■·■·■|        |·■··■·■·■·■·■·■|   |·■·■··■·■·■··■·■·■··■··■·■·■|
          0~200ms             0~400ms                    0~800ms
          ^ 균일 분산
```

### 3) 다층 타임아웃(Multi-Layer Timeout)

```text
   [Client] --HTTP--► [Load Balancer] --HTTP--► [Service A] --gRPC--► [Service B]
   |                   |                         |                    |
   | T_total=5s        | T_LB=2s                 | T_A=3s             | T_B=2s
   |                   |                         |                    |
   v                   v                         v                    v
   +----------------+ +----------------+       +--------------+    +--------------+
   | 1. ConnectTimeout| | 4. BackendResp |       | 5. ReadTimeout|   | 7. OpTimeout |
   |    = 1s        | |   Timeout=30s  |       |    = 2s      |    |    = 1s      |
   | 2. WriteTimeout | | 6. Connection  |       |              |    |              |
   |    = 2s        | |   IdleTimeout  |       |              |    |              |
   | 3. ReadTimeout  | |   = 60s       |       |              |    |              |
   |    = 3s        | |                |       |              |    |              |
   +----------------+ +----------------+       +--------------+    +--------------+

   ⚠ 핵심 원칙: "Inner Timeout < Outer Timeout"
   Service B(1s) < Service A(3s) < Client(5s) 이어야 함
   그렇지 않으면 Client는 5s 기다리지만 실제로는 Service B가 1s 만에 실패한 경우를 못 받음
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **CircuitBreaker (서킷 브레이커)** | 장애 격리 및 Fast Fail | Resilience4j `CircuitBreakerConfig`: `failureRateThreshold=50`, `slidingWindowType=COUNT_BASED/TIME_BASED`, `slidingWindowSize=100`, `minimumNumberOfCalls=10`, `waitDurationInOpenState=60s`, `permittedNumberOfCallsInHalfOpenState=5`, `automaticTransitionFromOpenToHalfOpenEnabled=true`. 슬라이딩 윈도우는 `ConcurrentHashMap<Long, AtomicReference<MutableGraphNode>>` 구조로 O(1) 갱신 |
| **Retry (재시도)** | 일시 장애 자동 복구 | Resilience4j `RetryConfig`: `maxAttempts=3`, `intervalFunction=IntervalFunction.ofExponentialRandomBackoff(100ms, 2.0, 0.5)` (initial 100ms, multiplier 2, jitter factor 0.5). `retryOnException`으로 `IOException`, `TimeoutException`, `5xx`만 재시도, `4xx`(클라이언트 오류)는 재시도 금지. **멱등성 보장 필수** |
| **Timeout (타임아웃)** | 동기 호출 자원 점유 상한 | OkHttp: `connectTimeout(1s)`, `readTimeout(3s)`, `writeTimeout(2s)`, `callTimeout(5s)`. gRPC: `KeepAliveTime`, `KeepAliveTimeout`. **전체 요청 체인에서 Inner < Outer** 관계 유지. Hystrix의 `execution.isolation.thread.timeoutInMilliseconds=3000` |
| **Bulkhead (벌크헤드, 격벽)** | 자원 풀 분리 | Resilience4j `BulkheadConfig`: `maxConcurrentCalls=20`, `maxWaitDuration=0`. **ThreadPoolBulkhead**: `maxThreadPoolSize=10`, `coreThreadPoolSize=5`, `queueCapacity=20`. 의존 서비스별 격리하여 한 서비스 장애
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 526 / 800

<- **이전**: [525. 백프레셔 흐름 제어 리액티브 스트림](/studynote/13_cloud_architecture/06_exam_summary/525_backpressure_flow_control_reactive_streams/)
**다음**: [527. 사이드카 패턴 프록시 서비스 확장](/studynote/13_cloud_architecture/06_exam_summary/527_sidecar_pattern_proxy_service_extension/) ->

---
