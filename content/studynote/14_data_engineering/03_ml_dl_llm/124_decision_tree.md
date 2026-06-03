---
title: 124. 의사결정 트리 (Decision Tree) - 해석 가능한 분류·회귀 알고리즘
date: '2026-04-19'
tags:
- studynote-dataengineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 의사결정 트리는 **[[247_feature_label_variables|피처]] 값에 따라 데이터를 반복적으로 분할(Split)**하여 트리 구조의 규칙을 학습하는 **해석 가능한(Interpretable)** [[104_classification_analysis|분류]]·회귀 [[001_algorithm_definition|알고리즘]]이다.
> 2. **가치**: "나이 ≥ 30 → 소득 ≥ 5000만원 → 대출 승인"처럼 **규칙이 인간이 읽을 수 있는 형태**로 표현되어, 블랙박스 모델과 달리 **의사결정 근거를 설명**할 수 있다.
> 3. **판단 포인트**: 깊은 트리는 과적합([[245_overfitting_variance|Overfitting]]) 위험이 크므로 **[[435_pruning_hardware|가지치기]]([[435_pruning_hardware|Pruning]])·최대 깊이 제한**이 필요하며, [[257_ensemble_learning|앙상블]]([[353_random_forest|Random Forest]]·XGBoost)로 단일 트리의 약점을 극복한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    의사결정 트리 예시 (대출 승인)                      │
├───────────────────────────────────────────────────────┤
│            [나이 ≥ 30?]                               │
│           /          \                                │
│         Yes          No                               │
│    [소득 ≥ 5000?]     [학력 = 대졸?]                  │
│     /      \          /       \                       │
│   Yes      No       Yes      No                      │
│  승인 ✅  거절 ❌   승인 ✅  거절 ❌                  │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 의사결정 트리는 **20 질문 게임**이다. "나이가 30 이상?" "소득이 5000만원 이상?" 등 질문을 반복하여 답에 도달한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 분할 기준

| 기준 | [[001_algorithm_definition|알고리즘]] | 설명 |
|:---|:---|:---|
| **[[108_gini_impurity|지니 불순도]]** | CART | 불순도 최소화 |
| **[[151_entropy|엔트로피]]** | ID3/C4.5 | 정보 이득 최대화 |
| **[[136_variance|분산]] 감소** | 회귀 트리 | [[136_variance|분산]] 최소화 |

- **📢 섹션 요약 비유**: 분할은 "이 질문으로 가장 깔끔하게 그룹이 나뉘는가?"를 측정하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 단일 트리 | [[353_random_forest|Random Forest]] | XGBoost |
|:---|:---|:---|:---|
| **과적합** | 높음 | **낮음** | 낮음 |
| **해석** | **가능** | 어려움 | 어려움 |
| **[[282_performance_tactics|성능]]** | 보통 | 높음 | **최고** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 과적합 방지
1. **[[435_pruning_hardware|가지치기]] ([[435_pruning_hardware|Pruning]])**: Pre-[[435_pruning_hardware|pruning]](조기 중단), Post-[[435_pruning_hardware|pruning]].
2. **max_depth 제한**: 트리 깊이 제한.
3. **[[257_ensemble_learning|앙상블]]**: 여러 트리를 결합 (RF, XGBoost).

---

## Ⅴ. 기대효과 및 결론

의사결정 트리는 **가장 해석 가능한 ML [[001_algorithm_definition|알고리즘]]**이며, [[353_random_forest|Random Forest]]·XGBoost·LightGBM의 기본 학습기(Base Learner)로서 현대 ML의 근간이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[108_gini_impurity|지니 불순도]]** | CART의 분할 기준 |
| **[[151_entropy|엔트로피]]** | ID3/C4.5의 분할 기준 |
| **[[435_pruning_hardware|가지치기]]** | 과적합 방지 |
| **[[353_random_forest|Random Forest]]** | [[259_bagging_random_forest|배깅]] + 의사결정 트리 |
| **XGBoost** | [[127_boosting|부스팅]] + 의사결정 트리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[ID3 (Quinlan, 1986) — 엔트로피 기반]
    │
    ▼
[C4.5 (1993) — ID3 개선, 연속 변수 처리]
    │
    ▼
[CART (Breiman, 1984→2001) — 지니, 회귀 트리]
    │
    ▼
[Random Forest (2001) — 배깅 앙상블]
    │
    ▼
[현재: XGBoost / LightGBM — 부스팅 앙상블]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 의사결정 트리는 **20 질문 게임**이에요. "나이가 30 이상?" "키가 크?" 질문으로 답을 찾아요.
2. 질문을 **너무 많이 하면(과적합)** 오히려 헷갈리니까 **적당히** 해야 해요.
3. 여러 게임을 동시에 하고 **다수결([[353_random_forest|Random Forest]])**로 결정하면 더 정확해요!
