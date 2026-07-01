---
title: "MVCC 다중 버전 동시성 제어 (MVCC)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 98
---

# 📖 【암기용】 개념 완전 이해

> 목적: MVCC를 처음 보는 사람도 버전 체인·스냅샷·트랜잭션 ID·Vacuum의 관계를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 한 데이터의 여러 버전을 보관해 읽기와 쓰기 충돌을 줄이는 동시성 제어 방식
- **왜 필요한가**: 읽기 작업이 많을 때 모든 조회가 쓰기 잠금을 기다리면 응답 지연이 커진다. MVCC는 읽기 시점의 버전을 보여주어 조회 대기를 줄인다.
- **핵심 직관**: 문서의 현재본을 수정 중이어도 독자는 자신이 시작한 시점의 사본을 읽는 방식이다.

## 깊이 이해
- **배경·문제의식**: OLTP는 조회와 갱신이 동시에 발생한다. 잠금 기반 방식은 읽기-쓰기 충돌에서 대기를 만들지만, MVCC는 이전 버전을 유지해 읽기가 쓰기를 기다리지 않도록 한다.
- **작동 원리**: 각 행 버전에는 생성 트랜잭션 ID와 삭제 또는 만료 트랜잭션 ID가 붙는다. 트랜잭션은 시작 시점의 Snapshot을 기준으로 볼 수 있는 버전만 읽고, 갱신은 새 버전을 생성한다. 오래된 버전은 Vacuum 또는 Garbage Collection으로 회수한다.
- **비유**: 위키 문서가 편집될 때 과거 리비전을 남겨 두는 것과 같다. 사용자는 자신이 연 시점의 리비전을 보고, 편집자는 새 리비전을 추가한다.
- **구체 예시**: T1이 `balance=100`을 읽는 동안 T2가 `balance=80`으로 Commit해도 T1은 Snapshot 기준 100을 계속 읽고, 새 트랜잭션은 80을 읽는다.
- **흔한 오해·주의점**: MVCC가 모든 동시성 문제를 제거하지 않는다. Write-Write 충돌, Write Skew, 버전 저장 공간 증가, Vacuum 지연을 별도로 관리해야 한다.

## 연결 개념
- Snapshot Isolation - MVCC로 제공되는 대표 격리 모델
- 트랜잭션 ID - 버전 가시성 판단 기준
- Read Anomalies - MVCC가 차단하거나 남기는 이상현상

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. MVCC의 버전 관리, Snapshot 가시성, 정리 작업, 충돌 판단을 연결한다.
> 핵심: MVCC 답안은 "읽기 잠금 없음"에서 멈추지 말고 버전 체인과 Vacuum 리스크까지 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MVCC는 데이터의 다중 버전을 유지해 트랜잭션별 Snapshot에 맞는 행 버전을 읽게 하는 동시성 제어 기법이다.
> 2. **가치**: 읽기-쓰기 충돌 대기를 줄이고 Consistent Read를 제공하되, 버전 저장 공간과 정리 비용을 관리해야 한다.
> 3. **판단 포인트**: 트랜잭션 ID, 버전 체인, Snapshot, Vacuum, Read-Write/Write-Write 충돌을 함께 설명해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| MVCC 구조 이해 확인 | Version Chain, Snapshot, TxID, Visibility Rule | 단순히 Lock을 안 쓴다고 설명 |
| 동시성·격리 판단 확인 | Snapshot Isolation, Write Conflict, Write Skew | Serializable과 Snapshot Isolation을 동일시 |
| 운영 리스크 인식 확인 | Vacuum, Undo, GC, Bloat, Long Transaction | 버전 정리 비용 누락 |
> 요약: MVCC 문제는 버전 가시성 규칙과 운영 정리 비용을 동시에 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: MVCC는 다중 버전 동시성 제어이다.
- 배경: 읽기와 쓰기가 많은 OLTP에서 조회가 갱신 잠금을 기다리면 p95 지연과 lock wait가 증가한다.
- 필요성: Snapshot, TxID, Version Chain, Vacuum으로 일관된 읽기와 Write-Write 충돌 관리를 동시에 수행해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Row Logical Key -> Version Chain
  / xmin: 생성 TxID
  / xmax: 삭제 또는 만료 TxID
