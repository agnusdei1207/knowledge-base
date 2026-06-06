---
title: "IPC Performance Overhead"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/)(Inter-Process Communication)는 독립된 메모리 공간을 가진 프로세스들이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받기 위한 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 레벨의 통신 규약이다. 프로세스 간의 완벽한 격리([Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/))를 허무는 행위이므로 필연적으로 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 오버헤드가 발생한다.
> 2. **오버헤드의 근원**: [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 갉아먹는 3대 주범은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 송신자 $\rightarrow$ [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) $\rightarrow$ 수신자로 2번 복사하는 **메모리 카피(Memory Copy)**, 유저 모드와 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드를 오가는 <strong><a href="/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/">문맥 교환</a>(<a href="/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/">Context Switch</a>)</strong>, 그리고 다수의 프로세스가 자원을 다툴 때 발생하는 <strong><a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a> 락(<a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">Synchronization</a> <a href="/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a>)</strong>이다.
> 3. **최적화**: [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)나 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 같은 전통적인 메시지 패싱([Message Passing](/studynote/02_operating_system/02_process_thread/119_message_passing/))은 사용하기 쉽지만 복사 오버헤드가 크고, [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/)([Shared Memory](/studynote/02_operating_system/02_process_thread/118_shared_memory/))는 복사가 0회([Zero-copy](/studynote/02_operating_system/09_file_system/566_mmap_zero_copy_sendfile/))로 가장 빠르지만 개발자가 직접 락([Mutex](/studynote/02_operating_system/04_synchronization/223_mutex/))을 관리해야 하는 치명적인 트레이드오프를 갖는다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong><a href="/studynote/02_operating_system/02_process_thread/117_ipc/">IPC</a> (Inter-Process Communication)</strong>: [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 제공하는 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)([Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/)), 메시지 큐(Message [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/)), [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/)([Shared Memory](/studynote/02_operating_system/02_process_thread/118_shared_memory/)), [소켓](/studynote/02_operating_system/02_process_thread/125_socket/)([Socket](/studynote/02_operating_system/02_process_thread/125_socket/)) 등의 프로세스 간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통신 메커니즘.
  - **오버헤드 (Overhead)**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통신이라는 목적을 달성하기 위해, 부가적으로 소모되는 시간(CPU 연산)이나 메모리 비용.

- **필요성 (격리의 딜레마)**:
  - 프로세스는 본래 "남의 메모리를 절대 볼 수 없도록" 철저히 고립되어 있다.
  - 하지만 크롬 브라우저의 '렌더링 프로세스'와 '네트워크 프로세스'가 분리되어 있다면, 이 둘은 반드시 이미지를 주고받아야 한다.
  - **딜레마**: 안전하게 주자니 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 거치느라 너무 느리고(메시지 패싱), 빠르게 주자니 벽을 허물어야 해서 충돌(레이스 컨디션)이 발생한다.
  - **해결책**: 용도와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 크기에 맞춰 다양한 [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) 기법이 탄생했으며, 아키텍트는 각 기법의 오버헤드 특성을 정확히 파악하고 적재적소에 골라 써야 한다.

  - 서로 다른 성에 사는 성주(프로세스)들이 물건을 교환한다.
  - **메시지 패싱 (오버헤드 큼)**: 성주 A가 국왕([커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))의 택배 기사에게 물건을 주면, 기사가 성주 B에게 가져다준다. 안전하지만 시간이 두 배로 걸린다.
  - <strong><a href="/studynote/02_operating_system/02_process_thread/118_shared_memory/">공유 메모리</a> (오버헤드 작음)</strong>: 두 성 사이에 다리(공유 공간)를 놓고 물건을 그냥 밀어놓는다. 가장 빠르지만, 두 성주가 동시에 물건을 집으려다 다리 위에서 싸움(충돌)이 날 수 있어 신호등(락)을 직접 설치해야 한다.

- **발전 과정**:
  1. <strong><a href="/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a> (<a href="/studynote/02_operating_system/02_process_thread/123_pipe/">Pipe</a>)</strong>: UNIX [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/). [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/), 부모-자식 간 통신만 가능.
  2. <strong>System V / <a href="/studynote/02_operating_system/02_process_thread/133_posix_ipc/">POSIX IPC</a></strong>: 메시지 큐, [세마포어](/studynote/02_operating_system/04_synchronization/224_semaphore/), [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/) 표준화. 양방향 및 무관한 [프로세스 간 통신](/studynote/02_operating_system/02_process_thread/117_ipc/) 가능.
  3. <strong><a href="/studynote/02_operating_system/02_process_thread/126_rpc/">RPC</a> / <a href="/studynote/02_operating_system/02_process_thread/125_socket/">Socket</a></strong>: 네트워크를 넘어 다른 컴퓨터의 프로세스와 통신. (오버헤드 최강)
  4. <strong>최신 <a href="/studynote/02_operating_system/02_process_thread/117_ipc/">IPC</a> (<a href="/studynote/02_operating_system/10_security/662_android_binder_ipc_thread_pool/">Binder</a>, <a href="/studynote/02_operating_system/10_security/615_ebpf/">eBPF</a>)</strong>: 메모리 복사를 1회로 줄이거나([Binder](/studynote/02_operating_system/10_security/662_android_binder_ipc_thread_pool/)), [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 큐를 우회하는([io_uring](/studynote/02_operating_system/08_storage_and_io_systems/464_io_uring/)) 고성능 IPC의 등장.

- **📢 섹션 요약 비유**: IPC는 두 이웃 간에 택배를 보내는 방식입니다. 택배 회사를 거치면(메시지 패싱) 편하지만 배송비가 들고, 담벼락을 허물고([공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/)) 직접 손으로 넘겨주면 배송비는 0원이지만 사생활 침해를 막을 자물쇠([동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/))가 필요합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 메시지 패싱([Message Passing](/studynote/02_operating_system/02_process_thread/119_message_passing/)) 아키텍처와 오버헤드

[파이프](/studynote/02_operating_system/02_process_thread/123_pipe/), 메시지 큐, [소켓](/studynote/02_operating_system/02_process_thread/125_socket/)이 이 방식을 사용한다. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 통과하는 경로를 추적해 본다.

```text
  +-------------------------------------------------------------------+
  |                 메시지 패싱 (Pipe/Socket) 동작 및 오버헤드              |
  +-------------------------------------------------------------------+
  |                                                                   |
  |  [User Space]       프로세스 A (송신자)          프로세스 B (수신자)     |
  |                         | 1. write()               ^ 4. read()    |
  |  =======================v==========================|==============|
  |  [Kernel Space]         | [1차 Memory Copy]        |              |
  |                         v                          | [2차 Memory Copy]
  |                  [ 커널 내부 버퍼 (Mailbox) ]------+              |
  |                                                                   |
  |  ★ 오버헤드 분석:                                                   |
  |   1. 시스템 콜 오버헤드: write()와 read() 호출 시 2번의 [Context Switch] 발생.|
  |   2. 복사 오버헤드: 유저 $\rightarrow$ 커널, 커널 $\rightarrow$ 유저로 [2번의 메모리 카피] 발생. |
  |   3. 대기 오버헤드: 버퍼가 꽉 차거나 비어있으면 프로세스가 블로킹(Sleep) 됨.  |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** "10MB짜리 사진을 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)로 보낸다"고 가정하자. 10MB [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리로 복사되고, 다시 수신자의 유저 메모리로 복사된다. 총 20MB의 메모리 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)이 낭비된다. 만약 초당 1만 장의 사진을 처리하는 [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인이라면 이 **2-Copy 오버헤드** 때문에 CPU가 100%를 치게 된다.

---

### [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/)([Shared Memory](/studynote/02_operating_system/02_process_thread/118_shared_memory/)) 아키텍처와 오버헤드

POSIX `shm_open()`과 `mmap()`을 활용한 가장 빠른 [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) 방식이다.

```text
  +-------------------------------------------------------------------+
  |                 공유 메모리 (Shared Memory) 동작 및 오버헤드             |
  +-------------------------------------------------------------------+
  |                                                                   |
  |  [User Space]       프로세스 A (송신자)          프로세스 B (수신자)     |
  |                         |                          ^              |
  |                         | (단순 포인터 쓰기/읽기, 시스템 콜 없음!)        |
  |                         v                          |              |
  |  ============== [ 공유 메모리 영역 (Shared Page) ] ================|
  |                                                                   |
  |  [Kernel Space]                                                   |
  |   - 커널은 처음에 메모리를 매핑(mmap)해 줄 때만 개입하고, 이후엔 빠짐.      |
  |                                                                   |
  |  ★ 오버헤드 분석:                                                   |
  |   1. 통신 오버헤드: **[Zero-Copy], 커널 개입 없음. 성능 최강.**          |
  |   2. 동기화 오버헤드: A가 쓰고 있는데 B가 읽으면 데이터가 깨짐 (Race Condition).|
  |      반드시 [세마포어/뮤텍스]를 사용해야 하므로 여기서 [Lock 오버헤드]가 발생!|
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/) 자체는 복사가 0회([Zero-copy](/studynote/02_operating_system/09_file_system/566_mmap_zero_copy_sendfile/))이므로 빛의 속도다. 하지만 치명적인 약점이 있다. 송신자가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다 쓰지도 않았는데 수신자가 읽어가는 것을 막기 위해 개발자가 직접 락([Mutex](/studynote/02_operating_system/04_synchronization/223_mutex/))을 걸어야 한다. 이 락을 잡고 푸는 과정 자체가 결국 시스템 콜과 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 스위치를 유발하므로, <strong>"작은 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 엄청나게 자주 보낼 때는 락 오버헤드 때문에 오히려 <a href="/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a>보다 <a href="/studynote/02_operating_system/02_process_thread/118_shared_memory/">공유 메모리</a>가 더 느려질 수 있다"</strong>는 것이 시스템 아키텍트들의 숨겨진 비밀이다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) 기법별 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 오버헤드 비교표

| [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) 종류 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송 단위 | 복사(Copy) 횟수 | [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 처리 | 주요 오버헤드 원인 |
|:---|:---|:---:|:---|:---|
| <strong><a href="/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a> (<a href="/studynote/02_operating_system/02_process_thread/123_pipe/">Pipe</a> / <a href="/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/">FIFO</a>)</strong>| [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 스트림 | **2회** | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 알아서 블로킹 해줌 | 메모리 카피, 잦은 시스템 콜 |
| **메시지 큐 (MQ)** | 고정 구조체 단위 | **2회** | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 알아서 블로킹 해줌 | 메모리 카피, 큐 크기 제한 관리 |
| <strong><a href="/studynote/02_operating_system/02_process_thread/118_shared_memory/">공유 메모리</a> (SHM)</strong> | 구조체 / [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) | <strong>0회 (<a href="/studynote/02_operating_system/09_file_system/566_mmap_zero_copy_sendfile/">Zero-copy</a>)</strong>| <strong>개발자가 락(<a href="/studynote/02_operating_system/04_synchronization/223_mutex/">Mutex</a>) 100% 직접 구현</strong> | <strong><a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a> 락(<a href="/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a>) 경합 오버헤드</strong> |
| <strong><a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> <a href="/studynote/02_operating_system/02_process_thread/125_socket/">소켓</a> (UDS)</strong> | [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 스트림 | **2회** | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 알아서 블로킹 해줌 | 패킷 헤더/[라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 파싱(네트워크 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)) |

<strong><a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> <a href="/studynote/02_operating_system/02_process_thread/125_socket/">소켓</a>(Unix <a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">Domain</a> <a href="/studynote/02_operating_system/02_process_thread/125_socket/">Socket</a>)</strong>: 네트워크를 타는 일반 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/)([TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/IP)보다는 훨씬 빠르다. [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 내에서 네트워크 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)([TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 계층)을 통과하지 않고 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 계층에서 버퍼만 주고받기 때문이다. [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 로컬 연결(MySQL의 `.sock` [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))이 `127.0.0.1`보다 빠른 이유가 이 오버헤드 차이 때문이다.

### 과목 융합 관점

- <strong><a href="/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a> (OS)</strong>: 안드로이드 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 이 2-Copy와 0-Copy의 딜레마를 해결하기 위해 <strong><a href="/studynote/02_operating_system/10_security/662_android_binder_ipc_thread_pool/">Binder</a>(바인더)</strong>라는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 드라이버를 독자 개발했다. 송신자의 유저 스페이스에서 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)로 1번만 복사하면, [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 수신자의 유저 스페이스(mmap된 공간)에 직접 꽂아줌으로써 <strong>1-Copy</strong>라는 타협점을 찾아 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 보안([커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 권한 제어)을 동시에 잡았다.
- <strong><a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 시스템 (Distributed System)</strong>: [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 간에 [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/)([RPC](/studynote/02_operating_system/02_process_thread/126_rpc/), [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/))를 할 때, 직렬화/역직렬화(Serialization) 오버헤드가 발생한다. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 JSON으로 바꾸는 데 CPU가 다 소모되므로, [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 버퍼([gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/))나 FlatBuffers 같은 바이너리 직렬화 프레임워크를 도입하는 것이 클라우드 [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) 오버헤드 최적화의 기본이다.

- **📢 섹션 요약 비유**: 자전거([파이프](/studynote/02_operating_system/02_process_thread/123_pipe/))는 타기 쉽지만 짐을 적게 싣고, 트럭([공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/))은 짐을 많이 싣지만 운전 면허([동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 락)를 따기 어렵습니다. 안드로이드 바인더는 이 둘의 장점을 섞은 소형 택배차(1-Copy)입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/">마이크로서비스</a>(<a href="/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a>) 로컬 <a href="/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/">프록시</a> 통신 병목 (<a href="/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/">TCP</a> vs UDS)</strong>: [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/)) 내에서 앱 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)와 [사이드카](/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)(Envoy [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/))가 통신할 때, 로컬 호스트(`127.0.0.1`)를 통한 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 통신을 썼더니 초당 1만 건의 트래픽에서 CPU 100% 병목이 발생함.
   - **원인 분석**: 루프백(`127.0.0.1`) [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 통신은 실제 랜카드([NIC](/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/))로 나가진 않지만, 리눅스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 무거운 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/IP [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)([방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/), [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 상태 머신)을 전부 통과해야 하므로 패킷 1개당 엄청난 CPU 오버헤드가 발생한다.
   - <strong>대응 (Unix <a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">Domain</a> <a href="/studynote/02_operating_system/02_process_thread/125_socket/">Socket</a> 적용)</strong>: [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 내 공유 볼륨(EmptyDir)을 마운트하고 통신 방식을 `127.0.0.1`에서 <strong>Unix <a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">Domain</a> <a href="/studynote/02_operating_system/02_process_thread/125_socket/">Socket</a> (<code>/tmp/envoy.sock</code>)</strong>으로 변경한다. [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 이 통신이 로컬임을 즉시 인지하고 네트워크 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)을 100% 바이패스하여 메모리 복사만 수행하므로, CPU 오버헤드가 50% 이하로 극감하고 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))이 2배 이상 뛴다.

2. <strong>시나리오 — 고화질 <a href="/studynote/09_security/18_iot_ot_physical/933_cctv/">CCTV</a> 영상 처리 <a href="/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a>라인 최적화 (<a href="/studynote/02_operating_system/02_process_thread/118_shared_memory/">공유 메모리</a>)</strong>: 카메라 프로세스가 4K 영상을 캡처하고, [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 프로세스가 이를 넘겨받아 얼굴 인식을 한다. 두 프로세스 간에 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)([Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/))로 영상을 넘겼더니 프레임이 뚝뚝 끊김(30fps -> 10fps).
   - **원인 분석**: 4K 영상 1프레임(약 25MB)을 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)로 넘길 때마다 유저 $\rightarrow$ [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) $\rightarrow$ 유저로 2번의 복사(50MB)가 일어난다. 초당 30프레임이면 1.5GB/s의 메모리 복사 오버헤드가 생겨 시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 마비된다.
   - **아키텍처 적용 (SHM + Ring Buffer)**: POSIX [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/)(`shm_open`)를 생성하여 두 프로세스가 동일한 물리 메모리(4K 버퍼)를 바라보게 한다. 카메라가 버퍼 0번에 영상을 다 쓰면 락([Semaphore](/studynote/02_operating_system/04_synchronization/224_semaphore/))을 풀고, AI가 바로 읽어간다. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동(Copy) 오버헤드는 0([Zero](/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/))이 되며 프레임 드랍이 완벽히 해결된다.

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 성능 최적화를 위한 IPC 아키텍처 선택 플로우               |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [두 개의 독립된 프로세스 간에 데이터를 주고받아야 함]                       |
  |                |                                                  |
  |                v                                                  |
  |      주고받는 데이터의 크기가 메가바이트(MB) 단위 이상으로 큰가?               |
  |          +- 예 ------> [Shared Memory (공유 메모리) 채택]             |
  |          |            (개발 복잡도가 높더라도 2-Copy 오버헤드를 막아야 함) |
  |          +- 아니오 (수십 바이트 크기의 단순한 제어 명령어, JSON 등)         |
  |                |                                                  |
  |                v                                                  |
  |      서로 다른 물리적 컴퓨터(네트워크) 간의 통신 가능성을 열어두어야 하는가?      |
  |          +- 예 ------> [TCP/UDP Socket 채택]                         |
  |          |            (오버헤드는 가장 크지만 완벽한 확장성 제공)           |
  |          |                                                        |
  |          +- 아니오 ---> [Unix Domain Socket 또는 Message Queue 채택] |
  |                         (단일 머신 내에서 개발 생산성과 속도의 최적 타협점)  |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** "[공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/)가 무조건 제일 빠르니까 [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/)만 쓰자!"라고 주장하는 것은 주니어의 흔한 착각이다. [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/)를 쓸 때 발생하는 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 락([Mutex](/studynote/02_operating_system/04_synchronization/223_mutex/)) 병목이나 락 해제 누락([Deadlock](/studynote/02_operating_system/05_deadlock/281_deadlock_definition/))에 따른 유지보수 비용은 상상을 초월한다. 시스템 아키텍트는 <strong>"<a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>이 깡패인 대용량 미디어 처리에는 <a href="/studynote/02_operating_system/02_process_thread/118_shared_memory/">공유 메모리</a>를, 비즈니스 로직이 중요한 <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/">마이크로서비스</a> 간 통신에는 <a href="/studynote/02_operating_system/02_process_thread/125_socket/">소켓</a>이나 메시지 큐"</strong>를 배치하는 이분법적 전략을 가져가야 한다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **Cache Line Bouncing (캐시 핑퐁) 회피**: [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/) 구현 시, 송신자가 쓰는 변수와 수신자가 쓰는 [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) 변수가 우연히 같은 64바이트 캐시 라인에 위치하면, 양쪽 CPU 코어의 L1 캐시가 계속 무효화(Invalidate)되며 극심한 하드웨어 오버헤드가 발생한다. 변수 사이에 [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)([Padding](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/))을 넣어 [거짓 공유](/studynote/01_computer_architecture/11_multicore_synchronization/409_false_sharing/)([False Sharing](/studynote/01_computer_architecture/11_multicore_synchronization/409_false_sharing/))를 막았는가?
- **메시지 큐 크기 제한**: System V 메시지 큐나 POSIX 큐는 OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리를 사용하므로 크기 한계(기본 8KB~수 MB)가 빡빡하다. 큐가 가득 찼을 때 송신 프로세스가 멈추는([Blocking](/studynote/02_operating_system/02_process_thread/122_sync_async_communication/)) 오버헤드를 피하기 위해 비동기 모드(`O_NONBLOCK`)로 에러 처리를 꼼꼼히 구현했는가?

- **📢 섹션 요약 비유**: 작은 우편물을 보낼 때 택배비(메시지 패싱)를 아끼겠다고 부산에서 서울까지 직접 걸어가는 것([공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/) 락 구현)은 바보짓입니다. 화물 용량과 목적지에 따라 오토바이, 기차, 비행기를 적절히 섞어 쓰는 것이 진정한 물류([IPC](/studynote/02_operating_system/02_process_thread/117_ipc/)) 최적화입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 레거시 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) ([Stream](/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/) [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/)) | UDS / [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/) 최적화 적용 | 개선 효과 |
|:---|:---|:---|:---|
| <strong>정량 (전송 <a href="/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">대역폭</a>)</strong>| 초당 수백 MB 한계 (2-Copy) | 초당 수십 GB 달성 (0-Copy) | 대용량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(영상, 빅데이터) 병목 해소 |
| **정량 (CPU 사용률)**| [Context](/studynote/02_operating_system/01_overview_architecture/033_context/) Switch로 %sys 타임 폭주 | 유저 모드 통신으로 오버헤드 극감 | 잔여 CPU를 실제 비즈니스 로직에 투입 가능 |
| **정성 (아키텍처)** | 복잡한 네트워크 통신 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 강제 | UDS 적용으로 로컬 통신 투명성 확보 | [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 로컬 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)의 [보안성](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) 및 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상 |

### 미래 전망
- <strong><a href="/studynote/02_operating_system/10_security/615_ebpf/">eBPF</a> 기반 <a href="/studynote/02_operating_system/02_process_thread/117_ipc/">IPC</a> 가속</strong>: [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 환경에서 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/)) 간의 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 통신을 [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) 훅이 감지하여, [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 버퍼를 거치지 않고 송신자의 메모리에서 수신자의 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 큐로 다이렉트 복사해 버리는(Sockmap 패스스루) 차세대 런타임 가속 기능이 [Cilium](/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/) 등에 도입되어 [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) 오버헤드를 소멸시키고 있다.
- <strong>하드웨어 가속 <a href="/studynote/02_operating_system/02_process_thread/117_ipc/">IPC</a> (<a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/">CXL</a>/<a href="/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/">RDMA</a>)</strong>: 단일 머신 내부의 [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/) 개념을 확장하여, 아예 다른 서버 랙(Rack)에 있는 프로세스의 메모리를 내 메모리처럼 읽고 쓰는 RDMA나 [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 기반의 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 원격 [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/)(0-Copy over Network)가 클라우드 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)센터의 표준 통신망으로 자리 잡고 있다.

### 결론
[IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) 기법의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 오버헤드는, [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 "프로세스의 격리를 통한 절대적 안전([Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))"을 지키기 위해 어쩔 수 없이 지불해야 하는 보안세([Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Tax)다. 개발자가 이 세금을 내기 싫다면 직접 락([Lock](/studynote/05_database/04_transactions_concurrency/510_lock/))을 들고 [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/)의 전쟁터로 나가야 하고, 편하게 살고 싶다면 2-Copy의 페널티를 감수하고 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)([파이프](/studynote/02_operating_system/02_process_thread/123_pipe/), [소켓](/studynote/02_operating_system/02_process_thread/125_socket/))에 일을 맡기면 된다. 훌륭한 아키텍처는 이 극단 사이에서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 크기와 호출 빈도를 수학적으로 계산하여, 가장 적절한 통로를 뚫어주는 정교한 타협의 예술이다.

- **📢 섹션 요약 비유**: 성벽(프로세스 격리)을 높이 쌓을수록 성문([IPC](/studynote/02_operating_system/02_process_thread/117_ipc/))을 통과하는 검색 시간(오버헤드)은 길어집니다. 짐의 크기에 따라 개구멍([파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)), 비밀 통로([공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/)), 공식 무역항([소켓](/studynote/02_operating_system/02_process_thread/125_socket/))을 적절히 개방하는 성주(아키텍트)만이 제국을 가장 번영하게 만들 수 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 시스템 콜 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 래퍼 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 모놀리식 vs [마이크로 커널](/studynote/04_software_engineering/09_cloud_native_ai_architecture/598_microkernel_plugin_architecture/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비교 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 프로세스 주소 공간 분리 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| PCB 구성 요소 필수 암기 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[모놀리식 vs 마이크로 커널 성능 비교]
    |
    v
[IPC 기법 성능 오버헤드 (IPC Performance Overhead)]
    |
    +---> [프로세스 주소 공간 분리]
    +---> [PCB 구성 요소 필수 암기]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 두 개의 섬(프로세스)에 사는 친구들이 물건을 교환해야 해요. 가장 안전한 방법은 바다의 경찰 아저씨([커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))에게 택배를 맡기는 거예요(메시지 패싱).
2. 하지만 경찰 아저씨를 거치면 시간이 2배로 걸리죠(복사 오버헤드). 그래서 두 섬 사이에 큰 다리를 놓고 물건을 그냥 밀어주기로 했어요([공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/)).
3. 속도는 엄청 빨라졌지만, 두 친구가 동시에 물건을 집으려다 다리 위에서 부딪혀 떨어질 수 있어요. 그래서 다리 양 끝에 신호등([동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 락)을 세우는 귀찮은 작업을 직접 해야 한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 681 / 800

<- **이전**: [680. 모놀리식 vs 마이크로 커널 성능 비교 (Monolithic Vs Microkernel Performance)](/studynote/02_operating_system/11_exam_summary/680_monolithic_vs_microkernel_performance/)
**다음**: [682. 프로세스 주소 공간 분리 (Process Address Space Isolation)](/studynote/02_operating_system/11_exam_summary/682_process_address_space_isolation/) ->

---
