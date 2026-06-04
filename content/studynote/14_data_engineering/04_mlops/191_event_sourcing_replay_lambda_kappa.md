---
title: "191. 람다/카파 아키텍처 재현 (Event Sourcing Replay - Lambda/Kappa Architecture)"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)([Event Sourcing](/studynote/12_it_management/05_security_compliance/307_event_sourcing/))은 시스템 상태를 이벤트 스트림으로 저장해 언제든 과거 시점으로 재현(Replay)하는 패턴이다.
> 2. **가치**: [람다](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)([Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/))는 배치+스트림 [이중 경로](/studynote/02_operating_system/08_storage_and_io_systems/500_multipath_io/)로 정확성과 저지연을 동시에 달성하고, 카파([Kappa](/studynote/16_bigdata/12_trends/235_kappa/))는 스트림 단일 경로로 운영 복잡도를 줄인다.
> 3. **판단 포인트**: 배치 재처리 비용과 운영 복잡도 허용 수준에 따라 [람다](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) vs 카파를 선택하며, 최신 스트림 엔진(Flink, [Spark Structured Streaming](/studynote/16_bigdata/03_spark/061_structured_streaming/))은 카파 전환을 가속한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) ([Event Sourcing](/studynote/12_it_management/05_security_compliance/307_event_sourcing/)) 정의

[이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)은 애플리케이션 상태 변화를 **이벤트(Event)** 의 연속으로 저장하고, [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)를 이 이벤트들을 순서대로 재적용(Replay)하여 도출하는 패턴이다. 전통적 CRUD 방식이 최종 상태만 저장하는 것과 대비된다.

| 방식 | 저장 단위 | 특징 |
|:---|:---|:---|
| CRUD | [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)([스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)) | 이력 손실, 간단한 구현 |
| [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) | 이벤트 스트림 | 완전한 이력, 재현 가능 |

### 1.2 왜 [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)이 필요한가?

- <strong><a href="/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a> 추적(<a href="/studynote/11_design_supervision/01_audit_framework/065_audit_trail_worm_storage_compliance/">Audit Trail</a>)</strong>: 모든 변경 사항이 불변([Immutable](/studynote/13_cloud_architecture/05_data_engineering/298_immutable/)) 이벤트로 기록됨
- **시간 여행(Time Travel)**: 특정 시점의 상태 재현 가능
- **새 로직 소급 적용**: 비즈니스 로직 변경 시 과거 이벤트 전체 재처리
- <strong><a href="/studynote/12_it_management/05_security_compliance/306_cqrs/">CQRS</a>(<a href="/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/">Command</a> Query Responsibility Segregation)</strong> 와 자연스러운 결합

### 1.3 [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) 이벤트 스트림 개념

```
시간 흐름 ->
+------+  +------+  +------+  +------+  +------+
|E1    |-> |E2    |-> |E3    |-> |E4    |-> |E5    |
|주문생성|  |결제완료|  |배송시작|  |배송완료|  |리뷰작성|
+------+  +------+  +------+  +------+  +------+
     v Replay(재현)
+---------------------------------+
| 현재 상태 = 순서대로 이벤트 적용     |
| 언제든 원하는 시점 상태 재현 가능    |
+---------------------------------+
```

📢 **섹션 요약 비유**: [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)은 "가계부"와 같다. 잔액만 적어두면 과거를 알 수 없지만, 입출금 내역을 모두 기록하면 어느 날의 잔액이든 계산해낼 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [람다 아키텍처](/studynote/16_bigdata/04_streaming/095_lambda_architecture/) ([Lambda Architecture](/studynote/16_bigdata/04_streaming/095_lambda_architecture/))

Nathan Marz가 제안한 빅데이터 처리 아키텍처로, 배치와 스트림 두 레이어를 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 운영하여 정확성과 저지연을 동시에 달성한다.

