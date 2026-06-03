+++
title = "1097. 브로드캐스트 스톰 (루프 발생)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 브로드캐스트 스톰은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 평가와 고급 분석에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: 브로드캐스트 스톰을 이해하면 측정 정확도과 모델 적합성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **Flooding (플러딩)**: 1075번에서 배웠듯, [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 모르는 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소나 `FF:FF:FF:FF:FF:FF` 같은 브로드캐스트([ARP](/knowledge-base/studynote/03_network/06_network_layer_ip/312_arp_address_resolution_protocol_ip_to_mac/)) 패킷을 받으면, 묻지도 따지지도 않고 **자기에 꽂힌 모든 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 복사해서 다 쏟아버립니다.**
- **[TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/)(수명)의 부재**: L3 라우터 패킷(IP)에는 `TTL`이라는 폭탄 타이머가 있어서 255번 점프하면 허공에서 자동 폭파됩니다. 하지만 L2 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패킷([이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 프레임)에는 이 **수명 타이머 껍데기가 아예 없습니다!** 한 번 던져진 패킷은 누군가 랜선을 뽑지 않는 한 우주가 멸망할 때까지 허공을 날아다닙니다.

```text
[EIGRP DUAL 지연 스케일 분산]
    │
    ▼
[브로드캐스트 스톰]
    │
    └──▶ [LACP 이더채널 포트 논리 그룹화]
```

- **📢 섹션 요약 비유**: 브로드캐스트 스톰은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

신뢰도를 높이려고 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 3대를 **삼각형(물리적 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 루프)**으로 선을 꽂는 순간 지옥이 열립니다.

1. [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 1번이 "[ARP](/knowledge-base/studynote/03_network/06_network_layer_ip/312_arp_address_resolution_protocol_ip_to_mac/) 주소 좀요!" 하고 브로드캐스트 패킷 1개를 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) A에 던집니다.
2. [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) A는 멍청하니까, 그 1개를 **[스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) B와 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) C 두 방향으로 동시에 복사해서 쏩니다(플러딩).**
3. [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) B는 A한테 받은 걸 C한테 쏘고, C는 A한테 받은 걸 B한테 쏩니다. 
4. 이제 B와 C가 서로 주고받은 걸 또다시 복사해서 A, B, C 서로에게 미친 듯이 메아리치며 핑퐁 복제를 시작합니다.
5. **결과 (브로드캐스트 스톰)**: 패킷에 [TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/)(폭파 타이머)이 없기 때문에 죽지 않습니다. 1개가 2개, 4개, 100만 개로 1초 만에 기하급수적으로 자가 증식하여(폭풍), [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 사이의 1Gbps 랜선을 쓰레기 패킷으로 100% 가득 채워버립니다. 정상적인 인터넷 통신은 0.1초도 불가능해지며, 쇳덩어리 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 CPU가 100%를 찍고 다운(재부팅)됩니다.

```text
[EIGRP DUAL 지연 스케일 분산]
    │
    ▼
[브로드캐스트 스톰]
    │
    └──▶ [LACP 이더채널 포트 논리 그룹화]
```

- **📢 섹션 요약 비유**: 브로드캐스트 스톰의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

스톰이 불 때 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)의 뇌([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 테이블 장부)도 같이 타버립니다.
- [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) A의 장부: "아까 철수 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) `AA`) 패킷이 **1번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)**에서 왔지! 적어두자."
- 근데 빙글빙글 루핑을 타고 한 바퀴 돌아온 똑같은 철수 패킷이 이번엔 **2번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)**로 들어옵니다!
- [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) A의 뇌정지: "어? 철수가 1번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에서 2번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 순간이동 했네? 장부 2번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 수정!" 
- 1초에 수만 번 장부를 지웠다 썼다(Flapping) 하다가 램(RAM)이 꽉 차서 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 기계가 벽돌로 변해버립니다.

