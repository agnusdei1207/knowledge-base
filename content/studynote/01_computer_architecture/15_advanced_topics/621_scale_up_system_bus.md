---
title: "621. 스케일 업 (Scale-Up) 시스템 버스"
date: "2026-05-08"
tags:
  - "studynote-computer-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스케일 업 (Scale-Up) [시스템 버스](/studynote/01_computer_architecture/03_architecture_basics_performance/127_system_bus/)는 여러 CPU [소켓](/studynote/02_operating_system/02_process_thread/125_socket/)과 대용량 메모리를 하나의 서버 이미지로 묶어, <strong><a href="/studynote/02_operating_system/02_process_thread/118_shared_memory/">공유 메모리</a> 기반의 단일 대형 시스템</strong>처럼 동작하게 하는 내부 상호연결 구조다.
> 2. **가치**: [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)으로 잘게 쪼개기 어려운 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/), 인메모리 분석, 대형 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 호스트는 노드 간 네트워크보다 <strong><a href="/studynote/02_operating_system/02_process_thread/125_socket/">소켓</a> 간 <a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a> 보장형 고속 연결</strong>에서 더 높은 실효 성능을 얻는다.
> 3. **판단 포인트**: 코어 수만 늘린다고 성능이 선형 증가하지 않으며, 비균일 메모리 접근 ([NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/), [Non-Uniform Memory Access](/studynote/02_operating_system/06_memory_management/377_numa_allocation/)) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 [캐시 일관성](/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) 비용을 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)와 애플리케이션이 함께 감당할 수 있어야 한다.

---

## Ⅰ. 개요 및 필요성

스케일 업 [시스템 버스](/studynote/01_computer_architecture/03_architecture_basics_performance/127_system_bus/)는 하나의 서버 안에 여러 프로세서 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/)을 배치하고, 이들을 [초고속](/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 내부 연결로 묶어 단일 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 인스턴스가 바라보는 거대한 컴퓨터를 만드는 구조다. 대칭형 다중처리 ([SMP](/studynote/02_operating_system/03_cpu_scheduling/195_real_time_scheduling/), Symmetric Multiprocessing)에서 출발했지만, 현대 대형 서버는 대부분 [NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 구조를 채택해 각 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/)이 자기 메모리를 갖고도 전체 주소 공간을 공유하도록 설계한다.

이런 구조가 필요한 이유는 모든 워크로드가 [스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/) ([Scale-Out](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))으로 예쁘게 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)되지 않기 때문이다. 대형 온라인 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 처리 ([OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/), Online [Transaction](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Processing) [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/), 전사적 자원 관리 ([ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/), [Enterprise Resource Planning](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)), 대규모 메모리 공유형 분석은 상태 공유와 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)가 많아 노드 간 네트워크 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 비용이 급격히 커진다. 이때는 여러 대의 작은 서버보다, 한 대의 큰 서버 안에서 메모리 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 유지하며 처리하는 편이 단순하고 빠르다.

[시스템 버스](/studynote/01_computer_architecture/03_architecture_basics_performance/127_system_bus/)가 약하면 많은 CPU를 꽂아도 실제로는 메모리 병목 때문에 성능이 늘지 않는다. 결국 스케일 업의 핵심은 "CPU 개수"가 아니라, <strong><a href="/studynote/02_operating_system/02_process_thread/125_socket/">소켓</a> 간 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>와 캐시 상태를 얼마나 빠르고 일관되게 주고받을 수 있는가</strong>에 있다.

- **📢 섹션 요약 비유**: 스케일 업은 직원 수만 늘린 회의가 아니라, 모두가 같은 전광판을 즉시 보는 지휘실에 가깝다. 전광판 연결이 느리면 사람은 많아도 회의가 굴러가지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

