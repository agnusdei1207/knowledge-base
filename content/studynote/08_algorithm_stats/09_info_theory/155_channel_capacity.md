---
title: 6. 채널 용량 (Channel Capacity) — 샤논 용량 공식
date: '2026-04-21'
tags:
- studynote-algorithm
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 채널 용량 C는 *오류 없는 정보 전송의 이론적 최댓값* — 이를 넘으면 임의로 낮은 오류율 달성이 불가능하다.
> 2. **가치**: 섀넌-하틀리 ([[941_shannon_hartley_theorem_channel_capacity_snr|Shannon-Hartley]]) 정리 C = B·log₂(1+S/N)은 [[418_5g_embb_urllc_mmtc_slicing|5G]], Wi-Fi, [[592_satellite_communication_characteristics|위성 통신]] [[140_bandwidth|대역폭]] 설계의 수학적 기반이다.
> 3. **판단 포인트**: 채널 용량을 높이는 방법은 두 가지뿐 — [[140_bandwidth|대역폭]] B 증가 OR [[024_신호_대_잡음비|신호 대 잡음비]] ([[024_신호_대_잡음비|SNR]], [[024_신호_대_잡음비|Signal-to-Noise Ratio]]) 향상. MIMO는 [[100_공간_다중화_Spatial_Multiplexing|공간 다중화]]로 유효 용량을 배가한다.

---

## Ⅰ. 개요 및 필요성

**채널 용량 (Channel Capacity)** C는 주어진 채널에서 달성 가능한 최대 상호 정보량이다:

```
C = max_{P(X)} I(X;Y)   [bits/channel use]
```

섀넌의 **[[157_channel_coding|채널 부호화 정리]] (Noisy [[157_channel_coding|Channel Coding Theorem]])**:
- R < C이면: 임의로 작은 오류율 달성 가능 (부호 블록이 길면)
- R > C이면: 오류율이 0으로 수렴 불가 (불가능)

여기서 R은 **코드율 ([[082_process_memory_structure|Code]] Rate)** [bits/channel use].

### AWGN 채널의 섀넌-하틀리 정리

**AWGN (Additive White Gaussian Noise, 가산 백색 가우시안 잡음)** 채널:

```
C = B · log₂(1 + S/N)   [bits/s]
```

- B: [[140_bandwidth|대역폭]] ([[140_bandwidth|Bandwidth]]) [Hz]
- S: [[130_signal|신호]] 전력 ([[130_signal|Signal]] [[069_type_1_2_error_statistical_power|Power]])
- N: 잡음 전력 (Noise [[069_type_1_2_error_statistical_power|Power]])
- S/N: [[024_신호_대_잡음비|신호 대 잡음비]] ([[024_신호_대_잡음비|SNR]], [[024_신호_대_잡음비|Signal-to-Noise Ratio]])

📢 **섹션 요약 비유**: 채널 용량은 "고속도로의 최대 처리 차량 수"다 — 차선 수([[140_bandwidth|대역폭]])와 도로 상태(S/N비)가 동시에 결정하며, 이를 초과해 달리면 교통 체증(오류)이 반드시 발생한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 채널 모델 다이어그램

```
       신호 X                   수신 신호 Y
   ┌──────────┐   +잡음 N(0,σ²)   ┌──────────┐
   │  송신기   │─────────────────►│  수신기   │
   └──────────┘                   └──────────┘
         │                              │
    P(X) 최적화                   I(X;Y) 계산
    ─────────────────────────────────────
    C = max I(X;Y)
```

### 주요 채널 모델 비교

| 채널 | 정의 | 용량 공식 |
|:---|:---|:---|
| AWGN | 가우시안 잡음 가산 | C = B·log₂(1+S/N) |
| [[019_bsc|BSC]] (이진 대칭) | 오류 [[130_probability|확률]] p로 [[073_bit|비트]] 반전 | C = 1 - H(p) |
| [[755_bec|BEC]] (이진 소거) | [[130_probability|확률]] ε로 [[073_bit|비트]] 소거 | C = 1 - ε |

**[[019_bsc|BSC]] (Binary Symmetric Channel, 이진 대칭 채널)**:

```
  0 ────(1-p)──► 0
    ╲─────p────► 1

  1 ────(1-p)──► 1
    ╲─────p────► 0

C_BSC = 1 - H_b(p)   여기서 H_b(p) = -p·log₂p - (1-p)·log₂(1-p)
```

