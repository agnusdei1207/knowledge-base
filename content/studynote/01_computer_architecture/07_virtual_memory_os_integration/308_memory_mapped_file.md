---
title: 308. 메모리 맵 파일 (Memory-Mapped File)
date: '2026-04-20'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[131_mmap_ipc|메모리 맵 파일]] (Memory-Mapped [[501_file_definition_logical_record|File]])은 [[501_file_definition_logical_record|파일]]을 "읽어 와서 복사하는 대상"이 아니라, 프로세스의 [[382_virtual_address_space|가상 주소 공간]] 안에 직접 연결되는 메모리 구간으로 다루게 만드는 [[001_operating_system_purpose|운영체제]] 기법이다.
> 2. **가치**: 이 방식은 `read()`/`write()` 중심 입출력보다 복사 횟수와 시스템 콜 빈도를 줄여, 대용량 [[501_file_definition_logical_record|파일]]의 무작위 접근과 프로세스 간 공유를 훨씬 자연스럽게 만든다.
> 3. **판단 포인트**: 빠르다는 이유만으로 항상 유리한 것은 아니며, [[387_page_fault|페이지 부재]] ([[387_page_fault|Page Fault]]) 비용·[[212_synchronization_mechanisms|동기화]]·[[015_지연_데이터_관점|지연]]시간 예측 가능성까지 감당할 수 있을 때 진짜 이점이 난다.

---

## Ⅰ. 개요 및 필요성

[[131_mmap_ipc|메모리 맵 파일]] (Memory-Mapped [[501_file_definition_logical_record|File]])은 디스크 [[501_file_definition_logical_record|파일]]의 일부 또는 전체를 프로세스의 [[382_virtual_address_space|가상 주소 공간]]에 매핑하여, [[501_file_definition_logical_record|파일]] 접근을 메모리 접근처럼 보이게 만드는 방식이다. 즉 응용 프로그램은 [[501_file_definition_logical_record|파일]]을 "버퍼에 복사해 둔 [[001_dikw_pyramid|데이터]]"가 아니라, 포인터로 바로 [[316_reference_pattern_nosql|참조]]할 수 있는 주소 범위로 인식한다. 여기서 핵심은 [[501_file_definition_logical_record|파일]]과 메모리의 경계를 없애는 것이 아니라, **[[001_operating_system_purpose|운영체제]]가 그 경계를 뒤에서 대신 관리한다는 점**이다.

이 개념이 필요한 이유는 전통적인 [[501_file_definition_logical_record|파일]] 입출력이 두 가지 비용을 반복해서 만들기 때문이다. 첫째, 사용자 코드가 [[501_file_definition_logical_record|파일]]을 읽을 때마다 [[022_kernel_role|커널]] 모드 전환과 시스템 콜 오버헤드가 생긴다. 둘째, [[286_page_frame|페이지]] 캐시 ([[286_page_frame|Page]] Cache)에 올라온 [[001_dikw_pyramid|데이터]]를 다시 사용자 버퍼로 복사해야 하므로, 대용량 [[501_file_definition_logical_record|파일]]이나 무작위 접근에서는 CPU (Central Processing Unit)와 메모리 대역폭이 불필요하게 소모된다. [[131_mmap_ipc|메모리 맵 파일]]은 이 과정을 "필요한 [[286_page_frame|페이지]]를 필요한 시점에 주소 공간으로 연결"하는 방식으로 바꿔 낭비를 줄인다.

