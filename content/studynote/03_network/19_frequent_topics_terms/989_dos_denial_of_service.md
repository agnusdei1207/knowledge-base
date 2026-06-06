---
title: "DoS"
date: "2026-05-08"
tags:
  - "studynote-network"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [서비스 거부](/studynote/02_operating_system/10_security/599_dos_ddos_attack/) 공격은 빈출 주제와 용어에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [서비스 거부](/studynote/02_operating_system/10_security/599_dos_ddos_attack/) 공격을 이해하면 구분 명확성과 설명력 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [서비스 거부](/studynote/02_operating_system/10_security/599_dos_ddos_attack/) 공격 ([DoS](/studynote/02_operating_system/10_security/599_dos_ddos_attack/), Denial of [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))은 공격자가 표적 시스템, 네트워크 또는 애플리케이션의 처리 용량을 초과하는 비정상적인 요청을 대량으로 전송하여, 시스템의 한정된 자원(네트워크 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), 프로세스 큐, 메모리 버퍼 등)을 고갈시킴으로써 합법적인 사용자의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 요청을 처리할 수 없게 만드는 사이버 공격 기법이다. 이는 정보 보안의 3요소([기밀성](/studynote/09_security/01_intro_principles/002_confidentiality/), [무결성](/studynote/09_security/01_intro_principles/003_integrity/), [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) 중 [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)([Availability](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))을 직접적으로 훼손한다.

- **필요성**: 인터넷 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)에는 네트워크 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 높은 연결을 전제로 설계되어 악의적인 자원 고갈 시도에 대한 방어 매커니즘이 부재했다. [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) ([Transmission Control Protocol](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/))의 3-Way Handshake 과정에서 발생하는 SYN 대기 큐의 한계나 [ICMP](/studynote/03_network/06_network_layer_ip/318_icmp_internet_control_message_protocol_diagnostics/) (Internet Control Message [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))의 응답 특성은 쉽게 악용될 수 있었다. 디지털 경제가 클라우드와 상시 연결된 웹 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 의존하게 되면서, 단 몇 분의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단(Downtime)도 막대한 금전적 손실과 브랜드 [신뢰도](/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 하락으로 직결되므로 [DoS](/studynote/02_operating_system/10_security/599_dos_ddos_attack/) 공격의 본질을 이해하고 네트워크 계층별 방어 아키텍처를 설계하는 것은 현대 IT 인프라 생존의 필수 조건이 되었다.

- **💡 비유**: 한정된 좌석을 가진 인기 레스토랑에 악의적인 무리(공격 트래픽)가 가짜 예약을 대량으로 걸어두거나 입구에 진을 치고 주문을 하지 않으면서 자리만 차지하게 만들어, 진짜 식사를 하려는 손님(정상 사용자)들이 식당에 들어가지 못하고 발길을 돌리게 만드는 상황과 같습니다.

- **등장 배경 및 발전 과정**:
  1. <strong><a href="/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> 취약점 악용</strong>: 1990년대 후반 Ping of Death, Smurf Attack 등 네트워크 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 구조적 취약점을 이용해 단일 패킷이나 적은 트래픽으로도 시스템을 패닉([Kernel Panic](/studynote/02_operating_system/01_overview_architecture/036_kernel_panic/))에 빠뜨리거나 자원을 고갈시키는 공격이 주를 이루었다.
  2. **DDoS의 출현**: 단일 공격자의 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 한계를 극복하기 위해, 악성코드에 감염된 수많은 좀비 [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) (Zombie [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/))로 구성된 [봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) ([Botnet](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/))을 활용하여 트래픽을 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 전송하는 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [서비스 거부](/studynote/02_operating_system/10_security/599_dos_ddos_attack/) 공격 (DDoS, Distributed [DoS](/studynote/02_operating_system/10_security/599_dos_ddos_attack/))으로 진화했다.
  3. **L7 애플리케이션 공격의 부상**: 네트워크 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 방어 기술이 발전함에 따라, 공격자들은 L3/L4 볼륨 공격 대신 적은 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)으로도 서버의 CPU와 DB ([Database](/studynote/05_database/04_transactions_concurrency/501_database/)) 커넥션을 고갈시키는 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) ([HyperText Transfer Protocol](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)) GET Flooding, [Slowloris](/studynote/09_security/03_network_security/258_slowloris/) 같은 정교한 L7 공격으로 타겟을 전환하였다.

