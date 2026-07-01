---
title: "가상 스레드 — Java Project Loom (Virtual Thread)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 27
---

# 📖 【암기용】 개념 완전 이해

> 목적: 가상 스레드를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Java 런타임이 OS 스레드보다 많은 경량 스레드를 관리하는 동시성 모델
- **왜 필요한가**: 서버 요청당 OS 스레드 1개를 배정하면 수천 동시 요청에서 메모리와 context switch 비용이 커진다. 가상 스레드는 blocking 코드 스타일을 유지하면서 동시 요청 수를 늘린다.
- **핵심 직관**: OS 스레드는 실제 좌석이고, 가상 스레드는 대기표이다. 작업이 I/O로 멈추면 좌석을 반납하고, 재개 시 다시 좌석을 배정받는다.

## 깊이 이해
- **배경·문제의식**: Java 서버는 thread-per-request 모델이 읽기 쉽지만 OS 스레드는 stack 메모리와 커널 스케줄링 비용을 가진다. 비동기 콜백은 스레드 수를 줄이나 코드 흐름과 디버깅이 어려워진다.
- **작동 원리**: 가상 스레드는 JVM이 관리하는 경량 스레드이며 carrier thread라는 OS 스레드 위에서 실행된다. blocking I/O 지점에서 continuation 상태를 저장하고 carrier thread를 다른 가상 스레드에 양보한다.
- **비유**: 콜센터 상담원이 고객 응답을 기다릴 때 전화를 붙잡고 있지 않고 대기 목록에 넣은 뒤 다른 고객을 처리하는 방식이다.
- **구체 예시**: Java 21에서 `Executors.newVirtualThreadPerTaskExecutor()`를 사용하면 요청 10,000개를 가상 스레드 10,000개로 표현하면서 carrier thread는 CPU 코어 수 근처로 유지할 수 있다.
- **흔한 오해·주의점**: 가상 스레드는 CPU 연산을 줄이지 않는다. CPU-bound 작업은 코어 수 제한을 받으며, synchronized 블록이나 native call에서 carrier thread pinning이 생길 수 있다.

## 연결 개념
- Project Loom — Java 가상 스레드와 structured concurrency 지원 프로젝트
- Continuation — 중단 지점의 실행 상태를 저장·복원하는 메커니즘
- Async I/O — 가상 스레드와 비교되는 비동기 동시성 모델

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 가상 스레드는 단순 스레드 수 증가가 아니라 carrier thread, continuation, blocking I/O unmount, structured concurrency 관점으로 설명한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 가상 스레드는 JVM이 관리하는 경량 스레드로, OS carrier thread에 mount/unmount되며 blocking I/O 중 carrier를 점유하지 않는다.
> 2. **가치**: thread-per-request 코드를 유지하면서 수천~수만 동시 I/O 요청을 낮은 메모리 사용량으로 처리한다.
> 3. **판단 포인트**: I/O-bound 워크로드, carrier pinning, thread-local 사용량, DB connection pool 한계를 함께 확인해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 현대 Java 동시성 이해 확인 | virtual thread, carrier thread, continuation | OS 스레드와 동일한 개념으로 설명 |
| blocking vs async 비교 확인 | blocking I/O unmount, 코드 단순성, event loop 차이 | CPU-bound 작업까지 개선된다고 단정 |
| 실무 도입 판단 확인 | pinning, pool size, observability | DB connection 수와 외부 의존성 병목 누락 |

> 요약: 이 문제는 가상 스레드의 실행 원리와 적용 한계를 I/O 동시성 관점으로 판단하도록 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 가상 스레드는 JVM 관리 경량 실행 단위이다.
- 배경: OS 스레드 기반 thread-per-request 모델은 수천 동시 요청에서 stack 메모리와 context switch/sec가 증가한다.
- 필요성: 가상 스레드는 blocking 코드 스타일을 유지하면서 I/O 대기 중 carrier thread를 반환해 동시 요청 수, heap 사용량, p95 latency 기준으로 확장성을 검증하게 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Request -> Virtual Thread -> Continuation -> Carrier Thread -> JVM Scheduler
  / Blocking I/O: unmount -> wait
  / Resume: mount -> continue
  / Structured Concurrency: task scope -> join / cancel
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Virtual Thread | 애플리케이션 작업 단위 | Java 21 표준 기능 |
| Carrier Thread | 실제 OS 스레드 | ForkJoinPool 기반 실행 |
| Continuation | 실행 상태 저장·복원 | blocking 지점에서 unmount |
| JVM Scheduler | 가상 스레드 배치 | work-stealing 활용 |
| Structured Concurrency | 관련 작업 생명주기 묶음 | join, cancel, timeout |

