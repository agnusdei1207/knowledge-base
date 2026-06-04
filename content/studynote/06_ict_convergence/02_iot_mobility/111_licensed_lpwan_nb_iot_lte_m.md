+++
title = "111. 면허 대역 LPWAN - NB-IoT vs LTE-M 3GPP 표준 IoT 통신"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 면허 대역 LPWAN은 통신사가 보유한 <strong><a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/">LTE</a> 면허 주파수 대역</strong>을 활용하여 [NB-IoT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/620_nbiot_narrowband_iot_lte_guardband/)(200kHz 협대역)와 [LTE-M](/knowledge-base/studynote/03_network/12_iot_wpan_edge/621_ltem_emtc_iot_mobility_voice/)(1.4MHz 광대역)으로 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 디바이스에 <strong>통신사급 <a href="/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/">QoS</a>(품질 보장)</strong>를 제공하는 [3GPP](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/751_3gpp_3rd_generation_partnership_project/) 국제 표준 기술이다.
> 2. **가치**: 비면허 [LPWAN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/)([LoRa](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/)·[Sigfox](/knowledge-base/studynote/03_network/12_iot_wpan_edge/1030_lpwan_sigfox/))이 Best Effort인 반면, 면허 대역은 통신사 기지국 인프라를 그대로 활용하여 <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/">SLA</a> 보장·이동성(<a href="/knowledge-base/studynote/03_network/11_wireless_mobile_communication/556_handover_handoff_types_concept/">Handover</a>)·양방향 통신</strong>이 가능하며 별도 GW 구축이 불필요하다.
> 3. **판단 포인트**: NB-IoT는 **고정형·초저전력·초소량**(스마트 미터), [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/)-M은 **이동형·음성·중속도**(자산 추적·웨어러블)에 적합하며, [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) Release 17 RedCap으로 통합 진화 중이다.

---

## Ⅰ. 개요 및 필요성

