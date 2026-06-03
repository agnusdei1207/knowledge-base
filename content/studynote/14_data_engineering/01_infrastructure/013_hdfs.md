---
title: 13. HDFS (Hadoop Distributed File System) - 거대 파일을 기본 128MB 블록 단위로 쪼개 수많은 데이터노드에
  분산 저장
date: '2023-10-24'
description: 거대 파일을 블록 단위로 쪼개어 수천 대의 노드에 분산 복제 저장하는 하둡 분산 파일 시스템의 코어 아키텍처
tags:
- data_engineering
---

# HDFS ([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[553_distributed_file_system|Distributed File System]])

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 테라바이트(TB) 이상의 거대한 단일 [[501_file_definition_logical_record|파일]]을 기본 128MB 크기의 블록(Block) 단위로 물리적으로 쪼개어, 클러스터 내의 수많은 [[015_datanode|데이터노드]]([[015_datanode|DataNode]])에 흩뿌려 저장하는 [[136_variance|분산]] [[501_file_definition_logical_record|파일]] 시스템이다.
> 2. **가치**: 저가형 하드웨어의 잦은 디스크 고장을 전제로 설계되어, 동일한 블록을 서로 다른 물리적 위치(Rack)에 3벌씩 [[016_replication_factor|복제]]([[016_replication_factor|Replication]])함으로써 완벽한 [[296_fault_tolerance_architecture|결함 허용]]([[800_system_architecture_fault_tolerance_dual|Fault Tolerance]])과 [[001_dikw_pyramid|데이터]] 무결성을 보장한다.
> 3. **융합**: HDFS는 [[001_dikw_pyramid|데이터]]가 있는 노드로 연산 코드를 보내는 '[[019_data_locality|데이터 지역성]]([[019_data_locality|Data Locality]])'의 기반을 제공하며, 스파크(Spark) 및 하이브([[544_hive|Hive]]) 등 모든 빅데이터 처리 엔진의 영구 저장소로 활약한다.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

HDFS ([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[553_distributed_file_system|Distributed File System]])는 아파치 [[843_hadoop_rack_awareness_data_replication_topology|하둡]]의 가장 밑바탕을 이루는 심장과도 같은 스토리지 계층이다. 기존 [[501_file_definition_logical_record|파일]] 시스템([[525_fat_file_allocation_table|FAT]], NTFS, ext4 등)은 물리적인 하드 디스크 하나에 국한되어 동작하므로, 1TB짜리 디스크에 2TB의 단일 [[501_file_definition_logical_record|파일]]을 온전히 저장하는 것은 불가능했다. 빅데이터 시대에는 한 [[501_file_definition_logical_record|파일]]의 크기가 수십 테라바이트에 달하는 웹 [[568_logs_distributed_logging_elk_fluentd|로그]]나 유전체 [[001_dikw_pyramid|데이터]]가 쏟아져 나왔기 때문에, [[001_operating_system_purpose|운영체제]] 종속적인 기존 로컬 [[501_file_definition_logical_record|파일]] 시스템으로는 이 방대한 볼륨([[001_bigdata_3v_5v|Volume]])을 감당할 수 없었다.

HDFS는 이 거대한 [[501_file_definition_logical_record|파일]]을 가상으로 묶고 [[369_logic_bomb|논리]]적으로 분할하여, 수천 대의 컴퓨터에 장착된 낡은 하드 디스크들을 하나로 거대하게 이어붙인 '무한대의 [[369_logic_bomb|논리]]적 창고'를 창조해냈다. 핵심 설계 철학은 "하드웨어 장비는 언제나 망가질 수 있다(Hardware is unreliable)"는 전제다. 비싼 엔터프라이즈 스토리지를 사서 고장을 막으려 애쓰는 대신, 싸구려 디스크가 망가지는 것을 일상으로 취급하고 소프트웨어 차원에서 똑같은 [[001_dikw_pyramid|데이터]]를 여러 군데에 복사해 두어 생존성을 확보하는 파괴적 혁신을 이룩했다.

아래 다이어그램은 기존 로컬 [[501_file_definition_logical_record|파일]] 시스템이 거대 [[501_file_definition_logical_record|파일]]을 처리하지 못하는 한계와 HDFS가 이를 어떻게 잘게 쪼개어 네트워크 공간으로 확장하는지 비교하여 보여준다.

