+++
title = "297. 요구 페이징 (Demand Paging)"
date = 2026-04-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/) ([Demand Paging](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/))은 프로세스 전체를 미리 적재하지 않고, 실제 접근이 발생한 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) ([Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/))만 그 순간 물리 메모리로 가져오는 <strong><a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a> 적재 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>이다.
> 2. **가치**: 이 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 비싼 주기억장치 자원을 현재 필요한 작업에 집중시켜, 더 많은 프로세스를 동시에 실행하고 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 구동 시간을 줄이게 만든다.
> 3. **판단 포인트**: 성패는 결국 [참조의 지역성](/knowledge-base/studynote/02_operating_system/04_synchronization/253_locality_of_reference/) (Locality)과 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) ([Page Fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)) 비용의 균형에 달려 있으며, 지역성이 무너지면 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 곧바로 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) ([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/))으로 추락한다.

---

## Ⅰ. 개요 및 필요성

[요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/) ([Demand Paging](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/))은 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) ([Virtual Memory](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)) 환경에서 <strong>"필요해질 때까지 올리지 않는다"</strong>는 원칙으로 동작하는 메모리 적재 방식이다. 전통적인 전체 적재 방식은 실행 전에 코드, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 라이브러리까지 한꺼번에 메모리에 올리므로 준비 시간도 길고, 실제로 거의 쓰지 않는 영역까지 주기억장치를 점유한다. 반면 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 사용 빈도가 높은 일부 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)만 먼저 살아 있게 두고, 아직 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)되지 않은 영역은 보조기억장치에 남겨 둔다.

이 방식이 필요해진 이유는 프로그램의 실제 사용 패턴이 매우 편중되어 있기 때문이다. 문서 편집기 전체가 500MB여도 사용자가 지금 당장 반복해서 쓰는 기능은 입력, 저장, 화면 갱신 같은 작은 부분에 집중된다. 즉 프로그램은 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로는 크지만, 순간적으로 뜨거운 작업 집합은 작다. [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 이 편중성을 이용해 같은 16GB 물리 메모리에서도 더 많은 프로세스를 살려 두고, 시스템의 멀티프로그래밍 정도 ([Degree of Multiprogramming](/knowledge-base/studynote/02_operating_system/04_synchronization/258_degree_of_multiprogramming/))를 높인다.

아래 그림은 "실행 전에 모두 싣는 방식"과 "접근 시점에 싣는 방식"의 차이를 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">전체 적재 vs 요구 페이징의 자원 사용 방식</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">구분</div><div class="kb-diagram-cell">전체 적재</div><div class="kb-diagram-cell">요구 페이징</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">시작 시 메모리 사용</div><div class="kb-diagram-cell">프로그램 전체</div><div class="kb-diagram-cell">초기 필요 페이지 일부</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">초기 실행 지연</div><div class="kb-diagram-cell">큼</div><div class="kb-diagram-cell">작음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">안 쓰는 코드의 점유</div><div class="kb-diagram-cell">그대로 유지</div><div class="kb-diagram-cell">접근 전까지 미적재</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">메모리 압박 시 확장성</div><div class="kb-diagram-cell">낮음</div><div class="kb-diagram-cell">상대적으로 높음</div></div>
</div>
</div>



핵심은 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)이 메모리를 공짜로 늘려 주는 기술이 아니라, <strong>당장 필요한 것과 나중에 필요한 것을 시간적으로 분리</strong>하는 기술이라는 점이다. 따라서 이 기법은 메모리 부족 자체를 없애는 해법이 아니라, 제한된 메모리를 더 영리하게 나누는 운영 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 이해해야 한다.

- **📢 섹션 요약 비유**: [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 이삿날 모든 짐을 한 번에 방 안에 쌓아 두는 대신, 오늘 바로 쓸 침대와 책상만 먼저 들여놓는 방식과 같다. 방은 덜 복잡해지고 생활은 빨리 시작되지만, 나중에 필요해진 짐은 창고에서 다시 가져와야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)이 동작하려면 중앙처리장치 (Central Processing Unit), 메모리 관리 장치 ([Memory Management Unit](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/284_mmu/)), [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) ([Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)), [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) ([Operating System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)), 그리고 백킹 스토어 (Backing Store)가 역할을 나눠 가져야 한다. 중앙처리장치가 가상 주소를 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하면 메모리 관리 장치는 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 엔트리 ([Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) Entry)를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다. 이때 해당 엔트리에 존재 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 또는 유효 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 "없음"으로 표시되어 있으면, 하드웨어는 이를 정상 접근이 아닌 <strong>적재 요청 이벤트</strong>로 해석해 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)를 발생시킨다.

