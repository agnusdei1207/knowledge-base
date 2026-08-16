---
sidebar:
  order: 25
  label: "025. 가상 스레드: Java Project Loom (Virtual Thread)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "가상 스레드: Java Project Loom (Virtual Thread)"
date: "2026-08-13T13:58:00+09:00"
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

<details><summary>용어 설명</summary>

- **Virtual Thread (가상 스레드)**: Java 21에서 정식화된 JVM 관리 경량 스레드로, 소수 캐리어 스레드에 다중화되는 실행 단위.
- **Carrier Thread**: Virtual Thread를 실제로 할당받아 CPU 코어 상에서 실행하는 하부의 OS Platform Thread (ForkJoinPool 잇스턴스).
- **Continuation**: Virtual Thread의 런타임 스택 및 실행 재개 지점을 JVM 힙(Heap) 공간에 바인딩 보존/복원하는 핵심 메커니즘.

</details>

- 정의/개념: 대기 작업을 캐리어 스레드에 다중화하는 **Virtual Thread**
- 배경/필요성: 요청별 플랫폼 스레드는 대기 증가 시 **스레드 자원 상한** 도달

#### 한줄 요약

- 다수 가상 스레드를 소수 캐리어 스레드에 다중화하는 것이 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Unmount / Mount**: Virtual Thread가 I/O Blocking 인가 시 Carrier Thread와의 연결을 떼어내고(Unmount), I/O 완료 시 유휴 Carrier Thread에 다시 인가(Mount)되는 동작.
- **Thread-per-request Model**: 복잡한 비동기/반응형(Reactive) 코드 체인 없이, 전통적인 순차적 블로킹 코드(Thread-per-request) 스타일을 유지하면서도 극상의 동시성(High Throughput)을 달성하는 패턴.

</details>

- 필요에 따라 확장되는 스택으로 플랫폼 스레드보다 낮은 초기 비용
- 지원되는 블로킹 연산에서 **Unmount / Mount**로 캐리어 재사용
- 기존 **Thread-per-request** 스타일의 순차 코드 활용 가능

#### 한줄 요약

- 대기 동시성은 확대되지만 CPU 계산 병렬도는 코어 수로 제한된다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

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
| 가상 스레드 집합 | 사용자 로직과 동적 스택 상태 보유 |
| JVM 스케줄러 | 실행 가능한 가상 스레드를 캐리어에 할당 |
| 캐리어 스레드 집합 | 가상 스레드를 실제 CPU에서 실행 |
| 입출력 하위 시스템 | 지원 블로킹 I/O의 **Unmount**•**Mount** 연계 |

#### 한줄 요약

- 호출 스택, JVM, 운영체제가 가상 스레드 실행을 연결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Thread Pinning**: 특정 네이티브•외부 함수 실행 중 가상 스레드가 캐리어에서 분리되지 못하는 현상.

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
3. **캐리어 분리 가능성 판정**: 블로킹 시 네이티브 호출 등 **Pinning** 조건 확인
4. **분리·실행 가능 전환**: Pinning 미발생 시 Continuation 스택 힙 덤프 후 **Unmount** (Carrier Thread 유휴 전환).
5. **고정 대기 **: 분리 불가 시 캐리어 점유 상태로 대기

#### 한줄 요약

- 블로킹 시 분리•실행 가능 전환, 분리 불가 구간은 고정 대기가 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Platform Thread vs Virtual Thread**: Platform Thread는 OS 커널 1:1 매핑 스레드, Virtual Thread는 JVM 내부 $M:N$ 매핑 경량 스레드.

</details>

| 비교 항목 | Platform Thread (전통적 스레드) | Virtual Thread (Java 21 Loom) |
|:---|:---|:---|
| 스케줄링 주체 | OS Kernel Scheduler | **JVM Scheduler (ForkJoinPool)** |
| 매핑 관계 | OS Kernel Thread와 **1:1** 매핑 | OS Carrier Thread와 **M:N** 매핑 |
| 메모리 특성 | 네이티브 스택 등 플랫폼 자원 사용 | 필요에 따라 확장되는 동적 스택 |
| 동시성 상한 | OS 스레드 자원에 직접 영향 | 메모리와 하위 자원에 의해 제한 |
| 적합한 워크로드 | CPU-bound 연산 | **I/O-bound (HTTP/DB) 웹 서버 연산** |

#### 한줄 요약

- 블로킹 I/O는 가상, CPU 계산은 플랫폼 스레드가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **ReentrantLock**: Thread Pinning을 유발하는 `synchronized` 키워드 대신 Virtual Thread 환경에서 안전하게 Unmount를 지원하는 대안 락 클래스.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 네이티브 호출의 장기 **Thread Pinning** | JFR 고정 이벤트로 원인 구간 측정•축소 | 캐리어 점유시간 감소 |
| 가상 스레드를 풀로 제한해 동시성 축소 | 작업별 가상 스레드 생성과 자원별 제한 분리 | 스레드 대기열 중복 방지 |
| 무한 생성으로 인한 하부 DB 커넥션 풀(HikariCP) 고갈 | **Semaphore** 기반 자원 억세스 수량 제한 | 하부 인프라 고갈 예방 |

> 사례: Spring Boot 3.2+ 내 `spring.threads.virtual.enabled=true` 옵션을 통한 Virtual Thread 전면 인가

#### 한줄 요약

- 세마포어, 캐리어 사용률, 스레드 로컬을 통제한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Virtual Thread 적용 기준(Virtual Thread Adoption Criteria)**: I/O 바운드 비율, synchronized 사용 유무, DB 커넥션 쿼터에 기반한 수립 체계.

</details>

- 대기 중심 요청은 **Virtual Thread**, CPU 병렬도는 **코어 한도**로 제한

#### 한줄 요약

- I/O 대기와 고정 구간 및 CPU 계산량을 함께 평가하는 것이 핵심이다.
