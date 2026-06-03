---
title: 356. 데이터옵스 CI/CD dbt 분석 파이프 자동망 (DataOps CI/CD with dbt)
date: '2026-05-09'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DataOps는 DevOps의 원칙(자동화, 협업, 빠른 피드백)을 [[645_data_pipeline_acceleration|데이터 파이프라인]]에 적용해 분석 [[001_dikw_pyramid|데이터]]의 품질 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 배포 속도를 높이는 방법론이다.
> 2. **핵심 도구**: dbt ([[001_dikw_pyramid|data]] build tool)는 SQL [[520_select|SELECT]] 문을 변환 모델(Transformation Model)로 다루어, [[288_version_ihl_tos_total_length|버전]] 관리 테스트 문서화 의존성 [[070_graph_datastructure|그래프]]를 [[001_dikw_pyramid|데이터]] 변환에 제공하는 [[191_oss_license_compliance|오픈소스]] 프레임워크다.
> 3. **품질 게이트**: [[236_data_contract|데이터 계약]]([[236_data_contract|Data Contract]])은 생산자와 소비자 간의 [[005_schema|스키마]] [[085_sla|SLA]] ([[085_sla|Service Level Agreement]]) 의미론적 합의를 코드로 명문화해 [[123_pipe|파이프]]라인 하위 [[344_compatibility_usability|호환성]]을 보장하는 핵심 메커니즘이다.

---

## I. 개요 및 필요성

[[645_data_pipeline_acceleration|데이터 파이프라인]]은 전통적으로 소수의 [[001_dikw_pyramid|데이터]] 엔지니어가 수동으로 배포하고, 변경 이력 관리가 부실하며, 테스트가 없거나 프로덕션 직접 [[395_verification_process_review|검증]]에 의존했다. 분석 팀이 늘어나고 [[001_dikw_pyramid|데이터]] 소비자(ML 모델, 대시보드, 리포트)가 다양해질수록 이 방식은 더 이상 지속 불가능하다.

DataOps는 다음 세 가지 문제를 해결한다.

1. **느린 배포 사이클**: [[330_code_review|코드 리뷰]] 없이 [[215_etl_vs_elt_pipeline|ETL]] 스크립트를 수동으로 배포하면 변경이 한 달에 수회에 불과하다. [[090_configuration_item|CI]]/CD 자동화로 하루 수십 회 배포를 목표로 한다.
2. **품질 불투명**: [[001_dikw_pyramid|데이터]] [[352_defect_definition|결함]]이 다운스트림 대시보드 ML 모델 오염으로 연쇄되기 전까지 인지하지 못하는 구조를 자동 품질 [[395_verification_process_review|검증]]으로 사전 차단한다.
3. **협업 단절**: [[001_dikw_pyramid|데이터]] 엔지니어 분석가 [[001_dikw_pyramid|데이터]] 사이언티스트가 서로 다른 도구와 프로세스로 작업해 [[002_silo_hyeonhyung|사일로]]가 형성된다.

dbt는 분석가가 친숙한 SQL로 변환 로직을 작성하면서 소프트웨어 엔지니어링의 모범 사례([[288_version_ihl_tos_total_length|버전]] 관리, 테스트, 문서)를 적용할 수 있게 해준다.

- **📢 섹션 요약 비유**: DataOps는 [[645_data_pipeline_acceleration|데이터 파이프라인]]에 교통 [[130_signal|신호]]등을 설치하는 것이다. 기존에는 [[001_dikw_pyramid|데이터]]가 빨간불을 무시하고 달리다 사고([[001_dikw_pyramid|데이터]] 품질 문제)가 나도 몰랐지만, 이제는 [[130_signal|신호]]등([[090_configuration_item|CI]]/CD, 품질 검사)이 자동으로 통제한다.

---

## II. dbt 핵심 아키텍처 및 동작 원리

dbt의 핵심 철학은 변환(Transformation)은 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] 내부에서 SQL로다. [[034_elt|ELT]] (Extract, Load, Transform) 패턴에서 T(변환)만을 담당하며, E와 L은 Fivetran, Airbyte 등 별도 도구에 맡긴다.

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
- staging/: 원본 [[001_dikw_pyramid|데이터]]를 그대로 표준화만 (컬럼명 [[093_normalization|정규화]], 타입 캐스팅)
- intermediate/: 복잡한 조인 집계 중간 단계
- mart/: 분석가 BI가 바로 사용하는 최종 비즈니스 엔티티 (fact, dim)

