+++
weight = 100
title = "100. CNI (Container Network Interface) - 파드 간 오버레이 통신 표준"
date = "2026-04-10"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[822_cni_container_network_interface_kubernetes|CNI]] ([[194_container_virtualization_docker_namespace|Container]] Network Interface)는 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]]가 [[085_pod_kubernetes_container_unit|파드]]([[198_pod_kubernetes_minimum_deployment_unit|Pod]])에 IP를 할당하고 오버레이 통신망을 구성하는 과정을 외부 플러그인에게 위임하기 위한 표준 규격이다.
> 2. **가치**: K8s 본체의 수정 없이 Flannel의 단순한 캡슐화부터 Calico의 고성능 다이렉트 [[339_routing_overview_best_path_selection|라우팅]], Cilium의 [[615_ebpf|eBPF]] 기반 보안까지 인프라 환경에 맞는 네트워크 엔진을 선택할 수 있다.
> 3. **판단 포인트**: 클러스터 구축 시 트래픽 규모, [[007_security_policy|보안 정책]](Network [[164_policy|Policy]]) 필요성, 노드 간 물리적 [[339_routing_overview_best_path_selection|라우팅]] 환경을 종합적으로 고려하여 [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인을 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

[[822_cni_container_network_interface_kubernetes|CNI]] ([[194_container_virtualization_docker_namespace|Container]] Network Interface)는 K8s 클러스터 내에서 [[561_container_based_deployment|컨테이너]] 간의 네트워크 연결을 설정하고 삭제하는 공통 인터페이스다. [[196_kubernetes_k8s_container_orchestration|쿠버네티스]]는 자체적으로 네트워크를 구축하지 않고 "[[085_pod_kubernetes_container_unit|파드]]는 고유 IP를 가져야 하며, [[307_nat_network_address_translation_router_principles|NAT]] 없이 서로 통신해야 한다"는 원칙만 제시한다. 이 조건을 만족시키기 위해 외부 네트워크 솔루션들이 K8s와 연동될 수 있도록 만든 표준 구멍이 바로 CNI다.

이 표준이 필요한 이유는 K8s가 모든 인프라(AWS, [[061_on_premise_legacy_infrastructure|온프레미스]], 베어메탈)의 네트워크 장비와 [[339_routing_overview_best_path_selection|라우팅]] 방식을 직접 제어할 수 없기 때문이다. CNI가 없다면 K8s 코어 코드는 세상의 모든 네트워크 벤더 종속적인 [[339_routing_overview_best_path_selection|라우팅]] 규칙으로 비대해졌을 것이다. 따라서 네트워크 제어 권한을 [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인으로 분리함으로써 시스템의 확장성과 유지보수성을 확보했다.

- **📢 섹션 요약 비유**: CNI는 아파트 건물주(K8s)가 방마다 통신선을 직접 깔지 않고, 어떤 통신사(벤더)든 규격만 맞추면 모뎀을 꽂을 수 있게 만들어 둔 벽면 인터넷 콘센트다.

---

## Ⅱ. 아키텍처 및 핵심 원리

K8s의 Kubelet은 [[085_pod_kubernetes_container_unit|파드]]가 [[087_process_state_transition|생성]]될 때 [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인을 호출(ADD)하여 [[085_pod_kubernetes_container_unit|파드]]의 가상 네트워크 인터페이스(veth)를 [[087_process_state_transition|생성]]하고 IP를 할당한다. 이후 서로 다른 노드에 있는 [[085_pod_kubernetes_container_unit|파드]] 간 통신을 위해 CNI는 주로 [[815_overlay_network_virtualization_l2_extension|오버레이 네트워크]] ([[815_overlay_network_virtualization_l2_extension|Overlay Network]]) 캡슐화 기술을 사용한다.

| 구성 요소 | 역할 | 동작 방식 |
| :--- | :--- | :--- |
| **[[082_kubelet_node_agent|Kubelet]]** | [[085_pod_kubernetes_container_unit|파드]] 라이프사이클 관리 | [[085_pod_kubernetes_container_unit|파드]] [[087_process_state_transition|생성]]/삭제 시 [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 바이너리 실행 |
| **[[822_cni_container_network_interface_kubernetes|CNI]] 플러그인** | 실질적 네트워크 구성 | IPAM(IP 할당), veth [[087_process_state_transition|생성]], [[339_routing_overview_best_path_selection|라우팅]] 테이블 갱신 |
| **[[815_overlay_network_virtualization_l2_extension|Overlay Network]]** | 노드 간 논리적 통신망 | [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]], IPIP 등을 사용해 기존 물리망 위를 [[377_tunneling_mechanism_overview|터널링]] |

```text
┌──────────────────────────────────────────────────────────────┐
│                  오버레이 네트워크 캡슐화 통신 흐름                 │
├──────────────────────────────────────────────────────────────┤
│ Node 1 (IP: 192.168.1.10)              Node 2 (IP: 10.0.0.5) │
│ ┌───────────────┐                      ┌───────────────┐     │
│ │ Pod A (10.1.x)│──▶ [VXLAN 캡슐화] ──▶│ Pod B (10.2.x)│     │
│ └───────────────┘    (가짜 겉봉투 씌움)  └───────────────┘     │
│       │                                        ▲             │
│       ▼                                        │             │
│ [물리 라우터] ───── (192.168.1.10 ─▶ 10.0.0.5) ─────┘             │
└──────────────────────────────────────────────────────────────┘
```

물리 라우터는 [[085_pod_kubernetes_container_unit|파드]]의 가상 IP 대역을 모르기 때문에 패킷을 버린다. 따라서 CNI는 출발지와 목적지 물리 노드 IP를 적은 새 헤더로 원본 패킷을 감싸는 캡슐화 작업을 수행해 물리망을 통과시킨다. 

- **📢 섹션 요약 비유**: 오버레이 캡슐화는 우체국(라우터)이 모르는 비밀 주소([[085_pod_kubernetes_container_unit|파드]] IP)가 적힌 편지를, 우체국이 아는 합법적인 겉봉투(노드 IP)에 한 번 더 담아 보내는 특급 첩보 배송이다.

---

## Ⅲ. 비교 및 연결

[[822_cni_container_network_interface_kubernetes|CNI]] 플러그인은 기능의 무거움과 통신 방식에 따라 3세대로 나눌 수 있으며, 인프라의 요구사항에 따라 뚜렷한 경계를 가진다.

| 항목 | [[823_flannel_overlay_cni_vxlan|Flannel]] (플란넬) | [[824_calico_bgp_routing_cni_network_policy|Calico]] (칼리코) | [[825_cilium_ebpf_kubernetes_networking_security|Cilium]] (실리움) |
| :--- | :--- | :--- | :--- |
| **통신 방식** | [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] 기반 오버레이 | [[365_bgp_border_gateway_protocol_path_vector|BGP]] 기반 다이렉트 [[339_routing_overview_best_path_selection|라우팅]] (필요시 오버레이) | [[615_ebpf|eBPF]] (Extended [[069_ebpf|Berkeley Packet Filter]]) 기반 |
| **Network [[164_policy|Policy]]** | 미지원 (보안 통제 불가) | 완벽 지원 (L3/L4 [[690_firewall_generation_evolution|방화벽]]) | 완벽 지원 (L7 가시성 및 보안) |
| **[[282_performance_tactics|성능]] 및 복잡도** | [[282_performance_tactics|성능]] 낮음, 매우 단순함 | [[282_performance_tactics|성능]] 높음, 엔터프라이즈 표준 | 초고성능, 최신 [[022_kernel_role|커널]] 요구 |

Flannel은 단순 통신만 뚫어주기 때문에 소규모 개발망에 적합하다. 반면 Calico는 패킷 캡슐화 오버헤드를 없앤 [[365_bgp_border_gateway_protocol_path_vector|BGP]] 통신과 [[690_firewall_generation_evolution|방화벽]] [[164_policy|정책]]을 지원해 사실상의 산업 표준이 되었다. 최근에는 리눅스 [[022_kernel_role|커널]] 수준에서 네트워크를 낚아채는 [[615_ebpf|eBPF]] 기술을 적용한 Cilium이 차세대 CNI로 부상하고 있다.

- **📢 섹션 요약 비유**: Flannel은 신호등 없는 흙길, Calico는 경찰이 통제하는 8차선 고속도로, Cilium은 차를 띄워 하늘로 날려 보내는 최첨단 플라잉카 전용 튜브 도로다.

---

## Ⅳ. 실무 적용 및 기술사 판단

클러스터를 구축할 때 [[822_cni_container_network_interface_kubernetes|CNI]] 선택은 아키텍처의 근간을 결정하는 핵심 의사결정이다. 한 번 설치된 CNI를 운영 중에 교체하는 것은 전체 네트워크 단절을 의미하므로 [[459_quic_fec_forward_error_correction|초기]] 선택이 매우 중요하다.

### [[435_checklist_based_testing|체크리스트]]
1. **Network [[164_policy|Policy]] 필요 여부**: [[085_pod_kubernetes_container_unit|파드]] 간 통신을 차단하는 보안 규칙이 필요한가? (그렇다면 Flannel은 배제한다.)
2. **물리망 [[365_bgp_border_gateway_protocol_path_vector|BGP]] 연동 가능성**: 노드가 위치한 [[238_switch_operation_principles|스위치]] 장비가 [[365_bgp_border_gateway_protocol_path_vector|BGP]] [[339_routing_overview_best_path_selection|라우팅]]을 지원하는가? (지원한다면 Calico의 Non-Overlay 모드를 채택해 [[282_performance_tactics|성능]]을 극대화한다.)
3. **[[022_kernel_role|커널]] [[288_version_ihl_tos_total_length|버전]] 제약**: OS [[022_kernel_role|커널]]이 최신 eBPF를 지원할 만큼 최신 [[288_version_ihl_tos_total_length|버전]]인가? (구형 [[022_kernel_role|커널]]이라면 [[825_cilium_ebpf_kubernetes_networking_security|Cilium]] 도입을 보류해야 한다.)

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 보안이 중요한 금융권 망에서 [[282_performance_tactics|성능]]만 보고 Network Policy를 미지원하는 CNI를 채택하는 설계.
- 여러 리전에 걸친 노드 간 통신 환경에서 암호화([[589_ipsec_offload|IPsec]]/[[387_wireguard_vpn_modern_tunneling|WireGuard]]) 기능 없이 오버레이 터널만 뚫어 평문 통신을 방치하는 설계.

- **📢 섹션 요약 비유**: [[822_cni_container_network_interface_kubernetes|CNI]] 선택은 건물 기초 공사 시 배관 파이프의 굵기와 재질을 고르는 것과 같다. 나중에 배관을 갈아끼우려면 건물을 부수고 다시 지어야 한다.

---

## Ⅴ. 기대효과 및 결론

표준화된 [[822_cni_container_network_interface_kubernetes|CNI]] 규격을 도입함으로써 K8s는 플랫폼 자체의 결합도를 낮추고 거대한 [[385_third_party_cookie_deprecation_cdw|서드파티]] 네트워크 생태계를 만들어냈다. 관리자는 클러스터의 목적에 맞춰 가벼움, 보안, [[282_performance_tactics|성능]] 중 하나를 취사선택할 수 있게 되었다.

향후 K8s 네트워크 환경은 iptables와 kube-proxy의 [[282_performance_tactics|성능]] 병목을 완전히 제거하는 방향으로 진화할 것이다. 따라서 CNI의 발전 방향은 오버레이의 복잡도를 줄이고 [[615_ebpf|eBPF]] 같은 [[022_kernel_role|커널]] 네이티브 기술을 활용하여 [[282_performance_tactics|성능]]과 보안 가시성을 동시에 잡는 형태로 수렴할 것이다.

- **📢 섹션 요약 비유**: [[822_cni_container_network_interface_kubernetes|CNI]] 표준은 레고 블록의 규격이다. 규격만 맞으면 어떤 화려한 날개나 무기를 꽂아도 완벽하게 조립되어 작동한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **Kube-proxy** | [[090_service_kubernetes_network_load_balancing|서비스]]([[090_service_kubernetes_network_load_balancing|Service]]) IP를 실제 [[085_pod_kubernetes_container_unit|파드]]로 포워딩하는 노드 내 [[339_routing_overview_best_path_selection|라우팅]] 에이전트 |
| **Network [[164_policy|Policy]]** | [[085_pod_kubernetes_container_unit|파드]] 간의 트래픽 [[094_ingress_kubernetes_l7_routing_gateway|Ingress]]/Egress를 통제하는 K8s [[690_firewall_generation_evolution|방화벽]] 규칙 |
| **[[365_bgp_border_gateway_protocol_path_vector|BGP]] ([[365_bgp_border_gateway_protocol_path_vector|Border Gateway Protocol]])** | 노드 간 [[339_routing_overview_best_path_selection|라우팅]] 정보를 교환하여 캡슐화 없이 통신하게 해주는 [[295_protocol_field_tcp_udp_icmp|프로토콜]] |
| **[[615_ebpf|eBPF]]** | 리눅스 [[022_kernel_role|커널]] 소스 수정 없이 [[022_kernel_role|커널]] 공간에서 샌드박스화된 코드를 실행하는 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
Underlay Network 한계 (물리 라우터 파드 IP 인식 불가)
    │
    ▼
오버레이 네트워크 캡슐화 (VXLAN, IPIP) · Flannel
    │
    ▼
CNI (Container Network Interface) 표준화
    │
    ▼
다이렉트 라우팅 및 보안 규칙 (BGP, Network Policy) · Calico
    │
    ▼
커널 네이티브 네트워크 가속 및 가시성 확보 (eBPF) · Cilium
```

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 세상에는 여러 아파트(노드)가 있고, 아파트 안에는 수많은 방([[085_pod_kubernetes_container_unit|파드]])이 있어요.
2. 서로 다른 아파트에 있는 방끼리 비밀 전화를 걸려면, 동네 우체국이 모르는 주소를 알아서 전달해 줄 똑똑한 전화국 직원이 필요해요.
3. CNI는 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 건물주가 고용한 전화국 직원으로, 플란넬, 칼리코 같은 여러 회사 중 우리 아파트에 가장 잘 맞는 직원을 골라 쓸 수 있답니다.
