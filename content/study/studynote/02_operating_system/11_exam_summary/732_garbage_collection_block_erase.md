+++
weight = 732
title = "732. 가비지 컬렉션 블록 지우기 (Garbage Collection Block Erase)"
date = "2026-05-09"
[extra]
categories = "studynote-operating-system"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SSD의 [[380_garbage_collection|가비지 컬렉션]]([[380_garbage_collection|Garbage Collection]], GC)은 낸드 플래시 메모리의 "덮어쓰기 불가" 특성 때문에 필연적으로 쌓이는 **무효화된 쓰레기 [[286_page_frame|페이지]](Invalid [[286_page_frame|Page]])들을 한곳으로 모아, 블록(Block) 단위로 한 번에 폭파(Erase)시켜 새로운 빈 공간(Free Block)을 확보하는 백그라운드 청소 작업**이다.
> 2. **메커니즘**: FTL은 [[001_dikw_pyramid|데이터]]가 흩어진 여러 블록에서 '아직 살아있는 유효한 [[286_page_frame|페이지]](Valid [[286_page_frame|Page]])'만 골라 새로운 빈 블록으로 이사(Copy)시킨 뒤, 기존 블록 전체를 깨끗하게 포맷(Erase)하여 재사용 가능한 상태로 만든다.
> 3. **[[282_performance_tactics|성능]] 하락의 원인**: 이사(Copy)와 지우기(Erase) 작업은 일반적인 [[289_cqrs_db|쓰기]]보다 수백 배 느리다. 만약 디스크가 꽉 차서 사용자가 [[001_dikw_pyramid|데이터]]를 쓸 때마다 실시간으로 이 GC가 동작해야 한다면(On-demand GC), SSD의 [[289_cqrs_db|쓰기]] 속도가 [[465_hdd_structure|HDD]] 수준으로 곤두박질치는 **[[289_cqrs_db|쓰기]] 절벽(Write Cliff)** 현상이 발생하게 된다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **[[380_garbage_collection|가비지 컬렉션]] (GC)**: [[478_ftl_flash_translation_layer|FTL]]([[478_ftl_flash_translation_layer|Flash Translation Layer]]) 내부에서 수행되는 여유 공간 확보 [[001_algorithm_definition|알고리즘]].
  - **Valid [[286_page_frame|Page]]**: 현재 [[322_logical_virtual_address|논리 주소]](LBA)와 정상적으로 맵핑되어 있는 실제 유효한 [[001_dikw_pyramid|데이터]].
  - **Invalid [[286_page_frame|Page]] (Garbage)**: [[001_dikw_pyramid|데이터]]가 수정되어 새로운 곳에 쓰이면서, 예전 자리에 버려진(연결이 끊긴) 쓰레기 [[001_dikw_pyramid|데이터]].

- **필요성 (쓰레기장과 빗자루의 한계)**: 
  - 낸드 플래시는 4KB 단위로 [[001_dikw_pyramid|데이터]]를 쓸(Program) 수는 있지만, **지울 때(Erase)는 무조건 수 MB 크기의 블록(Block) 단위로만 지워야 한다.**
  - SSD를 쓰다 보면 1MB짜리 블록 안에 Valid [[286_page_frame|페이지]]와 Invalid [[286_page_frame|페이지]]가 바둑판처럼 섞이게 된다.
  - 빈 공간이 모자란다고 이 블록을 그냥 지워버리면, 그 안에 섞여 있던 Valid(살아있는) [[286_page_frame|페이지]]까지 몽땅 날아가는 대형 사고가 터진다.
  - **해결책**: "블록을 지우기 전에, 그 블록 안에 살아있는 애들만 일단 다른 새 아파트로 대피시키자! 그런 다음에 낡은 아파트를 통째로 폭파해 빈 땅을 만들자!" 이것이 [[327_ssd|SSD]] [[380_garbage_collection|가비지 컬렉션]]의 탄생이다.

  - 아파트(블록)에 100가구([[286_page_frame|페이지]])가 산다. 이 중 90가구는 이사를 갔고 10가구만 남아있다.
  - 재건축(지우기, Erase)을 하려면 이 아파트를 폭파해야 한다. 하지만 10가구가 아직 살고 있다.
  - **[[380_garbage_collection|가비지 컬렉션]]**: 남은 10가구를 새로 지은 옆 아파트(새 블록)로 짐을 다 옮겨준다(Copy). 이제 옛날 아파트가 완전히 텅 비었음을 확인하고, 다이너마이트로 시원하게 폭파(Erase)시켜 새로운 아파트를 지을 수 있는 공터(Free Block)로 만든다.

