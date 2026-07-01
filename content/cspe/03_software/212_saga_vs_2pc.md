---
title: "마이크로서비스 사가 패턴 vs 2PC (Saga vs 2PC)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 212
---

# 📖 【암기용】 개념 완전 이해

> 목적: Saga와 2PC를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 분산 트랜잭션에서 원자성과 가용성 사이 선택을 다루는 대표 패턴
- **왜 필요한가**: MSA는 서비스별 DB를 쓰므로 주문·결제·재고를 하나의 DB 트랜잭션으로 묶을 수 없음
- **핵심 직관**: 2PC는 모두 서명해야 확정하는 계약, Saga는 단계별 실행 후 실패 시 취소 거래를 쌓는 방식임

## 깊이 이해
- **배경·문제의식**: 모놀리식 DB는 ACID 트랜잭션으로 정합성을 맞추지만, MSA는 네트워크·장애·소유권 분리 때문에 전역 락이 비용을 만든다.
- **작동 원리**: 2PC는 Coordinator가 Prepare와 Commit 두 단계를 제어한다. Saga는 각 Local Transaction을 완료하고 실패하면 Compensation Transaction으로 앞 단계를 되돌린다.
- **비유**: 2PC는 모든 부서가 동시에 결재해야 문서가 완료되는 절차, Saga는 배송·결제·포장을 진행하다 실패하면 환불·회수·취소 업무를 실행하는 절차임
- **구체 예시**: 주문 생성 후 결제 승인 실패 시 Saga는 주문 상태를 `CANCELLED`로 바꾸고 재고 예약을 해제한다. 2PC는 재고·결제 DB가 prepared 상태로 대기한다.
- **흔한 오해·주의점**: Saga는 강한 일관성이 아니라 최종 일관성이다. 보상 트랜잭션이 비즈니스 의미상 완전한 원복인지 별도 검증해야 함

## 연결 개념
- Outbox Pattern - 이벤트 발행과 DB 갱신의 원자성 보완
- Eventual Consistency - 분산 시스템 정합성 모델
- Idempotency - 재시도 시 중복 처리 방지

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 2PC와 Saga의 정의보다 도메인 정합성, 장애 복구, 락 지속 시간 기준으로 선택한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 2PC는 Coordinator 기반 원자 커밋, Saga는 Local Transaction과 보상 트랜잭션의 연쇄이다.
> 2. **가치**: MSA에서 서비스별 DB 독립성과 비즈니스 정합성을 동시에 다루는 설계 판단 기준 제공.
> 3. **판단 포인트**: 금융 원장처럼 강한 일관성이 필요하면 2PC/단일 DB, 장기 업무 프로세스는 Saga를 선택한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 분산 트랜잭션 선택 역량 확인 | ACID, 최종 일관성, 보상 트랜잭션, Coordinator | Saga를 rollback과 동일하게 설명 |
| MSA 데이터 정합성 판단 확인 | DB per Service, Outbox, idempotency, 상태 머신 | 2PC 성능 저하만 쓰고 가용성·락 문제 누락 |
| 장애 복구 설계 확인 | 재시도, 중복 방지, 보상 실패, 관측성 | 실패 시나리오와 검증 지표 누락 |

> 요약: 이 문제는 "무엇이 더 낫다"가 아니라 업무 정합성 요구와 장애 복구 모델별 선택을 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 분산 트랜잭션 정합성 기법
- 배경: MSA는 서비스별 데이터 소유권 때문에 하나의 DB 트랜잭션으로 업무를 닫기 어렵다.
- 필요성: 주문·결제·재고 업무는 일관성 수준과 장애 복구 절차를 명시해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Business Request
  / 2PC: Coordinator -> Prepare Participants -> Commit/Rollback
  / Saga: Orchestrator/Choreography -> Local Tx -> Event -> Compensation
DB per Service -> Outbox -> Message Broker -> Observability
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Coordinator | 2PC prepare/commit 제어 | 단일 장애 지점과 락 지속 시간 관리 |
| Saga Orchestrator | 단계 순서와 보상 흐름 제어 | 중앙 상태 머신으로 추적 용이 |
| Local Transaction | 서비스 내부 DB 변경 | ACID 범위는 단일 서비스 |
| Compensation | 취소·환불·예약 해제 | 업무 의미상 보상 가능성 검증 |

