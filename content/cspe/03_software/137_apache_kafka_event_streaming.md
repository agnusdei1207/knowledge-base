---
title: "Apache Kafka 이벤트 스트리밍 (Apache Kafka)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 137
---

# 📖 【암기용】 개념 완전 이해

> 목적: Kafka가 메시지 큐와 다른 event log 플랫폼인 이유를 이해하게 만든다.

## 한눈에
- **개요**: 이벤트를 topic partition에 append-only log로 저장하고 여러 consumer가 독립적으로 읽는 분산 스트리밍 플랫폼
- **왜 필요한가**: MSA·로그·CDC·실시간 분석에서 시스템 간 직접 호출을 줄이고, 이벤트를 재사용·재처리할 수 있어야 함.
- **핵심 직관**: 방송국이 시간순 녹화본을 보관하고, 각 부서가 필요한 시점부터 다시 보는 구조임.

## 깊이 이해
- **배경·문제의식**: 전통 큐는 메시지를 소비하면 사라지는 모델이 많아 재처리와 다중 구독이 어렵다. Kafka는 partition log와 offset으로 이벤트 보존과 소비 위치를 분리함.
- **작동 원리**: producer가 key 기준으로 partition에 record를 append함. broker는 replication으로 leader/follower를 유지하고, consumer group은 partition을 나눠 읽으며 offset을 commit함.
- **비유**: 여러 계산대 영수증이 시간순 파일에 쌓이고, 회계팀·마케팅팀·감사팀이 각자 읽은 위치를 따로 표시함.
- **구체 예시**: 주문 topic을 12 partition으로 만들고 `order_id` key를 사용하면 같은 주문의 이벤트 순서는 partition 내에서 보장됨.
- **흔한 오해·주의점**: Kafka는 전체 topic 순서를 보장하지 않음. 순서는 partition 내부에서만 보장되며, key 설계가 잘못되면 순서·부하 분산 문제가 발생함.

## 연결 개념
- Exactly-Once Semantics — producer idempotence와 transaction
- Kafka Connect — CDC·외부 시스템 연계
- Kappa Architecture — durable log 기반 처리

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: Kafka 문제에서 topic/partition/offset/consumer group과 운영 지표를 연결해 답안화함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Kafka는 topic partition에 이벤트를 지속 저장하고 consumer group별 offset으로 독립 소비를 지원하는 event streaming platform임.
> 2. **가치**: decoupling, replay, fan-out, backpressure 흡수로 MSA·CDC·실시간 분석의 이벤트 허브 역할을 수행함.
> 3. **판단 포인트**: partition key, replication factor, retention, consumer lag, exactly-once 요구를 업무별로 설계해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 이벤트 스트리밍 구조 이해 확인 | topic, partition, broker, offset, consumer group | Kafka를 단순 MQ로만 설명 |
| 분산 처리 판단 확인 | partition 병렬성, replication, retention | 전체 순서 보장으로 오해 |
| 운영 리스크 확인 | lag, rebalance, ISR, 데이터 유실 | acks·min.insync.replicas 누락 |

> 요약: Kafka 답안은 log 저장 모델과 consumer offset 독립성을 중심으로 구조·운영 지표를 써야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: Kafka는 분산 이벤트 스트리밍 플랫폼임.
- 배경: 시스템 간 직접 연동은 장애 전파와 결합도를 키우고 큐 기반 메시징은 재처리와 다중 구독에 제약이 있음.
- 필요성: durable log, partition 병렬성, consumer group 모델로 실시간 데이터 흐름을 중계함.

---

## Ⅱ. 구조 및 구성요소

