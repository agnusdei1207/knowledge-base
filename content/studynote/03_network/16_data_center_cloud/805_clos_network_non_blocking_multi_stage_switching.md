---
title: 805. Clos 네트워크
date: '2026-05-08'
tags:
- studynote-network
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Clos 네트워크는 데이터센터와 클라우드 네트워크에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: Clos 네트워크를 이해하면 확장성과 운영 자동화 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- 10대의 전화를 10대의 전화와 1:1로 엮어주려면([[388_crossbar_switch|크로스바 스위치]]), 교차점(스위칭 소자)이 $[[489_raid_10_hybrid|10]] \times [[489_raid_10_hybrid|10]] = 100$개가 필요합니다.
- 만약 1,000대의 전화를 엮으려면 교차점이 무려 $1,000 \times 1,000 = 1,000,000$ (100만) 개가 필요합니다! 장비 크기가 기하급수적으로 커지고 열이 펄펄 끓어 상용화 자체가 불가능했습니다.

```text
[ECMP 스파인-리프 병렬 라우팅 경로 활성…]
    │
    ▼
[Clos 네트워크]
    │
    └──▶ [North-South 트래픽]
```

- **📢 섹션 요약 비유**: Clos 네트워크는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [[170_selectivity_cardinality_distribution_tuning|선택도]] 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

벨 연구소의 클로스는 거대 [[238_switch_operation_principles|스위치]] 1개를 **가장 작은 싸구려 [[238_switch_operation_principles|스위치]]들을 세 개의 층(Stage)으로 피라미드처럼 쌓아 연결**하는 방식으로 쪼개버렸습니다.

### 1. [[094_ingress_kubernetes_l7_routing_gateway|Ingress]] Stage (입력단)
- 서버들이 처음 데이터를 꽂는 1단계 [[238_switch_operation_principles|스위치]]들입니다. (현대 802번의 Leaf [[238_switch_operation_principles|스위치]] 역할)

### 2. Middle Stage (중간 스위칭단) 🌟 핵심 🌟
- **규칙 1**: 입력단의 모든 [[238_switch_operation_principles|스위치]]는 중간단에 있는 모든 [[238_switch_operation_principles|스위치]]와 각각 1가닥씩 선을 무조건 연결(Full-Mesh)해야 합니다.
- **규칙 2 (논블로킹의 비밀)**: 중간단에 배치하는 [[238_switch_operation_principles|스위치]]의 개수를 "입력 [[238_switch_operation_principles|스위치]]의 [[446_port_and_bus|포트]] 수보다 2배 정도(정확히는 $2n-1$)" 많게 넉넉히 깔아둡니다.
- **왜?**: 내가 1번 입력단에서 2번 출력단으로 가려는데 중간단 1번 [[238_switch_operation_principles|스위치]]가 다른 놈 때문에 꽉 막혀있더라도, 2번, 3번, 4번... 우회할 수 있는 중간 [[238_switch_operation_principles|스위치]]가 미친 듯이 많이 널려 있기 때문에 패킷은 절대 막히지 않고 빈 구멍을 찾아 빠져나갑니다. **(논블로킹, Non-blocking 달성)**

### 3. [[189_egress|Egress]] Stage (출력단)
- 중간 [[238_switch_operation_principles|스위치]]에서 빠져나온 데이터를 받아 목적지 서버로 넘겨주는 최종 관문입니다.

```text
[ECMP 스파인-리프 병렬 라우팅 경로 활성…]
    │
    ▼
[Clos 네트워크]
    │
    └──▶ [North-South 트래픽]
```

- **📢 섹션 요약 비유**: Clos 네트워크의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

수학의 승리이자 인류 네트워크 인프라의 구원입니다.

1. **크로스포인트(교차점) 비용의 극적 감소**:
   - 아까 1,000명을 엮으려면 100만 개의 교차점(비용)이 필요했습니다. 하지만 Clos 구조로 3단 쪼개기를 하면, 교차점이 약 **1/[[489_raid_10_hybrid|10]] 수준인 10만 개 정도**로 확 줄어듭니다! 100억짜리 [[238_switch_operation_principles|스위치]] 대신 10억짜리 [[238_switch_operation_principles|스위치]] 군단으로 100% 동일한 성능을 냅니다.
2. **현대 Spine-Leaf 아키텍처의 이론적 조상**:
   - 앞서 802번 문서에서 극찬한 데이터센터의 'Spine-Leaf 2-Tier 아키텍처'가, 사실은 이 1952년 Clos 박사의 3단 [[238_switch_operation_principles|스위치]] 모델의 허리(Middle Stage)를 접어서(Folded Clos) 만든 완벽한 현대적 재림입니다.

