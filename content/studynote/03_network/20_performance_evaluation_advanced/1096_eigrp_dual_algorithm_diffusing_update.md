---
title: "1096. Eigrp Dual Algorithm Diffusing Update"
date: "2026-05-08"
tags:
  - "studynote-network"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [EIGRP](/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)은 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 평가와 고급 분석에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [EIGRP](/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)을 이해하면 측정 정확도과 모델 적합성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- <strong><a href="/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/">EIGRP</a></strong>는 기본적으로 옆 라우터의 소문을 믿고 장부([라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 테이블)를 갱신합니다(디스턴스 벡터).
- 하지만 30초마다 전체 장부를 멍청하게 다 던지는 RIP과 달리, **처음에만 전체를 주고받고, 그 뒤로는 '변화가 생긴 부분'만 살짝(부분 업데이트, Multicast) 던져서 네트워크 트래픽을 극단적으로 아낍니다.** (링크 상태의 장점 흡수)

```text
[BGP 속성]
    |
    v
[EIGRP DUAL 지연 스케일 분산]
    |
    +---> [브로드캐스트 스톰]
```

- **📢 섹션 요약 비유**: [EIGRP](/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

OSPF는 [다익스트라](/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/) 공식을 썼지만, EIGRP는 <strong>DUAL</strong>이라는 독자적인 미친 수학 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 돌립니다. 이 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 길을 고르고 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)을 비축하는 과정이 핵심입니다.

### 1. 복합 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) ([Metric](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)) 점수 계산 - 넓이와 딜레이
RIP처럼 거쳐 간 횟수(Hop) 따위로 길을 고르지 않습니다.
- <strong><a href="/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">대역폭</a> (<a href="/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">Bandwidth</a>)</strong>: 고속도로 차선 폭. (경로 중 가장 좁은 병목 구간의 속도)
- <strong><a href="/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a> (Delay)</strong>: 톨게이트 통과 시간의 누적 합. (장비 스케일 확장에 대비해 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 값을 곱하고 나눕니다.)
- K상수 공식(`K1~K5`)에 이 두 개를 섞어서 점수(Cost)를 미치도록 세밀하게 뽑아냅니다. [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)이 10Gbps로 넓고 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 적은 곳이 무조건 1등으로 선택됩니다.

### 2. 절대 끊기지 않는 마법: Successor와 Feasible Successor 🌟
DUAL [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 미리 계산해 두는 1등 길과 2등 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 길입니다.
- **Successor (석세서, 1등 길)**: DUAL 공식으로 계산해 낸 가장 빠르고 쾌적한 최적의 메인 경로입니다. 이 길로 패킷이 날아갑니다.
- <strong>Feasible Successor (피저블 석세서, 2등 <a href="/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/">백업</a> 길)</strong>: 이게 EIGRP의 흑마법입니다. 메인 길이 터졌을 때를 대비해, 조건을 만족하는 2등 길을 **토폴로지 테이블 주머니에 미리 계산해서 꿍쳐둡니다.**
  - **조건 (Feasibility Condition)**: "2등 길이 알려준 거리(AD)가 내가 지금 쓰는 1등 길 전체 거리(FD)보다 짧아야만 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)으로 둔다!" (그래야 빙빙 도는 루핑이 절대 안 생김)
- <strong>무중단 절체 (<a href="/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/">Failover</a>)</strong>: 포크레인이 1등 길(광케이블)을 푹 찍어서 끊어졌습니다. OSPF는 이때부터 "으아악 길 터졌다!" 하며 지도를 새로 그리고 수학 공식을 돌리느라(Convergence Time) 수 초 동안 패킷이 바닥에 버려집니다.
- **EIGRP의 기적**: 1등 길이 툭 끊기는 그 찰나! 주머니에 꿍쳐놨던 2등 길(Feasible Successor)을 <strong>단 0.001초 만에 꺼내서 <a href="/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a> 테이블(메인 길)로 쓱 올려버립니다.</strong> 수학 계산(DUAL)을 다시 할 필요가 아예 없기 때문에, 체감상 수렴 시간이 제로(0)에 수렴하는 극강의 회복력을 자랑합니다.

```text
[BGP 속성]
    |
    v
[EIGRP DUAL 지연 스케일 분산]
    |
    +---> [브로드캐스트 스톰]
```

- **📢 섹션 요약 비유**: [EIGRP](/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

- OSPF는 길이 2개인데 속도가 다르면, 무조건 빠른 길 1곳으로만 다 쏟아붓습니다(균등 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)만 가능).
- EIGRP는 **"속도가 2배 빠르면, 트래픽(짐)도 2배 많이 실어서 양쪽 길로 골고루 던져라!"** 라며, [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 다른 두 길의 비율에 맞춰서 데이터를 똑똑하게 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 펌핑(비균등 로드밸런싱, [Variance](/studynote/08_algorithm_stats/08_stats/136_variance/) 조절)해 주어 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 200% 다 쥐어짜 냅니다.

[EIGRP](/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이 기반 조건을 만든다면, [EIGRP](/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)은 그 위에서 핵심 메커니즘을 구현하고, [브로드캐스트 스톰](/studynote/03_network/20_performance_evaluation_advanced/1097_broadcast_storm_switching_loop_stp/)은 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 측정 정확도과 모델 적합성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)의 기반 정리 | [EIGRP](/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)의 핵심 동작 | [브로드캐스트 스톰](/studynote/03_network/20_performance_evaluation_advanced/1097_broadcast_storm_switching_loop_stp/)의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 측정 정확도 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [EIGRP](/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- 이 모든 기가 막힌 기능은 <strong>오직 시스코(<a href="/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/">Cisco</a>) 라우터 기계끼리만 통합니다.</strong> 회사에 싼 주니퍼나 화웨이 스위치가 1대라도 섞여 있으면 이 마법을 쓸 수 없어 결국 [OSPF](/studynote/03_network/07_network_layer_routing/357_ospf_open_shortest_path_first_overview/)(오픈 표준)로 울며 겨자 먹기로 돌아가야 하는 족쇄가 있었습니다. (최근에 오픈소스로 풀긴 했지만 이미 늦었습니다.)

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 기존 <strong><a href="/studynote/03_network/07_network_layer_routing/357_ospf_open_shortest_path_first_overview/">OSPF</a> <a href="/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a></strong>은 완벽주의자여서, 한강 다리 1개가 무너지면 그 자리에 멈춰 서서 <strong>'서울 시내 전체 지도를 처음부터 다시 그리고(<a href="/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/">다익스트라</a> <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a>) 재계산'</strong>하느라 차들이 한참 동안 오도 가도 못하고 길바닥에 멈춰 섰습니다(느린 수렴 시간). 시스코가 만든 <strong><a href="/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/">EIGRP</a>(DUAL <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a>)</strong>는 매일 출근길에 <strong>'메인 도로(1등 길)'와 '내비게이션 플랜 B 도로(2등 <a href="/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/">백업</a> 길)'를 수첩에 동시에 적어두는 천재 택시 기사</strong>입니다. 택시가 1등 한강 다리(Successor)를 타러 갔는데 다리가 공사 중입니다. 이 기사는 당황해서 지도를 다시 펴고 계산하지 않습니다. 0.1초 만에 주머니에서 수첩을 딱 꺼내어, 미리 계산해 둔 2등 마포대교(Feasible Successor)로 바로 핸들을 꺾어버립니다. 길 끊김을 감지하는 즉시 단 1초의 딜레이(계산 시간)도 없이 완벽한 플랜 B로 트래픽을 던져버리는, 장애 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 속도 우주 최강의 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 흑마법입니다.

---

## Ⅴ. 기대효과 및 결론

[EIGRP](/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)은 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 평가와 고급 분석을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 측정 정확도 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [브로드캐스트 스톰](/studynote/03_network/20_performance_evaluation_advanced/1097_broadcast_storm_switching_loop_stp/), [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [EIGRP](/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) ([Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)) | 실제 전달 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 나타내는 대표 지표다. |
| [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) ([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) | 사용자 체감 품질을 좌우한다. |
| [브로드캐스트 스톰](/studynote/03_network/20_performance_evaluation_advanced/1097_broadcast_storm_switching_loop_stp/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: BGP 속성]
    |
    v
[현재 개념: EIGRP DUAL 지연 스케일 분산]
    |
    +---> [확장 A: 브로드캐스트 스톰]
    +---> [확장 B: AI 기반 성능 예측]
```

[EIGRP](/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)는 [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)에서 출발해 현재 메커니즘을 정교화하고, 이후 [브로드캐스트 스톰](/studynote/03_network/20_performance_evaluation_advanced/1097_broadcast_storm_switching_loop_stp/)와 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 달리기 시합에서 누가 얼마나 빨랐는지 재려면 초시계와 기록표가 필요해요.
2. 이 개념은 네트워크가 어디서 느려졌는지 숫자로 찾아내는 도구예요.
3. 그래서 막연히 고치는 대신 가장 중요한 곳부터 똑똑하게 손볼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 205 / 1120

<- **이전**: [1095. BGP 속성 (Local Pref, MED, AS-path 구성비)](/studynote/03_network/20_performance_evaluation_advanced/1095_bgp_attributes_local_pref_med_as_path/)
**다음**: [1097. 브로드캐스트 스톰 (루프 발생)](/studynote/03_network/20_performance_evaluation_advanced/1097_broadcast_storm_switching_loop_stp/) ->

---
