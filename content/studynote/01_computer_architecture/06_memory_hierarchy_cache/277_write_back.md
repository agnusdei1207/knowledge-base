---
title: "277. Write-Back (나중 쓰기)"
date: "2026-04-20"
tags:
  - "studynote-computer-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Write-Back (나중 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))은 CPU (Central Processing Unit)가 쓴 값을 먼저 캐시에만 반영하고, 나중에 캐시 라인이 교체될 때 하위 메모리로 내려보내는 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이다.
> 2. **가치**: 같은 주소를 여러 번 갱신하는 동안 메모리 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 왕복을 줄여 평균 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 소모를 크게 낮춘다.
> 3. **판단 포인트**: 빠른 대신 캐시와 메모리 내용이 잠시 달라지므로, [더티 비트](/studynote/01_computer_architecture/06_memory_hierarchy_cache/278_dirty_bit/) ([Dirty Bit](/studynote/02_operating_system/07_virtual_memory/396_dirty_bit/)), [캐시 일관성](/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/), 플러시 제어를 함께 설계해야 안전하다.

---

## Ⅰ. 개요 및 필요성

Write-Back은 캐시의 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 중 하나로, 수정된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 메인 메모리에 즉시 기록하지 않고 캐시 내부에 머물게 두는 방식이다. 핵심 목적은 빠른 캐시와 느린 [DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/) (Dynamic Random Access Memory) 사이의 속도 차이를 완화하는 데 있다. CPU가 루프 안에서 같은 변수나 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) 원소를 반복 갱신할 때마다 메모리까지 매번 내려가면, 실제 계산보다 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 대기 시간이 더 커질 수 있다.

이 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 필요한 이유는 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 연산의 대부분이 "한 번 쓰고 끝"이 아니라 "같은 블록을 짧은 시간 안에 여러 번 수정"하는 형태로 나타나기 때문이다. 예를 들어 [카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) 증가, [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 프레임 갱신, 객체 필드 업데이트는 같은 캐시 라인 안에서 연속적으로 일어난다. 이때 매번 DRAM에 쓰는 Write-Through보다, 캐시 안에서 변경을 흡수했다가 마지막 상태만 반영하는 Write-Back이 훨씬 효율적이다.

아래 그림은 Write-Back이 "매번 쓰지 않고, 퇴출 시점에 몰아서 쓴다"는 시간축상의 차이를 보여준다.

```text
+--------------------------------------------------------------------------+
|               Write-Back의 핵심: 수정은 즉시, 메모리 반영은 나중        |
+--------------------------------------------------------------------------+
| CPU Store #1     CPU Store #2     CPU Store #3             Eviction     |
|     |                |                |                      |           |
|     v                v                v                      v           |
| Cache Line:   clean ---> dirty --------> dirty ---------------> writeback  |
| Main Memory:  old   -----------------------------------------> final data |
+--------------------------------------------------------------------------+
```

즉 Write-Back은 "[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 자체를 없애는" 기술이 아니라, 여러 번의 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 하나의 메모리 반영으로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)하는 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이다. 대신 그 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 구간 동안 메모리에는 구버전이 남아 있으므로, 시스템은 어느 쪽이 최신인지 정확히 추적할 장치를 반드시 가져야 한다.

- **📢 섹션 요약 비유**: Write-Back은 메모를 고칠 때마다 본사 문서함에 보내지 않고, 내 책상 초안에 계속 수정하다가 최종본만 한 번 제출하는 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Write-Back 캐시는 단순히 "나중에 쓰자"고 선언하는 것으로 끝나지 않는다. 각 캐시 라인은 자신이 수정되었는지 표시하는 [더티 비트](/studynote/01_computer_architecture/06_memory_hierarchy_cache/278_dirty_bit/) ([Dirty Bit](/studynote/02_operating_system/07_virtual_memory/396_dirty_bit/))를 가져야 하고, 교체 시점에는 그 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 검사해 하위 계층으로 실제 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 동작을 수행해야 한다. 또한 이 순간의 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 줄이기 위해 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 버퍼 (Write Buffer)를 두는 경우가 많다.

