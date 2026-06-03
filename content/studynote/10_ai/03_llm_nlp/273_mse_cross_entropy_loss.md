+++
title = "273. MSE / 크로스 엔트로피 (Cross-Entropy) 손실 함수"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)([Loss Function](/knowledge-base/studynote/12_it_management/02_itsm_itil/087_loss_function/))는 모델의 예측값(ŷ)과 실제값(y) 사이의 오차를 수치화하여 학습 방향을 결정한다 — <strong><a href="/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/">MSE</a>(<a href="/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/">Mean Squared Error</a>)</strong>는 회귀에, <strong><a href="/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/">크로스 엔트로피</a>(<a href="/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/">Cross-Entropy</a>)</strong>는 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)에 각각 이론적으로 최적이다.
> 2. **가치**: [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) 선택이 학습 안정성과 속도에 직결된다 — [크로스 엔트로피](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/)는 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)에서 MSE보다 기울기가 더 명확하고 빠르게 수렴하며, KL 발산([KL Divergence](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/153_kl_divergence/))과의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 통해 정보 이론적 해석이 가능하다.
> 3. **판단 포인트**: [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 문제에 MSE를 사용하면 [Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/) 포화 구간에서 기울기가 거의 0이 되어 학습이 극히 느려지므로, 반드시 [크로스 엔트로피](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/)를 사용해야 하는 이론적 근거가 기술사 핵심 논점이다.

---

## Ⅰ. 개요 및 필요성

### [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)의 역할

[손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)([Loss Function](/knowledge-base/studynote/12_it_management/02_itsm_itil/087_loss_function/)) = 비용 함수(Cost Function) = 목적 함수(Objective Function):

```
학습 목표: W*, b* = argmin_{W,b} L(ŷ, y)

손실 함수의 조건:
  1. 미분 가능 (역전파 적용 위해)
  2. 예측이 정답에 가까울수록 손실 감소
  3. 문제 유형(회귀/분류)에 적합
```

### [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">손실 함수 분류</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">회귀용</div><div class="kb-diagram-cell">분류용</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">MSE (Mean Squared Error)</div><div class="kb-diagram-cell">Binary Cross-Entropy</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">MAE (Mean Absolute Err)</div><div class="kb-diagram-cell">Categorical Cross-Entropy</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Huber Loss</div><div class="kb-diagram-cell">Focal Loss (불균형 클래스)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">RMSE</div><div class="kb-diagram-cell">KL Divergence</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)는 요리 채점 기준 — 맛이 목표와 얼마나 다른지(오차)를 측정하는데, 달콤함을 겨루는 대회(회귀)와 국가 음식 맞추기 대회([분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/))는 다른 채점 기준([손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/))이 필요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [MSE](/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/) ([Mean Squared Error](/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/))

```
MSE = (1/n) × Σᵢ (yᵢ - ŷᵢ)²

n: 샘플 수
yᵢ: 실제값
ŷᵢ: 예측값

기울기: ∂MSE/∂ŷᵢ = -2/n × (yᵢ - ŷᵢ)
```

**특성**:
- 오차의 제곱 → 큰 오차 강하게 패널티
- [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)([Outlier](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/))에 민감 (제곱 효과)
- 연속적이고 미분 가능
- 최솟값이 하나 ([볼록 함수](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/164_convex_function/), Convex)

### MAE (Mean Absolute Error)

```
MAE = (1/n) × Σᵢ |yᵢ - ŷᵢ|

기울기: ∂MAE/∂ŷᵢ = -1/n × sign(yᵢ - ŷᵢ)
```

[MSE](/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/) vs MAE 비교:

| 항목 | [MSE](/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/) | MAE |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/">이상치</a> 민감도</strong> | 높음 (제곱) | 낮음 (절댓값) |
| **기울기** | 연속적 | x=0에서 미정의 (불연속) |
| **최적화** | 빠른 수렴 | 느린 수렴 |
| **선택 기준** | [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 없는 회귀 | [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 있는 회귀 |

### [크로스 엔트로피](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/) ([Cross-Entropy](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/))

<strong>이진 <a href="/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/">크로스 엔트로피</a> (Binary <a href="/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/">Cross-Entropy</a>, BCE)</strong>:

```
BCE = -(1/n) × Σᵢ [yᵢ log(ŷᵢ) + (1-yᵢ) log(1-ŷᵢ)]

yᵢ ∈ {0, 1}, ŷᵢ ∈ (0, 1)

기울기 (Sigmoid 출력층 결합 시):
∂BCE/∂z = ŷ - y   ← 매우 단순!
```

<strong>범주형 <a href="/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/">크로스 엔트로피</a> (Categorical <a href="/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/">Cross-Entropy</a>, CCE)</strong>:

```
CCE = -(1/n) × Σᵢ Σₖ yᵢₖ log(ŷᵢₖ)

yᵢₖ: 클래스 k에 대한 원핫 인코딩 (0 또는 1)
ŷᵢₖ: Softmax 출력 확률

기울기 (Softmax 결합 시):
∂CCE/∂zₖ = ŷₖ - yₖ   ← 역시 단순!
```

### [MSE](/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/) vs [크로스 엔트로피](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/): [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)에서 왜 CE가 더 나은가?



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">MSE vs Cross-Entropy 기울기 비교 (분류 문제)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">분류 출력층: Sigmoid + MSE</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">∂MSE/∂W = (ŷ - y) × σ'(z) × x</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↑ σ'(z)은 포화 구간에서 ≈ 0 → 기울기 소멸!</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">분류 출력층: Sigmoid + BCE</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">∂BCE/∂W = (ŷ - y) × x ← σ'(z) 항이 제거됨!</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↑ 항상 명확한 기울기 (포화 구간에서도)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Softmax + CCE도 동일: ∂CCE/∂W = (ŷ - y) × x</div></div>
</div>
</div>



수학적 이유: BCE와 CE의 미분에서 [Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)/Softmax의 도함수가 상쇄되어 깔끔한 기울기가 남는다.

- **📢 섹션 요약 비유**: CE는 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)를 위해 설계된 잣대 — MSE로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)를 평가하는 것은 달리기 대회를 수영 기술로 채점하는 것처럼 맞지 않고, CE는 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 문제에서 기울기를 명확하게 유지해 빠른 학습을 가능하게 한다.

---

## Ⅲ. 비교 및 연결

### KL 발산 ([KL Divergence](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/153_kl_divergence/))과 [크로스 엔트로피](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/) [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">KL 발산 (Kullback-Leibler Divergence):</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DKL(P</div><div class="kb-diagram-cell">Q) = Σ P(x) log(P(x)/Q(x))</div></div>
<div class="kb-diagram-note">= Σ P(x) log P(x) - Σ P(x) log Q(x)</div>
<div class="kb-diagram-note">= -H(P) + H(P, Q)</div>
<div class="kb-diagram-note">여기서:</div>
<div class="kb-diagram-note">H(P) : P의 엔트로피 (Entropy, 고정값)</div>
<div class="kb-diagram-note">H(P, Q) : 크로스 엔트로피 (P를 기준으로 Q 평가)</div>
<div class="kb-diagram-note">→ KL 발산 최소화 = 크로스 엔트로피 최소화 (P 고정 시)</div>
<div class="kb-diagram-note">→ 분류 학습은 예측 분포 Q를 실제 분포 P에 가깝게 만드는 것</div>
</div>
</div>



### [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) 종합 비교

| [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) | 수식 (요약) | 문제 유형 | [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) | 기울기 특성 |
|:---|:---|:---|:---:|:---|
| <strong><a href="/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/">MSE</a></strong> | Σ(y-ŷ)²/n | 회귀 | 민감 | 연속적, 빠른 수렴 |
| **MAE** | Σ|y-ŷ|/n | 회귀 ([이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)) | 강건 | 불연속 (0에서) |
| **Huber** | 이차+일차 혼합 | 회귀 | 중간 | 연속, 강건 |
| **BCE** | -[y·log(ŷ)+(1-y)·log(1-ŷ)] | 이진 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | - | σ'(z) 상쇄, 명확 |
| **CCE** | -Σy·log(ŷ) | 다중 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | - | [Softmax](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/)' 상쇄, 명확 |
| **Focal Loss** | -(1-ŷ)^γ y·log(ŷ) | 불균형 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | - | 어려운 샘플 집중 |

- **📢 섹션 요약 비유**: [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)는 다른 경기의 다른 심판 기준 — MSE는 "목표물과의 거리"(회귀), CE는 "맞았냐 틀렸냐의 [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/)"([분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/))로 채점하며, 같은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 기준이 다르면 다른 결과를 낸다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사 시험 핵심 논점

1. <strong><a href="/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a>에 <a href="/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/">MSE</a> 사용 시 문제</strong>: [Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/) 포화 구간에서 σ'(z)≈0 → [MSE](/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/) 기울기≈0 → 학습 극히 느림 → BCE로 해결
2. <strong>CE와 KL 발산 <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a></strong>: H(P,Q) = H(P) + DKL(P||Q) → CE 최소화 = KL 발산 최소화
3. <strong>원핫 인코딩 (<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/079_one_hot_encoding_categorical_dummy_variable/">One-hot Encoding</a>)과 CCE</strong>: 실제 클래스만 y=1, 나머지 y=0 → CCE = -log(ŷ_correct) (정답 클래스의 log [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/))
4. **Focal Loss 등장 이유**: 클래스 불균형(Class Imbalance) 문제 → 쉬운 샘플(높은 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/))의 손실을 (1-ŷ)^γ로 down-weighting

### [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) 선택 가이드



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">문제 유형 결정 트리:</div>
<div class="kb-diagram-tree-item" style="--depth:0">연속값 예측 (회귀)?</div>
<div class="kb-diagram-note">── 이상치 있음? → Huber Loss 또는 MAE</div>
<div class="kb-diagram-note">── 이상치 없음? → MSE</div>
<div class="kb-diagram-tree-item" style="--depth:0">클래스 예측 (분류)?</div>
<div class="kb-diagram-tree-item" style="--depth:3">이진 (0/1)? → Binary CE + Sigmoid</div>
<div class="kb-diagram-tree-item" style="--depth:3">다중 클래스? → Categorical CE + Softmax</div>
<div class="kb-diagram-tree-item" style="--depth:3">다레이블? → Binary CE × K개 + Sigmoid</div>
<div class="kb-diagram-tree-item" style="--depth:3">클래스 불균형? → Focal Loss</div>
</div>
</div>



- **📢 섹션 요약 비유**: [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) 선택은 병원에서 올바른 검사 기준 사용 — 혈당 검사([MSE](/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/))로 골밀도([분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 문제)를 측정하면 엉뚱한 결과가 나오듯, 문제 유형에 맞는 [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)를 써야 정확한 학습이 된다.

---

## Ⅴ. 기대효과 및 결론

### [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)별 특성 요약



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">MSE vs Cross-Entropy 특성 비교 요약</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">MSE (회귀): Cross-Entropy (분류):</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">L = Σ(y-ŷ)²/n</div><div class="kb-diagram-cell">L = -Σ y·log(ŷ)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">볼록 함수 ✓</div><div class="kb-diagram-cell">볼록 함수 ✓</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">이상치 민감 ⚠</div><div class="kb-diagram-cell">이상치 영향 적음 ✓</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">분류에 느림 ❌</div><div class="kb-diagram-cell">분류에 최적 ✓</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">기울기: 연속 ✓</div><div class="kb-diagram-cell">기울기: ŷ-y (간단) ✓</div></div>
</div>
</div>



### 기대효과

| 효과 | 올바른 [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) 선택 시 |
|:---|:---|
| **학습 수렴 속도** | CE 사용 시 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 문제에서 [MSE](/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/) 대비 수십 배 빠른 수렴 |
| **기울기 안정성** | CE + [Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)/[Softmax](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/) 조합의 깔끔한 기울기로 안정적 학습 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 최적화</strong> | 문제에 맞는 손실로 모델 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 극대화 |
| **해석 가능성** | CE = 정보 이론적 불확실성 감소 → 직관적 해석 |

### 결론

[손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)는 신경망이 "무엇을 잘해야 하는지"를 정의하는 핵심 요소다. MSE는 회귀 문제에, [크로스 엔트로피](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/)는 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 문제에 이론적으로 최적이며, 이 선택은 수학적으로 KL 발산 최소화와 동치다. 특히 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 문제에서 [MSE](/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/) 대신 CE를 사용해야 하는 이유([Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/) 포화 기울기 소멸 방지)는 기술사 시험에서 매우 빈번하게 출제되는 핵심 논점이다.

- **📢 섹션 요약 비유**: 올바른 [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)를 고르는 것은 올바른 나침반을 고르는 것 — 회귀라는 사막을 걸을 때는 [MSE](/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/)(거리 측정), [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)라는 바다를 항해할 때는 CE(방향 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/))가 더 정확한 길을 안내한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [MSE](/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/) ([Mean Squared Error](/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/)) | 회귀, (y-ŷ)², [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 민감 / 회귀 문제의 표준 [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) |
| MAE (Mean Absolute Error) | y-ŷ / , [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 강건 / MSE의 [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 강건 대안 |
| 이진 [크로스 엔트로피](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/) (BCE) | [Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/), 이진 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) / 이진 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 표준 [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) |
| 범주형 [크로스 엔트로피](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/) (CCE) | [Softmax](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/), 원핫 인코딩 / 다중 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 표준 [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) |
| KL 발산 ([KL Divergence](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/153_kl_divergence/)) | 정보 이론, 분포 거리 / CE = [엔트로피](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/151_entropy/) + KL 발산 |
| Focal Loss | 클래스 불균형, (1-ŷ)^γ / 어려운 샘플 집중 [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] → [MSE / 크로스 엔트로피 (Cross-Entropy) 손실 함수] → [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. ⚖️ **"다른 게임은 다른 점수판"**
2. 다트 게임(회귀)은 과녁 중심에서 얼마나 멀었는지([MSE](/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/))로 점수를 매겨요 — 멀수록 큰 감점이에요.
3. OX 퀴즈([분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/))는 맞았냐 틀렸냐 + 얼마나 확신했냐([크로스 엔트로피](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/))로 채점해요 — "맞다고 100% 확신했는데 틀리면" 엄청 큰 패널티!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 273 / 420

← **이전**: [272. 역전파 (Backpropagation)](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/)
**다음**: [274. 옵티마이저 (Optimizer)](/knowledge-base/studynote/10_ai/03_llm_nlp/274_optimizer_learning_rate/) →

---
