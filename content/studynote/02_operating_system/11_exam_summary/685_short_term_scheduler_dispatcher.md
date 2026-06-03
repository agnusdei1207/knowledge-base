+++
title = "685. 단기 스케줄러 디스패치 (Short Term Scheduler Dispatcher)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)([Short-term Scheduler](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/))는 메모리에 올라와 실행을 기다리는 프로세스([Ready Queue](/knowledge-base/studynote/02_operating_system/02_process_thread/088_ready_queue/)) 중 **"다음 10ms 동안 누가 CPU를 쓸 것인가?"를 1초에도 수백 번씩 결정하는 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 의사결정 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)**이다.
> 2. **[디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)([Dispatcher](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/))**: [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)가 "다음은 프로세스 B다!"라고 결정을 내리면, 실제로 현재 프로세스를 쫓아내고 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)를 교체([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/))하여 **프로세스 B에게 CPU 제어권을 실질적으로 넘겨주는 행동대장**이 바로 [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)다.
> 3. **가치**: [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)의 판단(Decision)과 [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)의 실행(Execution)이 결합하여 현대 [멀티태스킹](/knowledge-base/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/)이 완성되며, [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)가 문맥을 교환하는 데 걸리는 시간([Dispatch Latency](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/169_dispatch_latency/))은 [실시간 시스템](/knowledge-base/studynote/02_operating_system/01_overview_architecture/009_real_time_system/)의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 좌우하는 가장 치명적인 병목이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **[단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/) (CPU [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/))**: Ready 상태의 프로세스들 중 다음에 실행할 프로세스를 선택하는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 코드.
  - **[디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/) ([Dispatcher](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/))**: [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)가 선택한 프로세스에게 CPU의 실질적인 제어권을 양도([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/))하는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/).

- **필요성 ([결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/)(판사)와 집행자(경찰)의 분리)**: 
  - 병원에 환자 100명이 대기 중이다. "다음엔 누가 진료를 볼 것인가?"를 결정하는 것은 간호사([스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/))의 몫이다. (선착순인가, 응급환자 우선인가)
  - 하지만 간호사가 결정을 내렸다고 해서 진료가 시작되는 것은 아니다. 누군가는 이전 환자를 밖으로 내보내고, 새 환자를 진찰실로 부르고, 의사의 진료 차트를 새 환자의 것으로 바꿔 끼워야 한다. 이 육체노동을 담당하는 보안요원이 바로 [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)다.
  - **해결책**: "선택하는 로직"과 "하드웨어 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)를 갈아 끼우는 로직"을 분리하여, [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 어떤 스케줄링 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)([라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/), CFS 등)을 쓰든 [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)는 똑같이 동작할 수 있도록 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)화했다.

  - **[단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)**: 야구 감독. "다음 타석엔 3번 타자가 나간다!"라고 머리로 전략적 **결정**을 내림.
  - **[디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)**: 심판과 타격 코치. 이전 타자를 더그아웃으로 돌려보내고([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) Save), 3번 타자에게 헬멧과 배트를 쥐여주어 타석에 세운 뒤([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) Restore), "플레이 볼!(Jump to User Mode)"을 외치는 **실행자**.

- **발전 과정**:
  1. **[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) OS**: [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)와 [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)가 명확히 구분되지 않고 한 덩어리 코드였음.
  2. **[모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)화**: 스케줄링 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)([Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))과 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 메커니즘(Mechanism)이 분리됨. [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)는 철저하게 어셈블리 언어로 최적화됨.
  3. **실시간 OS (RTOS)**: [디스패치 지연](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/169_dispatch_latency/)([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))을 마이크로초 단위로 보장하는 것이 OS의 가장 중요한 스펙이 됨.

- **📢 섹션 요약 비유**: 판사([단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/))가 "다음은 2번 죄수다"라고 판결을 내리면, 교도관([디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/))이 1번 죄수를 감방에 집어넣고 2번 죄수를 법정으로 끌고 나오는 완벽한 분업 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)([Dispatcher](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/))가 하는 3가지 핵심 작업

