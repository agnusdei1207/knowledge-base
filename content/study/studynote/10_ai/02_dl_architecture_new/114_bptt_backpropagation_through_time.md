+++
weight = 114
title = "114. BPTT (Backpropagation Through Time) - 시간 축 역전파와 Truncated BPTT"
date = "2026-04-19"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: BPTT([[272_backpropagation|Backpropagation]] Through Time)는 RNN의 순환 구조를 **시간 축으로 펼친(Unfolding) 후 일반 [[272_backpropagation|역전파]]를 적용**하는 학습 [[001_algorithm_definition|알고리즘]]이며, 펼친 길이 T에 비례하여 $O(T)$의 시간·메모리 비용이 발생한다.
> 2. **가치**: 시퀀스 길이 T가 길수록 과거 정보를 반영할 수 있지만, [[088_vanishing_gradient_relu_skip_connection|기울기 소실]]/폭발이 심해지고 메모리가 폭발하므로 실무에서는 **Truncated BPTT(일정 길이 k로 잘라서 [[272_backpropagation|역전파]])**를 사용한다.
> 3. **판단 포인트**: Truncated BPTT의 절단 길이 k는 "기억 범위"를 결정하며, k가 너무 작으면 [[291_long_term_dependency|장기 의존성]] 학습 실패, 너무 크면 메모리/시간 비용 폭발이라는 트레이드오프가 존재한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    BPTT: 시간 축 펼침 후 역전파                       │
├───────────────────────────────────────────────────────┤
│  [RNN 순환 구조]        [시간 축 펼침 (Unfolding)]    │
│   ┌──▶ h ──┐            h₁ → h₂ → h₃ → h₄          │
│   │   │    │            ↑    ↑    ↑    ↑             │
│   └── x ───┘            x₁   x₂   x₃   x₄          │
│                                                       │
│  역전파: L → h₄ → h₃ → h₂ → h₁ (시간 역방향)       │
│  기울기: ∂L/∂W = Σ(∂L/∂h_t × ∂h_t/∂W)              │
│                                                       │
│  문제: T=1000이면 h₁까지 1000단계 역전파 → 폭발/소실 │
│  해결: Truncated BPTT (k=20으로 잘라서 역전파)       │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: BPTT는 1000페이지 소설을 처음부터 끝까지 형광펜(기울기)으로 표시하는 것이고, Truncated BPTT는 20페이지씩 끊어서 표시하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Full BPTT vs Truncated BPTT

| 항목 | Full BPTT | Truncated BPTT |
|:---|:---|:---|
| **[[272_backpropagation|역전파]] 범위** | 전체 시퀀스 T | **k 스텝만** |
| **메모리** | $O(T)$ | $O(k)$ |
| **[[291_long_term_dependency|장기 의존성]]** | 이론적 가능 (소실 문제) | k 이내만 |
| **실무** | 짧은 시퀀스만 | **대부분 사용** |

- **📢 섹션 요약 비유**: Full BPTT는 1년 치 일기를 한번에 복습하는 것이고, Truncated BPTT는 최근 20일치만 복습하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | BPTT ([[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]]) | 일반 [[272_backpropagation|역전파]] ([[696_fibre_channel_protocol|FC]]/[[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]]) |
|:---|:---|:---|
| **축** | 시간 축 (T 단계) | 레이어 축 (L 층) |
| **[[267_weight_bias_activation|가중치]] 공유** | **$W_h$ 모든 시간 단계에서 공유** | 레이어별 독립 |
| **기울기 누적** | 시간 단계별 기울기 합산 | 레이어별 계산 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### Truncated BPTT [[009_config|설정]] 가이드
- **k = 20~50**: 일반 NLP·음성 [[150_task|태스크]].
- **k = 100~200**: 장거리 의존성이 중요한 [[150_task|태스크]] (음악 [[087_process_state_transition|생성]]).
- **[[292_lstm|LSTM]] + k = 35**: PyTorch 기본 언어 모델 [[009_config|설정]].

---

## Ⅴ. 기대효과 및 결론

BPTT는 [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]] 학습의 유일한 방법이었으나, Transformer의 Self-Attention은 시간 축 펼침이 불필요하여 BPTT 자체가 필요 없다. 하지만 실시간 스트리밍·엣지 환경에서 [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]]/LSTM이 여전히 사용되므로 BPTT의 원리 이해는 필수다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[272_backpropagation|역전파]] ([[272_backpropagation|Backpropagation]])** | BPTT의 기반 [[001_algorithm_definition|알고리즘]] |
| **[[088_vanishing_gradient_relu_skip_connection|기울기 소실]]/폭발** | BPTT에서 T가 클 때 발생하는 문제 |
| **Truncated BPTT** | 메모리·기울기 문제 해결을 위한 절단 기법 |
| **[[292_lstm|LSTM]]** | BPTT의 [[088_vanishing_gradient_relu_skip_connection|기울기 소실]]을 게이트로 완화 |
| **[[246_transformer_self_attention_parallel_positional_encoding|Transformer]]** | BPTT 불필요, Self-Attention으로 [[430_index_fast_full_scan|병렬]] 학습 |

### 📈 관련 키워드 및 발전 흐름도

```text
[역전파 (1986, Rumelhart) — FC 네트워크 학습]
    │
    ▼
[BPTT (1990, Werbos) — RNN 시간 축 역전파]
    │
    ▼
[Truncated BPTT — 실무 메모리·기울기 제어]
    │
    ▼
[LSTM (1997) — 기울기 소실 완화, BPTT 효과 극대화]
    │
    ▼
[Transformer (2017) — BPTT 불필요, 병렬 학습]
```

### 👶 어린이를 위한 3줄 비유 설명
1. BPTT는 1000페이지 소설을 읽고 **처음부터 끝까지 형광펜**으로 중요한 부분을 표시하는 거예요.
2. 하지만 너무 길면 힘들어서, **최근 20페이지만 표시**(Truncated)하는 방법을 써요.
3. Transformer는 아예 소설 전체를 **한눈에 보는 초능력**이 있어서 형광펜이 필요 없답니다!
