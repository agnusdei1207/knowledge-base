+++
title = "496. 6G 테라헤르츠, NTN, RIS 기술 (6G Terahertz NTN RIS Satellite Communication)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [6G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/)(6th Generation)는 ITU-R IMT-2030 표준으로, [테라헤르츠](/knowledge-base/studynote/03_network/03_physical_layer_media/157_terahertz_thz_6g/)([THz](/knowledge-base/studynote/03_network/03_physical_layer_media/157_terahertz_thz_6g/), 100GHz~10THz) 대역을 활용해 Tbps급 속도와 10μs 이하 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 목표로 하며, AI가 네트워크 설계에 내재화([AI-Native](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/792_ai_native_6g_neural_network_radio/))되는 차세대 이동통신이다.
> 2. **가치**: NTN(Non-Terrestrial Network)으로 위성·[HAPS](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/596_haps_high_altitude_platform_station_drone/)(고고도 플랫폼)를 통합하여 해상·오지의 커버리지 공백을 해소하고, RIS(Reconfigurable Intelligent Surface)로 전파 방향을 능동 제어해 음영지역(Dead Zone)을 소프트웨어적으로 제거한다.
> 3. **판단 포인트**: [THz](/knowledge-base/studynote/03_network/03_physical_layer_media/157_terahertz_thz_6g/) 대역은 극고속이지만 경로 손실과 대기 흡수가 심해 수십 m 이내 통신에 제한된다. NTN·RIS는 이 한계를 보완하는 핵심 기술이며, 기술사 시험에서 6G의 도전 과제와 해결책을 세트로 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

<strong>5G의 한계와 <a href="/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/">6G</a> 필요성</strong>

