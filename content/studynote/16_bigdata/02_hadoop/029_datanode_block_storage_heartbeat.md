---
title: "029. Datanode Block Storage Heartbeat"
date: "2026-03-04"
tags:
  - "hadoop"
  - "studynote-bigdata"
weight: 29
---
## 핵심 인사이트 (3줄 요약)
- **HDFS의 일꾼(Worker)**: [데이터노드](/studynote/14_data_engineering/01_infrastructure/015_datanode/)([DataNode](/studynote/14_data_engineering/01_infrastructure/015_datanode/))는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 블록(Block) 단위로 로컬 디스크에 직접 저장하고 관리하는 물리적 서버 노드입니다.
- **상태 보고 (Heartbeat)**: [네임노드](/studynote/14_data_engineering/01_infrastructure/014_namenode/)([NameNode](/studynote/14_data_engineering/01_infrastructure/014_namenode/))에게 주기적으로 하트비트와 블록 리포트를 전송하여, 자신의 생존 여부와 저장된 블록의 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 보고합니다.
- <strong>클라이언트 <a href="/studynote/02_operating_system/02_process_thread/120_direct_communication/">직접 통신</a></strong>: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 작업 시 [네임노드](/studynote/14_data_engineering/01_infrastructure/014_namenode/)는 위치 정보만 알려주고, 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송은 클라이언트와 [데이터노드](/studynote/14_data_engineering/01_infrastructure/015_datanode/) 간에 직접 이루어져 병목을 방지합니다.

