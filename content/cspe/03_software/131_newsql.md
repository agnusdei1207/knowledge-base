---
title: "NewSQL — CockroachDB·Spanner (NewSQL)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 131
---

# 📖 【암기용】 개념 완전 이해

> 목적: NewSQL을 처음 봐도 관계형 DB와 NoSQL 사이의 위치를 이해하게 만든다.

## 한눈에
- **개요**: 전통 RDBMS의 **SQL**과 **ACID 트랜잭션**을 유지하면서, NoSQL처럼 자동 샤딩으로 **수평 확장**이 가능한 분산 OLTP 데이터베이스 계열이 **NewSQL**이다.
- **왜 필요한가**: 전통 RDBMS는 단일 노드 확장(scale-up)에 한계가 있고, NoSQL은 조인·강한 트랜잭션·SQL 호환성이 약해 계좌이체·주문결제처럼 정합성이 필수인 대규모 업무에는 제약이 있다. NewSQL은 이 둘의 장점만 결합해 그 간극을 메운다.
- **핵심 직관**: 여러 지점에 금고를 나눠 두되(분산), 각 금고를 여러 벌 복제해 두고 과반수가 동의해야 장부에 기록해서(합의), 본사 장부는 언제나 하나처럼 맞는 구조다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| NewSQL | SQL·ACID와 수평 분산을 결합한 분산 OLTP DB 계열 | 상위 개념 — RDBMS와 NoSQL의 절충 |
| ACID | 원자성·일관성·고립성·지속성 — 트랜잭션이 지켜야 할 4대 성질 | 계좌이체가 절반만 되는 일이 없도록 하는 규칙 |
| Raft / Paxos | 여러 복제본이 같은 순서로 로그를 기록하도록 맞추는 분산 합의 알고리즘 | 여러 지점 중 과반수가 동의해야 장부에 기록 |
| 쿼럼 커밋(Quorum Commit) | 전체 복제본 중 과반수가 응답해야 트랜잭션을 확정 짓는 방식 | 이사회 의결정족수 통과 시에만 결의 확정 |
| MVCC | 데이터의 여러 버전을 동시에 유지해 읽기와 쓰기가 서로 막지 않게 하는 기법 | 문서 개정판을 버전별로 보관해 열람 중에도 새 개정판 작성 가능 |
| Range Shard | 키의 정렬 범위 단위로 데이터를 나누는 분할 방식 | 사전을 ㄱ~ㅁ, ㅂ~ㅈ처럼 구간별로 나눠 여러 권으로 제본 |
| TrueTime | Spanner가 GPS·원자시계로 전역 서버 시간 오차를 좁혀 트랜잭션 순서를 보장하는 API | 전 세계 지점 시계를 오차 ±수 ms로 동기화 |
| Hot Range | 특정 키 범위에 요청이 몰려 그 range를 담당하는 노드만 과부하되는 현상 | 사전에서 유독 한 글자로 시작하는 단어만 계속 찾음 |

## 깊이 이해

### 왜 NewSQL이 등장했나 (배경)
- 2000년대 후반 NoSQL(Cassandra, MongoDB 등)은 수평 확장은 쉬웠지만 조인·트랜잭션·SQL을 포기했다. "A 계좌에서 빼고 B 계좌에 더한다"처럼 여러 row가 원자적으로 함께 성공하거나 함께 실패해야 하는 연산은 NoSQL로 안전하게 짜기 어려웠다. 2012년 Google이 Spanner 논문을 발표하며 "분산돼 있으면서도 SQL과 ACID를 유지"하는 것이 가능함을 보였고, 이후 CockroachDB(2015)·TiDB 같은 오픈소스가 같은 모델을 구현했다 — 이 계열을 NewSQL이라 부른다.

### 분산 트랜잭션이 정합성을 지키는 방법 — Raft 쿼럼 수치
- 데이터는 key range 단위로 나뉘고, 각 range는 복제본 3개를 하나의 Raft 그룹으로 묶는다. 쓰기 요청은 3개 중 2개(과반수, 쿼럼)가 "로그에 기록했다"고 응답해야 커밋이 확정된다. 복제본 1개가 장애 나도 나머지 2개로 쿼럼을 채워 서비스가 계속되지만, 2개 이상 장애가 나면 그 range는 쓰기 불가 상태가 된다.

