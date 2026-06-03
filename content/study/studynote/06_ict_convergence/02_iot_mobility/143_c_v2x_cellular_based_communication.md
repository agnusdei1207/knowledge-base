+++
weight = 143
title = "143. C-V2X (Cellular V2X) - 5G 셀룰러 기반 차량 통신"
date = "2026-04-19"
[extra]
categories = "studynote-ict-convergence"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: C-V2X는 **[[751_3gpp_3rd_generation_partnership_project|3GPP]] 표준 기반으로 셀룰러 네트워크(4G [[752_lte_long_term_evolution_4g|LTE]]/[[763_5g_nr_new_radio_scalable_numerology|5G NR]])를 활용**한 차량 통신 기술이며, Uu(기지국 경유)와 PC5(사이드링크, [[120_direct_communication|직접 통신]]) 두 가지 인터페이스를 제공한다.
> 2. **가치**: [[1025_c_v2x_wave_dsrc|DSRC]](802.11p) 대비 **넓은 커버리지·높은 대역·진화 경로(4G→[[418_5g_embb_urllc_mmtc_slicing|5G]]→[[419_6g_ntn_thz_ris_next_gen|6G]])**가 장점이며, 기존 셀룰러 인프라를 활용할 수 있어 배포 비용이 낮다.
> 3. **판단 포인트**: PC5(직접, 저지연)가 안전 메시지에, Uu(기지국, 넓은 범위)가 클라우드 교통 정보에 적합하며, [[763_5g_nr_new_radio_scalable_numerology|5G NR]] V2X가 현재 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
C-V2X 인터페이스:
  Uu: 차량 → 기지국 → 클라우드 (넓은 범위)
  PC5: 차량 ↔ 차량/인프라 (직접, 저지연)
5G NR V2X: URLLC (1ms 이하 지연)
```

- **📢 섹션 요약 비유**: C-V2X는 **스마트폰 + 워키토키 결합**이다. 스마트폰(Uu, 넓은 범위)과 워키토키(PC5, [[120_direct_communication|직접 통신]])를 동시에 가진다.

---

## Ⅱ~Ⅴ. 결론

C-V2X는 **[[141_v2x_vehicle_to_everything_communication|V2X]] 통신의 차세대 표준**이며, [[418_5g_embb_urllc_mmtc_slicing|5G]] NR의 URLLC로 초저지연 안전 통신을 실현한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **C-[[141_v2x_vehicle_to_everything_communication|V2X]]** | 셀룰러 기반 [[141_v2x_vehicle_to_everything_communication|V2X]] |
| **PC5** | 사이드링크 (직접) |
| **Uu** | 기지국 경유 |
| **[[763_5g_nr_new_radio_scalable_numerology|5G NR]] [[141_v2x_vehicle_to_everything_communication|V2X]]** | 차세대 표준 |
| **[[1025_c_v2x_wave_dsrc|DSRC]]** | 대안 (802.11p) |

### 📈 관련 키워드 및 발전 흐름도

```text
[DSRC (2010)] → [LTE-V2X (3GPP R14, 2017)]
    → [5G NR V2X (R16, 2020)]
    → [현재: 6G V2X 연구 — 초저지연·AI 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. C-V2X는 **스마트폰+워키토키**예요. 두 가지 방법으로 대화해요.
2. 스마트폰(Uu)은 **멀리 있는 서버**와, 워키토키(PC5)는 **가까운 차**와 대화해요.
3. [[418_5g_embb_urllc_mmtc_slicing|5G]] 덕분에 **0.001초 만에** 위험 알림을 보낼 수 있어요!
