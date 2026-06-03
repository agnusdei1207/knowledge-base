---
title: 363. SDN SDDC VXLAN 논리망 오버레이 통신 제어망 (SDN SDDC VXLAN Logical Network Overlay
  and Control Plane)
date: '2026-05-09'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[633_sdn_whitebox|SDN]] (Software-Defined Networking)은 네트워크의 제어 평면(Control Plane)과 [[001_dikw_pyramid|데이터]] 평면([[001_dikw_pyramid|Data]] Plane)을 분리해 소프트웨어로 네트워크 [[164_policy|정책]]을 중앙에서 프로그래밍하는 패러다임이며, [[631_sddc|SDDC]] ([[023_sddc_software_defined_data_center|Software-Defined Data Center]])는 이를 스토리지·컴퓨팅까지 확장한 개념이다.
> 2. **가치**: [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] ([[817_vxlan_virtual_extensible_lan_mac_in_udp|Virtual Extensible LAN]])은 [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] [[377_tunneling_mechanism_overview|터널링]]으로 물리 네트워크(Underlay) 위에 [[369_logic_bomb|논리]] 네트워크(Overlay)를 구성해, VLAN의 4,096개 한계를 16,777,214개(VNI 24비트)로 확장하고 [[310_multi_tenant_database_architecture|멀티테넌트]] 클라우드의 네트워크 격리를 해결한다.
> 3. **판단 포인트**: [[365_bgp_border_gateway_protocol_path_vector|BGP]] [[820_evpn_ethernet_vpn_bgp_control_plane|EVPN]] ([[820_evpn_ethernet_vpn_bgp_control_plane|Ethernet VPN]])을 [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] 제어 평면으로 사용하면 [[673_mac_message_authentication_code|MAC]]/IP 주소 학습을 플러드 없이 수행해 동-서(East-West) 트래픽 최적화와 멀티테넌시 보안 격리를 동시에 달성한다.

---

## Ⅰ. 개요 및 필요성

전통 네트워크는 각 [[238_switch_operation_principles|스위치]]·라우터가 자체 제어 평면을 운영해 [[136_variance|분산]] 관리됐다. 새 [[164_policy|정책]] 적용 시 수백 개 장비를 개별 [[009_config|설정]]해야 해 변경 속도가 느리고 오류 가능성이 높다.

[[224_vlan_virtual_lan_broadcast_domain|VLAN]] ([[224_vlan_virtual_lan_broadcast_domain|Virtual LAN]])은 IEEE 802.1Q 기준 12비트 [[224_vlan_virtual_lan_broadcast_domain|VLAN]] ID로 4,096개 세그먼트가 최대다. 수십만 테넌트를 운영하는 클라우드 환경에서는 절대적으로 부족하다. VXLAN은 24비트 VNI를 사용해 약 1,600만 개의 [[369_logic_bomb|논리]] 네트워크 세그먼트를 제공한다.