다음은 기존 네트워크 구조에서 단일 공격자의 [DoS](/studynote/02_operating_system/10_security/599_dos_ddos_attack/) 공격이 서버의 한정된 큐를 고갈시키는 문제 발생 배경을 보여주는 다이어그램이다.

```text
+---------------------------------------------------------------+
|        DoS 공격의 근본 원인: 자원 비대칭성과 큐 고갈 구조           |
+---------------------------------------------------------------+
|                                                               |
| [정상 사용자]                                [타겟 서버]         |
|     |   1. 정상 요청 (SYN)                      |             |
|     +----------------------------> +---------+|             |
|     |   2. 응답 (SYN-ACK)         | 연결 대기||  처리 완료   |
|     <----------------------------+ 큐(Queue)++-----------> |
|     |   3. 확인 (ACK)             +---------+|  (정상)     |
|     +---------------------------->           |             |
|                                                               |
| [공격자 (Attacker)]                                           |
|     |   1. 위조된 요청 (Spoofed SYN) 대량 발생                    |
|     +----------------------------> +---------+             |
|     +----------------------------> | 꽉 찬 큐| ---> 시스템 마비 |
|     +----------------------------> | (Queue) |     (정상 사용자|
|     |   (ACK를 보내지 않음)         +---------+      접속 불가) |
|                                                               |
| ⚠ 문제점: 서버는 연결이 완료될 때까지 메모리를 할당하고 기다려야 함.   |
| 공격자는 자신의 자원(스푸핑 패킷 생성) 소모 대비 서버의 자원(메모리,  |
| 타임아웃 대기)을 비대칭적으로 크게 고갈시킬 수 있음.                 |
+---------------------------------------------------------------+
```

**[다이어그램 해설]** 이 그림은 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) SYN Flooding 공격의 원리를 통해 [DoS](/studynote/02_operating_system/10_security/599_dos_ddos_attack/) 공격의 핵심인 '자원 비대칭성'을 보여준다. 서버는 [TCP 3-Way Handshake](/studynote/03_network/08_transport_layer/416_tcp_3_way_handshake_connection_setup/) 과정에서 클라이언트의 SYN 요청을 받으면 커넥션 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)을 위한 메모리(Backlog [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/))를 할당하고 SYN-ACK를 보낸 뒤 일정 시간([Timeout](/studynote/02_operating_system/05_deadlock/319_timeout_prevention/)) 대기한다. 공격자는 출발지 IP를 위조([Spoofing](/studynote/02_operating_system/10_security/598_spoofing/))하여 SYN 패킷만 무수히 보내고 최종 ACK를 응답하지 않는다. 이로 인해 서버의 연결 대기 큐는 순식간에 가득 차게 되고, 정작 정상 사용자의 SYN 요청은 큐에 들어갈 자리가 없어 Drop(폐기)된다. 결과적으로 공격자는 아주 적은 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)만으로도 서버의 핵심 자원을 소진시켜 [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 파괴할 수 있다.

- **📢 섹션 요약 비유**: 마치 전화 교환원에게 장난 전화를 수백 통 걸어 통화 대기선을 꽉 채움으로써, 진짜 위급한 전화를 걸려는 사람의 신호가 통화 중(Busy) 음으로 튕겨나가게 만드는 악의적 방해 공작과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **공격자 (Attacker / Master)** | 공격의 주체 및 지휘관 | [봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) ([Botnet](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/)) 구축, C&C 서버를 통한 명령 하달 | [스푸핑](/studynote/02_operating_system/10_security/598_spoofing/) ([Spoofing](/studynote/02_operating_system/10_security/598_spoofing/)), [봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) 제어 | 범죄 조직 보스 |
| **증폭기 / 반사체 (Amplifier / Reflector)** | DRDoS 공격 시 트래픽을 증폭시켜 서버로 반사 | 위조된 IP로 요청을 받아 거대한 응답을 타겟으로 전송 | [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) ([Domain Name System](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/)), [NTP](/studynote/03_network/10_application_layer_dns_mgmt/536_ntp_network_time_protocol_stratum/) ([Network Time Protocol](/studynote/03_network/10_application_layer_dns_mgmt/536_ntp_network_time_protocol_stratum/)) | 확성기 및 반사 거울 |
| **타겟 (Target / Victim)** | 공격의 최종 목표 지점 | 대량의 트래픽/요청을 처리하다가 시스템 자원 고갈 | 웹 서버, 라우터, DB | 표적이 된 성 |
| **L3/L4 네트워크 장비** | 1차 방어선 (라우터, [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/), [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)) | [ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) ([Access Control List](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)) 필터링, [Rate Limiting](/studynote/09_security/05_web_app_security/520_rate_limiting/) 수행 | [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) ([Border Gateway Protocol](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/)) Blackholing | 성벽과 외곽 경비대 |
| <strong><a href="/studynote/09_security/03_network_security/250_scrubbing_center/">스크러빙 센터</a> (<a href="/studynote/03_network/14_network_security_threats/721_drdos_scrubbing_center_mitigation/">Scrubbing Center</a>)</strong> | 대규모 클라우드 기반 트래픽 정제소 | [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 우회로 트래픽을 흡수하여 정상 패킷만 타겟으로 전달 | Anycast [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), DPI (Deep Packet Inspection) | 대규모 오폐수 정화장 |

### [DoS](/studynote/02_operating_system/10_security/599_dos_ddos_attack/) 공격의 유형 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 및 공격 매커니즘

[DoS](/studynote/02_operating_system/10_security/599_dos_ddos_attack/) 공격은 OSI 7계층 기준 타겟팅하는 계층과 고갈시키려는 자원의 종류에 따라 크게 세 가지 범주로 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)된다.

1. **볼륨 기반 공격 (Volumetric Attacks)**: 공격 목표의 네트워크 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) ([Bandwidth](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/))을 완전히 포화시키는 것이 목적이다. [UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) Flooding, [ICMP](/studynote/03_network/06_network_layer_ip/318_icmp_internet_control_message_protocol_diagnostics/) Flooding이 대표적이며, 대량의 트래픽(Gbps ~ Tbps 단위)을 쏟아부어 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)를 막아버린다.
2. <strong><a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a> 공격 (<a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">Protocol</a> Attacks)</strong>: 서버나 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/), 로드 밸런서 등 L3/L4 네트워크 인프라 장비의 실제 처리 능력([State Table](/studynote/01_computer_architecture/01_basic_electronics_logic/066_state_table/) 용량 등)을 소모시킨다. SYN Flooding, Ping of Death, Smurf Attack 등이 속한다.
3. **애플리케이션 계층 공격 (Application Layer Attacks)**: L7 계층에서 웹 서버, 애플리케이션 로직, DB의 CPU/메모리 자원을 고갈시킨다. 패킷 크기는 작지만 처리 비용이 높은 요청(예: 복잡한 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 검색, 대용량 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 다운로드)을 반복 전송하는 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) GET Flooding, [Slowloris](/studynote/09_security/03_network_security/258_slowloris/), [RUDY](/studynote/03_network/14_network_security_threats/723_rudy_slow_http_post_attack/) 공격이 있다.

