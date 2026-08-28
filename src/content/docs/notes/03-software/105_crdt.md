---
sidebar:
  order: 105
  label: "105. CRDT 충돌 없는 복제 데이터"
  badge:
    text: "미출 · 50%"
    variant: note
title: "CRDT 충돌 없는 복제 데이터 (Conflict-free Replicated Data Type)"
date: "2026-08-26T18:17:00+09:00"
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

<details><summary>용어 설명</summary>

- **CRDT(Conflict-free Replicated Data Type)**: 중앙 서버의 락(Lock)이나 합의 없이 복제본들이 로컬에서 동시 수정되어도, 수학적 병합 함수를 통해 항상 동일한 상태로 수렴하는 분산 자료구조.
- **SEC(Strong Eventual Consistency)**: 업데이트가 전달되기만 하면 수신 순서와 무관하게 모든 노드가 결정적으로 100% 동일한 상태에 도달하는 강한 최종 일관성.

</details>

- 정의/개념: 분산 환경에서 중앙 합의나 락 없이 동시 수정된 복제본들을 **수학적 법칙(반격자 구조)에 따라 충돌 없이 동일 상태로 결정적 수렴**시키는 분산 자료구조
- 배경/필요성: 중앙 합의나 락으로 순서를 정하면 모든 갱신이 조정 노드까지 왕복해야 해 지연이 네트워크 왕복에 묶이고 단절 구간에서는 편집 자체가 불가능하므로, 병합 연산이 교환·결합·멱등 법칙을 만족하도록 자료구조를 설계해 조정 계층 없이도 같은 상태로 수렴하게 만들 필요

#### 한줄 요약
- CRDT는 조정 비용을 자료구조의 제약으로 바꾼 설계이므로, 병합 규칙으로 표현할 수 있는 연산만 쓸 수 있다는 한계를 대가로 무조정 동시 편집을 얻는다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **3대 수학적 성질**: 교환법칙($A \sqcup B = B \sqcup A$), 결합법칙($(A \sqcup B) \sqcup C = A \sqcup (B \sqcup C)$), 멱등성($A \sqcup A = A$).
- **Local-First Software**: 네트워크 연결이 없어도 로컬 디바이스에서 모든 읽기/쓰기가 즉시 완결되고 백그라운드 동기화되는 소프트웨어 패러다임.

</details>

- 메시지 전달 순서와 무관하게 동일 상태에 도달하는 **강한 최종 일관성(Strong Eventual Consistency)**
- 병합 연산의 **교환법칙, 결합법칙, 멱등성(Idempotent) 수학적 보장**
- 상태 전체를 전파하는 **CvRDT(State-based)** 와 연산자만 전파하는 **CmRDT(Operation-based)** 지원

#### 한줄 요약
- 수학적 결합법칙과 멱등성을 기반으로 락 없는 무조정 동시 편집을 지원한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CvRDT vs CmRDT**: 전체 상태를 전파하여 LUB(최소상한)로 합치는 CvRDT(State-based)와 변경 연산만 전파하는 CmRDT(Operation-based).

</details>

```text
[CRDT 동시 편집 및 결정적 병합 아키텍처]
|-- 클라이언트 A (로컬 수정 즉시 확정) ──┐
|                                        ├──► [P2P / WebRTC / WebSocket 메시지 전파]
|-- 클라이언트 B (로컬 수정 즉시 확정) ──┘           │
`-- 결정적 병합 엔진 (Deterministic Merge Function: Join-Semilattice)
    |-- G-Counter / PN-Counter (Max 연산자 기반 카운터)
    |-- OR-Set / LWW-Element-Set (UUID 태그 기반 삽입/삭제 추적 집합)
    `-- RGA / Yjs / Automerge (텍스트 시퀀스 동시 편집 트리 구조)
```

선의 의미: 계층 및 클라이언트의 독립 수정과 결합 함수를 통한 결정적 수렴 구조

| 구성요소 | 책임 |
|:---|:---|
| 복제 상태 | 로컬 변경의 **즉시 반영·보관** |
| 변경 메타데이터 | 식별자·논리 시계로 **인과 추적** |
| 병합 함수 | 교환·결합·멱등 기반 **결정적 수렴** |
| 전파 계층 | 상태·델타·연산의 **피어 전달** |

