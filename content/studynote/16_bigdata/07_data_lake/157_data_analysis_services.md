---
title: "Data Analysis Services"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 157
---
## 핵심 인사이트 (3줄 요약)
1. 클라우드 관리형 빅데이터 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(Amazon EMR, Azure HDInsight, GCP Dataproc)는 [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)/Spark 클러스터를 수 분 내에 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/)하고, 운영 완료 후 즉시 종료하여 <strong>사용한 시간만큼만 비용을 지불</strong>하는 탄력적 컴퓨팅을 제공한다.
2. 세 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 모두 <strong>컴퓨팅과 스토리지를 분리(Decoupled <a href="/studynote/12_it_management/05_security_compliance/319_architecture/">Architecture</a>)</strong>하여 S3/ADLS/GCS에 저장된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 여러 클러스터가 독립적으로 처리할 수 있어 [레이크하우스](/studynote/16_bigdata/07_data_lake/146_lakehouse/) 아키텍처와 자연스럽게 통합된다.
3. 클러스터 시작 시간(수 분), 생태계 통합 깊이, 비용 모델(EC2 vs SKU)이 세 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 핵심 차별 요소이며, [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 옵션(EMR [Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/), Dataproc [Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/))이 운영 오버헤드를 더욱 낮추고 있다.

---

## Ⅰ. 개요 및 필요성

자체 관리 [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 클러스터는 하드웨어 구매, 클러스터 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/), 보안 패치, 용량 계획 등 막대한 운영 오버헤드가 따른다. 분석 워크로드는 주기적이거나 일회성인 경우가 많아 항상 켜 있는 클러스터가 비효율적이다.

클라우드 관리형 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 클릭 또는 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출로 클러스터를 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고, 작업 완료 후 삭제하는 탄력적 운영을 가능하게 한다. 2024년 현재는 [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 옵션이 등장하여 클러스터 관리 자체를 클라우드에 위임하는 방향으로 진화하고 있다.

| [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 클라우드 | 기반 기술 | 출시 |
|:---|:---|:---|:---|
| Amazon EMR (Elastic [MapReduce](/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)) | AWS | [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)/Spark/[Hive](/studynote/05_database/04_transactions_concurrency/544_hive/)/Presto | 2009 |
| Azure HDInsight | Microsoft Azure | [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)/Spark/[Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)/[HBase](/studynote/05_database/04_transactions_concurrency/543_hbase/) | 2014 |
| GCP Dataproc | Google Cloud | [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)/Spark | 2015 |

> 📢 **섹션 요약 비유**: 관리형 빅데이터 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 렌터카와 같다. 내 차(자체 클러스터)를 유지 관리하는 대신, 필요할 때 렌트(클러스터 시작)하고 반납(종료)하면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+------------------------------------------------------------------+
|          클라우드 관리형 빅데이터 서비스 아키텍처                  |
+------------------------------------------------------------------+
|                                                                  |
|  +----------------------------------------------------------+   |
|  |  객체 스토리지 (영구 저장)                                  |   |
|  |  AWS S3  /  Azure ADLS Gen2  /  GCS                      |   |
|  |  (Delta Lake / Iceberg / Parquet 파일)                    |   |
|  +------------------------+---------------------------------+   |
|                           | 읽기/쓰기 (HDFS 커넥터)              |
|  +------------------------v---------------------------------+   |
|  |  클러스터 (임시, 작업 중만 실행)                             |   |
|  |                                                          |   |
|  |  Amazon EMR          Azure HDInsight    GCP Dataproc     |   |
|  |  +-------------+    +---------------+  +-------------+  |   |
|  |  | Master Node |    | Head Node     |  | Master Node |  |   |
|  |  | Core Nodes  |    | Worker Nodes  |  | Worker Node |  |   |
|  |  | Task Nodes  |    | (auto-scale)  |  | (Preemptible|  |   |
|  |  | (Spot 가능) |    |               |  |  VM 가능)   |  |   |
|  |  +-------------+    +---------------+  +-------------+  |   |
|  +----------------------------------------------------------+   |
|                           |                                     |
|  +------------------------v---------------------------------+   |
|  |  주변 서비스 연동                                           |   |
|  |  EMR: Glue/Athena/SageMaker  |  Dataproc: BigQuery/Vertex|   |
|  |  HDInsight: Synapse/ML Studio|                            |   |
|  +----------------------------------------------------------+   |
+------------------------------------------------------------------+
```

<strong>3대 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 상세 비교</strong>

| 항목 | Amazon EMR | Azure HDInsight | GCP Dataproc |
|:---|:---|:---|:---|
| 클러스터 시작 시간 | 5~10분 | 15~20분 | 90초~2분 |
| 스팟/저비용 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) | EC2 [Spot Instance](/studynote/06_ict_convergence/03_cloud_infrastructure/209_spot_instance_cloud_cost_optimization/) | Azure Spot [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) | Preemptible [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) |
| [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 옵션 | EMR [Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) | 제한적 | Dataproc [Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) |
| 기본 스토리지 | Amazon S3 | Azure ADLS Gen2 | Google Cloud Storage |
| [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 지원 | EMR on EKS | AKS 통합 | Dataproc on GKE |
| ML 통합 | SageMaker | Azure ML Studio | Vertex [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) |
| Spark [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 업그레이드 | [AMI](/studynote/06_ict_convergence/02_iot_mobility/162_ami_advanced_metering_infrastructure/) 교체 | 클러스터 재생성 | 즉시 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 선택 |

> 📢 **섹션 요약 비유**: EMR은 대형 마트(AWS 풀 [에코](/studynote/03_network/01_data_communication/031_에코_반향/)시스템), HDInsight는 Office Suite(Microsoft 생태계 통합), Dataproc는 스포츠카(빠른 시작, [BigQuery](/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) 통합)에 비유할 수 있다.

---

## Ⅲ. 비교 및 연결

<strong>자체 관리 클러스터 vs 관리형 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> vs <a href="/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/">서버리스</a></strong>

| 항목 | 자체 [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) | 관리형 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) (EMR/Dataproc) |
|:---|:---|:---|:---|
| [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/) 시간 | 수 시간~수 일 | 2~20분 | 수 초 (자동) |
| 운영 오버헤드 | 매우 높음 | 보통 | 없음 |
| 비용 최적화 | 어려움 | Spot 인스턴스 활용 | 사용량 기반 완전 종량 |
| 적합 워크로드 | 상시 대용량 | 정기 배치, 중간 규모 | 간헐적 소규모~대규모 |

<strong><a href="/studynote/16_bigdata/07_data_lake/146_lakehouse/">레이크하우스</a> 통합 패턴</strong>

- <strong>EMR + S3 + <a href="/studynote/16_bigdata/07_data_lake/147_delta_lake/">Delta Lake</a></strong>: EMR 클러스터에서 [Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/) 테이블 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)
- **Dataproc + GCS + Iceberg**: Spark on Dataproc으로 Iceberg 테이블 처리
- **HDInsight + ADLS Gen2 + Hudi**: HDInsight Spark로 [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) upsert

> 📢 **섹션 요약 비유**: 세 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 선택은 이사업체 선택과 같다. 짐의 양([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 규모), 이사 빈도(워크로드 패턴), 이미 살고 있는 동네(클라우드 생태계)에 따라 최적 업체가 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong>비용 최적화 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>

| [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 설명 | 절감 효과 |
|:---|:---|:---|
| Spot/Preemptible [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) | [Task](/studynote/02_operating_system/02_process_thread/150_task/) Node에 스팟 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 사용 | 60~80% 비용 절감 |
| 작업 완료 후 즉시 종료 | 클러스터를 ephemeral하게 운영 | 유휴 시간 비용 제거 |
| 스토리지-컴퓨팅 분리 | S3/GCS를 외부 스토리지로 | 클러스터 종료 시에도 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보존 |
| [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 전환 | 소규모 간헐적 작업에 [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) | [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/) 비용 제거 |

**기술사 답안 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| 3대 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 비교 | 시작 시간 (Dataproc 최단), 생태계 (AWS/Azure/GCP), [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 지원 |
| 컴퓨팅-스토리지 분리 이유 | 클러스터 종료 후에도 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보존, 여러 클러스터가 동일 [데이터 공유](/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/) |
| Spot [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 사용 한계 | 중단 가능(중요 워크로드 부적합), Checkpoint 설계 필요 |
| [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 전환 시점 | 간헐적 소규모 작업, 클러스터 관리 오버헤드 제거 시 |

> 📢 **섹션 요약 비유**: Spot 인스턴스 사용은 빈 좌석 할인 비행기를 타는 것이다. 저렴하지만 갑자기 취소될 수 있으므로, 중요한 약속(크리티컬 작업)에는 정규 좌석(온디맨드)이 필요하다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 인프라 운영 비용 절감 | 클러스터 관리 인력 불필요, 보안 패치 자동화 |
| 탄력적 확장 | 워크로드 크기에 따라 수 분 내 클러스터 규모 조정 |
| 최신 기술 즉시 활용 | Spark [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 업그레이드가 클러스터 교체로 즉시 가능 |
| 비용 투명성 | 사용 시간·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 기반 정확한 비용 집계 |

클라우드 관리형 빅데이터 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 자체 [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 클러스터의 운영 부담을 제거하고, [레이크하우스](/studynote/16_bigdata/07_data_lake/146_lakehouse/) 아키텍처의 컴퓨팅 레이어를 탄력적으로 제공한다. [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 방향으로의 진화가 가속화되면서 2025년 이후 간헐적 배치 작업은 대부분 [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)로 전환될 것으로 전망된다. 기술사 시험에서는 <strong>3대 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 비교(시작 시간·생태계·비용)</strong>, **컴퓨팅-스토리지 분리 이유**, <strong>Spot <a href="/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/">VM</a> 트레이드오프</strong>가 핵심 논점이다.

> 📢 **섹션 요약 비유**: 관리형 빅데이터 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 클라우드 시대의 공유 주방이다. 내 주방(자체 서버)이 없어도 필요할 때 전문 주방(클러스터)을 빌려 요리(분석)하고, 끝나면 깨끗이 반납한다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| Amazon EMR | AWS 구현체 | EC2 기반, S3 통합, Spot 지원 |
| Azure HDInsight | Azure 구현체 | ADLS Gen2, Synapse 통합 |
| GCP Dataproc | GCP 구현체 | 빠른 시작, [BigQuery](/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) 통합 |
| EMR [Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) | [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 진화 | 클러스터 없이 Spark 실행 |
| 컴퓨팅-스토리지 분리 | 설계 원칙 | [레이크하우스](/studynote/16_bigdata/07_data_lake/146_lakehouse/) 아키텍처 핵심 |
| Spot/Preemptible [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) | 비용 최적화 | [Task](/studynote/02_operating_system/02_process_thread/150_task/) Node 비용 60~80% 절감 |

---


### 📈 관련 키워드 및 발전 흐름도

```text
[온프레미스 하둡 클러스터 — 자체 서버 구축·운영, 높은 초기 비용과 확장성 한계]
    |
    v
[클라우드 매니지드 하둡 (EMR·HDInsight·Dataproc) — 클러스터 프로비저닝 자동화, 분 단위 과금]
    |
    v
[컴퓨팅-스토리지 분리 아키텍처 — S3·ADLS·GCS에 데이터, 클러스터 종료 후도 데이터 보존]
    |
    v
[Spot/Preemptible VM 활용 — Task 노드 비용 60~80% 절감, 내결함성 설계 필수]
    |
    v
[서버리스 빅데이터 (EMR Serverless·Dataproc Serverless) — 클러스터 없이 Spark·Hive 실행]
```

이 흐름은 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) [하둡](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)의 운영 부담을 [클라우드 매니지드 서비스](/studynote/12_it_management/01_governance_strategy/837_msp_managed_service_provider/)로 해소하고, 컴퓨팅-스토리지 분리로 비용 효율을 높이며, Spot [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 활용을 거쳐 클러스터 없이 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 실행하는 [서버리스 빅데이터](/studynote/16_bigdata/09_platform/182_serverless_bigdata/) 분석으로 진화하는 클라우드 빅데이터 아키텍처의 핵심 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 클라우드 빅데이터 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 요리사(Spark) 팀을 필요할 때만 빌려주는 파견 업체예요.
2. 요리가 끝나면 팀을 돌려보내고(클러스터 종료) 재료([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))만 창고(S3/GCS)에 남겨두면 돼요.
3. AWS(EMR), Azure(HDInsight), GCP(Dataproc) 세 파견 업체 중 이미 쓰는 클라우드 것을 선택하면 가장 편해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 157 / 262

<- **이전**: [156. 데이터 패브릭 (Data Fabric) — 위치 무관 지능형 데이터 연결](/studynote/16_bigdata/07_data_lake/156_data_fabric/)
**다음**: [158. Databricks — Spark 기반 레이크하우스 통합 플랫폼](/studynote/16_bigdata/07_data_lake/158_databricks_platform/) ->

---
