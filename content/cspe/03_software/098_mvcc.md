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
- **개요**: MVCC(Multi-Version Concurrency Control)는 **동시성 제어**(Concurrency Control) 기법의 한 갈래로, 하나의 논리적 행에 대해 **여러 버전**을 동시에 보관해 읽기가 쓰기 잠금을 기다리지 않게 하는 방식이다.
- **왜 필요한가**: 잠금 기반 동시성 제어는 읽기에도 Shared Lock을 요구하는 구현이 많아, 쓰기 트랜잭션이 진행 중이면 조회가 대기한다. 조회 비중이 높은 OLTP에서 이 대기는 곧 응답 지연으로 나타난다. MVCC는 "읽기는 과거 버전을 그대로 읽고, 쓰기는 새 버전을 추가한다"는 원칙으로 읽기-쓰기 간 잠금 대기를 없앤다.
- **핵심 직관**: 문서 편집 이력(리비전)과 같다. 편집자가 최신본을 고치는 동안에도, 이미 문서를 열어본 사람은 자신이 연 시점의 리비전을 계속 읽는다.

## 핵심 용어 정리

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 동시성 제어(Concurrency Control) | 여러 트랜잭션이 같은 데이터에 동시에 접근할 때 정합성을 지키기 위한 기법의 총칭(잠금 기반, MVCC 등) | 교차로의 신호 규칙 전체 |
| 트랜잭션 격리 수준(Isolation Level) | 한 트랜잭션이 다른 트랜잭션의 변경을 얼마나 볼 수 있는지 정하는 등급(Read Uncommitted~Serializable) | 방음 성능 등급 |
| Version Chain(버전 체인) | 같은 논리적 행의 과거~현재 물리적 버전을 연결한 목록 | 한 문서의 리비전 목록 |
| xmin | 그 버전을 만든(생성한) 트랜잭션의 ID | "이 리비전을 작성한 사람 번호" |
| xmax | 그 버전을 만료시킨(다음 버전이 생기게 한) 트랜잭션 ID. 아직 최신이면 비어 있음 | "이 리비전이 교체된 시점" |
| Snapshot | 트랜잭션 시작 시점에 "어느 TxID까지 커밋된 상태로 볼지" 고정한 기준 | 특정 순간을 찍은 사진 |
| Visibility Rule(가시성 규칙) | 어떤 버전이 현재 트랜잭션의 Snapshot에서 보여야 하는지 판정하는 규칙 | 그 사진에 찍힌 사람만 보인다는 규칙 |
| Vacuum / GC | 어떤 Snapshot에서도 더 이상 필요 없는 오래된 버전을 물리적으로 회수하는 작업 | 아무도 안 읽는 옛 리비전 파쇄 |
| Write Skew | 서로 다른 트랜잭션이 각자의 Snapshot을 기준으로 조건을 확인한 뒤 갱신해, 두 갱신이 합쳐지면 조건이 깨지는 이상현상 | 두 당직 의사가 각자 "다른 한 명이 남아있다"고 보고 동시에 자기 당직을 뺌 |
| TxID Wraparound | 트랜잭션 ID가 32비트 정수 한계(약 21억)에 도달해 번호가 순환하며 과거 버전을 최신으로 오판하는 장애 | 오래된 번호표가 새 번호와 겹쳐 순서가 꼬임 |

## 깊이 이해

### 왜 필요했나 — 잠금 기반의 한계
2PL 같은 잠금 기반 동시성 제어는 읽기에도 Shared Lock을 요구하는 구현이 많다. 긴 쓰기 트랜잭션이 하나 있으면 그 뒤의 모든 읽기가 잠금 해제를 기다린다. OLTP 서비스는 조회 비율이 70~90%에 달하는 경우가 흔한데, 이 조회가 매번 대기하면 p95 응답시간이 크게 늘어난다. MVCC는 읽기를 아예 잠그지 않는 대신 "읽는 시점 기준의 과거 버전"을 보여주는 방식으로 이 병목을 없앤다. PostgreSQL, MySQL InnoDB, Oracle이 모두 MVCC 계열 엔진이다.