특히 [[002_database_definition|데이터베이스]] [[154_database_index_b_tree_search_optimization|인덱스]], 실행 [[501_file_definition_logical_record|파일]] 로딩, [[119_log_analysis|로그 분석]], 이미지 처리처럼 [[501_file_definition_logical_record|파일]]의 일부분을 자주 건너뛰며 읽는 작업에서 효과가 크다. 반대로 작은 [[501_file_definition_logical_record|파일]]을 잠깐 읽고 끝내는 단순 작업에서는 매핑 설정과 [[353_page_table|페이지 테이블]] 관리 비용이 오히려 더 비쌀 수 있다. 그래서 [[131_mmap_ipc|메모리 맵 파일]]은 만능 입출력 기법이 아니라, **[[381_virtual_memory|가상 메모리]]의 강점을 [[501_file_definition_logical_record|파일]] 시스템까지 확장하는 선택지**로 이해해야 한다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│            왜 mmap이 필요한가: 복사 중심 I/O를 주소 중심 I/O로 전환         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 전통적 read()                                                               │
│   디스크 ─▶ 페이지 캐시 ─▶ 사용자 버퍼 ─▶ 애플리케이션 해석                │
│             (커널 관리)     (한 번 더 복사)                                 │
│                                                                             │
│ 메모리 맵 파일                                                              │
│   디스크 ─▶ 페이지 캐시 ─▶ 가상 주소 공간에 매핑 ─▶ 애플리케이션 접근       │
│             (커널 관리)       (포인터처럼 참조)                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

이 그림의 포인트는 "디스크가 RAM으로 바뀐다"가 아니라, 응용 프로그램이 **[[286_page_frame|페이지]] 캐시를 주소 공간의 일부처럼 바라보게 된다**는 데 있다. 그래서 [[131_mmap_ipc|메모리 맵 파일]]은 [[501_file_definition_logical_record|파일]] 시스템 기술이면서 동시에 [[381_virtual_memory|가상 메모리]] 기술이다.

- **📢 섹션 요약 비유**: [[131_mmap_ipc|메모리 맵 파일]]은 창고 물건을 매번 복사해 책상 위에 올리는 대신, 책상 옆에 창고 선반을 바로 붙여 놓는 것과 같다. 물건을 가지러 다니는 수고가 줄지만, 선반 정리 규칙은 여전히 창고 관리자가 맡는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[131_mmap_ipc|메모리 맵 파일]]의 핵심 구성 요소는 프로세스의 [[381_virtual_memory|가상 메모리]] 영역, [[353_page_table|페이지 테이블]], [[328_mmu|MMU]] ([[284_mmu|Memory Management Unit]]), [[286_page_frame|페이지]] 캐시, 그리고 [[501_file_definition_logical_record|파일]] 시스템이다. `mmap()` 호출이 일어나는 순간 실제 [[501_file_definition_logical_record|파일]] 전체가 RAM (Random Access Memory)에 올라오는 것은 아니다. [[001_operating_system_purpose|운영체제]]는 "이 주소 구간은 이 [[501_file_definition_logical_record|파일]]의 몇 번째 오프셋과 연결된다"는 메타데이터를 먼저 만들고, 실제 내용은 접근 시점에 늦게 가져온다.

이 때문에 [[131_mmap_ipc|메모리 맵 파일]]은 [[255_demand_paging|요구 페이징]] ([[255_demand_paging|Demand Paging]])과 같은 흐름으로 동작한다. 프로세스가 아직 적재되지 않은 매핑 영역을 읽거나 쓰면 [[387_page_fault|페이지 부재]]가 발생하고, [[022_kernel_role|커널]]은 [[501_file_definition_logical_record|파일]]의 해당 [[286_page_frame|페이지]]를 [[286_page_frame|페이지]] 캐시에 올린 뒤 [[353_page_table|페이지 테이블]]을 갱신한다. 그다음 같은 주소를 다시 실행하면 CPU는 이를 평범한 메모리 접근처럼 처리한다. 즉 `mmap()`의 빠름은 "초기에 다 읽어서 빠른 것"이 아니라, **필요한 [[286_page_frame|페이지]]만 늦게 읽고 이후에는 주소 [[316_reference_pattern_nosql|참조]]로 재사용하기 때문에 빠른 것**이다.

