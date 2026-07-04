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
- **개요**: Cassandra는 리더 노드 없이 모든 노드가 대등하게 연결된 **분산 NoSQL 데이터베이스**로, 데이터 모델은 행마다 다른 컬럼 집합을 가질 수 있는 **와이드 컬럼(컬럼 패밀리)** 방식이다.
- **왜 필요한가**: 로그·IoT·이벤트처럼 초당 수십만 건씩 쓰기가 들어오는 시스템은, 쓰기를 한 노드(리더)가 모두 받는 구조에서는 그 노드가 병목이 된다. Cassandra는 링(ring) 구조로 쓰기를 여러 노드에 분산하고, 한두 노드가 죽어도 나머지 복제본으로 쓰기를 계속한다.
- **핵심 직관**: 접수 양식을 창구 하나가 아니라 여러 창구가 나눠 받되, 접수번호 규칙(파티션 키)만 알면 어느 창구에 보관했는지 바로 찾아가는 구조다.

## 핵심 용어 정리
| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 와이드 컬럼(컬럼 패밀리) | 행마다 다른 컬럼 집합을 가질 수 있는 넓은 표 형태 저장 방식 — Cassandra의 상위 데이터 모델 분류 | 사람마다 다른 항목을 채우는 신청서 |
| 파티션 키(Partition Key) | 데이터를 어느 노드에 저장할지 정하는 해시 기준 키 | 우편번호로 배달 구역 결정 |
| 클러스터링 키(Clustering Key) | 같은 파티션 안에서 행의 정렬 순서를 정하는 키 | 서랍 안 물건을 날짜순 정렬 |
| 링(Ring)·토큰(Token)·Consistent Hashing | 노드들을 원형으로 배치하고 각 노드가 토큰 구간을 나눠 담당하는 분산 구조 | 원탁에 앉은 담당자들이 구간을 나눠 맡음 |
| Coordinator | 클라이언트 요청을 받아 해당 파티션의 담당 노드로 중개하는 노드(요청마다 어느 노드든 될 수 있음) | 접수 담당 창구 |
| Replication Factor(RF) | 같은 데이터를 몇 개 노드에 복제해 둘지(보통 3) | 같은 서류를 3곳에 복사 보관 |
| Consistency Level(ONE/QUORUM/ALL) | 쓰기·읽기가 "성공"으로 인정되기 위해 응답해야 하는 노드 수 기준 | 3명 중 몇 명 서명이 있어야 유효 서류인지 |
| Commit Log | 디스크에 순차로 append하는 쓰기 로그(장애 복구용) | 은행 거래 원장 |
| Memtable | 메모리 상의 최신 쓰기를 담아두는 정렬된 버퍼 | 임시 메모장 |
| SSTable(Sorted String Table) | Memtable이 가득 차면 디스크로 flush되는 불변(immutable) 정렬 파일 | 완성돼 봉인된 서류철 |
| Compaction | 여러 SSTable을 병합해 중복·삭제 데이터를 정리하는 백그라운드 작업 | 서류철 여러 개를 하나로 재정리 |
| LSM-Tree | Commit Log→Memtable→SSTable→Compaction으로 이어지는 쓰기 중심 저장 구조(Cassandra 저장 엔진의 기반) | 일단 다 받아 적고, 나중에 정리 |
| Bloom Filter | "이 키가 이 SSTable에 없다"를 빠르게 걸러주는 확률적 자료구조(없다는 답은 확실, 있다는 답은 재확인 필요) | 체로 걸러 없는 걸 먼저 제외 |
| Tombstone | 삭제된 데이터임을 표시하는 마커(실제 삭제는 compaction 때 일어남) | "폐기 예정" 스티커 |
| Gossip Protocol | 노드들이 주기적으로 무작위 상대와 상태 정보를 주고받아 클러스터 전체 상태를 퍼뜨리는 방식 | 소문이 퍼지듯 서로 근황을 전달 |
| Read Repair | 읽기 시 복제본 간 값 불일치를 발견하면 최신 값으로 맞춰주는 과정 | 사본끼리 대조해 오래된 걸 갱신 |
| Hinted Handoff | 쓰기 대상 노드가 다운됐을 때 다른 노드가 대신 받아뒀다가 복구되면 전달하는 메커니즘 | 부재중 우편물을 이웃이 맡아뒀다 전달 |

## 깊이 이해

### 배경 — 단일 리더 병목을 수치로 이해
- 단일 리더 RDB에서 모든 쓰기가 리더 한 대로 몰리면, 리더의 디스크 쓰기 처리량(예: 초당 5만 건)이 시스템 전체의 상한이 된다. 리더를 늘릴 수 없으니(쓰기는 한 곳으로 모여야 정합성이 유지되므로) 병목은 그대로 남는다.
- Cassandra는 리더가 없는 peer-to-peer 구조라, 쓰기가 파티션 키에 따라 여러 노드로 애초에 분산된다. 노드를 추가하면 담당 파티션 범위가 줄어 처리량이 수평으로 늘어난다.

