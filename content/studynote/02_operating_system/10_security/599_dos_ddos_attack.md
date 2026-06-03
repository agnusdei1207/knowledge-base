+++
title = "599. 서비스 거부 (DoS) 및 분산 서비스 거부 (DDoS) 네트워크 자원 고갈 공격"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DoS (Denial of [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 및 DDoS (Distributed DoS) 공격은 시스템 권한을 탈취(Hacking)하는 것이 아니라, 타겟 서버의 네트워크 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), CPU, 메모리, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 자원 등을 고갈시켜 정상적인 사용자의 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 이용을 원천적으로 불가능하게 만드는 **[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)([Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) 파괴 공격**이다.
> 2. **가치**: 해커의 단일 PC에서 이루어지던 고전적 DoS와 달리, 현대의 DDoS는 악성 [봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/)([Botnet](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/))과 프로토콜의 증폭 반사(Reflection) 취약점을 활용해 수십 Tbps의 폭발적 트래픽을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하며 인터넷 근간 인프라를 마비시키는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 사이버 테러 도구다.
> 3. **융합**: [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) (OS)의 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)(Backlog [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/), Time-wait)과 웹 애플리케이션 아키텍처의 비동기 처리 구조를 교묘히 타격하므로, 단순 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 확장이 아닌 [CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/)/Anycast 망 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/), [WAF](/knowledge-base/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/) [임계치](/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/) 제어, 블랙홀(Blackholing) [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 등 L3에서 L7을 아우르는 융합 방어 아키텍처가 필수적이다.

---

## Ⅰ. 개요 및 필요성

**개념 및 정의**
[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 거부 (DoS, Denial of [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 공격은 타겟 시스템이 감당할 수 없는 엄청난 양의 트래픽을 전송하거나, 치명적인 오작동을 유발하는 패킷을 보내 시스템의 가용 자원([대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), 메모리, 프로세스 연결 수)을 완전히 바닥나게 하는 공격이다. [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 거부 (DDoS, Distributed DoS)는 이 공격을 좀비 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)([봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/)) 수만~수십만 대가 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)된 위치에서 일제히 쏟아붓게 함으로써 파괴력을 극대화한 진화 형태다.

**필요성 및 등장 배경**
정보보안의 3요소([기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/), [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/), [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) 중 데이터가 유출되지 않았더라도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 자체가 멈춘다면 기업은 즉각적인 금전적/신뢰적 타격을 입는다. 과거 Ping of Death나 SYN Flooding 같은 1:1 기반의 DoS 공격은 방어측 인터넷 회선망([Pipe](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/))의 발전과 OS [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 패치로 점차 막히기 시작했다. 그러자 해커들은 [사물인터넷](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)([IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)) 기기 취약점을 뚫어 거대한 [봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) 군단을 만들거나, [NTP](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/536_ntp_network_time_protocol_stratum/)/[DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 서버의 응답 크기 차이를 이용해 트래픽을 수백 배로 불리는(Amplification) DDoS 기법을 개발하여 클라우드 센터조차 무너뜨리는 괴물 트래픽을 뿜어내기 시작했다.

```text
┌─────────────────────────────────────────────────────────────────┐
│      DoS와 DDoS 공격 아키텍처의 근본적 진화 차이 비교도         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [고전적 DoS (1:1 공격)]                                        │
│                                                                 │
│  해커 (Attacker) ━━━━(악성 트래픽 폭탄)━━━━▶ 타겟 서버          │
│  => 한계: 해커의 회선 속도가 타겟 서버의 회선 속도보다          │
│           느리면 공격 실패. 방어자가 해커 IP 차단하면 끝.       │
│                                                                 │
│  [현대적 DDoS (N:1 분산 공격 아키텍처)]                         │
│                                                                 │
│                    ┌─ 좀비 PC (Bot) ──┐                         │
│  해커 (Attacker)   ├─ IP 카메라 (Bot) ─┤                        │
│        │           ├─ 홈 공유기 (Bot) ─┤                        │
│     (명령 하달)     ├─ 좀비 PC (Bot) ──┤                        │
│        ▼           └─ 봇넷 군단 수만 대 ┘                       │
│  C&C 서버 ───────────────┘       │                              │
│  (Command & Control)                 ▼                          │
│                           (( 수십 Tbps 트래픽 폭풍 ))           │
│                                      ▼                          │
│                                  타겟 서버 및 전체 네트워크 다운│
└─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 아키텍처 다이어그램은 DoS에서 DDoS로의 패러다임 전환이 갖는 파괴력의 차이를 직관적으로 보여준다. 1:1 DoS는 복싱 시합처럼 체급([대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)) 차이에 의해 승패가 결정되지만, DDoS는 해커가 C&C(명령 제어) 서버를 통해 전 세계에 퍼져 있는 취약한 단말(좀비 [봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/))에 공격 명령을 하달하는 구조다. 따라서 해커 자신의 위치나 IP는 완벽히 숨겨지며, 좀비 단말들이 제각각 정상적인 IP로 위장하여 동시다발적으로 트래픽을 쏘아대므로 단순한 IP 차단 방식([ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)) [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)은 수만 개의 룰을 처리하다 CPU 자원이 고갈되어 스스로 뻗어버리는 치명적인 결과를 낳는다.

- **📢 섹션 요약 비유**: 한 명의 진상 손님(DoS)이 매대에서 계산을 방해하는 것은 경비원을 불러 끌어내면 되지만, 수만 명의 가짜 손님(DDoS [봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/))이 백화점 출입구를 동시에 막아버리면 진짜 손님은 아예 들어가지도 못하고 건물 전체가 마비되는 것과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 공격 유형별 구성 요소 및 타겟 지점

DDoS 공격은 공격이 타겟으로 삼는 OSI 7계층 지점에 따라 크게 세 가지 부류로 나뉜다.

| [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) (OSI 계층) | 주요 공격 기법 | 고갈시키는 자원 | 동작 원리 / 비유 |
|:---|:---|:---|:---|
| **L3/L4 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 고갈형** ([Volume](/knowledge-base/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/) Based) | [UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) Flooding, [ICMP](/knowledge-base/studynote/03_network/06_network_layer_ip/318_icmp_internet_control_message_protocol_diagnostics/) Flooding | 인터넷 회선 용량 ([Bandwidth](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)), 라우터 PPS 처리 한계 | 엄청난 양의 소포(패킷)를 우체국 도로에 쏟아부어 도로 자체를 마비시킴 |
| **L3/L4 상태 고갈형** ([Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) / [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)) | [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) SYN Flooding, Smurf Attack | [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 테이블, OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 백로그 큐 (Backlog [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/)) | 식당 예약을 수만 개 걸어놓고(SYN) 나타나지 않아, 진짜 손님을 받지 못하게 테이블을 고갈시킴 |
| **L7 애플리케이션형** (App Layer) | [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) GET Flooding, [Slowloris](/knowledge-base/studynote/09_security/03_network_security/258_slowloris/) | 서버 CPU, 메모리, DB 커넥션 풀, 웹 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 워커 | 한 명이 주문 카운터에 가서 동전으로 계산하며 시간을 질질 끌어(Slow) 뒷사람을 못 받게 함 |

### 심층 동작 원리: [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) SYN Flooding과 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 고갈

L4 계층의 가장 대표적이고 고질적인 공격인 **SYN Flooding**은 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 프로토콜의 '3-Way Handshake' 설계 취약점을 집요하게 파고든다.

```text
┌──────────────────────────────────────────────────────────────────┐
│      TCP 3-Way Handshake와 SYN Flooding 공격 커널 상태 변화      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [정상적인 TCP 연결 프로세스]                                    │
│  Client ──(1. SYN)──▶ Server (SYN_RECV 상태 전이)                │
│                        ※ 커널 Backlog Queue에 연결 정보 저장     │
│  Client ◀──(2. SYN-ACK)─ Server                                  │
│  Client ──(3. ACK)──▶ Server (ESTABLISHED 상태 전이)             │
│                        ※ Queue에서 제거하고 통신 시작            │
│                                                                  │
│  [TCP SYN Flooding 공격 흐름]                                    │
│  해커 ──(1. 가짜 IP SYN 1)──▶ Server [Queue 1 할당]              │
│  해커 ──(1. 가짜 IP SYN 2)──▶ Server [Queue 2 할당]              │
│  해커 ──(1. 가짜 IP SYN 3)──▶ Server [Queue 3 할당]              │
│       ... (1초에 수만 개 발생)                                   │
│                                                                  │
│  서버 응답 ◀──(2. SYN-ACK)─ 가짜 IP (존재하지 않거나 응답안함)   │
│                                                                  │
│  결과: 타겟 서버의 OS 커널 Backlog Queue(보류 중인 연결 대기열)가│
│        가득 차서 가용 한계에 도달 (Queue Full).                  │
│        이후 도달하는 정상 사용자의 진짜 SYN 요청은 커널 레벨에서 │
│        가차 없이 폐기(Drop)되어 접속이 거부됨 (가용성 파괴)      │
└──────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 구조도는 DDoS가 단순히 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 막는 것이 아니라, OS 내부의 논리적 자원을 어떻게 고갈시키는지를 정밀하게 보여준다. 서버 OS(리눅스/윈도우)는 `SYN` 요청을 받으면 클라이언트가 `ACK`로 응답할 때까지 해당 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 정보를 메모리의 '백로그 큐(Backlog [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/))'에 유지한다. 해커는 출발지 IP를 조작([Spoofing](/knowledge-base/studynote/02_operating_system/10_security/598_spoofing/))한 대량의 SYN 패킷만 던지고 사라진다. 서버는 가짜 주소로 SYN-ACK를 보내고 하염없이 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)([Timeout](/knowledge-base/studynote/02_operating_system/05_deadlock/319_timeout_prevention/))이 날 때까지 큐 공간을 비우지 못한다. 순식간에 큐 용량(예: 1024~4096개)이 꽉 차버리면, OS는 큐를 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)하기 위해 새롭게 들어오는 모든 통신 요청(진짜 고객의 접근)을 버려버린다. 네트워크 회선(10Gbps)은 텅텅 비어있음에도 불구하고, 서버는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 불가(DoS) 상태에 빠지는 것이다.

- **📢 섹션 요약 비유**: 가짜 번호로 짜장면 100그릇을 배달 주문(SYN)해놓고 잠적해버리면, 중국집 주방([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 큐)은 가짜 요리를 만드느라 꽉 차서 정작 가게를 찾아온 진짜 손님의 주문은 하나도 받지 못하는 원리입니다.

---

## Ⅲ. 비교 및 연결

### 반사 증폭(Reflection Amplification) 공격 (DRDoS) 분석

단순한 [봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) DDoS를 넘어, 가장 파괴적인 위력을 자랑하는 기법이 바로 **[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 반사 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 거부 (DRDoS, Distributed Reflection DoS)** 공격이다. 이는 [스푸핑](/knowledge-base/studynote/02_operating_system/10_security/598_spoofing/)([Spoofing](/knowledge-base/studynote/02_operating_system/10_security/598_spoofing/))과 네트워크 프로토콜의 증폭(Amplification) 배율을 완벽히 융합한 천재적이고 악랄한 기법이다.

| 비교 항목 | 전통적 [Botnet](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) DDoS | DRDoS (증폭 반사 공격) |
|:---|:---|:---|
| **트래픽 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 주체** | 해커가 감염시킨 봇(좀비 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)) | 인터넷상의 정상적인 오픈 서버([DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/), [NTP](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/536_ntp_network_time_protocol_stratum/), Memcached 등) |
| **공격 메커니즘** | 봇들이 직접 타겟으로 트래픽 발송 | 출발지 IP를 '타겟 IP'로 [스푸핑](/knowledge-base/studynote/02_operating_system/10_security/598_spoofing/)하여 정상 서버에 요청 전송 |
| **증폭 효과 (Amplification)** | 1:1 (요청한 만큼 트래픽 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)) | 적게는 50배 ([DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/))에서 많게는 51,000배 (Memcached)로 증폭 |
| **은닉성 및 방어 난이도** | [봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) IP 차단으로 부분적 방어 가능 | 전 세계의 정상적인 대형 서버에서 날아오므로 차단이 매우 어려움 |

DRDoS의 가공할 파괴력을 수치적 증폭 계수로 시각화하면 다음과 같다.

```text
┌───────────────────────────────────────────────────────────────┐
│      DRDoS (NTP 증폭 반사 공격) 트래픽 폭증 메커니즘          │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  [1단계: 질의 변조 및 스푸핑]                                 │
│  해커 ──(64 Bytes 작은 요청)──▶ 정상적인 NTP 서버             │
│         출발지 IP: 타겟의 IP (스푸핑)                         │
│         명령어: `monlist` (서버의 최근 접속자 600명 목록 요청)│
│                                                               │
│  [2단계: 반사 및 증폭 (Reflection & Amplification)]           │
│  NTP 서버는 받은 요청이 진짜 '타겟'이 보낸 줄 앎              │
│  NTP 서버 내부에 저장된 거대한 결과값(수십 개의 패킷) 생성    │
│                                                               │
│  [3단계: 거대 트래픽 직격]                                    │
│  정상 NTP 서버 ━━━━(3,000 Bytes 응답)━━━━▶ 타겟 서버 피해자   │
│                 (약 500배 증폭되어 쏟아짐!)                   │
│                                                               │
│  결과: 해커가 10Mbps 대역폭만으로 공격해도,                   │
│        타겟 서버에는 5Gbps(500배)의 괴물 트래픽이 꽂히게 됨.  │
└───────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 다이어그램은 DRDoS가 왜 "핵무기급" 공격인지 설명한다. [UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 프로토콜은 핸드쉐이크가 없어 IP [스푸핑](/knowledge-base/studynote/02_operating_system/10_security/598_spoofing/)이 자유롭다. 해커는 인터넷에 열려있는 무고한 [NTP](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/536_ntp_network_time_protocol_stratum/)(시간 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)) 서버나 [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 서버들에게 64바이트짜리 깃털같이 가벼운 질의를 던지되, 응답받을 주소를 공격 목표(Target)의 IP로 속인다. 특히 `monlist` 같은 특수 명령어는 결과값이 원본 요청보다 수백 배 거대하다(증폭). 결과적으로 해커의 작은 움직임이 거대한 쓰나미로 증폭되어(Amplification) 타겟에게 반사(Reflection)된다. 이 공격 트래픽은 글로벌 대기업의 정상 서버 IP를 달고 오기 때문에, 방어자는 섣불리 해당 IP를 차단(Blacklist)할 수도 없는 진퇴양난에 빠진다.

- **📢 섹션 요약 비유**: 해커가 피자집, 치킨집, 족발집 수십 군데에 전화를 걸어 "주소는 타겟 빌딩 1층이고 한 군데당 100인분씩 배달해주세요"라고 거짓 주문(반사 및 증폭)을 넣어서, 타겟 빌딩 앞을 수천 대의 오토바이로 마비시키는 교활한 전술입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: L7 애플리케이션 공격 ([Slowloris](/knowledge-base/studynote/09_security/03_network_security/258_slowloris/)) 방어 설계

1. **상황 (L7 핀포인트 공격)**: 대규모 트래픽 증가 현상(Flooding)이 전혀 없는데도 웹 서버(Apache)가 계속해서 먹통이 되며 "503 [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Unavailable" 에러를 뿜어낸다. 네트워크 차원의 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)이나 라우터 CPU 상태는 매우 정상적이다.
2. **원인 분석 ([Slowloris](/knowledge-base/studynote/09_security/03_network_security/258_slowloris/) 공격)**: 해커가 정상적인 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 연결을 맺은 뒤, [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 헤더의 마지막 끝맺음 기호인 `\r\n\r\n`을 일부러 보내지 않고, 10초에 한 번씩 쓸데없는 X-Header 한 줄만 전송하며 연결을 지연시키고 있다. 아파치 워커(Worker) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 헤더가 완료되기를 기다리며 연결을 계속 물고 있다가, [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 가용 풀(MaxClients)이 순식간에 고갈되어 버린 것이다. (소량의 트래픽으로 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 마비 달성).
3. **아키텍처 및 OS 방어 결단**:
   - **[이벤트 루프](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/)([Event Loop](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/)) 웹서버로의 교체**: 1커넥션 당 1스레드를 점유하는 아파치 구조 대신, 비동기 논블로킹 I/O (epoll/kqueue) 기반의 Nginx 서버로 앞단을 교체하여 수만 개의 껍데기 연결을 단일 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)로 무력화 처리한다.
   - **[타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)([Timeout](/knowledge-base/studynote/02_operating_system/05_deadlock/319_timeout_prevention/)) 튜닝**: OS 단의 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/[HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) [Timeout](/knowledge-base/studynote/02_operating_system/05_deadlock/319_timeout_prevention/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)(`client_header_timeout`, `client_body_timeout`)을 5초 이내로 극단적으로 짧게 줄여, 완전한 헤더를 제때 보내지 않는 좀비 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)을 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨에서 신속하게 Drop 시킨다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) ([클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) DDoS 완화 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))
현대 수 Tbps 급의 공격은 기업 내부 망([On-Premise](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)) [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)([IPS](/knowledge-base/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/)/[UTM](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/147_utm_unmanned_aircraft_system_traffic_management/)) 장비로는 절대 막아낼 수 없다. 트래픽이 회선 제공자([ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_information_strategy_planning_4_steps/)) 단에서 꽉 막히면 장비가 아무리 좋아도 "파이프가 막힌" 상태이기 때문이다.

- **OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 하드닝 ([Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) Tuning)**:
  - `net.ipv4.tcp_syncookies = 1` 활성화 (SYN Flooding 시 백로그 큐를 안 쓰고 [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/)로 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)).
  - `net.ipv4.tcp_max_syn_backlog` 크기 대폭 확장.
- **클라우드 트래픽 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) (Anycast & [Scrubbing Center](/knowledge-base/studynote/03_network/14_network_security_threats/721_drdos_scrubbing_center_mitigation/))**: AWS Shield, Cloudflare 등 글로벌 [스크러빙 센터](/knowledge-base/studynote/09_security/03_network_security/250_scrubbing_center/)([Scrubbing Center](/knowledge-base/studynote/03_network/14_network_security_threats/721_drdos_scrubbing_center_mitigation/))와 계약하여 [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) Anycast [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)을 적용했는가? (수백 Gbps 공격이 오면 트래픽을 글로벌 클라우드 망으로 우회 흡수시켜 더러운 패킷만 걸러내고 깨끗한 패킷만 본사로 전달하는 아키텍처 구축 필수).

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **인라인(Inline) 단일 장비 방어 맹신**: 수십 Gbps 회선 환경에서, L7 장비(WAF나 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)) 1대를 인라인으로 세워두고 DDoS를 막으려는 아키텍처. 엄청난 양의 볼륨 공격이 들어오면 패킷 검사(Inspection) 오버헤드 때문에 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) CPU 리소스가 먼저 100%를 치며, 스스로 전체망을 차단해 버리는 'Self-DoS' 현상을 유발한다.

- **📢 섹션 요약 비유**: 거대한 홍수(수 Tbps 트래픽)가 밀려오는데 집 대문 앞에 튼튼한 방패 하나(단일 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 장비)를 둔다고 막을 수 없습니다. 물결을 수만 갈래 수로로 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)시키고 정수장([스크러빙 센터](/knowledge-base/studynote/09_security/03_network_security/250_scrubbing_center/))을 통과하게 만드는 도시 차원의 거대한 치수 공사가 필요합니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과 (융합형 Anti-DDoS 아키텍처 도입 시)

| 구분 | [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 단일 방어 한계 | 클라우드 + OS 튜닝 융합 방어 시 | 기술적 함의 |
|:---|:---|:---|:---|
| **[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) (Uptime)** | 10Gbps 이상 공격 시 회선 장애 (100% 다운) | **무제한 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 풀** 기반 99.99% 연속성 유지 | 비즈니스 손실액 및 평판 저하 원천 봉쇄 |
| **[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 자원 (OS)** | [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 1만 개 누적 시 [커널 패닉](/knowledge-base/studynote/02_operating_system/01_overview_architecture/036_kernel_panic/) / 연결 거부 | SYN [Cookie](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) 및 [WAF](/knowledge-base/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/) 엣지 커팅으로 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) | 백엔드 서버는 오직 '정제된' 진짜 트래픽만 처리 |
| **운영 (Ops)** | 보안 담당자가 수동으로 IP [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) 수천 개 등록 작업 | ML 알고리즘이 L7 볼륨 [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) 후 자동 룰 적용 | 방어 레이턴시 [제로화](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/784_zeroization_circuit/) 및 휴먼 에러 방지 |

### 미래 전망
[IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 기기의 폭발적 증가(IP 카메라, 스마트 냉장고 등)와 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 통신망의 보급은 해커들에게 더 거대하고 빠른 [봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) 무기고를 제공하고 있다. 미라이(Mirai) [봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) 류의 소스코드 공개로 누구나 테라비트(Tbps)급 공격을 할 수 있는 시대다. 이에 맞서 방어자들은 **[eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 기반의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 패킷 필터링([XDP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/670_xdp/))** 기술을 발전시키고 있다. 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 네트워크 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 깊숙한 곳까지 가기 전에(네트워크 카드 드라이버 단계에서), 규칙에 맞지 않는 DDoS 패킷을 초당 수천만 개씩 시스템 콜 오버헤드 없이 즉각 파기(Drop)하는 선언적 프로그램 기술이 미래의 DDoS 최전선 방패막이가 될 것이다.

### 참고 표준
- **RFC 4987**: [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) SYN Flooding 대응 가이드라인 (SYN Cookies 메커니즘)
- **RFC 5635**: [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) Blackholing ([라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 기반 공격 트래픽 흡수 표준)
- **KISA DDoS 대응 가이드**: [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/), 애플리케이션 계층별 모범 완화 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)

- **📢 섹션 요약 비유**: 해커가 아무리 많은 좀비 군단을 이끌고 물량 공세(DDoS)를 펼치더라도, 우리는 거대한 클라우드 방어막(거름망)과 똑똑한 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)([XDP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/670_xdp/) 자동문)을 통해 더러운 흙탕물은 바다로 흘려보내고 깨끗한 식수만 집 안으로 들여보낼 수 있게 진화하고 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [제로 데이](/knowledge-base/studynote/02_operating_system/10_security/597_zero_day_exploit/) ([Zero-Day](/knowledge-base/studynote/02_operating_system/10_security/597_zero_day_exploit/)) 취약점 / 익스플로잇 (Exploit) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [스푸핑](/knowledge-base/studynote/02_operating_system/10_security/598_spoofing/) ([Spoofing](/knowledge-base/studynote/02_operating_system/10_security/598_spoofing/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [포트 스캐닝](/knowledge-base/studynote/02_operating_system/10_security/600_port_scanning/) ([Port Scanning](/knowledge-base/studynote/02_operating_system/10_security/600_port_scanning/)) 도구 원리 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [침입 탐지 시스템](/knowledge-base/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/) ([IDS](/knowledge-base/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/)) / 침입 방지 시스템 ([IPS](/knowledge-base/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/)) 시스템 콜 트레이싱 기반 [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[스푸핑 (Spoofing)]
    │
    ▼
[서비스 거부 (DoS) 및 분산 서비스 거부 (DDoS) 네트워크 자원 고갈 공격]
    │
    ├──▶ [포트 스캐닝 (Port Scanning) 도구 원리]
    └──▶ [침입 탐지 시스템 (IDS) / 침입 방지 시스템 (IPS) 시스템 콜 트레이싱 기반 이상 탐지]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 내가 혼자서 문구점 카운터에 백 원짜리 동전 수천 개를 내밀며 계산을 일부러 질질 끌면 다른 친구들이 물건을 못 사게 되는데, 이게 **DoS 공격([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 거부)** 이에요.
2. 해커가 전 세계 수만 명의 악당 친구들([봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/))을 동시에 동원해서 문구점 문 앞을 완전히 가로막아 꼼짝도 못하게 만드는 게 바로 **DDoS 공격**이랍니다.
3. 이를 막기 위해 문구점 사장님은 입구를 여러 동네(클라우드 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/))에 나눠서 만들고, 가짜 돈을 내는 사람들은 입구 경비원(SYN [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/)/[WAF](/knowledge-base/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/))이 바로바로 쫓아내게 만들었어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 599 / 800

← **이전**: [598. 스푸핑 (Spoofing) - IP/MAC 등 신분 위장](/knowledge-base/studynote/02_operating_system/10_security/598_spoofing/)
**다음**: [600. 포트 스캐닝 (Port Scanning) 도구 원리](/knowledge-base/studynote/02_operating_system/10_security/600_port_scanning/) →

---
