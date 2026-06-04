---
title: "823. Flannel (단순 오버레이 CNI)"
date: "2026-05-08"
tags:
  - "studynote-network"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Flannel는 데이터센터와 클라우드 네트워크에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: Flannel를 이해하면 확장성과 운영 자동화 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 생태계에서 가장 널리 알려지고 역사 깊은 초창기 [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/)([Container Network Interface](/studynote/13_cloud_architecture/02_iaas_paas_saas/100_cni_container_network_interface_flannel_calico/)) 플러그인 중 하나입니다. 코어OS(CoreOS)에서 개발했습니다.
- **철학**: "[라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 그딴 거 몰라도 됨! 그냥 물리 네트워크 구조가 어떻든 간에 신경 끄고, 모든 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 노드(서버)들을 거대한 가상 네트워크(Overlay) 하나로 묶어줄게!"

```text
[컨테이너 네트워킹 인터페이스 쿠버네티스 망…]
    |
    v
[Flannel]
    |
    +---> [Calico]
```

- **📢 섹션 요약 비유**: Flannel는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Flannel은 백엔드 방식으로 여러 가지를 지원하지만, 99% 실무에서는 <strong><a href="/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/">VXLAN</a> (817번 문서 <a href="/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">참조</a>)</strong> 방식을 씁니다.

1. **IP 대역 쪼개주기**: [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 클러스터 전체에 `10.244.0.0/16` 이라는 거대한 가상 IP 덩어리를 줍니다. Flannel은 1번 서버(노드)에는 `10.244.1.0/24`를, 2번 서버에는 `10.244.2.0/24`를 사이좋게 떼어서 나눠줍니다.
2. **포장지 씌우기 (Encapsulation)**:
   - 1번 서버의 A [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 2번 서버의 B [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)로 데이터를 쏩니다.
   - 데이터가 서버 밖으로 나가기 직전, 1번 서버 바닥에 깔린 <strong>flanneld (데몬 에이전트)</strong>가 이 패킷을 낚아챕니다.
   - 그리고 이 패킷을 커다란 '일반 [UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 택배 박스([VXLAN](/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) 껍데기)' 안에 쏙 넣고, 겉면 주소에 <strong>"2번 서버의 진짜 물리적 IP 주소"</strong>를 적어서 던집니다.
3. **물리망의 속임수 통과**:
   - 데이터센터의 진짜 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)(언더레이) 장비들은 "어? 그냥 1번 서버가 2번 서버로 평범한 [UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 패킷 보내는 거네?" 하고 묻지도 따지지도 않고 배달해 줍니다. 중간 라우터들은 박스 안에 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) IP가 들어있는지 꿈에도 모릅니다.
4. **목적지 해체 (Decapsulation)**:
   - 2번 서버의 `flanneld`가 박스를 받아 칼로 북북 찢습니다(디캡슐레이션). 그 안에서 원래 A가 보냈던 순수한 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 패킷을 꺼내 B [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)에게 살포시 건네줍니다.

```text
[컨테이너 네트워킹 인터페이스 쿠버네티스 망…]
    |
    v
[Flannel]
    |
    +---> [Calico]
```

- **📢 섹션 요약 비유**: Flannel의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

### 1. 장점: 미친 듯이 쉬운 설치와 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)
- 네트워크 엔지니어가 물리 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 장비를 단 1도 만질 필요가 없습니다. ([언더레이 네트워크](/studynote/03_network/16_data_center_cloud/816_underlay_network_physical_infrastructure_routing/) 구조 완전 무시)
- AWS, 사내 전산실, 노트북 등 환경을 가리지 않고 `kubectl apply` 한 줄이면 완벽하게 [포드](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 간 통신이 뚫리는 기적의 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)을 보여줍니다. 테스트 및 소규모 클러스터에 절대 권력자입니다.

### 2. 한계: 속도 저하와 보안의 부재
- **캡슐화 오버헤드 폭발**: 패킷을 계속 박스로 싸고(Encap), 뜯고(Decap) 하는 작업을 리눅스 커널이 CPU를 갈아 넣어 해야 하므로 패킷 하나 보낼 때마다 미세한 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))이 생기고 전송 속도가 떨어집니다. (다음 824번 Calico가 이 문제를 박살 냅니다.)
- <strong>Network <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">Policy</a> 지원 불가 🌟</strong>: [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)의 생명은 "웹 [포드](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/)만 DB [포드](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/)에 접속할 수 있어!"라는 깐깐한 미니 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)(Network [Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/))을 거는 것인데, Flannel은 길만 뚫을 줄 알지 이 **보안 통제 기능이 아예 없어서 실무(운영망)에서 쓸 수가 없습니다.**

