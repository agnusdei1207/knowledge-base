---
title: "트랜잭션 격리 수준 4단계 (Transaction Isolation Levels)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 96
---

# 📖 【암기용】 개념 완전 이해

> 목적: 트랜잭션 격리 수준을 처음 보는 사람도 Read Uncommitted부터 Serializable까지의 차이를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 트랜잭션 격리 수준은 **동시성 제어(Concurrency Control)**에서 여러 트랜잭션이 서로의 변경을 얼마나 볼 수 있는지 정하는 **ANSI SQL 표준 4단계**(Read Uncommitted → Read Committed → Repeatable Read → Serializable)다.
- **왜 필요한가**: 모든 트랜잭션을 완전히 직렬(한 번에 하나씩)로 실행하면 정합성은 완벽하지만 대기 시간이 커져 처리량이 떨어진다. 반대로 격리를 낮추면 처리량은 늘지만 Dirty Read·Phantom Read 같은 읽기 이상이 생긴다. 격리 수준은 이 둘 사이의 손잡이다.
- **핵심 직관**: 격리 수준은 "남이 지금 고치고 있는 장부를, 확정되기 전까지 어디까지 보여줄 것인가"를 정하는 4단계 눈금이다 — 많이 보여줄수록 빠르지만 위험하고, 적게 보여줄수록 느리지만 안전하다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 동시성 제어 (Concurrency Control) | 여러 트랜잭션이 동시에 실행될 때 결과가 어긋나지 않게 조율하는 기법 — 격리 수준의 **상위 개념** | 교차로 신호 체계 |
| ACID의 Isolation | 트랜잭션이 서로 간섭받지 않아야 한다는 ACID 4원칙 중 하나 — 격리 수준은 이를 **4단계로 구체화**한 것 | 원칙(격리성)을 실제 손잡이(격리 수준)로 만든 것 |
| Read Uncommitted | 다른 트랜잭션이 아직 Commit하지 않은 값도 읽을 수 있는 가장 낮은 격리 | 옆 사람이 쓰다 만 초안까지 훔쳐봄 |
| Read Committed | 다른 트랜잭션이 Commit을 완료한 값만 읽는 격리 (문장 단위 스냅샷) | 최종 저장본만 봄, 저장 중간은 안 보임 |
| Repeatable Read | 트랜잭션 시작 시점 기준으로, 같은 행을 다시 읽어도 항상 같은 값이 보장되는 격리 (트랜잭션 단위 스냅샷) | 내가 처음 읽은 페이지를 고정해서 계속 그 버전만 봄 |
| Serializable | 동시 실행 결과가 어떤 직렬(순차) 실행 순서와 동일하도록 보장하는 가장 높은 격리 | 한 줄로 줄 세워 한 명씩 처리한 것과 같은 결과 |
| MVCC (Multi-Version Concurrency Control) | 값의 여러 버전을 동시에 보관해 읽기가 쓰기를 기다리지 않게 하는 구현 방식 | 서로 다른 시점의 스냅샷 사진첩 |
| 2PL (Two-Phase Locking) | 잠금을 확장 단계에 걸고 축소 단계에만 푸는 방식으로 직렬 가능성을 보장하는 구현 기법 | 회의 중엔 자료 잠그고 끝나야 풀어줌 |
| Snapshot Isolation | 트랜잭션 시작 시점 스냅샷만 보고, 먼저 Commit한 쪽이 이기는 MVCC 기반 격리 구현 | 내가 시작한 시점 사진 한 장만 보고 작업 |
| Dirty Read | 미확정(Rollback 가능) 값을 읽는 현상 | 옆 사람이 취소할 수도 있는 초안을 읽음 |
| Non-Repeatable Read | 같은 행을 두 번 읽었는데 값이 달라지는 현상 | 아까 본 문장이 다시 보니 바뀌어 있음 |
| Phantom Read | 같은 조건으로 다시 조회했는데 행 개수(집합)가 달라지는 현상 | 아까 목록에 없던 항목이 새로 나타남 |
| Lost Update | 두 트랜잭션의 갱신 중 하나가 덮어써져 사라지는 현상 | 동시에 고친 문서에서 한쪽 수정이 사라짐 |

## 깊이 이해

