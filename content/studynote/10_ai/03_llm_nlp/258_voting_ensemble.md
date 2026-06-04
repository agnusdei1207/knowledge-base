---
title: "258. 보팅 (Voting)"
date: "2026-05-09"
tags:
  - "studynote-ai"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 보팅(Voting)은 서로 다른 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)(이종 모델, [Heterogeneous](/studynote/05_database/05_distributed_nosql_newsql/273_heterogeneous_db/) Models)들의 예측을 집계하는 가장 단순한 [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 방법이다.
> 2. **가치**: 하드 보팅(Hard Voting)은 다수결로 클래스를 결정하고, 소프트 보팅(Soft Voting)은 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 평균을 사용하여 더 정교한 결과를 낸다.
> 3. **판단 포인트**: 보팅의 효과는 각 모델이 서로 독립적인 오류를 범할 때 극대화되며, 상관된 모델들의 조합은 개선 효과가 제한적이다.

---

## Ⅰ. 개요 및 필요성

보팅(Voting)은 <strong>여러 이종 모델(<a href="/studynote/05_database/05_distributed_nosql_newsql/273_heterogeneous_db/">Heterogeneous</a> Models)</strong>의 예측 결과를 합쳐 최종 결정을 내리는 [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 기법이다. Bagging이나 Boosting과 달리, 보팅은 <strong>같은 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>로 학습된 서로 다른 <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>들을 결합한다.

**보팅이 필요한 이유**:
- SVM은 경계면 근처 샘플에 강함
- Random Forest는 비선형 패턴에 강함
- Logistic Regression은 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 보정이 잘 됨
- 이 세 모델의 약점이 서로 다르므로, 결합하면 전반적 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 향상된다.

| 구분 | Hard Voting | Soft Voting |
|:---|:---|:---|
| 집계 방법 | 다수결 (최빈 클래스) | [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 평균 -> argmax |
| 필요 정보 | 클래스 레이블 | 클래스 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) |
| [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) | 낮음 | 높음 |
| 사용 조건 | [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 출력 불가 모델 포함 시 | 모든 모델이 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 출력 가능 시 |

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 보팅은 배심원 재판과 같다. 12명의 배심원이 각자 다른 직업과 관점을 가지고 유/무죄를 결정하는 것처럼, 다양한 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 "각자의 관점"으로 클래스를 판정한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 하드 보팅 vs 소프트 보팅 구조

```
  입력 데이터 X
       |
  +----+----------------------------------+
  |         이종 모델 학습 (병렬)          |
  +----------+----------+-----------------+
  |  SVM     |    RF    |  Logistic Reg.  |
  | Class: A | Class: B |    Class: A     |
  |  -----   |  -----   |   ---------     |
  | Pr(A)=.9 | Pr(A)=.3 |  Pr(A)=0.7     |
  +-----+----+-----+----+--------+--------+
        |          |             |
  +-----v----------v-------------v--------+
  |           집계 방법                    |
  +----------------+----------------------+
  |  Hard Voting   |    Soft Voting       |
  |  A:2, B:1      |  Pr(A)=(0.9+0.3+0.7)|
  |  -> 다수결: A   |       /3 = 0.633     |
  |                |  -> argmax: A         |
  +----------------+----------------------+
             최종 예측: Class A
```

### 소프트 보팅의 수식

$$\hat{y} = \text{argmax}_k \sum_{j=1}^{M} w_j \cdot p_{jk}$$

- $M$: 모델 수
- $w_j$: j번째 모델의 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) (기본값 1, 가중 보팅 시 조정)
- $p_{jk}$: j번째 모델이 클래스 k로 예측한 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)

### 보팅 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)기 예시 (이진 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/))

| 모델 | P(양성) | 하드 보팅 | 소프트 보팅 |
|:---|:---:|:---:|:---:|
| [SVM](/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) | 0.85 | Positive | - |
| [Random Forest](/studynote/06_ict_convergence/05_data_science/353_random_forest/) | 0.40 | Negative | - |
| [Logistic Regression](/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/) | 0.72 | Positive | - |
| **집계 결과** | **(0.85+0.40+0.72)/3=0.657** | **Positive (2:1)** | **Positive (>0.5)** |

- **📢 섹션 요약 비유**: 하드 보팅은 "손들어서 투표"고, 소프트 보팅은 "각자 얼마나 확신하는지 점수를 매겨서 합산"하는 방식이다. 확신의 정도가 다를 때는 소프트 보팅이 더 현명하다.

---

## Ⅲ. 비교 및 연결

### 보팅 vs [Bagging](/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/) vs [Boosting](/studynote/14_data_engineering/03_ml_dl_llm/127_boosting/)

| 특성 | Voting | [Bagging](/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/) | [Boosting](/studynote/14_data_engineering/03_ml_dl_llm/127_boosting/) |
|:---|:---|:---|:---|
| 모델 종류 | 이종 (다른 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) | 동종 (같은 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) | 동종 (같은 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 샘플링 | 동일 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | Bootstrap 샘플링 | [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 기반 재샘플링 |
| 학습 방식 | 독립 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) | 독립 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) | 순차 [직렬](/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) |
| 다양성 원천 | [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 차이 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 차이 | 오차 집중 |
| 구현 복잡도 | 낮음 | 중간 | 높음 |

### 독립성 가정과 실제

보팅 효과의 수학적 근거: 각 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)기의 오류율이 ε < 0.5이고 독립적이라면, n개 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)기의 다수결 오류율은:

