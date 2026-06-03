+++
title = "71. 운영체제 타이머 (Timer) - 시스템 클럭, 카운터"
date = 2026-03-21

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 타이머는 하드웨어 클럭 신호를 기반으로 주기적 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 발생시켜 CPU 시간 분배, 시스템 시간 유지, 타임아웃 관리를 담당하는 OS의 시간 제어 장치다.
> 2. **가치**: [선점형 스케줄링](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/166_preemptive_scheduling/), 시간 측정, 슬립(Sleep) 구현, 타임아웃 감지의 기반이 되어 OS가 공정하고 반응적으로 동작할 수 있게 한다.
> 3. **판단**: 시스템 클럭(단순 시간 카운팅)과 타이머(인터럽트 생성)를 구분하고, HRT(High-Resolution Timer)와 저해상도 타이머의 트레이드오프를 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

OS는 시간이 흐른다는 것을 어떻게 알까? CPU는 스스로 시간을 재지 않는다. 대신 하드웨어 타이머(Timer)가 주기적인 전기 신호를 발생시키고, 이 신호가 CPU에 인터럽트(Interrupt)를 보낸다. OS는 이 인터럽트를 카운트하여 시간을 측정하고, 매 인터럽트마다 스케줄러를 호출하여 CPU를 어떤 프로세스가 사용할지 결정한다.

타이머가 없다면 OS는 시간 기반 제어가 불가능하다. 선점형 스케줄링(Preemptive Scheduling)은 "일정 시간이 지나면 현재 프로세스에서 CPU를 빼앗는" 방식인데, 시간을 재는 타이머가 없으면 구현이 불가능하다. 또한 `sleep(1)`, `timeout(5s)` 같은 시간 기반 API, 네트워크 TCP 재전송 타이머, 파일시스템 저널 플러시 주기 등 OS 전반에 걸쳐 타이머가 필수적이다.

초기 OS는 단순히 일정 주기의 클럭 인터럽트(Clock Interrupt, Tick)에만 의존했다. 그러나 실시간 시스템과 고해상도 타이머 수요가 증가하면서, 리눅스는 커널 2.6.16(2006)부터 HRT(High-Resolution Timers)를 도입하여 나노초 단위의 정밀 타이머를 지원하기 시작했다. 현대 OS는 전통 틱 기반 타이머와 고해상도 타이머를 함께 운용한다.

- **📢 섹션 요약 비유**: 교실에서 수업을 진행하려면 학교 종(타이머)이 필요하다. 종이 울려야 수업 시작과 종료를 알 수 있고, 쉬는 시간을 관리할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### OS 타이머 계층 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">하드웨어 레벨</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">물리적 타이머 하드웨어</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PIT (x86)</div><div class="kb-diagram-cell">HPET (x86)</div><div class="kb-diagram-cell">TSC</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">8253/8254</div><div class="kb-diagram-cell">(고정밀)</div><div class="kb-diagram-cell">(나노초)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">APIC Timer / ARM Generic Timer</div></div>
<div class="kb-diagram-note">IRQ (인터럽트)</div>
<div class="kb-diagram-note">커널 레벨</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Clocksource Framework (클럭 소스 추상화)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Timer Interrupt Handler (타이머 인터럽트 핸들러)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ jiffies 업데이트 (저해상도)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ ktime 업데이트 (고해상도)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ tick_handle_periodic() 호출</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 스케줄러 호출 (scheduler_tick())</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 타이머 휠(Timer Wheel) 만료 검사</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 계정(Accounting): CPU 사용 시간 집계</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">HRT 서브시스템 (High-Resolution Timer)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ hrtimer_interrupt() → 나노초 단위 만료 처리</div></div>
</div>
</div>



### 주요 하드웨어 타이머 종류

