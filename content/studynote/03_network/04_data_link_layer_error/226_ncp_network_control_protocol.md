+++
title = "226. NCP (Network Control Protocol)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NCP (Network Control [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))는 [PPP](/knowledge-base/studynote/03_network/04_data_link_layer_error/224_ppp_point_to_point_protocol/) ([Point-to-Point Protocol](/knowledge-base/studynote/03_network/04_data_link_layer_error/224_ppp_point_to_point_protocol/)) 연결의 마지막 단계에서, IP나 IPX 등 상위 네트워크 계층 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 협상하고 동적으로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하기 위한 제어 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 집합이다.
> 2. **가치**: LCP가 물리적 링크를 구성하고 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 마친 후, NCP(예: IPCP)가 IP 주소를 할당하고 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 정보를 교환함으로써 비로소 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 패킷이 전송될 수 있는 완벽한 통신 환경을 구축한다.
> 3. **판단 포인트**: 다양한 네트워크 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)([IPv4](/knowledge-base/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/), [IPv6](/knowledge-base/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/), AppleTalk 등)을 단일 [PPP](/knowledge-base/studynote/03_network/04_data_link_layer_error/224_ppp_point_to_point_protocol/) 링크 위에서 동시에 다중화하여 전송할 수 있게 해주는 모듈식 아키텍처의 핵심 요소다.

---

## Ⅰ. 개요 및 필요성

- **개념**: NCP (Network Control [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층(Layer 2) 통신 규약인 [PPP](/knowledge-base/studynote/03_network/04_data_link_layer_error/224_ppp_point_to_point_protocol/) 내에서, 상위 3계층 네트워크 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 초기화하고 협상하기 위해 사용되는 하위 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)들의 총칭이다. IP용으로는 IPCP (IP Control [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)), IPv6용으로는 IPv6CP가 사용된다.

- **필요성**: 두 노드 간 물리적 연결이 완료되고([LCP](/knowledge-base/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/) 단계) 사용자가 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)되었다고 해서 곧바로 인터넷이 되는 것은 아니다. 서로 통신하려면 양단이 IP 주소를 가져야 하고, 헤더 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 여부 등을 맞춰야 한다. NCP는 이러한 상위 네트워크 논리적 구성을 전담하여 링크를 실사용 가능한 상태로 만든다.

- **💡 비유**: 고속도로(물리적 링크)가 깔리고 톨게이트 요금 정산([LCP](/knowledge-base/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/)/[인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))이 끝났다고 차가 달릴 수 있는 것은 아닙니다. NCP는 각 차량에 <strong>"차량 번호판(IP 주소)"을 발급하고 "내비게이션 경로(<a href="/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a> <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a>)"를 세팅</strong>해 주어 차가 올바르게 주행할 수 있게 해주는 차량 등록 사업소와 같습니다.

```text
[LCP]
    |
    v
[NCP]
    |
    +---> [PAP]
```

