---
title: "155. Channel Capacity"
date: "2026-04-21"
tags:
  - "studynote-algorithm-stats"
weight: 155
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 채널 용량 C는 *오류 없는 정보 전송의 이론적 최댓값* — 이를 넘으면 임의로 낮은 오류율 달성이 불가능하다.
> 2. **가치**: 섀넌-하틀리 ([Shannon-Hartley](/studynote/03_network/19_frequent_topics_terms/941_shannon_hartley_theorem_channel_capacity_snr/)) 정리 C = B·log₂(1+S/N)은 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/), Wi-Fi, [위성 통신](/studynote/03_network/11_wireless_mobile_communication/592_satellite_communication_characteristics/) [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 설계의 수학적 기반이다.
> 3. **판단 포인트**: 채널 용량을 높이는 방법은 두 가지뿐 — [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) B 증가 OR [신호 대 잡음비](/studynote/03_network/01_data_communication/024_신호_대_잡음비/) ([SNR](/studynote/03_network/01_data_communication/024_신호_대_잡음비/), [Signal-to-Noise Ratio](/studynote/03_network/01_data_communication/024_신호_대_잡음비/)) 향상. MIMO는 [공간 다중화](/studynote/03_network/02_multiplexing_multiple_access/100_공간_다중화_Spatial_Multiplexing/)로 유효 용량을 배가한다.

---

## Ⅰ. 개요 및 필요성

**채널 용량 (Channel Capacity)** C는 주어진 채널에서 달성 가능한 최대 상호 정보량이다:

```
C = max_{P(X)} I(X;Y)   [bits/channel use]
```

섀넌의 <strong><a href="/studynote/08_algorithm_stats/09_info_theory/157_channel_coding/">채널 부호화 정리</a> (Noisy <a href="/studynote/08_algorithm_stats/09_info_theory/157_channel_coding/">Channel Coding Theorem</a>)</strong>:
- R < C이면: 임의로 작은 오류율 달성 가능 (부호 블록이 길면)
- R > C이면: 오류율이 0으로 수렴 불가 (불가능)

여기서 R은 <strong>코드율 (<a href="/studynote/02_operating_system/02_process_thread/082_process_memory_structure/">Code</a> Rate)</strong> [bits/channel use].

### AWGN 채널의 섀넌-하틀리 정리

**AWGN (Additive White Gaussian Noise, 가산 백색 가우시안 잡음)** 채널:

```
C = B · log₂(1 + S/N)   [bits/s]
```

- B: [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) ([Bandwidth](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)) [Hz]
- S: [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 전력 ([Signal](/studynote/02_operating_system/02_process_thread/130_signal/) [Power](/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/))
- N: 잡음 전력 (Noise [Power](/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/))
- S/N: [신호 대 잡음비](/studynote/03_network/01_data_communication/024_신호_대_잡음비/) ([SNR](/studynote/03_network/01_data_communication/024_신호_대_잡음비/), [Signal-to-Noise Ratio](/studynote/03_network/01_data_communication/024_신호_대_잡음비/))

📢 **섹션 요약 비유**: 채널 용량은 "고속도로의 최대 처리 차량 수"다 — 차선 수([대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/))와 도로 상태(S/N비)가 동시에 결정하며, 이를 초과해 달리면 교통 체증(오류)이 반드시 발생한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 채널 모델 다이어그램

```
       신호 X                   수신 신호 Y
   +----------+   +잡음 N(0,σ^)   +----------+
   |  송신기   |-----------------►|  수신기   |
   +----------+                   +----------+
         |                              |
    P(X) 최적화                   I(X;Y) 계산
    -------------------------------------
    C = max I(X;Y)
```

### 주요 채널 모델 비교

| 채널 | 정의 | 용량 공식 |
|:---|:---|:---|
| AWGN | 가우시안 잡음 가산 | C = B·log₂(1+S/N) |
| [BSC](/studynote/12_it_management/01_governance_strategy/019_bsc/) (이진 대칭) | 오류 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) p로 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 반전 | C = 1 - H(p) |
| [BEC](/studynote/09_security/15_malware_attack_vectors/755_bec/) (이진 소거) | [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) ε로 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 소거 | C = 1 - ε |

<strong><a href="/studynote/12_it_management/01_governance_strategy/019_bsc/">BSC</a> (Binary Symmetric Channel, 이진 대칭 채널)</strong>:

```
  0 ----(1-p)--► 0
    ╲-----p----► 1

  1 ----(1-p)--► 1
    ╲-----p----► 0

C_BSC = 1 - H_b(p)   여기서 H_b(p) = -p·log₂p - (1-p)·log₂(1-p)
```

<strong><a href="/studynote/09_security/15_malware_attack_vectors/755_bec/">BEC</a> (Binary Erasure Channel, 이진 소거 채널)</strong>:

```
  0 --(1-ε)--► 0
    ╲--(ε)---► ? (소거)

  1 --(1-ε)--► 1
    ╲--(ε)---► ? (소거)

C_BEC = 1 - ε
```

BEC는 [LDPC](/studynote/03_network/04_data_link_layer_error/203_ldpc_low_density_parity_check/), [폴라 코드](/studynote/03_network/04_data_link_layer_error/204_polar_code_5g_control_channel/) 설계에 핵심 채널 모델.

### [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) vs SNR의 트레이드오프

```
용량 C [bits/s]
   ^
   |        - - - - -   (SNR ^)
   |      - - - - -
   |    - - - - -         B 증가: 선형 이득
   |  - - - -
   +--------------------► 대역폭 B [Hz]

SNR 증가: 로그 이득 (수확 체감)
```

- B를 2배로 -> C도 약 2배 (선형 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/))
- SNR을 2배로 -> C는 1 [bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) 증가 ([로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/))