| 구성 요소 | 역할 | 설계 핵심 |
| :-- | :-- | :-- |
| [더티 비트](/studynote/01_computer_architecture/06_memory_hierarchy_cache/278_dirty_bit/) ([Dirty Bit](/studynote/02_operating_system/07_virtual_memory/396_dirty_bit/)) | 메모리와 다른 최신 사본 여부 표시 | 1이면 퇴출 전 반드시 반영 |
| 태그 (Tag) / 유효 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) (Valid [Bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/)) | 어떤 메모리 블록인지 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | 히트/미스 판단 정확도 |
| [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 버퍼 (Write Buffer) | 퇴출 시 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 완화 | CPU 정지 시간 최소화 |
| 교체 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) ([LRU](/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/), [Least Recently Used](/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) 등) | 어떤 라인을 밀어낼지 결정 | 더티 라인 퇴출 비용 고려 |

다음 그림은 Write-Back에서 실제 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 요청이 처리되는 내부 흐름을 요약한다.

```text
+-----------------------------------------------------------------------+
|                  Write-Back 캐시의 쓰기 처리 순서                    |
+-----------------------------------------------------------------------+
| 1) CPU store                                                         |
|      |                                                               |
|      v                                                               |
| 2) Cache hit? -- 아니오 ---> 블록 적재(보통 Write Allocate)           |
|      | 예                                                            |
|      v                                                               |
| 3) 캐시 데이터 갱신                                                  |
|      |                                                               |
|      v                                                               |
| 4) Dirty Bit = 1 설정                                                |
|      |                                                               |
|      v                                                               |
| 5) 라인 교체 시 Dirty 검사 -- 0 ---> 그냥 폐기                        |
|                         |                                             |
|                         +- 1 ---> Write Buffer ---> 하위 메모리 기록    |
+-----------------------------------------------------------------------+
```

여기서 중요한 병목은 "평상시 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)"가 아니라 "더티 라인이 쫓겨나는 순간"이다. 캐시 미스가 발생해 새 블록을 넣어야 하는데 희생 라인이 더티 상태라면, 먼저 그 라인을 메모리로 내려보내야 자리를 비울 수 있다. 그래서 고성능 프로세서는 퇴출 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 버퍼에 넘겨 백그라운드로 처리하고, 앞단의 파이프라인은 가능한 빨리 다음 명령으로 넘어가게 만든다.

