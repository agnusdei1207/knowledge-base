+++
title = "350. 버스 마스터 (Bus Master)"
date = 2026-03-27

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터 ([Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) Master)는 시스템 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)에서 주소와 제어 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 먼저 내보내며 전송을 시작할 수 있는 주도 장치다.
> 2. **가치**: CPU (Central Processing Unit)만 전송을 지휘하던 구조에서 [DMA](/knowledge-base/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) ([Direct Memory Access](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/318_dma/)) 컨트롤러나 고성능 주변장치까지 마스터가 되면, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동을 CPU 계산과 분리해 병목을 줄일 수 있다.
> 3. **판단 포인트**: [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터링은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 높이지만, 동시에 [버스 중재](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/351_bus_arbitration/), [메모리 보호](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/307_memory_protection/), [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) 같은 통제 장치가 함께 있어야 안전하다.

---

## Ⅰ. 개요 및 필요성

[버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터 ([Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) Master)는 공유 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)에서 통신을 <strong>개시</strong>할 수 있는 장치다. 단순히 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 많이 보내는 장치가 아니라, 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)와 제어 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 잡고 "어디에 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 수행할지"를 먼저 선언할 수 있어야 마스터라고 부른다. 반대로 메모리나 일반 입출력 장치처럼 호출을 받아 응답만 하는 장치는 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 슬레이브 ([Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) Slave)다.

이 구분이 필요한 이유는 공유 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 본질적으로 한 번에 한 주체만 질서를 만들 수 있는 공용 자원이기 때문이다. 모두가 동시에 주소와 제어 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 내보내면 전기적 충돌이 발생하고, 아무도 먼저 시작하지 못하면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 자체가 멈춘다. 그래서 시스템은 "누가 말을 먼저 시작할 권한을 갖는가"를 하드웨어 수준에서 분리한다.

