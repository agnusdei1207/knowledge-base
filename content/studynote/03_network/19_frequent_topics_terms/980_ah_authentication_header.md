---
title: "AH (Authentication Header)"
date: "2026-05-08"
tags:
  - "studynote-network"
weight: 980
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AH는 빈출 주제와 용어에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: AH를 이해하면 구분 명확성과 설명력 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) ([Authentication Header](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/))는 IP 패킷의 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 및 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 보장하기 위해 [IETF](/studynote/03_network/12_iot_wpan_edge/635_ietf_core_working_group_coap/) (Internet 엔진ering [Task](/studynote/02_operating_system/02_process_thread/150_task/) Force)에서 정의한 [IPSec](/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/) 보안 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이다. 패킷의 내용이 전송 중에 변경되지 않았으며, 송신자가 위장되지 않았음을 수신자가 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)할 수 있게 해주는 '디지털 봉인' 역할을 한다.
- **필요성**: 기존의 평문 IP 기반 통신에서는 공격자가 패킷을 가로채어 출발지 IP 주소를 조작 ([IP Spoofing](/studynote/03_network/14_network_security_threats/704_ip_spoofing_trust_injection/))하거나 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 내용을 몰래 변경하더라도 수신자가 이를 알아챌 방법이 없다. 금융 거래나 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 정보 교환 시에는 내용이 암호화되지 않아도 무방하더라도 내용이 조작되지 않았다는 '확실한 증명'이 반드시 필요하다.
- **💡 비유**: AH는 중요한 공문서 봉투 겉면에 찍힌 '밀랍 인장 (Wax Seal)'과 같다. 투명한 봉투라 누구나 안의 글씨 (평문 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 읽을 수는 있지만, 도중에 누군가 글자를 고치거나 위조 서명을 넣으려 하면 인장이 깨지기 때문에 수신자는 즉시 조작 사실을 알아챌 수 있다.
- **등장 배경 및 발전 과정**:
  1. <strong>IP <a href="/studynote/02_operating_system/10_security/598_spoofing/">스푸핑</a> 및 <a href="/studynote/03_network/14_network_security_threats/707_session_hijacking_tcp_seq_cookie/">세션 하이재킹</a> 위협</strong>: 1990년대 초 인터넷 해킹 기법이 발전하면서, 타인의 IP로 위장하여 통신에 끼어드는 공격이 성행했다.
  2. <strong><a href="/studynote/09_security/01_intro_principles/003_integrity/">무결성</a> <a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a>의 필요성 대두</strong>: [기밀성](/studynote/09_security/01_intro_principles/002_confidentiality/)(암호화)은 연산 비용이 크고 각국의 수출 통제 규제를 받았기 때문에, 순수하게 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)과 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)만 제공하는 가벼운 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 필요성이 제기되었다.
  3. **AH와 ESP의 분리 표준화 (RFC 2402, 4302)**: [IPSec](/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/) 프레임워크는 강력한 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/))과 암호화([ESP](/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/))를 분리하여 설계함으로써, 환경과 요구사항에 맞게 취사선택할 수 있는 유연한 보안 아키텍처를 완성했다.

[AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) 도입 전 IP [스푸핑](/studynote/02_operating_system/10_security/598_spoofing/) 공격의 위협과 [AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) 도입 후의 방어 메커니즘을 구조도로 시각화하면 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)이 왜 중요한지 명확해진다.

```text
  +-------------------------------------------------------------+
  |              IP 스푸핑 위협 및 AH를 통한 방어 원리              |
  +-------------------------------------------------------------+
  |                                                             |
  |  [AH 미적용 시 IP Spoofing 공격]                                |
  |  해커 (IP: 1.1.1.1) ------------> 목적지 서버                     |
  |  가짜 패킷: [ Src IP: 정상PC(10.0.0.2) | Data: "돈을 보내라" ]     |
  |  ⚠ 서버: "정상PC(10.0.0.2)가 보낸 명령이군. 실행!" (위장 성공)         |
  |                                                             |
  |  [AH 적용 시 방어 성공]                                          |
  |  해커 (IP: 1.1.1.1) ------------> 목적지 서버                     |
  |  조작 패킷: [ Src IP: 정상PC | AH Header | Data ]               |
  |                                                             |
  |  서버의 AH 검증 프로세스:                                        |
  |   1. AH에 포함된 무결성 해시(ICV) 확인                            |
  |   2. 서버가 수신된 (IP헤더+데이터+비밀키)로 해시 재계산              |
  |   3. 수신된 ICV ≠ 계산된 ICV (해커는 정상PC의 비밀키를 모름)          |
  |  ✅ 서버: "해시값이 불일치한다! IP가 조작된 패킷이군. 폐기!"            |
  +-------------------------------------------------------------+
```

