---
title: "Outbox 패턴 (Outbox Pattern)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 250
---

# 📖 【암기용】 개념 완전 이해

> 목적: Outbox 패턴을 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: DB 변경과 이벤트 발행을 하나의 로컬 트랜잭션으로 묶기 위해 outbox 테이블에 이벤트를 먼저 저장하는 패턴
- **왜 필요한가**: 주문 DB 저장은 성공했는데 메시지 브로커 발행이 실패하면 다른 서비스는 주문 생성 사실을 모른다. 반대로 발행 후 DB 저장이 실패하면 존재하지 않는 주문 이벤트가 퍼진다.
- **핵심 직관**: 우편함에 편지를 넣는 행위까지 거래 장부에 기록하고, 배달부가 나중에 안전하게 발송하는 방식이다.

## 깊이 이해
- **배경·문제의식**: 분산 트랜잭션 2PC는 운영 비용과 결합도가 크다. MSA에서는 서비스 DB와 메시지 브로커를 하나의 글로벌 트랜잭션으로 묶기 어렵기 때문에 로컬 트랜잭션과 비동기 발행으로 정합성을 맞춘다.
- **작동 원리**: 업무 테이블 변경과 outbox 이벤트 row 삽입을 같은 DB 트랜잭션으로 커밋한다. 별도 publisher가 outbox를 읽어 Kafka/RabbitMQ로 발행하고 성공 시 published 상태로 바꾼다.
- **비유**: 온라인 쇼핑 주문서를 저장하면서 택배 발송 요청서를 같은 서랍에 넣고, 택배 담당자가 주기적으로 서랍을 비우는 방식이다.
- **구체 예시**: `orders` insert와 `outbox_events(OrderCreated)` insert를 한 트랜잭션으로 커밋하고, Debezium CDC 또는 poller가 Kafka topic으로 발행한다.
- **흔한 오해·주의점**: Outbox는 exactly-once를 마법처럼 보장하지 않는다. publisher 재시도 때문에 소비자는 멱등성 처리가 필요하다.

## 연결 개념
- Saga Pattern — 서비스 간 장기 트랜잭션 조정
- Idempotency Design — 중복 이벤트 소비 방지
- CDC — outbox 테이블 변경을 이벤트 스트림으로 전송

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Outbox 답안은 로컬 트랜잭션, 비동기 발행, 중복 소비, 지연 모니터링까지 포함해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Outbox Pattern은 업무 DB 변경과 발행할 이벤트 저장을 같은 로컬 트랜잭션으로 처리하는 분산 정합성 패턴이다.
> 2. **가치**: DB commit 성공과 이벤트 발행 실패 사이의 불일치를 줄이고 2PC 없이 서비스 간 이벤트 전달을 구현한다.
> 3. **판단 포인트**: outbox table, publisher/CDC, at-least-once 발행, consumer idempotency, lag monitoring이 필수이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 분산 정합성 이해 확인 | DB 변경과 이벤트 발행 원자성 문제 | 단순 메시지 큐 사용으로 답함 |
| MSA 패턴 판단 확인 | 2PC 대안, Saga 연계, CDC | exactly-once 보장으로 과장 |
| 운영 설계 확인 | 재시도, 중복 소비, outbox lag | 발행 지연과 테이블 정리 누락 |

> 요약: Outbox는 DB와 브로커 사이 원자성 간극을 로컬 트랜잭션과 비동기 발행으로 줄이는 패턴이다.

---

## Ⅰ. 개요 및 필요성

Outbox 패턴은 업무 데이터 변경과 이벤트 저장을 한 트랜잭션으로 묶는 패턴이다. MSA에서 DB와 메시지 브로커를 동시에 커밋하기 어렵기 때문에 이벤트 유실 또는 거짓 발행 문제가 발생한다. 기술사는 2PC 대신 로컬 트랜잭션과 멱등 소비를 조합해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Service Transaction -> Business Table + Outbox Table
                    -> Publisher/CDC -> Message Broker -> Consumer
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Business Table | 주문·결제 등 업무 상태 저장 | local transaction 대상 |
| Outbox Table | 발행할 이벤트 payload 저장 | event id, status, created_at |
| Publisher/CDC | outbox를 읽어 브로커로 발행 | poller 또는 Debezium |
| Consumer | 이벤트 처리와 멱등성 보장 | processed_event table |

