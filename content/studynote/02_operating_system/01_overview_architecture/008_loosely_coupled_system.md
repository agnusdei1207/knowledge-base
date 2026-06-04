+++
title = "8. 약결합 시스템 (Loosely Coupled System) / 분산 시스템"
date = 2026-03-21

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 약결합 시스템 (Loosely Coupled System)은 각 프로세서가 자신만의 독립된 메모리(Local Memory)를 가지며, 네트워크를 통한 메시지 패싱([Message Passing](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/)) 방식으로 협업하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅 시스템이다.
> 2. **가치**: 자원 공유로 인한 병목이 없어 무한에 가까운 수평적 확장([Scale-out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))이 가능하고, 특정 노드 장애가 전체로 전파되지 않는 높은 [결함 허용](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/296_fault_tolerance_architecture/)([Fault Tolerance](/knowledge-base/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/)) 능력을 제공한다.
> 3. **융합**: 현대의 [클라우드 컴퓨팅](/knowledge-base/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/), [마이크로서비스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/)([MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/)), 빅데이터 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리([Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)/Spark)의 물리적 근간이며, [네트워크 지연](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/) 시간([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)([Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) 관리가 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 핵심이다.

---

## Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

- **개념**: 약결합 시스템 (Loosely Coupled System)은 여러 개의 독립적인 컴퓨터 노드들이 고속 네트워크로 연결되어 하나의 시스템처럼 동작하는 아키텍처다. 각 노드는 자체 프로세서, 메모리, [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) (OS, [Operating System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))를 독립적으로 보유하며, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공유는 [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)가 아닌 네트워크를 통한 메시지 교환 ([Message Passing](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/))으로 이루어진다.

- **필요성**: [강결합 시스템](/knowledge-base/studynote/02_operating_system/01_overview_architecture/007_tightly_coupled_system/)의 물리적 확장 한계를 극복하고, 전 세계적인 규모의 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 안정적으로 운영하기 위해 필수적이다. 단일 시스템의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 넘어서는 대규모 연산이 필요하거나, 지리적으로 떨어진 자원을 통합해야 할 때, 그리고 시스템의 일부가 고장 나도 전체 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 유지되어야 하는 '고가용성(High [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))' 요구를 충족하기 위해 도입되었다.

- **💡 비유**: 약결합 시스템은 "각자의 주방(메모리)에서 요리하는 여러 명의 요리사가 전화나 메신저(네트워크)로 주문 상황을 공유하는 것"과 같다. 서로의 조리 도구가 부딪힐 일은 없지만, 정보를 전달하는 데 시간이 조금 더 걸리는 구조다.

- **등장 배경**: [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 메인프레임 중심의 중앙 집중형 방식은 비용이 매우 비싸고 확장이 어려웠다. 1980년대 이후 워크스테이션과 PC의 보급, 그리고 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)([Ethernet](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/))과 같은 네트워크 기술의 발전으로 저렴한 컴퓨터 여러 대를 묶어 슈퍼컴퓨터 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 내는 '[클러스터 컴퓨팅](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/383_cluster_computing/)'이 등장하며 약결합 시스템이 주류가 되었다.

```text
  +-------------------------------------------------------------+
  |           약결합 시스템 (Loosely Coupled) 기본 구조         |
  +-------------------------------------------------------------+
  |                                                             |
  |  [ Node A ]          [ Node B ]          [ Node C ]         |
  |  +-------+           +-------+           +-------+          |
  |  | CPU   |           | CPU   |           | CPU   |          |
  |  +-------+           +-------+           +-------+          |
  |  |Local M|           |Local M|           |Local M|          |
  |  +---+---+           +---+---+           +---+---+          |
  |      |                   |                   |              |
  |  +---+-------------------+-------------------+---+          |
  |  |           High-Speed Network (Switch)         |          |
  |  +-----------------------------------------------+          |
  |                                                             |
  |  [특징] 독립된 메모리/OS, 메시지 기반 통신, 높은 유연성     |
  |  [장점] 노드 추가가 쉽고 장애 격리(Isolation)가 확실함      |
  +-------------------------------------------------------------+
```

**[다이어그램 해설]** 약결합 시스템의 가장 큰 특징은 '공유하는 자원이 없다([Shared Nothing](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/306_embedding_model/))'는 점이다. 각 노드(Node)는 완결된 형태의 컴퓨터이며, 오직 네트워크 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)를 통해서만 소통한다. 이는 [강결합 시스템](/knowledge-base/studynote/02_operating_system/01_overview_architecture/007_tightly_coupled_system/)의 치명적인 약점인 '공유 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 경합' 문제를 원천적으로 제거한다. 노드가 10대에서 100대로 늘어나도 각 노드의 내부 연산 속도는 변하지 않으며, 단지 네트워크 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)의 대역폭만 충분하다면 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 선형적으로 확장할 수 있다. 이러한 '[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)([Decentralization](/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/))'의 철학은 대규모 웹 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 트래픽 급증을 견디는 유일한 해결책이다.

