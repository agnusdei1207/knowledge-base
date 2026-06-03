---
title: 137. LSTM & GRU - 장기 의존성을 해결한 순환 신경망
date: '2026-04-19'
tags:
- studynote-dataengineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[292_lstm|LSTM]]([[292_lstm|Long Short-Term Memory]])은 **Forget·Input·Output 3개의 게이트로 셀 상태(Cell [[272_state_pattern|State]])를 제어**하여 Vanilla RNN의 [[291_long_term_dependency|장기 의존성]]([[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]]) 문제를 해결한 순환 신경망이며, GRU는 LSTM을 **2개 게이트(Reset·Update)로 단순화**한 경량 변형이다.
> 2. **가치**: RNN은 "어제 비가 왔다"는 기억하지만 "한 달 전 비가 왔다"는 잊지만, LSTM은 **중요한 정보를 셀 상태에 장기 보존**하여 먼 과거의 맥락도 활용한다.
> 3. **판단 포인트**: 성능은 [[292_lstm|LSTM]]≈GRU이나 GRU가 파라미터가 적어(학습 빠름) 소규모 데이터에 유리하며, 현재는 **Transformer가 대부분 대체**했으나 시계열·온디바이스에서 여전히 사용된다.

---

## Ⅰ. 개요 및 필요성

```text
LSTM 3 Gate:
  Forget: 어떤 정보를 버릴지 (sigmoid)
  Input:  어떤 정보를 저장할지 (sigmoid × tanh)
  Output: 어떤 정보를 출력할지 (sigmoid)
  Cell State: 정보 고속도로 (장기 기억)

GRU 2 Gate: Reset + Update (LSTM 단순화)
```

- **📢 섹션 요약 비유**: LSTM은 **포스트잇 붙은 일기장**이다. 중요한 페이지에 포스트잇(Gate)을 붙여서 잊지 않는다.

---

## Ⅱ~Ⅴ. 결론

[[292_lstm|LSTM]]/GRU는 **시퀀스 모델링의 중요한 이정표**이며, [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] 이전의 NLP·음성·시계열 핵심 아키텍처였다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[292_lstm|LSTM]]** | 3 Gate + Cell [[272_state_pattern|State]] |
| **[[294_gru|GRU]]** | 2 Gate (경량) |
| **Cell [[272_state_pattern|State]]** | 장기 기억 고속도로 |
| **[[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]]** | [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]] 문제 → [[292_lstm|LSTM]] 해결 |
| **[[246_transformer_self_attention_parallel_positional_encoding|Transformer]]** | [[292_lstm|LSTM]] 대체 ([[430_index_fast_full_scan|병렬]]) |

### 📈 관련 키워드 및 발전 흐름도

```text
[Vanilla RNN (1986)] → [LSTM (Hochreiter, 1997)]
    → [GRU (Cho, 2014)] → [Seq2Seq+Attention (2014)]
    → [Transformer (2017) — LSTM 대체]
    → [현재: xLSTM/Mamba — LSTM 르네상스]
```

### 👶 어린이를 위한 3줄 비유 설명
1. LSTM은 **포스트잇 붙은 일기장**이에요. 중요한 페이지를 **잊지 않아요**.
2. RNN은 옛날 일기를 잊지만, LSTM은 **포스트잇(Gate) 덕분에 기억**해요.
3. GRU는 **포스트잇을 2개만 쓰는** 간단한 버전이에요!
