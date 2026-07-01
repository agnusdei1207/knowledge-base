---
title: "PACELC 정리 (PACELC Theorem)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 118
---

# 📖 【암기용】 개념 완전 이해

> 목적: PACELC 정리를 처음 보는 사람도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 분산 시스템은 partition 시 C/A를, partition이 없을 때도 latency/consistency를 선택한다는 원칙
- **왜 필요한가**: CAP는 장애 시 선택을 설명하지만 정상 상태에서도 멀리 떨어진 노드 합의를 기다리면 지연이 증가한다. PACELC는 평상시 지연과 일관성 선택까지 함께 본다.
- **핵심 직관**: 비상시에는 정확한 확인과 즉시 처리 중 하나를 고르고, 평상시에도 본점 확인을 매번 기다릴지 지점 판단을 허용할지 선택한다.

## 깊이 이해
- **배경·문제의식**: 글로벌 DB는 리전 간 네트워크 지연이 50~200ms 수준일 수 있다. partition이 없어도 모든 쓰기·읽기에 합의를 요구하면 사용자 지연이 커진다.
- **작동 원리**: PACELC는 `if P then A or C, Else L or C`로 읽는다. 즉, 분할이 있으면 가용성과 일관성 중 선택하고, 분할이 없으면 지연과 일관성 중 선택한다.
- **비유**: 평상시 카드 결제 때 본사 승인을 기다리면 정확하지만 시간이 걸리고, 지점 한도 내 승인하면 지연은 줄지만 나중에 본사 정산이 필요하다.
- **구체 예시**: Dynamo/Cassandra는 PA/EL 성향으로 장애 시 가용성과 평상시 낮은 지연을 우선한다. Spanner는 PC/EC 성향으로 TrueTime과 quorum을 통해 일관성을 우선한다.
- **흔한 오해·주의점**: PACELC는 CAP의 대체가 아니라 확장이다. 장애가 없을 때도 latency-consistency 트레이드오프가 존재한다는 점을 추가한다.

## 연결 개념
- CAP 정리 — partition 시 C/A 선택의 기반
- Dynamo/Cassandra — 가용성과 지연을 중시하는 대표 사례
- Spanner — 글로벌 일관성과 외부 일관성 구현 사례
- Quorum·Timestamp — 일관성 수준과 지연을 조절하는 수단

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: PACELC 답안은 CAP와의 차이를 쓰고, 정상 상태의 latency/consistency 선택을 제품 사례로 비교해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PACELC는 partition 시 A/C 선택, partition이 없을 때 L/C 선택까지 설명하는 분산 DB 트레이드오프 모델이다.
> 2. **가치**: 장애 상황뿐 아니라 정상 운영 중 글로벌 합의 지연과 일관성 보장의 비용을 평가하게 한다.
> 3. **판단 포인트**: Dynamo·Cassandra는 PA/EL, Spanner는 PC/EC 성향으로 비교하고 업무 SLA에 맞춰 선택해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| CAP 확장 이해 확인 | if P then A/C, else L/C 구조 | CAP와 동일한 설명만 반복 |
| 제품별 트레이드오프 비교 확인 | Dynamo, Cassandra, Spanner 성향 | 특정 제품을 절대 CP/AP로 단정 |
| 정상 상태 지연 판단 확인 | quorum, cross-region latency, consistency level | 장애 상황만 설명하고 ELC 부분 누락 |

> 요약: 이 문제는 장애 시뿐 아니라 정상 상태의 지연과 일관성 비용을 함께 판단하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

PACELC는 분산 DB의 장애·정상 상태 선택을 함께 설명하는 원칙이다. CAP가 partition 시 C/A 선택에 초점을 둔다면, PACELC는 partition이 없을 때도 latency와 consistency 사이의 선택이 있음을 제시한다. 글로벌 서비스의 DB 선택과 consistency level 설계에 필요하다.

---

## Ⅱ. 구조 및 구성요소

