---
title: "223. LAPD (Link Access Procedure on the D channel)"
date: "2026-05-08"
tags:
  - "studynote-network"
weight: 223
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LAPD는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: LAPD를 이해하면 오류율과 재전송 비용 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: LAPD (Link Access Procedure on the D channel)는 ISDN 환경에서 사용자와 네트워크 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 간의 호([Call](/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/)) 제어 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 및 소량의 패킷 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 전송하기 위한 계층 2 ([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크) 규격이다. 주로 ISDN의 D(Delta) 채널 위에서 동작한다.
- **필요성**: 기존 통신망은 전화선 하나당 전화기 한 대만 연결되는 점대점 구조였다. 그러나 ISDN은 하나의 물리 회선(BRI 기준 2B+D)에 최대 8대의 단말기를 병렬로 연결(다중점 접속)할 수 있어야 했다. 따라서 어느 단말기가 보내는 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)인지, 그것이 음성 호 제어인지 패킷 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)인지를 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층에서 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하고 분기([Multiplexing](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/))할 방법이 절실했다.
- **비유**: LAPD는 큰 사무실의 '내선 전화 교환원'과 같다. 외부에서 들어오는 굵은 케이블(물리 링크) 하나를 받아서, "이건 1번 자리 팩스로(TEI 1, SAPI 16)", "저건 2번 자리 전화기로(TEI 2, SAPI 0)" 분류하여 정확히 꽂아주는 역할을 한다.
- **발전 과정**: LAPB가 점대점([P2P](/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/)) 통신에 특화되었다면, LAPD는 점대다중점(Point-to-Multipoint) 환경을 위해 HDLC의 주소 필드를 확장(1바이트 -> 2바이트)하여 [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)([Multiplexing](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)) 기능을 추가한 형태로 발전했다.

```text
  +---------------------------------------------------------+
  |                 ISDN 인터페이스와 LAPD의 위치             |
  +---------------------------------------------------------+
  |                                                         |
  |   [TE1 (단말기1)] -+                                      |
  |   [TE2 (단말기2)] -+-- S/T 인터페이스 (멀티드롭) -- [NT1/네트워크] |
  |   [TE3 (단말기3)] -+                                      |
  |                                                         |
  |  * B 채널 (64kbps): 실제 음성/데이터 전송 (투명하게 통과) |
  |  * D 채널 (16kbps): 호 제어 신호 전송 (LAPD 프로토콜 사용)|
  +---------------------------------------------------------+
```

- **📢 섹션 요약 비유**: LAPD는 하나의 도로(D 채널) 위에 여러 대의 마을버스(단말기)가 동시에 달릴 수 있도록, 각 버스마다 고유한 노선 번호(TEI/SAPI)를 부여하는 정교한 교통 통제 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소: 확장된 주소 필드 (SAPI + TEI)

LAPD 프레임 구조의 가장 큰 특징은 [HDLC](/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/)/LAPB에서 1바이트였던 Address 필드를 2바이트로 확장하여 [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)를 지원한다는 점이다.

| 필드명 | 크기 ([Bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/)) | 역할 및 내부 동작 |
|:---|:---|:---|
| **SAPI** ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [Access Point](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) [Identifier](/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/)) | 6 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 유형 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/). (0: 호 제어 [신호](/studynote/02_operating_system/02_process_thread/130_signal/), 16: 패킷 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) X.25, 63: 관리) |
| **C/R** ([Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/)/Response) | 1 | 명령/응답 구분 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) |
| <strong><a href="/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/">EA</a></strong> (Extended Address) | 1 | 주소 필드 확장 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) (첫 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 0, 두 번째 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 1) |
| **TEI** (Terminal Endpoint [Identifier](/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/)) | 7 | 물리 회선에 연결된 단말기 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 번호 (0~127) |

### [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) ([Multiplexing](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)) 동작 메커니즘

하나의 ISDN 회선에 여러 대의 전화기([TE](/studynote/03_network/07_network_layer_routing/361_ospf_traffic_engineering_te/))가 물려있을 때, 외부에서 호([Call](/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/))가 들어오면 네트워크(NT)는 어떻게 특정 전화기를 울리게 할까?

