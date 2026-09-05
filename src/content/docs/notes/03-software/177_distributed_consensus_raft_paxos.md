---
sidebar:
  order: 177
  label: "177. 분산 합의: Raft•Paxos"
  badge:
    text: "미출 · 50%"
    variant: note
title: "분산 합의: Raft•Paxos (Distributed Consensus Raft Paxos)"
date: "2026-08-31T10:48:00+09:00"
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

- 정의/개념: 노드 장애와 네트워크 분할 환경에서도 과반수(Quorum) 합의를 통해 동일한 연산 순서와 상태 머신을 일관되게 복제하는 분산 합의 알고리즘
- 배경/필요성: 비동기 분산 시스템에서 노드들이 독자적으로 상태 갱신 시 발생하는 네트워크 분할(Split-Brain) 및 데이터 불일치(Data Divergence) 한계

#### 한줄 요약
- 과반수 투표와 복제 로그로 커밋된 명령의 순서를 유지한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Term(임기)**: Raft에서 논리적 시간을 나타내는 단조 증가 번호로 구 리더의 쓰기를 차단하는 Fencing Token 역할.
- **Strong Leader**: 모든 클라이언트 쓰기 요청은 오직 리더만이 수신하고 팔로워들에게 단방향 복제하는 강력한 리더십.

</details>

- 모든 쓰기를 단일 리더가 수신하여 팔로워에게 단방향 복제하는 Strong Leader 모델
- 리더 심장박동 두절 시 후보자가 출마하여 과반수 투표를 얻는 리더 선출(Leader Election)
- 과반수($N/2 + 1$) 노드에 로그 기록 성공 시 커밋을 확정하는 로그 복제(Log Replication)

#### 한줄 요약
- 강력한 리더십, 과반수 선거, 안전한 로그 복제를 통해 분산 클러스터의 단일 진실점을 유지한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Raft 3대 노드 상태**: Leader(쓰기 접수/로그 전파), Candidate(선거 출마/투표 요청), Follower(심장박동 수신/로그 기록).

</details>

```text
[Raft 분산 합의 클러스터 구조]
├── Leader
├── Follower
├── Candidate
├── Replicated Log
└── Replicated State Machine
```

선의 의미: 계층 및 리더가 클라이언트 요청을 받아 Replicated Log에 기록하고 과반수 팔로워에 복제하여 상태 머신을 동기화하는 구조

| 구성요소 | 책임 |
|:---|:---|
| Leader | AppendEntries 전송과 커밋 인덱스 관리 |
| Follower | 심장박동 수신과 로그 일치성 검증 |
| Candidate | Term 증가와 RequestVote 요청 |
| Replicated Log | Log Index·Term·명령 보관 |
| State Machine | 커밋 순서대로 명령 적용 |

#### 한줄 요약
- 리더가 복제 로그의 순서를 독점 결정하고 상태 머신은 커밋된 순서만 적용하므로, 노드들이 서로를 직접 조율하지 않고도 동일한 상태에 도달한다.

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
   3. [과반수 승인 집계] 리더를 포함한 과반수 복제본의 기록 확인
        │
   4. [Commit 확정] Leader가 `commitIndex`를 전진시키고 상태 머신(State Machine)에 실제 반영
        │
   클라이언트에게 성공 회신을 보내고, 후속 Heartbeat를 통해 팔로워들에게 최종 Commit 전파
```

동작 원리:

1. 로컬 로그 기록: 리더가 현재 Term 명령 추가
2. 복제 RPC 브로드캐스트: AppendEntries 전송
3. 과반수 승인 집계: 정족수의 기록 완료 확인
4. Commit 확정: commitIndex 전진과 상태 적용

#### 한줄 요약
- 과반수 승인 이전의 로그는 언제든 덮어써질 수 있고 이후에는 되돌릴 수 없으므로, 커밋 확정 시점이 곧 안전성과 응답 지연을 맞바꾸는 경계가 된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Raft vs Multi-Paxos**: 이해성과 구현성을 최우선한 Raft와 수학적 원리를 최초로 정립한 Paxos.

</details>

| 비교 항목 | Raft 알고리즘 | Paxos (Multi-Paxos) |
|:---|:---|:---|
| 핵심 설계 철학 | 이해 가능성을 고려한 역할 분리 | 합의 단계를 수학적으로 정의 |
| 리더 선출 방식 | 합의의 필수 전제 조건으로 단일 리더 선출 | 리더 없이도 동작 가능하나 성능 위해 리더 차용 |
| 로그 복제 방식 | 리더 중심 AppendEntries | 슬롯별 합의와 안정 리더 활용 |
| 대표 계열 | etcd·Consul·KRaft | Multi-Paxos 계열 시스템 |

#### 한줄 요약
- 명확한 리더십과 구현 용이성은 Raft, 전통적 분산 스토리지 원형은 Multi-Paxos를 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Randomized Election Timeout**: 모든 노드가 동시에 후보자로 출마하여 표가 분산(Split Vote)되는 현상을 방지하기 위해 타임아웃을 150~300ms 사이로 무작위 분산하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 동시 후보자 출마에 따른 Split Vote | 무작위 Election Timeout 적용 | 재선거 충돌 가능성 감소 |
| 로그 무한 누적으로 인한 디스크 고갈 및 복구 지연 | 정기적 Snapshotting (상태 머신 스냅샷 압축 후 과거 로그 폐기) | 디스크 용량 절감 및 복구 가속 |
| 소수 진영의 구 리더가 쓰기 수신 | 과반수 실패 시 **커밋 제한·Term 갱신** | 미커밋 쓰기의 상태 적용 차단 |
| 노드 수 대비 장애 허용 효율 저하 | 장애 목표에 맞는 홀수 투표 노드 구성 | 동일 정족수의 불필요 노드 감소 |

#### 한줄 요약
- 네 대책은 과반수라는 합의 조건이 선거 충돌·디스크·정족수 비용으로 되돌아오는 지점을 완화한 것이며, 노드를 늘려도 정족수만 커질 뿐 쓰기 처리량은 늘지 않는다.

## Ⅶ. 결론

- 현대 클라우드 네이티브 인프라의 핵심 제어면(etcd, Kubernetes, Kafka KRaft, Consul, TiKV)을 지탱하는 가장 핵심적인 분산 합의 및 고가용성 메타데이터 관리의 사실상 표준(de facto standard)으로 확립되었으며, 실무 구축 시에는 동시 출마 충돌을 방지하는 150~300ms 무작위 선거 타임아웃(Randomized Election Timeout), 디스크 고갈을 방지하는 Log Compaction/Snapshotting, 홀수 노드(3대 또는 5대) 쿼럼 클러스터링, 구 리더의 오동작을 방어하는 Term/Fencing 검증을 결합하여 무결점 분산 합의 인프라를 완성

#### 한줄 요약
- 과반수 상실 시 쓰기 가용성을 포기하고 커밋 안전성을 유지한다.
