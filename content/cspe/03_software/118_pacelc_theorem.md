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
- **개요**: PACELC는 **CAP 정리**를 확장한 분산 시스템 **트레이드오프 모델**로, 네트워크 분할(P)이 발생하면 가용성(A)과 일관성(C) 중 하나를, 분할이 없는 평상시(Else)에도 지연(L)과 일관성(C) 중 하나를 선택해야 한다는 원칙이다.
- **왜 필요한가**: CAP는 "분할이 생겼을 때"만 설명한다. 그런데 실제 글로벌 서비스는 대부분 분할 없는 정상 상태로 운영되며, 이때도 리전 간 합의를 기다리면 지연이 생긴다. PACELC는 이 "평상시" 트레이드오프까지 명시적으로 다룬다.
- **핵심 직관**: 통신 두절 같은 비상시엔 "본사 확인 없이 처리(가용성)"할지 "정확성 확인 후 처리(일관성)"할지 고르고, 통신이 멀쩡한 평상시에도 "즉시 지점 판단(저지연)"할지 "매번 본사 확인(일관성)"할지 여전히 골라야 한다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| CAP 정리 | PACELC가 확장하는 상위 개념 — 분할 시 일관성/가용성 트레이드오프만 설명 | PACELC의 앞부분(P)을 그대로 계승 |
| P (Partition) | 네트워크 분할이 발생한 상태 | 본사-지점 통신 두절 |
| A (Availability) | 분할 시에도 요청을 계속 처리(가용성 우선) | 지점이 본사 확인 없이 독자 승인 |
| C (Consistency) | 분할 시 정합성을 우선해 확인 안 되면 응답을 미루거나 거부 | 본사 확인이 될 때까지 대기 |
| E (Else) | 분할이 없는 정상 상태 — PACELC가 CAP에 새로 추가한 조건 | 통신이 멀쩡한 평상시 |
| L (Latency) | 정상 상태에서 원격 확인 없이 로컬 응답으로 지연을 낮추는 선택 | 지점에서 바로 처리 |
| PA/EL | 분할 시 가용성, 평상시 저지연을 우선하는 성향 | Dynamo, Cassandra |
| PC/EC | 분할 시에도, 평상시에도 일관성을 우선하는 성향(항상 합의 대기) | Spanner |
| Quorum | 전체 노드가 아니라 과반수의 응답만 확인하고 성공으로 인정하는 합의 방식 — L/C 선택을 조절하는 손잡이 | 전 지점이 아니라 과반수 지점 동의로 결정 |
| TrueTime | Spanner가 쓰는, 오차범위를 함께 제공하는 전역 시계(GPS+원자시계 기반) | 전 세계 지점 시계를 초 단위로 동기화 |

## 깊이 이해

### 공식으로 읽기: if P then A or C, else L or C
- 이 한 줄이 PACELC의 전부다. 분할(P)이 발생하면 CAP처럼 A 아니면 C를 고른다. 분할이 없어도(Else) 완전히 자유롭지는 않다 — 복제본이 여러 리전에 흩어져 있는 한, 쓰기를 모든(또는 과반수) 복제본에 확인받고 응답할지(C, 일관성), 로컬 복제본에만 쓰고 바로 응답할지(L, 저지연) 여전히 골라야 하기 때문이다.

### 수치로 보는 정상 상태 지연 문제
- 리전 간 왕복 지연(RTT)은 물리 거리 때문에 예를 들어 서울-버지니아 약 180ms, 서울-도쿄 약 30~40ms 수준이다. 매 쓰기마다 원격 리전 quorum 확인을 기다리면(PC/EC 방향) 이 RTT가 그대로 사용자 응답 시간에 더해진다. 반대로 로컬 리전에만 쓰고 비동기로 복제하면(PA/EL 방향) 응답은 로컬 디스크 커밋 시간(수 ms) 선에서 끝난다 — 장애가 전혀 없는 같은 시스템인데도 선택에 따라 응답 시간이 수십 배 차이 난다.

### 제품 사례로 확인하는 PA/EL vs PC/EC
- Dynamo, Cassandra: 분할 시 가용성 우선(PA), 평상시엔 로컬 replica에 먼저 쓰고 응답(EL) — tunable consistency로 ONE/QUORUM/ALL을 상황에 맞게 조정할 수 있다.
- Spanner: 분할 시 일관성 우선(PC), 평상시에도 TrueTime과 quorum commit으로 외부 일관성(external consistency)을 보장(EC) — 대신 커밋마다 지연이 발생한다.

### 흔한 오해
- PACELC를 CAP의 "대체"로 오해하기 쉽지만, PACELC는 CAP 뒤에 else 절을 덧붙인 확장이다. CAP만 보면 "분할이 없을 때는 트레이드오프가 없다"고 착각하기 쉽다. 실제로는 리전이 나뉘어 있는 한 정상 상태에도 latency-consistency 선택이 항상 존재한다.

## 연결 개념
- CAP 정리 — partition 시 C/A 선택의 기반이자 PACELC가 확장하는 상위 모델
- Dynamo/Cassandra — 가용성과 지연을 중시하는 PA/EL 대표 사례
- Spanner — 글로벌 일관성과 외부 일관성을 구현한 PC/EC 대표 사례
- Quorum·TrueTime — 일관성 수준과 지연을 실제로 조절하는 수단

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

- 개요: PACELC는 분산 DB 선택 원칙이다.
- 배경: CAP는 partition 시 C/A 선택을 설명하지만 정상 상태의 cross-region 합의도 latency와 consistency 비용을 만든다.
- 필요성: PA/EL, PC/EC 성향과 consistency level, quorum, cross-region latency 기준으로 글로벌 DB를 선택해야 한다.

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
