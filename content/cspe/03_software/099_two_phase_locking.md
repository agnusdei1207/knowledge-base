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
- **개요**: 트랜잭션이 잠금을 얻는 단계와 푸는 단계를 분리해 직렬 가능성을 보장하는 규칙
- **왜 필요한가**: 동시 트랜잭션이 같은 행을 읽고 쓰면 갱신 손실과 불일치가 발생한다. 2PL은 잠금 순서로 충돌을 통제한다.
- **핵심 직관**: 회의실 예약처럼 필요한 자원을 모두 확보하는 동안은 반납하지 않고, 반납을 시작하면 새 예약을 하지 않는 규칙이다.

## 깊이 이해
- **배경·문제의식**: DBMS는 동시에 실행되는 트랜잭션 결과가 어떤 직렬 순서와 같아야 정합성을 설명할 수 있다. 무작위 잠금 획득·해제는 직렬 가능성을 깨뜨릴 수 있다.
- **작동 원리**: Growing Phase에서는 필요한 Shared/Exclusive Lock을 획득한다. 첫 Unlock 이후 Shrinking Phase에 들어가며 새 Lock을 얻지 않는다. Strict 2PL은 Exclusive Lock을 Commit/Abort까지 유지해 Cascading Rollback을 줄인다.
- **비유**: 요리사가 재료를 모으는 동안에는 재료를 반납하지 않고, 조리가 끝나 반납을 시작하면 새 재료를 가져오지 않는 방식과 같다.
- **구체 예시**: T1이 A를 X Lock 후 B를 요청하고, T2가 B를 X Lock 후 A를 요청하면 Deadlock이 생긴다. Wait-For Graph에서 순환을 탐지해 한 트랜잭션을 Abort한다.
- **흔한 오해·주의점**: 2PL은 직렬 가능성을 보장하지만 교착상태를 자동 제거하지 않는다. Lock granularity와 Deadlock 처리 정책이 별도로 필요하다.

## 연결 개념
- 트랜잭션 격리 수준 - Serializable 구현 수단 중 하나
- Deadlock - 잠금 기반 동시성 제어의 대표 리스크
- MVCC - 읽기 대기를 줄이는 대안 동시성 제어

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

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
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
