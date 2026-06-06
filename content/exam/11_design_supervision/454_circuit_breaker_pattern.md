---
title: "Circuit Breaker Pattern Fault Isolation"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 마이클 니가드(Michael Nygard)가 저서 *Release It!*에서 제시한 안정성 디자인 패턴으로, 원격 서비스 호출 실패율이 임계치를 초과하면 즉시 호출을 차단(OPEN)하여 **연쇄 장애(Cascading Failure)와 Thread Pool 고갈**을 방지하는 FSM(Finite State Machine) 기반의 런타임 가드(Guard)이다.
> 2. **가치**: 장애 전파 차단으로 **MTTR(Mean Time To Recovery)을 60~80% 단축**하고, Fallback 전략과 결합하여 핵심 거래의 부분 가용성(Degraded Service)을 보장하며, 슬라이딩 윈도우(Sliding Window) 기반의 정량적 임계치로 오탐(False Positive)을 최소화한다.
> 3. **판단 포인트**: Count-Based vs Time-Based 슬라이딩 윈도우 선택, **Half-Open 상태의 동시성 제어**(Test 요청의 단일성 보장), 폴백(Fallback) 정책의 비즈니스 우선순위 결정, Bulkhead·Retry·Timeout·Rate Limiter와의 **조합 순서(Composition Order)**가 핵심 설계 판단 기준이다.

---

## Ⅰ. 개요 및 필요성

마이크로서비스 아키텍처(MSA) 환경에서 서비스 간 호출은 일반적으로 동기식 HTTP/gRPC 통신에 의존한다. 이때 하류(Downstream) 서비스가 응답 지연(Latency Spike) 또는 에러를 반환하기 시작하면, 상류(Upstream) 서비스의 **Tomcat/HTTP Client의 작업 스레드(Worker Thread)가 점유된 채 해제되지 못해** 결국 Thread Pool이 고갈된다. 고갈된 스레드 풀은 신규 요청조차 처리하지 못해 자기 자신마저 장애 상태로 빠지는 **자기 연쇄 장애(Self-Induced Cascading Failure)**를 유발한다. Netflix가 2011년 AWS 리전 장애에서 겪은 경험(데이터베이스 Connection Pool 고갈 -> 결제/추천 서비스 동시 마비)이 이를 대표적으로 보여준다.

서킷 브레이커는 전기 회로의 퓨즈(Fuse)·차단기 개념을 차용하여, **통계적 실패율**을 기반으로 호출 경로 자체를 물리적으로 차단하여 Thread Pool 자원을 보호한다. 전통적인 단순 재시도(Retry) 패턴은 실패 시 즉시 무한 재시도로 오히려 장애를 가중시키는데, 서킷 브레이커는 **"빠른 실패(Fail Fast) + 자동 복구 시도"**라는 두 가지 가치를 동시 제공한다.

```text
                    [서킷 브레이커 미적용 vs 적용 비교]

  [미적용: 무방비 호출]                          [적용: 가드 호출]

  Client --요청---> Service A --요청---> Service B     Client --요청---> [CB] ---> Service A --요청---> Service B
                      |                       |                          |             |                       |
                      | <----Timeout(30s)------+                          |             | <----Timeout(3s)-------+
                      | 스레드 점유 유지 ❌      |                          |             |   스레드 즉시 해제 ✅   |
                      v                       |                          v             v                       |
              [ThreadPool 고갈]                |                  [정상 서비스 제공]    [실패율 60% 감지]           |
                      |                       |                                            |                       |
                      v                       |                                            v                       |
              [Client-500 에러 폭주]          |                              OPEN 상태: 즉시 Fallback 반환        |
                                              |                              (재고 기본값/캐시/큐잉/429)          |
                                              |                                            |                       |
                                              |                                            v                       |
                                              |                                    60초 후 HALF_OPEN             |
                                              |                                    테스트 호출 1건 허용              |

  ※ 핵심 차이: 스레드 점유 시간(30s -> 수 ms), 자원 고갈 전파 차단, Fail-Fast 응답
```

기존의 **단순 타임아웃 + 재시도(Retry)** 조합은 하류 서비스의 부분 장애(Partial Failure) 시 스레드 자원이 일시적으로 묶이는 문제를 근본적으로 해결하지 못한다. Netflix의 Hystrix는 이 문제를 해결하기 위해 2012년 출시되어 Thread Pool 격리 + 서킷 브레이커 + Dashboard를 통합 제공했으나, 2018년 Reactive 모델과 함수형 라이브러리의 등장으로 Maintenance Mode 전환 후 **Resilience4j**가 사실상의 표준(de facto standard) 라이브러리로 자리 잡았다.

