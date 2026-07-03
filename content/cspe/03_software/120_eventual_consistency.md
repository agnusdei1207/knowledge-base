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
- **개요**: 최종 일관성은 **분산 시스템의 일관성 모델** 중 하나로, 복제본 간 쓰기가 비동기로 전파되어 일시적으로 서로 다른 값을 보일 수 있지만 새 쓰기가 없으면 결국(eventually) 모든 복제본이 동일한 상태로 수렴한다는 보장이다.
- **왜 필요한가**: 글로벌 서비스가 모든 요청마다 모든 노드의 합의를 기다리면 지연이 커진다. 최종 일관성은 비동기 복제와 충돌 해결을 통해 응답을 지속하면서 이후에 데이터를 맞춘다.
- **핵심 직관**: 여러 사람이 같은 문서를 각자 수정하면 잠시 다른 버전이 존재하지만, 동기화가 끝나면 하나의 결과로 모이는 방식이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 일관성 모델 (Consistency Model) | 최종 일관성이 속하는 상위 범주 — 분산 복제본 간 값이 언제 같아지는지를 규정하는 규칙 | 여러 규칙 중 가장 느슨한 축 |
| 즉시 일관성 (Strong Consistency) | 모든 읽기가 항상 가장 최근 쓰기를 반영 — 최종 일관성과 대비되는 개념 | 최신판만 항상 보여줌 |
| 비동기 복제 (Async Replication) | 쓰기를 로컬에 먼저 반영한 뒤 다른 노드로 지연 전파 | 소식을 나중에 전달 |
| Replica Lag | 원본과 복제본 사이의 반영 시간 차 | 방송 중계 지연 |
| Read Repair | 읽기 시점에 오래된 값을 발견하면 즉시 최신값으로 보정 | 지나가다 잘못된 안내판을 고침 |
| Anti-Entropy | 백그라운드에서 주기적으로 복제본을 비교·동기화하는 프로세스 | 정기 재고 실사 |
| Vector Clock | 어떤 갱신이 먼저인지 인과관계를 추적하는 버전 메타데이터 | 각 지점이 찍은 도장 순번표 |
| LWW (Last-Write-Wins) | 타임스탬프가 가장 늦은 쓰기를 승자로 채택하는 충돌 해결 규칙 | 최종 수정시각이 늦은 문서를 채택 |
| Read-Your-Writes | 자신이 쓴 값은 이후 자신의 읽기에서 반드시 보이는 세션 보장 | 내가 쓴 댓글은 새로고침해도 그대로 보임 |
| Monotonic Read | 한 번 본 최신값보다 오래된 값이 다시 보이지 않는 보장 | 시간이 거꾸로 가지 않음 |

## 깊이 이해

### 작동 원리: 왜 "일단 로컬에 쓰고 나중에 맞추나"
- 여러 리전에 복제본을 둔 분산 DB가 모든 쓰기마다 전 리전 합의를 기다리면 지연이 크다. 그래서 쓰기는 한 노드(보통 요청과 가까운 노드)에 먼저 성공시키고, 변경 이벤트를 비동기로 다른 노드에 전파한다. 전파가 끝나기 전까지는 노드마다 다른 값을 보여줄 수 있다 — 이 구간이 바로 "일시 불일치" 구간이다.

### 수치로 보는 수렴 시간과 stale read
- Cassandra에서 write consistency `ONE`, read consistency `ONE`으로 설정하면 쓰기는 노드 1개 확인만으로 응답하므로 지연은 수 ms이지만, 다른 노드에서 곧바로 읽으면 replication lag(정상 시 수십~수백 ms, 장애 시 초 단위까지) 동안 이전 값(stale read)을 볼 수 있다. `QUORUM`(과반수 확인)으로 올리면 최신값을 볼 가능성이 커지지만 매 요청마다 여러 노드 응답을 기다려야 해 지연이 늘어난다 — latency와 consistency를 맞바꾸는 지점이 수치로 드러난다.

### 충돌 해결과 순서 보장 메커니즘
- 여러 노드가 동시에 같은 키를 갱신하면 어느 값이 "이긴다"고 정할 기준이 필요하다. Vector Clock은 각 노드의 갱신 횟수를 벡터로 기록해 인과관계(A가 B보다 먼저인지, 동시인지)를 판별한다. 판별이 안 되는 진짜 동시 갱신은 LWW(타임스탬프 비교)나 애플리케이션 병합 규칙으로 정리한다.
- 사용자 체감을 지키는 장치가 Read-Your-Writes와 Monotonic Read다. 세션을 같은 노드(또는 최신 버전을 가진 노드)로 고정해, 내가 방금 쓴 값이 사라지거나 시간이 거꾸로 가는 것처럼 보이는 상황을 막는다.

### 판별원리: 언제 최종 일관성을 쓰나
- 업무별로 불일치 허용 시간(stale 허용 초)을 정할 수 있는지가 기준이다. 원장·재고처럼 0초 허용이면 즉시 일관성을, 피드·알림·캐시처럼 5~60초 오차가 허용되면 최종 일관성을 택하고 그 시간을 SLA로 명시한다.

### 비유와 흔한 오해
- **비유**: 가족 캘린더 앱에서 한 사람이 일정을 추가하면 다른 사람 휴대폰에는 몇 초 뒤 반영된다. 잠시 차이는 있지만 동기화 후에는 같은 일정표가 된다.
- **오해**: "최종 일관성 = 아무 때나 맞으면 됨"이 아니다. 수렴 시간에 상한이 없으면 SLA 위반이고, Read-Your-Writes 같은 세션 보장이 없으면 사용자가 자신이 쓴 데이터가 사라진 것처럼 느껴 신뢰를 잃는다.

## 연결 개념
- BASE — 최종 일관성을 포함하는 완화된 분산 트랜잭션 모델
- CRDT — 최종 일관성을 수학적으로 보장하는 자료구조(충돌 해결을 구조 차원에서 해결)
- Read-your-writes·Monotonic read — 사용자 체감을 지키는 세션 보장
- Conflict resolution — 동시 쓰기 충돌을 결정하는 규칙(Vector Clock, LWW)

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

- 개요: 최종 일관성은 복제본 사후 수렴 모델이다.
- 배경: 글로벌 서비스와 대규모 NoSQL은 모든 요청마다 원격 합의를 기다리면 지역 지연과 장애 전파 비용이 커진다.
- 필요성: convergence time, read-your-writes, monotonic read, vector clock, LWW 기준으로 불일치 허용 범위를 관리해야 한다.

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
