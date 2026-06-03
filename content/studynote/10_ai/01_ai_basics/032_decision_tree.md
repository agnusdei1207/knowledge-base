---
title: 의사결정 트리 (Decision Tree)
date: '2026-03-03'
tags:
- studynote-ai
---

> **핵심 인사이트 3줄**
> 1. [[124_decision_tree|의사결정 트리]]([[124_decision_tree|Decision Tree]])는 특성 기반 조건 분기를 통해 [[104_classification_analysis|분류]]·회귀를 수행하는 화이트박스 모델로, 결과 해석이 직관적이다.
> 2. 정보 이득(IG)·[[108_gini_impurity|지니 불순도]]·[[136_variance|분산]] 감소를 분기 기준으로 사용하며, [[435_pruning_hardware|가지치기]]([[435_pruning_hardware|Pruning]])로 과적합을 방지한다.
> 3. [[353_random_forest|랜덤 포레스트]]·XGBoost·LightGBM 등 [[257_ensemble_learning|앙상블]] 기법의 기반 학습기(Base Learner)로 사용되어 현대 ML 경진대회에서 압도적 [[282_performance_tactics|성능]]을 발휘한다.

---

## Ⅰ. [[124_decision_tree|의사결정 트리]]의 구조와 용어

[[124_decision_tree|의사결정 트리]]([[124_decision_tree|Decision Tree]])는 **트리 구조로 [[001_dikw_pyramid|데이터]]를 반복 분할해 [[104_classification_analysis|분류]]·회귀 문제를 해결**하는 지도학습 [[001_algorithm_definition|알고리즘]]이다.

```
          [나이 <= 30?]  ← 루트 노드 (Root Node)
          /          \
       예(Y)         아니오(N)
         |               |
  [학생?]       [신용 점수 > 700?]  ← 내부 노드
  /    \              /      \
 예    아니오        예        아니오
 |       |           |           |
구매  구매안함     구매       구매안함
↑         ↑
리프 노드 (Leaf Node, 최종 분류)
```

| 용어        | 설명                          |
|-----------|-------------------------------|
| 루트 노드  | 최초 분기점 (가장 중요한 특성)  |
| 내부 노드  | 중간 분기 조건                  |
| 리프 노드  | 최종 클래스/값                  |
| 깊이       | 루트에서 리프까지 레벨 수       |

📢 **섹션 요약 비유**: [[124_decision_tree|의사결정 트리]]는 스무고개와 같다 — 예/아니오 질문을 반복하면서 범위를 좁혀 정답을 찾는다.

---

## Ⅱ. 분기 기준 — 정보 이득과 [[108_gini_impurity|지니 불순도]]

### 정보 이득 (Information Gain, IG)

```
IG(S, A) = Entropy(S) - Σ (|Sv|/|S|) × Entropy(Sv)

Entropy = -Σ p_i × log₂(p_i)
```

- [[151_entropy|엔트로피]]가 낮을수록 순수(한 클래스)
- IG가 높은 특성을 분기 기준으로 선택 (ID3 [[001_algorithm_definition|알고리즘]])

### [[108_gini_impurity|지니 불순도]] ([[108_gini_impurity|Gini Impurity]])

```
Gini(S) = 1 - Σ p_i²
```

- 0 = 완전 순수, 0.5 = 최대 불순 (이진 [[104_classification_analysis|분류]])
- CART [[001_algorithm_definition|알고리즘]]에서 사용, 계산이 빠름

### 분기 기준 비교

| 기준          | [[001_algorithm_definition|알고리즘]] | 특징                    |
|-------------|----------|------------------------|
| 정보 이득     | ID3      | 다중 분기, 편향 있음     |
| 정보 이득비   | C4.5     | 가지 수 [[093_normalization|정규화]]           |
| [[108_gini_impurity|지니 불순도]]   | CART     | 이진 분기, 빠름          |
| [[136_variance|분산]] 감소     | CART(회귀) | 연속 타깃 변수에 사용   |

📢 **섹션 요약 비유**: [[108_gini_impurity|지니 불순도]]는 섞인 사탕 봉지 순도이다 — 한 종류만 있으면 0, 여러 종류가 섞여 있으면 0.5에 가까워진다.

---

## Ⅲ. 과적합과 [[435_pruning_hardware|가지치기]] ([[435_pruning_hardware|Pruning]])

```
과적합 문제:
깊은 트리 → 훈련 데이터에 완벽 적합 → 새 데이터 예측력 저하
```

### 사전 [[435_pruning_hardware|가지치기]] (Pre-[[435_pruning_hardware|Pruning]] / [[281_early_stopping|Early Stopping]])

- **최대 깊이 제한** (max_depth)
- **최소 샘플 수** (min_samples_split, min_samples_leaf)
- **최소 IG 임계값** [[009_config|설정]]

### 사후 [[435_pruning_hardware|가지치기]] (Post-[[435_pruning_hardware|Pruning]] / Reduced Error [[435_pruning_hardware|Pruning]])

1. 트리 완전히 성장 후
2. [[395_verification_process_review|검증]] 세트로 각 노드 제거 시 정확도 [[396_validation|확인]]
3. 정확도 저하 없으면 노드 제거 (서브트리 → 리프 변환)