- **📢 섹션 요약 비유**: 🎬 **호텔 방화 셔터(Fire Shutter)**와 같다. 한 층에서 화재(장애)가 발생하면 자동으로 셔터가 내려와 불이 옆 층·다른 객실로 번지지 않게 막고, 소방 시스템이 정상화됐는지 확인한 후(Pull Station 테스트) 다시 셔터를 올린다.

---

## Ⅱ. 아키텍처 및 핵심 원리

서킷 브레이커는 **상태 머신(State Machine)**과 **슬라이딩 윈도우(Sliding Window)** 두 핵심 메커니즘으로 구성된다. 모든 호출 결과(성공/실패/타임아웃)는 슬라이딩 윈도우에 기록되며, 윈도우 내의 통계치로 상태 전이(Transition)가 결정된다.

```text
                          [서킷 브레이커 상태 전이 다이어그램 (FSM)]

                            +-------------------------------------+
                            |   CLOSED (정상 - 모든 요청 허용)      |
                            |   • 요청 통과 -> 원격 호출 실행          |
                            |   • 슬라이딩 윈도우에 결과 기록        |
                            |   • 실패율 < 임계치(threshold) 유지    |
                            +--------------+----------------------+
                                           |
                                           |  실패율 ≥ failureRateThreshold
                                           |  (예: 최근 100건 중 50% 실패)
                                           |  AND 최소 호출수 ≥ minimumNumberOfCalls
                                           v
                            +-------------------------------------+
                            |   OPEN (차단 - 즉시 실패 반환)         |
                            |   • 원격 호출을 수행하지 않음          |
                            |   • Fallback 로직 즉시 실행            |
                            |   • resetTimeout 동안 대기             |
                            |   • 카운터 / 메트릭 발행 (Prometheus) |
                            +--------------+----------------------+
                                           |
                                           |  resetTimeout 경과
                                           |  (예: 60초 후)
                                           v
                            +-------------------------------------+
                            |   HALF_OPEN (반개방 - 복구 테스트)     |
                            |   • permittedNumberOfCalls 만큼만 통과 |
                            |   • 동시에 1건 또는 N건의 테스트 호출   |
                            |   • 결과로 CLOSED 또는 OPEN 결정      |
                            +--------------+----------------------+
                                           |
                            +--------------+----------------------+
                            |                                     |
                            v                                     v
                  +----------------------+         +----------------------+
                  | 성공률 ≥ 임계치        |         | 실패율 ≥ 임계치        |
                  | -> CLOSED 전이          |         | -> OPEN 전이            |
                  | (윈도우/카운터 리셋)    |         | (resetTimeout 재시작)  |
                  +----------------------+         +----------------------+

  ※ Resilience4j의 permittedNumberOfCallsInHalfOpenState 기본값 = 10
  ※ slidingWindowSize 기본값 = 100 (count-based)
  ※ failureRateThreshold 기본값 = 50%
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **상태 머신 (State Machine)** | CLOSED/OPEN/HALF_OPEN 3상태 관리 및 전이 규칙 적용 | `@CircuitBreaker(name="payment", fallbackMethod="fallback")` 선언, AtomicReference 기반 Lock-Free 상태 전이, Half-Open 시 단일 스레드만 테스트 수행 |
| **슬라이딩 윈도우 (Sliding Window)** | 최근 N개 호출의 성공/실패/지연 통계 집계 | **Count-Based**: 최근 100건(`slidingWindowType=COUNT_BASED`), **Time-Based**: 최근 60초(`slidingWindowType=TIME_BASED`); 내부적으로 Ring Buffer + AtomicLongArray 또는 Bucket 기반 카운터 사용 |
| **이벤트 리스너 (Event Listener)** | 상태 전이 및 호출 결과를 외부 시스템에 통지 | `onStateTransition`, `onError`, `onSlowCallRateExceeded` 이벤트, Micrometer/Prometheus 메트릭 자동 발행, Slack/PagerDuty Webhook 연동 |
| **Fallback 실행기 (Fallback Executor)** | OPEN 또는 호출 실패 시 대체 경로 제공 | 정적 기본값(Default Value), 캐시 조회(Stale Cache), 다른 정상 서비스 호출(Standby Service), 큐잉(Kafka/MQ 적재), **차등 응답**(부분 성공 데이터 반환) |
| **Slow Call Detector (확장)** | 타임아웃은 아니지만 느린 호출도 장애로 간주 | `slowCallDurationThreshold`(예: 2초) 초과 시 slowCall로 카운트, `slowCallRateThreshold`(예: 80%) 초과 시 OPEN 전이 - Slow Failure 방지 |

### 핵심 파라미터 및 알고리즘 (Resilience4j 기준)

```
주요 설정 파라미터:
  - failureRateThreshold        : 50.0 (%)        // 실패율 임계치
  - slowCallRateThreshold       : 100.0 (%)       // 느린 호출 임계치
  - slowCallDurationThreshold   : 60000 (ms)      // '느림'의 기준
  - slidingWindowType           : COUNT_BASED     // 또는 TIME_BASED
  - slidingWindowSize           : 100             // 카운트 또는 초(seconds)
  - minimumNumberOfCalls        : 100             // 통계 유효 최소 호출 수
  - permittedNumberOfCallsInHalfOpenState : 10   // 테스트 호출 허용 수
  - waitDurationInOpenState     : 60000 (ms)      // OPEN 유지 시간
  - automaticTransitionFromOpenToHalfOpenEnabled : true  // 자동 전이 활성화
  - recordExceptions            : [IOException, TimeoutException, ...]  // 카운트 대상
  - ignoreExceptions            : [BusinessException]  // 무시(예: 4xx 비즈니스 에러)
