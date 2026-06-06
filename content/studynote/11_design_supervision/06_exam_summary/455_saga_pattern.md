---
title: "455. 사가 패턴 분산 트랜잭션 보상 (Saga Pattern Distributed Transaction Compensation)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Saga Pattern은 마이크로서비스 환경에서 **ACID의 원자성(Atomicity)을 포기**하고, 일련의 로컬 트랜잭션(`Ti`)과 그에 대응하는 **보상 트랜잭션(`Ci`)**을 통해 BASE 모델의 **최종 일관성(Eventual Consistency)**을 달성하는 분산 트랜잭션 해결 패턴이다.
> 2. **가치**: 2PC(2-Phase Commit) 대비 **응답 지연(Latency)을 1/10 수준**으로 단축하고, 단일 코디네이터의 SPOF(Single Point of Failure)를 제거하여 **시스템 가용성 99.99%** 달성이 가능하며, 장기 실행 트랜잭션(Long-Running Transaction)을 자연스럽게 지원한다.
> 3. **판단 포인트**: **Choreography vs Orchestration** 아키텍처 선택, 보상 불가능 단계(외부 API, 알림 발송 등)의 **Semaphore 처리 전략**, **격리성 결핍(Lack of Isolation)**으로 인한 더티 읽기/팬텀 읽기 허용 여부, 그리고 Saga Log의 **영속화 및 복제 전략**이 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

모놀리식 아키텍처가 도메인 단위로 분해되어 마이크로서비스로 전환되면, 단일 RDBMS의 `BEGIN...COMMIT`만으로 보장되던 트랜잭션 경계가 서비스 간 네트워크 호출을跨越하게 된다. 이때 **분산 트랜잭션의 본질적 난제**가 등장한다. CAP 정리에 따르면 네트워크 파티션(P)은 피할 수 없으므로, 일관성(C)과 가용성(A) 사이에서 선택해야 한다. 전통적인 2PC(XA Protocol)는 강한 일관성을 위해 **동기식 락(Synchronous Lock)**, **타임아웃 지연**, **코디네이터 SPOF**라는 세 가지 고질적 문제를 안고 있어, TPS(Transactions Per Second) 1,000 이상의 고부하 환경에서는 병목이 된다.

1987년 Garcia-Molina & Salem의 *"Sagas"* 논문에서 처음 개념이 제시된 Saga는, 하나의 비즈니스 트랜잭션을 **N개의 서브 트랜잭션**으로 분할하고, 중간 실패 시 이미 완료된 서브 트랜잭션들을 **역순으로 보상**하여 비즈니스적 무결성을 회복한다. 이는 "**롤백이 아닌 보상(Compensate, not Rollback)**"이라는 철학으로, 현실 도메인의 *비대칭성*(예: 결제 취소는 환불 행위이며, 결제 자체의 물리적 삭제가 아님)을 정확히 모델링한다.

```text
[정상 흐름 (Forward Path) - 모두 성공]
+----------+      +----------+      +----------+      +----------+
| OrderSvc | -T1-->|PaySvc    | -T2-->|InvSvc    | -T3-->|ShipSvc   |
| (주문생성)|      |(결제승인)|      |(재고차감)|      |(배송요청)|
+----------+      +----------+      +----------+      +----------+
      |                                                      |
      +-------------- 비즈니스 트랜잭션 완료 -----------------+

[실패 흐름 (Compensation Path) - T3에서 예외 발생]
+----------+      +----------+      +----------+      +----------+
| OrderSvc | <--C1-|PaySvc    | <--C2-|InvSvc    | <--X--|ShipSvc   |
| (주문취소)|      |(결제환불)|      |(재고복원)|      |(배송실패)|
+----------+      +----------+      +----------+      +----------+
                          보상 트랜잭션은 T의 역순으로 실행
```

