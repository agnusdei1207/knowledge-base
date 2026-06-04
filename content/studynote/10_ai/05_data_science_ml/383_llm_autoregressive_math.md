---
title: "383. LLM 자기 회귀 (Auto-Regressive) 언어 모델 우도 수식"
date: "2026-05-09"
tags:
  - "studynote-ai"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 자기 회귀 (Auto-Regressive) 언어 모델은 시퀀스의 결합 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)을 연쇄 법칙 (Chain Rule)으로 분해하여, 이전 토큰들이 주어졌을 때 다음 토큰의 [조건부 확률](/studynote/08_algorithm_stats/08_stats/132_conditional_probability/)을 순차적으로 곱하는 방식으로 텍스트를 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한다.
> 2. **가치**: [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 우도 (Log-Likelihood) 최대화를 학습 목표로 삼으면, 교사 강요 (Teacher Forcing)로 안정적이고 효율적인 학습이 가능하며 [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 계열 모델의 사전학습 방법이다.
> 3. **판단 포인트**: 퍼플렉시티 (Perplexity)는 언어 모델의 표준 평가 지표로, 낮을수록 예측 불확실성이 낮고 더 나은 언어 모델임을 의미한다.

---

## Ⅰ. 개요 및 필요성

언어 모델의 궁극적 목표는 자연어 텍스트의 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 분포 P(x₁, x₂, …, xₙ)를 학습하는 것이다. 자기 회귀 접근은 이를 [조건부 확률](/studynote/08_algorithm_stats/08_stats/132_conditional_probability/)의 곱으로 분해해 각 단계를 독립적으로 학습 가능하게 만든다.

[GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) ([Generative Pre-trained Transformer](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)) 계열은 모두 이 원리로 사전학습된다. 인간의 읽기·[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)처럼 "앞 내용을 보고 다음을 예측"하는 자연스러운 귀납 구조다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 자기 회귀 언어 모델은 "앞 글자들을 보고 다음 글자를 맞추는 받아쓰기 게임"을 무한 반복하며 언어 패턴을 학습하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 결합 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)의 연쇄 법칙 분해

```
P(x₁, x₂, ..., xₙ) = Π_{t=1}^{n} P(xₜ | x₁, ..., xₜ₋₁)
                     = P(x₁) · P(x₂|x₁) · P(x₃|x₁,x₂) · ...
```

### 학습 목표: [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 우도 최대화

```
L(θ) = Σ_{t=1}^{n} log P(xₜ | x₁,...,xₜ₋₁ ; θ)

최적화: θ* = argmax L(θ)
교차 엔트로피 손실 = -L(θ) / n  (최소화)
```

### 교사 강요 (Teacher Forcing)

학습 시 실제 토큰(Ground Truth)을 이전 입력으로 사용:
```
+------------------------------------------------------+
|  학습:   [BOS, "오늘", "날씨", "가"] -> "맑다" 예측   |
|           ^실제 토큰 사용 (Teacher Forcing)           |
|                                                      |
|  추론:   [BOS, "오늘"] -> "날씨" 예측 ->               |
|           [BOS, "오늘", "날씨"] -> "가" 예측 -> ...     |
|           ^이전 예측 토큰 사용 (Auto-Regressive)      |
+------------------------------------------------------+
```

### 퍼플렉시티 (Perplexity)

```
PPL = exp( -1/n · Σ_{t=1}^{n} log P(xₜ | x₁,...,xₜ₋₁) )
    = exp( H(언어 모델) )   (교차 엔트로피의 지수)

PPL=1   : 완벽한 예측 (불가능)
PPL=100 : 매 위치에서 100가지 균등 분포로 추측하는 수준
```

| 모델 | PPL (PTB) | 비고 |
|:---|:---|:---|
| n-gram (3-gram) | ~[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)0 | 고전 |
| [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/) | ~65 | 딥러닝 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) |
| [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-2 | ~35 | [트랜스포머](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) |
| [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-3 | ~20 | 대규모 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) |

- **📢 섹션 요약 비유**: 퍼플렉시티는 "언어 모델이 다음 단어를 고를 때 몇 가지 선택지 앞에서 머뭇거리는가"다. 낮을수록 자신 있게 다음 단어를 고른다.

---

## Ⅲ. 비교 및 연결

| 구분 | 자기 회귀 (AR) | 자동 인코딩 (AE, BERT형) |
|:---|:---|:---|
| 학습 목표 | 다음 토큰 예측 (LM loss) | [마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)크 토큰 복원 ([MLM](/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/) loss) |
| [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 방식 | 좌->우 순차 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 비자기 회귀 (동시 예측) |
| 대표 모델 | [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-2/3/4, LLaMA | [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/), RoBERTa |
| 강점 | 텍스트 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 이해·[분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) [태스크](/studynote/02_operating_system/02_process_thread/150_task/) |

- **📢 섹션 요약 비유**: AR 모델은 소설을 처음부터 끝까지 순서대로 쓰는 작가, AE 모델은 이미 쓴 소설의 빈칸을 메우는 편집자다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**Beam Search**: 각 단계에서 상위 k개 후보 유지, 최종 가장 높은 시퀀스 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 선택
<strong><a href="/studynote/10_ai/05_data_science_ml/386_llm_temperature/">Temperature</a> <a href="/studynote/03_network/01_data_communication/056_표본화_Sampling/">Sampling</a></strong>: P(xₜ)를 T로 나눠 재조정 -> T<1 집중, T>1 다양성
<strong>Exposure <a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/094_bias/">Bias</a></strong>: Teacher Forcing의 학습-추론 불일치 -> Scheduled Sampling으로 완화

기술사 포인트: 연쇄 법칙 분해, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 우도 최대화, 퍼플렉시티 수식을 정확히 쓰고 [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 계열과의 연관성을 설명.

- **📢 섹션 요약 비유**: Exposure Bias는 "연습 때는 선생님이 답을 알려줬는데 시험 때는 혼자 해야 하는" 괴리감이다. 실제 추론에서 모델 자신의 이전 예측 오류가 누적된다.

---

## Ⅴ. 기대효과 및 결론

자기 회귀 언어 모델의 우도 수식은 단순하지만, 그 위에 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)을 통해 [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-4, LLaMA 3, Claude 등 현대 LLM이 만들어졌다. [조건부 확률](/studynote/08_algorithm_stats/08_stats/132_conditional_probability/) 분해의 이론적 완결성과 교사 강요의 실용성이 결합된 이 방법은 사전학습의 표준이 됐다.

- **📢 섹션 요약 비유**: 자기 회귀 언어 모델은 "한 글자씩 완성되는 퍼즐"이다. 퍼즐 조각 하나하나(토큰)가 이전 조각들을 본 최선의 선택으로 놓이면서 전체 그림(문장)이 완성된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 자기 회귀 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 연쇄 법칙, [조건부 확률](/studynote/08_algorithm_stats/08_stats/132_conditional_probability/) / [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 원리 |
| [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 우도 | 교차 [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/), 최대화 / 사전학습 목표 함수 |
| 교사 강요 | Teacher Forcing, 학습 효율 / 안정적 학습 기법 |
| 퍼플렉시티 | PPL, 지수 [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/) / 언어 모델 평가 지표 |
| Beam Search | k 후보, [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 최대화 / 추론 디코딩 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| Exposure [Bias](/studynote/01_computer_architecture/02_data_representation_arithmetic/094_bias/) | 학습-추론 불일치 / AR 모델 한계 |

### 📈 관련 키워드 및 발전 흐름도

```text
[입력 표현·특징 추출] -> [LLM 자기 회귀 (Auto-Regressive) 언어 모델 우도 수식] -> [경량화·멀티모달·서비스 적용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 자기 회귀 언어 모델은 "앞 글자를 보고 다음 글자를 예측하는 빈칸 채우기 게임"을 계속하는 거야.
2. 퍼플렉시티는 모델이 "다음 단어로 몇 가지를 고민하는지"야. [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)이면 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)가지 후보 중 고민, 100이면 100가지 중 고민하는 것처럼 헷갈리는 거야.
3. 교사 강요는 연습 때 선생님이 "틀렸어, 정답은 이거야"라고 바로 고쳐줘서 빠르게 학습할 수 있게 도와주는 방법이야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 383 / 420

<- **이전**: [382. 트랜스포머 포지셔널 인코딩 (Positional Encoding) 수식](/studynote/10_ai/05_data_science_ml/382_positional_encoding_math/)
**다음**: [384. 토크나이저 BPE (Byte Pair Encoding)](/studynote/10_ai/05_data_science_ml/384_tokenizer_bpe/) ->

---
