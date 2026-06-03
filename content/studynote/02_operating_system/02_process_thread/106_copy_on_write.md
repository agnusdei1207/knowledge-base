---
title: 106. Copy-on-Write (COW) - fork() 최적화 기법
date: '2026-03-22'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[542_cow_file_system|Copy-on-Write]] ([[542_cow_file_system|COW]])는 `fork()` 시스템 콜 시 자식 프로세스에게 부모의 물리 메모리를 즉시 복사하지 않고 [[353_page_table|페이지 테이블]]만 매핑한 뒤, 실제 [[289_cqrs_db|쓰기]] (Write) 작업이 발생할 때만 해당 [[286_page_frame|페이지]]를 독립적으로 복사하는 [[015_지연_데이터_관점|지연]] 할당 기법이다.
> 2. **가치**: 대용량 프로세스를 [[016_replication_factor|복제]]할 때 발생하는 엄청난 메모리 복사 [[015_지연_데이터_관점|지연]] 시간과 메모리 공간 낭비를 획기적으로 제거하며, 특히 [[087_process_state_transition|생성]] 직후 다른 프로그램으로 덮어씌워지는 `exec()` 패턴에서 불필요한 복사 비용을 제로에 가깝게 만든다.
> 3. **판단 포인트**: [[289_cqrs_db|쓰기]] 작업이 드문 [[016_replication_factor|복제]] 작업이나 [[022_snapshot_backup_architecture|스냅샷]] [[087_process_state_transition|생성]]에 최적의 [[282_performance_tactics|성능]]을 보이지만, [[289_cqrs_db|쓰기]]가 매우 빈번하게 일어나는 시스템에서는 매번 [[720_page_fault_isr|페이지 폴트]] ([[387_page_fault|Page Fault]]) 오버헤드가 발생하여 오히려 [[282_performance_tactics|성능]]을 저하시킬 수 있으므로 워크로드 특성 분석이 필수적이다.

---

## Ⅰ. 개요 및 필요성

[[001_operating_system_purpose|운영체제]] (OS, [[001_operating_system_purpose|Operating System]])에서 새로운 프로세스를 [[087_process_state_transition|생성]]하는 `fork()` 시스템 콜은 전통적으로 부모 프로세스의 전체 주소 공간(코드, [[001_dikw_pyramid|데이터]], 힙, [[057_stack|스택]])을 자식 프로세스에게 그대로 물리적으로 복사해 주었다. 그러나 부모 프로세스가 기가바이트(GB) 단위의 메모리를 사용 중이라면 복사에 수 초의 [[015_지연_데이터_관점|지연]]이 발생하고 물리 메모리 공간이 절반으로 줄어드는 심각한 병목이 일어난다.

더 큰 문제는 유닉스 계열 프로세스 [[087_process_state_transition|생성]]의 전형적인 패턴이 `fork()` 직후 `exec()` 시스템 콜을 호출하여 자식 프로세스를 전혀 새로운 프로그램으로 덮어씌운다는 점이다. 애써 긴 시간 복사해 둔 [[001_dikw_pyramid|데이터]]가 단 1밀리초 만에 폐기되는 막대한 낭비가 발생한다. 이를 막기 위해 "당장 복사하지 말고 원본을 같이 읽다가, 누군가 내용을 고치려 할 때만 복사하자"는 경제적인 최적화 아이디어인 [[542_cow_file_system|Copy-on-Write]] ([[542_cow_file_system|COW]])가 필연적으로 등장하게 되었다.

- **📢 섹션 요약 비유**: 형과 동생이 백과사전을 같이 보게 하다가, 동생이 특정 [[286_page_frame|페이지]]에 형광펜([[289_cqrs_db|쓰기]])을 칠하려고 할 때만 그 한 장을 따로 복사기로 찍어주는 효율적인 공부법과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COW는 [[001_operating_system_purpose|운영체제]] [[022_kernel_role|커널]]과 메모리 관리 장치 ([[328_mmu|MMU]], [[284_mmu|Memory Management Unit]])의 정교한 협업 메커니즘을 통해 구현된다. 핵심은 [[353_page_table|페이지 테이블]]의 권한 [[073_bit|비트]] 조작과 예외 처리 (Exception Handling) 분기다.

