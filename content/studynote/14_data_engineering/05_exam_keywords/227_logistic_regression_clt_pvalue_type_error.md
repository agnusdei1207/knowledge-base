+++
title = "227. 로지스틱 회귀 (Logistic Regression) CLT p-value 1/2종 오류"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 로지스틱 회귀(Logistic Regression)는 선형 회귀의 출력을 [시그모이드](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)([Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)) 함수로 압축해 0~1 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)을 예측하는 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 모델이며, 우도 최대화([MLE](/knowledge-base/studynote/08_algorithm_stats/08_stats/143_mle/), Maximum Likelihood Estimation)로 계수를 추정한다.
> 2. **가치**: 중심극한정리([CLT](/knowledge-base/studynote/08_algorithm_stats/08_stats/139_clt/), Central Limit Theorem)는 표본 통계량의 정규분포 수렴 성질로 가설검정의 수학적 토대를 제공하며, p-value와 1/2종 오류 이해는 올바른 통계적 의사결정의 핵심이다.
> 3. **판단 포인트**: [p-value](/knowledge-base/studynote/06_ict_convergence/05_data_science/337_p_value_significance/) < 0.05는 "유의하다"는 의미이지만 "맞다"는 의미가 아니며, 1종 오류(거짓 양성)와 2종 오류(거짓 음성)의 트레이드오프를 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 맥락에 맞게 조정해야 한다.

---

## Ⅰ. 개요 및 필요성

### 왜 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 문제에 선형 회귀를 쓰면 안 되는가?

선형 회귀(y = β₀ + β₁x)의 출력은 -∞ ~ +∞다. 이메일 스팸 여부(0 또는 1)를 예측하는데 출력이 -0.3이나 1.7이면 의미가 없다. 로지스틱 회귀는 [시그모이드](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/) 함수로 이 문제를 해결한다.

```
선형 회귀 출력범위: -∞ ~ +∞  (연속 예측에 적합)
로지스틱 회귀 출력: 0 ~ 1    (확률 예측, 이진 분류에 적합)
```

📢 **섹션 요약 비유**: 선형 회귀는 "수직선 위에서 위치를 예측"하고, 로지스틱 회귀는 "0과 1 사이의 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 문으로 통과 여부를 판단"한다. 거리를 재는 자와 O/X 판단 도구의 차이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. 로지스틱 회귀 수식



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">시그모이드 함수 (Sigmoid Function):</div>
<div class="kb-diagram-note">1</div>
<div class="kb-diagram-note">P(Y=1|x) =</div>
<div class="kb-diagram-note">1 + e^(-(β₀+β₁x))</div>
<div class="kb-diagram-note">출력: 0 ~ 1 사이의 확률값</div>
<div class="kb-diagram-note">로짓 (Logit) 변환:</div>
<div class="kb-diagram-note">P</div>
<div class="kb-diagram-note">log ( ) = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ</div>
<div class="kb-diagram-note">1 - P</div>
<div class="kb-diagram-note">오즈비 (Odds Ratio, OR): e^βᵢ</div>
<div class="kb-diagram-note">β₁ = 0.5라면 OR = e^0.5 ≈ 1.65</div>
<div class="kb-diagram-note">→ x₁이 1 증가할 때 오즈가 1.65배 증가</div>
</div>
</div>



### 2-2. [MLE](/knowledge-base/studynote/08_algorithm_stats/08_stats/143_mle/) (Maximum Likelihood Estimation, 우도 최대화)

선형 회귀는 OLS(최소제곱법)로 계수를 구하지만, 로지스틱 회귀는 MLE를 사용한다.

```
로그 우도 함수 (Log-Likelihood):
L(β) = Σ[yᵢ log P(xᵢ) + (1-yᵢ) log(1 - P(xᵢ))]

목표: L(β)를 최대화하는 β를 경사하강법(Gradient Descent)으로 탐색

손실 함수 = Binary Cross-Entropy Loss (이진 교차 엔트로피)
           = -L(β)    ← 최소화 방향
```

### 2-3. 중심극한정리 ([CLT](/knowledge-base/studynote/08_algorithm_stats/08_stats/139_clt/), Central Limit Theorem)