### Spanner의 TrueTime — 구체 수치
- 여러 대륙에 흩어진 서버는 시계가 완벽히 일치하지 않는다(clock drift). Spanner는 GPS와 원자시계로 시간 오차를 약 ±7ms 이내로 관리하는 TrueTime API를 쓰고, 커밋 시 그 오차만큼 짧게 대기(commit wait)해 "이 트랜잭션의 타임스탬프가 실제로 이미 지났다"는 것을 보장한다. 이 방식으로 대륙 간에도 트랜잭션 순서가 실제 시간 순서와 일치하는 external consistency를 확보한다.

### cross-region 지연이 큰 이유 — 수치 예
- 서울과 미국 동부 리전 간 왕복 지연(RTT)은 대략 150~180ms다. 두 리전에 걸친 range에 쓰기를 하면 쿼럼 커밋을 위해 원거리 복제본의 응답까지 기다려야 하므로, 같은 리전 안에서 끝나는 트랜잭션(수 ms)보다 커밋 지연이 수십~백여 배 늘어난다. 그래서 실무에서는 자주 접근하는 range의 리더를 사용자와 가까운 리전에 고정(leaseholder locality)해 지연을 줄인다.

### hot range 문제 — 구체 예제
- 주문번호를 auto-increment(순차 증가)로 채번하면, 새 주문은 항상 가장 큰 키값이 속한 range 하나에만 몰려 쓰인다. 초당 5,000건이 들어와도 그 range를 담당하는 노드 1대만 부하를 받고 나머지 노드는 거의 놀게 된다(hot range). 키 앞에 해시 prefix를 붙이거나 tenant_id를 앞자리에 두면 여러 range에 고르게 분산된다.

### 흔한 오해
- NewSQL이 모든 쿼리를 자동으로 빠르게 만들지는 않는다. 여러 리전에 걸친 트랜잭션은 물리적 거리(빛의 속도로 정해지는 네트워크 RTT)가 지연의 하한선이라 소프트웨어만으로는 없앨 수 없다.

## 연결 개념
- 분산 데이터베이스(130) — NewSQL이 구현하는 상위 개념(샤딩+복제)
- Raft·Paxos — NewSQL이 정합성을 확보하는 분산 합의 알고리즘
- MVCC — 단일 노드 RDBMS와도 공유하는 트랜잭션 고립 기법

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: NewSQL 문제에서 SQL 호환성, 분산 합의, ACID 보장, 운영 리스크를 연결해 답안화함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NewSQL은 RDBMS의 SQL·ACID와 NoSQL의 수평 분산을 결합한 분산 OLTP 데이터베이스임.
> 2. **가치**: 자동 샤딩·quorum replication으로 노드 장애 시에도 트랜잭션 정합성과 서비스 연속성을 동시에 확보함.
> 3. **판단 포인트**: 글로벌 트랜잭션 지연, 합의 비용, 스키마 설계, 운영 복잡도를 업무 중요도와 함께 판단해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| RDBMS·NoSQL 한계 비교 역량 확인 | SQL, ACID, 자동 샤딩, 분산 합의 | NewSQL을 NoSQL의 한 종류로만 서술 |
| 분산 트랜잭션 판단 확인 | quorum commit, MVCC, timestamp ordering | CAP·PACELC 관점 누락 |
| 실무 도입 리스크 확인 | cross-region RTT, hot range, schema migration | 모든 업무에 동일하게 적용한다고 단정 |

> 요약: NewSQL 답안은 SQL 호환성보다 분산 합의 비용과 OLTP 정합성 보장을 함께 써야 채점 포인트가 맞음.

---

## Ⅰ. 개요 및 필요성

- 개요: NewSQL은 분산 ACID OLTP DBMS임.
- 배경: 전통 RDBMS는 scale-up 중심이고 NoSQL은 강한 트랜잭션 제약이 있어 주문·결제·계정처럼 정합성이 필요한 대규모 서비스에 한계가 있음.
- 필요성: SQL 인터페이스, 자동 샤딩, Raft/Paxos 계열 복제 합의로 분산 환경의 일관된 트랜잭션을 제공함.

---

## Ⅱ. 구조 및 구성요소

