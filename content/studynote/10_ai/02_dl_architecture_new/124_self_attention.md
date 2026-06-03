+++
title = "124. Self-Attention (자기 주의 메커니즘) - 시퀀스 내 모든 위치 상호 참조"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Self-Attention은 <strong>같은 시퀀스 내에서 각 위치가 다른 모든 위치를 참조</strong>하여 문맥을 파악하는 메커니즘이며, Transformer의 핵심 연산이다. Q·K·V가 모두 <strong>같은 시퀀스에서 생성</strong>된다.
> 2. **가치**: "The animal didn't cross the street because **it** was too tired"에서 "it"이 "animal"을 가리킨다는 것을 파악하려면 문장 전체를 참조해야 하며, Self-Attention이 이를 <strong>가중치로 정량화</strong>한다.
> 3. **판단 포인트**: Cross-Attention(Q≠K,V, 인코더→디코더)과 구분하고, **Masked Self-Attention**(디코더에서 미래 토큰 참조 방지)의 필요성을 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

자연어에서 단어의 의미는 문장 전체 맥락에 따라 결정된다. "The animal didn't cross the street because it was too tired"에서 "it"이 "animal"을 가리키는지 "street"을 가리키는지는 문장 전체를 보아야 알 수 있다. 이러한 참조(Coreference) 해결은 NLP의 핵심 도전이다.

RNN은 시퀀스를 순차적으로 처리하므로 현재 위치에서 먼 과거 정보는 기울기 소실로 희석된다. Self-Attention은 이를 근본적으로 해결한다. 시퀀스의 <strong>모든 위치 쌍에 대해 동시에 유사도를 계산</strong>하고, 관련성에 비례한 가중치로 정보를 집계한다. 거리에 관계없이 중요한 위치에 직접 집중할 수 있다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Self-Attention 동작 예시</div>
<div class="kb-diagram-note">입력: "The cat sat on the mat"</div>
<div class="kb-diagram-note">"sat"의 Self-Attention 가중치:</div>
<div class="kb-diagram-note">The → 0.05 (관련 낮음)</div>
<div class="kb-diagram-note">cat → 0.30 (주어! 관련 높음)</div>
<div class="kb-diagram-note">sat → 0.10 (자기 자신)</div>
<div class="kb-diagram-note">on → 0.15 (위치 관계)</div>
<div class="kb-diagram-note">the → 0.05 (관련 낮음)</div>
<div class="kb-diagram-note">mat → 0.35 (장소! 관련 높음)</div>
<div class="kb-diagram-note">→ "sat"은 "cat"(누가)과 "mat"(어디)에 높은 가중치</div>
<div class="kb-diagram-note">→ "누가(cat) 어디에(mat) 앉았는지" 자동 파악</div>
<div class="kb-diagram-note">Q = K = V = "sat"의 임베딩 × W_Q/K/V</div>
<div class="kb-diagram-note">Score = Q · K^T / √d_k</div>
<div class="kb-diagram-note">Weight = softmax(Score)</div>
<div class="kb-diagram-note">Output = Weight · V</div>
</div>
</div>



- **📢 섹션 요약 비유**: Self-Attention은 교실에서 **모든 학생이 서로의 얼굴을 보면서** 누가 누구와 관련 있는지 파악하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Self vs Cross vs Masked Self-Attention

| 유형 | Q 출처 | K·V 출처 | 마스킹 | 용도 |
|:---|:---|:---|:---|:---|
| **Self-Attention** | 같은 시퀀스 | 같은 시퀀스 | 없음 | **인코더 (양방향)** |
| **Cross-Attention** | 디코더 | 인코더 | 없음 | 인코더→디코더 참조 |
| **Masked Self-Attention** | 같은 시퀀스 | 같은 시퀀스 | 미래 마스킹 | **디코더 (자기회귀)** |

### 마스킹(Masking)의 필요성

