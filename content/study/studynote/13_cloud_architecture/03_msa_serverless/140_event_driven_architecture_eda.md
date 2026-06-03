+++
weight = 140
title = "140. EDA (Event-Driven Architecture) - 이벤트 기반 아키텍처"
date = "2026-04-19"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: EDA는 **이벤트(상태 변화 알림)를 중심으로 [[090_service_kubernetes_network_load_balancing|서비스]] 간 통신을 설계**하는 아키텍처이며, 이벤트 생산자→이벤트 브로커([[179_kafka_flink_watermark_time_window|Kafka]])→이벤트 소비자의 비동기·느슨 결합 구조이다.
> 2. **가치**: 동기 호출([[156_rest_representational_state_transfer|REST]])은 호출자가 **응답까지 블로킹**되고 [[090_service_kubernetes_network_load_balancing|서비스]] 간 강결합이지만, EDA는 **비동기·느슨 결합**으로 확장성·탄력성이 높다.
> 3. **판단 포인트**: Event Notification(알림)·Event-Carried [[272_state_pattern|State]] Transfer(상태 전달)·[[307_event_sourcing|Event Sourcing]](이벤트 저장) 3가지 패턴을 구분하며, [[179_kafka_flink_watermark_time_window|Kafka]]·EventBridge·SNS/SQS가 핵심 인프라이다.

---

## Ⅰ. 개요 및 필요성

```text
동기 (REST): A→B→C (체이닝, 블로킹)
비동기 (EDA): A→이벤트→Kafka→B, C (독립 소비, 비블로킹)
  → 생산자·소비자 독립 → 느슨 결합 → 확장성↑
```

- **📢 섹션 요약 비유**: REST는 전화(응답 대기), EDA는 **게시판(올리면 관심있는 사람이 봄)**이다.

---

## Ⅱ~Ⅴ. 결론

EDA는 **MSA의 느슨 결합·확장성을 실현하는 핵심 아키텍처**이며, Kafka가 이벤트 브로커의 사실상 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[064_eda|EDA]]** | [[538_event_driven_architecture_eda|이벤트 기반 아키텍처]] |
| **[[179_kafka_flink_watermark_time_window|Kafka]]** | 이벤트 브로커 |
| **Pub/Sub** | 발행/구독 패턴 |
| **[[307_event_sourcing|Event Sourcing]]** | [[064_eda|EDA]] 고급 패턴 |
| **[[306_cqrs|CQRS]]** | EDA와 결합 |

### 📈 관련 키워드 및 발전 흐름도

```text
[동기 RPC (2000s)] → [메시지 큐 (RabbitMQ, 2007)]
    → [Kafka (2011, 대용량 이벤트)]
    → [EDA + MSA (2016~)]
    → [현재: EventBridge·Eventarc — 서버리스 EDA]
```

### 👶 어린이를 위한 3줄 비유 설명
1. EDA는 **게시판**이에요. 소식(이벤트)을 올리면 **관심있는 사람이 봐요**.
2. 전화([[156_rest_representational_state_transfer|REST]])처럼 **기다리지 않아도** 돼서 빨라요.
3. 새 소식을 **여러 사람이 동시에** 볼 수 있어서 효율적이에요!
