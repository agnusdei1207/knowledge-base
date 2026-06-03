+++
title = "204. NameNode 메타데이터와 MapReduce 디스크 병목 SPOF 극복"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) NameNode는 전체 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)시스템 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 RAM에 단독으로 유지하는 구조로 인해 [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) (Single Point of Failure)와 메모리 확장 한계를 내포하며, MapReduce는 Shuffle 단계의 반복적 디스크 I/O (Input/Output)가 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목이 된다.
> 2. **가치**: HA (High [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) + [YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/) (Yet Another Resource Negotiator) 전환으로 SPOF를 해소하고, Spark의 인메모리(In-Memory) 처리로 디스크 병목을 근본적으로 극복했다.
> 3. **판단 포인트**: 기술사 논술에서는 "어떤 문제가 있었고, 어떤 기술적 진화가 이루어졌으며, 남은 트레이드오프는 무엇인가"를 구조적으로 서술하는 것이 고득점의 핵심이다.

---

## Ⅰ. 개요 및 필요성

### NameNode의 구조적 취약점

HDFS의 NameNode는 두 가지 근본적 한계를 가진다.

```
NameNode 구조적 한계
┌─────────────────────────────────────────────────────────┐
│  NameNode (단일 서버)                                    │
│  ┌─────────────────────────────────────────────────┐    │
│  │ FsImage (파일시스템 스냅샷) + EditLog (변경 로그) │    │
│  │ 모두 메모리에 상주 → RAM 한계에 수억 파일 저장 불가│    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  문제 1: SPOF — NameNode 장애 = 전체 HDFS 접근 불가     │
│  문제 2: 메모리 확장 한계 — 파일 수 증가 시 RAM 소진      │
└─────────────────────────────────────────────────────────┘
```

### MapReduce의 디스크 I/O 병목

MapReduce는 각 Job 단계마다 결과를 [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/)(디스크)에 저장하고, 다음 단계에서 다시 읽는 구조다. 반복적 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)([머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/))에서 특히 치명적이다.

```
MapReduce 다단계 처리의 디스크 I/O
┌────────────────────────────────────────────────────────────┐
│ Job 1: Map → [디스크 쓰기] → Reduce → [HDFS 저장]          │
│         ↓                                                  │
│ Job 2: [HDFS 읽기] → Map → [디스크 쓰기] → Reduce → [HDFS] │
│         ↓                                                  │
│ Job N: [HDFS 읽기] → Map → ... (반복할수록 I/O 누적)        │
│                                                            │
│ K-Means 100 이터레이션 = 200회 HDFS 읽기+쓰기 발생!         │
└────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: MapReduce의 디스크 병목은 "계산할 때마다 종이에 답을 써서 금고에 넣고, 다음 계산 시 금고에서 꺼내 다시 보는 것"이다. 100번 계산하면 200번 금고를 여닫아야 한다. 이걸 머릿속(메모리)에서 전부 처리하면 훨씬 빠르다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) [메타데이터 관리](/knowledge-base/studynote/16_bigdata/10_governance/203_metadata_management/) 메커니즘

```
NameNode 메타데이터 흐름
┌────────────────────────────────────────────────────────────┐
│  NameNode RAM                                              │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ FsImage (최신 스냅샷) + EditLog (최신 변경사항) 병합  │ │
│  │ → 전체 파일시스템 트리 메모리 유지                    │ │
│  └──────────────────────────────────────────────────────┘ │
│               │                    │                       │
│               ▼                    ▼                       │
│  ┌──────────────────┐  ┌──────────────────────────────┐   │
│  │   FsImage (디스크) │  │  EditLog (디스크)              │   │
│  │   (체크포인트)     │  │  (모든 변경사항 순차 기록)      │   │
│  └──────────────────┘  └──────────────────────────────┘   │
│               │                                            │
│               ▼                                            │
│  Secondary NameNode (체크포인팅):                          │
│  FsImage + EditLog 병합 → 새 FsImage 생성 → NameNode 전송 │
└────────────────────────────────────────────────────────────┘
```

| [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) | 역할 | 중요 주의사항 |
|:---|:---|:---|
| FsImage | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)시스템 전체 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) | 체크포인트 시점의 최신 상태 |
| EditLog | 체크포인트 이후 모든 변경사항 기록 | 너무 커지면 재시작 시 재생 시간 증가 |
| Secondary [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) | FsImage + EditLog [체크포인팅](/knowledge-base/studynote/16_bigdata/03_spark/071_checkpointing/) | **HA 대체가 아님!** — 장애 시 수동 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 필요 |
| Standby [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) (HA) | [Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) NameNode의 [Hot Standby](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/457_hot_standby/) | JournalNode 클러스터로 EditLog 공유 |

### [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 해결: HA [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) 아키텍처

[Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 2.x부터 도입된 HA (High [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) NameNode는 [Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)/Standby [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 구조를 제공한다.

```
HA NameNode 아키텍처
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  ┌──────────────────┐       ┌──────────────────────────┐  │
│  │  Active NameNode │       │   Standby NameNode       │  │
│  │  (읽기/쓰기)      │       │   (편집로그 동기 추적)    │  │
│  └────────┬─────────┘       └───────────┬──────────────┘  │
│           │  EditLog 쓰기               │ EditLog 읽기     │
│           ▼                            ▼                  │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  JournalNode 클러스터 (3대 이상, Quorum 방식)          │  │
│  └─────────────────────────────────────────────────────┘  │
│                         │                                  │
│                         ▼                                  │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  ZooKeeper 클러스터 (3/5대)                           │  │
│  │  → Active/Standby 역할 선출 (Failover Controller)    │  │
│  └─────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

