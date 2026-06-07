---
title: "Databricks Platform"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 158
---
## 핵심 인사이트 (3줄 요약)
1. Databricks는 [Apache Spark](/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) 창시자들이 설립한 회사로, [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/)·[Unity Catalog](/studynote/16_bigdata/07_data_lake/150_unity_catalog/)·[MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/)·Photon 엔진을 통합한 <strong><a href="/studynote/16_bigdata/07_data_lake/146_lakehouse/">레이크하우스</a> 올인원 플랫폼</strong>을 제공하며 컴퓨팅 네이티브(Compute-Native) 아키텍처로 차별화된다.
2. <strong><a href="/studynote/16_bigdata/03_spark/074_photon_engine/">Photon 엔진</a></strong>은 C++ 기반 벡터화 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 엔진으로 기존 Spark 대비 SQL 워크로드에서 최대 8배 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 달성하며, <strong><a href="/studynote/13_cloud_architecture/01_virtualization/030_auto_scaling/">Auto Scaling</a></strong> 클러스터가 워크로드에 따라 노드를 자동으로 조정한다.
3. AWS·Azure·GCP 모두에서 동일한 API로 동작하는 [멀티 클라우드 전략](/studynote/06_ict_convergence/03_cloud_infrastructure/189_multi_cloud_strategy_vendor_lock_in/)과, SQL 친화적 Snowflake와 코드 친화적 Databricks의 포지셔닝 차별화가 핵심 시장 대립 구도를 형성한다.

---

## Ⅰ. 개요 및 필요성

Apache Spark는 뛰어난 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에도 불구하고 클러스터 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/), [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/), ML 실험 관리, [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)를 모두 직접 구성해야 하는 운영 복잡성이 있었다. Databricks는 이 모든 요소를 통합 플랫폼으로 제공하여, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자·BI 분석가가 하나의 환경에서 협업할 수 있게 한다.

[Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) [Lakehouse](/studynote/16_bigdata/07_data_lake/146_lakehouse/) Platform은 [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/)(저장), [Unity Catalog](/studynote/16_bigdata/07_data_lake/150_unity_catalog/)(거버넌스), [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/)(ML 수명 주기), Workflows([오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)), SQL Analytics(BI)를 단일 통합 환경으로 제공한다.

