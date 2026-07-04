---
title: "락 관리 — 2단계 잠금 프로토콜 (2PL Two-Phase Locking)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 99
---

# 📖 【암기용】 개념 완전 이해

> 목적: 2PL을 처음 보는 사람도 Growing·Shrinking 단계, Strict 2PL, Lock Table, Deadlock의 관계를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 2PL(Two-Phase Locking)은 **동시성 제어**(Concurrency Control) 기법 중 잠금 기반 방식으로, 트랜잭션의 잠금 획득 단계와 해제 단계를 둘로 나눠 **직렬 가능성**(Serializability)을 보장하는 프로토콜이다.
- **왜 필요한가**: 여러 트랜잭션이 잠금을 아무 순서로나 걸고 풀면, 실행 결과가 어떤 순차 실행과도 같지 않은(직렬 가능하지 않은) 상태가 될 수 있다. 2PL은 "필요한 잠금을 다 모을 때까지는 아무것도 풀지 않는다"는 규칙으로 이 문제를 막는다.
- **핵심 직관**: 회의실을 예약할 때, 필요한 회의실을 모두 확보하는 동안은 이미 잡은 회의실을 반납하지 않고, 반납을 시작한 뒤로는 새 회의실을 잡지 않는 규칙과 같다.

## 핵심 용어 정리

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 동시성 제어(Concurrency Control) | 여러 트랜잭션의 동시 접근에서 정합성을 지키는 기법의 총칭 | 교차로의 신호 규칙 전체 |
| 직렬 가능성(Serializability) | 동시 실행 결과가 트랜잭션들을 어떤 순서로 하나씩 실행한 결과와 같아지는 성질 | 여러 사람이 동시에 일해도 결과는 "누가 먼저 했다고 쳐도" 말이 되는 상태 |
| Shared Lock(S-Lock) | 읽기용 잠금. 여러 트랜잭션이 동시에 걸 수 있음 | 도서관 열람실 — 여러 명이 같이 봐도 됨 |
| Exclusive Lock(X-Lock) | 쓰기용 잠금. 한 트랜잭션만 걸 수 있고 다른 S/X Lock과 공존 불가 | 대출된 책 — 한 사람만 가져감 |
| Lock Compatibility(잠금 호환성) | 두 잠금 모드가 동시에 걸릴 수 있는지 정의한 규칙(S-S는 허용, X가 섞이면 대기) | 회의실 동시 사용 가능 여부 규칙 |
| Growing Phase(확장 단계) | 트랜잭션이 필요한 잠금을 계속 획득만 하는 구간. 이 구간엔 Unlock 금지 | 짐을 계속 가져오기만 하는 단계 |
| Shrinking Phase(수축 단계) | 첫 Unlock 이후 잠금을 해제만 하는 구간. 이 구간엔 신규 Lock 금지 | 짐을 반납만 하는 단계 |
| Strict 2PL | Exclusive Lock을 Commit/Abort 시점까지 유지해 다른 트랜잭션이 커밋 전 데이터를 못 읽게 하는 강화 규칙 | 계산이 끝날 때까지 물건을 안 내려놓음 |
| Cascading Rollback(연쇄 롤백) | 한 트랜잭션이 Abort될 때, 그 트랜잭션이 쓴 값을 읽은 다른 트랜잭션까지 함께 롤백해야 하는 연쇄 현상 | 도미노처럼 줄줄이 취소됨 |
| Lock Table | 각 데이터 객체별로 어떤 잠금이 걸려 있고 누가 대기 중인지 기록하는 자료구조 | 회의실별 예약 현황판 |
| Wait-For Graph | "트랜잭션 A가 B가 가진 잠금을 기다린다"를 화살표로 표현한 그래프. 순환이 생기면 교착상태 | 누가 누구를 기다리는지 그린 화살표 지도 |
| Deadlock(교착상태) | 두 개 이상의 트랜잭션이 서로가 가진 잠금을 기다리며 영원히 멈춘 상태 | 두 사람이 서로 상대가 든 젓가락을 기다리며 못 먹는 상황 |

## 깊이 이해

### 왜 2단계로 나눠야 하나 — 문제의식
동시에 실행되는 트랜잭션들의 결과가 "어떤 순서로 하나씩 실행했다고 가정해도 말이 되는" 상태(직렬 가능)여야 정합성을 설명할 수 있다. 그런데 트랜잭션이 잠금을 얻었다 풀었다를 자유롭게 반복하면, 다른 트랜잭션이 그 틈에 끼어들어 직렬 가능성을 깨뜨릴 수 있다. 2PL 정리(Two-Phase Locking Theorem)는 "모든 트랜잭션이 잠금 획득을 끝낸 뒤에만 잠금 해제를 시작한다"는 규칙만 지키면, 그 실행 스케줄이 충돌 직렬 가능(Conflict Serializable)함을 보장한다.

