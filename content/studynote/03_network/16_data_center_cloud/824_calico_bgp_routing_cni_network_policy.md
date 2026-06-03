---
title: 824. Calico (BGP 라우팅 CNI)
date: '2026-05-08'
tags:
- studynote-network
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Calico는 데이터센터와 클라우드 네트워크에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: Calico를 이해하면 확장성과 운영 자동화 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [[196_kubernetes_k8s_container_orchestration|쿠버네티스]]와 [[531_cloud_native_architecture|클라우드 네이티브]] 환경에서, 무거운 오버레이 [[377_tunneling_mechanism_overview|터널링]]([[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]])을 뚫지 않고 **표준 [[365_bgp_border_gateway_protocol_path_vector|BGP]]([[365_bgp_border_gateway_protocol_path_vector|Border Gateway Protocol]]) [[339_routing_overview_best_path_selection|라우팅]]을 사용하여 [[561_container_based_deployment|컨테이너]] 간의 순수 L3(네트워크 계층) 다이렉트 통신을 제공하며, 미치도록 강력한 [[690_firewall_generation_evolution|방화벽]](Network [[164_policy|Policy]])을 지원하는 고성능 [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인**입니다. (Tigera 개발)
- 현재 전 세계 상용 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 운영망(Production) 구축 시 압도적인 1위로 쓰입니다.

```text
[Flannel]
    │
    ▼
[Calico]
    │
    └──▶ [Cilium]
```

- **📢 섹션 요약 비유**: Calico는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [[170_selectivity_cardinality_distribution_tuning|선택도]] 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

어떻게 이중 포장(캡슐화) 없이 물리망을 뚫고 통신할까요?

1. **[[365_bgp_border_gateway_protocol_path_vector|BGP]] 라우터로 변신한 서버 (Node=Router)**:
   - Calico를 깔면, 수십 대의 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 노드(물리 서버) 안에 `BIRD`라는 이름의 [[365_bgp_border_gateway_protocol_path_vector|BGP]] [[339_routing_overview_best_path_selection|라우팅]] 소프트웨어가 켜집니다. 즉, **모든 서버가 스스로 어엿한 하나의 거대 라우터로 변신**하는 기적이 일어납니다.
2. **[[341_dynamic_routing_protocol_operation|동적 라우팅]] 장부 교환**:
   - 1번 서버 안에 새로운 [[561_container_based_deployment|컨테이너]]([[489_raid_10_hybrid|10]].0.1.5)가 뿅! 태어납니다. 
   - 1번 서버의 [[365_bgp_border_gateway_protocol_path_vector|BGP]] 에이전트는 즉시 2번 서버, 3번 서버에게 연락을 돌립니다. "야! 내 밑에 [[489_raid_10_hybrid|10]].0.1.5 생겼어! 여기로 올 패킷은 나한테 쏴!" ([[365_bgp_border_gateway_protocol_path_vector|BGP]] Route Reflection)
   - 전국의 모든 서버가 **[[561_container_based_deployment|컨테이너]] IP 주소가 어디 있는지 적힌 [[339_routing_overview_best_path_selection|라우팅]] 테이블(엑셀 장부)을 1초 만에 쫙 [[212_synchronization_mechanisms|동기화]]**합니다.
3. **빛의 속도 전송 (포장 금지)**:
   - 패킷을 보낼 때, Flannel처럼 [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] 택배 박스로 두껍게 싸지 않습니다. 내 책상에 있는 엑셀 장부([[339_routing_overview_best_path_selection|라우팅]] 테이블)를 펴보고 "아, 쟤는 2번 서버 밑에 있군" 하고 진짜 목적지 IP 그대로 쌩얼로 냅다 던져버립니다(Pure L3 [[339_routing_overview_best_path_selection|Routing]]). 속도가 물리 랜선 직결 수준으로 극강입니다.

*(※ 단, 사내 물리 [[238_switch_operation_principles|스위치]]가 BGP를 지원하지 않는 옛날 장비라면, Calico도 눈물을 머금고 IPIP나 [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] 오버레이 껍데기를 씌우는 모드로 [[313_rollback|후퇴]]([[129_fallback|Fallback]])해서 작동합니다.)*

```text
[Flannel]
    │
    ▼
[Calico]
    │
    └──▶ [Cilium]
```

- **📢 섹션 요약 비유**: Calico의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

속도도 빠르지만, 회사들이 Calico를 쓰는 진짜 이유는 바로 이 '보안 통제' 기능 때문입니다.

- **문제점**: [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 기본 상태는 모든 [[561_container_based_deployment|컨테이너]]가 서로 마음대로 핑퐁 통신을 합니다. 해커가 찌끄레기 팟 하나를 털면 사내망이 다 털립니다.
- **[[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]] (iptables 장악)**: 
  - 관리자가 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]]에 `NetworkPolicy` 규칙을 적습니다. "오직 [라벨: Frontend]가 붙은 팟만, [라벨: DB] 팟의 3306 포트로 접속하게 해!"
  - Calico에 딸려있는 강력한 호위 무사 `Felix` 요원이 이 명령을 낚아채어, **리눅스 서버 [[022_kernel_role|커널]] 깊숙한 곳의 [[690_firewall_generation_evolution|방화벽]](iptables)에 이 차단 룰을 수천 줄씩 빛의 속도로 코딩해 박아버립니다.**
  - 조건에 맞지 않는 악성 패킷은 [[561_container_based_deployment|컨테이너]]에 닿기도 전에 리눅스 밑바닥 [[022_kernel_role|커널]]에서 목이 잘려 나갑니다(Zero-Trust 실현).

