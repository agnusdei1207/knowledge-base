---
title: "108. 이상 탐지 (Anomaly Detection) — 통계/ML/딥러닝 기반 이상치 감지"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) ([Anomaly](/studynote/05_database/04_transactions_concurrency/530_anomaly/) [Detection](/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/))는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 정상 패턴에서 유의미하게 벗어난 관측치를 자동으로 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하는 기법으로, 레이블 없는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서도 적용 가능한 비지도·준지도 학습의 핵심 응용 분야다.
> 2. **가치**: 금융 사기 (Financial Fraud), 네트워크 침입 (Network Intrusion), 설비 고장 예지 (Predictive Maintenance), 의료 이상 진단 등 "정상의 소수 이탈 패턴"이 막대한 비용을 유발하는 모든 영역에서 조기 경보 시스템의 역할을 한다.
> 3. **판단 포인트**: Z-score/IQR 같은 통계 방법은 단변량에 강하고, [Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) Forest·One-Class [SVM](/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) ([Support Vector Machine](/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/))은 고차원 표형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 유효하며, [Autoencoder](/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/)/LSTM은 시퀀스·이미지 [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)에서 강점을 보인다.

---

## Ⅰ. 개요 및 필요성

정상 거래 수백만 건 중 단 몇 건의 사기 거래를 찾아내는 것, 수백 대의 장비 센서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 한 대의 조기 고장 징후를 감지하는 것—[이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)는 이처럼 극소수의 비정상 사례를 실시간으로 포착하는 기술이다.

[이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)가 일반 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 문제와 다른 핵심적 이유는 <strong>극심한 클래스 불균형 (Class Imbalance)</strong>이다. 사기 거래는 전체의 0.01%도 안 될 수 있으며, 이 경우 단순히 "모든 것이 정상"이라고 예측해도 99.99% 정확도가 나온다. 진짜 이상을 탐지하려면 정확도가 아닌 [재현율](/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/) ([Recall](/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/))과 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) ([Precision](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/))의 균형이 중요하다.

- **📢 섹션 요약 비유**: [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)는 수백만 명의 승객 중 위험물을 숨긴 한 명을 공항 보안 검색대에서 잡아내는 것이다. 오탐(무고한 사람을 잡음)과 미탐(진짜 위험인물을 놓침) 사이의 균형이 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 이상 유형 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)

```text
+--------------------------------------------------------------------+
|                     이상 유형 3가지                                |
+------------------+---------------------+---------------------------+
|  점 이상치       |  문맥적 이상치      |  집단 이상치              |
|  (Point Anomaly) |  (Contextual Anomaly|  (Collective Anomaly)     |
+------------------+---------------------+---------------------------+
|  ● <- 이상        |  일반: 기온 35℃     |  각 점은 정상이나         |
|                  |  맥락: 한겨울 35℃  |  패턴 전체가 비정상       |
|  정상 데이터    |  -> 계절 맥락이 핵심 |  예: 특정 시간대 집단     |
|  분포에서 멀리   |                     |  구매 급증 (카드 복제)    |
|  벗어난 단일값  |                     |                           |
+------------------+---------------------+---------------------------+
```

### 주요 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 비교

| [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 원리 | 장점 | 단점 | 적합 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
|:---|:---|:---|:---|:---|
| **Z-score / IQR** | 평균±k·σ 또는 사분위 범위 | 단순, 빠름 | 단변량, 정규분포 가정 | 단순 수치 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| <strong><a href="/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/">Isolation</a> Forest</strong> | [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)는 적은 분기로 고립됨 | 고차원, 빠름 | 국소 이상에 약함 | 표형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| <strong>One-Class <a href="/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/">SVM</a></strong> | 정상 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경계 학습 | [커널 트릭](/studynote/10_ai/01_ai_basics/059_kernel_trick_rbf_polynomial/) | 대용량에 느림 | 중소규모 고차원 |
| <strong>LOF (Local <a href="/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/">Outlier</a> Factor)</strong> | 국소 밀도 비교 | 국소 이상 강함 | O(n^) 느림 | 중규모 |
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/">Autoencoder</a></strong> | 정상 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재구성 학습, 복원 오차 | [비정형 데이터](/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/) | 학습 비용 | 이미지, 시계열 |
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/292_lstm/">LSTM</a> (<a href="/studynote/10_ai/04_ai_ops_ethics/292_lstm/">Long Short-Term Memory</a>)</strong> | 시퀀스 패턴 학습 | 시계열 의존성 | 학습 복잡 | 시계열, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) |

- **📢 섹션 요약 비유**: [Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) Forest는 "이상한 사람은 군중 속에 숨기 어렵다"는 원리를 사용한다. 나무에서 가지를 몇 번 자르면 고립되는 사람이 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)다.

