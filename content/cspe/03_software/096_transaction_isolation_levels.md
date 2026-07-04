---
title: "트랜잭션 격리 수준 4단계 (Transaction Isolation Levels)"
date: "2026-07-04"
tags:
  - "cspe-software"
weight: 96
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: 복수의 트랜잭션이 동시 실행될 때, 한 트랜잭션이 다른 트랜잭션의 변경 데이터를 어디까지 볼 수 있게 할지 결정하는 4단계 타협점
- **왜 필요한가**: (095 ACID 참조) 고립성(I)을 100% 지키면(순차 실행) 성능이 심각하게 저하된다. 따라서 데이터 정확성을 조금 포기하더라도 동시 처리 성능(속도)을 높이기 위해 필요하다.
- **핵심 직관**: 보안 검색대와 같다. "가방을 다 열어보고 몸수색까지 한다(Serializable = 속도 느림, 안전함) vs 겉옷만 훑고 패스한다(Read Uncommitted = 속도 빠름, 위험함)" 사이의 선택이다.

## 핵심 용어 정리

| 용어/표기 | 의미 | 비유·예 |
|:---|:---|:---|
| 격리 수준 (Isolation Level) | 트랜잭션 간의 데이터 가시성(Visibility)을 제어하는 단계 | 보안 검색의 깐깐함 정도 |
| Read Uncommitted | 다른 트랜잭션이 커밋하지 않은 임시 데이터도 읽음 (Level 0) | 결제 중인 화면 훔쳐보기 |
| Read Committed | 커밋이 완료된 데이터만 읽음 (Level 1, Oracle 기본) | 결제 완료 영수증만 보기 |
| Repeatable Read | 한 트랜잭션 내에서 같은 조회는 항상 같은 결과를 보장 (Level 2, MySQL 기본) | 시험 중엔 책이 안 바뀌게 고정 |
| Serializable | 트랜잭션들을 완전히 순차적으로 실행 (Level 3) | 1명씩만 방에 들어가서 작업 |

## 깊이 이해
- **배경·문제의식**: ACID 원칙 중 '격리성'은 트랜잭션 병행 처리 시 데이터 간섭을 막아야 함을 의미한다. 하지만 엄격한 Lock 기반 제어는 대기 시간(Stall)을 발생시켜 TPS(초당 트랜잭션)를 급감시킨다. ANSI SQL-92 표준은 이를 해결하기 위해 4단계 격리 수준을 정의했다.
- **작동 원리 (어떤 이상 현상을 막는가)**: 
  - 각 단계는 위로 갈수록 엄격해지며, 특정 이상 현상(097 이상 현상 참조)을 하나씩 차단한다.
  - **Level 0 (Read Uncommitted)**: 속도는 최고. 하지만 Dirty Read(커밋 안 된 가짜 데이터 읽기) 발생.
  - **Level 1 (Read Committed)**: Dirty Read 차단. 하지만 Non-Repeatable Read(동일 조회 결과 달라짐) 발생 가능.
  - **Level 2 (Repeatable Read)**: Non-Repeatable Read 차단. MySQL은 이 단계에서 MVCC로 Phantom Read(유령 레코드 출현)도 일부 차단.
  - **Level 3 (Serializable)**: 모든 이상 현상 차단. 완벽한 고립성 달성, 하지만 성능 최악.
- **흔한 오해·주의점**: "높은 격리 수준이 무조건 좋다?" 아니다. Serializable은 성능 이슈로 실무에서 거의 쓰이지 않는다. 대다수 서비스는 Read Committed나 Repeatable Read를 선택하고, 부족한 정합성은 애플리케이션 로직(Optimistic Lock 등)으로 푼다.

