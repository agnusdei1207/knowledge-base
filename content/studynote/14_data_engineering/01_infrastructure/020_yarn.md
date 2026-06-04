+++
title = "20. YARN (Yet Another Resource Negotiator) - 하둡 2.0 클러스터 자원(CPU/Mem) 스케줄링 통합 관리자"
description = "하둡 2.0 클러스터의 두뇌로, 자원(CPU/Memory) 관리와 애플리케이션 스케줄링을 완벽히 분리해낸 중앙 통합 리소스 관리자"
date = 2025-01-01

[taxonomies]
tags = ["data_engineering"]

[extra]
tags = ["data_engineering"]
+++

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 1.0의 단일 [맵리듀스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)([MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)) 전용 엔진 한계를 타파하기 위해 등장한 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 2.0의 심장으로, 클러스터 전체의 자원(CPU, 메모리) 할당 기능과 애플리케이션 실행/모니터링 기능을 완전히 분리한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)급 리소스 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)입니다.
> 2. **가치**: 하나의 거대한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클러스터 위에서 [맵리듀스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)뿐만 아니라 [아파치 스파크](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/)(Spark), 플링크(Flink), 실시간 스트리밍 등 다양한 연산 엔진들이 서로 자원을 뺏기지 않고 평화롭게 공존하며 동시에 구동할 수 있는 [멀티테넌트](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/310_multi_tenant_database_architecture/)([Multi-tenant](/knowledge-base/studynote/03_network/17_sdn_nfv/888_multi_tenant_cloud_resource_isolation_noisy_neighbor/)) 환경을 구축했습니다.
> 3. **융합**: [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)([Container](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/)) 기반의 격리 사상을 채택하여 현대의 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)([Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)) [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)과 기술적 철학을 공유하며, [데이터 지역성](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/)([Data Locality](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/))을 고려한 정교한 자원 분배 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)의 코어 엔진 역할을 수행합니다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

과거 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 1.0 시대, [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)은 오직 '[맵리듀스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)([MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/))'라는 단일 배치 작업만을 위해 돌아가는 폐쇄적인 시스템(JobTracker 기반)이었습니다. 이 구조의 치명적 한계는 중앙의 JobTracker가 4,000대 노드의 자원 [상태도](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/065_state_diagram/) 확인하고, 각 작업이 잘 도는지 모니터링도 하며, 장애 복구까지 혼자 다 처리해야 한다는 점이었습니다. 결과적으로 클러스터가 커지면 중앙의 JobTracker가 과부하로 폭발(병목)해버려 [스케일 아웃](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)이 불가능해졌고, 무엇보다 스파크나 [그래프 분석](/knowledge-base/studynote/16_bigdata/05_analysis/114_graph_analytics/) 같은 새로운 연산 엔진을 올릴 수가 없었습니다.

이 병목을 해소하고 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)을 진정한 '[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 센터의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)'로 탈바꿈시킨 혁명이 바로 <strong>YARN(Yet Another Resource Negotiator)</strong>의 등장입니다. 야후(Yahoo!) 주도로 개발된 YARN은 극단적인 역할 분리 철학을 가져왔습니다. "중앙 관제탑은 오직 전체 자원(RAM/CPU) 분배만 신경 쓰고(ResourceManager), 개별 애플리케이션의 실행과 장애 감시는 각 작업을 대표하는 현장 소장(ApplicationMaster)을 노드에 띄워서 위임하자!"

이 아키텍처 혁신 덕분에 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 클러스터는 특정 프레임워크에 종속되지 않는 범용 자원 플랫폼이 되었습니다. 오늘날 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어들이 동일한 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 장비 위에서 낮에는 실시간 스트림([Spark Streaming](/knowledge-base/studynote/16_bigdata/03_spark/060_spark_streaming_dstream/))을 띄우고, 밤에는 무거운 배치([MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/)/[Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/))를 돌려 인프라 활용률을 100%로 쥐어짤 수 있게 된 것은 순전히 YARN 덕분입니다.

