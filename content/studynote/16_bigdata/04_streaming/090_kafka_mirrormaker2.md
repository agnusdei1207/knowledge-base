---
title: "090. Kafka Mirrormaker2"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
---

## 핵심 인사이트 (3줄 요약)

- **본질**: [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) MirrorMaker 2 (MM2, [카프카](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 미러메이커 2)는 [Apache Kafka](/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) 2.4+부터 도입된 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect 기반의 클러스터 간 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 도구로, 양방향(Bidirectional) [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), 오프셋 변환(Offset Translation), 토픽 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)을 지원하여 [재해 복구](/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/)([DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/), Disaster [Recovery](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/))와 지리적 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 배포의 표준 솔루션이다.
- **가치**: 레거시 MirrorMaker 1은 오프셋 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)가 없어 장애 시 Consumer 위치를 잃었지만, MM2는 오프셋을 자동으로 변환·저장하여 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 전환 후에도 Consumer가 처리 위치를 유지하고 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 재처리를 최소화한다.
- **판단 포인트**: MM2는 단순 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)가 아니라 "[Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)-Passive([단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/))"와 "[Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)-[Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)(양방향)"를 모두 지원하므로 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 요구사항([RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/), [RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/))과 지역별 독립 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 필요 여부에 따라 토폴로지를 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1. 클러스터 간 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)가 필요한 이유

단일 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 클러스터는 다음 시나리오에 취약하다.

| 시나리오 | 문제 | 해결책 |
|:---|:---|:---|
| [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 장애 | 단일 클러스터 = [단일 장애점](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) | [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 클러스터에 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) |
| 지역별 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 확장 | 글로벌 Consumer의 높은 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 지역 근접 클러스터 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) |
| 클러스터 분리 운영 | 개발/스테이징/프로덕션 격리 | 환경 간 선택적 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) |
| [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 업그레이드 | 무중단 마이그레이션 필요 | 신구 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 클러스터 병행 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) |

### 2. MirrorMaker 1의 한계와 MM2의 등장

