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
- **개요**: 동시 트랜잭션이 같은 데이터를 읽고 쓰면서 관찰 결과가 어긋나는 현상
- **왜 필요한가**: 낮은 격리 수준은 TPS를 늘릴 수 있지만, 미확정 값 읽기·반복 조회 불일치·범위 조회 변화·갱신 손실을 만든다.
- **핵심 직관**: 내가 보고 있는 장부가 다른 사람의 임시 수정, 확정 수정, 새 행 삽입 때문에 계속 달라지는 문제이다.

## 깊이 이해
- **배경·문제의식**: DB는 동시에 여러 트랜잭션을 수행한다. 읽기와 쓰기가 겹치면 "같은 조건으로 읽었는데 결과가 다름" 또는 "내 갱신이 사라짐" 같은 업무 오류가 발생한다.
- **작동 원리**: Dirty Read는 Rollback될 수 있는 값을 읽는 현상이다. Non-Repeatable Read는 같은 행을 두 번 읽었을 때 값이 달라지는 현상이다. Phantom Read는 같은 조건 범위 조회에서 행 집합이 달라지는 현상이다. Lost Update는 두 갱신 중 하나가 덮어써지는 현상이다.
- **비유**: 회의록을 작성 중인 사람이 임시 문장을 보여주거나, 내가 복사한 뒤 누군가 문장을 바꾸거나, 새 안건을 끼워 넣어 최종 목록이 달라지는 상황과 같다.
- **구체 예시**: `balance=100`을 두 트랜잭션이 동시에 읽고 각각 10 차감 후 90으로 저장하면 최종값은 80이어야 하나 90이 되어 10이 사라진다.
- **흔한 오해·주의점**: Phantom Read는 행 값 변경이 아니라 조건에 맞는 행 집합 변화이다. Lost Update는 읽기 이상 표에 없더라도 실무 장애 비용이 커서 반드시 함께 비교한다.

## 연결 개념
- 트랜잭션 격리 수준 - 이상현상 방지 범위를 단계화한 규칙
- MVCC - Snapshot으로 읽기 일관성을 제공하는 방식
- 2PL - 잠금으로 충돌을 직렬화하는 방식

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
