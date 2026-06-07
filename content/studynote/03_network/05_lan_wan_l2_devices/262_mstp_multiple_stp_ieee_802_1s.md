---
title: "MSTP (Multiple STP)"
date: "2026-05-08"
tags:
  - "studynote-network"
weight: 262
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MSTP는 LAN/WAN과 2계층 장비에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: MSTP를 이해하면 스위칭 효율과 브로드캐스트 범위 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 여러 개의 VLAN을 하나의 [스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/) 인스턴스(MSTI)로 매핑(묶음 처리)하여, 네트워크에 존재하는 [스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/)의 개수를 획기적으로 줄이는 IEEE 국제 표준 규격.
- **필요성**: [VLAN](/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/), 20, 30... 1000이 있다고 치자.
  - 1개의 트리만 쓰면(CST), A~B 간의 우회 선로는 영원히 차단(Block)되어 비싼 돈 주고 깐 광케이블이 평생 놀고먹는다. ([로드 밸런싱](/studynote/03_network/16_data_center_cloud/833_load_balancing_l4_l7_switch_traffic_distribution/) 불가)
  - 그래서 시스코는 VLAN마다 트리를 그렸다(PVST). "[VLAN](/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 10은 A선로로, [VLAN](/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 20은 B선로로 가게 하자!" ([로드 밸런싱](/studynote/03_network/16_data_center_cloud/833_load_balancing_l4_l7_switch_traffic_distribution/) 가능). 하지만 VLAN이 1000개면 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 1000개의 BPDU를 2초마다 찍어내느라 뇌(CPU)가 타버린다.
  - **해결책**: "[VLAN](/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 1~500은 1번 그룹으로, 501~1000은 2번 그룹으로 묶자! 그럼 트리는 딱 2개만 계산하면 되잖아!" 이것이 MSTP의 탄생 배경이다.

- **💡 비유**: 1000명의 택배 기사([VLAN](/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/))가 매일 본사로 출근합니다.
  - **CST**: 1000명이 모두 똑같은 1번 도로만 쓰고, 2번 도로는 텅 비워둠. (비효율)
  - **PVST**: 1000명에게 각자 내비게이션 경로를 1000장 그려줌. (본사 직원 과로사)
  - **MSTP**: "1번~500번 기사는 1번 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)(인스턴스 1)에 타! 501~1000번 기사는 2번 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)(인스턴스 2)에 타!" (고작 2대의 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 경로만 관리하면 완벽한 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 탑승 완료!)

```text
[백업 포트, 대체 포트 추가]
    |
    v
[MSTP]
    |
    +---> [이더채널 / 링크 어그리게이션]
```

- **📢 섹션 요약 비유**: <strong> MSTP는 수백 개의 점조직(<a href="/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/">VLAN</a>)들을 성향이 비슷한 몇 개의 </strong>"연합 조직(Instance)"**으로 통폐합하여, [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 관리해야 할 서류([BPDU](/studynote/03_network/05_lan_wan_l2_devices/254_bpdu_bridge_protocol_data_unit/)) 더미를 획기적으로 줄여주는 구조조정 전문가입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/)는 [로드 밸런싱](/studynote/03_network/16_data_center_cloud/833_load_balancing_l4_l7_switch_traffic_distribution/)([Load Balancing](/studynote/02_operating_system/03_cpu_scheduling/196_hard_soft_real_time/))과 CPU 부하의 딜레마 속에서 세 가지 형태로 진화했다.

