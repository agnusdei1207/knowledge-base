+++
title = "74. 틱리스 커널 (Tickless Kernel)"
date = 2026-03-21

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 틱리스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)(Tickless Kernel, CONFIG_NO_HZ)은 아무 작업이 없는 유휴(Idle) 상태에서 주기적 타이머 인터럽트를 중단하여 전력 소비와 인터럽트 오버헤드를 줄이는 커널 설계다.
> 2. **가치**: 모바일/임베디드 환경에서 배터리 수명을 연장하고, 서버 환경에서는 불필요한 인터럽트 오버헤드를 제거하여 NoHz_Full 모드에서 CPU 독점 성능을 극대화할 수 있다.
> 3. **판단**: "Tickless"는 틱을 완전히 제거하는 것이 아니라 "필요하지 않을 때 틱을 억제하는" 동적 틱(Dynamic Tick) 메커니즘이며, jiffies 업데이트와 스케줄링 정확성을 유지한다.

---

## Ⅰ. 개요 및 필요성

전통적인 리눅스 커널은 초당 HZ번(250Hz면 4ms마다) 타이머 인터럽트를 발생시켰다. 이는 CPU가 완전히 유휴(Idle) 상태여도 예외가 없었다. 노트북이 아무것도 하지 않는 동안에도 초당 250번씩 CPU가 깨어나 타이머 핸들러를 실행하고 다시 유휴 상태로 돌아가야 했다. 이는 배터리를 지속적으로 소모하는 불필요한 낭비였다.

틱리스 커널(Tickless Kernel, NO_HZ)은 이 문제를 해결하기 위해 리눅스 2.6.21(2007)에 도입되었다. 핵심 아이디어는 단순하다: "CPU가 유휴 상태일 때는 다음 실제 이벤트(타이머 만료, 인터럽트)가 발생할 때까지 타이머를 끈다." 이를 통해 유휴 상태에서 CPU는 깊은 절전(Deep Sleep) 상태(C-state)로 진입하여 전력 소비를 대폭 줄일 수 있다.

틱리스 커널은 세 가지 모드로 발전했다:
- **CONFIG_NO_HZ_IDLE** (Linux 2.6.21): 유휴 CPU에서만 틱 억제 → 가장 일반적
- **CONFIG_NO_HZ_FULL** (Linux 3.10): 실행 중인 프로세스가 1개뿐인 CPU도 틱 억제 → HPC/게임용
- **CONFIG_HZ_PERIODIC** (레거시): 전통적 주기 틱, 모든 상황에서 틱 발생

틱리스 커널은 모바일(Android), 임베디드(IoT), 서버(대기 시간 최소화) 모두에서 중요한 설계 요소다. 현재 대부분의 리눅스 배포판에서 CONFIG_NO_HZ_IDLE이 기본 활성화되어 있다.

- **📢 섹션 요약 비유**: 아무도 없는 교실에서는 종을 울릴 필요가 없다. 누군가 들어올 때 종을 울리면 된다. 틱리스 커널은 그런 스마트한 종이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 전통 주기 틱 vs 틱리스 커널 비교



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">전통 주기 틱 (CONFIG_HZ_PERIODIC)</div></div>
<div class="kb-diagram-note">시간 → T T+4ms T+8ms T+12ms T+16ms ...</div>
<div class="kb-diagram-note">틱 → ↑ ↑ ↑ ↑ ↑</div>
<div class="kb-diagram-note">인터럽트 발생 (CPU 유휴 중에도 계속)</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">틱리스 커널 (CONFIG_NO_HZ_IDLE)</div></div>
<div class="kb-diagram-note">시간 → T T+4ms T+8ms T+50ms T+54ms</div>
<div class="kb-diagram-note">CPU → 실행 유휴 유휴 타이머만료 실행</div>
<div class="kb-diagram-note">틱 → ↑ ↑ (억제) ↑ ↑</div>
<div class="kb-diagram-note">유휴 구간: 틱 없음</div>
<div class="kb-diagram-note">다음 이벤트까지 CPU 절전</div>
</div>
</div>



