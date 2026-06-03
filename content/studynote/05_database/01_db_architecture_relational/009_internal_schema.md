+++
title = "9. 내부 스키마 (Internal Schema) - 물리적 저장 장치 관점"
description = "물리적 저장 장치 관점의 데이터베이스 스키마와 최적화 원리"
date = 2024-05-20

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

# 내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) (Internal [Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/))
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 3단계 아키텍처 중 최하위 계층으로, [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 실제 디스크(물리적 저장 장치)에 어떻게 저장될지 명세하는 구조입니다.
> 2. **가치**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록 크기, [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/), 인덱싱 구조 등을 정의하여 시스템의 I/O 응답 속도와 스토리지 효율을 극대화합니다.
> 3. **융합**: [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(OS)의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 관리, 블록 스토리지 아키텍처 및 [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) 자료구조 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)과 직접적으로 맞물려 동작합니다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)
내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) (Internal [Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/))는 시스템 엔지니어나 물리적 [데이터베이스 설계자](/knowledge-base/studynote/05_database/01_db_architecture_relational/027_database_designer/) 관점에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 저장 장치에 실제로 표현되는 방식을 정의합니다. 사용자와 응용 프로그램은 테이블([개념 스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/008_conceptual_schema/))이라는 2차원 표만 인식하지만, 컴퓨터의 디스크 드라이브는 2차원 표를 이해하지 못하고 연속된 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)([Bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/))와 블록(Block)의 스트림만을 처리합니다.
내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)는 이 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 표를 디스크의 실린더, 트랙, 섹터, [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 단위로 어떻게 배치할 것인지 결정합니다. 대용량 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 발생하는 현대 시스템에서는, 아무리 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)([정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))가 잘 되어 있어도 디스크 I/O 병목을 해결하지 못하면 시스템이 멈춰버립니다. 따라서 레코드의 물리적 배치 순서, [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/), 암호화, [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 자료구조 등을 다루는 내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)의 최적화는 전체 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 좌우하는 결정적 요인입니다.

아래 그림은 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 테이블이 내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)를 거쳐 물리적 스토리지로 매핑되는 계층 구조를 보여줍니다.
```text
[개념 스키마]    Employee 테이블 (Row & Column)
                       ↓ (개념/내부 사상)
[내부 스키마] ┌──────────────────────────────────────────┐
              │ - 레코드 포맷: 가변 길이 (Row Chaining)  │
              │ - 인덱스 구조: B+Tree (Clustered)        │
              │ - 파티셔닝   : Range Partition by Date   │
              │ - 데이터 압축: LZ4 / Page 암호화(TDE)    │
              └──────────────────────────────────────────┘
                       ↓ (OS 파일 시스템 매핑)
[물리 저장소]    Data File 1 (Extent -> Block -> OS Page -> HDD/SSD)
```
이 도식에서 핵심은 내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)가 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(Employee)를 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 이해할 수 있는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)/블록 구조로 '번역'하고 '포장'하는 역할을 수행한다는 점입니다. [개념 스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/008_conceptual_schema/)는 하나지만, DBA는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상을 위해 테이블을 여러 개의 물리 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 분할하거나([파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)), [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 추가하는 등 내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)를 자유롭게 재구성할 수 있습니다. 이것이 물리적 [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/)(Physical [Data Independence](/knowledge-base/studynote/05_database/04_transactions_concurrency/504_data_independence/))의 근간입니다.

📢 **섹션 요약 비유**: 물류 창고에서 서류상의 '품목 리스트([개념 스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/008_conceptual_schema/))'를 보고, 실제 지게차가 동선을 최소화할 수 있도록 'A구역 3번 선반 2층(내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/))'에 물건을 적재하는 배치도와 같습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)는 DBMS의 스토리지 엔진(Storage 엔진, 예: InnoDB)과 버퍼 매니저를 제어하는 복잡한 파라미터들로 구성됩니다.

