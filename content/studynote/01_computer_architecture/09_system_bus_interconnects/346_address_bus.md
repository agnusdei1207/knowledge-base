+++
title = "346. 주소 버스 (Address Bus)"
date = 2026-04-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) (Address [Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/))는 CPU (Central Processing Unit)나 [DMA](/knowledge-base/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) ([Direct Memory Access](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/318_dma/)) 마스터가 "어느 위치를 접근할지"를 하드웨어에 지정하는 위치 정보 전용 경로다.
> 2. **가치**: 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)의 폭은 단순한 선 개수가 아니라, 시스템이 직접 식별할 수 있는 주소 공간 (Address Space)의 크기와 메모리 확장 한계를 결정한다.
> 3. **판단 포인트**: 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 [데이터 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/)처럼 많은 값을 실어 나르는 길이 아니라, 메모리 맵과 디코딩 전략을 통해 메모리·입출력·캐시 일관성의 경계를 정하는 설계 축이다.

---

## Ⅰ. 개요 및 필요성

주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) (Address [Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/))는 프로세서가 읽기나 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 수행하기 전에, 목표가 되는 메모리 셀이나 입출력 장치 레지스터의 위치를 먼저 지정하는 [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)선 묶음이다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 "무엇"인지보다 먼저 "어디"인지를 확정해야 하므로, 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 시스템 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)에서 가장 먼저 의미를 결정하는 좌표축 역할을 맡는다. 이 좌표 체계가 없으면 메인 메모리인 RAM (Random Access Memory)도, 장치 제어 레지스터도 모두 익명의 저장 공간으로 남아 CPU가 정확한 접근을 할 수 없다.

주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 중요한 이유는 현대 컴퓨터가 하나의 거대한 저장 공간처럼 보이지만, 실제로는 [DRAM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/) (Dynamic Random Access Memory), [ROM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/255_rom/) ([Read Only Memory](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/255_rom/)), [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) ([Peripheral Component Interconnect](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/) Express) 장치, 타이머, [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 컨트롤러 등이 서로 다른 범위에 배치된 구조이기 때문이다. CPU는 명령어를 실행할 때 매 순간 주소를 내보내며, 하드웨어는 그 주소를 보고 "이번 요청은 RAM용인지, 장치용인지, 금지된 영역인지"를 즉시 판정한다. 즉 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 단순 배선이 아니라, 시스템 자원 전체를 질서 있게 배치하는 하드웨어상의 지도다.

아래 그림은 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)보다 먼저 의미를 정하는 순서를 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                Address-first bus transaction sequence               │
├──────────────────────────────────────────────────────────────────────┤
│ CPU ── address=0x4000_1000 ──▶ Address Bus ──▶ Address Decoder      │
│  │                                                                   │
│  └── control=READ ───────────▶ Control Bus ─────▶ target select      │
│                                                                      │
│ Selected target only ─────────▶ Data Bus ─────────▶ CPU              │
│                                                                      │
│ Key point: address decides the destination before data can move.     │
└──────────────────────────────────────────────────────────────────────┘
```

이 흐름의 핵심은 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 운반하지 않더라도, 어떤 장치가 응답할 자격이 있는지를 먼저 정한다는 점이다. 따라서 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 설계가 흔들리면 [데이터 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/)와 [제어 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/347_control_bus/)가 정상이어도 잘못된 장치가 응답하거나, 아무 장치도 선택되지 않는 치명적 오류가 발생한다.

- **📢 섹션 요약 비유**: 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 대형 물류센터의 "선반 번호 호출기"와 같다. 어떤 상자를 꺼낼지 선반 번호가 먼저 정해져야 지게차가 정확한 위치로 움직일 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)의 핵심 원리는 "[비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 패턴으로 위치를 표현하고, [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)가 그 패턴을 해석해 단 하나의 대상만 활성화한다"는 것이다. 예를 들어 32비트 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)라면 이론적으로 2^32개의 주소 조합을 만들 수 있고, [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 단위 주소 지정([Byte](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) Addressing)을 가정하면 최대 4GB 공간을 직접 표현할 수 있다. 64비트 시스템은 논리적으로 2^64 범위를 다룰 수 있지만, 실제 구현에서는 전력·핀 수·회로 복잡도를 줄이기 위해 48비트나 52비트 정도만 [물리 주소](/knowledge-base/studynote/02_operating_system/06_memory_management/323_physical_address/)로 쓰는 경우가 많다.

| 항목 | 의미 | 설계상 중요 포인트 |
| :--- | :--- | :--- |
| 주소 폭 (Address Width) | 주소선 개수 | 최대 주소 공간 결정 |
| 주소 지정 단위 | [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)/[워드](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) 단위 | 세밀도와 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 결정 |
| 주소 디코딩 | 범위 해석 후 대상 선택 | 충돌 방지, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 최소화 |
| 칩 선택 (Chip [Select](/knowledge-base/studynote/05_database/04_transactions_concurrency/520_select/)) | 특정 장치 활성화 | 잘못된 응답 차단 |

아래 그림은 주소 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 상위 영역 선택과 하위 오프셋으로 나뉘는 전형적 구조를 요약한다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                    Address interpretation model                     │
├──────────────────────────────────────────────────────────────────────┤
│ A31 .............. A20 │ A19 ................................. A0   │
│ ── region select ───── │ ─────────── offset inside region ───────   │
│                                                                      │
│ 0000_0000_xxx...  -> main memory                                     │
│ 1111_0000_xxx...  -> MMIO region                                     │
│ 1111_1111_xxx...  -> firmware / reserved                             │
└──────────────────────────────────────────────────────────────────────┘
```