[디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)는 [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)에 의해 호출된 직후, 다음 3가지 작업을 순식간에 해치운다.

1. **[문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) ([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/))**:
   - 쫓겨나는 프로세스(A)의 [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)(CPU [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/), [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 등)를 A의 PCB에 저장(Save)한다.
   - 선택된 프로세스(B)의 과거 상태를 B의 PCB에서 꺼내 CPU [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에 복원(Restore)한다.
   - [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/)(주소 변환 캐시)를 플러시(Flush)하거나 ASID를 교체하여 메모리 공간을 B의 것으로 바꾼다.
2. **모드 전환 (Mode [Switch](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/))**:
   - [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/) 자신은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드(Ring 0)에서 동작하고 있었다.
   - 이제 B 프로세스를 실행시켜야 하므로, CPU의 권한을 유저 모드(Ring 3)로 강등([Switch](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/))시킨다.
3. **사용자 프로그램 복귀 (Jump / iret)**:
   - 프로세스 B가 이전에 멈췄던 지점([프로그램 카운터](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/), [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/))의 주소로 CPU를 점프시킨다.

---

### [디스패치 지연](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/169_dispatch_latency/) ([Dispatch Latency](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/169_dispatch_latency/))의 딜레마

[디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)가 이 3가지 작업을 하는 동안 CPU는 "사용자 앱"을 1밀리초도 실행하지 못한다. 이를 **[디스패치 지연](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/169_dispatch_latency/)([Dispatch Latency](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/169_dispatch_latency/))**이라 한다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 단기 스케줄러와 디스패치 지연(Latency)의 타임라인        │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [ CPU 타임라인 ]                                                  │
  │                                                                   │
  │   --- 프로세스 P0 실행 중 ---                                         │
  │          │                                                        │
  │          ⚡ 인터럽트 발생 (예: 타임 슬라이스 종료)                         │
  │          │                                                        │
  │  ========▼====[ 디스패치 지연 (Dispatch Latency) 구간 ]=============│
  │  커 │ 1. 단기 스케줄러 실행: "다음은 누구지? P1이네." (알고리즘 연산)        │
  │  널 │ 2. 디스패처 동작: P0 레지스터 저장, P1 레지스터 복원                 │
  │  공 │ 3. 모드 전환: 커널 -> 유저                                      │
  │  간 │ 4. P1 코드로 점프                                              │
  │  ========▼========================================================│
  │          │                                                        │
  │   --- 프로세스 P1 실행 시작 ---                                       │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)는 1초에 수백 번~수천 번 호출된다. 만약 [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)가 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)을 하는 데 1ms가 걸리고, 프로세스에게 주어지는 타임 [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)가 10ms라면, CPU는 전체 시간의 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%를 앱이 아닌 "교대하는 데(오버헤드)" 날려버린다. 따라서 [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/) 코드는 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 내에서도 가장 최적화된 극강의 어셈블리어로 작성되며, [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)을 줄이는 것이 최고 지상 과제다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 장기 / 중기 / [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)의 차이