**[다이어그램 해설]** [IPSec](/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/) AH가 없는 환경에서 목적지 서버는 IP 헤더의 출발지 주소 (Source IP)를 전적으로 신뢰하여 작동한다. 따라서 해커가 자신의 IP를 속여 패킷을 전송하면 서버는 이를 막아낼 수 없다. 그러나 AH를 적용하면 송수신자만 아는 공유 비밀키 (Shared [Secret](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))를 이용해 전체 패킷에 대한 해시 ([MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/), [Message Authentication Code](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/))를 생성하여 패킷에 부착한다. 해커가 IP 헤더를 조작하려 해도 비밀키를 모르기 때문에 올바른 해시값을 다시 계산하여 붙일 수 없다. 결국 수신 서버에서 해시 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) (ICV [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/))에 실패하여 조작된 패킷은 즉시 버려지며 (Drop), 완벽한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 발신자 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)이 이루어진다.

- **📢 섹션 요약 비유**: 서류를 보낼 때 보내는 사람의 지문(비밀키)으로 서명한 위조 방지 홀로그램 스티커([AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/))를 붙여서, 도중에 누군가 잉크를 덧칠하거나 보낸 사람 이름을 바꾸면 스티커가 깨지도록 설계한 것과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소

| 요소명 | 역할 | 내부 동작 | [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | 비유 |
|:---|:---|:---|:---|:---|
| <strong><a href="/studynote/12_it_management/04_sdlc_testing/159_spi_schedule_performance_index/">SPI</a> (<a href="/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a> Parameters <a href="/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">Index</a>)</strong> | 보안 연관 ([SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/)) [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | 수신자가 이 패킷을 처리할 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)/키를 찾기 위한 32비트 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) | 32-bit Integer | 자물쇠를 열 열쇠 번호 |
| **Sequence Number** | [재생 공격](/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/) (Anti-replay) 방지 | 패킷마다 1씩 증가하는 [카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/), 이미 받은 번호면 폐기 | 32/64-bit [Counter](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) | 은행 [OTP](/studynote/01_computer_architecture/15_advanced_topics/748_otp/) 일회용 비밀번호 |
| <strong>ICV (<a href="/studynote/09_security/01_intro_principles/003_integrity/">Integrity</a> Check Value)</strong> | [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 및 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | IP 헤더, [AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) 헤더, 페이로드를 [HMAC](/studynote/03_network/13_network_security_basics/674_hmac_hash_based_mac_ipsec/) ([MD5](/studynote/03_network/13_network_security_basics/668_md5_hash_collision_vulnerability/)/SHA) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 계산한 해시값 | [HMAC](/studynote/03_network/13_network_security_basics/674_hmac_hash_based_mac_ipsec/)-SHA256 등 | 위조 방지 밀랍 인장 |
| **Next Header** | 상위 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 지정 | [AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) 헤더 다음에 오는 페이로드의 종류 ([TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/), [UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 등) 명시 | 8-bit [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) ID | 봉투 안의 내용물 종류 |
| **Payload Length** | [AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) 헤더의 길이 지정 | 전체 패킷 내에서 [AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) 헤더가 차지하는 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 수 | 8-bit Length | 봉인 스티커의 크기 |

### [AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) 패킷의 물리적 구조와 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 범위

AH의 핵심은 패킷에서 '어디까지를 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 범위([Authentication](/studynote/02_operating_system/10_security/604_authentication_factors/) Coverage)로 삼는가'이다. ESP가 IP 헤더를 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)하지 않는 반면, AH는 IP 헤더의 '고정 필드'까지 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 영역에 포함시켜 더 넓은 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 제공한다.

```text
  +------------------------------------------------------------------+
  |                 IPSec AH의 패킷 캡슐화 및 인증 범위 (수송 모드)        |
  +------------------------------------------------------------------+
  |                                                                  |
  | [IPSec AH 수송 모드 패킷 구조]                                     |
  |                                                                  |
  |     <---------------------- 인증 범위 (MAC 계산 영역) ------------------>|
  | +---------------+---------------+---------------+----------------+ |
  | | Orig IP Header|   AH Header   |   TCP Header  |      Data      | |
  | |(가변 필드 제외) | (ICV 필드 제외) |               |                | |
  | +---------------+---------------+---------------+----------------+ |
  |                                                                  |
  | [AH Header 세부 구조 (RFC 4302)]                                   |
  |  0                   1                   2                   3   |
  |  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 |
  | +---------------+---------------+-------------------------------+|
  | | Next Header   | Payload Len   |          RESERVED             ||
  | +---------------+---------------+-------------------------------+|
  | |                  Security Parameters Index (SPI)              ||
  | +---------------------------------------------------------------+|
  | |                      Sequence Number                          ||
  | +---------------------------------------------------------------+|
  | |                                                               ||
  | |            Integrity Check Value (ICV) - 가변 길이                ||
  | |                                                               ||
  | +---------------------------------------------------------------+|
  +------------------------------------------------------------------+
```

**[다이어그램 해설]** AH는 수송 모드 적용 시 기존 IP 헤더와 상위 계층 ([TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/[UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/)) 사이에 위치한다. AH의 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 범위([Authentication](/studynote/02_operating_system/10_security/604_authentication_factors/) Coverage)는 놀랍게도 IP 헤더, [AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) 헤더 자신, 그리고 상위 페이로드 전체를 포괄한다. 단, 라우터를 거치며 값이 필연적으로 변하는 IP 헤더의 가변 필드 (Mutable Fields, 예: [TTL](/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/), [Header Checksum](/studynote/03_network/06_network_layer_ip/296_header_checksum_ipv4_integrity/), TOS 등)는 ICV 계산을 할 때 임시로 '0'으로 설정하여 계산에서 제외한다. 이를 통해 라우터를 정상적으로 통과하면서도 IP 주소(고정 필드)의 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 지켜낸다. [AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) 헤더 내부는 다음 헤더를 가리키는 포인터, [SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)용 [SPI](/studynote/12_it_management/04_sdlc_testing/159_spi_schedule_performance_index/), [재생 공격](/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/) 방어용 Sequence Number, 그리고 최종 해시값인 ICV로 구성된다.

### 심층 동작 원리 ([무결성](/studynote/09_security/01_intro_principles/003_integrity/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 및 [재생 공격](/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/) 방어)

AH의 송수신 처리 메커니즘은 해시 연산과 [카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) 윈도우 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)으로 이루어진다.

① **전송측 ICV 계산**: 송신자는 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)할 IP 패킷을 구성하고, 가변 필드를 0으로 마스킹한다.
② **해싱 적용**: 마스킹된 패킷 전체와 양단 간에 사전 합의된 비밀키(Shared [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))를 결합하여 [HMAC](/studynote/03_network/13_network_security_basics/674_hmac_hash_based_mac_ipsec/) (Hash-based [Message Authentication Code](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)) 함수 (예: [HMAC](/studynote/03_network/13_network_security_basics/674_hmac_hash_based_mac_ipsec/)-SHA256)를 돌려 고유한 ICV 값을 얻어낸다.
③ <strong><a href="/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/">AH</a> 부착 및 전송</strong>: 계산된 ICV를 [AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) 헤더에 기록하고, 증가시킨 Sequence Number를 함께 담아 인터넷으로 전송한다.
④ <strong>수신측 Anti-replay <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong>: 수신자는 AH의 Sequence Number를 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하여 슬라이딩 윈도우 (Sliding Window, 보통 64 패킷) 내에 있는지, 이전에 받은 적이 있는 패킷인지 검사한다. 중복/과거 패킷이면 즉시 폐기 ([재생 공격](/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/) 방어).
⑤ **수신측 ICV 재계산 및 비교**: Sequence Number를 통과하면 수신자는 동일한 비밀키로 패킷의 ICV를 재계산한다. 패킷에 적힌 ICV와 재계산된 ICV가 완벽히 일치하면 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 및 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)이 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)된 것이며, 상위 계층 ([TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/))으로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 올려보낸다.

