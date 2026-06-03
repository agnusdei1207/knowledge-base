---
title: 393. 쓰기 시 복사 (COW, Copy-on-Write) - fork() 시 자원 공유하다 쓸 때 페이지 복제
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[289_cqrs_db|쓰기]] 시 복사([[542_cow_file_system|COW]]: [[542_cow_file_system|Copy-on-Write]])는 프로세스가 [[016_replication_factor|복제]](`fork()`)되거나 [[001_dikw_pyramid|데이터]]를 복사할 때 1GB의 물리적 메모리를 무식하게 몽땅 복사하지 않고, **일단 부모와 자식이 같은 물리 프레임을 '공유'하게 매핑만 해둔 뒤, 누군가 [[001_dikw_pyramid|데이터]]를 수정(Write)하려고 시도하는 그 찰나의 순간에만 몰래 해당 [[286_page_frame|페이지]]만을 뜯어 복사(Copy)해 주는 초고도화된 OS 속임수([[380_computational_graph_lazy_eager_execution|Lazy]] Optimization)**다.
> 2. **가치**: 자식 프로세스를 낳을 때 발생하는 수 밀리초의 메모리 복사 렉(STW)과 램 용량 고갈([[157_oom_killer|OOM]])을 원천 차단하여, **[[104_process_creation|프로세스 생성]] 속도를 나노초 단위의 $O(1)$로 수직 상승시키며 현대 클라우드/[[561_container_based_deployment|컨테이너]] 스케일링의 근본적 토대를 완성**했다.
> 3. **융합**: [[381_virtual_memory|가상 메모리]]의 **'[[353_page_table|페이지 테이블]] 매핑' 기술**과 하드웨어 MMU의 **'Read-Only 권한 [[073_bit|비트]]([[677_trap_based_system_call_implementation|Trap]])'**가 절묘하게 융합되어, 소프트웨어가 쓰는(Write) 순간 터지는 하드웨어 [[677_trap_based_system_call_implementation|트랩]]([[387_page_fault|Page Fault]])을 가로채어 복사를 수행하는 예술적 아키텍처다.

---

## Ⅰ. 개요 및 필요성

- **개념**: "수정(Write)이 일어나기 전까지는 완벽하게 공유(Share)한다." OS가 메모리를 복사하라는 명령을 받아도 즉시 물리적 복사를 수행하지 않는다. 부모와 자식의 [[353_page_table|페이지 테이블]]이 똑같은 물리 램 프레임을 가리키도록 화살표만 이어준다. 단, 이 프레임에 '읽기 전용(Read-Only)' 락을 걸어둔다. 나중에 자식이 [[001_dikw_pyramid|데이터]]를 수정하려 락을 찌르면 그때서야 "아 찢어질 때가 됐군" 하며 4KB [[286_page_frame|페이지]] 딱 1장만 물리적으로 복사해 준다.
- **필요성**: 리눅스에서 새로운 앱(자식)을 띄우려면 `fork()`라는 함수로 현재 돌아가는 [[105_parent_child_process|부모 프로세스]]를 통째로 [[016_replication_factor|복제]]해야 한다. 만약 카카오톡이 2GB 램을 먹고 있는데 `fork`를 치면, 2GB의 램을 복사(Memcpy)하느라 시스템이 수 초간 얼어붙는다. 더 환장하는 건, 자식은 [[016_replication_factor|복제]]되자마자 99%의 확률로 `exec()` 함수를 실행하여 복사된 2GB를 모조리 쓰레기통에 버리고 새로운 코드를 덮어쓴다는 점이다. **"어차피 0.1초 뒤에 다 버릴 2GB를 왜 피땀 흘려 복사하고 있어야 하는가?"** 이 멍청한 낭비를 끝내기 위해 인류는 '미룰 수 있을 때까지 복사를 미루는' COW라는 철학을 도입했다.

