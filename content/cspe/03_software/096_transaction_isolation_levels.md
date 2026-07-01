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
- **개요**: 동시 트랜잭션이 서로 보이는 범위를 조절하는 정합성 단계
- **왜 필요한가**: 모든 트랜잭션을 완전히 직렬화하면 대기 시간이 커지고, 격리를 낮추면 Dirty Read·Phantom 같은 읽기 이상이 생긴다.
- **핵심 직관**: 격리 수준은 "남이 작성 중인 장부를 어디까지 볼 수 있게 할 것인가"를 정하는 규칙이다.

## 깊이 이해
- **배경·문제의식**: OLTP 시스템은 수백~수천 TPS로 동시에 데이터를 읽고 쓴다. 높은 격리는 정합성 오류를 줄이지만 잠금 대기와 재시도 비용을 만든다.
- **작동 원리**: Read Uncommitted는 미확정 변경도 읽을 수 있다. Read Committed는 Commit된 값만 읽는다. Repeatable Read는 같은 행을 다시 읽어도 값이 유지된다. Serializable은 실행 결과가 직렬 순서와 같도록 보장한다.
- **비유**: 공동 문서 작업에서 임시 저장본까지 볼지, 저장 완료본만 볼지, 내가 읽은 문단을 고정할지, 문서 전체 편집 순서를 줄 세울지의 차이다.
- **구체 예시**: 재고 1개 상품을 두 사용자가 동시에 구매하면 낮은 격리에서는 Lost Update 또는 음수 재고가 발생할 수 있어 조건부 UPDATE나 Serializable이 필요하다.
- **흔한 오해·주의점**: Repeatable Read가 항상 Phantom Read를 막는 것은 DBMS 구현에 따라 다르다. InnoDB는 Next-Key Lock으로 많은 Phantom을 차단하지만 Snapshot Isolation은 Write Skew를 남길 수 있다.

## 연결 개념
- Read Anomalies - 격리 수준이 방지해야 하는 현상
- MVCC - 읽기 잠금 없이 Snapshot을 제공하는 구현 방식
- 2PL - 잠금 기반 직렬 가능성 보장 방식

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
