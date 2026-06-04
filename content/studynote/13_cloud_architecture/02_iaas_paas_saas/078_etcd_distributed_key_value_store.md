+++
title = "78. etcd (엣시디) - 클러스터의 모든 상태 정보(설정, 메타데이터)를 저장하는 고가용성 분산 Key-Value 저장소"
date = 2026-04-07

[taxonomies]
tags = ["studynote-cloud"]

[extra]
tags = ["studynote-cloud"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: etcd는 작은 크기의 중요한 상태 정보를 저장하는 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) K/V (Key-Value) 저장소다.
> 2. **가치**: [Raft](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/) ([Raft](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/) [Consensus Algorithm](/knowledge-base/studynote/06_ict_convergence/01_blockchain/011_consensus_algorithm/)) 합의를 통해 클러스터가 같은 사실을 보게 만든다.
> 3. **판단 포인트**: etcd는 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)과 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 위한 저장소이지, 큰 본문 데이터를 담는 범용 데이터베이스가 아니다.

---

## Ⅰ. 개요 및 필요성

[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템은 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), [서비스 디스커버리](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/306_service_discovery_pattern/), 리더 선출처럼 모두가 같은 값을 봐야 하는 순간이 많다. etcd는 그런 "공통 메모" 역할을 한다.
특히 [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 같은 클라우드 제어면에서는 노드 상태와 오브젝트 상태가 흔들리면 전체 운영이 불안정해진다.
```text
Client -> Leader -> Followers
         | Raft log commit |
         v
     snapshot / watch event
```

- **📢 섹션 요약 비유**: [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템은 모두가 같은 상태를 봐야 흔들리지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

etcd는 클라이언트 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) ([Application Programming Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/))를 통해 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)와 읽기를 받는다. [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 요청은 리더를 거쳐 합의되고, 커밋된 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 팔로워에 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)된다.
watch는 키 변화 알림을, lease는 임시 자원의 생명주기를, snapshot과 compaction은 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 정리하는 역할을 한다.
| 구성 요소 | 역할 | 판단 포인트 |
| --- | --- | --- |
| Leader | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 합의의 중심 | 쿼럼을 만족해야 반영된다 |
| Followers | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)와 읽기 보조 | 상태를 따라간다 |
| Watch | 변경 이벤트 전달 | 구성 관리에 자주 쓴다 |
| Lease | [TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) 기반 임시값 관리 | [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)·에페메랄 자원에 유리하다 |
| [Snapshot](/knowledge-base/studynote/02_operating_system/10_security/637_zfs_snapshot_cow_architecture/)/[Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 압축과 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) | 운영 안정성을 높인다 |

- **📢 섹션 요약 비유**: [Raft](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/), watch, lease, snapshot이 제어면을 만든다.

---

## Ⅲ. 비교 및 연결

etcd는 Redis처럼 빠른 캐시가 아니라, 정확한 합의가 필요한 제어면 저장소다. ZooKeeper와 비교하면 모두 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 조정에 쓰이지만, etcd는 watch와 간결한 K/V API가 강점이다.
클라우드 관점에서는 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 하나보다 등가 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)된 저장소가 훨씬 안전하다. 그래서 etcd는 인프라의 기준점이 된다.
| 비교축 | etcd | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) | [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) |
| --- | --- | --- | --- |
| [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 가능 | 조정 중심 |
| 주요 용도 | [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)/[설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 캐시/[세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 조정 |
| 클라우드 적합성 | 매우 높다 | 보조적 | 높다 |

- **📢 섹션 요약 비유**: etcd는 캐시가 아니라 합의 기반 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 저장소다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 작은 값, 낮은 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 빈도, 높은 정확성이 필요한 곳에 etcd를 둔다. 반대로 큰 오브젝트나 대량 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), 장기 보관 데이터는 적합하지 않다.
[백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), quorum, [네트워크 지연](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/), [compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 주기를 함께 점검해야 한다. 특히 단일 리전이 아니라면 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차를 먼저 설계해야 한다.
### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)과 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)처럼 작은 값을 저장하는가?
2. watch와 lease가 실제 운영 패턴에 맞는가?
3. [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)과 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차가 문서화되어 있는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 큰 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이나 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 그대로 넣는 것
- [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 없이 quorum만 믿고 운영하는 것

- **📢 섹션 요약 비유**: 작고 중요한 상태에만 써야 제 역할을 한다.

---

## Ⅴ. 기대효과 및 결론

etcd를 잘 쓰면 동적 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), [서비스 디스커버리](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/306_service_discovery_pattern/), 리더 선출이 안정된다. 제어면의 단일 진실 공급원으로 볼 수 있다.
앞으로는 멀티 클러스터와 엣지 환경에서 etcd의 운영 패턴과 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 자동화가 더 중요해진다.
기술사는 이 주제를 "클러스터가 함께 보는 작은 공용 노트"로 기억하면 된다.

- **📢 섹션 요약 비유**: 제어면의 기준점을 하나로 묶는 것이 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| --- | --- |
| [Raft](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/) | 합의 알고리즘이다 |
| Quorum | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 반영의 기준이다 |
| Watch | 변경 이벤트를 알린다 |
| Lease | 임시 자원 수명을 관리한다 |
| [Snapshot](/knowledge-base/studynote/02_operating_system/10_security/637_zfs_snapshot_cow_architecture/) | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 압축하고 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)한다 |
| Leader election | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 제어의 핵심 기능이다 |

### 📈 관련 키워드 및 발전 흐름도

```text
write request
  |
  v
Raft consensus
  |
  v
commit to log
  |
  v
watch event
  |
  v
controllers react
```

### 👶 어린이를 위한 3줄 비유 설명

1. 반장 셋이 모두 도장 찍어야 공책 내용을 바꾸는 반 공책과 같다.
2. 한 명만 마음대로 적으면 반 전체가 헷갈린다.
3. 그래서 모두가 같은 공책을 보게 만드는 것이 중요하다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 77 / 371

<- **이전**: [77. Kube-API Server - 모든 K8s 명령(kubectl)을 REST API로 수신하고 컴포넌트 간 통신을 중계하는 허브](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/077_kube_api_server_k8s_hub/)
**다음**: [79. Kube-Scheduler (스케줄러) - 새로 생성된 Pod가 자원 여유가 있는 어떤 워커 노드에 배치될지 결정](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) ->

---
