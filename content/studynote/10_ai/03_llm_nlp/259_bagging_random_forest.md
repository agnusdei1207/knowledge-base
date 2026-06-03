---
title: 259. 배깅 (Bagging)
date: '2026-05-09'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 배깅(Bagging, Bootstrap Aggregating)은 복원 추출(Bootstrap [[056_표본화_Sampling|Sampling]])로 다양한 훈련 서브셋을 만들고, 독립적으로 학습한 모델들을 [[430_index_fast_full_scan|병렬]]로 집계하여 [[136_variance|분산]]([[136_variance|Variance]])을 줄이는 [[257_ensemble_learning|앙상블]] 기법이다.
> 2. **가치**: [[353_random_forest|랜덤 포레스트]]([[353_random_forest|Random Forest]])는 배깅에 특성 무작위 선택(Random Feature [[022_mcts_four_stages|Selection]])을 추가하여 상관관계를 더욱 낮춰 가장 강력한 배깅 구현체가 되었다.
> 3. **판단 포인트**: OOB(Out-Of-Bag) 오차를 활용하면 별도 [[395_verification_process_review|검증]] 세트 없이도 모델 [[282_performance_tactics|성능]]을 추정할 수 있는 것이 배깅만의 장점이다.

---

## Ⅰ. 개요 및 필요성

단일 결정 트리([[124_decision_tree|Decision Tree]])는 **고분산(High [[136_variance|Variance]])** 모델이다. 훈련 [[001_dikw_pyramid|데이터]]가 조금만 달라져도 완전히 다른 트리가 만들어질 수 있다. 이 불안정성을 극복하기 위해 [[595_leo_low_earth_orbit_starlink_6g|Leo]] Breiman([[098_md5|1996]])이 배깅을 제안했다.

**배깅의 핵심 아이디어**:
> "같은 모집단에서 독립 표본을 N개 뽑아 평균을 내면 [[136_variance|분산]]이 1/N로 감소한다"

- 현실에서는 모집단이 하나뿐이므로, **복원 추출(Bootstrap)**로 N개의 가상 [[001_dikw_pyramid|데이터]]셋을 만든다.
- 각 [[001_dikw_pyramid|데이터]]셋으로 독립적으로 모델을 훈련 → 결과를 평균/다수결로 집계

| 특성 | 단일 결정 트리 | 배깅 [[257_ensemble_learning|앙상블]] |
|:---|:---|:---|
| [[136_variance|분산]] | 높음 (불안정) | 낮음 (안정적) |
| 편향 | 낮음 | 낮음 (유지) |
| 해석 가능성 | 높음 | 낮음 |
| 계산 비용 | 낮음 | 높음 ([[430_index_fast_full_scan|병렬]] 가능) |
| 과적합 [[003_resistance|저항]] | 낮음 | 높음 |

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 배깅은 "여론조사를 여러 번 해서 평균을 내는 것"이다. 한 번의 조사(단일 트리)는 오차가 크지만, 수백 번의 독립 조사(배깅)를 평균 내면 훨씬 안정적인 결과가 나온다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 배깅 전체 흐름

```
  원본 훈련 데이터 (n개 샘플)
         │
         │  복원 추출 (Bootstrap Sampling)
  ┌──────┼──────────────────────────────┐
  │      │    각 부트스트랩 샘플: n개   │
  │      │    (약 63.2% 고유 샘플 포함) │
  │  ┌───▼───┐ ┌───────┐ ┌───────┐     │
  │  │ D_1   │ │  D_2  │ │  D_B  │ ··· │
  │  └───┬───┘ └───┬───┘ └───┬───┘     │
  │      │         │         │         │
  │  ┌───▼───┐ ┌───▼───┐ ┌───▼───┐     │
  │  │ h_1   │ │  h_2  │ │  h_B  │ ··· │
  │  │ (Tree)│ │ (Tree)│ │ (Tree)│     │
  │  └───┬───┘ └───┬───┘ └───┬───┘     │
  │      └─────────┴─────────┘         │
  │               집계                  │
  │   분류: 다수결 / 회귀: 평균         │
  └─────────────────────────────────────┘
              최종 예측
```

### 부트스트랩 샘플링의 특성