- **📢 섹션 요약 비유**: 각자의 집에서 재택근무를 하며 화상회의로 협업하는 팀처럼, 독립성은 높지만 소통의 효율이 중요한 조직과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **컴퓨팅 노드 (Node)** | 독립적 연산 및 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 | 자체 OS와 메모리 상에서 프로세스 실행 | Bare-metal / [Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) | 개별 식당 |
| **로컬 메모리 (Local Memory)** | 해당 노드 전용 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 | 타 노드에서 직접 접근 불가 (격리) | DDR4 / [NVMe](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) | 식당 전용 냉장고 |
| <strong>네트워크 인터페이스 (<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/">NIC</a>)</strong> | 외부 노드와의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 송수신 창구 | 패킷 캡슐화 및 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 처리 | [Ethernet](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) / [InfiniBand](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/) | 식당 전화기 |
| **인터커넥트 (Interconnect)** | 노드 간 고속 통신 통로 | 저지연, 고대역폭 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송 | [RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) / [Fibre Channel](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) | 배달 도로 |
| <strong>메시지 패싱 <a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/">라이브러리</a></strong> | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서의 통신 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) | 송신(Send)과 수신(Receive) 함수 제공 | MPI ([Message Passing Interface](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/227_mpi_message_passing_interface_distributed_computing/)) | 공동 주문 플랫폼 |

---

### 메시지 패싱 ([Message Passing](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/)) 메커니즘

약결합 시스템에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공유는 메모리 복사가 아닌 '복사본의 전송'을 통해 이루어진다. 이 과정에서 발생하는 직렬화(Serialization)와 [네트워크 지연](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/)은 시스템 설계 시 반드시 고려해야 할 요소다.

```text
 +---------------------------------------------------------------+
 |               약결합 시스템 데이터 교환 흐름 (MPI 예시)       |
 +---------------------------------------------------------------+
 |                                                               |
 |   [Node 1: Sender]                 [Node 2: Receiver]         |
 |   +--------------+                 +--------------+           |
 |   | User App     |                 | User App     |           |
 |   +------+-------+                 +------^-------+           |
 |          | (1) MPI_Send                   | (4) MPI_Recv      |
 |   +------v-------+                 +------+-------+           |
 |   | OS Kernel    |                 | OS Kernel    |           |
 |   | (Buffer)     |                 | (Buffer)     |           |
 |   +------+-------+                 +------^-------+           |
 |          | (2) Packetizing         | (3) Reassembly           |
 |   +------v-------+                 +------+-------+           |
 |   | Network HW   | --- Network ---> | Network HW   |           |
 |   +--------------+                 +--------------+           |
 |                                                               |
 |  * 지연 시간(Latency) = SW 오버헤드 + 전송 시간 + 버퍼링 시간 |
 +---------------------------------------------------------------+
```

**[다이어그램 해설]** [강결합 시스템](/knowledge-base/studynote/02_operating_system/01_overview_architecture/007_tightly_coupled_system/)이 옆 사람의 도화지를 직접 보는 것이라면, 약결합 시스템은 내 도화지 내용을 편지로 써서(직렬화) 우체국([NIC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/))을 통해 보내는 과정과 같다. 송신 노드에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 패킷으로 쪼개고 헤더를 붙이는 과정(1~2), 그리고 수신 노드에서 이를 다시 조립하여 애플리케이션에 전달하는 과정(3~4)에서 불가피하게 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 발생한다. 따라서 약결합 시스템용 알고리즘은 '통신 횟수'를 최소화하고 한 번에 보낼 때 큰 덩어리로 보내는 전략이 유리하다. 실무에서는 이 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 줄이기 위해 CPU를 거치지 않고 메모리 간에 직접 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쏘는 [RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) (Remote [Direct Memory Access](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/318_dma/)) 기술이 고성능 클러스터에서 필수적으로 사용된다.

---

### 장애 격리와 고가용성 (High [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))

약결합 시스템의 가장 큰 매력은 '부분의 고장이 전체의 멸망으로 이어지지 않는다'는 점이다.

```text
 [Client Request] ---> [ Load Balancer ]
                                         |
             +-------------+-------------+
             v             v             v
       [ Node 1 ]    [ Node 2 ]    [ Node 3 ]
       (Running)     (⚠ Fault)     (Running)
             |             |             |
             +-------------+--+----------+
                              v
                      [ Health Check ]
                "Node 2 이상 발생 -> 트래픽 차단"
```

**[다이어그램 해설]** [강결합 시스템](/knowledge-base/studynote/02_operating_system/01_overview_architecture/007_tightly_coupled_system/)은 [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)나 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)에 문제가 생기면 모든 CPU가 오동작할 위험이 크지만, 약결합 시스템은 각 노드가 독립된 OS를 가지므로 장애가 물리적으로 격리([Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/))된다. 위 도식처럼 로드 밸런서([Load Balancer](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/031_load_balancer/))가 각 노드의 상태를 주기적으로 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)(Health Check)하다가, Node 2에 장애가 발생하면 즉시 해당 노드를 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 대열에서 제외한다. 나머지 Node 1과 3은 아무런 영향 없이 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 지속하며, 관리자는 시스템 가동 중에도 Node 2를 교체하거나 수리할 수 있다. 이것이 바로 '무중단 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)'를 가능케 하는 약결합 시스템의 핵심 원리이다.

