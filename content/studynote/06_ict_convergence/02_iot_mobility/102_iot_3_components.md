---
title: IoT 3대 구성 요소
date: '2024-03-21'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[101_iot_concept|사물인터넷]]([[101_iot_concept|IoT]]; Internet of Things) 시스템은 현실의 [[001_dikw_pyramid|데이터]]를 수집하는 **디바이스(Device)**, [[001_dikw_pyramid|데이터]]를 전달하는 **네트워크(Network)**, [[001_dikw_pyramid|데이터]]를 분석해 가치를 창출하는 **플랫폼(Platform)**의 3대 구성 요소로 이루어진다.
> 2. **가치**: 이 3요소가 유기적으로 결합되어 센싱된 원시 [[001_dikw_pyramid|데이터]]([[225_raw|Raw]] [[001_dikw_pyramid|Data]])를 의미 있는 지능화된 정보(Intelligence)로 변환하는 'Sense-Connect-Think' 파이프라인을 완성한다.
> 3. **판단 포인트**: [[101_iot_concept|IoT]] 아키텍처 설계의 성패는 단순히 고성능 기기를 사는 것이 아니라, [[001_dikw_pyramid|데이터]] 폭증으로 인한 네트워크 [[140_bandwidth|대역폭]] 부족이나 배터리 소모 같은 '병목 현상([[617_io_bottleneck|Bottleneck]])'을 각 계층 간의 조율로 어떻게 해결하느냐에 달려 있다.

---

## Ⅰ. 개요 및 필요성

[[101_iot_concept|사물인터넷]]([[101_iot_concept|IoT]]) 3대 구성 요소는 사람의 개입 없이 사물 간 통신을 이끌어내기 위한 종단간([[401_transport_layer_role_end_to_end_multiplexing|End-to-End]]) 아키텍처의 필수 인프라 집합이다. 온갖 종류의 센서와 기기들이 쏟아져 나오는 파편화된 기술 환경에서, 시스템을 체계적으로 설계하고 관리하기 위한 표준화된 골격으로 이 3요소가 정의되었다.

이러한 명확한 계층 분리가 없으면, 각 제조사가 자신만의 통신 방식과 앱을 강제하여 기기 간 [[287_interoperability_tactics|상호운용성]]([[084_blockchain_interoperability_polkadot_cosmos|Interoperability]])이 붕괴된다. 디바이스가 수집한 물리적 정보가 끊김 없이 네트워크를 타고 올라가 플랫폼에서 분석되기 위해서는, 각 요소가 명확한 역할과 표준 [[295_protocol_field_tcp_udp_icmp|프로토콜]]을 가져야만 한다.

- **📢 섹션 요약 비유**: [[101_iot_concept|IoT]] 3대 요소는 인간의 몸과 같다. 감각을 느끼는 눈과 귀(디바이스), 그 신호를 뇌로 전달하는 신경망(네트워크), 그리고 정보를 종합해 판단하는 뇌(플랫폼)가 있어야 하나의 사람이 움직인다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IoT의 핵심 원리는 [[001_dikw_pyramid|데이터]]를 획득(Sense)하고, 전달(Connect)하며, 처리(Think)하는 선형적인 [[645_data_pipeline_acceleration|데이터 파이프라인]] 구조다. 각 구성 요소는 물리적 세계의 신호를 사이버 세계의 서비스로 변환하는 각 단계의 부담을 나눠 가진다.

```text
┌──────────────────────────────────────────────────────────────┐
│          IoT 3-Component Core Architecture: 데이터 흐름       │
├──────────────────────────────────────────────────────────────┤
│ [Physical World]       [Communication]        [Cyber World]  │
│                                                              │
│  ( Component 1 )        ( Component 2 )       ( Component 3 )│
│  [   Device    ]        [   Network   ]       [  Platform   ]│
│  +-------------+        +-------------+       +-------------+│
│  │ · Sensing   │───────▶│ · Routing   │──────▶│ · Analytics ││
│  │ · Actuating │◀───────│ · Gateway   │◀──────│ · AI/Control││
│  +-------------+        +-------------+       +-------------+│
│   센서/MCU/RTOS         5G/LPWAN/MQTT         AWS/Azure/AI   │
└──────────────────────────────────────────────────────────────┘
```

