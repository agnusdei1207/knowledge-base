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
- **개요**: 여러 노드가 장애와 지연 속에서도 하나의 값·로그 순서에 동의하는 알고리즘
- **왜 필요한가**: 분산 DB, 설정 저장소, 클러스터 매니저는 여러 노드가 같은 순서로 명령을 적용해야 split-brain과 데이터 손상을 피할 수 있다.
- **핵심 직관**: 회의 참석자 일부가 늦거나 빠져도 과반이 같은 회의록 순서에 서명해야 결정이 확정되는 구조이다.

## 깊이 이해
- **배경·문제의식**: 네트워크 지연, 노드 장애, 메시지 중복이 있는 환경에서 단순 다수결만으로는 같은 순서의 로그를 보장하기 어렵다.
- **작동 원리**: Raft는 leader election, log replication, safety rule로 문제를 나눈다. Paxos는 proposer, acceptor, learner가 proposal number 기반으로 값을 선택한다.
- **비유**: Raft는 회장 선출 후 회장이 안건을 순서대로 배포하고 과반 서명을 받는 방식, Paxos는 번호표가 붙은 제안 중 과반이 수락한 제안을 채택하는 방식임.
- **구체 예시**: etcd는 Raft로 key-value 변경 로그를 과반 노드에 복제한 뒤 Kubernetes API 서버의 클러스터 상태를 일관되게 저장함.
- **흔한 오해·주의점**: 합의 알고리즘은 모든 노드 응답을 기다리지 않는다. 보통 3노드는 2개, 5노드는 3개 과반이면 커밋 가능하나 partition에서 minority는 쓰기 불가임.

## 연결 개념
- Quorum — 과반 합의 기준
- Leader Election — Raft의 리더 선출
- Linearizability — 합의 로그가 제공하는 강한 일관성

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

분산 합의는 여러 노드가 같은 값과 순서에 동의하는 알고리즘이다. 분산 시스템은 노드 장애와 네트워크 partition 때문에 단일 서버처럼 상태를 관리하기 어렵다. Raft·Paxos는 과반 quorum으로 로그 커밋 순서를 확정해 split-brain을 방지한다.

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

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
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
