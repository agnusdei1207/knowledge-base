+++
title = "646. 블록체인 노드 스토리지 병목 현상"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 노드 스토리지 병목은 거래 1건이 단순 추가 기록으로 끝나지 않고, <strong>상태 조회·해시 갱신·키값 저장소 정리 작업</strong>으로 분해되면서 많은 무작위 읽기와 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 일으키는 데서 생긴다.
> 2. **가치**: 이 병목은 단순 저장 용량 문제가 아니라 신규 노드 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 시간, 운영 비용, 참여 가능한 노드 수를 결정하므로, 결국 네트워크의 탈중앙성과 확장성에 직접 영향을 준다.
> 3. **판단 포인트**: 해결책은 빠른 [솔리드 스테이트 드라이브](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/475_ssd_structure/) ([Solid State Drive](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/), [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/)) 하나를 다는 것이 아니라, <strong>핫 상태 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>와 과거 이력 분리, 자료구조 완화, <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/">쓰기 증폭</a> <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/">억제</a></strong>를 함께 설계하는 데 있다.

---

## Ⅰ. 개요 및 필요성

[블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 노드는 과거 블록 이력과 [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)를 동시에 유지하는 저장 시스템이다. 블록은 순차적으로 쌓이므로 겉보기에는 단순한 append-only 구조처럼 보이지만, 실제 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 단계에서는 `지금 계정 잔액이 얼마인지`, `스마트 계약의 현재 상태가 무엇인지`를 계속 읽고 갱신해야 한다. 즉, [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 저장 계층은 아카이브 저장소이면서 동시에 매우 바쁜 온라인 상태 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)이기도 하다.

문제가 커지는 이유는 블록 크기와 거래 수가 늘수록 과거 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 커지는 것이 아니라 `현재 상태 집합`도 함께 비대해지기 때문이다. 상태가 메모리에 다 올라가지 않으면 무작위 디스크 접근이 급증하고, 새로운 노드가 네트워크에 합류할 때 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)가 며칠씩 걸릴 수 있다. 결국 스토리지 병목은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 문제를 넘어, 비싼 장비를 가진 운영자만 노드를 돌릴 수 있게 만드는 참여 장벽으로 이어진다.

- **📢 섹션 요약 비유**: [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 노드는 낡은 장부를 창고에 쌓아두는 회계팀이 아니라, 예전 장부와 오늘 장부를 동시에 뒤적이며 지금 잔액까지 맞춰야 하는 은행 창구와 같다. 장부가 두꺼워질수록 창구 속도부터 떨어진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

대부분의 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 노드는 블록 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 상태 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/), 영수증·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) 계층을 동시에 관리한다. 여기서 진짜 병목은 [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)를 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 구조에 맞게 갱신하는 과정이다. 머클 패트리시아 [트라이](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/087_trie/) (Merkle Patricia [Trie](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/066_trie/), MPT) 같은 구조는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 한 항목이 바뀌어도 경로 상위 노드들의 해시를 다시 계산해야 하며, 이 노드들이 다시 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 구조 병합 트리 ([Log-Structured Merge-tree](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/221_lsm_tree_memtable_sequential_flush_compaction/), LSM tree) 기반 키값 저장소에 기록되면서 추가 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 낳는다.

