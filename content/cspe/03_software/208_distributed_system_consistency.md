---
title: "분산 시스템 일관성 모델 (Distributed System Consistency)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 208
---

# 📖 【암기용】 개념 완전 이해

> 목적: 분산 시스템 일관성 모델을 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: **복제(Replication)**된 데이터를 여러 사용자가 읽을 때 어떤 최신성·순서로 보이는지를 규정하는, **CAP 정리**에 직결되는 정합성 규칙
- **왜 필요한가**: 분산 DB와 캐시는 장애 대비·지역 분산을 위해 데이터를 여러 노드에 복제한다. 네트워크 지연과 장애(partition)가 있는 환경에서 "복제본이 즉시 같은 값을 가져야 하는가, 잠시 달라도 되는가"를 정해야 한다.
- **핵심 직관**: 여러 지점 은행 장부가 언제 서로 맞아야 하는지를 정하는 약속이다 — 항상 실시간으로 맞추면 창구 응답이 느려지고, 나중에 맞춰도 되면 응답은 빠르지만 잠깐 다른 잔액을 볼 수 있다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 복제(Replication) | 동일 데이터를 여러 노드에 복사해 두는 것 — 일관성 모델이 다루는 대상 | 여러 지점에 같은 장부 사본을 두는 것 |
| CAP 정리 | 네트워크 분단(P) 발생 시 일관성(C)과 가용성(A) 중 하나만 보장 가능하다는 정리 | 본점-지점 통신이 끊기면 "정확한 잔액 확인"과 "즉시 응답" 중 하나만 고를 수 있음 |
| Strong Consistency(Linearizability) | 쓰기 완료 직후 어느 복제본에서 읽어도 항상 최신 값 | 방금 입금한 돈이 어느 창구에서 조회해도 바로 반영됨 |
| Eventual Consistency | 새 쓰기가 없으면 시간이 지나 결국 모든 복제본이 같은 값으로 수렴 | 소문이 전 지점에 퍼지는 데 시간이 걸리지만 결국 같은 내용으로 통일됨 |
| Causal Consistency | 원인-결과가 있는 작업 순서는 보장, 무관한 작업 순서는 자유 | 질문 다음에 답변이 보이는 건 보장하지만, 남남끼리의 대화 순서는 안 섞여도 무방 |
| Quorum (N, W, R) | 전체 복제본 수 N, 쓰기 확인 필요 수 W, 읽기 확인 필요 수 R | "3곳 창구 중 몇 곳 서명 받아야 유효한 거래인지"의 규칙 |
| Version Vector | 노드별 갱신 횟수를 벡터로 기록해 인과관계·동시성(충돌)을 판별하는 장치 | 각 부서 결재 도장 순서로 누가 먼저 처리했는지 추적 |
| Conflict Resolution(LWW 등) | 동시 쓰기 충돌 시 최종값을 정하는 규칙(Last-Write-Wins, merge 등) | 동시에 두 사람이 같은 칸을 고쳤을 때 최종본을 정하는 사규 |

## 깊이 이해

### CAP 정리부터: 왜 "선택"이 필요한가
- 2000년 Eric Brewer가 제시하고 2002년 증명된 CAP 정리는 "Consistency, Availability, Partition tolerance 세 가지를 동시에 100% 만족하는 분산 시스템은 없다"는 것이다. 네트워크 분단(P)은 케이블 단절·스위치 장애로 언젠가 발생하므로 상수로 두고, **분단이 실제로 터졌을 때 C와 A 중 무엇을 포기할지**가 진짜 질문이다.
- 예: 3개 노드(A, B, C) 중 A와 B 사이 네트워크가 끊겼다고 하자. 클라이언트가 A에 쓰기 요청을 보냈을 때, A가 B의 응답을 기다리다 실패하면(요청 거부) 가용성을 잃고, A가 즉시 자기 값만 반영해 응답하면 B는 잠시 구버전을 들고 있어 일관성을 잃는다.
- PACELC는 한 걸음 더 나아가 "분단이 없는 평상시(Else)에도 지연(Latency)과 일관성(Consistency) 사이에 트레이드오프가 있다"고 확장한다 — quorum 확인 왕복시간만큼 강한 일관성은 항상 지연이 더 든다.

### Quorum 공식으로 최신성 보장하기 — 숫자로 확인
- 공식: **R + W > N**이면 읽기 quorum과 쓰기 quorum이 최소 1개 이상의 복제본에서 겹친다. 이 겹치는 복제본이 항상 최신 값을 갖고 있어, 읽을 때 그중 가장 최근 버전을 고르면 최신성이 보장된다.
- **워크드 예제**: N=3(복제본 A, B, C), W=2, R=2로 설정. 쓰기 요청 시 A, B가 먼저 응답(ack)하면 W=2 충족으로 커밋 완료 — C는 아직 반영 전(replication lag). 이후 읽기 요청이 B, C 두 곳에 질의(R=2)하면 B는 최신값·C는 구버전을 반환하는데, 두 값의 버전을 비교해 B의 최신값을 채택한다. R+W=4 > N=3이므로 "쓰기에 참여한 노드"와 "읽기에 질의한 노드"가 항상 최소 1곳 겹치는 것이 수학적으로 보장된다.
- 만약 W=1(A만 ack)로 낮추면 쓰기는 빨라지지만, 읽기가 B, C만 질의할 경우 A를 거치지 않아 최신값을 놓칠 확률(stale read)이 생긴다 — 이것이 "지연을 줄이면 일관성 보장이 깨진다"는 PACELC의 실체다.

