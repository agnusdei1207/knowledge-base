+++
title = "73. 틱 (Tick) / 지피스 (Jiffies)"
date = 2026-03-21

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Tick(틱)은 타이머 하드웨어가 주기적으로 발생시키는 인터럽트 이벤트이고, Jiffies(지피스)는 시스템 부팅 이후 누적된 Tick 횟수를 저장하는 커널 전역 카운터다.
> 2. **가치**: OS의 저해상도 시간 관리, 스케줄링 기준, 타임아웃 계산의 기초 단위로서 커널 전반에서 사용된다.
> 3. **판단**: jiffies는 HZ 설정에 따라 실제 시간으로 환산해야 하며(예: jiffies/HZ = 초), 오버플로(overflow) 처리와 고해상도 타이머(HRT)와의 관계를 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

OS는 시간이 얼마나 경과했는지 알아야 한다. 프로세스에게 CPU를 얼마나 줬는지, 슬립 요청이 얼마나 지났는지, 네트워크 패킷 재전송 타임아웃이 언제인지 등을 모두 시간 기준으로 관리하기 때문이다.

초기 리눅스는 이 시간 관리를 Tick과 Jiffies라는 단순한 메커니즘으로 구현했다. 타이머 하드웨어(PIT 등)가 일정 주기마다 인터럽트를 발생시킬 때마다(=Tick마다) 커널은 `jiffies`라는 전역 변수를 1씩 증가시킨다. 그 결과 `jiffies`는 시스템이 부팅된 이후 발생한 Tick의 총 횟수를 담고 있으며, 이를 HZ(초당 Tick 횟수)로 나누면 경과 시간(초 단위)을 계산할 수 있다.

Jiffies 기반 시간 관리는 단순하고 오버헤드가 낮다. 그러나 HZ=250인 경우 최소 시간 단위가 4ms여서 밀리초 이하의 정밀도가 필요한 상황에는 부적합하다. 이를 보완하기 위해 리눅스 2.6.16(2006)부터 나노초 정밀도의 HRT(High-Resolution Timer, `hrtimer`)가 도입되었다. 현재는 jiffies 기반 저해상도 타이머와 ktime 기반 고해상도 타이머가 공존한다.

- **📢 섹션 요약 비유**: 시계의 똑딱 소리(Tick)를 들을 때마다 체크 표시를 하나씩 늘리고(Jiffies), 체크 표시 수를 세면 시간을 알 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Tick과 Jiffies의 동작 메커니즘



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">하드웨어 타이머</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">주기 인터럽트(IRQ) 발생</div></div>
<div class="kb-diagram-note">↓ (1/HZ 초마다, 예: HZ=250이면 4ms마다)</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">timer_interrupt() 호출</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">do_timer() 실행</div></div>
<div class="kb-diagram-note">jiffies_64++; ← 전역 카운터 증가</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">시간 경과 계산</div></div>
<div class="kb-diagram-note">경과 시간(초) = jiffies / HZ</div>
<div class="kb-diagram-note">경과 시간(ms) = jiffies * 1000 / HZ</div>
<div class="kb-diagram-note">특정 미래 시점 = jiffies + N * HZ (N초 후)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">타이머 만료 확인</div></div>
<div class="kb-diagram-note">timer_list에서 jiffies &gt;= timer.expires 인 타이머 처리</div>
</div>
</div>



### Jiffies 핵심 상수 및 매크로

| 매크로/변수 | 설명 | 예시 (HZ=250) |
| :--- | :--- | :--- |
| `HZ` | 초당 틱 횟수 설정 | 250 |
| `jiffies` | 현재 jiffies 값 (전역) | - |
| `jiffies_64` | 64비트 jiffies (오버플로 방지) | - |
| `msecs_to_jiffies(ms)` | 밀리초 → jiffies 변환 | msecs_to_jiffies(1000) = 250 |
| `jiffies_to_msecs(j)` | jiffies → 밀리초 변환 | jiffies_to_msecs(250) = 1000 |
| `time_after(a, b)` | a > b 비교 (오버플로 안전) | 타임아웃 체크 |
| `time_before(a, b)` | a < b 비교 (오버플로 안전) | 미래 시점 체크 |

### HZ 설정에 따른 특성 비교

| HZ 값 | 틱 주기 | jiffies 오버플로 (32비트) | 특성 |
| :--- | :--- | :--- | :--- |
| 100 | 10ms | ~497일 | 낮은 오버헤드, 낮은 정밀도 |
| 250 | 4ms | ~199일 | 균형 (대부분 서버/데스크톱) |
| 300 | 3.33ms | ~166일 | 일부 배포판 |
| 1000 | 1ms | ~49일 | 높은 응답성, 높은 오버헤드 |

### 32비트 Jiffies 오버플로 문제

32비트 `jiffies`는 HZ=250 기준으로 약 199일 만에 0으로 초기화(Wraparound)된다. 단순한 비교 연산(`if (jiffies > expire)`)은 오버플로 시 틀린 결과를 낸다.

