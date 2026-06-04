+++
title = "91. ClusterIP - K8s 클러스터 내부 통신 전용 기본 서비스"
date = 2026-04-10

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ClusterIP는 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)([Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)) 클러스터 내부에서만 접근 가능한 가상의 IP(VIP, Virtual IP)를 제공하여 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/)) 간의 안정적인 통신을 보장하는 기본 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 타입이다.
> 2. **가치**: [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)는 수시로 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되고 삭제되며 IP가 변경되지만, ClusterIP는 단일 진입점과 고정된 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 네임을 제공하여 [서비스 디스커버리](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/306_service_discovery_pattern/)([Service Discovery](/knowledge-base/studynote/12_it_management/05_security_compliance/303_service_discovery/))와 로드밸런싱을 투명하게 처리한다.
> 3. **판단 포인트**: 외부 접근이 필요 없는 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)나 백엔드 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)는 무조건 ClusterIP로 보호해야 하며, 외부 공개가 필요한 경우에만 Ingress나 LoadBalancer와 결합하여 사용한다.

---

## Ⅰ. 개요 및 필요성

ClusterIP는 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)에서 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)([Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 객체를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)할 때 타입을 지정하지 않으면 기본으로 설정되는 통신 방식이다. 클러스터 내부의 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)들이 서로를 안정적으로 찾고 통신할 수 있도록 고정된 가상 주소를 부여하는 역할을 한다.

[쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 환경에서 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)는 일시적(Ephemeral)인 존재다. [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/), 노드 장애, [롤링 업데이트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/117_rolling_update_deployment/) 등으로 인해 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)는 끊임없이 재생성되며 그때마다 IP 주소가 바뀐다. 만약 프론트엔드 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 백엔드 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)의 IP를 하드코딩하여 통신한다면, 백엔드 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 재생성되는 순간 통신은 단절된다. ClusterIP는 이러한 종속성을 끊어내고, 바뀌지 않는 단일 IP와 [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) ([Domain Name System](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/)) 이름을 제공하여 클러스터 내부 통신의 혼란을 방지한다.

- **📢 섹션 요약 비유**: ClusterIP는 회사의 '내선 대표 번호'와 같다. 전화를 받는 직원([파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/))이 휴가를 가거나 퇴사해서 자리가 바뀌어도, 대표 번호 하나만 누르면 현재 출근한 직원 중 한 명에게 알아서 연결해 준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ClusterIP [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되면 Kube-proxy가 클러스터 내 모든 노드의 iptables 또는 IPVS (IP Virtual Server) 규칙을 업데이트하여 트래픽을 가로채고 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)시킨다.

| 핵심 요소 | 동작 원리 및 역할 |
| :--- | :--- |
| **VIP (Virtual IP)** | 실제 물리 인터페이스에 바인딩되지 않는 가상 IP 대역(예: [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/).96.x.x)을 할당받아 단일 진입점으로 작동한다. |
| **Endpoint (엔드포인트)** | 라벨 셀렉터(Label Selector)를 통해 현재 살아있는 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)들의 실제 IP 주소 목록을 실시간으로 추적하고 관리한다. |
| **CoreDNS** | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 이름 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시 `svc-name.namespace.svc.cluster.local` 형태의 FQDN (Fully Qualified [Domain](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) Name)을 자동 등록한다. |
| **Kube-proxy** | 노드 레벨에서 트래픽을 가로채어 엔드포인트에 등록된 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)들로 [라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/)(Round Robin) 방식으로 패킷을 전달한다. |