### 쓰기 경로 — LSM-Tree를 순서대로 따라가기
- ① 쓰기 요청이 오면 먼저 Commit Log에 append한다(디스크 순차 쓰기라 매우 빠르고, 장애 시 이 로그로 복구한다). ② 동시에 메모리의 Memtable에도 기록한다(이 시점에 클라이언트는 이미 ack를 받을 수 있다). ③ Memtable이 예: 256MB에 도달하면 통째로 디스크에 SSTable로 flush된다. ④ SSTable이 쌓이면 백그라운드 Compaction이 여러 개를 병합해 중복 키·tombstone을 정리한다.
- 이 경로의 핵심은 "쓰기는 항상 append만 한다"는 점이다 — 기존 파일을 찾아 덮어쓰지 않으므로 랜덤 쓰기가 없고, 그만큼 쓰기 처리량이 높다.

### 파티션 키와 토큰 링 — 구체 예
- `device_id + day`를 파티션 키로 쓰면, 이 값이 해시 함수(Murmur3)를 거쳐 토큰(정수값)이 되고, 그 토큰이 속한 구간을 담당하는 노드에 저장된다. 노드가 4대면 토큰 공간을 4구간으로 나눠 각 노드가 담당하며, 노드를 추가하면 인접 구간 일부만 새 노드로 넘겨주면 된다(전체 재배치가 필요 없다).
- 예: 센서 200,000건/초 이벤트를 `device_id + day`로 분산하면 특정 하루·특정 장비의 데이터는 항상 같은 파티션(같은 노드 그룹)에 모이므로, 그 장비의 하루 데이터를 조회하는 질의는 한 파티션만 읽으면 된다.

### Consistency Level 수식 — W + R > RF
- RF=3(복제본 3개)에서 쓰기 CL=QUORUM(2/3 응답 필요), 읽기 CL=QUORUM(2/3 응답 필요)이면 W+R=4 > RF=3이 성립해, 쓰기와 읽기가 최소 1개 노드에서는 반드시 겹친다 — 즉 읽을 때 가장 최근에 쓰인 값을 놓치지 않는다(강한 일관성).
- 반대로 쓰기 CL=ONE, 읽기 CL=ONE이면 W+R=2 ≤ RF=3이라 쓰기와 읽기가 겹치지 않는 조합이 생길 수 있다 — 이 경우 방금 쓴 값을 못 읽을 수 있다(최종 일관성, eventual consistency). CL 조합은 "얼마나 빨리 응답할지"와 "얼마나 최신 값을 보장할지"의 트레이드오프다.

### Compaction과 Tombstone — 수치로 보는 위험
- TTL이나 DELETE로 데이터를 지우면 즉시 사라지지 않고 tombstone 마커만 남는다. 기본 `gc_grace_seconds`(10일, 864,000초)가 지나야 compaction 때 실제로 삭제된다.
- 한 파티션에 tombstone이 예: 100,000개 이상 쌓이면, 그 파티션을 읽을 때마다 이 tombstone들을 다 훑어야 해서 읽기 지연이 급격히 커진다(Cassandra는 기본적으로 10만 건을 경고 임계값으로 잡는다). TTL 데이터를 자주 쓰는 워크로드는 `TimeWindowCompactionStrategy`로 시간 구간별 SSTable을 분리해 이 문제를 줄인다.

### 비유 정리
- 접수 양식을 여러 창구(노드)가 나눠 받되, 접수번호(파티션 키) 규칙만 알면 담당 창구를 바로 찾을 수 있다. 창구 하나가 잠깐 자리를 비워도(노드 장애) 다른 복제 창구가 접수를 계속 받는다(hinted handoff·read repair로 나중에 맞춘다).

## 연결 개념
- LSM-Tree — Cassandra 저장 엔진의 상위 개념(쓰기 경로와 compaction의 기반).
- CAP 정리 — Cassandra는 기본적으로 AP(가용성·분할 내성) 쪽에 서고, Consistency Level 조합으로 일관성 정도를 조정한다.
- 파티셔닝·샤딩 — 파티션 키 기반 데이터 분산은 샤딩의 한 구현이다.
- Redis(123) — 둘 다 분산 NoSQL이지만, Redis는 인메모리 key-value로 저지연 단건 접근에, Cassandra는 디스크 기반 와이드 컬럼으로 대량 쓰기·영속 저장에 초점을 둔다.

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
