---
title: 66. 스피어만 순위 상관 계수 (Spearman Rank Correlation)
date: '2026-04-10'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스피어만 순위 상관 계수(Spearman Rank Correlation)는 값의 크기 대신 순위를 이용해 단조 [[083_relationship_in_er_model|관계]]를 측정한다.
> 2. **가치**: [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]]와 비정규 분포에 더 robust해서 Pearson보다 넓은 상황에 적용하기 쉽다.
> 3. **판단**: 선형 [[083_relationship_in_er_model|관계]]가 아니라도 순서가 맞으면 높은 상관을 보일 수 있으므로, 해석을 조심해야 한다.

---

## Ⅰ. 개요 및 필요성

[[001_dikw_pyramid|데이터]]가 정규분포처럼 깔끔하지 않아도 변수 간 [[083_relationship_in_er_model|관계]]를 보고 싶을 때가 많다. 이때 순위를 이용하면 [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 영향이 줄어든다.

스피어만 상관은 "같이 커지거나 같이 작아지는가"를 보는 데 유용하다.

- **📢 섹션 요약 비유**: 숫자 크기보다 줄서기 순서를 보는 방법이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Data
  ↓
Rank Transform
  ↓
Rank Differences
  ↓
Spearman ρ
```

| 항목 | 의미 |
| :-- | :-- |
| Rank | 값의 순서 |
| ρ (rho) | 순위 상관 계수 |
| Robustness | [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]]에 강함 |

스피어만은 값 자체 대신 순위를 비교하므로, 비선형이더라도 단조 [[083_relationship_in_er_model|관계]]라면 [[083_relationship_in_er_model|관계]]를 포착할 수 있다.

- **📢 섹션 요약 비유**: 점수가 아니라 등수만 가지고 비교하는 운동회 순위표다.

---

## Ⅲ. 비교 및 연결

| 구분 | Pearson | Spearman |
| :-- | :-- | :-- |
| [[083_relationship_in_er_model|관계]] | 선형 | 단조 |
| [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 영향 | 큼 | 작음 |
| [[001_dikw_pyramid|데이터]] 분포 | 정규성 기대 | 덜 요구 |

| 사용 상황 | 추천 |
| :-- | :-- |
| [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] 많음 | Spearman |
| 비선형 단조 [[083_relationship_in_er_model|관계]] | Spearman |
| 정확한 선형 [[083_relationship_in_er_model|관계]] | Pearson |

스피어만은 순위 기반이라 해석이 직관적이다. 하지만 값의 간격 정보가 사라진다는 점은 기억해야 한다.

- **📢 섹션 요약 비유**: 키 차이는 무시하고, 달리기 순서만 보는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. [[001_dikw_pyramid|데이터]]가 비정규/[[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]]가 많은가?
2. 단조 [[083_relationship_in_er_model|관계]]를 보는 문제인가?
3. Pearson과 함께 비교했는가?
4. 순위 변환으로 정보 손실이 허용되는가?
5. 해석 대상이 선형인지 비선형인지 분리했는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- Pearson과 Spearman을 같은 지표로 취급하는 설계
- 순위 기반 해석을 값 기반 해석처럼 하는 설계
- [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]]가 많은데 Pearson만 쓰는 설계
- 단조 [[083_relationship_in_er_model|관계]]를 놓치고 선형성만 보는 설계

기술사 관점에서는 Spearman을 "통계적 순위 비교"로 이해하고, [[001_dikw_pyramid|데이터]] 특성에 맞는 상관 지표를 고르는 것이 중요하다.

- **📢 섹션 요약 비유**: 시험 점수의 차이보다 등수의 흐름이 더 중요할 때가 있다.

---

## Ⅴ. 기대효과 및 결론

Spearman은 [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]]에 강하고 비정규 [[001_dikw_pyramid|데이터]]에도 적용하기 쉬워 탐색적 분석에서 유용하다.

결론적으로 Spearman은 순위 기반의 robust 상관 지표다.

- **📢 섹션 요약 비유**: 숫자보다 순서가 더 중요할 때 쓰는 비교법이다.

---

## 관련 개념 맵

```text
Rank
  ↓
Spearman ρ
  ↓
Monotonic Relationship
  ↓
Robust Analysis
```

---

## 관련 키워드 및 발전 흐름도

```text
Pearson
  ↓
Spearman
  ↓
Robust Statistics
  ↓
Nonparametric Analysis
```

---

## 어린이를 위한 3줄 비유 설명

누가 몇 등인지 보는 거예요.  
점수 차이보다 순서가 중요할 때 써요.  
스피어만은 그런 순위 비교예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 66 / 258

← **이전**: [[065_pearson_correlation_coefficient_multicollinearity|65. 피어슨 상관 계수 (Pearson Correlation) - 선형적 비례 관계 측정]]
**다음**: [[067_hypothesis_testing_null_alternative_p_value|67. 가설 검정 - 귀무 가설(H0) vs 대립 가설(H1)]] →

---
