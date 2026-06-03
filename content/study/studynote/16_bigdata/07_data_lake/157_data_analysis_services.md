+++
weight = 157
title = "157. 클라우드 빅데이터 분석 서비스 — Amazon EMR/Azure HDInsight/GCP Dataproc"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
1. 클라우드 관리형 빅데이터 [[090_service_kubernetes_network_load_balancing|서비스]](Amazon EMR, Azure HDInsight, GCP Dataproc)는 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]]/Spark 클러스터를 수 분 내에 [[528_provisioning|프로비저닝]]하고, 운영 완료 후 즉시 종료하여 **사용한 시간만큼만 비용을 지불**하는 탄력적 컴퓨팅을 제공한다.
2. 세 [[090_service_kubernetes_network_load_balancing|서비스]] 모두 **컴퓨팅과 스토리지를 분리(Decoupled [[319_architecture|Architecture]])**하여 S3/ADLS/GCS에 저장된 [[001_dikw_pyramid|데이터]]를 여러 클러스터가 독립적으로 처리할 수 있어 [[146_lakehouse|레이크하우스]] 아키텍처와 자연스럽게 통합된다.
3. 클러스터 시작 시간(수 분), 생태계 통합 깊이, 비용 모델(EC2 vs SKU)이 세 [[090_service_kubernetes_network_load_balancing|서비스]]의 핵심 차별 요소이며, [[206_serverless_cold_start|서버리스]] 옵션(EMR [[206_serverless_cold_start|Serverless]], Dataproc [[206_serverless_cold_start|Serverless]])이 운영 오버헤드를 더욱 낮추고 있다.

---

## Ⅰ. 개요 및 필요성

자체 관리 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 클러스터는 하드웨어 구매, 클러스터 [[009_config|설정]], 보안 패치, 용량 계획 등 막대한 운영 오버헤드가 따른다. 분석 워크로드는 주기적이거나 일회성인 경우가 많아 항상 켜 있는 클러스터가 비효율적이다.

클라우드 관리형 [[090_service_kubernetes_network_load_balancing|서비스]]는 클릭 또는 [[014_api_posix|API]] 호출로 클러스터를 [[087_process_state_transition|생성]]하고, 작업 완료 후 삭제하는 탄력적 운영을 가능하게 한다. 2024년 현재는 [[206_serverless_cold_start|서버리스]] 옵션이 등장하여 클러스터 관리 자체를 클라우드에 위임하는 방향으로 진화하고 있다.

| [[090_service_kubernetes_network_load_balancing|서비스]] | 클라우드 | 기반 기술 | 출시 |
|:---|:---|:---|:---|
| Amazon EMR (Elastic [[018_mapreduce|MapReduce]]) | AWS | [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]]/Spark/[[544_hive|Hive]]/Presto | 2009 |
| Azure HDInsight | Microsoft Azure | [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]]/Spark/[[179_kafka_flink_watermark_time_window|Kafka]]/[[543_hbase|HBase]] | 2014 |
| GCP Dataproc | Google Cloud | [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]]/Spark | 2015 |

> 📢 **섹션 요약 비유**: 관리형 빅데이터 [[090_service_kubernetes_network_load_balancing|서비스]]는 렌터카와 같다. 내 차(자체 클러스터)를 유지 관리하는 대신, 필요할 때 렌트(클러스터 시작)하고 반납(종료)하면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌──────────────────────────────────────────────────────────────────┐
│          클라우드 관리형 빅데이터 서비스 아키텍처                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  객체 스토리지 (영구 저장)                                  │   │
│  │  AWS S3  /  Azure ADLS Gen2  /  GCS                      │   │
│  │  (Delta Lake / Iceberg / Parquet 파일)                    │   │
│  └────────────────────────┬─────────────────────────────────┘   │
│                           │ 읽기/쓰기 (HDFS 커넥터)              │
│  ┌────────────────────────▼─────────────────────────────────┐   │
│  │  클러스터 (임시, 작업 중만 실행)                             │   │
│  │                                                          │   │
│  │  Amazon EMR          Azure HDInsight    GCP Dataproc     │   │
│  │  ┌─────────────┐    ┌───────────────┐  ┌─────────────┐  │   │
│  │  │ Master Node │    │ Head Node     │  │ Master Node │  │   │
│  │  │ Core Nodes  │    │ Worker Nodes  │  │ Worker Node │  │   │
│  │  │ Task Nodes  │    │ (auto-scale)  │  │ (Preemptible│  │   │
│  │  │ (Spot 가능) │    │               │  │  VM 가능)   │  │   │
│  │  └─────────────┘    └───────────────┘  └─────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌────────────────────────▼─────────────────────────────────┐   │
│  │  주변 서비스 연동                                           │   │
│  │  EMR: Glue/Athena/SageMaker  │  Dataproc: BigQuery/Vertex│   │
│  │  HDInsight: Synapse/ML Studio│                            │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

**3대 [[090_service_kubernetes_network_load_balancing|서비스]] 상세 비교**

