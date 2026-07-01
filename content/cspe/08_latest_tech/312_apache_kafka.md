---
title: "Apache Kafka 이벤트 스트리밍 (Apache Kafka)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 312
---

# 📖 【암기용】 개념 완전 이해

> 목적: Apache Kafka를 메시지를 단순 전달하는 큐가 아니라 이벤트를 partitioned log로 저장하고 여러 소비자가 재처리할 수 있게 하는 이벤트 스트리밍 플랫폼으로 이해하게 만든다.

## 한눈에
- **개요**: topic partition에 이벤트를 순서대로 기록하고 consumer group이 offset으로 읽는 분산 로그 플랫폼
- **왜 필요한가**: 서비스 간 직접 호출과 일회성 큐만으로는 이벤트 재처리, fan-out, 장애 격리, 실시간 파이프라인 구성이 어렵다.
- **핵심 직관**: 여러 팀이 같은 CCTV 녹화본을 각자 필요한 시점부터 다시 볼 수 있게 저장하는 공용 이벤트 장부임.

## 깊이 이해
- **배경·문제의식**: MSA와 데이터 파이프라인은 주문, 결제, 배송 같은 이벤트를 여러 시스템이 서로 다른 속도로 소비해야 한다.
- **작동 원리**: Producer가 topic partition에 record를 append하고 broker가 복제하며, consumer group은 partition별 offset을 commit해 처리 위치를 관리한다.
- **비유**: 기차역 전광판이 아니라 시간순 운행 기록부에 가깝다. 승객마다 필요한 노선을 보고, 놓친 기록도 보존 기간 내 다시 확인할 수 있다.
- **구체 예시**: 주문 이벤트 topic을 결제, 재고, 추천, lakehouse 적재 consumer group이 각각 독립 offset으로 읽어 서로 다른 처리를 수행한다.
- **흔한 오해·주의점**: Kafka의 순서 보장은 topic 전체가 아니라 partition 내부 순서다. key 설계가 잘못되면 같은 주문의 이벤트 순서가 보장되지 않는다.

## 연결 개념
- Consumer Group — 병렬 소비와 offset 관리 단위
- Exactly-Once Semantics — idempotent producer와 transaction 기반 보장
- Kafka Connect — 외부 시스템과 source/sink 연동

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Kafka는 topic-partition-offset 모델과 replication, consumer group, retention, transaction을 중심으로 답해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Apache Kafka는 이벤트를 topic partition의 append-only log로 저장하고 consumer가 offset 기반으로 읽는 분산 스트리밍 플랫폼임.
> 2. **가치**: 이벤트 fan-out, 재처리, 서비스 결합도 완화, CDC·streaming pipeline의 durable buffer를 제공함.
> 3. **판단 포인트**: partition key, replication factor, retention, consumer lag, idempotent producer, transaction 설정이 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Kafka 구조 이해 확인 | topic, partition, broker, offset, consumer group | 일반 MQ와 동일시 |
| 운영 설계 판단 확인 | partition 전략, replication, retention, lag | partition 수만 늘리면 해결로 단정 |
| 보장 수준 확인 | at-least-once, idempotence, transaction | exactly-once를 무조건 보장으로 표현 |

> 요약: 이 문제는 Kafka를 분산 로그와 소비 위치 관리 모델로 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 분산 이벤트 로그 플랫폼
- 배경: MSA와 데이터 파이프라인은 동일 이벤트를 여러 소비자가 독립 속도로 읽고 재처리해야 함.
- 필요성: durable log, consumer group, offset, replication으로 장애 격리와 이벤트 재처리를 지원해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Producer -> Topic / Partition -> Broker Cluster / Replication
        +-> Consumer Group / Offset
        +-> Kafka Connect / Streams / Schema Registry
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Producer | key, value, header, timestamp를 record로 발행 | idempotence 설정 |
| Topic/Partition | 이벤트 저장과 병렬 처리 단위 | partition 내 순서 보장 |
| Broker Cluster | partition 저장·복제·leader 관리 | replication factor |
| Consumer Group | partition을 나눠 읽고 offset commit | rebalance 발생 |

