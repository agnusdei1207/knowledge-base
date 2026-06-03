+++
title = "72. 타이머 인터럽트 - 선점형 스케줄링의 기반"
date = 2026-03-21

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 타이머 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)는 일정 주기마다 CPU의 현재 실행을 강제로 중단시키고 OS 커널이 제어권을 되찾게 하는 하드웨어 메커니즘이다.
> 2. **가치**: 선점형 스케줄링(Preemptive Scheduling)과 시간 분할(Time-Slicing)의 물리적 기반이며, 이를 통해 다중 프로세스가 CPU를 공정하게 나눠 쓸 수 있다.
> 3. **판단**: 타이머 인터럽트 없이는 비협조적인 프로세스가 CPU를 독점할 수 있으므로, 시스템 응답성과 공정성의 핵심 보장 장치다.

---

## Ⅰ. 개요 및 필요성

멀티태스킹 OS가 등장하기 전, 하나의 프로그램이 CPU를 독점하고 끝날 때까지 다른 프로그램은 기다려야 했다. 비협조적 다중 프로그래밍(Non-preemptive Multiprogramming)이라 불리는 이 방식에서는 한 프로그램이 무한 루프에 빠지면 전체 시스템이 멈춰 버린다. 이를 해결하기 위해 "OS가 강제로 CPU를 빼앗을 수 있는" 선점(Preemption) 개념이 탄생했다.

그런데 OS가 CPU를 빼앗으려면, 현재 실행 중인 프로그램이 자발적으로 제어권을 넘기지 않더라도 OS가 개입할 수 있어야 한다. 이것이 가능한 이유는 바로 타이머 인터럽트(Timer Interrupt) 덕분이다. 하드웨어 타이머가 주기적으로 전기 신호(인터럽트)를 CPU에 보내면, CPU는 현재 실행 중인 코드를 멈추고 OS의 인터럽트 서비스 루틴(ISR)을 실행한다. OS는 이 순간을 이용해 현재 프로세스의 실행 시간을 계산하고, 필요하면 다른 프로세스로 컨텍스트 스위치를 수행한다.

타이머 인터럽트는 단순한 "알람"이 아니다. OS가 시스템 전반을 제어하는 유일한 정기적 진입점이다. 타이머 인터럽트 핸들러 내에서는 스케줄링 결정, CPU 사용 시간 계정(Accounting), 타임아웃 처리, 소프트 타이머 만료 확인 등 OS의 핵심 관리 작업이 이루어진다.

- **📢 섹션 요약 비유**: 놀이터에서 아이들이 놀고 있을 때, 선생님이 종을 울리면 즉시 돌아봐야 한다. 타이머 인터럽트는 그 종이다. 어떤 아이가 얼마나 오래 놀았는지 확인하고, 다음 차례를 정한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 타이머 인터럽트 전체 처리 흐름



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">하드웨어 타이머</div></div>
<div class="kb-diagram-note">주기마다 (1/HZ 초, 예: HZ=250이면 4ms마다)</div>
<div class="kb-diagram-note">IRQ 신호 → CPU의 인터럽트 핀으로 전송</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">CPU 하드웨어 처리</div></div>
<div class="kb-diagram-note">현재 명령 실행 완료 후</div>
<div class="kb-diagram-note">IF (Interrupt Flag) 확인</div>
<div class="kb-diagram-note">→ 현재 레지스터 상태 스택 저장 (자동)</div>
<div class="kb-diagram-note">→ IDT(Interrupt Descriptor Table)에서 ISR 주소 조회</div>
<div class="kb-diagram-note">→ 커널 모드로 전환 (Ring 3 → Ring 0)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">커널 ISR: timer_interrupt() 실행</div></div>
<div class="kb-diagram-tree-item" style="--depth:1">1. jiffies / ktime 카운터 증가</div>
<div class="kb-diagram-tree-item" style="--depth:1">2. tick_handle_periodic() 호출</div>
<div class="kb-diagram-note">─ scheduler_tick() 호출</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 현재 프로세스 vruntime 업데이트 (CFS)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ time quantum 소진 확인</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ TIF_NEED_RESCHED 플래그 설정 (필요 시)</div></div>
<div class="kb-diagram-note">─ run_local_timers() - 만료된 timer_list 처리</div>
<div class="kb-diagram-note">─ hrtimer_run_queues() - 고해상도 타이머 처리</div>
<div class="kb-diagram-note">─ update_process_times() - CPU 사용 통계</div>
<div class="kb-diagram-tree-item" style="--depth:1">3. EOI (End of Interrupt) 신호 → 인터럽트 컨트롤러</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">인터럽트 반환 시점</div></div>
<div class="kb-diagram-note">TIF_NEED_RESCHED가 설정된 경우</div>
<div class="kb-diagram-note">→ schedule() 호출</div>
<div class="kb-diagram-note">→ 다음 프로세스 선택 (스케줄러)</div>
<div class="kb-diagram-note">→ 컨텍스트 스위치(Context Switch) 수행</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">다음 프로세스 실행</div></div>
</div>
</div>



