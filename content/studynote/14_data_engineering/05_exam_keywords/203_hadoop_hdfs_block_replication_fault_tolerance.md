+++
title = "203. 하둡 HDFS (Hadoop Distributed File System) 블록 복제 내결함성"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) ([Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [Distributed File System](/knowledge-base/studynote/02_operating_system/09_file_system/553_distributed_file_system/))는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 고정 크기 블록(128MB)으로 분할하고, 각 블록을 여러 DataNode에 자동 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)(기본 3회)하여, 범용 하드웨어 위에서 페타바이트급 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장을 실현한다.
> 2. **가치**: 블록 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)와 [랙 인지](/knowledge-base/studynote/14_data_engineering/01_infrastructure/017_rack_awareness/)([Rack Awareness](/knowledge-base/studynote/14_data_engineering/01_infrastructure/017_rack_awareness/)) 배치를 통해 단일 노드 또는 랙 단위 장애에도 무중단 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근을 보장하며, MapReduce의 [데이터 지역성](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/)([Data Locality](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/))을 활용해 네트워크 전송 없이 처리한다.
> 3. **판단 포인트**: 기술사 논술에서는 NameNode의 메모리 내 [메타데이터 관리](/knowledge-base/studynote/16_bigdata/10_governance/203_metadata_management/) 한계, 블록 크기 선택 기준(대용량 순차 접근 최적화), [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 계수와 저장 비용 트레이드오프를 명확히 서술해야 한다.

---

## Ⅰ. 개요 및 필요성

### [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)([Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)) 등장 배경

2003~2006년 구글이 발표한 세 편의 논문 — GFS (Google [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) System), [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/), BigTable — 이 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)의 탄생 기반이 되었다. 야후(Yahoo)의 더그 커팅(Doug Cutting)이 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)로 구현한 HDFS는 GFS의 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 대체제이다.

| 구글 논문 | 발표 연도 | [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 구현체 |
|:---|:---|:---|
| GFS (Google [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) System) | 2003 | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) |
| [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) | 2004 | [Hadoop MapReduce](/knowledge-base/studynote/07_enterprise_systems/06_exam_summary/395_hadoop_mapreduce_disk_bottleneck/) |
| BigTable | 2006 | Apache [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/) |

### [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 설계 철학

HDFS는 "고가 하드웨어를 믿지 말라"는 철학에서 출발한다. 수천 대의 범용(Commodity) 서버를 묶어, 어느 서버가 장애를 일으켜도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 손실되지 않도록 설계되었다.

```
HDFS 설계 원칙
+--------------------------------------------------------+
|  원칙 1: 하드웨어 장애는 예외가 아니라 정상 상황이다    |
|  원칙 2: 대용량 파일 순차 접근에 최적화 (스트리밍 읽기) |
|  원칙 3: Write-Once-Read-Many (쓰기 1회, 읽기 다수)     |
|  원칙 4: 범용 하드웨어로 구성 (저비용 Scale-Out)        |
+--------------------------------------------------------+
```