- **등장 배경 및 낭비의 종말**:
  1. **무식한 `fork()`의 재앙**: [[459_quic_fec_forward_error_correction|초기]] UNIX는 `fork()`를 치면 진짜로 프로세스 전체 메모리를 [[074_byte|바이트]] 단위로 복사했다. 무겁고 느려서 프로세스를 함부로 못 만들었다.
  2. **[[381_virtual_memory|가상 메모리]]와 [[353_page_table|페이지 테이블]]의 등장**: 페이징이 도입되자 "어? 물리 메모리는 놔두고 장부의 화살표만 2개 꽂아놓으면 공유가 되네?"라는 사실을 깨달음.
  3. **COW의 완성**: [[289_cqrs_db|쓰기]] 충돌을 막기 위해 하드웨어의 권한 제어([[328_mmu|MMU]] [[677_trap_based_system_call_implementation|Trap]])를 소프트웨어적 예외 처리로 우아하게 받아치는 기법으로 진화.

```text
┌───────────────────────────────────────────────────────────────────────┐
│        COW (Copy-on-Write) 적용 전후의 fork() 동작 시각화             │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│ [ 상황: 1GB짜리 프로세스가 fork()를 호출하여 자식을 낳음 ]            │
│                                                                       │
│ ▶ 1. 과거의 무식한 fork() (COW 없음)                                  │
│  부모 장부 ──▶ [ 물리 램: 부모 데이터 1GB ]                           │
│  자식 장부 ──▶ [ 물리 램: 자식 전용 데이터 1GB 통째로 복사! ]         │
│  💥 결과: 램 용량 2GB로 2배 폭증. 복사하느라 1초 동안 서버 멈춤.      │
│                                                                       │
│ ▶ 2. 현대의 천재적 fork() (COW 적용)                                  │
│  부모 장부 ──┐ ┌▶ [ 물리 램: 1GB 원본 데이터 (Read-Only) ]            │
│  자식 장부 ──┴─┘                                                      │
│  ✅ 결과: 복사 0.001초 컷. 램 용량 1GB 그대로 유지 (100% 절약).       │
│                                                                       │
│ [ 3. 자식이 4KB 페이지 1장만 수정(Write)하려고 할 때! ]               │
│  부모 장부 ──▶ [ 물리 램: 1GB 원본 데이터 ] ◀─ (여전히 공유 중)       │
│  자식 장부 ──▶ [ 딱 1장만 새로 복사된 4KB 물리 프레임 툭! ]           │
│  ✅ 1GB 전체가 아니라, 값이 바뀌는 그 4KB 조각 하나만 몰래 복사함.    │
└───────────────────────────────────────────────────────────────────────┘
```
**[다이어그램 해설]** [[381_virtual_memory|가상 메모리]] 추상화가 부리는 흑마술의 정점이다. 부모와 자식은 각자의 가상 주소 `0x1000` 번지에 자기만의 [[001_dikw_pyramid|데이터]]가 있다고 100% 굳게 믿고 있다. 뒤로는 OS가 똑같은 물리 프레임에 십자수 놓듯 화살표를 묶어둔 줄은 꿈에도 모른다. 이 거짓말은 누군가 변수의 값을 덮어쓰기(수정) 전까지는 영원히 들통나지 않으며, 시스템 자원을 상상 초월로 아껴준다.

- **📢 섹션 요약 비유**: 회사에서 100페이지짜리 결산 보고서를 10명에게 나눠줄 때, 복사기로 1000장을 뽑아 나눠주는(과거) 게 아니라, 구글 문서(Google Docs) 링크 하나만 딱 띄워주고(공유 매핑), 누군가 오타를 수정(Write)하려고 하면 그 사람 전용으로 사본 만들기(Copy)가 자동으로 눌러지는 스마트 오피스의 혁신입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[328_mmu|MMU]] [[677_trap_based_system_call_implementation|트랩]]을 이용한 [[542_cow_file_system|COW]] 3단계 파이프라인

