---
title: "DataOps CI/CD with dbt"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 356
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DataOps는 DevOps의 원칙(자동화, 협업, 빠른 피드백)을 [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)에 적용해 분석 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 품질 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 배포 속도를 높이는 방법론이다.
> 2. **핵심 도구**: dbt ([data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) build tool)는 SQL [SELECT](/studynote/05_database/04_transactions_concurrency/520_select/) 문을 변환 모델(Transformation Model)로 다루어, [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 테스트 문서화 의존성 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)를 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환에 제공하는 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 프레임워크다.
> 3. **품질 게이트**: [데이터 계약](/studynote/16_bigdata/12_trends/236_data_contract/)([Data Contract](/studynote/16_bigdata/12_trends/236_data_contract/))은 생산자와 소비자 간의 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/) ([Service Level Agreement](/studynote/12_it_management/02_itsm_itil/869_sla/)) 의미론적 합의를 코드로 명문화해 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 하위 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)을 보장하는 핵심 메커니즘이다.

---

## I. 개요 및 필요성

[데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)은 전통적으로 소수의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어가 수동으로 배포하고, 변경 이력 관리가 부실하며, 테스트가 없거나 프로덕션 직접 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)에 의존했다. 분석 팀이 늘어나고 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소비자(ML 모델, 대시보드, 리포트)가 다양해질수록 이 방식은 더 이상 지속 불가능하다.

DataOps는 다음 세 가지 문제를 해결한다.

1. **느린 배포 사이클**: [코드 리뷰](/studynote/04_software_engineering/06_software_architecture/330_code_review/) 없이 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 스크립트를 수동으로 배포하면 변경이 한 달에 수회에 불과하다. [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 자동화로 하루 수십 회 배포를 목표로 한다.
2. **품질 불투명**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [결함](/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)이 다운스트림 대시보드 ML 모델 오염으로 연쇄되기 전까지 인지하지 못하는 구조를 자동 품질 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)으로 사전 차단한다.
3. **협업 단절**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어 분석가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 사이언티스트가 서로 다른 도구와 프로세스로 작업해 [사일로](/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)가 형성된다.