```

**장애 판정 알고리즘**: 슬라이딩 윈도우 내 `failureRate = (failedCalls / totalCalls) × 100` 이 임계치를 초과하고, `totalCalls >= minimumNumberOfCalls` 조건을 동시에 만족할 때 CLOSED -> OPEN 전이가 발생한다. 이 **이중 조건(Double Guard)**은 트래픽이 적은 시점에 소수의 실패로 오탐되는 문제를 방지한다. 또한 `recordExceptions` / `ignoreExceptions`로 **4xx 비즈니스 예외는 실패가 아닌 정상 흐름**으로 처리하여, 사용자 입력 오류로 서킷이 열리는 것을 막는다.

**Half-Open 동시성 제어**: 100개의 스레드가 동시에 OPEN 만료 시점을 발견하여 모두 테스트 호출을 보내는 **Thundering Herd 문제**를 방지하기 위해, `waitDurationInOpenState` 만료 시점의 **첫 번째 호출자만 Half-Open 진입 트리거** 권한을 얻고, 나머지는 OPEN 상태를 계속 유지한다(`automaticTransitionFromOpenToHalfOpenEnabled`가 활성화된 경우 내부 스케줄러가 자동 전이).

- **📢 섹션 요약 비유**: 🚦 **신호등(Traffic Light)**과 같다. 평소엔 초록불(CLOSED)이라 차량(요청)이 다 지나가지만, 일정 시간 교통 정체(실패율 증가)가 감지되면 빨간불(OPEN)로 바뀌어 진입을 막고, 정체 해소 여부를 소수의 차량(테스트 호출)으로 먼저 확인 후 다시 초록불로 바꾼다.

---

## Ⅲ. 비교 및 연결

서킷 브레이커는 단독 사용보다 **안정성 패턴(Stability Pattern) 군**과 조합되어 사용된다. 각 패턴의 역할 분담과 조합 시 주의사항이 아키텍처의 성패를 가른다.

| 구분 | 서킷 브레이커 (Circuit Breaker) | 재시도 (Retry) | 벌크헤드 (Bulkhead) | 속도 제한 (Rate Limiter) | 타임아웃 (Timeout) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **핵심 목적** | 장애 전파 차단(빠른 실패) | 일시 장애 극복(투명한 복구) | 자원 격리(Thread Pool 분할) | 호출량 통제(과부하 방지) | 무한 대기 방지 |
| **동작 시점** | 호출 전/후 (사후 판단) | 호출 실패 후 | 호출 전 (격리 컨테이너 할당) | 호출 전 (토큰 소비) | 호출 중 (시간 제한) |
| **주 파라미터** | failureRate, windowSize | maxAttempts, backoff | maxConcurrentCalls, queueCapacity | limitForPeriod, limitRefreshPeriod | timeoutDuration |
| **상태 보유** | 3-State FSM (CLOSED/OPEN/HALF_OPEN) | Stateless (Stateless) 또는 Idempotency Key | 자원 풀(Pool) 기반 | 토큰 버킷(Token Bucket) | 없음 |
| **조합 위치** | 가장 바깥쪽 (호출 차단) | Retry -> 서킷 브레이커 -> 원격 | 서킷 내부 또는 외부에 격리 풀 | 가장 바깥 (트래픽 차단) | 모든 원격 호출 직전 |
| **대표 구현** | Resilience4j, Hystrix, Envoy | Spring Retry, Resilience4j-Retry | Resilience4j-Bulkhead, Semaphore | Resilience4j-RateLimiter, Guava RateLimiter | Resilience4j-TimeLimiter
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 454 / 600

<- **이전**: [453. 이벤트 소싱 CQRS 설계 패턴](/studynote/11_design_supervision/06_exam_summary/453_event_sourcing_cqrs)
**다음**: [455. 사가 패턴 분산 트랜잭션 보상](/studynote/11_design_supervision/06_exam_summary/455_saga_pattern/) ->

---
