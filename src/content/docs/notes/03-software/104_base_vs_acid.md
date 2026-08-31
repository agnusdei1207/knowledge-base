---
sidebar:
  order: 104
  label: "104. BASE vs ACID"
  badge:
    text: "기출 · 50%"
    variant: note
title: "BASE vs ACID (BASE vs ACID)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-software"
weight: 104
extra:
  question_no: "104"
  source_status: "기출"
  source_history: "131회"
  priority: 50
  priority_note: "131회 기출, ACID•BASE 선택 기준 명확"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **ACID vs BASE**: 원자적 즉각 정합성을 보장하는 ACID(관계형 모델)와 기본 가용성(BA), 유연한 상태(S), 최종 일관성(E)을 지향하는 BASE(분산 모델).
- **2PC(Two-Phase Commit)**: 분산 환경에서 ACID를 구현하기 위한 코디네이터 기반 2단계 커밋 프로토콜 (락 경합 및 단일 장애점 병목 존재).

</details>

- 정의/개념: 데이터 트랜잭션 모델에서 **강한 일관성 중심의 ACID와 분산 고가용성·최종일관성 중심의 BASE**를 비교·결합하는 정합성 패러다임
- 배경/필요성: 마이크로서비스(MSA) 및 대규모 분산 환경에서 전통적인 ACID 트랜잭션과 2PC(2-Phase Commit)를 강제할 경우 발생하는 극심한 락 블로킹, 단일 장애점(SPOF) 병목 및 가용성 저하 문제를 극복하고, 개별 서비스 내부는 로컬 ACID로 즉각적 정합성을 보장하되 서비스 간에는 기본 가용성(Basically Available), 유연한 상태(Soft-State), 최종 일관성(Eventual Consistency) 중심의 BASE 패러다임을 결합하여 **시스템의 초고가용성과 분산 데이터 정합성을 동시에 달성**할 필요

#### 한줄 요약
- ACID와 BASE는 우열이 아니라 정합성을 커밋 시점에 확정할지 수렴 이후로 미룰지의 차이이므로, 도메인 경계마다 잠금 대기 비용과 불일치 노출 비용 중 어느 쪽을 감당할 수 있는지가 선택 기준이 된다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Eventual Consistency(최종 일관성)**: 일시적인 복제 지연이 존재하더라도 추가 변경이 없으면 일정 시간 후 모든 분산 노드의 데이터가 일치하게 수렴.
- **Compensating Transaction(보상 트랜잭션)**: 분산 Saga 트랜잭션 중 중간 단계 실패 시 이미 커밋된 이전 단계들을 원복하기 위해 실행하는 취소 트랜잭션.

</details>

- 금융/결제 등 엄격한 정합성을 위한 **즉각적 강한 일관성(Strict ACID)**
- 대규모 트래픽과 서비스 독립성을 위한 **최종 일관성 및 고가용성(BASE)**
- 트랜잭셔널 아웃박스(Transactional Outbox) 및 Saga 패턴을 통한 **비동기 이벤트 수렴**

#### 한줄 요약
- ACID의 무결성과 BASE의 가용성을 분리 적용하여 신뢰성과 성능을 양립한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Transactional Outbox & Saga**: 비즈니스 DB에 이벤트를 함께 커밋(ACID)한 뒤 Kafka CDC를 통해 타 서비스로 비동기 전파(BASE)하는 구조.

</details>

```text
[ACID + BASE 하이브리드 아키텍처]
|-- 1. 주문 서비스 (Order Service: 단일 DB Local ACID 트랜잭션)
|   |-- Order Table Insert + Outbox Table Insert (단일 트랜잭션 원자 커밋)
|   `-- CDC 커넥터 (Debezium -> Kafka 이벤트 브로커로 무손실 발행)
`-- 2. 후속 분산 서비스 (BASE 최종 일관성 수렴)
    |-- 결제 서비스 (Payment: 멱등성 보장 컨슈머 + 로컬 DB 반영)
    |-- 배송 서비스 (Delivery: 주문 이벤트 수신 후 배송 준비)
    `-- 실패 시 보상 트랜잭션 (Saga Compensating Event 발행으로 주문 취소)
