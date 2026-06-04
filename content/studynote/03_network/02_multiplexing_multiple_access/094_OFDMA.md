+++
title = "94. OFDMA (Orthogonal Frequency Division Multiple Access) - LTE, 5G"
description = "4G LTE와 5G 시스템의 핵심 다중 접속 기술인 OFDMA의 구조, 직교 부반송파 할당 원리 및 기존 기술과의 비교 분석"
date = 2026-03-31

[taxonomies]
tags = ["network"]

[extra]
tags = ["network"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [OFDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/) (Orthogonal Frequency [Division](/knowledge-base/studynote/05_database/07_exam_summary/411_division_operation/) [Multiple Access](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/))는 전체 주파수 대역을 서로 수학적으로 직교(Orthogonal)하는 수백~수천 개의 좁은 [부반송파](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/)([Subcarrier](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/))로 쪼갠 뒤, 시간과 주파수 단위의 2차원 블록으로 다수 사용자에게 동적 할당하는 [다중 접속](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 방식이다.
> 2. **가치**: [직교성](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/) 덕분에 [부반송파](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/) 간의 간섭(ICI)이 없고 [보호 대역](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/074_보호_대역_Guard_Band/)([Guard Band](/knowledge-base/studynote/03_network/19_frequent_topics_terms/946_guard_band_fdm_adjacent_channel_interference/))이 불필요하여 주파수 효율이 극대화되며, [CDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/957_cdma_code_division_multiple_access_dsss_orthogonality/) 시대의 고질적 한계였던 [셀 호흡](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/093_셀_호흡_현상/) 현상과 근거리-원거리 문제를 구조적으로 회피했다.
> 3. **판단 포인트**: 높은 피크 전력(PAPR) 문제가 있어 단말기의 배터리 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)가 필수적인 업링크(Uplink)에서는 SC-[FDMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/088_주파수_분할_다중접속_FDMA/) (Single Carrier [FDMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/088_주파수_분할_다중접속_FDMA/))를 혼용하며, 5G에서는 도플러 천이 방어를 위해 [부반송파](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/) 간격을 유연하게 조절하는 Flexible Numerology를 선택 적용한다.

---

## Ⅰ. 개요 및 필요성

OFDMA는 4G [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 및 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 모바일 네트워크에서 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다루기 위해 채택된 직교 주파수 분할 기반의 다중 사용자 접속 기술이다.

스마트폰 도입 이후 무선 인터넷 요구량이 폭증하면서, 기존 3G의 대세였던 [CDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/957_cdma_code_division_multiple_access_dsss_orthogonality/) ([Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) [Division](/knowledge-base/studynote/05_database/07_exam_summary/411_division_operation/) [Multiple Access](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/)) 기술은 거대한 한계에 부딪혔다. 모든 사용자가 같은 주파수 대역을 쓰면서 코드로만 구별하다 보니 사용자가 늘어날수록 서로가 서로에게 심각한 잡음(간섭)으로 작용했고, 속도 향상을 위한 시스템 복잡도가 감당 불가 수준으로 치솟았다.

이를 해결하기 위해 등장한 OFDMA는 넓은 주파수 대역을 아주 좁은 '[부반송파](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/)' 수백 개로 잘게 쪼개어, 각 단말기가 서로 겹치지 않는 별도의 공간을 배타적으로 사용하도록 통제한다. 이 잘게 쪼개진 자원 격자(Grid)를 기지국이 1ms 단위로 최적의 주파수를 찾아 할당하면서 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 브로드밴드 시대가 열리게 되었다.

- **📢 섹션 요약 비유**: CDMA가 넓은 체육관에 여러 명을 몰아넣고 각자 다른 언어로 동시에 떠들게 하여 결국 시끄러워지는 방식이라면, OFDMA는 체육관에 수백 개의 작은 칸막이를 치고 시간표에 따라 내 칸과 내 시간에만 들어가 조용히 공부하는 완벽히 통제된 독서실과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

OFDMA의 아키텍처는 PRB (Physical Resource Block)라는 2차원 격자 블록과 [직교성](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/)([Orthogonality](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/))에 기반한다.

일반적인 [주파수 분할 방식](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/552_fdd_vs_tdd_wireless_duplexing/)(FDM)은 주파수 간 간섭을 막으려 낭비되는 빈 공간인 [보호 대역](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/074_보호_대역_Guard_Band/)을 둔다. 하지만 OFDMA는 한 [부반송파](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/)의 정점(Peak)이 올 때 양옆 [부반송파](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/)의 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 세기가 정확히 0이 되도록 간격을 수학적으로 설계하여, 촘촘히 겹쳐도 간섭이 없는 '[직교성](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/)'을 확보했다.

기지국이 단말에게 자원을 나눠주는 가장 작은 티켓인 PRB (Physical Resource Block)는 12개의 [부반송파](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/)와 7개의 심볼(1 Slot, 0.5ms)로 이루어져 있다. 이를 통해 기지국은 각 단말이 겪는 주파수 [페이딩](/knowledge-base/studynote/03_network/03_physical_layer_media/167_fading_large_scale_small_scale/)([Fading](/knowledge-base/studynote/03_network/03_physical_layer_media/167_fading_large_scale_small_scale/)) 환경을 1ms마다 파악하여 가장 전파가 깨끗한 [부반송파](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/) 타일만 골라주는 주파수 선택적 스케줄링 (Frequency Selective Scheduling)을 수행한다.

```text
+--------------------------------------------------------------+
|           LTE/5G OFDMA Resource Grid (자원 격자) 아키텍처          |
+--------------------------------------------------------------+
| 주파수 (Freq)                                                 |
|   ^                                                          |
|   | +--+--+--+--+--+--+--+ <- 1개 RE (Resource Element)         |
|   | +--+--+--+--+--+--+--+                                   |
| 12| +--+--+--+--+--+--+--+     이 전체 블록 (12개 부반송파 x 7개 심볼)|
| 개| +--+--+--+--+--+--+--+   -> 1개의 PRB (Physical Resource Block) |
| 부| +--+--+--+--+--+--+--+      (기지국 스케줄러의 최소 할당 단위)     |
| 반| +--+--+--+--+--+--+--+                                   |
| 송| +--+--+--+--+--+--+--+                                   |
| 파| +--+--+--+--+--+--+--+                                   |
|   +---------------------------► 시간 (Time)                |
|      <--- 1 Slot (7 Symbols) --->                            |
+--------------------------------------------------------------+
```

이 매트릭스 다이어그램처럼 수십 명의 사용자가 기지국으로부터 테트리스 블록 같은 수만 개의 자원을 실시간으로 조각내어 부여받아, 간섭 없이 자기 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 처리한다.

- **📢 섹션 요약 비유**: 큰 트럭 1대로 한 번에 무거운 짐을 옮기다 길이 막혀 낭패를 보는 대신, 짐을 1,000조각으로 나누어 1,000대의 오토바이에 싣고 안 막히는 골목길만 쏙쏙 골라서 한꺼번에 배달을 완료하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 배송 시스템이다.

---

## Ⅲ. 비교 및 연결

OFDMA는 탁월하지만 CDMA나 파생 기술과 극명한 트레이드오프를 갖는다.

| 항목 | [CDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/957_cdma_code_division_multiple_access_dsss_orthogonality/) (3G) | [OFDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/) (4G/[5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/)) |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/">다중 접속</a> 분리 기준</strong> | 코드 ([Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/)) | 주파수 타일과 시간 (Freq & Time Grid) |
| **셀 커버리지 특성** | 가입자가 몰리면 수축 ([셀 호흡](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/093_셀_호흡_현상/)) | 직교 할당으로 커버리지가 직관적이고 안정적 |
| **PAPR (최대 전력비)** | 상대적으로 낮음 | **매우 높음 (수천 개 파형 중첩 시 피크 전력 치솟음)** |
| **스케줄링 복잡도** | 단순 전력 제어 위주 | 1ms 단위 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 2차원 자원 할당으로 복잡도 최상 |

특히 OFDMA의 수많은 [부반송파](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/)가 우연히 같은 위상으로 겹쳐 [전압](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/)이 폭증하는 PAPR (Peak-to-Average [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Ratio) 문제는 치명적이다. 전원 플러그를 꽂는 기지국(다운링크)은 버티지만 배터리를 쓰는 단말기(업링크)는 증폭기 효율이 급감해 배터리가 터질 듯이 소모된다. 그래서 [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 업링크에서는 [OFDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/) 대신 PAPR을 대폭 낮춘 하이브리드 대안인 SC-[FDMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/088_주파수_분할_다중접속_FDMA/) (Single Carrier [FDMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/088_주파수_분할_다중접속_FDMA/))를 전략적으로 혼용하게 되었다.

- **📢 섹션 요약 비유**: 기지국(부자 식당)은 비싼 대형 오븐이 있어 화력이 요동치는 수백 가지 요리([OFDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/))를 한 번에 쳐내지만, 단말기(자취생)는 작은 가스버너뿐이라 불꽃이 튀면 위험하니 화력이 일정한 요리법(SC-[FDMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/088_주파수_분할_다중접속_FDMA/))을 강제로 써야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 통신 엔지니어는 환경에 맞춰 [OFDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/) 구조의 취약점을 제어해야 한다.

- **고속 이동체(KTX) 도플러 방어**: OFDMA의 생명은 '수학적 [직교성](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/)'이다. 시속 300km로 달리면 도플러 천이 (Doppler Shift) 효과로 수신 주파수가 어긋나고 [직교성](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/)이 붕괴하여 인접 채널을 침범한다. 이 현상을 막기 위해 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 엔지니어들은 [부반송파](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/) 간격을 기존 15kHz에서 30kHz나 60kHz로 물리적으로 벌려버리는 Flexible Numerology 기법을 적용하여 흔들림의 마진을 확보한다.
- **인접 셀 간섭 회피 (ICIC)**: 셀 안에서는 간섭이 없지만, 경계 구역에 가면 옆 기지국의 같은 주파수 블록과 정면 충돌한다. ICIC (Inter-Cell Interference Coordination)를 적용해 A 기지국은 외곽 단말에 상단 주파수만 주고, B 기지국은 하단 주파수만 할당하도록 기지국 간 상호 협력 스케줄링을 설정해야 치명적 속도 저하를 막을 수 있다.

- **📢 섹션 요약 비유**: 주차선([직교성](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/))을 촘촘히 그어놨는데, 고속 이동 환경(강풍) 때문에 차들이 흔들려 옆 차를 긁는다면, 엔지니어는 아예 주차선 자체를 평소보다 2~4배 넓게 그려 문콕 사고의 여지를 원천 차단하는 유연한 설계를 적용한다.

---

## Ⅴ. 기대효과 및 결론

OFDMA는 [보호 대역](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/074_보호_대역_Guard_Band/)의 낭비를 없애고 시간/주파수 자원을 파편화하여 1ms 단위 스케줄링을 구현함으로써 모바일 통신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리량을 수십 배 폭증시킨 1등 공신이다.

앞으로 6G를 향한 진화에서는 [OFDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/) 격자 공간의 한계를 넘기 위해 물리적 공간(Space) 축을 결합한 Massive MIMO와 시너지를 내거나, "[직교성](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/)"이라는 규칙을 의도적으로 깨고 남는 전력 마진에 다른 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 중첩시켜 하나의 격자에 여러 명을 구겨 넣는 [NOMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/095_NOMA_비직교_다중_접속/) ([Non-Orthogonal Multiple Access](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/095_NOMA_비직교_다중_접속/)) 기술과의 융합으로 발전할 것이다. OFDMA는 통신망의 가장 단단한 아파트 뼈대와 같다.

- **📢 섹션 요약 비유**: OFDMA는 공간을 최대한 정밀하게 쪼개어 만든 최종 진화형 통신 아파트다. 미래의 통신은 이 건물을 부수는 게 아니라, 한 방에 벙크 침대([NOMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/095_NOMA_비직교_다중_접속/))를 넣어 더 많은 사람을 재우는 방식으로 용량을 늘린다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>SC-<a href="/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/088_주파수_분할_다중접속_FDMA/">FDMA</a></strong> | 높은 피크 [전압](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/)(PAPR)으로 인한 단말기 배터리 방전을 해결하기 위해 [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 업링크에 도입된 싱글 캐리어 접속 방식 |
| **PRB (Physical Resource Block)** | [OFDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/) 환경에서 기지국 스케줄러가 단말에게 발급하는 시간-주파수 2차원 자원의 최소 할당 단위 블록 |
| <strong><a href="/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/">CP</a> (<a href="/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/">Cyclic Prefix</a>)</strong> | 다중 경로를 거치며 발생한 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) [에코](/knowledge-base/studynote/03_network/01_data_communication/031_에코_반향/) [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)가 다음 심볼을 덮쳐 침범하지 않도록 심볼 앞에 붙이는 잉여 복사본 버퍼 |
| **Flexible Numerology** | 5G에서 사용자 이동 속도에 따라 도플러 천이에 버티도록 [부반송파](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/) 간격(15, 30, 60kHz)을 유연하게 늘리거나 줄이는 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
CDMA 대역폭 포화 · 셀 호흡 등 한계 발생
    |
    v
OFDM (다중 반송파 분할 전송, 직교성 기반)
    |
    v
OFDMA (OFDM을 여러 사용자의 다중 접속으로 확장)
    |
    v
SC-FDMA (업링크 PAPR 극복) · ICIC (셀 경계 간섭 회피)
    |
    v
NOMA (비직교 다중 접속 융합) 및 5G Flexible Numerology 확장
```

이 흐름도는 코드로 구분하던 3G 시대를 끝내고, 수학적 [직교성](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/)으로 주파수와 시간을 완벽히 조각내는 현재의 아키텍처로 진화한 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 옛날 통신은 큰 운동장에서 수십 명이 섞여서 동시에 대화하니까 조금만 늘어나도 너무 시끄러웠어요 ([CDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/957_cdma_code_division_multiple_access_dsss_orthogonality/)).
2. <strong><a href="/knowledge-base/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/">OFDMA</a></strong>는 이 운동장에 수천 개의 좁고 투명한 방음 칸막이([부반송파](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/))를 치고, 기지국 선생님이 "넌 1번 칸, 넌 2번 칸!" 하고 정확히 시간을 정해 자리를 나눠주는 방식이에요.
3. 벽이 아주 튼튼해서 옆 사람 소리가 안 들리기 때문에([직교성](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/)), 스마트폰으로 영화를 아주 빠르게 끊김 없이 볼 수 있게 된 거랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 94 / 1120

<- **이전**: [93. 셀 호흡 (Cell Breathing) 현상](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/093_셀_호흡_현상/)
**다음**: [95. NOMA (Non-Orthogonal Multiple Access) - 비직교 다중 접속 (5G/6G 기술)](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/095_NOMA_비직교_다중_접속/) ->

---
