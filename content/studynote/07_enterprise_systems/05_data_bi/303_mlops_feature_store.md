+++
title = "303. MLOps 피처 스토어 데이터마트 연동 (MLOps Feature Store)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-enterprise-systems"]

[extra]
tags = ["studynote-enterprise-systems"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Feature Store는 ML [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)를 중앙에서 관리해 학습과 서빙 시의 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 불일치([Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)-Serving Skew)를 근원적으로 차단한다.
> 2. **가치**: [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 재사용률이 60~80% 상승해 팀 간 중복 개발을 제거하고 모델 출시 시간을 2~5배 단축한다.
> 3. **판단 포인트**: Online Store의 읽기 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) <10ms 요건 충족 여부가 실시간 추천/사기 탐지 시스템의 핵심 SLA다.

## Ⅰ. 개요 및 필요성

ML 모델 개발에서 가장 많은 시간을 소비하는 단계는 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 엔지니어링([Feature 엔진ering](/knowledge-base/studynote/12_it_management/02_itsm_itil/865_feature_engineering/))이다.
각 팀이 동일한 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)를 독립적으로 구현하면, 학습 시 사용한 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 계산 로직과 서빙 시 계산 로직이 미묘하게 달라져 모델 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 저하된다. 이를 [Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)-Serving Skew라 한다.

[Feature Store](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) ([피처 스토어](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/))는 이 문제를 해결하기 위한 중앙화된 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 저장소·관리 플랫폼이다.
[피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)를 한 번 정의하면 오프라인 학습과 온라인 서빙 양측에서 동일한 계산 결과를 보장한다.

주요 제품: Feast ([오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)), Tecton (상용 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/951_saas/)), Hopsworks ([오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)+상용), AWS SageMaker [Feature Store](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/)

📢 **섹션 요약 비유**: Feature Store는 공용 식자재 창고다. 각 요리사(팀)가 자기 냉장고에 따로 재료를 보관하면 유통기한이 달라지지만, 공용 창고를 쓰면 모두 같은 신선도의 재료로 요리한다.

## Ⅱ. 아키텍처 및 핵심 원리

### 온라인 스토어 vs 오프라인 스토어

| 항목 | 온라인 스토어 (Online Store) | 오프라인 스토어 (Offline Store) |
|:---|:---|:---|
| 저장소 | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/), [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/), [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) | [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/), S3 ([Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)), [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) |
| 읽기 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | <10ms (p99) | 수초~수분 |
| 주 용도 | 실시간 모델 서빙 | 배치 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 형태 | 최신 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)값 (Point-in-Time) | 시계열 전체 이력 |
| 비용 | 높음 (인메모리) | 낮음 (스토리지) |

### [ASCII](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램: [Feature Store](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) 아키텍처

```
  원천 데이터
  +----------+  +----------+  +----------+
  | 이벤트 로그|  |  RDB 거래  |  | 사용자 프로필|
  +----+-----+  +----+-----+  +----+-----+
       +--------------+--------------+
                      v
            +---------------------+
            |  Feature Pipeline   | (Spark / Flink)
            +----------+----------+
               +-------+--------+
               v                v
  +---------------------+  +---------------------+
  |   Offline Store     |  |   Online Store      |
  |  (S3 / Hive)        |  |  (Redis Cluster)    |
  |  학습 데이터 생성용  |  |  서빙 시 <10ms 조회  |
  +--------+------------+  +--------+------------+
           |                        |
           v                        v
  +-----------------+    +-----------------------+
  |  ML Training    |    |  Real-time Serving    |
  |  (Batch)        |    |  (API, <100ms 응답)    |
  +-----------------+    +-----------------------+
```

### Feast vs Tecton vs Hopsworks

