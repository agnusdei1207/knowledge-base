---
title: "Dirty Read·Non-Repeatable Read·Phantom Read (Read Anomalies)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 97
---

# 📖 【암기용】 개념 완전 이해

> 목적: 읽기 이상현상을 처음 보는 사람도 Dirty Read, Non-Repeatable Read, Phantom Read, Lost Update 차이를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 읽기 이상현상(Read Anomalies)은 **동시성 제어(Concurrency Control)**가 낮은 격리 수준으로 완화됐을 때, 여러 트랜잭션이 같은 데이터를 동시에 읽고 써서 관찰 결과가 실제와 어긋나는 4가지 대표 현상(Dirty Read·Non-Repeatable Read·Phantom Read·Lost Update)이다.
- **왜 필요한가**: 격리 수준을 낮추면 잠금 대기가 줄어 처리량(TPS)이 오르지만, 그 대가로 미확정 값을 읽거나(Dirty Read), 같은 조회가 두 번 다른 값을 내거나(Non-Repeatable), 조회할 때마다 행 개수가 바뀌거나(Phantom), 내가 한 갱신이 사라지는(Lost Update) 문제가 생긴다. 이 현상들을 구분해야 어떤 격리 수준을 선택해야 하는지 판단할 수 있다.
- **핵심 직관**: 내가 보고 있는 장부가, 다른 사람의 아직 확정 안 된 수정 / 방금 확정된 수정 / 새로 끼워 넣은 항목 / 내 수정과의 충돌 때문에 계속 달라지는 문제다 — "언제, 무엇이 달라 보이는가"로 4가지를 구분한다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 동시성 제어 (Concurrency Control) | 여러 트랜잭션이 같은 데이터를 동시에 접근할 때 결과가 어긋나지 않게 조율하는 기법 — 읽기 이상현상의 **상위 개념**(이 조율이 불완전하면 이상현상이 발생) | 여러 사람이 같은 문서를 동시에 편집할 때의 충돌 규칙 |
| 트랜잭션 격리 수준 | Read Uncommitted~Serializable의 4단계로 어떤 이상현상까지 허용할지 정하는 표준 — 읽기 이상현상과 **직결되는 상위 개념** | 각 단계가 "이 정도까지는 봐도 된다"고 정한 눈금 |
| Dirty Read (오손 읽기) | 다른 트랜잭션이 아직 Commit하지 않은(Rollback될 수도 있는) 값을 읽는 현상 | 남이 쓰다 지울 수도 있는 낙서를 진짜인 줄 알고 읽음 |
| Non-Repeatable Read (반복 불가 읽기) | 같은 행을 같은 트랜잭션 안에서 두 번 읽었는데 값이 달라지는 현상 | 아까 본 문장이 다시 보니 남이 고쳐서 바뀌어 있음 |
| Phantom Read (유령 읽기) | 같은 조건으로 범위 조회를 반복했는데 값이 아니라 **행의 개수(집합)**가 달라지는 현상 | 아까 목록엔 없던 새 항목이 다시 조회하니 나타남 |
| Lost Update (갱신 손실) | 두 트랜잭션이 같은 값을 읽고 각자 갱신했는데, 하나의 갱신 결과가 다른 하나에 덮어써져 사라지는 현상 | 두 사람이 동시에 고친 문서에서 한 명의 수정이 저장 시 사라짐 |
| Write Skew | 서로 다른 행을 각자 조건에 맞게 갱신했지만, 두 결과를 합치면 업무 규칙을 위반하게 되는 현상 (Snapshot Isolation에서 특히 발생) | 당직자 2명이 "다른 한 명이 있으니 나는 빠져도 됨"을 동시에 확인하고 둘 다 빠짐 |
| MVCC | 값의 여러 버전을 보관해 읽기 시점의 스냅샷을 제공하는 구현 방식 | 서로 다른 시점의 스냅샷 사진첩 |
| 잠금 (Lock) | 특정 행·범위에 대한 접근을 막아 충돌을 방지하는 기법 (Row Lock, Predicate Lock 등) | 회의실 예약으로 이중 사용을 막음 |

## 깊이 이해

