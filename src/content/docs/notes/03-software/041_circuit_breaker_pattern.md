---
sidebar:
  order: 41
  label: "041. 서킷 브레이커 패턴 (Circuit Breaker Pattern)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "서킷 브레이커 패턴 (Circuit Breaker Pattern)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 41
extra:
  question_no: "041"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "서킷 브레이커는 연쇄 장애 차단 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Circuit Breaker Pattern**: 전기 회로의 누전 차단기(Circuit Breaker) 원리를 소프트웨어에 적용하여, 원격 서비스 호출 실패율이 일정 임계치(Threshold)를 초과 시 차단기를 내려(Open) 호출을 즉시 차단함으로써 타 서비스로의 Cascading Failure를 방지하는 장애 격리 패턴.
- **Cascading Failure (연쇄 장애)**: 하나의 마이크로서비스 장애(지연/다운)가 호출측 서비스의 스레드 및 커넥션 풀을 강제 고착(Blocking)시켜 시스템 전체로 마비가 연쇄 전파되는 현상.
- **Fallback**: 서킷 브레이커가 Open 상태이거나 원격 호출 실패 시, 에러 메세지 대신 예비 캐시 데이터나 우회(Fallback) 응답값을 반환하여 유저 경험을 보존하는 기법.

</details>

- 정의/개념: 원격 호출의 연쇄 장애(Cascading Failure)를 차단하기 위해 타깃 서비스의 에러 비율/지연율을 모니터링하여 차단기(Open/Closed/Half-Open)를 자동 제어하는 **Circuit Breaker Pattern**
- 배경/필요성: 분산 MSA 환경에서 단일 서비스 지연으로 인한 스레드 고갈(Thread Exhaustion) 및 전체 시스템 다운 차단 요구성

#### 한줄 요약

- 실패 임계치 차단과 시험 호출 기반 서킷 브레이커가 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Closed State**: 차단기가 닫힌 정상 상태로, 모든 외부 원격 호출을 허용하며 호출 실패율 및 지연 시간을 sliding window 큐에 누적 모니터링.
- **Open State**: 실패율이 임계치를 초과하여 차단기가 열린 장애 차단 상태로, 원격 호출을 즉시 거부하고 Fallback 응답을 즉시 반환.
- **Half-Open State**: 일정 쿨다운 타임(Cooldown Time) 경과 후 차단기를 반쯤 열어 제한된 소량의 시험 호출(Probe Request)을 전송, 복구 성공 여부를 타핑 검증하는 상태.

</details>

- 3대 상태 전이 메커니즘 (**Closed $\rightarrow$ Open $\rightarrow$ Half-Open $\rightarrow$ Closed**)
- Sliding Window (Count-based / Time-based) 기반 실패 임계치 자동 판정
- **Fallback 메커니즘** 결합 및 **Cascading Failure (연쇄 장애)** 차단

#### 한줄 요약

- Closed, Open, Half-Open 상태 전이가 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Sliding Window**: 최근 $N$개의 호출 수(Count-based) 또는 최근 $N$초(Time-based) 동안의 원격 호출 성공/실패 수치를 지속적으로 유지하는 윈도우 슬라이딩 모니터링 큐.

</details>

```text
[호출 인터셉터] -------- [실패 측정 창] -------- [상태 기계]
                                                     /     \
                                                    /       \
                                         [복구 제어기]     [대체 응답 처리기]
```

선의 의미: 원격 호출 인터셉터가 Sliding Window에 런타임 수치를 수집하고, State Machine이 조건 충족 시 Open/Closed 상태를 전이하며 Fallback을 인가하는 구조.

| 구성요소 | 핵심 역할 및 주요 파라미터 |
|:---|:---|
| **Closed State** | 모든 호출 수용, `failureRateThreshold` (e.g. 50%) 초과 시 Open 전이 |
| **Open State** | 호출 즉시 차단(Fallback 실행), `waitDurationInOpenState` (e.g. 10s) 쿨다운 대기 |
| **Half-Open State**| `permittedNumberOfCallsInHalfOpenState` (e.g. 3회) 시험 호출 전송 복구 검증 |
| **Sliding Window** | `slidingWindowSize` (e.g. 100회/10초) 설정으로 민감도(Sensitivity) 조율 |
| **Fallback Handler**| Open 또는 Exception 발생 시 대체 캐시/디폴트 데이터 반환 로직 |

#### 한줄 요약

