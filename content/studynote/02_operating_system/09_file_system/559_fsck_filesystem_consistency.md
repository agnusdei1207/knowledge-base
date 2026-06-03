---
title: 559. 파일 시스템 일관성 검사 (fsck / chkdsk)
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 디스크에 [[501_file_definition_logical_record|파일]]을 쓸 때는 (1)방명록([[506_directory_structure_symbol_table|디렉터리]]) 작성 $\to$ (2)문패(i-node) [[087_process_state_transition|생성]] $\to$ (3)방 짐 넣기([[001_dikw_pyramid|Data]] Block) 라는 3박자 동기화가 필수다. 근데 짐통을 문 찰나에 "정전 크래시([[069_type_1_2_error_statistical_power|Power]] Failure 뇌사 랙!)" 가 터지면? 방에는 짐이 꽉 찼는데 문패는 비어있다는 모순(Inconsistency)이 발생해 [[501_file_definition_logical_record|파일]] 시스템 생태계가 붕괴한다. **`fsck`** 는 이 어긋난 **"3박자 장부들의 톱니바퀴를 하드디스크 밑바닥부터 뒤져서 앞뒤 핀(링크 수, 할당 상태)을 강제 일치시켜 꿰매는 고강도 렌더링 검사기"** 다.
> 2. **가치**: `fsck` 수술 로봇 록백 덕분에, 목이 날아간 [[501_file_definition_logical_record|파일]](이름표가 지워진 찌꺼기 덩어리)을 버리지 않고 `lost+found` (고아원 폴더)에 안전하게 임시 수용($O(1)$ 대피소 스왑) 하여, 유저가 어떻게든 소중한 [[001_dikw_pyramid|데이터]]를 하나라도 구조 건져낼 수 있는 시스템 불멸성(Resilience) 통치 구조를 탄생시켰다 포팅.
> 3. **한계**: 가장 끔찍한 딜레마. 옛날 ext2 시절엔 서버 용량이 1TB면, `fsck` 가 1번부터 1TB 블록 전체를 거북이처럼 기어 다니며 장부를 크로스 체크해야 해서(Full Scan I/O [[573_timeout_retry_backoff_strategy|타임아웃]] 랙) 부팅이 무려 3시간이나 숨을 멈추고 서버가 마비되는 미친 오버헤드 늪을 낳았다. 이 죽음의 시간이 못 견디게 끔찍하여 **[[539_journaling_file_system|저널링 파일 시스템]](539장 Journaling 방패 결착!)** 이 지구상에 진화하게 된 가장 완벽한 인과 모순을 안고 있다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **장부 불일치 붕괴 (Inconsistency 멸망 파단 늪)**: 유저가 100GB [[501_file_definition_logical_record|파일]]을 지울 때 [[022_kernel_role|커널]]은 "i-node 제거 $\to$ [[001_dikw_pyramid|Data]] 블록 빈공간 장부(Free List) 체크표시" 순서대로 도장을 찍는다. 그런데 i-node 명패만 딱 떼어내 쓰레기통에 버린 0.001초 찰나에 블루스크린(Crash)이 터졌다. 재부팅 후 [[022_kernel_role|커널]]이 볼 때, 그 100GB 짐은 이름이 없으니 '주인 없는 땅(Unallocated)' 이면서 동시에 빈칸 장부엔 도장이 안 찍혀 있어 '쓸 수 없는 땅(Allocated)' 이라는 극악의 교착 데들락(Orphan Block)에 빠져버린다.
  - **fsck 체크 디스크 (장부 꿰매기 재봉틀 수술 빔!)**: 리눅스의 `fsck`([[501_file_definition_logical_record|File]] System [[194_consistency_database_integrity|Consistency]] Check), 윈도우의 `chkdsk` 백신 발싸! 수술 봇이 깨어난다. 1원칙 "슈퍼블록([[518_vfs_objects_superblock_inode_dentry_file|Superblock]] 전체 용량)은 무사한가?" $\to$ 2원칙 "모든 i-node 가 품은 고기([[001_dikw_pyramid|Data]] Block) 개수와 전체 빚(할당된 디스크 공간)의 [[003_integrity|무결성]] 대차가 딱 맞는가?" 이중 장부 [[606_auditing_linux_auditd|감사]]([[363_audit|Audit]] 기전)를 통해 불일치 블록 쓰레기들을 강제 삭제하거나 분리수거 때린다 스왑.
