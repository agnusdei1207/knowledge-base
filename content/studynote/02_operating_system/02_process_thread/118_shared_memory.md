+++
title = "118. 공유 메모리 (Shared Memory) 방식 - 빠름, 동기화 문제 발생"
date = 2026-05-08

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 공유 메모리 (Shared Memory)는 두 개 이상의 프로세스가 동일한 물리 메모리 영역을 각자의 [가상 주소 공간](/knowledge-base/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/)에 매핑하여, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 개입 없이 직접 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽고 쓰는 가장 빠른 [IPC](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/) (Inter-[Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/) Communication) 방식이다.
> 2. **가치**: [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)(`shmget()`, `shmat()`) 이후에는 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 교환이 유저 모드에서만 이루어지므로 시스템 콜과 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드 전환이 발생하지 않아, [메시지 전달](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/) 방식에 비해 대량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송 시 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 100~1000배 더 짧다.
> 3. **융합**: 현대 시스템에서 POSIX 공유 메모리(`shm_open()` + `mmap()`), 리눅스의 `memfd_create()`, 그리고 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 컴퓨팅의 [CUDA](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/) 공유 메모리, [RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) 기반 원격 공유 메모리까지, [직접 메모리 접근](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/450_dma_direct_memory_access/) 원리는 단일 머신에서 클러스터 규모까지 모든 고성능 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 교환의 근간이 된다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 공유 메모리 (Shared Memory)는 운영체제가 프로세스 간에 공유할 수 있는 물리 메모리 영역을 할당하고, 각 프로세스의 [가상 주소 공간](/knowledge-base/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/)([Virtual Address Space](/knowledge-base/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/)) 일부가 이 공유 영역을 가리키도록 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) ([Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/))을 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하는 [IPC](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/) 메커니즘이다. 매핑 완료 후에는 프로세스가 일반 메모리에 접근하는 것과 완전히 동일한 방식(포인터 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 교환할 수 있다.
- **필요성**: [메시지 전달](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/) 방식([파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/), 메시지 큐 등)은 매 통신마다 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드 전환과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복사가 발생하므로, 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(비디오 프레임, 과학 계산 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 등)를 고빈도로 교환하는 환경에서는 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 치명적이다. 공유 메모리는 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 한 번의 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)만으로 이후에는 어떤 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 오버헤드도 없이 직접 메모리에 접근하므로, 고성능 컴퓨팅([HPC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/548_automotive_hpc/)), 고빈도 거래(HFT), 멀티미디어 처리 등 대량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 교환이 필수적인 분야에서 대안이 없는 선택이다.

- **등장 배경**: [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 유닉스에서 IPC는 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)와 시그널만 지원되어 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 교환의 효율이 매우 낮았다. AT&T Bell Labs의 System V에서 `shmget()`, `shmat()`, `shmdt()`, `shmctl()` API가 도입되면서 처음으로 공유 메모리 IPC가 표준화되었다. 이후 IEEE POSIX 표준에서 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 기반 인터페이스(`shm_open()` + `mmap()`)로 재설계되어, 기존 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터([File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) Descriptor) 기반 I/O와의 통합성이 크게 향상되었다.

