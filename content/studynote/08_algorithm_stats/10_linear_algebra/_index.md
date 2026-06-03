+++
title = "10. 선형대수 기초 (Linear Algebra Fundamentals)"

[extra]
tags = ["studynote-algorithm-stats"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 선형대수(Linear Algebra)는 벡터·행렬·선형 변환을 다루는 수학으로, <strong>머신러닝에서 데이터는 벡터, 모델은 행렬 연산, 학습은 행렬의 최적화</strong>로 표현된다.
> 2. **가치**: 신경망의 순전파(Forward Pass)는 행렬 곱셈의 연쇄, 역전파(Backpropagation)는 야코비안(Jacobian) 행렬 계산, PCA는 고유값 분해(Eigen Decomposition)다 — ML의 모든 핵심 연산이 선형대수다.
> 3. **판단 포인트**: 고차원 벡터의 내적(Dot Product)이 유사도의 척도이며, 트랜스포머(Transformer)의 Attention이 바로 Query·Key 벡터의 내적 기반이다.

---

## Ⅰ. 핵심 개념

### 1. 벡터 (Vector)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-note">벡터 v =</div><div class="kb-diagram-node">v₁, v₂, ..., vₙ</div><div class="kb-diagram-note">ᵀ ∈ ℝⁿ</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">내적 (Dot Product): a·b = Σ aᵢbᵢ =</div><div class="kb-diagram-cell">a</div><div class="kb-diagram-cell">b</div><div class="kb-diagram-cell">cos(θ)</div></div>
<div class="kb-diagram-note">→ θ=0: 같은 방향 (유사도 최대)</div>
<div class="kb-diagram-note">→ θ=90°: 직교 (유사도 0)</div>
<div class="kb-diagram-note">→ θ=180°: 반대 방향 (유사도 최소)</div>
<div class="kb-diagram-note">L2 노름 (크기): ‖v‖ = √(v₁² + v₂² + ... + vₙ²)</div>
</div>
</div>



### 2. 행렬 연산



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">행렬 곱: C = A·B (A: m×k, B: k×n → C: m×n)</div>
<div class="kb-diagram-note">신경망 Forward Pass:</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">z = W·x + b</div><div class="kb-diagram-node">W: 가중치 행렬, x: 입력 벡터, b: 편향</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">a = σ(z)</div><div class="kb-diagram-node">σ: 활성화 함수</div></div>
<div class="kb-diagram-note">→ 레이어가 깊어질수록 행렬 곱 연쇄</div>
</div>
</div>



### 3. 고유값 분해 (Eigen Decomposition)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Av = λv (A: 정방행렬, v: 고유벡터, λ: 고유값)</div>
<div class="kb-diagram-note">활용:</div>
<div class="kb-diagram-tree-item" style="--depth:1">PCA: 공분산 행렬의 고유벡터 → 주성분 방향</div>
<div class="kb-diagram-tree-item" style="--depth:1">PageRank: 전이 행렬의 고유벡터 → 페이지 중요도</div>
<div class="kb-diagram-tree-item" style="--depth:1">행렬 거듭제곱 효율화 (A^n = Q·Λⁿ·Q⁻¹)</div>
</div>
</div>



### 4. 특이값 분해 (SVD, Singular Value Decomposition)

```text
A = U·Σ·Vᵀ

U: 좌 특이벡터 (열 공간 기저)
Σ: 특이값 대각행렬 (중요도 순 정렬)
V: 우 특이벡터 (행 공간 기저)

활용:
  - 추천 시스템 (행렬 분해)
  - 이미지 압축 (상위 k개 특이값만 사용)
  - 의사역행렬 (Pseudoinverse)
```

- **📢 섹션 요약 비유**: 내적은 **'두 화살표가 얼마나 같은 방향을 가리키는지 측정'** 입니다. Transformer의 Attention이 "어떤 단어가 현재 단어와 가장 관련 있는가?"를 찾기 위해 내적(cosine 유사도)을 사용하는 것과 같습니다.

---

## Ⅱ. ML에서의 선형대수 활용

### 핵심 연결

| ML 개념 | 선형대수 연산 |
|:---|:---|
| 신경망 순전파 | 행렬 곱셈 + 비선형 활성화 |
| 역전파 | 야코비안 행렬 × 연쇄 법칙 |
| PCA (차원 축소) | 공분산 행렬 고유값 분해 |
| SVD (추천 시스템) | 행렬 분해 A = U·Σ·Vᵀ |
| Attention (Transformer) | Q·Kᵀ / √dₖ 행렬 내적 |
| 선형 회귀 OLS | 정규 방정식 β = (XᵀX)⁻¹Xᵀy |

### Gram-Schmidt 직교화



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">고차원 벡터를 서로 수직인(직교) 벡터 집합으로 변환</div>
<div class="kb-diagram-note">→ QR 분해의 기초</div>
<div class="kb-diagram-note">→ 수치적으로 안정된 선형 시스템 풀기</div>
</div>
</div>



- **📢 섹션 요약 비유**: SVD는 **'복잡한 사진을 몇 가지 기본 패턴으로 분해하는 것'** 입니다. 얼굴 사진을 100개의 고유 패턴(특이벡터)으로 분해하면, 상위 10개만 써도 원본과 비슷한 얼굴이 복원됩니다 — 이것이 이미지 압축과 추천 시스템의 원리입니다.

---

## Ⅲ. 기대효과 및 결론

선형대수는 **"AI의 수학적 심장"** 이다. GPU가 행렬 연산에 최적화된 이유, 딥러닝이 병렬 연산으로 학습할 수 있는 이유가 모두 선형대수로 귀결된다.

선형대수를 이해하면 신경망을 **"수십억 개의 행렬 연산의 최적화"** 로 볼 수 있어, 아키텍처 설계와 디버깅이 훨씬 직관적이 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **고유값 분해 (Eigen Decomposition)** | PCA·PageRank의 수학적 기초 |
| **SVD (특이값 분해)** | 추천 시스템·이미지 압축·의사역행렬 |
| **Attention Mechanism** | Q·Kᵀ 내적 기반 유사도 → Transformer의 핵심 |
| **경사 하강법 (Gradient Descent)** | 야코비안·헤시안 행렬 기반 최적화 |
| **행렬 분해** | LU·QR·Cholesky — 선형 시스템 효율적 풀이 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">벡터·행렬 기초 (내적·행렬 곱·역행렬)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">고유값 분해 → PCA (주성분 분석)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">SVD (특이값 분해) → 행렬 인수분해 → 추천 시스템</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">신경망 = 행렬 곱 연쇄 → GPU 병렬 가속</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Attention = 내적 기반 유사도 → Transformer → LLM</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 선형대수는 **'숫자 박스(행렬)로 하는 계산'** 이에요. AI가 사진을 인식할 때는 사진을 숫자 박스로 만들어서 수천 번의 행렬 계산을 해요!
2. 내적은 **'두 화살이 얼마나 같은 방향을 가리키는지'** 측정하는 거예요. 챗봇이 "안녕"과 "hello"가 비슷한 의미인지 알 때 이 방법을 써요!
3. 선형대수를 이해하면 **AI가 왜 GPU로 빠르게 학습하는지** 알 수 있어요. GPU가 행렬 계산을 동시에 수천 개 처리하기 때문이에요!
