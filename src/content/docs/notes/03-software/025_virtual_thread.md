---
sidebar:
  order: 25
  label: "025. 가상 스레드: Java Project Loom"
  badge:
    text: "기출 • 50%"
    variant: note
title: "가상 스레드: Java Project Loom (Virtual Thread)"
date: "2026-08-17T18:40:00+09:00"
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

- **M:N 다중화(Continuation & Carrier Thread)**: 수백만 개의 경량 가상 스레드를 소수의 OS 커널 스레드(캐리어)에 매핑하고 I/O 시 힙 메모리로 분리하는 기법.
- **메모리 고갈 및 디버깅 복잡도(Stack Exhaustion & Complexity)**: 스레드당 1MB의 물리 스택 할당으로 인한 OOM 한계 및 비동기 콜백 체인의 추적 어려움.

</details>

- 정의/개념: JVM 런타임이 콜 스택을 힙에 저장하고 **M:N 다중화(Continuation & ForkJoinPool)** 로 I/O 대기 시 플랫폼 스레드를 양보하는 경량 동시성 기법
- 배경/필요성: 기존 OS 1:1 스레드 모델의 스택 메모리 고갈 및 논블로킹 Reactive 코드 도입 시 **디버깅 복잡도 폭증 한계** 직면

#### 한줄 요약

- I/O 대기 중 OS 스레드 낭비를 제거하기 위해 수백만 가상 스레드를 소수 캐리어에 M:N 다중화하는 경량 동시성 모델

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **마운트/언마운트(Mount/Unmount)**: 가상 스레드가 실행 시 캐리어 스레드에 탑재(Mount)되고, I/O 대기 발생 시 컨티뉴에이션을 힙에 저장하고 캐리어에서 분리(Unmount)되는 메커니즘.
- **요청당 스레드 모델(Thread-per-request)**: 콜백·Reactive 스타일 없이 동기식 직관적 코드로 높은 동시성을 달성하는 프로그래밍 모델.

</details>

- 초경량 생성 비용으로 스레드 풀 없이 요청당 가상 스레드 생성 가능
- I/O 대기 시 **언마운트**로 캐리어 스레드를 즉시 다른 가상 스레드에 양보
- 비동기 Reactive 코드 대신 동기식 **요청당 스레드** 스타일로 고동시성 구현

#### 한줄 요약

- I/O 대기 시 캐리어를 즉시 양보하는 언마운트로 고동시성을 달성하며 동기식 코드 스타일 유지

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Continuation.yield()**: 가상 스레드가 I/O 대기 시 현재 콜 스택을 힙에 저장하고 캐리어 스레드를 반환하는 JVM 내부 API.

</details>

```text
[ 가상 스레드 M:N 다중화 구조 ]
가상 스레드 (수백만 개, JVM 힙 관리)
[VT1] [VT2].. [VT_N]
       │ M:N 스케줄링
JVM 스케줄러 (ForkJoinPool)
├─ 유휴 캐리어에 가상 스레드 배정 (Mount)
└─ I/O 대기 감지 시 가상 스레드 분리 (Unmount)
캐리어 스레드 (소수, OS 플랫폼 스레드)
[Carrier A] [Carrier B]
       │
CPU 코어
```

선의 의미: 가지(`├─`, `└─`)는 JVM 스케줄러의 Mount·Unmount 결정 기준 관계

| 구성요소 | 책임 |
|:---|:---|
| 가상 스레드 집합 | 비즈니스 로직 실행 상태(컨티뉴에이션)를 JVM 힙에 보관 |
| **JVM 스케줄러** | ForkJoinPool 기반 가상 스레드와 캐리어 스레드 M:N 매핑 |
| **캐리어 스레드** | OS 플랫폼 스레드로 실제 CPU 코어에서 가상 스레드 실행 |
| I/O 하위 시스템 | I/O 대기 감지 시 컨티뉴에이션 저장 후 언마운트 트리거 |

#### 한줄 요약

- JVM 스케줄러가 수백만 가상 스레드를 소수의 캐리어 스레드에 M:N으로 배정하고 I/O 대기 시 언마운트

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **스레드 피닝(Thread Pinning)**: `synchronized` 블록·JNI 호출 내에서 I/O 대기 발생 시 가상 스레드가 언마운트되지 못하고 캐리어 스레드를 점유한 채 블로킹되는 현상.