```text
  +---------------------------------------------------------------+
  |               LAPD의 SAPI/TEI 기반 데이터 분기 구조             |
  +---------------------------------------------------------------+
  |                                                               |
  |                 물리적 D 채널 (16kbps 또는 64kbps)            |
  |                           |                                   |
  |       +-------------------+-------------------+               |
  |       v [SAPI: 0] (호 제어)                   v [SAPI: 16]    |
  |    호 제어 처리기                         X.25 패킷 처리기    |
  |       |                                       |               |
  |   +---+---+                               +---+---+           |
  |   v   v   v                               v       v           |
  | TEI:1 TEI:2 TEI:127                     TEI:1   TEI:3         |
  |(전화1)(전화2)(브로드캐스트)                (단말1) (단말3)        |
  +---------------------------------------------------------------+
```

**[다이어그램 해설]** LAPD 수신단은 먼저 프레임의 SAPI 값을 읽어 이 프레임이 음성 전화를 연결하기 위한 '[신호](/studynote/02_operating_system/02_process_thread/130_signal/)'인지, 아니면 인터넷을 하기 위한 '패킷 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)'인지 논리적으로 분류한다. 그 다음 TEI 값을 읽어 정확히 어떤 물리적 단말기를 향한 것인지 찾아간다. TEI 값이 127인 경우는 연결된 모든 단말기에게 전송하는 브로드캐스트(Broadcast) 용도로, 주로 외부에서 전화가 걸려왔을 때 모든 전화기를 동시에 울리게(Ring) 할 때 사용된다.

### 동적 TEI 할당 (Automatic TEI Assignment)

단말기를 회선에 새로 꽂을 때마다 사용자가 수동으로 번호를 지정하는 것은 불편하다. LAPD는 단말이 연결될 때 네트워크에 '내 번호(TEI)를 할당해 줘'라고 요청하는 절차를 내장하고 있다. 이는 오늘날 [DHCP](/studynote/03_network/10_application_layer_dns_mgmt/522_dhcp_dynamic_host_configuration_protocol/)(Dynamic Host Configuration [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))가 IP 주소를 동적으로 할당하는 것과 매우 유사한 철학이다.

- **📢 섹션 요약 비유**: 건물(물리 회선) 안으로 우편물이 들어오면, 먼저 부서(SAPI, 예: 영업부/인사부)를 나누고, 그 다음 개인의 사원번호(TEI)를 보고 책상까지 배달해 주는 완벽한 사내 우편 시스템입니다.

---

## Ⅲ. 비교 및 연결

