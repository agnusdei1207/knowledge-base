---
title: "182. Llc Logical Link Control"
date: "2026-05-06"
tags:
  - "studynote-network"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/) (Logical Link Control)는 IEEE (Institute of Electrical and Electronics 엔진ers) 802 구조에서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층의 상위 부계층으로, 서로 다른 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) ([Media](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) [Access Control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/)) 방식 위에 공통된 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 인터페이스를 제공한다.
> 2. **가치**: 상위 계층 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)해 적절한 수신자에게 넘기고, 필요하면 연결·흐름·[오류 제어](/studynote/03_network/04_data_link_layer_error/188_error_control_overview/) 모델까지 정의함으로써 "[매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)마다 다른 2계층"을 "상위 계층이 이해하기 쉬운 공통 창구"로 바꾼다.
> 3. **판단 포인트**: 시험에서는 LLC를 MAC과 구분해 설명해야 하고, 실무에서는 [Ethernet](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) II와 [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/)/SNAP (Subnetwork Access [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 확장 포함) 공존 구조를 이해해야 하며, 현대 LAN (Local Area Network)에서 LLC의 실제 역할은 주로 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)에 가깝다는 점을 놓치면 안 된다.

---

## Ⅰ. 개요 및 필요성

LLC는 <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 링크 계층을 상하 두 층으로 나눴을 때, 상위 계층과 맞닿아 있는 <a href="/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a> 제어 부분</strong>이다. IEEE 802 계열 표준은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층 전체를 하나로 두지 않고, [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 접근과 물리적 전송 특성을 다루는 MAC과, 상위 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)과의 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 연결을 다루는 LLC로 분리했다. 이 분할 덕분에 상위 계층은 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/), [토큰 링](/studynote/03_network/05_lan_wan_l2_devices/281_token_ring_ieee_802_5_token_bus_ieee_802_4/), 무선 LAN (Wireless Local Area Network) 같은 서로 다른 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 차이를 직접 알지 않아도 된다.

이 구조가 필요해진 이유는 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)가 다양해졌기 때문이다. 만약 상위 계층이 링크 종류마다 별도의 2계층 규칙을 알아야 했다면, 같은 IP (Internet [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)) 패킷이라도 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)마다 다른 방식으로 해석하고 전달해야 한다. IEEE 802는 이를 피하기 위해 <strong>"위로는 공통 창구, 아래로는 <a href="/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/">매체</a>별 구현"</strong>이라는 분업 구조를 만든 것이다.

따라서 LLC의 본질은 물리 전송을 직접 제어하는 계층이 아니라, <strong><a href="/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/">매체</a> 독립적인 <a href="/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a> 인터페이스를 제공하는 계층</strong>이다. 상위 계층은 LLC를 통해 "어느 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)인지", "어떤 형태의 링크 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 필요한지"를 표현하고, MAC은 실제 프레임 전송과 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 접근을 처리한다.

- **📢 섹션 요약 비유**: LLC는 여러 종류의 배달 수단 위에 놓인 공통 접수 창구와 같아서, 고객은 오토바이인지 트럭인지 몰라도 같은 양식으로 택배를 맡길 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

LLC의 핵심 기능은 <strong>상위 <a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a> <a href="/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/">식별</a>과 공통 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 모델 제공</strong>이다. 기본 [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/) 헤더는 DSAP (Destination [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [Access Point](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)), SSAP (Source [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [Access Point](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)), Control 필드로 구성되며, 필요하면 SNAP (Subnetwork Access [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)) 확장이 뒤에 붙는다. 이때 SAP ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [Access Point](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/))는 "이 프레임을 어느 상위 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이나 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 사용자에게 넘길 것인가"를 가리키는 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 접점이다.

| 요소 | 역할 | 실무 포인트 |
| :--- | :--- | :--- |
| DSAP (Destination [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [Access Point](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)) | 수신 측 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | 어떤 상위 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)로 올릴지 결정 |
| SSAP (Source [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [Access Point](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)) | 송신 측 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 송신자 정보 제공 |
| Control 필드 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 형식 표현 | 비연결형/연결형 제어 정보 반영 |
| SNAP (Subnetwork Access [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)) | SAP 한계 확장 | 더 많은 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) 지원 |
| [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 부계층 | 실제 프레임 전송 | 주소 지정, [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 접근, FCS (Frame Check Sequence) 처리 담당 |

SNAP 확장 안에는 OUI (Organizationally Unique [Identifier](/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/))와 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)가 들어가므로, 원래 SAP 공간만으로 표현하기 어려운 상위 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)도 구분할 수 있다. 대표적으로 [IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) (Internet [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) version 4), [IPv6](/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/) (Internet [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) version 6), [ARP](/studynote/03_network/06_network_layer_ip/312_arp_address_resolution_protocol_ip_to_mac/) ([Address Resolution Protocol](/studynote/03_network/06_network_layer_ip/312_arp_address_resolution_protocol_ip_to_mac/)) 같은 상위 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 이 경로로 구분한다. 아래 그림은 LLC가 상위 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)과 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 사이에서 어떻게 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)를 수행하는지 보여 준다.

