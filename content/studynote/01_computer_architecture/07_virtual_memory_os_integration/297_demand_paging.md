---
title: 297. 요구 페이징 (Demand Paging)
date: '2026-04-20'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[255_demand_paging|요구 페이징]] ([[255_demand_paging|Demand Paging]])은 프로세스 전체를 미리 적재하지 않고, 실제 접근이 발생한 [[286_page_frame|페이지]] ([[286_page_frame|Page]])만 그 순간 물리 메모리로 가져오는 **[[015_지연_데이터_관점|지연]] 적재 [[268_strategy_pattern|전략]]**이다.
> 2. **가치**: 이 [[268_strategy_pattern|전략]]은 비싼 주기억장치 자원을 현재 필요한 작업에 집중시켜, 더 많은 프로세스를 동시에 실행하고 [[459_quic_fec_forward_error_correction|초기]] 구동 시간을 줄이게 만든다.
> 3. **판단 포인트**: 성패는 결국 [[253_locality_of_reference|참조의 지역성]] (Locality)과 [[720_page_fault_isr|페이지 폴트]] ([[387_page_fault|Page Fault]]) 비용의 균형에 달려 있으며, 지역성이 무너지면 [[255_demand_paging|요구 페이징]]은 곧바로 [[257_thrashing|스래싱]] ([[257_thrashing|Thrashing]])으로 추락한다.

---

## Ⅰ. 개요 및 필요성

[[255_demand_paging|요구 페이징]] ([[255_demand_paging|Demand Paging]])은 [[381_virtual_memory|가상 메모리]] ([[381_virtual_memory|Virtual Memory]]) 환경에서 **"필요해질 때까지 올리지 않는다"**는 원칙으로 동작하는 메모리 적재 방식이다. 전통적인 전체 적재 방식은 실행 전에 코드, [[001_dikw_pyramid|데이터]], 라이브러리까지 한꺼번에 메모리에 올리므로 준비 시간도 길고, 실제로 거의 쓰지 않는 영역까지 주기억장치를 점유한다. 반면 [[255_demand_paging|요구 페이징]]은 사용 빈도가 높은 일부 [[286_page_frame|페이지]]만 먼저 살아 있게 두고, 아직 [[316_reference_pattern_nosql|참조]]되지 않은 영역은 보조기억장치에 남겨 둔다.

이 방식이 필요해진 이유는 프로그램의 실제 사용 패턴이 매우 편중되어 있기 때문이다. 문서 편집기 전체가 500MB여도 사용자가 지금 당장 반복해서 쓰는 기능은 입력, 저장, 화면 갱신 같은 작은 부분에 집중된다. 즉 프로그램은 [[369_logic_bomb|논리]]적으로는 크지만, 순간적으로 뜨거운 작업 집합은 작다. [[255_demand_paging|요구 페이징]]은 이 편중성을 이용해 같은 16GB 물리 메모리에서도 더 많은 프로세스를 살려 두고, 시스템의 멀티프로그래밍 정도 ([[258_degree_of_multiprogramming|Degree of Multiprogramming]])를 높인다.