공유 메모리의 가상 주소-물리 주소 매핑 구조를 시각화하면, 왜 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 개입 없이 직접 접근이 가능한지 이해할 수 있다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│          공유 메모리의 가상-물리 주소 매핑 구조                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [프로세스 A의 가상 주소 공간]     [프로세스 B의 가상 주소 공간]    │
│                                                                     │
│  0x0000 ┌───────────────┐      0x0000 ┌───────────────┐             │
│         │   Code        │             │   Code        │             │
│         │   Data        │             │   Data        │             │
│         │   Heap        │             │   Heap        │             │
│  0x5000 │ ┌───────────┐ │      0x7000 │ ┌───────────┐ │             │
│         │ │ 공유 영역  │ │             │ │ 공유 영역  │ │           │
│         │ │ (매핑됨)  │ │             │ │ (매핑됨)  │ │             │
│         │ └─────┬─────┘ │             │ └─────┬─────┘ │             │
│  0x6000 │   Stack      │      0x8000 │   Stack      │               │
│         └──────┼────────┘             └──────┼────────┘             │
│                │                             │                      │
│  ──────────────┼───── Page Table ────────────┼──────────            │
│                │                             │                      │
│                ▼                             ▼                      │
│         ┌──────────────────────────────────────┐                    │
│         │     물리 메모리 (Physical RAM)         │                  │
│         │                                      │                    │
│         │   ┌──────────────────────────────┐   │                    │
│         │   │     공유 메모리 영역           │   │                  │
│         │   │  (두 프로세스가 동일 페이지    │   │                  │
│         │   │   공유함)                     │   │                   │
│         │   └──────────────────────────────┘   │                    │
│         └──────────────────────────────────────┘                    │
│                                                                     │
│  핵심: Page Table이 두 가상 주소를 동일 물리 주소로 매핑함          │
│       → 프로세스 A의 쓰기가 프로세스 B에 즉시 반영됨                │
│       → CPU 명령(LOAD/STORE)만으로 통신 완료 (커널 개입 없음!)      │
└─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 구조도는 공유 메모리가 "왜 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 개입 없이 동작하는가"를 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)([Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)) 관점에서 명확히 보여준다. 운영체제는 `shmget()`으로 물리 메모리에 공유 영역을 할당하고, `shmat()`를 통해 각 프로세스의 [가상 주소 공간](/knowledge-base/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/) 내에 이 물리 메모리를 매핑한다. 이 매핑은 프로세스 A의 0x5000 번지와 프로세스 B의 0x7000 번지가 동일한 물리 메모리 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 가리키도록 각자의 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 엔트리([Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) Entry, PTE)를 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하는 방식으로 이루어진다. 매핑 완료 후에는 CPU가 일반적인 LOAD/STORE 명령으로 메모리에 접근하므로, 시스템 콜이나 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드 전환 없이 프로세스 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 교환이 즉각적으로 이루어진다. 이것이 공유 메모리가 가장 빠른 [IPC](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/) 방식인 근본 이유다.

- **📢 섹션 요약 비유**: 두 사람이 각자의 지도(가상 주소)에서 서로 다른 장소를 적어도, 실제로 가리키는 땅(물리 메모리)이 같으면 한 사람이 집을 지으면 다른 사람도 즉시 그 집을 볼 수 있는 것과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### System V 공유 메모리 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)

