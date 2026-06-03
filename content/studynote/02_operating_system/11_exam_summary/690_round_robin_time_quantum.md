+++
title = "690. 라운드 로빈 시간 할당량 (Quantum)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/)(Round Robin, [RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/))은 모든 프로세스에게 공평하게 동일한 시간 조각, 즉 **[시간 할당량](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/179_time_quantum_context_switch/)(Time Quantum 또는 Time [Slice](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/))**을 주고 번갈아 실행하게 만드는 [시분할 시스템](/knowledge-base/studynote/02_operating_system/01_overview_architecture/003_time_sharing_system/)(Time-sharing)의 가장 기본적인 [선점형 스케줄링](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/166_preemptive_scheduling/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.
> 2. **트레이드오프**: 타임 퀀텀을 무한히 크게 잡으면 먼저 온 놈이 다 쓰는 **[FCFS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/)(일괄 처리)**로 퇴화하고, 타임 퀀텀을 극단적으로 작게 잡으면 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)은 빛의 속도가 되지만 CPU가 1초에도 수만 번씩 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)를 바꾸느라 힘이 다 빠지는 **[문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 오버헤드([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) Overhead)**의 늪에 빠진다.
> 3. **튜닝의 예술**: 완벽한 타임 퀀텀은 "대부분의 I/O 바운드 프로세스가 한 번의 퀀텀 안에 CPU 계산을 끝내고 스스로 I/O 대기로 빠질 수 있을 만큼" 넉넉하되, "사용자가 랙(Lag)을 느끼기 전(보통 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100ms)"에 턴이 돌아오게 조율하는 것이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **Round Robin ([RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/))**: 도착한 순서대로 프로세스를 큐에 넣고, 각자에게 정해진 시간(Time Quantum)만 CPU를 허락한 뒤 시간이 지나면 강제로 뺏어 큐의 맨 뒤로 쫓아내는(선점) 방식.
  - **[시간 할당량](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/179_time_quantum_context_switch/) (Time Quantum, $q$)**: 프로세스 1개가 한 번에 CPU를 독점할 수 있는 최대 제한 시간 (주로 10ms ~ 100ms).

- **필요성 (FCFS의 절망 극복)**: 
  - [FCFS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/) 방식에서는 10시간짜리 배치 작업 뒤에 카카오톡(1ms짜리 작업)이 줄을 서면, 사용자는 카카오톡이 켜질 때까지 10시간을 멍하니 기다려야 했다.
  - 이 지독한 [호위 효과](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/174_convoy_effect/)([Convoy Effect](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/174_convoy_effect/))를 부수기 위해, "아무리 긴 작업이라도 절대 한 번에 다 끝내게 두지 말고, 조금씩 끊어서 먹여라!"라는 강제 분할 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 필요해졌다.
  - **해결책**: 타이머 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 통해 물리적으로 10ms마다 알람을 울리고, 알람이 울리면 무조건 하던 일을 멈추고 다음 사람에게 CPU를 넘겨주는 RR이 대화형 시스템(UI)을 구원했다.

  - **[FCFS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/)**: 뷔페에 1명씩만 입장 가능. 앞사람이 배 터질 때까지 다 먹고 나갈 때까지 뒷사람은 10시간 동안 밖에서 굶는다.
  - **Round Robin ([RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/))**: 모든 손님을 뷔페에 넣되, "한 사람당 접시에 고기를 1분($q$)만 담을 수 있다!"는 엄격한 룰을 적용. 1분이 지나면 조교가 무조건 호루라기를 불어 다음 사람에게 국자를 넘기게 한다. 덕분에 10명 모두가 10분 안에는 최소한 고기 한 점씩은 씹어볼 수 있다(빠른 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)).

- **발전 과정**:
  1. **[FCFS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/)/[SJF](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/175_sjf_scheduling/) ([초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/))**: [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형, 한 번 잡으면 끝까지 감. [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 최악.
  2. **Round Robin ([RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/))**: [시분할 시스템](/knowledge-base/studynote/02_operating_system/01_overview_architecture/003_time_sharing_system/)의 탄생. 고정된 타임 퀀텀으로 모든 프로세스에 공평한 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)을 보장.
  3. **VRR (Virtual Round Robin)**: I/O 바운드 프로세스가 퀀텀을 다 못 채우고 양보했을 때 손해를 보는 것을 막기 위해 남은 퀀텀을 보상해 주는 개선 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/).