- **필요성**: 정전([[069_type_1_2_error_statistical_power|Power]] Loss)이나 [[036_kernel_panic|커널 패닉]]은 인류 [[001_operating_system_purpose|운영체제]] 역사상 피할 수 없는 철판 서버의 숙명이다. 장부가 1바이트라도 어긋난 상태로 계속 [[501_file_definition_logical_record|파일]]을 쓰게 놔두면 엉뚱한 다른 유저의 정상 [[501_file_definition_logical_record|파일]] 위를 덮어 써버리는(Systemic Overwrite 부패 데들락) 디스크 전염병이 창궐한다. 이것을 [[517_virtual_file_system_vfs|VFS]] 최하단에서 차단 방역할 수학적 [[352_defect_definition|결함]] 복원기가 필연적으로 요구되었다 증명.

  - (정전 크래시 장부 파괴 늪): 은행원(OS)이 손님(앱)한테 100만 원 받아 금고에 방금 탁! 넣었는데 컴퓨터 장부에 "+100만 원" 엔터 치려는 순간 벼락이 쳐서 은행 전체 퓨즈가 나갔습니다. 내일 출근해보니 금고 안의 총액(실제 [[001_dikw_pyramid|Data]] Block)과 컴퓨터 장부(i-node 포인터) 액수가 안 맞아 금고 문이 영원히 닫혀버립니다 락업 에러!
  - **(fsck [[606_auditing_linux_auditd|감사]] 수술 기전!)**: 새벽에 피도 눈물도 없는 **[본사 최고 [[606_auditing_linux_auditd|감사]]원(fsck 결산 빔!)]** 이 뛰어옵니다 스왑! 아무도 은행을 못 쓰게 셔터([[516_mount_mechanism|마운트]] 해제 Offline 타격!)를 잠가버립니다. 그리고 10원짜리 동전 하나까지(블록 1번~1억 번까지) 바닥에서 다 기어 다니며 세알립니다. "야! 금고에 100만 원 남는데 주인이(i-node 매핑) 장부에 없네? 이거 일단 [lost+found 고아원 박스] 에 담아놔! 장부 강제 일치시켜 샷다 열어!" 라며 [[003_integrity|무결성]] 발란스(Balance)를 억지로라도 맞춰내는 재재건 기적(방검복 스피드!)입니다 결속!

- **fsck 다단계 스캔 (Pass 1~5) 장부 대차 크로스 조인 [[103_ascii|ASCII]] 뷰**:
부팅될 때 화면에 주르륵 올라오는 `fsck Pass 1, 2, 3..` 이 도대체 뭘 검사하며 디스크를 갈아 마시는지 그 렌더를 까보면 다음과 같다.

