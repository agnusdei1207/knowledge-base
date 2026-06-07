---
title: "523. RoCE (RDMA over Converged Ethernet)"
date: "2026-05-08"
tags:
  - "studynote-computer-architecture"
weight: 523
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: RoCE ([RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) over Converged [Ethernet](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/))는 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 위에 [RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) (Remote [Direct Memory Access](/studynote/01_computer_architecture/08_io_storage_systems/318_dma/)) 전송 의미를 얹어, 범용 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 네트워크에서도 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 우회·[직접 메모리 접근](/studynote/02_operating_system/08_storage_and_io_systems/450_dma_direct_memory_access/) 기반의 저지연 통신을 구현하는 기술이다.
> 2. **가치**: 전용 [인피니밴드](/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/) 패브릭 없이도 고속 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)와 RNIC ([RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) Network Interface Card)를 활용해 [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) ([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)) 학습, [NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) 오버 패브릭 ([NVMe-oF](/studynote/02_operating_system/08_storage_and_io_systems/499_nvme_over_fabrics/), [Non-Volatile Memory Express](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) over Fabrics), 스케일아웃 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 같은 워크로드의 동서향 통신 비용을 크게 낮춘다.
> 3. **판단 포인트**: RoCE [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 약어 자체보다 네트워크 튜닝에 달려 있다. PFC (Priority-based [Flow Control](/studynote/03_network/08_transport_layer/421_tcp_flow_control_sliding_window_algorithm/)), ECN (Explicit Congestion Notification), DCQCN ([Data Center](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) Quantized Congestion Notification), [우선순위 큐](/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/) 설계가 맞지 않으면 오히려 혼잡과 tail latency가 커질 수 있다.

---

## Ⅰ. 개요 및 필요성

RoCE는 "[이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)으로 RDMA를 하고 싶다"는 요구에서 출발했다. [인피니밴드](/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/) RDMA는 매우 빠르지만 전용 패브릭과 별도 운영 역량이 필요하다. 반면 대형 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)는 이미 대규모 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 장비와 운영 경험을 보유하고 있었으므로, 같은 케이블과 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 위에서 [RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) 이점을 얻으려는 시도가 자연스럽게 이어졌다.

하지만 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)의 기본 철학은 최선형 전달(best effort)이다. 패킷 손실과 재전송을 소프트웨어가 감당하는 구조는 웹 트래픽에는 괜찮지만, RDMA처럼 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 재시도에 매우 민감한 통신에는 불리하다. 그래서 RoCE는 단순한 캡슐화 기술이 아니라, [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)에 손실·혼잡 제어 규율을 더해 "RDMA가 견딜 수 있는 네트워크"를 만드는 작업과 같이 이해해야 한다.

이 그림은 RoCE가 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 비용 사이에서 어떤 절충점을 노리는지 보여 준다.

```text
+----------------------------------------------------------------------+
|      RoCE는 범용 Ethernet에 RDMA 전용 규칙을 얹어 비용과 성능을 절충 |
+----------------------------------------------------------------------+
| App / Accelerator                                                    |
|   |                                                                  |
| RNIC --------------- Ethernet Fabric --------------- RNIC             |
|   |                 (priority + ECN + queue 제어)                    |
|   v                                                                  |
| Remote Memory                                                        |
|                                                                      |
| 같은 스위치망을 쓰되, RDMA 흐름은 별도 우선순위와 혼잡 제어가 필요    |
+----------------------------------------------------------------------+
```

즉 RoCE는 "[이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 위에서 돌아가는 [RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/)"가 아니라, <strong><a href="/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/">이더넷</a>을 <a href="/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/">RDMA</a> 친화적으로 재조정한 패브릭</strong>이다. 이 관점을 놓치면 왜 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)이 네트워크 카드만큼 중요한지 설명할 수 없다.

- **📢 섹션 요약 비유**: RoCE는 일반 고속도로에 구급차 전용 차선을 따로 만드는 것과 같다. 도로는 같지만, 빨리 가야 하는 차를 위해 규칙과 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 체계를 다시 짜야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