아래 그림은 "실행 전에 모두 싣는 방식"과 "접근 시점에 싣는 방식"의 차이를 보여준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                전체 적재 vs 요구 페이징의 자원 사용 방식                  │
├───────────────────────┬────────────────────────┬───────────────────────────┤
│ 구분                  │ 전체 적재              │ 요구 페이징               │
├───────────────────────┼────────────────────────┼───────────────────────────┤
│ 시작 시 메모리 사용   │ 프로그램 전체          │ 초기 필요 페이지 일부     │
│ 초기 실행 지연        │ 큼                     │ 작음                      │
│ 안 쓰는 코드의 점유   │ 그대로 유지            │ 접근 전까지 미적재        │
│ 메모리 압박 시 확장성 │ 낮음                   │ 상대적으로 높음           │
└───────────────────────┴────────────────────────┴───────────────────────────┘
```

핵심은 [[255_demand_paging|요구 페이징]]이 메모리를 공짜로 늘려 주는 기술이 아니라, **당장 필요한 것과 나중에 필요한 것을 시간적으로 분리**하는 기술이라는 점이다. 따라서 이 기법은 메모리 부족 자체를 없애는 해법이 아니라, 제한된 메모리를 더 영리하게 나누는 운영 [[268_strategy_pattern|전략]]으로 이해해야 한다.

- **📢 섹션 요약 비유**: [[255_demand_paging|요구 페이징]]은 이삿날 모든 짐을 한 번에 방 안에 쌓아 두는 대신, 오늘 바로 쓸 침대와 책상만 먼저 들여놓는 방식과 같다. 방은 덜 복잡해지고 생활은 빨리 시작되지만, 나중에 필요해진 짐은 창고에서 다시 가져와야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[255_demand_paging|요구 페이징]]이 동작하려면 중앙처리장치 (Central Processing Unit), 메모리 관리 장치 ([[284_mmu|Memory Management Unit]]), [[353_page_table|페이지 테이블]] ([[353_page_table|Page Table]]), [[001_operating_system_purpose|운영체제]] ([[001_operating_system_purpose|Operating System]]), 그리고 백킹 스토어 (Backing Store)가 역할을 나눠 가져야 한다. 중앙처리장치가 가상 주소를 [[316_reference_pattern_nosql|참조]]하면 메모리 관리 장치는 [[353_page_table|페이지 테이블]] 엔트리 ([[353_page_table|Page Table]] Entry)를 [[396_validation|확인]]한다. 이때 해당 엔트리에 존재 [[073_bit|비트]] 또는 유효 [[073_bit|비트]]가 "없음"으로 표시되어 있으면, 하드웨어는 이를 정상 접근이 아닌 **적재 요청 이벤트**로 해석해 [[720_page_fault_isr|페이지 폴트]]를 발생시킨다.

| 구성 요소 | 하는 일 | 설계상 중요 포인트 |
| :-- | :-- | :-- |
| 메모리 관리 장치 ([[284_mmu|Memory Management Unit]]) | 가상 주소를 해석하고 적재 여부 [[396_validation|확인]] | [[073_bit|비트]] 판정 속도, 변환 [[002_bigdata_5v|정확성]] |
| [[353_page_table|페이지 테이블]] 엔트리 ([[353_page_table|Page Table]] Entry) | 프레임 번호와 존재 여부 기록 | Present/Valid, Dirty, [[316_reference_pattern_nosql|Reference]] [[073_bit|비트]] |
| 자유 프레임 목록 (Free Frame List) | 비어 있는 물리 프레임 제공 | 부족 시 교체 [[164_policy|정책]]과 연동 |
| 백킹 스토어 (Backing Store) | 아직 메모리에 없는 [[286_page_frame|페이지]] 보관 | 디스크 [[015_지연_데이터_관점|지연]]시간이 전체 비용 좌우 |
| [[720_page_fault_isr|페이지 폴트]] 핸들러 | 적재·갱신·재실행 수행 | 예외 처리 순서와 [[194_consistency_database_integrity|일관성]] |

이 그림은 "주소 [[316_reference_pattern_nosql|참조]] → 부재 [[396_validation|확인]] → 적재 → 재실행"의 시간을 따라가며 [[255_demand_paging|요구 페이징]]의 실제 흐름을 보여준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                     요구 페이징의 동작 시퀀스                             │
├────────────────────────────────────────────────────────────────────────────┤
│ 1. CPU references virtual address                                          │
│        │                                                                   │
│        ▼                                                                   │
│ 2. MMU checks page table entry                                             │
│        │                                                                   │
│   Present=1 ───────────────▶ 바로 접근                                     │
│        │                                                                   │
│   Present=0                                                                │
│        ▼                                                                   │
│ 3. Page Fault trap to OS                                                   │
│        │                                                                   │
│ 4. OS finds free frame or selects victim page                              │
│        │                                                                   │
│ 5. Disk/SSD reads missing page into RAM                                    │
│        │                                                                   │
│ 6. Page table updated + instruction restarted                              │
└────────────────────────────────────────────────────────────────────────────┘
```