```text
Distributed DB
  / P 발생 -> A or C 선택
  / Else 정상 -> L or C 선택
PA/EL: Dynamo, Cassandra 성향
PC/EC: Spanner 성향
Workload SLA -> Consistency Level 결정
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| P 조건 | 네트워크 분할 발생 | CAP의 partition 상황 |
| A/C 선택 | 가용성 또는 일관성 우선 | 장애 응답 정책 결정 |
| E 조건 | partition이 없는 정상 상태 | PACELC가 CAP에 추가한 부분 |
| L/C 선택 | 낮은 지연 또는 일관성 우선 | cross-region quorum 비용 반영 |
| 제품 성향 | DB 아키텍처 비교 | Dynamo, Cassandra, Spanner 사례 |

> 요약: PACELC는 partition 조건과 정상 조건을 나누어 분산 DB의 응답 정책과 지연 비용을 설명한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Request 수신 -> partition 상태 판단
  / P 있음 -> A 우선 or C 우선 정책 적용
  / P 없음 -> L 우선 local 응답 or C 우선 quorum 확인
응답 반환 -> lag/conflict/latency 측정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 네트워크 분할·노드 격리 여부 확인 | heartbeat timeout, packet loss |
| 2 | P 상황에서 A/C 정책 적용 | error rate 또는 stale write |
| 3 | 정상 상태에서 L/C 정책 적용 | p95 latency, quorum RTT |
| 4 | consistency level별 읽기·쓰기 경로 선택 | R/W quorum 설정 |
| 5 | 지연·충돌·수렴 지표로 보정 | conflict count, convergence time |

> 요약: PACELC는 요청 시점의 장애 여부에 따라 A/C 또는 L/C 선택 경로를 적용하고, 지연과 충돌 지표로 보정한다.

---

## Ⅳ. 특징

| 구분 | CAP | PACELC | 수치·판단 기준 |
|:---|:---|:---|:---|
| 범위 | partition 상황 | partition + 정상 상황 | 장애·평상시 모두 평가 |
| 선택 축 | C vs A | P: C/A, E: L/C | cross-region RTT 50~200ms |
| 사례 | CP/AP 분류 | PA/EL, PC/EC 분류 | 제품별 consistency level |
| 운영 지표 | 가용성, 불일치 | 지연, 불일치, 수렴 | p95 latency, conflict rate |
| 한계 | 정상 지연 설명 부족 | 모델은 단순화 | 업무별 세부 SLA 필요 |

> 요약: PACELC는 CAP보다 정상 상태의 latency-consistency 비용까지 설명하므로 글로벌 DB 선택에 더 구체적인 기준을 제공한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| Dynamo 계열 | PC/EC | PA/EL | 장바구니·피드처럼 응답 지속과 낮은 지연 |
| Cassandra | tunable consistency | PA/EL~PC/EC 조정 | QUORUM, ONE, ALL 선택 |
| Spanner | PA/EL 대안 | PC/EC | 금융·원장처럼 글로벌 일관성 필요 |
| 단일 리전 DB | 낮은 지연 | 리전 장애 취약 | SLA와 DR 요구 비교 |
| 멀티 리전 DB | 합의 지연 증가 | 일관성 보장 가능 | p95 지연 허용치 |

> 요약: 낮은 지연과 응답 지속이 우선이면 PA/EL, 글로벌 일관성이 핵심이면 PC/EC 성향 DB를 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 지연 증가 | cross-region quorum | 리더 리전 배치, read-only replica | p95/p99 latency |
| 불일치 | 낮은 consistency level | conditional write, read repair | stale read 비율 |
| 장애 오판 | partition 감지 지연 | timeout 튜닝, health check | false failover count |

> 요약: PACELC 리스크는 지연·불일치·지역 비용이며, consistency level과 리전 배치로 조절한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정상 지연 | p95 100ms 이하 등 SLA | tracing, APM |
| 분할 대응 | 장애 시 응답 정책 준수 | chaos test |
| 일관성 | 업무별 stale 허용 시간 | read-after-write test |
| 충돌 | conflict rate 0.1% 이하 | reconciliation log |

> 요약: PACELC 적용은 정상 지연, 장애 응답, 일관성, 충돌, 지역 비용을 동시에 검증해야 한다.

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 업무 분류: 원장·권한은 PC/EC 성향, 피드·추천·장바구니는 PA/EL 성향으로 나누고 stale 허용 시간을 문서화함
2. 제품 설정: Cassandra는 `ONE/QUORUM/ALL`, DynamoDB는 global table 지연, Spanner는 multi-region quorum 지연을 부하테스트로 검증함
3. 리전 설계: 사용자 근접 read replica, 리더 리전 배치, 장애 시 read-only 전환 정책을 p95 지연과 RPO 기준으로 조정함

**결론 (2줄):**
- 기술사 판단: PACELC는 CAP 답안을 확장해 정상 상태 지연까지 설명하므로 글로벌 DB 선택 문제에서 반드시 L/C 축을 포함해야 함
- 향후 방향: 분산 SQL과 tunable consistency DB는 업무별 consistency level을 세분화하나, latency-consistency 선택 자체는 계속 남음

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "PACELC를 설명하시오", "기술하시오" | P 조건과 E 조건의 선택 흐름 | CAP 대비 차이와 제품 사례 |
| 요구사항 명시형 | "CAP와 비교하시오", "DB 선택 기준을 제시하시오" | Dynamo/Cassandra/Spanner 비교 | L/C 선택, 지연·일관성 지표 |

> 요약: 설명형은 PACELC 구조, 비교형은 CAP 한계와 제품별 선택 기준을 중심으로 전환한다.
