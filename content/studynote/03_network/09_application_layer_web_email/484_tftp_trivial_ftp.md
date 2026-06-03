+++
title = "484. TFTP (Trivial FTP)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TFTP는 응용 계층과 웹/메일에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: TFTP를 이해하면 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)과 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: TFTP(Trivial [File Transfer Protocol](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/))는 [FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/)([File Transfer Protocol](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/))의 극단적인 경량화 버전이다. 복잡한 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 연결 상태 유지와 이중 채널 구조를 버리고 비연결형인 [UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/)(기본 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 69) 위에서 구동되며, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)(ID/PW)과 디렉토리 탐색 기능조차 제거된 순수한 "[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 읽기(RRQ)와 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(WRQ)" 원툴 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이다.

- **필요성**: 인터넷 초창기부터 깡통 상태의 컴퓨터나 네트워크 장비(라우터, [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) 등)를 켰을 때 OS나 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)를 어디선가 가져와야 했다. 장비 안에는 겨우 수 킬로바이트(KB) 용량의 부트롬(Boot [ROM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/255_rom/))밖에 없었다. 이 좁은 공간에 복잡한 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)과 방대한 [FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/) 클라이언트 소스 코드를 구워 넣는 것은 불가능했다. "그냥 묻지도 따지지도 말고 저기 있는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 하나만 가볍게 내려받을 수 있는 가장 작고 무식한 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)"이 인프라 엔지니어들에게 절대적으로 필요했다.

- **💡 비유**: 일반 <strong><a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/">FTP</a></strong>가 택배 기사가 신분증(ID/PW)을 꼼꼼히 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고 인수증에 사인([TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/))을 받은 뒤 무거운 짐을 집 안까지 안전하게 날라주는 <strong>우체국 안심 택배</strong>라면, <strong>TFTP</strong>는 드라이브스루 창구에서 이름표 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)도 없이 그냥 종이봉투([UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/))를 던져주고 돈도 안 받고 차를 보내버리는 <strong>초간단 패스트푸드 픽업</strong>과 같습니다.

- **등장 배경**:
  1. **초창기 네트워크 부팅의 난관**: 디스크 없는 터미널(Diskless Workstation)이 유행하던 시절, [네트워크 인터페이스 카드](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/)([NIC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/))만으로 서버에서 OS 이미지를 당겨와 부팅하는 PXE(Preboot Execution [Environment](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/066_gitlab_flow_environment_branch_strategy/)) 생태계가 싹트기 시작했다.
  2. **가벼움의 미학**: 1981년 [IETF](/knowledge-base/studynote/03_network/12_iot_wpan_edge/635_ietf_core_working_group_coap/)(RFC 783)에서 TCP의 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)과 FTP의 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 싹 다 덜어낸 TFTP 표준을 제정했다.
  3. **인프라 자동화의 핵심**: 라우터나 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)에 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)를 입히거나 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 빼낼 때, 복잡한 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 절차 없이 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 한 줄로 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 쏴버리는 용도로 네트워크 장비 벤더([Cisco](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/) 등)의 절대적 지지를 받으며 살아남았다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">TFTP 통신 흐름도: Stop-and-Wait 메커니즘 (RRQ)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Client (깡통 라우터/PC)</div><div class="kb-diagram-node">TFTP Server (69)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. Read Request (RRQ): "boot.img 줘!"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(인증 절차 아예 없음! 그냥 파일 이름만 던짐)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. Data Block 1 (512 Bytes)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. ACK 1 (1번 블록 잘 받았어!)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. Data Block 2 (512 Bytes)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">5. ACK 2 (2번 블록 잘 받았어!)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(중략)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">6. Data Block N (500 Bytes) - 마지막 조각!</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">🌟 결과: 블록 크기가 512 바이트보다 작게 오면 "파일 끝(EOF)"으로 인식!</div></div>
</div>
</div>



**[다이어그램 해설]** TFTP는 UDP를 쓴다. UDP는 패킷 유실을 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)해주지 않기 때문에 TFTP가 애플리케이션 레벨에서 가장 멍청하고 원시적인 핑퐁 게임인 **Stop-and-Wait (정지 대기)** 알고리즘을 사용한다. 서버가 512바이트짜리 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록(1번)을 던지면, 클라이언트가 "1번 잘 받았어(ACK)"라고 대답할 때까지 서버는 다음 블록(2번)을 절대 던지지 않고 멈춰 서서 기다린다. 만약 중간에 패킷 유실되어 ACK가 안 오면 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)을 걸고 똑같은 블록을 재전송한다. 512바이트씩 찔끔찔끔 보내고 멈추기를 반복하므로 대용량 전송 시 속도는 매우 처참하지만, 구현해야 할 소스 코드가 불과 수백 줄에 불과할 정도로 극단적으로 가볍다는 것이 최대 무기다. 마지막 블록이 512바이트 미만(예: 500바이트)으로 오면 클라이언트는 아! 이게 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 끝이구나! 하고 다운로드를 종료한다.