### 왜 나뉘어 있나 (배경)
- DB는 항상 여러 트랜잭션을 동시에 수행한다. 만약 모든 트랜잭션을 하나씩 순서대로만 처리한다면(완전 직렬) 이상현상은 전혀 없겠지만 처리량이 크게 떨어진다. 그래서 격리 수준을 의도적으로 낮춰 성능을 얻는 대신, "낮췄을 때 정확히 어떤 오류가 날 수 있는가"를 미리 분류해 둔 것이 읽기 이상현상 4종이다. 이 분류가 있어야 "우리 업무는 이 이상현상까지는 허용 가능한가"를 판단할 수 있다.

### Dirty Read 워크드 예제
- T2가 `UPDATE account SET balance = balance + 1000000 WHERE id='A'`를 실행해(아직 Commit 안 함) A의 값이 잔액 100만원→ 200만원으로 바뀐 상태다. 이때 T1이 A를 조회하면 200만원이 보인다(Read Uncommitted에서). 그런데 T2가 이후 어떤 이유로 Rollback하면 A는 다시 100만원으로 돌아가고, T1은 존재한 적 없는 200만원을 근거로 이미 다른 판단(예: 대출 승인)을 내려버렸을 수 있다.

### Non-Repeatable Read 워크드 예제
- T1이 트랜잭션 안에서 `SELECT balance FROM account WHERE id='A'`를 실행해 100만원을 읽는다. 그 사이 T2가 A에 10만원을 입금하고 Commit한다. T1이 같은 트랜잭션 안에서 **같은 SELECT를 다시** 실행하면 이번엔 110만원이 나온다 — 같은 조회인데 결과가 달라졌다. Read Committed까지는 이 현상이 허용되고, Repeatable Read부터는 트랜잭션 시작 시점 스냅샷을 고정해 막는다.

### Phantom Read 워크드 예제
- T1이 `SELECT * FROM orders WHERE amount > 100000`을 실행해 5건을 읽는다. 그 사이 T2가 `amount=200000`인 새 주문을 INSERT하고 Commit한다. T1이 트랜잭션 안에서 **같은 조건으로 다시** 조회하면 6건이 나온다 — 기존 행의 값이 바뀐 게 아니라 조건을 만족하는 **행 자체가 새로 생겨** 집합이 달라졌다는 점이 Non-Repeatable Read와의 차이다. Repeatable Read는 DBMS 구현에 따라 이를 막을 수도, 못 막을 수도 있고(예: InnoDB는 Next-Key Lock으로 상당수 차단), 표준적으로는 Serializable에서 완전히 차단된다.

### Lost Update 워크드 예제 (수치로 확인)
- 재고(stock=100)를 두 트랜잭션 T1, T2가 동시에 처리한다고 하자. T1: `SELECT stock`(100 읽음) → `stock=100-10=90`으로 UPDATE. T2도 거의 동시에 `SELECT stock`(역시 100 읽음, T1의 커밋 전) → `stock=100-20=80`으로 UPDATE.
- T2가 나중에 Commit하면 최종 값은 80이 된다. 하지만 올바른 결과는 100-10-20=70이어야 한다 — T1의 -10 차감이 통째로 사라졌다(Lost Update). 방지책: `UPDATE product SET stock = stock - 10 WHERE id=1 AND stock >= 10`처럼 조건부 갱신을 쓰거나(값을 다시 읽지 않고 DB가 직접 연산), 버전 컬럼으로 낙관적 잠금을 걸거나(`WHERE version=5`, 성공 시 version+1), `SELECT ... FOR UPDATE`로 행 잠금을 걸어 T2가 T1의 Commit을 기다리게 한다.

### Write Skew — Lost Update와 구분해서 이해하기
- 당직 규칙 "최소 1명은 당직을 서야 한다"가 있고, 당직자 A와 B가 모두 당직 중이라고 하자. A는 "B가 있으니 나는 빠져도 되겠다"고 확인 후 자신을 제외 처리하고, 거의 동시에 B도 "A가 있으니 나는 빠져도 되겠다"고 확인 후 자신을 제외 처리한다. 두 트랜잭션은 서로 다른 행(A의 행, B의 행)을 갱신했으므로 Lost Update는 아니지만, 최종적으로 당직자가 0명이 되어 업무 규칙을 위반한다 — 이것이 Write Skew이며, Snapshot Isolation만으로는 막지 못하고 Serializable(SSI)이 필요하다.