현대 스케일 업 서버는 중앙 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 하나를 여러 CPU가 공유하던 방식보다, 각 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/)을 점대점으로 연결하는 포인트 투 포인트 ([Point-to-Point](/studynote/07_enterprise_systems/03_eai_esb_msa/142_point_to_point_integration_spaghetti/)) 인터커넥트를 사용한다. 인텔의 퀵패스 인터커넥트 (QPI, QuickPath Interconnect), 이후의 초경로 인터커넥트 (UPI, Ultra Path Interconnect), AMD의 인피니티 패브릭 (Infinity Fabric)이 대표적이다. 이 링크는 단순 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동뿐 아니라 [캐시 일관성](/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) 메시지, 원격 메모리 접근 요청, [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 신호까지 함께 운반한다.

| 구성 요소 | 역할 | 성능에 미치는 영향 |
| :-- | :-- | :-- |
| CPU [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) ([Socket](/studynote/02_operating_system/02_process_thread/125_socket/)) | 코어와 마지막 단계 캐시를 보유 | [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 수가 늘수록 공유 상태 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 부담 증가 |
| 메모리 컨트롤러 (Memory Controller) | 로컬 [DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/) 접근 처리 | 로컬 접근은 빠르지만 원격 접근은 추가 홉 발생 |
| [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 간 인터커넥트 | [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·캐시 상태 교환 | [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 부족 시 원격 메모리와 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 트래픽이 병목 |
| [캐시 일관성](/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | 여러 캐시의 동일 주소 값을 맞춤 | 코어 수 증가 시 snoop·[directory](/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 비용이 커짐 |

아래 그림은 4소켓 [NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 서버에서 "로컬 메모리"와 "원격 메모리" 경로가 어떻게 달라지는지 보여준다.

```text
+----------------------------------------------------------------------------+
|        4-Socket NUMA: local DRAM is near, remote DRAM crosses links       |
+----------------------------------------------------------------------------+
|  [CPU0]--UPI/IF--[CPU1]                                                   |
|    |              |                                                       |
|  DRAM0          DRAM1                                                     |
|    |              |                                                       |
|  [CPU2]--UPI/IF--[CPU3]                                                   |
|    |              |                                                       |
|  DRAM2          DRAM3                                                     |
|                                                                            |
|  Local path  : CPU0 -> DRAM0                                              |
|  Remote path : CPU0 -> UPI/IF -> CPU1 -> DRAM1                            |
|  Coherence   : cache state must be checked before remote data is used     |
+----------------------------------------------------------------------------+
```

실제 운영에서는 로컬 메모리 접근이 대략 수십에서 100ns 안팎인 반면, 원격 메모리는 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 홉과 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)이 추가되어 더 큰 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 보인다. 그래서 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 버퍼 풀, 가상 머신 메모리, 분석 엔진 스레드를 해당 [NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 노드에 가깝게 배치하는 것이 중요하다. 스케일 업 [시스템 버스](/studynote/01_computer_architecture/03_architecture_basics_performance/127_system_bus/)는 결국 "모든 CPU를 한 방에 모으는 기술"이 아니라, <strong>멀어진 메모리 거리를 인터커넥트와 <a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a> 제어로 견디게 만드는 기술</strong>이다.

- **📢 섹션 요약 비유**: 각 팀원 책상 옆에 개인 서랍이 있고, 남의 서랍을 열려면 복도를 뛰어가 관리대장까지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)받는 사무실과 같다. 복도와 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 절차가 빠를수록 대형 사무실도 효율적으로 움직인다.

---

## Ⅲ. 비교 및 연결

스케일 업 [시스템 버스](/studynote/01_computer_architecture/03_architecture_basics_performance/127_system_bus/)와 [스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/) 클러스터 망의 가장 큰 차이는 <strong>공유 방식</strong>이다. 스케일 업은 하드웨어가 [캐시 일관성](/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/)을 보장하는 [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/) 모델을 제공하지만, [스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)은 네트워크 위에서 [메시지 전달](/studynote/02_operating_system/02_process_thread/119_message_passing/)과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)를 소프트웨어가 직접 다룬다. 따라서 같은 "확장"이라도 프로그래밍 모델, 장애 범위, 운영 전략이 완전히 달라진다.

| 항목 | 스케일 업 [시스템 버스](/studynote/01_computer_architecture/03_architecture_basics_performance/127_system_bus/) | [스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/) 클러스터 망 |
| :-- | :-- | :-- |
| [데이터 공유](/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/) 방식 | [캐시 일관성](/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) 기반 [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/) | [메시지 전달](/studynote/02_operating_system/02_process_thread/119_message_passing/)·[샤딩](/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)·[복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) |
| [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) 범위 | ns ~ low μs | 수십 μs ~ ms |
| 장애 범위 | 한 대의 서버가 큰 실패 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) | 노드 단위로 격리 가능 |
| 확장 비용 곡선 | [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 수가 늘수록 급격히 상승 | 노드 추가가 비교적 선형 |
| 적합 워크로드 | 강한 공유 상태, 대용량 메모리 | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 가능 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 대규모 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 |

[운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)도 이 차이를 직접 다룬다. 리눅스는 [NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 스케줄러와 CPU 바인딩으로 스레드를 가까운 메모리에 붙이려 하고, [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)는 버퍼 풀과 세션을 특정 노드에 고정해 원격 메모리 비율을 낮추려 한다. 즉 스케일 업 [시스템 버스](/studynote/01_computer_architecture/03_architecture_basics_performance/127_system_bus/)는 하드웨어 주제처럼 보이지만, 실제 성패는 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)와 미들웨어가 NUMA를 얼마나 의식하느냐에 달려 있다.

- **📢 섹션 요약 비유**: 스케일 업은 한 건물 안에서 빠른 엘리베이터와 공용 문서를 쓰는 회사이고, [스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)은 여러 지점을 택배와 메신저로 묶은 회사다. 둘 다 조직이지만 일하는 규칙이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

스케일 업 [시스템 버스](/studynote/01_computer_architecture/03_architecture_basics_performance/127_system_bus/)는 메모리를 크게 공유해야 하고, [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)에 민감하며, 소프트웨어를 쉽게 쪼갤 수 없는 환경에서 빛난다. 대표적으로 대형 단일 인스턴스 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/), 대규모 인메모리 분석, 코어당 라이선스보다 노드 수 제약이 더 큰 상용 패키지, 그리고 고밀도 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 호스트가 여기에 속한다. 반대로 웹 애플리케이션, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 처리, 배치 파이프라인처럼 수평 확장이 쉬운 업무는 비싼 대형 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 장비보다 [스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)이 유리하다.

기술사 관점의 판단 체크리스트는 다음과 같다.

1. 워크로드가 [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/) 이점을 실제로 얻는가, 아니면 메시지 기반 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)이 더 자연스러운가?
2. 원격 메모리 비율과 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 간 트래픽을 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)·[하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 수준에서 관찰하고 제어할 수 있는가?
3. 4소켓, 8소켓으로 올라갈수록 늘어나는 전력, 라이선스, 장애 영향 범위를 감당할 수 있는가?
4. 가상 머신 CPU pinning, 메모리 locality, 인터리빙 정책을 운영 팀이 유지할 역량이 있는가?

흔한 안티패턴은 "코어 수가 많으니 무조건 빠르다"고 믿고 NUMA를 숨긴 채 가상 머신을 무작위로 배치하는 것이다. 이 경우 원격 메모리와 [캐시 일관성](/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) 트래픽이 폭증해, 8소켓 서버가 기대보다 느린 비싼 장비가 되기 쉽다. 스케일 업은 하드웨어를 사는 행위가 아니라, <strong><a href="/studynote/02_operating_system/06_memory_management/377_numa_allocation/">NUMA</a> 친화적 배치 정책까지 함께 설계하는 행위</strong>로 봐야 한다.

- **📢 섹션 요약 비유**: 대형 도서관을 짓는다고 자동으로 공부가 잘되지는 않는다. 자주 보는 책을 자기 자리 가까이에 놓고, 동선을 설계해야 큰 건물의 장점이 살아난다.

---

## Ⅴ. 기대효과 및 결론

스케일 업 [시스템 버스](/studynote/01_computer_architecture/03_architecture_basics_performance/127_system_bus/)가 잘 설계되면 단일 시스템 이미지, 대용량 [메모리 풀](/studynote/02_operating_system/06_memory_management/369_memory_pool/), 낮은 내부 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이라는 강점을 얻는다. 그 결과 애플리케이션 구조를 크게 바꾸지 않고도 성능을 높일 수 있고, 운영자도 여러 노드가 아니라 하나의 큰 서버를 기준으로 자원을 관리할 수 있다. 특히 메모리 집약형 상용 워크로드에서는 이런 단순성이 큰 경쟁력이 된다.

그러나 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 수가 늘수록 비용과 소비전력, [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 오버헤드, 장애 파급 범위도 함께 커진다. 그래서 최근에는 [칩렛](/studynote/01_computer_architecture/14_hardware_security_trends/497_chiplet/), 고속 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 인터커넥트, 계산 익스프레스 링크 ([CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/), [Compute Express Link](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/)) 기반 메모리 확장처럼 "한 대를 더 크게 만들되, 메모리와 가속기를 더 유연하게 붙이는 방향"으로 진화하고 있다. 결국 이 주제는 <strong>CPU를 많이 꽂는 법</strong>이 아니라, <strong>한 대의 서버를 어디까지 일관된 <a href="/studynote/02_operating_system/02_process_thread/118_shared_memory/">공유 메모리</a> 기계로 유지할 수 있는가</strong>로 기억하는 것이 정확하다.

- **📢 섹션 요약 비유**: 스케일 업은 도시를 무조건 넓히는 것이 아니라, 중심가의 도로와 지하철을 정교하게 깔아 한 도시 안에서 빠르게 움직이게 만드는 일과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| 대칭형 다중처리 ([SMP](/studynote/02_operating_system/03_cpu_scheduling/195_real_time_scheduling/), Symmetric Multiprocessing) | 여러 CPU가 하나의 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)를 공유하는 기본 모델 |
| 비균일 메모리 접근 ([NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/), [Non-Uniform Memory Access](/studynote/02_operating_system/06_memory_management/377_numa_allocation/)) | 로컬·원격 메모리 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 차이가 생기는 현대 대형 서버 구조 |
| [캐시 일관성](/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) ([Cache Coherence](/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/)) | 여러 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/)이 같은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 값을 다르게 보지 않게 맞추는 핵심 메커니즘 |
| 초경로 인터커넥트 (UPI, Ultra Path Interconnect) | 인텔 계열 스케일 업 서버의 대표적인 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 간 연결 기술 |
| 계산 익스프레스 링크 ([CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/), [Compute Express Link](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/)) | 메모리·가속기 확장을 더 유연하게 만드는 차세대 coherent 연결 |

### 📈 관련 키워드 및 발전 흐름도

```text
공유 버스 기반 SMP
    |
    v
NUMA + 소켓별 메모리 컨트롤러
    |
    v
QPI/UPI · Infinity Fabric
    |
    v
NUMA 스케줄링 · 디렉터리 기반 일관성 최적화
    |
    v
CXL 기반 메모리 확장
```

이 흐름은 "CPU를 많이 연결하는 문제"가 점차 "메모리와 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 얼마나 효율적으로 확장하는가"의 문제로 이동했음을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 스케일 업 [시스템 버스](/studynote/01_computer_architecture/03_architecture_basics_performance/127_system_bus/)는 큰 집 안에서 여러 사람이 같은 장난감 상자를 함께 쓰게 해 주는 빠른 복도예요.
2. 내 방 장난감은 바로 집을 수 있지만, 다른 방 장난감은 복도를 건너가야 해서 조금 더 오래 걸려요.
3. 그래서 큰 집일수록 복도를 잘 만들고, 자주 쓰는 장난감은 내 방 가까이에 두는 게 중요하답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 621 / 803

<- **이전**: [620. 서버리스 컴퓨팅 컨테이너 분리 하드웨어 기술](/studynote/01_computer_architecture/15_advanced_topics/620_serverless_hw_isolation/)
**다음**: [622. 스케일 아웃 (Scale-Out) 클러스터 망](/studynote/01_computer_architecture/15_advanced_topics/622_scale_out_cluster/) ->

---