가설검정의 수학적 기반이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">CLT 핵심 명제:</div>
<div class="kb-diagram-note">모집단이 어떤 분포를 따르더라도,</div>
<div class="kb-diagram-note">표본 크기 n이 충분히 크면(보통 n ≥ 30),</div>
<div class="kb-diagram-note">표본 평균의 분포는 정규분포 N(μ, σ²/n)에 수렴한다.</div>
<div class="kb-diagram-note">의의: 모집단 분포를 몰라도 표본 통계량으로 모수를 추정 가능</div>
</div>
</div>



### 2-4. [p-value](/knowledge-base/studynote/06_ict_convergence/05_data_science/337_p_value_significance/) 정확한 해석

```
p-value 정의:
귀무가설(H₀)이 참이라는 가정 하에,
현재 관측된 결과 이상으로 극단적인 결과가
나올 확률

해석 예시:
p = 0.03 → "귀무가설이 참이라면, 이 결과보다 극단적인 값이
             나올 확률은 3%다. 즉, 매우 드문 결과이므로
             귀무가설을 기각한다."

[자주 하는 오해]
p = 0.03 ≠ "귀무가설이 참일 확률이 3%"
p = 0.03 ≠ "효과가 진짜일 확률이 97%"
p = 0.03 ≠ "연구 결과가 재현될 확률이 97%"
```

### 2-5. 1종 오류 vs 2종 오류



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">실제 현실</div>
<div class="kb-diagram-note">H₀ 참 H₁ 참(H₀ 거짓)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">검정</div><div class="kb-diagram-cell">H₀ 기각</div><div class="kb-diagram-cell">1종 오류 (α)</div><div class="kb-diagram-cell">올바른 검출 (검정력, 1-β)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">결과</div><div class="kb-diagram-cell">H₀ 채택</div><div class="kb-diagram-cell">올바른 채택</div><div class="kb-diagram-cell">2종 오류 (β)</div></div>
<div class="kb-diagram-note">1종 오류 (Type I Error, 거짓 양성, False Positive):</div>
<div class="kb-diagram-note">→ 실제로 효과 없는데 있다고 판단 (경보 오발령)</div>
<div class="kb-diagram-note">→ α = 유의수준 (보통 0.05)</div>
<div class="kb-diagram-note">2종 오류 (Type II Error, 거짓 음성, False Negative):</div>
<div class="kb-diagram-note">→ 실제로 효과 있는데 없다고 판단 (탐지 실패)</div>
<div class="kb-diagram-note">→ β = 오류율, 검정력(Power) = 1 - β</div>
</div>
</div>



| 상황 | 더 위험한 오류 | 이유 |
|:---|:---|:---|
| 신약 임상시험 | 2종 오류 (치료 효과 놓침) | 환자 치료 기회 상실 |
| [바이러스](/knowledge-base/studynote/02_operating_system/10_security/589_virus/) 감지 (보안) | 2종 오류 (위협 놓침) | 침해 허용 |
| 스팸 필터 | 1종 오류 (정상 메일 차단) | 업무 메일 손실 |
| 품질 검사 (제조) | 2종 오류 (불량품 통과) | 리콜·안전사고 |

📢 **섹션 요약 비유**: 1종 오류는 "건강한 사람을 환자라고 진단하는 것"(불필요한 치료), 2종 오류는 "환자를 건강하다고 진단하는 것"(치료 기회 상실)이다. 어떤 오류가 더 위험한지는 상황에 따라 다르다.

---

## Ⅲ. 비교 및 연결

### 3-1. 로지스틱 회귀 vs 다른 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 모델

| 구분 | 로지스틱 회귀 | 의사결정트리 | [SVM](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) | 신경망 |
|:---|:---|:---|:---|:---|
| 해석 가능성 | 높음 (계수·OR 해석) | 높음 | 낮음 | 매우 낮음 |
| 선형 경계 | 선형만 가능 | 비선형 가능 | 커널로 비선형 | 비선형 |
| [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 출력 | 자연스러운 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) | 불순도 기반 | 경계 거리 기반 | [Softmax](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/) |
| 과적합 | 낮음 | 높음 ([가지치기](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/) 필요) | 중간 | 높음 |

