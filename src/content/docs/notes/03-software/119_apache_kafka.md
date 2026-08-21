---
sidebar:
  order: 119
  label: "119. Apache Kafka 이벤트 스트리밍 (Apache Kafka)"
  badge:
    text: "미출 · 70%"
    variant: note
title: "Apache Kafka 이벤트 스트리밍 (Apache Kafka)"
date: "2026-08-13T22:31:00+09:00"
tags:
  - "notes-software"
weight: 119
extra:
  question_no: "119"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "Kafka 로그•파티션•소비자 확장성이 높음"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Apache Kafka**: LinkedIn이 개발한 분산 이벤트 스트리밍 플랫폼(Distributed Event Streaming Platform)으로, 초당 수백만 건의 메시지를 디스크 Append-Only Commit Log에 순차 저장하여 초저지연 수평 분산 송수신을 담당하는 비동기 메시지 브로커.
- **Partition & Offset**: 토픽(Topic)을 수평 분할한 카프카의 기본 병렬 처리 단위(Partition)와, 파티션 내부에서 메시지마다 64-bit 순차 정수로 부여되는 고유 식별자(Offset).
- **Consumer Group**: 동일한 Topic을 병렬 소비하기 위해 다수의 컨슈머 인스턴스를 하나로 묶은 클라이언트 집합으로, 1개의 파티션은 그룹 내 단 1개의 컨슈머만 1:1 매핑 점유.

</details>

- 정의/개념: 파티션 로그에 이벤트를 보존•재생하는 **Apache Kafka**
- 배경/필요성: 소모성 큐만으로는 **다중 구독•과거 재처리** 제약

#### 한줄 요약

- 이벤트를 분산 일지에 보존하고 여러 독자가 각자 읽는 플랫폼이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Zero-Copy Technology**: OS Kernel의 `sendfile()` 시스템 콜을 활용해, 디스크 페이지 캐시에서 네트워크 NIC 버퍼로 직접 데이터를 전송하여 CPU/메모리 복사 오버헤드를 0으로 차단.
- **ISR (In-Sync Replicas)**: Leader 파티션의 최신 Offset을 지연 없이 실시간 추종하고 있는 하이 퀄리티 Follower 레플리카 노드들의 집합.

</details>

- **High Throughput & Low Latency (Zero-Copy & PageCache 기술 활용)**
- **Decoupled Architecture & Message Replay (Offset 조작으로 과거 이벤트 재처리)**
- **Distributed Replication (Leader-Follower ISR 기반 고가용성 보장)** #### 한줄 요약

- 병렬성과 재처리는 좋으나 순서 보장과 편중 및 재배정을 관리해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Producer, Broker, Consumer, Controller**: 카프카 시스템을 이끄는 4대 물리적 핵심 요소.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Apache Kafka Cluster Architecture               │
├────────────────────────────────────────────────────────────────────────┤
│ [Producer] ──► [Broker 1 (Topic A - Partition 0 Leader)] ──► [Consumer A]│
│                [Broker 2 (Topic A - Partition 1 Leader)] ──► [Consumer B]│
│                     │ (ISR Replication)                                │
│                     ▼                                                  │
│                [Broker 3 (Topic A - Partition 0/1 Follower)]           │
├────────────────────────────────────────────────────────────────────────┤
│ Cluster Metadata Management: Apache ZooKeeper or KRaft (Kafka Raft)    │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Producer가 메시지를 아키텍처 파티션 리더 노드에 보내고, ISR 팔로워 노드가 이를 복제하며, 컨슈머 그룹이 오프셋을 읽어 처리하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| Producer | 키로 파티션을 선택해 이벤트 발행 |
| Topic•Partition | 이벤트 순서•병렬성•보존 경계 제공 |
| Broker•ISR | 파티션 리더 저장과 팔로워 복제 |
| KRaft Controller | 클러스터 메타데이터와 리더 선출 관리 |
| Consumer Group | 파티션 분담과 처리 오프셋 관리 |

#### 한줄 요약