| 타이머 | 해상도 | 특징 | 용도 |
| :--- | :--- | :--- | :--- |
| PIT (Programmable Interval Timer) | ~838ns | 고전 x86 타이머, 가장 단순 | 레거시 틱 생성 |
| HPET (High Precision Event Timer) | 100ns 이상 | 멀티코어에서 공유, 고해상도 | HRT, 시스템 시간 |
| TSC (Time Stamp Counter) | ~1ns | CPU 사이클 카운터, 최고 정밀 | 고성능 시간 측정 |
| APIC Timer | 프로세서별 | CPU별 독립 타이머, 로컬 | 선점 타이머 |
| ARM Generic Timer | 1~10ns | ARM 표준 타이머, 64비트 | 모바일/임베디드 |
| RTC (Real Time Clock) | 1초 | 배터리 유지, 절전 모드에서도 동작 | 실제 시각 유지 |

### 주요 타이머 자료구조 (Linux)

| 자료구조 | 설명 | 해상도 |
| :--- | :--- | :--- |
| jiffies | 부팅 이후 틱 횟수 카운터 | HZ 단위 (보통 250~1000 Hz) |
| ktime_t | 나노초 단위 커널 시간 | 나노초 |
| timespec64 | 초 + 나노초 구조체 | 나노초 |
| hrtimer | 고해상도 타이머 구조체 | 나노초 |
| timer_list | 저해상도 타이머 구조체 | jiffies 단위 |

### 타이머 휠 (Timer Wheel) 구조

타이머 휠은 만료 시간이 가까운 타이머부터 효율적으로 관리하는 자료구조다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">현재 시간(jiffies) = T</div>
<div class="kb-diagram-note">타이머 만료 시간에 따른 버킷 분류:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">T+1   ~ T+8</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">Level 0 버킷 (0~7) : 매우 가까운 타이머</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">T+9   ~ T+64</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">Level 1 버킷 (8~15) : 가까운 타이머</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">T+65  ~ T+512</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">Level 2 버킷 : 중간 타이머</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">T+513 ~ T+4096</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">Level 3 버킷 : 먼 타이머</div></div>
<div class="kb-diagram-note">...</div>
<div class="kb-diagram-note">→ 각 틱마다 현재 시간에 해당하는 버킷만 검사 → O(1) 복잡도</div>
</div>
</div>



### 타이머 동작 흐름

```
1. 하드웨어 타이머가 일정 간격으로 IRQ 발생
2. CPU가 현재 명령을 중단하고 Timer ISR(Interrupt Service Routine) 진입
3. jiffies / ktime 업데이트
4. 만료된 타이머 처리 (timer_list, hrtimer)
5. scheduler_tick() 호출
   - 현재 프로세스의 CPU 사용 시간 증가
   - 시간 할당(Time Quantum) 만료 확인
   - 선점 필요 시 TIF_NEED_RESCHED 플래그 설정
6. 인터럽트 반환 후 스케줄러 호출 (선점 발생)
```

- **📢 섹션 요약 비유**: 타이머는 교실의 벨이다. 벨이 울리면 선생님(OS)이 학생들(프로세스)에게 차례를 바꾸라고 알리고, 남은 수업 시간(CPU 할당량)을 계산한다.

---

## Ⅲ. 비교 및 연결

### 클럭 vs 타이머 vs 카운터 비교

| 항목 | 시스템 클럭(Clock) | 타이머(Timer) | 카운터(Counter) |
| :--- | :--- | :--- | :--- |
| 역할 | 기준 주파수 신호 생성 | 일정 간격 인터럽트 발생 | 경과 틱 누적 |
| 해상도 | 수십 GHz (CPU 클럭) | 설정 가능 (1ms~100ns) | 타이머 해상도 의존 |
| OS 의존 | 하드웨어 독립 | OS 커널이 관리 | OS가 유지 (jiffies) |
| 사용 예 | CPU 동작 속도 | 스케줄링 인터럽트 | 경과 시간 계산 |

### 저해상도 타이머 vs 고해상도 타이머

