+++
title = "489. MQTT Pub/Sub와 CoAP REST 경량 프로토콜 (MQTT CoAP IoT Lightweight Protocols)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [MQTT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/)(Message Queuing Telemetry Transport)와 [CoAP](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/)([Constrained Application Protocol](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/))은 제한된 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 환경을 위해 설계된 두 가지 경량 메시지 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)로, MQTT는 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 기반 Pub/Sub 패턴, CoAP는 [UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 기반 RESTful 패턴을 사용한다.
> 2. **가치**: [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/[WebSocket](/knowledge-base/studynote/03_network/09_application_layer_web_email/480_websocket_full_duplex/) 대비 수십 배 낮은 오버헤드로 수백만 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 기기의 안정적·저전력 메시지 교환을 실현하며, 두 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 특성 차이를 이해해야 올바른 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 아키텍처를 설계할 수 있다.
> 3. **판단 포인트**: 안정적인 이벤트 스트림·다수 구독자 시스템엔 [MQTT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/), 자원 제약 기기의 단순 요청-응답·배터리 절약엔 CoAP가 적합하다. 두 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 혼합하는 게이트웨이 패턴도 실무에서 자주 사용된다.

---

## Ⅰ. 개요 및 필요성

<strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a> <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a>의 필요성</strong>

HTTP는 헤더 오버헤드가 수백~수천 [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)에 달해, RAM이 수십 KB에 불과한 MCU(Micro Controller Unit)에서 동작하기 어렵다. [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 환경에서는 아래 조건을 모두 만족하는 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이 필요하다.

- 패킷 크기: 수 [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 수준의 최소 헤더
- [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/): 불안정한 무선 환경에서도 전달 보장
- 저전력: 배터리 기기에서 수년간 동작
- 확장성: 수백만 기기 동시 접속

- **📢 섹션 요약 비유**: HTTP는 백과사전 편지다. 질문 하나에 표지·목차·각주까지 다 포함해서 보낸다. [MQTT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/)/CoAP는 엽서다. 핵심 내용 한 줄만 담아 가볍고 빠르게 전달한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+------------------------------------------------------------+
|         MQTT Pub/Sub 구조 vs CoAP 요청-응답 구조 비교         |
+--------------------------+---------------------------------+
|         MQTT             |           CoAP                  |
|  [Publisher(발행자)]      |  [CoAP Client]                  |
|       |                  |       | GET/PUT/POST/DELETE      |
|       v  토픽(Topic)      |       v                         |
|  [Broker(브로커)]         |  [CoAP Server]                  |
|       |                  |  (자원 URI: /sensor/temp)        |
|       v  구독(Subscribe)  |                                 |
|  [Subscriber(구독자)]     |  [Observe 옵션]                  |
|  (다수의 클라이언트)        |  (변경 시 자동 알림 -> Push)       |
+--------------------------+---------------------------------+
```

### [MQTT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) vs [CoAP](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/) 핵심 비교표

| 항목 | [MQTT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) | [CoAP](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/) |
|:---:|:---:|:---:|
| 전송 계층 | [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) | [UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) |
| 통신 패턴 | Pub/Sub (브로커 필수) | RESTful 요청-응답 |
| 헤더 크기 | 최소 2바이트 | 4바이트 |
| [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) | [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 기반 보장 | CON([확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/))/NON(비확인) 옵션 |
| [멀티캐스트](/knowledge-base/studynote/03_network/06_network_layer_ip/298_ip_classes_a_b_c_d_multicast_e_experimental/) | 미지원 | 지원 ([UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 특성) |
| 브로커 | 필수 (Mosquitto, HiveMQ) | 불필요 ([P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) 가능) |
| 보안 | [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) | [DTLS](/knowledge-base/studynote/03_network/12_iot_wpan_edge/644_dtls_datagram_tls_coap_security/) |
| 적합 환경 | 안정적 네트워크, 다수 구독 | 제약적 기기, 저전력 |

<strong><a href="/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/">MQTT</a> <a href="/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/">QoS</a>(<a href="/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/">Quality of Service</a>) 3단계</strong>

- <strong><a href="/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/">QoS</a> 0 (At most once)</strong>: 전달 보장 없음. 손실 허용 센서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/).
- <strong><a href="/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/">QoS</a> 1 (At least once)</strong>: 최소 1회 전달. 중복 가능. 대부분의 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 이벤트.
- <strong><a href="/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/">QoS</a> 2 (Exactly once)</strong>: 정확히 1회 전달. 금융·의료 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/). 오버헤드 최대.

<strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/">CoAP</a> 특징</strong>

- **Observe 옵션**: 클라이언트가 서버 자원을 구독하면, 값 변경 시 서버가 자동으로 알림 전송. MQTT의 Push와 유사한 효과를 UDP로 구현.
- **CON/NON 메시지**: CON(Confirmable)은 ACK 수신까지 재전송. NON(Non-confirmable)은 [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 전송, 저전력.

- **📢 섹션 요약 비유**: [MQTT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) 브로커는 라디오 방송국이다. 기상청(Publisher)이 날씨를 방송하면, 수백만 라디오(Subscriber)가 동시에 수신한다. CoAP는 편의점 주문이다. 손님([Client](/knowledge-base/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/))이 "콜라 주세요(GET)" 하면 직원(Server)이 바로 건네준다.

---

## Ⅲ. 비교 및 연결

<strong>MQTT와 <a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/">CoAP</a> 선택 기준</strong>

| 조건 | 선택 |
|:---|:---:|
| 다수의 구독자가 동일 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 필요 | [MQTT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) |
| 기기가 초소형·배터리 극제약 | [CoAP](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/) |
| 안정적인 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 네트워크 환경 | [MQTT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) |
| 불안정한 무선 환경, [멀티캐스트](/knowledge-base/studynote/03_network/06_network_layer_ip/298_ip_classes_a_b_c_d_multicast_e_experimental/) 필요 | [CoAP](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/) |
| 클라우드 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 플랫폼 연동 | [MQTT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) (표준화 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중) |
| [M2M](/knowledge-base/studynote/03_network/12_iot_wpan_edge/602_m2m_machine_to_machine_telemetry/)(Machine-to-Machine) [직접 통신](/knowledge-base/studynote/02_operating_system/02_process_thread/120_direct_communication/) | [CoAP](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/) |

**혼합 아키텍처**: 현장 기기([CoAP](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/)) ↔ 엣지 게이트웨이([CoAP](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/)->[MQTT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) 변환) ↔ 클라우드 [MQTT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) 브로커. 제약 기기는 CoAP로 게이트웨이에 보내고, 게이트웨이가 MQTT로 변환해 클라우드에 전달.

- **📢 섹션 요약 비유**: MQTT와 CoAP를 함께 쓰는 것은 지역 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)([CoAP](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/))와 고속버스([MQTT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/))를 환승하는 것이다. 마을에서 지역 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)([CoAP](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/))로 나오고, 터미널(게이트웨이)에서 고속버스([MQTT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/))로 갈아탄다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a> 선택 시나리오</strong>

| 시나리오 | [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | 이유 |
|:---|:---:|:---|
| 스마트홈 조명 상태 실시간 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) | [MQTT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) | 다수 앱 구독, 안정 네트워크 |
| 초소형 온도 센서 (CR2032 배터리) | [CoAP](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/) NON | 최소 전력, [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) |
| 공장 생산 라인 이벤트 스트림 | [MQTT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) [QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 1 | 이벤트 유실 불가 |
| 설비 제어 명령 전송 ([확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 필수) | [MQTT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) [QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 2 / [CoAP](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/) CON | 정확 1회 전달 |

**보안 포인트**: MQTT는 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3, CoAP는 [DTLS](/knowledge-base/studynote/03_network/12_iot_wpan_edge/644_dtls_datagram_tls_coap_security/)([Datagram TLS](/knowledge-base/studynote/03_network/12_iot_wpan_edge/644_dtls_datagram_tls_coap_security/)). 인증서 저장 불가 기기는 [PSK](/knowledge-base/studynote/09_security/03_network_security/142_psk_pre_shared_key/)(Pre-Shared [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) 방식 사용.

- **📢 섹션 요약 비유**: [QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 선택은 택배 보험 선택이다. 보험 없음([QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 0)은 싸지만 분실 위험, 기본 보험([QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 1)은 재배송은 하지만 중복 도착 가능, 풀 보험([QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 2)은 정확하지만 수수료가 가장 비싸다.

---

## Ⅴ. 기대효과 및 결론

MQTT와 CoAP는 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 생태계의 메시지 교환 표준으로 자리 잡았다. AWS [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) Core·Azure [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) [Hub](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) 모두 MQTT를 네이티브 지원하며, CoAP는 [LwM2M](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/121_lwm2m_lightweight_m2m/)([Lightweight M2M](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/121_lwm2m_lightweight_m2m/)) 디바이스 관리 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 기반이다. 두 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 특성과 트레이드오프를 명확히 이해하는 것이 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 아키텍처 설계의 기본기다.

- **📢 섹션 요약 비유**: MQTT와 CoAP는 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 세계의 한글과 영어다. 상황에 맞게 골라 쓰면 되고, 둘 다 알면 어떤 시스템도 설계할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [MQTT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) Broker | Mosquitto, HiveMQ, EMQ · 메시지 중계 서버 |
| [QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 3단계 | 0/1/2, 오버헤드 · 전달 보장 수준 |
| [CoAP](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/) Observe | Push, [UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) · 서버 자원 변경 자동 알림 |
| [LwM2M](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/121_lwm2m_lightweight_m2m/) | [CoAP](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/) 기반 · OMA 기기 관리 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
| [DTLS](/knowledge-base/studynote/03_network/12_iot_wpan_edge/644_dtls_datagram_tls_coap_security/) | [CoAP](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/) 보안 · [UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 위 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 계층 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Mosquitto · HiveMQ] -> [MQTT Pub · Sub] -> [CoAP 보안 · UDP 위 TLS 계층]
```

### 👶 어린이를 위한 3줄 비유 설명

1. MQTT는 학교 방송 시스템이에요. 선생님(Publisher)이 마이크(Broker)에 말하면 전교생(Subscriber)이 동시에 들을 수 있어요.
2. CoAP는 학생증 조회기예요. 카드 대면(요청)하면 즉시 결과(응답)를 알려줘요. 따로 방송국이 없어도 돼요.
3. QoS는 알림 설정이에요. 중요한 수업 알림([QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 2)은 반드시 읽음 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/), 날씨 알림([QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 0)은 그냥 와도 되고 없어져도 괜찮아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 489 / 552

<- **이전**: [488. LPWAN: LoRa, NB-IoT 면허/비면허 비교 (LPWAN: LoRa NB-IoT Licensed Unlicensed)](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/488_lpwan_lora_nb_iot_licensed_unlicensed/)
**다음**: [490. Matter 스마트홈 상호 운용성 표준 (Matter Smart Home Interoperability Standard)](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/490_matter_smart_home_interoperability_standard/) ->

---
