+++
weight = 121
title = "121. 지도 학습 (Supervised Learning) - 라벨 기반 학습·분류·회귀"
date = "2026-04-19"
[extra]
categories = "studynote-dataengineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 지도 학습은 **입력(X)과 정답 라벨(y)의 쌍**으로 구성된 학습 [[001_dikw_pyramid|데이터]]를 통해 모델이 **X→y 매핑 함수를 학습**하는 ML 패러다임이며, [[104_classification_analysis|분류]]([[107_classification|Classification]])와 회귀(Regression)로 나뉜다.
> 2. **가치**: 정답 라벨이 주어지므로 **명확한 평가 기준(정확도·[[076_mse_mean_squared_error_regression|MSE]])**이 있어 모델 성능을 객관적으로 측정할 수 있으며, 가장 성숙하고 실무에서 널리 사용되는 ML 방식이다.
> 3. **판단 포인트**: 지도 학습의 핵심 과제는 **라벨링 비용(인건비·시간)**이며, 이를 줄이기 위한 Semi-supervised [[240_switch_learning_forwarding_flooding|Learning]]·[[266_self_supervised_learning|Self-supervised Learning]]·[[483_active_vs_passive_ftp|Active]] Learning이 대안으로 발전했다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    지도 학습 분류 vs 회귀                              │
├───────────────────────────────────────────────────────┤
│  [분류 (Classification)]                              │
│   입력: 이메일 텍스트 → 출력: 스팸/정상 (이산값)      │
│   모델: 로지스틱 회귀, SVM, Random Forest, DNN       │
│                                                       │
│  [회귀 (Regression)]                                  │
│   입력: 면적·위치 → 출력: 집값 3.2억 (연속값)        │
│   모델: 선형 회귀, Ridge, Random Forest, DNN          │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[104_classification_analysis|분류]]는 "이 동물이 고양이인가 개인가?" (카테고리)이고, 회귀는 "이 집의 가격은 얼마인가?" (숫자)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 학습 패러다임 비교

| 패러다임 | 라벨 | 목표 | 대표 |
|:---|:---|:---|:---|
| **지도** | **있음** | 예측 | [[104_classification_analysis|분류]]·회귀 |
| **비지도** | 없음 | 구조 발견 | 클러스터링·[[163_pca|PCA]] |
| **강화** | 보상 | 행동 최적화 | 게임·로봇 |
| **자기 지도** | 자동 [[087_process_state_transition|생성]] | 표현 학습 | **[[301_bert_mlm|BERT]]·[[302_gpt_autoregressive|GPT]]** |

- **📢 섹션 요약 비유**: 지도 학습은 선생님(라벨)이 정답을 알려주는 수업, 비지도는 혼자 규칙을 찾는 탐구, 강화는 게임에서 점수를 올리며 배우는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[104_classification_analysis|분류]] | 회귀 |
|:---|:---|:---|
| **출력** | 이산 (카테고리) | **연속 (숫자)** |
| **손실** | [[154_cross_entropy|Cross-Entropy]] | **[[076_mse_mean_squared_error_regression|MSE]]** |
| **평가** | Accuracy, F1 | **R², RMSE** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 라벨링 비용 절감 [[268_strategy_pattern|전략]]
1. **[[214_active_learning|Active Learning]]**: 불확실한 샘플만 라벨링 요청.
2. **Semi-supervised**: 소량 라벨 + 대량 비라벨 활용.
3. **Self-supervised**: [[001_dikw_pyramid|데이터]] 자체에서 라벨 자동 [[087_process_state_transition|생성]] ([[301_bert_mlm|BERT]] 마스킹).

---

## Ⅴ. 기대효과 및 결론

지도 학습은 ML의 **가장 기본이자 실무 적용이 가장 광범위한 패러다임**이며, [[266_self_supervised_learning|Self-supervised Learning]]([[301_bert_mlm|BERT]]·[[302_gpt_autoregressive|GPT]])이 라벨링 비용 문제를 혁신적으로 해결하면서 새로운 지평을 열고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[104_classification_analysis|분류]]** | 이산값 예측 (스팸 탐지·이미지 [[104_classification_analysis|분류]]) |
| **회귀** | 연속값 예측 (가격·매출 예측) |
| **라벨링 비용** | 지도 학습의 핵심 과제 |
| **Self-supervised** | 라벨 없이 학습 ([[301_bert_mlm|BERT]]·[[302_gpt_autoregressive|GPT]]) |
| **[[110_bias_variance_tradeoff|편향-분산 트레이드오프]]** | 지도 학습 모델 선택의 기준 |

### 📈 관련 키워드 및 발전 흐름도

```text
[선형 회귀 / 로지스틱 회귀 (통계학)]
    │
    ▼
[SVM / Decision Tree (1990s)]
    │
    ▼
[Random Forest / XGBoost (2000~2010s)]
    │
    ▼
[DNN / CNN / RNN (Deep Learning, 2012~)]
    │
    ▼
[현재: Self-supervised → Fine-tuning (BERT·GPT)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 지도 학습은 **선생님(라벨)**이 "이건 고양이, 이건 개"라고 알려주는 수업이에요.
2. 많이 배우면 처음 보는 동물 사진도 **"이건 고양이야!"**라고 맞출 수 있어요.
3. 문제는 선생님이 **일일이 정답을 알려줘야 해서** 시간과 비용이 많이 든다는 거예요!