```text
  ┌──────────────────────────────────────────────────────────────────────────────────────────┐
  │                 "i-node 장부와, Data 고기 덩어리의 숫자가 한 치의 어긋남도 없어야 한다!" │
  ├──────────────────────────────────────────────────────────────────────────────────────────┤
  │                                                                                          │
  │  🚨 [ 정전 크래시로 망가진 더티(Dirty) 상태의 디스크 마운트 시도! ]                      │
  │     => 커널 봇: "오쉣! Unclean Shutdown 낙인 발견! fsck 강제 출동 빔!"                   │
  │                                                                                          │
  │  =========================▼===================================                           │
  │                                                                                          │
  │  ✅ [ PASS 1: 모든 i-node 대탈곡 확인 록백 ]                                             │
  │     - "장부에 적힌 i-node 번호가 정상적인가? 지워진 애가 가짜로 살아있나?"               │
  │                                                                                          │
  │  🔥 [ PASS 2: 디렉터리 트리 (이름표) 뼈대 조립 스위치 늪 ]                               │
  │     - "폴더 이름(apple.txt)은 있는데, 가리키는 i-node (150번)이 파괴됐어!                │
  │       => (조치 빔): 폴더 이름표 강제 삭제! (Unlinked Error 치료 스루풋)"                 │
  │                                                                                          │
  │  ✅ [ PASS 3: 폴더 고아원 수용소 (lost+found 렌더) 연결망! ]                             │
  │     - "어라? 200번 i-node는 멀쩡히 살아서 데이터(영화)를 갖고 있는데,                    │
  │       세상 어떤 폴더 트리에도 이 200번을 가리키는 연결 고리가 없네?! 고아다!"            │
  │       => (조치 빔): 200번 고아를 통째로 뜯어다가 /lost+found/#200 으로                   │
  │                     강제 이주(Re-link 생명 연장 포팅) 시켜버림 컷!                       │
  │                                                                                          │
  │  🔥 [ PASS 4 & 5: 남은 찌꺼기 빚 청산 (Free Block List) 결산 타격! ]                     │
  │     - "i-node 들이 쓰고 있는 총 고기 블록 숫자를 더해보자 = 10만 개."                    │
  │     - "근데 전체 용량 장부(슈퍼블록)에는 9만 개라고 적혀있어? 야 숫자 고쳐!"             │
  │       => (조치 빔): 비트맵(Bitmap) 장부를 실제 바닥 상태와 동일하게 덧칠 완료!           │
  └──────────────────────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** fsck가 거치는 극단적인 이중 대조(Cross Check) 알고리즘의 뼈대다. [[501_file_definition_logical_record|파일]] 시스템 에러의 핵심은 "쓰레기를 안고 사는 것(Orphan Inode)" 과 "멀쩡한 집을 두 명에게 겹쳐 파는 것([[001_dikw_pyramid|Data]] Block Overlapping)" 이다. 이 미스매치는 오직 [[506_directory_structure_symbol_table|디렉터리]] $\to$ i-node $\to$ 물리 Block 이라는 3각 연결 고리를 1번부터 1억 번까지 수동으로 순회 점검해야만 모순 파단을 잡아낼 수 있다. 수술이 성공하면 주소 잃은 [[501_file_definition_logical_record|파일]]들은 `#123445` 같은 기괴한 번호표를 달고 최상위 록백 동굴인 `lost+found` 방에 모여 유저의 살처분 결정을 대기하게 된다 도출 통달.

- **📢 섹션 요약 비유**: 복잡한 창고에서 필요한 물건을 찾기 위해 먼저 구역과 표지판을 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 트레이드오프 전선 종결: 극악 오버헤드 fsck (과거형) vs 총알 저널 [[658_ir_recovery|복구]] (현대형 록백)
100TB 짜리 디스크에 정전 1방이 터지면 서버 리부팅에 걸리는 시간의 차이가 보여주는 [[100_sre_site_reliability_engineering_error_budget|SRE]] 멸망전.

| 시스템 복원 아키텍처 뷰 | ext2 무식한 스캔 `fsck` (장부 전체 바닥 탈곡기 늪) | ✨ ext4 저널링 (Journal 방패 복원 스왑) |
|:---|:---|:---|
| **크래시 후 [[658_ir_recovery|복구]] 범위 스캔 I/O량** | **1번 블록부터 100TB 끝까지 무지성으로 전체 장부를 싹 다 긁어 퍼즐 맞춤 파단.** | 정전 나기 직전에 쓰던 **'최근 일기장 50MB 한 칸'** 만 쓱 읽고 복원 컷! $O(1)$ 스피드 부스트. |
| **서버 부팅(Reboot) 강제 병목 시간** | 병원, 공장 서버 정전 후 켜질 때 `fsck` 만 **3시간~하루 종일 걸리며 [[090_service_kubernetes_network_load_balancing|서비스]] 올 마비 사형.** | 전원이 나가도 **1초~3초 만에 [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]] 꿰매버리고 쿨하게 정상 부팅 록백 폭주.** |
| **현대 fsck 의 위상 및 용도 변경 빔** | 매번 크래시 날 때마다 불려 가는 노예 청소기 역할의 **[[282_performance_tactics|성능]] [[015_지연_데이터_관점|지연]] 파멸의 원흉 데들락.** | 평소엔 저널(일기)이 다 고치고, 저널마저 박살나는 최악 초토화 상태에만 꺼내는 **최후의 구명보트 통제.** |

