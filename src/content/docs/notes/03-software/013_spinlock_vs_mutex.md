---
sidebar:
  order: 13
  label: "013. 스핀락 vs 뮤텍스 (Spinlock vs Mutex)"
  badge:
    text: "기출 • 50%"
    variant: note
title: 스핀락 vs 뮤텍스 (Spinlock vs Mutex)
date: "2026-08-13T13:17:00+09:00"
tags: [notes-software]
weight: 13
extra:
  question_no: "013"
  source_status: "기출"
  source_history: "123회"
  priority: 50
  priority_note: "123회 기출, 스핀락•뮤텍스 선택 기준"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Spinlock (스핀락)**: 락 획득 실패 시 스레드가 CPU를 반납하지 않고 `while` 루프 기반 바쁜 대기(Busy Waiting)를 수행하여 락을 즉각 가로채는 동기화 기법.
- **Mutex (뮤텍스)**: 락 획득 실패 시 스레드를 OS 커널 대기 큐(Wait Queue)로 블록 이송(Sleep/Block)시켜 CPU를 타 스레드에 양도하는 상호 배제 기법.
- **Adaptive Mutex**: 락 소유자가 현재 타 CPU 코어에서 구동 중이면 짧게 스핀락을 돌고, 수면 중이면 Sleep 블록으로 자동 전환하는 적응형 락 기법.

</details>

- 정의/개념: 임계 구역(Critical Section) 점유 실패 시 대기 스레드의 CPU 처리 매커니즘(Busy Waiting vs Sleep/Block)에 따른 대표적 동기화 2대 분류인 **스핀락 vs 뮤텍스**
- 배경/필요성: 단일 대기 방식은 짧은 잠금의 **전환 비용**과 긴 스핀 낭비 유발

#### 한줄 요약

- 수면 가능 여부와 보유시간에 따라 잠금 방식을 선택한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Busy Waiting (바쁜 대기)**: 실행 상태를 유지하며 락 상태를 반복 검사하는 동작.
- **Context Switch Threshold**: 문맥 전환에 소모되는 대략적인 시간 비용(약 수 μs 수치)으로, 임계 구역 실행시간과의 비교 기준점.

</details>

- 수면 전환 없이 락을 반복 검사하는 **Spinlock**
- 획득 실패 시 대기 큐에서 수면하는 **Mutex**
- **Critical Section** 점유 시간 크기 대 **Context Switch Threshold** 지연의 트레이드오프

#### 한줄 요약

- 스핀락은 바쁜 대기, 뮤텍스는 수면 대기 사용이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Atomic Test-and-Set (TAS)**: 하드웨어 수준에서 락 변수의 읽기와 쓰기를 단일 불가분(Atomic) 명령어로 실행하는 전용 지시어.

</details>

```text
           [경쟁 스레드]
                  |
           [락 상태 워드] -- [대기 방식]
                  |
            [소유 스레드]
                  |
             [임계 구역]
```

선의 의미: 경쟁 스레드가 락 상태 워드의 Atomic 변수(TAS)를 검사하여 스핀(Busy Wait) 또는 커널 수면(Sleep Wait) 대기 방식으로 분기되는 구조.

| 구성요소 | 책임 |
|:---|:---|
| Atomic Lock Variable | **Test-and-Set(TAS)** 또는 **Compare-and-Swap(CAS)** 기반 락 점유 상태 보관 |
| Spin Loop | **Spinlock** 사용 시 CPU 레지스터 상에서 락 해제 순간을 지속 감시 |
| Kernel Wait Queue | **Mutex** 사용 시 락 획득 실패 스레드를 Block 시켜 수면 관리하는 큐 |
| Critical Section | 동기화 보장을 통해 오직 단일 소유자만 구동되는 코드 영역 |

#### 한줄 요약

- 상태 워드와 대기 방식이 임계 구역 소유권 경쟁을 통제한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Sleep-capable Context**: 인터럽트 핸들러(ISR)와 달리 커널 스케줄러에 의해 수면(Sleep)이 허용되는 프로세스/스레드 런타임 문맥.

