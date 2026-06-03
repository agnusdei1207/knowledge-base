+++
title = "110. 비면허 LPWAN - LoRaWAN (CSS) vs Sigfox (UNB) 대역 확산 기술 비교"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 비면허 대역 LPWAN은 정부가 무료 개방한 <strong>ISM 밴드(900MHz 부근)</strong>에서 통신사 인프라 없이 <strong>자가 기지국으로 도시 규모 <a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a> 사설망을 구축</strong>하는 기술이며, LoRaWAN(CSS 변조)과 [Sigfox](/knowledge-base/studynote/03_network/12_iot_wpan_edge/1030_lpwan_sigfox/)(UNB 변조)가 양대 산맥이다.
> 2. **가치**: LoRaWAN은 <strong>Chirp <a href="/knowledge-base/studynote/03_network/01_data_communication/068_스펙트럼_확산_Spread_Spectrum/">Spread Spectrum</a>(CSS)</strong>으로 넓게 펼쳐 노이즈를 뚫고, Sigfox는 <strong>Ultra Narrow Band(UNB)</strong>로 100Hz에 에너지를 몰빵하여 초장거리를 달성한다. 정반대 전략으로 같은 목표(원격 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/))를 해결한다.
> 3. **판단 포인트**: LoRaWAN은 <strong>자체 GW 구축(자유도↑)</strong>이 가능하여 사설 IoT에 적합하고, Sigfox는 <strong>본사 망 독점 운영(관리 편의↑)</strong>이지만 확장에 한계가 있어 하락세다.

---

## Ⅰ. 개요 및 필요성

국가 전파는 한정 자원으로 통신사가 수조 원에 경매하여 독점 사용(면허 대역)하지만, 정부는 일부 주파수(ISM 밴드)를 <strong>출력 제한 하에 무료 개방</strong>하고 있다. Wi-Fi(2.4GHz)·Bluetooth가 이 무료 도로를 쓰듯, LoRa와 Sigfox도 900MHz 비면허 대역에서 자체 규칙으로 도시 규모 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 사설망을 구축한다.