```text
+--------------------------------------------------------------+
|           ClusterIP를 통한 파드 간 통신 흐름도              |
+--------------------------------------------------------------+
|                                                              |
|  [Frontend Pod]                                              |
|         | 1. HTTP GET http://backend-svc                     |
|         v                                                    |
|  [CoreDNS] --> 2. DNS 질의: backend-svc -> 10.96.0.10 반환    |
|         |                                                    |
|         v 3. 트래픽 전송 (Dest: 10.96.0.10)                  |
|  [Kube-proxy (iptables/IPVS)] <-- 4. 규칙 매칭 및 로드밸런싱 |
|         |                                                    |
|         +---------------+---------------+                    |
|         v               v               v 5. 파드로 전달     |
|    [Backend 1]     [Backend 2]     [Backend 3]               |
|    (10.1.1.2)      (10.1.1.5)      (10.1.1.9)                |
+--------------------------------------------------------------+
```

이 구조에서 트래픽은 실제로는 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)에서 노드의 네트워크 스택을 거쳐 대상 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)로 바로 라우팅된다. ClusterIP라는 물리적 장비가 존재하는 것이 아니라, 각 노드의 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 규칙에 의해 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 라우팅이 성립하는 것이다.

- **📢 섹션 요약 비유**: 우체국(Kube-proxy)은 '비밀 기지(ClusterIP)'라는 주소로 편지가 오면, 실제 기지 요원들의 현재 위치(Endpoint)를 장부에서 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한 뒤 알아서 편지를 분배해 주는 마법의 우체통이다.

---

## Ⅲ. 비교 및 연결

[쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)의 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 타입은 외부 트래픽을 클러스터 내부로 어떻게 끌어오느냐에 따라 단계적으로 확장된다. ClusterIP는 이 계층 구조의 가장 안쪽 뼈대를 이룬다.

| 비교 항목 | ClusterIP | NodePort | LoadBalancer |
| :--- | :--- | :--- | :--- |
| **접근 범위** | 클러스터 **내부** 통신 전용 | 클러스터 **외부** (노드 IP + [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)) | 클러스터 **외부** (클라우드 로드밸런서) |
| **통신 대상** | 백엔드 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) | 테스트 환경, 자체 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 연동 | 상용 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 프론트엔드 노출 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">보안성</a></strong> | 매우 높음 (외부 격리) | 중간 ([포트 스캐닝](/knowledge-base/studynote/02_operating_system/10_security/600_port_scanning/) 노출 위험) | 낮음 (공인 IP 부여 시 위험 증가) |
| **구조적 의존성**| 독립적 동작 | 내부적으로 ClusterIP를 포함 | 내부적으로 NodePort와 ClusterIP를 포함 |

NodePort를 열든 클라우드의 LoadBalancer를 붙이든, 결국 트래픽의 종착지 바로 앞에서는 ClusterIP의 룰을 거쳐 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)로 분배된다. 따라서 ClusterIP는 모든 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 네트워킹의 근간이 된다.

