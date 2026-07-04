---
title: "분산 합의 — Raft·Paxos (Distributed Consensus Raft Paxos)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 209
---

# 📖 【암기용】 개념 완전 이해

> 목적: 분산 합의 Raft·Paxos를 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 여러 노드가 장애·지연 속에서도 하나의 값 또는 로그 순서에 동의하도록 만드는 **복제된 상태 머신(Replicated State Machine)** 구현 알고리즘 — 핵심 도구는 **Quorum(과반) 합의**다.
- **왜 필요한가**: 분산 DB, 설정 저장소, 클러스터 매니저는 여러 노드가 정확히 같은 순서로 명령을 적용해야 split-brain(둘 이상의 리더가 서로 다른 결정을 내리는 상황)과 데이터 손상을 피할 수 있다.
- **핵심 직관**: 회의 참석자 일부가 늦거나 자리를 비워도 "과반수"가 같은 회의록 순서에 서명해야 그 결정이 확정되는 구조다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| Replicated State Machine | 같은 명령 로그를 같은 순서로 여러 노드에 적용해 상태를 동일하게 유지하는 기법 — 합의가 만들어주는 결과물 | 여러 지점이 같은 순서의 전표를 처리해 항상 같은 잔액을 유지 |
| Quorum(과반) | 전체 노드 중 과반수 — 결정이 확정되려면 반드시 필요한 최소 동의 수 | 이사회에서 과반 찬성이 있어야 안건 통과 |
| Term(Raft) | 리더 임기를 세는 논리적 시계 — 새 선거마다 1씩 증가 | 국회 회기 번호, 회기가 바뀌면 새 의장 선출 |
| Leader / Follower / Candidate(Raft) | 리더=명령 제안, Follower=수신·응답, Candidate=선거 중 후보 상태 | 의장(리더), 참석자(팔로워), 입후보자(캔디데이트) |
| Log Replication(Raft) | 리더가 명령을 로그에 추가하고 팔로워에 복제하는 절차 | 의장이 회의록 항목을 각 참석자에게 배포 |
| Commit Index(Raft) | 과반이 복제 확인한 로그 위치 — 이 지점까지는 확정(상태머신 적용 가능) | "몇 번 항목까지 모두 서명 완료"로 표시된 줄 |
| Proposer / Acceptor / Learner(Paxos) | 제안자 / 수락자 / 학습자 — Paxos의 세 역할 | 제안자=안건 발의자, 수락자=투표권자, 학습자=결과 통보받는 사람 |
| Proposal Number(Paxos) | 제안마다 매기는 고유 증가 번호 — 최신 제안 판별 기준 | 안건에 붙는 접수 번호, 더 큰 번호가 이후 제안 |
| Split-Brain | 둘 이상의 노드가 동시에 자신이 리더라고 믿고 서로 다른 결정을 내리는 장애 | 두 명이 동시에 "내가 의장이다"라며 서로 다른 결정을 공표 |

## 깊이 이해

### 왜 다수결만으로는 부족한가 (문제의식)
- 네트워크 지연, 노드 장애, 메시지 중복·순서 뒤바뀜이 있는 환경에서 단순 다수결 투표만으로는 두 가지 문제가 생긴다. 하나는 동시에 두 후보가 과반을 나눠 가져 아무도 리더가 되지 못하는 상황(split vote), 다른 하나는 리더가 확정된 뒤에도 낡은 리더가 계속 명령을 내리는 상황(split-brain)이다. Raft·Paxos는 이를 각각 무작위 타임아웃과 Term/Proposal Number로 해결한다.

### Raft 리더 선출 — 숫자로 이해
- 5노드 클러스터라면 과반은 3이다(⌊5/2⌋+1). 모든 노드는 election timeout(보통 150~300ms 사이 무작위값)을 갖고 있다가, 그 시간 동안 리더의 heartbeat를 못 받으면 스스로 candidate가 되어 Term을 1 올리고 투표를 요청한다.
- 무작위 타임아웃을 쓰는 이유: 모든 노드가 같은 타임아웃을 쓰면 동시에 candidate가 되어 표가 갈릴 위험(split vote)이 크다. 150~300ms처럼 범위를 두면 한 노드가 먼저 깨어나 다른 노드보다 먼저 투표를 받아갈 확률이 높아져 대부분 한 번에 리더가 정해진다.
- 한 Term에는 최대 1명의 리더만 존재할 수 있다 — 각 노드는 같은 Term에서 한 번만 투표하므로, 5노드 중 3표를 받으면(과반) 나머지 2노드는 이미 표를 다 썼으니 같은 Term에서 다른 candidate가 동시에 3표를 받을 수 없다.

