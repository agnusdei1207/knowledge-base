---
title: "BASE vs ACID (BASE vs ACID)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 119
extra:
  question_no: "119"
  exam_status: "기출"
  exam_history: "121회, 131회"
---

## 미리 알고가기

- ACID는 강한 정합성과 복구를 중심으로 한 트랜잭션 원칙임
- BASE는 가용성과 분산 확장을 위해 일시적 불일치를 허용하는 접근임
- 둘은 우열 관계가 아니라 업무 요구에 따른 선택 축임

## Ⅰ. 개요

- **정의/개념**: ACID는 원자성과 일관성과 고립성과 지속성으로 핵심 업무 데이터의 신뢰성을 보장하는 트랜잭션 원칙이고, BASE는 Basically Available, Soft state, Eventually consistent를 기반으로 분산 시스템에서 가용성과 확장성을 우선하는 데이터 처리 접근임
- **배경/필요성**: 모든 서비스가 같은 수준의 정합성을 필요로 하지 않으므로, 핵심 거래와 대규모 분산 조회를 같은 모델로 처리하면 성능과 비용이 모두 비효율적일 수 있음

## Ⅱ. 특징

- ACID는 오류와 동시성 상황에서도 강한 정합성을 제공함
- BASE는 노드 분산과 가용성을 높이기 위해 일시적 불일치를 허용함
- ACID는 지연과 동시성 비용이 커질 수 있음
- BASE는 보정 로직과 사용자 기대 관리가 필수임

## Ⅲ. 종류 및 비교

| 판단 기준 | ACID | BASE |
|:---|:---|:---|
| 우선 가치 | 정합성과 복구 | 가용성과 확장성 |
| 데이터 상태 | 즉시 일관성 지향 | 최종 일관성 지향 |
| 강점 | 금융·주문 핵심 처리 안정 | 대규모 분산 처리 유연 |
| 한계 | 분산 환경 비용 증가 | 일시적 불일치 대응 필요 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Consistency Model | 최신 상태를 언제 보장할지 정해 업무 신뢰성을 좌우함 |
| Failure Handling | ACID는 rollback과 recovery를, BASE는 retry와 reconcile을 중시함 |
| Availability Strategy | BASE는 요청 지속 처리를, ACID는 정합성 보호를 우선시할 수 있음 |
| Compensation Logic | BASE 환경에서는 지연 동기화와 보정 흐름이 별도 필요함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 업무 중요도 파악 | --> | 정합성 모델 선택 | --> | 처리/복구 설계  | --> | 운영 검증      |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **업무 중요도 파악**: 최신 정합성 요구 수준을 식별함
2. **정합성 모델 선택**: ACID 또는 BASE 성향을 정함
3. **처리와 복구 설계**: rollback 또는 보정 로직을 구축함
4. **운영 검증**: 오류와 지연과 불일치 영향을 측정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 핵심 거래에 BASE 성향을 무비판적으로 적용하면 일시적 불일치가 곧 금전 손실과 업무 오류로 이어질 수 있음
   - 해결방안: business criticality별 consistency tier를 분리하고 wrong-tier assignment count와 reconciliation loss rate로 검증함
2. 문제: BASE를 선택하고도 보정 로직과 사용자 안내를 설계하지 않으면 운영 복잡도가 폭증할 수 있음
   - 해결방안: compensation workflow와 UX notice를 포함하고 reconciliation completion rate와 user confusion rate로 검증함
3. 문제: ACID가 필요한 영역과 아닌 영역을 같은 저장 경로로 묶으면 전체 시스템 지연과 비용이 불필요하게 커질 수 있음
   - 해결방안: polyglot persistence를 적용하고 average transaction cost와 workload fit score로 검증함

## Ⅶ. 적용 사례

- 결제 시스템에서는 일관성 등급을 분리하고, wrong-tier assignment count와 reconciliation loss rate로 결과를 확인함
- 대규모 피드 서비스에서는 보정 흐름을 운영하고, reconciliation completion rate와 user confusion rate로 결과를 확인함
- 복합 서비스 플랫폼에서는 저장소를 분리하고, average transaction cost와 workload fit score로 결과를 확인함

## Ⅷ. 결론

BASE와 ACID 비교의 핵심은 어느 쪽이 더 좋으냐가 아니라 어떤 업무가 어느 수준의 정합성과 가용성을 요구하는지 명확히 나누는 데 있음.