- **발전 과정**:
  1. **[[459_quic_fec_forward_error_correction|초기]] [[327_ssd|SSD]]**: 용량이 꽉 찰 때만 GC 수행 (사용 중 렉 발생 심각).
  2. **Background GC**: 컴퓨터가 쉴 때 몰래 청소하는 기능(BGC) 도입.
  3. **TRIM [[158_instruction|명령어]] 도입**: OS가 지워진 [[501_file_definition_logical_record|파일]]을 FTL에게 미리 알려주어 GC 효율을 극대화.

- **📢 섹션 요약 비유**: 헌 집 줄게 새집 다오. 헌 집에 남은 쓸만한 물건(Valid)만 새집으로 옮겨 담고, 쓰레기로 가득 찬 헌 집은 통째로 철거하여 다시 쓸 수 있는 깨끗한 땅(Free Block)을 만드는 토지 구획 정리 사업입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[380_garbage_collection|가비지 컬렉션]] (GC) 동작 파이프라인 시뮬레이션

FTL이 어떻게 Valid [[001_dikw_pyramid|데이터]]를 구출하고 블록을 [[459_quic_fec_forward_error_correction|초기]]화하는지 4단계로 본다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 SSD 가비지 컬렉션 (GC) 이사 및 폭파 시뮬레이션           │
  ├───────────────────────────────────────────────────────────────────┤
  │  [상황: Block X와 Block Y가 쓰레기(Invalid)로 가득 참]                  │
  │                                                                   │
  │   - Block X: [V1] [ I ] [ I ] [V2]  (V: Valid, I: Invalid)        │
  │   - Block Y: [ I ] [V3] [ I ] [ I ]                               │
  │   - Block Z: [ 비어있음 (Free Block) ]                              │
  │                                                                   │
  │  [ 1. Victim Block (희생 블록) 선정 ]                                │
  │   - FTL이 쓰레기(I)가 가장 많은 블록을 찾는다 -> Block X와 Y 당첨.         │
  │                                                                   │
  │  [ 2. 유효 데이터 복사 (Valid Page Copy) ]                           │
  │   - Block X의 V1, V2를 Block Z로 복사한다.                            │
  │   - Block Y의 V3를 Block Z로 복사한다.                               │
  │   - FTL 매핑 테이블 업데이트 (V1, V2, V3의 주소가 Block Z로 변경됨!)       │
  │                                                                   │
  │  [ 3. 희생 블록 폭파 (Erase Block) ]                                 │
  │   - 이제 Block X와 Y에는 쓰레기(I)만 남았다.                            │
  │   - 하드웨어에 Erase 명령을 내려 Block X, Y를 완전히 백지화(Free)시킨다.   │
  │                                                                   │
  │  [ 4. 결과 (Free Block 확보) ]                                      │
  │   - Block Z: [V1] [V2] [V3] [ 비어있음 ]  (사용 중)                   │
  │   - Block X: [ 완벽히 비어있음 ] (새로운 데이터를 받을 준비 완료)           │
  │   - Block Y: [ 완벽히 비어있음 ] (새로운 데이터를 받을 준비 완료)           │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 과정은 엄청난 고비용 작업이다. V1, V2, V3를 복사하느라 낸드 플래시에 쓸데없는 "읽기"와 "[[289_cqrs_db|쓰기]]"가 추가로 발생했다. 내가 저장하고 싶은 [[001_dikw_pyramid|데이터]]는 100MB인데, GC가 뒤에서 이삿짐을 나르느라 실제로 낸드 칩에 300MB를 쓰게 될 수도 있다. 이를 전문 용어로 **[[480_write_amplification|쓰기 증폭]] ([[696_waf_web_application_firewall|WAF]]: [[480_write_amplification|Write Amplification]] Factor)** 이라 하며, WAF가 높아질수록 SSD의 수명은 기하급수적으로 깎여나간다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### GC를 최적화하는 핵심 기술: TRIM [[158_instruction|명령어]]