dbt는 분석가가 친숙한 SQL로 변환 로직을 작성하면서 소프트웨어 엔지니어링의 모범 사례([버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리, 테스트, 문서)를 적용할 수 있게 해준다.

- **📢 섹션 요약 비유**: DataOps는 [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)에 교통 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)등을 설치하는 것이다. 기존에는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 빨간불을 무시하고 달리다 사고([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 문제)가 나도 몰랐지만, 이제는 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)등([CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD, 품질 검사)이 자동으로 통제한다.

---

## II. dbt 핵심 아키텍처 및 동작 원리

dbt의 핵심 철학은 변환(Transformation)은 [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 내부에서 SQL로다. [ELT](/studynote/14_data_engineering/01_infrastructure/034_elt/) (Extract, Load, Transform) 패턴에서 T(변환)만을 담당하며, E와 L은 Fivetran, Airbyte 등 별도 도구에 맡긴다.

```text
+----------------------------------------------------------+
|          dbt ELT 파이프라인 아키텍처                      |
+----------------------------------------------------------+
|                                                          |
|  소스 시스템       적재(Load)       변환(Transform)       |
|  +----------+   +----------+     +------------------+  |
|  | CRM DB   |-> | Fivetran |---> | dbt 모델 (SQL)   |  |
|  | ERP DB   |   | Airbyte  |     | staging/->marts/ |  |
|  | 이벤트로그|   | (Raw적재)|     | Jinja 매크로      |  |
|  +----------+   +----------+     +-------+----------+  |
|                                          |              |
|  +---------------------------------------v----------+   |
|  | DWH (Snowflake / BigQuery / Redshift)           |   |
|  | raw.* -> staging.* -> intermediate.* -> mart.*  |   |
|  +-------------------------------------------------+   |
|                                                          |
+----------------------------------------------------------+
```

dbt 모델 계층 구조:
- staging/: 원본 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 그대로 표준화만 (컬럼명 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/), 타입 캐스팅)
- intermediate/: 복잡한 조인 집계 중간 단계
- mart/: 분석가 BI가 바로 사용하는 최종 비즈니스 엔티티 (fact, dim)

dbt 테스트 유형:
- [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 테스트([Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) Test): not_null, unique, accepted_values, relationships - YAML로 선언
- [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 테스트([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Test): 커스텀 SQL로 비즈니스 규칙 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) (assert_total_revenue_positive.sql)
- 소스 신선도(Source Freshness): 소스 테이블이 정해진 주기 내 갱신됐는지 자동 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)

- **📢 섹션 요약 비유**: dbt 모델은 레시피 책과 같다. 재료(원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 손질(staging)하고, 조리(intermediate)하고, 플레이팅(mart)하는 각 단계가 SQL [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 분리돼 누구나 읽고 수정할 수 있다.

---

## III. 비교 및 연결

| 항목         | 전통 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)                    | [ELT](/studynote/14_data_engineering/01_infrastructure/034_elt/) (Spark 기반)          | dbt [ELT](/studynote/14_data_engineering/01_infrastructure/034_elt/)                    |
|:-----------|:----------------------------|:--------------------------|:---------------------------|
| 변환 위치    | [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 서버에서 사전 변환         | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅 클러스터에서      | [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 내부에서     |
| 주요 언어    | SQL + Python/Java (커스텀)   | [Spark SQL](/studynote/16_bigdata/03_spark/056_spark_sql/) / PySpark       | SQL + Jinja 템플릿          |
| [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리    | 없거나 산발적                 | Git (코드), [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 별도 관리 | Git 기반 완전 통합            |
| 테스트       | 없거나 수동                   | [단위 테스트](/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/) (선택)          | [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 테스트 내장       |
| 문서         | Wiki, 수동 유지               | 코드 주석                   | 자동 문서화 (lineage 포함)   |
| 학습 곡선    | 높음                         | 높음 (Spark)               | 낮음 (SQL 작성자도 접근 가능) |

[데이터 계약](/studynote/16_bigdata/12_trends/236_data_contract/)([Data Contract](/studynote/16_bigdata/12_trends/236_data_contract/))은 Protobuf나 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) Schema처럼 생산자와 소비자 간에 계약을 코드로 정의한다. 주요 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/): [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 필드 정의, [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/) (업데이트 주기, [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)), 의미론적 설명. 계약 위반은 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 자동으로 감지된다.

- **📢 섹션 요약 비유**: [데이터 계약](/studynote/16_bigdata/12_trends/236_data_contract/)은 공장(생산자)과 판매점(소비자) 사이의 납품 규격서다. A4 용지 500매, 무게 80g, 매주 월요일 납품처럼 명시해두면 한쪽이 변경해도 미리 경보가 울린다.

---

## [IV](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/). 실무 적용 및 기술사 판단

[DataOps](/studynote/12_it_management/05_security_compliance/965_dataops/) [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 설계 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/):

1. [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/): [PR](/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시 dbt run --[select](/studynote/05_database/04_transactions_concurrency/520_select/) [state](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/):modified+ 로 변경된 모델과 하위 의존 모델만 실행해 비용 절감
2. CD: Merge 후 자동으로 프로덕션 환경에 dbt run + dbt test 실행, 품질 게이트 통과 시만 배포
3. Slim [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/): dbt Cloud의 defer 기능으로 변경되지 않은 모델은 프로덕션 결과물을 재사용
4. 소스 신선도 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링: dbt source freshness를 [스케줄](/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/) 실행해 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 자동 감지
5. Great Expectations 통합: 복잡한 분포 기반 품질 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 dbt 테스트와 병행

```text
+--------------------------------------------------------+
|         DataOps CI/CD 파이프라인 흐름                  |
+--------------------------------------------------------+
|                                                        |
|  개발자 -> PR 생성                                      |
|      |                                                 |
|      v                                                 |
|  GitHub Actions / dbt Cloud CI                        |
|  +-- dbt run (변경 모델 + 하위 모델만)                   |
|  +-- dbt test (스키마, 데이터 테스트)                    |
|  +-- Great Expectations (분포 검증)                     |
|  +-- 데이터 계약 검증 (스키마 호환성)                     |
|      |                                                 |
|      +-- PASS -> 코드 리뷰 -> Merge -> CD 트리거        |
|      +-- FAIL -> PR 블록, 알림 전송                     |
|                                                        |
|  CD: Merge 후 자동 실행                                 |
|  +-- dbt run (영향받는 모델)                            |
|  +-- dbt test (품질 게이트)                             |
|  +-- 배포 완료 -> BI 도구, ML 파이프라인 자동 갱신        |
|                                                        |
+--------------------------------------------------------+
```

[안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/):
- 테스트 없는 dbt 모델: not_null, unique 테스트조차 없으면 [오류 탐지](/studynote/02_operating_system/01_overview_architecture/040_error_detection/) 불가
- 모든 모델 항상 전체 실행: PR마다 전체 실행하면 비용이 기하급수적으로 증가. Slim CI로 변경 모델만 실행
- [데이터 계약](/studynote/16_bigdata/12_trends/236_data_contract/) 무시: [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변경을 구두로 협의하면 하위 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 파악이 불가능해 다운스트림 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인이 무너짐

- **📢 섹션 요약 비유**: [DataOps](/studynote/12_it_management/05_security_compliance/965_dataops/) [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD는 식당 주방의 HACCP (Hazard Analysis Critical Control Points) 시스템 같다. 조리 단계마다 온도 위생을 자동으로 점검하고, 기준 미달이면 요리가 손님에게 나가지 않는다.

---

## V. 기대효과 및 결론

DataOps와 dbt를 도입하면 [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) 배포 리드타임이 수주에서 수시간으로 단축되고, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [결함](/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)이 프로덕션에 도달하기 전에 자동으로 차단된다. dbt의 Lineage [Graph](/studynote/12_it_management/03_ea_isp/888_graph/)(계보 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/))는 특정 모델의 변경이 어떤 대시보드 ML 모델에 영향을 미치는지 즉각 파악하게 해준다.

[데이터 계약](/studynote/16_bigdata/12_trends/236_data_contract/)은 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)된 팀 간의 명시적 합의를 코드로 관리함으로써 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 계약과 동일한 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)에 부여한다. 이는 [Data Mesh](/studynote/12_it_management/05_security_compliance/320_data_mesh/) 아키텍처에서 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀이 독립적으로 [데이터 제품](/studynote/16_bigdata/07_data_lake/154_data_product/)을 운영하는 환경에서 특히 중요하다.

결론적으로 DataOps는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 팀이 코드를 배포하는 방식에서 [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)이 소프트웨어처럼 관리되는 방식으로의 문화적 기술적 전환이다.

- **📢 섹션 요약 비유**: DataOps의 완성은 음식점 리뷰 시스템의 공개화와 같다. 주방([파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인)이 어떻게 운영되는지 손님([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소비자)이 투명하게 볼 수 있고, 위생 점검(품질 테스트) 결과가 실시간으로 공개돼 신뢰가 쌓인다.

---

### 📌 관련 개념 맵

| 개념                           | 연결 포인트                                             |
|:-----------------------------|:------------------------------------------------------|
| [ELT](/studynote/14_data_engineering/01_infrastructure/034_elt/) (Extract, Load, Transform) | dbt가 담당하는 T(변환) 단계, 웨어하우스 내부 처리         |
| [Data Lineage](/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/) ([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보)     | dbt [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) ([Directed Acyclic Graph](/studynote/06_ict_convergence/03_cloud_infrastructure/255_apache_airflow_dag/))로 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 변경 영향 파악 |
| [Data Contract](/studynote/16_bigdata/12_trends/236_data_contract/) ([데이터 계약](/studynote/16_bigdata/12_trends/236_data_contract/))   | 생산자-소비자 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/) 합의 코드화, [Data Mesh](/studynote/12_it_management/05_security_compliance/320_data_mesh/) 핵심 요소  |
| Great Expectations             | 분포 기반 복합 품질 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), dbt 테스트와 상호 보완           |
| [Data Mesh](/studynote/12_it_management/05_security_compliance/320_data_mesh/)                      | [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀 독립 [데이터 제품](/studynote/16_bigdata/07_data_lake/154_data_product/) 운영, DataOps를 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 단위로 확장 |

### 📈 관련 키워드 및 발전 흐름도

```text
전통 ETL (수동 배포, 품질 검증 부재)
    |
    v
ELT + 데이터 웨어하우스 (Snowflake, BigQuery 등장)
    |
    v
dbt 오픈소스 (SQL 기반 변환 모델화, 2016년)
    |
    v
DataOps 방법론 확산 (CI/CD, 자동 테스트, 2018~)
    |
    v
데이터 계약 (Data Contract, 스키마 합의 코드화)
    |
    v
Data Mesh (도메인 팀 분산 소유, DataOps 도메인 단위 적용)
```

### 👶 어린이를 위한 3줄 비유 설명

1. dbt는 요리 레시피 북이에요. 재료(원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 어떻게 손질하고 조리하는지 SQL로 적어두면, 컴퓨터가 자동으로 요리([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환)해줘요.
2. [DataOps](/studynote/12_it_management/05_security_compliance/965_dataops/) [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD는 요리가 끝날 때마다 맛 검사(테스트)를 자동으로 해줘서, 맛없는 요리(나쁜 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 손님(대시보드, ML 모델)에게 나가지 않게 막아줘요.
3. [데이터 계약](/studynote/16_bigdata/12_trends/236_data_contract/)은 주방과 홀 직원이 이 요리는 항상 이 모양, 이 크기로 나와야 해라고 약속하는 것처럼, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주는 쪽과 받는 쪽이 서로 규칙을 코드로 약속하는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 356 / 373

<- **이전**: [355. CXL 칩렛 메모리 풀 고성능 서버 아키텍처망 (CXL Chiplet Memory Pool)](/studynote/15_devops_sre/05_devsecops/355_architecture/)
**다음**: [357. OOM Killed 커널 자원 제한 종료 방어망 (OOM Killer Kubernetes QoS cgroup Memory Limits)](/studynote/15_devops_sre/05_devsecops/357_oom_killed/) ->

---