| 항목 | MirrorMaker 1 | MirrorMaker 2 |
|:---|:---|:---|
| 기반 | 단순 Consumer/Producer | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect Framework |
| 오프셋 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) | ❌ 없음 | ✅ 자동 변환 및 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) |
| 양방향 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | ❌ 불가 | ✅ [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)-[Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) 지원 |
| 토픽 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | ❌ 수동 | ✅ 자동 |
| [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 | 제한적 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 활용 |

**📢 섹션 요약 비유**
> MM1은 "편지를 사람이 직접 복사해서 보내는 것"이고, MM2는 "자동 팩스 시스템"이다. MM2는 복사본에 원본 번호 매핑(오프셋 변환)까지 자동으로 처리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. MM2 아키텍처 구성

```
[Active-Passive DR 구성]

Primary Cluster (US-East)              Secondary Cluster (US-West, DR)
+--------------------------+           +--------------------------+
|  Topic: orders           |           |  Topic: us-east.orders   |
|  Partition 0: msg1..1000 |  MM2 복제 |  Partition 0: msg1..1000 |
|  Partition 1: msg2..800  | ---------->|  Partition 1: msg2..800  |
|  Consumer offset: 950    |           |  Consumer offset: 950    |
|                          |           |  (오프셋 변환 자동 저장)  |
+--------------------------+           +--------------------------+

[Active-Active 양방향 구성]
US-East <--------------------> US-East.us-west.events (접두사 자동 추가)
US-West <--------------------> US-West.us-east.events (무한 루프 방지)
```

### 2. MM2 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 예시

```properties
# MirrorMaker 2 설정 (mm2.properties)
clusters = primary, secondary

# 클러스터 접속 정보
primary.bootstrap.servers = primary-kafka:9092
secondary.bootstrap.servers = secondary-kafka:9092

# 복제 방향: primary -> secondary
primary->secondary.enabled = true
primary->secondary.topics = orders, transactions, events.*  # 복제할 토픽 패턴

# 토픽 자동 생성 활성화
sync.topic.configs.enabled = true
sync.topic.acls.enabled = true

# 복제 인자
replication.factor = 3

# 오프셋 동기화 주기
offset-syncs.topic.replication.factor = 3
```

### 3. 오프셋 변환(Offset Translation)

```
원본 클러스터 (Primary):
  orders 파티션 0: 오프셋 0~10,000

복제 클러스터 (Secondary):
  us-east.orders 파티션 0: 오프셋 0~10,000 (같음, 또는 다를 수 있음)

MM2가 저장하는 오프셋 변환 맵:
  Primary:orders:0:9500 -> Secondary:us-east.orders:0:9500

DR 전환 후 Consumer 재시작:
  원래 오프셋(9500) -> Secondary에서 9500 위치 -> 중단 없이 재시작!
```

### 4. 주요 내부 토픽

| 내부 토픽 | 용도 |
|:---|:---|
| `heartbeats` | 클러스터 간 연결 상태 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| `mm2-configs.secondary.internal` | [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 상태 저장 |
| `mm2-offsets.secondary.internal` | 오프셋 변환 맵 저장 |
| `mm2-status.secondary.internal` | [태스크](/studynote/02_operating_system/02_process_thread/150_task/) 상태 저장 |

**📢 섹션 요약 비유**
> MM2의 오프셋 변환은 "해외 이사 시 책 번호 매핑"이다. 원래 집(Primary)에서 책([메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지)에 번호(오프셋)를 매겼는데, 새 집(Secondary)에서 번호가 달라질 수 있다. MM2는 두 집의 번호 대조표(오프셋 변환 맵)를 자동으로 관리한다.

---

## Ⅲ. 비교 및 연결

### 1. [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 토폴로지 선택

| 토폴로지 | 구성 | 장점 | 단점 |
|:---|:---|:---|:---|
| [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)-Passive | Primary -> Secondary | 단순, 명확한 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 전환 | Secondary는 읽기 전용 |
| [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)-[Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) | 양방향 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | 지역별 독립 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 가능 | 루프 방지 로직 필요 |
| [Hub](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)-and-Spoke | 중앙 -> 다수 지역 | 중앙 집중식 관리 | 중앙 장애 시 전체 영향 |
| Fan-Out | 1 소스 -> N 대상 | 동일 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 다목적 활용 | [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 소모 |

### 2. [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) MirrorMaker 2 vs [Confluent](/studynote/12_it_management/02_itsm_itil/878_reinforcement_learning/) Replicator

| 항목 | MirrorMaker 2 ([오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)) | [Confluent](/studynote/12_it_management/02_itsm_itil/878_reinforcement_learning/) Replicator (상용) |
|:---|:---|:---|
| 라이선스 | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | 유료 ([Confluent](/studynote/12_it_management/02_itsm_itil/878_reinforcement_learning/) Enterprise) |
| 오프셋 변환 | ✅ | ✅ (더 세밀한 제어) |
| [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect 기본 | [Confluent](/studynote/12_it_management/02_itsm_itil/878_reinforcement_learning/) Control Center |
| [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) | 별도 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 필요 | 자동 통합 |

**📢 섹션 요약 비유**
> [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)-Passive는 "본사-지점 구조", [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)-Active는 "두 본사 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 운영"이다. 지점(Secondary)은 본사가 닫힐 때만 역할을 하지만, 두 본사는 항상 동시에 영업한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 1. [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 전환 절차

```
정상 운영:
  Primary - MM2 복제 ---> Secondary (읽기 전용)
  Consumer <- Primary 읽기

Primary 장애 발생:
1. Secondary의 오프셋 변환 맵 확인
2. Consumer 연결을 Secondary로 전환
3. 토픽 이름 변경: us-east.orders -> orders (Alias 설정)
4. Consumer 재시작 (오프셋 변환으로 처리 위치 복원)

Primary 복구 후:
5. 역방향 복제(Secondary -> Primary) 실행
6. 오프셋 재동기화 후 Primary 복귀
```

### 2. [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [ ] MM2 Connect Worker 수: 최소 3대 (HA 구성)
- [ ] [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 토픽 패턴 명확화 (전체 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) vs 선택 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/))
- [ ] 오프셋 변환 맵 저장 토픽의 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 인자 = 3
- [ ] [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 전환 훈련 주기적 수행 (실제 전환 없이는 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 불가)
- [ ] Consumer 코드에 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 클러스터 주소 자동 전환 로직 포함

**📢 섹션 요약 비유**
> [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 전환 훈련은 "화재 대피 훈련"과 같다. 실제 화재가 나기 전에 훈련해야 실전에서 당황하지 않는다. MM2 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)이 완벽해도 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 전환을 한 번도 안 해봤다면 실제 상황에서 실수가 발생한다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| [RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) 최소화 | 거의 실시간 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 최소화 |
| [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) 단축 | 오프셋 변환으로 빠른 Consumer 재시작 |
| 무중단 마이그레이션 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 업그레이드 시 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 운영 |
| 글로벌 확장 | 지역별 클러스터에 동일 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 제공 |

### 2. 결론

[Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) MirrorMaker 2는 엔터프라이즈 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 운영에서 <strong>DR과 글로벌 <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>의 핵심 인프라</strong>다. 기술사 답안에서는 MM1의 한계(오프셋 비동기화), MM2의 개선([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect 기반, 오프셋 변환), [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)-Passive vs [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)-[Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) 토폴로지 선택 기준, 그리고 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 전환 절차를 함께 서술하는 것이 핵심이다.

**📢 섹션 요약 비유**
> MirrorMaker 2는 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 센터의 자동 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 시스템"이다. 매 순간 원본 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 복사하고, 복사본 위치(오프셋)도 자동으로 매핑하여, 원본이 사라져도 복사본에서 정확히 어디서부터 계속할 수 있는지 알고 있다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect | 기반 프레임워크 | MM2는 Connect Connector로 구현 |
| [Consumer Lag](/studynote/16_bigdata/04_streaming/089_consumer_lag/) | [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 상태 측정 | [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) Lag = 원본과 복사본의 오프셋 차이 |
| [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) (Disaster [Recovery](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)) | 주요 목적 | [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)-Passive DR의 핵심 도구 |
| 오프셋 변환 | 핵심 기능 | [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 전환 후 Consumer 위치 복원 |
| [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/) | [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 단위 | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 단위로 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) |


### 📈 관련 키워드 및 발전 흐름도

```text
[단일 클러스터 Kafka — 하나의 데이터센터 내 메시지 브로커, 장애 시 단일 장애점]
    |
    v
[Kafka MirrorMaker 1 — 간단한 컨슈머+프로듀서 복제, 오프셋 변환 미지원]
    |
    v
[Kafka MirrorMaker 2 (MM2) — Kafka Connect 기반, 오프셋 변환·자동 토픽 동기화 지원]
    |
    v
[Active-Passive DR — MM2로 보조 클러스터를 원본과 동기화, 장애 시 Failover 전환]
    |
    v
[Active-Active 다중 리전 — 양방향 복제로 지역 간 고가용성 메시지 처리 아키텍처]
```

이 흐름은 단일 클러스터의 [단일 장애점](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 위험을 해소하기 위해 MirrorMaker 1에서 오프셋 변환과 자동 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)를 지원하는 MM2로 진화하고, [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)-Passive DR을 거쳐 완전한 [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)-[Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) 다중 리전 아키텍처로 발전하는 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 클러스터 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)의 핵심 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

[Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) MirrorMaker 2는 "중요 숙제의 사본을 만드는 자동 복사기"예요. 원본 공책(Primary 클러스터)의 내용을 실시간으로 사본 공책(Secondary 클러스터)에 복사하고, 어디까지 읽었는지(오프셋)도 기록해 둬요. 원본 공책이 불에 타도(Primary 장애) 사본 공책에서 읽던 곳부터 바로 이어서 공부할 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 90 / 262

<- **이전**: [14. Consumer Lag — Kafka 소비 지연 모니터링](/studynote/16_bigdata/04_streaming/089_consumer_lag/)
**다음**: [16. Amazon Kinesis Data Streams — AWS 관리형 스트리밍](/studynote/16_bigdata/04_streaming/091_amazon_kinesis/) ->

---