> 요약: 2PC는 전역 커밋 제어, Saga는 서비스별 완료와 보상 흐름 제어가 구조의 중심이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Order Request -> Reserve Inventory -> Authorize Payment -> Create Shipment
  / Success -> Order Confirmed -> Event Publish
  / Failure -> Cancel Shipment -> Refund Payment -> Release Inventory
-> State/Audit Log Collect
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 업무 단계와 보상 단계 정의 | 상태 전이표 100% 작성 |
| 2 | Local Tx 수행 후 이벤트 발행 | Outbox 미발행 0건 |
| 3 | 실패 감지 후 보상 트랜잭션 실행 | 재시도 3회, DLQ 격리 |
| 4 | 최종 상태 확정과 감사 로그 기록 | saga_id 기준 추적 가능 |

> 요약: Saga는 성공 경로보다 실패 경로의 보상 순서와 중복 실행 방지가 설계의 핵심이다.

---

## Ⅳ. 특징

| 구분 | 2PC | Saga | 판단 수치 |
|:---|:---|:---|:---|
| 일관성 | 강한 원자 커밋 | 최종 일관성 | 정합성 허용 지연 1~5초 여부 |
| 장애 영향 | Participant prepared 상태 락 | 단계별 보상·재시도 | 락 지속 100ms 초과 시 2PC 부담 증가 |
| 적용 업무 | 짧은 DB 트랜잭션 | 장기 업무 프로세스 | 결제·배송처럼 외부 API 포함 시 Saga |
| 운영 복잡도 | Coordinator 복구 필요 | 상태 머신·보상 설계 필요 | saga failure rate 0.1% 이하 목표 |

> 요약: 2PC는 강한 일관성, Saga는 가용성과 업무 보상을 선택하는 구조이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | Saga vs 2PC | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단일 DB ACID | 서비스별 DB + 이벤트/Coordinator | 서비스 소유권 분리 여부 |
| 비용/성능 | 전역 락·동기 커밋 | 비동기 이벤트·보상 | p95 업무 완료 3초 이하, 락 최소화 |
| 운영/위험 | 커밋 실패 복구 | 보상 실패·중복 이벤트 | audit trail과 idempotency 필수 |

> 요약: 서비스별 DB와 외부 API가 있으면 Saga, 단일 데이터 경계와 강한 원자성이 핵심이면 2PC가 맞다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 보상 실패 | 환불 API 장애, 재고 해제 실패 | 재시도, DLQ, 수동 보정 큐 | compensation failure 0.1% 이하 |
| 중복 처리 | 메시지 재전송, 타임아웃 | idempotency key, unique constraint | duplicate reject count |
| 상태 불일치 | 이벤트 발행 누락 | Transactional Outbox, CDC | outbox lag 5초 이하 |

> 요약: Saga 운영은 보상 실패, 중복 처리, 이벤트 발행 누락을 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정합성 지연 | 최종 상태 도달 p95 3초 이하 | saga state metric |
| 실패 복구 | DLQ 15분 이내 처리 | broker, runbook |
| 감사성 | saga_id 기반 100% 추적 | distributed tracing, audit log |

> 요약: 성공 여부는 최종 상태 도달 시간, 실패 복구 시간, 업무 추적성으로 판정한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 업무 분류: 원장·잔액 차감은 단일 DB 또는 2PC, 주문·배송·알림은 Saga로 분리하고 정합성 허용 지연 3초 기준 설정
2. Saga 구현: Orchestration 상태 머신, Outbox, idempotency key, DLQ를 기본 구성으로 적용
3. 검증 체계: 보상 실패 0.1% 이하, outbox lag 5초 이하, saga_id 추적률 100%를 운영 지표로 등록

**결론 (2줄):**
- 기술사 판단: 강한 원자성이 업무 불변조건이면 2PC/단일 DB, 장기 업무 흐름과 서비스 자율성이 우선이면 Saga 선택
- 향후 방향: Event Sourcing, CDC, Workflow Engine을 결합해 보상 상태와 감사 추적을 자동화하는 방향으로 발전

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "분산 트랜잭션을 설명하시오" | 2PC와 Saga 흐름 비교 | 일관성·가용성·운영 복잡도 |
| 요구사항 명시형 | "MSA 정합성 방안을 제시하시오" | Outbox, 보상, idempotency 설계 | 업무별 선택 기준과 실패 대응 |

> 요약: 설명형은 원리 비교, 방안형은 업무 경계와 장애 복구 설계 중심으로 전환한다.