### 3-2. 통계적 유의성의 한계 (p-hacking 문제)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">p-hacking (p-해킹) 시나리오:</div>
<div class="kb-diagram-note">1. 20개 가설을 동시에 검정 (α=0.05 각각 적용)</div>
<div class="kb-diagram-note">2. 기대 거짓 양성 수 = 20 × 0.05 = 1개</div>
<div class="kb-diagram-note">3. "우연히" 1개 유의한 결과 → 이것만 발표</div>
<div class="kb-diagram-note">→ 이것이 재현 불가 연구(Replication Crisis)의 원인</div>
<div class="kb-diagram-note">해결책:</div>
<div class="kb-diagram-tree-item" style="--depth:0">Bonferroni 보정: α를 검정 수로 나눔 (α/k)</div>
<div class="kb-diagram-tree-item" style="--depth:0">FDR (False Discovery Rate) 통제: Benjamini-Hochberg</div>
<div class="kb-diagram-tree-item" style="--depth:0">사전 등록(Pre-registration): 가설 먼저 공개</div>
</div>
</div>



### 3-3. 검정력 (Statistical [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/)) 설계



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Power = 1 - β = P(H₀ 기각 | H₁ 참)</div>
<div class="kb-diagram-note">검정력 높이는 방법:</div>
<div class="kb-diagram-note">① 표본 크기(n) 증가 ← 가장 직접적</div>
<div class="kb-diagram-note">② 유의수준(α) 증가 ← 1종 오류 증가 트레이드오프</div>
<div class="kb-diagram-note">③ 효과 크기 증가 ← 통제 불가</div>
<div class="kb-diagram-note">④ 측정 오차 감소 ← 실험 설계 개선</div>
</div>
</div>



📢 **섹션 요약 비유**: p-value는 "법정에서 알리바이가 없다는 것"이지, "범인이라는 증명"이 아니다. p < 0.05는 단지 "이 결과는 우연으로 설명하기 어렵다"는 뜻이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. 신용 대출 부도 예측 시나리오



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">목표</div><div class="kb-diagram-note">고객 특성으로 대출 부도 여부 예측</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">특성</div><div class="kb-diagram-note">소득(X₁), 대출 금액(X₂), 신용 등급(X₃), 고용 형태(X₄)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">로지스틱 회귀 결과</div></div>
<div class="kb-diagram-note">변수 계수(β) OR(e^β) p-value</div>
<div class="kb-diagram-note">소득 -0.8 0.45 &lt; 0.001 ← 소득 높을수록 부도 낮음</div>
<div class="kb-diagram-note">대출 금액 0.5 1.65 &lt; 0.001 ← 대출 클수록 부도 높음</div>
<div class="kb-diagram-note">신용 등급 -1.2 0.30 &lt; 0.001</div>
<div class="kb-diagram-note">고용(비정규) 0.9 2.46 0.023</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">임계값(Threshold) 설정</div></div>
<div class="kb-diagram-note">P ≥ 0.3 → 대출 거절 (낮은 임계값: 2종 오류 감소, 1종 오류 증가)</div>
<div class="kb-diagram-note">→ 금융기관은 대출 손실(2종 오류) 방지 우선</div>
</div>
</div>



### 4-2. ROC 커브 (Receiver Operating Characteristic Curve)와 AUC

임계값 변화에 따른 1종/2종 오류 트레이드오프를 시각화한다.

```
TPR (True Positive Rate = 민감도)  vs  FPR (False Positive Rate)
AUC (Area Under Curve) = 0.5 (랜덤) ~ 1.0 (완벽)
실무 기준: AUC ≥ 0.8 = 양호
```

📢 **섹션 요약 비유**: ROC 커브는 "보안 검색대의 민감도 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)"이다. 민감도를 높이면 범죄자를 더 잘 잡지만(2종 오류 감소), 무고한 여행자도 더 많이 걸린다(1종 오류 증가).

---

## Ⅴ. 기대효과 및 결론