| 단계 | 구성 요소 | 동작 원리 |
|:---|:---|:---|
| **1. fork() 호출** | [[022_kernel_role|커널]] ([[022_kernel_role|Kernel]]) | 부모의 [[353_page_table|페이지 테이블]]을 복사하되, 물리 메모리는 복사하지 않음. 모든 [[286_page_frame|페이지]] 엔트리를 읽기 전용 (Read-Only)으로 설정함. |
| **2. [[289_cqrs_db|쓰기]] 시도 감지** | [[328_mmu|MMU]] | 자식(또는 부모)이 공유 중인 읽기 전용 [[286_page_frame|페이지]]에 [[289_cqrs_db|쓰기]](Write)를 시도하면 접근 위반 예외인 [[720_page_fault_isr|페이지 폴트]] ([[387_page_fault|Page Fault]])를 발생시킴. |
| **3. 물리 [[397_frame_allocation|프레임 할당]]** | 폴트 핸들러 | 예외를 가로챈 [[022_kernel_role|커널]]이 [[542_cow_file_system|COW]] 상황임을 인지하고, 새로운 빈 물리 [[286_page_frame|페이지]] 프레임을 하나 할당함. |
| **4. 복사 및 권한 갱신**| 폴트 핸들러 | 기존 내용을 새 프레임에 복사하고, 프로세스의 [[353_page_table|페이지 테이블]]을 새 프레임으로 연결한 뒤 [[289_cqrs_db|쓰기]] 권한 (Read-Write)을 부여함. |

```text
┌──────────────────────────────────────────────────────────────┐
│             Copy-on-Write (COW) 메커니즘 흐름도                │
├──────────────────────────────────────────────────────────────┤
│ [1. fork() 직후 - 자원 공유]                                     │
│ 부모 프로세스 (PTE: Read-Only) ────┐                            │
│                                  ▼                            │
│                             [물리 메모리 페이지 A]                │
│                                  ▲                            │
│ 자식 프로세스 (PTE: Read-Only) ────┘                            │
│                                                              │
│ [2. 자식 프로세스가 쓰기(Write) 시도]                            │
│ 자식 ──(쓰기 명령)──▶ MMU가 읽기 전용 위반 감지 ──▶ Page Fault 발생 │
│                                                              │
│ [3. 커널의 개입 및 페이지 개별 복사]                             │
│ 부모 프로세스 (PTE: Read-Only) ────▶ [물리 메모리 페이지 A]      │
│                                                              │
│ 자식 프로세스 (PTE: Read-Write) ───▶ [새로운 물리 페이지 A']     │
│ (새로 할당 후 A 내용 복사, 쓰기 권한 부여로 정상 쓰기 완료)           │
└──────────────────────────────────────────────────────────────┘
```

이 그림이 보여주듯 COW의 마법은 [[720_page_fault_isr|페이지 폴트]]라는 '오류'를 적극적인 '[[507_acid_properties|트리거]]'로 활용한다는 점이다. MMU가 [[289_cqrs_db|쓰기]] 시도를 감시하고 있다가 걸러내면 [[022_kernel_role|커널]]이 비로소 단 1개의 [[286_page_frame|페이지]](일반적으로 4KB)만 복사하는 [[023_lazy_evaluation|지연 평가]] ([[023_lazy_evaluation|Lazy Evaluation]])를 수행한다.

- **📢 섹션 요약 비유**: 한 권의 은행 장부를 두 직원이 공유하다가, 한 직원이 잔액을 수정하려 할 때만 은행장([[328_mmu|MMU]])이 경고를 울리고 새 장부 한 장을 복사해 주는 철저한 자원 절약 시스템입니다.

---

## Ⅲ. 비교 및 연결

전통적인 깊은 복사 (Deep Copy) 모델과 [[542_cow_file_system|COW]] 모델은 [[282_performance_tactics|성능]] 트레이드오프에서 명확한 차이를 드러낸다.