## 연결 개념
- **읽기 이상 현상 (Read Anomalies)**: 각 격리 수준에서 발생하는 구체적인 에러 상황 (097 키워드)
- **MVCC**: 격리 수준을 Lock 없이 달성하게 해주는 핵심 기술 (098 키워드)

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 트랜잭션 격리 수준은 병행 처리 시 발생할 수 있는 데이터 정합성 문제(이상 현상)를 차단하기 위해 4단계로 규정한 데이터 가시성 제어 표준이다.
> 2. **가치**: 데이터의 무결성(안전성)과 병행 처리 성능(동시성) 사이의 트레이드오프(Trade-off)를 비즈니스 성격에 맞게 조절할 수 있도록 한다.
> 3. **판단 포인트**: DBMS별 기본값(MySQL은 Repeatable Read, Oracle은 Read Committed)이 다르므로 환경에 맞춘 설정이 필수적이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 데이터 정합성과 동시성 간의 트레이드오프 이해 | 4단계 격리 수준 명칭과 허용/차단되는 이상 현상 매핑 | 격리 수준만 나열하고 이상 현상 방어 여부 누락 |
| 실무 환경에서의 DBMS별 기본값 인식 | DB별 기본 격리 수준 (Oracle, MySQL)의 차이 | Serializable이 실무 표준이라고 단정하는 오류 |

> 요약: 4단계 격리 수준이 각각 차단하는 이상 현상(Dirty, Non-repeatable, Phantom Read)과의 매핑이 채점의 핵심이다.

---

## Ⅰ. 개요 및 필요성

- 개요: 트랜잭션 격리 수준(Isolation Levels)은 복수의 트랜잭션이 동시 실행될 때 상호 간섭을 제어하기 위해 ANSI SQL-92에서 정의한 4단계 고립화 표준임
- 배경: 엄격한 직렬화(Serializable)를 강제할 경우 Lock 경합으로 인해 동시 처리 성능(Throughput)이 급감하는 문제 발생
- 필요성: 애플리케이션의 성격(성능 우선 vs 정합성 우선)에 따라 동시성과 데이터 정합성 간의 최적 타협점을 선택하기 위해 필요함

---

## Ⅱ. 구조 및 구성요소 (4단계 격리 수준)

```text
Performance (High) <-------------------------------------> Consistency (High)
Read Uncommitted -> Read Committed -> Repeatable Read -> Serializable
 (Level 0)           (Level 1)         (Level 2)          (Level 3)
```

| 격리 수준 | 허용/차단 기준 | 실무 적용 |
|:---|:---|:---|
| Read Uncommitted | 커밋되지 않은 데이터도 읽기 허용 (격리 안 함) | 로깅, 통계 추출 등 정합성이 덜 중요한 곳 |
| Read Committed | 커밋이 완료된 데이터만 읽기 허용 | Oracle 기본값, 일반적인 웹 서비스 |
| Repeatable Read | 트랜잭션 내 동일 쿼리는 동일 결과 보장 | MySQL 기본값, 금융/결제 일부 로직 |
| Serializable | 모든 트랜잭션을 순차적으로 직렬화하여 실행 | 완벽한 무결성이 요구되는 제한적 특수 상황 |

> 요약: 성능을 중시하는 Level 0부터 정합성을 중시하는 Level 3까지 4단계 스펙트럼으로 구성된다.

---

## Ⅲ. 동작원리 및 방어 흐름도 (이상 현상 매핑)

```text
Tx 동시 실행 -> Isolation Level 설정 확인 -> 발생 가능한 Read Anomaly 필터링
           |-> Level 0: Dirty Read, Non-Repeatable Read, Phantom Read 방치
           |-> Level 1: Dirty Read 차단
           |-> Level 2: Non-Repeatable Read 차단 (일부 Phantom 방어)
           |-> Level 3: Phantom Read까지 모두 차단 (Lock/MVCC 직렬화)
```

- 1단계 [격리 기준 판단]: 트랜잭션 A가 읽는 도중 트랜잭션 B가 데이터를 변경/커밋함
- 2단계 [Level 1 방어]: Read Committed는 B가 '커밋'할 때까지 A에게 변경 전 데이터를 보여주어 Dirty Read 방어
- 3단계 [Level 2 방어]: Repeatable Read는 B가 커밋하더라도, A가 시작될 당시의 스냅샷만 보여주어 Non-Repeatable Read 방어
- 4단계 [Level 3 방어]: Serializable은 A가 읽은 영역에 B가 새로 삽입(Insert)하는 것까지 락으로 막아 Phantom Read 원천 차단

