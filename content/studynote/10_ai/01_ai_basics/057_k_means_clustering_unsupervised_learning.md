+++
title = "57. K-Means 군집화 (K-Means Clustering) - 중심점 반복 이동으로 군집 찾기"
date = 2026-04-07

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: K-Means는 정답 라벨이 없는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 K개의 중심점으로 나누고, 각 점을 가장 가까운 중심에 반복 할당하는 [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.
> 2. **가치**: 고객 세분화, 이미지 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/), 패턴 탐색처럼 "비슷한 것끼리 묶기"가 필요한 곳에서 직관적이고 빠르게 쓸 수 있다.
> 3. **판단 포인트**: [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 중심점, 거리 척도, [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/), 군집 수 K의 선택이 결과를 크게 좌우한다.

---

## Ⅰ. 개요 및 필요성

K-Means는 정답이 없는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 스스로 묶는 도구다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 라벨이 없을 때 "어떤 것끼리 비슷한가"를 먼저 보고 싶을 때 쓴다.

고객 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/), 문서 묶기, 이미지 색상 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)처럼 비슷한 것끼리 모으는 문제에 자주 쓰인다.

- **📢 섹션 요약 비유**: 색종이 [더미](/knowledge-base/studynote/04_software_engineering/11_testing_validation/459_dummy_test_double/)를 비슷한 색끼리 자동으로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하는 기계다.

---

## Ⅱ. [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 반복 흐름

K-Means는 크게 두 단계를 반복한다.

1. 각 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 가장 가까운 중심점에 할당한다.
2. 각 군집의 평균 위치로 중심점을 다시 옮긴다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">초기 중심점 선택</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">가까운 중심점에 할당</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">군집 평균으로 중심점 이동</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">변화가 거의 없을 때까지 반복</div>
</div>
</div>



이 반복이 멈추면 각 중심점 주변으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 안정적으로 모인다.

- **📢 섹션 요약 비유**: 아이들이 가장 가까운 반장에게 줄을 서고, 반장은 다시 줄의 가운데로 가는 일을 반복하는 것과 같다.

---

## Ⅲ. 거리와 스케일의 영향

K-Means는 거리를 기준으로 군집을 나눈다. 그래서 변수의 크기가 다르면 결과가 왜곡된다.

특히 [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)([outlier](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/))가 있으면 중심점이 끌려갈 수 있다. 따라서 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)와 스케일 조정이 중요하다.

- **📢 섹션 요약 비유**: 키와 몸무게가 섞인 줄세우기에서는 단위가 큰 쪽이 지나치게 영향력을 가진다.

---

## Ⅳ. [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)값과 변형 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)

[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 중심점을 어디에 두느냐가 결과를 좌우한다. 너무 나쁘게 시작하면 엉뚱한 군집이 나온다.

이를 보완하는 대표 방법은 다음과 같다.

- **K-Means++**: [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 중심점을 멀찍이 흩어 놓는다.
- **K-Medoids**: 평균 대신 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 점을 중심으로 쓴다.
- **Mini-Batch K-Means**: 큰 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 일부 샘플만 보고 빠르게 갱신한다.

군집 품질은 Elbow 방법이나 Silhouette 점수로 비교할 수 있다.

- **📢 섹션 요약 비유**: 씨앗을 아무 데나 뿌리지 말고, 처음부터 골고루 놓아야 밭이 예쁘게 나뉜다.

---

## Ⅴ. 실무 활용과 한계

K-Means는 단순하고 빠르지만, 모든 상황에 맞지는 않는다.

실무 활용 예시는 다음과 같다.

- 고객 세분화
- 이미지 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)
- [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)의 전처리
- 문서나 제품의 비슷한 묶음 찾기

한계도 분명하다. 군집이 구형이 아닐 때, [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)가 많을 때, K 값을 잘못 잡을 때 결과가 흔들린다.

- **📢 섹션 요약 비유**: 네모난 상자에 둥근 공만 잘 들어가듯, 모양이 안 맞으면 억지로 끼워 맞추기 어렵다.

---

## 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">데이터 입력</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">초기 중심점</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">할당 / 평균 이동 반복</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">K개 군집 완성</div>
</div>
</div>



---

## 관련 키워드 및 발전 흐름도

1. [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/) → 라벨 없는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 탐색
2. 반복 할당과 재계산 → 중심점 수렴
3. K-Means++ → [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)값 안정화
4. K-Medoids / Mini-Batch → 변형과 확장
5. 군집 평가 지표 → Elbow, Silhouette로 품질 점검

---

## 어린이를 위한 3줄 비유 설명

K-Means는 친구들을 비슷한 무리끼리 자동으로 모아 주는 거예요.  
중심점이 먼저 잡히고, 친구들이 가까운 곳으로 계속 이동해요.  
그러다 보면 비슷한 사람끼리 한 그룹이 돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 57 / 420

← **이전**: [56. K-NN (K-Nearest Neighbors) - 새로운 데이터를 가장 가까운 K개 이웃의 클래스 중 다수결로 판별 (게으른](/knowledge-base/studynote/10_ai/01_ai_basics/056_knn_k_nearest_neighbors_lazy_learning/)
**다음**: [58. SVM (Support Vector Machine) - 마진(Margin)을 최대화하는 초평면(Hyperplane) 분할 모델](/knowledge-base/studynote/10_ai/01_ai_basics/058_svm_support_vector_machine_margin_hyperplane/) →

---