- **📢 섹션 요약 비유**: 송신자가 서류에 고유 번호(시퀀스 넘버)와 비밀 도장(ICV)을 찍어 보내면, 수신자는 돋보기로 도장의 진위를 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고 번호표 대장을 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해 어제 낸 서류를 오늘 다시 내는 사기꾼([재생 공격](/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/))을 걸러내는 치밀한 검문소 역할을 합니다.

---

## Ⅲ. 비교 및 연결

IPSec의 양대 산맥인 AH와 ESP는 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)하는 영역과 암호화 제공 여부에서 극명한 차이를 보인다.

| 비교 항목 | [AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) ([Authentication Header](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/)) | [ESP](/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/) ([Encapsulating Security Payload](/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/)) | 판단 포인트 |
|:---|:---|:---|:---|
| <strong><a href="/studynote/09_security/01_intro_principles/002_confidentiality/">기밀성</a> (암호화)</strong> | ❌ 지원 안 함 (평문 전송) | ✅ 지원 ([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 암호화) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 은닉이 필수적인가? |
| <strong><a href="/studynote/09_security/01_intro_principles/003_integrity/">무결성</a> / <a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a></strong> | ✅ 지원 (IP 헤더 일부 + 페이로드 전체) | ✅ 지원 ([ESP](/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/) 헤더 + 페이로드만) | 외부 IP 헤더의 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 여부 |
| <strong><a href="/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/">NAT</a> 통과 (<a href="/studynote/03_network/07_network_layer_routing/384_nat_t_ipsec_nat_traversal_udp_4500/">NAT Traversal</a>)</strong> | ❌ 불가능 (IP 변조 시 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 깨짐) | ✅ 가능 ([NAT-T](/studynote/03_network/07_network_layer_routing/384_nat_t_ipsec_nat_traversal_udp_4500/), [UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 캡슐화 사용 시) | 공유기/[방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 통과 필수성 |
| <strong>IP 헤더 <a href="/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a> 범위</strong> | 출발/목적지 IP 등 고정 필드 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) | 외부 IP 헤더 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 안 함 | [스푸핑](/studynote/02_operating_system/10_security/598_spoofing/)에 대한 엄격한 방어 필요성 |
| <strong><a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a> 번호 (IP <a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a> 필드)</strong> | 51 | 50 | [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 예외 처리 시 |

현대 네트워크 설계에서 AH와 ESP의 생존을 가른 가장 큰 기술적 분기점인 '[NAT](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) 통과 가능성'을 시각화하면 다음과 같다.

```text
  +------------------------------------------------------------------+
  |                 NAT 환경에서의 AH와 ESP의 동작 차이 비교               |
  +------------------------------------------------------------------+
  |                                                                  |
  | [AH의 NAT 통과 실패 (인증 범위 충돌)]                                 |
  |  송신자 (10.0.0.2) ----> [ NAT 라우터 ] ----> 인터넷 ----> 수신자          |
  |  (AH: Src=10.0.0.2로 ICV 계산)    |(Src를 203.0.113.5로 변경)     |
  |                                   |                              |
  |  수신자 검증: 수신된 Src IP(203.0.113.5)로 ICV 재계산                 |
  |  결과: 원본 ICV(10.0.0.2 기반) ≠ 계산된 ICV(203.x 기반)              |
  |  💥 AH 무결성 검증 실패! 패킷 무조건 폐기 (Drop). NAT와 절대 공존 불가. |
  |                                                                  |
  | [ESP의 NAT 통과 성공 (NAT-T 적용 시)]                                 |
  |  송신자 (10.0.0.2) ----> [ NAT 라우터 ] ----> 인터넷 ----> 수신자          |
  |  (ESP: IP 헤더는 인증에서 제외됨) |(Src를 203.0.113.5로 변경)     |
  |                                   |                              |
  |  수신자 검증: ESP는 IP 헤더가 아닌 '페이로드'에 대해서만 인증 수행        |
  |  결과: IP가 변조되어도 페이로드 해시는 일치함                          |
  |  ✅ ESP 무결성 검증 성공! (IP 주소가 바뀌어도 통신 유지)                 |
  +------------------------------------------------------------------+
```

**[다이어그램 해설]** AH가 가진 가장 치명적인 아킬레스건은 바로 'IP 헤더 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)'이다. AH는 강력한 방어를 위해 출발지 IP 주소를 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)에 포함시킨다. 그런데 [NAT](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)(공유기) 장비를 지나면 필연적으로 출발지 사설 IP가 공인 IP로 변환(조작)된다. 수신자는 변경된 공인 IP를 바탕으로 해시(ICV)를 재계산하므로, 송신자가 사설 IP로 계산했던 원본 해시값과 무조건 불일치하게 된다. 즉, AH는 [NAT](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) 환경에서 모든 정상 패킷을 '조작된 공격 패킷'으로 오인하여 폐기한다. 반면 ESP는 외부 IP 헤더를 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 대상에서 제외하므로 [NAT](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) 환경에서도 [NAT-T](/studynote/03_network/07_network_layer_routing/384_nat_t_ipsec_nat_traversal_udp_4500/) 우회 기술을 통해 성공적으로 통신할 수 있다. 이로 인해 현대 인터넷에서 AH의 사용은 급감했다.

### 과목 융합 관점

- <strong><a href="/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/">네트워크 보안</a> (Network <a href="/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a>)</strong>: BGP나 OSPF와 같은 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 정보 교환 시, [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 테이블 내용이 기밀일 필요는 없으나 중간에 공격자가 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 정보를 위조하여 트래픽 방향을 트는 것 ([Routing](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) Blackhole, MITM)은 치명적이다. 이때 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 암호화 오버헤드 없이 강력한 출발지 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 제공하는 AH가 [OSPFv3](/studynote/03_network/07_network_layer_routing/362_ospfv3_ipv6_support/) 등에서 채택되곤 한다.
- <strong><a href="/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/">IPv6</a> 아키텍처</strong>: IPv6는 본질적으로 NAT가 필요 없을 정도로 주소 공간이 광활하므로 엔드 투 엔드([End-to-End](/studynote/03_network/08_transport_layer/401_transport_layer_role_end_to_end_multiplexing/)) 공인 IP 통신이 가능하다. IPv6의 확장 헤더 구조(Extension Header)에는 AH가 기본적으로 정의되어 있으며, [NAT](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) 충돌 문제가 없는 순수 [IPv6](/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/) 환경에서는 AH의 방어력이 다시금 빛을 발할 수 있다.

- **📢 섹션 요약 비유**: AH는 겉포장지(IP 헤더)까지 통째로 코팅해버리는 방식이라 배송 중 우체국이 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 스티커([NAT](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) 주소 변환)를 붙일 수 없게 만들어버리는 치명적 단점이 존재하는 것과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

1. <strong>시나리오 — 클라우드 <a href="/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/">VPC</a> 내부의 <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/">마이크로서비스</a> 간 <a href="/studynote/05_database/07_exam_summary/442_consistency_integrity/">무결성 보장</a></strong>: [NAT](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) 장비가 개입하지 않는 동일한 AWS [VPC](/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/) ([Virtual Private Cloud](/studynote/13_cloud_architecture/01_virtualization/028_vpc/)) 또는 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 사설망 내부에서, 수천 개의 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 간에 교환되는 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출이 위조되지 않았음을 가벼운 오버헤드로 증명해야 하는 상황. 아키텍트는 암호화 부하가 큰 [ESP](/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/) 대신, IP 헤더 [스푸핑](/studynote/02_operating_system/10_security/598_spoofing/)까지 막아주는 <strong><a href="/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/">AH</a> 기반의 수송 모드 <a href="/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/">IPSec</a> <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a></strong>을 내부에 배포하여 고성능 [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 구현할 수 있다.
2. <strong>시나리오 — <a href="/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/">BGP</a> <a href="/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a> 피어링 보안 <a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a></strong>: 서로 다른 통신 사업자([ISP](/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/)) 라우터 간에 [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 피어링을 맺을 때, 제3자가 [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 업데이트 메시지를 위조하여 트래픽을 가로채는 공격을 막아야 한다. 이때 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 정보 자체는 평문(Public)이므로 암호화가 필요 없다. 엔지니어는 라우터 간 [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)에 [MD5](/studynote/03_network/13_network_security_basics/668_md5_hash_collision_vulnerability/) [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)이나 <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/">IPSec</a> <a href="/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/">AH</a></strong>를 적용하여 패킷의 출발지와 내용 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 수학적으로 보증하는 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 세워야 한다.
3. <strong>시나리오 — <a href="/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/">IPSec</a> <a href="/studynote/03_network/07_network_layer_routing/384_nat_t_ipsec_nat_traversal_udp_4500/">NAT-T</a> 환경의 <a href="/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/">VPN</a> 구축 시도 중 장애</strong>: 주니어 엔지니어가 본사와 지사 간 VPN을 구성하며 보안을 극대화하겠다며 [ESP](/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/)+[AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) 조합 모드를 강제했다. 그런데 지사 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)([NAT](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/))을 통과하는 순간 모든 [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)이 드롭되는 장애가 발생했다. 시니어 아키텍트는 AH가 NAT를 통과할 수 없다는 설계적 한계를 짚어주고, [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 <strong><a href="/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/">ESP</a> 단독(<a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>+암호화) 터널 모드 + <a href="/studynote/03_network/07_network_layer_routing/384_nat_t_ipsec_nat_traversal_udp_4500/">NAT-T</a> 허용</strong>으로 즉시 롤백하여 통신을 복구한다.

AH가 제공하는 또 다른 핵심 기능인 '[재생 공격](/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/)([Replay Attack](/studynote/09_security/03_network_security/274_replay_attack/)) 방어 메커니즘'의 내부 윈도우 관리를 시각화하면, 수신 측의 정교한 시퀀스 넘버 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 로직을 알 수 있다.

```text
  +------------------------------------------------------------------+
  |                 AH의 재생 공격 방어 (Anti-Replay Window)               |
  +------------------------------------------------------------------+
  |                                                                  |
  |   [수신자의 Sliding Window (크기 W, 예: 64)]                        |
  |   --------------------> 시간 (Sequence Number 증가 방향)               |
  |                                                                  |
  |           (이미 받은 오래된 패킷)     (현재 수신 윈도우 범위)                  |
  |         ... 97, 98, 99, 100 | 101, 102, 103 ... 164 |           |
  |   [폐기 구역: 너무 늦음]        [검증 구역: 정상 수신 대기]   [미래 구역]  |
  |                             +-------- 윈도우 W -------+           |
  |                                     ^                            |
  |                           비트맵으로 수신 여부 체크 (1=수신, 0=미수신)   |
  |                                                                  |
  |   판단 1. Seq=95 수신 -> 윈도우 왼쪽(과거) -> 즉시 폐기 (Replay 공격)     |
  |   판단 2. Seq=102 수신 -> 윈도우 내부, 비트맵=1(이미 받음) -> 즉시 폐기    |
  |   판단 3. Seq=105 수신 -> 윈도우 내부, 비트맵=0 -> 정상 처리 후 비트맵=1로 |
  |   판단 4. Seq=166 수신 -> 윈도우 오른쪽(새로운 최신) -> 정상 처리 후 윈도우 |
  |                          전체를 오른쪽으로 슬라이딩 (103~166으로 갱신)    |
  +------------------------------------------------------------------+
```

**[다이어그램 해설]** [재생 공격](/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/)([Replay Attack](/studynote/09_security/03_network_security/274_replay_attack/))은 해커가 정상적인 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)이 완료된 과거의 패킷(예: '계좌로 100만 원 송금하라')을 복사해두었다가 나중에 다시 전송하는 해킹 기법이다. AH는 모든 패킷에 순차적으로 증가하는 Sequence Number(Seq)를 부여한다. 수신자는 보통 64 패킷 크기의 '슬라이딩 윈도우' 비트맵을 유지한다. 만약 해커가 과거 패킷을 다시 보내면, 그 패킷의 Seq는 이미 윈도우의 왼쪽(너무 낡음)에 있거나, 윈도우 내부에 있더라도 이미 수신 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)(비트맵=1)이 된 상태이므로 즉각 폐기된다. 이 정교한 윈도우 메커니즘을 통해 네트워크 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)으로 인한 약간의 순서 뒤바뀜(Out-of-order)은 허용하면서도 악의적인 [재생 공격](/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/)은 완벽히 차단한다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **기술적**: [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)해야 할 통신 경로 상에 [NAT](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)(공유기)나 PAT 장비가 존재하는가? (존재한다면 [AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) 사용 불가, [ESP](/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/) 도입) 내부망에서 출발지 IP 위장 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 필수적인가?
- **운영·보안적**: AH만 적용할 경우 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 평문으로 스니핑될 위험은 감수할 수 있는가? ESP가 제공하는 '[인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)' 기능만으로도 충분하지 않고 반드시 IP 헤더 고정 필드까지 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)해야 하는 강력한 근거가 있는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong>외부 인터넷 구간의 <a href="/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/">VPN</a> 구성 시 <a href="/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/">AH</a> 강제 사용</strong>: 오늘날 퍼블릭 인터넷은 100% [NAT](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) 라우터를 경유한다고 보아도 무방하다. 이곳에 [AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) 터널/수송 모드를 고집하는 것은 네트워크 아키텍처에 대한 무지의 소치이며 즉각적인 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 단절을 낳는다.
- <strong>AH와 ESP를 무조건 중복 적용 (<a href="/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/">AH</a>+<a href="/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/">ESP</a>)</strong>: [ESP](/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/) 자체에도 [HMAC](/studynote/03_network/13_network_security_basics/674_hmac_hash_based_mac_ipsec/) 기반의 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([Authentication](/studynote/02_operating_system/10_security/604_authentication_factors/)) 기능이 포함되어 있다. 극도로 민감한 망이 아닌 일반 기업망에서 AH와 ESP를 동시에 이중으로 씌우는 것은 불필요한 해시 연산 오버헤드와 패킷 크기(MTU) 증가만 초래하는 전형적인 과잉 설계다.