---

## Ⅲ. 비교 및 연결

| 항목 | [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) (비지도) | 이진 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) (지도학습) |
|:---|:---|:---|
| **레이블 필요** | 불필요 | 필수 |
| **적합 상황** | 이상 사례가 드물고 레이블링 불가 | 충분한 사기/정상 레이블 보유 |
| **모델 업데이트** | 드리프트 (Drift) 자동 적응 필요 | 재학습 주기 필요 |
| **오탐률** | 상대적으로 높음 | 낮음 (정보가 충분할 때) |
| <strong>대표 <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong> | [Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) Forest, [Autoencoder](/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/) | XGBoost, LightGBM |

스트리밍 [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)에서는 [Apache Kafka](/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) + Flink [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인에 [Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) Forest 또는 [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/) 모델을 연동하여 실시간 점수를 계산한다. 임계값 (Threshold) 자동 조정과 [컨셉 드리프트](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/) ([Concept Drift](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)) 탐지가 실무 운영의 핵심 과제다.

- **📢 섹션 요약 비유**: 비지도 [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)는 "어떤 것이 이상한지 모르지만, 평소와 다른 것을 감지"하는 방법이고, 지도학습 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)는 "이전에 본 사기 패턴을 기억해두고 같은 패턴을 잡는" 방법이다. 전혀 새로운 유형의 사기에는 비지도 방식이 더 강하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적용 시나리오

1. <strong>금융 사기 탐지 (<a href="/studynote/13_cloud_architecture/05_data_engineering/267_gnn_fraud_detection_knowledge_graph/">FDS</a>, Fraud <a href="/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/">Detection</a> System)</strong>: 실시간 거래마다 [Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) Forest 점수 계산 -> 임계값 초과 시 즉시 차단
2. **제조 설비 예지 보전**: 진동·온도·[전류](/studynote/01_computer_architecture/01_basic_electronics_logic/002_current/) 시계열 -> [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/) [Autoencoder](/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/) 복원 오차 급증 = 고장 조기 경보
3. **사이버 보안**: 네트워크 트래픽 패턴 이상 -> One-Class SVM으로 [제로데이](/studynote/09_security/15_malware_attack_vectors/761_zero_day/) 공격 탐지
4. <strong>의료 <a href="/studynote/02_operating_system/04_synchronization/229_monitor/">모니터</a>링</strong>: ICU 환자 생체 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) -> 실시간 [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/) [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)로 급변 조기 알림

### 기술사 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 이상 유형이 점, 문맥, 집단 중 무엇인지 먼저 정의했는가?
2. 레이블된 이상 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 충분히 있다면 지도학습 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)가 더 효과적이다
3. 스트리밍 환경에서 [컨셉 드리프트](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/) ([Concept Drift](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)) [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 있는가?
4. 오탐 (False Positive)과 미탐 (False Negative)의 비즈니스 비용을 비교했는가? (금융: 미탐 비용이 오탐보다 훨씬 큼)
5. 설명 가능성 ([XAI](/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/), [eXplainable AI](/studynote/14_data_engineering/05_exam_keywords/255_xai_lime_shap_explainable_contribution/))이 필요하면 [SHAP](/studynote/10_ai/04_ai_ops_ethics/327_shap/) 값으로 [Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) Forest 결과를 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)했는가?

