---
sidebar:
  order: 53
  label: "053. XGBoost•LightGBM (XGBoost and LightGBM)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "XGBoost•LightGBM (XGBoost and LightGBM)"
date: "2026-08-17T09:25:00+09:00"
tags:
  - "notes-basic-theory"
weight: 53
extra:
  question_no: "053"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "표형 데이터 부스팅 구현 비교 중심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **GBDT(Gradient Boosted Decision Trees)**: 손실 함수의 1차 그래디언트(Gradient, $g_i$)와 2차 헤시안(Hessian, $h_i$)을 기반으로 잔차를 줄이는 약한 결정 트리를 순차 결합하는 강력한 앙상블 알고리즘.
- **XGBoost(eXtreme Gradient Boosting)**: 정규화 항($\Omega(f) = \gamma T + \frac{1}{2}\lambda \sum w_j^2$)을 목적 함수에 직접 도입하고 수평적 레벨 단위(Level-wise)로 트리를 성장시키는 고성능 부스팅 라이브러리.
- **LightGBM(Light Gradient Boosting Machine)**: 히스토그램 기반 분할, 수직적 리프 단위(Leaf-wise) 성장, GOSS 및 EFB 기법을 통해 초대규모 데이터를 초고속으로 처리하는 차세대 부스팅 프레임워크.

</details>

- 정의/개념: 테일러 2차 전개(2nd-order Taylor Expansion)를 통해 손실 함수를 근사 최적화하고 하드웨어 가속 및 정규화 기법을 적용한 **정형 데이터 표준 GBDT 앙상블 프레임워크**
- 배경/필요성: 기존 전통 GBDT의 느린 순차 학습 속도, 메모리 비효율, 과적합 취약성을 극복하고 **수백만 행의 테이블 데이터에서 고속 훈련 및 정밀 예측 달성 필수**

#### 한줄 요약

- 테일러 2차 미분과 정규화를 적용한 XGBoost와 리프 단위 고속 분할을 도입한 LightGBM

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **GOSS(Gradient-based One-Side Sampling)**: 기울기(Gradient)가 큰 샘플은 전량 유지하고, 기울기가 작은 샘플은 일정한 비율로 무작위 다운샘플링하여 계산량을 대폭 절감하는 LightGBM 핵심 기술.
- **EFB(Exclusive Feature Bundling)**: 상호 배타적인(동시에 0이 아닌 값이 거의 없는) 희소 특성들을 하나의 단일 변수로 묶어 피처 차원을 축소하는 알고리즘.

</details>

- 목적 함수 내 **L1/L2 정규화 항($\gamma T + \frac{1}{2}\lambda w^2$)을 통한 자체적 과적합 억제**
- XGBoost의 **균형 잡힌 레벨 단위(Level-wise) 성장** vs LightGBM의 **손실 최대 감소 리프 단위(Leaf-wise) 성장**
- LightGBM의 **연속형 변수 히스토그램(Histogram Binning) 양자화를 통한 메모리 및 연산 $O(N)$ 최적화**

#### 한줄 요약

- 그래디언트와 헤시안 기반 최적 분할을 수행하며, 트리 성장 방식과 샘플링 전략으로 효율화

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **GBDT 2차 테일러 목적 함수**: $\tilde{\mathcal{L}}^{(t)} \approx \sum_{i=1}^n \left[ g_i f_t(\mathbf{x}_i) + \frac{1}{2} h_i f_t^2(\mathbf{x}_i) \right] + \Omega(f_t)$ ($g_i$: 1차 미분, $h_i$: 2차 미분).

</details>

```text
[ GBDT 트리 성장 전략 비교도 ]
 
 1. XGBoost: Level-wise (균형 트리 분할)
                [ Root ]
                /      \
            [ Node ]  [ Node ]      ── 동일 깊이의 모든 노드를 균등 분할 (Depth 통제)
            /   \      /   \
          [L]   [L]  [L]   [L]
 
 2. LightGBM: Leaf-wise (최대 손실 감소 리프 우선 분할)
                [ Root ]
                /      \
            [ Node ]  [ Leaf ]
            /      \
        [ Node ]  [ Leaf ]         ── 손실 감소량(Loss Reduction)이 가장 큰 리프만 집중 분할
        /      \
      [Leaf]  [Leaf]
```

선의 의미: 레벨 단위 균등 깊이 분할과 리프 단위 비대칭 집중 분할 아키텍처 비교도.

| 구성요소 | 책임 |
|:---|:---|
| 테일러 2차 연산기 | 손실 함수의 **1차 편미분($g_i$)과 2차 편미분($h_i$)을 도출하여 분할 이득 계산** |
| 분할 탐색 엔진 | XGBoost(가중치 분위수 스케치) vs LightGBM(GOSS + EFB 히스토그램) |
| 트리 생성기 | Level-wise 또는 Leaf-wise 방식으로 **최적 잎 가중치($w^* = -\frac{\sum g}{\sum h + \lambda}$) 할당** |
| 조기 종료 평가기 | 검증셋 성능 모니터링으로 **최적 에포크(`early_stopping_rounds`) 자동 중단** |

#### 한줄 요약

- 2차 미분값으로 최적 잎 가중치를 산출하고, 레벨별 또는 리프별 분할 탐색으로 트리를 생성

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **분할 이득 공식(Split Gain)**: $\text{Gain} = \frac{1}{2} \left[ \frac{(\sum_{L} g_i)^2}{\sum_{L} h_i + \lambda} + \frac{(\sum_{R} g_i)^2}{\sum_{R} h_i + \lambda} - \frac{(\sum g_i)^2}{\sum h_i + \lambda} \right] - \gamma$.

