---
title: "100. Cni Container Network Interface Flannel Calico"
date: "2026-04-10"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) ([Container](/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/) Network Interface)는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)가 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))에 IP를 할당하고 오버레이 통신망을 구성하는 과정을 외부 플러그인에게 위임하기 위한 표준 규격이다.
> 2. **가치**: K8s 본체의 수정 없이 Flannel의 단순한 캡슐화부터 Calico의 고성능 다이렉트 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), Cilium의 [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) 기반 보안까지 인프라 환경에 맞는 네트워크 엔진을 선택할 수 있다.
> 3. **판단 포인트**: 클러스터 구축 시 트래픽 규모, [보안 정책](/studynote/09_security/01_intro_principles/007_security_policy/)(Network [Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/)) 필요성, 노드 간 물리적 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 환경을 종합적으로 고려하여 [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인을 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

[CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) ([Container](/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/) Network Interface)는 K8s 클러스터 내에서 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 간의 네트워크 연결을 설정하고 삭제하는 공통 인터페이스다. [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)는 자체적으로 네트워크를 구축하지 않고 "[파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)는 고유 IP를 가져야 하며, [NAT](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) 없이 서로 통신해야 한다"는 원칙만 제시한다. 이 조건을 만족시키기 위해 외부 네트워크 솔루션들이 K8s와 연동될 수 있도록 만든 표준 구멍이 바로 CNI다.

이 표준이 필요한 이유는 K8s가 모든 인프라(AWS, [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/), 베어메탈)의 네트워크 장비와 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 방식을 직접 제어할 수 없기 때문이다. CNI가 없다면 K8s 코어 코드는 세상의 모든 네트워크 벤더 종속적인 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 규칙으로 비대해졌을 것이다. 따라서 네트워크 제어 권한을 [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인으로 분리함으로써 시스템의 확장성과 유지보수성을 확보했다.

- **📢 섹션 요약 비유**: CNI는 아파트 건물주(K8s)가 방마다 통신선을 직접 깔지 않고, 어떤 통신사(벤더)든 규격만 맞추면 모뎀을 꽂을 수 있게 만들어 둔 벽면 인터넷 콘센트다.

---

## Ⅱ. 아키텍처 및 핵심 원리

K8s의 Kubelet은 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)될 때 [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인을 호출(ADD)하여 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)의 가상 네트워크 인터페이스(veth)를 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고 IP를 할당한다. 이후 서로 다른 노드에 있는 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 통신을 위해 CNI는 주로 [오버레이 네트워크](/studynote/03_network/16_data_center_cloud/815_overlay_network_virtualization_l2_extension/) ([Overlay Network](/studynote/03_network/16_data_center_cloud/815_overlay_network_virtualization_l2_extension/)) 캡슐화 기술을 사용한다.

| 구성 요소 | 역할 | 동작 방식 |
| :--- | :--- | :--- |
| <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/082_kubelet_node_agent/">Kubelet</a></strong> | [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 라이프사이클 관리 | [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)/삭제 시 [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 바이너리 실행 |
| <strong><a href="/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/">CNI</a> 플러그인</strong> | 실질적 네트워크 구성 | IPAM(IP 할당), veth [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 테이블 갱신 |
| <strong><a href="/studynote/03_network/16_data_center_cloud/815_overlay_network_virtualization_l2_extension/">Overlay Network</a></strong> | 노드 간 논리적 통신망 | [VXLAN](/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/), IPIP 등을 사용해 기존 물리망 위를 [터널링](/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/) |

```text
+--------------------------------------------------------------+
|                  오버레이 네트워크 캡슐화 통신 흐름                 |
+--------------------------------------------------------------+
| Node 1 (IP: 192.168.1.10)              Node 2 (IP: 10.0.0.5) |
| +---------------+                      +---------------+     |
| | Pod A (10.1.x)|---> [VXLAN 캡슐화] --->| Pod B (10.2.x)|     |
| +---------------+    (가짜 겉봉투 씌움)  +---------------+     |
|       |                                        ^             |
|       v                                        |             |
| [물리 라우터] ----- (192.168.1.10 --> 10.0.0.5) -----+             |
+--------------------------------------------------------------+
```

물리 라우터는 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)의 가상 IP 대역을 모르기 때문에 패킷을 버린다. 따라서 CNI는 출발지와 목적지 물리 노드 IP를 적은 새 헤더로 원본 패킷을 감싸는 캡슐화 작업을 수행해 물리망을 통과시킨다.

- **📢 섹션 요약 비유**: 오버레이 캡슐화는 우체국(라우터)이 모르는 비밀 주소([파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) IP)가 적힌 편지를, 우체국이 아는 합법적인 겉봉투(노드 IP)에 한 번 더 담아 보내는 특급 첩보 배송이다.

---

## Ⅲ. 비교 및 연결

[CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인은 기능의 무거움과 통신 방식에 따라 3세대로 나눌 수 있으며, 인프라의 요구사항에 따라 뚜렷한 경계를 가진다.

| 항목 | [Flannel](/studynote/03_network/16_data_center_cloud/823_flannel_overlay_cni_vxlan/) (플란넬) | [Calico](/studynote/03_network/16_data_center_cloud/824_calico_bgp_routing_cni_network_policy/) (칼리코) | [Cilium](/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/) (실리움) |
| :--- | :--- | :--- | :--- |
| **통신 방식** | [VXLAN](/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) 기반 오버레이 | [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 기반 다이렉트 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) (필요시 오버레이) | [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) (Extended [Berkeley Packet Filter](/studynote/02_operating_system/01_overview_architecture/069_ebpf/)) 기반 |
| <strong>Network <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">Policy</a></strong> | 미지원 (보안 통제 불가) | 완벽 지원 (L3/L4 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)) | 완벽 지원 (L7 가시성 및 보안) |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 및 복잡도</strong> | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 낮음, 매우 단순함 | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 높음, 엔터프라이즈 표준 | 초고성능, 최신 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 요구 |

Flannel은 단순 통신만 뚫어주기 때문에 소규모 개발망에 적합하다. 반면 Calico는 패킷 캡슐화 오버헤드를 없앤 [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 통신과 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 지원해 사실상의 산업 표준이 되었다. 최근에는 리눅스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수준에서 네트워크를 낚아채는 [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) 기술을 적용한 Cilium이 차세대 CNI로 부상하고 있다.

- **📢 섹션 요약 비유**: Flannel은 신호등 없는 흙길, Calico는 경찰이 통제하는 8차선 고속도로, Cilium은 차를 띄워 하늘로 날려 보내는 최첨단 플라잉카 전용 튜브 도로다.

---

## Ⅳ. 실무 적용 및 기술사 판단

클러스터를 구축할 때 [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 선택은 아키텍처의 근간을 결정하는 핵심 의사결정이다. 한 번 설치된 CNI를 운영 중에 교체하는 것은 전체 네트워크 단절을 의미하므로 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 선택이 매우 중요하다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. <strong>Network <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">Policy</a> 필요 여부</strong>: [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 통신을 차단하는 보안 규칙이 필요한가? (그렇다면 Flannel은 배제한다.)
2. <strong>물리망 <a href="/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/">BGP</a> 연동 가능성</strong>: 노드가 위치한 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 장비가 [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)을 지원하는가? (지원한다면 Calico의 Non-Overlay 모드를 채택해 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 극대화한다.)
3. <strong><a href="/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> <a href="/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a> 제약</strong>: OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 최신 eBPF를 지원할 만큼 최신 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)인가? (구형 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이라면 [Cilium](/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/) 도입을 보류해야 한다.)

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 보안이 중요한 금융권 망에서 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)만 보고 Network Policy를 미지원하는 CNI를 채택하는 설계.
- 여러 리전에 걸친 노드 간 통신 환경에서 암호화([IPsec](/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/)/[WireGuard](/studynote/03_network/07_network_layer_routing/387_wireguard_vpn_modern_tunneling/)) 기능 없이 오버레이 터널만 뚫어 평문 통신을 방치하는 설계.

- **📢 섹션 요약 비유**: [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 선택은 건물 기초 공사 시 배관 파이프의 굵기와 재질을 고르는 것과 같다. 나중에 배관을 갈아끼우려면 건물을 부수고 다시 지어야 한다.

---

## Ⅴ. 기대효과 및 결론

표준화된 [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 규격을 도입함으로써 K8s는 플랫폼 자체의 결합도를 낮추고 거대한 [서드파티](/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) 네트워크 생태계를 만들어냈다. 관리자는 클러스터의 목적에 맞춰 가벼움, 보안, [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 중 하나를 취사선택할 수 있게 되었다.

향후 K8s 네트워크 환경은 iptables와 kube-proxy의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목을 완전히 제거하는 방향으로 진화할 것이다. 따라서 CNI의 발전 방향은 오버레이의 복잡도를 줄이고 [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) 같은 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 네이티브 기술을 활용하여 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 보안 가시성을 동시에 잡는 형태로 수렴할 것이다.

- **📢 섹션 요약 비유**: [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 표준은 레고 블록의 규격이다. 규격만 맞으면 어떤 화려한 날개나 무기를 꽂아도 완벽하게 조립되어 작동한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **Kube-proxy** | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) IP를 실제 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)로 포워딩하는 노드 내 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 에이전트 |
| <strong>Network <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">Policy</a></strong> | [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간의 트래픽 [Ingress](/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/)/Egress를 통제하는 K8s [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 규칙 |
| <strong><a href="/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/">BGP</a> (<a href="/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/">Border Gateway Protocol</a>)</strong> | 노드 간 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 정보를 교환하여 캡슐화 없이 통신하게 해주는 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
| <strong><a href="/studynote/02_operating_system/10_security/615_ebpf/">eBPF</a></strong> | 리눅스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 소스 수정 없이 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 공간에서 샌드박스화된 코드를 실행하는 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
Underlay Network 한계 (물리 라우터 파드 IP 인식 불가)
    |
    v
오버레이 네트워크 캡슐화 (VXLAN, IPIP) · Flannel
    |
    v
CNI (Container Network Interface) 표준화
    |
    v
다이렉트 라우팅 및 보안 규칙 (BGP, Network Policy) · Calico
    |
    v
커널 네이티브 네트워크 가속 및 가시성 확보 (eBPF) · Cilium
```

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 세상에는 여러 아파트(노드)가 있고, 아파트 안에는 수많은 방([파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/))이 있어요.
2. 서로 다른 아파트에 있는 방끼리 비밀 전화를 걸려면, 동네 우체국이 모르는 주소를 알아서 전달해 줄 똑똑한 전화국 직원이 필요해요.
3. CNI는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 건물주가 고용한 전화국 직원으로, 플란넬, 칼리코 같은 여러 회사 중 우리 아파트에 가장 잘 맞는 직원을 골라 쓸 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 99 / 371

<- **이전**: [99. CSI (Container Storage Interface) - K8s 스토리지 범용 표준 플러그인](/studynote/13_cloud_architecture/02_iaas_paas_saas/099_csi_container_storage_interface_kubernetes_plugin/)
**다음**: [101. K8s 보안 - 서비스 어카운트 (ServiceAccount) 및 RBAC 권한](/studynote/13_cloud_architecture/02_iaas_paas_saas/101_serviceaccount_rbac_kubernetes_authorization/) ->

---
