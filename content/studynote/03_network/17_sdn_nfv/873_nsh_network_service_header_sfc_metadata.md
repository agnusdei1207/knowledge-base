---
title: 873. 네트워크 서비스 헤더 (NSH)
date: '2026-05-08'
tags:
- studynote-network
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 네트워크 [[090_service_kubernetes_network_load_balancing|서비스]] 헤더는 [[633_sdn_whitebox|SDN]]/NFV에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: 네트워크 [[090_service_kubernetes_network_load_balancing|서비스]] 헤더를 이해하면 [[164_policy|정책]] 유연성과 자동화 수준 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- 과거에 억지로 체인을 엮을 때는 [[372_policy_based_routing_pbr_route_map|PBR]]([[164_policy|정책]] 기반 [[339_routing_overview_best_path_selection|라우팅]])이나 [[224_vlan_virtual_lan_broadcast_domain|VLAN]] 꼼수를 썼습니다.
- **한계**: [[238_switch_operation_principles|스위치]]가 매번 패킷의 본문(IP, [[446_port_and_bus|포트]])을 샅샅이 까보고 "아, 얜 [[690_firewall_generation_evolution|방화벽]] 거친 애구나" 하고 수동으로 판단해야 했습니다. 트래픽이 몰리면 [[238_switch_operation_principles|스위치]]가 뇌정지가 왔고, 가상 앱([[866_vnf_virtual_network_function_software_appliance|VNF]]) 10개를 거치는 복잡한 체인은 길을 잃어버리기 일쑤였습니다.

```text
[서비스 체이닝 (Service Chainin…]
    │
    ▼
[네트워크 서비스 헤더]
    │
    └──▶ [P4 (Programming Protocol…]
```

- **📢 섹션 요약 비유**: 네트워크 [[090_service_kubernetes_network_load_balancing|서비스]] 헤더는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [[170_selectivity_cardinality_distribution_tuning|선택도]] 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

- **개념**: [[635_ietf_core_working_group_coap|IETF]](국제 인터넷 표준화 기구)에서 제정한 공식 [[872_service_chaining_sfc_vnf_traffic_steering|SFC]]([[090_service_kubernetes_network_load_balancing|서비스]] 기능 체이닝) 전용 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 규약입니다. 
- 원래 패킷 겉면에 **'이 패킷이 어떤 징검다리 코스(체인)를 밟아야 하며, 지금 현재 몇 번째 징검다리를 밟았는지(경로와 상태)'를 적어놓은 꼬리표(헤더 [[001_dikw_pyramid|데이터]])를 추가로 씌워서(인캡슐레이션) 전송하는 기술**입니다.

```text
[서비스 체이닝 (Service Chainin…]
    │
    ▼
[네트워크 서비스 헤더]
    │
    └──▶ [P4 (Programming Protocol…]
```

- **📢 섹션 요약 비유**: 네트워크 [[090_service_kubernetes_network_load_balancing|서비스]] 헤더의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

이마에 붙인 포스트잇(NSH)을 현미경으로 들여다보면 3가지 글씨가 적혀 있습니다.

### 1. [[159_spi_schedule_performance_index|SPI]] ([[090_service_kubernetes_network_load_balancing|Service]] Path [[088_identifier_in_er_model|Identifier]]) - "너 무슨 코스 타니?"
- 클라우드에 수만 개의 징검다리 코스(체인)가 있습니다.
- SPI는 **패킷이 배정받은 전체 코스의 고유 ID 번호**입니다. 
- (예: `SPI=100번`은 `방화벽 ➜ IPS ➜ 로드밸런서` 코스, `SPI=200번`은 `방화벽 ➜ 필터링` 코스) [[238_switch_operation_principles|스위치]]들은 [[159_spi_schedule_performance_index|SPI]] 100번을 보면 묻지도 따지지도 않고 그 코스 설계도대로 쳐냅니다.

