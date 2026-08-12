---
sidebar:
  order: 105
  label: "105. CRDT 충돌 없는 복제 데이터 (Conflict-free Replicated Data Type)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "CRDT 충돌 없는 복제 데이터 (Conflict-free Replicated Data Type)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 105
extra:
  question_no: "105"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "CRDT는 무조정 병합•수렴 설계의 현안"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **CRDT (Conflict-free Replicated Data Type)**: Marc Shapiro 박사 등이 정립한 분산 수학적 자료구조로, 중앙 합의 알고리즘(Paxos/Raft)이나 락(Lock) 없이 분산 노드가 오프라인 상태에서 각각 동시 수정을 수행하더라도, 수학적 가반반군(Semi-lattice) 특성 기반으로 메시지를 렌더링하면 100% 충돌 없이 결정적으로 동일하게 수렴하는 자료구조.
- **Strong Eventual Consistency (SEC, 강한 최종 일관성)**: 노드 간 동기화 순서나 메시지 도착 순서와 전혀 무관하게, 동일한 업데이트 집합을 수신받은 모든 분산 노드가 100% 동일한 상태값에 최종 수렴함을 보장하는 성질.
- **Join-Semilattice (상한 반시분격자)**: 교환 법칙(Commutative), 결합 법칙(Associative), 멱등성(Idempotent)을 만족하는 수학적 결합 연산자($\sqcup$)를 지닌 상한 반격자 구조.

</details>

- 정의/개념: 분산 환경에서 중앙 합의(Consensus)나 락 제어 없이 각 노드가 로컬 이벤트를 독립적으로 수행한 후, 수학적 반격자 연산을 통해 100% 충돌 없이 최종 동일 상태로 결정적 병합 수렴을 이루는 분산 자료형인 **CRDT**
- 배경/필요성: 구글 도구(Google Docs), Figma 등 실시간 협업 에디터에서 오프라인 모드 수정 수용, 분산 DB 노드 간 락 제어로 인한 Latency 및 네트워크 단절 병목 극복 요구성

#### 한줄 요약

- 각자 고친 사본을 어떤 순서로 합쳐도 같은 결과가 되게 만든 자료형이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **3-Mathematical Properties**: 교환 법칙($A \sqcup B = B \sqcup A$), 결합 법칙($(A \sqcup B) \sqcup C = A \sqcup (B \sqcup C)$), 멱등성($A \sqcup A = A$).
- **No Consensus / Zero Blocking**: 2PC나 Raft 합의 없이 오프라인 로컬 데이터 변경 즉시 확정.

</details>

- **Strong Eventual Consistency (SEC) 강한 최종 일관성** 달성
- 수학적 3대 조건 **(교환성, 결합성, 멱등성)** 완비
- **State-based (CvRDT)** 대 **Operation-based (CmRDT)** 2가지 동기화 방식 제공

#### 한줄 요약

- 기술적으로 같은 값에는 도달하지만 그 값이 업무상 옳은지는 별도로 확인해야 한다.

## Ⅲ. 구조 및 구성요소 (State-based CvRDT vs Operation-based CmRDT)

<details><summary>핵심 용어</summary>

- **CvRDT (State-based / Convergent Replicated Data Type)**: 노드의 전체 데이터 상태(State)를 전파하여 LUB(Least Upper Bound) 연산으로 병합(Merge)하는 방식 (메시지 수신 순서 상관없음, 멱등성 보장).
- **CmRDT (Operation-based / Commutative Replicated Data Type)**: 변경 연산자(Op)만을 네트워크로 전파하여 수신노드가 이를 실행(Apply)하는 방식 (메시지 유실 불가, Causal Order 전달 필수).

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        CRDT 2대 구현 아키텍처                          │
├───────────────────────────────────┬────────────────────────────────────┤
│ 1. CvRDT (State-based)            │ 2. CmRDT (Operation-based)         │
├───────────────────────────────────┼────────────────────────────────────┤
│  Node A ──(Full State/Delta)──► Node B │  Node A ──(Operation Delta)──► Node B │
│  Merge(State A, State B)          │  Apply(Op A)                       │
│  • LUB Semi-lattice 멱등 연산자   │  • 인과적 전달 (Causal Delivery)   │
└───────────────────────────────────┴────────────────────────────────────┘
```

선의 의미: CvRDT는 전체 상태/델타를 전파하여 가반반군 멱등 병합을 수행하고, CmRDT는 변경 오퍼레이션을 인과적 전달 수단을 통해 실행하는 아키텍처.

| 구분 (Category) | CvRDT (State-based / Convergent) | CmRDT (Operation-based / Commutative) |
|:---|:---|:---|
| **전파 대상 데이터**| **전체 상태(State) 또는 델타(Delta) 분량** | **개별 변경 연산자(Operation / Delta)** |
| **네트워크 요구 조건**| 메시지 중복, 재정렬, 유실에 안전 (멱등성) | **메시지 유실 엄금 (Exactly-Once / Causal)**|
| **병합(Merge) 함수**| **LUB (Least Upper Bound) 상한 연산자 사용**| **Commutative Op (교환 가능한 연산) 실행** |
| **페이로드 크기** | 상대적 큼 (전체 상태 전파 시) | **상대적 극소 (연산자 조각만 전파)** |

#### 한줄 요약

- 사본과 변경표, 순서표, 합치는 규칙, 전달 담당자로 구성된다.

## Ⅳ. 흐름도 (CRDT 카운터: PN-Counter 병합 프로세스)

<details><summary>핵심 용어</summary>

- **PN-Counter (Positive-Negative Counter)**: 증가(P) 벡터와 감소(N) 벡터를 각 노드별로 독립 배열로 유지하여, $A - B$ 최종 카운트를 100% 충돌 없이 계산해내는 CRDT 카운터.

</details>

```text
[Node A: P=[1,0], N=[0,0] (+1 증가)] ──────┐
                                           ├─► Merge(Max Vector): P=[1,2], N=[0,1]