이 도식은 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 1.0의 병목 구조가 YARN의 위임형 아키텍처로 진화하며 얻은 확장의 자유를 시각화한 것입니다.
```text
[과거: 하둡 1.0 (JobTracker 중앙 독재 병목)]
                ┌─> Task (Map)
 [JobTracker] ──┼─> Task (Reduce)   ==> 수만 개의 태스크를 혼자 감시하다가
 (자원+스케줄링)  └─> Task (Map)         메모리 터지고 병목 발생! 💥

[혁신: 하둡 2.0 YARN (권한 위임 분산 구조)]
 [ResourceManager] (중앙: 난 전체 CPU/RAM 양만 관리할게. 태스크 감시는 안해!)
         │
         ├──(자원 협상)──> [ApplicationMaster A (스파크 전담 현장 소장)] ---> Worker 제어
         └──(자원 협상)──> [ApplicationMaster B (Hive 전담 현장 소장)]  ---> Worker 제어
```
이 흐름의 핵심은 '권한의 하방 위임'입니다. 수만 개의 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) 상태 추적이라는 엄청난 오버헤드를 중앙 마스터에서 떼어내어, 클러스터의 임의 노드에 동적으로 뜨는 `ApplicationMaster`들에게 떠넘겼습니다. 따라서 YARN 클러스터는 노드가 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000대를 넘어가도 중앙 마스터가 터지지 않는 진정한 무한 확장의 지위를 얻어냈습니다. 실무에서는 이 구조 변화 덕분에 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/)([Out of Memory](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/))으로 클러스터 전체가 뻗는 대재앙이 사라졌습니다.

📢 **섹션 요약 비유**: 회장님(JobTracker)이 전 직원의 책상 배정과 개별 업무 실적까지 혼자 감시하다가 과로사하는 회사에서, 회장님(ResourceManager)은 각 부서에 예산만 던져주고 실제 팀원 관리와 프로젝트 책임은 각 팀장(ApplicationMaster)이 현장에서 전담하는 체계적 대기업으로 승격한 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

YARN은 철저하게 마스터-슬레이브(Master-Slave) 구조 위에서 동적인 '[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)([Container](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/))' 단위로 자원을 격리하고 할당합니다.

