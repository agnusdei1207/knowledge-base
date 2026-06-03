+++
title = "518. TLB 슈팅다운 (TLB Shootdown)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 슈팅다운 ([TLB Shootdown](/knowledge-base/studynote/02_operating_system/07_virtual_memory/435_tlb_shootdown/))은 한 코어가 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 매핑을 바꿨을 때, 같은 주소 공간을 실행 중인 다른 코어들의 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) ([Translation Lookaside Buffer](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/))에 남아 있는 낡은 번역 엔트리를 강제로 무효화하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 절차다.
> 2. **가치**: 해제된 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 재사용, 접근 권한 변경, [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 이동 같은 사건이 시스템 전체에 즉시 반영되어야 메모리 손상과 보안 오류를 막을 수 있으므로, [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 슈팅다운은 가상 메모리의 정확성을 지키는 마지막 안전장치다.
> 3. **판단 포인트**: 실제 비용은 `invalidate` 명령 자체보다 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 전달, 원격 코어 정지, 응답 대기, 이후의 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 재적재에 있으므로, 대상 코어 축소·범위 무효화·[배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)·하드웨어 브로드캐스트 지원 여부가 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이를 만든다.

---

## Ⅰ. 개요 및 필요성

[TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 슈팅다운은 멀티코어 시스템에서 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)된 주소 변환 캐시의 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 맞추기 위한 절차다. 각 코어는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 위해 자신의 TLB에 최근 가상 주소 → [물리 주소](/knowledge-base/studynote/02_operating_system/06_memory_management/323_physical_address/) 번역 결과를 따로 저장한다. 문제는 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)이 바뀌어도 다른 코어의 TLB는 자동으로 바뀌지 않는 경우가 많다는 점이다.

예를 들어 한 스레드가 `munmap()`으로 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 해제하거나 `mprotect()`로 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 권한을 제거했는데, 다른 코어의 TLB에 예전 번역이 남아 있다면 어떤 일이 생길까. 이미 다른 용도로 재할당된 물리 프레임을 계속 쓰거나, 더 이상 허용되지 않은 권한으로 접근하는 심각한 오류가 발생할 수 있다. 즉 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 슈팅다운은 "[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 보조 기능"이 아니라 <strong>정확성을 위해 반드시 필요한 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a> 절차</strong>다.

이 문제가 더 까다로운 이유는 주소 공간이 여러 코어에서 동시에 실행될 수 있기 때문이다. 멀티스레드 프로세스, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 전역 매핑, [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 환경에서는 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 변경이 곧 여러 코어의 로컬 상태를 동시에 흔든다. 그래서 슈팅다운은 메모리 관리 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 아니라, 사실상 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)처럼 다뤄야 한다.

- **📢 섹션 요약 비유**: [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 슈팅다운은 학교 시간표가 바뀌었을 때 모든 교실 벽의 옛 시간표를 동시에 떼어내는 일과 같다. 한 교실만 고쳐 놓으면 다른 교실 학생들은 여전히 잘못된 시간에 수업하러 간다.

---

## Ⅱ. 아키텍처 및 핵심 원리

전형적인 슈팅다운 경로는 네 단계로 이해하면 쉽다. 첫째, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 PTE ([Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) Entry)를 수정한다. 둘째, 해당 주소 공간을 현재 실행 중인 코어 집합을 찾는다. 셋째, 자기 코어의 TLB를 지운 뒤 나머지 코어에 IPI (Inter-Processor [Interrupt](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)) 또는 아키텍처 전용 무효화 명령을 보낸다. 넷째, 원격 코어가 `INVLPG`, `INVPCID`, `TLBI (TLB Invalidate)` 같은 무효화 명령을 실행하고 완료 응답을 보낸 뒤에야 원래 작업이 계속된다.

이 그림은 비용이 어디서 커지는지를 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">shootdown 비용은 flush보다 "모두 멈추고 맞추는 과정"에 있다</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Initiator Core Remote Core A Remote Core B</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PTE update run run</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">local invalidate</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">IPI / invalidate ▶ trap</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">flush local TLB</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">IPI / invalidate ▶ trap</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">done ▶</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">wait for all done</div><div class="kb-diagram-cell">flush local TLB</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">done ▶</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">resume only after every stale translation is gone</div></div>
</div>
</div>



| 단계 | 실제 작업 | 왜 비싼가 |
| :--- | :--- | :--- |
| 대상 선정 | 어떤 코어가 이 주소 공간을 실행 중인지 판별 | 대상을 넓게 잡을수록 불필요한 원격 정지가 늘어남 |
| 전달 | IPI 또는 브로드캐스트 무효화 전파 | [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 전달과 핸들러 진입 자체가 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 만듦 |
| 원격 정지 | 실행 중인 파이프라인을 멈추고 특권 모드 진입 | 사용자 코드가 끊기며 tail latency가 커짐 |
| 재적재 | 무효화 뒤 다시 [page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) walk로 번역을 채움 | flush 이후에도 한동안 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 하락이 이어짐 |

따라서 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 슈팅다운의 비용은 단순한 "지우기"가 아니라, <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/">페이지 테이블</a> 변경을 전역적으로 확정하는 회합 비용</strong>이다. 주소 하나만 바꿔도 대상 코어가 많고 무효화 범위가 넓으면 시스템 전체가 잠깐 흔들리는 이유가 여기에 있다.

- **📢 섹션 요약 비유**: [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 슈팅다운은 회의실 여러 곳에 붙은 공지문을 동시에 바꾸는 작업과 같다. 종이 한 장 바꾸는 시간보다, 모든 회의실 진행을 잠깐 멈추게 하고 "다 바꿨다"는 확인을 받는 시간이 더 오래 걸린다.

---

## Ⅲ. 비교 및 연결

[TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 슈팅다운은 [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/)과 비슷해 보이지만, 관리 대상과 수행 주체가 다르다. [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) ([Cache Coherence](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/))은 주로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 캐시 라인 최신성을 하드웨어가 맞추는 문제이고, [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 슈팅다운은 주소 변환 메타데이터를 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 명시적으로 무효화하는 문제다. 즉 둘 다 "낡은 사본 제거"를 다루지만, 자동화 수준과 비용 구조가 다르다.

| 항목 | [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) | [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 슈팅다운 |
| :--- | :--- | :--- |
| 대상 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 캐시 라인 | 주소 변환 엔트리 |
| 변화 원인 | 일반적인 읽기·[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) | [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 수정, 권한 변경, 매핑 해제 |
| 주 수행자 | 하드웨어 snoop / [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) | [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) + 아키텍처 무효화 명령 |
| 대표 비용 | coherence traffic, invalidation | IPI, 원격 정지, [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) refill |
| 확장 해법 | snoop filter, [directory](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) | [ASID](/knowledge-base/studynote/02_operating_system/06_memory_management/360_asid/)/PCID, range invalidate, hardware broadcast |

아키텍처별 차이도 중요하다. 전통적인 x86 계열은 IPI 기반 원격 무효화 비중이 높았고, ARM은 TLBI 계열 명령과 배리어를 통해 좀 더 구조화된 브로드캐스트 무효화를 제공해 왔다. 최근 x86도 `INVLPGB` 같은 [하드웨어 보조](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/527_hardware_assisted_virtualization/) 기능을 통해 원격 무효화 비용을 줄이려는 방향으로 진화하고 있다.

또한 [ASID](/knowledge-base/studynote/02_operating_system/06_memory_management/360_asid/) (Address Space [Identifier](/knowledge-base/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/))나 PCID (Process-Context [Identifier](/knowledge-base/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/))는 슈팅다운 대상을 줄이는 핵심 수단이다. 주소 공간 태그가 있으면 "이 번역이 어느 프로세스 소속인지"를 구분할 수 있어, 관련 없는 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 엔트리까지 통째로 비우지 않아도 된다. [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 환경에서는 여기에 EPT (Extended [Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Tables)나 NPT (Nested [Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Tables) 무효화가 겹쳐 비용이 더 증폭될 수 있다.

- **📢 섹션 요약 비유**: [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/)이 도서관 책 내용의 최신판을 맞추는 일이라면, [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 슈팅다운은 책이 꽂힌 서가 위치표를 고치는 일에 가깝다. 둘 다 중요하지만, 위치표는 사서가 직접 바꿔야 하는 경우가 많다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 슈팅다운 병목은 보통 "코어는 많은데 메모리 관리가 잦을수록 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 이상하게 떨어진다"는 형태로 나타난다. [JIT](/knowledge-base/studynote/09_security/11_iam_access_control/568_jit_access/) ([Just-In-Time](/knowledge-base/studynote/09_security/11_iam_access_control/568_jit_access/)) 컴파일러의 잦은 `mprotect()`, 고빈도 `mmap()/munmap()`, [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 마이그레이션, [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) ([Non-Uniform Memory Access](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/)) 재배치, [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/) 분할, [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 환경의 메모리 회수 작업은 모두 슈팅다운을 자주 유발할 수 있다. 이때 문제는 CPU (Central Processing Unit) 연산량이 아니라, [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 변경이 너무 잦아 <strong>전역 번역 캐시 <a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a>가 처리량을 갉아먹는 것</strong>이다.

해법의 방향은 세 가지다. 첫째, 변경 자체를 줄인다. 작은 버퍼를 매번 매핑·해제하지 말고 풀링하거나 [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)한다. 둘째, 무효화 범위와 대상을 줄인다. [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 단위 `invalidate` 대신 범위 기반 무효화와 [ASID](/knowledge-base/studynote/02_operating_system/06_memory_management/360_asid/)/PCID 태깅을 활용한다. 셋째, 하드웨어 지원을 쓴다. 아키텍처가 허용한다면 브로드캐스트 무효화나 더 정교한 태그 기반 유지 전략이 IPI 폭풍을 줄여 준다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 변경이 정말 빈번한가, 아니면 단순 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 미스가 많은 것인가?
2. 매핑 해제 작업을 배치해 한 번의 슈팅다운으로 묶을 수 있는가?
3. 해당 주소 공간을 실행 중인 코어만 정확히 추려서 무효화하고 있는가?
4. [ASID](/knowledge-base/studynote/02_operating_system/06_memory_management/360_asid/)/PCID, 범위 무효화, 하드웨어 브로드캐스트 같은 완화 수단을 지원하는가?
5. [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 환경이라면 게스트 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 무효화와 2단계 번역 무효화가 겹치지 않는가?

### 피해야 할 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 작은 메모리 구간을 자주 `mmap()/munmap()`하며 코어 수 증가 비용을 무시하는 설계
- 관련 없는 모든 코어에 무차별 IPI를 보내는 보수적 [무효화 정책](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/405_write_invalidate/)
- [거대 페이지](/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/)를 자주 쪼개고 다시 합치면서 슈팅다운 빈도와 범위를 동시에 키우는 운영

- **📢 섹션 요약 비유**: [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 슈팅다운 최적화는 쓰레기가 생길 때마다 전 직원 회의를 여는 대신, 한꺼번에 모아 처리하고 꼭 필요한 사람만 부르는 운영 방식과 같다.

---

## Ⅴ. 기대효과 및 결론

[TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 슈팅다운을 올바르게 이해하면, 멀티코어 시스템에서 왜 메모리 관리 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 곧 확장성 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 되는지 보인다. 같은 [메모리 보호](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/307_memory_protection/) 기능이라도 무효화 범위가 좁고 대상 코어가 정확할수록 처리량과 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 안정성이 함께 좋아진다. 반대로 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 변경을 가볍게 보면, 코어를 늘릴수록 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)와 재적재 비용이 더 빨리 폭증한다.

앞으로의 방향은 명확하다. 더 정교한 주소 공간 태깅, 범위 기반 `invalidate`, 하드웨어 브로드캐스트, 원격 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 가속이 계속 강화될 것이다. 결국 목표는 "정확성을 위해 다 멈추는 방식"에서 "정확성을 유지하되 멈추는 대상을 최소화하는 방식"으로 가는 것이다.

결론적으로 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 슈팅다운은 <strong>주소 변환 캐시를 위한 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a> <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a></strong>이다. 이 개념을 단순 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 기법이 아니라, [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 변경이 시스템 전체에 전파되는 비용 구조로 기억해야 멀티코어 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 문제를 제대로 읽을 수 있다.

- **📢 섹션 요약 비유**: [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 슈팅다운은 회사 조직도 변경 공지를 모든 부서 게시판에 반영하는 절차와 같다. 바꾸는 내용은 짧아도, 모든 부서가 옛 공지를 떼기 전에는 새 체계가 제대로 작동하지 않는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) ([Translation Lookaside Buffer](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/)) | 슈팅다운으로 직접 무효화되는 번역 캐시다. |
| PTE ([Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) Entry) | 변경이 발생하는 원본 메타데이터다. |
| IPI (Inter-Processor [Interrupt](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)) | 전통적 원격 무효화 전달 수단이다. |
| [ASID](/knowledge-base/studynote/02_operating_system/06_memory_management/360_asid/) / PCID | 슈팅다운 범위를 줄여 주는 주소 공간 태그다. |
| INVLPG / INVPCID / TLBI | 아키텍처별 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 무효화 명령군이다. |
| EPT / NPT | [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 환경에서 슈팅다운 비용을 증폭시키는 2단계 번역 구조다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">단일 코어의 로컬 TLB flush</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">멀티코어 공유 주소 공간</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">TLB 슈팅다운 (IPI 기반 원격 invalidate)</div>
<div class="kb-diagram-tree-item" style="--depth:4">▶ ASID / PCID 기반 대상 축소</div>
<div class="kb-diagram-tree-item" style="--depth:4">▶ range-based invalidate</div>
<div class="kb-diagram-tree-item" style="--depth:4">▶ hardware broadcast invalidate</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">가상화·many-core 시대의 확장형 번역 캐시 일관성</div>
</div>
</div>



이 흐름은 "내 코어만 지우면 되던 시대"에서 출발해, "여러 코어의 번역 캐시를 정밀하게 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)하는 시대"로 발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터는 각자 작은 메모장에 "이 주소는 여기로 가면 돼"라고 적어 두고 빨리 일해요.
2. 그런데 길이 바뀌었는데 어떤 친구 메모장에 옛 주소가 남아 있으면 엉뚱한 곳으로 가 버려요.
3. 그래서 한 친구가 길을 바꾸면 다른 친구들에게도 "옛 메모 지워!"라고 알려 주는 게 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 슈팅다운이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 518 / 803

← **이전**: [517. 거대 페이지 (Huge Page)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/517_huge_page/)
**다음**: [519. IOMMU 성능 오버헤드 (IOMMU Performance Overhead)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/519_iommu_overhead/) →

---
