+++
title = "795. 틱리스 커널(Tickless) 모바일 배터리 보존"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 틱리스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)([Tickless Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/074_tickless_kernel/))은 CPU [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 일정한 시간(예: 1ms)마다 무조건 강제로 깨어나던 고정된 타이머 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)(Periodic [Tick](/knowledge-base/studynote/02_operating_system/01_overview_architecture/073_tick_jiffies/)) 방식을 버리고, **"할 일이 없을 때는 다음 예약된 스케줄이 올 때까지 알람을 끄고 무한정 깊은 수면(Deep Sleep)에 빠지는" 동적 이벤트 기반(Event-Driven) 타이머 아키텍처**다.
> 2. **가치**: 아무 일도 안 하면서 1초에 1,000번씩 허공에 도끼질을 하던 CPU의 무의미한 각성(Wake-up) 오버헤드를 0으로 만들어, 스마트폰이 주머니 속에 있을 때(대기 모드) 배터리가 증발하는 현상을 막고 기기의 **대기 전력 수명을 며칠 단위로 획기적으로 연장**시켰다.
> 3. **융합**: 모바일(Android/iOS)의 배터리 보존을 위해 탄생한 이 `CONFIG_NO_HZ_IDLE` 기술은, 이제 [HPC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/548_automotive_hpc/)(고성능 컴퓨팅)와 금융 서버 환경에서 단 1코어만 돌릴 때 타이머 간섭 자체를 없애는 `CONFIG_NO_HZ_FULL` 극저지연 튜닝 기술로 융합 발전하여 데스크톱/서버의 생태계까지 정복했다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - 과거 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 HZ(Hertz)라는 값에 따라 1초에 100번~1000번씩 규칙적으로 시계 알람([Timer](/knowledge-base/studynote/02_operating_system/01_overview_architecture/071_os_timer/) [Tick](/knowledge-base/studynote/02_operating_system/01_overview_architecture/073_tick_jiffies/))을 울렸다.
  - 틱리스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)(동적 틱, Dynamic [Tick](/knowledge-base/studynote/02_operating_system/01_overview_architecture/073_tick_jiffies/))은 CPU가 쉬는 상태([Idle](/knowledge-base/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/))에 들어갈 때, 이 규칙적인 알람을 아예 꺼버리고 "다음 네트워크 패킷이 올 때"나 "3초 뒤 타이머 콜백이 예약된 시점"으로 하드웨어 타이머를 재프로그래밍(Reprogramming) 한 뒤 잠을 잔다.

- **필요성(문제의식)**: 
  - 리눅스 서버 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 스마트폰 초창기에 그대로 올렸더니, 사용자가 화면을 끄고 자는 동안에도 배터리가 1시간에 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%씩 살살 녹아내렸다.
  - "도대체 왜 녹지?" 분석해 보니, CPU는 쉴 때 전기를 안 먹는 C-State(Sleep 상태)로 들어가야 하는데, 고정된 타이머([Tick](/knowledge-base/studynote/02_operating_system/01_overview_architecture/073_tick_jiffies/))가 1ms마다 CPU의 뺨을 때려서 "별일 없어?"라고 깨우고 다시 재우기를 반복하고 있었다.
  - 잠드는 데 2ms가 걸리는데 1ms마다 깨우니, CPU는 영원히 깊은 잠에 들지 못하고 얕은 잠만 자며 전기를 퍼먹었다.
  - **해결책**: "할 일이 10초 뒤에 있다면, 10초 동안 알람 자체를 꺼버리자!"

  - **고정 틱 (Periodic [Tick](/knowledge-base/studynote/02_operating_system/01_overview_architecture/073_tick_jiffies/))**: 비행기 조종사가 승객들이 잘 자는지 확인하려고, 아무 일도 없는데 무조건 1분마다 방송을 켜서 "승객 여러분, 이상 없으십니까?"라고 묻는 미친 짓. 승객(CPU)은 밤새 잠을 못 자 피곤해 죽는다(배터리 고갈).
  - **틱리스 (Tickless)**: 조종사가 "내일 아침 7시 도착 예정이니 그때까지 방송 끕니다. 응급 환자가 생기면([인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)) 승무원 호출 벨을 누르세요"라고 선언. 승객(CPU)은 아침까지 한 번도 안 깨고 푹 잔다(전력 보존).