또 하나의 실전 포인트는 Write-Back이 대개 Write Allocate와 짝을 이룬다는 점이다. [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 미스가 났을 때 해당 블록을 캐시에 가져와 수정해야, 이후 반복 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 캐시 안에서 흡수할 수 있기 때문이다. 즉 Write-Back은 단일 명령 최적화가 아니라, "앞으로 또 접근할 가능성"까지 반영한 지역성 중심 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이다.

- **📢 섹션 요약 비유**: Write-Back 캐시는 공사 현장의 임시 창고와 같다. 자재를 바로 본사로 되돌려 보내지 않고 현장에 쌓아 두었다가, 공사가 끝나거나 자리가 필요할 때 한꺼번에 정리한다.

---

## Ⅲ. 비교 및 연결

Write-Back의 의미는 다른 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)과 비교할 때 더 선명해진다. 가장 대표적인 비교 대상은 Write-Through이다. Write-Through은 쓰는 즉시 하위 메모리까지 반영하므로 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 단순하지만, [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 트래픽이 많을수록 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 부담이 빠르게 커진다. 반대로 Write-Back은 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 부담을 줄이는 대신 "최신 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 지금 캐시에만 존재한다"는 상태를 허용한다.

| 비교 항목 | Write-Back | [Write-Through](/studynote/01_computer_architecture/06_memory_hierarchy_cache/276_write_through/) |
| :-- | :-- | :-- |
| 메모리 반영 시점 | 캐시 라인 퇴출 시 | 각 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 시점마다 즉시 |
| 평균 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 트래픽 | 적음 | 많음 |
| 하드웨어 복잡도 | 높음 | 상대적으로 단순 |
| 전원 차단 시 위험 | 캐시 내 최신 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유실 가능 | 메모리 반영 완료 가능성 높음 |
| 멀티코어 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 부담 | 큼 | 상대적으로 작음 |

이 차이는 단순한 취향 문제가 아니라 시스템 계층 전체에 영향을 준다. 멀티코어에서는 코어 A의 캐시에만 최신 값이 있고 메모리에는 옛값이 남아 있을 수 있으므로, MESI (Modified, Exclusive, Shared, Invalid) 같은 [캐시 일관성](/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이 필요하다. 또 [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) ([Direct Memory Access](/studynote/01_computer_architecture/08_io_storage_systems/318_dma/)) 장치가 메모리를 직접 읽고 쓰는 상황에서는, CPU 캐시에만 남은 더티 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 플러시하지 않으면 장치가 오래된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보게 된다.

정리하면 Write-Back은 캐시 구조 하나의 옵션이 아니라, 메모리 계층·[버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)·입출력·멀티코어 설계와 연결되는 선택이다. 그래서 시험이나 실무에서 Write-Back을 설명할 때는 단순히 "빠르다"고 끝내지 말고, 왜 그 빠름이 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 관리 비용으로 되돌아오는지까지 함께 말해야 한다.

- **📢 섹션 요약 비유**: Write-Through가 수정할 때마다 가족 단톡방에 바로 공지하는 방식이라면, Write-Back은 내 수첩에 먼저 적어 두었다가 나중에 공식 공지하는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 Write-Back은 범용 CPU의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 캐시에서 거의 기본 선택이지만, 모든 영역에 무조건 좋은 것은 아니다. 읽고 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 반복되는 일반 메모리에는 매우 유리하지만, 장치 제어 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 같은 MMIO (Memory-Mapped I/O) 영역에는 부적합할 수 있다. 장치 입장에서는 "나중에"가 아니라 "지금 즉시" 명령이 도착해야 하기 때문이다.

### 실무 판단 체크포인트

1. <strong>반복 갱신 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>인가?</strong>
   같은 블록을 여러 번 수정한다면 Write-Back 효과가 크다.
2. **외부 장치와 메모리를 공유하는가?**
   [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/), [네트워크 인터페이스 카드](/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/) ([NIC](/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/), Network Interface Card), 그래픽 처리 장치 ([GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/), [Graphics Processing Unit](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))와 버퍼를 공유한다면 캐시 플러시/무효화 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 반드시 필요하다.
3. <strong>장애 시 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 유실이 치명적인가?</strong>
   전원 차단 직전 캐시에만 남은 최신 값은 사라질 수 있으므로, [영속성](/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/) 계층에서는 별도 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)가 필요하다.

### 대표 시나리오

- **고성능 일반 연산**: 루프 안에서 구조체 필드를 수천 번 갱신하는 경우, Write-Back은 메모리 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 사용을 크게 줄인다.
- <strong><a href="/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/">DMA</a> 전송 전후 <a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a></strong>: 드라이버는 전송 시작 전 더티 라인을 메모리로 밀어내고, 전송 후에는 캐시를 무효화해 장치가 쓴 최신 값을 CPU가 다시 읽게 해야 한다.
- **지속성 보장 시스템**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스나 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템은 캐시 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)만 믿지 않고, 배리어·flush 명령·저널링으로 영속 기록 시점을 명시적으로 통제한다.

### 피해야 할 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- MMIO 영역을 일반 캐시 가능 메모리처럼 Write-Back으로 취급하는 설계
- 멀티코어 공유 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 비용을 무시한 단순 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 가정
- "캐시에 있으니 저장된 것"으로 착각해 [영속성](/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/) 보장을 생략하는 설계

결국 기술사 관점의 답안 포인트는 명확하다. <strong>Write-Back은 <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 최적화 <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>이지, <a href="/studynote/09_security/01_intro_principles/003_integrity/">무결성</a> 보증 <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>이 아니다.</strong> 따라서 채택 여부는 "[버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 절감 이익"과 "[일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 관리 비용"을 함께 비교해 판단해야 한다.

- **📢 섹션 요약 비유**: Write-Back은 손님이 많은 식당에서 주문서를 주방 앞 보드에 먼저 모아 적는 방식과 같다. 빠르지만, 배달 기사나 다른 주방이 함께 볼 때는 최신 주문인지 꼭 맞춰줘야 혼선이 없다.

---

## Ⅴ. 기대효과 및 결론

