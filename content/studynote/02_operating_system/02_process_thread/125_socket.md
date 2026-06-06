---
title: "125. Socket"
date: "2026-05-08"
tags:
  - "studynote-operating-system"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 소켓 (Socket)은 네트워크 상에서 프로세스 간 통신을 가능하게 하는 양방향 통신 종단점 (Endpoint)으로, IP (Internet [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)) 주소와 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) ([Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)) 번호의 조합으로 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)되는 소프트웨어적 창구다.
> 2. **가치**: [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터 ([File](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) Descriptor) 기반의 단일 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 계층을 통해 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) ([Transmission Control Protocol](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)) 스트림과 [UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) ([User Datagram Protocol](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/)) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)그램이라는 상이한 통신 의미론 (Semantics)을 동일한 `read()`/`write()` 인터페이스로 통합하여, 네트워크 프로그래밍의 복잡도를 극적으로 낮춘다.
> 3. **융합**: 로컬 [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) (Inter-Process Communication)로서의 UNIX [Domain](/studynote/05_database/02_modeling_normalization/064_relation_domain/) Socket에서부터 글로벌 네트워크 통신까지 범용적으로 사용되며, [RPC](/studynote/02_operating_system/02_process_thread/126_rpc/) ([Remote Procedure Call](/studynote/02_operating_system/02_process_thread/126_rpc/)), [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/), [마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/) 등 거의 모든 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템의 근간을 이루는 가장 일반적인 통신 메커니즘이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 소켓 (Socket)은 1983년 BSD (Berkeley Software Distribution) UNIX에서 처음 도입된 네트워크 통신 인터페이스로, 두 프로세스가 네트워크를 통해 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받을 수 있게 해주는 표준화된 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) ([Application Programming Interface](/studynote/02_operating_system/01_overview_architecture/014_api_posix/))다. 각 소켓은 (IP 주소, [포트 번호](/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/))의 쌍으로 유일하게 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)된다.

- **필요성**: 물리적으로 분리된 호스트에서 실행되는 프로세스 간에 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 교환하려면 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), 패킷 분할, [흐름 제어](/studynote/03_network/04_data_link_layer_error/213_flow_control_buffer_overflow/), 오류 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 등 수많은 네트워크 계층의 복잡한 작업이 필수적으로 수반된다. [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) ([Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/))나 [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/) ([Shared Memory](/studynote/02_operating_system/02_process_thread/118_shared_memory/)) 같은 기존 IPC는 동일 머신 내에서만 동작하므로, 서로 다른 시스템 간 통신에는 사용할 수 없다. 소켓은 이러한 네트워크 하위 계층의 복잡성을 OS ([Operating System](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)) [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)로 은닉하고, 애플리케이션에게는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 입출력 ([File](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) I/O)과 동일한 친숙한 인터페이스를 제공하여 네트워크 프로그래밍을 실용화한다.

- **등장 배경 및 발전 과정**:
  1. <strong><a href="/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> 네트워크 프로그래밍의 파편화</strong>: 1970년대 각 벤더마다 고유의 네트워크 API를 제공하여, 하드웨어가 바뀌면 애플리케이션을 전면 재작성해야 하는 심각한 이식성 (Portability) 문제가 존재했다.
  2. **BSD 소켓의 혁신**: 1983년 4.2BSD에서 "모든 것은 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이다"라는 UNIX 철학을 네트워크로 확장하여, 소켓을 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터로 관리하는 혁신적 패러다임이 제시되었다.
  3. **POSIX 표준화와 보편화**: POSIX (Portable [Operating System](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) Interface)에서 소켓 API가 표준화되고, Windows (Winsock)까지 수용되면서 전 세계 모든 OS에서 동일한 네트워크 프로그래밍 모델이 가능해졌다.

이 도식은 소켓이 네트워크 통신의 복잡성을 어떻게 계층적으로 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)하여 애플리케이션 개발의 단순화를 달성하는지를 보여준다.