- 📢 섹션 요약 비유: SDN은 도시 교통관제센터다. 모든 [[130_signal|신호]]등([[238_switch_operation_principles|스위치]])이 중앙관제센터([[633_sdn_whitebox|SDN]] Controller) 지시를 따르므로, 교통 정체 시 모든 [[130_signal|신호]]를 한 번에 조정할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
┌──────────────────────────────────────────────────────────────────┐
│              VXLAN 오버레이 구조                                  │
├──────────────────────────────────────────────────────────────────┤
│  [VM A] ─────────────────────────────── [VM B]                  │
│  논리 네트워크 (Overlay, VNI=10001)                               │
│    │                                       │                    │
│  [VTEP A]                               [VTEP B]               │
│  VXLAN 터널 엔드포인트                  VXLAN 터널 엔드포인트    │
│    └── UDP/IP 캡슐화 ──▶ [물리 네트워크] ──▶ 역캡슐화 ──────────┘│
│                                                                  │
│  VXLAN 헤더: Outer IP + Outer UDP (4789) + VXLAN (VNI 24bit)   │
└──────────────────────────────────────────────────────────────────┘
```

| 항목           | [[224_vlan_virtual_lan_broadcast_domain|VLAN]]                  | [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]]                          |
| :------------- | :-------------------- | :----------------------------- |
| 세그먼트 수    | 4,096 (12비트)        | 16,777,214 (24비트)            |
| 캡슐화         | 802.1Q 태그           | [[406_udp_user_datagram_protocol_connectionless_fast|UDP]]/IP 터널 ([[446_port_and_bus|포트]] 4789)        |
| 제어 평면      | [[570_stp_vs_mtp|STP]] ([[959_spanning_tree_protocol_stp_loop_avoidance|스패닝 트리]])     | [[365_bgp_border_gateway_protocol_path_vector|BGP]] [[820_evpn_ethernet_vpn_bgp_control_plane|EVPN]] (권장)                |
| 멀티테넌시     | [[224_vlan_virtual_lan_broadcast_domain|VLAN]] 공유             | VNI별 완전 격리                |

**[[365_bgp_border_gateway_protocol_path_vector|BGP]] [[820_evpn_ethernet_vpn_bgp_control_plane|EVPN]]**: [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] 제어 평면으로, [[673_mac_message_authentication_code|MAC]]/IP 주소를 [[365_bgp_border_gateway_protocol_path_vector|BGP]] 업데이트로 배포해 VTEP 간 플러드(Flood & Learn) 없이 [[673_mac_message_authentication_code|MAC]] 학습을 수행한다.

**[[631_sddc|SDDC]]**: [[633_sdn_whitebox|SDN]] + [[632_sds|SDS]] + [[015_virtualization|가상화]] 컴퓨팅을 통합해 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 전체를 소프트웨어로 [[198_abstraction_control_data_process|추상화]]한다. VMware NSX + vSAN + vSphere가 대표 [[631_sddc|SDDC]] 구현이다.

- 📢 섹션 요약 비유: VXLAN은 물리 도로(Underlay) 위에 가상의 전용 도로(Overlay)를 추가로 그리는 것이다. 테넌트마다 전용 도로를 할당해 완전히 분리된 길을 달릴 수 있다.

---

## Ⅲ. 비교 및 연결

| 항목           | 전통 네트워크           | [[633_sdn_whitebox|SDN]]                           | [[631_sddc|SDDC]]                           |
| :------------- | :---------------------- | :---------------------------- | :----------------------------- |
| 제어 방식      | [[136_variance|분산]] (장비별 독립)      | 중앙 집중 (Controller)        | 중앙 집중 + 자동화             |
| 멀티테넌시     | [[224_vlan_virtual_lan_broadcast_domain|VLAN]] 한계               | [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] VNI 대규모 격리          | [[164_policy|정책]] 기반 테넌트 격리          |

[[205_kubernetes_container_orchestration|Kubernetes]] [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인([[825_cilium_ebpf_kubernetes_networking_security|Cilium]], [[824_calico_bgp_routing_cni_network_policy|Calico]])은 [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] 또는 [[365_bgp_border_gateway_protocol_path_vector|BGP]] 기반으로 [[085_pod_kubernetes_container_unit|파드]] 네트워크를 구성한다. Cilium은 [[615_ebpf|eBPF]] 기반으로 [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] 오버헤드 없이 직접 [[339_routing_overview_best_path_selection|라우팅]]해 레이턴시를 개선한다.

- 📢 섹션 요약 비유: [[633_sdn_whitebox|SDN]] 컨트롤러는 항공 관제센터다. 각 비행기(패킷)가 어느 경로를 날지를 지상에서 중앙 지시로 최적화한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**[[633_sdn_whitebox|SDN]]/[[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] 설계 [[435_checklist_based_testing|체크리스트]]**
1. VTEP 위치: [[054_hypervisor|하이퍼바이저]](소프트웨어 VTEP) vs 물리 [[238_switch_operation_principles|스위치]](하드웨어 VTEP) 선택
2. [[365_bgp_border_gateway_protocol_path_vector|BGP]] [[820_evpn_ethernet_vpn_bgp_control_plane|EVPN]] 제어 평면 적용으로 플러드 트래픽 제거
3. MTU [[009_config|설정]]: [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] 오버헤드 50바이트를 고려해 물리 인터페이스 MTU를 1600 이상으로 [[009_config|설정]]
4. VNI 네이밍 규칙 정의: 테넌트·환경(prod/dev)·[[224_vlan_virtual_lan_broadcast_domain|VLAN]] ID 매핑 문서화

**[[128_water_scrum_fall_anti_pattern|안티패턴]]**
- [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] MTU 미설정 → 패킷 [[291_fragmentation_and_reassembly_process|단편화]]로 [[282_performance_tactics|성능]] 저하
- [[365_bgp_border_gateway_protocol_path_vector|BGP]] [[820_evpn_ethernet_vpn_bgp_control_plane|EVPN]] 없이 플러드 모드 → 브로드캐스트 폭풍
- [[633_sdn_whitebox|SDN]] Controller [[454_spof|단일 장애점]](Single Point of Failure) 구성

- 📢 섹션 요약 비유: [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] MTU [[009_config|설정]] 실수는 편지봉투(패킷)보다 편지([[001_dikw_pyramid|데이터]])가 커서 구겨 넣는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

[[633_sdn_whitebox|SDN]] + [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] + [[365_bgp_border_gateway_protocol_path_vector|BGP]] [[820_evpn_ethernet_vpn_bgp_control_plane|EVPN]] 조합은 클라우드 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]의 네트워크 자동화·확장성·멀티테넌시 문제를 동시에 해결한다. 대형 CSP들이 이 조합을 기반으로 수백만 테넌트 네트워크를 자동화된 API로 운영한다.

미래는 [[615_ebpf|eBPF]] 기반 네트워킹([[825_cilium_ebpf_kubernetes_networking_security|Cilium]])과 AI가 [[633_sdn_whitebox|SDN]] [[164_policy|정책]]을 자동 [[087_process_state_transition|생성]]하는 [[416_prompt_injection_semantic_routing|Intent]]-Based Networking([[857_ibn_intent_based_networking_declarative_automation|IBN]]) 방향이다.

- 📢 섹션 요약 비유: SDDC는 도시 전체를 디지털 쌍둥이로 복사한 것과 같다. 물리 도시(하드웨어)는 그대로 두고, 디지털 시뮬레이션에서 모든 변경을 먼저 테스트한 후 실제에 적용한다.

---

### 📌 관련 개념 맵

| 개념                                    | 연결 포인트                                               |
| :-------------------------------------- | :-------------------------------------------------------- |
| [[855_openflow_standard_protocol_sdn_southbound|OpenFlow]]                                | [[633_sdn_whitebox|SDN]] [[459_quic_fec_forward_error_correction|초기]] 표준 [[295_protocol_field_tcp_udp_icmp|프로토콜]], 컨트롤러-[[238_switch_operation_principles|스위치]] 통신             |
| VTEP ([[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] Tunnel EndPoint)            | [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] 캡슐화/역캡슐화 수행 [[369_logic_bomb|논리]] 엔드포인트               |
| [[365_bgp_border_gateway_protocol_path_vector|BGP]] [[820_evpn_ethernet_vpn_bgp_control_plane|EVPN]] ([[820_evpn_ethernet_vpn_bgp_control_plane|Ethernet VPN]])                 | [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] 제어 평면, [[673_mac_message_authentication_code|MAC]]/IP 무플러드 학습                    |
| NSX-T (VMware)                          | [[631_sddc|SDDC]] 대표 솔루션, 마이크로세그멘테이션 제공              |
| [[825_cilium_ebpf_kubernetes_networking_security|Cilium]] ([[615_ebpf|eBPF]])                           | [[205_kubernetes_container_orchestration|Kubernetes]] [[822_cni_container_network_interface_kubernetes|CNI]], [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] 대체 직접 [[339_routing_overview_best_path_selection|라우팅]]                   |

### 📈 관련 키워드 및 발전 흐름도

```text
전통 VLAN (4,096 세그먼트 한계)
    │
    ▼
OpenFlow + SDN Controller — 제어/데이터 평면 분리
    │
    ▼
VXLAN (24비트 VNI, 16M 세그먼트) — 멀티테넌트 확장
    │
    ▼
BGP EVPN — VXLAN 제어 평면, 플러드 제거
    │
    ▼
SDDC (NSX-T + vSAN + vSphere) — 전체 데이터센터 추상화
    │
    ▼
eBPF (Cilium) — 오버레이 없는 직접 네트워킹
```

### 👶 어린이를 위한 3줄 비유 설명

1. SDN은 모든 교통신호를 중앙에서 컴퓨터로 조종하는 스마트 교통 관제 시스템이에요.
2. VXLAN은 물리적 도로 위에 가상의 전용차선을 그려서 각 회사(테넌트)가 자기만의 길을 달릴 수 있게 해요.
3. SDDC는 건물(하드웨어) 위에 유리 천막(소프트웨어)을 덮어서 안에서 모든 것을 자유롭게 바꿀 수 있는 구조예요.
