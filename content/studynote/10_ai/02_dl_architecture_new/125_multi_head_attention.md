+++
title = "125. Multi-Head Attention - 다관점 병렬 Attention으로 풍부한 표현 학습"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Multi-Head Attention은 <strong>QKV를 h개 헤드로 분할하여 각 헤드가 독립적으로 Attention을 수행</strong>한 후 결합(Concat+Linear)하는 구조이며, 단일 Attention보다 <strong>다양한 관계 패턴을 동시에 포착</strong>한다.
> 2. **가치**: 단일 Attention은 하나의 관점에서만 참조하지만, 8개 헤드는 각각 **문법 관계·의미 관계·위치 관계** 등 다른 패턴에 주목하여 <strong>더 풍부한 표현</strong>을 학습한다.
> 3. **판단 포인트**: d_model=512, h=8이면 각 헤드는 d_k=64 차원에서 독립 Attention을 수행하며, 총 연산량은 단일 헤드와 동일하되 <strong>표현력은 증가</strong>한다.

---

## Ⅰ. 개요 및 필요성

단일 Self-Attention은 각 토큰이 다른 모든 토큰과의 관계를 하나의 관점(단일 Q·K·V)에서만 학습한다. 그러나 언어의 복잡성은 동시에 여러 다른 종류의 관계를 처리할 필요가 있다.

예를 들어 "The bank can guarantee deposits will eventually cover future tuition costs"에서:
- 헤드 1: "bank"와 "deposits" → 금융 의미 관계
- 헤드 2: "can guarantee" → 동사 구조 관계
- 헤드 3: "future tuition costs" → 시간적 관계
- 헤드 4: 문장 전체 문법 구조

Multi-Head Attention은 h개의 독립적인 Attention 헤드를 병렬로 실행하여, 각 헤드가 서로 다른 표현 부분공간(Representation Subspace)에서 정보를 수집하도록 한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Multi-Head Attention 구조 (h=8, d_model=512)</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">입력 X</div><div class="kb-diagram-node">seq_len × 512</div></div>
<div class="kb-diagram-note">↓ (8개 헤드로 분할)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Head 1: Q₁K₁V₁ (d_k=64) → Attn₁ (문법)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Head 2: Q₂K₂V₂ (d_k=64) → Attn₂ (의미)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Head 3: Q₃K₃V₃ (d_k=64) → Attn₃ (위치)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Head 4: Q₄K₄V₄ (d_k=64) → Attn₄ (추론)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Head 5: Q₅K₅V₅ (d_k=64) → Attn₅</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Head 6: Q₆K₆V₆ (d_k=64) → Attn₆</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Head 7: Q₇K₇V₇ (d_k=64) → Attn₇</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Head 8: Q₈K₈V₈ (d_k=64) → Attn₈</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">↓</div><div class="kb-diagram-node">seq_len × 512</div><div class="kb-diagram-note">)</div></div>
<div class="kb-diagram-note">Concat(Attn₁, ..., Attn₈)</div>
<div class="kb-diagram-note">↓ (W_O 선형 변환)</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">W_O</div><div class="kb-diagram-node">512 × 512</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">seq_len × 512</div></div>
<div class="kb-diagram-note">총 파라미터: h × (d_k × d_model) × 3 (Q/K/V) + d_model × d_model (W_O)</div>
<div class="kb-diagram-note">= 8 × 64 × 512 × 3 + 512 × 512</div>
<div class="kb-diagram-note">≈ 786K + 262K ≈ 1.05M (단일 헤드와 동일)</div>
</div>
</div>



- **📢 섹션 요약 비유**: 단일 Attention은 1명의 감독관이 감시하는 것이고, Multi-Head는 <strong>8명의 전문가가 각자 다른 관점(문법·의미·위치)</strong>으로 동시에 분석하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Multi-Head Attention 수식

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_h) \cdot W^O$$

$$\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$$

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

| 파라미터 | 의미 | 표준값 |
|:---|:---|:---|
| **h** | 헤드 수 | 8 (base), 16 (large) |
| **d_model** | 모델 전체 차원 | 512 (base), 1024 (large) |
| **d_k = d_v** | 각 헤드의 차원 | d_model / h = 64 |
| **W_O** | 출력 투영 행렬 | (h·d_v) × d_model |

