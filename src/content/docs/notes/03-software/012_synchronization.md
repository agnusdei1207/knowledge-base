---
sidebar:
  order: 12
  label: "012. 세마포어•뮤텍스•모니터 (Semaphore Mutex Monitor)"
  badge:
    text: "기출 • 70%"
    variant: note
title: 세마포어•뮤텍스•모니터 (Semaphore Mutex Monitor)
date: "2026-08-13T13:14:00+09:00"
tags: [notes-software]
weight: 12
extra:
  question_no: "012"
  source_status: "기출"
  source_history: "125회, 126회, 132회"
  priority: 70
  priority_note: "125•126•132회 반복, 동기화 원리 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Process Synchronization (동기화)**: 동시 구동되는 프로세스/스레드들이 공유 자원(Shared Memory/Variable)에 접근할 때 데이터 일관성(Consistency)을 유지하도록 순서와 상호 배제를 제어하는 기술.
- **Semaphore (세마포어)**: 정수 카운터 변수($S$)를 이용하여 $P$(Wait/sem_wait) 및 $V$(Signal/sem_post) 원자적 함수로 접근 가능한 N개 자원 수량을 제어하는 동기화 기법.
- **Mutex (뮤텍스)**: 소유권(Ownership)을 바탕으로 오직 락을 획득(Lock)한 단 1개의 스레드만이 락을 해제(Unlock)할 수 있는 이진 상호 배제 키(Key) 객체.
- **Monitor (모니터)**: 프로그래밍 언어 차원에서 공유 변수, 상호 배제 락, Condition Variable을 클래스 캡슐화(Encapsulation)하여 안전하게 동기화를 자동 지원하는 고수준 메커니즘.

</details>

- 정의/개념: 공유 자원 경쟁 조건(Race Condition)을 차단하기 위해 임계 구역(Critical Section) 진입/해제 메커니즘을 제공하는 대표적 동기화 프리미티브 3종인 **세마포어·뮤텍스·모니터**
- 배경/필요성: 동시 읽기•수정은 갱신 유실 등 **경쟁 조건** 발생

#### 한줄 요약

- 공유 자원 특성에 맞는 진입•대기•해제 규칙을 선택한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Critical Section (임계 구역)**: 둘 이상의 스레드가 동시에 공유 데이터에 접근하면 안 되는 비공유 독점 코드 실행 구역.
- **Condition Variable (조건 변수)**: 모니터 내부에서 특정 조건이 충족될 때까지 스레드를 블록 대기(`wait()`)시키거나 깨우는(`signal()/broadcast()`) 시그널링 객체.

</details>

- 카운팅 정수 기반 $N$개 동시 억세스 허용(**Counting Semaphore**) 및 소유권 부재
- **Ownership**을 보유해 획득한 주체만 해제하는 **Mutex**
- 언어 차원의 객체 지향 캡슐화 및 **Condition Variable (wait/signal)** 자동 연동(**Monitor**)

#### 한줄 요약

- 상호 배제와 대기•깨움으로 경쟁 조건을 방지한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Spinlock vs Mutex**: 락 대기 중 반복 검사할지, 실행을 중단하고 대기 큐에서 잠들지의 차이.

</details>

```text
[동기화 프리미티브]
 ├─ Semaphore
 ├─ Mutex Lock
 └─ Monitor
     ├─ Entry Queue
     └─ Condition Variable
```

선의 의미: 실행 스레드가 동기화 프리미티브(Semaphore/Mutex/Monitor)를 거쳐 락을 획득 시 임계 구역 진입, 실패 시 대기 큐로 블록 차단되는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| Semaphore ($S$) | 원자적 **$P()$/$V()$** 연산을 통한 $N$개 자원 카운팅 제어 ($S \ge 0$) |
| Mutex Lock | 단일 1:1 상호 배제 락, **Ownership** 검증 및 Lock/Unlock 제어 |
| Monitor Entry Queue | 모니터 내부 메소드 호출 시 단 1개의 스레드만 진입하도록 대기시키는 입구 큐 |
| Condition Variable | **wait()**, **signal()** 연산을 통한 모니터 내부 특정 상태 조건 충족 대기/깨움 |

#### 한줄 요약

- 동기화 프리미티브가 대기 큐와 임계 구역 접근을 통제한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Spurious Wakeup**: Condition Variable wait() 대기 중 시그널 수신 없이도 스레드가 조기 깨어나는 현상으로, `while(!condition) wait()` 루프 보호 필수.