| 이전 환경 ([분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 도구) | [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) 통합 |
|:---|:---|
| [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) + Spark 자체 클러스터 | 관리형 Spark 클러스터 |
| [Hive](/studynote/05_database/04_transactions_concurrency/544_hive/) + 별도 [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) | [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/) 단일 스토리지 |
| 개별 ML 도구 (Jupyter 등) | [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/) + [Feature Store](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) |
| 별도 오케스트레이터 (Airflow) | [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) Workflows |
| 별도 BI 도구 연결 | [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) SQL + [Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) |

> 📢 **섹션 요약 비유**: Databricks는 스위스 아미 나이프다. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리(Spark), ML 실험([MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/)), SQL 분석([Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) SQL), 거버넌스([Unity Catalog](/studynote/16_bigdata/07_data_lake/150_unity_catalog/))가 하나의 손잡이에 모두 달려 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+------------------------------------------------------------------+
|               Databricks Lakehouse Platform                       |
+------------------------------------------------------------------+
|                                                                  |
|  +---------------------------------------------------------+    |
|  |              사용자 인터페이스 레이어                      |    |
|  |  Notebooks | Databricks SQL | ML Experiments | Workflows |    |
|  +---------------------------------------------------------+    |
|                                                                  |
|  +---------------------------------------------------------+    |
|  |              컴퓨팅 레이어                                |    |
|  |  +--------------+  +--------------+  +--------------+   |    |
|  |  | All-Purpose  |  | Job Cluster  |  |  SQL          |   |    |
|  |  | Cluster      |  |  (배치 전용) |  |  Warehouse   |   |    |
|  |  | (개발/탐색)   |  |              |  |  (BI 전용)   |   |    |
|  |  +--------------+  +--------------+  +--------------+   |    |
|  |           Apache Spark + Photon Engine (C++ 벡터화)      |    |
|  +---------------------------------------------------------+    |
|                                                                  |
|  +---------------------------------------------------------+    |
|  |              데이터/ML 레이어                              |    |
|  |  Delta Lake | Unity Catalog | MLflow | Feature Store     |    |
|  +---------------------------------------------------------+    |
|                                                                  |
|  +---------------------------------------------------------+    |
|  |              클라우드 스토리지 레이어                      |    |
|  |   AWS S3  |  Azure ADLS Gen2  |  Google Cloud Storage    |    |
|  +---------------------------------------------------------+    |
+------------------------------------------------------------------+
```

**핵심 제품·기능 상세**

| 제품/기능 | 역할 | 핵심 특징 |
|:---|:---|:---|
| [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/) | 저장 포맷 | ACID, 타임 트래블, Z-ORDER |
| [Unity Catalog](/studynote/16_bigdata/07_data_lake/150_unity_catalog/) | 거버넌스 | 3계층 [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/), [Fine-Grained](/studynote/01_computer_architecture/11_multicore_synchronization/399_fine_grained_multithreading/) [AC](/studynote/12_it_management/04_sdlc_testing/155_ac_actual_cost/) |
| [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/) | ML 수명 주기 | 실험 추적, [모델 레지스트리](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/), 서빙 |
| [Photon 엔진](/studynote/16_bigdata/03_spark/074_photon_engine/) | [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | C++ 벡터화, SQL 최대 8배 가속 |
| [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) SQL | BI [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) SQL 웨어하우스 |
| Workflows | [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) | [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) 기반 작업 의존성 관리 |
| [AutoML](/studynote/14_data_engineering/04_mlops/176_automl_hyperparameter_optimization_bayesian/) | ML 자동화 | 자동 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 엔지니어링·하이퍼파라미터 |
| Delta Live Tables | [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 | 선언적 스트리밍·배치 통합 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 |

> 📢 **섹션 요약 비유**: Photon 엔진은 자동차의 터보 엔진이다. 같은 도로([쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/))를 달려도 기존 Spark(일반 엔진)보다 훨씬 빠르게 목적지(결과)에 도달한다.

---

## Ⅲ. 비교 및 연결

<strong><a href="/studynote/16_bigdata/12_trends/240_databricks_vs_snowflake_dw/">Databricks vs Snowflake</a> — 핵심 대립 구도</strong>

| 항목 | [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) | [Snowflake](/studynote/05_database/04_transactions_concurrency/541_cassandra/) |
|:---|:---|:---|
| 핵심 포지셔닝 | 코드 네이티브 (Python/Spark 중심) | SQL 네이티브 (ANSI SQL 중심) |
| ML/[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 지원 | 최고 수준 ([MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/), [AutoML](/studynote/14_data_engineering/04_mlops/176_automl_hyperparameter_optimization_bayesian/) 내장) | Snowpark ML (2023~) |
| 스토리지 방식 | 오픈 포맷 (Delta/Iceberg on 객체 스토리지) | 독점 스토리지 포맷 |
| 스트리밍 | [Spark Structured Streaming](/studynote/16_bigdata/03_spark/061_structured_streaming/) + [DLT](/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/) | Snowpipe (마이크로 배치) |
| 가격 모델 | DBU ([Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) Unit) 기반 | Credit 기반 |
| 주 사용자 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어, ML 엔지니어 | SQL 분석가, BI 개발자 |
| 벤더 독립성 | 오픈 포맷 (Delta/Iceberg) | 높은 [벤더 종속](/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/)성 |

**연관 기술 연결**

- <strong><a href="/studynote/10_ai/02_dl_architecture_new/180_mlflow/">MLflow</a></strong>: Databricks에서 인큐베이션, 현재 LF [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)&[Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재단 기증
- <strong><a href="/studynote/16_bigdata/07_data_lake/147_delta_lake/">Delta Lake</a></strong>: Linux Foundation 기증, 벤더 중립화
- <strong><a href="/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/">Apache Spark</a></strong>: [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) 창업자들이 [UC](/studynote/12_it_management/02_itsm_itil/871_underpinning_contract/) Berkeley AMPLab에서 개발

> 📢 **섹션 요약 비유**: Databricks는 종합 연구소([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리+ML+SQL 올인원)이고, Snowflake는 최고급 SQL 레스토랑(SQL에 특화)이다. 요리사([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어)에게는 연구소가, 식품 분석가(BI 분석가)에게는 레스토랑이 더 편하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**클러스터 유형별 최적 사용 시나리오**

| 클러스터 유형 | 특징 | 사용 시나리오 |
|:---|:---|:---|
| All-Purpose Cluster | 상시 실행, 협업 | 탐색적 분석, 개발·디버깅 |
| Job Cluster | 작업 시작 시 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 완료 후 종료 | 운영 배치 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 |
| SQL Warehouse | [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) SQL 최적화 | BI 도구 연결, SQL 분석 |
| Instance Pools | 미리 워밍업된 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) | 빠른 클러스터 시작 필요 시 |

**기술사 답안 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) 핵심 제품 구성 | [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/) + [Unity Catalog](/studynote/16_bigdata/07_data_lake/150_unity_catalog/) + [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/) + Photon + Workflows |
| [Photon 엔진](/studynote/16_bigdata/03_spark/074_photon_engine/) 원리 | C++ 기반 벡터화 실행, JVM 오버헤드 제거, [SIMD](/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/) 활용 |
| [Databricks vs Snowflake](/studynote/16_bigdata/12_trends/240_databricks_vs_snowflake_dw/) | [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) = 코드 네이티브/ML, [Snowflake](/studynote/05_database/04_transactions_concurrency/541_cassandra/) = SQL 네이티브/BI |
| DBU([Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) Unit) | 클러스터 유형·크기에 따른 가격 단위, 시간당 소비량 |

> 📢 **섹션 요약 비유**: [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) 선택은 팀 구성에 따라 달라진다. Python/ML 중심 팀이라면 Databricks가 고향이고, SQL BI 중심 팀이라면 Snowflake가 더 자연스럽다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 통합 플랫폼 효율 | 여러 도구 연동 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 제거, 단일 보안·거버넌스 |
| ML 가속 | [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/)·Feature Store로 ML 실험->배포 사이클 단축 |
| 비용 최적화 | [Auto Scaling](/studynote/13_cloud_architecture/01_virtualization/030_auto_scaling/) + Spot 인스턴스 + 작업 완료 종료 |
| 오픈 포맷 | Delta/Iceberg로 [벤더 종속](/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/) 최소화 |

Databricks는 2023년 기준 기업 가치 430억 달러로 평가되며, 2024년 IPO를 준비 중인 빅데이터 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 플랫폼의 선두 기업이다. [레이크하우스](/studynote/16_bigdata/07_data_lake/146_lakehouse/) 아키텍처의 레퍼런스 구현체로서 기업 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼 표준에 가장 가까이 있다. 기술사 시험에서는 <strong><a href="/studynote/16_bigdata/03_spark/074_photon_engine/">Databricks</a> 핵심 제품 구성</strong>, <strong><a href="/studynote/16_bigdata/03_spark/074_photon_engine/">Photon 엔진</a> 특성</strong>, <strong>Snowflake와의 포지셔닝 비교</strong>가 핵심 논점이다.

> 📢 **섹션 요약 비유**: Databricks는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 팀의 슈퍼 앱이다. 한 앱에서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집·처리·ML·분석·[시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)를 모두 처리하듯, 하나의 플랫폼에서 [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)부터 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델 배포까지 완결된다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/) | 저장 레이어 | [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) 핵심 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 기여 |
| [Unity Catalog](/studynote/16_bigdata/07_data_lake/150_unity_catalog/) | 거버넌스 레이어 | 3계층 [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/), 리니지 |
| [MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/) | ML 수명 주기 | 실험·[레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)·서빙 통합 |
| [Photon 엔진](/studynote/16_bigdata/03_spark/074_photon_engine/) | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 가속 | C++ 벡터화, SQL 8배 향상 |
| DBU | 가격 단위 | 클러스터 유형별 시간당 단가 |
| [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) SQL | BI 레이어 | [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) SQL 웨어하우스 |

---


### 📈 관련 키워드 및 발전 흐름도

```text
[Apache Spark — 인메모리 분산 처리 엔진, 배치·스트림 통합]
    |
    v
[Databricks (Managed Spark) — Spark 완전 관리형 클라우드 플랫폼, 자동 최적화]
    |
    v
[Delta Lake — ACID 트랜잭션·스키마 진화·타임 트래블 지원 오픈 테이블 포맷]
    |
    v
[레이크하우스 (Lakehouse) — 데이터 레이크의 유연성 + 데이터 웨어하우스의 ACID·성능 통합]
    |
    v
[Unity Catalog + MLflow — 데이터·모델 거버넌스 통합, 엔드투엔드 AI/ML 파이프라인]
```
이 흐름은 순수 Spark 엔진이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 보장의 한계를 드러내자 Delta Lake의 ACID가 이를 보완하고, [레이크하우스](/studynote/16_bigdata/07_data_lake/146_lakehouse/) 아키텍처와 통합 거버넌스로 발전하는 [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/) 플랫폼의 진화 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. Databricks는 모든 도구가 한 건물에 있는 연구소예요. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집, 분석, [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 훈련을 한 곳에서 다 할 수 있어요.
2. Photon 엔진은 자동차 터보 장치처럼, 같은 일을 훨씬 빠르게 해주는 특별 엔진이에요.
3. Spark 만든 사람들이 세운 회사라 마치 요리사가 직접 차린 레스토랑처럼, 도구와 플랫폼이 딱 맞게 설계되어 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 158 / 262

<- **이전**: [157. 클라우드 빅데이터 분석 서비스 — Amazon EMR/Azure HDInsight/GCP Dataproc](/studynote/16_bigdata/07_data_lake/157_data_analysis_services/)
**다음**: [159. Snowflake on Data Lake — External Table과 Iceberg 지원](/studynote/16_bigdata/07_data_lake/159_snowflake_data_lake/) ->

---
