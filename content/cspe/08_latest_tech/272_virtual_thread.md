---
title: "가상 스레드 (Virtual Thread)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 272
---

# 📖 【암기용】 개념 완전 이해

> 목적: 가상 스레드를 OS 스레드보다 작은 비용으로 대량의 blocking 작업을 처리하기 위한 JVM 수준 스레드로 이해하게 만든다.

## 한눈에
- **개요**: JVM이 관리하는 경량 스레드로, blocking I/O 중심 서버에서 요청당 스레드 모델을 유지하게 해주는 동시성 기술
- **왜 필요한가**: 플랫폼 스레드는 OS 스레드와 연결되어 메모리와 스케줄링 비용이 크므로 동시 접속이 늘면 thread pool 병목이 발생한다.
- **핵심 직관**: 책상 수는 적어도 서류 작업자가 기다리는 동안 자리를 비우게 해 더 많은 작업자가 순서를 나눠 쓰는 방식이다.

## 깊이 이해
- **배경·문제의식**: 기존 Java 서버는 blocking I/O를 다루기 위해 thread pool 크기를 제한했고, 많은 동시 요청은 대기열과 timeout을 만들었다.
- **작동 원리**: 가상 스레드는 JVM scheduler가 carrier platform thread 위에서 실행하며, 대부분의 blocking I/O 시점에 carrier를 반납하고 나중에 재개된다.
- **비유**: 상담원이 고객 답변을 기다리는 동안 전화기를 붙잡고 있지 않고, 대기표를 남긴 뒤 다른 상담을 처리하는 방식이다.
- **구체 예시**: Java 21에서 `Executors.newVirtualThreadPerTaskExecutor()`로 요청마다 가상 스레드를 생성해 JDBC·HTTP 호출 중심 업무를 단순 blocking 코드로 작성한다.
- **흔한 오해·주의점**: 가상 스레드는 CPU 연산을 줄이지 않는다. CPU-bound 작업은 코어 수가 한계이며, synchronized block과 native call은 carrier pinning을 만들 수 있다.

## 연결 개념
- Reactive System — 비동기·메시지 기반 확장 모델과 비교되는 동시성 접근
- Structured Concurrency — 가상 스레드 작업 묶음을 생명주기 단위로 관리하는 방향
- Cloud Native Observability — 대량 스레드의 trace와 thread dump 관측 필요

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: 가상 스레드는 blocking I/O 동시성 문제를 JVM scheduler와 carrier thread로 해결하지만 CPU-bound 해법은 아니다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Virtual Thread는 JVM이 관리하는 경량 스레드로 요청당 스레드 모델을 높은 동시성에서 유지하게 하는 기술임.
> 2. **가치**: blocking I/O 시 carrier thread를 반납해 thread pool 고갈과 callback 기반 코드 복잡도를 줄임.
> 3. **판단 포인트**: I/O-bound 서버에는 적합하고 CPU-bound, synchronized pinning, 제한된 DB connection pool에는 별도 통제가 필요함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Java 동시성 변화 이해 확인 | JVM scheduler, carrier thread, blocking I/O | OS 스레드 무제한 생성으로 설명 |
| Reactive와 비교 확인 | 단순 blocking 코드 vs non-blocking pipeline | Reactive 불필요를 모든 경우로 단정 |
| 적용 리스크 판단 확인 | pinning, connection pool, CPU-bound | 처리량이 자동 증가한다고 과장 |

> 요약: 이 문제는 가상 스레드가 I/O 대기 비용을 줄이는 동시성 모델이지 CPU 연산 가속 기술이 아님을 구분하게 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: JVM 경량 스레드 동시성
- 배경: 플랫폼 스레드는 OS 스레드와 매핑되어 대량 blocking 요청에서 pool 고갈과 대기열을 만든다.
- 필요성: 요청당 스레드 코드 구조를 유지하면서 I/O-bound 동시성을 확대해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Application Task -> Virtual Thread -> JVM Scheduler -> Carrier Platform Thread
Virtual Thread -> Blocking I/O -> Unmount / Park -> Resume -> Result
Monitoring -> Thread Dump / JFR -> Pinning / Latency 확인
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Virtual Thread | 애플리케이션 작업 실행 단위 | Java 21 정식 기능 |
| Carrier Thread | 실제 OS 스레드와 매핑 | JVM scheduler가 공유 |
| Scheduler | 가상 스레드 배치와 재개 | blocking I/O 시 unmount |
| Observability | pinning과 지연 추적 | JFR, thread dump |