Write-Back의 가장 큰 효과는 메모리 계층의 병목을 줄여 CPU가 계산에 더 오래 집중하게 만든다는 점이다. 특히 [시간적 지역성](/studynote/01_computer_architecture/06_memory_hierarchy_cache/247_temporal_locality/) ([Temporal Locality](/studynote/01_computer_architecture/06_memory_hierarchy_cache/247_temporal_locality/))이 높은 워크로드에서는 여러 번의 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 캐시 내부 변경으로 흡수하므로, 체감 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 전력 효율이 함께 좋아진다. [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 사용량이 줄어들면 다른 코어와 장치가 같은 메모리 시스템을 공유할 때도 여유가 커진다.

하지만 이 효과는 어디까지나 조건부다. 더티 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 추적, 교체 시점 처리, 멀티코어 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) 연동, 전원 장애 대응이 모두 뒷받침되어야 한다. 즉 Write-Back은 "빠른 대신 복잡한" [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이며, 그 복잡성을 감당할 구조가 있을 때 비로소 장점이 실현된다.

미래 확장 관점에서는 대용량 멀티코어, 비휘발성 메모리, [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) ([Compute Express Link](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/)) 같은 계층 확장에서 이 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)의 의미가 더 커질 수 있다. 다만 계층이 많아질수록 "어디에 최신 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 있는가"를 맞추는 비용도 함께 증가한다. 따라서 Write-Back은 <strong>캐시가 메모리를 대신 저장해 주는 기술</strong>이 아니라, <strong>최신 상태를 잠시 위임받아 <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>을 벌어 주는 기술</strong>로 기억하는 것이 정확하다.

- **📢 섹션 요약 비유**: Write-Back은 고속도로 진입 전에 차량을 잠깐 모아 흐름을 정리해 주는 램프미터와 같다. 교통량은 빨라지지만, [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 체계를 제대로 운영해야만 전체가 안전하게 흐른다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| Write Allocate | [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 미스 시 블록을 캐시로 가져와 Write-Back 효과를 높이는 짝 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| [더티 비트](/studynote/01_computer_architecture/06_memory_hierarchy_cache/278_dirty_bit/) ([Dirty Bit](/studynote/02_operating_system/07_virtual_memory/396_dirty_bit/)) | 메모리보다 캐시가 최신임을 나타내는 핵심 상태 정보 |
| MESI (Modified, Exclusive, Shared, Invalid) | 멀티코어에서 Write-Back 캐시의 최신성 충돌을 조정하는 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
| [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) ([Direct Memory Access](/studynote/01_computer_architecture/08_io_storage_systems/318_dma/)) | 캐시를 우회해 메모리에 직접 접근하므로 플러시/무효화와 연결 |
| Flush / Fence | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)된 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 관찰 가능한 순서로 강제하는 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 수단 |

### 📈 관련 키워드 및 발전 흐름도

```text
Write-Through 중심의 단순 일관성
        |
        v
Write-Back + 더티 비트 (Dirty Bit)
        |
        v
Write Allocate + 쓰기 버퍼 (Write Buffer)
        |
        v
MESI 기반 멀티코어 캐시 일관성
        |
        v
DMA 동기화 · Flush/Fence · 확장 메모리 계층
```

이 흐름은 "즉시 기록"에서 출발해 "[지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 기록 + 상태 추적 + 시스템 차원의 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)"로 설계 관심사가 확장되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. Write-Back은 숙제를 고칠 때마다 선생님께 바로 보여주지 않고, 내 공책에서 여러 번 고친 뒤 마지막에만 보여주는 거예요.
2. 그래서 빨리 고칠 수 있지만, 선생님 책상에는 잠깐 동안 옛날 답이 남아 있을 수 있어요.
3. 그래서 컴퓨터는 "이 공책이 최신이야!"라는 표시를 붙여 두고, 나중에 꼭 정답을 옮겨 적어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 277 / 803

<- **이전**: [276. Write-Through (동시 쓰기)](/studynote/01_computer_architecture/06_memory_hierarchy_cache/276_write_through/)
**다음**: [278. 더티 비트 (Dirty Bit)](/studynote/01_computer_architecture/06_memory_hierarchy_cache/278_dirty_bit/) ->

---
