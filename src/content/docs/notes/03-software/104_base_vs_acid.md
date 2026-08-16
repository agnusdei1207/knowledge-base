---
sidebar:
  order: 104
  label: "104. BASE vs ACID (BASE vs ACID)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "BASE vs ACID (BASE vs ACID)"
date: "2026-08-13T20:45:00+09:00"
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

- **ACID (Atomicity, Consistency, Isolation, Durability)**: 관계형 데이터베이스(RDBMS)의 트랜잭션 수용 모델로, 데이터의 무결성과 즉각적인 강한 일관성(Strict Immediate Consistency)을 최우선 보장하는 원칙.
- **BASE (Basically Available, Soft-state, Eventual Consistency)**: 분산 NoSQL 및 마이크로서비스(MSA)의 트랜잭션 모델로, 시스템의 고가용성(High Availability)과 수평 확장성(Scale-Out)을 위해 즉각적 일관성을 포기하고 최종 일관성(Eventual Consistency)을 지향하는 원칙.
- **Eventual Consistency (최종 일관성)**: 데이터 변경 후 일정 시간 지연(Replication Lag)이 발생할 수 있지만, 추가적인 변경이 없다면 시간이 흐름에 따라 결국 모든 노드의 데이터가 일치하게 되는 분산 상태.

</details>

- 정의/개념: 트랜잭션 보장 **ACID**와 분산 상태 모델 BASE의 비교
- 배경/필요성: 단일 원자 경계를 서비스 전체로 확장하면 **결합**•**지연** 증가

#### 한줄 요약

- 핵심 장부는 한 번에 정확히 고치고, 여러 사본은 잠시 달라도 나중에 맞출 수 있다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Basically Available**: 분산 노드 일부에 장애가 나도 시스템 전체가 멈추지 않고 가용 응답을 보장함.
- **Soft-State**: 외부 이벤트 전파 없이도 노드의 데이터 상태가 변경될 수 있음 (시간에 따른 일관성 변화).

</details>

- **ACID**: 즉시 일관성(`Strict Consistency`), 2PL/WAL 중심, RDBMS 기반 원자성 보장.
- **BASE**: 가용 상태•Soft State•최종 일관성을 설명하는 분산 모델
- **운영 Trade-off**: 비관적 락(`Pessimistic Locking`) 대 낙관적/비동기 수렴(`Optimistic/Asynchronous Convergence`).

#### 한줄 요약

- 아직 끝나지 않은 거래는 되돌리고 이미 끝난 분산 업무는 반대 작업으로 보정한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Compensating Transaction (보상 트랜잭션)**: BASE 모델에서 마이크로서비스 간 비동기 체인이 도중 실패했을 때, 이미 Commit된 이전 단계의 변경 사항을 원복(Undo)하기 위해 반대(Reverse) 연산 트랜잭션을 실행하는 기법.

</details>

| 모델 요소 | 의미 |
|:---|:---|
| ACID | 원자성•일관성•격리성•지속성 보장 |
| Basically Available | 일부 기능 저하 중에도 가용 응답 유지 |
| Soft State | 비동기 전파 중 복제 상태가 시간에 따라 변화 |
| Eventual Consistency | 추가 변경이 없으면 복제본이 최종 수렴 |

#### 한줄 요약

- 원장을 먼저 확정하고 검색•알림 사본은 이벤트로 뒤따라 맞춘다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Transactional Outbox Pattern**: ACID DB에 로컬 비즈니스 데이터와 아웃박스(Outbox) 이벤트 테이블을 단일 트랜잭션으로 커밋한 후, CDC(Debezium)나 Poller가 이를 비동기 전파하는 패턴.

</details>

```text
[업무 변경 요청]
       │
       ▼
1. 로컬 원자 커밋
       │
       ▼
2. 아웃박스 이벤트 발행
       │
       ▼
3. 멱등 이벤트 처리
       │
       ▼
4. 파생 상태 갱신
       │
       ▼
5. 수렴 상태 확인
       │
       ▼
   [처리 완료]
```

### 동작 원리

1. 로컬 원자 커밋: 업무 데이터와 이벤트를 함께 확정
2. 아웃박스 이벤트 발행: CDC•폴러가 브로커로 전달
3. 멱등 이벤트 처리: 중복 키 검사 후 한 번만 반영
4. 파생 상태 갱신: 각 서비스의 로컬 상태 변경
5. 수렴 상태 확인: 지연•실패•재처리 결과 감시

#### 한줄 요약

- 원장은 먼저 정확히 확정하고 검색•알림 같은 사본은 확인 가능한 이벤트로 뒤따라 맞춘다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Consistency Tradeoff**: 계좌 이체, 주식 체결 등 1원이라도 틀리면 안 되는 핵심 도메인은 ACID, 좋아요 수, SNS 피드, 장바구니 등은 BASE 수용.

</details>

| 비교 항목 | ACID (전통적 모델) | BASE (현대적 분산 모델) |
|:---|:---|:---|
| 시스템 우선순위 | **트랜잭션 불변식 보장** | **분산 가용 상태•최종 수렴** |
| 트랜잭션 경계 | 단일 DB 스키마 단위 | **다중 마이크로서비스 (MSA) 도메인 단위** |
| 쿼리 일관성 수준 | Strict Read (항상 최신값 조회) | Stale Read 허용 (시간차 최신값 반영) |
| 대표적 도메인 | **금융 뱅킹, 계좌 이체, 주식 결제, 수량 관리**| **SNS 피드, 스트리밍, 장바구니, 로그 수집** |

#### 한줄 요약

- 결제 원장은 즉시 맞추고 알림•검색 사본은 재시도하며 뒤따라 맞춘다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Idempotent Consumer (멱등 수신기)**: 비동기 메시지가 중복 수신(At-Least-Once)되더라도 멱등 키(Idempotency Key)를 검사하여 중복 갱신을 차단하는 설계.

</details>

| 2대 비동기 난제 | 발생 원인 및 위험 요소 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. Message Loss (메시지 유실) | 비동기 이벤트 전파 중 브로커 다운 | **Transactional Outbox Pattern & CDC 적용** |
| 2. Duplicate Message | 네트워크 재시도로 중복 메시지 수신 | **Idempotency Key 및 Unique Constraint 적용** |
| 3. Saga Failure | 비동기 연쇄 처리 중 중간 단계 실패 | **보상 트랜잭션 (Compensating Transaction) 자동화**|

> 사례: **배달의민족 주문-결제(ACID) 및 라이더 배차-알림(BASE) 분리 아키텍처**

#### 한줄 요약

- 돈과 재고는 먼저 정확히 확정하고, 늦어도 되는 사본만 비동기로 갱신한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **트랜잭션 수립 기준(Transaction Architecture Standards)**: 무결성 요구 수준, 서비스 가용성 SLA, MSA 분산 구조 및 Polyglot Persistence에 의거한 체계.

</details>

- 즉시 불변식은 **ACID**, 지연 허용 파생 상태는 BASE 적용

#### 한줄 요약

- ACID•BASE 적용 기준은 지금 맞아야 할 값과 나중에 맞아도 될 값을 구분한다.