```text
[단일 파일 시스템의 한계와 HDFS 블록 분할 메커니즘]

[Local File System 한계]            [HDFS 블록 기반 분산 스토리지]
                                   ┌───────────────────────┐ (128MB 단위 분할)
 파일 크기: 500GB                      │     파일 (500GB)       │
 ┌─────────────────┐               └─┬──────┬──────┬───────┘
 │   OS Disk       │                 ↓      ↓      ↓  ...  
 │  (최대 100GB)   │          ┌─────┐┌─────┐┌─────┐   (Network)
 │ ❌ 공간 부족!    │          │Blk 1││Blk 2││Blk 3│... ┌─────┐
 └─────────────────┘          └──┬──┘└──┬──┘└──┬──┘   │Blk N│
                                 ↓      ↓      ↓      └──┬──┘
                              [노드A] [노드B] [노드C] ... [노드Z]
```

이 흐름의 핵심은 [[501_file_definition_logical_record|파일]] 자체를 하나의 큰 덩어리로 취급하지 않고 물리적으로 철저히 해체한다는 점이다. 클라이언트는 HDFS라는 [[369_logic_bomb|논리]]적인 단일 폴더 뷰를 보지만, 내부적으로는 128MB의 정형화된 블록들이 무작위 노드에 뿌려진다. 이러한 블록 단위 분할 덕분에 HDFS는 [[501_file_definition_logical_record|파일]] 크기의 물리적 제한을 완전히 없앴으며, 디스크 I/O를 수십 대의 노드에서 동시에 [[430_index_fast_full_scan|병렬]]로 읽어들이는 극단적인 속도 향상을 이루어냈다.

> 📢 **섹션 요약 비유**: 코끼리(500GB [[501_file_definition_logical_record|파일]]) 한 마리를 작은 냉장고(단일 서버) 하나에 넣는 건 불가능하지만, 코끼리를 128MB 크기의 수백 개 상자에 완벽히 나누어 담고(블록화) 마을 사람 전체의 냉장고에 하나씩 맡겨두는([[136_variance|분산]] 저장) 마법과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

HDFS 아키텍처는 마스터-슬레이브(Master-Slave) 구조의 극단을 보여주는 대표적인 설계다. 전체 [[501_file_definition_logical_record|파일]] 시스템의 네임스페이스와 폴더 트리를 관리하는 '[[014_namenode|네임노드]]'와, 실제 쪼개진 [[001_dikw_pyramid|데이터]] 블록을 물리적 디스크에 저장하는 수천 대의 '[[015_datanode|데이터노드]]'로 명확히 역할이 나뉜다.

| 구성 요소 | 역할 | 내부 동작 | [[295_protocol_field_tcp_udp_icmp|프로토콜]] | 비유 |
|:---|:---|:---|:---|:---|
| **[[014_namenode|NameNode]] (마스터)** | [[012_metadata|메타데이터]] 중앙 관리 | "A파일은 Blk1, Blk2로 나뉘어 있고, 각각 노드 1,3,5에 있다"는 장부(FsImage/EditLog)를 메모리에서 관리 | HDFS [[003_audit_stakeholders|Client]] [[126_rpc|RPC]] | 대형 물류 창고의 총괄 장부 |
| **[[015_datanode|DataNode]] (워커)** | 실제 블록 저장 및 읽기/[[289_cqrs_db|쓰기]] | 물리 디스크에 [[501_file_definition_logical_record|파일]]을 저장하고, 3초마다 마스터에 하트비트(생존 신고) 및 블록 리포트 전송 | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]], 블록 전송 | 각 지역 물류 창고 관리인 |
| **Secondary [[014_namenode|NameNode]]** | [[012_metadata|메타데이터]] [[555_backup_and_restore_strategy|백업]]/병합 | [[483_active_vs_passive_ftp|Active]] [[014_namenode|네임노드]]의 메모리 부하를 줄이기 위해 [[568_logs_distributed_logging_elk_fluentd|로그]](EditLog)를 주기적으로 가져와 [[022_snapshot_backup_architecture|스냅샷]] 병합(Checkpoint) 수행 | [[461_http_stateless_connection_oriented|HTTP]] | 회계 [[606_auditing_linux_auditd|감사]] [[555_backup_and_restore_strategy|백업]] 보조 |
| **Block (블록)** | HDFS [[369_logic_bomb|논리]]적 최소 저장 단위 | 기본 128MB ([[843_hadoop_rack_awareness_data_replication_topology|하둡]] 1.x는 64MB). OS 디스크 블록(4KB)보다 압도적으로 커서 디스크 탐색(Seek) 시간 비중 최소화 | 바이너리 [[001_dikw_pyramid|데이터]] | 물류용 규격 [[561_container_based_deployment|컨테이너]] |
| **[[016_replication_factor|Replication]] [[082_pipeline|Pipeline]]** | 3중 [[016_replication_factor|복제]] 흐름 [[123_pipe|파이프]] | 클라이언트가 첫 노드에 [[001_dikw_pyramid|데이터]]를 쓰면, 그 노드가 다음 노드로 릴레이(Relay) 방식으로 [[001_dikw_pyramid|데이터]]를 [[123_pipe|파이프]]라이닝 복사 | [[125_socket|소켓]] 스트림 | 버킷 릴레이 (소방수 양동이 전달) |

