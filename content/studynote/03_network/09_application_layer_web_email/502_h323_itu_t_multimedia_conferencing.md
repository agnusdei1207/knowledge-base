---
title: "502. H.323"
date: "2026-05-08"
tags:
  - "studynote-network"
weight: 502
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: H.323는 응용 계층과 웹/메일에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: H.323를 이해하면 응답 시간과 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: H.323은 LAN, WAN, 인터넷과 같이 패킷 전송을 보장하지 않는([QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 미보장) 패킷 교환망 위에서 시청각 멀티미디어 통신을 하기 위한 통신 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) '우산(Umbrella)' 규격이다. 단일 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이 아니라, H.225, H.245 등 수많은 서브 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 묶어놓은 거대한 종합 선물 세트다.

- **필요성**: 90년대 초, 인터넷이 보급되면서 사람들은 "비싼 구리선 전화망(PSTN) 말고, 공짜인 인터넷(IP) 선으로 전화를 걸자(VoIP)!"는 아이디어를 냈다. 그런데 문제가 터졌다. A 회사 장비와 B 회사 장비가 영상 통화를 하려는데 서로 규칙이 달라 화면이 깨졌다. 당시 통신업계의 절대 권력자였던 ITU-T(국제전기통신연합)가 나섰다. **"ISDN(종합정보통신망) 시절에 우리가 만들어 둔 깐깐하고 완벽한 통신 룰을 그대로 IP 망에 이식해서, 전 세계 어떤 장비든 100% 호환되게 하는 절대 헌법을 만들자!"** 이 철저한 중앙 통제식 전화국 마인드가 H.323이라는 거대한 괴물을 탄생시켰다.

- **💡 비유**: <strong>H.323</strong>은 유럽의 <strong>'황실 궁정 예절법'</strong>입니다. 춤(영상)을 추고 대화(음성)를 나누려면 책 100페이지 분량의 깐깐한 규칙(누가 먼저 인사하고, 손은 어떻게 잡고)을 1초의 오차도 없이 지켜야 합니다. 규칙이 빡빡해서 서로 싸울 일은 없지만, 평민(인터넷 개발자)들이 배우기엔 너무 어렵고 숨이 막힙니다. 반면 나중에 나온 <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/">SIP</a></strong>는 클럽의 <strong>'스트리트 힙합 규칙'</strong>입니다. 그냥 "야 나랑 놀래?" "콜!" 이라는 가벼운 텍스트([HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)) 두 마디로 파티가 터집니다. 결국 세상은 무거운 황실 예절(H.323)을 버리고 가벼운 힙합([SIP](/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/))을 선택했습니다.

- **등장 배경**:
  1. **ISDN의 황혼과 IP의 부상**: 기존의 전화선 화상 회의 표준이었던 H.320(ISDN 기반)을, 폭발적으로 성장하는 LAN/IP 망([이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/))에서도 돌아가게 하려는 ITU-T의 생존([Pivot](/studynote/12_it_management/01_governance_strategy/829_pivot/)) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/).
  2. **벤더 파편화 방지**: 마이크로소프트의 넷미팅(NetMeeting) 등 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 소프트웨어들이 이 표준을 탑재하며 90년대 후반 화상 통신의 실질적 글로벌 스탠다드로 군림했었다.