</details>

```text
┌──────────────────────────────┐
│ 공유 자원 접근 요청         │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 프리미티브 선택          │
│ 허가 수·소유권·상태 조건    │
└──────────────┬───────────────┘
               ▼
╔══════════════════════════════╗
║ 반복: 획득 조건 미충족      ║
║ 2. 획득 조건 검사           ║
║   ├─ 미충족 ─▶ 대기 큐      ║
║   │             │ 깨움      ║
║   │             └─▶ 재검사  ║
║   └─ 충족 ───────▶ 반복 종료║
╚══════════════╤═══════════════╝
               ▼
┌──────────────────────────────┐
│ 3. 접근 권한 획득           │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 4. 임계 구역 실행           │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 5. 권한 해제•깨움           │
└──────────────┬───────────────┘
               ▼
        [접근 결과 반환]
```

### 동작 원리

1. **프리미티브 선택**: 접근 허가 수량(Semaphore) 및 캡슐화 조건(Monitor)에 맞게 동기화 모듈 선정.
2. **획득 조건 검사**: 락/카운터 획득 시도 및 실패 시 **Wait Queue**로 블록 이송.
3. **접근 권한 획득**: 원자적(Atomic) 락 점유 및 세마포어 카운터 차감.
4. **임계 구역 실행**: **Critical Section** 진입 및 데이터 연산 갱신.
5. **권한 해제·깨움**: 락 반납 및 **Signal/Post**를 통한 대기 큐 스레드 깨움(Wakeup).

#### 한줄 요약

- 획득 실패 시 획득 조건 검사를 반복한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Binary Semaphore**: 카운터가 0과 1만 갖는 세마포어로, 소유권이 없다는 점을 제외하면 Mutex와 유사.

</details>

| 비교 항목 | 세마포어 (Semaphore) | 뮤텍스 (Mutex) | 모니터 (Monitor) |
|:---|:---|:---|:---|
| 자원 억세스 수 | $N$개 복수 자원 제어 가능 (Counting) | 단 1개 자원 억세스 (Binary) | 단 1개 모니터 진입 (Binary) |
| Ownership (소유권) | **소유권 없음** (타 스레드가 signal/post 가능) | **소유권 존재** (Lock 건 스레드만 Unlock) | **소유권 존재** (언어 차원 자동 관리) |
| 제어 방식 | 원자적 $P(), V()$ 함수 호출 | Lock / Unlock 함수 호출 | synchronized 키워드 및 wait()/notify() |
| 주요 활용 분야 | 커넥션 풀 자원 관리, 리소스 쿼팅 | 단일 메모리 변수 보호 | Java `ReentrantLock` / synchronized |

#### 한줄 요약

- 허가 수는 세마포어, 소유권은 뮤텍스, 상태 조건은 모니터가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Reentrant Lock**: 동일 스레드가 이미 획득한 뮤텍스 락을 재귀적으로 중복 획득할 때 데드락 없이 승인해 주는 재진입 가능 락.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 세마포어 연산 순서 오류에 따른 **Deadlock** | 구조화된 잠금과 **Monitor** 적용 | 잠금 누락과 순서 오류 감소 |
| Condition Variable **Spurious Wakeup** 현상 발생 | `while(!condition) { wait(); }` 조건 재검사 구문 적용 | 오작동 깨움 방지 |
| 스레드 예외(Exception) 발생 시 Mutex 락 미반납 | **try - finally { unlock(); }** / RAII 패턴 적용 | 락 고갈 예방 |

> 사례: Java `java.util.concurrent` 패키지 내 **Semaphore**, **ReentrantLock**, **Condition** 실무 적용

#### 한줄 요약

- 잠금 순서•보유시간•예외 안전 해제를 검증한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **동기화 프리미티브 선택 기준(Synchronization Selection Criteria)**: 자원 수량, 소유권 존재성, 언어 지원 및 모듈 복잡도에 따른 수립 체계.

</details>

- **동기화 프리미티브 선택 기준**에 따라 $N$개 자원 할당은 **세마포어**, 1:1 변수 보호는 **뮤텍스**, 고수준 캡슐화 개발은 **모니터** 채택

#### 한줄 요약

- 허가 수•소유권•상태 조건에 맞는 프리미티브를 선택한다.
