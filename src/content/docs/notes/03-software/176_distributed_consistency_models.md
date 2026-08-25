---
sidebar:
  order: 176
  label: "176. 분산 시스템 일관성 모델"
  badge:
    text: "미출 · 70%"
    variant: note
title: "분산 시스템 일관성 모델 (Distributed System Consistency)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 176
extra:
  question_no: "176"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "관찰 순서와 복제 지연의 설계 가치"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Consistency Model(일관성 모델)**: 분산 복제본 환경에서 읽기/쓰기 연산의 순서와 시점이 클라이언트에게 어떻게 관찰될지를 정의한 계약.
- **Linearizability & Eventual Consistency**: 물리적 절대 시간에 따른 즉시 최신성 보장(Linearizability)과 시차 후 수렴 보장(Eventual).

</details>

- 정의/개념: 분산 복제본 환경에서 읽기와 쓰기 연산의 **관찰 순서와 최신성 보장 수준을 정의하는 분산 시스템 정합성 계약 규약**
- 배경/필요성: 분산 복제 지연 및 네트워크 단절(CAP) 환경에서 **완벽한 최신성, 고가용성, 초저지연을 동시에 100% 만족 불가**

#### 한줄 요약
- 비즈니스 도메인 요구에 맞춰 선형성부터 최종 일관성까지 최적의 일관성 모델을 선택한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Quorum Consistency ($W + R > N$)**: 전체 복제본($N$) 중 쓰기 승인 수($W$)와 읽기 조회 수($R$)의 합이 $N$을 초과하여 항상 최신 데이터를 읽도록 보장.
- **Read-Your-Writes**: 사용자가 자신이 직접 수정한 데이터만큼은 새로고침 시 즉시 최신값으로 관찰되도록 보장하는 세션 일관성.

</details>

- 일관성 강도가 높을수록 동기화 대기로 지연시간이 증가하는 **Latency vs Consistency**
- 강력한 합의일수록 단일 노드 장애 시 쓰기를 거부하는 **Availability vs Consistency**
- 정족수 공식($W + R > N$) 및 버전 벡터를 통한 **유연한 정합성 튜닝 가능성**

#### 한줄 요약
- 일관성 강도와 응답 지연 및 가용성 간의 트레이드오프를 통해 최적의 정합성 계층을 설계한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **정족수(Quorum) 기반 일관성 구조**: $N$(복제본 수), $W$(쓰기 정족수), $R$(읽기 정족수), Conflict Resolution(버전 충돌 해결).

</details>

```text
[분산 시스템 Quorum 기반 일관성 제어 구조]
|-- 1. Client Read / Write Operations
`-- 2. Quorum Coordination Layer (조정자 노드: Coordinator)
    |-- N: Total Replicas (전체 복제본 수 = 3)
    |-- W: Write Quorum (과반수 쓰기 승인 수 = 2)
    |-- R: Read Quorum (과반수 읽기 조회 수 = 2)
    `-- Quorum Equation: `W + R > N` (2 + 2 = 4 > 3 -> Strong Consistency 보장)
`-- 3. Distributed Replicas (Node 1, Node 2, Node 3)
    `-- Conflict Resolution Engine (Vector Clock, LWW: Last-Write-Wins 타임스탬프)
```

선의 의미: 계층 및 클라이언트의 요청을 조정자 노드가 정족수 공식에 따라 복제본 노드들에 전파하고 충돌을 해결하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **복제본 수 (N)** | 데이터의 고가용성과 내구성을 위해 유지하는 **전체 물리적 복제 노드 수 정의** | $N=3$ 또는 $N=5$ |
| **쓰기 정족수 (W)** | 쓰기 성공 판정을 위해 **반드시 응답해야 하는 최소 복제본 노드 수 정의** | 과반수 ($W > N/2$) |
| **읽기 정족수 (R)** | 최신 데이터를 보장하기 위해 **동시에 조회해야 하는 최소 복제본 노드 수 정의** | $R > N - W$ |
| **충돌 해결 규칙** | 동시 다발적 쓰기 충돌 시 **Vector Clock 또는 LWW(Last-Write-Wins)로 최신값 결정** | 버전 충돌 해소 |

#### 한줄 요약
- 복제본 수(N), 쓰기 정족수(W), 읽기 정족수(R), 충돌 해결 규칙이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **강한 일관성(Linearizability) 처리 5단계**: 쓰기 요청 수신 $\to$ 전역 순서 부여 $\to$ 과반수(W) 복제 커밋 $\to$ 성공 반환 $\to$ 후속 읽기에 최신값 반환.

