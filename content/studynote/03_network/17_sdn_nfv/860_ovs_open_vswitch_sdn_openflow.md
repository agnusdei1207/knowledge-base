+++
title = "860. OVS (Open vSwitch)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OVS는 [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)/NFV에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: OVS를 이해하면 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성과 자동화 수준 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 오픈스택(OpenStack)이나 [KVM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/713_kvm_over_ip/), [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 같은 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)/클라우드 환경에서, 서버([하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)) 내부에 존재하는 수십 개의 가상머신([VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))이나 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 간의 네트워크 트래픽을 처리하기 위해 만들어진 <strong>리눅스 기반의 고성능 <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/">오픈소스</a> '<a href="/knowledge-base/studynote/02_operating_system/10_security/630_vswitch_vnf_overhead/">가상 스위치</a>(Virtual <a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">Switch</a>)' 소프트웨어</strong>입니다.
- **지위**: 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)로 편입되어, 현존하는 클라우드 네트워크 배관의 사실상 산업 표준(De facto standard)입니다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">화이트박스 스위치</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">OVS</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">미니넷 SDN 토폴로지 에뮬레이터 연구 평가…</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: OVS는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

OVS가 멍청한 리눅스 기본 브릿지(Linux [Bridge](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/))를 학살하고 1짱이 된 데는 이유가 있습니다.

