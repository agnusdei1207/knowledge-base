---
title: "Amazon Kinesis"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 91
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Amazon Kinesis [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Streams (아마존 키네시스 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스트림)은 샤드(Shard) 기반의 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 스트리밍 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로, 샤드 1개당 1MB/s [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)·2MB/s 읽기 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 가지며 AWS 완전 관리형으로 인프라 없이 [실시간 데이터 스트리밍](/studynote/07_enterprise_systems/05_data_bi/300_realtime_data_streaming_kafka_cdc/)을 시작할 수 있다.
- **가치**: 자체 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 클러스터 운영과 달리 브로커 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/), [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), 패치가 모두 AWS에서 관리되며, [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)·Flink on EMR·Kinesis [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Analytics(Flink)·S3와 네이티브 통합되어 AWS 중심 아키텍처에서 빠른 스트리밍 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 구축이 가능하다.
- **판단 포인트**: Kinesis vs Kafka의 핵심 선택 기준은 <strong><a href="/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/">벤더 종속</a> vs 유연성</strong>이다. Kinesis는 AWS 생태계에서 간단하고 빠르지만 샤드 수 기반 수동 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)과 비용 예측이 복잡한 반면, Kafka는 유연하고 이식 가능하지만 운영 오버헤드가 크다.

---

## Ⅰ. 개요 및 필요성

### 1. Kinesis 제품군 구조

