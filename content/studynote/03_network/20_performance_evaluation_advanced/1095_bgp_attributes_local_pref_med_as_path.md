+++
title = "1095. BGP 속성 (Local Pref, MED, AS-path 구성비)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 평가와 고급 분석에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 이해하면 측정 정확도과 모델 적합성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **Path Vector (패스 벡터)**: BGP는 단순히 거리가 아니라, 거쳐 가는 통신사([AS](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/))들의 리스트 전체를 보고 판단합니다.
- SKT 입장에서는 빠르지만 비싼 유료망 타(Transit)는 것보다, 조금 느려도 서로 요금을 안 내기로 합의한(Peering) 망으로 트래픽을 쏟아붓고 싶어 합니다.
- 관리자가 이 "돈 아끼는 길"을 억지로 1등으로 만들게 해주는 <strong>권력의 지팡이</strong>가 바로 [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)([Attribute](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/))입니다.

```text
[OSPF ABR / ASBR Area 위계…]
    │
    ▼
[BGP 속성]
    │
    └──▶ [EIGRP DUAL 지연 스케일 분산]
```

- **📢 섹션 요약 비유**: [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Local Preference (내부 선호도) - "우리 회사 직원들의 최애 길"
라우터가 나가는 길(Outbound)을 정할 때 <strong>가장 막강한 1순위 절대 권력</strong>입니다.
- **특징**: 우리 통신사([AS](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/)) 안에서만 공유되는 비밀 점수입니다. 밖으로 새어 나가지 않습니다.
- **상황**: 우리 회사에서 미국으로 나가는 출구가 A(유료), B(무료) 2개입니다.
- **조작**: 관리자가 B 출구 라우터에 <strong><code>Local-Pref 200</code></strong> 훈장을 찍어버리고, A 출구엔 `100`(기본값)을 줍니다. 우리 회사 모든 라우터는 점수가 높은 B(무료) 출구로 미친 듯이 몰려갑니다. 거리가 100배 멀어도 무조건 이 점수가 짱입니다.

### 2. [AS](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/)-Path (국가 도장 릴레이) - "최단 [AS](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) 경로"
Local Pref가 똑같을 때 보는 2순위 대중적인 길 찾기 룰입니다.
- **특징**: 내가 목적지까지 갈 때 거쳐야 하는 <strong>통신사(<a href="/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/">AS</a>)들의 명함 개수</strong>입니다.
- **상황**: 미국 구글([AS](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) 15169)에서 온 소문이 2개가 있습니다.
  - 길 1: `AS 100 ➜ AS 200 ➜ AS 15169` (거친 나라 2개)
  - 길 2: `AS 300 ➜ AS 15169` (거친 나라 1개)
- **판단**: 당연히 거친 나라의 개수([AS](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/)-Path)가 더 짧은 '길 2'를 1등 경로로 채택합니다.
- <strong>해커의 꼼수 (<a href="/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/">AS</a>-Path Prepending)</strong>: 만약 길 2로 트래픽이 몰려 터질 것 같으면, 관리자가 억지로 내 번호를 여러 번 복사해 붙입니다. `AS 300 ➜ 300 ➜ 300 ➜ 15169`. 남들이 보기에 길 2가 무진장 길어 보이게 속여서 우회시키는 흑마법입니다.

### 3. MED (Multi-Exit Discriminator) - "우리 집에 올 땐 이 문으로 들어와"
들어오는 길(Inbound)을 꼬실 때 쓰는 외부용 간판입니다.
- **특징**: 인접한 다른 회사([AS](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/)) 라우터에게 던져주는 훈수입니다. Local-Pref의 정반대로, <strong>점수가 낮을수록 1등(<a href="/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/">Metric</a> 개념)</strong>입니다.
- **상황**: KT([AS](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) 100)와 SKT([AS](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) 200) 사이에 뚫린 연결 다리가 서울(A)과 부산(B) 두 곳입니다.
- **조작**: KT가 생각합니다. '서울 다리는 좁으니까, SKT 니네가 우리 쪽으로 패킷 쏠 때는 넓은 부산 다리(B)로 쏴라!' KT가 SKT에게 소문을 낼 때 부산 다리 경로에 <strong><code>MED 10</code></strong> (낮은 점수)을 적어 쏘고, 서울 다리엔 <strong><code>MED 100</code></strong>을 적어 쏩니다. SKT 라우터는 점수가 낮은 부산 다리를 1등으로 알고 트래픽을 쏟아붓습니다. (단, 이웃끼리만 통하고 멀리 퍼지진 않습니다.)

```text
[OSPF ABR / ASBR Area 위계…]
    │
    ▼
[BGP 속성]
    │
    └──▶ [EIGRP DUAL 지연 스케일 분산]
```

- **📢 섹션 요약 비유**: [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

위의 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)들이 부딪히면 순서대로 쳐냅니다.
1. [Weight](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 가 가장 높은 놈 ([Cisco](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/) 전용)
2. **Local Preference 가 가장 높은 놈 (1짱)**
3. 내가 직접 만든(Originated) 경로
4. <strong><a href="/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/">AS</a>-Path 가 가장 짧은 놈 (2짱)</strong>
5. Origin 코드가 좋은 놈 ([IGP](/knowledge-base/studynote/03_network/07_network_layer_routing/345_igp_interior_gateway_protocol_rip_ospf/) > [EGP](/knowledge-base/studynote/03_network/07_network_layer_routing/346_egp_exterior_gateway_protocol_bgp/) > ?)
6. **MED 가 가장 낮은 놈 (3짱)**

[BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [OSPF](/knowledge-base/studynote/03_network/07_network_layer_routing/357_ospf_open_shortest_path_first_overview/) ABR / ASBR Area 위계…가 기반 조건을 만든다면, [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)은 그 위에서 핵심 메커니즘을 구현하고, [EIGRP](/knowledge-base/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)은 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 측정 정확도과 모델 적합성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [OSPF](/knowledge-base/studynote/03_network/07_network_layer_routing/357_ospf_open_shortest_path_first_overview/) ABR / ASBR Area 위계…의 기반 정리 | [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)의 핵심 동작 | [EIGRP](/knowledge-base/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 측정 정확도 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: OSPF가 내비게이션 최단 거리를 찾는 <strong>'순수 수학공식 로봇'</strong>이라면, <strong>BGP의 <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/">속성</a>(<a href="/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/">Attribute</a>) 3대장</strong>은 정치판에서 돈과 인맥으로 승부하는 <strong>'더러운 외교 협상'</strong>입니다. 회사에서 해외 출장을 갈 때, 가장 강력한 1번 규칙 <strong>Local Pref(로컬 프레프)</strong>는 사장님의 <strong>'특명'</strong>입니다. 거리가 멀고 돌아가더라도 무조건 사장님이 지시한 저가 항공사(Local Pref 점수 높음)를 타야 합니다. 사장님 지시가 똑같다면, 2번 규칙 <strong><a href="/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/">AS</a>-Path(에이에스 패스)</strong>를 봅니다. 경유지(공항 환승) 개수가 제일 적은 비행기를 고릅니다(경유지가 많을수록 피곤하니까). 마지막 3번 규칙 <strong>MED(메드)</strong>는 도착지 국가 공항 직원의 <strong>'안내판'</strong>입니다. "우리나라에 올 때 1번 게이트(MED 100)는 짐 검사가 빡세니까, 2번 게이트(MED [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/))로 들어오세요!"라며 밖에서 쳐들어오는 방문객들의 동선을 내 입맛대로 강제로 비틀어버리는 외교 전술입니다. 단순한 속도 경쟁을 넘어 얽히고설킨 통신사들의 돈 문제를 해결해 주는 [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 전용 트래픽 통제 지휘봉입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [OSPF](/knowledge-base/studynote/03_network/07_network_layer_routing/357_ospf_open_shortest_path_first_overview/) ABR / ASBR Area 위계… 수준의 기본 대책으로 충분한지, 아니면 [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [EIGRP](/knowledge-base/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 측정 정확도 부족인지, 모델 적합성 악화인지 먼저 분리한다.
2. [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 [EIGRP](/knowledge-base/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)와의 연계 방식을 함께 검증한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [OSPF](/knowledge-base/studynote/03_network/07_network_layer_routing/357_ospf_open_shortest_path_first_overview/) ABR / ASBR Area 위계…와의 경계를 정리하지 않아 중복 투자나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 평가와 고급 분석을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 측정 정확도 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [EIGRP](/knowledge-base/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/), [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [OSPF](/knowledge-base/studynote/03_network/07_network_layer_routing/357_ospf_open_shortest_path_first_overview/) ABR / ASBR Area 위계… | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) ([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)) | 실제 전달 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 나타내는 대표 지표다. |
| [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) ([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) | 사용자 체감 품질을 좌우한다. |
| [EIGRP](/knowledge-base/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: OSPF ABR / ASBR Area 위계…]
    │
    ▼
[현재 개념: BGP 속성]
    │
    ├──▶ [확장 A: EIGRP DUAL 지연 스케일 분산]
    └──▶ [확장 B: AI 기반 성능 예측]
```

[BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)는 [OSPF](/knowledge-base/studynote/03_network/07_network_layer_routing/357_ospf_open_shortest_path_first_overview/) ABR / ASBR Area 위계…에서 출발해 현재 메커니즘을 정교화하고, 이후 [EIGRP](/knowledge-base/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)와 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 달리기 시합에서 누가 얼마나 빨랐는지 재려면 초시계와 기록표가 필요해요.
2. 이 개념은 네트워크가 어디서 느려졌는지 숫자로 찾아내는 도구예요.
3. 그래서 막연히 고치는 대신 가장 중요한 곳부터 똑똑하게 손볼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 204 / 1120

← **이전**: [1094. OSPF ABR / ASBR Area 위계 분산망](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1094_ospf_abr_asbr_area_hierarchy_routing/)
**다음**: [1096. EIGRP DUAL 지연 스케일 분산](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1096_eigrp_dual_algorithm_diffusing_update/) →

---