이 구조는 상위 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 큰 구역을 정하고, 하위 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 그 안의 세부 위치를 지정하는 방식이다. 그래서 시스템 설계자는 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 단순히 늘리는 것만이 아니라, 어느 구간을 메모리 맵 I/O (Memory-Mapped Input/Output), 어느 구간을 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/), 어느 구간을 주기억장치에 배정할지까지 함께 설계해야 한다. 결국 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)의 물리 폭과 주소 맵 정책이 합쳐져 실제 시스템의 접근 질서를 만든다.

- **📢 섹션 요약 비유**: 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 도서관 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계와 같다. 앞자리는 몇 층 서가인지 알려주고, 뒷자리는 그 서가 안에서 몇 번째 책인지 가리킨다.

---

## Ⅲ. 비교 및 연결

주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 제대로 이해하려면 [데이터 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/)와 [제어 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/347_control_bus/), 그리고 가상 주소 체계와의 경계를 함께 봐야 한다. 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 위치 정보만 전달하므로 보통 CPU에서 외부 장치로 향하는 [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 구조를 취한다. 반면 [데이터 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/)는 읽기와 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 모두 수행해야 하므로 양방향이고, [제어 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/347_control_bus/)는 읽기·[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)·[인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)·대기 같은 상태 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 주고받기 때문에 역할이 가장 복합적이다.

| 구분 | 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) (Address [Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)) | [데이터 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/) ([Data Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/)) | [제어 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/347_control_bus/) ([Control Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/347_control_bus/)) |
| :--- | :--- | :--- | :--- |
| 답하는 질문 | 어디에? | 무엇을? | 언제/어떻게? |
| 대표 방향성 | 주로 [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) | 양방향 | 양방향 |
| 폭의 의미 | 주소 공간 크기 | 전송량/[워드](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) 크기 | [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 종류 수 |
| 병목 형태 | 공간 배치 한계 | [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 부족 | 타이밍·[동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 문제 |

운영체제와 연결해 보면, 프로그램이 사용하는 것은 보통 가상 주소 (Virtual Address)이며 이를 실제 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)에 실릴 [물리 주소](/knowledge-base/studynote/02_operating_system/06_memory_management/323_physical_address/) ([Physical Address](/knowledge-base/studynote/02_operating_system/06_memory_management/323_physical_address/))로 바꾸는 주체는 [MMU](/knowledge-base/studynote/02_operating_system/06_memory_management/328_mmu/) ([Memory Management Unit](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/284_mmu/))다. 즉 소프트웨어가 보는 주소와 회로가 받는 주소는 다를 수 있고, 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 그 변환이 끝난 뒤 마지막으로 하드웨어에 공개되는 최종 좌표다. 또한 MMIO는 장치 레지스터를 메모리처럼 같은 주소 공간 안에 배치하므로, 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 메모리와 장치를 하나의 통일된 접근 모델로 묶어 준다.

이 지점에서 중요한 설계 감각은 "주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 넓다 = 무조건 빠르다"가 아니라는 점이다. 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 더 넓은 공간을 식별하게 해 주지만, 실제 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 캐시 계층, [데이터 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/) [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), 메모리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간이 함께 결정한다. 따라서 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 속도의 상징이라기보다, 시스템이 어디까지 인식하고 배치할 수 있는지를 규정하는 공간 설계의 축으로 이해해야 한다.

- **📢 섹션 요약 비유**: 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 도시 지도, [데이터 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/)는 배송 트럭, [제어 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/347_control_bus/)는 교통 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)와 같다. 지도가 넓다고 배송이 자동으로 빨라지는 것은 아니지만, 지도가 없으면 어느 동네도 제대로 찾을 수 없다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 추상 이론보다 메모리 맵 설계와 충돌 회피 문제로 자주 등장한다. [마이크로컨트롤러](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/130_microcontroller/) 기반 임베디드 시스템에서는 [플래시 메모리](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/), [SRAM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/250_sram/) (Static Random Access Memory), GPIO (General Purpose Input/Output), 타이머, UART (Universal Asynchronous Receiver-Transmitter)를 각 주소 구간에 배치한다. 이때 주소 범위를 겹치게 잡으면 한 번의 접근에 둘 이상의 장치가 동시에 응답할 수 있어, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 오염이나 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 컨텐션이 발생한다.

서버나 고성능 시스템에서는 [물리 주소](/knowledge-base/studynote/02_operating_system/06_memory_management/323_physical_address/) 확장과 장치 매핑이 더 중요한 판단 포인트다. 예를 들어 64비트 CPU여도 모든 [물리 주소](/knowledge-base/studynote/02_operating_system/06_memory_management/323_physical_address/) [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 구현하지 않을 수 있으므로, 실제 메모리 확장 한계는 [ISA](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/) ([Instruction Set Architecture](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/)) 문서와 칩셋 명세를 함께 봐야 한다. 또한 대형 [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) 장치나 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리를 MMIO 영역으로 매핑할 때는 주소 공간 예약 때문에 사용 가능한 RAM 영역이 일부 줄어들 수 있으므로, 단순 장착 용량만 보고 설계하면 안 된다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 주소 맵이 서로 겹치지 않도록 상위 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 기준으로 구역을 명확히 나눴는가?
2. 주소 [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 시스템 타이밍 예산 안에 들어오는가?
3. MMIO 구간과 캐시 정책이 충돌하지 않도록 비캐시 영역을 분리했는가?
4. [물리 주소](/knowledge-base/studynote/02_operating_system/06_memory_management/323_physical_address/) 폭과 실제 지원 메모리 용량을 칩셋·프로세서 기준으로 모두 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)했는가?

### 피해야 할 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 주소 폭만 보고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상을 기대하는 판단
- 장치 레지스터와 메모리 영역을 느슨하게 섞어 디버깅이 어려운 메모리 맵 구성
- 예약 영역을 무시해 "장착한 RAM = 모두 사용 가능"이라고 가정하는 설계

- **📢 섹션 요약 비유**: 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 설계는 쇼핑몰 층별 안내도를 짜는 일과 같다. 매장 배치를 겹치게 그리면 손님도 직원도 같은 번호를 보고 서로 다른 곳으로 뛰어가게 된다.

---

## Ⅴ. 기대효과 및 결론

잘 설계된 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 체계는 시스템 전체를 단순하게 만든다. CPU는 동일한 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 규칙으로 메모리와 장치를 접근할 수 있고, 하드웨어는 주소 디코딩만으로 응답 대상을 정해 복잡한 제어 로직을 줄일 수 있다. 이 단순함은 결국 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 용이성, 장치 확장성, 장애 분석 가능성으로 이어진다.

반대로 주소 체계가 난잡하면 하드웨어 자원은 늘어도 시스템은 더 다루기 어려워진다. 특히 멀티코어, [IOMMU](/knowledge-base/studynote/02_operating_system/10_security/627_iommu_dma_isolation/) (Input/Output [Memory Management Unit](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/284_mmu/)), [CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) ([Compute Express Link](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/)) 같은 현대 기술이 들어오면 주소 공간은 단순 메모리 번지 체계를 넘어, 장치 공유와 메모리 풀링의 기반이 된다. 따라서 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 "메모리 위치를 알려주는 선"으로만 기억하기보다, 컴퓨터가 자원을 공간적으로 조직하는 가장 기본적인 질서로 기억하는 것이 정확하다.

- **📢 섹션 요약 비유**: 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 거대한 캠퍼스의 건물 번호 체계와 같다. 번호 체계가 명확하면 처음 온 사람도 강의실을 찾지만, 번호가 뒤섞이면 좋은 건물이 많아도 전체 캠퍼스는 혼란에 빠진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [데이터 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/) ([Data Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/)) | 주소가 선택한 대상과 실제 값을 주고받는 통로 |
| [제어 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/347_control_bus/) ([Control Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/347_control_bus/)) | 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)/대기 등 접근 행위를 규정하는 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 집합 |
| [MMU](/knowledge-base/studynote/02_operating_system/06_memory_management/328_mmu/) ([Memory Management Unit](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/284_mmu/)) | 가상 주소를 [물리 주소](/knowledge-base/studynote/02_operating_system/06_memory_management/323_physical_address/)로 변환한 뒤 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)로 전달 |
| MMIO (Memory-Mapped Input/Output) | 장치 레지스터를 메모리와 같은 주소 공간에 배치 |
| 주소 [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) (Address [Decoder](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)) | 주소 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 해석해 특정 장치만 활성화 |
| [IOMMU](/knowledge-base/studynote/02_operating_system/10_security/627_iommu_dma_isolation/) (Input/Output [Memory Management Unit](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/284_mmu/)) | 장치 측 주소 접근까지 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)·변환하는 확장 계층 |

### 📈 관련 키워드 및 발전 흐름도

```text
주소 지정 필요
    │
    ▼
주소 버스 (Address Bus) · 주소 공간 (Address Space)
    │
    ▼
주소 디코더 (Address Decoder) · 칩 선택 (Chip Select)
    │
    ▼
MMU (Memory Management Unit) · 가상 메모리 (Virtual Memory)
    │
    ▼
MMIO (Memory-Mapped Input/Output) · PCIe address mapping
    │
    ▼
IOMMU · CXL memory expansion
```

이 흐름은 단순 위치 지정에서 출발해, 주소 변환·장치 통합·메모리 확장으로 개념이 넓어지는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 컴퓨터가 "몇 번 서랍을 열까?"를 정하는 숫자 표지판이에요.
2. 표지판이 정확해야 로봇이 장난감이 든 서랍과 스위치가 있는 서랍을 헷갈리지 않아요.
3. 그래서 주소 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 물건을 옮기기 전에 먼저 목적지를 알려주는 길잡이랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 347 / 803

← **이전**: [345. 데이터 버스 (Data Bus)](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/)
**다음**: [347. 제어 버스 (Control Bus)](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/347_control_bus/) →

---
