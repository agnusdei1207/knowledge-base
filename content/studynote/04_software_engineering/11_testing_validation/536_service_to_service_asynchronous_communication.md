+++
title = "536. 서비스 간 비동기 통신 - 메시지 큐, AMQP"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 서비스 간 비동기 통신(Asynchronous Communication)은 메시지 브로커(Message Broker)를 중개자로 두어 발신자와 수신자가 직접 연결되지 않고 독립적으로 동작하는 느슨한 결합(Loose Coupling) 통신 방식이다.
> 2. **가치**: 생산자 서비스가 소비자 서비스의 가용 여부와 무관하게 메시지를 전송할 수 있어 서비스 간 시간적 결합이 제거되고, 소비자 수를 조정하여 처리량을 독립적으로 확장할 수 있다.
> 3. **판단 포인트**: 멱등성(Idempotency) 보장, 중복 메시지 처리(At-least-once vs Exactly-once), 데드 레터 큐(DLQ) 설계가 반드시 필요하며, 순서 보장이 필요한 경우 파티션 키(Partition Key) 전략을 별도 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

마이크로서비스 아키텍처에서 모든 서비스 간 통신을 동기 방식으로 처리하면 여러 한계가 나타난다. 주문이 완료된 후 결제 처리, 재고 차감, 이메일 발송, 포인트 적립이 모두 동기 호출로 연결되면 하나의 서비스 장애가 전체 흐름을 마비시키고, 모든 처리가 끝날 때까지 주문 API가 응답하지 않아 사용자 경험이 나빠진다.

비동기 통신은 이 문제를 해결한다. 주문 서비스는 "주문 완료" 메시지를 브로커에 발행(Publish)하고 즉시 사용자에게 응답한다. 결제, 재고, 이메일, 포인트 서비스는 각자의 속도로 이 메시지를 구독(Subscribe)하여 처리한다. 각 서비스는 독립적으로 실패하고 재시도할 수 있으며, 서로의 처리 속도에 영향받지 않는다.

메시지 큐(Message Queue) 개념은 1980년대 IBM MQ(당시 MQSeries)에서 시작되어, 오픈소스 AMQP(Advanced Message Queuing Protocol) 표준이 2003년 JPMorgan Chase 주도로 개발되었다. 이를 구현한 RabbitMQ(2007)가 등장하면서 엔터프라이즈 메시지 큐의 표준이 되었고, LinkedIn이 2011년 Kafka를 오픈소스로 공개하면서 대용량 스트림 처리 분야의 새로운 패러다임이 열렸다.

- **📢 섹션 요약 비유**: 편지를 우체통에 넣으면 내가 더 이상 신경 쓰지 않아도 우체국(메시지 브로커)이 배달을 책임진다. 수신자가 집에 없어도 편지는 우편함에 보관되어 나중에 받을 수 있다. 동기 통신은 직접 전화하는 것이고, 비동기는 우편을 보내는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 메시지 브로커 핵심 구성 요소



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">비동기 통신 핵심 구조</div></div>
<div class="kb-diagram-note">생산자 (Producer)</div>
<div class="kb-diagram-note">↓ 메시지 발행 (Publish)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">메시지 브로커 (Broker)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Exchange / Topic</div><div class="kb-diagram-cell">← 라우팅 규칙 결정</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Queue / Partition</div><div class="kb-diagram-cell">← 메시지 저장소</div></div>
<div class="kb-diagram-note">↓ 메시지 구독 (Subscribe)</div>
<div class="kb-diagram-note">소비자 (Consumer)</div>
</div>
</div>



### RabbitMQ와 Kafka 비교

