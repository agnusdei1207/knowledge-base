---
title: "비동기 I/O·이벤트 루프 (Async I/O Event Loop)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 28
---

# 📖 【암기용】 개념 완전 이해

> 목적: 비동기 I/O와 이벤트 루프를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: I/O 완료를 기다리는 동안 스레드를 막지 않고 이벤트로 처리하는 동시성 모델
- **왜 필요한가**: 네트워크 서버는 대부분 시간을 소켓 응답 대기에 쓴다. 요청마다 스레드를 묶어두면 스레드 수와 메모리 사용량이 커진다.
- **핵심 직관**: 음식 주문 후 카운터 앞에서 기다리지 않고 진동벨을 받아 자리에 앉아 있다가 알림이 오면 음식을 받는 방식이다.

## 깊이 이해
- **배경·문제의식**: blocking I/O는 코드 흐름이 단순하지만 대기 중 스레드가 묶인다. 비동기 I/O는 non-blocking socket과 이벤트 통지로 적은 수의 스레드가 많은 연결을 처리한다.
- **작동 원리**: 애플리케이션은 소켓을 non-blocking으로 설정하고 epoll, kqueue, IOCP 같은 커널 이벤트 통지기에 관심 이벤트를 등록한다. 이벤트 루프는 준비된 이벤트를 가져와 callback, promise, coroutine을 실행한다.
- **비유**: 안내 데스크가 모든 손님 앞에서 대기하지 않고 번호표와 알림판으로 준비 완료된 손님만 호출하는 구조이다.
- **구체 예시**: Node.js는 libuv 이벤트 루프와 epoll/kqueue/IOCP를 사용한다. Nginx는 worker 프로세스와 event-driven 구조로 수만 keep-alive 연결을 처리한다.
- **흔한 오해·주의점**: 비동기 I/O는 CPU 연산을 분산하지 않는다. 이벤트 루프 스레드에서 긴 CPU 작업을 수행하면 전체 연결의 p99 지연이 증가한다.

## 연결 개념
- epoll/kqueue/IOCP — OS별 이벤트 통지 인터페이스
- callback/promise/coroutine — 비동기 완료 처리 방식
- backpressure — 생산 속도가 소비 속도를 넘지 않게 조절하는 제어

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 이벤트 루프는 단순 callback 구조가 아니라 non-blocking I/O, readiness/completion 통지, backpressure, CPU 작업 분리까지 포함해 설명한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 비동기 I/O·이벤트 루프는 I/O 대기 중 스레드를 점유하지 않고 커널 이벤트 통지로 완료 작업을 실행하는 동시성 구조이다.
> 2. **가치**: 적은 worker로 많은 socket 연결을 처리하고, 네트워크 대기 시간이 큰 서비스의 메모리 사용량과 context switch를 줄인다.
> 3. **판단 포인트**: epoll/kqueue/IOCP 차이, callback/promise 처리, 이벤트 루프 블로킹, backpressure를 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 비동기 I/O 원리 확인 | non-blocking, event registration, event dispatch | 멀티스레드와 같은 개념으로 설명 |
| 플랫폼별 통지 방식 확인 | epoll, kqueue, IOCP, libuv | Linux 전용으로만 서술 |
| 운영 리스크 판단 확인 | event loop lag, backpressure, CPU offload | callback 구조만 쓰고 장애 지표 누락 |

> 요약: 이 문제는 비동기 I/O의 커널 통지 흐름과 이벤트 루프 운영 리스크를 함께 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 비동기 I/O는 대기를 이벤트로 전환한다.
- 배경: blocking I/O는 요청 수만큼 스레드가 대기하지만, 이벤트 루프는 epoll, kqueue, IOCP로 준비된 I/O만 처리한다.
- 필요성: 대규모 연결 서버는 10,000 connection 부하, loop lag, p99 latency 기준으로 연결당 스레드 비용을 줄여야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client Socket -> Non-blocking FD -> Event Demultiplexer
  -> Event Loop -> Callback / Promise / Coroutine -> Response
  -> Backpressure -> Queue / Buffer Control
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Non-blocking FD | 즉시 반환되는 소켓·파일 디스크립터 | EAGAIN 처리 필요 |
| Event Demultiplexer | 준비된 이벤트 목록 반환 | epoll, kqueue, IOCP |
| Event Loop | 이벤트 수신·콜백 실행 | 단일 루프 블로킹 주의 |
| Callback/Promise | 완료 후 실행 로직 표현 | exception propagation 관리 |
| Backpressure | 생산·소비 속도 조절 | queue length, high watermark |

