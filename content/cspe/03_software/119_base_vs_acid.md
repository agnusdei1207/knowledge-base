---
title: "BASE vs ACID (BASE vs ACID)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 119
---

# 📖 【암기용】 개념 완전 이해

> 목적: BASE vs ACID를 처음 보는 사람도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 엄격한 트랜잭션 보장인 ACID와 완화된 분산 일관성 모델인 BASE를 비교하는 관점
- **왜 필요한가**: 모든 데이터가 같은 수준의 즉시 일관성을 요구하지 않는다. 결제 원장은 ACID가 필요하지만 피드 좋아요 수, 추천 결과, 캐시 데이터는 잠시 차이가 나도 서비스가 유지될 수 있다.
- **핵심 직관**: 은행 장부는 한 숫자라도 틀리면 안 되지만, 게시물 조회수는 몇 초 뒤 맞아도 사용자 피해가 작다.

## 깊이 이해
- **배경·문제의식**: RDBMS는 ACID로 원자성·일관성·격리성·지속성을 제공한다. 분산 NoSQL은 대규모 가용성과 지연 요구 때문에 Basically Available, Soft state, Eventual consistency로 완화된 모델을 채택한다.
- **작동 원리**: ACID는 트랜잭션 commit 시점에 제약조건과 로그를 통해 일관 상태를 보장한다. BASE는 요청을 가능한 범위에서 받아들이고, 중간 상태 변화를 허용하며, 시간이 지나면 replicas가 수렴하도록 설계한다.
- **비유**: ACID는 회계 결산처럼 모든 항목이 맞아야 제출하고, BASE는 협업 문서처럼 각자 먼저 수정한 뒤 동기화로 맞춘다.
- **구체 예시**: 계좌 이체는 debit/credit이 하나의 ACID 트랜잭션이어야 한다. 반면 소셜 피드 좋아요 수는 Kafka 이벤트와 비동기 집계로 5초 뒤 수렴해도 업무 허용 범위일 수 있다.
- **흔한 오해·주의점**: BASE는 데이터 무결성을 포기한다는 뜻이 아니다. 충돌 해결, 재처리, idempotency, 보상 거래를 통해 허용된 범위 안에서 수렴을 관리한다.

## 연결 개념
- ACID — Atomicity, Consistency, Isolation, Durability
- BASE — Basically Available, Soft state, Eventual consistency
- CAP·PACELC — 분산 환경에서 일관성과 가용성·지연의 선택 설명
- Saga·Outbox — BASE 성향 시스템에서 트랜잭션 경계를 나누는 패턴

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: BASE vs ACID 답안은 용어 비교를 넘어 업무 데이터 등급과 분산 트랜잭션 설계 기준을 제시해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ACID는 트랜잭션 단위의 엄격한 일관성을, BASE는 분산 환경에서 가용성과 사후 수렴을 우선하는 모델이다.
> 2. **가치**: 원장·결제·재고는 ACID, 피드·캐시·분석 집계는 BASE 성향으로 분리해 SLA와 비용을 맞춘다.
> 3. **판단 포인트**: 불일치 허용 시간, 보상 거래 가능성, 재처리 설계, 충돌 해결 기준이 선택의 핵심이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 트랜잭션 모델 비교 역량 확인 | ACID 4요소와 BASE 3요소 | BASE를 단순히 일관성 없음으로 설명 |
| 분산 시스템 설계 판단 확인 | strict transaction vs eventual consistency | 업무별 데이터 등급과 허용 시간 누락 |
| 실무 적용 패턴 확인 | Saga, Outbox, idempotency, conflict resolution | RDBMS vs NoSQL 제품 비교로만 끝냄 |

> 요약: 이 문제는 엄격한 트랜잭션과 사후 수렴 모델을 업무 위험 기준으로 구분하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

BASE vs ACID는 데이터 일관성 보장 수준의 비교 관점이다. ACID는 트랜잭션 commit 시 일관 상태를 보장하고, BASE는 분산 환경에서 응답 지속과 사후 수렴을 선택한다. 시스템 설계자는 업무별 불일치 비용과 복구 방식을 기준으로 모델을 선택해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Business Data -> Consistency Requirement
  / ACID: Atomicity + Consistency + Isolation + Durability
  / BASE: Basically Available + Soft State + Eventual Consistency
Transaction Boundary -> Compensation/Recovery -> SLA
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Atomicity | 전부 성공 또는 전부 취소 | 계좌 이체·주문 결제 |
| Isolation | 동시 트랜잭션 간 간섭 제어 | 격리 수준과 lock/MVCC 연결 |
| Basically Available | 일부 기능·응답을 유지 | degradation, fallback 허용 |
| Soft State | 중간 상태 변화 허용 | replica lag, pending 상태 |
| Eventual Consistency | 시간이 지나면 수렴 | 재처리·충돌 해결 필요 |

