+++
weight = 123
title = "123. Transformer 아키텍처 - Self-Attention 기반 병렬 시퀀스 처리"
date = "2026-04-19"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Transformer는 **순환([[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]]) 없이 Self-Attention만으로 시퀀스를 [[430_index_fast_full_scan|병렬]] 처리**하는 아키텍처이며, "Attention Is All You Need"(Vaswani, 2017)에서 제안되어 현대 AI의 **사실상 유일한 기반 아키텍처**가 되었다.
> 2. **가치**: RNN은 시퀀스를 순차 처리하여 **[[430_index_fast_full_scan|병렬]]화 불가·장거리 의존성 약화**라는 근본 한계가 있었으나, Transformer는 **모든 위치를 동시에 [[316_reference_pattern_nosql|참조]]([[124_self_attention|Self-Attention]])**하고 **[[418_gpu|GPU]] [[430_index_fast_full_scan|병렬]]화가 가능**하여 학습 속도와 [[282_performance_tactics|성능]]을 혁신적으로 개선했다.
> 3. **판단 포인트**: **[[040_encoder|인코더]]-[[039_decoder|디코더]] 구조**(기계 번역), **[[040_encoder|인코더]]만**([[301_bert_mlm|BERT]], [[104_classification_analysis|분류]]), **[[039_decoder|디코더]]만**([[302_gpt_autoregressive|GPT]], [[087_process_state_transition|생성]])의 3가지 변형을 구분하고, [[299_multi_head_attention|Multi-Head Attention]]·[[300_positional_encoding|Positional Encoding]]·Layer Normalization이 핵심 구성 요소이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Transformer 구조                                   │
├───────────────────────────────────────────────────────┤
│  [인코더 ×N]              [디코더 ×N]                 │
│  ┌──────────────┐        ┌──────────────┐            │
│  │ Multi-Head   │        │ Masked Multi-│            │
│  │ Self-Attn    │        │ Head Self-Attn│           │
│  │ + Add & Norm │        │ + Add & Norm │            │
│  │              │        │              │            │
│  │ Feed-Forward │   ──▶  │ Cross-Attn   │            │
│  │ + Add & Norm │        │ (Enc→Dec)    │            │
│  └──────────────┘        │ Feed-Forward │            │
│                          │ + Add & Norm │            │
│  + Positional Encoding   └──────────────┘            │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: RNN은 줄서기(순차 처리)이고, Transformer는 회의(모든 사람이 동시에 서로 [[316_reference_pattern_nosql|참조]], [[430_index_fast_full_scan|병렬]] 처리)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 핵심 구성 요소

| 요소 | 역할 |
|:---|:---|
| **[[124_self_attention|Self-Attention]]** | 시퀀스 내 모든 위치 상호 [[316_reference_pattern_nosql|참조]] |
| **Multi-Head** | 여러 관점에서 동시 Attention |
| **[[300_positional_encoding|Positional Encoding]]** | 순서 정보 주입 (sin/cos) |
| **Residual + LayerNorm** | 깊은 학습 안정화 |
| **Feed-[[235_forward_backward_chaining|Forward]]** | 비선형 변환 (MLP) |

### [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] 변형

| 변형 | 구성 | 대표 | 용도 |
|:---|:---|:---|:---|
| **[[040_encoder|인코더]]-[[039_decoder|디코더]]** | 둘 다 | T5 | 번역 |
| **[[040_encoder|인코더]]만** | [[040_encoder|인코더]] | **[[301_bert_mlm|BERT]]** | [[104_classification_analysis|분류]]·[[117_ner|NER]] |
| **[[039_decoder|디코더]]만** | [[039_decoder|디코더]] | **[[302_gpt_autoregressive|GPT]]** | 텍스트 [[087_process_state_transition|생성]] |

- **📢 섹션 요약 비유**: BERT는 독해 시험(양방향 이해), GPT는 작문 시험(왼→오 [[087_process_state_transition|생성]])이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]] | [[292_lstm|LSTM]] | [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] |
|:---|:---|:---|:---|
| **[[430_index_fast_full_scan|병렬]]화** | 불가 | 불가 | **가능** |
| **장거리** | 약함 | 개선 | **Self-Attn** |
| **학습 속도** | 느림 | 느림 | **빠름** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] 적용 분야
- NLP: [[301_bert_mlm|BERT]]·[[302_gpt_autoregressive|GPT]]·T5.
- Vision: ViT·DINO.
- Audio: Whisper.
- [[158_multimodal_clip_vision_audio_encoding|Multimodal]]: [[302_gpt_autoregressive|GPT]]-4V·Gemini.

---

## Ⅴ. 기대효과 및 결론

Transformer는 **현대 AI의 단일 기반 아키텍처**이며, NLP를 넘어 Vision·Audio·Multimodal까지 적용되어 [[190_ai_llm_requirements_specification|AI]] 패러다임을 완전히 바꾸었다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[124_self_attention|Self-Attention]]** | Transformer의 핵심 연산 |
| **Multi-Head** | 다관점 [[430_index_fast_full_scan|병렬]] Attention |
| **[[300_positional_encoding|Positional Encoding]]** | 순서 정보 주입 |
| **[[301_bert_mlm|BERT]]** | [[040_encoder|인코더]]만 사용 (양방향) |
| **[[302_gpt_autoregressive|GPT]]** | [[039_decoder|디코더]]만 사용 (자기 회귀) |

### 📈 관련 키워드 및 발전 흐름도

```text
[RNN / LSTM (순환, ~2016)]
    │
    ▼
[Attention (Bahdanau, 2014) — 병목 해소]
    │
    ▼
[Transformer (Vaswani, 2017) — "Attention Is All You Need"]
    │
    ▼
[BERT (2018) / GPT-2 (2019) — 사전 학습 혁명]
    │
    ▼
[현재: GPT-4 / Gemini / Claude — 거대 Transformer]
```

### 👶 어린이를 위한 3줄 비유 설명
1. RNN은 **줄서기**예요. 앞 사람이 끝나야 다음 사람이 시작하니까 느려요.
2. Transformer는 **회의**예요. 모든 사람이 **동시에 서로 이야기([[124_self_attention|Self-Attention]])**해서 빨라요.
3. ChatGPT, [[301_bert_mlm|BERT]], Gemini 모두 **[[246_transformer_self_attention_parallel_positional_encoding|Transformer]]**로 만들어졌답니다!
