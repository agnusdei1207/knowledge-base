+++
title = "121. 어텐션 메커니즘 (Attention Mechanism) - Seq2Seq 병목 해소·가중 컨텍스트"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Attention은 [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)가 출력을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)할 때, [인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)의 **모든 Hidden State에 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)(Attention [Weight](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/))를 부여하여 동적으로 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)**하는 메커니즘으로, 고정 [컨텍스트 벡터](/knowledge-base/studynote/10_ai/02_dl_architecture_new/120_context_vector/)의 정보 병목을 해소한다.
> 2. **가치**: "I love you" → "나는 너를 사랑해" 번역 시, "사랑해"를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)할 때 **"love"에 높은 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)**를 부여하여 해당 입력에 "주목(Attend)"한다. 이로써 긴 문장에서도 정보 손실 없이 정확한 번역이 가능해진다.
> 3. **판단 포인트**: Bahdanau(Additive) Attention과 Luong(Multiplicative/[Dot](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/519_dot_dns_over_tls/)-product) Attention을 구분하고, [Self-Attention](/knowledge-base/studynote/10_ai/02_dl_architecture_new/124_self_attention/)([Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/))으로의 진화를 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Attention 동작 과정                                │
├───────────────────────────────────────────────────────┤
│  인코더: h₁(I), h₂(love), h₃(you)                   │
│                                                       │
│  디코더 t=3 ("사랑해" 생성):                          │
│   1. s₃(디코더 상태)와 h₁,h₂,h₃ 유사도 계산         │
│   2. e₃₁=score(s₃,h₁), e₃₂=score(s₃,h₂)...        │
│   3. α = softmax([e₃₁, e₃₂, e₃₃])                  │
│      = [0.1, 0.8, 0.1]  ← "love"에 집중!            │
│   4. c₃ = 0.1·h₁ + 0.8·h₂ + 0.1·h₃ (가중 합)       │
│   5. 출력 = f(s₃, c₃) → "사랑해"                    │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Attention은 시험 중 **전체 교과서를 보면서** 문제에 관련된 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)에 **형광펜을 칠하는** 것이다. 관련 높은 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)일수록 밝게 칠한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Attention 유형

| 유형 | Score 함수 | 특징 |
|:---|:---|:---|
| **Bahdanau (Additive)** | v^T · [tanh](/knowledge-base/studynote/10_ai/01_ai_basics/070_hyperbolic_tangent_tanh_activation/)(W[s;h]) | 학습 파라미터 많음 |
| **Luong ([Dot](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/519_dot_dns_over_tls/)-product)** | s^T · h | **효율적, 빠름** |
| **Scaled [Dot](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/519_dot_dns_over_tls/)-product** | (Q·K^T)/√d_k | **[Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 표준** |

### Cross-Attention vs [Self-Attention](/knowledge-base/studynote/10_ai/02_dl_architecture_new/124_self_attention/)

| 비교 | Cross-Attention | [Self-Attention](/knowledge-base/studynote/10_ai/02_dl_architecture_new/124_self_attention/) |
|:---|:---|:---|
| **Q** | [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) | **같은 시퀀스** |
| **K, V** | [인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/) | **같은 시퀀스** |
| **대표** | [Seq2Seq](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/245_seq2seq_context_vector_attention_dynamic_weight/) Attention | **[Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)** |

- **📢 섹션 요약 비유**: Cross-Attention은 번역가가 원문을 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하는 것이고, Self-Attention은 글 쓸 때 자기 문장 앞뒤를 돌아보는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 고정 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) | Attention | [Self-Attention](/knowledge-base/studynote/10_ai/02_dl_architecture_new/124_self_attention/) |
|:---|:---|:---|:---|
| **[참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)** | 마지막 h만 | **모든 h** | **자기 시퀀스** |
| **[병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화** | 불가 | 불가 | **가능** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### Attention의 해석 가능성
- Attention [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)하면 "모델이 어디를 보고 판단했는지" [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 가능 → 설명 가능 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)([XAI](/knowledge-base/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/))의 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 형태.

---

## Ⅴ. 기대효과 및 결론

Attention은 **현대 AI의 가장 중요한 단일 아이디어**이며, [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)·[BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)·[GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)·ViT·Diffusion 등 거의 모든 최신 모델의 기반이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Bahdanau Attention** | Additive Score, 2014 |
| **Luong Attention** | [Dot](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/519_dot_dns_over_tls/)-product Score, 2015 |
| **[Self-Attention](/knowledge-base/studynote/10_ai/02_dl_architecture_new/124_self_attention/)** | Transformer의 핵심 |
| **[Multi-Head Attention](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/299_multi_head_attention/)** | 여러 관점에서 Attention |
| **Cross-Attention** | [인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)-[디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) Attention |

### 📈 관련 키워드 및 발전 흐름도

```text
[Seq2Seq 고정 컨텍스트 벡터 (2014)]
    │
    ▼
[Bahdanau Attention (2014) — Additive]
    │
    ▼
[Luong Attention (2015) — Dot-product]
    │
    ▼
[Self-Attention + Transformer (2017) — "Attention Is All You Need"]
    │
    ▼
[현재: Flash Attention / Linear Attention — 효율적 Attention]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Attention은 시험 중 **교과서 전체를 보면서** 문제와 관련된 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)에 **형광펜**을 치는 거예요.
2. 관련 높은 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 **밝게**, 관련 낮은 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 **약하게** 칠해요.
3. 이 아이디어가 너무 좋아서 **ChatGPT([Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/))의 핵심 기술**이 되었답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 121 / 420

← **이전**: [120. 컨텍스트 벡터 (Context Vector) - Seq2Seq 병목과 Attention의 동기](/knowledge-base/studynote/10_ai/02_dl_architecture_new/120_context_vector/)
**다음**: [122. Q·K·V 시스템 (Query·Key·Value) - Attention의 핵심 연산 구조](/knowledge-base/studynote/10_ai/02_dl_architecture_new/122_qkv_system/) →

---
