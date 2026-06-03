---
title: 117. 6LoWPAN (IPv6 over Low-Power WPAN) - IoT IPv6 압축·적응 계층
date: '2026-04-19'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 6LoWPAN은 IEEE 802.15.4의 **127바이트 MTU 제약** 위에서 [[324_ipv6_128bit_next_generation_address|IPv6]](최소 1280바이트 MTU)를 동작시키기 위해 **헤더 [[347_compaction|압축]]·[[291_fragmentation_and_reassembly_process|단편화]]·[[389_mesh_topology|메시]] [[339_routing_overview_best_path_selection|라우팅]]**을 수행하는 적응 계층이다.
> 2. **가치**: [[101_iot_concept|IoT]] 디바이스에 [[324_ipv6_128bit_next_generation_address|IPv6]] 주소를 부여하면 인터넷과 직접 통신이 가능하지만, 802.15.4의 작은 프레임에 [[324_ipv6_128bit_next_generation_address|IPv6]] 헤더(40바이트)를 넣으면 페이로드가 거의 없다. 6LoWPAN은 헤더를 **2~7바이트로 [[347_compaction|압축]]**하여 이 문제를 해결한다.
> 3. **판단 포인트**: [[092_thread_lwp|Thread]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]이 **6LoWPAN을 적응 계층으로 사용**하며, Matter의 저전력 전송 인프라의 핵심 기술이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    6LoWPAN 헤더 압축                                  │
├───────────────────────────────────────────────────────┤
│  [IPv6 헤더: 40바이트]                                │
│   + UDP 헤더: 8바이트 = 48바이트                      │
│   802.15.4 MTU: 127바이트                             │
│   → 페이로드: 127 - 48 - MAC헤더 ≈ 50바이트뿐!      │
│                                                       │
│  [6LoWPAN 압축 후]                                    │
│   IPv6+UDP 헤더: 2~7바이트로 압축                     │
│   → 페이로드: 100바이트 이상 확보!                    │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[324_ipv6_128bit_next_generation_address|IPv6]] 편지(40바이트 봉투)를 작은 엽서(127바이트 MTU)에 넣으려면 봉투를 접어야 한다. 6LoWPAN이 그 "접기 기술"이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 6LoWPAN 핵심 기능

| 기능 | 설명 |
|:---|:---|
| **헤더 [[347_compaction|압축]] (IPHC)** | [[324_ipv6_128bit_next_generation_address|IPv6]] 40B → 2~7B [[347_compaction|압축]] ([[329_ipv6_link_local_fe80_site_local|링크 로컬 주소]] 생략) |
| **[[291_fragmentation_and_reassembly_process|단편화]] ([[291_fragmentation_and_reassembly_process|Fragmentation]])** | 1280B [[324_ipv6_128bit_next_generation_address|IPv6]] 패킷 → 127B 조각으로 분할 |
| **[[389_mesh_topology|메시]] [[339_routing_overview_best_path_selection|라우팅]]** | 802.15.4 L2 [[389_mesh_topology|메시]] 포워딩 |
| **NHC** | Next Header [[159_compression|Compression]] ([[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 8B → 2B) |

- **📢 섹션 요약 비유**: 6LoWPAN은 이사할 때 큰 가구([[324_ipv6_128bit_next_generation_address|IPv6]] 패킷)를 분해([[291_fragmentation_and_reassembly_process|단편화]])하고 포장 줄이기([[347_compaction|압축]])해서 작은 차(802.15.4 프레임)에 실는 기술이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[324_ipv6_128bit_next_generation_address|IPv6]] 직접 | 6LoWPAN | [[092_thread_lwp|Thread]] |
|:---|:---|:---|:---|
| **헤더** | 40B | **2~7B** | 6LoWPAN 사용 |
| **MTU** | 1280B 이상 | 127B 적응 | 127B 적응 |
| **[[389_mesh_topology|메시]]** | ✗ | ✅ | ✅ |
| **용도** | 일반 네트워크 | [[604_wpan_wireless_personal_area_network|WPAN]] 적응 | **스마트 홈 표준** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 6LoWPAN이 사용되는 곳
1. **[[092_thread_lwp|Thread]]**: 6LoWPAN을 적응 계층으로 사용, Matter의 전송 인프라.
2. **산업 [[101_iot_concept|IoT]]**: ISA100.11a, WirelessHART가 6LoWPAN 활용.

---

## Ⅴ. 기대효과 및 결론

6LoWPAN은 "[[101_iot_concept|IoT]] 디바이스에 IPv6를 넣기 위한 필수 적응 기술"이며, [[092_thread_lwp|Thread]]·Matter의 하위 계층으로서 스마트 홈 생태계의 기반 기술이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **IEEE 802.15.4** | 6LoWPAN의 물리/[[673_mac_message_authentication_code|MAC]] 기반 |
| **[[324_ipv6_128bit_next_generation_address|IPv6]]** | 6LoWPAN이 [[347_compaction|압축]]하여 전달하는 네트워크 [[295_protocol_field_tcp_udp_icmp|프로토콜]] |
| **[[092_thread_lwp|Thread]]** | 6LoWPAN을 적응 계층으로 사용 |
| **IPHC** | [[324_ipv6_128bit_next_generation_address|IPv6]] 헤더 [[347_compaction|압축]] [[001_algorithm_definition|알고리즘]] |
| **[[612_matter_csa_smart_home_standard|Matter]]** | [[092_thread_lwp|Thread]] + 6LoWPAN 위에서 동작하는 앱 표준 |

### 📈 관련 키워드 및 발전 흐름도

```text
[IEEE 802.15.4 (2003) — 저전력 WPAN PHY/MAC]
    │
    ▼
[6LoWPAN RFC 4944 (2007) — IPv6 over 802.15.4 표준]
    │
    ▼
[IPHC RFC 6282 (2011) — 헤더 압축 개선]
    │
    ▼
[Thread 1.0 (2015) — 6LoWPAN + IPv6 메시 네트워크]
    │
    ▼
[현재: Matter + Thread — 6LoWPAN 기반 스마트 홈 인프라]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[324_ipv6_128bit_next_generation_address|IPv6]] 편지는 **봉투(40바이트)가 너무 커서** 작은 엽서(127바이트)에 안 들어가요.
2. 6LoWPAN은 봉투를 **작게 접어서([[347_compaction|압축]])** 엽서에 넣을 수 있게 해주는 기술이에요.
3. 이 기술 덕분에 아주 작은 센서도 **인터넷([[324_ipv6_128bit_next_generation_address|IPv6]]) 주소를 가지고** 세상과 대화할 수 있답니다!