### 틱리스 커널 동작 흐름



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">프로세스 종료 / CPU 유휴 진입</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">tick_nohz_idle_enter() 호출</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">다음 타이머 이벤트 시각 계산</div>
<div class="kb-diagram-note">next_event = min(hrtimer 만료, timer_list 만료, 스케줄러 이벤트)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">clockevent 프로그래밍 (next_event 시각에만 인터럽트 발생하도록)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">CPU → 절전 모드(C-state) 진입</div>
<div class="kb-diagram-note">C1: 클럭 일시 중지</div>
<div class="kb-diagram-note">C2: 캐시 플러시, 깊은 절전</div>
<div class="kb-diagram-note">C3: DRAM 셀프 리프레시, 최대 절전</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">next_event 시각 도달 또는 다른 인터럽트 발생</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">CPU 깨어남 → tick_nohz_idle_exit() 호출</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">빠진 jiffies 일괄 업데이트 (tick_do_update_jiffies64)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">만료된 타이머 처리 → 스케줄러 실행</div>
</div>
</div>



### CONFIG_NO_HZ 세 가지 모드 비교

| 모드 | 대상 | 틱 억제 조건 | 주요 사용처 |
| :--- | :--- | :--- | :--- |
| CONFIG_HZ_PERIODIC | 모든 CPU | 억제 없음 (항상 틱) | 레거시, 실시간 |
| CONFIG_NO_HZ_IDLE | 유휴 CPU | CPU가 완전 유휴일 때 | 일반 서버, 모바일 |
| CONFIG_NO_HZ_FULL | 유휴+단일실행 CPU | 실행 중 프로세스 1개면 억제 | HPC, 게임, 초저지연 |

### NO_HZ_FULL 모드의 의미



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">NO_HZ_FULL 적용 시</div></div>
<div class="kb-diagram-note">일반 CPU(0번): 커널 스레드, 관리 작업 → 주기 틱 유지</div>
<div class="kb-diagram-note">고성능 CPU(1~N번): 사용자 프로세스 1개 실행 중</div>
<div class="kb-diagram-note">→ 타이머 인터럽트 완전 억제</div>
<div class="kb-diagram-note">→ CPU 100% 응용 프로그램에 전달</div>
<div class="kb-diagram-note">→ 컨텍스트 스위치 최소화</div>
<div class="kb-diagram-note">효과: 초당 수백 번의 인터럽트 오버헤드 제거</div>
<div class="kb-diagram-note">CPU 독점 실행으로 캐시 효율 극대화</div>
<div class="kb-diagram-note">레이턴시-민감 애플리케이션 성능 향상</div>
</div>
</div>



### 틱리스 커널에서 jiffies 업데이트

전통 방식에서는 매 틱마다 jiffies를 1씩 증가시켰다. 틱리스 환경에서는 여러 틱을 건너뛸 수 있으므로, CPU가 절전에서 깨어날 때 경과한 시간을 일괄 계산하여 jiffies를 한 번에 업데이트한다.

```c
/* 틱리스 커널의 jiffies 복구 */
void tick_do_update_jiffies64(ktime_t now)
{
    u64 delta = ktime_to_ns(ktime_sub(now, last_jiffies_update));
    u64 ticks = delta / tick_period;
    /* 빠진 틱 수를 한 번에 jiffies에 반영 */
    jiffies_64 += ticks;
    last_jiffies_update = ktime_add_ns(last_jiffies_update,
                                       ticks * tick_period);
}
```

- **📢 섹션 요약 비유**: 종을 매번 치지 않고, 오랫동안 아무것도 없었다가 필요할 때 몇 번치 울렸는지를 계산해서 한 번에 알려 주는 스마트 종이다.

---

## Ⅲ. 비교 및 연결

### 틱리스 커널 전후 전력 소비 변화

| 항목 | 주기 틱 | 틱리스(NO_HZ_IDLE) | 차이 |
| :--- | :--- | :--- | :--- |
| 유휴 인터럽트 횟수 | 초당 250번 | 0~수 번 | 최대 100% 절감 |
| CPU 절전 진입 | 짧은 C-state 반복 | 긴 C-state 유지 | 깊은 절전 가능 |
| 배터리 영향 | 큼 | 줄어듦 | 모바일에서 수 시간 차이 |
| 인터럽트 지연 | 일정 (1/HZ) | 가변 (이벤트까지) | 예측성 다소 감소 |