아래 그림은 신규 블록 반영 시 저장 계층에서 병목이 어떻게 누적되는지 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ New block commit path inside a blockchain node                    │
├────────────────────────────────────────────────────────────────────┤
│ [Execute Tx]                                                      │
│      │                                                           │
│      ├─ random read ──> [State Trie]                             │
│      │                      │                                    │
│      └─ hash update ───────>│                                    │
│                             ▼                                    │
│                      [KV store / LSM tree] -> Flush -> Compaction │
│                                                  │               │
│                                                  ▼               │
│                                               [SSD / NVMe]       │
└────────────────────────────────────────────────────────────────────┘
```

| 저장 계층 | 주 역할 | 주된 I/O 패턴 | 병목 원인 |
| :--- | :--- | :--- | :--- |
| 블록 본문 | 과거 거래와 헤더 보존 | 비교적 순차 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) | 용량 증가 |
| 상태 [트라이](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/087_trie/) | 현재 잔액·계약 상태 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) | 무작위 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) | 트리 탐색과 해시 재계산 |
| LSM 기반 KV 저장소 | 실제 키-값 영속화 | flush + [compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) | [쓰기 증폭](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/)과 읽기 증폭 |
| [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)/캐시 | 빠른 재시작과 조회 보조 | 대용량 읽기 | 메모리 부족 시 효율 급락 |

이 구조 때문에 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 저장 문제는 `얼마나 많이 저장할까`보다 `어떤 패턴으로 읽고 쓸까`가 더 중요하다. 비휘발성 메모리 익스프레스 ([Non-Volatile Memory Express](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/), [NVMe](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/)) 저장장치는 무작위 접근에 유리하고, 존드 [네임스페이스](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/) (Zoned [Namespaces](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/700_nvme_namespaces/), [ZNS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/703_zns_ssd/)) 기반 장치는 LSM [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 패턴과 정렬될 때 [compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 부담을 줄일 수 있다. 그러나 하드웨어를 바꿔도 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 구조와 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 배치가 그대로면 근본 병목은 남는다.

- **📢 섹션 요약 비유**: 글자 하나를 고칠 때마다 색인표, 목차, [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 번호까지 다시 붙여야 하는 거대한 백과사전과 같다. 책장이 빨라져도 편집 방식이 그대로면 힘든 것은 여전하다.

---

## Ⅲ. 비교 및 연결

일반 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)는 필요한 경우 덮어쓰기와 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 재구성을 통해 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 최적화할 수 있지만, [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 노드는 불변 이력과 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능성까지 유지해야 한다. 그래서 단순 조회 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)보다 [쓰기 증폭](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/)과 상태 관리 부담이 훨씬 크다. 또한 모든 노드가 같은 역할을 맡을 필요는 없으므로, 저장 전략도 노드 유형에 따라 달라진다.

| 노드 유형 | 보관 범위 | 장점 | 단점 |
| :--- | :--- | :--- | :--- |
| 아카이브 노드 (Archive Node) | 전체 이력 + 모든 과거 상태 | 가장 강한 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)·분석 능력 | 저장공간과 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 비용이 매우 큼 |
| [풀 노드](/knowledge-base/studynote/06_ict_convergence/01_blockchain/083_full_node_complete_ledger/) ([Full Node](/knowledge-base/studynote/06_ict_convergence/01_blockchain/083_full_node_complete_ledger/)) | 전체 블록 + [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) 중심 | [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)과 운영의 균형 | 상태 비대화 영향을 직접 받음 |
| 프루닝 노드 (Pruned Node) | 최근 상태 + 필요한 이력 일부 | 저장 비용 절감 | 오래된 상태 질의와 포렌식에 제약 |
| 무상태 클라이언트 ([Stateless](/knowledge-base/studynote/15_devops_sre/05_devsecops/239_stateless_redis/) [Client](/knowledge-base/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/)) 지향 구조 | 최소 상태 + 외부 증명 활용 | 참여 장벽 완화 가능 | 증명 배포 체계가 별도로 필요 |

이 비교는 `모든 노드가 모든 데이터를 영원히 들고 있어야 한다`는 단순 가정을 깨 준다. 최근에는 롤업과 [데이터 가용성](/knowledge-base/studynote/06_ict_convergence/01_blockchain/094_data_availability_da_layer_celestia/) 계층이 이력을 분리하고, 버클 트리 (Verkle Tree) 나 상태 증명 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)이 상태 접근 비용을 줄이려 한다. 즉 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 저장 진화는 저장장치만 빨라지는 방향이 아니라, 노드가 반드시 갖고 있어야 하는 정보를 더 작고 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능하게 만드는 방향으로 움직인다.

- **📢 섹션 요약 비유**: 모든 사람이 집에 국가기록원을 통째로 들여놓고 살 필요는 없다. 어떤 집은 원본 보관소가 되고, 어떤 집은 오늘 필요한 서류만 빠르게 보는 민원 창구가 되는 식으로 역할을 나눠야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 체인 유형과 노드 역할을 먼저 구분해야 한다. 거래 확정 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 핵심인 운영 노드는 [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) 캐시와 무작위 읽기 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 중요하고, 규제 대응이나 포렌식이 필요한 노드는 장기 이력 보존 전략이 중요하다. 따라서 `모든 노드에 같은 스토리지 정책`을 적용하는 것은 대부분 비효율적이다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) 집합이 메모리에 어느 정도 상주할 수 있는가?
2. 키값 저장소 [compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 시간과 디스크 대기시간을 분리 관측하고 있는가?
3. 최근 상태, 과거 이력, [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)을 물리적으로 다른 계층으로 나눌 수 있는가?
4. 프루닝을 적용해도 필요한 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)·증명 요구사항을 충족하는가?
5. [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)용 [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) 배포 체계가 준비되어 있는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 낮은 입출력 초당 처리 횟수 (Input/Output Operations Per Second, IOPS) 의 네트워크 블록 스토리지 위에 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 노드를 올리는 경우
- 핫 상태 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 거의 조회하지 않는 오래된 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 같은 장치, 같은 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 정책으로 묶는 경우
- 저장공간 절약만 보고 과도하게 프루닝하여 나중에 증명 서비스나 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 요구를 수행하지 못하는 경우

기술사 관점에서는 `체인의 합의 구조`만큼이나 `저장 구조의 감당 가능성`을 같이 봐야 한다. 블록 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 속도를 올리기 전에 상태 캐시 [적중률](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/264_hit_ratio/), [compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 폭발 시 tail [latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/), 신규 노드 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 시간을 먼저 재야 한다. 저장 병목을 무시하면 합의 알고리즘을 아무리 고도화해도 실효 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 금방 바닥난다.

- **📢 섹션 요약 비유**: 고속 열차를 새로 들였는데 역 플랫폼이 너무 좁아 승객을 못 태우는 상황과 같다. 선로만 빠르게 깔아서는 전체 교통량이 늘지 않는다.

---

## Ⅴ. 기대효과 및 결론

스토리지 병목을 줄이면 신규 노드 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 시간이 짧아지고, 같은 하드웨어로 더 높은 거래 처리량과 더 안정적인 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 지연을 얻을 수 있다. 무엇보다 운영 비용이 낮아져 더 많은 참여자가 노드를 돌릴 수 있으므로, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 개선이 [탈중앙화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/) 개선으로도 이어진다. 그래서 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 스토리지 최적화는 단순 인프라 튜닝이 아니라 네트워크 구조를 건강하게 만드는 작업이다.

다만 불변 원장이라는 특성상 저장 문제를 완전히 없앨 수는 없다. 결국 상태 축소, 증명 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/), 역할 분리, 더 나은 저장장치의 조합이 필요하다. 이 주제를 기억할 때는 `블록체인은 용량만 많이 먹는다`가 아니라, <strong><a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a> 가능한 상태를 유지하기 위해 비싼 무작위 읽기·<a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 비용을 계속 지불하는 시스템</strong>이라는 관점이 핵심이다.

- **📢 섹션 요약 비유**: [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 저장 최적화는 창고를 무작정 크게 짓는 일이 아니라, 자주 쓰는 물건은 손 닿는 선반에 두고 오래된 서류는 별도 보관소로 보내는 창고 운영술과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 머클 패트리시아 [트라이](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/087_trie/) (Merkle Patricia [Trie](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/066_trie/), MPT) | [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)를 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능하게 만들지만, 작은 변경도 다단계 해시 갱신을 유발한다. |
| [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 구조 병합 트리 ([Log-Structured Merge-tree](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/221_lsm_tree_memtable_sequential_flush_compaction/), LSM tree) | [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 노드가 자주 쓰는 키값 저장 구조로, compaction이 저장 병목의 핵심 원인 중 하나다. |
| 상태 프루닝 ([State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) [Pruning](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/)) | 오래된 상태를 줄여 운영 비용을 낮추지만, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)와 포렌식 요구와 충돌할 수 있다. |
| 비휘발성 메모리 익스프레스 ([Non-Volatile Memory Express](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/), [NVMe](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/)) | 무작위 읽기 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 높여 상태 조회 병목을 완화하는 대표 저장장치 인터페이스다. |
| 무상태 클라이언트 ([Stateless](/knowledge-base/studynote/15_devops_sre/05_devsecops/239_stateless_redis/) [Client](/knowledge-base/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/)) | 노드가 모든 상태를 직접 들고 있지 않아도 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)할 수 있게 만드는 미래 지향적 접근이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
Append-only ledger growth
    │
    ▼
State trie + authenticated storage
    │
    ▼
LSM compaction and random-read bottlenecks
    │
    ▼
NVMe / snapshots / pruning / ZNS tuning
    │
    ▼
Verkle-style proofs and stateless validation
```

이 흐름은 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 저장 이슈가 `용량 증가`에서 출발해, 결국 `상태 검증을 얼마나 작고 빠르게 만들 것인가`의 문제로 진화함을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)은 매일 일기장을 쓰는 것뿐 아니라, 오늘 기분이 어떤지도 따로 적어 두는 친구와 같아요.
2. 일기장이 너무 두꺼워지면 예전 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)와 오늘 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 같이 찾느라 시간이 오래 걸려요.
3. 그래서 자주 보는 내용은 책상 위에 두고, 오래된 내용은 정리해서 보관해야 빨리 움직일 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 647 / 803

← **이전**: [645. 데이터 파이프라인 (Data Pipeline) 가속](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)
**다음**: [647. 비잔틴 장애 허용 (BFT) 분산 시스템 검증](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) →

---