디코더에서 자기회귀(Autoregressive) 생성 시, 모델이 미래 토큰을 미리 보고 예측하면 학습이 의미 없어진다("치팅 문제"). Masked Self-Attention은 Score 행렬에서 미래 위치를 $-\infty$로 마스킹하여 소프트맥스 후 가중치를 0으로 만든다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Masked Self-Attention 행렬 (4개 토큰):</div>
<div class="kb-diagram-note">The cat sat on</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">The</div><div class="kb-diagram-node">1.0  0.0   0.0  0.0</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">"The"는 자신만 참조</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">cat</div><div class="kb-diagram-node">0.3  0.7   0.0  0.0</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">"cat"는 "The, cat" 참조</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">sat</div><div class="kb-diagram-node">0.1  0.3   0.6  0.0</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">"sat"은 앞 3개 참조</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">on</div><div class="kb-diagram-node">0.1  0.2   0.3  0.4</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">"on"은 모두 참조</div></div>
<div class="kb-diagram-note">마스킹: 우상삼각 부분을 -∞로 설정 → softmax 후 0</div>
</div>
</div>



### 병렬 처리의 구현

Self-Attention의 가장 큰 장점은 <strong>모든 위치의 Attention을 행렬 연산으로 동시에 계산</strong>한다는 것이다. RNN은 h_t를 h_{t-1}에 의존하여 순차 처리해야 하지만, Self-Attention은 모든 위치의 Q, K, V를 한 번에 행렬 곱으로 계산한다.

```python
# Self-Attention 행렬 연산 (PyTorch)
import torch
import torch.nn.functional as F

def self_attention(X, W_Q, W_K, W_V, mask=None):
    # X: [batch, seq_len, d_model]
    Q = X @ W_Q   # [batch, seq_len, d_k]
    K = X @ W_K   # [batch, seq_len, d_k]
    V = X @ W_V   # [batch, seq_len, d_v]

    d_k = Q.size(-1)
    scores = Q @ K.transpose(-2, -1) / (d_k ** 0.5)

    if mask is not None:
        scores = scores.masked_fill(mask == 0, float('-inf'))

    weights = F.softmax(scores, dim=-1)
    output = weights @ V
    return output, weights
```

### O(n²) 복잡도와 대안

Self-Attention의 계산 복잡도는 O(n²·d)이다. 시퀀스 길이 n이 커지면 메모리·계산 비용이 급증한다.

| 기법 | 복잡도 | 방식 |
|:---|:---|:---|
| **Self-Attention** | O(n²·d) | 기본 |
| **Sparse Attention** | O(n·√n·d) | 일부 쌍만 계산 |
| **Linformer** | O(n·d) | K·V를 저차원으로 압축 |
| **Flash Attention** | O(n²·d) (IO 최적화) | 타일 기반 메모리 효율화 |

- **📢 섹션 요약 비유**: Self는 책 전체를 보고 이해하는 것, Masked는 앞 페이지만 보고 다음 페이지를 예측하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 항목 | RNN | Self-Attention |
|:---|:---|:---|
| **참조 범위** | 직전 상태만 (편향) | **전체 시퀀스 직접 참조** |
| **병렬화** | 불가 | **가능** |
| **장거리 의존성** | 기울기 소실로 약함 | **강함** |
| **계산 비용** | O(n·d²) | **O(n²·d)** |
| **해석 가능성** | 낮음 | **Attention 시각화 가능** |
| **위치 정보** | 내재적 | **Positional Encoding 필요** |

### Self-Attention이 BERT와 GPT에서 다르게 사용되는 방식

- **BERT (인코더)**: Masked Language Model로 학습 → 양방향 Self-Attention (모든 위치 참조)
- **GPT (디코더)**: Causal Language Model로 학습 → Masked Self-Attention (과거만 참조)

이 차이가 BERT의 이해 강점과 GPT의 생성 강점을 결정한다.

- **📢 섹션 요약 비유**: BERT의 Self-Attention은 방 안에서 모든 사람을 360도로 보는 것이고, GPT의 Masked Self-Attention은 앞사람만 보는 행진이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Self-Attention의 계층적 해석

다중 레이어 Transformer에서 각 레이어의 Attention 헤드는 다른 수준의 패턴을 학습한다.

- **하위 레이어**: 문법적 관계 (주어-동사 일치, 전치사 관계)
- **중간 레이어**: 의미적 관계 (동의어, 반의어)
- **상위 레이어**: 추론 관계 (원인-결과, 함의)

### 설계 판단 체크리스트

