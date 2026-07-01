---
title: "이벤트 기반 아키텍처 (Event-Driven Architecture)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 274
---

# 📖 【암기용】 개념 완전 이해

> 목적: 이벤트 기반 아키텍처를 상태 변화 사실을 이벤트로 발행하고 여러 소비자가 비동기로 반응하는 구조로 이해하게 만든다.

## 한눈에
- **개요**: 생산자가 이벤트를 발행하고 소비자가 이를 구독해 비동기 처리하는 아키텍처
- **왜 필요한가**: 서비스가 서로 직접 호출하면 변경 영향이 커지고 한 서비스 장애가 호출 체인을 따라 전파된다.
- **핵심 직관**: 결혼식 초대장을 발송하면 각 하객이 각자 일정과 준비를 진행하는 것처럼, 발행자는 후속 업무를 직접 지시하지 않는다.

## 깊이 이해
- **배경·문제의식**: MSA와 데이터 플랫폼은 주문 생성, 결제 완료, 배송 시작 같은 상태 변화를 여러 서비스가 독립적으로 활용해야 한다.
- **작동 원리**: producer가 event broker에 이벤트를 발행하고 broker는 topic·partition·subscription 규칙에 따라 consumer에게 전달한다.
- **비유**: 게시판에 공지를 올리면 부서별 담당자가 필요한 업무만 가져가 처리하는 구조다.
- **구체 예시**: `OrderCreated` 이벤트가 발행되면 재고 서비스는 예약을 수행하고, 알림 서비스는 메시지를 전송하며, 분석 서비스는 데이터 마트에 적재한다.
- **흔한 오해·주의점**: 이벤트는 명령이 아니라 발생한 사실이다. `SendEmail`보다 `OrderCreated`처럼 도메인 상태 변화를 표현해야 결합도가 낮다.

## 연결 개념
- Reactive System — EDA가 구현하는 메시지 기반 시스템 원칙
- FaaS — 이벤트를 함수 실행 트리거로 활용
- Stream Processing — 이벤트 흐름을 실시간 집계·분석하는 처리 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: EDA는 event producer, broker, consumer, schema, idempotency, ordering을 함께 설계해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: EDA는 도메인 상태 변화를 이벤트로 발행하고 소비자가 비동기로 반응하는 아키텍처임.
> 2. **가치**: 생산자와 소비자 결합도를 낮추고 장애 전파를 제한하며 후속 업무를 독립 확장함.
> 3. **판단 포인트**: eventual consistency, 메시지 순서, 중복 처리, schema evolution을 설계해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 비동기 아키텍처 이해 확인 | producer, broker, consumer, topic | 단순 큐 사용법으로 축소 |
| 도메인 모델링 확인 | event는 발생 사실, command와 구분 | 이벤트를 명령형 이름으로 설계 |
| 운영 리스크 판단 확인 | idempotency, ordering, DLQ, schema | 중복·순서·재처리 누락 |

> 요약: 이 문제는 이벤트로 결합도를 낮추는 구조와 비동기 운영 리스크를 함께 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 비동기 이벤트 발행·구독 구조
- 배경: 직접 호출 중심 MSA는 서비스 변경과 장애가 호출 체인을 따라 전파될 수 있음.
- 필요성: 주문·결제·알림·분석처럼 후속 업무가 많은 도메인은 이벤트로 결합도를 낮춰야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Producer -> Event Broker -> Topic / Partition -> Consumer Group
Schema Registry -> Event Contract -> Producer / Consumer
Consumer -> State Store / External API -> DLQ / Retry
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Producer | 도메인 이벤트 발행 | outbox pattern 적용 가능 |
| Broker | 이벤트 저장과 전달 | Kafka, NATS, cloud pub/sub |
| Consumer | 이벤트 구독과 후속 처리 | consumer group, offset |
| Schema Registry | 이벤트 계약 관리 | backward compatibility |

> 요약: EDA는 broker가 이벤트를 중개하고 schema가 생산자·소비자 간 계약을 관리하는 구조다.

---

## Ⅲ. 동작원리 및 흐름도

```text
도메인 상태 변경 -> 이벤트 생성 -> broker 발행
-> topic 저장 -> consumer polling / push -> 처리
-> offset commit -> 실패 시 retry / DLQ
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 트랜잭션 결과를 이벤트로 생성 | event name, schema |
| 2 | broker topic에 발행 | publish success |
| 3 | consumer가 이벤트를 읽고 처리 | consumer lag |
| 4 | 처리 성공 시 offset commit, 실패 시 DLQ | retry count, DLQ depth |

> 요약: EDA는 상태 변경을 이벤트로 저장·전달하고 소비자가 비동기로 처리 결과를 확정한다.

---

## Ⅳ. 특징

| 구분 | 동기 API 호출 | Event-Driven Architecture | 판단 기준 |
|:---|:---|:---|:---|
| 결합도 | 호출 대상과 시점 결합 | 이벤트 계약 중심 | 후속 소비자 수 |
| 일관성 | 즉시 응답 확인 | eventual consistency | 업무 허용 범위 |
| 장애 영향 | 호출 실패 전파 | broker·DLQ로 격리 | 장애 반경 |
| 추적 | 요청 경로 중심 | 메시지 흐름 추적 필요 | correlation id |

> 요약: EDA는 결합도와 장애 전파를 낮추지만 일관성·순서·추적 설계를 요구한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | REST orchestration | event choreography | 소비자 독립성 |
| 비용/성능 | 호출 구조 단순 | broker 운영 필요 | 이벤트량·보존 기간 |
| 운영/위험 | 실패 즉시 확인 | 재처리·순서 관리 필요 | idempotency 구현 가능 |

> 요약: 후속 업무가 독립적이고 지연 허용이 있으면 EDA, 즉시 트랜잭션은 동기 API가 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 중복 처리 | at-least-once 전달 | idempotency key | duplicate 처리 건수 |
| 순서 불일치 | partition key 오류 | aggregate id 기준 partition | out-of-order count |
| 계약 파괴 | schema 변경 | compatibility check | schema reject count |

> 요약: EDA 리스크는 중복, 순서, 계약 변경이며 idempotency·partition key·schema registry로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 전달 | publish failure 0건 | broker metric |
| 처리 | consumer lag 기준 이내 | lag dashboard |
| 재처리 | DLQ replay 절차 검증 | replay test |

> 요약: EDA 운영은 발행 실패, consumer lag, DLQ 재처리를 핵심 지표로 관리한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 이벤트 이름은 `OrderCreated`, `PaymentCompleted`처럼 과거형 도메인 사실로 정의하고 command와 분리함.
2. outbox pattern과 schema registry를 적용해 DB 트랜잭션과 이벤트 발행 누락을 통제함.
3. consumer는 idempotency key, retry policy, DLQ replay runbook을 갖추고 lag 기준으로 autoscaling함.

**결론 (2줄):**
- 기술사 판단: 후속 업무가 독립적이고 지연 허용이 있으면 EDA를 선택하고, 강한 즉시 일관성이 필요하면 동기 트랜잭션 경계를 유지함.
- 향후 방향: EDA는 FaaS, stream processing, event mesh와 결합되어 클라우드 네이티브 통합 패턴으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "EDA를 설명하시오" | 발행·저장·소비·재처리 흐름 | 동기 API 대비 차이 |
| 요구사항 명시형 | "비동기 MSA를 설계하시오" | outbox·schema·DLQ 절차 | 중복·순서·계약 리스크 |

> 요약: 설명형은 pub/sub 구조를, 설계형은 운영 리스크 통제를 중심으로 작성한다.