### Growing/Shrinking 단계를 계좌 이체로 확인하기
계좌 A(잔액 100)에서 계좌 B(잔액 50)로 30을 이체하는 T1을 생각하자. T1은 Growing Phase에서 X-Lock(A)를 얻고 A=70으로 갱신한 뒤, X-Lock(B)를 얻고 B=80으로 갱신한다. 이 두 번째 Lock 획득까지가 Growing Phase다. 이후 Commit과 함께 Shrinking Phase에 들어가 X-Lock(A), X-Lock(B)를 순서대로 해제한다. 만약 T1이 X-Lock(A)를 갱신 직후 바로 풀고 X-Lock(B)를 나중에 잡았다면(2단계 규칙 위반), 그 사이에 다른 트랜잭션이 A만 반영된 중간 상태를 읽어 직렬 가능성이 깨질 수 있다.

### Deadlock을 Wait-For Graph로 판정하기
T1이 X-Lock(A)를 잡고 B를 요청하는 동안, T2가 X-Lock(B)를 먼저 잡고 A를 요청하면 교착상태가 된다. Wait-For Graph로 그리면 "T1 → T2"(T1이 T2가 쥔 B를 기다림)와 "T2 → T1"(T2가 T1이 쥔 A를 기다림)이라는 두 화살표가 순환(cycle)을 만든다. DBMS는 이 그래프에서 순환을 주기적으로(또는 요청마다) 탐지하고, 처리 비용이 가장 작은 트랜잭션 하나를 희생자로 선정해 Abort시켜 순환을 끊는다.

### Strict 2PL이 필요한 이유 — 수치로 보는 연쇄 롤백
일반 2PL은 Shrinking Phase 도중, 즉 Commit 전에도 X-Lock을 풀 수 있다. T1이 X-Lock(A)를 갱신 직후 풀면 T2가 그 값을 즉시 읽어갈 수 있는데, 만약 T1이 이후 실패해 Abort되면 T2가 읽은 값도 무효가 되어 T2까지 함께 Rollback해야 한다. 만약 T1의 변경을 읽은 트랜잭션이 5개였다면 연쇄 롤백은 최대 5건으로 번진다. Strict 2PL은 X-Lock을 Commit/Abort 시점까지 유지해, 커밋 전 값을 아예 다른 트랜잭션이 읽지 못하게 막아 이 연쇄를 원천 차단한다. 대부분의 상용 DBMS는 Strict 2PL(정확히는 Strong Strict 2PL)을 기본으로 채택한다.

### 잠금 호환성 행렬
| 요청\보유 | 없음 | S-Lock | X-Lock |
|:---:|:---:|:---:|:---:|
| S-Lock | 허용 | 허용 | 대기 |
| X-Lock | 허용 | 대기 | 대기 |

S-Lock끼리는 여러 트랜잭션이 동시에 가질 수 있지만(읽기는 서로 방해하지 않음), X-Lock이 하나라도 얽히면 반드시 대기한다. 이 행렬이 Lock Manager가 매 요청마다 확인하는 규칙이다.

## 연결 개념
- 트랜잭션 격리 수준(Isolation Level) — 2PL로 Serializable을 구현하는 대표 수단
- MVCC(098) — 읽기 잠금 없이 동시성을 제어하는 대안 기법
- Deadlock 탐지/예방 — 2PL 운영에서 반드시 함께 다뤄야 하는 리스크

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 2PL 단계, Lock Table, Strict 2PL, Deadlock 대응을 연결한다.
> 핵심: 2PL 답안은 직렬 가능성 보장 원리와 교착상태 비용을 함께 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 2PL은 Lock 획득 단계와 해제 단계를 분리해 충돌 직렬 가능성(Conflict Serializability)을 보장하는 프로토콜이다.
> 2. **가치**: Shared/Exclusive Lock과 Lock Table로 Read-Write, Write-Write 충돌을 명시적으로 제어한다.
> 3. **판단 포인트**: Strict 2PL, Lock Granularity, Deadlock Detection/Prevention, Lock Wait 지표를 함께 판단해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 2PL 원리 이해 확인 | Growing Phase, Shrinking Phase, Lock/Unlock 규칙 | 잠금만 설명하고 2단계 조건 누락 |
| 직렬 가능성 판단 확인 | Conflict Serializability, Strict 2PL | Deadlock이 없다고 오해 |
| 운영 리스크 대응 확인 | Lock Table, Wait-For Graph, Timeout | 교착상태 탐지·해결 방안 누락 |
> 요약: 2PL 문제는 직렬 가능성 보장과 Deadlock 처리 비용을 같이 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 2PL은 잠금 기반 동시성 제어 규칙이다.
- 배경: 트랜잭션이 같은 데이터에 동시에 접근하면 Lost Update, Dirty Read, Cascading Rollback이 발생한다.
- 필요성: Growing Phase, Shrinking Phase, Strict 2PL, Wait-For Graph로 직렬 가능성과 Deadlock 처리를 함께 설계해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Transaction -> Lock Manager -> Lock Table
  / Shared Lock: Read 허용
  / Exclusive Lock: Write 독점