| 구성 요소 | 역할 | 내부 동작 메커니즘 | 실무 매핑 ([Oracle](/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/)/MySQL) | 비유 |
|:---|:---|:---|:---|:---|
| **Tablespace & Datafile** | [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)/물리 매핑 공간 | 여러 테이블을 묶어 물리적 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(.ibd, .dbf)에 할당 | TABLESPACE, 디스크 할당 | 거대한 서랍장 |
| <strong>Block / <a href="/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">Page</a></strong> | I/O의 최소 단위 | 디스크에서 메모리로 퍼올리는 기본 전송 단위 (보통 8KB~16KB) | DB_BLOCK_SIZE | 물건을 담는 규격 박스 |
| **Record Format** | 행(Row) 저장 방식 | 고정/가변 길이 레코드 관리, 행 이주(Row Migration) 처리 | Row Header, Null Bitmap | 박스 내부 칸막이 |
| <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">Index</a> Structure</strong> | 검색 경로 최적화 | [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) 또는 Hash 구조로 포인터(ROWID) [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 구성 | CLUSTERED, 보조 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) | 백과사전 색인 |
| <strong><a href="/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/">Clustering</a>/<a href="/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/">Partitioning</a></strong> | 물리적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/) | 조인 속도 향상을 위해 연관 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 동일 블록에 모음 | Range, Hash [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) | 연관 상품 묶음 진열 |

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 디스크 블록에 물리적으로 저장되는 (내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 관점) 세부 구조는 다음과 같습니다.
```text
┌── DB Block (e.g., 8KB) ───────────────────────────┐
│ [Block Header] LSN, Checksum, Transaction ID      │
│ [Row Directory] -> 각 Record의 오프셋 포인터 배열 │
│                                                   │
│ [Free Space] (향후 Update를 대비한 빈 공간, PCTFREE)│
│                                                   │
│ [Record 3] (Col A=..., Col B=...)                 │
│ [Record 2] (Col A=..., Col B=...)                 │
│ [Record 1] (Col A=..., Col B=...)                 │
└───────────────────────────────────────────────────┘
```
이 구조의 핵심은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레코드가 블록의 밑바닥부터 쌓이고, 헤더 포인터는 위에서부터 내려오는 구조라는 점입니다. 중간에 있는 `Free Space`는 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 도중 레코드 길이가 늘어날 때(Update 시) 다른 블록으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 튕겨 나가는 현상(Row Migration)을 방지하기 위한 여유 공간입니다. DBA는 내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 설계 시 이 빈 공간의 비율(PCTFREE)을 튜닝하여 디스크 낭비와 I/O [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 사이의 타협점을 찾습니다.

📢 **섹션 요약 비유**: 이삿짐을 박스에 담을 때, 나중에 물건을 더 넣을 것을 대비해 박스 상단을 조금 비워두는(Free Space) 고도의 테트리스 작업과 같습니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 최적화 시, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 방식(Row vs Column)에 따라 극명한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이가 발생합니다.

| 아키텍처 특성 | 로우 스토어 (Row Store) | 컬럼 스토어 (Column Store) | 트레이드오프 판단 |
|:---|:---|:---|:---|
| **저장 방식** | 하나의 행(Row) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 연속적으로 저장 | 같은 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)(Column) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)끼리 연속 저장 | **디스크 블록 배치 순서** |
| **I/O 병목** | 특정 컬럼만 집계할 때도 전체 행을 읽어야 함 | 필요한 컬럼 블록만 읽음 (I/O 극소화) | <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 접근 패턴</strong> |
| <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a> 효율</strong> | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타입이 혼재되어 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률 낮음 | 동일 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타입 연속으로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률 극대화 | **스토리지 비용 절감** |
| **최적 워크로드**| [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) (잦은 삽입, 단건 조회) | [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) (대용량 집계, [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/), 통계) | <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>의 목적</strong> |

이 매트릭스는 내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)를 어떻게 구성하느냐에 따라 동일한 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 테이블이 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)용([OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/))이 되기도 하고 분석용([OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/))이 되기도 함을 증명합니다. 최신 [NewSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/058_newsql_google_spanner_truetime_distributed_transaction/) [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)(예: [TiDB](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/293_elt_process/), SAP HANA)는 메모리에서는 Row 단위로 처리하고 디스크 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 시에는 Column 단위로 저장하는 하이브리드([HTAP](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/)) 내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)를 채택하여 두 방식의 장점을 모두 취하고 있습니다.

📢 **섹션 요약 비유**: 도서관에서 책을 번호순(Row)으로 꽂을지, 장르별(Column)로 꽂을지 결정하는 것입니다. 한 권을 통째로 빌릴 땐 번호순이 빠르지만, 특정 장르의 책 두께만 비교할 땐 장르별 배치가 압도적으로 빠릅니다.

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
실무에서 내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 관련 이슈는 대부분 치명적인 장애나 엄청난 I/O [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)으로 직결됩니다.