RoCE는 [RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) 연산 자체는 [인피니밴드](/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/) 계열 전송 의미를 유지하면서, 그 운반 경로를 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)으로 바꾼다. 호스트 애플리케이션은 큐 쌍에 Work Request를 게시하고, RNIC는 등록된 메모리에서 데이터를 DMA로 읽어 패킷화한 뒤 전송한다. 수신 측 RNIC는 원격 메모리에 직접 쓰거나 읽고, 완료 큐를 통해 결과를 알린다.

RoCE v1은 계층 2 기반이라 같은 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 브로드캐스트 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 안에서만 동작했다. RoCE v2는 사용자 데이터그램 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)/인터넷 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) ([UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/)/IP) 헤더를 추가해 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 가능한 구조가 되었고, 현재 대부분의 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 구축은 v2를 전제로 한다. 하지만 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)이 가능해졌다고 해서 혼잡 문제가 사라지지는 않는다. 오히려 대규모 패브릭에서는 ECN 표시와 DCQCN 같은 혼잡 [회복](/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/) 메커니즘이 더 중요해진다.

| 요소 | 역할 | 운영 포인트 |
| :--- | :--- | :--- |
| RNIC ([RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) Network Interface Card) | [RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) 전송과 [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/) | [펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/)·드라이버·큐 튜닝 필요 |
| PFC (Priority-based [Flow Control](/studynote/03_network/08_transport_layer/421_tcp_flow_control_sliding_window_algorithm/)) | 우선순위별 일시 정지로 손실 완화 | 과도하면 [Head-of-Line](/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/) [Blocking](/studynote/02_operating_system/02_process_thread/122_sync_async_communication/) 유발 |
| ECN (Explicit Congestion Notification) | 혼잡 구간 표시 | [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 임계값 튜닝 중요 |
| DCQCN ([Data Center](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) Quantized Congestion Notification) | 송신 속도 조절 | 대규모 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 트래픽에서 핵심 |
| RoCE v2 | [UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/)/IP 기반 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 가능 | L3 확장성과 네트워크 설계 자유도 확보 |

이 그림은 RoCE v2가 어떤 계층 위에 세워지는지 보여 준다.

```text
+----------------------------------------------------------------------+
|          RoCE v2는 RDMA 전송을 UDP/IP 안에 실어 L3까지 확장한다      |
+----------------------------------------------------------------------+
| [ Ethernet ][ IP ][ UDP ][ InfiniBand Transport ][ RDMA Payload ]    |
|     ^          ^         ^                                           |
|     |          |         +- Queue Pair / Completion 의미 유지        |
|     |          +------------ ECN marking / routing                   |
|     +---------------------- PFC pause / priority queue              |
+----------------------------------------------------------------------+
```

따라서 RoCE의 핵심은 RNIC [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)만이 아니다. 패브릭 전체가 [RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) 흐름을 어떻게 우선시하고, 혼잡을 어떻게 완화하며, 손실을 어떻게 억제하는지가 실제 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 결정한다.

- **📢 섹션 요약 비유**: RoCE는 빠른 오토바이를 사는 것만으로 끝나지 않는다. [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 체계, 전용 차선, 과속 완충 장치까지 같이 설계해야 정말 빨라진다.

---

## Ⅲ. 비교 및 연결

RoCE의 경계는 [인피니밴드](/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)와 [iWARP](/studynote/03_network/16_data_center_cloud/814_iwarp_tcp_ip_based_rdma_compatibility/) (Internet Wide Area [RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))를 함께 볼 때 선명하다. [인피니밴드](/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)는 전용 패브릭이라 가장 일관된 저지연을 얻기 쉽고, iWARP는 전송 제어 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) ([TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)) 위에서 동작해 기존 네트워크 친화성이 높다. RoCE는 그 중간에서 "[이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 위에 가깝게 [인피니밴드](/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)급 RDMA를 구현"하려는 선택지다.

| 항목 | [인피니밴드](/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/) | RoCE v2 | [iWARP](/studynote/03_network/16_data_center_cloud/814_iwarp_tcp_ip_based_rdma_compatibility/) |
| :--- | :--- | :--- | :--- |
| 기반 패브릭 | 전용 패브릭 | [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) | [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) + [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) |
| [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 특성 | 최저, 예측성 높음 | 매우 낮음, 튜닝 의존 | 상대적으로 높음 |
| 운영 난도 | 전용 운영 필요 | [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)·품질 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/), [Quality of Service](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/)) 튜닝 중요 | [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 친화적 |
| 장점 | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 비용 효율과 보급성 | 손실 환경 적응성 |
| 대표 활용 | 슈퍼컴퓨터, 초대형 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) | 클라우드 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), [NVMe-oF](/studynote/02_operating_system/08_storage_and_io_systems/499_nvme_over_fabrics/) | 특정 엔터프라이즈 [RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) |