여기서 중요한 것은 [[720_page_fault_isr|페이지 폴트]]가 곧바로 실패를 뜻하지 않는다는 점이다. [[255_demand_paging|요구 페이징]]에서 [[720_page_fault_isr|페이지 폴트]]는 오히려 "이제 이 [[286_page_frame|페이지]]가 필요하다"는 신호다. 다만 그 비용이 크다. 메모리 접근이 대략 수십~수백 나노초 (ns) 수준이라면, 저장장치 접근은 수십 마이크로초 (μs)에서 밀리초 (ms)까지 늘어날 수 있다. 즉 [[255_demand_paging|요구 페이징]]은 **평소에는 절약하고, 필요 시 크게 지불하는 구조**다.

또 하나의 핵심은 적재 자체보다 **재실행의 투명성**이다. [[001_operating_system_purpose|운영체제]]는 필요한 [[286_page_frame|페이지]]를 올린 뒤 중단되었던 명령을 다시 실행해, 사용자와 프로세스 입장에서는 마치 처음부터 메모리에 있었던 것처럼 보이게 해야 한다. 이 투명성이 깨지면 [[381_virtual_memory|가상 메모리]]의 [[198_abstraction_control_data_process|추상화]] 자체가 무너진다.

- **📢 섹션 요약 비유**: [[255_demand_paging|요구 페이징]]은 도서관 서고 시스템과 같다. 서가에 없는 책을 찾으면 사서가 창고에서 가져다주고, 독자는 잠깐 기다린 뒤 같은 자리에서 독서를 이어 간다. 중요한 것은 책을 가져오는 순간보다, 독서 흐름이 다시 자연스럽게 이어지게 만드는 운영 방식이다.

---

## Ⅲ. 비교 및 연결

[[255_demand_paging|요구 페이징]]을 제대로 이해하려면 [[384_pure_demand_paging|순수 요구 페이징]] ([[384_pure_demand_paging|Pure Demand Paging]])과 선행 적재 또는 프리페이징 ([[385_prepaging|Prepaging]])을 함께 봐야 한다. [[384_pure_demand_paging|순수 요구 페이징]]은 한 번도 [[316_reference_pattern_nosql|참조]]되지 않은 [[286_page_frame|페이지]]를 절대 먼저 올리지 않으므로 메모리 낭비가 가장 적다. 반면 프리페이징은 곧 필요해질 가능성이 높은 인접 [[286_page_frame|페이지]]를 미리 가져와 [[459_quic_fec_forward_error_correction|초기]] [[720_page_fault_isr|페이지 폴트]] 연속 발생을 줄인다. 결국 차이는 **예측 실패 비용을 감수하고 미리 준비할 것인가, 아니면 예측 없이 꼭 필요할 때만 지불할 것인가**에 있다.

| 비교 항목 | [[384_pure_demand_paging|순수 요구 페이징]] | 프리페이징 |
| :-- | :-- | :-- |
| [[459_quic_fec_forward_error_correction|초기]] 적재량 | 최소 | 상대적으로 큼 |
| 첫 접근 [[015_지연_데이터_관점|지연]] | [[720_page_fault_isr|페이지 폴트]]가 자주 발생 가능 | 완화 가능 |
| 메모리 낭비 위험 | 낮음 | 예측 실패 시 존재 |
| 적합한 상황 | 지역성이 강한 일반 워크로드 | 연속 스캔, 반복 실행 패턴 |