Calico를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. Flannel가 기반 조건을 만든다면, Calico는 그 위에서 핵심 메커니즘을 구현하고, Cilium는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 확장성과 운영 자동화에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | Flannel의 기반 정리 | Calico의 핵심 동작 | Cilium의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 확장성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [[396_validation|확인]] | 현재 메커니즘의 적합성 판단 | 운영·확장 [[268_strategy_pattern|전략]] 연결 |

- **📢 섹션 요약 비유**: Flannel이 우체국 직원(물리 [[238_switch_operation_principles|스위치]]) 몰래 편지 겉면에 큰 합법 박스를 뒤집어씌워 보내는 '이중 포장 밀수꾼'이라면, **Calico**는 아예 동네 주민(서버) 전체가 스스로 정식 우체국장([[365_bgp_border_gateway_protocol_path_vector|BGP]] 라우터)으로 취업해 버리는 당당한 '정공법'입니다. 새로 이사 온 사람([[561_container_based_deployment|컨테이너]])이 생길 때마다 전국 우체국장들끼리 주소록을 1초 만에 최신판으로 공유합니다. 포장 박스를 씌울 필요 없이 맨투맨으로 주소를 정확히 아니 편지가 빛의 속도로 날아갑니다([[148_5g_embb_urllc_mmtc|초고속]] [[339_routing_overview_best_path_selection|라우팅]]). 게다가 각 동네 입구마다 무서운 조폭(Felix [[690_firewall_generation_evolution|방화벽]])을 세워둬서, 초대장(Network [[164_policy|Policy]])이 없는 불법 패킷은 동네에 발을 들이기도 전에 몽둥이로 다 찢어버리는 완벽한 [[148_5g_embb_urllc_mmtc|초고속]] 요새망입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 Calico를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [[823_flannel_overlay_cni_vxlan|Flannel]] 수준의 기본 대책으로 충분한지, 아니면 Calico가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 Cilium와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 현재 문제의 핵심이 확장성 부족인지, 운영 자동화 악화인지 먼저 분리한다.
2. Calico가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [[396_validation|확인]]한다.
3. 도입 후에는 인접 기술인 Cilium와의 연계 방식을 함께 검증한다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- Calico의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- Flannel와의 경계를 정리하지 않아 중복 투자나 [[164_policy|정책]] 충돌을 만드는 설계

- **📢 섹션 요약 비유**: Calico를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

Calico는 데이터센터와 클라우드 네트워크를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 확장성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [[825_cilium_ebpf_kubernetes_networking_security|Cilium]], [[821_cloud_native_networking_scale_out_msa|클라우드 네이티브 네트워킹]], 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [[821_cloud_native_networking_scale_out_msa|클라우드 네이티브 네트워킹]] 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: Calico는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[823_flannel_overlay_cni_vxlan|Flannel]] | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [[815_overlay_network_virtualization_l2_extension|오버레이 네트워크]] ([[815_overlay_network_virtualization_l2_extension|Overlay Network]]) | 가상 환경의 논리적 연결을 만든다. |
| 패브릭 (Fabric) | 대규모 데이터센터의 균일한 연결 구조다. |
| [[825_cilium_ebpf_kubernetes_networking_security|Cilium]] | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: Flannel]
    │
    ▼
[현재 개념: Calico]
    │
    ├──▶ [확장 A: Cilium]
    └──▶ [확장 B: 클라우드 네이티브 네트워킹]
```

Calico는 Flannel에서 출발해 현재 메커니즘을 정교화하고, 이후 Cilium와 [[821_cloud_native_networking_scale_out_msa|클라우드 네이티브 네트워킹]] 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 큰 아파트에 사는 친구들이 층마다 다른 규칙으로 엘리베이터를 타면 복잡해져요.
2. 이 개념은 어느 층에서 누구를 어떻게 연결할지 자동으로 정리해 주는 관리실과 같아요.
3. 그래서 많은 컴퓨터가 한 건물 안에서 더 잘 협력할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 945 / 1120

← **이전**: [[823_flannel_overlay_cni_vxlan|823. Flannel (단순 오버레이 CNI)]]
**다음**: [[825_cilium_ebpf_kubernetes_networking_security|825. Cilium (eBPF 네트워크 프레임워크)]] →

---
