+++
weight = 122
title = "122. Q·K·V 시스템 (Query·Key·Value) - Attention의 핵심 연산 구조"
date = "2026-04-19"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Q(Query)·K(Key)·V(Value)는 **Attention 연산의 3대 구성 요소**로, Query가 "무엇을 찾는가", Key가 "각 위치의 매칭 키", Value가 "실제 정보"를 담당한다. $\text{Attention}(Q,K,V) = \text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$
> 2. **가치**: Bahdanau Attention은 Score 함수가 암묵적이었으나, QKV 분리로 **Query·Key로 유사도를 계산하고 Value에서 정보를 가져오는** 명시적 구조가 되어 Multi-Head Attention·Cross-Attention 등 **다양한 확장이 가능**해졌다.
> 3. **판단 포인트**: Self-Attention에서는 Q=K=V(같은 시퀀스에서 생성), Cross-Attention에서는 Q(디코더)≠K,V(인코더)이며, $\sqrt{d_k}$로 나누는 것은 **내적 값이 커져 softmax가 포화되는 것을 방지**하기 위함이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Scaled Dot-Product Attention                       │
├───────────────────────────────────────────────────────┤
│  입력: X (시퀀스)                                     │
│  Q = X · W_Q  (무엇을 찾는가?)                        │
│  K = X · W_K  (각 위치의 매칭 키)                     │
│  V = X · W_V  (실제 정보)                             │
│                                                       │
│  Score = Q · K^T / √d_k  (유사도)                     │
│  Weight = softmax(Score)  (가중치)                     │
│  Output = Weight · V      (가중 합)                    │
│                                                       │
│  → Q와 K가 유사한 위치의 V 정보를 더 많이 가져옴     │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Q는 도서관에서 **검색어(질문)**이고, K는 각 책의 **태그(키워드)**이며, V는 책의 **실제 내용**이다. 검색어와 태그가 매치될수록 그 책의 내용을 더 많이 참조한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Self vs Cross Attention의 QKV

| 유형 | Q 출처 | K, V 출처 |
|:---|:---|:---|
| **Self-Attention** | **같은 시퀀스** | 같은 시퀀스 |
| **Cross-Attention** | 디코더 | **인코더** |

### √d_k 스케일링 이유
- d_k가 크면 Q·K^T 내적값이 커져 softmax 출력이 0/1에 집중(포화).
- √d_k로 나누어 **기울기 소실을 방지**하고 학습을 안정화.

- **📢 섹션 요약 비유**: √d_k는 시험 점수를 100점 만점으로 환산하는 것이다. 원점수가 수천 점이면 비교가 어렵지만, 100점으로 맞추면 비교 가능하다.

---

## Ⅲ. 비교 및 연결

| 비교 | Additive (Bahdanau) | Dot-Product | Scaled Dot-Product |
|:---|:---|:---|:---|
| **계산** | v^T·tanh(W[s;h]) | Q·K^T | **Q·K^T/√d_k** |
| **속도** | 느림 | 빠름 | **빠름** |
| **사용** | Seq2Seq | - | **Transformer** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### Multi-Head Attention
- QKV를 **h개 헤드로 분할**하여 각 헤드가 다른 관점으로 Attention → 결합.
- "문법 관계", "의미 관계" 등 **다양한 패턴을 동시에 포착**.

---

## Ⅴ. 기대효과 및 결론

QKV 시스템은 **Transformer의 핵심 연산 단위**이며, 이 구조의 이해가 BERT·GPT·ViT·Diffusion 등 모든 현대 AI 모델 이해의 출발점이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Query** | "무엇을 찾는가" (검색어) |
| **Key** | "각 위치의 매칭 키" (태그) |
| **Value** | "실제 정보" (내용) |
| **Scaled Dot-Product** | Q·K^T/√d_k, Transformer 표준 |
| **Multi-Head** | QKV를 h개 관점으로 병렬 처리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Bahdanau Attention (2014) — 암묵적 Score]
    │
    ▼
[Luong Dot-Product (2015) — Q·K^T]
    │
    ▼
[Scaled Dot-Product (Transformer, 2017) — QKV 명시화]
    │
    ▼
[Multi-Head Attention — 다관점 병렬 Attention]
    │
    ▼
[현재: Flash Attention / GQA — 효율적 QKV 연산]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Q는 도서관에서 **"공룡"이라고 검색**하는 거예요 (Query).
2. K는 각 책에 붙은 **태그(키워드)**예요. "공룡" 태그가 있는 책이 매치돼요.
3. V는 책의 **실제 내용**이에요. 매치된 책의 내용을 **더 많이 읽어서** 답을 만들어요!
