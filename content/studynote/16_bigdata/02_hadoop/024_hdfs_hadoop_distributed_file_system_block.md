---
title: "Hdfs Hadoop Distributed File System Block"
date: "2026-03-04"
tags:
  - "hadoop"
  - "studynote-bigdata"
weight: 24
---
## 핵심 인사이트 (3줄 요약)
- <strong>초대용량 <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 스토리지</strong>: HDFS는 테라바이트/페타바이트 급의 거대한 단일 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 디스크 기본 128MB 블록 단위로 잘게 쪼개어 수백 대의 노드에 뿌려 저장하는 [분산 파일 시스템](/studynote/02_operating_system/09_file_system/553_distributed_file_system/)입니다.
- <strong>저비용 하드웨어 <a href="/studynote/04_software_engineering/06_software_architecture/352_defect_definition/">결함</a> 극복</strong>: 값싼 상용 서버(Commodity Hardware) 사용을 전제로 설계되어 언제든 디스크나 노드가 고장 날 수 있다고 가정하며, 이를 '3벌 블록 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)([Replication](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/))'를 통해 무정지로 자동 방어합니다.
- <strong><a href="/studynote/02_operating_system/10_security/590_worm/">WORM</a> (<a href="/studynote/01_computer_architecture/15_advanced_topics/693_worm_storage/">Write Once Read Many</a>) 특성</strong>: 스트리밍 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 지속적인 읽기 및 배치 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 연산에 최적화되어 있어, 한 번 쓰고 나면 내용의 일부분 변경은 불가능하고 덧붙이기(Append)만 가능한 구조입니다.

### Ⅰ. 개요 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
단일 디스크 드라이브 용량은 10TB 안팎에서 성장이 둔화되었지만 처리해야 할 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)와 영상 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 기하급수적으로 폭증했습니다. 이 물리적 한계를 부수기 위해 구글의 GFS(Google [File](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) System) 논문에 영감을 받아 탄생한 스토리지 기술이 HDFS입니다.
기존의 전통적 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이 트리 계층 구조의 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 내부에 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 페이로드를 품는 방식이었다면, HDFS는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 메타(이름, 권한)를 관리하는 중앙 통제 서버와 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록이 저장되는 수많은 말단 서버를 분리하는 과감한 네트워크 아키텍처를 채택했습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

