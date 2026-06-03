---
title: 120. CoAP (Constrained Application Protocol) - IoT 경량 RESTful 프로토콜
date: '2026-04-19'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CoAP은 **[[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 기반의 경량 RESTful [[295_protocol_field_tcp_udp_icmp|프로토콜]]**로, HTTP와 유사한 GET/PUT/POST/DELETE를 지원하면서도 **4바이트 고정 헤더**로 제약 디바이스(센서·액추에이터)에 최적화되었다.
> 2. **가치**: MQTT가 Pub/Sub(이벤트 전달)에 강하다면, CoAP은 **Request/Response(리소스 조회·제어)**에 강하며, [[461_http_stateless_connection_oriented|HTTP]]-CoAP [[264_proxy_pattern_surrogate_access_control|프록시]]를 통해 웹 서비스와 직접 연동이 가능하다.
> 3. **판단 포인트**: [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 기반이므로 **[[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]을 Confirmable/Non-Confirmable 메시지로 구분**하며, [[644_dtls_datagram_tls_coap_security|DTLS]]([[644_dtls_datagram_tls_coap_security|Datagram TLS]])로 보안을 확보한다. MQTT와 경쟁이 아닌 **보완 [[083_relationship_in_er_model|관계]]**이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    CoAP vs HTTP vs MQTT                               │
├───────────────────────────────────────────────────────┤
│  [HTTP]        [CoAP]         [MQTT]                  │
│   TCP           UDP            TCP                    │
│   헤더: 수백B    헤더: 4B       헤더: 2B               │
│   Req/Res       Req/Res        Pub/Sub                │
│   무거움         경량 RESTful   경량 이벤트            │
│                                                       │
│  CoAP = "IoT의 HTTP" (RESTful, UDP 경량화)           │
│  MQTT = "IoT의 메시징" (Pub/Sub, TCP 경량화)         │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: HTTP는 대형 트럭, MQTT는 오토바이 택배, CoAP은 자전거 택배다. 자전거(CoAP)는 작은 골목(제약 디바이스)도 다닐 수 있고, 택배(RESTful) 서비스도 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### CoAP 메시지 유형

| 유형 | 설명 |
|:---|:---|
| **CON (Confirmable)** | [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 필요, ACK 응답 필수 |
| **NON (Non-Confirmable)** | [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 불필요, ACK 없음 |
| **ACK** | CON에 대한 [[396_validation|확인]] 응답 |
| **RST (Reset)** | 처리 불가 에러 응답 |

### CoAP vs [[622_mqtt_publish_subscribe_qos|MQTT]]

| 비교 | CoAP | [[622_mqtt_publish_subscribe_qos|MQTT]] |
|:---|:---|:---|
| **전송** | **[[406_udp_user_datagram_protocol_connectionless_fast|UDP]]** | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] |
| **패턴** | **Req/Res (RESTful)** | Pub/Sub |
| **헤더** | 4B | 2B |
| **적합** | **리소스 조회·제어** | 이벤트·센서 [[001_dikw_pyramid|데이터]] |

- **📢 섹션 요약 비유**: CoAP은 전화(요청→응답)이고, MQTT는 라디오 방송(구독·수신)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[461_http_stateless_connection_oriented|HTTP]] | CoAP | [[622_mqtt_publish_subscribe_qos|MQTT]] |
|:---|:---|:---|:---|
| **전송** | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] | **[[406_udp_user_datagram_protocol_connectionless_fast|UDP]]** | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] |
| **패턴** | Req/Res | **Req/Res** | Pub/Sub |
| **크기** | 무거움 | **경량** | 경량 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 활용 시나리오
- CoAP: 센서 값 GET 요청, 액추에이터 PUT 제어.
- [[622_mqtt_publish_subscribe_qos|MQTT]]: 센서 [[001_dikw_pyramid|데이터]] 스트리밍, 이벤트 알림.
- **혼합**: CoAP(제어) + [[622_mqtt_publish_subscribe_qos|MQTT]](모니터링) 병행 구성.

---

## Ⅴ. 기대효과 및 결론

CoAP은 **IoT의 RESTful 표준**으로서 웹 서비스와의 자연스러운 연동을 가능케 하며, [[121_lwm2m_lightweight_m2m|LwM2M]](경량 디바이스 관리) [[295_protocol_field_tcp_udp_icmp|프로토콜]]의 전송 계층으로 채택되어 [[101_iot_concept|IoT]] 디바이스 관리의 기반이 되고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **RESTful** | CoAP이 [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 위에 구현한 아키텍처 |
| **[[644_dtls_datagram_tls_coap_security|DTLS]]** | CoAP의 보안 계층 (UDP용 [[694_thread_local_storage_tls|TLS]]) |
| **[[622_mqtt_publish_subscribe_qos|MQTT]]** | CoAP의 보완 [[295_protocol_field_tcp_udp_icmp|프로토콜]] (Pub/Sub) |
| **[[121_lwm2m_lightweight_m2m|LwM2M]]** | CoAP 기반 [[101_iot_concept|IoT]] 디바이스 관리 [[295_protocol_field_tcp_udp_icmp|프로토콜]] |
| **[[461_http_stateless_connection_oriented|HTTP]]-CoAP [[264_proxy_pattern_surrogate_access_control|프록시]]** | 웹↔[[101_iot_concept|IoT]] 연동 게이트웨이 |

### 📈 관련 키워드 및 발전 흐름도

```text
[HTTP (웹 표준, 1991~)]
    │
    ▼
[CoAP RFC 7252 (2014) — IoT용 경량 RESTful]
    │
    ▼
[LwM2M (2015~) — CoAP 기반 디바이스 관리]
    │
    ▼
[CoAP over TCP (RFC 8323, 2018) — NAT 환경 대응]
    │
    ▼
[현재: CoAP + MQTT + Matter — IoT 프로토콜 생태계]
```

### 👶 어린이를 위한 3줄 비유 설명
1. HTTP는 대형 트럭이에요. 짐([[001_dikw_pyramid|데이터]])은 많이 나르지만 **작은 골목(센서)에는 못 들어가요**.
2. CoAP은 **자전거 택배**예요. 골목골목(제약 디바이스)을 다니면서 물건을 **가져다주고(GET) 놓아주고(PUT)** 해요.
3. MQTT는 **라디오 방송**이에요. 방송국(Broker)이 뉴스(센서 [[001_dikw_pyramid|데이터]])를 구독자에게 내보내요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 120 / 552

← **이전**: [[119_mqtt_qos_levels|119. MQTT QoS 레벨 (QoS 0/1/2) - IoT 메시지 전달 보장 수준]]
**다음**: [[121_lwm2m_lightweight_m2m|121. LwM2M (Lightweight M2M) - OMA 표준 IoT 디바이스 관리 프로토콜]] →

---