[스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 3형제 중 [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)의 위치를 명확히 해야 한다.

| 구분 | [장기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/163_long_term_scheduler/) (Job Scheduler) | [중기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/162_medium_term_scheduler_swapping/) (Swapper) | [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/) (CPU Scheduler) |
|:---|:---|:---|:---|
| **대상 큐** | 밖(디스크) $\rightarrow$ [Ready Queue](/knowledge-base/studynote/02_operating_system/02_process_thread/088_ready_queue/) | 메모리 $\leftrightarrow$ 디스크 (Swap) | **[Ready Queue](/knowledge-base/studynote/02_operating_system/02_process_thread/088_ready_queue/) $\rightarrow$ CPU** |
| **결정 내용** | 메모리에 몇 개의 프로세스를 올릴까? (N값 조절) | 메모리가 부족한데 누굴 쫓아낼까? | **지금 당장 누가 CPU를 쓸까?** |
| **실행 빈도** | 아주 가끔 (수 초 ~ 수 분) | 가끔 (메모리 부족 시) | **매우 자주 (1초에 수천 번, ms 단위)** |
| **속도 중요성**| 별로 안 중요함 | 보통 | **숨 막히게 빨라야 함 (오버헤드 직결)** |

현대 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(Windows, Linux, 모바일)는 가상 메모리가 발달하여 '[장기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/163_long_term_scheduler/)'의 개념이 거의 사라졌다. 우리가 흔히 "OS [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 어쩌고~"라고 말하는 것은 100% **[단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)**를 의미한다.

### 과목 융합 관점

- **컴퓨터구조 ([CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/))**: [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)의 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)이 아무리 빨라도, CPU의 **캐시(L1/L2/[TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/))가 차가워지는(Cold Cache) 현상**은 소프트웨어로 막을 수 없다. 따라서 [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)는 "가급적 P1을 예전에 P1이 돌았던 바로 그 CPU 코어에 다시 배정"하려는 성질(Cache [Affinity](/knowledge-base/studynote/02_operating_system/11_exam_summary/778_process_affinity_scheduling_pinning/))을 띠게 되며, 이를 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/)/[SMP](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/195_real_time_scheduling/) 스케줄링이라 한다.
- **[실시간 시스템](/knowledge-base/studynote/02_operating_system/01_overview_architecture/009_real_time_system/) (RTOS)**: 에어백 제어나 미사일 요격 시스템에서 [디스패치 지연](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/169_dispatch_latency/)은 "[지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)"이 아니라 "죽음"을 뜻한다. RTOS의 [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)는 일반적인 공평함(Fairness)을 철저히 무시하고, 우선순위가 높은 작업이 들어오면 기존 작업을 1 $\mu s$(마이크로초) 내에 찢어버리고 디스패치를 강제하는 극단적인 선점(Preemptive) 메커니즘을 갖는다.

