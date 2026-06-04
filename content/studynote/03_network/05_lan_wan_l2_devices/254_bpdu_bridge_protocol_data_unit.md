+++
title = "254. BPDU (Bridge Protocol Data Unit)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: BPDU는 LAN/WAN과 2계층 장비에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: BPDU를 이해하면 스위칭 효율과 브로드캐스트 범위 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)들이 Spanning Tree [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) ([STP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/)) 정보를 교환하기 위해 사용하는 [멀티캐스트](/knowledge-base/studynote/03_network/06_network_layer_ip/298_ip_classes_a_b_c_d_multicast_e_experimental/) 전용 프레임. (목적지 MAC이 `01:80:C2:00:00:00`인 특수 프레임)
- **필요성**: [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) A, B, C가 원형으로 연결되어 있을 때, 서로 말 한마디 섞지 않고 누가 대장([Root Bridge](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/255_root_bridge_rp_dp_bp/))을 할지, 어느 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 막을지(Block) 눈치 게임으로 정할 수는 없다. 누군가는 "내 아이디가 1등이야!"라고 소리쳐야 하고, 나머지는 "알겠습니다 대장!"이라고 응답해야 한다. 이 통신수단이 BPDU다.

- **💡 비유**: BPDU는 마피아 조직([스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 네트워크)의 두목을 뽑기 위한 <strong>"명함 교환식"</strong>과 같습니다. 2초마다 조직원들끼리 명함을 돌리며 서로의 '전투력(우선순위 값)'을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고 서열을 유지합니다. 만약 두목이 20초(Max Age) 동안 명함을 돌리지 않으면 "두목이 경찰에 잡혀갔다(선로 끊어짐)!"라고 판단하고 새로운 두목 선거를 엽니다.

```text
[스패닝 트리 프로토콜]
    |
    v
[BPDU]
    |
    +---> [루트 브리지, 루트 포트, 지정 포트, 차단…]
```

- **📢 섹션 요약 비유**: <strong> BPDU는 <a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a>들끼리만 사용하는 </strong>"암호가 걸린 무전기 채널"**입니다. 이 무전으로 선거 유세를 하고 대열(Tree)을 유지하며, 일반 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)(사용자 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))는 이 무전 채널을 전혀 듣지 못합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 두 가지 형태의 BPDU
[STP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) 세계에서는 평시와 비상시를 나누어 두 가지의 명함을 쓴다.

1. <strong>Configuration BPDU (<a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a> BPDU)</strong>:
   - 대장([Root Bridge](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/255_root_bridge_rp_dp_bp/)) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 "내가 대장이야, 다들 잘 지내고 있지?"라며 **2초(Hello Time)에 한 번씩** 주기적으로 뿜어내는 엽서다.
   - 쫄따구 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)들은 이 엽서를 받아보고 "아 대장님 살아계시네" 안심하며 자신의 다른 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 이 엽서를 전달(Relay)해 준다.
2. **TCN BPDU (Topology Change Notification)**:
   - 비상 연락망이다. 쫄따구 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)의 꽂혀 있던 선이 갑자기 툭 빠지거나 끊어지면(토폴로지 변화), 쫄따구가 대장을 향해 "대장님! 큰일 났습니다! 선이 하나 끊어졌습니다!"라고 위로 쏘아 올리는 긴급 경보다.

```text
 +-------------------------------------------------------------+
 |                Configuration BPDU의 핵심 내용물               |
 +-------------------------------------------------------------+
 |                                                             |
 |   +-----------------------------------------------------+   |
 |   | Root ID  : 이 마을 대장님의 ID (우선순위 + 대장 MAC)       |   |
 |   | Cost     : 대장님 집까지 가는 데 드는 거리(비용) 누적값     |   |
 |   | Bridge ID: 이 명함을 뿌린 내 ID (우선순위 + 내 MAC)        |   |
 |   | Port ID  : 이 명함이 뿜어져 나간 내 포트 번호             |   |
 |   | Timers   : Hello Time(2초), Max Age(20초) 등 규정시간    |   |
 |   +-----------------------------------------------------+   |
 |                                                             |
 |   * 선거 원칙: 스위치는 남의 BPDU를 받으면 자기 정보와 비교하여,    |
 |     상대방이 나보다 숫자가 작으면 무릎을 꿇고, 내가 작으면 이긴다!   |
 +-------------------------------------------------------------+
```

