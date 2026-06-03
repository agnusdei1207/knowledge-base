+++
title = "300. 페이지 교체 알고리즘 (Page Replacement)"
date = 2026-04-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [페이지 교체 알고리즘](/knowledge-base/studynote/02_operating_system/07_virtual_memory/401_page_replacement_algorithms/) ([Page Replacement Algorithm](/knowledge-base/studynote/02_operating_system/07_virtual_memory/395_page_replacement_algorithm/))은 물리 메모리의 빈 프레임이 없을 때, 다음 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 손실이 가장 작도록 희생 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 고르는 가상 메모리의 의사결정 규칙이다.
> 2. **가치**: 같은 메모리 용량이라도 어떤 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 내보내느냐에 따라 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) ([Page Fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)) 빈도, 디스크 입출력, 응답시간, [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) ([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)) 위험이 크게 달라진다.
> 3. **판단 포인트**: 최적 해답은 미래 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)를 알아야 하지만 현실은 불가능하므로, [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 지역성 (Locality), [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/), 수정 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/), 워크로드 특성을 이용해 정확도와 구현 비용 사이에서 타협한다.

---

## Ⅰ. 개요 및 필요성

[페이지 교체 알고리즘](/knowledge-base/studynote/02_operating_system/07_virtual_memory/401_page_replacement_algorithms/)은 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/) ([Demand Paging](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)) 환경에서 새 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 적재해야 하지만 메인 메모리의 모든 프레임이 이미 사용 중일 때, 어떤 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 내보낼지 정하는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이다. 가상 메모리는 프로세스에게 큰 주소 공간을 제공하지만, 실제 하드웨어인 RAM (Random Access Memory)은 유한하므로 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 항상 "무엇을 남기고 무엇을 밀어낼지"를 판단해야 한다. 이 판단이 필요한 이유는 프로그램의 접근 패턴이 무작위가 아니라 [시간적 지역성](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/247_temporal_locality/) ([Temporal Locality](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/247_temporal_locality/))과 [공간적 지역성](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/248_spatial_locality/) ([Spatial Locality](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/248_spatial_locality/))을 띠기 때문이다. 최근에 쓴 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)와 그 주변 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 다시 쓸 가능성이 높으므로, 지역성을 잘 따라가는 교체 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)일수록 적은 메모리로도 높은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 낸다.

반대로 교체 판단이 틀리면 CPU (Central Processing Unit)가 계산보다 디스크 대기 시간을 더 오래 견디게 된다. 특히 밀리초(ms) 단위의 디스크 접근이 반복되면 나노초(ns)~마이크로초(μs) 단위의 메모리 접근 장점이 사실상 사라지고, 시스템은 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 들이고 내보내는 데 대부분의 시간을 쓰게 된다. 이것이 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)이며, [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)는 단순한 저장공간 관리가 아니라 시스템 생존성을 좌우하는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 제어 문제다.

