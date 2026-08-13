---
sidebar:
  order: 17
  label: "017. 다중프로그래밍•다중처리 (Multiprogramming•Multiprocessing)"
  badge:
    text: "미출 • 30%"
    variant: note
title: 다중프로그래밍•다중처리 (Multiprogramming•Multiprocessing)
date: "2026-08-13T13:29:00+09:00"
tags: [notes-software]
weight: 17
extra:
  question_no: "017"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "교대 실행•동시 실행 구조 비교 기초"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Multiprogramming (다중프로그래밍)**: 단일 CPU 코어 환경에서 여러 개의 프로세스를 물리 메모리에 적재하여, I/O 블로킹 발생 시 타 프로세스로 빠르게 시분할 교대 디스패치(Context Switching)하여 CPU 유휴 시간을 소멸시키는 기법.
- **Multiprocessing (다중처리)**: 2개 이상의 물리 CPU 코어가 장착된 멀티코어/다중 소켓 아키텍처 상에서 여러 프로세스/스레드를 물리적으로 동시 병렬 실행(Parallel Execution)하는 기법.

</details>

- 정의/개념: 단일 코어의 시분할 Interleaving 교대 연산 기법인 **Multiprogramming** 및 다중 코어의 물리적 동시 병렬 연산 기법인 **Multiprocessing**
- 배경/필요성: 단일 작업 실행은 I/O 대기와 유휴 코어의 **연산 자원 낭비**

#### 한줄 요약

- 단일 CPU의 다중프로그래밍과 다중 코어의 다중처리를 구분한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Interleaving**: 단일 CPU 코어가 시간에 따라 빠르게 프로세스들을 번갈아 교대 실행함으로써 사용자에게 마치 동시 실행되는 것처럼 느끼게 하는 기술.
- **Parallel Execution**: 복수의 코어에 독립적 명령어가 각각 물리 디스패치되어 실제 진정한 동시 연산을 수행하는 기술.

</details>

- 단일 CPU 상에서 I/O 대기 시간을 활용한 시분할 교대 수행 (**Multiprogramming / Interleaving**)
- 복수 CPU/코어 상에서 동시 연산 처리 (**Multiprocessing / Parallel Execution**)
- 캐시 일관성(Cache Coherence) 및 동기화 락 오버헤드 유발 유무 차이

#### 한줄 요약

- 유휴시간 은폐와 병렬 처리의 동기화 비용 사이 절충이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **SMP (Symmetric Multiprocessing)**: 모든 CPU 코어가 단일 버스를 통해 동일 메모리(RAM)와 I/O 디바이스를 등등하게 공유하는 대칭형 다중처리 구조.
- **Amdahl's Law (암달의 법칙)**: 병렬화 가능한 비율($P$)과 코어 수($N$)에 따른 이론적 속도 향상 가속비(Speedup) 상한 계산 법칙.

</details>

```text
             [작업 집합]
                  |
              [준비 큐]
                  |
              [스케줄러]
                  |
             [코어 1•2]
                  |
              [공유 메모리]
```

선의 의미: 작업 집합이 준비 큐를 거쳐 커널 스케줄러에 의해 단일/다중 CPU 코어로 배정 인가되고 공유 메모리를 공유하는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 작업 집합 | 실행 가능한 프로세스•스레드 보관 |
| 준비 큐 | CPU 할당 대기 작업을 정책 순서로 정렬 |
| 스케줄러 | 작업을 단일 또는 복수 **코어**에 배정 |
| 코어 1•2 | 교대 실행 또는 물리적 **병렬 실행** 수행 |
| 공유 메모리 | 병렬 작업의 데이터 공유와 일관성 제공 |

#### 한줄 요약

- 준비 큐와 스케줄러가 작업을 코어에 배정하고 공유 메모리를 연결한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Context Switch Overhead**: 다중프로그래밍 환경에서 프로세스 덤프 및 복원 시 소비되는 커널 주기 오버헤드.

</details>

```text
다중프로그래밍

[작업 A 실행]
       │
       ▼
[1. I/O 대기•교대 실행]
       │
       ▼
[작업 B 교대 실행]
       │
       ▼
[단일 CPU 유휴시간 은폐]

다중처리

[병렬 작업 집합]
       │
       ▼
[2. 코어별 병렬 디스패치]
       │
       ▼
[여러 코어 동시 실행]
       │
       ▼
[동기화•결과 결합]
```

### 동작 원리

1. **I/O 대기·교대 실행**: 작업 A 대기 중 작업 B로 문맥 전환
2. **코어별 병렬 디스패치**: 분할 작업을 복수 코어에 동시 배정

#### 한줄 요약

- I/O 대기는 교대 실행으로 숨기고, 병렬 작업은 동시 실행한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Multitasking vs Multithreading**: Multitasking은 OS 레벨의 다중 프로세스 제어 개념이며, Multithreading은 단일 프로세스 내의 복수 실행 흐름 제어 개념.

</details>

| 용어 개념 | 핵심 실행 특징 | 하드웨어 자원 관계 |
|:---|:---|:---|
| **Multiprogramming** | 메모리에 여러 프로그램을 적재 후 I/O 시 교대 실행 | 단일 CPU 유휴 소멸 |
| **Multitasking** | Time Slice(타임 슬라이스) 기반으로 고속 전환 시분할 연산 | 사용자 체감 동시성 |
| **Multiprocessing** | 복수의 물리 CPU 코어에서 병렬 동시 실행 | 멀티 코어 물리 확충 |
| **Multithreading** | 단일 프로세스 내에서 복수의 스레드가 코드/데이터 공유 연산 | 프로세스 내부 자원 공유 |

#### 한줄 요약

- 대기시간 활용은 다중프로그래밍, 병렬화는 다중처리가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **False Sharing**: 서로 다른 코어에서 구동되는 스레드들이 물리적으로 동일한 캐시 라인(64 Byte)에 속한 변수를 각각 수정할 때 불필요한 캐시 무효화 트래픽이 전파되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Multiprogramming 상에서 과도한 프로세스 적재로 인한 메모리 스레싱 | **Admission Control** 및 Working Set 기반 DOM 제어 | 시스템 가용성 유지 |
| Multiprocessing 환경에서 **False Sharing** 발생으로 인한 캐시 병목 | **@Contended (Cache Line Padding)** 기술 적용 | 코어 간 캐시 버스 병목 차단 |
| 코어 수 증가에도 불구하고 **Amdahl's Law**에 따른 가속비 한계 | 직렬 코드 구간(Serial Section) 최소화 튜닝 | 병렬 가속 효율 극대화 |

> 사례: Linux 커널 내 **SMP Multiprocessor Scheduler** 및 Java `@Contended` 패딩 적용

#### 한줄 요약

- 수용 제어, 경합 프로파일링, 캐시 지역성 기반 운영이 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **실행 아키텍처 선택 기준(Execution Architecture Criteria)**: 코어 수, I/O 바운드 비율, 직렬 구간 비율 및 동기화 오버헤드 수치에 기반한 체계.

</details>

- I/O 대기는 **다중프로그래밍**, 병렬 가능 작업은 **다중처리** 적용

#### 한줄 요약

- I/O 대기•병렬 구간•동기화 비용을 함께 평가하는 것이 핵심이다.
