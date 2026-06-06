---
title: "CXL Chiplet Memory Pool"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) ([Compute Express Link](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/))은 [PCIe](/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) 5.0/6.0 물리 계층을 기반으로 CPU, [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/), 메모리 확장 장치 간 [캐시 일관성](/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) (Cache-Coherent) [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/) 접근을 가능하게 하는 개방형 인터커넥트 표준이다.
> 2. **가치**: DIMM 슬롯 제한을 넘어 테라바이트 수준의 메모리를 서버에 풀로 연결하고, 여러 CPU가 이 [메모리 풀](/studynote/02_operating_system/06_memory_management/369_memory_pool/)을 동적으로 공유함으로써 메모리 집약적 워크로드의 [TCO](/studynote/12_it_management/01_governance_strategy/016_tco/) (Total Cost of Ownership)를 대폭 절감한다.
> 3. **판단 포인트**: [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 메모리는 [DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/) 대비 레이턴시가 약 2~4배 높으므로, [핫 데이터](/studynote/01_computer_architecture/15_advanced_topics/675_hot_data_caching/)는 로컬 DRAM에, 웜 [콜드 데이터](/studynote/01_computer_architecture/15_advanced_topics/676_cold_data_archiving/)는 [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 메모리에 배치하는 [NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/) ([Non-Uniform Memory Access](/studynote/02_operating_system/06_memory_management/377_numa_allocation/)) 인식 소프트웨어 설계가 필수다.

---

## I. 개요 및 필요성

현대 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 및 대용량 [인메모리 데이터베이스](/studynote/16_bigdata/06_nosql/139_inmemory_db/) 워크로드는 테라바이트 수준의 메모리를 요구한다. 그러나 기존 서버 아키텍처는 DIMM (Dual Inline Memory [Module](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)) 슬롯 수와 CPU 메모리 채널 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)의 물리적 한계로 서버당 수 TB 수준에서 확장이 멈춘다.

CXL은 2019년 Intel 주도로 AMD, ARM, Google, Microsoft, Meta 등이 참여해 설립한 컨소시엄이 제정한 표준이다. 핵심 혁신은 PCIe의 물리 계층을 재사용하면서 그 위에 세 가지 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 추가한 것이다.

- <strong><a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/">CXL</a>.io</strong>: 기존 [PCIe](/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) I/O 장치 접근 (기존 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 유지)
- <strong><a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/">CXL</a>.cache</strong>: 장치가 호스트 CPU 메모리를 캐시화
- <strong><a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/">CXL</a>.mem</strong>: 호스트 CPU가 장치의 메모리에 LOAD/STORE 명령으로 직접 접근

[칩렛](/studynote/01_computer_architecture/14_hardware_security_trends/497_chiplet/) ([Chiplet](/studynote/01_computer_architecture/14_hardware_security_trends/497_chiplet/)) 아키텍처는 모놀리식 대형 다이(die) 대신 기능별로 소형 다이를 분리해 고급 패키징으로 연결하는 설계 방식이다. AMD Ryzen의 CCD (Core Complex Die), Intel Meteor Lake의 Tile 아키텍처가 대표적이다. [UCIe](/studynote/01_computer_architecture/12_accelerators_ai_hardware/443_ucie/) ([Universal Chiplet Interconnect Express](/studynote/01_computer_architecture/12_accelerators_ai_hardware/443_ucie/)) 표준은 서로 다른 제조사의 [칩렛](/studynote/01_computer_architecture/14_hardware_security_trends/497_chiplet/)을 연결하는 개방형 규격이다.

- **📢 섹션 요약 비유**: CXL은 서버 메모리를 수도 배관처럼 바꾸는 기술이다. 기존에는 각 집(서버)이 물탱크([DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/))를 따로 소유했지만, CXL로 수도관을 연결하면 지역 전체가 하나의 대형 저수지([메모리 풀](/studynote/02_operating_system/06_memory_management/369_memory_pool/))를 공유할 수 있다.

---

## II. 아키텍처 및 핵심 원리

[CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 메모리 아키텍처의 세 가지 사용 유형:

| [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 유형  | 동작 방식                                | 대표 사용 사례            |
|:--------|:---------------------------------------|:-----------------------|
| Type 1  | [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/).cache: 가속기가 호스트 메모리 캐시화  | [FPGA](/studynote/01_computer_architecture/15_advanced_topics/606_dynamic_partial_reconfiguration/), 네트워크 카드 캐시   |
| Type 2  | [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/).cache + [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/).mem: 가속기 자체 메모리  | [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/), [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 가속기 메모리 통합 |
| Type 3  | [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/).mem: 순수 메모리 확장 장치            | [DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/)/PMem [메모리 풀](/studynote/02_operating_system/06_memory_management/369_memory_pool/) 확장  |

```text
+-----------------------------------------+
|   CXL 메모리 풀링 서버 아키텍처           |
+-----------------------------------------+
|                                         |
|  서버1              서버2               |
|  +---------------+  +---------------+  |
|  | CPU+로컬DRAM  |  | CPU+로컬DRAM  |  |
|  |  64GB DDR5   |  |  64GB DDR5   |  |
|  +------+--------+  +------+--------+  |
|         | CXL.mem         | CXL.mem    |
|         +--------+--------+            |
|                  |                     |
|         +--------v--------+            |
|         | CXL 메모리 풀   |            |
|         | DRAM: 4TB       |            |
|         | PMem: 16TB      |            |
|         | 레이턴시: ~250ns |            |
|         +-----------------+            |
|                                         |
+-----------------------------------------+
```

[NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 토폴로지: [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 메모리는 OS에 별도 [NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 노드로 노출된다. Linux [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 numactl, memkind [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)를 통해 [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 메모리와 로컬 [DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/) 간의 메모리 배치를 제어할 수 있다.

- **📢 섹션 요약 비유**: [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) [메모리 풀](/studynote/02_operating_system/06_memory_management/369_memory_pool/)은 책상 위 책(로컬 [DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/), 빠름)과 바로 옆 책장([CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 메모리, 약간 느림)의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)다. 자주 보는 책은 책상 위에, 가끔 보는 책은 책장에 두면 공간(메모리 슬롯)을 효율적으로 쓸 수 있다.

---

## III. 비교 및 연결

| 항목         | 로컬 [DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/) (DDR5)          | [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 메모리 (Type 3)     | [HBM](/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/) ([High Bandwidth Memory](/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/)) |
|:-----------|:--------------------------|:----------------------|:----------------------------|
| 레이턴시     | 약 80ns                   | 약 200~300ns          | 약 80ns                      |
| [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)      | 약 100 GB/s (dual-channel) | 약 64 GB/s ([CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 2.0) | 약 1 TB/s (HBM3)            |
| 용량        | 최대 6TB (DDR5 48 DIMM)  | 사실상 무제한 확장       | 최대 64GB (온칩 패키지)        |
| 비용        | 중간                       | 낮음 ([DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/) 대비)        | 매우 높음                     |
| 워크로드     | 모든 메모리 집약 워크로드    | 인메모리 DB, 웜 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)   | [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 추론, [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 온칩            |

[칩렛 아키텍처](/studynote/06_ict_convergence/03_cloud_infrastructure/233_chiplet_architecture_advanced_packaging/)는 기능별 최적 공정 원칙을 실현한다. CPU 코어는 최신 5nm 공정으로, I/O 다이는 6nm로, 메모리 컨트롤러는 12nm로 각각 제조해 비용과 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 동시에 최적화한다. 이를 이종 집적 ([Heterogeneous](/studynote/05_database/05_distributed_nosql_newsql/273_heterogeneous_db/) Integration)이라 한다.

- **📢 섹션 요약 비유**: [칩렛](/studynote/01_computer_architecture/14_hardware_security_trends/497_chiplet/)은 레고 블록 조립처럼 다른 회사가 만든 최선의 부품을 연결하는 것이다. CPU 코어(고급 블록), I/O(표준 블록), 메모리 컨트롤러(저렴한 블록)를 최적 비율로 조합한다.

---

## [IV](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/). 실무 적용 및 기술사 판단

[CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 메모리 도입 결정에서 가장 중요한 기준은 워크로드의 메모리 접근 패턴이다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 워크로드가 메모리 바운드(Memory-Bound)[인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)? (CPU 사용률보다 메모리 부족이 병목인 경우)
2. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 패턴에 핫/웜/콜드 계층 구조가 있는가?
3. 소프트웨어가 [NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 인식([NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/)-Aware) 설계로 메모리 배치를 제어하는가?
4. [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 컨트롤러와 서버 CPU가 같은 [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)(1.1/2.0/3.0)을 지원하는가?
5. 메모리 용량 확장 비용이 서버 추가 비용보다 낮은가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 메모리에 [핫 데이터](/studynote/01_computer_architecture/15_advanced_topics/675_hot_data_caching/) 배치: 레이턴시 민감한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 로컬 [DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/) 없이 CXL에만 저장하면 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 2~4배 저하된다.
- [NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 토폴로지 무시: [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 메모리를 일반 DRAM처럼 OS 기본 할당자에 맡기면 임의 배치로 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측이 불가능해진다.
- [칩렛](/studynote/01_computer_architecture/14_hardware_security_trends/497_chiplet/) 내부 레이턴시 과소평가: 다이 간 인터커넥트([UCIe](/studynote/01_computer_architecture/12_accelerators_ai_hardware/443_ucie/), Infinity Fabric)는 온칩 통신보다 느리므로 크로스 다이 접근 패턴을 최소화해야 한다.

- **📢 섹션 요약 비유**: [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 메모리 설계는 주방 도구 배치와 같다. 자주 쓰는 칼([핫 데이터](/studynote/01_computer_architecture/15_advanced_topics/675_hot_data_caching/))은 손 닿는 곳(로컬 [DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/))에, 가끔 쓰는 냄비([콜드 데이터](/studynote/01_computer_architecture/15_advanced_topics/676_cold_data_archiving/))는 수납장([CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 메모리)에 두어야 효율적이다.

---

## V. 기대효과 및 결론

[CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) [메모리 풀링](/studynote/01_computer_architecture/12_accelerators_ai_hardware/442_memory_pooling/)을 도입하면 서버당 메모리 용량을 기존 [DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/) 한계(2~6TB)에서 수십 TB 이상으로 확장할 수 있고, 여러 서버가 [메모리 풀](/studynote/02_operating_system/06_memory_management/369_memory_pool/)을 공유해 메모리 활용률을 높인다. 대용량 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 서빙, 인메모리 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB, 실시간 [OLAP](/studynote/12_it_management/05_security_compliance/316_olap/) 워크로드에서 서버 수 대비 메모리 용량 비율이 획기적으로 개선된다.

한계는 레이턴시 패널티와 소프트웨어 생태계 미성숙이다. [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 1.1의 레이턴시(약 250ns)는 로컬 [DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/)(약 80ns) 대비 3배이며, 이를 활용하는 [NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/)-Aware 소프트웨어가 아직 성숙하지 않았다. [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 2.0/3.0으로 레이턴시가 개선되고 스위칭 구조가 추가되면 메모리 분리(Disaggregation)가 더욱 현실화될 것이다.

CXL은 컴퓨팅과 메모리의 물리적 결합을 끊는 패러다임 전환이다. 메모리를 스토리지처럼 풀로 관리하는 미래가 [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 위에서 실현된다.

- **📢 섹션 요약 비유**: CXL은 개인 자가용(전용 [DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/))에서 카풀 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)([공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/) 풀)로의 전환이다. [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)엔 자가용보다 느릴 수 있지만, 전체 자원 활용률은 훨씬 높아진다.

---

### 📌 관련 개념 맵

| 개념                                              | 연결 포인트                                           |
|:-------------------------------------------------|:----------------------------------------------------|
| [PCIe](/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) ([Peripheral Component Interconnect](/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/) Express)  | CXL의 물리 계층, 고속 서버 인터커넥트 표준              |
| [NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/) ([Non-Uniform Memory Access](/studynote/02_operating_system/06_memory_management/377_numa_allocation/))                 | [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 메모리 접근 패턴 최적화를 위한 핵심 아키텍처 개념     |
| [칩렛](/studynote/01_computer_architecture/14_hardware_security_trends/497_chiplet/) ([Chiplet](/studynote/01_computer_architecture/14_hardware_security_trends/497_chiplet/))                                   | 모놀리식 다이를 기능별 소형 다이로 분리하는 이종 집적 기법  |
| [UCIe](/studynote/01_computer_architecture/12_accelerators_ai_hardware/443_ucie/) ([Universal Chiplet Interconnect Express](/studynote/01_computer_architecture/12_accelerators_ai_hardware/443_ucie/))    | [칩렛](/studynote/01_computer_architecture/14_hardware_security_trends/497_chiplet/) 간 표준 인터커넥트, 이종 제조사 [칩렛](/studynote/01_computer_architecture/14_hardware_security_trends/497_chiplet/) 연결            |
| [HBM](/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/) ([High Bandwidth Memory](/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/))                      | [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 중심 고성능 메모리, CXL과 상호 보완적 위치          |

### 📈 관련 키워드 및 발전 흐름도

```text
DDR DIMM (서버 내 로컬 메모리, 용량 한계)
    |
    v
Intel Optane PMem (persistent memory, NVMe 대비 고속)
    |
    v
CXL 1.0/1.1 (캐시 일관성 메모리 확장)
    |
    v
CXL 2.0 (스위칭, 멀티 서버 메모리 풀링)
    |
    v
CXL 3.0 (P2P 통신, 패브릭 수준 메모리 공유)
    |
    v
메모리 분리 아키텍처 (Compute-Memory Disaggregation)
```

### 👶 어린이를 위한 3줄 비유 설명

1. CXL은 각 컴퓨터(서버)가 자기 메모리만 쓰던 것을 여러 컴퓨터가 하나의 큰 메모리 창고를 함께 쓰게 만드는 기술이에요.
2. 창고([CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 메모리)는 책상(로컬 [DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/))보다 조금 멀어서 꺼내오는 데 시간이 더 걸려요.
3. 그래서 자주 쓰는 것은 책상 위에, 가끔 쓰는 것은 창고에 넣어두는 게 스마트한 방법이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 355 / 373

<- **이전**: [354. 마이크로 프론트엔드 UI 컴포넌트 독립 배포망 (Micro Frontend)](/studynote/13_cloud_architecture/05_data_engineering/354_process/)
**다음**: [356. 데이터옵스 CI/CD dbt 분석 파이프 자동망 (DataOps CI/CD with dbt)](/studynote/15_devops_sre/05_devsecops/356_ci_cd_dbt/) ->

---