- **📢 섹션 요약 비유**: [장기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/163_long_term_scheduler/)가 '대학 합격자(메모리 진입)'를 뽑는 입학처장이라면, [중기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/162_medium_term_scheduler_swapping/)는 성적이 떨어진 학생을 기숙사에서 쫓아내는(Swap-out) 사감이고, [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)는 매일 수업 시간에 누구에게 발표(CPU)를 시킬지 초 단위로 지목하는 열혈 선생님입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — 고빈도 트레이딩(HFT) 서버에서의 디스패치 지터(Jitter) 방어**: 증권사 서버에서 특정 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 패킷을 받았을 때 10마이크로초 안에 반응해야 하는데, 가끔 500마이크로초씩 반응이 늦어짐.
   - **원인 분석**: [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)가 다른 백그라운드 프로세스에게 CPU를 주느라, 트레이딩 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 Ready Queue에서 대기하거나, 다른 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 내쫓고 디스패치되는([Dispatch Latency](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/169_dispatch_latency/)) 과정에서 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 발생한 것이다.
   - **대응 (아키텍처 적용)**: [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)의 개입을 원천 차단해야 한다. 리눅스 부팅 파라미터에 `isolcpus=2,3`을 주어 2번과 3번 코어를 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)의 통제에서 완전히 빼버린다. 그리고 트레이딩 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)만 2번 코어에 핀(Pinning)으로 꽂아둔다. 이제 2번 코어에서는 **[단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)와 [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)가 아예 작동하지 않으며([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 0회)**, 트레이딩 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 영원히 CPU를 100% 독점하여 지터가 소멸한다.

2. **시나리오 — 클라우드 환경의 Steal Time 폭주**: AWS EC2(가상머신)에 웹 서버를 올렸는데, 내 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 안에서 `top`을 쳐보면 CPU가 텅텅 비어있는데([Idle](/knowledge-base/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/)) 웹 서버 응답이 미친 듯이 느리다. 지표를 보니 `%st (Steal Time)`가 40%를 찍고 있다.
   - **원인 분석**: [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)는 두 번 동작한다. 내 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 안의 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 "웹 서버 실행해!"라고 디스패치했는데, 하필 그 찰나에 **호스트(AWS 물리 서버)의 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)**가 내 VM의 vCPU를 다른 고객의 VM에게 디스패치해 버린 것이다. 내 VM은 실행될 준비가 다 됐는데도 물리 CPU를 뺏겨서 멈춰있는 시간, 그것이 바로 Steal Time이다.
   - **기술사적 판단**: 이는 [멀티 테넌트](/knowledge-base/studynote/03_network/17_sdn_nfv/888_multi_tenant_cloud_resource_isolation_noisy_neighbor/) 환경에서 클라우드 사업자가 CPU를 과도하게 오버커밋(Over-provisioning)했을 때 발생한다. T3/T4g 같은 버스트 가능한 인스턴스의 크레딧이 고갈되었을 확률이 높으므로, M5/C5 같은 고정 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)(Dedicated) 인스턴스로 아키텍처를 변경해야 [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)가 뺏기는 현상을 막을 수 있다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 단기 스케줄링 특성에 따른 애플리케이션 아키텍처 튜닝        │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [CPU 코어에서 돌고 있는 수백 개의 스레드 관리 전략]                        │
  │                │                                                  │
  │                ▼                                                  │
  │      응답 속도보다 공평성과 배터리 절약이 중요한 데스크탑/모바일인가?             │
  │          ├─ 예 ─────▶ [리눅스 CFS (Completely Fair Scheduler) 유지]   │
  │          │            - 단기 스케줄러가 vruntime을 계산하여 공평하게 디스패치 │
  │          └─ 아니오 (특정 스레드의 절대적인 실시간 처리가 중요하다)            │
  │                │                                                  │
  │                ▼                                                  │
  │      결제가 지연되거나 패킷이 드롭되는 것을 0%로 막아야 하는가?                │
  │          ├─ 예 ─────▶ [스레드 스케줄링 정책을 FIFO나 RR로 변경]        │
  │          │            `chrt -f 99 <pid>` (실시간 스케줄링 정책 적용)    │
  │          │            - 단기 스케줄러는 이 스레드가 스스로 양보하기 전까지    │
  │          │              절대 다른 일반 프로세스를 디스패치하지 않음!          │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 개발자들은 보통 소스 코드 레벨의 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)만 신경 쓴다. 하지만 아무리 코드를 잘 짜도, [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)가 내 프로세스에 CPU를 안 꽂아주면(디스패치 안 해주면) 그 코드는 멈춰있는 돌덩이다. 고성능 백엔드 아키텍트는 OS [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)의 눈치를 보며, "내 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 예뻐해 달라"고 우선순위(Nice 값)를 깎거나 실시간 클래스로 격상시키는 OS 레벨의 튜닝을 반드시 병행해야 한다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **[Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 오버헤드 측정**: `vmstat 1` 명령어를 쳤을 때 `cs(Context Switch)` 수치가 초당 10만 번을 넘어가고 있지 않은가? [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)가 너무 예민하게 반응하여 일은 안 하고 교대만 하는 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) 상태라면, [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/) 크기를 확 줄이거나 타임 [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)(퀀텀) 크기를 늘려야 한다.

- **📢 섹션 요약 비유**: [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/) 튜닝은 교차로의 신호등([디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)) 주기 설정과 같습니다. 신호를 1초마다 바꾸면(잦은 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)) 차들이 멈추고 출발하느라([디스패치 지연](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/169_dispatch_latency/)) 매연만 내뿜고 한 대도 교차로를 못 지납니다. 적절한 10초 주기로 묶어주는 것이 도로 전체의 흐름을 뚫습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 스케줄링/디스패치 구조 미분리 ([초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)) | [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)와 [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/) 분리 (현대) | 개선 효과 |
|:---|:---|:---|:---|
| **정량 ([지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))** | 무거운 분기문으로 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 최적화된 어셈블리로 **수십 $\mu s$ 내외** | 실시간(Real-time) 반응성에 근접한 [멀티태스킹](/knowledge-base/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/) |
| **정성 (유연성)** | 스케줄링 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 수정 시 OS 전체 불안정 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)([Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))과 메커니즘(Mechanism) 분리 | 용도(서버, 폰, RTOS)에 맞춰 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)만 쉽게 교체 가능 |
| **정성 (자원 활용)** | I/O 대기 시 CPU 멈춤 | 즉각적인 디스패치로 다른 앱 실행 | 시스템 CPU 활용률(Utilization) 극대화 |