로지스틱 회귀·[CLT](/knowledge-base/studynote/08_algorithm_stats/08_stats/139_clt/)·[p-value](/knowledge-base/studynote/06_ict_convergence/05_data_science/337_p_value_significance/)·오류 유형은 [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 시대에도 여전히 유효한 통계의 핵심 개념이다. 블랙박스 딥러닝 모델의 예측 결과를 검증하거나, 실험 결과를 보고할 때 반드시 필요한 언어이기 때문이다.

### 핵심 정리

| 개념 | 핵심 포인트 |
|:---|:---|
| 로지스틱 회귀 | [시그모이드](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/) 출력, [MLE](/knowledge-base/studynote/08_algorithm_stats/08_stats/143_mle/) 계수 추정, OR 해석 |
| [CLT](/knowledge-base/studynote/08_algorithm_stats/08_stats/139_clt/) | 충분한 표본 → 표본 평균 정규분포 수렴 |
| [p-value](/knowledge-base/studynote/06_ict_convergence/05_data_science/337_p_value_significance/) | 귀무가설 하 관측값 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/). "맞다"가 아님 |
| 1종 오류 | False Positive, α로 통제 |
| 2종 오류 | False Negative, β, 검정력(1-β) |
| AUC-ROC | 임계값 불문 모델 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 지표 |

📢 **섹션 요약 비유**: 통계 검정은 "망원경으로 별을 관측하는 것"과 같다. p-value는 "이 빛이 배경 잡음일 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)"이고, 효과 크기는 "별의 밝기"이며, 검정력은 "망원경의 해상도"다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 핵심 모델 | Logistic Regression (로지스틱 회귀) | 이진 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 예측 |
| 함수 | [Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/) Function ([시그모이드](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/)) | 0~1 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 변환 |
| 추정법 | [MLE](/knowledge-base/studynote/08_algorithm_stats/08_stats/143_mle/) (Maximum Likelihood Estimation) | 우도 최대화 계수 추정 |
| 이론 | [CLT](/knowledge-base/studynote/08_algorithm_stats/08_stats/139_clt/) (Central Limit Theorem) | 표본 평균 정규 수렴 이론 |
| 검정 | [p-value](/knowledge-base/studynote/06_ict_convergence/05_data_science/337_p_value_significance/) | 귀무가설 하 관측 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) |
| 오류 | Type I Error (1종 오류) | 거짓 양성, α |
| 오류 | Type II Error (2종 오류) | 거짓 음성, β |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | AUC-ROC | 임계값 독립 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) |
| 해석 | Odds Ratio (오즈비) | 로지스틱 계수 해석 |
| 문제 | p-hacking | 다중 검정 거짓 유의성 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. 로지스틱 회귀는 "내일 비가 올 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)이 70%다"처럼 0~100% [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)로 답을 내는 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 방법이다. 단순히 "0 또는 1"이 아니라 얼마나 확신하는지까지 알려준다.

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">선형 회귀 (연속값 예측)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">로지스틱 회귀: Sigmoid → 확률 출력 (이진 분류)</div>
<div class="kb-diagram-tree-item" style="--depth:2">CLT (중심극한정리) · 정규분포 가정</div>
<div class="kb-diagram-tree-item" style="--depth:2">p-value · 1종/2종 오류 · 임계값 결정</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">다중 분류: Softmax 회귀 · One-vs-Rest</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">비선형: SVM · 트리 계열 · 딥러닝</div>
</div>
</div>


2. p-value는 "이 실험 결과가 그냥 운으로 나올 가능성"인데, 이 가능성이 5%보다 작으면 "이건 진짜 효과가 있다"고 판단한다.
3. 1종 오류는 "정상인을 환자라고 부르는 실수"이고, 2종 오류는 "환자를 정상이라고 놓치는 실수"인데, 어느 실수가 더 위험한지는 상황마다 다르다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 227 / 258

← **이전**: [226. 피어슨 상관 (Pearson Correlation) 회귀 R² 결정계수 다중공선성 VIF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/226_pearson_correlation_regression_r2_vif_multicollinearity/)
**다음**: [228. PCA (Principal Component Analysis) LDA t-SNE 차원 축소](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/228_pca_lda_tsne_dimensionality_reduction/) →

---
