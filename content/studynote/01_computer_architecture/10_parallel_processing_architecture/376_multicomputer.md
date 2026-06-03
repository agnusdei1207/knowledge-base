+++
title = "376. 다중 컴퓨터 (Multicomputer)"
date = 2026-03-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 다중 컴퓨터 (Multicomputer)는 각 노드가 자기 프로세서, 메모리, 운영체제까지 독립적으로 가진 채 네트워크로 협력하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 메모리형 [MIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/372_mimd/) (Multiple [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Multiple [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 구조다.
> 2. **가치**: 메모리를 물리적으로 공유하지 않으므로 [시스템 버스](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/127_system_bus/) 병목과 중앙 메모리 경합을 피하면서, 노드 수를 늘려 처리량과 가용성을 수평 확장할 수 있다.
> 3. **판단 포인트**: 다중 컴퓨터의 성패는 CPU [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 자체보다 메시지 패싱 ([Message Passing](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/)), [데이터 지역성](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/) ([Data Locality](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/)), 장애 허용 설계가 얼마나 잘 맞물리느냐에 달려 있다.

---

## Ⅰ. 개요 및 필요성

다중 컴퓨터 (Multicomputer)는 여러 대의 독립된 컴퓨터가 하나의 [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)를 쓰지 않고, 네트워크를 통해 메시지를 주고받으며 하나의 큰 문제를 나누어 푸는 구조다. 즉 "한 대를 거대하게 키우는 방식"이 아니라 "여러 대를 협력시키는 방식"으로 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성을 확보한다.

이 개념이 필요해진 이유는 전통적인 [다중 프로세서](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/375_multiprocessor/) ([Multiprocessor](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/375_multiprocessor/))가 코어 수가 커질수록 [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/) 접근과 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 경합 때문에 급격히 비효율적이 되기 때문이다. 프로세서가 많아질수록 모두가 같은 메모리 입구로 몰리니, 계산 능력은 늘어도 실제 처리량은 선형으로 증가하지 않는다. 반면 다중 컴퓨터는 각 노드가 자기 로컬 메모리에서 대부분의 계산을 끝내고, 꼭 필요한 순간에만 통신하므로 규모를 훨씬 크게 키울 수 있다.

아래 그림은 왜 다중 컴퓨터가 등장했는지를 보여준다. 핵심은 "공유를 줄이고 협력을 네트워크로 바꿨다"는 발상의 전환이다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│      공유 메모리 확장 한계와 다중 컴퓨터의 등장 배경               │
├──────────────────────────────────────────────────────────────────────┤
│ [다중 프로세서]                                                     │
│  CPU0  CPU1  CPU2  CPU3                                             │
│    │     │     │     │                                              │
│    └─────┴─────┴─────┘                                              │
│            │                                                        │
│      Shared Memory                                                  │
│            │                                                        │
│      병목: 버스 경합 · 캐시 일관성 · 중앙 자원 포화                │
│                                                                      │
│ [다중 컴퓨터]                                                       │
│  Node0 ─── Network ─── Node1                                        │
│   │                      │                                           │
│ Local Mem0            Local Mem1                                    │
│                                                                      │
│  Node2 ─── Network ─── Node3                                        │
│   │                      │                                           │
│ Local Mem2            Local Mem3                                    │
│                                                                      │
│      효과: 로컬 계산 확대 · 수평 확장 · 장애 격리                  │
└──────────────────────────────────────────────────────────────────────┘
```

슈퍼컴퓨터, 대규모 웹 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 빅데이터 플랫폼, 대형 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 학습 클러스터가 모두 이 철학 위에 서 있다. 한 노드가 모든 것을 책임지는 것이 아니라, 작은 실패를 허용하면서 전체 규모를 키우는 구조이기 때문이다.

- **📢 섹션 요약 비유**: 다중 컴퓨터는 학생 1,000명이 한 교실 칠판 하나를 같이 쓰는 대신, 각자 교실에서 숙제를 풀고 필요할 때만 메신저로 답을 주고받는 학교 운영 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

다중 컴퓨터의 핵심 원리는 <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 메모리 (<a href="/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/378_distributed_memory/">Distributed Memory</a>)</strong> 와 <strong>메시지 패싱 (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/">Message Passing</a>)</strong> 이다. 각 노드는 자기 주소 공간만 직접 읽고 쓸 수 있으며, 다른 노드의 메모리는 Load/Store 명령으로 바로 접근할 수 없다. 따라서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공유는 네트워크를 통한 요청과 응답으로 이뤄진다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 노드 (Node) | CPU, 로컬 메모리, 운영체제를 가진 독립 실행 단위 | 노드 수 증가 시 개별 장애를 격리할 수 있어야 함 |
| 인터커넥트 (Interconnect) | 노드 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전달 경로 | 지연시간, [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), 토폴로지 설계가 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 좌우 |
| 메시지 패싱 계층 | `send/receive`, collective 연산, [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 제공 | MPI ([Message Passing Interface](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/227_mpi_message_passing_interface_distributed_computing/)), [RPC](/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/) ([Remote Procedure Call](/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/)) 등 선택 |
| 작업 분할 로직 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 노드별로 나누고 결과를 합침 | 통신량보다 계산량이 충분히 커야 효율 확보 |
| 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 계층 | 노드 실패 시 재시도, [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), 재스케줄링 수행 | 부분 실패를 시스템 전체 실패로 번지지 않게 해야 함 |

이 구조에서 중요한 것은 "계산은 로컬에서, 통신은 최소한으로"라는 원칙이다. 메시지 한 번을 보내면 직렬화, 버퍼 복사, [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 통과, 수신 측 인터럽트와 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 함께 발생하므로, 메모리 접근보다 훨씬 비싸다. 그래서 다중 컴퓨터 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 자주 대화하는 구조보다, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 먼저 잘 쪼개 놓고 각 노드가 오래 계산한 뒤 결과만 교환하는 구조가 유리하다.

아래 흐름은 메시지 패싱이 왜 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 핵심 변수인지 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                 다중 컴퓨터의 데이터 교환 흐름                      │
├──────────────────────────────────────────────────────────────────────┤
│ Node A                                                               │
│  1) 로컬 데이터 계산                                                 │
│  2) 전송 버퍼에 결과 적재                                            │
│  3) Send(message) 호출                                               │
│                 │                                                    │
│                 ▼                                                    │
│        Network / Switch / Interconnect                               │
│                 │                                                    │
│                 ▼                                                    │
│ Node B                                                               │
│  4) Receive(message) 대기 또는 인터럽트 처리                         │
│  5) 수신 버퍼에서 로컬 메모리로 복사                                 │
│  6) 다음 계산 단계 수행                                              │
│                                                                      │
│ 병목 지점: 작은 메시지 남발 · 빈번한 동기화 · 원격 데이터 의존       │
└──────────────────────────────────────────────────────────────────────┘
```

현대 시스템은 이 한계를 줄이기 위해 [인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/) ([InfiniBand](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)), [RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) (Remote [Direct Memory Access](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/318_dma/)), 고속 [토러스](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/390_torus/) ([Torus](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/390_torus/)) 또는 팻트리 (Fat-tree) 네트워크를 사용한다. 하지만 하드웨어가 빨라져도 "[공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)처럼 공짜 통신"이 되는 것은 아니므로, 애초에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 배치를 잘 설계하는 것이 더 중요하다.

- **📢 섹션 요약 비유**: 다중 컴퓨터는 각 지점이 자기 창고에서 일하다가 필요한 물건만 택배로 주고받는 물류 체계와 같다. 택배가 가능하다고 해서 볼펜 한 자루씩 계속 보내면 결국 배송비가 이익을 잡아먹는다.

---

## Ⅲ. 비교 및 연결

다중 컴퓨터를 제대로 이해하려면 [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)형 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 시스템과의 경계를 분명히 봐야 한다. 이름은 비슷하지만, 설계 철학과 병목 위치가 다르다.

| 항목 | [다중 프로세서](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/375_multiprocessor/) ([Multiprocessor](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/375_multiprocessor/)) | 다중 컴퓨터 (Multicomputer) |
| :--- | :--- | :--- |
| 메모리 구조 | 하나의 [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/) 또는 논리적 공유 주소 공간 | 노드별 독립 로컬 메모리 |
| 통신 방식 | 메모리 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) 유지 | 메시지 전송, 명시적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 |
| 지연시간 특성 | 매우 낮지만 중앙 병목 발생 가능 | 상대적으로 높지만 대규모 확장 용이 |
| 확장 방향 | 스케일업 ([Scale-up](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)) 중심 | 스케일아웃 ([Scale-out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)) 중심 |
| 대표 환경 | [SMP](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/195_real_time_scheduling/) (Symmetric Multiprocessing), [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) ([Non-Uniform Memory Access](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/)) 서버 | 클러스터, 그리드, 슈퍼컴퓨터, 클라우드 |

이 차이는 소프트웨어 구조에도 그대로 반영된다. [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/) 환경은 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/), 락, [세마포어](/knowledge-base/studynote/02_operating_system/04_synchronization/224_semaphore/) 중심으로 사고하지만, 다중 컴퓨터는 프로세스 분리, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/), 메시지 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/), [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 중심이 된다. 즉 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리의 단위가 "코어 간 협력"에서 "노드 간 협력"으로 바뀌는 셈이다.

또한 다중 컴퓨터는 [클러스터 컴퓨팅](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/383_cluster_computing/) ([Cluster Computing](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/383_cluster_computing/)), [그리드 컴퓨팅](/knowledge-base/studynote/02_operating_system/01_overview_architecture/051_grid_computing/) ([Grid Computing](/knowledge-base/studynote/02_operating_system/01_overview_architecture/051_grid_computing/)), [맵리듀스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) ([MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)), [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) ([Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)) 같은 상위 소프트웨어 생태계와 강하게 연결된다. 하드웨어 수준에서는 노드들이 느슨하게 묶여 있지만, 운영 관점에서는 스케줄러와 오케스트레이터가 이를 하나의 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 풀처럼 관리한다. 결국 다중 컴퓨터는 하드웨어 구조이면서 동시에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 사고방식의 출발점이다.

- **📢 섹션 요약 비유**: [다중 프로세서](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/375_multiprocessor/)가 한 사무실 안에서 한 장의 화이트보드를 같이 쓰는 팀이라면, 다중 컴퓨터는 여러 지사가 각자 사무실을 갖고 정해진 보고서 형식으로만 협업하는 회사와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 다중 컴퓨터를 채택할지는 "작업이 얼마나 잘 쪼개지는가"로 판단해야 한다. 요청 간 상태 공유가 적고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 노드별로 자연스럽게 분할되며, 일부 노드 실패를 허용할 수 있다면 다중 컴퓨터는 매우 강력하다. 반대로 모든 단계가 하나의 최신 상태를 즉시 공유해야 한다면, 네트워크 지연과 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 비용 때문에 오히려 불리할 수 있다.

### 적용이 잘 맞는 경우

1. <strong>대규모 웹 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a></strong>: 무상태 ([Stateless](/knowledge-base/studynote/15_devops_sre/05_devsecops/239_stateless_redis/)) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 서버를 여러 노드에 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)해 로드밸런서 뒤에 두는 구조
2. **빅데이터 분석**: [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 이미지, 배치 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 조각내 각 노드에서 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리한 뒤 최종 집계하는 구조
3. <strong>고성능 계산 (<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/548_automotive_hpc/">HPC</a>, <a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/226_hpc_supercomputing_infrastructure/">High Performance Computing</a>)</strong>: 큰 문제를 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 분할해 수천 노드에서 동시에 계산하는 구조
4. <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> <a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 학습</strong>: 여러 가속기 노드가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 또는 모델을 나누어 학습하는 구조

### 적용이 까다로운 경우

- 모든 요청이 하나의 강한 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 상태를 즉시 공유해야 하는 경우
- 작은 메시지를 초당 매우 많이 교환하는 세밀한 상호작용 구조
- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)보다 통신이 더 많은 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)