Clos 네트워크를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [[804_ecmp_equal_cost_multi_path_routing_load_balancing|ECMP]] 스파인-리프 [[430_index_fast_full_scan|병렬]] [[339_routing_overview_best_path_selection|라우팅]] 경로 활성…가 기반 조건을 만든다면, Clos 네트워크는 그 위에서 핵심 메커니즘을 구현하고, North-South 트래픽은 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 확장성과 운영 자동화에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [[804_ecmp_equal_cost_multi_path_routing_load_balancing|ECMP]] 스파인-리프 [[430_index_fast_full_scan|병렬]] [[339_routing_overview_best_path_selection|라우팅]] 경로 활성…의 기반 정리 | Clos 네트워크의 핵심 동작 | North-South 트래픽의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 확장성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [[396_validation|확인]] | 현재 메커니즘의 적합성 판단 | 운영·확장 [[268_strategy_pattern|전략]] 연결 |

- **📢 섹션 요약 비유**: 단일 거대 [[238_switch_operation_principles|스위치]](Crossbar) 방식은 서울의 모든 자동차 1,000만 대를 단 하나의 '초대형 1,000만 평짜리 광장 교차로'에 쏟아부어 지가 알아서 길을 찾아가게 만드는 무식하고 돈 많이 드는 토목 공사입니다. 이 거대한 교차로를 짓느라 나라가 망합니다. **클로스(Clos) 네트워크**는 천재 도로공사 직원의 아이디어입니다. "초대형 광장 하나를 만들지 말고, 작은 사거리 교차로 수만 개를 벌집 모양으로 그물처럼(3단계) 촘촘하게 엮어봐!" 한 사거리가 막히더라도 우회할 수 있는 수천 개의 다른 사거리가 존재하기 때문에(논블로킹), 결국 1,000만 대의 차가 동시에 출발해도 단 한 대도 막히지 않고 목적지에 쾌속 도달하는 기적의 우회로 그물망 시스템입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 Clos 네트워크를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [[804_ecmp_equal_cost_multi_path_routing_load_balancing|ECMP]] 스파인-리프 [[430_index_fast_full_scan|병렬]] [[339_routing_overview_best_path_selection|라우팅]] 경로 활성… 수준의 기본 대책으로 충분한지, 아니면 Clos 네트워크가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 North-South 트래픽와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 현재 문제의 핵심이 확장성 부족인지, 운영 자동화 악화인지 먼저 분리한다.
2. Clos 네트워크가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [[396_validation|확인]]한다.
3. 도입 후에는 인접 기술인 North-South 트래픽와의 연계 방식을 함께 검증한다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- Clos 네트워크의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [[804_ecmp_equal_cost_multi_path_routing_load_balancing|ECMP]] 스파인-리프 [[430_index_fast_full_scan|병렬]] [[339_routing_overview_best_path_selection|라우팅]] 경로 활성…와의 경계를 정리하지 않아 중복 투자나 [[164_policy|정책]] 충돌을 만드는 설계

- **📢 섹션 요약 비유**: Clos 네트워크를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

Clos 네트워크는 데이터센터와 클라우드 네트워크를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 확장성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 North-South 트래픽, [[821_cloud_native_networking_scale_out_msa|클라우드 네이티브 네트워킹]], 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [[821_cloud_native_networking_scale_out_msa|클라우드 네이티브 네트워킹]] 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: Clos 네트워크는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[804_ecmp_equal_cost_multi_path_routing_load_balancing|ECMP]] 스파인-리프 [[430_index_fast_full_scan|병렬]] [[339_routing_overview_best_path_selection|라우팅]] 경로 활성… | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [[815_overlay_network_virtualization_l2_extension|오버레이 네트워크]] ([[815_overlay_network_virtualization_l2_extension|Overlay Network]]) | 가상 환경의 논리적 연결을 만든다. |
| 패브릭 (Fabric) | 대규모 데이터센터의 균일한 연결 구조다. |
| North-South 트래픽 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: ECMP 스파인-리프 병렬 라우팅 경로 활성…]
    │
    ▼
[현재 개념: Clos 네트워크]
    │
    ├──▶ [확장 A: North-South 트래픽]
    └──▶ [확장 B: 클라우드 네이티브 네트워킹]
```

Clos 네트워크는 [[804_ecmp_equal_cost_multi_path_routing_load_balancing|ECMP]] 스파인-리프 [[430_index_fast_full_scan|병렬]] [[339_routing_overview_best_path_selection|라우팅]] 경로 활성…에서 출발해 현재 메커니즘을 정교화하고, 이후 North-South 트래픽와 [[821_cloud_native_networking_scale_out_msa|클라우드 네이티브 네트워킹]] 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 큰 아파트에 사는 친구들이 층마다 다른 규칙으로 엘리베이터를 타면 복잡해져요.
2. 이 개념은 어느 층에서 누구를 어떻게 연결할지 자동으로 정리해 주는 관리실과 같아요.
3. 그래서 많은 컴퓨터가 한 건물 안에서 더 잘 협력할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 926 / 1120

← **이전**: [[804_ecmp_equal_cost_multi_path_routing_load_balancing|804. ECMP (Equal-Cost Multi-Path) 스파인-리프 병렬 라우팅 경로 활성화]]
**다음**: [[806_north_south_traffic_data_center_gateway|806. North-South 트래픽 (외부 사용자-데이터센터간 흐름)]] →

---