| 항목 | Amazon EMR | Azure HDInsight | GCP Dataproc |
|:---|:---|:---|:---|
| 클러스터 시작 시간 | 5~10분 | 15~20분 | 90초~2분 |
| 스팟/저비용 [[598_vm_migration_nic|VM]] | EC2 [[209_spot_instance_cloud_cost_optimization|Spot Instance]] | Azure Spot [[598_vm_migration_nic|VM]] | Preemptible [[598_vm_migration_nic|VM]] |
| [[206_serverless_cold_start|서버리스]] 옵션 | EMR [[206_serverless_cold_start|Serverless]] | 제한적 | Dataproc [[206_serverless_cold_start|Serverless]] |
| 기본 스토리지 | Amazon S3 | Azure ADLS Gen2 | Google Cloud Storage |
| [[561_container_based_deployment|컨테이너]] 지원 | EMR on EKS | AKS 통합 | Dataproc on GKE |
| ML 통합 | SageMaker | Azure ML Studio | Vertex [[190_ai_llm_requirements_specification|AI]] |
| Spark [[288_version_ihl_tos_total_length|버전]] 업그레이드 | [[162_ami_advanced_metering_infrastructure|AMI]] 교체 | 클러스터 재생성 | 즉시 [[288_version_ihl_tos_total_length|버전]] 선택 |

> 📢 **섹션 요약 비유**: EMR은 대형 마트(AWS 풀 [[031_에코_반향|에코]]시스템), HDInsight는 Office Suite(Microsoft 생태계 통합), Dataproc는 스포츠카(빠른 시작, [[263_storage_compute_separation_bigquery|BigQuery]] 통합)에 비유할 수 있다.

---

## Ⅲ. 비교 및 연결

**자체 관리 클러스터 vs 관리형 [[090_service_kubernetes_network_load_balancing|서비스]] vs [[206_serverless_cold_start|서버리스]]**

| 항목 | 자체 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] | 관리형 [[090_service_kubernetes_network_load_balancing|서비스]] | [[206_serverless_cold_start|서버리스]] (EMR/Dataproc) |
|:---|:---|:---|:---|
| [[528_provisioning|프로비저닝]] 시간 | 수 시간~수 일 | 2~20분 | 수 초 (자동) |
| 운영 오버헤드 | 매우 높음 | 보통 | 없음 |
| 비용 최적화 | 어려움 | Spot 인스턴스 활용 | 사용량 기반 완전 종량 |
| 적합 워크로드 | 상시 대용량 | 정기 배치, 중간 규모 | 간헐적 소규모~대규모 |

**[[146_lakehouse|레이크하우스]] 통합 패턴**

- **EMR + S3 + [[147_delta_lake|Delta Lake]]**: EMR 클러스터에서 [[147_delta_lake|Delta Lake]] 테이블 읽기/[[289_cqrs_db|쓰기]]
- **Dataproc + GCS + Iceberg**: Spark on Dataproc으로 Iceberg 테이블 처리
- **HDInsight + ADLS Gen2 + Hudi**: HDInsight Spark로 [[217_cdc_binlog_change_capture_debezium|CDC]] upsert

> 📢 **섹션 요약 비유**: 세 [[090_service_kubernetes_network_load_balancing|서비스]] 선택은 이사업체 선택과 같다. 짐의 양([[001_dikw_pyramid|데이터]] 규모), 이사 빈도(워크로드 패턴), 이미 살고 있는 동네(클라우드 생태계)에 따라 최적 업체가 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**비용 최적화 [[268_strategy_pattern|전략]]**

| [[268_strategy_pattern|전략]] | 설명 | 절감 효과 |
|:---|:---|:---|
| Spot/Preemptible [[598_vm_migration_nic|VM]] | [[150_task|Task]] Node에 스팟 [[598_vm_migration_nic|VM]] 사용 | 60~80% 비용 절감 |
| 작업 완료 후 즉시 종료 | 클러스터를 ephemeral하게 운영 | 유휴 시간 비용 제거 |
| 스토리지-컴퓨팅 분리 | S3/GCS를 외부 스토리지로 | 클러스터 종료 시에도 [[001_dikw_pyramid|데이터]] 보존 |
| [[206_serverless_cold_start|서버리스]] 전환 | 소규모 간헐적 작업에 [[206_serverless_cold_start|서버리스]] | [[528_provisioning|프로비저닝]] 비용 제거 |

**기술사 답안 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| 3대 [[090_service_kubernetes_network_load_balancing|서비스]] 비교 | 시작 시간 (Dataproc 최단), 생태계 (AWS/Azure/GCP), [[206_serverless_cold_start|서버리스]] 지원 |
| 컴퓨팅-스토리지 분리 이유 | 클러스터 종료 후에도 [[001_dikw_pyramid|데이터]] 보존, 여러 클러스터가 동일 [[386_data_clean_room_sharing|데이터 공유]] |
| Spot [[598_vm_migration_nic|VM]] 사용 한계 | 중단 가능(중요 워크로드 부적합), Checkpoint 설계 필요 |
| [[206_serverless_cold_start|서버리스]] 전환 시점 | 간헐적 소규모 작업, 클러스터 관리 오버헤드 제거 시 |