```text
+-------------------------------------------------------------+
|          H.323의 거대한 '우산(Umbrella)' 아키텍처: 통신사식 빡빡한 융합 망   |
+-------------------------------------------------------------+
|                                                             |
| 🏢 [ H.323 망의 4대 핵심 노드 (인프라 뼈대) ]                      |
|                                                             |
|  1. Terminal (단말): 화상 회의 PC, IP 전화기                      |
|  2. Gateway (게이트웨이): IP 망과 옛날 구리선(PSTN) 전화를 이어주는 통역사 |
|  3. Gatekeeper (게이트키퍼) 🌟 (H.323의 뇌): 통화 승인, 대역폭 관리, |
|     전화번호(Alias)를 IP 주소로 바꿔주는 절대 권력의 통제 센터!          |
|  4. MCU (다점 제어 장치): 3명 이상이 화상 회의할 때 영상을 섞어주는 중앙 믹서|
|                                                             |
|        ======= [ 통화 연결을 위한 지옥의 3단계 복잡한 핑퐁 ] ========   |
|                                                             |
| 📞 [ 터미널 A ] ------------------------------------------> [ 터미널 B ] |
|   1️⃣ H.225 (RAS): "게이트키퍼님, 저 전화 걸어두 돼요? IP 좀 찾아주세요!"    |
|   2️⃣ H.225 (Call Setup): "A야 나 전화 걸게! 띠르릉~ (Q.931 ISDN 룰 차용)"|
|   3️⃣ H.245 (Control): "우리 오디오는 G.711 쓰고, 비디오는 H.261 쓰자!"   |
|                                                             |
| 🌟 아키텍트 분석: H.323은 전화 연결 한 번 하려면 프로토콜이 3개(RAS, Call Setup,|
|   H.245)나 쪼개져서 미친 듯이 핑퐁을 쳐야 한다. 그것도 인간이 못 읽는 이진수(ASN.1)|
|   덩어리로. 보안과 통제(통신사 마인드)는 완벽하지만, 인터넷의 가벼운 철학과는 |
|   너무나도 동떨어진 무거운 '결합도(Tightly Coupled)'의 극치였다.           |
+-------------------------------------------------------------+
```

**[다이어그램 해설]** "H.323이 왜 SIP한테 져서 망했나요?"라는 질문의 해답이 담긴 아키텍처다. SIP는 `INVITE` 메시지 텍스트 1장 안에 "나랑 통화할래? + 내 마이크 스펙은 이거야([SDP](/studynote/09_security/01_intro_principles/048_sdp/))"를 한방에 섞어서 가볍게 던진다(1-Round Trip). 반면 H.323은 전화국의 꼰대 마인드를 버리지 못해, 전화 걸고(H.225), 상대방이 받으면 그제야 마이크 성능을 깐깐하게 조율(H.245)하는 지루한 핑퐁(Multiple Round Trips)을 강요했다. 이 무거운 연결 [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)([Call](/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/) Setup [Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))과 이진수 떡칠 코드는 인터넷 시대의 개발자들에게 환영받지 못하는 재앙이었다.

- **📢 섹션 요약 비유**: H.323 망의 <strong>게이트키퍼(Gatekeeper)</strong>는 깐깐한 <strong>'학교 기숙사 사감 선생님'</strong>입니다. 학생(Terminal)이 친구 방에 놀러 가려면 무조건 사감 선생님한테 "저녁 8시에 놀러 가도 됩니까? ([RAS](/studynote/01_computer_architecture/13_reliability_power_management/449_ras/) 권한 요청)" 허락을 받아야 하고, 사감이 "안 돼! 지금 기숙사 복도 꽉 찼어([대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 초과)!" 하면 방에서 나갈 수도 없는 극단적인 중앙 통제 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. H.323 우산 밑의 다중 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 패밀리

H.323은 스스로 무언가를 하지 않고 하위 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)들을 지휘하는 감독이다.
- **제어(Signaling) 파트**:
  - `H.225.0 RAS`: 게이트키퍼(통제 센터)와 단말 간의 등록(Registration), 권한(Admission), 상태(Status) 통신. (SIP의 `REGISTER`와 비슷).
  - `H.225.0 Call Setup`: 실제 두 단말기 간 전화벨을 울리고 끊는 호 제어. 웃긴 건 옛날 ISDN 유선 전화망 룰(`Q.931`)을 그대로 IP 위에 복붙해 놨다.
  - `H.245`: 통화가 연결된 후, 미디어 채널을 뚫고 코덱(Codec)을 협상하는 규격. (SIP의 `SDP` 역할).
- <strong>미디어(<a href="/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/">Media</a>) 파트</strong>:
  - `오디오 코덱`: G.711(일반 전화), G.722, G.729 등.
  - `비디오 코덱`: H.261, H.263, H.264 (오늘날 우리가 아는 그 H.264 맞다).
  - 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 SIP와 똑같이 <strong><code>RTP</code> (실시간 전송 <a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a>)</strong>를 타고 UDP로 날아간다. (결국 길 뚫는 방식만 달랐지, 짐(미디어)을 나르는 트럭은 둘 다 똑같은 걸 썼다).

### 2. ASN.1 BER (이진 인코딩)의 치명적 저주