OS와 [[327_ssd|SSD]] 사이의 보이지 않는 벽을 뚫어준 혁명적 기술이다.

| 상황 | TRIM 미지원 (과거) | TRIM 지원 (현대 OS) |
|:---|:---|:---|
| **OS에서 [[501_file_definition_logical_record|파일]] 삭제 시** | OS만 [[501_file_definition_logical_record|파일]] 시스템(ext4)에서 삭제 표시. **SSD는 모름.** | OS가 [[327_ssd|SSD]] 컨트롤러에 **"LBA 100~200번 지웠음!"** 이라고 통보. |
| **[[327_ssd|SSD]] FTL의 상태 인지** | 해당 [[286_page_frame|페이지]]를 여전히 **Valid(살아있는 [[001_dikw_pyramid|데이터]])**로 착각. | 해당 [[286_page_frame|페이지]]를 즉시 **Invalid(쓰레기)**로 마킹. |
| **GC 수행 시 결과** | 지워진 [[501_file_definition_logical_record|파일]]인데도 새 블록으로 힘들게 복사함 ([[696_waf_web_application_firewall|WAF]] 폭발) | 복사 안 하고 그냥 블록째 폭파해 버림 ([[696_waf_web_application_firewall|WAF]] 1에 수렴) |
| **[[282_performance_tactics|성능]] 결과** | SSD를 오래 쓸수록 극도로 느려짐 (쓰레기 이사 지옥) | **몇 년을 써도 새것처럼 빠른 속도 유지** |

### 과목 융합 관점

- **프로그래밍 언어 (Java GC)**: 흥미롭게도 SSD의 GC는 Java 가상머신(JVM)의 [[380_garbage_collection|가비지 컬렉션]] 중 **Mark-and-Compact** 또는 **Copying GC** [[001_algorithm_definition|알고리즘]]과 100% 동일한 철학을 갖는다. 흩어진 객체([[286_page_frame|페이지]]) 중 살아있는 놈(Valid)만 서바이버 영역(빈 블록)으로 쫙 복사하고, 원래 있던 에덴(Eden) 영역을 통째로 밀어버리는 구조가 하드웨어 낸드 플래시 레벨에서 정확히 똑같이 재현된 것이다.

