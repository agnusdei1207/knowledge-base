---
title: "STP, Spanning Tree Protocol"
date: "2026-05-08"
tags:
  - "studynote-network"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)은 LAN/WAN과 2계층 장비에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 이해하면 스위칭 효율과 브로드캐스트 범위 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [STP](/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) (Spanning Tree [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))는 IEEE 802.1D로 표준화된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층(2계층) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)로, 물리적으로 루프가 존재하는 네트워크 위에서 논리적으로 루프를 끊어낸 안전한 '트리' 구조의 경로를 실시간으로 자동 연산해 내는 알고리즘이다. 라디아 펄만(Radia Perlman)이 발명했다.
- **필요성**: 기업 네트워크에서 메인 선로 하나가 끊어졌다고 직원 1000명이 인터넷을 못 쓰면 난리가 난다. 그래서 네트워크 설계자들은 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 간에 백업용 선(Redundancy)을 주렁주렁 달아 놓는다. 하지만 이렇게 다중 연결을 하면 100% 확률로 [브로드캐스트 스톰](/studynote/03_network/20_performance_evaluation_advanced/1097_broadcast_storm_switching_loop_stp/)(L2 루핑)이 발생해 1초 만에 망이 박살 난다. "선은 연결하되, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 무한히 돌지 못하게 한쪽 길을 임시로 잠가줄 똑똑한 신호등"이 절실했다.

- **💡 비유**: 한강 다리가 끊어질까 봐 다리를 2개(메인 다리, 예비 다리) 지어 놨습니다. 그런데 차들이 두 다리를 통해 뺑글뺑글 꼬리물기(루핑)를 하며 교통 체증([브로드캐스트 스톰](/studynote/03_network/20_performance_evaluation_advanced/1097_broadcast_storm_switching_loop_stp/))을 유발합니다. STP는 <strong>예비 다리 입구에 "바리케이드(Block)"를 쳐서 평소엔 못 지나가게 막아두다가, 메인 다리가 무너지면 바리케이드를 치우고 예비 다리를 쓰게 해주는 톨게이트 관리자</strong>입니다.

```text
[MAC 주소 호핑]
    |
    v
[스패닝 트리 프로토콜]
    |
    +---> [BPDU]
```

- **📢 섹션 요약 비유**: ** STP는 거미줄처럼 엉킨 실타래(루프 네트워크)를 가위로 싹둑싹둑 잘라서, 물이 역류하지 않고 폭포수처럼 위에서 아래로만 흐르는 **"완벽한 나무뿌리 모양(Spanning Tree)의 물길"**로 정돈해 주는 조경사입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

STP는 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 전원을 켜자마자 자기들끼리 "[BPDU](/studynote/03_network/05_lan_wan_l2_devices/254_bpdu_bridge_protocol_data_unit/)"라는 엽서를 주고받으며 다음의 3단계 선거와 계산을 수행한다.

### 1단계: 전체 대장 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 선출 ([Root Bridge](/studynote/03_network/05_lan_wan_l2_devices/255_root_bridge_rp_dp_bp/))
- [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 마을에 단 한 명의 대장(Root)을 뽑는다. 기준은 <strong><a href="/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/">브리지</a> ID(<a href="/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/">Bridge</a> ID)</strong>가 가장 낮은(작은) 놈이다.
- [브리지](/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) ID = `우선순위 번호(Priority) + 스위치의 MAC 주소`.
- 모든 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)의 기본 우선순위는 32,768이다. 우선순위가 같으면 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소가 가장 낮은(공장에서 제일 옛날에 생산된) 고물 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 대장이 되는 참사가 벌어질 수 있으므로, 관리자는 메인 코어 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)의 우선순위를 `4096` 등 낮게 강제 설정하여 대장으로 만들어야 한다.

### 2단계: 대장에게 가는 가장 빠른 길 찾기 (Root [Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 선출)
- 대장([루트 브리지](/studynote/03_network/05_lan_wan_l2_devices/255_root_bridge_rp_dp_bp/))이 아닌 나머지 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)(Non-[Root Bridge](/studynote/03_network/05_lan_wan_l2_devices/255_root_bridge_rp_dp_bp/))들은 "내 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)들 중에 대장님한테 가는 가장 빠른 길이 어디지?"를 계산한다. 이 가장 빠르고 짧은 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 <strong>루트 <a href="/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a>(<a href="/studynote/03_network/07_network_layer_routing/370_pim_rp_rendezvous_point_rpf_loop_prevention/">RP</a>)</strong>라 부르며, 한 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)당 무조건 딱 1개만 열린다.
- 기준(Cost)은 100Mbps 선은 Cost 19, 1Gbps 광랜은 Cost 4로, 값이 적을수록 빠른 길이다.

### 3단계: 도로의 통행권 배분 (Designated [Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) / Block [Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))
- 이제 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)와 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)를 연결하는 '각각의 랜선([Segment](/studynote/03_network/08_transport_layer/407_tcp_segment_header_structure_20_60_bytes/))'마다 "이 선을 주도적으로 쓸 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)는 둘 중 누구지?"를 가린다. 이 뚫려 있는 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)가 <strong>지정 <a href="/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a>(DP)</strong>다.
- 대장(Root) [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)의 모든 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)는 항상 DP다.
- 남은 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 중에서, RP도 아니고 DP도 못 된 불쌍한 패배자 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)는 **차단(Block, Non-Designated)** 모드로 들어가 입을 다문다. 루프가 완벽히 끊어지는 순간이다.