dbt 테스트 유형:
- [[005_schema|스키마]] 테스트([[505_schema|Schema]] Test): not_null, unique, accepted_values, relationships - YAML로 선언
- [[001_dikw_pyramid|데이터]] 테스트([[001_dikw_pyramid|Data]] Test): 커스텀 SQL로 비즈니스 규칙 [[395_verification_process_review|검증]] (assert_total_revenue_positive.sql)
- 소스 신선도(Source Freshness): 소스 테이블이 정해진 주기 내 갱신됐는지 자동 [[396_validation|확인]]

- **📢 섹션 요약 비유**: dbt 모델은 레시피 책과 같다. 재료(원시 [[001_dikw_pyramid|데이터]])를 손질(staging)하고, 조리(intermediate)하고, 플레이팅(mart)하는 각 단계가 SQL [[501_file_definition_logical_record|파일]]로 분리돼 누구나 읽고 수정할 수 있다.

---

## III. 비교 및 연결

| 항목         | 전통 [[215_etl_vs_elt_pipeline|ETL]]                    | [[034_elt|ELT]] (Spark 기반)          | dbt [[034_elt|ELT]]                    |
|:-----------|:----------------------------|:--------------------------|:---------------------------|
| 변환 위치    | [[215_etl_vs_elt_pipeline|ETL]] 서버에서 사전 변환         | [[136_variance|분산]] 컴퓨팅 클러스터에서      | [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] 내부에서     |
| 주요 언어    | SQL + Python/Java (커스텀)   | [[056_spark_sql|Spark SQL]] / PySpark       | SQL + Jinja 템플릿          |
| [[288_version_ihl_tos_total_length|버전]] 관리    | 없거나 산발적                 | Git (코드), [[005_schema|스키마]] 별도 관리 | Git 기반 완전 통합            |
| 테스트       | 없거나 수동                   | [[397_unit_test|단위 테스트]] (선택)          | [[005_schema|스키마]] [[001_dikw_pyramid|데이터]] 테스트 내장       |
| 문서         | Wiki, 수동 유지               | 코드 주석                   | 자동 문서화 (lineage 포함)   |
| 학습 곡선    | 높음                         | 높음 (Spark)               | 낮음 (SQL 작성자도 접근 가능) |

[[236_data_contract|데이터 계약]]([[236_data_contract|Data Contract]])은 Protobuf나 [[343_json|JSON]] Schema처럼 생산자와 소비자 간에 계약을 코드로 정의한다. 주요 [[082_attribute_types_er_model|속성]]: [[005_schema|스키마]] [[288_version_ihl_tos_total_length|버전]], 필드 정의, [[085_sla|SLA]] (업데이트 주기, [[452_availability|가용성]]), 의미론적 설명. 계약 위반은 [[090_configuration_item|CI]] [[123_pipe|파이프]]라인에서 자동으로 감지된다.

- **📢 섹션 요약 비유**: [[236_data_contract|데이터 계약]]은 공장(생산자)과 판매점(소비자) 사이의 납품 규격서다. A4 용지 500매, 무게 80g, 매주 월요일 납품처럼 명시해두면 한쪽이 변경해도 미리 경보가 울린다.

---

## [[288_version_ihl_tos_total_length|IV]]. 실무 적용 및 기술사 판단

[[324_dataops|DataOps]] [[090_configuration_item|CI]]/CD [[123_pipe|파이프]]라인 설계 [[435_checklist_based_testing|체크리스트]]:

1. [[090_configuration_item|CI]]: [[067_pull_request_pr_merge_request_code_review|PR]] [[087_process_state_transition|생성]] 시 dbt run --[[520_select|select]] [[272_state_pattern|state]]:modified+ 로 변경된 모델과 하위 의존 모델만 실행해 비용 절감
2. CD: Merge 후 자동으로 프로덕션 환경에 dbt run + dbt test 실행, 품질 게이트 통과 시만 배포
3. Slim [[090_configuration_item|CI]]: dbt Cloud의 defer 기능으로 변경되지 않은 모델은 프로덕션 결과물을 재사용
4. 소스 신선도 [[229_monitor|모니터]]링: dbt source freshness를 [[208_schedule_history_transaction_execution_order|스케줄]] 실행해 [[001_dikw_pyramid|데이터]] [[015_지연_데이터_관점|지연]] 자동 감지
5. Great Expectations 통합: 복잡한 분포 기반 품질 [[395_verification_process_review|검증]]을 dbt 테스트와 병행

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

[[128_water_scrum_fall_anti_pattern|안티패턴]]:
- 테스트 없는 dbt 모델: not_null, unique 테스트조차 없으면 [[040_error_detection|오류 탐지]] 불가
- 모든 모델 항상 전체 실행: PR마다 전체 실행하면 비용이 기하급수적으로 증가. Slim CI로 변경 모델만 실행
- [[236_data_contract|데이터 계약]] 무시: [[005_schema|스키마]] 변경을 구두로 협의하면 하위 [[344_compatibility_usability|호환성]] 파악이 불가능해 다운스트림 [[123_pipe|파이프]]라인이 무너짐

