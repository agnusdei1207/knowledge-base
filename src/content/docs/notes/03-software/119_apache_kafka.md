---
sidebar:
  order: 119
  label: "119. Apache Kafka 이벤트 스트리밍 (Apache Kafka)"
  badge:
    text: "미출 • 70%"
    variant: note
title: "Apache Kafka 이벤트 스트리밍 (Apache Kafka)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **Apache Kafka**: LinkedIn이 개발한 분산 이벤트 스트리밍 플랫폼(Distributed Event Streaming Platform)으로, 초당 수백만 건의 메시지를 디스크 Append-Only Commit Log에 순차 저장하여 초저지연 수평 분산 송수신을 담당하는 비동기 메시지 브로커.
- **Partition & Offset**: 토픽(Topic)을 수평 분할한 카프카의 기본 병렬 처리 단위(Partition)와, 파티션 내부에서 메시지마다 64-bit 순차 정수로 부여되는 고유 식별자(Offset).
- **Consumer Group**: 동일한 Topic을 병렬 소비하기 위해 다수의 컨슈머 인스턴스를 하나로 묶은 클라이언트 집합으로, 1개의 파티션은 그룹 내 단 1개의 컨슈머만 1:1 매핑 점유.

</details>

- 정의/개념: 대규모 실시간 스트림 데이터를 순차 Commit Log 파티션에 Append-Only 디스크 전송하여, 생산자(Producer)와 소비자(Consumer) 간 결합도를 완벽히 분리하는 분산 이벤트 스트리밍인 **Apache Kafka**
- 배경/필요성: 기존 Message Queue(RabbitMQ)의 디스크 렌더링 한계 및 1:1 소모성 메시징 한계 극복, 1:N 이종 시스템으로의 대용량 실시간 이벤트 데이터 Pub/Sub 수용 요구성

#### 한줄 요약

- 이벤트를 분산 일지에 보존하고 여러 독자가 각자 읽는 플랫폼이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Zero-Copy Technology**: OS Kernel의 `sendfile()` 시스템 콜을 활용해, 디스크 페이지 캐시에서 네트워크 NIC 버퍼로 직접 데이터를 전송하여 CPU/메모리 복사 오버헤드를 0으로 차단.
- **ISR (In-Sync Replicas)**: Leader 파티션의 최신 Offset을 지연 없이 실시간 추종하고 있는 하이 퀄리티 Follower 레플리카 노드들의 집합.

</details>

- **High Throughput & Low Latency (Zero-Copy & PageCache 기술 활용)**
- **Decoupled Architecture & Message Replay (Offset 조작으로 과거 이벤트 재처리)**
- **Distributed Replication (Leader-Follower ISR 기반 고가용성 보장)**

#### 한줄 요약

- 병렬성과 재처리는 좋으나 순서 보장과 편중 및 재배정을 관리해야 한다.

## Ⅲ. 구조 및 구성요소 (Kafka 4대 아키텍처 및 ISR 구조)

<details><summary>핵심 용어</summary>

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

| 구성요소 (Element) | 역할 및 기술 메커니즘 | 실무 튜닝 파라미터 |
|:---|:---|:---|
| **Topic & Partition** | 메시지가 분류 저장되는 단위 및 수평 병렬 처리 축 | 파티션 수 = 최대 컨슈머 개수 |
| **Offset** | 파티션 내 메시지 순서 번호 (0, 1, 2, 3...) | **`__consumer_offsets` 자동 커밋** |
| **ISR (In-Sync Replicas)**| Leader의 최신 오프셋을 바짝 추적하는 Follower 집합| `min.insync.replicas=2` |
| **KRaft (Kafka Raft)** | ZooKeeper를 대체하는 카프카 전용 내장 합의 엔진 | Controller 노드 메타데이터 튜닝 |

#### 한줄 요약

- 작성자, 번호 일지, 사본 서버, 관리자, 독자 모임으로 구성된다.

## Ⅳ. 흐름도 (Kafka acks 옵션에 따른 내구성/성능 트레이드오프)

<details><summary>핵심 용어</summary>

- **`acks=all` (`acks=-1`)**: Leader 파티션뿐만 아니라 ISR 그룹 내의 모든 `min.insync.replicas` 노드가 유효하게 기록 완료 메시지(ACK)를 보낼 때까지 Producer가 기다리는 최고 안전성 옵션.

