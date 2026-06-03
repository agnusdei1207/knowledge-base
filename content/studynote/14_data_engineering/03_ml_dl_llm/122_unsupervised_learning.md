+++
title = "122. 비지도 학습 (Unsupervised Learning) - 라벨 없는 데이터의 구조 발견"
date = 2026-04-19

[taxonomies]
tags = ["studynote-dataengineering"]

[extra]
tags = ["studynote-dataengineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 비지도 학습은 **정답 라벨 없이** [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 <strong>내재된 구조·패턴·군집을 자동 발견</strong>하는 ML 패러다임이며, 클러스터링·[차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)·[이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)·[생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 모델이 대표 기법이다.
> 2. **가치**: 실세계 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 **95% 이상은 라벨이 없으므로**, 라벨링 없이도 고객 세그먼테이션·이상 거래 탐지·[데이터 시각화](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/283_data_visualization_dashboard_report/)에 활용할 수 있다.
> 3. **판단 포인트**: K-Means(클러스터링)·[PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/)([차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/))·[Autoencoder](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/)(표현 학습)·[DBSCAN](/knowledge-base/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/)(밀도 기반 클러스터링)을 구분하고, [Self-supervised Learning](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/)([BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)·[GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/))은 비지도의 현대적 진화 형태이다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">비지도 학습 주요 유형</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">클러스터링</div><div class="kb-diagram-node">차원 축소</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">K-Means PCA</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DBSCAN t-SNE</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Gaussian Mixture UMAP</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">이상 탐지</div><div class="kb-diagram-node">생성 모델</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Isolation Forest Autoencoder</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">One-Class SVM VAE, GAN</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: 지도 학습은 선생님이 정답을 알려주는 수업이고, 비지도 학습은 <strong>학생이 스스로 규칙을 발견</strong>하는 탐구 활동이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 주요 기법 비교

| 기법 | 유형 | 대표 | 용도 |
|:---|:---|:---|:---|
| **K-Means** | 클러스터링 | K개 중심 | 고객 세그먼테이션 |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/">PCA</a></strong> | [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) | 선형 | 고차원 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/">DBSCAN</a></strong> | 밀도 클러스터링 | 밀도 | [이상치 탐지](/knowledge-base/studynote/10_ai/05_data_science_ml/397_outlier_mahalanobis/) |
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/">Autoencoder</a></strong> | 표현 학습 | 신경망 | [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 추출 |

- **📢 섹션 요약 비유**: K-Means는 비슷한 학생끼리 <strong>반 나누기</strong>이고, PCA는 성적표의 **핵심 과목만 추려서** 비교하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 지도 | 비지도 | 자기 지도 |
|:---|:---|:---|:---|
| **라벨** | 있음 | **없음** | 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| **목표** | 예측 | **구조 발견** | 표현 학습 |
| **대표** | [SVM](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/), XGBoost | K-Means, [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) | <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/">BERT</a>, <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/">GPT</a></strong> |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 활용 시나리오
1. **고객 세그먼테이션**: K-Means로 VIP·일반·이탈 위험 고객 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/).
2. **이상 거래 탐지**: [Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) Forest로 사기 거래 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/).
3. <strong><a href="/knowledge-base/studynote/07_enterprise_systems/05_data_bi/283_data_visualization_dashboard_report/">데이터 시각화</a></strong>: t-SNE/UMAP으로 고차원 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 2D로 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/).

---

## Ⅴ. 기대효과 및 결론

비지도 학습은 <strong>라벨 없는 대량 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>에서 가치를 추출</strong>하는 핵심 기법이며, Self-supervised Learning으로 진화하여 [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)·BERT의 사전 학습 기반이 되었다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **K-Means** | 중심 기반 클러스터링 |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/">PCA</a></strong> | 선형 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/">DBSCAN</a></strong> | 밀도 기반 클러스터링 |
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/">Autoencoder</a></strong> | 비지도 표현 학습 |
| **Self-supervised** | 비지도의 현대적 진화 ([BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)) |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">K-Means / PCA (통계학, 1960s~)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">DBSCAN (1996) — 밀도 기반 클러스터링</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Autoencoder / VAE (2013~) — 신경망 비지도</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">t-SNE / UMAP (시각화, 2018~)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재: Self-supervised (BERT·GPT) — 비지도의 극한 진화</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. 비지도 학습은 **정답 없이 퍼즐을 맞추는** 거예요. 비슷한 조각끼리 모아봐요.
2. K-Means는 구슬을 <strong>색깔별로 <a href="/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a></strong>하는 것이고, PCA는 구슬의 **핵심 특징만** 추려내는 거예요.
3. 정답을 모르지만 <strong>규칙을 스스로 발견</strong>할 수 있어서 정말 대단해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 122 / 258

← **이전**: [121. 지도 학습 (Supervised Learning) - 라벨 기반 학습·분류·회귀](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)
**다음**: [123. 강화 학습 (Reinforcement Learning) - 보상 기반 행동 최적화](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/123_reinforcement_learning/) →

---