Transaction Snapshot -> Visibility Rule -> Visible Version
Old Version -> Vacuum / Garbage Collection
```

| 구성요소 | 역할 | 판단 포인트 |
|:---|:---|:---|
| Version Chain | 동일 행의 과거·현재 버전 연결 | 체인 길이와 조회 비용 |
| Transaction ID | 버전 생성·만료 시점 표시 | Wraparound, TxID 관리 |
| Snapshot | 트랜잭션이 볼 수 있는 TxID 집합 | Statement vs Transaction Snapshot |
| Visibility Rule | 버전 노출 여부 판단 | xmin/xmax와 Commit 상태 |
| Vacuum/GC | 오래된 버전 회수 | Long transaction 영향 |
> 요약: MVCC는 행 버전에 TxID를 붙이고 Snapshot 가시성 규칙으로 읽을 버전을 선택한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Transaction Begin -> Snapshot Capture
-> Read Row -> Version Chain Scan -> Visibility Check
-> Update Row -> New Version Append
-> Commit / Abort -> Vacuum Old Version
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 트랜잭션 시작 시 Snapshot 생성 | active TxID 목록 |
| 2 | 읽기 시 Version Chain 탐색 | visible version 1개 선택 |
| 3 | 갱신 시 기존 버전 만료 후 새 버전 생성 | xmin/xmax 설정 |
| 4 | Commit 시 버전 가시성 확정 | Commit log 반영 |
| 5 | 정리 작업으로 불필요 버전 회수 | dead tuple 비율, bloat |
> 요약: MVCC는 읽을 때 Snapshot에 맞는 버전을 찾고 쓸 때 새 버전을 추가하며, 후속 정리로 저장 공간을 회수한다.

---

## Ⅳ. 특징

| 구분 | 잠금 기반 읽기 | MVCC | 정량·판단 기준 |
|:---|:---|:---|:---|
| 읽기 처리 | Shared Lock 대기 가능 | Snapshot 읽기 | read lock wait 0ms 목표 |
| 쓰기 처리 | Exclusive Lock 충돌 | 새 버전 생성 후 충돌 검증 | write conflict count |
| 저장 공간 | 현재 버전 중심 | 과거 버전 추가 저장 | dead tuple 20% 이하 |
| 운영 작업 | 잠금 모니터링 중심 | Vacuum/GC 모니터링 추가 | vacuum lag, bloat ratio |
> 요약: MVCC는 읽기 대기를 줄이는 대신 버전 저장 공간과 정리 지연을 운영 지표로 관리해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 2PL Shared/Exclusive Lock | Snapshot + Version Chain | 읽기 비중 70% 이상 OLTP |
| 비용/성능 | Lock wait 중심 | 버전 탐색·Vacuum 비용 | p95 read latency, bloat ratio |
| 운영/위험 | Deadlock 중심 | Long transaction, TxID wraparound | vacuum lag 임계치 |
> 요약: 읽기 중심 서비스는 MVCC가 적합하나 장기 트랜잭션과 버전 누적을 운영 기준으로 제한해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Table Bloat | 오래된 버전 미회수 | Autovacuum 튜닝, Batch 분할 | dead tuple ratio |
| Write Skew | Snapshot 간 조건 갱신 충돌 | Serializable, Predicate Lock | serialization failure count |
| TxID Wraparound | 트랜잭션 ID 소진 | Freeze Vacuum, 모니터링 알림 | age(datfrozenxid) |
> 요약: MVCC 리스크는 버전 누적, Snapshot 충돌, TxID 관리이며 Vacuum과 격리 수준 격상으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 읽기 지연 | 주요 조회 p95 100ms 이하 | APM, DB wait event |
| 버전 정리 | dead tuple 20% 이하 | pg_stat_user_tables, 엔진별 메트릭 |
| 충돌 관리 | write conflict·retry 성공률 99% 이상 | DB 로그, 애플리케이션 로그 |
> 요약: MVCC 운영 품질은 읽기 지연, 버전 누적, 충돌 재시도 성공률로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Snapshot 정책: 일반 조회는 Read Committed Snapshot, 정산 배치는 Repeatable Read로 분리하고 장기 트랜잭션 5분 초과 알림 설정함
2. Vacuum 관리: dead tuple 20% 또는 vacuum lag 10분 초과 시 Autovacuum scale factor와 비용 제한을 조정함
3. 충돌 제어: 조건 갱신 업무는 version 컬럼 또는 Serializable 적용, serialization failure 발생 시 최대 3회 재시도함

**결론 (2줄):**
- 기술사 판단: 읽기 비중이 큰 OLTP는 MVCC를 선택하되, 재고·정산처럼 조건 충돌이 큰 업무는 명시 잠금이나 Serializable을 병행함
- 향후 방향: 클라우드 DB와 분산 SQL에서도 MVCC 기반 Snapshot과 GC 비용을 SLO 지표로 관리하는 방향임

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "MVCC를 설명하시오" | Snapshot 생성, 버전 탐색, Vacuum 흐름 | 2PL 대비 읽기 대기·버전 비용 |
| 요구사항 명시형 | "동시성 제어를 비교하시오", "운영 방안을 제시하시오" | Lock/MVCC 선택과 충돌 처리 | Bloat, Long Transaction, Write Skew 대응 |
> 요약: 설명형은 버전 가시성, 운영형은 Vacuum과 충돌 지표 중심으로 목차를 전환한다.
