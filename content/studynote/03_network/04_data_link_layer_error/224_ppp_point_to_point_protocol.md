+++
title = "224. PPP (Point-to-Point Protocol)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PPP는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: PPP를 이해하면 오류율과 재전송 비용 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: PPP ([Point-to-Point](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/142_point_to_point_integration_spaghetti/) [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))는 동기식([Synchronous](/knowledge-base/studynote/03_network/01_data_communication/010_동기식_비동기식_전송/)) 또는 비동기식(Asynchronous) 점대점 링크에서 여러 종류의 네트워크 계층 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)하여 전송할 수 있게 해주는 계층 2 표준 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이다.
- **필요성**: 1980년대 후반 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 통신 시절 사용되던 SLIP [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)은 오직 IPv4만 지원했고, 동적 IP 할당 기능도 없었으며, 무엇보다 '[사용자 인증](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/)' 기능이 없어 보안에 매우 취약했다. 서로 다른 벤더의 장비끼리 호환되면서도, 전화선을 통해 인터넷에 접속하려는 사용자를 안전하게 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)하고 IP를 자동으로 부여해 줄 강력한 범용 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이 필요했다.
- **비유**: PPP는 단순한 배달 기사가 아니라 '종합 물류 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)'다. 물건([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 배달할 뿐만 아니라, 배달 전에 신분증 검사([인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))를 하고, 내용물의 종류(IP, IPX)를 명확히 분류하며, 필요하면 압축이나 암호화 포장까지 알아서 해주는 만능 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)다.
- **발전 과정**: SLIP의 대체재로 등장한 PPP는 [HDLC](/knowledge-base/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) 프레임 구조를 차용하되 제어 기능을 모듈화([LCP](/knowledge-base/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/), [NCP](/knowledge-base/studynote/03_network/04_data_link_layer_error/226_ncp_network_control_protocol/))함으로써 인터넷 접속의 사실상 표준(De facto standard)이 되었다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PPP의 3대 핵심 컴포넌트</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">네트워크 계층</div><div class="kb-diagram-note">IP, IPX, AppleTalk 등 다양한 프로토콜</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(1) NCP (Network Control Protocol) : 망 설정</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PPP</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(2) LCP (Link Control Protocol) : 링크 설정 및 인증</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(3) HDLC 기반 프레이밍 (Framing)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">물리 계층</div><div class="kb-diagram-note">모뎀(비동기), ISDN/전용선(동기), 이더넷</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: PPP는 단순히 두 도시를 잇는 아스팔트 도로([프레이밍](/knowledge-base/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/))가 아니라, 그 도로 위에 톨게이트([LCP](/knowledge-base/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/) [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))와 차선 분배기([NCP](/knowledge-base/studynote/03_network/04_data_link_layer_error/226_ncp_network_control_protocol/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/))까지 모두 갖춘 완벽한 턴키(Turn-key) 방식의 민자 고속도로 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소

| 요소명 | 역할 | 내부 동작 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/">프레이밍</a> (<a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/">Framing</a>)</strong> | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 시작과 끝 구분 | HDLC와 유사한 `01111110` [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) 사용, [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)/[바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 스터핑 지원 |
| <strong><a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/">LCP</a> (<a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/">Link Control Protocol</a>)</strong> | 물리적 링크의 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), 유지, 종료 | 최대 프레임 크기(MTU) 협상, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)([PAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/227_pap_password_authentication_protocol/)/[CHAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/228_chap_challenge_handshake_authentication_protocol/)) 결정 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a> (<a href="/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/">Authentication</a>)</strong> | 접속하려는 사용자의 신원 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | [PAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/227_pap_password_authentication_protocol/) (명문장 전송, 취약), [CHAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/228_chap_challenge_handshake_authentication_protocol/) (Challenge-Response 3way 핸드쉐이크, 안전) |
| <strong><a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/226_ncp_network_control_protocol/">NCP</a> (<a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/226_ncp_network_control_protocol/">Network Control Protocol</a>)</strong> | 상위 네트워크 계층의 세부 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | IPCP (IP Control [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))를 통해 동적 IP 주소, [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 서버 등 할당 |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">LAPD</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">PPP</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">LCP</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: PPP의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

PPP의 가장 강력한 특징은 단순히 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 흘려보내는 것이 아니라, 명확한 단계를 거쳐 링크를 수립한다는 점이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PPP 세션 수립 단계 (Phases)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Dead</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">Establish</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">LCP 옵션 협상 (MTU 등)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">──(성공)──</div><div class="kb-diagram-node">Authenticate</div><div class="kb-diagram-note">(선택적)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PAP 또는 CHAP을 통한 신원 확인</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Network</div><div class="kb-diagram-connector">◀</div><div class="kb-diagram-note">──(성공)── IPCP를 통한 동적 IP 및 DNS 할당</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▼ (NCP 완료)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Open</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-note">실제 인터넷(IP 패킷) 데이터 송수신 시작</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▼ (연결 종료 요청 또는 물리적 끊김)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Terminate</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">Dead</div></div>
</div>
</div>



**[다이어그램 해설]** 사용자가 [모뎀](/knowledge-base/studynote/03_network/03_physical_layer_media/146_modem_modulator_demodulator/)으로 전화를 걸면 먼저 [LCP](/knowledge-base/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/) 단계(Establish)에서 기본 통신 규칙을 정한다. 이후 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 단계(Authenticate)에서 ID/Password를 검증하고, 성공하면 [NCP](/knowledge-base/studynote/03_network/04_data_link_layer_error/226_ncp_network_control_protocol/)(Network) 단계로 넘어가 [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_information_strategy_planning_4_steps/)(통신사)로부터 IP 주소를 동적으로 받아온다. 이 모든 과정이 끝나야만 비로소 '인터넷 연결됨(Open)' 상태가 되어 웹 서핑이 가능해진다. 하나라도 실패하면 연결은 즉시 종료된다.

### [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 메커니즘: [PAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/227_pap_password_authentication_protocol/) vs [CHAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/228_chap_challenge_handshake_authentication_protocol/)

PPP는 회선 도청의 위험을 막기 위해 [CHAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/228_chap_challenge_handshake_authentication_protocol/)(Challenge Handshake [Authentication](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/) [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))이라는 강력한 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 방식을 도입했다.

- <strong><a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/227_pap_password_authentication_protocol/">PAP</a> (<a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/227_pap_password_authentication_protocol/">Password Authentication Protocol</a>)</strong>: 클라이언트가 ID와 비밀번호를 평문(Plain text)으로 2-Way 핸드쉐이크로 전송. [중간자 공격](/knowledge-base/studynote/03_network/14_network_security_threats/706_mitm_man_in_the_middle_hsts/)(MITM)에 극도로 취약함.
- <strong><a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/228_chap_challenge_handshake_authentication_protocol/">CHAP</a></strong>: 서버가 난수(Challenge)를 보내면, 클라이언트가 [해시 함수](/knowledge-base/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/)([MD5](/knowledge-base/studynote/03_network/13_network_security_basics/668_md5_hash_collision_vulnerability/) 등)를 이용해 '비밀번호+난수'의 결과값(Response)을 보내는 3-Way 핸드쉐이크. 비밀번호 자체가 회선에 노출되지 않음.


