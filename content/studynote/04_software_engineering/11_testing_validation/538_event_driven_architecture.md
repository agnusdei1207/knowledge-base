+++
title = "538. 이벤트 기반 아키텍처 (EDA)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 이벤트 기반 아키텍처(EDA, Event-Driven Architecture)는 시스템 내에서 발생한 상태 변화(이벤트)를 중심으로 컴포넌트들이 느슨하게 결합하여 반응하는 아키텍처 패턴으로, 이벤트 생산자와 소비자가 직접 연결되지 않는다.
> 2. **가치**: 생산자와 소비자 간의 시간적·공간적 결합을 제거하여 시스템 확장성과 회복성을 높이고, 새로운 기능 추가 시 기존 코드 변경 없이 새로운 소비자를 추가하는 개방-폐쇄 원칙을 자연스럽게 구현한다.
> 3. **판단 포인트**: 이벤트가 "발생한 사실(과거형)"을 나타내야 하며, 이벤트 스키마의 하위 호환성 관리, 멱등성 처리, 이벤트 흐름의 관측성 확보가 EDA 성공의 핵심 판단 기준이다.

---

## Ⅰ. 개요 및 필요성

이벤트 기반 아키텍처(EDA)는 1990년대부터 기업 통합(Enterprise Integration) 분야에서 사용되어 온 오래된 개념이다. 초기에는 GUI 프로그래밍에서 버튼 클릭 이벤트에 핸들러가 반응하는 단순한 형태였지만, 분산 시스템이 보편화되면서 서비스 간 통신 아키텍처로 발전했다.

마이크로서비스 아키텍처의 부상과 함께 EDA는 서비스 간 결합도를 낮추는 핵심 패턴으로 재조명받았다. 동기 HTTP 호출 체인이 만들어내는 강한 시간적 결합(temporal coupling) 문제를 해결하기 위해, "이벤트"라는 불변의 사실 레코드를 중심으로 시스템을 설계하는 접근법이 확산되었다.

EDA가 필요한 핵심 이유는 세 가지다. 첫째, **느슨한 결합(Loose Coupling)**: 이벤트 생산자는 누가 이벤트를 소비하는지 알 필요가 없고, 소비자는 누가 이벤트를 생산하는지 알 필요가 없다. 둘째, **독립적 확장**: 이벤트 소비자들은 각자의 처리 능력에 맞게 독립적으로 확장할 수 있다. 셋째, **감사 추적(Audit Trail)**: 모든 이벤트를 보존하면 시스템의 상태 변화를 완전하게 추적할 수 있다.

- **📢 섹션 요약 비유**: 학교 방송이 나오면 각 교실이 자기 역할대로 반응한다. 방송국은 각 교실이 어떻게 반응하는지 모르고, 교실도 방송국이 어떻게 방송을 만드는지 모른다. 둘은 "방송"이라는 이벤트로만 연결된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### EDA 핵심 구성 요소



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">이벤트 기반 아키텍처 전체 구조</div></div>
<div class="kb-diagram-note">이벤트 생산자 (Event Producer)</div>
<div class="kb-diagram-note">"OrderCreated" 이벤트 발행</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">이벤트 브로커 (Broker)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Apache Kafka / RabbitMQ /</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">AWS EventBridge</div></div>
<div class="kb-diagram-note">이벤트 구독 및 전달</div>
<div class="kb-diagram-note">결제 서비스 재고 서비스 알림 서비스</div>
<div class="kb-diagram-note">(이벤트 소비자) (이벤트 소비자) (이벤트 소비자)</div>
<div class="kb-diagram-note">각 소비자는 독립적으로 이벤트를 처리하며</div>
<div class="kb-diagram-note">서로의 존재를 알지 못한다</div>
</div>
</div>



### 이벤트 유형 분류

| 이벤트 유형 | 설명 | 특성 | 예시 |
|:---|:---|:---|:---|
| 도메인 이벤트 (Domain Event) | 비즈니스 상태 변화를 나타내는 이벤트 | 불변, 과거형 명명 | OrderPlaced, PaymentReceived |
| 통합 이벤트 (Integration Event) | 경계 컨텍스트 간 통합을 위한 이벤트 | 버전 관리 중요 | OrderShipped, CustomerCreated |
| 시스템 이벤트 (System Event) | 인프라/운영 상태 변화 | 기술적 사실 | ServiceHealthChanged, NodeFailure |
| 커맨드 이벤트 (Command Event) | 특정 행위를 요청하는 이벤트 | 수신자 한정 | ProcessPaymentCommand |