- **📢 섹션 요약 비유**: TRIM이 없으면, 직원이 퇴사해도 경비실([[478_ftl_flash_translation_layer|FTL]])에 알려주지 않아서 경비실은 퇴사자 자리까지 매일 청소하고 짐을 챙겨줍니다. TRIM은 "얘 퇴사했으니까 그 자리 물건은 그냥 다 쓰레기통에 버려!"라고 명확히 통보하여 경비원의 과로사를 막아주는 사내 메신저입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — [[002_database_definition|데이터베이스]]([[502_dbms|DBMS]]) 서버의 Write Cliff ([[289_cqrs_db|쓰기]] 절벽) 현상**: 새로 산 1TB [[482_nvme|NVMe]] SSD에 MySQL을 올리고 초당 1만 건의 [[289_cqrs_db|쓰기]] 테스트를 했다. 처음 5분은 3GB/s로 미친 듯이 빠르더니, 디스크가 900GB쯤 차는 순간 [[289_cqrs_db|쓰기]] 속도가 100MB/s로 수직 낙하하며 DB가 뻗음.
   - **원인 분석**: 디스크가 비어있을 때는 GC 없이 그냥 Free Block에 쭉쭉 썼다. 하지만 용량이 꽉 차서 여유 블록이 사라지자, FTL이 **"사용자의 [[289_cqrs_db|쓰기]] 요청을 잠시 멈춰 세우고([[122_sync_async_communication|Blocking]]), 급하게 GC를 돌려 쓰레기를 비운 뒤에야 [[001_dikw_pyramid|데이터]]를 쓰는" (On-demand GC)** 최악의 상황이 터진 것이다. 지우기(Erase)는 [[289_cqrs_db|쓰기]](Program)보다 10배 이상 느리므로 속도가 절벽처럼 떨어졌다.
   - **대응 (오버 [[528_provisioning|프로비저닝]], Over-Provisioning)**: 엔터프라이즈 환경에서는 [[327_ssd|SSD]] 전체 용량의 20~30%를 [[514_partition_slice_volume|파티션]] 잡지 않고 '할당되지 않은 공간(Unallocated Space)'으로 놔두어야 한다. 이 숨겨진 공간은 FTL이 평소에 여유롭게 백그라운드 GC(BGC)를 돌릴 수 있는 '숨통(Free Block Pool)' 역할을 하여, Write Cliff 현상을 원천적으로 방어한다. (삼성/인텔 엔터프라이즈 SSD가 비싼 이유가 이 OP 공간이 하드웨어적으로 크게 잡혀있기 때문이다.)

2. **시나리오 — 스토리지 [[450_benchmark_test|벤치마크 테스트]] 시 결과가 널뛰기하는 현상**: 서버 엔지니어가 `fio` 툴로 [[327_ssd|SSD]] [[282_performance_tactics|성능]]을 측정하는데, 돌릴 때마다 IOPS 결과가 2배씩 차이가 남.
   - **원인 분석**: 1차 테스트 때 썼던 쓰레기 [[001_dikw_pyramid|데이터]]들이 [[327_ssd|SSD]] 내부에 가득 찬 상태에서, 백그라운드 GC가 돌기 전에 2차 테스트를 바로 돌렸기 때문이다.
   - **기술사적 가이드**: 정확한 [[327_ssd|SSD]] 벤치마크를 위해서는, 테스트 직전에 **`blkdiscard` (리눅스 TRIM 강제 호출 [[158_instruction|명령어]])**나 `Secure Erase`를 실행하여 [[327_ssd|SSD]] 전체를 공장 출고 상태(모든 블록이 Free)로 [[459_quic_fec_forward_error_correction|초기]]화한 뒤 테스트해야 한다. 또한 'Sustain(지속)' [[282_performance_tactics|성능]]을 보려면 일부러 디스크를 100% 꽉 채운 뒤, 1시간 이상 Write를 지속하여 강제로 GC가 동작하는 최악의 조건(Steady [[272_state_pattern|State]])에서의 바닥 [[282_performance_tactics|성능]]을 측정하는 것이 진짜 실무 벤치마킹이다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 SSD 스토리지 수명(TBW) 및 성능 방어 아키텍처 플로우         │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [DB/카프카 등 Write-Intensive(쓰기 집약적) 서버 인프라 설계]              │
  │                │                                                  │
  │                ▼                                                  │
  │      사용 중인 파일 시스템과 OS 커널이 주기적인 TRIM을 지원하는가?            │
  │          ├─ 예 ─────▶ [Cron / Systemd timer로 주 1회 fstrim 스케줄링]  │
  │          │            (실시간 discard 옵션(mount -o discard)은 I/O 딜레이를 │
  │          │             유발하므로, 야간에 배치로 주 1회 몰아서 지우는 걸 권장)    │
  │          └─ 아니오 ──▶ ZFS 등 구형 환경이라면 펌웨어 레벨 튜닝 절실          │
  │                │                                                  │
  │                ▼                                                  │
  │      서비스 오픈 후 디스크 사용량 임계치(Alert Threshold)를 몇 %로 잡을 것인가?│
  │          ├──▶ [일반 서버: 80% / DB 서버: 70% 설정 권장]                 │
  │          │    결론: HDD 시절에는 95% 찰 때까지 버텨도 성능 저하가 없었지만,    │
  │          │          SSD는 80%를 넘기면 GC 효율이 극감하여 WAF가 폭발한다.      │
  │          │          디스크가 70% 찼을 때 무조건 용량 증설(Scale-up)을 해야 한다.│
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** "디스크 용량 = 속도"라는 공식은 [[327_ssd|SSD]] 시대의 새로운 진리다. 1TB SSD에 900GB의 짐이 차 있으면, FTL은 빈 100GB 방을 찾기 위해 이삿짐을 미친 듯이 이리저리 빼고 넣어야 한다(GC). 방이 500GB 비어 있으면 이삿짐을 그냥 대충 휙휙 던져도(최소한의 GC) 정리가 된다. 디스크 용량을 넉넉하게 유지하는 것 자체가 최고의 I/O [[282_performance_tactics|성능]] 튜닝이다.

