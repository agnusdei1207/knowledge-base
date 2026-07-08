---
title: "Apache Kafka 이벤트 스트리밍 (Apache Kafka)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 312
extra:
  question_no: "312"
  exam_status: "기출"
  exam_history: "124회, 136회"
---

## 미리 알고가기

- Apache Kafka는 분산 로그 기반 이벤트 스트리밍 플랫폼임
- topic과 partition과 consumer group과 offset이 기본 운영 단위임
- 메시지 큐처럼 쓰일 수 있지만 핵심은 durable log와 reprocessing capability에 있음

## Ⅰ. 개요

- **정의/개념**: Apache Kafka는 대규모 이벤트를 분산 로그 형태로 저장하고 생산자와 소비자가 느슨하게 결합된 상태에서 고처리량으로 발행과 구독과 재처리를 수행하게 하는 이벤트 스트리밍 플랫폼임
- **배경/필요성**: 서비스 간 동기 호출이 늘고 로그와 이벤트 데이터가 폭증하면서 높은 처리량과 내구성과 재처리 기능을 갖춘 중앙 이벤트 백본이 필요해짐

## Ⅱ. 특징

- append only 로그 구조를 사용해 메시지 보관과 재처리에 강함
- partition 기반 수평 확장이 가능해 대량 이벤트 처리에 적합함
- consumer group 모델로 병렬 소비와 장애 전환을 유연하게 지원함
- key 분포와 partition 설계가 잘못되면 처리 균형과 순서 보장이 동시에 흔들릴 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Apache Kafka | RabbitMQ | Apache Pulsar |
|:---|:---|:---|:---|
| 핵심 구조 | 분산 로그 | 메시지 큐 | 세그먼트 분리형 로그 |
| 강점 | 고처리량과 재처리 | 복잡한 라우팅 | 멀티테넌시와 tiered storage |
| 순서 보장 | partition 내부 | queue 단위 | topic partition 단위 |
| 대표 용도 | 이벤트 백본, 스트리밍 | 작업 큐 | 대규모 메시징과 스트림 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Producer | 애플리케이션이 key와 topic 기준으로 이벤트를 발행해 Kafka 로그에 데이터를 적재하는 입력 계층임 |
| Topic and Partition | 이벤트를 논리적 주제와 물리적 분할로 관리해 확장성과 부분 순서 보장을 동시에 제공하는 저장 구조임 |
| Broker Cluster | 파티션 리더와 복제본을 운영해 내구성과 가용성을 보장하는 분산 서버 계층임 |
| Consumer Group | 여러 소비자가 같은 그룹 내에서 파티션을 분담해 병렬 처리와 장애 전환을 수행하는 소비 구조임 |
| Offset and Retention Control | 읽은 위치와 보관 기간을 관리해 재처리와 장애 복구와 비용 제어의 기준점을 제공하는 운영 계층임 |

```text
+-----------+    +-----------+    +-----------+    +-----------+
| Producers | -> | Topic /   | -> | Brokers   | -> | Consumers |
|           |    | Partitions|    | Cluster   |    | Group     |
+-----------+    +-----------+    +-----------+    +-----------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 이벤트 발행   | -> | 파티션 기록   | -> | 복제 동기화   | -> | 소비자 fetch  | -> | offset 반영   |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **이벤트 발행**: producer가 topic과 key를 지정해 레코드를 전송함
2. **파티션 기록**: broker 리더가 레코드를 append only 로그에 기록함
3. **복제 동기화**: follower가 복제해 장애 시 복구 기반을 마련함
4. **소비자 fetch**: consumer가 partition 로그를 읽어 처리함
5. **offset 반영**: 처리 위치를 저장해 재시작과 재처리 기준으로 사용함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 특정 key에 이벤트가 편중되면 일부 partition만 과부하되어 전체 처리량과 지연이 함께 악화될 수 있음
   - 해결방안: key distribution review와 adaptive partition strategy를 적용하고 partition skew ratio와 hottest partition lag로 검증함
2. 문제: 보관 기간과 압축 정책을 잘못 설정하면 재처리 가능 범위가 부족하거나 스토리지 비용이 급격히 증가할 수 있음
   - 해결방안: retention tiering policy와 topic lifecycle governance를 적용하고 replayable retention window와 storage cost per topic로 검증함
3. 문제: 파티션을 넘는 글로벌 순서를 기대하면 소비 로직에서 비즈니스 정합성 오류가 반복될 수 있음
   - 해결방안: ordering scope design과 key based sequencing rule을 적용하고 cross partition ordering defect count와 ordering assumption violation rate로 검증함

## Ⅶ. 적용 사례

- 대용량 이벤트 백본이 key 분포 검토를 운영하며 확인 지표는 partition skew ratio와 hottest partition lag임
- 플랫폼 운영팀이 토픽 수명주기 정책을 적용하며 확인 지표는 replayable retention window와 storage cost per topic임
- 주문 처리 서비스가 순서 범위 설계를 명확히 하며 확인 지표는 cross partition ordering defect count와 ordering assumption violation rate임

## Ⅷ. 결론

Apache Kafka는 메시지 전달보다 로그 보관과 재처리 가치가 큰 플랫폼이므로 partition 설계와 retention 정책이 아키텍처 품질을 좌우함.
