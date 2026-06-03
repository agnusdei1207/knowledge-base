+++
title = "538. SSH (Secure Shell) 포트 22 / Telnet (원격 접속) 포트 23 비교"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SSH [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 22 / Telnet [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 23…는 이름 해석과 네트워크 관리에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: SSH [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 22 / Telnet [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 23…를 이해하면 가시성과 관리 자동화 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 원격지에 물리적으로 떨어져 있는 서버나 네트워크 장비(라우터, [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/))의 콘솔 화면(CLI 터미널)에 접속하여 명령어를 실행할 수 있게 해주는 애플리케이션 계층(L7)의 통신 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이다. Telnet은 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 23번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를, SSH(Secure [Shell](/knowledge-base/studynote/02_operating_system/01_overview_architecture/044_shell/))는 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 22번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 기본으로 사용한다.
- **필요성**: 수백 대의 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 서버를 관리하기 위해 엔지니어가 일일이 키보드와 모니터를 들고 이동할 수는 없다. 따라서 네트워크를 통해 터미널 환경을 가져오는 원격 접속 기술은 IT 인프라 관리의 숨쉬는 공기와 같다. 하지만 네트워크 회선은 언제나 감청당할 수 있는 공개된 도로와 같으므로 통신의 안전성([기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/), [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)) 보장 여부가 가장 중요한 선택 기준이 된다.
- **등장 배경**: ① [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 아파넷(ARPANET) 시절 통신 자체에 목적을 둔 평문 기반 Telnet 탄생 → ② 네트워크 대중화로 인한 악의적 [패킷 스니핑](/knowledge-base/studynote/09_security/03_network_security/272_packet_sniffing/)(Sniffing)에 의한 관리자 탈취 사고 빈발 → ③ 1995년 암호화와 키 교환 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 태생적으로 내장한 SSH [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 등장 및 보안 대체.

```text
┌─────────────────────────────────────────────────────────────┐
│             Telnet과 SSH의 치명적 차이 시각화 (스니핑 위협)           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [클라이언트]                                  [서버]            │
│       │                                         │            │
│       │── "ID: root" ─────────(평문)─────────▶│            │
│       │── "PW: admin123" ─────(평문)─────────▶│ [Telnet]   │
│       │                                         │            │
│      ※ 악의적 해커가 Wireshark로 중간에서 훔쳐보면 글자가 그대로 보임! │
│                                                             │
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
│                                                             │
│       │── "e1x$#k@9z..." ─────(AES 암호문)─────▶│            │
│       │── "m9*qL!2p..."  ─────(AES 암호문)─────▶│ [SSH]      │
│       │                                         │            │
│      ※ 해커가 패킷을 가로채도 강력한 암호 덩어리일 뿐 해독 불가능.        │
└─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 그림은 두 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이 근본적으로 왜 세대 교체되었는지를 극명하게 보여준다. Telnet [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)은 암호화 캡슐화 로직이 전무하여 사용자가 치는 키보드 입력 값(아이디, 패스워드 포함)이 [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 단위로 네트워크 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)와 라우터를 날 것 그대로 통과한다. 내부 망이라 할지라도 [ARP](/knowledge-base/studynote/03_network/06_network_layer_ip/312_arp_address_resolution_protocol_ip_to_mac/) [스푸핑](/knowledge-base/studynote/02_operating_system/10_security/598_spoofing/)([Spoofing](/knowledge-base/studynote/02_operating_system/10_security/598_spoofing/)) 기법을 쓴 공격자에게 10초면 탈취당한다. 반면 SSH는 Diffie-Hellman 방식 등으로 동적 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 키를 안전하게 교환한 뒤 통신 전체를 [AES](/knowledge-base/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/) 등 대칭키 암호화로 감싸기 때문에, 중간 과정에서 패킷이 유출되더라도 통신의 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)([Confidentiality](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/))이 완벽히 보호된다.

- **📢 섹션 요약 비유**: Telnet은 은행 비밀번호를 엽서에 적어서 우체통에 넣는 것이고, SSH는 비밀번호를 풀 수 없는 강철 금고에 넣은 뒤 열쇠 구멍조차 없는 장갑차로 배달하는 것과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 요소명 | 역할 | 내부 원리 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **전송 계층 (Transport Layer)** | 보안 채널 확립 | 서버 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), [암호화 알고리즘](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/504_cryptography_algorithms_aes_rsa_sha/) 협상, [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 키 교환(KEX) | [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/), Diffie-Hellman, [AES](/knowledge-base/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/), [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) | 장갑차 길 뚫기 |
| **[사용자 인증](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/) (User Auth Layer)** | 클라이언트의 신원 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 패스워드 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 또는 비대칭 공개키(Public [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) 서명 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/), Ed25519 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)키 | 탑승자 신분증 검사 |
| **연결 계층 (Connection Layer)** | 단일 암호화 채널의 [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) | 암호화된 터널 위에서 여러 개의 논리적 채널(터미널, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)전송, [포트 포워딩](/knowledge-base/studynote/03_network/14_network_security_threats/736_port_forwarding_jump_station_bastion_host/)) 통신 지원 | 멀티플렉싱([Multiplexing](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)) | 장갑차 내부 다용도 칸막이 |
| **대칭키 ([Session Key](/knowledge-base/studynote/09_security/03_network_security/140_session_key/))** | 통신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 고속 암/복호화 | [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)마다 일회용으로 생성되며 트래픽 캡슐화에 사용 | [AES](/knowledge-base/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/)-GCM, ChaCha20 | 일회용 금고 비밀번호 |
| **공개키 (Public/Private [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))** | 서버 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 및 비밀번호 없는 로그인 | 서버가 진짜인지 증명하고, 클라이언트가 합법적 사용자인지 증명 서명 | `known_hosts`, `authorized_keys` | 자물쇠와 고유 열쇠 |

### SSH 접속 핸드셰이크(Handshake) 메커니즘

SSH 통신은 단순한 [TCP 3-Way Handshake](/knowledge-base/studynote/03_network/08_transport_layer/416_tcp_3_way_handshake_connection_setup/) 이후에 매우 복잡하고 철저한 [암호학](/knowledge-base/studynote/03_network/13_network_security_basics/652_cryptography_concept_encryption_decryption/)적 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)(Handshake)을 통해 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)을 생성한다. 이 과정은 보안의 핵심 3요소인 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)(암호화), [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)(변조 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)), [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)(진짜 서버/사용자 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/))을 모두 달성한다.

```text
┌───────────────────────────────────────────────────────────────┐
│               SSH v2 보안 세션 초기화 흐름도 (Handshake)            │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│   [Client]                                       [Server]     │
│      │               1. TCP 연결 확립                 │         │
│      │◀═════════════ (3-Way Handshake) ════════════▶│         │
│      │                                                │         │
│      │               2. 버전 및 암호군 협상             │         │
│      │───────────── 지원 가능한 알고리즘 목록 ─────────▶│         │
│      │◀──────────── 선택된 알고리즘 확정 ──────────────│         │
│      │                                                │         │
│      │               3. 키 교환 (KEX) 및 서버 인증       │         │
│      │◀──────────── 서버의 공개키(Public Key) 전송 ────│         │
│      │                                                │         │
│  ※ Client는 known_hosts 파일에서 이 서버의 공개키가 맞는지 1차 검증! │
│      │                                                │         │
│      │◀═════════════ Diffie-Hellman 키 교환 ══════════▶│         │
│  ※ 공유 비밀키(Shared Secret) 생성 ─▶ 대칭 세션키(Session Key) 추출 │
│                                                               │
│      │               4. 보안 채널 확립 및 사용자 인증      │         │
│      │=====[이후 통신은 세션키로 AES-256 전체 암호화됨]======│         │
│      │───── (암호화) 비대칭키 서명 데이터 전송(로그인) ──▶│         │
│      │◀──── (암호화) 인증 성공! 터미널 쉘(Shell) 제공 ───│         │
└───────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 흐름도의 가장 핵심적인 부분은 3번 단계인 "서버 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)과 키 교환"이다. 클라이언트는 서버에 접속할 때 서버가 가짜(해커가 만든 위장 서버)가 아닌지 서버의 공개키를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)(`known_hosts` 대조)한다. 만약 처음 접속하는 서버라면 "이 서버를 신뢰할 것인가?"(fingerprint [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/))를 묻는다. 이후 Diffie-Hellman 수학적 마법을 통해 네트워크로 비밀번호를 교환하지 않고도 양쪽이 동일한 대칭키([Session Key](/knowledge-base/studynote/09_security/03_network_security/140_session_key/))를 나누어 가진다. 그 다음 4번 단계부터 이루어지는 클라이언트 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)(비밀번호 혹은 `.ssh/id_rsa` 키 로그인)은 이 강력하게 암호화된 터널 안에서 이루어지므로 외부 해커는 절대 내용을 알 수 없다.

- **📢 섹션 요약 비유**: SSH [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 22 / Telnet [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 23…의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

| 비교 기준 | Telnet (Telecommunication Network) | SSH (Secure [Shell](/knowledge-base/studynote/02_operating_system/01_overview_architecture/044_shell/)) |
|:---|:---|:---|
| **통신 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)** | [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 23번 | [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 22번 |
| **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)** | 평문 (Cleartext) 전송 - 패스워드 탈취 매우 쉬움 | 암호화 전송 ([AES](/knowledge-base/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/), ChaCha20 등) - 강력한 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) 보장 |
| **[사용자 인증](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/) 방식** | 오직 계정 ID / Password 기반 | 패스워드 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) + 비대칭 공개키(Public [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) 쌍 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) (권장) |
| **[무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)** | 없음 (중간자 패킷 변조 방어 불가) | [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) ([Message Authentication Code](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/))을 통한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변조/손실 완벽 감지 |
| **기능 확장성** | 단순히 원격 텍스트 쉘([Shell](/knowledge-base/studynote/02_operating_system/01_overview_architecture/044_shell/)) 접속만 지원 | [SFTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/485_sftp_ssh_file_transfer/)(보안 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)전송), [SCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/747_scp/), X11 포워딩, 로컬/원격 [포트 포워딩](/knowledge-base/studynote/03_network/14_network_security_threats/736_port_forwarding_jump_station_bastion_host/)([터널링](/knowledge-base/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/)) 제공 |
| **운영 표준** | 보안 규정(ISO27001 등)에서 명시적 사용 금지 조항 | 현대 모든 클라우드, 리눅스 인프라 접속의 절대적 필수 표준 규격 |

Telnet은 인터넷에 '나쁜 짓을 하는 해커'가 없던 순수한 연구자들의 시대에 만들어진 성선설적 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이다. 반면 SSH는 중간에서 누군가 패킷을 복사하고 변조할 것이라는 성악설(Zero-Trust 관점)을 바탕으로 철저한 [암호학](/knowledge-base/studynote/03_network/13_network_security_basics/652_cryptography_concept_encryption_decryption/) 방어벽을 둘러친 현대적 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이다. 따라서 기능 비교를 넘어, 정보보안 심사 시 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 관리 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 Telnet이 열려있으면 즉각적인 '치명적 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)(Critical)' 사유가 된다.

```text
┌───────────────────────────────────────────────────────────────┐
│                 SSH의 기능적 확장성 (포트 포워딩 터널링)             │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│   [해커 공격 망 / 비신뢰 구간]                                      │
│                                                               │
│   로컬 PC (L)                  방화벽               사내 망 DB (D) │
│   [Port 8080] ====================|==============▶ [Port 3306]  │
│                                   |                           │
│   (직접 접속 시도 시) ─────── 차단 (Drop)! ────────────────│
│                                                               │
│   [SSH 포트 포워딩(터널링) 매직]                                      │
│                                   |          [SSH Server(S)]  │
│   [Port 8080] <---(암호화 터널)---|------------> [Port 22]    │
│                                   |                 │         │
│                                   |            (내부 로컬 포워드) │
│                                   |                 ▼         │
│                                   |             [Port 3306]   │
│                                                               │
│  명령어: ssh -L 8080:DB_IP:3306 user@SSH_Server_IP            │
│  => 클라이언트가 로컬 8080 포트로 쏘는 트래픽이 SSH 암호화 파이프를 타고 │
│     방화벽을 무사히 넘어가 목적지 DB에 도달한다!                       │
└───────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 다이어그램은 SSH가 단순한 콘솔 텍스트를 전달하는 용도에서 벗어나, [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)을 뚫는 강력한 보안 우회 터널([Tunneling](/knowledge-base/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/)) 장비로 쓰이는 '로컬 [포트 포워딩](/knowledge-base/studynote/03_network/14_network_security_threats/736_port_forwarding_jump_station_bastion_host/)(Local [Port](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) Forwarding)'의 개념을 보여준다. 외부에서 사내 망의 DB 서버(3306 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))로 직접 붙으려 하면 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)에 막힌다. 이때 허용된 유일한 문인 SSH 서버(22번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))와 튼튼한 암호화 터널을 뚫고, 내 로컬 PC의 8080 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 입력되는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 이 터널을 거쳐 SSH 서버가 대신 DB로 쏴주는 원리다. SSH는 이러한 통신 [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)([Multiplexing](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)) 능력을 통해 VPN을 대체하는 경량화된 보안 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 인프라 역할을 수행한다.

- **📢 섹션 요약 비유**: Telnet이 오직 말소리만 전하는 낡은 종이컵 전화기라면, SSH는 도청이 불가능한 전용 군사 핫라인일 뿐만 아니라 그 선을 타고 일급 기밀문서([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 전송)와 비밀 요원([포트 포워딩](/knowledge-base/studynote/03_network/14_network_security_threats/736_port_forwarding_jump_station_bastion_host/))까지 실어 나를 수 있는 방탄 비밀 지하 통로와 같습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

1. **상황**: 스타트업에서 AWS 퍼블릭 클라우드에 수십 대의 Linux 가상 머신(EC2)을 구축했다. 편의성을 위해 계정과 비밀번호를 통해 SSH 접근을 허용해 두었으나, 전 세계의 [봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/)([Botnet](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/))들로부터 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 22번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 겨냥한 무차별 대입 공격(Brute-Force Attack) 및 사전 공격(Dictionary Attack) 로그가 하루에 수만 건씩 발생하고 시스템 CPU 리소스를 낭비하고 있다.
2. **원인**: 기본 SSH [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 외부(0.0.0.0/0)에 개방한 채로 암호 기반 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)(PasswordAuthentication)을 허용하면 [봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/)의 주요 먹잇감이 된다. 암호는 길이나 복잡성에 한계가 있어 해킹 노출 위험이 높다.
3. **의사결정 및 조치**: 아키텍트는 즉시 3단계 보안 강화를 실행해야 한다.
   - **비대칭키 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 강제화**: `sshd_config`에서 `PasswordAuthentication no`로 설정하여 암호 입력을 원천 금지하고, 로컬 PC에서 생성한 `ed25519` 공개키 방식을 통해서만 접속하도록 아키텍처를 변경한다.
   - **Fail2Ban 적용**: 수 차례 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)에 실패한 IP는 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)(iptables/firewalld) 레벨에서 즉각 블록(Block)하도록 자동화된 침입 차단 데몬을 올린다.
   - **[포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 및 접근 제어**: SSH 기본 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 22번에서 무작위 높은 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)(예: 49222 등)로 변경(보안 스캐닝 노이즈 대폭 감소)하고, 보안 그룹([Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Group) 정책을 통해 회사의 지정된 공인 IP([Bastion Host](/knowledge-base/studynote/09_security/05_web_app_security/218_bastion_host_dmz_security/))에서만 SSH 통신을 허용하도록 네트워크 룰을 바꾼다.

- **보안 점검 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) (네트워크 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)/라우터)**: 아직도 구형 사내 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 관리 접근 시 Telnet [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)(23)가 열려 있는가? `transport input ssh` 명령어로 Telnet 접근 라우팅을 차단하고 SSH [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 2(v2)만 허용하도록 하드닝(Hardening) 조치를 취했는가?
- **SSH 키 관리 체계**: 회사 퇴사자 발생 시, 인프라의 `~/.ssh/authorized_keys` [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에서 퇴사자의 공개키를 즉시 회수 및 삭제할 수 있는 중앙 집중형 키 관리 시스템(예: HashiCorp [Vault](/knowledge-base/studynote/09_security/11_iam_access_control/567_vault/) 또는 AWS Systems Manager [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) Manager)이 도입되어 있는가? (단순 키 관리는 보안 구멍을 유발한다).
- **[안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) (치명적 오류)**: GitHub이나 공용 소스코드 저장소에 자신의 개인키(Private [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/), `id_rsa` [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))를 실수로 커밋(Commit)하여 올리는 행위. 이는 클라우드 인프라가 통째로 털리는 가장 흔하면서 치명적인 사고다. 개인키는 "내 영혼이자 도장"이므로 절대 로컬 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 외부로 유출해서는 안 된다.

- **📢 섹션 요약 비유**: 비밀번호 방식이 집 열쇠를 여러 명에게 복사해주고 혹시 털릴까 밤잠을 설치는 것이라면, SSH 공개키 방식은 들어올 수 있는 사람의 지문(공개키)만 집 자물쇠에 등록해두고, 진짜 지문을 가진 손가락(개인키)은 절대 집 밖에 빌려주지 않는 철벽 방어 시스템과 같습니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | Telnet 및 패스워드 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 환경 | SSH 및 공개키 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 적용 | 개선 효과 |
|:---|:---|:---|:---|
| **정량 ([보안성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))** | 스니핑에 의한 탈취율 100%, Brute-Force 방어 0% | 128비트 이상 강력 대칭키 통신, 무차별 대입 공격 무력화 | 계정 정보 평문 유출 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) **0% 완전 차단** |
| **정량 (생산성)** | 수동 비밀번호 입력 필요 (서버 100대 관리 시 수백 분 소요) | SSH [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) 기반 로그인으로 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 생략 패스 (비밀번호 없는 로그인) | [Ansible](/knowledge-base/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/) 등 인프라 자동화 도구 연동 **100% 자동화 효율** |
| **정성 (규제 준수)** | [ISMS](/knowledge-base/studynote/09_security/17_framework_compliance/836_iso_27001_isms/), PCI-DSS 보안 심사 시 부적합 및 페널티 부여 | 필수 보안 규정 완벽 부합 | 기업 컴플라이언스([Compliance](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/058_it_compliance_sox_basel_gdpr_isms/)) 심사 통과 및 대외 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 제고 |

### 미래 전망 및 진화 방향
- **[양자 내성 암호](/knowledge-base/studynote/14_data_engineering/04_mlops/183_post_quantum_cryptography_key_transition/)([PQC](/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/)) 기반 SSH**: 다가오는 [양자 컴퓨터](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/) 시대에는 현재 SSH 핸드셰이크에 주로 쓰이는 [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/) 및 [ECC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/)([타원곡선](/knowledge-base/studynote/09_security/03_network_security/120_elliptic_curve_equation/)) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 쇼어 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)(Shor's [algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))에 의해 수학적으로 깨질 위험(Store Now, Decrypt Later)이 있다. 따라서 최신 OpenSSH [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)에서는 [양자 내성 암호](/knowledge-base/studynote/14_data_engineering/04_mlops/183_post_quantum_cryptography_key_transition/)인 NTRU Prime 등을 기존 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)과 하이브리드 형태로 섞어서 키를 교환하는 포스트 퀀텀(Post-Quantum) 대응 업데이트가 활발히 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중이다.
- **Zero-Trust와 [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) Manager 구조로의 패러다임 전환**: 앞으로는 22번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 자체를 인터넷에 아예 열지 않는 방향으로 진화하고 있다. 클라우드 사업자(AWS [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) Manager 등)는 SSM 에이전트를 통해 아웃바운드 [HTTPS](/knowledge-base/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/)(443 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)) [터널링](/knowledge-base/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/)만을 이용해 브라우저 위에서 가상 쉘을 띄워주는 방식으로 발전시켜, 서버에 접근하는 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 구멍 자체를 지워버리는 궁극적 [제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)(Zero-Trust) 모델을 지향하고 있다.

### 참고 표준
- **RFC 4251 ~ 4254**: SSH-2 (Secure [Shell](/knowledge-base/studynote/02_operating_system/01_overview_architecture/044_shell/) version 2) 핵심 아키텍처 및 전송/[인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)/연결 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 표준
- **RFC 854**: Telnet [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) [Specification](/knowledge-base/studynote/04_software_engineering/03_design_architecture/148_requirements_specification_formal_informal/) (가장 오래된 평문 규격)

통신 인프라 관리의 생명줄인 원격 쉘 접속은 결국 '편리함'과 '보안'의 줄다리기다. SSH는 [암호학](/knowledge-base/studynote/03_network/13_network_security_basics/652_cryptography_concept_encryption_decryption/)을 깊이 숨기고 편의성을 극대화한 현대 인프라의 가장 위대한 걸작이며, 자동화 시대([IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/))를 지탱하는 보이지 않는 고속 철로와 같다.

- **📢 섹션 요약 비유**: 투명한 유리관을 통해 비밀을 소리쳐 전달하던 Telnet 시대는 끝났습니다. 이제는 아무리 강력한 도둑(해커, 양자컴퓨터)이 와도 부술 수 없는 콘크리트 암호 파이프라인(SSH) 위에서, 전 세계의 수백만 대의 서버들이 자동화 로봇들의 지휘를 받으며 안전하게 관리되는 시대로 진화했습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [SNTP](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/537_sntp_ptp_precision_time_protocol/) / PTP ([Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) [Ti](/knowledge-base/studynote/03_network/14_network_security_threats/746_ti_threat_intelligence_ioc_stix_taxii/)… | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) ([Domain Name System](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/)) | 이름과 주소를 연결해 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 접근성을 만든다. |
| 모니터링 (Monitoring) | 장애 징후를 조기에 발견하기 위한 기초다. |
| [NetFlow](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/) / sFlow 트래픽 흐름 모… | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: SNTP / PTP (Precision Ti…]
    │
    ▼
[현재 개념: SSH 포트 22 / Telnet 포트 23…]
    │
    ├──▶ [확장 A: NetFlow / sFlow 트래픽 흐름 모…]
    └──▶ [확장 B: 자율 운영 네트워크]
```

SSH [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 22 / Telnet [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 23…는 [SNTP](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/537_sntp_ptp_precision_time_protocol/) / PTP ([Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) [Ti](/knowledge-base/studynote/03_network/14_network_security_threats/746_ti_threat_intelligence_ioc_stix_taxii/)…에서 출발해 현재 메커니즘을 정교화하고, 이후 [NetFlow](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/) / sFlow 트래픽 흐름 모…와 자율 운영 네트워크 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 먼 옛날, 멀리 떨어진 컴퓨터와 통신하는 텔넷(Telnet)은 비밀번호를 엽서에 그냥 적어 보내는 것과 같아서 나쁜 아저씨들이 길목에서 쉽게 훔쳐볼 수 있었어요.
2. 하지만 SSH(Secure [Shell](/knowledge-base/studynote/02_operating_system/01_overview_architecture/044_shell/))는 누구도 열 수 없는 두꺼운 철제 금고에 비밀번호를 넣고, 열쇠구멍 모양도 그때그때 바뀌는 최첨단 자물쇠를 채워서 배달해요.
3. 그래서 오늘날 전 세계의 컴퓨터 엔지니어들은 이 안전한 장갑차(SSH) 통로를 이용해서, 해커들이 득실거리는 위험한 인터넷 바다 위에서도 수만 대의 컴퓨터들을 마음 놓고 척척 조종한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 659 / 1120

← **이전**: [537. SNTP (Simple NTP) / PTP (Precision Time Protocol, IEEE 1588](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/537_sntp_ptp_precision_time_protocol/)
**다음**: [539. NetFlow (Cisco) / sFlow 트래픽 흐름 모니터링 분석 프로토콜](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/) →

---