이 비교는 [[253_locality_of_reference|참조의 지역성]]과 직접 연결된다. [[247_temporal_locality|시간적 지역성]] ([[247_temporal_locality|Temporal Locality]])이 강하면 한 번 가져온 [[286_page_frame|페이지]]를 반복해서 쓰므로 [[255_demand_paging|요구 페이징]]이 매우 효율적이다. [[248_spatial_locality|공간적 지역성]] ([[248_spatial_locality|Spatial Locality]])이 강하면 현재 [[286_page_frame|페이지]] 주변이 곧 필요해질 가능성이 높아 프리페이징이나 읽기 선행이 효과를 낸다. 반대로 랜덤 접근이 많은 대용량 [[070_graph_datastructure|그래프]] 탐색이나 메모리 압박 아래의 과도한 [[675_multitasking_terminology_preemptive|멀티태스킹]] 환경에서는 [[720_page_fault_isr|페이지 폴트]]가 연쇄적으로 터지며, [[255_demand_paging|요구 페이징]]의 이점이 급속히 사라진다.

[[255_demand_paging|요구 페이징]]은 또 다른 핵심 기술과도 연결된다. 변환 색인 버퍼 ([[291_tlb|Translation Lookaside Buffer]])는 주소 변환 속도를 높여 주지만, [[286_page_frame|페이지]] 자체가 없으면 결국 [[720_page_fault_isr|페이지 폴트]]를 막지 못한다. [[260_page_replacement|페이지 교체]] 알고리즘은 메모리가 꽉 찼을 때 누구를 내보낼지 결정하고, 작업 집합 모델 ([[416_working_set_model|Working Set Model]])은 현재 프로세스가 실제로 필요로 하는 [[286_page_frame|페이지]] 범위를 추정한다. 즉 [[255_demand_paging|요구 페이징]]은 혼자 성립하는 기술이 아니라, **주소 변환·교체 [[164_policy|정책]]·스케줄링·디스크 [[282_performance_tactics|성능]]**이 함께 받쳐 줄 때 비로소 효율을 낸다.

- **📢 섹션 요약 비유**: [[384_pure_demand_paging|순수 요구 페이징]]은 손님이 주문할 때만 요리하는 식당이고, 프리페이징은 점심시간 인기 메뉴를 조금 미리 준비하는 식당이다. 손님 흐름을 잘 맞히면 둘 다 효율적이지만, 손님이 예측과 다르게 몰리면 주방은 바로 바빠진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[255_demand_paging|요구 페이징]]은 대개 "메모리를 아끼는 기술"보다 "어떤 [[015_지연_데이터_관점|지연]]을 어디까지 허용할 것인가"의 문제로 다뤄진다. 예를 들어 웹 애플리케이션 서버는 기동 직후 첫 요청이 느릴 수 있는데, 이는 아직 자주 쓰일 코드 경로와 [[001_dikw_pyramid|데이터]] [[286_page_frame|페이지]]가 충분히 메모리에 올라오지 않았기 때문이다. 이런 경우 워밍업 요청을 미리 보내 주요 [[286_page_frame|페이지]]를 당겨 두면 사용자 체감 [[015_지연_데이터_관점|지연]]을 크게 줄일 수 있다. 반대로 [[003_dbms_database_management_system|데이터베이스 관리 시스템]] ([[501_database|Database]] [[372_management|Management]] System)은 자체 [[536_buffer_cache_page_cache|버퍼 캐시]]를 강하게 운용하므로, [[001_operating_system_purpose|운영체제]]의 [[255_demand_paging|요구 페이징]]에 지나치게 의존하면 예측 불가능한 [[015_지연_데이터_관점|지연]]이 늘 수 있다.

### 기술사 판단 [[435_checklist_based_testing|체크리스트]]

