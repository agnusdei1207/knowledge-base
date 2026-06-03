+++
title = "230. SVD (Singular Value Decomposition) 행렬 분해 랜덤 포레스트 XGBoost 부스팅"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SVD(Singular Value Decomposition, [특이값 분해](/knowledge-base/studynote/10_ai/05_data_science_ml/342_svd/))는 임의의 행렬을 세 행렬의 곱으로 분해하여 잠재 구조를 추출하며, 이를 추천·[압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)·노이즈 제거에 활용한다.
> 2. **가치**: [랜덤 포레스트](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/)([Random Forest](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/))의 [배깅](/knowledge-base/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/)([Bagging](/knowledge-base/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/), Bootstrap Aggregating)과 XGBoost의 그레이디언트 [부스팅](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/127_boosting/)([Gradient Boosting](/knowledge-base/studynote/10_ai/01_ai_basics/034_gradient_boosting/))은 [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/)([Ensemble](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/)) 학습의 두 축으로, 개별 모델의 편향([Bias](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/094_bias/))과 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)([Variance](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/))을 각각 다른 방향으로 감소시킨다.
> 3. **판단 포인트**: [배깅](/knowledge-base/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/)([랜덤 포레스트](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/))은 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 학습으로 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)을 줄이고, [부스팅](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/127_boosting/)(XGBoost)은 순차 학습으로 편향을 줄인다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 노이즈 많으면 [랜덤 포레스트](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/), 정제된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 극대화엔 XGBoost가 유리하다.

---

## Ⅰ. 개요 및 필요성

### [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 학습의 철학