```text
Client SQL -> SQL Gateway -> Transaction Coordinator -> Range Shard
                                      / Raft Group -> Replica 1/2/3
                                      / MVCC Store -> Commit Log
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| SQL Gateway | SQL 파싱·최적화·라우팅 | PostgreSQL 호환 계층 제공 가능 |
| Transaction Coordinator | 분산 트랜잭션 조정 | 2PC 또는 timestamp 기반 commit |
| Range Shard | 키 범위 단위 데이터 분할 | hot range 발생 시 split 필요 |
| Raft/Paxos Group | replica 합의 | 3 replica 중 quorum 2개 commit |
| MVCC Store | 버전 기반 읽기 제공 | snapshot read와 serializable 처리 |

> 요약: NewSQL은 SQL 계층 위에 샤딩·복제·합의를 결합해 단일 DB처럼 보이는 분산 OLTP 구조를 만든다.

---

## Ⅲ. 동작원리 및 흐름도

```text
SQL 요청 -> 파싱/최적화 -> shard 위치 확인 -> replica quorum write
-> MVCC version 생성 -> commit timestamp 확정 -> client 응답
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | SQL 수신 및 실행계획 생성 | index 사용률, full scan 여부 |
| 2 | key range 기반 shard 라우팅 | split/merge 상태, leader 위치 |
| 3 | quorum replication 수행 | commit quorum 2/3, log append 지연 |
| 4 | MVCC 버전 확정 및 응답 | serializable conflict, retry rate |

> 요약: NewSQL 쓰기는 shard leader와 replica quorum을 거쳐 commit되며, MVCC가 동시 읽기와 직렬화 검증을 담당함.

---

## Ⅳ. 특징

| 구분 | 기존 RDBMS | NewSQL | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 확장 방식 | scale-up, read replica | 자동 shard split, replica rebalance | 노드 3대 이상, quorum 2/3 |
| 트랜잭션 | 단일 노드 ACID 중심 | 분산 ACID, serializable isolation | cross-shard transaction retry율 |
| 지연 | LAN 중심 | region 배치에 따라 WAN RTT 반영 | region 간 50~150ms commit 지연 |
| 운영 | 수동 파티션 관리 | range·replica 자동 관리 | hot range, leaseholder locality |

> 요약: NewSQL은 ACID를 유지한 수평 분산이 장점이나, cross-region write와 hot key 설계가 핵심 제약임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | RDBMS sharding 수동 구성 | shard·replica 자동 관리 | 테넌트·주문 키 기준 분산 가능 시 |
| 비용/성능 | 단일 노드 증설 비용 증가 | 노드 추가와 quorum 비용 공존 | write p95 100ms 이하 목표 검증 |
| 운영/위험 | DBA 중심 failover | consensus 기반 failover | leader 이동, split policy 운영 역량 |

> 요약: NewSQL은 분산 정합성이 필요한 OLTP에 적합하며, 단일 리전 write-heavy 업무는 기존 RDBMS가 비용 측면에서 유리할 수 있음.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| hot range | 단조 증가 key 집중 | hash prefix, keyspace 분산 | top range QPS 편차 3배 이하 |
| commit 지연 | quorum write와 WAN RTT | region locality, follower read | p95 write latency 100ms 이하 |
| transaction retry | serializable conflict | 짧은 transaction, retry backoff | retry rate 1% 이하 |

> 요약: NewSQL 리스크는 데이터 키 설계와 region 배치에서 발생하며, p95 지연과 retry율로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 트랜잭션 지연 | p95 write 100ms 이하 | DB metrics, APM trace |
| 복제 상태 | under-replicated range 0건 | cluster health check |
| 정합성 | serializable anomaly 0건 | Jepsen류 테스트, transaction log |

> 요약: 도입 후 성공 여부는 지연, replica health, 정합성 이상 여부를 동시에 측정해야 함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 주문·계정 테이블은 tenant_id 또는 user_id 기준 key 설계로 shard 편차 3배 이하 유지
2. 단일 리전 primary write, 타 리전 follower read 구성으로 read p95 50ms 이하 목표 설정
3. schema migration은 online DDL, backfill rate limit, retry budget 1% 기준으로 단계 실행

**결론 (2줄):**
- 기술사 판단: 글로벌 OLTP와 강한 정합성이 동시에 필요하면 NewSQL, 단일 리전 단순 OLTP면 RDBMS+replica를 우선 검토함
- 향후 방향: Spanner·CockroachDB 계열은 cloud-native DB와 결합해 multi-region transaction 운영 모델로 확산됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "NewSQL을 설명하시오" | SQL gateway, shard, quorum commit 흐름 | RDBMS·NoSQL 대비 특징 |
| 요구사항 명시형 | "비교하시오", "도입 방안을 제시하시오" | CAP/PACELC, cross-region transaction | 업무별 선택 기준, hot range 대응 |

> 요약: 설명형은 구조·원리, 요구사항형은 RDBMS·NoSQL 비교와 운영 지표 중심으로 목차를 조정함.
