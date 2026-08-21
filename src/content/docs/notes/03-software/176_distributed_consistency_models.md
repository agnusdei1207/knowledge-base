---
sidebar:
  order: 176
  label: "176. 분산 시스템 일관성 모델 (Distributed System Consistency)"
  badge:
    text: "미출 · 70%"
    variant: note
title: "분산 시스템 일관성 모델 (Distributed System Consistency)"
date: "2026-08-14T03:36:00+09:00"
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

- **Consistency Model (일관성 모델)**: 분산된 여러 대의 데이터베이스(복제본)에서 데이터 읽기(Read)와 쓰기(Write)의 순서와 시점이 클라이언트에게 어떻게 관찰될지 보장하는 수학적 계약.
- **Strict Consistency (엄격한 일관성)**: 데이터가 쓰이는 즉시, 물리적 거리에 상관없이 우주 모든 곳의 클라이언트가 정확히 똑같은 최신 값을 읽을 수 있는 가장 강력한(현실 불가능한) 이론적 일관성.
- **Eventual Consistency (최종 일관성)**: 쓰기 직후 당분간은 오래된 데이터를 읽을 수 있지만(Stale Read), 추가적인 쓰기가 없다면 궁극적으로는(Eventual) 모든 복제본이 같은 값에 도달하는 느슨한 일관성.

</details>

- 정의/개념: 분산 Read•Write의 관찰 순서를 정하는 **Consistency Model**
- 배경/필요성: 복제 지연•Partition에서 **최신성•가용성•지연** 동시 극대화 곤란

#### 한줄 요약

- 여러 지점의 같은 장부를 읽을 때 어떤 순서와 얼마나 최신인 값을 반드시 보여 줄지 약속하는 모델이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Read-Your-Writes (자기 쓰기 읽기)**: 최종 일관성을 허용하더라도, "내가 작성한 게시글"만큼은 내가 새로고침 했을 때 즉시 보이도록 보장(Session Consistency)하여 사용자 경험을 방어하는 기법.

</details>

- **Latency vs Consistency (일관성이 강할수록 합의 시간이 길어져 지연 속도 증가)**
- **Availability vs Consistency (일관성이 강할수록 노드 하나만 죽어도 전체 쓰기 거부 발생)**
- **Stale Read Acceptance (최종 일관성 채택 시 오래된 데이터를 읽는 비즈니스 리스크 감수)**

#### 한줄 요약

- 모든 복사본의 최신값을 확인할수록 응답은 늦고 분할 때 거부될 수 있으므로 재고와 피드에 같은 강도를 적용하지 않는다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Quorum (정족수)**: 5대의 복제 서버 중 3대 이상(과반수)에 쓰기가 성공해야 최종 쓰기 완료로 인정(W)하고, 읽을 때도 3대 이상(R)에서 읽어 가장 최신 버전을 채택하는 일관성 합의 공식(W + R > N).

</details>

```text
[Quorum Policy]
 ├── [N]
 ├── [W]
 ├── [R]
 └── [Version•Conflict Rule]
```

| 구성요소 | 책임 |
|---|---|
| N | Data를 보유하는 **Replica 수** 정의 |
| W | Write 성공에 필요한 **승인 Replica 수** 정의 |
| R | Read가 확인할 **Replica 수** 정의 |
| Version•Conflict Rule | 최신값 판정과 **동시 Write 충돌** 해결 |

#### 한줄 요약

- 조정기가 필요한 복사본의 승인을 모아 완료를 알리고 버전 정보가 동시 변경을 구분해 충돌 처리 기준을 제공한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Linearizability (선형성)**: 쓰기 연산(W)이 끝난 직후부터 발생하는 모든 읽기(R)는 반드시 방금 쓴 값이나 그보다 최신 값을 반환해야 하며, 절대 과거로 회귀할 수 없음을 의미하는 단일 시점 모델.

</details>