- **📢 섹션 요약 비유**: 전구 여러 개를 병렬로 연결하여 하나가 나가도 나머지는 계속 켜져 있는 조명 장식과 같습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 약결합 (Loosely Coupled) vs 강결합 (Tightly Coupled) 심층 비교

| 비교 항목 | 약결합 시스템 (Loosely Coupled) | [강결합 시스템](/knowledge-base/studynote/02_operating_system/01_overview_architecture/007_tightly_coupled_system/) (Tightly Coupled) |
|:---|:---|:---|:---|
| **통신 메커니즘** | 메시지 패싱 ([Message Passing](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/)) | 공유 변수 (Shared Variables) |
| **물리적 거리** | 수 미터 ~ 수천 킬로미터 | 센티미터 (동일 보드/칩 내) |
| **운영 비용** | 높음 (네트워크 장비, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 관리) | 낮음 (단일 시스템 비용) |
| **프로그래밍 모델** | 복잡함 ([분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/), [RPC](/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/)) | 단순함 ([멀티스레딩](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/397_multithreading/)) |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a></strong> | 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)) | 즉각적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) (Strong [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/">신뢰성</a> 구조</strong> | 소프트웨어 기반 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) (Checkpoint) | 하드웨어 기반 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) ([ECC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/), Redundancy) |

약결합 시스템은 지리적 제약이 없어 전 세계 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)를 묶을 수 있지만, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 모든 노드에 완벽히 똑같이 복사되는 데 시간이 걸린다. 반면 강결합은 속도는 압도적이지만 물리적 케이블 길이나 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 감쇄 문제로 인해 한 뼘 이상의 거리를 두기 어렵다. 실무에서는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 중요한 연산은 강결합([GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 서버 내부)에서 처리하고, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 확장은 약결합(서버 간 클러스터)으로 처리하는 '하이브리드' 전략이 정석이다.

- **📢 섹션 요약 비유**: 약결합이 전 세계 지사들이 협업하는 "글로벌 대기업"이라면, 강결합은 한 사무실에서 어깨를 맞대고 일하는 "스타트업 팀"과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **대규모 쇼핑몰의 이벤트 트래픽 폭주**: 블랙 프라이데이 이벤트로 트래픽이 평소의 100배가 몰렸다. 단일 서버(강결합)였다면 CPU [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 업그레이드([Scale-up](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/))에 한계가 있어 사이트가 다운되었겠지만, 약결합 클라우드 환경에서는 자동으로 서버 노드를 1,000대까지 늘려(Auto-scaling) 대응함으로써 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단을 막을 수 있었다.

2. <strong><a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/">재해 복구</a>(<a href="/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/">DR</a>) 시스템 구축</strong>: [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 화재와 같은 대규모 재난에 대비해야 한다. [강결합 시스템](/knowledge-base/studynote/02_operating_system/01_overview_architecture/007_tightly_coupled_system/)은 물리적 위치가 고정되므로 재난에 취약하지만, 약결합 구조를 활용해 서울과 부산에 노드를 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 배치하고 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 실시간 복제함으로써 한쪽 센터가 전멸해도 다른 쪽에서 즉시 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 승계([Failover](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/))하도록 설계할 수 있다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **확장 규모**: 향후 시스템 규모가 10배 이상 커질 가능성이 있는가? (약결합 필수)
- **네트워크 인프라**: 노드 간 통신을 위한 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 대역폭이 충분하며, 이중화되어 있는가?
- **상태 관리**: 애플리케이션이 '[Stateless](/knowledge-base/studynote/15_devops_sre/05_devsecops/239_stateless_redis/)'하게 설계되어 어떤 노드에서 실행되든 결과가 같은가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **과도한 통신(Chatty Communication)**: 약결합 환경에서 아주 작은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 너무 자주 주고받으면, 실제 연산 시간보다 네트워크 대기 시간이 더 길어지는 배보다 배꼽이 큰 상황이 발생한다.
- <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 락(Distributed <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a>) 남용</strong>: 모든 노드가 하나의 자원을 쓰려고 중앙 집중식 락을 걸면, 약결합의 장점인 독립성이 사라지고 시스템 전체가 가장 느린 노드의 속도에 맞춰지게 된다.

- **📢 섹션 요약 비유**: 서로 다른 나라에 사는 사람들이 아주 작은 일까지 사사건건 전화로 상의해서 결정한다면, 실제 일은 못 하고 전화기만 붙들고 있는 것과 같습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 도입 전 (Single/Tightly) | 도입 후 (Loosely/Cluster) | 개선 효과 |
|:---|:---|:---|:---|
| **확장성** | 물리적 슬롯 제한 (Max 32 CPU) | 무제한 (Max 수만 대 이상) | 수평적 확장성 **무한대** |
| **안정성** | [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) ([SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)) 존재 | 장애 격리 및 자동 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) **99.999% (5 Nines)** 달성 |
| **비용 효율** | 고가의 전용 장비 필요 | 저렴한 범용 장비(Commodity HW) | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 대비 비용([TCO](/knowledge-base/studynote/12_it_management/01_governance_strategy/016_tco/)) **50% 이상 절감** |

### 미래 전망
약결합 시스템은 이제 클라우드를 넘어 <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/">엣지 컴퓨팅</a> (<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/">Edge Computing</a>)</strong>으로 확장되고 있다. 중앙 서버가 아닌 사용자의 스마트폰이나 자율주행차, 공장의 센서들이 각각의 노드가 되어 메시지를 주고받는 거대한 약결합 네트워크를 형성하고 있다. 또한, [네트워크 지연](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/)을 극복하기 위해 물리적 광통신 대신 위성 통신이나 [6G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/) 기술을 결합하여, 지구 전체를 하나의 거대한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨터로 만드는 방향으로 진화 중이다.

- **📢 섹션 요약 비유**: 예전에는 큰 공장에만 기계가 있었다면, 이제는 모든 가정집의 작은 기계들이 인터넷으로 연결되어 거대한 가상의 공장을 만드는 시대가 오고 있습니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))

