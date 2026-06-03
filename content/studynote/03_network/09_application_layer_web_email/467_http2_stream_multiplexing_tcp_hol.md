---
title: 467. HTTP/2 스트림 (Stream) 다중화 (Multiplexing)
date: '2026-05-08'
tags:
- studynote-network
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[461_http_stateless_connection_oriented|HTTP]]/2 스트림 다중화는 응용 계층과 웹/메일에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [[461_http_stateless_connection_oriented|HTTP]]/2 스트림 다중화를 이해하면 [[138_response_time|응답 시간]]과 [[344_compatibility_usability|호환성]] 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1. [[461_http_stateless_connection_oriented|HTTP]]/1.1 [[123_pipe|파이프]]라이닝의 참사 (The Pain Point)
[[461_http_stateless_connection_oriented|HTTP]]/1.1은 1개의 [[123_pipe|파이프]]([[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 연결)에 요청을 연달아 쑤셔 넣는 '[[123_pipe|파이프]]라이닝'을 도입했지만, 치명적인 결함이 있었습니다.
- **문제 발생**: 응답을 **'반드시 요청받은 순서대로(In-Order)'** 덩어리째 반환해야 했습니다. 1번 요청이 10초 걸리는 무거운 영상이라면, 이미 처리가 끝난 2번, 3번의 가벼운 텍스트 [[501_file_definition_logical_record|파일]]은 1번 영상이 [[123_pipe|파이프]]를 다 빠져나갈 때까지 10초 동안 [[123_pipe|파이프]] 입구에서 꼼짝없이 막혀 있어야 했습니다. 이것이 악명 높은 **[[461_http_stateless_connection_oriented|HTTP]] [[456_quic_hol_head_of_line_blocking_resolution|HOL]]([[456_quic_hol_head_of_line_blocking_resolution|Head-of-Line]]) 블로킹**입니다.

### 2. [[461_http_stateless_connection_oriented|HTTP]]/2의 혁명: 덩어리를 부수고 섞어라! ([[071_다중화_Multiplexing|Multiplexing]])
이 병목을 부수기 위해 구글의 엔지니어들(SPDY)은 텍스트 덩어리를 포기하고 [[001_dikw_pyramid|데이터]]를 잘게 부수는 '바이너리 [[184_framing_mechanism|프레이밍]](Binary [[184_framing_mechanism|Framing]])'을 도입했습니다.
- **필요성**: 1번 영상, 2번 텍스트, 3번 CSS를 아주 잘게 쪼갠 뒤(Frame), 1번-2번-3번-1번-2번 조각들을 마구 뒤섞어 [[123_pipe|파이프]](단일 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]])에 한꺼번에 흘려보냅니다. 도착지(브라우저)에서 조각에 적힌 번호표(Stream ID)를 보고 다시 조립하면, 무거운 영상 때문에 가벼운 텍스트가 막히는 일은 영원히 사라지게 됩니다.

```text
[HTTP/2 특징]
    │
    ▼
[HTTP/2 스트림 다중화]
    │
    └──▶ [HTTP/2 헤더 압축]
```

- **📢 섹션 요약 비유**: [[461_http_stateless_connection_oriented|HTTP]]/1.1이 "한 사람이 계산을 끝낼 때까지 뒷사람이 꼼짝 못 하고 기다려야 하는 1줄짜리 좁은 마트 계산대"라면, [[461_http_stateless_connection_oriented|HTTP]]/2의 멀티플렉싱은 "계산원 한 명이 수십 명의 손님 물건을 바코드로 번갈아 가며 1개씩 찍어주는 천재적인 [[430_index_fast_full_scan|병렬]] 처리 계산대"입니다. 물건이 적은 사람은 순식간에 계산을 끝내고 먼저 나갈 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[461_http_stateless_connection_oriented|HTTP]]/2의 멀티플렉싱은 3단계의 논리적 구조를 통해 구현됩니다.

```text
┌─────────────────────────────────────────────────────────────┐
│          [ HTTP/2 멀티플렉싱 (Multiplexing) 논리적 아키텍처 ]        │
│                                                             │
│   단일 물리적 연결 (Single TCP Connection)                        │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                                                     │   │
│   │ [ Stream ID: 1 ]  (논리적 양방향 통로: HTML 요청/응답)   │   │
│   │   ▶ Message (요청) -> [ HEADERS 프레임 ]               │   │
│   │   ◀ Message (응답) <- [ HEADERS 프레임 | DATA 프레임 ] │   │
│   │                                                     │   │
│   │ [ Stream ID: 3 ]  (논리적 양방향 통로: CSS 요청/응답)    │   │
│   │   ▶ Message (요청) -> [ HEADERS 프레임 ]               │   │
│   │   ◀ Message (응답) <- [ HEADERS 프레임 | DATA 프레임 ] │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│     ▼ (전송 시 프레임들의 무작위 믹스 및 Interleaving)               │
│                                                             │
│   [TCP 버퍼] ◀ [DATA 1] [DATA 3] [HEAD 3] [DATA 1] [HEAD 1] │
└─────────────────────────────────────────────────────────────┘
```