### 2. SI ([[090_service_kubernetes_network_load_balancing|Service]] [[154_database_index_b_tree_search_optimization|Index]]) - "지금 몇 번째 징검다리 밟았니?" 🌟
- 가장 중요한 내비게이션(상태 추적) 정보입니다. 코스의 남은 단계 수를 거꾸로 셉니다.
- **동작 예시**:
  - 처음에 출발할 때 `SI=255` (가득 찬 상태) 도장이 찍혀있습니다.
  - 1번 [[690_firewall_generation_evolution|방화벽]]([[866_vnf_virtual_network_function_software_appliance|VNF]])을 통과하고 나올 때, [[690_firewall_generation_evolution|방화벽]]이 노란색 포스트잇의 숫자를 하나 깎아서 `SI=254`로 고쳐 적습니다.
  - 다음 [[238_switch_operation_principles|스위치]]가 이 패킷을 받으면 패킷 이마를 봅니다. "어? `SI=254`네? 1단계 끝났다는 뜻이군! 엑셀 장부를 보니 254번 상태일 땐 2번 IPS로 던지라네!" 하고 정확하게 2단계로 패스해 줍니다. 
  - 앱을 거칠 때마다 SI가 -1씩 깎이면서(Decrement), 징검다리의 무한 루핑(뺑뺑이)을 막고 완벽한 순서를 보장해 냅니다.

### 3. [[012_metadata|메타데이터]] ([[012_metadata|Metadata]]) - "앞사람이 남긴 메모"
- 1번 [[690_firewall_generation_evolution|방화벽]]이 패킷을 검사해 보니 "이거 살짝 해킹 의심되는데?" 싶으면, 패킷 본문은 안 건드리고 이 NSH 포스트잇 공간에 "해킹 의심도 80%"라고 몰래 텍스트([[033_context|Context]])를 끄적여서([[012_metadata|메타데이터]]) 2번 IPS에게 넘겨줍니다. 
- 2번 IPS는 포스트잇 메모를 읽고 더 빡세게 패킷을 찢어서 정밀 검사합니다. 가상 앱들끼리 패킷의 뒷담화(정보)를 실시간으로 공유하는 텔레파시 채널이 됩니다.

