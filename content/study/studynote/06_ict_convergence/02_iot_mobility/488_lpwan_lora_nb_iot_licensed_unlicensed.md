+++
weight = 488
title = "488. LPWAN: LoRa, NB-IoT 면허/비면허 비교 (LPWAN: LoRa NB-IoT Licensed Unlicensed)"
date = "2026-05-09"
[extra]
categories = "studynote-ict-convergence"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[109_lpwan_low_power_wide_area_network|LPWAN]]([[615_lpwan_low_power_wide_area_network|Low-Power Wide-Area Network]])은 수 km 이상의 넓은 지역에 배터리로 10년 이상 동작하는 수백만 [[101_iot_concept|IoT]] 기기를 연결하기 위해 설계된 저전력 광역 통신 기술 군(群)이다.
> 2. **가치**: 비면허 대역 기반의 LoRaWAN·Sigfox는 독립 인프라로 자유 구축이 가능하며, 면허 대역 기반의 [[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]]·[[752_lte_long_term_evolution_4g|LTE]]-M은 기존 이동통신 망을 활용해 신뢰도와 이동성을 보장한다.
> 3. **판단 포인트**: 고정 저빈도 소량 [[001_dikw_pyramid|데이터]](검침, 환경 모니터링)엔 LoRaWAN이나 [[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]], 이동 중 음성·중속 [[001_dikw_pyramid|데이터]](반려동물 추적, 웨어러블)엔 [[621_ltem_emtc_iot_mobility_voice|LTE-M]]([[621_ltem_emtc_iot_mobility_voice|eMTC]])이 최적이다.

---

## Ⅰ. 개요 및 필요성

**[[109_lpwan_low_power_wide_area_network|LPWAN]] 등장 배경**

기존 [[604_wpan_wireless_personal_area_network|WPAN]]([[609_zigbee_ieee_802_15_4_mesh_iot|ZigBee]], [[607_ble_bluetooth_low_energy_iot|BLE]])은 범위가 수십 m에 불과하고, 이동통신(4G [[752_lte_long_term_evolution_4g|LTE]])은 전력 소비가 커서 배터리 [[101_iot_concept|IoT]] 기기에 부적합했다. 수 km 이상의 넓은 지역을 수년간 배터리로 커버하는 틈새 요구를 LPWAN이 채운다.

**[[109_lpwan_low_power_wide_area_network|LPWAN]] 핵심 특성**

- 배터리 수명: 10년 이상 (초저전력 설계)
- 전송 거리: 2~50km
- [[001_dikw_pyramid|데이터]]율: 수백 bps~수십 kbps (저속)
- 동시 접속: 수백만 기기/기지국

