+++
title = "56. K-NN (K-Nearest Neighbors) - 새로운 데이터를 가장 가까운 K개 이웃의 클래스 중 다수결로 판별 (게으른 학습, Lazy Learning)"
date = 2026-04-07

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [K-NN](/knowledge-base/studynote/06_ict_convergence/05_data_science/352_knn_distance_metrics/) ([K-Nearest Neighbors](/knowledge-base/studynote/10_ai/03_llm_nlp/262_knn/))은 규칙을 학습하는 대신 원본 사례를 저장해 두고, 새 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 오면 가장 가까운 이웃의 다수결로 답을 고르는 [lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) learning이다.
> 2. **가치**: 비선형 경계나 유사도 판단에 강하고, 빠른 baseline과 설명 가능한 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 문제에서 직관적으로 쓸 수 있다.
> 3. **판단 포인트**: 거리 척도, [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/), K 값, 탐색 구조가 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 거의 결정한다.

---

## Ⅰ. 개요 및 필요성

K-NN은 "공식을 만들지 말고 사례를 외우자"에 가까운 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. 학습 단계에서 복잡한 파라미터를 추정하지 않고, 모든 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 그대로 저장한다.

새로운 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 들어오면 주변에서 가장 가까운 K개 이웃을 찾아 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)나 회귀를 수행한다. 그래서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 형태가 복잡해도 일단 빠르게 적용해 볼 수 있다.

- **📢 섹션 요약 비유**: K-NN은 시험공부를 공식으로 하지 않고, 기출문제와 비슷한 족보를 바로 찾아 보는 똑똑한 암기법이다.

---

## Ⅱ. 거리 계산과 K 값 선택

K-NN의 핵심은 "무엇을 가깝다고 볼 것인가"이다. 보통 유클리드 거리(Euclidean distance)를 많이 쓰지만, 맨해튼 거리(Manhattan distance)나 [코사인 유사도](/knowledge-base/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)([Cosine similarity](/knowledge-base/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/))도 상황에 따라 쓰인다.

특징 스케일이 다르면 거리 계산이 왜곡된다. 그래서 키, 몸무게, 소득처럼 단위가 다른 값은 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)([normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))나 표준화(standardization)를 먼저 해야 한다.

K 값은 너무 작으면 잡음에 민감하고, 너무 크면 경계가 무뎌진다. 보통 홀수 K를 써서 동률을 줄이고, [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해 선택한다.

- **📢 섹션 요약 비유**: 가까운 친구를 몇 명 볼지 정하는 일이다. 너무 적게 보면 성급하고, 너무 많이 보면 내 판단이 흐려진다.

---

## Ⅲ. 학습 시간과 예측 비용

K-NN은 학습 시간은 거의 없지만, 예측할 때 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 비교해야 해서 비용이 커진다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 많을수록 느려지고, 차원이 높아질수록 거리의 의미도 약해진다.

이 문제가 바로 차원의 저주([curse of dimensionality](/knowledge-base/studynote/12_it_management/02_itsm_itil/080_curse_of_dimensionality/))다. 변수가 늘어나면 가까움과 멂의 차이가 희미해져, 이웃을 찾는 이점이 줄어든다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">학습 데이터 저장</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">새 샘플 입력</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">모든 점과 거리 계산</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">가장 가까운 K개 선택</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">다수결 또는 평균</div>
</div>
</div>



- **📢 섹션 요약 비유**: 책을 외우는 시간은 없지만, 시험 볼 때마다 도서관 전체를 뒤져야 해서 느려질 수 있다.

---

## Ⅳ. 실무 최적화와 검색 구조

대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서는 모든 점을 전부 비교할 수 없다. 그래서 공간을 나무처럼 나눠 빠르게 후보를 찾는 구조를 쓴다.

- **KD-Tree (k-dimensional tree)**: 차원축을 기준으로 공간을 분할한다.
- **Ball Tree**: 구 형태로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 묶어 탐색 범위를 줄인다.
- **가중 투표**: 가까운 이웃에 더 큰 비중을 준다.
- <strong><a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a>와 <a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/">차원 축소</a></strong>: 거리 왜곡을 줄이고 검색 효율을 높인다.

또한 [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/)이나 벡터 검색에서는 K-NN이 "가장 비슷한 항목 찾기"의 기본 엔진처럼 쓰인다.

- **📢 섹션 요약 비유**: 동네 전체를 직접 걸어 다니지 않고, 지도와 구역표를 써서 가까운 집만 빠르게 찾는 방법이다.

---

## Ⅴ. 언제 쓰고 언제 조심할지

K-NN은 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)와 회귀 둘 다에 쓸 수 있지만, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 매우 크거나 차원이 높은 문제에서는 조심해야 한다. 해석은 쉽지만 속도와 메모리 비용이 문제다.

다음 기준으로 판단하면 좋다.

- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 작고 직관적 유사도가 중요하면 유리하다.
- 스케일 차이가 큰 입력은 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)가 필수다.
- 잡음이 많으면 K 값을 크게 하거나 가중 투표를 고려한다.
- 실시간 예측이 많으면 KD-Tree (k-dimensional tree)나 다른 검색 최적화가 필요하다.

- **📢 섹션 요약 비유**: K-NN은 작은 동네에서는 빠르고 편하지만, 도시 전체를 매번 걸어서 찾기에는 너무 힘든 방식이다.

---

## 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">원본 데이터 저장</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">거리 계산</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">K 이웃 선택</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">다수결 / 평균</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">분류 / 회귀 출력</div>
</div>
</div>



---

## 관련 키워드 및 발전 흐름도

1. 비모수 통계와 패턴 인식 → K-NN의 기초
2. 게으른 학습([Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/)) → 학습 대신 저장 중심 방식 확립
3. 차원의 저주 → 고차원 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 인식
4. KD-Tree (k-dimensional tree)와 Ball Tree → 탐색 가속
5. 벡터 검색과 유사도 추천 → 대규모 실무 활용으로 확장

---

## 어린이를 위한 3줄 비유 설명

K-NN은 새 친구가 오면 옆에 있는 친구들만 보고 누구와 비슷한지 맞히는 게임이에요.  
가까운 친구가 많을수록 그 친구의 정체를 더 잘 짐작할 수 있어요.  
하지만 친구가 너무 많아지면 한 명씩 다 보기 힘들어져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 56 / 420

← **이전**: [55. 로지스틱 회귀와 시그모이드 이진 분류 (Logistic Regression / Sigmoid Binary Classification)](/knowledge-base/studynote/10_ai/01_ai_basics/055_logistic_regression_sigmoid_binary_classification/)
**다음**: [57. K-Means 군집화 (K-Means Clustering) - 중심점 반복 이동으로 군집 찾기](/knowledge-base/studynote/10_ai/01_ai_basics/057_k_means_clustering_unsupervised_learning/) →

---
