---
sidebar:
  order: 177
  label: "177. 분산 합의: Raft•Paxos (Distributed Consensus Raft Paxos)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "분산 합의: Raft•Paxos (Distributed Consensus Raft Paxos)"
date: "2026-08-14T03:40:00+09:00"
tags:
  - "notes-software"
weight: 177
extra:
  question_no: "177"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "과반수•리더 교체•로그 안전성의 기반 가치"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Distributed Consensus (분산 합의)**: 네트워크 분할이나 노드 장애가 발생하더라도, 분산 시스템 내의 정상적인 다수 노드(Quorum)가 단일한 데이터 값이나 연산 순서에 대해 동일한 결론에 도달하도록 보장하는 알고리즘 원리.
- **Raft**: 이해와 구현이 매우 난해한 Paxos를 대체하기 위해 리더 선출(Leader Election), 로그 복제(Log Replication), 안전성(Safety) 문제로 분리하여 설계된 이해하기 쉬운(Understandable) 분산 합의 알고리즘.
- **Paxos**: 레슬리 램포트(Leslie Lamport)가 제안한 최초의 수학적으로 완벽한 분산 합의 알고리즘으로, 제안자(Proposer), 수락자(Acceptor), 학습자(Learner) 역할로 나누어 과반수 합의를 이끌어내는 프로토콜.

</details>

- 정의/개념: 장애 중 단일 값•순서에 동의하는 **분산 합의**
- 배경/필요성: 독립 Node 결정은 Partition에서 **Split-Brain•Log 분기** 유발

#### 한줄 요약

- 서버 일부가 끊겨도 과반 장부가 겹치는 성질을 이용해 같은 순서 위치에 두 개의 다른 명령이 확정되지 않게 한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Term (임기)**: Raft에서 논리적인 시간을 나타내는 단조 증가(Monotonically Increasing) 번호. 새로운 선거가 시작될 때마다 증가하며, 오래된 임기를 가진 리더의 명령은 즉각 무시되는 펜싱(Fencing) 토큰 역할.

</details>

- **Strong Leader (강력한 리더십)**: 클라이언트의 모든 쓰기 요청은 오직 리더(Leader) 노드만이 수신하고 팔로워들에게 전파하며, 리더가 죽었을 때만 새로운 리더 선출.
- **Leader Election (리더 선출)**: 리더로부터 심장박동(Heartbeat)이 끊기면 팔로워가 후보자(Candidate)로 승격하여 과반수(Quorum) 투표를 얻어 새 리더로 등극.
- **Log Replication (로그 복제)**: 리더가 받은 명령을 로그 엔트리로 만들어 팔로워들에게 복제하고, 과반수가 기록(Append)에 성공하면 커밋(Commit)하여 상태 머신에 반영.

#### 한줄 요약

- 새 대표는 과반에 남은 이전 기록을 이어받고 과반과 통신하지 못하는 대표는 새 결정을 확정하지 못한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Quorum (정족수/과반수)**: 총 노드 수가 $N$개일 때, $\lfloor N/2 \rfloor + 1$ 개 노드의 동의. 서로 다른 두 Quorum은 반드시 1개 이상의 교집합 노드를 가지므로, 절대 2개의 다른 결론(Split-Brain)이 나오지 않음을 수학적으로 보장.

</details>

```text
[Raft Cluster]
 ├── [Leader]
 ├── [Candidate]
 ├── [Follower]
 └── [Replicated Log]
```

| 구성요소 | 책임 |
|---|---|
| Leader | Client Write 수신과 **Log 복제•Commit** 조정 |
| Candidate | Term 증가와 **과반 Vote** 요청 |
| Follower | AppendEntries•Vote 요청을 **Term**•**Log** 기반 검증 |
| Replicated Log | 합의된 **Command 순서** 및 Commit Index 보존 |

#### 한줄 요약

- 리더가 안건을 내면 팔로워가 장부에 기록하고 과반 승인 뒤 상태 머신이 같은 순서로 실행하며 스냅샷이 오래된 장부를 압축한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Two-Phase Commit (2PC) 유사성**: Raft의 로그 복제는 리더가 명령을 뿌리고(1단계), 과반수가 디스크에 썼다고 보고하면 커밋을 선언(2단계)하는 점에서 2PC와 비슷하나, 전체 노드(All)가 아닌 과반수(Quorum)만으로 진행되어 가용성이 훨씬 높은 알고리즘.