| 비교 항목 | SLIP | PPP | [HDLC](/knowledge-base/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) |
|:---|:---|:---|:---|
| **설계 목적** | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 시리얼 IP 전송 | 다중 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 지원, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 동적 IP | 범용 링크 제어 (동기식 중심) |
| <strong>다중 <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a></strong> | 불가 (오직 IPv4만) | 완벽 지원 (IP, IPX, [IPv6](/knowledge-base/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/) 등) | [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)에 따라 다름 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>/보안</strong> | 없음 | [PAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/227_pap_password_authentication_protocol/), [CHAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/228_chap_challenge_handshake_authentication_protocol/), [EAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/229_eap_extensible_authentication_protocol/) 지원 | 없음 |
| <strong><a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/188_error_control_overview/">오류 제어</a></strong> | 없음 | FCS를 통한 오류 검출 ([복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)는 안 함) | 검출 및 재전송([ARQ](/knowledge-base/studynote/03_network/19_frequent_topics_terms/949_arq_automatic_repeat_request_go_back_n_selective/)) 지원 |

PPP는 HDLC의 프레임 구조를 빌려왔으나, 무거운 오류 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)([ARQ](/knowledge-base/studynote/03_network/19_frequent_topics_terms/949_arq_automatic_repeat_request_go_back_n_selective/)) 기능은 버리고 대신 '[인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)'과 '다중 네트워크 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)'라는 현대 인터넷에 꼭 필요한 기능만을 담은 걸작이다.

- **📢 섹션 요약 비유**: SLIP이 오직 110v 돼지코만 꽂을 수 있는 구형 멀티탭이라면, PPP는 220v, [USB](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/), C타입을 모두 꽂을 수 있고 과전류 차단([인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)) 기능까지 들어있는 스마트 멀티탭입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

