---
title: 145. 메시지 브로커 (Message Broker) - 동기·비동기 통합
date: '2026-04-19'
tags:
- studynote-enterprise-systems
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[389_mesh_topology|메시]]지 브로커는 **생산자와 소비자 사이에서 [[389_mesh_topology|메시]]지를 중계([[339_routing_overview_best_path_selection|라우팅]]·[[454_buffering|버퍼링]]·변환)**하여 비동기·느슨 결합 통신을 가능하게 하는 미들웨어이며, RabbitMQ·ActiveMQ·Kafka가 대표이다.
> 2. **가치**: 동기([[156_rest_representational_state_transfer|REST]])는 **수신자 장애 시 전체 실패**하지만, [[389_mesh_topology|메시]]지 브로커는 **큐에 저장 후 비동기 처리**하여 장애 격리·피크 완화·순서 보장을 제공한다.
> 3. **판단 포인트**: RabbitMQ(전통 MQ, AMQP)·[[179_kafka_flink_watermark_time_window|Kafka]]([[136_variance|분산]] [[568_logs_distributed_logging_elk_fluentd|로그]], 대용량)·SQS(AWS 관리형)를 워크로드에 맞게 선택한다.

---

## Ⅰ. 개요 및 필요성

```text
동기: A→B (B 장애 시 A도 실패)
비동기: A→Queue→B (B 장애 시 Queue에 보관)
패턴: Point-to-Point(1:1) | Pub/Sub(1:N)
RabbitMQ: 전통 MQ (AMQP, 복잡 라우팅)
Kafka: 분산 로그 (대용량, 순서 보장)
```

- **📢 섹션 요약 비유**: [[389_mesh_topology|메시]]지 브로커는 **우체국**이다. 편지([[389_mesh_topology|메시]]지)를 맡기면 우체국이 상대방에게 배달한다.

---

## Ⅱ~Ⅴ. 결론

[[389_mesh_topology|메시]]지 브로커는 **비동기 통합의 핵심 인프라**이며, [[179_kafka_flink_watermark_time_window|Kafka]](대용량)와 RabbitMQ(복잡 [[339_routing_overview_best_path_selection|라우팅]])를 상황에 맞게 선택한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[389_mesh_topology|메시]]지 브로커** | 중계 미들웨어 |
| **RabbitMQ** | AMQP (전통 MQ) |
| **[[179_kafka_flink_watermark_time_window|Kafka]]** | [[136_variance|분산]] [[568_logs_distributed_logging_elk_fluentd|로그]] |
| **Pub/Sub** | 발행/구독 |
| **Dead Letter** | 처리 실패 [[389_mesh_topology|메시]]지 |

### 📈 관련 키워드 및 발전 흐름도

```text
[IBM MQ (1990s)] → [JMS (Java, 2001)]
    → [RabbitMQ (2007, AMQP)]
    → [Kafka (2011, 분산 로그)]
    → [현재: Pulsar·RedPanda — Kafka 대안]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[389_mesh_topology|메시]]지 브로커는 **우체국**이에요. 편지([[389_mesh_topology|메시]]지)를 맡기면 **대신 배달**해요.
2. 상대방이 부재(장애)여도 **우체국이 보관**했다가 나중에 전달해요.
3. Kafka는 **대형 택배 센터**, RabbitMQ는 **동네 우체국**이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 145 / 482

← **이전**: [[144_hub_and_spoke_architecture_eai|144. Hub-and-Spoke 아키텍처 심화 - EAI 중앙 통합]]
**다음**: [[146_esb_enterprise_service_bus_architecture|146. ESB (Enterprise Service Bus) - 엔터프라이즈 서비스 버스]] →

---
