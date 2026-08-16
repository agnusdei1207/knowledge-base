---
sidebar:
  order: 26
  label: "026. 비동기 I/O•이벤트 루프 (Async I/O Event Loop)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "비동기 I/O•이벤트 루프 (Async I/O Event Loop)"
date: "2026-08-13T14:02:00+09:00"
tags:
  - "notes-software"
weight: 26
extra:
  question_no: "026"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "138회 기출, 이벤트 루프•비동기 처리 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Async I/O (비동기 I/O)**: 프로세스가 I/O 요청 인가 후 결과를 기다리지 않고 즉시 제어권을 반환받아 타 작업을 수행하며, I/O 완료 시 시그널/콜백으로 결과를 수신받는 기법.
- **Event Loop (이벤트 루프)**: 단일/소수의 스레드가 무한 루프를 구동하며, OS Multiplexing 엔진(epoll/kqueue)으로부터 전달된 I/O Event들을 Event Queue에서 인출하여 전용 Callback Handler에 디스패치하는 구조.
- **I/O Multiplexing**: 단일 스레드가 `epoll()`, `kqueue()`, `select()` 등 OS 전용 서브시스템을 통해 수만 개의 File Descriptor(소켓) 상태 변화를 동시 감시하는 기술.

</details>

- 정의/개념: 준비•완료 이벤트를 소수 스레드가 처리하는 **Async I/O•Event Loop**
- 배경/필요성: 연결별 OS 스레드는 대기 연결 증가 시 **메모리•전환 비용** 증가

#### 한줄 요약

- 제어권 반환과 완료 이벤트 기반 비동기 입출력이 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Non-blocking I/O**: I/O Read/Write 호출 시 커널 데이터 미준비 시에도 블록되지 않고 즉시 `EWOULDBLOCK / EAGAIN` 에러 코드를 반환받아 타 작업을 계속하는 기법.
- **Reactor Pattern**: 이벤트 루프가 동시 유입되는 서비스 요청 Event를 감지(Demultiplexing)하여 등록된 EventHandler로 연산을 디스패치하는 비동기 이벤트 처리 디자인 패턴.

</details>

- 대기 연결 수와 OS 스레드 수의 직접 비례 완화
- **Non-blocking I/O + I/O Multiplexing (epoll/kqueue/io_uring)** 연동
- **Reactor Pattern** 기반 Single Thread Event Loop 처리 및 CPU-bound 작업 분리 (Worker Pool)

#### 한줄 요약

- 짧은 처리기는 이벤트 루프, 차단•계산은 작업 풀이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **epoll / kqueue / io_uring**: Linux와 BSD 계열에서 준비 또는 완료 이벤트를 전달하는 I/O 인터페이스.
- **Worker Thread Pool**: Event Loop 내에서 CPU 연산이 오래 걸리는 작업(암호화, 대용량 계산)이 수행되어 Event Loop가 Block되는 사태를 막기 위해 위임하는 백그라운드 스레드 풀.

</details>

```text
+------- 비동기 I/O 런타임 -------+
|                                 |
|      [I/O 등록 인터페이스]      |
|                |                |
|         [이벤트 감시기]         |
|                |                |
|           [이벤트 큐]           |
|                |                |
|          [이벤트 루프]          |
|                |                |
|          [완료 처리기]          |
|                |                |
|          [워커 스레드 풀]       |
|                                 |
+---------------------------------+
```

선의 의미: 소켓 이벤트가 OS epoll 감시기를 거쳐 Event Queue에 수용되면, 단일 Event Loop 스레드가 이를 인출하여 Callback Handler 및 Worker Pool로 위임 처리하는 흐름.

| 구성요소 | 책임 |
|:---|:---|
| I/O 등록 인터페이스 | 파일 기술자와 관심 이벤트 등록 |
| 이벤트 감시기 | **epoll_wait**•**kqueue**로 준비 이벤트 수집 |
| 이벤트 큐 | 읽기•쓰기•접속 이벤트 임시 보관 |
| 이벤트 루프 | 이벤트 인출과 완료 처리기 디스패치 |
| 완료 처리기 | 결과 반영과 후속 비동기 작업 등록 |
| 워커 스레드 풀 | 긴 계산•블로킹 작업 분리 실행 |

#### 한줄 요약