### 왜 4단계로 나뉘었나 (배경)
- OLTP 시스템은 수백~수천 TPS로 동시에 같은 데이터를 읽고 쓴다. "완전히 안전하게(Serializable)"만 고집하면 잠금 대기·충돌 재시도가 늘어 처리량이 급감하고, "무조건 빠르게(Read Uncommitted)"만 고집하면 잘못된 값을 근거로 업무를 처리하게 된다. ANSI SQL은 이 트레이드오프를 4단계로 표준화해 업무 성격에 맞게 고를 수 있게 했다.

### 4단계를 계좌 잔액 100만원 예제로 순서대로 이해하기
- 전제: T1이 `balance=100`인 계좌를 다루는 도중, T2가 같은 계좌에 10을 더해 `balance=110`으로 Commit하려 한다.
- **Read Uncommitted**: T2가 아직 Commit하지 않고 `balance=110`으로만 바꿔 둔 순간에도 T1이 조회하면 110이 보인다. 만약 T2가 이후 Rollback하면 T1은 존재한 적 없는 값(Dirty Read)을 근거로 판단한 것이 된다.
- **Read Committed**: T1은 T2가 Commit을 완료하기 전까지는 100만 본다. T2가 Commit하는 순간 T1이 다시 조회하면 110으로 바뀌어 보인다 — 조회할 때마다(문장 단위) 최신 Commit 값을 새로 스냅샷하기 때문에, 같은 트랜잭션 안에서도 두 번 읽은 값이 다를 수 있다(Non-Repeatable Read).
- **Repeatable Read**: T1이 트랜잭션을 시작한 시점(예: balance=100)의 스냅샷을 고정해서, T2가 그 사이 Commit해도 T1은 트랜잭션이 끝날 때까지 계속 100을 본다. 같은 행의 값은 보장되지만, `WHERE amount > 50`처럼 범위 조회를 하면 T2가 새로 삽입한 행이 뒤늦게 나타날 수 있다(Phantom Read, DBMS 구현에 따라 다름).
- **Serializable**: T1과 T2가 동시에 실행돼도, 마치 T1 → T2 또는 T2 → T1 순서로 하나씩 실행한 것과 똑같은 최종 결과만 허용한다. 이를 위해 범위 전체에 Predicate Lock을 걸거나(2PL 기반), Commit 시점에 충돌을 감지해 하나를 실패시킨다(SSI, Serializable Snapshot Isolation).

### 구현 방식 — Lock 기반 vs MVCC 기반
- 잠금 기반(2PL): 읽기·쓰기 시 실제로 잠금을 걸어 다른 트랜잭션의 접근을 대기시킨다. 정확하지만 대기 시간이 늘어난다.
- MVCC 기반: 값의 여러 버전을 보관해 "읽기는 잠금 없이, 자신이 볼 자격이 있는 버전만" 읽게 한다. PostgreSQL·MySQL InnoDB·Oracle이 널리 사용하며, 읽기가 쓰기를 막지 않아 처리량이 높다. 다만 두 트랜잭션이 서로 다른 조건으로 동시에 갱신하면 Write Skew(각자 조건은 만족했지만 합쳐서 보면 규칙 위반)가 생길 수 있다.

### 재고 1개 동시 구매 워크드 예제
- 재고가 1개 남은 상품을 두 사용자가 거의 동시에 `SELECT stock` 후 `stock=stock-1` 방식으로 처리한다고 하자. Read Committed에서는 두 트랜잭션이 모두 "재고 1"을 읽고 각각 0으로 갱신할 수 있어 재고가 -1(또는 이중 판매)이 될 수 있다(Lost Update).
- 해결: `UPDATE product SET stock = stock - 1 WHERE id=1 AND stock > 0` 같은 조건부 UPDATE를 쓰면 두 번째 트랜잭션은 조건이 거짓이 되어 실패하고, 애플리케이션이 이를 감지해 "품절"로 처리한다. 또는 Serializable로 격상해 DBMS가 충돌을 감지하게 할 수도 있다.