네트워크 [[090_service_kubernetes_network_load_balancing|서비스]] 헤더를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [[872_service_chaining_sfc_vnf_traffic_steering|서비스 체이닝]] ([[090_service_kubernetes_network_load_balancing|Service]] Chainin…가 기반 조건을 만든다면, 네트워크 [[090_service_kubernetes_network_load_balancing|서비스]] 헤더는 그 위에서 핵심 메커니즘을 구현하고, [[874_p4_programming_data_plane_pipeline_int_telemetry|P4]] (Programming [[295_protocol_field_tcp_udp_icmp|Protocol]]…는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 [[164_policy|정책]] 유연성과 자동화 수준에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [[872_service_chaining_sfc_vnf_traffic_steering|서비스 체이닝]] ([[090_service_kubernetes_network_load_balancing|Service]] Chainin…의 기반 정리 | 네트워크 [[090_service_kubernetes_network_load_balancing|서비스]] 헤더의 핵심 동작 | [[874_p4_programming_data_plane_pipeline_int_telemetry|P4]] (Programming [[295_protocol_field_tcp_udp_icmp|Protocol]]…의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | [[164_policy|정책]] 유연성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [[396_validation|확인]] | 현재 메커니즘의 적합성 판단 | 운영·확장 [[268_strategy_pattern|전략]] 연결 |

- **📢 섹션 요약 비유**: 네트워크 [[090_service_kubernetes_network_load_balancing|서비스]] 헤더는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- NSH 자체는 박스에 붙이는 송장(스티커)이지, 박스 그 자체(운반 수단)가 아닙니다.
- 그래서 817번에서 배운 **[[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] 박스(오버레이 터널) 안에 NSH 스티커가 붙은 패킷을 통째로 밀어 넣어서 배달([[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]]-GPE 등)**하는 것이 현대 클라우드 체이닝 배관의 절대 표준입니다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: NSH는 놀이공원([[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]) 입구에서 손님(패킷)의 손목에 채워주는 **'스마트 칩 자유이용권 팔찌'**입니다. 팔찌 안에는 두 가지가 들어있습니다. 첫째, **[[159_spi_schedule_performance_index|SPI]](코스 번호)**입니다. "이 손님은 바이킹 ➜ 롤러코스터 ➜ 귀신의 집 순서로 도는 VIP 코스([[159_spi_schedule_performance_index|SPI]] 100) 손님이다!" 둘째, **SI(남은 티켓 횟수)**입니다. 손님이 바이킹을 타고 나오면 출구 직원이 팔찌를 찍어 횟수를 3에서 2(SI=2)로 깎습니다. 다음 길목에 서 있는 안내원([[238_switch_operation_principles|스위치]])은 손님이 누군지 물어보지도 않고 팔찌만 딱 스캔합니다. "오! [[159_spi_schedule_performance_index|SPI]] 100번 코스인데 SI가 2가 남았군! 바이킹 탔으니 이제 롤러코스터 탈 차례네. 이쪽으로 가세요!" [[238_switch_operation_principles|스위치]]나 [[690_firewall_generation_evolution|방화벽]] 장비가 골치 아프게 [[339_routing_overview_best_path_selection|라우팅]] 장부를 머리 싸매고 고민할 필요 없이, 손목 팔찌(NSH)만 띡띡 스캔해서 0.1초 만에 다음 코스로 착착 돌려보내는 기적의 무인 릴레이 패스 시스템입니다.

---

## Ⅴ. 기대효과 및 결론

네트워크 [[090_service_kubernetes_network_load_balancing|서비스]] 헤더는 [[633_sdn_whitebox|SDN]]/NFV를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 [[164_policy|정책]] 유연성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [[874_p4_programming_data_plane_pipeline_int_telemetry|P4]] (Programming [[295_protocol_field_tcp_udp_icmp|Protocol]]…, 프로그래머블 네트워크, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 프로그래머블 네트워크 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: 네트워크 [[090_service_kubernetes_network_load_balancing|서비스]] 헤더는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[872_service_chaining_sfc_vnf_traffic_steering|서비스 체이닝]] ([[090_service_kubernetes_network_load_balancing|Service]] Chainin… | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 제어 평면 (Control Plane) | [[164_policy|정책]]과 경로 결정을 담당한다. |
| [[001_dikw_pyramid|데이터]] 평면 ([[001_dikw_pyramid|Data]] Plane) | 실제 패킷 전달을 수행한다. |
| [[874_p4_programming_data_plane_pipeline_int_telemetry|P4]] (Programming [[295_protocol_field_tcp_udp_icmp|Protocol]]… | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 서비스 체이닝 (Service Chainin…]
    │
    ▼
[현재 개념: 네트워크 서비스 헤더]
    │
    ├──▶ [확장 A: P4 (Programming Protocol…]
    └──▶ [확장 B: 프로그래머블 네트워크]
```

네트워크 [[090_service_kubernetes_network_load_balancing|서비스]] 헤더는 [[872_service_chaining_sfc_vnf_traffic_steering|서비스 체이닝]] ([[090_service_kubernetes_network_load_balancing|Service]] Chainin…에서 출발해 현재 메커니즘을 정교화하고, 이후 [[874_p4_programming_data_plane_pipeline_int_telemetry|P4]] (Programming [[295_protocol_field_tcp_udp_icmp|Protocol]]…와 프로그래머블 네트워크 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감 차를 움직이는 조종기와 차체를 따로 생각하면 바꾸기 쉬워져요.
2. 이 개념은 네트워크의 머리와 몸을 나눠 더 쉽게 프로그램하게 해줘요.
3. 그래서 새 규칙을 더 빨리 넣고 바꿀 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 994 / 1120

← **이전**: [[872_service_chaining_sfc_vnf_traffic_steering|872. 서비스 체이닝 (SFC)]]
**다음**: [[874_p4_programming_data_plane_pipeline_int_telemetry|874. 데이터 평면 프로그래밍 모델 (P4)]] →

---
