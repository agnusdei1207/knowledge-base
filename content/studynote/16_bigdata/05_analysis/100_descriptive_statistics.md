+++
title = "기술 통계 (Descriptive Statistics)"
date = 2025-05-22

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
- <strong>기술 통계 (Descriptive <a href="/knowledge-base/studynote/05_database/03_relational_model/168_clustering_factor_index_physical_alignment/">Statistics</a>)</strong>: 수집된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 전체적인 특징을 요약하고 설명하기 위해 평균, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/), 분포 등을 산출하는 기초 통계 방법론.
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 가시화</strong>: 숫자로 된 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 중심 경향성(Central Tendency)과 산포도([Dispersion](/knowledge-base/studynote/03_network/03_physical_layer_media/133_dispersion_mode_chromatic/)) 지표로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)하여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 '모양'을 파악함.
- **분석의 기초**: [추론 통계](/knowledge-base/studynote/16_bigdata/05_analysis/101_inferential_statistics/)로 나아가기 전, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)([Outlier](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/))를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고 변수의 성질을 이해하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학의 필수 관문.

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
수백만 건의 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([Raw](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 자체는 인간이 해석하기 어렵습니다. 기술 통계는 이러한 방대한 정보를 몇 개의 대표적인 수치와 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)로 요약하여, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 무엇을 말하고 있는지 직관적으로 전달하는 역할을 합니다. 이는 모든 빅데이터 분석 및 기계 학습 모델링의 출발점입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
기술 통계의 주요 측정 지표와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 요약 프로세스 아키텍처입니다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Descriptive Statistics Architecture Map</div></div>
<div class="kb-diagram-note">Raw Data Pool (ZB Scale)</div>
<div class="kb-diagram-note">v</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Data Summary Metrics</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. Central Tendency (중심 경향성)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- Mean, Median, Mode</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. Dispersion / Variability (산포도)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- Variance, Std Dev, IQR, Range</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. Shape / Distribution (분포/모양)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- Skewness (왜도), Kurtosis (첨도)</div></div>
<div class="kb-diagram-note">v</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Visualization Methods</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Histogram, Box Plot, Scatter Plot)</div></div>
</div>
</div>



**핵심 원리:**
1. **중심 경향성**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어디에 모여 있는가? (평균은 [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)에 민감하므로 중앙값과 함께 고려).
2. **산포도**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 얼마나 퍼져 있는가? (표준편차가 클수록 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 불확실성이 높음).
3. **분포의 비대칭성**: [왜도](/knowledge-base/studynote/14_data_engineering/02_math_mining/064_skewness_kurtosis_log_transformation/)([Skewness](/knowledge-base/studynote/14_data_engineering/02_math_mining/064_skewness_kurtosis_log_transformation/))가 양수면 왼쪽으로 치우친(긴 꼬리가 오른쪽) 형태이며, 이는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전처리([로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 변환 등)의 근거가 됨.
4. **IQR (Interquartile Range)**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 중간 50% 범위를 의미하며, 박스 플롯(Box Plot)을 통해 [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)를 정의하는 기준이 됨.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | 기술 통계 (Descriptive) | [추론 통계](/knowledge-base/studynote/16_bigdata/05_analysis/101_inferential_statistics/) (Inferential) |
| :--- | :--- | :--- |
| **목적** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 설명 및 요약 | 표본을 통한 모집단 특성 예측 |
| **결과물** | 평균, 도표, [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) | [p-value](/knowledge-base/studynote/06_ict_convergence/05_data_science/337_p_value_significance/), 신뢰구간, 가설 채택 |
| **범위** | 현재 보유한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전체 | 불확실성을 포함한 전체 모집단 |
| **수행 시점** | 분석 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) ([EDA](/knowledge-base/studynote/12_it_management/02_itsm_itil/064_eda/) 단계) | 분석 중기 ([가설 검정](/knowledge-base/studynote/08_algorithm_stats/08_stats/145_hypothesis_testing/) 단계) |
| **핵심 질문** | "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어떻게 생겼는가?" | "이 결과가 우연이 아닌가?" |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
* <strong>적용 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> (Implementation <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">Strategy</a>)</strong>:
  * <strong><a href="/knowledge-base/studynote/10_ai/05_data_science_ml/397_outlier_mahalanobis/">이상치 탐지</a></strong>: 기술 통계 산출 시 평균과 중앙값의 차이가 크다면 [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 존재를 의심하고, Box Plot의 Whisker를 벗어나는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 대한 정제 로직(Capping, Trimming) 적용.
  * <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a></strong>: 분포([왜도](/knowledge-base/studynote/14_data_engineering/02_math_mining/064_skewness_kurtosis_log_transformation/)/첨도)를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하여 [정규 분포](/knowledge-base/studynote/08_algorithm_stats/08_stats/138_normal_distribution/)를 따르지 않는 경우 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)([Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))를 통해 ML 모델의 학습 효율 극대화.
* **기술사적 판단 (Architectural Judgment)**:
  * 빅데이터 환경에서는 극단적인 [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 하나가 전체 평균을 왜곡하기 쉬움. 따라서 단순 평균(Arithmetic Mean)보다는 절사 평균(Trimmed Mean)이나 중앙값(Median)을 대표값으로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하는 견고한(Robust) 분석 설계가 필요함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
기술 통계는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 대한 '객관적인 요약본'을 제공하여 의사결정의 편향을 방지합니다. 향후에는 수조 개의 행을 가진 초거대 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋에서도 실시간으로 기술 통계 지표를 계산하고 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)하는 스트리밍 통계 기술(Sketching algorithms 등)이 플랫폼의 핵심 경쟁력이 될 것입니다.

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
* **기초 통계**: Mean/Median/Mode, [Variance](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)/Standard Deviation
* **분포 분석**: [Normal Distribution](/knowledge-base/studynote/08_algorithm_stats/08_stats/138_normal_distribution/), [Skewness](/knowledge-base/studynote/14_data_engineering/02_math_mining/064_skewness_kurtosis_log_transformation/)/Kurtosis, Z-Score
* <strong><a href="/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/">시각화</a> 도구</strong>: Histogram, Box-and-Whisker Plot, Five-number [Summary](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/300_summary/)

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">기초 통계</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">분포 분석</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">상관 분석</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">시각화 도구</div></div>
</div>
</div>



이 흐름도는 선행 개념이 현재 개념으로 응축되고, 다시 확장 개념으로 이어지는 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 우리 반 친구들의 키를 일일이 다 말하는 대신, "우리 반 평균 키는 140cm야"라고 짧게 줄여 말하는 것이 기술 통계예요.
2. 키가 제일 큰 친구와 작은 친구의 차이가 얼마나 나는지도 알려주면 우리 반의 특징을 더 잘 알 수 있죠.
3. 복잡한 관찰 일기를 사진 한 장으로 요약해서 보여주는 것과 같답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 100 / 262

← **이전**: [24. 실시간 OLAP (Real-time OLAP) — Apache Druid/Pinot/ClickHouse](/knowledge-base/studynote/16_bigdata/04_streaming/099_realtime_olap/)
**다음**: [추론 통계 (Inferential Statistics)](/knowledge-base/studynote/16_bigdata/05_analysis/101_inferential_statistics/) →

---
