---
title: "1. 정보이론 (Information Theory) — Shannon, 1948"
date: "2026-04-21"
tags:
  - "studynote-algorithm"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Claude Shannon이 1948년 정립한 정보이론은 *불확실성을 정량화*하고, 통신·[압축](/studynote/02_operating_system/06_memory_management/347_compaction/)·암호화의 수학적 한계를 규정한다.
> 2. **가치**: 자기정보 I(x) = -log₂P(x) [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)라는 단 하나의 공식이 인터넷, [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/), [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 학습까지 연결되는 공통 언어다.
> 3. **판단 포인트**: 기술사 시험에서 '정보량·[엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/)·[채널 용량](/studynote/08_algorithm_stats/09_info_theory/155_channel_capacity/)·부호화 정리'는 묶음으로 출제된다 — 개념 간 인과 관계를 그릴 수 있어야 한다.

---

## Ⅰ. 개요 및 필요성

1948년 클로드 섀넌 (Claude Shannon) 은 벨연구소 기술 저널에 "A Mathematical Theory of Communication"을 발표하며 **정보이론 (Information Theory)** 을 창시했다. 이 논문 이전에는 '정보'를 수학적으로 정의할 방법이 없었다.

### 정보이론이 해결한 세 가지 근본 질문

| 질문 | 답 | 공식·개념 |
|:---|:---|:---|
| 메시지가 얼마나 많은 정보를 담는가? | 놀라운 사건일수록 정보량이 크다 | I(x) = -log₂P(x) bits |
| 평균 정보량의 최솟값은? | [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 분포의 [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/) | H(X) = -Σ p·log₂p |
| 잡음 있는 채널을 오류 없이 얼마나 빠르게 전송할 수 있나? | [채널 용량](/studynote/08_algorithm_stats/09_info_theory/155_channel_capacity/) C가 상한 | C = B·log₂(1 + S/N) |

### 자기정보 (Self-Information)

사건 x가 발생했을 때 얻는 정보량:

```
I(x) = -log₂ P(x)   [단위: bit]
```

- P(x) = 1 (확실한 사건) -> I = 0 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) (놀랍지 않음)
- P(x) = 0.5 (동전 앞면) -> I = 1 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)
- P(x) = 1/8 -> I = 3 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) (드문 사건, 높은 정보량)

[로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 밑이 2이면 <strong><a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/">비트</a> (<a href="/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/">bit</a>)</strong>, e이면 <strong>나트 (<a href="/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/">nat</a>)</strong>, 10이면 **하틀리 (hartley)** 단위가 된다.

📢 **섹션 요약 비유**: 정보량은 "깜짝 상자"와 같다 — 열어봤을 때 놀랄수록 ([확률](/studynote/08_algorithm_stats/08_stats/130_probability/)이 낮을수록) 상자 안 선물이 크다(정보량이 많다).

---

## Ⅱ. 아키텍처 및 핵심 원리

### 섀넌 통신 모델

```
+----------+   메시지   +----------+   신호   +----------+
|  정보원   |---------->|  송신기   |--------->|  채널    |
| (Source) |           |(Encoder) |          |(+ 잡음)  |
+----------+           +----------+          +----+-----+
                                                   | 수신 신호
                                              +----v-----+   메시지   +----------+
                                              |  수신기   |---------->|  수신자  |
                                              |(Decoder) |           |  (Sink)  |
                                              +----------+           +----------+
```

### 섀넌의 핵심 업적 연대표

```
1948년 -------------------------------------------------------------►
   |
   +-► 자기정보 I(x) = -log₂P(x) 정의
   +-► 섀넌 엔트로피 H(X) = -Σ p·log₂p 정의
   +-► 소스 부호화 정리 (압축 한계 = 엔트로피)
   +-► 채널 부호화 정리 (오류 없는 전송 한계 = 채널 용량 C)
   +-► 상호 정보량 I(X;Y) 정의
   +-► 연속 채널 용량 C = B·log₂(1+S/N) (Shannon-Hartley 정리)
```

### 이진 채널 (Binary Channel)

가장 단순한 형태로, 입력 0 또는 1, 오류 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) p인 <strong>이진 대칭 채널 (<a href="/studynote/12_it_management/01_governance_strategy/019_bsc/">BSC</a>, Binary Symmetric Channel)</strong>:

