---
title: "트랜잭션 ACID (Transaction ACID)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 95
---

# 📖 【암기용】 개념 완전 이해

> 목적: 트랜잭션 ACID를 처음 보는 사람도 Commit·Rollback·WAL·복구의 관계를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 여러 데이터 변경을 하나의 업무 단위로 묶어 정합성을 지키는 4대 원칙
- **왜 필요한가**: 계좌이체처럼 한쪽 차감과 다른 쪽 증가가 함께 끝나야 하는 업무에서 중간 실패는 데이터 불일치를 만든다.
- **핵심 직관**: 트랜잭션은 "모두 반영하거나 모두 취소하는 계약"이고, ACID는 그 계약을 지키는 검증 항목이다.

## 깊이 이해
- **배경·문제의식**: DB는 동시에 여러 사용자가 수정하고, 디스크·전원·네트워크 장애가 발생한다. SQL 한 문장보다 큰 업무 단위를 보존하지 않으면 잔액·재고·주문 상태가 어긋난다.
- **작동 원리**: Atomicity는 Commit 전 변경을 Rollback 가능하게 하고, Consistency는 제약조건을 통과한 상태만 허용한다. Isolation은 동시 트랜잭션의 간섭을 통제하고, Durability는 Commit 후 WAL과 Flush로 장애 후 재실행 가능성을 남긴다.
- **비유**: 은행 직원이 송금 전표를 처리할 때 출금·입금·기록을 한 묶음으로 처리하고, 중간에 정전이 나면 전표 로그로 처음부터 복구하는 방식과 같다.
- **구체 예시**: A 계좌 10만원 차감 후 B 계좌 10만원 증가 전 장애가 나면 Rollback 또는 Redo/Undo 로그로 두 계좌 합계가 변하지 않게 복구한다.
- **흔한 오해·주의점**: ACID는 격리 수준 하나로 완성되지 않는다. 로그, 잠금, MVCC, 제약조건, 복구 정책이 함께 구성되어야 한다.

## 연결 개념
- 트랜잭션 격리 수준 - Isolation의 구체 구현 선택
- WAL - Durability와 장애복구의 기반 로그 구조
- 2PL·MVCC - 동시 실행 중 정합성을 지키는 대표 기법

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. ACID 4요소를 장애복구·동시성 제어·무결성 검증과 연결한다.
> 핵심: ACID 답안은 용어 암기가 아니라, Commit 전후 장애 시점별 DBMS 처리를 설명해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 트랜잭션 ACID는 원자성·일관성·격리성·지속성으로 업무 단위 변경의 정합성을 보장하는 원칙이다.
> 2. **가치**: Commit·Rollback·WAL·Lock/MVCC로 동시 수정과 장애 후 복구를 제어한다.
> 3. **판단 포인트**: 업무별 정합성 요구, 격리 수준, 로그 Flush 정책, 복구 목표(RPO/RTO)를 함께 선택해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| ACID 4요소 이해 확인 | Atomicity, Consistency, Isolation, Durability | 각 요소를 한글 풀이만 쓰고 구현 기법 누락 |
| 장애복구 메커니즘 확인 | WAL, Undo, Redo, Checkpoint, Commit Log | Commit 전 장애와 Commit 후 장애 구분 누락 |
| 동시성·정합성 판단 확인 | Lock, MVCC, Isolation Level, Constraint | Isolation만 설명하고 Consistency·Durability 누락 |
> 요약: ACID 문제는 4요소를 복구 로그와 동시성 제어 흐름으로 연결해야 득점 가능하다.

---

## Ⅰ. 개요 및 필요성

- 개요: ACID는 트랜잭션 정합성 원칙이다.
- 배경: 여러 SQL이 하나의 업무 단위로 실행될 때 중간 장애나 동시 수정이 발생하면 잔액, 주문, 재고 상태가 어긋난다.
- 필요성: Commit, Rollback, WAL, Lock/MVCC로 금융·주문·재고 OLTP의 원자성, 격리성, 지속성을 보장해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Transaction Request -> SQL Set -> Concurrency Control
  / Atomicity -> Undo Log
  / Isolation -> Lock / MVCC