</details>

```text
┌──────────────────────────────┐
│ 잠금 대기 방식 결정         │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 수면 가능성 판정         │
└───────┬──────────────────────┘
        ├─ 수면 불가 ───────────▶ [3. 스핀락 선택]
        │ 수면 가능
        ▼
┌──────────────────────────────┐
│ 2. 보유시간•전환비용 비교   │
└───────┬──────────────────────┘
        ├─ 보유시간 < 전환비용 ─▶ [3. 스핀락 선택]
        └─ 보유시간 ≥ 전환비용 ─▶ [4. 뮤텍스 선택]
```

### 동작 원리

1. **수면 가능성 판정**: 현재 런타임 문맥이 **Sleep-capable Context**(스레드)인지 수면 불가(인터럽트 ISR)인지 검증.
2. **보유시간·전환비용 비교**: 임계 구역 점유 시간 $T_{\text{hold}}$ 과 문맥 전환 비용 $T_{\text{ctx}}$ 비교.
3. **스핀락 선택**: 수면 불가 또는 짧은 보유 구간에 적용
4. **뮤텍스 선택**: 수면 가능하고 긴 보유 구간에 적용

#### 한줄 요약

- 수면 불가•짧은 보유는 스핀락, 긴 보유는 뮤텍스가 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Interrupt Service Routine (ISR)**: 하드웨어 인터럽트를 처리하며 일반적인 수면 락을 사용할 수 없는 실행 문맥.

</details>

| 비교 항목 | Spinlock (스핀락) | Mutex (뮤텍스) |
|:---|:---|:---|
| 대기 메커니즘 | 실행 상태의 **Busy Waiting** | 대기 큐에서 **Sleep / Block** |
| 전환 비용 | 락 대기 자체는 수면 전환 없음 | 수면•깨움 전환 비용 발생 |
| 적합한 임계 구역 | 극도로 짧은 연산 구역 ($T_{\text{hold}} < T_{\text{ctx}}$) | 긴 연산, I/O 작업 포함 구역 ($T_{\text{hold}} \ge T_{\text{ctx}}$) |
| ISR 수용 여부 | 커널 규칙에 맞는 **IRQ-safe 스핀락** 사용 | 수면 불가 문맥에서는 사용 불가 |

#### 한줄 요약

- 짧은 보유는 스핀락, 긴 보유는 뮤텍스를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Cache Line Bouncing**: 멀티소켓/멀티코어 환경에서 잦은 스핀락 TAS 수행으로 인해 L1/L2 캐시 일관성(MESI) 프로토콜 트래픽이 폭증하는 병목.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Spinlock 보유 스레드가 선점(Preempt)되어 무한 스핀 발생 | Spinlock 인가 시 해당 코어의 선점 및 인터럽트 차단 | 코어 스핀 마비 예방 |
| 멀티코어 환경에서 Spinlock 억세스로 인한 **Cache Line Bouncing** | **PAUSE** 명령어 수용 및 **Ticket/MCS Lock** 체계 적용 | 캐시 일관성 버스 트래픽 억제 |
| 임계 구역 길이를 예측하기 힘든 런타임 환경 | **Adaptive Mutex (Spin 후 Sleep 전환)** 사용 | 동적 상황 최적 성능 확보 |

> 사례: Linux 커널 내부 **spinlock_t** (ISR 영역) 및 **mutex_t** (Process Context) 이원화 실증

#### 한줄 요약

- 보유시간 계측과 스핀 상한으로 CPU 낭비를 제한한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **동기화 선택 기준(Spinlock vs Mutex Selection Criteria)**: 런타임 문맥(ISR vs Thread), 임계 구역 수행 시간 및 문맥 전환 비용에 기반한 수립 체계.

</details>

- **동기화 선택 기준**에 따라 ISR/초단기 임계 구역은 **Spinlock**, I/O 및 장기 구역은 **Mutex / Adaptive Mutex** 채택

#### 한줄 요약

- 수면 가능 여부와 보유시간으로 잠금 방식을 선택한다.