### 2. BPDU와 토폴로지 변경의 폭풍 (TCN 발생 시)
1. 말단 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)가 죽으면 TCN BPDU를 뿌린다.
2. 대장(Root)이 이 소식을 접하면, "동네 지형이 바뀌었으니, 너네가 외우고 있던 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 테이블 싹 다 폐기해!"라는 특수 명령(TC [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 세팅)을 담아 다음번 Configuration BPDU를 동네 전체에 뿌린다.
3. 이를 받은 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)들은 300초가 기준이던 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) [에이징](/knowledge-base/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) 타임을 15초로 확 줄여서 예전 지도([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 테이블)를 싹 날려버리고 처음부터 다시 학습([Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/))을 시작한다. (이 15초 동안은 엄청난 플러딩 트래픽이 발생한다)

- **📢 섹션 요약 비유**: BPDU의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

BPDU를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [스패닝 트리 프로토콜](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/253_spanning_tree_protocol_stp_ieee_802_1d/)이 기반 조건을 만든다면, BPDU는 그 위에서 핵심 메커니즘을 구현하고, [루트 브리지](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/255_root_bridge_rp_dp_bp/), 루트 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), 지정 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), 차단…는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 스위칭 효율과 브로드캐스트 범위에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [스패닝 트리 프로토콜](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/253_spanning_tree_protocol_stp_ieee_802_1d/)의 기반 정리 | BPDU의 핵심 동작 | [루트 브리지](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/255_root_bridge_rp_dp_bp/), 루트 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), 지정 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), 차단…의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 스위칭 효율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: BPDU는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

사내 직원이 장난으로 자기 자리에 싸구려 공유기([허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/))를 하나 가져와 벽 랜포트에 꽂고 둥글게 루프를 만들면 회사 망이 터진다.
또한 해커가 조작된 BPDU(우선순위 0번)를 만들어 쏘면 자기가 대장 행세를 하며 트래픽을 가로챈다.
이를 막기 위해 일반 PC나 프린터가 연결되는 <strong>Access <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a>에는 반드시 <code>spanning-tree bpduguard enable</code> 명령어를 입력</strong>해 두어야 한다. 이 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 BPDU 패킷이 단 1개라도 들어오는 순간 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 "어? 여긴 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 자리인데 왜 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 명함이 날아오지?" 하며 즉시 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 완전히 셧다운(Error-Disabled) 시켜 망을 보호한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: <strong> BPDU는 <a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a>들의 </strong>"신분증과 심장박동 센서"**가 결합된 것입니다. 2초마다 쿵쾅거리는 박동(Hello)이 멈추면 조직은 비상사태(TCN)를 선포하고 새로운 수술([STP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) 재계산)에 들어갑니다.

---

## Ⅴ. 기대효과 및 결론

BPDU는 LAN/WAN과 2계층 장비를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 스위칭 효율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [루트 브리지](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/255_root_bridge_rp_dp_bp/), 루트 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), 지정 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), 차단…, 지능형 캠퍼스 패브릭, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 지능형 캠퍼스 패브릭 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: BPDU는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [스패닝 트리 프로토콜](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/253_spanning_tree_protocol_stp_ieee_802_1d/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 ([Media](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) [Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/) Address) | 2계층 전달 대상을 식별하는 기본 주소다. |
| [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) ([Switch](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)) | 프레임을 적절한 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 전달하는 핵심 장비다. |
| [루트 브리지](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/255_root_bridge_rp_dp_bp/), 루트 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), 지정 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), 차단… | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 스패닝 트리 프로토콜]
    |
    v
[현재 개념: BPDU]
    |
    +---> [확장 A: 루트 브리지, 루트 포트, 지정 포트, 차단…]
    +---> [확장 B: 지능형 캠퍼스 패브릭]
```

BPDU는 [스패닝 트리 프로토콜](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/253_spanning_tree_protocol_stp_ieee_802_1d/)에서 출발해 현재 메커니즘을 정교화하고, 이후 [루트 브리지](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/255_root_bridge_rp_dp_bp/), 루트 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), 지정 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), 차단…와 지능형 캠퍼스 패브릭 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 학교 우편함에 이름표가 붙어 있어야 편지가 엉뚱한 곳에 가지 않아요.
2. 이 개념은 어느 교실로 보내야 할지 알아보는 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 규칙과 같아요.
3. 그래서 같은 건물 안에서도 편지가 더 빠르고 질서 있게 움직여요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 375 / 1120

<- **이전**: [253. 스패닝 트리 프로토콜 (STP, Spanning Tree Protocol)](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/253_spanning_tree_protocol_stp_ieee_802_1d/)
**다음**: [255. 루트 브리지 (Root Bridge), 루트 포트 (RP), 지정 포트 (DP), 차단 포트 (BP, Non-Designated)](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/255_root_bridge_rp_dp_bp/) ->

---