- **📢 섹션 요약 비유**: 아무리 덩치 큰 트럭이라도 10분 이상은 달리지 못하게 강제로 휴게소로 쫓아내는 '고속도로 10분 운행 제한법'입니다. 트럭 기사는 괴롭겠지만, 뒤에 따라오던 수많은 승용차는 덕분에 꽉 막힌 길을 뻥 뚫고 시원하게 내달릴 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 타임 퀀텀($q$)에 따른 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)과 [반환 시간](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/172_turnaround_waiting_response_time/)의 변화

프로세스 3개($P_1=24ms$, $P_2=3ms$, $P_3=3ms$)가 동시에 도착했다고 가정하고 간트 차트를 그려보자.

**Case 1: $q = 4ms$ (최적의 [RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/))**
```text
  [ P1(4) ] [ P2(3) ] [ P3(3) ] [ P1(4) ] [ P1(4) ] [ P1(4) ] [ P1(4) ] [ P1(4) ]
  0         4         7         10        14        18        22        26        30
```
- P1은 너무 길어서 4ms마다 계속 쫓겨나 맨 뒤로 간다 (총 6번 나눠서 실행).
- P2와 P3는 3ms밖에 안 되므로, 자기 턴(4ms)이 오자마자 한 번에 다 쓰고 알아서 종료된다.
- **[응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)(처음 CPU를 잡는 시간)**: P1=0ms, P2=4ms, P3=7ms (모두 10ms 안에 즉각 반응을 체감!)
- **평균 [반환 시간](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/172_turnaround_waiting_response_time/)(완전히 끝난 시간)**: P1(30) + P2(7) + P3([10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)) / 3 = **15.6ms** ([FCFS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/) 최악의 17ms보다 훨씬 낫다)

**Case 2: $q = \infty$ (무한대)**
- 그냥 **[FCFS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/)**와 똑같이 동작한다.
- [호위 효과](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/174_convoy_effect/)가 발생하여 짧은 프로세스들이 피눈물을 흘린다.

**Case 3: $q = 1ms$ (극단적으로 작음)**
- 1ms마다 P1, P2, P3가 쉴 새 없이 바뀐다.
- [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)은 미친 듯이 빠르지만(P3조차 2ms면 반응함), 스케줄러가 개입하여 **[문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/))**을 하는 횟수가 무려 30번 가까이 터진다.
- 만약 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)에 1ms가 걸린다면? 1ms 일하고 1ms 교대하느라, 전체 CPU 성능의 50%가 허공에 증발([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/))한다.

---

### 경험 법칙 (Rule of Thumb): 80% Rule

