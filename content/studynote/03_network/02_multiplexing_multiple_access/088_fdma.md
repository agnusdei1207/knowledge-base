---
title: "FDMA (Frequency Division Multiple Access)"
date: "2026-03-30"
tags:
  - "network"
  - "studynote-network"
weight: 88
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: FDMA (Frequency [Division](/studynote/05_database/07_exam_summary/411_division_operation/) [Multiple Access](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/))는 통신 시스템의 전체 주파수 대역을 좁은 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)의 여러 채널로 쪼개어 다수의 사용자에게 고정 할당하는 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 기술이다.
> 2. **가치**: 사용자가 자신만의 주파수 차선을 독점하므로 통신 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 거의 발생하지 않으며, 아날로그 음성이나 방송처럼 연속적인 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 전송에 매우 안정적인 구조를 제공한다.
> 3. **판단 포인트**: 각 채널 사이에 상호 간섭을 막기 위한 여유 공간([Guard Band](/studynote/03_network/19_frequent_topics_terms/946_guard_band_fdm_adjacent_channel_interference/))이 필수적이라 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 낭비가 크고, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통신처럼 트래픽이 불규칙한 현대망에서는 비효율적이므로 채택을 지양해야 한다.

---

## Ⅰ. 개요 및 필요성

과거 1세대(1G) 아날로그 이동통신 환경에서는 다수의 사용자가 하나의 기지국을 동시에 이용해야 했다. 주파수가 겹치면 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)가 충돌하여 통화가 혼선되므로, 전체 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 쪼개어 사용자마다 독립적인 "주파수 통로"를 부여하는 FDMA가 도입되었다.

이 방식은 송신자와 수신자 사이에 끊김 없는 물리적 경로를 만들어주어 제어가 매우 단순하다. 그러나 특정 주파수 채널을 배정받은 사용자가 말을 하지 않는 순간에도 그 주파수를 다른 사람이 재사용할 수 없어 자원이 낭비되는 근본적인 한계가 발생한다.

- 📢 섹션 요약 비유: 하나의 커다란 라디오 주파수를 여러 개의 미니 라디오 방송국 채널로 잘게 쪼개어, 각자 자기 채널에서만 떠들도록 만든 방송 시스템과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

FDMA 시스템은 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 분할과 필터링을 통해 사용자 간 [직교성](/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/)을 유지한다.

| 핵심 구성요소 | 역할 및 동작 원리 |
| :--- | :--- |
| Channel (채널) | 전체 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 `f1`, `f2`, `f3` 등의 서브 대역으로 일정하게 분할한 고정 경로 |
| [Guard Band](/studynote/03_network/19_frequent_topics_terms/946_guard_band_fdm_adjacent_channel_interference/) ([보호 대역](/studynote/03_network/02_multiplexing_multiple_access/074_보호_대역_Guard_Band/)) | 인접한 채널 간의 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)가 겹치지 않도록 채널과 채널 사이에 두는 빈 주파수 공간 |
| [BPF](/studynote/02_operating_system/01_overview_architecture/069_ebpf/) (Band-Pass Filter) | 수신기에서 자신에게 할당된 특정 주파수 대역의 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)만 통과시키고 나머지는 차단 |

```text
+-------------------------------------------------------------+
|          FDMA의 주파수 자원 분할 및 간섭 방지 구조          |
+-------------------------------------------------------------+
| 전력                                                        |
|  ^                                                          |
|  |  [User 1]      [User 2]      [User 3]      [User 4]      |
|  | +--------+    +--------+    +--------+    +--------+     |
|  | | 채널 1 | GB | 채널 2 | GB | 채널 3 | GB | 채널 4 |     |
|  | +--------+    +--------+    +--------+    +--------+     |
|  +------------------------------------------------------> 주파수(f)
|                                                             |
|  * GB = Guard Band (인접 채널 간섭/ACI 방지용 완충 지대)    |
+-------------------------------------------------------------+
```

