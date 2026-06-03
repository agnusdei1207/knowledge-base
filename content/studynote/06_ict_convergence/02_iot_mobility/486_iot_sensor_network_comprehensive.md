---
title: 486. IoT 센서 네트워크 종합 (IoT Sensor Network Comprehensive)
date: '2026-05-09'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[101_iot_concept|IoT]](Internet of Things) [[103_wsn_sensor_network|센서 네트워크]]는 물리 세계의 [[001_dikw_pyramid|데이터]]를 수집하는 디바이스(Device), [[001_dikw_pyramid|데이터]]를 전달하는 네트워크(Network), [[001_dikw_pyramid|데이터]]를 처리·저장하는 플랫폼(Platform) 3계층이 협력하는 [[136_variance|분산]] 감지 시스템이다.
> 2. **가치**: 배터리·처리능력·메모리가 극도로 제한된 소형 노드가 수년간 자율 동작해야 하므로, 통신 기술 선택([[604_wpan_wireless_personal_area_network|WPAN]] vs [[571_wlan_bss_ess_structure|WLAN]] vs [[109_lpwan_low_power_wide_area_network|LPWAN]])이 곧 시스템 수명과 비용 구조를 결정짓는 핵심 설계 판단이다.
> 3. **판단 포인트**: "전송 거리 vs 배터리 수명 vs [[001_dikw_pyramid|데이터]] [[139_throughput|처리량]]" 트레이드오프를 먼저 정의하고, 그 교점에 맞는 무선 기술을 선택해야 한다. 근거리 고속엔 [[571_wlan_bss_ess_structure|WLAN]], 초원거리 저전력엔 [[109_lpwan_low_power_wide_area_network|LPWAN]], 단거리 [[389_mesh_topology|메시]]엔 WPAN이 답이다.

---

## Ⅰ. 개요 및 필요성

[[103_wsn_sensor_network|WSN]](Wireless Sensor Network)은 다수의 소형 센서 노드가 무선으로 자가 조직화(Self-organizing)하여 환경 정보를 수집하고 싱크 노드(Sink Node)로 전달하는 네트워크다. [[101_iot_concept|IoT]] 생태계의 최말단 신경망에 해당한다.

**3대 구성요소**

- **디바이스(Device)**: 센서·액추에이터·MCU(Micro Controller Unit)를 탑재한 엣지 노드. 배터리, 처리능력, 메모리 모두 수십~수백 mW·KB 수준으로 극도로 제약됨.
- **네트워크(Network)**: 노드 간 [[001_dikw_pyramid|데이터]]를 전달하는 무선 계층. 토폴로지(스타/[[389_mesh_topology|메시]]/클러스터)와 [[295_protocol_field_tcp_udp_icmp|프로토콜]]이 에너지 소비를 좌우함.
- **플랫폼(Platform)**: 클라우드·엣지에서 [[001_dikw_pyramid|데이터]]를 수집·[[093_normalization|정규화]]·분석. AWS [[101_iot_concept|IoT]] Core, Azure [[101_iot_concept|IoT]] [[152_hub_dummy_switching_intelligent|Hub]] 등이 대표 사례.

**[[103_wsn_sensor_network|WSN]] 핵심 구조 개념**

- **싱크 노드(Sink Node)**: 센서 노드들이 수집한 [[001_dikw_pyramid|데이터]]를 집결시켜 상위 네트워크로 전달하는 게이트웨이 역할. 보통 전원 제약 없이 상시 동작.
- **클러스터 헤드(Cluster Head)**: 인근 노드들의 [[001_dikw_pyramid|데이터]]를 집계·압축하여 싱크로 전달. 에너지 균형을 위해 순환 선출(LEACH [[295_protocol_field_tcp_udp_icmp|프로토콜]] 등).