```
데이터 소스
    |
    +-----------------------------+
    |                             |
    v                             v
+-----------------+   +-----------------+
|  배치 레이어      |   |  스피드 레이어    |
|  (Batch Layer)  |   |  (Speed Layer)  |
|                 |   |                 |
| HDFS / S3       |   | Kafka + Flink   |
| Spark Batch     |   | 실시간 처리       |
| 고정확도         |   | 저지연           |
| 고지연(시간~일)  |   | 근사치(최근 데이터)|
+--------+--------+   +--------+--------+
         |                     |
         v                     v
+---------------------------------+
|          서빙 레이어              |
|         (Serving Layer)         |
|                                 |
|  배치 뷰(Batch View) +           |
|  실시간 뷰(Realtime View) 병합    |
|  -> 사용자 쿼리 응답               |
+---------------------------------+
```

| 레이어 | 역할 | 기술 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |
|:---|:---|:---|:---|
| Batch Layer | 전체 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정확 처리 | [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/), Spark, [Hive](/studynote/05_database/04_transactions_concurrency/544_hive/) | 시간~일 |
| [Speed Layer](/studynote/12_it_management/02_itsm_itil/092_GPT_NLP/) | 최근 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 빠른 처리 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), Flink, Storm | 초~분 |
| Serving Layer | 두 레이어 결과 병합 조회 | [Cassandra](/studynote/05_database/04_transactions_concurrency/541_cassandra/), [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/), Druid | ms |

### 2.2 [카파 아키텍처](/studynote/16_bigdata/04_streaming/096_kappa_architecture/) ([Kappa Architecture](/studynote/16_bigdata/04_streaming/096_kappa_architecture/))

Jay Kreps([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 창시자)가 [람다](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)의 복잡성을 비판하며 제안. <strong><a href="/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/">스트림 처리</a> 단일 레이어</strong>로 배치 역할까지 수행.

```
데이터 소스
    |
    v
+---------------------------------+
|         메시지 큐(Kafka)          |
|   이벤트 영구 보관 (무한 보존)      |
|   파티셔닝, 순서 보장              |
+----------------+----------------+
                 |
        +--------+--------+
        |                 |
        v                 v
+--------------+  +--------------+
| 실시간 처리   |  | 재처리(Replay) |
| (Consumer v1)|  | (Consumer v2) |
| 현재 로직 적용|  | 새 로직 소급  |
+------+-------+  +------+-------+
       |                 |
       +--------+--------+
                v
+---------------------------------+
|          서빙 레이어              |
|   단일 스트림 처리 결과 조회        |
+---------------------------------+
```

### 2.3 [람다](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) vs 카파 비교

| 항목 | [람다 아키텍처](/studynote/16_bigdata/04_streaming/095_lambda_architecture/) | [카파 아키텍처](/studynote/16_bigdata/04_streaming/096_kappa_architecture/) |
|:---|:---|:---|
| 처리 경로 | 배치 + 스트림 [이중 경로](/studynote/02_operating_system/08_storage_and_io_systems/500_multipath_io/) | 스트림 단일 경로 |
| 운영 복잡도 | 높음 (코드 [이중화](/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)) | 낮음 (단일 [코드베이스](/studynote/15_devops_sre/01_culture_methodology/007_codebase/)) |
| 재처리 방법 | 배치 재실행 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 오프셋 리셋 후 재처리 |
| 정확도 | 배치 기준 높은 정확도 | [스트림 처리](/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/) 정확도 (근사 허용) |
| 적합 사례 | 복잡한 집계, ML 학습 | [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/), 실시간 파이프라인 |
| 도입 난이도 | 복잡 | 비교적 단순 |

### 2.4 [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) ([Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) Query Responsibility Segregation)

CQRS는 명령([Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/): [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))과 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)(Query: 읽기)를 분리하는 패턴이다. [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)과 결합하면 강력한 시스템을 구성한다.

