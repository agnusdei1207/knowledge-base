+++
title = "517. 거대 페이지 (Huge Page)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/) (Huge [Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/))는 기본 4KB [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)보다 훨씬 큰 2MB·1GB 단위로 가상 메모리를 매핑해, 같은 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) ([Translation Lookaside Buffer](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/)) 엔트리로 더 넓은 주소 공간을 덮게 만드는 번역 단위 최적화다.
> 2. **가치**: 메모리 집약 워크로드에서는 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 미스, [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 워크 ([Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Walk), [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 메모리 사용량을 함께 줄여 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/), [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/), [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 추론의 실효 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 끌어올린다.
> 3. **판단 포인트**: [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 이득은 "[페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 크다"보다 "크게 묶어도 되는 메모리인가"에 달려 있으며, 메모리 파편화, [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)·병합 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) ([Non-Uniform Memory Access](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/)) 배치, [Copy-on-Write](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/) 분할 비용을 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

[거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)는 운영체제가 기본 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)보다 훨씬 큰 단위로 가상 주소를 물리 메모리에 매핑하는 방식이다. 보통 범용 운영체제는 4KB [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 기본으로 쓰지만, 현대 서버는 수백 GB에서 수 TB까지 메모리를 다루므로 이 단위가 너무 잘게 느껴질 때가 많다. 이때 CPU (Central Processing Unit)는 실제 계산보다 주소 변환용 캐시를 찾고, 없으면 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)을 여러 단계 따라가는 데 더 많은 시간을 쓰게 된다.

문제의 본질은 메모리 용량 증가 속도와 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 커버리지 증가 속도가 같지 않다는 점이다. 예를 들어 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 엔트리 수가 같다면 4KB [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 몇 MB 수준만 덮지만, 2MB [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)는 같은 엔트리로 수 GB까지 덮을 수 있다. 특히 대형 버퍼 풀, 분석 엔진, 가상 머신 메모리처럼 넓고 연속적인 영역을 오래 쓰는 워크로드에서는 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽기 전 주소 변환부터 막히는" 현상이 더 두드러진다.

이 그림은 왜 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)가 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 문제를 먼저 겨냥하는지 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">페이지가 커질수록 같은 TLB가 덮는 범위가 넓어진다</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">TLB entries = 2,048 가정</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4KB page : 2,048 × 4KB = 8MB</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2MB page : 2,048 × 2MB = 4GB</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1GB page : 2,048 × 1GB = 2TB</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">메모리는 TB급으로 커졌는데 TLB 엔트리 수는 크게 늘지 않는다</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 페이지를 크게 묶지 않으면 주소 변환이 먼저 병목이 된다</div></div>
</div>
</div>



즉 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)는 메모리를 더 많이 만드는 기술이 아니라, <strong>주소 변환의 관리 단위를 굵게 만들어 번역 비용을 줄이는 기술</strong>이다. 이 관점을 잡아야 이후의 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/), [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/), 메모리 파편화 이슈가 하나로 묶인다.