> 요약: Outbox는 업무 테이블과 이벤트 테이블을 같은 DB 트랜잭션에 넣고 발행은 별도 프로세스가 처리한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
명령 처리 -> 업무 row 저장 + outbox row 저장
-> commit -> publisher 발행 -> consumer 멱등 처리
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 서비스가 업무 트랜잭션 시작 | DB local transaction |
| 2 | 업무 row와 outbox event를 함께 insert | commit 원자성 보장 |
| 3 | publisher가 미발행 row를 브로커로 전송 | outbox lag 30초 이하 |
| 4 | consumer가 event id로 중복 처리 차단 | 중복 반영 0건 |

> 요약: Outbox는 저장 원자성을 DB에 맡기고 발행과 소비는 at-least-once와 멱등성으로 처리한다.

---

## Ⅳ. 특징

| 구분 | 직접 발행 | Outbox 패턴 | 수치 판단 |
|:---|:---|:---|:---|
| 원자성 | DB commit과 publish 분리 | DB row와 event row 동시 commit | 이벤트 유실 0건 목표 |
| 발행 방식 | 동기 publish | poller/CDC 비동기 발행 | lag 30초 이하 |
| 중복 | 재시도 시 중복 가능 | at-least-once 전제 | consumer 멱등 처리 필수 |

> 요약: Outbox는 이벤트 유실을 줄이지만 중복 발행 가능성을 소비자 멱등성으로 흡수해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 트랜잭션 | 2PC | local transaction + outbox | 서비스 독립성과 브로커 분리 필요 시 |
| 발행 | API 처리 중 직접 publish | 비동기 publisher/CDC | DB commit 이후 재시도 필요 시 |
| 정합성 | 강한 일관성 추구 | eventual consistency | Saga 기반 업무 보상 가능 시 |

> 요약: 2PC 부담이 큰 MSA에서는 Outbox가 이벤트 유실 방지와 서비스 자율성의 균형점을 제공한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 발행 지연 | publisher 장애, 큐 적체 | 다중 publisher, lag alert | outbox lag 30초 이하 |
| 중복 소비 | 발행 재시도 | event id 기반 멱등 처리 | 중복 반영 0건 |
| 테이블 증가 | 발행 완료 row 누적 | partition, TTL cleanup | 보관 기간 7~30일 |

> 요약: Outbox 운영 리스크는 발행 지연, 중복 소비, 테이블 증가이며 lag와 cleanup으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 유실 방지 | commit된 event 발행률 100% | outbox vs broker audit |
| 지연 | outbox lag 30초 이하 | publisher metric |
| 소비 | 중복 업무 반영 0건 | consumer idempotency log |

> 요약: Outbox 검증은 유실률, 발행 지연, 소비자 멱등 처리 결과로 수행한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 주문 저장 트랜잭션에 `orders` insert와 `outbox_events` insert를 포함하고 event id unique index를 설정
2. Debezium CDC 또는 poller가 미발행 이벤트를 Kafka로 전송하며 outbox lag 30초 초과 시 경보 발생
3. 소비자는 `processed_event` 테이블로 event id 중복 반영을 차단하고 cleanup은 7~30일 보관 정책으로 수행

**결론 (2줄):**
- 기술사 판단: MSA에서 DB와 브로커 간 원자성 문제가 있으면 2PC보다 Outbox와 멱등 소비 조합을 우선 검토한다
- 향후 방향: CDC 기반 Outbox, Kafka transaction, Saga orchestration이 결합되어 서비스 간 정합성 패턴의 표준 조합으로 확산된다

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Outbox 패턴을 설명하시오" | 로컬 트랜잭션과 비동기 발행 흐름 | 직접 발행과 Outbox 차이 |
| 요구사항 명시형 | "MSA 정합성 방안을 제시하시오", "비교하시오" | 2PC 대안, CDC, 멱등 소비 설계 | 유실·중복·지연 통제 기준 |

> 요약: 설명형은 구조와 흐름, 방안형은 2PC 대안과 운영 지표를 중심으로 답한다.
