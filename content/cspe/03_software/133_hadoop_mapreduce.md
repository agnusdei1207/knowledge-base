---
title: "빅데이터 분산 처리 — Hadoop·MapReduce·HDFS (Hadoop MapReduce)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 133
---

# 📖 【암기용】 개념 완전 이해

> 목적: Hadoop, MapReduce, HDFS가 왜 함께 등장했는지, 내부에서 어떤 용어가 어떻게 맞물리는지 이해하게 만든다.

## 한눈에
- **개요**: Hadoop MapReduce는 대용량 데이터를 **분산 저장**(HDFS)하고 **분산 병렬 처리**(MapReduce)하는 **빅데이터 배치 처리 프레임워크**다.
- **왜 필요한가**: 단일 서버는 디스크 용량·I/O 대역폭·메모리 모두에 한계가 있어, TB~PB급 로그·클릭스트림을 한 대의 서버로 저장·분석할 수 없다. Hadoop은 데이터를 여러 저가 서버(commodity server)에 쪼개 저장하고, 계산도 그 서버들에서 나눠 수행한다.
- **핵심 직관**: 큰 책 한 권을 여러 사람에게 페이지째 찢어 나눠주고, 각자 자기 페이지에서 단어를 센 뒤 마지막에 합산하는 방식이다 — "데이터를 계산 장소로 옮기지 않고, 계산을 데이터가 있는 곳으로 보낸다."

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 분산 처리 | 하나의 작업을 여러 서버에 나눠 동시에 수행하는 방식 — Hadoop이 속한 상위 범주 | 여러 일꾼이 나눠서 일하기 |
| 빅데이터 배치 처리 | 대량 데이터를 실시간이 아니라 정해진 주기로 모아서 한 번에 처리하는 방식 | 하루치 영수증을 마감 후 한꺼번에 정산 |
| HDFS | Hadoop Distributed File System — 파일을 block 단위로 여러 노드에 나눠 저장하는 분산 파일시스템 | 책을 챕터 단위로 찢어 여러 서고에 분산 보관 |
| Block | HDFS가 파일을 저장하는 고정 크기 단위(기본 128MB) | 책 한 챕터 |
| Replica | 장애에 대비해 만드는 block 복제본(기본 3개, 서로 다른 노드·랙에 배치) | 중요 서류를 3곳에 백업 |
| NameNode | "어느 block이 어느 DataNode에 있는지" metadata를 메모리에 관리하는 마스터 서버 | 도서관 목록 카드함 |
| DataNode | 실제 block 바이트를 디스크에 저장하는 워커 서버 | 책이 꽂힌 서고 |
| YARN | cluster의 CPU·메모리 자원을 job에 배분하는 자원관리자 | 공사현장 인력 배치소 |
| Map | 입력 레코드를 (key, value) 쌍으로 변환하는 단계 | 자료를 항목별로 1차 분류 |
| Shuffle/Sort | map이 출력한 (key, value)를 key별로 모아 정렬해 reduce로 전달하는 단계 | 분류된 카드를 항목별 상자로 모으기 |
| Reduce | 같은 key로 모인 값들을 집계하는 단계 | 상자별로 합계 내기 |
| Data Locality | 데이터를 네트워크로 옮기지 않고, 계산(코드)을 데이터가 저장된 노드로 보내는 원칙 | 재료가 있는 주방에서 바로 요리 |
| Combiner | map task 내부에서 미리 부분 합산해 shuffle로 보낼 데이터량을 줄이는 mini-reducer | 지점별 중간집계 후 본사에 요약만 전송 |

## 깊이 이해

### 왜 Hadoop이 필요했나 (배경)
2003~2004년 구글이 발표한 GFS(분산 파일시스템)와 MapReduce 논문에서 출발했다. 웹 검색 색인이 페타바이트 규모로 커지자, 한 대의 고성능 서버(scale-up)로는 저장 용량과 I/O 처리량이 모두 한계에 부딪혔다. 핵심 발상은 "데이터를 계산 서버로 옮기지 말고, 계산을 데이터가 있는 서버로 보낸다"였다 — 수십~수백 GB 데이터를 네트워크로 옮기는 것보다, 수 KB~MB 크기의 계산 코드를 옮기는 편이 훨씬 저렴하기 때문이다. Yahoo가 이 아이디어를 오픈소스로 재구현한 것이 Hadoop이다.

### HDFS가 파일을 쪼개 저장하는 방법 (수치로 이해)
HDFS는 파일을 고정 크기 block(기본 128MB)으로 잘라 여러 DataNode에 분산 저장한다. 예를 들어 10TB(약 10,485,760MB) 로그 파일이라면 128MB로 나눌 때 약 81,920개 block이 생긴다. 각 block은 장애 대비로 3개 복제본을 서로 다른 노드·랙에 저장하므로(replication factor=3), 실제 디스크 사용량은 원본의 3배인 약 30TB가 된다. NameNode가 이 8만여 개 block의 위치 정보를 모두 메모리에 들고 있어야 하므로, 파일 개수가 지나치게 많아지면(예: 128MB 미만 small file이 수백만 개) NameNode 메모리 부담이 커진다 — 이것이 "small file 문제"다.

### MapReduce 처리 흐름 — word count로 단계 확인
"how are you, are you fine"이라는 문장의 단어 수를 센다고 하자.
1. **Map**: 줄 단위로 읽어 단어마다 (단어, 1) 쌍을 만든다 → (how,1) (are,1) (you,1) (are,1) (you,1) (fine,1).
2. **Shuffle/Sort**: 같은 key(단어)를 모아 정렬한다 → are:[1,1], fine:[1], how:[1], you:[1,1]. 이 단계는 여러 노드에 흩어진 map 출력을 네트워크로 모아야 해서 가장 비용이 크며, "MapReduce의 심장"이라 불린다.
3. **Reduce**: key별로 값을 합산한다 → are:2, fine:1, how:1, you:2.
실제로는 이 과정이 81,920개 block에서 동시에 일어나며, 각 map task는 자신이 처리할 block이 저장된 DataNode(또는 같은 랙)에서 우선 실행된다(data locality) — 원격 노드에서 읽으면 네트워크가 병목이 되기 때문이다.

### Combiner로 shuffle 비용 줄이기
한 block 안에 "are"가 10,000번 나온다면, combiner 없이는 (are,1)을 10,000번 네트워크로 전송하지만, combiner를 쓰면 map task 내부에서 미리 합산한 (are,10000) 하나만 전송한다. 이는 shuffle 트래픽을 극적으로 줄이는 표준 최적화다.

### 흔한 오해
Hadoop MapReduce는 각 단계 사이 중간 결과를 디스크에 쓰기 때문에(disk 기반 shuffle), 같은 데이터를 여러 번 반복 스캔하는 머신러닝 반복 연산이나 초 단위 응답이 필요한 실시간 처리에는 적합하지 않다. 이 한계를 메모리 기반 처리로 극복한 것이 Spark다(134 참고).

## 연결 개념
- HDFS·YARN — Hadoop을 이루는 저장·자원관리 하위 축
- Apache Spark — disk shuffle을 메모리 캐시로 대체한 후속 엔진(134)
- Lambda/Kappa Architecture — Hadoop이 batch layer로 편입되는 상위 아키텍처(135, 136)

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

- 개요: Hadoop MapReduce는 분산 저장·배치 처리 프레임워크임.
- 배경: 로그·검색·정산 데이터는 TB~PB 규모로 증가해 단일 서버 처리에 한계가 있음.
- 필요성: HDFS block 분산과 data locality 기반 작업 배치로 대량 배치 분석을 수행함.

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