아래의 HDFS 읽기/[[289_cqrs_db|쓰기]] 아키텍처 계층도는 클라이언트가 거대 [[501_file_definition_logical_record|파일]]을 HDFS에 저장할 때 NameNode와 DataNode가 어떻게 상호작용하는지 통신 흐름을 보여준다.

```text
┌───────────────────────────────────────────────────────────────┐
│                    [HDFS Client (사용자 / Spark 등)]          │
│                      │ 1. 쓰기 요청 (파일 분할)               │
└──────────────────────┼────────────────────────────────────────┘
                       ▼
             ┌──────────────────┐
             │    NameNode      │ 2. 메타데이터 기록 및 
             │ (장부/디렉토리)  │ 블록을 저장할 DataNode 목록 반환
             └───────┬──────────┘
                     │ 3. 할당된 노드 리스트 (예: D1, D3, D5) 반환
        ┌────────────┴─────────────┐
        ▼                          ▼
┌──────────────┐          ┌──────────────┐          ┌──────────────┐
│ DataNode 1   │ 4. 블록  │ DataNode 3   │ 5. 파이프│ DataNode 5   │
│ (블록 1-본본)│──전송───>│ (블록 1-복제1)│──라인───>│ (블록 1-복제2)│
└──────────────┘          └──────────────┘          └──────────────┘
      ▲                           ▲                        ▲
      └───────────────────────────┴────────────────────────┘
                 6. 3초마다 Heartbeat 및 Block Report 송신
```

이 구조도의 핵심 트레이드오프는 [[001_dikw_pyramid|데이터]]의 흐름과 제어(장부)의 흐름이 철저히 분리되어 있다는 점이다. 클라이언트는 어떤 노드에 [[001_dikw_pyramid|데이터]]를 저장할지 NameNode에게 묻지만(제어 흐름), 실제 테라바이트급 [[001_dikw_pyramid|데이터]]는 마스터 노드를 거치지 않고 Client와 [[015_datanode|DataNode]] 간에 직접 [[123_pipe|파이프]]라인으로 전송된다([[001_dikw_pyramid|데이터]] 흐름). 이는 마스터 노드가 [[001_dikw_pyramid|데이터]] 트래픽에 파묻혀 병목 상태가 되는 것을 완벽히 방지하는 HDFS의 가장 위대한 아키텍처적 승리다.

블록 크기가 128MB로 비정상적으로 큰 이유는 디스크의 랜덤 탐색([[467_disk_access_time|Seek Time]]) 지연을 상쇄하고 순차 읽기(Sequential Read) 속도를 극대화하기 위해서다. 보통 탐색 시간이 10ms라면 [[501_file_definition_logical_record|파일]] 전송 시간을 1초 정도로 길게 가져가야 탐색 시간의 비율이 1% 이하로 떨어지기 때문에, 거대 [[001_dikw_pyramid|데이터]] 분석에 있어 128MB 단위 스트리밍 읽기가 압도적인 효율을 발휘한다.