### 비유와 흔한 오해
- **비유**: 회의록을 작성 중인 사람이 아직 확정 안 된 임시 문장을 보여주면(Dirty Read), 내가 복사해 둔 문단을 누군가 그새 고치면(Non-Repeatable Read), 회의 안건 목록에 새 안건이 끼어들면(Phantom Read), 두 사람이 동시에 같은 항목을 고쳐 한쪽이 사라지면(Lost Update) — 각각 "언제 무엇이 달라 보였는가"로 구분된다.
- **오해**: Phantom Read는 "행의 값이 바뀐 것"이 아니라 "조건에 맞는 행의 개수(집합)가 바뀐 것"이다 — Non-Repeatable Read와 혼동하기 쉽지만 전자는 개별 행 값 변화, 후자는 집합 크기 변화다. 또한 Lost Update는 ANSI SQL 표준의 4개 이상현상 표에는 직접 등장하지 않지만, 실무에서 발생 빈도와 장애 비용이 매우 커서 반드시 함께 다뤄야 한다.

## 연결 개념
- 트랜잭션 격리 수준: 이 4가지 이상현상 중 어디까지 허용할지를 단계화한 규칙
- MVCC: Snapshot으로 읽기 일관성을 제공해 일부 이상현상을 막는 구현 방식
- 2PL: 잠금으로 충돌을 직렬화해 이상현상을 막는 구현 방식
- 트랜잭션 ACID: 이 이상현상들이 침해하는 상위 원칙(Isolation)

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 읽기 이상현상별 발생 조건, 격리 수준 매핑, 방지 기법을 연결한다.
> 핵심: 이상현상 답안은 예시 SQL 타임라인과 격리 수준 선택 기준을 함께 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Read Anomalies는 동시 트랜잭션에서 읽기 결과가 미확정·변경·삽입·덮어쓰기 영향으로 어긋나는 현상이다.
> 2. **가치**: 이상현상을 분류하면 격리 수준, 잠금, MVCC, 재시도 정책을 업무 위험에 맞게 선택할 수 있다.
> 3. **판단 포인트**: Dirty, Non-Repeatable, Phantom, Lost Update를 발생 조건과 방지 격리 수준으로 매핑해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 읽기 이상현상 구분 확인 | Dirty, Non-Repeatable, Phantom, Lost Update | Non-Repeatable과 Phantom을 같은 현상으로 설명 |
| 격리 수준 매핑 역량 확인 | RC, RR, Serializable, Snapshot Isolation | 격리 수준별 방지 범위를 DBMS 차이 없이 단정 |
| 실무 대응 판단 확인 | SELECT FOR UPDATE, Predicate Lock, Version Check | 예시 없이 용어만 나열 |
> 요약: 이 문제는 이상현상 이름보다 발생 타임라인과 방지 기법 매핑을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: Read Anomalies는 동시성 읽기 오류이다.
- 배경: 낮은 격리 수준은 잠금 대기를 줄이나 미확정 데이터 읽기, 반복 조회 불일치, 범위 결과 변화, 갱신 손실을 만든다.
- 필요성: Dirty Read, Phantom Read, Lost Update를 격리 수준, SELECT FOR UPDATE, MVCC 정책으로 방지해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Transaction T1 / T2 Concurrent Execution
  / Dirty Read -> Uncommitted Value Read
  / Non-Repeatable Read -> Same Row Value Changed
  / Phantom Read -> Range Result Set Changed
  / Lost Update -> Overwritten Write
