+++
weight = 1085
title = "1085. IPsec IKEv2 터널 협상"
date = "2026-05-08"
[extra]
categories = "studynote-network"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[589_ipsec_offload|IPsec]] [[280_ikev2|IKEv2]] 터널 협상은 [[282_performance_tactics|성능]] 평가와 고급 분석에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [[589_ipsec_offload|IPsec]] [[280_ikev2|IKEv2]] 터널 협상을 이해하면 측정 정확도과 모델 적합성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- IPsec은 실제로 [[001_dikw_pyramid|데이터]]를 암호화해서 쏘는 트럭([[382_esp_encapsulating_security_payload_confidentiality|ESP]]/[[381_ah_authentication_header_integrity_auth|AH]])입니다.
- **[[383_ike_isakmp_sa_security_association|IKE]]**: 트럭이 달리기 전에 먼저 라우터 양쪽이 만나서 "우리 어떤 [[504_cryptography_algorithms_aes_rsa_sha|암호화 알고리즘]] 쓸래? 암호 키([[067_db_key_uniqueness_minimality|Key]])는 뭘로 할래?"라고 **규칙을 정하고 보안 터널([[767_sa_standalone_5g_core_network|SA]], [[283_security_tactics|Security]] Association)을 뚫어주는 '사전 협상 전문 외교관 [[295_protocol_field_tcp_udp_icmp|프로토콜]]'**입니다. ([[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 500번 사용)

```text
[다크 웹 Tor 통신 프로토콜 암호화층]
    │
    ▼
[IPsec IKEv2 터널 협상]
    │
    └──▶ [WireGuard 라우팅 고속망 체계]
```

- **📢 섹션 요약 비유**: [[589_ipsec_offload|IPsec]] [[280_ikev2|IKEv2]] 터널 협상은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [[170_selectivity_cardinality_distribution_tuning|선택도]] 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

- 통신을 너무 복잡하게 만들었습니다. 
- Main Mode(6번 핑퐁) 또는 Aggressive Mode(3번 핑퐁)로 1단계 터널을 뚫고, 다시 Quick Mode(3번 핑퐁)로 2단계 진짜 터널을 뚫는 미친 짓(최대 9번의 메시지 교환)을 하느라 CPU 오버헤드가 크고 연결이 느렸습니다.
- 모바일(스마트폰) 지원 기능이 아예 없었습니다.

```text
[다크 웹 Tor 통신 프로토콜 암호화층]
    │
    ▼
[IPsec IKEv2 터널 협상]
    │
    └──▶ [WireGuard 라우팅 고속망 체계]
```

- **📢 섹션 요약 비유**: [[589_ipsec_offload|IPsec]] [[280_ikev2|IKEv2]] 터널 협상의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

IETF에서 복잡한 걸 싹 다 갈아엎고 모바일 시대에 맞게 재창조했습니다.

### 1. 4-Way 핑퐁으로 [[148_5g_embb_urllc_mmtc|초고속]] [[347_compaction|압축]] (속도 향상)
- 9번 핑퐁 치던 걸 **단 4개의 메시지(2번의 왕복, 4-Way Handshake)**로 싹 다 욱여넣었습니다.
  - **IKE_SA_INIT (2번)**: "야 나랑 [[589_ipsec_offload|IPsec]] 할래? 우리 암호 방식 이거 쓰자!" (1단계 뼈대 터널 [[087_process_state_transition|생성]])
  - **IKE_AUTH (2번)**: "콜! 내 인증서(신분증) 여기 있어, 너도 인증서 내놔. 그리고 진짜 [[001_dikw_pyramid|데이터]] 터널(Child [[767_sa_standalone_5g_core_network|SA]])도 같이 바로 뚫자!" (신분 [[396_validation|확인]] + 2단계 진짜 터널 동시 [[087_process_state_transition|생성]])
- 협상이 빛의 속도로 끝나서 [[983_vpn_virtual_private_network|VPN]] 접속 버튼을 누르자마자 1초 만에 철컥 붙습니다.

### 2. MOBIKE ([[280_ikev2|IKEv2]] Mobility and Multihoming) 🌟 최강 무기 🌟
- **스마트폰 VPN의 구원자**입니다.
- KTX를 타고 폰으로 [[589_ipsec_offload|IPsec]] VPN을 켰습니다. 와이파이 존에서 IP가 `10.x.x.x` 였는데, [[752_lte_long_term_evolution_4g|LTE]] 기지국으로 넘어가면서 IP가 `11.x.x.x` 로 바뀌었습니다.
- [[279_ikev1|IKEv1]]: IP가 바뀌었으니 터널을 다 때려 부수고 1번부터 다시 협상(접속 끊김 발생).
- **MOBIKE 탑재 [[280_ikev2|IKEv2]]**: 폰이 서버한테 `UPDATE_SA_ADDRESSES` 패킷을 하나 툭 던집니다. "야! 나 터널 그대로 둔 채 내 IP만 11번으로 바뀌었으니까 장부 수정만 해!" 서버가 오케이 하면 **화상 회의가 단 1초도 끊기지 않고 부드럽게(Seamless) [[983_vpn_virtual_private_network|VPN]] 터널이 유지됩니다.**

### 3. 디도스(DDoS) 방어: [[475_cookie_local_state|쿠키]]([[475_cookie_local_state|Cookie]]) 챌린지
- 해커가 가짜 IP로 1단계(INIT) 요청만 100만 번 쏴서 [[983_vpn_virtual_private_network|VPN]] 라우터의 메모리를 터뜨리는 공격을 막습니다.
- 의심스러우면 라우터가 `Cookie` 퀴즈를 던지고, "너 진짜 살아있는 놈이면 이 [[475_cookie_local_state|쿠키]] 값 다시 답장에 넣어서 보내!"라고 역으로 [[396_validation|확인]]([[239_stateless_redis|Stateless]] 방어)한 뒤에야 암호 협상 메모리를 열어주어 장비를 보호합니다.

[[589_ipsec_offload|IPsec]] [[280_ikev2|IKEv2]] 터널 협상을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. 다크 웹 Tor 통신 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 암호화층이 기반 조건을 만든다면, [[589_ipsec_offload|IPsec]] [[280_ikev2|IKEv2]] 터널 협상은 그 위에서 핵심 메커니즘을 구현하고, [[387_wireguard_vpn_modern_tunneling|WireGuard]] [[339_routing_overview_best_path_selection|라우팅]] 고속망 체계는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 측정 정확도과 모델 적합성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | 다크 웹 Tor 통신 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 암호화층의 기반 정리 | [[589_ipsec_offload|IPsec]] [[280_ikev2|IKEv2]] 터널 협상의 핵심 동작 | [[387_wireguard_vpn_modern_tunneling|WireGuard]] [[339_routing_overview_best_path_selection|라우팅]] 고속망 체계의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 측정 정확도 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [[396_validation|확인]] | 현재 메커니즘의 적합성 판단 | 운영·확장 [[268_strategy_pattern|전략]] 연결 |

- **📢 섹션 요약 비유**: [[589_ipsec_offload|IPsec]] [[280_ikev2|IKEv2]] 터널 협상은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- 현재 시스코, 주니퍼, 팔로알토 등 모든 글로벌 기업용 방화벽과 아이폰/안드로이드의 기본 [[589_ipsec_offload|IPsec]] VPN은 100% IKEv2를 표준으로 채택하여 돌아가고 있습니다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 기존 **[[279_ikev1|IKEv1]] [[983_vpn_virtual_private_network|VPN]] 협상**은 조선시대 **'양국 사신들의 외교 회담'**이었습니다. 양쪽 사신이 길 위에서 만나 인사하고(1번), 신분증 검사하고(2번), 암호 맞추고(3번), 세부 룰 정하고(4번)... 총 9번이나 왕복으로 편지를 주고받아야 비로소 터널 공사가 시작되어 연결이 한 세월이었습니다. 게다가 폰으로 와이파이에서 LTE로 바뀌어 주소가 달라지면 "너 신분증 다시 꺼내!"라며 터널을 다 때려 부수고 처음부터 다시 협상해야 했습니다(끊김 현상). 최신 **[[280_ikev2|IKEv2]] 협상**은 현대의 **'[[148_5g_embb_urllc_mmtc|초고속]] 전자 계약 시스템'**입니다. 만나는 즉시 서로 신분증과 암호화 룰을 한 봉투에 다 쓸어 담아서 딱 2번만 왕복 교환(4-Way)하면 1초 만에 공사가 끝납니다. 특히 스마트폰 IP가 와이파이에서 LTE로 바뀌어도, **MOBIKE**라는 흑마법을 통해 터널을 부수지 않고 서버에 "나 방금 이사했어 주소만 바꿔!"라고 쪽지 하나만 날리면 끊김 0.1초도 없이 VPN이 완벽히 이어지는 기업형 모바일 보안망의 최강자입니다.

---

## Ⅴ. 기대효과 및 결론

[[589_ipsec_offload|IPsec]] [[280_ikev2|IKEv2]] 터널 협상은 [[282_performance_tactics|성능]] 평가와 고급 분석을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 측정 정확도 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [[387_wireguard_vpn_modern_tunneling|WireGuard]] [[339_routing_overview_best_path_selection|라우팅]] 고속망 체계, [[190_ai_llm_requirements_specification|AI]] 기반 [[282_performance_tactics|성능]] 예측, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [[190_ai_llm_requirements_specification|AI]] 기반 [[282_performance_tactics|성능]] 예측 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [[589_ipsec_offload|IPsec]] [[280_ikev2|IKEv2]] 터널 협상은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 다크 웹 Tor 통신 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 암호화층 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [[139_throughput|처리량]] ([[139_throughput|Throughput]]) | 실제 전달 [[282_performance_tactics|성능]]을 나타내는 대표 지표다. |
| [[015_지연_데이터_관점|지연]] ([[141_latency|Latency]]) | 사용자 체감 품질을 좌우한다. |
| [[387_wireguard_vpn_modern_tunneling|WireGuard]] [[339_routing_overview_best_path_selection|라우팅]] 고속망 체계 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 다크 웹 Tor 통신 프로토콜 암호화층]
    │
    ▼
[현재 개념: IPsec IKEv2 터널 협상]
    │
    ├──▶ [확장 A: WireGuard 라우팅 고속망 체계]
    └──▶ [확장 B: AI 기반 성능 예측]
```

[[589_ipsec_offload|IPsec]] [[280_ikev2|IKEv2]] 터널 협상는 다크 웹 Tor 통신 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 암호화층에서 출발해 현재 메커니즘을 정교화하고, 이후 [[387_wireguard_vpn_modern_tunneling|WireGuard]] [[339_routing_overview_best_path_selection|라우팅]] 고속망 체계와 [[190_ai_llm_requirements_specification|AI]] 기반 [[282_performance_tactics|성능]] 예측 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 달리기 시합에서 누가 얼마나 빨랐는지 재려면 초시계와 기록표가 필요해요.
2. 이 개념은 네트워크가 어디서 느려졌는지 숫자로 찾아내는 도구예요.
3. 그래서 막연히 고치는 대신 가장 중요한 곳부터 똑똑하게 손볼 수 있어요.