이 그림은 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)가 발생한 뒤 교체 여부와 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 비용이 어떻게 갈리는지를 보여준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│              페이지 폴트 이후의 핵심 의사결정 흐름                        │
├────────────────────────────────────────────────────────────────────────────┤
│ CPU 참조 ─▶ 페이지 폴트 ─▶ 빈 프레임 있음? ── 예 ─▶ 즉시 적재             │
│                           │                                                │
│                           └─ 아니오 ─▶ 희생 페이지 선택                    │
│                                         │                                  │
│                                         ▼                                  │
│                              Dirty Bit = 1 인가?                           │
│                                │                 │                          │
│                               예                아니오                      │
│                                │                 │                          │
│                         디스크에 기록        바로 제거                       │
│                                │                 │                          │
│                                └─────── 빈 프레임 확보 ───────▶ 새 페이지 적재 │
└────────────────────────────────────────────────────────────────────────────┘
```

핵심은 교체가 "누구를 버릴까"만의 문제가 아니라 "버리는 데 얼마가 드는가"까지 포함한다는 점이다. 수정 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 켜진 더티 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 내보내기 전에 반드시 보조기억장치에 써야 하므로, 같은 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 패턴에서도 [희생자 선택](/knowledge-base/studynote/02_operating_system/05_deadlock/310_victim_selection/) 비용이 달라진다.

- **📢 섹션 요약 비유**: 좌석이 꽉 찬 도서관에서 새 손님을 받으려면, 곧 다시 올 사람 자리를 빼앗으면 혼란이 커진다. [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)는 "지금 가장 덜 아쉬운 자리를 비우는" 사서의 판단과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)의 핵심 입력은 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)열 ([Reference](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) String), 프레임 수, [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) ([Reference](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [Bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/)), 수정 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) ([Dirty Bit](/knowledge-base/studynote/02_operating_system/07_virtual_memory/396_dirty_bit/))다. [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 메모리 관리 장치인 [MMU](/knowledge-base/studynote/02_operating_system/06_memory_management/328_mmu/) ([Memory Management Unit](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/284_mmu/))가 남기는 접근 흔적을 활용해, 최근에 쓰였는지와 내보낼 때 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 비용이 큰지를 함께 판단한다. 이때 이상적인 목표는 앞으로 가장 늦게 다시 쓰일 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 버리는 것이지만, 미래를 알 수 없으므로 현실 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 "최근 과거가 가까운 미래를 어느 정도 대표한다"는 가정 위에 서 있다.

대표 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 보면 각 방식이 무엇을 근거로 미래를 추정하는지가 다르다.

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 희생자 선정 기준 | 장점 | 한계 및 구현 비용 |
| :--- | :--- | :--- | :--- |
| [FIFO](/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) (First-In, First-Out) | 가장 먼저 들어온 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) | 구현이 가장 단순 | 지역성 무시, 벨라디의 모순 가능 |
| [OPT](/knowledge-base/studynote/02_operating_system/11_exam_summary/724_optimal_page_replacement_unrealizable/) (Optimal) | 미래에 가장 늦게 다시 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)될 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) | 이론상 최저 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) | 미래 정보 필요, 실제 구현 불가 |
| [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) ([Least Recently Used](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/)) | 가장 오래 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)되지 않은 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) | 지역성 반영, [성능 우수](/knowledge-base/studynote/05_database/07_exam_summary/484_elt_extract_load_transform/) | 정확 구현 시 시간 기록 비용 큼 |
| [LFU](/knowledge-base/studynote/02_operating_system/04_synchronization/263_lfu_page_replacement/) ([Least Frequently Used](/knowledge-base/studynote/02_operating_system/04_synchronization/263_lfu_page_replacement/)) | 누적 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 횟수가 가장 적은 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) | 장기 인기 데이터에 유리 | 최근 급변 워크로드 반영이 둔함 |
| [Clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/) (Second Chance) | [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 0인 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 순환 탐색 | [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) 근사, 구현이 가벼움 | 완전한 LRU보다 정확도 낮을 수 있음 |

특히 실무에서 많이 쓰는 Clock은 "최근에 한 번이라도 쓰였으면 한 번 봐준다"는 아이디어로 동작한다. [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 원형 리스트처럼 프레임을 훑으며 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 1이면 0으로 내리고 지나가고, [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 0인 프레임을 만나면 희생자로 선택한다. 이는 하드웨어 추적 정보는 최소만 쓰면서도 최근 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 어느 정도 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)할 수 있어, LRU의 철학을 저비용으로 흉내 내는 방식이다.

이 그림은 [Clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 왜 "최근에 쓴 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)에게 두 번째 기회"를 주는지 보여준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                    Clock 알고리즘의 순환 스캔                              │
├────────────────────────────────────────────────────────────────────────────┤
│                    hand                                                    │
│                     ▼                                                      │
│      [P1,R=1] ─ [P2,R=0] ─ [P3,R=1] ─ [P4,R=0]                            │
│         │          │          │          │                                 │
│   R=1 이면 0으로    └─ 희생 가능  R=1 이면 0으로   다음 후보                │
│   내리고 통과                     내리고 통과                              │
│                                                                            │
│  1회전 차: 최근 사용 페이지는 보호                                          │
│  2회전 차: 여전히 참조되지 않은 페이지가 실제 희생자가 됨                   │
└────────────────────────────────────────────────────────────────────────────┘
```