| 항목 | Feast | Tecton | Hopsworks |
|:---|:---|:---|:---|
| 유형 | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | 상용 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/951_saas/) | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)+상용 |
| 실시간 변환 | 미지원 | 지원 (Streaming) | 지원 |
| 온라인 스토어 | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/), [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) | 자체 | RonDB |
| [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 | 제한적 | 강력 | 강력 |

📢 **섹션 요약 비유**: 오프라인 스토어는 대형 창고, 온라인 스토어는 계산대 옆 빠른 진열대다. 손님(모델)이 주문하면 계산대 옆에서 즉시 집어준다.

## Ⅲ. 비교 및 연결

### [Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)-Serving Skew 방지 메커니즘

| 상황 | Skew 없이 | Skew 발생 시 |
|:---|:---|:---|
| 나이 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 계산 | Feature Store에서 동일 [함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/) | 학습: pandas, 서빙: Java -> 소숫점 오차 |
| 결측값 처리 | 스토어 레벨에서 통일 | 학습: 0 대체, 서빙: -1 대체 |
| 7일 윈도우 집계 | Point-in-Time Correct [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 보장 | 미래 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 누수([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Leakage) |

📢 **섹션 요약 비유**: [Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)-Serving Skew는 레시피가 두 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)인데 맛이 다른 상황이다. Feature Store는 레시피를 하나로 통일해 주방 어디서든 같은 맛을 보장한다.

## Ⅳ. 실무 적용 및 기술사 판단

### [Feature Store](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [ ] 현재 팀 간 동일 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)가 중복 구현되고 있는가? (2팀 이상이면 도입 정당화)
- [ ] Online Store 읽기 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/869_sla/) <10ms 충족 가능한 [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 클러스터 확보 여부
- [ ] Point-in-Time Correct [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 지원 여부 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)
- [ ] [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) [버저닝](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/317_versioning_data_model_design/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 수립 (메이저/마이너 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리)
- [ ] [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링: 드리프트 감지 (PSI >0.2 알람)

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

| [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) | 문제 | 해결 방법 |
|:---|:---|:---|
| [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)를 모델별로 개별 관리 | 동일 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 수십 중복, Skew 발생 | [Feature Store](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) 중앙화 |
| Online Store에 모든 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 저장 | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 메모리 비용 폭증 | 서빙 필요 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)만 선택적 저장 |
| Point-in-Time 조인 미적용 | 미래 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 누수 -> 과평가 모델 | Feast/Tecton PiT [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 활용 |

📢 **섹션 요약 비유**: Point-in-Time Join은 시험 당일 기준 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 보는 것이다. 미래 정답을 미리 알고 풀면 성적이 좋아도 실제로는 틀린 것이다.

## Ⅴ. 기대효과 및 결론

### 기대효과

| 항목 | 도입 전 | 도입 후 |
|:---|:---|:---|
| [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 개발 시간 | 모델당 2~4주 | 1~3일 (기존 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 재사용) |
| [Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)-Serving Skew | 빈번 (모델 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 20~30%) | 거의 없음 |
| 온라인 추론 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 50~200ms | <10ms (사전 계산·[캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)) |
| [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 재사용률 | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)% 미만 | 60~80% |

### 한계 및 선결 과제

- [Feature Store](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) 인프라 자체가 운영 부담 -> 플랫폼 팀 전담 필요
- [Cold start](/knowledge-base/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/): 히스토리 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 없는 신규 사용자 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 처리 별도 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 필요
- Streaming [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)(실시간 집계)는 Flink/[Spark Streaming](/knowledge-base/studynote/16_bigdata/03_spark/060_spark_streaming_dstream/) 연동 복잡도 높음

📢 **섹션 요약 비유**: Feature Store는 도서관 사서다. 각자 책([피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/))을 집에만 두면 남들은 못 쓰지만, 사서가 관리하면 누구든 빌려 쓰고 항상 최신판을 보장받는다.

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [Feature Store](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) | 중심 | [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 중앙 관리 플랫폼 |
| Online Store | 구성 요소 | 실시간 서빙용 인메모리 저장소 |
| Offline Store | 구성 요소 | 배치 학습용 대용량 저장소 |
| [Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)-Serving Skew | 해결 대상 | 학습/서빙 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 불일치 문제 |
| Point-in-Time [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) | 핵심 기능 | 과거 시점 기준 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 조인 |

### 📈 관련 키워드 및 발전 흐름도

```
실험실 ML 모델 - 프로덕션 배포 단절 문제
    |
    v
수작업 피처 엔지니어링 반복 - 일관성 부재
    |
    v
Feature Store 등장 - 피처 재사용·공유 플랫폼
    |
    v
온라인(Redis)/오프라인(Hive) 이중 저장 구조
    |
    v
MLOps 통합 - 피처->모델->서빙 자동화 파이프라인
```

> **키워드**: [Feature Store](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/), [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/), [Feature 엔진ering](/knowledge-base/studynote/12_it_management/02_itsm_itil/865_feature_engineering/), Online Store, Offline Store, Feast, [Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)-Serving Skew

### 👶 어린이를 위한 3줄 비유 설명

1. [피처 스토어](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/)는 마트 진열대예요. 여러 요리사(모델)가 같은 재료([피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/))를 진열대에서 가져다 쓰니 항상 같은 재료를 써요.
2. 온라인 스토어는 손님 바로 앞 빠른 진열대, 오프라인 스토어는 창고 깊숙이 있는 대량 저장고예요.
3. [Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)-Serving Skew 방지는 시험 준비할 때와 실제 시험에서 똑같은 교재를 쓰는 것이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 303 / 482

<- **이전**: [302. 데이터옵스 CI/CD 파이프라인 자동 테스팅 (DataOps CI/CD dbt)](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/302_dataops_cicd_dbt/)
**다음**: [304. 실시간 CDP 아키텍처 1st Party 클릭 로그 수집 통합 (Real-time CDP Architecture)](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/304_realtime_cdp_architecture/) ->

---
