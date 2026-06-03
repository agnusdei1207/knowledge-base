+++
title = "122. Q·K·V 시스템 (Query·Key·Value) - Attention의 핵심 연산 구조"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Q(Query)·K(Key)·V(Value)는 <strong>Attention 연산의 3대 구성 요소</strong>로, Query가 "무엇을 찾는가", Key가 "각 위치의 매칭 키", Value가 "실제 정보"를 담당한다. $\text{Attention}(Q,K,V) = \text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$
> 2. **가치**: Bahdanau Attention은 Score 함수가 암묵적이었으나, QKV 분리로 **Query·Key로 유사도를 계산하고 Value에서 정보를 가져오는** 명시적 구조가 되어 Multi-Head Attention·Cross-Attention 등 <strong>다양한 확장이 가능</strong>해졌다.
> 3. **판단 포인트**: Self-Attention에서는 Q=K=V(같은 시퀀스에서 생성), Cross-Attention에서는 Q(디코더)≠K,V(인코더)이며, $\sqrt{d_k}$로 나누는 것은 <strong>내적 값이 커져 softmax가 포화되는 것을 방지</strong>하기 위함이다.

---

## Ⅰ. 개요 및 필요성

Bahdanau Attention에서는 디코더 상태(s)와 인코더 상태(h) 사이의 유사도를 계산하는 Score 함수가 일종의 "암묵적 메커니즘"이었다. Transformer(2017)는 이를 Q·K·V라는 명시적인 세 가지 구성 요소로 체계화했다.

이 체계화의 핵심 장점은 세 역할을 명확히 분리함으로써 다양한 변형과 확장이 가능해졌다는 것이다. Self-Attention(Q=K=V), Cross-Attention(Q≠K,V), Multi-Head Attention(여러 헤드의 QKV), Causal Attention(Q 마스킹) 등이 모두 같은 QKV 프레임워크에서 파생된다.

```text
Scaled Dot-Product Attention 연산 과정

입력: X (시퀀스, shape: [seq_len, d_model])

1. 투영 (Projection):
   Q = X · W_Q    (Query: 무엇을 찾는가?)
   K = X · W_K    (Key: 각 위치의 매칭 키)
   V = X · W_V    (Value: 실제 정보)

2. 유사도 계산:
   Score = Q · K^T / √d_k
   (√d_k로 나누는 이유: d_k가 크면 내적값이 커져 softmax 포화)

3. 정규화:
   Weight = softmax(Score)
   (각 행의 합 = 1.0, 확률적 가중치)

4. 정보 취합:
   Output = Weight · V
   (가중치가 높은 위치의 Value를 더 많이 가져옴)
```

- **📢 섹션 요약 비유**: Q는 도서관에서 <strong>검색어(질문)</strong>이고, K는 각 책의 <strong>태그(키워드)</strong>이며, V는 책의 <strong>실제 내용</strong>이다. 검색어와 태그가 매치될수록 그 책의 내용을 더 많이 참조한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Q·K·V의 역할 상세

| 구성 요소 | 의미 | 비유 | 계산 |
|:---|:---|:---|:---|
| **Query (Q)** | "무엇을 찾는가?" | 도서관 검색어 | X · W_Q |
| **Key (K)** | "각 위치의 특징" | 책 목록의 태그 | X · W_K |
| **Value (V)** | "실제 정보 내용" | 책의 본문 내용 | X · W_V |
| **Score** | Q와 K의 유사도 | 검색 일치도 | Q · K^T / √d_k |
| **Weight** | 정규화된 가중치 | 관련성 비율(%) | softmax(Score) |
| **Output** | 가중합 | 핵심 내용 요약 | Weight · V |

### Self vs Cross Attention의 QKV

| 유형 | Q 출처 | K, V 출처 | 적용 위치 |
|:---|:---|:---|:---|
| **Self-Attention** | **같은 시퀀스** | 같은 시퀀스 | Transformer 인코더·디코더 |
| **Cross-Attention** | 디코더 | **인코더** | Transformer 디코더 |
| **Masked Self-Attention** | 같은 시퀀스 | 같은 시퀀스 (미래 마스킹) | GPT 디코더 |

### √d_k 스케일링(Scaling)의 수학적 이유