Amazon Kinesis는 스트리밍 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리를 위한 완전 관리형 AWS [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 패밀리다.

| [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 역할 | 비교 대상 |
|:---|:---|:---|
| Kinesis [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Streams | 내구성 있는 스트림 저장 ([메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐) | [Apache Kafka](/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) |
| Kinesis [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Firehose | 스트림 -> S3/Redshift/ES 자동 전달 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect |
| Kinesis [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Analytics | 스트림에 SQL/Flink 적용 | Flink/ksqlDB |
| Kinesis Video Streams | 비디오 [스트림 처리](/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/) | (특수 목적) |

이 문서는 <strong>Kinesis <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> Streams</strong>에 집중한다.

### 2. 사용 사례

- [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 실시간 수집 (수백만 디바이스)
- 웹/모바일 앱 [클릭스트림 분석](/studynote/16_bigdata/05_analysis/120_clickstream_analysis/)
- 금융 거래 실시간 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링
- [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 집계 및 실시간 알림

**📢 섹션 요약 비유**
> Kinesis는 "AWS가 운영하는 컨베이어 벨트 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)"다. 직접 컨베이어를 만들고([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 클러스터 구축) 유지보수할 필요 없이, AWS가 이미 깔아 놓은 벨트를 빌려 쓰는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Kinesis [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Streams 구조

```
+--------------------------------------------------------------+
|  Kinesis Data Streams: "OrderEvents" 스트림                  |
|                                                              |
|  +--------------+  +--------------+  +--------------+       |
|  |  Shard 1     |  |  Shard 2     |  |  Shard 3     |       |
|  |              |  |              |  |              |       |
|  | 1MB/s 쓰기   |  | 1MB/s 쓰기   |  | 1MB/s 쓰기   |       |
|  | 2MB/s 읽기   |  | 2MB/s 읽기   |  | 2MB/s 읽기   |       |
|  | 오프셋(시퀀스)|  | 오프셋(시퀀스)|  | 오프셋(시퀀스)|      |
|  +--------------+  +--------------+  +--------------+       |
|                                                              |
|  데이터 보존: 24시간(기본) ~ 7일(확장) ~ 365일(장기)          |
+--------------------------------------------------------------+
                 |                     |
    +------------+                     +-------------+
    v                                               v
Lambda (서버리스)                          Kinesis Data Analytics
(실시간 트리거)                             (Flink SQL/Java 처리)
```

### 2. 샤드 용량 계산

```
필요 샤드 수 계산:

쓰기 샤드 = 초당 레코드 수 / 1,000 또는 MB/s / 1MB
읽기 샤드 = 소비자 수 × MB/s 소비량 / 2MB

예시: 초당 5,000 레코드, 평균 레코드 크기 500 bytes
  -> 쓰기 처리량 = 5,000 × 500B = 2.5MB/s
  -> 쓰기 샤드 = ceil(2.5 / 1) = 3 샤드

  3개 Lambda 함수가 각각 1MB/s씩 소비한다면:
  -> 읽기 처리량 = 3 × 1MB = 3MB/s
  -> 읽기 샤드 = ceil(3 / 2) = 2 샤드 (쓰기가 더 많으므로 3 샤드 유지)
```

### 3. Kinesis vs [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 비교

| 비교 항목 | Amazon Kinesis [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Streams | [Apache Kafka](/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) |
|:---|:---|:---|
| 운영 방식 | 완전 관리형 (AWS) | 자체 운영 또는 MSK |
| [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 단위 | 샤드 (Shard) | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) ([Partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)) |
| [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) | 수동 (샤드 추가/분할) | 유연 ([파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수 조정) |
| 보존 기간 | 24h~365일 (비용에 따라) | 무제한 ([설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)에 따라) |
| [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)/단위 | 1MB/s [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), 2MB/s 읽기 | 브로커 하드웨어에 따라 |
| 비용 모델 | 샤드 시간당 + [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송 | 클러스터 운영 비용 |
| [벤더 종속](/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/) | AWS 전용 | 멀티클라우드 가능 |
| 커뮤니티 | AWS [에코](/studynote/03_network/01_data_communication/031_에코_반향/)시스템 | 대형 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 생태계 |

**📢 섹션 요약 비유**
> Kinesis는 "렌터카(AWS 관리)", Kafka는 "내 차(자체 운영)"다. 렌터카는 편하지만 비용이 불투명하고 원하는 옵션을 마음대로 바꿀 수 없다. 내 차는 자유롭지만 유지보수가 내 책임이다.

---

## Ⅲ. 비교 및 연결

### 1. Kinesis Enhanced Fan-Out

기본 Kinesis는 샤드당 2MB/s 읽기를 모든 Consumer가 공유한다. Enhanced Fan-Out(확장 팬아웃)은 각 Consumer가 샤드당 <strong>독립적으로 2MB/s</strong>를 가진다.

```
기본 모드 (Shared):
  샤드 1: 2MB/s -> Consumer A + Consumer B + Consumer C 공유 (~0.67MB/s 각각)

Enhanced Fan-Out:
  샤드 1 -> Consumer A: 2MB/s (독립)
         -> Consumer B: 2MB/s (독립)
         -> Consumer C: 2MB/s (독립)
```

### 2. AWS [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 통합

| 통합 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 역할 |
|:---|:---|
| AWS [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) | 레코드별 [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 처리 ([트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)) |
| Amazon EMR (Flink/Spark) | 복잡한 스트리밍 연산 |
| Amazon S3 | Kinesis Firehose를 통한 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) 저장 |
| Amazon [DynamoDB](/studynote/05_database/04_transactions_concurrency/545_dynamodb/) | 스트리밍 이벤트의 상태 저장 |
| Amazon CloudWatch | 샤드 레벨 지표 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 |

**📢 섹션 요약 비유**
> Enhanced Fan-Out은 "공용 수도관(기본 모드)에서 세대별 독립 배관(Fan-Out)으로 업그레이드"하는 것이다. 이웃 세대가 물을 많이 써도 내 수압([처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))에 영향이 없어진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 1. Kinesis vs [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 선택 기준

| 상황 | 권장 솔루션 |
|:---|:---|
| AWS 전용 아키텍처, 빠른 구축 | Amazon Kinesis |
| 멀티클라우드 또는 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 포함 | [Apache Kafka](/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) |
| 운영 팀 없는 소규모 팀 | Kinesis (관리형) |
| 대규모 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/), 세밀한 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 제어 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) (MSK 또는 자체) |
| [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 호환 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 필요 | Amazon MSK (Managed [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)) |

### 2. 샤드 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [ ] `ProvisionedThroughputExceededException` 발생 시 샤드 분할(SplitShard)
- [ ] Enhanced Fan-Out: Consumer > 1개이고 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 경쟁 발생 시 활성화
- [ ] On-Demand 모드([2021](/studynote/04_software_engineering/11_testing_validation/869_owasp_top_10_2021/)+): 자동 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/), 예측 불가능한 트래픽에 적합
- [ ] 샤드 수 줄이기: MergeShards [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) (인접 샤드만 병합 가능)

**📢 섹션 요약 비유**
> Kinesis On-Demand 모드는 "오토스케일링 되는 고속도로"다. 교통량에 따라 차선이 자동으로 늘어나고 줄어들어 피크 시간에도 막히지 않는다. 대신 차선 수를 내가 통제할 수 없다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| 빠른 시작 | 클러스터 구축 없이 수 분 내 스트리밍 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 구동 |
| AWS 통합 | [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)/S3/Flink와 네이티브 연동으로 개발 생산성 향상 |
| 운영 부담 감소 | 브로커 패치, [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링을 AWS가 담당 |

### 2. 결론

Amazon Kinesis [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Streams는 <strong>AWS 생태계 내 스트리밍의 표준 솔루션</strong>이다. 기술사 답안에서는 샤드 기반 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 구조, Kafka와의 [벤더 종속](/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/) vs 유연성 트레이드오프, Enhanced Fan-Out의 필요성, 그리고 AWS [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 통합 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 체계적으로 서술해야 한다.

**📢 섹션 요약 비유**
> Kinesis는 "AWS라는 도시의 지하철 시스템"이다. 도시 안(AWS)에서는 최적화되어 있고 편리하지만, 다른 도시(다른 클라우드)로 이사하면 지하철이 없어 처음부터 다시 만들어야 한다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [Apache Kafka](/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) | 비교 대상 | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 스트리밍의 대안 |
| Amazon MSK | 연관 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 완전 관리형(MSK)은 Kinesis의 대안 |
| Kinesis Firehose | 연동 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | Kinesis [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 S3/Redshift로 자동 전달 |
| AWS [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) | 소비자 통합 | Kinesis [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)로 [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 처리 |
| [Consumer Lag](/studynote/16_bigdata/04_streaming/089_consumer_lag/) | [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 개념 | Kinesis에서는 GetRecords.MillisBehindLatest |


### 📈 관련 키워드 및 발전 흐름도

```text
[배치 수집 (Batch Ingestion) — 주기적 ETL 파이프라인, 높은 지연]
    |
    v
[Amazon Kinesis Data Streams — 실시간 스트림 수집, 샤드 기반 병렬 처리]
    |
    v
[Kinesis Data Firehose — 무서버 스트림->S3/Redshift 자동 전달, 변환 내장]
    |
    v
[Kinesis Data Analytics (Apache Flink) — SQL·Flink로 스트림 실시간 분석]
    |
    v
[Lambda Architecture / Kappa Architecture — 배치+스트림 통합 또는 스트림 단일화 아키텍처]
```
이 흐름은 [배치 처리](/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)의 높은 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 한계를 극복하기 위해 Amazon Kinesis가 실시간 스트림 수집의 관리형 표준으로 자리잡고, 저장·분석 레이어와 결합하여 엔드투엔드 실시간 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 아키텍처로 진화하는 스트리밍 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리의 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

Amazon Kinesis는 AWS가 운영하는 컨베이어 벨트예요. 공장(여러분의 앱)에서 물건([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 올려놓으면 벨트가 알아서 다음 장소([Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/), S3)로 이동시켜 줘요. 직접 벨트를 만들고 수리할([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 운영) 필요 없이 AWS에 빌리면 되니까 처음 시작하기 훨씬 쉬워요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 91 / 262

<- **이전**: [15. Kafka MirrorMaker 2 — 클러스터 간 복제 및 DR](/studynote/16_bigdata/04_streaming/090_kafka_mirrormaker2/)
**다음**: [17. Google Pub/Sub — GCP 글로벌 분산 메시지 서비스](/studynote/16_bigdata/04_streaming/092_google_pubsub/) ->

---