| 방식 | 구성 | 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | 한계 |
|:---|:---|:---|:---|
| Secondary [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) | Single [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) + Secondary | 수동 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 가능 | [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 존재 |
| HA [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) | [Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) + Standby + JournalNode + [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) | 자동 [Failover](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/) (30~60초) | 복잡성 증가 |
| [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) [Federation](/knowledge-base/studynote/09_security/11_iam_access_control/543_federation/) | [네임스페이스](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/) 분리 다중 [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) | 독립적 장애 격리 | [네임스페이스](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/) 간 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 이동 불가 |

### [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) vs [YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/) 아키텍처 발전

```
Hadoop 1.x (MapReduce v1) vs Hadoop 2.x (YARN)
┌─────────────────────────────────────────────────────────────┐
│  Hadoop 1.x:                                                │
│  JobTracker (단일 마스터) ─── TaskTracker (슬레이브)          │
│  → JobTracker가 클러스터 관리 + 작업 스케줄링 모두 담당       │
│  → SPOF, Map/Reduce 작업만 지원                             │
│                                                             │
│  Hadoop 2.x (YARN):                                         │
│  ResourceManager (클러스터 자원) + ApplicationMaster (앱별)  │
│  → 역할 분리로 SPOF 개선, Spark/Tez/MPI 등 다중 프레임워크   │
└─────────────────────────────────────────────────────────────┘
```

| [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) | [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 1.x | [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 2.x ([YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/)) |
|:---|:---|:---|
| 클러스터 관리 | JobTracker ([SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)) | ResourceManager (HA 지원) |
| 작업 실행 | TaskTracker | NodeManager |
| 애플리케이션 관리 | JobTracker 내장 | ApplicationMaster (앱별 독립) |
| 지원 프레임워크 | MapReduce만 | Spark, Tez, MPI 등 |

📢 **섹션 요약 비유**: YARN으로의 전환은 "소방서장(JobTracker)이 화재 진압도 하고 소방차도 배치하고 인사 관리도 혼자 하던 것을 → 소방청장(ResourceManager)은 소방차만 배치하고, 각 사건 현장 지휘관(ApplicationMaster)이 현장을 직접 지휘하는 구조"로 바꾼 것이다.

---

## Ⅲ. 비교 및 연결

### Secondary [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) vs HA Standby [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/)

| 항목 | Secondary [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) | HA Standby [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) |
|:---|:---|:---|
| 주 역할 | [체크포인팅](/knowledge-base/studynote/16_bigdata/03_spark/071_checkpointing/) (FsImage + EditLog 병합) | Active의 [Hot Standby](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/457_hot_standby/) |
| [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 해결 | ❌ 해결 안 됨 | ✅ 자동 [Failover](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/) |
| [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) | 주기적 [체크포인팅](/knowledge-base/studynote/16_bigdata/03_spark/071_checkpointing/) | JournalNode 통한 실시간 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) |
| 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | 수동 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 최신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 가능 | [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 자동 전환 (30~60초) |
| 리소스 | 저사양 서버 가능 | Active와 동일 사양 필요 |

### [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 디스크 병목의 근본 원인과 Spark 해결

```
MapReduce vs Spark 처리 방식
┌─────────────────────────────────────────────────────────────┐
│  MapReduce (디스크 중심):                                    │
│  Input → [Map] → 디스크 → [Shuffle] → 디스크 → [Reduce]    │
│                                          → HDFS 저장        │
│                                                             │
│  Spark (메모리 중심):                                        │
│  Input → [RDD Transform1] → RAM → [RDD Transform2] → RAM   │
│        → [Action] → 최종 출력 (중간 결과는 메모리만!)         │
│                                                             │
│  성능 차이: 반복 알고리즘에서 Spark가 10~100배 빠름           │
└─────────────────────────────────────────────────────────────┘
```

| 항목 | [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) | [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) |
|:---|:---|:---|
| 중간 결과 저장 | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 디스크 | RAM (메모리) |
| 반복 처리 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 매 이터레이션마다 디스크 I/O | [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) 캐싱으로 재사용 |
| [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) | 분~시간 | 초~분 |
| 적합 워크로드 | 단순 배치 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) | 반복 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/), 스트리밍, SQL |

📢 **섹션 요약 비유**: MapReduce의 디스크 병목은 "수학 문제 풀 때마다 중간 계산을 지우고 종이에 받아쓰는 것"이고, Spark는 "계산기 메모리에 중간 값을 저장하고 바로 다음 계산에 사용하는 것"이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) HA 설계 시 고려사항

```
NameNode HA 설계 체크리스트
┌──────────────────────────────────────────────────────────┐
│  ✓ JournalNode: 3개 이상 (Quorum 방식, 과반수 쓰기 성공)  │
│  ✓ ZooKeeper: 3 또는 5개 (홀수 과반수 보장)               │
│  ✓ Fencing (펜싱): Split-Brain 방지                       │
│    - 네트워크 펜싱: 구 Active의 네트워크 격리              │
│    - STONITH: 구 Active 노드 강제 전원 차단                │
│  ✓ DNS/VIP: 클라이언트는 Active 위치를 투명하게 접근       │
└──────────────────────────────────────────────────────────┘
```

**Split-Brain 문제**: 두 NameNode가 모두 [Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) 상태를 주장하는 상황. 두 NameNode가 서로 다른 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 갱신하면 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)시스템 손상이 발생한다. Fencing (울타리치기) 메커니즘으로 반드시 방지해야 한다.