```
  0 -----(1-p)----► 0
    ╲
     (p)
       ╲
        ► 1
  1 -----(1-p)----► 1
    ╲
     (p)
       ╲
        ► 0
```

BSC의 [채널 용량](/studynote/08_algorithm_stats/09_info_theory/155_channel_capacity/): C = 1 - H(p) = 1 + p·log₂p + (1-p)·log₂(1-p)

📢 **섹션 요약 비유**: 섀넌 통신 모델은 "우편 시스템"과 같다 — 편지(정보원)를 봉투([인코더](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/))에 넣어 도로(채널)로 보내고, 배달부([디코더](/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/))가 풀어 수신자에게 전달한다. 도로가 막히거나(잡음) 봉투가 젖으면(오류) 정보가 손실된다.

---

## Ⅲ. 비교 및 연결

### 섀넌 이전과 이후 비교

| 항목 | 섀넌 이전 | 섀넌 이후 |
|:---|:---|:---|
| 정보의 정의 | 주관적, 비공식 | -log₂P(x)로 객관화 |
| [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 한계 | 경험적 | [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/) H(X)가 하한 |
| 통신 오류 | 오류 없는 전송 불가라 믿음 | [채널 용량](/studynote/08_algorithm_stats/09_info_theory/155_channel_capacity/) C < 전송률이면 가능 |
| 응용 범위 | 전신·전화 | 인터넷, Wi-Fi, [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/), [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) |

### 타 분야와의 연결

- **열역학**: 볼츠만 [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/) S = k_B·ln(W) — 섀넌 [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/)와 수학적으로 동일한 구조
- **통계학**: 최대 [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/) 원리 -> 사전 지식이 없을 때 균등분포가 최선
- <strong><a href="/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/">머신러닝</a></strong>: [크로스 엔트로피](/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/) 손실, KL (Kullback-Leibler) 다이버전스, [상호 정보량](/studynote/08_algorithm_stats/09_info_theory/152_mutual_information/) 기반 특성 선택

📢 **섹션 요약 비유**: 정보이론과 열역학 [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/)의 관계는 "쌍둥이 형제"와 같다 — 얼굴(수식)이 똑같이 생겼지만 사는 세계(물리학 vs 수학)가 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 응용 영역별 섀넌 이론의 역할

| 분야 | 섀넌 이론 적용 | 구체적 기술 |
|:---|:---|:---|
| [데이터 압축](/studynote/08_algorithm_stats/09_info_theory/159_compression/) | [소스 부호화 정리](/studynote/08_algorithm_stats/09_info_theory/156_source_coding/) | ZIP, JPEG, MP3, H.265 |
| 오류 정정 | [채널 부호화 정리](/studynote/08_algorithm_stats/09_info_theory/157_channel_coding/) | [해밍 코드](/studynote/01_computer_architecture/02_data_representation_arithmetic/111_hamming_code/), [LDPC](/studynote/03_network/04_data_link_layer_error/203_ldpc_low_density_parity_check/), [폴라 코드](/studynote/03_network/04_data_link_layer_error/204_polar_code_5g_control_channel/) |
| 암호화 | 완전 비밀성(Perfect Secrecy) | [일회용 패드](/studynote/09_security/02_crypto/074_one_time_pad/)([OTP](/studynote/01_computer_architecture/15_advanced_topics/748_otp/)) |
| [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) | [크로스 엔트로피](/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/) [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) | 신경망 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)기 학습 |
| [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 통신 | [채널 용량](/studynote/08_algorithm_stats/09_info_theory/155_channel_capacity/) = B·log₂(1+S/N) | [MIMO](/studynote/03_network/02_multiplexing_multiple_access/097_MIMO_다중_안테나_기술/), [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 설계 |

### 기술사 판단 포인트

1. <strong>"<a href="/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a>률 한계는?"</strong> -> [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/) H(X)가 평균 부호 길이 하한
2. **"오류 없는 전송 조건은?"** -> 전송률 R < [채널 용량](/studynote/08_algorithm_stats/09_info_theory/155_channel_capacity/) C
3. <strong>"<a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> <a href="/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a> <a href="/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/">손실 함수</a>로 왜 <a href="/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/">크로스 엔트로피</a>?"</strong> -> 최대우도 추정([MLE](/studynote/08_algorithm_stats/08_stats/143_mle/))과 동치이기 때문

📢 **섹션 요약 비유**: 섀넌의 [채널 용량](/studynote/08_algorithm_stats/09_info_theory/155_channel_capacity/)은 "도로 용량"과 같다 — 차선 수([대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/))와 도로 상태(S/N비)가 교통 처리량을 결정하고, 이를 초과하면 교통 체증(오류)이 반드시 발생한다.

---

## Ⅴ. 기대효과 및 결론

정보이론은 <strong>디지털 문명의 수학적 토대</strong>다. 섀넌의 두 부호화 정리는 각각:
- **소스 부호화**: 저장/전송 용량의 한계를 알려준다 ([압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 가능 최대치)
- **채널 부호화**: [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 있는 통신의 가능/불가능 경계를 그어준다

현재까지 [폴라 코드](/studynote/03_network/04_data_link_layer_error/204_polar_code_5g_control_channel/) ([Polar Code](/studynote/03_network/04_data_link_layer_error/204_polar_code_5g_control_channel/), [5G NR](/studynote/03_network/15_nextgen_communication_architecture/763_5g_nr_new_radio_scalable_numerology/) 제어 채널) 가 섀넌 한계에 가장 근접한 실용 코드로 평가된다. 양자 정보이론은 고전 정보이론을 양자 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)([qubit](/studynote/01_computer_architecture/12_accelerators_ai_hardware/448_qubit/))로 확장하며 차세대 암호화·통신 기반을 형성하고 있다.

📢 **섹션 요약 비유**: 섀넌의 두 정리는 "교통공학의 두 법칙"과 같다 — "짐을 얼마나 작게 쌀 수 있는가(소스 부호화)"와 "도로가 얼마나 많은 차를 안전하게 보낼 수 있는가(채널 부호화)"를 동시에 최적화하는 것이 현대 통신 설계의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 관련 개념 | 수식 |
|:---|:---|:---|
| 자기정보 | [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/), [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) | I(x) = -log₂P(x) |
| [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/) | 상호정보, 결합엔트로피 | H(X) = -Σ p log₂p |
| [채널 용량](/studynote/08_algorithm_stats/09_info_theory/155_channel_capacity/) | AWGN 채널, [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) | C = B·log₂(1+S/N) |
| 소스 부호화 | 허프만, 산술 부호화 | L̄ ≥ H(X) |
| 채널 부호화 | [LDPC](/studynote/03_network/04_data_link_layer_error/203_ldpc_low_density_parity_check/), [폴라 코드](/studynote/03_network/04_data_link_layer_error/204_polar_code_5g_control_channel/) | R < C -> 오류 없는 전송 가능 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[자기정보]
    |
    v
[엔트로피]
    |
    v
[채널 용량]
    |
    v
[소스 부호화]
```

이 흐름도는 선행 개념이 현재 개념으로 응축되고, 다시 확장 개념으로 이어지는 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. **정보량은 "깜짝 상자"**: 열었을 때 예상 못 한 것이 나올수록 상자가 크다 (희귀할수록 정보가 많다).
2. <strong><a href="/studynote/08_algorithm_stats/09_info_theory/151_entropy/">엔트로피</a>는 "상자 크기의 평균"</strong>: 여러 상자를 매일 열면, 평균적으로 얼마나 놀라는지를 나타낸다.
3. <strong><a href="/studynote/08_algorithm_stats/09_info_theory/155_channel_capacity/">채널 용량</a>은 "도로의 차선 수"</strong>: 차선이 많고 도로가 좋을수록 동시에 많은 차(정보)를 보낼 수 있다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 150 / 175

<- **이전**: [20. 회귀 분석 (Regression Analysis) — 단순/다중/로지스틱](/studynote/08_algorithm_stats/08_stats/149_regression_analysis/)
**다음**: [2. 엔트로피 (Shannon Entropy) — H(X) = -Σ p·log₂p](/studynote/08_algorithm_stats/09_info_theory/151_entropy/) ->

---