### 선점 메커니즘 상세

| 단계 | 동작 | 관여 컴포넌트 |
| :--- | :--- | :--- |
| 틱 발생 | 타이머 하드웨어가 IRQ 발생 | PIT/APIC Timer |
| ISR 진입 | CPU가 커널 모드로 전환 | CPU 하드웨어 |
| 시간 측정 | 현재 프로세스의 CPU 시간 증가 | timer_interrupt() |
| 선점 판단 | time quantum 초과 여부 확인 | scheduler_tick() |
| 플래그 설정 | TIF_NEED_RESCHED 설정 | 스케줄러 |
| 컨텍스트 스위치 | ISR 반환 시 다음 프로세스로 전환 | schedule() |

### TIF_NEED_RESCHED 플래그 메커니즘



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">scheduler_tick()에서 time quantum 초과 감지</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">set_tsk_need_resched(current) 호출</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">TIF_NEED_RESCHED 플래그 설정</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">인터럽트 반환 시 preempt_schedule_irq() 호출</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">schedule() → 다음 실행 프로세스 선택</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">switch_to(prev, next) → 컨텍스트 스위치</div>
</div>
</div>



### 타이머 인터럽트 주기(HZ)와 영향

| HZ 값 | 인터럽트 주기 | 장점 | 단점 | 적합 환경 |
| :--- | :--- | :--- | :--- | :--- |
| 100 | 10ms | 오버헤드 최소 | 스케줄링 지연 큼 | 서버(처리량 중심) |
| 250 | 4ms | 균형 | 균형 | 일반 서버/데스크톱 |
| 300 | 3.33ms | 균형 | 균형 | 일부 Linux 배포판 |
| 1000 | 1ms | 응답성 최고 | CPU 오버헤드 증가 | 실시간, 오디오 |

### 선점형 vs 비선점형 스케줄링 비교

| 항목 | 선점형(Preemptive) | 비선점형(Non-preemptive) |
| :--- | :--- | :--- |
| 타이머 인터럽트 역할 | 강제 선점의 트리거 | 사용되지 않음 |
| 프로세스 독점 가능성 | 없음 (time quantum 제한) | 있음 |
| 응답성 | 높음 | 낮음 |
| 구현 복잡도 | 높음 | 낮음 |
| OS 제어권 | 항상 유지 | 프로세스에 의존 |
| 예시 | Linux, Windows NT | 협력적 멀티태스킹(초기 macOS) |

- **📢 섹션 요약 비유**: 학교 종이 울리면 학생들이 하던 일을 멈추고 다음 수업으로 이동하듯, 타이머 인터럽트가 울리면 현재 프로세스가 멈추고 스케줄러가 다음 프로세스를 선택한다.

---

## Ⅲ. 비교 및 연결

### 타이머 인터럽트 vs 다른 인터럽트 비교

| 항목 | 타이머 인터럽트 | 하드웨어 인터럽트 (일반) | 소프트웨어 인터럽트(시스템 콜) |
| :--- | :--- | :--- | :--- |
| 발생 주체 | 하드웨어 타이머 | 장치(NIC, 디스크 등) | 사용자 프로그램 |
| 발생 주기 | 정기적 (주기적) | 비정기적 (이벤트 기반) | 비정기적 (호출 기반) |
| 주 목적 | 스케줄링, 시간 관리 | 데이터 수신/전송 알림 | OS 서비스 요청 |
| 선점 역할 | 핵심 선점 메커니즘 | 인터럽트 처리 중 선점 가능 | 해당 없음 |

