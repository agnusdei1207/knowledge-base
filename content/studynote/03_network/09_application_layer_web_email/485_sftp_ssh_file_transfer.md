+++
title = "485. SFTP (SSH FTP)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SFTP는 응용 계층과 웹/메일에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: SFTP를 이해하면 응답 시간과 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: SFTP([SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) [File Transfer Protocol](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/))는 네트워크를 통해 클라이언트와 서버 간에 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 안전하게 복사, 전송, 관리하기 위한 네트워크 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이다. 구조적으로 [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 확장(Extension) 하위 시스템으로 구동되며, [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 터널이 뚫어놓은 안전한 암호화 고속도로 위를 달리는 화물 열차와 같다.

- **필요성**: 2000년대 이후 해커들의 스니핑(Sniffing) 기술 발전으로 고전 FTP의 평문 아이디/패스워드 전송은 기업 보안의 시한폭탄이 되었다. 설상가상으로 구형 FTP는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 보내기 위해 2개의 연결(제어+[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))과 복잡한 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 규칙(Passive 랜덤 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))을 강요해 인프라 관리자들을 분노케 했다. "[방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)에 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)는 딱 1개(22번)만 열고, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인부터 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 덩어리까지 하나의 강력한 암호화 터널 안에 모두 밀어 넣어버릴 수 없을까?"라는 엔터프라이즈의 보안/운영적 갈증이 SFTP의 완벽한 대승을 이끌었다.

- **💡 비유**: <strong>고전 <a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/">FTP</a></strong>가 물건 내용물(평문)이 투명한 비닐에 담겨 있고, 대화를 위한 오토바이([포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 21)와 짐을 싣는 대형 트럭([포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 20)이 따로따로 이동하는 복잡한 수송 작전이라면, <strong>SFTP</strong>는 절대 뚫리지 않는 하나의 거대한 <strong>'장갑 열차(<a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/">SSH</a> 22번 <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a> 터널)'</strong>를 깔아두고, 그 안에 기관사([명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/))와 수백 톤의 화물칸([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 전부 쑤셔 넣어 한 방에 안전하게 수송하는 완벽한 단일 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 시스템입니다.

