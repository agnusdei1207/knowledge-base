+++
title = "231. SMOTE (Synthetic Minority Over-sampling Technique) 불균형 데이터 증강"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SMOTE(Synthetic Minority Over-[sampling](/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/) Technique)는 소수 클래스 샘플 간 [k-NN](/knowledge-base/studynote/06_ict_convergence/05_data_science/352_knn_distance_metrics/)(k-Nearest Neighbor) 보간([Interpolation](/knowledge-base/studynote/14_data_engineering/04_mlops/187_time_series_interpolation_rollup_dashboard/))으로 합성 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)해 클래스 불균형(Class Imbalance)을 해소한다.
> 2. **가치**: 사기 탐지·의료 진단처럼 소수 클래스가 핵심인 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서 모델이 다수 클래스에 편향되는 문제를 근본적으로 차단하고 [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)([Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/))을 극적으로 개선한다.
> 3. **판단 포인트**: 불균형 비율·[피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 공간 특성·과적합 위험에 따라 SMOTE 변형 선택 및 언더샘플링(UnderSampling) 조합 여부를 결정하며, [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Leakage 방지를 위해 반드시 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에만 적용한다.

## Ⅰ. 개요 및 필요성

### 클래스 불균형 (Class Imbalance) 문제

실세계 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 대부분 클래스 비율이 심각하게 불균형하다.

| [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) | 다수 클래스 비율 | 소수 클래스 비율 |
|:---|:---:|:---:|
| 신용카드 사기 탐지 | 99.8% (정상 거래) | 0.2% (사기 거래) |
| 암 진단 | 95% (음성) | 5% (양성) |
| 네트워크 침입 탐지 | 99% (정상 트래픽) | 1% (공격 트래픽) |
| 제조 불량 검출 | 98% (양품) | 2% (불량품) |

이러한 불균형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 그대로 학습하면 모델이 다수 클래스만 예측해도 높은 정확도(Accuracy)를 달성한다. 사기 탐지에서 무조건 "정상"이라 예측해도 99.8% 정확도가 나오지만, 소수 클래스(사기)를 전혀 탐지하지 못해 비즈니스적으로는 완전히 무용한 모델이 된다.

### [불균형 데이터 처리](/knowledge-base/studynote/06_ict_convergence/05_data_science/356_imbalanced_data_sampling/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">불균형 데이터 처리 전략</div>
<div class="kb-diagram-tree-item" style="--depth:0">데이터 수준 (Data-Level)</div>
<div class="kb-diagram-note">── 오버샘플링 (OverSampling) ← 소수 클래스 증가</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── 무작위 오버샘플링 (Random OverSampling)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── SMOTE / ADASYN / BorderlineSMOTE</div></div>
<div class="kb-diagram-note">── 언더샘플링 (UnderSampling) ← 다수 클래스 감소</div>
<div class="kb-diagram-note">── 무작위 언더샘플링 (Random UnderSampling)</div>
<div class="kb-diagram-note">── Tomek Links / ENN (Edited Nearest Neighbour)</div>
<div class="kb-diagram-tree-item" style="--depth:0">알고리즘 수준 (Algorithm-Level)</div>
<div class="kb-diagram-note">── 비용 민감 학습 (Cost-Sensitive Learning)</div>
<div class="kb-diagram-note">── 앙상블 (Ensemble): BalancedBagging, EasyEnsemble</div>
<div class="kb-diagram-tree-item" style="--depth:0">평가 수준 (Evaluation-Level)</div>
<div class="kb-diagram-tree-item" style="--depth:2">Accuracy 대신 F1 · AUC · G-Mean 사용</div>
</div>
</div>



📢 **섹션 요약 비유**: 클래스 불균형은 마치 100명의 반 학생 중 1명만 빨간 옷을 입은 상황이다. 선생님이 "모두 파란 옷"이라 해도 99%가 맞아 보이지만, 빨간 옷을 찾는 임무는 완전히 실패한다.

## Ⅱ. 아키텍처 및 핵심 원리

### SMOTE 합성 샘플 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 원리

SMOTE는 소수 클래스 샘플 간 [k-최근접 이웃](/knowledge-base/studynote/10_ai/01_ai_basics/038_knn/)([k-NN](/knowledge-base/studynote/06_ict_convergence/05_data_science/352_knn_distance_metrics/), k-Nearest Neighbor)을 이용해 보간([Interpolation](/knowledge-base/studynote/14_data_engineering/04_mlops/187_time_series_interpolation_rollup_dashboard/)) 방식으로 새로운 합성 샘플을 만든다.

<strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a> 공식:</strong>
```
x_new = x_i + λ × (x_nn - x_i)

여기서:
  x_i   = 소수 클래스 임의 샘플
  x_nn  = x_i의 k-NN 중 무작위 선택된 이웃
  λ     = [0, 1] 범위의 난수 (균등 분포)
```

### SMOTE 샘플 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 과정 ([ASCII](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">피처 공간 (Feature Space)</div>
<div class="kb-diagram-note">F2</div>
<div class="kb-diagram-note">5 │ ○ ○</div>
<div class="kb-diagram-note">○</div>
<div class="kb-diagram-note">4 │ ● ○</div>
<div class="kb-diagram-note">★</div>
<div class="kb-diagram-note">3 │ ●</div>
<div class="kb-diagram-note">★</div>
<div class="kb-diagram-note">2 │ ○ ●</div>
<div class="kb-diagram-note">1 │ ○ ○</div>
<div class="kb-diagram-tree-item" style="--depth:1">F1</div>
<div class="kb-diagram-note">1 2 3</div>
<div class="kb-diagram-note">● = 소수 클래스 원본 (3개)</div>
<div class="kb-diagram-note">★ = SMOTE 합성 샘플 (보간점, 2개)</div>
<div class="kb-diagram-note">○ = 다수 클래스 원본</div>
<div class="kb-diagram-note">x_new = ● + λ × (인접● - ●)</div>
<div class="kb-diagram-note">→ 두 ● 사이 선분 위의 임의 점을 새 샘플로 생성</div>
</div>
</div>



### SMOTE 변형 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 비교

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 핵심 아이디어 | 장점 | 단점 |
|:---|:---|:---|:---|
| **SMOTE** | [k-NN](/knowledge-base/studynote/06_ict_convergence/05_data_science/352_knn_distance_metrics/) 이웃 간 선형 보간 | 단순·검증됨 | 경계선 근처 노이즈 샘플 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 가능 |
| **ADASYN** (Adaptive Synthetic [Sampling](/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/)) | [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 어려운 샘플에 더 많이 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 어려운 경계 집중 학습 | 과도한 노이즈 증폭 위험 |
| **Borderline-SMOTE** | 경계선 근처 소수 샘플만 선택 | 결정 경계 강화 | 경계 샘플 부족 시 효과 ↓ |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/">SVM</a>-SMOTE</strong> | [SVM](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) 서포트 벡터 주변 샘플 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 고차원 효과적 | 계산 비용 높음 |
| **SMOTENC** | 범주형+수치형 혼합 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 | 실무 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 적합 | 인코딩 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 복잡 |

### 언더샘플링 (UnderSampling) vs 오버샘플링 ([OverSampling](/knowledge-base/studynote/14_data_engineering/02_math_mining/096_oversampling_smote/))



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 불균형 해소 전략 비교</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">구분</div><div class="kb-diagram-cell">언더샘플링</div><div class="kb-diagram-cell">오버샘플링</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">방향</div><div class="kb-diagram-cell">다수 클래스 ↓</div><div class="kb-diagram-cell">소수 클래스 ↑</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 크기</div><div class="kb-diagram-cell">감소 (학습 빠름)</div><div class="kb-diagram-cell">증가 (학습 느림)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">정보 손실</div><div class="kb-diagram-cell">있음 (위험)</div><div class="kb-diagram-cell">없음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">과적합 위험</div><div class="kb-diagram-cell">낮음</div><div class="kb-diagram-cell">높음 (단순 복제 시)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">권장 상황</div><div class="kb-diagram-cell">데이터 충분</div><div class="kb-diagram-cell">데이터 희귀</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">대표 기법</div><div class="kb-diagram-cell">Tomek Links, ENN</div><div class="kb-diagram-cell">SMOTE, ADASYN</div></div>
</div>
</div>



📢 **섹션 요약 비유**: SMOTE는 두 점 사이에 점을 찍는 것이다. 빨간 공 두 개 사이에 새 빨간 공을 놓아 "비슷하지만 완전히 같지 않은" 새 예시를 만드는 것과 같다.

## Ⅲ. 비교 및 연결

### 평가 지표 선택 주의사항

불균형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 Accuracy는 사용하면 안 된다. 올바른 지표 선택이 핵심이다.

| 지표 | 공식 | 불균형 적합성 | 비고 |
|:---|:---|:---:|:---|
| Accuracy (정확도) | (TP+TN) / 전체 | ❌ 부적합 | 다수 클래스 편향 |
| [Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) ([정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)) | TP / (TP+[FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)) | ✅ | 오탐([FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)) 비용 높을 때 |
| [Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/) ([재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)) | TP / (TP+FN) | ✅ | 미탐(FN) 비용 높을 때 |
| [F1 Score](/knowledge-base/studynote/10_ai/03_llm_nlp/255_f1_score/) | 2×P×R / (P+R) | ✅ | P·R 균형 필요 시 |
| ROC-AUC | ROC 곡선 아래 면적 | ✅ | 전체 임계값 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) |
| G-Mean | √(Recall_pos × Recall_neg) | ✅✅ | 심각한 불균형 시 최선 |
| [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/)-AUC | [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 곡선 아래 면적 | ✅✅ | 소수 클래스 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 집중 |

### SMOTE 적용 시 [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Leakage 방지



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">❌ 잘못된 적용 (Data Leakage 발생):</div>
<div class="kb-diagram-note">전체 데이터 → SMOTE → 훈련/테스트 분할</div>
<div class="kb-diagram-note">(테스트 데이터에 합성 샘플 유입 → 평가 결과 부풀려짐)</div>
<div class="kb-diagram-note">✅ 올바른 적용:</div>
<div class="kb-diagram-note">전체 데이터 → 훈련/테스트 분할 → 훈련 데이터에만 SMOTE</div>
<div class="kb-diagram-note">(테스트 데이터는 반드시 원본 유지 → 공정한 평가)</div>
<div class="kb-diagram-note">✅ 파이프라인 적용 (sklearn Pipeline):</div>
<div class="kb-diagram-note">Pipeline([</div>
<div class="kb-diagram-note">('smote', SMOTE()),</div>
<div class="kb-diagram-note">('model', XGBClassifier())</div>
<div class="kb-diagram-note">])</div>
<div class="kb-diagram-note">→ cross_val_score로 CV 수행 시 각 폴드 내에서만 SMOTE 적용</div>
</div>
</div>



📢 **섹션 요약 비유**: 시험 문제를 미리 알고 공부(테스트에 SMOTE 적용)하면 점수가 높아 보이지만 실력이 아니다. 공부할 때(훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))만 연습 문제를 늘려야 진짜 실력이 오른다.

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 불균형 처리 파이프라인



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">불균형 데이터 처리 파이프라인</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">원시 데이터 EDA 전처리 SMOTE 모델 학습</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Raw Data</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">학습</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">비율 분석] 처리·정규화] 샘플생성]</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">불균형비율 훈련 데이터만</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">측정 (1%?) (테스트 제외)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">평가: F1 · AUC · PR-AUC 중심 (Accuracy 배제)</div></div>
</div>
</div>