### 1. 거대 규모 [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 컨트롤러와의 완벽한 연동 ([OpenFlow](/knowledge-base/studynote/03_network/17_sdn_nfv/855_openflow_standard_protocol_sdn_southbound/)) 🌟
- 물리적인 [화이트박스 스위치](/knowledge-base/studynote/03_network/17_sdn_nfv/859_whitebox_switch_open_hardware_nos/)만 OpenFlow를 알아듣는 게 아닙니다.
- <strong>OVS는 태생부터 <a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/">SDN</a>(소프트웨어 정의 네트워크)을 위해 만들어진 <a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a>입니다.</strong> 
- 1,000대의 서버 뱃속에 있는 1,000개의 OVS들이 저 위 하늘에 떠 있는 중앙 [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 컨트롤러(뇌)와 <strong><a href="/knowledge-base/studynote/03_network/17_sdn_nfv/855_openflow_standard_protocol_sdn_southbound/">OpenFlow</a> <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a></strong>을 통해 대화를 나눕니다. 컨트롤러가 "이 IP는 막아라!"라고 플로우 룰을 내리면, OVS가 즉시 자기 배 속 스위칭 장부에 반영하여 수만 대의 VM을 마이크로 통제합니다.

### 2. 강력한 오버레이 [터널링](/knowledge-base/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/)(Overlay) 기능 흡수
- 앞서 배운 거대한 클라우드 망 포장 기술인 <strong><a href="/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/">VXLAN</a>, <a href="/knowledge-base/studynote/03_network/07_network_layer_routing/378_gre_generic_routing_encapsulation/">GRE</a>, <a href="/knowledge-base/studynote/03_network/16_data_center_cloud/819_stt_stateless_transport_tunneling_offload/">STT</a> (817~819번 <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">참조</a>)</strong> 터널을 만들고 뜯는 캡슐화 포장 작업을 OVS가 자체적으로 완벽하게 100% 하드캐리 해냅니다. OVS야말로 오버레이 클라우드 망의 진짜 노동자(VTEP)입니다.

### 3. [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 처리를 위한 Fast Path / Slow Path 분리 구조 🌟
- **Slow Path (vswitchd 데몬, 유저 스페이스)**: 처음 보는 낯선 패킷이 들어오면 OVS의 뇌(유저 공간 프로그램)가 [OpenFlow](/knowledge-base/studynote/03_network/17_sdn_nfv/855_openflow_standard_protocol_sdn_southbound/) 장부를 천천히 뒤적거려 길을 찾아냅니다. (느림)
- <strong>Fast Path (리눅스 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/">모듈</a> <a href="/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/205_datapath/">Datapath</a>)</strong>: 한 번 길을 찾은 패킷은 OVS가 그 길을 아예 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 깊숙한 바닥(캐시)에 하드코딩해 버립니다. 두 번째 들어오는 똑같은 패킷은 뇌로 올라오지 않고, <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> 바닥에서 0.001초 만에 튕겨서 목적지 VM으로 직행(Fast Path)</strong>합니다. 이 [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/) 마법 덕분에 소프트웨어 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)인데도 무지막지한 속도를 냅니다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">화이트박스 스위치</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">OVS</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">미니넷 SDN 토폴로지 에뮬레이터 연구 평가…</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: OVS의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

하지만 이 '[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 Fast Path' 마저도 10Gbps, 100Gbps 망이 열리자 리눅스 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 한계에 막혀 뻗기 시작했습니다(CPU 과부하 병목, 844번 문서).
- **진화**: 이를 해결하기 위해 OVS에 <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/671_dpdk/">DPDK</a>(<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 평면 개발 키트, 846번 문서)</strong> 흑마법을 합쳤습니다.
- 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 아예 쓰레기통에 버려 우회(Bypass)하고, OVS가 물리 랜카드에서 VM으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [폴링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)([Polling](/knowledge-base/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/)) 방식으로 직통 복사해 버리는 <strong>OVS-<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/671_dpdk/">DPDK</a></strong> 구조가 적용되면서, 클라우드의 가상 스위칭 속도가 하드웨어 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 뺨치는 괴물 같은 성능으로 진화했습니다.

OVS를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [화이트박스 스위치](/knowledge-base/studynote/03_network/17_sdn_nfv/859_whitebox_switch_open_hardware_nos/)가 기반 조건을 만든다면, OVS는 그 위에서 핵심 메커니즘을 구현하고, [미니넷](/knowledge-base/studynote/03_network/17_sdn_nfv/861_mininet_sdn_topology_network_emulator/) [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 토폴로지 에뮬레이터 연구 평가…는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성과 자동화 수준에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [화이트박스 스위치](/knowledge-base/studynote/03_network/17_sdn_nfv/859_whitebox_switch_open_hardware_nos/)의 기반 정리 | OVS의 핵심 동작 | [미니넷](/knowledge-base/studynote/03_network/17_sdn_nfv/861_mininet_sdn_topology_network_emulator/) [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 토폴로지 에뮬레이터 연구 평가…의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: 물리 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 도로 위를 달리는 '진짜 아스팔트 사거리 교차로'라면, <strong>OVS(<a href="/knowledge-base/studynote/02_operating_system/10_security/630_vswitch_vnf_overhead/">가상 스위치</a>)</strong>는 심시티 게임 속 컴퓨터 메모리 안에 지어놓은 완벽하게 정교한 '소프트웨어 사거리 교차로'입니다. 옛날엔 이 가짜 교차로에 신호등([방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/))도 없고 지하차도([VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) 터널)도 없는 빈약한 흙길 수준이었습니다. 하지만 OVS는 하늘에서 내려보는 중앙 교통관제센터([SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 컨트롤러)와 완벽하게 무전기([OpenFlow](/knowledge-base/studynote/03_network/17_sdn_nfv/855_openflow_standard_protocol_sdn_southbound/))로 대화하며, 즉각 즉각 가짜 도로의 신호등을 바꾸고 최첨단 터널을 파내는 '초고성능 소프트웨어 톨게이트'입니다. 게다가 맨날 지나가는 출퇴근 차량(Fast Path)은 하이패스 차선을 뚫어주고, 아예 리눅스 바닥을 갈아엎는 [DPDK](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/671_dpdk/) 마법까지 접목하여, 눈에 보이지 않는 가짜 소프트웨어 교차로 주제에 진짜 쇳덩어리 아스팔트 도로와 맞먹는 속도를 뽑아내는 클라우드 트래픽 통제의 심장입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 OVS를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [화이트박스 스위치](/knowledge-base/studynote/03_network/17_sdn_nfv/859_whitebox_switch_open_hardware_nos/) 수준의 기본 대책으로 충분한지, 아니면 OVS가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [미니넷](/knowledge-base/studynote/03_network/17_sdn_nfv/861_mininet_sdn_topology_network_emulator/) [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 토폴로지 에뮬레이터 연구 평가…와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성 부족인지, 자동화 수준 악화인지 먼저 분리한다.
2. OVS가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 [미니넷](/knowledge-base/studynote/03_network/17_sdn_nfv/861_mininet_sdn_topology_network_emulator/) [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 토폴로지 에뮬레이터 연구 평가…와의 연계 방식을 함께 검증한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- OVS의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [화이트박스 스위치](/knowledge-base/studynote/03_network/17_sdn_nfv/859_whitebox_switch_open_hardware_nos/)와의 경계를 정리하지 않아 중복 투자나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: OVS를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

OVS는 [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)/NFV를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [미니넷](/knowledge-base/studynote/03_network/17_sdn_nfv/861_mininet_sdn_topology_network_emulator/) [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 토폴로지 에뮬레이터 연구 평가…, 프로그래머블 네트워크, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 프로그래머블 네트워크 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: OVS는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [화이트박스 스위치](/knowledge-base/studynote/03_network/17_sdn_nfv/859_whitebox_switch_open_hardware_nos/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 제어 평면 (Control Plane) | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)과 경로 결정을 담당한다. |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 평면 ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Plane) | 실제 패킷 전달을 수행한다. |
| [미니넷](/knowledge-base/studynote/03_network/17_sdn_nfv/861_mininet_sdn_topology_network_emulator/) [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 토폴로지 에뮬레이터 연구 평가… | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">선행 개념: 화이트박스 스위치</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재 개념: OVS</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 A: 미니넷 SDN 토폴로지 에뮬레이터 연구 평가…</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 B: 프로그래머블 네트워크</div></div>
</div>
</div>



OVS는 [화이트박스 스위치](/knowledge-base/studynote/03_network/17_sdn_nfv/859_whitebox_switch_open_hardware_nos/)에서 출발해 현재 메커니즘을 정교화하고, 이후 [미니넷](/knowledge-base/studynote/03_network/17_sdn_nfv/861_mininet_sdn_topology_network_emulator/) [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 토폴로지 에뮬레이터 연구 평가…와 프로그래머블 네트워크 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감 차를 움직이는 조종기와 차체를 따로 생각하면 바꾸기 쉬워져요.
2. 이 개념은 네트워크의 머리와 몸을 나눠 더 쉽게 프로그램하게 해줘요.
3. 그래서 새 규칙을 더 빨리 넣고 바꿀 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 981 / 1120

← **이전**: [859. 화이트박스 스위치](/knowledge-base/studynote/03_network/17_sdn_nfv/859_whitebox_switch_open_hardware_nos/)
**다음**: [861. 미니넷 (Mininet)](/knowledge-base/studynote/03_network/17_sdn_nfv/861_mininet_sdn_topology_network_emulator/) →

---