RoCE는 [NVMe-oF](/studynote/02_operating_system/08_storage_and_io_systems/499_nvme_over_fabrics/), GPUDirect [RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/), [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 키-값 저장소와도 긴밀히 연결된다. 특히 고성능 스토리지나 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 집합 통신은 기존 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)만으로는 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 아쉬웠지만, [인피니밴드](/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/) 전면 도입도 부담스러웠다. RoCE는 바로 그 공백을 메우며, "고속 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)의 [RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) 표준" 역할을 맡았다.

다만 RoCE는 장비만 꽂는다고 [인피니밴드](/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)처럼 동작하지 않는다. [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 네트워크 큐 길이, 버퍼 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/), 혼잡 제어, 우선순위 분리의 질에 따라 크게 흔들린다. 그래서 RoCE는 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이면서 동시에 네트워크 운영 완성도의 문제다.

- **📢 섹션 요약 비유**: [인피니밴드](/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)가 전용 철도라면, RoCE는 고속도로에 특급 물류선을 만든 방식이고, iWARP는 기존 도로 규칙을 그대로 쓰면서 더 똑똑한 운송 계약을 맺는 방식에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "이미 가진 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 자산으로 RDMA를 어디까지 끌어올릴 것인가"가 RoCE 채택의 핵심이다. 100/200/400기가비트 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)이 이미 깔려 있고, [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 학습이나 백엔드 스토리지 트래픽처럼 동서향 대역폭이 큰 환경이라면 RoCE가 매우 강력하다. 특히 [NVMe-oF](/studynote/02_operating_system/08_storage_and_io_systems/499_nvme_over_fabrics/) 백엔드, [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) ([Graphics Processing Unit](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)) 집합 통신, 메모리 중심 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 복제는 RoCE의 효과가 잘 드러나는 대표 사례다.

반대로 잘못 설계된 RoCE는 평균 속도보다 tail latency와 장애가 더 큰 문제를 만든다. PFC를 모든 트래픽에 무분별하게 켜면 [Head-of-Line](/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/) Blocking이 커지고, ECN 임계값이 맞지 않으면 패브릭 전체가 흔들릴 수 있다. 즉 RoCE는 하드웨어 스펙보다 <strong>네트워크 정책의 <a href="/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/">정밀도</a></strong>가 더 중요하다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) 트래픽을 일반 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 트래픽과 우선순위·큐 수준에서 분리했는가?
2. PFC는 필요한 클래스에만 제한적으로 적용했고, ECN/DCQCN 튜닝을 병행했는가?
3. [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 버퍼, 큐 깊이, 오버서브스크립션이 peak 동서향 트래픽을 감당하는가?
4. RoCE v1의 L2 제약인지, RoCE v2의 L3 설계인지 운영 범위를 명확히 정했는가?

### 피해야 할 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- "RoCE NIC만 꽂으면 [RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 나온다"는 플러그앤플레이식 기대
- 모든 우선순위 클래스에 PFC를 켜서 패브릭 전체를 멈추게 만드는 설계
- 웹·[백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)·[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)·스토리지 트래픽을 한 큐에 몰아넣는 혼합 운영

- **📢 섹션 요약 비유**: RoCE 운영은 응급차 전용 차선을 잘 그어 두는 일과 같다. 차가 좋다고 끝이 아니라, 어느 길을 비우고 어디서 속도를 줄일지까지 제대로 정해야 한다.

---

## Ⅴ. 기대효과 및 결론

RoCE의 가장 큰 효과는 RDMA를 전용 슈퍼컴퓨팅 기술에서 일반 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 기술로 끌어내렸다는 점이다. [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 자산을 활용해 저지연 메모리 접근, [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/), 고성능 스토리지 공유를 구현할 수 있으므로, 대규모 인프라에서 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 비용의 균형점을 찾기 쉽다. 이는 곧 AI와 스토리지 분리형 아키텍처의 확산으로 이어진다.

하지만 RoCE는 "저렴한 [인피니밴드](/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)"로만 기억하면 틀린다. 이 기술은 전용 패브릭 비용을 줄이는 대신, 네트워크 엔지니어링 난도를 올리는 구조다. 따라서 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 큐, 버퍼, PFC, ECN, 텔레메트리를 다룰 수 있는 팀이 있을 때 진짜 강점이 살아난다.

결론적으로 RoCE는 <strong><a href="/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/">이더넷</a>을 <a href="/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/">RDMA</a> 친화적인 패브릭으로 재훈련시키는 기술</strong>이다. 이 관점으로 보면 왜 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 클러스터, [NVMe-oF](/studynote/02_operating_system/08_storage_and_io_systems/499_nvme_over_fabrics/) 백엔드, [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 캐시가 RoCE를 선택하는지, 또 왜 네트워크 운영 미숙이 곧 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하로 이어지는지 한 번에 설명된다.

- **📢 섹션 요약 비유**: RoCE는 평범한 도시에 특급 물류망을 심는 일과 같다. 새 도시를 짓는 대신, 기존 도로를 더 똑똑하게 운영해 빠른 배송을 만드는 방식이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) (Remote [Direct Memory Access](/studynote/01_computer_architecture/08_io_storage_systems/318_dma/)) | RoCE가 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 위에서 구현하는 핵심 통신 의미다. |
| RNIC ([RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) Network Interface Card) | 메모리 직접 접근과 [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)을 담당하는 하드웨어다. |
| PFC (Priority-based [Flow Control](/studynote/03_network/08_transport_layer/421_tcp_flow_control_sliding_window_algorithm/)) | 손실 민감한 [RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) 흐름을 보호하는 대표 제어 수단이다. |
| ECN / DCQCN | PFC만으로 부족한 혼잡 제어를 보완해 tail latency를 줄인다. |
| [NVMe-oF](/studynote/02_operating_system/08_storage_and_io_systems/499_nvme_over_fabrics/) ([NVMe over Fabrics](/studynote/02_operating_system/08_storage_and_io_systems/499_nvme_over_fabrics/)) | RoCE가 자주 쓰이는 대표 상위 스토리지 워크로드다. |
| GPUDirect [RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) | [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리 통신을 가속해 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 클러스터 효율을 높인다. |

### 📈 관련 키워드 및 발전 흐름도

```text
Best-effort Ethernet
        |
        v
DCB (Data Center Bridging) 기반 우선순위 제어
        |
        v
RoCE v1 (L2 기반)
        |
        v
RoCE v2 (UDP/IP 기반)
        |
        v
ECN · DCQCN · AI / NVMe-oF 패브릭 최적화
```

이 흐름은 "범용 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)"이 "저지연 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 패브릭"으로 점차 특화되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. RoCE는 동네 큰 길을 그냥 쓰지 않고, 아주 급한 택배가 빨리 가도록 특별 규칙을 만든 길이에요.
2. 길은 원래 있던 길이라 돈을 많이 아끼지만, [신호](/studynote/02_operating_system/02_process_thread/130_signal/)등과 차선 규칙을 아주 잘 지켜야 해요.
3. 그래서 길 정리가 잘되면 멀리 있는 장난감도 아주 빨리 가져올 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 523 / 803

<- **이전**: [522. 인피니밴드 RDMA (InfiniBand RDMA)](/studynote/01_computer_architecture/15_advanced_topics/522_infiniband_rdma/)
**다음**: [524. 스토리지 클래스 메모리 (SCM) 계층화](/studynote/01_computer_architecture/15_advanced_topics/524_scm_tiering/) ->

---
