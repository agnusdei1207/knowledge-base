+++
title = "520. PCIe 스위치 패브릭 (PCIe Switch Fabric)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) ([Peripheral Component Interconnect](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/) Express) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭은 제한된 루트 컴플렉스 ([Root Complex](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/358_root_complex/)) 레인을 패킷 스위칭 구조로 분기해, 더 많은 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) ([Graphics Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))·[SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) ([Solid State Drive](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))·[NIC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/) (Network Interface Card)를 하나의 I/O 토폴로지 안에 붙이게 만드는 확장용 내부 네트워크다.
> 2. **가치**: 잘 설계된 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭은 [P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) ([Peer-to-Peer](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/)) DMA를 통해 장치 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 CPU (Central Processing Unit) 복사 없이 직접 흐르게 하고, 멀티호스트와 자원 [풀링](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/)을 지원해 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) ([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))·고성능 컴퓨팅 ([HPC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/548_automotive_hpc/))·스토리지 시스템의 활용도를 크게 높인다.
> 3. **판단 포인트**: [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 수를 늘려 주지만 업스트림 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 새로 만들지는 않으므로, 오버서브스크립션, 홉 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), ACS ([Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/) Services) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 오류 격리, 전력·발열까지 함께 설계해야 진짜 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 나온다.

---

## Ⅰ. 개요 및 필요성

[PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭은 점대점 링크로 설계된 PCIe를 더 큰 장치 집합으로 확장하기 위한 구조다. CPU (Central Processing Unit)나 [SoC](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/131_soc/) ([System on Chip](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/131_soc/))가 제공하는 [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) 레인 수는 한정돼 있으므로, 직접 연결만으로는 대량의 [NVMe](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) ([Non-Volatile Memory Express](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/)) [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/), 여러 장의 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/), 고속 NIC를 모두 붙이기 어렵다. 특히 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 서버, JBOF (Just a Bunch of Flash), 가속기 섀시처럼 장치 수가 CPU [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 수를 쉽게 넘는 환경에서는 단순 bifurcation만으로 해결되지 않는다.

여기서 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)의 역할은 단순한 분배기가 아니다. [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 계층 패킷을 읽고 적절한 다운스트림 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 전달하며, 같은 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 아래에 있는 장치끼리는 상위 루트 컴플렉스를 거치지 않고 서로 [직접 통신](/knowledge-base/studynote/02_operating_system/02_process_thread/120_direct_communication/)하게 만들 수 있다. 그래서 [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭은 "[포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 늘리는 부품"이면서 동시에 <strong>I/O <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 경로를 재설계하는 토폴로지 장치</strong>다.

이 구조가 중요해진 배경은 두 가지다. 첫째, 장치 수와 장치당 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 요구가 동시에 커졌다. 둘째, [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) ↔ [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/), [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) ↔ [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/), [NIC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/) ↔ GPU처럼 CPU보다 장치끼리 주고받는 동서(East-West) 트래픽이 늘었다. 따라서 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭은 단순 확장이 아니라, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 CPU 중심에서 장치 중심으로 흐르는 환경에 맞춘 해법이다.

- **📢 섹션 요약 비유**: [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭은 집 안의 멀티탭이 아니라, 대형 건물의 배전반에 가깝다. 콘센트 수만 늘리는 것이 아니라 어느 층에 얼마나 전력을 보낼지 구조 자체를 다시 짜는 장치다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 업스트림 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), 여러 개의 다운스트림 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), 내부 크로스바, 버퍼, [흐름 제어](/knowledge-base/studynote/03_network/04_data_link_layer_error/213_flow_control_buffer_overflow/) 로직으로 구성된다. 호스트에서 내려온 [TLP](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/385_tlp/) ([Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Layer Packet)를 주소와 ID에 따라 올바른 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)하고, 필요하면 같은 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 안에서 장치 간 트래픽을 로컬로 처리한다. 구현에 따라 cut-through에 가까운 빠른 전달을 하기도 하고, store-and-forward처럼 좀 더 보수적으로 버퍼링한 뒤 전달하기도 한다.

이 그림은 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 수를 늘리는 동시에, 어디서 병목이 생길 수 있는지를 보여준다.

```text
+----------------------------------------------------------------------+
|      switch fabric는 fan-out과 local routing을 주지만 uplink는 유한 |
+----------------------------------------------------------------------+
| Host / Root Complex  x16                                             |
|          |                                                           |
|          v                                                           |
|   [ Upstream Port ]                                                  |
|          |                                                           |
|   +------+-------------------------------------------------------+    |
|   |                    PCIe Switch Fabric                         |    |
|   |  crossbar + buffers + arbitration                             |    |
|   +---------------+-------------------+---------------------------+    |
|   | Down x16      | Down x16          | Down x4                   |    |
|   v               v                   v                           |    |
| GPU0  <--- P2P -->  GPU1             NVMe SSD                       |    |
|   |                                                    multi-host |    |
|   +------------------------- local switching ---------------------+    |
|                                                                      |
| aggregate hot traffic > x16 uplink  -> oversubscription bottleneck    |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 설계 시 보는 포인트 |
| :--- | :--- | :--- |
| Upstream [Port](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) | 호스트와 연결되는 상향 링크 | 전체 시스템의 최종 병목이 되기 쉬움 |
| Downstream [Port](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) | 장치 또는 하위 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 연결 | 장치별 요구 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)과 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 폭 매칭 필요 |
| 내부 크로스바 / 버퍼 | [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 간 패킷 중재와 전달 | 혼잡 시 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 [head-of-line](/knowledge-base/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/) [blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/) 최소화 |
| [P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) 경로 | 같은 패브릭 내 장치 간 [직접 통신](/knowledge-base/studynote/02_operating_system/02_process_thread/120_direct_communication/) | CPU 메모리 왕복 감소, 소프트웨어 지원 필요 |
| NTB (Non-Transparent [Bridge](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)) / 멀티호스트 | 서로 다른 호스트를 분리 연결 | 주소 공간 격리, 장애 전파 범위 관리 필요 |

따라서 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭의 핵심은 "링크를 더 만든다"가 아니라, <strong>어떤 트래픽은 로컬에서 돌리고 어떤 트래픽만 상위로 올릴지 결정하는 <a href="/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a> 구조</strong>에 있다. 이 때문에 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 단순 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 수보다 내부 중재 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)과 실제 트래픽 행렬에 더 크게 좌우된다.

- **📢 섹션 요약 비유**: [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭은 입체 교차로와 같다. 길이 많다고 다 빨라지는 것이 아니라, 어디서 바로 빠지고 어디서 합류하는지가 교통 흐름을 결정한다.

---

## Ⅲ. 비교 및 연결

[PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭은 lane bifurcation과 자주 혼동되지만 성격이 다르다. bifurcation은 CPU가 가진 x16 레인을 x8+x8 또는 x4+x4+x4+x4처럼 <strong>정적으로 쪼개는 것</strong>이고, [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 들어온 트래픽을 <strong>패킷 단위로 중재하고 <a href="/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a>하는 것</strong>이다. 즉 bifurcation은 배선을 나누는 기술이고, [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 토폴로지를 확장하는 기술이다.

| 방식 | 장점 | 약점 | 잘 맞는 환경 |
| :--- | :--- | :--- | :--- |
| 직접 연결 / bifurcation | 가장 낮은 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 구조 단순 | CPU 레인 수만큼만 확장 가능 | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 민감 장치, 소규모 서버 |
| [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭 | [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 수 확대, 로컬 [P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/), 멀티호스트 가능 | 홉 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 오버서브스크립션 관리 필요 | [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 확장, [NVMe](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) 박스, 가속기 섀시 |
| [CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) ([Compute Express Link](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/)) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) / 외부 패브릭 | [메모리 풀링](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/442_memory_pooling/)·coherence 확장 가능 | 제어 복잡도와 비용 증가 | 차세대 composable infrastructure |

여기서 중요한 연결 개념이 ACS다. 보안과 격리를 위해 ACS redirect를 강하게 켜면, 장치 간 트래픽이 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 내부에서 바로 가지 못하고 상위 루트 컴플렉스로 우회할 수 있다. 즉 "P2P를 지원하는 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)"가 있어도 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/), [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), [IOMMU](/knowledge-base/studynote/02_operating_system/10_security/627_iommu_dma_isolation/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 이를 막으면 기대한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로가 나오지 않는다.

또한 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭은 NTB, GPUDirect, [NVMe-oF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/499_nvme_over_fabrics/) ([NVMe over Fabrics](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/499_nvme_over_fabrics/)) 대상 장치 박스, 스토리지 풀과도 이어진다. 하나의 호스트 안에서만 쓰는 장치 허브가 아니라, 멀티호스트 자원 분리와 장치 공유, 서비스형 가속기 인프라를 만드는 기반으로 확장되기 때문이다.

- **📢 섹션 요약 비유**: bifurcation이 한 도로를 여러 갈래로 나누는 분기점이라면, [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 신호등과 우회로까지 갖춘 교차로다. 차선만 늘어나는 것과 교통을 통제하는 것은 전혀 다른 일이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭 설계의 핵심은 장치 목록이 아니라 트래픽 행렬이다. 예를 들어 GPU가 주로 CPU 메모리와 통신하는지, GPU끼리 [직접 통신](/knowledge-base/studynote/02_operating_system/02_process_thread/120_direct_communication/)하는지, NVMe가 동시에 풀 스루풋으로 읽히는지에 따라 최적 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 배치가 달라진다. [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 수를 늘려 주지만, 업스트림 x16 하나에 고대역 장치 여러 개를 붙이면 결국 위쪽 링크가 병목이 된다.

또한 P2P가 중요하다면 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 옵션, ACS, [IOMMU](/knowledge-base/studynote/02_operating_system/10_security/627_iommu_dma_isolation/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 드라이버 지원을 함께 확인해야 한다. 하드웨어만 보고 "[스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 있으니 GPU와 NVMe가 [직접 통신](/knowledge-base/studynote/02_operating_system/02_process_thread/120_direct_communication/)하겠지"라고 가정하면 안 된다. 실제로는 보안 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이나 주소 해석 문제 때문에 상위 루트로 우회되거나, 일부 조합에서는 아예 P2P가 제한될 수 있다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 장치 간 실제 hot path가 무엇인지, CPU 경유 트래픽과 [P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) 트래픽 비율을 파악했는가?
2. 업스트림 대비 다운스트림의 동시 최대 수요를 계산해 오버서브스크립션 비율을 확인했는가?
3. 홉 수가 늘어날 때 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 민감 장치의 tail latency가 허용 범위 안에 있는가?
4. ACS, [IOMMU](/knowledge-base/studynote/02_operating_system/10_security/627_iommu_dma_isolation/), 리셋 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/), AER ([Advanced Error Reporting](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/716_pcie_aer/)) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 원하는 격리 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)과 일치하는가?
5. [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 칩 전력, 방열, 케이블 길이, hot-plug 운영까지 포함해 시스템 수준으로 검토했는가?

### 피해야 할 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 있으니 CPU 업스트림 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 한계도 사라진다고 오해하는 설계
- [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 민감 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 군집을 깊은 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 체인 뒤에 배치하는 토폴로지
- ACS redirect를 강하게 켜 둔 채 [P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) [DMA](/knowledge-base/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 원인을 소프트웨어 탓으로만 돌리는 운영

- **📢 섹션 요약 비유**: [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭 설계는 쇼핑몰 주차장 출입구를 짜는 일과 같다. 주차면이 많아도 출입구가 좁고 동선이 꼬이면 차는 결국 한곳에 몰린다.

---

## Ⅴ. 기대효과 및 결론

[PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭을 제대로 설계하면 같은 CPU 레인 자원으로 더 많은 장치를 붙이고, 장치 간 [직접 통신](/knowledge-base/studynote/02_operating_system/02_process_thread/120_direct_communication/)을 활성화하며, 가속기와 스토리지를 더 유연하게 [풀링](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/)할 수 있다. 그래서 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 학습 노드, 스토리지 확장 섀시, 멀티호스트 가속기 박스에서 시스템 활용도가 크게 오른다. 특히 CPU 메모리를 우회하는 [P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) 경로가 잘 살아나면, 복사 오버헤드와 루트 컴플렉스 부담이 함께 줄어든다.

반대로 잘못 설계하면 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 단순한 병목 증폭기로 바뀐다. [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 수는 많아 보이는데 업링크가 막히고, 홉 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 누적되고, 리셋이나 오류가 넓게 번져 운영성이 떨어질 수 있다. 앞으로는 [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) 6.0 이후 세대, 케이블 기반 외부 패브릭, [CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 스위칭과의 결합을 통해 더 큰 규모의 composable infrastructure로 확장되겠지만, 기본 원리는 여전히 같다. <strong>토폴로지를 잘 짜야 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>이 나온다.</strong>

결론적으로 [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭은 단순한 멀티포트 허브가 아니라, <strong>장치 수·<a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">대역폭</a>·<a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>·격리를 동시에 설계하는 I/O 토폴로지 엔진</strong>이다. 이 개념은 "[포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 확장"보다 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어디로 어떻게 흐르는가를 설계하는 기술"로 기억해야 정확하다.

- **📢 섹션 요약 비유**: [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭은 도시의 고속도로 인터체인지와 같다. 길을 많이 내는 것보다, 어떤 차를 어디로 우회시킬지 잘 설계할 때 도시 전체가 빨라진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Root Complex](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/358_root_complex/) | [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭이 결국 연결되는 상위 호스트 I/O 출발점이다. |
| Lane Bifurcation | [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)와 자주 혼동되지만, 정적 레인 분할이라는 점에서 성격이 다르다. |
| [P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) [DMA](/knowledge-base/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) | [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭이 제공하는 가장 중요한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로 최적화다. |
| ACS ([Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/) Services) | 격리와 보안 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 [P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) 경로를 바꾸는 핵심 제어 기능이다. |
| NTB (Non-Transparent [Bridge](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)) | 멀티호스트 연결과 자원 공유를 가능하게 하는 확장 요소다. |
| [CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) [Switch](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) | [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) 물리층 위에서 메모리 coherence와 [풀링](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/)으로 확장되는 다음 단계다. |

### 📈 관련 키워드 및 발전 흐름도

```text
직접 연결 PCIe 장치
        |
        v
lane bifurcation 기반 정적 분기
        |
        v
PCIe 스위치 패브릭
        |
        +--> P2P DMA
        +--> 멀티호스트 / NTB
        +--> JBOF · GPU expansion chassis
        |
        v
CXL switch · composable infrastructure · 외부 패브릭 확장
```

이 흐름은 "[포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 나누는 수준"에서 출발해, "장치 간 경로와 자원 풀을 설계하는 수준"으로 진화하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 컴퓨터 안에 더 많은 길을 만들어 주는 교통 정리 센터예요.
2. 친구들끼리 물건을 주고받을 때 꼭 선생님 책상을 거치지 않아도 되게 도와줘요.
3. 하지만 큰길 하나가 너무 좁으면 아무리 갈래길이 많아도 결국 그곳에서 막히기 때문에 길 배치를 잘해야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 520 / 803

<- **이전**: [519. IOMMU 성능 오버헤드 (IOMMU Performance Overhead)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/519_iommu_overhead/)
**다음**: [521. NVMe 오버 패브릭 (NVMe-oF)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/521_nvme_of/) ->

---