- 호출 인터셉터, 상태 기계, 대체 응답이 차단과 복구를 연결한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Probe Request (시험 호출)**: Half-Open 상태에서 타깃 서비스가 정상 복구되었는지 여부를 사전에 테스트하기 위해 전송하는 최소한의 한정된 호출.

</details>

```text
┌──────────────────────────────┐
│ Closed (정상 통신)           │◀────────────────┐
└──────────────┬───────────────┘                 │
               ▼ (실패율 임계치 초과)            │ (시험 호출 성공)
┌──────────────────────────────┐                 │
│ Open (호출 즉시 차단/Fallback)│                 │
└──────────────┬───────────────┘                 │
               ▼ (Cool-down 타임아웃)            │
┌──────────────────────────────┐                 │
│ Half-Open (시험 호출 전송)   ├─────────────────┘
└──────────────┬───────────────┘
               ▼ (시험 호출 실패)
         [Open 재전이]
```

### 동작 원리

1. **Closed**: 정상 상태로 모든 원격 호출 수행하며 Sliding Window 내 에러율 모니터링.
2. **Open 전이**: 실패율/지연율 임계치(e.g., 50% 이상) 초과 시 **Open State**로 트립(Trip) 되어 원격 호출 거부 및 **Fallback** 실행.
3. **Cool-down 대기**: 지정된 대기 시간(e.g., 10초) 동안 차단 상태 유지 및 타깃 서비스 복구 여유 부여.
4. **Half-Open 전이**: 대기 완료 후 **Half-Open State**로 전이하여 3~5회의 제한된 **Probe Request** 인가.
5. **Closed 복귀 / Open 유지**: 시험 호출 100% 성공 시 **Closed** 복귀, 1건이라도 실패 시 다시 **Open**으로 재트립.

#### 한줄 요약

- 결과 집계•임계 판정과 Half-Open 시험 판정의 상태 순환이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Resilience4j vs Hystrix**: Hystrix는 Netflix에서 개발한 구형 서킷 브레이커(Thread-pool 위주, deprecated), Resilience4j는 함수형 Java 8+ / Reactor 중심의 가볍고 현대적인 표준 라이브러리.

</details>

| 비교 항목 | Resilience4j (현대 표준) | Netflix Hystrix (구형) |
|:---|:---|:---|
| 구현 방식 | Java 8+ Functional / Lambda / AOP 위주 | Thread Pool 및 Semaphore 격리 중심 |
| 타 모듈 결합 | RateLimiter, Bulkhead, Retry 등 유연한 조합 | 모놀리식 라이브러리 덩어리 |
| 유지보수 상태 | **현재 커뮤니티 활발 유지보수중** | **Deprecated (개발 중단)** |
| 런타임 오버헤드 | 메모리 foot-print 수 KB (매우 경량) | 쓰레드 생성 오버헤드 큼 |

#### 한줄 요약

- 일시 오류는 재시도, 지속 장애는 서킷 브레이커가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Bulkhead Pattern (격벽 패턴)**: 선박의 격벽 구조처럼 서비스별로 스레드 풀(Thread Pool) 또는 세마포어를 분리 지정하여, 특정 서비스 장애 시 타 스레드 풀이 고갈되는 것을 물리적으로 막는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 적은 호출 표본 수에서 우연한 에러로 차단기 오작동 | `minimumNumberOfCalls` (e.g. 최소 20회 이상) 설정 | 오차단 방지 |
| 서킷 브레이커 Open 시 클라이언트에 raw 500 에러 노출 | **Fallback Method** 구현 (로컬 캐시/빈 객체 반환) | 사용자 경험(UX) 보존 |
| 특정 서비스의 독점이 타 스레드 풀을 고갈시킴 | **Bulkhead Pattern (스레드 풀 분리)** 혼용 인가 | 자원 고갈 물리 차단 |

> 사례: Spring Boot 3 + **Resilience4j CircuitBreaker** 모듈 연동 및 Prometheus 모니터링

#### 한줄 요약

- 최소 표본, 검증 동시 수, 최대 노후도를 통제한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **서킷 브레이커 설계 기준(Circuit Breaker Design Standards)**: 서비스 중요도, 원격 타임아웃 쿼터 및 Fallback 데이터 보유 유무에 기반한 수립 체계.

</details>

- **서킷 브레이커 설계 기준**에 따라 MSA 시스템 구축 시 **Resilience4j CircuitBreaker + Fallback + Bulkhead** 필수 세팅

#### 한줄 요약

- 오류 지속성과 지연 예산을 함께 평가하는 것이 핵심이다.