### 기술사 판단 포인트

1. <strong>비율 <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/">10</a>:1 이하</strong>: 단순 클래스 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)(class_weight='balanced') 조정으로 충분
2. **비율 100:1 이상**: SMOTE + 언더샘플링 조합(SMOTEENN, SMOTETomek) 권장
3. <strong>고차원 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong>: SMOTE 직전 [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/)([Principal Component Analysis](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/)) [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) 권장
4. <strong>범주형 <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a> 혼합</strong>: SMOTENC 또는 인코딩 후 표준 SMOTE 적용
5. **실시간 추론 시스템**: 학습 시만 SMOTE, 추론 파이프라인에는 미적용

📢 **섹션 요약 비유**: 요리 연습(훈련)할 때는 재료를 다양하게 써도 되지만, 실제 손님 음식(테스트)에는 정해진 레시피대로만 만들어야 진짜 실력을 알 수 있다.

## Ⅴ. 기대효과 및 결론

### 기법별 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비교 (불균형비율 100:1 기준, 소수 클래스 기준)

| 접근 방식 | [Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/) (소수) | [Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) (소수) | [F1 Score](/knowledge-base/studynote/10_ai/03_llm_nlp/255_f1_score/) |
|:---|:---:|:---:|:---:|
| 불균형 그대로 학습 | 0.05 | 0.90 | 0.09 |
| 무작위 오버샘플링 | 0.65 | 0.52 | 0.58 |
| SMOTE 단독 적용 | 0.78 | 0.71 | 0.74 |
| SMOTE + ENN 조합 | 0.82 | 0.76 | 0.79 |
| ADASYN 적용 | 0.80 | 0.68 | 0.74 |