d_k = 64일 때, Q와 K의 각 원소가 표준 정규 분포(평균 0, 분산 1)를 따른다면 Q·K^T의 분산은 d_k = 64가 된다. 표준 편차가 √64 = 8이므로, 소프트맥스 입력값이 ±8 범위에서 변동한다.

소프트맥스에 큰 값이 입력되면 특정 위치에 확률이 집중(포화)되어 기울기 소실이 발생한다. √d_k = 8로 나누면 분산을 다시 1로 정규화하여 안정적인 학습이 가능해진다.

```python
# PyTorch Scaled Dot-Product Attention 구현
import torch
import torch.nn.functional as F

def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.size(-1)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / (d_k ** 0.5)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    weights = F.softmax(scores, dim=-1)
    output = torch.matmul(weights, V)
    return output, weights
```

### Multi-Head Attention에서의 QKV 분할

Multi-Head Attention에서는 d_model 차원의 QKV를 h개 헤드로 분할한다.

```text
d_model = 512, h = 8헤드
각 헤드의 d_k = d_v = 512 / 8 = 64

헤드 i에서:
  Q_i = Q · W_Q_i    (shape: [seq, 64])
  K_i = K · W_K_i    (shape: [seq, 64])
  V_i = V · W_V_i    (shape: [seq, 64])
  head_i = Attention(Q_i, K_i, V_i)

최종 출력:
  MultiHead(Q,K,V) = Concat(head_1, ..., head_8) · W_O
```

- **📢 섹션 요약 비유**: √d_k는 시험 점수를 100점 만점으로 환산하는 것이다. 원점수가 수천 점이면 비교가 어렵지만, 100점으로 맞추면 비교 가능하다.

---

## Ⅲ. 비교 및 연결

| 비교 항목 | Additive (Bahdanau) | Dot-Product | Scaled Dot-Product |
|:---|:---|:---|:---|
| **계산 방식** | v^T·tanh(W[s;h]) | Q·K^T | **Q·K^T/√d_k** |
| **속도** | 느림 (tanh 포함) | 빠름 | **빠름** |
| **안정성** | 안정 | 불안정 (d_k 크면) | **안정** |
| **사용 모델** | Seq2Seq Attention | 초기 실험 | **Transformer 표준** |
| **병렬화** | 가능 | 가능 | **가능** |

### QKV 체계와 정보 검색의 유사성

QKV 시스템은 데이터베이스 검색과 개념적으로 유사하다.

- **하드 검색(Hard Retrieval, 데이터베이스)**: 키워드가 정확히 매치되어야 정보 반환
- **소프트 검색(Soft Retrieval, Attention)**: 유사도에 비례하여 모든 Value를 가중합 → 더 유연

이 개념은 이후 RAG(Retrieval-Augmented Generation)에서 벡터 유사도 검색으로 발전한다.

- **📢 섹션 요약 비유**: QKV는 도서관 사서와 같다. Query는 "공룡 그림책 주세요"이고, Key는 각 책의 분류 태그이고, Value는 책 내용이다. 사서(Attention)는 태그가 가장 잘 맞는 책을 우선 추천한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### QKV 파라미터 최적화 전략

```text
표준 Transformer 설정:
  d_model = 512, h = 8, d_k = d_v = 64
  파라미터: W_Q, W_K, W_V (각 d_model × d_k), W_O (h·d_v × d_model)

GPT-2 설정:
  d_model = 768, h = 12, d_k = 64

GPT-3 설정:
  d_model = 12288, h = 96, d_k = 128

효율화 방식:
  MQA (Multi-Query Attention): K,V 헤드 1개 공유
  GQA (Grouped Query Attention): K,V 헤드 g개 공유 (Llama 표준)
```

### 설계 판단 체크리스트

1. **d_k는 얼마로 설정할 것인가?** → 보통 64, √d_k 스케일링 필수
2. **헤드 수(h)는?** → d_model / h = d_k (정수여야 함)
3. **Self-Attention인가 Cross-Attention인가?** → 태스크에 따라 Q 출처 결정
4. **마스킹이 필요한가?** → 디코더(GPT)는 미래 마스킹 필수
5. **효율화가 필요한가?** → GQA·Flash Attention 고려

