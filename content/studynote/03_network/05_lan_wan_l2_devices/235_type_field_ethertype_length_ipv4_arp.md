---
title: "IPv4 = 0x0800, ARP = 0x0806"
date: "2026-05-08"
tags:
  - "studynote-network"
weight: 235
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Type 필드 / Length 필드는 LAN/WAN과 2계층 장비에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: Type 필드 / Length 필드를 이해하면 스위칭 효율과 브로드캐스트 범위 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 통신에서 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 필드가 "누구에게(Who)"를 나타낸다면, Type/Length 2바이트 필드는 "무엇을(What)" 혹은 "얼마나(How much)"를 나타낸다. 현재 대부분의 통신은 [Ethernet](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) II 기반이므로 이 필드는 <strong>Ethertype (이더타입)</strong>이라고 널리 불린다.
- **필요성**: 컴퓨터의 네트워크 인터페이스([NIC](/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/))는 케이블에서 0과 1의 전기 신호를 받아 조립한 뒤, 껍데기([MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 헤더)를 벗기고 알맹이(페이로드)를 CPU([운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))로 올려보내야 한다. 그런데 알맹이가 IP 주소 기반의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)인지, 아니면 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소를 묻는 [ARP](/studynote/03_network/06_network_layer_ip/312_arp_address_resolution_protocol_ip_to_mac/) 요청인지 구별할 수 없다면 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 처리할 수 없다. Ethertype은 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)에게 "이건 IP 관련 부서로 보내라"라고 지시하는 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 태그 역할을 한다.

- **💡 비유**: Ethertype은 택배 박스 겉면에 붙어있는 <strong>"취급 주의 / 내용물 표시 스티커"</strong>와 같습니다. 박스에 '신선 식품(`0x0800` [IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/))' 스티커가 붙어 있으면 우편집중국([운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))은 이를 냉장 창고(IP 처리 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/))로 보내고, '가전제품(`0x0806` [ARP](/studynote/03_network/06_network_layer_ip/312_arp_address_resolution_protocol_ip_to_mac/))' 스티커가 붙어 있으면 일반 창고([ARP](/studynote/03_network/06_network_layer_ip/312_arp_address_resolution_protocol_ip_to_mac/) 처리 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/))로 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)해 줍니다.

```text
[Preamble & SFD]
    |
    v
[Type 필드 / Length 필드]
    |
    +---> [페이로드 크기, 패딩]
```