1. **스트림 (Stream)**: 클라이언트와 서버 사이에 맺어진 하나의 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 연결 내에서 논리적으로 구분된 가상의 양방향 흐름입니다. 각 스트림은 고유한 정수 ID(Stream ID)를 가집니다.
2. **메시지 (Message)**: 논리적인 [[461_http_stateless_connection_oriented|HTTP]] 요청(Request) 또는 응답(Response) 덩어리입니다. (여러 개의 프레임으로 구성됨)
3. **프레임 (Frame)**: [[461_http_stateless_connection_oriented|HTTP]]/2 통신의 최소 단위입니다. 모든 프레임의 헤더에는 자신이 어느 스트림(Stream ID) 소속인지 적혀 있습니다.

### 2. 우선순위 (Stream Prioritization) 제어
모든 스트림이 공평하게 뒤섞여 날아가면, 브라우저 화면을 그리는 데 필수적인 [[110_unlicensed_lpwan_lorawan_sigfox|CSS]] [[501_file_definition_logical_record|파일]]이 덜 중요한 이미지 [[501_file_definition_logical_record|파일]]과 섞여 렌더링이 늦어질 수 있습니다.
- [[461_http_stateless_connection_oriented|HTTP]]/2는 각 스트림에 1~256 사이의 **[[267_weight_bias_activation|가중치]]([[267_weight_bias_activation|Weight]])**와 **의존성(Dependency 트리)**을 부여할 수 있습니다. "[[110_unlicensed_lpwan_lorawan_sigfox|CSS]] 프레임(스트림 3)을 이미지 프레임(스트림 5)보다 우선해서 대역폭을 할당해 줘!"라고 브라우저가 서버에 똑똑하게 지시할 수 있는 아키텍처입니다.

| [[461_http_stateless_connection_oriented|HTTP]]/1.1의 꼼수 (Workarounds) | 발생하던 부작용 (Trade-offs) | [[461_http_stateless_connection_oriented|HTTP]]/2의 완벽한 해결책 |
| :--- | :--- | :--- |
| **다중 커넥션 (Multi-connections)** | 브라우저당 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] [[125_socket|소켓]] 6개 [[087_process_state_transition|생성]]. 1만 명 접속 시 서버에 6만 개 [[125_socket|소켓]] 낭비([[157_oom_killer|OOM]]) | **단일 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 커넥션(Single Connection)**에서 무한대의 스트림으로 [[430_index_fast_full_scan|병렬]] 처리 |
| **이미지 스프라이트 / [[501_file_definition_logical_record|파일]] 병합** | 100개의 아이콘을 1장의 큰 이미지로 합침. 아이콘 1개 수정 시 전체 재다운로드 (캐시 무효화) | **수많은 작은 [[501_file_definition_logical_record|파일]]을 [[430_index_fast_full_scan|병렬]]로 요청([[071_다중화_Multiplexing|Multiplexing]])**. 쪼개진 개별 [[501_file_definition_logical_record|파일]]의 완벽한 브라우저 [[456_caching|캐싱]] 활용 |
| **[[064_relation_domain|도메인]] [[280_sharding|샤딩]] ([[064_relation_domain|Domain]] [[243_sharding_horizontal_scaling_database|Sharding]])** | img1.com, img2.com 등 [[064_relation_domain|도메인]]을 쪼개어 [[125_socket|소켓]] 제한을 우회. [[511_dns_hierarchical_distributed_architecture|DNS]] 조회 [[015_지연_데이터_관점|지연]] 폭발. | [[064_relation_domain|도메인]]을 나눌 필요 없이, **단일 [[064_relation_domain|도메인]]에서 모든 트래픽 [[430_index_fast_full_scan|병렬]] 처리** |