- **📢 섹션 요약 비유**: [[101_iot_concept|IoT]] [[103_wsn_sensor_network|센서 네트워크]]는 전국 날씨 관측소 네트워크와 같다. 수천 개의 작은 기상 센서(노드)가 지역 집결소(클러스터 헤드)에 [[001_dikw_pyramid|데이터]]를 보내고, 집결소는 기상청 서버(싱크 노드 → 플랫폼)로 취합한다. 배터리로 산꼭대기에서 수년간 버텨야 하므로 "얼마나 자주 전송할지"가 생존의 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌─────────────────────────────────────────────────────────┐
│            IoT 3계층 아키텍처 및 무선 기술 분류             │
├─────────────────────────────────────────────────────────┤
│  [디바이스 계층]  센서 노드 (MCU + 센서 + 무선 모듈)         │
│      │  WPAN(ZigBee/BLE, ~10m)                         │
│      │  WLAN(Wi-Fi, ~100m, 고속)                        │
│      │  LPWAN(LoRa/NB-IoT, ~수km, 저전력)               │
│      ▼                                                  │
│  [네트워크 계층]  게이트웨이 / 싱크 노드                     │
│      │  인터넷(IP 백홀)                                   │
│      ▼                                                  │
│  [플랫폼 계층]   IoT 플랫폼 (수집·저장·분석·API)             │
│      │  대시보드 / 응용 서비스                              │
│      ▼                                                  │
│  [응용 계층]    스마트팩토리 / 스마트시티 / 헬스케어            │
└─────────────────────────────────────────────────────────┘
```

### 무선 기술 비교표

| 기술 [[104_classification_analysis|분류]] | 대표 기술 | 전송 범위 | 배터리 수명 | [[001_dikw_pyramid|데이터]]율 | 주요 용도 |
|:---:|:---:|:---:|:---:|:---:|:---:|
| [[604_wpan_wireless_personal_area_network|WPAN]] | [[609_zigbee_ieee_802_15_4_mesh_iot|ZigBee]], [[607_ble_bluetooth_low_energy_iot|BLE]] | [[489_raid_10_hybrid|10]]~100m | 수개월~2년 | 250kbps | 스마트홈, 헬스케어 |
| [[571_wlan_bss_ess_structure|WLAN]] | [[576_802_11ax_wifi_6_ofdma_twt|Wi-Fi 6]] | 100~200m | 수시간 | Gbps급 | 고화질 스트리밍 |
| [[109_lpwan_low_power_wide_area_network|LPWAN]](비면허) | LoRaWAN | 2~15km | 10년+ | 0.3~50kbps | 농업, 자산 추적 |
| [[109_lpwan_low_power_wide_area_network|LPWAN]](면허) | [[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]] | 수십km | 10년+ | 200kbps | 스마트 미터링 |

- **📢 섹션 요약 비유**: 무선 기술 선택은 택배 [[090_service_kubernetes_network_load_balancing|서비스]] 선택과 같다. 빠른 당일 배송(Wi-Fi, 고속·단거리)이 필요하면 비용이 높고, 10년짜리 장기 구독([[617_lora_lorawan_css_chirp_spread_spectrum|LoRa]], 저속·원거리)이면 느리지만 비용이 극히 낮다. 둘 다 잡을 수는 없다.

---

## Ⅲ. 비교 및 연결

**디바이스 제약 3대 과제**

- **배터리**: 대부분의 [[101_iot_concept|IoT]] 노드는 교체 불가 위치에 설치됨. 수신·전송·슬립 모드 전환 전략으로 소비 전력 최소화.
- **처리능력**: MCU는 ARM Cortex-M0/M3 수준(수십 MHz). 복잡한 암호화·[[190_ai_llm_requirements_specification|AI]] 추론은 엣지 게이트웨이에 위임.
- **메모리**: 수십 KB의 [[250_sram|SRAM]]·플래시. 경량 [[295_protocol_field_tcp_udp_icmp|프로토콜]]([[120_coap_constrained_application_protocol|CoAP]], MQTT-SN) 필수.

**토폴로지 비교**

- **스타(Star)**: 단순·저비용, 싱크 노드 [[454_spof|단일 장애점]]([[454_spof|SPOF]]).
- **[[389_mesh_topology|메시]]([[389_mesh_topology|Mesh]])**: 자가 치유, 다중 경로. [[609_zigbee_ieee_802_15_4_mesh_iot|ZigBee]]·[[092_thread_lwp|Thread]] 사용, 홉 증가 시 [[015_지연_데이터_관점|지연]] 누적.
- **클러스터 트리(Cluster-Tree)**: 에너지 균형, LEACH 기반 동적 클러스터링.

- **📢 섹션 요약 비유**: [[103_wsn_sensor_network|센서 네트워크]] 토폴로지는 학교 연락망이다. 반장(클러스터 헤드)이 모아서 선생님(싱크)에게 전달하면 효율적이지만, 반장 한 명이 빠지면 그 반 연락이 끊긴다. [[389_mesh_topology|메시]]는 학생 모두가 서로 전달하니 안전하지만 [[389_mesh_topology|메시]]지 경로가 복잡해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**기술 선택 시나리오**

| 시나리오 | 권장 기술 | 이유 |
|:---|:---:|:---|
| 농장 토양 수분 모니터링 (넓은 면적) | LoRaWAN | 배터리 수명·범위 우선 |
| 스마트홈 전등 제어 (빠른 반응) | [[609_zigbee_ieee_802_15_4_mesh_iot|ZigBee]]/[[607_ble_bluetooth_low_energy_iot|BLE]] | 낮은 [[015_지연_데이터_관점|지연]], 근거리 |
| 도시 [[024_gas|가스]] 미터기 원격 검침 | [[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]] | [[551_cellular_network_concept_reuse_handover|이동통신망]] 활용, 안정성 |
| 공장 고화질 카메라 스트리밍 | [[576_802_11ax_wifi_6_ofdma_twt|Wi-Fi 6]] | 고대역폭 필수 |

**기술사 답안 핵심 포인트**

1. 요구사항(범위·주기·페이로드·전원)을 먼저 정의한 후 기술 선택.
2. [[109_lpwan_low_power_wide_area_network|LPWAN]] 채택 시 업링크 중심([[001_dikw_pyramid|데이터]] 소량) 구조로 설계.
3. 보안: 디바이스 [[303_authentication_authorization_patterns|인증]]([[142_psk_pre_shared_key|PSK]]/[[159_pki_public_key_infrastructure|PKI]]), OTA([[523_iot_firmware_ota_security|Over-The-Air]]) [[032_firmware|펌웨어]] 업데이트 방안 포함.

- **📢 섹션 요약 비유**: 실무 [[101_iot_concept|IoT]] 설계는 건물 배관 설계와 같다. 어디에 어떤 굵기의 [[123_pipe|파이프]](통신 기술)를 놓을지는 물 사용량([[001_dikw_pyramid|데이터]]량)과 수압([[015_지연_데이터_관점|지연]] 요구)을 먼저 측정한 다음에 결정해야 한다. 먼저 [[123_pipe|파이프]]를 고르면 나중에 교체 비용이 폭증한다.

---

## Ⅴ. 기대효과 및 결론

[[101_iot_concept|IoT]] [[103_wsn_sensor_network|센서 네트워크]]는 제조·농업·도시 인프라에서 **실시간 가시성(Visibility)**을 제공함으로써 예방적 유지보수와 자원 최적화를 실현한다. 무선 기술의 발전([[109_lpwan_low_power_wide_area_network|LPWAN]] 정확도 향상, 에너지 하베스팅)과 엣지 [[190_ai_llm_requirements_specification|AI]] 결합으로 자율적 의사결정 능력이 확대되고 있다.

핵심 결론: **디바이스 제약 → 통신 기술 선택 → 아키텍처 설계**의 논리적 흐름을 시험 답안에서 반드시 전개해야 한다.

- **📢 섹션 요약 비유**: [[101_iot_concept|IoT]] [[103_wsn_sensor_network|센서 네트워크]]는 도시에 깔리는 신경계다. 뇌(플랫폼)가 아무리 뛰어나도 말초 신경(센서 노드)이 배터리 방전으로 죽어버리면 도시는 눈이 멀게 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[103_wsn_sensor_network|WSN]](Wireless Sensor Network) | 싱크 노드, LEACH · [[101_iot_concept|IoT]] 말단 감지 네트워크 |
| [[109_lpwan_low_power_wide_area_network|LPWAN]] | [[617_lora_lorawan_css_chirp_spread_spectrum|LoRa]], [[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]], [[1030_lpwan_sigfox|Sigfox]] · 저전력 광역 통신 |
| 클러스터 헤드 | LEACH, 에너지 균형 · 노드 군집 집계자 |
| [[101_iot_concept|IoT]] 플랫폼 | AWS [[101_iot_concept|IoT]], Azure [[101_iot_concept|IoT]] · [[001_dikw_pyramid|데이터]] 수집·처리 |
| 에너지 하베스팅 | 태양광, 진동 · 배터리 의존도 탈피 |

### 📈 관련 키워드 및 발전 흐름도

```text
[싱크 노드 · LEACH] → [IoT 센서 네트워크 종합] → [태양광 · 진동]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[101_iot_concept|IoT]] [[103_wsn_sensor_network|센서 네트워크]]는 집 안 곳곳에 붙인 온도계 스티커들이 서로 대화해서 엄마 스마트폰으로 알려주는 것이에요.
2. 배터리가 작아서 오래 써야 하니까, 꼭 필요할 때만 잠깐 말하고(전송) 나머지는 잠(슬립 모드)을 자요.
3. 멀리 있는 온도계는 큰 소리로 외쳐야 하고([[109_lpwan_low_power_wide_area_network|LPWAN]]), 가까운 건 귓속말로 충분해요([[607_ble_bluetooth_low_energy_iot|BLE]]).