### 설계 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [ ] [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 노드별로 자연스럽게 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)되는가?
- [ ] 메시지 수를 줄이고 묶음 전송([Batching](/knowledge-base/studynote/05_database/06_dw_olap_trends/389_bulk_insert_batching_optimization/))할 수 있는가?
- [ ] 노드 장애 시 재시도, [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), 재분배 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 준비되어 있는가?
- [ ] 네트워크 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)과 지연시간이 병목이 되지 않는가?
- [ ] 중앙 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 서버나 단일 스케줄러가 새 병목으로 떠오르지 않는가?

### 대표 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 물리적으로만 노드를 늘리고, 애플리케이션은 여전히 단일 서버 전제의 공유 상태에 의존하는 경우
- 미세한 공유 변수까지 원격 호출로 쪼개어 통신 폭발을 일으키는 경우
- 계산량보다 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 셔플이 더 큰 구조를 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화라고 착각하는 경우

기술사 관점에서는 "다중 컴퓨터는 만능 확장 기술이 아니라, 통신보다 계산이 큰 문제에 적합한 구조"라고 정리하는 것이 정확하다. 하드웨어를 늘리는 행위보다 소프트웨어의 분할 경계와 장애 모델 설계가 더 중요하다.

- **📢 섹션 요약 비유**: 다중 컴퓨터는 배달 앱처럼 주문을 지역별 기사에게 나누면 강하지만, 모든 기사가 매초 같은 지도를 동시에 수정해야 하는 일에는 오히려 비효율적인 방식과 같다.

