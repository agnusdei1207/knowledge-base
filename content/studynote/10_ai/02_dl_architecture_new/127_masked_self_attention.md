---
title: "127. Masked Self Attention"
date: "2026-04-19"
tags:
  - "studynote-ai"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Masked Self-Attention은 <strong><a href="/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/">디코더</a>에서 현재 위치 이후의 미래 토큰을 <a href="/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">참조</a>하지 못하도록 <a href="/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/">마스</a>킹(-∞)하는 <a href="/studynote/10_ai/02_dl_architecture_new/124_self_attention/">Self-Attention</a></strong>이며, [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 등 자기 회귀([Autoregressive](/studynote/14_data_engineering/05_exam_keywords/248_bert_encoder_mlm_gpt_decoder_autoregressive_comparison/)) 모델의 핵심 메커니즘이다.
> 2. **가치**: "I love"까지 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 후 다음 토큰을 예측할 때, 정답인 "you"를 이미 본 상태에서 예측하면 <strong>학습이 무의미(<a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">data</a> leakage)</strong>하므로, Masked Self-Attention이 미래를 가려서 <strong>진정한 예측</strong>을 가능하게 한다.
> 3. **판단 포인트**: Causal Mask(하삼각 행렬)를 Attention Score에 적용하여 미래 위치에 -∞를 더하고 [softmax](/studynote/10_ai/03_llm_nlp/270_softmax/) 후 0이 되게 하며, [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)(양방향)는 [마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹 없이 전체 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Masked Self-Attention                              |
+-------------------------------------------------------+
|  입력: "I love you <EOS>"                             |
|                                                       |
|  Attention Matrix (마스킹 전):                        |
|       I    love  you  <EOS>                           |
|  I  [ 0.5  0.3   0.1  0.1 ]                          |
|  love[ 0.2  0.4   0.3  0.1 ]                         |
|  you [ 0.1  0.2   0.5  0.2 ]                         |
|                                                       |
|  Causal Mask (하삼각):                                |
|       I    love  you  <EOS>                           |
|  I  [ ✓    ✗     ✗    ✗   ]                          |
|  love[ ✓    ✓     ✗    ✗   ]                         |
|  you [ ✓    ✓     ✓    ✗   ]                         |
|                                                       |
|  "love" 예측 시 "I"만 참조 (미래 차단!)              |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Masked Self-Attention은 시험에서 <strong>다음 문제의 답을 못 보게 가리는 것</strong>이다. 답을 보면 실력 측정이 안 되니까.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Self vs Masked Self vs Cross

| 유형 | [마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹 | 용도 |
|:---|:---|:---|
| **Self** | 없음 | [인코더](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/) ([BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)) |
| **Masked Self** | **하삼각** | <strong><a href="/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/">디코더</a> (<a href="/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/">GPT</a>)</strong> |
| **Cross** | 없음 | [인코더](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)->[디코더](/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) |

- **📢 섹션 요약 비유**: Self는 책 전체를 보고 이해, Masked는 앞 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)만 보고 다음 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 예측.

---

## Ⅲ. 비교 및 연결

| 비교 | [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) (Self) | [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) (Masked Self) |
|:---|:---|:---|
| <strong><a href="/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">참조</a></strong> | 양방향 | **왼->오만** |
| **학습** | [MLM](/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/) (빈칸) | **다음 토큰 예측** |
| **용도** | 이해·[분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) | <strong><a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a></strong> |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [KV Cache](/studynote/06_ict_convergence/04_ai_llm/291_kv_cache/)
- 자기 회귀 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시 이전 [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)·Value를 [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)하여 중복 계산 방지.
- Masked Self-Attention의 성질(과거만 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/))을 활용한 추론 최적화.

---

## Ⅴ. 기대효과 및 결론

Masked Self-Attention은 <strong><a href="/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/">GPT</a>·Llama 등 자기 회귀 LLM의 필수 구성 요소</strong>이며, KV Cache와 결합하여 효율적 텍스트 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)을 실현한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Causal Mask** | 하삼각 행렬 (미래 차단) |
| <strong><a href="/studynote/14_data_engineering/05_exam_keywords/248_bert_encoder_mlm_gpt_decoder_autoregressive_comparison/">Autoregressive</a></strong> | 이전 토큰으로 다음 예측 |
| <strong><a href="/studynote/06_ict_convergence/04_ai_llm/291_kv_cache/">KV Cache</a></strong> | 추론 시 [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)·Value 재사용 |
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/">BERT</a></strong> | [마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹 없음 (양방향) |
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/">GPT</a></strong> | Masked [Self-Attention](/studynote/10_ai/02_dl_architecture_new/124_self_attention/) 사용 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Self-Attention (Transformer, 2017)]
    |
    v
[Masked Self-Attention (GPT-1, 2018)]
    |
    v
[KV Cache 최적화 (2020~)]
    |
    v
[Sliding Window Attention (Mistral, 2023)]
    |
    v
[현재: Sparse + Masked — 효율적 긴 시퀀스 생성]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Masked Self-Attention은 시험에서 **다음 문제의 답을 가리는** 거예요.
2. 답을 미리 보면 <strong>진짜 실력</strong>을 측정할 수 없으니까요.
3. GPT가 <strong>앞 단어만 보고 다음 단어를 예측</strong>할 수 있는 건 이 [마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹 덕분이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 127 / 420

<- **이전**: [126. Positional Encoding - Transformer에 순서 정보를 주입하는 기법](/studynote/10_ai/02_dl_architecture_new/126_positional_encoding/)
**다음**: [128. Cross-Attention - 인코더->디코더 참조 메커니즘](/studynote/10_ai/02_dl_architecture_new/128_cross_attention/) ->

---