### 로그 복제와 커밋 — 워크드 예제
- 리더가 클라이언트 명령 `SET x=5`를 받으면 자신의 로그에 (index=10, term=3, command=SET x=5)로 추가하고 모든 팔로워에게 복제 요청(AppendEntries)을 보낸다.
- 5노드 중 자신 포함 3곳(리더+팔로워 2곳)이 "복제 완료" 응답을 보내면 과반(3/5) 충족 → commit index를 10으로 올리고 상태머신에 `x=5`를 반영한 뒤 클라이언트에 성공 응답한다. 나머지 2노드는 아직 못 받았어도 상관없다 — 다음 heartbeat 때 따라잡는다(replication lag).
- 리더가 죽으면 새로 선출되는 리더는 "가장 로그가 길고 최신 Term을 가진" 후보만 당선될 수 있도록 제한되어(선거 제한 규칙) 이미 커밋된 로그가 사라지지 않는다.

### Paxos — 제안 번호로 합의하는 원리
- Paxos는 두 단계로 진행된다. ① Prepare/Promise: proposer가 proposal number n(예: n=5)으로 "n보다 작은 제안은 더 이상 받지 않겠다는 약속"을 과반 acceptor에게 요청한다. ② Accept/Accepted: 과반이 약속하면 proposer가 실제 값을 담아 accept 요청을 보내고, 과반이 수락하면 그 값이 확정된다.
- **경쟁 예제**: proposer P1이 n=5로 값 "A"를 제안 중인데 동시에 P2가 n=7로 값 "B"를 제안하면, acceptor들은 더 큰 번호(7)의 약속을 우선하므로 P1의 n=5 제안은 accept 단계에서 거절당한다. 번호 비교만으로 "누구 제안이 이겼는지"가 결정되어 두 값이 동시에 확정되는 일이 없다.
- Paxos는 이렇게 일반적인 이론을 제시하지만 실제 구현(멀티 Paxos)이 복잡해서, Raft는 "리더가 있으면 매번 새로 경쟁할 필요가 없다"는 점에 착안해 리더 임기(Term) 하나로 절차를 단순화한 것이다.

### 비유와 흔한 오해
- 비유: Raft는 "회장을 먼저 뽑고 회장이 안건을 순서대로 배포해 과반 서명을 받는" 방식이고, Paxos는 "번호표가 붙은 제안 중 과반이 수락한 가장 최근 제안을 채택하는" 방식이다.
- 오해 1: 합의는 "모든 노드"의 응답을 기다리지 않는다. 3노드면 2개, 5노드면 3개 과반이면 커밋 가능하다 — 그래야 노드 1~2개가 죽어도 서비스가 계속된다.
- 오해 2: 합의 클러스터는 홀수 노드로 구성하는 것이 정석이다. 4노드는 과반이 3이라 노드 2개가 죽으면(4개 중 2개 남음, 과반 미달) 서비스가 멈추는데, 이는 5노드가 2개 죽어도 3개로 과반을 유지하는 것보다 내결함성이 나쁘다 — 짝수는 노드만 늘고 내결함성 이득은 없다.

## 연결 개념
- Quorum — 과반 합의를 가능하게 하는 산술적 기준 (208 참고)
- Replicated State Machine — 합의 알고리즘이 궁극적으로 만들어주는 결과물
- Linearizability — 합의 로그가 제공하는 강한 일관성 보장 (208의 최상위 등급)

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 수치·표준명·비교축으로 작성한다.
> 핵심: 분산 합의는 알고리즘 암기가 아니라 장애 환경에서 로그 순서와 split-brain 방지를 보장하는 통제 기술이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 분산 합의는 여러 노드가 동일한 값과 로그 순서에 과반 기준으로 동의하는 알고리즘이다.
> 2. **가치**: leader election, log replication, quorum commit으로 메타데이터 저장소와 분산 DB의 일관성을 보장한다.
> 3. **판단 포인트**: 노드 수, quorum, leader 장애, 네트워크 partition, commit latency를 함께 판단해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 분산 합의 원리 확인 | quorum, leader, log replication, safety | 단순 투표 또는 replication과 혼동 |
| Raft·Paxos 비교 확인 | Raft 이해 용이성, Paxos 이론 일반성 | 두 알고리즘을 제품명으로 설명 |
| 운영 적용 판단 확인 | etcd, ZooKeeper, Consul, DB metadata | 노드 수·quorum·split-brain 조건 누락 |