[운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 아키텍트들은 "그러면 도대체 타임 퀀텀($q$)을 몇 ms로 설정해야 완벽한가?"를 두고 수십 년간 싸웠다.
결론적으로 도출된 공식은 **"전체 프로세스의 80%가 자신에게 주어진 타임 퀀텀(q)보다 짧은 CPU 버스트를 가지도록 설정하라"**는 것이다.

- 시스템에 돌아가는 앱의 80%는 I/O 바운드다. 이 녀석들은 CPU를 1~5ms 정도 아주 짧게 쓰고 잠든다.
- 따라서 $q$를 10ms 정도로 잡아두면, 80%의 앱들은 타임 퀀텀(10ms)을 다 쓰기도 전에 자발적으로 CPU를 내려놓으므로(강제 선점 안 당함), 억지로 쫓겨나면서 발생하는 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 오버헤드를 막을 수 있다.
- 반면 20%의 CPU 바운드(욕심쟁이)들은 10ms마다 꼬박꼬박 쫓겨나며(선점당하며) 시스템의 응답성을 해치지 않게 된다.

- **📢 섹션 요약 비유**: 타임 퀀텀은 시험 시간입니다. 너무 짧게 주면 학생들이 이름 쓰다 말고 시험지를 걷었다 나눠줬다 하느라 1시간을 다 버립니다([문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 오버헤드). 적당히 80%의 학생들이 풀 수 있는 시간을 줘야 모두가 평화롭습니다.

---

## Ⅲ. 비교 및 연결

### [라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/)([RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/))의 치명적 단점: 동일한 [반환 시간](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/172_turnaround_waiting_response_time/)의 함정

RR이 공평하고 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)이 좋은 건 맞지만, 모든 프로세스의 길이가 비슷할 때는 수학적으로 **최악의 [반환 시간](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/172_turnaround_waiting_response_time/)([Turnaround Time](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/172_turnaround_waiting_response_time/))**을 만들어낸다.

예를 들어 10ms짜리 프로세스 10개가 있고 $q=1ms$ 라고 치자.
- **[FCFS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/)**: 1번이 10ms에 끝나고, 2번이 20ms에 끝난다. 평균 [반환 시간](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/172_turnaround_waiting_response_time/)은 약 55ms.
- **[RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/)**: 1번부터 10번까지 1ms씩 번갈아 가며 한 입씩 베어 먹는다. 10개가 모두 99ms ~ 100ms 부근에서 우르르 끝난다! 평균 [반환 시간](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/172_turnaround_waiting_response_time/)은 약 **99.5ms**. 
- 이처럼 모든 작업의 크기가 같을 때 RR을 돌리면, 아무도 제때 안 끝나고 다 같이 고통받다가 다 같이 끝나는 극강의 비효율([지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/))이 발생한다.

### 과목 융합 관점

- **네트워크 (NW)**: L4 로드밸런서가 백엔드 웹 서버 3대에 트래픽을 분배할 때 쓰는 가장 기본 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)도 **Round Robin**이다. 트래픽을 1-2-3-1-2-3 순서로 던진다. 만약 1번 서버가 유독 성능이 좋은 서버라면, RR의 "무조건 똑같이 분배한다"는 철학 때문에 1번 서버는 놀고 2, 3번 서버는 터져나가는 비효율이 생긴다. 이를 보완한 것이 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 기반(Weighted [RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/))이다.
- **자료구조 ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Structure)**: RR의 원형 큐(Circular [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/)) 관리에서, 큐에서 빼낸 프로세스가 아직 안 끝났으면 다시 큐의 꼬리(Rear)에 집어넣고(Enqueue), 머리(Front)에서 새 프로세스를 뽑아(Dequeue) CPU에 밀어 넣는 $O(1)$의 완벽한 큐잉 로직이 쉴 새 없이 돌아간다.

- **📢 섹션 요약 비유**: 다 같이 배가 고픈데 햄버거를 1입씩만 먹고 옆 사람에게 넘기라([RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/))고 하면, 다들 10바퀴를 돌 때까지 아무도 배를 못 채웁니다. 차라리 한 명이 다 먹고 치우게([FCFS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/)) 하는 게 누군가에겐 훨씬 나을 수도 있습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — I/O 바운드 프로세스의 억울함 (VRR: Virtual Round Robin 도입)**: [RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/) 시스템에서 $q=100ms$ 다.
   - **원인 분석**: CPU 바운드(인코딩)는 자기 턴이 오면 100ms를 꽉 채워 다 쓴다. 그런데 불쌍한 I/O 바운드(카카오톡)는 자기 턴에 1ms만 쓰고 "네트워크 기다릴게" 하고 스스로 턴을 포기(Sleep)했다.
   - 네트워크 통신이 끝나고 다시 큐에 돌아온 카카오톡은? 맨 뒤에 서서 또 100ms씩 쓰는 CPU 바운드들을 하염없이 기다려야 한다. 공평하게 100ms를 줬는데 I/O 바운드만 억울하게 손해를 보는 구조다.
   - **대응 (기술사적 가이드)**: **가상 [라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/)(VRR)** 아키텍처를 도입한다. I/O를 하느라 자기 퀀텀을 다 못 쓰고 반납한 프로세스는, I/O가 끝난 뒤 일반 [Ready Queue](/knowledge-base/studynote/02_operating_system/02_process_thread/088_ready_queue/) 맨 뒤로 가는 게 아니라 **Auxiliary [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/)(VIP 대기열)**로 빠진다. OS는 VIP 대기열에 있는 애들한테 무조건 먼저 CPU를 줘서 "아까 못 쓴 99ms"를 마저 쓰게 보상(Compensation)해 준다. 이것이 멀티레벨 큐로 발전하는 시발점이다.

