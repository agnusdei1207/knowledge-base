---
title: 트랜잭션 격리 수준 (Transaction Isolation Levels)
date: 2026-07-05
tags: [cspe-software]
weight: 073
---

## Ⅰ. 개요
- 동시에 실행되는 트랜잭션들이 서로 어느 정도까지 영향을 미치게 할지 결정하는 설정임.
- ANSI/ISO SQL 표준(SQL92)에서 4단계 수준을 정의함.
- 출제 의도: 데이터 정합성 유지와 성능 간의 최적 균형점 도출 역량 확인.

## Ⅱ. 구성요소
- 부정합 현상 (Read Phenomena)
[Dirty Read] | [Non-Repeatable Read] | [Phantom Read]

| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Dirty Read | 커밋되지 않은 데이터의 읽기 허용 | 발표 전 가안을 인용함 |
| Non-Repeatable Read | 한 Tx 내 같은 쿼리가 다른 값 반환 | 읽는 중에 누가 값을 바꿈 |
| Phantom Read | 한 Tx 내 같은 쿼리가 다른 개수 반환 | 읽는 중에 누가 행을 추가함 |
> 요약: 낮은 격리 수준에서 발생하는 읽기 일관성 위배 현상들임.

## Ⅲ. 절차
- 격리 수준 4단계 (저레벨 -> 고레벨)
[Read Uncommitted] -> [Read Committed] -> [Repeatable Read] -> [Serializable]

1. Read Uncommitted: 커밋 전 데이터도 읽음. Dirty Read 발생함.
2. Read Committed: 커밋된 데이터만 읽음. 대부분의 DB 기본값임.
3. Repeatable Read: Tx 시작 시점의 스냅샷 제공. Phantom Read 가능성 있음.
4. Serializable: 모든 Tx를 순차 실행하는 것과 같이 처리. 완벽한 격리 보장함.
> 요약: 수준이 높을수록 일관성은 강화되나 동시성 성능은 저하됨.

## Ⅳ. 문제점
- Serializable 수준 사용 시 잠금 경합으로 인한 시스템 응답 불가 현상 위험.

## Ⅴ. 개선방안
- MVCC(Multi-Version Concurrency Control) 기술을 활용한 읽기-쓰기 충돌 완화.

## Ⅵ. 전망
- 클라우드 DB는 글로벌 서비스 가용성을 위해 기본 격리 수준을 유연하게 조정 지원.
- Snapshot Isolation을 넘어선 하드웨어 지원 트랜잭션 메모리 활용 가속화 예상.
