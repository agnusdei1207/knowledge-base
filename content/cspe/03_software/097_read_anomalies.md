---
title: "Dirty Read·Non-Repeatable Read·Phantom Read (Read Anomalies)"
date: "2026-07-04"
tags:
  - "cspe-software"
weight: 97
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: 여러 트랜잭션이 동시에 실행될 때 격리 수준이 낮아서 발생하는 세 가지 대표적인 '읽기 이상 현상(Read Anomalies)'
- **왜 필요한가**: (096 격리 수준 참조) 성능을 위해 격리 수준(Isolation Level)을 낮추면 데이터 정확성이 깨지는데, 정확히 '어떤 식'으로 깨지는지 알아야 애플리케이션에서 적절한 방어가 가능하다.
- **핵심 직관**: 
  - **Dirty**: 아직 확정 안 된 거짓말을 믿음.
  - **Non-Repeatable**: 두 번 물어봤는데 대답(값)이 바뀜.
  - **Phantom**: 두 번 물어봤는데 아까 없던 귀신(새 레코드)이 생김.

## 핵심 용어 정리

| 용어/표기 | 의미 | 비유·예 |
|:---|:---|:---|
| Dirty Read | 트랜잭션 A가 아직 커밋 안 된 B의 데이터를 읽는 현상 | 작가가 결말 쓰다 지웠는데 독자가 미리 보고 믿음 |
| Non-Repeatable Read | A가 같은 데이터를 두 번 읽는 사이, B가 데이터를 '수정'해 값이 달라지는 현상 | 1초 전 5만원이었는데 결제 누르니 6만원으로 뜀 |
| Phantom Read | A가 범위 조건으로 두 번 읽는 사이, B가 새 데이터를 '삽입'해 없던 행이 나타나는 현상 | 아까 2명이었는데 다시 세보니 3명(귀신 출몰) |

## 깊이 이해
- **배경·문제의식**: DBMS는 Lock을 적게 걸어 동시성을 높이려 한다. 그 부작용으로 다른 트랜잭션이 만지고 있는 덜 익은 데이터나 변경된 데이터를 읽게 되는 부작용(이상 현상)이 정의되었다.
- **작동 원리 (어떻게 발생하는가)**: 
  - **Dirty Read**: T1이 레코드 X의 값을 10에서 20으로 바꿈 (미커밋). T2가 20을 읽어감. T1이 롤백(Rollback)해 10으로 돌아감. T2는 20이라는 '가짜 데이터'를 가지고 로직 수행!
  - **Non-Repeatable Read (NRR)**: T1이 X=10을 읽음. T2가 X를 20으로 수정(Update)하고 커밋. T1이 다시 X를 읽으니 20이 됨. 한 트랜잭션 내에서 조회 결과의 일관성이 깨짐.
  - **Phantom Read**: T1이 `나이>20`인 레코드 2개를 읽음. T2가 25살 신규 레코드를 삽입(Insert)하고 커밋. T1이 다시 `나이>20`을 조회하니 3개가 됨.
- **흔한 오해·주의점**: "NRR과 Phantom Read는 같은 거 아닌가?" 엄연히 다르다. NRR은 **기존 데이터의 수정(Update/Delete)** 때문에 값이 바뀌는 것이고, Phantom은 **새 데이터의 삽입(Insert)** 때문에 집합의 건수가 바뀌는 것이다. 방어하는 Lock의 종류(행 락 vs 범위 락)도 다르다.

