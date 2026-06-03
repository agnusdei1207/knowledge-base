+++
title = "298. 페이지 부재 (Page Fault)"
date = 2026-04-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) ([Page Fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/))는 CPU (Central Processing Unit)가 참조한 가상 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 현재 RAM (Random Access Memory)에 없거나 접근 권한 조건을 만족하지 않을 때, 하드웨어가 OS ([Operating System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)로 제어를 넘기는 예외 경계다.
> 2. **가치**: 이 예외 덕분에 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 프로그램 전체를 미리 적재하지 않고도 필요한 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)만 늦게 불러오는 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/) ([Demand Paging](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/))을 실현할 수 있다.
> 3. **판단 포인트**: [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) 자체는 정상 동작일 수 있지만, Major Fault가 잦아져 디스크 I/O (Input/Output)가 폭증하면 곧바로 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 악화와 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) ([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/))으로 이어진다.

---

## Ⅰ. 개요 및 필요성

[페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) ([Page Fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/))는 프로세스가 접근한 가상 주소가 지금 당장 물리 메모리에서 해석되지 않을 때 발생하는 하드웨어 예외다. 많은 초보자가 이를 "프로그램 오류"로만 이해하지만, [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 시스템에서는 오히려 정상적인 적재 요청 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)로 더 자주 등장한다. 즉, [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)는 메모리 관리가 실패했다는 뜻이 아니라, 아직 올리지 않은 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 이제 올리라는 통보다.

이 개념이 필요한 이유는 프로그램의 전체 주소 공간과 실제 순간 사용량이 크게 다르기 때문이다. 예를 들어 2 GB 애플리케이션이라도 실행 직후 실제로 자주 접근하는 코드는 일부 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화 루틴과 라이브러리의 몇 개 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)에 불과하다. 모든 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 시작 시점에 RAM에 적재하면 메모리 낭비와 긴 시작 시간이 함께 발생하므로, [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 "필요할 때만 올린다"는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 택한다.

[페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)가 없으면 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)도 성립하지 않는다. [MMU](/knowledge-base/studynote/02_operating_system/06_memory_management/328_mmu/) ([Memory Management Unit](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/284_mmu/))는 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)의 Present Bit나 Valid Bit를 보고 현재 적재 여부를 판단하고, 없는 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 만났을 때 CPU를 그냥 진행시키지 않고 반드시 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 알려야 한다. 이 경계가 있어야만 물리 메모리보다 큰 프로세스도 실행할 수 있고, 여러 프로세스가 한정된 RAM을 나눠 쓰는 멀티프로그래밍도 가능해진다.

- **📢 섹션 요약 비유**: [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)는 도서관 열람실에서 책 번호를 적어 냈는데 서가에 책이 없어서, 사서가 보관창고에서 책을 꺼내 오도록 요청표를 넘기는 순간과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)는 "주소 변환 실패 → [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 개입 → 적재 또는 종료 → 명령 재시작"의 흐름으로 처리된다. 이때 핵심은 CPU, [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) ([Translation Lookaside Buffer](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/)), [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/), 저장장치, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 역할 분담이다. 하드웨어는 예외를 감지하고 넘겨주며, 실제 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 수행한다.

아래 그림은 [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)가 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목이 되는 위치를 함께 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">페이지 부재 처리 흐름: 계산보다 대기 비용이 큼</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CPU 명령 실행</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">가상 주소 생성</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">TLB 조회 ── miss ──▶ 페이지 테이블 조회</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ Present=1, 권한 OK ▶ 계속 실행</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ Present=0 또는 권한 위반</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Trap to OS Kernel</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">주소 불법 확인 빈 Frame 확보 디스크 읽기</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">또는 권한 검사 또는 Victim 선정 (Swap/File)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">페이지 테이블 엔트리/ TLB 갱신 후 재시작</div></div>
</div>
</div>



실제 처리 절차는 보통 다음 순서를 따른다. 첫째, MMU가 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 엔트리의 적재 상태와 권한 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 확인한다. 둘째, Present Bit가 0이면 [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) 트랩이 발생하고, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 이 접근이 유효한 주소 범위인지부터 확인한다. 셋째, 적법한 접근이라면 빈 프레임을 찾거나 [페이지 교체 알고리즘](/knowledge-base/studynote/02_operating_system/07_virtual_memory/401_page_replacement_algorithms/)으로 희생 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 정한다. 넷째, [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) ([Solid State Drive](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))나 스왑 영역, 또는 실행 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에서 해당 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 읽어 온다. 다섯째, [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)과 TLB를 갱신한 뒤, 중단된 명령을 다시 실행한다.