---

## Ⅴ. 기대효과 및 결론

다중 컴퓨터의 가장 큰 효과는 확장성과 내고장성이다. 저렴한 범용 노드를 추가해 처리량을 늘릴 수 있고, 일부 노드가 고장 나도 전체 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 즉시 멈추지 않도록 설계할 수 있다. 또한 지리적으로 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)된 자원을 묶어 하나의 계산 플랫폼처럼 쓸 수 있어, 클라우드와 초대형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)센터의 기본 토대가 된다.

하지만 전제조건도 분명하다. 네트워크는 메모리보다 느리고, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서는 부분 실패가 정상 상태이며, [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 유지는 공짜가 아니다. 그래서 다중 컴퓨터의 진짜 경쟁력은 하드웨어 대수가 아니라 <strong>좋은 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 배치, 통신 절제, 장애 <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 자동화</strong>에서 나온다.

앞으로는 [CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) ([Compute Express Link](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/)), [RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/), 스마트 인터커넥트 기술 덕분에 노드 간 경계가 더 흐려질 수 있다. 그럼에도 다중 컴퓨터의 핵심 기억점은 변하지 않는다. <strong>공유를 줄이고, 지역성을 살리고, 실패를 전제로 확장한다</strong>는 철학이 바로 이 구조의 본질이다.

- **📢 섹션 요약 비유**: 다중 컴퓨터는 거대한 한 몸을 키우는 대신, 서로 연락 가능한 여러 팀을 잘 조직해 큰 일을 해내는 조직 운영법과 같다. 중요한 것은 팀 수 자체보다, 누가 어떤 자료를 들고 있고 언제 협업하는지를 잘 짜는 일이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [클러스터 컴퓨팅](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/383_cluster_computing/) ([Cluster Computing](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/383_cluster_computing/)) | 다중 컴퓨터를 범용 서버 집합으로 구현한 대표 형태 |
| [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 메모리 ([Distributed Memory](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/378_distributed_memory/)) | 각 노드가 독립 주소 공간을 가진다는 구조적 전제 |
| MPI ([Message Passing Interface](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/227_mpi_message_passing_interface_distributed_computing/)) | 다중 컴퓨터 환경에서 프로세스 간 통신을 표준화한 방식 |
| [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) ([Non-Uniform Memory Access](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/)) | [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/) 확장의 타협안으로, 다중 컴퓨터와 경계를 비교할 때 중요 |
| 스케일아웃 ([Scale-out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)) | 노드 수를 늘려 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 용량을 확장하는 운영 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| [데이터 지역성](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/) ([Data Locality](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/)) | 계산을 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 있는 노드 근처에서 수행해 통신량을 줄이는 원리 |

### 📈 관련 키워드 및 발전 흐름도

```text
단일 프로세서
    │
    ▼
다중 프로세서 (Multiprocessor)
    │
    ├─ 공유 메모리 확장 한계
    ▼
다중 컴퓨터 (Multicomputer)
    │
    ├─ 메시지 패싱 (Message Passing)
    ├─ 클러스터 컴퓨팅 (Cluster Computing)
    ├─ 그리드 컴퓨팅 (Grid Computing)
    ▼
클라우드 · 빅데이터 · 분산 AI 학습
    │
    ▼
RDMA · CXL 기반 저지연 분산 자원 공유
```

이 흐름은 "단일 시스템 확장 → [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/) 한계 → [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 협력 → 소프트웨어 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) → 저지연 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)화"로 이어지는 진화 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 다중 컴퓨터는 친구들이 책상 하나를 같이 쓰는 대신, 각자 자기 책상에서 숙제를 하고 필요할 때만 쪽지를 주고받는 방식이에요.
2. 그래서 친구 수가 아주 많아져도 책상 때문에 싸우지 않고 일을 나눠 할 수 있어요.
3. 대신 쪽지를 너무 자주 보내면 시간이 오래 걸리니까, 각자 자기 몫을 오래 풀고 마지막에만 답을 합치는 게 중요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 377 / 803

← **이전**: [375. 다중 프로세서 (Multiprocessor)](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/375_multiprocessor/)
**다음**: [377. 공유 메모리 시스템 (Shared Memory)](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/377_shared_memory/) →

---