"여러 약한 예측기(Weak Learner)의 집단 지성이 하나의 강한 예측기(Strong Learner)를 능가한다"는 원리가 [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 학습의 핵심이다.

```
단일 모델의 한계:
┌──────────────────────────────────────────────────────────────┐
│ 높은 편향(High Bias)   : 학습 데이터도 잘 못 맞춤 → 과소적합 │
│ 높은 분산(High Variance): 새 데이터에 불안정   → 과적합      │
└──────────────────────────────────────────────────────────────┘

앙상블 전략:
  배깅 (Bagging) → 분산(Variance) 감소 → 랜덤 포레스트
  부스팅 (Boosting) → 편향(Bias) 감소 → XGBoost, AdaBoost
  스태킹 (Stacking) → 여러 모델 결합 → 메타 학습기
```

📢 **섹션 요약 비유**: [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 학습은 "혼자 결정하지 않고 여러 전문가의 의견을 종합하는 위원회 제도"다. 전문가가 각자 다른 시각으로 판단하기 때문에 집단 실수 확률이 낮아진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. SVD (Singular Value Decomposition, [특이값 분해](/knowledge-base/studynote/10_ai/05_data_science_ml/342_svd/))

```
임의의 m×n 행렬 A를 다음으로 분해:

A (m×n) = U (m×m) × Σ (m×n) × Vᵀ (n×n)

┌────────────────────────────────────────────────────────┐
│ U: 왼쪽 특이벡터 (Left Singular Vectors)               │
│    m×m 직교행렬 (열벡터가 서로 수직)                   │
│                                                        │
│ Σ: 특이값 대각행렬 (Singular Value Matrix)              │
│    대각원소 σ₁ ≥ σ₂ ≥ ... ≥ σₙ ≥ 0 (내림차순)         │
│    특이값 크기 = 해당 축의 정보량                       │
│                                                        │
│ Vᵀ: 오른쪽 특이벡터 (Right Singular Vectors)           │
│     n×n 직교행렬                                       │
└────────────────────────────────────────────────────────┘

Truncated SVD (절단 SVD): 상위 k개만 유지
A ≈ Uₖ × Σₖ × Vₖᵀ  → 데이터 압축·잠재 구조 추출
```

SVD와 [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/):
- 사용자-아이템 행렬 R ≈ P × Qᵀ
- P: 사용자 잠재 요인 벡터 (User Latent Factor)
- Q: 아이템 잠재 요인 벡터 (Item Latent Factor)

### 2-2. [랜덤 포레스트](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/) ([Random Forest](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/)) — [배깅](/knowledge-base/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/) [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/)

```
배깅 (Bagging, Bootstrap Aggregating):
────────────────────────────────────────────────────────
원본 데이터 D
    │
    ├── Bootstrap 샘플 D₁ → 의사결정트리 T₁
    ├── Bootstrap 샘플 D₂ → 의사결정트리 T₂
    ├── Bootstrap 샘플 D₃ → 의사결정트리 T₃
    │   ...
    └── Bootstrap 샘플 Dₙ → 의사결정트리 Tₙ

Bootstrap: 복원 추출로 원본과 동일 크기의 샘플 생성
           약 63.2% 원본 포함, 36.8% 미포함 (OOB: Out-of-Bag)

최종 예측:
  분류: 다수결 투표 (Majority Voting)
  회귀: 평균 (Averaging)
```

<strong><a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/">랜덤 포레스트</a> 추가 무작위성</strong>: 각 분기(Split)마다 전체 특성 중 √d개([분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)) 또는 d/3개(회귀)만 후보로 사용 → 트리 간 상관 감소 → [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 더 감소

| 하이퍼파라미터 | 설명 | 기본값/범위 |
|:---|:---|:---|
| n_estimators | 트리 수 | 100~1000 |
| max_depth | 트리 최대 깊이 | None (무제한) |
| max_features | 분기 시 후보 특성 수 | sqrt(d) |
| min_samples_split | 분기 최소 샘플 수 | 2 |
| oob_score | OOB [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 사용 여부 | False |

### 2-3. XGBoost — 그레이디언트 [부스팅](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/127_boosting/)

```
부스팅 (Boosting) 흐름:
────────────────────────────────────────────────────────
단계 1: 초기 예측 f₀(x) = 상수 (평균값)
단계 2: 잔차(Residual) = 실제값 - 예측값
단계 3: 잔차를 학습하는 새 트리 추가
단계 4: 모든 트리 예측 합산
    ...반복...

XGBoost (eXtreme Gradient Boosting) 특징:
  - 목적함수 = 손실함수 + 정규화항 (트리 복잡도 페널티)
  - 2차 테일러 근사로 더 정확한 기울기 계산
  - Column Subsampling, Row Subsampling 지원
  - 병렬 처리 (특성 분기점 탐색 병렬화)
  - Pruning (전정): 음수 gain이면 가지 제거

학습률 (Learning Rate, η):
  f(x) = f₀ + η·h₁ + η·h₂ + ...
  η 작으면: 과적합 방지, 트리 수 증가 필요
  η 크면: 빠른 학습, 과적합 위험
```

| 하이퍼파라미터 | 설명 | 권장 범위 |
|:---|:---|:---|
| n_estimators | 트리 수 | 100~3000 |
| learning_rate (η) | [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) | 0.01~0.3 |
| max_depth | 트리 깊이 | 3~[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) |
| subsample | 행 서브샘플링 비율 | 0.6~1.0 |
| colsample_bytree | 열 서브샘플링 비율 | 0.6~1.0 |
| reg_alpha (L1) | L1 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) | 0~1 |
| reg_lambda (L2) | L2 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) | 1 |

📢 **섹션 요약 비유**: [부스팅](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/127_boosting/)은 "틀린 문제만 집중 연습하는 학생"이다. 1번 시도에서 틀린 것을 2번에서 집중 연습하고, 2번에서 틀린 것을 3번에서 집중한다. [배깅](/knowledge-base/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/)은 "여러 반 학생이 각자 공부해 다수결로 답 내는 것"이다.

---

## Ⅲ. 비교 및 연결

### 3-1. [편향-분산 트레이드오프](/knowledge-base/studynote/14_data_engineering/02_math_mining/110_bias_variance_tradeoff/) ([Bias-Variance Tradeoff](/knowledge-base/studynote/14_data_engineering/02_math_mining/110_bias_variance_tradeoff/))

```
예측 오차 분해:
E[(y - f̂(x))²] = Bias(f̂)² + Var(f̂) + 노이즈²

단순 모델 (선형회귀):
  높은 편향(Bias) + 낮은 분산(Var) → 과소적합

복잡 모델 (깊은 의사결정트리):
  낮은 편향(Bias) + 높은 분산(Var) → 과적합

앙상블 전략:
  배깅 → 분산 감소, 편향 유지
  부스팅 → 편향 감소, 분산 주의
```

### 3-2. [랜덤 포레스트](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/) vs XGBoost 비교

| 구분 | [랜덤 포레스트](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/) | XGBoost |
|:---|:---|:---|
| 학습 방식 | [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) (독립 트리) | 순차 (이전 트리 오류 학습) |
| 목표 | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)([Variance](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)) 감소 | 편향([Bias](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/094_bias/)) 감소 |
| 과적합 | 강건함 | 튜닝 필요 |
| 속도 | 빠름 ([병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화) | 느림 (순차), GPU로 가속 |
| 해석 | 특성 중요도 직관적 | 특성 중요도 + [SHAP](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/327_shap/) |
| 노이즈 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 강건함 | 민감할 수 있음 |
| 대회 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 안정적 | 최고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) (캐글 우승 모델) |

