---
title: "Distributed System Consistency CAP PACELC"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CAP 정리는 네트워크 분할(Partition) 발생 시 일관성(Consistency)과 가용성(Availability) 중 하나를 포기해야 한다는 Brewer의 명제(2000, 증명 2002 Gilbert-Lynch)이며, PACELC는 이를 확장하여 정상 운영 시(Else)에도 지연시간(Latency)과 일관성 사이의 트레이드오프를 명시한 분산 데이터베이스 설계 프레임워크이다.
> 2. **가치**: 정량적으로는 시스템 p99 지연시간을 10ms 이하로 유지하면서도 멀티리전 RPO(Recovery Point Objective)를 0에 근접시키거나(PC/EC), 수십 ms 수준의 쓰기 지연으로 99.999% 가용성을 달성(PA/EL)하는 등 명확한 SLO(Service Level Objective) 목표 하에서 시스템 아키텍처를 결정할 수 있게 한다.
> 3. **판단 포인트**: 금융 원장(Strong Consistency, PC/EC) vs 장바구니·IoT 센서 데이터(AP/EL), 동기식 Quorum(2PC, Raft) vs 비동기 안티엔트로피(Read Repair, Hinted Handoff), 그리고 CRDT(Conflict-free Replicated Data Type)와 벡터 클럭을 통한 eventual consistency의 수렴 보장 등 도메인별 핵심 트레이드오프를 식별해야 한다.

---

## Ⅰ. 개요 및 필요성

CAP 정리는 2000년 UC Berkeley의 Eric Brewer가 PODC(Principles of Distributed Computing) 컨퍼런스 키노트에서 처음 제시한 추측(conjecture)이다. 2002년 MIT의 Seth Gilbert와 Nancy Lynch가 비동기 네트워크 모델에서 이를 정형적으로 증명(CAP Theorem)함으로써, 분산 시스템 설계의 제1원칙으로 자리 잡았다. 이후 2010년 Daniel Abadi는 PACELC 논문("Consistency Tradeoffs in Modern Distributed Database System Design", IEEE Computer Society)을 통해 정상 상태(Else)에서의 Latency-Consistency trade-off를 추가하여, 클라우드 네이티브 환경에서 실제 설계 결정을 더 정확히 표현하는 프레임워크로 발전시켰다.

전통적인 단일 데이터센터 RDBMS(Oracle RAC, MySQL Master-Slave)는 동기식 복제(Synchronous Replication)와 2PC(Two-Phase Commit)를 통해 ACID를 보장했으나, 지리적으로 분산된 멀티리전 환경에서는 WAN 지연시간(RTT 50~200ms)이 누적되어 처리량(Throughput)이 급격히 저하된다. AWS us-east-1 ↔ eu-west-1 간 RTT는 평균 80ms로, 3홉 커밋(3-Phase Commit) 시 240ms가 소요되어 사용자 응답성 SLA를 위반한다. 또한 DNS, BGP, 광케이블 단선, NATS/PubSub 메시지 브로커 장애 등으로 인한 네트워크 분할(Network Partition)은 필연적으로 발생하며, 이를 무시할 수 없는 현실적 제약 조건이 되었다.

```text
[ 분산 시스템의 CAP 트레이드오프 시각화 ]

                 네트워크 정상 (No Partition)
        +------------------------------------------+
        |  CAP: 모든 속성 선택 가능(학술적)         |
        |  PACELC: Latency ↔ Consistency 트레이드오프|
        +------------------------------------------+
                              |
                              | 네트워크 장애 (Partition 발생)
                              v
        +------------------------------------------+
        |            분산 시스템 삼각형              |
        |                                          |
        |              Consistency                 |
        |              (일관성)                     |
        |             ╱            ╲               |
        |            ╱   양자택일    ╲              |
        |           ╱   (Pick 2 of 3) ╲            |
        |          ╱   실제는 Pick 1  ╲             |
        |   Availability ---- Partition             |
        |   (가용성)        tolerance                |
        |                 (분할내성)                 |
        +------------------------------------------+

[ PACELC 분기 결정 플로우 ]

                  P? (파티션 발생?)
                 ╱                ╲
               Yes                 No
               ╱                    ╲
        +----------+           +----------+
        | C or A?  |           | L or C?  |
        | (C=CP)   |           | (L=EL)   |
        | (A=AP)   |           | (C=EC)   |
        +----------+           +----------+
```