ADSL이나 [VDSL](/knowledge-base/studynote/03_network/03_physical_layer_media/148_adsl_vdsl_gfast/) 같은 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 인터넷이 보급되던 2000년대 초반, 통신사(KT, SKT 등)는 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)([Ethernet](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/))이라는 훌륭한 LAN 기술을 가정까지 끌고 왔다. 하지만 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)은 근본적으로 브로드캐스트 망이라 '누가 접속했는지 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)하고 요금을 과금하는' 기능이 없었다. 그래서 통신사들은 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 프레임 안에 PPP를 캡슐화하여 넣는 <strong>PPPoE (PPP over <a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/">Ethernet</a>)</strong> 기술을 도입했다.

- **도입의 당위성**: [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)의 싼 가격과 빠른 속도를 유지하면서도, 기존 전화선 시절 [모뎀](/knowledge-base/studynote/03_network/03_physical_layer_media/146_modem_modulator_demodulator/) 통신사들이 쓰던 PPP의 강력한 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([RADIUS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/) 서버 연동) 및 IP 통제 관리 시스템을 그대로 재활용할 수 있는 완벽한 비즈니스적 판단이었다.
- <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>: 현대의 모바일([LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/)/[5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/))이나 순수 광랜(FTTH) 환경에서는 DHCP와 802.[1X](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/584_802_1x_pnac_eap_radius/) 같은 다른 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 기술이 발전하면서, 굳이 MTU를 깎아먹는([이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 1500바이트 → PPPoE 1492바이트) PPPoE를 쓸 이유가 사라지고 있다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 고속철도([이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/))가 깔렸지만 기차표 검사 시스템을 새로 만들기 아까워서, 예전 고속버스([모뎀](/knowledge-base/studynote/03_network/03_physical_layer_media/146_modem_modulator_demodulator/)) 시절 쓰던 매표소(PPP)를 기차역 입구에 그대로 들고 와서 쓴 것이 바로 PPPoE입니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | 내용 | 개선 효과 |
|:---|:---|:---|
| **정량** | IPCP를 통한 동적 IP 할당 | [IPv4](/knowledge-base/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) 주소 고갈 문제 완화, 통신사의 효율적 IP 풀 관리 |
| **정성** | 플러그 앤 플레이(Plug & Play) | 사용자가 복잡한 네트워크 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 없이 ID/PW만으로 즉시 인터넷 접속 |

순수한 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 케이블([Serial](/knowledge-base/studynote/03_network/01_data_communication/009_직렬_전송_vs_병렬_전송/) Cable) 위를 달리는 원시적인 형태의 PPP는 이제 찾아보기 어렵다. 그러나 PPP가 정립한 [LCP](/knowledge-base/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/)(링크 협상), [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([CHAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/228_chap_challenge_handshake_authentication_protocol/)/[EAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/229_eap_extensible_authentication_protocol/)), [NCP](/knowledge-base/studynote/03_network/04_data_link_layer_error/226_ncp_network_control_protocol/)(IP 동적 할당)라는 3단계 모듈형 접속 아키텍처는 오늘날 [VPN](/knowledge-base/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/)(PPTP, [L2TP](/knowledge-base/studynote/03_network/07_network_layer_routing/379_l2tp_layer_2_tunneling_protocol/))과 다양한 [터널링](/knowledge-base/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/) 기술의 코어 엔진으로 계속해서 살아가고 있다. PPP는 단순히 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 넘어 '안전하고 통제된 접속'이라는 네트워크의 기본 철학을 정의한 위대한 유산이다. 향후에는 고신뢰 저지연 링크 제어 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: 옛날식 다이얼 전화기는 박물관으로 갔지만, 그때 정립된 '전화번호 체계'와 '요금 청구 방식'은 스마트폰 시대인 지금까지도 변함없이 이어지는 것과 같습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [LAPD](/knowledge-base/studynote/03_network/04_data_link_layer_error/223_lapd_isdn_d_channel/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [프레이밍](/knowledge-base/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/) ([Framing](/knowledge-base/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/)) | [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)열을 의미 있는 전송 단위로 구분한다. |
| [오류 제어](/knowledge-base/studynote/03_network/04_data_link_layer_error/188_error_control_overview/) ([Error Control](/knowledge-base/studynote/03_network/04_data_link_layer_error/188_error_control_overview/)) | 검출과 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 정책을 함께 설계해야 한다. |
| [LCP](/knowledge-base/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">선행 개념: LAPD</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재 개념: PPP</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 A: LCP</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 B: 고신뢰 저지연 링크 제어</div></div>
</div>
</div>



PPP는 LAPD에서 출발해 현재 메커니즘을 정교화하고, 이후 LCP와 고신뢰 저지연 링크 제어 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 편지를 보낼 때 봉투를 제대로 닫고 틀린 글자가 없는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 해요.
2. 이 개념은 편지가 깨지거나 사라졌을 때 다시 보내는 규칙까지 정해줘요.
3. 그래서 중간에 흔들려도 중요한 내용이 더 안전하게 도착해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 345 / 1120

← **이전**: [223. LAPD (Link Access Procedure on the D channel)](/knowledge-base/studynote/03_network/04_data_link_layer_error/223_lapd_isdn_d_channel/)
**다음**: [225. LCP (Link Control Protocol)](/knowledge-base/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/) →

---