- **디바이스 (Device)**: 스마트 센서와 액추에이터(Actuator)로 구성되며 임베디드 OS가 탑재된다. 주변 환경 [[001_dikw_pyramid|데이터]]를 읽어 들이고 플랫폼의 명령을 물리적 동작으로 수행한다.
- **네트워크 (Network)**: Wi-Fi, 5G부터 저전력 장거리 통신망인 [[109_lpwan_low_power_wide_area_network|LPWAN]] (Low [[069_type_1_2_error_statistical_power|Power]] Wide Area Network)까지, [[001_dikw_pyramid|데이터]]를 빠르고 손실 없이 목적지로 라우팅한다.
- **플랫폼 (Platform/[[090_service_kubernetes_network_load_balancing|Service]])**: 수집된 빅데이터를 저장하고, [[241_machine_learning_basics|머신러닝]]/AI를 통해 분석결과를 시각화하며, 외부 시스템과 연동하는 API를 제공한다.

- **📢 섹션 요약 비유**: 편지 배달 시스템이다. 현장에서 편지를 쓰는 발신자(디바이스)가 우체국 배달망(네트워크)을 통해 편지를 보내면, 본부의 분석팀(플랫폼)이 내용을 읽고 지시사항을 다시 내려보낸다.

---

## Ⅲ. 비교 및 연결

각 구성 요소는 서로 다른 기술적 트레이드오프와 발전 방향을 갖는다. 최근에는 각 계층의 경계가 흐려지는 '[[235_edge_computing_smart_factory|엣지 컴퓨팅]]([[235_edge_computing_smart_factory|Edge Computing]])' 트렌드가 나타나고 있다.

| 구성 요소 | 핵심 제약 및 트레이드오프 | 최신 융합 및 발전 방향 |
| :--- | :--- | :--- |
| **디바이스 (Device)** | [[466_power_consumption|전력 소모]](배터리) vs 연산 능력 | 저전력 온디바이스 [[190_ai_llm_requirements_specification|AI]], TinyML 도입으로 엣지 단에서 1차 판단 수행 |
| **네트워크 (Network)** | 전송 속도 vs 도달 거리 vs 비용 | [[419_6g_ntn_thz_ris_next_gen|6G]] 및 [[592_satellite_communication_characteristics|위성 통신]](NTN; Non-Terrestrial Network) 융합으로 음영지역 해소 |
| **플랫폼 (Platform)** | 엄청난 트래픽 처리 vs 실시간 분석 | [[126_digital_twin_concept|디지털 트윈]]([[126_digital_twin_concept|Digital Twin]]) 및 [[531_cloud_native_architecture|클라우드 네이티브]] 기반 자율 운영 |

이러한 발전은 플랫폼에 집중되던 부하를 디바이스와 네트워크 엣지로 분산시킴으로써 지연시간을 줄이고 통신 비용을 최적화하는 융합을 만들어낸다.

- **📢 섹션 요약 비유**: 과거에는 뇌(플랫폼)가 모든 것을 다 판단해서 피곤했지만, 이제는 반사 신경(디바이스 [[190_ai_llm_requirements_specification|AI]])과 자율신경계(스마트 네트워크)가 알아서 척척 기초 판단을 해주고 뇌는 큰 그림만 그린다.

---

## Ⅳ. 실무 적용 및 기술사 판단

기술사는 [[101_iot_concept|IoT]] 시스템을 설계할 때 단순 하드웨어 조립이 아닌 **병목([[617_io_bottleneck|Bottleneck]]) 해결과 보안 내재화**에 집중해야 한다. 

예를 들어, 산불 감지 센서 수만 개를 설치할 때 모든 [[001_dikw_pyramid|데이터]]를 5G망으로 플랫폼에 실시간 전송하도록 설계하면 통신비 폭탄과 배터리 방전으로 프로젝트는 실패한다. 이 경우, 산불 징후가 있을 때만 신호를 보내는 **온디바이스 엣지 처리**와 배터리로 수년간 버티는 **[[617_lora_lorawan_css_chirp_spread_spectrum|LoRa]] 등 [[109_lpwan_low_power_wide_area_network|LPWAN]] 네트워크**를 결합하는 의사결정을 내려야 한다. 