### ⚡ 가장 치명적 트레이드오프: [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] [[456_quic_hol_head_of_line_blocking_resolution|HOL]] 블로킹 ([[405_tcp_transmission_control_protocol_connection_oriented|TCP]] [[456_quic_hol_head_of_line_blocking_resolution|Head-of-Line]] [[122_sync_async_communication|Blocking]])
[[461_http_stateless_connection_oriented|HTTP]]/2는 [[461_http_stateless_connection_oriented|HTTP]] 레벨(L7)의 블로킹은 없앴지만, 하부의 **전송 계층(L4)인 TCP가 가진 블로킹의 늪**에 그대로 빠지고 맙니다.
- **재앙의 시나리오**: 단일 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 커넥션 [[123_pipe|파이프]] 안에서 10개의 스트림(이미지 5개, [[110_unlicensed_lpwan_lorawan_sigfox|CSS]] 5개)이 막 섞여서 날아오고 있습니다. 그런데 무선(Wi-Fi) 전파가 흔들려 수만 개의 패킷 중 딱 **1개의 패킷이 유실(Loss)**되었습니다.
- **TCP의 한계**: TCP는 '완벽한 순서 보장' [[295_protocol_field_tcp_udp_icmp|프로토콜]]입니다. 5번 패킷이 유실되면, 무사히 도착한 6, 7, 8, 9번 패킷들을 브라우저(앱)로 올려보내지 않고 [[022_kernel_role|커널]](OS)의 수신 버퍼에 가둬버립니다. (서버가 5번을 재전송해 줄 때까지 꼼짝 못 함)
- **결과**: 1개의 패킷이 유실되었을 뿐인데, 단일 TCP에 묶여있던 10개의 스트림 전체가 브라우저에서 멈춰버리는 **'[[405_tcp_transmission_control_protocol_connection_oriented|TCP]] [[456_quic_hol_head_of_line_blocking_resolution|HOL]] 블로킹'** 대참사가 발생합니다. ([[461_http_stateless_connection_oriented|HTTP]]/1.1은 [[125_socket|소켓]]을 6개로 나눴기 때문에 1개가 터져도 5개는 살아있었음)

- **📢 섹션 요약 비유**: [[461_http_stateless_connection_oriented|HTTP]]/2의 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] [[456_quic_hol_head_of_line_blocking_resolution|HOL]] 블로킹은 "거대한 100인승 [[344_bus|버스]](단일 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]])에 모든 [[501_file_definition_logical_record|파일]] 승객을 태우고 고속도로를 달리는 것"과 같습니다. [[344_bus|버스]]는 매우 효율적이지만, [[344_bus|버스]] 타이어 하나가 펑크 나면 안에 타고 있던 100명의 승객(모든 스트림) 전체가 지각하게 되는 끔찍한 구조적 약점을 안고 있습니다.

---

## Ⅲ. 비교 및 연결

[[461_http_stateless_connection_oriented|HTTP]]/2 스트림 다중화를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [[461_http_stateless_connection_oriented|HTTP]]/2 특징이 기반 조건을 만든다면, [[461_http_stateless_connection_oriented|HTTP]]/2 스트림 다중화는 그 위에서 핵심 메커니즘을 구현하고, [[461_http_stateless_connection_oriented|HTTP]]/2 헤더 [[347_compaction|압축]]은 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 [[138_response_time|응답 시간]]과 [[344_compatibility_usability|호환성]]에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [[461_http_stateless_connection_oriented|HTTP]]/2 특징의 기반 정리 | [[461_http_stateless_connection_oriented|HTTP]]/2 스트림 다중화의 핵심 동작 | [[461_http_stateless_connection_oriented|HTTP]]/2 헤더 [[347_compaction|압축]]의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | [[138_response_time|응답 시간]] 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [[396_validation|확인]] | 현재 메커니즘의 적합성 판단 | 운영·확장 [[268_strategy_pattern|전략]] 연결 |

- **📢 섹션 요약 비유**: [[461_http_stateless_connection_oriented|HTTP]]/2 스트림 다중화는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

| 고려 사항 | 세부 내용 | 주요 아키텍처 의사결정 |
|:---|:---|:---|
| **도입 환경** | 기존 레거시 시스템과의 [[344_compatibility_usability|호환성]] 분석 | 마이그레이션 [[268_strategy_pattern|전략]] 및 단계별 전환 계획 수립 |
| **비용([[012_roi_return_on_investment|ROI]])** | [[459_quic_fec_forward_error_correction|초기]] 구축 비용(CAPEX) 및 운영 비용(OPEX) | [[016_tco|TCO]] 관점의 장기적 효율성 [[395_verification_process_review|검증]] |
| **보안/위험** | 컴플라이언스 준수 및 [[001_dikw_pyramid|데이터]] [[442_consistency_integrity|무결성 보장]] | [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] 기반 [[303_authentication_authorization_patterns|인증]]/[[509_authorization_models_rbac_abac|인가]] 체계 연계 |