- **커버리지 공백**: [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 지상 기지국은 해양·산악·극지 등 전 지구 육지의 20% 미만 커버.
- **음영지역**: 실내·터널·도심 협곡. 빌딩 반사로 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 왜곡.
- <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 통합 부재</strong>: 5G는 네트워크가 AI를 서비스로 운반하지만, 망 자체에 AI가 내재화되지 않음.

<strong><a href="/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/">6G</a> ITU-R IMT-2030 핵심 목표</strong>

| 지표 | [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) (IMT-2020) | [6G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/) (IMT-2030 목표) |
|:---:|:---:|:---:|
| 최대 데이터율 | 20Gbps | 1Tbps |
| [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) | 1ms | 10μs (0.01ms) |
| 주파수 대역 | ~100GHz | [THz](/knowledge-base/studynote/03_network/03_physical_layer_media/157_terahertz_thz_6g/) (100GHz~10THz) |
| 위치 정확도 | 미터 | 센티미터 |
| 커버리지 | 지상 중심 | 비지상(NTN) 통합 |

- **📢 섹션 요약 비유**: 5G가 고속열차라면 6G는 하이퍼루프다. 5G가 아직 달리고 있는 동안 6G는 완전히 다른 인프라([THz](/knowledge-base/studynote/03_network/03_physical_layer_media/157_terahertz_thz_6g/) 주파수, 위성, 스마트 반사 벽)를 새로 깔고 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌──────────────────────────────────────────────────────────┐
│           6G 통합 네트워크 아키텍처 (3계층)                 │
├──────────────────────────────────────────────────────────┤
│  [비지상 계층 - NTN]                                       │
│  LEO 위성(Starlink 등, 550km) / MEO(8,000km) / GEO(36,000km)│
│  HAPS(High-Altitude Platform Station, 20km 성층권)         │
│        │  위성-지상 직접 통신 / 위성간 ISL 링크             │
│        ▼                                                  │
│  [지상 계층 - Terrestrial]                                 │
│  6G gNB(THz 기지국, 초소형·밀집 배치)                      │
│        │                                                  │
│  [RIS 계층]                                                │
│  ┌────────────────────────────────────────────────┐      │
│  │ RIS(Reconfigurable Intelligent Surface)        │      │
│  │ - 메타물질 패널(수백~수천 개 반사 소자)           │      │
│  │ - 전파 방향·위상 프로그래머블 제어               │      │
│  │ - 능동 증폭 없이 신호 반사·굴절 → 음영지역 제거   │      │
│  └────────────────────────────────────────────────┘      │
│        ▼                                                  │
│  [단말 계층]  스마트폰·XR·자율주행·IoT                      │
└──────────────────────────────────────────────────────────┘
```

### [6G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/) 핵심 기술 비교

| 기술 | 개요 | 특징 |
|:---:|:---:|:---:|
| [THz](/knowledge-base/studynote/03_network/03_physical_layer_media/157_terahertz_thz_6g/) 통신 | 100GHz~10THz 대역 | 1Tbps 가능, 경로 손실 심각(수십 m 제한) |
| NTN(Non-Terrestrial) | [LEO](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/)/[HAPS](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/596_haps_high_altitude_platform_station_drone/)/[GEO](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/593_geo_geostationary_earth_orbit_satellite/) 위성 | 전 지구 커버리지, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 차이 큼 |
| RIS | 메타물질 반사 표면 | 수동 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 반사, 저전력 음영 해소 |
| [AI-Native](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/792_ai_native_6g_neural_network_radio/) | 망 설계에 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 내재화 | 자율 최적화, 제로터치 네트워킹 |

- **📢 섹션 요약 비유**: RIS는 스마트 거울 벽이다. 건물 옆에 스마트 거울을 붙이면, 음영지역으로 가는 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 거울이 받아서 정확히 원하는 방향으로 반사해 준다. 별도 증폭기 없이 전파 길을 바꾼다.

---

## Ⅲ. 비교 및 연결

**NTN 위성 궤도 비교**

| 궤도 | 고도 | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 대표 사례 |
|:---:|:---:|:---:|:---:|
| [LEO](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/)(저궤도) | 200~2,000km | ~20ms | Starlink, OneWeb |
| [MEO](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/594_meo_medium_earth_orbit_gps/)(중궤도) | 2,000~35,786km | ~70ms | GPS, O3b |
| [GEO](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/593_geo_geostationary_earth_orbit_satellite/)(정지궤도) | 35,786km | ~600ms | 기존 위성방송 |
| [HAPS](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/596_haps_high_altitude_platform_station_drone/) | 20km (성층권) | ~1ms | SoftBank HAPSMobile |

<strong><a href="/knowledge-base/studynote/03_network/03_physical_layer_media/157_terahertz_thz_6g/">THz</a> 대역의 과제</strong>

- **대기 흡수(Molecular Absorption)**: 수증기·산소가 THz파 강하게 흡수 → 강우 시 급격한 감쇠.
- **높은 경로 손실**: 주파수가 높을수록 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 감쇠 급증 → 수십 m 셀 크기(Nano Cell) 필요.
- **소자 성숙도**: [THz](/knowledge-base/studynote/03_network/03_physical_layer_media/157_terahertz_thz_6g/) [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·처리 [반도체](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/009_semiconductor/) 아직 연구 단계.

- **📢 섹션 요약 비유**: THz는 레이저 포인터다. 매우 강렬하고 빠르지만, 창문(수증기) 한 장만 있어도 막혀버린다. 그래서 RIS 거울 네트워크와 [HAPS](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/596_haps_high_altitude_platform_station_drone/) 중계기가 필요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/">6G</a> 응용 시나리오</strong>

| 시나리오 | [6G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/) 기술 | 요구 사항 |
|:---|:---:|:---|
| 홀로그램 통신 | [THz](/knowledge-base/studynote/03_network/03_physical_layer_media/157_terahertz_thz_6g/), [eMBB](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/)++ | Tbps, 초저지연 |
| 원해 선박 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) | [LEO](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/) NTN | 전 지구 커버리지 |
| 도심 음영 해소 | RIS | 수동 반사, 저비용 |
| 자율주행 [V2X](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/141_v2x_vehicle_to_everything_communication/) | [6G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/) [uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/)+ | 10μs, 고정밀 위치 |

**기술사 답안 핵심**

1. [6G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/) = [THz](/knowledge-base/studynote/03_network/03_physical_layer_media/157_terahertz_thz_6g/)(속도) + NTN(커버리지) + RIS(음영해소) + [AI-Native](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/792_ai_native_6g_neural_network_radio/)(자율화) 4축.
2. THz의 단거리 한계 → 밀집 기지국(Nano Cell) + RIS 보완.
3. NTN [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/): [LEO](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/) < [HAPS](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/596_haps_high_altitude_platform_station_drone/) < [MEO](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/594_meo_medium_earth_orbit_gps/) < [GEO](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/593_geo_geostationary_earth_orbit_satellite/) 순서 반드시 암기.
4. RIS vs 중계기([Repeater](/knowledge-base/studynote/03_network/03_physical_layer_media/151_repeater_baseband/)): RIS는 능동 증폭 없이 반사만 → 전력 소비 극소.

- **📢 섹션 요약 비유**: 6G의 4축은 슈퍼히어로 팀이다. [THz](/knowledge-base/studynote/03_network/03_physical_layer_media/157_terahertz_thz_6g/)(속도 담당), NTN(범위 담당), RIS(장애물 제거), [AI-Native](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/792_ai_native_6g_neural_network_radio/)(두뇌·[전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 담당). 혼자론 한계가 있지만 함께라면 전 지구를 커버한다.

---

## Ⅴ. 기대효과 및 결론

6G는 2030년대 상용화를 목표로 전 세계 주요국(한국·미국·EU·중국·일본)이 R&D를 경쟁적으로 추진 중이다. [THz](/knowledge-base/studynote/03_network/03_physical_layer_media/157_terahertz_thz_6g/)·NTN·RIS의 유기적 결합과 [AI-Native](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/792_ai_native_6g_neural_network_radio/) 망 설계가 [6G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/) 비전을 실현하는 핵심이다. 기술사 시험에서는 5G와의 차별점, 각 기술의 역할과 한계를 명확히 정리해야 한다.

- **📢 섹션 요약 비유**: [6G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/) 비전은 전 지구가 하나의 와이파이 존이 되는 것이다. 위성(NTN)이 지붕이 되고, 스마트 반사벽(RIS)이 구석을 채우며, THz가 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 코어를 담당한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [THz](/knowledge-base/studynote/03_network/03_physical_layer_media/157_terahertz_thz_6g/)(Terahertz) | 100GHz~10THz · [6G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/) 고주파 대역, Tbps 가능 |
| NTN | [LEO](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/)/[HAPS](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/596_haps_high_altitude_platform_station_drone/)/[GEO](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/593_geo_geostationary_earth_orbit_satellite/) · [비지상 네트워크](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/154_ntn_non_terrestrial_network_6g/) 전 지구 커버리지 |
| RIS | 메타물질, 반사 제어 · 프로그래머블 전파 반사 표면 |
| [AI-Native](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/792_ai_native_6g_neural_network_radio/) | 제로터치, 자율 최적화 · 망 설계에 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 내재화 |
| [HAPS](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/596_haps_high_altitude_platform_station_drone/) | 성층권, 20km · 고고도 플랫폼 통신 중계 |

### 📈 관련 키워드 및 발전 흐름도

```text
[100GHz~10THz · 6G 고주파 대역] → [6G 테라헤르츠 · NTN] → [성층권 · 20km]
```

### 👶 어린이를 위한 3줄 비유 설명

1. THz는 엄청 빠른 빛 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)예요. 너무 빠른 대신 비 오면 막히고 멀리 못 가는 단점이 있어요.
2. NTN 위성은 우주에서 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 뿌리는 것이에요. 바다 한가운데나 깊은 산속도 커버할 수 있어요.
3. RIS는 스마트 거울 벽이에요. [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)가 건물에 막혀도 거울이 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 받아서 내 스마트폰 방향으로 튕겨줘요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 496 / 552

← **이전**: [495. 5G 3대 특성과 네트워크 슬라이싱 (5G eMBB uRLLC mMTC Network Slicing)](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/495_5g_embb_urllc_mmtc_network_slicing/)
**다음**: [497. O-RAN 오픈 무선 접속 네트워크 (O-RAN Open Radio Access Network)](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/497_oran_open_radio_access_network/) →

---
