+++
title = "1050. RDMA / RoCE 스토리지 서버 네트워킹"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) / [RoCE](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/523_roce/) 스토리지 서버 네트워킹은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 평가와 고급 분석에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) / [RoCE](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/523_roce/) 스토리지 서버 네트워킹을 이해하면 측정 정확도과 모델 적합성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 딥러닝([GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 서버)과 [NVMe](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 스토리지 시대가 오면서 옛날 방식이 무너졌습니다.
- <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/">스택</a> 통과</strong>: 데이터가 랜선으로 나가려면 무조건 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)([TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/IP [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/))을 거쳐야 합니다. 이 과정에서 메모리 복사([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/))가 수차례 일어납니다.
- **CPU 혹사**: 100Gbps 랜카드로 쏟아지는 패킷을 조립하느라 정작 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 연산을 해야 할 비싼 CPU가 패킷 까대기([인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 처리)를 하다가 100% 과부하로 서버가 기절해버립니다.

```text
[NTP / GPS 동기화]
    |
    v
[RDMA / RoCE 스토리지 서버 네트워킹]
    |
    +---> [VXLAN 오버레이 VTEP 터널링 연결기법]
```

- **📢 섹션 요약 비유**: [RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) / [RoCE](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/523_roce/) 스토리지 서버 네트워킹은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

- **개념**: 서버 A의 메인 메모리(RAM)에서 서버 B의 메인 메모리로, <strong>양쪽 서버의 CPU, 캐시, <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a>(OS <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a>)의 개입을 100% 무시하고 랜카드(RNIC) 하드웨어끼리 다이렉트로 메모리에 데이터를 꽂아 넣는(<a href="/knowledge-base/studynote/02_operating_system/09_file_system/566_mmap_zero_copy_sendfile/">Zero-Copy</a>, <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">Kernel</a> Bypass) <a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/">초고속</a>/초저지연 메모리 전송 기술</strong>입니다.

[RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) 텔레파시를 쏘려면 전용 랜카드와 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)(인프라)가 필요합니다. 어떤 랜선을 쓸까요?

### 1. [인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/) ([InfiniBand](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/), IB) - "금수저 귀족 전용망"
- 애초에 슈퍼컴퓨터들의 [RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) 통신을 위해 만들어진 <strong>오리지널 순혈 <a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/">초고속</a> 네트워크망</strong>입니다.
- 일반 랜선([이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/))을 안 쓰고, [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/), 랜카드, 케이블을 모조리 수천만 원짜리 '[인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/) 전용 하드웨어'로 싹 갈아엎어야 합니다. [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 시간이 나노초 단위로 가장 미친 듯이 빠르고 완벽하지만, 너무 비싸고 일반 인터넷망과 호환이 안 되는 폐쇄망입니다.

### 2. [RoCE](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/523_roce/) ([RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) over Converged [Ethernet](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)) 🌟 대세 🌟
- **개념**: 통신사 빡침 방지법입니다. "야! 우리가 수천억 들여 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)에 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)(일반 랜선과 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/))을 다 깔아놨는데, 언제 그 비싼 [인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)를 또 깔아! <strong>우리가 흔히 쓰는 일반 <a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/">이더넷</a>(<a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/">Ethernet</a>, 802.3) 패킷 껍데기 안에다가 <a href="/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/">인피니밴드</a>(<a href="/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/">RDMA</a>) 페이로드를 살짝 숨겨서(캡슐화) 쏴버리자!</strong>"
- <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/523_roce/">RoCE</a> v1 vs v2</strong>:
  - v1: 맥([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)) 주소만 쓰는 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) L2 기반이라 옆방 라우터를 넘어갈 수 없었습니다.
  - <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/523_roce/">RoCE</a> v2 (현재 천하 통일)</strong>: IP 주소와 [UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 헤더(L3/L4 계층)를 뒤집어씌워 라우팅이 가능해졌습니다. 그냥 <strong>흔한 인터넷 IP 환경 인프라를 그대로 쓰면서도 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> 바이패스의 달콤한 <a href="/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/">RDMA</a> 속도 꿀을 빠는 궁극의 하이브리드 타협 기술</strong>입니다.

### 3. [iWARP](/knowledge-base/studynote/03_network/16_data_center_cloud/814_iwarp_tcp_ip_based_rdma_compatibility/) (Internet Wide Area [RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))
- RoCE는 무지성 [UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 기반이라 데이터가 가다 손실되면 답이 없습니다. [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)단에서 혼잡 제어(PFC) 세팅을 미친 듯이 해줘야 합니다.
- <strong><a href="/knowledge-base/studynote/03_network/16_data_center_cloud/814_iwarp_tcp_ip_based_rdma_compatibility/">iWARP</a></strong>: "그냥 안전 빵 튼튼한 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/IP 뼈대 위에서 RDMA를 돌리자!"는 파생형인데, [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 특유의 무거운 오버헤드 때문에 속도에서 밀려 지금은 [RoCE](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/523_roce/) v2에 거의 압살당했습니다.

```text
[NTP / GPS 동기화]
    |
    v
[RDMA / RoCE 스토리지 서버 네트워킹]
    |
    +---> [VXLAN 오버레이 VTEP 터널링 연결기법]
```

- **📢 섹션 요약 비유**: [RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) / [RoCE](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/523_roce/) 스토리지 서버 네트워킹의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

[RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) / [RoCE](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/523_roce/) 스토리지 서버 네트워킹을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [NTP](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/536_ntp_network_time_protocol_stratum/) / GPS [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)가 기반 조건을 만든다면, [RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) / [RoCE](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/523_roce/) 스토리지 서버 네트워킹은 그 위에서 핵심 메커니즘을 구현하고, [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) 오버레이 VTEP [터널링](/knowledge-base/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/) 연결기법은 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 측정 정확도과 모델 적합성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [NTP](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/536_ntp_network_time_protocol_stratum/) / GPS [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)의 기반 정리 | [RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) / [RoCE](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/523_roce/) 스토리지 서버 네트워킹의 핵심 동작 | [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) 오버레이 VTEP [터널링](/knowledge-base/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/) 연결기법의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 측정 정확도 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) / [RoCE](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/523_roce/) 스토리지 서버 네트워킹은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- AWS나 Azure 클라우드에서 엔비디아(NVIDIA) [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 서버 수백 대를 묶어 챗GPT 같은 거대 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델을 학습시킵니다.
- [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 1번과 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 2번이 테라바이트급 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 데이터를 1초 만에 교환해야 하는데 CPU를 거치면 학습이 10년 걸립니다.
- 100Gbps 이상의 <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/523_roce/">RoCE</a> v2 지원 SmartNIC(랜카드)</strong>를 달아, [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리끼리 직접 직통으로([GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) [Direct](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/) [RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/)) 데이터를 꽂아버려 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 클러스터 연산 병목을 박살 낸 일등 공신 아키텍처입니다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 기존 <strong><a href="/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/">TCP</a>/IP 통신</strong>은 회사의 A 부서에서 B 부서로 100박스 서류를 보낼 때, <strong>'FM 절차를 밟는 비효율의 극치'</strong>입니다. A 부서장(CPU)이 결재하고 우편실([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))로 내려보내면, 우편실 직원([TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/IP [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/))이 서류를 분류해 B 부서 우편실로 보내고, 다시 B 부서장(CPU)이 서류를 하나하나 검수해서 창고(메모리)에 쌓아야 합니다. 부서장은 서류 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하느라 본업(연산)을 못 해 과로사로 쓰러집니다. <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/">RDMA</a> (<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/523_roce/">RoCE</a>)</strong>는 이런 쓸데없는 절차를 다 부수고 <strong>'두 부서 창고 사이에 다이렉트 컨베이어 벨트를 뚫어버린 기적'</strong>입니다. 부서장(CPU)과 우편실([운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))은 서류가 오가는지조차 모릅니다. 하드웨어 기계([RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) 랜카드)가 알아서 서류 100박스를 빛의 속도로 A 창고에서 B 창고(메모리)에 그대로 텔레포트시켜 꽂아버립니다([Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) Bypass & [Zero-Copy](/knowledge-base/studynote/02_operating_system/09_file_system/566_mmap_zero_copy_sendfile/)). 부서장은 오직 창고에 쌓인 완성된 서류만 꺼내서 100% 두뇌를 본업([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 연산)에만 집중할 수 있게 해주는 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 스토리지 망의 궁극의 마법입니다.

---

## Ⅴ. 기대효과 및 결론

[RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) / [RoCE](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/523_roce/) 스토리지 서버 네트워킹은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 평가와 고급 분석을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 측정 정확도 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) 오버레이 VTEP [터널링](/knowledge-base/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/) 연결기법, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) / [RoCE](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/523_roce/) 스토리지 서버 네트워킹은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [NTP](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/536_ntp_network_time_protocol_stratum/) / GPS [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) ([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)) | 실제 전달 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 나타내는 대표 지표다. |
| [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) ([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) | 사용자 체감 품질을 좌우한다. |
| [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) 오버레이 VTEP [터널링](/knowledge-base/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/) 연결기법 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: NTP / GPS 동기화]
    |
    v
[현재 개념: RDMA / RoCE 스토리지 서버 네트워킹]
    |
    +---> [확장 A: VXLAN 오버레이 VTEP 터널링 연결기법]
    +---> [확장 B: AI 기반 성능 예측]
```

[RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) / [RoCE](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/523_roce/) 스토리지 서버 네트워킹는 [NTP](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/536_ntp_network_time_protocol_stratum/) / GPS [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)에서 출발해 현재 메커니즘을 정교화하고, 이후 [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) 오버레이 VTEP [터널링](/knowledge-base/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/) 연결기법와 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 달리기 시합에서 누가 얼마나 빨랐는지 재려면 초시계와 기록표가 필요해요.
2. 이 개념은 네트워크가 어디서 느려졌는지 숫자로 찾아내는 도구예요.
3. 그래서 막연히 고치는 대신 가장 중요한 곳부터 똑똑하게 손볼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 155 / 1120

<- **이전**: [104. CSMA (Carrier Sense Multiple Access) 반송파 감지](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/104_csma/)
**다음**: [1051. VXLAN 오버레이 VTEP 터널링 연결기법](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1051_vxlan_overlay_vtep_tunneling_mac_in_udp/) ->

---
