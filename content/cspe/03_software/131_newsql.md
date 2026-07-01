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
- **개요**: SQL과 ACID를 유지하면서 분산 확장을 지원하는 데이터베이스 계열
- **왜 필요한가**: 전통 RDBMS는 단일 노드 확장 한계가 있고, NoSQL은 조인·트랜잭션·SQL 호환성이 약해 금융·주문 업무에 제약이 있음.
- **핵심 직관**: 여러 지점에 금고를 나눠 두되, 장부는 하나처럼 맞추는 구조임.

## 깊이 이해
- **배경·문제의식**: OLTP 시스템은 계좌 이체처럼 ACID가 필요하지만, 글로벌 서비스는 지역별 지연과 장애 격리를 요구함. NewSQL은 SQL 질의 모델, 분산 합의, 자동 샤딩을 결합해 이 간극을 줄임.
- **작동 원리**: 데이터를 range 단위로 나누고 replica를 여러 노드에 배치함. 쓰기는 Raft·Paxos 계열 합의로 quorum commit을 수행하며, MVCC와 timestamp ordering으로 읽기 일관성을 제공함.
- **비유**: 여러 매장 POS가 각자 주문을 받지만, 본사 장부는 주문 번호와 재고 수량이 동시에 맞는 구조임.
- **구체 예시**: Spanner는 TrueTime 기반 external consistency를 제공하고, CockroachDB는 range replica 3개 중 quorum 2개 응답으로 commit함.
- **흔한 오해·주의점**: NewSQL은 모든 질의를 자동으로 낮은 지연으로 처리하지 않음. cross-region transaction은 WAN RTT 50~150ms가 commit 지연에 반영됨.

## 연결 개념
- ACID·MVCC — 트랜잭션 일관성 기반
- Raft·Paxos — 분산 합의 기반
- 샤딩·복제 — 데이터 분산 배치 기반

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

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
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