| 구성 요소 | 역할 | 내부 동작 | [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | 비유 |
|:---|:---|:---|:---|:---|
| <strong>ResourceManager (<a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/197_rm_rate_monotonic_scheduling/">RM</a>)</strong> | 글로벌 자원 스케줄링 (Master) | 클러스터 전체의 가용 CPU/RAM을 파악하고 페어(Fair), 캐파시티(Capacity) 큐에 따라 자원을 분배합니다. | [RPC](/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/) / Scheduler | 중앙 예산 부처 |
| **NodeManager (NM)** | 로컬 노드 자원 관리 (Worker) | 각 서버 1대마다 떠서, 실제 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 띄우고 메모리/CPU 사용량을 감시하며 RM에게 보고합니다. | Hearbeat 통신 | 각 건물 관리인 |
| **ApplicationMaster (AM)** | 앱 생명주기 관리 (App 단위) | 작업이 제출되면 1개씩 생성되며, RM에게 필요한 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)(자원)를 구걸(협상)하고 장애 복구를 책임집니다. | [RPC](/knowledge-base/studynote/02_operating_system/02_process_thread/126_rpc/) Negotiation | 프로젝트 외주 팀장 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/">Container</a></strong> | 논리적 자원 격리 단위 | 'RAM 2GB, CPU 1코어' 형태로 격리된 실행 공간. 이 안에서 Spark Executor나 Map [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)가 돕니다. | [cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) / JVM | 임대 사무실 |

이 다이어그램은 사용자가 스파크(Spark) 잡을 YARN에 제출했을 때 벌어지는 아키텍처 내부의 5단계 동적 [자원 할당](/knowledge-base/studynote/02_operating_system/01_overview_architecture/041_resource_allocation/) 시퀀스를 보여줍니다.
```text
┌──────────────── YARN Application Execution Flow ────────────────┐
│                                                                 │
│ [Client] ──1. Job 제출 (Spark 앱)──> [ResourceManager]              │
│                                       (전체 큐/자원 확인)             │
│                                            │                    │
│                    2. 첫 컨테이너 띄워라 명령 │                    │
│                                            ▼                    │
│ [NodeManager 1] <────────────────── [ApplicationMaster 생성]       │
│                                            │ (스파크 잡의 대장)      │
│     ▲                   3. 나 컨테이너 100개 필요해! 자원 협상 요청 │
│     │                           (Resource Negotiation)          │
│     │ 5. Task 실행 명령                        ▼                    │
│ [NodeManager 2~N] <──4. 컨테이너 할당 티켓 발급── [ResourceManager] │
│      │                                                          │
│  [Container] ─ (그 안에서 Spark Executor가 메모리를 잡고 연산 시작)  │
└─────────────────────────────────────────────────────────────────┘
```
이 도식에서 가장 놀라운 점은 ApplicationMaster(AM)의 존재 방식입니다. AM은 고정된 마스터 서버에 뜨지 않고, 워커 노드(NodeManager) 중 자원이 남는 아무 곳의 첫 번째 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 안에서 동적으로 스폰(Spawn)됩니다. 만약 AM이 띄워진 노드의 하드웨어가 죽어버리면, RM은 이를 감지하고 다른 노드에 새 AM을 띄워 처음부터 다시 복구시킵니다. 따라서 이 배치는 특정 마스터 노드의 [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)([단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)) 한계를 극복하고, 클러스터 자원을 극도로 탄력적으로 유동화하는 결과를 낳습니다.

**심층 동작 원리**
1. <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/">스케줄러</a> 큐 (Queues)</strong>: [RM](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/197_rm_rate_monotonic_scheduling/) 내부에는 트리 구조의 큐(예: root.marketing, root.data_science)가 존재하며, 부서별로 가용할 수 있는 최대 RAM/CPU 파이가 엄격히 통제됩니다.
2. **자원 협상 (Negotiation)**: AM은 RM에게 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 있는 IP 192.168.1.10에 4GB짜리 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 달라([데이터 지역성](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/) 요구)"고 구체적으로 요청합니다.
3. <strong><a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a> 스케줄링 (Delay Scheduling)</strong>: RM은 해당 노드에 4GB가 당장 없으면 즉시 다른 노드를 주지 않고, 지역성을 살리기 위해 수 초간 기다려주는 유연성을 발휘합니다.
4. **선점 (Preemption)**: 특정 부서가 자원을 초과 점유하고 있고 급한 VIP 큐가 굶고 있다면, [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)는 실행 중인 남의 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 강제로 죽여(Kill) 자원을 뺏어버립니다.

📢 **섹션 요약 비유**: 거대한 뷔페 식당(클러스터)에서 매니저([RM](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/197_rm_rate_monotonic_scheduling/))는 테이블(자원) 빈자리만 안내해 주고 맙니다. 각 테이블에 앉은 손님 대표(AM)가 알아서 자기 일행들에게 고기를 가져다 먹일지 스파게티를 먹일지([태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) 실행) 지휘하며 질서를 유지하는 자동화 시스템입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

현대 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어링 생태계에서 YARN의 라이벌이자 진화 방향인 [컨테이너 오케스트레이션](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 도구 <strong><a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/">쿠버네티스</a>(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/">Kubernetes</a>, K8s)</strong>와의 아키텍처 비교는 가장 중요한 아키텍처 의사결정 지점입니다.

| 항목 | YARN ([Hadoop Ecosystem](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/211_hadoop_ecosystem_mapreduce/)) | [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) ([Cloud Native](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/)) | 실무 판단 포인트 |
|:---|:---|:---|:---|
| **설계 목적** | 대규모 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 프로세싱(Batch/<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a>)</strong> 전용 | [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)([MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/)) 및 <strong>무상태 웹 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a></strong> 범용 | 워크로드의 근본적 성격 |
| **격리 기술** | JVM 프로세스 위주, [cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) (비교적 약한 격리) | [Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/), [Namespaces](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/700_nvme_namespaces/) (강력한 OS 레벨 격리) | 환경/[라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 충돌 여부 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/">데이터 지역성</a></strong> | HDFS와 완벽히 통합되어 **최우선 보장** 연산 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 위치 개념 약함 ([CSI](/knowledge-base/studynote/12_it_management/02_itsm_itil/068_csi/) 등 외부 연결 의존) | 대용량 I/O 속도 방어의 필수성 |
| **장기 실행(Long-running)**| 비교적 취약, 배치 잡 중심 스케줄링 | 자가 치유([ReplicaSet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/086_replicaset_kubernetes_controller_self_healing/)) 기반 365일 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 최적 | 웹 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 서버 vs [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 잡 |

이 비교 매트릭스는 온프레미스의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 왕자(YARN)와 클라우드의 제왕(K8s) 간의 워크로드 차이를 보여주는 대조 매트릭스입니다.
```text
+-- 자원 스케줄링 패러다임 차이 --+

[YARN 강점: Batch Data Processing]
"이 스파크 잡은 데이터가 노드 A에 있으니 무조건 노드 A 근처에 띄워!"
=> I/O 속도 극대화에 목숨 욺 (Data Locality 사수)

[Kubernetes 강점: Microservices]
"웹 서버 파드 3개가 죽었네? 클러스터 안 아무 노드에나 빨리 띄워 복구해!"
=> 무중단 서비스와 빠른 복원력에 목숨 욺 (빠른 재배치 사수)
+---------------------------------+
```
A 방식(YARN)은 철저히 '[하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/)'라는 스토리지 구조와 피가 섞여 있어, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 있는 곳으로 연산을 밀어 넣는 데 미친 성능을 보여줍니다. 반면 B 방식(K8s)은 개발자가 파이썬, 고(Go), 노드(Node) 등 어떤 언어로 짠 환경이든 [도커](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) 이미지로 말아 올리기만 하면 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 충돌 없이 깔끔하게 격리해 돌려주는 이식성이 뛰어납니다. 실무에서는 스파크(Spark) 잡을 돌릴 때 레거시 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 클러스터가 있다면 YARN을 쓰고, 클라우드 네이티브로 신규 구축한다면 [데이터 지역성](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/) 손실을 캐시로 메꾸면서 Spark on K8s 아키텍처로 넘어가고 있는 거대한 과도기적 융합 국면에 있습니다.

📢 **섹션 요약 비유**: YARN이 중장비를 동원해 거대한 광산([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 순식간에 캐고 철수하는 데 특화된 야전 공병대라면, [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)는 다양한 상점([마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/))들이 폐업해도 즉시 새 상점을 열어 1년 내내 불이 꺼지지 않게 관리하는 거대한 쇼핑몰 관리단과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

현장의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어에게 YARN 튜닝은 "큐([Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/)) 설계와 메모리 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 방어"라는 두 가지 전쟁으로 요약됩니다.

**실무 의사결정 및 자원 설계 시나리오**
1. <strong>부서 간 자원 경합 (<a href="/knowledge-base/studynote/03_network/17_sdn_nfv/888_multi_tenant_cloud_resource_isolation_noisy_neighbor/">Multi-tenant</a>) 문제</strong>
   - **현상**: 마케팅 팀이 제출한 엄청난 스파크 배치 잡이 클러스터의 CPU 100%를 독식하여, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 사이언티스트들의 주피터 노트북 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)가 3시간째 대기(Pending) 상태에 빠집니다.
   - **판단**: YARN의 `Capacity Scheduler`를 도입하여 큐를 찢습니다. 마케팅 큐(Max 70%), 사이언스 큐(Min 30%)로 보장(Guarantee) 자원을 설정하고, 선점(Preemption) 기능을 켜서 마케팅이 선넘게 자원을 먹고 있으면 YARN이 마케팅 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 Kill하여 사이언스 팀에게 자원을 강제 반환하도록 설계합니다.
2. <strong>스파크 Executor <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a> (메모리 초과 사망) 방어</strong>
   - **상황**: YARN이 스파크 워커에게 4GB [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 줬는데, 스파크 잡이 내부적으로 파이썬(PySpark) 프로세스를 띄우며 오프힙(Off-heap) 메모리를 과다 사용해 4.5GB를 씁니다.
   - **판단**: YARN NodeManager는 즉시 "물리 메모리 제한 초과(Physical memory limits exceeded)" 에러를 뱉으며 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 무자비하게 암살(Kill)합니다. 엔지니어는 `spark.yarn.executor.memoryOverhead` 파라미터를 넉넉히(기본 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)% -> 20%) 튜닝하여 YARN에게 처음부터 더 큰 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 요구하도록 타협안을 마련해야 합니다.

<strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a> (치명적 <a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/">결함</a> 사례)</strong>
- **단일 Default 큐 방치**: 클러스터를 구축하고 수백 명이 쓰는데 YARN 큐를 하나(default)로만 두면, 나쁜 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 하나를 던진 주니어 개발자가 전사의 빅데이터 인프라를 다운시킬 수 있습니다. 반드시 용도/부서별로 자원을 격리(Quotas)해야 합니다.

이 흐름도는 실무에서 클러스터 자원 고갈 시 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 개입하는 선점(Preemption) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 플로우를 보여줍니다.
```text
[상황: VIP 부서(A큐)가 급하게 스파크 잡 제출] -> 클러스터 자원 0% 남음
       │
       ├─ RM 스케줄러: "A큐의 최소 보장 자원이 지켜지지 않고 있다!" 판단
       │
       ├─ (희생양 탐색) 현재 할당량을 초과해서 막 쓰고 있는 B부서 컨테이너 색출
       │
       ├─ (경고 1차) B부서의 ApplicationMaster에게 "15초 안에 자원 반납해" 시그널 전송
       │
       └─ (강제 킬) 안 뱉으면 NodeManager에게 OS kill(-9) 명령 하달 -> 자원 회수
                 │
                 └──> 회수한 자원을 VIP A큐에 즉시 할당하여 서비스 지연 방지
```
이 흐름의 핵심은 제한된 자원 하에서 '공평함(Fairness)'을 수리적으로 강제한다는 점입니다. 이 선점 기능이 없으면 무거운 배치 잡 하나가 끝날 때까지 전체 클러스터가 먹통이 되는 데드락([Deadlock](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/))에 빠집니다. 따라서 실무 관리자는 큐의 깊이(Depth)와 우선순위 가중치를 어떻게 세팅하느냐에 따라 클러스터의 투자 대비 효용([ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/))을 2배 이상 끌어올릴 수 있습니다.

📢 **섹션 요약 비유**: 왕복 2차선 도로(자원)에서 평소에는 화물차(마케팅 배치)가 2차선을 다 막고 달려도 놔두지만, 구급차(VIP 사이언스 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/))가 등장하면 사이렌(Preemption)을 울려 화물차를 갓길로 쫓아내고 길을 터주는 스마트 교통 통제 시스템입니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

YARN의 도입은 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)을 단순한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장고에서 거대한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 애플리케이션 플랫폼([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Operating System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))으로 격상시킨 위대한 아키텍처 리팩토링입니다.

| 정성적 효과 | 정량적 지표 및 변화 |
|:---|:---|
| **클러스터 활용률 극대화** | 주야간 워크로드 혼합 배치로 서버 유휴 시간 [제로화](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/784_zeroization_circuit/) ([ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/) 2배 상승) |
| **다양한 연산 엔진 생태계 폭발** | Spark, Tez, Flink, Storm 등이 단일 [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 위에서 동시 공존 실행 가능 |
| <strong>무한한 <a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/">스케일 아웃</a> 확보</strong> | JobTracker의 단일 병목 소멸로 노드 한계가 4,000대에서 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000대 이상으로 돌파 |

미래의 자원 관리 표준은 점차 YARN에서 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)([Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/))로 헤게모니가 넘어가고 있습니다. 더 가볍고, 클라우드 네이티브하며, 딥러닝([GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)) 자원 격리까지 완벽하게 지원하기 때문입니다. 하지만 YARN이 정립한 '[자원 할당](/knowledge-base/studynote/02_operating_system/01_overview_architecture/041_resource_allocation/)과 애플리케이션 수명주기 관리의 분리', '계층적 큐([Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/))를 통한 부서별 자원 보장'이라는 철학은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅의 바이블로 남아 모든 현대적 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)의 뼛속에 스며들어 있습니다. YARN의 스케줄링 메커니즘을 튜닝해 본 경험은 클라우드 시대 비용 최적화([FinOps](/knowledge-base/studynote/12_it_management/05_security_compliance/344_finops/)) 엔지니어링의 가장 든든한 밑거름이 될 것입니다.

📢 **섹션 요약 비유**: YARN은 무질서하게 난개발되던 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 도시에 훌륭한 신도시 구획(격리)을 짜고 도로망(자원 분배)을 깔아, 수십 개의 다국적 기업(스파크, 하이브)이 한 도시 안에서 싸우지 않고 평화롭게 장사할 수 있게 만든 위대한 도시 계획가입니다.

---
### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
* ApplicationMaster (각 스파크 잡마다 1개씩 떠서 현장에서 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 구걸하고 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)를 책임지는 핵심 위임자)
* [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) (YARN이라는 자원 풀 위에서 동작함으로써 [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 생태계의 디스크 I/O를 대체하며 왕좌에 오른 인메모리 엔진)
* Capacity Scheduler / Fair Scheduler (YARN이 다수 사용자의 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 교통 정리하고 자원을 쪼개주는 트리 구조의 큐 스케줄링 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))
* Preemption (선점, 자원이 부족할 때 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 남의 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 강제로 죽여 우선순위가 높은 큐에 바치는 생존 메커니즘)
* [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) ([컨테이너 오케스트레이션](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)의 클라우드 대세로, YARN의 빅데이터 자원 관리 왕좌를 위협하는 현대적 아키텍처)

### 📈 관련 키워드 및 발전 흐름도

```text
[MapReduce v1 (MRv1) — JobTracker 단일 장애점, 자원 관리·실행 혼재]
    │
    ▼
[YARN (Yet Another Resource Negotiator) — ResourceManager·NodeManager 분리]
    │
    ▼
[ApplicationMaster — 각 잡(Job)별 독립 실행 조율자, 컨테이너 요청/관리]
    │
    ▼
[Capacity / Fair Scheduler — 다중 테넌트 자원 큐 관리]
    │
    ▼
[Apache Spark on YARN — 인메모리 엔진이 YARN 자원 풀 위에서 MR 대체]
```
MRv1의 [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)과 자원 비효율을 YARN이 역할 분리로 해결했으며, ApplicationMaster 모델로 Spark 등 다양한 프레임워크를 통합하는 범용 클러스터 OS로 진화했다.

### 👶 어린이를 위한 3줄 비유 설명
1. 학교 운동장에 장난감 수만 개(자원)가 있는데, 예전엔 교장 선생님 혼자서 1,000명의 아이들에게 일일이 장난감을 나눠주다 쓰러졌어요!
2. 그래서 새로 온 똑똑한 선생님(YARN)은 각 반 반장(ApplicationMaster)들에게 "너희 반에 필요한 장난감 개수만 나한테 말해!"라고 규칙을 바꿨어요.
3. 그러면 선생님은 전체 수량만 확인하고 반장에게 박스째로 넘겨주고, 진짜로 누가 무슨 장난감을 갖고 놀지(작업 실행)는 반장이 알아서 관리하니까 학교가 엄청나게 평화롭고 빠르게 돌아가게 된 거랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 20 / 258

← **이전**: [19. 데이터 지역성 (Data Locality) - 연산 코드를 데이터가 이미 존재하는 노드로 전송하여 네트워크 전송 오버헤드 최소화](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/)
**다음**: [21. 아파치 스파크 (Apache Spark) - 하둡 맵리듀스의 느린 디스크 반복 접근 단점을 극복한 인메모리(In-Memory)](/knowledge-base/studynote/14_data_engineering/01_infrastructure/021_apache_spark_in_memory/) →

---
