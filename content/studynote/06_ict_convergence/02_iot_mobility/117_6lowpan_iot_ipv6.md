---
title: "117. 6Lowpan Iot Ipv6"
date: "2026-04-19"
tags:
  - "studynote-ict-convergence"
weight: 117
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 6LoWPAN은 IEEE 802.15.4의 **127바이트 MTU 제약** 위에서 [IPv6](/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/)(최소 1280바이트 MTU)를 동작시키기 위해 <strong>헤더 <a href="/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a>·<a href="/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/">단편화</a>·<a href="/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/">메시</a> <a href="/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a></strong>을 수행하는 적응 계층이다.
> 2. **가치**: [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 디바이스에 [IPv6](/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/) 주소를 부여하면 인터넷과 직접 통신이 가능하지만, 802.15.4의 작은 프레임에 [IPv6](/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/) 헤더(40바이트)를 넣으면 페이로드가 거의 없다. 6LoWPAN은 헤더를 <strong>2~7바이트로 <a href="/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a></strong>하여 이 문제를 해결한다.
> 3. **판단 포인트**: [Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이 <strong>6LoWPAN을 적응 계층으로 사용</strong>하며, Matter의 저전력 전송 인프라의 핵심 기술이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    6LoWPAN 헤더 압축                                  |
+-------------------------------------------------------+
|  [IPv6 헤더: 40바이트]                                |
|   + UDP 헤더: 8바이트 = 48바이트                      |
|   802.15.4 MTU: 127바이트                             |
|   -> 페이로드: 127 - 48 - MAC헤더 ≈ 50바이트뿐!      |
|                                                       |
|  [6LoWPAN 압축 후]                                    |
|   IPv6+UDP 헤더: 2~7바이트로 압축                     |
|   -> 페이로드: 100바이트 이상 확보!                    |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [IPv6](/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/) 편지(40바이트 봉투)를 작은 엽서(127바이트 MTU)에 넣으려면 봉투를 접어야 한다. 6LoWPAN이 그 "접기 기술"이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 6LoWPAN 핵심 기능

| 기능 | 설명 |
|:---|:---|
| <strong>헤더 <a href="/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a> (IPHC)</strong> | [IPv6](/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/) 40B -> 2~7B [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) ([링크 로컬 주소](/studynote/03_network/06_network_layer_ip/329_ipv6_link_local_fe80_site_local/) 생략) |
| <strong><a href="/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/">단편화</a> (<a href="/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/">Fragmentation</a>)</strong> | 1280B [IPv6](/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/) 패킷 -> 127B 조각으로 분할 |
| <strong><a href="/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/">메시</a> <a href="/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a></strong> | 802.15.4 L2 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/) 포워딩 |
| **NHC** | Next Header [Compression](/studynote/08_algorithm_stats/09_info_theory/159_compression/) ([UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 8B -> 2B) |

- **📢 섹션 요약 비유**: 6LoWPAN은 이사할 때 큰 가구([IPv6](/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/) 패킷)를 분해([단편화](/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/))하고 포장 줄이기([압축](/studynote/02_operating_system/06_memory_management/347_compaction/))해서 작은 차(802.15.4 프레임)에 실는 기술이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [IPv6](/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/) 직접 | 6LoWPAN | [Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) |
|:---|:---|:---|:---|
| **헤더** | 40B | **2~7B** | 6LoWPAN 사용 |
| **MTU** | 1280B 이상 | 127B 적응 | 127B 적응 |
| <strong><a href="/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/">메시</a></strong> | ✗ | ✅ | ✅ |
| **용도** | 일반 네트워크 | [WPAN](/studynote/03_network/12_iot_wpan_edge/604_wpan_wireless_personal_area_network/) 적응 | **스마트 홈 표준** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 6LoWPAN이 사용되는 곳
1. <strong><a href="/studynote/02_operating_system/02_process_thread/092_thread_lwp/">Thread</a></strong>: 6LoWPAN을 적응 계층으로 사용, Matter의 전송 인프라.
2. <strong>산업 <a href="/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a></strong>: ISA100.11a, WirelessHART가 6LoWPAN 활용.

---

## Ⅴ. 기대효과 및 결론

6LoWPAN은 "[IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 디바이스에 IPv6를 넣기 위한 필수 적응 기술"이며, [Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)·Matter의 하위 계층으로서 스마트 홈 생태계의 기반 기술이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **IEEE 802.15.4** | 6LoWPAN의 물리/[MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 기반 |
| <strong><a href="/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/">IPv6</a></strong> | 6LoWPAN이 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)하여 전달하는 네트워크 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
| <strong><a href="/studynote/02_operating_system/02_process_thread/092_thread_lwp/">Thread</a></strong> | 6LoWPAN을 적응 계층으로 사용 |
| **IPHC** | [IPv6](/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/) 헤더 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| <strong><a href="/studynote/03_network/12_iot_wpan_edge/612_matter_csa_smart_home_standard/">Matter</a></strong> | [Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) + 6LoWPAN 위에서 동작하는 앱 표준 |

### 📈 관련 키워드 및 발전 흐름도

```text
[IEEE 802.15.4 (2003) — 저전력 WPAN PHY/MAC]
    |
    v
[6LoWPAN RFC 4944 (2007) — IPv6 over 802.15.4 표준]
    |
    v
[IPHC RFC 6282 (2011) — 헤더 압축 개선]
    |
    v
[Thread 1.0 (2015) — 6LoWPAN + IPv6 메시 네트워크]
    |
    v
[현재: Matter + Thread — 6LoWPAN 기반 스마트 홈 인프라]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [IPv6](/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/) 편지는 **봉투(40바이트)가 너무 커서** 작은 엽서(127바이트)에 안 들어가요.
2. 6LoWPAN은 봉투를 <strong>작게 접어서(<a href="/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a>)</strong> 엽서에 넣을 수 있게 해주는 기술이에요.
3. 이 기술 덕분에 아주 작은 센서도 <strong>인터넷(<a href="/studynote/03_network/06_network_layer_ip/324_ipv6_128bit_next_generation_address/">IPv6</a>) 주소를 가지고</strong> 세상과 대화할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 117 / 552

<- **이전**: [116. Matter 스마트 홈 표준 - Apple·Google·Amazon 통합 IoT 프로토콜](/studynote/06_ict_convergence/02_iot_mobility/116_matter_smart_home_standard/)
**다음**: [118. MQTT 프로토콜 (Message Queuing Telemetry Transport) - IoT 경량 메시징](/studynote/06_ict_convergence/02_iot_mobility/118_mqtt_protocol/) ->

---
