+++
title = "1099. VLAN 간 라우팅"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 간 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 평가와 고급 분석에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 간 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)을 이해하면 측정 정확도과 모델 적합성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- 842번 **[VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) ([가상 랜](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/245_vlan_virtual_lan_broadcast_control/))**: 1개의 물리적 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)를 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로 쪼개어 브로드캐스트 도메인을 분리하는 기술입니다.
- **절대 룰**: 10번 방([VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/), 영업부)에서 뿜어낸 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) L2 패킷은 죽었다 깨어나도 20번 방([VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 20, 인사부)으로 건너갈 수 없습니다. IP 대역도 다릅니다(`10.0.10.x` vs `10.0.20.x`). 
- 서로 통신(핑)하려면 반드시 IP 주소를 읽고 꺾어주는 **L3 계층(네트워크 계층)의 우체국(라우터)**을 강제로 한 번 거쳐야만 합니다.

```text
[LACP 이더채널 포트 논리 그룹화]
    │
    ▼
[VLAN 간 라우팅]
    │
    └──▶ [스위치 포트 미러링]
```

- **📢 섹션 요약 비유**: [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 간 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

어떻게 분리된 방을 이어줄 것인가? 3번의 하드웨어/소프트웨어 혁명이 있었습니다.

### 1세대: 무식한 물리적 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) (Legacy) - "전선 도배"
- [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)에 10번 방 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)와 20번 방 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)가 있습니다.
- [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 위에 라우터 기계를 1대 삽니다.
- [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 10번 방 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) ➜ 랜선을 꽂아 라우터 1번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 연결.
- [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 20번 방 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) ➜ 랜선을 꽂아 라우터 2번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 연결.
- **단점**: [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 방이 50개면? 라우터에 구멍 50개가 필요하고 랜선 50개를 일일이 물리적으로 꽂아야 하는 미친 돈지랄 노가다가 터져 바로 멸망했습니다.

### 2세대: 라우터-온-어-스틱 (Router-on-a-Stick) 🌟 기출 🌟 - "외나무다리"
랜선 1개로 50개 방을 다 처리하는 궁극의 꼼수입니다.
- [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)와 라우터 사이에 **랜선(구리선) 딱 1개(스틱, Stick)**만 꽂습니다.
- 이 랜선 양쪽의 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 **802.1Q 트렁크 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)(Trunk [Port](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))** 모드로 바꿉니다. (트렁크는 모든 [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 번호 딱지가 붙은 패킷이 몽땅 섞여 지나갈 수 있는 톨게이트입니다.)
- **서브 인터페이스 (Sub-Interface 마법)**:
  - 껍데기 기계(라우터)에 뚫린 구멍은 1개(`FastEthernet 0/0`)인데, 라우터 뇌(소프트웨어) 안에다가 가상의 구멍(서브 인터페이스)을 칼로 쪼개어 만듭니다.
  - `Fa0/0.10` 구멍: "난 [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 껍데기 달고 오는 놈들 전용 문이다!"
  - `Fa0/0.20` 구멍: "난 [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 20 전용 문!"
- **작동**: 영업부 패킷이 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)를 나와 트렁크 1차선 얇은 외나무다리(스틱)를 타고 라우터로 쏙 올라가면, 라우터가 방 번호 딱지를 보고 서브 구멍에 넣어 L3 길 찾기를 해준 뒤 180도 유턴시켜서 인사부 방으로 확 꽂아줍니다.
- **단점 (병목 현상)**: 모든 부서의 트래픽이 이 얇은 외나무다리 랜선 1가닥으로 미친 듯이 몰렸다 돌아가느라(헤어핀 트래픽) 병목이 오지게 터져서 다운로드 속도가 바닥을 칩니다.

### 3세대: L3 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) (SVI 기법) 🌟 현대 대세 🌟 - "뇌를 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 안에 박아라"
외나무다리 병목에 개빡친 시스코가 칼을 갈았습니다.
- **개념**: 라우터 기계와 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 기계를 합쳐버립니다. **L3 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) (멀티레이어 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/))**라는 쇳덩어리를 삽니다. 겉모습은 그냥 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)가 48개 달린 L2 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)인데, 기계 뱃속에 **L3 라우터의 뇌([ASIC](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/070_asic/) [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 칩셋)**를 집어넣은 트랜스포머입니다.
- **SVI ([Switch](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) Virtual Interface) 마법**:
  - [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 소프트웨어 설정창에 들어가서 가상의 IP 문을 뚫습니다. `interface vlan 10`, `interface vlan 20`. 
  - 영업부([VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)) 패킷이 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 1번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 쏙 들어옵니다. 패킷이 밖(라우터)으로 나갈 필요가 아예 없습니다!
  - **[스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 뱃속 안에서 0.0001초 만에 칩셋이 "아 이거 20번 방 가네?" 하고 L3 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)을 즉석에서 꺾어버린 뒤, 곧장 20번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 빛의 속도로 꽂아버립니다.** 외부 랜선 병목 제로! 미친 속도 뻥튀기! 전 세계 모든 기업의 코어/분배 망 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 L3 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)(SVI)로 통일된 이유입니다.

```text
[LACP 이더채널 포트 논리 그룹화]
    │
    ▼
[VLAN 간 라우팅]
    │
    └──▶ [스위치 포트 미러링]
```

- **📢 섹션 요약 비유**: 기존 **[VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 쪼개기**는 하나의 커다란 운동장을 영업부와 인사부가 절대 섞이지 못하게 **'유리로 된 10미터짜리 거대한 방음벽'**으로 둘로 쪼개놓은 것입니다. 두 부서는 서로 쳐다만 볼 뿐 평생 엑셀 서류를 건넬 수 없습니다. 서류를 건네주려면(인터-[VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)) 방법이 필요합니다. 1세대 **무식한 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)**은 벽마다 사다리 50개를 세워두는 돈지랄입니다. 2세대 **라우터-온-어-스틱(Router-on-a-stick)**은 두 구역 사이에 딱 1개의 **'공용 좁은 계단(스틱, 트렁크 랜선 1개)'**을 세워두고, 꼭대기에 옥탑방 우체국장(라우터)을 앉혀둔 것입니다. 영업부원이 계단을 낑낑대고 올라가서 우체국장에게 서류를 주면, 국장이 도장을 찍어 반대편 인사부 계단으로 굴려 내려줍니다. 하지만 모든 부서원이 이 계단 1개로만 몰리니 계단이 무너질 듯 정체됩니다(스틱 병목). 최종 진화형 3세대 **L3 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) (SVI)**는 아예 계단을 싹 다 부수고, 방음벽 유리창 한가운데에 **'빛의 속도로 서류만 통과시켜 주는 마법의 자동 우체통(가상 SVI 인터페이스)'** 구멍을 뚫어버린 것입니다. 부서원이 밖으로 계단을 오르지 않고 벽에 서류를 툭 던지기만 하면 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 기계 뱃속 안에서 0.1초 만에 반대편 부서로 서류가 직빵으로 꽂히는 궁극의 고속 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 융합 머신입니다.