| 유형 | 의미 | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 특성 | [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 대응 |
| :--- | :--- | :--- | :--- |
| Minor Fault | [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 이미 메모리 어딘가에 있으나 현재 매핑만 없음 | 비교적 짧음 | [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 매핑만 보완 |
| Major Fault | 실제 저장장치 읽기가 필요한 경우 | 매우 김 | 디스크 I/O 후 재개 |
| Invalid / [Protection](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) Fault | 주소가 잘못되었거나 권한 위반 | [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)보다 종료 가능성 큼 | 프로세스 예외 처리 또는 종료 |

핵심 병목은 Major Fault다. RAM 접근이 대략 수십~수백 ns (nanosecond) 수준인데 비해 [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 접근은 수십~수백 μs (microsecond), [HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) (Hard Disk Drive)는 ms (millisecond) 단위까지 늘어난다. 즉 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 하나를 잘못 만나면 CPU 입장에서는 수만 배에서 수십만 배 긴 대기 시간이 생긴다. 그래서 [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)의 본질은 "주소 변환 예외"이면서 동시에 "[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 뒤흔드는 저장장치 왕복"이다.

- **📢 섹션 요약 비유**: [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) 처리는 주방에 없는 재료를 창고에서 가져오는 일과 같아서, 주문 자체는 1초면 읽지만 창고 왕복이 길면 요리사는 손이 아니라 발로 일하게 된다.

---

## Ⅲ. 비교 및 연결

[페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)를 제대로 이해하려면 캐시 미스 (Cache Miss), [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) 오류 ([Segmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) Fault), [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)을 함께 봐야 경계가 선명해진다. 셋 다 "필요한 데이터나 권한이 지금 없다"는 점에서는 비슷하지만, 발생 계층과 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 방식이 완전히 다르다. 이 차이가 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 장애 해석의 기준이 된다.

| 비교 항목 | 캐시 미스 | [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) | [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) 오류 |
| :--- | :--- | :--- | :--- |
| 발생 계층 | CPU 캐시 ↔ RAM | RAM ↔ 보조기억장치 | 가상 주소 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 경계 |
| 주된 처리 주체 | 하드웨어 | 하드웨어 + OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) | OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) |
| 정상 동작 여부 | 매우 정상적 | 정상일 수도 있음 | 대체로 비정상 |
| 대표 비용 | 수십~수백 사이클 | 수천~수백만 사이클 | [프로세스 종료](/knowledge-base/studynote/02_operating_system/02_process_thread/107_process_termination/) 가능 |

캐시 미스는 대부분 하드웨어만으로 조용히 처리되지만, [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드 전환이 필요하다. 따라서 둘 다 "미스"이지만 시스템 전체 비용 차이가 압도적으로 크다. 반대로 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) 오류는 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)용 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 적재가 아니라 잘못된 주소 접근 자체를 문제로 보기 때문에, [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 가져와 해결하는 방향으로 가지 않는다.

또한 [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)는 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/), [참조의 지역성](/knowledge-base/studynote/02_operating_system/04_synchronization/253_locality_of_reference/) (Locality), [페이지 교체 알고리즘](/knowledge-base/studynote/02_operating_system/07_virtual_memory/401_page_replacement_algorithms/)과 강하게 연결된다. 지역성이 좋으면 한 번 적재한 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 오래 재사용하므로 [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)율이 낮아지고, 지역성이 깨지면 워킹셋 ([Working Set](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/))이 메모리보다 커져 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)이 시작된다. 즉 [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)는 단독 개념이 아니라, [메모리 계층 구조](/knowledge-base/studynote/02_operating_system/04_synchronization/252_memory_hierarchy/) 전체가 얼마나 잘 맞물리는지를 보여 주는 관찰 지표다.

- **📢 섹션 요약 비유**: 캐시 미스가 책상 서랍에서 펜을 찾는 정도라면, [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)는 창고까지 내려가는 일이고, [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) 오류는 애초에 남의 사물함을 억지로 열려는 행동에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)를 "발생 여부"보다 "어떤 종류가 얼마나 자주 발생하는가"로 봐야 한다. 애플리케이션 시작 직후 라이브러리와 코드 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 순차적으로 적재되며 Minor Fault와 일부 Major Fault가 보이는 것은 자연스럽다. 하지만 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 안정화 이후에도 Major Fault가 계속 높다면, 이는 메모리 부족·비정상적인 메모리 접근 패턴·과도한 [메모리 맵 파일](/knowledge-base/studynote/02_operating_system/02_process_thread/131_mmap_ipc/) 사용을 의심해야 한다.