- **📢 섹션 요약 비유**: TFTP는 물건을 한 번에 다 싣고 오는 게 아니라, 삽으로 모래를 한 삽 퍼서 주고([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)), "받았어?(ACK)" [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한 뒤에야 다음 삽을 푸는 아주 답답하지만 절대 코드가 꼬일 일 없는 단순 노동과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### TFTP 메시지 포맷 (5가지 [Opcode](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/159_opcode/))

TFTP는 복잡한 텍스트 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 쓰지 않고, 2바이트짜리 [Opcode](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/159_opcode/)(명령 코드)로 자신의 의도를 나타내는 이진(Binary) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이다.

| [Opcode](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/159_opcode/) | 메시지 타입 | 설명 |
|:---|:---|:---|
| **1** | **RRQ** (Read Request) | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 다운로드 요청. `[Opcode: 1][파일명][0][모드(netascii/octet)][0]` 형태 |
| **2** | **WRQ** (Write Request) | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 업로드 요청. |
| **3** | <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">DATA</a></strong> | 실제 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/). `[Opcode: 3][블록 번호 2바이트][데이터(최대 512바이트)]` |
| **4** | **ACK** (Acknowledgment) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수신 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/). `[Opcode: 4][블록 번호 2바이트]` |
| **5** | **ERROR** | 에러 발생. 예: "[File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) not found", "Access violation" |

### 통신 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 변경의 마법 (Ephemeral [Port](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))