```c
/* 틀린 코드: 오버플로 미처리 */
if (jiffies > expire_time) { /* 만료 처리 */ }

/* 올바른 코드: time_after() 매크로 사용 */
if (time_after(jiffies, expire_time)) { /* 만료 처리 */ }

/* time_after()의 내부 구현 */
#define time_after(a, b) ((long)(b) - (long)(a) < 0)
/* → 부호 있는 뺄셈으로 오버플로를 안전하게 처리 */
```

64비트 `jiffies_64`는 HZ=1000 기준으로도 5.85억 년 후에나 오버플로가 발생하므로 실용적으로 안전하다.

### Jiffies 기반 타이머 사용 예시 (커널 코드)

```c
/* 3초 후에 만료되는 타이머 설정 */
struct timer_list my_timer;
timer_setup(&my_timer, my_callback, 0);
mod_timer(&my_timer, jiffies + 3 * HZ);

/* 500ms 슬립 */
msleep(500);  /* 내부적으로 jiffies 기반 계산 */

/* 타임아웃 체크 */
unsigned long timeout = jiffies + msecs_to_jiffies(5000); /* 5초 */
while (!condition) {
    if (time_after(jiffies, timeout)) {
        return -ETIMEDOUT;
    }
    schedule();
}
```

### Jiffies vs ktime 비교 (저해상도 vs 고해상도)

| 항목 | Jiffies (저해상도) | ktime_t (고해상도) |
| :--- | :--- | :--- |
| 단위 | Tick (1/HZ 초) | 나노초(ns) |
| 정밀도 | 1~10ms | ~1ns |
| 자료형 | unsigned long | s64 (나노초 값) |
| 타이머 | timer_list | hrtimer |
| 오버헤드 | 매우 낮음 | 약간 높음 |
| 주요 용도 | 일반 타임아웃, 스케줄링 | 오디오, 실시간, 정밀 제어 |

- **📢 섹션 요약 비유**: 종이 울릴 때마다 칠판에 정자 표시(Jiffies)를 하나씩 그린다. 나중에 표시 개수를 세면 수업이 몇 번 바뀌었는지, 시간이 얼마나 지났는지 알 수 있다.

---

## Ⅲ. 비교 및 연결

### Tick vs Jiffies vs ktime 비교

| 항목 | Tick | Jiffies | ktime_t |
| :--- | :--- | :--- | :--- |
| 성격 | 이벤트(인터럽트) | 카운터(누적값) | 절대 시간값 |
| 단위 | 없음(사건 발생) | 정수 (틱 횟수) | 나노초(정수) |
| 역할 | 시간 신호 발생 | 경과 시간 추적 | 정밀 시간 측정 |
| 해상도 | 1/HZ 초 | 1/HZ 초 | ~1ns |
| 오버플로 | 없음 | 32비트 시 주의 | 실용적으로 없음 |

### Jiffies와 관련 커널 기능

| 커널 기능 | Jiffies 활용 방식 |
| :--- | :--- |
| 타이머 휠(Timer Wheel) | 타이머 만료 시점을 jiffies로 표현 |
| 스케줄러 | 프로세스 실행 시간 계정(accounting) |
| sleep()/msleep() | 슬립 시간을 jiffies로 변환 |
| 네트워크 TCP | 재전송 타임아웃을 jiffies로 계산 |
| 파일시스템 | dirty page 플러시 주기 관리 |
| 인터럽트 통계 | /proc/interrupts 통계 갱신 |

### Jiffies 읽기의 원자성(Atomicity)

jiffies는 32비트 시스템에서 단순 읽기(4바이트)로 원자적으로 읽을 수 있다. 그러나 jiffies_64는 64비트 값이어서 32비트 CPU에서는 두 번의 32비트 읽기가 필요하므로 비원자적이다. 이를 위해 `get_jiffies_64()` 함수가 제공되며 내부적으로 seqlock을 사용한다.

```c
/* 안전한 64비트 jiffies 읽기 */
u64 current_jiffies = get_jiffies_64();
```

- **📢 섹션 요약 비유**: 알람 소리(Tick)와 알람 울린 횟수(Jiffies)는 다르다. 소리를 들을 때마다 횟수를 세는 것이 Jiffies다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. jiffies와 ktime_t의 용도 차이를 구분하는가? (저해상도 vs 고해상도)
2. HZ 값이 시스템의 성능/응답성 요구사항에 맞게 설정되어 있는가?
3. jiffies 비교 시 `time_after()`, `time_before()` 매크로를 사용하는가? (오버플로 안전)
4. 64비트 jiffies가 필요한 경우 `get_jiffies_64()`를 사용하는가?
5. 밀리초/초 변환 시 `msecs_to_jiffies()` / `jiffies_to_msecs()`를 사용하는가?
6. 나노초 정밀도가 필요한 경우 jiffies 대신 hrtimer를 사용하는가?
7. `jiffies + N * HZ` 표현이 오버플로 위험 없이 사용되는가?
8. 타이머 만료 검사가 올바른 비교 매크로로 구현되어 있는가?

