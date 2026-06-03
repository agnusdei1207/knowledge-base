+++
title = "778. 프로세스 친화성 (Affinity) 스케줄링"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 프로세스 친화성([CPU Affinity](/knowledge-base/studynote/02_operating_system/02_process_thread/144_cpu_affinity/) / Pinning)은 멀티 코어([SMP](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/195_real_time_scheduling/)) 시스템에서 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 특정 프로세스나 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 이리저리 코어를 옮겨 다니게(Migration) 내버려 두지 않고, **특정 CPU 코어 하나(또는 그룹)에 딱 달라붙어서 평생 그곳에서만 실행되도록 족쇄(Pinning)를 채우는 고성능 스케줄링 튜닝 기법**이다.
> 2. **가치**: [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 0번 코어에서 1번 코어로 이사 갈 때 발생하는 치명적인 L1/L2 캐시 오염(Cache Miss)과 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 플러시 오버헤드를 완벽히 제거하여, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스나 고빈도 네트워크 장비의 메모리 접근 레이턴시를 나노초(ns) 단위로 고정(Deterministic)시킨다.
> 3. **융합**: 현대 매니코어(Many-core) 서버의 핵심 구조인 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/)(불균일 메모리 접근) 아키텍처와 결합하여, CPU 코어와 그 코어에 직결된 물리 램(Local RAM) 간의 최단 거리 고속도로를 강제로 열어주는 인프라 엔지니어링의 최고급 최적화 칼날로 활용된다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **친화성(Affinity)**: "특정 프로세스가 특정 CPU 코어를 얼마나 사랑하고 찰싹 달라붙고 싶어 하는가"를 나타내는 척도.
  - **소프트 친화성 (Soft Affinity)**: OS의 기본 방식. "웬만하면 네가 방금 놀던 코어에서 계속 놀게 해줄게, 근데 그 코어가 너무 바쁘면 다른 빈 코어로 이사(Migration)가야 해!" (최선의 노력, Best-effort).
  - **하드 친화성 (Hard Affinity / Pinning)**: 강제 방식. "넌 무슨 일이 있어도 무조건 3번 코어에서만 실행돼! 3번 코어가 꽉 막혀도 다른 빈 코어로 절대 도망갈 수 없어!" (명시적 강제, CPU Pinning).

- **필요성(문제의식)**: 
  - CPU [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)(예: 리눅스 CFS)의 최우선 목적은 "모든 코어가 쉬지 않게 일을 골고루 나누는 것([Load Balancing](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/196_hard_soft_real_time/))"이다. 그래서 0번 코어가 바쁘면 거기 있던 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) A를 한가한 1번 코어로 몰래 옮겨버린다(Migration).
  - [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) A 입장에서는 0번 코어의 L1 캐시에 방금 다운받은 뜨끈뜨끈한 캐시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수 메가바이트를 예쁘게 다 세팅해 놨는데, 갑자기 1번 코어로 쫓겨나면서 그 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 다 쓰레기가 된다. 1번 코어에서 처음부터 다시 메인 메모리를 뒤져가며 캐시를 쌓아야 하는 엄청난 속도 저하(Cache Cold Miss)가 발생한다.
  - **해결책**: "[스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)야, 제발 눈치 없이 공평하게 나눈답시고 내 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 자리 좀 옮기지 마라! 난 줄 서서 오래 기다려도 좋으니 캐시가 따뜻한 내 자리(Hard Affinity)에 짱박혀 있을 테다!"

  - **소프트 친화성 (기본 OS)**: 은행에서 1번 창구 직원이랑 한참 대출 서류를 맞춰놨는데, 갑자기 지점장이 "1번 창구 너무 바쁘니까 고객님은 텅 빈 2번 창구로 가세요"라며 강제로 옮김. 2번 창구 직원에게 처음부터 서류 설명을 다 다시 해야 함(Cache Miss).
  - **하드 친화성 (Pinning)**: "전 무조건 1번 창구 김대리님한테만 상담받을 겁니다!" 번호표를 뽑고 하루 종일 기다리는 한이 있어도(Load 쏠림) 절대 딴 창구로 가지 않아 설명의 연속성(Cache [Hit](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/263_cache_hit_miss/))을 유지하는 단골 고객.

