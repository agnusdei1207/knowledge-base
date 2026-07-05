---
title: "트랜잭션 격리 수준 (Isolation Level)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-software"
weight: 96
---

## 핵심 인사이트 (3줄 요약)
- 복수의 트랜잭션이 동시에 실행될 때, "서로의 데이터 변경 사항을 어느 수준까지 엿볼 수 있게 허용할 것인가?"를 통제하는 4단계의 엄격도 기준(ANSI SQL-92 표준).
- 레벨이 높을수록 데이터 정합성(정확도)은 완벽해지지만, DB에 걸리는 락(Lock)이 많아져 성능(동시 처리량)은 바닥으로 떨어지는 치명적인 **트레이드오프** 관계에 있음.
- 대부분의 실무 상용 DB(Oracle, MySQL)는 성능 저하를 막기 위해 완벽한 격리를 포기하고, 적절한 타협점인 **Read Committed** 또는 **Repeatable Read**를 기본값(Default)으로 사용함.
---
## Ⅰ. 개요 및 필요성
- **개요**: ACID 속성 중 하나인 격리성(Isolation)을 유연하게 조절하기 위해 정의된 4단계 수준 (Read Uncommitted ➡️ Read Committed ➡️ Repeatable Read ➡️ Serializable).
- **필요성**: 모든 트랜잭션을 한 줄로 세워 순서대로 처리(직렬화)하면 동시성 에러는 없지만 쇼핑몰 결제가 1시간씩 걸림. "약간의 데이터 불일치(읽기 이상 현상)는 비즈니스적으로 참아줄 테니, 제발 속도 좀 높여달라"는 성능적 요구 때문에 등장함.
---
## Ⅱ. 아키텍처 및 핵심 원리
- **트랜잭션 격리 4단계 (Level 0 ~ 3)**:
  1. **Read Uncommitted (Lv.0)**:
     - 커밋되지 않은(아직 롤백될 수도 있는) 남의 데이터를 그냥 읽어버림. (가장 빠르나 엉망진창).
  2. **Read Committed (Lv.1) - [Oracle 기본값]**:
     - 커밋이 완료된 확실한 데이터만 읽음. 단, 똑같은 데이터를 두 번 읽는 사이에 남이 데이터를 수정해 버리면 값이 달라질 수 있음.
  3. **Repeatable Read (Lv.2) - [MySQL(InnoDB) 기본값]**:
     - 내가 트랜잭션을 시작한 시점의 데이터 스냅샷을 보장함. 두 번 읽어도 값이 같음. 단, 남이 새로운 행(Row)을 추가해 버리면 두 번째 읽을 때 갑자기 안 보이던 데이터가 생겨남(유령 현상).
  4. **Serializable (Lv.3)**:
     - 완벽한 직렬화. 내가 데이터를 읽고 있으면 남들은 쳐다보지도 못함(Table/Range Lock). (가장 안전하나 극악의 속도).

```text
[ 격리 수준(Isolation Level)과 성능/정합성 트레이드오프 ]

 (성능 최고, 정합성 최악) -----------------------------------> (성능 최악, 정합성 완벽)
 [ Read Uncommitted ] ➡️ [ Read Committed ] ➡️ [ Repeatable Read ] ➡️ [ Serializable ]
        |                      |                      |                      |
 ❌ Dirty Read 발생        ❌ Non-Repeatable     ❌ Phantom Read       ✅ 모든 이상현상 방어
                         Read 발생             발생                  (완벽한 직렬화)
```
---
## Ⅲ. 비교 및 연결
| 이상 현상 (Anomaly) | 원인 및 현상 | 어느 레벨에서 방어되는가? |
|---|---|---|
| **Dirty Read (오염된 읽기)** | 트랜잭션 A가 값을 100 ➡️ 200으로 바꿨지만 커밋 안 함. B가 200을 읽어감. A가 롤백함. B는 가짜(200)를 가진 셈. | **Read Committed**부터 방어됨 |
| **Non-Repeatable Read (반복 불가능 읽기)** | A가 값을 읽음. B가 값을 수정하고 커밋함. A가 다시 읽으니 값이 달라짐. | **Repeatable Read**부터 방어됨 |
| **Phantom Read (유령 읽기)** | A가 `AGE>20`인 사람을 검색함(2명). B가 25세 사람을 INSERT 커밋함. A가 다시 검색하니 3명이 튀어나옴(유령). | **Serializable**에서만 방어됨 |
---
## Ⅳ. 실무 적용 및 기술사 판단
- **MySQL (InnoDB)의 마법 (MVCC)**: MySQL은 기본값이 Repeatable Read임. 이론상 Phantom Read(유령 읽기)가 발생해야 하지만, 실제로는 다중 버전 동시성 제어(MVCC)의 언두 로그(Undo Log)와 넥스트 키 락(Next-Key Lock) 기술을 결합하여, **Serializable 급의 락을 걸지 않고도 Phantom Read를 99% 막아내는 기적**을 보여줌. 기술사 답안 작성 시 이 MVCC 아키텍처의 우수성을 반드시 어필해야 함.
- **Lost Update (갱신 손실) 방어**: 두 트랜잭션이 동시에 같은 게시글 조회수를 올릴 때, 값이 덮어씌워져 1만 올라가는 치명적 현상. 이는 Isolation Level만으로 해결되지 않으며, 개발자가 소스코드에서 `SELECT ... FOR UPDATE` 구문(비관적 락)이나 버전(Version) 컬럼을 활용한 '낙관적 락(Optimistic Lock)' 패턴을 명시적으로 적용해야 해결 가능함.
---
## Ⅴ. 기대효과 및 결론
- 개발자와 DBA에게 '데이터의 완벽성'과 '시스템의 응답 속도' 사이에서 비즈니스 성격(예: 통계 배치 vs 금융 결제)에 맞는 최적의 다이얼을 돌릴 수 있는 통제권을 부여함.
- 클라우드 대규모 분산 데이터베이스 시대에도 이 격리 수준의 원리는 변하지 않으며, 구글 Spanner 같은 최신 DB들은 TrueTime API(원자 시계)를 동원해 '성능 저하 없는 Serializable'이라는 꿈의 경지에 도전하고 있음.
---
### 📌 관련 개념 맵
- 트랜잭션(ACID) ➡️ 이상 현상 (Dirty/Phantom Read) ➡️ 격리 수준 (Isolation Level) ➡️ MVCC 및 Locking

### 📈 관련 키워드 및 발전 흐름도
- 순차 처리 ➡️ 비관적 락(Pessimistic Lock)의 성능 저하 ➡️ ANSI SQL 격리 수준 정의 ➡️ MVCC(다중 버전 동시성 제어) 혁명

### 👶 어린이를 위한 3줄 비유 설명
1. 선생님(트랜잭션 A)이 칠판에 시험 정답을 고쳐 적고 있는데, 아직 다 안 썼어요.
2. 0단계(Uncommitted)는 학생이 칠판을 훔쳐보고 틀린 답을 베껴가는 최악의 상황이에요 (Dirty Read).
3. 2단계(Repeatable Read)는 학생이 눈을 감았다 뜰 때마다 칠판의 글씨가 바뀌지 않도록(정답 유지), 선생님이 학생이 다 볼 때까지 칠판을 가려주는 마법이랍니다!