n개 샘플에서 복원 추출로 n개를 뽑으면:
- 특정 샘플이 선택될 [[130_probability|확률]]: 1 - (1-1/n)^n → n→∞ 시 **1 - 1/e ≈ 63.2%**
- 나머지 **36.8%는 OOB(Out-Of-Bag) 샘플**로 [[395_verification_process_review|검증]]에 사용 가능

### [[353_random_forest|랜덤 포레스트]] ([[353_random_forest|Random Forest]])

[[353_random_forest|랜덤 포레스트]]는 배깅에 **특성 무작위 선택(Random Feature Subspace)**을 추가한다.

```
  각 트리의 노드 분할 시:
  ┌────────────────────────────────────────┐
  │ 전체 특성 수: p개                      │
  │ 무작위 선택 특성 수:                   │
  │   분류: √p  (예: 100개 중 10개)        │
  │   회귀: p/3 (예: 100개 중 33개)        │
  │                                        │
  │ → 트리 간 상관관계 ↓                   │
  │ → 다양성 ↑                             │
  │ → 앙상블 효과 극대화                   │
  └────────────────────────────────────────┘
```

| 하이퍼파라미터 | 설명 | 기본값 |
|:---|:---|:---|
| n_estimators | 트리 수 | 100 |
| max_features | 노드당 고려 특성 수 | 'sqrt' ([[104_classification_analysis|분류]]), 'auto' |
| max_depth | 트리 최대 깊이 | None (무제한) |
| min_samples_split | 분할 최소 샘플 수 | 2 |
| oob_score | OOB 오차 계산 여부 | False |

### OOB 오차 추정

각 샘플은 전체 B개 트리 중 약 36.8%(1/e)의 트리에서 OOB 샘플로 남는다. 이 트리들의 예측을 집계하여 **[[250_cross_validation_kfold|교차 검증]] 없이 일반화 [[282_performance_tactics|성능]]을 추정**할 수 있다.

- **📢 섹션 요약 비유**: [[353_random_forest|랜덤 포레스트]]의 특성 무작위 선택은 "각 직원이 회사 전체 정보가 아닌 자기 분야 정보만 보고 판단"하는 것이다. 덕분에 모든 직원이 같은 결론을 내리는(과적합) 것을 방지한다.

---

## Ⅲ. 비교 및 연결

### Bagging vs [[353_random_forest|Random Forest]]

| 특성 | 순수 Bagging | [[353_random_forest|Random Forest]] |
|:---|:---|:---|
| 특성 선택 | 모든 특성 사용 | 무작위 서브셋 |
| 트리 상관관계 | 상대적으로 높음 | 낮음 |
| [[136_variance|분산]] 감소 효과 | 중간 | 더 높음 |
| 특성 중요도 | 미제공 | 제공 ([[355_random_forest_feature_importance|Feature Importance]]) |

### 특성 중요도 ([[355_random_forest_feature_importance|Feature Importance]])

Random Forest는 각 특성이 불순도(Gini, [[151_entropy|Entropy]]) 감소에 기여한 평균 양을 특성 중요도로 제공한다. 이는 특성 선택(Feature [[022_mcts_four_stages|Selection]])에 활용된다.

```
  특성 중요도 예시 (신용 평가):
  ┌──────────────────────────┐
  │ 월 소득     ████████ 0.32│
  │ 신용 기간   ██████   0.24│
  │ 부채 비율   █████    0.20│
  │ 직업 유형   ████     0.16│
  │ 나이        ██       0.08│
  └──────────────────────────┘
```

- **📢 섹션 요약 비유**: Bagging은 "같은 교과서로 공부했지만 서로 다른 부분을 집중한 학생들"이고, Random Forest는 거기에 "각 학생이 랜덤으로 고른 과목만 시험 보는" 규칙을 추가한 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[353_random_forest|Random Forest]] 튜닝 [[268_strategy_pattern|전략]]

1. **n_estimators**: 많을수록 좋지만 계산 비용 증가. 보통 100~500으로 시작
2. **max_features**: 'sqrt'가 기본이지만 특성이 많으면 'log2'도 고려
3. **max_depth**: None으로 두면 과적합 위험, [[001_dikw_pyramid|데이터]] 크기에 따라 조정
4. **class_weight**: 불균형 [[001_dikw_pyramid|데이터]]에서 'balanced' [[009_config|설정]]

### [[430_index_fast_full_scan|병렬]] 처리 이점

