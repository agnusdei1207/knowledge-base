+++
weight = 203
title = "203. 하둡 HDFS (Hadoop Distributed File System) 블록 복제 내결함성"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[013_hdfs|HDFS]] ([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[553_distributed_file_system|Distributed File System]])는 [[501_file_definition_logical_record|파일]]을 고정 크기 블록(128MB)으로 분할하고, 각 블록을 여러 DataNode에 자동 [[016_replication_factor|복제]](기본 3회)하여, 범용 하드웨어 위에서 페타바이트급 [[136_variance|분산]] 저장을 실현한다.
> 2. **가치**: 블록 [[016_replication_factor|복제]]와 [[017_rack_awareness|랙 인지]]([[017_rack_awareness|Rack Awareness]]) 배치를 통해 단일 노드 또는 랙 단위 장애에도 무중단 [[001_dikw_pyramid|데이터]] 접근을 보장하며, MapReduce의 [[019_data_locality|데이터 지역성]]([[019_data_locality|Data Locality]])을 활용해 네트워크 전송 없이 처리한다.
> 3. **판단 포인트**: 기술사 논술에서는 NameNode의 메모리 내 [[203_metadata_management|메타데이터 관리]] 한계, 블록 크기 선택 기준(대용량 순차 접근 최적화), [[016_replication_factor|복제]] 계수와 저장 비용 트레이드오프를 명확히 서술해야 한다.

---

## Ⅰ. 개요 및 필요성

### [[843_hadoop_rack_awareness_data_replication_topology|하둡]]([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]]) 등장 배경

2003~2006년 구글이 발표한 세 편의 논문 — GFS (Google [[501_file_definition_logical_record|File]] System), [[018_mapreduce|MapReduce]], BigTable — 이 [[843_hadoop_rack_awareness_data_replication_topology|하둡]]의 탄생 기반이 되었다. 야후(Yahoo)의 더그 커팅(Doug Cutting)이 [[191_oss_license_compliance|오픈소스]]로 구현한 HDFS는 GFS의 [[191_oss_license_compliance|오픈소스]] 대체제이다.

| 구글 논문 | 발표 연도 | [[843_hadoop_rack_awareness_data_replication_topology|하둡]] 구현체 |
|:---|:---|:---|
| GFS (Google [[501_file_definition_logical_record|File]] System) | 2003 | [[013_hdfs|HDFS]] |
| [[018_mapreduce|MapReduce]] | 2004 | [[395_hadoop_mapreduce_disk_bottleneck|Hadoop MapReduce]] |
| BigTable | 2006 | Apache [[543_hbase|HBase]] |

### [[013_hdfs|HDFS]] 설계 철학

HDFS는 "고가 하드웨어를 믿지 말라"는 철학에서 출발한다. 수천 대의 범용(Commodity) 서버를 묶어, 어느 서버가 장애를 일으켜도 [[001_dikw_pyramid|데이터]]가 손실되지 않도록 설계되었다.

```
HDFS 설계 원칙
┌────────────────────────────────────────────────────────┐
│  원칙 1: 하드웨어 장애는 예외가 아니라 정상 상황이다    │
│  원칙 2: 대용량 파일 순차 접근에 최적화 (스트리밍 읽기) │
│  원칙 3: Write-Once-Read-Many (쓰기 1회, 읽기 다수)     │
│  원칙 4: 범용 하드웨어로 구성 (저비용 Scale-Out)        │
└────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: HDFS는 "클라우드 이전 시대의 구글 드라이브"다. [[501_file_definition_logical_record|파일]] 하나를 3군데 복사해서 저장하기 때문에, 내 컴퓨터가 고장나도 다른 컴퓨터에서 [[501_file_definition_logical_record|파일]]을 찾을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[013_hdfs|HDFS]] 아키텍처: NameNode와 [[015_datanode|DataNode]]

HDFS는 마스터-슬레이브(Master-Slave) 아키텍처를 따른다.

```
HDFS 전체 아키텍처
┌────────────────────────────────────────────────────────────┐
│                         클라이언트                          │
└───────────────────────────┬────────────────────────────────┘
                            │ ① 파일 위치 요청
                            ▼
┌──────────────────────────────────────────────────────────┐
│                      NameNode (1대)                       │
│  - 파일 시스템 네임스페이스 (트리 구조)                    │
│  - 파일 ↔ 블록 매핑 (메모리 내 유지)                      │
│  - 블록 ↔ DataNode 위치 매핑 (FsImage + EditLog)          │
└───────┬──────────────────────┬───────────────────────────┘
        │ ② 블록 위치 응답     │ 하트비트/블록 리포트
        │                      ▼
        │          ┌─────────────────────┐
        │          │ Secondary NameNode  │
        │          │ (체크포인팅 전용)    │
        │          └─────────────────────┘
        │
        ▼ ③ 직접 데이터 접근