| 항목 | 저해상도 타이머 (Low-Res) | 고해상도 타이머 (HRT) |
| :--- | :--- | :--- |
| 해상도 | 1/HZ 초 (1~4ms) | 나노초 수준 |
| 자료구조 | timer_list (타이머 휠) | hrtimer |
| 인터럽트 | 정기 틱마다 처리 | 만료 시점에 즉시 처리 |
| 오버헤드 | 낮음 | 약간 높음 |
| 용도 | 일반 타임아웃, 슬립 | 실시간 오디오, 정밀 제어 |
| 리눅스 도입 | 초기부터 | 2.6.16 (2006) |

### 관련 OS 기능과의 연결

| 기능 | 타이머 활용 방식 |
| :--- | :--- |
| 선점형 스케줄링 | 타이머 인터럽트로 time quantum 만료 감지 |
| sleep() / usleep() | hrtimer로 정확한 대기 시간 구현 |
| TCP 재전송 타이머 | 네트워크 스택 내 소프트 타이머 |
| 파일시스템 sync | 주기적 타이머로 dirty page 플러시 |
| watchdog | 타이머 미갱신 시 시스템 리셋 |
| 전력 관리(Tickless) | 유휴 시 타이머 인터럽트 중단 → 절전 |

- **📢 섹션 요약 비유**: 벨이 울리면 수업 순서가 바뀌고(스케줄링), 타이머가 꺼지면 쉬는 시간(절전 모드)이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. 시스템 클럭(하드웨어)과 OS 타이머(소프트웨어)의 역할 차이를 명확히 이해하는가?
2. HZ 값(타이머 인터럽트 주파수)이 시스템 성격(서버/임베디드/실시간)에 맞게 설정되는가?
3. 고해상도 타이머(HRT)와 저해상도 타이머(timer_list)의 용도를 구분하는가?
4. Tickless 커널(CONFIG_NO_HZ)이 전력 관리와 어떻게 연결되는가?
5. 타이머 휠(Timer Wheel)의 O(1) 만료 처리 원리를 이해하는가?
6. 타이머 드리프트(Timer Drift)나 jitter 문제에 대한 대응 방안이 있는가?
7. 실시간 시스템(PREEMPT_RT)에서 타이머 정밀도 요구사항이 충족되는가?
8. TSC 기반 clocksource 사용 시 다중 소켓 환경의 TSC 동기화 문제를 고려했는가?

### 안티패턴

- **클럭과 타이머 혼동**: 시스템 클럭(CPU 동작 주파수)과 OS 타이머(인터럽트 주기)를 같은 개념으로 이해하면 설계 오류가 발생한다. 3GHz CPU에서도 HZ=250이면 타이머 인터럽트는 초당 250번만 발생한다.
- **HZ 값 무조건 높게 설정**: HZ=1000으로 설정하면 정밀도가 높지만 초당 1000번의 인터럽트가 발생하여 인터럽트 처리 오버헤드가 증가한다. 서버는 HZ=100~250, 실시간 시스템은 HZ=1000이 일반적이다.
- **busy-wait 루프로 시간 대기**: `while (time < target) {}` 형태의 바쁜 대기(Busy-Wait)는 CPU를 100% 점유한다. 반드시 `sleep()`, `nanosleep()` 등 타이머 기반 대기를 사용해야 한다.
- **타이머 콜백에서 긴 작업 수행**: 타이머 인터럽트 컨텍스트에서 오래 걸리는 작업을 실행하면 다른 인터럽트가 지연된다. 워크큐(Workqueue)나 소프트IRQ로 위임해야 한다.

기술사 관점에서는 OS 타이머를 "시간 기반 제어의 기반 메커니즘"으로 설명하되, 스케줄링과의 연결(timer interrupt → scheduler_tick → context switch), HRT와 절전(Tickless Kernel)과의 관계까지 함께 서술해야 한다.