아래 다이어그램은 [[131_mmap_ipc|메모리 맵 파일]]의 실제 처리 경로를 보여 준다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                 메모리 맵 파일의 처리 흐름: 매핑은 먼저, 적재는 나중         │
├─────────────────────────────────────────────────────────────────────────────┤
│ Application                                                                  │
│    │                                                                          │
│    ├─ mmap(fd, offset, length)                                                │
│    ▼                                                                          │
│ Virtual Memory Area 생성                                                      │
│    │                                                                          │
│    ▼                                                                          │
│ Page Table에 "파일과 연결된 주소 범위" 등록                                   │
│    │                                                                          │
│    ▼                                                                          │
│ 첫 접근(load/store)                                                           │
│    │                                                                          │
│    ├─ page present ───────────────────────────────────────────────▶ 바로 접근  │
│    │                                                                          │
│    └─ page absent                                                             │
│          │                                                                    │
│          ▼                                                                    │
│     Page Fault                                                                │
│          │                                                                    │
│          ▼                                                                    │
│     OS Kernel이 파일 오프셋 확인                                               │
│          │                                                                    │
│          ▼                                                                    │
│     Page Cache 적재 + Page Table 갱신                                          │
│          │                                                                    │
│          ▼                                                                    │
│     명령 재시작 후 메모리처럼 접근                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | [[282_performance_tactics|성능]]상 의미 |
| :--- | :--- | :--- |
| [[381_virtual_memory|가상 메모리]] 영역 ([[428_vma_struct|Virtual Memory Area]]) | [[501_file_definition_logical_record|파일]]과 주소 범위의 관계를 기록 | 사용자 입장에서 [[501_file_definition_logical_record|파일]]을 포인터처럼 다루게 함 |
| [[353_page_table|페이지 테이블]] ([[353_page_table|Page Table]]) | 가상 [[286_page_frame|페이지]]와 물리 프레임의 현재 연결 상태 관리 | 적재 여부와 권한 검사 지점 |
| [[286_page_frame|페이지]] 캐시 ([[286_page_frame|Page]] Cache) | [[501_file_definition_logical_record|파일]] [[001_dikw_pyramid|데이터]]를 메모리에 유지 | `read()`와 `mmap()`이 공유하는 실체 |
| [[387_page_fault|페이지 부재]] 처리기 | 미적재 [[286_page_frame|페이지]]를 [[501_file_definition_logical_record|파일]]에서 불러옴 | 최초 접근 [[015_지연_데이터_관점|지연]]의 원인 |
| `msync()` 또는 언매핑 | 변경 내용을 디스크와 정합 | [[289_cqrs_db|쓰기]] [[015_지연_데이터_관점|지연]]과 내구성 판단 포인트 |

여기서 중요한 기술적 차이는 읽기와 [[289_cqrs_db|쓰기]]의 의미다. 읽기 매핑은 [[501_file_definition_logical_record|파일]] 내용을 그대로 [[316_reference_pattern_nosql|참조]]하지만, [[289_cqrs_db|쓰기]] 가능한 공유 매핑은 Dirty Page를 만들어 나중에 [[501_file_definition_logical_record|파일]]로 반영할 수 있다. 반대로 사적 매핑은 복사-[[289_cqrs_db|쓰기]] ([[542_cow_file_system|Copy-on-Write]])를 이용해 원본 [[501_file_definition_logical_record|파일]]을 바꾸지 않고 프로세스 내부 변경만 유지한다. 따라서 [[131_mmap_ipc|메모리 맵 파일]]은 "빠른 [[501_file_definition_logical_record|파일]] 접근"을 넘어, **공유할 것인지, 격리할 것인지, 언제 영속화할 것인지까지 선택하는 메커니즘**이다.

- **📢 섹션 요약 비유**: [[131_mmap_ipc|메모리 맵 파일]]은 대형 쇼핑몰 안내도와 같다. 지도를 받아 두는 순간 모든 가게 물건이 집으로 오는 것은 아니고, 실제로 그 층에 가 봐야 물건을 보게 된다. 하지만 한 번 길을 익히면 다음부터는 매번 안내 데스크에 묻지 않아도 된다.

