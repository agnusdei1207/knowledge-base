+++
title = "228. PCA (Principal Component Analysis) LDA t-SNE 차원 축소"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)([Dimensionality Reduction](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_dimensionality_reduction/))는 고차원 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 핵심 정보는 유지하면서 불필요한 차원을 제거하여, 차원의 저주([Curse of Dimensionality](/knowledge-base/studynote/12_it_management/02_itsm_itil/080_curse_of_dimensionality/))를 극복하고 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)·모델 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 개선하는 기법이다.
> 2. **가치**: [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/)([Principal Component Analysis](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/), [주성분 분석](/knowledge-base/studynote/06_ict_convergence/05_data_science/338_pca_principal_component_analysis/))는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 최대화 비지도 축소, LDA(Linear Discriminant Analysis, [선형 판별 분석](/knowledge-base/studynote/14_data_engineering/02_math_mining/082_lda_linear_discriminant_analysis_classification/))는 클래스 분리 극대화 지도 축소, t-SNE(t-Distributed Stochastic Neighbor [Embedding](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/))는 고차원 이웃 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 보존하는 비선형 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)를 각각 제공한다.
> 3. **판단 포인트**: PCA는 전처리·[압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 목적, LDA는 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 전처리, t-SNE/UMAP은 탐색적 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 목적으로 선택해야 하며, t-SNE는 새 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환(out-of-sample)이 불가능하다는 제약이 있다.

---

## Ⅰ. 개요 및 필요성

### 차원의 저주 ([Curse of Dimensionality](/knowledge-base/studynote/12_it_management/02_itsm_itil/080_curse_of_dimensionality/))

차원이 증가할수록 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포인트 간 거리가 모두 비슷해지고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 희소해져 모델 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 역설적으로 저하된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">차원 수 │ 단위 정육면체에서 전체 부피의 1% 커버하는 변 길이</div>
<div class="kb-diagram-note">2 │ 0.10 (10%)</div>
<div class="kb-diagram-note">10 │ 0.63 (63%)</div>
<div class="kb-diagram-note">100 │ 0.955 (95.5%)</div>
<div class="kb-diagram-note">1000 │ 0.995 (99.5%)</div>
</div>
</div>



→ 고차원에서는 "근접 이웃"의 의미가 약해지고, [KNN](/knowledge-base/studynote/10_ai/03_llm_nlp/262_knn/)·클러스터링·회귀 모두 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하

📢 **섹션 요약 비유**: 차원의 저주는 "도서관 책이 2D 평면에서 3D 공간, 그 다음 4D, 5D... 로 흩어질수록 찾고 싶은 책이 너무 멀어지는 것"이다. [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)는 "다시 2D 선반으로 책을 정렬"하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) ([Principal Component Analysis](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/), [주성분 분석](/knowledge-base/studynote/06_ict_convergence/05_data_science/338_pca_principal_component_analysis/))

PCA는 비지도(Unsupervised) 선형 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)다. 원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)([Variance](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/))이 가장 크게 보존되는 방향(주성분, [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/))으로 새 축을 정의한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">PCA 알고리즘 흐름:</div>
<div class="kb-diagram-note">① 데이터 중심화 (평균 빼기, Mean Centering)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">② 공분산 행렬 계산 (Covariance Matrix)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">③ 고유값 분해 (Eigenvalue Decomposition) 또는 SVD</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">④ 고유벡터(Eigenvector) = 주성분 방향 축</div>
<div class="kb-diagram-note">고유값(Eigenvalue) = 해당 축의 설명 분산량</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">⑤ 설명 분산 누적 비율 확인 (Explained Variance Ratio)</div>
<div class="kb-diagram-note">보통 PC들이 95% 이상 설명하는 수까지 선택</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">⑥ 원본 데이터를 선택된 PC 공간으로 투영</div>
<div class="kb-diagram-note">Scree Plot (스크리 플롯):</div>
<div class="kb-diagram-note">설명 분산</div>
<div class="kb-diagram-note">80%│ ●</div>
<div class="kb-diagram-note">●</div>
<div class="kb-diagram-note">40%│ ●</div>
<div class="kb-diagram-note">●──●──●──●</div>
<div class="kb-diagram-note">PC1 PC2 PC3 PC4 (엘보우 이후 완만 → 거기서 자름)</div>
</div>
</div>



