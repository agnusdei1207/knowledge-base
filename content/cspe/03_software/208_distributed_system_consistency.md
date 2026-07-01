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
- **개요**: 여러 노드에 복제된 데이터가 사용자에게 어떤 순서와 최신성으로 보이는지 정한 규칙
- **왜 필요한가**: 분산 DB와 캐시는 장애 대비와 지역 분산을 위해 데이터를 복제한다. 이때 모든 사용자가 항상 같은 값을 보는지, 잠시 다른 값을 봐도 되는지를 결정해야 한다.
- **핵심 직관**: 여러 지점 은행 장부가 언제 서로 맞아야 하는지를 정하는 약속이다.

## 깊이 이해
- **배경·문제의식**: 네트워크 지연과 장애가 있는 환경에서 모든 노드가 즉시 같은 값을 갖게 만들면 지연이 증가하거나 가용성이 낮아진다.
- **작동 원리**: Strong consistency는 쓰기 완료 후 모든 읽기가 최신 값을 보장한다. Eventual consistency는 시간이 지나면 수렴한다. Causal consistency는 원인 관계가 있는 작업 순서를 보장한다.
- **비유**: 단체 채팅에서 송금 내역은 모두가 즉시 같은 값을 봐야 하지만, 좋아요 수는 몇 초 늦게 반영되어도 업무 문제가 작다.
- **구체 예시**: 재고 1개 상품 결제는 strong 또는 linearizable 처리, 상품 조회 캐시는 eventual consistency와 TTL 30초 적용 가능.
- **흔한 오해·주의점**: CAP는 세 가지를 모두 가질 수 없다는 단순 구호가 아니다. 네트워크 partition 상황에서 consistency와 availability 중 무엇을 희생할지 선택하는 문제이다.

## 연결 개념
- CAP Theorem — partition 발생 시 C/A 선택 문제
- Quorum — R, W, N 조합으로 일관성 조정
- Distributed Consensus — strong consistency 구현 기반

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

분산 일관성 모델은 복제 데이터의 관찰 규칙이다. 분산 시스템은 복제와 지역 분산으로 가용성을 확보하지만 노드 간 지연과 partition을 피할 수 없다. 일관성 모델은 업무 손실과 사용자 경험을 기준으로 데이터 최신성 수준을 정한다.

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

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
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
