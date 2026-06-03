---
title: 282. 가상 메모리 (Virtual Memory)
date: '2026-04-20'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[381_virtual_memory|가상 메모리]] ([[381_virtual_memory|Virtual Memory]])는 프로그램이 보는 주소와 실제 물리 메모리 주소를 분리해, 작은 물리 메모리도 더 크고 안전한 작업 공간처럼 쓰게 만드는 주소 [[198_abstraction_control_data_process|추상화]] 계층이다.
> 2. **가치**: 각 프로세스에 독립된 주소 공간을 제공하므로 [[307_memory_protection|메모리 보호]], 재배치 용이성, [[675_multitasking_terminology_preemptive|멀티태스킹]], 대용량 프로그램 실행이 동시에 가능해진다.
> 3. **판단 포인트**: [[381_virtual_memory|가상 메모리]]는 용량을 “공짜로 늘리는 기술”이 아니라, [[387_page_fault|페이지 부재]] ([[387_page_fault|Page Fault]]) 비용을 통제하면서 지역성 (Locality)을 활용할 때만 [[282_performance_tactics|성능]] 이점을 내는 절충 구조다.

---

## Ⅰ. 개요 및 필요성

[[381_virtual_memory|가상 메모리]] ([[381_virtual_memory|Virtual Memory]])는 CPU (Central Processing Unit)가 생성한 가상 주소를 물리 메모리의 실제 주소로 변환해 사용하는 메모리 관리 방식이다. 핵심은 프로그램이 “연속적이고 넓은 개인 메모리”를 쓰는 것처럼 보이게 만들면서, 실제 하드웨어는 여러 프로세스의 [[001_dikw_pyramid|데이터]]를 잘게 나누어 공유한다는 점이다. 즉, [[381_virtual_memory|가상 메모리]]는 단순한 저장 공간 확장이 아니라 **주소 [[198_abstraction_control_data_process|추상화]] + [[571_protection_vs_security|보호]] + 적재 [[015_지연_데이터_관점|지연]]**을 묶은 시스템 설계다.

이 개념이 필요해진 이유는 [[459_quic_fec_forward_error_correction|초기]] 컴퓨터의 물리 메모리 제약이 너무 직접적이었기 때문이다. 물리 메모리만 직접 다루던 시절에는 프로그램을 어느 주소에 적재할지 사람이 맞춰야 했고, 프로그램 크기가 메모리보다 크면 오버레이 (Overlay) 같은 수동 기법으로 코드를 나눠 불러와야 했다. 또한 한 프로그램의 버그가 다른 프로그램의 메모리를 덮어써 전체 시스템을 무너뜨리는 문제도 잦았다.

[[381_virtual_memory|가상 메모리]]는 이 문제를 세 가지로 풀었다. 첫째, 각 프로세스에 0번지부터 시작하는 독립 주소 공간을 제공해 개발자가 실제 적재 위치를 의식하지 않게 했다. 둘째, 필요한 [[286_page_frame|페이지]]만 물리 메모리에 적재해 물리 용량보다 큰 작업 집합을 다룰 수 있게 했다. 셋째, [[001_operating_system_purpose|운영체제]]와 하드웨어가 접근 권한을 검사해 [[307_memory_protection|메모리 보호]]를 강제했다.

따라서 [[381_virtual_memory|가상 메모리]]를 이해할 때는 “디스크를 램처럼 쓰는 기술”이라는 축약 설명만으로는 부족하다. 더 정확한 관점은 **프로그램의 [[369_logic_bomb|논리]] 세계와 하드웨어의 물리 세계를 분리하여, 둘 사이를 [[001_operating_system_purpose|운영체제]] ([[001_operating_system_purpose|Operating System]])와 메모리 관리 장치가 중재하는 구조**라고 보는 것이다.