HDFS는 [마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터-워커(Master-Worker) 아키텍처로 작동하며, [네임노드](/studynote/14_data_engineering/01_infrastructure/014_namenode/)와 다수의 [데이터노드](/studynote/14_data_engineering/01_infrastructure/015_datanode/)로 구성됩니다.

```text
+-------------------+             +-----------------------+
|    NameNode       |             |      DataNode 1       |
|  (Master Node)    |             |  (Worker Node)        |
| - Namespace/Meta  |<-- Heart -->| - Block A (128MB)     |
| - Block Map       |    beat     | - Block B (128MB)     |
+---------+---------+             +-----------------------+
          |
          | Read/Write Request
          v
+-------------------+             +-----------------------+
|     Client        |             |      DataNode 2       |
| (Application)     |<===========>|  (Worker Node)        |
| - File splitting  |  Data Flow  | - Block A (Replica)   |
+-------------------+             | - Block C (128MB)     |
                                  +-----------------------+
```

1. **블록(Block) 분할 (기본 128MB)**: 리눅스 기본 블록(4KB)보다 수만 배 거대한 사이즈. [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/)([Seek Time](/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/)) 비중을 줄이고 디스크 전송 속도에 연산 속도를 맞추기 위해 거대하게 설계되었습니다.
2. <strong><a href="/studynote/14_data_engineering/01_infrastructure/016_replication_factor/">복제</a> 계수 (<a href="/studynote/14_data_engineering/01_infrastructure/016_replication_factor/">Replication Factor</a> 3)</strong>: 원본 블록 A가 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되면, 동일 랙의 다른 노드에 1벌, 전혀 다른 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 전원을 쓰는 랙의 노드에 1벌을 복사([Rack Awareness](/studynote/14_data_engineering/01_infrastructure/017_rack_awareness/))하여 화재나 정전에도 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보존합니다.
3. **하트비트 (Heartbeat)**: [데이터노드](/studynote/14_data_engineering/01_infrastructure/015_datanode/)는 3초마다 [네임노드](/studynote/14_data_engineering/01_infrastructure/014_namenode/)에 생존 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 보냅니다. 10분 간 끊기면 [네임노드](/studynote/14_data_engineering/01_infrastructure/014_namenode/)는 해당 노드가 죽었다고 판단하고, 잃어버린 블록들을 다른 건강한 노드에 다시 3벌이 되도록 긴급 자동 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)합니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) | 전통적 [NAS](/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/)/[SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 스토리지 | [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/) ([하둡](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 스토리지) | 클라우드 객체 스토리지 (S3) |
| :--- | :--- | :--- | :--- |
| **저장 패러다임** | 네트워크 어태치 블록/[파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) I/O | 로컬 디스크 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 분할 + [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) I/O 접근 | [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/[REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) 기반 [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)-Value 객체 저장 |
| <strong><a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 수정 가능 여부</strong> | 임의의 위치 랜덤 R/W 완벽 지원 | [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 한 번, 읽기 다수 (수정 불가, Append만) | 수정 불가 (새 객체로 덮어쓰기 덮어씌움) |
| **하드웨어 의존도** | 고가의 전용 어플라이언스 스토리지 ([RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/)) | 깡통 x86 서버 로컬 디스크 (S/W [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 의존) | AWS가 무한 확장 관리 ([Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)) |
| <strong>작은 <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>(Small <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">File</a>) 대응</strong> | 수만 개 작은 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 처리 유리 | [NameNode](/studynote/14_data_engineering/01_infrastructure/014_namenode/) 메모리 폭발 병목 (치명적 약점) | 객체 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 무한 확장이므로 문제없음 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- <strong><a href="/studynote/13_cloud_architecture/05_data_engineering/269_small_file_problem_data_lakehouse/">Small File Problem</a>(작은 <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 문제)</strong>: HDFS의 가장 큰 아킬레스건입니다. [네임노드](/studynote/14_data_engineering/01_infrastructure/014_namenode/)는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 1개당 약 150바이트의 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)를 메모리(RAM)에 상주시키는데, 1KB짜리 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 1억 개를 넣으면 디스크는 남아도는데 [마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터 서버의 메모리가 폭발([OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/))하여 클러스터가 죽습니다. 기술사는 [하둡](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 적재 전 반드시 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 병합(HAR, [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) 묶음)하는 [데이터 파이프라인 전처리](/studynote/10_ai/02_dl_architecture_new/181_apache_airflow/) 설계를 강제해야 합니다.
- **클라우드 전환 딜레마**: [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)가 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 중심일 때 HDFS가 진리였으나, 최근 [클라우드 네이티브 아키텍처](/studynote/12_it_management/05_security_compliance/204_cloud_native_architecture/)에서는 HDFS의 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 및 디스크 관리 오버헤드를 버리고 S3로 저장소를 전면 이관하는 '스토리지-컴퓨터 분리' 아키텍처가 압도적 대세입니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
HDFS는 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 움직이지 말고 연산을 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 곁으로 보내라([Data Locality](/studynote/14_data_engineering/01_infrastructure/019_data_locality/))"라는 철학을 물리적으로 실현시킨 걸작 인프라입니다. 페타바이트급 정제되지 않은 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) 원시 공간을 싼 가격에 확보해주며, 스파크 인메모리 엔진 밑단에서도 디스크 입출력의 강력한 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 펌프 역할을 안정적으로 수행하고 있습니다.

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **선행 개념**: 빅데이터 인프라, [분산 파일 시스템](/studynote/02_operating_system/09_file_system/553_distributed_file_system/)
- **핵심 기술**: [네임노드](/studynote/14_data_engineering/01_infrastructure/014_namenode/)([NameNode](/studynote/14_data_engineering/01_infrastructure/014_namenode/)), [데이터노드](/studynote/14_data_engineering/01_infrastructure/015_datanode/)([DataNode](/studynote/14_data_engineering/01_infrastructure/015_datanode/)), 블록 128MB, 3중 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)
- **확장 및 응용**: 작은 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 문제([Small File Problem](/studynote/13_cloud_architecture/05_data_engineering/269_small_file_problem_data_lakehouse/)), [랙 인지](/studynote/14_data_engineering/01_infrastructure/017_rack_awareness/)([Rack Awareness](/studynote/14_data_engineering/01_infrastructure/017_rack_awareness/)), AWS S3

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 빅데이터 인프라, 분산 파일 시스템]
    |
    v
[핵심 기술: 네임노드(NameNode), 데이터노드(DataNode), 블록 128MB, 3중 복제]
    |
    v
[확장 및 응용: 작은 파일 문제(Small File Problem), 랙 인지(Rack Awareness), AWS S3]
```

이 흐름도는 선행 개념: 빅데이터 인프라, [분산 파일 시스템](/studynote/02_operating_system/09_file_system/553_distributed_file_system/)에서 출발해 확장 및 응용: 작은 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 문제([Small File Problem](/studynote/13_cloud_architecture/05_data_engineering/269_small_file_problem_data_lakehouse/)), [랙 인지](/studynote/14_data_engineering/01_infrastructure/017_rack_awareness/)([Rack Awareness](/studynote/14_data_engineering/01_infrastructure/017_rack_awareness/)), AWS S3까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 100층짜리 거대한 블록 장난감을 한 번에 옮기려면 무거워서 허리가 부러질 거예요.
2. HDFS는 이 장난감을 10층짜리 10개로 분해해서 친구들 10명의 배낭에 나누어 담는 똑똑한 짐꾼 시스템이에요.
3. 혹시 친구 한 명이 넘어져서 블록을 잃어버릴까 봐, 몰래 다른 친구들 배낭에 똑같은 블록을 3벌씩 복사해 숨겨두는 안전 마법도 걸려있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 24 / 262

<- **이전**: [01. 아파치 하둡 (Apache Hadoop) - 분산 스토리지 및 처리](/studynote/16_bigdata/02_hadoop/023_apache_hadoop_distributed_storage_processing/)
**다음**: [03. 네임노드 (NameNode) - 메타데이터 관리와 고가용성](/studynote/16_bigdata/02_hadoop/025_namenode_metadata_spof_ha/) ->

---