> 📢 **섹션 요약 비유**: 물건을 보낼 때 사장님([[014_namenode|NameNode]])에게는 "이 [[561_container_based_deployment|컨테이너]]를 어디 창고로 보낼까요?"라고 주소만 묻고, 실제 무거운 화물(Block)은 사장님 책상을 거치지 않고 택배 기사([[015_datanode|DataNode]])들끼리 릴레이로 직접 전달하여 병목을 없앤 시스템입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

HDFS는 [[590_worm|WORM]] (Write Once, Read Many - 한 번 쓰고 여러 번 읽기) 워크로드에 극단적으로 최적화된 [[501_file_definition_logical_record|파일]] 시스템이다. 일반적인 범용 RDBMS나 로컬 [[001_operating_system_purpose|운영체제]] [[501_file_definition_logical_record|파일]] 시스템과는 그 사용 목적이 근본적으로 다르다.

| 비교 항목 | HDFS ([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[501_file_definition_logical_record|File]] System) | 로컬 OS [[501_file_definition_logical_record|파일]] 시스템 (ext4, NTFS) | [[136_variance|분산]] [[035_nosql|NoSQL]] ([[543_hbase|HBase]], [[541_cassandra|Cassandra]]) |
|:---|:---|:---|:---|
| **저장 목적** | 테라바이트/페타바이트급 거대 [[501_file_definition_logical_record|파일]] 연속 저장 | OS [[022_kernel_role|커널]] 및 사용자의 자잘한 문서/프로그램 저장 | 수십억 건의 Row 단위 실시간 읽기/[[289_cqrs_db|쓰기]]/업데이트 |
| **블록 사이즈** | 기본 128MB (거대함) | 보통 4KB (매우 작음) | 테이블의 메모리 [[494_memtable_sstable_flush|멤테이블]] 및 SSTable 단위 |
| **[[001_dikw_pyramid|데이터]] 갱신 (Update)** | ❌ 원칙적으로 내용 수정 불가 (Append만 가능) | ✅ [[501_file_definition_logical_record|파일]] 중간의 랜덤 수정/덮어쓰기 자유로움 | ✅ 특정 [[067_db_key_uniqueness_minimality|Key]] 기반 Row의 실시간 업데이트 지원 |
| **장애 내성** | 3중 [[016_replication_factor|복제]]로 노드 하나가 죽어도 무중단 [[090_service_kubernetes_network_load_balancing|서비스]] 보장 | 디스크 물리적 파손 시 [[001_dikw_pyramid|데이터]] 유실 ([[483_raid_overview|RAID]] 별도 필요) | [[244_consistent_hashing_ring_distribution|컨시스턴트 해싱]] 기반의 [[452_availability|가용성]] 및 [[016_replication_factor|복제]] 보장 |

다음의 상태 상태도는 HDFS가 [[296_fault_tolerance_architecture|결함 허용]]([[800_system_architecture_fault_tolerance_dual|Fault Tolerance]])을 달성하기 위해, [[016_replication_factor|복제]]본 중 하나가 소실되었을 때 일어나는 자가 치유(Self-healing) [[658_ir_recovery|복구]] [[123_pipe|파이프]]라인을 보여준다.

```text
[HDFS 노드 장애 발생 시 블록 자가 복구 (Under-replicated) 메커니즘]

[정상 상태] D1(블록A), D2(블록A), D3(블록A) 유지 => 복제 계수(Replication Factor) 3 만족
     │
     │ 💥 DataNode 2 하드웨어 크래시 (Heartbeat 중단)
     ▼
[NameNode 감지] "D2가 10분간 무응답. 블록A의 복제본이 2개(D1, D3)로 떨어짐!"
     │
     │ 복구 명령 (Replication Command) 하달
     ▼
[파이프라인 재가동] D1에게 지시 ──복사──> [새로운 D4 노드]에 블록A 전송
     │
     ▼
[상태 수렴] D1, D3, D4가 블록A를 소유하게 되어 다시 안전한 복제 계수 3 회복 완료
```

