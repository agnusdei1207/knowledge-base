---
title: "CSMA/CD"
date: "2026-05-08"
tags:
  - "studynote-network"
weight: 951
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [반송파](/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출은 빈출 주제와 용어에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [반송파](/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출을 이해하면 구분 명확성과 설명력 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

하나의 구리선(공유 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/))을 여러 대의 PC가 공유할 때, 2대 이상이 동시에 전기를 쏘면 전압이 겹쳐서 데이터가 걸레짝이 됩니다. 이 피 터지는 도로([Collision Domain](/studynote/03_network/05_lan_wan_l2_devices/237_collision_domain_vs_broadcast_domain/))의 교통정리 규칙이 필요했습니다.

```text
[HDLC 비트 스터핑]
    |
    v
[반송파 감지 다중 접속 및 충돌 검출]
    |
    +---> [은닉 단말 문제]
```

- **📢 섹션 요약 비유**: [반송파](/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IEEE 802.3 유선 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)([Ethernet](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/))의 절대 표준 규약입니다.

### 1단계: CS (Carrier Sense) - "말하기 전에 귀 기울이기"
- 내가 데이터를 보내기 전에, 랜선에 귀를 대고 다른 놈이 지금 전기를 쏘고 있는지(Carrier) 엿듣습니다.
- 누군가 말하고 있으면(Busy) 조용히 기다리고, 랜선이 조용하면([Idle](/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/)) 그제야 패킷을 밀어 넣습니다.

### 2단계: MA ([Multiple Access](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/)) - "[다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/)의 비극"
- 10명이 다 같이 귀를 대고 기다리다가, 랜선이 조용해지는 찰나의 순간에 "지금이다!" 하고 2명이 동시에 패킷을 쏴버리는 불상사가 100% 발생합니다. 전기 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)가 쾅 부딪혀 쓰레기가 됩니다.

### 3단계: CD ([Collision Detection](/studynote/03_network/02_multiplexing_multiple_access/106_CSMA_CD_유선이더넷_충돌감지/)) - "충돌 감지와 [잼 신호](/studynote/03_network/02_multiplexing_multiple_access/107_잼_신호_백오프_알고리즘/)" 🌟 핵심 🌟
여기가 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)의 위대한 발명입니다. (유선은 전압이 변하는 걸로 충돌을 쉽게 알 수 있습니다.)
- **충돌 감지**: 패킷을 쏘면서도 내 귀를 열어둡니다. 내가 보낸 5V [신호](/studynote/02_operating_system/02_process_thread/130_signal/)와 상대방의 5V [신호](/studynote/02_operating_system/02_process_thread/130_signal/)가 부딪혀 전압이 10V로 확 튀어 오르는 순간! "아 ㅆㅂ 충돌 났다([Collision](/studynote/05_database/04_transactions_concurrency/563_hash_collision_chaining_linear_probing/))!" 하고 즉각 눈치챕니다.
- <strong><a href="/studynote/03_network/02_multiplexing_multiple_access/107_잼_신호_백오프_알고리즘/">잼 신호</a> (<a href="/studynote/03_network/02_multiplexing_multiple_access/107_잼_신호_백오프_알고리즘/">Jam Signal</a>)</strong>: 충돌을 눈치챈 두 컴퓨터는 즉시 전송을 멈추고, 전국의 모든 컴퓨터에게 "야 다들 멈춰!! 충돌 났어!!!"라는 삐- 소리([잼 신호](/studynote/03_network/02_multiplexing_multiple_access/107_잼_신호_백오프_알고리즘/))를 32비트짜리로 요란하게 방송합니다. 이 소리를 들은 모든 컴퓨터는 전송을 멈춥니다.

### 4단계: 이진 지수 백오프 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) (Binary Exponential Backoff) 🌟
충돌 난 두 놈이 똑같이 1초 쉬었다 다시 쏘면 영원히 충돌이 납니다. 랜덤 눈치 게임을 돌립니다.
- 첫 충돌: 0초 또는 1초 중 '랜덤'으로 하나 골라서 쉬었다 쏩니다. (재충돌 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 50%)
- 두 번째 겹침: 이번엔 범위가 $2^2$로 늘어나, 0~3초 중 랜덤으로 쉬었다 쏩니다. ([확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 25%)
- 세 번째 겹침: 0~7초 중 랜덤 휴식.
- 충돌이 반복될수록 쉴 수 있는 시간의 범위(K)가 지수 함수($2^n$)로 미친 듯이 벌어져서, 두 컴퓨터가 똑같은 숫자를 뽑을 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)을 수학적으로 0으로 수렴하게 만들어 결국 한 놈이 먼저 쏘게 만들어주는 눈치 게임의 극의입니다. (최대 16번 충돌하면 포기하고 패킷 버림).

```text
[HDLC 비트 스터핑]
    |
    v
[반송파 감지 다중 접속 및 충돌 검출]
    |
    +---> [은닉 단말 문제]
```

