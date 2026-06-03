+++
title = "363. SDN SDDC VXLAN 논리망 오버레이 통신 제어망 (SDN SDDC VXLAN Logical Network Overlay and Control Plane)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) (Software-Defined Networking)은 네트워크의 제어 평면(Control Plane)과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 평면([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Plane)을 분리해 소프트웨어로 네트워크 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 중앙에서 프로그래밍하는 패러다임이며, [SDDC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/631_sddc/) ([Software-Defined Data Center](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/023_sddc_software_defined_data_center/))는 이를 스토리지·컴퓨팅까지 확장한 개념이다.
> 2. **가치**: [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) ([Virtual Extensible LAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/))은 [UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) [터널링](/knowledge-base/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/)으로 물리 네트워크(Underlay) 위에 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 네트워크(Overlay)를 구성해, VLAN의 4,096개 한계를 16,777,214개(VNI 24비트)로 확장하고 [멀티테넌트](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/310_multi_tenant_database_architecture/) 클라우드의 네트워크 격리를 해결한다.
> 3. **판단 포인트**: [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [EVPN](/knowledge-base/studynote/03_network/16_data_center_cloud/820_evpn_ethernet_vpn_bgp_control_plane/) ([Ethernet VPN](/knowledge-base/studynote/03_network/16_data_center_cloud/820_evpn_ethernet_vpn_bgp_control_plane/))을 [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) 제어 평면으로 사용하면 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)/IP 주소 학습을 플러드 없이 수행해 동-서(East-West) 트래픽 최적화와 멀티테넌시 보안 격리를 동시에 달성한다.

---

## Ⅰ. 개요 및 필요성

전통 네트워크는 각 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)·라우터가 자체 제어 평면을 운영해 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 관리됐다. 새 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 적용 시 수백 개 장비를 개별 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)해야 해 변경 속도가 느리고 오류 가능성이 높다.

[VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) ([Virtual LAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/))은 IEEE 802.1Q 기준 12비트 [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) ID로 4,096개 세그먼트가 최대다. 수십만 테넌트를 운영하는 클라우드 환경에서는 절대적으로 부족하다. VXLAN은 24비트 VNI를 사용해 약 1,600만 개의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 네트워크 세그먼트를 제공한다.

- 📢 섹션 요약 비유: SDN은 도시 교통관제센터다. 모든 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)등([스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/))이 중앙관제센터([SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) Controller) 지시를 따르므로, 교통 정체 시 모든 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 한 번에 조정할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">VXLAN 오버레이 구조</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">VM A</div><div class="kb-diagram-node">VM B</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">논리 네트워크 (Overlay, VNI=10001)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">VTEP A</div><div class="kb-diagram-node">VTEP B</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">VXLAN 터널 엔드포인트 VXLAN 터널 엔드포인트</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">물리 네트워크</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-note">역캡슐화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">VXLAN 헤더: Outer IP + Outer UDP (4789) + VXLAN (VNI 24bit)</div></div>
</div>
</div>