> 요약: 가상 스레드는 JVM scheduler가 carrier thread 위에서 작업을 배치하고 I/O 대기 시 carrier를 다른 작업에 배정한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 -> virtual thread 생성 -> blocking 코드 실행
-> I/O 대기 발생 -> carrier 반납 -> I/O 완료
-> virtual thread 재개 -> 응답 반환
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 요청 또는 작업마다 가상 스레드 생성 | thread creation failure 0건 |
| 2 | 업무 로직을 blocking 스타일로 실행 | 코드 구조 단순성 |
| 3 | I/O 대기 시 JVM이 virtual thread를 park | carrier utilization |
| 4 | I/O 완료 후 virtual thread 재개 | p95 latency, pinning event |

> 요약: 가상 스레드는 I/O 대기 중 carrier를 반납해 같은 OS 스레드 자원으로 더 많은 대기 작업을 수용한다.

---

## Ⅳ. 특징

| 구분 | Platform Thread | Virtual Thread | 판단 기준 |
|:---|:---|:---|:---|
| 관리 주체 | OS scheduler | JVM scheduler | Java 21 이상 |
| 비용 구조 | OS stack·context 비용 | JVM 관리 stack | 동시 요청 수 |
| 코드 모델 | blocking 가능, pool 제한 | 요청당 blocking 코드 가능 | I/O-bound 업무 |
| 한계 | thread pool 고갈 | pinning, 외부 자원 pool 한계 | DB connection 수 |

> 요약: 가상 스레드는 I/O 대기 동시성을 다루는 도구이며 외부 connection pool과 CPU 코어 한계는 그대로 남는다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Reactive non-blocking | Virtual Thread blocking | 코드 복잡도와 I/O 특성 |
| 비용/성능 | event loop, callback chain | 요청당 thread | p95 지연과 메모리 |
| 운영/위험 | backpressure 명시 | pool 제한 별도 필요 | DB·HTTP client 설정 |

> 요약: 단순 I/O 서버는 가상 스레드, 스트리밍·backpressure 중심 파이프라인은 Reactive가 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Carrier Pinning | synchronized block, native call | ReentrantLock, JFR 분석 | pinned thread event |
| DB 병목 | connection pool 크기 제한 | semaphore, pool sizing | connection wait time |
| CPU 포화 | CPU-bound 작업 증가 | fixed executor 분리 | CPU utilization |

> 요약: 가상 스레드 리스크는 pinning, 외부 pool 병목, CPU 포화이며 JFR과 pool 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연 | p95 응답시간 SLA 이내 | load test |
| pinning | pinned event 지속 발생 없음 | JFR |
| 자원 | heap·connection wait 기준 이내 | APM, pool metric |

> 요약: 가상 스레드 도입은 응답 지연, pinning, 외부 자원 대기 시간을 함께 확인해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Java 21 이상에서 I/O-bound API부터 `newVirtualThreadPerTaskExecutor`를 적용하고 baseline 부하시험과 비교함.
2. DB connection pool, HTTP client pool, rate limit을 semaphore로 제한해 가상 스레드 수와 외부 자원 수를 분리함.
3. JFR pinning event, thread dump, p95 latency를 배포 전후로 비교해 synchronized 구간을 제거함.

**결론 (2줄):**
- 기술사 판단: blocking I/O 중심 Java 서비스는 가상 스레드를 선택하고, CPU-bound 계산과 backpressure 중심 스트림은 별도 실행 모델을 선택함.
- 향후 방향: 가상 스레드는 structured concurrency와 결합되어 Java 서버의 기본 동시성 모델로 자리 잡음.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "가상 스레드를 설명하시오" | carrier 반납과 재개 흐름 | platform thread 대비 차이 |
| 요구사항 명시형 | "Java 서버 동시성 개선 방안을 제시하시오" | pool·pinning 점검 절차 | Reactive와 선택 기준 |

> 요약: 설명형은 JVM 동작을, 방안형은 외부 자원 통제와 pinning 검증을 중심으로 작성한다.
