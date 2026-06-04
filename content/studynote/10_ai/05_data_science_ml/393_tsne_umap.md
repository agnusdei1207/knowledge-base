---
title: "393. t-SNE / UMAP (TSNE UMAP)"
date: "2026-05-09"
tags:
  - "studynote-ai"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: t-SNE (t-distributed Stochastic Neighbor [Embedding](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/))와 UMAP (Uniform Manifold Approximation and Projection)은 고차원 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 매니폴드 (Manifold) 구조를 보존하면서 2~3차원으로 비선형 [차원 축소](/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)하는 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/) 기법이다.
> 2. **가치**: 클러스터링 구조, [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/), 클래스 분리도를 직관적으로 탐색할 수 있어 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 벡터 분석·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이해·모델 디버깅에 필수적인 탐색적 도구다.
> 3. **판단 포인트**: t-SNE는 지역 구조 보존에 강하고 전역 구조 왜곡 가능, UMAP은 전역 구조를 더 잘 보존하고 20~[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)0배 빠르며 새 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 변환 적용 가능한 프로젝션 학습이 가능하다.

---

## Ⅰ. 개요 및 필요성

고차원 공간 (수백~수천 차원)은 인간이 직접 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)할 수 없다. 차원의 저주 ([Curse of Dimensionality](/studynote/12_it_management/02_itsm_itil/864_curse_of_dimensionality/))로 인해 고차원에서 거리 개념도 무의미해진다. [차원 축소](/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 본질 구조를 유지하며 저차원으로 표현하는 것이다.

[PCA](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) ([Principal Component Analysis](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/))는 선형 변환만 수행하므로 비선형 구조(매니폴드)를 잃어버린다. t-SNE와 UMAP은 비선형 매니폴드를 보존한다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 지구 표면(3D 구면)을 세계 지도(2D 평면)로 펼칠 때 어딘가는 왜곡이 생긴다. t-SNE/UMAP은 이 왜곡을 최소화하며 지도를 만드는 방법이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### t-SNE (van der Maaten & Hinton, 2008)

```
1단계 - 고차원 유사도 (가우시안 커널):
   pⱼ|ᵢ = exp(-||xᵢ-xⱼ||^ / 2σᵢ^) / Σk≠i exp(-||xᵢ-xₖ||^ / 2σᵢ^)
   pᵢⱼ = (pⱼ|ᵢ + pᵢ|ⱼ) / 2n   (대칭화)

2단계 - 저차원 유사도 (t분포, 꼬리 두꺼움):
   qᵢⱼ = (1 + ||yᵢ-yⱼ||^)⁻¹ / Σk≠l (1 + ||yₖ-yₗ||^)⁻¹

3단계 - KL 다이버전스 최소화:
   L = KL(P||Q) = Σᵢⱼ pᵢⱼ log(pᵢⱼ / qᵢⱼ)
```

**t분포의 역할**: 저차원에서 멀리 있는 점들 간에 더 작은 인력 -> 클러스터 분리 강화

### UMAP (McInnes et al., 2018)

```
1단계 - 퍼지 토폴로지 그래프 구성:
   각 데이터 포인트의 k-NN 그래프 -> 가중치 w(uᵢ,uⱼ)

2단계 - 저차원 임베딩 최적화:
   w_low(yᵢ,yⱼ) = (1 + a·||yᵢ-yⱼ||^(2b))⁻¹

   교차 엔트로피:
   L = Σw·log(w/w_low) + (1-w)·log((1-w)/(1-w_low))
```

```
+------------------------------------------------------+
|  고차원 임베딩 (BERT, ResNet 등)                      |
|  [●●●] [○○○] [^^^]  (3 클래스, 768차원)             |
|       v t-SNE / UMAP                                 |
|  저차원 시각화 (2D)                                   |
|                                                      |
|  ●●●●                                                |
|      ○○○                                             |
|          ^^^                                         |
|  (클러스터 구조 시각화 성공)                           |
+------------------------------------------------------+
```

| 특성 | t-SNE | UMAP |
|:---|:---|:---|
| 속도 | 느림 O(n^) | 빠름 O(n log n) |
| 전역 구조 보존 | 약함 | 강함 |
| 지역 구조 보존 | 매우 강함 | 강함 |
| 새 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환 | 불가 (재실행) | 가능 (변환 학습) |
| 하이퍼파라미터 | perplexity | n_neighbors, min_dist |

- **📢 섹션 요약 비유**: t-SNE는 "이웃 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)만 집착하는 지도 제작자", UMAP은 "이웃과 전체 지형 모두를 균형 있게 보는 지도 제작자"다.

---

## Ⅲ. 비교 및 연결

| 방법 | 선형? | 보존 | 속도 | 역변환 |
|:---|:---|:---|:---|:---|
| [PCA](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) | 선형 | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 최대 | 매우 빠름 | 가능 |
| t-SNE | 비선형 | 지역 구조 | 느림 | 불가 |
| UMAP | 비선형 | 지역+전역 | 빠름 | 제한적 |
| [Autoencoder](/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/) | 비선형 | 학습 의존 | 중간 | 가능 |

**perplexity (t-SNE 핵심 파라미터)**: 각 점의 유효 이웃 수 (5~50). 너무 낮으면 분리된 점들, 너무 높으면 구조 소실.

- **📢 섹션 요약 비유**: perplexity는 "지도를 만들 때 얼마나 넓은 범위를 이웃으로 볼 것인가"의 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)이다. 너무 좁으면 지역 정보만, 너무 넓으면 전체가 뭉개진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/">임베딩</a> 품질 <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong>: [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/), [Word2Vec](/studynote/10_ai/04_ai_ops_ethics/339_word2vec/), [ResNet](/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/) 특성의 클러스터 구조 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)
<strong><a href="/studynote/10_ai/05_data_science_ml/397_outlier_mahalanobis/">이상치 탐지</a></strong>: 군집에서 벗어난 점 -> 레이블 오류 또는 진짜 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)
**클래스 분리도**: 클러스터 간 거리로 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 가능성 예측
**UMAP 권장 상황**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)만 건 이상, 전역 구조 분석, 빠른 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)