2. **시나리오 — [틱리스 커널](/knowledge-base/studynote/02_operating_system/11_exam_summary/795_tickless_kernel_mobile_battery_preservation/)([Tickless Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/074_tickless_kernel/))로 오버헤드 박살 내기**: 64코어 빅데이터 서버에서 1번 코어에 아주 무거운 [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 프로세스 딱 1개만 실행시켜 놨다.
   - **원인 분석**: 리눅스는 기본적으로 $q$를 맞추기 위해 타이머 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)([Tick](/knowledge-base/studynote/02_operating_system/01_overview_architecture/073_tick_jiffies/))를 1초에 250번(`HZ=250`) 터뜨린다. 코어에 프로세스가 1개밖에 없는데도, OS는 "야 시간 다 됐어! 다른 놈 줄게! 어? 줄 놈이 없네? 너 계속해"라는 바보 같은 [RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/) 짓을 초당 250번씩 반복하며 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 페널티와 캐시 낭비를 일으킨다.
   - **아키텍처 적용**: [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 파라미터에 `CONFIG_NO_HZ_FULL` ([Tickless](/knowledge-base/studynote/02_operating_system/11_exam_summary/795_tickless_kernel_mobile_battery_preservation/))를 적용한다. OS는 "어차피 이 코어의 Ready Queue에 대기자가 얘 1명뿐이네?"라고 판단하면 아예 하드웨어 타이머 틱을 꺼버린다([Tick](/knowledge-base/studynote/02_operating_system/01_overview_architecture/073_tick_jiffies/)-less). RR의 퀀텀 제한이 아예 해제되어 프로세스가 100% 코어를 독점 연산하게 되어 극한의 성능을 뽑아낸다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 타임 퀀텀(q) 및 스케줄링 HZ 파라미터 튜닝 플로우           │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [리눅스 커널 빌드 시 HZ(초당 타이머 인터럽트 횟수) 값 설정]                 │
  │                │                                                  │
  │                ▼                                                  │
  │      서버가 초저지연(Low Latency)을 요구하는 데스크탑이나 게임 서버인가?        │
  │          ├─ 예 ─────▶ [HZ=1000 설정 (q = 1ms)]                     │
  │          │            (응답 시간을 극한으로 당김. 대신 CPU 낭비(배터리 광탈) 감수)│
  │          └─ 아니오 (웹 서버, DB 서버, 일반적인 백엔드 인프라)               │
  │                │                                                  │
  │                ▼                                                  │
  │      서버가 파일 I/O 나 대규모 연산을 묵직하게 처리해야 하는가?               │
  │          ├─ 예 ─────▶ [HZ=100 (q = 10ms) 또는 HZ=250 설정 (디폴트)] │
  │          │            (Context Switch 오버헤드를 10배 줄이고, 캐시 핫(Hot) 유지)│
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 클라우드 인프라 엔지니어가 `sysctl`이나 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 파라미터에서 가장 많이 건드리는 것이 이 퀀텀(Quantum)과 관계된 값이다. RR이 모든 스케줄링의 뼈대이긴 하나, 퀀텀이 너무 짧으면 서버가 일은 안 하고 스위칭만 하는 좀비가 되고, 너무 길면 사용자들의 "서버가 랙 걸려요"라는 불만이 폭주하는 지옥의 시소가 된다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **Time Quantum과 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 비용의 비율 계산**: 만약 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)([레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 저장/복원)에 $0.1ms$가 걸린다고 치자. $q$를 $1ms$로 잡으면 CPU의 $[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)\%$가 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)이라는 '쓰레기 작업'에 낭비된다. 아키텍트는 반드시 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 시간이 전체 타임 퀀텀의 **1% 미만**이 되도록 $q$를 길게 설계했는지 수학적 점검을 마쳐야 한다.

- **📢 섹션 요약 비유**: 공평함([RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/))의 부작용은 "잘 달리고 있는 놈의 바짓가랑이도 억지로 잡아끌어 내린다"는 점입니다. 줄 서 있는 다른 사람이 없을 때(대기자 0명)는 쿨하게 시계(타이머)를 꺼버리는 유연함이 필요합니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [FCFS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/) ([비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/), 퀀텀 없음) | Round Robin (적절한 타임 퀀텀) | 개선 효과 |
|:---|:---|:---|:---|
| **정량 ([응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/))**| 예측 불가 (수 분~수 시간 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)) | **수십 ms 이내 (예측 가능)** | 시스템의 대화형(Interactive) 반응 극대화 |
| **정성 (공평성)** | 도착 순서의 운빨에 좌우됨 | **모두가 기아([Starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/)) 없이 실행** | 무한 루프 악성코드로부터 시스템 생존 |
| **정량 ([반환 시간](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/172_turnaround_waiting_response_time/))**| 짧은 작업이 희생됨 | 동일 크기 작업 많을 시 전체적으로 늦어짐 | (단점) 평균 [반환 시간](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/172_turnaround_waiting_response_time/)은 다소 희생됨 |

