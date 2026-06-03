+++
weight = 461
title = "461. HTTP (HyperText Transfer Protocol) 상태 비저장 (Stateless), 연결형/비연결형 특징"
date = "2026-05-08"
[extra]
categories = "studynote-network"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: HTTP 상태 비저장, 연결형/비연결형 특징은 응용 계층과 웹/메일에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: HTTP 상태 비저장, 연결형/비연결형 특징을 이해하면 응답 시간과 [[344_compatibility_usability|호환성]] 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

> ⚠️ 이 문서는 인터넷의 근간을 이루는 HTTP 프로토콜의 아키텍처 철학인 [[162_rest_statelessness|무상태성]]([[239_stateless_redis|Stateless]])과 비연결성(Connectionless), 그리고 하위 계층인 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 연결형(Connection-oriented) 구조와의 상호작용 메커니즘을 심층 분석합니다.

```text
[패킷 손실 복구 메커니즘 개선]
    │
    ▼
[HTTP 상태 비저장, 연결형/비연결형 특징]
    │
    └──▶ [HTTP 메서드]
```

- **📢 섹션 요약 비유**: HTTP 상태 비저장, 연결형/비연결형 특징은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [[170_selectivity_cardinality_distribution_tuning|선택도]] 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[459_quic_fec_forward_error_correction|초기]] 웹(World Wide Web)은 전 세계의 수많은 텍스트 문서(HTML)를 하이퍼링크로 연결하여 빠르게 읽고 넘기는 용도로 설계되었습니다. 1:1로 지속적인 [[160_session_controlling_terminal|세션]]을 맺고 통신하는 텔넷(Telnet)이나 FTP와 달리, 웹 서버는 언제 어디서 쏟아질지 모르는 불특정 다수의 대규모 요청을 처리해야 했습니다. 이를 위해 HTTP(HyperText Transfer [[295_protocol_field_tcp_udp_icmp|Protocol]])는 **상태를 저장하지 않고([[239_stateless_redis|Stateless]])**, 한 번 응답하면 즉시 **연결을 끊어버리는(Connectionless)** 극단적으로 가벼운 패러다임을 채택했습니다.

### 2. 해결하고자 하는 문제 (Pain Point)
만약 10만 명의 사용자가 동시에 접속하는 쇼핑몰 서버가 Stateful(상태 유지) 및 Connection-oriented(연결 유지) 방식으로 설계되었다면, 서버는 10만 개의 [[125_socket|소켓]]([[125_socket|Socket]])을 열어둔 채 사용자들의 모든 과거 행동 [[001_dikw_pyramid|데이터]]를 메모리에 유지해야 합니다. 이는 필연적으로 서버 자원의 고갈([[157_oom_killer|OOM]]: [[157_oom_killer|Out Of Memory]], [[125_socket|소켓]] [[446_port_and_bus|포트]] 고갈)과 엄청난 [[212_synchronization_mechanisms|동기화]] 오버헤드를 초래하여 시스템을 마비시킵니다. HTTP는 철저하게 서버의 부담을 줄이는 방향으로 아키텍처를 설계하여 이 문제를 원천 차단했습니다.

```text
[패킷 손실 복구 메커니즘 개선]
    │
    ▼
[HTTP 상태 비저장, 연결형/비연결형 특징]
    │
    └──▶ [HTTP 메서드]
```

- **📢 섹션 요약 비유**: HTTP의 [[239_stateless_redis|Stateless]] 방식은 마치 '자판기'와 같습니다. 어제 내가 콜라를 뽑았는지 기억하지 못하지만, 오늘 당장 동전(요청)을 넣으면 즉시 사이다(응답)를 내어줍니다. 기억하지 않기 때문에 하루에 수만 명이 찾아와도 지치지 않습니다.

---

## Ⅲ. 비교 및 연결