| 비교 항목 | 깊은 복사 (전통적 fork) | [[015_지연_데이터_관점|지연]] 복사 ([[542_cow_file_system|COW]] 기반 fork) |
|:---|:---|:---|
| **[[459_quic_fec_forward_error_correction|초기]] [[087_process_state_transition|생성]] 속도** | 물리적 [[001_dikw_pyramid|데이터]] 크기에 비례 (매우 느림) | [[353_page_table|페이지 테이블]] 복사만 수행 (매우 빠름) |
| **[[459_quic_fec_forward_error_correction|초기]] 메모리 사용량**| 정확히 2배 소모 | 공유하므로 추가 소모 거의 0바이트 |
| **[[289_cqrs_db|쓰기]] 시 오버헤드** | 이미 복사되어 있어 오버헤드 없음 | [[289_cqrs_db|쓰기]] 발생 시마다 [[720_page_fault_isr|페이지 폴트]] [[015_지연_데이터_관점|지연]](Micro-sec) 발생 |

[[001_operating_system_purpose|운영체제]]의 [[381_virtual_memory|가상 메모리]] 철학 측면에서 COW는 동일 [[286_page_frame|페이지]] 병합 (KSM, [[022_kernel_role|Kernel]] Same-[[286_page_frame|page]] Merging) 기법과 직접적으로 연결된다. COW가 같은 부모에서 나온 동일한 [[286_page_frame|페이지]]를 나눌 때 복사를 [[015_지연_데이터_관점|지연]]한다면, KSM은 서로 다른 프로그램이 우연히 똑같은 내용의 [[286_page_frame|페이지]]를 가질 때 이를 하나로 합치고 [[542_cow_file_system|COW]] 플래그를 달아 메모리를 극단적으로 쥐어짜는 진화형 기법이다. 이는 가상 머신([[598_vm_migration_nic|VM]], [[598_vm_migration_nic|Virtual Machine]]) 환경에서 획기적인 역할을 한다.

- **📢 섹션 요약 비유**: 처음부터 돈을 주고 집을 두 채 짓는 것(깊은 복사)과 룸메이트로 살다가 싸울 때만 방을 하나 더 구하는 것([[542_cow_file_system|COW]])의 차이이며, 나중에는 아예 성격 맞는 남남끼리 합숙시키는 것(KSM)으로 진화했습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 개발자와 인프라 엔지니어는 COW의 이면을 반드시 인지하고 장애를 피해야 한다.