| 비교 항목 | RabbitMQ (AMQP) | Apache Kafka |
|:---|:---|:---|
| 패러다임 | 메시지 큐 (Message Queue) | 이벤트 스트리밍 (Event Streaming) |
| 메시지 처리 | 소비자가 가져가면 삭제 | 파티션에 보존 (설정된 보존 기간) |
| 소비자 모델 | 경쟁 소비자 (Competing Consumers) | 소비자 그룹 (Consumer Groups) |
| 순서 보장 | 큐 단위 순서 보장 | 파티션 단위 순서 보장 |
| 처리량 | 중간 (초당 수만 건) | 높음 (초당 수백만 건) |
| 메시지 크기 | 중소형 권장 | 대용량 가능 |
| 재처리 | 어려움 (이미 소비된 메시지 삭제) | 쉬움 (오프셋 재조정으로 재처리) |
| 적합 사용처 | 작업 큐, RPC 패턴, 복잡한 라우팅 | 로그 수집, 이벤트 소싱, 대용량 스트림 |
| 주요 사용 기업 | 일반 엔터프라이즈, 금융 | Netflix, Uber, LinkedIn |

### AMQP 핵심 개념 (RabbitMQ)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">AMQP 메시지 라우팅 구조</div></div>
<div class="kb-diagram-note">Producer</div>
<div class="kb-diagram-note">↓ "order.created" 라우팅 키로 발행</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Exchange</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Direct/Fanout/Topic)</div></div>
<div class="kb-diagram-note">↓ 바인딩 규칙에 따라</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">결제큐</div><div class="kb-diagram-cell">재고큐</div><div class="kb-diagram-cell">알림큐</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Queue)</div><div class="kb-diagram-cell">(Queue)</div><div class="kb-diagram-cell">(Queue)</div></div>
<div class="kb-diagram-note">결제 서비스 재고 서비스 알림 서비스</div>
</div>
</div>



| Exchange 유형 | 동작 방식 | 사용 예시 |
|:---|:---|:---|
| Direct | 라우팅 키 정확 일치 | 특정 서비스로 직접 전달 |
| Fanout | 모든 바인딩 큐로 브로드캐스트 | 알림 발송 (모든 구독자에게) |
| Topic | 패턴 매칭 라우팅 키 | order.* → 주문 관련 모든 이벤트 |
| Headers | 메시지 헤더 기반 라우팅 | 복잡한 조건부 라우팅 |

### Kafka 핵심 개념



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Kafka 아키텍처</div></div>
<div class="kb-diagram-note">Producer Kafka Cluster Consumer Group</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">주문 서비스 →→→</div><div class="kb-diagram-cell">Topic:</div><div class="kb-diagram-cell">→→→ 결제 서비스 (Consumer 1)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">order-events</div><div class="kb-diagram-cell">→→→ 재고 서비스 (Consumer 2)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Partition 0</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Partition 1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Partition 2</div></div>
<div class="kb-diagram-tree-item" style="--depth:0">같은 파티션 내에서는 순서 보장</div>
<div class="kb-diagram-tree-item" style="--depth:0">파티션 키로 관련 메시지를 같은 파티션으로 라우팅</div>
<div class="kb-diagram-tree-item" style="--depth:0">오프셋(Offset)으로 소비 위치 추적</div>
</div>
</div>



### 메시지 전달 보장 수준

| 보장 수준 | 설명 | 특성 | 적합 상황 |
|:---|:---|:---|:---|
| At-most-once | 최대 한 번 전달 (손실 가능) | 빠름, 중복 없음 | 로그, 통계 (정확도 덜 중요) |
| At-least-once | 최소 한 번 전달 (중복 가능) | 신뢰성, 멱등성 필요 | 대부분의 비즈니스 이벤트 |
| Exactly-once | 정확히 한 번 전달 | 느림, 복잡, 비용 큼 | 금융 거래, 중복 불가 시나리오 |

- **📢 섹션 요약 비유**: 주문서(메시지)를 주방 카운터(브로커/큐)에 올려놓으면, 주방장(소비자)이 여러 명이어도 각자 주문서를 하나씩 가져가서 처리한다. 카운터가 있어서 주방장이 바빠도 주문이 쌓이기만 하고 사라지지 않는다.

---

## Ⅲ. 비교 및 연결