실무적 시사점: 고SNR 환경에서는 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 확장이 더 효율적.

📢 **섹션 요약 비유**: [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) vs SNR의 트레이드오프는 "주방 넓히기 vs 요리사 실력 높이기"다 — 주방([대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/))을 넓히면 정비례로 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)이 늘지만, 요리사([SNR](/studynote/03_network/01_data_communication/024_신호_대_잡음비/))를 키우면 수확 체감([로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))으로만 늘어난다.

---

## Ⅲ. 비교 및 연결

### [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/)/Wi-Fi 6에서의 섀넌 한계 접근

| 기술 | 최대 변조 방식 | 이론 효율 [bits/s/Hz] |
|:---|:---|:---|
| [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) | 256-QAM | 8 |
| [5G NR](/studynote/03_network/15_nextgen_communication_architecture/763_5g_nr_new_radio_scalable_numerology/) Sub-6GHz | 256-QAM + [Massive MIMO](/studynote/03_network/02_multiplexing_multiple_access/099_Massive_MIMO_대규모_다중_안테나/) | ~30 |
| [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [mmWave](/studynote/03_network/03_physical_layer_media/156_mmwave_millimeter_wave/) | 256-QAM + [Beamforming](/studynote/03_network/02_multiplexing_multiple_access/101_beamforming/) | ~100+ |
| 이론 한계 (섀넌) | SNR에 의존 | B·log₂(1+[SNR](/studynote/03_network/01_data_communication/024_신호_대_잡음비/))/B |

### MIMO와 채널 용량

<strong><a href="/studynote/03_network/02_multiplexing_multiple_access/097_MIMO_다중_안테나_기술/">MIMO</a> (<a href="/studynote/03_network/02_multiplexing_multiple_access/097_MIMO_다중_안테나_기술/">Multiple-Input Multiple-Output</a>)</strong> 에서 N_T 송신, N_R 수신 [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/):

```
C_MIMO = Σᵢ log₂(1 + λᵢ·P/(N_T·σ^))
```

여기서 λᵢ는 채널 행렬 H의 특이값 (Singular Values). [공간 다중화](/studynote/03_network/02_multiplexing_multiple_access/100_공간_다중화_Spatial_Multiplexing/)로 용량을 min(N_T, N_R)배 확장 가능.

📢 **섹션 요약 비유**: MIMO는 "여러 차선 동시 활용"이다 — [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/)마다 독립된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스트림을 보내는 것이 여러 차선을 동시에 사용하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 네트워크 설계 시나리오

목표: 1km^ 셀에서 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) Gbps 총 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)

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
| 채널 용량을 두 배로 늘리는 가장 효율적인 방법은? | [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) B를 2배 확장 (선형 이득) |
| SNR이 이미 높으면 어떤 방법이 비효율적? | [SNR](/studynote/03_network/01_data_communication/024_신호_대_잡음비/) 추가 증가 ([로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 이득, 수확 체감) |
| MIMO가 채널 용량을 늘리는 원리는? | [공간 다중화](/studynote/03_network/02_multiplexing_multiple_access/100_공간_다중화_Spatial_Multiplexing/) (독립 채널 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)) |

