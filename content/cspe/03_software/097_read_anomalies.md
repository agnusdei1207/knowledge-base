---
title: "Dirty Read·Non-Repeatable Read·Phantom Read (Read Anomalies)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 97
extra:
  question_no: "097"
  exam_status: "기출"
  exam_history: "136회"
---

## 미리 알고가기

- 읽기 이상 현상은 동시성 환경에서 조회 결과가 기대와 다르게 흔들리는 문제임
- Dirty Read, Non-Repeatable Read, Phantom Read는 대표적인 정합성 이상 현상임
- 격리 수준과 락 방식과 MVCC 구현이 발생 여부를 좌우함

## Ⅰ. 개요

- **정의/개념**: 읽기 이상 현상은 여러 트랜잭션이 동시에 실행될 때 한 트랜잭션의 읽기 결과가 다른 트랜잭션의 미완료 변경이나 재조회 시점 차이 때문에 일관되지 않게 나타나는 동시성 문제임
- **배경/필요성**: 업무 시스템에서 조회 결과가 시점마다 달라지면 잘못된 판단과 중복 처리와 감사 불일치가 발생하므로, 각 이상 현상의 의미와 방지 수준을 이해해야 함

## Ⅱ. 특징

- Dirty Read는 아직 커밋되지 않은 값을 읽는 문제임
- Non-Repeatable Read는 같은 조건 재조회 시 값이 달라지는 문제임
- Phantom Read는 같은 조건 재조회 시 행 집합이 달라지는 문제임
- 이상 현상별로 필요한 제어 방식이 달라 단순 락 추가만으로 항상 해결되지는 않음

## Ⅲ. 종류 및 비교

| 판단 기준 | Dirty Read | Non-Repeatable Read | Phantom Read |
|:---|:---|:---|:---|
| 원인 | 미커밋 데이터 노출 | 다른 트랜잭션의 갱신 커밋 | 다른 트랜잭션의 삽입·삭제 |
| 영향 | 롤백 데이터 오판 | 재조회 불일치 | 집계·검색 결과 집합 변동 |
| 주 방지 수단 | 커밋 후 읽기 | 반복 읽기 보장 | 범위 잠금·직렬화 |
| 대표 위험 | 잘못된 업무 판단 | 중간 상태 처리 오류 | 조건 기반 처리 누락·중복 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Read Operation | 조회 시점과 범위가 이상 현상 노출 여부를 결정함 |
| Concurrent Writer | 다른 트랜잭션의 갱신과 삽입과 삭제가 읽기 결과를 흔듦 |
| Isolation Rule | 읽기 허용 범위를 제한해 이상 현상을 줄이거나 차단함 |
| Detection and Retry | 이상 현상 가능 영역을 감시하고 필요 시 재시도나 재검증을 수행함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 조회 시작      | --> | 동시 변경 발생   | --> | 재조회/범위 조회 | --> | 결과 불일치 판정 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **조회 시작**: 한 트랜잭션이 데이터를 읽음
2. **동시 변경 발생**: 다른 트랜잭션이 갱신이나 삽입을 수행함
3. **재조회 또는 범위 조회**: 같은 조건으로 다시 읽음
4. **결과 불일치 판정**: 이상 현상 종류를 식별함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 읽기 이상 현상을 단순 조회 오차로 간주하면 재고와 회계와 집계 로직에서 중대한 업무 오류가 누적될 수 있음
   - 해결방안: anomaly-sensitive transaction을 식별하고 consistency defect count와 reconciliation error rate로 검증함
2. 문제: 모든 이상 현상을 동일한 방식으로 막으려 하면 불필요한 직렬화 비용이 발생할 수 있음
   - 해결방안: anomaly type별 control policy를 적용하고 serialization overhead와 prevented anomaly rate로 검증함
3. 문제: 애플리케이션이 재조회 차이를 허용하지 않으면서도 보정 로직이 없으면 사용자 경험과 데이터 신뢰성이 동시에 낮아질 수 있음
   - 해결방안: idempotent retry와 post-read validation을 결합하고 stale read incident count와 user-visible inconsistency rate로 검증함

## Ⅶ. 적용 사례

- 재고 예약 시스템에서는 이상 현상 민감 트랜잭션을 분류하고 확인 지표는 consistency defect count와 reconciliation error rate임
- 대량 집계 배치에서는 제어 정책을 구분하고 확인 지표는 serialization overhead와 prevented anomaly rate임
- 사용자 조회 서비스에서는 보정 로직을 추가하고 확인 지표는 stale read incident count와 user-visible inconsistency rate임

## Ⅷ. 결론

읽기 이상 현상 관리는 데이터베이스 이론 암기가 아니라 어떤 업무에서 어떤 불일치를 허용할 수 없는지 구체적으로 식별하는 작업임.