#### 한줄 요약
- 모든 복제본이 서로를 보지 않고도 같은 결과를 내야 하므로 삭제조차 지운 흔적을 메타데이터로 남겨야 하며, 조정 비용이 사라진 자리를 메타데이터 누적 비용이 대신 채운다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **PN-Counter 수렴 과정**: 증가 배열 $P[A, B]$와 감소 배열 $N[A, B]$를 노드별로 각각 $\max$ 연산하여 최종값 $\sum P - \sum N$을 계산.

</details>

```text
사용자 A와 B가 오프라인 상태에서 각각 문서 편집 (동시 수정 발생)
        │
   [로컬 즉시 반영] 노드 A와 B가 락 대기 없이 로컬 CRDT 트리에 변경 즉시 커밋
        │
   [네트워크 재연결] 노드 A와 B가 온라인으로 복구되어 Yjs CRDT 변경 메시지 상호 교환
        │
   [병합 연산 실행] 양쪽 노드가 동일한 수학적 병합 함수($\sqcup$)를 각자 독립적으로 실행
        │
   [결정적 동일 수렴] 중앙 서버 중재 없이도 노드 A와 B의 문서 내용이 100% 일치하게 자동 완성
```

#### 한줄 요약
- 로컬 커밋이 네트워크를 기다리지 않으므로 단절이 길어져도 쓰기 지연은 늘지 않지만, 재연결 시점에 교환하고 병합해야 할 상태량이 그 단절 기간에 비례해 커진다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **CRDT 4대 대표 자료형**: PN-Counter(카운터), OR-Set(집합), LWW-Set(최신승리), RGA/Yjs(텍스트 시퀀스).

</details>

| CRDT 자료형 | 대상 데이터 구조 | 충돌 해결 메커니즘 | 대표 활용 사례 |
|:---|:---|:---|:---|
| PN-Counter | 정수형 숫자 (Counter) | **노드별 증가(P)/감소(N) 벡터의 Max 연산** | 좋아요 수, 조회수, 동시 접속자 수 |
| OR-Set (Observed-Remove) | 고유 원소 집합 (Set) | **원소마다 고유 UUID 태그를 부여하여 삭제 추적** | 쇼핑몰 장바구니, 태그 목록 |
| LWW-Element-Set | 최신 우선 집합 (Set) | 타임스탬프를 비교하여 **마지막 쓰기(LWW)가 승리** | 사용자 프로필 속성 갱신 |
| RGA / Yjs / Automerge | 텍스트 시퀀스 (String) | **문자별 고유 ID와 상대적 위치 트리 링크드 리스트**| **Figma, Google Docs, Notion 동시 협업** |

#### 한줄 요약
- 카운터는 PN-Counter, 집합은 OR-Set, 동시 문서 편집은 RGA/Yjs 시퀀스를 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Tombstone Bloat**: 삭제된 텍스트/원소의 묘비(Tombstone) 메타데이터가 메모리에 계속 남아 문서 크기가 눈덩이처럼 불어나는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 삭제 태그(**Tombstone**) 누적으로 인한 메모리 팽창 | **모든 피어의 동기화 완료 확인 후 가비지 컬렉션(GC) Purge** | 메모리 오버헤드 80% 절감 |
| 클라이언트 시계 오차로 인한 LWW 데이터 덮어쓰기 | **물리 시계 대신 Lamport Timestamp 또는 Hybrid Logical Clock 적용** | 인과 관계 역전 방지 |
| 대용량 상태 전송으로 인한 네트워크 대역폭 낭비 | **전체 상태 대신 변경분만 전송하는 Delta-State CRDT 도입** | 네트워크 트래픽 90% 절감 |
| 비즈니스 불변식(예: 재고 수량 $\ge 0$) 위반 위험 | **CRDT 수렴 계층 상단에 애플리케이션 비즈니스 검증 레이어 결합** | 업무 무결성 훼손 방어 |

#### 한줄 요약
- Tombstone GC, HLC 논리 시계, Delta-State 전송, 비즈니스 검증 레이어로 안정성을 확보한다.

## Ⅶ. 결론

- 동시 협업은 **CRDT 자료구조**, 동기화는 **Delta** 선택

#### 한줄 요약
- CRDT는 중앙 서버의 락과 합의 오버헤드를 제거하고 수학적 결정성을 통해 복제본의 강력한 최종 일관성을 보장하는 현대 분산 소프트웨어의 핵심 자료구조다.