- **📢 섹션 요약 비유**: [[381_virtual_memory|가상 메모리]]는 대형 도서관의 개인 열람석과 같다. 이용자는 자기 책상 하나만 보지만, 실제로는 사서가 창고 전체에서 필요한 책만 가져다주고 다른 사람 책과 섞이지 않게 철저히 관리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[381_virtual_memory|가상 메모리]]의 중심에는 [[328_mmu|MMU]] ([[284_mmu|Memory Management Unit]]), [[353_page_table|페이지 테이블]] ([[353_page_table|Page Table]]), [[357_tlb|TLB]] ([[291_tlb|Translation Lookaside Buffer]]), 그리고 보조기억장치가 있다. CPU는 가상 주소를 내보내고, MMU는 이를 [[286_page_frame|페이지]] 번호와 오프셋으로 나눈 뒤 TLB에서 최근 변환 결과를 먼저 찾는다. TLB에 없으면 [[353_page_table|페이지 테이블]]을 따라가 물리 프레임을 찾고, 해당 [[286_page_frame|페이지]]가 메모리에 없으면 [[387_page_fault|페이지 부재]]를 발생시켜 [[001_operating_system_purpose|운영체제]]에 제어를 넘긴다.

아래 표는 [[381_virtual_memory|가상 메모리]]의 핵심 구성 요소와 병목을 한눈에 정리한 것이다.

| 구성 요소 | 역할 | [[282_performance_tactics|성능]] 관점 핵심 포인트 |
| :-- | :-- | :-- |
| 가상 [[286_page_frame|페이지]] (Virtual [[286_page_frame|Page]]) | 프로세스가 보는 메모리 조각 | 보통 4KB, 2MB, 1GB 등으로 관리 |
| 물리 프레임 (Physical Frame) | 실제 RAM (Random Access Memory)의 저장 조각 | 프레임 수가 부족하면 교체 발생 |
| [[357_tlb|TLB]] | 최근 주소 변환 캐시 | 미스가 나면 [[353_page_table|페이지 테이블]] 탐색 비용 증가 |
| [[353_page_table|페이지 테이블]] | 가상-물리 매핑과 권한 정보 저장 | 크기가 커지면 다단계 구조 필요 |
| [[387_page_fault|페이지 부재]] 처리 | 없는 [[286_page_frame|페이지]]를 [[327_ssd|SSD]]/HDD에서 적재 | 가장 큰 [[015_지연_데이터_관점|지연]], 보통 ns가 아니라 us~ms 단위 |

