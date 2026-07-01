---
title: "이벤트 기반 아키텍처 (Event-Driven Architecture)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 207
---

# 📖 【암기용】 개념 완전 이해

> 목적: 이벤트 기반 아키텍처를 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 상태 변화 이벤트를 발행하고 여러 소비자가 비동기로 반응하는 아키텍처
- **왜 필요한가**: 주문 완료, 결제 승인, 재고 차감, 알림 발송처럼 한 사건 뒤 여러 처리가 이어질 때 동기 호출 체인은 장애 전파와 결합도 증가를 만든다.
- **핵심 직관**: 방송국이 뉴스를 송출하면 필요한 부서가 각자 듣고 후속 조치를 하는 방식이다.

## 깊이 이해
- **배경·문제의식**: MSA는 서비스 자율성을 높이지만 동기 API 체인이 길어지면 분산 모놀리스가 된다. 이벤트 기반 구조는 발행자와 소비자의 시간·구현 결합을 줄인다.
- **작동 원리**: 서비스가 업무 상태 변화를 이벤트로 발행하면 broker 또는 event streaming platform이 전달한다. 소비자는 이벤트를 구독해 자체 DB를 갱신하거나 후속 프로세스를 실행한다.
- **비유**: 은행 입금 알림을 받으면 회계, 문자, 포인트 시스템이 각각 필요한 업무를 수행하는 구조임.
- **구체 예시**: `OrderCreated` 이벤트 1건을 발행하면 결제 예약, 재고 차감, 알림 발송, 분석 적재 4개 소비자가 독립적으로 처리함.
- **흔한 오해·주의점**: 이벤트 기반 구조는 트랜잭션을 없애지 않는다. 정확한 이벤트 정의, outbox, idempotency, eventually consistent UX 설계가 필요하다.

## 연결 개념
- Message Queue·Kafka — 이벤트 전달 인프라
- Saga Pattern — 장기 트랜잭션 보상 처리
- CQRS — 명령 모델과 조회 모델 분리

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 수치·표준명·비교축으로 작성한다.
> 핵심: EDA는 비동기 메시징 도입이 아니라 이벤트 의미, 전달 보장, 일관성 모델을 함께 설계하는 아키텍처이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: EDA는 도메인 상태 변화를 이벤트로 발행하고 구독자가 비동기로 처리하는 구조이다.
> 2. **가치**: 서비스 결합도와 장애 전파를 줄이고, 신규 소비자를 발행자 수정 없이 추가한다.
> 3. **판단 포인트**: 이벤트 스키마, outbox, 순서, 중복, eventual consistency, 관측성을 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 분산 아키텍처 설계 확인 | Event producer, broker, consumer, schema registry | 단순 메시지 큐 사용으로 축소 |
| 일관성 판단 확인 | eventual consistency, Saga, outbox | ACID 전체 보장으로 오해 |
| 운영 리스크 확인 | 중복, 순서, 재처리, poison event | 이벤트 추적·보상 처리 누락 |

> 요약: 이 문제는 이벤트 전달 기술보다 도메인 이벤트와 일관성 통제 설계를 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 이벤트 발행·구독 분산 아키텍처
- 배경: MSA의 동기 호출 체인은 장애 전파와 배포 결합을 만든다.
- 필요성: event broker, schema registry, DLQ, trace 기준으로 서비스 결합도와 비동기 확장을 관리한다.

---

## Ⅱ. 구조 및 구성요소

