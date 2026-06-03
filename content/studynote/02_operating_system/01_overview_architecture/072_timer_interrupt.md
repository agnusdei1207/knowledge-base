---
title: 72. 타이머 인터럽트 - 선점형 스케줄링의 기반
date: '2026-03-21'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 타이머 [[016_interrupt_mechanism|인터럽트]]는 일정 주기마다 CPU 실행을 끊고 OS가 제어를 되찾게 하는 장치다.
> 2. **가치**: 선점형 스케줄링과 시간 분할의 기반이다.
> 3. **판단**: 타이머 없이 공정한 CPU 분배를 구현하기 어렵다.

---

## Ⅰ. 개요 및 필요성

프로세스가 CPU를 너무 오래 독점하면 시스템이 멈춘 것처럼 보인다. 타이머 [[016_interrupt_mechanism|인터럽트]]는 이를 막는다.

그래서 OS가 주기적으로 개입할 수 있다.

- **📢 섹션 요약 비유**: 놀다가 종이 울리면 번갈아 가는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Timer Tick
  ↓ interrupt
Kernel
  ↓
Scheduler / Context Switch
```

| 구성 | 역할 |
| :-- | :-- |
| [[071_os_timer|Timer]] | 주기 [[130_signal|신호]] |
| [[016_interrupt_mechanism|Interrupt]] | 제어 전환 |
| Scheduler | 다음 작업 선택 |

타이머 [[016_interrupt_mechanism|인터럽트]]는 CPU 시간을 잘게 나누고, OS가 선점할 기회를 제공한다.

- **📢 섹션 요약 비유**: 학교 종이 울리면 자리 정리가 시작되는 것이다.

---

## Ⅲ. 비교 및 연결

| 개념 | 의미 |
| :-- | :-- |
| [[071_os_timer|Timer]] | 시간 기준 |
| [[016_interrupt_mechanism|Interrupt]] | 끊고 제어 |
| Preemption | 강제 전환 |

| 효과 | 설명 |
| :-- | :-- |
| Fairness | 공정성 |
| Responsiveness | 응답성 |

타이머 [[016_interrupt_mechanism|인터럽트]]는 OS가 CPU를 통제하는 핵심 메커니즘이다.

- **📢 섹션 요약 비유**: 순번대로 차례를 바꾸게 하는 [[130_signal|신호]]다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. 타이머 주기를 이해하는가?
2. [[016_interrupt_mechanism|인터럽트]]와 [[079_kube_scheduler_pod_placement|스케줄러]] 연결을 아는가?
3. 선점형 스케줄링을 설명할 수 있는가?
4. 시간 분할의 필요성을 아는가?
5. [[033_context|컨텍스트]] 스위치와 연결하는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 타이머 없이 폴링만 하는 설계
- 선점 개념 없이 CPU를 공유하는 설계
- [[016_interrupt_mechanism|인터럽트]] 비용을 무시하는 설계
- 시간 분배를 공정성 없이 처리하는 설계

기술사 관점에서는 타이머 [[016_interrupt_mechanism|인터럽트]]를 "선점형 스케줄링의 [[507_acid_properties|트리거]]"로 설명해야 한다.

- **📢 섹션 요약 비유**: 종이 울려야 다음 사람이 들어온다.

---

## Ⅴ. 기대효과 및 결론

타이머 [[016_interrupt_mechanism|인터럽트]]는 시스템 응답성과 공정성을 높인다.

결론적으로 타이머 [[016_interrupt_mechanism|인터럽트]]는 선점형 스케줄링의 기반이다.

- **📢 섹션 요약 비유**: 시간을 나누는 학교 종이다.

---

## 관련 개념 맵

```text
Timer
  ↓ interrupt
Preemption
  ↓
Scheduler
```

---

## 관련 키워드 및 발전 흐름도

```text
Timer
  ↓
Interrupt
  ↓
Preemptive Scheduling
  ↓
Context Switch
```

---

## 어린이를 위한 3줄 비유 설명

종이 울리면 바꿔요.  
CPU도 잠깐 쉬어요.  
타이머 [[016_interrupt_mechanism|인터럽트]]는 그런 [[130_signal|신호]]예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 72 / 800

← **이전**: [[071_os_timer|71. 운영체제 타이머 (Timer) - 시스템 클럭, 카운터]]
**다음**: [[073_tick_jiffies|73. 틱 (Tick) / 지피스 (Jiffies)]] →

---