> 요약: 가상 스레드는 continuation으로 중단 상태를 저장하고 carrier thread를 재사용하는 JVM 스케줄링 구조이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 -> 가상 스레드 생성 -> carrier에 mount
  -> blocking I/O 발생 -> continuation 저장 / unmount
  -> I/O 완료 -> remount -> 응답 반환
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 요청마다 가상 스레드를 생성 | virtual thread count |
| 2 | JVM이 carrier thread에 mount | carrier utilization |
| 3 | blocking I/O에서 continuation 저장 후 unmount | pinned thread count |
| 4 | I/O 완료 이벤트 후 재개 | request p95 latency |
| 5 | structured scope로 하위 작업 join/cancel | timeout, cancellation count |

> 요약: 가상 스레드는 blocking I/O에서 carrier를 비워 다른 작업을 실행하고, 완료 후 저장된 continuation을 재개한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | 본 기술 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| Thread-per-request | OS 스레드 1개당 요청 1개 | 가상 스레드 요청 단위 생성 | 10,000 동시 I/O 요청 표현 |
| Event loop | callback/promise 기반 | blocking 코드 유지 | 디버깅 stack trace 유지 |
| 자원 | OS stack MB 단위 | 가상 스레드 stack 동적 확장 | heap 사용량 모니터링 |
| 한계 | CPU-bound 병렬화 | I/O-bound 대기 절감 | CPU 70% 이상 시 carrier 증설 효과 제한 |

> 요약: 가상 스레드는 I/O 대기 시간이 큰 서버에서 코드 단순성과 동시성을 함께 제공하나 CPU 병목은 해결하지 않는다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 고정 스레드 풀 | task당 virtual thread | 요청 수가 스레드 수보다 큰 I/O 서버 |
| 비용/성능 | OS thread context switch | JVM mount/unmount | p95 지연, heap 사용량 |
| 운영/위험 | callback 복잡도 | blocking 코드 유지 | pinning, thread-local, pool bottleneck |

> 요약: 가상 스레드는 I/O-bound 요청 처리에는 적합하나 외부 pool 크기와 pinning 여부를 함께 검증해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| carrier pinning | synchronized, native call, 일부 blocking | JFR pinning event 분석, lock 교체 | pinned duration p99 |
| DB 병목 | connection pool이 50개로 제한 | pool size 조정, backpressure | pool wait p95 |
| 메모리 증가 | thread-local 과다 사용 | thread-local 제거, scoped value 검토 | heap usage, GC pause |

> 요약: 도입 리스크는 pinning, 외부 pool, thread-local이며 JFR과 APM 지표로 검증한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 성능/지연 | p95 100ms 이하, 처리량 2배 이상 | k6, JMeter |
| 품질/동시성 | virtual thread 10,000개, error rate 0.1% 이하 | JFR, Micrometer |
| 운영/자원 | carrier CPU 70% 이하, GC pause p99 200ms 이하 | JFR, Prometheus |

> 요약: 가상 스레드 효과는 요청 지연, 동시성 수, carrier와 heap 자원 지표로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Java 21 이상에서 web request, outbound HTTP, DB I/O 중심 서비스를 가상 스레드 실행기로 전환하고 p95 지연을 부하 테스트로 측정한다.
2. JFR로 pinned thread event, heap 사용량, GC pause를 수집하고 synchronized 구간은 ReentrantLock 또는 비차단 구조로 조정한다.
3. DB connection pool, HTTP client pool, rate limit을 가상 스레드 수와 별도로 제한해 외부 시스템 과부하를 방지한다.

**결론 (2줄):**
- 기술사 판단: I/O-bound Java 서버는 가상 스레드, CPU-bound 계산은 고정 크기 executor와 병렬 알고리즘을 선택한다.
- 향후 방향: Java 동시성은 virtual thread와 structured concurrency를 결합해 thread-per-request 모델을 재정립한다.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "가상 스레드를 설명하시오" | mount/unmount, continuation 흐름 | 기존 스레드·이벤트 루프 비교 |
| 요구사항 명시형 | "도입 방안을 제시하시오", "비교하시오" | pinning, pool 병목, 관측 흐름 | I/O-bound 선택 기준과 지표 |

> 요약: 설명형은 JVM 원리를, 도입형은 pinning과 외부 자원 병목 통제를 중심으로 작성한다.