### 실무 시나리오 및 판단 기준
1. **[[542_redis|Redis]] RDB [[022_snapshot_backup_architecture|스냅샷]] [[555_backup_and_restore_strategy|백업]]**: 인메모리 DB인 [[297_snowflake_schema|레디스]]는 [[001_dikw_pyramid|데이터]]를 디스크에 저장하기 위해 `BGSAVE` 명령어를 내리며 백그라운드 프로세스를 `fork()` 한다. 이때 [[542_cow_file_system|COW]] 덕분에 수십 GB의 [[297_snowflake_schema|레디스]] 메모리가 순간적으로 복사되지 않고 순식간에 [[555_backup_and_restore_strategy|백업]] 프로세스가 [[087_process_state_transition|생성]]된다. 
2. **메모리 부족 ([[157_oom_killer|OOM]]) [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 판단**: 만약 [[297_snowflake_schema|레디스]] [[022_snapshot_backup_architecture|스냅샷]]을 뜨는 중에 원본 DB에 [[289_cqrs_db|쓰기]] 트래픽이 폭주한다면, [[289_cqrs_db|쓰기]]가 일어난 [[286_page_frame|페이지]]들이 계속 새롭게 복사([[542_cow_file_system|COW]])되면서 시스템의 물리 메모리 가용량을 급격히 갉아먹게 된다. 최악의 경우 [[157_oom_killer|OOM]] ([[157_oom_killer|Out Of Memory]]) 킬러가 발동해 DB 자체가 죽어버리므로, 여유 메모리를 충분히 확보해야 한다.
3. **[[561_container_based_deployment|컨테이너]] 환경**: Docker의 [[501_file_definition_logical_record|파일]] 시스템(OverlayFS 등)도 COW를 채택했다. 베이스 이미지는 공유하고 변경된 [[501_file_definition_logical_record|파일]]만 상위 레이어로 끌어올려 저장하는 방식으로 공간을 최적화한다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 프로세스를 `fork()` 한 후, 자식 프로세스가 전역 배열을 처음부터 끝까지 순차적으로 덮어쓰는 대규모 [[430_index_fast_full_scan|병렬]] 처리 로직을 구현하는 행위 (수백만 번의 [[720_page_fault_isr|페이지 폴트]]가 발생해 엄청난 [[282_performance_tactics|성능]] 하락과 무의미한 오버헤드를 야기함).

- **📢 섹션 요약 비유**: 도화지에 그림을 그릴 때 필요한 부분만 복사해서 쓰면 이득이지만, 결국 온 도화지를 모두 색칠해야 하는 상황이라면 매번 복사기를 돌리러 가는 시간([[720_page_fault_isr|페이지 폴트]]) 때문에 처음부터 새 도화지를 사는 것보다 훨씬 손해를 보는 구조적 한계와 같습니다.

---

## Ⅴ. 기대효과 및 결론

Copy-on-Write는 "필요해질 때까지 일하지 않는다"는 컴퓨터 과학의 [[015_지연_데이터_관점|지연]] 할당 최적화 철학의 정점을 보여주는 기술이다. `fork()`의 무거운 코스트를 O(1)에 가깝게 줄여주어 유닉스 환경의 경쾌한 다중 프로세싱을 가능하게 만들었으며, 현대의 클라우드 환경에서는 [[561_container_based_deployment|컨테이너]]의 눈부신 부팅 속도와 자원 절약의 근간으로 활약하고 있다.

단, "[[289_cqrs_db|쓰기]]가 빈번할 경우 [[720_page_fault_isr|페이지 폴트]] 빚이 폭발한다"는 전제조건을 늘 염두에 두어야 한다. 향후에는 메모리뿐만 아니라 ZFS, Btrfs 같은 차세대 [[501_file_definition_logical_record|파일]] 시스템과 [[015_virtualization|가상화]] 스토리지 계층에서도 [[542_cow_file_system|COW]] 철학이 적용되어, [[001_dikw_pyramid|데이터]] 중복을 없애고 시스템 밀도를 높이는 가장 중요한 기술적 지렛대로 자리 잡을 것이다.

- **📢 섹션 요약 비유**: 게으름이 빚어낸 천재적인 발명품입니다. 당장 하지 않아도 될 일을 최대한 뒤로 미룸으로써, 결과적으로 자원 소모를 최소화하는 마법 같은 효율을 이끌어낸 최고의 경제학자입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **fork() 및 exec()** | COW의 직접적인 혜택을 받는 시스템 콜 쌍. fork의 복사 비용을 줄이고 exec 시 낭비를 완벽히 차단함 |
| **[[387_page_fault|Page Fault]] ([[720_page_fault_isr|페이지 폴트]])** | MMU가 하드웨어적으로 [[289_cqrs_db|쓰기]] 위반을 감지해 [[022_kernel_role|커널]]이 개별 복사를 수행하도록 호출하는 작동 [[507_acid_properties|트리거]] |
| **KSM ([[022_kernel_role|Kernel]] Same-[[286_page_frame|page]] Merging)** | 동일한 내용을 가진 메모리 [[286_page_frame|페이지]]를 찾아내 COW로 강제 병합하여 자원을 절약하는 리눅스 기술 |
| **OverlayFS** | 메모리가 아닌 [[501_file_definition_logical_record|파일]] 시스템 (디스크) 계층에 [[542_cow_file_system|COW]] 철학을 적용하여 [[063_docker_architecture|도커]] 이미지를 가볍게 만드는 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
Deep Copy (물리적 전체 복사, 높은 지연)
    │
    ▼
Copy-on-Write (메모리 지연 복사, fork() 속도 최적화)
    │
    ▼
KSM (Kernel Same-page Merging, 가상화 메모리 중복 제거 병합)
    │
    ▼
OverlayFS / ZFS (파일 시스템 계층으로 COW 철학 확장 및 스냅샷 최적화)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 찰흙 놀이를 할 때, 동생이 "나도 찰흙 줘"라고 하면 처음부터 찰흙을 통째로 떼어주지 않고 그냥 같이 보고만 있어요.
2. 동생이 실제로 찰흙에 손가락으로 자국을 내려고 하는 그 순간에만, 딱 그 부분의 찰흙만 복사해서 동생 손에 쥐여주는 똑똑한 방법이에요.
3. 만약 동생이 찰흙을 만지지 않고 바로 밖으로 놀러 나가면 찰흙을 전혀 안 써도 되니까 재료를 아낄 수 있답니다!
