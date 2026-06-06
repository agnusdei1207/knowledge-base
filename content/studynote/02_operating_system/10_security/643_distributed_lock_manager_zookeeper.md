---
title: "Chubby, ZooKeeper"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 단일 서버에서는 OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 Mutex나 Semaphore로 락([Lock](/studynote/05_database/04_transactions_concurrency/510_lock/))을 관리하지만, 물리적으로 떨어진 수백 대의 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 서버들이 하나의 자원(예: DB 테이블, 마스터 선출)을 두고 경쟁할 때는 <strong><a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 락 매니저 (<a href="/studynote/02_operating_system/01_overview_architecture/047_dlm/">DLM</a>: Distributed <a href="/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a> Manager)</strong>라는 합의된 제3의 통제소가 필요하다.
> 2. **메커니즘**: Google의 Chubby나 [Apache ZooKeeper](/studynote/14_data_engineering/01_infrastructure/029_apache_zookeeper/) 같은 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 코디네이터는 <strong>임시 노드(Ephemeral Node)</strong>와 **와치(Watch)** 매커니즘을 사용해 락을 구현한다. 누군가 락을 잡고 죽어버려도([세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 끊김) 임시 노드가 자동 삭제되어 데드락을 방지하고, 대기자들에게 즉시 알림을 쏴주어 [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)([Polling](/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/)) 오버헤드를 없앤다.
> 3. **가치**: [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락은 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/))와 클라우드 아키텍처에서 노드 간의 충돌([Race Condition](/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/))을 막고, 리더 선출(Leader Election)을 완벽하게 통제하여 '[스플릿 브레인](/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/)(Split-brain)' 대참사를 막는 가장 핵심적인 인프라 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 도구다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락(Distributed [Lock](/studynote/05_database/04_transactions_concurrency/510_lock/))은 여러 독립된 프로세스나 서버가 공유 자원([데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/), [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템, 특정 연산 등)에 순차적으로 접근해야 할 때, 네트워크를 통해 [상호 배제](/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/)([Mutual Exclusion](/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/))를 보장하는 기술이다. 이를 전문적으로 수행하는 시스템을 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 코디네이션 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(Distributed Coordination [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))라고 부른다.

- **필요성 (단일 락의 붕괴)**:
  - 과거에는 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 서버 1대에 모든 요청이 몰렸으므로, DB 자체의 Lock이나 OS의 Lock을 쓰면 됐다.
  - 하지만 서버가 100대로 늘어나고([Scale-out](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)), 이 100대가 똑같은 스토리지의 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 동시에 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(Write)를 시도한다면 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 1초 만에 박살난다. 100대의 서버 중 누군가는 락을 쥐고, 나머지는 대기해야 한다.
  - 만약 락을 쥐고 있는 1번 서버가 정전으로 죽어버리면? 남은 99대는 1번 서버가 락을 풀 때까지 영원히 기다리는 무한 데드락에 빠진다.
  - **해결책**: "살아있는 놈만 락을 가질 수 있고, 죽으면 락이 자동으로 풀리며, 락이 풀리는 순간 다음 대기자에게 즉시 알려주는" 똑똑한 글로벌 중앙 통제소([DLM](/studynote/02_operating_system/01_overview_architecture/047_dlm/))가 절실했다.

  - **로컬 락**: 한 가족이 화장실 문(공유 자원)을 잠그고 쓰는 것.
  - <strong><a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 락 (<a href="/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/">ZooKeeper</a>)</strong>: 전국 각지에 흩어진 100명의 직원이 하나의 금고를 열어야 한다. 직원들은 직접 금고로 가지 않고, 본사의 '열쇠 관리소([ZooKeeper](/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/))'에 전화를 건다. 관리소는 "가장 먼저 전화한 사람에게 임시 열쇠(Ephemeral Node)를 주고, 그 사람이 전화를 끊거나 연락이 두절되면(장애) 열쇠를 빼앗아 2번째 대기자에게 즉시 문자를 보내주는(Watch)" 완벽한 번호표 시스템을 운영한다.

- **발전 과정**:
  1. <strong><a href="/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> <a href="/studynote/02_operating_system/01_overview_architecture/047_dlm/">DLM</a></strong>: VMS 클러스터, [Oracle](/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) RAC 내부의 [DLM](/studynote/02_operating_system/01_overview_architecture/047_dlm/). 특정 솔루션에 종속되고 무거움.
  2. **Google Chubby (2006)**: Paxos 기반의 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템. GFS와 Bigtable의 마스터 선출을 위해 개발.
  3. <strong><a href="/studynote/14_data_engineering/01_infrastructure/029_apache_zookeeper/">Apache ZooKeeper</a></strong>: Chubby의 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [클론](/studynote/02_operating_system/02_process_thread/149_clone_system_call/). [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 생태계의 표준 코디네이터로 등극. (현재는 [etcd](/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/), Consul, [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) Redlock 등 다양화됨)

- **📢 섹션 요약 비유**: 수백 명의 요리사가 하나의 냄비(자원)에 재료를 넣으려 할 때, 주방장([DLM](/studynote/02_operating_system/01_overview_architecture/047_dlm/))이 호루라기를 불며 순서를 정해주고, 재료를 넣다 쓰러진 요리사는 즉시 밖으로 끌어내어 요리가 멈추지 않게 하는 식당의 지휘자입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [ZooKeeper](/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 기반 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락 구현 원리 (Znode)

ZooKeeper는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템과 비슷한 계층적 [디렉터리](/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 구조(`Znode`)를 메모리에 유지한다. 여기서 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락을 구현하는 데 핵심이 되는 두 가지 마법의 기능이 있다.

1. **Ephemeral Node (임시 노드)**: 클라이언트가 연결([세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/))되어 있는 동안만 존재하고, 클라이언트가 죽거나 네트워크가 끊기면 즉시 자동 삭제되는 노드. (데드락 방지)
2. **Sequence Node (순차 노드)**: 노드를 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)할 때 이름 뒤에 자동으로 1, 2, 3... 번호표를 붙여주는 기능. (순서 보장)
3. **Watch (감시/알림)**: 특정 노드의 변경([생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)/삭제)을 기다리고 있다가 이벤트가 발생하면 클라이언트에게 콜백(Callback)을 날려주는 기능. ([폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) 방지)

```text
  +-------------------------------------------------------------------+
  |                 ZooKeeper 분산 락 획득 및 해제 알고리즘 흐름               |
  +-------------------------------------------------------------------+
  |                                                                   |
  |  [상황 1: 3대의 서버가 동시에 Lock 요청]                                 |
  |  ZooKeeper 내부에 "/lock_path" 라는 디렉터리가 있음.                      |
  |                                                                   |
  |  1. Server A, B, C가 동시에 임시+순차 노드(Ephemeral Sequential) 생성 요청|
  |     Server A ---> 생성 성공: /lock_path/req-0000001 (가장 빠름)        |
  |     Server B ---> 생성 성공: /lock_path/req-0000002                  |
  |     Server C ---> 생성 성공: /lock_path/req-0000003                  |
  |                                                                   |
  |  [상황 2: Lock 획득 판단 (자기 순서 확인)]                               |
  |  2. 서버들은 "/lock_path"의 자식 노드 목록을 조회한다.                    |
  |     - Server A: "내가 제일 앞번호(001)네? 내가 락을 획득했다!" (작업 시작)   |
  |     - Server B: "나는 2등이네. 내 앞번호인 001번 노드에 Watch(감시)를 걸자."|
  |     - Server C: "나는 3등이네. 내 앞번호인 002번 노드에 Watch(감시)를 걸자."|
  |                                                                   |
  |  [상황 3: Lock 해제 (장애 또는 정상 종료)]                               |
  |  3. Server A가 작업을 마치고 연결을 끊거나, 장애로 죽어버림.                |
  |     ---> ZooKeeper는 즉시 임시 노드 "/lock_path/req-0000001" 을 삭제.  |
  |                                                                   |
  |  4. 001번 노드가 삭제되었으므로, 거기에 Watch를 걸어둔 Server B에게 즉시 알림!|
  |     - Server B: "오, 앞사람이 끝났네. 목록 다시 조회!"                    |
  |     - Server B: "이제 내가 1등(002)이다! Lock 획득!" (작업 시작)         |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 이 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 위대함은 <strong>'Herd Effect(소떼 현상)'를 완벽히 차단</strong>했다는 점이다. 만약 100대의 서버가 모두 1등(001번) 노드만 쳐다보고(Watch) 있었다면, 1번이 끝나는 순간 99대에게 동시에 알림이 날아가 [ZooKeeper](/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 서버가 터져버린다. 하지만 이 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)에서는 B는 A만 감시하고, C는 B만 감시하고, D는 C만 감시한다. 앞사람이 죽으면 딱 그다음 사람 한 명에게만 알림이 간다. 네트워크 오버헤드가 최소화되고 락이 아주 우아하게 다음 타자에게 넘어간다. 죽은 서버가 영원히 락을 쥐고 있는 데드락([Deadlock](/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)) 문제도 '임시 노드' 기능 덕분에 완벽히 해결된다.

---

### [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) 기반 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락 (Redlock [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))

무거운 [ZooKeeper](/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 대신 가벼운 인메모리 캐시인 Redis를 이용한 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락도 매우 널리 쓰인다.

1. **기본 원리 (SETNX)**: Redis의 `SET resource_name my_random_value NX PX 30000` 명령어를 사용한다. (NX: 없으면 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)해라 = [Lock](/studynote/05_database/04_transactions_concurrency/510_lock/) 획득 / PX 30000: 30초 뒤 자동 삭제 = [TTL](/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) 데드락 방지)
2. <strong>Redlock <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>: 단일 Redis는 장애 시 락 정보가 날아간다. [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 환경의 창시자 Salvatore Sanfilippo는 N개(보통 5개)의 독립된 [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) 마스터 노드에 동시에 SETNX를 쏘아, 과반수(Quorum, 3대) 이상에서 락 획득에 성공하면 진짜 락을 얻은 것으로 치는 **Redlock(레드락)** [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 제안했다.

- **📢 섹션 요약 비유**: [ZooKeeper](/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 락이 관공서에서 대기표를 뽑고 차례를 기다리는 '줄서기' 방식이라면, [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) Redlock은 5명의 문지기 중 3명 이상에게 먼저 뇌물(SETNX)을 먹이는 사람이 문을 여는 '다수결 선착순' 방식입니다.

---

## Ⅲ. 비교 및 연결

### [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락 기술 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 비교

| 비교 항목 | [ZooKeeper](/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) (ZAB) / [etcd](/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/) ([Raft](/studynote/05_database/04_transactions_concurrency/259_raft_paxos/)) | [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) (Redlock) | RDBMS (MySQL Named [Lock](/studynote/05_database/04_transactions_concurrency/510_lock/)) |
|:---|:---|:---|:---|
| <strong><a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a> (<a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">Consistency</a>)</strong> | <strong>Strong <a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">Consistency</a> (매우 높음)</strong> | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서 수학적 취약점 존재 | 높음 |
| **락 해제/알림 방식** | 임시 노드 + Watch (이벤트 푸시) | [TTL](/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) (만료 시간) + 주기적 [Polling](/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/) | [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 종료 / [Polling](/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/) |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> (속도)</strong> | 다소 무거움 (디스크 [영속성](/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/) 동반) | **매우 빠름 (순수 메모리 연산)** | 느림 |
| **데드락 방지** | [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 타임아웃으로 즉각 해제 | [TTL](/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) 만료로 해제 (만료 전 작업 시 위험) | [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)/커넥션 종료 시 해제 |
| **주 사용처** | K8s([etcd](/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/)), [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 리더 선출 | 짧고 빠른 [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 캐시 락 | 기존 RDBMS 인프라 재활용 |

### 과목 융합 관점

- <strong><a href="/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a> (OS)</strong>: 로컬 OS의 [스핀락](/studynote/02_operating_system/04_synchronization/222_spinlock/)([Spinlock](/studynote/02_operating_system/04_synchronization/222_spinlock/))이 "CPU 코어를 태우며 무한 대기"하는 구조라면, ZooKeeper의 Watch는 OS의 블로킹(Sleep)과 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)(Wake-up) 메커니즘을 네트워크 스케일로 확장한 것과 정확히 일치한다.
- <strong><a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a> (<a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">Algorithm</a>)</strong>: ZooKeeper나 [etcd](/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/) 내부에서 락 정보를 여러 노드에 동일하게 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)([Replication](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/))하기 위해 사용하는 <strong>Paxos, ZAB(<a href="/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/">ZooKeeper</a> Atomic Broadcast), <a href="/studynote/05_database/04_transactions_concurrency/259_raft_paxos/">Raft</a></strong> [합의 알고리즘](/studynote/06_ict_convergence/01_blockchain/011_consensus_algorithm/)은 네트워크 단절(Network [Partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)) 상황에서도 [스플릿 브레인](/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/)(Split-brain)을 막아내는 컴퓨터 과학의 정수다.

- **📢 섹션 요약 비유**: 빠르고 가벼운 티켓이 필요하면 Redis를 쓰고, 돈이 오가는 절대 틀려선 안 되는 금고 열쇠가 필요하면 조금 무겁지만 절대 안전한 ZooKeeper나 etcd를 쓰는 것이 아키텍처의 정석입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/">마이크로서비스</a>(<a href="/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a>) 선착순 쿠폰 발급 시스템</strong>: 1,000장의 쿠폰을 발급하는데, 10대의 Spring Boot 서버([컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/))로 10만 명의 트래픽이 쏟아진다. [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락이 없으면 쿠폰 잔여 수량을 읽고(Read) 빼는(Update) 사이 [경쟁 조건](/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/)([Race Condition](/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/))이 터져 쿠폰이 1,500장 발급될 수 있다.
   - <strong>아키텍처 적용 (<a href="/studynote/05_database/04_transactions_concurrency/542_redis/">Redis</a> Redisson)</strong>: 빠른 응답 속도가 생명이다. ZooKeeper보다 가벼운 [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) 기반의 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락 라이브러리인 자바의 <strong>Redisson</strong>을 사용한다.
   - 10대의 서버가 쿠폰 발급 로직을 실행하기 전 `RLock lock = redisson.getLock("coupon_1"); lock.tryLock();`을 호출한다.
   - Redisson 내부는 Pub/Sub 구조로 되어 있어, 락을 못 얻은 서버가 미친 듯이 Redis를 때리는([Busy Waiting](/studynote/02_operating_system/04_synchronization/227_busy_waiting/)) 현상 없이 얌전히 대기하다가 이벤트 알림을 받고 처리하므로 [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) 부하 없이 초당 수만 건의 락을 완벽히 소화한다.

2. **시나리오 — 클라우드 스케줄러의 이중 실행 방지 (Leader Election)**: 자정에 100만 건의 배치(Batch) 메일을 발송하는 서버가 있다. [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 위해 서버를 2대 띄웠는데, [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락이 없으면 두 서버가 동시에 크론([Cron](/studynote/15_devops_sre/02_cicd_gitops/107_nightly_build_scheduled_cron_pipeline/))을 돌려 고객에게 메일이 2번씩 발송되는 대참사가 발생한다.
   - <strong>대응 (<a href="/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/">ZooKeeper</a> Leader Election)</strong>: 2대의 서버가 켜지자마자 ZooKeeper에 `/batch_master`라는 임시 순차 노드를 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한다. 번호표 1번을 부여받은 서버가 "[Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)(리더)"가 되어 배치 작업을 수행하고, 2번 서버는 "Standby(대기)" 상태로 돌입한다. 만약 1번 서버가 죽으면 임시 노드가 사라지고, Watch 알림을 받은 2번 서버가 즉시 1등이 되어 배치를 이어받는다. 완벽한 [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)-Standby 고가용성 클러스터가 구축된다.

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 분산 락 (Distributed Lock) 도입 및 솔루션 선정 플로우      |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [분산 서버 간의 자원 동시 접근 및 데이터 정합성 문제 발생]               |
  |                |                                                  |
  |                v                                                  |
  |      요청의 빈도가 초당 수백/수천 건 이상으로 매우 높고 속도가 생명인가?    |
  |          +- 예 (선착순 이벤트 등) ---> [Redis 분산 락 (Redisson 등) 도입]|
  |          |                        (단, Redlock 알고리즘의 한계로 극히   |
  |          |                         낮은 확률의 락 붕괴는 감수해야 함)   |
  |          +- 아니오                                                |
  |                |                                                  |
  |                v                                                  |
  |      절대로 락이 두 명에게 부여되면 안 되는 절대적 무결성(Master 선출)인가? |
  |          +- 예 (결제 처리, 리더 선출) ---> [ZooKeeper / etcd (CP 시스템)] |
  |          |                            (Raft 합의 알고리즘 기반 강력 보장) |
  |          |                                                        |
  |          +- 아니오 ---> 기존 DB의 Named Lock이나 JPA 낙관적 락으로 대체  |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** "모든 곳에 ZooKeeper를 쓰면 되지 않나?"는 틀린 접근이다. [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락을 거는 행위 자체가 네트워크 I/O를 발생시키기 때문에 시스템의 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))을 박살낸다. 가장 좋은 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락은 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락을 아예 안 쓰는 아키텍처(요청을 [카프카](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 큐에 줄 세워 단일 컨슈머가 처리하게 함)를 만드는 것이다. 불가피하게 써야 한다면 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)([Redis](/studynote/05_database/04_transactions_concurrency/542_redis/))과 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)([Zookeeper](/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/)) 사이의 트레이드오프를 철저히 계산해야 한다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong>락 <a href="/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/">TTL</a>(Time-To-Live) 갱신 (Watchdog)</strong>: 서버 A가 [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) 락을 10초 잡고 작업을 하는데 풀 풀스캔이 15초 걸렸다. 10초 뒤 락이 풀려버리고 서버 B가 들어와서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 꼬인다. 작업이 길어질 때 백그라운드 스레드가 락의 TTL을 지속적으로 연장해 주는 <strong>Watchdog 메커니즘</strong>이 적용되었는가?
- <strong><a href="/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/">스플릿 브레인</a> 방어 (Fencing Token)</strong>: [가비지 컬렉션](/studynote/02_operating_system/06_memory_management/380_garbage_collection/)(GC Pause)으로 인해 서버 A가 5초간 멈췄다 깨어났다. 그 사이 ZooKeeper는 A가 죽은 줄 알고 B에게 락을 줬다. A가 깨어나 자기가 아직 락을 쥔 줄 알고 DB에 쓴다. 이를 막기 위해 락을 줄 때마다 증가하는 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 번호(Fencing Token)를 DB에 같이 넘겨, 구버전의 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 튕겨내는 방어 로직이 있는가? ([분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락의 핵심 면접 질문)

- **📢 섹션 요약 비유**: [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락은 '운전대'입니다. 운전대(락)를 넘겨받은 줄 알고 눈을 감고 달리면 사고(GC Pause 문제)가 납니다. 운전대를 잡았더라도 페달을 밟기 전(DB [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))에 지금 내 운전대가 진짜인지(Fencing Token) 한 번 더 확인하는 이중 안전장치가 필수입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락 미적용 환경 | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락 ([ZooKeeper](/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/)/[Redis](/studynote/05_database/04_transactions_concurrency/542_redis/)) 적용 | 개선 효과 |
|:---|:---|:---|:---|
| <strong>정성 (<a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 정합성)</strong>| 동시 접속 시 쿠폰 초과 발급, 계좌 마이너스 | [경쟁 조건](/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/)([Race Condition](/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/)) 완벽 차단 | 비즈니스 크리티컬 로직의 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 보장 |
| <strong>정량 (<a href="/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a>)</strong> | 배치 서버 1대 죽으면 수동 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)(수십 분) | 리더 선출을 통한 즉각 [Failover](/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/) (수 초) | 무중단 자동화 클러스터 구축 |
| **정성 (자원 효율)** | 동시 실행(중복 실행)으로 인한 리소스 낭비 | [상호 배제](/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/)를 통해 단 1회의 실행 보장 | 데드락 없는 안전한 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 제어 |

### 미래 전망
- <strong>etcd의 <a href="/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/">클라우드 네이티브</a> 표준화</strong>: 과거 [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 시대의 제왕이었던 [ZooKeeper](/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) (Java 기반, 무거움)는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)(K8s)의 등장과 함께 Go 언어로 작성된 가볍고 빠른 <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/">etcd</a></strong>로 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 코디네이터의 왕좌가 넘어가고 있다. K8s의 모든 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 상태 관리와 락은 etcd의 [Raft](/studynote/05_database/04_transactions_concurrency/259_raft_paxos/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 기반으로 돌아간다.
- <strong><a href="/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> 자체 내장 <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 락</strong>: [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락 매니저를 따로 띄우는 관리 오버헤드를 줄이기 위해, CockroachDB나 [TiDB](/studynote/05_database/05_distributed_nosql_newsql/293_elt_process/) 같은 차세대 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) DB들이 아예 내부 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 엔진에 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락킹 메커니즘을 내장하여 개발자가 신경 쓸 필요 없는 방향으로 진화 중이다.

### 결론
[분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락 매니저([DLM](/studynote/02_operating_system/01_overview_architecture/047_dlm/))의 구현은 멀티코어 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 [스핀락](/studynote/02_operating_system/04_synchronization/222_spinlock/)/뮤텍스 개념을 네트워크 위로 확장한 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 공학의 걸작이다. 임시 노드(Ephemeral), 콜백(Watch), [합의 알고리즘](/studynote/06_ict_convergence/01_blockchain/011_consensus_algorithm/)(Paxos/[Raft](/studynote/05_database/04_transactions_concurrency/259_raft_paxos/))의 우아한 결합은 "서버는 언제든 죽을 수 있고, 네트워크는 언제든 끊길 수 있다"는 최악의 가정을 전제로 설계되었다. 현대 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)를 다루는 엔지니어에게 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락의 한계(GC Pause, [Clock Skew](/studynote/05_database/06_dw_olap_trends/388_spanner_truetime_clock_skew/))를 이해하고 Fencing Token과 같은 방어 수단을 엮어내는 것은 시스템의 대형 사고를 막는 가장 결정적인 역량이다.

- **📢 섹션 요약 비유**: 오케스트라([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/)) 단원들이 서로 악보(DB)를 뺏으려 싸우지 않게, 절대 고장 나지 않는 지휘봉([분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 락)을 세워 완벽한 연주 순서를 지켜내는 현대 클라우드의 지휘자입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) OS 투명성 (Transparency: 위치, 마이그레이션, [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), 병행 투명성 보장 구조) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 람포트 논리적 시계 (Lamport's Logical Clocks) [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 환경 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 정렬 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 자원 제약 ([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) / [Container](/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/) 자원 오버커밋 킬링 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 동적 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 서명 ([Module Signature Verification](/studynote/02_operating_system/10_security/645_kernel_module_signature_verification/)) [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 통제 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[람포트 논리적 시계 (Lamport's Logical Clocks) 분산 환경 동기화 정렬]
    |
    v
[분산 락 매니저 구현 (Chubby, ZooKeeper 등 분산 코디네이션 락 알고리즘)]
    |
    +---> [마이크로서비스 커널 자원 제약 (Pod / Container 자원 오버커밋 킬링 정책)]
    +---> [커널 동적 모듈 서명 (Module Signature Verification) 무결성 통제]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 전국에 있는 100명의 친구들이 하나의 곰 인형(공유 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 가지고 놀고 싶어 해요. 한 번에 여러 명이 인형을 잡으면 찢어지겠죠?
2. 그래서 '동물원 관리자([ZooKeeper](/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/))'를 두었어요. 관리자에게 먼저 전화한 사람에게 임시 번호표(락)를 주고 인형을 줍니다.
3. 인형을 가지고 놀던 친구가 잠들거나 전화를 끊으면(장애), 관리자는 즉시 인형을 뺏어서 다음 번호표를 가진 친구에게 문자를 보내(Watch) 차례를 알려줘요. 그래서 인형이 절대 찢어지지 않는답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 643 / 800

<- **이전**: [642. 람포트 논리적 시계 (Lamport's Logical Clocks) 분산 환경 동기화 정렬](/studynote/02_operating_system/10_security/642_lamport_logical_clocks/)
**다음**: [644. 마이크로서비스 커널 자원 제약 (Pod / Container 자원 오버커밋 킬링 정책)](/studynote/02_operating_system/10_security/644_microservice_resource_limits_cgroups/) ->

---