1. **인코더인가 디코더인가?** → 마스킹 여부 결정
2. **시퀀스 길이가 4096 이상인가?** → Flash Attention 필수
3. **해석 가능성이 필요한가?** → Attention 시각화 도구 설계
4. **멀티모달인가?** → Cross-Attention 방식 결정

### 안티패턴

- **Masked Self-Attention 마스킹 실수**: 미래 정보 누출 → 학습 오염
- **Positional Encoding 없이 Self-Attention**: 순서 정보 손실 → 무작위 순서와 동일 처리
- **메모리 문제 무시**: 긴 시퀀스에서 O(n²) 메모리 → OOM 발생

- **📢 섹션 요약 비유**: Self-Attention은 신호등 없는 교차로에서 모든 차가 서로를 보며 통행하는 것이다. 효율적이지만 규칙(마스킹, 포지셔널 인코딩)이 없으면 혼란이 발생한다.

---

## Ⅴ. 기대효과 및 결론

### 도입 시 기대 효과

| 효과 항목 | 정량/정성 효과 |
|:---|:---|
| **장거리 의존성 해결** | 문서 전체 길이에 관계없이 직접 참조 |
| **병렬 처리** | RNN 대비 3~10배 학습 속도 향상 |
| **표현 품질** | 문맥 의존적 임베딩 (BERT 임베딩 vs Word2Vec) |
| **해석 가능성** | Attention 가중치 시각화로 모델 동작 이해 |

### 미래 전망

Self-Attention은 <strong>Transformer·BERT·GPT의 단일 핵심 메커니즘</strong>이며, Vision(ViT)·Audio(Whisper)까지 확장되어 현대 AI의 근간이다. 계산 비용 문제를 해결하는 Flash Attention, GQA 등의 효율화 기법이 계속 발전하고 있다.

- **📢 섹션 요약 비유**: Self-Attention은 민주주의다. 모든 단어(국민)가 평등하게 서로를 참조(투표)하며, 중요한 단어(대표)에는 더 높은 가중치(영향력)가 부여된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **Self-Attention** | 같은 시퀀스 내 상호 참조 |
| **Masked Self-Attention** | 미래 토큰 마스킹 (GPT 디코더) |
| **Cross-Attention** | 인코더→디코더 참조 |
| **Multi-Head Attention** | 다관점 Self-Attention |
| **O(n²) 복잡도** | Self-Attention의 근본 한계 |
| **Flash Attention** | O(n²) 메모리 최적화 (IO-Aware) |
| **Sparse Attention** | O(n·√n) 부분 계산 |
| **ALiBi / RoPE** | 위치 정보를 Attention Score에 통합 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Cross-Attention (Bahdanau, 2014)</div>
<div class="kb-diagram-note">→ 인코더→디코더 참조</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Self-Attention (Transformer, 2017)</div>
<div class="kb-diagram-note">→ 시퀀스 자기 참조, 완전 병렬화</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Masked Self-Attention (GPT, 2018)</div>
<div class="kb-diagram-note">→ 자기회귀 생성을 위한 마스킹</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Multi-Head + Masked Self-Attention</div>
<div class="kb-diagram-note">→ 다관점 + 마스킹 통합</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Efficient Attention (Linformer, 2020)</div>
<div class="kb-diagram-note">→ O(n) 선형 복잡도 근사</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Flash Attention (2022)</div>
<div class="kb-diagram-note">→ IO-Aware 메모리 최적화</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">현재: Flash Attention 2/3, GQA</div>
<div class="kb-diagram-note">→ 서빙 최적화 표준</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. Self-Attention은 교실에서 **모든 친구의 얼굴을 보면서** 관계를 파악하는 거예요.
2. "고양이가 매트 위에 앉았다"에서 "앉았다"는 **"고양이"와 "매트"를 더 많이** 봐요.
3. 이 방법 덕분에 AI가 <strong>문장의 뜻을 정확하게 이해</strong>할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 124 / 420

← **이전**: [123. Transformer 아키텍처 - Self-Attention 기반 병렬 시퀀스 처리](/knowledge-base/studynote/10_ai/02_dl_architecture_new/123_transformer_architecture/)
**다음**: [125. Multi-Head Attention - 다관점 병렬 Attention으로 풍부한 표현 학습](/knowledge-base/studynote/10_ai/02_dl_architecture_new/125_multi_head_attention/) →

---