$$P(\text{다수결 오류}) = \sum_{k=\lceil n/2 \rceil}^{n} \binom{n}{k} \epsilon^k (1-\epsilon)^{n-k}$$

n=5, ε=0.3 -> 다수결 오류율 ≈ 0.163 (단일 모델 0.3보다 낮음)

그러나 현실에서 모델들은 **완전 독립적이지 않으므로**, 다양성 확보가 핵심이다.

- **📢 섹션 요약 비유**: 보팅의 효과는 배심원들이 서로 의논하지 않고 독립적으로 판단할 때 가장 크다. 한 배심원의 의견이 다른 배심원에게 영향을 주면(상관관계), 집단 지성의 이점이 사라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 보팅 [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 설계 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

**좋은 보팅 조합 예시**:
- [SVM](/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) + [Random Forest](/studynote/06_ict_convergence/05_data_science/353_random_forest/) + [Gradient Boosting](/studynote/10_ai/01_ai_basics/034_gradient_boosting/) + [Logistic Regression](/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/)
- 각 모델이 서로 다른 특성(선형/비선형/트리 기반)을 활용하므로 다양성 확보

**나쁜 보팅 조합 예시**:
- [Decision Tree](/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/) + [Decision Tree](/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/) + [Decision Tree](/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/) (모두 동일 -> Bagging이 낫다)

### 가중 보팅(Weighted Voting)

[검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 세트 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에 비례하여 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 부여하면 단순 보팅보다 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 향상된다.

```
  모델별 가중치 결정:
  +----------------+------------+--------------+
  | 모델           | 검증 정확도 | 소프트 보팅 가중치|
  +----------------+------------+--------------+
  | SVM            | 0.88       | 0.35         |
  | Random Forest  | 0.85       | 0.34         |
  | Logistic Reg.  | 0.77       | 0.31         |
  +----------------+------------+--------------+
```

### 기술사 답안 포인트

- **Hard vs Soft 선택 기준**: 모든 기본 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)기가 `predict_proba`를 지원하면 Soft Voting 권장
- **모델 선택 원칙**: 단독 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 무작위(50%)보다 좋고, 서로 낮은 상관관계
- **sklearn 구현**: `VotingClassifier(estimators=[...], voting='soft')`

- **📢 섹션 요약 비유**: 보팅 [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 설계는 팀 구성과 같다. 각자 강점이 다른 멤버들을 모아야 팀 시너지가 발생한다. 모두 같은 특기를 가진 팀(동종 모델 조합)은 Bagging으로 따로 처리하는 게 낫다.

---

## Ⅴ. 기대효과 및 결론

보팅 [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/)을 적용하면:

1. <strong>빠른 <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 개선</strong>: 기존 훈련된 모델을 재사용하여 추가 학습 없이 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상
2. **모델 다양성 활용**: 각 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 강점을 상호 보완
3. **안정성 증대**: 특정 모델의 실패가 전체 예측에 미치는 영향 감소
4. **구현 단순성**: [Bagging](/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/)/Boosting보다 이해하기 쉽고 구현이 간단

보팅은 <strong>이미 잘 훈련된 여러 모델이 있고, 빠르게 <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>을 끌어올려야 할 때</strong> 최적의 선택이다.

- **📢 섹션 요약 비유**: 보팅은 "이미 실력 있는 전문가들을 한 방에 모아 의견을 듣는 것"이다. 새로운 전문가를 키우는(재학습) 시간 없이 현재 가진 자원으로 최선의 결정을 내리는 실용적 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 보팅 (Voting) | Hard Voting, Soft Voting / 이종 모델 [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 방법 |
| 하드 보팅 (Hard Voting) | 다수결, 클래스 레이블 / 단순 다수결 집계 |
| 소프트 보팅 (Soft Voting) | [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 평균, argmax / 정교한 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 집계 |
| 이종 모델 ([Heterogeneous](/studynote/05_database/05_distributed_nosql_newsql/273_heterogeneous_db/)) | [SVM](/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/), RF, LR 조합 / 다양성의 원천 |
| 독립성 ([Independence](/studynote/08_algorithm_stats/08_stats/133_independence/)) | 상관관계, 오류 상쇄 / 보팅 효과의 조건 |
| 가중 보팅 (Weighted Voting) | [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 기반 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) / 단순 보팅의 개선 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] -> [보팅 (Voting)] -> [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 어떤 영화가 재밌는지 모를 때, 친구 10명에게 물어보고 가장 많이 추천한 영화를 보는 게 하드 보팅이야.
2. 소프트 보팅은 친구들이 "얼마나 강력하게 추천하는지" 점수를 매겨서 총점이 높은 영화를 선택하는 거야.
3. 친구들이 모두 같은 취향이면 소용없으니까, 서로 다른 취향의 친구들에게 물어보는 게 포인트야!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 258 / 420

<- **이전**: [257. 앙상블 (Ensemble) 학습](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/)
**다음**: [259. 배깅 (Bagging)](/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/) ->

---