```text
Domain Service -> Event Producer -> Broker/Stream -> Consumer A/B/C
                              +-> Schema Registry / DLQ / Trace
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Domain Event | 상태 변화의 사실 표현 | `OrderCreated`, `PaymentApproved` |
| Producer | 트랜잭션 후 이벤트 발행 | outbox pattern 권장 |
| Broker/Stream | 이벤트 저장·전달 | Kafka, RabbitMQ, Pulsar |
| Consumer | 이벤트 수신 후 후속 처리 | 멱등성과 재처리 필요 |

> 요약: EDA는 도메인 이벤트, 발행자, 전달 인프라, 소비자, 스키마·관측 통제로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
업무 트랜잭션 -> Outbox 저장 -> Event Publish -> Consumer 처리 -> Projection 갱신 -> Trace 수집
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 도메인 트랜잭션과 outbox 레코드 저장 | DB commit atomicity |
| 2 | relay가 event broker로 발행 | publish failure 재시도 |
| 3 | 소비자가 이벤트 처리 및 ACK | idempotency key 확인 |
| 4 | 조회 모델·후속 업무 갱신 | consumer lag, consistency delay 측정 |

> 요약: EDA는 트랜잭션과 이벤트 발행을 outbox로 묶고, 소비자 지연과 보상 처리를 관측한다.

---

## Ⅳ. 특징

| 구분 | 동기 호출 아키텍처 | 이벤트 기반 아키텍처 | 판단 포인트 |
|:---|:---|:---|:---|
| 결합 | 호출 대상·순서 고정 | 구독자 독립 추가 | 소비자 3개 이상이면 EDA 검토 |
| 일관성 | 요청 내 즉시 일관성 | 최종 일관성 | 지연 허용 1초~수분 여부 |
| 장애 | 하위 장애가 상위 응답에 영향 | 큐·스트림에 적재 후 재처리 | DLQ와 replay 필수 |
| 추적 | 단일 trace 상대 단순 | 비동기 trace 연결 필요 | correlation id 100% 전파 |

> 요약: EDA는 결합도를 낮추지만 최종 일관성과 비동기 관측성 설계가 필수이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Request/Response 체인 | Publish/Subscribe | 후속 처리 3개 이상, 독립 배포 필요 |
| 비용/성능 | 호출 지연 누적 | 비동기 지연 분산 | API p95 300ms 이하, consistency delay 허용 |
| 운영/위험 | 장애 즉시 노출 | lag·DLQ·replay 운영 | 운영팀이 event trace를 볼 수 있어야 함 |

> 요약: EDA는 즉시 응답보다 후속 처리 분리와 독립 확장이 더 큰 시스템에 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 이벤트 유실 | 트랜잭션 후 발행 실패 | transactional outbox | outbox pending 0건 |
| 중복 처리 | 재전달·consumer restart | idempotency, dedup store | duplicate side effect 0건 |
| 스키마 파손 | 이벤트 필드 삭제·타입 변경 | schema registry, compatibility check | incompatible schema 0건 |

> 요약: EDA 리스크는 유실, 중복, 스키마 파손이며 outbox와 schema registry로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 전달 | event publish success 99.9% 이상 | broker metric |
| 지연 | consumer lag 업무 SLA 이하 | stream offset, queue depth |
| 추적 | correlation id 전파 100% | distributed tracing |

> 요약: EDA 성공 여부는 이벤트 전달률, 소비 지연, trace 연결률로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. 도메인 이벤트는 past tense 명명, version 필드, schema registry compatibility rule로 표준화함.
2. Transactional outbox와 relay를 적용해 DB commit과 이벤트 발행 사이 유실 구간을 제거함.
3. Consumer 멱등성, DLQ, replay runbook, correlation id 전파를 운영 표준으로 정의함.

**결론 (2줄):**
- 기술사 판단: 즉시 일관성이 필수인 결제 승인 자체는 동기 처리, 승인 후 알림·분석·정산은 EDA로 분리함.
- 향후 방향: EDA는 CQRS, event sourcing, data mesh와 결합해 실시간 운영 데이터 플랫폼으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "EDA를 설명하시오" | outbox, publish, consume, projection 흐름 | 동기 호출 대비 결합·일관성 차이 |
| 요구사항 명시형 | "MSA 개선 방안을 제시하시오", "설계하시오" | 이벤트 스키마, Saga, DLQ, trace | 선택 기준, 리스크 대응, 점검 지표 |

> 요약: 설명형은 이벤트 원리, 설계·방안형은 일관성·재처리·관측성 통제를 중심으로 전환한다.