### 미래 전망
- **[eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 기반 플러그인 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) (sched_ext)**: 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 6.11부터 [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)를 개발자가 마음대로 바꿀 수 있는 기능이 공식 추가되었다. 예전에는 Linus Torvalds가 만든 CFS [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)를 무조건 써야 했지만, 이제는 Rust나 C로 "우리 회사 웹 서버에만 100% 최적화된" [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/) 로직을 짜서, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 재부팅 없이 실시간으로 [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)에 주입할 수 있는 미친 시대가 열렸다.
- **Microsecond 단위의 스케줄링 한계**: 네트워크 속도가 400Gbps를 돌파하면서, 패킷 하나가 들어오고 나가는 시간이 마이크로초 단위로 떨어졌다. OS의 [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)가 개입하여 디스패치하는 시간(수 $\mu s$)조차 너무 느린 병목이 되자, 아예 OS의 스케줄링을 받지 않는 유저 스페이스 [폴링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)([DPDK](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/671_dpdk/))이나 하드웨어 [오프로딩](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)(SmartNIC)으로 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 자체를 회피하려는 움직임이 가속되고 있다.

### 결론
[단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)와 [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)라는 오케스트라의 '지휘자'와 '무대 감독'이다. "누가 연주할지"를 끝없이 고민하는 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)의 철학적 판단과, 0.0001초의 낭비도 없이 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)를 갈아 끼우는 [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)의 육체적 기계성이 결합하여 우리는 수백 개의 프로그램이 동시에 살아 숨 쉬는 컴퓨터를 쓸 수 있게 되었다. 이 찰나의 교대 과정(Dispatch)을 이해하는 것은, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화의 한계선이 하드웨어의 클럭 스피드가 아니라 '[운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 결정 속도'에 있음을 깨닫는 과정이다.

- **📢 섹션 요약 비유**: 수백 명의 배우(프로세스)가 하나의 핀조명(CPU)을 번갈아 받아야 하는 연극에서, 누구에게 조명을 비출지 결정하는 감독([스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/))과 0.1초 만에 마이크와 옷(문맥)을 갈아입혀 무대로 밀어 넣는 스태프([디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/))의 피 튀기는 예술이 바로 [멀티태스킹](/knowledge-base/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/)입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| PCB 구성 요소 필수 암기 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 플러시 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| CPU 바운드 vs I/O 바운드 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 선점 / [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/) 스케줄링 차이 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[문맥 교환 TLB 플러시]
    │
    ▼
[단기 스케줄러 디스패치 (Short Term Scheduler Dispatcher)]
    │
    ├──▶ [CPU 바운드 vs I/O 바운드]
    └──▶ [선점 / 비선점 스케줄링 차이]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 게임기가 하나뿐인데 친구 10명이 모였어요. '[단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/)'는 "철수 끝났어? 다음은 영희가 해!"라고 누구 차례인지 재빨리 결정하는 심판이에요.
2. '[디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)'는 심판의 말을 듣고, 철수의 손에서 조이패드를 강제로 뺏어서 영희 손에 딱 쥐여주고 게임을 다시 켜주는 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 요원이죠.
3. 이 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 요원이 패드를 뺏고 넘겨주는 동작이 너무 느리면([디스패치 지연](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/169_dispatch_latency/)), 정작 게임할 시간이 다 날아가 버리기 때문에 엄청나게 날렵하게 움직여야 한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 685 / 800

← **이전**: [684. 문맥 교환 TLB 플러시 (Context Switch TLB Flush ASID)](/knowledge-base/studynote/02_operating_system/11_exam_summary/684_context_switch_tlb_flush_asid/)
**다음**: [686. CPU 바운드 vs I/O 바운드 (CPU Bound Vs I/O Bound Workload)](/knowledge-base/studynote/02_operating_system/11_exam_summary/686_cpu_bound_vs_io_bound_workload/) →

---