```
+-------------------------------------------------+
|                   CQRS + 이벤트 소싱              |
|                                                 |
|  클라이언트                                       |
|    |                                            |
|    +---- Command(쓰기) ---> Command Handler       |
|    |                           |                |
|    |                           v                |
|    |                    이벤트 스토어             |
|    |                    (Kafka/EventStore)       |
|    |                           |                |
|    |                     Projection             |
|    |                    (읽기 모델 생성)          |
|    |                           |                |
|    |                           v                |
|    +---- Query(읽기) --->  Read DB(최적화)        |
|                           (Redis/Elasticsearch) |
+-------------------------------------------------+
```

📢 **섹션 요약 비유**: [람다](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)는 두 개의 주방에서 요리하는 레스토랑(빠른 패스트푸드 창구 + 정성스러운 정식 주방)이고, 카파는 한 주방에서 빠르고 정확하게 모든 요리를 처리하는 효율적 주방이다.

---

## Ⅲ. 비교 및 연결

### 3.1 [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) Replay 상세 흐름

```
[기존 로직 v1 처리 중]
Kafka Topic: order-events (offset 0 ~ 100,000)

오프셋 0  ---> 이벤트 소비 ---> 로직 v1 적용 ---> DB 저장

[새 로직 v2 적용 필요]
          +---------------------------------+
          |  새 컨슈머 그룹(Consumer Group)  |
          |  오프셋 0부터 재시작              |
          |  오프셋 0 ---> 로직 v2 적용       |
          |  오프셋 1 ---> 로직 v2 적용       |
          |      ...                        |
          |  오프셋 100,000 ---> v2 완료      |
          +---------------------------------+

결과: v2 기준 전체 히스토리 재계산 완료
v1 결과와 병행 운영 후 전환 (Blue/Green)
```

### 3.2 Kafka를 [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) 스토어로 활용

| [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 기능 | [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) 활용 |
|:---|:---|
| 토픽(Topic) [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) | 엔티티(Entity) ID 기준 [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/) |
| 오프셋(Offset) | 이벤트 순서 보장 |
| 보존 기간([Retention](/studynote/05_database/04_transactions_concurrency/515_mvcc/)) | 무기한 보존으로 완전한 이력 |
| [컨슈머 그룹](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/) | 여러 Projection [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 |
| [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)([Log Compaction](/studynote/13_cloud_architecture/05_data_engineering/261_kafka_log_compaction_key_value/)) | 최신 상태 [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) 유지 |

### 3.3 [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) vs 전통 DB

| 비교 항목 | 전통 DB (CRUD) | [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) |
|:---|:---|:---|
| 저장 단위 | [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) | 이벤트 스트림 |
| [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 복잡도 | 단순 [SELECT](/studynote/05_database/04_transactions_concurrency/520_select/) | Projection [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 필요 |
| 이력 추적 | 별도 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 테이블 필요 | 기본 제공 |
| 확장성 | 수직적 확장 | 수평적 확장 |
| 디버깅 | 어려움 | 이벤트 재현으로 용이 |
| 스토리지 | 효율적 | 많은 스토리지 필요 |

📢 **섹션 요약 비유**: Kafka의 오프셋(Offset)은 책의 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 번호와 같다. 어느 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)부터든 다시 읽을 수 있고, 새 독자(새 [컨슈머 그룹](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/))는 1페이지부터 자신만의 읽기를 시작할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [람다](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) vs 카파 선택 기준

| 상황 | 권장 아키텍처 | 이유 |
|:---|:---|:---|
| 복잡한 집계 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) + 정확도 최우선 | [람다](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) | 배치 레이어의 정확한 처리 |
| 실시간 이벤트 파이프라인 | 카파 | 단순한 운영, 재처리 용이 |
| 팀 규모 작음 | 카파 | 이중 [코드베이스](/studynote/15_devops_sre/01_culture_methodology/007_codebase/) 유지 부담 |
| 레거시 배치 시스템 공존 | [람다](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) | 점진적 마이그레이션 |
| Flink/[Spark Structured Streaming](/studynote/16_bigdata/03_spark/061_structured_streaming/) 도입 | 카파 | 배치/스트림 통합 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) |

### 4.2 실무 구현 패턴: [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) + 카파

```
[주문 시스템 예시]

사용자 주문
    |
    v
Order Command Handler
    | OrderCreated 이벤트 발행
    v
Kafka Topic: order-events
 +- Partition 0: userId % N
 +- 무기한 보존(log.retention.ms=-1)
 +- Log Compaction 활성화

    |
    +---> Consumer Group A: 재고 Projection -> Redis
    +---> Consumer Group B: 결제 Projection -> PostgreSQL
    +---> Consumer Group C: 검색 Projection -> Elasticsearch
    +---> Consumer Group D: 분석 Projection -> ClickHouse
```

### 4.3 재처리(Replay) 운영 절차

1. <strong>새 <a href="/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/">Consumer Group</a> <a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a></strong>: `order-events-v2-consumer`
2. **오프셋 초기화**: `--reset-offsets --to-earliest`
3. <strong>새 로직 <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a> 배포</strong>: Blue/Green 전략으로 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 운영
4. <strong>재처리 완료 <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong>: 처리 카운트 및 결과 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)
5. **트래픽 전환**: 서빙 레이어에서 v2 결과로 전환
6. **기존 Consumer 제거**: v1 [Consumer Group](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/) 중단

