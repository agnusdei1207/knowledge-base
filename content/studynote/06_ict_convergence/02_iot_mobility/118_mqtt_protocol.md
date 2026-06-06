---
title: "118. Mqtt Protocol"
date: "2026-04-19"
tags:
  - "studynote-ict-convergence"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MQTT는 <strong>Pub/Sub(발행/구독) 기반 경량 메시징 <a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a></strong>로, [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)이 제한된 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 환경에서 센서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 <strong>최소 2바이트 헤더</strong>로 전송할 수 있는 사실상 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 메시징 표준이다.
> 2. **가치**: HTTP는 헤더만 수백 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)이지만, MQTT는 <strong>고정 헤더 2바이트 + 가변 헤더</strong>로 페이로드 대비 오버헤드가 극히 작아 저전력·저대역폭 디바이스에 최적이다.
> 3. **판단 포인트**: [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 3단계(0: At most once, 1: At least once, 2: Exactly once)와 <strong>Retained Message·Last Will·Topic 계층 구조</strong>를 이해하고, [MQTT](/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) 5.0의 Shared Subscription(로드밸런싱)을 숙지해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    MQTT Pub/Sub 아키텍처                               |
+-------------------------------------------------------+
|  [Publisher]                [Subscriber]               |
|   센서 --publish---> Broker --subscribe---> 서버       |
|   Topic: home/sensor/temp   Topic: home/sensor/#     |
|   Payload: {"temp": 25.3}                             |
|                                                       |
|  Broker (Mosquitto, EMQX): 메시지 중개·QoS 보장      |
|  Publisher는 Subscriber를 몰라도 됨 (느슨한 결합)    |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: MQTT는 우체국(Broker) 시스템이다. 보내는 사람(Publisher)은 우편함(Topic)에 넣고, 받는 사람(Subscriber)은 원하는 우편함을 구독한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 3단계

| [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) | 보장 | 오버헤드 | 용도 |
|:---|:---|:---|:---|
| **0** | At most once (최선) | **최소** | 센서 주기 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| **1** | At least once (최소 1회) | 중간 | 알림·이벤트 |
| **2** | Exactly once (정확히 1회) | **최대** | 결제·제어 명령 |

### [MQTT](/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) vs [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)

| 비교 | [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) | [MQTT](/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) |
|:---|:---|:---|
| **헤더** | 수백 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) | **2바이트~** |
| **패턴** | Request/Response | **Pub/Sub** |
| **연결** | 매번 새로 | **지속 연결 (Keep-alive)** |
| <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a> 적합</strong> | 부적합 | **최적** |

- **📢 섹션 요약 비유**: HTTP는 매번 전화를 걸어야 하는 통화이고, MQTT는 한 번 연결한 무전기로 계속 대화하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [MQTT](/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) | [CoAP](/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/) | AMQP |
|:---|:---|:---|:---|
| **전송** | [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) | [UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) | [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) |
| **패턴** | Pub/Sub | Req/Res | Pub/Sub + [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/) |
| **헤더** | 2B | 4B | 8B+ |
| **용도** | <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a> 센서</strong> | [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 제어 | 엔터프라이즈 MQ |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [MQTT](/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) 5.0 주요 개선
- **Shared Subscription**: 같은 Topic을 여러 Subscriber가 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 (로드밸런싱).
- **Request/Response**: Pub/Sub 위에 [RPC](/studynote/02_operating_system/02_process_thread/126_rpc/) 패턴 구현.
- **Properties**: 메시지에 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)(Content-Type, Correlation [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 추가.

---

## Ⅴ. 기대효과 및 결론

| 지표 | [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) | [MQTT](/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) | 개선 |
|:---|:---|:---|:---|
| [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) | 높음 | <strong>1/<a href="/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/">10</a>~1/100</strong> | 대폭 절감 |
| 배터리 | 빠른 소모 | **절약 (지속 연결)** | [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 적합 |
| 실시간성 | [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) 간격 | **즉시 Push** | 실시간 |

MQTT는 AWS [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) Core·Azure [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) [Hub](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)·Google Cloud IoT의 기본 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이며, [MQTT](/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) over QUIC로 더욱 빠른 전송이 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Pub/Sub** | MQTT의 핵심 메시징 패턴 |
| <strong><a href="/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/">QoS</a></strong> | [메시지 전달](/studynote/02_operating_system/02_process_thread/119_message_passing/) 보장 수준 (0/1/2) |
| **Broker** | Mosquitto, EMQX 등 메시지 중개 서버 |
| **Topic** | 메시지 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 경로 (계층 구조) |
| <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/">CoAP</a></strong> | [UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 기반 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 대안 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[MQTT v3.1 (1999, IBM) — IoT 경량 메시징 시작]
    |
    v
[OASIS 표준화 (2014) — MQTT 3.1.1]
    |
    v
[AWS IoT Core (2015~) — MQTT 클라우드 네이티브]
    |
    v
[MQTT 5.0 (2019) — Shared Sub, Properties]
    |
    v
[현재: MQTT over QUIC — 고속 전송·멀티플렉싱]
```

### 👶 어린이를 위한 3줄 비유 설명
1. MQTT는 **우체국(Broker)** 시스템이에요. 센서가 편지([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 우편함(Topic)에 넣어요.
2. 서버는 원하는 우편함을 <strong>구독</strong>해서 편지가 오면 바로 읽어요.
3. 편지 봉투(헤더)가 **아주 작아서(2바이트)** 작은 센서도 쉽게 보낼 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 118 / 552

<- **이전**: [117. 6LoWPAN (IPv6 over Low-Power WPAN) - IoT IPv6 압축·적응 계층](/studynote/06_ict_convergence/02_iot_mobility/117_6lowpan_iot_ipv6/)
**다음**: [119. MQTT QoS 레벨 (QoS 0/1/2) - IoT 메시지 전달 보장 수준](/studynote/06_ict_convergence/02_iot_mobility/119_mqtt_qos_levels/) ->

---