## 연결 개념
- **트랜잭션 격리 수준 (Isolation Levels)**: 이 이상 현상들을 어디까지 막아줄 것인가의 기준 (096 키워드)
- **MVCC**: 이 현상들을 Lock 없이 스냅샷으로 방어하는 기술 (098 키워드)

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 읽기 이상 현상(Read Anomalies)은 트랜잭션의 병행 처리 과정에서 고립성(Isolation)이 완벽히 보장되지 않아 발생하는 세 가지 대표적인 데이터 불일치 에러다.
> 2. **가치**: 이 이상 현상들을 정확히 인지해야 비즈니스 로직의 치명적 결함(잘못된 재고 차감 등)을 막고, 적절한 격리 수준을 선택할 수 있다.
> 3. **판단 포인트**: NRR은 UPDATE/DELETE, Phantom은 INSERT 연산에 기인하므로, 방어를 위한 메커니즘(Record Lock vs Range Lock)을 명확히 구분해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 병행 제어 실패로 인한 현상 이해 | Dirty Read, Non-Repeatable Read, Phantom Read의 정확한 발생 시나리오 | 3가지 현상의 발생 원인(미커밋, 수정, 삽입) 혼동 |
| 이상 현상과 격리 수준 매핑 역량 | ANSI SQL 격리 수준 4단계와 각 현상의 방어 범위 연결 | MySQL과 Oracle의 방어 수준(MVCC) 차이 누락 |

> 요약: 세 가지 현상이 발생하는 메커니즘을 명확한 예시(Update vs Insert)로 구분하고, 이를 차단하는 격리 수준을 매핑해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 읽기 이상 현상은 다중 사용자 데이터베이스 환경에서 동시성 제어(Concurrency Control)가 부족할 때 발생하는 데이터 참조 불일치 현상임
- 배경: 트랜잭션 직렬화(Serializable)를 강제할 경우 성능이 크게 저하되므로, DBMS는 성능을 위해 격리 수준을 낮추게 되며 이로 인해 이상 현상 발생
- 필요성: 각 이상 현상이 유발하는 비즈니스 오류(가짜 데이터 참조, 집계 오류 등)를 파악하고, 최적의 격리 수준(Isolation Level)을 선택하기 위해 이해 필수

---

## Ⅱ. 3대 읽기 이상 현상 (구조 및 발생 메커니즘)

```text
Tx A Read ----> (Tx B 개입) ----> Tx A Re-Read
  |-> Dirty Read: Tx B의 [미커밋 데이터]를 읽음 (가짜 데이터)
  |-> Non-Repeatable Read: Tx B가 [Update/Delete] 후 커밋 -> A가 읽는 값이 변경됨
  |-> Phantom Read: Tx B가 [Insert] 후 커밋 -> A가 읽는 범위 집합 개수가 증가함
```

| 이상 현상 | 발생 연산 원인 | 비즈니스 리스크 예시 |
|:---|:---|:---|
| Dirty Read (오류 읽기) | 타 트랜잭션의 미확정 데이터 참조 | 결제 실패(Rollback)된 쿠폰을 이미 사용 처리 |
| Non-Repeatable Read (반복불가 읽기) | 타 트랜잭션의 **Update/Delete** 후 커밋 | 장바구니 담을 땐 1만원, 결제창 넘어가니 2만원 |
| Phantom Read (유령 읽기) | 타 트랜잭션의 **Insert** 후 커밋 | A부서 월급 합계 집계 중 신입사원 추가로 총액 불일치 |

> 요약: Dirty는 '신뢰할 수 없는 과거', NRR은 '값의 변동', Phantom은 '개수의 변동'을 의미한다.

---

## Ⅲ. 격리 수준별 이상 현상 방어 흐름도

```text
Tx 동시 실행 요청 -> DBMS 격리 수준 판단
   |-> Level 0 (Read Uncommitted): 방어 없음 (Dirty, NRR, Phantom 발생)
   |-> Level 1 (Read Committed): 미커밋 Read 차단 (Dirty 차단)
   |-> Level 2 (Repeatable Read): Read 시점 Snapshot 유지 (NRR 차단)
   |-> Level 3 (Serializable): Range/Table Lock 강제 (Phantom까지 차단)
```

- 1단계 [Read Uncommitted]: 어떠한 잠금도 없어 모든 이상 현상 발생 (Dirty Read 노출)
- 2단계 [Read Committed]: 커밋된 데이터만 읽도록 허용하여 Dirty Read 차단, 하지만 NRR과 Phantom은 잔존
- 3단계 [Repeatable Read]: 트랜잭션 시작 시점의 스냅샷(버전)을 읽게 하여 NRR 차단, 단 새로운 데이터가 삽입되는 Phantom 현상 발생 가능 (표준 기준)
- 4단계 [Serializable]: 읽는 범위에 락을 걸어 타 트랜잭션의 Insert까지 원천 차단하여 Phantom Read 완벽 방어