- **등장 배경**: 
  - 코어가 2~4개이던 시절에는 공평한 분배가 더 중요했다. 그러나 64코어, 128코어 시대로 오며 코어 간 캐시 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)(MESI 핑퐁) [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 비용이 어마어마해지자, 차라리 한 우물만 파는 것이 압도적으로 빠르다는 것을 깨닫고 HFT(초고빈도 매매) 및 DB 아키텍트들의 필수 교양으로 자리 잡았다.

```text
  ┌─────────────────────────────────────────────────────────────┐
  │                 CPU Migration(이주) 오버헤드와 Affinity 방어 원리     │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  [ 1. 스케줄러의 무분별한 이주 (Migration) - 캐시 파괴 ]            │
  │   시간 T1: [ Core 0 ] ◀ Thread A 실행 중 (L1 캐시 99% 웜업 완료!)│
  │               │                                              │
  │   시간 T2: (Core 0 바쁨, Core 1 빔)                            │
  │            스케줄러: "A야 너 Core 1로 방 빼!" (Migration)        │
  │               │                                              │
  │   시간 T3: [ Core 1 ] ◀ Thread A 도착                        │
  │            🚨 대참사: Core 1의 캐시는 텅 빔(Cold).                │
  │            메모리에서 다시 데이터 퍼오느라 수백 마이크로초 멈춤(Stall)! │
  │                                                             │
  │  [ 2. 하드 친화성 (CPU Pinning / taskset) - 캐시 보존 ]          │
  │   설정: `taskset -c 0 ./my_app` (넌 무조건 Core 0번만 써!)     │
  │                                                             │
  │   시간 T1: [ Core 0 ] ◀ Thread A 실행 중 (L1 캐시 웜업)        │
  │   시간 T2: (Core 0 매우 바쁨, Core 1 텅텅 빔)                    │
  │            스케줄러: "A를 옮기고 싶지만 족쇄(Affinity)가 있네. 포기." │
  │   시간 T3: [ Core 0 ] ◀ 대기 큐에서 살짝 기다렸다가 다시 Core 0 실행! │
  │            🚀 성공: 캐시가 그대로 살아있어 메모리 지연 0초로 즉시 연산! │
  └─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 초보 개발자들은 `top` [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 쳤을 때 모든 코어가 고르게 50%씩 일하고 있으면 "스케줄링이 예술이네"라고 착각한다. 하지만 고성능 엔지니어의 눈에는 그것이 "[스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)들이 이 코어 저 코어로 미친 듯이 이사(Migration) 다니며 서로의 L1/L2 캐시를 짓밟고 있는 지옥도"로 보인다. [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 하나의 코어에 강력한 본드로 붙여버리면(Pinning), 비록 다른 코어가 놀고 있어 가끔 CPU 활용률이 찌그러져 보일지언정, 해당 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 **메모리 접근 레이턴시는 흔들림 없는 일직선(Deterministic)**을 그리게 된다. 이것이 실시간(Real-Time) 시스템과 인메모리 DB의 최강 스킬이다.

- **📢 섹션 요약 비유**: 이삿짐센터 직원이 남는 빈 트럭 아무 데나 내 짐을 흩어서 싣게 놔두면([스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 기본값), 도착해서 내 물건을 찾느라 며칠이 걸립니다(캐시 미스). 짐이 많아 트럭 하나에 다 안 실려 기다리더라도, 무조건 "1번 트럭"에만 내 짐을 다 때려 박으라고 강제(Affinity)해야 나중에 정리할 때 1초 만에 물건을 뺄 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 아키텍처와의 필연적 결합 (초격차의 비밀)

현대 서버 CPU(Intel Xeon, AMD EPYC 등)는 하나의 거대한 칩이 아니라, 여러 개의 CPU 덩어리(노드)가 합쳐진 **[NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) ([Non-Uniform Memory Access](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/), 불균일 메모리 접근)** 구조다. Affinity의 진정한 파괴력은 여기서 폭발한다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 NUMA 노드 구조와 CPU Affinity의 완벽한 짝꿍 아키텍처      │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [ NUMA Node 0 ]                           [ NUMA Node 1 ]       │
  │  ┌────────┬────────┐                       ┌────────┬────────┐    │
  │  │ Core 0 │ Core 1 │   (QPI / Infinity     │ Core 2 │ Core 3 │    │
  │  ├────────┴────────┤   Fabric 고속 통신망)   ├────────┴────────┤    │
  │  │ Local RAM (32GB)│◀════════════════════▶│ Local RAM (32GB)│    │
  │  └─────────────────┘                       └─────────────────┘    │
  │                                                                   │
  │   [ 🚨 안티패턴: Affinity 없음 ]                                     │
  │   - 스레드가 Core 0에서 돌면서, 메모리 할당(malloc)을 Node 1의 램에 해버림! │
  │   - Core 0이 데이터를 읽을 때마다 좁은 QPI 다리를 건너 원정(Remote Access) │
  │     가야 하므로 **메모리 속도가 반토막(지연 시간 2배 증가)** 남.             │
  │                                                                   │
  │   [ 🚀 최고 아키텍처: NUMA Pinning (numactl + taskset) ]             │
  │   - 룰: "이 데이터베이스 프로세스는 무조건 Node 0 (Core 0,1)에서만 돌고,      │
  │         메모리도 무조건 Node 0의 램에서만 할당받아라!"                   │
  │   - 결과: QPI 원정 통신망 사용량 0%. 모든 메모리 접근이 최단거리 Local RAM  │
  │         에서 이루어져 극단적인 RAM 스루풋과 캐시 대역폭을 확보.            │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** "불균일(Non-Uniform)"이라는 말은 내 방 책상(로컬 램)에 있는 책을 집는 속도와, 동생 방 책상(원격 램)에 있는 책을 집는 속도가 2배 이상 차이 난다는 뜻이다. 과거 [SMP](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/195_real_time_scheduling/)(대칭형) 구조에서는 램 위치가 평등했지만, 현대 서버는 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 구조라 코어별로 자기 구역 램이 정해져 있다. [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 노드 0번과 1번으로 이리저리 던져버리면(Migration), [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 탯줄(메모리 주소)이 길게 꼬여서 엄청난 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하를 맞는다. 아키텍트는 반드시 `numactl` [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 이용해 **프로세스 족쇄(CPU Pinning)**와 **메모리 족쇄(Membind)**를 하나의 동일한 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 노드에 세트로 묶어서 감금해 버려야 진정한 하드웨어의 신이 될 수 있다.

- **📢 섹션 요약 비유**: 서울 본사 직원이 회의실(CPU 코어)은 부산지사로 쓰고, 서류 보관함(RAM)은 서울 본사에 두면 회의할 때마다 KTX를 타고 서울-부산을 왕복하느라 일(원격 메모리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/))을 못 합니다. 직원을 무조건 서울 회의실과 서울 보관함에 딱 묶어두는([NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) Affinity) 것이 기본 상식입니다.

---

## Ⅲ. 비교 및 연결

### CPU 격리([Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/)) vs CPU 친화성(Affinity)

아키텍트가 무적의 백엔드 서버를 깎아 만들 때 쓰는 양손의 검이다.

| 튜닝 기법 | 동작 철학 | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 및 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) |
|:---|:---|:---|
| **CPU 격리 ([Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/))** | OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)에게 **"이 코어(예: 7번)는 없는 셈 치고 투명인간 취급해!"**라고 명령. 일반 앱이나 백그라운드 잡음이 절대 침범하지 못하는 무균실을 만듦. | 부팅 파라미터 `isolcpus=7` |
| **CPU 친화성 (Affinity)** | 특정 VIP 프로세스의 목덜미를 잡고 **"넌 아까 만들어둔 저 무균실(7번 코어)에 들어가서 너 혼자 평생 살아라!"**라고 직접 꽂아 넣음. | `taskset -c 7 ./my_vip_app`<br>또는 C언어 `sched_setaffinity()` |

**최강의 콤보**: `isolcpus`로 무균실 코어를 텅텅 비워둔 다음, 초저지연을 요하는 네트워크 패킷 수신 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)([DPDK](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/671_dpdk/))나 HFT(고빈도 매매) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)만 `taskset`으로 딱 집어서 무균실 안에 집어넣는다. 이 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 OS의 간섭, 다른 앱의 방해를 1%도 받지 않고 CPU 1알을 통째로 100% 독점하는 신의 권력을 쥔다.

### 과목 융합 관점

- **네트워크 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) (IRQ Affinity / RPS)**: 아무리 내 앱을 7번 코어에 묶어놔도(Pinning), 랜카드([NIC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/)) 하드웨어가 패킷을 받을 때마다 발생시키는 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)(IRQ)가 7번 코어를 찌르면 내 앱은 멈춰야 한다. 그래서 시스템 아키텍트는 내 앱을 7번에 묶었으면, 랜카드 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 핑퐁은 강제로 0~3번 코어만 맞도록 `/proc/irq/{번호}/smp_affinity` 마스크를 튜닝하여 소프트웨어와 하드웨어의 충돌 영역을 모세의 기적처럼 반으로 갈라버린다.
- **클라우드 / [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) (vCPU Pinning)**: [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)나 오픈스택 환경에서 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))에 CPU를 1개 주면, 그건 진짜 물리 코어 1개가 아니라 시분할로 잘린 가상 조각(vCPU)일 뿐이라 여전히 시끄러운 이웃(Noisy Neighbor)에 시달린다. [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) CPU Manager [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 `static`으로 주어, 아예 특정 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 물리 워커 노드의 하드웨어 코어를 독점하게 1:1로 묶어주는(vCPU Pinning) 구성을 해야만 클라우드에서도 베어메탈(Bare-metal) 수준의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 나온다.

- **📢 섹션 요약 비유**: 친화성(Affinity)이 내가 항상 앉는 지정석을 예매한 거라면, 격리([Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/))는 극장장에게 돈을 찔러주고 내 지정석 반경 3미터 이내에는 아무도 표를 팔지 못하게 텅텅 비워두라고(간섭 배제) 한 것입니다. 두 개를 같이 써야 진짜 완벽한 영화 관람([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))이 완성됩니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오 및 트러블슈팅

1. **시나리오 — Nginx/[Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 멀티 인스턴스의 CPU [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) 파국**: 코어가 8개인 서버에 싱글 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 기반인 Redis를 8개 띄웠다. 코어가 8개니 알아서 1개씩 물고 잘 돌 줄 알았는데, 로드가 튀자 전체 레이턴시가 미친 듯이 널뛰기 시작했다.
   - **원인 분석**: OS [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)는 8개의 Redis가 어떤 놈이 어떤 놈인지 모른다. 그냥 무식하게 1번 Redis를 0번 코어에서 돌리다 3번 코어로 던지고, 2번 Redis를 3번 코어에서 돌리다 0번 코어로 밀어낸다. 8개의 무거운 [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 프로세스가 8개의 코어를 엉망진창으로 섞으며 캐시 라인을 매초마다 파괴하고(Cache [Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)) 있었다.
   - **아키텍트 판단 (명시적 1:1 코어 매핑)**: 싱글 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [이벤트 루프](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/) 아키텍처([Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/), Nginx, Node.js)를 멀티코어 장비에 띄울 때는 방관하면 독이 된다. Systemd [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 시작 파일에 각각 `ExecStartPost=/usr/bin/taskset -cp 0 $PID`, `taskset -cp 1 $PID` 식으로 0번 레디스는 0번 코어에, 1번 레디스는 1번 코어에 무식하게 1:1로 자물쇠를 채워(Pinning) 묶어버린다. 캐시 충돌이 거짓말처럼 0이 되고, 처리량이 2배 이상 부드럽게 고정된다.

2. **시나리오 — 빅데이터 [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)/Spark 클러스터의 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 함정**: 2개의 CPU [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)([NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 노드 0, 1)이 달린 강력한 장비에서 Java 기반 JVM 메모리 100GB짜리 스파크 앱을 띄웠는데 시스템 전체가 I/O 지옥에 빠져 허우적댔다.
   - **원인 분석**: 기본적으로 리눅스의 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 메모리 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 `localalloc`(자신이 돌고 있는 코어 쪽 램을 먼저 씀)이다. 스파크 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 Node 0 코어에서 돌면서 Node 0 쪽 램(64GB)을 꽉 채웠다. Node 1 램(64GB)은 텅텅 비어있는데, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 Node 0 램이 꽉 찼으니 멀리 있는 Node 1 램을 가져다 쓰는(Remote Access) 대신 어처구니없게도 자기 발밑의 하드디스크 스왑(Swap) 파티션을 긁어버리기 시작한 것이다([NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) Swap Insanity).
   - **아키텍트 판단 ([NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) Interleave 튜닝)**: 이렇게 덩치가 커서 여러 노드의 램을 다 씹어먹어야 하는 자바/빅데이터 앱은 노드 친화성이 오히려 치명적인 데드락(Swap)을 부른다. 아키텍트는 실행 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 앞에 **`numactl --interleave=all java -jar ...`** 를 붙여 강제로 실행시킨다. 이 룰은 "메모리 할당할 때 0번 노드, 1번 노드 따지지 말고 양쪽에서 지퍼 물리듯 번갈아 가며 골고루 뽑아 써라!"는 뜻이다. 특정 노드 편중에 의한 [스와핑](/knowledge-base/studynote/02_operating_system/06_memory_management/335_swapping/) 발작을 억제하는 빅데이터 인프라의 마법 주문이다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 개발 언어별 CPU 친화성(Affinity) 통제 아키텍처 트리       │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [ 우리 팀의 핵심 코어가 어떤 언어/프레임워크로 작성되었나? ]                  │
  │                │                                                  │
  │                ▼                                                  │
  │      C / C++ / Rust (시스템 네이티브 언어)                          │
  │          └──▶ 최상! 코드 내부에 `sched_setaffinity()` 시스템 콜을 박아서 │
  │                 프로그램 스스로 메인/워커 스레드를 각 코어에 하드코딩 맵핑 설계.│
  │                                                                   │
  │      Nginx / Redis (C 기반이지만 이미 컴파일된 상용 솔루션)             │
  │          └──▶ 설정 파일(`worker_cpu_affinity`)이나 외부 OS 유틸인     │
  │                 `taskset` 명령어를 써서 껍데기 위에서 강제로 묶어버림.     │
  │                                                                   │
  │      Java / Go (자체 스케줄러(JVM, Goroutine)를 가진 언어)           │
  │          └──▶ 🚨 경고! 커널 코어(OS Thread)와 1:1 매핑이 되지 않음.     │
  │                 코드단에서 CPU를 고정하려 해봤자 JVM/Go 런타임이 맘대로 섞어버림.│
  │                 -> 언어 단이 아닌, 아예 Docker/K8s의 컨테이너 레벨(Cgroups)│
  │                 단위에서 `cpuset`으로 물리 코어를 외부에서 통째로 격리해야 함.│
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 코드를 잘 짜는 것과 서버를 튜닝하는 것은 다른 세계다. C언어는 OS의 뼈대([System call](/knowledge-base/studynote/02_operating_system/01_overview_architecture/013_system_call/))를 직접 만질 수 있어 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 1번은 코어 1번에 찰싹 붙이는 외과수술이 가능하다. 하지만 Java나 Go 언어는 OS [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 위에 자기들만의 뚱뚱한 가상 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)(JVM, [Goroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/))를 한 겹 더 깔아놓았기 때문에 OS 단의 Affinity를 걸어도 무용지물이 되는 경우가 많다. 이런 하이레벨 언어는 도커나 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)의 `cpuset` ([Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/)) 기능을 이용해 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 박스 자체를 물리 코어에 덮어씌워 가둬버리는 것이 올바른 아키텍처 설계다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **모든 프로세스에 무지성 Affinity 할당**: "캐시 히트가 좋아지니까 빠르대!"라며 웹서버, DB, 로깅 에이전트 등 모든 프로세스에 각각 코어를 하나씩 하드코딩(taskset) 해버리는 주니어의 만행. 트래픽은 살아 움직인다. 웹이 바쁠 때 DB가 놀 수도 있는데, 철조망(Affinity)을 다 쳐버려서 노는 코어가 바쁜 코어를 도와주지 못하게([Load Balancing](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/196_hard_soft_real_time/) 파괴) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 손발을 잘라버렸다. 결국 트래픽 [스파이크](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/129_spike_agile_technical_investigation/) 한 방에 코어 1번만 100%를 치고 장렬히 전사하며 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 다운된다. Affinity는 **"다른 코어가 평생 0%로 놀아도 절대 뺏어가지 않겠다"**는 각오가 선 절대 권력의 단 1~2개 VIP 프로세스에만 핀포인트로 부여하는 필살기다.

- **📢 섹션 요약 비유**: 모든 직원(프로세스)에게 "넌 영원히 1번 복사기만 써, 넌 2번 정수기만 써"라고 지정(Affinity)해주면 질서는 잡히지만, 1번 복사기에 줄이 100명 서 있어도 옆에 노는 2번 복사기를 쓰지 못해 회사가 망합니다. 지정석은 회장님(VIP 워크로드) 한 명에게만 주고, 나머지는 OS 매니저가 알아서 유동적으로 쓰게 놔두는 게 정답입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 소프트 친화성 (기본 OS 스케줄링) | 하드 친화성 및 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) Pinning 적용 | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (캐시 레이턴시)**| 잦은 이주(Migration)로 L1 미스 패널티 100+ ns | 전용 코어 독점으로 L1 히트 **1~2 ns** 방어 | 인메모리 DB 및 초지연 트레이딩의 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 1/50 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) |
| **정량 (메모리 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/))** | [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 노드 간 원격 메모리 참조로 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 고갈 | Local 메모리 강제 매핑으로 QPI [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 트래픽 0 | 매니코어 서버(64코어 이상)의 선형적(Linear) 확장성 보장 |
| **정성 (지터 Jitter)** | OS 간섭으로 처리 시간이 1ms~100ms 널뛰기 함 | 항상 1ms 고정의 결정론적(Deterministic) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 영상/음성 스트리밍 및 로봇 제어의 마이크로 버벅임 원천 제거 |

### 미래 전망
- **eBPF를 통한 지능형 동적 Pinning**: 무식하게 코드를 박아두는 하드 파티셔닝을 넘어서, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 단에 기생하는 [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 프로그램이 런타임에 L3 캐시 미스율과 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 토폴로지를 1초 단위로 분석하여, "지금 이 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 3번 코어로 던지고 메모리를 복사해 주는 게 낫겠다"고 판단해 동적으로 족쇄를 묶고 푸는(Dynamic Affinity) [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 자기 주도 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 차세대 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 최적화의 꽃이 될 것이다.
- **클라우드 서버리스의 한계 극복**: AWS [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 같은 서버리스는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 떴다 사라지므로 코어 친화성이란 개념 자체가 존재할 수 없다 (콜드 스타트의 지옥). 하지만 점차 극도의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 요구하는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 추론이 서버리스로 올라타면서, 클라우드 제공자가 투명하게 이면에서 특정 워크로드를 미리 웜업된 특정 물리 코어와 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 램에 강제로 꽂아주는 'Micro-AffinityaaS' 계층이 은밀히 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)되고 있다.

### 참고 표준
- **sched_setaffinity (POSIX / Linux)**: 유닉스 계열 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)에서 프로세스의 실행 가능 CPU 마스크(비트맵)를 조작하여 OS [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)의 목줄을 쥐는 C언어 공식 시스템 콜.
- **[ACPI](/knowledge-base/studynote/02_operating_system/01_overview_architecture/075_acpi/) SRAT (System Resource Affinity Table)**: 메인보드 하드웨어 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)(BIOS/[UEFI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/706_uefi/))가 OS 부팅 시 "1번 CPU의 로컬 램은 이거고, 2번 CPU 로컬 램은 저거야"라고 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 지도를 그려서 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 넘겨주는 핵심 하드웨어 스펙.

프로세스 친화성 스케줄링은 범용 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 가진 "가장 멍청한 공평함"에 반기를 들고, "가장 이기적인 독재"를 선언하는 아키텍처적 결단이다. [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)는 코어를 놀리지 않으려 끊임없이 짐(프로세스)을 이리저리 옮기려 하지만, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 중력이 되어버린 빅데이터 시대에는 그 짐을 옮기는 비용(캐시 붕괴) 자체가 짐보다 더 무거워져 버렸다. 족쇄(Pinning)를 채워 한 자리에 뿌리박게 만드는 이 튜닝은, 소프트웨어 엔지니어가 하드웨어 실리콘 칩의 미세한 맥박과 나노초의 떨림까지 꿰뚫어 보고 통제하는 가장 관능적인 인프라 예술이다.

- **📢 섹션 요약 비유**: 식당 매니저(OS)가 테이블 회전율(공평성)을 높이겠다고 밥 먹는 손님을 계속 옆 테이블로 메뚜기 뛰게 만들면(기본 스케줄링) 손님은 숟가락 챙기느라(캐시 미스) 화가 나서 나갑니다. VIP 손님에게는 구석의 아늑한 '지정석 룸(CPU Pinning)'을 주고 절대 건드리지 않아야 가장 비싼 코스 요리(고성능 연산)를 완벽하게 즐기고 지갑을 열게 됩니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [클라우드 컴퓨팅](/knowledge-base/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/) OS [자원 풀링](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/638_resource_pooling_cxl/) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러 [메모리 보호](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/307_memory_protection/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [부하 균등화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/196_hard_soft_real_time/) ([Load Balancing](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/196_hard_soft_real_time/)) 큐 이주 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 동적 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 트레이싱 프레임워크 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[OOM 킬러 메모리 보호 정책]
    │
    ▼
[프로세스 친화성 (Affinity) 스케줄링]
    │
    ├──▶ [부하 균등화 (Load Balancing) 큐 이주]
    └──▶ [eBPF 동적 커널 트레이싱 프레임워크 성능]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 철수는 1번 책상(코어)에 앉아서 크레파스랑 스케치북(L1 캐시)을 다 쫙 펴놓고 그림을 아주 빠르게 그리고 있었어요.
2. 그런데 선생님([운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))이 공평하게 앉아야 한다며 갑자기 철수를 3번 빈 책상으로 가라고 쫓아냈어요. 철수는 짐을 다 싸서 3번 책상에 다시 세팅하느라(캐시 미스) 엄청난 시간을 낭비했죠.
3. 그래서 화가 난 철수는 "나 1번 책상에 밧줄로 묶어주세요!(CPU 족쇄/Pinning)"라고 했고, 그 뒤로는 아무도 철수 자리를 안 뺏어서 세계에서 그림을 제일 빨리 그리는 아이가 되었답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 778 / 800

← **이전**: [777. OOM 킬러 메모리 보호 정책 (OOM Killer Memory Protection)](/knowledge-base/studynote/02_operating_system/11_exam_summary/777_oom_killer_memory_protection/)
**다음**: [779. 부하 균등화 (Load Balancing) 큐 이주](/knowledge-base/studynote/02_operating_system/11_exam_summary/779_load_balancing_queue_migration/) →

---
