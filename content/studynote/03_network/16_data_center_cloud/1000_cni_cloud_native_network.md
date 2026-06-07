---
title: "CNI"
date: "2026-05-08"
tags:
  - "studynote-network"
weight: 1000
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/)([Container Network Interface](/studynote/13_cloud_architecture/02_iaas_paas_saas/100_cni_container_network_interface_flannel_calico/))는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)([Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)) 같은 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 환경에서, 수시로 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되고 사라지는 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))들에게 네트워크 IP를 할당하고 연결해주는 표준화된 인터페이스다.
> 2. **가치**: 특정 네트워크 벤더에 종속되지 않고, 관리자가 플러그인([Flannel](/studynote/03_network/16_data_center_cloud/823_flannel_overlay_cni_vxlan/), [Calico](/studynote/03_network/16_data_center_cloud/824_calico_bgp_routing_cni_network_policy/), [Cilium](/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/) 등)만 갈아 끼우면 오버레이([VXLAN](/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/)), [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), 혹은 [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) 기반의 고성능 네트워크 등 원하는 통신 환경을 즉시 구현할 수 있다.
> 3. **판단 포인트**: 클러스터 규모가 작다면 설치가 쉬운 Flannel을 쓰지만, 규모가 커지고 [마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/) 보안과 트래픽 가시성이 필요해지면 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 오버헤드가 적은 [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) 기반의 [Cilium](/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/) CNI를 채택하는 것이 클라우드 아키텍트의 핵심 판단이다.

---

## Ⅰ. 개요 및 필요성

