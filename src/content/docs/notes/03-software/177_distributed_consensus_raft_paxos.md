---
sidebar:
  order: 177
  label: "177. 분산 합의: Raft•Paxos"
  badge:
    text: "미출 · 50%"
    variant: note
title: "분산 합의: Raft•Paxos (Distributed Consensus Raft Paxos)"
date: "2026-08-26T10:25:00+09:00"
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

- **분산 합의(Distributed Consensus)**: 비동기 네트워크 환경에서 일부 노드 장애나 지연이 발생해도 과반수(Quorum) 노드가 동일한 값과 순서에 동의하도록 보장하는 분산 알고리즘.
- **Raft vs Paxos**: 이해와 구현이 난해한 Paxos를 리더 선출, 로그 복제, 안전성 3단계로 명확히 분리하여 재설계한 알고리즘(Raft).

</details>

- 정의/개념: 노드 장애와 네트워크 분할 환경에서도 **과반수(Quorum) 합의를 통해 동일한 연산 순서와 상태 머신을 일관되게 복제하는 분산 합의 알고리즘**
- 배경/필요성: 분산 노드의 독립 판단 시 발생하는 **네트워크 단절 시 Split-Brain 발생, 로그 분기 및 데이터 정합성 파괴 해결 불가**

#### 한줄 요약
- 과반수 투표와 Replicated Log를 통해 노드 결함 시에도 단일 상태 머신의 무결성을 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Term(임기)**: Raft에서 논리적 시간을 나타내는 단조 증가 번호로 구 리더의 쓰기를 차단하는 Fencing Token 역할.
- **Strong Leader**: 모든 클라이언트 쓰기 요청은 오직 리더만이 수신하고 팔로워들에게 단방향 복제하는 강력한 리더십.

</details>

- 모든 쓰기를 단일 리더가 수신하여 팔로워에게 단방향 복제하는 **Strong Leader 모델**
- 리더 심장박동 두절 시 후보자가 출마하여 과반수 투표를 얻는 **리더 선출(Leader Election)**
- 과반수($N/2 + 1$) 노드에 로그 기록 성공 시 커밋을 확정하는 **로그 복제(Log Replication)**

#### 한줄 요약
- 강력한 리더십, 과반수 선거, 안전한 로그 복제를 통해 분산 클러스터의 단일 진실점을 유지한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Raft 3대 노드 상태**: Leader(쓰기 접수/로그 전파), Candidate(선거 출마/투표 요청), Follower(심장박동 수신/로그 기록).

</details>

```text
[Raft 분산 합의 클러스터 구조]
├── Leader Node
│   ├── Client Write Request 수신
│   ├── Replicated Log Append
│   └── AppendEntries RPC 브로드캐스트
├── Follower Nodes
│   ├── Heartbeat 수신 및 로그 디스크 기록
│   └── 타임아웃 시 Candidate 승격
├── Candidate State
│   └── Term 증가 및 RequestVote 과반수 투표
└── Replicated State Machine
    └── 합의된 로그 순서대로 상태 갱신
```

선의 의미: 계층 및 리더가 클라이언트 요청을 받아 Replicated Log에 기록하고 과반수 팔로워에 복제하여 상태 머신을 동기화하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| 리더 (Leader) | 모든 클라이언트 쓰기 요청을 수신하고 **팔로워들에게 로그 복제(AppendEntries) 및 커밋 총괄** | 단일 쓰기 진입점 |
| 후보자 (Candidate) | 리더 장애 시 **Term(임기)을 증가시키고 팔로워들에게 RequestVote 과반 투표 요청** | 리더 선출 주체 |
| 팔로워 (Follower) | 리더의 심장박동(Heartbeat)을 수신하며 **로그를 디스크에 기록하고 일치성 검증** | 수동적 수신자 |
| 복제 로그 (Log) | 합의된 명령어의 **전역 순서(Log Index)와 Term 번호를 불변 디스크에 영속 보관** | Replicated Log |

#### 한줄 요약
- 리더, 후보자, 팔로워, 복제 로그가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Raft 로그 복제 5단계**: 쓰기 요청 수신 $\to$ 로컬 로그 기록 $\to$ 팔로워 복제 RPC 전송 $\to$ 과반수(Quorum) 승인 확인 $\to$ Commit 확정 및 회신.