COW는 소프트웨어(OS) 혼자서는 절대 구현할 수 없다. MMU의 권한 제어 [[073_bit|비트]]([[571_protection_vs_security|Protection]] [[086_fenwick_tree|Bit]])가 핵심 [[507_acid_properties|트리거]](방아쇠) 역할을 한다.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│              하드웨어 Page Fault를 악용한(?) COW 매커니즘                │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ 1. [ 함정 설치 ] OS가 fork() 시 부모와 자식의 페이지 테이블을 똑같이     │
│    매핑하고, 해당 페이지들의 권한을 🌟[ Read-Only (읽기 전용) ]으로      │
│    강제로 다 바꿔버림.                                                   │
│                                                                          │
│ 2. [ 함정 발동 ] 자식이 변수 A의 값을 바꾸기 위해 쓰기(Write) 명령 실행. │
│    MMU: "어라? 이 페이지 R/O 인데 네가 쓴다고? 불법이다!"                │
│    -> MMU가 CPU를 멈추고 OS에 [ 💥 Page Fault 트랩 ]을 냅다 던짐.        │
│                                                                          │
│ 3. [ 흑마술 복구 ] 깨어난 OS가 내부 장부(VMA)를 까봄.                    │
│    OS: "아, 이거 원래 쓸 수 있는 건데 내가 COW 하려고 일부러 잠가둔 거네"│
│    -> OS가 빈 물리 프레임 하나를 구해와서 원본 데이터를 4KB 복사해줌.    │
│    -> 자식의 페이지 테이블 화살표를 새 프레임으로 꽂고, 권한을 [ R/W ]로 │
│       열어준 뒤, CPU 보고 다시 명령어 실행하라고 놔줌.                   │
└──────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** [[286_page_frame|Page]] Fault는 원래 "[[001_dikw_pyramid|데이터]]가 램에 없으니 하드디스크에서 가져와라"는 신호다. 하지만 리눅스 커널은 이 하드웨어 에러 신호를 "아! 누군가 [[001_dikw_pyramid|데이터]]를 덮어쓰려 하는구나! 이제 복사본을 찢어줄 때가 됐군"이라는 **알람시계**로 재활용([[323_overloading_vs_overriding|Overloading]])하는 천재성을 발휘했다. 하드웨어의 엄격한 보안 락(Read-Only)을 소프트웨어적 최적화의 징검다리로 써먹은 해커들의 걸작이다.

---

### 레퍼런스 카운트 ([[316_reference_pattern_nosql|Reference]] Count)의 존재

하나의 물리 [[286_page_frame|페이지]]를 부모, 자식, 손자 등 여러 프로세스가 공유하게 되면, "언제 이 물리 램을 100% 삭제(Free)해도 되는가?"가 복잡해진다.
- 리눅스는 물리 [[286_page_frame|페이지]] 프레임마다 장부(`struct page`)에 `_refcount` 라는 변수를 달아둔다.
- `fork()`로 자식이 생겨 프레임을 공유하면 카운트가 `2`가 된다.
- 부모가 COW로 새 [[286_page_frame|페이지]]를 찢어 나가면 원본 [[286_page_frame|페이지]]의 카운트는 `1`로 줄어든다.
- 카운트가 `0`이 되는 순간, 이 램 조각을 아무도 보지 않는다는 뜻이므로 OS는 쿨하게 이 물리 프레임을 [[348_buddy_system|버디 시스템]](Free List)으로 반환해 버린다.

- **📢 섹션 요약 비유**: 박물관의 유리장(Read-Only) 안에 든 희귀한 책을 여러 명이 같이 봅니다. 누군가 책에 낙서하고 싶다고 하면, 관리인이 얼른 복사본 한 장을 쥐여주고 유리장 앞 인원수(레퍼런스 카운트)를 1명 줄입니다. 아무도 책을 안 보게 되어 인원수가 0이 되면 관리인은 불을 끄고 퇴근합니다.

---

## Ⅲ. 비교 및 연결

### 비교 1: 일반 메모리 할당 vs [[542_cow_file_system|Copy-on-Write]]

| 항목 | 일반 복사 (Eager Copy) | [[289_cqrs_db|쓰기]] 시 복사 ([[542_cow_file_system|Copy-on-Write]]) |
|:---|:---|:---|
| **복사 시점** | 명령이 떨어진 **즉시 100% 몽땅** 복사 | [[001_dikw_pyramid|데이터]] 수정(Write)이 발생하는 **미래의 찰나에 4KB씩** 복사 |
| **메모리(RAM) 낭비** | 복사한 만큼 메모리 점유율 2배, 3배 폭증 | 수정하지 않는 90%의 [[001_dikw_pyramid|데이터]]는 영원히 공유되므로 램 낭비 거의 0% |
| **명령 실행 [[015_지연_데이터_관점|지연]]** | `fork()` 호출 시 1초간 서버 멈춤 (최악) | `fork()`는 1밀리초 컷. 나중에 변수 쓸 때만 살짝 렉 터짐 |
| **주 사용처** | 과거의 유닉스, 무식한 [[001_dikw_pyramid|데이터]] [[555_backup_and_restore_strategy|백업]] | 최신 OS의 `fork()`, [[022_snapshot_backup_architecture|스냅샷]], 가상 머신 [[016_replication_factor|복제]], [[542_redis|Redis]] [[555_backup_and_restore_strategy|백업]] |

