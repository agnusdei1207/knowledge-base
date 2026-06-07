---
title: "Jiffies"
date: "2026-03-21"
tags:
  - "studynote-operating-system"
weight: 73
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Tick은 타이머가 발생시키는 주기 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)이고, jiffies는 그 누적 카운트다.
> 2. **가치**: OS 시간 관리와 스케줄링 기준이 된다.
> 3. **판단**: 시간 단위와 누적 값의 차이를 구분해야 한다.

---

## Ⅰ. 개요 및 필요성

운영체제는 시간이 얼마나 지났는지 알아야 한다.

Tick과 jiffies는 그 기준을 제공한다.

- **📢 섹션 요약 비유**: 시계의 똑딱 소리와 그 횟수를 세는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Timer Tick
  v
Jiffies++
```

| 개념 | 의미 |
| :-- | :-- |
| Tick | 주기 이벤트 |
| Jiffies | 누적 카운트 |
| Timekeeping | 시간 관리 |

Tick이 하나씩 발생할 때마다 jiffies가 증가한다. 그래서 OS는 시간을 추적한다.

- **📢 섹션 요약 비유**: 종이 울릴 때마다 체크 표시를 하나씩 늘리는 것이다.

---

## Ⅲ. 비교 및 연결

| 구분 | Tick | Jiffies |
| :-- | :-- | :-- |
| 성격 | 이벤트 | 카운트 |
| 역할 | 기준 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) | 누적 시간 |

| 관련 | 의미 |
| :-- | :-- |
| Scheduler | 시간 분배 |
| [Timer Interrupt](/studynote/02_operating_system/01_overview_architecture/072_timer_interrupt/) | [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 발생 |

Tick과 jiffies는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 시간 표현에서 자주 함께 등장한다.

- **📢 섹션 요약 비유**: 알람 소리와 알람 횟수를 구분하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. tick과 jiffies를 구분하는가?
2. [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 시간 관리와 연결하는가?
3. 스케줄링 기준으로 이해하는가?
4. [timeout](/studynote/02_operating_system/05_deadlock/319_timeout_prevention/) 계산에 쓰는가?
5. 시간 단위를 혼동하지 않는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- tick을 jiffies로 착각하는 설계
- 시간을 이벤트와 카운트로 구분하지 않는 설계
- [timeout](/studynote/02_operating_system/05_deadlock/319_timeout_prevention/) 계산을 대충 하는 설계
- [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 시간 개념을 단순 숫자로만 보는 설계

기술사 관점에서는 tick과 jiffies를 "OS 시간 측정의 기본 단위와 누적값"으로 설명해야 한다.

- **📢 섹션 요약 비유**: 똑딱 소리와 센 숫자를 같이 봐야 한다.

---

## Ⅴ. 기대효과 및 결론

Tick과 jiffies를 이해하면 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 시간 관리가 보인다.

결론적으로 tick은 주기 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)이고 jiffies는 누적 카운트다.

- **📢 섹션 요약 비유**: 소리와 횟수를 따로 세는 것이다.

---

## 관련 개념 맵

```text
Timer Tick
  v
Jiffies
  v
Kernel Timekeeping
```

---

## 관련 키워드 및 발전 흐름도

```text
Tick
  v
Jiffies
  v
Timekeeping
```

---

## 어린이를 위한 3줄 비유 설명

똑딱 소리가 나요.
몇 번 울렸는지 세요.
틱과 지피스는 그런 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 73 / 800

<- **이전**: [72. 타이머 인터럽트 - 선점형 스케줄링의 기반](/studynote/02_operating_system/01_overview_architecture/072_timer_interrupt/)
**다음**: [74. 틱리스 커널 (Tickless Kernel)](/studynote/02_operating_system/01_overview_architecture/074_tickless_kernel/) ->

---
