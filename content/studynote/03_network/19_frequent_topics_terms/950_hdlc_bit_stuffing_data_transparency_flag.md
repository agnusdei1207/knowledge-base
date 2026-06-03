+++
title = "950. HDLC 비트 스터핑 (Bit Stuffing)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [HDLC](/knowledge-base/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) [비트 스터핑](/knowledge-base/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)은 빈출 주제와 용어에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [HDLC](/knowledge-base/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) [비트 스터핑](/knowledge-base/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)을 이해하면 구분 명확성과 설명력 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층(L2)의 대표적인 고전 프로토콜인 **[HDLC](/knowledge-base/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/)(High-Level [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Link Control)**는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보낼 때 패킷의 시작과 끝을 알리기 위해 특수한 '깃발([Flag](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/))' [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 씁니다.
- **[플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)([Flag](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)) 패턴**: `01111110` (즉, 앞뒤로 0이 있고 가운데 1이 연속 6개). 
- **투명성(Transparency)의 위기**: 사용자가 보낸 순수한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(Payload) 안에 우연히 저 `01111110` 이라는 패턴이 똑같이 들어있을 수 있습니다. 
- 수신 측 장비는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽다가 중간에 저 패턴을 만나면 "아! 여기서 패킷 전송이 끝났구나!"라고 착각하여 뒤에 남은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 싹 다 버려버리는 치명적 오류가 터집니다.

```text
[자동 재전송 요구 선택적/GBN]
    │
    ▼
[HDLC 비트 스터핑]
    │
    └──▶ [반송파 감지 다중 접속 및 충돌 검출]
```

- **📢 섹션 요약 비유**: [HDLC](/knowledge-base/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) [비트 스터핑](/knowledge-base/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

- **개념**: 전송할 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 본문(Payload) 안에 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)(`01111110`)와 동일한 패턴이 우연히 발생하여 수신자가 프레임의 끝으로 오인하는 것을 방지하기 위해, **송신 측이 강제로 특정 위치에 [더미](/knowledge-base/studynote/04_software_engineering/11_testing_validation/459_dummy_test_double/) [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)(0)를 쑤셔 넣고(Stuffing), 수신 측이 이를 다시 뽑아내어(Destuffing) 원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 투명성을 보장하는 기술**입니다.

```text
[자동 재전송 요구 선택적/GBN]
    │
    ▼
[HDLC 비트 스터핑]
    │
    └──▶ [반송파 감지 다중 접속 및 충돌 검출]
```

- **📢 섹션 요약 비유**: [HDLC](/knowledge-base/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) [비트 스터핑](/knowledge-base/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

### 1. 송신자 (Stuffing - 쑤셔 넣기)
- 송신자는 전송할 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 1비트씩 훑어봅니다.
- 만약 본문 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중에 **`1`이 연속해서 5번(`11111`) 나오면, 그 즉시 묻지도 따지지도 않고 그 뒤에 강제로 `0`을 하나 쑤셔 넣습니다.** 
- **예시**: 
  - 원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/): `01111110` ([플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)와 똑같아 위험함!)
  - 스터핑 후: `011111` **`0`** `10`
- **효과**: 이제 본문 안에는 죽었다 깨어나도 `1`이 6번 연속 나오는 일(`01111110` [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) 패턴)이 절대 발생하지 않습니다. 수신자가 헷갈릴 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 0%가 됩니다.

### 2. 수신자 (De-stuffing - 뽑아내기)
- 수신자는 도착한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 1비트씩 훑어봅니다.
- **`1`이 5번 연속으로 나왔는데, 그 바로 뒤에 `0`이 붙어있다면?** "아! 이건 송신자가 억지로 쑤셔 넣은 가짜 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)구나!" 하고 눈치채고 **그 `0`을 칼로 쓱 오려내서 버려버립니다.**
- 가짜 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) `0`을 뽑아내면, 원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 100% 동일하게 완벽 복원됩니다.