- 비차단 입출력, 이벤트 감시기, 이벤트 큐, 디스패치, 완료 처리기가 순환한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Event Loop Blocking**: 이벤트 루프에서 긴 블로킹•계산 작업을 실행해 다른 이벤트 처리가 지연되는 현상.

</details>

```text
┌──────────────────────────────┐
│ 비동기 작업 요청            │◀──────────────┐
└──────────────┬───────────────┘               │
               ▼                               │
┌──────────────────────────────┐               │
│ 1. I/O 요청 등록            │               │
│ 2. 제어권 즉시 반환         │               │
│ 3. 완료 이벤트 수집         │               │
│ 4. 완료 처리기 디스패치     │               │
│ 5. 결과 처리•후속 등록      │               │
└───────┬──────────────────────┘               │
        ├─ 후속 I/O 있음 ──────────────────────┘
        └─ 처리 완료 ─────────────▶ [결과 반영]
```

### 동작 원리

1. **I/O 요청 등록**: 소켓 Read/Write 요청을 Non-blocking 세팅 후 커널 **epoll_ctl()** 에 등록.
2. **제어권 즉시 반환**: 즉시 반환받아 Event Loop 스레드는 타 이벤트 인출 구동.
3. **완료 이벤트 수집**: 커널 epoll_wait() 신호 수신 시 **Event Queue**에 결과 이벤트 이송.
4. **완료 처리기 디스패치**: Event Loop가 Queue 노드를 인출하여 **Callback Handler** 호출.
5. **결과 처리·후속 등록**: 런타임 결과 반영 및 필요한 경우 후속 비동기 I/O 체이닝 등록.

#### 한줄 요약

- I/O 요청 등록부터 결과 처리•후속 등록까지의 반복 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **io_uring**: 제출 큐와 완료 큐 링으로 비동기 I/O 요청과 결과 전달을 묶는 Linux 인터페이스.

</details>

| 비교 항목 | Thread-per-request (동기 블로킹) | Async I/O Event Loop (비동기) |
|:---|:---|:---|
| 스레드 모델 | 요청당 1개 OS 스레드 생성/할당 (1:1) | 단일 또는 극소수 Event Loop 스레드 |
| 대기 연결 확장 | 연결 증가에 따라 스레드 자원 증가 | 소수 루프가 다수 연결 감시 가능 |
| 개발 복잡도 | 낮음 (순차적 코드 작성 용이) | 상대적으로 높음 (Callback, Promise, Async/Await) |
| 대표적 프레임워크 | Tomcat, Traditional Spring MVC | **Node.js, Netty, Nginx, Redis, Vert.x** |

#### 한줄 요약

- 비동기는 이벤트 재개, 동기 입출력은 호출 흐름 대기가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Backpressure (역압력)**: Event Queue에 처리 불가능할 정도의 I/O Event가 유입될 때, 유입 소켓 읽기(`socket.pause()`)를 차단하여 시스템 OOM을 막는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 이벤트 루프의 긴 연산•대기 | CPU 작업을 **Worker Thread Pool**로 이송 | 루프 처리 지연 제한 |
| 이벤트 유입 증가에 따른 큐 메모리 고갈 | **Backpressure**와 유한 버퍼 적용 | 버퍼 상한과 유입 속도 통제 |
| 복잡한 콜백 함수 체이닝으로 인한 **Callback Hell** | **Async / Await, Promise, RxJava/Project Reactor** 적용 | 코드 가독성 및 유지보수성 확보 |

> 사례: **Node.js libuv** 런타임, **Netty EventLoopGroup**, **Nginx Master/Worker Process** 실무 아키텍처

#### 한줄 요약

- 처리기 시간 상한, 취소 전파, 통합 오류 처리 기반 루프 보호가 핵심이다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **비동기 이중화 선택 기준(Async I/O Selection Criteria)**: 동시 세션 수 타깃, I/O 대 연산 작업 비율, 프레임워크 생태계에 기반한 선택 체계.

</details>

- **비동기 이중화 선택 기준**에 따라 수만 동시 소켓 세션 및 초저지연 게이트웨이 구축 시 **Netty / Node.js (Async I/O Event Loop)** 채택

#### 한줄 요약

- 대기 연결 수와 처리기 실행시간을 함께 평가하는 것이 핵심이다.