### [[542_redis|Redis]] ([[297_snowflake_schema|레디스]]) BGSAVE [[022_snapshot_backup_architecture|스냅샷]]의 마술

COW의 파괴력이 가장 잘 드러나는 백엔드 실무 아키텍처다.
- 100GB 메모리를 쓰는 In-memory DB인 Redis가 있다. 새벽 2시에 [[001_dikw_pyramid|데이터]]를 디스크로 [[555_backup_and_restore_strategy|백업]](BGSAVE)해야 한다.
- 만약 Redis가 100GB를 복사해서 [[555_backup_and_restore_strategy|백업]]한다면? 100GB 램이 더 필요해서 램이 터져 죽거나([[157_oom_killer|OOM]]), [[555_backup_and_restore_strategy|백업]]하는 10분 동안 사용자 요청을 1건도 못 받고 멈춰버린다.
- **COW의 구원**: Redis는 단순히 `fork()` 명령 한 줄만 날려 자식 프로세스를 만든다. 100GB 램을 복사하지 않고 0.1초 만에 자식이 생긴다! 자식 프로세스는 조용히 디스크로 100GB [[001_dikw_pyramid|데이터]]를 써 내려간다([[555_backup_and_restore_strategy|백업]]). 
- [[105_parent_child_process|부모 프로세스]](메인 [[542_redis|Redis]])는 유저 요청이 들어와 [[001_dikw_pyramid|데이터]]를 수정(Write)할 때만, 딱 그 4KB 조각들만 램에 하나씩 찢어져 복사([[542_cow_file_system|COW]])된다.
- **결과**: 서버 멈춤 0초. 추가 메모리 소모는 [[555_backup_and_restore_strategy|백업]]하는 동안 변경된 [[001_dikw_pyramid|데이터]] 몇 MB 수준으로 방어. COW가 없었다면 현대의 인메모리 DB 생태계는 애초에 불가능했다.

```text
┌──────────┬────────────┬────────────┬───────────────────────────────┐
│ 백업 방식  │ 램 추가 요구량│ 시스템 멈춤 렉 │ DB 성능 타격         │
├──────────┼────────────┼────────────┼───────────────────────────────┤
│ Lock 백업 │ 0 GB       │ 백업 내내 멈춤  │ ☠️ 최악 (서비스 마비)   │
│ 통짜 복사  │ 원본만큼(100G)│ 복사할 때 멈춤  │ ☠️ OOM으로 서버 사망│
│ COW 백업  │ 수정분만(수MB)│ **없음 (0초)**│ 🚀 평소와 똑같음       │
└──────────┴────────────┴────────────┴───────────────────────────────┘
```
**[매트릭스 해설]** `fork()`와 COW의 조합은 [[002_database_definition|데이터베이스]] [[022_snapshot_backup_architecture|스냅샷]]([[637_zfs_snapshot_cow_architecture|Snapshot]])을 찍을 때 시공간을 얼려버리는 타임머신과 같다. 부모가 [[001_dikw_pyramid|데이터]]를 1억 번 수정하더라도, 자식 프로세스가 가리키는 프레임에는 락이 걸려있어 부모가 건드리지 못하고 튕겨 나가므로([[542_cow_file_system|COW]]), 자식은 '새벽 2시 딱 그 순간의 100GB 램 상태'를 영원히 온전하게 보존한 채로 하드디스크에 천천히 기록할 수 있는 것이다.

