---
title: "Saga 패턴 - 분산 트랜잭션 (Saga Pattern)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 48
---

# 📖 【암기용】 개념 완전 이해

> 목적: Saga 패턴을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 여러 서비스의 로컬 트랜잭션을 보상 트랜잭션으로 연결하는 분산 트랜잭션 패턴
- **왜 필요한가**: MSA는 서비스별 DB를 분리하므로 하나의 ACID 트랜잭션으로 주문·결제·배송을 묶기 어려움. 실패 시 이미 완료된 단계를 되돌리는 업무 보상이 필요함.
- **핵심 직관**: 여행 예약에서 항공권 결제 후 호텔 예약이 실패하면 항공권을 취소하는 절차를 미리 정해두는 방식임.

## 깊이 이해
- **배경·문제의식**: 2PC는 참여자 잠금과 coordinator 장애 문제가 있어 고가용 MSA에 부담이 큼. Saga는 각 서비스가 로컬 트랜잭션을 완료하고 이벤트 또는 orchestrator로 다음 단계를 진행함.
- **작동 원리**: Choreography는 서비스가 이벤트를 구독해 다음 동작을 수행함. Orchestration은 중앙 Saga coordinator가 단계와 보상을 지시함.
- **비유**: 릴레이 경주에서 각 주자가 자기 구간을 뛰고 바통을 넘기며, 문제가 생기면 정해진 복귀 절차를 수행하는 방식임.
- **구체 예시**: 주문 생성 -> 결제 승인 -> 재고 차감 -> 배송 요청 중 재고 차감 실패 시 결제 취소와 주문 취소 이벤트를 발행함.
- **흔한 오해·주의점**: Saga는 즉시 일관성을 보장하지 않음. 최종 일관성을 전제로 하며, idempotency와 outbox 없이 구현하면 중복 처리와 메시지 유실이 발생함.

## 연결 개념
- Choreography/Orchestration: Saga 제어 방식
- Compensation Transaction: 업무 보상 처리
- Transactional Outbox: 이벤트 발행과 DB commit 정합성

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Saga 답안은 choreography/orchestration, compensation transaction, idempotency, outbox를 분산 정합성 관점으로 연결해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Saga는 여러 서비스의 로컬 트랜잭션을 순차 실행하고 실패 시 보상 트랜잭션으로 업무 상태를 복구하는 패턴이다.
> 2. **가치**: DB per Service 구조에서 2PC 없이 분산 업무 흐름을 처리하고 고가용성과 서비스 자율성을 유지함.
> 3. **판단 포인트**: 보상 가능 업무인지, 최종 일관성 허용 시간이 얼마인지, 메시지 중복·유실을 어떻게 통제할지 판단해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 분산 트랜잭션 이해 확인 | local transaction, compensation, eventual consistency | ACID와 동일하게 설명 |
| 제어 방식 비교 확인 | choreography vs orchestration | 두 방식을 이름만 나열 |
| 운영 정합성 판단 확인 | idempotency, outbox, retry, DLQ | 메시지 유실·중복 처리 누락 |

> 요약: 이 문제는 분산 트랜잭션을 DB 잠금이 아니라 업무 보상과 메시지 신뢰성으로 해결하는지를 묻는다.

---

## Ⅰ. 개요 및 필요성

Saga는 MSA 분산 트랜잭션 패턴이다. 서비스별 DB를 소유하는 MSA에서는 주문·결제·배송을 하나의 DB 트랜잭션으로 묶을 수 없다. Saga는 로컬 트랜잭션과 보상 트랜잭션으로 최종 일관성을 달성한다.

---

## Ⅱ. 구조 및 구성요소