### 도입 [[435_checklist_based_testing|체크리스트]]
- **Swap [[514_partition_slice_volume|파티션]]의 [[327_ssd|SSD]] 수명 갉아먹기**: 리눅스의 Swap 공간을 SSD에 잡아두면, 메모리가 꽉 찰 때마다 OS가 4KB 단위로 미친 듯이 Swap I/O를 날린다. 이는 SSD의 WAF를 폭발시켜 1년 만에 디스크를 폐기 처분하게 만든다. K8s가 시스템 레벨에서 스왑을 강제로 꺼버리는(Disable) 가장 중요한 하드웨어적 이유 중 하나가 바로 이 [[327_ssd|SSD]] [[380_garbage_collection|가비지 컬렉션]]의 과부하 방지다.

- **📢 섹션 요약 비유**: 퍼즐 맞추기를 할 때, 책상이 텅 비어있으면 10초 만에 맞춥니다(새 [[327_ssd|SSD]]). 그런데 책상 위에 잡동사니가 90% 차 있으면, 퍼즐 한 조각 맞출 때마다 다른 물건을 치워가며(GC) 해야 해서 1시간이 걸립니다(Write Cliff). 책상([[327_ssd|SSD]])은 항상 30% 이상 비워두는 것이 정신건강에 좋습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | GC 미지원 / 용량 95% 포화 상태 | OP 20% 및 TRIM 기반 BGC 활성화 | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (I/O [[194_consistency_database_integrity|일관성]])**| Write 시 간헐적으로 수십 ms 정지 | **초당 10만 IOPS 지속 유지 (Steady)**| [[141_latency|Latency]] Jitter 없는 고성능 인프라 확보 |
| **정량 (수명, TBW)**| [[696_waf_web_application_firewall|WAF]] 상승으로 셀 마모도(Wear) 급증 | [[696_waf_web_application_firewall|WAF]] 1.x 수렴으로 불필요한 Erase 방지 | 엔터프라이즈 스토리지 물리적 수명 2배 연장 |
| **정성 (유지보수)** | 디스크 풀 시 서버 동반 멈춤 위험 | 백그라운드 자가 치유(Self-healing) | 인프라 엔지니어의 장애 대응 공수 절감 |