</details>

```text
정형 훈련 데이터셋 (X, y) 인입
   │
   ▼
[ 1. 기본 예측값 f_0(x) 초기화 ]
   │
   ▼
[ 2. 부스팅 반복 루프 (t = 1 to M) ]
├─ 2-1. 모든 샘플에 대해 손실 함수의 1차(g_i) 및 2차(h_i) 미분값 계산
├─ 2-2. 히스토그램 빈 생성 및 GOSS 샘플링 / EFB 특성 번들링 (LightGBM)
├─ 2-3. 분할 이득(Gain)이 최대가 되는 최적 분할점 탐색 (Leaf-wise 또는 Level-wise)
├─ 2-4. 리프 가중치 w_j* 계산 및 신규 트리 f_t(x) 완성
└─ 2-5. 앙상블 누적: f_t(x) = f_(t-1)(x) + η · f_t(x)
   │
   ▼
[ 3. 검증셋 평가 및 얼리 스토핑(Early Stopping) 판정 ]
   │
   ▼
[ 4. 최적 앙상블 모델 확정 및 Feature Importance 산출 ]
```

**동작 원리**

1. **미분값 계산**: 현재 앙상블 예측값에 대해 목적 함수의 $g_i, h_i$ 도출
2. **최적 분할점 탐색**: 피처별 히스토그램을 순회하며 분할 이득(Gain)이 최대인 지점 선정
3. **트리 가중치 할당**: 정규화 파라미터 $\lambda$를 적용하여 각 리프 노드의 최적 스칼라 가중치 결정
4. **학습률 수축**: 과적합을 방지하기 위해 축소율 $\eta$(예: 0.05)를 곱해 누적 예측에 가산
5. **조기 중단 검증**: 검증 데이터 손실이 정체되면 즉시 훈련을 종료하여 과적합 방지

#### 한줄 요약

- 미분값 계산, 최적 분할 탐색, 가중치 할당, 학습률 수축을 거치며 검증 손실 기반 조기 종료 수행

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **GBDT 2대 프레임워크 비교**:
  - XGBoost: 레벨 단위 성장, 엄격한 Exact Greedy/Approximate 탐색, 안정적 수렴.
  - LightGBM: 리프 단위 성장, 히스토그램 기반, GOSS/EFB 적용으로 속도 10배 이상 향상.

</details>

| 비교 항목 | XGBoost (eXtreme Gradient) | LightGBM (Light Gradient) |
|:---|:---|:---|
| 트리 성장 방식 | **레벨 단위 (Level-wise, 균형 트리)** | **리프 단위 (Leaf-wise, 비대칭 트리)** |
| 연속형 분할 방식 | 정렬 기반 Exact Greedy / Quantile Sketch | **히스토그램 기반 양자화 (256 Bins)** |
| 대규모 샘플링 기법 | 서브샘플링 (Subsample) | **GOSS (Gradient-based One-Side Sampling)** |
| 희소 피처 처리 | 결측치 자동 방향 할당 (Sparsity-aware) | **EFB (Exclusive Feature Bundling)** |
| 훈련 속도 및 메모리 | 보통 속도, 중간 메모리 점유 | **초고속 (10배+ 빠름), 초저메모리** |
| 과적합 위험성 | 상대적으로 낮음 (Depth 제어 용이) | **소표본($N < 10,000$) 시 리프 과적합 주의** |

#### 한줄 요약

- 중소규모와 균형 성장은 XGBoost, 대규모 고차원 데이터와 초고속 훈련은 LightGBM을 적용

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **CatBoost(Categorical Boosting)**: 범주형 변수를 타깃 인코딩할 때 발생하는 데이터 누수를 Ordered Target Statistics로 완벽 차단하는 범주형 특화 GBDT 알고리즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| LightGBM 적용 시 소규모 데이터에서 **비대칭 리프 과적합** | `max_depth`, `num_leaves=31`, `min_child_samples=20` 제한 | 깊은 리프 과적합 원천 차단 |
| 수천만 건 대규모 정형 데이터에서의 **훈련 지연 및 메모리 고갈** | **LightGBM (GOSS + EFB + Histogram) 및 GPU 가속** | 훈련 시간 80% 단축 및 실시간 재학습 |
| 고차원 카디널리티(High-cardinality) 범주형 변수 처리 | **`categorical_feature` 지정 또는 CatBoost 전환** | 원-핫 인코딩 차원 폭증 방지 |
| 피처 간 복합 비선형 상호작용의 설명력 부재 | **TreeSHAP 알고리즘을 통한 국소/전역 기여도 산출** | 규제 준수 및 피처 중요도 XAI 확보 |

#### 한줄 요약

- **num_leaves 제약 과적합 방지·LightGBM GPU 대규모 가속·CatBoost 범주형 처리·TreeSHAP XAI**

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **정형 데이터 엔지니어링 표준**: 추천 시스템 랭킹, CTR 예측, 금융 리스크 평가 등 대부분의 테이블 데이터 예측 파이프라인에서 LightGBM은 1차 베이스라인이자 최우선 모델로 자리매김.

</details>

- 중소규모/균형 트리는 **XGBoost**, 대규모 고차원 정형 데이터는 **LightGBM**, 범주형 중심은 **CatBoost** 선택

#### 한줄 요약

- 데이터 규모와 범주형 특성에 따라 XGBoost와 LightGBM을 선택하고, TreeSHAP으로 해석력을 확보