### 비동기 통신 패턴 종류

| 패턴 | 설명 | 구현 방식 |
|:---|:---|:---|
| 발행-구독 (Pub/Sub) | 하나의 메시지를 여러 구독자가 수신 | Kafka Topic, RabbitMQ Fanout |
| 작업 큐 (Work Queue) | 여러 소비자가 경쟁하여 하나씩 처리 | RabbitMQ Queue |
| 요청-응답 (Request-Reply) | 비동기 방식의 요청-응답 | 응답 큐 + Correlation ID |
| 이벤트 소싱 연계 | 상태 변경을 이벤트 스트림으로 발행 | Kafka + Event Sourcing |

### 동기 통신 vs 비동기 통신 선택 기준

| 선택 기준 | 동기 통신 선택 | 비동기 통신 선택 |
|:---|:---|:---|
| 응답 즉시성 | 즉각적 결과 필요 | 나중에 처리 가능 |
| 일관성 요구 | 강한 일관성 필수 | 최종 일관성 허용 |
| 처리 시간 | 수 ms 내 처리 | 수 초 이상 가능 |
| 서비스 가용성 | 대상 서비스 항상 가용 | 대상 서비스 일시 불가 허용 |
| 확장 요구 | 동일 처리량 | 독립적 처리량 확장 필요 |
| 예시 | 재고 확인 후 주문 | 주문 완료 후 이메일 발송 |

### 이벤트 기반 아키텍처(EDA)와의 연결

비동기 통신은 이벤트 기반 아키텍처(Event-Driven Architecture, EDA)의 핵심 구현 수단이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">이벤트 기반 아키텍처 흐름</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">주문 서비스</div></div>
<div class="kb-diagram-note">→ "OrderCreated" 이벤트 발행</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">이벤트 브로커 (Kafka)</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">──</div><div class="kb-diagram-node">결제 서비스</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">"PaymentProcessed" 이벤트 발행</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">──</div><div class="kb-diagram-node">재고 서비스</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">"InventoryReserved" 이벤트 발행</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">──</div><div class="kb-diagram-node">알림 서비스</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">이메일/SMS 발송</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">──</div><div class="kb-diagram-node">포인트 서비스</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">적립금 계산</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: 학교 방송(이벤트)이 나오면 각 교실(서비스)이 자기 할 일을 한다. 방송국(브로커)은 모든 교실에 전달만 하고, 각 교실이 방송에 어떻게 반응하는지는 방송국이 관리하지 않는다. 교실(서비스) 하나가 없어도 방송은 계속된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 비동기 통신 설계 시 필수 고려사항



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">비동기 메시지 처리 안전 설계</div></div>
<div class="kb-diagram-note">1. 멱등성 (Idempotency) 보장</div>
<div class="kb-diagram-tree-item" style="--depth:1">같은 메시지를 여러 번 처리해도 결과가 동일</div>
<div class="kb-diagram-tree-item" style="--depth:1">메시지 ID 기반 중복 처리 방지</div>
<div class="kb-diagram-note">if (processed.contains(messageId)) {</div>
<div class="kb-diagram-note">return; // 이미 처리됨</div>
<div class="kb-diagram-note">}</div>
<div class="kb-diagram-note">2. 데드 레터 큐 (Dead Letter Queue, DLQ)</div>
<div class="kb-diagram-tree-item" style="--depth:1">처리 실패 메시지를 별도 큐에 보관</div>
<div class="kb-diagram-tree-item" style="--depth:1">운영자 확인 및 재처리 가능</div>
<div class="kb-diagram-note">Normal Queue → 3회 실패 → DLQ</div>
<div class="kb-diagram-note">3. 재시도 전략 (Retry with Backoff)</div>
<div class="kb-diagram-tree-item" style="--depth:1">지수 백오프: 1초 → 2초 → 4초 → 8초</div>
<div class="kb-diagram-tree-item" style="--depth:1">무한 재시도 방지 (최대 횟수 제한)</div>
<div class="kb-diagram-note">4. 메시지 순서 보장</div>
<div class="kb-diagram-tree-item" style="--depth:1">순서가 중요한 경우 파티션 키 사용</div>
<div class="kb-diagram-tree-item" style="--depth:1">Kafka: partitionKey = orderId</div>
<div class="kb-diagram-tree-item" style="--depth:1">동일 주문 관련 이벤트 → 같은 파티션</div>
</div>
</div>



