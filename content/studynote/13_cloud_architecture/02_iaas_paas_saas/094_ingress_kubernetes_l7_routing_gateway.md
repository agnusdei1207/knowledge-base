---
title: "094. Ingress Kubernetes L7 Routing Gateway"
date: "2026-04-10"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 인그레스 (Ingress)는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 클러스터 외부의 트래픽을 내부의 여러 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 분배해주는 거대한 L7 (Application Layer) [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 규칙의 집합소다.
> 2. **가치**: 값비싼 클라우드 로드밸런서를 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)마다 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)할 필요 없이, 단 1개의 로드밸런서와 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)/경로 기반 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)으로 인프라 비용을 극적으로 절감한다.
> 3. **판단 포인트**: Ingress 객체 자체는 종이 규칙일 뿐이므로, 실제 트래픽을 처리할 인그레스 컨트롤러 (Ingress Controller, 예: Nginx)가 반드시 구동되어야 한다.

---

## Ⅰ. 개요 및 필요성

인그레스 (Ingress)는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 외부에서 들어오는 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/[HTTPS](/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/) 트래픽을 클러스터 내부의 알맞은 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))로 연결하는 규칙 모음이다. 이 규칙은 특정 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 이름(Host)이나 URL 경로(Path)에 따라 트래픽을 다르게 분배할 수 있게 해준다.

[마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/) ([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/), [Microservices Architecture](/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) 환경에서는 수십 개의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 각자의 API를 제공한다. 만약 L4 로드밸런서만 사용한다면, 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)마다 별도의 외부 IP와 로드밸런서 장비가 필요해져 비용과 관리 복잡도가 폭발적으로 증가한다. 인그레스는 클러스터 진입점을 하나로 통일하고, 그 안에서 똑똑하게 목적지를 찾아주는 역할을 함으로써 이 문제를 해결한다.

- **📢 섹션 요약 비유**: 쇼핑몰 입점 상가 10곳이 각각 전용 출입문과 경호원을 두면 비용이 감당 안 됩니다. 인그레스는 거대한 중앙 정문 하나만 뚫어놓고, 로비에 똑똑한 안내 데스크 직원을 두어 손님의 목적지에 맞게 층수를 안내하는 시스템과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

