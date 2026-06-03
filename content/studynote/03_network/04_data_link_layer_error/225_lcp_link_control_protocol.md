---
title: 225. LCP (Link Control Protocol)
date: '2026-05-08'
tags:
- studynote-network
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LCP는 [[001_dikw_pyramid|데이터]] 링크 계층에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: LCP를 이해하면 오류율과 재전송 비용 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: LCP (Link Control [[295_protocol_field_tcp_udp_icmp|Protocol]])는 점대점 통신에서 양단의 노드가 실제 [[001_dikw_pyramid|데이터]]를 주고받기 전에, [[001_dikw_pyramid|데이터]] 링크 계층의 통신 파라미터를 협상하고 링크의 품질을 모니터링하는 [[295_protocol_field_tcp_udp_icmp|프로토콜]]이다.
- **필요성**: 두 개의 통신 장비(예: 내 PC의 모뎀과 통신사의 서버)는 서로 하드웨어 성능과 지원하는 기능이 다르다. 한쪽은 한 번에 1500바이트를 받을 수 있지만 다른 쪽은 1000바이트만 받을 수 있다면 [[001_dikw_pyramid|데이터]]가 깨지게 된다. 따라서 본격적인 통신(네트워크 연결)을 시작하기 전에 양쪽 장비가 서로의 능력을 파악하고 "우리는 이런 규칙으로 통신하자"고 합의를 보는 절차가 반드시 필요했다.
- **비유**: LCP는 두 나라의 정상이 회담을 시작하기 전에 양국 실무진이 만나 "통역사는 누구로 할지([[303_authentication_authorization_patterns|인증]] 방식)", "회의 시간은 몇 분으로 할지(MRU)" 등 회담의 룰(규칙)을 미리 맞추는 사전 조율 과정과 같다.
- **발전 과정**: 과거 SLIP 같은 [[459_quic_fec_forward_error_correction|초기]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 이러한 사전 협상 과정이 없어 사용자가 수동으로 모든 [[009_config|설정]]을 맞춰야 했으나, PPP가 도입되면서 LCP를 통해 이 과정이 100% 자동화(Plug and Play)되었다.

```text
  ┌─────────────────────────────────────────────────────────┐
  │                 LCP의 링크 수립 3단계                   │
  ├─────────────────────────────────────────────────────────┤
  │                                                         │
  │  [1. 링크 설정 협상 (Link Configuration)]               │
  │    A: "나는 MTU 1500, CHAP 인증 쓸게." (Configure-Req)  │
  │    B: "좋아, 동의해." (Configure-Ack)                   │
  │                                                         │
  │  [2. 링크 유지 및 품질 테스트 (Link Maintenance)]       │
  │    A: "연결 잘 되어 있지?" (Echo-Request)               │
  │    B: "응, 잘 들려." (Echo-Reply)                       │
  │                                                         │
  │  [3. 링크 종료 (Link Termination)]                      │
  │    A: "이제 연결 끊을게." (Terminate-Req)               │
  │    B: "알았어, 끊자." (Terminate-Ack)                   │
  └─────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: LCP는 본격적인 스포츠 경기를 시작하기 전에 심판과 양 팀 주장이 모여 경기장의 크기(프레임 크기)와 반칙 규정([[303_authentication_authorization_patterns|인증]] 방식)을 합의하는 경기 전 룰미팅(Rule Meeting)입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### LCP 프레임 구조와 패킷 유형

LCP 프레임은 PPP의 페이로드(Payload) 영역 안에 담겨 전송된다. [[295_protocol_field_tcp_udp_icmp|프로토콜]] 필드 값이 `0xC021`일 때 해당 프레임이 LCP 패킷임을 의미한다.

| LCP 코드 | 패킷 이름 | 역할 및 내부 동작 |
|:---|:---|:---|
| **0x01** | Configure-Request | 내가 원하는 통신 옵션을 상대방에게 제안함 |
| **0x02** | Configure-Ack | 상대의 제안을 완벽히 수락함 (링크 [[009_config|설정]] 완료) |
| **0x03** | Configure-[[211_nak_negative_acknowledgement|Nak]] | 제안은 이해했지만 그 값(Value)은 변경해줘 (예: MTU를 줄여줘) |
| **0x04** | Configure-Reject | 그 옵션 자체를 난 지원하지 않아 (예: [[228_chap_challenge_handshake_authentication_protocol|CHAP]] [[303_authentication_authorization_patterns|인증]] 못함) |
| **0x09/0x0A** | Echo-Req / Reply | 링크가 정상적으로 살아있는지 [[396_validation|확인]] (Keep-alive) |
| **0x05/0x06** | Terminate-Req / Ack | 정상적인 링크 종료 절차 |

### 주요 협상 옵션 (Configuration Options)

LCP가 협상하는 가장 중요한 3가지 파라미터는 다음과 같다.

1. **MRU (Maximum Receive Unit)**: 내가 수신할 수 있는 최대 프레임 크기 (기본값 1500 [[074_byte|바이트]]). MTU([[292_packet_encapsulation_mtu_ethernet_1500_bytes|Maximum Transmission Unit]])의 수신 관점 용어다.
2. **[[604_authentication_factors|Authentication]] [[295_protocol_field_tcp_udp_icmp|Protocol]]**: 통신을 허락하기 전 어떤 방식으로 신원을 [[396_validation|확인]]할지 결정 ([[227_pap_password_authentication_protocol|PAP]] 또는 [[228_chap_challenge_handshake_authentication_protocol|CHAP]] 등).
3. **[[503_magic_number_file_signature|Magic Number]]**: 루프백(Loopback, 내가 보낸 신호가 나에게 다시 돌아오는 현상)을 감지하기 위한 랜덤 숫자. 양쪽이 서로 다른 [[503_magic_number_file_signature|매직 넘버]]를 생성하여, 내가 보낸 [[503_magic_number_file_signature|매직 넘버]]가 그대로 돌아오면 회선이 꼬였음(Loop)을 즉각 인지한다.

```text
  ┌───────────────────────────────────────────────────────────────┐
  │                 LCP의 Magic Number 루프백 감지 원리             │
  ├───────────────────────────────────────────────────────────────┤
  │                                                               │
  │  [정상 상태]                                                  │
  │   라우터 A (Magic: 1234) ─────(Req 1234)─────▶ 라우터 B        │
  │                          ◀────(Req 5678)─────  (Magic: 5678)  │
  │   * A는 5678을 받고 "정상적인 상대방이구나" 판단              │
  │                                                               │
  │  [루프백(선로 꼬임) 발생 상태]                                │
  │   라우터 A (Magic: 1234) ─────(Req 1234)──┐                  │
  │                          ◀────(Req 1234)──┘ 회선 꼬임         │
  │   * A는 1234를 다시 받고 "내 신호가 돌아왔네! 회선 오류다!"   │
  │     즉시 링크 차단!                                           │
  └───────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 전화선이나 시리얼 케이블을 연결할 때 물리적인 결함으로 송신선(TX)과 수신선(RX)이 브릿지되어 내가 보낸 신호를 내가 다시 받는 루프 현상이 자주 발생했다. LCP는 난수([[503_magic_number_file_signature|Magic Number]])를 서로 교환하는 아주 단순한 방법으로 이 치명적인 물리적 장애를 소프트웨어적으로 즉각 감지하고 연결을 차단한다.

- **📢 섹션 요약 비유**: 통화를 시작할 때 서로 "여보세요? 나 홍길동인데, 너 누구니?"라고 먼저 [[396_validation|확인]]하여, 혼선으로 인해 메아리(내 목소리가 돌아옴)가 들리는지 체크하는 똑똑한 통화 연결 과정입니다.

---

## Ⅲ. 비교 및 연결

| 비교 항목 | LCP (Link Control [[295_protocol_field_tcp_udp_icmp|Protocol]]) | [[226_ncp_network_control_protocol|NCP]] ([[226_ncp_network_control_protocol|Network Control Protocol]]) |
|:---|:---|:---|
| **역할** | '물리적/[[001_dikw_pyramid|데이터]] 링크'의 룰 협상 및 유지 | '네트워크 계층(IP 등)'의 환경 [[009_config|설정]] |
| **실행 순서** | [[224_ppp_point_to_point_protocol|PPP]] 연결의 가장 첫 단계 (가장 먼저 실행) | LCP와 [[303_authentication_authorization_patterns|인증]]이 완료된 후에만 실행 |
| **협상 내용** | MRU(프레임 크기), [[303_authentication_authorization_patterns|인증]] 방식([[227_pap_password_authentication_protocol|PAP]]/[[228_chap_challenge_handshake_authentication_protocol|CHAP]]) | IP 주소, [[511_dns_hierarchical_distributed_architecture|DNS]] 서버 주소 등 (IPCP) |
| **비유** | 도로 포장 및 차선 규격 합의 | 어느 차([[286_ipv4_internet_protocol_version_4_rfc_791|IPv4]], [[324_ipv6_128bit_next_generation_address|IPv6]])가 다닐지 번호판 발급 |

LCP는 도로의 폭(MRU)과 통행증 검사 방식([[303_authentication_authorization_patterns|인증]])을 정하고, 이것이 완료되어 톨게이트를 통과해야만 NCP가 작동하여 차량 번호판(IP 주소)을 달아주는 철저한 분업 구조다.

- **📢 섹션 요약 비유**: LCP는 건물의 기초 공사와 배관(인프라)을 점검하는 작업이고, NCP는 그 배관 위에서 어떤 종류의 물(IP, IPX)을 흐르게 할지 수도꼭지를 달아주는 작업입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

ADSL 모뎀을 통해 인터넷에 연결할 때, 간혹 "PPPoE 연결 중 [[303_authentication_authorization_patterns|인증]] 실패" 또는 "MTU 사이즈 문제로 특정 웹사이트 접속 불가" 장애가 발생한다. 이는 모두 LCP 협상 단계에서의 실패다. 통신사 라우터는 MTU 1492를 요구(Configure-Req)했는데, 홈 공유기가 고집스럽게 1500을 요구하면 서로 `Configure-Nak`만 주고받다가 LCP 연결이 [[319_timeout_prevention|Timeout]] 되어 인터넷이 아예 연결되지 않는다. 이때 엔지니어는 공유기 [[009_config|설정]]에서 MTU를 수동으로 맞춰주어 LCP 협상을 통과시켜야 한다.

- **트러블슈팅의 시작점**: [[224_ppp_point_to_point_protocol|PPP]] 기반의 통신 장애([[983_vpn_virtual_private_network|VPN]], PPPoE 등)가 발생했을 때 핑(Ping) 테스트를 하기 전에 가장 먼저 [[396_validation|확인]]해야 하는 [[568_logs_distributed_logging_elk_fluentd|로그]]가 바로 LCP 협상 [[568_logs_distributed_logging_elk_fluentd|로그]](LCP Negotiation)다.
- **[[128_water_scrum_fall_anti_pattern|안티패턴]]**: 보안 장비([[690_firewall_generation_evolution|방화벽]])에서 무조건적인 [[318_icmp_internet_control_message_protocol_diagnostics|ICMP]] 차단 [[009_config|설정]]을 하듯, LCP의 `Echo-Request`를 차단하도록 [[009_config|설정]]하면, 링크 양단은 상대방이 죽었다고 판단하여 수시로 연결을 끊어버리는(Flapping) 대참사가 발생한다. LCP 제어 패킷은 절대 필터링해서는 안 된다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 서로 언어가 다른 두 사람이 대화할 때 "영어로 합시다"라고 합의(LCP)하는 과정이 계속 실패하면, 아예 본론([[226_ncp_network_control_protocol|NCP]])은 꺼내지도 못하고 전화가 끊어지는 것과 같습니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | 내용 | 개선 효과 |
|:---|:---|:---|
| **정량** | [[503_magic_number_file_signature|Magic Number]] 기반 루프백 감지 | [[1097_broadcast_storm_switching_loop_stp|브로드캐스트 스톰]] 및 [[339_routing_overview_best_path_selection|라우팅]] 루프 방지, CPU 부하 0% 수렴 |
| **정성** | 플러그 앤 플레이 지원 | 서로 다른 벤더([[539_netflow_sflow_traffic_monitoring|Cisco]], Juniper 등) 장비 간의 완벽한 상호 [[344_compatibility_usability|호환성]] 확보 |

LCP는 단순한 [[001_dikw_pyramid|데이터]] 전송 [[295_protocol_field_tcp_udp_icmp|프로토콜]]([[216_hdlc_high_level_data_link_control|HDLC]])에 '지능적 협상'이라는 생명력을 불어넣은 혁신적인 메커니즘이다. 비록 전화선 기반의 통신은 사라졌지만, LCP가 확립한 'Configure-Request → Ack/[[211_nak_negative_acknowledgement|Nak]]'의 우아한 3단계 상태 머신과 [[503_magic_number_file_signature|매직 넘버]] 기반의 오류 감지 기술은 오늘날 [[589_ipsec_offload|IPsec]], [[283_ssl_vpn|SSL VPN]] 등 수많은 현대 [[377_tunneling_mechanism_overview|터널링]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]의 [[459_quic_fec_forward_error_correction|초기]] 연결(Handshake) 디자인에 영원한 교과서로 남아있다. 향후에는 고신뢰 저지연 링크 제어 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: 과거 LCP가 작성한 '통신 협상 매뉴얼'은 너무나 완벽해서, 통신 매체가 구리선에서 광케이블과 무선으로 바뀐 현대에도 여전히 그 뼈대 그대로 사용되고 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[224_ppp_point_to_point_protocol|PPP]] | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [[184_framing_mechanism|프레이밍]] ([[184_framing_mechanism|Framing]]) | 비트열을 의미 있는 전송 단위로 구분한다. |
| [[188_error_control_overview|오류 제어]] ([[188_error_control_overview|Error Control]]) | 검출과 [[658_ir_recovery|복구]] 정책을 함께 설계해야 한다. |
| [[226_ncp_network_control_protocol|NCP]] | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: PPP]
    │
    ▼
[현재 개념: LCP]
    │
    ├──▶ [확장 A: NCP]
    └──▶ [확장 B: 고신뢰 저지연 링크 제어]
```

LCP는 PPP에서 출발해 현재 메커니즘을 정교화하고, 이후 NCP와 고신뢰 저지연 링크 제어 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 편지를 보낼 때 봉투를 제대로 닫고 틀린 글자가 없는지 [[396_validation|확인]]해야 해요.
2. 이 개념은 편지가 깨지거나 사라졌을 때 다시 보내는 규칙까지 정해줘요.
3. 그래서 중간에 흔들려도 중요한 내용이 더 안전하게 도착해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 346 / 1120

← **이전**: [[224_ppp_point_to_point_protocol|224. PPP (Point-to-Point Protocol)]]
**다음**: [[226_ncp_network_control_protocol|226. NCP (Network Control Protocol)]] →

---
