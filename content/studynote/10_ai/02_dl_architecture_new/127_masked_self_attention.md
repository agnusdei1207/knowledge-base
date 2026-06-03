---
title: 127. Masked Self-Attention - 자기 회귀 디코더의 미래 토큰 차단
date: '2026-04-19'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Masked Self-Attention은 **[[039_decoder|디코더]]에서 현재 위치 이후의 미래 토큰을 [[316_reference_pattern_nosql|참조]]하지 못하도록 [[172_maas_mobility_as_a_service|마스]]킹(-∞)하는 [[124_self_attention|Self-Attention]]**이며, [[302_gpt_autoregressive|GPT]] 등 자기 회귀([[248_bert_encoder_mlm_gpt_decoder_autoregressive_comparison|Autoregressive]]) 모델의 핵심 메커니즘이다.
> 2. **가치**: "I love"까지 [[087_process_state_transition|생성]] 후 다음 토큰을 예측할 때, 정답인 "you"를 이미 본 상태에서 예측하면 **학습이 무의미([[001_dikw_pyramid|data]] leakage)**하므로, Masked Self-Attention이 미래를 가려서 **진정한 예측**을 가능하게 한다.
> 3. **판단 포인트**: Causal Mask(하삼각 행렬)를 Attention Score에 적용하여 미래 위치에 -∞를 더하고 [[270_softmax|softmax]] 후 0이 되게 하며, [[301_bert_mlm|BERT]](양방향)는 [[172_maas_mobility_as_a_service|마스]]킹 없이 전체 [[316_reference_pattern_nosql|참조]]한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Masked Self-Attention                              │
├───────────────────────────────────────────────────────┤
│  입력: "I love you <EOS>"                             │
│                                                       │
│  Attention Matrix (마스킹 전):                        │
│       I    love  you  <EOS>                           │
│  I  [ 0.5  0.3   0.1  0.1 ]                          │
│  love[ 0.2  0.4   0.3  0.1 ]                         │
│  you [ 0.1  0.2   0.5  0.2 ]                         │
│                                                       │
│  Causal Mask (하삼각):                                │
│       I    love  you  <EOS>                           │
│  I  [ ✓    ✗     ✗    ✗   ]                          │
│  love[ ✓    ✓     ✗    ✗   ]                         │
│  you [ ✓    ✓     ✓    ✗   ]                         │
│                                                       │
│  "love" 예측 시 "I"만 참조 (미래 차단!)              │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Masked Self-Attention은 시험에서 **다음 문제의 답을 못 보게 가리는 것**이다. 답을 보면 실력 측정이 안 되니까.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Self vs Masked Self vs Cross

| 유형 | [[172_maas_mobility_as_a_service|마스]]킹 | 용도 |
|:---|:---|:---|
| **Self** | 없음 | [[040_encoder|인코더]] ([[301_bert_mlm|BERT]]) |
| **Masked Self** | **하삼각** | **[[039_decoder|디코더]] ([[302_gpt_autoregressive|GPT]])** |
| **Cross** | 없음 | [[040_encoder|인코더]]→[[039_decoder|디코더]] [[316_reference_pattern_nosql|참조]] |

- **📢 섹션 요약 비유**: Self는 책 전체를 보고 이해, Masked는 앞 [[286_page_frame|페이지]]만 보고 다음 [[286_page_frame|페이지]] 예측.

---

## Ⅲ. 비교 및 연결

| 비교 | [[301_bert_mlm|BERT]] (Self) | [[302_gpt_autoregressive|GPT]] (Masked Self) |
|:---|:---|:---|
| **[[316_reference_pattern_nosql|참조]]** | 양방향 | **왼→오만** |
| **학습** | [[138_mlm_learning|MLM]] (빈칸) | **다음 토큰 예측** |
| **용도** | 이해·[[104_classification_analysis|분류]] | **[[087_process_state_transition|생성]]** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[291_kv_cache|KV Cache]]
- 자기 회귀 [[087_process_state_transition|생성]] 시 이전 [[067_db_key_uniqueness_minimality|Key]]·Value를 [[456_caching|캐싱]]하여 중복 계산 방지.
- Masked Self-Attention의 성질(과거만 [[316_reference_pattern_nosql|참조]])을 활용한 추론 최적화.

---

## Ⅴ. 기대효과 및 결론

Masked Self-Attention은 **[[302_gpt_autoregressive|GPT]]·Llama 등 자기 회귀 LLM의 필수 구성 요소**이며, KV Cache와 결합하여 효율적 텍스트 [[087_process_state_transition|생성]]을 실현한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Causal Mask** | 하삼각 행렬 (미래 차단) |
| **[[248_bert_encoder_mlm_gpt_decoder_autoregressive_comparison|Autoregressive]]** | 이전 토큰으로 다음 예측 |
| **[[291_kv_cache|KV Cache]]** | 추론 시 [[067_db_key_uniqueness_minimality|Key]]·Value 재사용 |
| **[[301_bert_mlm|BERT]]** | [[172_maas_mobility_as_a_service|마스]]킹 없음 (양방향) |
| **[[302_gpt_autoregressive|GPT]]** | Masked [[124_self_attention|Self-Attention]] 사용 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Self-Attention (Transformer, 2017)]
    │
    ▼
[Masked Self-Attention (GPT-1, 2018)]
    │
    ▼
[KV Cache 최적화 (2020~)]
    │
    ▼
[Sliding Window Attention (Mistral, 2023)]
    │
    ▼
[현재: Sparse + Masked — 효율적 긴 시퀀스 생성]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Masked Self-Attention은 시험에서 **다음 문제의 답을 가리는** 거예요.
2. 답을 미리 보면 **진짜 실력**을 측정할 수 없으니까요.
3. GPT가 **앞 단어만 보고 다음 단어를 예측**할 수 있는 건 이 [[172_maas_mobility_as_a_service|마스]]킹 덕분이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 127 / 420

← **이전**: [[126_positional_encoding|126. Positional Encoding - Transformer에 순서 정보를 주입하는 기법]]
**다음**: [[128_cross_attention|128. Cross-Attention - 인코더→디코더 참조 메커니즘]] →

---
