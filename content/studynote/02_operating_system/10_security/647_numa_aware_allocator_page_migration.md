+++
title = "647. NUMA 인지형 메모리 할당기 커널 페이지 이동 정책 프레임워크 설계 (NUMA Aware Allocator Page Migration)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 현대의 멀티 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)/매니코어 서버는 CPU 코어와 메모리가 짝을 지어 묶인 <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/">NUMA</a> (<a href="/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/">Non-Uniform Memory Access</a>)</strong> 아키텍처를 따른다. 내 코어에 달린 메모리(Local)를 읽는 것은 빠르지만, 남의 코어에 달린 메모리(Remote)를 읽으면 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)(QPI/UPI) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 때문에 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 크게 떨어진다.
> 2. <strong>해결 (할당 및 이동 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>)</strong>: 이를 해결하기 위해 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/">NUMA</a>-Aware Allocator</strong>를 통해 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 돌고 있는 코어의 로컬 메모리에 우선 할당(First-touch)하며, [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 다른 코어로 이주(Migration)하면 백그라운드 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(`numad`)가 해당 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 자주 쓰는 메모리 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)도 새 코어 근처로 이주시키는 <strong>자동 <a href="/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">페이지</a> 이동(AutoNUMA)</strong> [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 수행한다.
> 3. **가치**: 빅데이터, 인메모리 DB(SAP HANA), 고성능 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 환경에서 개발자의 코드 수정 없이도 OS 스스로 메모리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))을 최소화하여 시스템 전체의 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))을 수십 % 끌어올리는 현대 OS 스케줄링의 꽃이다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/">NUMA</a> 노드(Node)</strong>: 물리적인 CPU [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)과 그 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)에 직접 연결된 RAM 슬롯의 묶음.
  - <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/">NUMA</a>-Aware Allocator</strong>: 프로세스가 메모리를 달라고 할 때, 아무 메모리나 주지 않고 현재 프로세스가 돌고 있는 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 노드와 가장 가까운 로컬 메모리를 찾아서 주는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 똑똑한 메모리 할당기.
  - <strong><a href="/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">Page</a> Migration (<a href="/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">페이지</a> 이동)</strong>: [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)에 의해 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 Node 0에서 Node 1로 이사 갔을 때, 기존 Node 0에 남아있던 메모리(이제 원격 메모리가 됨)를 Node 1의 메모리로 몰래 복사/이동시켜 주는 프레임워크.

- **필요성 (SMP의 붕괴와 메모리 병목)**:
  - 과거 코어가 몇 개 없던 시절([SMP](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/195_real_time_scheduling/))에는 모든 CPU가 하나의 거대한 메모리를 똑같은 속도로 공유했다.
  - 코어가 64개, 128개로 늘어나자 모든 코어가 하나의 메모리 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)(통로)를 향해 돌진하면서 심각한 병목(Traffic Jam)이 터졌다.
  - 하드웨어 제조사는 이를 해결하기 위해 메모리를 코어별로 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)([NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/))시켰다. 하지만 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 옛날처럼 "남의 메모리든 내 메모리든 대충 빈 곳을 쓰게" 놔두면 캐시 미스보다 끔찍한 원격 메모리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 지옥이 펼쳐진다.
  - **해결책**: [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)(어느 CPU에서 돌릴지)와 메모리 할당기(어디에 저장할지)가 융합되어, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 코어를 물리적으로 가장 가까운 곳에 붙여놓는 '[데이터 지역성](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/)([Data Locality](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/))' 강제 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 필요해졌다.

  - <strong><a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/195_real_time_scheduling/">SMP</a> (옛날 방식)</strong>: 회사에 거대한 중앙 정수기가 하나 있다. 100명의 직원이 물을 마시려 매번 중앙으로 걸어가야 해서 줄이 엄청 길다(병목).
  - <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/">NUMA</a> (현대 방식)</strong>: 사무실을 4개 구역(Node)으로 쪼개고 구역마다 정수기(Local Memory)를 놨다. 내 구역 물을 마시면 1초, 다른 구역으로 넘어가서 마시면 5초(Remote Memory)가 걸린다.
  - <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/">NUMA</a> 인지 할당 / <a href="/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">페이지</a> 이동</strong>: 신입사원이 들어오면 무조건 자기 자리 옆 정수기 물을 떠 준다(First-touch 할당). 만약 사원이 부서를 이동([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 마이그레이션)하면, 총무팀(AutoNUMA)이 밤에 몰래 그 사원의 짐(메모리 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/))도 새 부서 옆으로 옮겨준다.

