---
title: "Exactly-Once Semantics 정확히 한 번 처리 (Exactly-Once Semantics)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 314
extra:
  question_no: "314"
  exam_status: "기출"
  exam_history: "136회"
---

## 미리 알고가기

- Exactly-Once Semantics는 이벤트가 중복 없이 한 번만 처리된 것과 같은 결과를 보장하려는 처리 의미임
- 단일 시스템 내부 보장과 외부 sink까지 포함한 종단간 보장은 난도가 다름
- checkpoint와 transaction과 idempotent sink 설계가 함께 맞아야 실효성이 생김

## Ⅰ. 개요

- **정의/개념**: Exactly-Once Semantics는 장애와 재시도 상황이 있어도 각 이벤트가 논리적으로 한 번만 반영된 것과 동일한 결과를 보장하도록 상태와 출력과 오프셋을 일관되게 관리하는 처리 보장 모델임
- **배경/필요성**: 결제와 재고와 정산처럼 중복 반영이 직접 손실로 이어지는 업무가 늘면서 at least once 재처리만으로는 비즈니스 정합성을 유지하기 어려워짐

## Ⅱ. 특징

- 단순 메시지 수신 보장이 아니라 상태 업데이트와 외부 출력 일관성까지 다룸
- checkpoint와 transaction을 결합해 재시작 시 중복 반영을 줄이는 구조가 일반적임
- idempotent sink를 쓰면 구현 복잡도를 줄이면서 실질 exactly-once에 근접할 수 있음
- 외부 시스템이 transaction을 지원하지 않으면 종단간 보장을 구현하기 어려움

## Ⅲ. 종류 및 비교

| 판단 기준 | At-Most-Once | At-Least-Once | Exactly-Once Semantics |
|:---|:---|:---|:---|
| 중복 가능성 | 없음 | 있음 | 없음 |
| 유실 가능성 | 있음 | 낮음 | 낮음 |
| 구현 복잡도 | 낮음 | 중간 | 높음 |
| 대표 용도 | 모니터링 로그 | 일반 이벤트 처리 | 결제, 정산, 재고 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Source Offset Tracking | 어떤 이벤트까지 읽었는지 위치를 관리해 재시작 시 처리 경계를 정확히 복원하는 입력 기준점임 |
| Stateful Processing Core | 집계와 조인과 비즈니스 상태를 유지하면서 입력 이벤트를 반영해 논리적 결과를 만드는 연산 핵심부임 |
| Checkpoint Coordinator | 상태와 오프셋을 같은 시점으로 고정해 복구 후 중복 재처리 범위를 제한하는 일관성 제어 계층임 |
| Transactional or Idempotent Sink | 외부 시스템 반영 시 중복 쓰기를 막아 엔드 투 엔드 보장의 마지막 고리를 형성하는 출력 계층임 |
| Recovery Controller | 장애 발생 시 마지막 일관 시점부터 재개해 처리 결과를 보정하는 복구 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| Source      | -> | Stateful    | -> | Checkpoint  | -> | Sink        |
| Offset      |    | Processing  |    | / Tx Coord  |    | Verify      |
+-------------+    +-------------+    +-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 이벤트 읽기   | -> | 상태 반영     | -> | 체크포인트 생성 | -> | sink 커밋    | -> | 장애 시 복구  |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **이벤트 읽기**: source offset 기준으로 새 이벤트를 수신함
2. **상태 반영**: 연산 상태에 이벤트 결과를 적용함
3. **체크포인트 생성**: 상태와 오프셋을 일관된 지점으로 저장함
4. **sink 커밋**: transaction 또는 idempotent write로 외부 반영함
5. **장애 시 복구**: 마지막 일관 시점부터 다시 실행해 중복과 유실을 줄임

## Ⅵ. 문제점 및 해결 방안

1. 문제: 외부 sink가 transaction이나 idempotency를 지원하지 않으면 내부 엔진이 정확한 복구를 해도 종단간 중복 반영이 남을 수 있음
   - 해결방안: idempotent sink contract와 deduplication key policy를 적용하고 duplicate output rate와 sink idempotency coverage로 검증함
2. 문제: 체크포인트와 분산 transaction 비용이 커지면 지연과 처리량이 악화되어 실시간성 요구와 충돌할 수 있음
   - 해결방안: checkpoint interval tuning과 critical flow selective EOS를 적용하고 checkpoint overhead ratio와 end to end latency impact로 검증함
3. 문제: 여러 시스템을 연결한 종단간 exactly-once 설계가 지나치게 복잡하면 운영자가 실패 원인을 빠르게 파악하기 어려워질 수 있음
   - 해결방안: recovery traceability logging과 failure mode runbook을 적용하고 mean time to diagnose replay issue와 manual recovery error count로 검증함

## Ⅶ. 적용 사례

- 정산 파이프라인이 idempotent sink 계약을 적용하며 확인 지표는 duplicate output rate와 sink idempotency coverage임
- 실시간 이벤트 처리 서비스가 선택적 EOS 전략을 운영하며 확인 지표는 checkpoint overhead ratio와 end to end latency impact임
- 운영 조직이 재처리 추적 로그를 강화하며 확인 지표는 mean time to diagnose replay issue와 manual recovery error count임

## Ⅷ. 결론

Exactly-Once Semantics는 엔진 기능만으로 완성되지 않으므로 source와 state와 sink를 한 일관성 경계로 설계할 때 비로소 실효성이 생김.
