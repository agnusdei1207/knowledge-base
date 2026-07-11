---
title: "분산 합의 — Raft·Paxos (Distributed Consensus Raft Paxos)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 209
extra:
  question_no: "209"
  exam_status: "미출제"
---

## 미리 알고가기

- 분산 합의는 장애·메시지 지연·중복·순서 변경 중에도 복제 노드가 같은 명령 순서와 결과를 선택하는 기법임
- 다수 Quorum은 서로 교차하므로 이전에 선택된 값·로그를 새 리더가 확인해 다른 값의 중복 결정을 막음
- Raft는 Leader Election·Log Replication·Safety를 Term과 연속 Log로 구성함
- Paxos는 Proposer·Acceptor·Learner가 Ballot의 Prepare/Promise·Accept 단계로 한 값을 선택함
- Multi-Paxos는 슬롯별 Paxos를 반복하고 안정된 Leader가 Phase 1을 재사용해 복제 로그를 구성함
- 합의는 비잔틴 장애를 다루지 않으며 과반 노드가 통신할 수 없으면 안전성은 유지해도 새 명령을 커밋하지 못함

## 작성 근거(검토용)

- Raft·Paxos는 결정 단위, 역할, 세대 식별자, 리더, 정상 경로, 장애 복구, 멤버십 변경으로 비교함
- 절차는 리더 확립·제안·다수 승인·커밋·리더 교체에서 두 알고리즘의 대응 단계를 병렬로 설명함
- 설정 저장소와 DB 복제 그룹은 선출 시간·p99 커밋 지연·Phase 1 재수행률로 검증함

## Ⅰ. 개요

- **정의/개념**: Raft와 Paxos는 교차하는 다수 Quorum과 증가하는 Term·Ballot을 사용해 복제 상태 머신의 한 로그 위치에 하나의 값만 선택되도록 하는 비잔틴 장애 제외 합의 알고리즘임
- **배경/필요성**: 리더·노드 장애와 네트워크 분할 후에도 설정·Lock·메타데이터·DB 명령의 순서가 갈라지지 않도록 안전한 리더 교체와 로그 커밋 기준이 필요함

## Ⅱ. 특징

- 노드는 명령을 결정적 상태 머신에 같은 순서로 적용해 동일 상태와 출력을 만듦
- Term·Ballot이 작은 이전 리더의 메시지를 거부하고 다수 응답이 가능한 리더만 새 값을 선택함
- 영속 저장한 투표·Ballot·Log·Accepted Value가 재시작 후 중복 투표와 다른 값 선택을 방지함
- Raft Leader는 AppendEntries의 이전 Index·Term을 확인해 Follower Log 충돌 구간을 복구함
- Paxos Proposer는 Phase 1 응답의 가장 높은 Ballot Accepted Value를 다음 제안에 포함해 이미 선택된 값을 보존함
- Snapshot·Log Compaction·Client 중복 제거·멤버십 변경은 기본 합의 위에 추가해야 하는 운영 기능임

## Ⅲ. 종류 및 비교

| 판단 기준 | Raft | Paxos·Multi-Paxos |
|:---|:---|:---|
| 결정 단위 | 연속된 복제 Log Entry | Single-Decree 값과 반복 Slot |
| 핵심 역할 | Leader·Follower·Candidate | Proposer·Acceptor·Learner |
| 세대 식별 | 단조 증가 Term | 단조 증가 Proposal/Ballot Number |
| 리더 구조 | 선출된 Leader만 Log를 Follower로 전파 | 기본 Paxos는 다중 Proposer, Multi-Paxos는 안정 Leader 사용 |
| 정상 복제 | AppendEntries로 이전 Log 일치와 새 Entry를 확인 | Phase 1 후 Slot별 Phase 2 Accept를 다수에 전송 |
| 리더 장애 | Election Timeout 후 RequestVote와 Log 최신성 검사 | 높은 Ballot의 Prepare로 Promise·Accepted Value 회수 |
| 멤버십 변경 | 겹치는 다수의 Joint Consensus | 구현별 Reconfiguration·Vertical Paxos 등 별도 절차 |

> 요약: Raft는 Term별 강한 Leader가 연속 Log를 복제하고 Multi-Paxos는 안정 Leader가 Phase 1 이후 Slot별 Accept를 반복함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Client·Command | 상태 머신에 순서대로 적용할 명령과 중복 식별자를 전달함 |
| Leader·Proposer | 명령의 Log Index·Slot과 Term·Ballot을 정해 Quorum에 제안함 |
| Follower·Acceptor | 투표·Promise·Log·Accepted Value를 영속 저장하고 제안에 응답함 |
| Majority Quorum | 겹치는 다수 집합으로 이전 결정과 새 제안의 연결을 보장함 |
| Replicated Log·Learner | 선택된 명령 순서를 보존하고 결정 결과를 각 노드에 전달함 |
| State Machine·Snapshot | 커밋 순서로 명령을 적용하고 오래된 Log를 상태 Snapshot으로 압축함 |

```text
Client -> Leader|Proposer -> Majority Quorum -> Committed Log|Chosen Slot
                                      -> Replicated State Machines
```

> 요약: 리더가 명령을 Quorum에 제안하고 다수의 영속 승인을 받은 Log·Slot만 상태 머신 적용 대상으로 확정함.

## Ⅴ. 원리 및 절차 흐름도

| 처리 단계 | Raft | Multi-Paxos |
|:---|:---|:---|
| 리더 확립 | Candidate가 Term을 올리고 최신 Log 조건으로 과반 투표를 받음 | Proposer가 높은 Ballot Prepare로 다수 Promise를 받음 |
| 값 제안 | Leader가 명령을 새 Index에 추가해 AppendEntries 전송 | Leader가 Slot·Ballot·Value를 Phase 2 Accept로 전송 |
| 다수 승인 | 현재 Term Entry가 다수 Log에 복제되면 Commit Index 전진 | 다수 Acceptor가 같은 Slot·Ballot 값을 수락하면 Chosen |
| 결과 적용 | Commit Index까지 순서대로 상태 머신에 적용·응답 | Learner가 Chosen Slot을 순서대로 상태 머신에 적용·응답 |
| 장애 복구 | 새 Leader가 Log 충돌을 되돌리고 누락 Entry를 재전송 | 새 Ballot Leader가 Accepted Value를 회수한 뒤 Slot 진행 |

> 요약: 두 방식 모두 새 리더가 이전 다수의 상태를 보존하고 다수 승인된 명령만 순서대로 상태 머신에 적용함.

## Ⅵ. 실무 사례

1. 클러스터 설정 저장소는 Raft 로그 복제를 적용하고 Leader 선출 시간·p99 커밋 지연을 확인함
2. 분산 DB 복제 그룹은 Multi-Paxos 안정 Leader를 적용하고 Phase 1 재수행률·Slot 커밋 지연을 확인함

## Ⅶ. 결론

- Raft·Paxos는 과반 통신·영속 상태·리더 교체·로그 복구·멤버십 변경 조건을 함께 검증해 적용해야 함
