---
title: "119. MQTT QoS 레벨 (QoS 0/1/2) - IoT 메시지 전달 보장 수준"
date: "2026-04-19"
tags:
  - "studynote-ict-convergence"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [MQTT](/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/)([Quality of Service](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/))는 [메시지 전달](/studynote/02_operating_system/02_process_thread/119_message_passing/) 보장 수준을 3단계(0: 최대 1회, 1: 최소 1회, 2: 정확히 1회)로 정의하며, <strong>Publisher->Broker와 Broker->Subscriber 각각에 독립적으로 <a href="/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a></strong>된다.
> 2. **가치**: 온도 센서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 0, 유실 허용)와 결제 명령([QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 2, 정확히 1회 필수)처럼, <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>의 중요도에 따라 전달 보장 수준을 선택</strong>하여 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)·배터리·[신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)의 균형을 맞춘다.
> 3. **판단 포인트**: [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 2는 <strong>4-way 핸드셰이크(PUBLISH->PUBREC->PUBREL->PUBCOMP)</strong>로 오버헤드가 크므로, 대부분의 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 시나리오는 <strong><a href="/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/">QoS</a> 1(중복 허용, 유실 방지)</strong>이 실용적 최적점이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    QoS 레벨별 핸드셰이크                              |
+-------------------------------------------------------+
|  [QoS 0 — Fire and Forget]                            |
|   Pub --PUBLISH---> Broker  (끝, 확인 없음)           |
|                                                       |
|  [QoS 1 — At Least Once]                              |
|   Pub --PUBLISH---> Broker --PUBACK---> Pub            |
|   (PUBACK 없으면 재전송 -> 중복 가능)                  |
|                                                       |
|  [QoS 2 — Exactly Once]                               |
|   Pub --PUBLISH---> Broker --PUBREC---> Pub            |
|   Pub --PUBREL---> Broker --PUBCOMP---> Pub            |
|   (4-way 핸드셰이크, 정확히 1회 보장)                 |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 0은 엽서(도착 보장 없음), [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 1은 등기우편(배달 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/), 중복 가능), [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 2는 내용증명(정확히 1회, 증거 남김)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 레벨 비교

| [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) | 보장 | 핸드셰이크 | 오버헤드 | 적합 |
|:---|:---|:---|:---|:---|
| **0** | 최대 1회 (유실 가능) | 1회 | **최소** | 센서 주기 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| **1** | 최소 1회 (중복 가능) | 2회 | 중간 | <strong>대부분 <a href="/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a></strong> |
| **2** | 정확히 1회 | **4회** | 최대 | 결제·제어 명령 |

### [멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/)([Idempotency](/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/)) 설계
[QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 1은 중복 전달이 가능하므로, 수신 측에서 <strong>메시지 ID로 중복 필터링(멱등 처리)</strong>하면 [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 2의 효과를 얻을 수 있다.

- **📢 섹션 요약 비유**: [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 1 + [멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/)은 "같은 택배가 2번 와도 1번만 수령처리"하는 것이다. [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 2보다 가볍게 같은 효과를 낸다.

---

## Ⅲ. 비교 및 연결

| 비교 | [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 0 | [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 1 | [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 2 |
|:---|:---|:---|:---|
| **전력** | 최소 | 중간 | 높음 |
| <strong><a href="/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">대역폭</a></strong> | 최소 | 중간 | 높음 |
| <strong><a href="/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/">신뢰성</a></strong> | 낮음 | **높음** | 최고 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 시나리오별 [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 선택
- **온도/습도 센서**: [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 0 (5초마다 전송, 1개 유실 무관).
- **화재 알람**: [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 1 (반드시 도달, 중복 OK).
- **스마트 도어락 제어**: [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 2 (정확히 1회 열림/닫힘).

---

## Ⅴ. 기대효과 및 결론

[MQTT](/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/) QoS는 IoT의 <strong>"<a href="/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/">신뢰성</a> vs 효율" 트레이드오프를 3단계로 단순화</strong>한 우아한 설계이며, 실무에서는 [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 1 + 멱등 처리가 가장 실용적인 조합이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/">QoS</a> 0</strong> | Fire and Forget, 최저 오버헤드 |
| <strong><a href="/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/">QoS</a> 1</strong> | At Least Once, 실용적 최적점 |
| <strong><a href="/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/">QoS</a> 2</strong> | Exactly Once, 4-way 핸드셰이크 |
| <strong><a href="/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/">멱등성</a></strong> | [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 1 중복을 안전하게 처리하는 설계 |
| <strong><a href="/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/">MQTT</a> 5.0</strong> | Shared Subscription 등 [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 개선 |

### 📈 관련 키워드 및 발전 흐름도

```text
[MQTT v3.1 (1999) — QoS 0/1/2 정의]
    |
    v
[MQTT 3.1.1 (2014, OASIS) — 표준화]
    |
    v
[QoS 1 + 멱등 패턴 (실무 Best Practice)]
    |
    v
[MQTT 5.0 (2019) — Shared Subscription]
    |
    v
[현재: MQTT over QUIC — 전송 계층 신뢰성 강화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 0은 <strong>엽서</strong>예요. 보내면 끝이고 도착할지 모르지만 **가장 가벼워요**.
2. [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 1은 <strong>등기우편</strong>이에요. 배달 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)을 받지만 **같은 편지가 2번** 올 수도 있어요.
3. [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 2는 <strong>내용증명</strong>이에요. 정확히 **1번만** 도착하지만 절차가 복잡해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 119 / 552

<- **이전**: [118. MQTT 프로토콜 (Message Queuing Telemetry Transport) - IoT 경량 메시징](/studynote/06_ict_convergence/02_iot_mobility/118_mqtt_protocol/)
**다음**: [120. CoAP (Constrained Application Protocol) - IoT 경량 RESTful 프로토콜](/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/) ->

---