```text
┌───────────────────────────────────────────────────────┐
│      LoRa (CSS) vs Sigfox (UNB) 변조 방식 비교         │
├───────────────────────────────────────────────────────┤
│  [LoRa: Chirp Spread Spectrum]                        │
│   주파수 ▲                                            │
│          /  ← Chirp (낮→높으로 쭉 올라가는 패턴)      │
│         /   넓은 대역에 에너지를 펼침                  │
│        /    → 노이즈가 일부 깨워도 패턴으로 복원       │
│   ────────────────→ 시간                              │
│                                                       │
│  [Sigfox: Ultra Narrow Band]                          │
│   에너지 ▲  ████  ← 100Hz 초협대역에 에너지 몰빵     │
│          │  ████    면도칼처럼 얇고 강력               │
│          │  ████  → 하루 12바이트 한계, 초장거리       │
│   ────────────────→ 주파수                            │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: LoRa는 덤프트럭(넓게 펼쳐 충격 흡수)이고, Sigfox는 오토바이(좁고 날렵하게 돌파)다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 항목 | LoRaWAN (CSS) | [Sigfox](/knowledge-base/studynote/03_network/12_iot_wpan_edge/1030_lpwan_sigfox/) (UNB) |
|:---|:---|:---|
| **변조** | Chirp [Spread Spectrum](/knowledge-base/studynote/03_network/01_data_communication/068_스펙트럼_확산_Spread_Spectrum/) | Ultra Narrow Band |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">대역폭</a></strong> | 125~500 kHz (넓게 펼침) | 100 Hz (극단적 좁음) |
| **속도** | 0.3~50 kbps | 100~600 bps |
| **커버리지** | 15~30 km | 30~50 km |
| **GW 구축** | **자유** (누구나 [안테나](/knowledge-base/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 설치) | 본사 독점 |
| **메시지 제한** | 없음 (Duty Cycle만 준수) | 하루 140건, 12바이트 |
| **양방향** | 지원 (Class A/B/C) | 제한적 (다운링크 4건/일) |
| **한국 현황** | SKT·한전 전국망 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 축소 |

### LoRaWAN 클래스

| 클래스 | 수신 방식 | 전력 | 용도 |
|:---|:---|:---|:---|
| **A** | 업링크 후 짧은 수신 창 | 최저 | 센서 (대부분) |
| **B** | 비콘 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 주기적 수신 | 중간 | 액추에이터 |
| **C** | 상시 수신 | 최고 | 게이트웨이·전원 장비 |

- **📢 섹션 요약 비유**: LoRaWAN Class A는 "내가 말할 때만 귀를 여는" 절전형이고, Class C는 "항상 전화기를 들고 있는" 상시 대기형이다.

---

## Ⅲ. 비교 및 연결

| 비교 | LoRaWAN | [Sigfox](/knowledge-base/studynote/03_network/12_iot_wpan_edge/1030_lpwan_sigfox/) | [NB-IoT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/620_nbiot_narrowband_iot_lte_guardband/) (면허) |
|:---|:---|:---|:---|
| **대역** | 비면허 | 비면허 | 면허 |
| **GW 자유도** | 자체 구축 | 본사 독점 | 통신사 |
| <strong><a href="/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/">QoS</a></strong> | Best Effort | Best Effort | **보장** |
| **양방향** | 지원 | 제한 | 완전 지원 |
| **생태계** | 개방, 활발 | 폐쇄, 하락 | [3GPP](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/751_3gpp_3rd_generation_partnership_project/) 표준 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### LoRaWAN 적합 시나리오
1. **스마트 농업**: 자가 GW 1대로 농장 전체 커버, 토양 센서 수백 개 운영.
2. <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/171_smart_city_platform_architecture/">스마트 시티</a></strong>: 공공 가로등·쓰레기통 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/), 시 자체 사설망 구축.

### [Sigfox](/knowledge-base/studynote/03_network/12_iot_wpan_edge/1030_lpwan_sigfox/) 적합 시나리오
- **초장거리·초소량**: 사막/해양 자산 추적 (하루 위치 1회 전송).

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **Sigfox로 실시간 모니터링**: 하루 140건 메시지 제한 → 실시간 불가.
- **LoRa로 영상 전송**: 50 kbps 한계 → 영상 전송 물리적 불가능.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 셀룰러 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) | LoRaWAN | 개선 |
|:---|:---|:---|:---|
| 센서당 통신비 | 월 5,000원 | **월 0원 (자가 GW)** | 100% 절감 |
| GW 1대 커버리지 | 2~5 km | **15~30 km** | 6배 |
| 망 자유도 | 통신사 의존 | **자체 구축** | 완전 자율 |

LoRaWAN은 비면허 LPWAN의 승자로 굳어지고 있으며, 위성 [LoRa](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/)(Amazon Sidewalk, Lacuna Space)로 진화하여 전지구 커버리지를 향해 나아가고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/">LPWAN</a></strong> | LoRaWAN·Sigfox가 속하는 상위 기술 범주 |
| **ISM 밴드** | 비면허 대역, 무료 사용 가능한 주파수 |
| <strong>CSS (Chirp <a href="/knowledge-base/studynote/03_network/01_data_communication/068_스펙트럼_확산_Spread_Spectrum/">Spread Spectrum</a>)</strong> | LoRa의 핵심 변조 방식, 대역 확산 |
| **UNB (Ultra Narrow Band)** | Sigfox의 핵심 변조 방식, 초협대역 |
| <strong><a href="/knowledge-base/studynote/03_network/12_iot_wpan_edge/620_nbiot_narrowband_iot_lte_guardband/">NB-IoT</a></strong> | 면허 대역 [LPWAN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/), 통신사 인프라 활용 경쟁 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
[ISM 밴드 개방 — 비면허 주파수 무료 사용 허용]
    │
    ▼
[Sigfox (2012, 프랑스) — UNB 최초 상용 LPWAN]
    │
    ▼
[LoRa (2013, Semtech) — CSS 기반 개방형 LPWAN]
    │
    ▼
[LoRa Alliance 표준화 (2015~) — LoRaWAN 프로토콜 확립]
    │
    ▼
[현재: 위성 LoRa (Lacuna Space) — 전지구 IoT 커버리지]
```

### 👶 어린이를 위한 3줄 비유 설명
1. LoRa는 큰 목소리(넓은 전파)로 소리치면서 시끄러운 운동장에서도 친구에게 메시지를 전하는 방법이에요.
2. Sigfox는 아주 작은 목소리(좁은 전파)지만 **레이저처럼 정확하게** 한 친구에게만 쏘는 방법이에요.
3. 둘 다 전기(배터리)를 아주 조금만 쓰고 아주 멀리까지 메시지를 보낼 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 110 / 552

← **이전**: [109. 저전력 광역 통신망 (LPWAN) - LoRa·Sigfox·NB-IoT 기술 비교](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/)
**다음**: [111. 면허 대역 LPWAN - NB-IoT vs LTE-M 3GPP 표준 IoT 통신](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/111_licensed_lpwan_nb_iot_lte_m/) →

---
