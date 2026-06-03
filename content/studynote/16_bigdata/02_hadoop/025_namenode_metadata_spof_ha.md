---
title: 03. 네임노드 (NameNode) - 메타데이터 관리와 고가용성
date: '2026-03-04'
tags:
- hadoop
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
- **HDFS의 중앙 사령탑**: [[014_namenode|네임노드]]([[014_namenode|NameNode]])는 [[001_dikw_pyramid|데이터]]가 저장된 위치, [[501_file_definition_logical_record|파일]] 권한, [[506_directory_structure_symbol_table|디렉터리]] 구조 등 [[501_file_definition_logical_record|파일]] 시스템의 모든 [[012_metadata|메타데이터]]([[061_namespace|Namespace]])를 메모리(RAM) 위에서 통제하는 단일 [[172_maas_mobility_as_a_service|마스]]터 서버입니다.
- **[[454_spof|SPOF]] ([[454_spof|단일 장애점]]) 한계 극복**: [[459_quic_fec_forward_error_correction|초기]] [[843_hadoop_rack_awareness_data_replication_topology|하둡]]에서는 [[014_namenode|네임노드]] 서버 한 대가 물리적으로 고장 나면 전체 수백 대 클러스터의 [[001_dikw_pyramid|데이터]]가 미아가 되는 치명적 약점이 있었으나, [[843_hadoop_rack_awareness_data_replication_topology|하둡]] 2.0 HA(고가용성) 아키텍처로 이를 완벽히 방어합니다.
- **[[001_dikw_pyramid|데이터]] 흐름의 병목 방지 설계**: 클라이언트가 [[501_file_definition_logical_record|파일]]을 읽을 때 [[014_namenode|네임노드]]는 "[[001_dikw_pyramid|데이터]]가 어디 있는지 지도"만 던져주며 빠지고, 실제 기가바이트의 [[001_dikw_pyramid|데이터]] 다운로드는 워커([[015_datanode|데이터노드]])와 클라이언트 간 [[120_direct_communication|직접 통신]]으로 이루어져 중앙 서버 네트워크 과부하를 막습니다.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
수천 대의 깡통 서버(워커)에 [[001_dikw_pyramid|데이터]]를 잘게 쪼개 저장([[013_hdfs|HDFS]])해 두면, 누군가는 "어느 서버에 어떤 조각이 있는지" 완벽하게 기록하는 꼼꼼한 총괄 장부가 필요합니다. 이 장부를 쥔 단일 통제관이 바로 [[014_namenode|네임노드]]입니다. 
빠른 [[501_file_definition_logical_record|파일]] 탐색을 위해 모든 [[506_directory_structure_symbol_table|디렉터리]] 트리 정보를 하드디스크가 아닌 RAM(메모리)에 통째로 띄워놓고 응답하므로 엄청나게 빠르지만, 만약 전원이 나가 메모리가 날아가면 클러스터는 즉시 사망하는 아찔한 외줄타기를 하는 [[172_maas_mobility_as_a_service|마스]]터 서버이기도 합니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[[843_hadoop_rack_awareness_data_replication_topology|하둡]] 2.0 고가용성(High [[452_availability|Availability]], HA) 아키텍처에서는 Active와 Standby 두 대의 [[014_namenode|네임노드]]가 상호 보완합니다.

```text
+---------------------------------+      +---------------------------------+
|        Active NameNode          |      |       Standby NameNode          |
|  - Manages HDFS Namespace       |      |  - Synchronizes via Journal     |
|  - Receives Client Requests     |      |  - Ready for Failover           |
+---------------+-----------------+      +---------------+-----------------+
                |                                        |
                v                                        v
+--------------------------------------------------------------------------+
|                        JournalNodes (Quorum)                             |
|                        (Edits Log Synchronization)                       |
+--------------------------------------------------------------------------+
```