---

## Ⅲ. 비교 및 연결

[[131_mmap_ipc|메모리 맵 파일]]을 이해하려면 전통적인 `read()`/`write()` 방식, [[118_shared_memory|공유 메모리]], 실행 [[501_file_definition_logical_record|파일]] 로딩과 함께 봐야 한다. 같은 [[501_file_definition_logical_record|파일]] 접근이라도 접근 패턴과 [[212_synchronization_mechanisms|동기화]] 방식이 다르면 장점과 위험이 완전히 달라지기 때문이다. 특히 [[131_mmap_ipc|메모리 맵 파일]]의 진짜 강점은 "순차 읽기 최적화"보다 **무작위 접근과 공유된 주소 해석**에 있다.

| 비교 축 | `read()` / `write()` 기반 I/O | [[131_mmap_ipc|메모리 맵 파일]] (Memory-Mapped [[501_file_definition_logical_record|File]]) |
| :--- | :--- | :--- |
| 프로그래밍 모델 | 명시적으로 버퍼를 채우고 비움 | 포인터/배열처럼 직접 [[316_reference_pattern_nosql|참조]] |
| 시스템 콜 빈도 | 접근할수록 반복 증가 | 매핑 시 1회, 이후 [[387_page_fault|페이지 부재]] 중심 |
| 복사 비용 | [[286_page_frame|페이지]] 캐시 → 사용자 버퍼 복사 필요 | 복사 최소화, [[286_page_frame|페이지]] 캐시 직접 [[316_reference_pattern_nosql|참조]] |
| 무작위 접근 | `lseek()` + `read()` 반복 부담 큼 | 주소 계산만으로 접근 가능 |
| [[015_지연_데이터_관점|지연]]시간 예측 | 비교적 명시적 | [[387_page_fault|페이지 부재]] 시 급격한 [[015_지연_데이터_관점|지연]] 가능 |
| [[212_synchronization_mechanisms|동기화]] 책임 | [[014_api_posix|API]] 호출 경계가 분명 | 메모리 공유처럼 보이므로 더 주의 필요 |

이 차이는 다른 컴퓨터구조 개념과도 이어진다. [[131_mmap_ipc|메모리 맵 파일]]은 MMU와 [[353_page_table|페이지 테이블]] 없이는 성립하지 않으며, [[352_page_size|페이지 크기]] ([[352_page_size|Page Size]])가 커지면 한 번의 [[387_page_fault|페이지 부재]]가 가져오는 [[001_dikw_pyramid|데이터]] 양도 달라진다. 또한 [[257_thrashing|스래싱]] ([[257_thrashing|Thrashing]])이 심한 환경에서는 `mmap()`이 오히려 폭발적인 [[387_page_fault|페이지 부재]]를 일으켜 [[282_performance_tactics|성능]]을 더 나쁘게 만들 수 있다. 즉 [[131_mmap_ipc|메모리 맵 파일]]은 독립적인 입출력 API가 아니라, **[[381_virtual_memory|가상 메모리]] [[164_policy|정책]]을 그대로 끌어안는 [[501_file_definition_logical_record|파일]] 접근 [[268_strategy_pattern|전략]]**이다.

[[001_operating_system_purpose|운영체제]] 관점에서는 실행 [[501_file_definition_logical_record|파일]] 로딩이 대표적 사례다. 프로그램을 실행할 때 [[022_kernel_role|커널]]은 바이너리 전체를 복사해 두기보다, 코드 섹션과 라이브러리를 메모리 맵 형태로 걸어 놓고 필요한 [[286_page_frame|페이지]]부터 적재한다. [[002_database_definition|데이터베이스]]나 검색 엔진도 비슷하게 대형 [[154_database_index_b_tree_search_optimization|인덱스]]를 매핑해 두고 필요한 노드만 건드린다. 결국 [[131_mmap_ipc|메모리 맵 파일]]은 "[[501_file_definition_logical_record|파일]]을 메모리로 바꾼다"기보다, **[[501_file_definition_logical_record|파일]]을 [[286_page_frame|페이지]] 단위 주소 공간 [[164_policy|정책]] 안으로 편입시킨다**고 보는 편이 더 정확하다.