### 설계 판단 체크리스트

1. **멱등성 보장**: 소비자 서비스가 동일 메시지를 여러 번 처리해도 부작용이 없는가?
2. **DLQ(Dead Letter Queue) 설계**: 처리 실패 메시지가 별도 큐에 보관되어 운영자가 확인·재처리할 수 있는가?
3. **메시지 순서 보장 전략**: 순서가 중요한 이벤트(주문 생성 → 주문 취소)의 처리 순서를 보장하는가?
4. **메시지 스키마 버전 관리**: 스키마 변경 시 기존 소비자와 하위 호환성을 유지하는가? (Avro, Protobuf, Schema Registry 활용)
5. **브로커 장애 대응**: 메시지 브로커 장애 시 생산자가 메시지를 안전하게 버퍼링하거나 재발행할 수 있는가?
6. **소비자 그룹 확장**: 처리량이 증가할 때 소비자 인스턴스를 동적으로 추가할 수 있는가?
7. **메시지 모니터링**: 큐 깊이(Queue Depth), 소비 지연(Consumer Lag)을 실시간으로 모니터링하는가?

### 안티패턴

- **이벤트 유출 (Event Leakage)**: 내부 구현 세부사항이 이벤트에 노출되어 소비자가 내부 구조에 의존하게 되는 패턴이다. 이벤트는 "무슨 일이 발생했는가"를 기술해야 하며, "어떻게 처리했는가"를 포함해서는 안 된다. 예를 들어 OrderDbUpdated 이벤트 대신 OrderShipped 이벤트를 사용해야 한다.
- **거대한 메시지 (Massive Message)**: 메시지에 수 MB의 데이터를 직접 포함하면 브로커에 부하를 주고 네트워크 비용이 증가한다. 참조 패턴(Reference Pattern)을 사용하여 메시지에는 ID만 담고, 실제 데이터는 저장소에서 조회하도록 설계해야 한다.
- **DLQ 무시**: 데드 레터 큐에 쌓인 실패 메시지를 모니터링하지 않으면, 중요한 비즈니스 이벤트가 조용히 손실된다. DLQ는 반드시 알람 설정과 정기적 처리 절차가 있어야 한다.
- **동기-비동기 혼용의 모호성**: 동기 호출과 비동기 메시지를 명확한 기준 없이 혼용하면 서비스 경계가 불명확해지고 트랜잭션 처리가 복잡해진다.

- **📢 섹션 요약 비유**: 같은 편지를 두 번 받아도 한 번만 처리해야 한다(멱등성). 배달 불가 편지(DLQ)는 우체국에 보관해 나중에 처리하고, 지연 발송(재시도) 시 간격을 점점 늘려야 과부하를 방지한다.

---

## Ⅴ. 기대효과 및 결론

비동기 통신을 올바르게 도입하면 마이크로서비스 아키텍처의 핵심 품질 속성인 회복성(Resilience)과 확장성(Scalability)이 크게 향상된다.

**정량적 효과**: Kafka를 활용한 이벤트 기반 처리는 초당 수백만 건의 이벤트를 처리할 수 있으며(LinkedIn은 하루 수조 건), 소비자 그룹을 추가하여 선형적 처리량 확장이 가능하다. Netflix는 Kafka를 통해 수백 개 서비스 간의 이벤트를 처리하며, 서비스 장애 시에도 메시지가 큐에 보존되어 복구 후 재처리가 가능하다.