### 3-3. 특성 중요도 ([Feature Importance](/knowledge-base/studynote/10_ai/05_data_science_ml/355_random_forest_feature_importance/))

[랜덤 포레스트](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/)와 XGBoost 모두 특성 중요도를 제공한다.

| 방법 | 설명 | 특징 |
|:---|:---|:---|
| Impurity (불순도 기반) | 분기 시 불순도 감소량 합계 | 연속 특성 과대평가 경향 |
| Permutation Importance | 특성 순열 후 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 변화 | 더 신뢰할 수 있음 |
| [SHAP](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/327_shap/) ([SHapley Additive exPlanations](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/327_shap/)) | 각 예측에 특성별 기여도 | 가장 정확한 해석 |

📢 **섹션 요약 비유**: 특성 중요도는 "팀 성적에 각 선수가 얼마나 기여했는지 계산"하는 것이다. SHAP는 "각 경기에서 각 선수의 기여도를 개별적으로 측정"하는 가장 공정한 방법이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. 신용 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 예측 시나리오 (XGBoost)

```
[데이터] 50만 건 대출 신청 이력, 특성 120개

[전처리]
① 결측값 처리: XGBoost 내장 결측값 처리 활용
② 범주형 인코딩: Label Encoding

[XGBoost 학습]
n_estimators = 1000, learning_rate = 0.05
max_depth = 6, subsample = 0.8
Early Stopping: val loss 50회 미개선 시 중단

[결과]
AUC = 0.913, KS-통계량 = 0.42
SHAP 분석: 신용 등급 > 부채비율 > 연체 이력 순 중요도

[배포] Flask API + 실시간 예측 서빙
```

### 4-2. SVD 기반 [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/) 실제 구현

```
[Netflix 풍 추천 시스템]

행렬 R (사용자 × 영화) = P × Qᵀ + 편향

학습: ALS (Alternating Least Squares)
  P 고정 → Q 업데이트 (OLS)
  Q 고정 → P 업데이트 (OLS)
  ...반복...

정규화: λ(‖P‖² + ‖Q‖²) 추가 (과적합 방지)

추천: 사용자 i의 아이템 j 예측 점수 = pᵢ · qⱼᵀ + bᵢ + bⱼ
     (bᵢ: 사용자 편향, bⱼ: 아이템 편향)
```

📢 **섹션 요약 비유**: SVD 추천에서 잠재 요인은 "은밀한 영화 장르 코드"다. 공식 장르(액션·로맨스)가 아니라, "감성적이고 느린 템포"같은 측정 불가 특성을 수학이 자동으로 발견한다.

---

## Ⅴ. 기대효과 및 결론

SVD·[랜덤 포레스트](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/)·XGBoost는 현대 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 사이언스 현업에서 가장 많이 사용되는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 군에 속한다. 특히 XGBoost는 수년간 Kaggle 대회의 최강자로 군림하며 [정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/) 예측의 표준이 되었다.

### [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 방법 선택 가이드

| 상황 | 권장 방법 |
|:---|:---|
| 빠른 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)) 구축 | [랜덤 포레스트](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/) |
| 최고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) ([정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/)) | XGBoost / LightGBM |
| 해석 중요 (규제 산업) | [랜덤 포레스트](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/) + [SHAP](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/327_shap/) |
| [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/) [행렬 분해](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/161_matrix_decomposition/) | SVD / ALS |
| 불균형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | XGBoost + scale_pos_weight |
| 대용량 고속 처리 | LightGBM (Leaf-wise 성장) |

