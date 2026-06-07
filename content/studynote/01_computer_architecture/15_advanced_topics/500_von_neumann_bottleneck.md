---
title: "500. Von Neumann Bottleneck"
date: "2026-04-20"
tags:
  - "studynote-computer-architecture"
weight: 500
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 폰 노이만 병목은 연산기보다 메모리 접근과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동이 더 느리고 더 비싸서, CPU (Central Processing Unit)가 계산보다 기다림에 더 많은 시간을 쓰게 되는 현상이다.
> 2. **가치**: 캐시, 프리패치, 다중 채널, [HBM](/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/) ([High Bandwidth Memory](/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/)), [PIM](/studynote/01_computer_architecture/12_accelerators_ai_hardware/430_pim/) ([Processing-In-Memory](/studynote/01_computer_architecture/12_accelerators_ai_hardware/430_pim/)) 같은 개선 기법은 모두 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 더 가까이 두거나, 더 넓게 보내거나, 아예 덜 옮기게 만드는 것"에 초점이 있다.
> 3. **판단 포인트**: 같은 병목처럼 보여도 어떤 워크로드는 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간이 문제이고, 어떤 워크로드는 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)이나 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 에너지가 문제이므로 해법도 다르게 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

폰 노이만 병목은 프로그램과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 같은 메모리 공간에 두는 구조 자체보다, 그 메모리와 연산기 사이의 왕복 비용이 시스템 전체 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 지배하게 되는 현상을 뜻한다. CPU는 몇 개의 cycle 안에 산술 연산을 끝낼 수 있지만, L1 캐시 ([Level 1 Cache](/studynote/01_computer_architecture/06_memory_hierarchy_cache/260_l1_cache/))를 벗어나 L2, L3, [DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/) (Dynamic Random Access Memory)으로 갈수록 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 도착 시간이 급격히 늘어난다. 결국 고성능 코어도 필요한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 제때 받지 못하면 놀게 된다.

이 문제가 중요해진 이유는 연산 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상 속도와 메모리 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)·[대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 개선 속도가 같지 않았기 때문이다. 클럭 향상과 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 실행 덕분에 코어는 빨라졌지만, 외부 메모리 접근은 물리 거리와 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) [무결성](/studynote/09_security/01_intro_principles/003_integrity/), 전력 한계 때문에 훨씬 천천히 개선되었다. 그래서 현대 시스템에서는 "얼마나 빨리 계산하는가"보다 "얼마나 적게 옮기고 빨리 공급받는가"가 더 중요해졌다.

```text
+----------------------------------------------------------------------------+
| 같은 연산기라도 메모리 공급이 늦으면 실제 성능은 멈춘다                      |
+----------------------------------------------------------------------------+
| CPU Core : 연산 수 ns                                                       |
|    |                                                                        |
|    +- L1 Hit    : 수 cycle                                                  |
|    +- L2 / L3   : 수십 cycle                                                |
|    +- DRAM Miss : 수백 cycle                                                |
+----------------------------------------------------------------------------+
| 결과: 연산기 속도보다 데이터 도착 시간이 전체 처리량을 지배                  |
+----------------------------------------------------------------------------+
```

즉 폰 노이만 병목은 "CPU와 메모리가 분리돼 있다"는 교과서 문장을 넘어, <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 이동 자체가 <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>과 에너지의 주적이 된 상태</strong>를 가리킨다. 이 관점을 잡아야 개선 기법도 하나의 흐름으로 읽힌다.

- **📢 섹션 요약 비유**: 요리사는 매우 빠른데 냉장고가 멀어서 재료를 가지러 다니느라 시간을 다 쓰는 주방과 같다. 요리 실력보다 동선이 문제인 상황이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

폰 노이만 병목 개선 기법은 크게 네 방향으로 나뉜다. 첫째, 캐시와 블로킹처럼 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 더 가까이 둬서 평균 접근 시간을 줄인다. 둘째, 프리패치와 [비순차 실행](/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/), [동시 멀티스레딩](/studynote/01_computer_architecture/11_multicore_synchronization/400_smt/) ([SMT](/studynote/01_computer_architecture/11_multicore_synchronization/400_smt/), Simultaneous [Multithreading](/studynote/02_operating_system/02_process_thread/095_multithreading_benefits/))으로 기다리는 시간을 겹쳐 숨긴다. 셋째, 다중 채널과 HBM으로 통로 자체를 넓혀 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 올린다. 넷째, PIM과 Near-Memory Computing처럼 계산을 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 쪽으로 옮겨 이동량 자체를 줄인다.