A 방식(로컬/[[492_nas_network_attached_storage|NAS]] 디스크)은 속도가 매우 빠르고 중간 수정이 자유롭지만 디스크 장애에 극도로 취약하다. 이를 막기 위한 하드웨어 [[483_raid_overview|RAID]] 장비는 비용이 막대하다. 반면 B 방식(HDFS)은 무조건 [[501_file_definition_logical_record|파일]]을 3벌씩 복사해 다른 랙(Rack) [[238_switch_operation_principles|스위치]]에 [[136_variance|분산]]시켜 두므로, 서버실에 불이 나 랙 하나가 통째로 타버려도 [[001_dikw_pyramid|데이터]] 유실률이 0에 수렴한다. 다만 중간 [[001_dikw_pyramid|데이터]]를 수정할 수 없으므로([[298_immutable|Immutable]]), 실무에서는 HDFS의 이 치명적인 업데이트 불가 단점을 메우기 위해 HDFS 위에서 동작하는 델타 레이크([[147_delta_lake|Delta Lake]])나 아파치 아이스버그(Iceberg) 같은 [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]] 계층을 융합하여 ACID 트랜잭션과 수정을 지원하도록 진화시켰다.

> 📢 **섹션 요약 비유**: HDFS는 '석판에 글씨를 새기는 튼튼한 금고'입니다. 한 번 새기면(Write) 수천 명이 가져가서 복사해 볼 수 있고(Read) 절대 지워지지 않지만, 중간에 오타가 났다고 해서 지우개로 쓱싹쓱싹 수정할 수는 없는 구조를 가졌습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

실무에서 HDFS 클러스터를 구축하고 관리할 때 직면하는 가장 치명적인 재앙은 **"Small Files Problem (소규모 [[501_file_definition_logical_record|파일]] 병목)"**이다.

1. **소규모 [[501_file_definition_logical_record|파일]] 안티패턴의 붕괴 [[369_logic_bomb|논리]]**: HDFS의 [[014_namenode|네임노드]]는 빠른 속도를 위해 모든 [[501_file_definition_logical_record|파일]]과 블록의 [[012_metadata|메타데이터]] 위치(장부)를 오직 주 메모리(RAM)에 전부 올려둔다. [[501_file_definition_logical_record|파일]] 1개당 약 150바이트의 [[012_metadata|메타데이터]] 메모리를 먹는다. 1TB [[501_file_definition_logical_record|파일]]을 128MB 블록으로 쪼개면 장부 기록은 몇 줄 안 되지만, 10KB짜리 [[501_file_definition_logical_record|파일]] 1억 개를 HDFS에 넣으면 총 용량은 1TB 남짓인데도 [[014_namenode|네임노드]]의 램(RAM) 15GB가 순식간에 증발한다. 결국 [[014_namenode|NameNode]] [[157_oom_killer|OOM]]([[157_oom_killer|Out of Memory]]) 크래시가 발생하며 클러스터 전체가 뻗어버린다.
2. **[[017_rack_awareness|랙 인지]] ([[017_rack_awareness|Rack Awareness]]) 설계**: [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] [[238_switch_operation_principles|스위치]] 전원이 나가는 물리적 대장애를 막기 위해, HDFS는 [[016_replication_factor|복제]]본 3개를 같은 랙(Rack) 서버에 전부 몰아넣지 않고, 1개는 같은 랙, 나머지 2개는 물리적으로 다른 랙에 배치하도록 클러스터 토폴로지를 스크립트로 구성해야 한다. 
3. **[[452_availability|가용성]] 보장 ([[014_namenode|NameNode]] HA)**: [[014_namenode|NameNode]] 자체가 죽으면 전체 클러스터 장부가 사라져 아무것도 못하는 [[454_spof|단일 장애점]]([[454_spof|SPOF]])이 된다. 실무 환경에서는 반드시 [[483_active_vs_passive_ftp|Active]] NameNode와 Standby NameNode를 [[456_dual_redundancy|이중화]](High [[452_availability|Availability]] 구성)하고, 그 사이에 저널노드(JournalNode)를 두어 실시간으로 장부 기록을 동기화해야 한다.

```text
[HDFS 스토리지 운영 효율화 및 파일 최적화 의사결정 트리]

[일일 로그 데이터가 10KB 단위로 HDFS에 지속 유입]
       ↓
[단순 적재 방치 시] ──> [NameNode 메타데이터 메모리 폭발 💥 (클러스터 중단)]
       ↓
[어떻게 전처리할 것인가?]
  ├─ (주기적 배치 병합) ──> [Spark/Hive 잡으로 자정마다 작은 파일을 1GB 파케이(Parquet)로 뭉치기]
  ├─ (Hadoop 기본 아카이브) ──> [HAR (Hadoop Archive) 명령어로 묶음 압축 저장]
  └─ (스트리밍 버퍼링) ──> [Kafka → Flink 파이프라인에서 메모리에 들고 있다가 128MB가 차면 Flush]
```

