+++
weight = 821
title = "821. 클라우드 네이티브 네트워킹"
date = "2026-05-08"
[extra]
categories = "studynote-network"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹은 데이터센터와 클라우드 네트워크에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹을 이해하면 확장성과 운영 자동화 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [[061_on_premise_legacy_infrastructure|온프레미스]](물리적 전산실) 환경의 무겁고 고정된 네트워크 인프라 설계 방식을 버리고, **[[007_public_cloud|퍼블릭 클라우드]](AWS, GCP)나 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]](k8s) 환경에서 돌아가는 [[532_microservices_decomposition_patterns|마이크로서비스]]([[619_msa_traffic_hardware|MSA]])와 [[561_container_based_deployment|컨테이너]]들의 폭발적인 [[087_process_state_transition|생성]]/소멸([[249_scaling_normalization_standardization|스케일링]])에 맞춰, 네트워크 [[339_routing_overview_best_path_selection|라우팅]], 보안, 로드밸런싱을 100% 소프트웨어 기반으로 실시간 자동화하여 연동하는 차세대 네트워크 아키텍처**입니다.

```text
[EVPN]
    │
    ▼
[클라우드 네이티브 네트워킹]
    │
    └──▶ [컨테이너 네트워킹 인터페이스 쿠버네티스 망…]
```