H.323의 숨통을 끊어버린 기술적 패착이다.
- **ASN.1 (Abstract Syntax Notation One)**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 네트워크로 쏠 때 어떻게 포장할지 정의하는 오래된 통신 규칙이다.
- **문제점**: H.323은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 포장할 때 `BER(Basic Encoding Rules)` 이라는 이진(Binary) 규칙을 써서 `01011100` 형태의 기계어로 패킷을 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)해버렸다. 옛날 구리선 시절엔 인터넷 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)이 좁았으니 1바이트라도 아끼려고 이렇게 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)하는 게 '착한 공학'이었다.
- **시대의 변화**: 2000년대 [초고속](/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 인터넷이 깔렸다. 텍스트 몇 글자 더 쓴다고 망이 터지지 않게 되었다. 개발자들은 와이어샤크(Wireshark)로 패킷을 까봤을 때 영어로 `INVITE` 라고 훤히 보이는 SIP에 환호했다. H.323은 에러가 터지면 패킷이 0과 1로 뭉개져 있어 해독기를 돌리지 않으면 디버깅이 아예 불가능했다. <strong>개발 용이성(Developer Experience, <a href="/studynote/04_software_engineering/10_trends_pm_quality/726_platform_engineering_idp_dx/">DX</a>)의 참패</strong>였다.

```text
[SIP]
    |
    v
[H.323]
    |
    +---> [IP PBX]
```

- **📢 섹션 요약 비유**: H.323은 친구한테 쪽지를 보낼 때, 종이를 아끼려고 글씨를 암호화된 <strong>'모스 부호(이진수)'</strong>로 꾹꾹 눌러 써서 보냅니다. 배달부가 보기엔 가벼워서 좋지만, 친구가 쪽지를 받으면 암호 해독 책을 펴놓고 끙끙대며 번역(디코딩)해야 합니다(무거운 파싱 부하). SIP는 그냥 시원한 A4 용지에 <strong>'한글 텍스트'</strong>로 "안녕!"이라고 써서 보냅니다. 종이는 좀 무겁지만, 누구나 직관적으로 읽고 1초 만에 이해할 수 있죠(디버깅의 승리).

---

## Ⅲ. 비교 및 연결

### 딜레마: H.323 (통신사의 오만) vs [SIP](/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/) (인터넷 해커들의 실용주의)

통신 역사상 가장 치열했던 VoIP 표준 패권 전쟁이다.

| 비교 항목 | H.323 (ITU-T 진영) | [SIP](/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/) ([IETF](/studynote/03_network/12_iot_wpan_edge/635_ietf_core_working_group_coap/) 진영) | 승패 결과 |
|:---|:---|:---|:---|
| **출신 성분** | 전화국(Telco) 아저씨들. "엄격한 통제와 안정성이 최우선!" | 인터넷 해커([IETF](/studynote/03_network/12_iot_wpan_edge/635_ietf_core_working_group_coap/)). "가볍고 유연하게, 웹(Web)처럼 만들자!" | <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/">SIP</a> 완승.</strong> 통신사 꼰대 마인드는 인터넷 확장을 못 버팀. |
| **코딩 구조** | **이진(Binary) 기반 (ASN.1)**. 촘촘하지만 눈에 안 보임. | <strong>텍스트(Text) 기반 (<a href="/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a> 모방)</strong>. [가독성](/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/) 최고. | <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/">SIP</a> 압승.</strong> 개발자 친화성([DX](/studynote/04_software_engineering/10_trends_pm_quality/726_platform_engineering_idp_dx/))이 표준 생태계를 장악함. |
| **확장성** | H.323 위원회 모여서 도장 찍기 전까진 기능 추가 불가. (폐쇄적) | 그냥 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 헤더에 `X-My-Feature: Yes` 문자열 한 줄 추가하면 끝! | <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/">SIP</a> 완승.</strong> 게임, 화상, 메신저 등 모든 [UC](/studynote/12_it_management/02_itsm_itil/871_underpinning_contract/) 융합을 다 빨아들임. |
| <strong><a href="/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/">Call</a> Setup 속도</strong> | 연결, 코덱 협상 등 핑퐁(Round Trip) 수십 번 쳐야 함. (느림) | `INVITE` 1방에 코덱 정보([SDP](/studynote/09_security/01_intro_principles/048_sdp/)) 다 섞어 던짐. ([초고속](/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/)) | <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/">SIP</a> 압승.</strong> 스마트폰 시대엔 무거운 연결은 죄악임. |

### 과목 융합 관점

- <strong>네트워크 공학 (<a href="/studynote/03_network/07_network_layer_routing/384_nat_t_ipsec_nat_traversal_udp_4500/">NAT Traversal</a> - <a href="/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/">방화벽</a> 통과의 저주)</strong>: SIP도 공유기([NAT](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/))를 통과할 때 [SDP](/studynote/09_security/01_intro_principles/048_sdp/) 속 사설 IP 때문에 고통받지만, H.323은 그 고통의 레벨이 우주급이다. H.323은 통신할 때 1개의 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)만 쓰지 않는다. [Call](/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/) Setup용 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)(1720), H.245용 동적 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), RAS용 [UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 등, 전화를 한 통 걸면 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)에 '임의의 구멍([포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))'을 미친 듯이 여러 개 뚫어재껴야 한다. 회사 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 담당자(보안팀)가 제일 극혐하는 구조다. 결국 H.323을 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 너머로 쓰려면, [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)(Router) 자체가 H.323 패킷의 이진수 속살까지 까보고 동적으로 구멍을 뚫어주는 영리한 <strong><a href="/studynote/03_network/06_network_layer_ip/310_alg_application_layer_gateway_nat_traversal/">ALG</a> (<a href="/studynote/03_network/06_network_layer_ip/310_alg_application_layer_gateway_nat_traversal/">Application Layer Gateway</a>)</strong> 기능을 하드웨어 레벨에서 비싼 돈을 주고 탑재해야만 했다. (인프라 비용의 떡상 원인).
- **클라우드와 엔터프라이즈 (레거시 마이그레이션 딜레마)**: 2020년대 지금, H.323을 새로 구축하는 회사는 지구상에 존재하지 않는다. 하지만 거대한 금융권 본사나 정부 청사의 구석에는 아직도 10년 전 10억을 주고 산 낡은 시스코/폴리콤 H.323 화상 회의 장비(MCU) 쇳덩이가 돌아가고 있다. IT 아키텍트는 이걸 버릴 수 없다. 그래서 최새로운 유형의 웹 기반 줌(Zoom)이나 마이크로소프트 팀즈(Teams) 클라우드를 도입할 때, 이 낡은 H.323 쇳덩이 방과 클라우드 화상 방을 하나로 엮어주는 <strong>'Cloud Video Interop (CVI) 게이트웨이'</strong>라는 융합 통역기를 중간에 세팅해야 하는 레거시 빚 청산(Tech Debt) 야근을 운명적으로 겪게 된다.