### 안티패턴

- **Tick을 Jiffies로 착각**: Tick은 이벤트(인터럽트 발생)이고 Jiffies는 그 누적 카운트다. 이 둘을 혼동하면 "타이머 인터럽트가 발생했다"와 "시간이 X만큼 경과했다"를 구분하지 못한다.
- **직접 정수 비교로 오버플로 버그**: `if (jiffies > deadline)` 형태의 직접 비교는 jiffies가 오버플로(wrap-around)될 때 틀린 결과를 반환한다. 반드시 `time_after()` 매크로를 사용해야 한다.
- **나노초 정밀도가 필요한 곳에 jiffies 사용**: 오디오 타이밍, 고빈도 트레이딩 등 마이크로초 이하 정밀도가 필요한 곳에 jiffies를 사용하면 정밀도 부족으로 동작이 불안정해진다.
- **HZ를 단위로 시간 하드코딩**: `timeout = 250`처럼 HZ 값을 가정하고 하드코딩하면 HZ 설정이 다른 커널에서 동작이 달라진다. 반드시 `N * HZ`나 `msecs_to_jiffies(N)` 형태를 사용해야 한다.

기술사 관점에서는 Tick과 Jiffies를 "OS 저해상도 시간 관리의 기초 단위"로 설명하되, HZ와의 관계, 오버플로 처리, HRT와의 관계를 함께 언급해야 한다.

- **📢 섹션 요약 비유**: 똑딱 소리(Tick)와 센 숫자(Jiffies)를 함께 봐야 한다. 소리를 20번 들었고 1초에 10번 소리가 나면 2초가 지난 것을 알 수 있다.

---

## Ⅴ. 기대효과 및 결론

Tick/Jiffies 기반 시간 관리는 30년 이상 리눅스 커널에서 안정적으로 동작해 온 검증된 메커니즘이다. 오버헤드가 극히 낮으면서도 OS의 시간 기반 제어(스케줄링, 타임아웃, 슬립)에 필요한 기능을 충분히 제공한다.

현대 커널에서는 Tickless 커널(CONFIG_NO_HZ)과 결합하여, 유휴 상태에서는 Tick을 발생시키지 않아 전력 소비를 줄이고, 실행 중인 프로세스가 있을 때만 Tick을 발생시키는 적응적(adaptive) 동작을 한다. 이를 통해 서버, 모바일, 임베디드 환경 모두에서 에너지 효율을 높인다.

기술사 시험에서 Tick/Jiffies는 타이머 인터럽트 → jiffies → 스케줄러 → 컨텍스트 스위치라는 연결 고리를 완성하는 핵심 연결 개념이다. 단독으로 출제되기보다 OS 시간 관리, 스케줄링, Tickless 커널과 연계하여 출제된다. 결론적으로 Tick은 OS의 심장 박동이고, Jiffies는 그 박동 횟수를 세는 맥박계다.

- **📢 섹션 요약 비유**: 소리(Tick)와 횟수(Jiffies)를 따로 세는 것처럼, OS도 인터럽트 이벤트와 경과 시간을 구분하여 관리한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 타이머 인터럽트 | Tick 발생의 물리적 원천 |
| HZ | 초당 Tick 횟수, Jiffies 해상도 결정 |
| ktime_t | Jiffies의 고해상도 대안 |
| hrtimer | 고해상도 타이머, ktime_t 사용 |
| Tickless 커널 | 유휴 시 Tick 억제, Jiffies 업데이트 방식 변경 |
| 타이머 휠(Timer Wheel) | Jiffies 기반 타이머 자료구조 |
| 선점형 스케줄링 | Tick마다 시간 할당 검사 |
| time_after() | Jiffies 오버플로 안전 비교 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">PIT 기반 단순 인터럽트 → jiffies 카운터 도입</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">HZ 설정으로 Tick 주파수 조절 기능 추가</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">32비트 jiffies → 64비트 jiffies_64 도입 (오버플로 대응)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">ktime_t 도입 → 나노초 기반 고정밀 시간 표현</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">HRT (hrtimer) 도입 (Linux 2.6.16) → 고해상도 타이머</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Tickless Kernel (Linux 2.6.21) → 동적 Tick 억제</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Full Tickless (Linux 3.10) → 실행 중에도 Tick 억제 가능</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Time Namespace (Linux 5.6) → 컨테이너별 독립 jiffies</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 똑딱 시계가 소리를 낼 때마다(Tick) 칠판에 표시를 하나씩 그려요(Jiffies++).
2. 나중에 표시 개수를 세면 얼마나 시간이 지났는지 알 수 있어요.
3. 틱(Tick)은 소리, 지피스(Jiffies)는 그 소리를 센 숫자예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 73 / 800

← **이전**: [72. 타이머 인터럽트 - 선점형 스케줄링의 기반](/knowledge-base/studynote/02_operating_system/01_overview_architecture/072_timer_interrupt/)
**다음**: [74. 틱리스 커널 (Tickless Kernel)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/074_tickless_kernel/) →

---
