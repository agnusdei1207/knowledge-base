---
sidebar:
  order: 119
  label: "119. Apache Kafka"
  badge:
    text: "미출 · 70%"
    variant: note
title: "Apache Kafka"
date: "2026-08-25T11:00:00+09:00"
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

- **Apache Kafka**: 이벤트를 불변 커밋 로그(Commit Log)에 순차 기록하여 고성능 Pub/Sub 및 스트림 처리를 지원하는 분산 스트리밍 플랫폼.
- **Partition & Offset**: 토픽의 수평 병렬 처리 기본 단위(Partition)와 파티션 내에서 메시지의 순차적 위치를 나타내는 64비트 정수(Offset).

</details>

- 정의/개념: 대규모 이벤트를 **디스크 Append-Only 파티션 로그에 순차 저장하고 Zero-Copy 및 ISR 복제로 초고속 송수신·재생하는 분산 스트리밍 플랫폼**
- 배경/필요성: 전통적 소모성 메시지 큐의 **메시지 즉시 삭제로 인한 다중 구독 불가, 과거 데이터 소급 재생 불가 및 대용량 I/O 병목 해결 불가**

#### 한줄 요약
- 파티션 분산 로그와 Zero-Copy 전송을 통해 초고성능 이벤트 스트리밍과 메시지 재생을 지원한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Zero-Copy**: OS 커널의 `sendfile()` 시스템 콜을 활용하여 디스크 페이지 캐시에서 네트워크 소켓으로 직접 데이터를 전송하는 기법.
- **ISR(In-Sync Replicas)**: 리더 파티션의 최신 오프셋을 지연 없이 실시간으로 따라잡고 있는 동기화 팔로워 복제본 그룹.

</details>

- PageCache 및 OS `sendfile()`을 활용한 **초고처리량·초저지연(Zero-Copy) I/O**
- 컨슈머 오프셋(Offset) 조작을 통한 **이벤트 영속 보존 및 과거 데이터 소급 재생**
- Leader-Follower 복제 및 **ISR(In-Sync Replicas) 기반 무손실 고가용성 보장**

#### 한줄 요약
- Zero-Copy 고속 전송, 영속 로그 기반 메시지 재생, ISR 고가용성을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Producer, Broker, Consumer Group, KRaft**: 이벤트를 발행하는 프로듀서, 저장 브로커, 병렬 소비 컨슈머 그룹, 쿼럼 메타데이터 관리자 KRaft.

</details>

```text
[Apache Kafka 분산 스트리밍 아키텍처]
|-- Producer (메시지 키 기반 파티셔너 라우팅 및 배치 압축 전송)
`-- Kafka Broker Cluster (KRaft Raft 쿼럼 기반 메타데이터 관리)
    |-- [Broker 1] -> Topic A - Partition 0 (Leader) ◄──► Consumer 1 (Group A)
    |-- [Broker 2] -> Topic A - Partition 1 (Leader) ◄──► Consumer 2 (Group A)
    `-- [Broker 3] -> Partition 0, 1 (ISR Follower 복제본 보관)
```

선의 의미: 계층 및 Producer의 발행, Broker 파티션 저장 및 ISR 복제, Consumer Group의 병렬 구독 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **프로듀서 (Producer)** | 메시지 키(Key)를 해싱하여 **타깃 파티션으로 이벤트를 일괄 배치(Batch) 발행** | `acks=all`, 멱등성 프로듀서 |
| **토픽 및 파티션** | 메시지가 순차 저장되는 **Append-Only 로그 파일이자 병렬 처리의 기본 단위** | 파티션 단위 순서 보장 |
| **브로커 및 ISR** | 파티션 리더로서 쓰기/읽기를 처리하고 **팔로워 복제본과 동기화(ISR) 유지** | 디스크 순차 쓰기 ($O(1)$) |
| **컨슈머 그룹 (Consumer)**| 파티션과 컨슈머를 1:1 매핑하여 **오프셋 기반으로 병렬 구독 및 커밋 수행** | 파티션 리밸런싱 지원 |
| **KRaft 컨트롤러** | 주키퍼(ZooKeeper) 없이 **Raft 합의 알고리즘으로 클러스터 메타데이터 관리** | 메타데이터 전파 10배 가속 |

