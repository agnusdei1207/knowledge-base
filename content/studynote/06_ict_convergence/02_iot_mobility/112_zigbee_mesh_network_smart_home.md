---
title: 112. Zigbee 메시 네트워크 (Zigbee Mesh Network) - IEEE 802.15.4 스마트 홈 WPAN
date: '2026-04-19'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Zigbee는 IEEE 802.15.4 기반의 **저전력·저속·단거리(~100m) [[604_wpan_wireless_personal_area_network|WPAN]](Wireless Personal Area Network)** [[295_protocol_field_tcp_udp_icmp|프로토콜]]로, **[[389_mesh_topology|메시]]([[389_mesh_topology|Mesh]]) 토폴로지**를 통해 수백 개 센서 노드가 자가 치유(Self-healing) 네트워크를 형성하는 스마트 홈·빌딩 자동화의 핵심 기술이다.
> 2. **가치**: [[607_ble_bluetooth_low_energy_iot|BLE]]([[607_ble_bluetooth_low_energy_iot|Bluetooth Low Energy]])가 1:1 Point-to-Point에 강하다면, Zigbee는 **[[100_many_to_many_model|다대다]]([[100_many_to_many_model|Many-to-Many]]) [[389_mesh_topology|메시]] [[339_routing_overview_best_path_selection|라우팅]]**에 강하여 조명 100개·센서 200개를 하나의 네트워크로 제어할 수 있다.
> 3. **판단 포인트**: [[609_zigbee_ieee_802_15_4_mesh_iot|Zigbee]] 3.0이 프로파일 통합(HA/LL/SE)으로 호환성을 확보했으나, **[[612_matter_csa_smart_home_standard|Matter]](구 CHIP) [[295_protocol_field_tcp_udp_icmp|프로토콜]]이 [[609_zigbee_ieee_802_15_4_mesh_iot|Zigbee]]·[[092_thread_lwp|Thread]]·Wi-Fi·BLE를 통합하는 차세대 표준**으로 부상하여 Zigbee의 독자적 위치가 흔들리고 있다.

---

## Ⅰ. 개요 및 필요성

스마트 홈에서 조명·에어컨·도어록·센서를 제어하려면 **저전력으로 수백 개 디바이스가 안정적으로 통신**해야 한다. Wi-Fi는 [[466_power_consumption|전력 소모]]가 크고, BLE는 [[389_mesh_topology|메시]] 지원이 제한적이다.