- **📢 섹션 요약 비유**: ** Ethertype은 병원의 **"접수창구 진료과목 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)표"**입니다. 환자([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 도착하면 안내 데스크([MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 계층)가 내과([IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/))로 보낼지, 외과([ARP](/studynote/03_network/06_network_layer_ip/312_arp_address_resolution_protocol_ip_to_mac/))로 보낼지 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)해 주는 완벽한 교통정리 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 상위 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) (Demultiplexing)
[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크(L2) 계층에서 네트워크(L3) 계층으로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 올려보낼 때, Ethertype은 <strong>역다중화(Demultiplexing)</strong>의 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 역할을 한다. 하위 계층([이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 하나)이 상위 계층(IP, [ARP](/studynote/03_network/06_network_layer_ip/312_arp_address_resolution_protocol_ip_to_mac/), [IPv6](/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/) 등 여러 개)을 지원할 수 있게 해 주는 아키텍처의 핵심이다.

```text
 +-------------------------------------------------------------+
 |                 Ethertype에 의한 상위 계층 역다중화            |
 +-------------------------------------------------------------+
 |                                                             |
 |   OSI 3계층 (네트워크)        [ IPv4 모듈 ]  [ ARP 모듈 ]  [ IPv6 모듈 ] |
 |                                   ^            ^            ^      |
 |                                   |            |            |      |
 |                            0x0800 |     0x0806 |     0x86DD |      |
 |                                   |            |            |      |
 |   OSI 2계층 (데이터 링크)      [    MAC 계층 (Ethertype 확인)    ] |
 |                                   ^                                |
 |                                   |                                |
 |   OSI 1계층 (물리)             [ 이더넷 케이블 (010101...) ]         |
 |                                                             |
 +-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Type 필드 / Length 필드의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

Type 필드 / Length 필드를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. Preamble & SFD가 기반 조건을 만든다면, Type 필드 / Length 필드는 그 위에서 핵심 메커니즘을 구현하고, [페이로드 크기](/studynote/03_network/05_lan_wan_l2_devices/236_payload_size_and_padding_46_1500_bytes/), [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)은 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 스위칭 효율과 브로드캐스트 범위에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | Preamble & SFD의 기반 정리 | Type 필드 / Length 필드의 핵심 동작 | [페이로드 크기](/studynote/03_network/05_lan_wan_l2_devices/236_payload_size_and_padding_46_1500_bytes/), [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 스위칭 효율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: Type 필드 / Length 필드는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

이더타입은 IEEE에서 표준으로 관리하며, 실무에서 패킷을 덤프 뜨거나 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)([ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)) 룰을 짤 때 이 16진수 코드를 직접 다뤄야 할 때가 많다.

| Ethertype (Hex) | 설명 ([프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)) | 비고 |
|:---|:---|:---|
| <strong><code>0x0800</code></strong> | <strong><a href="/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/">IPv4</a></strong> (Internet [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) version 4) | 현재 인터넷 트래픽의 대다수 |
| <strong><code>0x0806</code></strong> | <strong><a href="/studynote/03_network/06_network_layer_ip/312_arp_address_resolution_protocol_ip_to_mac/">ARP</a></strong> ([Address Resolution Protocol](/studynote/03_network/06_network_layer_ip/312_arp_address_resolution_protocol_ip_to_mac/)) | IP로 MAC을 찾기 위한 필수 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
| <strong><code>0x86DD</code></strong> | <strong><a href="/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/">IPv6</a></strong> (Internet [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) version 6) | 차세대 IP 주소 체계 |
| <strong><code>0x8100</code></strong> | <strong><a href="/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/">VLAN</a> Tag</strong> (IEEE 802.1Q) | [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) ([VLAN](/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/)) 태그 삽입 시 |

### 3. Length 필드로서의 동작 (IEEE 802.3의 경우)
만약 2바이트 값이 `0x05DC` (10진수로 1500) 이하라면, 이는 내용물이 무엇인지 알려주는 Type이 아니라 페이로드의 크기([바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/))를 의미하는 Length 필드로 동작한다. 이 경우 "내용물이 무엇인가?"에 대한 정보는 페이로드 내부에 숨어 있는 802.2 [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/)(Logical Link Control) 헤더의 DSAP/SSAP 필드를 열어봐야만 알 수 있다. (현대에는 Spanning Tree [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 등 구형 네트워킹 제어 메시지에서나 드물게 볼 수 있다.)

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: ** Type이냐 Length냐를 숫자의 크기(1500 기준)로 구분하는 것은, **"키가 150cm 이하이면 초등학생(Length 룰 적용), 153cm 이상이면 성인(Type 룰 적용)"**이라고 자동 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 게이트를 만들어 둔 것과 같은 극강의 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 꼼수입니다.

---

## Ⅴ. 기대효과 및 결론

Type 필드 / Length 필드는 LAN/WAN과 2계층 장비를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 스위칭 효율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [페이로드 크기](/studynote/03_network/05_lan_wan_l2_devices/236_payload_size_and_padding_46_1500_bytes/), [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/), 지능형 캠퍼스 패브릭, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 지능형 캠퍼스 패브릭 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: Type 필드 / Length 필드는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [Preamble & SFD](/studynote/03_network/05_lan_wan_l2_devices/234_preamble_and_sfd_start_of_frame_delimiter/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 ([Media](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) [Access Control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/) Address) | 2계층 전달 대상을 식별하는 기본 주소다. |
| [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) ([Switch](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)) | 프레임을 적절한 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 전달하는 핵심 장비다. |
| [페이로드 크기](/studynote/03_network/05_lan_wan_l2_devices/236_payload_size_and_padding_46_1500_bytes/), [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: Preamble & SFD]
    |
    v
[현재 개념: Type 필드 / Length 필드]
    |
    +---> [확장 A: 페이로드 크기, 패딩]
    +---> [확장 B: 지능형 캠퍼스 패브릭]
```

Type 필드 / Length 필드는 Preamble & SFD에서 출발해 현재 메커니즘을 정교화하고, 이후 [페이로드 크기](/studynote/03_network/05_lan_wan_l2_devices/236_payload_size_and_padding_46_1500_bytes/), [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)와 지능형 캠퍼스 패브릭 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 학교 우편함에 이름표가 붙어 있어야 편지가 엉뚱한 곳에 가지 않아요.
2. 이 개념은 어느 교실로 보내야 할지 알아보는 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 규칙과 같아요.
3. 그래서 같은 건물 안에서도 편지가 더 빠르고 질서 있게 움직여요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 356 / 1120

<- **이전**: [234. Preamble & SFD (Start of Frame Delimiter)](/studynote/03_network/05_lan_wan_l2_devices/234_preamble_and_sfd_start_of_frame_delimiter/)
**다음**: [236. 페이로드 크기 (46 ~ 1500 bytes), 패딩(Padding)](/studynote/03_network/05_lan_wan_l2_devices/236_payload_size_and_padding_46_1500_bytes/) ->

---