클라우드 환경이 가상 머신([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))에서 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)([Container](/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/))로 진화하면서 네트워크에도 큰 문제가 생겼다. VM은 한번 켜지면 IP가 거의 바뀌지 않지만, [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 환경의 [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/)([컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 그룹)는 하루에도 수백 번씩 죽고 살아나며 그때마다 IP 주소가 바뀐다. 이렇게 동적인 환경에서는 전통적인 라우터나 고정된 IP [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 방식으로는 통신을 유지할 수 없다.

이 혼란을 잠재우기 위해 [CNCF](/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/)([Cloud Native](/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/) Computing Foundation)가 주도하여 만든 표준이 바로 <strong><a href="/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/">CNI</a>(<a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/100_cni_container_network_interface_flannel_calico/">Container Network Interface</a>)</strong>다. "[컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)될 때 어떻게 네트워크에 연결할 것인가"에 대한 규칙만 정의해 두고, 실제 작동은 다양한 [서드파티](/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) 플러그인들이 알아서 하도록 책임을 분리(Decoupling)한 것이다.

```text
[MEC]
    |
    v
[클라우드 네이티브 네트워크]
    |
    +---> [QoS / QoE 차이 비교]
```

- **📢 섹션 요약 비유**: 매일 수십 번씩 텐트를 쳤다 접었다 하는 유목민 캠핑장([쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/))에서, 텐트를 칠 때마다 즉석에서 수도관과 전기선을 표준 규격으로 딱 맞게 꽂아주는 만능 어댑터가 CNI다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 클러스터에서 [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인은 [Kubelet](/studynote/13_cloud_architecture/02_iaas_paas_saas/082_kubelet_node_agent/)(노드 관리자)의 지시를 받아 작동한다. 주요 역할은 <strong>IP 주소 할당 (IPAM: IP Address <a href="/studynote/12_it_management/05_security_compliance/1013_management/">Management</a>)</strong>과 <strong>네트워크 인터페이스(veth pair) <a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a> 및 <a href="/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a> <a href="/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a></strong>이다.

```text
+--------------------------------- [ Kubernetes Node ] ---------------------------------+
|                                                                                       |
|  +-------------------------+               +---------------------------------------+  |
|  |       Pod A (App)       |               |              Pod B (DB)               |  |
|  |  +-------------------+  |               |  +---------------------------------+  |  |
|  |  |  eth0 (10.0.1.2)  |  |               |  |         eth0 (10.0.1.3)         |  |  |
|  |  +---------+---------+  |               |  +----------------+----------------+  |  |
|  +------------+------------+               +-------------------+-------------------+  |
|               | (veth pair)                                    | (veth pair)          |
|  +------------+------------------------------------------------+------------+         |
|  |                          CNI Plugin (e.g., Calico)                         |         |
|  |                      [ IPAM / Routing / Network Policy ]                   |         |
|  +------------+-------------------------------------------------------------+         |
|               |                                                                       |
|        [ 물리 NIC (eth0) ] -------------------------> 외부 네트워크 / 다른 노드        |
+---------------------------------------------------------------------------------------+
```

1. <strong><a href="/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/">Pod</a> <a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a> 시</strong>: Kubelet이 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 런타임을 통해 Pod를 띄우면, [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인을 호출한다. CNI는 가상 랜선(veth pair)을 만들어 한쪽은 [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 안(eth0)에, 한쪽은 호스트 네트워크에 연결하고 IP 대역 대장에서 IP를 하나 꺼내 부여한다.
2. <strong>오버레이 vs <a href="/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a></strong>: 플러그인의 성격에 따라, 노드 간 통신 시 패킷을 다시 포장하는 오버레이(Overlay, 예: Flannel의 [VXLAN](/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/)) 방식을 쓰거나, 패킷 포장 없이 실제 [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)(예: [Calico](/studynote/03_network/16_data_center_cloud/824_calico_bgp_routing_cni_network_policy/))을 사용하여 다른 노드의 Pod와 통신하게 만든다.

- **📢 섹션 요약 비유**: 아파트(Node)에 새 입주자([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))가 이사 오면, 관리사무소([Kubelet](/studynote/13_cloud_architecture/02_iaas_paas_saas/082_kubelet_node_agent/))가 통신사 기사님([CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/))을 불러 새 공유기 선(veth)을 깔아주고 임시 전화번호(IP)를 달아주는 과정이다.

---

## Ⅲ. 비교 및 연결

시중에는 다양한 [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인이 존재하며, 각기 다른 트레이드오프(Trade-off)를 가진다.

| [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 | 통신 방식 | 네트워크 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)(보안) | 주요 특징 및 권장 환경 |
|:---:|:---|:---|:---|
| <strong><a href="/studynote/03_network/16_data_center_cloud/823_flannel_overlay_cni_vxlan/">Flannel</a></strong> | 오버레이 ([VXLAN](/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/)) | 지원 안 함 (불가) | [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)이 가장 단순함. 보안 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 필요 없는 소규모 클러스터. |
| <strong><a href="/studynote/03_network/16_data_center_cloud/824_calico_bgp_routing_cni_network_policy/">Calico</a></strong> | [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) (비오버레이) | 완벽 지원 | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 뛰어나며, 상세한 L3/L4 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 룰 적용 가능. 표준적인 엔터프라이즈 환경. |
| <strong><a href="/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/">Cilium</a></strong> | [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) ([커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨 최적화) | L7/[API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 레벨까지 지원 | iptables를 우회하여 압도적인 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 가시성 제공. 최신 대규모 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 환경. |
| <strong>AWS <a href="/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/">VPC</a> <a href="/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/">CNI</a></strong> | [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) | [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Group 연동 | AWS의 실제 사설 IP(ENI)를 Pod에 직접 할당. AWS EKS 환경에 최적화. |

최근 [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 생태계의 트렌드는 리눅스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 네트워크 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)(iptables 등)이 너무 무겁고 느려지는 문제를 피하기 위해, [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 내부에서 패킷을 직접 처리하는 <strong><a href="/studynote/02_operating_system/10_security/615_ebpf/">eBPF</a>(extended <a href="/studynote/02_operating_system/01_overview_architecture/069_ebpf/">Berkeley Packet Filter</a>)</strong> 기반의 Cilium으로 급격히 이동하고 있다.

- **📢 섹션 요약 비유**: 이삿짐을 나를 때 우편배달부([Flannel](/studynote/03_network/16_data_center_cloud/823_flannel_overlay_cni_vxlan/))를 쓸지, 고속도로 직통 화물차([Calico](/studynote/03_network/16_data_center_cloud/824_calico_bgp_routing_cni_network_policy/))를 쓸지, 아예 순간이동 마법([Cilium](/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/), [eBPF](/studynote/02_operating_system/10_security/615_ebpf/))을 쓸지 상황에 맞게 골라 쓰는 것이 [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 선택이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**실무 적용 시나리오:**
[마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/)([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/))에서는 수십 개의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 서로 통신한다. 이때 결제 Pod에서만 DB Pod로 접근할 수 있게 막는 '네트워크 폴리시(Network [Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/))' 구현이 필수다. [Flannel](/studynote/03_network/16_data_center_cloud/823_flannel_overlay_cni_vxlan/) 같은 기본 CNI는 이를 지원하지 못하므로, 실무에서는 100% Calico나 Cilium을 선택하여 [마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/)([Micro-segmentation](/studynote/13_cloud_architecture/01_virtualization/059_micro_segmentation_east_west_traffic/)) [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)을 구축한다.

**기술사 판단 포인트 (Trade-off):**
CNI를 선택할 때는 <strong>'네트워크 <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>'과 'IP 자원 고갈'</strong> 문제를 동시에 봐야 한다.
1. AWS [VPC](/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/) CNI처럼 클라우드 업체의 실제 IP를 Pod에 주면 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 최고(오버레이 캡슐화 없음)지만, 가용 IP 개수 제한에 걸려 Pod를 더 이상 띄우지 못하는 치명적 장애가 발생할 수 있다.
2. 반대로 오버레이([VXLAN](/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/))를 쓰면 IP 고갈 문제는 없지만, 패킷을 쌌다 풀었다 하는 CPU 오버헤드와 MTU([Maximum Transmission Unit](/studynote/03_network/06_network_layer_ip/292_packet_encapsulation_mtu_ethernet_1500_bytes/)) 파편화로 인해 네트워크 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~20% 저하된다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 진짜 주소(클라우드 IP)를 나눠주면 배달은 빠르지만 주소판이 모자랄 수 있고, 임시 주소(오버레이)를 쓰면 무한대로 살 수 있지만 매번 주소록을 뒤져야 해서 배달이 느려지는 딜레마를 겪게 된다.

---

## Ⅴ. 기대효과 및 결론

CNI는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)가 인프라의 제왕으로 군림할 수 있게 해준 숨은 일등 공신이다. 네트워크의 복잡성을 플러그인이라는 인터페이스 뒤로 숨김으로써, 개발자는 인프라 구성에 신경 쓰지 않고 애플리케이션 배포에만 집중할 수 있는 진정한 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/)([Cloud Native](/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/)) 환경이 완성되었다.

앞으로는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 통신과 엣지 컴퓨팅을 위해 네트워크 가시성([Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/))과 초저지연이 더욱 중요해진다. 따라서 [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 기술은 단순한 IP 할당 수준을 넘어, [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) 기반으로 [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)([Service Mesh](/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/)) 기능까지 흡수하며 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 네트워크 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플레인의 절대적인 핵심으로 진화해 나갈 것이다. 향후에는 [클라우드 네이티브 네트워킹](/studynote/03_network/16_data_center_cloud/821_cloud_native_networking_scale_out_msa/) 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: 전기 플러그([CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 표준) 모양을 통일해 놓으니, 사용자는 뒤에서 화력발전소를 쓰든 태양광(각종 플러그인)을 쓰든 신경 쓰지 않고 그냥 코드만 꽂아서 가전제품(앱)을 편하게 쓸 수 있게 된 것이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [MEC](/studynote/03_network/12_iot_wpan_edge/627_mec_multi_access_edge_computing_5g/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [오버레이 네트워크](/studynote/03_network/16_data_center_cloud/815_overlay_network_virtualization_l2_extension/) ([Overlay Network](/studynote/03_network/16_data_center_cloud/815_overlay_network_virtualization_l2_extension/)) | 가상 환경의 논리적 연결을 만든다. |
| 패브릭 (Fabric) | 대규모 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)센터의 균일한 연결 구조다. |
| [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) / QoE 차이 비교 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: MEC]
    |
    v
[현재 개념: 클라우드 네이티브 네트워크]
    |
    +---> [확장 A: QoS / QoE 차이 비교]
    +---> [확장 B: 클라우드 네이티브 네트워킹]
```

[클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 네트워크는 MEC에서 출발해 현재 메커니즘을 정교화하고, 이후 [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) / QoE 차이 비교와 [클라우드 네이티브 네트워킹](/studynote/03_network/16_data_center_cloud/821_cloud_native_networking_scale_out_msa/) 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 수천 개의 레고 블록([컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/))으로 커다란 성을 지을 때, 블록들끼리 전화를 할 수 있게 전화선을 연결해 줘야 해요.
2. CNI는 레고 블록이 새로 조립될 때마다 알아서 전화선(가상 네트워크)을 딱딱 꽂아주고 전화번호(IP)를 나눠주는 만능 로봇이에요.
3. 이 로봇 덕분에 블록을 하루에 백 번 부수고 다시 만들어도 전화가 끊기지 않고 잘 연결된답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 100 / 1120

<- **이전**: [99. Massive MIMO (대규모 다중 안테나)](/studynote/03_network/02_multiplexing_multiple_access/099_Massive_MIMO_대규모_다중_안테나/)
**다음**: [1001. QoS / QoE 차이 비교](/studynote/03_network/20_performance_evaluation_advanced/1001_qos_qoe_difference/) ->

---