- **📢 섹션 요약 비유**: 빙하 속에 얼어붙은 매머드(자식 프로세스가 보는 메모리)를 연구소(하드디스크)로 옮겨야 합니다. 빙하를 통째로 얼음틀에 찍어내려면 수백 톤의 얼음(통짜 복사)이 필요하지만, [[542_cow_file_system|COW]] 마법을 쓰면 빙하 겉표면만 얇게 코팅(Read-Only)해두고, 날씨가 더워 얼음이 녹으려(Write) 할 때만 그 부분에 드라이아이스를 살짝 뿌려주며 0.1초 만에 완벽한 매머드 [[022_snapshot_backup_architecture|스냅샷]]을 떠내는 예술적 보존술입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: [[063_docker_architecture|도커]]([[063_docker_architecture|Docker]]) [[561_container_based_deployment|컨테이너]]와 KSM ([[631_ksm_kernel_samepage_merging|Kernel Samepage Merging]])
- 클라우드 서버에 1GB짜리 우분투 [[561_container_based_deployment|컨테이너]]를 100개 띄우면 100GB가 날아가야 한다. 하지만 [[063_docker_architecture|도커]]는 실행될 때 이미 베이스 이미지(Base Image)를 공유하고, `fork()`의 연속으로 파생되므로 수백 개의 [[561_container_based_deployment|컨테이너]]가 띄워져도 램 점유율은 몇 기가 오르지 않는다. (COW의 기본기)
- **KSM (중복 [[286_page_frame|페이지]] 병합)**:
   - 여기서 더 나아가, 리눅스 커널은 백그라운드에서 메모리를 스캔하다가 "어? [[561_container_based_deployment|컨테이너]] A의 10번 프레임과 [[561_container_based_deployment|컨테이너]] B의 50번 프레임 내용이 '100% 똑같은 [[001_dikw_pyramid|데이터]]'네?" 라는 걸 발견하면 흑마술을 부린다.
   - 프레임 2개 중 1개를 지워버리고, 두 [[561_container_based_deployment|컨테이너]]의 [[353_page_table|페이지 테이블]] 화살표를 남은 1개의 프레임에 묶어버린 뒤 **[[542_cow_file_system|COW]] (Read-Only)** 락을 걸어버린다!
   - 훗날 누군가 값을 바꾸면 어차피 COW로 다시 찢어주면 그만이다. 이 미친 "선 공유 후 복사" 기술 덕분에 [[713_kvm_over_ip|KVM]] 클라우드 호스팅 업체들은 64GB 램 서버에 100GB어치의 손님을 받아 과금하는 창조 경제(Memory Overcommit)를 달성했다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]: JVM과 Transparent Huge Pages의 결합
- COW는 4KB 조각 단위로 복사될 때 가장 가성비가 좋다. 
- 만약 리눅스의 [[371_huge_pages|거대 페이지]](THP, 2MB 단위)가 켜져 있는데 Redis가 `fork()` [[555_backup_and_restore_strategy|백업]]을 쳐서 COW가 걸렸다고 치자.
- 유저 1명이 들어와서 [[542_redis|Redis]] 변수 1바이트를 고쳤다(Write).
- OS는 이 1바이트 락을 풀기 위해 자그마치 **2MB 전체 덩어리([[517_huge_page|Huge Page]])를 통째로 복사**해서 찢어줘야 한다 ([[542_cow_file_system|COW]] 증폭). 1바이트 쓰려다 2MB 복사 렉이 터지는 것이다. 
- 이것이 인메모리 DB에서 THP([[371_huge_pages|거대 페이지]])를 절대 켜면 안 되는 두 번째 핵심 이유다. [[542_cow_file_system|COW]] 폭풍이 터지면 램이 빛의 속도로 갈려 나간다.

- **📢 섹션 요약 비유**: 4KB짜리 A4 용지(일반 [[286_page_frame|페이지]])를 공유하다가 글씨 하나 틀리면 A4 한 장만 복사해주면 됩니다. 하지만 전지 크기의 2MB짜리 대형 캔버스([[517_huge_page|Huge Page]])를 공유하다가 점 하나 찍겠다고 대형 캔버스를 통째로 복사해서 새로 사 오려면 돈(램)과 시간(CPU)이 거덜 나는 재앙입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 내용 |
|:---|:---|
| **[[104_process_creation|프로세스 생성]] 속도 $O(1)$** | `fork()` 시 램 [[001_dikw_pyramid|데이터]] 복사 없이 수 KB짜리 [[353_page_table|페이지 테이블]] 장부만 슥 복사하고 리턴하므로 앱 실행 딜레이 [[784_zeroization_circuit|제로화]] |
| **메모리(RAM) 용량 절약** | 90% 이상의 [[001_dikw_pyramid|데이터]]는 수정되지 않고 읽기만 하므로, 수백 개의 프로세스가 단 1벌의 물리 램을 돌려쓰는 극강의 가성비 달성 |
| **무중단 [[555_backup_and_restore_strategy|백업]]([[637_zfs_snapshot_cow_architecture|Snapshot]]) 인프라**| [[002_database_definition|데이터베이스]]나 [[501_file_definition_logical_record|파일]] 시스템(ZFS, Btrfs)이 [[090_service_kubernetes_network_load_balancing|서비스]] 정지(STW) 없이 수십 TB의 [[001_dikw_pyramid|데이터]]를 안전하게 [[194_consistency_database_integrity|일관성]] 보존([[194_consistency_database_integrity|Consistency]])하며 [[555_backup_and_restore_strategy|백업]] |