| 개념 명칭 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 및 시너지 설명 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a> (Distributed OS)</strong> | 여러 노드의 자원을 사용자에게 하나의 시스템처럼 보이게 관리하는 OS |
| <strong><a href="/knowledge-base/studynote/03_network/16_data_center_cloud/833_load_balancing_l4_l7_switch_traffic_distribution/">로드 밸런싱</a> (<a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/196_hard_soft_real_time/">Load Balancing</a>)</strong> | 약결합 노드들에게 부하를 골고루 나누어 주는 핵심 기술 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/648_cap_theorem_storage/">캡 정리</a> (<a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/219_cap_pacelc_distributed_tradeoff/">CAP Theorem</a>)</strong> | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)(C), [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)(A), 분할 내성(P)을 동시에 만족할 수 없다는 이론 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/">RPC</a> (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/">Remote Procedure Call</a>)</strong> | 네트워크 너머의 함수를 마치 내 컴퓨터에 있는 것처럼 호출하는 기술 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/">쿠버네티스</a> (<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/">Kubernetes</a>)</strong> | 수많은 약결합 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 노드들을 효율적으로 오케스트레이션하는 표준 도구 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[강결합 시스템 (Tightly Coupled System) — 공유 메모리]
    |
    v
[약결합 시스템 (Loosely Coupled System) — 메시지 패싱]
    |
    v
[분산 운영체제 (Distributed OS)]
    |
    v
[마이크로서비스 아키텍처 (MSA)]
    |
    v
[엣지 컴퓨팅 (Edge Computing) / 클라우드 네이티브]
```

[운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 아키텍처가 단일 서버 [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/) 방식에서 수평 확장 가능한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)·[엣지 컴퓨팅](/knowledge-base/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/) 생태계로 진화한 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
1. 약결합 시스템은 <strong>"각자의 집에서 요리하는 요리사들이 서로 전화로 도와주는 것"</strong>과 같아요.
2. 한 명의 요리사가 갑자기 배가 아파서 쉬더라도, 다른 집에 있는 요리사들이 요리를 계속 만들 수 있어 안전해요.
3. 요리사가 더 많이 필요하면 새로운 친구를 부르기만 하면 되니까, 아주 커다란 파티 음식도 문제없이 준비할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 8 / 800

<- **이전**: [7. 강결합 시스템 (Tightly Coupled System)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/007_tightly_coupled_system/)
**다음**: [9. 실시간 시스템 (Real-time System) - Hard vs Soft](/knowledge-base/studynote/02_operating_system/01_overview_architecture/009_real_time_system/) ->

---