이 의사결정의 핵심은 HDFS를 절대 범용 [[501_file_definition_logical_record|파일]] [[555_backup_and_restore_strategy|백업]] 디스크처럼 써서는 안 된다는 점이다. 실무에서는 [[179_kafka_flink_watermark_time_window|카프카]]([[179_kafka_flink_watermark_time_window|Kafka]]) 등에서 유입되는 수많은 자잘한 이벤트 [[568_logs_distributed_logging_elk_fluentd|로그]]를 [[568_logs_distributed_logging_elk_fluentd|로그]]스태시(Logstash)나 플링크(Flink) 단계에서 윈도우 버퍼에 들고 있다가, 최소 128MB 이상의 덩어리가 되었을 때 한 방에 HDFS로 떨어뜨리는(Flush) 구조가 강제된다. 또한 저장 시에는 단순 Text가 아니라 Columnar 포맷([[178_parquet_rle_encoding_columnar_compression|Parquet]], ORC)과 Snappy [[347_compaction|압축]]을 결합하여 I/O 비용을 극한으로 깎아내야 한다.

> 📢 **섹션 요약 비유**: 수백 평짜리 거대한 냉동 창고(HDFS)에 콩자반(작은 [[501_file_definition_logical_record|파일]])을 낱알로 수억 개 던져놓으면 재고 관리 장부([[014_namenode|NameNode]])가 터져버립니다. 반드시 콩을 10kg짜리 커다란 포대자루([[347_compaction|압축]] 포맷)에 꽉꽉 담아 [[347_compaction|압축]]한 뒤 넣어야만 창고가 제대로 돌아갑니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

HDFS는 빅데이터 시대에 스토리지가 가야 할 '[[136_variance|분산]]과 [[016_replication_factor|복제]]'의 패러다임을 확립한 위대한 표준이다.

| 기대 효과 | 기존 스토리지 인프라 ([[492_nas_network_attached_storage|NAS]]/[[493_san_storage_area_network|SAN]]) | HDFS 기반 인프라 도입 후 | 비즈니스 가치 |
|:---|:---|:---|:---|
| **[[001_dikw_pyramid|데이터]] 보존 한계** | 고가의 벤더 장비 비용으로 과거 [[568_logs_distributed_logging_elk_fluentd|로그]] 삭제 강요 | 무한대의 수평 확장([[202_scale_out_distributed_horizontal_expansion|Scale-out]])으로 전수 보관 | 기계학습 모델을 위한 거대한 재료(Feature) 원천 확보 |
| **I/O 병목 돌파** | 단일 스토리지 헤드에서 네트워크 병목 발생 | [[001_dikw_pyramid|데이터]]가 위치한 수백 대 노드의 로컬 디스크 [[430_index_fast_full_scan|병렬]] 읽기 | 대용량 [[228_batch_processing_hadoop_spark|배치 처리]] 시간 수백 배 단축 |
| **안정성 비용** | 값비싼 하드웨어 [[483_raid_overview|RAID]] 카드 및 [[456_dual_redundancy|이중화]] 솔루션 | 범용 장비 고장 시 소프트웨어 차원의 즉각 자가 복원 | 인프라 [[016_tco|TCO]] 급감 및 유지보수 자동화 |

최근 클라우드 시대로 접어들면서, 직접 서버에 디스크를 꽂아 구성하는 HDFS의 비중은 AWS S3나 GCS 같은 '클라우드 [[494_object_storage|오브젝트 스토리지]]([[494_object_storage|Object Storage]])'에 자리를 내주고 있다. [[494_object_storage|오브젝트 스토리지]]는 HDFS의 설계 철학([[136_variance|분산]], 3중 [[016_replication_factor|복제]])을 그대로 계승하면서도 유지보수 부담을 없앤 궁극의 형태다. 그러나 무거운 [[001_dikw_pyramid|데이터]]를 디스크에 깔고 연산을 밀어 넣는 HDFS의 '[[019_data_locality|데이터 지역성]]'과 견고한 스트리밍 처리 메커니즘은 여전히 빅데이터 [[136_variance|분산]] [[501_file_definition_logical_record|파일]] 시스템의 교과서이자 영원한 레퍼런스로 기능할 것이다.