> 요약: ACID는 commit 순간의 정확한 상태, BASE는 허용된 중간 상태와 사후 수렴을 중심으로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
업무 요청 -> 데이터 등급 판단
  / ACID 필요 -> 단일 트랜잭션 -> lock/MVCC -> commit/rollback
  / BASE 허용 -> event 발행 -> 비동기 처리 -> 수렴 검증
불일치 감지 -> 보상 거래 or 재처리 -> 감사 로그 기록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 데이터 불일치 비용과 허용 시간 산정 | RPO, stale 허용 초 |
| 2 | ACID 업무는 트랜잭션 경계 설정 | rollback 성공률 |
| 3 | BASE 업무는 이벤트·큐 기반 처리 | retry 성공률, DLQ |
| 4 | 중간 상태와 충돌 해결 정책 적용 | pending age, conflict count |
| 5 | 최종 수렴과 감사 로그 확인 | reconciliation success rate |

> 요약: ACID는 즉시 commit 기준, BASE는 이벤트 처리와 보상 절차를 통해 허용 시간 내 수렴시키는 흐름이다.

---

## Ⅳ. 특징

| 구분 | ACID | BASE | 수치·판단 기준 |
|:---|:---|:---|:---|
| 일관성 시점 | commit 즉시 | 일정 시간 후 수렴 | stale 허용 0초 vs 1~60초 |
| 가용성 | lock·quorum에 영향 | 일부 응답 지속 | degraded mode 가능 |
| 트랜잭션 | 엄격한 원자성 | 보상 거래·재처리 | Saga step success rate |
| 대표 업무 | 원장, 결제, 재고 차감 | 피드, 알림, 추천, 캐시 | 불일치 피해 금액 |
| 운영 요구 | DB 로그·격리 수준 | idempotency·DLQ·reconcile | DLQ 0건 목표 |

> 요약: ACID는 불일치 비용이 큰 업무, BASE는 일시 차이를 허용하고 사후 수렴이 가능한 업무에 맞다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 결제 | BASE 허용 | ACID 선택 | 이중 결제·누락 허용 불가 |
| 재고 | 순차 ACID | 조건부 ACID+예약 | 초과 판매 비용 기준 |
| 피드 | ACID 적용 | BASE 선택 | stale 5~30초 허용 |
| MSA 거래 | 2PC | Saga/Outbox | 서비스 독립 배포 요구 |
| 분석 집계 | 즉시 반영 | 비동기 집계 | 결과 수렴 시간 SLA |

> 요약: 금전·권한·재고는 ACID 우선, 경험·집계·알림은 BASE와 재처리 설계를 검토한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 데이터 불일치 | 이벤트 누락·중복 | outbox, idempotency key | duplicate rate |
| 장기 pending | 비동기 처리 실패 | DLQ, retry backoff, alert | pending age |
| 보상 실패 | Saga 단계 오류 | compensating transaction | compensation failure |
| 과도한 lock | ACID 경계 과대 | 트랜잭션 축소, 격리 수준 조정 | lock wait p95 |

> 요약: BASE는 중복·누락·pending, ACID는 lock wait와 경계 과대가 주요 리스크이다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 불일치 시간 | 업무별 0초/5초/60초 | read-after-write test |
| 재처리 | retry 성공률 99.9% | queue metric |
| DLQ | 미처리 0건 또는 SLA 내 처리 | DLQ dashboard |
| 트랜잭션 지연 | p95 commit 100ms 이하 | DB APM |

> 요약: 모델 선택 이후에는 불일치 시간, 재처리, DLQ, commit 지연, 감사 로그로 품질을 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 데이터 등급화: 원장·권한·재고는 ACID, 피드·알림·분석 집계는 BASE로 구분하고 stale 허용 시간을 SLA에 명시함
2. BASE 구현: Outbox, Kafka, idempotency key, DLQ, reconciliation job을 적용해 중복·누락·장기 pending을 통제함
3. ACID 최적화: 트랜잭션 경계를 100ms 이하 작업으로 축소하고 격리 수준을 Read Committed, Repeatable Read 등 업무별로 선택함

**결론 (2줄):**
- 기술사 판단: 불일치 피해가 금전·권한에 연결되면 ACID, 사후 보상과 수렴이 가능하면 BASE를 적용하는 조건부 판단이 타당함
- 향후 방향: 분산 트랜잭션은 2PC 단독보다 Saga, Outbox, CDC 기반 수렴 검증을 조합하는 방향임

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "BASE와 ACID를 설명하시오", "기술하시오" | 트랜잭션 commit과 비동기 수렴 흐름 | ACID 4요소와 BASE 3요소 비교 |
| 요구사항 명시형 | "비교하시오", "적용 방안을 제시하시오" | 업무 데이터 등급과 보상 거래 절차 | 불일치 허용 시간, DLQ, lock wait 대응 |

> 요약: 설명형은 요소 비교, 적용형은 업무별 데이터 등급과 운영 통제 지표 중심으로 전환한다.