### 2. 치명적 오버헤드 폭발: 오프라인(Offline) 검사에 묶인 스토리지 셧다운 마비 랙
[[501_file_definition_logical_record|파일]] 시스템 점검 툴이 절대 살아 움직이는 기차(온라인 [[516_mount_mechanism|마운트]]) 안에서는 바퀴를 고칠 수 없는 구조적 치명 파편을 해석한다.

- **[[128_water_scrum_fall_anti_pattern|안티패턴]] 오염 발생 미스터리 (Online [[516_mount_mechanism|마운트]] 상태에서의 fsck 충돌 파괴 늪 스왑)**: 
  - (온라인 수술의 파단 데들락 랙): [[100_sre_site_reliability_engineering_error_budget|SRE]] 신입이 서버가 살아서 디스크 [[501_file_definition_logical_record|파일]]들이 막 I/O 되고 있는 쌩쌩한 `/var` 볼륨을 둔 채 강제로 `fsck -f /var` 검사 명령을 때려버렸다. 
  - ([[193_atomicity_all_or_nothing|원자성]] 붕괴 빔 결합 발동!): 뇌 수술(`fsck` 봇)을 하는데, 환자([[022_kernel_role|커널]] [[517_virtual_file_system_vfs|VFS]])가 계속 머리를 흔들며([[501_file_definition_logical_record|파일]] [[087_process_state_transition|생성]]/삭제 지속!) 장부를 실시간으로 갱신하고 있다.
  - 파멸 결과: 수술 봇이 "어? 10번 i-node 비었네? 쓰레기로 날리자!" 라고 도끼를 내리찍는 0.1초 찰나에 유저 프로그램이 10번 i-node에 중요 [[001_dikw_pyramid|데이터]]를 막 저장했다! 결과적으로 정상 [[501_file_definition_logical_record|파일]]이 수술 로봇의 칼빵을 맞고 다 분해되어 디스크 전체가 **[[658_ir_recovery|복구]] 불가능 [[036_kernel_panic|커널 패닉]] 쓰레기 지옥판으로 산산조각 붕괴 멸망([[001_dikw_pyramid|Data]] Corruption) 한다 증명.**
- **[[100_sre_site_reliability_engineering_error_budget|SRE]] 극복 솔루션 패치 타결 조율 (런레벨 Single Mode 와 Read-Only 강제 록백!!) / 수술대 방패**: 
  - 엔지니어 1방 철칙!: 리눅스의 절대 명언. "움직이는 기차 바퀴는 멈추고 고쳐라!" 
  - 진압(Unmount) 포팅 기전: 반드시 심각한 디스크 오류 [[658_ir_recovery|복구]]는 해당 디스크를 **[[516_mount_mechanism|마운트]] 해제(Unmount 접속 차단 렌더)** 하거나, 기껏해야 절대 [[501_file_definition_logical_record|파일]]을 쓸 수 없는 **오직 읽기 모드(Read-Only 기브스 묶기)** 로 족쇄를 채운 다음 돌려야 한다. 이 때문에 부팅이 안 될 때 [[359_usb|USB]] 구조 디스크(Live CD) 로 들어가서 고치는 싱글 모드(Single User Rescue) 운영 전략이 IT 부서 생명 연장의 기본기로 박혔다 증명 록보장.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 하드디스크 긁힘(Bad Sector) 철판 파괴를 [[369_logic_bomb|논리]] 소프트웨어(fsck)로 치료하겠다는 무지의 참사
물리적 디스크 바늘이 긁힌 데드존(Dead Zone)을 억지로 꿰매려다 [[100_sre_site_reliability_engineering_error_budget|SRE]] [[573_timeout_retry_backoff_strategy|타임아웃]] 멸망 폭주를 일으키는 늪 뷰.