- **📢 섹션 요약 비유**: [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)는 도시 지도를 작은 블록 단위 대신 큰 구역 단위로 보는 것과 같다. 골목 하나하나는 덜 자세하지만, 넓은 지역을 훨씬 빨리 찾을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)의 핵심은 번역 계층을 일부 건너뛰고, 한 번의 번역으로 더 많은 바이트를 대표하게 만드는 것이다. x86-64 4단계 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)을 기준으로 보면 4KB [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 `PML4 → PDPT → PD → PT → Frame` 경로를 따라가지만, 2MB [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 `PD` 엔트리에서 `PS (Page Size)` 비트를 세워 `PT` 단계를 건너뛴다. 1GB [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 `PDPT` 단계에서 바로 큰 프레임을 가리켜 하위 테이블을 더 많이 생략한다.

이 차이는 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 워크 횟수와 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 메모리 사용량을 동시에 바꾼다. 예를 들어 1GB 영역을 4KB [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)로 매핑하면 262,144개의 엔트리가 필요하지만, 2MB [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)면 512개, 1GB [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)면 사실상 1개 엔트리로 표현된다. 따라서 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)는 "[TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 미스가 줄어든다"에 그치지 않고, **미스가 났을 때 뒤지는 장부 자체도 훨씬 얇아진다**.

| 메커니즘 | [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)에서 일어나는 일 | 직접 효과 | 숨은 비용 |
| :--- | :--- | :--- | :--- |
| 번역 단위 확대 | 한 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 엔트리가 2MB·1GB 영역 대표 | [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) reach 급증 | 무효화·[보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 변경 단위도 커짐 |
| [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 축소 | 하위 테이블 일부 생략 | [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 워크 단축, [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 감소 | 세밀한 매핑 제어 약화 |
| 연속 메모리 확보 | 큰 물리 메모리 덩어리 필요 | 장기 버퍼에 유리 | 파편화 시 할당 실패 가능 |
| [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 병합·분할 | 작은 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 큰 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)로 승격, 필요 시 다시 분할 | 자동 최적화 가능 | 승격·분할 순간 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 발생 |

운영체제는 보통 두 방식으로 이를 제공한다. 하나는 부팅 시점이나 관리자가 미리 큰 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 풀을 예약해 두는 명시적 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)이고, 다른 하나는 THP (Transparent [Huge Pages](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/))처럼 커널이 4KB [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)들을 관찰하다가 조건이 맞으면 자동으로 2MB [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)로 승격하는 방식이다. 전자는 예측 가능성이 높고, 후자는 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 쉽지만 병합·[압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 시점의 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 변동을 동반할 수 있다.

핵심 공식은 단순하다. <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/">TLB</a> Reach = <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/">TLB</a> 엔트리 수 × <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/352_page_size/">페이지 크기</a></strong>. [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)는 이 식의 오른쪽 항 하나를 크게 만들어, 주소 변환 구조 전체를 유리하게 바꾼다.

- **📢 섹션 요약 비유**: [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)는 서류철을 낱장 대신 묶음 단위로 관리하는 것과 같다. 찾을 때는 빨라지지만, 중간 한 장만 수정하려면 다시 묶음을 풀어야 할 수 있다.

---

## Ⅲ. 비교 및 연결

[거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)는 "무조건 큰 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 최고"라는 단순 선택이 아니다. 실제로는 기본 4KB, 자동 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/), 명시적 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)가 서로 다른 장단점을 가진다. 중요한 비교 축은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 그 자체보다 <strong>예측 가능성, 메모리 유연성, 운영 복잡도</strong>다.

| 방식 | 장점 | 약점 | 잘 맞는 환경 |
| :--- | :--- | :--- | :--- |
| 기본 4KB [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) | 세밀한 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)·[스와핑](/knowledge-base/studynote/02_operating_system/06_memory_management/335_swapping/)·[Copy-on-Write](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/) 제어 | [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) reach 낮음, [page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) walk 많음 | 범용 앱, 짧은 프로세스, 메모리 변동 큰 환경 |
| THP (Transparent [Huge Pages](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)) | 애플리케이션 수정 없이 자동 이득 가능 | 병합·분할·[압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 시 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 변동 | [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 중심 서버, 일반 분석 워크로드 |
| 명시적 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/) | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 예측 가능, 장기 고정 버퍼에 강함 | 사전 예약 필요, 유휴 메모리 낭비 가능 | [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/), [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플레인 개발 키트 ([DPDK](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/671_dpdk/)), 대형 자바 가상 머신 (JVM) |

이 주제는 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)와 특히 강하게 연결된다. EPT (Extended [Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Tables)나 NPT (Nested [Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Tables)를 쓰는 가상 머신은 게스트와 호스트 양쪽 번역 계층을 함께 지나가므로, 기본 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)만 고집하면 중첩 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 워크 비용이 빠르게 커진다. 반대로 게스트 메모리와 호스트 메모리 모두에서 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)를 잘 쓰면, 번역 계층이 얕아져 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 오버헤드를 눈에 띄게 줄일 수 있다.

또한 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 환경에서는 "큰 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)"보다 "가까운 큰 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)"가 더 중요하다. 2MB [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)라도 다른 소켓의 원격 메모리에 놓이면, [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 이득을 일부 얻더라도 원격 접근 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 상쇄할 수 있다. 즉 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)는 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 기술이면서 동시에 메모리 배치 기술이기도 하다.

- **📢 섹션 요약 비유**: 4KB는 낱권 책, THP는 사서가 자동으로 묶어 주는 합본, 명시적 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)는 출판사에서 미리 전집 세트를 주문하는 것과 같다. 무엇이 좋은지는 독서 방식과 보관 공간에 따라 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)는 "켜면 빨라진다"보다 "어떤 메모리 영역에만 크게 묶는 것이 맞는가"로 접근해야 한다. 대형 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [버퍼 캐시](/knowledge-base/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/), 인메모리 [키-값 저장소](/knowledge-base/studynote/14_data_engineering/01_infrastructure/036_key_value/), [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)의 게스트 메모리, 장기 유지되는 분석 배열처럼 크고 오래 살아 있는 영역은 대표적인 적합 대상이다. 반대로 `fork()`가 잦거나, Copy-on-Write가 빈번하거나, 메모리 점유가 요동치는 서비스에서는 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/) 분할과 회수가 오히려 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)의 원인이 될 수 있다.