이 그림은 CPU가 [[001_dikw_pyramid|데이터]]를 읽기까지 거치는 계층과, 어느 지점에서 고속 처리와 저속 처리가 갈리는지를 보여준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                가상 주소가 실제 데이터가 되기까지의 경로                  │
├────────────────────────────────────────────────────────────────────────────┤
│ CPU가 가상 주소 생성                                                      │
│      │                                                                    │
│      ▼                                                                    │
│  [ VPN | Offset ]                                                         │
│      │                                                                    │
│      ▼                                                                    │
│  TLB 조회 ────────────────┬─────────────── TLB Hit ─────▶ 물리 주소 생성   │
│      │                    │                                                 │
│      │ TLB Miss           │                                                 │
│      ▼                    │                                                 │
│ 페이지 테이블 조회        │                                                 │
│      │                    │                                                 │
│      ├── Present = 1 ─────┘                                                 │
│      │                                                                      │
│      └── Present = 0 ─▶ Page Fault ─▶ OS 처리 ─▶ 디스크에서 Page-In         │
│                                             │                              │
│                                             └── PTE 갱신 후 명령 재시도     │
└────────────────────────────────────────────────────────────────────────────┘
```

핵심 원리는 [[255_demand_paging|요구 페이징]] ([[255_demand_paging|Demand Paging]])이다. 프로그램 전체를 한꺼번에 RAM에 올리지 않고, 실제 [[316_reference_pattern_nosql|참조]]된 [[286_page_frame|페이지]]만 가져온다. 이 방식은 물리 메모리를 절약하지만, [[387_page_fault|페이지 부재]]가 발생하면 [[327_ssd|SSD]] ([[327_ssd|Solid State Drive]])나 [[465_hdd_structure|HDD]] (Hard Disk Drive) 접근이 필요해 수 마이크로초에서 수 밀리초까지 [[015_지연_데이터_관점|지연]]이 커질 수 있다. [[251_dram|DRAM]] (Dynamic Random Access Memory) 접근이 대략 수십~수백 ns인 점을 생각하면, [[387_page_fault|페이지 부재]] 한 번은 수만 배 이상의 비용 차이를 만든다.

이때 [[001_operating_system_purpose|운영체제]]는 단순 적재만 하는 것이 아니라 권한 비트와 상태 비트를 함께 관리한다. 읽기/[[289_cqrs_db|쓰기]]/실행 권한, 수정 여부([[396_dirty_bit|Dirty Bit]]), [[316_reference_pattern_nosql|참조]] 여부(Access [[086_fenwick_tree|Bit]]), 존재 여부(Present [[086_fenwick_tree|Bit]])가 [[353_page_table|페이지 테이블]] 엔트리인 PTE ([[353_page_table|Page Table]] Entry)에 기록된다. 덕분에 [[381_virtual_memory|가상 메모리]]는 [[282_performance_tactics|성능]] 계층이면서 동시에 [[307_memory_protection|메모리 보호]]와 프로세스 격리의 기반이 된다.

- **📢 섹션 요약 비유**: [[381_virtual_memory|가상 메모리]]는 호텔 프런트와 창고가 함께 움직이는 시스템과 같다. 손님은 방 번호만 말하면 되지만, 프런트는 열쇠 기록을 확인하고 방이 비어 있지 않으면 창고에서 가구를 옮겨와 방을 다시 꾸민 뒤 손님을 들여보낸다.

---

## Ⅲ. 비교 및 연결

[[381_virtual_memory|가상 메모리]]의 경계를 분명히 하려면 직접 [[323_physical_address|물리 주소]] 방식, 캐시, [[364_segmentation|세그멘테이션]]과 비교해야 한다. [[323_physical_address|물리 주소]] 직접 사용은 단순하지만 재배치와 [[571_protection_vs_security|보호]]가 약하고, 캐시는 속도 격차를 줄이기 위한 하드웨어 자동 계층이며, [[364_segmentation|세그멘테이션]]은 [[369_logic_bomb|논리]] 단위를 잘 드러내지만 [[342_external_fragmentation|외부 단편화]] 문제를 안는다. 현대 시스템이 [[286_page_frame|페이지]] 기반 [[381_virtual_memory|가상 메모리]]를 표준으로 삼는 이유는 **고정 크기 관리가 [[291_fragmentation_and_reassembly_process|단편화]] 제어와 하드웨어 구현에 유리하기 때문**이다.

| 비교 대상 | 무엇을 해결하는가 | 장점 | 한계 |
| :-- | :-- | :-- | :-- |
| [[323_physical_address|물리 주소]] 직접 사용 | 단순 주소 접근 | 구현 단순, 변환 비용 적음 | [[571_protection_vs_security|보호]]·재배치·확장성 취약 |
| [[381_virtual_memory|가상 메모리]] + [[259_paging|페이징]] | 용량, [[571_protection_vs_security|보호]], 재배치, [[675_multitasking_terminology_preemptive|멀티태스킹]] | 표준화, 격리, 대용량 지원 | [[387_page_fault|페이지 부재]]·[[357_tlb|TLB]] 미스 비용 |
| [[259_cache_memory|캐시 메모리]] ([[259_cache_memory|Cache Memory]]) | CPU와 RAM 사이 속도 차이 | 완전 하드웨어 자동화, 매우 빠름 | 용량 문제는 못 해결 |
| [[364_segmentation|세그멘테이션]] ([[364_segmentation|Segmentation]]) | 코드/[[001_dikw_pyramid|데이터]]/스택의 [[369_logic_bomb|논리]] 분리 | [[369_logic_bomb|논리]] 의미 표현이 쉬움 | [[342_external_fragmentation|외부 단편화]], 관리 복잡 |

[[381_virtual_memory|가상 메모리]]는 다른 과목과도 강하게 연결된다. [[001_operating_system_purpose|운영체제]]에서는 [[260_page_replacement|페이지 교체]], [[265_working_set|워킹 셋]] ([[265_working_set|Working Set]]), [[257_thrashing|스래싱]] ([[257_thrashing|Thrashing]]), [[131_mmap_ipc|메모리 맵 파일]]로 이어지고, 컴퓨터구조에서는 TLB와 캐시의 상호작용, [[289_multilevel_page_table|다단계 페이지 테이블]], 64비트 주소 공간 설계와 연결된다. 보안 관점에서는 프로세스 격리, [[374_aslr|ASLR]] (Address Space Layout Randomization), NX (No-eXecute) 비트의 기반이 된다.

특히 캐시와 [[381_virtual_memory|가상 메모리]]는 자주 함께 혼동된다. 둘 다 지역성을 이용하지만, 캐시는 “더 빠른 저장장치에 복사해 두는 계층”이고 [[381_virtual_memory|가상 메모리]]는 “더 큰 주소 공간을 만들기 위한 매핑 계층”이라는 점에서 목표가 다르다. 캐시 미스는 보통 하드웨어 내부에서 수십~수백 사이클로 처리되지만, [[387_page_fault|페이지 부재]]는 [[001_operating_system_purpose|운영체제]]가 개입하는 시스템 이벤트라는 점에서 무게가 완전히 다르다.

- **📢 섹션 요약 비유**: 캐시는 책상 위 자주 쓰는 필통이고, [[381_virtual_memory|가상 메모리]]는 학교 전체 사물함 배치도다. 필통은 손이 빨리 닿게 해 주고, 사물함 배치도는 물건이 어디에 있어야 안전하고 질서 있게 관리되는지를 정해 준다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[381_virtual_memory|가상 메모리]]는 “있으면 좋은 기능”이 아니라 시스템 성격에 따라 설계 전략이 갈리는 핵심 정책이다. 범용 서버와 데스크톱은 [[381_virtual_memory|가상 메모리]]를 적극 활용해 높은 [[675_multitasking_terminology_preemptive|멀티태스킹]]과 격리를 얻지만, 실시간 제어 시스템은 예측 불가능한 [[387_page_fault|페이지 부재]]를 위험 요소로 본다. 즉, 중요한 질문은 [[381_virtual_memory|가상 메모리]]를 쓸지 말지가 아니라 **어디까지 [[331_dynamic_loading|동적 적재]]를 허용할지**다.

예를 들어 대규모 [[001_dikw_pyramid|데이터]] 처리 시스템은 [[131_mmap_ipc|메모리 맵 파일]] ([[308_memory_mapped_file|Memory-Mapped File]])을 이용해 수십 기가바이트 [[501_file_definition_logical_record|파일]]을 가상 주소 공간에 매핑하고 필요한 [[286_page_frame|페이지]]만 읽는다. 이 접근은 개발 생산성과 I/O 단순성을 높이지만, 작업 집합이 RAM을 크게 초과하면 [[387_page_fault|페이지 부재]]가 폭증해 오히려 처리량이 급락한다. 반대로 [[002_database_definition|데이터베이스]] 버퍼 풀처럼 애플리케이션이 직접 메모리 관리 정책을 구현하는 경우에는 [[001_operating_system_purpose|운영체제]]의 [[260_page_replacement|페이지 교체]]와 이중으로 충돌하지 않도록 튜닝이 필요하다.

기술사 답안이나 설계 면접에서는 다음 판단 문장이 중요하다.

1. **[[138_response_time|응답 시간]] 예측 가능성이 최우선이면** 핵심 코드와 [[001_dikw_pyramid|데이터]]는 고정([[510_lock|lock]])하거나 [[387_page_fault|페이지 부재]]를 사실상 금지해야 한다.
2. **처리량과 격리가 중요하면** [[381_virtual_memory|가상 메모리]]를 적극 활용하되, 스왑 의존 운영을 정상 상태로 받아들이면 안 된다.
3. **[[352_page_size|페이지 크기]] 선택에서는** 작은 [[286_page_frame|페이지]]가 내부 [[291_fragmentation_and_reassembly_process|단편화]]를 줄이지만 [[353_page_table|페이지 테이블]]과 [[357_tlb|TLB]] 부담을 키우고, 큰 [[286_page_frame|페이지]]는 [[357_tlb|TLB]] 효율을 높이지만 낭비와 입출력 증폭을 만들 수 있다.

### 실무 [[435_checklist_based_testing|체크리스트]]

- `vmstat`, `sar`, `perf` 등으로 [[387_page_fault|페이지 부재]]율과 스왑 입출력을 관찰하는가?
- [[357_tlb|TLB]] 미스와 캐시 미스, 실제 디스크 I/O 병목을 구분해서 보는가?
- 메모리 부족 문제를 단순 스왑 확대로 덮지 않고 작업 집합 크기와 [[014_concurrency|동시성]] 수준을 함께 조정하는가?
- [[517_huge_page|Huge Page]], [[377_numa_allocation|NUMA]] ([[377_numa_allocation|Non-Uniform Memory Access]]), [[749_memory_mapped_file_mmap|mmap]] 정책이 애플리케이션 접근 패턴과 맞는가?

### 대표 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- RAM 부족 상태를 스왑으로 장기간 버티게 두는 설계
- 실시간 시스템에서 [[286_page_frame|페이지]] 잠금 없이 최악 [[015_지연_데이터_관점|지연]]을 논하는 설계
- 메모리 사용량만 보고 안심하고, 실제 [[387_page_fault|페이지 부재]] 폭증을 놓치는 운영

- **📢 섹션 요약 비유**: [[381_virtual_memory|가상 메모리]] 운영은 창고형 매장을 꾸리는 일과 같다. 손님이 많이 온다고 통로보다 창고를 믿기만 하면 계산대는 멈춘다. 필요한 물건이 매장 안에 제때 놓이도록 동선과 재고를 함께 설계해야 장사가 된다.

---

## Ⅴ. 기대효과 및 결론

[[381_virtual_memory|가상 메모리]]가 주는 가장 큰 효과는 프로그래밍 모델의 단순화다. 개발자는 물리 메모리의 실제 배치를 거의 의식하지 않고도 큰 주소 공간, 안전한 격리, [[336_library_vs_framework|라이브러리]] 공유, [[331_dynamic_loading|동적 적재]] 같은 혜택을 동시에 얻는다. [[001_operating_system_purpose|운영체제]]는 이를 바탕으로 멀티프로세스 환경, [[333_shared_library|공유 라이브러리]], 포크 (fork), [[131_mmap_ipc|메모리 맵 파일]] 같은 고급 기능을 실현한다.

하지만 효과는 전제조건 위에서만 성립한다. 충분한 물리 메모리, 좋은 지역성, 적절한 [[352_page_size|페이지 크기]], 과도하지 않은 [[014_concurrency|동시성]], 안정적인 저장장치가 뒷받침되지 않으면 [[381_virtual_memory|가상 메모리]]는 곧바로 [[015_지연_데이터_관점|지연]] 폭탄이 된다. 특히 [[257_thrashing|스래싱]]은 “용량을 [[369_logic_bomb|논리]]로 덮을 수는 있어도, 접근 시간을 무시할 수는 없다”는 사실을 보여주는 대표 사례다.

앞으로의 확장 방향은 세 가지 정도로 요약할 수 있다. 첫째, Huge Page와 다단계 [[286_page_frame|페이지]] 최적화로 [[357_tlb|TLB]] 부담을 줄이는 방향이다. 둘째, [[015_virtualization|가상화]] 환경의 이중 주소 변환을 줄이기 위한 EPT (Extended [[286_page_frame|Page]] Tables), NPT (Nested [[286_page_frame|Page]] Tables) 같은 하드웨어 보조다. 셋째, [[441_cxl|CXL]] ([[441_cxl|Compute Express Link]]) 기반 메모리 확장처럼 물리 메모리 계층 자체를 유연하게 만드는 방향이다.

결국 [[381_virtual_memory|가상 메모리]]는 “메모리를 늘리는 마법”이 아니라 **주소를 설계해 [[282_performance_tactics|성능]]·[[571_protection_vs_security|보호]]·확장성을 함께 얻는 시스템 계약**으로 기억해야 한다. 주소 변환이 부드럽게 숨겨질 때는 현대 컴퓨팅의 토대가 되지만, [[387_page_fault|페이지 부재]]가 통제를 벗어나는 순간 가장 먼저 드러나는 병목도 바로 이 계층이다.

- **📢 섹션 요약 비유**: [[381_virtual_memory|가상 메모리]]는 무한한 운동장을 그려 주는 설계도이지만, 실제로는 출입문과 복도 폭이 정해진 경기장이다. 설계도만 믿고 사람을 너무 많이 들이면 경기보다 입장 대기가 더 길어진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [[328_mmu|MMU]] ([[284_mmu|Memory Management Unit]]) | 가상 주소를 [[323_physical_address|물리 주소]]로 변환하는 하드웨어 관문 |
| [[357_tlb|TLB]] ([[291_tlb|Translation Lookaside Buffer]]) | 주소 변환 결과를 캐싱해 [[353_page_table|페이지 테이블]] 접근 [[015_지연_데이터_관점|지연]]을 줄임 |
| [[353_page_table|페이지 테이블]] ([[353_page_table|Page Table]]) | 매핑, 권한, 존재 여부를 담는 [[001_operating_system_purpose|운영체제]]의 메모리 장부 |
| [[255_demand_paging|요구 페이징]] ([[255_demand_paging|Demand Paging]]) | 필요한 시점에만 [[286_page_frame|페이지]]를 적재해 물리 메모리를 절약 |
| [[387_page_fault|페이지 부재]] ([[387_page_fault|Page Fault]]) | 적재되지 않은 [[286_page_frame|페이지]] 접근 시 [[001_operating_system_purpose|운영체제]]가 개입하는 사건 |
| [[257_thrashing|스래싱]] ([[257_thrashing|Thrashing]]) | 작업 집합을 못 담아 [[260_page_replacement|페이지 교체]]만 반복하는 [[282_performance_tactics|성능]] 붕괴 상태 |
| [[307_memory_protection|메모리 보호]] ([[307_memory_protection|Memory Protection]]) | 프로세스 간 침범을 막는 권한 검사와 격리의 기반 |
| [[131_mmap_ipc|메모리 맵 파일]] ([[308_memory_mapped_file|Memory-Mapped File]]) | [[501_file_definition_logical_record|파일]]을 주소 공간에 직접 매핑해 I/O와 메모리 접근을 연결 |

### 📈 관련 키워드 및 발전 흐름도

```text
오버레이 (Overlay) · 고정 분할 메모리
        │
        ▼