- **📢 섹션 요약 비유**: [[324_dataops|DataOps]] [[090_configuration_item|CI]]/CD는 식당 주방의 HACCP (Hazard Analysis Critical Control Points) 시스템 같다. 조리 단계마다 온도 위생을 자동으로 점검하고, 기준 미달이면 요리가 손님에게 나가지 않는다.

---

## V. 기대효과 및 결론

DataOps와 dbt를 도입하면 [[645_data_pipeline_acceleration|데이터 파이프라인]] 배포 리드타임이 수주에서 수시간으로 단축되고, [[001_dikw_pyramid|데이터]] [[352_defect_definition|결함]]이 프로덕션에 도달하기 전에 자동으로 차단된다. dbt의 Lineage [[104_graph|Graph]](계보 [[070_graph_datastructure|그래프]])는 특정 모델의 변경이 어떤 대시보드 ML 모델에 영향을 미치는지 즉각 파악하게 해준다.

[[236_data_contract|데이터 계약]]은 [[136_variance|분산]]된 팀 간의 명시적 합의를 코드로 관리함으로써 [[532_microservices_decomposition_patterns|마이크로서비스]] [[014_api_posix|API]] 계약과 동일한 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]을 [[645_data_pipeline_acceleration|데이터 파이프라인]]에 부여한다. 이는 [[320_data_mesh|Data Mesh]] 아키텍처에서 [[064_relation_domain|도메인]] 팀이 독립적으로 [[154_data_product|데이터 제품]]을 운영하는 환경에서 특히 중요하다.

결론적으로 DataOps는 [[001_dikw_pyramid|데이터]] 팀이 코드를 배포하는 방식에서 [[645_data_pipeline_acceleration|데이터 파이프라인]]이 소프트웨어처럼 관리되는 방식으로의 문화적 기술적 전환이다.

- **📢 섹션 요약 비유**: DataOps의 완성은 음식점 리뷰 시스템의 공개화와 같다. 주방([[123_pipe|파이프]]라인)이 어떻게 운영되는지 손님([[001_dikw_pyramid|데이터]] 소비자)이 투명하게 볼 수 있고, 위생 점검(품질 테스트) 결과가 실시간으로 공개돼 신뢰가 쌓인다.

---

### 📌 관련 개념 맵

| 개념                           | 연결 포인트                                             |
|:-----------------------------|:------------------------------------------------------|
| [[034_elt|ELT]] (Extract, Load, Transform) | dbt가 담당하는 T(변환) 단계, 웨어하우스 내부 처리         |
| [[214_data_lineage_tracking|Data Lineage]] ([[001_dikw_pyramid|데이터]] 계보)     | dbt [[401_bayesian_network_dag_causality|DAG]] ([[255_apache_airflow_dag|Directed Acyclic Graph]])로 자동 [[087_process_state_transition|생성]], 변경 영향 파악 |
| [[236_data_contract|Data Contract]] ([[236_data_contract|데이터 계약]])   | 생산자-소비자 [[005_schema|스키마]] [[085_sla|SLA]] 합의 코드화, [[320_data_mesh|Data Mesh]] 핵심 요소  |
| Great Expectations             | 분포 기반 복합 품질 [[395_verification_process_review|검증]], dbt 테스트와 상호 보완           |
| [[320_data_mesh|Data Mesh]]                      | [[064_relation_domain|도메인]] 팀 독립 [[154_data_product|데이터 제품]] 운영, DataOps를 [[064_relation_domain|도메인]] 단위로 확장 |

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

1. dbt는 요리 레시피 북이에요. 재료(원시 [[001_dikw_pyramid|데이터]])를 어떻게 손질하고 조리하는지 SQL로 적어두면, 컴퓨터가 자동으로 요리([[001_dikw_pyramid|데이터]] 변환)해줘요.
2. [[324_dataops|DataOps]] [[090_configuration_item|CI]]/CD는 요리가 끝날 때마다 맛 검사(테스트)를 자동으로 해줘서, 맛없는 요리(나쁜 [[001_dikw_pyramid|데이터]])가 손님(대시보드, ML 모델)에게 나가지 않게 막아줘요.
3. [[236_data_contract|데이터 계약]]은 주방과 홀 직원이 이 요리는 항상 이 모양, 이 크기로 나와야 해라고 약속하는 것처럼, [[001_dikw_pyramid|데이터]]를 주는 쪽과 받는 쪽이 서로 규칙을 코드로 약속하는 거예요.
