---
title: "빅데이터 분산 처리 — Hadoop·MapReduce·HDFS (Hadoop MapReduce)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 133
---

# 📖 【암기용】 개념 완전 이해

> 목적: Hadoop, MapReduce, HDFS가 왜 함께 등장했는지 이해하게 만든다.

## 한눈에
- **개요**: 대용량 파일을 여러 노드에 저장하고, 데이터가 있는 곳에서 병렬 계산하는 프레임워크
- **왜 필요한가**: 단일 서버 메모리·디스크로 처리하기 어려운 TB~PB 데이터 배치 분석을 commodity cluster에서 처리해야 함.
- **핵심 직관**: 큰 책을 찢어 여러 사람에게 나눠 읽게 한 뒤, 각자 센 단어 수를 마지막에 합산하는 방식임.

## 깊이 이해
- **배경·문제의식**: 로그·검색 색인·클릭스트림은 데이터가 커서 중앙 서버로 모두 옮기면 네트워크가 병목이 됨. Hadoop은 HDFS에 데이터를 block 단위로 분산 저장하고, MapReduce 작업을 data locality 기준으로 배치함.
- **작동 원리**: HDFS는 파일을 128MB 이상 block으로 나누고 3 replica로 저장함. Map task가 block을 읽어 key-value를 만들고, shuffle/sort가 key별로 모은 뒤 reduce task가 집계함.
- **비유**: 전국 창고에 재고가 있을 때 본사로 모두 보내지 않고, 각 창고에서 먼저 집계한 뒤 본사에서 합산함.
- **구체 예시**: 10TB 로그를 128MB block으로 나누면 약 81920개 block이 생성되고, map task가 block 단위로 병렬 실행됨.
- **흔한 오해·주의점**: Hadoop은 실시간 처리 엔진이 아님. disk 기반 shuffle과 batch job 특성 때문에 초 단위 응답에는 Spark·Flink·Kafka Streams가 적합함.

## 연결 개념
- HDFS — 분산 파일 저장 기반
- YARN — cluster resource manager
- Spark — memory 기반 반복 처리 대안

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: Hadoop 문제에서 저장 구조, MapReduce 처리 흐름, 배치 처리 한계와 대안을 연결함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Hadoop MapReduce는 HDFS 분산 저장과 map-shuffle-reduce 계산 모델을 결합한 배치 처리 프레임워크임.
> 2. **가치**: data locality와 replica 기반으로 대용량 데이터를 저비용 cluster에서 처리함.
> 3. **판단 포인트**: 배치 처리에는 적합하나 반복 연산·저지연 스트림에는 Spark·Flink 계열을 검토해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 빅데이터 분산 처리 구조 확인 | HDFS block, NameNode, DataNode, MapReduce | Hadoop을 단순 저장소로만 설명 |
| 처리 흐름 이해 확인 | map, shuffle/sort, reduce 단계 | shuffle 병목과 data locality 누락 |
| 적용 한계 판단 확인 | batch, disk I/O, small file 문제 | 실시간 처리 용도라고 단정 |

> 요약: Hadoop 답안은 HDFS 저장과 MapReduce 계산을 분리해 쓰고, batch 처리 한계를 명확히 제시해야 함.

---

## Ⅰ. 개요 및 필요성

Hadoop MapReduce는 대용량 데이터를 분산 저장·배치 처리하는 프레임워크임. 로그·검색·정산 데이터는 TB~PB 규모로 증가해 단일 서버 처리에 한계가 있음. Hadoop은 HDFS block 분산과 data locality 기반 작업 배치로 대량 배치 분석을 수행함.

---

## Ⅱ. 구조 및 구성요소