HTTP가 상태를 기억하지 않고([[239_stateless_redis|Stateless]]), 금방 연결을 끊어버린다(Connectionless)고 해서 [[001_dikw_pyramid|데이터]] 전송 자체가 부실한 것은 아닙니다. 텍스트 문서의 [[003_integrity|무결성]]을 보장하기 위해 HTTP는 전송 계층(L4) 프로토콜로 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 있는 **[[405_tcp_transmission_control_protocol_connection_oriented|TCP]]([[405_tcp_transmission_control_protocol_connection_oriented|Transmission Control Protocol]])**를 선택했습니다.

```text
┌─────────────────────────────────────────────────────────────┐
│  [ HTTP over TCP : 논리적 무상태와 물리적 연결의 조화 ]     │
│                                                             │
│       [ Application Layer - L7 ]                            │
│  Client                            Server                   │
│    │     HTTP GET /index.html        │    <-- Stateless     │
│    ├────────────────────────────────▶│    <-- Connectionless│
│    │     HTTP 200 OK (HTML Data)     │                      │
│    │◀────────────────────────────────┤                      │
│                                                             │
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
│       [ Transport Layer - L4 ]                              │
│  Client                            Server                   │
│    │      SYN (연결 요청)            │    <-- TCP 3-Way     │
│    ├────────────────────────────────▶│        Handshake     │
│    │      SYN + ACK                  │    (Connection-      │
│    │◀────────────────────────────────┤      oriented)       │
│    │      ACK                        │                      │
│    ├────────────────────────────────▶│                      │
└─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** L7의 HTTP 요청이 발생하기 직전, 하위 L4 계층에서는 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 3-Way Handshake를 통해 물리적인 가상 회선(Virtual Circuit)을 단단하게 연결합니다(Connection-oriented). HTTP 통신이 끝나면 L4는 4-Way Handshake로 연결을 해제합니다. 즉, 뼈대([[405_tcp_transmission_control_protocol_connection_oriented|TCP]])는 연결형이지만 그 위에서 노는 [[090_service_kubernetes_network_load_balancing|서비스]](HTTP)는 비연결형인 구조입니다.

### 2. 상태 비저장 ([[239_stateless_redis|Stateless]]) 메커니즘
Stateless는 **"서버가 클라이언트의 이전 상태([[033_context|Context]])를 보존하지 않는 구조"**입니다. 클라이언트가 이전 통신의 연속 선상에서 새로운 요청을 하더라도, 서버는 이를 완전히 독립적인 새로운 요청으로 취급합니다.

- **장점**: 
  - 상태 보존을 위한 메모리 공간 할당 불필요
  - 특정 서버에 클라이언트가 종속되지 않으므로, 로드 밸런서(L4/L7)를 통해 어떠한 백엔드 서버로든 트래픽을 자유롭게 [[136_variance|분산]]([[202_scale_out_distributed_horizontal_expansion|Scale-out]]) 가능
- **단점**: 
  - 매 요청마다 클라이언트가 자신을 증명할 모든 추가 정보([[160_session_controlling_terminal|세션]] ID, 장바구니 내용 등)를 반복해서 전송해야 하므로 네트워크 [[140_bandwidth|대역폭]] 낭비 발생

```text
┌─────────────────────────────────────────────────────────────┐
│  [ Stateful vs Stateless 아키텍처 동작 비교 ]               │
│                                                             │
│  [ 1. Stateful Server (기존 방식) ]                         │
│  User: "안녕하세요, 저는 홍길동입니다." -> Server: "네, 기억할게요." │
│  User: "장바구니에 사과 담아주세요."    -> Server: "(홍길동 님이구나) 네!"│
│  User: "결제할게요."                    -> Server: "(홍길동 님의 사과) 완료!"│
│  * 제약: 해당 유저는 반드시 자신을 기억하는 '이 서버'와만 통신해야 함 │
│                                                             │
│  [ 2. Stateless Server (HTTP 방식) ]                        │
│  User: "안녕하세요, 홍길동입니다."      -> Server: "응답 완료. (기억 삭제)"│
│  User: "홍길동인데 사과 담을게요."      -> Server: "응답 완료. (기억 삭제)"│
│  User: "홍길동인데 아까 담은 사과 결제요"-> Server: "응답 완료. (기억 삭제)"│
│  * 장점: 유저가 문맥을 매번 실어 보내므로, 아무 서버나 응답 가능! │
└─────────────────────────────────────────────────────────────┘
```

Connectionless는 **"서버가 클라이언트의 요청에 대해 응답을 마치면 맺었던 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 연결을 즉시 끊어버리는 구조"**입니다.
- 웹사이트 열람의 본질은 짧은 시간 [[001_dikw_pyramid|데이터]]를 다운로드하고, 사용자는 한참 동안 문서를 읽는(유휴 시간) 패턴을 갖습니다.
- 연결을 끊지 않으면 10만 명이 문서를 읽는 동안 서버는 10만 개의 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] [[125_socket|소켓]]을 유지해야 합니다.
- 응답 후 연결을 끊으면, [[125_socket|소켓]]을 즉시 회수하여 다른 사용자의 요청 처리에 재사용할 수 있습니다. 이것이 1대의 웹 서버가 수만 명을 [[090_service_kubernetes_network_load_balancing|서비스]]하는 비결입니다.

| 비교 항목 | Stateful (상태 유지) | [[239_stateless_redis|Stateless]] (무상태) - HTTP |
| :--- | :--- | :--- |
| **상태 저장 위치** | 서버 ([[160_session_controlling_terminal|Session]], Memory) | 클라이언트 (요청에 포함) 또는 외부 DB |
| **서버 부하** | 연결된 클라이언트 수 비례 증가 | 매우 낮음 (응답 후 자원 해제) |
| **확장성 (Scalability)** | 수평 확장 어려움 ([[160_session_controlling_terminal|Session]] [[105_clustering_analysis|Clustering]], Sticky [[160_session_controlling_terminal|Session]] 강제됨) | **무한한 수평 확장 가능** (아무 서버나 처리 가능) |
| **네트워크 트래픽** | 적음 (과거 문맥을 서버가 알기 때문) | 많음 (매번 문맥 정보를 헤더 등에 담아 전송) |
| **장애 시 영향** | 서버 다운 시 해당 클라이언트 상태 증발 | 특정 서버가 죽어도 다른 서버가 이어받아 정상 처리 |

현대 웹(쇼핑몰, 은행, 메신저)에서는 무상태/비연결만으로는 [[090_service_kubernetes_network_load_balancing|서비스]]를 구현할 수 없습니다. 따라서 HTTP의 철학은 유지하되, 별도의 기술을 접목하여 **단점(트레이드오프)**을 극복합니다.

1. **상태가 없는 문제 해결 ([[239_stateless_redis|Stateless]] 극복)**
   - **[[475_cookie_local_state|쿠키]]([[475_cookie_local_state|Cookie]])와 [[160_session_controlling_terminal|세션]]([[160_session_controlling_terminal|Session]])**: HTTP 헤더에 [[475_cookie_local_state|쿠키]]를 담아 클라이언트를 식별하고, 서버 측 [[160_session_controlling_terminal|세션]] 스토리지에 상태를 임시 저장.
   - **토큰([[549_jwt_json_web_token|JWT]])**: 최근 [[974_restful_api_stateless_http_methods_uri|RESTful API]] 및 [[619_msa_traffic_hardware|MSA]] 환경에서는 서버조차 [[160_session_controlling_terminal|세션]]을 저장하지 않기 위해, 상태(권한/정보)를 암호화된 토큰에 담아 클라이언트에게 주고받게 하는 순수 무상태 [[303_authentication_authorization_patterns|인증]] 구조 사용.

2. **매번 연결을 끊는 문제 해결 (Connectionless 극복)**
   - HTML 다운로드 후 이미지, [[110_unlicensed_lpwan_lorawan_sigfox|CSS]], JS를 다운받기 위해 매번 3-Way Handshake를 하면 심각한 [[015_지연_데이터_관점|지연]]([[141_latency|Latency]])이 발생.
   - **HTTP/1.1 Keep-Alive**: 지정된 시간이나 횟수 동안 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 연결을 끊지 않고 유지하여, 하나의 연결 위에서 다수의 자원을 다운로드하는 **지속 연결(Persistent Connection)** 기술 표준화.

- **📢 섹션 요약 비유**: 순수 HTTP는 "금붕어 기억력을 가진 택배 기사"입니다. 배달하면 끝이고(비연결), 어제 배달 간 집을 오늘 기억 못 합니다(무상태). 그래서 우리는 택배 상자에 항상 "전체 주소와 고객 정보([[475_cookie_local_state|쿠키]]/토큰)"를 큼지막하게 적어서 보내야 합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

| 고려 사항 | 세부 내용 | 주요 아키텍처 의사결정 |
|:---|:---|:---|
| **아키텍처 확장성** | 사용자 트래픽의 급격한 증가([[129_spike_agile_technical_investigation|Spike]])가 예상되는가? | L7 웹 서버 계층은 완전한 Stateless로 구축하고, 상태는 [[136_variance|분산]] 캐시([[542_redis|Redis]])나 토큰([[549_jwt_json_web_token|JWT]])으로 분리하여 Auto-Scaling 극대화 |
| **보안 및 [[303_authentication_authorization_patterns|인증]]** | [[239_stateless_redis|Stateless]] 환경에서 안전하게 사용자를 식별할 수 있는가? | [[549_jwt_json_web_token|JWT]] 토큰의 탈취 방지를 위해 Access Token의 유효기간을 짧게 하고, HTTP Only [[475_cookie_local_state|쿠키]]를 혼용하는 [[302_security_architecture_design|보안 아키텍처]] 적용 |
| **연결 오버헤드** | SSL/[[694_thread_local_storage_tls|TLS]] 핸드셰이크 [[015_지연_데이터_관점|지연]]이 성능에 악영향을 주는가? | 서버 앞단에 리버스 [[264_proxy_pattern_surrogate_access_control|프록시]](Nginx 등)를 두어 클라이언트와 Keep-Alive 통신을 맺고, 백엔드와는 효율적인 커넥션 [[285_pooling_layer|풀링]](Connection [[285_pooling_layer|Pooling]]) 설계 |

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 실무 적용은 "집을 지을 때 터를 다지고 자재를 고르는 과정"과 같이, 환경과 예산에 맞춘 최적의 선택이 필요합니다. 완벽한 무상태 구조를 구축해야 서버를 수십 대로 쉽게 복제해 낼 수 있습니다.

---

## Ⅴ. 기대효과 및 결론

1. **상태 비저장의 극대화 ([[199_cloud_native_architecture_msa_cicd_devops|Cloud Native]] & [[206_serverless_cold_start|Serverless]])**
   HTTP의 [[239_stateless_redis|Stateless]] 철학은 현대 클라우드의 [[342_faas|FaaS]] (Function [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]], AWS [[216_lambda_kappa_architecture_batch_realtime|Lambda]] 등) 아키텍처 철학으로 계승되었습니다. [[206_serverless_cold_start|서버리스]] 함수들은 호출될 때만 기동되어 연산을 처리하고 바로 소멸하는 완벽한 [[239_stateless_redis|Stateless]] 컴퓨팅을 구현하고 있습니다.

2. **비연결성의 완전한 붕괴와 실시간 스트리밍 (WebSockets & [[481_sse_server_sent_events|SSE]])**
   웹의 역할이 정적 문서 뷰어에서 실시간 주식 거래, 화상 회의, 게임([[505_webrtc_web_real_time_communication|WebRTC]])으로 발전하면서 비연결성 패러다임은 큰 도전을 받고 있습니다. 이를 보완하기 위해 한 번 연결된 TCP를 끊지 않고 양방향으로 영구 통신하는 **[[480_websocket_full_duplex|WebSocket]]**, [[008_단방향_반이중_전이중|단방향]] 실시간 푸시를 위한 **[[481_sse_server_sent_events|SSE]]([[481_sse_server_sent_events|Server-Sent Events]])** 기술이 HTTP 인프라 위에서 융합 발전하고 있습니다.

3. **HTTP/3의 [[454_quic_quick_udp_internet_connections|QUIC]] 기반 전송 혁신**
   TCP의 3-Way Handshake라는 태생적 한계(무거운 [[459_quic_fec_forward_error_correction|초기]] 연결 비용)를 극복하기 위해, Google 주도로 [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 기반의 [[454_quic_quick_udp_internet_connections|QUIC]] 프로토콜을 사용하는 HTTP/3가 표준화되었습니다. 이는 무상태/비연결의 철학은 유지하되 0-RTT 연결이라는 혁신을 이루어냈습니다.


## 🧠 지식 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])

*   **네트워크 계층 구조 기초**
    *   OSI 7 Layer (L7 Application, L4 Transport)
    *   [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/IP 모델 ([[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 연결 지향성, [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 비연결성)
*   **상태 보완 기술 (Stateful Workarounds)**
    *   [[475_cookie_local_state|Cookie]] (클라이언트 측 상태 임시 보관)
    *   [[160_session_controlling_terminal|Session]] (서버 측 메모리 점유 상태 보관)
    *   [[549_jwt_json_web_token|JWT]] (비상태/[[003_integrity|무결성]] 증명 자가 포함 토큰)
*   **비연결성 보완 기술 (Connectionless Workarounds)**
    *   HTTP/1.1 Keep-Alive (지속 연결)
    *   [[480_websocket_full_duplex|WebSocket]] (L7 양방향 전이중 통신)
    *   HTTP/3 [[454_quic_quick_udp_internet_connections|QUIC]] ([[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 기반 [[071_다중화_Multiplexing|다중화]] 및 0-RTT) 향후에는 지능형 애플리케이션 전달 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: 인터넷이 "단순한 도서관"에서 "실시간 [[594_metaverse_realtime_sync_rendering_offloading|메타버스]] 놀이터"로 진화하면서, HTTP도 자신의 오랜 고집(비연결성)을 유연하게 접고 새로운 장비([[975_websocket_full_duplex_realtime_http_upgrade|웹소켓]], HTTP/3)를 장착하며 시대의 요구에 응답하고 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 패킷 손실 [[658_ir_recovery|복구]] 메커니즘 개선 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [[160_session_controlling_terminal|세션]] ([[160_session_controlling_terminal|Session]]) | 사용자 상태 유지와 요청 흐름을 묶는다. |
| 캐시 (Cache) | 응답 속도와 백엔드 부하에 직접 영향을 준다. |
| HTTP 메서드 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 패킷 손실 복구 메커니즘 개선]
    │
    ▼
[현재 개념: HTTP 상태 비저장, 연결형/비연결형 특징]
    │
    ├──▶ [확장 A: HTTP 메서드]
    └──▶ [확장 B: 지능형 애플리케이션 전달]
```

HTTP 상태 비저장, 연결형/비연결형 특징는 패킷 손실 [[658_ir_recovery|복구]] 메커니즘 개선에서 출발해 현재 메커니즘을 정교화하고, 이후 HTTP 메서드와 지능형 애플리케이션 전달 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 이 기술은 마치 우리가 매일 사용하는 "스마트폰"과 같아요.
2. 복잡한 기계 장치들이 숨어 있지만, 우리는 화면만 터치하면 쉽게 원하는 것을 할 수 있죠.
3. 이처럼 보이지 않는 곳에서 시스템이 잘 돌아가도록 돕는 멋진 마법 같은 기술이랍니다!