기술사 포인트: t-SNE와 UMAP의 [손실 함수](/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) 차이(KL vs 교차 [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/))와 t분포의 역할(클러스터 분리 강화) 설명.

- **📢 섹션 요약 비유**: [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)는 "모델이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 어떻게 이해하는지 MRI로 촬영하는 것"이다. 클러스터가 명확하면 모델이 잘 분리 학습했다는 증거다.

---

## Ⅴ. 기대효과 및 결론

t-SNE와 UMAP은 고차원 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 탐색의 필수 도구로, 딥러닝 모델의 표현 학습 품질을 직관적으로 평가할 수 있게 한다. UMAP은 t-SNE의 속도·전역 구조 보존 한계를 개선해 대규모 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 분석의 표준이 됐다.

- **📢 섹션 요약 비유**: t-SNE/UMAP은 AI의 "X-ray"다. 모델 내부 표현을 사람이 볼 수 있는 형태로 투영해 문제를 진단한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| t-SNE | [KL 다이버전스](/studynote/08_algorithm_stats/09_info_theory/153_kl_divergence/), t분포 / 지역 구조 보존 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/) |
| UMAP | 퍼지 토폴로지, 교차 [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/) / 전역+지역 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/) |
| 매니폴드 | 고차원 내 저차원 구조 / 비선형 [차원 축소](/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) 기반 |
| perplexity | t-SNE 파라미터 / 유효 이웃 수 |
| [PCA](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) | 선형 [차원 축소](/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) / t-SNE/UMAP의 선행 |
| 클러스터 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/) | [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) / 모델 표현 품질 분석 |

### 📈 관련 키워드 및 발전 흐름도

```text
[입력 표현·특징 추출] -> [t-SNE / UMAP (TSNE UMAP)] -> [경량화·멀티모달·서비스 적용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. t-SNE/UMAP은 3D 지구본을 2D 세계 지도로 펴는 것처럼, 수백 차원의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 2D로 펼쳐서 눈으로 볼 수 있게 해.
2. t-SNE는 가까운 이웃만 잘 표현하는 지도를 만들고, UMAP은 가까운 것과 먼 것 모두 잘 표현하는 더 균형 잡힌 지도를 만들어.
3. AI가 고양이와 개를 잘 구분하는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하려면 t-SNE로 그림을 그려봐. 고양이들이 한 덩어리, 개들이 한 덩어리로 모이면 AI가 잘 학습한 거야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 393 / 420

<- **이전**: [392. 퍼셉트론 수렴 정리 (Perceptron Convergence Theorem)](/studynote/10_ai/05_data_science_ml/392_perceptron_convergence/)
**다음**: [394. AutoML / Hyperopt (Automl Hyperopt TPE)](/studynote/10_ai/05_data_science_ml/394_automl_hyperopt_tpe/) ->

---