> 📢 **섹션 요약 비유**: Spot 인스턴스 사용은 빈 좌석 할인 비행기를 타는 것이다. 저렴하지만 갑자기 취소될 수 있으므로, 중요한 약속(크리티컬 작업)에는 정규 좌석(온디맨드)이 필요하다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 인프라 운영 비용 절감 | 클러스터 관리 인력 불필요, 보안 패치 자동화 |
| 탄력적 확장 | 워크로드 크기에 따라 수 분 내 클러스터 규모 조정 |
| 최신 기술 즉시 활용 | Spark [[288_version_ihl_tos_total_length|버전]] 업그레이드가 클러스터 교체로 즉시 가능 |
| 비용 투명성 | 사용 시간·[[001_dikw_pyramid|데이터]] [[139_throughput|처리량]] 기반 정확한 비용 집계 |

클라우드 관리형 빅데이터 [[090_service_kubernetes_network_load_balancing|서비스]]는 자체 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 클러스터의 운영 부담을 제거하고, [[146_lakehouse|레이크하우스]] 아키텍처의 컴퓨팅 레이어를 탄력적으로 제공한다. [[206_serverless_cold_start|서버리스]] 방향으로의 진화가 가속화되면서 2025년 이후 간헐적 배치 작업은 대부분 [[206_serverless_cold_start|서버리스]]로 전환될 것으로 전망된다. 기술사 시험에서는 **3대 [[090_service_kubernetes_network_load_balancing|서비스]] 비교(시작 시간·생태계·비용)**, **컴퓨팅-스토리지 분리 이유**, **Spot [[598_vm_migration_nic|VM]] 트레이드오프**가 핵심 논점이다.

> 📢 **섹션 요약 비유**: 관리형 빅데이터 [[090_service_kubernetes_network_load_balancing|서비스]]는 클라우드 시대의 공유 주방이다. 내 주방(자체 서버)이 없어도 필요할 때 전문 주방(클러스터)을 빌려 요리(분석)하고, 끝나면 깨끗이 반납한다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| Amazon EMR | AWS 구현체 | EC2 기반, S3 통합, Spot 지원 |
| Azure HDInsight | Azure 구현체 | ADLS Gen2, Synapse 통합 |
| GCP Dataproc | GCP 구현체 | 빠른 시작, [[263_storage_compute_separation_bigquery|BigQuery]] 통합 |
| EMR [[206_serverless_cold_start|Serverless]] | [[206_serverless_cold_start|서버리스]] 진화 | 클러스터 없이 Spark 실행 |
| 컴퓨팅-스토리지 분리 | 설계 원칙 | [[146_lakehouse|레이크하우스]] 아키텍처 핵심 |
| Spot/Preemptible [[598_vm_migration_nic|VM]] | 비용 최적화 | [[150_task|Task]] Node 비용 60~80% 절감 |

---


### 📈 관련 키워드 및 발전 흐름도

```text
[온프레미스 하둡 클러스터 — 자체 서버 구축·운영, 높은 초기 비용과 확장성 한계]
    │
    ▼
[클라우드 매니지드 하둡 (EMR·HDInsight·Dataproc) — 클러스터 프로비저닝 자동화, 분 단위 과금]
    │
    ▼
[컴퓨팅-스토리지 분리 아키텍처 — S3·ADLS·GCS에 데이터, 클러스터 종료 후도 데이터 보존]
    │
    ▼
[Spot/Preemptible VM 활용 — Task 노드 비용 60~80% 절감, 내결함성 설계 필수]
    │
    ▼
[서버리스 빅데이터 (EMR Serverless·Dataproc Serverless) — 클러스터 없이 Spark·Hive 실행]
```

이 흐름은 [[061_on_premise_legacy_infrastructure|온프레미스]] [[843_hadoop_rack_awareness_data_replication_topology|하둡]]의 운영 부담을 [[045_msp_managed_service_provider|클라우드 매니지드 서비스]]로 해소하고, 컴퓨팅-스토리지 분리로 비용 효율을 높이며, Spot [[598_vm_migration_nic|VM]] 활용을 거쳐 클러스터 없이 [[298_qkv_attention|쿼리]]를 실행하는 [[182_serverless_bigdata|서버리스 빅데이터]] 분석으로 진화하는 클라우드 빅데이터 아키텍처의 핵심 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 클라우드 빅데이터 [[090_service_kubernetes_network_load_balancing|서비스]]는 요리사(Spark) 팀을 필요할 때만 빌려주는 파견 업체예요.
2. 요리가 끝나면 팀을 돌려보내고(클러스터 종료) 재료([[001_dikw_pyramid|데이터]])만 창고(S3/GCS)에 남겨두면 돼요.
3. AWS(EMR), Azure(HDInsight), GCP(Dataproc) 세 파견 업체 중 이미 쓰는 클라우드 것을 선택하면 가장 편해요.