교체 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)에는 중요한 이론적 구분도 있다. LRU와 OPT처럼 프레임 수가 늘어나면 기존 메모리 집합을 포함하는 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) [Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))은 일반적으로 프레임 증가가 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 악화로 이어지지 않는다. 반면 FIFO처럼 포함 성질이 없는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 프레임을 더 줬는데도 폴트가 늘어나는 벨라디의 모순 (Bélády's [Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/))을 일으킬 수 있다. 따라서 핵심 원리는 단순히 "오래된 것을 버린다"가 아니라, <strong>지역성을 얼마나 보존하면서 구현 비용을 감당할 수 있느냐</strong>다.

- **📢 섹션 요약 비유**: 냉장고가 꽉 찼을 때 FIFO는 먼저 넣은 반찬부터 버리고, LRU는 한동안 먹지 않은 반찬을 버리며, Clock은 "최근에 손댄 음식은 일단 한 번 더 남겨두자"고 판단하는 방식이다.

---

## Ⅲ. 비교 및 연결

[페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)를 제대로 이해하려면 "이론상 최선"과 "현실의 근사치"를 구분해야 한다. OPT는 기준점으로는 완벽하지만 구현 불가능하고, FIFO는 구현은 쉽지만 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 안정성이 약하다. 그래서 실제 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) 계열 또는 그 근사 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 채택한다. 즉 비교의 핵심은 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 이름보다 <strong>미래 예측 정확도와 상태 추적 오버헤드의 균형</strong>이다.

또한 [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)는 캐시 교체와 닮았지만 판단 시간이 전혀 다르다. CPU 캐시는 수 ns 안에 결정을 내려야 하므로 회로가 단순한 Pseudo-[LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) (Pseudo [Least Recently Used](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/)) 같은 방식이 쓰이고, [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)는 디스크나 [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) ([Solid State Drive](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/)) I/O를 앞두고 있으므로 수십~수백 ns의 추가 계산보다 잘 고르는 편이 훨씬 이득이다. 같은 "replacement"라도 계층마다 최적 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 달라지는 이유다.

[운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)과의 연결도 중요하다. [전역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/399_global_replacement/) ([Global Replacement](/knowledge-base/studynote/02_operating_system/07_virtual_memory/399_global_replacement/))는 시스템 전체 프레임 풀에서 희생자를 고르므로 순간 효율은 높을 수 있지만, 메모리 집약 프로세스가 다른 프로세스의 작업 집합 ([Working Set](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/))을 침식할 위험이 있다. 반대로 [지역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/400_local_replacement/) ([Local Replacement](/knowledge-base/studynote/02_operating_system/07_virtual_memory/400_local_replacement/))는 프로세스별 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)가 쉽지만, 유휴 프레임을 융통성 있게 공유하지 못할 수 있다. 따라서 [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 선택만의 문제가 아니라, 스케줄링·메모리 할당 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)과 함께 봐야 한다.

이 연결점에서 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) ([Working Set](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/))과 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 빈도 제어인 [PFF](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/) ([Page Fault Frequency](/knowledge-base/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/))가 등장한다. [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)은 "지금 프로세스가 실제로 유지해야 하는 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 묶음"을 추정하고, PFF는 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 빈도가 높아질 때 프레임을 더 배정하거나 실행 수준을 낮추는 방식으로 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)을 제어한다. 즉 [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)는 독립 기법이 아니라 워크로드 적응형 메모리 관리 체계의 한 축이다.