다음은 현대 DDoS 방어의 핵심 아키텍처인 [스크러빙 센터](/studynote/09_security/03_network_security/250_scrubbing_center/) ([Scrubbing Center](/studynote/03_network/14_network_security_threats/721_drdos_scrubbing_center_mitigation/))를 통한 트래픽 정제 흐름도이다.

```text
+------------------------------------------------------------------+
|             클라우드 기반 DDoS 스크러빙 센터 (Scrubbing Center) 동작       |
+------------------------------------------------------------------+
|                                                                  |
|  [인터넷 트래픽]  (정상 요청 + DDoS 볼륨 공격 트래픽 혼재)                  |
|       |                                                          |
|       |  <- BGP Anycast 라우팅 변경 (트래픽 우회)                     |
|       v                                                          |
|  +------------------------------------------------------------+  |
|  | DDoS 방어 클라우드 (Cloud Scrubbing Center)                    |  |
|  |                                                            |  |
|  |  1. L3/L4 필터링 (ACL, Rate Limit)                         |  |
|  |     +- 볼륨 공격 차단 (UDP/ICMP Flood 폐기)                   |  |
|  |     v                                                      |  |
|  |  2. 프로토콜 분석 (TCP State 검증, SYN Cookie)                 |  |
|  |     +- 비정상 연결 시도 차단 (SYN Flood 방어)                  |  |
|  |     v                                                      |  |
|  |  3. L7 DPI (Deep Packet Inspection) & 행위 기반 분석          |  |
|  |     +- 봇 탐지 (JS 챌린지, CAPTCHA, HTTP 헤더 검증)            |  |
|  |     +- 악성 L7 페이로드 차단 (Slowloris, GET Flood)            |  |
|  +----------------+-------------------------------------------+  |
|                   |                                              |
|                   v 정제된 정상 트래픽 (Clean Traffic) 만 통과           |
|  +------------------------------------------------------------+  |
|  | 타겟 데이터센터 (Victim Data Center) / 웹 서버                    |  |
|  |  -> 정상적인 서비스 제공 가능 (가용성 유지)                          |  |
|  +------------------------------------------------------------+  |
+------------------------------------------------------------------+
```