또한, 보안([[283_security_tactics|Security]])은 3대 구성 요소 특정 한 곳에만 적용하는 것이 아니라, 디바이스 [[303_authentication_authorization_patterns|인증]]([[694_thread_local_storage_tls|TLS]]), 네트워크 암호화, 플랫폼 접근통제 등 전체 계층에 수평적으로 적용하는 종단간 보안 아키텍처를 수립해야 한다.

- **📢 섹션 요약 비유**: 공장을 짓는데 모든 컨베이어 벨트를 무조건 제일 빠른 모터로 달면 전기세만 날아간다. 무거운 짐이 지나는 곳과 가벼운 짐이 지나는 곳을 분석해 최적의 모터를 골라 배치하는 것이 설계자의 몫이다.

---

## Ⅴ. 기대효과 및 결론

[[101_iot_concept|IoT]] 3대 구성 요소를 최적화하여 구축하면 인프라의 가시성을 100% 확보할 수 있고 유지보수의 자동화로 운영 비용(OPEX)을 획기적으로 절감할 수 있다. 한계점으로는 구성 요소 간 통신이 늘어날수록 공격 표면(Attack Surface)이 넓어지므로 철저한 보안 패치가 전제되어야 한다는 것이다.

미래의 IoT는 세 가지 요소가 클라우드 환경에서 완전히 하나로 통합된 '서비스형 자산(Asset-as-a-[[090_service_kubernetes_network_load_balancing|Service]])' 형태로 진화할 것이다. 결국 [[101_iot_concept|IoT]] 3대 구성 요소는 단순히 물리적 사물을 묶는 기술이 아니라, 모든 비즈니스 도메인을 [[001_dikw_pyramid|데이터]] 기반의 지능형 서비스로 탈바꿈시키는 핵심 인프라 토대임을 명심해야 한다.

- **📢 섹션 요약 비유**: 3개의 톱니바퀴가 완벽하게 맞물려 돌아가는 시계 무브먼트와 같다. 하나라도 크기가 맞지 않거나 녹이 슬면 시계 전체가 멈추므로 전체적인 밸런스가 가장 중요하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **[[622_mqtt_publish_subscribe_qos|MQTT]] / [[120_coap_constrained_application_protocol|CoAP]]** | 디바이스와 네트워크 레이어 간에 [[001_dikw_pyramid|데이터]]를 주고받는 초경량 메시징 [[295_protocol_field_tcp_udp_icmp|프로토콜]] |
| **[[235_edge_computing_smart_factory|엣지 컴퓨팅]] ([[235_edge_computing_smart_factory|Edge Computing]])** | 플랫폼의 과부하를 막기 위해 네트워크 단말이나 디바이스 가까이서 [[001_dikw_pyramid|데이터]]를 처리하는 기술 |
| **[[109_lpwan_low_power_wide_area_network|LPWAN]] (Low [[069_type_1_2_error_statistical_power|Power]] Wide Area Network)** | 저전력, 장거리 통신을 지원하여 [[101_iot_concept|IoT]] 디바이스에 최적화된 네트워크 통신망 |
| **[[126_digital_twin_concept|디지털 트윈]] ([[126_digital_twin_concept|Digital Twin]])** | 플랫폼 상에 물리적 디바이스를 똑같이 복제하여 시뮬레이션하고 최적화하는 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
단순 사물 통신 (M2M)
    │
    ▼
IoT 3대 구성 요소 확립 (Device - Network - Platform)
    │
    ▼
경량화 프로토콜 (MQTT) 및 저전력 통신망 (LPWAN) 적용
    │
    ▼
엣지 컴퓨팅 (Edge Computing) 확산 및 트래픽 분산
    │
    ▼
지능형 사물인터넷 (AIoT) 및 디지털 트윈 (Digital Twin) 융합
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[101_iot_concept|사물인터넷]] 세상은 우리 몸이 일하는 방식과 아주 똑같아요.
2. 눈과 귀가 되어 온도와 소리를 느끼는 부분은 **디바이스**라고 불러요.
3. 그 정보를 신경을 타고 슝 전달하는 건 **네트워크**고, 정보를 모아 "앗 뜨거워!"라고 생각하는 똑똑한 머리가 **플랫폼**이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 102 / 552

← **이전**: [[101_iot_concept|사물인터넷 (IoT) 개념]]
**다음**: [[103_wsn_sensor_network|센서 네트워크 (WSN)]] →

---
