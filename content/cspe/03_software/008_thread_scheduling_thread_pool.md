---
title: "스레드 스케줄링·스레드 풀 (Thread Scheduling Thread Pool)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 8
---

# 📖 【암기용】 개념 완전 이해

> 목적: 스레드 스케줄링과 스레드 풀을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 스레드 실행 순서와 재사용 작업자 집합 관리
- **왜 필요한가**: 요청마다 스레드를 만들면 생성·전환·스택 메모리 비용이 커진다. 스레드 풀은 미리 만든 worker로 작업을 반복 처리한다.
- **핵심 직관**: 매 주문마다 직원을 새로 뽑지 않고, 대기 중인 직원에게 주문표를 배분하는 방식이다.

## 깊이 이해
- **배경·문제의식**: 멀티코어 서버는 수천 요청을 동시에 받지만 CPU core는 제한되어 있다. 스레드가 core보다 과도하게 많으면 context switch와 memory footprint가 늘고, 적으면 I/O 대기 중 CPU가 놀 수 있다.
- **작동 원리**: 요청은 work queue에 들어가고 worker thread가 꺼내 실행한다. CPU-bound는 core 수 근처, I/O-bound는 blocking ratio를 반영해 더 크게 잡는다. queue가 가득 차면 backpressure나 reject 정책이 필요하다.
- **비유**: 식당 주방에서 주문표 queue가 있고 요리사 pool이 순서대로 처리한다. 요리사가 너무 많으면 서로 부딪히고, 너무 적으면 주문표가 쌓인다.
- **구체 예시**: CPU-bound pool은 8 core에서 8~10개가 기준이고, I/O wait가 70%인 작업은 core/(1-blocking) 공식으로 약 26개까지 산정 가능하다.
- **흔한 오해·주의점**: thread pool 크기를 크게 하면 처리량이 계속 증가하지 않는다. 일정 지점 이후 lock contention, DB connection 고갈, queue 대기시간 증가가 발생한다.

## 연결 개념
- User/Kernel Thread: 스케줄링 주체와 커널 인식 범위
- Work Queue: 요청 버퍼와 backpressure 지점
- Starvation: worker 점유로 특정 작업이 처리되지 않는 현상

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 스레드 풀은 생성 비용 절감이 아니라 CPU core, blocking ratio, queue, starvation, backpressure를 함께 설계하는 주제이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스레드 스케줄링은 runnable thread에 CPU를 배정하는 정책이고, 스레드 풀은 worker thread를 재사용해 작업을 처리하는 실행 구조이다.
> 2. **가치**: thread 생성 비용과 context switch를 줄이고, work queue로 유입량을 제어한다.
> 3. **판단 포인트**: CPU-bound는 core 수, I/O-bound는 blocking ratio, 외부 자원은 connection pool과 함께 산정해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| thread 실행 모델 이해 확인 | user thread, kernel thread, 1:1/N:M 모델 | 스레드와 프로세스 혼동 |
| pool sizing 판단 확인 | core 수, blocking ratio, queue length | 큰 pool이 항상 처리량 증가라는 단정 |
| starvation·backpressure 확인 | work queue, reject policy, priority queue | queue 무한 증가 리스크 누락 |

> 요약: 이 문제는 thread 수가 아니라 CPU·I/O·queue·외부 자원 제한의 균형을 묻는다.

---

## Ⅰ. 개요 및 필요성

스레드 풀은 worker thread 재사용 구조이다.
스레드 생성·소멸과 과도한 context switch를 줄이고, work queue를 통해 요청 유입과 처리량을 조절한다.
서버 시스템에서는 CPU-bound, I/O-bound, DB connection 한계를 반영해 pool 크기와 queue 정책을 설계해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client Request -> Work Queue -> Worker Thread Pool
Worker -> CPU Task / Blocking I/O / DB Call
Metrics -> Pool Resize / Backpressure / Reject
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Work queue | 처리 대기 작업 저장 | bounded queue 권장 |
| Worker thread | queue에서 작업을 꺼내 실행 | reusable thread |
| Scheduler | runnable worker에 CPU 배정 | kernel thread 기준 |
| Rejection policy | queue 포화 시 처리 | drop, timeout, caller-runs |
| Monitor | pool·queue·latency 계측 | active count, queue wait |

