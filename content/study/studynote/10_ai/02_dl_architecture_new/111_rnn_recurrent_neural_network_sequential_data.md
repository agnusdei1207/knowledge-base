+++
weight = 111
title = "111. 순환 신경망 (RNN, Recurrent Neural Network) - 시퀀스 데이터와 기울기 소실"
date = "2026-04-19"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]]([[244_rnn_time_series_lstm_cell_gate_long_term_dependency|Recurrent Neural Network]])은 은닉 상태(Hidden [[272_state_pattern|State]])를 **이전 시간 단계에서 다음 시간 단계로 [[014_recursion|재귀]]적으로 전달**하여, 시계열·텍스트·음성 같은 **순서가 중요한 시퀀스(Sequence) [[001_dikw_pyramid|데이터]]**를 처리하는 신경망이다.
> 2. **가치**: CNN이 공간(이미지)을 보는 눈이라면, RNN은 시간 축(과거→현재→미래)을 따라 **문맥([[033_context|Context]])을 기억**하는 기억력이며, 기계 번역·음성 인식·주가 예측의 기초가 되었다.
> 3. **판단 포인트**: 바닐라 RNN은 **[[088_vanishing_gradient_relu_skip_connection|기울기 소실]]([[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]])** 문제로 [[291_long_term_dependency|장기 의존성]]([[291_long_term_dependency|Long-term Dependency]])을 학습하지 못하며, 이를 해결한 **[[292_lstm|LSTM]]·[[294_gru|GRU]]**가 사실상 표준이었고, 현재는 **[[246_transformer_self_attention_parallel_positional_encoding|Transformer]]([[124_self_attention|Self-Attention]])**가 대부분의 시퀀스 [[150_task|태스크]]를 지배한다.

---

## Ⅰ. 개요 및 필요성

CNN과 [[696_fibre_channel_protocol|FC]](완전 연결) 네트워크는 입력 순서를 무시한다. "나는 학교에 간다"와 "간다 학교에 나는"을 같은 것으로 본다. 하지만 언어·음악·주가는 **순서가 의미를 결정**한다.