### 미래 전망
- **순수 RR의 소멸과 CFS의 진화**: 현대 리눅스는 순수한 Round Robin을 쓰지 않는다. 대신 **CFS (Completely Fair Scheduler)**를 쓴다. CFS는 고정된 타임 퀀텀($q=10ms$)을 주지 않고, 현재 떠 있는 프로세스 개수에 비례하여 동적으로 퀀텀을 쪼갠다. (예: 총시간 20ms 안에 프로세스가 2개면 10ms씩, 4개면 5ms씩 알아서 탄력적으로 분배)
- **실시간(RT) 큐에서의 부활**: 하지만 음악 재생이나 심장 박동기 제어 같은 실시간 스케줄링 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)(`SCHED_RR`)에서는, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 멋대로 퀀텀을 바꾸는 것을 막기 위해 여전히 철저하고 고정된 순수 [라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/)(Round Robin)이 최강의 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 살아남아 사용되고 있다.

### 결론
[라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/)(Round Robin)과 [시간 할당량](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/179_time_quantum_context_switch/)(Time Quantum)의 발명은 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 역사상 "평등(Equality)"을 하드웨어 타이머라는 무력을 빌려 강제 구현한 최초의 혁명이다. 앞사람이 끝날 때까지 하염없이 멈춰있던 답답한 컴퓨터를, 여러 사람이 동시에 접속해 키보드를 쳐도 즉각 반응하는 마법의 상자로 탈바꿈시켰다. 이 단순한 '순서대로 시간 돌려쓰기' 룰은 지난 50년간 [다단계 피드백 큐](/knowledge-base/studynote/02_operating_system/11_exam_summary/691_mlfq_multi_level_feedback_queue/)([MLFQ](/knowledge-base/studynote/02_operating_system/11_exam_summary/691_mlfq_multi_level_feedback_queue/))와 네트워크 패킷 로드밸런싱의 근간이 되며 모든 트래픽 분배 기술의 영원한 할아버지로 남았다.

- **📢 섹션 요약 비유**: 아이들(프로세스)이 그네를 탈 때 "10번 탔으면 무조건 내려!(Time Quantum)"라는 규칙을 만든 엄마([운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))의 지혜입니다. 한 아이가 울면서 더 타겠다고 떼를 써도, 이 단호한 룰 덕분에 놀이터의 평화와 공정이 유지됩니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [FCFS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/) [호위 효과](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/174_convoy_effect/) ([Convoy Effect](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/174_convoy_effect/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [SJF](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/175_sjf_scheduling/) 기아 ([Starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/)) 발생 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [다단계 피드백 큐](/knowledge-base/studynote/02_operating_system/11_exam_summary/691_mlfq_multi_level_feedback_queue/) ([MLFQ](/knowledge-base/studynote/02_operating_system/11_exam_summary/691_mlfq_multi_level_feedback_queue/)) 천이 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [HRN](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/187_hrn_scheduling/) 대기 시간 공식 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[SJF 기아 (Starvation) 발생]
    │
    ▼
[라운드 로빈 시간 할당량 (Quantum)]
    │
    ├──▶ [다단계 피드백 큐 (MLFQ) 천이]
    └──▶ [HRN 대기 시간 공식]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터라는 놀이기구 1대를 10명의 친구가 같이 타려고 해요. 만약 '순서대로([FCFS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/))' 타면 1번 친구가 10시간 동안 타는 바람에 나머지는 울면서 집에 가야 해요.
2. 그래서 '[라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/)'이라는 새로운 규칙을 만들었어요! "모두 공평하게 딱 5분([시간 할당량](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/179_time_quantum_context_switch/))씩만 타고 무조건 다음 사람에게 양보해!"
3. 5분마다 강제로 내리게 하니까, 10명 모두가 아주 짧은 시간 안에 한 번씩은 놀이기구를 타볼 수 있어서 아무도 울지 않는 최고의 놀이터가 되었답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 690 / 800

← **이전**: [689. SJF 기아 (Starvation) 발생](/knowledge-base/studynote/02_operating_system/11_exam_summary/689_sjf_starvation_and_aging/)
**다음**: [691. 다단계 피드백 큐 (MLFQ) 천이](/knowledge-base/studynote/02_operating_system/11_exam_summary/691_mlfq_multi_level_feedback_queue/) →

---