1. [[720_page_fault_isr|페이지 폴트]]가 대부분 경미한 부재 (Minor Fault)인지, 실제 저장장치 입출력 (Major Fault)을 동반하는지 구분했는가?
2. 저장장치가 비휘발성 메모리 익스프레스 ([[482_nvme|Non-Volatile Memory Express]]) 기반 [[475_ssd_structure|솔리드 스테이트 드라이브]] ([[327_ssd|Solid State Drive]])인지, [[015_지연_데이터_관점|지연]]이 큰 하드디스크 드라이브 (Hard Disk Drive)인지 [[396_validation|확인]]했는가?
3. 프로세스별 작업 집합이 물리 메모리 안에 유지되는지, 아니면 교체와 재적재가 반복되는지 관찰했는가?
4. 실시간 제어, 고빈도 거래, [[015_지연_데이터_관점|지연]] 민감 서비스처럼 [[720_page_fault_isr|페이지 폴트]] 자체를 허용하면 안 되는 구간이 있는가?

### 대표 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 물리 메모리 부족을 [[390_swap_space|스왑 공간]] 확대만으로 해결하려는 판단
- [[561_container_based_deployment|컨테이너]] 밀도를 높이기 위해 메모리 한계를 과도하게 낮춰 연속 [[720_page_fault_isr|페이지 폴트]]를 유발하는 배치
- 첫 요청 [[015_지연_데이터_관점|지연]] 문제를 애플리케이션 버그로만 보고, 실제 메모리 적재 패턴을 관찰하지 않는 운영

기술사 답안에서는 "[[255_demand_paging|요구 페이징]]은 항상 좋다"고 쓰면 부족하다. **지역성이 뚜렷하고 [[459_quic_fec_forward_error_correction|초기]] 적재 비용을 줄이고 싶을 때는 채택 가치가 크지만, [[015_지연_데이터_관점|지연]] 상한이 엄격하거나 작업 집합이 물리 메모리를 자주 넘는 환경에서는 적극적인 메모리 고정, 프리페치, [[536_buffer_cache_page_cache|버퍼 캐시]] 설계가 더 중요하다**고 판단해야 한다.

- **📢 섹션 요약 비유**: [[255_demand_paging|요구 페이징]]은 냉장고가 작은 식당의 운영 비법이 될 수 있지만, 손님이 몰리는 시간에 재료를 계속 창고에서 가져와야 하면 오히려 장사가 망한다. 결국 중요한 것은 냉장고 크기보다 손님 패턴을 읽고, 어떤 재료는 미리 꺼내 둘지 결정하는 운영 감각이다.

---

## Ⅴ. 기대효과 및 결론

잘 설계된 [[255_demand_paging|요구 페이징]]은 세 가지 효과를 만든다. 첫째, [[459_quic_fec_forward_error_correction|초기]] 적재량을 줄여 프로그램 시작 체감을 개선한다. 둘째, 물리 메모리를 실제 사용 [[286_page_frame|페이지]] 위주로 배분해 시스템 전체 처리량을 높인다. 셋째, [[322_logical_virtual_address|논리 주소]] 공간이 물리 메모리보다 크더라도 프로그램이 동작할 수 있게 해 소프트웨어 설계 자유도를 넓힌다. 이 때문에 [[255_demand_paging|요구 페이징]]은 현대 [[001_operating_system_purpose|운영체제]]의 기본값에 가깝다.

그러나 전제조건도 분명하다. 저장장치가 지나치게 느리거나, 지역성이 약하거나, 동시에 실행되는 프로세스의 작업 집합 합이 물리 메모리를 지속적으로 초과하면 [[255_demand_paging|요구 페이징]]은 즉시 병목으로 변한다. 비휘발성 저장장치가 빨라져도 메모리와 저장장치 사이의 속도 차는 여전히 크므로, [[255_demand_paging|요구 페이징]]이 메모리 설계 문제를 근본적으로 없애 주지는 못한다.