```text
Producer -> Topic Partition -> Broker Leader -> Follower Replica
                              / Consumer Group -> Offset Commit
                              / Schema Registry -> Stream Processor
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Producer | record 발행 | key, acks, idempotence 설정 |
| Topic/Partition | 이벤트 저장 단위 | partition 내부 순서 보장 |
| Broker/Replica | log 저장·복제 | ISR, replication factor 3 |
| Consumer Group | 병렬 소비 | group당 partition owner 1개 |
| Offset | 소비 위치 관리 | commit 정책이 재처리 범위 결정 |

> 요약: Kafka는 partition log에 이벤트를 저장하고 consumer group이 offset을 관리해 병렬 소비와 replay를 지원함.

---

## Ⅲ. 동작원리 및 흐름도

```text
record 생성 -> key 기반 partition 선택 -> leader append
-> follower replication -> consumer poll -> offset commit -> downstream 처리
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | producer가 key와 value 전송 | serialization, schema version |
| 2 | partition leader에 append | acks=all, batch size |
| 3 | follower가 ISR 내 복제 | min.insync.replicas 2 이상 |
| 4 | consumer가 poll 후 offset commit | consumer lag, rebalance 횟수 |

> 요약: Kafka는 leader append와 ISR 복제로 내구성을 확보하고, consumer offset으로 처리 위치를 분리함.

---

## Ⅳ. 특징

| 구분 | 전통 메시지 큐 | Apache Kafka | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 저장 모델 | consume 후 삭제 중심 | retention 기반 log 보존 | 7일 또는 size 기반 |
| 소비 모델 | 큐당 소비자 | consumer group fan-out | group별 offset 독립 |
| 순서 | 큐 단위 순서 | partition 내부 순서 | key 설계 필수 |
| 내구성 | broker 설정 의존 | replication+ISR | RF 3, min ISR 2 |

> 요약: Kafka는 메시지 전달보다 이벤트 보존·재처리·다중 소비에 초점을 둔 streaming backbone임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | MQ point-to-point | partitioned log | 다중 소비와 replay 요구 |
| 비용/성능 | 낮은 운영 복잡도 | broker cluster 운영 | 초당 10만건 이상 이벤트 |
| 운영/위험 | 메시지 유실 관리 | lag·ISR·rebalance 관리 | 24x7 관측성 필요 |

> 요약: Kafka는 이벤트가 여러 시스템에 재사용될 때 선택하고, 단순 작업 큐는 RabbitMQ·SQS 계열도 검토함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 데이터 유실 | acks=1, ISR 부족 | acks=all, min.insync.replicas=2 | under-replicated partition 0 |
| 처리 지연 | consumer 처리량 부족 | partition 증설, batch 처리 | consumer lag 1000건 이하 |
| rebalance 폭증 | consumer 장애·timeout | static membership, session timeout 조정 | rebalance count |

> 요약: Kafka 운영은 유실, lag, rebalance를 핵심 리스크로 두고 broker·consumer 지표를 함께 본다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 가용성 | ISR shrink 0건 | Kafka metrics |
| 처리량 | topic별 ingress/egress 목표 충족 | broker JMX, Prometheus |
| 스키마 품질 | backward compatibility 100% | Schema Registry check |

> 요약: Kafka 도입 효과는 replica 상태, 처리량, schema compatibility로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 업무 entity 기준 key를 정의하고 partition 수는 목표 처리량과 consumer 병렬도 기준으로 산정함
2. 중요 이벤트는 RF 3, acks=all, min.insync.replicas=2, idempotent producer를 기본값으로 설정함
3. Schema Registry와 DLQ topic을 두고 schema 호환성 실패·역직렬화 오류를 분리 처리함

**결론 (2줄):**
- 기술사 판단: 이벤트 replay와 fan-out이 필요하면 Kafka, 단순 command queue면 관리형 MQ를 선택함
- 향후 방향: Kafka는 CDC, stream processing, data lake ingestion을 연결하는 실시간 데이터 허브로 확장됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Kafka를 설명하시오" | produce, append, replicate, consume 흐름 | MQ 대비 log 기반 특징 |
| 요구사항 명시형 | "설계하시오", "운영 방안을 제시하시오" | partition key, ISR, offset, lag | 유실 방지, replay, schema governance |

> 요약: 설명형은 구조 원리, 설계형은 partition·복제·운영 지표 중심으로 답안화함.