*(추가 실무 적용 가이드 - L4/L7 로드밸런서 및 [[264_proxy_pattern_surrogate_access_control|프록시]] 아키텍처)*
- 클라이언트(브라우저)와 서버가 [[461_http_stateless_connection_oriented|HTTP]]/2로 통신하려면, 중간에 있는 수많은 문지기([[506_cdn_content_delivery_network_edge_caching|CDN]], [[696_waf_web_application_firewall|WAF]], 로드밸런서)들이 모두 [[461_http_stateless_connection_oriented|HTTP]]/2의 [[184_framing_mechanism|프레이밍]] 계층을 파싱(Parsing)할 줄 알아야 합니다.
- **실무 의사결정 (종단 간 [[461_http_stateless_connection_oriented|HTTP]]/2 구성의 한계)**: AWS ALB(Application [[031_load_balancer|Load Balancer]])를 사용할 때, 클라이언트와 ALB 구간은 [[461_http_stateless_connection_oriented|HTTP]]/2 통신([[071_다중화_Multiplexing|Multiplexing]])을 쉽게 켤 수 있습니다. 하지만 **ALB와 백엔드 서버(EC2) 구간까지 억지로 [[461_http_stateless_connection_oriented|HTTP]]/2를 유지할 필요는 없습니다.** 
- 백엔드 구간은 사설망([[836_vpc_virtual_private_cloud_subnet_isolation|VPC]]) 내부라 패킷 유실률이 0에 가깝고 [[015_지연_데이터_관점|지연]]([[441_rtt_round_trip_time_srtt_smoothed|RTT]])이 극히 낮습니다. 오히려 ALB가 [[461_http_stateless_connection_oriented|HTTP]]/2 스트림을 [[461_http_stateless_connection_oriented|HTTP]]/1.1로 변환(Down-grade)하여 백엔드로 뿌려주는 아키텍처가 시스템 부하(오버헤드) 측면에서 유리하며, 현재 대부분의 엔터프라이즈 클라우드 인프라의 표준(De facto) 설계 패턴입니다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 [[395_verification_process_review|검증]]한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 실무 적용은 "집을 지을 때 터를 다지고 자재를 고르는 과정"과 같이, 환경과 예산에 맞춘 최적의 선택이 필요합니다. "거친 바다(인터넷)를 건널 때는 파도에 흔들리지 않는 거대한 크루즈선([[461_http_stateless_connection_oriented|HTTP]]/2 멀티플렉싱)이 필요하지만, 항구에 도착해 잔잔한 내륙 운하(사내 VPC망)로 들어오면 작고 날렵한 모터보트([[461_http_stateless_connection_oriented|HTTP]]/1.1)로 옮겨 타는 것이 가장 합리적인 물류(아키텍처) [[268_strategy_pattern|전략]]입니다."

---

## Ⅴ. 기대효과 및 결론

1. **[[461_http_stateless_connection_oriented|HTTP]]/3 ([[454_quic_quick_udp_internet_connections|QUIC]]) 시대의 개막: 진정한 [[456_quic_hol_head_of_line_blocking_resolution|HOL]] 블로킹의 종식**
   [[461_http_stateless_connection_oriented|HTTP]]/2가 TCP라는 낡은 마차 위에서 춤을 추다가 엎어지는 꼴([[405_tcp_transmission_control_protocol_connection_oriented|TCP]] [[456_quic_hol_head_of_line_blocking_resolution|HOL]] 블로킹)을 본 구글은, 아예 낡은 마차를 폭파해 버리기로 결심했습니다. 
   - 연결과 순서 강제가 없는 **[[406_udp_user_datagram_protocol_connectionless_fast|UDP]]([[406_udp_user_datagram_protocol_connectionless_fast|User Datagram Protocol]])** 위에 '[[454_quic_quick_udp_internet_connections|QUIC]]'이라는 새로운 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 계층을 쌓아 올렸습니다. 
   - [[461_http_stateless_connection_oriented|HTTP]]/3 환경에서는 스트림 1번 패킷이 공중에서 폭파되어도, 스트림 2번과 3번은 TCP의 간섭 없이 브라우저로 곧바로 직행하는 **완벽한 논리적/물리적 스트림 분리(Independent Streams)**를 달성해 냈습니다.

2. **모바일 [[418_5g_embb_urllc_mmtc_slicing|5G]] 및 위성 통신망(Starlink)과의 결합**
   기지국 사이를 이동할 때([[556_handover_handoff_types_concept|핸드오버]]) 와이파이에서 LTE로 바뀌면 IP 주소가 변경되어 기존 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 연결([[461_http_stateless_connection_oriented|HTTP]]/2)은 뚝 끊어지고 재연결을 해야 합니다. 미래의 [[461_http_stateless_connection_oriented|HTTP]]/3([[454_quic_quick_udp_internet_connections|QUIC]])는 IP 주소 대신 **Connection ID**로 연결을 추적하므로, 지하철에서 내리며 와이파이가 끊겨도 유튜브 영상이 단 0.1초도 끊기지 않고 부드럽게 이어지는 모바일 친화적 인프라 시대를 열어가고 있습니다.


