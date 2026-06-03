---
title: 123. OCF (Open Connectivity Foundation) - IoT 상호운용성 표준
date: '2026-04-19'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: OCF는 **이기종 [[101_iot_concept|IoT]] 디바이스 간 [[287_interoperability_tactics|상호운용성]]([[084_blockchain_interoperability_polkadot_cosmos|Interoperability]])을 보장**하는 개방형 표준으로, 제조사·[[295_protocol_field_tcp_udp_icmp|프로토콜]]에 관계없이 디바이스가 **자동 발견(Discovery)·통신·보안 연결**될 수 있도록 한다.
> 2. **가치**: [[101_iot_concept|IoT]] 디바이스가 제조사마다 독자 [[295_protocol_field_tcp_udp_icmp|프로토콜]]을 사용하면 "삼성 냉장고↔LG 에어컨" 연동이 불가능하지만, OCF 표준을 따르면 **브랜드 무관하게 자동 연동**된다.
> 3. **판단 포인트**: OCF는 **IoTivity([[191_oss_license_compliance|오픈소스]] 구현체)**를 제공하며, [[612_matter_csa_smart_home_standard|Matter]](2022)와 함께 **스마트 홈 [[287_interoperability_tactics|상호운용성]] 표준 생태계**를 형성한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    OCF 프레임워크                                     │
├───────────────────────────────────────────────────────┤
│  [응용 계층] — 스마트홈·헬스케어·산업 IoT 앱         │
│  [OCF 서비스 계층]                                    │
│   디바이스 발견·리소스 관리·보안·데이터 모델          │
│  [전송 계층] — CoAP / HTTP / WebSocket               │
│  [네트워크] — Wi-Fi / BLE / Thread / Zigbee          │
│                                                       │
│  핵심: 이기종 디바이스 자동 발견 + 표준 데이터 모델   │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: OCF는 IoT의 **[[359_usb|USB]] 표준**이다. [[359_usb|USB]] 이전에는 프린터마다 다른 케이블이 필요했지만, USB로 통일되면서 아무 프린터나 연결할 수 있게 되었다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### OCF vs [[612_matter_csa_smart_home_standard|Matter]]

| 비교 | OCF | [[612_matter_csa_smart_home_standard|Matter]] |
|:---|:---|:---|
| **범위** | 범용 [[101_iot_concept|IoT]] | **스마트 홈 특화** |
| **전송** | [[120_coap_constrained_application_protocol|CoAP]]/[[461_http_stateless_connection_oriented|HTTP]] | [[092_thread_lwp|Thread]]/Wi-Fi |
| **구현체** | IoTivity | connectedhomeip |
| **지원** | 삼성·Intel | **Apple·Google·Amazon** |

- **📢 섹션 요약 비유**: OCF는 범용 전원 [[259_adapter_pattern_interface_wrapper|어댑터]], Matter는 스마트홈 전용 [[259_adapter_pattern_interface_wrapper|어댑터]]이다.

---

## Ⅲ. 비교 및 연결

| 비교 | OCF | oneM2M | [[612_matter_csa_smart_home_standard|Matter]] |
|:---|:---|:---|:---|
| **초점** | 디바이스 연동 | **플랫폼** | 스마트 홈 |
| **계층** | 디바이스 | [[090_service_kubernetes_network_load_balancing|서비스]] | 디바이스 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### IoTivity
- Linux Foundation [[191_oss_license_compliance|오픈소스]] 프로젝트.
- OCF 스펙의 [[316_reference_pattern_nosql|참조]] 구현체.
- C/C++ 기반, 경량 디바이스 지원.

---

## Ⅴ. 기대효과 및 결론

OCF는 **이기종 [[101_iot_concept|IoT]] [[287_interoperability_tactics|상호운용성]]의 기술 표준**이며, Matter와 함께 스마트 홈·산업 IoT의 표준 생태계를 형성하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **IoTivity** | OCF의 [[191_oss_license_compliance|오픈소스]] 구현체 |
| **[[612_matter_csa_smart_home_standard|Matter]]** | 스마트 홈 [[287_interoperability_tactics|상호운용성]] 표준 |
| **[[120_coap_constrained_application_protocol|CoAP]]** | OCF의 기본 전송 [[295_protocol_field_tcp_udp_icmp|프로토콜]] |
| **oneM2M** | [[101_iot_concept|IoT]] [[090_service_kubernetes_network_load_balancing|서비스]] 플랫폼 표준 |
| **[[092_thread_lwp|Thread]]** | 저전력 [[389_mesh_topology|메시]] 네트워크 ([[612_matter_csa_smart_home_standard|Matter]] 전송) |

### 📈 관련 키워드 및 발전 흐름도

```text
[독자 IoT 프로토콜 (사일로, 2010s)]
    │
    ▼
[OIC → OCF (2014~2016) — 상호운용성 표준]
    │
    ▼
[IoTivity 오픈소스 (2015~)]
    │
    ▼
[Matter (2022) — 스마트 홈 통합 표준]
    │
    ▼
[현재: OCF + Matter + Thread — IoT 표준 생태계]
```

### 👶 어린이를 위한 3줄 비유 설명
1. OCF는 IoT의 **[[359_usb|USB]] 표준**이에요. 어떤 회사 제품이든 **같은 규격으로 연결**돼요.
2. [[359_usb|USB]] 이전에는 프린터마다 **다른 케이블**이 필요했지만, USB로 통일되면서 편리해졌어요.
3. 삼성 냉장고와 LG 에어컨도 OCF를 따르면 **서로 대화**할 수 있답니다!