| 구성 요소 | 하는 일 | 설계상 중요 포인트 |
| :-- | :-- | :-- |
| 메모리 관리 장치 ([Memory Management Unit](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/284_mmu/)) | 가상 주소를 해석하고 적재 여부 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 판정 속도, 변환 [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/) |
| [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 엔트리 ([Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) Entry) | 프레임 번호와 존재 여부 기록 | Present/Valid, Dirty, [Reference](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) |
| 자유 프레임 목록 (Free Frame List) | 비어 있는 물리 프레임 제공 | 부족 시 교체 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)과 연동 |
| 백킹 스토어 (Backing Store) | 아직 메모리에 없는 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 보관 | 디스크 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간이 전체 비용 좌우 |
| [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 핸들러 | 적재·갱신·재실행 수행 | 예외 처리 순서와 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |

이 그림은 "주소 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) → 부재 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) → 적재 → 재실행"의 시간을 따라가며 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)의 실제 흐름을 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">요구 페이징의 동작 시퀀스</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. CPU references virtual address</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. MMU checks page table entry</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Present=1 ▶ 바로 접근</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Present=0</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. Page Fault trap to OS</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. OS finds free frame or selects victim page</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">5. Disk/SSD reads missing page into RAM</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">6. Page table updated + instruction restarted</div></div>
</div>
</div>



여기서 중요한 것은 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)가 곧바로 실패를 뜻하지 않는다는 점이다. [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)에서 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)는 오히려 "이제 이 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 필요하다"는 신호다. 다만 그 비용이 크다. 메모리 접근이 대략 수십~수백 나노초 (ns) 수준이라면, 저장장치 접근은 수십 마이크로초 (μs)에서 밀리초 (ms)까지 늘어날 수 있다. 즉 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 <strong>평소에는 절약하고, 필요 시 크게 지불하는 구조</strong>다.

또 하나의 핵심은 적재 자체보다 <strong>재실행의 투명성</strong>이다. [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 필요한 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 올린 뒤 중단되었던 명령을 다시 실행해, 사용자와 프로세스 입장에서는 마치 처음부터 메모리에 있었던 것처럼 보이게 해야 한다. 이 투명성이 깨지면 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)의 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 자체가 무너진다.

- **📢 섹션 요약 비유**: [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 도서관 서고 시스템과 같다. 서가에 없는 책을 찾으면 사서가 창고에서 가져다주고, 독자는 잠깐 기다린 뒤 같은 자리에서 독서를 이어 간다. 중요한 것은 책을 가져오는 순간보다, 독서 흐름이 다시 자연스럽게 이어지게 만드는 운영 방식이다.

---

## Ⅲ. 비교 및 연결

[요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)을 제대로 이해하려면 [순수 요구 페이징](/knowledge-base/studynote/02_operating_system/07_virtual_memory/384_pure_demand_paging/) ([Pure Demand Paging](/knowledge-base/studynote/02_operating_system/07_virtual_memory/384_pure_demand_paging/))과 선행 적재 또는 프리페이징 ([Prepaging](/knowledge-base/studynote/02_operating_system/07_virtual_memory/385_prepaging/))을 함께 봐야 한다. [순수 요구 페이징](/knowledge-base/studynote/02_operating_system/07_virtual_memory/384_pure_demand_paging/)은 한 번도 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)되지 않은 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 절대 먼저 올리지 않으므로 메모리 낭비가 가장 적다. 반면 프리페이징은 곧 필요해질 가능성이 높은 인접 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 미리 가져와 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 연속 발생을 줄인다. 결국 차이는 <strong>예측 실패 비용을 감수하고 미리 준비할 것인가, 아니면 예측 없이 꼭 필요할 때만 지불할 것인가</strong>에 있다.

| 비교 항목 | [순수 요구 페이징](/knowledge-base/studynote/02_operating_system/07_virtual_memory/384_pure_demand_paging/) | 프리페이징 |
| :-- | :-- | :-- |
| [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 적재량 | 최소 | 상대적으로 큼 |
| 첫 접근 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)가 자주 발생 가능 | 완화 가능 |
| 메모리 낭비 위험 | 낮음 | 예측 실패 시 존재 |
| 적합한 상황 | 지역성이 강한 일반 워크로드 | 연속 스캔, 반복 실행 패턴 |