### 각 헤드가 학습하는 다양한 패턴

실험적으로 확인된 Multi-Head Attention의 헤드별 전문화:

| 헤드 예시 | 주로 포착하는 패턴 |
|:---|:---|
| 헤드 1~2 | 로컬 근거리 의존성 (인접 단어) |
| 헤드 3~4 | 문법 구조 (주어-동사-목적어) |
| 헤드 5~6 | 의미 관계 (동의어, 반의어) |
| 헤드 7~8 | 장거리 참조 (대명사-선행사) |

### GQA / MQA (효율화 변형)

최신 LLM에서는 메모리·속도 최적화를 위해 K·V 헤드 수를 줄인다.

```text
MHA (Multi-Head): Q K V 각각 h개 헤드
    q₁q₂...q_h │ k₁k₂...k_h │ v₁v₂...v_h

MQA (Multi-Query): Q만 h개, K·V는 1개 공유
    q₁q₂...q_h │     k₁     │     v₁

GQA (Grouped-Query): Q는 h개, K·V는 g개 (h/g 비율)
    q₁q₂q₃q₄   │    k₁ k₂   │    v₁ v₂
    (Llama 2·3, Mistral 표준)
```

| 방식 | K·V 헤드 | 추론 속도 | 품질 | 사용 모델 |
|:---|:---|:---|:---|:---|
| **MHA** | h개 | 기본 | 최고 | 원본 Transformer |
| **MQA** | 1개 | 빠름 | 약간 저하 | 초기 효율화 |
| **GQA** | g개 | 빠름 | 거의 동일 | **Llama 2·3, Mistral** |

- **📢 섹션 요약 비유**: MHA는 8명이 각자 카메라를 가진 것이고, GQA는 8명이 4대 카메라를 공유하는 것이다 (효율↑).

---

## Ⅲ. 비교 및 연결

| 비교 항목 | 단일 Head | Multi-Head (MHA) | GQA |
|:---|:---|:---|:---|
| **관점 수** | 1개 | **h개 (병렬)** | h개 (K·V 공유) |
| **표현력** | 낮음 | **높음** | 높음 |
| **파라미터** | 동일 | 동일 (분할) | 약간 감소 |
| **추론 KV-cache** | 1× | h× | **g× (g<h)** |
| **효율** | 기본 | 기본 | **향상** |

### Multi-Head Attention 시각화 해석

각 헤드의 Attention 가중치를 시각화하면 서로 다른 패턴이 나타난다. 이를 통해:
- 모델이 어떤 관계를 학습했는지 해석 가능
- 특정 헤드가 불필요한 패턴만 학습하고 있다면 프루닝(Pruning) 후보
- 버그 탐지: 특정 헤드가 모든 위치에 균일한 가중치를 준다면 학습 문제

- **📢 섹션 요약 비유**: Multi-Head는 다각도 CCTV다. 한 대(단일 헤드)로는 사각지대가 생기지만, 여러 대(멀티헤드)로 사각지대 없이 전체를 관찰할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 헤드 수 선택 기준



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">d_model별 표준 헤드 수:</div>
<div class="kb-diagram-note">d_model = 256 → h = 4, d_k = 64</div>
<div class="kb-diagram-note">d_model = 512 → h = 8, d_k = 64 (BERT-base)</div>
<div class="kb-diagram-note">d_model = 768 → h = 12, d_k = 64 (GPT-2)</div>
<div class="kb-diagram-note">d_model = 1024 → h = 16, d_k = 64 (BERT-large)</div>
<div class="kb-diagram-note">d_model = 4096 → h = 32, d_k = 128 (LLaMA-7B)</div>
<div class="kb-diagram-note">원칙: d_k = d_model / h ≥ 32 (너무 작으면 표현력 저하)</div>
</div>
</div>



### 설계 판단 체크리스트