### 4.4 주요 도전과 해결책

| 도전 과제 | 해결 방법 |
|:---|:---|
| 이벤트 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변화 | Apache Avro + [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) [Registry](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) |
| 재처리 시 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 부하 | 별도 토픽/클러스터에서 재처리 |
| 이벤트 순서 보장 | 동일 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키 사용 |
| 대용량 이벤트 스토어 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Tiered Storage |
| [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) 없이 긴 이력 재현 | 주기적 [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) + 이후 이벤트 적용 |

📢 **섹션 요약 비유**: 재처리(Replay)는 비디오 녹화본을 처음부터 다시 돌려보는 것과 같다. 같은 영상이지만 새로운 시각(로직)으로 다시 분석하면 다른 결론을 낼 수 있다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) + [카파 아키텍처](/studynote/16_bigdata/04_streaming/096_kappa_architecture/)의 기대효과

| 효과 | 정량적 지표 |
|:---|:---|
| 운영 복잡도 감소 | [람다](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 대비 [코드베이스](/studynote/15_devops_sre/01_culture_methodology/007_codebase/) 50% 감소 |
| 재처리 자동화 | 수동 배치 재실행 제거 |
| 완전한 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적 | 모든 상태 변화 100% 추적 |
| 새 기능 빠른 배포 | [Consumer Group](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/) 추가로 무중단 확장 |

### 5.2 기술 선택 가이드라인 (기술사 관점)

```
이벤트 소싱/스트림 아키텍처 의사결정 트리

스트림 처리 필요?
+- NO  -> 전통 CRUD + 배치 ETL
+- YES -> 실시간 정확도 요구?
          +- 높음 + 복잡 집계 -> 람다 아키텍처
          |   (배치 + 스트림 병렬 운영)
          +- 보통 + 운영 단순화 -> 카파 아키텍처
              (스트림 단일 경로)
              +- 이력/감사 필요? -> 이벤트 소싱 결합
```

### 5.3 현업 채택 현황

| 기업 | 아키텍처 | 용도 |
|:---|:---|:---|
| Netflix | [람다](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) -> 카파 전환 | 실시간 추천 |
| LinkedIn | 카파 ([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 기반) | 사용자 활동 스트림 |
| Uber | [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) + [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) | 실시간 주문/위치 처리 |
| Airbnb | [람다](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) -> Flink 기반 카파 | 가격 최적화 |

### 5.4 결론 요약

[이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 불변성과 재현성을 보장하는 강력한 패턴이며, [카파 아키텍처](/studynote/16_bigdata/04_streaming/096_kappa_architecture/)와 결합 시 운영 단순성과 실시간 처리를 동시에 달성한다. 기술사 시험에서는 <strong><a href="/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/">람다</a> vs 카파의 트레이드오프</strong>와 <strong>Kafka를 <a href="/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/">이벤트 소싱</a> 스토어로 활용하는 방법</strong>이 핵심 논점이다.

📢 **섹션 요약 비유**: [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) + [카파 아키텍처](/studynote/16_bigdata/04_streaming/096_kappa_architecture/)는 "블랙박스 + 실시간 내비게이션" 조합과 같다. 블랙박스(이벤트 스토어)로 모든 주행 기록을 저장하고, 내비게이션([스트림 처리](/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/))이 실시간으로 최적 경로를 안내하며, 사고(장애) 시 블랙박스로 정확한 원인을 파악한다.

---

### 📌 관련 개념 맵

| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 저장 패턴 | [Event Sourcing](/studynote/12_it_management/05_security_compliance/307_event_sourcing/) ([이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)) | 상태를 이벤트 스트림으로 저장 |
| 아키텍처 패턴 | [Lambda Architecture](/studynote/16_bigdata/04_streaming/095_lambda_architecture/) ([람다 아키텍처](/studynote/16_bigdata/04_streaming/095_lambda_architecture/)) | 배치 + 스트림 [이중 경로](/studynote/02_operating_system/08_storage_and_io_systems/500_multipath_io/) |
| 아키텍처 패턴 | [Kappa Architecture](/studynote/16_bigdata/04_streaming/096_kappa_architecture/) ([카파 아키텍처](/studynote/16_bigdata/04_streaming/096_kappa_architecture/)) | 스트림 단일 경로 |
| 설계 패턴 | [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) | 명령과 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 분리 |
| 인프라 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) | 이벤트 스토어 + 메시지 큐 |
| 재처리 | Replay (재현) | 오프셋 리셋 후 재처리 |
| 표현 변환 | Projection (프로젝션) | 이벤트 -> 읽기 모델 변환 |
| [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 관리 | [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) [Registry](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) | 이벤트 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 |

### 👶 어린이를 위한 3줄 비유 설명

1. [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)은 일기를 매일 쓰는 것과 같아요. 일기를 처음부터 다시 읽으면 오늘의 나를 정확히 이해할 수 있죠.

### 📈 관련 키워드 및 발전 흐름도

```text
CRUD 기반 상태 저장 (현재 상태만 유지)
    |
    v
이벤트 소싱 (Event Sourcing): 모든 변화를 이벤트로 기록
    +-► 이벤트 스토어: 불변 로그 (Kafka · EventStoreDB)
    +-► 상태 재구성: 이벤트 리플레이 (Replay)
    |
    v
람다 아키텍처: Batch Layer + Speed Layer 분리
    |
    v
카파 아키텍처: Speed Layer만으로 통합 (Kafka 중심)
    |
    v
CQRS: 쓰기 모델(Command)과 읽기 모델(Query) 분리
```
2. [람다 아키텍처](/studynote/16_bigdata/04_streaming/095_lambda_architecture/)는 두 개의 창구가 있는 은행이에요. 빠른 창구(스트림)와 정확한 창구(배치) 두 곳에서 결과를 합쳐요.
3. [카파 아키텍처](/studynote/16_bigdata/04_streaming/096_kappa_architecture/)는 스트리밍 서비스처럼 한 곳에서 모든 영상을 보여주는데, 필요하면 처음부터 다시 재생해서 새로운 자막(로직)도 입힐 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 191 / 258

<- **이전**: [190. 스플릿 브레인 (Split Brain) 방어 주키퍼 (ZooKeeper) 펜싱 합의 코디 연계망](/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/)
**다음**: [192. 엣지 AI 컴파일러 (Edge AI - ONNX, TensorRT) 모델 직렬화 패키징 배포망](/studynote/14_data_engineering/04_mlops/192_edge_ai_onnx_tensorrt_model_serialization/) ->

---