- **📢 섹션 요약 비유**: 아무리 튼튼한 금고([AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/))라도, 택배 기사가 배송지를 바꿔 적어야만 전달할 수 있는 복잡한 현대의 택배 시스템([NAT](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) 환경)에서는 억지로 반송되어버리는 너무 고지식한 보안 장치와 같습니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | 최적화 전 | 최적화 후 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | [ESP](/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/) (암호화+[인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)) 사용 시 높은 CPU 오버헤드 | 내부망에 [AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) ([인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 전용) 전면 적용 | 암호화 복호화 오버헤드 제거로 <strong><a href="/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a>(TPS) 40% 이상 향상</strong> |
| **정량** | [재생 공격](/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/) 방어 부재 | [AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) Sequence Number 윈도우 적용 | 동일 패킷 반복 전송을 통한 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 고갈(DDoS) 패킷 **100% 차단** |
| **정성** | IP 위장 공격 ([Spoofing](/studynote/02_operating_system/10_security/598_spoofing/)) 속수무책 | 전체 IP 고정 필드 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 출발지 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [신뢰도](/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 확보 및 내부자 위장 침투 (Lateral Movement) 방어 |

### 미래 전망
- <strong><a href="/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/">IPv6</a> 확산에 따른 재부상</strong>: 전 세계적으로 IPv4가 고갈되고 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 기기 중심의 [IPv6](/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/) 전환이 가속화되면서 NAT의 필요성이 사라지는 추세다. [End-to-End](/studynote/03_network/08_transport_layer/401_transport_layer_role_end_to_end_multiplexing/) [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)이 투명해지는 순수 [IPv6](/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/) 환경에서는 AH의 [NAT](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) 충돌 단점이 사라지므로, 오버헤드가 적은 경량 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)로서의 가치가 재조명될 가능성이 높다.
- <strong><a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/417_hardware_accelerator/">하드웨어 가속기</a>(<a href="/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/">NIC</a>) 탑재</strong>: 최신 스마트 [NIC](/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/)(Network Interface Card)와 [DPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/436_dpu/)([Data Processing Unit](/studynote/06_ict_convergence/03_cloud_infrastructure/229_dpu_ipu_infrastructure_accelerator_offloading/)) 장비들은 AH와 ESP의 [HMAC](/studynote/03_network/13_network_security_basics/674_hmac_hash_based_mac_ipsec/) 해시 연산을 CPU 대신 하드웨어 계층에서 [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)([Offloading](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/))하여 와이어 스피드(Wire-speed) 100Gbps 환경에서도 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 없는 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 수행하도록 진화하고 있다.

### 참고 표준
- **RFC 4302**: IP [Authentication Header](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) ([AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 표준 규격서)
- **RFC 2104**: [HMAC](/studynote/03_network/13_network_security_basics/674_hmac_hash_based_mac_ipsec/): Keyed-Hashing for Message [Authentication](/studynote/02_operating_system/10_security/604_authentication_factors/)
- **IEEE 802.1AE (MACsec)**: L2 계층의 통신 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 표준 (네트워크 하위 계층에서 AH와 유사한 역할)

현대 [네트워크 보안](/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/)에서 AH는 암호화를 제공하는 ESP의 그림자에 가려진 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)처럼 보일 수 있다. 그러나 '[기밀성](/studynote/09_security/01_intro_principles/002_confidentiality/)'과 '[무결성](/studynote/09_security/01_intro_principles/003_integrity/)/[인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)'을 아키텍처 관점에서 철저히 분리하여 설계한 IPSec의 디자인 철학을 가장 잘 보여주는 핵심 구성 요소다.

[IPSec](/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/) 내에서 AH와 ESP가 차지하는 [보안 기능](/studynote/04_software_engineering/11_testing_validation/895_security_features_design/) 제공의 커버리지를 벤 다이어그램과 매트릭스로 요약하면, 두 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이 어떻게 보완적 역할을 하는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 수 있다.

```text
  +------------------------------------------------------------------+
  |              IPSec 보안 기능 커버리지 (AH vs ESP)                   |
  +------------------------------------------------------------------+
  |                                                                  |
  |                  [ IPSec 보안 프레임워크 (RFC 4301) ]                 |
  |                                                                  |
  |  +------------------+  +--------------------------------------+  |
  |  |        AH        |  |                 ESP                  |  |
  |  | +--------------+ |  | +--------------+ +-----------------+ |  |
  |  | |무결성/인증 보장| |  | |기밀성(암호화)보장| | 페이로드 무결성/| |  |
  |  | |(IP헤더 + 페이로드| |  | |(순수 데이터 은닉)| | 인증 보장       | |  |
  |  | |  강력한 스푸핑 방어| |  | |  NAT 완벽 통과  | | (IP헤더 제외)   | |  |
  |  | +--------------+ |  | +--------------+ +-----------------+ |  |
  |  |    [재생공격 방어]   |  |             [재생공격 방어]              |  |
  |  +------------------+  +--------------------------------------+  |
  |                                                                  |
  |  현대의 결론: ESP의 [인증 보장] 기능 발전과 NAT 환경의 고착화로 인해,         |
  |             대부분의 방화벽/VPN 벤더는 ESP를 단독으로 사용하는 것을 표준으로 |
  |             삼고, AH는 특수 목적망(IPv6, BGP 등)에서만 제한적으로 활용한다.|
  +------------------------------------------------------------------+
```

**[다이어그램 해설]** AH는 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)([Integrity](/studynote/09_security/01_intro_principles/003_integrity/))과 출발지 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([Authentication](/studynote/02_operating_system/10_security/604_authentication_factors/))에 집중하여 IP 헤더까지 강력하게 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)한다. ESP는 본래 암호화([Confidentiality](/studynote/09_security/01_intro_principles/002_confidentiality/))를 위해 탄생했으나, 진화를 거듭하며 자체적인 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)(Auth Trailer) 기능까지 추가로 장착하게 되었다. 비록 ESP의 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)이 외부 IP 헤더를 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)하지는 못하지만, 페이로드를 완벽히 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)하고 NAT를 무사히 통과한다는 엄청난 실무적 장점이 있다. 그 결과 현대 실무에서는 굳이 [AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/)+ESP를 같이 쓰지 않고, [ESP](/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/) 단독 사용만으로 [기밀성](/studynote/09_security/01_intro_principles/002_confidentiality/), 페이로드 [무결성](/studynote/09_security/01_intro_principles/003_integrity/), [재생 공격](/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/) 방어, [NAT](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) 통과라는 네 마리 토끼를 모두 잡는 아키텍처가 시장의 표준(De facto standard)이 되었다.