- **📢 섹션 요약 비유**: `read()`가 필요한 재료를 주문할 때마다 소포로 받아 보는 방식이라면, [[131_mmap_ipc|메모리 맵 파일]]은 마트 진열대를 우리 주방 통로와 직접 연결해 놓는 방식이다. 대신 누가 먼저 집어 가고 언제 재고를 채울지까지 같이 신경 써야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[131_mmap_ipc|메모리 맵 파일]]은 세 가지 상황에서 특히 강하다. 첫째, 수 GB~수 TB 규모 [[501_file_definition_logical_record|파일]]에서 일부 구간만 자주 탐색하는 무작위 읽기 워크로드다. 둘째, 여러 프로세스가 같은 정적 [[001_dikw_pyramid|데이터]] 집합을 공유해야 하는 경우다. 셋째, 실행 [[501_file_definition_logical_record|파일]]·라이브러리처럼 "필요한 부분만 늦게 적재"하는 편이 시작 시간과 메모리 사용량 모두에 유리한 경우다.

반대로 다음 조건에서는 신중해야 한다. [[015_지연_데이터_관점|지연]]시간이 절대적으로 예측 가능해야 하는 실시간 시스템이라면 [[387_page_fault|페이지 부재]] 한 번도 치명적일 수 있다. [[501_file_definition_logical_record|파일]]이 매우 작고 접근이 짧게 끝난다면 매핑 생성과 해제가 오히려 부담이다. 또한 여러 스레드나 프로세스가 같은 공유 매핑을 수정하면 락, 메모리 가시성, flush 시점 문제까지 동시에 관리해야 하므로 "빠른 I/O"가 순식간에 "복잡한 [[014_concurrency|동시성]] 문제"로 바뀔 수 있다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. **접근 패턴이 무작위적인가, 순차적인가?**  
   무작위 탐색이 많을수록 [[131_mmap_ipc|메모리 맵 파일]]의 주소 기반 접근 이점이 커진다.
2. **[[387_page_fault|페이지 부재]] [[015_지연_데이터_관점|지연]]을 허용할 수 있는가?**  
   초저지연 시스템이면 사전 적재, `mlock`, 일반 I/O, 전용 캐시 [[268_strategy_pattern|전략]]을 함께 검토해야 한다.
3. **여러 프로세스가 공유 수정하는가?**  
   그렇다면 락, [[193_atomicity_all_or_nothing|원자성]], flush [[164_policy|정책]], 장애 시 [[001_dikw_pyramid|데이터]] 일관성을 먼저 설계해야 한다.
4. **[[501_file_definition_logical_record|파일]] 크기가 [[382_virtual_address_space|가상 주소 공간]]에 비해 충분히 큰가?**  
   64비트 환경에서는 유리하지만, 주소 공간 압박이 있는 환경에서는 매핑 단위를 쪼개야 한다.

### 대표 적용 사례

- **실행 [[501_file_definition_logical_record|파일]] 로딩**: 코드 [[286_page_frame|페이지]]와 공유 라이브러리를 필요 시점에만 적재해 시작 비용을 낮춘다.
- **[[002_database_definition|데이터베이스]] [[154_database_index_b_tree_search_optimization|인덱스]]**: B+트리 (B+ Tree)나 [[377_lsm_tree_storage_engine|LSM-tree]] (Log-Structured Merge Tree) [[154_database_index_b_tree_search_optimization|인덱스]] 탐색에서 임의 접근 비용을 줄인다.
- **대형 [[568_logs_distributed_logging_elk_fluentd|로그]]/[[118_image_analysis|이미지 분석]]**: 전체 [[501_file_definition_logical_record|파일]] 복사 없이 특정 구간만 슬라이싱하듯 접근한다.

