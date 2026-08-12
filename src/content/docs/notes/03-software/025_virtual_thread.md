---
sidebar:
  order: 25
  label: "025. 가상 스레드: Java Project Loom (Virtual Thread)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "가상 스레드: Java Project Loom (Virtual Thread)"
date: "2026-08-06T23:27:50+09:00"
tags: [notes-software]
weight: 25
extra:
  question_no: "025"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "138회 기출, 경량 동시성•스케줄링 현안"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Virtual Thread (가상 스레드)**: Java 21 (Project Loom)에 공식 도입된 경량 사용자 공간 스레드(User-mode Thread)로, OS Kernel Thread(1:1 매핑)가 아닌 JVM 내부에서 수백만 개를 $M:N$ 매핑 및 스케줄링 관리하는 기법.
- **Carrier Thread**: Virtual Thread를 실제로 할당받아 CPU 코어 상에서 실행하는 하부의 OS Platform Thread (ForkJoinPool 잇스턴스).
- **Continuation**: Virtual Thread의 런타임 스택 및 실행 재개 지점을 JVM 힙(Heap) 공간에 바인딩 보존/복원하는 핵심 메커니즘.

</details>

- 정의/개념: OS 커널 스레드 1:1 매핑 한계를 극복하고 JVM 차원에서 수십만 개의 런타임 동시 실행을 지원하는 차세대 경량 동시성 모델인 **Virtual Thread (Java Project Loom)**
- 배경/필요성: 기존 Platform Thread의 높은 메모리(Default 1MB) 및 Context Switch 오버헤드, Reactive/Async 프로그래밍의 복잡한 코드 콜백 헬(Callback Hell) 극복 요구성

#### 한줄 요약

- 다수 가상 스레드를 소수 캐리어 스레드에 다중화하는 것이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Unmount / Mount**: Virtual Thread가 I/O Blocking 인가 시 Carrier Thread와의 연결을 떼어내고(Unmount), I/O 완료 시 유휴 Carrier Thread에 다시 인가(Mount)되는 동작.
- **Thread-per-request Model**: 복잡한 비동기/반응형(Reactive) 코드 체인 없이, 전통적인 순차적 블로킹 코드(Thread-per-request) 스타일을 유지하면서도 극상의 동시성(High Throughput)을 달성하는 패턴.

</details>

- 메모리 Footprint 수 KB 수준(Platform Thread 대비 $\frac{1}{1000}$ 수준)
- I/O Blocking 발생 시 커널 스레드가 블록되지 않고 즉시 **Unmount / Mount** 전환
- 기존 **Thread-per-request** 명령 및 동기식(Synchronous) 코드 호환성 100% 보존

#### 한줄 요약

- 대기 동시성은 확대되지만 CPU 계산 병렬도는 코어 수로 제한된다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Continuation.yield()**: Blocking I/O 호출 시 Virtual Thread의 스택 프레임을 힙(Heap)으로 덤프 이송하고 Carrier Thread 제어권을 반납하는 함수.

</details>

```text
[가상 스레드 집합] -------- [JVM 스케줄러] -------- [캐리어 스레드 집합]
          \\                      /
           \\                    /
              [입출력 하위 시스템]
```

선의 의미: 수십만 개의 Virtual Thread가 JVM ForkJoinPool 기반 Carrier Thread로 $M:N$ 매핑 스케줄링되고 I/O Unmount/Mount 연동되는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| Virtual Thread | **Continuation** 기반 힙(Heap) 상주 스택 관리, 사용자 로직 수행 |
| Carrier Thread | **ForkJoinPool** 인스턴스로 구동되며 Virtual Thread를 실제 CPU 코어에 마운트 디스패치 |
| Scheduler | JVM 차원의 $M:N$ 스케줄러로 준비된 Virtual Thread를 Carrier에 할당 |
| I/O Unmount Engine | Socket/File Blocking 인가 시 **Continuation.yield()** 호출 및 Carrier 분리 |

#### 한줄 요약

- 호출 스택, JVM, 운영체제가 가상 스레드 실행을 연결한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Thread Pinning**: `synchronized` 블록이나 Native Method(JNI) 구동 중 I/O 인가 시, Virtual Thread가 Carrier Thread에서 Unmount되지 못하고 강제 고착되는 현상.