**[[755_bec|BEC]] (Binary Erasure Channel, 이진 소거 채널)**:

```
  0 ──(1-ε)──► 0
    ╲──(ε)───► ? (소거)

  1 ──(1-ε)──► 1
    ╲──(ε)───► ? (소거)

C_BEC = 1 - ε
```

BEC는 [[203_ldpc_low_density_parity_check|LDPC]], [[204_polar_code_5g_control_channel|폴라 코드]] 설계에 핵심 채널 모델.

### [[140_bandwidth|대역폭]] vs SNR의 트레이드오프

```
용량 C [bits/s]
   ▲
   │        ─ ─ ─ ─ ─   (SNR ↑)
   │      ─ ─ ─ ─ ─
   │    ─ ─ ─ ─ ─         B 증가: 선형 이득
   │  ─ ─ ─ ─
   └────────────────────► 대역폭 B [Hz]

SNR 증가: 로그 이득 (수확 체감)
```

- B를 2배로 → C도 약 2배 (선형 [[083_relationship_in_er_model|관계]])
- SNR을 2배로 → C는 1 [[086_fenwick_tree|bit]] 증가 ([[568_logs_distributed_logging_elk_fluentd|로그]] [[083_relationship_in_er_model|관계]])

실무적 시사점: 고SNR 환경에서는 [[140_bandwidth|대역폭]] 확장이 더 효율적.

📢 **섹션 요약 비유**: [[140_bandwidth|대역폭]] vs SNR의 트레이드오프는 "주방 넓히기 vs 요리사 실력 높이기"다 — 주방([[140_bandwidth|대역폭]])을 넓히면 정비례로 [[139_throughput|처리량]]이 늘지만, 요리사([[024_신호_대_잡음비|SNR]])를 키우면 수확 체감([[568_logs_distributed_logging_elk_fluentd|로그]])으로만 늘어난다.

---

## Ⅲ. 비교 및 연결

### [[418_5g_embb_urllc_mmtc_slicing|5G]]/Wi-Fi 6에서의 섀넌 한계 접근

| 기술 | 최대 변조 방식 | 이론 효율 [bits/s/Hz] |
|:---|:---|:---|
| [[752_lte_long_term_evolution_4g|LTE]] | 256-QAM | 8 |
| [[763_5g_nr_new_radio_scalable_numerology|5G NR]] Sub-6GHz | 256-QAM + [[099_Massive_MIMO_대규모_다중_안테나|Massive MIMO]] | ~30 |
| [[418_5g_embb_urllc_mmtc_slicing|5G]] [[156_mmwave_millimeter_wave|mmWave]] | 256-QAM + [[101_beamforming|Beamforming]] | ~100+ |
| 이론 한계 (섀넌) | SNR에 의존 | B·log₂(1+[[024_신호_대_잡음비|SNR]])/B |

### MIMO와 채널 용량

**[[097_MIMO_다중_안테나_기술|MIMO]] ([[097_MIMO_다중_안테나_기술|Multiple-Input Multiple-Output]])** 에서 N_T 송신, N_R 수신 [[171_antenna_basic_dipole_resonance|안테나]]:

```
C_MIMO = Σᵢ log₂(1 + λᵢ·P/(N_T·σ²))
```

여기서 λᵢ는 채널 행렬 H의 특이값 (Singular Values). [[100_공간_다중화_Spatial_Multiplexing|공간 다중화]]로 용량을 min(N_T, N_R)배 확장 가능.

📢 **섹션 요약 비유**: MIMO는 "여러 차선 동시 활용"이다 — [[171_antenna_basic_dipole_resonance|안테나]]마다 독립된 [[001_dikw_pyramid|데이터]] 스트림을 보내는 것이 여러 차선을 동시에 사용하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[418_5g_embb_urllc_mmtc_slicing|5G]] 네트워크 설계 시나리오

목표: 1km² 셀에서 [[489_raid_10_hybrid|10]] Gbps 총 [[139_throughput|처리량]]

```
필요 조건:
  C ≥ 10 Gbps
  B · log₂(1 + S/N) ≥ 10×10⁹

100 MHz 대역폭, SNR = 30dB (S/N = 1000):
  C = 100×10⁶ · log₂(1001) ≈ 100×10⁶ · 9.97 ≈ 997 Mbps (단일 안테나)

Massive MIMO 32×32 = 최대 32개 스트림:
  C_total ≈ 32 × 997 ≈ 31.9 Gbps (이론적 상한)
```