📢 **섹션 요약 비유**: HDFS는 "클라우드 이전 시대의 구글 드라이브"다. [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 하나를 3군데 복사해서 저장하기 때문에, 내 컴퓨터가 고장나도 다른 컴퓨터에서 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 찾을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 아키텍처: NameNode와 [DataNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/015_datanode/)

HDFS는 마스터-슬레이브(Master-Slave) 아키텍처를 따른다.

```
HDFS 전체 아키텍처
+------------------------------------------------------------+
|                         클라이언트                          |
+---------------------------+--------------------------------+
                            | ① 파일 위치 요청
                            v
+----------------------------------------------------------+
|                      NameNode (1대)                       |
|  - 파일 시스템 네임스페이스 (트리 구조)                    |
|  - 파일 ↔ 블록 매핑 (메모리 내 유지)                      |
|  - 블록 ↔ DataNode 위치 매핑 (FsImage + EditLog)          |
+-------+----------------------+---------------------------+
        | ② 블록 위치 응답     | 하트비트/블록 리포트
        |                      v
        |          +---------------------+
        |          | Secondary NameNode  |
        |          | (체크포인팅 전용)    |
        |          +---------------------+
        |
        v ③ 직접 데이터 접근
+-----------------------------------------------------------+
|                     DataNode 클러스터                      |
|  +---------+   +---------+   +---------+   +---------+  |
|  |DataNode1|   |DataNode2|   |DataNode3|   |DataNode4|  |
|  | Blk A1  |   | Blk A2  |   | Blk A3  |   | Blk B1  |  |
|  | Blk C1  |   | Blk B2  |   | Blk C2  |   | Blk B3  |  |
|  +---------+   +---------+   +---------+   +---------+  |
+-----------------------------------------------------------+
```

| [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) | 역할 | 핵심 특성 |
|:---|:---|:---|
| [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 [메타데이터 관리](/knowledge-base/studynote/16_bigdata/10_governance/203_metadata_management/) | 전체 네임스페이스를 RAM에 유지 (GB 단위) |
| [DataNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/015_datanode/) | 실제 블록 저장·[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 로컬 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)시스템에 블록 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 저장 |
| Secondary [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) | FsImage [체크포인팅](/knowledge-base/studynote/16_bigdata/03_spark/071_checkpointing/) | EditLog 병합으로 [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) 부담 경감 (HA 대체 아님!) |
| Standby [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) | HA (High [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) 구성 | [Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) 장애 시 자동 전환 |

### 블록 단위 저장 (Block-Based Storage)

HDFS는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 **128MB** (기본값) 블록으로 분할하여 저장한다.

```
파일 -> 블록 분할 예시
+---------------------------------------------------------+
|  파일: movie.mp4 (384MB)                                 |
|                                                         |
|  +--------------+ +--------------+ +--------------+     |
|  |  블록 A       | |  블록 B       | |  블록 C       |     |
|  |  128MB        | |  128MB        | |  128MB        |     |
|  +------+-------+ +------+-------+ +------+-------+     |
|         | 복제 ×3        | 복제 ×3        | 복제 ×3      |
|  DN1,DN2,DN3       DN2,DN3,DN4       DN1,DN3,DN4        |
+---------------------------------------------------------+
```

| 블록 크기 | 이유 | 트레이드오프 |
|:---|:---|:---|
| 128MB (기본값) | 대용량 순차 접근 최적화, [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 감소 | 소규모 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에는 낭비 |
| 64MB (이전 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)) | 구버전 기본값 | 현재는 권장하지 않음 |
| 256MB (대용량) | 매우 큰 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 처리 최적화 | [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) 메모리 더 절약 |

### [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 계수 3과 [랙 인지](/knowledge-base/studynote/14_data_engineering/01_infrastructure/017_rack_awareness/) 배치

HDFS의 기본 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 계수([Replication Factor](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/))는 3이며, [랙 인지](/knowledge-base/studynote/14_data_engineering/01_infrastructure/017_rack_awareness/)([Rack Awareness](/knowledge-base/studynote/14_data_engineering/01_infrastructure/017_rack_awareness/)) 정책으로 배치한다.

```
랙 인지 복제 배치 정책
+-------------------------------------------------------------+
|  데이터센터                                                   |
|                                                             |
|  +------------ Rack 1 ------------+  +--- Rack 2 --------+  |
|  |  DataNode1 <--- 복제본 1 (첫번째)|  |  DataNode3 <--- 복제본 3|  |
|  |  DataNode2 <--- 복제본 2 (같은 랙)|  |                   |  |
|  +---------------------------------+  +-------------------+  |
|                                                             |
|  정책: 2개는 같은 랙, 1개는 다른 랙                          |
|  -> 랙 내 스위치 장애 시에도 다른 랙 복제본으로 서비스 가능    |
+-------------------------------------------------------------+
```

| [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 배치 | 이유 |
|:---|:---|
| 1번 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/): [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 클라이언트와 같은 랙 [DataNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/015_datanode/) | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 |
| 2번 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/): 같은 랙의 다른 [DataNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/015_datanode/) | 랙 내 네트워크 활용 |
| 3번 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/): 다른 랙의 [DataNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/015_datanode/) | 랙 단위 장애 대응 |

📢 **섹션 요약 비유**: 블록 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)는 "중요한 서류를 사무실 서랍([복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)1), 회의실 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)함([복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)2), 다른 건물 창고([복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)3)에 나눠 보관"하는 것이다. 건물 하나가 불이 나도 다른 건물 창고에서 꺼낼 수 있다.

---

## Ⅲ. 비교 및 연결

### 내결함성 메커니즘 상세

| 장애 유형 | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 감지 방법 | [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 방법 |
|:---|:---|:---|
| [DataNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/015_datanode/) 장애 | 하트비트 10분 무응답 | NameNode가 해당 블록 재복제 지시 |
| 블록 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손상 | [체크섬](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/)([Checksum](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/)) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 다른 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본으로 대체 후 재복제 |
| 랙 장애 | 블록 리포트 누락 | 다른 랙의 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본 활용 |
| [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) 장애 | [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 기반 모니터링 | Standby [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) 자동 전환 (HA) |

### [데이터 지역성](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/) ([Data Locality](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/))

MapReduce는 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 컴퓨팅으로 이동"시키는 대신 "컴퓨팅을 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 이동"시키는 [데이터 지역성](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/) 원칙을 따른다.

```
데이터 지역성 원칙
+---------------------------------------------------------+
|  전통 방식 (데이터 -> 컴퓨팅):                            |
|  DataNode --[네트워크]---> 중앙 처리 서버 (병목 발생)     |
|                                                         |
|  MapReduce 방식 (컴퓨팅 -> 데이터):                       |
|  DataNode --[로컬 실행]---> Map Task 직접 실행            |
|  네트워크 전송 없음 -> 처리 속도 대폭 향상                 |
+---------------------------------------------------------+
```

| 지역성 레벨 | 설명 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) |
|:---|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 로컬 ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)-Local) | Map Task와 블록이 동일 노드 | 최고 (로컬 디스크 읽기) |
| 랙 로컬 (Rack-Local) | 같은 랙의 다른 노드 | 중간 (내부 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 경유) |
| 오프 랙 (Off-Rack) | 다른 랙의 노드 | 최저 (WAN급 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)) |