Growing Phase -> Lock Acquire
Shrinking Phase -> Lock Release -> Commit / Abort
```

| 구성요소 | 역할 | 판단 포인트 |
|:---|:---|:---|
| Lock Manager | 잠금 요청 승인·대기·해제 관리 | Compatibility Matrix |
| Lock Table | 객체별 보유 Lock과 대기 큐 저장 | Row/Page/Table 단위 |
| Growing Phase | Lock 획득 가능, Unlock 금지 | 첫 Unlock 전까지 확장 |
| Shrinking Phase | Unlock 가능, 신규 Lock 금지 | 직렬 가능성 유지 조건 |
| Strict 2PL | X Lock을 Commit까지 유지 | Cascading Rollback 차단 |
> 요약: 2PL은 Lock Manager가 잠금 호환성을 검사하고 단계 규칙으로 직렬 가능성을 보장한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Begin -> Lock Request -> Compatibility Check
-> Granted / Wait Queue
-> Read / Write Execute -> Commit / Abort
-> Lock Release -> Deadlock Detect / Resolve
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 트랜잭션이 S/X Lock 요청 | Lock mode와 객체 ID |
| 2 | Lock Table에서 호환성 검사 | S-S 허용, X 충돌 대기 |
| 3 | Growing 단계에서 작업 수행 | Unlock 전 신규 Lock 가능 |
| 4 | Commit/Abort 후 Lock 해제 | Strict 2PL은 X Lock 유지 |
| 5 | 대기 순환 탐지와 희생자 Abort | Wait-For Graph cycle |
> 요약: 2PL은 잠금 호환성 검사, 대기 큐, Commit 후 해제, Deadlock 처리를 순차적으로 수행한다.

---

## Ⅳ. 특징

| 구분 | 일반 잠금 운용 | 2PL/Strict 2PL | 정량·판단 기준 |
|:---|:---|:---|:---|
| 직렬 가능성 | 해제 후 재획득 시 깨질 수 있음 | 2단계 규칙으로 보장 | conflict graph cycle 없음 |
| Rollback 영향 | Dirty Write 가능 | X Lock Commit까지 유지 | cascading rollback 0건 |
| 동시 처리 | 잠금 대기 발생 | 충돌 데이터 중심 대기 | lock wait p95, deadlock/hour |
| 구현 비용 | 단순 Lock/Unlock | Lock Table·Deadlock 처리 필요 | 메모리, Wait-For Graph 비용 |
> 요약: 2PL은 정합성을 강하게 보장하지만 잠금 대기와 교착상태를 운영 지표로 관리해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | MVCC Snapshot | 2PL Lock 기반 | 쓰기 충돌과 직렬 가능성 요구 |
| 비용/성능 | 읽기 대기 감소 | Lock wait와 Deadlock 처리 | 충돌률, p95 wait, TPS |
| 운영/위험 | Write Skew 가능 | Deadlock 가능 | 오류 비용 vs 대기 비용 |
> 요약: 쓰기 충돌 정합성이 우선이면 2PL, 읽기 지연 최소화가 우선이면 MVCC를 우선 검토한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Deadlock | 서로 다른 잠금 획득 순서 | Lock ordering, Wait-For Graph 탐지 | deadlock count/hour |
| Lock Escalation | 다수 Row Lock 보유 | Batch 크기 제한, 인덱스 조건 개선 | escalation count |
| 장기 대기 | 긴 트랜잭션과 범위 잠금 | timeout, 트랜잭션 분할 | lock wait p95 |
> 요약: 2PL 운영 리스크는 Deadlock, Lock Escalation, 장기 대기이며 순서 규칙과 타임아웃으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 직렬 가능성 | 충돌 그래프 cycle 0건 | 동시성 테스트, 로그 분석 |
| 잠금 대기 | lock wait p95 100ms 이하 | DB wait event |
| 교착상태 | deadlock 1건/시간 이하 | deadlock log, Wait-For Graph |
> 요약: 2PL 효과는 직렬 가능성 테스트와 잠금 대기·교착상태 지표로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 잠금 순서 표준화: 업무별 자원 접근 순서를 `고객 -> 주문 -> 재고 -> 결제`로 고정하고 코드 리뷰 체크리스트에 반영함
2. Deadlock 처리: Wait-For Graph 탐지 또는 timeout 5초, 희생자 Abort 후 Idempotent Retry 최대 3회 적용함
3. 잠금 범위 축소: 조건 컬럼 인덱스 추가와 Batch 1,000건 이하 분할로 Table Lock 전환과 p95 lock wait를 줄임

**결론 (2줄):**
- 기술사 판단: 직렬 가능성이 필수인 쓰기 중심 업무는 Strict 2PL, 조회 중심 업무는 MVCC 기반 격리를 선택함
- 향후 방향: DBMS는 MVCC를 기본으로 하되 중요 갱신 구간에 명시 잠금과 재시도 정책을 조합하는 방향임

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "2PL을 설명하시오" | Growing/Shrinking 단계와 Lock Table 흐름 | Strict 2PL, Deadlock, MVCC 대비 |
| 요구사항 명시형 | "동시성 제어를 비교하시오", "교착상태 대응 방안을 제시하시오" | Wait-For Graph, timeout, retry 흐름 | Lock wait, Deadlock 비용, 선택 기준 |
> 요약: 설명형은 2단계 규칙, 방안형은 교착상태 탐지와 잠금 범위 축소 중심으로 전환한다.