인그레스 시스템은 크게 규칙을 정의하는 'Ingress 객체'와 이 규칙을 실행하는 'Ingress Controller'로 구성된다. 클라이언트의 요청이 들어오면 외부 로드밸런서가 트래픽을 인그레스 컨트롤러 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))로 보내고, 컨트롤러는 자신이 가진 규칙표를 확인하여 적절한 내부 ClusterIP [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 트래픽을 전달한다.

| 구성 요소 | 역할 | 핵심 특징 |
| :--- | :--- | :--- |
| Ingress Resource | [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 규칙 명세서 (yaml) | 호스트, 경로, 대상 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 정의 |
| Ingress Controller | 규칙을 물리적으로 실행하는 라우터 | Nginx, Traefik 등 웹 서버 엔진 |
| [TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) Termination | 인증서 해독 및 평문 변환 | 백엔드 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)의 복호화 부하 제거 |

```text
+--------------------------------------------------------------+
|             Ingress L7 Routing Architecture                |
+--------------------------------------------------------------+
| [Client] --> (HTTPS) --> [ External LoadBalancer ] (L4)      |
|                               |                            |
| +-----------------------------v--------------------------+ |
| |                  Ingress Controller                    | |
| | (TLS Termination: 복호화 수행, HTTP로 변환)            | |
| |                                                        | |
| |  if Host == api.shop.com/order ---> [Service: Order]    | |
| |  if Host == api.shop.com/pay   ---> [Service: Pay]      | |
| +-----------------------------+--------------------------+ |
|                               | 트래픽 분배                |
|             +-----------------+-----------------+          |
|             v                                   v          |
|   [ Order Pods ]                          [ Pay Pods ]     |
+--------------------------------------------------------------+
```

이 다이어그램은 외부에서 단일 진입점으로 들어온 암호화된 트래픽이 컨트롤러에서 복호화된 후, L7 정보(URL)를 바탕으로 여러 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 나뉘는 병목 해소 과정을 보여준다.

- **📢 섹션 요약 비유**: 국회에서 통과된 법률(Ingress 규칙) 그 자체로는 범죄가 잡히지 않습니다. 그 법률 책을 읽고 실제로 도로에서 음주 단속을 수행하는 경찰관(Ingress Controller)이 있어야 트래픽 통제가 돌아가는 원리입니다.

---

## Ⅲ. 비교 및 연결

인그레스를 정확히 이해하려면 기존 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 네트워크 노출 방식인 NodePort, LoadBalancer [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 비교해야 한다. 이들은 주로 OSI 4계층(L4) 수준의 단순 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 포워딩을 수행한다.

| 항목 | NodePort | LoadBalancer | Ingress |
| :--- | :--- | :--- | :--- |
| [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 계층 | L4 (IP, [Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)) | L4 (IP, [Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)) | L7 ([HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/[HTTPS](/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/), Host, Path) |
| 클라우드 비용 | 낮음 (노드 IP 직접 개방) | 높음 ([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)마다 LB [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)) | 매우 낮음 (LB 1개로 통합) |
| 활용 목적 | 테스트 환경, 소규모 내부 통신 | 단일 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 외부 공개 | 다수 [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 통합 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) |
| [TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 처리 | 개별 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)에서 직접 처리 | 개별 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 혹은 LB에서 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | 컨트롤러에서 통합 처리 (Termination) |

NodePort나 LoadBalancer는 단순한 '[파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)'라면, Ingress는 '[스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 보드'다. 트래픽의 내용(URL)을 들여다보고 판단할 수 있는 지능이 추가되어 훨씬 정교한 통제가 가능해진다.

- **📢 섹션 요약 비유**: L4 로드밸런서는 주소만 보고 우편물을 동네로 던지는 택배 기사라면, L7 인그레스는 편지봉투에 적힌 수신자 이름을 정확히 읽고 각자의 방 문 앞까지 배달해 주는 똑똑한 집사입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 인그레스 도입 시 가장 중요한 의사결정은 어떤 인그레스 컨트롤러를 선택할 것인가이다. Nginx Ingress Controller가 가장 대중적이지만, 환경에 따라 ALB Ingress(AWS), [Istio](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) Gateway([Service Mesh](/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/)) 등을 고려해야 한다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. <strong>컨트롤러 <a href="/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a></strong>: 인그레스 컨트롤러 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 죽으면 클러스터 전체의 외부 통신이 끊어지므로 반드시 복제본(Replica)을 늘려 고가용성(HA)을 확보했는가?
2. <strong><a href="/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/">TLS</a> 인증서 자동화</strong>: Cert-Manager와 연동하여 Let's Encrypt 등으로 인증서 발급과 갱신을 자동화했는가?
3. **규칙 충돌 방지**: 여러 부서가 작성한 Ingress yaml [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 간에 동일 경로(`/`)에 대한 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 규칙 충돌이 없는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 50개의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 각각 LoadBalancer 타입으로 노출시켜 인프라 비용을 낭비하는 설계
- 인그레스 컨트롤러 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)에 대한 리소스 제한(CPU/Memory)을 너무 낮게 잡아 트래픽 병목이 발생하는 구성

- **📢 섹션 요약 비유**: 인그레스 컨트롤러는 백화점의 중앙 에스컬레이터입니다. 이곳이 좁거나 고장 나면 층별 매장이 아무리 넓어도 손님을 받을 수 없으므로, 가장 튼튼하고 넓게 설계해야 합니다.

---

## Ⅴ. 기대효과 및 결론

인그레스의 도입은 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 환경에서 [퍼블릭 클라우드](/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/) 비용을 최소화하고 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 관리를 중앙 집중화하는 확실한 기대효과를 준다. 또한, SSL/[TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 처리와 같은 공통 보안 로직을 컨트롤러에 위임함으로써 백엔드 개발자는 순수 비즈니스 로직 개발에만 집중할 수 있게 된다.

최근에는 인그레스의 한계를 넘어 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/[UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)과 더욱 복잡한 트래픽 제어가 가능한 Gateway [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 규격으로 진화하는 추세다. 하지만 여전히 Ingress는 K8s 웹 트래픽 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)의 가장 검증되고 보편적인 표준 이정표로 기억해야 한다.

- **📢 섹션 요약 비유**: 각자 자동차를 타고 톨게이트 비용을 내던 사람들이, 거대한 고속버스(인그레스) 하나로 통합하여 비용을 아끼고 정확한 정류장에 내릴 수 있게 된 혁신입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| ClusterIP | 인그레스가 트래픽을 전달하는 내부 K8s [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 기본 타입 |
| Nginx Ingress Controller | 인그레스 규칙을 실제로 구동시키는 가장 대표적인 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 엔진 |
| [TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) Termination | 인그레스 앞단에서 [HTTPS](/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/) 암호를 풀고 내부로는 평문을 보내는 기법 |
| Gateway [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | Ingress의 복잡성을 개선하고 역할을 분리하기 위해 등장한 차세대 K8s [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 표준 |

### 📈 관련 키워드 및 발전 흐름도

```text
NodePort / LoadBalancer (L4)
    |
    v
Ingress Resource · Ingress Controller (L7 통합 라우팅)
    |
    v
Cert-Manager 연동 (TLS 자동화) · SSL Termination
    |
    v
Service Mesh (Istio Ingress Gateway)
    |
    v
Gateway API (차세대 표준)
```

이 흐름도는 "L4 단순 포워딩 -> L7 URL 기반 통합 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) -> [보안 자동화](/studynote/09_security/13_secops_ir_forensics/638_security_automation/) -> K8s 네이티브 고급 게이트웨이"로 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 체계가 진화하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 놀이공원([쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/))에 롤러코스터, 회전목마 같은 여러 놀이기구([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))가 있어요.
2. 예전엔 놀이기구마다 매표소를 따로 만들어서 돈이 너무 많이 들었어요.
3. 그래서 커다란 중앙 정문(인그레스)을 하나 만들고, 안내원 아저씨가 표를 확인한 뒤 가고 싶은 놀이기구 길로 쏙쏙 안내해 주는 거랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 93 / 371

<- **이전**: [93. LoadBalancer - 퍼블릭 클라우드 연동 K8s 외부 진입점](/studynote/13_cloud_architecture/02_iaas_paas_saas/093_loadbalancer_kubernetes_service_cloud_provider/)
**다음**: [95. HPA (Horizontal Pod Autoscaler) - CPU 기반 파드 자동 스케일링](/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/) ->

---