- **📢 섹션 요약 비유**: H.323 화상 회의 장비는 집에 놔둔 거대한 <strong>'LP판 전축 세트'</strong>와 같습니다. 소리(품질)도 좋고 뭔가 기계적으로 완벽해 보이지만, 요즘 유행하는 스마트폰 [블루투스](/studynote/03_network/12_iot_wpan_edge/605_bluetooth_ieee_802_15_1_piconet_scatternet/) 이어폰([SIP](/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/), [WebRTC](/studynote/03_network/09_application_layer_web_email/505_webrtc_web_real_time_communication/))이랑은 절대 연결이 안 됩니다. 아빠는 전축이 아까워서 못 버리고(레거시), 결국 중간에 비싼 변환 젠더(게이트웨이)를 주렁주렁 달아서 억지로 스마트폰 음악을 틀고 있는 웃픈 상황이 연출되는 겁니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

1. **시나리오 — 구형 H.323 인프라와 새로운 유형의 SIP망 간의 CVI (Cloud Video Interop) 융합 브릿징**: 대기업 본사. 임원 회의실엔 15년 된 5,000만 원짜리 폴리콤(Polycom) H.323 화상 장비가 벽에 박혀있다. 그런데 재택근무하는 직원들은 노트북에서 MS 팀즈(Teams - [SIP](/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/)/[WebRTC](/studynote/03_network/09_application_layer_web_email/505_webrtc_web_real_time_communication/) 기반)를 쓴다. 내일 당장 사장님이 임원 회의실에서 재택 직원 100명과 화상 회의를 하겠다고 통보했다. 장비끼리 언어가 달라 연결이 안 된다.
   - **판단**: 전 세계 엔터프라이즈 화상 망 관리자가 겪는 가장 끔찍한 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 파편화 장애다. H.323 장비는 절대 스스로 팀즈 클라우드로 붙지 못한다. 실무 아키텍트는 펙시프(Pexip)나 시스코([Cisco](/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/)) 같은 벤더가 파는 <strong>CVI(Cloud Video Interop) 게이트웨이 구독권(<a href="/studynote/12_it_management/05_security_compliance/951_saas/">SaaS</a>)</strong>을 긴급하게 뚫어야 한다.
   임원실 H.323 장비가 `12345@teams.b2b.com` 이라는 가상 IP로 전화를 걸면(Dial-in), 펙시프 게이트웨이가 중간에서 무거운 H.323 이진수 신호를 받아, 가벼운 [SIP](/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/)/[WebRTC](/studynote/03_network/09_application_layer_web_email/505_webrtc_web_real_time_communication/) 텍스트 껍데기로 0.1초 만에 통역(Transcoding)하여 MS 팀즈 서버로 패킷을 꽂아주는 '우아한 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 세탁(Translation)'이 가동되어야 사장님의 분노를 막을 수 있다.