📢 **섹션 요약 비유**: [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)은 "도로 차선 수", SNR은 "도로 품질"이다 — 차선이 많을수록 비례해서 차가 더 지나가고, 도로 품질 개선은 처음에 효과가 크지만 갈수록 효과가 줄어든다(수확 체감).

---

## Ⅴ. 기대효과 및 결론

채널 용량 이론은 <strong>현대 무선 통신 설계의 이론적 상한</strong>이다. [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/), [Wi-Fi 6E](/studynote/06_ict_convergence/02_iot_mobility/158_wifi_6e/), [위성 통신](/studynote/03_network/11_wireless_mobile_communication/592_satellite_communication_characteristics/) 모두 섀넌 한계를 얼마나 가깝게 달성하는지를 기준으로 평가된다.

섀넌 한계에 근접한 코드:
1. [터보 코드](/studynote/03_network/04_data_link_layer_error/202_turbo_code_shannon_limit/) (1993, Berrou et al.)
2. [LDPC](/studynote/03_network/04_data_link_layer_error/203_ldpc_low_density_parity_check/) (Low-Density Parity-Check, Gallager 1960, 2000년대 재발견)
3. [폴라 코드](/studynote/03_network/04_data_link_layer_error/204_polar_code_5g_control_channel/) (Arıkan, 2009) — [5G NR](/studynote/03_network/15_nextgen_communication_architecture/763_5g_nr_new_radio_scalable_numerology/) 제어 채널 채택

**물리 계층 설계의 목표**: 주어진 B와 SNR에서 C에 최대한 근접하는 부호화/변조 체계 선택.

📢 **섹션 요약 비유**: [폴라 코드](/studynote/03_network/04_data_link_layer_error/204_polar_code_5g_control_channel/)가 섀넌 한계에 가장 가깝다는 것은 "고속도로 용량의 99.9%를 실제로 사용하는 정밀 교통 시스템"을 드디어 만들어 낸 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 수식 | 연결 |
|:---|:---|:---|
| 채널 용량 C | max I(X;Y) | 섀넌 부호화 정리 |
| 섀넌-하틀리 | B·log₂(1+S/N) | AWGN 채널 용량 |
| [BSC](/studynote/12_it_management/01_governance_strategy/019_bsc/) 용량 | 1 - H_b(p) | 이진 대칭 채널 |
| [BEC](/studynote/09_security/15_malware_attack_vectors/755_bec/) 용량 | 1 - ε | [LDPC](/studynote/03_network/04_data_link_layer_error/203_ldpc_low_density_parity_check/)/[폴라 코드](/studynote/03_network/04_data_link_layer_error/204_polar_code_5g_control_channel/) 분석 |
| [MIMO](/studynote/03_network/02_multiplexing_multiple_access/097_MIMO_다중_안테나_기술/) 용량 | Σ log₂(1+λᵢP/...) | 다중 [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 확장 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[신호대잡음비 (SNR, Signal-to-Noise Ratio)]
    |
    v
[섀넌 용량 (Shannon Capacity)]
    |
    v
[채널 부호화 (Channel Coding)]
    |
    v
[오류 정정 (Error Correction)]
```

이 흐름도는 잡음 환경에서 섀넌 용량과 채널 부호화, 오류 정정으로 발전하는 흐름을 보여준다.
### 👶 어린이를 위한 3줄 비유 설명

1. **채널 용량은 "도로 통행 한계"**: 아무리 운전을 잘해도 도로 용량 이상의 차는 보낼 수 없다.
2. <strong><a href="/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">대역폭</a>은 차선 수, SNR은 도로 포장 품질</strong>: 차선이 많고 도로가 좋을수록 더 많은 차(정보)가 달린다.
3. **MIMO는 "평행 도로 추가"**: [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/)마다 새 도로를 하나씩 만들어 동시에 이용한다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 155 / 175

<- **이전**: [5. 크로스 엔트로피 (Cross-Entropy) — 분류 손실 함수](/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/)
**다음**: [7. 소스 부호화 정리 (Source Coding Theorem) — 엔트로피 한계](/studynote/08_algorithm_stats/09_info_theory/156_source_coding/) ->

---