### 2-2. LDA (Linear Discriminant Analysis, [선형 판별 분석](/knowledge-base/studynote/14_data_engineering/02_math_mining/082_lda_linear_discriminant_analysis_classification/))

LDA는 지도(Supervised) 선형 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)다. 클래스 간 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)(Between-Class [Variance](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/))을 최대화하고 클래스 내 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)(Within-Class [Variance](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/))을 최소화하는 축을 찾는다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">LDA 목표:</div>
<div class="kb-diagram-note">클래스 간 분산 (SB)</div>
<div class="kb-diagram-note">최대화:</div>
<div class="kb-diagram-note">클래스 내 분산 (SW)</div>
<div class="kb-diagram-note">PCA와의 차이:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PCA: 레이블 무관, 전체 분산 최대화 (비지도)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">LDA: 레이블 사용, 클래스 분리 최대화 (지도)</div></div>
<div class="kb-diagram-note">최대 축 수: min(클래스 수 - 1, 특성 수)</div>
<div class="kb-diagram-note">→ 클래스가 3개이면 최대 2개의 판별 축 가능</div>
</div>
</div>



### 2-3. t-SNE (t-Distributed Stochastic Neighbor [Embedding](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/))

t-SNE는 비선형 비지도 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 전용 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)다. 고차원에서의 이웃 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 분포를 저차원(2D/3D)에서 재현한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">t-SNE 핵심 아이디어:</div>
<div class="kb-diagram-note">① 고차원: 데이터 포인트 간 유사도를 가우시안 확률로 계산</div>
<div class="kb-diagram-note">② 저차원: 유사도를 t-분포(꼬리 두터운 분포)로 표현</div>
<div class="kb-diagram-note">③ KL Divergence를 최소화하여 고·저차원 확률 분포 정렬</div>
<div class="kb-diagram-note">t-분포를 쓰는 이유:</div>
<div class="kb-diagram-note">고차원→저차원 시 "군집 간 거리가 찌그러지는 문제(Crowding Problem)"를</div>
<div class="kb-diagram-note">t-분포의 긴 꼬리(Heavy Tail)가 완화한다.</div>
</div>
</div>



### 2-4. 방법별 종합 비교

| 구분 | [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) | LDA | t-SNE | UMAP |
|:---|:---|:---|:---|:---|
| 유형 | 비지도·선형 | 지도·선형 | 비지도·비선형 | 비지도·비선형 |
| 목적 | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 최대화 | 클래스 분리 | 군집 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) | 구조 보존 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) |
| 출력 차원 | 자유 | 클래스수-1 | 2D/3D 주로 | 자유 |
| 신규 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 변환 가능 | 변환 가능 | 불가 | 가능 () |
| 계산 복잡도 | O(min(n,d)³) | O(nd²) | O(n²) | O(n log n) |
| 해석 가능성 | 중간 | 높음 | 낮음 | 낮음 |

📢 **섹션 요약 비유**: PCA는 "그림자로 3D 물체를 가장 잘 표현하는 조명 각도 찾기", LDA는 "두 그룹이 가장 잘 구분되는 조명 각도 찾기", t-SNE는 "가까운 것끼리 뭉치도록 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 손으로 배치하는 것"이다.

---

## Ⅲ. 비교 및 연결