2. **시나리오 — ISDN 유선망 철거와 미디어 게이트웨이(Voice Gateway)의 존버**: 구형 공공기관. 아직도 외부에서 걸려 오는 민원 전화망이 E1/T1(ISDN 구리선) 규격의 H.323 기반 전화 교환기(PBX)에 물려 있다. 망을 100% 최신 All-IP [SIP](/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/) 망으로 갈아엎는 프로젝트를 수주했다.
   - **판단**: "H.323 쓰레기니까 내일 당장 끄고 버리세요!"라고 하면 전화가 끊겨 기관이 마비된다(빅뱅 배포의 자살). 1단계로, 기존 KT 국선(ISDN)과 신규 내부 [SIP](/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/) 서버 사이에 **미디어 게이트웨이(Voice Gateway)** 장비를 샌드위치처럼 끼워 넣어야 한다. 외부에서 아날로그 음성(`Q.931/G.711`)이 들어오면 게이트웨이가 이걸 IP 패킷(`SIP/RTP`)으로 깎아서 내부망으로 토스해 준다(Soft Landing). 2단계로 KT 구리선을 100% 인터넷 선([SIP](/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/) Trunk)으로 개통받은 날, 비로소 구형 H.323 PBX 장비의 전원 플러그를 뽑아 영원한 무덤으로 보내는 2-Step [스트랭글러 피그](/studynote/04_software_engineering/05_devops_ci_cd/310_strangler_fig_pattern/)([Strangler Fig](/studynote/04_software_engineering/05_devops_ci_cd/310_strangler_fig_pattern/)) 이관 패턴이 정석이다.

```text
  +-------------------------------------------------------------+
  |         실무 아키텍처: 왜 H.323은 방화벽(Firewall) 관리자의 주적이 되었나? |
  +-------------------------------------------------------------+
  | [ 🏢 회사 내부망 (H.323 단말) ]               [ 🌍 인터넷 (외부 거래처) ]  |
  |                                                             |
  | 1. 통화 시작! (1720 포트로 똑똑) ----------> (방화벽: "ㅇㅋ 1720은 열어줄게") |
  |                                                             |
  | 2. 협상 시작 (H.245) <----> (문제 터짐💥)  <----> "포트 31055번 새로 열자!"|
  |                                                             |
  | 3. 음성/영상(RTP) <----> (대환장💥💥) <----> "포트 40001번, 40002번 열자!"|
  |                                                             |
  | 🛡️ [ 일반 방화벽의 멘붕 ]                                         |
  |   - "아니, 처음에 1720 포트 하나만 쓴다며? 왜 통화 중에 지들끼리 이진수(ASN.1)|
  |     패킷 속에서 지들 맘대로 임의의 포트(Random Port) 10개를 뚫자고 합의함? |
  |     난 보안장비라 그런 거 몰라! 싹 다 차단(Drop) 쾅!!" -> (화상 화면 안 뜸)  |
  |                                                             |
  |        ======= [ 🌟 아키텍트의 구원: H.323 ALG 하드웨어 가속 ] ======== |
  |                                                             |
  | 🤖 [ ALG (Application Layer Gateway) 탑재 방화벽 ]              |
  |   - 방화벽이 그냥 길만 뚫어주는 게 아니라, H.323 이진수 패킷을 핀셋으로 까봄!|
  |   - "오! 패킷 내용 보니까 얘네 40001번 포트 쓰기로 방금 합의했네? |
  |     내가 눈치껏 40001번 방화벽 구멍을 스르륵 동적으로 열어줄게(Pinholing)!"  |
  |   - -> (비로소 화면이 터짐. 하지만 방화벽 CPU 리소스는 걸레짝이 됨 💀)       |
+-------------------------------------------------------------+
```