> 요약: Kafka는 topic partition을 중심으로 저장·순서·병렬성·소비 위치를 관리한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
record 발행 -> partition 선택 -> leader broker append
-> follower replication -> consumer poll -> 처리 후 offset commit
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | producer가 key 기반 partition 선택 | key distribution |
| 2 | leader broker가 log에 record append | ack, ISR |
| 3 | consumer group이 partition assignment 수행 | rebalance log |
| 4 | 처리 완료 후 offset commit과 lag 측정 | committed offset |

> 요약: Kafka는 append log와 offset commit을 분리해 이벤트 보존과 소비 진행 상태를 독립 관리한다.

---

## Ⅳ. 특징

| 구분 | 전통 MQ | Apache Kafka | 판단 기준 |
|:---|:---|:---|:---|
| 저장 모델 | 소비 후 제거 중심 | retention 기반 log 보존 | 재처리 필요성 |
| 소비 방식 | queue consumer | consumer group별 offset | fan-out 요구 |
| 순서 보장 | queue 단위 | partition 내부 | key 설계 |
| 확장 단위 | broker/queue | partition 병렬성 | 처리량 목표 |

> 요약: Kafka는 메시지 전달보다 이벤트 로그 보존과 독립 소비를 중시하는 플랫폼이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 통신 방식 | REST 동기 호출 | event-driven async | 결합도·장애 격리 |
| 데이터 이동 | 배치 ETL | CDC/streaming ingest | 지연 SLA |
| 처리 보장 | at-most/at-least | idempotence+transaction 가능 | 중복 허용 여부 |

> 요약: Kafka는 이벤트 재사용과 durable buffer가 필요한 경우 적합하며, 단순 요청·응답에는 REST/gRPC가 더 단순하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| consumer lag 증가 | 처리량 부족·hot partition | partition key 조정, consumer scale-out | lag by partition |
| 순서 깨짐 | key 없는 round-robin 발행 | 업무 entity key 고정 | out-of-order count |
| 저장소 압박 | retention·compaction 정책 부재 | retention.ms/bytes, log compaction | disk usage |

> 요약: Kafka 운영 리스크는 lag, key 설계, retention 정책으로 관리한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 가용성 | replication factor와 ISR 정책 준수 | broker metric |
| 지연 | produce-consume p95 SLA 충족 | client metric |
| 소비 안정 | rebalance 빈도 통제 | consumer group log |

> 요약: Kafka 성과는 topic 수보다 lag, p95 지연, ISR 상태, rebalance 빈도로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 업무 entity 기준 partition key를 정하고 partition 수, replication factor, retention 정책을 topic별로 문서화함.
2. producer는 idempotence와 acks 설정을 검토하고, 소비자는 처리 완료 후 offset commit과 retry/DLQ 정책을 분리함.
3. consumer lag, under-replicated partition, broker disk, rebalance count를 운영 dashboard와 alert에 연결함.

**결론 (2줄):**
- 기술사 판단: 이벤트 fan-out과 재처리가 필요한 플랫폼은 Kafka가 적합하고, 단순 명령 전달은 일반 MQ나 동기 API가 운영 복잡도를 줄임.
- 향후 방향: Kafka는 CDC, stream processing, lakehouse ingestion, event-driven MSA의 중심 로그 계층으로 계속 사용됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Apache Kafka를 설명하시오" | publish, replication, consume, offset 흐름 | MQ 대비 차이 |
| 요구사항 명시형 | "이벤트 기반 아키텍처를 설계하시오" | partition key, consumer group, retention 설계 | lag·순서·저장소 리스크 |

> 요약: 설명형은 분산 로그 모델을, 설계형은 key·partition·offset 운영을 중심으로 작성한다.
