+++
weight = 118
title = "118. MQTT 프로토콜 (Message Queuing Telemetry Transport) - IoT 경량 메시징"
date = "2026-04-19"
[extra]
categories = "studynote-ict-convergence"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MQTT는 **Pub/Sub(발행/구독) 기반 경량 메시징 [[295_protocol_field_tcp_udp_icmp|프로토콜]]**로, [[140_bandwidth|대역폭]]이 제한된 [[101_iot_concept|IoT]] 환경에서 센서 [[001_dikw_pyramid|데이터]]를 **최소 2바이트 헤더**로 전송할 수 있는 사실상 [[101_iot_concept|IoT]] 메시징 표준이다.
> 2. **가치**: HTTP는 헤더만 수백 [[074_byte|바이트]]이지만, MQTT는 **고정 헤더 2바이트 + 가변 헤더**로 페이로드 대비 오버헤드가 극히 작아 저전력·저대역폭 디바이스에 최적이다.
> 3. **판단 포인트**: [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] 3단계(0: At most once, 1: At least once, 2: Exactly once)와 **Retained Message·Last Will·Topic 계층 구조**를 이해하고, [[622_mqtt_publish_subscribe_qos|MQTT]] 5.0의 Shared Subscription(로드밸런싱)을 숙지해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    MQTT Pub/Sub 아키텍처                               │
├───────────────────────────────────────────────────────┤
│  [Publisher]                [Subscriber]               │
│   센서 ──publish──▶ Broker ──subscribe──▶ 서버       │
│   Topic: home/sensor/temp   Topic: home/sensor/#     │
│   Payload: {"temp": 25.3}                             │
│                                                       │
│  Broker (Mosquitto, EMQX): 메시지 중개·QoS 보장      │
│  Publisher는 Subscriber를 몰라도 됨 (느슨한 결합)    │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: MQTT는 우체국(Broker) 시스템이다. 보내는 사람(Publisher)은 우편함(Topic)에 넣고, 받는 사람(Subscriber)은 원하는 우편함을 구독한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] 3단계

| [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] | 보장 | 오버헤드 | 용도 |
|:---|:---|:---|:---|
| **0** | At most once (최선) | **최소** | 센서 주기 [[001_dikw_pyramid|데이터]] |
| **1** | At least once (최소 1회) | 중간 | 알림·이벤트 |
| **2** | Exactly once (정확히 1회) | **최대** | 결제·제어 명령 |

### [[622_mqtt_publish_subscribe_qos|MQTT]] vs [[461_http_stateless_connection_oriented|HTTP]]

| 비교 | [[461_http_stateless_connection_oriented|HTTP]] | [[622_mqtt_publish_subscribe_qos|MQTT]] |
|:---|:---|:---|
| **헤더** | 수백 [[074_byte|바이트]] | **2바이트~** |
| **패턴** | Request/Response | **Pub/Sub** |
| **연결** | 매번 새로 | **지속 연결 (Keep-alive)** |
| **[[101_iot_concept|IoT]] 적합** | 부적합 | **최적** |

- **📢 섹션 요약 비유**: HTTP는 매번 전화를 걸어야 하는 통화이고, MQTT는 한 번 연결한 무전기로 계속 대화하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[622_mqtt_publish_subscribe_qos|MQTT]] | [[120_coap_constrained_application_protocol|CoAP]] | AMQP |
|:---|:---|:---|:---|
| **전송** | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] | [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] |
| **패턴** | Pub/Sub | Req/Res | Pub/Sub + [[058_queue|Queue]] |
| **헤더** | 2B | 4B | 8B+ |
| **용도** | **[[101_iot_concept|IoT]] 센서** | [[101_iot_concept|IoT]] 제어 | 엔터프라이즈 MQ |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[622_mqtt_publish_subscribe_qos|MQTT]] 5.0 주요 개선
- **Shared Subscription**: 같은 Topic을 여러 Subscriber가 [[136_variance|분산]] 처리 (로드밸런싱).
- **Request/Response**: Pub/Sub 위에 [[126_rpc|RPC]] 패턴 구현.
- **Properties**: 메시지에 [[012_metadata|메타데이터]](Content-Type, Correlation [[001_dikw_pyramid|Data]]) 추가.

---

## Ⅴ. 기대효과 및 결론

| 지표 | [[461_http_stateless_connection_oriented|HTTP]] [[448_polling_programmed_io|폴링]] | [[622_mqtt_publish_subscribe_qos|MQTT]] | 개선 |
|:---|:---|:---|:---|
| [[140_bandwidth|대역폭]] | 높음 | **1/[[489_raid_10_hybrid|10]]~1/100** | 대폭 절감 |
| 배터리 | 빠른 소모 | **절약 (지속 연결)** | [[101_iot_concept|IoT]] 적합 |
| 실시간성 | [[448_polling_programmed_io|폴링]] 간격 | **즉시 Push** | 실시간 |

MQTT는 AWS [[101_iot_concept|IoT]] Core·Azure [[101_iot_concept|IoT]] [[152_hub_dummy_switching_intelligent|Hub]]·Google Cloud IoT의 기본 [[295_protocol_field_tcp_udp_icmp|프로토콜]]이며, [[622_mqtt_publish_subscribe_qos|MQTT]] over QUIC로 더욱 빠른 전송이 [[216_progress_in_synchronization|진행]] 중이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Pub/Sub** | MQTT의 핵심 메시징 패턴 |
| **[[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]]** | [[119_message_passing|메시지 전달]] 보장 수준 (0/1/2) |
| **Broker** | Mosquitto, EMQX 등 메시지 중개 서버 |
| **Topic** | 메시지 [[339_routing_overview_best_path_selection|라우팅]] 경로 (계층 구조) |
| **[[120_coap_constrained_application_protocol|CoAP]]** | [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 기반 [[101_iot_concept|IoT]] 대안 [[295_protocol_field_tcp_udp_icmp|프로토콜]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[MQTT v3.1 (1999, IBM) — IoT 경량 메시징 시작]
    │
    ▼
[OASIS 표준화 (2014) — MQTT 3.1.1]
    │
    ▼
[AWS IoT Core (2015~) — MQTT 클라우드 네이티브]
    │
    ▼
[MQTT 5.0 (2019) — Shared Sub, Properties]
    │
    ▼
[현재: MQTT over QUIC — 고속 전송·멀티플렉싱]
```

### 👶 어린이를 위한 3줄 비유 설명
1. MQTT는 **우체국(Broker)** 시스템이에요. 센서가 편지([[001_dikw_pyramid|데이터]])를 우편함(Topic)에 넣어요.
2. 서버는 원하는 우편함을 **구독**해서 편지가 오면 바로 읽어요.
3. 편지 봉투(헤더)가 **아주 작아서(2바이트)** 작은 센서도 쉽게 보낼 수 있답니다!