[Node B: P=[0,2], N=[0,1] (+2증가, -1감소)] ┘   Total = (1+2) - (0+1) = 2 (완벽 수렴!)
```

### 동작 원리

1. **Local Mutation**: 노드 A는 `P[0] += 1` 증가, 노드 B는 `P[1] += 2, N[1] += 1` 변경.
2. **State Propagation**: 각 노드의 Vector 배열을 타 노드로 교환.
3. **Merge Operation**: `P_Merged = Max(P_A, P_B)`, `N_Merged = Max(N_A, N_B)` 원소별 최고값(Max) 취함 $\rightarrow$ **배열 교환 결과 최종 카운트 2로 양 노드 100% 동일 수렴**.

#### 한줄 요약

- 두 사본이 변경표를 주고받아 같은 값이 되었는지와 그 값이 업무상 허용되는지를 확인한다.

## Ⅴ. 종류 및 비교 (CRDT 4대 대표 자료형)

<details><summary>핵심 용어</summary>

- **LWW-Element-Set (Last-Write-Wins Set)**: 타임스탬프를 부여하여 가장 최신에 추가/삭제된 Element가 이기는 형태의 CRDT Set.
- **RGA (Replicated Growing Array)**: Figma, Google Docs 등 텍스트 에디터에서 글자 순서 삽입/삭제를 충돌 없이 처리하는 시퀀스 CRDT.

</details>

| CRDT 자료형 | 대표 구조 (Data Type) | 충돌 해결 메커니즘 및 특징 |
|:---|:---|:---|
| **G-Counter / PN-Counter** | **Vector Counter** | 노드별 증가(P)/감소(N) 벡터를 Max 연산하여 수렴 |
| **LWW-Element-Set** | **Set (Add-Set / Remove-Set)** | 타임스탬프 부여하여 마지막 쓰기(LWW)가 최종 승리 |
| **OR-Set (Observed-Remove)**| **Set with Tag** | 각 Element마다 고유 Tag(UUID)를 주어 삽입/삭제 추적 |
| **RGA / Yjs / Automerge** | **Sequence Array (Text Edit)**| **Figma, Google Docs 동시 문서 편집 전용 시퀀스** |

#### 한줄 요약

- 현재 상태를 합치거나 변경 명령을 전달하되 어느 쪽도 합치는 규칙이 핵심이다.

## Ⅵ. 실무 고려사항 및 대책 (CRDT 한계성 및 메모리 관리)

<details><summary>핵심 용어</summary>

- **Tombstone Cleanup (묘비 제거)**: CRDT에서 데이터 삭제 시 즉시 지우지 않고 묘비(Tombstone) 태그를 달아두는데, 이 Tombstone이 메모리에 계속 누적되어 성능이 저하되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 삭제 태그(**Tombstone**)가 계속 누적되어 메모리 폭증 | **모든 노드 동기화 완료 후 GC 기반 Tombstone Purge** | 메모리 오버헤드 해소 |
| 시계열 타임스탬프 오차로 인한 LWW 실수 오버라이드 | **Lamport Timestamp 또는 Vector Clock 인과성 결합** | 데이터 덮어쓰기 방지 |
| CRDT 수렴 결과와 비즈니스 수량 제약(재고 < 0) 충돌 | **CRDT 기반 최종 수렴 + 비즈니스 유효성 검증 레이어**| 무결성 파괴 방지 |

> 사례: **Figma 실시간 화이트보드 (Yjs CRDT) & Redis Hashes/Counters CRDT 수용**

#### 한줄 요약

- 동시에 편집한 글은 자동으로 합칠 수 있어도 문장의 의미가 자연스러운지는 사람이 확인해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **CRDT 수립 기준(CRDT Architecture Standards)**: 무조정 오프라인 수정 요건, SEC 일관성 목표 및 Yjs/Automerge 라이브러리 수용성에 의거한 체계.

</details>

- **CRDT 수립 기준**에 따라 실시간 동시 협업 에디터/오프라인 DB 구축 시 **Yjs / Automerge 기반 CRDT 자료구조** 필수 적용

#### 한줄 요약

- CRDT 적용 판단 기준은 값의 수렴과 업무상 올바름을 구분한다.
