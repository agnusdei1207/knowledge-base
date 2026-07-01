---
title: "Cassandra 컬럼 패밀리 DB (Cassandra Column Family)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 124
---

# 📖 【암기용】 개념 완전 이해

> 목적: Cassandra 컬럼 패밀리 DB를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 파티션 키와 컬럼 패밀리 모델로 대규모 쓰기와 다중 데이터센터 복제를 처리하는 NoSQL DB
- **왜 필요한가**: 로그, IoT, 메시지, 이벤트처럼 쓰기가 계속 들어오는 시스템은 단일 리더 DB에서 쓰기 병목이 생긴다. Cassandra는 노드 간 링 구조와 quorum 설정으로 대량 쓰기와 장애 허용을 처리한다.
- **핵심 직관**: 거대한 노트를 날짜와 센서 ID별로 여러 책장에 나누고, 어느 책장 일부가 빠져도 다른 책장에서 계속 기록하는 방식임

## 깊이 이해
- **배경·문제의식**: 전통 RDB는 강한 정합성과 조인에 강하지만, 초당 수십만 건 쓰기와 지리적 분산에서 단일 리더 병목이 생긴다. Cassandra는 peer-to-peer 구조와 LSM-Tree 저장으로 쓰기 경로를 단순화한다.
- **작동 원리**: 클라이언트 요청은 coordinator 노드가 받아 partition key 해시로 복제 대상 노드를 찾는다. 쓰기는 commit log와 memtable에 기록되고, SSTable로 flush된 뒤 compaction으로 정리된다.
- **비유**: 같은 접수 양식을 여러 창구에 나눠 받되, 접수번호 규칙으로 어느 창구에 보관했는지 바로 찾는 방식임
- **구체 예시**: 초당 200,000건 센서 이벤트를 `device_id + day` 파티션 키로 분산하고 RF=3, QUORUM 쓰기로 노드 1대 장애 시에도 쓰기 지속 가능함
- **흔한 오해·주의점**: Cassandra는 SQL 조인 DB가 아니다. 쿼리 먼저 정하고 테이블을 설계해야 하며, 높은 카디널리티 파티션과 wide partition 크기를 통제해야 한다.

## 연결 개념
- LSM-Tree - 쓰기 경로와 compaction의 기반
- CAP 정리 - AP/조정 가능 일관성 판단 배경
- 파티셔닝·샤딩 - partition key 기반 데이터 분산

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Cassandra 답안은 컬럼 패밀리보다 partition key, replication factor, consistency level, compaction을 중심으로 써야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Cassandra는 peer-to-peer 링, 컬럼 패밀리 모델, LSM-Tree 저장 구조를 결합한 분산 NoSQL DB임.
> 2. **가치**: 대량 쓰기, 다중 데이터센터 복제, 노드 장애 허용이 필요한 이벤트·로그성 데이터에 적합함.
> 3. **판단 포인트**: partition key 분포, RF, consistency level, compaction 전략이 처리량과 일관성을 결정함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 컬럼 패밀리 DB 구조 이해 확인 | partition key, clustering key, SSTable | RDB 컬럼 저장소와 혼동하지 않음 |
| 분산 일관성 판단 확인 | RF, QUORUM, tunable consistency | eventual consistency만 쓰고 CL 계산 누락 방지 |
| 운영 설계 역량 확인 | compaction, tombstone, wide partition | 조인·임의 검색 업무에 적용 단정 금지 |

> 요약: Cassandra 문제는 쿼리 기반 모델링과 조정 가능 일관성을 함께 설명해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: Cassandra는 컬럼 패밀리 기반 분산 DB이다.
- 배경: 대규모 이벤트·로그·IoT 데이터는 쓰기 처리량, 노드 장애 허용, 다중 리전 복제를 동시에 요구한다.
- 필요성: 링 기반 분산, LSM-Tree 저장, 조정 가능 일관성으로 대량 쓰기와 장애 허용 요구를 처리한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> Coordinator -> Partition Key Hash -> Replica Nodes
Write -> Commit Log -> Memtable -> SSTable -> Compaction
Read -> Bloom Filter -> Partition Index -> SSTable Merge
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Partition Key | 데이터 분산 기준 | hot partition 방지 |
| Column Family | 행 키와 컬럼 묶음 저장 | query-first 모델링 |
| Replication Factor | 복제본 수 결정 | RF=3 구성이 일반적 |
| Consistency Level | 읽기·쓰기 응답 기준 | ONE, QUORUM, ALL |