브로드캐스트 스톰을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [EIGRP](/knowledge-base/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)이 기반 조건을 만든다면, 브로드캐스트 스톰은 그 위에서 핵심 메커니즘을 구현하고, LACP [이더채널](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [그룹화](/knowledge-base/studynote/02_operating_system/09_file_system/535_grouping_counting_free_space/)는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 측정 정확도과 모델 적합성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [EIGRP](/knowledge-base/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)의 기반 정리 | 브로드캐스트 스톰의 핵심 동작 | LACP [이더채널](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [그룹화](/knowledge-base/studynote/02_operating_system/09_file_system/535_grouping_counting_free_space/)의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 측정 정확도 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: 브로드캐스트 스톰은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

843번(복습) STP가 이 지옥을 막기 위해 탄생했습니다. (IEEE 802.1D)
- 물리적으로 삼각형 랜선을 꽂아두더라도, [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)들끼리 0.1초 만에 대화를 나눠서 **[논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로 딱 1개의 길([포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))을 가위로 싹둑 잘라버립니다(Block).**
- 삼각형이 아니라 `ㄱ` 자 모양의 나뭇가지(Tree) 구조로 강제 변형시켜, 패킷이 빙글빙글 돌 수 있는 원형 트랙(루프) 자체를 애초에 원천 차단하는 가장 위대하고도 비효율적인 L2 보안 흑마법입니다. (선 하나를 일부러 끄고 놀려야 하므로 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 낭비가 발생함)

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: **스위칭 루프와 브로드캐스트 스톰**은 거울로 둘러싸인 밀실에서 **'메아리가 영원히 증폭되는 지옥'**과 같습니다. 컴퓨터가 "야!" 하고 소리 한 번을 질렀습니다. 그런데 벽([스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)) 3개가 원형으로 둥글게 둘러싸고 있어서, 그 소리가 1번 벽에서 2번 벽으로 튕기고, 2번에서 3번으로 튕기며 메아리가 복제되기 시작합니다. 심지어 이 메아리는 산에서처럼 점점 작아져서 죽는 것(라우터 [TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) 소멸)이 아니라, 벽에 튕길 때마다 스피커 앰프에 증폭되어 2배로 커집니다([스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 플러딩). 단 1초 만에 "야!" 소리가 수백만 겹의 폭음으로 변해 밀실 전체를 찢을 듯이 채워버려, 그 안에 있는 모든 사람([스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)와 서버)의 고막을 터뜨리고 기절시키는 끔찍한 폐쇄회로 핑퐁 재앙입니다. 이를 막는 **[STP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/)([스패닝 트리](/knowledge-base/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/))**는 밀실의 한쪽 벽(랜선 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 하나)을 강제로 허물어버려, 소리가 빙글빙글 돌지 못하고 밖으로 빠져나가 소멸하게 만드는 환풍구 뚫기 수술입니다.

---

## Ⅴ. 기대효과 및 결론

브로드캐스트 스톰은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 평가와 고급 분석을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 측정 정확도 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 LACP [이더채널](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [그룹화](/knowledge-base/studynote/02_operating_system/09_file_system/535_grouping_counting_free_space/), [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: 브로드캐스트 스톰은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [EIGRP](/knowledge-base/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) ([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)) | 실제 전달 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 나타내는 대표 지표다. |
| [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) ([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) | 사용자 체감 품질을 좌우한다. |
| LACP [이더채널](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [그룹화](/knowledge-base/studynote/02_operating_system/09_file_system/535_grouping_counting_free_space/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: EIGRP DUAL 지연 스케일 분산]
    │
    ▼
[현재 개념: 브로드캐스트 스톰]
    │
    ├──▶ [확장 A: LACP 이더채널 포트 논리 그룹화]
    └──▶ [확장 B: AI 기반 성능 예측]
```

브로드캐스트 스톰는 [EIGRP](/knowledge-base/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/) DUAL [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스케일 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)에서 출발해 현재 메커니즘을 정교화하고, 이후 LACP [이더채널](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [그룹화](/knowledge-base/studynote/02_operating_system/09_file_system/535_grouping_counting_free_space/)와 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 달리기 시합에서 누가 얼마나 빨랐는지 재려면 초시계와 기록표가 필요해요.
2. 이 개념은 네트워크가 어디서 느려졌는지 숫자로 찾아내는 도구예요.
3. 그래서 막연히 고치는 대신 가장 중요한 곳부터 똑똑하게 손볼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 206 / 1120

← **이전**: [1096. EIGRP DUAL 지연 스케일 분산](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1096_eigrp_dual_algorithm_diffusing_update/)
**다음**: [1098. LACP 이더채널 포트 논리 그룹화](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1098_lacp_etherchannel_link_aggregation_port/) →

---
