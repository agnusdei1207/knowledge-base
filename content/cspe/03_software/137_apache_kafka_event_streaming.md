---
title: "Apache Kafka 이벤트 스트리밍 (Apache Kafka)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 137
---

# 📖 【암기용】 개념 완전 이해

> 목적: Kafka가 왜 "사라지는 메시지 큐"가 아니라 "다시 읽을 수 있는 로그"인지, 내부 용어를 이해하게 만든다.

## 한눈에
- **개요**: Apache Kafka는 이벤트를 **topic의 partition**에 **append-only log**로 저장하고, 여러 consumer가 각자 독립된 위치(offset)에서 읽을 수 있게 하는 **분산 이벤트 스트리밍 플랫폼**이다.
- **왜 필요한가**: 전통적인 메시지 큐는 소비되면 메시지가 사라지는 모델이 많아, 같은 이벤트를 여러 시스템이 각자 다른 속도로 재사용·재처리하기 어렵다. MSA·CDC·실시간 분석은 "한 번 발생한 이벤트를 여러 팀이 서로 다른 시점에 반복해서 읽는" 요구가 흔하다.
- **핵심 직관**: 여러 계산대의 영수증이 시간순으로 파일(로그)에 계속 쌓이고, 회계팀·마케팅팀·감사팀이 각자 자기가 읽은 위치(offset)를 따로 표시해두며 원하는 시점부터 다시 읽는 구조다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 분산 이벤트 스트리밍 플랫폼 | 이벤트를 지속 저장하고 여러 소비자가 재사용하도록 중계하는 상위 범주 | 방송국의 시간순 녹화·재생 시스템 |
| topic | 같은 종류의 이벤트를 모으는 논리적 채널(이름) | 방송 채널 이름 |
| partition | topic을 병렬 처리 단위로 나눈 물리적 하위 로그. partition 내부는 순서 보장 | 채널 안의 개별 녹화 테이프 |
| offset | partition 안에서 각 레코드의 순번(위치) | 테이프의 재생 시간 지점 |
| producer | 이벤트(record)를 topic에 발행하는 클라이언트 | 계산대에서 영수증을 발행하는 직원 |
| consumer | topic에서 이벤트를 읽는 클라이언트 | 영수증철을 읽는 담당자 |
| consumer group | 여러 consumer가 partition을 나눠 병렬로 읽는 논리적 묶음. group당 partition 하나는 consumer 1개만 담당 | 부서별로 구역을 나눠 담당 |
| broker | 실제 partition 데이터를 저장·서빙하는 Kafka 서버 | 방송국의 개별 송출국 |
| replication / ISR | partition을 여러 broker에 복제(기본 3개)하고, 그중 최신 상태를 따라가는 복제본 집합(In-Sync Replica) | 원본 테이프의 백업본들 |
| leader / follower | partition마다 쓰기를 담당하는 broker(leader)와 그 복제를 받는 broker(follower) | 원본 담당자와 백업 담당자 |
| retention | 이벤트를 얼마나 오래(또는 얼마나 많이) 보관할지 정하는 정책(기간·용량 기준) | 녹화본 보관 기한 |
| exactly-once semantics | producer의 idempotence(중복 전송 무시)와 transaction으로 "정확히 한 번만 처리됨"을 보장하는 기능 | 같은 주문을 두 번 접수하지 않도록 확인하는 절차 |

## 깊이 이해

### 왜 Kafka가 "메시지 큐"와 다른가 (배경)
전통적 메시지 큐(RabbitMQ 등)는 "소비하면 사라지는" point-to-point 모델이 기본이라, 한 메시지를 여러 시스템이 각자 재사용하려면 큐를 여러 개 복제해야 했다. Kafka(2011년 LinkedIn에서 개발)는 메시지를 소비해도 지우지 않고 retention 기간 동안 로그에 그대로 남긴다. 그 결과 "발행은 한 번, 구독은 여러 팀이 각자 원하는 시점부터"가 가능해졌다 — 이것이 메시지 큐가 아니라 "분산 커밋 로그"로 불리는 이유다.

### partition과 순서 보장 — key 설계 수치 예제
주문 이벤트를 담는 topic을 12개 partition으로 만들고, producer가 `order_id`를 key로 사용한다고 하자. Kafka는 `partition = hash(key) % 12` 방식으로 partition을 정하므로, 같은 `order_id`를 가진 이벤트(주문 생성→결제→배송)는 항상 같은 partition에 들어가고, 그 partition 안에서는 발행 순서대로 저장·소비된다. 하지만 Kafka는 topic 전체의 순서는 보장하지 않는다 — 12개 partition에 걸쳐 있는 서로 다른 주문끼리는 어느 것이 먼저 처리될지 순서가 섞일 수 있다. key를 잘못 설계하면(예: 모든 이벤트에 같은 key를 써서 1개 partition에만 몰림) 병렬성이 사라지고 특정 partition에 부하가 집중된다.

### replication과 내구성 — ISR 수치 예제
partition의 replication factor를 3으로 설정하면, 하나의 leader broker와 2개의 follower broker가 같은 데이터를 갖는다. `min.insync.replicas=2`, `acks=all`로 설정하면, producer는 leader를 포함해 최소 2개 broker(ISR 내)에 데이터가 쓰였다는 응답을 받아야 "성공"으로 간주한다. 이 상태에서 broker 1대가 죽어도 나머지 2대 중 1대가 leader로 승격되어 데이터 유실 없이 서비스가 계속된다. 반대로 `acks=1`(leader만 확인)로 설정하면 leader가 응답 직후 죽었을 때 follower에 아직 복제되지 않은 데이터가 유실될 수 있다.

### consumer group과 병렬 소비 — 수치 예제
12개 partition을 가진 topic을 consumer 5개로 구성된 group이 읽는다면, Kafka는 partition을 consumer들에게 최대한 고르게 분배한다(예: 3개 consumer가 partition 2개씩, 2개 consumer가 partition 3개씩, 합계 12개). 초당 12,000건이 유입되는 topic이라면 partition당 평균 1,000건/초이므로, 각 consumer는 자신이 담당한 partition 수만큼(2,000건/초 또는 3,000건/초)을 처리해야 한다. consumer 수를 partition 수보다 늘려도(예: consumer 13개) 13번째 consumer는 담당할 partition이 없어 유휴 상태가 된다 — **partition 수가 consumer 병렬성의 상한**이다.

### 흔한 오해
"Kafka는 topic 전체의 순서를 보장한다"는 오해가 가장 흔하다. 순서는 partition 내부에서만 보장되며, 전체 순서가 필요하면 partition을 1개로 제한해야 하는데 그러면 병렬성을 포기하게 된다. 또한 "Kafka는 메시지가 영구 보존된다"는 것도 오해다 — retention 정책(기간 또는 용량)을 지나면 오래된 세그먼트는 삭제되거나, compaction 설정 시 key별 최신 값만 남긴다.

## 연결 개념
- Kappa Architecture — Kafka의 durable log와 replay를 기반으로 하는 상위 아키텍처(136)
- Lambda Architecture — batch·speed 양쪽이 공유하는 원천 로그로 Kafka를 사용(135)
- Kafka Connect·Schema Registry — CDC 연계·스키마 호환성을 다루는 주변 생태계

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