```text
  +-----------------------------------------------------------------+
  |              소켓 (Socket) 계층 추상화 구조                     |
  +-----------------------------------------------------------------+
  |                                                                 |
  |  +-----------------------------------------------------+        |
  |  | Application Layer (사용자 공간)                       |      |
  |  |   +---------+  +---------+  +---------+            |         |
  |  |   | HTTP    |  | FTP     |  | Custom  |            |         |
  |  |   | Server  |  | Client  |  | RPC App |            |         |
  |  |   +----+----+  +----+----+  +----+----+            |         |
  |  |        |            |            |                  |        |
  |  |        +------------+------------+                  |        |
  |  |                     |                               |        |
  |  |  +------------------v--------------------------+   |         |
  |  |  | Socket API (socket, bind, listen, accept,   |   |         |
  |  |  |          connect, send, recv, close)        |   |         |
  |  |  +------------------+--------------------------+   |         |
  |  +---------------------+-----------------------------+          |
  |                        |                                        |
  |  +---------------------v-----------------------------+          |
  |  | OS Kernel (커널 공간)                               |        |
  |  |  +------------------------------------------+     |          |
  |  |  | Transport Layer                         |     |           |
  |  |  |  TCP (SOCK_STREAM) / UDP (SOCK_DGRAM)   |     |           |
  |  |  +------------------------------------------+     |          |
  |  |  | Network Layer                           |     |           |
  |  |  |  IP (Routing, Fragmentation)             |     |          |
  |  |  +------------------------------------------+     |          |
  |  |  | Link / Physical Layer                    |     |          |
  |  |  |  NIC Driver, Ethernet, Wi-Fi             |     |          |
  |  |  +------------------------------------------+     |          |
  |  +---------------------------------------------------+          |
  |                                                                 |
  |  애플리케이션은 Socket API만 호출 -> 나머지는 OS가 자동 처리     |
  +-----------------------------------------------------------------+
```

**[다이어그램 해설]** 이 계층도는 소켓 (Socket)의 핵심 가치가 "하위 계층 은닉 (Layer Hiding)"에 있음을 명확히 보여준다. 애플리케이션 계층에서는 `socket()`, `bind()`, `listen()`, `accept()`, `connect()`, `send()`, `recv()`, `close()`라는 일련의 시스템 콜 ([System Call](/studynote/02_operating_system/01_overview_architecture/013_system_call/))만 호출하면 된다. OS ([Operating System](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)) [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 이 호출을 받아 전송 계층에서의 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) ([Transmission Control Protocol](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)) 3-Way Handshake, 혼잡 제어 ([Congestion Control](/studynote/03_network/08_transport_layer/428_tcp_congestion_control_network_perspective/)), 재전송 (Retransmission), 패킷 분할 및 재조립을 자동으로 수행하고, 네트워크 계층에서의 IP [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)을 처리하며, 물리 계층에서의 [NIC](/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/) (Network Interface Card) 드라이버 제어까지 전담한다. 즉, 애플리케이션 개발자는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어떤 경로로 전송되는지, 중간에 패킷이 유실되었는지, 어떤 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)로 [흐름 제어](/studynote/03_network/04_data_link_layer_error/213_flow_control_buffer_overflow/)가 수행되는지 전혀 알 필요가 없다. 이 강력한 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)가 소켓을 가장 범용적이고 성공적인 네트워크 프로그래밍 인터페이스로 만든 근본 원인이다.