| [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 함수 | 역할 | 내부 동작 | 비유 |
|:---|:---|:---|:---|
| **shmget()** | 공유 메모리 세그먼트 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 또는 기존 것 획득 | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 물리 메모리 할당, shmid_ds 구조체 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 정수 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) 반환 | 공유 창고 대여 계약 |
| **shmat()** | 프로세스의 [가상 주소 공간](/knowledge-base/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/)에 공유 메모리 연결 | [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 엔트리 수정, 가상 주소 포인터 반환 | 창고로 이어지는 문 개방 |
| **shmdt()** | 프로세스의 [가상 주소 공간](/knowledge-base/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/)에서 공유 메모리 분리 | [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 엔트리 무효화 (물리 메모리는 유지) | 창고로 이어지는 문 폐쇄 |
| **shmctl()** | 공유 메모리 세그먼트 제어(삭제, 권한 변경 등) | `IPC_RMID`로 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에서 세그먼트 삭제 | 창고 철거 또는 권한 변경 |

---

### 공유 메모리 기반 생산자-소비자 문제

공유 메모리를 활용한 가장 전형적 패턴은 생산자-소비자 (Producer-Consumer) 문제다. 다음은 공유 메모리 버퍼를 사용한 생산자-소비자 구조와 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 요구사항이다.

```text
┌────────────────────────────────────────────────────────────────────┐
│     공유 메모리 기반 생산자-소비자 (Producer-Consumer) 구조        │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌────────────┐      ┌──────────────────────────────────┐          │
│  │  생산자      │      │       공유 메모리 영역              │     │
│  │ (Producer)  │      │                                  │         │
│  │             │      │  ┌───────────────────────────┐   │         │
│  │  data를 생성 │      │  │  공유 버퍼 (Buffer)       │   │        │
│  │             │─────▶│  │  ┌─────┬─────┬─────┐    │   │           │
│  │  buffer에   │      │  │  │ 10  │ 20  │ 30  │    │   │           │
│  │  쓰기 (write)│      │  │  └─────┴─────┴─────┘    │   │          │
│  └────────────┘      │  │  in=3  out=0  count=3   │   │            │
│                       │  │                           │   │         │
│  ┌────────────┐      │  │  ┌─────────────────────┐ │   │           │
│  │  소비자      │      │  │  │ mutex (상호배제)     │ │   │        │
│  │ (Consumer)  │      │  │  └─────────────────────┘ │   │          │
│  │             │─────▶│  │  ┌─────────────────────┐ │   │          │
│  │  buffer에서  │      │  │  │ empty(빈칸=버퍼용량) │ │   │        │
│  │  읽기 (read) │      │  │  │ full(가득참=0)      │ │   │         │
│  └────────────┘      │  │  └─────────────────────┘ │   │           │
│                       │  └───────────────────────────┘   │         │
│                       └──────────────────────────────────┘         │
│                                                                    │
│  동기화 규칙 (필수!):                                              │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │ 1. mutex: 버퍼에 한 프로세스만 접근 가능 (상호배제)        │    │
│  │ 2. empty: 버퍼가 가득 찼을 때 생산자 대기                  │    │
│  │ 3. full:  버퍼가 비었을 때 소비자 대기                     │    │
│  │                                                         │       │
│  │  생산자: wait(empty) → wait(mutex) → write →              │     │
│  │          signal(mutex) → signal(full)                     │     │
│  │                                                         │       │
│  │  소비자: wait(full) → wait(mutex) → read →                │     │
│  │          signal(mutex) → signal(empty)                    │     │
│  └─────────────────────────────────────────────────────────┘       │
└────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 구조도는 공유 메모리를 활용한 생산자-소비자 패턴에서 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)가 왜 필수적인지를 명확히 보여준다. 공유 버퍼는 단일 물리 메모리 영역이므로, 생산자가 버퍼 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)(in)를 갱신하는 동시에 소비자가 같은 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 읽으면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치가 발생한다. 이를 방지하기 위해 [mutex](/knowledge-base/studynote/02_operating_system/04_synchronization/223_mutex/)(뮤텍스)로 [상호 배제](/knowledge-base/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/)([Mutual Exclusion](/knowledge-base/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/))를 보장해야 한다. 또한 버퍼가 가득 찼을 때(empty=0) 생산자가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 덮어쓰는 것을 막기 위해 empty 세마포어로 대기시키고, 버퍼가 비었을 때(full=0) 소비자가 의미 없는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽는 것을 막기 위해 full 세마포어로 대기시킨다. 이 세 가지 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 변수([mutex](/knowledge-base/studynote/02_operating_system/04_synchronization/223_mutex/), empty, full)가 공유 메모리 자체에 함께 저장되어, 모든 프로세스가 동일한 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 상태를 공유한다.

### POSIX 공유 메모리 (`shm_open()` + `mmap()`)

POSIX 표준은 System V API의 정수 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) 대신 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터 기반의 더 통합적인 인터페이스를 제공한다. `shm_open()`이 `/dev/shm/` 아래에 이름 있는 공유 메모리 객체를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고, `mmap()`이 이를 프로세스의 [가상 주소 공간](/knowledge-base/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/)에 매핑한다.

- **📢 섹션 요약 비유**: 공유 메모리는 공용 화이트보드에 여러 사람이 동시에 글씨를 쓰는 것과 같아서, 신호등([동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)) 없이 쓰면 글씨가 뒤섞이지만 신호등만 잘 지키면 가장 빠르게 의사소통할 수 있습니다.

---

## Ⅲ. 비교 및 연결

### 공유 메모리 vs 기타 [IPC](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/) 방식 심층 비교

| 비교 항목 | 공유 메모리 | [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/) ([Pipe](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)) | 메시지 큐 (Message [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/)) | [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) ([Socket](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)) |
|:---|:---|:---|:---|:---|
| **통신 속도** | 매우 빠름 (직접 접근) | 중간 ([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 버퍼 경유) | 느림 ([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 구조체 복사) | 가장 느림 (네트워크 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 경유) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a></strong> | 사용자가 직접 구현 필수 | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 자동 관리 | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 자동 관리 | [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이 자동 관리 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 크기</strong> | [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 단위(4KB~수GB) | [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 스트림(무제한) | 메시지 단위(제한 있음) | [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 스트림/[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)그램 |
| **대상 범위** | 동일 머신 | 부모-자식 프로세스 | 동일 머신 | 동일/원격 머신 |

공유 메모리의 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 문제를 다이어그램으로 시각화하면, 경합 조건 ([Race Condition](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/))이 어떻게 발생하는지 구체적으로 이해할 수 있다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│     공유 메모리 동기화 없이 두 프로세스가 동시 쓸 때의 문제         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  공유 메모리: counter = 0 (초기값)                                  │
│                                                                     │
│  시간 ──────────────────────────────────────────▶                   │
│                                                                     │
│  프로세스 A:  counter값 읽기(0) ─── counter+1 계산(1) ─── 쓰기(1)   │
│                    │                        │                       │
│  프로세스 B:        └── counter값 읽기(0) ─── counter+1 계산 ─┤     │
│                                                │                    │
│                                                ▼                    │
│                                           쓰기(1) ← 기대값 2!       │
│                                                                     │
│  결과: counter = 1 (기대값은 2였음!)                                │
│       → 경합 조건 (Race Condition) 발생!                            │
│                                                                     │
│  해결:                                                              │
│  ┌────────────────────────────────────────────────────────┐         │
│  │  프로세스 A: lock(mutex) → 읽기(0) → 계산(1) → 쓰기(1)  │        │
│  │                        → unlock(mutex)                 │         │
│  │                                                        │         │
│  │  프로세스 B:               lock(mutex) 대기...          │        │
│  │                           (A의 unlock 후)               │        │
│  │                           → 읽기(1) → 계산(2) → 쓰기(2)│         │
│  │                           → unlock(mutex)               │        │
│  │                                                        │         │
│  │  결과: counter = 2 (정상!)                               │       │
│  └────────────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 타임라인 다이어그램은 공유 메모리에서 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)가 없을 때 발생하는 경합 조건([Race Condition](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/))의 전형적인 패턴을 보여준다. 두 프로세스가 동시에 `counter`의 값을 읽었을 때, 두 프로세스 모두 0을 읽고 각자 독립적으로 1을 더해 1을 쓴다. 기대값은 2이지만 실제 결과는 1이 된다. 이것이 [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/)([Atomicity](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/))이 보장되지 않는 읽기-수정-[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(Read-Modify-Write) 연산의 근본적 문제다. 뮤텍스([Mutex](/knowledge-base/studynote/02_operating_system/04_synchronization/223_mutex/))를 사용하면 한 프로세스가 [임계 구역](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/)([Critical Section](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/))에 진입하는 동안 다른 프로세스가 대기하도록 강제하여, [counter](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) 값이 항상 올바르게 갱신되도록 보장한다. 공유 메모리를 사용하는 모든 시스템에서 이러한 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 보장이 필수적이다.

### 과목 융합 관점
- <strong>컴퓨터 아키텍처 (<a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/">CA</a>)</strong>: 멀티코어 프로세서에서 각 코어가 공유하는 L3 캐시 (Last Level Cache)는 하드웨어 수준의 공유 메모리다. [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)(MESI 등)이 소프트웨어 수준의 뮤텍스와 동일한 역할을 하여, 여러 코어가 동일 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 일관되게 접근하도록 보장한다.
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> (DB)</strong>: 공유 메모리는 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)의 공유 버퍼 풀(Shared Buffer Pool) 구현에 사용된다. 여러 백엔드 프로세스가 디스크에서 읽은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 공유 버퍼 풀에 저장하고 접근하므로, 디스크 I/O를 최소화할 수 있다. PostgreSQL의 `shared_buffers`가 대표적 사례다.

- **📢 섹션 요약 비유**: 공유 메모리는 고속도로(빠른 직접 접근)와 같아서 신호등([동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/))이 있으면 모든 차가 안전하게 통과하지만, 신호등이 고장 나면 교차로에서 충돌 사고(경합 조건)가 발생합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 -- 대용량 비디오 프레임 실시간 처리**: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 실시간 영상 분석 시스템에서 카메라 캡처 프로세스가 4K 해상도(1프레임당 약 8MB)를 초당 60프레임 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 추론 프로세스가 이를 분석해야 하는 상황.
   - **판단**: [메시지 전달](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/)([파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)/[소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/))로 8MB * 60 = 480MB/s를 전송하면 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 버퍼 복사 비용으로 CPU 사용률이 30% 이상 소모되고 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 수백 마이크로초로 증가한다. 반면 공유 메모리에 원형 버퍼(Ring Buffer)를 구성하면, 캡처 프로세스가 프레임을 버퍼에 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)만 하고 추론 프로세스가 포인터만 읽어오면 되므로 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 개입이 전혀 필요 없다. [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)는 [CAS](/knowledge-base/studynote/02_operating_system/11_exam_summary/768_cas_compare_and_swap_lock_free/)([Compare-And-Swap](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/415_compare_and_swap/)) 기반의 락 프리([Lock-free](/knowledge-base/studynote/02_operating_system/04_synchronization/256_lock_free_data_structures/)) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 관리로 구현하여 뮤텍스 오버헤드마저 제거해야 한다.

2. **시나리오 -- 공유 메모리 누수로 인한 시스템 메모리 고갈**: 프로세스가 `shmget()`으로 공유 메모리를 할당한 뒤 비정상 종료(Crash)하여 `shmdt()`와 `shmctl(IPC_RMID)`이 호출되지 않아, 공유 메모리 세그먼트가 시스템에 영구적으로 남아 메모리가 점진적으로 고갈되는 상황.
   - **판단**: System V 공유 메모리의 전형적인 자원 누수 문제다. 해결책으로 세 가지를 병행해야 한다. 첫째, 프로세스에 시그널 핸들러(SIGINT, SIGTERM)를 등록하여 비정상 종료 시 `shmctl(IPC_RMID)`을 호출하도록 한다. 둘째, `ipcs -m` 명령으로 정기적으로 고아(orphan) 공유 메모리 세그먼트를 모니터링하고 `ipcrm -m`으로 정리하는 운영 스크립트를 구성한다. 셋째, POSIX 공유 메모리(`shm_open()`)로 전환하면 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 카운트([Reference](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) Count)가 0이 될 때 자동으로 해제되므로 누수 위험이 크게 줄어든다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **기술적**: 공유 메모리의 크기를 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 크기의 배수로 맞추었는가? [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)에 사용하는 뮤텍스/세마포어가 공유 메모리 내부에 배치되어 모든 프로세스가 동일한 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 객체를 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하는가? 캐시 라인 (Cache Line, 64바이트) 경계에 따라 false sharing을 피하도록 자료구조를 [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)([Padding](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/))했는가?
- **운영·보안적**: 공유 메모리 세그먼트의 접근 권한(0600 등)이 최소 권한 원칙으로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)되어 있어, 의도치 않은 프로세스의 접근이 차단되는가? `ipcrm` 정리 자동화 스크립트가 운영 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)에 포함되어 있는가?

- **📢 섹션 요약 비약**: 공유 메모리는 성능이 뛰어나지만 관리 책임이 사용자에게 있으므로, 사용 후 반드시 정리(해제)하고, 동시 접근 시 반드시 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)(뮤텍스)하는 두 가지 규칙을 절대 잊지 말아야 합니다.

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [메시지 전달](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/) ([파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)/[소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)) | 공유 메모리 (Shared Memory) | 개선 효과 |
|:---|:---|:---|:---|
| <strong>정량 (1MB <a href="/knowledge-base/studynote/03_network/01_data_communication/017_전송_지연/">전송 지연</a>)</strong> | 약 50~200us ([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 복사 2회) | 약 0.1~1us (직접 접근) | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) **100~1000배 단축** |
| **정량 (CPU 사용률)** | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드 전환으로 높음 | 유저 모드에서만 동작 | CPU 오버헤드 **70% 이상 감소** |
| <strong>정성 (<a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">대역폭</a>)</strong> | 시스템 콜당 수 KB~수 MB | 물리 메모리 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)(수십 GB/s) 극대 활용 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) **수십배 증가** |

### 미래 전망
- <strong><a href="/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/">CXL</a> (<a href="/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/">Compute Express Link</a>) 기반 원격 공유 메모리</strong>: [CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 3.0 표준은 [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) 버스를 통해 타 장치의 메모리를 로컬 메모리처럼 직접 접근할 수 있는 코히어런트(coherent) 공유 메모리 인터페이스를 제공한다. 이는 단일 머신의 공유 메모리 개념을 서버 클러스터 규모로 확장하여, [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 아키텍처의 메모리 접근 비균일성 문제를 해결하는 차세대 기술이다.
- <strong><a href="/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/">GPU</a> 공유 메모리와의 통합</strong>: NVIDIA CUDA의 공유 메모리(Shared Memory)는 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 블록 내 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공유를 위한 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 온칩 메모리로, CPU 프로세스 간 공유 메모리와 동일한 설계 원리를 공유한다. 통합 메모리(Unified Memory) 기술이 발전하면서 CPU-[GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 간의 투명한 공유 메모리 접근이 현실화되고 있다.

### 참고 표준
- **POSIX.1 (IEEE 1003.1)**: `shm_open()`, `shm_unlink()`, `ftruncate()`, `mmap()`, `munmap()` POSIX 공유 메모리 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 표준.
- <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/132_system_v_ipc/">System V IPC</a></strong>: `shmget()`, `shmat()`, `shmdt()`, `shmctl()` 레거시 공유 메모리 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/).
- <strong>Linux <code>memfd_create()</code> (3.17~)</strong>: 익명 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 기반 공유 메모리로, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 경로 없이 `mmap()`과 결합하여 사용.

- **📢 섹션 요약 비유**: 공유 메모리 기술은 처음에는 한 컴퓨터 안에서만 쓰였지만, 이제는 CXL이라는 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 도로를 통해 여러 서버를 하나의 거대한 공용 창고처럼 만드는 수준까지 진화했습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [협력적 프로세스](/knowledge-base/studynote/02_operating_system/02_process_thread/116_cooperating_independent_process/) ([Cooperating Process](/knowledge-base/studynote/02_operating_system/02_process_thread/116_cooperating_independent_process/)) vs 독립적 프로세스 (Independent [Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [프로세스 간 통신](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/) ([IPC](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/), Inter-[Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/) Communication) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [메시지 전달](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/) ([Message Passing](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/)) 방식 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [직접 통신](/knowledge-base/studynote/02_operating_system/02_process_thread/120_direct_communication/) ([Direct Communication](/knowledge-base/studynote/02_operating_system/02_process_thread/120_direct_communication/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[프로세스 간 통신 (IPC, Inter-Process Communication)]
    │
    ▼
[공유 메모리 (Shared Memory) 방식]
    │
    ├──▶ [메시지 전달 (Message Passing) 방식]
    └──▶ [직접 통신 (Direct Communication)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 공유 메모리는 두 집 사이에 만든 "공용 놀이터"와 같아서, 한 친구가 모래성을 만들면 다른 친구도 즉시 볼 수 있어서 연락이 엄청 빨라요!
2. 하지만 두 친구가 동시에 같은 모래성을 만지려 하면 무너질 수 있어서, 번갈아 가며 만지도록 순서표(뮤텍스)를 만들어야 안전해요.
3. 이 공용 놀이터는 컴퓨터가 비디오나 큰 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 처리할 때 아주 빠르게 정보를 나누어 주는 데 사용되며, 사용 후에는 반드시 치워야(메모리 해제) 다른 프로그램들을 위해 놀이터를 비워줄 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 118 / 800

← **이전**: [117. 프로세스 간 통신 (IPC, Inter-Process Communication)](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/)
**다음**: [119. 메시지 전달 (Message Passing) 방식 - 안전, 커널 개입(시스템 콜) 오버헤드](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/) →

---