- **발전 과정**:
  1. <strong><a href="/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/">NUMA</a></strong>: 하드웨어만 NUMA로 분리. OS는 이를 인지하지 못해 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 오히려 하락함.
  2. **수동 통제 (numactl)**: 관리자가 수동으로 특정 프로세스를 특정 노드에 못 박음(Pinning).
  3. **AutoNUMA (Linux 3.8+)**: [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)와 메모리 관리자가 연동되어, 런타임에 스스로 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)와 메모리를 한 쌍으로 묶어 이동시키는 자동화 프레임워크 완성.

- **📢 섹션 요약 비유**: 이삿짐을 나를 때 사람(CPU)만 보내는 것이 아니라, 그 사람이 자주 쓰는 필수 도구(메모리 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/))까지 함께 포장해서 새 집으로 자동 배송해 주는 스마트한 이사 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 하드웨어 토폴로지 (Topology)

2소켓 서버(CPU가 2개 꽂힌 서버)의 전형적인 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 토폴로지다.

| 노드 구분 | 물리적 구성 | 접근 [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) ([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/">NUMA</a> Node 0</strong> | CPU 0 (Core 0~31) + RAM Slot A (256GB) | **로컬 접근 (Local Access): 약 80ns** |
| <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/">NUMA</a> Node 1</strong> | CPU 1 (Core 32~63) + RAM Slot B (256GB)| 로컬 접근 (Local Access): 약 80ns |
| **인터커넥트** | Node 0 ↔ Node 1 (Intel UPI / AMD xGMI) | **원격 접근 (Remote Access): 약 120~150ns** |

---

### [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 메모리 할당 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) (Allocation Policies)

프로세스가 `malloc()`을 호출하고 처음 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쓸 때, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 아래 4가지 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 중 하나를 따른다.

1. **First-Touch (기본값)**: 메모리를 처음 건드리는([Page Fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) 발생) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 현재 돌고 있는 코어의 로컬 노드에 할당한다. 가장 합리적이다.
2. **Interleave (교차 할당)**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 Node 0, Node 1, Node 0, Node 1에 번갈아 가며 뿌린다. 단일 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 떨어지지만, 100개의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 동시에 큰 배열을 읽을 때 특정 메모리 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)만 터지는 병목 현상을 방지([대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 극대화)할 때 쓴다. (주로 거대 DB에서 사용)
3. **Bind (고정 할당)**: 무조건 내가 지정한 특정 노드(예: Node 0)에만 할당해라. 꽉 차면 스왑(Swap)을 쓰거나 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬을 당하더라도 다른 노드는 쓰지 않겠다는 독한 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/).
4. **Preferred (우선 할당)**: Node 0에 먼저 줘보고, 없으면 그제야 Node 1의 메모리를 써라. (유연한 Bind)

---

### AutoNUMA: [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 스캐닝 및 마이그레이션 아키텍처

[스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 A 노드에서 B 노드로 이사 갔을 때, 남겨진 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 어떻게 데려올까? [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/">NUMA</a> Balancing</strong> 메커니즘이 작동한다.

```text
  +-------------------------------------------------------------------+
  |                 AutoNUMA (NUMA Balancing) 동작 메커니즘            |
  +-------------------------------------------------------------------+
  |                                                                   |
  |  [상황 1: 초기 상태 (원격 접근 발생)]                                 |
  |   - 스레드는 Node 1에서 실행 중인데, 데이터(Page X)는 Node 0에 있음.      |
  |   - 스레드가 Page X를 읽을 때마다 UPI 버스를 타느라 성능이 저하됨.          |
  |                                                                   |
  |  [상황 2: 커널의 함정 설치 (PTE Scanning)]                           |
  |   - 커널 데몬(numad)이 주기적으로 Page X의 페이지 테이블 엔트리(PTE)에     |
  |     가짜로 'PROT_NONE (접근 불가)' 권한을 걸어버린다. (Unmapping)      |
  |                                                                   |
  |  [상황 3: 함정 발동 (NUMA Hinting Fault)]                           |
  |   - Node 1의 스레드가 Page X를 읽으려 시도함.                         |
  |   - 권한이 없으므로 하드웨어 [Page Fault] 트랩 발생!                  |
  |                                                                   |
  |  [상황 4: 커널의 이동 결정 및 이사 (Migration)]                       |
  |   - 커널: "잡았다! Node 1에 있는 녀석이 Node 0의 Page X를 자주 쓰는군!"    |
  |   - 커널은 Page X를 Node 0에서 Node 1의 빈 메모리로 [몰래 복사]한다.     |
  |   - 복사가 끝나면 PTE를 새로운 Node 1의 주소로 고치고 권한을 복구함.       |
  |                                                                   |
  |  [결과] 이제 스레드는 Node 1에 있는 로컬 데이터를 읽으므로 속도가 빨라짐!      |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 백만 장이 넘는 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 중 누가 어느 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 자주 쓰는지 일일이 감시할 CPU 여유가 없다. 그래서 고안한 천재적인 방법이 <strong>"함정(<a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/">Trap</a>)"</strong>이다. [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)들을 슬쩍 '접근 불가'로 만들어 놓고, 누가 불만을 터뜨리는지([Page Fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)) 본다. 불만을 터뜨린 놈([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))이 1번 동네에 사는데 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 0번 동네에 있으면, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 그 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 1번 동네로 옮겨주는 식이다. 이 작업을 백그라운드에서 아주 천천히 조심스럽게 진행하여 시스템 전체의 부하를 주지 않으면서 서서히 [데이터 지역성](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/)(Locality)을 수렴시킨다.

- **📢 섹션 요약 비유**: 도서관 사서([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))가 책들을 일부러 손 안 닿는 높은 곳에 꽂아둡니다. 어떤 학생([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))이 까치발을 들고 책을 꺼내려 하면([Page fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)), 사서가 쏜살같이 달려와 "너 3층 열람실에서 공부하지? 이 책 3층에 옮겨줄게!"라고 맞춤형 이사를 해주는 것입니다.

---

## Ⅲ. 비교 및 연결

### 할당기(Allocator) 수준의 구조 비교

| 비교 항목 | 전통적 [UMA](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/379_uma/) ([SMP](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/195_real_time_scheduling/)) 할당 | [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/)-Aware 할당 ([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨) | [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/)-Aware 애플리케이션 (유저 레벨) |
|:---|:---|:---|:---|
| **개념** | 빈 공간 아무 데나 순서대로 줌 | [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 도는 CPU 근처에 줌 | 앱 코드가 직접 `numa_alloc_onnode` 호출 |
| **특징** | 구조가 매우 단순함 | **First-touch 로직으로 투명하게 작동** | 개발자가 명시적으로 노드 번호를 관리함 |
| **문제점** | 최신 2/4소켓 서버에서 30% [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 | 멀티스레드가 한 변수(글로벌) [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화 시 병목 | 소스 코드를 대대적으로 뜯어고쳐야 함 |

**First-touch 딜레마 (개발자의 실수)**: 개발자가 메인 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 하나로 100GB짜리 배열을 0으로 쭈욱 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화(memset)했다. First-touch 원칙에 의해 이 100GB는 모두 메인 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 돌던 Node 0에 몰빵된다. 그 후 연산을 위해 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 64개를 띄워 절반을 Node 1에 보냈더니, Node 1의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)들은 죽어라 Node 0의 메모리를 원격으로 읽느라 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 폭발한다. (이럴 때는 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화도 멀티스레드로 쪼개서 각자 로컬을 터치하게 짜야 한다.)

### 과목 융합 관점

- <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a> (OS) / 스케줄링</strong>: 리눅스의 CFS [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)는 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 토폴로지를 인식한다. 부하 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)을 위해 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 남는 코어로 튕겨낼 때([Load Balancing](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/196_hard_soft_real_time/)), 캐시 효율을 위해 같은 L3 캐시를 공유하는 코어 $\rightarrow$ 같은 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 노드의 코어 $\rightarrow$ 아예 다른 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 노드의 코어 순서로 점차 범위를 넓혀가며 '이사 페널티'를 최소화한다. (Sched Domains 아키텍처)
- <strong><a href="/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/">가상화</a> (Cloud)</strong>: [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)([KVM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/713_kvm_over_ip/))가 8코어/16GB 가상머신([VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))을 띄울 때, 8코어와 16GB를 Node 0과 Node 1에 반반씩 찢어서 주면 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 박살난다(vNUMA 미설정). 클라우드 아키텍처에서는 반드시 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 하나가 물리적 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 경계를 넘지 않도록 Pinning 해주는 것이 클라우드 설계의 기본이다.

- **📢 섹션 요약 비유**: 부서를 나눌 때 아무나 섞어놓지 않고, 같은 프로젝트를 하는 팀원([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))과 서류(메모리)를 반드시 같은 층([NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 노드)에 배치하는 오피스 공간 배치의 미학입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — SAP HANA / <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/">Redis</a> 등 인메모리(In-Memory) DB의 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 튜닝</strong>: 거대한 램을 사용하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스를 2소켓([NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 2개) 물리 서버에 올렸더니 응답 속도가 널뛰기를 하고 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 떨어짐.
   - **대응 (Interleave 적용)**: 거대 DB는 수많은 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 메모리 전체를 무작위로 휘젓고 다닌다. 만약 First-touch로 한 노드에 메모리가 쏠리면 해당 노드의 메모리 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)([Bandwidth](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)) 한계에 부딪힌다. 따라서 DB 시작 스크립트에 `numactl --interleave=all` 옵션을 주어, 메모리를 할당할 때 Node 0과 1에 강제로 반반씩 지퍼백처럼 섞어서(Interleave) 할당하게 한다. [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))은 5%쯤 늘어나지만 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 병목이 해소되어 전체 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))이 30% 이상 증가한다.

2. <strong>시나리오 — 리눅스의 원인 불명 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a> (<a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/425_oom_killer_score/">Out-of-Memory</a>) Killer 발동</strong>: 전체 램이 128GB(Node0 64GB, Node1 64GB)인 서버에서 `free` 명령어를 치면 50GB나 남아있는데도, 특정 애플리케이션이 실행되다 말고 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬을 당해서 죽어버림.
   - **원인 분석**: 애플리케이션이 `numactl --membind=0` (또는 기본 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)상 Node 0 몰빵) 상태로 돌아서 Node 0의 64GB를 다 써버렸다. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 `zone_reclaim_mode` [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)에 따라, "Node 0이 꽉 찼으니 Node 1의 남는 메모리를 빌려올까, 아니면 그냥 Node 0에 있는 프로세스를 죽여버릴까?" 사이에서 갈등하다가 후자([OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/))를 택한 것이다. ([NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) Imbalance 현상).
   - **대응 (기술사적 가이드)**: [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 파라미터 `vm.zone_reclaim_mode = 0`으로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하여, 로컬 노드 메모리가 부족하면 강제로 원격 노드 메모리를 끌어다 쓰게(Spill over) 허용해야 한다. [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 느려지지만 서버가 죽는 대참사는 막을 수 있다.

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 NUMA 아키텍처 메모리 튜닝 의사결정 플로우                |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [멀티 소켓(2개 이상) 서버에서 고성능 애플리케이션 구동]                    |
  |                |                                                  |
  |                v                                                  |
  |      애플리케이션이 엄청난 양의 메모리(100GB 이상)를 순차/랜덤하게 스캔하는가?|
  |      (예: In-memory DB, ElasticSearch, 빅데이터 분석)                 |
  |          +- 예 ------> [numactl --interleave=all 설정 권장]         |
  |          |            (AutoNUMA 끄기: 커널이 쓸데없이 페이지 옮기느라 |
  |          |             CPU 태우는 Thrashing 방지)                   |
  |          +- 아니오                                                |
  |                |                                                  |
  |                v                                                  |
  |      1개의 VM이나 프로세스가 1개 NUMA 노드 크기(예: 16코어, 64GB)에 쏙 들어가는가?|
  |          +- 예 ------> [numactl --cpunodebind=X --membind=X 강제 고정]|
  |          |            (100% 로컬 메모리 적중률 확보, 극강의 성능 달성)   |
  |          |                                                        |
  |          +- 아니오 ---> OS 기본값(First-touch + AutoNUMA) 유지      |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** "NUMA는 마법이 아니라 저주다"라는 말이 인프라 엔지니어들 사이에 있다. 잘 모르면 오히려 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 떨어진다. AutoNUMA는 완벽하지 않다. [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 이리저리 복사하느라 오히려 CPU 코어 하나를 100% 태우기도 한다([NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) Balancing Overhead). 그래서 고도의 엔터프라이즈 환경에서는 K8s 레벨에서 `Topology Manager`를 써서, 아예 처음 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 띄울 때부터 "너는 CPU도 Node 0번 것만 쓰고 램도 Node 0번, 랜카드([SR-IOV](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/497_sr_iov_pcie_mapping/))도 Node 0번에 꽂힌 것만 써!"라고 철저히 격리(Pinning)해 버리는 튜닝을 가장 선호한다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong>vNUMA (Virtual <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/">NUMA</a>) 노출</strong>: [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)에서 거대한 VM을 만들 때, 게스트 OS([VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 내부 리눅스)에게 "너의 물리적 환경은 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 2개짜리야"라고 가상 토폴로지를 똑같이 노출해 주었는가? (이걸 숨기면 게스트 OS는 자기가 UMA인 줄 알고 스케줄링을 엉망으로 짠다.)
- <strong>Transparent <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/">Huge Pages</a> (THP) 충돌</strong>: 2MB 단위의 대형 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 쓸 때 AutoNUMA가 동작하면, 2MB 통째로 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 이주시켜야 하므로 복사 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)(Migration [Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))이 극심해질 수 있다. THP와 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) Balancing의 동시 사용에 대한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 벤치마크가 필수다.

- **📢 섹션 요약 비유**: [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 튜닝은 기숙사 방 배정입니다. 아무 방에나 학생을 넣고 매일 짐을 옮겨주기(AutoNUMA)보다는, 애초에 체대생은 1층 헬스장 옆, 미대생은 2층 작업실 옆에 못 박아 두는 것(Pinning)이 가장 현명한 관리법입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 무시 (기본 [UMA](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/379_uma/) 동작) | [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/)-Aware 최적화 적용 | 개선 효과 |
|:---|:---|:---|:---|
| <strong>정량 (<a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">Latency</a>)</strong> | 메모리 원격 접근 빈발 (150ns) | 로컬 메모리 [적중률](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/264_hit_ratio/) 90% 이상 (80ns)| 메모리 접근 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 **최대 50% 감소** |
| <strong>정량 (DB <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>)</strong> | 쏠림으로 인한 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 병목 | Interleave로 메모리 채널 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) | 인메모리 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) **20~30% 증가** |
| **정성 (자원 안정성)**| 특정 노드 메모리 고갈로 서버 패닉 | 밸런싱 및 Spill-over 허용 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | Noisy Neighbor 차단 및 장애 유연성 획득 |

### 미래 전망
- <strong><a href="/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/">CXL</a>(<a href="/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/">Compute Express Link</a>) 기반 Memory Tiering</strong>: 다가오는 [CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 시대에는 로컬 램(DDR5)과 원격 램([CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 확장 램), 그리고 초원격 램([메모리 풀링](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/442_memory_pooling/))이라는 3단계 이상의 거대한 메모리 계층(Tier)이 등장한다. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 프레임워크는 단순히 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 간 이동을 넘어, "자주 쓰는 핫 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 로컬 DDR5로, 차가운 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 느린 [CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 램으로" 자동으로 밀고 당기는 오토 티어링(Auto-Tiering) 두뇌로 진화하고 있다.
- <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/">eBPF</a> 커스텀 마이그레이션</strong>: [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 천편일률적으로 정하는 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 마이그레이션 규칙 대신, eBPF를 이용해 애플리케이션 개발자가 직접 "이 메모리 풀은 내일 아침 9시에 Node 1로 복사해 줘"라고 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)에 동적 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 주입하는 기술이 연구되고 있다.

### 결론
[NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 인지형 메모리 할당기와 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 이동 프레임워크는, 무한히 늘어나는 CPU 코어 수의 물리적 한계(메모리 벽, [Memory Wall](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/433_memory_wall/))를 극복하기 위해 소프트웨어 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 내놓은 가장 치열한 타협안이다. 하드웨어의 불균형을 추상화로 덮으려던 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)의 시도를 포기하고, 하드웨어의 물리적 토폴로지를 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 가장 깊숙한 곳까지 노출시켜 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 있는 곳에 연산을 붙이는" 클라우드 네이티브의 기본 철학을 OS 단에서 실현한 마스터피스다.

- **📢 섹션 요약 비유**: 물건(메모리)을 가져오기 위해 공장(CPU)을 돌리던 시대가 끝나고, 공장 옆에 맞춤형 물류 창고를 통째로 옮겨 심어주는 초정밀 배급망이 완성되었습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 동적 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 서명 ([Module Signature Verification](/knowledge-base/studynote/02_operating_system/10_security/645_kernel_module_signature_verification/)) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 통제 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 리눅스 시스템 콜 테이블 ([sys_call_table](/knowledge-base/studynote/02_operating_system/10_security/646_syscall_table_hooking_expansion/)) 확장 및 보안 훅 추가 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 프로세스 체크포인트/리스토어 ([CRIU](/knowledge-base/studynote/02_operating_system/10_security/648_process_checkpoint_restore_criu/)) [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 마이그레이션 도구 구조 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [커널 메모리 컴팩션](/knowledge-base/studynote/02_operating_system/10_security/649_kernel_memory_compaction/) ([Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)) [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) 런타임 제거 백그라운드 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 구조 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[리눅스 시스템 콜 테이블 (sys_call_table) 확장 및 보안 훅 추가]
    |
    v
[NUMA 인지형 메모리 할당기 커널 페이지 이동 정책 프레임워크 설계 (NUMA Aware Allocator Page Migration)]
    |
    +---> [프로세스 체크포인트/리스토어 (CRIU) 컨테이너 마이그레이션 도구 구조]
    +---> [커널 메모리 컴팩션 (Compaction) 외부 단편화 런타임 제거 백그라운드 스레드 구조]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 커다란 사무실(컴퓨터)이 A구역과 B구역으로 나뉘어 있고, 각 구역마다 정수기(메모리)가 있어요.
2. A구역 직원이 B구역 정수기 물을 마시러 가면 시간이 너무 오래 걸리죠? 그래서 똑똑한 사장님([운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))은 A구역 직원이 입사하면 무조건 A구역 정수기 컵을 배정해 줘요.
3. 만약 그 직원이 나중에 B구역으로 자리를 옮기면, 사장님이 밤에 몰래 그 직원의 개인 컵을 B구역 정수기 옆으로 예쁘게 옮겨다 놓는답니다([페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 이동)!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 647 / 800

<- **이전**: [646. 리눅스 시스템 콜 테이블 (sys_call_table) 확장 및 보안 훅 추가](/knowledge-base/studynote/02_operating_system/10_security/646_syscall_table_hooking_expansion/)
**다음**: [648. 프로세스 체크포인트/리스토어 (CRIU) 컨테이너 마이그레이션 도구 구조](/knowledge-base/studynote/02_operating_system/10_security/648_process_checkpoint_restore_criu/) ->

---