- **등장 배경**: 
  - 2008년 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 2.6.21에 `NO_HZ`라는 이름으로 처음 도입되었다. 스마트폰(Android)의 등장과 함께 배터리 수명이 기기의 상업적 성패를 가르는 1순위 지표가 되면서, 모바일 아키텍처의 가장 절대적이고 기본적인 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 튜닝으로 자리 잡았다.

```text
  ┌─────────────────────────────────────────────────────────────┐
  │                 전통적 Tick vs Tickless(동적 틱)의 수면 상태 비교      │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  [ HZ = 1000 (1ms) 인 구형 커널 ]                           │
  │  CPU: 💤 (Sleep 진입)                                       │
  │  1ms: ⚡ Tick! ─▶ 커널: "일 있냐?" ─▶ 없음 ─▶ 다시 💤           │
  │  2ms: ⚡ Tick! ─▶ 커널: "일 있냐?" ─▶ 없음 ─▶ 다시 💤           │
  │  3ms: ⚡ Tick! ─▶ 커널: "일 있냐?" ─▶ 없음 ─▶ 다시 💤           │
  │  ▶ 결과: 깊은 잠(Deep C-State)에 들어갈 시간이 없어서 전력 누수 폭발. │
  │                                                             │
  │  [ Tickless (NO_HZ_IDLE) 현대 안드로이드 커널 ]               │
  │  CPU: "나 할 일 다 끝났어."                                    │
  │  커널: "다음 예약된 크론(Cron) 작업이 5초 뒤네?                  │
  │        하드웨어 타이머야, 알람 1ms 말고 5초(5000ms) 뒤로 맞춰 놔!" │
  │  CPU: 💤💤💤💤💤 (Deep Sleep 진입 - 화면 꺼짐)                │
  │  1ms ~ 4999ms : (아무 일도 일어나지 않음. 전력 소모 0.1mW)      │
  │  5000ms: ⏰ 예약된 알람! ─▶ CPU 기상 ─▶ 5초 전 예약된 작업 실행.   │
  └─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 단순해 보이는 구조 변경이 모바일 혁명을 가능케 했다. CPU는 단순히 '자고/깨고' 두 상태만 있는 게 아니라, 깊이에 따라 C0(실행), C1(얕은 잠), C3(깊은 잠), C6(가사 상태) 등의 [C-States](/knowledge-base/studynote/02_operating_system/01_overview_architecture/077_c_states/) 등급을 가진다. 깊은 잠(C6)에 들어갈수록 전기는 아끼지만 깨어나는 데 수 밀리초가 걸린다. 1ms마다 틱이 울리면 CPU는 구조적으로 절대 C3 이하의 깊은 잠으로 내려가지 못한다. 틱리스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 이 1ms 족쇄를 끊어버려, CPU가 화면이 꺼진 주머니 속에서 C6 가사 상태로 돌입할 수 있게 허락해 주는 절대적 전제 조건이다.

- **📢 섹션 요약 비유**: 요리사가 주문이 없을 때, "언제 주문이 올지 몰라"라며 가스레인지 불을 10분 내내 약하게 켜두는 게 고정 틱이라면, 틱리스는 아예 밸브를 잠가버리고 의자에 누워 자다가 배달 앱(타이머/[인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/))이 "딩동!" 울릴 때만 불을 켜는 확실한 가스비(배터리) 절약법입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 하드웨어 타이머의 진화 (PIT에서 APIC / HPET로)

틱리스를 구현하려면 하드웨어의 뒷받침이 필수적이었다.

1. **PIT (구형 발진기)**: "1ms마다 무조건 전기 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 발사!"라는 기능밖에 없었다. 소프트웨어가 틱리스를 하고 싶어도 끄거나 조절할 수가 없었다.
2. **Local APIC [Timer](/knowledge-base/studynote/02_operating_system/01_overview_architecture/071_os_timer/) / HPET (현대 타이머)**: OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 타이머 레지스터에 접근하여, "지금부터 452 밀리초 뒤에 딱 한 번만([One-shot](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/272_in_context_learning_icl/) mode) [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 쏴 줘"라고 아주 정밀하게 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)(Reprogramming)할 수 있는 고해상도 하드웨어 칩이 도입되었다. 틱리스는 이 [One-shot](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/272_in_context_learning_icl/) 모드를 이용한 것이다.

### jiffies (시간 기록) 복원의 마술

틱리스의 맹점은 "시계가 멈춘다"는 데 있다. 리눅스는 틱([Tick](/knowledge-base/studynote/02_operating_system/01_overview_architecture/073_tick_jiffies/))이 울릴 때마다 `jiffies`라는 전역 변수를 +1 올려서 시스템의 현재 시간을 계산한다. 그런데 5초 동안 틱을 꺼버리면, 시스템은 5초 전 과거의 시간에 갇히게 된다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 Tickless 모드에서의 시간 누락(Drift) 보정 알고리즘       │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [ T=0초 ] CPU가 Idle 진입. 틱 정지. (현재 jiffies = 100)           │
  │                                                                   │
  │   [ T=5초 ] ⚡ 외부 인터럽트(카톡 알림)로 인해 CPU 강제 기상!              │
  │                                                                   │
  │   [ 커널 기상 핸들러 작동 (`tick_nohz_idle_exit`) ]                 │
  │   1. 커널: "헐 나 5초나 잤어? jiffies 갱신 안 했는데!"                 │
  │   2. 커널은 메인보드의 영구 하드웨어 클럭(RTC 또는 TSC)을 즉시 읽어옴.     │
  │   3. 커널: "하드웨어 시계를 보니 5000 밀리초가 지났네."                 │
  │   4. `jiffies = jiffies + 5000;` ◀ 단숨에 5000번 분량의 시간을 보상! │
  │                                                                   │
  │   [ T=5.001초 ] 앱 실행 재개. 앱은 시스템 시계가 정상적으로 5초 흐른 걸로 착각.│
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** OS는 시계가 멈추는 것을 결코 허용하지 않는다. 잠에서 깬 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 가장 먼저 하는 일은, 자신이 얼마 동안 기절해 있었는지 '절대 시계(하드웨어 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/))'를 쳐다보고 계산하는 것이다. 이 과정(Time-keeping compensation) 덕분에, 스마트폰은 배터리를 아끼느라 수시로 심장([Tick](/knowledge-base/studynote/02_operating_system/01_overview_architecture/073_tick_jiffies/))을 멈추지만 사용자 눈에는 카카오톡 시계가 1초의 오차도 없이 완벽히 맞는 기적 같은 동기화를 유지한다.

- **📢 섹션 요약 비유**: 잠자리에 들기 전 초침 시계 소리(틱)가 시끄러워서 아예 건전지를 빼버리고 잤습니다(틱리스). 아침에 일어나자마자 스마트폰(절대 시계)을 켜서 지금이 7시인 걸 확인하고, 초침 시계 바늘을 7시로 확 돌려맞추는(jiffies 보상) 것과 같습니다. 자는 동안 째깍 소리에 안 시달리면서도 다음 날 시간을 정확히 맞출 수 있습니다.

---

## Ⅲ. 비교 및 연결

### 틱리스(Tickless) 옵션의 3대 진화 (CONFIG_NO_HZ 트리)

서버 아키텍트는 목적에 따라 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 컴파일할 때 이 3가지 중 하나의 사상을 택해야 한다.

| [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 컴파일 옵션 | 동작 방식 | 주요 사용처 | 장단점 |
|:---|:---|:---|:---|
| **NO_HZ_NONE** (고정 틱) | 클래식. 무슨 일이 있어도 HZ 주기로 틱 발생. | 낡은 레거시 시스템 | 배터리 다 버림. 대신 타이머 구현이 가장 심플함. |
| **NO_HZ_IDLE** (동적 틱) | CPU가 **유휴([Idle](/knowledge-base/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/)) 상태일 때만** 틱을 끔. 일할 때는 정상 틱 발생. | **모든 안드로이드/일반 리눅스** | 일반적인 배터리 방어의 표준. (대부분의 시스템 기본값) |
| **NO_HZ_FULL** (완전 틱리스)| CPU가 **일하고 있을 때(단 1개의 스레드만 돌 때)**조차 틱을 아예 꺼버림. | [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 금융 트레이딩(HFT), 슈퍼컴퓨터 | [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 방해가 0%가 되어 초저지연 달성. 단, [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 난이도가 극악. |

### 과목 융합 관점

- **[가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 및 클라우드 ([VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) Exit 오버헤드 방어)**: 1대의 호스트 머신에 100대의 가상머신([VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))을 띄웠다고 가정하자. 100대의 VM이 `NO_HZ_NONE` (고정 틱)을 쓴다면, 아무 일도 안 하는 밤에도 100대의 VM이 1ms마다 번갈아 가며 "나 틱 울렸어!"라며 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)를 깨운다([VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) Exit 발생). 호스트 서버는 틱을 처리하느라 CPU 100%를 찍고 폭발한다. 클라우드에서 게스트 OS의 틱리스(Tickless) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 적용은, 클라우드 제공자(AWS)의 서버 터짐을 막아주는 핵심 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 튜닝 요소다.
- **[실시간 시스템](/knowledge-base/studynote/02_operating_system/01_overview_architecture/009_real_time_system/) ([PREEMPT_RT](/knowledge-base/studynote/02_operating_system/10_security/654_preempt_rt_linux_spinlock_mutex/) 와의 충돌)**: 하드 리얼타임 OS는 철저하게 타이머 틱 단위로 스케줄링([라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/))을 잘라야 한다. 틱리스를 켜버리면 스레드가 영원히 CPU를 독점할 위험이 생긴다. 따라서 극단적인 제어가 필요한 드론/의료 장비에서는 배터리가 닳더라도 오히려 틱리스를 끄고 1ms 단위의 숨 막히는 고정 틱 환경으로 세팅하여 데드라인([Deadline](/knowledge-base/studynote/02_operating_system/11_exam_summary/766_realtime_scheduling_deadline/))을 확보한다.

- **📢 섹션 요약 비유**: 틱리스-아이들이 "쉬는 시간([Idle](/knowledge-base/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/))에만 종을 안 치는 학교"라면, 완전 틱리스(Full)는 "전교 1등 학생(단일 워크로드) 한 명만 교실에 있으면 공부에 방해된다고 아예 수업 시간 종([Tick](/knowledge-base/studynote/02_operating_system/01_overview_architecture/073_tick_jiffies/))조차 영원히 안 쳐주는 초특급 대우 학교"입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오 및 최적화 함정

1. **시나리오 — 고빈도 트레이딩(HFT) 서버의 1ms 주기 Jitter(튀는 현상) 제거**: 주식 매매 서버를 짰는데 이상하게 코드가 1ms마다 한 번씩 10마이크로초 정도 느려지는 렉(Jitter)이 낀다.
   - **원인 분석**: 서버에 `NO_HZ_IDLE` (기본값)이 켜져 있었다. 이 모드는 쉴 때만 틱을 끄고, 트레이딩 앱이 미친 듯이 100%로 연산할 때는 옛날처럼 1ms마다 타이머 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)([Tick](/knowledge-base/studynote/02_operating_system/01_overview_architecture/073_tick_jiffies/))를 때린다. 앱이 계산을 잘하다가 1ms마다 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에게 "시간 계산 좀 할게"라며 CPU를 뺏기니까 10µs의 치명적 렉이 걸린 것이다.
   - **아키텍트 판단 (NO_HZ_FULL + isolcpus 조합)**: 아키텍트는 부팅 파라미터에 `nohz_full=2-15` 와 `isolcpus=2-15`를 넣는다. 이 뜻은 "2번부터 15번 코어는 완벽한 무균실로 만들고, 여기에 단 1개의 스레드만 꽂혔을 때는 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 틱([Tick](/knowledge-base/studynote/02_operating_system/01_overview_architecture/073_tick_jiffies/))을 영원히 죽여라!"라는 뜻이다. OS는 이 코어에 대해 1초에 단 1Hz의 틱(최소한의 생존 틱)만 남기고 완벽히 침묵한다. 트레이딩 앱은 단 한 번의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 간섭 없이 100% CPU 파이프라인을 독점하는 신의 경지에 오른다.

2. **시나리오 — 안드로이드 앱의 무분별한 WakeLock(웨이크락) 남용으로 인한 배터리 광탈**: 내가 만든 안드로이드 앱을 켜기만 하면 사용자 폰이 밤새 뜨거워지고 배터리가 0%가 되어 앱 리뷰가 테러당했다.
   - **원인 분석**: 백그라운드 서비스에서 GPS 위치를 수집하겠다고, 안드로이드 API인 `WakeLock.acquire()`를 걸어두고 해제(`release()`)하지 않았다. 웨이크락은 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)에게 "나 지금 일해야 하니까 CPU 제발 재우지 마!"라고 멱살을 잡는 권한이다. 틱리스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 기기 화면이 꺼진 걸 보고 깊은 잠(C-state)으로 들어가 알람을 끄려고 했는데, 이 멍청한 앱 하나가 멱살을 쥐고 있어서 CPU가 밤새 켜진 채로 전기를 태운 것이다.
   - **아키텍트 판단 (Doze 모드와 JobScheduler 수용)**: 모바일 앱 개발자는 절대 `WakeLock`을 직접 다루면 안 된다. 구글이 강제하는 **JobScheduler** 나 **WorkManager** API를 써야 한다. 이 도구들은 앱이 산발적으로 깨워달라는 요청을 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 거부하고 모아두었다가, 폰이 가끔 메일을 받기 위해 깨어날 때(Maintenance Window) "야, 기왕 일어난 김에 니들 것도 한 번에 다 처리해!"라고 일괄 처리([Batching](/knowledge-base/studynote/05_database/06_dw_olap_trends/389_bulk_insert_batching_optimization/))를 강제하여 틱리스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 깊은 잠을 보장해 주는 아키텍처다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 모바일 및 서버 아키텍트의 타이머(Timer) 최적화 트리           │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [ 시스템에 "일정 주기로 반복되는 로직(Timer)"을 설계해야 한다 ]              │
  │                │                                                  │
  │                ▼                                                  │
  │      그 주기가 반드시 0.1초 단위의 정확한 간격(Strict)으로 실행되어야 하는가?  │
  │          ├─ 예 ─────▶ 🚨 [ 배터리 소모 각오. High-res Timer 사용 ]     │
  │          │             (커널의 틱리스를 강제로 깨워 막대한 전력 소모 유발)      │
  │          │                                                        │
  │          └─ 아니오 (대충 10분, 30분 근처에 실행돼도 서비스에 지장 없음)         │
  │                │                                                  │
  │                ▼                                                  │
  │      [ 타이머 연기 및 병합(Timer Coalescing / Slack) 튜닝 적용 ]           │
  │      - Linux: `prctl(PR_SET_TIMERSLACK)` 로 타이머 오차 범위(Slack)를 넓힘 │
  │      - Android: `AlarmManager.setInexactRepeating()` 사용         │
  │                                                                   │
  │      ▶ 결과: OS가 여러 앱의 자잘한 타이머를 5분에 한 번으로 뭉쳐서(Batch)      │
  │              한꺼번에 처리함. CPU가 깨어나는 횟수를 1/10로 줄여 배터리 수호!   │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** "정확함(Exactness)은 배터리의 적이다." 이것이 틱리스 생태계의 제1원칙이다. 카톡 알림이 정확히 오후 1시 0분 0초에 와야 하는가? 1시 0분 2초에 와도 아무도 죽지 않는다. 하지만 이 2초의 여유(Slack)를 허락해주면, OS는 화면 뒤에서 이메일 갱신, 날씨 갱신, 카톡 알림을 한꺼번에 묶어서 오후 1시 0분 2초에 CPU를 단 한 번만 깨워(Wake-up) 처리하고 다시 재운다. 인프라 설계자는 자신의 로직이 OS의 깊은 잠(Tickless)을 방해하지 않는 둥글둥글한 로직인지 끊임없이 반문해야 한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **0.1초짜리 [폴링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)([Polling](/knowledge-base/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/)) 루프로 백그라운드 대기하기**: "새 데이터가 왔나?" 확인하려고 `while(1) { sleep(0.1); check_data(); }` 코드를 짜는 짓. `sleep` 함수는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 내부에서 타이머 이벤트를 세팅한다. 0.1초마다 타이머가 울린다는 것은, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 애써 틱을 끄고(Tickless) 수면에 돌입하려 할 때마다 당신의 앱이 0.1초 간격으로 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 뺨을 갈겨서 계속 깨우는 패륜적 행위다. [폴링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)을 버리고 반드시 이벤트 기반의 블로킹 함수(`epoll_wait`, `select`)를 써서, 진짜 데이터가 왔을 때만 하드웨어 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)로 깨워달라고 OS에게 고이 목숨을 맡겨야 한다.

- **📢 섹션 요약 비유**: 아이(앱)가 잠든 엄마(틱리스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))에게 "엄마, 내일 아침에 깨워줘" 하고 자는 건 착한 일(이벤트 대기)이지만, "엄마, 아침인지 10분마다 물어볼게" 하면서 밤새 엄마를 툭툭 치는 건 집안(시스템)을 파탄 내는 최악의 불효([안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/))입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 고정 틱 (Periodic [Tick](/knowledge-base/studynote/02_operating_system/01_overview_architecture/073_tick_jiffies/)) 환경 | 틱리스 (NO_HZ) 환경 적용 | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (Wake-up 횟수)** | 화면 꺼진 상태에서도 초당 1,000회 기상 | 화면 꺼지면 시간당 수십 회로 극감 | CPU [Idle](/knowledge-base/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/) 진입 비율 극대화 |
| **정량 ([전력 소모](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/466_power_consumption/) / 배터리)**| 대기 [전력 소모](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/466_power_consumption/) 극심 (스마트폰 하루 못 감) | C-State 최고 깊이(C6) 도달 가능 | **모바일 기기 대기 시간 수십~수백 배 상승** |
| **정성 (클라우드 효율)** | 100개 VM이 호스트 CPU를 틱으로 찢어놓음 | VM들이 쉴 땐 호스트도 간섭 0으로 완벽히 쉼| [퍼블릭 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/) [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)의 멀티테넌시(오버커밋) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 안정화 |

### 미래 전망
- **NOHZ_FULL의 상용화 (Zero-Jitter)**: 현재는 극한의 튜닝을 아는 소수의 HFT(금융)나 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 텔레콤 업체만 쓰지만, 클라우드의 게임 스트리밍(Cloud Gaming)과 자율주행 관제 서버가 발전함에 따라 "아무 방해도 받지 않는 100% 격리 코어"의 수요가 늘고 있다. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 1초에 한 번 울리던 그 최소한의 틱마저 완전히 박멸하여, 스레드가 영원히 방해받지 않는 완벽한 0-[Tick](/knowledge-base/studynote/02_operating_system/01_overview_architecture/073_tick_jiffies/) 아키텍처로 진화 중이다.
- **이기종 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 칩셋과의 연동 ([SoC](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/131_soc/) 레벨 틱리스)**: 이제 CPU만 자는 게 능사가 아니다. 스마트폰의 [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 안에는 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/), [NPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/), 통신 모뎀이 섞여 있다. CPU가 깊은 잠(Tickless)에 빠졌을 때, 화면은 꺼져있어도 칩셋 구석의 초저전력 오디오 DSP(음성 인식기) 혼자 깨어있다가 "헤이 구글" 소리를 듣는 순간에만 하드웨어 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)로 전체 칩셋을 깨우는 시스템 온 칩([SoC](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/131_soc/)) 단위의 광역 틱리스 기술이 현재 온디바이스 AI의 뼈대를 이루고 있다.

### 참고 표준
- **[ACPI](/knowledge-base/studynote/02_operating_system/01_overview_architecture/075_acpi/) (Advanced Configuration and [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Interface)**: [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)와 하드웨어 간의 전원 관리(C-State, P-State)를 정의하는 글로벌 표준. 틱리스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 성립하기 위한 하드웨어적 토대.
- **Linux High-Resolution Timers (hrtimers)**: 구형의 둔탁한 1ms 틱을 버리고 나노초(ns) 단위로 타이머를 예약/해제할 수 있게 해 준 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 혁명적 서브시스템(Thomas Gleixner 주도).

틱리스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)([Tickless Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/074_tickless_kernel/))은 컴퓨터가 항상 바쁘게 돌아가야만 쓸모 있다는 산업화 시대의 강박관념(HZ)을 과감히 부숴버린 철학적 전환이다. "아무것도 하지 않는 시간"을 가장 가치 있는 시간(배터리 보존)으로 만들기 위해, [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 스스로의 심장 박동([Tick](/knowledge-base/studynote/02_operating_system/01_overview_architecture/073_tick_jiffies/))마저 멈추는 기괴하고도 눈물겨운 진화를 택했다. 오늘날 여러분의 스마트폰이 주머니 속에서 일주일간 배터리를 유지하다가 전화가 오는 그 1초의 찰나에만 번개처럼 살아날 수 있는 것은, 바로 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 매 순간 "죽은 듯이 자는 법"을 완벽하게 터득했기 때문이다.

- **📢 섹션 요약 비유**: 수영 선수(CPU)가 기록을 단축하려면 숨([Tick](/knowledge-base/studynote/02_operating_system/01_overview_architecture/073_tick_jiffies/))을 자주 쉬는 게 아니라, 물속(대기 상태)에서 숨을 최대한 오래 참고 멈춰야만 저항을 줄여 가장 빠르고 효율적으로 나아갈 수 있습니다. 틱리스는 OS가 수영 선수에게 가르쳐준 궁극의 무호흡 잠수 기법입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) 윈도우 사이즈 동적 조절 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 컬러링 캐시 경합 회피 물리 할당 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 로컬 메모리 원격 메모리 지연차 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [유니커널](/knowledge-base/studynote/02_operating_system/10_security/640_unikernel_mirageos_architecture/) 보안과 가벼운 부팅 특성 망 적용 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[페이지 컬러링 캐시 경합 회피 물리 할당]
    │
    ▼
[틱리스 커널(Tickless) 모바일 배터리 보존]
    │
    ├──▶ [NUMA 로컬 메모리 원격 메모리 지연차]
    └──▶ [유니커널 보안과 가벼운 부팅 특성 망 적용]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 옛날 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 엄마는 아기(CPU)가 잘 자는지 확인하려고, 10분마다 알람을 켜고 방문을 열어서 "아기야 잘 자니?" 하고 물어봤어요. 아기는 밤새 푹 자지 못해 피곤했죠(배터리 낭비).
2. 똑똑해진 틱리스(Tickless) 엄마는 이제 알람을 끄고 아기가 다음 날 아침(예약된 작업)까지 쭉 통잠을 자도록 내버려 둬요.
3. 대신 아기가 배가 고파서 으앙! 하고 우는 소리([인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/))가 들릴 때만 즉시 달려가서 밥을 준답니다. 그래서 우리 폰 배터리가 밤새 하나도 안 닳는 거예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 795 / 800

← **이전**: [794. 페이지 컬러링 캐시 경합 회피 물리 할당 (Page Coloring Cache Conflict Avoidance)](/knowledge-base/studynote/02_operating_system/11_exam_summary/794_page_coloring_cache_conflict_avoidance/)
**다음**: [796. NUMA 로컬 메모리 원격 메모리 지연차 (NUMA Local Remote Memory Latency)](/knowledge-base/studynote/02_operating_system/11_exam_summary/796_numa_local_remote_memory_latency/) →

---