위 아키텍처에서 보이듯, 필터의 차단 특성이 완벽한 수직이 아니기 때문에 `ACI (Adjacent Channel Interference, 인접 채널 간섭)`를 방지하려면 반드시 Guard Band가 필요하며, 이 공간은 누구도 통신할 수 없는 데드존이 된다.

- 📢 섹션 요약 비유: 넓은 고속도로를 여러 개의 1차선 도로로 나누고, 차들끼리 부딪히지 않게 차선 사이에 넓은 화단을 심어둔 것과 같다. 화단 때문에 실제 차가 다니는 길은 줄어든다.

---

## Ⅲ. 비교 및 연결

[다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 기술은 자원을 어떻게 나누느냐에 따라 세대로 진화해 왔다.

| 비교 축 | FDMA (Frequency [Division](/studynote/05_database/07_exam_summary/411_division_operation/)) | [TDMA](/studynote/03_network/02_multiplexing_multiple_access/089_시분할_다중접속_TDMA/) (Time [Division](/studynote/05_database/07_exam_summary/411_division_operation/)) | [OFDMA](/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/) (Orthogonal FDMA) |
| :--- | :--- | :--- | :--- |
| 자원 분할 축 | 주파수 대역 분할 | 시간(Time Slot) 분할 | 직교 [부반송파](/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/) 분할 |
| 낭비 요인 | [Guard Band](/studynote/03_network/19_frequent_topics_terms/946_guard_band_fdm_adjacent_channel_interference/) (주파수 낭비) | Guard Time (시간 낭비) | [직교성](/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/) 덕분에 낭비 최소화 |
| 통신 적합성 | 연속적인 아날로그 음성 (1G) | 디지털 음성 및 저속 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) (2G) | 고속 모바일 광대역 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) (4G/[5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/)) |
| 장비 복잡도 | [BPF](/studynote/02_operating_system/01_overview_architecture/069_ebpf/) 등 아날로그 필터링 복잡 | 시간 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)(Sync) 복잡 | [FFT](/studynote/08_algorithm_stats/07_numerical/126_fft/)/IFFT 디지털 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 처리 필수 |

FDMA는 주파수를 쪼개어 "공간"을 나누고, TDMA는 주파수를 통째로 쓰되 "시간"을 교대로 쓴다. OFDMA는 FDMA의 진화형으로, [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 간 [직교성](/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/)([Orthogonality](/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/))을 이용해 Guard Band를 없애고 주파수를 촘촘하게 겹쳐 써서 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 효율을 극대화했다.

- 📢 섹션 요약 비유: FDMA가 뷔페에서 각자 자기 접시를 들고 따로 먹는 거라면, TDMA는 하나의 큰 접시를 시간제한을 두고 교대로 먹는 것이고, OFDMA는 식판에 반찬 칸을 빈틈없이 겹쳐 완벽히 세팅해 먹는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

현대 통신망을 설계할 때 FDMA 기반 구조는 구체적인 환경 요인을 기준으로 판별해야 한다.

- 아날로그 TV 방송, FM 라디오, 혹은 위성 통신의 특정 [백홀](/studynote/03_network/20_performance_evaluation_advanced/1009_backhaul_network_base_station_core_connection/)([Backhaul](/studynote/03_network/20_performance_evaluation_advanced/1009_backhaul_network_base_station_core_connection/)) 링크처럼, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 발생이 버스트(Burst)하지 않고 항상 일정한 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 점유하는 환경에서는 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 없는 FDMA가 여전히 유효한 설계다.
- 반면, 웹 서핑이나 패킷 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통신처럼 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보냈다가 한참 쉬는" 트래픽 패턴에서는 주파수를 고정 점유하는 FDMA를 적용하면 네트워크 수용 용량(Capacity)이 극도로 저하되므로 절대 기피해야 한다.
- `FDD (Frequency Division Duplex, 주파수 분할 이중통신)` 장비 설계 시, 송신 대역과 수신 대역 간의 간섭을 막는 듀플렉서(Duplexer) 비용과 크기가 기지국이나 단말기 소형화에 치명적인 병목이 됨을 인지해야 한다.

- 📢 섹션 요약 비유: 끊임없이 물이 나오는 호스(방송)를 연결할 때는 독립된 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)(FDMA)가 좋지만, 찔끔찔끔 나오는 여러 수도꼭지([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 각 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)에 물리면 빈 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)만 많아져 낭비가 심하다.