[HDLC](/knowledge-base/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) [비트 스터핑](/knowledge-base/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [자동 재전송 요구](/knowledge-base/studynote/03_network/19_frequent_topics_terms/949_arq_automatic_repeat_request_go_back_n_selective/) 선택적/GBN가 기반 조건을 만든다면, [HDLC](/knowledge-base/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) [비트 스터핑](/knowledge-base/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)은 그 위에서 핵심 메커니즘을 구현하고, [반송파](/knowledge-base/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출은 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 구분 명확성과 설명력에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [자동 재전송 요구](/knowledge-base/studynote/03_network/19_frequent_topics_terms/949_arq_automatic_repeat_request_go_back_n_selective/) 선택적/GBN의 기반 정리 | [HDLC](/knowledge-base/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) [비트 스터핑](/knowledge-base/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)의 핵심 동작 | [반송파](/knowledge-base/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 구분 명확성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [HDLC](/knowledge-base/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) [비트 스터핑](/knowledge-base/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- **[비트 스터핑](/knowledge-base/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)([Bit Stuffing](/knowledge-base/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/))**: [HDLC](/knowledge-base/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) 같은 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 단위 프로토콜에서 씁니다. (1이 5개면 0 추가)
- **[바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 스터핑([Byte](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) Stuffing)**: [PPP](/knowledge-base/studynote/03_network/04_data_link_layer_error/224_ppp_point_to_point_protocol/) 같은 [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)(문자) 단위 프로토콜에서 씁니다. [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) 문자(`0x7E`)와 똑같은 글자가 나오면, 그 글자 앞에 '탈출(ESC, `0x7D`)' 문자를 억지로 끼워 넣어 "이건 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)가 아니라 진짜 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)야!"라고 면죄부를 주는 방식입니다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: [비트 스터핑](/knowledge-base/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)은 첩보 영화의 **'암호 편지 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)'**입니다. 첩보원끼리 "편지에 **'장미꽃'**이라는 단어가 나오면 작전 종료다!"라고 약속([플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/))했습니다. 그런데 첩보원이 일상 편지를 쓰다가 "오늘 길가에 **장미꽃**이 예쁘더라"라고 썼습니다. 본부가 이걸 보고 "아, 작전 끝났구나!" 오해하고 철수하면 대참사가 납니다. 이를 막기 위해 첩보원은 "편지 본문에 '장미'라는 단어를 쓸 일이 생기면, 무조건 중간에 '가짜(0)' 글자를 넣어 **'장미(가짜)꽃'**이라고 적어라!"라는 룰([비트 스터핑](/knowledge-base/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/))을 만듭니다. 본부는 편지를 읽다가 '장미(가짜)꽃'이 보이면 '(가짜)' 글자만 지워버리고 원래 뜻으로 이해합니다. 하지만 진짜 작전 종료일 때는 온전한 **'장미꽃'**이라고 적어 보내기 때문에, 본부가 오해 없이 정확하게 작전의 끝(프레임 종료)을 알아채는 멍청하면서도 완벽한 눈속임 규칙입니다.

---

## Ⅴ. 기대효과 및 결론

[HDLC](/knowledge-base/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) [비트 스터핑](/knowledge-base/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)은 빈출 주제와 용어를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 구분 명확성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [반송파](/knowledge-base/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출, [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 기반 용어 해석, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 기반 용어 해석 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [HDLC](/knowledge-base/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) [비트 스터핑](/knowledge-base/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [자동 재전송 요구](/knowledge-base/studynote/03_network/19_frequent_topics_terms/949_arq_automatic_repeat_request_go_back_n_selective/) 선택적/GBN | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 정의 (Definition) | 용어의 시작점을 분명하게 만든다. |
| 비교 (Comparison) | 헷갈리는 개념의 경계를 드러낸다. |
| [반송파](/knowledge-base/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 자동 재전송 요구 선택적/GBN]
    │
    ▼
[현재 개념: HDLC 비트 스터핑]
    │
    ├──▶ [확장 A: 반송파 감지 다중 접속 및 충돌 검출]
    └──▶ [확장 B: 컨텍스트 기반 용어 해석]
```

[HDLC](/knowledge-base/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) [비트 스터핑](/knowledge-base/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)는 [자동 재전송 요구](/knowledge-base/studynote/03_network/19_frequent_topics_terms/949_arq_automatic_repeat_request_go_back_n_selective/) 선택적/GBN에서 출발해 현재 메커니즘을 정교화하고, 이후 [반송파](/knowledge-base/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지 [다중 접속](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 및 충돌 검출와 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 기반 용어 해석 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 비슷한 이름의 장난감을 헷갈리지 않게 표를 붙이는 것과 같아요.
2. 이 개념은 무엇이 어떻게 다른지 쉽게 구별하게 도와줘요.
3. 그래서 시험에서도 실무에서도 말을 더 정확하게 쓸 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 1071 / 1120

← **이전**: [949. 자동 재전송 요구 (ARQ) 선택적/GBN](/knowledge-base/studynote/03_network/19_frequent_topics_terms/949_arq_automatic_repeat_request_go_back_n_selective/)
**다음**: [951. 반송파 감지 다중 접속 및 충돌 검출 (CSMA/CD)](/knowledge-base/studynote/03_network/19_frequent_topics_terms/951_csma_cd_carrier_sense_multiple_access_collision_detection/) →

---
