---
title: "Transformer Architecture Self Attention"
date: "2026-04-19"
tags:
  - "studynote-data-engineering"
weight: 139
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Transformer는 <strong>RNN의 순차 처리를 Self-Attention으로 대체</strong>하여 시퀀스 전체를 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리하는 아키텍처이며, "Attention Is All You Need"(2017, Google)에서 제안되었다.
> 2. **가치**: RNN은 시퀀스를 순차 처리하여 <strong><a href="/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a>화 불가·<a href="/studynote/10_ai/04_ai_ops_ethics/291_long_term_dependency/">장기 의존성</a> 약점</strong>이 있지만, Transformer는 <strong>O(1) 거리로 모든 위치에 접근</strong>하고 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화가 완벽하여 대규모 학습이 가능하다.
> 3. **판단 포인트**: [Encoder](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)-only([BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/), 이해)·[Decoder](/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)-only([GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/), [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/))·[Encoder](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)-[Decoder](/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)(T5, 번역)로 변형되며, [Multi-Head Attention](/studynote/10_ai/04_ai_ops_ethics/299_multi_head_attention/)·[Positional Encoding](/studynote/10_ai/04_ai_ops_ethics/300_positional_encoding/)·Feed-Forward Network가 핵심 구성이다.

---

## Ⅰ. 개요 및 필요성

```text
Transformer = Encoder + Decoder
  Encoder: [Multi-Head Self-Attention -> FFN] × N
  Decoder: [Masked Self-Attention -> Cross-Attention -> FFN] × N
  + Positional Encoding (순서 정보)
```

- **📢 섹션 요약 비유**: RNN은 **줄 서서 한 명씩 통과(순차)**, Transformer는 <strong>모든 사람이 동시에 대화(<a href="/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a>)</strong>하는 것이다.

---

## Ⅱ~Ⅴ. 결론

Transformer는 <strong>현대 AI의 기반 아키텍처</strong>이며, [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)·[GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)·T5·[LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)·ViT 모두 [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 변형이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/">Transformer</a></strong> | [Self-Attention](/studynote/10_ai/02_dl_architecture_new/124_self_attention/) 기반 |
| <strong><a href="/studynote/10_ai/02_dl_architecture_new/124_self_attention/">Self-Attention</a></strong> | 모든 위치 간 관련도 |
| **Multi-Head** | 다관점 Attention |
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/300_positional_encoding/">Positional Encoding</a></strong> | 순서 정보 주입 |
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/">GPT</a>/<a href="/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/">BERT</a></strong> | [Decoder](/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)/[Encoder](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/) 변형 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Seq2Seq+Attention (2014)] -> [Transformer (2017, Google)]
    -> [BERT (Encoder, 2018)] -> [GPT-2/3 (Decoder, 2019~)]
    -> [T5 (Enc-Dec, 2019)] -> [GPT-4/LLM (2023~)]
    -> [현재: Mamba/RWKV — Transformer 대안 탐색]
```

### 👶 어린이를 위한 3줄 비유 설명
1. RNN은 **한 줄로 서서 순서대로** 이야기를 전달해요(느림).
2. Transformer는 <strong>모든 사람이 동시에 대화</strong>해서 훨씬 빨라요([병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)).
3. ChatGPT, [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/), 번역기 등 <strong>거의 모든 <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a></strong>가 Transformer를 사용해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 139 / 258

<- **이전**: [138. Attention Mechanism - 동적 가중치로 핵심 정보에 집중](/studynote/14_data_engineering/03_ml_dl_llm/138_attention_mechanism_dynamic_weight/)
**다음**: [140. Self-Attention·Multi-Head·Positional Encoding 상세](/studynote/14_data_engineering/03_ml_dl_llm/140_self_attention_multihead_positional_encoding/) ->

---