**[다이어그램 해설]** VoIP 망 구축 시 가장 많이 겪는 'One-way Audio(한쪽 목소리만 들림)'나 '화면 안 뜸' 에러의 근본 원인을 해부한 도면이다. H.323은 시그널링(제어)과 미디어([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))의 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 번호를 통화할 때마다 난수(Random)로 찢어서 쓴다. 일반 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)(L4)은 IP와 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)만 본다. 패킷 '내용물(L7)' 안에 적혀있는 "우리 40001번 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 쓰자"라는 이진수 약속을 읽지 못하고 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 막아버린다. 그래서 H.323 망을 칠 때는 반드시 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)을 7계층(L7)까지 다 까볼 수 있는 스마트한 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)([ALG](/studynote/03_network/06_network_layer_ip/310_alg_application_layer_gateway_nat_traversal/)/SBC)으로 비싸게 세팅해야 하는 극악의 유지보수 비용([TCO](/studynote/12_it_management/01_governance_strategy/016_tco/)) 증가를 낳았다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **기술적**: 사내에 아직 돌아가는 레거시 H.323 쇳덩이를 언제까지 안고 갈 것인가? H.323 장비는 대부분 하드웨어 의존적(DSP 칩 내장)이라 제조사([Cisco](/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/), Polycom)가 EoL(단종) 선언을 해버리면 고장 났을 때 부품을 못 구해 회의실이 문을 닫아야 한다. 내년 IT 예산 기안([ISP](/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/))을 짤 때, 쇳덩이 장비를 클라우드 기반 [WebRTC](/studynote/03_network/09_application_layer_web_email/505_webrtc_web_real_time_communication/)(줌, 팀즈, 웹엑스)의 순수 소프트웨어([SaaS](/studynote/12_it_management/05_security_compliance/951_saas/)) 기반 룸 시스템으로 전면 걷어내는 **All-Cloud Video Migration** 마스터플랜을 그렸는가?
- **운영·보안적**: 공인 IP를 달고 H.323 게이트키퍼(Gatekeeper)를 인터넷에 열어둔 경우, 옛날 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 특성상 암호화(H.235 [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))를 안 켜고 평문으로 쏘는 경우가 90%다. 와이어샤크만 켜면 외부 해커가 사장님 화상 회의의 음성/영상 [RTP](/studynote/03_network/08_transport_layer/451_rtp_real_time_transport_protocol/) 패킷을 그대로 가로채서(Sniffing) 녹화본을 떠버릴 수 있다. 구형 H.323 장비를 외부와 연결해야 한다면, 무조건 <strong><a href="/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/">가상 사설망</a>(<a href="/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/">VPN</a>) 터널</strong> 안으로 때려 박아 물리적 암호화 캡슐을 씌워야만 감청 참사를 막을 수 있다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong>레거시 스펙 억지 호환의 괴물화 (Frankenstein <a href="/studynote/12_it_management/05_security_compliance/319_architecture/">Architecture</a>)</strong>: 클라우드 화상 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(Zoom 등)를 런칭하는데, "국내 공공기관은 아직 H.323 많이 쓰니까 우리 서버 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 단에 H.323 이진수 파싱(Parsing) 엔진도 네이티브로 다 때려 박자!"라고 결정하는 아키텍트의 오판. H.323의 문법은 너무 방대하고 복잡해서 이걸 직접 개발해 얹는 순간, 가볍게 날아가야 할 클라우드 시그널링 메인 서버([SIP](/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/)/[WebRTC](/studynote/03_network/09_application_layer_web_email/505_webrtc_web_real_time_communication/))가 무거운 이진수 예외 처리 코드에 짓눌려 스파게티 괴물로 썩어버린다. <strong>"현대 아키텍처의 코어는 무조건 가벼운 최신 룰(<a href="/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/">SIP</a>/<a href="/studynote/03_network/09_application_layer_web_email/505_webrtc_web_real_time_communication/">WebRTC</a>)로만 통일하고, 낡은 옛날 언어(H.323)를 쓰는 놈들은 성문 밖에 '전용 게이트웨이(번역기)' 하나만 달랑 세워둬서 거기서 세탁하고 들어오게 해라."</strong> 이것이 레거시 전염을 막는 방역 융합 철칙이다.