</details>

```text
클라이언트의 상태 갱신 쓰기 요청
        │
   1. [로컬 로그 기록] Leader가 현재 Term의 명령어를 자신의 Replicated Log에 미커밋 추가
        │
   2. [복제 RPC 브로드캐스트] Leader가 팔로워들에게 `AppendEntries` RPC를 병렬 전송
        │
   3. [과반수 승인 집계] 전체 $N=3$ 노드 중 과반수($W=2$) 이상의 팔로워로부터 기록 완료 Ack 수신
        │
   4. [Commit 확정] Leader가 `commitIndex`를 전진시키고 상태 머신(State Machine)에 실제 반영
        │
   클라이언트에게 성공 회신을 보내고, 후속 Heartbeat를 통해 팔로워들에게 최종 Commit 전파
```

#### 한줄 요약
- 로컬 기록 → 복제 RPC 전송 → 과반수 승인 → Commit 확정 → 결과 회신 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Raft vs Multi-Paxos**: 이해성과 구현성을 최우선한 Raft와 수학적 원리를 최초로 정립한 Paxos.

</details>

| 비교 항목 | Raft 알고리즘 | Paxos (Multi-Paxos) |
|:---|:---|:---|
| 핵심 설계 철학 | **이해 가능성(Understandability) 최우선 설계** | **수학적 완벽성 최우선 (논문 및 구현 난해)** |
| 리더 선출 방식 | **합의의 필수 전제 조건으로 단일 리더 선출** | 리더 없이도 동작 가능하나 성능 위해 리더 차용 |
| 로그 복제 방향 | **리더의 로그가 절대 기준 (단방향 강제 덮어쓰기)**| 슬롯(Slot)별 독립 합의 후 로그 조립 |
| 대표적 구현체 | **etcd, Consul, CockroachDB, Kafka(KRaft)** | **Google Spanner, Chubby, Apache ZooKeeper(ZAB)**|

#### 한줄 요약
- 명확한 리더십과 구현 용이성은 Raft, 전통적 분산 스토리지 원형은 Multi-Paxos를 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Randomized Election Timeout**: 모든 노드가 동시에 후보자로 출마하여 표가 분산(Split Vote)되는 현상을 방지하기 위해 타임아웃을 150~300ms 사이로 무작위 분산하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 동시 후보자 출마로 표 분산되어 선거 무한 교착 (Split Vote) | **노드별 Election Timeout을 150ms~300ms 사이 난수로 무작위 분산** | 단일 후보자 조기 과반 득표 보장 |
| 로그 무한 누적으로 인한 디스크 고갈 및 복구 지연 | **정기적 Snapshotting (상태 머신 스냅샷 압축 후 과거 로그 폐기)** | 디스크 용량 절감 및 복구 가속 |
| 소수파 구역에 고립된 구 리더가 클라이언트 쓰기 수신 | **과반수 Ack 실패 시 커밋 불가 및 새 리더의 높은 Term에 의해 퇴역** | Split-Brain 데이터 오염 원천 차단 |
| 짝수 노드 구성 시 과반수 쿼럼 상실 취약점 | **etcd/Consul 클러스터는 반드시 3, 5, 7개의 홀수(Odd) 노드로 구축** | 결함 허용 가용성 극대화 |

#### 한줄 요약
- 랜덤 타임아웃, 스냅샷 압축, 과반수 검증, 홀수 노드 배치로 운영한다.

## Ⅶ. 결론

- 쿠버네티스 etcd, 분산 DB 등 단일 상태 진실점이 필수적인 인프라 환경에서 **과반수(Quorum) 투표와 단일 리더십 기반의 Raft 분산 합의 알고리즘을 표준 채택**하고, **홀수 노드 배치와 스냅샷 압축 정책**을 결합하여 네트워크 단절 시에도 결함 없는 분산 합의 체계 완성

#### 한줄 요약
- Raft는 명확한 리더 선출과 과반수 로그 복제를 통해 분산 시스템의 Split-Brain을 방지하고 상태 머신의 완벽한 일관성을 달성하는 핵심 합의 기술이다.