- **📢 섹션 요약 비유**: OPT는 시험 문제 답안을 미리 본 상태에서 짐 싸는 것이고, FIFO는 아무 생각 없이 먼저 넣은 짐부터 버리는 것이다. 현실의 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 여행 패턴을 기억해 "곧 다시 쓸 물건"을 남기는 숙련된 짐 정리법에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 중요한 질문은 "어떤 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 가장 아름다운가"가 아니라 "현재 워크로드에서 어떤 지표가 병목을 말해 주는가"다. [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/), JVM (Java [Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)), 브라우저, [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 호스트는 모두 메모리를 크게 쓰지만 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 패턴이 다르다. 순차 스캔이 많은 배치성 작업은 막 읽은 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 곧 다시 안 볼 수 있고, 온라인 트랜잭션은 소수 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 매우 자주 재사용한다. 따라서 교체 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 평균 이론보다 워크로드의 지역성 구조를 읽어야 한다.

### 실무 판단 포인트

1. <strong>Major Fault 증가 여부 <a href="/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>: [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 중 디스크 I/O를 동반하는 주요 폴트가 급증하면 교체 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)보다 먼저 메모리 부족 자체를 의심해야 한다.
2. **pgscan / pgsteal 비율 관찰**: 리눅스에서는 많이 스캔하고 적게 회수하면 적합한 희생자를 못 찾고 있다는 뜻이므로, [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) 전조로 본다.
3. <strong>Swap In/Out 지속 여부 <a href="/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>: 스왑 입출력이 지속되면 작업 집합이 RAM을 넘고 있다는 의미다. 이때는 튜닝보다 증설이 정답일 수 있다.
4. **애플리케이션 자체 캐시와 충돌 여부 점검**: [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)나 검색엔진은 자체 버퍼 풀을 쓰므로, [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 캐시와 이중 캐시가 되면 의도치 않은 교체 압력이 생길 수 있다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- 최근 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)율 상승이 일시적 버스트인가, 지속적 작업 집합 초과인가?
- 더티 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 비중이 높아 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 지연이 교체 병목으로 이어지고 있는가?
- [전역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/399_global_replacement/)가 특정 프로세스의 지연시간 꼬리를 악화시키고 있지 않은가?
- [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)/가상머신 환경에서 cgroup 제한이나 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 풍선 메모리 때문에 실제 가용 프레임이 줄어든 것은 아닌가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/">FIFO</a> 수준의 단순 사고로 병목 해석하기</strong>: 메모리 문제를 "오래된 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 빨리 버리면 된다"로 단순화하면 지역성 붕괴를 놓친다.
- **스왑을 무조건 끄는 운영**: 지연을 줄이려다 완충지대를 없애면, 급격한 메모리 압박 시 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) ([Out Of Memory](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/)) 종료가 더 빨리 올 수 있다.
- <strong>애플리케이션 캐시와 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a> 캐시를 동시에 극단적으로 키우기</strong>: 두 계층이 서로의 작업 집합을 밀어내며 오히려 교체 비용만 키운다.

기술사 답안이나 설계 면접에서는 "교체 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 무엇으로 쓸까"보다 "언제 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 문제를 의심하고, 언제 용량 문제로 판단할까"를 말할 수 있어야 한다. [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)는 튜닝의 마지막 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%를 다루지만, 실제 장애의 90%는 작업 집합이 물리 메모리를 초과한 상태에서 나타난다.

- **📢 섹션 요약 비유**: 옷장이 복잡할 때 접는 방법을 바꾸는 것도 중요하지만, 당장 옷장 크기를 넘는 옷을 쌓아 두었다면 정리 기술만으로는 해결되지 않는다. [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)도 정리 규칙과 수납 용량을 함께 봐야 한다.

---

## Ⅴ. 기대효과 및 결론

좋은 [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 같은 하드웨어에서도 체감 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 크게 바꾼다. 자주 쓰는 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 오래 남기면 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)율이 줄고, 디스크 I/O가 감소하며, CPU가 대기보다 계산에 더 많은 시간을 쓰게 된다. 결과적으로 응답시간 안정성, 다중 프로세스 공존성, 메모리 활용률이 함께 좋아진다. 특히 서버 환경에서는 평균 처리량보다 지연시간 꼬리와 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) 회피가 더 중요한데, 적절한 교체 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 이 구간을 방어하는 데 직접 기여한다.