- **📢 섹션 요약 비유**: [반송파](/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

- [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)([Hub](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)) 시대에는 이 눈치 게임이 필수였지만, 요즘 우리가 쓰는 <strong><a href="/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a>(<a href="/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">Switch</a>, 전이중 Full-Duplex)</strong> 장비는 포트마다 도로를 따로 분리해주기 때문에 충돌([Collision](/studynote/05_database/04_transactions_concurrency/563_hash_collision_chaining_linear_probing/)) 자체가 아예 일어나지 않습니다.
- 따라서 현대 유선 랜망에서는 [CSMA](/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/CD 기능이 사실상 꺼진 상태로(필요 없이) 빛의 속도로 쌩쌩 양방향 통신을 하고 있습니다.

[반송파](/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [HDLC](/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) [비트 스터핑](/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)이 기반 조건을 만든다면, [반송파](/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출은 그 위에서 핵심 메커니즘을 구현하고, [은닉 단말](/studynote/03_network/19_frequent_topics_terms/952_csma_ca_hidden_terminal_rts_cts_wireless/) 문제는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 구분 명확성과 설명력에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [HDLC](/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) [비트 스터핑](/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)의 기반 정리 | [반송파](/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출의 핵심 동작 | [은닉 단말](/studynote/03_network/19_frequent_topics_terms/952_csma_ca_hidden_terminal_rts_cts_wireless/) 문제의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 구분 명확성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [CSMA](/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/CD는 '어두운 회의실에서의 완벽한 토론 예절'입니다. 어두워서 누가 말할지 안 보입니다. **첫째(CS)**, 말하기 전에 누군가 떠들고 있는지 조용히 귀를 기울입니다. **둘째(MA)**, 조용해지면 말을 꺼냅니다. **셋째(CD)**, 근데 눈치가 겹쳐서 나랑 철수가 동시에 "저기요!" 하고 말이 겹쳤습니다. 둘 다 깜짝 놀라 말을 멈추고 "아 겹쳤네 ㅈㅅ!([잼 신호](/studynote/03_network/02_multiplexing_multiple_access/107_잼_신호_백오프_알고리즘/))" 하고 소리칩니다. <strong>넷째(백오프 <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a>)</strong>, 다시 동시에 말하면 또 겹치니까, 나는 마음속으로 3초를 세고, 철수는 랜덤으로 5초를 센 뒤에, 내가 먼저 3초 뒤에 "제가 먼저 할게요" 하고 치고 나가는 완벽한 비동기 눈치 게임 매너입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [반송파](/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출을 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [HDLC](/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) [비트 스터핑](/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/) 수준의 기본 대책으로 충분한지, 아니면 [반송파](/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출이 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [은닉 단말](/studynote/03_network/19_frequent_topics_terms/952_csma_ca_hidden_terminal_rts_cts_wireless/) 문제와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 구분 명확성 부족인지, 설명력 악화인지 먼저 분리한다.
2. [반송파](/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 [은닉 단말](/studynote/03_network/19_frequent_topics_terms/952_csma_ca_hidden_terminal_rts_cts_wireless/) 문제와의 연계 방식을 함께 검증한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [반송파](/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [HDLC](/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) [비트 스터핑](/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)와의 경계를 정리하지 않아 중복 투자나 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: [반송파](/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출을 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[반송파](/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출은 빈출 주제와 용어를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 구분 명확성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [은닉 단말](/studynote/03_network/19_frequent_topics_terms/952_csma_ca_hidden_terminal_rts_cts_wireless/) 문제, [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 기반 용어 해석, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 기반 용어 해석 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [반송파](/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [HDLC](/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) [비트 스터핑](/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 정의 (Definition) | 용어의 시작점을 분명하게 만든다. |
| 비교 (Comparison) | 헷갈리는 개념의 경계를 드러낸다. |
| [은닉 단말](/studynote/03_network/19_frequent_topics_terms/952_csma_ca_hidden_terminal_rts_cts_wireless/) 문제 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: HDLC 비트 스터핑]
    |
    v
[현재 개념: 반송파 감지 다중 접속 및 충돌 검출]
    |
    +---> [확장 A: 은닉 단말 문제]
    +---> [확장 B: 컨텍스트 기반 용어 해석]
```

[반송파](/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출는 [HDLC](/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) [비트 스터핑](/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)에서 출발해 현재 메커니즘을 정교화하고, 이후 [은닉 단말](/studynote/03_network/19_frequent_topics_terms/952_csma_ca_hidden_terminal_rts_cts_wireless/) 문제와 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 기반 용어 해석 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 비슷한 이름의 장난감을 헷갈리지 않게 표를 붙이는 것과 같아요.
2. 이 개념은 무엇이 어떻게 다른지 쉽게 구별하게 도와줘요.
3. 그래서 시험에서도 실무에서도 말을 더 정확하게 쓸 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 1072 / 1120

<- **이전**: [950. HDLC 비트 스터핑 (Bit Stuffing)](/studynote/03_network/19_frequent_topics_terms/950_hdlc_bit_stuffing_data_transparency_flag/)
**다음**: [952. 은닉 단말 (Hidden Terminal) 문제 (CSMA/CA RTS/CTS)](/studynote/03_network/19_frequent_topics_terms/952_csma_ca_hidden_terminal_rts_cts_wireless/) ->

---