```

선의 의미: 계층 및 단일 서비스의 ACID 확정과 분산 서비스 간의 BASE 비동기 수렴 구조

| 구성요소 | 책임 |
|:---|:---|
| ACID | 로컬 트랜잭션의 **즉각적 정합성 보장** |
| Basically Available | 장애 중 **서비스 응답 유지** |
| Soft-State | 복제 중 **과도기 상태 허용** |
| Eventual Consistency | 분산 데이터의 **최종 수렴** |

#### 한줄 요약
- 로컬 커밋은 즉시 확정되지만 그 사실이 다른 서비스에 도달하기 전까지 시스템 전체는 불일치 상태에 놓이므로, BASE 구간의 설계 품질은 그 불일치가 지속되는 시간을 얼마나 짧게 만드느냐로 판정된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Outbox 기반 BASE 수렴 절차**: 로컬 원자 커밋 $\to$ CDC 이벤트 발행 $\to$ 멱등 컨슈머 처리 $\to$ 최종 일관성 달성.

</details>

```text
클라이언트가 주문 결제 요청
        │
   [주문 서비스 ACID] Order + Outbox 테이블에 로컬 원자 커밋 (단일 DB)
        │
   [CDC 이벤트 발행] Debezium이 Outbox 로그를 감지하여 Kafka Topic으로 발행
        │
   [결제 서비스 BASE] Kafka 메시지 수신 후 멱등성(Idempotency Key) 검사
        │
   결제 외부 PG사 호출이 성공했는가?
   ┌────┴───────────────────────────┐
  예 (결제 성공)                    아니오 (결제 실패)
   │                                 │
[결제 완료 상태 로컬 저장]          [Saga 보상 트랜잭션]
배송 서비스로 이벤트 전달         '주문 취소' 보상 이벤트 발행하여
(최종 일관성 수렴 완료)           주문 상태를 CANCELLED로 원복
```

#### 한줄 요약
- 성공 경로는 이벤트 수렴으로 끝나지만 실패 경로는 이미 커밋된 로컬 변경을 롤백할 수 없어 업무 로직으로 되돌리는 보상 트랜잭션을 요구하므로, BASE의 진짜 비용은 지연이 아니라 보상 설계에 있다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **ACID vs BASE 비교**: 즉각적 강한 일관성의 RDBMS(ACID)와 가용성 및 최종 일관성 중심의 분산 시스템(BASE).

</details>

| 비교 항목 | ACID (전통적 관계형 모델) | BASE (현대적 분산 MSA 모델) |
|:---|:---|:---|
| 일관성 모델 | **강한 일관성 (Strict Consistency)** | **최종 일관성 (Eventual Consistency)** |
| 동시성 제어 | 2PL 락 잠금, MVCC 스냅샷 | 분산 이벤트, 타임스탬프, 멱등 컨슈머 |
| 분산 확장성 | 수직 확장(Scale-up), 분산 2PC 오버헤드 큼 | **수평 확장(Scale-out) 및 고가용성에 최적화** |
| 주 활용 분야 | **은행 계좌, 결제 원장, 증권 거래** | **SNS 피드, 쇼핑몰 장바구니, 알림 시스템** |

#### 한줄 요약
- 정밀 금융 도메인은 ACID, 대규모 분산 확장 도메인은 BASE 모델을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Idempotency Key(멱등키)**: 네트워크 재시도로 중복 전달된 메시지에 대해 1회만 처리되도록 보장하는 고유 식별자.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 비동기 메시지 전파 중 브로커 다운으로 메시지 유실 | **Transactional Outbox Pattern 및 Debezium CDC 적용** | 이벤트 발행의 원자성 및 유실 0 보장 |
| 네트워크 재시도로 인한 중복 메시지 수신 (At-Least-Once) | **Idempotency Key 검증 및 Unique 제약조건 기반 멱등 컨슈머 구현** | 중복 결제 및 중복 차감 원천 방지 |
| 분산 연쇄 처리 중 특정 서비스 실패로 인한 정합성 파괴 | **Saga Pattern(오케스트레이션) 기반 보상 트랜잭션 자동화** | 실패 시 이전 완료 단계 자동 원복 |
| 데이터 수렴 지연으로 사용자가 화면에서 미반영 확인 | **프론트엔드 Optimistic UI 반영 또는 폴링/웹소켓 상태 알림** | 사용자 경험(UX) 왜곡 방지 |

#### 한줄 요약
- 아웃박스 패턴, 멱등 컨슈머, Saga 보상 트랜잭션, Optimistic UI로 분산 정합성을 완성한다.

## Ⅶ. 결론

- 현대 분산 클라우드 아키텍처 및 마이크로서비스(MSA) 영속성 설계의 **양대 핵심 트랜잭션 패러다임**으로 확립되었으며, 실무 아키텍처 구현 시에는 **단일 서비스 내부 원장은 Strict ACID로 견고히 보호하고, 서비스 간 분산 트랜잭션은 Transactional Outbox 및 Saga 패턴(보상 트랜잭션) 기반의 비동기 BASE 모델로 수렴시키는 하이브리드 전략**을 수립하여 가용성과 정합성의 최적 균형을 실현

#### 한줄 요약
- ACID(로컬 정합성)와 BASE(분산 가용성)는 상호 대립이 아닌 상호 보완재이며, 도메인 경계에 따른 조화로운 결합이 현대 분산 시스템의 정석이다.