### [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 실무 최적화

| 최적화 방법 | 설명 | 개선 효과 |
|:---|:---|:---|
| Combiner 사용 | Map 결과를 로컬에서 사전 집계 | Shuffle [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 양 50~80% 감소 |
| [Compression](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/159_compression/) | Map 출력 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) (Snappy, LZ4) | I/O와 네트워크 전송 감소 |
| 파티셔너 최적화 | 사용자 정의 파티셔너로 균등 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) | 리듀서 스큐(Skew) 방지 |
| Speculative Execution | 느린 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 실행 | 스트래글러(Straggler) 문제 완화 |

### 기술사 논술 핵심 포인트

1. **[SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) vs 복잡성 트레이드오프**: HA 구성은 SPOF를 제거하지만, JournalNode·[ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/)·Fencing의 추가 운영 복잡성이 발생한다. 이를 명확히 인정하고 선택 기준을 제시할 것.
2. **Hadoop의 역할 변화**: [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)([On-Premise](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/))에서는 여전히 [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/)+YARN이 중심이지만, 클라우드에서는 컴퓨팅-스토리지 분리(S3+Spark)가 주류다. 이 전환의 의미를 설명할 수 있어야 한다.
3. **MapReduce의 현재 위치**: [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 자체는 느리지만, [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) on Tez / SparkSQL 등이 내부적으로 최적화된 실행 엔진을 사용하므로 "[MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) = [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/)"라는 오해를 하지 말 것.

📢 **섹션 요약 비유**: [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) HA는 "대통령과 부통령 제도"다. 대통령([Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/))이 쓰러지면 부통령(Standby)이 즉각 취임하지만, 전 대통령이 혼수상태에서 명령을 계속 내리는 혼란(Split-Brain)을 막으려면 헌법적 절차(Fencing)가 반드시 필요하다.

---

## Ⅴ. 기대효과 및 결론

### [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) HA와 [YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/) 도입 효과

| 영역 | 개선 전 ([Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 1.x) | 개선 후 ([Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 2.x) |
|:---|:---|:---|
| [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) | [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) ([단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)) | HA [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) (99.9% 이상) |
| 확장성 | 4,000 노드 한계 | [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) Federation으로 수만 노드 |
| 프레임워크 | [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 전용 | Spark, Tez, MPI 등 다중 지원 |
| 디스크 I/O | 모든 중간 결과 [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 저장 | [YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/) + Spark으로 메모리 처리 가능 |

### 결론

[NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) SPOF와 [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 디스크 병목은 [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 생태계의 성숙 과정에서 식별되고 해결된 대표적 기술 한계다. HA NameNode는 SPOF를 제거했고, YARN은 단일 프레임워크 의존성을 끊었으며, Spark는 디스크 병목을 메모리로 극복했다. 이 진화 과정은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서 "[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)"과 "[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)"이라는 두 가치를 점진적으로 달성하는 방식의 모범 사례다.

📢 **섹션 요약 비유**: HDFS의 발전 과정은 "자전거([MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)) → 오토바이([YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/) + [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)) → 자동차(Spark on [YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/))"의 진화다. 자전거도 목적지에는 도달하지만, 자동차는 더 빠르고 더 많은 짐을 실을 수 있다. 다만 자동차는 주차 공간(메모리)이 더 필요하다.

---

### 📌 관련 개념 맵
| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 문제 → 해결 | [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) → HA [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) | [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 기반 자동 [Failover](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/) |
| 문제 → 해결 | 디스크 병목 → [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) | 인메모리 [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) 처리 |
| 구성 요소 | JournalNode 클러스터 | HA [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) EditLog 공유 저장소 |
| 구성 요소 | [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) | [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) 리더 선출 조정자 |
| 관련 개념 | Split-Brain | 두 NameNode가 모두 [Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) 주장하는 이상 상태 |
| 발전 방향 | [YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/) (Yet Another Resource Negotiator) | [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 한계 극복 범용 자원 관리자 |
| 보완 기술 | [Apache Tez](/knowledge-base/studynote/16_bigdata/02_hadoop/028_apache_tez/) | MapReduce를 [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) 실행으로 최적화 |

### 👶 어린이를 위한 3줄 비유 설명
1. [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) SPOF는 "마을 지도를 딱 한 명이 갖고 있는 것"이에요. 그 사람이 아프면 아무도 창고 위치를 모르게 돼요.

### 📈 관련 키워드 및 발전 흐름도

```text
NameNode 단일 장애점 (SPOF)
    │
    ▼
HA NameNode: Active-Standby · JournalNode 동기화
    │
    ▼
MapReduce: Map → Shuffle → Reduce (디스크 기반)
    │ 디스크 I/O 병목
    ▼
Spark: 인메모리 처리 → 10~100배 성능 향상
```
2. HA NameNode는 "지도를 두 명이 갖고, 한 명이 아프면 다른 사람이 바로 지도를 꺼내는 것"이에요.
3. [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 디스크 병목은 "덧셈할 때마다 칠판에 지우고 다시 쓰는 것"인데, Spark는 "머릿속으로 연산해서 최종 답만 칠판에 쓰는 것"처럼 훨씬 빠르답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 204 / 258

← **이전**: [203. 하둡 HDFS (Hadoop Distributed File System) 블록 복제 내결함성](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/203_hadoop_hdfs_block_replication_fault_tolerance/)
**다음**: [205. 셔플·정렬 (Shuffle & Sort)과 YARN (Yet Another Resource Negotiator)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/205_shuffle_sort_yarn_resource_manager/) →

---
