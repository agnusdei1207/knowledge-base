+++
title = "61. 데이터 마이닝 프레임워크 - KDD와 CRISP-DM"
date = 2026-04-10

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마이닝은 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)만 돌리는 일이 아니라, 문제 정의부터 배포까지 이어지는 프로세스다.
> 2. **구조**: [KDD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/225_kdd_t_test_anova_statistical_analysis/) (Knowledge Discovery in Databases)는 학문적 5단계 절차이고, CRISP-DM (Cross-Industry Standard [Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/) for [Data Mining](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/284_data_mining_association_classification_clustering_crisp_dm/))은 비즈니스 중심 6단계 표준이다.
> 3. **판단**: 좋은 결과는 모델보다 [데이터 정제](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/266_data_cleansing/), 비즈니스 이해, 평가와 배포에서 더 많이 결정된다.

---

## Ⅰ. 개요 및 필요성

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 많다고 지식이 저절로 나오지는 않는다. 분석 목적, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 준비, 해석, 실행까지 흐름이 있어야 비로소 쓸모가 생긴다.

KDD와 CRISP-DM은 이 흐름을 표준화해 주는 지도다. 분석가가 산으로 가는 걸 막고, 결과를 실제 업무로 연결하게 만든다.

- **📢 섹션 요약 비유**: 재료만 잔뜩 있다고 요리가 되지 않는 것처럼, 순서와 레시피가 있어야 음식이 완성된다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">KDD</div>
<div class="kb-diagram-note">선택 -&gt; 전처리 -&gt; 변환 -&gt; 마이닝 -&gt; 해석/평가</div>
<div class="kb-diagram-note">CRISP-DM</div>
<div class="kb-diagram-note">비즈니스 이해 -&gt; 데이터 이해 -&gt; 데이터 준비 -&gt; 모델링 -&gt; 평가 -&gt; 배포</div>
</div>
</div>



| [KDD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/225_kdd_t_test_anova_statistical_analysis/) | 의미 |
| :-- | :-- |
| [Selection](/knowledge-base/studynote/10_ai/01_ai_basics/022_mcts_four_stages/) | 필요한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 고르기 |
| Preprocessing | 결측치/[이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 정리 |
| Transformation | 모델이 먹기 좋게 변환 |
| [Data Mining](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/284_data_mining_association_classification_clustering_crisp_dm/) | [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 적용 |
| Interpretation | 결과 해석 및 지식화 |

| CRISP-DM | 의미 |
| :-- | :-- |
| Business Understanding | 비즈니스 목표 정의 |
| [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Understanding | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 상태 파악 |
| [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Preparation](/knowledge-base/studynote/09_security/13_secops_ir_forensics/654_ir_preparation/) | 전처리 및 통합 |
| Modeling | 모델 학습 |
| Evaluation | 사업 목표와 결과 비교 |
| [Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/) | 실제 업무 적용 |

KDD는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학의 공정도 같고, CRISP-DM은 실제 비즈니스 프로젝트의 운영표에 가깝다. 둘 다 "모델"보다 "과정"을 더 크게 본다.

- **📢 섹션 요약 비유**: 원석을 캐는 공장과, 그 원석을 팔 수 있게 포장하는 경영 계획이 각각 있는 셈이다.

---

## Ⅲ. 비교 및 연결

| 항목 | [KDD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/225_kdd_t_test_anova_statistical_analysis/) | CRISP-DM |
| :-- | :-- | :-- |
| 출발점 | [데이터 중심](/knowledge-base/studynote/04_software_engineering/06_software_architecture/383_data_centric_architecture/) | 비즈니스 중심 |
| 강점 | 정제와 변환 강조 | 프로젝트 적용성 높음 |
| 약점 | 운영/배포 약함 | 학문적 엄밀성은 덜 강조 |
| 공통점 | 프로세스 중심 | 프로세스 중심 |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Data Swamp</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">정제 / 변환</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">모델링</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">평가</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">비즈니스 가치</div>
</div>
</div>



[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마이닝은 "좋은 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 찾기"보다 "문제를 올바르게 정의하고, 결과를 실제 업무에 연결하는 것"이 더 중요하다.

- **📢 섹션 요약 비유**: 길을 잘 찾는 것도 중요하지만, 어디로 갈지 먼저 정하는 게 더 중요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 비즈니스 목표가 명확한가?
2. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질과 정제 계획이 충분한가?
3. 모델 성능보다 현업 가치가 측정되는가?
4. 배포 후 모니터링과 재학습이 있는가?
5. 분석 결과를 실제 액션으로 바꿀 수 있는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)부터 먼저 고르는 설계
- 전처리를 가볍게 보고 모델만 신경 쓰는 설계
- 평가 없이 보고서만 만드는 설계
- 배포와 운영을 빼먹는 일회성 분석

기술사 관점에서는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마이닝을 기술 데모가 아니라 운영 가능한 의사결정 프로세스로 봐야 한다. 그래서 결과 해석과 실행 계획이 꼭 붙어야 한다.

- **📢 섹션 요약 비유**: 씨앗을 심는 것보다, 실제로 열매를 따서 팔 수 있어야 농사가 끝나는 것이다.

---

## Ⅴ. 기대효과 및 결론

KDD와 CRISP-DM은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마이닝을 체계화해, 분석이 연구로 끝나지 않고 사업 가치로 이어지게 한다.

결국 중요한 것은 모델의 화려함이 아니라, 문제 정의부터 배포까지 하나의 흐름으로 이어지는지다.

- **📢 섹션 요약 비유**: 퍼즐 조각을 맞추는 데서 끝나는 게 아니라, 완성된 그림을 벽에 걸어야 진짜 의미가 있다.

---

## 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Business Problem</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">KDD / CRISP-DM</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Data Preparation</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Modeling / Evaluation</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Deployment</div>
</div>
</div>



---

## 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">데이터 정제</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">KDD</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">CRISP-DM</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">모델링</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">배포 / 모니터링</div>
</div>
</div>



---

## 어린이를 위한 3줄 비유 설명

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마이닝은 그냥 기계에 숫자를 넣는 게 아니에요.  
무엇을 찾을지 정하고, 자료를 깨끗이 하고, 결과를 확인해야 해요.  
그래야 진짜 쓸모 있는 답을 얻을 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 61 / 258

← **이전**: [60. 다크 데이터 (Dark Data) 발굴 및 프라이버시 클린 룸 (Privacy Clean Room)](/knowledge-base/studynote/14_data_engineering/01_infrastructure/060_dark_data_discovery_privacy_clean_room/)
**다음**: [62. 탐색적 데이터 분석 (EDA, Exploratory Data Analysis)](/knowledge-base/studynote/14_data_engineering/02_math_mining/062_eda_exploratory_data_analysis/) →

---