> 요약: 격리 수준이 올라갈수록 DB 엔진은 Read Lock 유지 범위를 늘리거나 더 오래된 MVCC 스냅샷을 유지하여 이상 현상을 차단한다.

---

## Ⅳ. 특징 (비교)

| 비교 축 | Read Committed (Level 1) | Repeatable Read (Level 2) |
|:---|:---|:---|
| 구현 방식 | 쿼리문이 실행될 때마다 새 스냅샷(버전) 생성 | 트랜잭션이 시작될 때 단 한 번 스냅샷 생성 |
| 이상 현상 노출 | Dirty Read 방어 / NRR, Phantom 발생 | NRR 방어 / Phantom 발생 (MySQL은 완화) |
| 대표적 기본값 | Oracle, PostgreSQL | MySQL (InnoDB) |
| 성능 병목 | 적음 (잠금 최소화) | 스냅샷 유지로 인한 UNDO 테이블스페이스 증가 |

> 요약: 실무에서 가장 많이 고민하는 구간은 Level 1과 Level 2 사이이며, DBMS의 MVCC 구현 방식에 따라 방어 범위가 미세하게 다르다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 동시성 (Concurrency) | 데이터 정합성 (Consistency) | 선택 기준 |
|:---|:---|:---|:---|
| Read Uncommitted | 최고 (Lock 없음) | 최하 (Dirty Read) | 1초 단위 실시간 대시보드 통계 |
| Read Committed | 높음 | 보통 | 일반적인 게시판, 이커머스 상품 조회 |
| Repeatable Read | 보통 | 높음 | 정산, 리포트 생성, 결제 트랜잭션 |
| Serializable | 최하 (테이블/범위 Lock) | 최고 | 재고 차감 등 초정밀 동시성 제어 필요 시 |

> 요약: 격리 수준을 높이는 것은 성능 저하를 직결하므로, 비즈니스 성격이 허용하는 가장 낮은 수준의 격리를 선택하는 것이 유리하다.

**리스크·대응 (기본은 불릿):**
- MySQL Phantom Read: 표준에서는 Level 2에서 Phantom Read가 발생하나, MySQL InnoDB는 넥스트 키 락(Next-Key Lock)과 MVCC를 통해 이를 자체 차단함 (지표: Deadlock 발생 빈도)
- Undo 영역 비대화: Repeatable Read 환경에서 장기 실행 트랜잭션(Long Transaction) 존재 시 과거 스냅샷 유지로 디스크 풀(Disk Full) 장애 위험 → 트랜잭션 타임아웃 설정 및 배치 분할

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 기본 격리수준 유지 및 낙관적 락(Optimistic Lock): DB는 Read Committed/Repeatable Read를 유지하고, 애플리케이션 계층에서 버전(Version) 컬럼을 이용한 낙관적 락으로 동시 갱신 방어
2. 분리 아키텍처 (CQRS): 쓰기(Command) DB는 Repeatable Read 이상으로 엄격히 관리하고, 읽기(Query) DB는 복제본을 활용해 Read Uncommitted 수준으로 성능 극대화
3. 조회 특화 분리: 배치 리포트처럼 일관된 조회가 필요한 경우 의도적으로 세션 단위 격리 수준을 Repeatable Read로 상향 설정하여 실행

**결론 (2줄):**
- 기술사 판단: 격리 수준은 동시성과 정합성의 시소게임이므로, 맹목적으로 Serializable을 선택하기보다는 발생 가능한 이상 현상(Anomalies)을 애플리케이션 레벨에서 허용/제어할 수 있는지 먼저 판단해야 한다
- 향후 방향: 최근 분산 DB(Spanner 등)에서는 TrueTime API를 활용하여 성능 저하 없이 직렬화 가능(Strict Serializable) 수준을 제공하는 방향으로 진화하고 있다

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 설명형 | "격리 수준 4단계 설명", "차이점" | 단계별 허용 이상 현상 차단 메커니즘 | 동시성/정합성 트레이드오프 표 |
| 방안형 | "동시성 제어 시 문제점과 방안" | Lock 경합으로 인한 성능 저하 원리 | 격리 수준 하향 + 낙관적 락 복합 적용 방안 |
