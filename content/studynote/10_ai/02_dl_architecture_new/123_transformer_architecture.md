---
title: "123. Transformer Architecture"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 123
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Transformer는 <strong>순환(<a href="/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/">RNN</a>) 없이 Self-Attention만으로 시퀀스를 <a href="/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a> 처리</strong>하는 아키텍처이며, "Attention Is All You Need"(Vaswani, 2017)에서 제안되어 현대 AI의 <strong>사실상 유일한 기반 아키텍처</strong>가 되었다.
> 2. **가치**: RNN은 시퀀스를 순차 처리하여 <strong><a href="/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a>화 불가·장거리 의존성 약화</strong>라는 근본 한계가 있었으나, Transformer는 <strong>모든 위치를 동시에 <a href="/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">참조</a>(<a href="/studynote/10_ai/02_dl_architecture_new/124_self_attention/">Self-Attention</a>)</strong>하고 <strong><a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/">GPU</a> <a href="/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a>화가 가능</strong>하여 학습 속도와 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 혁신적으로 개선했다.
> 3. **판단 포인트**: <strong><a href="/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/">인코더</a>-<a href="/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/">디코더</a> 구조</strong>(기계 번역), <strong><a href="/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/">인코더</a>만</strong>([BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/), [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)), <strong><a href="/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/">디코더</a>만</strong>([GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/), [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/))의 3가지 변형을 구분하고, [Multi-Head Attention](/studynote/10_ai/04_ai_ops_ethics/299_multi_head_attention/)·[Positional Encoding](/studynote/10_ai/04_ai_ops_ethics/300_positional_encoding/)·Layer Normalization이 핵심 구성 요소이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Transformer 구조                                   |
+-------------------------------------------------------+
|  [인코더 ×N]              [디코더 ×N]                 |
|  +--------------+        +--------------+            |
|  | Multi-Head   |        | Masked Multi-|            |
|  | Self-Attn    |        | Head Self-Attn|           |
|  | + Add & Norm |        | + Add & Norm |            |
|  |              |        |              |            |
|  | Feed-Forward |   --->  | Cross-Attn   |            |
|  | + Add & Norm |        | (Enc->Dec)    |            |
|  +--------------+        | Feed-Forward |            |
|                          | + Add & Norm |            |
|  + Positional Encoding   +--------------+            |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: RNN은 줄서기(순차 처리)이고, Transformer는 회의(모든 사람이 동시에 서로 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/), [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 핵심 구성 요소

| 요소 | 역할 |
|:---|:---|
| <strong><a href="/studynote/10_ai/02_dl_architecture_new/124_self_attention/">Self-Attention</a></strong> | 시퀀스 내 모든 위치 상호 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) |
| **Multi-Head** | 여러 관점에서 동시 Attention |
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/300_positional_encoding/">Positional Encoding</a></strong> | 순서 정보 주입 (sin/cos) |
| **Residual + LayerNorm** | 깊은 학습 안정화 |
| <strong>Feed-<a href="/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/">Forward</a></strong> | 비선형 변환 (MLP) |

### [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 변형

| 변형 | 구성 | 대표 | 용도 |
|:---|:---|:---|:---|
| <strong><a href="/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/">인코더</a>-<a href="/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/">디코더</a></strong> | 둘 다 | T5 | 번역 |
| <strong><a href="/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/">인코더</a>만</strong> | [인코더](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/) | <strong><a href="/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/">BERT</a></strong> | [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)·[NER](/studynote/16_bigdata/05_analysis/117_ner/) |
| <strong><a href="/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/">디코더</a>만</strong> | [디코더](/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) | <strong><a href="/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/">GPT</a></strong> | 텍스트 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |

- **📢 섹션 요약 비유**: BERT는 독해 시험(양방향 이해), GPT는 작문 시험(왼->오 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/))이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [RNN](/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/) | [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/) | [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) |
|:---|:---|:---|:---|
| <strong><a href="/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a>화</strong> | 불가 | 불가 | **가능** |
| **장거리** | 약함 | 개선 | **Self-Attn** |
| **학습 속도** | 느림 | 느림 | **빠름** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 적용 분야
- NLP: [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)·[GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)·T5.
- Vision: ViT·DINO.
- Audio: Whisper.
- [Multimodal](/studynote/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding/): [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-4V·Gemini.

---

## Ⅴ. 기대효과 및 결론

Transformer는 <strong>현대 AI의 단일 기반 아키텍처</strong>이며, NLP를 넘어 Vision·Audio·Multimodal까지 적용되어 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 패러다임을 완전히 바꾸었다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/10_ai/02_dl_architecture_new/124_self_attention/">Self-Attention</a></strong> | Transformer의 핵심 연산 |
| **Multi-Head** | 다관점 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) Attention |
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/300_positional_encoding/">Positional Encoding</a></strong> | 순서 정보 주입 |
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/">BERT</a></strong> | [인코더](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)만 사용 (양방향) |
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/">GPT</a></strong> | [디코더](/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)만 사용 (자기 회귀) |

### 📈 관련 키워드 및 발전 흐름도

```text
[RNN / LSTM (순환, ~2016)]
    |
    v
[Attention (Bahdanau, 2014) — 병목 해소]
    |
    v
[Transformer (Vaswani, 2017) — "Attention Is All You Need"]
    |
    v
[BERT (2018) / GPT-2 (2019) — 사전 학습 혁명]
    |
    v
[현재: GPT-4 / Gemini / Claude — 거대 Transformer]
```

### 👶 어린이를 위한 3줄 비유 설명
1. RNN은 <strong>줄서기</strong>예요. 앞 사람이 끝나야 다음 사람이 시작하니까 느려요.
2. Transformer는 <strong>회의</strong>예요. 모든 사람이 <strong>동시에 서로 이야기(<a href="/studynote/10_ai/02_dl_architecture_new/124_self_attention/">Self-Attention</a>)</strong>해서 빨라요.
3. ChatGPT, [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/), Gemini 모두 <strong><a href="/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/">Transformer</a></strong>로 만들어졌답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 123 / 420

<- **이전**: [122. Q·K·V 시스템 (Query·Key·Value) - Attention의 핵심 연산 구조](/studynote/10_ai/02_dl_architecture_new/122_qkv_system/)
**다음**: [124. Self-Attention (자기 주의 메커니즘) - 시퀀스 내 모든 위치 상호 참조](/studynote/10_ai/02_dl_architecture_new/124_self_attention/) ->

---