Flannel를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [컨테이너 네트워킹 인터페이스](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 망…가 기반 조건을 만든다면, Flannel는 그 위에서 핵심 메커니즘을 구현하고, Calico는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 확장성과 운영 자동화에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [컨테이너 네트워킹 인터페이스](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 망…의 기반 정리 | Flannel의 핵심 동작 | Calico의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 확장성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: Flannel은 국가(물리 라우터)의 감시를 피해 물건을 주고받는 완벽한 '우체국 이중 포장 꼼수'입니다. [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 마을([컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)) 주민들은 국가에 등록되지 않은 불법 거주자들입니다. 1번 동네 주민 A가 2번 동네 주민 B에게 편지를 직접 보내면 우체국(물리 라우터)에서 주소를 몰라 편지를 찢어버립니다. <strong>Flannel 요원</strong>은 A의 편지를 뺏어서, 겉면에 '합법적인 1번 동네 이장 ➜ 2번 동네 이장(진짜 서버 IP)'이라고 적힌 대형 합법 봉투([VXLAN](/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/))에 넣어 이중 포장을 합니다. 우체국은 겉봉투만 보고 무사통과시켜 줍니다. 2번 동네에 도착하면 요원이 겉봉투를 뜯고 진짜 편지를 B에게 몰래 전해줍니다. 도로 공사([라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/))가 전혀 필요 없는 기적의 밀수망이지만, 매번 편지를 이중 포장하고 뜯느라 우체국 직원이 땀을 뻘뻘 흘려(CPU 과부하) 속도가 좀 느린 것이 흠입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 Flannel를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [컨테이너 네트워킹 인터페이스](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 망… 수준의 기본 대책으로 충분한지, 아니면 Flannel가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 Calico와 같은 후속 기술, 자동화 체계, 표준 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)까지 함께 검토해야 한다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 확장성 부족인지, 운영 자동화 악화인지 먼저 분리한다.
2. Flannel가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 Calico와의 연계 방식을 함께 검증한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- Flannel의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [컨테이너 네트워킹 인터페이스](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 망…와의 경계를 정리하지 않아 중복 투자나 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: Flannel를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

Flannel는 데이터센터와 클라우드 네트워크를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 확장성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [Calico](/studynote/03_network/16_data_center_cloud/824_calico_bgp_routing_cni_network_policy/), [클라우드 네이티브 네트워킹](/studynote/03_network/16_data_center_cloud/821_cloud_native_networking_scale_out_msa/), 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [클라우드 네이티브 네트워킹](/studynote/03_network/16_data_center_cloud/821_cloud_native_networking_scale_out_msa/) 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: Flannel는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [컨테이너 네트워킹 인터페이스](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 망… | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [오버레이 네트워크](/studynote/03_network/16_data_center_cloud/815_overlay_network_virtualization_l2_extension/) ([Overlay Network](/studynote/03_network/16_data_center_cloud/815_overlay_network_virtualization_l2_extension/)) | 가상 환경의 논리적 연결을 만든다. |
| 패브릭 (Fabric) | 대규모 데이터센터의 균일한 연결 구조다. |
| [Calico](/studynote/03_network/16_data_center_cloud/824_calico_bgp_routing_cni_network_policy/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 컨테이너 네트워킹 인터페이스 쿠버네티스 망…]
    |
    v
[현재 개념: Flannel]
    |
    +---> [확장 A: Calico]
    +---> [확장 B: 클라우드 네이티브 네트워킹]
```

Flannel는 [컨테이너 네트워킹 인터페이스](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 망…에서 출발해 현재 메커니즘을 정교화하고, 이후 Calico와 [클라우드 네이티브 네트워킹](/studynote/03_network/16_data_center_cloud/821_cloud_native_networking_scale_out_msa/) 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 큰 아파트에 사는 친구들이 층마다 다른 규칙으로 엘리베이터를 타면 복잡해져요.
2. 이 개념은 어느 층에서 누구를 어떻게 연결할지 자동으로 정리해 주는 관리실과 같아요.
3. 그래서 많은 컴퓨터가 한 건물 안에서 더 잘 협력할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 944 / 1120

<- **이전**: [822. 컨테이너 네트워킹 인터페이스 (CNI)](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/)
**다음**: [824. Calico (BGP 라우팅 CNI)](/studynote/03_network/16_data_center_cloud/824_calico_bgp_routing_cni_network_policy/) ->

---