따라서 [[255_demand_paging|요구 페이징]]은 "디스크를 메모리처럼 쓰는 마법"으로 기억하면 안 된다. 더 정확한 기억법은 **"지역성을 믿고 메모리 적재 시점을 뒤로 미루는 [[001_operating_system_purpose|운영체제]]의 확률적 [[268_strategy_pattern|전략]]"**이다. 이 관점으로 보면 왜 [[720_page_fault_isr|페이지 폴트]]율, 작업 집합, 교체 [[164_policy|정책]], 저장장치 [[282_performance_tactics|성능]]이 함께 중요해지는지도 자연스럽게 이해된다.

- **📢 섹션 요약 비유**: [[255_demand_paging|요구 페이징]]은 작은 가방으로 긴 여행을 떠나는 기술이다. 짐을 적게 들고 빨리 출발할 수 있지만, 여행 동선이 엉키면 숙소와 보관함을 계속 오가느라 시간만 잃게 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [[381_virtual_memory|가상 메모리]] ([[381_virtual_memory|Virtual Memory]]) | [[255_demand_paging|요구 페이징]]은 [[381_virtual_memory|가상 메모리]]를 현실적으로 구현하는 대표 적재 [[164_policy|정책]]이다. |
| [[720_page_fault_isr|페이지 폴트]] ([[387_page_fault|Page Fault]]) | [[255_demand_paging|요구 페이징]]이 필요한 [[286_page_frame|페이지]]를 불러오는 공식 진입 이벤트다. |
| [[260_page_replacement|페이지 교체]] ([[260_page_replacement|Page Replacement]]) | 자유 프레임이 없을 때 어떤 [[286_page_frame|페이지]]를 내보낼지 결정해 [[255_demand_paging|요구 페이징]]의 지속 가능성을 좌우한다. |
| 작업 집합 ([[265_working_set|Working Set]]) | 현재 시점에 실제로 필요한 [[286_page_frame|페이지]] 범위를 설명해 [[255_demand_paging|요구 페이징]]의 성공 여부를 가늠하게 한다. |
| [[257_thrashing|스래싱]] ([[257_thrashing|Thrashing]]) | [[255_demand_paging|요구 페이징]]이 지역성을 잃고 입출력 폭주 상태로 붕괴한 결과다. |
| 프리페이징 ([[385_prepaging|Prepaging]]) | [[255_demand_paging|요구 페이징]]의 [[459_quic_fec_forward_error_correction|초기]] [[015_지연_데이터_관점|지연]]을 줄이기 위해 일부 [[286_page_frame|페이지]]를 선제 적재하는 보완 [[268_strategy_pattern|전략]]이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
전체 적재 중심 메모리 운영
        │
        ▼
가상 메모리 (Virtual Memory)
        │
        ▼
요구 페이징 (Demand Paging)
        │
        ├──▶ 페이지 폴트 처리 (Page Fault Handling)
        │
        ├──▶ 페이지 교체 (Page Replacement)
        │
        ▼
작업 집합 · 스래싱 제어 · 프리페이징
        │
        ▼
지연 민감 워크로드별 메모리 최적화
```

이 흐름은 단순 적재에서 시작해, 필요한 순간만 적재하고, 이후에는 폴트 처리와 교체 [[164_policy|정책]], 작업 집합 제어까지 확장되는 [[001_operating_system_purpose|운영체제]] 메모리 관리의 발전 축을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[255_demand_paging|요구 페이징]]은 학교에 갈 때 모든 책을 다 들고 가지 않고, 오늘 바로 볼 책만 먼저 챙기는 방법이에요.
2. 수업하다가 안 가져온 책이 필요하면 잠깐 책장에서 가져와야 해서 조금 기다리게 돼요.
3. 그래서 가방은 가벼워지지만, 자꾸 책장을 오가게 되면 오히려 공부 흐름이 끊길 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 297 / 803

← **이전**: [[296_paging_segmentation_hybrid|296. 페이징과 세그멘테이션 혼용 (Paging-Segmentation Hybrid)]]
**다음**: [[298_page_fault|298. 페이지 부재 (Page Fault)]] →

---