### 버전 체인을 xmin/xmax로 추적하기
행이 갱신될 때 기존 값을 덮어쓰지 않고 새 버전을 추가한다. 예를 들어 TxID=50이 `balance=100`인 행을 만들면 그 버전은 xmin=50, xmax=없음이다. 이후 TxID=80이 같은 행을 `balance=80`으로 UPDATE하면, 기존 버전은 xmax=80으로 마감되고, xmin=80·xmax=없음인 새 버전이 추가된다. 이제 이 논리적 행 하나는 물리적으로 2개 버전(xmin=50/xmax=80, xmin=80/xmax=없음)을 가진 버전 체인이 된다.

### 가시성 규칙을 숫자로 확인하기
TxID=60인 트랜잭션이 이보다 먼저 시작해 Snapshot을 고정했다고 하자(그 시점에 TxID=80은 아직 시작 전). Repeatable Read에서 이 트랜잭션은 이후 TxID=80이 커밋을 마쳐도 같은 Snapshot을 계속 쓴다. 가시성 규칙은 "xmin이 내 Snapshot 이전에 커밋됐고, xmax가 없거나 내 Snapshot 이후에 마감된 버전만 보인다"이므로, TxID=60은 xmin=80 버전을 보지 못하고 xmin=50/xmax=80 버전을 읽어 여전히 `balance=100`을 얻는다. 반대로 TxID=60이 끝난 뒤 새로 시작한 TxID=90은 xmin=80 버전이 보여 `balance=80`을 읽는다. 같은 물리 데이터를 트랜잭션마다 다른 버전으로 읽는 것이 MVCC의 핵심이다.

### Vacuum이 필요한 이유 — 수치로 보는 Bloat
버전은 갱신될 때마다 쌓이므로, 회수하지 않으면 테이블이 비대해진다(Table Bloat). 예를 들어 초당 1,000건 UPDATE가 발생하는 테이블에서 Vacuum이 10분간 지연되면 약 60만 개의 죽은 버전(dead tuple)이 쌓인다. dead tuple 비율이 전체 행의 20%를 넘으면 인덱스 스캔과 시퀀셜 스캔 모두 불필요한 페이지를 읽어 느려진다. Vacuum/Autovacuum은 현재 활성 중인 모든 트랜잭션의 Snapshot에서 더 이상 보이지 않는 버전만 골라 물리적으로 삭제해 공간을 회수한다.

### TxID Wraparound — 왜 위험한가
트랜잭션 ID는 흔히 32비트 정수로 관리되어 최댓값이 약 21억(2^31)이다. 이 번호가 소진되면 순번이 처음으로 되돌아가는데(wraparound), 이때 과거 TxID가 순환 이후의 새 TxID보다 커 보이는 역전이 생겨 오래된 버전이 "아직 생성되지 않은 미래 데이터"로 잘못 판정될 수 있다. 초당 1,000건씩 트랜잭션이 발생한다면 약 24일 만에 21억에 도달할 수 있으므로, Freeze Vacuum으로 오래된 버전의 TxID를 특수 고정값으로 바꾸고, 가장 오래된 미동결 트랜잭션과의 거리(age)를 운영 지표로 감시해야 한다.

### Write Skew — MVCC가 막지 못하는 이상현상
당직 배정 예시로 보면 이렇다. 규칙은 "최소 1명은 당직을 서야 한다"이고 현재 의사 A, B 두 명이 당직 중이다. TxID 1은 자신의 Snapshot에서 "B가 당직 중"임을 확인하고 "A는 빠져도 된다"고 판단해 A를 뺀다. 거의 동시에 TxID 2도 자신의 Snapshot에서 "A가 당직 중"임을 확인하고 B를 뺀다. 두 트랜잭션 모두 자기 Snapshot 안에서는 규칙을 지켰지만, 서로의 변경을 보지 못한 채 커밋되면 당직자가 0명이 되어 규칙이 깨진다. 이를 막으려면 Serializable 격리 수준(Serializable Snapshot Isolation, Predicate Lock)이 별도로 필요하다.

## 연결 개념
- 트랜잭션 격리 수준(Isolation Level) — MVCC가 Read Committed·Repeatable Read를 구현하는 수단
- 2단계 잠금(2PL, 099) — MVCC와 대비되는 잠금 기반 동시성 제어
- Write Skew, TxID Wraparound — MVCC 도입 시 별도로 관리해야 하는 리스크

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
