---
title: "Interrupt Scheduling"
date: "2026-05-08"
tags:
  - "studynote-operating-system"
weight: 199
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 스케줄링 ([Interrupt](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) Scheduling)은 하드웨어가 발생시키는 수많은 [비동기적](/studynote/02_operating_system/01_overview_architecture/017_hardware_interrupt/) [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) [신호](/studynote/02_operating_system/02_process_thread/130_signal/)(IRQ)들을 운영체제가 어떤 코어에, 어떤 우선순위로, 언제 분배하여 처리할 것인지 결정하는 <strong><a href="/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> 최하단부의 자원 분배 메커니즘</strong>이다.
> 2. **가치**: [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 처리가 특정 코어에만 몰리면 해당 코어의 사용자 프로세스가 굶어 죽는 현상([Livelock](/studynote/02_operating_system/05_deadlock/315_livelock_vs_deadlock/))이 발생하므로, 이를 다수의 코어로 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)(IRQ [Load Balancing](/studynote/02_operating_system/03_cpu_scheduling/196_hard_soft_real_time/))시켜 시스템 전체의 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)과 네트워크 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))을 극한으로 끌어올린다.
> 3. **융합**: 고속의 네트워크 카드(100Gbps [NIC](/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/)) 환경에서 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 폭풍([Interrupt](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) Storm)을 방어하기 위해 리눅스는 수신 패킷 처리를 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)(Top Half)와 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(Bottom Half)로 쪼개고, <strong>NAPI(병합 <a href="/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/">폴링</a>)</strong>와 <strong>RPS/RFS(Receive Packet Steering)</strong>를 통해 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 스케줄링 패러다임을 혁신했다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 마우스 클릭, 디스크 읽기 완료, 네트워크 패킷 도착 등 하드웨어는 CPU에게 즉각적인 처리를 요구하며 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)([Interrupt](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/))를 쏜다. 이때 다중 코어 시스템에서 "어느 코어가 이 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 받아 [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/)([인터럽트 서비스 루틴](/studynote/02_operating_system/01_overview_architecture/020_isr/))을 실행할지" 동적으로 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)하고 분배하는 기술을 뜻한다.
- **필요성**: 싱글 코어 시절에는 무조건 0번 코어가 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 다 맞았다. 하지만 멀티 코어 시대에 초당 100만 개의 패킷이 들어올 때 0번 코어 혼자 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 다 처리하면, 0번 코어는 100% [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드(sy)에 갇혀 사용자 앱(us)을 돌리지 못하고 뻗어버리며, 나머지 1~7번 코어는 할 일이 없어 노는 기형적인 로드 임밸런스(Load Imbalance)가 발생한다.

- **등장 배경**: 과거 1Gbps 랜카드 시절에는 CPU가 버틸 만했으나, 10Gbps, 100Gbps [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 시대가 열리며 '[인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 처리 자체의 오버헤드'가 전체 서버 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 깎아먹는 최대 주범으로 등극했다. 이를 타파하기 위해 하드웨어적 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 분배(APIC)와 소프트웨어적 큐잉(NAPI)이 융합하며 발전했다.

```text
  [단일 코어 집중 vs 다중 코어 인터럽트 분산 (IRQ Balancing)]

  (1) 안 좋은 예: 인터럽트 0번 코어 쏠림 (Interrupt Storm)
  [ NIC (랜카드) ] -- (패킷 10만 개 도착) ---> [ 코어 0 ] 🚨 (CPU 100% 포화, 터짐)
                                            [ 코어 1 ] (0%)
                                            [ 코어 2 ] (0%)

  (2) 좋은 예: 인터럽트 스케줄링 (IRQ Affinity 분산)
  [ NIC (랜카드) ] -+- (패킷 3만 개) -----> [ 코어 0 ] (30% 부하)
   (다중 큐 지원)   +- (패킷 3만 개) -----> [ 코어 1 ] (30% 부하)
                   +- (패킷 4만 개) -----> [ 코어 2 ] (30% 부하)
   >> 시스템 전체가 여유를 갖고 백엔드 사용자 애플리케이션을 돌릴 수 있다.
```
**[다이어그램 해설]** 초고성능 서버 튜닝의 첫걸음은 `top` 명령어를 쳤을 때 특정 코어의 `si` (소프트 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)) 혹은 `hi` (하드 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)) 수치만 100%를 치고 있는지 확인하는 것이다. 코어 1개에 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 몰리면 다른 코어가 아무리 널널해도 시스템 네트워크 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)은 그 코어 1개의 한계에 갇혀버린다. [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 찢어서 던지는 것이 스케줄링의 핵심이다.

- **📢 섹션 요약 비유**: 택배([인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/))가 하루에 1만 개 오는데, 경비실 아저씨 1명(코어 0)한테만 전부 다 받으라고 하면 아저씨는 쓰러집니다. 택배차를 여러 동(멀티 코어)으로 흩어지게 해서 경비원 10명이 1천 개씩 나눠 받게 만드는 것이 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 스케줄링입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 하드웨어 레벨의 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) (APIC)
x86 시스템에서는 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 분배하기 위해 CPU 칩 외부에 <strong>I/O APIC (Advanced Programmable <a href="/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/">Interrupt</a> Controller)</strong>라는 하드웨어 칩이 존재한다.
1. 하드웨어([NIC](/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/) 등)가 I/O APIC에 핀으로 전기 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 쏜다.
2. I/O APIC는 리눅스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 미리 설정해 둔 '[인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 목적지 테이블(Redirection Table)'을 읽는다.
3. "아, 랜카드(IRQ [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)) [신호](/studynote/02_operating_system/02_process_thread/130_signal/)는 CPU 코어 0, 1, 2, 3에게 [라운드 로빈](/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/)으로 쏴주라고 되어있네!" 하고 판단하여 특정 코어의 Local APIC로 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 전달한다.

