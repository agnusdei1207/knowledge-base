---
title: 142. WAVE/DSRC - 자율주행 전용 단거리 통신 규격
date: '2026-04-19'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[590_wave_ieee_802_11p_dsrc_v2x|WAVE]](Wireless Access in Vehicular Environments)/[[1025_c_v2x_wave_dsrc|DSRC]](Dedicated Short-Range Communications)는 **5.9GHz 전용 주파수에서 차량 간 [[120_direct_communication|직접 통신]](V2V·V2I)**을 제공하는 IEEE 802.11p 기반 규격이다.
> 2. **가치**: 셀룰러(4G/[[418_5g_embb_urllc_mmtc_slicing|5G]])는 기지국 경유로 **수십ms [[015_지연_데이터_관점|지연]]**이 있지만, DSRC는 **[[120_direct_communication|직접 통신]]으로 수ms 이내 저지연**을 제공하여 긴급 제동 경고 등 안전 메시지에 적합하다.
> 3. **판단 포인트**: FCC가 5.9GHz 대역 일부를 Wi-Fi에 재배정(2020)하면서 DSRC의 미래가 불투명해졌고, **[[143_c_v2x_cellular_based_communication|C-V2X]]([[763_5g_nr_new_radio_scalable_numerology|5G NR]])가 주류로 전환** 중이다.

---

## Ⅰ. 개요 및 필요성

```text
DSRC: 5.9GHz 전용 대역, 802.11p
  통신 범위: ~300m (직접)
  지연: <10ms (안전 메시지)
  vs C-V2X: 5G NR, 기지국+직접, 대역 효율↑
```

- **📢 섹션 요약 비유**: DSRC는 **워키토키([[120_direct_communication|직접 통신]])**, C-V2X는 **스마트폰(기지국+직접)**이다.

---

## Ⅱ~Ⅴ. 결론

DSRC는 **[[141_v2x_vehicle_to_everything_communication|V2X]] 통신의 [[459_quic_fec_forward_error_correction|초기]] 표준**이지만, [[143_c_v2x_cellular_based_communication|C-V2X]]([[763_5g_nr_new_radio_scalable_numerology|5G NR]])로 주류 전환이 [[216_progress_in_synchronization|진행]] 중이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[1025_c_v2x_wave_dsrc|DSRC]]** | 802.11p 전용 통신 |
| **[[590_wave_ieee_802_11p_dsrc_v2x|WAVE]]** | 차량 무선 접근 |
| **[[143_c_v2x_cellular_based_communication|C-V2X]]** | 셀룰러 기반 대안 |
| **5.9GHz** | 전용 주파수 |
| **저지연** | 안전 메시지 핵심 |

### 📈 관련 키워드 및 발전 흐름도

```text
[DSRC 802.11p (2010)] → [WAVE 표준 (IEEE 1609)]
    → [FCC 5.9GHz 재배정 (2020)]
    → [C-V2X 부상 (2020~)]
    → [현재: C-V2X 주류 — DSRC 축소]
```

### 👶 어린이를 위한 3줄 비유 설명
1. DSRC는 **워키토키**예요. 가까운 차끼리 **직접 대화**해요.
2. 스마트폰([[143_c_v2x_cellular_based_communication|C-V2X]])처럼 **기지국 없이도** 바로 통신해요.
3. 하지만 요즘은 **스마트폰 방식([[143_c_v2x_cellular_based_communication|C-V2X]])**이 더 인기가 많아요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 142 / 552

← **이전**: [[141_v2x_vehicle_to_everything_communication|141. V2X (Vehicle-to-Everything) 통신 - 차량-인프라 연결]]
**다음**: [[143_c_v2x_cellular_based_communication|143. C-V2X (Cellular V2X) - 5G 셀룰러 기반 차량 통신]] →

---