### 피해야 할 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 작은 [[501_file_definition_logical_record|파일]]을 대량으로 짧게 읽는 작업에 무조건 `mmap()`을 적용하는 것
- 공유 매핑을 쓰면서도 `msync()`·flush [[164_policy|정책]] 없이 내구성을 가정하는 것
- 메모리 사용량을 RSS (Resident Set Size)만 보고 판단해, 매핑된 [[501_file_definition_logical_record|파일]] [[286_page_frame|페이지]]의 실제 압박을 과소평가하는 것

기술사 답안 관점에서는 "[[131_mmap_ipc|메모리 맵 파일]]은 [[566_mmap_zero_copy_sendfile|Zero-copy]] 지향의 고속 [[501_file_definition_logical_record|파일]] 접근 기법"에서 멈추면 부족하다. 더 정확한 답은 **[[381_virtual_memory|가상 메모리]] 메커니즘을 [[501_file_definition_logical_record|파일]] 접근에 재사용하는 구조이며, [[282_performance_tactics|성능]] 이득은 접근 패턴과 [[387_page_fault|페이지 부재]] 관리가 받쳐 줄 때만 현실화된다**는 것이다.

- **📢 섹션 요약 비유**: [[131_mmap_ipc|메모리 맵 파일]]은 고속도로 직결 진입로와 같다. 맞는 차와 맞는 길에서는 엄청 빠르지만, 골목길 배달 오토바이까지 모두 올리면 오히려 사고와 정체가 늘어난다.

---

## Ⅴ. 기대효과 및 결론

[[131_mmap_ipc|메모리 맵 파일]]을 적절히 사용하면 [[501_file_definition_logical_record|파일]] 접근이 더 단순하고 더 빠르게 느껴진다. 개발자는 버퍼 관리 코드를 줄이고, [[001_operating_system_purpose|운영체제]]는 [[286_page_frame|페이지]] 캐시와 주소 변환 장치를 이용해 필요한 부분만 적재하며, 여러 프로세스는 동일한 [[501_file_definition_logical_record|파일]] 기반 [[001_dikw_pyramid|데이터]]를 중복 복사 없이 공유할 수 있다. 이 덕분에 대용량 정적 [[001_dikw_pyramid|데이터]] 처리, 실행 [[501_file_definition_logical_record|파일]] 로딩, 분석 시스템에서 높은 생산성과 [[282_performance_tactics|성능]]을 동시에 얻는다.

하지만 한계도 분명하다. [[387_page_fault|페이지 부재]]는 결국 저장장치 [[015_지연_데이터_관점|지연]]을 숨겨 두는 방식이므로, 접근 패턴이 나쁘거나 메모리 압박이 크면 체감 [[282_performance_tactics|성능]]이 급격히 흔들린다. 공유 매핑은 빠른 대신 [[212_synchronization_mechanisms|동기화]]와 내구성 책임을 응용 프로그램 쪽으로 더 많이 밀어낸다. 즉 [[131_mmap_ipc|메모리 맵 파일]]은 "복사가 적으니 무조건 빠르다"가 아니라, **[[501_file_definition_logical_record|파일]]을 메모리처럼 다루는 대신 메모리 계층의 위험도 함께 받아들이는 [[268_strategy_pattern|전략]]**이다.

앞으로도 이 기법의 중요성은 유지된다. [[482_nvme|NVMe]] ([[482_nvme|Non-Volatile Memory Express]]) 저장장치, 대용량 [[286_page_frame|페이지]], 사용자 공간 [[501_file_definition_logical_record|파일]] 시스템 최적화가 발전해도, 결국 필요한 것은 "[[501_file_definition_logical_record|파일]] [[001_dikw_pyramid|데이터]]를 언제 어떤 단위로 주소 공간에 편입할 것인가"라는 판단이기 때문이다. 그래서 [[131_mmap_ipc|메모리 맵 파일]]은 [[501_file_definition_logical_record|파일]] 입출력 기법이라기보다, [[001_operating_system_purpose|운영체제]]와 컴퓨터구조가 만나는 접점으로 기억하는 것이 가장 정확하다.