> 요약: Cassandra는 파티션 키로 데이터를 분산하고, RF와 CL 조합으로 가용성과 일관성을 조정함.

---

## Ⅲ. 동작원리 및 흐름도

```text
Write Request -> Coordinator -> Replica Write -> Commit Log/Memtable -> Ack by CL -> SSTable Flush
Read Request -> Replica Read -> SSTable Merge -> Read Repair -> Response
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | coordinator가 파티션 해시 계산 | token ownership |
| 2 | RF 기준 복제 노드에 쓰기 전송 | write latency p95 |
| 3 | commit log와 memtable 기록 | dropped mutation count |
| 4 | CL 충족 시 응답 반환 | W+R > RF 조건 |
| 5 | SSTable flush·compaction 수행 | pending compaction |

> 요약: Cassandra는 쓰기를 먼저 로그와 메모리에 기록하고, CL 충족 응답 후 SSTable 정리로 저장 구조를 관리함.

---

## Ⅳ. 특징

| 구분 | RDB/단일 리더 | Cassandra | 판단 포인트 |
|:---|:---|:---|:---|
| 쓰기 구조 | 리더 중심 | peer-to-peer 다중 노드 | 초당 쓰기 건수와 파티션 분포 |
| 일관성 | 강한 정합성 기본 | CL 기반 조정 | W+R > RF 필요 여부 |
| 쿼리 | 조인·집계 | 파티션 키 조회 | 쿼리 먼저 테이블 설계 |

> 요약: Cassandra는 쓰기와 분산 복제에 초점을 둔 DB이며, 조인·임의 조건 검색은 별도 검색/분석 계층이 필요함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | RDB master-replica | peer-to-peer ring | 단일 리더 쓰기 병목 발생 |
| 비용/성능 | 수직 증설 | 노드 추가 수평 분산 | 파티션별 쓰기 균등성 |
| 운영/위험 | SQL 튜닝 | compaction/tombstone 관리 | 삭제 비율, TTL 사용량 |

> 요약: Cassandra는 대량 쓰기와 노드 수평 확장이 핵심일 때 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Hot Partition | 낮은 키 분산 | composite key, bucketing | partition size p95 |
| Tombstone 폭증 | TTL·삭제 과다 | TTL 설계, compaction 전략 | tombstone scanned ratio |
| Read Amplification | SSTable 다중 조회 | Bloom filter, compaction | read latency p95 |

> 요약: Cassandra 운영 리스크는 파티션 크기, tombstone, compaction 지연을 기준으로 제어함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 쓰기 | write latency p95 20ms 이하 | nodetool tablehistograms |
| 균형 | 노드별 load 편차 20% 이내 | nodetool status |
| 정리 | pending compaction 지속 증가 0 | compactionstats |

> 요약: Cassandra 도입 후에는 쓰기 지연, 노드 균형, compaction backlog를 지속 점검함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 조회 패턴을 먼저 정의하고 `tenant_id + day` 같은 composite partition key로 hot partition을 방지함.
2. RF=3, LOCAL_QUORUM 읽기/쓰기처럼 리전 내 정합성 목표에 맞는 CL을 선택함.
3. TTL 데이터는 TimeWindowCompactionStrategy로 분리하고 tombstone 비율을 모니터링함.

**결론 (2줄):**
- 기술사 판단: 대량 쓰기·다중 DC가 우선이면 Cassandra, 조인·트랜잭션이 우선이면 RDB를 선택함.
- 향후 방향: Cassandra는 시계열·로그·IoT 저장소에서 스트림 처리와 검색 엔진을 결합한 구조로 활용됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Cassandra를 설명하시오" | 쓰기 경로, RF, CL, compaction | RDB와 컬럼 패밀리 비교 |
| 요구사항 명시형 | "대량 로그 저장 설계 방안을 제시하시오" | partition key와 compaction 전략 | hot partition, tombstone 대응 |

> 요약: 설명형은 구조와 원리, 설계형은 키 분산과 운영 리스크를 중심으로 전개함.