```text
 +-------------------------------------------------------------+
 |                STP 동작 결과 도식 (루프 차단 과정)               |
 +-------------------------------------------------------------+
 |                                                             |
 |            [ 루트 브리지 (대장!) ]                             |
 |             (우선순위: 4096)                                |
 |             DP ↙            ↘ DP                          |
 |      (Cost 4) /              \ (Cost 4)                   |
 |             ↙                  ↘                          |
 |         RP ↙                    ↘ RP                      |
 |    [ 스위치 B ] ---- (예비선) ---- [ 스위치 C ]                 |
 |              DP                BLOCK                        |
 |                                                             |
 |   * 설명:                                                     |
 |   1) 대장은 우선순위가 낮은 위쪽 스위치.                          |
 |   2) B와 C는 대장으로 가는 RP(Root Port)를 하나씩 개통.           |
 |   3) 밑의 예비선(B와 C 연결선)은 루프를 만드므로 닫아야 함.          |
 |   4) C의 포트가 가위바위보(계산)에서 져서 BLOCK 처리됨.             |
 |   5) 이로써 물리적으론 삼각형이지만, 논리적으론 'ㅅ' 모양(트리)이 됨!  |
 +-------------------------------------------------------------+
```

### 3. STP의 50초 [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) 문제
초창기 802.1D 표준 STP는 선로가 끊어졌을 때(장애 발생), 막아두었던 Block [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 열어 통신을 복구하는 데 무려 <strong>50초(Max Age 20 + Listening 15 + <a href="/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/">Learning</a> 15)</strong>라는 끔찍하게 긴 시간이 걸렸다. 현대의 고속 네트워크에서 50초 단절은 치명적이므로, 이를 개선하여 1초 만에 복구하는 <strong><a href="/studynote/03_network/05_lan_wan_l2_devices/260_rstp_rapid_spanning_tree_protocol_ieee_802_1w/">RSTP</a> (<a href="/studynote/03_network/05_lan_wan_l2_devices/260_rstp_rapid_spanning_tree_protocol_ieee_802_1w/">Rapid STP</a>, 802.1w)</strong>가 현재 업계의 기본 표준으로 자리 잡았다.

- **📢 섹션 요약 비유**: <strong> STP는 각 <a href="/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a>들이 서로 명함(<a href="/studynote/03_network/05_lan_wan_l2_devices/254_bpdu_bridge_protocol_data_unit/">BPDU</a>)을 교환하여 </strong>서열(대장, 중간, 쫄따구)을 딱 정리한 다음, 쓸데없는 곁가지 도로에 바리케이드를 치는 완벽한 계급 기반의 교통정리 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)**입니다.

---

## Ⅲ. 비교 및 연결

[스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 호핑이 기반 조건을 만든다면, [스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)은 그 위에서 핵심 메커니즘을 구현하고, BPDU는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 스위칭 효율과 브로드캐스트 범위에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 호핑의 기반 정리 | [스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 핵심 동작 | BPDU의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 스위칭 효율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 호핑 수준의 기본 대책으로 충분한지, 아니면 [스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 BPDU와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 스위칭 효율 부족인지, 브로드캐스트 범위 악화인지 먼저 분리한다.
2. [스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 BPDU와의 연계 방식을 함께 검증한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 호핑와의 경계를 정리하지 않아 중복 투자나 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: [스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)은 LAN/WAN과 2계층 장비를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 스위칭 효율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [BPDU](/studynote/03_network/05_lan_wan_l2_devices/254_bpdu_bridge_protocol_data_unit/), 지능형 캠퍼스 패브릭, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 지능형 캠퍼스 패브릭 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 호핑 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 ([Media](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) [Access Control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/) Address) | 2계층 전달 대상을 식별하는 기본 주소다. |
| [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) ([Switch](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)) | 프레임을 적절한 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 전달하는 핵심 장비다. |
| [BPDU](/studynote/03_network/05_lan_wan_l2_devices/254_bpdu_bridge_protocol_data_unit/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: MAC 주소 호핑]
    |
    v
[현재 개념: 스패닝 트리 프로토콜]
    |
    +---> [확장 A: BPDU]
    +---> [확장 B: 지능형 캠퍼스 패브릭]
```

[스패닝 트리](/studynote/03_network/19_frequent_topics_terms/959_spanning_tree_protocol_stp_loop_avoidance/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)는 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 호핑에서 출발해 현재 메커니즘을 정교화하고, 이후 BPDU와 지능형 캠퍼스 패브릭 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 학교 우편함에 이름표가 붙어 있어야 편지가 엉뚱한 곳에 가지 않아요.
2. 이 개념은 어느 교실로 보내야 할지 알아보는 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 규칙과 같아요.
3. 그래서 같은 건물 안에서도 편지가 더 빠르고 질서 있게 움직여요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 374 / 1120

<- **이전**: [252. MAC 주소 호핑 (MAC Flapping)](/studynote/03_network/05_lan_wan_l2_devices/252_mac_address_hopping_flapping/)
**다음**: [254. BPDU (Bridge Protocol Data Unit)](/studynote/03_network/05_lan_wan_l2_devices/254_bpdu_bridge_protocol_data_unit/) ->

---