- **📢 섹션 요약 비유**: LPWAN은 우체통과 같다. 속도는 빠르지 않지만, 멀리 있는 동네(넓은 범위)에 편지를 10년간 배달할 수 있다. 인터넷 익스프레스([[752_lte_long_term_evolution_4g|LTE]])는 빠르지만 배터리를 엄청 잡아먹는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌───────────────────────────────────────────────────────────┐
│                 LPWAN 기술 분류 체계                        │
├──────────────────────────┬────────────────────────────────┤
│    비면허(Unlicensed)      │       면허(Licensed)            │
├──────────────────────────┼────────────────────────────────┤
│  LoRaWAN                 │  NB-IoT (Narrowband IoT)       │
│  - CSS(Chirp Spread       │  - 3GPP Release 13             │
│    Spectrum) 변조          │  - LTE 보호대역(200kHz) 활용    │
│  - Star-of-Stars 토폴로지  │  - 최대 200kbps               │
│  - 전송 범위 2~15km        │  - PSM/eDRX 초저전력 모드       │
│                          │                                │
│  Sigfox                  │  LTE-M (eMTC)                  │
│  - UNB(Ultra Narrow Band)│  - 3GPP Release 13             │
│  - 최대 140 메시지/일       │  - 이동성 + 음성(VoLTE) 지원    │
│  - 12 바이트 페이로드 한계  │  - 최대 1Mbps                  │
└──────────────────────────┴────────────────────────────────┘
```

### [[109_lpwan_low_power_wide_area_network|LPWAN]] 기술 상세 비교표

| 항목 | LoRaWAN | [[1030_lpwan_sigfox|Sigfox]] | [[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]] | [[621_ltem_emtc_iot_mobility_voice|LTE-M]] |
|:---:|:---:|:---:|:---:|:---:|
| 스펙트럼 | 비면허(ISM) | 비면허(ISM) | 면허([[752_lte_long_term_evolution_4g|LTE]] [[571_protection_vs_security|보호]]대역) | 면허([[752_lte_long_term_evolution_4g|LTE]]) |
| 전송 거리 | 2~15km | [[489_raid_10_hybrid|10]]~50km | 수십km | 수십km |
| 최대 [[001_dikw_pyramid|데이터]]율 | 50kbps | 100bps | 200kbps | 1Mbps |
| 배터리 수명 | 10년+ | 10년+ | 10년+ | 5~10년 |
| 이동성 | 제한적 | 낮음 | 낮음 | 지원 |
| 메시지/일 제한 | 없음 | 140개 | 없음 | 없음 |
| 인프라 | 자체 구축 | [[1030_lpwan_sigfox|Sigfox]] 전용 | 통신사 망 | 통신사 망 |

**LoRaWAN Star-of-Stars 토폴로지**: 종단 노드 → 게이트웨이(복수) → 네트워크 서버 → 앱 서버. 게이트웨이는 여러 노드의 패킷을 수신해 서버로 전달, 서버가 중복 제거·[[339_routing_overview_best_path_selection|라우팅]] 담당.

- **📢 섹션 요약 비유**: LoRaWAN은 개인 라디오 방송국이다. 내 땅에 안테나를 세워 마음대로 방송하지만 채널(주파수)이 자유롭지 않아 혼선이 생길 수 있다. NB-IoT는 KT/SKT 공중파다. 혼선 없이 안정적이지만 통신사 요금을 내야 한다.

---

## Ⅲ. 비교 및 연결

**비면허 vs 면허 핵심 트레이드오프**

| 항목 | 비면허 ([[617_lora_lorawan_css_chirp_spread_spectrum|LoRa]], [[1030_lpwan_sigfox|Sigfox]]) | 면허 ([[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]], [[621_ltem_emtc_iot_mobility_voice|LTE-M]]) |
|:---|:---:|:---:|
| [[459_quic_fec_forward_error_correction|초기]] 비용 | 낮음 (자체 구축 가능) | 높음 (통신사 계약) |
| 간섭 위험 | 있음 (ISM 혼잡) | 없음 ([[074_보호_대역_Guard_Band|보호 대역]]) |
| [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] 보장 | 미보장 | [[085_sla|SLA]] 보장 |
| 배포 속도 | 빠름 | 통신사 의존 |
| 이동성 | 낮음 | [[621_ltem_emtc_iot_mobility_voice|LTE-M]] 지원 |

**eDRX(Extended Discontinuous Reception)와 PSM([[069_type_1_2_error_statistical_power|Power]] Saving Mode)**: [[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]]/[[752_lte_long_term_evolution_4g|LTE]]-M의 초저전력 핵심. PSM은 등록 유지하면서 수신 회로를 꺼 배터리를 극대화한다.

- **📢 섹션 요약 비유**: eDRX/PSM은 알람 맞춰놓고 자는 것이다. 정해진 시간에만 잠깐 깨서(수신) 메시지를 확인하고, 나머지 시간은 깊이 잠든다(슬립). 덕분에 배터리가 10년간 버틴다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**응용 사례 선택 기준**

| 응용 사례 | 권장 기술 | 이유 |
|:---|:---:|:---|
| 농업 토양 센서 (고정, 저빈도) | LoRaWAN | 자체 인프라, 낮은 비용 |
| 스마트 [[024_gas|가스]] 미터 (도시, [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]) | [[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]] | 이통망 활용, [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] 보장 |
| 반려동물 GPS 추적 (이동성) | [[621_ltem_emtc_iot_mobility_voice|LTE-M]] | 이동성·음성 지원 |
| 주차장 점유 감지 (저밀도 도시) | [[1030_lpwan_sigfox|Sigfox]] | 초소량 [[001_dikw_pyramid|데이터]], 저비용 |

**기술사 필수 포인트**

1. LoRaWAN [[231_adr_architecture_decision_record_documentation|ADR]](Adaptive [[001_dikw_pyramid|Data]] Rate): [[130_signal|신호]] 강도에 따라 전송 속도·전력 자동 조절.
2. [[1030_lpwan_sigfox|Sigfox]] 메시지 한도(140개/일)는 알림·경보 용도에만 적합, 연속 모니터링 불가.
3. [[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]] In-band/Guard-band/[[150_5g_sa_standalone_architecture|Standalone]] 배포 옵션 이해.

- **📢 섹션 요약 비유**: [[109_lpwan_low_power_wide_area_network|LPWAN]] 기술 선택은 배달 방법 선택이다. 시골 직배송([[617_lora_lorawan_css_chirp_spread_spectrum|LoRa]] 자체 구축)은 자유롭지만 직접 트럭을 사야 한다. 쿠팡 로켓배송([[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]], 통신사)은 안정적이지만 이용료를 낸다. 드론 배송([[1030_lpwan_sigfox|Sigfox]])은 초경량 편지만 가능하다.

---

## Ⅴ. 기대효과 및 결론

LPWAN은 스마트 미터링·정밀 농업·스마트시티 인프라에서 수백만 [[101_iot_concept|IoT]] 노드의 경제적 연결 기반을 제공한다. 비면허([[617_lora_lorawan_css_chirp_spread_spectrum|LoRa]])와 면허([[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]]/[[621_ltem_emtc_iot_mobility_voice|LTE-M]])의 생태계가 병존하며, 프로젝트 요구사항([[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]·이동성·인프라 자율성)에 따라 최적 기술이 달라진다.

- **📢 섹션 요약 비유**: LPWAN은 장거리 마라톤용 운동화다. 빠른 단거리 [[129_spike_agile_technical_investigation|스파이크]]([[752_lte_long_term_evolution_4g|LTE]])와 달리, 느리지만 10년을 달릴 수 있는 지구력 특화 장비다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[110_unlicensed_lpwan_lorawan_sigfox|CSS]](Chirp [[068_스펙트럼_확산_Spread_Spectrum|Spread Spectrum]]) | [[617_lora_lorawan_css_chirp_spread_spectrum|LoRa]] 물리 계층 · 치프 [[954_spread_spectrum_communication_anti_jamming_cdma|확산 스펙트럼]] 변조 |
| PSM/eDRX | [[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]], [[621_ltem_emtc_iot_mobility_voice|LTE-M]] · 초저전력 슬립 모드 |
| Star-of-Stars | LoRaWAN 토폴로지 · 게이트웨이 복수 수신 구조 |
| [[231_adr_architecture_decision_record_documentation|ADR]](Adaptive [[001_dikw_pyramid|Data]] Rate) | LoRaWAN · 자동 전송률·전력 조절 |
| ISM 대역 | 비면허 [[109_lpwan_low_power_wide_area_network|LPWAN]] · 산업·과학·의료용 공용 주파수 |

### 📈 관련 키워드 및 발전 흐름도

```text
[LoRa 물리 계층 · 치프 확산 스펙트럼 변조] → [LPWAN: LoRa · NB-IoT 면허] → [비면허 LPWAN · 산업]
```

### 👶 어린이를 위한 3줄 비유 설명

1. LoRa는 저전력 봉화 [[130_signal|신호]]예요. 배터리 하나로 10년 동안 산꼭대기에서 [[130_signal|신호]]를 보낼 수 있어요.
2. NB-IoT는 이동통신 회사가 깔아준 안전한 전용선이에요. 끊김이 없는 대신 요금을 내야 해요.
3. Sigfox는 엽서 배달부예요. 딱 12글자짜리 초소형 메시지만 하루 140번 보낼 수 있어요.