대표적인 판단 사례는 두 가지다. 첫째, 대용량 분석 작업에서 CPU 사용률은 낮은데 디스크 대기 시간이 높고 응답이 끊긴다면, 실제 계산보다 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 교체하고 재적재하는 데 시간을 쓰는 상황일 수 있다. 둘째, 실시간 제어 시스템이나 초저지연 거래 시스템에서는 단 한 번의 Major Fault도 치명적이므로, 핵심 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 잠그는 메모리 고정 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 워밍업 절차가 필요하다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. `vmstat`, `sar`, `perf`, `/proc/<pid>/stat` 등에서 Major Fault가 지속적으로 증가하는가?
2. 워킹셋이 물리 메모리보다 커서 스왑 인/아웃이 반복되는가?
3. [메모리 맵 파일](/knowledge-base/studynote/02_operating_system/02_process_thread/131_mmap_ipc/) (`mmap`) 사용이 많다면 접근 패턴이 순차적인가, 무작위적인가?
4. [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 민감 시스템이라면 `mlock` 또는 사전 적재로 [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) 가능성을 제거했는가?

### 피해야 할 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 스왑 공간이 있으니 RAM 부족을 감수해도 된다고 판단하는 것
- 장애 분석에서 [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)와 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) 오류를 같은 범주로 오해하는 것
- [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 워밍업 구간의 정상적 Minor Fault와 운영 중 Major Fault 폭증을 구분하지 않는 것

기술사 답안 관점에서는 "[페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)는 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)의 필수 메커니즘이지만, 과도한 Major Fault는 설계 실패 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)"라고 정리하면 좋다. 즉 채택 여부의 문제가 아니라, [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)가 드물고 예측 가능하도록 워킹셋과 적재 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 관리하는 것이 핵심 판단이다.

- **📢 섹션 요약 비유**: [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) 관리는 창고 물류 관리와 같아서, 가끔 창고를 다녀오는 것은 정상 운영이지만 손님이 올 때마다 매번 창고를 뛰면 그 가게는 이미 재고 배치에 실패한 것이다.

---

## Ⅴ. 기대효과 및 결론

[페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) 메커니즘이 잘 동작하면 시스템은 물리 메모리보다 훨씬 큰 주소 공간을 사용자에게 투명하게 제공할 수 있다. 그 결과 대형 프로그램도 필요한 부분만 적재하며 빠르게 시작하고, 여러 프로세스가 제한된 RAM을 효율적으로 공유할 수 있다. 이는 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)의 유연성과 경제성을 가능하게 하는 핵심 토대다.

반면 한계도 분명하다. [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)는 결국 저장장치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 시스템 안으로 끌어오므로, 지역성이 나쁜 워크로드나 메모리 과부하 환경에서는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 급격히 무너질 수 있다. 따라서 [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)는 "있어도 되는 예외"이지만, "자주 있어서는 안 되는 예외"로 기억해야 한다.

앞으로는 더 빠른 [NVMe](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) ([Non-Volatile Memory Express](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/)) 저장장치, 정교한 [프리페칭](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/280_prefetching/), 애플리케이션별 메모리 [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/), 메모리 계층 통합 기술이 [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) 비용을 줄여 갈 것이다. 그래도 본질은 변하지 않는다. [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)는 하드웨어와 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 협력해 메모리의 환상을 유지하는 순간이며, 시스템 설계자는 그 환상의 비용을 항상 함께 계산해야 한다.

- **📢 섹션 요약 비유**: [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)는 공연 뒤편의 무대 전환과 같아서 관객이 모르게 소품을 바꿔 주면 훌륭한 연출이지만, 전환이 너무 자주 길어지면 공연 자체가 끊겨 버린다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/) ([Demand Paging](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)) | [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)를 계기로 필요한 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)만 늦게 적재하는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 엔트리 ([Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) Entry) | Present [Bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/), 권한 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/), 프레임 번호로 부재 여부를 판정 |
| [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) ([Translation Lookaside Buffer](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/)) | 주소 변환 캐시이며, [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) 처리 후 갱신 대상 |
| [페이지 교체 알고리즘](/knowledge-base/studynote/02_operating_system/07_virtual_memory/401_page_replacement_algorithms/) ([Least Recently Used](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/), [Clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/) 등) | 빈 프레임이 없을 때 어떤 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 내보낼지 결정 |
| [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) ([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)) | [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)가 과도해져 CPU보다 교체·I/O가 지배하는 상태 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">가상 메모리 (Virtual Memory)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">요구 페이징 (Demand Paging)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">페이지 부재 (Page Fault)</div>
<div class="kb-diagram-tree-item" style="--depth:2">▶ Minor Fault</div>
<div class="kb-diagram-tree-item" style="--depth:2">▶ Major Fault</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">페이지 교체 알고리즘 (Least Recently Used / Clock)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">워킹셋 (Working Set) · 스래싱 (Thrashing) 관리</div>
</div>
</div>



이 흐름은 "[가상 주소 공간](/knowledge-base/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/) 제공 → 필요 시 적재 → 부재 발생 → 교체 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 선택 → [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 안정화"라는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 메모리 관리 흐름을 압축한다.

### 👶 어린이를 위한 3줄 비유 설명

1. [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)는 읽고 싶은 책이 책상 위에 없어서 창고에서 가져와야 하는 순간이에요.
2. 창고가 멀면 오래 기다려야 하니까, 자주 보는 책은 책상 가까이에 두는 게 중요해요.
3. 컴퓨터도 똑같이, 자주 쓰는 데이터는 메모리에 두고 없으면 그때 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 가져다준답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 298 / 803

← **이전**: [297. 요구 페이징 (Demand Paging)](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/297_demand_paging/)
**다음**: [299. 페이지 폴트 처리 과정 (Page Fault Handling)](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/299_page_fault_handling/) →

---
