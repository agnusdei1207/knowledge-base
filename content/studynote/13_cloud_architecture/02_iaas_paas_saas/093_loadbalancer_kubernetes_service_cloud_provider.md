---
title: "Loadbalancer Kubernetes Service Cloud Provider"
date: "2026-04-10"
tags:
  - "studynote-cloud-architecture"
weight: 93
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: K8s ([Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/))의 LoadBalancer [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 클러스터 내부의 네트워크를 [퍼블릭 클라우드](/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/) 벤더의 L4 로드밸런서와 자동으로 연동해 주는 외부 진입점이다.
> 2. **가치**: 인프라 관리자가 직접 [퍼블릭 클라우드](/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/) 콘솔에서 로드밸런서를 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고 노드 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 연결하는 수동 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/) ([Provisioning](/studynote/09_security/11_iam_access_control/528_provisioning/)) 작업을 완전히 자동화한다.
> 3. **판단 포인트**: [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)마다 로드밸런서를 개별 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하므로 비용이 급증할 수 있으며, L7 ([HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/[HTTPS](/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/)) 경로 기반 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)이 필요할 때는 [Ingress](/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/) ([인그레스](/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/))로 전환을 고려해야 한다.

---

## Ⅰ. 개요 및 필요성

K8s [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 타입 중 LoadBalancer는 클러스터 외부의 사용자 트래픽을 내부 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) ([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))로 연결하기 위해 클라우드 사업자의 실제 로드밸런서를 동적으로 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 기술이다.

기존의 NodePort (노드포트) 방식은 모든 노드의 특정 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)(30000~32767)를 열어야 했고, 사용자가 직접 특정 노드의 IP를 알고 접속해야 하는 한계가 있었다. 상용 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서는 고객에게 고정된 단일 공인 IP와 표준 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)(80, 443)를 제공해야 하며, 특정 노드가 다운되더라도 트래픽이 우회될 수 있는 진정한 의미의 부하 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)이 필수적이다. LoadBalancer는 K8s의 CCM (Cloud Controller Manager)이 AWS, GCP 등의 API를 호출하여 이 모든 구성을 코드로 자동화 ([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/))한다.

- **📢 섹션 요약 비유**: NodePort가 아파트 담벼락에 뚫어 놓은 여러 개의 쪽문이라면, LoadBalancer는 외부 도로와 연결된 거대하고 깔끔한 아파트 단지의 공식 정문 건물이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

LoadBalancer [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 단독으로 동작하는 것이 아니라, `외부 LB 인프라 -> NodePort -> ClusterIP -> Pod`로 이어지는 4단계 계층 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 구조를 감싸는 형태다.

| 구성 요소 | 역할 및 동작 방식 |
| :--- | :--- |
| <strong>Cloud <a href="/studynote/07_enterprise_systems/03_eai_esb_msa/150_soa_triangle_architecture/">Provider</a> <a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a></strong> | CCM이 클라우드 벤더의 API를 호출하여 L4 로드밸런서 인스턴스(예: AWS NLB)를 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/) |
| **NodePort** | 클라우드 로드밸런서가 트래픽을 꽂아 넣을 수 있도록 클러스터의 모든 워커 노드에 동일한 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 개방 |
| **kube-proxy** | 노드에 도달한 트래픽을 목적지 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)로 포워딩하는 iptables/IPVS 룰 적용 |
| <strong>External Traffic <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">Policy</a></strong> | `Local` [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 시, [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 없는 노드를 거치지 않고 직접 목적지 노드로 트래픽을 보내 SNAT 핑퐁 최소화 |

```text
+--------------------------------------------------------------+
|        LoadBalancer 트래픽 인입 및 계층적 라우팅 흐름        |
+--------------------------------------------------------------+
| [클라이언트] ---> (포트 80/443, 공인 IP)                      |
|                                                              |
|       v AWS NLB / GCP TCP LB (외부 클라우드 로드밸런서)      |
|                                                              |
|       +---> [노드 A] (포트 31000) ---> 파드 없음 (핑퐁 발생)   |
|       |                                                      |
|       +---> [노드 B] (포트 31000) ---> (kube-proxy) ---> [파드] |
+--------------------------------------------------------------+
```

[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시 K8s는 내부적으로 NodePort와 ClusterIP를 함께 할당한다. 이후 클라우드 LB는 노드의 IP와 해당 NodePort를 백엔드 타겟 그룹으로 묶어, 외부 트래픽을 클러스터 내부로 밀어 넣는다.

- **📢 섹션 요약 비유**: 로드밸런서는 거대한 깔때기와 같다. 넓은 외부 공인 IP로 쏟아지는 트래픽을 모아, 클러스터라는 체를 거쳐 정확한 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)라는 유리병 안으로 흘려보낸다.

---

## Ⅲ. 비교 및 연결

외부로 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 노출하는 K8s의 세 가지 방식은 노출 범위와 지능(L4 vs L7)에서 명확한 경계를 가진다.