### 안티패턴

- **√d_k 스케일링 생략**: 학습 불안정, 소프트맥스 포화
- **Q=K=V라고 가중치 공유**: W_Q, W_K, W_V는 서로 다른 학습 가능 행렬
- **Cross-Attention에서 Q,K,V 출처 혼동**: Q는 디코더, K·V는 인코더

- **📢 섹션 요약 비유**: QKV를 이해하지 않고 Transformer를 쓰는 것은, 레시피 없이 요리하는 것이다. 결과물이 나오긴 하지만 왜 그런 결과가 나오는지 알 수 없다.

---

## Ⅴ. 기대효과 및 결론

### QKV 체계의 확장성

QKV 시스템은 하나의 통일된 프레임워크로 다양한 Attention 변형을 표현할 수 있는 범용성을 가진다.

| 확장 | 설명 |
|:---|:---|
| **Multi-Head Attention** | QKV를 h개로 분할, 다관점 병렬 처리 |
| **Cross-Attention** | Q 출처와 K·V 출처를 분리 |
| **Masked Attention** | 마스킹 행렬을 Score에 적용 |
| **Flash Attention** | QKV 연산의 메모리 효율 최적화 |
| **GQA / MQA** | K·V 헤드 수 감소로 추론 가속 |
| **Linear Attention** | Softmax를 선형 함수로 대체 O(n) |

QKV 시스템은 <strong>Transformer의 핵심 연산 단위</strong>이며, 이 구조의 이해가 BERT·GPT·ViT·Diffusion 등 모든 현대 AI 모델 이해의 출발점이다.

- **📢 섹션 요약 비유**: QKV는 Lego의 기본 블록이다. 이 블록 하나로 집(BERT), 성(GPT), 우주선(멀티모달)을 모두 만들 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **Query (Q)** | "무엇을 찾는가" (검색어) |
| **Key (K)** | "각 위치의 매칭 키" (태그) |
| **Value (V)** | "실제 정보" (내용) |
| **Scaled Dot-Product** | Q·K^T/√d_k, Transformer 표준 |
| **Multi-Head** | QKV를 h개 관점으로 병렬 처리 |
| **√d_k 스케일링** | softmax 포화 방지, 학습 안정화 |
| **Flash Attention** | QKV 연산 메모리 최적화 (IO-aware) |
| **GQA** | Key·Value 헤드 공유 (Llama, 효율화) |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Bahdanau Attention (2014)</div>
<div class="kb-diagram-note">→ 암묵적 Score 함수</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Luong Dot-Product (2015)</div>
<div class="kb-diagram-note">→ Q·K^T (명시적이나 미스케일)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Scaled Dot-Product (Transformer, 2017)</div>
<div class="kb-diagram-note">→ Q·K^T/√d_k, QKV 명시화</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Multi-Head Attention (2017)</div>
<div class="kb-diagram-note">→ QKV를 h개 관점으로 병렬 처리</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">MQA (Multi-Query, 2019)</div>
<div class="kb-diagram-note">→ K·V 1개 헤드 공유</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">GQA (Grouped Query, Llama 2, 2023)</div>
<div class="kb-diagram-note">→ K·V g개 헤드 공유</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">현재: Flash Attention 2/3</div>
<div class="kb-diagram-note">→ IO-Aware QKV 연산, 서빙 최적화</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. Q는 도서관에서 <strong>"공룡"이라고 검색</strong>하는 거예요 (Query).
2. K는 각 책에 붙은 <strong>태그(키워드)</strong>예요. "공룡" 태그가 있는 책이 매치돼요.
3. V는 책의 <strong>실제 내용</strong>이에요. 매치된 책의 내용을 **더 많이 읽어서** 답을 만들어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 122 / 420

← **이전**: [121. 어텐션 메커니즘 (Attention Mechanism) - Seq2Seq 병목 해소·가중 컨텍스트](/knowledge-base/studynote/10_ai/02_dl_architecture_new/121_attention_mechanism/)
**다음**: [123. Transformer 아키텍처 - Self-Attention 기반 병렬 시퀀스 처리](/knowledge-base/studynote/10_ai/02_dl_architecture_new/123_transformer_architecture/) →

---
