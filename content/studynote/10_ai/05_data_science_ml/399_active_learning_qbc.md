---
title: 399. 액티브 러닝 (Active Learning)
date: '2026-05-09'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[214_active_learning|액티브 러닝]] ([[214_active_learning|Active Learning]])은 레이블이 없는 대규모 [[001_dikw_pyramid|데이터]] 중 "가장 정보가 풍부한" 샘플을 선택적으로 레이블링하여 최소한의 어노테이션으로 최대의 [[282_performance_tactics|성능]]을 달성하는 학습 패러다임이다.
> 2. **가치**: QBC (Query By Committee, 위원회 기반 [[298_qkv_attention|쿼리]])는 여러 모델 [[257_ensemble_learning|앙상블]]의 예측 불일치가 최대인 샘플을 선택하여 가장 유익한 샘플을 효율적으로 발굴한다.
> 3. **판단 포인트**: 불확실성 샘플링 (Uncertainty [[056_표본화_Sampling|Sampling]]), QBC, 기대 모델 변화 (Expected Model Change), 코어셋 (Core-set) 등 다양한 [[298_qkv_attention|쿼리]] [[268_strategy_pattern|전략]]의 특성을 파악하고 [[001_dikw_pyramid|데이터]] 및 비용 구조에 맞게 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

의료 영상, 법률 문서, 전문 [[064_relation_domain|도메인]]에서 레이블링은 전문가 비용이 매우 높다. 전체 [[001_dikw_pyramid|데이터]]를 레이블하는 대신, AI가 "어떤 샘플에 레이블이 가장 필요한가"를 스스로 판단해 선택적으로 요청한다.

동일 [[282_performance_tactics|성능]] 달성에 필요한 레이블 수를 70~90% 감소시키는 것이 가능하다.

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[214_active_learning|액티브 러닝]]은 "시험공부할 때 내가 잘 모르는 문제만 선생님께 질문하는" 효율적 학습 [[268_strategy_pattern|전략]]이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[214_active_learning|액티브 러닝]] 사이클

```
┌──────────────────────────────────────────────────────┐
│  [초기 레이블 풀] ─► [모델 학습] ─► [쿼리 전략]      │
│                              ↑            ↓           │
│  [미레이블 풀] ◄─── 정보 풍부 샘플 선택  │           │
│       ↓                                  │           │
│  [전문가 레이블링] ──────────────────────┘           │
│  반복 → 성능 수렴                                     │
└──────────────────────────────────────────────────────┘
```

### 불확실성 샘플링 (Uncertainty [[056_표본화_Sampling|Sampling]])

```
최소 신뢰도 (Least Confident):
  x* = argmax (1 - P(ŷ|x))   (최고 확률 클래스의 확신 가장 낮은 것)

마진 샘플링 (Margin Sampling):
  x* = argmin (P(ŷ₁|x) - P(ŷ₂|x))  (상위 2개 클래스 확률 차이 최소)

엔트로피 샘플링 (Entropy Sampling):
  x* = argmax H(y|x) = argmax [-Σ P(yᵢ|x) log P(yᵢ|x)]
```

### QBC (Query By Committee)

```
위원회 C = {θ₁, θ₂, ..., θₙ}  (n개 독립 모델)

불일치 측정 (Vote Entropy):
  x* = argmax [-Σⱼ V(yⱼ|x)/|C| · log V(yⱼ|x)/|C|]

V(yⱼ|x): 위원회에서 yⱼ로 예측한 모델 수
```

**QBC 실용 구현**: [[259_bagging_random_forest|배깅]] ([[259_bagging_random_forest|Bagging]]), MC [[242_regularization_dropout_early_stopping_l1_l2_lasso_ridge|Dropout]], 딥 [[257_ensemble_learning|앙상블]]

| [[268_strategy_pattern|전략]] | 원리 | 계산 비용 | 적합 상황 |
|:---|:---|:---|:---|
| 불확실성 ([[151_entropy|엔트로피]]) | 단일 모델 예측 불확실 | 낮음 | 빠른 [[298_qkv_attention|쿼리]] |
| QBC | [[257_ensemble_learning|앙상블]] 불일치 | 중간 | 다양한 모델 |
| 기대 모델 변화 | 기울기 크기 최대화 | 높음 | 정밀한 선택 |
| Core-set | 기하학적 커버리지 | 중간 | 분포 표현성 |
| BALD | [[152_mutual_information|상호 정보량]] 최대화 | 중간 | 베이지안 모델 |

- **📢 섹션 요약 비유**: QBC는 "전문가 패널의 의견이 가장 많이 갈리는 케이스"를 먼저 판별하는 것이다. 모두가 동의하는 케이스보다 이견이 있는 케이스를 레이블링하면 더 많이 배운다.

