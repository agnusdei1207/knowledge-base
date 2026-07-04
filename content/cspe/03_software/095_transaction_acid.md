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
- **개요**: ACID는 **트랜잭션(Transaction)**이 지켜야 할 4대 정합성 원칙 — 원자성(Atomicity)·일관성(Consistency)·격리성(Isolation)·지속성(Durability)이다.
- **왜 필요한가**: 계좌이체처럼 여러 SQL이 하나의 업무로 함께 끝나야 하는 작업에서, 중간에 장애가 나거나 여러 사용자가 동시에 손대면 잔액·재고·주문 상태가 어긋난다. ACID는 이런 상황에서도 데이터가 어긋나지 않게 하는 DBMS의 계약이다.
- **핵심 직관**: 트랜잭션은 "모두 반영하거나 모두 취소하는 계약서"이고, ACID 4요소는 그 계약서가 실제로 지켜지는지 검증하는 4가지 체크리스트다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 트랜잭션 (Transaction) | 여러 SQL을 하나의 논리적 업무 단위로 묶은 것 — ACID의 **상위 개념** | 송금 전표 한 장 (출금+입금을 한 건으로 처리) |
| 동시성 제어 (Concurrency Control) | 여러 트랜잭션이 동시에 실행될 때 서로 간섭하지 않게 조율하는 기법 — Isolation의 **상위 개념** | 교차로 신호등 |
| Atomicity (원자성) | 트랜잭션 내 모든 변경이 전부 반영되거나 전부 취소됨 | "All or Nothing" 스위치 |
| Consistency (일관성) | 트랜잭션 전후로 제약조건을 만족하는 상태만 허용됨 | 검문소를 통과한 상태만 인정 |
| Isolation (격리성) | 동시 실행 중인 트랜잭션이 서로의 미확정 변경에 간섭받지 않음 | 옆 칸 작업이 안 보이는 독립 작업실 |
| Durability (지속성) | Commit된 결과는 이후 장애가 나도 사라지지 않음 | 도장 찍힌 계약서는 불이 나도 사본이 남음 |
| Commit | 트랜잭션의 변경을 확정해 영구 반영하는 명령 | 계약서에 최종 서명 |
| Rollback | 트랜잭션의 변경을 모두 취소해 원상 복구하는 명령 | 서명 전 계약서를 찢어버림 |
| WAL (Write-Ahead Log) | 실제 데이터를 고치기 전에 "무엇을 바꿀지"를 먼저 로그로 기록하는 원칙 | 공사 전에 설계도부터 남겨 둠 |
| Undo Log | Rollback 시 되돌릴 "변경 전 값"을 기록한 로그 | 지우개 — 이전 상태로 되돌리는 기록 |
| Redo Log | 장애 후 Commit된 변경을 재실행할 "변경 후 값"을 기록한 로그 | 복사본 — 다시 그대로 그리는 기록 |
| Checkpoint | 그 시점까지의 변경을 디스크에 확실히 반영해 복구 시작점을 앞당기는 지점 | 저장 게임의 세이브 포인트 |
| 2PL (Two-Phase Locking) | 잠금 획득 단계와 해제 단계를 분리해 직렬 가능성을 보장하는 동시성 제어 기법 | 확장 단계엔 자물쇠만 걸고, 축소 단계에 들어가면 풀기만 함 |
| MVCC (Multi-Version Concurrency Control) | 값의 여러 버전을 유지해 읽기가 쓰기를 기다리지 않게 하는 기법 | 스냅샷 여러 장을 따로 보관 |

## 깊이 이해

### 왜 필요한가 (배경)
- DB는 항상 여러 사용자가 동시에 데이터를 수정하고 있고, 디스크 장애·전원 차단·네트워크 단절 같은 장애도 언제든 발생한다. SQL 문장 하나 단위로는 "여러 문장이 함께 성공해야 의미 있는 업무"를 표현할 수 없다 — 그래서 여러 SQL을 하나의 업무 단위(트랜잭션)로 묶고, 그 단위가 장애·동시 접근 속에서도 깨지지 않게 보장하는 ACID 원칙이 필요했다.