### Ⅰ. 개요 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
HDFS는 [마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터-슬레이브 아키텍처를 가집니다. [마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터인 [네임노드](/studynote/14_data_engineering/01_infrastructure/014_namenode/)가 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)를 관리한다면, 슬레이브인 수많은 [데이터노드](/studynote/14_data_engineering/01_infrastructure/015_datanode/)는 기가바이트에서 테라바이트에 이르는 거대 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 128MB(기본값)의 블록으로 쪼개어 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 보관합니다. 이는 저가의 범용 서버(Commodity Hardware)를 수평 확장([Scale-out](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))하여 대규모 저장소를 구축하기 위한 핵심 구성 요소입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
[데이터노드](/studynote/14_data_engineering/01_infrastructure/015_datanode/)는 [네임노드](/studynote/14_data_engineering/01_infrastructure/014_namenode/)의 지시에 따라 블록의 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 삭제, [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)를 수행합니다.

```text
[ DataNode Internal & Communication Architecture ]

1. Block Storage: Stores data as local files (blk_ID) + Checksum (.meta).
2. Communication Loop:
   - Heartbeat: Every 3 seconds (Survival check).
   - Block Report: Every hour (Full list of blocks held).

[ Diagram: Data Write Pipeline ]
   [ Client ] ----(1. Get Locations)----> [ NameNode ]
       |                                      |
       | <----(2. DN1, DN2, DN3)--------------+
       |
       +----(3. Write Block)----> [ DataNode 1 ]
                                      |
                               (4. Replication)
                                      |
                                 [ DataNode 2 ] ----> [ DataNode 3 ]
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
[네임노드](/studynote/14_data_engineering/01_infrastructure/014_namenode/)와 [데이터노드](/studynote/14_data_engineering/01_infrastructure/015_datanode/)의 역할을 명확히 비교합니다.

| 비교 항목 | [네임노드](/studynote/14_data_engineering/01_infrastructure/014_namenode/) ([NameNode](/studynote/14_data_engineering/01_infrastructure/014_namenode/)) | [데이터노드](/studynote/14_data_engineering/01_infrastructure/015_datanode/) ([DataNode](/studynote/14_data_engineering/01_infrastructure/015_datanode/)) |
| :--- | :--- | :--- |
| **역할** | 관리자 (Manager) | 실무자 (Worker) |
| **저장 내용** | [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) ([파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 목록, 위치) | <strong>실제 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 블록</strong> |
| **메모리 vs 디스크** | RAM 위주 (빠른 조회) | <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/">HDD</a>/<a href="/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/">SSD</a> 위주 (대용량 저장)</strong> |
| **수량** | 단일 또는 소수(HA) | <strong>수십~수만 대 (<a href="/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/">Scale-out</a>)</strong> |
| **장애 영향** | 전체 시스템 마비 ([SPOF](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)) | 해당 노드의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유실 ([복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)로 해결) |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
1. **디스크 밸런싱 (Balancer)**: 특정 [데이터노드](/studynote/14_data_engineering/01_infrastructure/015_datanode/)에 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 쏠릴 경우 `hdfs balancer` 명령을 통해 클러스터 전체의 디스크 사용률을 균등하게 맞춰야 합니다.
2. **배드 블록 관리**: 하드웨어 수명이 다해 발생하는 [체크섬](/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/)([Checksum](/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/)) 오류를 감지하면, [네임노드](/studynote/14_data_engineering/01_infrastructure/014_namenode/)는 즉시 다른 건강한 노드에서 해당 블록을 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)하도록 지시합니다.
3. **기술사적 판단**: [데이터노드](/studynote/14_data_engineering/01_infrastructure/015_datanode/)는 저가형 서버를 사용하므로 '장애는 일상'이라는 전제하에 설계되었습니다. 따라서 하드웨어 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)보다는 노드 대수를 늘려 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))을 확보하는 것이 경제적/기술적 정답입니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
[데이터노드](/studynote/14_data_engineering/01_infrastructure/015_datanode/)는 빅데이터 저장의 물리적 토대입니다. 최근에는 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 환경에 맞춰 '컴퓨팅과 스토리지의 분리'가 대세가 되면서, S3 같은 객체 스토리지가 [데이터노드](/studynote/14_data_engineering/01_infrastructure/015_datanode/)의 역할을 일부 대체하기도 하지만, [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화가 필요한 대규모 [하둡](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 클러스터에서는 여전히 [데이터노드](/studynote/14_data_engineering/01_infrastructure/015_datanode/)의 지역성(Locality) 기반 연산이 압도적인 효율을 제공합니다.

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념**: [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/), [분산 파일 시스템](/studynote/02_operating_system/09_file_system/553_distributed_file_system/), [하둡 에코시스템](/studynote/13_cloud_architecture/04_devops_observability/211_hadoop_ecosystem_mapreduce/)
- <strong><a href="/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a> 개념</strong>: 블록(Block), 하트비트(Heartbeat), [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)([Replication](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/))
- **관련 기술**: Amazon S3 (객체 스토리지), Ceph

### 📈 관련 키워드 및 발전 흐름도

```text
[HDFS NameNode]
    |
    v
[DataNode]
    |
    v
[블록 저장]
    |
    v
[Heartbeat]
    |
    v
[HA]
```

NameNode와 DataNode의 역할 분담과 Heartbeat 기반 상태 감지가 [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 고가용성으로 발전하는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
1. 아주 커다란 도서관에서 [네임노드](/studynote/14_data_engineering/01_infrastructure/014_namenode/)가 '책 목록'을 적은 장부를 든 사서 선생님이라면, [데이터노드](/studynote/14_data_engineering/01_infrastructure/015_datanode/)는 '책'이 꽂혀 있는 책장들이에요.
2. 책장이 너무 많아서 학교 운동장만큼 넓지만, [데이터노드](/studynote/14_data_engineering/01_infrastructure/015_datanode/)들은 선생님께 "저 여기 잘 있어요!"라고 계속 인사를 해요.
3. 우리가 책을 읽고 싶을 때 사서 선생님께 물어보면, 선생님은 책이 있는 책장 번호를 알려주고 우리는 거기서 직접 책을 꺼내 봐요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 29 / 262

<- **이전**: [06. Apache Tez](/studynote/16_bigdata/02_hadoop/028_apache_tez/)
**다음**: [08. 랙 인지 (Rack Awareness) - 물리적 장애 격리를 위한 데이터 복제 전략](/studynote/16_bigdata/02_hadoop/030_rack_awareness_fault_tolerance_topology/) ->

---