| 특성 | [LAPB](/studynote/03_network/04_data_link_layer_error/222_lapb_link_access_procedure_balanced/) (X.25) | LAPD (ISDN D채널) | LAPF ([Frame Relay](/studynote/03_network/05_lan_wan_l2_devices/268_frame_relay_x25_simplification/)) |
|:---|:---|:---|:---|
| **설계 목적** | [P2P](/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 전송 | 다중점 [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) 및 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 제어 | 고속 가상 회선 [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) |
| **주소 필드** | 1 [Byte](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) (단순 C/R용) | 2 [Byte](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) (SAPI + TEI) | 2 [Byte](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 이상 ([DLCI](/studynote/03_network/05_lan_wan_l2_devices/270_dlci_data_link_connection_identifier/), 가상 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)) |
| <strong>오류 <a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a></strong> | 링크 계층에서 엄격히 수행 | 링크 계층에서 수행 (ACK 방식) | 오류 검출만 하고 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)는 상위로 넘김 |
| <strong><a href="/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/">다중화</a> 지원</strong> | 지원 안 함 (단일 링크) | 지원 ([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 및 터미널 분리) | 지원 (다수의 가상 회선 [DLCI](/studynote/03_network/05_lan_wan_l2_devices/270_dlci_data_link_connection_identifier/)) |

LAPD의 2바이트 주소 구조(SAPI+TEI)는 이후 [프레임 릴레이](/studynote/03_network/05_lan_wan_l2_devices/268_frame_relay_x25_simplification/)([Frame Relay](/studynote/03_network/05_lan_wan_l2_devices/268_frame_relay_x25_simplification/))의 LAPF [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)에서 [DLCI](/studynote/03_network/05_lan_wan_l2_devices/270_dlci_data_link_connection_identifier/) ([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Link Connection [Identifier](/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/))라는 10비트 가상 회선 번호 체계로 직접적으로 진화하게 된다.

- **📢 섹션 요약 비유**: LAPB가 단칸방의 외동딸이라면, LAPD는 여러 자녀(TEI)와 다양한 취미(SAPI)를 관리하는 다세대 주택이고, LAPF는 이를 기업형 아파트 단지(가상 회선)로 확장한 것입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

과거 ISDN(종합정보통신망)이 보급되던 시기, 하나의 전화선에 전화기, 팩스, PC용 모뎀을 동시에 꽂아 사용하는 환경이 일반적이었다. 전화가 걸려올 때 [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 인터넷이 끊어지지 않으면서 팩스와 전화기를 구별해서 울리게 하는 모든 마법이 D 채널 위를 달리는 LAPD의 TEI/SAPI [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) 덕분이었다.

- **현재의 위상**: ISDN 네트워크 자체가 광랜(FTTH)과 VoIP(Voice over IP) 기술로 대체되면서 LAPD [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)은 통신망 전면에서 사라졌다. 오늘날 음성과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)는 링크 계층(LAPD)이 아닌, 네트워크 계층(IP 패킷)과 애플리케이션 계층([SIP](/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))에서 처리된다.
- **레거시 연동**: 그러나 여전히 구형 PBX(사설 교환기)나 특정 산업군의 레거시 음성 중계망 장비를 연동할 때 PRI(Primary Rate Interface) 회선이 남아 있는 경우가 있으며, 이때 라우터는 LAPD [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 해석하여 [SIP](/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/)(IP 전화 [신호](/studynote/02_operating_system/02_process_thread/130_signal/))로 변환하는 게이트웨이 역할을 수행해야 한다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 스마트폰 하나로 통화와 인터넷을 모두 하는 지금은 구형 3단 분리형 오디오(ISDN)를 쓰지 않지만, 오디오의 각 스피커로 소리를 분배하던 그 내부 회로(LAPD) 설계 기술은 현대 홈시어터의 기초가 되었습니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | 내용 | 개선 효과 |
|:---|:---|:---|
| **정량** | 16kbps [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 내 다중 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 처리 | 물리적 선로 증설 없이 최대 8대 단말 수용 |
| **정성** | 대역 외 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)방식 (Out-of-Band) 도입 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(B채널)와 제어(D채널) 분리로 통화 중 끊김 방지 |

LAPD는 통신 역사상 처음으로 '음성 호 제어 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)'와 '사용자 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)'를 물리적으로 같은 선로 위에서 논리적으로 완벽히 분리(Out-of-Band Signaling)하여 [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)한 혁신적인 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이다. 이 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 자체는 역사 속으로 저물었으나, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층에서 논리적 주소(TEI)를 부여하고 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하는 철학은 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 기반의 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 스위칭과 [Frame Relay](/studynote/03_network/05_lan_wan_l2_devices/268_frame_relay_x25_simplification/), [ATM](/studynote/03_network/05_lan_wan_l2_devices/272_atm_asynchronous_transfer_mode_53byte_cell/) 등 후대 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통신망 구조 진화에 결정적인 영감을 제공했다. 향후에는 고신뢰 저지연 링크 제어 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: LAPD는 복잡한 교차로에 처음으로 '[신호](/studynote/02_operating_system/02_process_thread/130_signal/)등(제어)'과 '주행 차선([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))'을 분리하는 개념을 도입하여, 훗날 거대한 인터넷 고속도로 설계의 훌륭한 청사진을 남겼습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [LAPB](/studynote/03_network/04_data_link_layer_error/222_lapb_link_access_procedure_balanced/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [프레이밍](/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/) ([Framing](/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/)) | [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)열을 의미 있는 전송 단위로 구분한다. |
| [오류 제어](/studynote/03_network/04_data_link_layer_error/188_error_control_overview/) ([Error Control](/studynote/03_network/04_data_link_layer_error/188_error_control_overview/)) | 검출과 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 정책을 함께 설계해야 한다. |
| [PPP](/studynote/03_network/04_data_link_layer_error/224_ppp_point_to_point_protocol/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: LAPB]
    |
    v
[현재 개념: LAPD]
    |
    +---> [확장 A: PPP]
    +---> [확장 B: 고신뢰 저지연 링크 제어]
```

LAPD는 LAPB에서 출발해 현재 메커니즘을 정교화하고, 이후 PPP와 고신뢰 저지연 링크 제어 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 편지를 보낼 때 봉투를 제대로 닫고 틀린 글자가 없는지 확인해야 해요.
2. 이 개념은 편지가 깨지거나 사라졌을 때 다시 보내는 규칙까지 정해줘요.
3. 그래서 중간에 흔들려도 중요한 내용이 더 안전하게 도착해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 344 / 1120

<- **이전**: [222. LAPB (Link Access Procedure Balanced)](/studynote/03_network/04_data_link_layer_error/222_lapb_link_access_procedure_balanced/)
**다음**: [224. PPP (Point-to-Point Protocol)](/studynote/03_network/04_data_link_layer_error/224_ppp_point_to_point_protocol/) ->

---
