+++
weight = 129
title = "129. Position-wise FFN - Transformer 내 2층 MLP 비선형 변환"
date = "2026-04-19"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Position-wise FFN은 [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] 블록에서 [[124_self_attention|Self-Attention]] 후 **각 위치에 독립적으로 적용되는 2층 MLP(Linear→[[269_relu_activation|ReLU]]→Linear)**이며, 비선형 변환과 표현력 확장을 담당한다.
> 2. **가치**: Self-Attention만으로는 **선형 변환의 합**에 불과하므로, FFN의 비선형 활성화([[269_relu_activation|ReLU]]/GELU)가 있어야 복잡한 패턴을 학습할 수 있다.
> 3. **판단 포인트**: FFN의 내부 차원(d_ff)은 보통 d_model×4이며, 최신 LLM에서는 **SwiGLU 활성화**로 [[282_performance_tactics|성능]]을 개선한다.

---

## Ⅰ. 개요 및 필요성

```text
FFN(x) = W₂ · ReLU(W₁ · x + b₁) + b₂
d_model=512, d_ff=2048 (4배 확장 후 축소)
```

- **📢 섹션 요약 비유**: FFN은 Attention이 모은 정보를 **믹서기(비선형 변환)**에 넣어 새로운 형태로 바꾸는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 요소 | 역할 |
|:---|:---|
| **W₁ (d→4d)** | 차원 확장 |
| **[[269_relu_activation|ReLU]]/GELU** | 비선형 활성화 |
| **W₂ (4d→d)** | [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]] |

### SwiGLU (최신)
- Llama·PaLM에서 사용. ReLU보다 [[282_performance_tactics|성능]]↑.

---

## Ⅲ. 비교 및 연결

| 비교 | Attention만 | Attention + FFN |
|:---|:---|:---|
| **비선형** | 없음 | **있음** |
| **표현력** | 제한적 | **풍부** |

---

## Ⅳ. 실무 적용 및 기술사 판단

- [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] 파라미터의 ~66%가 FFN에 집중.
- MoE(Mixture of Experts)는 FFN을 전문가로 분리하여 효율화.

---

## Ⅴ. 기대효과 및 결론

FFN은 **Transformer의 비선형 표현력을 담당하는 핵심 구성 요소**이며, SwiGLU·MoE로 효율화·[[282_performance_tactics|성능]] 개선이 [[216_progress_in_synchronization|진행]]되고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **FFN** | 2층 MLP (비선형 변환) |
| **[[269_relu_activation|ReLU]]/GELU** | [[129_activation_function|활성화 함수]] |
| **SwiGLU** | 최신 활성화 (Llama) |
| **MoE** | FFN을 전문가로 분리 |
| **d_ff** | FFN 내부 차원 (d_model×4) |

### 📈 관련 키워드 및 발전 흐름도

```text
[MLP (1986)] → [Transformer FFN (2017)] → [GELU (2018)]
    → [SwiGLU (2022, PaLM/Llama)] → [현재: MoE FFN — 희소 전문가]
```

### 👶 어린이를 위한 3줄 비유 설명
1. FFN은 **믹서기**예요. Attention이 모은 재료를 **섞어서 새로운 맛**을 만들어요.
2. 믹서기(비선형)가 없으면 재료를 **그냥 쌓기만** 해서 맛이 단조로워요.
3. 좋은 믹서기(SwiGLU)를 쓰면 **더 맛있는(정확한) 결과**가 나온답니다!