### 일관성 스펙트럼 — Strong에서 Eventual까지
- 강한 순서로 나열하면 **Strong(Linearizable) > Sequential > Causal > Read-your-writes/Session > Eventual**이다. 위로 갈수록 "항상 최신"에 가깝고 지연·비용이 크며, 아래로 갈수록 지연은 낮지만 일시적으로 다른 값을 볼 위험이 있다.
- **Causal 예시**: SNS에서 A가 게시물을 올리고 B가 그 게시물에 댓글을 달면, 제3자에게는 "게시물 먼저, 댓글 나중"이라는 인과 순서가 항상 지켜져야 한다(댓글만 보이고 원글이 안 보이면 안 됨). 반면 서로 무관한 두 사용자의 게시물 순서는 뒤바뀌어 보여도 업무상 문제없다 — 이것이 causal consistency다.
- **Eventual 예시**: 상품 조회수 카운터는 지금 이 순간 정확한 숫자가 아니라 TTL 30초 캐시로 잠시 오래된 수치를 보여줘도 괜찮다. 반대로 결제·재고 차감처럼 "지금 정확히 1개 남았다"를 확정해야 하는 업무를 eventual로 처리하면 이중 판매(overselling) 사고가 난다.

### 충돌은 어떻게 푸는가 — LWW와 Version Vector
- 여러 노드에 동시에 쓰기가 들어오면 "누가 이겼는지" 정해야 한다. 가장 단순한 규칙은 **LWW(Last-Write-Wins)** — 타임스탬프가 더 늦은 쓰기가 이긴다. 구현이 쉽지만 시계 오차(clock skew)가 있으면 실제로 나중에 쓴 값이 지워질 수 있다.
- **Version Vector 예제**: 노드 A, B가 각각 [A:1, B:0], [A:0, B:1] 버전으로 동시에 같은 키를 수정했다면, 두 벡터 중 어느 쪽도 다른 쪽을 포함(dominate)하지 않는다 — 즉 "동시 쓰기(concurrent)"로 판정하고, 애플리케이션이 두 값을 모두 보여주거나 merge 규칙(예: 장바구니는 합집합)으로 병합한다. 반대로 [A:2, B:1]이 [A:1, B:1]을 포함하면 전자가 후자의 인과적 후속 버전이므로 자동으로 승자를 정할 수 있다.

### 흔한 오해
- CAP는 "세 가지 중 두 가지만 고정으로 고르는 제품 분류표"가 아니다. 분단이 없는 평상시엔 셋 다 정상 동작하며, **분단이 실제로 발생한 그 순간에만** C와 A 중 하나를 포기하는 선택이 발동된다.
- Strong consistency라고 해서 항상 느린 것은 아니다 — 단일 리전·저지연 네트워크에서는 quorum 왕복 비용이 수 ms 수준이라 체감 차이가 작을 수 있다. 문제는 지역 간(리전 간) 복제처럼 왕복이 수십~수백 ms일 때 커진다.

## 연결 개념
- CAP 정리 — 이 개념이 속한 상위 이론(partition 발생 시 C/A 선택)
- Quorum — R, W, N 조합으로 일관성 수준을 조정하는 구체 메커니즘
- Distributed Consensus(Raft·Paxos) — strong consistency를 실제로 구현하는 합의 알고리즘 (209에서 상세)

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 수치·표준명·비교축으로 작성한다.
> 핵심: 일관성 모델은 DB 제품명이 아니라 업무 위험, 지연 허용치, 장애 시 가용성 목표를 맞추는 설계 선택이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 분산 시스템 일관성 모델은 복제 데이터의 읽기 최신성, 순서, 수렴 시점을 정의하는 규칙이다.
> 2. **가치**: 업무별로 strong, causal, read-your-writes, eventual consistency를 선택해 정확성과 가용성의 균형을 맞춘다.
> 3. **판단 포인트**: CAP, PACELC, quorum, conflict resolution, SLA 지연을 함께 고려해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 분산 데이터 설계 이해 확인 | strong, eventual, causal, read-your-writes | 일관성을 ACID 하나로만 설명 |
| CAP·PACELC 판단 확인 | partition 시 C/A, 정상 시 latency/consistency | CAP를 제품 분류표로 단순 암기 |
| 업무 적용 역량 확인 | 재고·결제·조회·알림별 모델 선택 | 모든 업무에 strong consistency 적용 |

