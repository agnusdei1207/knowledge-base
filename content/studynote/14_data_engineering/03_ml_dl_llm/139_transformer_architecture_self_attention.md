---
title: 139. Transformer 아키텍처 - Self-Attention 기반 병렬 처리
date: '2026-04-19'
tags:
- studynote-dataengineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Transformer는 **RNN의 순차 처리를 Self-Attention으로 대체**하여 시퀀스 전체를 [[430_index_fast_full_scan|병렬]] 처리하는 아키텍처이며, "Attention Is All You Need"(2017, Google)에서 제안되었다.
> 2. **가치**: RNN은 시퀀스를 순차 처리하여 **[[430_index_fast_full_scan|병렬]]화 불가·[[291_long_term_dependency|장기 의존성]] 약점**이 있지만, Transformer는 **O(1) 거리로 모든 위치에 접근**하고 [[418_gpu|GPU]] [[430_index_fast_full_scan|병렬]]화가 완벽하여 대규모 학습이 가능하다.
> 3. **판단 포인트**: [[040_encoder|Encoder]]-only([[301_bert_mlm|BERT]], 이해)·[[039_decoder|Decoder]]-only([[302_gpt_autoregressive|GPT]], [[087_process_state_transition|생성]])·[[040_encoder|Encoder]]-[[039_decoder|Decoder]](T5, 번역)로 변형되며, [[299_multi_head_attention|Multi-Head Attention]]·[[300_positional_encoding|Positional Encoding]]·Feed-Forward Network가 핵심 구성이다.

---

## Ⅰ. 개요 및 필요성

```text
Transformer = Encoder + Decoder
  Encoder: [Multi-Head Self-Attention → FFN] × N
  Decoder: [Masked Self-Attention → Cross-Attention → FFN] × N
  + Positional Encoding (순서 정보)
```

- **📢 섹션 요약 비유**: RNN은 **줄 서서 한 명씩 통과(순차)**, Transformer는 **모든 사람이 동시에 대화([[430_index_fast_full_scan|병렬]])**하는 것이다.

---

## Ⅱ~Ⅴ. 결론

Transformer는 **현대 AI의 기반 아키텍처**이며, [[301_bert_mlm|BERT]]·[[302_gpt_autoregressive|GPT]]·T5·[[263_llm_large_language_model|LLM]]·ViT 모두 [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] 변형이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[246_transformer_self_attention_parallel_positional_encoding|Transformer]]** | [[124_self_attention|Self-Attention]] 기반 |
| **[[124_self_attention|Self-Attention]]** | 모든 위치 간 관련도 |
| **Multi-Head** | 다관점 Attention |
| **[[300_positional_encoding|Positional Encoding]]** | 순서 정보 주입 |
| **[[302_gpt_autoregressive|GPT]]/[[301_bert_mlm|BERT]]** | [[039_decoder|Decoder]]/[[040_encoder|Encoder]] 변형 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Seq2Seq+Attention (2014)] → [Transformer (2017, Google)]
    → [BERT (Encoder, 2018)] → [GPT-2/3 (Decoder, 2019~)]
    → [T5 (Enc-Dec, 2019)] → [GPT-4/LLM (2023~)]
    → [현재: Mamba/RWKV — Transformer 대안 탐색]
```

### 👶 어린이를 위한 3줄 비유 설명
1. RNN은 **한 줄로 서서 순서대로** 이야기를 전달해요(느림).
2. Transformer는 **모든 사람이 동시에 대화**해서 훨씬 빨라요([[430_index_fast_full_scan|병렬]]).
3. ChatGPT, [[301_bert_mlm|BERT]], 번역기 등 **거의 모든 [[190_ai_llm_requirements_specification|AI]]**가 Transformer를 사용해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 139 / 258

← **이전**: [[138_attention_mechanism_dynamic_weight|138. Attention Mechanism - 동적 가중치로 핵심 정보에 집중]]
**다음**: [[140_self_attention_multihead_positional_encoding|140. Self-Attention·Multi-Head·Positional Encoding 상세]] →

---