### [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) vs 기타 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)시스템 비교

| 항목 | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) | GFS (Google [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) System) | Amazon S3 |
|:---|:---|:---|:---|
| 접근 방식 | POSIX 유사 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | 독점 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | [REST API](/knowledge-base/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/) |
| [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | [완화된 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/412_relaxed_consistency/) | 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |
| 적합 사례 | [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/) ([MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)) | 구글 내부 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 오브젝트 저장, 클라우드 DL |
| [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수정 | Append 전용 | Append 전용 | 덮어쓰기 가능 |

📢 **섹션 요약 비유**: HDFS의 [데이터 지역성](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/)은 "요리사가 재료 창고 옆에서 요리하는 것"이다. 재료를 멀리 있는 주방으로 옮기는 대신(네트워크 전송), 창고 바로 옆에 조리대를 설치해(Map Task를 DataNode에서 실행) 이동 시간을 없앤다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 운영 핵심 파라미터

| 파라미터 | 기본값 | 튜닝 방향 | 이유 |
|:---|:---|:---|:---|
| [dfs](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/034_dfs/).[replication](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | 3 | 2 (개발/테스트) | 저장 비용 절감 |
| [dfs](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/034_dfs/).block.size | 128MB | 256MB (대용량 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)) | [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 감소 |
| [dfs](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/034_dfs/).[namenode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/).handler.count | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) | CPU 코어 수 × 20 | [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) [RPC](/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/) 병목 해소 |
| [dfs](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/034_dfs/).[datanode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/015_datanode/).du.reserved | 0 | 10GB | [DataNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/015_datanode/) 디스크 여유 공간 확보 |

### 소규모 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 문제 ([Small File Problem](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/269_small_file_problem_data_lakehouse/))

HDFS의 가장 큰 실무 문제 중 하나는 수백만 개의 소규모 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이다. 각 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)마다 최소 1개의 블록 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)가 [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) 메모리를 차지하기 때문이다.

```
소규모 파일 문제
+---------------------------------------------------------+
|  1KB 파일 1,000만 개 저장 시:                            |
|  -> NameNode 메모리: 약 150 bytes × 10,000,000 = 1.5GB   |
|  -> 실제 데이터: 10GB (전체의 6.7%)                       |
|  -> NameNode 메모리가 데이터보다 더 빨리 소진됨!           |
|                                                         |
|  해결책:                                                 |
|  - HAR (Hadoop Archive): 소규모 파일 묶음 저장           |
|  - SequenceFile: 키-값 쌍으로 소규모 파일 병합           |
|  - S3 + Parquet: 소규모 파일을 컬럼형으로 병합 저장      |
+---------------------------------------------------------+
```

### 기술사 논술 핵심 포인트