```text
[Write X=5 요청]
       │
       ▼
1. Write 순서 결정
       │
       ▼
2. Commit Point 통과
       │
       ▼
3. Write 성공 반환
       │
       ▼
4. 후속 Read에 최신값 반환
       │
       ▼
[X=5 관찰]
```

### 동작 원리

1. Write 순서 결정: 동시 Operation의 단일 관찰 순서 확정
2. Commit Point 통과: Write의 선형화 시점 형성
3. Write 성공 반환: 완료를 Client에 통지
4. 후속 Read에 최신값 반환: 완료 전 값으로 회귀 방지

#### 한줄 요약

- 선형화 모델은 쓰기 성공을 받은 뒤 다른 사용자가 읽을 때 이전 값이 나오지 않도록 완료 전에 필요한 복제본을 맞춘다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Causal Consistency (인과적 일관성)**: "질문이 작성됨 $\rightarrow$ 답변이 달림"처럼 원인과 결과가 명확한 데이터만 순서를 보장하고, 서로 무관한 게시글은 순서가 뒤섞여 보여도 허용하는 모델.

</details>

| 일관성 모델 | 보장 강도 | 보장 내용 및 특징 | 주요 사용처 |
|:---|:---|:---|:---|
| Linearizability | **Strong** | 실시간 순서와 최신 완료값 보장 | **잔액, 재고 불변식** |
| Sequential | 상 (Strong) | 모든 노드가 동일한 작업 순서를 관찰함 | 멀티플레이 게임 이벤트 |
| Causal | 중상 (Medium) | 인과 관계가 있는 데이터만 순서 보장 | 댓글 및 대댓글 시스템 |
| Session | 중 (Medium) | **내(Session)가 쓴 데이터는 내가 즉시 최신으로 봄**| **SNS 내 프로필 편집** |
| Eventual | **Weak** | 추가 Write가 없으면 Replica 수렴 | **피드, 집계 Cache** |

#### 한줄 요약

- 선형화는 실제 시간까지, 순차 일관성은 모두가 보는 한 순서까지, 인과 일관성은 원인 순서까지 지키며 최종 일관성은 잠시 달라도 결국 같은 값으로 모인다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Split-Brain (스플릿 브레인)**: 네트워크 단절로 인해 2개의 노드가 서로 리더(Leader)라고 주장하며 양쪽에서 쓰기를 다 받아버려, 나중에 네트워크가 복구되었을 때 데이터 정합성이 완전히 붕괴되는 현상.

</details>

| 3대 일관성 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. Split-Brain 충돌 | 네트워크 단절 시 양방향 쓰기 허용 | **과반수(Quorum) 투표 기반 Raft/Paxos 합의 알고리즘 적용**|
| 2. Stale Read 불만 | 결제 후 포인트가 안 깎인 걸로 보임 | **결제/재고 등 핵심 DB는 $W+R>N$ 강한 일관성 세팅** |
| 3. 동시성 재고 마이너스 | 동시에 마지막 남은 재고 1개를 구매 요청 | **DB Optimistic Lock(버전 검사) 및 조건부 차감**|

> 사례: **아마존 DynamoDB의 Eventual Consistency 기본값 적용 및 결제 시 Strong Consistency 옵션 강제 튜닝**

#### 한줄 요약

- 재고는 현재 버전과 수량이 맞을 때만 차감하고 사용자가 방금 쓴 프로필은 세션 토큰보다 오래된 복제본에서 읽지 않게 해야 한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **일관성 수립 기준**: 비즈니스 도메인 불변식(Invariant)에 기반한 Quorum 튜닝, CAP 타협, Session Consistency(RYW) 보장 및 Raft 알고리즘에 의거한 체계.

</details>

- 잔액•재고는 **선형화•조건부 Write**, 피드•Cache는 최종 수렴 선택

#### 한줄 요약

- 재고·잔액은 강한 보장과 조건부 쓰기를 사용하고 피드·캐시는 세션 보장과 충돌 수렴으로 지연과 가용성을 확보해야 한다.