**[다이어그램 해설]** 이 흐름도의 핵심은 타겟 서버가 직접 대규모 트래픽을 감당하는 대신, 글로벌 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 네트워크를 갖춘 클라우드 기반 [스크러빙 센터](/studynote/09_security/03_network_security/250_scrubbing_center/)가 중간에서 트래픽을 흡수([BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 우회)하여 계층적으로 필터링한다는 점이다. 트래픽이 유입되면 먼저 방대한 클라우드 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)으로 볼륨 공격을 흡수하고, L3/L4 방어 장비를 통해 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 변조 공격([SYN Flood](/studynote/09_security/03_network_security/255_syn_flood/) 등)을 차단한다. 이후 가장 걸러내기 까다로운 L7 공격은 DPI (Deep Packet Inspection) 엔진과 브라우저 챌린지(JavaScript 렌더링 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 등)를 통해 사람의 정상 요청과 봇(Bot)의 악성 요청을 구분해낸다. 최종적으로 정제된(Clean) 트래픽만이 [GRE](/studynote/03_network/07_network_layer_routing/378_gre_generic_routing_encapsulation/) ([Generic Routing Encapsulation](/studynote/03_network/07_network_layer_routing/378_gre_generic_routing_encapsulation/)) 터널이나 프록시를 통해 실제 타겟 서버로 전달된다. 이 다단계 필터링 구조는 단일 기업이 물리적으로 감당할 수 없는 테라비트(Tbps) 단위의 대규모 반사 증폭 공격을 막아내는 유일한 현실적 대안이다.

### 증폭/반사 공격 (DRDoS, Distributed Reflection [DoS](/studynote/02_operating_system/10_security/599_dos_ddos_attack/)) 원리

DRDoS 공격은 공격자가 직접 타겟에게 트래픽을 보내는 대신, 전 세계에 흩어진 취약한 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 서버([DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/), [NTP](/studynote/03_network/10_application_layer_dns_mgmt/536_ntp_network_time_protocol_stratum/), Memcached 등)에 출발지 IP를 타겟의 IP로 위조([Spoofing](/studynote/02_operating_system/10_security/598_spoofing/))하여 요청을 보낸다. 서버들은 이 작은 요청에 대해 수십~수만 배로 증폭된 응답(예: 대규모 [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 존 전송 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), [NTP](/studynote/03_network/10_application_layer_dns_mgmt/536_ntp_network_time_protocol_stratum/) monlist 응답)을 타겟 서버로 일제히 전송한다. 이는 트래픽 증폭비(Amplification Factor)를 활용하여 공격 효율을 극대화하는 방식이다.

- **📢 섹션 요약 비유**: 공격자가 피자 배달 앱에서 주문자의 주소를 '피해자의 집'으로 속여 동네의 모든 피자집(반사체)에 동시에 대량 주문(증폭)을 넣음으로써, 피해자의 집 앞이 수백 명의 배달원으로 꽉 막히게 만드는 지능적인 우회 타격 전술과 같습니다.

---

## Ⅲ. 비교 및 연결