```text
Order Service -> Local Tx -> OrderCreated Event
Payment Service -> Local Tx -> PaymentApproved Event
Inventory Service -> Local Tx / Fail -> Compensation Event
Saga Coordinator or Event Choreography -> State Tracking -> DLQ
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Local Transaction | 각 서비스 내부 ACID 처리 | DB per Service 유지 |
| Compensation | 완료된 업무를 반대 업무로 보상 | 취소, 환불, 재고 복원 |
| Saga Coordinator | orchestration 방식의 상태 제어 | 단계, timeout, 재시도 관리 |
| Event Broker/Outbox | 이벤트 전달 신뢰성 확보 | commit과 publish 불일치 방지 |

> 요약: Saga는 서비스별 로컬 트랜잭션을 이벤트나 coordinator로 연결하고 실패 시 보상 흐름을 실행한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Saga 시작 -> 서비스 A 로컬 트랜잭션 commit
-> 이벤트 발행 또는 coordinator 명령 -> 서비스 B 처리
-> 실패 감지 -> 보상 트랜잭션 역순 실행
-> Saga 상태 기록 -> 최종 성공/실패 확정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Saga instance 생성과 correlation ID 부여 | 중복 instance 0건 |
| 2 | 각 서비스 로컬 트랜잭션 수행 | local rollback rate |
| 3 | 이벤트 발행 또는 명령 전달 | outbox publish lag 5초 이하 |
| 4 | 실패 시 보상 트랜잭션 실행 | compensation success rate 99% |
| 5 | DLQ와 상태 저장소로 사후 처리 | unresolved saga count |

> 요약: Saga는 단계별 로컬 commit을 진행하고 실패 시 보상 흐름으로 업무 상태를 최종 정리한다.

---

## Ⅳ. 특징

| 구분 | 2PC | Saga Pattern | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 일관성 | 즉시 일관성 | 최종 일관성 | 허용 지연 1분 등 SLA 명시 |
| 가용성 | coordinator와 lock 의존 | 서비스별 독립 commit | lock 대기 제거 |
| 실패 처리 | rollback 중심 | compensation 중심 | 보상 성공률 99% 이상 |
| 복잡도 | DB/미들웨어 의존 | 업무 보상 설계 필요 | idempotency key 필수 |

> 요약: Saga는 고가용 MSA에 적합하지만 보상 가능한 업무와 최종 일관성 허용 범위가 전제이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 2PC, 공유 DB | local tx + compensation | 서비스별 DB와 고가용 요구 |
| 비용/성능 | lock 대기와 coordinator 의존 | 비동기 처리와 보상 비용 | 최종 일관성 지연 1분 이하 |
| 운영/위험 | rollback 단순 | 보상 실패, 중복 이벤트 | idempotent consumer 100% |

> 요약: Saga는 보상 가능한 업무와 비동기 정합성을 허용하는 도메인에서 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 보상 실패 | 외부 결제·재고 상태 불일치 | retry, manual task, DLQ | compensation failure rate |
| 중복 처리 | at-least-once delivery | idempotency key, unique constraint | duplicate event count |
| 이벤트 유실 | DB commit 후 publish 실패 | transactional outbox, CDC | outbox pending count |

> 요약: Saga의 핵심 리스크는 보상 실패와 메시지 신뢰성이며, outbox와 idempotency로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정합성 | unresolved saga 0건 | saga state store |
| 보상 처리 | 보상 성공률 99% 이상 | compensation log |
| 메시징 | outbox lag 5초 이하, DLQ 0.1% 이하 | broker metric |

> 요약: Saga 운영은 미해결 인스턴스, 보상 성공률, outbox/DLQ 지표로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 주문·결제·재고·배송 업무의 보상 가능 여부를 식별하고 각 단계별 compensation API와 timeout을 명시함.
2. Orchestration은 Temporal, Camunda, Axon, choreography는 Kafka event와 outbox를 적용해 correlation ID를 전파함.
3. idempotency key, retry policy, DLQ, manual resolution queue를 설계하고 unresolved saga count를 알림 기준으로 설정함.

**결론 (2줄):**
- 기술사 판단: 즉시 일관성이 절대 조건이면 Saga보다 단일 DB 또는 2PC를 검토하고, 고가용 MSA와 보상 가능 업무이면 Saga를 선택함.
- 향후 방향: Saga는 workflow engine, event streaming, observability와 결합해 장기 실행 업무 트랜잭션 표준으로 활용됨.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Saga 패턴을 설명하시오" | 로컬 트랜잭션과 보상 흐름 | 2PC 대비 최종 일관성 비교 |
| 요구사항 명시형 | "분산 트랜잭션 방안을 제시하시오", "설계하시오" | choreography/orchestration 선택과 outbox | 보상 실패, 중복 처리, DLQ 대응 |

> 요약: 설명형은 원리와 비교, 설계형은 보상 가능성·메시지 신뢰성·운영 지표 중심으로 전환한다.
