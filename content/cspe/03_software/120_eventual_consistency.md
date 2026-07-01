---
title: "최종 일관성 (Eventual Consistency)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 120
---

# 📖 【암기용】 개념 완전 이해

> 목적: 최종 일관성을 처음 보는 사람도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 분산 복제본이 즉시 같지는 않아도 시간이 지나면 같은 상태로 수렴하는 일관성 모델
- **왜 필요한가**: 글로벌 서비스는 모든 요청마다 모든 노드 합의를 기다리면 지연이 커진다. 최종 일관성은 비동기 복제와 충돌 해결을 통해 응답을 지속하면서 이후 데이터를 맞춘다.
- **핵심 직관**: 여러 사람이 같은 문서를 각자 수정하면 잠시 다른 버전이 존재하지만, 동기화가 끝나면 하나의 결과로 모이는 방식이다.

## 깊이 이해
- **배경·문제의식**: 분산 DB와 캐시는 지역 지연, 네트워크 분할, replica lag 때문에 모든 읽기에 최신값을 제공하기 어렵다. 피드, 카운터, 추천, 캐시처럼 일시 차이를 허용하는 업무에서 최종 일관성을 사용한다.
- **작동 원리**: 쓰기는 한 노드에서 먼저 성공하고 변경 이벤트가 다른 노드로 비동기 전파된다. read repair, anti-entropy, vector clock, last-write-wins 등으로 불일치를 감지하고 해결한다.
- **비유**: 가족 캘린더 앱에서 한 사람이 일정을 추가하면 다른 사람 휴대폰에는 몇 초 뒤 반영된다. 잠시 차이는 있지만 동기화 후 같은 일정표가 된다.
- **구체 예시**: Cassandra에서 write consistency `ONE`, read consistency `ONE`이면 낮은 지연을 얻지만 stale read가 가능하다. `QUORUM`을 쓰면 최신값 관측 가능성이 커지는 대신 지연이 증가한다.
- **흔한 오해·주의점**: 최종 일관성은 아무 때나 맞아도 된다는 의미가 아니다. 수렴 시간, read-your-writes, monotonic read, 충돌 해결 기준을 SLA로 관리해야 한다.

## 연결 개념
- BASE — 최종 일관성을 포함하는 완화된 분산 모델
- Read-your-writes — 자신이 쓴 값은 이후 읽기에서 보여야 하는 보장
- Monotonic read — 시간이 되돌아간 값이 보이지 않는 보장
- Conflict resolution — 동시 쓰기 충돌을 결정하는 규칙

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 최종 일관성 답안은 비동기 복제만 쓰지 말고, 수렴 시간과 세션 보장, 충돌 해결을 운영 지표로 제시해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 최종 일관성은 비동기 복제 환경에서 복제본이 즉시 같지 않아도 일정 시간 후 같은 상태로 수렴하는 모델이다.
> 2. **가치**: 글로벌 지연과 장애 상황에서 응답 지속을 확보하면서 피드·알림·캐시·카운터 업무의 확장성을 높인다.
> 3. **판단 포인트**: convergence time, stale read 허용, read-your-writes, monotonic read, conflict resolution을 SLA로 명시해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 분산 일관성 모델 이해 확인 | async replication, convergence, stale read | 단순 복제 지연으로만 설명 |
| 사용자 관점 보장 확인 | read-your-writes, monotonic read, causal ordering | 세션 보장과 충돌 해결 누락 |
| 운영 통제 역량 확인 | read repair, anti-entropy, version vector, LWW | 수렴 시간 지표 없이 추상 설명 |

> 요약: 이 문제는 일시 불일치를 허용하되 언제, 어떻게, 어떤 기준으로 수렴시키는지를 묻는다.

---

## Ⅰ. 개요 및 필요성

최종 일관성은 분산 복제본이 시간이 지나면 같은 상태로 수렴하는 모델이다. 글로벌 서비스와 대규모 NoSQL은 즉시 일관성보다 응답 지속과 낮은 지연을 선택하는 경우가 있다. 단, 수렴 시간과 사용자 세션 보장을 명확히 해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client Write -> Local Replica Commit
  / Async Replication -> Remote Replica
  / Read Repair -> stale value 보정
  / Anti-Entropy -> 백그라운드 동기화
Conflict Resolver -> Converged State -> Metrics
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Local replica | 근접 노드에서 읽기·쓰기 처리 | 낮은 지연, stale 가능 |
| Async replication | 변경 이벤트 비동기 전파 | lag와 순서 역전 가능 |
| Version metadata | 변경 순서·충돌 판단 | vector clock, timestamp |
| Conflict resolver | 동시 쓰기 병합·선택 | LWW, merge function, CRDT |
| Session guarantee | 사용자 체감 일관성 보완 | read-your-writes, monotonic read |