**정성적 효과**: 생산자와 소비자의 시간적·공간적 결합이 제거되어 독립적 배포와 독립적 확장이 가능해진다. 새로운 소비자(기능)를 추가할 때 생산자 코드를 변경할 필요가 없어 개방-폐쇄 원칙(Open-Closed Principle)을 자연스럽게 구현한다.

결론적으로, 비동기 메시지 기반 통신은 마이크로서비스의 느슨한 결합을 실현하는 핵심 기술이다. 동기 통신과 비동기 통신을 명확한 기준(응답 즉시성, 일관성 요구, 처리 시간)에 따라 적절히 혼용하는 것이 현대 마이크로서비스 아키텍처의 정석이다.

- **📢 섹션 요약 비유**: 바로 답하지 않아도 되는 업무는 우편함에 넣어두면 되지만, 우편함이 꽉 차거나(큐 과부하), 편지가 손실되거나(메시지 손실), 같은 편지를 두 번 처리하는 것(중복 처리)을 막기 위한 관리가 필수다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 서비스 간 동기 통신 (535) | 비동기의 대안, 즉각 응답 필요 시 활용 |
| 이벤트 기반 아키텍처 (538) | 비동기 통신의 상위 아키텍처 패턴 |
| 이벤트 버스와 스트림 처리 (539) | 비동기 통신 구현의 핵심 인프라 |
| 사가 패턴 (550) | 비동기 메시지를 통한 분산 트랜잭션 처리 |
| 이벤트 소싱 (555) | 비동기 이벤트를 상태의 원천으로 활용 |
| CQRS (554) | 커맨드와 쿼리를 비동기 이벤트로 분리 |
| 서킷 브레이커 (572) | 비동기 소비자의 장애 격리 패턴 |
| 분산 추적 (569) | 비동기 메시지 흐름의 추적 및 디버깅 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">IBM MQ (MQSeries) - 엔터프라이즈 메시지 큐 시작 (1990년대)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">AMQP (Advanced Message Queuing Protocol) 표준화 (2003)</div>
<div class="kb-diagram-note">(JPMorgan Chase 주도, 금융권 오픈 표준)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">RabbitMQ 오픈소스 출시 (2007)</div>
<div class="kb-diagram-note">(AMQP 구현체, 엔터프라이즈 표준)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Apache Kafka 오픈소스 공개 (LinkedIn, 2011)</div>
<div class="kb-diagram-note">(로그 수집용 → 이벤트 스트리밍 플랫폼으로 진화)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">이벤트 기반 아키텍처 (EDA) 확산 (2015~)</div>
<div class="kb-diagram-note">(마이크로서비스 표준 통신 패턴)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Kafka Streams, Apache Flink 실시간 처리</div>
<div class="kb-diagram-note">(스트림 처리 + 비동기 통신 융합)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">클라우드 네이티브 메시징</div>
<div class="kb-diagram-note">(AWS SQS/SNS, Azure Service Bus, GCP Pub/Sub)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 친구한테 카카오톡으로 메시지를 보내면, 친구가 지금 폰을 안 봐도 메시지는 사라지지 않고 나중에 읽을 수 있어요 - 이것이 비동기 통신이에요.
2. 여러 친구에게 같은 메시지를 보낼 수 있고(Pub/Sub), 각 친구가 자기 속도로 읽고 답장해도 되니, 내 카카오톡(생산자 서비스)은 계속 다른 일을 할 수 있어요.
3. 단, 같은 메시지를 두 번 보내도 친구가 한 번만 처리하게 하거나(멱등성), 읽지 못한 메시지를 별도로 보관하는(DLQ) 규칙이 있어야 문제가 생기지 않아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 664 / 973

← **이전**: [536. 서비스 간 비동기 통신 - 메시지 큐 (RabbitMQ, Kafka), AMQP 프로토콜](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/536_asynchronous_communication_kafka_rabbitmq/)
**다음**: [537. 안티패턴: 분산 모놀리스 (Distributed Monolith) - 독립 배포 불가능한 MSA](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/537_anti_pattern_distributed_monolith/) →

---