- **[[128_water_scrum_fall_anti_pattern|안티패턴]] 충돌 (Bad Block 탈곡기에 갈려 들어가는 fsck 셧다운 파단 랙)**: 
  - 오래된 [[465_hdd_structure|HDD]] 디스크 표면에 철 바늘이 긁혀서 "읽기 금지(물리적 배드 섹터 고장)" 가 생겼다. 
  - 초보 관리자가 이걸 고친다고 끝끝내 `fsck -c` (배드 블록 점검 옵션 빔) 를 날리고 퇴근했다.
  - 절단 발생: fsck 봇은 이 배드 블록을 읽으려다 하드웨어 컨트롤러가 거부하며 랙이 걸리자 수만 번 재시도 통신(Retries 오버헤드 폭파)을 하며 디스크 헤드를 박박 갈아버린다. 다음 날 아침, 조금 고장 났던 하드는 밤새 fsck 봇의 미친 박치기 진동 칼춤에 완전히 박살 나 서버 디스크가 100% 영구 사망(Wipe Out)하는 충격 트레이드오프 [[123_pipe|파이프]].
- **[[100_sre_site_reliability_engineering_error_budget|SRE]] 엔지니어 도축 솔루션 (S.M.A.R.T. 하드 센서 폐기와 ZFS 자가 치유 렌더 방어 빔!)**: 
  - [[100_sre_site_reliability_engineering_error_budget|SRE]] 무결 선고!: **물리 블록 망가짐은 소프트웨어(fsck)로 고치는 게 아니야, 디스크 뜯어서 버리고 [[555_backup_and_restore_strategy|백업]] [[658_ir_recovery|복구]]해!!**
  - 자가 치유(Self-Healing 564장 연계) 스로틀 발사: 최근 ZFS나 Btrfs 같은 괴물 [[501_file_definition_logical_record|파일]] 시스템은, 아예 `fsck` 같은 외부 사후 수술 도구를 쓰레기통에 폐기했다. 읽다가 블록이 망가졌어? 실시간 컨트롤러가 알아서 거울 볼륨(Mirror)에서 복사 땡겨와 정상 블록으로 슬쩍 바꿔 치기(On-the-fly Repair $O(1)$) 해버리는 영구 불멸의 백그라운드 스크러빙(Scrub 타격) 진화 메타로 구원해버렸다 [[396_validation|확인]] 끝장.

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- '[[501_file_definition_logical_record|파일]] 시스템 [[194_consistency_database_integrity|일관성]] 검사 (`fsck` 오프라인 장부 재봉틀 렌더)' 아키텍처는 전기 끊어짐, [[036_kernel_panic|커널 패닉]]이라는 예측 불가의 IT 아포칼립스 늪 한복판에서, OS가 스스로 1과 0의 질서를 바닥부터 재구성하여 시스템의 코마 상태를 멱살 잡고 부활시키는 [[100_sre_site_reliability_engineering_error_budget|SRE]] 운영의 1차 심폐소생술 뼈대다.
- 길 잃은 [[001_dikw_pyramid|데이터]](Orphan Block)와 무주공산 포인터를 찾아내어 시스템 트리 안에 어떻게든 안착(lost+found 고아 묶기 스왑 $O(1)$ 비율) 시키는 놀라운 잉여 [[658_ir_recovery|복구]] 엔진을 통해, 고객의 [[001_dikw_pyramid|데이터]] 손실을 최후의 [[074_byte|바이트]] 수준까지 방어하는 엔터프라이즈 신뢰망을 지배했다 선고.
- 비록 10TB가 넘는 대용량 스토리지 시대에 들어서면서 검사 시간이 수 일(Days) 단위로 치솟는 미친 속도 한계(Scan [[141_latency|Latency]] 마비 모순 데들락 랙) 트레이드오프를 맞이하게 되었지만, 이를 해결하기 위해 **저널링(Journaling [[568_logs_distributed_logging_elk_fluentd|로그]] 방패)** 과 [[542_cow_file_system|COW]] 덩어리를 흡수한 현대 [[501_file_definition_logical_record|파일]] 시스템 밑바탕 거름으로 장렬히 산화 [[164_scattering_reflection_radio_waves|산란]](Disperse Tooling)하며 여전히 마비의 최후 보루 영구 진화 요새로 록백 보장.

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

