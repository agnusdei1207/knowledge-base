---
title: "Saga 패턴 — 분산 트랜잭션 (Saga Pattern)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 48
extra:
  question_no: "048"
  exam_status: "기출"
  exam_history: "121회"
---

## 미리 알고가기

- Saga는 분산 서비스 간 긴 트랜잭션을 로컬 트랜잭션 연쇄로 나누는 패턴임
- 각 단계 실패 시 보상 트랜잭션으로 이전 효과를 되돌림
- orchestration 방식과 choreography 방식으로 나뉨

## Ⅰ. 개요

- **정의/개념**: Saga 패턴은 여러 서비스에 걸친 하나의 비즈니스 흐름을 각 서비스의 로컬 트랜잭션과 보상 트랜잭션으로 분해해 분산 트랜잭션을 처리하는 패턴임
- **배경/필요성**: MSA 환경에서는 전통적 2PC가 성능과 가용성과 결합도 측면에서 부담이 크므로, eventual consistency를 수용하는 대안적 분산 트랜잭션 방식이 필요함

## Ⅱ. 특징

- 각 서비스가 독립 DB를 유지하면서도 비즈니스 흐름을 이어갈 수 있음
- 실패 복구를 보상 로직으로 처리하므로 가용성은 높지만 설계 난도도 큼
- 오케스트레이션은 흐름 가시성이 좋고 choreography는 결합이 낮음
- 보상 불가능한 작업이 포함되면 패턴 적용이 어려워짐

## Ⅲ. 종류 및 비교

| 판단 기준 | Orchestration | Choreography |
|:---|:---|:---|
| 제어 방식 | 중앙 오케스트레이터가 단계 제어 | 이벤트 기반으로 각 서비스가 자율 반응 |
| 장점 | 흐름 추적과 가시성 우수 | 중앙 결합 낮음 |
| 한계 | 오케스트레이터 의존성 | 흐름 추적과 디버깅 어려움 |
| 적합 환경 | 복잡한 순서 제어 | 느슨한 이벤트 협력 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Local Transaction | 각 서비스 안에서 원자적으로 수행되는 최소 작업 단위임 |
| Compensation Action | 실패 시 이전 효과를 되돌려 비즈니스 정합성을 회복하는 핵심 수단임 |
| Saga Coordinator or Event Flow | 전체 순서를 중앙에서 통제하거나 이벤트 흐름으로 연결해 분산 상태를 이끎 |
| State Tracking | 현재 saga 단계와 실패 위치를 추적해 재시도와 보상을 정확히 실행하게 함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 단계 실행      | --> | 다음 단계 전달 | --> | 실패 감지      | --> | 보상 수행      |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **단계 실행**: 첫 서비스가 로컬 트랜잭션을 수행함
2. **다음 단계 전달**: 오케스트레이터나 이벤트로 다음 서비스에 흐름을 넘김
3. **실패 감지**: 어느 단계에서 실패했는지 상태를 확인함
4. **보상 수행**: 이전 단계들을 역순 또는 정의된 규칙대로 보상함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 보상 트랜잭션이 실제 비즈니스 상태를 완전히 원복하지 못하면 정합성 사고가 남을 수 있음
   - 해결방안: 보상 가능성 분석과 도메인 검증을 수행하고 compensation success rate와 residual inconsistency count로 검증함
2. 문제: choreography 기반 saga는 이벤트가 많아질수록 흐름 추적과 장애 분석이 어려워질 수 있음
   - 해결방안: correlation ID와 tracing을 적용하고 saga trace completeness와 MTTR로 검증함
3. 문제: 동일 이벤트 재처리나 중복 요청이 겹치면 의도치 않은 중복 보상이나 중복 실행이 발생할 수 있음
   - 해결방안: idempotency와 상태 저장을 강화하고 duplicate execution rate와 idempotency miss count로 검증함

## Ⅶ. 적용 사례

- 주문·결제·재고 연동에서는 saga를 적용하고, compensation success rate와 residual inconsistency count로 결과를 확인함
- 이벤트 중심 MSA에서는 choreography를 사용하고, saga trace completeness와 duplicate execution rate로 결과를 확인함
- 복잡한 승인 흐름에서는 orchestration을 사용하고, MTTR와 idempotency miss count로 결과를 확인함

## Ⅷ. 결론

Saga 패턴은 분산 트랜잭션을 없애는 기술이 아니라 중앙 락 대신 보상과 추적을 감당하겠다는 설계 선택임.