가상 주소 / 물리 주소 분리
        │
        ▼
페이징 (Paging) · 페이지 테이블 (Page Table)
        │
        ▼
TLB (Translation Lookaside Buffer) · 다단계 페이지 테이블
        │
        ▼
요구 페이징 (Demand Paging) · 페이지 부재 (Page Fault)
        │
        ▼
워킹 셋 (Working Set) · 스래싱 (Thrashing) 제어
        │
        ▼
메모리 맵 파일 · Huge Page · 가상화 이중 페이징
```

이 흐름은 단순 적재 기법에서 출발해, 주소 [[198_abstraction_control_data_process|추상화]] → 변환 최적화 → [[331_dynamic_loading|동적 적재]] → [[282_performance_tactics|성능]] 제어 → 현대 확장 기술로 이어지는 발전 맥락을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[381_virtual_memory|가상 메모리]]는 작은 책상만 있어도 아주 큰 공부방을 쓰는 것처럼 느끼게 해 주는 마법 같은 정리법이에요.
2. 지금 보는 책만 책상 위에 올리고, 나머지 책은 뒤 창고에 두었다가 필요할 때만 가져와요.
3. 하지만 책상에 자주 없는 책만 찾게 되면 공부보다 책 옮기느라 더 바빠지니까, 필요한 책이 가까이에 있게 잘 정리해야 해요.