- **📢 섹션 요약 비유**: 최신 스마트폰([SIP](/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/)) 안에다 옛날 구형 <strong>'카세트테이프(H.323) 재생기'</strong>를 억지로 구겨 넣으려는 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)입니다. 폰은 무거워지고 고장만 잘 나죠. 스마트폰은 그냥 최신 mp3 코어만 놔두고, 카세트테이프 음악을 듣고 싶은 꼰대 아저씨가 오면 바깥에서 테이프를 mp3로 구워서(변환 게이트웨이) 폰으로 넘겨주게 만드는 것이 훨씬 스마트한 시스템 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)입니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | 아날로그/ISDN 회선 화상 장비 (H.320) | IP 기반 멀티미디어 통합 H.323 융합 전환 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 회의할 때마다 비싼 ISDN [전용선](/studynote/03_network/05_lan_wan_l2_devices/266_leased_line_basics_e1_t1_t3/) 요금 부과 | 사내 LAN(IP) 선 하나로 음성/영상 공짜 통신 | 기업의 **전사적 통신 인프라 요금(OPEX) 80% 이상 극단적 상각** |
| **정량** | 폴리콤 장비는 소니 장비랑 영상 통화 불가 | ITU-T 절대 헌법으로 모든 벤더 코덱 통일화 | 이기종 화상 장비 간 <strong>상호 운용성(<a href="/studynote/06_ict_convergence/01_blockchain/084_blockchain_interoperability_polkadot_cosmos/">Interoperability</a>) 100% 보장 획득</strong> |
| **정성** | "전화선 따로, 랜선 따로" 2가닥 공사 지옥 | 전화기(Voice)와 [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 망을 한 줄로 합침 | 케이블 포설 최소화 및 **IP-PBX 기반의 효율적 사내 인프라 중앙 통제** |

### 미래 전망
- **위대한 패배자의 무덤 (박물관행)**: H.323의 미래 전망은 없다. 2020년대를 기점으로 글로벌 화상/음성 통신 패권은 [SIP](/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/)(백엔드 인프라)와 [WebRTC](/studynote/03_network/09_application_layer_web_email/505_webrtc_web_real_time_communication/)(프론트엔드 브라우저)의 양강 융합 체제로 완전히 끝났다. H.323은 ISDN 시대의 유산(통제, 빡빡한 룰, 무거운 이진 코드)을 너무 많이 끌어안고 인터넷이라는 자유로운 망에 올라탔다가 진화의 속도를 따라가지 못하고 멸종한 공룡이 되었다. 향후 10년 내에 관공서의 마지막 H.323 쇳덩이 장비의 전원 코드가 뽑히는 날, 이 표준은 IT 교과서에서나 볼 수 있는 완벽한 역사 속으로 사라질 것이다.
- **H.323이 남긴 불멸의 위대한 코덱 유산 (H.264)**: H.323 껍데기 자체는 SIP에 져서 멸망했지만, H.323 우산 밑에서 영상을 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)하기 위해 깎아냈던 <strong>비디오 코덱 기술(H.261 -> H.263 -> H.264)</strong>은 오히려 세상을 정복했다! 유튜브(YouTube), 넷플릭스, 아이폰 동영상 녹화 등 지구상 모든 동영상의 90% 이상이 아직도 ITU-T가 창조해 낸 위대한 'H.264/AVC' 코덱 알고리즘으로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)되어 전 세계를 돌아다닌다. 머리(시그널링)는 잘렸지만, 그 심장(미디어 코덱)은 인터넷 우주 전체를 호령하는 승리자로 영원히 살아남은 공학적 아이러니다.

### 참고 표준
- **ITU-T H.323 (1996년 첫 제정)**: 패킷 기반(IP) 망에서 오디오, 비디오, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통신을 제공하기 위한 멀티미디어 시스템의 뼈대를 규정한 가장 방대하고 무거운 국제 표준 권고안.
- **Q.931 (ISDN 호 제어)**: H.323이 전화 연결을 위해 뱃속에 품었던 룰. 원래 유선 전화국에서 쓰던 낡은 규칙을 IP 망에 억지로 끼워 맞춘 덕분에 끔찍하게 무거운 레거시의 저주를 떠안게 된 원흉 규격.