### 틱리스 커널과 ACPI C-State 연계



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">유휴 진입 → 틱 억제 → 다음 이벤트까지 시간 계산</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">cpuidle 드라이버 선택 → 적절한 C-state 결정</div>
<div class="kb-diagram-note">짧은 유휴: C1 (클럭 멈춤, 빠른 복귀)</div>
<div class="kb-diagram-note">중간 유휴: C2 (전압 낮춤)</div>
<div class="kb-diagram-note">긴 유휴: C3/C6 (전원 게이트, 최대 절전)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">틱리스가 없으면 C3 이상 진입 불가 (인터럽트 대기 필요)</div>
<div class="kb-diagram-note">틱리스가 있어야 긴 절전 가능 → 전력 절감 극대화</div>
</div>
</div>



### 틱리스 커널과 실시간 시스템의 관계

| 항목 | CONFIG_NO_HZ_IDLE | PREEMPT_RT + 주기 틱 |
| :--- | :--- | :--- |
| 전력 소비 | 낮음 | 높음 |
| 타이머 정밀도 | 이벤트 의존 | 일정 (HZ 기준) |
| 실시간 응답성 | 보통 | 우수 |
| 적합 환경 | 배터리, 서버 | 산업용 실시간 제어 |

실시간 시스템(예: 산업용 로봇 제어)에서는 예측 가능한 인터럽트 지연이 필요하므로 주기 틱을 유지하는 경우도 있다. 틱리스와 실시간 요구사항은 트레이드오프 관계다.

- **📢 섹션 요약 비유**: 계속 울리는 알람 대신 필요할 때만 울리는 스마트 알람이다. 전력을 아끼지만, 정확한 시각에 울려야 하는 수술실 알람은 반드시 주기적으로 울려야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. 시스템이 모바일/임베디드 환경이라면 CONFIG_NO_HZ_IDLE이 활성화되어 있는가?
2. HPC(고성능 컴퓨팅) 환경이라면 CONFIG_NO_HZ_FULL로 CPU 독점 성능이 필요한가?
3. 실시간 시스템(산업용 제어)에서는 주기 틱이 필요한지 검토했는가?
4. 틱리스 환경에서 jiffies 기반 시간 측정이 정확하게 동작하는가?
5. 틱리스와 cpuidle/C-state가 올바르게 연동되는가?
6. 가상화 환경에서 게스트 VM의 틱리스 설정이 하이퍼바이저와 호환되는가?
7. NO_HZ_FULL 모드에서 rcu (Read-Copy-Update) 처리가 올바르게 동작하는가?
8. 틱리스 설정 후 타이머 정밀도 변화로 인한 애플리케이션 동작 변화를 검증했는가?

### 안티패턴

- **틱을 완전히 제거한다는 오해**: 틱리스 커널은 유휴 상태에서 틱을 억제하는 것이지, 틱을 완전히 없애지 않는다. 활성 CPU에서는 여전히 정기적 틱이 필요하다.
- **전력과 성능을 같이 보지 않는 설계**: 틱리스 커널이 항상 더 빠른 것은 아니다. 주기적 틱이 주는 예측 가능한 스케줄링 시점이 사라지면 일부 워크로드에서 지연이 증가할 수 있다.
- **가상화 환경에서 틱리스 미고려**: VM 환경에서 게스트 틱리스 설정이 하이퍼바이저의 타이머 가상화와 충돌하면 jiffies 드리프트나 타이머 부정확 문제가 발생한다.
- **실시간 시스템에 틱리스 적용**: 실시간 제어 시스템에서 틱리스를 적용하면 타이머 인터럽트 지연이 비결정적(Non-deterministic)이 되어 실시간성이 깨진다. 실시간 요구사항 시스템은 주기 틱과 PREEMPT_RT를 함께 사용해야 한다.