특히 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 민감형 서비스에서는 THP를 기본으로 켜기보다 `madvise` 방식이나 명시적 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)를 검토하는 경우가 많다. 이유는 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 평균값보다 tail latency가 더 중요하기 때문이다. 자동 병합 스레드가 백그라운드에서 메모리를 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)하거나 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/) 승격을 시도하는 순간, 예측하지 못한 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) [스파이크](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/129_spike_agile_technical_investigation/)가 나타날 수 있다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. `dTLB-load-misses`, [page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) walk 관련 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 카운터가 실제 병목으로 확인되는가?
2. 대상 메모리 영역이 크고, 오래 살아 있고, 연속 접근 비중이 높은가?
3. [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 노드 배치와 부팅 시점 예약으로 충분한 연속 메모리를 확보할 수 있는가?
4. [스와핑](/knowledge-base/studynote/02_operating_system/06_memory_management/335_swapping/), 메모리 풍선 확장, [Copy-on-Write](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/), [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) 분할 비용을 감당할 수 있는가?
5. 평균 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)이 중요한가, 아니면 예측 가능한 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 더 중요한가?

### 피해야 할 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 메모리 파편화가 심한 장시간 가동 서버에 1GB [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 즉흥적으로 강제하는 운영
- THP를 켠 뒤 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) [스파이크](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/129_spike_agile_technical_investigation/) 원인을 측정하지 않고 "커널이 알아서 해 줄 것"이라 가정하는 판단
- [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/) 이득만 보고 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 원격 배치나 [Copy-on-Write](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/) 분할 비용을 무시하는 설계

- **📢 섹션 요약 비유**: [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/) 적용은 큰 화물 컨테이너를 쓰는 물류 설계와 같다. 장기적으로 대량 화물에는 유리하지만, 자주 뜯고 다시 싸야 하는 소포 업무에는 오히려 불편하다.

---

## Ⅴ. 기대효과 및 결론

[거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)를 올바르게 적용하면 CPU가 주소 변환에 허비하는 시간을 줄이고, [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)도 줄여 메모리 계층 전체를 더 효율적으로 쓸 수 있다. 그래서 같은 코어 수, 같은 메모리 용량에서도 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/), 가상 머신 밀도, 분석 워크로드의 실효 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)이 눈에 띄게 좋아질 수 있다.