TFTP 서버는 기본적으로 [UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 69번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 리스닝(Listening)하며 클라이언트의 RRQ/WRQ 요청을 기다린다. 하지만 <strong>실제 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 전송(DATA와 ACK 교환)은 69번 <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a>에서 일어나지 않는다.</strong>

만약 69번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 수천 대의 장비가 동시에 부팅 이미지를 달라고 몰려들면 하나의 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 패킷을 구분하기 어렵다. 따라서 클라이언트가 69번으로 첫 요청을 찌르면, 서버는 즉시 랜덤한 고포트(Ephemeral [Port](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), 임시 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))를 새로 하나 열어서 그 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 첫 번째 `DATA` 블록을 쏜다. 클라이언트는 이걸 눈치채고 이후부터는 69번이 아닌 그 새로운 임시 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 `ACK`를 쏘며 둘만의 독립적인 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 전송 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)을 이어간다. 이것이 TFTP가 멀티플렉싱([다중 접속](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 처리)을 구현하는 가벼운 트릭이다.


| 항목 | [FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/) ([File Transfer Protocol](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/)) | TFTP (Trivial [FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/)) |
|:---|:---|:---|
| **전송 계층** | <strong><a href="/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/">TCP</a></strong> ([신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 있는 스트림) | <strong><a href="/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/">UDP</a></strong> (비연결형 다이어그램) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a> 사용</strong> | 제어(21) + [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(20/랜덤) 이중 채널 | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 접속(69) + [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(임시 랜덤) 단일 핑퐁 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a> (<a href="/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/">Authentication</a>)</strong>| `USER/PASS` 필수 | **없음 (묻지도 따지지도 않음)** |
| **폴더 탐색 기능** | `LIST`, `CWD` (폴더 이동/조회 가능) | 없음 (정확한 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 이름과 경로를 알아야만 받을 수 있음) |
| <strong><a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/213_flow_control_buffer_overflow/">흐름 제어</a> / 혼잡 제어</strong> | [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 슬라이딩 윈도우로 고속 펌핑 | **Stop-and-Wait (ACK 올 때까지 대기)**, 속도 극악 |
| **주 사용처** | 인터넷망 대용량 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 송수신 (과거) | <strong>LAN 폐쇄망 내부 라우터/<a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a> <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/">펌웨어</a> 업데이트, PXE 부팅</strong> |

### 과목 융합 관점

- <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a> (OS)</strong>: 디스크 없는(Diskless) 환경에서 OS를 올리려면 [DHCP](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/522_dhcp_dynamic_host_configuration_protocol/), TFTP, BootP [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이 3인 1조로 융합되어 동작한다.
  1. 클라이언트(깡통 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/))가 켜지면 [NIC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/) 롬([ROM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/255_rom/))이 [DHCP](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/522_dhcp_dynamic_host_configuration_protocol/) 브로드캐스트를 쏴서 IP를 받는다.
  2. [DHCP](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/522_dhcp_dynamic_host_configuration_protocol/) 서버는 IP뿐만 아니라 `Option 66(TFTP 서버 IP)`과 `Option 67(부팅 파일 이름: pxelinux.0)`을 같이 알려준다.
  3. 클라이언트는 즉시 TFTP 서버로 달려가 이 부팅 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 다운로드받아 메모리(RAM)에 올려 OS 설치를 시작한다. 이것이 엔터프라이즈 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)센터에서 수천 대의 서버를 한 방에 자동 포맷하고 리눅스를 까는 <strong>PXE (Preboot Execution <a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/066_gitlab_flow_environment_branch_strategy/">Environment</a>)</strong> 아키텍처의 심장부다.
- <strong>보안 (<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a>)</strong>: TFTP는 보안의 S자도 없는 위험한 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이다. 만약 TFTP 서버를 외부에 퍼블릭으로 열어둔다면 누구나 `GET /etc/passwd` 같은 요청을 날려 서버의 핵심 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 무단으로 빼갈 수 있다([Directory Traversal](/knowledge-base/studynote/09_security/05_web_app_security/420_directory_traversal/)). 실무에서는 철저하게 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)([ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/))으로 감싸진 OOB(Out-of-Band) 관리망 안에서만 일시적으로 열어서 쓰고 닫아야 한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">액티브 FTP vs 패시브 FTP 동작 원리…</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">TFTP</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">SFTP</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: FTP가 정식으로 서류 심사를 거쳐 짐을 싣는 거대한 이삿짐센터라면, TFTP는 서류 검사도 없이 "저기 있는 박스 줘" 하면 그냥 던져주는 무인 보관함입니다. 빠르고 편하지만 도둑이 들기 딱 좋은 시스템이죠.

---

## Ⅲ. 비교 및 연결

TFTP를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [액티브](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/) vs 패시브 [FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/) 동작 원리…가 기반 조건을 만든다면, TFTP는 그 위에서 핵심 메커니즘을 구현하고, SFTP는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)과 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [액티브](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/) vs 패시브 [FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/) 동작 원리…의 기반 정리 | TFTP의 핵심 동작 | SFTP의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: TFTP는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

1. <strong>시나리오 — 대규모 IDC 베어메탈 서버 <a href="/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/">프로비저닝</a> (PXE Boot) 자동화</strong>: 클라우드 인프라팀이 500대의 신규 블레이드 서버를 랙(Rack)에 꽂았다. 사람이 일일이 USB를 들고 가서 OS를 깔 수 없으므로, 사내 망에 DHCP와 TFTP 서버(dnsmasq, tftpd)를 구축했다. 서버 전원을 켜면 NIC가 알아서 TFTP를 통해 Ubuntu Kickstart 부트 이미지를 빨아들여 동시에 500대가 자동 포맷되고 OS 세팅이 완료되는 인프라 코드화([IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)) 파이프라인을 완성했다.
   - **판단**: TFTP는 비록 낡고 느리지만, 이 '최초 생명 부여([Bootstrapping](/knowledge-base/studynote/14_data_engineering/02_math_mining/120_concept/))' 단계에서는 어떤 무거운 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)도 이 가벼움을 이길 수 없다. 부트롬(Boot [ROM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/255_rom/))에 HTTP나 [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 클라이언트 코드를 우겨넣는 것은 칩셋 단가 상승을 부르기 때문이다.

2. <strong>시나리오 — <a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/">Cisco</a> 라우터 <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a> <a href="/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/">백업</a>(<a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">Config</a> <a href="/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/">Backup</a>) <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/">타임아웃</a> 장애</strong>: 네트워크 엔지니어가 본사에서 지방 지사에 있는 [Cisco](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/) 라우터에 접속해 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 쳤다. `copy running-config tftp://10.0.0.5/backup.cfg`. 라우터 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 중앙 TFTP 서버로 덤프 뜨려는 시도였다. 하지만 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 용량이 2MB가 넘었고 핑(Ping)이 50ms인 지방 WAN 구간이라, TFTP의 지독한 Stop-and-Wait 전송 속도 탓에 전송이 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)되다 결국 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)으로 실패했다.
   - **판단**: TFTP의 기본 블록 크기(Block Size)는 512바이트다. 2MB를 보내려면 4,000번 왕복([RTT](/knowledge-base/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/))을 해야 한다. WAN 구간처럼 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))이 있는 곳에서는 최악이다. 실무에서는 RFC 2348 확장을 활용해 클라이언트와 서버가 사전에 `blksize=8192` [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 등으로 블록 크기 협상(Option Negotiation)을 거치도록 튜닝하거나, 라우터 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 방식을 [SCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/747_scp/)([SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 기반 복사)나 FTP로 업그레이드하는 것이 장애를 막는 정석이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">실무 아키텍처: PXE Network Booting (TFTP 융합 아키텍처)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">디스크 없는 깡통 PC</div><div class="kb-diagram-note">(전원 ON!)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. DHCP 브로드캐스트 (나 IP 좀 줘! 부팅 파일 위치도!)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">DHCP 서버</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. DHCP 응답 (IP: 192.168.1.10, TFTP IP: 192.168.1.100,</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">부트파일: pxelinux.0)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. TFTP RRQ (pxelinux.0 줘!)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">TFTP 서버 (Port 69)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. TFTP DATA (부팅 커널 이미지 쪼개서 전송)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">🌟 결과: 하드디스크가 텅 비어있던 PC가 메모리에 OS 이미지를 적재하고</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">운영체제 부팅 스크린을 띄우며 마법처럼 깨어난다!</div></div>
</div>
</div>



**[다이어그램 해설]** 클라우드 인프라를 지탱하는 베어메탈 서버 자동화의 바이블이다. 이 시퀀스에서 TFTP가 빠지면 네트워크 부팅 자체가 성립되지 않는다. 아무것도 모르는 깡통([NIC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/))에게 가장 가벼운 언어([UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/))로 생명의 불씨(OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))를 던져주어 일단 부팅을 시키고 나면, 그다음부터는 올라간 진짜 OS가 무겁고 튼튼한 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/[HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 통신망을 잡고 나머지 설치 패키지를 고속으로 다운받는다. TFTP는 우주선이 궤도에 오를 때까지만 쓰고 버리는 '1단 로켓' 역할을 완벽히 수행한다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **기술적**: 대용량 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)(수백 MB)를 전송해야 할 경우, 기본 512바이트 블록 제한에 걸려 전송 속도가 나락으로 떨어지지 않도록 TFTP 서버 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)에서 `Tsize(파일 전체 크기)` 및 `Blksize(블록 크기)` 옵션 협상 확장이 켜져 있는가?
- **운영·보안적**: 사내 망에 임시로 띄워둔 tftpd 데몬이 실수로 `0.0.0.0` (모든 인터페이스) 바인딩으로 열려있어, 외부망 인터넷에서 내부 스크립트 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 몰래 RRQ로 훔쳐갈 수 있는 보안 구멍이 방치되지 않았는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong>대용량 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 배포망으로의 남용</strong>: "[설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)도 없고 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)도 하나만 열면 되니 너무 편하네!"라는 이유로 사내 망의 수 기가바이트(GB)짜리 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 시스템을 TFTP 파이프라인으로 짜버리는 대형 사고. Stop-and-Wait의 저주에 걸려 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 1Gbps 네트워크 위에서 고작 1Mbps 속도를 내며 시스템이 병목에 질식사하게 된다.

