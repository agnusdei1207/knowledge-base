---
title: "125. Multi Head Attention"
date: "2026-04-19"
tags:
  - "studynote-ai"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Multi-Head Attention은 <strong>QKV를 h개 헤드로 분할하여 각 헤드가 독립적으로 Attention을 수행</strong>한 후 결합(Concat+Linear)하는 구조이며, 단일 Attention보다 <strong>다양한 <a href="/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a> 패턴을 동시에 포착</strong>한다.
> 2. **가치**: 단일 Attention은 하나의 관점에서만 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하지만, 8개 헤드는 각각 <strong>문법 <a href="/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a>·의미 <a href="/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a>·위치 <a href="/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a></strong> 등 다른 패턴에 주목하여 <strong>더 풍부한 표현</strong>을 학습한다.
> 3. **판단 포인트**: d_model=512, h=8이면 각 헤드는 d_k=64 차원에서 독립 Attention을 수행하며, 총 연산량은 단일 헤드와 동일하되 <strong>표현력은 증가</strong>한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Multi-Head Attention                               |
+-------------------------------------------------------+
|  입력 X (d_model=512)                                 |
|  +-- Head 1: Q₁K₁V₁ (d_k=64) -> Attn₁               |
|  +-- Head 2: Q₂K₂V₂ (d_k=64) -> Attn₂               |
|  +-- ...                                              |
|  +-- Head 8: Q₈K₈V₈ (d_k=64) -> Attn₈               |
|                                                       |
|  Concat(Attn₁, ..., Attn₈) -> W_O -> 출력 (512)       |
|                                                       |
|  각 헤드: 다른 관점 (문법·의미·위치 등)              |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 단일 Attention은 1명의 감독관이 감시하는 것이고, Multi-Head는 <strong>8명의 전문가가 각자 다른 관점(문법·의미·위치)</strong>으로 동시에 분석하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 계산 과정

| 단계 | 수식 |
|:---|:---|
| **분할** | Q_i = X·W_Q_i, K_i = X·W_K_i, V_i = X·W_V_i |
| **Attention** | head_i = Attn(Q_i, K_i, V_i) |
| **결합** | Concat(head_1,...,head_h) · W_O |

### GQA (Grouped Query Attention)
- 최신 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)(Llama 2)에서는 [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)·Value 헤드를 공유하여 **메모리·속도 최적화**.

- **📢 섹션 요약 비유**: MHA는 8명이 각자 카메라를 가진 것이고, GQA는 8명이 4대 카메라를 공유하는 것이다 (효율^).

---

## Ⅲ. 비교 및 연결

| 비교 | 단일 Head | Multi-Head | GQA |
|:---|:---|:---|:---|
| **관점** | 1개 | **h개** | h개 (KV 공유) |
| **표현력** | 낮음 | **높음** | 높음 |
| **효율** | - | 동일 | **향상** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 헤드 수 선택
- [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)-base: h=8, d_k=64.
- [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)-large: h=16, d_k=64.
- 헤드 수^ -> 다양한 관점, 단 d_kv -> 개별 헤드 용량 감소.

---

## Ⅴ. 기대효과 및 결론

Multi-Head Attention은 <strong>Transformer의 표현력을 결정</strong>하는 핵심 구조이며, GQA·MQA로 효율화되어 최신 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)([GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-4·Llama 3)에서 표준으로 사용된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Multi-Head** | h개 관점 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) Attention |
| **GQA** | [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)·Value 헤드 공유 (효율화) |
| **MQA** | 모든 헤드가 1개 KV 공유 |
| **d_model** | 모델 전체 차원 |
| **d_k** | 각 헤드의 차원 (d_model/h) |

### 📈 관련 키워드 및 발전 흐름도

```text
[단일 Head Attention (Bahdanau, 2014)]
    |
    v
[Multi-Head Attention (Transformer, 2017)]
    |
    v
[MQA — Multi-Query Attention (2019)]
    |
    v
[GQA — Grouped Query Attention (Llama 2, 2023)]
    |
    v
[현재: Efficient MHA — Flash Attention + GQA 조합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 단일 Attention은 <strong>1명의 탐정</strong>이 사건을 조사하는 거예요.
2. Multi-Head는 <strong>8명의 전문 탐정</strong>이 각자 다른 단서(문법·의미·위치)를 동시에 조사해요.
3. 탐정이 많으면 **더 많은 단서를 찾아서** 사건(문장)을 정확히 이해할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 125 / 420

<- **이전**: [124. Self-Attention (자기 주의 메커니즘) - 시퀀스 내 모든 위치 상호 참조](/studynote/10_ai/02_dl_architecture_new/124_self_attention/)
**다음**: [126. Positional Encoding - Transformer에 순서 정보를 주입하는 기법](/studynote/10_ai/02_dl_architecture_new/126_positional_encoding/) ->

---