### 리눅스의 Top Half 와 Bottom Half ([인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 쪼개기)
[인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 받은 코어는 하던 일을 멈추고 [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/)([Interrupt Service Routine](/studynote/01_computer_architecture/08_io_storage_systems/317_isr/))을 무조건 즉시 실행해야 한다. 이때 코어가 너무 오랫동안 묶여있으면 다른 급한 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 놓친다. 그래서 리눅스는 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 처리를 두 동강 냈다.

- <strong>Top Half (하드 <a href="/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/">인터럽트</a>)</strong>: "일단 패킷 도착했다고 ACK 쳐주고 메모리에 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 툭 던져놓고 1ms 만에 끝낸다!" (즉시성, 선점 방어)
- <strong>Bottom Half (소프트 <a href="/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/">인터럽트</a>, Tasklet)</strong>: Top Half가 던져놓고 간 패킷 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 여유 있게 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 해제하고 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/IP [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)으로 밀어 올리는 긴 작업. (일반 프로세스처럼 나중에 스케줄링되어 실행됨)

```text
  +----------------------------------------------------------------------+
  |         리눅스 인터럽트 처리의 이원화 구조 (Top & Bottom Half)       |
  +----------------------------------------------------------------------+
  |                                                                      |
  |   [ 1단계: Top Half (매우 빠름, 선점 불가 구역) ]                    |
  |   -> 랜카드가 패킷 도착 인터럽트(IRQ) 쏨                              |
  |   -> 코어가 하던 일 멈추고 NIC 버퍼에서 메모리(Ring Buffer)로 복사    |
  |   -> "나머지 긴 작업은 Bottom Half로 예약할게!" 하고 즉시 빠져나옴.   |
  |                                                                      |
  |   [ 2단계: Bottom Half (ksoftirqd 데몬 스케줄링) ]                   |
  |   -> 커널 스케줄러가 여유 있을 때 `ksoftirqd/0` (코어 0의 데몬)를 띄움|
  |   -> 예약된 패킷들을 꺼내서 TCP 스택 분석, 방화벽(iptables) 룰 검사   |
  |   -> 사용자 애플리케이션(Nginx) 소켓으로 데이터 전달 완료             |
  +----------------------------------------------------------------------+
```
**[다이어그램 해설]** 이 구조 덕분에 리눅스는 1초에 수십만 번의 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 폭격을 맞아도 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 완전히 얼어붙지 않는다. Top Half는 치고 빠지기의 달인이고, 진짜 무거운 계산은 Bottom Half 데몬(`ksoftirqd`)으로 위임하여, <strong>일반 프로세스 스케줄러가 <a href="/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/">인터럽트</a> 후속 작업마저 통제(스케줄링)할 수 있게</strong> 만든 천재적 설계다.

- **📢 섹션 요약 비유**: 우체부(랜카드)가 소포를 가져왔을 때, 하던 일 멈추고 1초 만에 문만 열어서 현관에 툭 던져두는 게 Top Half고, 주말에 시간 날 때 현관에 쌓인 박스 100개를 커터칼로 정성스레 뜯어서 거실(애플리케이션)로 옮기는 게 Bottom Half입니다.

---

## Ⅲ. 비교 및 연결

### [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 처리 패러다임의 진화: NAPI ([New](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/))

순수 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 방식의 치명적 결함은 <strong><a href="/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/">인터럽트</a> 폭풍(<a href="/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/">Interrupt</a> Storm)</strong>이다. 초당 10만 개 패킷이 들어오면 10만 번의 잦은 문맥 교환이 발생하여([Livelock](/studynote/02_operating_system/05_deadlock/315_livelock_vs_deadlock/)) 시스템이 아예 멈춘다. 이를 해결하기 위해 [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)([Polling](/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/))과 섞은 NAPI가 등장했다.

| 처리 방식 | 동작 원리 | 부하 시 시스템 상태 |
|:---|:---|:---|
| <strong>순수 <a href="/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/">인터럽트</a> (과거)</strong> | 패킷 1개당 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 1번 발생 | 10만 개 오면 10만 번 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 발생. <strong><a href="/studynote/02_operating_system/05_deadlock/315_livelock_vs_deadlock/">Livelock</a> 발생 (사망)</strong> |
| <strong>순수 <a href="/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/">폴링</a> (<a href="/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/">Polling</a>)</strong> | 주기적으로 "패킷 왔어?" 계속 물어봄 | 패킷이 없을 때도 계속 물어보느라 **CPU 100% 낭비** |
| **NAPI (하이브리드)** | <strong>첫 패킷은 <a href="/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/">인터럽트</a>로 받음. 그 이후 폭주하면 <a href="/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/">인터럽트</a>를 끄고 <a href="/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/">폴링</a> 모드로 전환하여 버퍼의 수천 개 패킷을 한 방에 퍼옴.</strong> | 패킷이 없으면 조용(절약). 패킷 폭주 시 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 오버헤드 0으로 삭제. **극한의 효율** |

### 소프트웨어적 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) [로드 밸런싱](/studynote/03_network/16_data_center_cloud/833_load_balancing_l4_l7_switch_traffic_distribution/): RPS / RFS
하드웨어(랜카드 다중 큐)가 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 코어별로 쪼개주지 못하는 저가형 랜카드를 쓸 때, 리눅스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 **소프트웨어로 가상의 다중 큐를 만들어** 0번 코어에 들어온 패킷들을 1~7번 코어로 던져주는 기술이다.
- **RPS (Receive Packet Steering)**: 패킷의 IP/[Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 해시값을 구해 1번, 2번, 3번 코어에 골고루 분배한다. (소프트웨어 [라운드 로빈](/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/))
- **RFS (Receive Flow Steering)**: RPS보다 더 똑똑하다. 이 패킷을 받아서 최종적으로 처리할 Nginx 애플리케이션([스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/))이 3번 코어에서 돌고 있다면, 굳이 1번 코어에 안 주고 <strong>3번 코어에게 핀포인트로 패킷을 던져 캐시 <a href="/studynote/01_computer_architecture/06_memory_hierarchy_cache/264_hit_ratio/">적중률</a>(<a href="/studynote/02_operating_system/11_exam_summary/778_process_affinity_scheduling_pinning/">Affinity</a>)을 100%로 보장</strong>한다.

- **📢 섹션 요약 비유**: NAPI는 첫 손님이 벨([인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/))을 누르면 매니저가 나가서 문을 활짝 열어놓고 수백 명을 줄 세워 한 번에 처리([폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/))하는 기법이고, RFS는 들어온 손님의 관상(IP/[Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))을 보고 그 손님을 가장 잘 아는 전담 웨이터(특정 코어)에게 콕 집어 배정해 주는 지능형 매니징입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오
1. **Irqbalance 데몬의 튜닝 (끄느냐 마느냐)**: 범용 리눅스는 부팅 시 `irqbalance`라는 데몬을 띄워놓는다. 이 녀석은 10초마다 각 코어의 부하를 검사해서, 0번에 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 몰리면 APIC 설정을 바꿔 1, 2, 3번으로 이사(Balancing)시켜 준다.
   - **문제 발생**: 고성능 DB([Redis](/studynote/05_database/04_transactions_concurrency/542_redis/), [Oracle](/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/)) 서버에서 이 데몬이 계속 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 목적지를 바꾸면, 패킷이 도착하는 코어와 연산하는 코어가 엇갈려 지독한 캐시 미스가 발생하고 응답 지연이 튄다.
   - <strong>실무 조치 (격리 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>)</strong>: 초고도 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 튜닝 시 엔지니어는 아예 `systemctl stop irqbalance`로 오지랖 데몬을 꺼버린다. 그리고 `smp_affinity` 파일을 직접 수정하여 랜카드 1번 큐는 코어 1번에, 2번 큐는 코어 2번에 영구적으로 수동 결박(Pinning)시킨다.
2. <strong>K8s 클라우드에서의 100G <a href="/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/">NIC</a> / <a href="/studynote/01_computer_architecture/15_advanced_topics/671_dpdk/">DPDK</a> <a href="/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> 우회</strong>: [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 통신망의 패킷 스위칭(UPF) 컨테이너는 초당 수천만 개의 패킷을 받아야 한다. 이때 NAPI든 RPS든 리눅스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 스케줄러가 개입하는 순간 아무리 잘 짜도 10G 이상의 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 감당 못 하고 병목이 걸린다.
   - **아키텍처 결단**: 패킷이 랜카드에 들어올 때 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)로 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 쏘는 것(IRQ) 자체를 금지한다. 대신 유저 스페이스의 애플리케이션 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 코어를 100% 독점한 상태로 랜카드 메모리([NIC](/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/) RX Ring)를 직접 무한 [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)([Polling](/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/))하여 퍼 나른다. 이것이 인텔의 <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/671_dpdk/">DPDK</a> (<a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> Plane Development Kit)</strong>이자, [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 스케줄링을 통째로 부정하고 우회(Bypass)하는 클라우드 네트워크 아키텍처의 정점이다.

```text
  +-----------------------------------------------------------------------+
  |     고대역폭(10G+) 서버의 인터럽트 처리 성능 최적화 의사결정 트리     |
  +-----------------------------------------------------------------------+
  |                                                                       |
  |   [서버 튜닝: Top 명령어 상 'si(softirq)'가 1개 코어에서 100% 임]     |
  |                |                                                      |
  |                v 랜카드가 하드웨어 다중 큐(RSS)를 지원하는가?         |
  |      [지원함 (Multi-Queue NIC)]                                       |
  |       +--> 조치 1: irqbalance 끄기                                     |
  |       +--> 조치 2: 각 NIC 큐별로 smp_affinity에 코어 1:1 매핑          |
  |                                                                       |
  |      [지원 안 함 (Single-Queue 저가형 NIC)]                           |
  |       +--> 조치 1: 리눅스 커널 RPS/RFS 활성화 (`echo f > rps_cpus`)    |
  |       +--> 조치 2: 소프트웨어적으로 인터럽트 부하를 타 코어로 강제 산란|
  +-----------------------------------------------------------------------+
```
**[다이어그램 해설]** 리눅스 서버 운영의 가장 흔하면서도 치명적인 병목 해결법이다. 랜카드는 10G를 샀는데 다운로드 속도가 1G밖에 안 나온다면 100% 확률로 0번 코어 하나만 `si` 부하를 맞고 장렬히 전사한 것이다. 이를 여러 코어로 찢어주기만 하면([Affinity](/studynote/02_operating_system/11_exam_summary/778_process_affinity_scheduling_pinning/) 튜닝) 별도의 하드웨어 추가 없이 속도가 4배, 8배로 선형 증가하는 마법을 볼 수 있다.

- **📢 섹션 요약 비유**: 8차선 고속도로(10G 랜카드)를 뚫어놨는데 톨게이트 직원([인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 처리 코어)이 1명뿐이라 차가 다 막힌 상태입니다. 직원을 8명 고용해서 각 차선에 세워두는([Affinity](/studynote/02_operating_system/11_exam_summary/778_process_affinity_scheduling_pinning/) 매핑) 세팅을 해줘야 진짜 고속도로가 됩니다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과
[인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 스케줄링(IRQ [Affinity](/studynote/02_operating_system/11_exam_summary/778_process_affinity_scheduling_pinning/), RPS/RFS)을 시스템 워크로드에 맞게 정밀하게 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)시키면, 특정 CPU 코어의 [Livelock](/studynote/02_operating_system/05_deadlock/315_livelock_vs_deadlock/) 마비를 막고, I/O 디바이스([NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/), [NIC](/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/))가 가진 물리적 최대 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)([Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))을 리눅스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 병목 없이 100%까지 극한으로 끌어올릴 수 있다.

### 결론 및 미래 전망
과거의 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 스케줄링은 "어떻게 하면 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 덜 아프게 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 잘 받을까"에 집중했다. 하지만 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 단위가 TB(테라바이트), 100Gbps로 폭증하는 클라우드 환경에서는 <strong>"<a href="/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/">인터럽트</a> 자체가 죄악(Overhead)"</strong>으로 규정되었다.
미래의 패러다임은 CPU가 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 처리하는 대신, 스마트 랜카드(SmartNIC/[DPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/436_dpu/))가 내장된 ARM 코어로 직접 패킷을 까서 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)시키거나(하드웨어 [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)), [eBPF](/studynote/02_operating_system/10_security/615_ebpf/)([XDP](/studynote/01_computer_architecture/15_advanced_topics/670_xdp/)) 기술을 통해 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 깊이 들어오기 전에 초입에서 패킷을 드롭(Drop)해버려 CPU [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 자체를 무효화하는 '제로 오버헤드([Zero](/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/) Overhead)' 아키텍처로 진화하고 있다.

- **📢 섹션 요약 비유**: 옛날엔 쏟아지는 스팸 우편([인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/))을 어떻게 직원 10명이 효율적으로 분리수거할지 고민했다면, 미래 기술은 아예 우체국(SmartNIC) 단에서 스팸 필터를 걸어 회사 문턱(CPU)으로 배달조차 못 하게 원천 차단하는 혁신적 방향으로 가고 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 프로세서 친화성 (Processor [Affinity](/studynote/02_operating_system/11_exam_summary/778_process_affinity_scheduling_pinning/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [멀티코어 스케줄링](/studynote/02_operating_system/03_cpu_scheduling/198_edf_scheduling/) ([Multicore Scheduling](/studynote/02_operating_system/03_cpu_scheduling/198_edf_scheduling/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 이기종 [다중 처리기 스케줄링](/studynote/02_operating_system/03_cpu_scheduling/193_smp_symmetric_multiprocessing/) (HMP) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 실시간 스케줄링 (Real-time Scheduling) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[멀티코어 스케줄링 (Multicore Scheduling)]
    |
    v
[하이퍼스레딩 (Hyper-threading) / SMT (Simultaneous Multithreading) 스케줄링]
    |
    +---> [이기종 다중 처리기 스케줄링 (HMP)]
    +---> [실시간 스케줄링 (Real-time Scheduling)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 엄마(CPU 코어 0번) 혼자 요리를 하고 있는데, 아빠, 언니, 오빠(하드웨어들)가 동시에 "밥 줘! 물 줘! 휴지 줘!" 하고 벨([인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/))을 마구 누르면 엄마가 쓰러지겠죠?
2. 그래서 가족회의를 해서 <strong><a href="/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/">인터럽트</a> 스케줄링</strong>을 짰어요. 아빠 벨이 울리면 첫째 아들(코어 1번)이 가고, 언니 벨이 울리면 둘째 딸(코어 2번)이 가기로 규칙을 나눈 거예요.
3. 이렇게 벨소리([인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/))를 여러 명에게 골고루 찢어서 분배해 주면, 엄마도 안 쓰러지고 가족들 심부름도 빛의 속도로 빨리 해결되는 평화로운 집이 된답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 199 / 800

<- **이전**: [198. 멀티코어 스케줄링 (Multicore Scheduling) - 메모리 스톨 (Memory Stall) 대응](/studynote/02_operating_system/03_cpu_scheduling/198_edf_scheduling/)
**다음**: [200. 실시간 커널 (Real-time Kernel) / PREEMPT_RT](/studynote/02_operating_system/03_cpu_scheduling/200_real_time_kernel_preempt_rt/) ->

---