[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 구조에서는 CPU가 거의 유일한 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터였다. 이 경우 디스크에서 메모리로 4KB 블록을 옮길 때도 CPU가 읽고, 다시 쓰고, 또 다음 블록으로 넘어가는 식으로 전 과정을 감독해야 했다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 양이 커질수록 CPU는 계산보다 운반 업무에 시간을 더 쓰게 되고, 이 한계를 줄이기 위해 [DMA](/knowledge-base/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) 컨트롤러와 고성능 주변장치에 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터 권한을 위임하는 구조가 등장했다.

- **📢 섹션 요약 비유**: [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터는 창고에서 지게차를 직접 움직일 수 있는 현장반장과 같다. 반장이 있어야 어느 선반에서 어떤 박스를 꺼낼지 먼저 지시할 수 있고, 작업자들은 그 지시에 맞춰 물건을 전달한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터의 핵심 원리는 <strong>요청 → 승인 → 주소/명령 제시 → <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 전송 → 종료 통지</strong>의 흐름이다. 마스터 후보가 여러 개라면 먼저 [버스 중재](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/351_bus_arbitration/)기 ([Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) Arbiter)가 사용권을 정하고, 권한을 얻은 장치만 주소선과 제어선을 구동한다. 슬레이브는 자신에게 해당하는 주소를 감지한 뒤 읽기 또는 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 요청에 응답한다.

아래 그림은 멀티 마스터 환경에서 한 장치가 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 획득해 메모리에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쓰는 전형적 흐름을 보여 준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">버스 마스터의 전송 흐름: 개시 권한이 핵심</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">CPU</div><div class="kb-diagram-node">DMA</div><div class="kb-diagram-node">NIC</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Bus Request</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Bus Arbiter</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Bus Grant</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Selected Bus Master</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Address + Read/Write Command on System Bus</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Main Memory</div><div class="kb-diagram-node">I/O Device</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Data Bus</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">핵심: 데이터가 흐른다고 모두 마스터가 아니라, 주소/명령을 먼저 내는 쪽이 마스터</div></div>
</div>
</div>



이 구조에서 가장 중요한 점은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)보다 <strong>주소·제어 주도권</strong>이 더 본질적이라는 사실이다. 예를 들어 [DMA](/knowledge-base/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) 컨트롤러가 메모리에 연속 블록을 기록할 때, 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 외부 장치에서 들어오더라도 메모리 주소를 증가시키며 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 명령을 발행하는 주체는 [DMA](/knowledge-base/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) 컨트롤러다. 그래서 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터는 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 생산자"가 아니라 "전송의 지휘자"라고 이해하는 것이 정확하다.

| 구성 요소 | 역할 | 설계 포인트 |
| :-- | :-- | :-- |
| [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터 | 주소와 제어 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 발행해 전송 시작 | 독점 시간 최소화, [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)트 전송 효율 |
| [버스 중재](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/351_bus_arbitration/)기 ([Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) Arbiter) | 여러 마스터 요청 중 하나를 선택 | 우선순위와 공정성 균형 |
| [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 슬레이브 | 지정된 주소 요청에 응답 | 응답 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 대기 상태 처리 |
| [DMA](/knowledge-base/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) 컨트롤러 | CPU 대신 대량 블록 전송 수행 | 시작 주소·길이·완료 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) |
| [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) | 전송 완료를 CPU에 통지 | [폴링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) 오버헤드 감소 |

실제 시스템에서는 한 번 권한을 얻은 마스터가 여러 워드를 연속 전송하는 [버스트 모드](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/320_burst_mode/) ([Burst Mode](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/320_burst_mode/))를 자주 사용한다. 이는 중재 횟수를 줄여 대역폭을 높이지만, 너무 길게 독점하면 다른 마스터의 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간이 커진다. 결국 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터링은 단순 권한 부여가 아니라, <strong>얼마나 오래 점유하게 할 것인가</strong>까지 포함한 자원 관리 문제다.

- **📢 섹션 요약 비유**: [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터는 도로 위에서 차를 직접 모는 운전기사와 같다. 짐이 많다고 모두 운전기사가 되는 것은 아니고, 실제로 핸들과 방향지시등을 잡는 사람이 운전기사가 된다.

---

## Ⅲ. 비교 및 연결

[버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터를 이해하려면 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 슬레이브와의 차이, 그리고 CPU 단독 마스터 구조와 멀티 마스터 구조의 차이를 함께 봐야 한다. 핵심 경계는 "누가 먼저 전송을 시작할 수 있는가"와 "그 결과 시스템 병목이 어디로 이동하는가"에 있다.

| 비교 항목 | [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터 | [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 슬레이브 |
| :-- | :-- | :-- |
| 통신 시작 | 가능 | 불가 |
| 주소/제어 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) | 직접 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 수신 후 해석 |
| 대표 장치 | CPU, [DMA](/knowledge-base/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) 컨트롤러, 일부 [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) 장치 | 메인 메모리, [ROM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/255_rom/), 단순 주변장치 |
| 병목 영향 | 중재 경쟁 유발 가능 | 응답 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 병목으로 작용 |
| 설계 부담 | 중재·[보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)·[일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 고려 필요 | [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 응답 [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/) 중심 |

CPU만 마스터인 구조는 제어가 단순하다. 모든 전송이 CPU를 거치므로 디버깅과 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)는 쉽지만, 네트워크 수신·디스크 읽기·영상 스트리밍처럼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 많은 작업에서 CPU가 복사 노동에 묶인다. 반면 멀티 마스터 구조는 CPU 부하를 줄이고 병렬성을 높이지만, [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 경합, [우선순위 역전](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/205_priority_inversion/), 기아 현상 ([Starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/))을 함께 관리해야 한다.

현대 [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) ([PCI Express](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/)) 계열 인터커넥트에서는 전통적 "공유 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)"의 전기적 형태는 약해졌지만, 개념적으로는 여전히 마스터-슬레이브 역할이 남아 있다. 예를 들어 네트워크 카드나 스토리지 컨트롤러가 메모리 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 트랜잭션을 스스로 발행하면, 물리적으로는 점대점 링크를 쓰더라도 기능적으로는 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터링과 같은 철학을 따른다. 즉 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터는 특정 배선 구조의 이름이라기보다, <strong>전송 개시 권한의 주체</strong>를 설명하는 개념이다.

또한 이 개념은 운영체제의 입출력 경로와도 직결된다. PIO (Programmed Input/Output)는 CPU가 직접 장치를 읽고 쓰는 방식이므로 CPU 중심 마스터 구조에 가깝고, DMA는 장치 또는 [DMA](/knowledge-base/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) 엔진이 전송을 주도하므로 마스터 권한이 분산된 구조에 가깝다. 따라서 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터는 하드웨어 개념이면서 동시에 시스템 소프트웨어의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 모델을 바꾸는 분기점이다.

- **📢 섹션 요약 비유**: CPU 단독 마스터는 본사에서 모든 배송 전화를 직접 받는 방식이고, 멀티 마스터는 각 물류센터에 출고 권한을 준 방식과 같다. 후자가 훨씬 빠를 수 있지만, 출고 순서와 창고 충돌을 따로 관리해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터링은 "장치를 더 똑똑하게 만들어 CPU를 쉬게 하는 기술"로 요약할 수 있지만, 무조건 켠다고 좋은 것은 아니다. 대용량 저장장치, 고속 네트워크 카드, 그래픽 처리 장치 ([Graphics Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)), 오디오 인터페이스처럼 연속 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름이 큰 장치에서는 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터링의 이점이 매우 크다. 반면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)량이 작고 제어가 단순한 센서나 저가 [마이크로컨트롤러](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/130_microcontroller/) 환경에서는 오히려 구현 비용이 더 클 수 있다.

기술사 답안 관점에서는 다음 판단 기준이 중요하다.

1. **채택이 유리한 경우**: 블록 단위 전송이 많고 CPU 오프로드가 전체 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 좌우할 때
2. **신중해야 하는 경우**: 여러 마스터가 동시에 메모리를 두드려 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 예측성이 떨어질 때
3. **보완이 필수인 경우**: 장치가 임의 메모리 영역에 접근할 수 있으므로 [IOMMU](/knowledge-base/studynote/02_operating_system/10_security/627_iommu_dma_isolation/) (Input-Output [Memory Management Unit](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/284_mmu/)) 같은 주소 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 장치가 필요할 때

특히 서버나 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 환경에서는 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터 장치가 잘못된 주소로 DMA를 수행하면 다른 프로세스나 가상 머신의 메모리를 오염시킬 수 있다. 그래서 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)만 볼 것이 아니라, 메모리 매핑 범위 제한, [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/), [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 병합, 중재 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)까지 함께 설계해야 한다. [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상은 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터링의 결과이고, 안정성 확보는 그 전제조건이다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- DMA를 켰지만 버퍼 정렬, 캐시 플러시, 메모리 배리어를 고려하지 않아 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치가 발생하는 설계
- 오래된 드라이버 문제로 UDMA (Ultra [DMA](/knowledge-base/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/))가 비활성화되어 PIO 모드로 떨어지고, CPU 사용률만 급증하는 운영 환경
- 고우선 장치에 과도한 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)트를 허용해 다른 장치 응답성이 급격히 나빠지는 설계

- **📢 섹션 요약 비유**: [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터링은 유능한 부팀장에게 결재 권한을 나눠 주는 일과 같다. 업무는 빨라지지만, 권한 범위와 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 규칙 없이 맡기면 오히려 더 큰 사고가 난다.

---

## Ⅴ. 기대효과 및 결론

[버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터의 가장 큰 효과는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 경로에서 CPU를 떼어 내는 데 있다. CPU는 [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 복사보다 스케줄링, [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 처리, 애플리케이션 연산에 집중할 수 있고, 저장장치·네트워크·가속기 장치는 자신의 전송 특성에 맞춰 병렬적으로 움직일 수 있다. 이 덕분에 시스템은 같은 클럭에서도 더 높은 체감 처리량을 낼 수 있다.

하지만 한계도 분명하다. 마스터가 많아질수록 공유 자원 경합은 심해지고, [메모리 보호](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/307_memory_protection/)와 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 검증은 더 어려워진다. 그래서 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터는 "빠른 장치"의 다른 이름이 아니라, <strong>시스템 자율성을 부여받은 장치</strong>라는 관점으로 기억해야 한다.

앞으로는 [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) 기반 피어 투 피어 ([Peer-to-Peer](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/)) 전송, [CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) ([Compute Express Link](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/)) 같은 메모리 확장 인터커넥트처럼 장치가 더 적극적으로 메모리와 자원을 다루는 방향이 강해질 가능성이 높다. 그럴수록 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터의 의미는 단순한 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 제어자를 넘어, 시스템 안에서 독립적으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름을 조직하는 실행 주체로 확대된다.

- **📢 섹션 요약 비유**: [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터는 회사의 모든 박스를 사장이 직접 옮기던 시대를 끝내고, 각 부서가 자기 물류를 직접 처리하게 만든 변화와 같다. 회사는 빨라지지만, 창고 규칙과 출입 통제가 더 중요해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 슬레이브 ([Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) Slave) | 마스터가 시작한 전송에 응답하는 상대 장치 |
| [DMA](/knowledge-base/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) ([Direct Memory Access](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/318_dma/)) | CPU 대신 대표적으로 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터 권한을 활용하는 메커니즘 |
| [버스 중재](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/351_bus_arbitration/) ([Bus Arbitration](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/351_bus_arbitration/)) | 여러 마스터가 공유 자원을 충돌 없이 쓰게 하는 제어 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| PIO (Programmed Input/Output) | CPU가 직접 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동을 주도하는 대비 개념 |
| [IOMMU](/knowledge-base/studynote/02_operating_system/10_security/627_iommu_dma_isolation/) (Input-Output [Memory Management Unit](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/284_mmu/)) | [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터 장치의 메모리 접근 범위를 제한하는 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 장치 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">CPU 단독 전송 제어</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">버스 마스터 (Bus Master) / 버스 슬레이브 (Bus Slave) 구분</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">DMA (Direct Memory Access) 기반 CPU 오프로드</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">멀티 마스터 + 버스 중재 (Bus Arbitration)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">PCIe (PCI Express) 장치 주도 전송 · Peer-to-Peer · IOMMU 보호</div>
</div>
</div>



이 흐름은 시스템 구조가 "CPU가 모두 지시하는 단계"에서 "장치가 스스로 전송을 시작하되, 중재와 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)를 함께 설계하는 단계"로 진화했음을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 마스터는 컴퓨터 안에서 "어디로 짐을 보낼지 먼저 말할 수 있는 대장"이에요.
2. 예전에는 CPU만 대장이었지만, 지금은 똑똑한 장치들도 스스로 짐을 옮길 수 있어요.
3. 대신 대장이 많아지면 서로 부딪히지 않게 순서와 규칙을 꼭 정해야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 351 / 803

← **이전**: [349. 비동기식 버스 (Asynchronous Bus)](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/349_asynchronous_bus/)
**다음**: [351. 버스 중재 (Bus Arbitration)](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/351_bus_arbitration/) →

---
