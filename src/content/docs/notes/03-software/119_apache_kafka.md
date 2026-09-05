---
sidebar:
  order: 119
  label: "119. Apache Kafka"
  badge:
    text: "미출 · 70%"
    variant: note
title: "Apache Kafka"
date: "2026-08-31T10:48:00+09:00"
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

- 정의/개념: 이벤트를 파티션 커밋 로그에 저장해 발행·구독·재생하는 플랫폼
- 배경/필요성: 전통적 메시지 큐의 메모리 고갈, **소비 후 삭제에 따른 과거 데이터 재처리 불가 및 점대점 결합도 한계**

#### 한줄 요약
- Kafka는 소비된 메시지를 지우지 않고 보존 기간으로만 관리하므로 재생과 다중 구독이 부가 비용 없이 따라오지만, 그 대가로 저장 용량과 보존 정책이 운영의 중심 변수가 된다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Zero-Copy**: OS 커널의 `sendfile()` 시스템 콜을 활용하여 디스크 페이지 캐시에서 네트워크 소켓으로 직접 데이터를 전송하는 기법.
- **ISR(In-Sync Replicas)**: 리더 파티션의 최신 오프셋을 지연 없이 실시간으로 따라잡고 있는 동기화 팔로워 복제본 그룹.

</details>

- PageCache와 `sendfile()`을 활용한 Zero-Copy I/O
- 컨슈머 오프셋(Offset) 조작을 통한 이벤트 영속 보존 및 과거 데이터 소급 재생
- Leader-Follower 복제와 ISR 기반 장애 복구

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
    |-- Broker 1
    |   `-- Topic A - Partition 0
    |-- Broker 2
    |   `-- Topic A - Partition 1
    `-- Broker 3
        `-- ISR Follower 복제본
```

선의 의미: 계층 및 Producer의 발행, Broker 파티션 저장 및 ISR 복제, Consumer Group의 병렬 구독 구조

| 구성요소 | 책임 |
|:---|:---|
| 프로듀서 | 키 기반 파티션 선택과 이벤트 발행 |
| 토픽·파티션 | Append-Only 로그와 순서 범위 제공 |
| 브로커·ISR | 파티션 읽기·쓰기와 복제본 동기화 |
| 컨슈머 그룹 | 오프셋 기반 병렬 소비와 커밋 |
| KRaft 컨트롤러 | 합의 기반 클러스터 메타데이터 관리 |

#### 한줄 요약
- 파티션이 병렬 처리의 단위이자 순서 보장의 경계를 겸하므로 처리량을 늘리려 파티션을 쪼갤수록 전역 순서는 포기해야 하고, 컨슈머 수도 파티션 수를 넘어설 수 없다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **`acks=all` 커밋 절차**: Producer 발행 $\to$ Leader 로그 기록 $\to$ ISR Follower 복제 $\to$ Quorum 확인 $\to$ Producer 성공 ACK.

</details>

```text
클라이언트 프로듀서의 이벤트 발행 요청 (`acks=all`)
        │
   [파티션 라우팅] Producer가 Key 해시를 계산하여 대상 Broker의 Partition Leader로 전송
        │
   [리더 로그 기록] Partition Leader가 OS PageCache 디스크 로그 끝에 순차 추가 (Append-Only)
        │
   [ISR 복제] 팔로워 브로커들이 리더로부터 변경 오프셋을 즉시 Fetch하여 로컬 복제
        │
   [ACK 판정] 현재 ISR의 복제 확인 후 리더가 Producer에 ACK 반환
        │
   컨슈머 그룹이 최신 High Watermark 오프셋을 읽어 비즈니스 로직을 병렬 소비
```

#### 한줄 요약
- ACK를 리더 기록 시점에 돌려줄지 ISR 복제 완료까지 기다릴지가 이 경로의 유일한 조절 지점이므로, 발행 지연을 줄이는 선택과 장애 시 유실을 없애는 선택이 여기서 갈린다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **RabbitMQ vs Kafka**: 메시지 수신 즉시 삭제되는 전통 큐(RabbitMQ)와 디스크에 영속 보존되는 이벤트 스트림(Kafka).

</details>

| 비교 항목 | 전통적 메시지 큐 (RabbitMQ) | 이벤트 스트리밍 플랫폼 (Apache Kafka) |
|:---|:---|:---|
| 메시지 수명주기 | 확인·보존 정책에 따른 큐 제거 | 보존 정책과 무관한 소비 오프셋 |
| 다중 구독 모델 | 큐·Exchange 기반 라우팅 | 그룹별 독립 오프셋 |
| 과거 데이터 재생 | 큐 유형과 보존 정책에 의존 | 보존 범위에서 오프셋 재설정 |
| 처리 특성 | 메시지 라우팅·작업 분배 | 파티션 순차 로그·스트림 재생 |

#### 한줄 요약
- 단순 작업 분배 큐는 RabbitMQ, 이벤트 영속 보존과 대규모 스트리밍 처리는 Kafka를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Rebalance Storm**: 컨슈머 추가/장애 시 파티션 재할당(Rebalance)으로 인해 전체 컨슈머의 읽기가 일시 중단되는 락업 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 처리 지연에 따른 Consumer Lag 증가 | 파티션과 컨슈머 처리량 함께 조정 | 지연과 병렬도 균형 조정 |
| 컨슈머 변경에 따른 리밸런싱 중단 | 협력적 리밸런싱 적용 | 파티션 이동 중 중단 범위 축소 |
| 재시도에 따른 메시지 중복 처리 | 프로듀서·컨슈머 멱등성 구현 | 중복 처리 영향 제한 |
| 브로커 장애의 메시지 유실 위험 | acks·min ISR·복제 계수 함께 설정 | 내구성과 쓰기 가용성 절충 |

#### 한줄 요약
- 파티션/컨슈머 증설, 협력적 리밸런싱, 멱등성 설정, acks=all로 안정성을 보장한다.

## Ⅶ. 결론

- 현대 이벤트 주도 아키텍처(EDA), 실시간 데이터 파이프라인 및 분산 메시징의 **글로벌 백본(Backbone) 플랫폼**으로 확립되었으며, 엔터프라이즈 운영 시에는 **데이터 유실 0을 보장하는 `acks=all` 및 `min.insync.replicas=2` 설정, 파티션별 순서 보장과 멱등성(Idempotent Producer) 활성화, 컨슈머 리밸런싱 중단을 최소화하는 협력적 스티키(Cooperative Sticky) 프로토콜 및 실시간 Consumer Lag 모니터링**을 결합하여 고가용성과 데이터 완결성을 동시 확보

#### 한줄 요약
- Apache Kafka는 디스크 순차 로그와 Zero-Copy 전송을 기반으로 초고성능 이벤트 스트리밍과 메시지 재생을 실현하는 현대 분산 데이터 인프라의 핵심 플랫폼이다.
