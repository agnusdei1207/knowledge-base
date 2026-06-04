---
title: "136. RNN (Recurrent Neural Network) - 순환 신경망과 시퀀스 처리"
date: "2026-04-19"
tags:
  - "studynote-dataengineering"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: RNN은 <strong>은닉 상태(Hidden <a href="/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/">State</a>)를 이전 시점에서 현재 시점으로 순환(Recurrence)하여 시퀀스 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>(텍스트·시계열·음성)의 순서 의존성을 학습</strong>하는 신경망이다.
> 2. **가치**: CNN은 공간 패턴, RNN은 <strong>시간 패턴</strong>을 처리하며, 기계 번역·음성 인식·시계열 예측의 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 핵심 아키텍처였다. 단, [장기 의존성](/studynote/10_ai/04_ai_ops_ethics/291_long_term_dependency/)([Long-term Dependency](/studynote/10_ai/04_ai_ops_ethics/291_long_term_dependency/))에 취약하다.
> 3. **판단 포인트**: Vanilla RNN의 [Vanishing Gradient](/studynote/14_data_engineering/05_exam_keywords/240_relu_vanishing_gradient_softmax_backprop_chain/) -> [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/)/GRU가 해결 -> 현재는 <strong>Transformer가 RNN을 거의 대체</strong>했으나, 시계열·온디바이스에서는 여전히 사용된다.

---

## Ⅰ. 개요 및 필요성

```text
RNN: h_t = f(W·h_{t-1} + U·x_t)
  h_t: 현재 은닉 상태 (이전 정보 보유)
  장점: 가변 길이 시퀀스 처리
  단점: 장기 의존성 학습 어려움 (Vanishing Gradient)
```

- **📢 섹션 요약 비유**: RNN은 **일기장을 읽으며 기억하는** 것이다. 과거 일기(은닉 상태)를 참고하여 오늘을 이해한다.

---

## Ⅱ~Ⅴ. 결론

RNN은 <strong>시퀀스 처리의 기초 아키텍처</strong>이며, [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/)/GRU를 거쳐 Transformer로 진화했다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/">RNN</a></strong> | 순환 은닉 상태 |
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/292_lstm/">LSTM</a></strong> | [장기 의존성](/studynote/10_ai/04_ai_ops_ethics/291_long_term_dependency/) 해결 |
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/294_gru/">GRU</a></strong> | [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/) 경량화 |
| <strong><a href="/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/">Transformer</a></strong> | [RNN](/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/) 대체 ([병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)) |
| **시계열** | [RNN](/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/) 여전히 활용 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Vanilla RNN (1986)] -> [LSTM (1997)] -> [GRU (2014)]
    -> [Seq2Seq + Attention (2014)]
    -> [Transformer (2017) — RNN 대체]
    -> [현재: Mamba/RWKV — RNN 르네상스 (선형)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. RNN은 **일기장을 읽는** 것이에요. 어제 일기(은닉 상태)를 참고해서 <strong>오늘을 이해</strong>해요.
2. 하지만 <strong>오래된 일기(장기 기억)</strong>는 잘 기억 못 해요(Vanishing).
3. LSTM은 <strong>중요한 일기에 포스트잇</strong>을 붙여서 잊지 않게 해줘요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 136 / 258

<- **이전**: [135. CNN (Convolutional Neural Network) - 합성곱 신경망의 구조와 원리](/studynote/14_data_engineering/03_ml_dl_llm/135_cnn_convolutional_neural_network/)
**다음**: [137. LSTM & GRU - 장기 의존성을 해결한 순환 신경망](/studynote/14_data_engineering/03_ml_dl_llm/137_lstm_gru_long_short_term_memory/) ->

---