배깅은 각 트리가 독립적이므로 `n_jobs=-1`로 모든 CPU 코어를 활용한 [[430_index_fast_full_scan|병렬]] 훈련이 가능하다. XGBoost([[127_boosting|부스팅]])보다 훈련 속도가 빠른 주요 이유다.

### 기술사 답안 포인트

- **"배깅이 [[136_variance|분산]]을 줄이는 이유"**: 독립 예측기들의 평균 → [[136_variance|분산]]이 1/n로 감소 (단, 예측기들이 독립일 때)
- **"OOB 오차의 활용"**: 별도 [[395_verification_process_review|검증]] 세트 불필요 → 소규모 [[001_dikw_pyramid|데이터]]에서 유리
- **"[[353_random_forest|Random Forest]] vs 단일 결정 트리"**: 비선형성·상호작용 포착은 유사하나 RF가 훨씬 안정적
- **"[[353_random_forest|Random Forest]] 한계"**: 해석 불가, 메모리 과다, 연속적 외삽(Extrapolation) 불가

- **📢 섹션 요약 비유**: Random Forest는 "각자 다른 문제지를 받아서 시험 본 학생들의 평균 점수"다. 모두 같은 시험지를 받으면(단순 배깅) 서로 비슷한 실수를 하지만, 다른 문제지(랜덤 특성)는 각자 독립적인 오류를 범해 평균이 더 정확해진다.

---

## Ⅴ. 기대효과 및 결론

배깅 및 [[353_random_forest|랜덤 포레스트]]를 적용하면:

1. **안정성**: 단일 결정 트리 대비 [[136_variance|분산]] 대폭 감소 → [[001_dikw_pyramid|데이터]] 변화에 강건
2. **특성 중요도**: 모델 해석 및 특성 선택에 활용 가능한 정보 제공
3. **OOB [[395_verification_process_review|검증]]**: [[250_cross_validation_kfold|교차 검증]] 대비 적은 계산 비용으로 일반화 [[282_performance_tactics|성능]] 추정
4. **결측값 처리**: 일부 구현체에서 결측값을 직접 처리 가능

Random Forest는 **전처리 부담이 적고, 특성 중요도를 제공하며, 과적합에 강한** 특성 덕분에 실무에서 첫 번째로 시도하는 기준 모델([[025_baseline|Baseline]])로 자주 선택된다.

- **📢 섹션 요약 비유**: Random Forest는 "편식 없이 무엇이든 잘 소화하는 만능 선수"다. 특별히 뛰어난 점은 없지만 약점도 없어서 어떤 [[001_dikw_pyramid|데이터]]에도 안정적인 [[282_performance_tactics|성능]]을 발휘한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 배깅 (Bagging) | Bootstrap Aggregating, 복원 추출 / [[136_variance|분산]] 감소 [[257_ensemble_learning|앙상블]] |
| 복원 추출 (Bootstrap [[056_표본화_Sampling|Sampling]]) | 63.2%, OOB / 배깅의 핵심 메커니즘 |
| OOB 오차 (Out-Of-Bag Error) | [[395_verification_process_review|검증]] 추정, 36.8% / 별도 [[395_verification_process_review|검증]] 세트 대체 |
| [[353_random_forest|랜덤 포레스트]] ([[353_random_forest|Random Forest]]) | Random Feature Subspace, Gini / 배깅의 강화 [[288_version_ihl_tos_total_length|버전]] |
| 특성 무작위 선택 (Random Feature) | √p, p/3 / 트리 간 상관관계 감소 |
| 특성 중요도 ([[355_random_forest_feature_importance|Feature Importance]]) | Gini 감소, 평균 불순도 / 해석 가능성 지원 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] → [배깅 (Bagging)] → [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 배깅은 같은 반 학생들한테 여러 번 다른 시험 문제를 줘서 각자 공부시키고, 나중에 다수결로 답을 정하는 거야.
2. [[353_random_forest|랜덤 포레스트]]는 거기에 "각 학생이 교과서의 랜덤한 부분만 공부할 수 있어"라는 규칙을 추가한 것!
3. 덕분에 모든 학생이 같은 내용만 공부해서 같은 실수를 하는 것(과적합)을 막을 수 있어.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 259 / 420

← **이전**: [[258_voting_ensemble|258. 보팅 (Voting)]]
**다음**: [[260_boosting_xgboost|260. 부스팅 (Boosting)]] →

---