### 결론

SMOTE는 클래스 불균형 문제 해결의 사실상 표준 기법이지만 만능이 아니다. [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 공간 특성, 불균형 비율, 과적합 위험을 종합 고려해 적합한 변형 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)과 언더샘플링 조합을 선택해야 한다. 무엇보다 Accuracy가 아닌 F1·AUC·[PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/)-AUC 기반 평가가 필수이며, [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Leakage 방지를 위해 학습/평가 분리 파이프라인 설계가 선행되어야 한다.

📢 **섹션 요약 비유**: SMOTE는 시험 공부할 때 핵심 유형 문제를 더 많이 만들어 연습하는 것이다. 단, 실제 시험([테스트 데이터](/knowledge-base/studynote/04_software_engineering/11_testing_validation/444_test_data_management/))에는 그 연습 문제가 들어가면 안 된다—그건 답 알려주는 것과 같으니까.

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 문제 원인 | 클래스 불균형 (Class Imbalance) | 소수 클래스가 과소 대표되는 현상 |
| 핵심 해법 | SMOTE | 소수 클래스 [k-NN](/knowledge-base/studynote/06_ict_convergence/05_data_science/352_knn_distance_metrics/) 보간 합성 샘플 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| 변형 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | ADASYN | 어려운 경계 근처 집중 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| 변형 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | Borderline-SMOTE | 결정 경계 강화 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) |
| 반대 방향 해법 | 언더샘플링 (UnderSampling) | 다수 클래스 제거로 균형 달성 |
| 조합 기법 | SMOTEENN / SMOTETomek | 오버+언더샘플링 하이브리드 |
| 평가 지표 | [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/)-AUC / F1 / G-Mean | 불균형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 핵심 지표 |
| 주의사항 | [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Leakage | [테스트 데이터](/knowledge-base/studynote/04_software_engineering/11_testing_validation/444_test_data_management/)에 SMOTE 적용 금지 |

### 👶 어린이를 위한 3줄 비유 설명

1. 반에 100명 중 파란 옷 99명, 빨간 옷 1명이 있는데, AI가 "모두 파란 옷"이라 해도 99%가 맞아 보이지만 빨간 옷을 찾는 임무는 완전히 실패한다.

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">클래스 불균형 데이터 (소수 클래스 탐지 실패)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">오버샘플링: SMOTE · ADASYN · BorderlineSMOTE</div>
<div class="kb-diagram-note">언더샘플링: RandomUnder · NearMiss · Tomek Links</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">비용 민감 학습 · 임계값 조정 · Focal Loss</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">데이터 증강 (이미지: Augmentation · 텍스트: Back Translation)</div>
</div>
</div>


2. SMOTE는 빨간 옷 아이 두 명 사이에 "비슷하게 생긴 새 빨간 옷 아이"를 만들어줘서 AI가 빨간 옷의 특징을 더 잘 배우게 해준다.
3. 단, 시험 볼 때(테스트)는 진짜 빨간 옷 아이만 써야 한다—연습용 가짜 아이를 시험에 쓰면 점수가 부풀려지는 속임수가 된다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 231 / 258

← **이전**: [230. SVD (Singular Value Decomposition) 행렬 분해 랜덤 포레스트 XGBoost 부스팅](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/)
**다음**: [232. TF-IDF (Term Frequency-Inverse Document Frequency) 코사인 유사도 텍스트 임베딩 혼동](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) →

---