> 요약: 이 문제는 Raft·Paxos 절차와 함께 장애 시 과반 합의로 일관성을 유지하는 판단을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 여러 노드의 값·순서 합의 알고리즘
- 배경: 분산 시스템은 노드 장애와 네트워크 partition 때문에 단일 서버처럼 상태를 관리하기 어렵다.
- 필요성: Raft·Paxos의 과반 quorum, leader election, log commit 기준으로 split-brain을 방지한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client Command -> Leader/Proposer -> Follower/Acceptor Quorum -> Commit Log -> State Machine
                              +-> Election / Term / Proposal Number
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Leader/Proposer | 값 또는 로그 항목 제안 | Raft leader, Paxos proposer |
| Follower/Acceptor | 제안 수신·투표·수락 | 과반 응답 필요 |
| Log/Value | 합의 대상 | 순서 보장 필요 |
| Quorum | commit 안전성 기준 | 3노드 2개, 5노드 3개 |

> 요약: 합의는 제안자, 수락자, 합의 로그, quorum으로 구성되며 과반 교집합이 안전성을 만든다.

---

## Ⅲ. 동작원리 및 흐름도

```text
리더 선출 -> 명령 수신 -> 로그 복제 -> 과반 ACK -> commit -> 상태머신 적용
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | timeout 후 후보가 term 증가 및 투표 요청 | 한 term 한 leader |
| 2 | leader가 client command를 log append | log index·term 기록 |
| 3 | follower 과반이 append ACK 반환 | quorum 충족 |
| 4 | leader가 commit index 전파 후 state machine 적용 | committed log 순서 동일 |

> 요약: Raft 계열 합의는 리더 선출, 로그 복제, 과반 승인, 상태머신 적용으로 동일 순서를 보장한다.

---

## Ⅳ. 특징

| 구분 | Paxos | Raft | 판단 포인트 |
|:---|:---|:---|:---|
| 접근 | proposer·acceptor·learner | leader·follower·candidate | Raft가 구현·교육 비용 낮음 |
| 절차 | prepare/accept 단계 | election/log/safety 분리 | 운영 설명 가능성 |
| 적용 | 이론 기반 다수 변형 | etcd, Consul 등 | Kubernetes metadata는 etcd Raft |
| 비용 | quorum round trip | leader 중심 1~2 RTT | p95 commit latency 측정 |

> 요약: Paxos는 일반 이론 기반, Raft는 이해와 구현을 위해 문제를 분해한 합의 알고리즘이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단일 primary | consensus cluster | 메타데이터 RPO 0, leader 장애 자동 복구 필요 |
| 비용/성능 | 로컬 쓰기 | quorum commit | 3노드 기준 2개 ACK 지연 허용 |
| 운영/위험 | 단일 장애점 | quorum 상실 시 쓰기 중단 | 홀수 노드, 3/5/7 구성 권장 |

> 요약: 합의 클러스터는 쓰기 지연 증가를 감수하고 RPO 0 수준의 메타데이터 일관성을 얻을 때 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| quorum 상실 | 노드 장애·partition | 홀수 노드, anti-affinity | quorum available 99.9% |
| split-brain | 다중 leader | term·lease·fencing token | dual leader 0건 |
| 로그 지연 | follower lag | snapshot, compaction, disk IOPS 관리 | follower lag, fsync latency |

> 요약: 운영 리스크는 quorum 상실, 다중 리더, 로그 지연이며 배치·fencing·스토리지 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 가용성 | quorum availability 99.9% 이상 | cluster health |
| 지연 | commit p95 50ms 이하 또는 업무 SLA | consensus metric |
| 복구 | leader failover 5초 이하 | fault injection test |

> 요약: 합의 품질은 quorum 가용성, commit 지연, leader failover 시간으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. etcd·Consul·ZooKeeper는 3개 또는 5개 홀수 노드로 구성하고 zone anti-affinity로 동일 장애 도메인 배치를 피함.
2. 쓰기 경로에는 deadline 500ms, fsync latency 모니터링, snapshot·compaction 정책을 적용해 로그 적체를 통제함.
3. leader 변경, term 증가, quorum loss, follower lag를 알람화하고 chaos test로 partition 시 minority 쓰기 차단을 검증함.

**결론 (2줄):**
- 기술사 판단: 클러스터 메타데이터와 리더 선출은 Raft·Paxos 합의, 대용량 데이터 경로는 별도 replication·sharding을 선택함.
- 향후 방향: 분산 DB와 Kubernetes 기반 플랫폼은 합의 계층을 숨기되, 운영자는 quorum과 지연 지표를 계속 관리해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "분산 합의를 설명하시오" | leader election, log replication, quorum commit | Raft·Paxos 구조 비교 |
| 요구사항 명시형 | "클러스터 일관성 방안을 제시하시오" | quorum, split-brain 방지, failover | 노드 수, 리스크 대응, 운영 지표 |

> 요약: 설명형은 알고리즘 절차, 방안형은 quorum 설계와 장애 검증 중심으로 전환한다.