이 흐름을 정량적으로 이해할 때 자주 쓰는 식이 [AMAT](/studynote/01_computer_architecture/06_memory_hierarchy_cache/265_amat/) (Average Memory Access Time)다.

<strong><a href="/studynote/01_computer_architecture/06_memory_hierarchy_cache/265_amat/">AMAT</a> = <a href="/studynote/01_computer_architecture/06_memory_hierarchy_cache/263_cache_hit_miss/">Hit</a> Time + Miss Rate × Miss Penalty</strong>
즉 캐시 [hit](/studynote/01_computer_architecture/06_memory_hierarchy_cache/263_cache_hit_miss/) 시간을 줄이거나, miss 비율을 낮추거나, miss가 났을 때 손실을 줄이는 방향이 모두 병목 개선으로 이어진다.

| 기법군 | 대표 수단 | 직접 겨냥하는 문제 | 잘 맞는 상황 |
| :-- | :-- | :-- | :-- |
| 지역성 강화 | 캐시 계층, 타일링, 블로킹 | 평균 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 | 반복 접근, 행렬 연산, 일반 애플리케이션 |
| 대기 숨기기 | 프리패치, [비순차 실행](/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/), [SMT](/studynote/01_computer_architecture/11_multicore_synchronization/400_smt/) | 코어 유휴 시간 | 규칙적 접근, 메모리 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 긴 코드 |
| 통로 확장 | 다중 채널, 인터리빙, [HBM](/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/) | [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 부족 | [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/), 고성능 컴퓨팅 ([HPC](/studynote/01_computer_architecture/15_advanced_topics/548_automotive_hpc/), [High Performance Computing](/studynote/06_ict_convergence/03_cloud_infrastructure/226_hpc_supercomputing_infrastructure/)), 스트리밍 처리 |
| 이동 축소 | [PIM](/studynote/01_computer_architecture/12_accelerators_ai_hardware/430_pim/), [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) 최적화, [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 에너지와 트래픽 | 분석, 검색, 대규모 메모리 스캔 |

```text
+----------------------------------------------------------------------------+
| 병목 완화 기법이 개입하는 위치                                               |
+----------------------------------------------------------------------------+
| CPU Core                                                                    |
|   |  <- 비순차 실행 · SMT · 벡터화                                           |
|   v                                                                        |
| Cache Hierarchy                                                             |
|   |  <- 지역성 최적화 · 블로킹 · 프리패치                                   |
|   v                                                                        |
| Memory Channels / HBM                                                       |
|   |  <- 다중 채널 · 인터리빙 · 초광폭 패키징                                |
|   v                                                                        |
| Near-Memory / PIM                                                           |
|      <- 데이터 이동 자체 축소                                                |
+----------------------------------------------------------------------------+
```

이 그림이 보여 주는 핵심은 개선 기법들이 서로 경쟁하기보다 계층별로 누적된다는 점이다. 좋은 시스템은 캐시만 크거나, HBM만 넣거나, PIM만 도입하는 식으로 해결하지 않고, <strong>가까이 두기·겹쳐 숨기기·넓히기·덜 옮기기</strong>를 함께 조합한다.

- **📢 섹션 요약 비유**: 폰 노이만 병목 해결은 냉장고를 더 가깝게 두고, 필요한 재료를 미리 꺼내 놓고, 주방 통로를 넓히고, 어떤 음식은 냉장고 앞에서 바로 손질하는 식으로 동선을 여러 겹 줄이는 일과 같다.

---

## Ⅲ. 비교 및 연결

폰 노이만 병목 개선 기법은 성격이 서로 다르다. 캐시와 프리패치는 기존 구조를 유지하면서 병목을 완화하는 방법이고, HBM은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통로 폭을 키우는 패키징 해법이며, PIM은 아예 계산 위치를 바꾸는 구조적 전환에 가깝다. 그래서 같은 "개선"이라도 효과 범위와 적용 비용이 다르다.

| 접근 방식 | 대표 기술 | 장점 | 한계 |
| :-- | :-- | :-- | :-- |
| 구조 유지형 | 캐시, 프리패치, [비순차 실행](/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/) | 범용성 높고 기존 소프트웨어와 잘 맞음 | 메모리 벽 자체를 없애지는 못함 |
| [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 확장형 | 다중 채널, [HBM](/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/), 인터리빙 | 스트리밍·AI에서 큰 효과 | 비용과 패키징 복잡도 증가 |
| 구조 전환형 | [PIM](/studynote/01_computer_architecture/12_accelerators_ai_hardware/430_pim/), Near-Memory Computing | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 에너지와 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 크게 줄임 | 프로그래밍 모델과 생태계 변화 필요 |

이 주제는 하바드 구조 ([Harvard Architecture](/studynote/01_computer_architecture/03_architecture_basics_performance/126_harvard_architecture/)), [NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/) ([Non-Uniform Memory Access](/studynote/02_operating_system/06_memory_management/377_numa_allocation/)), [칩렛](/studynote/01_computer_architecture/14_hardware_security_trends/497_chiplet/) 메모리 패브릭, [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) ([Compute Express Link](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/))과도 연결된다. 예를 들어 하바드 구조는 명령어와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로를 분리해 일부 병목을 완화하고, NUMA는 메모리 거리가 노드마다 다르다는 점에서 "같은 DRAM도 가까운 것과 먼 것이 다르다"는 현실을 보여 준다. 또 HBM과 [칩렛](/studynote/01_computer_architecture/14_hardware_security_trends/497_chiplet/)은 메모리를 더 가까이 붙이는 방향이고, CXL은 메모리 확장을 유연하게 만들지만 동시에 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 차이를 다시 관리해야 하는 과제를 남긴다.

결국 폰 노이만 병목은 CPU 내부 문제만이 아니라 시스템 전체 계층 문제다. 소프트웨어의 지역성, 운영체제의 메모리 배치, 패키징 기술, 인터커넥트 구조가 모두 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에 영향을 준다. 그래서 이 주제는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/), 아키텍처, 패키징을 함께 묶어 이해할 때 가장 잘 보인다.

- **📢 섹션 요약 비유**: 어떤 해결책은 냉장고 위치만 바꾸고, 어떤 해결책은 주방 복도를 넓히고, 어떤 해결책은 아예 냉장고 안에 조리대를 넣는 것과 같다. 같은 불편을 풀어도 공사 범위가 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 먼저 워크로드가 정말 메모리 병목인지 확인해야 한다. CPU 사용률이 낮다고 모두 폰 노이만 병목은 아니며, 캐시 미스 비율, 메모리 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 포화도, 산술 집약도를 같이 봐야 한다. 예를 들어 행렬 곱셈은 타일링과 캐시 재사용으로 큰 효과를 얻고, 거대 언어 모델 추론은 [HBM](/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/) [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)이 핵심이며, 대규모 스캔 기반 분석은 PIM이나 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)이 더 맞을 수 있다.

### 적용 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. **병목 유형 파악**: [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 문제인가, [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 포화인가, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 에너지인가?
2. **지역성 개선 여지**: [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) 순회 순서, 타일링, 캐시 친화적 자료구조로 해결 가능한가?
3. **메모리 배치**: [NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 노드, 채널 인터리빙, [HBM](/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/) 계층 배치가 적절한가?
4. **하드웨어 투자 타당성**: HBM이나 더 많은 채널 추가가 실제 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상으로 이어지는가?
5. **구조 전환 필요성**: 이동량이 압도적으로 크다면 PIM이나 near-memory 접근을 검토해야 하는가?

### 피해야 할 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 메모리 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)이 이미 포화인데 CPU 클럭이나 코어 수만 늘리는 증설
- 지역성 개선 없이 랜덤 접근 패턴을 그대로 둔 채 캐시 용량만 키우는 설계
- HBM을 넣고도 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 배치를 잘못해 자주 [PCIe](/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) ([Peripheral Component Interconnect](/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/) Express)나 외부 메모리로 왕복시키는 운영

기술사 답안에서는 "캐시를 넣는다" 수준으로 끝내지 말고, <strong>지역성·<a href="/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">대역폭</a>·<a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 이동량</strong>을 구분해 어느 기법이 어느 문제를 직접 겨냥하는지 적는 것이 좋다. 그래야 폰 노이만 병목을 구조적으로 이해하고 있다는 점이 드러난다.

- **📢 섹션 요약 비유**: 주방이 막혔을 때 요리사만 더 뽑아서는 해결되지 않는다. 재료 보관 위치, 통로 폭, 미리 준비하는 방식까지 함께 바꿔야 진짜 빨라진다.

---

## Ⅴ. 기대효과 및 결론

폰 노이만 병목을 잘 다루면 같은 코어 수와 같은 클럭에서도 실제 처리량이 크게 오른다. 캐시 hit가 늘어나면 평균 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간이 줄고, [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)이 넓어지면 연산기가 더 오래 일하며, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동이 줄어들면 에너지 효율도 높아진다. 그래서 병목 개선은 "보조 최적화"가 아니라 시스템 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 현실 값으로 바꾸는 핵심 작업이다.

그러나 이 병목은 완전히 사라지지 않는다. 모델과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 커질수록 다시 새로운 메모리 벽이 생기고, 계층을 늘릴수록 관리 복잡도도 커진다. 앞으로는 HBM4, [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) [메모리 풀링](/studynote/01_computer_architecture/12_accelerators_ai_hardware/442_memory_pooling/), 3D 적층 캐시, [PIM](/studynote/01_computer_architecture/12_accelerators_ai_hardware/430_pim/), [데이터 중심](/studynote/04_software_engineering/06_software_architecture/383_data_centric_architecture/) 아키텍처가 이 문제를 계속 다른 층위에서 완화해 나갈 가능성이 크다.

결론적으로 폰 노이만 병목 개선의 본질은 "더 빠른 CPU 만들기"가 아니라 <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 덜 움직이고, 더 가깝게 두고, 필요한 순간 더 넓게 공급하는 것</strong>이다. 이 한 문장을 기억하면 캐시에서 [HBM](/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/), PIM까지 이어지는 흐름이 자연스럽게 정리된다.

- **📢 섹션 요약 비유**: 폰 노이만 병목 개선은 요리사를 더 빠르게 뛰게 만드는 일이 아니라, 재료가 알아서 제때 도착하고 멀리 가지 않게 주방 구조를 바꾸는 일과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [AMAT](/studynote/01_computer_architecture/06_memory_hierarchy_cache/265_amat/) (Average Memory Access Time) | 캐시 [hit](/studynote/01_computer_architecture/06_memory_hierarchy_cache/263_cache_hit_miss/) 시간, miss 비율, miss penalty를 함께 보는 대표 지표다. |
| 지역성 (Locality) | 캐시와 프리패치가 효과를 내는 전제 조건이다. |
| [HBM](/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/) ([High Bandwidth Memory](/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/)) | 폰 노이만 병목을 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 확장 측면에서 완화하는 대표 패키징 기술이다. |
| [NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/) ([Non-Uniform Memory Access](/studynote/02_operating_system/06_memory_management/377_numa_allocation/)) | 메모리 접근 비용이 노드 위치에 따라 달라지는 시스템 구조다. |
| [PIM](/studynote/01_computer_architecture/12_accelerators_ai_hardware/430_pim/) ([Processing-In-Memory](/studynote/01_computer_architecture/12_accelerators_ai_hardware/430_pim/)) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 옮기지 않고 메모리 근처에서 계산해 구조적으로 병목을 줄인다. |
| [Memory Wall](/studynote/01_computer_architecture/12_accelerators_ai_hardware/433_memory_wall/) | 연산 속도와 메모리 공급 속도 차이에서 생기는 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 한계 개념이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
단일 버스 기반 고전적 폰 노이만 구조
        |
        v
CPU-메모리 속도 격차 확대 = Memory Wall
        |
        v
캐시 계층 · 프리패치 · 비순차 실행
        |
        v
다중 채널 · 인터리빙 · HBM
        |
        v
Near-Memory Computing · PIM · 데이터 중심 아키텍처
```

이 흐름은 병목을 처음에는 숨기고 완화하다가, 점차 메모리 자체와 계산 위치를 바꾸는 방향으로 진화하는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터는 계산은 엄청 빨리 하지만, 필요한 재료를 멀리서 가져오느라 기다릴 때가 많아요.
2. 그래서 자주 쓰는 재료는 가까운 서랍에 두고, 큰 창고와 주방 사이 길도 더 넓게 만들어요.
3. 가장 똑똑한 방법은 아예 창고 근처에서 재료 손질을 끝내서, 꼭 필요한 것만 주방으로 보내는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 500 / 803

<- **이전**: [499. 소프트웨어 정의 인프라 (SDI) 하드웨어 종속성](/studynote/01_computer_architecture/14_hardware_security_trends/499_sdi_hardware_dependency/)
**다음**: [501. 수퍼스칼라 발급 큐 (Superscalar Issue Queue)](/studynote/01_computer_architecture/15_advanced_topics/501_superscalar_issue_queue/) ->

---