- **📢 섹션 요약 비유**: TFTP는 아기에게 처음 떠먹이는 이유식(부팅 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)) 같은 겁니다. 소화(로직)가 아주 쉬워서 깡통 상태의 갓난아기(장비)도 금방 먹을 수 있지만, 다 큰 어른(대용량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송)에게 하루 종일 이유식만 먹이려 들면 답답해서 병이 납니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | [USB](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/) 기반 수동 인프라 셋업 | TFTP + PXE 부팅 자동화 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 서버 100대 OS 수동 설치 50시간 소요 | TFTP 브로드캐스팅 10분 동시 설치 | 인프라 [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/) (Time-to-Value) **99% 단축** |
| **정량** | [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) ROM에 무거운 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/[FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/) [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 탑재 | 롬 용량 수 KB의 TFTP 코드만 삽입 | 임베디드 및 네트워크 장비 메모리 **원가 절감** |
| **정성** | 복잡한 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 연동 과정 | [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) CLI [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 한 줄 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 완료 | 네트워크 장비 엔지니어 관리 편의성 극대화 |

### 미래 전망
- <strong>UEFI와 <a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a> 부팅의 추격</strong>: 최근 서버 메인보드의 진화로 기존 레거시 BIOS를 엎어버리고 UEFI가 대세가 되면서, 메인보드 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 자체에 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)과 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/)) 모듈을 욱여넣어 TFTP를 버리고 곧바로 안전한 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/[HTTPS](/knowledge-base/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/) 부팅([HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) Boot)을 때리는 시대가 도래하고 있다.
- **제한된 갈라파고스에서의 생존**: 범용 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 전송 생태계에서는 이미 멸종했지만, 낡은 시스코([Cisco](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/)) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 환경, 공장 자동화 라인의 소형 [PLC](/knowledge-base/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/) 장비, IP 폰(VoIP) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 배포 등 극한의 경량화와 하위 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)이 요구되는 [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/)([Operational Technology](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/)) 및 임베디드 폐쇄망에서는 앞으로도 영원히 수명을 다하지 않고 생존할 좀비 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이다.