하지만 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)는 만능 스위치가 아니다. [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 커질수록 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 단위, [스와핑](/knowledge-base/studynote/02_operating_system/06_memory_management/335_swapping/) 단위, 분할 비용도 함께 커지므로 유연성은 줄어든다. 앞으로의 방향은 "모든 곳을 크게"가 아니라, 혼합 [페이지 크기](/knowledge-base/studynote/02_operating_system/06_memory_management/352_page_size/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 자동 승격·강등 개선, 티어드 메모리와 [CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) ([Compute Express Link](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/)) 환경을 고려한 영역별 [페이지 크기](/knowledge-base/studynote/02_operating_system/06_memory_management/352_page_size/) 최적화로 갈 가능성이 크다.

결론적으로 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)는 <strong>메모리 용량 기술이 아니라 주소 변환 비용을 다루는 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 기술</strong>이다. 이 개념을 "[TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) reach를 넓히는 레버"로 기억하면, 왜 어떤 시스템은 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)로 빨라지고 어떤 시스템은 오히려 운영이 어려워지는지 자연스럽게 설명할 수 있다.

- **📢 섹션 요약 비유**: [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)는 창고 선반을 큰 박스 중심으로 다시 짜는 일과 같다. 자주 나가는 대량 물건은 빨라지지만, 작은 물건까지 전부 큰 박스에 넣으면 오히려 찾기 불편해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) ([Translation Lookaside Buffer](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/)) | [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)가 직접 겨냥하는 주소 변환 캐시다. |
| [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 워크 ([Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Walk) | [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)가 줄이려는 하드웨어 번역 탐색 과정이다. |
| THP (Transparent [Huge Pages](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)) | 커널이 자동으로 2MB [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 승격을 시도하는 대표 구현 방식이다. |
| HugeTLBfs | 명시적 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)를 예약·할당할 때 자주 쓰는 리눅스 인터페이스다. |
| EPT / NPT | [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 환경에서 [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/) 효과가 더 커지는 중첩 번역 구조다. |
| [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) ([Non-Uniform Memory Access](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/)) | [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 실제로 살아나려면 함께 맞춰야 하는 메모리 배치 조건이다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">기본 4KB 페이지 중심 가상 메모리</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">메모리 용량 증가 · TLB reach 한계</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">거대 페이지 (2MB / 1GB)</div>
<div class="kb-diagram-tree-item" style="--depth:4">▶ THP (Transparent Huge Pages)</div>
<div class="kb-diagram-tree-item" style="--depth:4">▶ 명시적 HugeTLBfs 예약</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">가상화 EPT / NPT 최적화</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">혼합 페이지 크기 정책 · 티어드 메모리 · CXL 시대의 영역별 최적화</div>
</div>
</div>



이 흐름은 "세밀한 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 관리"에서 출발해, "번역 비용 절감"을 거쳐, 결국 워크로드별로 [페이지 크기](/knowledge-base/studynote/02_operating_system/06_memory_management/352_page_size/)를 다르게 쓰는 방향으로 발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)는 작은 공책 여러 권 대신 큰 스케치북 한 권으로 그림을 정리하는 것과 같아요.
2. 한 번에 넓은 내용을 볼 수 있어서 찾기는 빨라지지만, 한쪽 구석만 고치려면 조금 번거로워질 수 있어요.
3. 그래서 컴퓨터는 큰 그림을 오래 볼 때만 큰 스케치북을 쓰는 게 더 똑똑하답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 517 / 803

← **이전**: [516. 이종 컴퓨팅 메모리 공유 (Heterogeneous Memory Sharing)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/516_heterogeneous_memory_sharing/)
**다음**: [518. TLB 슈팅다운 (TLB Shootdown)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/518_tlb_shootdown/) →

---