### 비유와 흔한 오해
- **비유**: 공동 문서 편집에서, 임시 저장본까지 보는지(RU), 저장 완료본만 보는지(RC), 내가 처음 열었을 때 문단을 고정해서 보는지(RR), 아예 한 명씩 순서대로 편집하게 줄 세우는지(Serializable)의 차이다.
- **오해**: Repeatable Read가 항상 Phantom Read를 막는 것은 아니다 — ANSI 표준상으로는 RR에서 Phantom이 허용되지만, MySQL InnoDB는 Next-Key Lock이라는 자체 구현으로 많은 Phantom 상황을 추가로 차단한다. 반대로 PostgreSQL의 Snapshot Isolation은 Dirty/Non-Repeatable/Phantom을 막아도 Write Skew는 막지 못할 수 있다. 즉 이름이 같아도 DBMS마다 실제 보장 범위가 다르므로 반드시 대상 DBMS 문서를 확인해야 한다.

## 연결 개념
- Read Anomalies (읽기 이상현상): 격리 수준이 낮을 때 실제로 관찰되는 4가지 현상
- MVCC: 읽기 잠금 없이 Snapshot을 제공하는 구현 방식
- 2PL: 잠금 기반으로 직렬 가능성을 보장하는 구현 방식
- 트랜잭션 ACID: 격리 수준이 구체화하는 상위 원칙(Isolation)

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 격리 수준별 허용 이상현상과 Lock/MVCC 구현 차이를 함께 제시한다.
> 핵심: 격리 수준 답안은 4단계 암기가 아니라 업무 위험에 맞는 선택 기준을 제시해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 트랜잭션 격리 수준은 동시 실행 트랜잭션 간 읽기·쓰기 가시성과 충돌 제어 강도를 정하는 단계이다.
> 2. **가치**: Dirty Read, Non-Repeatable Read, Phantom Read, Lost Update를 업무 허용 범위에 맞게 통제한다.
> 3. **판단 포인트**: 정합성 위험, 잠금 대기, MVCC 버전 보관, 재시도 비용을 함께 고려해 수준을 선택한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| ANSI SQL 격리 수준 이해 확인 | RU, RC, RR, Serializable | 단계 이름만 나열하고 읽기 이상 매핑 누락 |
| 동시성 제어 선택 역량 확인 | Lock 기반 vs MVCC Snapshot | DBMS별 구현 차이를 일반 원칙처럼 단정 |
| 실무 트레이드오프 판단 확인 | 정합성 위험, TPS, 대기 시간, 재시도 | Serializable을 모든 업무에 적용한다고 작성 |
> 요약: 격리 수준 문제는 이상현상 방지 범위와 구현 비용을 표로 연결해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 격리 수준은 트랜잭션 가시성 규칙이다.
- 배경: 다수 사용자가 같은 데이터를 동시에 접근하면 Dirty Read, Non-Repeatable Read, Phantom Read, Lost Update가 발생한다.
- 필요성: 업무별 오류 허용 범위와 TPS 목표에 맞춰 Read Committed, Repeatable Read, Serializable을 선택해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Concurrent Transactions -> Isolation Policy
  / Read Uncommitted -> Dirty Read 허용
  / Read Committed -> Commit 데이터만 읽기
  / Repeatable Read -> 동일 행 반복 읽기 유지
  / Serializable -> 직렬 실행과 동등
