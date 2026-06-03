---
title: 680. HDFS (Hadoop Distributed File System)
date: '2026-05-08'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[013_hdfs|HDFS]] ([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[553_distributed_file_system|Distributed File System]])는 대용량 [[501_file_definition_logical_record|파일]]을 큰 블록으로 나눠 여러 범용 서버에 저장하는, [[139_throughput|처리량]] 중심의 [[553_distributed_file_system|분산 파일 시스템]]이다.
> 2. **가치**: 장비 고장을 전제로 [[016_replication_factor|복제]]와 [[019_data_locality|데이터 지역성]]으로 설계되어, 값싼 서버를 많이 묶어도 배치 분석과 [[568_logs_distributed_logging_elk_fluentd|로그]] 처리를 안정적으로 수행할 수 있다.
> 3. **판단 포인트**: HDFS는 작은 [[501_file_definition_logical_record|파일]]을 자주 수정하는 범용 [[501_file_definition_logical_record|파일]] 서버가 아니라, 한 번 쓰고 여러 번 읽는 대규모 분석 [[001_dikw_pyramid|데이터]] 저장에 최적화된 구조다.

---

## Ⅰ. 개요 및 필요성

HDFS는 수 페타바이트급 [[001_dikw_pyramid|데이터]]를 비싼 전용 스토리지 없이 처리해야 했던 빅데이터 시대의 요구에서 등장했다. Google [[501_file_definition_logical_record|File]] System (GFS)의 아이디어를 계승한 HDFS는, 값싼 범용 서버 여러 대가 자주 고장 나더라도 전체 [[001_dikw_pyramid|데이터]]는 계속 살아남도록 설계되었다. 즉, 장비를 절대 고장 나지 않게 만드는 대신, 고장이 나도 시스템이 버티게 만드는 철학이다.

이 철학은 저장뿐 아니라 연산 방식도 바꿨다. [[001_dikw_pyramid|데이터]]를 한곳으로 옮겨 계산하는 대신, [[001_dikw_pyramid|데이터]]가 있는 노드 근처에서 계산을 수행하는 [[019_data_locality|데이터 지역성]]을 적극 활용했다. 그래서 HDFS는 단순한 [[501_file_definition_logical_record|파일]] 저장소가 아니라, [[071_anova_analysis_of_variance_f_value_post_hoc|분산 분석]] 프레임워크와 함께 움직이는 “[[001_dikw_pyramid|데이터]]를 위한 작업장” 역할을 맡게 되었다.

- **📢 섹션 요약 비유**: HDFS는 통나무를 모두 본사로 실어 나른 뒤 자르는 방식이 아니라, 통나무가 있는 숲에 나무꾼을 보내 그 자리에서 작업하게 만드는 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