1. **FsImage & Edits Log**: 메모리 상태를 날리지 않기 위해, [[014_namenode|네임노드]]는 [[501_file_definition_logical_record|파일]] 변경 내역(Edits)을 디스크에 계속 [[568_logs_distributed_logging_elk_fluentd|로그]]로 쓰고 정기적으로 메모리 덤프 이미지(FsImage)를 구워냅니다.
2. **저널 노드 (JournalNodes)**: [[483_active_vs_passive_ftp|Active]] 서버가 죽는 순간을 대비하여, Active가 변경 사항(Edits)을 처리할 때마다 독립된 저널 노드 3대에 [[212_synchronization_mechanisms|동기화]] 기록을 날립니다. Standby 서버는 이 저널 노드에서 [[568_logs_distributed_logging_elk_fluentd|로그]]를 계속 빨아들여 Active와 똑같은 메모리 지도를 유지합니다.
3. **[[798_distributed_lock_zookeeper_consensus|Zookeeper]] 리더 선출**: 아파치 주키퍼가 감시하다가 [[483_active_vs_passive_ftp|Active]] 서버가 핑에 응답하지 않으면, 찰나의 순간에 Standby 서버를 Active로 승격시켜 사용자는 장애를 전혀 느끼지 못하게([[300_failover_architecture|Failover]]) 조치합니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 아키텍처 구분 | 단일 [[014_namenode|NameNode]] ([[843_hadoop_rack_awareness_data_replication_topology|하둡]] 1.0) | HA [[014_namenode|NameNode]] ([[843_hadoop_rack_awareness_data_replication_topology|하둡]] 2.0+) | [[013_hdfs|HDFS]] [[543_federation|Federation]] ([[061_namespace|네임스페이스]] 연합) |
| :--- | :--- | :--- | :--- |
| **서버 구성** | [[014_namenode|NameNode]] 1대 + 보조(Secondary) 1대 | [[483_active_vs_passive_ftp|Active]] 1대 + Standby 1대 | 여러 세트의 [[014_namenode|NameNode]] 묶음 운용 |
| **[[454_spof|SPOF]] 해결 여부** | ❌ (Primary 죽으면 클러스터 정지, 보조는 [[555_backup_and_restore_strategy|백업]] 용도일 뿐) | ✅ (죽으면 Standby로 즉각 무정지 절체) | ✅ ([[064_relation_domain|도메인]]별 [[172_maas_mobility_as_a_service|마스]]터 분리로 장애 반경 축소) |
| **메모리 한계 확장** | 메모리 꽉 차면 더 이상 [[501_file_definition_logical_record|파일]] 추가 불가 | 메모리 한계량 한 대(128GB 등) 스펙에 묶임 | `/user`, `/log` 등 [[506_directory_structure_symbol_table|디렉터리]]별로 [[172_maas_mobility_as_a_service|마스]]터를 나눠 메모리 무한 확장 가능 |
| **운영 복잡도** | 구조가 단순하여 관리가 쉬움 | [[798_distributed_lock_zookeeper_consensus|Zookeeper]], JournalNode 운영 난이도 상승 | [[172_maas_mobility_as_a_service|마스]]터 여러 대를 묶어 관리하므로 아키텍처 고난이도 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
- **메모리 사이즈 사이징 (Sizing)**: [[501_file_definition_logical_record|파일]]과 블록 1개당 [[014_namenode|네임노드]] 메모리를 150 [[074_byte|Byte]] 점유한다는 공식을 철저히 암기해야 합니다. 1억 개의 [[501_file_definition_logical_record|파일]]을 올리려면 [[014_namenode|네임노드]] JVM 힙 메모리를 최소 15GB 이상 물리적으로 확보하는 인프라 용량 계획(Capacity Planning)이 [[001_dikw_pyramid|데이터]] 아키텍트의 필수 과제입니다.
- **[[190_split_brain_zookeeper_fencing_quorum|스플릿 브레인]] ([[190_split_brain_zookeeper_fencing_quorum|Split Brain]]) 방지 방벽**: [[014_namenode|네임노드]] HA 구성 시 두 서버가 찰나의 네트워크 단절로 서로 "내가 진짜 리더다"라고 우기며 [[001_dikw_pyramid|데이터]]를 동시에 쓰려 하면 클러스터 [[501_file_definition_logical_record|파일]]맵이 영구 파괴됩니다. 주키퍼 펜싱(Fencing) 스크립트를 통해 죽은 줄 알았던 구 리더 서버의 전원 [[446_port_and_bus|포트]]를 물리적 차단(STONITH)하는 무자비한 방어막을 반드시 [[009_config|설정]]해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
[[014_namenode|네임노드]]의 고가용성 구조 완성 덕분에 [[843_hadoop_rack_awareness_data_replication_topology|하둡]] 클러스터는 은행 등 미션 크리티컬한 엔터프라이즈 환경에서도 99.99% 업타임을 보장받게 되었습니다. 수천 대 워커의 심장을 단 2대의 [[172_maas_mobility_as_a_service|마스]]터가 철통같이 통제하는 구조는 이후 등장한 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] [[075_kubernetes_k8s_cluster_architecture|마스터 노드]], [[179_kafka_flink_watermark_time_window|카프카]] 컨트롤러 등 [[136_variance|분산]] [[172_maas_mobility_as_a_service|마스]]터-슬레이브 디자인의 확고한 교과서 아키텍처로 자리 잡았습니다.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **선행 개념**: [[013_hdfs|HDFS]], [[172_maas_mobility_as_a_service|마스]]터-워커 [[136_variance|분산]] 아키텍처
- **핵심 기술**: FsImage, Edits Log, HA (High [[452_availability|Availability]]), 주키퍼([[798_distributed_lock_zookeeper_consensus|Zookeeper]])
- **확장 및 응용**: [[013_hdfs|HDFS]] [[543_federation|Federation]], [[190_split_brain_zookeeper_fencing_quorum|Split Brain]], Fencing, 작은 [[501_file_definition_logical_record|파일]] 병목

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: HDFS, 마스터-워커 분산 아키텍처]
    │
    ▼
[핵심 기술: FsImage, Edits Log, HA (High Availability), 주키퍼(Zookeeper)]
    │
    ▼
[확장 및 응용: HDFS Federation, Split Brain, Fencing, 작은 파일 병목]
```

이 흐름도는 선행 개념: [[013_hdfs|HDFS]], [[172_maas_mobility_as_a_service|마스]]터-워커 [[136_variance|분산]] 아키텍처에서 출발해 확장 및 응용: [[013_hdfs|HDFS]] [[543_federation|Federation]], [[190_split_brain_zookeeper_fencing_quorum|Split Brain]], Fencing, 작은 [[501_file_definition_logical_record|파일]] 병목까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 100만 권의 책이 있는 거대한 도서관에서, 오직 '안내 데스크 할아버지([[014_namenode|네임노드]])' 혼자만 어느 책이 몇 번 꽂이에 있는지 지도를 외우고 있어요.
2. 만약 할아버지가 화장실에 가거나 쓰러지면 도서관이 멈추니까, 바로 옆에 똑같은 지도를 복사해서 들고 대기 중인 '쌍둥이 동생(Standby)'을 세워둔 거예요.
3. 책을 꺼내오는 힘든 일은 다른 직원들([[015_datanode|데이터노드]])이 직접 하니까, 할아버지는 안내만 손가락으로 슉슉 지정해 줘도 절대 지치지 않는답니다!