**비용 복잡도 [[435_pruning_hardware|가지치기]] (CCP, scikit-learn)**: α 값으로 트리 크기 제어

📢 **섹션 요약 비유**: [[435_pruning_hardware|가지치기]]는 과수원 나무 정리와 같다 — 가지를 너무 많이 놔두면 열매(정확도)가 작아지고, 적절히 정리해야 좋은 열매가 열린다.

---

## Ⅳ. 코드 구현 (Python / scikit-learn)

```python
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 모델 훈련
clf = DecisionTreeClassifier(
    criterion='gini',      # 분기 기준
    max_depth=3,           # 최대 깊이 (과적합 방지)
    min_samples_leaf=5,    # 리프 최소 샘플 수
    random_state=42
)
clf.fit(X_train, y_train)

print(f"Train acc: {clf.score(X_train, y_train):.3f}")
print(f"Test  acc: {clf.score(X_test, y_test):.3f}")
print(export_text(clf, feature_names=load_iris().feature_names))
```

📢 **섹션 요약 비유**: max_depth는 스무고개 질문 수 제한이다 — 질문이 너무 많으면 특정 사람 찾기는 쉽지만, 처음 보는 사람에겐 엉뚱한 답이 나온다.

---

## Ⅴ. [[257_ensemble_learning|앙상블]]로 확장 — [[353_random_forest|랜덤 포레스트]]와 [[127_boosting|부스팅]]

```
단일 의사결정 트리
       ↓
배깅 (Bagging):
   다수의 트리 → 다수결/평균 → 랜덤 포레스트
       ↓
부스팅 (Boosting):
   순차 학습 (이전 오류 보완) → XGBoost / LightGBM / CatBoost
```

| 모델            | 기반    | 특징                         |
|---------------|---------|------------------------------|
| [[353_random_forest|Random Forest]]  | [[259_bagging_random_forest|배깅]]    | [[430_index_fast_full_scan|병렬]] 학습, 낮은 [[136_variance|분산]]          |
| XGBoost        | [[127_boosting|부스팅]]  | [[093_normalization|정규화]], 결측값 처리, 고성능   |
| LightGBM       | [[127_boosting|부스팅]]  | 리프 기반 분할, 매우 빠름     |
| CatBoost       | [[127_boosting|부스팅]]  | 범주형 특성 자동 처리         |

📢 **섹션 요약 비유**: [[353_random_forest|랜덤 포레스트]]는 다수결 투표다 — 100명의 판사(트리)가 각자 판결하고, 다수가 선택한 판결이 최종이 된다. XGBoost는 실수를 배우는 학생이다 — 틀린 문제에 집중해 계속 향상된다.

---

## 📌 관련 개념 맵

```
의사결정 트리 (Decision Tree)
├── 분기 기준
│   ├── 정보 이득 / 엔트로피 (ID3)
│   ├── 정보 이득비 (C4.5)
│   └── 지니 불순도 (CART)
├── 과적합 방지
│   ├── 사전 가지치기 (Pre-Pruning)
│   └── 사후 가지치기 (Post-Pruning)
├── 앙상블 확장
│   ├── 랜덤 포레스트 (Random Forest) — 배깅
│   ├── XGBoost — 그레이디언트 부스팅
│   └── LightGBM — 리프 기반 부스팅
└── 해석 가능성
    ├── 특성 중요도 (Feature Importance)
    └── SHAP 값 (트리 기반)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
┌─────────────────────────────────────────────────────────────────┐
│              의사결정 트리 발전 흐름                             │
├──────────────┬────────────────────┬─────────────────────────────┤
│ 1960년대     │ CLS 알고리즘       │ 트리 기반 학습 원형          │
│ 1979년       │ ID3 (Quinlan)      │ 정보 이득 기반 분기          │
│ 1986년       │ C4.5 (Quinlan)     │ 연속형·결측값 처리           │
│ 1984년       │ CART (Breiman)     │ 지니 불순도·이진 분기        │
│ 2001년       │ Random Forest      │ 배깅 앙상블로 성능 대폭 향상 │
│ 2014년       │ XGBoost            │ 부스팅 혁명, Kaggle 석권     │
│ 2017년       │ LightGBM / CatBoost│ 대용량·고속 학습             │
└──────────────┴────────────────────┴─────────────────────────────┘

핵심 키워드 연결:
DT → 지니/엔트로피 → 가지치기 → RF → XGBoost
  ↓       ↓              ↓         ↓
화이트박스 분기기준    과적합 방지  앙상블 최강자
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [[124_decision_tree|의사결정 트리]]는 스무고개다 — "나이가 30살 이하야?"처럼 예/아니오 질문으로 정답을 찾는다.
2. [[435_pruning_hardware|가지치기]]는 나무 정리다 — 가지가 너무 많으면 새 열매(새 [[001_dikw_pyramid|데이터]])가 잘 안 열리니 적당히 잘라야 한다.
3. [[353_random_forest|랜덤 포레스트]]는 다수결 선거다 — 나무 100그루가 각자 투표하고, 가장 많은 표를 받은 답이 정답이 된다.