```text
+--------------------------------------------------------------------+
| IEEE 802 data link split and demultiplexing                       |
+--------------------------------------------------------------------+
| Network Layer                                                     |
|   IPv4 / IPv6 / ARP / other protocols                            |
|              |                                                     |
|              v                                                     |
| LLC : DSAP / SSAP / Control                                       |
|              |                                                     |
|     optional SNAP : OUI + protocol identifier                     |
|              |                                                     |
| MAC : frame delivery, addressing, medium access, FCS              |
|              |                                                     |
| Ethernet / Wi-Fi / Token Ring / other IEEE 802 media             |
+--------------------------------------------------------------------+
```

이 구조에서 LLC가 하는 가장 중요한 일은 <strong>상위 <a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a>을 구분해 주는 것</strong>이다. 수신 측은 [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/) 정보를 보고 이 프레임이 [IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) (Internet [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) version 4)인지, [IPv6](/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/) (Internet [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) version 6)인지, [ARP](/studynote/03_network/06_network_layer_ip/312_arp_address_resolution_protocol_ip_to_mac/) ([Address Resolution Protocol](/studynote/03_network/06_network_layer_ip/312_arp_address_resolution_protocol_ip_to_mac/))인지 판단해 올바른 상위 처리기로 보낸다. SAP만으로 부족한 경우에는 SNAP이 붙어 더 넓은 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 공간을 제공한다.

또한 IEEE 802.2는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 모델도 정의한다. Type 1은 비연결형 무응답 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), Type 2는 연결형 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), Type 3은 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 응답형 비연결 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)다. 하지만 현대의 일반적인 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 환경에서는 LLC가 복잡한 [오류 제어](/studynote/03_network/04_data_link_layer_error/188_error_control_overview/)를 적극 수행하기보다, <strong>간단한 <a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a> <a href="/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/">식별</a> 계층</strong>에 가깝게 쓰이는 경우가 많다.

- **📢 섹션 요약 비유**: LLC는 편지 봉투 앞면에 "이건 세무팀, 이건 인사팀"이라고 써서, 같은 우편실로 들어와도 알맞은 부서로 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)해 주는 사무실 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 담당과 같다.

---

## Ⅲ. 비교 및 연결

LLC를 제대로 이해하려면, 그것이 MAC과 역할이 다르고, 또 실제 프레임 형식에서는 [Ethernet](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) II와도 관계가 있다는 점을 함께 봐야 한다. LLC는 <strong><a href="/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a>적 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>와 <a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a> 구분</strong>, MAC은 <strong>물리적 프레임 전달과 <a href="/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/">매체</a> 접근</strong>을 담당한다. 한편 실제 유선 LAN에서는 [Ethernet](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) II 형식이 널리 쓰이기 때문에, [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)이 LLC가 아니라 EtherType으로 이뤄지는 경우도 많다.