```text
┌───────────────────────────────────────────────────────┐
│      RNN의 시간 축 펼침 (Unfolding)                    │
├───────────────────────────────────────────────────────┤
│  x₁ ──▶ [h₁] ──▶ x₂ ──▶ [h₂] ──▶ x₃ ──▶ [h₃]     │
│          │               │               │            │
│          ▼               ▼               ▼            │
│          y₁              y₂              y₃           │
│                                                       │
│  h_t = f(W_h · h_{t-1} + W_x · x_t + b)             │
│  이전 기억(h_{t-1}) + 현재 입력(x_t) → 새 기억(h_t)  │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: RNN은 소설을 읽는 독자다. 1장에서 읽은 내용(h₁)을 기억하고 2장을 읽어야(x₂) 줄거리를 이해한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[088_vanishing_gradient_relu_skip_connection|기울기 소실]] 문제 ([[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]])

RNN을 100 시간 단계로 펼치면, [[272_backpropagation|역전파]] 시 기울기가 $W_h$를 100번 곱하면서 **0에 수렴(소실)하거나 ∞로 폭발**한다. 결과적으로 "100 단어 전에 나온 주어"를 현재 동사와 연결하지 못한다.

| 문제 | 원인 | 해결 모델 |
|:---|:---|:---|
| **[[088_vanishing_gradient_relu_skip_connection|기울기 소실]]** | $\|W_h\| < 1$의 반복 곱셈 | [[292_lstm|LSTM]] (게이트로 기울기 [[571_protection_vs_security|보호]]) |
| **[[089_exploding_gradient_clipping|기울기 폭발]]** | $\|W_h\| > 1$의 반복 곱셈 | Gradient [[389_ppo_proximal_policy_optimization|Clipping]] |
| **[[291_long_term_dependency|장기 의존성]] 실패** | 소실의 직접적 결과 | [[294_gru|GRU]] (간소화 [[292_lstm|LSTM]]) |

### [[292_lstm|LSTM]] vs [[294_gru|GRU]]

| 항목 | [[292_lstm|LSTM]] | [[294_gru|GRU]] |
|:---|:---|:---|
| **게이트** | 3개 (Forget·Input·Output) | 2개 (Reset·Update) |
| **파라미터** | 많음 | 적음 |
| **[[282_performance_tactics|성능]]** | 약간 우수 (긴 시퀀스) | 비슷 (짧은 시퀀스에서 효율적) |
| **설계 철학** | 기억 [[571_protection_vs_security|보호]]에 충실 | 간소화·속도 우선 |

- **📢 섹션 요약 비유**: 바닐라 RNN은 메모지에 연필로 적는 것(쉽게 지워짐)이고, LSTM은 중요한 내용을 금고(Cell [[272_state_pattern|State]])에 넣고 열쇠(게이트)로 [[571_protection_vs_security|보호]]하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]] | [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] | [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] |
|:---|:---|:---|:---|
| **강점** | 시간 축 처리 | 공간 축 처리 | 시간+공간 [[430_index_fast_full_scan|병렬]] |
| **약점** | [[291_long_term_dependency|장기 의존성]], 순차 연산 | 순서 무시 | 연산 비용 높음 |
| **[[430_index_fast_full_scan|병렬]]화** | 불가 (순차) | 가능 | **완전 가능** |
| **대표 모델** | [[292_lstm|LSTM]], [[294_gru|GRU]] | [[287_resnet_skip_connection|ResNet]] | [[302_gpt_autoregressive|GPT]], [[301_bert_mlm|BERT]] |
| **현재 위치** | 레거시 (대부분 대체) | 비전 주력 | **NLP·시퀀스 지배** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]] 계열이 아직 유효한 영역
1. **실시간 스트리밍**: 센서 [[001_dikw_pyramid|데이터]]가 1개씩 들어오는 온라인 추론 (메모리 효율).
2. **경량 엣지 디바이스**: [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] 대비 파라미터가 적어 MCU에서 추론 가능.

### Transformer로 대체된 영역
- 기계 번역, 텍스트 [[087_process_state_transition|생성]], 음성 인식 → **[[246_transformer_self_attention_parallel_positional_encoding|Transformer]] ([[124_self_attention|Self-Attention]])** 압도적 우위.

---

## Ⅴ. 기대효과 및 결론

RNN은 시퀀스 [[001_dikw_pyramid|데이터]] 처리의 **역사적 토대**이며, [[292_lstm|LSTM]]·GRU의 게이트 메커니즘은 Transformer의 Attention 설계에 영감을 주었다. 현재는 대부분의 시퀀스 [[150_task|태스크]]에서 Transformer로 대체되었지만, 실시간 스트리밍·경량 엣지 환경에서는 여전히 유효하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[292_lstm|LSTM]]** | RNN의 [[088_vanishing_gradient_relu_skip_connection|기울기 소실]] 해결, 3-게이트 구조 |
| **[[294_gru|GRU]]** | [[292_lstm|LSTM]] 간소화, 2-게이트 |
| **[[088_vanishing_gradient_relu_skip_connection|기울기 소실]]** | RNN의 근본적 한계 |
| **[[246_transformer_self_attention_parallel_positional_encoding|Transformer]]** | RNN을 대체한 [[124_self_attention|Self-Attention]] 기반 모델 |
| **[[245_seq2seq_context_vector_attention_dynamic_weight|Seq2Seq]]** | [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]] [[040_encoder|인코더]]-[[039_decoder|디코더]] 구조, 기계 번역의 기초 |

### 📈 관련 키워드 및 발전 흐름도

```text
[바닐라 RNN (1986, Elman) — 시퀀스 처리의 시작]
    │
    ▼
[LSTM (1997, Hochreiter) — 기울기 소실 해결, 게이트 도입]
    │
    ▼
[GRU (2014, Cho) — LSTM 간소화]
    │
    ▼
[Seq2Seq + Attention (2015, Bahdanau) — 기계 번역 혁신]
    │
    ▼
[Transformer (2017, Vaswani) — Self-Attention, RNN 대체]
```

### 👶 어린이를 위한 3줄 비유 설명
1. RNN은 소설을 1장씩 읽으면서 **앞 내용을 기억**하고 다음 장을 이해하는 뇌예요.
2. 문제는 소설이 너무 길면 **1장 내용을 잊어버리는 건망증([[088_vanishing_gradient_relu_skip_connection|기울기 소실]])**이 있어요.
3. LSTM은 중요한 내용을 **금고에 넣어서 잊지 않게** 해주고, Transformer는 아예 소설 전체를 한눈에 보는 초능력이에요!
