+++
title = "141. V2X (Vehicle-to-Everything) 통신 - 차량-인프라 연결"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: V2X는 <strong>차량이 다른 차량(V2V)·인프라(V2I)·보행자(V2P)·네트워크(V2N)와 통신</strong>하여 교통 안전·효율을 향상시키는 기술이며, [DSRC](/knowledge-base/studynote/03_network/12_iot_wpan_edge/1025_c_v2x_wave_dsrc/)(802.11p)와 [C-V2X](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/143_c_v2x_cellular_based_communication/)(셀룰러)가 대표 규격이다.
> 2. **가치**: 자율주행 센서(카메라·[LiDAR](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/140_lidar_light_detection_and_ranging_tof/))는 <strong>시야 범위 내</strong>만 감지하지만, V2X는 **교차로 너머·커브 뒤** 등 비가시(Non-Line-of-Sight) 정보를 제공하여 안전성을 획기적으로 향상시킨다.
> 3. **판단 포인트**: [DSRC](/knowledge-base/studynote/03_network/12_iot_wpan_edge/1025_c_v2x_wave_dsrc/)(전용 주파수, 저지연)→[C-V2X](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/143_c_v2x_cellular_based_communication/)([5G NR](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/763_5g_nr_new_radio_scalable_numerology/), 고대역)로 주류 전환 중이며, 인프라([RSU](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/913_v2i_rsu_road_side_unit_mec_autonomous_driving/)) 구축과 표준 통일이 핵심 과제이다.

---

## Ⅰ. 개요 및 필요성

```text
V2V: 차량↔차량 (급정거 알림, 합류 협조)
V2I: 차량↔인프라 (신호등·도로 정보)
V2P: 차량↔보행자 (횡단 경고)
V2N: 차량↔네트워크 (클라우드 교통 정보)
```

- **📢 섹션 요약 비유**: V2X는 차량의 <strong>무전기</strong>이다. 눈(센서)으로 못 보는 곳의 정보도 무전(통신)으로 받는다.

---

## Ⅱ~Ⅴ. 결론

V2X는 <strong>자율주행의 비가시 정보 보완 핵심</strong>이며, [C-V2X](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/143_c_v2x_cellular_based_communication/)([5G NR](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/763_5g_nr_new_radio_scalable_numerology/))가 차세대 표준으로 수렴 중이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **V2X** | 차량-모든 것 통신 |
| **V2V** | 차량 간 |
| **V2I** | 차량-인프라 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/143_c_v2x_cellular_based_communication/">C-V2X</a></strong> | [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 셀룰러 기반 |
| <strong><a href="/knowledge-base/studynote/03_network/12_iot_wpan_edge/1025_c_v2x_wave_dsrc/">DSRC</a></strong> | 전용 주파수 기반 |

### 📈 관련 키워드 및 발전 흐름도

```text
[DSRC (802.11p, 2010)] → [C-V2X (3GPP, 2017)]
    → [5G NR V2X (2020)] → [인프라(RSU) 구축]
    → [현재: 6G V2X — 초저지연·초신뢰]
```

### 👶 어린이를 위한 3줄 비유 설명
1. V2X는 차의 <strong>무전기</strong>예요. 다른 차·신호등과 <strong>대화</strong>해요.
2. 눈(센서)으로 못 보는 <strong>커브 뒤 사고</strong>도 무전으로 미리 알 수 있어요.
3. 차들이 서로 **"나 지금 급정거해!"** 알려주면 사고가 줄어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 141 / 552

← **이전**: [140. LiDAR (Light Detection and Ranging) - ToF 기반 3D 거리 측정](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/140_lidar_light_detection_and_ranging_tof/)
**다음**: [142. WAVE/DSRC - 자율주행 전용 단거리 통신 규격](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/142_wave_dsrc_autonomous_vehicle_communication/) →

---