기술사 시험에서 [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/)은 <strong>"<a href="/knowledge-base/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/">배깅</a>(<a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 감소) vs <a href="/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/127_boosting/">부스팅</a>(편향 감소) + <a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/110_bias_variance_tradeoff/">편향-분산 트레이드오프</a>"</strong> 를 핵심 축으로, SVD는 <strong>"잠재 요인 분해와 추천·<a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a> 활용"</strong> 을 중심으로 서술해야 한다.

📢 **섹션 요약 비유**: [랜덤 포레스트](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/)는 "다양한 배경의 배심원 100명이 독립적으로 평결"하고, XGBoost는 "실수를 계속 피드백 받아 점점 나아지는 학습자"이다. 둘 다 혼자보다 훨씬 좋은 판단을 내린다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 핵심 기술 | SVD ([특이값 분해](/knowledge-base/studynote/10_ai/05_data_science_ml/342_svd/)) | 행렬 잠재 구조 추출 |
| [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) | [Bagging](/knowledge-base/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/) ([배깅](/knowledge-base/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/)) | [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)·독립 학습, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 감소 |
| [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) | [Boosting](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/127_boosting/) ([부스팅](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/127_boosting/)) | 순차·오류 집중 학습, 편향 감소 |
| 모델 | [Random Forest](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/) ([랜덤 포레스트](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/)) | [배깅](/knowledge-base/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/) + 특성 무작위 선택 |
| 모델 | XGBoost | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 그레이디언트 [부스팅](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/127_boosting/) |
| 진단 | [Bias-Variance Tradeoff](/knowledge-base/studynote/14_data_engineering/02_math_mining/110_bias_variance_tradeoff/) | 과소적합-과적합 균형 |
| 해석 | [SHAP](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/327_shap/) | 특성별 예측 기여도 |
| 특성 | [Feature Importance](/knowledge-base/studynote/10_ai/05_data_science_ml/355_random_forest_feature_importance/) (특성 중요도) | 모델 입력 영향력 순위 |
| 연관 | LightGBM | Leaf-wise 고속 [부스팅](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/127_boosting/) |
| 연관 | ALS (교대 최소제곱법) | SVD 추천 학습 방법 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. SVD는 "영화를 몇 가지 숨은 성격(잠재 요인)으로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하는 것"인데, 액션이나 로맨스 같은 공식 장르가 아니라 AI가 스스로 발견한 "비슷한 영화들의 공통 느낌"이다.

### 📈 관련 키워드 및 발전 흐름도

```text
단일 의사결정 트리 (과적합 위험)
    │
    ▼
앙상블 학습
    ├─► Bagging: Random Forest (병렬 · 분산↓)
    └─► Boosting: AdaBoost → GBM → XGBoost → LightGBM → CatBoost
    │
    ▼
행렬 분해: SVD → 추천 시스템 · 차원 축소
    │
    ▼
딥러닝 앙상블 · AutoML 자동 모델 선택
```
2. [랜덤 포레스트](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/)는 "100명의 전문가가 각자 다른 자료를 보고 투표"하는 방식이고, XGBoost는 "한 전문가가 틀린 부분만 집중 보완하며 100번 반복 학습"하는 방식이다.
3. [편향-분산 트레이드오프](/knowledge-base/studynote/14_data_engineering/02_math_mining/110_bias_variance_tradeoff/)는 "너무 단순한 규칙은 항상 틀리고(편향), 너무 복잡한 규칙은 외운 것만 맞고 새 문제엔 틀리는([분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)) 딜레마"로, [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/)은 이 둘의 균형을 잡는 방법이다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 230 / 258

← **이전**: [229. 시계열 ARIMA (AutoRegressive Integrated Moving Average) 정상성 협업 필터링](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/229_time_series_arima_stationarity_collaborative_filtering/)
**다음**: [231. SMOTE (Synthetic Minority Over-sampling Technique) 불균형 데이터 증강](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/231_smote_oversampling_class_imbalance_augmentation/) →

---