Lock / MVCC -> Anomaly Control -> Commit / Retry
```

| 격리 수준 | 허용 가능 이상현상 | 대표 구현 |
|:---|:---|:---|
| Read Uncommitted | Dirty Read 가능 | 잠금 검사 최소 |
| Read Committed | Non-Repeatable, Phantom 가능 | Statement Snapshot, 짧은 Shared Lock |
| Repeatable Read | Phantom 가능 여부 DBMS 의존 | Transaction Snapshot, Next-Key Lock |
| Serializable | Dirty/Non-Repeatable/Phantom 차단 | Predicate Lock, SSI, Strict 2PL |
| Snapshot Isolation | Dirty Read 차단, Write Skew 가능 | MVCC Snapshot, First-Committer-Wins |
> 요약: 격리 수준은 읽기 가시성 규칙이며, DBMS는 Lock 또는 MVCC로 각 단계의 이상현상을 통제한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Transaction Begin -> Isolation Level Set -> Read Snapshot / Lock Acquire
-> SQL Execute -> Conflict Detect
-> Commit Validation -> Commit / Abort / Retry
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 트랜잭션 시작과 격리 수준 설정 | 세션·트랜잭션 설정값 확인 |
| 2 | 읽기 시점 결정 | Statement 또는 Transaction Snapshot |
| 3 | 쓰기 충돌 탐지 | Row Lock, Version Conflict |
| 4 | Commit 검증 | Predicate 충돌, Write Skew 여부 |
| 5 | 실패 시 재시도 | Retry 횟수, Abort rate |
> 요약: 격리 수준은 읽기 시점과 쓰기 충돌 검증 시점을 달리해 동시성 오류를 제한한다.

---

## Ⅳ. 특징

| 구분 | 낮은 격리(RU/RC) | 높은 격리(RR/SR) | 정량·판단 기준 |
|:---|:---|:---|:---|
| 읽기 일관성 | Statement 단위 | Transaction 또는 직렬 순서 | Dirty Read 0건, Phantom 재현 여부 |
| 처리량 | 잠금 대기 감소 | 충돌 대기·Abort 증가 | TPS, Lock wait p95 |
| 구현 방식 | 짧은 잠금·MVCC 읽기 | Predicate Lock·SSI·2PL | Deadlock, Serialization failure |
| 적용 업무 | 조회·로그성 업무 | 결제·재고·정산 업무 | 오류 허용 0건 업무 여부 |
> 요약: 낮은 격리는 대기 시간을 줄이고 높은 격리는 업무 정합성 오류를 줄이므로 데이터 중요도에 따라 선택한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단일 기본 격리 일괄 적용 | 업무별 격리 수준 차등 적용 | 조회, 결제, 정산 단위 위험 분리 |
| 비용/성능 | Serializable 일괄 적용 | RC 기본 + 중요 구간 격상 | p95 300ms, Abort rate 1% 이하 |
| 운영/위험 | 애플리케이션 재시도 없음 | 재시도·Idempotency 포함 | Serialization failure 처리 가능 여부 |
> 요약: 실무에서는 Read Committed를 기본값으로 두고 재고·정산 같은 충돌 구간만 격리 수준을 높인다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Dirty Read | 미확정 변경 노출 | Read Committed 이상 적용 | Dirty Read 테스트 0건 |
| Lost Update | 동시 갱신 덮어쓰기 | SELECT FOR UPDATE, 조건부 UPDATE | 갱신 충돌 탐지율 |
| Serialization Failure | Serializable 검증 실패 | 지수 Backoff, 최대 3회 Retry | Abort rate, retry success rate |
> 요약: 격리 리스크는 읽기 오염, 갱신 손실, 직렬화 실패이며 잠금·조건부 갱신·재시도로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정합성 | Dirty/Lost Update 0건 | 동시성 시나리오 테스트 |
| 대기 시간 | Lock wait p95 100ms 이하 | DB wait event, APM |
| 재시도 | Serialization retry 성공률 99% 이상 | 애플리케이션 로그 |
> 요약: 격리 수준 선택은 정합성 테스트와 Lock 대기, 재시도 성공률로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 기본 정책: 일반 OLTP는 Read Committed를 기본값으로 두고 Dirty Read 0건과 p95 응답 300ms 이하를 함께 측정함
2. 중요 구간: 재고 차감·포인트 사용은 SELECT FOR UPDATE 또는 Serializable 적용, 충돌 시 최대 3회 Idempotent Retry 수행함
3. DBMS 검증: PostgreSQL SSI, MySQL InnoDB RR, Oracle RC/Snapshot 동작 차이를 테스트 케이스로 확인 후 운영 표준에 반영함

**결론 (2줄):**
- 기술사 판단: 읽기 위주 업무는 RC/MVCC, 금전·재고 충돌 업무는 RR/SR 또는 명시 잠금을 선택함
- 향후 방향: MVCC 기반 Snapshot과 애플리케이션 재시도 패턴을 함께 설계해 정합성과 처리량 균형을 맞추는 방향임

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "격리 수준을 설명하시오" | RU/RC/RR/SR별 읽기 가시성 흐름 | 이상현상 매핑과 Lock/MVCC 비교 |
| 요구사항 명시형 | "비교하시오", "선택 방안을 제시하시오" | 업무별 격리 수준·재시도 설계 | 정합성 위험, Lock 대기, Abort 비용 선택 기준 |
> 요약: 설명형은 4단계와 이상현상, 비교형은 업무별 선택 기준과 운영 지표로 목차를 바꾼다.