</details>

```text
[Write 요청]
     │
     ▼
1. Leader Log Append
     │
     ▼
2. Follower AppendEntries
     │
     ▼
3. Quorum Ack 확인
     │
     ▼
4. Commit•State Machine 적용
     │
     ▼
5. Commit Index 전파
     │
     ▼
[Write 성공 반환]
```

### 동작 원리

1. Leader Log Append: Current Term의 Command 기록
2. Follower AppendEntries: 이전 Index•Term 확인 후 복제
3. Quorum Ack 확인: 과반 Replica의 저장 승인 집계
4. Commit•State Machine 적용: Commit Index 이동과 실행
5. Commit Index 전파: 후속 Heartbeat로 Follower 적용 통지

#### 한줄 요약

- 세 노드 중 두 노드가 같은 명령을 기록해야 확정하므로 한 노드가 끊겨도 두 개의 서로 다른 과반 결정은 생기지 않는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Multi-Paxos (멀티 팩소스)**: 단일 값만 합의하는 Basic Paxos를 확장하여 연속적인 로그(상태 머신)를 구축하기 위해 고안된 구조이나, 규격화된 문서가 부족하여 구현체(Chubby, Spanner)마다 다르게 파편화된 복잡한 알고리즘.

</details>

| 구분 | Raft | Paxos (Multi-Paxos) |
|:---|:---|:---|
| 설계 철학 | **이해성(Understandability) 최우선 (교육/구현 용이)**| **수학적 완벽성 (최초 제안, 논문 난해)** |
| 리더 선출 | **합의의 선행 조건으로 강력한 리더를 먼저 선출** | 리더 없이도 진행 가능하나 성능 위해 리더 차용 |
| 로그 관리 | **리더의 로그가 절대적 기준 (방향성: 리더 $\rightarrow$ 팔로워)**| 각 인스턴스(로그 슬롯)별로 합의 도출 |
| 대표 구현체 | **etcd, Consul, CockroachDB, MongoDB, Kafka(KRaft)**| Google Spanner, Chubby, Apache ZooKeeper(ZAB) |

#### 한줄 요약

- 래프트는 리더 선출과 로그 복제 절차를 분리해 설명하고 팩소스는 번호가 더 큰 제안이 과거 승인값을 이어받는 원리를 중심으로 한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Election Timeout Randomization (무작위 선거 타임아웃)**: 모든 팔로워가 동시에 타임아웃되어 다 같이 후보자가 되면 표가 갈라져(Split Vote) 아무도 리더가 못 되는 현상을 막기 위해, 각 노드의 타임아웃 시간을 150ms ~ 300ms 사이로 랜덤하게 분산하는 래프트 핵심 기법.

</details>

| 3대 합의 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. Split Vote 무한 반복 | 후보자들의 동시 선거 출마로 표 분산 | **노드별 Election Timeout 랜덤 설정** |
| 2. Log 무한 증식 | 합의된 로그가 디스크 공간 한계치 초과 | **정기적 Snapshotting(스냅샷 압축) 후 과거 로그 삭제** |
| 3. 네트워크 파티션 고립 | 분할된 구역에 고립된 구 리더가 쓰기 수신| **과반수 Ack 실패 시 커밋 불가 (새 리더가 임기 갱신)**|

> 사례: **Kubernetes의 두뇌인 etcd 클러스터를 무조건 3, 5, 7개의 홀수(Odd) 노드로 배포하여 뗏목(Raft) 정족수를 유지하는 운영 사례**

#### 한줄 요약

- 설정 저장소는 과반이 기록하지 못하면 새 설정을 거부하고 시간이나 난수 결과도 로그에 넣어 모든 노드가 같은 값을 실행하게 해야 한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Replicated State Machine (복제된 상태 머신)**: 동일한 초기 상태를 가진 서버들이, 합의 알고리즘에 의해 똑같은 순서의 결정적(Deterministic) 로그 명령을 실행하면, 최종적으로 완벽히 동일한 상태에 도달한다는 분산 시스템의 최종 목표.

</details>

- 단일 제어 상태는 **합의**, Quorum 상실 시 Write 거부 선택

#### 한줄 요약

- 리더·설정처럼 하나의 정답이 필요한 제어 상태에만 합의를 사용하고 과반 상실 시 쓰기를 거부해 서로 다른 결정의 동시 확정을 막아야 한다.