| 형식/개념 | [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 위치 | 주 역할 | 오늘날 관찰 포인트 |
| :--- | :--- | :--- | :--- |
| [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) ([Media](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) [Access Control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/)) | [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 헤더 내부 주소/제어 | 주소 지정, [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 접근, 프레임 전송 | [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 특성에 직접 의존 |
| [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/) (Logical Link Control) | SAP 또는 SNAP | 상위 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/), 공통 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 모델 | 802 구조의 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 창구 |
| [Ethernet](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) II | [EtherType](/studynote/03_network/05_lan_wan_l2_devices/235_type_field_ethertype_length_ipv4_arp/) | 상위 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)을 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 프레임 안에서 직접 처리 | 유선 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)의 주류 형식 |
| 802.3 + [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/)/SNAP | [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/) + SNAP | 802 구조 유지하면서 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 확장 | 802.[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/) [브리지](/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) 환경 등에서 중요 |

이 비교에서 핵심은 LLC가 "없어진" 것이 아니라, <strong>환경에 따라 드러나는 정도가 달라졌다는 점</strong>이다. 순수 802 아키텍처 관점에서는 LLC가 매우 중요하지만, 실제 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 환경에서는 [EtherType](/studynote/03_network/05_lan_wan_l2_devices/235_type_field_ethertype_length_ipv4_arp/) 기반 [Ethernet](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) II가 더 익숙하게 보인다. 반면 무선 LAN과 유선 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 사이를 [브리지](/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)할 때는 [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/)/SNAP이 다시 의미를 갖는다.

또한 [오류 제어](/studynote/03_network/04_data_link_layer_error/188_error_control_overview/) 관점에서도 경계를 분명히 해야 한다. [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/) 표준은 연결형 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)까지 정의하지만, 현대 LAN에서 재전송과 품질 제어는 종종 MAC이나 상위 전송 계층에서 처리된다. 그래서 시험 답안에서는 "LLC가 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 제어를 정의한다"와 "실제 현대 환경에서 어느 정도 쓰이는가"를 함께 설명해야 완성도가 높다.

- **📢 섹션 요약 비유**: LLC와 MAC의 관계는 회사의 접수 데스크와 배송 기사 관계와 같아서, 데스크는 문서를 어느 부서로 보낼지 정하고 기사는 실제 길을 달려 전달한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 LLC는 주로 <strong>프레임 해석과 상위 <a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a> <a href="/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/">식별</a>을 정확히 이해하는 문제</strong>로 나타난다. 패킷 캡처를 볼 때 목적지 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 뒤의 2바이트가 길이(Length)인지, EtherType인지에 따라 해석이 갈린다. 일반적으로 그 값이 1500 이하이면 IEEE 802.3 길이 필드로 보고 이후 [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/)/[LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/)-SNAP을 해석하고, 1536 이상이면 [Ethernet](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) II EtherType으로 해석한다.

### 실무 판단 기준

1. <strong>현재 링크가 <a href="/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/">Ethernet</a> II인가, 802.3 + LLC인가?</strong> 프레임 해석의 출발점이 달라진다.
2. <strong>상위 <a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a> <a href="/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/">식별</a>이 SAP로 충분한가?</strong> 부족하면 SNAP 확장이 필요하다.
3. <strong>재전송과 <a href="/studynote/03_network/04_data_link_layer_error/188_error_control_overview/">오류 제어</a>를 어디에 둘 것인가?</strong> 현대 LAN에서는 LLC보다 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 또는 전송 계층이 더 큰 역할을 한다.
4. <strong><a href="/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/">브리지</a> 환경인가?</strong> 802.11과 [Ethernet](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 간 변환에서는 [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/)/SNAP 이해가 중요하다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- LLC와 MAC을 같은 개념처럼 설명해 계층 분리를 흐리는 것
- 현대 유선 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)이 모두 순수 IEEE 802.2 [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/) 형식으로 동작한다고 단정하는 것
- [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/) Type 2가 정의되어 있다는 이유만으로, 실제 LAN에서 링크 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)이 거기서 보장된다고 오해하는 것

기술사 답안에서는 "LLC는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층 상부에서 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)와 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 모델을 담당하고, MAC은 실제 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 접근을 담당한다"는 문장을 축으로 가져가면 좋다. 여기에 <strong><a href="/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/">Ethernet</a> II와 <a href="/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/">LLC</a>/SNAP 공존</strong>, <strong>현대 환경에서의 실질 역할 축소</strong>를 덧붙이면 더 정확한 설명이 된다.

