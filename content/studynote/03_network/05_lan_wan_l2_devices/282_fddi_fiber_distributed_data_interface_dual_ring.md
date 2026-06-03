+++
title = "282. FDDI (Fiber Distributed Data Interface)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: FDDI는 LAN/WAN과 2계층 장비에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: FDDI를 이해하면 스위칭 효율과 브로드캐스트 범위 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: ANSI(미국국립표준협회)와 ISO가 제정한 100Mbps 속도의 광섬유 [토큰 링](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/281_token_ring_ieee_802_5_token_bus_ieee_802_4/) LAN/MAN [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/). [토큰 패싱](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/115_token_passing/)([Token Passing](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/115_token_passing/)) 알고리즘을 사용하므로 충돌이 발생하지 않는다.
- **필요성**: 1980년대 말 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)(10Mbps)과 일반 [토큰 링](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/281_token_ring_ieee_802_5_token_bus_ieee_802_4/)(16Mbps)은 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 수십 대를 연결하기엔 충분했지만, A건물, B건물, C건물의 거대한 네트워크들을 하나로 묶어주는 메인 척추(Backbone) 역할을 하기에는 속도가 너무 느리고, 거리가 짧았으며(구리선의 한계), 한번 끊어지면 대형 사고가 났다. 따라서 "수십 km를 가면서도 속도는 10배 빠르고, 포크레인이 선을 파먹어도 즉각 복구되는 궁극의 튼튼한 척추"가 절실했다.

- **💡 비유**: FDDI는 건물을 잇는 **"지하철 순환선(2호선)"**과 같습니다. 동네 마을버스([이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/))가 모아온 승객([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))들을 한꺼번에 싣고 다른 동네로 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/)(광케이블)으로 실어 나릅니다. 내선 순환과 외선 순환(이중 링)이 다 있어서 한쪽 터널이 무너져도 반대 방향 열차로 어떻게든 승객을 실어 나를 수 있습니다.

```text
[토큰 링]
    │
    ▼
[FDDI]
    │
    └──▶ [DQDB]
```

- **📢 섹션 요약 비유**: ** 일반 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 랜선이 집 안에서 쓰는 **"플라스틱 수도관"**이라면, FDDI는 도시 전체의 물탱크를 연결하기 위해 땅속 깊숙이 묻어둔 **"절대 터지지 않는 초대형 강철 이중 배관(백본)"**입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 이중 링(Dual Ring)과 노드 종류
FDDI 네트워크는 물리적으로 2개의 광케이블 링으로 구성된다.
- **Primary Ring (주 링)**: 평상시에 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 토큰이 시계 방향으로 쌩쌩 도는 메인 도로.
- **Secondary Ring (부 링)**: 평상시엔 텅 비어있다가, 주 링이 끊어지면 반시계 방향으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 돌려 살려내는 스페어 도로.

노드(라우터나 대형 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/))가 이 링에 어떻게 물리느냐에 따라 두 종류로 나뉜다.
- **[DAS](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/339_das/) (Dual Attachment [Station](/knowledge-base/studynote/03_network/04_data_link_layer_error/218_hdlc_station_primary_secondary/))**: 메인 링과 예비 링 양쪽 모두에 랜카드가 꽂혀 있는 비싼 녀석. (백본망의 주요 기둥들)
- **SAS (Single Attachment [Station](/knowledge-base/studynote/03_network/04_data_link_layer_error/218_hdlc_station_primary_secondary/))**: 돈이 없어서 메인 링에만 꽂혀 있는 녀석. 중간에 배선기(Concentrator)를 거쳐서 간접적으로 연결된다.

### 2. 셀프 힐링(Self-Healing): 무중단 복구의 마법
포크레인이 땅을 파다가 노드 B와 노드 C 사이의 케이블을 완전히 절단 냈다고 가정해 보자.
1. 노드 B와 C는 자신들 사이의 빛 신호가 사라진 것을 0.001초 만에 감지한다.
2. 노드 B는 오른쪽(C 방향)으로 주 링을 쏘지 못하게 되자, 주 링의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 내부에서 꺾어 **부 링(반시계 방향)으로 U턴** 시켜버린다. (Wrap 과정)
3. 노드 C 역시 왼쪽(B 방향)으로 쏘지 못하자, 부 링에서 오던 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주 링으로 U턴 시킨다.
4. 끊어진 부분을 제외한 거대한 C자 모양의 새로운 하나의 링이 완성되며 통신 단절 없이 네트워크가 100% 복구된다.