[[501_file_definition_logical_record|파일]] 시스템 [[194_consistency_database_integrity|일관성]] 검사 (fsck / chkdsk)은 [[501_file_definition_logical_record|파일]] 시스템과 [[506_directory_structure_symbol_table|디렉터리]] 구조을 이해하는 연결 고리 역할을 한다. 이 개념을 익히면 시스템 동작을 더 예측 가능하게 설명할 수 있지만, 만능 해법은 아니므로 적용 전제와 한계를 함께 기억해야 한다. 앞으로는 [[560_multi_stream_file_fork_ads|다중 스트림]] ([[560_multi_stream_file_fork_ads|Multi-stream]]) [[501_file_definition_logical_record|파일]] / 포크 (Forks)처럼 더 세분화된 기술과 결합되며 자동화·최적화 방향으로 발전한다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[557_tmpfs_ramfs_memory_filesystem|임시 파일 시스템]] (tmpfs / ramfs) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 가상 장치 [[501_file_definition_logical_record|파일]] 시스템 (sysfs, procfs) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[560_multi_stream_file_fork_ads|다중 스트림]] ([[560_multi_stream_file_fork_ads|Multi-stream]]) [[501_file_definition_logical_record|파일]] / 포크 (Forks) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[561_encrypted_file_system_ecryptfs|암호화 파일 시스템]] (eCryptfs / Windows EFS) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[가상 장치 파일 시스템 (sysfs, procfs)]
    │
    ▼
[파일 시스템 일관성 검사 (fsck / chkdsk)]
    │
    ├──▶ [다중 스트림 (Multi-stream) 파일 / 포크 (Forks)]
    └──▶ [암호화 파일 시스템 (eCryptfs / Windows EFS)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 멍청한 엄마(일반 컴퓨터 유저)가 은행 창구 출납 직원에게 100만 원짜리 수표를 맡겼어요. 직원이 수표를 은행 지하 금고([[001_dikw_pyramid|데이터]] 블록 디스크 구이!)에 탁! 던져 넣고 컴퓨터 장부 표에 "입금" 도장을 딱 찍으려는 찰나! 폭풍우 벼락 파단 벼락이 치며 은행 전원이 몽땅 다 나가버렸어요(크래시 셧다운 멸망 에러 랙!).
2. 날이 밝고 컴퓨터(서버 봇)를 켜보니, 금고에는 분명 남는 100만 원 수표 종이가 누워있는데, 누구 장부에도 그런 돈이 들어왔단 기록이 없어요! "주인도 없는 잉여 돈(Orphan 쓰레기 모순!)" 이 발생해 은행 전산이 완전 멈춰([[516_mount_mechanism|마운트]] [[510_lock|Lock]] 랙!) 버렸어요!
3. 그래서 본사에서 무시무시한 **"fsck 결산 탈곡 로봇! 전체 바닥 장부 크로스 체크!([[606_auditing_linux_auditd|감사]] 수술 빔!)"** 이 파견됐어요 록백! 로봇 봇은 무조건 은행 셔터를 내리고 문을 닫아버린 뒤(Offline 오프라인 작업 모순 빔!), 10원짜리부터 장부까지 전체 10만 장 바닥을 샅샅이 다 기어 다니고 스캔(전체 스캔 I/O 속도 저하 부작용 늪!) 하면서 100만 원 주인을 찾아 "주인불명 임시 보관함(lost+found 고아원 스왑 융합!)" 에 억지로 쑤셔 박아 대차 균형을 맞춰 겨우겨우 문을 다시 열어주는 눈물의 [[658_ir_recovery|복구]](무결 재조립 사후 치료!)를 달성했답니다 시스템 생존 구조 랙!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 559 / 800

← **이전**: [[558_proc_sysfs_virtual_filesystem|558. 가상 장치 파일 시스템 (sysfs, procfs) - 커널 변수와 하드웨어 정보 노출 통로]]
**다음**: [[560_multi_stream_file_fork_ads|560. 다중 스트림 (Multi-stream) 파일 / 포크 (Forks) - 데이터 스트림과 리소스 스트림 분리]] →

---