- **📢 섹션 요약 비유**: LLC는 회의실 예약 시스템처럼 누구 방으로 연결할지 정하는 규칙이고, MAC은 실제 엘리베이터와 복도를 움직여 문서를 전달하는 수단과 같다.

---

## Ⅴ. 기대효과 및 결론

LLC의 가장 큰 효과는 <strong><a href="/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/">매체</a>마다 다른 링크 기술 위에 공통된 <a href="/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a> 인터페이스를 얹었다</strong>는 점이다. 덕분에 상위 계층은 링크 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)의 세부 차이를 모두 알지 않아도 되고, 네트워크 스택은 역할을 분리한 채 확장될 수 있었다. 즉 LLC는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층을 "그냥 프레임을 보내는 기술"에서 "상위 계층과 연결되는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 계층"으로 정리해 준 표준화 장치였다.

하지만 현대 네트워크에서는 LLC가 항상 전면에 보이지는 않는다. 유선 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)은 [Ethernet](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) II를 많이 쓰고, [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 제어는 MAC이나 전송 계층으로 넘어간 경우가 많다. 그럼에도 [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/) 개념은 여전히 중요하다. 왜냐하면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층을 MAC과 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 제어로 분해해 이해하지 않으면, 802 계열 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 설계 철학과 프레임 해석 원리를 놓치기 때문이다.

정리하면 LLC는 <strong>"<a href="/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/">매체</a> 독립적인 <a href="/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a> 창구"</strong>로 기억하는 것이 가장 정확하다. 현대 실무에서는 늘 전면에 드러나지 않더라도, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층의 상부 책임이 무엇인지 설명하는 핵심 개념으로 남아 있다.

- **📢 섹션 요약 비유**: LLC는 배송 수단이 바뀌어도 같은 접수 양식을 유지하게 해 주는 창구라서, 뒤에서 어떤 차량이 움직이든 앞단 사용자는 같은 방식으로 일을 맡길 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) ([Media](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) [Access Control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/)) | [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/) 아래에서 실제 프레임 전달과 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 접근을 담당한다 |
| SAP ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [Access Point](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)) | LLC가 상위 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 구분하는 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 접점이다 |
| DSAP / SSAP | 수신자와 송신자 측 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 필드다 |
| SNAP (Subnetwork Access [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)) | SAP 공간 한계를 보완해 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)을 확장한다 |
| [Ethernet](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) II | 현대 유선 LAN에서 자주 쓰이는 대안적 캡슐화 형식이다 |
| IEEE 802.3 | 길이 필드와 [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/) 해석을 연결하는 표준이다 |
| IEEE 802.[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/) | [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/)/SNAP 이해가 중요한 무선 LAN 표준이다 |
| FCS (Frame Check Sequence) | LLC가 아니라 주로 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 수준 프레임 검증과 연결된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
다양한 IEEE 802 매체 등장
        |
        v
데이터 링크 계층의 역할 분리 필요
        |
        v
LLC (논리 제어) + MAC (매체 접근) 구조
        |
        +---------------> SAP 기반 상위 프로토콜 다중화
        +---------------> SNAP으로 식별 공간 확장
        +---------------> Ethernet II와 공존하는 현대 캡슐화 해석
```

이 흐름도는 LLC가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층 분업 구조에서 출발해, 현대 LAN의 프레임 형식 해석까지 이어지는 개념임을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. LLC는 편지가 어느 친구에게 가야 하는지 이름표를 붙여 주는 규칙이에요.
2. 그래서 같은 우체국 차를 타더라도 편지는 알맞은 친구 책상으로 갈 수 있어요.
3. 컴퓨터도 [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/) 덕분에 여러 종류의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 헷갈리지 않고 나눠 보낼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 303 / 1120

<- **이전**: [181. 데이터 링크 계층의 역할: 프레이밍, 흐름 제어, 오류 제어, 회선 제어](/studynote/03_network/04_data_link_layer_error/181_data_link_layer_roles/)
**다음**: [183. 매체 접근 제어 (MAC, Media Access Control) - IEEE 802.3~802.11](/studynote/03_network/04_data_link_layer_error/183_mac_media_access_control/) ->

---