| 비교 항목 | 전통적 [DoS](/studynote/02_operating_system/10_security/599_dos_ddos_attack/) | DDoS ([분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [DoS](/studynote/02_operating_system/10_security/599_dos_ddos_attack/)) | DRDoS ([분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 반사 증폭 [DoS](/studynote/02_operating_system/10_security/599_dos_ddos_attack/)) | 판단 포인트 |
|:---|:---|:---|:---|:---|
| **공격 출발지** | 단일 공격자 IP | 수천~수십만 대의 좀비 [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) ([Botnet](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/)) | 정상적인 공공 서버 ([DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/), [NTP](/studynote/03_network/10_application_layer_dns_mgmt/536_ntp_network_time_protocol_stratum/) 등) | 방어선(IP 차단) 구축 난이도 |
| <strong>IP 위조 (<a href="/studynote/02_operating_system/10_security/598_spoofing/">Spoofing</a>)</strong> | 선택적 | 주로 봇 자체 IP 사용 | **필수** (응답을 타겟으로 유도) | 네트워크 [Egress](/studynote/16_bigdata/09_platform/189_egress/) 필터링 중요성 |
| <strong>트래픽 <a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a> 효율</strong> | 1:1 (공격자 자원 대비) | N:1 ([봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) 규모에 비례) | 1:N (수십~수만 배 **증폭 비율**) | 볼륨 공격의 파괴력 차이 |
| **방어 및 역추적** | 단일 IP 차단으로 용이 | IP [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)으로 차단 어려움, C&C 추적 | 정상 서버의 응답이므로 차단 시 부작용 우려 | [스크러빙 센터](/studynote/09_security/03_network_security/250_scrubbing_center/) 및 [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 필터링 필요 |

전통적인 DoS는 단일 소스에서 발생하므로 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)의 IP 차단 룰셋으로 쉽게 방어할 수 있다. 하지만 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)된 환경에서 들어오는 DDoS는 정상 트래픽과 구분이 어려우며, 특히 DRDoS의 경우 공격 트래픽의 출발지가 구글 8.8.8.8과 같은 정상적인 [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 서버일 수 있어 IP 기반 무조건 차단 시 정상적인 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 이용([DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 해상 등)까지 마비되는 트레이드오프가 발생한다.

네트워크 계층별 공격의 특성을 비교하면, 방어 전략이 트래픽의 '양'을 통제하는 것에서 요청의 '질(행위)'을 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 방향으로 어떻게 달라져야 하는지 명확해진다.

```text
+-----------------+--------------------------------+--------------------------------+
| 기준            | L3/L4 프로토콜/볼륨 공격       | L7 애플리케이션 공격           |
+-----------------+--------------------------------+--------------------------------+
| 주요 공격 기법  | SYN Flood, UDP Flood, Ping     | HTTP GET/POST Flood, Slowloris |
| 타겟 자원       | 네트워크 대역폭, TCP State Table| 웹 서버 CPU, DB 커넥션 큐        |
| 트래픽 규모     | Gbps ~ Tbps 단위 (초대형)      | Mbps 단위 (매우 작음)            |
| 공격 탐지 지표  | BPS (Bits Per Sec), PPS (Packets)| RPS (Requests Per Sec), 지연시간 |
| 방어 메커니즘   | Rate Limiting, SYN Cookie, ACL | WAF (Web App Firewall), CAPTCHA|
| 융합 보안 관점  | 클라우드 ISP 연동 방어 필수    | AI 기반 행위(Behavior) 분석 중요 |
+-----------------+--------------------------------+--------------------------------+
```

**[매트릭스 해설]** 이 비교 매트릭스에서 가장 주목할 부분은 "트래픽 규모"와 "타겟 자원"의 차이다. L3/L4 볼륨 공격은 수도관을 파열시킬 만큼 엄청난 양의 물(트래픽)을 밀어 넣어 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)([대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)) 자체를 막아버린다. 이를 막기 위해서는 타겟 앞에 거대한 댐(클라우드 [스크러빙 센터](/studynote/09_security/03_network_security/250_scrubbing_center/))을 세우는 무식하지만 물리적인 방어력([대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 확보)이 필수적이다. 반면 L7 공격은 적은 양의 물로도 독을 타는(고비용 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 요청) 정교한 암살과 같다. 트래픽 볼륨은 작아 네트워크 장비를 우회하지만, 서버의 CPU를 점유율 100%로 치솟게 한다. 이 경우 댐을 세우는 것이 아니라, 수질 검사기([WAF](/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/), [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 행위 분석)를 도입하여 문맥을 파악하고 정상 요청을 위장한 악성 요청을 식별해야 한다.

- **📢 섹션 요약 비유**: 성벽을 부수기 위해 거대한 투석기로 바위를 쏟아붓는 것(L3/L4 볼륨 공격)과, 성 안에 평범한 상인으로 위장해 침투한 뒤 우물에 독을 타 식수원을 오염시키는 것(L7 애플리케이션 공격)의 차이로 볼 수 있으며, 각각 성벽 강화([대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 증설)와 철저한 검문검색([WAF](/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/) 검사)이 필요합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

1. **시나리오 — 대규모 게임 출시일, 로그인 서버 대상 SYN Flooding 공격 발생**: 동시 접속자가 몰리는 런칭 타임에 초당 수백만 건의 위조된 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) SYN 패킷이 유입되어 로그인 서버의 Backlog Queue가 가득 차고 서버가 응답 불능([Timeout](/studynote/02_operating_system/05_deadlock/319_timeout_prevention/))에 빠지는 상황.
   - **의사결정**: 네트워크 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)에서 방어 기능을 활성화하고, [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(Linux) [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 파라미터를 튜닝하여 <strong>SYN <a href="/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/">Cookie</a> (<code>net.ipv4.tcp_syncookies = 1</code>)</strong>를 적용한다. 서버는 연결 큐에 메모리를 할당하지 않고, 연결 정보를 암호화하여 SYN-ACK 패킷의 시퀀스 번호로 클라이언트에게 되돌려 보낸다. 정상 클라이언트는 이 쿠키를 다시 ACK에 담아 보내므로 그때 커넥션을 맺고, 위조 IP를 쓴 공격자는 ACK를 못 보내므로 메모리 낭비를 원천 차단한다.

2. <strong>시나리오 — <a href="/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a> <a href="/studynote/09_security/03_network_security/258_slowloris/">Slowloris</a> 공격에 의한 웹 서버 커넥션 고갈</strong>: 트래픽 볼륨은 지극히 정상 수준(수십 Kbps)이나, 웹 서버(Apache)의 최대 커넥션 수(MaxClients)가 계속 꽉 차 있어 정상 사용자의 웹 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 접속이 안 되는 상황. 분석 결과, 수백 개의 봇이 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 헤더의 끝을 알리는 개행문자(`\r\n\r\n`)를 보내지 않고, 10초마다 의미 없는 헤더 필드를 한 줄씩 보내 커넥션을 끊지 않고 유지(Hold)하고 있음이 식별되었다.
   - **의사결정**: 요청 헤더를 모두 수신해야 워커 프로세스로 넘기는 Nginx와 같은 Event-Driven 아키텍처 기반의 리버스 프록시를 전면에 배치한다. 또한, [WAF](/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)에서 `client_header_timeout` 및 `client_body_timeout` 값을 매우 짧게(예: 5초) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)하고, 동일 IP에서의 동시 커넥션 수를 제한([Rate Limiting](/studynote/09_security/05_web_app_security/520_rate_limiting/))하여 유휴 상태의 비정상 커넥션을 강제로 끊어버린다.

의사결정 과정에서, 장애 발생 시 이것이 단순한 트래픽 폭증(Slashdot Effect)인지 실제 [DoS](/studynote/02_operating_system/10_security/599_dos_ddos_attack/) 공격인지를 빠르게 판별하고 대응하는 트리가 필요하다.

```text
+-------------------------------------------------------------------+
|           실무 서비스 장애 발생 시 DoS 인지 및 방어 의사결정 트리          |
+-------------------------------------------------------------------+
|                                                                   |
|   [서비스 접속 지연 / Timeout 알람 발생]                             |
|                |                                                  |
|                v                                                  |
|      [모니터링] 네트워크 인입 트래픽(BPS)이 평소의 10배 이상인가?         |
|          +- 예 ------> L3/L4 볼륨 공격(UDP/ICMP Flood) 의심            |
|          |                     |                                  |
|          |                     +--> [조치] BGP 기반 클라우드 스크러빙     |
|          |                               센터로 트래픽 우회 전환 (가동)   |
|          +- 아니오                                                |
|                |                                                  |
|                v                                                  |
|      [서버 로그] 인입 패킷 수(PPS)는 폭증했으나 트래픽(BPS)은 낮은가?     |
|          +- 예 ------> TCP SYN Flooding 등 프로토콜 공격 의심          |
|          |                     |                                  |
|          |                     +--> [조치] L4 장비 SYN Cookie 활성화,   |
|          |                                방화벽 임계치(Threshold) 조정 |
|          +- 아니오                                                |
|                |                                                  |
|                v                                                  |
|      [APM] 특정 API 엔드포인트에 대한 HTTP 503/Timeout이 집중되는가?    |
|          +- 예 ------> L7 HTTP GET Flood / Slowloris 의심            |
|          |                     |                                  |
|          |                     +--> [조치] WAF 룰셋 업데이트(IP 차단),   |
|          |                                CAPTCHA/JS 챌린지 강제 적용   |
|          +- 아니오 ---> 백엔드 DB Lock, 내부 로직 병목 등 비보안 장애 원인 분석|
+-------------------------------------------------------------------+
```

**[다이어그램 해설]** 실무에서 시스템이 다운되었을 때 가장 치명적인 실수는, 내부 애플리케이션 버그나 DB 병목([Lock](/studynote/05_database/04_transactions_concurrency/510_lock/))으로 인한 지연을 DDoS 공격으로 오인하여 엉뚱한 네트워크 장비만 튜닝하며 골든타임을 허비하는 것이다. 이 의사결정 트리는 장애의 양상을 인프라 지표(BPS, PPS)와 애플리케이션 지표([HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 상태 코드, [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/))로 교차 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하여 공격 계층을 정확히 핀포인트하는 과정을 보여준다. 트래픽 볼륨 자체가 회선의 한계를 초과했다면 즉각 [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 우회로 클라우드 방어를 켜야 하고(가장 비용이 큼), 네트워크 계층은 정상이나 서버의 큐만 찬다면 L4 방어를, 트래픽도 큐도 정상이지만 특정 무거운 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 유발하는 API만 호출된다면 WAF를 통해 애플리케이션 계층 차단을 수행해야 한다. 각각의 공격 벡터는 전혀 다른 방어 무기를 요구한다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **기술적**: L4/L7 [Rate Limiting](/studynote/09_security/05_web_app_security/520_rate_limiting/) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)이 정상적인 피크 트래픽을 드롭하지 않도록 [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)가 적절히 튜닝되었는가? [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 인프라가 대규모 질의 증폭 공격에 대비해 Anycast로 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)되어 있는가?
- **운영·보안적**: 클라우드 DDoS 방어 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)([CDN](/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/), [스크러빙 센터](/studynote/09_security/03_network_security/250_scrubbing_center/))의 페일오버 스크립트가 정기적인 모의훈련(DDoS [Red Teaming](/studynote/06_ict_convergence/04_ai_llm/301_ai_safety_red_teaming/))을 통해 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)되었는가? 타겟 서버의 진짜 Origin IP가 Shodan 등에 노출되어 프록시를 우회한 직접 타격 위험은 없는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **단일 접점(Single Point of Failure) 방어**: 클라우드 CDN을 전면에 배치하여 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 트래픽은 완벽히 방어했으나, 서버의 원본(Origin) IP가 그대로 노출되어 있거나 외부에서 직접 접근 가능한 [SSH](/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 포트가 열려 있어 공격자가 CDN을 우회해 직접 볼륨 공격을 때리는 구조. 이 경우 [CDN](/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) 투자는 무용지물이 된다.

- **📢 섹션 요약 비유**: 집에 최첨단 보안 시스템과 두꺼운 철문을 설치([CDN](/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/)/[WAF](/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/) 도입)해 놓고서, 뒷마당 개구멍(Origin IP 노출)을 열어둔 채 방어가 완벽하다고 착각하면 공격자는 언제든 치명적인 일격을 가할 수 있습니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | 방어 체계 미비 | 하이브리드 DDoS 방어 아키텍처 적용 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | Gbps급 볼륨 공격 시 IDC 회선 포화 | Tbps급 클라우드 스크러빙으로 볼륨 흡수 | [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 포화에 따른 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) <strong>Downtime <a href="/studynote/01_computer_architecture/15_advanced_topics/784_zeroization_circuit/">제로화</a></strong> |
| **정량** | L7 공격 방어 실패로 서버 자원 100% 점유 | [WAF](/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/)/Bot Management로 악성 요청 차단 | 서버 CPU/메모리 유휴 자원 **80% 이상 확보** |
| **정성** | 공격 발생 후 수동 분석 및 IP 차단 (수 시간 소요) | [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 트래픽 학습 및 자동 차단 룰 적용 | 대응 시간 단축 (초 단위 방어) 및 브랜드 [신뢰도](/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 유지 |

### 미래 전망
- <strong><a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a>/ML 기반 동적 공격 탐지 (Behavioral Analysis)</strong>: 공격자들이 [봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/)의 IP를 초 단위로 변경하고 정상 사용자와 똑같은 브라우징 패턴(마우스 이동 모사 등)을 흉내 내는 지능형 L7 공격이 증가하고 기승을 부리고 있다. 이에 대응하여, 시그니처나 [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/) 기반 차단을 넘어 머신러닝으로 정상적인 비즈니스 트래픽 베이스라인을 학습하고 미세한 이상 징후를 실시간 차단하는 행동 기반 WAF의 도입이 가속화될 것이다.
- <strong><a href="/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">5G</a> 및 <a href="/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a> 기기 발전에 따른 초거대 <a href="/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/">봇넷</a> 위협</strong>: 5G의 초고속망에 연결된 수십억 대의 취약한 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)(인터넷 공유기, IP 카메라 등) 기기들이 [봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/)으로 편입되면서, 공격 규모가 수 Tbps를 쉽게 상회하는 시대가 열리고 있다. [엣지 컴퓨팅](/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/)([Edge Computing](/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/)) 환경에서 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)된 노드들이 협력하여 공격 트래픽을 발생지 근처에서 차단하는 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 방어 체계가 필수 표준이 될 것이다.

### 참고 표준
- **RFC 2827 (BCP 38)**: 네트워크 [Ingress](/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/) 필터링 표준 (IP [스푸핑](/studynote/02_operating_system/10_security/598_spoofing/)을 방지하기 위한 라우터 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 가이드).
- <strong><a href="/studynote/09_security/17_framework_compliance/848_nist_sp_800_53/">NIST SP 800-53</a></strong>: 연방 정보 시스템 및 조직을 위한 보안 및 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 통제 ([가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 및 [Incident Response](/studynote/09_security/16_data_privacy/806_incident_response/) 규정).

클라우드와 [엣지 컴퓨팅](/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/)의 발전으로 [DoS](/studynote/02_operating_system/10_security/599_dos_ddos_attack/)/DDoS 방어 전략은 단일 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)의 경계 방어에서 글로벌 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 네트워크 기반의 상시 스크러빙 체계로 패러다임이 전환되었다. 방어자는 공격자보다 더 큰 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)([대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/))와 더 스마트한 두뇌([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/))를 전진 배치해야 하며, 이는 보안 아키텍처가 비즈니스 [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 유지의 핵심 투자처임을 시사한다.

- **📢 섹션 요약 비유**: 끝없이 밀려드는 좀비 떼([IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) [봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) 트래픽)를 성문 앞(Origin 서버)에서 창칼로 막는 낡은 전술 대신, 거대한 미로와 덫을 놓은 광활한 요새(글로벌 Edge 네트워크)를 구축하여 적을 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)시키고 자연스럽게 소멸시키는 현대적 방어망으로 진화하고 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [전자 서명](/studynote/03_network/19_frequent_topics_terms/988_digital_signature/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 정의 (Definition) | 용어의 시작점을 분명하게 만든다. |
| 비교 (Comparison) | 헷갈리는 개념의 경계를 드러낸다. |
| [봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) C&C | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 전자 서명]
    |
    v
[현재 개념: 서비스 거부 공격]
    |
    +---> [확장 A: 봇넷 C&C]
    +---> [확장 B: 컨텍스트 기반 용어 해석]
```

[서비스 거부](/studynote/02_operating_system/10_security/599_dos_ddos_attack/) 공격는 [전자 서명](/studynote/03_network/19_frequent_topics_terms/988_digital_signature/)에서 출발해 현재 메커니즘을 정교화하고, 이후 [봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) C&C와 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 기반 용어 해석 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. [서비스 거부](/studynote/02_operating_system/10_security/599_dos_ddos_attack/) 공격([DoS](/studynote/02_operating_system/10_security/599_dos_ddos_attack/))은 10명이 탈 수 있는 버스에 나쁜 악당들이 가짜 승객들로 10자리를 꽉 채워버려서, 진짜로 학교에 가야 하는 친구들이 버스를 타지 못하게 방해하는 못된 장난이에요.
2. 예전에는 한 명의 덩치 큰 악당이 문을 막았다면, 지금(DDoS)은 악당 대장이 조종하는 수만 마리의 로봇 좀비들이 사방에서 몰려와 길 자체를 막아버리는 엄청나게 큰 공격으로 변했어요.
3. 그래서 우리는 길목 곳곳에 로봇과 진짜 사람을 구별해 내는 똑똑한 경비원([방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/))과, 아주아주 넓은 우회도로(클라우드 방어소)를 만들어서 나쁜 로봇들만 골라내 버리고 진짜 친구들만 무사히 학교에 갈 수 있게 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)하고 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 1110 / 1120

<- **이전**: [988. 전자 서명](/studynote/03_network/19_frequent_topics_terms/988_digital_signature/)
**다음**: [990. 봇넷 (Botnet) C&C](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) ->

---