| 항목           | [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/)                  | [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/)                          |
| :------------- | :-------------------- | :----------------------------- |
| 세그먼트 수    | 4,096 (12비트)        | 16,777,214 (24비트)            |
| 캡슐화         | 802.1Q 태그           | [UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/)/IP 터널 ([포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 4789)        |
| 제어 평면      | [STP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) ([스패닝 트리](/knowledge-base/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/))     | [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [EVPN](/knowledge-base/studynote/03_network/16_data_center_cloud/820_evpn_ethernet_vpn_bgp_control_plane/) (권장)                |
| 멀티테넌시     | [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 공유             | VNI별 완전 격리                |

<strong><a href="/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/">BGP</a> <a href="/knowledge-base/studynote/03_network/16_data_center_cloud/820_evpn_ethernet_vpn_bgp_control_plane/">EVPN</a></strong>: [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) 제어 평면으로, [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)/IP 주소를 [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 업데이트로 배포해 VTEP 간 플러드(Flood & Learn) 없이 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 학습을 수행한다.

<strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/631_sddc/">SDDC</a></strong>: [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) + [SDS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/632_sds/) + [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 컴퓨팅을 통합해 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 전체를 소프트웨어로 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)한다. VMware NSX + vSAN + vSphere가 대표 [SDDC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/631_sddc/) 구현이다.

- 📢 섹션 요약 비유: VXLAN은 물리 도로(Underlay) 위에 가상의 전용 도로(Overlay)를 추가로 그리는 것이다. 테넌트마다 전용 도로를 할당해 완전히 분리된 길을 달릴 수 있다.

---

## Ⅲ. 비교 및 연결

| 항목           | 전통 네트워크           | [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)                           | [SDDC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/631_sddc/)                           |
| :------------- | :---------------------- | :---------------------------- | :----------------------------- |
| 제어 방식      | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) (장비별 독립)      | 중앙 집중 (Controller)        | 중앙 집중 + 자동화             |
| 멀티테넌시     | [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 한계               | [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) VNI 대규모 격리          | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 기반 테넌트 격리          |

[Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) [CNI](/knowledge-base/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인([Cilium](/knowledge-base/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/), [Calico](/knowledge-base/studynote/03_network/16_data_center_cloud/824_calico_bgp_routing_cni_network_policy/))은 [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) 또는 [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 기반으로 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 네트워크를 구성한다. Cilium은 [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 기반으로 [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) 오버헤드 없이 직접 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)해 레이턴시를 개선한다.

- 📢 섹션 요약 비유: [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 컨트롤러는 항공 관제센터다. 각 비행기(패킷)가 어느 경로를 날지를 지상에서 중앙 지시로 최적화한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/">SDN</a>/<a href="/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/">VXLAN</a> 설계 <a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/">체크리스트</a></strong>
1. VTEP 위치: [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)(소프트웨어 VTEP) vs 물리 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)(하드웨어 VTEP) 선택
2. [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [EVPN](/knowledge-base/studynote/03_network/16_data_center_cloud/820_evpn_ethernet_vpn_bgp_control_plane/) 제어 평면 적용으로 플러드 트래픽 제거
3. MTU [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/): [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) 오버헤드 50바이트를 고려해 물리 인터페이스 MTU를 1600 이상으로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)
4. VNI 네이밍 규칙 정의: 테넌트·환경(prod/dev)·[VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) ID 매핑 문서화

<strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>
- [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) MTU 미설정 → 패킷 [단편화](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)로 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하
- [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [EVPN](/knowledge-base/studynote/03_network/16_data_center_cloud/820_evpn_ethernet_vpn_bgp_control_plane/) 없이 플러드 모드 → 브로드캐스트 폭풍
- [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) Controller [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)(Single Point of Failure) 구성

- 📢 섹션 요약 비유: [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) MTU [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 실수는 편지봉투(패킷)보다 편지([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 커서 구겨 넣는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

[SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) + [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) + [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [EVPN](/knowledge-base/studynote/03_network/16_data_center_cloud/820_evpn_ethernet_vpn_bgp_control_plane/) 조합은 클라우드 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)의 네트워크 자동화·확장성·멀티테넌시 문제를 동시에 해결한다. 대형 CSP들이 이 조합을 기반으로 수백만 테넌트 네트워크를 자동화된 API로 운영한다.

미래는 [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 기반 네트워킹([Cilium](/knowledge-base/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/))과 AI가 [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 [Intent](/knowledge-base/studynote/06_ict_convergence/05_data_science/416_prompt_injection_semantic_routing/)-Based Networking([IBN](/knowledge-base/studynote/03_network/17_sdn_nfv/857_ibn_intent_based_networking_declarative_automation/)) 방향이다.

- 📢 섹션 요약 비유: SDDC는 도시 전체를 디지털 쌍둥이로 복사한 것과 같다. 물리 도시(하드웨어)는 그대로 두고, 디지털 시뮬레이션에서 모든 변경을 먼저 테스트한 후 실제에 적용한다.

---

### 📌 관련 개념 맵

| 개념                                    | 연결 포인트                                               |
| :-------------------------------------- | :-------------------------------------------------------- |
| [OpenFlow](/knowledge-base/studynote/03_network/17_sdn_nfv/855_openflow_standard_protocol_sdn_southbound/)                                | [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 표준 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/), 컨트롤러-[스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 통신             |
| VTEP ([VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) Tunnel EndPoint)            | [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) 캡슐화/역캡슐화 수행 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 엔드포인트               |
| [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [EVPN](/knowledge-base/studynote/03_network/16_data_center_cloud/820_evpn_ethernet_vpn_bgp_control_plane/) ([Ethernet VPN](/knowledge-base/studynote/03_network/16_data_center_cloud/820_evpn_ethernet_vpn_bgp_control_plane/))                 | [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) 제어 평면, [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)/IP 무플러드 학습                    |
| NSX-T (VMware)                          | [SDDC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/631_sddc/) 대표 솔루션, 마이크로세그멘테이션 제공              |
| [Cilium](/knowledge-base/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/) ([eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/))                           | [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) [CNI](/knowledge-base/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/), [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) 대체 직접 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)                   |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">전통 VLAN (4,096 세그먼트 한계)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">OpenFlow + SDN Controller — 제어/데이터 평면 분리</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">VXLAN (24비트 VNI, 16M 세그먼트) — 멀티테넌트 확장</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">BGP EVPN — VXLAN 제어 평면, 플러드 제거</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">SDDC (NSX-T + vSAN + vSphere) — 전체 데이터센터 추상화</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">eBPF (Cilium) — 오버레이 없는 직접 네트워킹</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. SDN은 모든 교통신호를 중앙에서 컴퓨터로 조종하는 스마트 교통 관제 시스템이에요.
2. VXLAN은 물리적 도로 위에 가상의 전용차선을 그려서 각 회사(테넌트)가 자기만의 길을 달릴 수 있게 해요.
3. SDDC는 건물(하드웨어) 위에 유리 천막(소프트웨어)을 덮어서 안에서 모든 것을 자유롭게 바꿀 수 있는 구조예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 363 / 373

← **이전**: [362. O-RAN 프론트홀 화이트박스 분리 아키텍처 (O-RAN Open Radio Access Network Fronthaul Whitebox](/knowledge-base/studynote/15_devops_sre/05_devsecops/362_o_ran/)
**다음**: [364. 멀티클러스터 쿠버네티스 페더레이션 고가용성 배포 (Multi-cluster Kubernetes Federation High-Availability](/knowledge-base/studynote/15_devops_sre/05_devsecops/364_process/) →

---