- 작성자, 번호 일지, 사본 서버, 관리자, 독자 모임으로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **`acks=all` (`acks=-1`)**: Leader 파티션뿐만 아니라 ISR 그룹 내의 모든 `min.insync.replicas` 노드가 유효하게 기록 완료 메시지(ACK)를 보낼 때까지 Producer가 기다리는 최고 안전성 옵션.

</details>

```text
[이벤트 발행]
      │
      ▼
1. 파티션 선택
      │
      ▼
2. 리더 로그 기록
      │
      ▼
3. ISR 복제
      │
      ▼
4. ACK 조건 판정
      │
      ▼
5. 발행 결과 반환
```

### 동작 원리

1. 파티션 선택: 키•파티셔너로 순서 경계 결정
2. 리더 로그 기록: 담당 Broker가 로그 끝에 이벤트 추가
3. ISR 복제: 팔로워가 리더 오프셋을 추종
4. ACK 조건 판정: acks•min ISR 조건 충족 확인
5. 발행 결과 반환: 성공 오프셋 또는 재시도 오류 응답

#### 한줄 요약

- 작성자는 번호 붙은 일지에 기록하고 독자는 마지막으로 처리한 번호를 책갈피로 저장한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **RabbitMQ vs Kafka**: RabbitMQ는 메시지 발송 후 소멸되는 전통적 AMQP 큐, Kafka는 디스크 보존형 Pub/Sub 이벤트 로그 플랫폼.

</details>

| 구분 | Traditional Message Queue (RabbitMQ) | Event Streaming Platform (Kafka) |
|:---|:---|:---|
| 메시지 보존 방식 | **소비자(Consumer) 수신 즉시 Queue에서 삭제** | **디스크 영속성 보존 (일수/용량 단위 retention)** |
| 메시지 재처리 | 큐 정책•DLQ 범위에서 재처리 | **Offset 이동으로 보존 이벤트 재생** |
| 처리 성능 | 라우팅•확인 정책에 좌우 | 파티션•배치•복제 정책에 좌우 |
| 라우팅 기능 | 복잡한 Exchange / Binding 라우팅 우수 | Simple Topic/Partition 라우팅 중심 |

#### 한줄 요약

- 작업 큐는 일을 나눠 끝내는 데, Kafka는 사건을 남겨 여러 독자가 다시 읽는 데 초점을 둔다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Consumer Lag**: Producer의 최신 메시지 생성 오프셋과 Consumer가 현재 소비 완료한 오프셋 간의 지연 격차 지표.
- **Rebalance Storm**: 컨슈머 추가/가동중단 시 전체 컨슈머 그룹의 파티션 매핑이 일시 멈추고 다시 배정되는 락업 현상.

</details>

| 실무 장애 및 병목 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| Consumer Lag 폭증 | 컨슈머 연산 속도가 프로듀서 전송 속도를 못 따라감 | **파티션 개수 확장 및 컨슈머 인스턴스 동시 증설** |
| Rebalance Storm 발생 | `max.poll.interval.ms` 시간 초과로 컨슈머 쫓겨남 | **`max.poll.records` 단축 및 Cooperative Rebalance 적용** |
| 메시지 중복 수신 (At-Least-Once) | 컨슈머 처리 성공 후 오프셋 커밋 전 튕김 발생 | **Consumer 로직 멱등성(Idempotency) 구현** |

> 사례: **쿠팡 / 네이버 Kafka 기반 실시간 로그 수집 & Flink Stream 파이프라인 연동** #### 한줄 요약

- 같은 주문의 순서는 한 일지에서 지키고 각 일지의 밀린 양을 따로 봐야 한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Kafka 수립 기준(Apache Kafka Standards)**: Zero-Copy 파이프라인, `acks=all` 내구성, KRaft 메타데이터 및 Consumer Lag 모니터링 체계에 의거한 기준.

</details>

- 사건 보존•다중 재생은 **Kafka**, 복잡한 작업 라우팅은 메시지 큐 선택

#### 한줄 요약

- 선택 기준은 순서 경계와 사건 재생 기간을 함께 정한다.