</details>

```text
클라이언트의 데이터 갱신(X=5) 요청
        │
   1. [쓰기 요청 수신] 조정자(Coordinator)가 클라이언트로부터 쓰기 명령 접수
        │
   2. [전역 순서 결정] Raft/Paxos 합의를 통해 트랜잭션 전역 논리 시계(Epoch/Term) 부여
        │
   3. [과반수 복제 커밋] 복제 노드들에 패킷을 전송하고 과반수($W=2$) 승인을 받아 Commit 완료
        │
   4. [성공 반환] 클라이언트에게 쓰기 성공(200 OK)을 즉시 통지 (Linearization Point)
        │
   5. 이후 어떤 클라이언트가 읽기($R=2$)를 수행해도 절대 과거 값으로 회귀하지 않고 최신 X=5 반환
```

#### 한줄 요약
- 요청 수신 → 순서 결정 → 과반수 커밋 → 성공 반환 → 최신값 보장 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **5대 일관성 모델**: Linearizability(선형성), Sequential(순차), Causal(인과), Session(세션), Eventual(최종).

</details>

| 일관성 모델 | 보장 강도 | 핵심 보장 내용 및 특징 | 최적 적용 도메인 |
|:---|:---|:---|:---|
| **Linearizability (선형성)**| **Strong** | **실제 절대 시간 기준 즉각적인 최신 완료값 보장** | **금융 계좌 잔액, 한정판 재고** |
| **Sequential (순차)** | 상 (Strong)| 모든 노드가 동일한 연산 순서로 관찰 (시간 불일치 허용)| 멀티플레이 게임 이벤트 |
| **Causal (인과)** | 중상 (Medium)| 인과 관계(질문-답변)가 있는 연산 간의 순서만 보장 | 게시글 댓글 및 대댓글 시스템 |
| **Session (세션)** | 중 (Medium)| **내가 쓴 데이터는 내가 즉시 최신으로 관찰 (RYW)** | **SNS 프로필 및 장바구니** |
| **Eventual (최종)** | **Weak** | 추가 쓰기가 없으면 궁극적으로 모든 복제본 수렴 | **SNS 타임라인 피드, 통계 캐시**|

#### 한줄 요약
- 금융·재고는 선형성(Linearizability), 사용자 경험은 세션(RYW), 대규모 조회는 최종 일관성을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Split-Brain**: 네트워크 분할로 인해 두 진영의 노드가 서로 리더라고 주장하며 독립 쓰기를 받아 데이터가 파괴되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 네트워크 분할 시 Split-Brain 발생으로 데이터 파괴 | **과반수(Quorum) 투표 기반 Raft/Paxos 합의 알고리즘 적용** | 단일 진영 리더 선출 및 무결성 보장 |
| 최종 일관성 DB에서 결제 직후 잔액이 안 바뀐 것처럼 보임 | **Read-Your-Writes 세션 일관성 및 마스터 노드 강제 읽기 라우팅** | 사용자 경험 및 신뢰성 확보 |
| 동시 주문 요청으로 인한 재고 마이너스 오버부킹 | **DB Optimistic Lock (버전 컬럼 조건부 Update) 적용** | 초과 판매 사고 원천 차단 |
| 복제 지연으로 인한 오래된 데이터(Stale Read) 노출 | **핵심 비즈니스 조회 시 DynamoDB `ConsistentRead: true` 옵션 강제** | 100% 최신 데이터 보장 |

#### 한줄 요약
- Quorum 합의, Read-Your-Writes 보장, 낙관적 락, Consistent Read 강제로 운영한다.

## Ⅶ. 결론

- 분산 클라우드 데이터베이스 아키텍처 설계 시 **비즈니스 도메인의 중요도에 따라 계좌 잔액과 재고는 Quorum 기반 강한 일관성(Linearizability)을 강제하고, SNS 피드와 조회성 캐시는 최종 일관성(Eventual) 및 세션 일관성(RYW)을 선별 적용**하여 시스템 정합성과 가용성을 완성

#### 한줄 요약
- 분산 일관성 모델은 선형성부터 최종 일관성까지의 스펙트럼에서 비즈니스 정합성과 응답 지연 간의 최적 균형점을 정의하는 분산 시스템 설계의 핵심 이론이다.