Constraint Check -> WAL -> Commit / Rollback -> Recovery
```

| 구성요소 | 역할 | 구현 수단 |
|:---|:---|:---|
| Atomicity | 전부 반영 또는 전부 취소 | Undo Log, Rollback Segment |
| Consistency | 제약조건 만족 상태만 허용 | PK/FK/CHECK, Trigger |
| Isolation | 동시 트랜잭션 간 간섭 통제 | 2PL, MVCC, Snapshot |
| Durability | Commit 후 결과 보존 | WAL, fsync, Checkpoint |
| Transaction Manager | 상태 전이 관리 | Active, Committed, Aborted |
> 요약: ACID는 로그·잠금·제약조건·복구 관리자가 함께 수행하는 DBMS 정합성 메커니즘이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Begin -> SQL Execute -> Undo/WAL Record
-> Constraint Check -> Lock/MVCC Validation
-> Commit Flush / Rollback Undo -> Checkpoint / Recovery
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Begin 후 트랜잭션 ID와 상태 생성 | Active 상태 등록 |
| 2 | 변경 전 이미지와 Redo 로그 기록 | WAL 선기록 원칙 |
| 3 | 제약조건과 격리 규칙 검사 | FK 위반 0건, 충돌 대기 |
| 4 | Commit 시 로그 Flush 후 결과 확정 | Commit Log 디스크 반영 |
| 5 | 장애 후 Undo/Redo 수행 | RPO 0 또는 정책값 충족 |
> 요약: 트랜잭션은 변경 전 로그 기록, 검증, Commit 로그 확정, 장애 후 Undo/Redo 순서로 ACID를 구현한다.

---

## Ⅳ. 특징

| 구분 | 미적용 처리 | ACID 트랜잭션 | 정량·판단 기준 |
|:---|:---|:---|:---|
| 장애 처리 | 중간 변경 잔존 가능 | Rollback·Redo로 복구 | Commit 전 Undo, Commit 후 Redo |
| 동시 처리 | 갱신 충돌 노출 | Lock/MVCC로 격리 | Deadlock rate, conflict retry |
| 무결성 | 애플리케이션 검사 의존 | DB 제약조건 검사 | Constraint violation 0건 |
| 지속성 | 메모리 반영 후 손실 가능 | WAL Flush 후 Commit | fsync latency, RPO 목표 |
> 요약: ACID는 업무 단위 변경을 장애 시점과 동시성 충돌에 관계없이 일관된 상태로 수렴시킨다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단일 SQL 자동 Commit | 명시적 트랜잭션 | 다중 테이블 변경과 보상 불가 업무 |
| 비용/성능 | 로그 Flush 최소 | WAL·Lock·검증 비용 발생 | p95 Commit latency, TPS 목표 |
| 운영/위험 | Eventual Consistency | Strong Consistency | 금융·재고·주문 상태 불일치 허용 여부 |
> 요약: ACID는 로그와 잠금 비용을 감수하고 업무 불일치 비용을 줄여야 하는 OLTP에 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Commit 지연 | WAL Flush와 동기 복제 | Group Commit, SSD, Sync 정책 조정 | p95 Commit latency |
| 교착상태 | 잠금 순서 불일치 | Lock ordering, timeout, retry | Deadlock count/hour |
| 장기 트랜잭션 | Lock 보유와 Undo 증가 | 트랜잭션 범위 축소, Batch 분할 | 평균 transaction duration |
> 요약: ACID 리스크는 Commit 지연, 교착상태, 장기 트랜잭션이며 로그·잠금·업무 범위 조정으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 원자성 | 장애 주입 후 부분 반영 0건 | Fault Injection, 데이터 합계 검증 |
| 지속성 | Commit 손실 0건, RPO 0~15분 | WAL 복구 테스트 |
| 격리성 | Dirty Read 0건, Lost Update 0건 | 동시성 테스트, Jepsen 유형 검증 |
> 요약: ACID 검증은 장애 주입, 로그 복구, 동시성 충돌 재현으로 수치화한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 트랜잭션 경계: 계좌이체·주문확정·재고차감처럼 보상 불가 업무는 단일 DB 트랜잭션으로 묶고 평균 수행시간 500ms 이하로 제한함
2. 로그·복구: WAL 아카이빙과 주기 Checkpoint를 설정하고 월 1회 장애 주입으로 RPO 15분·RTO 30분 검증함
3. 동시성 제어: 기본 Read Committed, 재고 차감은 Repeatable Read 또는 Serializable로 격상하고 Deadlock retry 3회 정책 적용함

**결론 (2줄):**
- 기술사 판단: 금전·재고처럼 불일치 비용이 큰 업무는 ACID를 우선하고, 분석·로그성 데이터는 완화된 정합성 모델을 병행함
- 향후 방향: 분산 트랜잭션보다 Saga·Outbox·Idempotency를 조합해 서비스 경계별 정합성을 설계하는 방향임

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "ACID를 설명하시오" | 4요소와 Commit/Rollback/WAL 흐름 | 장애복구·동시성 제어 사례 |
| 요구사항 명시형 | "장애복구 방안을 제시하시오", "격리성과 비교하시오" | 장애 시점별 Undo/Redo 또는 격리 수준 매핑 | RPO/RTO, Commit 지연, 잠금 비용 선택 기준 |
> 요약: 설명형은 4요소 전체, 방안형은 장애 시점과 복구 지표 중심으로 목차를 전환한다.
