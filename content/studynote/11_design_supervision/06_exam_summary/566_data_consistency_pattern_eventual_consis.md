---
title: "Data Consistency Pattern Eventual Consistency"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CAP 정리에서 AP(가용성·분할내성)를 우선시하는 약한 일관성 모델로, 복제본 간 일시적 불일치를 허용하되 "충분한 시간과 메시지 전달"이 보장되면 모든 노드가 동일한 값으로 수렴하는 분산 시스템의 핵심 패턴. 충돌 해소는 Vector Clock, LWW(Last-Write-Wins), CRDT(Conflict-free Replicated Data Type) 등으로 처리한다.
> 2. **가치**: 글로벌 멀티리전 환경에서 쓰기 지연시간을 10~50ms 수준으로 단축하고, 네트워크 파티션·노드 장애 시에도 99.99% 이상의 쓰기 가용성을 확보한다. Amazon DynamoDB, Apache Cassandra, Riak 등은 이를 통해 초당 수백만 건의 글로벌 쓰기를 처리한다.
> 3. **판단 포인트**: 비즈니스 도메인별로 허용 가능한 staleness window(SLA)를 정의하고, N/R/W 쿼럼과 슬롭(stale-read) 허용 범위를 수치로 결정해야 한다. 사용자 세션·재고 차감·금융 원장 등 강한 일관성이 필요한 흐름은 Saga, Outbox, 2PC 같은 보완 패턴과 함께 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적인 RDBMS 기반의 ACID 트랜잭션은 단일 데이터센터·단일 분할 환경에서 강력한 일관성을 보장한다. 그러나 2000년대 중반 Amazon, Google, Facebook이 글로벌 서비스를 확장하면서 다음의 한계가 명확해졌다.

- **단일 마스터의 쓰기 병목**: 2-Phase Commit(2PC) 기반의 동기식 복제는 코디네이터 장애 시 전체 트랜잭션이 블로킹되고, 멀티리전 RTT(예: 서울-도쿄 30ms, 서울-프랑크푸르트 250ms) 누적 시 쓰기 처리량이 급감한다.
- **파티션 내성 부재**: 네트워크 단절 시 가용성(Availability)이 0으로 떨어지며, Paxos/Raft 합의 알고리즘도 마이너리티 파티션에서는 쓰기 거부(quorum loss) 상태가 발생한다.
- **도메인별 일관성 요구 불균질**: 사용자 프로필·상품 리뷰·IoT 센서 측정값은 1~2초의 지연이 허용되지만, 결제·재고 차감·좌석 예약은 즉시 일관성이 필수다. 단일 일관성 모델로는 모든 워크로드를 효율적으로 처리할 수 없다.
- **데이터 볼륨 폭증**: 단일 노드가 처리할 수 없는 페타바이트급 시계열·로그·이벤트 스트림은 본질적으로 다중 마스터·비동기 복제 아키텍처를 요구한다.

이에 2007년 Amazon Dynamo 페이퍼, 2008년 Werner Vogels의 "Eventually Consistent" 선언, 그리고 2009년 BASE(Basically Available, Soft state, Eventually consistent) 용어 정립을 통해, **데이터 일관성 패턴의 패러다임이 "강한 일관성 우선"에서 "도메인별 적정 일관성 + 보상 트랜잭션"으로 전환**되었다.

```text
  [Old Paradigm] Strong Consistency Only (ACID)      [New Paradigm] Consistency Spectrum
  +----------------------------+                    +------------------------------------+
  |   Client -> Master DB       |                    |     +--------------+  +----------+ |
  |       v sync 2PC           |                    |     | Strong Zone  |  | Weak Zone| |
  |   Replica 1, 2, 3          |                    |     | (주문/결제)   |  | (피드/리뷰)| |
  |   단일 리전 종속            |                    |     +------+-------+  +----+-----+ |
  |   가용성 99.9%              |                    |            | Saga/Outbox    |        |
  |   쓰기 p99 = 80ms           |                    |     +------v---------------v-----+ |
  +----------------------------+                    |     |   Eventual Consistency    | |
                                                    |     |   + CRDT + Vector Clock   | |
                                                    |     |   글로벌 멀티리전 + AP     | |
                                                    |     |   가용성 99.99% / p9≈15ms | |
                                                    |     +--------------------------+ |
                                                    +------------------------------------+
```