### 이벤트 구조 설계

```json
{
    "eventId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "eventType": "order.created.v1",
    "version": "1.0",
    "timestamp": "2024-01-15T09:30:00Z",
    "source": "order-service",
    "correlationId": "x9y8z7w6-...",
    "data": {
        "orderId": "ORD-2024-001",
        "customerId": "CUST-12345",
        "items": [
            {"productId": "PROD-001", "quantity": 2, "price": 29900}
        ],
        "totalAmount": 59800,
        "currency": "KRW"
    }
}
```

| 필드 | 목적 |
|:---|:---|
| eventId | 중복 처리 방지를 위한 고유 식별자 |
| eventType + version | 스키마 버전 관리 |
| correlationId | 분산 추적을 위한 요청 연관 ID |
| source | 이벤트 출처 서비스 식별 |
| timestamp | 이벤트 발생 시각 (UTC) |

### EDA 핵심 패턴 3가지

| 패턴 | 설명 | 구현 방식 | 적합 상황 |
|:---|:---|:---|:---|
| 발행-구독 (Pub/Sub) | 하나의 이벤트를 여러 소비자에게 전달 | Kafka Topic, SNS | 1:N 이벤트 전파 |
| 이벤트 스트리밍 | 연속적 이벤트를 실시간 분석 | Kafka Streams, Flink | 실시간 집계, 탐지 |
| 이벤트 소싱 (Event Sourcing) | 이벤트 자체가 상태의 원천 | Kafka + 이벤트 저장소 | 감사 추적, 재처리 |

### 코레오그래피(Choreography) vs 오케스트레이션(Orchestration)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">코레오그래피 방식 - 이벤트 기반</div></div>
<div class="kb-diagram-note">주문 서비스 → "OrderCreated" 이벤트 발행</div>
<div class="kb-diagram-note">결제 서비스 → 이벤트 수신 → 결제 처리 → "PaymentCompleted" 발행</div>
<div class="kb-diagram-note">재고 서비스 → 이벤트 수신 → 재고 차감 → "InventoryReserved" 발행</div>
<div class="kb-diagram-note">배송 서비스 → 이벤트 수신 → 배송 준비 → "ShipmentScheduled" 발행</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">오케스트레이션 방식 - 중앙 제어</div></div>
<div class="kb-diagram-note">오케스트레이터 → 결제 서비스 (동기 호출)</div>
<div class="kb-diagram-note">→ 재고 서비스 (동기 호출)</div>
<div class="kb-diagram-note">→ 배송 서비스 (동기 호출)</div>
</div>
</div>



| 비교 항목 | 코레오그래피 | 오케스트레이션 |
|:---|:---|:---|
| 결합도 | 낮음 | 중간 |
| 가시성 | 낮음 (흐름 추적 어려움) | 높음 (중앙에서 확인) |
| 확장성 | 높음 | 보통 |
| 복잡도 | 분산됨 | 중앙 집중 |

- **📢 섹션 요약 비유**: 오케스트라에 지휘자(오케스트레이션)가 있으면 전체 흐름을 한눈에 볼 수 있지만, 지휘자가 없는 재즈 즉흥 연주(코레오그래피)는 각 연주자가 서로의 음에 반응하여 자율적으로 진행한다. EDA는 재즈 방식에 가깝다.

---

## Ⅲ. 비교 및 연결

### 동기 요청-응답 vs EDA 비교

| 비교 항목 | 동기 요청-응답 | 이벤트 기반 아키텍처 (EDA) |
|:---|:---|:---|
| 결합 방식 | 강한 시간적 결합 | 느슨한 결합 |
| 생산자-소비자 관계 | 직접 연결 | 브로커를 통한 간접 연결 |
| 확장성 | 호출 서비스에 의존 | 독립적 확장 |
| 장애 전파 | 높음 | 낮음 (큐가 버퍼) |
| 데이터 일관성 | 강한 일관성 | 최종 일관성 |
| 새 기능 추가 | 생산자 코드 수정 필요 | 소비자만 추가하면 됨 |
| 디버깅 용이성 | 쉬움 (호출 스택 추적) | 어려움 (이벤트 흐름 추적) |

### EDA와 관련 아키텍처 패턴