</details>

```text
가상 스레드 생성 및 JVM 스케줄러 큐 진입
   │
   ▼
1. Mount: 유휴 캐리어 스레드에 가상 스레드 탑재
   │
   ▼
2. CPU 연산 실행
   │
   ▼
3. I/O 대기 발생 → 피닝 여부 판정
├─ synchronized·JNI 없음: Unmount 실행
│      └─ 컨티뉴에이션 힙 저장 → 캐리어 반환 → 다른 가상 스레드 Mount
└─ synchronized·JNI 존재: 스레드 피닝 발생
       └─ 캐리어 점유 유지 → 타 가상 스레드 캐리어 사용 불가
   │
   ▼
4. I/O 완료 → 재Mount → 실행 재개
```

**동작 원리**

1. **Mount**: JVM 스케줄러가 유휴 캐리어 스레드에 가상 스레드를 탑재하여 실행 시작
2. **연산 실행**: CPU 바운드 연산을 캐리어 스레드 위에서 직접 실행
3. **Unmount**: I/O 대기 발생 시 컨티뉴에이션을 힙에 저장하고 캐리어를 즉시 반환
4. **피닝 발생**: `synchronized`·JNI 내부에서 I/O 대기 시 캐리어 점유 유지로 성능 저하

#### 한줄 요약

- I/O 대기 시 컨티뉴에이션을 힙에 저장하고 캐리어를 반환하는 Unmount로 스레드 이용률을 극대화

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **플랫폼 스레드(Platform Thread)**: OS 커널이 직접 관리하는 1:1 매핑 스레드로, 생성 비용·메모리 소비가 크고 스케줄링은 OS 커널이 담당.

</details>

| 비교 항목 | 플랫폼 스레드 (전통적) | 가상 스레드 (Java 21) |
|:---|:---|:---|
| 적용 기준 | CPU 바운드 연산 집약적 작업 | I/O 바운드 고동시성 웹 서버·API |
| 핵심 특징 | OS 커널 1:1 매핑, 스택 1MB 고정 | JVM 관리 M:N 매핑, 수백 바이트 힙 스택 |
| 한계 및 위험 | I/O 대기 중 OS 스레드 유휴 낭비 | **스레드 피닝** 발생 시 캐리어 점유 성능 저하 |

#### 한줄 요약

- CPU 바운드는 플랫폼 스레드, I/O 바운드 고동시성은 가상 스레드 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **ReentrantLock**: `synchronized` 대체 잠금으로, 가상 스레드 환경에서 I/O 대기 시 캐리어 스레드를 해제(Unmount)할 수 있어 피닝을 방지.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| `synchronized` 사용으로 **스레드 피닝** 발생 | `synchronized`를 **ReentrantLock**으로 교체 | I/O 대기 시 Unmount 정상 작동 보장 |
| 가상 스레드 수 제한 없어 하위 DB 커넥션 풀 고갈 | DB 커넥션 접근을 **세마포어(Semaphore)** 로 동시 접근 수 제한 | 가상 스레드 고동시성 유지하며 하위 자원 보호 |
| `ThreadLocal` 과다 사용으로 수백만 스레드 메모리 오버헤드 급증 | `ThreadLocal`을 **Scoped Values**로 대체 | 가상 스레드별 불필요한 데이터 복사 제거 |

#### 한줄 요약

- 피닝은 ReentrantLock으로, 자원 고갈은 세마포어로, 메모리 오버헤드는 Scoped Values로 해소

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **가상 스레드 적용 기준**: I/O 바운드 여부·피닝 위험·하위 자원 한도를 고려하여 가상 스레드와 플랫폼 스레드를 선택하는 판단 기준.

</details>

- I/O 바운드 웹 API·DB 접근은 **가상 스레드**, CPU 바운드 암호화·압축 연산은 **플랫폼 스레드** 선택

#### 한줄 요약

- I/O 대기 중심 고동시성 환경은 가상 스레드, CPU 집약적 연산은 플랫폼 스레드를 적용