기존 패러다임(단일 노드 RDBMS, CAV: Consistency + Availability + no-Partition 가정)과 신규 패러다임(분산 NoSQL/NewSQL, CAP 중 2개 선택 + PACELC 명시)의 핵심 차이는 **"완벽한 동시성 제어가 가능한 단일 신뢰 경계(Single Trust Boundary)"**의 가정을 버렸다는 점이다. 분산 환경에서는 FLP 불가능성(1985 Fischer-Lynch-Paterson) 결과가 보장하듯, 비동기 모델에서 합의(Consensus) 자체가 네트워크 실패 시 보장 불가능하므로, 엔지니어는 어떤 속성을 완화할지(relax) 명시적으로 결정해야 한다.

- **📢 섹션 요약 비유**: CAP는 재난 상황(지진) 발생 시 **"구조물을 무너뜨리지 않을 것(일관성)"**과 **"모든 거주자를 즉시 대피시킬 것(가용성)"** 사이에서 건축가가 단 하나의 선택만 해야 하는 상황과 같다. PACELC는 평상시에도 "내진 설계 강화(지연시간 증가)" ↔ "빠른 출입(일관성 완화)" 사이의 일상적 균형점을 따로 설계해야 함을 알려준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CAP의 세 속성은 다음과 같이 정형화된다(2.2 Gilbert-Lynch 비동기 공유 메모리 모델 기준).

1. **Consistency (선형화 가능성, Linearizability)**: 모든 클라이언트가 동일한 키에 대해 가장 최근의 쓰기 결과를 읽을 수 있어야 한다. Herlihy-Wing(1990)이 정의한 원자적(atomic) 읽기-쓰기 순서를 만족한다.
2. **Availability**: 분할되지 않은 모든 노드가 클라이언트 요청에 대해 비-에러 응답(즉, timeout이 아닌 합법적 데이터)을 반환해야 한다. 시스템의 모든 동작 노드가 응답 가능해야 한다.
3. **Partition Tolerance**: 노드 간 네트워크 메시지 손실/지연/단절에도 시스템이 계속 동작해야 한다. 현실적 분산 시스템에서 P는 반드시 요구되므로, **실질적 선택은 C vs A**가 된다.