다만 교체 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)만으로 모든 메모리 문제를 해결할 수는 없다. 지역성이 거의 없는 스트리밍성 대용량 작업에서는 어떤 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)도 높은 적중률을 만들기 어렵고, 더티 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 매우 많으면 희생자 선정보다 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 대기 자체가 병목이 된다. 또한 현대 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 단일 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 하나로 끝나지 않고, 세대별 LRU나 다중 큐처럼 워크로드를 분류해 다른 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 수준을 적용한다. 즉 미래 방향은 "하나의 완벽한 규칙"보다 "접근 패턴을 더 잘 분류하는 적응형 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)"에 가깝다.

결론적으로 [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)는 메모리 관리의 뒷정리 기술이 아니라, 유한한 RAM 위에서 무한해 보이는 주소 공간을 유지하게 만드는 핵심 조정 장치다. 이 개념은 "무엇을 버릴까"로만 기억하면 반쪽이고, "무엇을 남겨야 다음 계산이 끊기지 않는가"라는 관점으로 기억해야 실무와 시험에서 모두 강해진다.

- **📢 섹션 요약 비유**: 잘하는 여행자는 가방에서 덜 중요한 물건을 빼는 사람이 아니라, 도착지에서 다시 꼭 쓸 물건을 끝까지 남겨 두는 사람이다. [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)도 버리는 기술보다 남겨 둘 것을 알아보는 기술에 가깝다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) ([Page Fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)) | 교체 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 실제로 호출되는 직접 계기 |
| 작업 집합 ([Working Set](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)) | 현재 프로세스가 유지해야 할 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 범위를 추정해 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)을 줄임 |
| [PFF](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/) ([Page Fault Frequency](/knowledge-base/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/)) | [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 빈도를 기준으로 프레임 배정을 조절하는 운영 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| [더티 비트](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/278_dirty_bit/) ([Dirty Bit](/knowledge-base/studynote/02_operating_system/07_virtual_memory/396_dirty_bit/)) | 희생 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 퇴출 비용을 결정하는 핵심 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) |
| [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) ([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)) | 교체 실패가 시스템 전체 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 붕괴로 이어진 상태 |
| [Clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) 철학을 저비용으로 구현하는 대표적 실무 기법 |

### 📈 관련 키워드 및 발전 흐름도

```text
단순 교체 필요성 인식
    │
    ▼
FIFO (First-In, First-Out)
    │
    ├─ 한계 노출: 벨라디의 모순 (Bélády's Anomaly)
    ▼
OPT (Optimal)로 이상적 기준 정립
    │
    ▼
LRU (Least Recently Used) 중심의 지역성 활용
    │
    ▼
Clock · Second Chance로 실무형 근사 구현
    │
    ▼
Working Set · PFF (Page Fault Frequency) 기반 스래싱 제어
    │
    ▼
적응형 다중 큐 · 세대 기반 메모리 관리로 확장
```

이 흐름은 [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)가 단순 순서 규칙에서 출발해, 지역성 이해와 운영 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 결합을 거쳐, 오늘날의 적응형 메모리 관리로 발전했음을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감 상자가 꽉 찼는데 새 장난감을 넣으려면, 지금 덜 쓰는 장난감을 하나 빼야 해요.
2. 어제도 오늘도 가지고 논 장난감을 빼면 바로 다시 찾게 되니까, 한동안 안 만진 장난감을 빼는 게 더 똑똑해요.
3. 컴퓨터도 똑같이, 곧 다시 쓸 것 같은 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 남기고 덜 중요한 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 바꾸며 기억 공간을 아껴 써요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 300 / 803

← **이전**: [299. 페이지 폴트 처리 과정 (Page Fault Handling)](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/299_page_fault_handling/)
**다음**: [301. OPT (최적 교체)](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/301_opt_replacement/) →

---