- **📢 섹션 요약 비유**: <strong> NCP는 아파트 입주 시 계약(<a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/">LCP</a>)을 마친 후, 실제로 전구에 불이 들어오게 하려고 </strong>"전기/수도/[가스](/knowledge-base/studynote/06_ict_convergence/01_blockchain/024_gas/)(IP, [IPv6](/knowledge-base/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/))를 개통하는 마지막 행정 절차"**입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

NCP는 프레임 단위의 전달, 오류 검출, 재전송 제어를 다루는 축라는 관점에서 이해해야 한다. LCP와 [PAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/227_pap_password_authentication_protocol/) 사이의 연결점으로 놓고 보면 개념의 역할이 더 분명해진다.

```text
[LCP]
    |
    v
[NCP]
    |
    +---> [PAP]
```

- **📢 섹션 요약 비유**: NCP의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

[PPP](/knowledge-base/studynote/03_network/04_data_link_layer_error/224_ppp_point_to_point_protocol/) 연결은 크게 세 단계를 거친다.
1. <strong><a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/">LCP</a> (<a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/">Link Control Protocol</a>)</strong>: 링크 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), MTU 협상, 루프백 탐지.
2. <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a> 단계 (선택)</strong>: [PAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/227_pap_password_authentication_protocol/), [CHAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/228_chap_challenge_handshake_authentication_protocol/) 등을 통한 사용자 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/).
3. <strong>NCP (Network Control <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">Protocol</a>)</strong>: 네트워크 계층 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) (IP 주소 등 할당). 이 단계가 성공해야 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)그램이 교환된다.

```text
 +-------------------------------------------------------------+
 |                     PPP 연결 상태 천이도                    |
 +-------------------------------------------------------------+
 |                                                             |
 |   [Dead] ----(물리적 연결)----> [Establish]                  |
 |                                    |  (LCP 협상 진행)       |
 |                                    v                        |
 |  +--------------- [Authenticate] <--+                        |
 |  | (인증 실패)        |                                     |
 |  v                    v (인증 성공 또는 인증 없음)          |
 | [Terminate] <------- [Network]  (NCP 협상 진행)              |
 |                       |                                     |
 |                       v (IPCP 등 NCP 설정 완료)             |
 |                     [Open]  <---- 실제 IP 데이터 전송 상태!  |
 |                                                             |
 +-------------------------------------------------------------+
```

### 2. IPCP (IP Control [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)) 동작 방식
가장 대표적인 NCP인 IPCP(RFC 1332)의 주요 기능은 다음과 같다.
- **IP 주소 할당**: 다이얼업이나 PPPoE 연결 시 [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/) 서버가 클라이언트에게 동적 IP를 부여한다.
- <strong>헤더 <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a> 협상</strong>: Van Jacobson [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/IP 헤더 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 등을 사용할지 협상하여 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 효율을 높인다.

### 3. 멀티프로토콜 지원 ([Multiplexing](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/))
NCP 덕분에 PPP는 하나의 시리얼 라인 위에서 IP, [IPv6](/knowledge-base/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/), IPX [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)그램을 섞어서 전송할 수 있다. 프레임의 `Protocol` 필드를 통해 수신 측이 이를 식별한다. (예: 0x8021은 IPCP, 0x0021은 IP [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))

- **📢 섹션 요약 비유**: <strong> NCP는 만능 어댑터입니다. 하나의 수도관(<a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/224_ppp_point_to_point_protocol/">PPP</a>)을 통해 수돗물(<a href="/knowledge-base/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/">IPv4</a>), 정수기 물(<a href="/knowledge-base/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/">IPv6</a>), 온수(IPX) 등 다양한 액체를 문제없이 동시에 흘려보낼 수 있도록 </strong>"각 액체에 맞는 전용 밸브(IPCP, IPv6CP)를 달아주는 역할"**을 합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 NCP를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [LCP](/knowledge-base/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/) 수준의 기본 대책으로 충분한지, 아니면 NCP가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 PAP와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 오류율 부족인지, 재전송 비용 악화인지 먼저 분리한다.
2. NCP가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 PAP와의 연계 방식을 함께 검증한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- NCP의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- LCP와의 경계를 정리하지 않아 중복 투자나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: NCP를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

NCP는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 오류율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [PAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/227_pap_password_authentication_protocol/), 고신뢰 저지연 링크 제어, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 고신뢰 저지연 링크 제어 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: NCP는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [LCP](/knowledge-base/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [프레이밍](/knowledge-base/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/) ([Framing](/knowledge-base/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/)) | 비트열을 의미 있는 전송 단위로 구분한다. |
| [오류 제어](/knowledge-base/studynote/03_network/04_data_link_layer_error/188_error_control_overview/) ([Error Control](/knowledge-base/studynote/03_network/04_data_link_layer_error/188_error_control_overview/)) | 검출과 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 함께 설계해야 한다. |
| [PAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/227_pap_password_authentication_protocol/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: LCP]
    |
    v
[현재 개념: NCP]
    |
    +---> [확장 A: PAP]
    +---> [확장 B: 고신뢰 저지연 링크 제어]
```

NCP는 LCP에서 출발해 현재 메커니즘을 정교화하고, 이후 PAP와 고신뢰 저지연 링크 제어 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 편지를 보낼 때 봉투를 제대로 닫고 틀린 글자가 없는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 해요.
2. 이 개념은 편지가 깨지거나 사라졌을 때 다시 보내는 규칙까지 정해줘요.
3. 그래서 중간에 흔들려도 중요한 내용이 더 안전하게 도착해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 347 / 1120

<- **이전**: [225. LCP (Link Control Protocol)](/knowledge-base/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/)
**다음**: [227. PAP (Password Authentication Protocol)](/knowledge-base/studynote/03_network/04_data_link_layer_error/227_pap_password_authentication_protocol/) ->

---