기술사 관점에서는 틱리스 커널을 "주기적 타이머 오버헤드 동적 감소 설계"로 설명하되, 전력 절감 효과(C-state 연계), NO_HZ_IDLE/FULL 모드 차이, 실시간 시스템과의 트레이드오프를 함께 언급해야 한다.

- **📢 섹션 요약 비유**: 꼭 필요할 때만 종이 울리게 하는 스마트 교실이다. 학생이 없을 때는 종을 치지 않아 에너지를 아끼지만, 학생이 들어오면 즉시 종을 울린다.

---

## Ⅴ. 기대효과 및 결론

틱리스 커널은 현대 OS에서 전력 효율과 성능 사이의 균형을 맞추는 핵심 기술이다. 모바일 환경(Android)에서는 배터리 수명 향상에 직접 기여하며, 스마트폰이 대기 모드에서 수십 시간 유지될 수 있는 이유 중 하나다. 서버 환경에서는 유휴 코어의 전력 소비를 줄여 데이터센터의 PUE(Power Usage Effectiveness)를 개선한다.

NO_HZ_FULL 모드를 활용하는 HPC(고성능 컴퓨팅) 환경에서는 초당 수백 번의 인터럽트 오버헤드를 제거하여 CPU가 100%를 계산에 사용할 수 있게 한다. 시뮬레이션, 과학 계산, 게임 서버 등 CPU 집약적 워크로드에서 체감 성능이 향상된다.

미래에는 IoT 기기의 초저전력 동작, ARM 기반 서버 확산, 에너지 효율 규제 강화 등으로 틱리스 기술의 중요성이 더욱 커질 것이다. 결론적으로 틱리스 커널은 "언제 타이머를 울릴 것인가"를 상황에 맞게 동적으로 결정하는 지능적 에너지 관리 설계다.

- **📢 섹션 요약 비유**: 조용히 있어야 할 때는 조용한 시계다. 학생이 없는 교실에서 종을 울리지 않아 에너지를 아끼지만, 필요할 때는 정확히 울린다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Tick / Jiffies | 틱리스가 억제하는 대상 |
| ACPI C-State | 틱리스와 연계하여 깊은 절전 달성 |
| cpuidle | 틱리스와 C-state 선택을 연결하는 프레임워크 |
| CONFIG_NO_HZ_IDLE | 유휴 CPU 틱 억제 (기본 설정) |
| CONFIG_NO_HZ_FULL | 단일 실행 CPU까지 틱 억제 (HPC용) |
| PREEMPT_RT | 틱리스와 반대 방향: 응답성 우선 |
| HRT (hrtimer) | 틱리스 환경에서 정밀 타이머 제공 |
| RCU | NO_HZ_FULL에서 RCU quiescent state 처리 필요 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">전통 주기 틱 (CONFIG_HZ_PERIODIC)</div>
<div class="kb-diagram-note">→ 유휴 중에도 초당 250번 인터럽트</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">전력 낭비 문제 → Tickless 연구</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">CONFIG_NO_HZ_IDLE (Linux 2.6.21, 2007)</div>
<div class="kb-diagram-note">→ 유휴 CPU에서 틱 억제</div>
<div class="kb-diagram-note">→ 모바일/노트북 배터리 향상</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">CONFIG_NO_HZ_FULL (Linux 3.10, 2013)</div>
<div class="kb-diagram-note">→ 단일 실행 CPU도 틱 억제</div>
<div class="kb-diagram-note">→ HPC, 게임 서버 성능 향상</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Full Dynamic Tick 개선 (RCU, 타이머 통합)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">ARM64, RISC-V 지원 확대</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">IoT/엣지 컴퓨팅 초저전력 설계 표준화</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 아무도 없는 교실에서 종을 계속 울리면 전기 낭비겠죠? 틱리스 커널은 아무것도 없을 때 종을 멈춰요.
2. 필요한 시간이 되면 정확히 종을 울려서 CPU를 깨워요.
3. 덕분에 스마트폰 배터리가 더 오래 가요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 74 / 800

← **이전**: [73. 틱 (Tick) / 지피스 (Jiffies)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/073_tick_jiffies/)
**다음**: [75. ACPI (Advanced Configuration and Power Interface)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/075_acpi/) →

---