> 요약: 비동기 I/O는 non-blocking FD, OS 이벤트 통지기, 이벤트 루프, 완료 처리, backpressure로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
소켓 생성 -> non-blocking 설정 -> 이벤트 등록
  -> epoll/kqueue/IOCP 대기 -> ready/completion 이벤트 수신
  -> callback 실행 -> queue 압력 조절 -> 응답 전송
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 소켓을 non-blocking으로 설정 | EAGAIN 처리 |
| 2 | 읽기·쓰기 관심 이벤트 등록 | fd count, registration error |
| 3 | 이벤트 루프가 준비 이벤트를 수신 | event loop lag |
| 4 | callback/promise/coroutine으로 작업 실행 | handler duration |
| 5 | queue와 buffer로 backpressure 적용 | queue depth, dropped event |

> 요약: 이벤트 루프는 준비된 I/O 이벤트만 가져와 짧은 핸들러로 처리하고, 과부하 시 backpressure로 큐를 제어한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | 본 기술 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| Blocking I/O | 요청당 스레드 대기 | non-blocking event 처리 | 연결 10,000개 이상 |
| epoll/kqueue | readiness 통지 | 읽기 가능 상태 알림 | EAGAIN 반복 처리 |
| IOCP | completion 통지 | 완료 이벤트 큐 | Windows 고성능 서버 |
| 한계 | 코드 흐름 단순 | callback depth·loop blocking | loop lag 50ms 이하 |

> 요약: 이벤트 루프는 I/O 대기에는 적합하나 CPU 작업과 긴 핸들러는 별도 worker로 분리해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | thread-per-connection | event loop + non-blocking FD | 연결 수, 메모리 한계 |
| 비용/성능 | context switch 증가 | fd event dispatch | p99 latency, loop lag |
| 운영/위험 | 스레드 고갈 | loop blocking, callback error | CPU 작업 offload 필요성 |

> 요약: 연결 수가 많고 I/O 대기가 길면 이벤트 루프, CPU 계산이 길면 worker pool 또는 프로세스 분리를 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 이벤트 루프 지연 | 긴 CPU 작업·동기 파일 I/O | worker pool, task 분할 | loop lag p99 50ms 이하 |
| 메모리 증가 | 큐 무제한 적재 | high watermark, rate limit | queue depth, heap usage |
| 오류 전파 누락 | callback exception 미처리 | promise rejection handler, circuit breaker | unhandled rejection 0건 |

> 요약: 운영 리스크는 loop lag, 큐 증가, 예외 누락이며 worker 분리와 backpressure로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 성능/지연 | p95 100ms 이하, loop lag p99 50ms 이하 | APM, event-loop monitor |
| 품질/오류 | unhandled rejection 0건, error rate 0.1% 이하 | log, alert |
| 운영/자원 | fd 사용률 70% 이하, queue depth 임계치 이하 | lsof, Prometheus |

> 요약: 비동기 I/O 효과는 loop lag, p95/p99 지연, fd·queue 자원 지표로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 네트워크 서버는 non-blocking socket, epoll/kqueue/IOCP 기반 프레임워크를 선택하고 connection 10,000개 부하 테스트를 수행한다.
2. 이벤트 핸들러는 10ms 이하 실행을 목표로 하고 CPU·동기 파일 I/O는 worker pool 또는 별도 프로세스로 분리한다.
3. 큐마다 high watermark, timeout, retry 제한, circuit breaker를 적용해 backpressure와 장애 전파를 통제한다.

**결론 (2줄):**
- 기술사 판단: I/O-bound 대규모 연결 서버는 이벤트 루프, CPU-bound 서비스는 worker pool·프로세스 병렬 처리를 조합한다.
- 향후 방향: 비동기 I/O는 coroutine, structured concurrency, io_uring과 결합해 코드 흐름과 커널 I/O 경로를 함께 단순화한다.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "비동기 I/O를 설명하시오" | 이벤트 등록·통지·콜백 흐름 | epoll/kqueue/IOCP 특징 |
| 요구사항 명시형 | "설계하시오", "개선 방안을 제시하시오" | loop lag와 backpressure 흐름 | worker 분리, 큐 제어, 지표 |

> 요약: 설명형은 이벤트 처리 원리, 설계형은 loop blocking 방지와 backpressure 기준을 중심으로 작성한다.