### 결론 및 미래 전망

[[289_cqrs_db|쓰기]] 시 복사 ([[542_cow_file_system|Copy-on-Write]], [[542_cow_file_system|COW]])는 하드웨어의 무식함(수직적 메모리 복사)을 소프트웨어의 교활함(가상 매핑과 게으름)으로 극복한 컴퓨터 구조 역사상 가장 완벽한 속임수다. 이 기술은 운영체제의 `fork()`를 혁신한 것을 넘어, 스토리지 [[501_file_definition_logical_record|파일]] 시스템(ZFS), 클라우드 [[561_container_based_deployment|컨테이너]]([[063_docker_architecture|Docker]] UnionFS), [[139_inmemory_db|인메모리 데이터베이스]]([[542_redis|Redis]]) 등 IT 인프라 전반을 떠받치는 '[[022_snapshot_backup_architecture|스냅샷]]([[637_zfs_snapshot_cow_architecture|Snapshot]])의 척추'로 성장했다. 앞으로 [[001_dikw_pyramid|데이터]]의 규모가 페타바이트를 넘어가며 물리적으로 복사하는 것 자체가 불가능해지는 빅데이터 [[190_ai_llm_requirements_specification|AI]] 시대에는, "[[001_dikw_pyramid|데이터]]는 절대 움직이지 않는다. 오직 장부의 화살표(포인터)만 조작될 뿐이다"라는 COW의 [[023_lazy_evaluation|지연 평가]]([[023_lazy_evaluation|Lazy Evaluation]]) 철학이 시스템 설계의 절대적 성경으로 영원히 굴림할 것이다.

- **📢 섹션 요약 비유**: 물건을 살 때마다 진짜 현금(Memcpy)을 다발로 들고 다니며 건네주다 허리가 휜 인류가, 처음에는 신용카드 장부([[286_page_frame|페이지]] 매핑)만 긋고 나중에 진짜 결제일(Write)이 닥쳐서야 내 통장에서 딱 필요한 돈만 몰래 빼가는([[542_cow_file_system|COW]]) 완벽한 현대 자본주의 신용 시스템의 탄생입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[391_anonymous_memory|익명 메모리]] ([[391_anonymous_memory|Anonymous Memory]]) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[392_file_backed_memory|파일 지원 메모리]] ([[392_file_backed_memory|File-backed Memory]]) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[394_vfork|vfork]]() | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[260_page_replacement|페이지 교체]] ([[260_page_replacement|Page Replacement]])의 필요성 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[파일 지원 메모리 (File-backed Memory)]
    │
    ▼
[쓰기 시 복사 (COW, Copy-on-Write)]
    │
    ├──▶ [vfork()]
    └──▶ [페이지 교체 (Page Replacement)의 필요성]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[289_cqrs_db|쓰기]] 시 복사 ([[542_cow_file_system|COW]], [[542_cow_file_system|Copy-on-Write]])은 컴퓨터가 메모리를 더 크게 보이게 하고 부족함을 숨기는 방법이에요.
2. 먼저 [[392_file_backed_memory|파일 지원 메모리]] ([[392_file_backed_memory|File-backed Memory]])을 이해하면 [[289_cqrs_db|쓰기]] 시 복사 ([[542_cow_file_system|COW]], [[542_cow_file_system|Copy-on-Write]])이 왜 필요한지 더 쉽게 보여요.
3. 그래서 [[289_cqrs_db|쓰기]] 시 복사 ([[542_cow_file_system|COW]], [[542_cow_file_system|Copy-on-Write]])을 잘 알면 나중에 [[394_vfork|vfork]]()도 훨씬 쉽게 배울 수 있어요.