> 요약: 격리 수준을 올릴수록 DB 엔진은 더 강한 락(Lock)이나 다중 버전 스냅샷(MVCC)을 사용해 이상 현상을 단계적으로 차단한다.

---

## Ⅳ. 특징 (비교)

| 비교 축 | Non-Repeatable Read | Phantom Read |
|:---|:---|:---|
| 원인 행위 | 타 트랜잭션의 **수정(Update)** / 삭제(Delete) | 타 트랜잭션의 **삽입(Insert)** |
| 발생 영역 | 단일 특정 레코드 (행 단위) | 복수 레코드의 범위 (집합 단위) |
| 방어 기법 | Record Lock / MVCC 스냅샷 | Next-Key Lock (범위 락) / Table Lock |

> 요약: NRR은 존재하는 데이터의 일관성 문제이며 Record Lock으로 해결되나, Phantom Read는 부재했던 데이터의 출현이므로 넓은 범위의 잠금이 필요하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | Oracle 방식 | MySQL (InnoDB) 방식 | 선택 기준 |
|:---|:---|:---|:---|
| 기본 격리 수준 | Read Committed (NRR 허용) | Repeatable Read (NRR 차단) | 요구되는 정합성 깊이 |
| Phantom Read 방어 | Serializable 수준에서만 방어 | Repeatable Read에서도 자체 방어 (Next-Key Lock) | DBMS 특성 파악 |
| 동시성 제어 기법 | Undo 세그먼트 기반 MVCC | Undo 로그 기반 MVCC + Gap Lock | 락 경합 리스크 |

> 요약: 표준 SQL-92 기준과 실제 상용 DBMS의 구현(특히 MySQL의 Phantom Read 완화) 간 차이를 인지해야 한다.

**리스크·대응 (기본은 불릿):**
- 트랜잭션 롤백 시 Dirty Read 전파(Cascading Rollback): 한 트랜잭션의 실패로 인해 의존하던 여러 트랜잭션이 연쇄 롤백되는 재앙 → 최소 Read Committed 수준 이상 운영 환경 강제 의무화
- 팬텀 리드(Phantom Read)로 인한 이중 등록: 유니크 제약이 없는 컬럼 검색 후 Insert 시 동시성 충돌로 중복 데이터 생성 → 애플리케이션 레벨의 Unique Index 제약 추가 설계

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 정합성 우선 서비스: 재고, 결제, 포인트 차감 로직은 이상 현상을 막기 위해 격리 수준 상향(Repeatable Read) 또는 명시적 배타 락(`SELECT ... FOR UPDATE`) 적용
2. 집계/리포트 시스템 분리: 대량의 통계를 읽는 동안 Phantom Read를 막기 위해 Serializable을 적용하면 전체 시스템이 정지(Lock)되므로, 리드 레플리카(Read Replica)를 분리하여 격리
3. 낙관적 병행 제어(Optimistic Concurrency Control): NRR 현상을 DB 격리 수준이 아닌 앱 계층의 `@Version` 컬럼 확인으로 충돌을 감지하고 재시도(Retry)하도록 설계

**결론 (2줄):**
- 기술사 판단: 읽기 이상 현상은 고립성과 성능의 트레이드오프에서 발생하는 필연적 결과이며, DBMS의 Lock이나 MVCC 구현 메커니즘을 정확히 이해해야 완벽한 방어가 가능하다
- 향후 방향: 최근 마이크로서비스(MSA)와 분산 트랜잭션 환경에서는 단일 DB의 격리 수준에 의존할 수 없으므로, Saga 패턴 등 보상 트랜잭션을 통한 '최종 일관성(Eventual Consistency)' 기반 설계로 전환되고 있다

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "트랜잭션 병행 처리 시 문제점 설명" | Dirty, NRR, Phantom 메커니즘 상세 | 격리 수준 표, 실무 방어 전략 |
| 비교형 | "Non-repeatable과 Phantom의 차이" | Update(행) vs Insert(범위) 발생 원리 차이점 | 방어를 위한 Lock 범위 차이, DBMS별 특성 |