### 1. CST (Common Spanning Tree) - IEEE 802.1D
- **특징**: [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 네트워크 전체를 통틀어 물리적 토폴로지 위에 <strong>단 1개</strong>의 [스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/)만 돌린다.
- **장점**: [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) CPU 부하가 매우 적다. (계산할 트리가 하나뿐이니까)
- **단점**: [VLAN](/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 10과 [VLAN](/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 20이 가는 길이 똑같다. 차단(Block)된 예비 링크는 어떤 VLAN의 데이터도 보낼 수 없어 대역폭의 50%가 낭비된다.

### 2. PVST+ (Per-[VLAN](/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) Spanning Tree Plus) - [Cisco](/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/) 전용
- **특징**: [VLAN](/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 1개당 [스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/)를 1개씩 <strong>개별적으로(Per-<a href="/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/">VLAN</a>)</strong> 돌린다.
- **장점**: [VLAN](/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 10은 1번 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 쓰게 하고(2번 막음), [VLAN](/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 20은 2번 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 쓰게 할 수 있다(1번 막음). 막힌 링크 없이 완벽한 <strong><a href="/studynote/03_network/16_data_center_cloud/833_load_balancing_l4_l7_switch_traffic_distribution/">로드 밸런싱</a>(부하 <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>)</strong>이 가능하다.
- **단점**: 대규모 엔터프라이즈 환경에서 VLAN이 500개라면, [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 초당 500개의 [BPDU](/studynote/03_network/05_lan_wan_l2_devices/254_bpdu_bridge_protocol_data_unit/) 패킷을 처리해야 하므로 저사양 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 CPU 100%를 치고 뻗어버린다. (Scalability 부족)

### 3. MSTP (Multiple Spanning Tree [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)) - IEEE 802.1s
- **특징**: 여러 개의 VLAN을 묶어서 하나의 **MSTI(Multiple Spanning Tree Instance)** 그룹을 만든다.
- <strong><a href="/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a> 예시</strong>:
  - `Instance 1`: [VLAN](/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/), 20, 30을 할당 (이 그룹은 메인 링크 사용)
  - `Instance 2`: [VLAN](/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 40, 50, 60을 할당 (이 그룹은 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 링크 사용)
- **장점**: [로드 밸런싱](/studynote/03_network/16_data_center_cloud/833_load_balancing_l4_l7_switch_traffic_distribution/)(PVST의 장점)을 완벽히 달성하면서도, [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 계산할 트리는 단 2개(Instance 1, 2)뿐이므로 CPU 부하(CST의 장점)까지 완벽하게 잡아낸 현존 최고의 [STP](/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) 아키텍처다. 밑바탕 알고리즘은 [RSTP](/studynote/03_network/05_lan_wan_l2_devices/260_rstp_rapid_spanning_tree_protocol_ieee_802_1w/)(802.1w)를 사용하므로 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간도 1초로 매우 빠르다.

```text
 +-------------------------------------------------------------+
 |                STP 방식별 CPU 부하 vs 로드밸런싱 비교           |
 +-------------------------------------------------------------+
 |                                                             |
 |   1. CST  (1개 트리) : 부하 낮음 😇 / 로드 밸런싱 안됨 😡        |
 |   2. PVST (VLAN수 트리): 부하 폭발 😡 / 로드 밸런싱 완벽 😇        |
 |   3. MSTP (몇 개 트리) : 부하 낮음 😇 / 로드 밸런싱 완벽 😇        |
 |                                                             |
 |  * MSTP는 그룹(Instance)이라는 바구니에 VLAN을 담는 마법의 기술!   |
 +-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: <strong> 개별 학생(<a href="/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/">VLAN</a>) 1000명의 성적을 일일이 관리(PVST)하다가 쓰러지기 일보 직전인 교사에게, 학생들을 </strong>"문과반(Instance 1)과 이과반(Instance 2)"** 두 반으로만 나누어 그룹별 평균만 관리하게 만들어준 획기적인 교육청 시스템이 바로 MSTP입니다.

---

## Ⅲ. 비교 및 연결

MSTP를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [백업 포트](/studynote/03_network/05_lan_wan_l2_devices/261_rstp_backup_port_and_alternate_port/), 대체 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 추가가 기반 조건을 만든다면, MSTP는 그 위에서 핵심 메커니즘을 구현하고, [이더채널](/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) / 링크 어그리게이션은 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 스위칭 효율과 브로드캐스트 범위에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [백업 포트](/studynote/03_network/05_lan_wan_l2_devices/261_rstp_backup_port_and_alternate_port/), 대체 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 추가의 기반 정리 | MSTP의 핵심 동작 | [이더채널](/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) / 링크 어그리게이션의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 스위칭 효율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: MSTP는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 MSTP를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [백업 포트](/studynote/03_network/05_lan_wan_l2_devices/261_rstp_backup_port_and_alternate_port/), 대체 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 추가 수준의 기본 대책으로 충분한지, 아니면 MSTP가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [이더채널](/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) / 링크 어그리게이션와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 스위칭 효율 부족인지, 브로드캐스트 범위 악화인지 먼저 분리한다.
2. MSTP가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 [이더채널](/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) / 링크 어그리게이션와의 연계 방식을 함께 검증한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- MSTP의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [백업 포트](/studynote/03_network/05_lan_wan_l2_devices/261_rstp_backup_port_and_alternate_port/), 대체 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 추가와의 경계를 정리하지 않아 중복 투자나 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: MSTP를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

MSTP는 LAN/WAN과 2계층 장비를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 스위칭 효율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [이더채널](/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) / 링크 어그리게이션, 지능형 캠퍼스 패브릭, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 지능형 캠퍼스 패브릭 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: MSTP는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [백업 포트](/studynote/03_network/05_lan_wan_l2_devices/261_rstp_backup_port_and_alternate_port/), 대체 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 추가 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 ([Media](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) [Access Control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/) Address) | 2계층 전달 대상을 식별하는 기본 주소다. |
| [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) ([Switch](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)) | 프레임을 적절한 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 전달하는 핵심 장비다. |
| [이더채널](/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) / 링크 어그리게이션 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 백업 포트, 대체 포트 추가]
    |
    v
[현재 개념: MSTP]
    |
    +---> [확장 A: 이더채널 / 링크 어그리게이션]
    +---> [확장 B: 지능형 캠퍼스 패브릭]
```

MSTP는 [백업 포트](/studynote/03_network/05_lan_wan_l2_devices/261_rstp_backup_port_and_alternate_port/), 대체 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 추가에서 출발해 현재 메커니즘을 정교화하고, 이후 [이더채널](/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) / 링크 어그리게이션와 지능형 캠퍼스 패브릭 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 학교 우편함에 이름표가 붙어 있어야 편지가 엉뚱한 곳에 가지 않아요.
2. 이 개념은 어느 교실로 보내야 할지 알아보는 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 규칙과 같아요.
3. 그래서 같은 건물 안에서도 편지가 더 빠르고 질서 있게 움직여요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 383 / 1120

<- **이전**: [261. 백업 포트 (Backup Port), 대체 포트 (Alternate Port) 추가](/studynote/03_network/05_lan_wan_l2_devices/261_rstp_backup_port_and_alternate_port/)
**다음**: [263. 이더채널 (EtherChannel) / 링크 어그리게이션 (LACP, IEEE 802.3ad/802.1AX)](/studynote/03_network/05_lan_wan_l2_devices/263_etherchannel_link_aggregation_lacp/) ->

---