"가장 완벽하고 촘촘하게 짜여진 법전은, 가장 먼저 세상의 변화 속도에 짓눌려 붕괴한다." H.323은 90년대 중반 파편화되어 싸우던 무법의 화상 회의 시장을 하나로 묶어낸 위대한 통일 제국의 황제였다. 전화국(ITU-T) 최고 엘리트들의 강박적인 안정성 집착이 빚어낸 이 장대한 아키텍처는 에러를 허용하지 않는 완벽함을 추구했다. 하지만 그 완벽함을 위해 이진수(ASN.1)라는 무거운 철갑옷을 둘렀고, 가벼운 연결(Agility)을 원하는 인터넷 시대 개발자들의 열망을 외면했다. 결국, [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 메모장 하나 들고 나타난 젊고 건방진 [SIP](/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/) 진영의 '단순함([Simplicity](/studynote/09_security/01_intro_principles/014_simplicity/))'이라는 무기 앞에 제국의 성벽은 허무하게 무너져 내렸다. 그러나 우리가 오늘날 줌(Zoom)에서 깨끗한 화질로 얼굴을 보고, 넷플릭스 영상을 스트리밍으로 볼 수 있는 가장 밑바닥의 비디오 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)(H.264 코덱) 기술의 DNA에는 여전히 H.323 황제가 쏟아부었던 위대한 수학적 헌신이 피처럼 흐르고 있다.

- **📢 섹션 요약 비유**: H.323은 인터넷 화상 통신 역사에서 <strong>'무겁고 단단한 중세 기사(통신사)'</strong>였습니다. 완벽한 철갑옷(이진 코드)을 입고 규칙대로 싸웠지만, 달리기(속도와 확장성)가 너무 느렸죠. 결국 청바지 입고 가벼운 권총(텍스트 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/))을 든 <strong>'현대식 카우보이(<a href="/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/">SIP</a>)'</strong>에게 총을 맞고 쓰러졌습니다. 하지만 그 중세 기사가 죽기 전에 남긴 뛰어난 보검(H.264 비디오 코덱)은 현대 카우보이들이 빼앗아 들어 아직도 세상에서 가장 날카로운 무기로 쓰이고 있답니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [SIP](/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) ([Session](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)) | 사용자 상태 유지와 요청 흐름을 묶는다. |
| 캐시 (Cache) | 응답 속도와 백엔드 부하에 직접 영향을 준다. |
| [IP PBX](/studynote/03_network/09_application_layer_web_email/503_ip_pbx_private_branch_exchange/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: SIP]
    |
    v
[현재 개념: H.323]
    |
    +---> [확장 A: IP PBX]
    +---> [확장 B: 지능형 애플리케이션 전달]
```

H.323는 SIP에서 출발해 현재 메커니즘을 정교화하고, 이후 IP PBX와 지능형 애플리케이션 전달 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. <strong>H.323</strong>은 옛날 옛적 할아버지들이 만든 <strong>'엄청나게 까다로운 화상 전화 규칙서'</strong>예요. 전화를 걸려면 "안녕하십니까, 통화를 요청해도 되겠사옵니까?" 하고 10번이나 절을 해야 했죠(느리고 무거움).
2. 규칙이 너무 두꺼워서 컴퓨터가 읽기 좋게 암호(이진수)로 꽉꽉 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)해 놨더니, 막상 프로그램을 고쳐야 하는 개발자 삼촌들은 암호를 못 읽어서 눈물이 났어요.
3. 그래서 사람들은 "아휴 답답해! 그냥 편하게 '야 통화하자!' 하고 가벼운 한글 문자(텍스트)로 보내자!"라며 새로 만든 <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/535_system_in_package/">SIP</a></strong>라는 가벼운 규칙으로 몽땅 갈아타 버렸답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 623 / 1120

<- **이전**: [501. SIP (Session Initiation Protocol)](/studynote/03_network/09_application_layer_web_email/501_sip_session_initiation_protocol_voip/)
**다음**: [503. IP PBX](/studynote/03_network/09_application_layer_web_email/503_ip_pbx_private_branch_exchange/) ->

---