### 3-1. 언제 어떤 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)를 쓰는가?



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">목적별 선택 기준</div>
<div class="kb-diagram-note">고차원 전처리 → 모델 성능 개선 : PCA</div>
<div class="kb-diagram-note">(선형 관계 가정, 빠른 변환 필요)</div>
<div class="kb-diagram-note">분류 전 특성 변환 : LDA</div>
<div class="kb-diagram-note">(클래스 레이블 있고 선형 분리 가정)</div>
<div class="kb-diagram-note">데이터 탐색·시각화 : t-SNE 또는 UMAP</div>
<div class="kb-diagram-note">(군집 구조 발견, 이상점 탐지)</div>
<div class="kb-diagram-note">대용량 데이터 + 빠른 속도 : UMAP</div>
<div class="kb-diagram-note">(t-SNE보다 10~100× 빠름, 전역 구조 보존)</div>
</div>
</div>



### 3-2. PCA와 SVD의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)

PCA는 내부적으로 [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/)([Singular Value Decomposition](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/), [특이값 분해](/knowledge-base/studynote/10_ai/05_data_science_ml/342_svd/))를 이용한다.

```
데이터 행렬 X = U × Σ × Vᵀ

U: 왼쪽 특이벡터 (데이터 포인트의 좌표)
Σ: 특이값 (분산 크기에 비례)
Vᵀ: 오른쪽 특이벡터 = PCA의 주성분 축

PCA 주성분 = V의 열벡터
분산 = (특이값)² / (n-1)
```

### 3-3. t-SNE 하이퍼파라미터 실무

| 파라미터 | 설명 | 권장값 |
|:---|:---|:---|
| perplexity | 이웃 수 영향 (작으면 국소, 크면 전역) | 5~50 |
| learning_rate | 최적화 스텝 크기 | 100~1000 |
| n_iter | 최적화 반복 수 | ≥ 1000 |
| random_state | 재현성 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 고정값 |

📢 **섹션 요약 비유**: PCA와 SVD의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 "산을 보는 방법"이다. PCA는 "가장 산이 잘 보이는 각도 탐색", SVD는 그 각도를 수학적으로 분해하는 "도구"다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. 이미지 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 시나리오 ([PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) 적용)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">입력</div><div class="kb-diagram-note">100×100 픽셀 얼굴 이미지 = 10,000 차원</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">PCA 적용</div></div>
<div class="kb-diagram-note">① 10,000 차원 → PCA → 상위 50개 주성분 선택</div>
<div class="kb-diagram-note">② 설명 분산: PC1~PC50 = 95.2% 설명</div>
<div class="kb-diagram-note">③ 압축 비율: 10,000 → 50 = 200배 압축</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">활용</div></div>
<div class="kb-diagram-tree-item" style="--depth:0">Eigenface (고유얼굴): 얼굴 인식의 고전 방법</div>
<div class="kb-diagram-tree-item" style="--depth:0">차원 축소 후 SVM·로지스틱 회귀 성능 향상</div>
</div>
</div>



### 4-2. 고객 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) (t-SNE 적용)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">입력</div><div class="kb-diagram-note">고객 행동 특성 50개 차원 (클릭·구매·방문 패턴)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">t-SNE 적용</div></div>
<div class="kb-diagram-note">50차원 → t-SNE → 2차원 시각화</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">결과</div></div>
<div class="kb-diagram-note">2D 산점도에서 5개 군집 발견:</div>
<div class="kb-diagram-note">● 충성 고객 군집</div>
<div class="kb-diagram-note">● 가격 민감 군집</div>
<div class="kb-diagram-note">● 휴면 고객 군집</div>
<div class="kb-diagram-note">● 신규 고객 군집</div>
<div class="kb-diagram-note">● 고가치 VIP 군집</div>
<div class="kb-diagram-note">→ 각 군집에 맞는 맞춤형 마케팅 전략 수립</div>
</div>
</div>



📢 **섹션 요약 비유**: t-SNE로 고객을 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)하는 것은 "수백 가지 특성의 고객들을 2D 지도에 비슷한 고객끼리 가깝게 배치하는 것"이다. 지도를 보면 어느 고객 동네가 어디 있는지 한눈에 파악된다.

---

## Ⅴ. 기대효과 및 결론