이 비교는 [참조의 지역성](/knowledge-base/studynote/02_operating_system/04_synchronization/253_locality_of_reference/)과 직접 연결된다. [시간적 지역성](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/247_temporal_locality/) ([Temporal Locality](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/247_temporal_locality/))이 강하면 한 번 가져온 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 반복해서 쓰므로 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)이 매우 효율적이다. [공간적 지역성](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/248_spatial_locality/) ([Spatial Locality](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/248_spatial_locality/))이 강하면 현재 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 주변이 곧 필요해질 가능성이 높아 프리페이징이나 읽기 선행이 효과를 낸다. 반대로 랜덤 접근이 많은 대용량 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 탐색이나 메모리 압박 아래의 과도한 [멀티태스킹](/knowledge-base/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/) 환경에서는 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)가 연쇄적으로 터지며, [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)의 이점이 급속히 사라진다.

[요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 또 다른 핵심 기술과도 연결된다. 변환 색인 버퍼 ([Translation Lookaside Buffer](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/))는 주소 변환 속도를 높여 주지만, [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 자체가 없으면 결국 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)를 막지 못한다. [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) 알고리즘은 메모리가 꽉 찼을 때 누구를 내보낼지 결정하고, 작업 집합 모델 ([Working Set Model](/knowledge-base/studynote/02_operating_system/07_virtual_memory/416_working_set_model/))은 현재 프로세스가 실제로 필요로 하는 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 범위를 추정한다. 즉 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 혼자 성립하는 기술이 아니라, <strong>주소 변환·교체 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>·스케줄링·디스크 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong>이 함께 받쳐 줄 때 비로소 효율을 낸다.

- **📢 섹션 요약 비유**: [순수 요구 페이징](/knowledge-base/studynote/02_operating_system/07_virtual_memory/384_pure_demand_paging/)은 손님이 주문할 때만 요리하는 식당이고, 프리페이징은 점심시간 인기 메뉴를 조금 미리 준비하는 식당이다. 손님 흐름을 잘 맞히면 둘 다 효율적이지만, 손님이 예측과 다르게 몰리면 주방은 바로 바빠진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 대개 "메모리를 아끼는 기술"보다 "어떤 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 어디까지 허용할 것인가"의 문제로 다뤄진다. 예를 들어 웹 애플리케이션 서버는 기동 직후 첫 요청이 느릴 수 있는데, 이는 아직 자주 쓰일 코드 경로와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 충분히 메모리에 올라오지 않았기 때문이다. 이런 경우 워밍업 요청을 미리 보내 주요 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 당겨 두면 사용자 체감 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 크게 줄일 수 있다. 반대로 [데이터베이스 관리 시스템](/knowledge-base/studynote/05_database/01_db_architecture_relational/003_dbms_database_management_system/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) System)은 자체 [버퍼 캐시](/knowledge-base/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/)를 강하게 운용하므로, [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)에 지나치게 의존하면 예측 불가능한 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 늘 수 있다.

### 기술사 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)가 대부분 경미한 부재 (Minor Fault)인지, 실제 저장장치 입출력 (Major Fault)을 동반하는지 구분했는가?
2. 저장장치가 비휘발성 메모리 익스프레스 ([Non-Volatile Memory Express](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/)) 기반 [솔리드 스테이트 드라이브](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/475_ssd_structure/) ([Solid State Drive](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))인지, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 큰 하드디스크 드라이브 (Hard Disk Drive)인지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)했는가?
3. 프로세스별 작업 집합이 물리 메모리 안에 유지되는지, 아니면 교체와 재적재가 반복되는지 관찰했는가?
4. 실시간 제어, 고빈도 거래, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 민감 서비스처럼 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 자체를 허용하면 안 되는 구간이 있는가?

### 대표 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 물리 메모리 부족을 [스왑 공간](/knowledge-base/studynote/02_operating_system/07_virtual_memory/390_swap_space/) 확대만으로 해결하려는 판단
- [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 밀도를 높이기 위해 메모리 한계를 과도하게 낮춰 연속 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)를 유발하는 배치
- 첫 요청 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 문제를 애플리케이션 버그로만 보고, 실제 메모리 적재 패턴을 관찰하지 않는 운영

기술사 답안에서는 "[요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 항상 좋다"고 쓰면 부족하다. <strong>지역성이 뚜렷하고 <a href="/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> 적재 비용을 줄이고 싶을 때는 채택 가치가 크지만, <a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a> 상한이 엄격하거나 작업 집합이 물리 메모리를 자주 넘는 환경에서는 적극적인 메모리 고정, 프리페치, <a href="/knowledge-base/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/">버퍼 캐시</a> 설계가 더 중요하다</strong>고 판단해야 한다.

