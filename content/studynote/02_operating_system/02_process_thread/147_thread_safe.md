---
title: "147. 스레드 안전 (Thread-safe) 함수 및 라이브러리"
date: "2026-04-19"
tags:
  - "studynote-operating-system"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전([Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)-safe)이란 여러 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)([Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/))가 동시에 같은 함수나 자원을 호출해도 <strong><a href="/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/">경쟁 조건</a>(<a href="/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/">Race Condition</a>) 없이 항상 올바른 결과를 보장</strong>하는 성질이다.
> 2. **가치**: 멀티코어 CPU 환경에서 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 실행이 기본이 된 현재, [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전하지 않은 코드는 재현 불가능한 버그와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손상의 근원이 된다.
> 3. **판단 포인트**: [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전([Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)-safe)과 재진입 가능(Reentrant)은 다르다 — 전자는 뮤텍스([Mutex](/studynote/02_operating_system/04_synchronization/223_mutex/)) 등 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 장치로 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)하는 것이고, 후자는 아예 공유 상태 없이 설계하는 것이다.

---

## Ⅰ. 개요 및 필요성

[스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전은 함수 또는 자료구조가 <strong>여러 <a href="/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a>에서 동시에 호출되어도 의도한 동작을 유지</strong>하는 속성이다. 단일 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 환경에서는 순서가 보장되지만, 멀티스레드 환경에서는 CPU 스케줄러가 어느 시점에나 [문맥 교환](/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)([Context Switch](/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/))을 일으킬 수 있어, 공유 자원 접근 순서가 뒤섞이면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 무결성이 무너진다.

대표적인 위험 사례: C 표준 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)의 `strtok()`는 내부 정적 버퍼(static buffer)를 사용하므로, 두 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 동시에 호출하면 버퍼를 덮어써 잘못된 토큰을 반환한다. POSIX는 이를 해결한 `strtok_r()`(r = reentrant)을 제공한다.

<strong><a href="/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a> 안전이 필요한 상황</strong>:
- 멀티스레드 웹 서버에서 요청당 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 할당
- [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 파서에서 공유 파싱 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 사용
- 멀티스레드 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 처리([Signal](/studynote/02_operating_system/02_process_thread/130_signal/) Handler)에서 OS 콜 호출

- **📢 섹션 요약 비유**: [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전은 **'도서관 열람실 규칙'** 과 같습니다. 한 책(공유 자원)을 여러 사람이 동시에 읽으려 할 때, 먼저 대출 카드(잠금)를 끊어야만 빌릴 수 있게 만들어, 두 사람이 동시에 같은 책을 가져가 내용이 엉키는 사고를 막는 도서관 규칙입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전 달성 방법 4가지

```text
스레드 안전 달성 전략
+------------------------------------------------------------------+
|                                                                  |
|  ① 뮤텍스(Mutex) / 락(Lock) 사용                                  |
|     공유 자원 접근 전 락 획득 -> 임계 구역(Critical Section) 보호    |
|     장점: 범용적   단점: 데드락(Deadlock), 성능 저하               |
|                                                                  |
|  ② 원자적 연산 (Atomic Operation)                                 |
|     CAS(Compare-And-Swap), fetch_add 등 CPU 명령어 수준 원자성    |
|     장점: 락 없이 안전   단점: 복잡한 연산에는 부적합               |
|                                                                  |
|  ③ 스레드 지역 저장소 (TLS, Thread-Local Storage)                  |
|     스레드별 독립 복사본 -> 공유 자체를 없앰                         |
|     장점: 잠금 불필요   단점: 메모리 증가                           |
|                                                                  |
|  ④ 불변 데이터 (Immutable Data)                                    |
|     초기화 후 읽기 전용 -> 경쟁 조건 원천 차단                       |
|     장점: 가장 안전   단점: 상태 변경 불가                          |
+------------------------------------------------------------------+
```

### 2. [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전 vs. 재진입 가능 비교

| 구분 | [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전 ([Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)-safe) | 재진입 가능 (Reentrant) |
|:---|:---|:---|
| 정의 | [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 장치로 공유 자원 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) | 공유 상태 자체가 없음 |
| [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 필요 여부 | 필요 ([Mutex](/studynote/02_operating_system/04_synchronization/223_mutex/), Atomic 등) | 불필요 |
| 정적 변수 사용 | 가능 ([보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 시) | 금지 |
| 시그널 핸들러 사용 | 불가 (락 재진입 위험) | 가능 |
| 예시 | `malloc()` (내부 잠금), `printf()` | `strlen()`, `memcpy()` |

재진입 가능 함수는 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전의 부분집합이다 — 재진입 가능하면 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전하지만, 역은 성립하지 않는다.

### 3. C 표준 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/): 안전 vs. 비안전

| 비안전 함수 | 대체 안전 함수 | 문제 원인 |
|:---|:---|:---|
| `strtok()` | `strtok_r()` | 내부 정적 버퍼 |
| `localtime()` | `localtime_r()` | 내부 정적 tm 구조체 |
| `asctime()` | `asctime_r()` | 내부 정적 문자열 버퍼 |
| `rand()` | `rand_r()` | 전역 시드(seed) 상태 |
| `errno` (전역) | `errno` ([TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 구현) | POSIX에서 TLS로 해결 |

- **📢 섹션 요약 비유**: [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전과 재진입 가능의 차이는 **'공중화장실 vs. 1인 전용 화장실'** 입니다. 공중화장실([스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전)은 잠금장치([Mutex](/studynote/02_operating_system/04_synchronization/223_mutex/))가 있어 한 명씩 순서대로 쓸 수 있고, 1인 전용 화장실(재진입 가능)은 처음부터 혼자만 쓰게 설계되어 잠금 자체가 필요 없습니다.

---

## Ⅲ. 비교 및 연결

### [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 메커니즘 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비교

| 메커니즘 | 오버헤드 | 데드락 위험 | 적합 상황 |
|:---|:---|:---|:---|
| [Mutex](/studynote/02_operating_system/04_synchronization/223_mutex/) (뮤텍스) | 중간 | 있음 | 복잡한 [임계 구역](/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/) |
| [Spinlock](/studynote/02_operating_system/04_synchronization/222_spinlock/) ([스핀락](/studynote/02_operating_system/04_synchronization/222_spinlock/)) | 낮음 (짧은 구간) | 낮음 | 짧은 [임계 구역](/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/) + 멀티코어 |
| RW [Lock](/studynote/05_database/04_transactions_concurrency/510_lock/) ([읽기-쓰기 락](/studynote/02_operating_system/04_synchronization/280_read_write_lock/)) | 읽기 낮음 | 있음 | 읽기 다, [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 소 |
| Atomic Operations | 최저 | 없음 | [카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/), [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) 등 단순 연산 |
| 불변 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 없음 | 없음 | [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 객체, 상수 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |

### 연결 개념 흐름

[경쟁 조건](/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/)([Race Condition](/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/)) -> [임계 구역](/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/)([Critical Section](/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/)) [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) -> [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 메커니즘 선택 -> [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전 확보 -> 데드락([Deadlock](/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)) 방지 -> [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화(Atomic, [Lock-free](/studynote/02_operating_system/04_synchronization/256_lock_free_data_structures/))

- **📢 섹션 요약 비유**: [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 메커니즘 선택은 **'교통 통제 방식 선택'** 과 같습니다. [신호](/studynote/02_operating_system/02_process_thread/130_signal/)등([Mutex](/studynote/02_operating_system/04_synchronization/223_mutex/))은 범용적이지만 대기 시간이 있고, 로터리([Spinlock](/studynote/02_operating_system/04_synchronization/222_spinlock/))는 짧게 돌다가 빠져나가기 좋으며, 고속도로 전용차로(RW [Lock](/studynote/05_database/04_transactions_concurrency/510_lock/))는 승객(읽기)은 많고 화물차([쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))는 드물 때 최적입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 의사결정 기준

- <strong>락(<a href="/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a>) 채택</strong>: 복잡한 상태를 여러 단계에 걸쳐 수정해야 할 때
- **Atomic 채택**: 단순 [카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) 증가/감소, [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) 토글 등 한 번의 연산으로 처리 가능할 때
- <strong><a href="/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/">TLS</a> 채택</strong>: [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)별 독립적 상태가 필요하고 공유할 필요가 없을 때
- <strong>불변 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 채택</strong>: 초기화 이후 읽기만 하는 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 상수 객체

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

<strong><a href="/studynote/02_operating_system/04_synchronization/272_double_checked_locking/">double-checked locking</a> 미완성 구현</strong>: 싱글턴 패턴에서 락 없이 인스턴스를 먼저 확인하고, null이면 락을 잡는 패턴은 CPU [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 재정렬(Reordering)로 인해 C++[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/) 이전 표준에서는 안전하지 않다. C++[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/) 이후 `std::call_once` 또는 `memory_order_acquire/release`를 사용해야 한다.

<strong><a href="/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/">인터럽트</a>/시그널 핸들러에서 <a href="/studynote/02_operating_system/04_synchronization/223_mutex/">Mutex</a> 사용</strong>: 시그널 핸들러는 언제든지 메인 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 실행을 중단하고 진입한다. 핸들러 내에서 이미 락을 획득 중인 Mutex를 다시 잠그려 하면 <strong>데드락</strong>이 발생한다. 핸들러에서는 반드시 재진입 가능(async-[signal](/studynote/02_operating_system/02_process_thread/130_signal/)-safe) 함수만 호출해야 한다.

- **📢 섹션 요약 비유**: [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 핸들러에서 Mutex를 쓰는 것은 **'화재 대피 중에 화장실 문을 잠근 채 안에 있는 것'** 과 같습니다. 비상 탈출(시그널)은 언제나 즉시 이루어져야 하는데, 잠금([Mutex](/studynote/02_operating_system/04_synchronization/223_mutex/))이 걸려 있으면 출구가 막혀 버립니다.

---

## Ⅴ. 기대효과 및 결론

[스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전 설계는 멀티코어 CPU가 일반화된 현재 소프트웨어 품질의 기초다. [경쟁 조건](/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/)([Race Condition](/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/))은 재현이 어렵고, 디버깅에 수십 시간이 소요되는 최악의 버그 유형 중 하나다. 따라서 설계 단계에서 **어느 자료구조가 공유되는지**, <strong>어느 코드 경로가 <a href="/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/">임계 구역</a>인지</strong>를 명시적으로 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하는 것이 핵심이다.

**한계**: 과도한 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)는 오히려 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목([Lock Contention](/studynote/02_operating_system/04_synchronization/275_lock_contention_monitoring/))과 데드락을 유발한다. 락 없는([Lock-free](/studynote/02_operating_system/04_synchronization/256_lock_free_data_structures/)) 알고리즘이나 메시지 패싱([Message Passing](/studynote/02_operating_system/02_process_thread/119_message_passing/)) 방식(Go 채널, [Erlang](/studynote/03_network/20_performance_evaluation_advanced/1004_erlang_traffic_load_unit_calculation/) 액터 등)은 공유 상태 자체를 줄이는 근본적 대안이다.

**미래 방향**: ① Rust의 소유권(Ownership) 시스템 — 컴파일 타임에 [경쟁 조건](/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/) 원천 차단, ② [트랜잭셔널 메모리](/studynote/01_computer_architecture/15_advanced_topics/513_htm/)(Transactional Memory, TM), ③ 함수형 프로그래밍의 불변 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 철학 확산.

[스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전은 "잠금을 거는 것"이 아니라 "공유를 최소화하는 설계"를 먼저 추구해야 한다는 점을 기억해야 한다.

- **📢 섹션 요약 비유**: [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전의 핵심은 **'공용 우물을 쓰는 마을'** 과 같습니다. 잠금([Mutex](/studynote/02_operating_system/04_synchronization/223_mutex/))은 줄을 세우는 것이고, TLS는 집마다 개인 우물을 파는 것이며, 불변 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 물병을 미리 채워 각자 들고 다니게 하는 것입니다. 가장 좋은 방법은 처음부터 공유를 줄이는 설계입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/">경쟁 조건</a> (<a href="/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/">Race Condition</a>)</strong> | [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전 부재로 발생하는 비결정적 버그의 근원 |
| <strong>뮤텍스 (<a href="/studynote/02_operating_system/04_synchronization/223_mutex/">Mutex</a>)</strong> | [임계 구역](/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/)을 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)하는 가장 기본적인 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 장치 |
| <strong>데드락 (<a href="/studynote/02_operating_system/05_deadlock/281_deadlock_definition/">Deadlock</a>)</strong> | 잘못된 락 순서로 발생하는 영구 블로킹 상태 |
| <strong><a href="/studynote/02_operating_system/11_exam_summary/768_cas_compare_and_swap_lock_free/">CAS</a> (<a href="/studynote/01_computer_architecture/11_multicore_synchronization/415_compare_and_swap/">Compare-And-Swap</a>)</strong> | 락 없이 원자적 연산을 제공하는 CPU [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) |
| **재진입 가능 (Reentrant)** | 공유 상태 없이 설계된 함수; [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전의 강한 형태 |
| <strong><a href="/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/">TLS</a> (<a href="/studynote/02_operating_system/02_process_thread/092_thread_lwp/">Thread</a>-Local Storage)</strong> | [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)별 독립 저장소로 공유 자체를 제거하는 기법 |

### 📈 관련 키워드 및 발전 흐름도

```text
단일 스레드 프로그래밍 (공유 상태 무관)
    |
    v
멀티스레드 등장 -> 경쟁 조건(Race Condition) 문제
    |
    v
뮤텍스(Mutex) / 세마포어(Semaphore) — 임계 구역 보호
    |
    +-► 재진입 가능 함수 (Reentrant) — 공유 상태 제거
    |
    +-► Atomic Operations — 락 없는 원자 연산
    |
    +-► Lock-free / Wait-free 알고리즘
              |
              v
        Rust 소유권 시스템 / 트랜잭셔널 메모리 (TM)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 여러 친구가 동시에 하나의 그림 도구(공유 자원)를 쓰면 그림이 엉켜요. <strong><a href="/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a> 안전</strong>은 번호표를 뽑아 한 명씩 순서대로 쓰게 만드는 규칙이에요!
2. 더 좋은 방법은 각자 자기 색연필 세트([TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/))를 가지게 해서, 아예 같은 도구를 나눠 쓸 필요가 없게 하는 거예요.
3. **재진입 가능** 함수는 처음부터 '혼자만 쓸 수 있는 개인 도구함'처럼 설계되어서, 잠금도 필요 없고 언제 끼어들어도 문제가 안 생기는 완벽한 방법이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 147 / 800

<- **이전**: [146. 실시간 프로세스 (Real-time Process)](/studynote/02_operating_system/02_process_thread/146_realtime_process/)
**다음**: [148. 재진입 가능 코드 (Reentrant Code / Pure Code)](/studynote/02_operating_system/02_process_thread/148_reentrant_code/) ->

---