- **📢 섹션 요약 비유**: [[131_mmap_ipc|메모리 맵 파일]]은 창고와 작업대를 이어 주는 컨베이어벨트다. 잘 설계하면 사람이 들고 뛰지 않아도 일이 빨라지지만, 벨트가 막히면 작업대 전체가 함께 멈춘다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[255_demand_paging|요구 페이징]] ([[255_demand_paging|Demand Paging]]) | 매핑만 먼저 설정하고 실제 [[001_dikw_pyramid|데이터]]는 접근 시점에 적재하는 하부 메커니즘 |
| [[286_page_frame|페이지]] 캐시 ([[286_page_frame|Page]] Cache) | `read()`와 `mmap()`이 공통으로 활용하는 [[501_file_definition_logical_record|파일]] [[001_dikw_pyramid|데이터]]의 메모리 실체 |
| [[387_page_fault|페이지 부재]] ([[387_page_fault|Page Fault]]) | 매핑된 주소를 처음 건드릴 때 적재를 유발하는 예외 경계 |
| 복사-[[289_cqrs_db|쓰기]] ([[542_cow_file_system|Copy-on-Write]]) | 사적 매핑에서 원본 [[501_file_definition_logical_record|파일]]을 보존한 채 변경을 격리하는 방식 |
| [[117_ipc|IPC]] (Inter-Process Communication) | 여러 프로세스가 같은 매핑을 공유해 고속 [[001_dikw_pyramid|데이터]] 교환 경로로 활용 |
| [[352_page_size|페이지 크기]] ([[352_page_size|Page Size]]) | 한 번의 적재 단위와 [[341_internal_fragmentation|내부 단편화]], [[357_tlb|TLB]] 커버 범위를 함께 좌우 |

### 📈 관련 키워드 및 발전 흐름도

```text
파일 시스템 버퍼 I/O
    │
    ▼
페이지 캐시 (Page Cache) 공유
    │
    ▼
메모리 맵 파일 (Memory-Mapped File)
    │
    ├─▶ 요구 페이징 (Demand Paging)
    │
    ├─▶ 공유 매핑 · IPC (Inter-Process Communication)
    │
    ▼
복사-쓰기 (Copy-on-Write) · 실행 파일 지연 로딩
    │
    ▼
대용량 데이터베이스 · 분석 엔진 · 고성능 파일 접근
```

이 흐름은 단순 버퍼 기반 [[501_file_definition_logical_record|파일]] 읽기에서 출발해, [[001_operating_system_purpose|운영체제]]가 [[501_file_definition_logical_record|파일]] [[001_dikw_pyramid|데이터]]를 [[286_page_frame|페이지]] 단위 주소 공간 [[164_policy|정책]]으로 통합하면서 고성능 공유와 [[015_지연_데이터_관점|지연]] 적재로 확장되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[131_mmap_ipc|메모리 맵 파일]]은 책 내용을 공책에 베껴 적는 대신, 책장을 책상에 바로 붙여 두는 방법이에요.
2. 그래서 보고 싶은 곳을 손가락으로 바로 짚을 수 있지만, 아직 안 펼친 [[286_page_frame|페이지]]는 그때 가서 열어 봐야 해요.
3. 여러 친구가 같은 책장을 같이 붙여 두면 같은 내용을 빨리 볼 수 있지만, 누가 낙서했는지는 잘 약속해 둬야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 309 / 803

← **이전**: [[307_page_size|307. 페이지 크기 (Page Size)의 트레이드오프]]
**다음**: [[309_io_controller|309. 입출력 모듈 (I/O Module)]] →

---