- **📢 섹션 요약 비유**: 마치 전 세계 100개 우체국이 각자 우편물을 분류하다가, 1시간 정도 지난 뒤 같은 주소의 편지는 결국 같은 배달함에 모이도록 약속한 **"느슨한 우편 합의 시스템"**과 같다. 중간에는 잠깐 다른 곳에 가 있을 수 있지만, 결국은 같은 곳으로 수렴한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

이벤추얼 일관성의 핵심 메커니즘은 **쓰기 전파(Write Propagation) -> 일시적 분기(Temporary Divergence) -> 충돌 감지·해소(Conflict Detection & Resolution) -> 백그라운드 수렴(Anti-entropy Convergence)**의 4단계 사이클이다.

```text
  [Client A]                                       [Client B]
  write(k, "Apple", v=3)                           write(k, "Apple", v=5)
       |                                                  |
       v                                                  v
  +---------+                                       +---------+
  | Coord N1 | --- (Local W=1, Async) ----------►  | Coord N2 |
  +----+----+                                       +----+----+
       | Coordinator 결정 (DHT Ring 기준)             |
       v                                                  v
  +---------+   +---------+   +---------+      +---------+
  | Node 1  |   | Node 2  |   | Node 3  |      | Node 4  |
  | v=3 ★  |   | v=3     |   | v=3     |      | v=5     | (DHT ring의 다른 위치)
  | t=100   |   | t=100   |   | t=100   |      | t=105   |
  +----+----+   +----+----+   +----+----+      +----+----+
       |             |             |                |
       +----- Gossip/Merkle Sync (주기적 anti-entropy) ---+
                              |
                              v (Conflict Resolver)
              +---------------------------------------+
              | if(vector clock causal -> apply)       |
              | else(LWW)  -> v=5 (newer timestamp)   |
              | else(CRDT G-Set/PN-Counter -> merge)  |
              +---------------------------------------+
                              |
                              v
              +---------------------------------------+
              |  최종 수렴 상태: Node1=v5, Node2=v5,  |
              |  Node3=v5, Node4=v5 (consistency OK) |
              +---------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Coordinator Node** | 클라이언트 요청 수신, DHT(Consistent Hashing) 링 상의 복제 대상 노드 결정, 응답 반환 | Dynamo-style preference list, Cassandra Partitioner(Murmur3), Riak Ring |
| **Storage Node (Replica)** | 실제 데이터 저장·복제·읽기 처리. 각 노드는 local storage engine(LSM Tree: LevelDB/RocksDB/SSTable) 사용 | Hint-based replication, Log-Structured Merge(LSM) 트리로 쓰기 증폭 최소화 |
| **Anti-Entropy Service** | 백그라운드에서 Merkle Tree 해시 비교를 통해 분기된 복제본을 탐지·수정 | Dynamo-style Merkle Tree(per key range SHA-1), Gossip protocol(Epidemic Protocol) |
| **Conflict Resolver** | 동시 쓰기로 인한 버전 충돌 시 정책 적용: LWW, Vector Clock causal ordering, CRDT merge | Vector Clock (node, counter) 쌍의 인과 관계 추적, CRDT 4종(G-Counter, PN-Counter, G-Set, OR-Set, LWW-Register) |
| **Sloppy Quorum & Hinted Handoff** | 정상 N개 노드 중 일부가 장애일 때, 임시로 다른 가용 노드에 write를 위임하고 복구 시 원래 노드로 전달 | Dynamo의 "handoff" 메커니즘, Cassandra의 "write to any available replica" |
| **Read Repair** | read quorum 응답 중 버전 차이 발견 시, 최신 버전을 다른 노드에 동기화 | Dynamo: read-time 동기화, Cassandra: read repair chance 0.1 설정 |
| **Tombstone & GC** | 삭제 표시 후 physical delete는 lazy GC로 처리. gc_grace_seconds 동안 보존 | Cassandra tombstone, Riak allow_mult=true 환경의 sibling 처리 |

### 핵심 공식과 튜닝 파라미터

**Quorum Equation** — N(복제본 수), W(쓰기 정족수), R(읽기 정족수):
- `W + R > N`  -> **Strong Consistency** (모든 읽기가 최신 쓰기 포함)
- `W + R ≤ N`  -> **Eventual Consistency** 가능 (stale read 허용)
- 일반적 운영값: **N=3, W=2, R=2** (strong), **N=3, W=1, R=1** (eventual, latency 1 RTT)
- `W + R ≤ N` 인 경우 stale read 확률 ≈ `1 - (1 - (1-W/N)^w * (1-R/N)^r)`로 산출 가능 (Cassandra 문서 참조)

**Vector Clock 비교** — 두 버전 `Va = {(n1,3), (n2,1)}`, `Vb = {(n1,4), (n2,1)}`:
- `Va < Vb` 이면 Va가 인과적으로 이전 (Vb 채택)
- `Va || Vb` (incomparable) 이면 진짜 동시 충돌 -> Conflict Resolver 호출

**CAP 가용성 계산**: 정상 노드 비율이 W/N 미만이 되는 순간 쓰기 거부 발생. N=3, W=2일 때 2개 노드 장애까지 쓰기 가능(가용성 99.99% SLA). 슬로피 쿼럼은 일시적으로 4번째 노드로 핸드오프하여 100% 가용성에 근접.

- **📢 섹션 요약 비유**: **"동시 통역 다국어 회의실"**과 같다. 4명의 통역사가 각자 같은 문장을 다른 스타일로 받아쓰지만, 회의 종료 1시간 후 모든 통역 노트가 동일한 의미로 통일되고, 충돌 시 "더 신뢰할 만한 출처"의 버전을 채택한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **Strong Consistency (ACID)** | **Eventual Consistency (BASE)** | **Causal Consistency** |
| :--- | :--- | :--- | :--- |
| **일관성 보장** | read 후 모든 노드에서 최신값 보장 | 충분한 시간 후 수렴 (보장 없음) | 인과 관계가 있는 쓰기는 순서 보장 |
| **가용성** | 파티션 시 가용성 저하 (CP) | 파티션 시에도 쓰기 가능 (AP) | 파티션 시 인과 단위로 가용 |
| **쓰기 지연** | multi-RTT (2PC, Paxos commit) | 1 RTT (local quorum) | 1~2 RTT (dependency tracking) |
| **적합 도메인** | 금융 원장, 좌석예약, 재고 차감 | 소셜 피드, IoT 측정, 카운터, 프로필 | 댓글 스레드, 채팅, 협업 문서 |
| **충돌 처리** | Locking / 2PC로 사전 차단 | LWW / Vector Clock / CRDT 사후 병합 | 인과 의존성 그래프 추적 |
| **대표 시스템** | Google Spanner, CockroachDB, etcd | Cassandra, DynamoDB, Riak, Cosmos DB | ChainReplication, COPS, Eiger |

**연계 기술 상세:**

- **Saga Pattern**: 장기 트랜잭션을 로컬 트랜잭션들의 체인으로 분해하고, 실패 시 보상 트랜잭션으로 롤백. 이벤트추얼 일관성과 자주 결합되어 마이크로서비스 환경의 분산 트랜잭션을 해결한다(예: 주문 -> 결제 -> 재고 -> 배송).
- **Outbox Pattern**: 도메인 DB 트랜잭션과 이벤트 발행을 동일 트랜잭션으로 묶고, 별도 CDC(Change Data Capture) 프로세스(Debezium, Maxwell)가 outbox 테이블을 읽어 Kafka로 발행 -> **At-least-once 이벤트 전달** 보장.
- **CDC (Change Data Capture)**: DB의 redo/binlog를 tail하여 이벤트 스트림 생성. Debezium + Kafka + Kafka Connect Sink 조합으로 MySQL->Cassandra 동기화에 활용.
- **
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 566 / 600

<- **이전**: [565. 메시지 큐 비동기 통신 패턴](/studynote/11_design_supervision/06_exam_summary/565_message_queue_async_communication_patter)
**다음**: [567. 멱등성 설계 중복 요청 처리](/studynote/11_design_supervision/06_exam_summary/567_idempotency_design_duplicate_request_han/) ->

---