1. <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/">NameNode</a> <a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/">SPOF</a></strong>: HDFS의 근본 약점은 단일 [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/). [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 2.x부터 HA (High [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) + ZooKeeper로 해결
2. <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/">복제</a> vs 이레이저 코딩</strong>: [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 계수 3은 200% 스토리지 오버헤드. [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 3.x의 Erasure Coding으로 50% 이내로 줄임
3. <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/">데이터 지역성</a> 저하</strong>: 클라우드 환경(S3 분리)에서는 HDFS의 지역성 장점이 사라짐 -> 컬럼형 포맷([Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)) + 파티셔닝으로 보완

📢 **섹션 요약 비유**: [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 운영의 핵심 딜레마는 "[복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)를 많이 할수록 안전하지만 저장 공간이 낭비된다"는 것이다. 마치 중요한 문서를 복사해서 여러 금고에 넣을수록 안전하지만, 금고 임대료가 늘어나는 것과 같다. Erasure Coding은 "문서를 조각내서 XOR 패리티로 저장"해 금고 수를 줄이는 방법이다.

---

## Ⅴ. 기대효과 및 결론

### [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 도입 효과

| 효과 영역 | 수치 예시 | 설명 |
|:---|:---|:---|
| 저장 비용 | 기존 [SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 대비 80% 절감 | 범용 [HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 서버 활용 |
| [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) | 99.9% (3 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 기준) | 노드 장애 자동 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
| 처리 병렬성 | 선형 확장 | 노드 추가 = [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 비례 증가 |
| 확장성 | 수천 노드, 수백 PB | 야후 등 실제 수만 노드 운영 사례 |

### HDFS의 한계와 발전 방향

| 한계 | 발전 방향 |
|:---|:---|
| [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) | HA [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) + [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) [Federation](/knowledge-base/studynote/09_security/11_iam_access_control/543_federation/) |
| 소규모 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 취약 | [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)/ORC + [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) |
| 높은 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 오버헤드 | [Erasure Coding](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/681_erasure_coding/) (RS-6-3 등) |
| 클라우드 S3 분리 | 컴퓨팅-스토리지 분리 아키텍처([Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/), Iceberg) |

### 결론

HDFS는 빅데이터 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장의 기준을 세운 혁신적 시스템이지만, 클라우드 시대로 전환되며 컴퓨팅-스토리지 분리 아키텍처에 그 역할을 넘겨주고 있다. 그러나 HDFS의 핵심 개념(블록 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/), [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), [데이터 지역성](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/))은 현대의 오브젝트 스토리지와 [오픈 테이블 포맷](/knowledge-base/studynote/14_data_engineering/01_infrastructure/054_open_table_format_iceberg_delta_hudi/)(Iceberg, [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/))에 여전히 계승되어 있다.

📢 **섹션 요약 비유**: HDFS는 "빅데이터 시대의 기초 공사"다. 현대 빌딩(클라우드 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼)은 더 세련됐지만, 그 기초([분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장·[복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)·지역성 원칙)는 HDFS에서 가져온 것이다.

---

### 📌 관련 개념 맵
| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 구성 요소 | [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 중앙 관리자 |
| 구성 요소 | [DataNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/015_datanode/) | 실제 블록 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장·[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 노드 |
| 구성 요소 | Secondary [NameNode](/knowledge-base/studynote/14_data_engineering/01_infrastructure/014_namenode/) | [체크포인팅](/knowledge-base/studynote/16_bigdata/03_spark/071_checkpointing/) 전용 (HA가 아님) |
| 연관 기술 | [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) | [데이터 지역성](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/) 활용한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 |
| 상위 개념 | [YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/) | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 위의 리소스 관리 레이어 |
| 이론적 배경 | GFS (Google [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) System) | HDFS의 원조 논문 |
| 발전 방향 | [Apache Iceberg](/knowledge-base/studynote/16_bigdata/07_data_lake/148_apache_iceberg/) / [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/) | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 한계를 극복한 [오픈 테이블 포맷](/knowledge-base/studynote/14_data_engineering/01_infrastructure/054_open_table_format_iceberg_delta_hudi/) |
| 보완 기술 | [Erasure Coding](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/681_erasure_coding/) | [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 오버헤드 감소 기술 |

### 👶 어린이를 위한 3줄 비유 설명
1. HDFS는 "레고 블록으로 엄청 큰 성을 쌓는 것"이에요. 큰 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 하나를 128MB 블록 조각으로 나눠서, 여러 컴퓨터에 나눠 보관해요.

### 📈 관련 키워드 및 발전 흐름도

```text
단일 디스크 저장 -> 용량 · 내구성 한계
    |
    v
HDFS (Hadoop Distributed File System)
    +-► 블록 분할 (128MB) + 3중 복제 (Replication Factor)
    +-► NameNode: 메타데이터 관리 (파일->블록 맵)
    +-► DataNode: 실제 블록 저장
    |
    v
Hadoop 2.x: HA NameNode · Federation
    |
    v
클라우드 오브젝트 스토리지: S3 · GCS (HDFS 대체)
```
2. 블록마다 3개씩 복사본을 만들어두기 때문에, 컴퓨터 한 대가 고장나도 다른 곳에서 레고 조각을 꺼낼 수 있어요.
3. NameNode는 "어떤 컴퓨터에 어떤 레고 조각이 있는지 기억하는 목록 책"이고, DataNode는 "실제로 레고를 보관하는 창고"예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 203 / 258

<- **이전**: [202. 스케일 아웃 (Scale-Out) 분산 수평 확장](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)
**다음**: [204. NameNode 메타데이터와 MapReduce 디스크 병목 SPOF 극복](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/204_namenode_metadata_mapreduce_disk_bottleneck/) ->

---
