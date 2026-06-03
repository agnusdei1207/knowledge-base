+++
title = "30. 스플릿 브레인과 쿼럼 — 분산 시스템 합의 문제"
date = 2026-04-29

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [스플릿 브레인](/knowledge-base/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/)([Split Brain](/knowledge-base/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/))은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서 네트워크 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)으로 인해 각 노드 그룹이 자신이 마스터라고 믿고 독립 동작하는 현상이다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치·충돌이 발생한다.
> 2. **가치**: 쿼럼(Quorum)은 [스플릿 브레인](/knowledge-base/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/) 방지의 핵심 메커니즘이다. 과반수(⌊N/2⌋ + 1) 노드의 동의가 있을 때만 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)/마스터 선출이 가능하도록 하여, 네트워크 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 시 단 하나의 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)만 활성화된다.
> 3. **판단 포인트**: [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리에 따라 네트워크 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)(P) 상황에서 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)(C)과 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)(A) 중 하나를 선택해야 한다. 쿼럼은 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 희생하고 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 선택하는 [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 시스템의 핵심 메커니즘이다.

---

## Ⅰ. 개요 및 필요성

```text
스플릿 브레인 시나리오:

  정상:
  [Node1(M)] ── [Node2] ── [Node3]
  M = Master, 모두 연결

  네트워크 파티션:
  [Node1(M)] ✗✗✗✗✗ [Node2(M)] ── [Node3]
      │                    │
      │                    │
  "내가 마스터!"        "내가 마스터!"
  독립 쓰기 수행        독립 쓰기 수행
  → 데이터 충돌!

쿼럼 해결:
  3노드 클러스터 쿼럼 = 2
  Node1 단독: 쿼럼 없음 → 읽기 전용
  Node2+3: 쿼럼 있음 → 정상 운영
```

- **📢 섹션 요약 비유**: [스플릿 브레인](/knowledge-base/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/)은 전화 불통된 두 지사가 각자 독립적으로 결정하는 것이다. 둘 다 "내가 본사 지시를 받은 책임자"라고 주장하며 다른 결정을 내리면 혼란이 생긴다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 쿼럼 계산

| 노드 수 | 쿼럼 | 허용 장애 수 |
|:---|:---|:---|
| 3 | 2 | 1 |
| 5 | 3 | 2 |
| 7 | 4 | 3 |
| N | ⌊N/2⌋+1 | ⌊N/2⌋ |

### [Raft](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/) [합의 알고리즘](/knowledge-base/studynote/06_ict_convergence/01_blockchain/011_consensus_algorithm/) (쿼럼 기반)

```text
리더 선출:
  1. 팔로워 타임아웃 → 후보자 전환
  2. 후보자가 전체에 투표 요청
  3. 과반수 투표 획득 → 리더 선출
  4. 리더가 하트비트 전송 (팔로워 안정화)

로그 복제:
  1. 클라이언트 → 리더에 쓰기 요청
  2. 리더 → 팔로워에 로그 항목 복제
  3. 과반수 수신 확인 → 커밋
  4. 리더 → 클라이언트에 성공 응답
```

- **📢 섹션 요약 비유**: [Raft](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/) 리더 선출은 반장 선거다. 아무도 없으면 후보가 손 들고, 반 과반수 이상의 동의를 받으면 반장(리더)이 된다. 과반수 없이는 아무도 반장이 될 수 없다.

---

## Ⅲ. 비교 및 연결

| 비교 | [Raft](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/) | Paxos | ZAB ([ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/)) |
|:---|:---|:---|:---|
| 이해 난이도 | 쉬움 | 어려움 | 중간 |
| 목적 | 범용 합의 | 범용 합의 | [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 전용 |
| 리더 | 강한 리더 | 다수 제안자 | 강한 리더 |
| 사용 | [etcd](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/), Consul | 이론 표준 | [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) |

- **📢 섹션 요약 비유**: [Raft](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/)·Paxos·ZAB는 다수결 원칙의 세 구현이다. Paxos(복잡한 민주주의 헌법), [Raft](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/)(단순화된 대통령제), ZAB([ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 전용 의원내각제)로 각각 다른 실용성을 가진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) Sentinel [스플릿 브레인](/knowledge-base/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/) 방어

```text
min-replicas-to-write 1
min-replicas-max-lag 10

→ 최소 1개 복제본이 10초 이내 응답해야 쓰기 허용
→ 마스터 고립 시 쓰기 거부 (스플릿 브레인 방지)

Sentinel 쿼럼:
  3 Sentinel → 2개 동의 시 마스터 다운 판단
  → 페일오버 수행
```

### [etcd](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/) 쿼럼 실패 대응

```text
상황: 5노드 중 3노드 장애 (쿼럼 3 요구)
→ etcd 쓰기/읽기 불가 (Kubernetes 제어 플레인 중단)

복구:
  1. 장애 노드 복구 시 자동 재합류
  2. 강제 복구: etcdctl snapshot restore
  3. 예방: 홀수 노드 유지, 다중 AZ 배포
```

- **📢 섹션 요약 비유**: [etcd](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/) 쿼럼 실패는 국회 의사 정족수 미달이다. 의원 과반수 미달(쿼럼 없음)이면 법안 심의가 불가능([쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 불가)하다. Kubernetes는 etcd가 없으면 아무 결정도 못 한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a></strong> | [스플릿 브레인](/knowledge-base/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/)으로 인한 충돌 방지 |
| <strong>자동 <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a></strong> | 쿼럼 기반 마스터 자동 선출 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/">Kubernetes</a> 안정성</strong> | [etcd](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/) 쿼럼이 클러스터 제어 보장 |

차세대 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [합의 알고리즘](/knowledge-base/studynote/06_ict_convergence/01_blockchain/011_consensus_algorithm/)으로 HotStuff·Tendermint·[BFT](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/)(Byzantine [Fault Tolerance](/knowledge-base/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/)) 변형들이 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)·Web3 환경에서 주목받고 있다. 악의적 노드(Byzantine 노드)까지 허용하는 BFT는 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) [합의 알고리즘](/knowledge-base/studynote/06_ict_convergence/01_blockchain/011_consensus_algorithm/)의 이론적 기반이 된다.

- **📢 섹션 요약 비유**: BFT는 거짓말하는 선거인도 있는 투표 시스템이다. 일부 노드가 거짓 정보를 보내도 전체 합의가 올바르게 유지되는 것이 BFT의 목표다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/">CAP</a> 정리</strong> | [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 시 C vs A 선택 |
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/">Raft</a>/Paxos</strong> | 쿼럼 기반 [합의 알고리즘](/knowledge-base/studynote/06_ict_convergence/01_blockchain/011_consensus_algorithm/) |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/">etcd</a></strong> | [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 쿼럼 기반 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) KV 저장소 |
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/">Redis</a> Sentinel</strong> | 쿼럼 기반 마스터 자동 페일오버 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/">BFT</a></strong> | 악의적 노드 포함 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 합의 |

### 📈 관련 키워드 및 발전 흐름도

```text
[스플릿 브레인 — 네트워크 파티션 시 독립 동작 충돌]
    │
    ▼
[쿼럼 — 과반수 합의로 단일 파티션 활성화]
    │
    ▼
[Paxos/Raft — 쿼럼 기반 분산 합의 알고리즘]
    │
    ▼
[etcd/ZooKeeper — 쿼럼 기반 분산 코디네이션 서비스]
    │
    ▼
[BFT/HotStuff — 블록체인 Byzantine 내성 합의]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [스플릿 브레인](/knowledge-base/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/)은 전화가 끊긴 두 지사가 각자 독립적으로 결정하는 혼란 상황이에요!
2. 쿼럼은 "과반수 동의가 없으면 결정하지 않는다"는 규칙으로 혼란을 막아요!
3. 현대 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) DB와 Kubernetes는 모두 쿼럼 원칙으로 안정적으로 운영돼요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 30 / 258

← **이전**: [29. Apache ZooKeeper](/knowledge-base/studynote/14_data_engineering/01_infrastructure/029_apache_zookeeper/)
**다음**: [31. Oozie vs Airflow — 워크플로 스케줄러 비교](/knowledge-base/studynote/14_data_engineering/01_infrastructure/031_apache_oozie_airflow/) →

---