---

## Ⅴ. 기대효과 및 결론

FDMA는 다수의 통신자가 충돌 없이 무선 자원을 공유하는 가장 기본적이고 직관적인 기술적 기틀을 마련했다. 하드웨어 제어가 직관적이며 연속된 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 품질 보장이라는 확실한 장점을 남겼다.

그러나 주파수 스펙트럼은 매우 비싼 한정 자원이기 때문에, Guard Band와 유휴 시간 채널 점유로 인한 비효율성은 모바일 시대에 한계를 맞았다. 따라서 FDMA는 단독 기술로서의 생명력은 다했지만, 주파수를 분할한다는 핵심 철학은 후속 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 기술의 기본 논리적 토대로 영구히 자리 잡았다.

- 📢 섹션 요약 비유: 비싼 땅을 낭비하며 넓게 집을 짓던 옛날 방식이 한계에 부딪혔지만, 땅을 구획 정리한다는 개념 자체는 현대의 아파트([OFDMA](/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/))를 짓는 기초가 되었다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Multiple Access](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) ([다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/)) | 한정된 무선 자원을 여러 기기가 간섭 없이 나누어 쓰는 상위 기술 범주 |
| [Guard Band](/studynote/03_network/19_frequent_topics_terms/946_guard_band_fdm_adjacent_channel_interference/) ([보호 대역](/studynote/03_network/02_multiplexing_multiple_access/074_보호_대역_Guard_Band/)) | 인접 주파수 채널 간의 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 간섭을 막기 위한 필수적인 완충 주파수 |
| ACI (Adjacent Channel Interference) | 채널을 좁게 붙였을 때 옆 채널의 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)가 필터를 넘어와 내 통신을 방해하는 현상 |
| [OFDMA](/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/) (직교 주파수 분할 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/)) | [Guard Band](/studynote/03_network/19_frequent_topics_terms/946_guard_band_fdm_adjacent_channel_interference/) 없이 [부반송파](/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/)를 촘촘히 겹쳐 FDMA의 주파수 낭비를 해결한 4G/[5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
아날로그 음성 신호 전송 요구 (1G)
    |
    v
FDMA (주파수를 물리적인 채널로 고정 분할, ACI 방지용 Guard Band 도입)
    |
    v
디지털화 및 주파수 효율 한계 도달
    |
    v
TDMA / CDMA (시간이나 코드를 통한 자원 공유 방식 등장 - 2G/3G)
    |
    v
OFDMA (직교성을 통한 Guard Band 제거 및 부반송파 분배로 효율 극대화 - 4G/5G)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 여러 친구들이 한 운동장에서 각자 자기 노래를 부르면 너무 시끄러워서 안 들려요.
2. 그래서 FDMA는 운동장을 밧줄로 여러 칸으로 쪼개서, 한 명당 한 칸씩 들어가서 노래 부르게 한 거예요.
3. 노래가 안 겹쳐서 좋지만, 칸과 칸 사이에 빈 공간을 둬야 해서 운동장을 낭비하게 되는 단점이 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 88 / 1120

<- **이전**: [87. 다중 접속 (Multiple Access) 개념 (MAC 계층 연관)](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/)
**다음**: [89. TDMA (Time Division Multiple Access) - 슬롯 할당](/studynote/03_network/02_multiplexing_multiple_access/089_시분할_다중접속_TDMA/) ->

---