> 요약: 이 문제는 일관성 명칭보다 업무별 정확성·지연·가용성 선택 기준을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 복제 데이터 관찰 규칙
- 배경: 분산 시스템은 복제와 지역 분산으로 가용성을 확보하지만 노드 간 지연과 partition을 피할 수 없다.
- 필요성: quorum, version vector, conflict resolver 기준으로 업무 손실과 사용자 경험에 맞는 데이터 최신성 수준을 정한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> Replica A/B/C -> Replication Protocol -> Read/Write Rule
                       +-> Quorum / Version Vector / Conflict Resolver
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Replica | 데이터 복제본 저장 | leader, follower, multi-leader |
| Consistency Rule | 읽기·쓰기 관찰 규칙 정의 | linearizable, eventual 등 |
| Quorum | R+W>N 조건으로 최신성 조정 | N=3, W=2, R=2 예시 |
| Conflict Resolver | 동시 쓰기 충돌 해결 | LWW, vector clock, merge |

> 요약: 일관성 모델은 복제 구조, 읽기·쓰기 규칙, quorum, 충돌 해결 방식의 조합으로 구현된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
쓰기 요청 -> 복제본 기록 -> quorum 확인 -> 읽기 요청 -> 버전 비교 -> 최신값/수렴값 반환
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 쓰기를 leader 또는 quorum replica에 반영 | W ack 수 충족 |
| 2 | replication log 전파 | replication lag 측정 |
| 3 | 읽기 시 R개 replica 응답 수집 | stale read 비율 확인 |
| 4 | 버전 충돌 해결 후 응답 | conflict resolution error 0건 |

> 요약: 일관성은 쓰기 승인 조건, 복제 지연, 읽기 quorum, 충돌 해결 순서로 결정된다.

---

## Ⅳ. 특징

| 구분 | Strong/Linearizable | Causal/Session | Eventual |
|:---|:---|:---|:---|
| 보장 | 쓰기 후 모든 읽기 최신값 | 원인 관계·세션 내 순서 | 시간 경과 후 수렴 |
| 지연 | quorum·consensus로 증가 | 세션 stickiness 필요 | 지역 읽기 가능 |
| 적용 | 결제, 재고, 계좌 | 사용자 설정, 장바구니 | 조회수, 피드, 캐시 |
| 지표 | stale read 0건 | 세션 순서 위반 0건 | convergence 30초 이하 |

> 요약: 업무 손실이 크면 strong, 사용자 단위 순서가 핵심이면 causal, 조회·분석은 eventual을 선택한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단일 DB | 복제 DB·분산 캐시 | 지역 장애 대비와 읽기 확장 필요 |
| 비용/성능 | 단일 지연 | consistency 수준별 지연 | 결제 p95 200ms, 조회 p95 100ms 분리 |
| 운영/위험 | 단일 장애점 | stale read·conflict | 업무별 stale 허용치 문서화 |

> 요약: 일관성 모델은 시스템 전체가 아니라 업무 트랜잭션 단위로 다르게 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| stale read | replication lag | read quorum, session stickiness | stale read ratio 0.1% 이하 |
| write conflict | multi-leader 동시 갱신 | vector clock, merge rule | conflict count |
| 가용성 저하 | strong consistency quorum 실패 | fallback read, degrade mode | quorum failure rate |

> 요약: 리스크는 오래된 읽기, 쓰기 충돌, quorum 실패이며 업무별 허용치와 대체 흐름이 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 최신성 | replication lag 1초 이하 또는 업무 SLA | DB metric |
| 정확성 | conflict resolution error 0건 | audit reconciliation |
| 가용성 | partition 시 RTO 5분 이하 | chaos test |

> 요약: 일관성 설계는 복제 지연, 충돌 오류, 장애 복구 목표로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. 결제·재고 차감은 leader 기반 strong consistency 또는 RDB 트랜잭션으로 처리하고 조회 캐시는 eventual consistency와 TTL 30초를 적용함.
2. NoSQL 복제는 N=3, W=2, R=2 quorum을 기준으로 업무별 stale read 허용치를 문서화함.
3. multi-region 구성은 PACELC 기준으로 partition 시 결제는 C, 피드 조회는 A를 선택하고 chaos test로 검증함.

**결론 (2줄):**
- 기술사 판단: 금전·재고는 strong, 사용자 경험·분석은 eventual, 세션 연속성은 read-your-writes를 선택함.
- 향후 방향: global database와 CRDT는 지역 분산 환경에서 지연과 충돌 해결을 업무 규칙으로 흡수하는 방향으로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "분산 일관성 모델을 설명하시오" | quorum, replication, conflict 흐름 | strong·causal·eventual 비교 |
| 요구사항 명시형 | "CAP 관점에서 설계하시오", "적용 방안을 제시하시오" | 업무별 R/W, 장애 시 선택 | 리스크 대응, SLA·지표 기준 |

> 요약: 설명형은 모델 종류, 설계형은 업무별 일관성 선택과 장애 시 정책으로 목차를 전환한다.