1. **d_model을 결정했는가?** → h는 d_k ≥ 32 조건 하에 설정
2. **추론 속도가 중요한가?** → GQA 적용 (g=h/4 또는 g=h/8)
3. **해석 가능성이 필요한가?** → 헤드별 Attention 시각화 도구 설계
4. **모델 경량화가 필요한가?** → 헤드 프루닝 (불필요 헤드 제거)

### 안티패턴

- **헤드 수만 늘리기**: d_k가 너무 작아지면 표현력 저하
- **MHA/GQA 혼동**: 추론 KV-cache 크기 계산 오류
- **모든 헤드 동일 초기화**: 다양성이 사라져 단일 헤드와 유사

- **📢 섹션 요약 비유**: 헤드를 너무 많이 늘리는 것은 전문가를 너무 잘게 쪼개는 것이다. 각 전문가가 너무 좁은 영역만 담당하면 전체 그림을 못 본다.

---

## Ⅴ. 기대효과 및 결론

### 도입 시 기대 효과

| 효과 항목 | 정량/정성 효과 |
|:---|:---|
| **표현력 향상** | 단일 헤드 대비 다양한 언어 패턴 학습 |
| **번역 품질** | 다관점 Attention으로 BLEU score 향상 |
| **추론 능력** | 다양한 관계 동시 파악으로 복잡한 추론 개선 |
| **해석 가능성** | 헤드별 시각화로 모델 동작 이해 |
| **GQA 효율화** | 추론 속도 1.5~3배 향상 |

### 미래 전망

Multi-Head Attention은 <strong>Transformer의 표현력을 결정</strong>하는 핵심 구조이며, GQA·MQA로 효율화되어 최신 LLM(GPT-4·Llama 3)에서 표준으로 사용된다. Flash Attention과 결합하면 메모리 효율도 크게 개선된다.

- **📢 섹션 요약 비유**: Multi-Head Attention은 전문가 팀이다. 언어학자, 문법가, 논리학자가 동시에 한 문장을 분석하면 한 사람이 보는 것보다 더 깊고 정확한 이해가 나온다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **Multi-Head Attention** | h개 관점 병렬 Attention |
| **GQA** | Key·Value 헤드 공유 (효율화) |
| **MQA** | 모든 헤드가 1개 KV 공유 |
| **d_model** | 모델 전체 차원 |
| **d_k** | 각 헤드의 차원 (d_model/h) |
| **KV-cache** | 추론 시 K·V 재계산 방지 |
| **헤드 프루닝** | 불필요 헤드 제거로 경량화 |
| **Flash Attention** | MHA 연산의 메모리 최적화 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">단일 Head Attention (Bahdanau, 2014)</div>
<div class="kb-diagram-note">→ 하나의 관점</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Multi-Head Attention (Transformer, 2017)</div>
<div class="kb-diagram-note">→ h개 병렬 관점, 표현력 향상</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">MQA (Multi-Query, 2019)</div>
<div class="kb-diagram-note">→ K·V 1개 헤드 공유, 추론 속도 향상</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">GQA (Grouped-Query, Llama 2, 2023)</div>
<div class="kb-diagram-note">→ K·V g개 헤드 공유, 품질·효율 균형</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Flash Attention (2022~)</div>
<div class="kb-diagram-note">→ IO-Aware, 메모리·속도 동시 최적화</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">현재: Flash Attention 2/3 + GQA</div>
<div class="kb-diagram-note">→ LLM 서빙의 표준 Attention 구현</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. 단일 Attention은 <strong>1명의 탐정</strong>이 사건을 조사하는 거예요.
2. Multi-Head는 <strong>8명의 전문 탐정</strong>이 각자 다른 단서(문법·의미·위치)를 동시에 조사해요.
3. 탐정이 많으면 **더 많은 단서를 찾아서** 사건(문장)을 정확히 이해할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 125 / 420

← **이전**: [124. Self-Attention (자기 주의 메커니즘) - 시퀀스 내 모든 위치 상호 참조](/knowledge-base/studynote/10_ai/02_dl_architecture_new/124_self_attention/)
**다음**: [126. Positional Encoding - Transformer에 순서 정보를 주입하는 기법](/knowledge-base/studynote/10_ai/02_dl_architecture_new/126_positional_encoding/) →

---