```text
┌───────────────────────────────────────────────────────┐
│      Zigbee 메시 토폴로지 구조                         │
├───────────────────────────────────────────────────────┤
│        [Coordinator]                                  │
│         /    |    \                                    │
│   [Router] [Router] [Router]                          │
│    / \       |       / \                               │
│  [ED] [ED] [ED]  [ED] [ED]   (ED = End Device)       │
│                                                       │
│  Coordinator: 네트워크 생성·관리 (1개)                │
│  Router: 중계·라우팅 (상시 전원, 메시 구성)           │
│  End Device: 센서/스위치 (배터리, Sleep 모드)          │
│                                                       │
│  Self-healing: Router 1개 고장 → 자동 우회 경로 탐색  │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[609_zigbee_ieee_802_15_4_mesh_iot|Zigbee]] [[389_mesh_topology|메시]]는 마을 소문 전파 시스템이다. 이장([[250_coordinator_participant_2pc_roles|Coordinator]])이 소식을 내리면, 반장(Router)들이 릴레이로 전달하고, 주민(End Device)이 수신한다. 반장 1명이 아파도 다른 반장이 대신 전달한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 항목 | [[609_zigbee_ieee_802_15_4_mesh_iot|Zigbee]] | [[607_ble_bluetooth_low_energy_iot|BLE]] | Wi-Fi |
|:---|:---|:---|:---|
| **표준** | IEEE 802.15.4 | IEEE 802.15.1 | IEEE 802.[[308_static_dynamic_nat_pat_port_address_translation|11]] |
| **속도** | 250 kbps | 2 Mbps | ~Gbps |
| **거리** | ~100m ([[389_mesh_topology|메시]]로 확장) | ~50m | ~100m |
| **전력** | 매우 낮음 | 낮음 | 높음 |
| **토폴로지** | **Star/Tree/[[389_mesh_topology|Mesh]]** | Star ([[389_mesh_topology|Mesh]] 제한적) | Star |
| **노드 수** | **최대 65,000** | ~7 (Classic) | ~250 |
| **주요 용도** | 스마트 홈, 빌딩 자동화 | 웨어러블, 오디오 | 인터넷 |

- **📢 섹션 요약 비유**: Zigbee는 마을 전체를 커버하는 무전기 네트워크이고, BLE는 1:1 귓속말이며, Wi-Fi는 고속도로(빠르지만 [[466_power_consumption|전력 소모]] 큼)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[609_zigbee_ieee_802_15_4_mesh_iot|Zigbee]] | [[610_z_wave_900mhz_smart_home_iot|Z-Wave]] | [[092_thread_lwp|Thread]] | [[612_matter_csa_smart_home_standard|Matter]] |
|:---|:---|:---|:---|:---|
| **주파수** | 2.4GHz (ISM) | 900MHz | 2.4GHz | 다중 (Wi-Fi/[[092_thread_lwp|Thread]]) |
| **[[389_mesh_topology|메시]]** | ✅ | ✅ | ✅ (IP 기반) | ✅ |
| **IP 지원** | ✗ (게이트웨이 필요) | ✗ | **✅ ([[324_ipv6_128bit_next_generation_address|IPv6]])** | **✅** |
| **미래** | Matter에 흡수 중 | 축소 | [[612_matter_csa_smart_home_standard|Matter]] 하위 | **차세대 통합 표준** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적합 시나리오
1. **스마트 조명**: Philips Hue ([[609_zigbee_ieee_802_15_4_mesh_iot|Zigbee]] 기반), 조명 50개 [[389_mesh_topology|메시]] 제어.
2. **빌딩 자동화**: 온도·습도·CO2 센서 수백 개 배치.

### [[612_matter_csa_smart_home_standard|Matter]] 전환 [[268_strategy_pattern|전략]]
- 신규 프로젝트: **[[612_matter_csa_smart_home_standard|Matter]]([[092_thread_lwp|Thread]] 기반)** 권장.
- 기존 [[609_zigbee_ieee_802_15_4_mesh_iot|Zigbee]] 인프라: [[609_zigbee_ieee_802_15_4_mesh_iot|Zigbee]] 3.0 유지, [[612_matter_csa_smart_home_standard|Matter]] Bridge로 통합.

---

## Ⅴ. 기대효과 및 결론

Zigbee는 스마트 홈 WPAN의 선구자이지만, **[[612_matter_csa_smart_home_standard|Matter]] [[295_protocol_field_tcp_udp_icmp|프로토콜]](Apple·Google·Amazon 공동 표준)**이 [[609_zigbee_ieee_802_15_4_mesh_iot|Zigbee]]·[[092_thread_lwp|Thread]]·Wi-Fi를 통합하며 차세대 스마트 홈 표준으로 부상하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **IEEE 802.15.4** | [[609_zigbee_ieee_802_15_4_mesh_iot|Zigbee]]·Thread의 PHY/[[673_mac_message_authentication_code|MAC]] 계층 표준 |
| **[[389_mesh_topology|메시]] 네트워크** | Zigbee의 핵심 토폴로지, Self-healing |
| **[[607_ble_bluetooth_low_energy_iot|BLE]] ([[607_ble_bluetooth_low_energy_iot|Bluetooth Low Energy]])** | 1:1 통신 경쟁 기술 |
| **[[092_thread_lwp|Thread]]** | [[324_ipv6_128bit_next_generation_address|IPv6]] 기반 [[389_mesh_topology|메시]], Matter의 하위 [[295_protocol_field_tcp_udp_icmp|프로토콜]] |
| **[[612_matter_csa_smart_home_standard|Matter]]** | [[609_zigbee_ieee_802_15_4_mesh_iot|Zigbee]]·[[092_thread_lwp|Thread]]·Wi-Fi 통합 차세대 스마트 홈 표준 |

### 📈 관련 키워드 및 발전 흐름도

```text
[IEEE 802.15.4 (2003) — 저전력 WPAN 표준]
    │
    ▼
[Zigbee 1.0 (2004) — 스마트 홈 메시 네트워크]
    │
    ▼
[Zigbee 3.0 (2016) — 프로파일 통합 (HA/LL/SE)]
    │
    ▼
[Thread (2015~) — IPv6 메시, Google Nest 채택]
    │
    ▼
[Matter (2022~) — Apple·Google·Amazon 통합 표준]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Zigbee는 마을 전체에 **무전기 네트워크**를 깐 거예요. 반장들이 릴레이로 소식을 전달해요.
2. 반장 1명이 아파도 **다른 반장이 대신** 전달하니까 소식이 끊기지 않아요 ([[389_mesh_topology|메시]] 자가 치유).
3. 지금은 **Matter라는 새로운 규칙**이 나와서 모든 무전기가 하나의 언어로 통일되고 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 112 / 552

← **이전**: [[111_licensed_lpwan_nb_iot_lte_m|111. 면허 대역 LPWAN - NB-IoT vs LTE-M 3GPP 표준 IoT 통신]]
**다음**: [[113_z_wave_smart_home_900mhz|113. Z-Wave 스마트 홈 (Z-Wave Smart Home) - 900MHz 서브 GHz 저간섭 WPAN]] →

---