> 요약: 최종 일관성 구조는 비동기 복제, 버전 메타데이터, 충돌 해결, 세션 보장, 수렴 지표로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Write 요청 -> local commit -> client 응답
  / 변경 이벤트 전파 -> replica apply
  / 동시 쓰기 발견 -> conflict resolver
Read 요청 -> session rule 확인 -> 값 반환
Anti-entropy -> 수렴 확인 -> metrics 기록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 쓰기를 local replica에 반영하고 응답 | local commit latency |
| 2 | 변경 이벤트를 다른 replica로 비동기 전파 | replication lag |
| 3 | 읽기 시 session guarantee 적용 | read-your-writes 성공률 |
| 4 | 동시 쓰기는 버전 기반으로 해결 | conflict resolution rate |
| 5 | 백그라운드 동기화로 수렴 확인 | convergence time |

> 요약: 최종 일관성은 local commit 후 비동기 전파하고, 충돌 해결과 anti-entropy로 허용 시간 내 수렴시킨다.

---

## Ⅳ. 특징

| 구분 | 즉시 일관성 | 최종 일관성 | 수치·판단 기준 |
|:---|:---|:---|:---|
| 읽기 결과 | 최신 commit 보장 | stale read 가능 | stale 허용 1~60초 |
| 지연 | quorum·합의 지연 포함 | local replica 응답 | p95 latency 목표 |
| 장애 | partition 시 요청 거부 가능 | local 응답 지속 | error rate vs stale rate |
| 충돌 | 동시성 제어로 사전 차단 | 사후 해결 | conflict rate 0.1% 이하 |
| 적용 업무 | 원장, 권한, 재고 | 피드, 추천, 알림, 캐시 | 불일치 피해 범위 |

> 요약: 최종 일관성은 낮은 지연과 응답 지속을 얻는 대신 stale read와 충돌 해결 책임을 운영 설계에 포함한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 원장 | 최종 일관성 | 즉시 일관성 | 이중 지불 허용 불가 |
| 피드 | 즉시 일관성 | 최종 일관성 | stale 5~30초 허용 |
| 캐시 | 원본 DB read | 최종 일관성 캐시 | TTL·무효화 정책 존재 |
| 세션 보장 | 없음 | read-your-writes | 사용자 작성 후 조회 필요 |

> 요약: 최종 일관성은 불일치 허용 시간이 명확하고 보상·수렴 절차가 있는 업무에 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 사용자 혼란 | 자신이 쓴 값이 안 보임 | session affinity, read-your-writes | RYW 실패율 |
| 시간 역행 | 이전 버전 읽기 | monotonic read token | monotonic 위반 건수 |
| 충돌 손실 | LWW로 업데이트 유실 | vector clock, merge rule, CRDT | lost update count |
| 수렴 지연 | replication backlog | backpressure, anti-entropy job | convergence p95 |

> 요약: 최종 일관성 리스크는 세션 보장 위반과 충돌 손실이며, RYW·monotonic·수렴 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 수렴 시간 | p95 5초, p99 60초 등 | replica version diff |
| Stale read | SLA 내 0.1% 이하 | synthetic read test |
| RYW | 성공률 99.9% 이상 | session test |
| 충돌 | conflict rate 0.1% 이하 | resolver log |

> 요약: 최종 일관성 품질은 수렴 시간, stale read, 세션 보장, 충돌률, 재처리 backlog로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. SLA 명시: 업무별 stale 허용 시간을 0초, 5초, 60초로 등급화하고 원장·권한은 최종 일관성 대상에서 제외함
2. 세션 보장: read-your-writes는 primary read 또는 session token으로, monotonic read는 version watermark로 보장함
3. 충돌 해결: vector clock, CRDT, merge function, idempotency key를 적용하고 conflict log를 감사 대상으로 남김

**결론 (2줄):**
- 기술사 판단: 사용자 경험 데이터는 최종 일관성으로 지연과 가용성을 조정하고, 금전·권한 데이터는 즉시 일관성 모델을 선택함
- 향후 방향: CRDT, CDC, stream processing 기반 수렴 검증이 결합되며 최종 일관성은 운영 지표 중심의 모델로 발전함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "최종 일관성을 설명하시오", "기술하시오" | 비동기 복제와 수렴 흐름 | 즉시 일관성과 지연·충돌 비교 |
| 요구사항 명시형 | "보장 방안을 제시하시오", "비교하시오" | read-your-writes, monotonic read, conflict resolution | stale read·수렴 시간·충돌 대응 |

> 요약: 설명형은 비동기 수렴 원리, 방안형은 세션 보장과 충돌 해결 지표 중심으로 답안을 전환한다.