```text
 ┌─────────────────────────────────────────────────────────────┐
 │                 FDDI의 이중 링 자가 복구(Self-Healing)         │
 ├─────────────────────────────────────────────────────────────┤
 │                                                             │
 │   [ 평상시 ]                          [ 장애 발생 시 (U턴) ]       │
 │                                                             │
 │     ▶ 주 링(시계) ▶                      ▶ 주 링(시계) ▶        │
 │  ┌─ A ────── B ─┐                 ┌─ A ────── B ┐       │
 │  │   ◀ 부 링 ◀   │ 포크레인 절단!     │   ◀ 부 링 ◀   │ U턴!   │
 │  │              │    ====X====▶   │              X       │
 │  │   ◀ 부 링 ◀   │                 │   ◀ 부 링 ◀   │ U턴!   │
 │  └─ D ────── C ─┘                 └─ D ────── C ┘       │
 │     ▶ 주 링(시계) ▶                      ▶ 주 링(시계) ▶        │
 │                                                             │
 │   결과: 링이 끊어졌지만, B와 C가 내부에서 링을 꼬아서 이어버려       │
 │        거대한 "하나의 말굽 자석(U자) 모양"으로 망이 유지된다!        │
 └─────────────────────────────────────────────────────────────┘
```

### 3. FDDI의 소멸과 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)의 승리
아무리 완벽해도 도태될 수밖에 없었다. 광케이블 랜카드 2개([DAS](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/339_das/))를 꽂아야 하는 FDDI 라우터는 한 대에 수천만 원이 넘었다.
그 사이 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 진영(IEEE 802.3)은 [UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) 구리선 8가닥을 다 꼬아 쓰는 기염을 토하며 가격이 10분의 1도 안 되는 **"패스트 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)(100Mbps)"**과 **"기가비트 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)(1Gbps)"**을 시장에 쏟아부었다. 신뢰성은 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)([STP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/)/LACP)로 때워버렸다. FDDI는 가성비에서 압살당하며 2000년대 초반에 흔적도 없이 사라졌다.

- **📢 섹션 요약 비유**: ** FDDI는 타이어에 펑크가 나도 100km/h로 계속 달릴 수 있는 **"최첨단 방탄 군용 장갑차"**였습니다. 하지만 민간인(기업)들은 그 비싼 장갑차를 사는 대신, 펑크 나면 타이어를 빨리 갈아 끼우면([STP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/)) 되는 **"10배 빠르고 저렴한 스포츠카(기가 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/))"**를 선택했습니다.

---

## Ⅲ. 비교 및 연결

FDDI를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [토큰 링](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/281_token_ring_ieee_802_5_token_bus_ieee_802_4/)이 기반 조건을 만든다면, FDDI는 그 위에서 핵심 메커니즘을 구현하고, DQDB는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 스위칭 효율과 브로드캐스트 범위에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [토큰 링](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/281_token_ring_ieee_802_5_token_bus_ieee_802_4/)의 기반 정리 | FDDI의 핵심 동작 | DQDB의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 스위칭 효율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: FDDI는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 FDDI를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [토큰 링](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/281_token_ring_ieee_802_5_token_bus_ieee_802_4/) 수준의 기본 대책으로 충분한지, 아니면 FDDI가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 DQDB와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 스위칭 효율 부족인지, 브로드캐스트 범위 악화인지 먼저 분리한다.
2. FDDI가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 DQDB와의 연계 방식을 함께 검증한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- FDDI의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [토큰 링](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/281_token_ring_ieee_802_5_token_bus_ieee_802_4/)와의 경계를 정리하지 않아 중복 투자나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: FDDI를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

FDDI는 LAN/WAN과 2계층 장비를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 스위칭 효율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [DQDB](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/283_dqdb_distributed_queue_dual_bus_ieee_802_6/), 지능형 캠퍼스 패브릭, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 지능형 캠퍼스 패브릭 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: FDDI는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [토큰 링](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/281_token_ring_ieee_802_5_token_bus_ieee_802_4/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 ([Media](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) [Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/) Address) | 2계층 전달 대상을 식별하는 기본 주소다. |
| [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) ([Switch](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)) | 프레임을 적절한 포트로 전달하는 핵심 장비다. |
| [DQDB](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/283_dqdb_distributed_queue_dual_bus_ieee_802_6/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 토큰 링]
    │
    ▼
[현재 개념: FDDI]
    │
    ├──▶ [확장 A: DQDB]
    └──▶ [확장 B: 지능형 캠퍼스 패브릭]
```

FDDI는 [토큰 링](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/281_token_ring_ieee_802_5_token_bus_ieee_802_4/)에서 출발해 현재 메커니즘을 정교화하고, 이후 DQDB와 지능형 캠퍼스 패브릭 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 학교 우편함에 이름표가 붙어 있어야 편지가 엉뚱한 곳에 가지 않아요.
2. 이 개념은 어느 교실로 보내야 할지 알아보는 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 규칙과 같아요.
3. 그래서 같은 건물 안에서도 편지가 더 빠르고 질서 있게 움직여요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 403 / 1120

← **이전**: [281. 토큰 링 (Token Ring)](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/281_token_ring_ieee_802_5_token_bus_ieee_802_4/)
**다음**: [283. DQDB (Distributed Queue Dual Bus)](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/283_dqdb_distributed_queue_dual_bus_ieee_802_6/) →

---
