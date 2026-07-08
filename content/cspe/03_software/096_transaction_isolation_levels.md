---
title: "트랜잭션 격리 수준 4단계 (Transaction Isolation Levels)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 96
extra:
  question_no: "096"
  exam_status: "기출"
  exam_history: "120회, 136회, 138회"
---

## 미리 알고가기

- 격리 수준은 동시에 실행되는 트랜잭션 간 간섭 허용 범위를 정하는 정책임
- 일반적으로 Read Uncommitted, Read Committed, Repeatable Read, Serializable 순으로 강해짐
- 수준이 높을수록 정합성은 좋아지지만 경합 비용도 커질 수 있음

## Ⅰ. 개요

- **정의/개념**: 트랜잭션 격리 수준은 동시에 수행되는 여러 트랜잭션이 서로의 중간 상태를 얼마나 볼 수 있는지와 갱신 간섭을 어느 정도 허용할지를 정하는 동시성 제어 정책임
- **배경/필요성**: 핵심 업무 데이터는 정합성을 지켜야 하지만 모든 상황에 최고 격리를 적용하면 성능이 급격히 저하되므로, 업무 특성에 맞는 균형점이 필요함

## Ⅱ. 특징

- 허용 가능한 읽기 이상 현상 범위를 기준으로 수준을 구분함
- 데이터 정합성과 처리량 사이의 트레이드오프를 직접 조정할 수 있음
- DBMS 구현 방식에 따라 같은 이름의 수준이라도 세부 동작이 다를 수 있음
- 운영 중 격리 수준 선택 오류는 성능 저하나 데이터 불일치로 즉시 나타남

## Ⅲ. 종류 및 비교

| 판단 기준 | Read Committed | Repeatable Read | Serializable |
|:---|:---|:---|:---|
| Dirty Read 방지 | 가능 | 가능 | 가능 |
| Non-Repeatable Read 방지 | 제한적 | 가능 | 가능 |
| Phantom Read 방지 | 제한적 | 구현 의존 | 가능 |
| 성능 부담 | 낮음 | 중간 | 높음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Read Policy | 다른 트랜잭션의 커밋 상태를 어디까지 볼지 결정함 |
| Lock or Version Rule | 락 또는 버전 기반으로 충돌을 제어해 격리 수준을 구현함 |
| Conflict Detection | 갱신 충돌과 읽기 충돌을 판정해 재시도나 대기를 유발함 |
| Workload Mapping | 업무별로 필요한 정합성 수준을 선택해 불필요한 경합을 줄임 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 업무 특성 파악  | --> | 격리 수준 선택  | --> | 충돌 제어 수행  | --> | 성능/정합 검증  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **업무 특성 파악**: 정합성 요구와 동시 요청 패턴을 확인함
2. **격리 수준 선택**: 허용 가능한 이상 현상 범위를 정함
3. **충돌 제어 수행**: 락이나 버전 규칙으로 간섭을 통제함
4. **성능과 정합 검증**: 경합과 재시도와 오류를 관찰함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 업무 중요도를 구분하지 않고 높은 격리 수준을 일괄 적용하면 락 대기와 처리 지연이 급증할 수 있음
   - 해결방안: workload별 isolation profile을 분리하고 lock wait time과 transaction latency로 검증함
2. 문제: 낮은 격리 수준을 선택한 뒤 이상 현상 감지를 하지 않으면 정합성 오류가 운영에서 누적될 수 있음
   - 해결방안: anomaly monitoring과 business validation을 추가하고 consistency incident count와 retry success rate로 검증함
3. 문제: 애플리케이션 재시도 전략이 DB 충돌 정책과 맞지 않으면 오류 복구보다 장애 확대가 쉬워질 수 있음
   - 해결방안: retry policy를 격리 수준과 함께 설계하고 deadlock retry effectiveness와 duplicate transaction rate로 검증함

## Ⅶ. 적용 사례

- 주문 처리 시스템에서는 격리 프로파일을 분리하고 확인 지표는 lock wait time과 transaction latency임
- 재고 관리 서비스에서는 이상 현상 감시를 운영하고 확인 지표는 consistency incident count와 retry success rate임
- 금융 이체 플랫폼에서는 재시도 정책을 정합성 기준과 연계하고 확인 지표는 deadlock retry effectiveness와 duplicate transaction rate임

## Ⅷ. 결론

격리 수준 선택의 핵심은 가장 강한 옵션을 고르는 데 있지 않고 업무 정합성과 동시성 비용 사이의 균형을 설계하는 데 있음.
