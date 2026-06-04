---
title: "571. 무선 LAN (WLAN) 구조 분산: BSS(Basic Service Set), ESS(Extended Service Set)"
date: "2026-05-08"
tags:
  - "studynote-network"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 무선 LAN 구조 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/): [BSS](/studynote/02_operating_system/02_process_thread/083_bss_segment/), ESS는 무선·이동통신에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: 무선 LAN 구조 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/): [BSS](/studynote/02_operating_system/02_process_thread/083_bss_segment/), ESS를 이해하면 스펙트럼 효율과 이동성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: WLAN 아키텍처는 유선 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)(IEEE 802.3)의 [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)/[스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 역할을 '허공의 전파'로 대체하기 위해 IEEE 802.[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/) 워킹그룹에서 정의한 논리적 구조다. 기본 셀 단위인 BSS와, 이들을 묶어주는 DS(분배 시스템), 그리고 그 총합인 ESS로 구성된다.
- **필요성**: 커피숍 하나를 덮는 와이파이는 [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 한 대([BSS](/studynote/02_operating_system/02_process_thread/083_bss_segment/))면 충분하다. 하지만 10층짜리 대형 사옥에 와이파이를 깔려면 AP가 100대는 필요하다. 만약 각 AP가 독자적인 네트워크라면 직원이 노트북을 들고 1층에서 2층으로 갈 때마다 IP가 바뀌고 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 연결이 끊어지는 대참사가 발생한다. 따라서 이 100대의 AP를 뒤에서 몰래 하나의 거대한 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)처럼 엮어주는 상위 레벨의 논리적 묶음([ESS](/studynote/06_ict_convergence/02_iot_mobility/164_ess_energy_storage_system/))이 필수적이었다.
- **등장 배경**: ① 케이블의 물리적 한계를 벗어나려는 근거리 무선망 요구 -> ② [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 없이 기기끼리 묶는 임시망(Ad-hoc)의 제어 불능 및 충돌 한계 -> ③ 유선망([Ethernet](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/))과 무선망을 브릿징(Bridging)하는 [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 중심의 인프라스트럭처 기반 WLAN 표준화 완료.

```text
+-------------------------------------------------------------+
|             WLAN의 점진적 확장 아키텍처 (BSS --> ESS) 시각화          |
+-------------------------------------------------------------+
|                                                             |
|   [1단계: BSS (Basic Service Set) - "하나의 방"]                 |
|      +------------ BSS 1 ------------+                      |
|      |        (무선: 802.11)         |                      |
|      |  📱(폰) <----> 📡(AP 1) <----> 💻(노트북) |                      |
|      +-------------------------------+                      |
|      * 특징: AP 한 대가 관할하는 가장 기본적인 단위.                       |
|                                                             |
|   [2단계: ESS (Extended Service Set) - "하나의 거대한 빌딩"]          |
|                    [인터넷 / 유선망]                             |
|                           ^                                 |
|          +----------------+------------------+              |
|          |  DS (Distribution System, 유선 랜) |              |
|          +--------+-----------------+--------+              |
|                   |                 |                       |
|           +----- BSS 1 ----++----- BSS 2 ----+              |
|           |       📡(AP 1)  ||       📡(AP 2)  |              |
|           | 📱 --(이동)----->|| ---(도착)---> 📱 |              |
|           +----------------++----------------+              |
|      * 특징: 사용자는 AP1에서 AP2로 넘어가도 IP를 잃지 않고 통신 유지(로밍)!  |
+-------------------------------------------------------------+
```

**[다이어그램 해설]** BSS는 하나의 "셀(Cell)"과 같다. [BSS](/studynote/02_operating_system/02_process_thread/083_bss_segment/) 안의 기기들은 반드시 [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)([Access Point](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/))를 통해서만 서로 대화할 수 있다. 만약 폰이 바로 옆에 있는 노트북에 사진을 보내려 해도, 전파를 AP로 쏜 뒤 AP가 다시 노트북으로 쏴주는 '별 모양(Star Topology)' 통신을 한다. ESS는 이 AP들의 등 뒤에 꽂힌 굵은 랜선(DS, 분배 시스템)을 묶어낸 집합체다. 밖에서 볼 때 10층짜리 빌딩([ESS](/studynote/06_ict_convergence/02_iot_mobility/164_ess_energy_storage_system/)) 안에는 수백 개의 AP가 있지만, 사용자에게는 `Samsung_Guest`라는 단 하나의 와이파이(SSID)로만 보인다. 사용자가 걸어 다니면 단말기는 뒤에서 조용히 AP1과 연결을 끊고 AP2로 갈아타는 짓([Roaming](/studynote/03_network/11_wireless_mobile_communication/560_roaming/))을 하지만, 위에서 DS가 IP를 잡아주고 있기 때문에 사용자는 끊김을 느끼지 못한다.

- **📢 섹션 요약 비유**: BSS는 교실 한 칸입니다. 칠판 앞에 선 선생님([AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/))을 통해서만 학생들이 대화할 수 있죠. ESS는 수십 개의 교실이 복도(DS)로 묶인 거대한 학교입니다. 학생이 1반(BSS1)에서 2반(BSS2)으로 옮겨 가도, 여전히 똑같은 학교([ESS](/studynote/06_ict_convergence/02_iot_mobility/164_ess_energy_storage_system/)) 안이라서 교장 선생님(인터넷)은 그 학생을 똑같이 관리할 수 있는 완벽한 조직 체계입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### BSS의 두 가지 모드 (IBSS vs Infrastructure [BSS](/studynote/02_operating_system/02_process_thread/083_bss_segment/))

IEEE 802.[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/) 표준은 무선 기기들이 모이는 방식을 두 가지로 나누어 정의했다.

| 구분 | <strong>Infrastructure <a href="/studynote/02_operating_system/02_process_thread/083_bss_segment/">BSS</a> (인프라스트럭처 모드)</strong> | <strong>IBSS (Independent <a href="/studynote/02_operating_system/02_process_thread/083_bss_segment/">BSS</a> / Ad-hoc 모드)</strong> |
|:---|:---|:---|
| **중앙 통제자** | <strong><a href="/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/">AP</a> (<a href="/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/">Access Point</a>) 존재</strong> | <strong><a href="/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/">AP</a> 없음</strong> (단말기들끼리 평등하게 알아서 통신) |
| **통신 방식** | 단말기 ↔ [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) ↔ 다른 단말기 (Star 구조) | 단말기 ↔ 단말기 다이렉트 통신 ([Mesh](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)/[Peer](/studynote/06_ict_convergence/01_blockchain/060_hyperledger_architecture_peer_orderer_msp/) 구조) |
| <strong>BSSID (<a href="/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/">식별자</a>)</strong>| AP의 무선 랜카드 <strong><a href="/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a> 주소</strong> | 단말기 중 하나가 임의로 생성한 <strong>가짜(랜덤) <a href="/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a> 주소</strong> |
| **유선망(인터넷) 연결**| AP를 통해 외부 인터넷(DS)과 100% 연결 가능 | 유선망 연결 불가. 고립된 자기들만의 외딴섬 통신 |
| **실무 사용처** | 우리가 쓰는 99.9%의 집, 카페, 기업용 와이파이 | 산속, 재난 지역 등 AP가 다 박살 났을 때 기기끼리 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 공유 시 |

현대의 모든 엔터프라이즈 와이파이는 무조건 'Infrastructure [BSS](/studynote/02_operating_system/02_process_thread/083_bss_segment/)'다. AP가 없으면 충돌([Collision](/studynote/05_database/04_transactions_concurrency/563_hash_collision_chaining_linear_probing/)) 제어가 불가능해 속도가 바닥을 기기 때문이다.

와이파이 망을 구축할 때 가장 많이 헷갈리는 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) 3형제의 아키텍처를 정확히 구분해야 한다.

```text
+---------------------------------------------------------------+
|               WLAN 식별자 (Identifier)의 계층적 구조 시각화          |
+---------------------------------------------------------------+
|                                                               |
|   [ESS (거대한 사옥 네트워크)]                                    |
|   - 이름: ESSID = "SAMSUNG_CORP" (사람이 읽기 쉬운 문자열, 최대 32바이트) |
|                                                               |
|          +----------------------- DS (유선 백본) ----------------------+|
|          |                                                           ||
|    [BSS 1 (1층 로비)]                [BSS 2 (2층 사무실)]            ||
|    - AP1 기계 MAC: aa:bb:cc:11       - AP2 기계 MAC: aa:bb:cc:22 ||
|    - BSSID = "aa:bb:cc:11"           - BSSID = "aa:bb:cc:22"     ||
|    - 발산하는 SSID = "SAMSUNG_CORP"    - 발산하는 SSID = "SAMSUNG_CORP"||
|                                                               |
|   => 폰의 판단: "어? SSID(SAMSUNG_CORP)가 똑같은 이름으로 2개나 잡히네?"     |
|                 "근데 BSSID(MAC)를 까보니까 AP가 서로 다르구나!"            |
|                 "나는 지금 신호가 더 센 BSSID aa:bb:cc:11 에 붙어야지!"   |
+---------------------------------------------------------------+
```

**[다이어그램 해설]** <strong>SSID(<a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a> Set <a href="/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/">Identifier</a>)</strong>는 인간을 위한 이름표다. 우리가 카페에서 찾는 '스타벅스_와이파이'가 바로 SSID다. 엄밀히 말해 [ESS](/studynote/06_ict_convergence/02_iot_mobility/164_ess_energy_storage_system/) 모델에서는 여러 개의 AP가 똑같은 SSID를 뿜어대므로 이를 <strong>ESSID</strong>라고도 부른다. 반면 <strong>BSSID(Basic <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a> Set <a href="/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/">Identifier</a>)</strong>는 기계를 위한 이름표다. 각 AP의 고유한 무선 랜카드 '[MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소(48비트)'다. 내 스마트폰이 1층에서 2층으로 걸어갈 때 화면 위쪽의 와이파이 아이콘(SSID)은 안 바뀌지만, 스마트폰 내부 무선 칩셋은 1층 [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)(BSSID 1)를 버리고 2층 [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)(BSSID 2)로 잽싸게 갈아타는 이사 작업을 수행하고 있다. 이 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)의 분리가 WLAN [로밍](/studynote/03_network/11_wireless_mobile_communication/560_roaming/) 아키텍처의 핵심이다.

- **📢 섹션 요약 비유**: SSID(ESSID)는 '스타벅스'라는 체인점 간판입니다. 전국 어딜 가도 이름이 같습니다. BSSID는 '스타벅스 강남점 점장', '스타벅스 역삼점 점장'의 주민등록번호입니다. 우리는 모두 '스타벅스(SSID)'에 들어간다고 생각하지만, 실제로는 각 지점의 점장님(BSSID)과 1:1로 주문을 주고받는 것입니다.

---

## Ⅲ. 비교 및 연결

WLAN(와이파이)의 [BSS](/studynote/02_operating_system/02_process_thread/083_bss_segment/) 구조는 셀룰러 망의 Cell 구조와 완벽한 대척점에 있다. 두 거대 통신 진영이 세상을 바라보는 철학의 차이다.

| 비교 기준 | WLAN (Wi-Fi, 802.[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/) 진영) | Cellular ([LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/)/[5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/), [3GPP](/studynote/03_network/15_nextgen_communication_architecture/751_3gpp_3rd_generation_partnership_project/) 진영) |
|:---|:---|:---|
| **망 제어 철학** | <strong>경쟁 기반 <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>형 (<a href="/studynote/03_network/02_multiplexing_multiple_access/104_csma/">CSMA</a>/<a href="/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/">CA</a>)</strong> | <strong>스케줄링 기반 중앙통제형 (<a href="/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/">OFDMA</a>/CAC)</strong> |
| **기본 단위** | [BSS](/studynote/02_operating_system/02_process_thread/083_bss_segment/) (Basic [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Set) / [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 1대 | Cell (셀) / 기지국 1대 |
| **간섭(Interference) 대처** | "누가 말하고 있으면 나는 눈치 보고 쉰다." | "기지국이 0.01초 단위로 말할 타이밍을 강제 배분한다." |
| <strong><a href="/studynote/03_network/11_wireless_mobile_communication/560_roaming/">로밍</a>/<a href="/studynote/03_network/11_wireless_mobile_communication/556_handover_handoff_types_concept/">핸드오버</a> 주체</strong> | **단말기 주도 (Mobile-Initiated)**. 폰 스스로 BSSID를 스캔하고 옮겨버림. AP는 끌려감. | **네트워크 주도 (Network-Controlled)**. 폰이 보고하면 기지국이 허락해야만 이동함. |
| **주파수 대역** | 무료 공용 대역 (Unlicensed Band, 2.4/5GHz) | 국가가 수조 원에 파는 전용 대역 (Licensed Band) |

WLAN의 BSS는 통제받지 않는 시장통이다. 무전기처럼 "나 말한다!" 하고 쏘기([CSMA](/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/[CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/)) 때문에, 하나의 [BSS](/studynote/02_operating_system/02_process_thread/083_bss_segment/)([AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)) 밑에 100대의 폰이 모이면 서로 눈치를 보느라 아무도 데이터를 못 쏘는 최악의 속도 저하(Collisions)가 터진다. 반면 셀룰러(기지국)는 경찰관이 교통 통제를 하듯 100명의 폰에게 "너 1번, 너 2번" 시간과 주파수(PRB)를 완벽히 통제해서 쏴주기 때문에 수만 명이 모여도 망이 터지지 않는다. 이 근본적인 아키텍처 차이 때문에 넓은 핫스팟에는 무조건 셀룰러가, 좁고 쾌적한 실내에는 와이파이가 쓰이는 것이다.

```text
+---------------------------------------------------------------+
|               WLAN의 숨은 포탈(Portal) 아키텍처 시각화                |
+---------------------------------------------------------------+
|                                                               |
|   [무선 BSS]                   [유선 DS]                 [외부 망]   |
|   (802.11 전파)            (802.3 이더넷 랜선)           (TCP/IP 인터넷)|
|                                                               |
|      📱 --(무선)---> 📡 AP --(랜선)---> 스위치(DS) --(랜선)---> 🚪 [포탈] |
|                                                               |
|                                                          (라우터)   |
|   * 🚪 포탈(Portal)의 역할:                                       |
|   "야! 여기부턴 무선 LAN (802.11) 세상이 아니라 진짜 밖(802.3 이더넷)이야!" |
|   무선 프레임(802.11)의 껍데기를 다 벗겨버리고, 유선 프레임(802.3)으로     |
|   완전히 포장지를 갈아 끼워서 진짜 인터넷 밖으로 내보내는 '현관문' 역할.       |
+---------------------------------------------------------------+
```

**[다이어그램 해설]** IEEE 802.[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/) 표준 문서를 읽다 보면 <strong>Portal (포탈)</strong>이라는 신비한 용어가 나온다. BSS와 DS를 묶어 만든 [ESS](/studynote/06_ict_convergence/02_iot_mobility/164_ess_energy_storage_system/) 네트워크는 결국 집 안의 '로컬 망'일 뿐이다. 이 로컬 망에서 유튜브 서버(외부)로 나가려면 논리적인 현관문을 통과해야 하는데, 이 관문이 포탈이다. 실무에서는 보통 <strong>인터넷 공유기(라우터)</strong>가 포탈 역할을 겸한다. 스마트폰이 허공으로 쏜 데이터는 802.11이라는 특별한 껍데기([MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 헤더)를 입고 있다. 포탈은 이 껍데기를 찢어버리고, 전 세계 유선 통신 규격인 802.3([이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)) 껍데기로 갈아 끼워주는 완벽한 번역기(Translation [Bridge](/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)) 역할을 수행한다.

- **📢 섹션 요약 비유**: BSS가 집 안방이고 DS가 거실이라면, 포탈(Portal)은 우리 집 현관문입니다. 안방에서 입던 잠옷(802.[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/))을 입고 밖으로 나갈 순 없으니, 현관문에서 바깥 외출복(802.3 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/))으로 갈아입고 세상(인터넷)으로 나가게 해주는 아주 중요한 경계선입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

1. **상황**: 대기업 20층 사옥에 와이파이를 깔기 위해 [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 500대를 샀다. 기존 가정용 공유기([Fat](/studynote/02_operating_system/09_file_system/525_fat_file_allocation_table/) [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/))처럼 500대에 일일이 관리자가 접속해 `SSID=회사_망`, `PW=1234`를 타이핑하고 있다면 보안도 뚫리고 세팅에 한 달이 걸릴 것이다.
2. **원인**: 가정용 AP는 혼자서 BSS도 만들고, 암호화도 하고, 라우팅도 하는 '똑똑하고 무거운([Fat](/studynote/02_operating_system/09_file_system/525_fat_file_allocation_table/))' 장비다. 하지만 이런 놈이 500개가 모이면 서로 전파를 뿜어대어 자기들끼리 간섭([Co-Channel Interference](/studynote/03_network/11_wireless_mobile_communication/555_co_channel_adjacent_interference/))을 일으키고 통제가 불가능한 아수라장이 된다.
3. <strong>의사결정 및 조치 (Thin <a href="/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/">AP</a> + WLC 아키텍처 도입)</strong>:
   - 아키텍트는 500대의 AP를 <strong>바보 <a href="/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/">안테나</a>(Thin <a href="/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/">AP</a>, 또는 CAPWAP <a href="/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/">AP</a>)</strong>로 다운그레이드한다. 이들은 오직 전파만 쏘고 받는 껍데기 역할만 한다.
   - 중앙 전산실에 <strong>WLC (Wireless LAN Controller)</strong>라는 강력한 두뇌 장비를 한 대 설치하고 유선(DS)으로 500대의 AP를 묶는다.
   - WLC가 500대의 AP에게 "너는 1번 채널, 너는 6번 채널, 너는 11번 채널 써!"라고 간섭을 피해 실시간으로 조종(RRM)한다.
   - 스마트폰이 1층 AP에서 2층 AP로 이동할 때, AP들은 아무것도 모른다. 중앙의 WLC가 "오, 저 폰 올라왔네. 연결 안 끊기게 해!"라며 1밀리초 만에 암호키를 넘겨주는 완벽한 <strong>Fast <a href="/studynote/03_network/11_wireless_mobile_communication/560_roaming/">Roaming</a></strong>을 구현했다.
   - **결과**: 관리자는 WLC 세팅 한 번만으로 사옥 전체 500대 AP의 비밀번호와 채널을 통제하는 완벽한 거대 ESS를 완성했다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 및 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong>채널 중첩 (Channel Overlapping) 1, 6, <a href="/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/">11</a> 원칙 <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong>: 여러 개의 BSS를 이어 ESS를 만들 때, 인접한 AP끼리 같은 채널을 쓰면 무조건 전파가 찢어진다. 2.4GHz 대역은 채널이 13개지만 뚱뚱해서 서로 간섭하지 않고 독립적으로 쓸 수 있는 채널은 <strong>오직 1, 6, 11번 (Non-overlapping channels) 3개뿐</strong>이다. BSS들을 벌집 모양으로 배치할 때, 맞닿은 AP끼리 1, 6, [11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/) 채널을 퐁당퐁당 섞어 배치하는 셀 플래닝(Cell Planning)을 어기는 것이 실무 최대의 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)이다.
- <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a> (BSSID가 겹치는 오작동 방치)</strong>: 가끔 악의적인 해커가 사옥 구석에 라즈베리 파이를 숨겨두고 사내 망과 똑같은 `SSID`는 물론, 심지어 사내 AP와 완전히 동일한 기계 주소(`BSSID/MAC`)를 뿜어내는 사기꾼 공유기(Rogue [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) / Evil Twin)를 설치한다. 사용자의 폰은 이름과 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소가 똑같으니 속아서 해커의 AP에 붙어버리고 모든 비밀번호를 탈취당한다. WLC에는 반드시 이런 사기꾼 BSS를 감지하고, 주변 정상 AP들이 일제히 해커 AP를 향해 전파 교란(Deauthentication) 폭격을 때려 접속을 끊어버리는 **WIPS (무선 침입 방지 시스템)** 기능을 켜두어야 한다.

- **📢 섹션 요약 비유**: 사옥에 와이파이 500개를 까는 건 500명의 점장([Fat](/studynote/02_operating_system/09_file_system/525_fat_file_allocation_table/) [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/))을 뽑는 게 아닙니다. 점장 없이 서빙만 하는 알바생(Thin [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)) 500명을 뽑아 층마다 배치하고, 중앙 통제실에 있는 단 1명의 천재 매니저(WLC)가 인이어 무전기로 알바생 500명을 동시에 조종하며 거대한 식당([ESS](/studynote/06_ict_convergence/02_iot_mobility/164_ess_energy_storage_system/))을 굴리는 것이 최신 기업용 와이파이 건축학입니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | 단독 [BSS](/studynote/02_operating_system/02_process_thread/083_bss_segment/) (가정용 공유기) 파편화 망 | [ESS](/studynote/06_ict_convergence/02_iot_mobility/164_ess_energy_storage_system/) 및 WLC (무선랜 컨트롤러) 기반 망 | 개선 효과 |
|:---|:---|:---|:---|
| <strong>정량 (이동 <a href="/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">지연 시간</a>)</strong> | 다른 층 [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 이동 시 [DHCP](/studynote/03_network/10_application_layer_dns_mgmt/522_dhcp_dynamic_host_configuration_protocol/) IP 갱신, 1~2초 단절 | WLC가 세션을 유지한 채 뒤에서 스위칭 (수 ms) | 이동 중 화상 회의나 인터넷 튕김(Roam Drop) **0% 수렴** |
| **정량 (전파 간섭 최적화)**| AP끼리 주파수 눈치싸움 실패 시 속도 70% 폭락 | WLC가 중앙에서 1, 6, [11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/) 채널 실시간 스케줄링 | 사내 무선 간섭(CCI) [억제](/studynote/09_security/13_secops_ir_forensics/656_ir_containment/) 및 <strong>전체 <a href="/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a>(<a href="/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">Throughput</a>) 극대화</strong> |
| **정성 (보안 통제력)** | 500대 [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 각각 해킹 위험 (비밀번호 노출) | 802.[1X](/studynote/03_network/11_wireless_mobile_communication/584_802_1x_pnac_eap_radius/)/[RADIUS](/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/) 기반 중앙 WLC 통합 [보안 정책](/studynote/09_security/01_intro_principles/007_security_policy/) | 임직원 퇴사 시 중앙 서버(AD) 클릭 한 번으로 모든 사내 와이파이 접근 영구 차단 |

### 미래 전망 및 진화 방향
- <strong>SD-Access와 클라우드 제어 <a href="/studynote/06_ict_convergence/02_iot_mobility/164_ess_energy_storage_system/">ESS</a> (Cloud-Managed WLAN)</strong>: 과거엔 수천만 원짜리 무거운 무선랜 컨트롤러(WLC) 장비를 사옥 지하실에 둬야 했다. 이제는 [Cisco](/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/) Meraki 등 **클라우드 WLC** 아키텍처가 대세다. 그냥 인터넷만 연결된 멍텅구리 AP를 콘센트에 꽂으면, 아마존 클라우드에 떠 있는 WLC가 전 세계 지사(뉴욕, 서울)의 AP들을 통제하여 지구 전체를 하나의 논리적 ESS로 묶어버리는 마법이 상용화되었다.
- <strong><a href="/studynote/02_operating_system/02_process_thread/083_bss_segment/">BSS</a> Color (<a href="/studynote/03_network/11_wireless_mobile_communication/576_802_11ax_wifi_6_ofdma_twt/">Wi-Fi 6</a> 802.<a href="/studynote/03_network/11_wireless_mobile_communication/576_802_11ax_wifi_6_ofdma_twt/">11ax</a> 혁신)</strong>: 아무리 WLC가 채널을 1, 6, 11로 쪼개도 아파트나 도심에는 남의 집 [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 전파가 우리 집으로 넘어온다. Wi-Fi 6부터는 BSS에 '색깔표([BSS](/studynote/02_operating_system/02_process_thread/083_bss_segment/) Color)'를 칠한다. 내 폰이 통신하기 전 "어? 이건 우리 집 파란색([BSS](/studynote/02_operating_system/02_process_thread/083_bss_segment/) 1) 전파가 아니라 옆집 빨간색([BSS](/studynote/02_operating_system/02_process_thread/083_bss_segment/) 2) 찌꺼기네? 그럼 눈치 안 보고 나도 쏴야지!"라며 [CSMA](/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/CA의 쓸데없는 대기 시간을 무시해버려 밀집 지역의 속도를 4배 튀기는 [BSS](/studynote/02_operating_system/02_process_thread/083_bss_segment/) 구조 혁명이 완성되었다.

### 참고 표준
- <strong>IEEE 802.<a href="/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/">11</a></strong>: 무선 LAN을 관장하는 가장 방대한 글로벌 규격. 1997년 처음 제정되며 [BSS](/studynote/02_operating_system/02_process_thread/083_bss_segment/), DS, [ESS](/studynote/06_ict_convergence/02_iot_mobility/164_ess_energy_storage_system/), Portal의 용어와 아키텍처 철학을 세운 바이블.
- **CAPWAP (RFC 5415)**: Control And [Provisioning](/studynote/09_security/11_iam_access_control/528_provisioning/) of Wireless Access Points. 바보 [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/)(Thin [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/))와 중앙 두뇌(WLC)가 유선으로 데이터를 주고받기 위해 뚫는 암호화 [터널링](/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/) 통신 표준.

선을 자르고 전파로 허공을 날겠다는 인류의 꿈은 단순히 [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/)를 꽂는다고 해결되지 않았다. 작은 교실([BSS](/studynote/02_operating_system/02_process_thread/083_bss_segment/))들을 수십 개 만들고, 보이지 않는 복도(DS)로 묶어 거대한 성곽([ESS](/studynote/06_ict_convergence/02_iot_mobility/164_ess_energy_storage_system/))으로 빚어낸 이 치밀한 기하학적 토폴로지가 있었기에, 우리는 노트북을 들고 20층짜리 사옥 전체를 자유롭게 누비며 끊김 없는 디지털 유목민의 자유를 얻게 된 것이다.

- **📢 섹션 요약 비유**: 수백 개의 방([BSS](/studynote/02_operating_system/02_process_thread/083_bss_segment/))을 가진 거대한 궁전([ESS](/studynote/06_ict_convergence/02_iot_mobility/164_ess_energy_storage_system/))에서, 신하들([AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/))은 오직 방을 밝히는 역할만 하고, 중앙 통제실의 집사(WLC)가 모든 방의 불빛 밝기와 온도를 통제합니다. 덕분에 왕(스마트폰)은 어느 방을 돌아다니든 똑같은 온도와 밝기 속에서 불편함 없이 우아하게 생활할 수 있는 최고급 저택 시스템입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [WiMAX](/studynote/03_network/11_wireless_mobile_communication/570_wimax_802_16_wibro_mobile_broadband/) / 휴대인터넷 개요 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 셀 (Cell) | 무선 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 범위를 나누는 기본 단위다. |
| [핸드오버](/studynote/03_network/11_wireless_mobile_communication/556_handover_handoff_types_concept/) ([Handover](/studynote/03_network/11_wireless_mobile_communication/556_handover_handoff_types_concept/)) | 이동 중에도 연결을 유지하게 만든다. |
| [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) / DS | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: WiMAX / 휴대인터넷 개요]
    |
    v
[현재 개념: 무선 LAN 구조 분산: BSS, ESS]
    |
    +---> [확장 A: AP / DS]
    +---> [확장 B: 지능형 무선 자원 제어]
```

무선 LAN 구조 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/): [BSS](/studynote/02_operating_system/02_process_thread/083_bss_segment/), ESS는 [WiMAX](/studynote/03_network/11_wireless_mobile_communication/570_wimax_802_16_wibro_mobile_broadband/) / 휴대인터넷 개요에서 출발해 현재 메커니즘을 정교화하고, 이후 [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) / DS와 지능형 무선 자원 제어 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 내 방에 있는 와이파이 공유기 하나가 만들어주는 둥근 통신 구역을 텐트 한 동(<strong><a href="/studynote/02_operating_system/02_process_thread/083_bss_segment/">BSS</a></strong>)이라고 생각하면 돼요.
2. 하지만 엄청 큰 백화점은 텐트 한 동으론 부족해서, 수백 개의 텐트를 치고 그 사이를 유선 케이블 끈(**DS**)으로 단단히 묶어놨어요. 이렇게 거대하게 묶인 와이파이 왕국을 <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/164_ess_energy_storage_system/">ESS</a></strong>라고 부른답니다.
3. 텐트가 묶여있는 덕분에, 우리가 백화점 1층에서 5층으로 에스컬레이터를 타고 올라가도 우리 폰은 텐트 사이를 몰래 몰래 옮겨 타서 유튜브가 절대 안 끊기는 거예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 692 / 1120

<- **이전**: [570. WiMAX (IEEE 802.16) / 휴대인터넷(WiBro) 개요](/studynote/03_network/11_wireless_mobile_communication/570_wimax_802_16_wibro_mobile_broadband/)
**다음**: [572. AP (Access Point) / DS (Distribution System, 분배 시스템)](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) ->

---