- **📢 섹션 요약 비유**: [[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [[170_selectivity_cardinality_distribution_tuning|선택도]] 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. IP 주소의 생명주기 (Ephemeral IP)
- **과거**: 서버 한 대를 사면, IP 주소 `192.168.0.10`을 평생 부여하고 [[690_firewall_generation_evolution|방화벽]]에도 딱 못을 박았습니다(정적 IP).
- **[[531_cloud_native_architecture|클라우드 네이티브]]**: [[561_container_based_deployment|컨테이너]]([[198_pod_kubernetes_minimum_deployment_unit|Pod]])의 IP는 목숨이 파리 목숨입니다. 서버가 죽었다 켜지거나 트래픽이 몰려 복제될 때마다 매분 매초 **새로운 IP 주소가 랜덤으로 발급되고 사라집니다(임시적, Ephemeral).** 따라서 IP 주소 기반의 [[339_routing_overview_best_path_selection|라우팅]]이나 [[690_firewall_generation_evolution|방화벽]] 통제는 완전히 무의미해집니다.

### 2. [[306_service_discovery_pattern|서비스 디스커버리]] ([[303_service_discovery|Service Discovery]]) 도입 🌟
- IP가 1초마다 바뀌는데, A 서버가 B 서버를 어떻게 찾아갈까요?
- [[531_cloud_native_architecture|클라우드 네이티브]] 망에는 **중앙 전화번호부([[511_dns_hierarchical_distributed_architecture|DNS]] 기반 [[090_service_kubernetes_network_load_balancing|Service]] [[235_registry_immutable_tag|Registry]])**가 있습니다. B 서버가 새로 태어나면 스스로 전화번호부에 "나 새로 태어난 B(IP: [[489_raid_10_hybrid|10]].x.x.x)야!"라고 등록합니다. A 서버는 B의 IP를 외우지 않고, 전화번호부에 "B 어딨어?"라고 물어보고 접속합니다. (동적 위치 탐색)

### 3. [[136_variance|분산]] 로드밸런싱과 East-West 트래픽 폭발
- 옛날엔 중앙 입구(North-South)에 거대한 L4 [[238_switch_operation_principles|스위치]] 하나만 뒀습니다.
- 지금은 [[561_container_based_deployment|컨테이너]] 수천 개가 지들끼리 통신(East-West)하므로, 중앙 장비로 보내면 병목이 터집니다. 그래서 **로드밸런서([[264_proxy_pattern_surrogate_access_control|프록시]]) 기능 자체를 엄청나게 가벼운 소프트웨어로 쪼개어, 각 [[561_container_based_deployment|컨테이너]] 옆구리에 하나씩 붙여버리는 [[136_variance|분산]] 아키텍처([[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]], [[828_service_mesh_microservice_communication_infrastructure|Service Mesh]])**로 진화했습니다.

```text
[EVPN]
    │
    ▼
[클라우드 네이티브 네트워킹]
    │
    └──▶ [컨테이너 네트워킹 인터페이스 쿠버네티스 망…]
```

- **📢 섹션 요약 비유**: [[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

이 거대한 동적 핑퐁을 관리하기 위해 인류는 다음 세 가지를 만들어 냈습니다.
1. **[[822_cni_container_network_interface_kubernetes|CNI]] ([[561_container_based_deployment|컨테이너]] 네트워크 인터페이스)**: [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 안에서 수만 개의 [[561_container_based_deployment|컨테이너]]들에게 어떻게 자동으로 IP를 뿌리고 서로 통신하게 할 것인지 정하는 밑바닥 배관 표준 (822번 문서).
2. **Kube-Proxy와 [[094_ingress_kubernetes_l7_routing_gateway|Ingress]]**: 외부 인터넷에서 들어온 손님을, IP가 계속 바뀌는 수십 개의 [[561_container_based_deployment|컨테이너]] 중 한 곳으로 잘 넘겨주는 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]]의 기본 L4/L7 [[339_routing_overview_best_path_selection|라우팅]] 기능 (826, 827번 문서).
3. **[[828_service_mesh_microservice_communication_infrastructure|Service Mesh]] ([[302_service_mesh_istio|서비스 메시]])**: [[561_container_based_deployment|컨테이너]]들끼리 통신할 때 암호화(보안)를 걸고, 누가 통신을 많이 하는지 감시(추적)하는 고급 통신 관리 덮개 (828, 829번 문서).

[[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. EVPN가 기반 조건을 만든다면, [[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹은 그 위에서 핵심 메커니즘을 구현하고, [[822_cni_container_network_interface_kubernetes|컨테이너 네트워킹 인터페이스]] [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 망…는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 확장성과 운영 자동화에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | EVPN의 기반 정리 | [[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹의 핵심 동작 | [[822_cni_container_network_interface_kubernetes|컨테이너 네트워킹 인터페이스]] [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 망…의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 확장성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [[396_validation|확인]] | 현재 메커니즘의 적합성 판단 | 운영·확장 [[268_strategy_pattern|전략]] 연결 |

- **📢 섹션 요약 비유**: 기존 네트워킹은 집집마다 번지수가 영원히 고정된 '전통적인 마을 우체국 배달' 시스템입니다. [[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹은 유목민들이 매일 아침 수천 개의 텐트를 새로 치고 접는 '초거대 몽골 유목 캠프'입니다. 텐트 위치(IP 주소)가 매시간 바뀌는데 우편 배달부(라우터)가 옛날식 주소를 외우면 편지가 다 길을 잃습니다. 그래서 텐트를 칠 때마다 즉각 중앙 본부에 "나 지금 여기 텐트 쳤소!"라고 보고하는 '실시간 GPS 전화번호부([[303_service_discovery|Service Discovery]])'를 도입하고, 거대한 우체국 건물 대신 모든 텐트 옆에 초소형 드론(소프트웨어 로드밸런서)을 한 대씩 달아주어 텐트끼리 즉각 물건을 주고받게 만드는 완벽한 유동적 생존 통신망입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹을 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [[820_evpn_ethernet_vpn_bgp_control_plane|EVPN]] 수준의 기본 대책으로 충분한지, 아니면 [[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹이 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [[822_cni_container_network_interface_kubernetes|컨테이너 네트워킹 인터페이스]] [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 망…와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 현재 문제의 핵심이 확장성 부족인지, 운영 자동화 악화인지 먼저 분리한다.
2. [[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [[396_validation|확인]]한다.
3. 도입 후에는 인접 기술인 [[822_cni_container_network_interface_kubernetes|컨테이너 네트워킹 인터페이스]] [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 망…와의 연계 방식을 함께 검증한다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- EVPN와의 경계를 정리하지 않아 중복 투자나 [[164_policy|정책]] 충돌을 만드는 설계

- **📢 섹션 요약 비유**: [[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹을 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹은 데이터센터와 클라우드 네트워크를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 확장성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [[822_cni_container_network_interface_kubernetes|컨테이너 네트워킹 인터페이스]] [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 망…, [[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[820_evpn_ethernet_vpn_bgp_control_plane|EVPN]] | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [[815_overlay_network_virtualization_l2_extension|오버레이 네트워크]] ([[815_overlay_network_virtualization_l2_extension|Overlay Network]]) | 가상 환경의 논리적 연결을 만든다. |
| 패브릭 (Fabric) | 대규모 데이터센터의 균일한 연결 구조다. |
| [[822_cni_container_network_interface_kubernetes|컨테이너 네트워킹 인터페이스]] [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 망… | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: EVPN]
    │
    ▼
[현재 개념: 클라우드 네이티브 네트워킹]
    │
    ├──▶ [확장 A: 컨테이너 네트워킹 인터페이스 쿠버네티스 망…]
    └──▶ [확장 B: 클라우드 네이티브 네트워킹]
```

[[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹는 EVPN에서 출발해 현재 메커니즘을 정교화하고, 이후 [[822_cni_container_network_interface_kubernetes|컨테이너 네트워킹 인터페이스]] [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 망…와 [[531_cloud_native_architecture|클라우드 네이티브]] 네트워킹 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 큰 아파트에 사는 친구들이 층마다 다른 규칙으로 엘리베이터를 타면 복잡해져요.
2. 이 개념은 어느 층에서 누구를 어떻게 연결할지 자동으로 정리해 주는 관리실과 같아요.
3. 그래서 많은 컴퓨터가 한 건물 안에서 더 잘 협력할 수 있어요.