┌───────────────────────────────────────────────────────────┐
│                     DataNode 클러스터                      │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐  │
│  │DataNode1│   │DataNode2│   │DataNode3│   │DataNode4│  │
│  │ Blk A1  │   │ Blk A2  │   │ Blk A3  │   │ Blk B1  │  │
│  │ Blk C1  │   │ Blk B2  │   │ Blk C2  │   │ Blk B3  │  │
│  └─────────┘   └─────────┘   └─────────┘   └─────────┘  │
└───────────────────────────────────────────────────────────┘
```

| [[603_component_independent_deployment_unit|컴포넌트]] | 역할 | 핵심 특성 |
|:---|:---|:---|
| [[014_namenode|NameNode]] | [[501_file_definition_logical_record|파일]] 시스템 [[203_metadata_management|메타데이터 관리]] | 전체 네임스페이스를 RAM에 유지 (GB 단위) |
| [[015_datanode|DataNode]] | 실제 블록 저장·[[090_service_kubernetes_network_load_balancing|서비스]] | 로컬 [[501_file_definition_logical_record|파일]]시스템에 블록 [[501_file_definition_logical_record|파일]]로 저장 |
| Secondary [[014_namenode|NameNode]] | FsImage [[071_checkpointing|체크포인팅]] | EditLog 병합으로 [[014_namenode|NameNode]] 부담 경감 (HA 대체 아님!) |
| Standby [[014_namenode|NameNode]] | HA (High [[452_availability|Availability]]) 구성 | [[483_active_vs_passive_ftp|Active]] [[014_namenode|NameNode]] 장애 시 자동 전환 |

### 블록 단위 저장 (Block-Based Storage)

HDFS는 [[501_file_definition_logical_record|파일]]을 **128MB** (기본값) 블록으로 분할하여 저장한다.

```
파일 → 블록 분할 예시
┌─────────────────────────────────────────────────────────┐
│  파일: movie.mp4 (384MB)                                 │
│                                                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │
│  │  블록 A       │ │  블록 B       │ │  블록 C       │     │
│  │  128MB        │ │  128MB        │ │  128MB        │     │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘     │
│         │ 복제 ×3        │ 복제 ×3        │ 복제 ×3      │
│  DN1,DN2,DN3       DN2,DN3,DN4       DN1,DN3,DN4        │
└─────────────────────────────────────────────────────────┘
```

| 블록 크기 | 이유 | 트레이드오프 |
|:---|:---|:---|
| 128MB (기본값) | 대용량 순차 접근 최적화, [[014_namenode|NameNode]] [[012_metadata|메타데이터]] 감소 | 소규모 [[501_file_definition_logical_record|파일]]에는 낭비 |
| 64MB (이전 [[288_version_ihl_tos_total_length|버전]]) | 구버전 기본값 | 현재는 권장하지 않음 |
| 256MB (대용량) | 매우 큰 [[501_file_definition_logical_record|파일]] 처리 최적화 | [[014_namenode|NameNode]] 메모리 더 절약 |

### [[016_replication_factor|복제]] 계수 3과 [[017_rack_awareness|랙 인지]] 배치

HDFS의 기본 [[016_replication_factor|복제]] 계수([[016_replication_factor|Replication Factor]])는 3이며, [[017_rack_awareness|랙 인지]]([[017_rack_awareness|Rack Awareness]]) 정책으로 배치한다.

```
랙 인지 복제 배치 정책
┌─────────────────────────────────────────────────────────────┐
│  데이터센터                                                   │
│                                                             │
│  ┌──────────── Rack 1 ────────────┐  ┌─── Rack 2 ────────┐  │
│  │  DataNode1 ←── 복제본 1 (첫번째)│  │  DataNode3 ←── 복제본 3│  │
│  │  DataNode2 ←── 복제본 2 (같은 랙)│  │                   │  │
│  └─────────────────────────────────┘  └───────────────────┘  │
│                                                             │
│  정책: 2개는 같은 랙, 1개는 다른 랙                          │
│  → 랙 내 스위치 장애 시에도 다른 랙 복제본으로 서비스 가능    │
└─────────────────────────────────────────────────────────────┘
```

| [[016_replication_factor|복제]] 배치 | 이유 |
|:---|:---|
| 1번 [[016_replication_factor|복제]]: [[289_cqrs_db|쓰기]] 클라이언트와 같은 랙 [[015_datanode|DataNode]] | [[289_cqrs_db|쓰기]] [[282_performance_tactics|성능]] 최적화 |
| 2번 [[016_replication_factor|복제]]: 같은 랙의 다른 [[015_datanode|DataNode]] | 랙 내 네트워크 활용 |
| 3번 [[016_replication_factor|복제]]: 다른 랙의 [[015_datanode|DataNode]] | 랙 단위 장애 대응 |

📢 **섹션 요약 비유**: 블록 [[016_replication_factor|복제]]는 "중요한 서류를 사무실 서랍([[016_replication_factor|복제]]1), 회의실 [[501_file_definition_logical_record|파일]]함([[016_replication_factor|복제]]2), 다른 건물 창고([[016_replication_factor|복제]]3)에 나눠 보관"하는 것이다. 건물 하나가 불이 나도 다른 건물 창고에서 꺼낼 수 있다.

---

## Ⅲ. 비교 및 연결

### 내결함성 메커니즘 상세

| 장애 유형 | [[013_hdfs|HDFS]] 감지 방법 | [[658_ir_recovery|복구]] 방법 |
|:---|:---|:---|
| [[015_datanode|DataNode]] 장애 | 하트비트 10분 무응답 | NameNode가 해당 블록 재복제 지시 |
| 블록 [[001_dikw_pyramid|데이터]] 손상 | [[112_checksum|체크섬]]([[112_checksum|Checksum]]) [[395_verification_process_review|검증]] | 다른 [[016_replication_factor|복제]]본으로 대체 후 재복제 |
| 랙 장애 | 블록 리포트 누락 | 다른 랙의 [[016_replication_factor|복제]]본 활용 |
| [[014_namenode|NameNode]] 장애 | [[798_distributed_lock_zookeeper_consensus|ZooKeeper]] 기반 모니터링 | Standby [[014_namenode|NameNode]] 자동 전환 (HA) |

### [[019_data_locality|데이터 지역성]] ([[019_data_locality|Data Locality]])

MapReduce는 "[[001_dikw_pyramid|데이터]]를 컴퓨팅으로 이동"시키는 대신 "컴퓨팅을 [[001_dikw_pyramid|데이터]]로 이동"시키는 [[019_data_locality|데이터 지역성]] 원칙을 따른다.

```
데이터 지역성 원칙
┌─────────────────────────────────────────────────────────┐
│  전통 방식 (데이터 → 컴퓨팅):                            │
│  DataNode ──[네트워크]──▶ 중앙 처리 서버 (병목 발생)     │
│                                                         │
│  MapReduce 방식 (컴퓨팅 → 데이터):                       │
│  DataNode ──[로컬 실행]──▶ Map Task 직접 실행            │
│  네트워크 전송 없음 → 처리 속도 대폭 향상                 │
└─────────────────────────────────────────────────────────┘
```

| 지역성 레벨 | 설명 | [[282_performance_tactics|성능]] |
|:---|:---|:---|
| [[001_dikw_pyramid|데이터]] 로컬 ([[001_dikw_pyramid|Data]]-Local) | Map Task와 블록이 동일 노드 | 최고 (로컬 디스크 읽기) |
| 랙 로컬 (Rack-Local) | 같은 랙의 다른 노드 | 중간 (내부 [[238_switch_operation_principles|스위치]] 경유) |
| 오프 랙 (Off-Rack) | 다른 랙의 노드 | 최저 (WAN급 [[015_지연_데이터_관점|지연]]) |

### [[013_hdfs|HDFS]] vs 기타 [[136_variance|분산]] [[501_file_definition_logical_record|파일]]시스템 비교

| 항목 | [[013_hdfs|HDFS]] | GFS (Google [[501_file_definition_logical_record|File]] System) | Amazon S3 |
|:---|:---|:---|:---|
| 접근 방식 | POSIX 유사 [[501_file_definition_logical_record|파일]] [[014_api_posix|API]] | 독점 [[014_api_posix|API]] | [[477_rest_api_architecture|REST API]] |
| [[194_consistency_database_integrity|일관성]] | 강한 [[194_consistency_database_integrity|일관성]] | [[412_relaxed_consistency|완화된 일관성]] | 최종 [[194_consistency_database_integrity|일관성]] |
| 적합 사례 | [[228_batch_processing_hadoop_spark|배치 처리]] ([[018_mapreduce|MapReduce]]) | 구글 내부 [[090_service_kubernetes_network_load_balancing|서비스]] | 오브젝트 저장, 클라우드 DL |
| [[501_file_definition_logical_record|파일]] 수정 | Append 전용 | Append 전용 | 덮어쓰기 가능 |

📢 **섹션 요약 비유**: HDFS의 [[019_data_locality|데이터 지역성]]은 "요리사가 재료 창고 옆에서 요리하는 것"이다. 재료를 멀리 있는 주방으로 옮기는 대신(네트워크 전송), 창고 바로 옆에 조리대를 설치해(Map Task를 DataNode에서 실행) 이동 시간을 없앤다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[013_hdfs|HDFS]] 운영 핵심 파라미터

| 파라미터 | 기본값 | 튜닝 방향 | 이유 |
|:---|:---|:---|:---|
| [[034_dfs|dfs]].[[016_replication_factor|replication]] | 3 | 2 (개발/테스트) | 저장 비용 절감 |
| [[034_dfs|dfs]].block.size | 128MB | 256MB (대용량 [[501_file_definition_logical_record|파일]]) | [[014_namenode|NameNode]] [[012_metadata|메타데이터]] 감소 |
| [[034_dfs|dfs]].[[014_namenode|namenode]].handler.count | [[489_raid_10_hybrid|10]] | CPU 코어 수 × 20 | [[014_namenode|NameNode]] [[126_rpc|RPC]] 병목 해소 |
| [[034_dfs|dfs]].[[015_datanode|datanode]].du.reserved | 0 | 10GB | [[015_datanode|DataNode]] 디스크 여유 공간 확보 |

### 소규모 [[501_file_definition_logical_record|파일]] 문제 ([[269_small_file_problem_data_lakehouse|Small File Problem]])

HDFS의 가장 큰 실무 문제 중 하나는 수백만 개의 소규모 [[501_file_definition_logical_record|파일]]이다. 각 [[501_file_definition_logical_record|파일]]마다 최소 1개의 블록 [[012_metadata|메타데이터]]가 [[014_namenode|NameNode]] 메모리를 차지하기 때문이다.

```
소규모 파일 문제
┌─────────────────────────────────────────────────────────┐
│  1KB 파일 1,000만 개 저장 시:                            │
│  → NameNode 메모리: 약 150 bytes × 10,000,000 = 1.5GB   │
│  → 실제 데이터: 10GB (전체의 6.7%)                       │
│  → NameNode 메모리가 데이터보다 더 빨리 소진됨!           │
│                                                         │
│  해결책:                                                 │
│  - HAR (Hadoop Archive): 소규모 파일 묶음 저장           │
│  - SequenceFile: 키-값 쌍으로 소규모 파일 병합           │
│  - S3 + Parquet: 소규모 파일을 컬럼형으로 병합 저장      │
└─────────────────────────────────────────────────────────┘
```

### 기술사 논술 핵심 포인트

1. **[[014_namenode|NameNode]] [[454_spof|SPOF]]**: HDFS의 근본 약점은 단일 [[014_namenode|NameNode]]. [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 2.x부터 HA (High [[452_availability|Availability]]) [[014_namenode|NameNode]] + ZooKeeper로 해결
2. **[[016_replication_factor|복제]] vs 이레이저 코딩**: [[016_replication_factor|복제]] 계수 3은 200% 스토리지 오버헤드. [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 3.x의 Erasure Coding으로 50% 이내로 줄임
3. **[[019_data_locality|데이터 지역성]] 저하**: 클라우드 환경(S3 분리)에서는 HDFS의 지역성 장점이 사라짐 → 컬럼형 포맷([[178_parquet_rle_encoding_columnar_compression|Parquet]]) + 파티셔닝으로 보완

📢 **섹션 요약 비유**: [[013_hdfs|HDFS]] 운영의 핵심 딜레마는 "[[016_replication_factor|복제]]를 많이 할수록 안전하지만 저장 공간이 낭비된다"는 것이다. 마치 중요한 문서를 복사해서 여러 금고에 넣을수록 안전하지만, 금고 임대료가 늘어나는 것과 같다. Erasure Coding은 "문서를 조각내서 XOR 패리티로 저장"해 금고 수를 줄이는 방법이다.

---

## Ⅴ. 기대효과 및 결론

### [[013_hdfs|HDFS]] 도입 효과

| 효과 영역 | 수치 예시 | 설명 |
|:---|:---|:---|
| 저장 비용 | 기존 [[493_san_storage_area_network|SAN]] 대비 80% 절감 | 범용 [[465_hdd_structure|HDD]] 서버 활용 |
| [[452_availability|가용성]] | 99.9% (3 [[016_replication_factor|복제]] 기준) | 노드 장애 자동 [[658_ir_recovery|복구]] |
| 처리 병렬성 | 선형 확장 | 노드 추가 = [[139_throughput|처리량]] 비례 증가 |
| 확장성 | 수천 노드, 수백 PB | 야후 등 실제 수만 노드 운영 사례 |

### HDFS의 한계와 발전 방향

| 한계 | 발전 방향 |
|:---|:---|
| [[014_namenode|NameNode]] [[454_spof|SPOF]] | HA [[014_namenode|NameNode]] + [[798_distributed_lock_zookeeper_consensus|ZooKeeper]] [[543_federation|Federation]] |
| 소규모 [[501_file_definition_logical_record|파일]] 취약 | [[178_parquet_rle_encoding_columnar_compression|Parquet]]/ORC + [[012_metadata|메타데이터]] [[347_compaction|압축]] |
| 높은 [[016_replication_factor|복제]] 오버헤드 | [[681_erasure_coding|Erasure Coding]] (RS-6-3 등) |
| 클라우드 S3 분리 | 컴퓨팅-스토리지 분리 아키텍처([[147_delta_lake|Delta Lake]], Iceberg) |

### 결론

HDFS는 빅데이터 [[136_variance|분산]] 저장의 기준을 세운 혁신적 시스템이지만, 클라우드 시대로 전환되며 컴퓨팅-스토리지 분리 아키텍처에 그 역할을 넘겨주고 있다. 그러나 HDFS의 핵심 개념(블록 [[136_variance|분산]], [[016_replication_factor|복제]], [[019_data_locality|데이터 지역성]])은 현대의 오브젝트 스토리지와 [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]](Iceberg, [[147_delta_lake|Delta Lake]])에 여전히 계승되어 있다.

📢 **섹션 요약 비유**: HDFS는 "빅데이터 시대의 기초 공사"다. 현대 빌딩(클라우드 [[001_dikw_pyramid|데이터]] 플랫폼)은 더 세련됐지만, 그 기초([[136_variance|분산]] 저장·[[016_replication_factor|복제]]·지역성 원칙)는 HDFS에서 가져온 것이다.

---

### 📌 관련 개념 맵
| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 구성 요소 | [[014_namenode|NameNode]] | [[013_hdfs|HDFS]] [[012_metadata|메타데이터]] 중앙 관리자 |
| 구성 요소 | [[015_datanode|DataNode]] | 실제 블록 [[001_dikw_pyramid|데이터]] 저장·[[090_service_kubernetes_network_load_balancing|서비스]] 노드 |
| 구성 요소 | Secondary [[014_namenode|NameNode]] | [[071_checkpointing|체크포인팅]] 전용 (HA가 아님) |
| 연관 기술 | [[018_mapreduce|MapReduce]] | [[019_data_locality|데이터 지역성]] 활용한 [[136_variance|분산]] 처리 |
| 상위 개념 | [[020_yarn|YARN]] | [[013_hdfs|HDFS]] 위의 리소스 관리 레이어 |
| 이론적 배경 | GFS (Google [[501_file_definition_logical_record|File]] System) | HDFS의 원조 논문 |
| 발전 방향 | [[148_apache_iceberg|Apache Iceberg]] / [[147_delta_lake|Delta Lake]] | [[013_hdfs|HDFS]] 한계를 극복한 [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]] |
| 보완 기술 | [[681_erasure_coding|Erasure Coding]] | [[016_replication_factor|복제]] 오버헤드 감소 기술 |

### 👶 어린이를 위한 3줄 비유 설명
1. HDFS는 "레고 블록으로 엄청 큰 성을 쌓는 것"이에요. 큰 [[501_file_definition_logical_record|파일]] 하나를 128MB 블록 조각으로 나눠서, 여러 컴퓨터에 나눠 보관해요.

### 📈 관련 키워드 및 발전 흐름도

```text
단일 디스크 저장 → 용량 · 내구성 한계
    │
    ▼
HDFS (Hadoop Distributed File System)
    ├─► 블록 분할 (128MB) + 3중 복제 (Replication Factor)
    ├─► NameNode: 메타데이터 관리 (파일→블록 맵)
    └─► DataNode: 실제 블록 저장
    │
    ▼
Hadoop 2.x: HA NameNode · Federation
    │
    ▼
클라우드 오브젝트 스토리지: S3 · GCS (HDFS 대체)
```
2. 블록마다 3개씩 복사본을 만들어두기 때문에, 컴퓨터 한 대가 고장나도 다른 곳에서 레고 조각을 꺼낼 수 있어요.
3. NameNode는 "어떤 컴퓨터에 어떤 레고 조각이 있는지 기억하는 목록 책"이고, DataNode는 "실제로 레고를 보관하는 창고"예요.