- **등장 배경**:
  1. <strong><a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/">FTP</a> 보안의 파탄</strong>: 평문 FTP의 대안으로 나온 [FTPS](/knowledge-base/studynote/03_network/09_application_layer_web_email/486_ftps_ftp_over_ssl_tls/)([FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/) over SSL)조차 [Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)/Passive [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 2개 뚫어야 하는 지옥을 해결하지 못해 인프라 외면을 받았다.
  2. <strong><a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/">SSH</a> <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a>의 진화</strong>: [IETF](/knowledge-base/studynote/03_network/12_iot_wpan_edge/635_ietf_core_working_group_coap/) SECSH 워킹 그룹에서 단순한 터미널 텍스트 통신([SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/))을 넘어, 이 암호화 터널 위에서 다양한 애플리케이션을 구동할 수 있도록 구조를 확장하며 SFTP 스펙을 설계했다.
  3. **리눅스 내장 생태계**: [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 진영의 위대한 산물인 `OpenSSH` 패키지에 SFTP 서버(`sftp-server`) 서브시스템이 기본 탑재되면서, 관리자가 [FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/) 데몬(vsftpd 등)을 따로 설치할 필요 없이 리눅스만 깔면 즉시 무결점 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 전송 서버가 가동되는 축복이 열렸다.

```text
+-------------------------------------------------------------+
|          고전 FTP (Multi-Port) vs SFTP (Single-Port) 아키텍처 비교     |
+-------------------------------------------------------------+
|                                                             |
| [ ❌ 버려진 고전: FTP / FTPS ] - 방화벽 타공 지옥                   |
|                                                             |
| Client --(명령어 평문/암호화)---> [포트 21 방화벽 허용] --- 서버    |
|                                                             |
| Client --(짐 덩어리 전송 채널)---> [포트 50000 방화벽 허용] - 서버    |
| Client --(짐 덩어리 전송 채널)---> [포트 50001 방화벽 허용] - 서버    |
| (※ 수천 개의 랜덤 데이터 포트를 통째로 인바운드 허용해야 함)              |
|                                                             |
| [ ✅ 현대의 지배자: SFTP ] - 단일 터널 캡슐화 (Multiplexing)        |
|                                                             |
|                  === 거대한 SSH 암호화 장갑 터널 ===               |
|               +------------------------------+              |
| Client -----> |  [명령 패킷: rm -rf /log]      | ---> 서버       |
|  (FileZilla)  |  [파일 패킷: 0x1A2B3C 바이너리]   |   (OpenSSH)   |
|               +------------------------------+              |
|                 [포트 22 방화벽 1개 허용] <-- 🌟 인프라의 평화!     |
+-------------------------------------------------------------+
```

**[다이어그램 해설]** 클라우드 인프라(AWS 등) 시대에 SFTP가 사실상 표준(De facto)이 된 가장 강력한 아키텍처적 무기를 보여준다. 하단 SFTP 다이어그램에서 클라이언트와 서버 사이의 물리적 연결([TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/))은 오직 22번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 하나뿐이다. 이 강력한 암호화 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/) 내부에서, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 목록을 보는 제어(Control) 메시지와 1GB짜리 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 덤프 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 메시지가 섞여서 논리적 [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)([Multiplexing](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)) 스트림으로 흘러간다. 인프라 엔지니어 입장에서는 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)([Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Group)에서 골치 아프게 여러 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 뚫을 필요 없이 딱 22번 하나만 열면 모든 것이 종결되는 극한의 우아함을 누리게 된다.

- **📢 섹션 요약 비유**: 회사 정문에 직원 출입용 작은 문([포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 21)과 화물차 전용 대형 문 100개([포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 50000~)를 따로 만들고 각각 경비원을 세우는 것이 FTP라면, SFTP는 초거대 방탄 터널([포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 22) 딱 하나만 뚫어서 직원과 화물이 모두 한 길로만 완벽한 검문을 받으며 지나가게 하는 궁극의 단일 게이트 아키텍처입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 스택과 SFTP의 기생 구조

SFTP는 밑단에서 모든 복잡한 보안(핸드셰이크, 키 교환, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))을 [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 데몬(`sshd`)에게 외주(Outsourcing) 준다.

| 계층 | 담당 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) | 핵심 기능 및 원리 | 비유 |
|:---|:---|:---|:---|
| **전송 계층 (Transport)** | [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) Transport Layer [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | 서버 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)(Host [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)), 대칭키([AES](/knowledge-base/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/)) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 해시([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)) 보장 | 방탄 터널과 철도 레일 공사 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a> 계층 (Auth)</strong> | [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) User [Authentication](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/) [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | 비밀번호, <strong><a href="/knowledge-base/studynote/09_security/03_network_security/110_rsa/">RSA</a>/<a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/097_ecdsa_schnorr_signature_bitcoin/">ECDSA</a> 공개키/개인키</strong> 기반 무결점 클라이언트 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) | 터널 입구의 지문/홍채 인식소 |
| **연결 계층 (Connection)**| [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) Connection [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | 하나의 터널 안에 쉘([Shell](/knowledge-base/studynote/02_operating_system/01_overview_architecture/044_shell/)), [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)포워딩, SFTP 등을 섞어 보내는 멀티플렉싱(채널 쪼개기) | 열차 안의 승객칸, 화물칸 나누기 |
| **응용 계층 (Subsystem)** | **SFTP 서브시스템** | 실제 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 읽기, [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), 권한 변경(chmod) 등의 바이너리 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 패킷 주고받기 | 화물칸 안에 박스를 쌓는 로봇 |

### SFTP vs [SCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/747_scp/) (Secure Copy [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))

개발자들이 리눅스 콘솔에서 무심코 섞어 쓰는 `sftp`와 `scp`는 둘 다 [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 터널([포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 22)을 쓰지만, 본질적인 기능 레벨과 아키텍처 역사가 완전히 다르다.

1. <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/747_scp/">SCP</a> (원시적 복사기)</strong>: BSD 기반의 구형 rcp를 [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 위로 포팅한 것. 기능이 오직 "[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 던지고 받기"뿐이다. 전송을 일시 중지(Pause)했다가 이어받기(Resume) 하는 기능이 없고, 원격 서버의 디렉토리 목록을 예쁘게 보여주는 기능도 없다. 속도는 SFTP보다 약간 더 빠르지만(패킷 오버헤드가 적음), 현재 OpenSSH 진영에서는 보안 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)(경로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 미흡 등)을 이유로 [SCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/747_scp/) 스펙 자체를 '사용 중단(Deprecated)' 권고하고 SFTP 백엔드로 강제 마이그레이션시키고 있다.
2. <strong>SFTP (원격 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 시스템 매니저)</strong>: 다운로드/업로드(이어받기 완벽 지원)는 물론, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 이름 변경, 소유자 변경(chown), 폴더 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), [심볼릭 링크](/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/) 제어까지 원격지 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템에 대한 거의 완벽한 POSIX 제어권을 제공한다. FileZilla 같은 GUI 툴들이 뒤에서 쓰는 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이 100% SFTP다.

```text
+-------------------------------------------------------------+
|          SFTP 인증 메커니즘: Password vs Public Key           |
+-------------------------------------------------------------+
|                                                             |
| [ ❌ 패스워드 방식의 치명적 약점 ]                                |
| 서버: 비밀번호 대시오!                                          |
| 봇(Bot): root / 1234 ➔ 실패! (초당 1000번씩 사전 대입 공격)        |
| 🌟 결과: 암호화 터널이 무색하게, 브루트포스(Brute-force) 공격에 의해    |
| 서버 CPU가 낭비되고 비밀번호가 짧으면 뚫려버림.                       |
|                                                             |
| [ ✅ 모범 아키텍처: RSA / ED25519 공개키(Public Key) 기반 인증 ]   |
| 1. 클라이언트가 자물쇠(공개키, id_rsa.pub)와 열쇠(개인키) 쌍을 만듦.  |
| 2. 클라이언트가 자물쇠를 서버 관리자에게 주어 ~/.ssh/authorized_keys 에 등록|
|                                                             |
| SFTP 접속 시도!                                              |
| 서버: "이 랜덤 난수 박스를 내가 가진 네 자물쇠(공개키)로 잠가서 줄게."   |
| 클라이언트: "나한테만 있는 비밀 열쇠(개인키)로 열어서 난수를 돌려줄게!"    |
| 서버: "오, 진짜 네가 맞구나. 터널 오픈!" (비밀번호 입력 1도 없음)         |
|                                                             |
| 🌟 결과: 아무리 중국/러시아 봇들이 접속을 시도해도 애초에 개인키 파일이     |
| 없으면 인증 단계(Challenge) 자체를 시도할 수 없어 원천 차단됨.          |
+-------------------------------------------------------------+
```

**[다이어그램 해설]** 아무리 SFTP [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인이 튼튼해도 입구 컷([인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))에서 털리면 의미가 없다. 실무 클라우드(AWS EC2)에서는 리눅스 장비를 만들 때 아예 패스워드 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인 기능(`PasswordAuthentication no`) 자체를 원천 봉쇄하고, 오직 AWS가 발급해 준 `.pem` 이나 `.ppk` (개인키 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))를 가진 자만 SFTP에 붙을 수 있도록 비대칭키 아키텍처를 강제한다. 이는 비밀번호가 털릴 위험을 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 0%로 만들며, 인프라 자동화 봇([Jenkins](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/), [Ansible](/knowledge-base/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/) 등)이 사람 개입 없이 스크립트로 안전하게 SFTP [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 서버로 밀어 넣을 수 있는 무인 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인의 핵심 기둥이 된다.

- **📢 섹션 요약 비유**: 비밀번호 방식이 아무나 와서 "열려라 참깨"를 수만 번 외치다 우연히 문을 따는 방식이라면, 공개키(Public [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) 방식은 전 세계에 오직 하나뿐인 마스터 열쇠를 열쇠구멍에 꽂아야만 문이 열리는 생체 인식 뺨치는 궁극의 도어락입니다.

---

## Ⅲ. 비교 및 연결

### 딜레마: 막강한 권한([Shell](/knowledge-base/studynote/02_operating_system/01_overview_architecture/044_shell/))을 어떻게 가둘 것인가? (Chroot Jail)

SFTP의 밑단인 [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/)(`sshd`)는 본질적으로 리눅스 쉘([Shell](/knowledge-base/studynote/02_operating_system/01_overview_architecture/044_shell/), 명령창)을 열어주는 악마의 문이다. 외주 업체나 일반 유저에게 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 업로드용으로 SFTP 계정을 열어줬는데, 이 유저가 SFTP 클라이언트가 아닌 터미널(Putty)로 접속하면 리눅스 검은 화면이 열리고 `cd /etc` [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 쳐서 회사의 모든 백엔드 소스 코드를 휘젓고 다니는 대참사가 터질 수 있다.

**아키텍처 해결책: Chroot Jail (감옥 가두기)**
시스템 아키텍트는 서버의 `/etc/ssh/sshd_config` [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 강력한 족쇄를 채운다.
```text
Match Group sftp_users
    ChrootDirectory /data/sftp_home/%u
    ForceCommand internal-sftp
    AllowTcpForwarding no
```
이 3줄의 마법은 완벽하다.
1. `ChrootDirectory`: 유저가 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인하는 순간, 리눅스의 최상위 루트(`/`)가 자신이 속한 폴더(`/data/sftp_home/user1`)로 속여진다. 유저가 아무리 `cd ../../` 로 상위로 올라가려 발버둥 쳐도 이 감옥(Jail)을 절대로 벗어날 수 없다.
2. `ForceCommand internal-sftp`: 유저가 Putty 같은 검은 터미널 쉘로 접속을 시도하면, 쉘 기능을 박탈해버리고 오직 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 주고받는 행위(SFTP)만 허용하도록 강제한다. 즉, 터미널 접속을 즉시 끊어버린다.

### 과목 융합 관점

- <strong>보안 (<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a>) 및 로깅 (<a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/526_security_logging_and_monitoring_failures/">Logging</a>)</strong>: 규제 기관(금감원 등)의 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)를 받는 기업 환경에서는 "누가 언제 고객의 민감 정보 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(CSV)을 SFTP로 다운로드 받아 외부로 빼돌렸는가?"를 증명해야 한다. 순수 OpenSSH만 쓰면 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 전송 이력(Log)을 섬세하게 남기는 데 한계가 있다. 실무에서는 SFTP 요청 앞단에 WAF나 전용 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)([Proxy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)) 장비를 두거나, 클라우드의 완전 관리형 솔루션(AWS Transfer Family)을 융합하여 "홍길동이 12시 5분에 members.csv [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 `RETR` 했다"는 사실을 CloudWatch 같은 거대한 [SIEM](/knowledge-base/studynote/09_security/13_secops_ir_forensics/624_siem/) 통계망으로 실시간 쏟아붓는 아키텍처 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 감시망을 필수적으로 구축해야 한다.

- **📢 섹션 요약 비유**: 청소부(외주 업체)에게 회사 사무실(서버) 열쇠(SFTP)를 줬을 때, 사장실이나 금고(루트 디렉토리)까지 돌아다니지 못하도록 청소 구역만 철창으로 둘러싸고, 카메라(로깅)를 달아 쓰레기([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))만 정확히 치우고 나가게 통제하는 것이 Chroot 아키텍처의 핵심입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

1. <strong>시나리오 — B2B 대용량 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 정산 배치 연동 (Batch Interface)</strong>: A 은행과 B 결제대행사(PG)가 매일 새벽 3시에 10GB짜리 고객 결제 정산 내역 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(CSV)을 주고받아야 한다.
   - **판단**: [REST](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) API나 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) JSON으로 10GB를 보내는 것은 미친 짓(메모리 폭발, [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/))이다. 기업 간 대용량 배치 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 교환의 <strong>업계 표준 De facto는 무조건 SFTP</strong>다. B사 서버에 A사용 SFTP 계정을 만들고 공개키를 교환한 뒤, A사의 쉘 스크립트가 새벽마다 `sftp -i key.pem user@B_server` [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)로 접속해 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 올리는 무인 자동화 셸 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 짠다. HTTP의 복잡한 502 에러 처리나 멀티파트 바운더리 오버헤드 없이 순수 [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 스트림을 가장 우직하고 안전하게 밀어내는 B2B의 영원한 강자다.

2. **시나리오 — 레거시 서버 마이그레이션 중 SFTP 속도 병목**: 인프라 엔지니어가 1TB 크기의 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 구형 서버에서 새로운 유형의 서버로 옮기기 위해 `scp`나 `sftp` 명령을 걸어뒀다. 양쪽 다 10Gbps 광랜이 깔려 있는데, 실제 전송 속도는 100Mbps 수준에서 턱턱 막히고 서버 CPU 중 코어 1개만 사용률 100%를 찍으며 비명을 지르고 있었다.
   - **판단**: SFTP는 강력한 [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 터널에 '기생'하는 구조 탓에, 암호화/복호화 과정([AES](/knowledge-base/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/)-GCM 등)에서 막대한 시스템 CPU 연산(오버헤드)을 소모한다. 특히 싱글 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 한계 탓에 CPU 코어가 아무리 많아도 단일 전송 속도의 임계점에 갇힌다. 내부망([VPC](/knowledge-base/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/) 내부, 폐쇄망 등 패킷 [도청](/knowledge-base/studynote/03_network/14_network_security_threats/701_sniffing_eavesdropping_promiscuous/) 위험이 0%인 [신뢰 구간](/knowledge-base/studynote/08_algorithm_stats/08_stats/146_confidence_interval/))에서 단순 속도가 생명이라면, 보안 검열을 거치는 SFTP 대신 `rsync`나 Netcat(`nc`), 아예 암호화가 빠진 `tar | ssh(치프퍼 튜닝) ` 같은 우회로를 타는 아키텍처적 유연성이 필요하다. 보안을 얻은 대가로 극강의 퍼포먼스(최고 속도)는 어느 정도 포기해야 하는 트레이드오프다.

```text
  +-------------------------------------------------------------+
  |         실무 아키텍처: 클라우드 네이티브의 진화 (AWS Transfer Family) |
  +-------------------------------------------------------------+
  |                                                             |
  | [문제: 전통적 EC2 서버에 구축한 SFTP의 한계]                       |
  | Client ---> [ AWS EC2 (sshd) + EBS 디스크 (500GB) ]           |
  | ❌ 디스크 꽉 차면 터짐. EC2 다운되면 접속 불가(SPOF).                 |
  | ❌ 서버 보안 패치, OS 업그레이드 전부 엔지니어가 챙겨야 함.             |
  |                                                             |
  | [해결: 클라우드 완전 관리형 서버리스 SFTP 아키텍처]                  |
  |                   +------------------------------+          |
  |                   |      AWS Transfer Family     |          |
  | Client --(포트 22)-->| (서버 껍데기만 있음. 무한 스케일링)| --(IAM 역할)|
  |                   +------------------------------+          |
  |                                  | 내부 연결                  |
  |                                  v                          |
  |                       [ 🚀 AWS S3 버킷 ]                      |
  |                  (용량 무제한, 내구성 99.999999999%)          |
  |                                                             |
  | ✅ 판단: 껍데기는 SFTP(포트 22)를 열어주어 옛날 협력사(Client)의   |
  | 오래된 접속 프로그램은 그대로 호환시켜 주고, 실제 파일이 꽂히는 뒷단은|
  | 거대한 오브젝트 스토리지(S3)로 박아버려 용량과 인프라 관리의 족쇄를    |
  | 영원히 끊어버리는 궁극의 모던 아키텍처 패턴!                       |
+-------------------------------------------------------------+
```

**[다이어그램 해설]** 엔터프라이즈 환경에서 "SFTP 서버 좀 하나 만들어주세요"라는 요청이 오면 리눅스(CentOS)를 깔고 `vsftpd`나 `sshd`를 세팅하는 시대는 지났다. 백엔드가 S3([오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/))로 진화하면서 로컬 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 기반의 SFTP는 아키텍처의 암덩어리([Silo](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/))가 되었다. 클라우드 벤더(AWS, Azure)들은 앞단 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)은 전통적인 SFTP/[포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 22번을 흉내 내어 클라이언트를 속이고, 뒷단에서는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 들어오는 즉시 S3 버킷의 오브젝트로 변환해 꽂아버리는 [Serverless](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) Managed SFTP 브리지를 내놓았다. 이를 통해 보안 규정 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/), 무한 용량, 이벤트 기반([Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)) 자동화 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 트리거라는 세 마리 토끼를 단숨에 잡았다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **기술적**: 보안 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)를 통과하기 위해, `sshd_config` [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에서 취약한 구형 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)([Message Authentication Code](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)(예: [md5](/knowledge-base/studynote/03_network/13_network_security_basics/668_md5_hash_collision_vulnerability/))을 배제하고, 안전한 `hmac-sha2-256`, `hmac-sha2-512` 이상으로 터널 암호군(Cipher Suite) 수준을 강제 통제하고 있는가?
- **운영·보안적**: 임직원 퇴사나 외주사 계약 만료 시, SFTP 접속용으로 등록해 두었던 `authorized_keys` (공개키 목록)를 즉시 파기하는 중앙 집중화된 계정 라이프사이클([IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/)) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 체계가 도는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong>FTP의 미련을 못 버리고 FTPS와 섞어 <a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a></strong>: 22번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 하나로 끝나는 우아한 SFTP를 놔두고, 기존 인프라 담당자의 익숙함 때문에 [FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/) 데몬에 억지로 SSL [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 붙여 [FTPS](/knowledge-base/studynote/03_network/09_application_layer_web_email/486_ftps_ftp_over_ssl_tls/)([포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 21, 990) 환경을 유지하며 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 타공 지옥과 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 만료 갱신 노동을 자처하는 행위. SFTP는 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서(Certificate) 갱신 같은 골치 아픈 개념 없이 단순한 키 쌍([Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)-pair) 교환으로 끝나므로 유지 보수 피로도가 제로에 가깝다.

- **📢 섹션 요약 비유**: 껍데기는 구형 유선전화기(SFTP [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)) 모양을 하고 있어 할아버지(오래된 파트너사)도 쉽게 전화를 걸지만, 뒷면의 전선은 최첨단 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 광랜(클라우드 S3)에 꽂혀있어 절대 끊어지거나 용량이 꽉 찰 걱정이 없는 것이 클라우드 시대 SFTP 브리지의 마법입니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | 고전 [FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/) / 평문 환경 | 단일 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) SFTP 아키텍처 전환 후 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 최소 2개 이상~수천 개 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 인바운드 | <strong><a href="/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/">TCP</a> 22번 단일 <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a></strong> 인바운드 | 보안 네트워크 타공/심사 공수 **수십 배 절감** |
| **정량** | Brute-force 비번 크래킹으로 CPU 피크 | 공개키 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 도입 시 패스워드 로직 비활성화 | 패스워드 탈취로 인한 정보 유출 뚫릴 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) **0% 수렴** |
| **정성** | 공유기 [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) 문제로 "다운 안됨" 민원 폭주 | 단일 터널 라우팅으로 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 무사 통과 | 외주사 연동 및 클라이언트 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수발신 통신 **안정성 완벽 확보** |

### 미래 전망
- **대민 서비스에서의 퇴장과 B2B 인프라의 영원한 제왕**: 개인 사용자들이 영화나 음악을 받기 위해 알FTP나 FileZilla를 켜서 서버에 접속하는 낭만의 시대는 웹 하드와 구글 드라이브([HTTPS](/knowledge-base/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/) [REST API](/knowledge-base/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/))의 폭격으로 완전히 종말을 맞았다. 일반 유저의 컴퓨터에는 더 이상 SFTP 클라이언트 프로그램이 깔려있지 않다.
- **백엔드 심연의 지배자**: 하지만 대중의 눈에서 멀어졌을 뿐, 금융권의 배치 망(Batch Network), 망 연계 솔루션(망 분리), [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 덤프 이동 등 <strong>"기계와 기계가 사람의 개입 없이 정해진 시간에 묵묵히 100GB짜리 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>을 밀어 넣어야 하는" 백엔드의 가장 깊고 어두운 심연(Core Infrastructure)</strong>에서는 여전히, 그리고 앞으로 수십 년간 절대 대체되지 않을 견고한 콘크리트 인프라의 철칙으로 군림할 것이다.

### 참고 표준
- <strong><a href="/knowledge-base/studynote/03_network/12_iot_wpan_edge/635_ietf_core_working_group_coap/">IETF</a> SECSH Working Group</strong>: [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) [File Transfer Protocol](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/) ([초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 스펙 정의서)
- **RFC 4251 ~ 4254**: [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/) (SFTP의 기반이 되는 보안 터널, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 명세)

SFTP는 "안전한 껍데기([SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/)) 안에 모든 것을 쑤셔 넣는다"는 발상의 전환이 얼마나 위대한 인프라 혁신을 가져오는지 증명한 산증인이다. [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 여러 개를 열어 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)을 구멍 송송 뚫린 스위스 치즈로 만들던 FTP의 오만을 끝장내고, 22번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)라는 단 하나의 좁고 단단한 관문을 통해 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인부터 거대한 화물 이동까지 완벽하게 통제해 냈다. "단순함이 궁극의 정교함이다([Simplicity](/knowledge-base/studynote/09_security/01_intro_principles/014_simplicity/) is the ultimate sophistication)"라는 진리는 네트워크 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 설계에서도 예외가 아니다.

- **📢 섹션 요약 비유**: 수만 대의 자동차([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 패킷)가 이 골목 저 골목(복수 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))을 쑤시고 다녀서 경찰([방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/))이 감당 못하던 무법지대를 밀어버리고, 오직 중앙에 뚫린 통행증(공개키) 없이는 절대 못 들어가는 단 하나의 거대한 톨게이트 전용 도로([TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 22)를 깔아버린 완벽한 교통 정리의 미학입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [TFTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/484_tftp_trivial_ftp/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) ([Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)) | 사용자 상태 유지와 요청 흐름을 묶는다. |
| 캐시 (Cache) | 응답 속도와 백엔드 부하에 직접 영향을 준다. |
| [FTPS](/knowledge-base/studynote/03_network/09_application_layer_web_email/486_ftps_ftp_over_ssl_tls/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: TFTP]
    |
    v
[현재 개념: SFTP]
    |
    +---> [확장 A: FTPS]
    +---> [확장 B: 지능형 애플리케이션 전달]
```

SFTP는 TFTP에서 출발해 현재 메커니즘을 정교화하고, 이후 FTPS와 지능형 애플리케이션 전달 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 옛날 <strong><a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/">FTP</a></strong>는 택배 박스가 완전 투명한 비닐봉지여서 중간에 배달부(해커)가 우리 집 비밀번호랑 기밀문서를 눈으로 쓱 훔쳐볼 수 있었어요.
2. <strong>SFTP</strong>는 절대 깨지지 않는 무적의 <strong>검은색 장갑차(<a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/">SSH</a> 터널)</strong> 한 대를 만들어서, 그 안에 모든 짐을 꼭꼭 숨겨 단 한 길([포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 22번)로만 밀고 나가는 기술이에요!
3. 심지어 문을 열 때는 도둑들이 찍어 맞출 수 있는 쉬운 비밀번호 대신, 전 세계에 오직 나 하나만 갖고 있는 특별한 <strong>마법 열쇠(개인키)</strong>를 써야만 열리는 최고의 보안 금고랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 606 / 1120

<- **이전**: [484. TFTP (Trivial FTP)](/knowledge-base/studynote/03_network/09_application_layer_web_email/484_tftp_trivial_ftp/)
**다음**: [486. FTPS (FTP over SSL/TLS)](/knowledge-base/studynote/03_network/09_application_layer_web_email/486_ftps_ftp_over_ssl_tls/) ->

---