### 타이머 인터럽트와 스케줄러의 관계



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">타이머 인터럽트 → scheduler_tick() → CFS(완전 공정 스케줄러)</div>
<div class="kb-diagram-tree-item" style="--depth:8">가상 런타임(vruntime) 업데이트</div>
<div class="kb-diagram-tree-item" style="--depth:8">우선순위 재계산</div>
<div class="kb-diagram-tree-item" style="--depth:8">선점 필요 시 TIF_NEED_RESCHED 설정</div>
</div>
</div>



### 관련 OS 기능과 타이머 인터럽트 연결

| 기능 | 타이머 인터럽트 역할 |
| :--- | :--- |
| 선점형 스케줄링 | time quantum 만료 감지 및 프로세스 전환 |
| CPU 사용 시간 통계 | `/proc/stat`, `top` 등 CPU% 계산 기반 |
| POSIX 시그널 (SIGALRM) | 타이머 기반 시그널 전달 |
| sleep()/nanosleep() | 타이머 인터럽트로 슬립 해제 시점 감지 |
| 네트워크 재전송 타이머 | TCP keepalive, 재전송 타임아웃 |
| 프로파일링 | gprof, perf의 샘플링 기반 |

### 컨텍스트 스위치와의 관계

타이머 인터럽트는 컨텍스트 스위치를 <strong>강제</strong>할 수 있는 유일한 정기적 메커니즘이다. 인터럽트 반환 경로에서 TIF_NEED_RESCHED 플래그가 설정되어 있으면 `switch_to()`가 호출되어 CPU 레지스터, 스택 포인터, 프로그램 카운터 등이 다음 프로세스의 것으로 교체된다.

- **📢 섹션 요약 비유**: 순번대로 차례를 바꾸게 하는 신호다. 타이머가 울리지 않으면 한 사람이 계속 자기 차례를 점유할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. 타이머 인터럽트 주기(HZ)가 시스템의 응답성 요구사항과 맞는가?
2. 타이머 인터럽트 핸들러에서 수행하는 작업이 최소화되어 있는가? (인터럽트 지연 방지)
3. 선점형 커널(CONFIG_PREEMPT)이 활성화되어 있는가? (실시간 응답성)
4. PREEMPT_RT 패치가 필요한 실시간 요구사항이 있는가?
5. 타이머 인터럽트와 컨텍스트 스위치 오버헤드가 성능 병목이 되는가?
6. 멀티코어 환경에서 per-CPU 타이머와 글로벌 타이머의 역할 분담이 적절한가?
7. Tickless 커널(CONFIG_NO_HZ)과의 병행 설계를 고려했는가?
8. 인터럽트 핸들러에서 스핀락(Spinlock) 사용이 최소화되어 있는가?

### 안티패턴

- **타이머 없이 폴링(Polling)만 하는 설계**: 타이머 인터럽트 대신 `while (condition) {}` 형태의 폴링으로 상태를 확인하면 CPU를 100% 점유하여 다른 프로세스가 실행되지 못한다. 인터럽트 기반 비동기 처리가 표준이다.
- **선점 개념 없이 CPU를 공유하는 설계**: 비선점형 스케줄링은 협력적 다중 프로그래밍에서만 유효하다. 현대 범용 OS에서는 선점형 스케줄링이 필수이며, 타이머 인터럽트가 그 기반이다.
- **인터럽트 핸들러에서 긴 처리 수행**: 타이머 ISR 내에서 블로킹 작업이나 긴 연산을 수행하면 다른 인터럽트가 지연된다. 무거운 작업은 소프트IRQ(SoftIRQ)나 워크큐(Workqueue)로 위임해야 한다.
- **타이머 인터럽트 비용 무시**: HZ=1000으로 설정하면 초당 1000번의 컨텍스트 스위치가 발생할 수 있다. 시스템 특성에 맞는 HZ 값을 선택해야 한다.