#### 한줄 요약
- 프로듀서, 토픽/파티션, 브로커/ISR, 컨슈머 그룹, KRaft 컨트롤러로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **`acks=all` 커밋 절차**: Producer 발행 $\to$ Leader 로그 기록 $\to$ ISR Follower 복제 $\to$ Quorum 확인 $\to$ Producer 성공 ACK.

</details>

```text
클라이언트 프로듀서의 이벤트 발행 요청 (`acks=all`)
        │
   1. [파티션 라우팅] Producer가 Key 해시를 계산하여 대상 Broker의 Partition Leader로 전송
        │
   2. [리더 로그 기록] Partition Leader가 OS PageCache 디스크 로그 끝에 순차 추가 (Append-Only)
        │
   3. [ISR 복제] 팔로워 브로커들이 리더로부터 변경 오프셋을 즉시 Fetch하여 로컬 복제
        │
   4. [ACK 판정] `min.insync.replicas`(예: 2대) 노드에 복제 완료 확인 후 리더가 Producer에 ACK 반환
        │
   5. 컨슈머 그룹이 최신 High Watermark 오프셋을 읽어 비즈니스 로직을 병렬 소비
```

#### 한줄 요약
- 파티션 라우팅 → 리더 로그 기록 → ISR 복제 → ACK 반환 → 컨슈머 오프셋 구독 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **RabbitMQ vs Kafka**: 메시지 수신 즉시 삭제되는 전통 큐(RabbitMQ)와 디스크에 영속 보존되는 이벤트 스트림(Kafka).

</details>

| 비교 항목 | 전통적 메시지 큐 (RabbitMQ) | 이벤트 스트리밍 플랫폼 (Apache Kafka) |
|:---|:---|:---|
| 메시지 수명주기 | **소비자(Consumer) 수신 즉시 Queue에서 영구 삭제**| **설정된 보존 기간(Retention) 동안 디스크 영구 보존**|
| 다중 구독 모델 | 단일 큐에 여러 소비자가 경쟁 소비 (경쟁 컨슈머) | **컨슈머 그룹별로 독립 오프셋을 유지하며 다중 구독** |
| 과거 데이터 재생 | 불가 (DLQ 재처리 수준에 국한) | **오프셋(Offset)을 과거로 되돌려 무제한 소급 재생** |
| 처리 성능 및 지연 | 초당 수만 건 (메모리 중심 큐잉) | **초당 수백만 건 (Zero-Copy & 디스크 순차 쓰기)** |

#### 한줄 요약
- 단순 작업 분배 큐는 RabbitMQ, 이벤트 영속 보존과 대규모 스트리밍 처리는 Kafka를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Rebalance Storm**: 컨슈머 추가/장애 시 파티션 재할당(Rebalance)으로 인해 전체 컨슈머의 읽기가 일시 중단되는 락업 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 컨슈머 처리 속도 저하로 인한 **Consumer Lag** 급증 | **파티션 수 확장 및 컨슈머 인스턴스 1:1 증설 (Scale-Out)** | 지연 Lag 0화 및 처리량 증대 |
| 컨슈머 장애 시 전체 파티션 멈춤 (**Rebalance Storm**) | **`CooperativeStickyAssignor` 협력적 리밸런싱 알고리즘 적용** | 무중단 점진적 파티션 이전 |
| 네트워크 재시도로 인한 메시지 중복 수신 | **`enable.idempotence=true` 및 컨슈머 멱등성(Idempotency) 로직 구현**| 중복 데이터 처리 원천 방지 |
| 브로커 다운 시 메시지 유실 위험 | **`acks=all` 및 `min.insync.replicas=2` 강제 설정** | RPO=0 무손실 내구성 확보 |

#### 한줄 요약
- 파티션/컨슈머 증설, 협력적 리밸런싱, 멱등성 설정, acks=all로 안정성을 보장한다.

## Ⅶ. 결론

- 마이크로서비스 간 비동기 이벤트 주도 아키텍처(EDA) 및 실시간 분석을 위해 **Apache Kafka의 파티션 로그와 Zero-Copy 기술을 엔터프라이즈 이벤트 허브로 구축**하고, **KRaft 컨트롤러와 멱등 프로듀서 설정**을 통해 차세대 이벤트 스트리밍 완성

#### 한줄 요약
- Apache Kafka는 디스크 순차 로그와 Zero-Copy 전송을 기반으로 초고성능 이벤트 스트리밍과 메시지 재생을 실현하는 현대 분산 데이터 인프라의 핵심 플랫폼이다.