EDA는 여러 현대 아키텍처 패턴과 긴밀히 연결된다.

- **이벤트 소싱(Event Sourcing)**: 상태를 이벤트 시퀀스로 저장하고, 현재 상태는 이벤트 재실행으로 재구성한다. EDA와 결합하면 완전한 변경 이력과 재처리 능력을 얻는다.
- **CQRS(Command Query Responsibility Segregation)**: 커맨드(쓰기)와 쿼리(읽기)를 분리하고, 이벤트로 읽기 모델을 동기화한다.
- **사가 패턴(Saga Pattern)**: EDA를 통해 분산 트랜잭션을 코레오그래피 방식으로 구현한다.
- **서버리스(Serverless)**: 이벤트 트리거로 함수를 실행하는 FaaS(Function as a Service)는 EDA의 극단적 구현이다.

- **📢 섹션 요약 비유**: 사진(이벤트)을 찍으면 자동으로 클라우드에 올라가고(Event Sourcing), 가족들이 각자 알림을 받고(Pub/Sub), 원하는 사람은 나중에 다시 봐도 된다(재처리). 사진 한 장이 여러 일을 동시에 일으킨다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### EDA 설계 핵심 원칙

```
[이벤트 설계 원칙]

1. 이벤트는 과거형 명명 (사실 기록)
   GOOD: OrderCreated, PaymentFailed, ItemShipped
   BAD:  CreateOrder, ProcessPayment (커맨드 형태)

2. 이벤트는 불변 (Immutable)
   - 발행된 이벤트는 수정 불가
   - 수정이 필요하면 새 이벤트 발행

3. 충분한 컨텍스트 포함
   - 소비자가 추가 조회 없이 처리 가능하게
   - 너무 많으면 의존성 증가, 너무 적으면 N+1 조회

4. 스키마 하위 호환성 유지
   - 필드 추가는 허용, 필드 삭제는 버전업
   - Schema Registry (Confluent, AWS Glue) 활용
```

### 설계 판단 체크리스트

1. **이벤트 정의 명확성**: 이벤트가 "무슨 일이 발생했는가"를 과거형으로 명확히 표현하는가?
2. **멱등성(Idempotency) 보장**: 동일 이벤트를 여러 번 처리해도 결과가 동일한가? (eventId 기반 중복 처리 방지)
3. **스키마 버전 관리**: 이벤트 스키마 변경 시 기존 소비자와 하위 호환성을 유지하는가?
4. **DLQ(Dead Letter Queue) 운영**: 처리 실패 이벤트를 추적하고 재처리하는 체계가 있는가?
5. **이벤트 순서 보장**: 순서가 중요한 이벤트(생성 → 수정 → 삭제)의 처리 순서를 보장하는가?
6. **관측성(Observability)**: 이벤트 흐름을 분산 추적(Distributed Tracing)으로 추적할 수 있는가?
7. **이벤트 보존 기간**: 재처리 필요성에 맞는 이벤트 보존 기간이 설정되어 있는가?

### 안티패턴

- **이벤트 체인 과다 (Long Event Chain)**: 이벤트 A가 이벤트 B를 유발하고, B가 C를 유발하고, C가 D를 유발하는 깊은 이벤트 체인은 디버깅을 극도로 어렵게 만든다. 단계가 너무 많으면 오케스트레이션 방식(사가 패턴)이 더 적합하다.
- **이벤트 내 커맨드 포함 (Event Contains Command)**: "SendEmailCommand"처럼 특정 행위를 명령하는 이벤트는 생산자가 소비자의 행위를 알고 있다는 것을 의미하므로 결합도가 높아진다. 이벤트는 사실만 기록하고 소비자가 행동을 결정해야 한다.
- **과도하게 세밀한 이벤트**: 필드 하나 변경마다 이벤트를 발행하면 소비자가 수많은 이벤트를 처리해야 하고 이벤트 브로커에 부하가 집중된다. 비즈니스 의미 있는 단위로 이벤트를 묶어야 한다.

- **📢 섹션 요약 비유**: 알림이 많이 울려도 같은 일을 두 번 하면 안 되고(멱등성), 알림 내용이 너무 많아도 너무 적어도 곤란하며, 어떤 알림이 어디로 갔는지 추적할 수 있어야 한다.

---

## Ⅴ. 기대효과 및 결론