- **📢 섹션 요약 비유**: 학교 종이 시간의 흐름을 알려 주듯, OS 타이머는 커널에게 "지금 몇 시인지, 다음 수업으로 넘어갈 시간인지"를 알려 준다.

---

## Ⅴ. 기대효과 및 결론

OS 타이머는 멀티태스킹, 실시간 응답, 전력 관리 등 현대 OS의 핵심 기능 전반을 뒷받침한다. 타이머 인터럽트의 주기(HZ)를 적절히 설정하면 응답성(Responsiveness)과 효율성(Efficiency) 사이의 균형을 맞출 수 있다. 서버 환경에서는 HZ=250 설정이 인터럽트 오버헤드를 줄이면서도 충분한 스케줄링 정밀도를 제공한다.

고해상도 타이머(HRT)는 나노초 단위의 정밀 제어를 가능하게 하여 실시간 오디오/비디오 처리, 고빈도 트레이딩 시스템, 산업용 제어 시스템 등에서 필수적이다. Tickless 커널과 결합하면 유휴 상태에서 타이머 인터럽트를 중단하여 배터리 수명과 에너지 효율을 크게 향상시킨다.

현대 클라우드 환경에서는 가상화로 인한 타이머 정밀도 저하(VM clock drift) 문제가 있다. 이를 해결하기 위해 KVM의 kvmclock, Xen의 PV timer 등 가상화 친화적 타이머 인터페이스가 개발되어 있다. 결론적으로 OS 타이머는 스케줄링과 시간 제어의 핵심 장치로, 성능/정밀도/전력 소비의 트레이드오프를 이해하고 시스템 특성에 맞게 조정하는 것이 기술사 판단의 핵심이다.

- **📢 섹션 요약 비유**: 좋은 시계(타이머)가 있어야 효율적인 시간표(스케줄링)를 만들 수 있고, 쉬는 시간(절전)도 잘 활용할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 타이머 인터럽트 | OS 타이머의 작동 메커니즘 |
| jiffies | 타이머 틱 기반의 저해상도 커널 시간 |
| HRT (High-Resolution Timer) | 나노초 단위 정밀 타이머 |
| 선점형 스케줄링 | 타이머 인터럽트로 구현됨 |
| Tickless 커널 | 유휴 시 타이머 인터럽트 중단, 절전 |
| HPET/TSC | 고해상도 하드웨어 타이머 |
| 실시간 커널(PREEMPT_RT) | 타이머 정밀도가 핵심 |
| clocksource | 리눅스 타이머 하드웨어 추상화 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">PIT (8253) → 단순 틱 기반 인터럽트 (초기 Unix/Linux)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">jiffies 도입 → 저해상도 타이머 관리</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">HPET 도입 → 고정밀 이벤트 타이머 (Linux 2.6)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">HRT 도입 (Linux 2.6.16, 2006) → 나노초 정밀</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Tickless 커널 (Linux 2.6.21, 2007) → 절전 최적화</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">clocksource/clockevent 프레임워크 → 타이머 추상화</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">가상화 환경: kvmclock, Xen PV timer</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Time Namespace (Linux 5.6) → 컨테이너별 독립 시간</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 학교에 종이 없으면 수업 시작과 끝을 모르겠죠? 컴퓨터도 타이머가 없으면 언제 다음 프로그램으로 넘어가야 할지 몰라요.
2. 타이머가 딩동 울릴 때마다 OS가 "이번엔 어떤 프로그램이 CPU를 쓸 차례인지" 결정해요.
3. 좋은 타이머가 있으면 공평하게 시간을 나눌 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 71 / 800

← **이전**: [70. 하드웨어 추상화 계층 (HAL, Hardware Abstraction Layer)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/070_hal/)
**다음**: [72. 타이머 인터럽트 - 선점형 스케줄링의 기반](/knowledge-base/studynote/02_operating_system/01_overview_architecture/072_timer_interrupt/) →

---