---

## Ⅲ. 비교 및 연결

[VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 간 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. LACP [이더채널](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [그룹화](/knowledge-base/studynote/02_operating_system/09_file_system/535_grouping_counting_free_space/)가 기반 조건을 만든다면, [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 간 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)은 그 위에서 핵심 메커니즘을 구현하고, [스위치 포트 미러링](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1100_port_mirroring_span_tap_network_monitoring/)은 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 측정 정확도과 모델 적합성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | LACP [이더채널](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [그룹화](/knowledge-base/studynote/02_operating_system/09_file_system/535_grouping_counting_free_space/)의 기반 정리 | [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 간 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)의 핵심 동작 | [스위치 포트 미러링](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1100_port_mirroring_span_tap_network_monitoring/)의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 측정 정확도 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 간 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 간 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)을 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 LACP [이더채널](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [그룹화](/knowledge-base/studynote/02_operating_system/09_file_system/535_grouping_counting_free_space/) 수준의 기본 대책으로 충분한지, 아니면 [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 간 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)이 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [스위치 포트 미러링](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1100_port_mirroring_span_tap_network_monitoring/)와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 측정 정확도 부족인지, 모델 적합성 악화인지 먼저 분리한다.
2. [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 간 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 [스위치 포트 미러링](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1100_port_mirroring_span_tap_network_monitoring/)와의 연계 방식을 함께 검증한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 간 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- LACP [이더채널](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [그룹화](/knowledge-base/studynote/02_operating_system/09_file_system/535_grouping_counting_free_space/)와의 경계를 정리하지 않아 중복 투자나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 간 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)을 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 간 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 평가와 고급 분석을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 측정 정확도 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [스위치 포트 미러링](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1100_port_mirroring_span_tap_network_monitoring/), [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 간 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| LACP [이더채널](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [그룹화](/knowledge-base/studynote/02_operating_system/09_file_system/535_grouping_counting_free_space/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) ([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)) | 실제 전달 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 나타내는 대표 지표다. |
| [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) ([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) | 사용자 체감 품질을 좌우한다. |
| [스위치 포트 미러링](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1100_port_mirroring_span_tap_network_monitoring/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: LACP 이더채널 포트 논리 그룹화]
    │
    ▼
[현재 개념: VLAN 간 라우팅]
    │
    ├──▶ [확장 A: 스위치 포트 미러링]
    └──▶ [확장 B: AI 기반 성능 예측]
```

[VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 간 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)는 LACP [이더채널](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [그룹화](/knowledge-base/studynote/02_operating_system/09_file_system/535_grouping_counting_free_space/)에서 출발해 현재 메커니즘을 정교화하고, 이후 [스위치 포트 미러링](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1100_port_mirroring_span_tap_network_monitoring/)와 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 달리기 시합에서 누가 얼마나 빨랐는지 재려면 초시계와 기록표가 필요해요.
2. 이 개념은 네트워크가 어디서 느려졌는지 숫자로 찾아내는 도구예요.
3. 그래서 막연히 고치는 대신 가장 중요한 곳부터 똑똑하게 손볼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 208 / 1120

← **이전**: [1098. LACP 이더채널 포트 논리 그룹화](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1098_lacp_etherchannel_link_aggregation_port/)
**다음**: [109. RTS/CTS (Request To Send / Clear To Send)](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/109_RTS_CTS_은닉노드문제/) →

---
