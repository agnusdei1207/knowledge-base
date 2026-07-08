---
title: "CRDT 충돌 없는 복제 데이터 (Conflict-free Replicated Data Type)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 121
extra:
  question_no: "121"
  exam_status: "기출"
  exam_history: "124회"
---

## 미리 알고가기

- CRDT는 분산 복제본이 독립적으로 업데이트돼도 자동 병합으로 수렴하도록 설계된 자료구조임
- commutative 연산 또는 state merge 규칙이 핵심임
- 협업 편집과 오프라인 동기화에서 자주 활용됨

## Ⅰ. 개요

- **정의/개념**: CRDT는 여러 복제본이 네트워크 분할이나 오프라인 상태에서 독립적으로 갱신되더라도 미리 정의된 병합 규칙으로 충돌 없이 동일 상태로 수렴하도록 만든 분산 자료구조임
- **배경/필요성**: 사용자 동시 편집과 엣지·모바일 오프라인 환경에서는 중앙 직렬화 없이도 데이터 수렴을 보장할 자료구조가 필요함

## Ⅱ. 특징

- 중앙 락 없이도 로컬 업데이트를 계속 처리할 수 있음
- 병합 규칙만 지키면 복제본이 결국 같은 상태로 수렴함
- 단순 last-write-win보다 의미 보존에 유리함
- 모든 데이터 모델에 바로 적용되지는 않아 설계 제약이 존재함

## Ⅲ. 종류 및 비교

| 판단 기준 | State-based CRDT | Operation-based CRDT |
|:---|:---|:---|
| 복제 방식 | 전체 상태 병합 | 연산 전파와 적용 |
| 강점 | 구현 직관적 | 네트워크 효율 높음 |
| 한계 | 상태 크기 증가 가능 | 연산 전달 보장 필요 |
| 적합 환경 | 비교적 단순 복제 | 빈번한 상호작용 시스템 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Replica State | 각 노드가 독립적으로 유지하는 현재 자료구조 상태임 |
| Merge Rule | 교환 법칙과 결합 법칙과 멱등성을 만족해 수렴을 보장함 |
| Update Operation | 로컬에서 즉시 적용 가능한 변경 연산을 제공함 |
| Dissemination Channel | 상태나 연산을 다른 복제본에 전파해 수렴을 달성함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 로컬 업데이트   | --> | 상태/연산 전파   | --> | 병합 규칙 적용  | --> | 복제본 수렴     |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **로컬 업데이트**: 각 복제본이 즉시 변경을 반영함
2. **상태 또는 연산 전파**: 다른 노드에 변경 정보를 보냄
3. **병합 규칙 적용**: 충돌 없이 일관된 결과로 통합함
4. **복제본 수렴**: 최종적으로 같은 상태를 형성함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 업무 의미와 맞지 않는 단순 CRDT를 적용하면 기술적으로 수렴해도 비즈니스 관점에서는 잘못된 결과가 나올 수 있음
   - 해결방안: domain semantics review를 수행하고 semantic merge accuracy와 unexpected convergence count로 검증함
2. 문제: 상태 기반 CRDT를 큰 객체에 적용하면 전파 비용과 저장 부담이 과도해질 수 있음
   - 해결방안: delta-based propagation을 적용하고 sync payload size와 convergence latency로 검증함
3. 문제: 병합 결과를 사용자 경험에 반영하는 규칙이 없으면 협업 화면에서 예기치 않은 변경처럼 보일 수 있음
   - 해결방안: merge visibility UX를 설계하고 user merge confusion rate와 conflict resolution explainability score로 검증함

## Ⅶ. 적용 사례

- 협업 편집 서비스에서는 의미 검토를 수행하고, semantic merge accuracy와 unexpected convergence count로 결과를 확인함
- 모바일 오프라인 동기화에서는 델타 전파를 적용하고, sync payload size와 convergence latency로 결과를 확인함
- 실시간 공유 화면에서는 병합 가시성을 설계하고, user merge confusion rate와 conflict resolution explainability score로 결과를 확인함

## Ⅷ. 결론

CRDT의 본질은 충돌을 없애는 마법이 아니라 분산 업데이트가 어떤 규칙으로 수렴해야 하는지를 자료구조 수준에서 미리 설계하는 데 있음.