- **📢 섹션 요약 비유**: AH는 내용물을 투명하게 유지하되 위조를 절대 용납하지 않는 엄격한 유리병과 같아서, 안의 내용물을 감추고 유연하게 배송해야 하는 현대의 불투명한 택배 시장([ESP](/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/))에 자리를 내주었지만, 그 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 철학만큼은 여전히 살아 숨 쉬고 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [IPSec](/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/) 터널/수송 모드 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 정의 (Definition) | 용어의 시작점을 분명하게 만든다. |
| 비교 (Comparison) | 헷갈리는 개념의 경계를 드러낸다. |
| [ESP](/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: IPSec 터널/수송 모드]
    |
    v
[현재 개념: AH]
    |
    +---> [확장 A: ESP]
    +---> [확장 B: 컨텍스트 기반 용어 해석]
```

AH는 [IPSec](/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/) 터널/수송 모드에서 출발해 현재 메커니즘을 정교화하고, 이후 ESP와 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 기반 용어 해석 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 편지를 보낼 때, 친구와 나만 아는 '마법의 비밀 도장([AH](/studynote/03_network/07_network_layer_routing/381_ah_authentication_header_integrity_auth/))'을 편지 봉투와 내용물에 꾹 찍어 보내는 규칙을 만들었어요.
2. 중간에 나쁜 악당이 편지를 몰래 가로채서 글자를 지우거나 보낸 사람 이름을 자기 이름으로 고치면, 마법의 도장이 쩍 갈라지면서 깨져버려요.
3. 친구는 도장이 깨진 편지를 받으면 "아하, 누군가 장난을 쳤구나!" 하고 바로 쓰레기통에 버릴 수 있어서, 절대 가짜 편지에 속지 않게 되는 원리랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 1101 / 1120

<- **이전**: [979. IPSec 터널/수송 모드](/studynote/03_network/19_frequent_topics_terms/979_ipsec_tunnel_transport_mode/)
**다음**: [981. ESP (Encapsulating Security Payload)](/studynote/03_network/19_frequent_topics_terms/981_esp_encapsulating_security_payload/) ->

---