### 기술사 판단 포인트

| 질문 | 답 |
|:---|:---|
| 채널 용량을 두 배로 늘리는 가장 효율적인 방법은? | [[140_bandwidth|대역폭]] B를 2배 확장 (선형 이득) |
| SNR이 이미 높으면 어떤 방법이 비효율적? | [[024_신호_대_잡음비|SNR]] 추가 증가 ([[568_logs_distributed_logging_elk_fluentd|로그]] 이득, 수확 체감) |
| MIMO가 채널 용량을 늘리는 원리는? | [[100_공간_다중화_Spatial_Multiplexing|공간 다중화]] (독립 채널 [[087_process_state_transition|생성]]) |

📢 **섹션 요약 비유**: [[140_bandwidth|대역폭]]은 "도로 차선 수", SNR은 "도로 품질"이다 — 차선이 많을수록 비례해서 차가 더 지나가고, 도로 품질 개선은 처음에 효과가 크지만 갈수록 효과가 줄어든다(수확 체감).

---

## Ⅴ. 기대효과 및 결론

채널 용량 이론은 **현대 무선 통신 설계의 이론적 상한**이다. [[418_5g_embb_urllc_mmtc_slicing|5G]], [[158_wifi_6e|Wi-Fi 6E]], [[592_satellite_communication_characteristics|위성 통신]] 모두 섀넌 한계를 얼마나 가깝게 달성하는지를 기준으로 평가된다.

섀넌 한계에 근접한 코드:
1. [[202_turbo_code_shannon_limit|터보 코드]] (1993, Berrou et al.)
2. [[203_ldpc_low_density_parity_check|LDPC]] (Low-Density Parity-Check, Gallager 1960, 2000년대 재발견)
3. [[204_polar_code_5g_control_channel|폴라 코드]] (Arıkan, 2009) — [[763_5g_nr_new_radio_scalable_numerology|5G NR]] 제어 채널 채택

**물리 계층 설계의 목표**: 주어진 B와 SNR에서 C에 최대한 근접하는 부호화/변조 체계 선택.

📢 **섹션 요약 비유**: [[204_polar_code_5g_control_channel|폴라 코드]]가 섀넌 한계에 가장 가깝다는 것은 "고속도로 용량의 99.9%를 실제로 사용하는 정밀 교통 시스템"을 드디어 만들어 낸 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 수식 | 연결 |
|:---|:---|:---|
| 채널 용량 C | max I(X;Y) | 섀넌 부호화 정리 |
| 섀넌-하틀리 | B·log₂(1+S/N) | AWGN 채널 용량 |
| [[019_bsc|BSC]] 용량 | 1 - H_b(p) | 이진 대칭 채널 |
| [[755_bec|BEC]] 용량 | 1 - ε | [[203_ldpc_low_density_parity_check|LDPC]]/[[204_polar_code_5g_control_channel|폴라 코드]] 분석 |
| [[097_MIMO_다중_안테나_기술|MIMO]] 용량 | Σ log₂(1+λᵢP/...) | 다중 [[171_antenna_basic_dipole_resonance|안테나]] 확장 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[신호대잡음비 (SNR, Signal-to-Noise Ratio)]
    │
    ▼
[섀넌 용량 (Shannon Capacity)]
    │
    ▼
[채널 부호화 (Channel Coding)]
    │
    ▼
[오류 정정 (Error Correction)]
```

이 흐름도는 잡음 환경에서 섀넌 용량과 채널 부호화, 오류 정정으로 발전하는 흐름을 보여준다.
### 👶 어린이를 위한 3줄 비유 설명

1. **채널 용량은 "도로 통행 한계"**: 아무리 운전을 잘해도 도로 용량 이상의 차는 보낼 수 없다.
2. **[[140_bandwidth|대역폭]]은 차선 수, SNR은 도로 포장 품질**: 차선이 많고 도로가 좋을수록 더 많은 차(정보)가 달린다.
3. **MIMO는 "평행 도로 추가"**: [[171_antenna_basic_dipole_resonance|안테나]]마다 새 도로를 하나씩 만들어 동시에 이용한다.