HDFS는 [[501_file_definition_logical_record|파일]]을 큰 블록으로 나누고, 각 블록을 여러 DataNode에 [[016_replication_factor|복제]]해 저장한다. [[501_file_definition_logical_record|파일]] 이름, 블록 목록, 블록 위치 같은 [[012_metadata|메타데이터]]는 NameNode가 관리하며, 실제 [[001_dikw_pyramid|데이터]] 본문은 DataNode들이 맡는다. 따라서 NameNode는 “어디에 무엇이 있는가”를 기억하는 두뇌이고, DataNode는 “실제 블록을 들고 있는 노동자”라고 볼 수 있다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| [[014_namenode|NameNode]] | [[501_file_definition_logical_record|파일]] 시스템 [[203_metadata_management|메타데이터 관리]] | 메모리 크기와 이중화가 중요 |
| [[015_datanode|DataNode]] | 실제 블록 저장 | 디스크 수와 네트워크 대역폭이 핵심 |
| 블록 (Block) | [[501_file_definition_logical_record|파일]]을 나누는 큰 저장 단위 | 큰 블록일수록 [[012_metadata|메타데이터]] 부담 완화 |
| [[016_replication_factor|복제]] ([[016_replication_factor|Replication]]) | 블록 사본을 여러 노드에 저장 | 일반적으로 3중 [[016_replication_factor|복제]]가 기본 |
| 랙 인식 배치 | 같은 장애 도메인에만 몰리지 않게 배치 | [[238_switch_operation_principles|스위치]]·랙 단위 장애 대응 |
| HA (High [[452_availability|Availability]]) [[014_namenode|NameNode]] | [[012_metadata|메타데이터]] [[454_spof|단일 장애점]] 완화 | 액티브-스탠바이 운영 필요 |

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ Client                                                                  │
│   │ metadata request                                                    │
│   ▼                                                                      │
│ NameNode ------------------------------------------------------┐         │
│   │ block locations                                            │         │
│   ▼                                                            │         │
│ DataNode 1  ->  DataNode 2  ->  DataNode 3                     │         │
│   block copy      block copy      block copy                   │         │
│                                                                 │         │
│ write pipeline : client writes once, replicas flow in order     │         │
└──────────────────────────────────────────────────────────────────────────┘
```

이 구조 덕분에 HDFS는 대용량 순차 읽기와 쓰기에서 매우 강하다. 블록 크기를 128메가바이트 또는 256메가바이트처럼 크게 잡으면 [[012_metadata|메타데이터]] 수가 줄어들고, 분석 작업은 블록이 있는 노드에서 실행되어 네트워크 이동량도 줄어든다. 대신 [[501_file_definition_logical_record|파일]] 중간을 자주 수정하거나, 아주 작은 [[501_file_definition_logical_record|파일]] 수백만 개를 관리하는 용도로는 비효율이 커진다.

- **📢 섹션 요약 비유**: HDFS는 큰 퍼즐 조각을 여러 친구에게 한 세트씩 나눠 주고, 조립 설명서는 반장이 들고 있는 구조와 같다. 친구 한 명이 빠져도 다른 친구들이 같은 조각을 가지고 있어 퍼즐을 다시 맞출 수 있다.

---

## Ⅲ. 비교 및 연결

HDFS는 일반 [[501_file_definition_logical_record|파일]] 서버나 [[494_object_storage|오브젝트 스토리지]]와 비슷해 보여도 목적이 다르다. 일반 [[501_file_definition_logical_record|파일]] 시스템은 세밀한 수정과 사용자 편의성에 강하고, [[494_object_storage|오브젝트 스토리지]]는 클라우드 확장성과 [[012_metadata|메타데이터]] [[164_policy|정책]]에 강하다. HDFS는 그보다 “대규모 분석 [[501_file_definition_logical_record|파일]]을 얼마나 싸고 안정적으로 흘려보낼 것인가”에 집중한다.

| 구분 | 일반 [[501_file_definition_logical_record|파일]] 시스템 | [[494_object_storage|오브젝트 스토리지]] | [[013_hdfs|HDFS]] |
| :--- | :--- | :--- | :--- |
| 주된 인터페이스 | [[501_file_definition_logical_record|파일]] 경로, 공유 [[295_protocol_field_tcp_udp_icmp|프로토콜]] | 객체 [[289_identification_flags_fragmentation_offset|식별자]], 웹 인터페이스 | [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[501_file_definition_logical_record|파일]] 인터페이스 |
| 핵심 최적화 | 범용 [[501_file_definition_logical_record|파일]] 작업 | 대규모 저장과 내구성 | 대용량 순차 [[139_throughput|처리량]] |
| [[001_dikw_pyramid|데이터]] 수정 | 자유로운 [[501_file_definition_logical_record|파일]] 수정 | 객체 재기록 중심 | 추가 쓰기와 순차 처리에 유리 |
| 강점 | 사용자 친화적 | 클라우드 확장성과 [[164_policy|정책]] | [[019_data_locality|데이터 지역성]] 기반 분석 |
| 약점 | 대규모 [[071_anova_analysis_of_variance_f_value_post_hoc|분산 분석]] 비효율 | [[501_file_definition_logical_record|파일]]시스템 의미론 약함 | 작은 [[501_file_definition_logical_record|파일]], 낮은 [[015_지연_데이터_관점|지연]] 랜덤 접근에 약함 |

이 때문에 HDFS는 MapReduce나 Spark 같은 [[071_anova_analysis_of_variance_f_value_post_hoc|분산 분석]]과 함께 사용할 때 가장 빛난다. 반면 POSIX (Portable [[001_operating_system_purpose|Operating System]] Interface) 수준의 범용 공유 저장소나 온라인 [[191_transaction_concept_states|트랜잭션]] 처리 (Online [[191_transaction_concept_states|Transaction]] Processing, [[327_hint_handoff|OLTP]]) [[001_dikw_pyramid|데이터]]베이스의 영속 스토리지로 쓰기에는 적합하지 않다. 즉, HDFS는 “분석을 위한 [[501_file_definition_logical_record|파일]] 시스템”이지 “모든 애플리케이션을 위한 [[501_file_definition_logical_record|파일]] 시스템”은 아니다.

- **📢 섹션 요약 비유**: HDFS는 회사 공용 서랍장이 아니라, 공장 원자재를 대량으로 쌓아 두고 바로 생산 라인에 투입하기 좋은 대형 창고와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **[[568_logs_distributed_logging_elk_fluentd|로그]] [[208_data_lake_schema_on_read|데이터 레이크]]**
   - 웹 서비스와 장비에서 나오는 [[568_logs_distributed_logging_elk_fluentd|로그]]를 날짜 단위 대용량 [[501_file_definition_logical_record|파일]]로 적재한다.
   - 하루 단위 배치 분석이 많을수록 HDFS의 순차 처리 장점이 잘 드러난다.

2. **[[215_etl_vs_elt_pipeline|ETL]] (Extract, Transform, Load) 파이프라인**
   - 원천 [[001_dikw_pyramid|데이터]]를 HDFS에 쌓고, 변환 작업과 집계 작업을 [[136_variance|분산]] 실행한다.
   - [[001_dikw_pyramid|데이터]]가 노드 곳곳에 있어도 연산을 [[001_dikw_pyramid|데이터]] 근처로 보내 처리 비용을 줄일 수 있다.

3. **학습 [[001_dikw_pyramid|데이터]] 전처리**
   - 이미지나 텍스트를 대규모로 읽어 [[430_index_fast_full_scan|병렬]] 전처리해야 할 때 유용하다.
   - 다만 최근에는 [[494_object_storage|오브젝트 스토리지]]와 함께 혼합 사용되는 경우가 많다.

### 채택/회피 판단 체크포인트

- **채택이 유리한 경우**
  - 대형 [[501_file_definition_logical_record|파일]]을 반복적으로 배치 처리할 때
  - 저렴한 서버 여러 대로 저장과 분석을 함께 구성할 때
  - [[019_data_locality|데이터 지역성]], [[139_throughput|처리량]], 장애 허용성이 핵심일 때

- **회피가 유리한 경우**
  - 작은 [[501_file_definition_logical_record|파일]]이 매우 많아 [[014_namenode|NameNode]] 메모리 압박이 큰 경우
  - 범용 [[501_file_definition_logical_record|파일]] 공유나 저지연 상호작용형 저장소가 필요한 경우
  - 가상머신 ([[598_vm_migration_nic|Virtual Machine]]) 디스크나 [[327_hint_handoff|OLTP]] [[001_dikw_pyramid|데이터]]베이스처럼 세밀한 랜덤 쓰기가 중요한 경우

실무에서는 [[014_namenode|NameNode]] 이중화와 [[012_metadata|메타데이터]] 메모리 설계가 가장 중요하다. [[501_file_definition_logical_record|파일]] 수와 블록 수가 늘수록 [[014_namenode|NameNode]] 부담이 커지므로, 블록 크기 [[164_policy|정책]]과 작은 [[501_file_definition_logical_record|파일]] 병합 전략을 함께 세워야 한다. 또한 랙 인식 배치, [[016_replication_factor|복제]] 인수, 장애 [[658_ir_recovery|복구]] 시간 목표를 함께 조정해야 진짜 운영 가능한 HDFS가 된다.

- **📢 섹션 요약 비유**: [[013_hdfs|HDFS]] 운영은 창고를 많이 늘리는 일만이 아니라, 반장이 들고 있는 재고 장부가 너무 커지지 않게 정리 규칙까지 같이 만드는 일과 같다.

---

## Ⅴ. 기대효과 및 결론

HDFS는 값싼 하드웨어 위에서도 대용량 [[001_dikw_pyramid|데이터]] 저장과 배치 분석을 안정적으로 가능하게 만든 대표적 기술이다. [[016_replication_factor|복제]]와 [[019_data_locality|데이터 지역성]] 덕분에 하드웨어 고장을 특별한 사건이 아니라 일상적인 운영 조건으로 다룰 수 있게 했고, 이는 빅데이터 플랫폼의 대중화를 이끌었다. 대형 [[568_logs_distributed_logging_elk_fluentd|로그]], 이벤트, 원천 [[001_dikw_pyramid|데이터]] 보관소로서 HDFS가 가진 역사적 의미는 매우 크다.

다만 오늘날에는 [[494_object_storage|오브젝트 스토리지]]와 역할을 나누거나 함께 쓰는 경우가 많다. 클라우드 환경에서는 저장과 계산을 더 느슨하게 분리하는 추세가 강하고, 작은 [[501_file_definition_logical_record|파일]] 문제와 [[012_metadata|메타데이터]] 집중도 여전히 한계로 남는다. 그래서 HDFS는 **“범용 [[501_file_definition_logical_record|파일]] 시스템”이 아니라 “[[139_throughput|처리량]]과 [[019_data_locality|데이터 지역성]]을 중시하는 분석용 [[553_distributed_file_system|분산 파일 시스템]]”**으로 기억해야 한다.

- **📢 섹션 요약 비유**: HDFS는 무엇이든 넣는 책상이 아니라, 무거운 재료를 많이 쌓아 두고 공장처럼 흘려보내는 작업장에 더 가깝다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[014_namenode|NameNode]] | [[501_file_definition_logical_record|파일]]과 블록의 [[012_metadata|메타데이터]]를 기억하는 중앙 관리 노드다. |
| [[015_datanode|DataNode]] | 실제 [[001_dikw_pyramid|데이터]]를 담고 [[016_replication_factor|복제]]와 보고를 수행한다. |
| 블록 (Block) | [[501_file_definition_logical_record|파일]]을 대용량 조각으로 나눠 [[136_variance|분산]] 저장하게 해 준다. |
| [[016_replication_factor|복제]] | 장애 시에도 [[001_dikw_pyramid|데이터]] 가용성을 확보하는 기본 메커니즘이다. |
| 랙 인식 배치 | 동일 랙 장애가 전체 [[016_replication_factor|복제]]본을 동시에 잃지 않게 돕는다. |
| [[019_data_locality|데이터 지역성]] | 연산을 [[001_dikw_pyramid|데이터]] 가까이 보내 네트워크 비용을 줄이는 핵심 원리다. |
| [[543_federation|Federation]] | [[014_namenode|NameNode]] 부담을 여러 네임스페이스로 나누는 확장 방식이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
Google File System (GFS) 아이디어
        │
        ▼
HDFS 블록 복제 기반 분산 파일 저장
        │
        ▼
MapReduce / Spark와 결합한 데이터 지역성 분석
        │
        ▼
HA NameNode / Federation / 삭제 코딩 확장
        │
        ▼
오브젝트 스토리지와 공존하는 현대 데이터 레이크 구조
```

이 흐름은 [[136_variance|분산]] [[501_file_definition_logical_record|파일]] 저장이 단순 보관을 넘어, 대규모 분석 파이프라인의 실행 토대와 결합해 발전해 왔음을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. HDFS는 큰 책 한 권을 여러 장으로 나눠 여러 친구 집에 똑같이 나눠 두는 거예요.
2. 그래서 친구 한 명이 집에 없어도 다른 친구 집에서 책장을 다시 모을 수 있어요.
3. 그리고 숙제는 책을 학교로 다 가져오는 대신, 책이 있는 친구 집에서 바로 풀게 하는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 681 / 803

← **이전**: [[679_glusterfs|679. GlusterFS 분산 스토리지]]
**다음**: [[681_erasure_coding|681. Erasure Coding (삭제 코딩) HW 연산]] →

---