Isolation / Lock / MVCC -> Anomaly Prevention
```

| 이상현상 | 발생 조건 | 대표 사례 |
|:---|:---|:---|
| Dirty Read | T2가 T1의 미Commit 값을 읽음 | Rollback 후 잘못된 잔액 표시 |
| Non-Repeatable Read | 같은 행을 재조회했을 때 값 변경 | 주문 상태 1차 조회와 2차 조회 불일치 |
| Phantom Read | 같은 조건 범위의 행 집합 변경 | `amount > 100` 결과 행 증가 |
| Lost Update | 두 갱신 중 하나가 덮어써짐 | 재고 2회 차감 중 1회만 반영 |
| Write Skew | Snapshot 기반 조건 갱신 충돌 | 당직자 2명 동시 해제 |
> 요약: 읽기 이상현상은 값 오염, 값 변경, 행 집합 변화, 갱신 손실로 구분해 설명한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
T1 Begin -> Read Predicate / Row
T2 Begin -> Update / Insert / Commit
T1 Re-Read / Update -> Anomaly Observe
-> Isolation Check -> Lock / Snapshot / Retry
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | T1이 행 또는 범위 조건을 읽음 | Read set, Predicate 기록 |
| 2 | T2가 같은 행 변경 또는 조건 행 삽입 | Write set, Insert range 확인 |
| 3 | T2 Commit 또는 Rollback 발생 | Commit 상태, Undo 가능성 |
| 4 | T1이 재조회 또는 갱신 수행 | 값 변화, 행 집합 변화 탐지 |
| 5 | 격리 정책에 따라 차단·재시도 | Lock wait, Serialization failure |
> 요약: 이상현상은 첫 읽기와 재조회 사이에 다른 트랜잭션의 쓰기·삽입·Rollback이 끼어들 때 발생한다.

---

## Ⅳ. 특징

| 구분 | 발생 조건 | 방지 수준·기법 | 정량·판단 기준 |
|:---|:---|:---|:---|
| Dirty Read | 미Commit 값 읽기 | Read Committed 이상 | Dirty Read 테스트 0건 |
| Non-Repeatable | 같은 행 값 변경 | Repeatable Read 이상 | 동일 PK 재조회 불일치 0건 |
| Phantom | 조건 행 집합 변경 | Serializable, Predicate Lock | 범위 조회 행 수 변화 0건 |
| Lost Update | 갱신 덮어쓰기 | Row Lock, Version Column | 충돌 탐지율 100% |
> 요약: 이상현상별 방지 수준이 다르므로 업무 오류 비용에 맞춰 격리 수준과 잠금 범위를 선택한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 낮은 격리 일괄 적용 | 이상현상별 방지 기법 적용 | 업무별 허용 오류 0건 여부 |
| 비용/성능 | 잠금 최소화 | Row/Predicate Lock, MVCC 검증 | Lock wait p95, Abort rate |
| 운영/위험 | 재현 어려운 장애 | 타임라인 테스트와 충돌 로그 | 동시성 테스트 커버리지 |
> 요약: 이상현상은 운영 장애 후 추적이 어려우므로 사전 타임라인 테스트와 격리 수준 매핑이 필요하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Dirty Read | Read Uncommitted 사용 | RC 이상 강제 | RU 세션 0건 |
| Phantom | 범위 잠금 부재 | Predicate Lock, Next-Key Lock | Range anomaly 0건 |
| Lost Update | 읽고 쓰기 사이 충돌 미검증 | Optimistic Lock version, SELECT FOR UPDATE | update conflict detected count |
> 요약: Dirty는 격리 수준, Phantom은 범위 잠금, Lost Update는 버전 검증 또는 행 잠금으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 이상현상 재현 | 4종 시나리오별 기대 결과 일치 | 동시성 테스트 스크립트, 트랜잭션 로그 |
| 충돌 처리 | 재시도 성공률 99% 이상 | 애플리케이션 retry 로그 |
| 잠금 영향 | Lock wait p95 100ms 이하 | DB wait event, deadlock log |
> 요약: 대응 효과는 이상현상 테스트, 충돌 재시도 성공률, 잠금 대기 지표로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 테스트 설계: Dirty, Non-Repeatable, Phantom, Lost Update를 각각 T1/T2 타임라인으로 재현하고 회귀 테스트에 포함함
2. 업무 분류: 조회 화면은 RC, 정산·재고는 RR/SR 또는 SELECT FOR UPDATE로 분리하고 Lock wait p95 100ms 목표를 둠
3. 갱신 보호: Optimistic Lock `version` 컬럼 또는 조건부 UPDATE로 Lost Update를 탐지하고 실패 시 최대 3회 재시도함

**결론 (2줄):**
- 기술사 판단: 읽기 이상현상은 격리 수준 선택의 근거이며, 금전·재고 업무는 Lost Update와 Phantom을 우선 차단함
- 향후 방향: MVCC Snapshot, 명시 잠금, Idempotent Retry를 조합해 동시성 오류를 테스트 가능한 운영 기준으로 관리하는 방향임

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "읽기 이상현상을 설명하시오" | T1/T2 타임라인과 4종 이상현상 | 격리 수준별 방지 범위 |
| 요구사항 명시형 | "비교하시오", "방지 방안을 제시하시오" | 업무별 격리 수준·잠금·버전 검증 | 오류 비용, Lock 대기, 재시도 기준 |
> 요약: 설명형은 현상 구분, 방안형은 격리·잠금·재시도 조합 중심으로 답안을 구성한다.