| 항목 | NodePort | LoadBalancer | [Ingress](/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/) |
| :--- | :--- | :--- | :--- |
| <strong><a href="/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a> 계층</strong> | L4 (IP, [Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)) | L4 (IP, [Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)) | L7 ([HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/), URL 패스) |
| **외부 진입점** | 각 노드의 공인 IP + 비표준 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) | 클라우드 LB의 단일 공인 IP + 표준 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) | 클라우드 LB (1개) + [Ingress](/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/) Controller |
| **비용 구조** | 클라우드 LB 비용 없음 | <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 1개당 LB 1대 비용 발생</strong> | 여러 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 1대의 LB 공유 (비용 절감) |
| **주요 한계** | 상용 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)용으로 부적합 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 개수 비례 인프라 비용 폭증 | [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 복잡, 컨트롤러 추가 필요 |

LoadBalancer는 외부 L4 장비와의 단순 연결을 담당하지만, URL 패스 기반의 스마트한 트래픽 분배를 원한다면 이 LoadBalancer 뒤에 [Ingress](/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/) Controller를 배치하는 아키텍처로 진화하게 된다.

- **📢 섹션 요약 비유**: NodePort는 각 식당 주인이 직접 밖에서 손님을 부르는 것이고, LoadBalancer는 식당마다 전용 발렛파킹 직원을 고용하는 것이며, Ingress는 쇼핑몰 통합 안내 데스크를 두는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 LoadBalancer를 사용할 때는 "트래픽 최적화"와 "비용 통제"가 핵심 판단 기준이다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. **SNAT 및 레이턴시 문제**: `externalTrafficPolicy: Cluster` (기본값)는 트래픽이 무작위 노드로 가면서 홉 (Hop)이 추가된다. 클라이언트의 원본 IP를 보존하고 네트워크 지연을 줄이려면 `Local`로 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)해야 한다. 단, 이 경우 트래픽 불균형이 발생할 수 있어 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)의 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 배치 (Anti-Affinity) 설계가 수반되어야 한다.
2. **비용 폭탄 (Cost Explosion)**: [마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/) ([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/))에서 50개의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 모두 LoadBalancer로 열면 50대의 클라우드 LB가 과금된다.
3. <strong><a href="/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/">온프레미스</a> (<a href="/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/">On-Premise</a>) 한계</strong>: 베어메탈 (Bare Metal) 환경에서는 AWS/GCP의 API가 없으므로 `type: LoadBalancer`가 동작하지 않는다. 이 경우 MetalLB 같은 소프트웨어 기반 L2/[BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 솔루션을 별도로 구축해야 한다.

### 기술사적 의사결정
- **채택**: 트래픽 분리 격리가 엄격히 필요한 소수의 핵심 진입점 API나, L4 수준의 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/[UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 스트리밍 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 적용한다.
- **회피**: 수십 개의 웹/[API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(L7)를 띄우는 환경에서는 LoadBalancer 타입 직접 사용을 피하고, 단일 LoadBalancer와 연결된 [Ingress](/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/) 아키텍처로 전환해야 한다.

- **📢 섹션 요약 비유**: 회삿돈을 아끼려면 직원([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))마다 개별 법인차량(LoadBalancer)을 지급하지 말고, 대형 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)([Ingress](/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/)) 한 대를 렌트해 나눠 타게 만들어야 한다.

---

## Ⅴ. 기대효과 및 결론

LoadBalancer는 복잡한 인프라 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 작업을 K8s 매니페스트 (Manifest) 한 줄로 통합하여 진정한 의미의 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) ([Cloud Native](/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/)) 자동화를 완성했다. 이를 통해 개발자는 네트워크 장비의 CLI를 몰라도 글로벌 스케일의 부하 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)기를 즉시 확보할 수 있다.

하지만 1:1 결합 구조가 낳는 비용과 확장성 한계는 분명하다. 따라서 LoadBalancer는 "K8s와 [퍼블릭 클라우드](/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/)가 만나는 최초의 물리적 접점"으로 이해해야 하며, 이 접점을 어떻게 효율적으로 공유 ([Ingress](/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/), [API Gateway](/studynote/04_software_engineering/11_testing_validation/934_api_gateway/))할 것인지가 아키텍트의 최종 과제로 남게 된다.

- **📢 섹션 요약 비유**: 훌륭한 자동문(LoadBalancer)은 설치하기 쉽고 손님을 잘 맞이하지만, 문이 너무 많으면 유지보수비가 건물 렌트비를 넘어선다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **CCM (Cloud Controller Manager)** | K8s와 클라우드 벤더(AWS, GCP 등) API를 연결하는 [브리지](/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) |
| **NodePort (노드포트)** | LoadBalancer가 외부 트래픽을 노드 내부로 밀어 넣기 위해 의존하는 하위 기술 |
| <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/">Ingress</a> (<a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/">인그레스</a>)</strong> | LoadBalancer의 1:1 비용 문제를 해결하는 L7 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 및 호스트 기반 트래픽 제어기 |
| **MetalLB** | 클라우드 벤더가 없는 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 환경에서 LoadBalancer 기능을 구현하는 솔루션 |

### 📈 관련 키워드 및 발전 흐름도

```text
서비스 노출의 기초
    |
    v
NodePort (노드포트) · 단일 노드 IP 의존
    |
    v
LoadBalancer (로드밸런서) · 외부 L4 장비 연동 및 공인 IP 자동화
    |
    v
externalTrafficPolicy: Local · SNAT 방지 및 최적화
    |
    v
Ingress (인그레스) · L7 통합 라우팅으로 비용 및 효율성 극대화
```

### 👶 어린이를 위한 3줄 비유 설명

1. 학교 운동장에 텐트([파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/))를 치고 친구들을 초대하려고 해요.
2. 하지만 텐트가 어디 있는지 아무도 모르니까, 학교 정문(LoadBalancer)에 큰 간판을 세우고 안내원 아저씨를 불렀어요.
3. 이제 밖에서 온 친구들은 텐트 주소를 몰라도 안내원 아저씨가 정확하게 안내해 준답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 92 / 371

<- **이전**: [92. NodePort - 워커 노드의 특정 물리 포트 외부 노출](/studynote/13_cloud_architecture/02_iaas_paas_saas/092_nodeport_kubernetes_service_external_access/)
**다음**: [94. 인그레스 (Ingress) - K8s L7 URL 라우팅 통합 게이트웨이](/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/) ->

---