### 참고 표준
- **RFC 1350**: The TFTP [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) (Revision 2) - 가장 널리 쓰이는 표준 명세서
- **RFC 2347 / 2348**: TFTP Option Extension / Blocksize Option (512바이트 한계 돌파를 위한 확장)

"완벽함이란 더 이상 보탤 것이 없을 때가 아니라, 더 이상 뺄 것이 없을 때 완성된다." 생텍쥐페리의 이 격언은 TFTP 아키텍처에 완벽하게 부합한다. 상태 제어, 에러 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 슬라이딩 윈도우, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 등 네트워크 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이 가질 수 있는 모든 군더더기를 가차 없이 베어낸 이 무식한 핑퐁 게임은, 역설적이게도 그 텅 빈 가벼움 덕분에 네트워크 장비가 숨을 쉬기 위한 최초의 호흡(Booting)을 40년 넘게 도맡아올 수 있었다. 가장 원시적이지만 가장 치명적인 인프라의 마중물이다.

- **📢 섹션 요약 비유**: TFTP는 건물을 지을 때 가장 먼저 박아넣고 콘크리트가 굳으면 버려지는 뼈대(비계)와 같습니다. 예쁘지도 튼튼하지도 않지만, 이 뼈대가 없으면 거대한 마천루(클라우드 인프라)는 애초에 올라갈 시도조차 할 수 없는 근본적인 기초 공사입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [액티브](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/) vs 패시브 [FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/) 동작 원리… | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) ([Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)) | 사용자 상태 유지와 요청 흐름을 묶는다. |
| 캐시 (Cache) | 응답 속도와 백엔드 부하에 직접 영향을 준다. |
| [SFTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/485_sftp_ssh_file_transfer/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">선행 개념: 액티브 FTP vs 패시브 FTP 동작 원리…</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재 개념: TFTP</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 A: SFTP</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 B: 지능형 애플리케이션 전달</div></div>
</div>
</div>



TFTP는 [액티브](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/) vs 패시브 [FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/) 동작 원리…에서 출발해 현재 메커니즘을 정교화하고, 이후 SFTP와 지능형 애플리케이션 전달 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 일반 <strong><a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/">FTP</a></strong>가 우체국 아저씨가 신분증 검사 다 하고 무거운 짐을 집 안까지 튼튼한 수레([TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/))로 옮겨주는 거라면요.
2. <strong>TFTP</strong>는 이름 검사도 없이, 작은 삽(512바이트)으로 모래([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 한 번 푸고 "받았어?(ACK)" [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하면 다시 한 삽 푸는 <strong>초간단 노가다(<a href="/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/">UDP</a>)</strong>예요.
3. 무식하게 느리지만 룰이 너무나 단순해서, 복잡한 생각을 할 수 없는 깡통 로봇(공장 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화된 라우터)한테 처음으로 밥(OS 이미지)을 떠먹일 때 무조건 써야 하는 1등 공신이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 605 / 1120

← **이전**: [483. 액티브(Active) FTP vs 패시브(Passive) FTP 동작 원리 차이](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)
**다음**: [485. SFTP (SSH FTP)](/knowledge-base/studynote/03_network/09_application_layer_web_email/485_sftp_ssh_file_transfer/) →

---