- **📢 섹션 요약 비유**: [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) 임계값 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)은 화재 경보기 감도를 조절하는 것과 같다. 너무 민감하면 밥 태울 때마다 울리고 (오탐), 너무 둔하면 진짜 화재를 놓친다 (미탐).

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 손실 예방 | 금융 사기 조기 차단으로 연간 수억~수십억 피해 방지 |
| 설비 가동률 향상 | 예지 보전으로 갑작스러운 라인 중단 방지 |
| 보안 강화 | [시그니처 기반 탐지](/studynote/09_security/05_web_app_security/235_signature_based_detection_misuse_known_attacks/)가 잡지 못하는 [제로데이](/studynote/09_security/15_malware_attack_vectors/761_zero_day/) 위협 감지 |
| 의료 안전 | 중환자 생체 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 이상 자동 알림으로 의료 사고 예방 |
| 자동화 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 | 24/7 실시간 이상 감지로 인력 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 비용 절감 |

[이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)는 "모르는 것을 모른다는 것을 아는" 기술이다. 정상의 경계를 정의함으로써 그 경계 밖의 모든 것을 자동으로 경보 대상으로 만드는 이 접근은, 레이블이 없어도 동작한다는 점에서 빅데이터 시대 실무에서 독보적 가치를 지닌다. 딥러닝 기반 Autoencoder와 실시간 스트리밍 처리의 결합이 미래 [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)의 표준 아키텍처로 자리 잡고 있다.

- **📢 섹션 요약 비유**: [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)는 의사가 정상 혈액 수치 범위를 외워두고 환자의 수치가 그 범위를 벗어나는 순간 즉각 주목하는 것과 같다. 평소와 다르다는 것 자체가 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|
| [Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) Forest | 랜덤 분기로 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)를 빠르게 고립시키는 비지도 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| One-Class [SVM](/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) ([Support Vector Machine](/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/)) | 정상 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 결정 경계 학습 |
| [Autoencoder](/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/) | 재구성 오차 기반 딥러닝 [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) |
| [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/) ([Long Short-Term Memory](/studynote/10_ai/04_ai_ops_ethics/292_lstm/)) | 시계열 [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)의 핵심 모델 |
| [컨셉 드리프트](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/) ([Concept Drift](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)) | 시간에 따라 정상 패턴이 변하는 현상 |
| [FDS](/studynote/13_cloud_architecture/05_data_engineering/267_gnn_fraud_detection_knowledge_graph/) (Fraud [Detection](/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/) System) | 금융 [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)의 대표 응용 |
| [SHAP](/studynote/10_ai/04_ai_ops_ethics/327_shap/) ([SHapley Additive exPlanations](/studynote/10_ai/04_ai_ops_ethics/327_shap/)) | [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) 결과의 설명 가능성 도구 |

### 📈 관련 키워드 및 발전 흐름도

```text
[통계적 방법 (Statistical Method) — 기준선 이탈 탐지]
    |
    v
[머신러닝 기반 (ML-based) — Isolation Forest/Autoencoder]
    |
    v
[시계열 분석 (Time-series Analysis) — 계절성 제거]
    |
    v
[스트리밍 탐지 (Streaming Detection) — 실시간 처리]
    |
    v
[설명 가능 AI (XAI, Explainable AI) — 탐지 근거 제공]
```

이 흐름은 통계적 [기준선](/studynote/04_software_engineering/01_overview_principles/025_baseline/)에서 출발해 [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/), 시계열, 스트리밍으로 정교해지고, 마지막에 XAI로 탐지 이유를 설명하는 방향으로 발전한다.

### 👶 어린이를 위한 3줄 비유 설명
- [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)는 "보통과 다른 것"을 자동으로 찾아내는 거예요. 모든 사과 중에 썩은 사과 하나를 찾는 것처럼요.
- 컴퓨터가 "정상이 어떻게 생겼는지"를 먼저 배우고, 그것과 많이 다른 것이 나타나면 "이상하다!"고 알려줘요.
- 은행 카드 사기, 공장 기계 고장, 해킹 시도를 이렇게 미리 잡아낼 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 111 / 262

<- **이전**: [107. 소셜 네트워크 분석 (SNA, Social Network Analysis) — 중심성/커뮤니티 탐지](/studynote/16_bigdata/05_analysis/110_social_network_analysis/)
**다음**: [109. 시계열 분석 (Time Series Analysis) — ARIMA/Prophet/LSTM 시계열 예측](/studynote/16_bigdata/05_analysis/112_time_series_analysis/) ->

---