---

## Ⅲ. 비교 및 연결

**BALD (Bayesian [[214_active_learning|Active Learning]] by Disagreement)**: 예측과 파라미터 간의 [[152_mutual_information|상호 정보량]] 최대화:
```
x* = argmax I(y; θ | x, D)
   = H[y|x,D] - E_{θ~p(θ|D)}[H[y|x,θ]]
```

**배치 [[483_active_vs_passive_ftp|액티브]] 러닝**: 매 라운드에 여러 샘플 선택 (중복성 방지를 위해 다양성 고려)

- **📢 섹션 요약 비유**: BALD는 "AI의 예측이 고정된 파라미터에 민감하게 변하는 샘플"을 선택한다. 파라미터를 조금 바꿔도 예측이 크게 달라지면 그 샘플이 중요한 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**의료 영상**: 방사선 전문의 레이블링 비용 절감 (암 진단 [[001_dikw_pyramid|데이터]])
**NLP**: 텍스트 [[104_classification_analysis|분류]] 레이블링 (법률 문서, [[105_exploratory_data_analysis|감성 분석]])
**자율주행**: 어엣지 케이스 자동 발굴 및 우선 레이블링

구현 팁:
- MC [[242_regularization_dropout_early_stopping_l1_l2_lasso_ridge|Dropout]]: 추론 시 [[242_regularization_dropout_early_stopping_l1_l2_lasso_ridge|Dropout]] 활성화 → 다수 예측 → [[136_variance|분산]] 계산
- Modular 설계: [[298_qkv_attention|쿼리]] [[268_strategy_pattern|전략]]을 플러그인으로 교체 가능하게

- **📢 섹션 요약 비유**: MC Dropout은 "같은 시험을 [[489_raid_10_hybrid|10]]번 칠 때마다 답이 달라지는 문제"를 찾는다. 그런 문제가 진짜 모르는 것이다.

---

## Ⅴ. 기대효과 및 결론

[[483_active_vs_passive_ftp|액티브]] 러닝은 레이블 희소 [[064_relation_domain|도메인]]에서 [[190_ai_llm_requirements_specification|AI]] 실용화의 핵심 기술이다. QBC와 [[151_entropy|엔트로피]] 샘플링은 간단하면서도 효과적인 [[268_strategy_pattern|전략]]으로 널리 사용된다. 레이블링 비용의 급격한 감소는 의료, 법률, 과학 연구 등 전문 [[064_relation_domain|도메인]] [[190_ai_llm_requirements_specification|AI]] 도입의 장벽을 낮춘다.

- **📢 섹션 요약 비유**: [[483_active_vs_passive_ftp|액티브]] 러닝은 "천 권의 책을 다 읽는 대신, 진짜 도움이 되는 [[489_raid_10_hybrid|10]]0권을 골라 읽는" 지혜로운 학습법이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[214_active_learning|액티브 러닝]] | [[298_qkv_attention|쿼리]] [[268_strategy_pattern|전략]], 레이블 효율 / 선택적 레이블링 학습 |
| QBC | 위원회, 불일치, [[151_entropy|엔트로피]] / [[257_ensemble_learning|앙상블]] 기반 [[298_qkv_attention|쿼리]] |
| 불확실성 샘플링 | [[151_entropy|엔트로피]], 마진 / 단일 모델 [[298_qkv_attention|쿼리]] [[268_strategy_pattern|전략]] |
| BALD | [[152_mutual_information|상호 정보량]], 베이지안 / 이론적 최적 [[298_qkv_attention|쿼리]] |
| MC [[242_regularization_dropout_early_stopping_l1_l2_lasso_ridge|Dropout]] | 베이지안 근사 / 실용적 불확실성 추정 |
| Core-set | 기하학적 커버리지 / 분포 대표성 [[298_qkv_attention|쿼리]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] → [액티브 러닝 (Active Learning)] → [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[214_active_learning|액티브 러닝]]은 "내가 모르는 문제만 선생님께 질문하는" [[268_strategy_pattern|전략]]이야. 다 아는 문제는 설명 안 들어도 되니까.
2. QBC는 여러 선생님(위원회)에게 같은 문제를 보여줬을 때 "선생님마다 답이 다른 문제"를 먼저 물어보는 방법이야.
3. [[151_entropy|엔트로피]] 샘플링은 AI가 "고양이인지 개인지 확신이 없는 사진"을 먼저 레이블 요청하는 방식이야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 399 / 420

← **이전**: [[398_gat|398. GAT (Graph Attention Network)]]
**다음**: [[400_mlops_drift_detection|400. MLOps 드리프트 탐지 (Mlops Drift Detection)]] →

---