### 미래 전망
- **호스트 주도 [[380_garbage_collection|가비지 컬렉션]] (Host-Managed GC)**: 칩셋 안의 조그만 FTL이 낑낑대며 GC를 하는 것은 비효율적이다. 최신 Open-Channel [[327_ssd|SSD]] (또는 [[482_nvme|NVMe]] [[703_zns_ssd|ZNS]])는 아예 SSD가 스스로 GC를 하지 못하게 막고, 호스트의 거대한 [[001_operating_system_purpose|운영체제]](Linux [[022_kernel_role|커널]]) CPU가 "지금 서버 한가하니까 네가 직접 쓰레기 치워!"라고 지시하는 형태로 하드웨어 주도권을 소프트웨어로 다시 뺏어오는 아키텍처 혁명이 일어나고 있다.

### 결론
[[380_garbage_collection|가비지 컬렉션]](GC)은 "한 번 쓰면 지우기 전엔 다시 쓸 수 없다"는 낸드 플래시의 태생적 저주를 풀기 위해 발명된 인류의 눈물겨운 [[032_firmware|펌웨어]] 노가다다. 빛의 속도로 [[001_dikw_pyramid|데이터]]를 읽고 쓰는 화려한 SSD의 스펙 시트 이면에는, 우리가 컴퓨터를 끄고 자는 그 고요한 밤에도 블록을 이리저리 옮기며 묵묵히 쓰레기장을 청소하고 공터를 만들어내는 FTL의 백그라운드 땀방울이 서려 있다. SSD의 진짜 실력은 새 제품을 샀을 때의 벤치마크 점수가 아니라, [[001_dikw_pyramid|데이터]]를 100번 꽉 채우고 지우기를 반복했을 때 이 GC가 얼마나 영리하게 쓰레기를 비워내느냐(Steady [[272_state_pattern|State]])에 달려있다.

- **📢 섹션 요약 비유**: 우아하게 물 위를 헤엄치는 백조(빠른 [[327_ssd|SSD]])의 발밑에서는 물갈퀴([[380_garbage_collection|가비지 컬렉션]])가 미친 듯이 물을 휘젓고 있습니다. 백조가 지치지 않게 하려면 쓰레기(불필요한 [[289_cqrs_db|쓰기]])를 덜 버리고, 호수(디스크 여유 공간)를 넓게 유지해 주는 배려가 필요합니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[484_raid_0_striping|RAID 0]], 1, 5, 6 [[282_performance_tactics|성능]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[731_ssd_ftl_flash_translation_layer|SSD FTL]] ([[478_ftl_flash_translation_layer|Flash Translation Layer]]) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[501_file_definition_logical_record|파일]] 시스템 연속, 연결, [[526_indexed_allocation|색인 할당]] | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[525_fat_file_allocation_table|FAT]] 방식 [[524_linked_allocation|연결 할당]] 최적화 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[SSD FTL (Flash Translation Layer)]
    │
    ▼
[가비지 컬렉션 블록 지우기 (Garbage Collection Block Erase)]
    │
    ├──▶ [파일 시스템 연속, 연결, 색인 할당]
    └──▶ [FAT 방식 연결 할당 최적화]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 칠판(블록)에 글씨([[286_page_frame|페이지]])를 가득 썼어요. 군데군데 틀린 글씨(쓰레기)가 있지만, 이 칠판은 아주 특이해서 글자 1개만 지울 수 없고 무조건 '물뿌리개'로 칠판 전체를 한방에 지워야 해요.
2. 하지만 칠판에 아직 남아있는 중요한 글자들도 있잖아요? 이걸 그냥 지우면 혼나겠죠!
3. 그래서 똑똑한 비서([[478_ftl_flash_translation_layer|FTL]])가 중요한 글자들만 재빨리 옆에 있는 새 칠판에 예쁘게 옮겨 적은(Copy) 다음, 헌 칠판에 물을 쫙 뿌려서 깨끗한 새 칠판으로 만들어(Erase) 놓는답니다! 이걸 [[380_garbage_collection|가비지 컬렉션]]이라고 해요.