이벤트 기반 아키텍처를 올바르게 적용하면 마이크로서비스 아키텍처의 핵심 목표인 느슨한 결합과 높은 확장성을 동시에 달성할 수 있다.

**정량적 효과**: Netflix는 EDA 기반으로 하루 수십억 건의 이벤트를 처리하며, Kafka를 통해 각 서비스가 독립적으로 초당 수백만 건을 처리한다. 새로운 기능 추가 시 기존 서비스 코드 변경 없이 새 소비자만 추가하면 되어 개발 속도가 크게 향상된다.

**정성적 효과**: 개방-폐쇄 원칙(Open-Closed Principle)의 자연스러운 구현으로 시스템이 확장에 열려 있고 변경에 닫혀 있다. 이벤트 로그를 감사 추적(Audit Trail)으로 활용하면 규정 준수(Compliance)와 디버깅이 용이해진다.

미래 방향으로는 서버리스(FaaS)와의 통합, AI/ML 모델 추론 결과를 이벤트로 발행하는 AI-Native EDA, 실시간 스트림 처리와 이벤트 기반의 융합이 핵심 트렌드로 자리잡고 있다.

- **📢 섹션 요약 비유**: 잘 설계된 이벤트 기반 시스템은 종합 방송 시스템과 같다. 방송이 나오면 각자 알아서 필요한 행동을 하고, 새 청취자가 추가되어도 기존 방송 시스템을 바꿀 필요가 없다. 단, 방송이 혼선 없이 전달되고 중복 수신도 처리되도록 관리해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 서비스 간 비동기 통신 (536) | EDA의 핵심 구현 수단 (메시지 큐, 이벤트 브로커) |
| 이벤트 버스 및 스트림 처리 (539) | EDA의 인프라 구성 요소 |
| 사가 패턴 (550) | EDA 기반의 분산 트랜잭션 처리 패턴 |
| CQRS (554) | EDA와 결합하여 읽기/쓰기 모델 분리 |
| 이벤트 소싱 (555) | 이벤트를 상태의 원천으로 활용하는 EDA 구현 |
| 분산 추적 (569) | EDA에서 이벤트 흐름 추적을 위한 관측성 도구 |
| 코레오그래피 사가 (553) | 이벤트 기반 분산 트랜잭션의 코레오그래피 구현 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">GUI 이벤트 핸들러 (1980-90년대)</div>
<div class="kb-diagram-note">(버튼 클릭, 마우스 이동 등 UI 이벤트)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">엔터프라이즈 통합 패턴 (EIP, 2003)</div>
<div class="kb-diagram-note">(메시지, 채널, 라우터, 필터 패턴 체계화)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">메시지 지향 미들웨어 (MOM) 확산</div>
<div class="kb-diagram-note">(IBM MQ, JMS, AMQP 기반 시스템)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Apache Kafka 등장 (2011)</div>
<div class="kb-diagram-note">(이벤트 스트리밍 플랫폼, 대용량 처리)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">마이크로서비스 + EDA 결합 (2015~)</div>
<div class="kb-diagram-note">(코레오그래피 사가, 이벤트 소싱 확산)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">서버리스 + EDA 융합 (2018~)</div>
<div class="kb-diagram-note">(AWS EventBridge, Lambda 이벤트 트리거)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">AI-Native EDA (현재~)</div>
<div class="kb-diagram-note">(ML 추론 결과를 이벤트로 발행, 실시간 AI 파이프라인)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 학교 방송(이벤트)이 나오면 각 교실(서비스)이 알아서 행동한다 - 방송은 누가 듣는지 모르고, 교실도 방송국이 어떻게 만드는지 몰라도 된다.
2. 새 교실이 생겨도 기존 방송 시스템을 바꿀 필요 없이 그냥 방송을 듣기 시작하면 되니까, 학교(시스템)를 쉽게 확장할 수 있다.
3. 단, 방송이 두 번 들려도 한 번만 행동하고(멱등성), 방송을 제대로 받았는지 확인하고(관측성), 놓친 방송은 나중에 다시 들을 수 있어야(재처리) 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 667 / 973

← **이전**: [537. 분산 모놀리스 (Distributed Monolith) 안티패턴](/knowledge-base/studynote/04_software_engineering/11_testing_validation/537_distributed_monolith_antipattern/)
**다음**: [538. 이벤트 기반 아키텍처 (EDA) - 이벤트 생산자, 브로커, 소비자](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/538_event_driven_architecture_eda/) →

---