- **📢 섹션 요약 비유**: ClusterIP가 아파트 단지 내 인터폰(내선 전용)이라면, NodePort는 아파트 경비실 직통 전화(특정 [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/) 필요)이고, LoadBalancer는 외부 인터넷 검색에 등록된 아파트 공식 대표번호([접근성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/292_accessibility_kwcag_wcag/) 최고)다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무 아키텍처 설계에서 ClusterIP는 보안 격리와 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 디커플링의 핵심 도구로 쓰인다. 트래픽의 [인그레스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/)([Ingress](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/)) 경로를 설계할 때 어떤 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 클러스터 외부로 노출할지 엄격히 통제해야 한다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. <strong>내부망 격리 <a href="/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>: [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)(MySQL, [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 등) [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 실수로 NodePort나 LoadBalancer로 열려 있지 않은가? (반드시 ClusterIP 사용)
2. **FQDN 활용**: 애플리케이션 환경 변수에 대상 서버의 하드코딩된 IP가 아닌, `svc-name.namespace.svc.cluster.local`과 같은 CoreDNS [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 네임이 설정되어 있는가?
3. <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/597_headless_cms_architecture/">Headless</a> <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a> 고려</strong>: [StatefulSet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/088_statefulset_kubernetes_persistent_workload/) 등에서 개별 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)에 직접 접근해야 하는 경우, ClusterIP 값을 `None`으로 설정하여 DNS가 여러 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) IP를 직접 반환하게([Headless](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/597_headless_cms_architecture/)) 구성했는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 내부 백엔드 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)인데 편의성을 위해 NodePort를 열어두고 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 통신에 노드 IP를 사용하는 설계. 이는 트래픽 불균형과 불필요한 네트워크 홉을 발생시킨다.

- **📢 섹션 요약 비유**: 은행 지점을 설계할 때, 고객이 드나드는 창구(LoadBalancer)와 금고 관리자끼리 소통하는 무전망(ClusterIP)을 섞어 쓰면 도둑이 든다. 내부 소통은 무조건 철저히 분리된 전용 무전망만 써야 한다.

---

## Ⅴ. 기대효과 및 결론

ClusterIP를 적극적으로 활용하면 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) ([Microservices Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) 환경에서 각 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 간의 결합도를 획기적으로 낮출 수 있다. 백엔드 시스템은 IP 변경의 공포 없이 유연한 오토스케일링과 무중단 배포를 수행할 수 있으며, 클러스터의 전체적인 보안 수준은 굳건히 유지된다.

미래의 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 환경에서는 [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)([Service Mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/))인 [Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/) 등과 결합하여 ClusterIP 통신 구간에 [mTLS](/knowledge-base/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/) ([Mutual TLS](/knowledge-base/studynote/09_security/04_endpoint_security/187_mtls_mutual_tls_authentication/)) 인증과 정밀한 트래픽 셰이핑([Traffic Shaping](/knowledge-base/studynote/03_network/07_network_layer_routing/392_traffic_shaping_and_policing/)) 기능을 추가하는 방향으로 확장된다. 따라서 ClusterIP는 단순한 내부망 통신 수단을 넘어, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 지향 아키텍처의 근간을 지탱하는 논리적 주소 체계로 이해해야 한다.

- **📢 섹션 요약 비유**: 톱니바퀴들이 서로 맞물려 돌아갈 때, 톱니 하나가 망가져 교체하더라도 전체 기계가 멈추지 않게 해주는 완충 기어(ClusterIP)가 있어 기계(클러스터)는 영원히 안전하게 돌아간다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **Kube-proxy** | ClusterIP의 가상 IP를 실제 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)의 IP로 변환하고 라우팅하는 실질적 주체 |
| **CoreDNS** | ClusterIP [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 이름에 대해 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 이름 해석을 제공하여 이름 기반 통신 완성 |
| **Endpoint (또는 EndpointSlice)** | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 트래픽을 보내야 할 살아있는 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)들의 IP 목록 장부 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/">Ingress</a> (<a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/">인그레스</a>)</strong> | 외부 트래픽을 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)과 경로(Path)에 따라 적절한 내부 ClusterIP로 전달하는 L7 라우터 |

### 📈 관련 키워드 및 발전 흐름도

```text
파드 IP 변경에 따른 통신 단절 문제
    |
    v
ClusterIP (내부용 가상 IP 및 로드밸런싱)
    |
    v
CoreDNS 연동 (FQDN을 통한 이름 기반 서비스 디스커버리)
    |
    v
NodePort / LoadBalancer (클러스터 외부 트래픽 유입으로 확장)
    |
    v
Service Mesh (Istio 등, 내부 통신의 암호화 및 트래픽 정밀 제어)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 놀이공원([쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)) 안에서 직원들끼리 무전기(ClusterIP)로 연락을 주고받아요.
2. 직원이 바뀌어서 새 직원이 와도, "청소팀 나와라!" 하고 이름([DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/))만 부르면 알아서 연결이 돼요.
3. 밖에서 온 손님들은 이 무전기 주파수를 절대 들을 수 없어서 직원들의 통신이 아주 안전하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 90 / 371

<- **이전**: [90. 서비스 (Service) - K8s 파드의 고정된 네트워크 진입점](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)
**다음**: [92. NodePort - 워커 노드의 특정 물리 포트 외부 노출](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/092_nodeport_kubernetes_service_external_access/) ->

---
