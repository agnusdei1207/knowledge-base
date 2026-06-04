---
title: "121. 지도 학습 (Supervised Learning) - 라벨 기반 학습·분류·회귀"
date: "2026-04-19"
tags:
  - "studynote-dataengineering"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 지도 학습은 <strong>입력(X)과 정답 라벨(y)의 쌍</strong>으로 구성된 학습 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 통해 모델이 <strong>X->y 매핑 함수를 학습</strong>하는 ML 패러다임이며, [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)([Classification](/studynote/12_it_management/03_ea_isp/107_classification/))와 회귀(Regression)로 나뉜다.
> 2. **가치**: 정답 라벨이 주어지므로 <strong>명확한 평가 기준(정확도·<a href="/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/">MSE</a>)</strong>이 있어 모델 성능을 객관적으로 측정할 수 있으며, 가장 성숙하고 실무에서 널리 사용되는 ML 방식이다.
> 3. **판단 포인트**: 지도 학습의 핵심 과제는 <strong>라벨링 비용(인건비·시간)</strong>이며, 이를 줄이기 위한 Semi-supervised [Learning](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/)·[Self-supervised Learning](/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/)·[Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) Learning이 대안으로 발전했다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    지도 학습 분류 vs 회귀                              |
+-------------------------------------------------------+
|  [분류 (Classification)]                              |
|   입력: 이메일 텍스트 -> 출력: 스팸/정상 (이산값)      |
|   모델: 로지스틱 회귀, SVM, Random Forest, DNN       |
|                                                       |
|  [회귀 (Regression)]                                  |
|   입력: 면적·위치 -> 출력: 집값 3.2억 (연속값)        |
|   모델: 선형 회귀, Ridge, Random Forest, DNN          |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)는 "이 동물이 고양이인가 개인가?" (카테고리)이고, 회귀는 "이 집의 가격은 얼마인가?" (숫자)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 학습 패러다임 비교

| 패러다임 | 라벨 | 목표 | 대표 |
|:---|:---|:---|:---|
| **지도** | **있음** | 예측 | [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)·회귀 |
| **비지도** | 없음 | 구조 발견 | 클러스터링·[PCA](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) |
| **강화** | 보상 | 행동 최적화 | 게임·로봇 |
| **자기 지도** | 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 표현 학습 | <strong><a href="/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/">BERT</a>·<a href="/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/">GPT</a></strong> |

- **📢 섹션 요약 비유**: 지도 학습은 선생님(라벨)이 정답을 알려주는 수업, 비지도는 혼자 규칙을 찾는 탐구, 강화는 게임에서 점수를 올리며 배우는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 회귀 |
|:---|:---|:---|
| **출력** | 이산 (카테고리) | **연속 (숫자)** |
| **손실** | [Cross-Entropy](/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/) | <strong><a href="/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/">MSE</a></strong> |
| **평가** | Accuracy, F1 | **R^, RMSE** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 라벨링 비용 절감 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)
1. <strong><a href="/studynote/10_ai/03_llm_nlp/214_active_learning/">Active Learning</a></strong>: 불확실한 샘플만 라벨링 요청.
2. **Semi-supervised**: 소량 라벨 + 대량 비라벨 활용.
3. **Self-supervised**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자체에서 라벨 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) ([BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) 마스킹).

---

## Ⅴ. 기대효과 및 결론

지도 학습은 ML의 <strong>가장 기본이자 실무 적용이 가장 광범위한 패러다임</strong>이며, [Self-supervised Learning](/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/)([BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)·[GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/))이 라벨링 비용 문제를 혁신적으로 해결하면서 새로운 지평을 열고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a></strong> | 이산값 예측 (스팸 탐지·이미지 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)) |
| **회귀** | 연속값 예측 (가격·매출 예측) |
| **라벨링 비용** | 지도 학습의 핵심 과제 |
| **Self-supervised** | 라벨 없이 학습 ([BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)·[GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)) |
| <strong><a href="/studynote/14_data_engineering/02_math_mining/110_bias_variance_tradeoff/">편향-분산 트레이드오프</a></strong> | 지도 학습 모델 선택의 기준 |

### 📈 관련 키워드 및 발전 흐름도

```text
[선형 회귀 / 로지스틱 회귀 (통계학)]
    |
    v
[SVM / Decision Tree (1990s)]
    |
    v
[Random Forest / XGBoost (2000~2010s)]
    |
    v
[DNN / CNN / RNN (Deep Learning, 2012~)]
    |
    v
[현재: Self-supervised -> Fine-tuning (BERT·GPT)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 지도 학습은 <strong>선생님(라벨)</strong>이 "이건 고양이, 이건 개"라고 알려주는 수업이에요.
2. 많이 배우면 처음 보는 동물 사진도 <strong>"이건 고양이야!"</strong>라고 맞출 수 있어요.
3. 문제는 선생님이 **일일이 정답을 알려줘야 해서** 시간과 비용이 많이 든다는 거예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 121 / 258

<- **이전**: [120. 부트스트래핑 (Bootstrapping) - 비모수 통계적 추론·신뢰 구간 추정](/studynote/14_data_engineering/02_math_mining/120_concept/)
**다음**: [122. 비지도 학습 (Unsupervised Learning) - 라벨 없는 데이터의 구조 발견](/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/) ->

---