```text
Client Job -> YARN ResourceManager -> ApplicationMaster
HDFS NameNode -> DataNode Block Replica
Map Task -> Shuffle/Sort -> Reduce Task -> HDFS Output
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| NameNode | 파일 namespace와 block metadata 관리 | HA 구성 필요 |
| DataNode | block 저장·replica 제공 | replication factor 기본 3 |
| YARN | CPU·메모리 자원 할당 | queue별 capacity 관리 |
| MapReduce | key-value 기반 배치 계산 | disk 기반 shuffle 사용 |

> 요약: Hadoop은 HDFS가 저장을, YARN이 자원을, MapReduce가 batch 계산을 담당하는 분산 처리 구조임.

---

## Ⅲ. 동작원리 및 흐름도

```text
파일 적재 -> HDFS block 분할/복제 -> job 제출
-> map task 배치 -> shuffle/sort -> reduce 집계 -> HDFS 저장
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 입력 파일을 block 단위로 저장 | block size 128MB 이상 |
| 2 | map task를 data locality 기준 배치 | local map 비율 |
| 3 | key별 shuffle/sort 수행 | shuffle bytes, spill count |
| 4 | reduce 집계 후 결과 저장 | failed task, output record 수 |

> 요약: MapReduce는 데이터를 이동시키기보다 작업을 데이터 위치로 보내고, shuffle 단계에서 key별 집계를 완성함.

---

## Ⅳ. 특징

| 구분 | 단일 서버 배치 | Hadoop MapReduce | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 저장 | 로컬 디스크 | HDFS block+replica | replica factor 3 |
| 처리 | 단일 프로세스 | map/reduce 병렬 처리 | task 수 = block 수 기반 |
| 장애 | 작업 실패 시 중단 | task 재시도, replica 읽기 | retry count, failed node |
| 한계 | 용량 한계 | shuffle·disk I/O 병목 | small file 1만개 이상이면 NameNode 부담 |

> 요약: Hadoop은 대량 배치 처리에 적합하나, 작은 파일과 반복 계산에서는 metadata·disk I/O 비용이 커짐.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | RDBMS batch | HDFS+MapReduce | 비정형 로그 TB 단위 처리 |
| 비용/성능 | scale-up 서버 | commodity cluster | 처리시간 목표가 분~시간 단위 |
| 운영/위험 | 단순 운영 | NameNode HA, YARN queue | 운영 인력과 job SLA 필요 |

> 요약: Hadoop은 대량 오프라인 분석에는 적합하지만, 초 단위 응답·반복 ML은 Spark·Flink를 우선 검토함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| NameNode 장애 | metadata 단일 지점 | Active/Standby HA, JournalNode | failover time 60초 이하 |
| small file 문제 | file당 metadata 증가 | SequenceFile, Parquet 병합 | 평균 파일 크기 128MB 이상 |
| shuffle 병목 | 네트워크·disk spill 증가 | combiner, partitioner 조정 | shuffle spill count, bytes |

> 요약: Hadoop 운영 리스크는 metadata, shuffle, 장애 전환이며 HA와 파일 크기 표준화로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 처리시간 | batch SLA 1시간 이하 | YARN job history |
| data locality | local map 80% 이상 | MapReduce counter |
| 저장 건전성 | under-replicated block 0건 | HDFS fsck |

> 요약: Hadoop 도입 효과는 batch SLA, data locality, HDFS replica 상태로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 원천 로그는 일별 partition과 Parquet/ORC로 저장하고 평균 파일 크기 128~512MB로 병합함
2. NameNode HA, rack awareness, replication factor 3으로 노드·랙 장애를 격리함
3. shuffle-heavy job은 combiner, custom partitioner, reducer 수 조정으로 skew key를 분산함

**결론 (2줄):**
- 기술사 판단: TB~PB 오프라인 배치와 장기 저장은 Hadoop, 반복 분석과 스트림은 Spark·Flink로 분리함
- 향후 방향: Hadoop 저장 계층은 object storage와 lakehouse 포맷으로 이동하고, 계산 계층은 Spark·Flink 중심으로 재편됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Hadoop을 설명하시오" | HDFS block, map-shuffle-reduce 흐름 | batch 처리 특징과 한계 |
| 요구사항 명시형 | "Spark와 비교하시오", "도입 방안을 제시하시오" | disk 기반 처리와 data locality | 처리 지연, 반복 연산, 운영 리스크 |

> 요약: 설명형은 Hadoop 구성, 비교형은 Spark 대비 disk batch 한계를 중심으로 작성함.