기술사 관점에서는 타이머 인터럽트를 "선점형 스케줄링의 트리거"로 명확히 설명하되, ISR에서 스케줄러까지의 흐름(타이머 틱 → scheduler_tick() → TIF_NEED_RESCHED → schedule() → switch_to())을 연결해서 서술해야 한다.

- **📢 섹션 요약 비유**: 종이 울려야 다음 학생이 들어오듯, 타이머 인터럽트가 울려야 OS가 다음 프로세스를 선택할 기회를 얻는다.

---

## Ⅴ. 기대효과 및 결론

타이머 인터럽트는 현대 OS의 다중 프로그래밍 모델을 실현하는 물리적 기반이다. 이 메커니즘 덕분에 수십~수백 개의 프로세스가 단일 CPU(또는 멀티코어)를 공평하게 나눠 사용할 수 있고, 사용자는 마치 프로그램들이 동시에 실행되는 것처럼 느낄 수 있다.

응답성 측면에서는 HZ=1000 설정 시 1ms 단위로 스케줄링이 가능해져 오디오 스트리밍, UI 렌더링 같은 지연 민감 애플리케이션이 끊김 없이 동작한다. 안정성 측면에서는 어떤 프로세스도 CPU를 독점할 수 없으므로 전체 시스템의 응답성이 보장된다. Tickless 커널과 결합하면 유휴 상태에서 타이머 인터럽트를 중단하여 전력 소비를 줄이는 것도 가능하다.

결론적으로 타이머 인터럽트는 단순한 "주기 신호"가 아니라, OS가 시스템의 주도권을 유지하는 핵심 메커니즘이다. 스케줄링, 시간 관리, 타임아웃 처리, CPU 통계 수집 등 OS의 핵심 기능이 모두 이 인터럽트를 발판으로 동작한다.

- **📢 섹션 요약 비유**: 시간을 나누는 학교 종처럼, 타이머 인터럽트가 울려야 공평한 CPU 분배가 가능하고 시스템 전체가 원활하게 돌아간다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| OS 타이머(Timer) | 타이머 인터럽트의 하드웨어 발생 원천 |
| 선점형 스케줄링 | 타이머 인터럽트로 구현되는 핵심 기능 |
| 컨텍스트 스위치 | 타이머 인터럽트 후 발생하는 프로세스 전환 |
| jiffies | 타이머 인터럽트 카운트의 누적값 |
| HZ (Hz) | 초당 타이머 인터럽트 발생 횟수 |
| TIF_NEED_RESCHED | 선점 필요 신호 플래그 |
| Tickless 커널 | 유휴 시 타이머 인터럽트 억제 |
| PREEMPT_RT | 실시간 선점성 강화 패치 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">협력적 멀티태스킹 (프로세스 자발적 양보)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">선점형 스케줄링 필요성 → 타이머 인터럽트 도입</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">PIT 기반 단순 틱 인터럽트 (초기 Linux)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">APIC Timer: CPU별 독립 타이머 인터럽트</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">HRT (고해상도 타이머) → 나노초 정밀 인터럽트</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Tickless Kernel: 유휴 시 틱 억제</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">PREEMPT_RT: 인터럽트 핸들러도 선점 가능</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Full Tickless (Linux 3.10+): 완전 이벤트 기반</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 놀이터에서 아이들이 미끄럼틀을 혼자 오래 쓰면 안 되잖아요? 선생님이 종을 울려 다음 사람에게 차례를 줘요.
2. 타이머 인터럽트는 그 종이에요. CPU가 한 프로그램을 너무 오래 실행하면 "이제 바꿔!"라고 알려 줘요.
3. 덕분에 여러 프로그램이 CPU를 공평하게 나눠 쓸 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 72 / 800

← **이전**: [71. 운영체제 타이머 (Timer) - 시스템 클럭, 카운터](/knowledge-base/studynote/02_operating_system/01_overview_architecture/071_os_timer/)
**다음**: [73. 틱 (Tick) / 지피스 (Jiffies)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/073_tick_jiffies/) →

---