비면허 [LPWAN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/)([LoRa](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/))은 자체 GW를 깔아야 하고 [QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 보장이 없다. 통신사 입장에서는 이미 전국에 깔아놓은 [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 기지국의 빈 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)([Guard Band](/knowledge-base/studynote/03_network/19_frequent_topics_terms/946_guard_band_fdm_adjacent_channel_interference/))을 재활용하여 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 시장을 공략할 수 있으며, 기업 고객에게 SLA를 보장할 수 있다.

```text
+-------------------------------------------------------+
|     NB-IoT vs LTE-M 포지셔닝 맵                       |
+-------------------------------------------------------+
|  속도 ^                                               |
|  1Mbps |               ★ LTE-M                       |
| 200kbps|        ☆ NB-IoT                              |
|  600bps|  ◇ Sigfox                                    |
|  50kbps|     ◆ LoRa                                   |
|        +-----------------------------> 이동성           |
|        고정               Handover 지원               |
|                                                       |
|  QoS: ◇◆ Best Effort   ☆★ 통신사 SLA 보장           |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: NB-IoT는 편의점 택배(고정 배달, 저렴), [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/)-M은 퀵서비스(이동 배달, 빠름). 둘 다 택배회사(통신사) 인프라를 사용한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 항목 | [NB-IoT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/620_nbiot_narrowband_iot_lte_guardband/) | [LTE-M](/knowledge-base/studynote/03_network/12_iot_wpan_edge/621_ltem_emtc_iot_mobility_voice/) (Cat-M1) |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/751_3gpp_3rd_generation_partnership_project/">3GPP</a> Release</strong> | Rel-13 (2016) | Rel-13 (2016) |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">대역폭</a></strong> | 200 kHz (협대역) | 1.4 MHz |
| **최대 속도** | DL 200 kbps | DL 1 Mbps |
| **이동성** | 제한적 ([Handover](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/556_handover_handoff_types_concept/) 미지원) | **완전 지원** |
| **음성** | 미지원 | <strong><a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/758_volte_voice_over_lte_sip_qos/">VoLTE</a> 지원</strong> |
| **전력 절감** | PSM + eDRX | PSM + eDRX |
| **커버리지 확장** | MCL 164 dB (지하 침투) | MCL 156 dB |
| **적합 용도** | 고정 센서, 스마트 미터 | 이동 추적, 웨어러블 |

### 전력 절감 메커니즘
- <strong>PSM (<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/">Power</a> Saving Mode)</strong>: 통신 완료 후 모듈을 완전히 꺼서 수 μA 수준으로 대기.
- **eDRX (extended DRX)**: 수신 대기 주기를 수초->수십 분으로 확장하여 전력 절감.

- **📢 섹션 요약 비유**: PSM은 직원이 퇴근 후 건물 전기를 전부 끄는 것이고, eDRX는 "1시간에 한 번만 우편함을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)"하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [LoRa](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) (비면허) | [NB-IoT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/620_nbiot_narrowband_iot_lte_guardband/) (면허) | [LTE-M](/knowledge-base/studynote/03_network/12_iot_wpan_edge/621_ltem_emtc_iot_mobility_voice/) (면허) |
|:---|:---|:---|:---|
| **인프라** | 자체 GW | 통신사 기지국 | 통신사 기지국 |
| <strong><a href="/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/">QoS</a></strong> | Best Effort | <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/">SLA</a> 보장</strong> | <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/">SLA</a> 보장</strong> |
| **이동성** | 제한 | 제한 | <strong><a href="/knowledge-base/studynote/03_network/11_wireless_mobile_communication/556_handover_handoff_types_concept/">Handover</a></strong> |
| **비용** | GW 자체 구축 | 월정액 | 월정액 |
| **음성** | 불가 | 불가 | <strong><a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/758_volte_voice_over_lte_sip_qos/">VoLTE</a></strong> |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 선택 기준
1. **고정 설치 + 초소량**: 수도·전기 계량기 -> [NB-IoT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/620_nbiot_narrowband_iot_lte_guardband/).
2. **이동 + 음성**: 독거 노인 긴급 호출 웨어러블 -> [LTE-M](/knowledge-base/studynote/03_network/12_iot_wpan_edge/621_ltem_emtc_iot_mobility_voice/).
3. <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/">SLA</a> 필수</strong>: 의료·산업 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) -> 면허 대역 ([NB-IoT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/620_nbiot_narrowband_iot_lte_guardband/)/[LTE-M](/knowledge-base/studynote/03_network/12_iot_wpan_edge/621_ltem_emtc_iot_mobility_voice/)).

### [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) RedCap (Release 17)
NB-IoT와 [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/)-M을 하나의 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 프레임워크로 통합하는 경량 [5G NR](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/763_5g_nr_new_radio_scalable_numerology/) 규격. 기존 LPWAN의 후계자로 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 시대의 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 표준이 될 전망.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 비면허 [LPWAN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/) | 면허 [LPWAN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/) | 개선 |
|:---|:---|:---|:---|
| [QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) | Best Effort | <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/">SLA</a> 보장</strong> | [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 확보 |
| 인프라 구축 | 자체 GW 필요 | **통신사 전국망** | 즉시 사용 |
| 이동성 | 제한 | <strong><a href="/knowledge-base/studynote/03_network/11_wireless_mobile_communication/556_handover_handoff_types_concept/">Handover</a> (<a href="/knowledge-base/studynote/03_network/12_iot_wpan_edge/621_ltem_emtc_iot_mobility_voice/">LTE-M</a>)</strong> | 이동 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 가능 |

NB-IoT와 [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/)-M은 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) RedCap으로 수렴하며, 위성 NTN(Non-Terrestrial Network)과 결합하여 전지구 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 커버리지를 향해 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/03_network/12_iot_wpan_edge/620_nbiot_narrowband_iot_lte_guardband/">NB-IoT</a></strong> | 200kHz 협대역 면허 [LPWAN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/), 고정 센서 |
| <strong><a href="/knowledge-base/studynote/03_network/12_iot_wpan_edge/621_ltem_emtc_iot_mobility_voice/">LTE-M</a> (Cat-M1)</strong> | 1.4MHz 면허 [LPWAN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/), 이동+음성 |
| **PSM / eDRX** | 면허 LPWAN의 극저전력 메커니즘 |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">5G</a> RedCap (Rel-17)</strong> | [NB-IoT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/620_nbiot_narrowband_iot_lte_guardband/)·[LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/)-M의 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 통합 후계자 |
| **LoRaWAN** | 비면허 대역 경쟁 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
[2G/3G M2M (2000s) — 고전력·고비용 원격 IoT]
    |
    v
[3GPP Rel-13 (2016) — NB-IoT·LTE-M 표준화]
    |
    v
[전국망 상용화 (2018~) — 통신 3사 NB-IoT 서비스 개시]
    |
    v
[5G RedCap (Rel-17, 2022~) — 경량 5G NR로 통합]
    |
    v
[현재: 5G NTN (위성) + RedCap — 전지구 IoT]
```

### 👶 어린이를 위한 3줄 비유 설명
1. NB-IoT는 집에 고정된 <strong>수도 계량기</strong>가 매달 숫자를 보내는 통신이에요.
2. [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/)-M은 할머니 팔찌(웨어러블)가 **움직이면서도** 위치와 건강 정보를 보내는 통신이에요.
3. 둘 다 전화회사(통신사)가 관리하니까 <strong>안정적</strong>이고, 전기(배터리)를 아주 적게 써요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 111 / 552

<- **이전**: [110. 비면허 LPWAN - LoRaWAN (CSS) vs Sigfox (UNB) 대역 확산 기술 비교](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/110_unlicensed_lpwan_lorawan_sigfox/)
**다음**: [112. Zigbee 메시 네트워크 (Zigbee Mesh Network) - IEEE 802.15.4 스마트 홈 WPAN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/112_zigbee_mesh_network_smart_home/) ->

---