> 요약: 스레드 풀은 queue, worker, scheduler, rejection, monitor가 결합된 실행 제어 구조이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 -> Work Queue enqueue
-> Idle Worker dequeue -> Task 실행
-> Blocking이면 다른 worker 실행
-> 완료 후 worker 반환
-> Queue 포화 시 backpressure/reject
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 요청을 bounded queue에 삽입 | queue depth |
| 2 | idle worker가 작업을 가져감 | active thread count |
| 3 | CPU-bound 또는 I/O-bound로 실행 | CPU utilization, wait ratio |
| 4 | 완료 후 worker를 pool에 반환 | task throughput |
| 5 | queue 포화 시 제한 정책 수행 | reject count, timeout |

> 요약: 스레드 풀은 작업을 queue로 흡수하고 worker 재사용과 포화 정책으로 처리량과 지연을 제어한다.

---

## Ⅳ. 특징

| 구분 | 스레드 풀 | 요청별 스레드 생성 | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 생성 비용 | 초기 생성 후 재사용 | 요청마다 stack/TCB 생성 | stack 512KB~1MB |
| 처리량 | pool 크기와 queue로 제한 | burst 시 thread 폭증 | Little's Law 적용 |
| 지연 | queue wait 발생 가능 | 생성 지연 발생 | p95 queue wait |
| 장애 범위 | worker 고갈·starvation | 메모리 고갈 | bounded queue 필수 |

> 요약: 스레드 풀은 생성 비용을 줄이는 대신 queue 대기와 worker 고갈을 관리해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | unbounded thread | bounded pool+queue | 메모리 상한, SLO |
| 비용/성능 | 생성 비용 반복 | 재사용, switch 통제 | p95 latency, TPS |
| 운영/위험 | 폭증 시 OOM | queue 포화 시 backpressure | reject 정책 명확성 |

> 요약: pool은 thread 수보다 queue 상한과 reject 정책이 운영 결과를 좌우한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| starvation | 긴 작업이 worker 점유 | priority queue, pool 분리 | task wait p99 |
| thread 폭증 | cached pool 무제한 생성 | maxPoolSize, semaphore | thread count |
| 외부 자원 고갈 | DB/API connection보다 worker 과다 | bulkhead, connection limit | pool wait, 429/timeout |

> 요약: starvation과 자원 고갈은 pool 분리, bounded 설정, bulkhead로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| pool 크기 | CPU-bound core×1~2, I/O-bound core/(1-B) | load test |
| queue 대기 | p95 queue wait 50ms 이하 | executor metric |
| 포화 | reject/timeout 비율 1% 이하 | metric, log |

> 요약: 스레드 풀은 pool size, queue wait, reject rate를 함께 측정해 조정한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. CPU-bound pool은 core×1~2, blocking ratio 70% I/O-bound pool은 core/(1-0.7) 기준으로 초기값 산정
2. work queue를 bounded로 두고 timeout 200ms, reject policy, circuit breaker를 설정해 무한 대기를 차단
3. DB, 외부 API, 파일 I/O별 pool을 분리하고 active count, queue wait, reject count를 Prometheus로 수집

**결론 (2줄):**
- 기술사 판단: CPU-bound는 작은 pool, I/O-bound는 blocking ratio 반영 pool, 혼합 workload는 bulkhead로 분리함
- 향후 방향: virtual thread와 async I/O가 확산되어도 queue 상한, backpressure, 외부 자원 제한은 계속 설계 기준이 됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "스레드 풀을 설명하시오" | enqueue, worker 실행, 반환 흐름 | 요청별 생성과 비교 |
| 요구사항 명시형 | "처리량 개선 방안을 제시하시오" | pool sizing과 backpressure | starvation·외부 자원 고갈 대응 |

> 요약: 설명형은 구조와 동작, 방안형은 sizing 공식과 포화 제어를 중심으로 작성한다.
