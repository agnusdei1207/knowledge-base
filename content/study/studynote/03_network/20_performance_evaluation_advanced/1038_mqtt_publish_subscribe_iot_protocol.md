---
title: 1038. MQTT 프로토콜
date: '2026-05-08'
tags:
- studynote-network
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[622_mqtt_publish_subscribe_qos|MQTT]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 [[282_performance_tactics|성능]] 평가와 고급 분석에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [[622_mqtt_publish_subscribe_qos|MQTT]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]을 이해하면 측정 정확도과 모델 적합성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- 462번 HTTP는 폰([[003_audit_stakeholders|Client]])이 온도계(Server)에게 질문(Request)을 던져야만 대답(Response)을 해줍니다.
- 방 안의 수백 개 센서 온도를 알고 싶으면, 폰이 1초마다 수백 번의 접속과 질문을 날려대야([[747_io_polling_overhead|Polling]]) 해서 회선 낭비와 배터리 소모(오버헤드)가 재앙 수준이었습니다.

```text
[ONS 구조]
    │
    ▼
[MQTT 프로토콜]
    │
    └──▶ [CoAP 프로토콜 및 REST 인터페이스]
```

- **📢 섹션 요약 비유**: [[622_mqtt_publish_subscribe_qos|MQTT]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [[170_selectivity_cardinality_distribution_tuning|선택도]] 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

- **개념**: 제한된 [[140_bandwidth|대역폭]](쓰레기 같은 통신망)과 불안정한 환경(배터리 쪼들리는 센서)에서, 가볍고 빠르게 사물 간([[602_m2m_machine_to_machine_telemetry|M2M]], [[101_iot_concept|IoT]]) 센서 [[001_dikw_pyramid|데이터]]를 주고받기 위해 IBM이 1999년에 만든 **초경량 메시징 [[295_protocol_field_tcp_udp_icmp|프로토콜]]**입니다. (현재 ISO 표준)
- [[461_http_stateless_connection_oriented|HTTP]] 패킷 껍데기는 엄청 크고 무겁지만, MQTT의 헤더(껍데기)는 고작 **2바이트**로 깃털처럼 가벼워 저전력 통신망에 최고의 효율을 뽑습니다.

센서와 폰이 서로를 몰라도 통신이 되는 완벽한 '비동기 3자 분리' 아키텍처입니다.

### 1. 3대 핵심 등장인물
1. **Publisher (발행자)**: [[001_dikw_pyramid|데이터]]를 만드는 센서 (온도계). "나 온도 [[001_dikw_pyramid|데이터]] 던진다!"
2. **Subscriber (구독자)**: [[001_dikw_pyramid|데이터]]를 보고 싶어 하는 폰 (나의 앱). "온도 [[001_dikw_pyramid|데이터]] 들어오면 나한테 줘!"
3. **Broker (브로커 / 우체국 서버) 🌟**: 중간에 서서 모든 메시지를 받아서 분류하고 나눠주는 핵심 중계 서버입니다. (센서와 폰은 서로의 IP 주소를 전혀 모른 채, 오직 브로커하고만 연결됩니다.)

### 2. 토픽 (Topic) [[339_routing_overview_best_path_selection|라우팅]] - 카테고리 분배
- 우체국(브로커)은 편지를 어떻게 분류할까요? 주소가 아니라 **'토픽(관심사)'**으로 분류합니다.
- **동작**:
  1. 폰(구독자)이 브로커에게 말합니다. "나 `Home/LivingRoom/Temp` (거실 온도) 토픽 구독할게!"
  2. 거실 온도계(발행자)가 온도를 재고 브로커에게 던집니다. "[토픽: `Home/LivingRoom/Temp`] 메시지: 24도!"
  3. 브로커는 이 토픽을 구독 중인 모든 폰들에게 **동시에 카톡 푸시 알람을 쏘듯 24도라는 [[001_dikw_pyramid|데이터]]를 확 뿌려버립니다.**

```text
[ONS 구조]
    │
    ▼
[MQTT 프로토콜]
    │
    └──▶ [CoAP 프로토콜 및 REST 인터페이스]
```

- **📢 섹션 요약 비유**: [[622_mqtt_publish_subscribe_qos|MQTT]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

[[622_mqtt_publish_subscribe_qos|MQTT]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [[1037_ons_object_name_service_rfid_dns|ONS]] 구조가 기반 조건을 만든다면, [[622_mqtt_publish_subscribe_qos|MQTT]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 그 위에서 핵심 메커니즘을 구현하고, [[120_coap_constrained_application_protocol|CoAP]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 및 [[156_rest_representational_state_transfer|REST]] 인터페이스는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 측정 정확도과 모델 적합성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [[1037_ons_object_name_service_rfid_dns|ONS]] 구조의 기반 정리 | [[622_mqtt_publish_subscribe_qos|MQTT]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]의 핵심 동작 | [[120_coap_constrained_application_protocol|CoAP]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 및 [[156_rest_representational_state_transfer|REST]] 인터페이스의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 측정 정확도 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [[396_validation|확인]] | 현재 메커니즘의 적합성 판단 | 운영·확장 [[268_strategy_pattern|전략]] 연결 |

- **📢 섹션 요약 비유**: [[622_mqtt_publish_subscribe_qos|MQTT]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

네트워크가 쓰레기 같을 때 메시지가 사라지는 걸 막기 위해, 배달 [[396_validation|확인]]증([[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]]) 레벨을 폰에서 조절할 수 있습니다.

- **[[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] 0 (At most once, 최대 1번)**:
  - "보냈어! 가다 잃어버렸다고? 알빠노!" 한 번 툭 던지고 마는 가장 가볍고 무책임한 방식 (온도 [[001_dikw_pyramid|데이터]]에 적합).
- **[[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] 1 (At least once, 최소 1번)**:
  - 우체국이 "잘 받았음(ACK)" 도장을 찍어줄 때까지 온도계가 똑같은 [[001_dikw_pyramid|데이터]]를 **계속 끈질기게 다시 보냅니다.** 메시지 분실은 절대 없지만, 우체국이 똑같은 온도를 중복해서 여러 번 받을 수 있습니다.
- **[[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] 2 (Exactly once, 정확히 1번)**:
  - 무조건 딱 한 번만 완벽하게 도착하도록, 보내고-[[396_validation|확인]]하고-지우고-완료하는 미친 4단계 [[396_validation|확인]] 절차를 밟습니다. 통신은 제일 무겁지만, 돈과 직결된 과금 센서([[024_gas|가스]] 검침 결제)에서 절대 오류가 안 나게 할 때 씁니다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: [[461_http_stateless_connection_oriented|HTTP]] 방식이 **'엄마(폰)가 아들(온도계) 방에 1분마다 문 열고 들어가 "공부 다 했어?" 묻는 잔소리 통신'**이라면, **[[622_mqtt_publish_subscribe_qos|MQTT]](발행-구독 모델)**는 중간에 **'거실 칠판(브로커 서버)'**을 하나 놔두는 기적의 독립 생활입니다. 엄마(구독자)는 칠판에 "아들 수학 점수 칸 관심 있음"이라고 적어둡니다(토픽 구독). 아들(발행자)은 엄마 방에 찾아갈 필요 없이, 수학 시험을 치고 오면 그냥 거실 칠판 수학 칸에 "100점"이라고 적어놓고 쿨하게 자기 방으로 갑니다(발행). 그럼 칠판 관리자(브로커)가 알아서 엄마 방 문에 "아들 100점 맞음!"이라고 카톡 알림을 쏴줍니다. 엄마와 아들이 얼굴 한 번 보지 않고(IP 독립성), 엄마가 아들 방문을 두드릴 필요도 없이([[747_io_polling_overhead|Polling]] 제로), 정보가 업데이트되는 즉시 칠판을 통해 자동으로 뿌려지는 가장 이상적인 짠돌이 스마트홈의 [[001_dikw_pyramid|데이터]] 우체국 시스템입니다.

---

## Ⅴ. 기대효과 및 결론

[[622_mqtt_publish_subscribe_qos|MQTT]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 [[282_performance_tactics|성능]] 평가와 고급 분석을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 측정 정확도 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [[120_coap_constrained_application_protocol|CoAP]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 및 [[156_rest_representational_state_transfer|REST]] 인터페이스, [[190_ai_llm_requirements_specification|AI]] 기반 [[282_performance_tactics|성능]] 예측, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [[190_ai_llm_requirements_specification|AI]] 기반 [[282_performance_tactics|성능]] 예측 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [[622_mqtt_publish_subscribe_qos|MQTT]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[1037_ons_object_name_service_rfid_dns|ONS]] 구조 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [[139_throughput|처리량]] ([[139_throughput|Throughput]]) | 실제 전달 [[282_performance_tactics|성능]]을 나타내는 대표 지표다. |
| [[015_지연_데이터_관점|지연]] ([[141_latency|Latency]]) | 사용자 체감 품질을 좌우한다. |
| [[120_coap_constrained_application_protocol|CoAP]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 및 [[156_rest_representational_state_transfer|REST]] 인터페이스 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: ONS 구조]
    │
    ▼
[현재 개념: MQTT 프로토콜]
    │
    ├──▶ [확장 A: CoAP 프로토콜 및 REST 인터페이스]
    └──▶ [확장 B: AI 기반 성능 예측]
```

[[622_mqtt_publish_subscribe_qos|MQTT]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]는 [[1037_ons_object_name_service_rfid_dns|ONS]] 구조에서 출발해 현재 메커니즘을 정교화하고, 이후 [[120_coap_constrained_application_protocol|CoAP]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 및 [[156_rest_representational_state_transfer|REST]] 인터페이스와 [[190_ai_llm_requirements_specification|AI]] 기반 [[282_performance_tactics|성능]] 예측 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 달리기 시합에서 누가 얼마나 빨랐는지 재려면 초시계와 기록표가 필요해요.
2. 이 개념은 네트워크가 어디서 느려졌는지 숫자로 찾아내는 도구예요.
3. 그래서 막연히 고치는 대신 가장 중요한 곳부터 똑똑하게 손볼 수 있어요.