- **📢 섹션 요약 비유**: [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 냉장고가 작은 식당의 운영 비법이 될 수 있지만, 손님이 몰리는 시간에 재료를 계속 창고에서 가져와야 하면 오히려 장사가 망한다. 결국 중요한 것은 냉장고 크기보다 손님 패턴을 읽고, 어떤 재료는 미리 꺼내 둘지 결정하는 운영 감각이다.

---

## Ⅴ. 기대효과 및 결론

잘 설계된 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 세 가지 효과를 만든다. 첫째, [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 적재량을 줄여 프로그램 시작 체감을 개선한다. 둘째, 물리 메모리를 실제 사용 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 위주로 배분해 시스템 전체 처리량을 높인다. 셋째, [논리 주소](/knowledge-base/studynote/02_operating_system/06_memory_management/322_logical_virtual_address/) 공간이 물리 메모리보다 크더라도 프로그램이 동작할 수 있게 해 소프트웨어 설계 자유도를 넓힌다. 이 때문에 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 현대 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 기본값에 가깝다.

그러나 전제조건도 분명하다. 저장장치가 지나치게 느리거나, 지역성이 약하거나, 동시에 실행되는 프로세스의 작업 집합 합이 물리 메모리를 지속적으로 초과하면 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 즉시 병목으로 변한다. 비휘발성 저장장치가 빨라져도 메모리와 저장장치 사이의 속도 차는 여전히 크므로, [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)이 메모리 설계 문제를 근본적으로 없애 주지는 못한다.

따라서 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 "디스크를 메모리처럼 쓰는 마법"으로 기억하면 안 된다. 더 정확한 기억법은 <strong>"지역성을 믿고 메모리 적재 시점을 뒤로 미루는 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a>의 확률적 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>"</strong>이다. 이 관점으로 보면 왜 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)율, 작업 집합, 교체 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 저장장치 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 함께 중요해지는지도 자연스럽게 이해된다.

- **📢 섹션 요약 비유**: [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 작은 가방으로 긴 여행을 떠나는 기술이다. 짐을 적게 들고 빨리 출발할 수 있지만, 여행 동선이 엉키면 숙소와 보관함을 계속 오가느라 시간만 잃게 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) ([Virtual Memory](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)) | [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)를 현실적으로 구현하는 대표 적재 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이다. |
| [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) ([Page Fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)) | [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)이 필요한 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 불러오는 공식 진입 이벤트다. |
| [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) ([Page Replacement](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)) | 자유 프레임이 없을 때 어떤 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 내보낼지 결정해 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)의 지속 가능성을 좌우한다. |
| 작업 집합 ([Working Set](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)) | 현재 시점에 실제로 필요한 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 범위를 설명해 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)의 성공 여부를 가늠하게 한다. |
| [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) ([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)) | [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)이 지역성을 잃고 입출력 폭주 상태로 붕괴한 결과다. |
| 프리페이징 ([Prepaging](/knowledge-base/studynote/02_operating_system/07_virtual_memory/385_prepaging/)) | [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)의 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 줄이기 위해 일부 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 선제 적재하는 보완 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">전체 적재 중심 메모리 운영</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">가상 메모리 (Virtual Memory)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">요구 페이징 (Demand Paging)</div>
<div class="kb-diagram-tree-item" style="--depth:4">▶ 페이지 폴트 처리 (Page Fault Handling)</div>
<div class="kb-diagram-tree-item" style="--depth:4">▶ 페이지 교체 (Page Replacement)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">작업 집합 · 스래싱 제어 · 프리페이징</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">지연 민감 워크로드별 메모리 최적화</div>
</div>
</div>



이 흐름은 단순 적재에서 시작해, 필요한 순간만 적재하고, 이후에는 폴트 처리와 교체 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 작업 집합 제어까지 확장되는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 메모리 관리의 발전 축을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 학교에 갈 때 모든 책을 다 들고 가지 않고, 오늘 바로 볼 책만 먼저 챙기는 방법이에요.
2. 수업하다가 안 가져온 책이 필요하면 잠깐 책장에서 가져와야 해서 조금 기다리게 돼요.
3. 그래서 가방은 가벼워지지만, 자꾸 책장을 오가게 되면 오히려 공부 흐름이 끊길 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 297 / 803

← **이전**: [296. 페이징과 세그멘테이션 혼용 (Paging-Segmentation Hybrid)](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/296_paging_segmentation_hybrid/)
**다음**: [298. 페이지 부재 (Page Fault)](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/298_page_fault/) →

---
