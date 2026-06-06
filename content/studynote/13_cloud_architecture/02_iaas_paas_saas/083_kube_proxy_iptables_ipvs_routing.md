---
title: "083. Kube Proxy Iptables Ipvs Routing"
tags:
  - "cloud_architecture"
---

## 핵심 인사이트 (3줄 요약)
- **본질**: Kube-proxy는 각 노드에 배포되어 [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) VIP (Virtual IP) 트래픽을 살아 있는 [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) endpoint로 바꿔 주는 노드 로컬 네트워크 규칙 관리자다.
- **가치**: [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) IP가 계속 바뀌어도 [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 주소는 고정되므로, 애플리케이션은 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 이름만 알고 통신할 수 있다.
- **판단 포인트**: 작은 클러스터는 iptables로도 충분하지만, 규모가 커지면 IPVS (IP Virtual Server)나 [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) (Extended [Berkeley Packet Filter](/studynote/02_operating_system/01_overview_architecture/069_ebpf/)) 계열로 전환할지 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

[쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)에서 Pod는 임시적이다. 죽었다가 다시 뜨면 IP가 바뀐다. 애플리케이션이 이 변화를 직접 추적하게 두면, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 주소 변경 때문에 쉽게 깨진다. Kube-proxy는 이 문제를 해결하기 위해 Service라는 안정된 진입점을 만들고, 실제로는 살아 있는 Pod들로 트래픽을 흘려 보낸다.

즉, Kube-proxy는 패킷을 직접 오래 들고 나르는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 아니라, 노드 내부에 규칙을 심어 두고 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 알아서 분배하게 만드는 설정자다. [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 이름은 고정되고, 뒤에 연결된 Pod만 바뀐다. 이것이 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 추상화의 핵심이다.

```text
+--------------------------------------------------------------+
| Client -> Service VIP -> Kube-proxy 규칙 -> Live Pod IP       |
| Pod가 바뀌어도 Service 주소는 그대로 유지                   |
+--------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 손님은 항상 같은 식당 간판만 보고 들어가지만, 내부 주방의 요리사 배치는 그날그날 바뀌는 구조다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Kube-proxy는 보통 모든 워커 노드에 DaemonSet으로 배포된다. 그리고 Service와 Endpoints 변경을 감시해 iptables 또는 IPVS 테이블을 갱신한다. 여기서 실제 패킷 중계는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 수행하고, Kube-proxy는 규칙만 만든다. 패킷은 DNAT (Destination [Network Address Translation](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/))을 거쳐 목적지 Pod로 바뀐다.

| 모드 | 처리 위치 | 탐색 방식 | 확장성 |
| :--- | :--- | :--- | :--- |
| Userspace | 사용자 공간 | 직접 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) | 매우 낮음 |
| iptables | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) netfilter | 순차 룰 탐색 | 중간 |
| IPVS (IP Virtual Server) | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) LVS (Linux Virtual Server) | [해시 테이블](/studynote/08_algorithm_stats/04_datastructure/067_hash_table/) + [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 높음 |

[Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 타입도 함께 봐야 한다. ClusterIP는 클러스터 내부에서만 쓰는 안정된 VIP이고, NodePort는 모든 노드에 동일 포트를 열어 외부 진입을 허용한다. LoadBalancer는 클라우드 로드밸런서 뒤에서 노드나 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 노출한다. 어떤 타입이든 최종 [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 분배는 결국 Kube-proxy의 규칙을 따른다.

```text
+----------------------------------------------------------------+
| Service/Endpoints 변경 -► Kube-proxy Watch -► 규칙 갱신       |
+----------------------------------------------------------------+
| Packet -► iptables/IPVS -► DNAT -► Backend Pod               |
+----------------------------------------------------------------+
```

핵심은 "Kube-proxy가 느린가"보다 "규칙이 얼마나 빨리 바뀌는가"다. 규칙이 늦으면 새로운 Pod가 떠도 트래픽이 따라오지 못하고, 규칙이 과도하면 성능이 떨어진다.

- **📢 섹션 요약 비유**: 안내표를 벽에 붙여 둔 뒤, 우체부가 그 표만 보고 편지를 나르는 방식이다. 안내표를 빨리 갈아끼우는 것이 핵심이다.

---

## Ⅲ. 비교 및 연결

Kube-proxy는 Ingress나 외부 전송 계층 로드밸런서와 역할이 다르다. 외부 로드밸런서는 클러스터로 들어오는 큰 입구를 담당하고, Ingress는 애플리케이션 계층에서 경로와 호스트를 나눈다. Kube-proxy는 그 안쪽에서 [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) VIP를 실제 Pod로 쪼개는 마지막 단계다.

| 비교 항목 | 외부 전송 계층 로드밸런서 | [Ingress](/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/) | Kube-proxy |
| :--- | :--- | :--- | :--- |
| 위치 | 클러스터 외부 | 클러스터 경계 | 모든 워커 노드 |
| [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 대상 | 노드 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)/경로 | [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) |
| 주된 계층 | 전송 계층 | 애플리케이션 계층 | 전송 계층 |
| 역할 | 클러스터 입구 | URL/호스트 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) VIP [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) |

iptables와 IPVS도 비교해야 한다. iptables는 규칙 수가 늘수록 순차 탐색 부담이 커져 O(n)에 가깝고, IPVS는 해시 기반 탐색과 로드밸런싱 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 더 잘 버틴다. 그래서 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수가 많거나 엔드포인트가 많을수록 IPVS가 유리하다. 최근에는 [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) 기반 CNI가 Kube-proxy 기능 일부를 대체하기도 한다.

- **📢 섹션 요약 비유**: 큰 건물의 정문, 층별 안내판, 복도 안내원이 각각 다른 역할을 하듯, 외부 로드밸런서·[Ingress](/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/)·Kube-proxy는 계층이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수와 트래픽을 먼저 본다. 작은 클러스터면 iptables도 충분하지만, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 엔드포인트가 많아지면 선형 탐색이 병목이 된다. 그때는 IPVS로 바꾸거나, 더 나아가 [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) 기반 dataplane으로 전환할지 검토한다.

또 하나의 핵심은 Source IP 보존이다. Kube-proxy는 다른 노드의 Pod로 넘기기 위해 SNAT (Source [Network Address Translation](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/))을 적용할 수 있는데, 그러면 백엔드 로그에 클라이언트의 실제 IP가 아니라 노드 IP가 찍힌다. 이 문제가 중요하면 `externalTrafficPolicy: Local`을 고려해야 하지만, 노드별 부하 불균형이라는 대가가 있다.

체크리스트는 다음과 같다.
1. [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)/엔드포인트 수가 iptables 선형 탐색을 감당할 정도인가?
2. 실제 클라이언트 IP 보존이 필요한가?
3. kube-proxy daemonset이 모든 워커 노드에 정상 배포됐는가?
4. [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) ([Container Network Interface](/studynote/13_cloud_architecture/02_iaas_paas_saas/100_cni_container_network_interface_flannel_calico/))와 kube-proxy 방식이 충돌하지 않는가?

안티패턴은 명확하다. [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) IP를 앱에 하드코딩하거나, NodePort/LoadBalancer가 알아서 다 해결해 줄 것이라 착각하거나, SNAT의 존재를 모르고 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 로그를 해석하는 것이다. 네트워크 문제는 대개 규칙이 어긋났을 뿐이다.

- **📢 섹션 요약 비유**: 동네 식당은 종이에 적은 주문서로도 버티지만, 대형 푸드코트는 자동 분류기와 안내원이 모두 필요하다.

---

## Ⅴ. 기대효과 및 결론

Kube-proxy는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 이름을 안정적으로 유지하면서 Pod의 생명주기를 숨겨 준다. 그 결과 애플리케이션은 IP 변경을 신경 쓰지 않고도 트래픽을 처리할 수 있고, 운영자는 [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 단위로 네트워크를 관리할 수 있다.

한편 규모가 커질수록 iptables의 한계, SNAT로 인한 원본 IP 손실, 규칙 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 지연이 드러난다. 그래서 결론은 단순하다. Kube-proxy는 필수지만 영원한 정답은 아니며, 규모와 요구사항에 따라 IPVS나 [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) 대체 경로를 검토해야 한다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 고정된 접근점(VIP) |
| Endpoints | 실제 살아 있는 [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 목록 |
| iptables | 기본 규칙 삽입 방식 |
| IPVS (IP Virtual Server) | 대규모용 고성능 규칙 엔진 |
| DNAT (Destination [Network Address Translation](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)) | 목적지 주소 변환 |
| SNAT (Source [Network Address Translation](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)) | 소스 IP 변환 |
| [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) (Extended [Berkeley Packet Filter](/studynote/02_operating_system/01_overview_architecture/069_ebpf/)) | 차세대 대체 dataplane |
| [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) ([Container Network Interface](/studynote/13_cloud_architecture/02_iaas_paas_saas/100_cni_container_network_interface_flannel_calico/)) | [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 네트워크를 실제로 연결하는 계층 |

### 📈 관련 키워드 및 발전 흐름도

```text
Service / Endpoints
    |
    v
Kube-proxy Watch
    |
    +--------► iptables
    |
    +--------► IPVS (IP Virtual Server)
    |
    +--------► eBPF (Extended Berkeley Packet Filter)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 아파트에는 방 번호가 자주 바뀌는 주민들이 살고 있어요.
2. Kube-proxy는 로비에서 "몇 호가 어디 있는지"를 바로 알려 주는 안내원이에요.
3. 손님은 같은 주소만 기억하면 되고, 안내원이 그날그날 실제 방으로 데려다 준답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 82 / 371

<- **이전**: [82. Kubelet (큐블렛) - 마스터 노드의 명령을 받아 파드(Pod)를 생성/관리하고 헬스체크 결과를 보고하는 노드별 에이전트](/studynote/13_cloud_architecture/02_iaas_paas_saas/082_kubelet_node_agent/)
**다음**: [84. 컨테이너 런타임 (Container Runtime) - 파드 구동의 심장 containerd](/studynote/13_cloud_architecture/02_iaas_paas_saas/084_container_runtime_containerd_runc_cri/) ->

---