> 📢 **섹션 요약 비유**: HDFS는 [[001_dikw_pyramid|데이터]]라는 무거운 물줄기를 다스리기 위해 만들어진 최초의 견고한 '콘크리트 댐'입니다. 지금은 클라우드라는 '거대한 인공 호수(S3)'가 유행이지만, 그 호수의 밑바닥에는 HDFS가 발명한 물막이([[136_variance|분산]] [[016_replication_factor|복제]]) 설계 기술이 그대로 녹아들어 있습니다.

---

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **[[014_namenode|네임노드]] ([[014_namenode|NameNode]])** | HDFS의 [[506_directory_structure_symbol_table|디렉터리]] 트리와 블록 매핑 장부를 메모리에서 총괄하는 유일한 마스터 관리자
- **[[015_datanode|데이터노드]] ([[015_datanode|DataNode]])** | HDFS에서 쪼개진 실제 128MB 블록 덩어리를 물리 하드디스크에 보관하는 수많은 일꾼 노드
- **[[190_split_brain_zookeeper_fencing_quorum|스플릿 브레인]] ([[190_split_brain_zookeeper_fencing_quorum|Split Brain]])** | [[014_namenode|NameNode]] HA([[456_dual_redundancy|이중화]]) 구성 시 두 마스터가 동시에 자기가 대장이라고 주장해 장부가 꼬이는 치명적 장애 현상
- **[[178_parquet_rle_encoding_columnar_compression|파케이]] ([[178_parquet_rle_encoding_columnar_compression|Parquet]]) 포맷** | HDFS 저장 효율을 극대화하기 위해 행(Row)이 아닌 열(Column) 단위로 [[347_compaction|압축]]하여 저장하는 빅데이터 특화 [[501_file_definition_logical_record|파일]] 구조
- **[[019_data_locality|데이터 지역성]] ([[019_data_locality|Data Locality]])** | 네트워크 전송 비용을 없애기 위해, HDFS 블록이 보관된 [[015_datanode|DataNode]] 위에서 연산([[018_mapreduce|MapReduce]])을 직접 실행시키는 철학

### 📈 관련 키워드 및 발전 흐름도

```text
[GFS (Google File System) — 대규모 분산 파일시스템 설계 원리 제시]
    │
    ▼
[HDFS (Hadoop Distributed File System) — GFS 영감, 블록 분산 저장·복제]
    │
    ▼
[NameNode / DataNode — 메타데이터 중앙 관리 + 실제 블록 분산 저장 구조]
    │
    ▼
[HDFS Federation — 다수 NameNode로 네임스페이스 수평 확장]
    │
    ▼
[클라우드 오브젝트 스토리지 (S3/GCS) — HDFS 이후 데이터 레이크 저장소 주류]
```

이 흐름은 GFS 논문에서 영감을 받은 HDFS가 [[843_hadoop_rack_awareness_data_replication_topology|하둡]] 생태계의 핵심 [[136_variance|분산]] 저장 계층으로 자리잡고, 페더레이션 확장을 거쳐 클라우드 [[494_object_storage|오브젝트 스토리지]]로 대체·보완되는 진화 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 영화가 너무 길어서 내 스마트폰(하나의 디스크)에 다 안 들어갈 때, 영화를 10분짜리 조각(블록)들로 싹둑싹둑 잘라요.
2. 그리고 친구들 스마트폰 100대에 조각들을 3개씩 똑같이 복사해서 나누어 저장해 두는 시스템이 HDFS예요.
3. 이렇게 하면 한 친구 폰이 고장 나도 다른 친구 폰에 복사본이 있어서 영화가 절대 사라지지 않고 무사히 지켜지는 놀라운 [[001_dikw_pyramid|데이터]] 저장 창고랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 13 / 258

← **이전**: [[012_apache_hadoop|12. 아파치 하둡 (Apache Hadoop) - 대용량 데이터 분산 저장 및 병렬 처리 자바 오픈소스 프레임워크]]
**다음**: [[014_namenode|14. 네임노드 (NameNode) - 파일 디렉터리, 블록 맵핑 메타데이터 관리 마스터 노드 (SPOF 존재)]] →

---