**전환 패러다임**:
- **기존 (2PC/XA)**: *단일 글로벌 락 -> 강한 일관성 -> 낮은 가용성 -> 동기식 결합*
- **신규 (Saga)**: *서비스별 로컬 트랜잭션 -> 최종 일관성 -> 높은 가용성 -> 비동기 자율성*

- **📢 섹션 요약 비유**: 여러 은행에 분산된 자금을 이체할 때, A은행->B은행->C은행 순서로 보내다가 C은행이 실패하면, 이미 보낸 B은행과 A은행에서 **의미적으로 반대 거래**(환불/입금 취소)를 수행하여 전체를 원상복구하는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Saga는 두 가지 토폴로지로 구현되며, 메시지 전달 보장 수준과 도메인 복잡도에 따라 선택한다.

```text
[Choreography 방식 - 이벤트 기반 자율 협업]
        +-------------+  OrderCreated  +-------------+
        | OrderSvc    | --------------> | PaymentSvc  |
        | (Publisher) |                | (Subscriber)|
        +-------------+                +------+------+
                                              | PaymentCompleted
                                              v
                                       +-------------+
                                       | InventorySvc|
                                       +------+------+
                                              | InventoryReserved
                                              v
                                       +-------------+  ShipmentFailed
                                       | ShippingSvc | ------> Compensation
                                       +-------------+    Event 발행
   * 장점: 단일 장애점 없음, 서비스 결합도 낮음
   * 단점: Saga 흐름 추적 어려움, 순환 의존 위험

[Orchestration 방식 - 중앙 코디네이터]
                    +------------------------------+
                    |  Saga Orchestrator           |
                    |  (State Machine + Saga Log)  |
                    |  +--------------------+     |
                    |  |State: PENDING_PAY  |     |
                    |  |       v PAID       |     |
                    |  |       v RESERVED   |     |
                    |  |       v SHIPPED    |     |
                    |  |       v COMPLETED  |     |
                    |  +--------------------+     |
                    +------+-------+-------+------+
                  Command |       |       | Command
                           v       v       v
                    +--------++--------++--------+
                    |PaySvc  ||InvSvc  ||ShipSvc |
                    +--------++--------++--------+
                           Reply   Reply   Reply
   * 장점: 흐름 가시성, 명시적 상태 관리, 디버깅 용이
   * 단점: Orchestrator 자체의 SPOF 가능성, 개발 복잡도
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Saga Orchestrator** | 중앙 조정자, 비즈니스 트랜잭션의 상태머신(FSM) 관리 | **Camunda 8 (Zeebe)**, **Axon Server**, **Temporal**, **AWS Step Functions**, **Apache Airflow**, **Netflix Conductor**. 각 단계의 Command 발행, Reply 수신, 다음 상태 전이 규칙 보유 |
| **Saga Log / State Store** | Saga 인스턴스 실행 이력의 영속화 (At-least-once 보장) | **RDBMS (PostgreSQL/MySQL)**, **EventStoreDB**, **Kafka + Log Compaction**, **Redis + AOF**, **DynamoDB**. 멱등성 키(Saga ID + Step ID) 저장 |
| **Local Transaction Participant** | 각 마이크로서비스의 로컬 DB 트랜잭션 | 도메인 DB + JPA/JOOQ, 단일 서비스 내 **ACID 보장**. `Outbox Pattern`을 적용해 발행 보장 |
| **Compensating Action Handler** | 의미적 롤백 처리 (e.g., 결제승인 -> 결제환불) | 멱등성 보장을 위한 **Idempotency-Key** + **Optimistic Locking(version 필드)**, 보상 실패 시 **Dead Letter Queue** 적재 |
| **Event/Message Bus** | 비동기 메시지 전달, 순서 보장, 재시도 | **Apache Kafka (파티션 키 = SagaId)**, **Rabbit
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 455 / 600

<- **이전**: [454. 서킷 브레이커 패턴 장애 격리](/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern)
**다음**: [456. 스트랭글러 패턴 레거시 전환](/studynote/11_design_supervision/06_exam_summary/456_strangler_pattern/) ->

---