## 🧠 지식 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])

*   **[[461_http_stateless_connection_oriented|HTTP]] [[282_performance_tactics|성능]] 병목 ([[971_hol_blocking_head_of_line_tcp_http_delay|HOL Blocking]]) 아키텍처**
    *   **[[461_http_stateless_connection_oriented|HTTP]] [[971_hol_blocking_head_of_line_tcp_http_delay|HOL Blocking]]**: 애플리케이션 계층(L7) 병목. 앞선 무거운 응답이 뒤의 응답을 막음 ([[461_http_stateless_connection_oriented|HTTP]]/1.1의 문제)
    *   **[[405_tcp_transmission_control_protocol_connection_oriented|TCP]] [[971_hol_blocking_head_of_line_tcp_http_delay|HOL Blocking]]**: 전송 계층(L4) 병목. 1개의 패킷 유실이 버퍼 전체를 막음 ([[461_http_stateless_connection_oriented|HTTP]]/2의 남겨진 한계)
*   **[[461_http_stateless_connection_oriented|HTTP]]/2 멀티플렉싱([[071_다중화_Multiplexing|Multiplexing]]) 메커니즘**
    *   단일 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 커넥션 유지 (오버헤드 방지)
    *   메시지를 **바이너리 프레임(Binary Frame)**으로 분할하여 Interleaving (뒤섞음)
    *   스트림 ID(Stream ID) 기반 목적지 재조립 체계
*   **미래 기술 연계**
    *   [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 기반의 [[454_quic_quick_udp_internet_connections|QUIC]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[461_http_stateless_connection_oriented|HTTP]]/3) -> 독립적 스트림으로 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] [[456_quic_hol_head_of_line_blocking_resolution|HOL]] 100% 타파

- **📢 섹션 요약 비유**: 웹 통신망의 진화는 끝없는 교통체증([[456_quic_hol_head_of_line_blocking_resolution|HOL]])과의 사투였습니다. [[461_http_stateless_connection_oriented|HTTP]]/1.1은 꽉 막힌 "1차선 국도"였고, [[461_http_stateless_connection_oriented|HTTP]]/2는 차선을 늘린 "다차선 고속도로"였지만 사고가 나면 톨게이트가 막혔습니다. 이제 [[461_http_stateless_connection_oriented|HTTP]]/3는 자동차가 아예 각자의 길로 날아다니는 "하늘을 나는 드론 비행망"으로 진화하며 체증 자체를 역사에서 지워버렸습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[461_http_stateless_connection_oriented|HTTP]]/2 특징 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [[160_session_controlling_terminal|세션]] ([[160_session_controlling_terminal|Session]]) | 사용자 상태 유지와 요청 흐름을 묶는다. |
| 캐시 (Cache) | 응답 속도와 백엔드 부하에 직접 영향을 준다. |
| [[461_http_stateless_connection_oriented|HTTP]]/2 헤더 [[347_compaction|압축]] | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: HTTP/2 특징]
    │
    ▼
[현재 개념: HTTP/2 스트림 다중화]
    │
    ├──▶ [확장 A: HTTP/2 헤더 압축]
    └──▶ [확장 B: 지능형 애플리케이션 전달]
```

[[461_http_stateless_connection_oriented|HTTP]]/2 스트림 다중화는 [[461_http_stateless_connection_oriented|HTTP]]/2 특징에서 출발해 현재 메커니즘을 정교화하고, 이후 [[461_http_stateless_connection_oriented|HTTP]]/2 헤더 [[347_compaction|압축]]와 지능형 애플리케이션 전달 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 이 기술은 마치 우리가 매일 사용하는 "스마트폰"과 같아요.
2. 복잡한 기계 장치들이 숨어 있지만, 우리는 화면만 터치하면 쉽게 원하는 것을 할 수 있죠.
3. 이처럼 보이지 않는 곳에서 시스템이 잘 돌아가도록 돕는 멋진 마법 같은 기술이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 588 / 1120

← **이전**: [[466_http2_multiplexing_hpack|466. HTTP/2 특징]]
**다음**: [[468_http2_hpack_header_compression|468. HTTP/2 헤더 압축 (HPACK 알고리즘 활용)]] →

---
