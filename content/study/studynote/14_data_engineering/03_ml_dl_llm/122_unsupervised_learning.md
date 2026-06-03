+++
weight = 122
title = "122. 비지도 학습 (Unsupervised Learning) - 라벨 없는 데이터의 구조 발견"
date = "2026-04-19"
[extra]
categories = "studynote-dataengineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 비지도 학습은 **정답 라벨 없이** [[001_dikw_pyramid|데이터]]의 **내재된 구조·패턴·군집을 자동 발견**하는 ML 패러다임이며, 클러스터링·[[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]]·[[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]·[[087_process_state_transition|생성]] 모델이 대표 기법이다.
> 2. **가치**: 실세계 [[001_dikw_pyramid|데이터]]의 **95% 이상은 라벨이 없으므로**, 라벨링 없이도 고객 세그먼테이션·이상 거래 탐지·[[283_data_visualization_dashboard_report|데이터 시각화]]에 활용할 수 있다.
> 3. **판단 포인트**: K-Means(클러스터링)·[[163_pca|PCA]]([[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]])·[[335_autoencoder|Autoencoder]](표현 학습)·[[351_dbscan_density_based_clustering|DBSCAN]](밀도 기반 클러스터링)을 구분하고, [[266_self_supervised_learning|Self-supervised Learning]]([[301_bert_mlm|BERT]]·[[302_gpt_autoregressive|GPT]])은 비지도의 현대적 진화 형태이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    비지도 학습 주요 유형                              │
├───────────────────────────────────────────────────────┤
│  [클러스터링]        [차원 축소]                       │
│   K-Means            PCA                              │
│   DBSCAN             t-SNE                            │
│   Gaussian Mixture   UMAP                             │
│                                                       │
│  [이상 탐지]         [생성 모델]                       │
│   Isolation Forest   Autoencoder                      │
│   One-Class SVM      VAE, GAN                         │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 지도 학습은 선생님이 정답을 알려주는 수업이고, 비지도 학습은 **학생이 스스로 규칙을 발견**하는 탐구 활동이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 주요 기법 비교

| 기법 | 유형 | 대표 | 용도 |
|:---|:---|:---|:---|
| **K-Means** | 클러스터링 | K개 중심 | 고객 세그먼테이션 |
| **[[163_pca|PCA]]** | [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]] | 선형 | 고차원 [[003_bigdata_7v|시각화]] |
| **[[351_dbscan_density_based_clustering|DBSCAN]]** | 밀도 클러스터링 | 밀도 | [[397_outlier_mahalanobis|이상치 탐지]] |
| **[[335_autoencoder|Autoencoder]]** | 표현 학습 | 신경망 | [[247_feature_label_variables|피처]] 추출 |

- **📢 섹션 요약 비유**: K-Means는 비슷한 학생끼리 **반 나누기**이고, PCA는 성적표의 **핵심 과목만 추려서** 비교하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 지도 | 비지도 | 자기 지도 |
|:---|:---|:---|:---|
| **라벨** | 있음 | **없음** | 자동 [[087_process_state_transition|생성]] |
| **목표** | 예측 | **구조 발견** | 표현 학습 |
| **대표** | [[238_svm_margin_kernel_trick_naive_bayes|SVM]], XGBoost | K-Means, [[163_pca|PCA]] | **[[301_bert_mlm|BERT]], [[302_gpt_autoregressive|GPT]]** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 활용 시나리오
1. **고객 세그먼테이션**: K-Means로 VIP·일반·이탈 위험 고객 [[104_classification_analysis|분류]].
2. **이상 거래 탐지**: [[195_isolation_concurrency_control|Isolation]] Forest로 사기 거래 [[655_ir_detection_analysis|식별]].
3. **[[283_data_visualization_dashboard_report|데이터 시각화]]**: t-SNE/UMAP으로 고차원 [[001_dikw_pyramid|데이터]]를 2D로 [[003_bigdata_7v|시각화]].

---

## Ⅴ. 기대효과 및 결론

비지도 학습은 **라벨 없는 대량 [[001_dikw_pyramid|데이터]]에서 가치를 추출**하는 핵심 기법이며, Self-supervised Learning으로 진화하여 [[302_gpt_autoregressive|GPT]]·BERT의 사전 학습 기반이 되었다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **K-Means** | 중심 기반 클러스터링 |
| **[[163_pca|PCA]]** | 선형 [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]] |
| **[[351_dbscan_density_based_clustering|DBSCAN]]** | 밀도 기반 클러스터링 |
| **[[335_autoencoder|Autoencoder]]** | 비지도 표현 학습 |
| **Self-supervised** | 비지도의 현대적 진화 ([[301_bert_mlm|BERT]]) |

### 📈 관련 키워드 및 발전 흐름도

```text
[K-Means / PCA (통계학, 1960s~)]
    │
    ▼
[DBSCAN (1996) — 밀도 기반 클러스터링]
    │
    ▼
[Autoencoder / VAE (2013~) — 신경망 비지도]
    │
    ▼
[t-SNE / UMAP (시각화, 2018~)]
    │
    ▼
[현재: Self-supervised (BERT·GPT) — 비지도의 극한 진화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 비지도 학습은 **정답 없이 퍼즐을 맞추는** 거예요. 비슷한 조각끼리 모아봐요.
2. K-Means는 구슬을 **색깔별로 [[104_classification_analysis|분류]]**하는 것이고, PCA는 구슬의 **핵심 특징만** 추려내는 거예요.
3. 정답을 모르지만 **규칙을 스스로 발견**할 수 있어서 정말 대단해요!