</details>

```text
┌──────────────────────────────┐
│ 실행 가능 가상 스레드      │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 캐리어 탑재             │
│ 2. 가상 스레드 실행        │
└───────┬──────────────────────┘
        ├─ 실행 완료 ───────────▶ [결과 반환]
        │ 블로킹
        ▼
┌──────────────────────────────┐
│ 3. 캐리어 분리 가능성 판정 │
└───────┬──────────────────────┘
        ├─ 가능 ─▶ 4. 분리•실행 가능 전환
        └─ 불가 ─▶ 5. 고정 대기 (Thread Pinning)
```

### 동작 원리

1. **캐리어 탑재**: Virtual Thread가 JVM 스케줄러에 의해 유휴 **Carrier Thread**에 Mount.
2. **가상 스레드 실행**: Java 코드 실행 및 연산 수행.
3. **캐리어 분리 가능성 판정**: Blocking I/O 발생 시 **Thread Pinning** (synchronized 사용 여부) 검증.
4. **분리·실행 가능 전환**: Pinning 미발생 시 Continuation 스택 힙 덤프 후 **Unmount** (Carrier Thread 유휴 전환).
5. **고정 대기 (Pinning)**: Pinning 발생 시 Carrier Thread가 고착 대기하여 성능 저하 유발.

#### 한줄 요약

- 블로킹 시 분리•실행 가능 전환, 분리 불가 구간은 고정 대기가 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Platform Thread vs Virtual Thread**: Platform Thread는 OS 커널 1:1 매핑 스레드, Virtual Thread는 JVM 내부 $M:N$ 매핑 경량 스레드.

</details>

| 비교 항목 | Platform Thread (전통적 스레드) | Virtual Thread (Java 21 Loom) |
|:---|:---|:---|
| 스케줄링 주체 | OS Kernel Scheduler | **JVM Scheduler (ForkJoinPool)** |
| 매핑 관계 | OS Kernel Thread와 **1:1** 매핑 | OS Carrier Thread와 **M:N** 매핑 |
| 메모리 크기 | default 1MB (Fixed Stack) | **수 KB (Dynamic Heap Stack)** |
| 생성 가능 수량 | 수천 개 제한 (OOM 위험) | **수백만 개 동시 생성 가능** |
| 적합한 워크로드 | CPU-bound 연산 | **I/O-bound (HTTP/DB) 웹 서버 연산** |

#### 한줄 요약

- 블로킹 I/O는 가상, CPU 계산은 플랫폼 스레드가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **ReentrantLock**: Thread Pinning을 유발하는 `synchronized` 키워드 대신 Virtual Thread 환경에서 안전하게 Unmount를 지원하는 대안 락 클래스.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| `synchronized` 구문 사용 시 **Thread Pinning** 유발 | **ReentrantLock**으로 락 모듈 전면 교체 | Pinning 고착 차단 및 Unmount 정상화 |
| Virtual Thread를 기존 Thread Pool 방식으로 래핑 재사용 | Thread Pool 금지 및 필요 시마다 `Thread.ofVirtual().start()` 신규 생성 | 생성 비용 0% 장점 활용 |
| 무한 생성으로 인한 하부 DB 커넥션 풀(HikariCP) 고갈 | **Semaphore** 기반 자원 억세스 수량 제한 | 하부 인프라 고갈 예방 |

> 사례: Spring Boot 3.2+ 내 `spring.threads.virtual.enabled=true` 옵션을 통한 Virtual Thread 전면 인가

#### 한줄 요약

- 세마포어, 캐리어 사용률, 스레드 로컬을 통제한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Virtual Thread 적용 기준(Virtual Thread Adoption Criteria)**: I/O 바운드 비율, synchronized 사용 유무, DB 커넥션 쿼터에 기반한 수립 체계.

</details>

- **Virtual Thread 적용 기준**에 따라 High-concurrency I/O 웹 서버 구축 시 **Virtual Thread + ReentrantLock** 구조 적극 적용

#### 한줄 요약

- I/O 대기와 고정 구간 및 CPU 계산량을 함께 평가하는 것이 핵심이다.