### 계좌이체 워크드 예제로 4요소 전부 이해하기
- A 계좌(잔액 30만원)에서 B 계좌(잔액 5만원)로 10만원을 이체한다고 하자. 트랜잭션은 두 SQL로 구성된다: ① `UPDATE account SET balance = balance - 100000 WHERE id='A'` ② `UPDATE account SET balance = balance + 100000 WHERE id='B'`.
- **Atomicity**: ①만 실행되고 ②가 실행되기 전 서버가 죽으면, A는 20만원인데 B는 그대로 5만원이라 총합이 10만원 증발한다. Atomicity는 이 상태를 허용하지 않고, 재시작 시 Undo Log를 이용해 ①까지도 되돌려 A를 다시 30만원으로 복구한다 — 부분 반영을 없앤다.
- **Consistency**: `balance >= 0` 제약이 있다고 하면, A 계좌 잔액이 5만원인데 10만원을 출금하려는 트랜잭션은 애초에 거부된다. 트랜잭션 전후로 항상 "제약을 만족하는 상태"만 존재한다.
- **Isolation**: 이체 트랜잭션이 진행 중(① 실행, ② 아직)일 때 다른 트랜잭션이 A 잔액을 조회하면, 격리 수준에 따라 "차감 전 30만원"만 보이게 하거나(Commit 전 값 비노출) "차감 후 20만원"이 보이지 않게 막는다 — 진행 중인 변경이 남에게 새어나가지 않게 한다.
- **Durability**: ②까지 실행 후 Commit이 성공적으로 응답을 반환했다면, 그 직후 정전이 나도 재시작 시 A=20만원, B=15만원 상태가 반드시 남아 있어야 한다. 이를 위해 Commit 전에 WAL에 변경 내용을 먼저 디스크로 flush(fsync)해 둔다.

### Durability가 실제로 어떻게 구현되는가 — WAL 선행 기록 원칙
- 순서는 항상 "① 로그를 디스크에 먼저 쓴다 → ② 그 다음 실제 데이터 페이지를 (나중에 여유 있을 때) 디스크에 쓴다"이다. 이를 WAL(Write-Ahead Logging) 원칙이라 한다.
- 왜 데이터를 먼저 안 쓰고 로그부터 쓰는가: 데이터 페이지는 크고 랜덤 위치에 흩어져 있어 매 Commit마다 쓰면 느리다. 반면 로그는 순차 추가(append-only)라 훨씬 빠르게 디스크에 반영할 수 있다. Commit 시점에는 로그만 확실히 디스크에 있으면, 장애가 나도 로그를 재생(Redo)해서 데이터 페이지를 나중에 복구할 수 있다.
- Checkpoint는 "이 시점 이전 로그는 이미 데이터 페이지에도 반영됐다"는 표시를 남겨, 장애 복구 시 Checkpoint 이후 로그만 재생하면 되게 해서 복구 시간을 줄인다.

### 장애 시점별 복구 — Undo와 Redo를 구분해서 이해하기
- Commit **전** 장애(트랜잭션이 진행 중이었음): 이미 기록된 로그를 거꾸로 적용해 변경을 되돌린다 → **Undo**.
- Commit **후** 장애(로그는 디스크에 있지만 데이터 페이지 반영 전 정전): 로그를 다시 적용해 변경을 재현한다 → **Redo**.
- 예: WAL에 "① A -100000 (미확정)", "② B +100000 (미확정)", "COMMIT" 순으로 기록된 후 정전됐다면, 재시작 시 COMMIT 로그가 있으므로 ①②를 Redo로 재실행해 최종 상태(A=20만, B=15만)를 만든다. 반대로 COMMIT 로그가 없다면 ①②를 Undo로 되돌려 원상태(A=30만, B=5만)로 만든다.

### 비유와 흔한 오해
- **비유**: 은행 직원이 송금 전표를 처리할 때 출금·입금·기록을 한 묶음으로 처리하고, 처리 중 정전이 나면 전표 로그를 보고 어디까지 처리됐는지 확인해 처음부터 다시 하거나 마저 완료하는 것과 같다.
- **오해**: ACID는 격리 수준(Isolation) 하나만 잘 고르면 완성되는 게 아니다. Atomicity는 Undo Log, Consistency는 제약조건 검사, Isolation은 Lock/MVCC, Durability는 WAL·Checkpoint — 4가지가 각각 별도의 메커니즘으로 구현되고 함께 동작해야 한다.

## 연결 개념
- 트랜잭션 격리 수준: Isolation을 4단계로 구체화한 ANSI SQL 표준
- 읽기 이상현상 (Read Anomalies): Isolation이 불완전할 때 발생하는 구체적 오류 현상
- 2PL·MVCC: 동시 실행 중 정합성을 지키는 대표 구현 기법

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