1. <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/">파티셔닝</a> (<a href="/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/">Partitioning</a>) <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>: 수억 건이 쌓이는 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 테이블의 경우, [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 테이블은 1개로 두되 내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 단에서 월별로 물리적 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 쪼개는 Range [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)을 적용합니다. 이를 통해 오래된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 삭제(DROP)할 때 DELETE [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 대신 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)([Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)) 자체를 버림으로써 시스템 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/))을 유발하지 않습니다.
2. <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/169_clustering_factor_index_physical_sort/">클러스터링 팩터</a> (<a href="/knowledge-base/studynote/05_database/03_relational_model/169_clustering_factor_index_physical_sort/">Clustering Factor</a>) 관리</strong>: [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 트리의 정렬 순서와 실제 디스크 블록의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정렬 순서가 일치하는 정도를 의미합니다. 이 수치가 나쁘면(무작위 배치), [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 타더라도 디스크 헤드가 이리저리 튀면서 풀 스캔보다 느려지는 현상이 발생합니다. DBA는 주기적인 테이블 재구성을 통해 이 수치를 교정합니다.
3. <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a> (과도한 <a href="/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a> <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a>)</strong>: 조회 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 높인다고 내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)에 수십 개의 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 걸면, INSERT/UPDATE 발생 시마다 모든 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 트리를 재정렬해야 하는 최악의 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 병목이 발생합니다.

아래 트리는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 시 내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 튜닝의 의사결정 흐름을 보여줍니다.
```text
[쿼리 성능 저하 감지]
   ↓
[실행 계획(Plan) 분석]
   ├─> (풀 스캔 발생) ──> 인덱스 트리 추가 (내부 스키마 변경)
   └─> (인덱스 스캔 됨) ──> [병목 원인 파악]
          ├─> 랜덤 I/O 과다? ──> 클러스터드 인덱스 재정렬 (리빌드)
          └─> 블록 경합? ──> PCTFREE 증가 (블록당 레코드 수 감소시켜 락 분산)
```
이 흐름의 핵심은 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)(외부/개념) 수정 없이, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 물리적 배치와 블록 밀도를 조정하는 것만으로 극적인 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 개선을 이뤄낸다는 점입니다. 이것이 물리적 [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/)이 실무에서 주는 가장 강력한 무기입니다.

📢 **섹션 요약 비유**: 엔진(SQL)은 좋은데 차가 안 나간다면, 엔진을 바꾸는 대신 타이어 공기압(블록 크기)을 맞추고 기어비([인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/))를 조율하는 전문가의 튜닝 작업과 같습니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
정교한 내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 설계는 하드웨어 자원의 한계를 소프트웨어적으로 극복하게 해주는 마법입니다.

| 정량적 효과 | 정성적 효과 |
|:---|:---|
| 디스크 I/O 횟수 및 스토리지 공간 70% 이상 절감 | 예측 가능한 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) 보장 |
| [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 및 [파티션 프루닝](/knowledge-base/studynote/05_database/03_relational_model/184_partition_pruning/)을 통한 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 응답 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 최소화 | 시스템 다운타임 없는 대용량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 아카이빙 구조 확보 |

최근 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 환경에서는 스토리지와 컴퓨팅이 분리([Separation of Storage and Compute](/knowledge-base/studynote/05_database/06_dw_olap_trends/357_separation_of_storage_and_compute/))되면서, 내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)의 역할 중 [스토리지 티어링](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/674_storage_tiering/)(Hot/Cold [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자동 이동)과 S3와 같은 객체 스토리지 [파케이](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)([Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)) 포맷 매핑 기능이 미래 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 핵심 표준으로 자리 잡고 있습니다.

📢 **섹션 요약 비유**: 수백만 개의 소포를 처리하는 글로벌 물류 [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)에서, 단 1초의 낭비도 없도록 컨베이어 벨트와 창고 선반의 각도를 설계하는 궁극의 최적화 도면입니다.

---
### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
* [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) / B+Tree [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) (내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 검색 경로를 최적화하는 기본 자료구조)
* 물리적 [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/) (내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변경이 응용 프로그램에 영향을 주지 않는 성질)
* [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)과 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) (대용량 테이블을 여러 개의 물리적 단위로 쪼개는 내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 기술)
* 스토리지 엔진 ([DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 코어에서 디스크 블록 할당과 I/O를 통제하는 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/), 예: InnoDB)
* Row Migration & [Chaining](/knowledge-base/studynote/12_it_management/03_ea_isp/103_chaining/) (블록 공간 부족으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 분절되는 현상과 해소 기법)

### 📈 관련 키워드 및 발전 흐름도

```text
[개념 스키마 — 전체 데이터 의미 정의]
    │
    ▼
[논리 스키마 — 테이블/관계 구조 설계]
    │
    ▼
[내부 스키마(물리 설계) — 저장 구조 구체화]
    │
    ▼
[인덱스/파티셔닝 — 접근 성능 최적화]
    │
    ▼
[스토리지 엔진 최적화 — 실제 I/O 튜닝]
```

내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)는 개념·[논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)를 물리 저장 구조와 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 최적화로 연결하는 단계다.

### 👶 어린이를 위한 3줄 비유 설명
1. 서류상에 장난감 목록을 적어둔 것이 [개념 스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/008_conceptual_schema/)라면, 이 장난감들을 실제 방 안의 장난감 상자에 어떻게 예쁘게 우겨넣을지 고민하는 것이 내부 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)예요.
2. 로봇은 네모난 상자에, 인형은 동그란 상자에 차곡차곡 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해서 넣으면 방이 넓어지겠죠?
3. 이렇게 방 정리를 잘 해두면 나중에 놀고 싶은 장난감을 찾을 때 1초 만에 바로 꺼낼 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 9 / 600

← **이전**: [8. 개념 스키마 (Conceptual Schema) - 조직 전체 관점, 논리적 구조](/knowledge-base/studynote/05_database/01_db_architecture_relational/008_conceptual_schema/)
**다음**: [10. 스키마 매핑 (Mapping) - 외부/개념 사상, 개념/내부 사상](/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/) →

---