```text
[ CAP + PACELC 4-Quadrant 아키텍처 매트릭스 ]

                    Partition 시 (P)
                    +-----------------------------------------+
                    |                                         |
              CP    |   PC       |          PA                |
       (일관성 우선) | Spanner    |      DynamoDB               |
                    | HBase      |      Cassandra              |
                    | ZooKeeper  |      Riak                    |
                    | etcd/Raft  |      Cosmos DB (multi-master)|
                    | CockroachDB|                              |
                    +------------+-----------------------------+
                    |            |                              |
              AP    |            |                              |
       (가용성 우선) |            |                              |
                    +-----------------------------------------+
                    Else (정상) 시 (E)
                    +-----------------------------------------+
                    |                                         |
              EC    | Spanner   |     CockroachDB              |
       (일관성 우선) | (TrueTime)|     (Hybrid Logical Clock)    |
                    |           |                              |
                    +-----------+------------------------------+
                    |           |                              |
              EL    | BigTable  |     DynamoDB                 |
       (지연 우선)  | HBase     |     Cassandra (Tunable)       |
                    |           |     Redis Cluster            |
                    +-----------+------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Quorum 기반 복제** | 읽기/쓰기 일관성·가용성 균형 조정 | N(전체 복제본) = 3, W(쓰기 응답 수) = 2, R(읽기 응답 수) = 2일 때 W+R > N이면 strong consistency, W+R ≤ N이면 eventual. Amazon Dynamo(2007) 원리. |
| **합의 알고리즘 (Consensus)** | 분할된 노드 간 합의를 통한 리더 선출 및 로그 복제 | Paxos(Lamport 1998), Raft(Ongaro 2014), Zab(ZooKeeper), EPaxos(Moraru 2013). 쓰기 지연 = 리더 RTT × quorum. |
| **시간 동기화 (TrueTime)** | 전역 시간 불확실성(ε) 명시적 노출로 외부 일관성 구현 | Google Spanner의 GPS+Atomic Clock API. Commit Wait로 ε만큼 대기하여 선형화 보장, p99 약 5~10ms. |
| **안티엔트로피 & Read Repair** | 백그라운드에서 복제본 간 불일치 수렴 | Merkle Tree(Dynamo, Cassandra)로 동기화 차분 비교, Hinted Handoff로 오프라인 노드 임시 위임 후 복귀 시 재전송. |
| **벡터 클럭 / LWW / CRDT** | 동시 업데이트 충돌 해결 | Vector Clock(Dynamo) -> Last-Write-Wins(Redis, Cassandra)로 단순화, CRDT(상태/연산 기반, Riak 2.0, RedisGears)로 자동 수렴 보장. |
| **클라이언트 라우팅 (Sloppy Quorum)** | 분할 시 가용성 극대화 | 장애 노드 대신 다른 가용 노드로 쓰기 위임, 복구 시 Merkle 동기화. Cassandra `consistency = ANY/ONE/QUORUM/ALL` 옵션. |

**핵심 정량 파라미터:**
- **N=3, R=2, W=2**: 단일 노드 장애 허용, strong consistency (R+W=4>3). 지연 = 2홉 RTT.
- **N=3, R=1, W=1**: 읽기 1홉으로 빠르지만 stale read 가능성. 가용성 최대.
- **N=5, R=3, W=3**: 양 노드 장애까지 tolerance, 하지만 지연 3홉으로 WAN 환경에서 240ms+.
- **Spanner의 Commit Wait**: TrueTime ε이 최대 7ms이므로, commit timestamp 이후 ε만큼 sleep하여 외부 일관성(external consistency) 보장.

**선형화 가능성(Linearizability) 검증**:
- Jepsen(https://jepson.io) 테스트로 실제 시스템의 분할 시 동작 검증. 대표적 결함: Kafka 트랜잭션(ZooKeeper 의존성), Redis Cluster(네트워크 비对称 시 데이터 손실), MongoDB(과거 v4.0 미만 write concern 미흡).

- **📢 섹션 요약 비유**: Quorum 시스템은 **"5명의 위원회(N=5)에서 안건을 통과시키려면 최소 3명(W=3)의 동의 서명이 필요하고, 안건 내용을 확인하려면 최소 3명(R=3)에게 물어봐야 한다"**는 규칙이다. 만약 3+3 > 5이면 회의록이 절대 일관되지만, 2+2 < 5면 위원들이 각자 다른 시점의 안건을 가지고 있어 사후 정리(Merkle Tree) 작업이 필요하다.

---

## Ⅲ. 비교 및 연결

| 구분 | **CAP (Brewer, 2000)** | **PACELC (Abadi, 2010)** |
| :--- | :--- | :--- |
| **고려 시나리오** | 네트워크 분할(Partition) 시점만 분석 | 정상 운영(Else) 시점의 트레이드오프까지 포함 |
| **시간 축** | 단일 장애 이벤트(Static) | 시간 연속적 운영 모델(Dynamic) |
| **트레이드오프** | Consistency vs Availability | Partition 시: C vs A, Else 시: Latency vs Consistency |
| **설계 결정 반영도** | P는 필연이므로 C/A 선택만 명시 | PC/EC, PC/EL, PA/EC, PA/EL 4-Quadrant로 정밀 분류 |
| **실제 시스템 매핑** | Spanner(CP), DynamoDB(AP) | Spanner(PC/EC), DynamoDB(PA/EL), Cassandra(Tunable) |
| **한계** | 정상 운영 시의 비용/성능 분석 부재 | "Latency"의 정량적 정의가 시스템마다 다름 |
| **연관 연구** | FLP 불가능성, Herlihy-Wing 선형성 | HAT(Highly Available Transactions), ACID-2, TAPER |

| 구분 | **Strong Consistency (Linearizability)** | **Eventual Consistency** |
| :--- | :--- | :--- |
| **읽기 보장** | 가장 최근 쓰기 값 반환 | 수렴 후(보통 수 초) 모든 복제본 동일 |
| **쓰기 지연** | Quorum RTT × 홉 수 | 1 RTT (가용 노드만) |
| **구현** | Raft/Paxos + Sync Replication | Async Replication + Anti-entropy |
| **적용 사례** | 금융 원장, 재고 차감, 분산 락 | 장바구니, 세션 캐시, SNS 피드, IoT 텔레메트리 |
| **CAP 분류** | PC/EC | PA/EL |
| **대표 시스템** | Spanner, CockroachDB, etcd | Cassandra, Riak, DynamoDB, S3 (eventual listing) |
| **예외 케이스** | Write-Write Conflict (lost update) | Read-Your-Writes 미보장 (Session Affinity 필요) |

**다른 시스템 레이어와의 연결:**
- **분산 트랜잭션 (XA, Saga, TCC)**: CAP-CP 시스템의 Raft + 2PC vs CAP-AP 시스템의 Saga 보상 트랜잭션. `Seata`, `Apache ServiceComb Saga`가 대표.
- **메시지 큐 (Kafka, Pulsar)**: `acks=all` + `min.insync.replicas`로 strong consistency, `acks=1`로 latency 우선. Kafka KRaft(Kafka Raft) 모드는 PACELC에서 PC/EC.
- **캐시 (Redis Cluster, Memcached)**: read-through/write-through cache 패턴, 캐시 일관성 윈도우(cache coherency window) 존재. **PACELC의 EL 영역**.
- **Service Mesh (Istio, Linkerd)**: 일관성 라우팅(Consistent Hashing, Maglev) 및 retry/circuit breaker로 AP 성격 강화.
- **Storage 레이어 (S3, HDFS, MinIO)**: HDFS는 NameNode HA + QJM(Quorum Journal Manager)으로 CP, S3는 AP + eventual listing.

- **📢 섹션 요약 비유**: CAP는 **"비상시(Partition) 안전벨트 vs 에어백 선택"**이라면, PACELC는 **"평상시에도 스포츠카(저지연, 약간의 위험) vs 전동차(저전력, 느린 충전) 중 일상적으로 타고 다닐 차종을 선택"**하라는 추가 질문이다. 두 선택을 별도로 최적화해야 진짜 운전(시스템 운영)이 가능하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **데이터 분류 (Data Criticality Tiering)**
   - ① 금융 원장/결제/재고 차감 -> **CP (PC/EC)** 필수: Spanner, CockroachDB, MySQL Group Replication, etcd.
   - ② 사용자 프로필·세션·환경설정 -> **AP (PA/EL)** 권장: DynamoDB, Redis Cluster, Cassandra.
   - ③ 로그·메트릭·분석 데이터 -> **AP (PA/EL) + Time-series 최적화**: InfluxDB, TimescaleDB, Amazon Timestream.

2. **Quorum 파라미터 결정 (R, W, N 튜닝)**
   - Strong Read 보장: `R + W > N` 검증. 예: N=3, R=2, W=2.
   - Sloppy Quorum 적용: `consistency = ANY`(Cassandra)로 쓰기 가용성 극대화 시 데이터
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 521 / 800

<- **이전**: [520. 프로메테우스 PromQL 메트릭 쿼리 언어](/studynote/13_cloud_architecture/06_exam_summary/520_prometheus_promql_metrics_query_language/)
**다음**: [522. 클라우드 트랜잭션 사가 보상 패턴](/studynote/13_cloud_architecture/06_exam_summary/522_cloud_transaction_saga_compensation_pattern/) ->

---
