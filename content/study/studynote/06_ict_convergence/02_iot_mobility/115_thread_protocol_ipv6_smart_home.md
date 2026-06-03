---
title: 115. Thread 프로토콜 (Thread Protocol) - IPv6 기반 저전력 메시·Matter 핵심 전송 계층
date: '2026-04-19'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Thread는 IEEE 802.15.4 PHY/[[673_mac_message_authentication_code|MAC]] 위에 **[[324_ipv6_128bit_next_generation_address|IPv6]] + [[117_6lowpan_iot_ipv6|6LoWPAN]]**을 구현한 저전력 [[389_mesh_topology|메시]] 네트워크 [[295_protocol_field_tcp_udp_icmp|프로토콜]]로, 각 디바이스가 **IP 주소를 가져 인터넷과 [[120_direct_communication|직접 통신]]** 가능하다.
> 2. **가치**: [[609_zigbee_ieee_802_15_4_mesh_iot|Zigbee]]·Z-Wave가 게이트웨이를 통해야 인터넷에 접속하는 반면, [[092_thread_lwp|Thread]] 디바이스는 **Border Router만으로 [[324_ipv6_128bit_next_generation_address|IPv6]] 인터넷에 네이티브 연결**되어 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 변환 없이 클라우드와 [[120_direct_communication|직접 통신]]한다.
> 3. **판단 포인트**: **[[612_matter_csa_smart_home_standard|Matter]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]의 핵심 전송 계층**으로 채택되어 Apple·Google·Amazon이 Thread를 지원하며, Self-healing [[389_mesh_topology|메시]]·~250개 디바이스·수 ms 전환으로 스마트 홈의 차세대 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Zigbee vs Thread: IP 연결성 차이                    │
├───────────────────────────────────────────────────────┤
│  [Zigbee]                                             │
│   센서 ──Zigbee──▶ 게이트웨이 ──프로토콜 변환──▶ IP   │
│   디바이스에 IP 주소 없음                             │
│                                                       │
│  [Thread]                                             │
│   센서 ──Thread(IPv6)──▶ Border Router ──▶ IP         │
│   디바이스에 IPv6 주소 있음 → 직접 통신!              │
│   프로토콜 변환 불필요                                │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Zigbee는 통역사(게이트웨이)가 필요한 외국어이고, Thread는 세계 공용어([[324_ipv6_128bit_next_generation_address|IPv6]])를 쓰는 디바이스라 통역 없이 바로 대화 가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[092_thread_lwp|Thread]] 네트워크 역할

| 역할 | 기능 |
|:---|:---|
| **Border Router** | [[092_thread_lwp|Thread]] ↔ Wi-Fi/[[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 연결, [[324_ipv6_128bit_next_generation_address|IPv6]] [[339_routing_overview_best_path_selection|라우팅]] |
| **Leader** | 네트워크 [[089_configuration_management|구성 관리]] (자동 선출) |
| **Router** | [[389_mesh_topology|메시]] [[339_routing_overview_best_path_selection|라우팅]], 상시 전원 |
| **End Device (Sleepy)** | 배터리 센서, Sleep→Wake 간헐 전송 |

### [[092_thread_lwp|Thread]] vs [[609_zigbee_ieee_802_15_4_mesh_iot|Zigbee]] vs [[610_z_wave_900mhz_smart_home_iot|Z-Wave]]

| 항목 | [[092_thread_lwp|Thread]] | [[609_zigbee_ieee_802_15_4_mesh_iot|Zigbee]] | [[610_z_wave_900mhz_smart_home_iot|Z-Wave]] |
|:---|:---|:---|:---|
| **IP 지원** | **[[324_ipv6_128bit_next_generation_address|IPv6]] 네이티브** | ✗ | ✗ |
| **PHY** | IEEE 802.15.4 | IEEE 802.15.4 | 독자 (900MHz) |
| **[[389_mesh_topology|메시]]** | ✅ Self-healing | ✅ | ✅ (4홉) |
| **[[612_matter_csa_smart_home_standard|Matter]] 호환** | **핵심 전송 계층** | [[260_bridge_pattern_abstraction_implementation|Bridge]] | [[260_bridge_pattern_abstraction_implementation|Bridge]] |

- **📢 섹션 요약 비유**: Thread는 [[612_matter_csa_smart_home_standard|Matter]] 건물의 수도·전기 배관(전송 인프라)이고, Matter는 건물 설계도(앱 계층 표준)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[092_thread_lwp|Thread]] | Wi-Fi | [[607_ble_bluetooth_low_energy_iot|BLE]] |
|:---|:---|:---|:---|
| **전력** | 매우 낮음 | 높음 | 매우 낮음 |
| **[[389_mesh_topology|메시]]** | ✅ | ✗ | 제한적 |
| **IP** | **[[324_ipv6_128bit_next_generation_address|IPv6]]** | [[286_ipv4_internet_protocol_version_4_rfc_791|IPv4]]/6 | ✗ |
| **[[612_matter_csa_smart_home_standard|Matter]] 역할** | **전송 계층** | 전송 계층 | 커미셔닝만 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[612_matter_csa_smart_home_standard|Matter]] + [[092_thread_lwp|Thread]] 시나리오
- Google Nest [[152_hub_dummy_switching_intelligent|Hub]] → [[092_thread_lwp|Thread]] Border Router 역할 → [[092_thread_lwp|Thread]] 센서·조명 직접 제어.
- Apple HomePod → [[092_thread_lwp|Thread]] Border Router 내장 → [[612_matter_csa_smart_home_standard|Matter]] 디바이스 [[324_ipv6_128bit_next_generation_address|IPv6]] 연결.

---

## Ⅴ. 기대효과 및 결론

Thread는 **[[324_ipv6_128bit_next_generation_address|IPv6]] 네이티브 + 저전력 [[389_mesh_topology|메시]]**라는 두 마리 토끼를 잡았으며, Matter의 핵심 전송 계층으로 채택되어 스마트 홈 인프라의 사실상 표준으로 자리잡고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **IEEE 802.15.4** | Thread의 PHY/[[673_mac_message_authentication_code|MAC]] 계층 |
| **[[117_6lowpan_iot_ipv6|6LoWPAN]]** | IPv6를 802.15.4에 적응시키는 [[347_compaction|압축]] 기술 |
| **[[612_matter_csa_smart_home_standard|Matter]]** | Thread를 전송 계층으로 사용하는 앱 표준 |
| **Border Router** | [[092_thread_lwp|Thread]] ↔ IP 네트워크 연결 장치 |
| **[[609_zigbee_ieee_802_15_4_mesh_iot|Zigbee]]** | 같은 PHY를 쓰는 경쟁 [[295_protocol_field_tcp_udp_icmp|프로토콜]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[IEEE 802.15.4 (2003) — 저전력 WPAN PHY/MAC]
    │
    ▼
[Thread 1.0 (2015, Google Nest) — IPv6 메시]
    │
    ▼
[Thread 1.2 (2019) — 상용 Border Router 확산]
    │
    ▼
[Matter + Thread (2022~) — Apple·Google·Amazon 채택]
    │
    ▼
[현재: Thread 1.3 — 대규모 상용 배포, Matter 핵심 인프라]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Zigbee는 외국어를 쓰는 친구라서 **통역사(게이트웨이)**가 필요해요.
2. Thread는 **세계 공용어([[324_ipv6_128bit_next_generation_address|IPv6]])**를 쓰니까 통역 없이 바로 인터넷에 연결돼요!
3. 지금은 Apple·Google·Amazon이 모두 Thread를 지원해서 **스마트 홈의 공통 언어**가 되고 있답니다!