- **📢 섹션 요약 비유**: 복잡한 우체국 시스템, 항공편 물류, 도로 교통망(네트워크 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/))이 전부 벽 뒤에 숨겨져 있고, 우리에게는 편지를 넣고 꺼내는 우체통 하나(소켓 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/))만 보이는 것과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **소켓 쌍 (Socket Pair)** | 통신 양단의 고유 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) | (로컬 IP, 로컬 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)) - (원격 IP, 원격 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))의 4-튜플 | [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/[UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 연결 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | 발신자-수신자 주소 |
| <strong>소켓 <a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a> (Socket <a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a>)</strong> | 애플리케이션-[커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 간 인터페이스 | 시스템 콜 기반의 통신 제어 | POSIX 표준 | 우체국 접수 창구 |
| <strong><a href="/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> 송수신 버퍼 (Tx/Rx Buffer)</strong> | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 임시 저장소 | 네트워크 속도와 앱 처리 속도 간 격차 완충 | [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) [Window Size](/studynote/03_network/04_data_link_layer_error/215_window_size_sender_receiver/) | 우편물 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 대기함 |
| <strong>UNIX <a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">Domain</a> Socket (UDS)</strong> | 로컬 전용 소켓 | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 경로 기반, 네트워크 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 우회 | AF_UNIX, SOCK_STREAM | 사내 메신저 |
| <strong><a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a> 타입</strong> | 통신 의미론 결정 | SOCK_STREAM ([TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)) vs SOCK_DGRAM ([UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/)) | [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/[UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) | 등기우편 vs 일반우편 |

---

### [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 소켓 통신의 표준 수명주기

[TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) ([Transmission Control Protocol](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)) 소켓 기반의 클라이언트-서버 통신은 엄격한 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) 기계 ([State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) Machine)를 따르며, 각 단계에서 특정 시스템 콜이 수행된다.

이 흐름도는 서버의 수동적 개방 (Passive Open)과 클라이언트의 능동적 개방 ([Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) Open)이 맞물려 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 연결이 수립되고 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 교환되며 종료되는 전체 생명주기를 시각화한 것이다.

```text
  +-----------------------------------------------------------------+
  |        TCP 소켓 (Socket) 클라이언트-서버 통신 생명주기          |
  +-----------------------------------------------------------------+
  |                                                                 |
  |   [Server]                          [Client]                    |
  |                                                                 |
  |   socket(AF_INET, SOCK_STREAM, 0)    socket(...)                |
  |       |                                |                        |
  |   bind(ip, port)                       |                        |
  |       |                                |                        |
  |   listen(backlog)                      |                        |
  |       |                                |                        |
  |   accept() <----- 3-Way Handshake ---- connect(ip, port)         |
  |       |     (SYN -> SYN-ACK -> ACK)       |                       |
  |       |  (Block until connected)        |                       |
  |       v                                v                        |
  |   +-----------------------------------------+                   |
  |   |         ESTABLISHED (연결 수립)          |                  |
  |   |                                         |                   |
  |   |   recv()  <----- Data -------- send()    |                   |
  |   |   send()  ----- Data --------> recv()    |                   |
  |   |                                         |                   |
  |   |   (양방향 바이트 스트림 통신)            |                  |
  |   +-----------------------------------------+                   |
  |       |                                |                        |
  |   close() <----- 4-Way Handshake ---- close()                    |
  |       |     (FIN -> ACK -> FIN -> ACK)   |                         |
  |       v                                v                        |
  |   CLOSED                            CLOSED                      |
  +-----------------------------------------------------------------+
```

**[다이어그램 해설]** 이 생명주기 다이어그램의 핵심은 소켓 통신이 명확한 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) ([State Transition](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/))를 따른다는 점이다. 서버는 먼저 `socket()`으로 소켓 엔드포인트를 생성하고, `bind()`로 IP 주소와 [포트 번호](/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)를 할당한 뒤, `listen()`으로 수신 대기 상태로 전환한다. 이때 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 내부에는 SYN 큐와 Accept 큐라는 두 개의 연결 대기 큐가 생성된다. 클라이언트의 `connect()` 호출이 [TCP 3-Way Handshake](/studynote/03_network/08_transport_layer/416_tcp_3_way_handshake_connection_setup/) (SYN -> SYN-ACK -> ACK)를 촉발하면, 서버의 `accept()`는 완료된 연결을 큐에서 꺼내 새로운 통신용 소켓 (Connected Socket)을 반환한다. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 교환 단계에서는 TCP가 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 스트림 ([Byte](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) [Stream](/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/)) 방식으로 동작하므로 메시지 경계가 보장되지 않으며, 애플리케이션 계층에서 [프레이밍](/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/) ([Framing](/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/)) 처리가 필요하다. 종료 시에는 4-Way Handshake를 거치며, 양측이 각각 FIN 패킷을 보내고 ACK를 수신한 뒤 CLOSED 상태로 전이한다. 이 과정에서 TIME_WAIT 상태가 발생하여 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)가 일정 시간 동안 재사용 불가능해지는 현상은 대규모 서버 운영에서 반드시 고려해야 할 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 고갈 ([Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) Exhaustion) 문제의 원인이 된다.

### [Stream](/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/) vs Datagram 의미론 비교

소켓 통신의 의미론 (Semantics)은 전송 계층 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 선택에 따라 근본적으로 달라진다. [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) (SOCK_STREAM)는 연결 지향적 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 스트림을 제공하고, [UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) (SOCK_DGRAM)는 비연결형 메시지 단위 전송을 제공한다.

① <strong>SOCK_STREAM (<a href="/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/">TCP</a>)</strong>: [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 보장 (재전송, 순서 보장, [흐름 제어](/studynote/03_network/04_data_link_layer_error/213_flow_control_buffer_overflow/)), 연결 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)/해제 오버헤드, 1:1 통신, [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 스트림 (메시지 경계 없음)

② <strong>SOCK_DGRAM (<a href="/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/">UDP</a>)</strong>: 비신뢰성 (순서 섞임, 유실 가능), 연결 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 없음, 1:1/1:N/Broadcast 지원, 메시지 경계 보존

③ **SOCK_SEQPACKET**: 순서가 보장되는 메시지 경향의 하이브리드 타입으로, [SCTP](/studynote/03_network/08_transport_layer/447_sctp_multi_stream_multi_homing_4way_handshake/) ([Stream](/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/) Control Transmission [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))에서 사용되며 특수 통신 시나리오에서 활용된다.

- **📢 섹션 요약 비유**: [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 소켓은 연결될 때까지 문을 두드리고(Bind, Listen, Connect, Accept), 연결되면 끊어질 때까지 물 흐르듯 대화하는([바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 스트림) 전화 통화 방식이고, [UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 소켓은 문을 두드리지 않고 편지지를 던져 넣는([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)그램) 우편 투척 방식과 같습니다.

---

## Ⅲ. 비교 및 연결

### 비교 1: 네트워크 소켓 ([TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/[UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/)) vs 로컬 소켓 (UNIX [Domain](/studynote/05_database/02_modeling_normalization/064_relation_domain/) Socket)

| 비교 항목 | 네트워크 소켓 ([TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/[UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/)) | UNIX [Domain](/studynote/05_database/02_modeling_normalization/064_relation_domain/) Socket (UDS) | 판단 포인트 |
|:---|:---|:---|:---|
| **통신 범위** | 이기종 호스트 간 통신 가능 | 동일 머신 내 프로세스 간만 | 통신 대상의 물리적 위치 |
| <strong><a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a> <a href="/studynote/08_algorithm_stats/04_datastructure/057_stack/">스택</a></strong> | [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/IP 전체 계층 경유 | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리 복사만 ([스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 우회) | 레이턴시 요구 사항 |
| **주소 형식** | (IP 주소, [포트 번호](/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)) | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 경로 | 명명 체계 |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> | [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), [체크섬](/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/) 등 오버헤드 존재 | 직접 메모리 복사로 극히 빠름 | 내부 통신 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 민감도 |
| **주 사용처** | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템, 클라이언트-서버 | DB-앱, [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)-앱, [Docker](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 간 | 배포 토폴로지 |

이 비교도는 동일 머신 내에서 통신할 때 네트워크 소켓과 UNIX [Domain](/studynote/05_database/02_modeling_normalization/064_relation_domain/) Socket이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 통해 어떻게 다른 경로로 전달되는지를 시각화한 것이다.

```text
  +-----------------------------------------------------------------+
  |     TCP 루프백 소켓 vs UNIX Domain Socket — 데이터 경로 비교    |
  +-----------------------------------------------------------------+
  |                                                                 |
  |  [TCP 루프백 소켓 (127.0.0.1)]                                  |
  |                                                                 |
  |  Process A              OS Kernel                Process B      |
  |  +-------+  write()   +--------------------+   +-------+        |
  |  | App   |----------->| TCP Stack          |--->| App   |         |
  |  |       |           | - 세그먼테이션     |   |       |         |
  |  |       |           | - 체크섬 계산      |   |       |         |
  |  |       |           | - IP 라우팅(루프백)|   |       |         |
  |  |       |           | - 재조립           |   |       |         |
  |  |       |           | - ACK 처리         |   |       |         |
  |  +-------+           +--------------------+   +-------+         |
  |                     ⚠ 네트워크 스택 전체 경유 (오버헤드)        |
  |                                                                 |
  |  [UNIX Domain Socket (/tmp/app.sock)]                           |
  |                                                                 |
  |  Process A              OS Kernel                Process B      |
  |  +-------+  send()    +--------------------+   +-------+        |
  |  | App   |----------->| VFS Layer          |--->| App   |         |
  |  |       |           | (메모리 복사만)     |   |       |        |
  |  +-------+           +--------------------+   +-------+         |
  |                     ✅ 네트워크 스택 완전 우회                  |
  |                                                                 |
  |  성능 차이: UDS가 TCP 루프백 대비 레이턴시 30~50% 단축          |
  +-----------------------------------------------------------------+
```

**[다이어그램 해설]** 이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로 비교의 핵심은 동일 머신 내 통신에서도 소켓 타입에 따라 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 내에서 거치는 경로가 완전히 다르다는 점이다. [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 루프백 소켓은 127.0.0.1로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보내더라도 실제로는 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/IP [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 전체를 경유한다. 즉, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 세그먼테이션 ([Segmentation](/studynote/02_operating_system/06_memory_management/364_segmentation/))되고, [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/[IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) [체크섬](/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/) ([Checksum](/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/))이 계산되며, IP [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 테이블이 참조되고, 수신 측에서 재조립 및 ACK 처리가 수행된다. 반면 UNIX [Domain](/studynote/05_database/02_modeling_normalization/064_relation_domain/) Socket (UDS)은 [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) ([Virtual File System](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/)) 계층에서 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 버퍼 간의 메모리 복사만으로 통신이 완료된다. 실무에서 이러한 차이는 레이턴시 측면에서 UDS가 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 루프백 대비 약 30~50% 더 빠른 결과를 보이며, 특히 짧은 요청-응답 패턴이 반복되는 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 내부 통신 (예: [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 커넥션 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/), [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이 [사이드카](/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/))에서 이 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이가 직접적인 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) ([Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)) 향상으로 이어진다. 따라서 동일 호스트 내 통신인 경우 UDS를 기본 선택으로 채택하고, 이기종 호스트 간 통신만 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/UDP로 분리하는 아키텍처가 최적이다.

### 비교 2: 소켓 vs 기타 [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) 메커니즘

- <strong><a href="/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a> (<a href="/studynote/02_operating_system/02_process_thread/123_pipe/">Pipe</a>)</strong>: [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/), 부모-자식 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 필수. 소켓보다 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)이 간단하지만 유연성이 현저히 낮다.
- <strong>메시지 큐 (Message <a href="/studynote/08_algorithm_stats/04_datastructure/058_queue/">Queue</a>)</strong>: 비동기 메시지 전달에 유리하지만, 네트워크 통신에는 적합하지 않다.
- <strong><a href="/studynote/02_operating_system/02_process_thread/118_shared_memory/">공유 메모리</a> (<a href="/studynote/02_operating_system/02_process_thread/118_shared_memory/">Shared Memory</a>)</strong>: 가장 빠르지만 동기화가 필요하며 네트워크 확장이 불가능하다.

### 과목 융합 관점

- **컴퓨터 네트워크**: 소켓은 OSI 7계층 모델의 전송 계층 (Layer 4)과 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 계층 (Layer 5) 경계에 위치하며, 애플리케이션 계층 (Layer 7) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) ([HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/), [FTP](/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/), [SMTP](/studynote/03_network/09_application_layer_web_email/488_smtp_simple_mail_transfer_protocol/) 등)이 소켓 위에서 구현된다.
- <strong><a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 시스템</strong>: [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/), Thrift, RMI (Remote Method Invocation) 등 모든 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 통신 프레임워크의 최하위 전송 계층으로 소켓이 사용된다.

- **📢 섹션 요약 비유**: 같은 건물 안에서는 사내 메신저(UDS)로 빠르고 가볍게 대화하고, 다른 건물이나 다른 나라와는 국제 전화([TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/[UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/))를 거는 것처럼, 통신 거리와 요구 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에 따라 적절한 소켓을 선택하는 것과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — C10K 문제와 I/O 멀티플렉싱**: 웹 서버가 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000개 이상의 동시 클라이언트 연결을 처리해야 하는 상황. 전통적인 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)-per-커넥션 모델에서는 각 연결당 하나의 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 할당하므로 메모리와 [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/) 오버헤드가 폭증한다. 아키텍트는 `epoll` (Linux) 또는 `kqueue` (BSD) 기반의 I/O 멀티플렉싱과 Non-[Blocking](/studynote/02_operating_system/02_process_thread/122_sync_async_communication/) 소켓을 결합한 이벤트 구동 아키텍처 (Nginx, Node.js, [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/))를 채택하여 단일 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)로 수만 개의 소켓을 동시 관리하는 설계를 선택해야 한다.

2. <strong>시나리오 — TIME_WAIT <a href="/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a> 고갈</strong>: 고 빈도로 짧은 연결을 반복 생성하는 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 환경에서, 클라이언트 측 임시 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) (Ephemeral [Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))가 고갈되어 새로운 연결 생성이 실패하는 상황. 운영자는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 파라미터 `tcp_tw_reuse`를 활성화하고, [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 커넥션 풀 (Connection Pool)을 도입하여 연결 재사용으로 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 소모를 최소화해야 한다.

이 다이어그램은 대규모 동시 연결 환경에서 소켓 서버 아키텍처 선택이 시스템 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)에 미치는 영향을 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 기반 모델과 이벤트 기반 모델의 비교로 시각화한 것이다.

```text
  +---------------------------------------------------------------+
  |     스레드 기반 vs 이벤트 기반 소켓 서버 — 확장성 비교        |
  +---------------------------------------------------------------+
  |                                                               |
  |  [Thread-per-Connection 모델 (전통적)]                        |
  |                                                               |
  |  +-- Main --+                                                 |
  |  | accept() |---> T1 (conn1, read 대기중)                      |
  |  |         |---> T2 (conn2, read 대기중)                       |
  |  |         |---> T3 (conn3, read 대기중)                       |
  |  |         |---> ...                                           |
  |  |         |---> T10000 (conn10000, read 대기중)               |
  |  +----------+                                                 |
  |  메모리: 10000 × (스레드 스택 8MB) = 80GB 필요!               |
  |  ⚠ 10K 연결에서 이미 메모리 한계 도달                         |
  |                                                               |
  |  [Event-Driven 모델 (epoll / kqueue)]                         |
  |                                                               |
  |  +-- Event Loop (1 스레드) -------------------------+         |
  |  |                                                  |         |
  |  |  epoll_wait() ---> 준비된 소켓 목록 반환          |         |
  |  |       |                                          |         |
  |  |       +- conn1: read 가능 -> 데이터 처리           |        |
  |  |       +- conn7: write 가능 -> 전송 완료            |        |
  |  |       +- conn42: 새 연결 -> accept 처리            |        |
  |  |       +- ... (수만 개 소켓을 1 스레드로 관리)     |        |
  |  |                                                  |         |
  |  +--------------------------------------------------+         |
  |  메모리: 1 × 8MB + 소켓 구조체 ≈ 수십 MB                      |
  |  ✅ 단일 스레드로 100K+ 연결 처리 가능                        |
  +---------------------------------------------------------------+
```

**[다이어그램 해설]** 이 비교도는 소켓 서버의 확장성이 소켓 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 자체의 문제가 아니라, 소켓을 어떤 [동시성](/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 모델로 관리하느냐에 달려 있음을 명확히 보여준다. [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)-per-Connection 모델에서는 각 클라이언트 연결마다 전용 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 생성하므로, 각 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 기본 8MB의 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 메모리를 차지한다. [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000개의 동시 연결에 대해 약 80GB의 메모리가 필요하며, [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/) ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) Switching) 오버헤드도 기하급수적으로 증가한다. 반면 이벤트 기반 모델은 단일 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 `epoll_wait()` 시스템 콜을 통해 준비된 (Ready) 소켓 목록만을 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)로부터 받아와서 순차적으로 처리한다. 소켓은 Non-[Blocking](/studynote/02_operating_system/02_process_thread/122_sync_async_communication/) 모드로 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)되므로 I/O 대기에 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 블로킹되지 않고, [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 이벤트 (읽기 가능, [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 가능, 새 연결 등)를 알려줄 때만 해당 소켓에 대한 처리를 수행한다. 이 구조 덕분에 단일 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)로 10만 개 이상의 동시 연결을 수십 MB의 메모리만으로 처리할 수 있으며, Nginx가 Apache를 대체한 핵심 기술적 이유가 바로 이 이벤트 기반 아키텍처에 있다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **기술적**: 서버의 `somaxconn` (Listen 백로그 큐 크기)가 예상 동시 연결 수를 수용할 수 있도록 튜닝되었는가? Non-[Blocking](/studynote/02_operating_system/02_process_thread/122_sync_async_communication/) 소켓과 `epoll`/`kqueue` 기반 [이벤트 루프](/studynote/02_operating_system/02_process_thread/142_event_loop/)가 적용되었는가?
- **운영·보안적**: 소켓 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터 누수 (FD Leak)를 방지하기 위해 `close()`가 예외 경로에서도 반드시 호출되도록 보장되었는가? 외부 노출 소켓에 대해 DDoS 방어를 위한 연결 속도 제한 ([Rate Limiting](/studynote/09_security/05_web_app_security/520_rate_limiting/))이 적용되었는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong><a href="/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/">TCP</a> 스트림 경계 착각</strong>: [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 소켓에서 한 번의 `write()`가 한 번의 `read()`로 정확히 수신된다고 가정하는 설계. TCP는 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 스트림이므로 패킷이 분할되거나 병합될 수 있으며, 애플리케이션 계층에서 반드시 길이 접두사 (Length-Prefix) 또는 구분자 기반의 [프레이밍](/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/) ([Framing](/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/))을 구현해야 한다.

- **📢 섹션 요약 비유**: 1만 명의 손님에게 각각 전담 직원을 1명씩 배정하면([스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)-per-Connection) 인건비와 공간이 감당할 수 없지만, 안내 데스크 직원 1명이 모니터를 보고 손님이 올 때만 안내하면([이벤트 루프](/studynote/02_operating_system/02_process_thread/142_event_loop/)) 효율적으로 운영되는 것과 같습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 전통적 소켓 (동기/블로킹) | 최적화 (epoll + UDS + 연결 풀) | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 수천 연결에서 메모리 고갈 | 단일 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)로 10만+ 연결 처리 | 동시 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) **100배+ 향상** |
| **정량** | [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 루프백 레이턴시 | UDS로 로컬 통신 대체 | 내부 [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) 레이턴시 **50% 단축** |
| **정성** | 트래픽 [스파이크](/studynote/04_software_engineering/02_requirements_analysis/129_spike_agile_technical_investigation/) 시 서버 장애 | 이벤트 기반 탄력적 처리 | 시스템 [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 및 안정성 극대화 |

### 미래 전망
- <strong><a href="/studynote/03_network/08_transport_layer/454_quic_quick_udp_internet_connections/">QUIC</a> 기반 소켓의 부상</strong>: TCP의 [Head-of-Line](/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/) [Blocking](/studynote/02_operating_system/02_process_thread/122_sync_async_communication/) 문제를 해결하기 위해 [UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 기반 위에 구현된 [QUIC](/studynote/03_network/08_transport_layer/454_quic_quick_udp_internet_connections/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) ([HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/3 표준)이 차세대 소켓 통신의 중심으로 이동하고 있다.
- <strong>io_uring과 <a href="/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> 바이패스</strong>: 리눅스 5.1에서 도입된 io_uring은 기존 소켓 시스템 콜의 오버헤드를 시스템 콜 없이 비동기 I/O를 수행하는 혁신적인 방식으로, 네트워크 애플리케이션 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 한 단계 더 끌어올리고 있다.

### 참고 표준
- **POSIX.1-2008 (IEEE Std 1003.1)**: 소켓 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 표준 규격
- <strong>RFC 793 (<a href="/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/">TCP</a>) / RFC 768 (<a href="/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/">UDP</a>)</strong>: 전송 계층 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 명세
- <strong>RFC 8446 (<a href="/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/">TLS</a> 1.3)</strong>: 소켓 통신 위의 보안 계층 표준

- **📢 섹션 요약 비유**: 전통적인 소켓이 우편 배달부가 집집마다 걸어 다니던 방식이라면, io_uring과 QUIC은 드론과 [초고속](/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 열차로 물류 시스템 자체를 혁신하여 배송 속도와 효율을 극대화하는 진화와 같습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) ([Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [지명 파이프](/studynote/02_operating_system/02_process_thread/124_named_pipe_fifo/) (Named [Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/) / [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [RPC](/studynote/02_operating_system/02_process_thread/126_rpc/) ([Remote Procedure Call](/studynote/02_operating_system/02_process_thread/126_rpc/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [XDR](/studynote/02_operating_system/02_process_thread/127_xdr_external_data_representation/) ([External Data Representation](/studynote/02_operating_system/02_process_thread/127_xdr_external_data_representation/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[지명 파이프 (Named Pipe / FIFO)]
    |
    v
[소켓 (Socket) 통신]
    |
    +---> [RPC (Remote Procedure Call)]
    +---> [XDR (External Data Representation)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 소켓은 집에 설치된 <strong>"마법의 전화기"</strong>예요. 전 세계 어디든 전화번호(IP 주소)와 방 번호([포트 번호](/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/))만 알면 연결할 수 있어요.
2. 전화를 걸 때 "여보세요~" 하고 연결을 확인하는 것([TCP 3-Way Handshake](/studynote/03_network/08_transport_layer/416_tcp_3_way_handshake_connection_setup/))처럼, 소켓도 통신하기 전에 꼭 악수(Handshake)를 해야 해요.
3. TCP는 실수하면 다시 말해주는 친절한 통화 방식이고, UDP는 편지를 마구 던져 넣어 빠르지만 가끔 편지가 분실될 수도 있는 우편 방식이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 125 / 800

<- **이전**: [124. 지명 파이프 (Named Pipe / FIFO) - 양방향 가능, 부모-자식 관계 무관](/studynote/02_operating_system/02_process_thread/124_named_pipe_fifo/)
**다음**: [126. RPC (Remote Procedure Call) - 분산 시스템 함수 호출](/studynote/02_operating_system/02_process_thread/126_rpc/) ->

---