[차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)는 현대 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석 파이프라인에서 **전처리·탐색·모델링** 세 단계 모두에 필수적인 도구다.

### 선택 가이드 요약

| 상황 | 권장 방법 |
|:---|:---|
| 빠른 선형 전처리 | [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) |
| [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 전처리 (레이블 있음) | LDA |
| 소규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 군집 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) | t-SNE |
| 대규모 [데이터 시각화](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/283_data_visualization_dashboard_report/)·전처리 | UMAP |
| 비지도 탐색 + 새 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환 | UMAP |

기술사 시험에서 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)는 <strong>"<a href="/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/">PCA</a>(<a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 최대화)·LDA(클래스 분리)·t-SNE(이웃 보존)의 목적 차이 + 차원의 저주 해결 맥락"</strong> 을 중심으로 서술해야 한다.

📢 **섹션 요약 비유**: [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)는 "수백 개 특성으로 정의된 사람을 핵심 키워드 3개로 요약하는 것"이다. 정보 손실은 있지만, 핵심은 유지하고 훨씬 다루기 쉬워진다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 핵심 기법 | [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) ([주성분 분석](/knowledge-base/studynote/06_ict_convergence/05_data_science/338_pca_principal_component_analysis/)) | 비지도·선형·[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 최대화 |
| 핵심 기법 | LDA ([선형 판별 분석](/knowledge-base/studynote/14_data_engineering/02_math_mining/082_lda_linear_discriminant_analysis_classification/)) | 지도·선형·클래스 분리 |
| 핵심 기법 | t-SNE | 비선형·[시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 전용 |
| 비교 | UMAP | 빠른 비선형 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) |
| 수학 기반 | [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) ([특이값 분해](/knowledge-base/studynote/10_ai/05_data_science_ml/342_svd/)) | [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) 내부 계산 기반 |
| 문제 | [Curse of Dimensionality](/knowledge-base/studynote/12_it_management/02_itsm_itil/080_curse_of_dimensionality/) (차원의 저주) | 고차원 희소성 문제 |
| 파라미터 | Explained [Variance](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) Ratio | [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 선택 기준 |
| 파라미터 | Perplexity (퍼플렉서티) | t-SNE 이웃 영향 범위 |
| 응용 | Eigenface | [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) 기반 얼굴 인식 |
| 전처리 연계 | [Feature Engineering](/knowledge-base/studynote/12_it_management/02_itsm_itil/081_feature_engineering/) (특성 공학) | 축소 전 특성 변환 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. 수백 가지 정보로 설명된 그림을 딱 2~3가지 핵심 특징으로 요약하는 것이 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)이고, PCA는 "가장 많은 정보를 유지하는 방향으로 그림자를 만드는 것"이다.

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">고차원 데이터 (차원의 저주)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">차원 축소</div>
<div class="kb-diagram-tree-item" style="--depth:0">PCA: 분산 최대화 선형 투영 (비지도)</div>
<div class="kb-diagram-tree-item" style="--depth:0">LDA: 클래스 분리 최대화 투영 (지도)</div>
<div class="kb-diagram-tree-item" style="--depth:0">t-SNE / UMAP: 비선형 시각화 (2D/3D)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">응용: 시각화 · 노이즈 제거 · 피처 압축</div>
</div>
</div>


2. LDA는 "고양이와 개를 가장 잘 구분하는 방향으로 그림자를 만드는 것"으로, 처음부터 어떤 동물인지 알고 시작한다.
3. t-SNE는 "비슷한 친구끼리 가깝게, 다른 친구끼리 멀게 자리를 배치하는 것"인데, 2D 지도로 만들어주기 때문에 눈으로 군집을 바로 볼 수 있다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 228 / 258

← **이전**: [227. 로지스틱 회귀 (Logistic Regression) CLT p-value 1/2종 오류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/)
**다음**: [229. 시계열 ARIMA (AutoRegressive Integrated Moving Average) 정상성 협업 필터링](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/229_time_series_arima_stationarity_collaborative_filtering/) →

---
