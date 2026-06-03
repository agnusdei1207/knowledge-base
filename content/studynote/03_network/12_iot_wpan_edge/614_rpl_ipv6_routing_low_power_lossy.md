+++
title = "614. RPL (IPv6 Routing Protocol for Low-Power and Lossy Networks)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: RPL는 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/), [WPAN](/knowledge-base/studynote/03_network/12_iot_wpan_edge/604_wpan_wireless_personal_area_network/), 엣지에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: RPL를 이해하면 전력 효율과 현장 반응성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 컴퓨팅 파워, 메모리, 배터리([Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/))가 극도로 부족하고, 무선 전파의 손실(Lossy)이 매우 잦은 열악한 [6LoWPAN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/117_6lowpan_iot_ipv6/) 기반 [센서 네트워크](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/103_wsn_sensor_network/)([WSN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/103_wsn_sensor_network/)/[IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)) 환경을 위해 <strong>IETF에서 개발한 맞춤형 <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/">IPv6</a> <a href="/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a> <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a></strong>입니다.
- 일반적인 인터넷 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)([거리 벡터](/knowledge-base/studynote/03_network/07_network_layer_routing/347_distance_vector_routing_bellman_ford/), [링크 상태](/knowledge-base/studynote/03_network/07_network_layer_routing/348_link_state_routing_dijkstra_spf/))의 복잡성을 걷어내고, 오직 "어떻게 하면 에너지를 아끼면서 목적지(대장 노드)로 데이터를 몰아줄 수 있을까?"에 집중합니다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">6LoWPAN</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">RPL</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">LPWAN 개요</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: RPL는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

RPL은 전체 센서들의 길 찾기 지도를 그릴 때, 일반적인 복잡한 거미줄([Mesh](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)) 대신 물이 위에서 아래로 흐르기 좋은 <strong>나무 뿌리(Tree) 형태의 방향성 <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/">그래프</a></strong>를 만듭니다. 이를 <strong>DODAG(Destination Oriented <a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/255_apache_airflow_dag/">Directed Acyclic Graph</a>, 목적지 <a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/066_dag_directed_acyclic_graph_tangle/">지향성 비순환 그래프</a>)</strong>라고 부릅니다.

### DODAG의 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 원리
1. 산 정상에 전기가 빵빵한 대장(Sink Node / Root)이 있습니다.
2. 대장 노드가 "내가 대장이다!"라는 메시지(DIO)를 주변에 뿌립니다.
3. 그 메시지를 들은 A 센서와 B 센서는 "나는 대장으로부터 1정거장(Hop) 거리구나!"라고 자신의 랭크(Rank, 계급)를 1로 설정하고 다시 주변에 메시지를 뿌립니다.
4. 그 밑에 있는 C 센서는 "아, A와 B를 거치면 대장에게 갈 수 있구나. 내 랭크는 2다"라고 설정합니다.
5. 이런 식으로 산 아래쪽 센서까지 서열(Rank)이 쫙 매겨지며, 거대한 다단계 피라미드 조직도(DODAG)가 순식간에 완성됩니다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">6LoWPAN</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">RPL</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">LPWAN 개요</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: RPL의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

- <strong>상향 트래픽 최적화 (Upward <a href="/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">Routing</a>)</strong>: 수만 개의 센서가 수집한 온도를 대장 노드(Root) 한 곳으로 쏟아부어야 하므로([Many-to-One](/knowledge-base/studynote/02_operating_system/02_process_thread/098_many_to_one_model/)), 계급(Rank)이 낮은 쪽에서 높은 쪽으로 데이터를 무조건 위로 토스하기만 하면 되는 단순한 구조를 가집니다.
- **비순환 (Acyclic)**: 길을 잘못 들어 데이터가 빙글빙글 무한히 도는 현상(루프)을 막기 위해, 데이터는 무조건 자기보다 Rank(계급)가 높은(대장 쪽에 가까운) 노드에게만 전달하도록 철저히 룰을 정해 배터리 낭비를 막습니다.
- **자가 치유**: 만약 직속상관 A 노드가 배터리가 다 돼 죽어버리면, C 센서는 당황하지 않고 즉시 옆에 있던 B 센서 쪽으로 데이터를 올려보냅니다(부모 노드 전환).

RPL를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. 6LoWPAN가 기반 조건을 만든다면, RPL는 그 위에서 핵심 메커니즘을 구현하고, [LPWAN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/) 개요는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 전력 효율과 현장 반응성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | 6LoWPAN의 기반 정리 | RPL의 핵심 동작 | [LPWAN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/) 개요의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 전력 효율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: RPL는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

일반 라우터들은 누군가 고장 나면 1초에 한 번씩 "살아있니?" 하고 계속 브로드캐스트를 날려 지도를 최신화합니다(Hello 패킷). 건전지로 버티는 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서가 1초에 한 번씩 전파를 쏘면 며칠 못 가 방전되므로, RPL은 상태 변화가 있을 때만 찔끔찔끔 지도를 고치는 방식(트리클 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))으로 극한의 다이어트를 합니다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: RPL은 산속에 길을 잃은 수만 명의 병사들이 산 정상의 헬기장(Root 노드)으로 탈출하는 다단계 생존 게임입니다. 복잡한 지도를 그릴 체력(배터리)이 없으니, 산 정상에서 헬기가 빛을 비추면 병사들은 무조건 "나보다 헬기 빛이 더 밝게 보이는(Rank가 높은) 앞사람의 등짝"만 보고 수건돌리기 하듯 데이터를 위로, 위로 토스해서 넘깁니다. 앞사람이 쓰러지면 바로 옆사람 등짝을 보고 던집니다.

---

## Ⅴ. 기대효과 및 결론

RPL는 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/), [WPAN](/knowledge-base/studynote/03_network/12_iot_wpan_edge/604_wpan_wireless_personal_area_network/), 엣지를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 전력 효율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [LPWAN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/) 개요, 자율형 엣지 협업, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 자율형 엣지 협업 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: RPL는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [6LoWPAN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/117_6lowpan_iot_ipv6/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 저전력 통신 (Low [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Communication) | 배터리 수명과 직접 연결된다. |
| [센서 네트워크](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/103_wsn_sensor_network/) (Sensor Network) | 수많은 단말의 연결 구조를 결정한다. |
| [LPWAN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/) 개요 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">선행 개념: 6LoWPAN</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재 개념: RPL</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 A: LPWAN 개요</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 B: 자율형 엣지 협업</div></div>
</div>
</div>



RPL는 6LoWPAN에서 출발해 현재 메커니즘을 정교화하고, 이후 [LPWAN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/) 개요와 자율형 엣지 협업 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 작은 로봇 친구들이 배터리를 아껴가며 서로 메시지를 주고받는 장난감 마을과 같아요.
2. 이 개념은 누가 가까운지, 누가 대신 알려줄지, 무엇을 현장에서 바로 처리할지를 정해줘요.
3. 그래서 작은 기기들도 오래 버티면서 똑똑하게 협력할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 735 / 1120

← **이전**: [613. 6LoWPAN](/knowledge-base/studynote/03_network/12_iot_wpan_edge/613_6lowpan_ipv6_header_compression_iot/)
**다음**: [615. LPWAN (Low-Power Wide-Area Network) 개요 (저전력 광역 통신)](/knowledge-base/studynote/03_network/12_iot_wpan_edge/615_lpwan_low_power_wide_area_network/) →

---