</details>

```text
[Producer Write (acks=all)] ──► [Partition Leader Node]
                                       │
                                       ▼ (ISR Replication)
                                [ISR Follower Nodes] ──► [ACK Sent] ──► [Producer OK]
```

### 동작 원리

1. **`acks=0`**: Leader에 쓰여졌는지 확인하지 않고 무조건 다음 메시지 송신 (속도 극대화, 유실 위험).
2. **`acks=1`**: Leader 노드 디스크 PageCache 기록만 확인 후 ACK 수신 (기본값).
3. **`acks=all`**: Leader 및 ISR 지정 노드가 모두 기록 완료할 때까지 대기 (**유실 0% 완벽 보장**).

#### 한줄 요약

- 작성자는 번호 붙은 일지에 기록하고 독자는 마지막으로 처리한 번호를 책갈피로 저장한다.

## Ⅴ. 종류 및 비교 (Message Queue 대 Event Streaming Platform)

<details><summary>핵심 용어</summary>

- **RabbitMQ vs Kafka**: RabbitMQ는 메시지 발송 후 소멸되는 전통적 AMQP 큐, Kafka는 디스크 보존형 Pub/Sub 이벤트 로그 플랫폼.

</details>

| 비교 항목 | Traditional Message Queue (RabbitMQ) | Event Streaming Platform (Kafka) |
|:---|:---|:---|
| **메시지 보존 방식** | **소비자(Consumer) 수신 즉시 Queue에서 삭제** | **디스크 영속성 보존 (일수/용량 단위 retention)** |
| **메시지 재처리** | 삭제되므로 과거 메시지 재처리 불가능 | **Offset 수동 조작으로 과거 이벤트 N번 재처리** |
| **처리 성능 (TPS)** | 보통 (초당 수만 건 내외) | **초고속 (Zero-Copy 기반 초당 수백만 건)** |
| **라우팅 기능** | 복잡한 Exchange / Binding 라우팅 우수 | Simple Topic/Partition 라우팅 중심 |

#### 한줄 요약

- 작업 큐는 일을 나눠 끝내는 데, Kafka는 사건을 남겨 여러 독자가 다시 읽는 데 초점을 둔다.

## Ⅵ. 실무 고려사항 및 대책 (Kafka Rebalance 병목 & Consumer Lag)

<details><summary>핵심 용어</summary>

- **Consumer Lag**: Producer의 최신 메시지 생성 오프셋과 Consumer가 현재 소비 완료한 오프셋 간의 지연 격차 지표.
- **Rebalance Storm**: 컨슈머 추가/가동중단 시 전체 컨슈머 그룹의 파티션 매핑이 일시 멈추고 다시 배정되는 락업 현상.

</details>

| 실무 장애 및 병목 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **Consumer Lag 폭증** | 컨슈머 연산 속도가 프로듀서 전송 속도를 못 따라감 | **파티션 개수 확장 및 컨슈머 인스턴스 동시 증설** |
| **Rebalance Storm 발생**| `max.poll.interval.ms` 시간 초과로 컨슈머 쫓겨남 | **`max.poll.records` 단축 및 Cooperative Rebalance 적용** |
| 메시지 중복 수신 (At-Least-Once) | 컨슈머 처리 성공 후 오프셋 커밋 전 튕김 발생 | **Consumer 로직 멱등성(Idempotency) 구현** |

> 사례: **쿠팡 / 네이버 Kafka 기반 실시간 로그 수집 & Flink Stream 파이프라인 연동**

#### 한줄 요약

- 같은 주문의 순서는 한 일지에서 지키고 각 일지의 밀린 양을 따로 봐야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Kafka 수립 기준(Apache Kafka Standards)**: Zero-Copy 파이프라인, `acks=all` 내구성, KRaft 메타데이터 및 Consumer Lag 모니터링 체계에 의거한 기준.

</details>

- **Kafka 수립 기준**에 따라 대용량 실시간 이벤트 아키텍처 구축 시 **Kafka Cluster & `acks=all` & KRaft** 필수 적용

#### 한줄 요약

- 선택 기준은 순서 경계와 사건 재생 기간을 함께 정한다.
