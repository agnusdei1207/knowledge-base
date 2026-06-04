---
title: "727. 디스크 스케줄링 SCAN 엘리베이터 (Disk Scheduling Scan Elevator)"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SCAN [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 하드디스크([HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/))의 헤드가 마치 <strong>엘리베이터처럼 한쪽 방향으로 끝까지 이동하며 경로상에 있는 모든 I/O 요청을 처리</strong>하고, 끝에 도달하면 방향을 바꿔 반대쪽으로 이동하며 처리하는 [디스크 스케줄링](/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/) 기법이다. (이 때문에 엘리베이터 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로도 불린다.)
> 2. **해결책 (SSTF의 기아 극복)**: 가장 가까운 곳만 찾아가느라 양 끝단의 요청이 영원히 무시당하는 [SSTF](/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/)(Shortest [Seek Time](/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/) First)의 치명적인 약점인 <strong>기아(<a href="/studynote/02_operating_system/05_deadlock/314_starvation_prevention/">Starvation</a>) 현상을 기하학적 룰(일방통행)을 통해 완벽하게 해결</strong>했다.
> 3. **한계**: 양 끝단(0번 실린더, 199번 실린더)에 가까운 트랙일수록 중간 트랙보다 헤드가 방문하는 횟수가 절반으로 줄어들어(불공평성), 위치에 따른 대기 시간의 편차가 발생한다는 태생적인 한계가 있다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/">디스크 스케줄링</a></strong>: 하드디스크의 플래터(원판) 위를 도는 헤드(Head)가, 수많은 프로세스가 쏟아내는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 요청(Cylinder 번호)을 어떤 순서로 처리할지 결정하는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/).
  - <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/">Seek Time</a> (<a href="/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/">탐색 시간</a>)</strong>: 헤드가 원하는 트랙(실린더)으로 징~ 하고 이동하는 데 걸리는 물리적 시간. 디스크 I/O에서 가장 긴 시간(수 밀리초)을 차지하므로 이를 줄이는 것이 핵심이다.
  - **SCAN**: 헤드가 디스크의 한쪽 끝(0번)에서 다른 쪽 끝(199번)까지 이동하며 요청을 다 쳐내고, 끝에 닿으면 다시 199번에서 0번 방향으로 역주행하며 요청을 쳐내는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/).

- **필요성 (SSTF의 잔인성)**:
  - 과거에는 [FCFS](/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/)(먼저 온 순서)를 썼더니 헤드가 디스크 양끝을 미친 듯이 왕복하느라 기계가 박살 날 뻔했다.
  - 그래서 "가장 가까운 곳부터 가자"는 SSTF를 도입했더니, 중간 번호(50번)에서 요청이 계속 쏟아지면, 199번(양 끝단)에서 기다리는 요청은 평생 헤드가 오지 않아 굶어 죽었다([Starvation](/studynote/02_operating_system/05_deadlock/314_starvation_prevention/)).
  - **해결책**: "가장 가까운 곳이 아니라, 무조건 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)하는 방향으로 쭉 밀어붙이자! 엘리베이터처럼 1층에서 10층까지 가면서 중간에 누른 사람들 다 태우고, 10층 찍으면 그때 내려오자!"는 아이디어가 나왔다.

  - <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/">SSTF</a> (이기적인 택시기사)</strong>: 강남역에 서 있는데, 교대역(가까움) 콜이 오면 가고, 또 강남역 콜이 오면 돌아간다. 부산(멀리)에서 부른 콜은 평생 무시한다.
  - **SCAN (엘리베이터)**: 1층에서 10층으로 올라가는 엘리베이터. 3층, 5층에서 누르면 태우고 간다. 만약 내가 4층인데 엘리베이터가 방금 5층으로 지나쳐 올라갔다면? 엘리베이터가 10층을 찍고 다시 내려올 때까지 무조건 기다려야 한다.

- **발전 과정**:
  1. <strong><a href="/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/">FCFS</a></strong>: 멍청함. 물리적 이동 거리 최악.
  2. <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/">SSTF</a></strong>: 똑똑하지만 양 끝단 기아([Starvation](/studynote/02_operating_system/05_deadlock/314_starvation_prevention/)) 발생.
  3. **SCAN**: 엘리베이터 방식. 기아는 없앴으나 양 끝단이 차별받음.
  4. <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/">C-SCAN</a></strong>: 차별마저 없앤 원형 엘리베이터 (현대 [디스크 스케줄링](/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/)의 근간).

- **📢 섹션 요약 비유**: 청소부가 방을 닦을 때, 눈앞에 보이는 먼지([SSTF](/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/))만 계속 쫓아다니면 방구석은 영원히 안 닦입니다. SCAN은 걸레를 들고 왼쪽 벽에서 오른쪽 벽까지 쭉 밀고 가며(Sweep) 한 번에 청소하는, 가장 체력([탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/))을 아끼는 완벽한 물리적 최적화입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### SCAN [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 시뮬레이션

디스크 실린더가 0번부터 199번까지 있다.
현재 헤드 위치: **50번 ([진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 방향: 우측 $\rightarrow$ 199번 방향)**
요청 큐: `[98, 183, 37, 122, 14, 124, 65, 67]`

```text
  +-------------------------------------------------------------------+
  |                 SCAN (엘리베이터) 알고리즘 이동 궤적 시뮬레이션         |
  +-------------------------------------------------------------------+
  |                                                                   |
  |  [ 헤드 이동 방향: 50 ---> 199 ]                                     |
  |                                                                   |
  |   1. 현재 위치: 50                                                  |
  |   2. 50보다 큰 요청들을 오름차순으로 스윕(Sweep)하며 처리!                |
  |      50 ---> 65 ---> 67 ---> 98 ---> 122 ---> 124 ---> 183             |
  |   3. 183을 처리하고 나서 더 이상 우측 요청이 없더라도,                       |
  |      **디스크의 끝(199)까지 무식하게 계속 직진함!!** (이것이 SCAN의 특징)    |
  |      183 ---> 199 (끝점 도달)                                         |
  |                                                                   |
  |  [ 199 도착! 이제 방향을 튼다: 199 ---> 0 ]                           |
  |                                                                   |
  |   4. 199에서 왼쪽으로 가면서 남은 요청(50보다 작았던 것들)을 처리!          |
  |      199 ---> 37 ---> 14 (처리 완료)                                 |
  |                                                                   |
  |  ★ 총 이동 거리 (Total Head Movement):                              |
  |     (199 - 50) + (199 - 14) = 149 + 185 = **334 실린더**           |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** SCAN은 자비가 없다. 헤드가 183번 요청을 처리했다고 돌아오지 않는다. 자기가 가던 방향의 '물리적인 끝(199번)'을 찍고(Touch) 나서야 비로소 후진 기어를 넣는다. 이 무식한 직진 본능 때문에 구현이 매우 단순해지고, 뒤에서 기다리던 14번 요청도 '언젠가는 100% 처리됨'이 수학적으로 완벽히 보장(기아 방지)된다.

---

### LOOK [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) (SCAN의 똑똑한 변형)

SCAN의 "끝까지 무조건 간다"는 점을 보완한 것이 <strong>LOOK <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>이다.
- **LOOK**: 엘리베이터가 올라가다가, 꼭대기 10층에 누른 사람이 없으면 굳이 10층까지 안 가고, 8층(마지막 요청)에서 바로 방향을 꺾어 내려온다.
- 위 시뮬레이션에서 199번까지 안 가고 `183`에서 바로 `37`로 꺾기 때문에 불필요한 공회전(Overhead)이 줄어들어, 현실의 OS는 SCAN보다 LOOK을 훨씬 많이 쓴다.

- **📢 섹션 요약 비유**: SCAN은 종점까지 무조건 운행하는 시내버스고, LOOK은 승객이 다 내리면 중간에서 그냥 차를 돌려버리는 약삭빠른 시골 버스입니다. 당연히 LOOK이 기름(이동 시간)을 덜 먹습니다.

---

## Ⅲ. 비교 및 연결

### [디스크 스케줄링](/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/) 3대장 비교

| [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 이동 원칙 | 장점 | 단점 |
|:---|:---|:---|:---|
| <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/">SSTF</a></strong> (Shortest Seek) | 무조건 현재 위치에서 가장 가까운 곳 | 평균 [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/)([Seek Time](/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/)) 최소화 | 멀리 있는 요청은 영원히 처리 안 됨 (<strong><a href="/studynote/02_operating_system/05_deadlock/314_starvation_prevention/">Starvation</a></strong>) |
| **SCAN** (Elevator) | 방향을 정해 끝까지 밀고 튕겨 나옴 | <strong>기아(<a href="/studynote/02_operating_system/05_deadlock/314_starvation_prevention/">Starvation</a>) 원천 차단</strong> | 양 끝단 트랙은 가운데보다 방문 횟수가 적어 억울함 |
| <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/">C-SCAN</a></strong> (Circular) | 끝까지 갔다가, 반대쪽 끝으로 휙 날아와서 [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/)으로만 훓음 | **모든 트랙에 대한 완벽한 공평성(대기시간 균일)**| 끝에서 끝으로 날아갈 때(Return) 낭비 발생 |

### SCAN [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 "불공평성(Unfairness)" 문제 (C-SCAN이 태어난 이유)

왜 양 끝단이 억울할까?
- 중간(50번) 트랙: 헤드가 `0 -> 100` 갈 때 1번 방문하고, `100 -> 0` 올 때 또 1번 방문한다. 즉, **주기가 짧다**.
- 끝단(0번) 트랙: 헤드가 `0`을 찍고 `100`으로 떠나버리면, `100` 찍고 다시 `0`으로 돌아올 때까지 가장 기나긴 왕복 시간을 꼬박 기다려야 한다.
- **결론**: SCAN은 가운데 위치한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)일수록 평균 대기 시간이 짧고, 가장자리에 있을수록 대기 시간이 미친 듯이 길어지는 <strong>위치 차별(<a href="/studynote/08_algorithm_stats/08_stats/136_variance/">Variance</a> of wait time)</strong>이 존재한다.

- **📢 섹션 요약 비유**: 동네 한가운데(50번) 사는 친구는 왕복하는 셔틀버스를 자주 탈 수 있지만, 동네 구석 끝(0번)에 사는 친구는 셔틀버스가 한 번 떠나면 다시 돌아올 때까지 하루 종일 기다려야 하는 지리적 소외를 겪게 됩니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — <a href="/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/">HDD</a> 시대의 극악한 I/O 병목 방어 (I/O Scheduler 튜닝)</strong>: 리눅스 서버에 MySQL을 올리고 하드디스크([HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/)) 10개를 RAID로 묶어 서비스하던 시절. 동시 접속자가 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000명 몰리면 디스크 드르륵 소리가 나면서 Load Average가 100을 뚫었다.
   - **원인 분석**: 디스크 암(Arm)의 물리적 이동 속도는 1초에 100번 내외(100 IOPS)가 한계다. OS가 요청 들어온 순서대로([FCFS](/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/)) 디스크에 명령을 밀어 넣으면, 암이 플래터 위를 미친 듯이 와이퍼처럼 흔들리다가 헤드가 박살 나거나 응답 지연이 수 초 단위로 터진다.
   - **아키텍처 적용**: 리눅스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 블록 I/O 스케줄러를 `deadline`이나 `cfq`에서 <strong><code>anticipatory</code></strong>나 <strong><code>noop</code></strong> 튜닝을 통해 큐에 패킷을 모아두었다가 <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/">C-SCAN</a> (또는 C-LOOK)</strong> 방식으로 쫙 정렬(Sorting)해서 하드웨어로 내려보낸다. 이렇게 하면 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000개의 쿼리가 10번의 왕복(Sweep)만으로 모두 처리되어, 100 IOPS짜리 고철 디스크가 1,000 TPS를 쳐내는 기적의 인프라 튜닝이 완성된다.

2. <strong>시나리오 — <a href="/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/">NVMe</a> SSD의 시대: <a href="/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/">디스크 스케줄링</a>의 종말</strong>: 최신 클라우드 인프라에서 수천만 원짜리 [NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) SSD를 달았다. 서버 엔지니어가 과거의 영광을 잊지 못하고 리눅스 I/O 스케줄러를 `CFQ(SCAN 기반)`로 열심히 튜닝했다. 그런데 성능이 더 떨어졌다.
   - **원인 분석**: **SSD에는 물리적으로 움직이는 헤드(Head)나 원판(Platter)이 존재하지 않는다.** [플래시 메모리](/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/) 셀에 전기로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 꽂아 넣기 때문에, 0번지를 읽든 199번지를 읽든 [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/)([Seek Time](/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/))이 무조건 **0초($O(1)$)**다.
   - **기술사적 판단**: 이런 환경에서 OS가 "엘리베이터처럼 정렬해서 줘야지~" 하고 SCAN [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 CPU를 태워가며 큐를 정렬(Sorting)하는 것은 아무 쓸모 없는 멍청한 오버헤드다. 따라서 현대 리눅스는 SSD가 꽂히면 무조건 I/O 스케줄러를 <strong><code>none</code> (과거의 <code>noop</code>, 선입선출 <a href="/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/">FCFS</a> 기반)</strong>으로 설정하여, 들어오는 즉시 튜닝 없이 SSD의 컨트롤러로 직행시켜버리는 것이 정답이다 ([NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) Multi-queue 아키텍처).

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 물리적 저장 매체에 따른 I/O 스케줄러(알고리즘) 선택        |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [새로운 서버나 DB 인스턴스의 디스크 스케줄러(sysfs) 설정]                |
  |                |                                                  |
  |                v                                                  |
  |      저장 장치가 회전하는 플래터와 헤드를 가진 HDD (Hard Disk) 인가?         |
  |          +- 예 ------> [이동 거리 최소화 알고리즘 (C-SCAN 등) 필수]     |
  |          |            대책: `mq-deadline` 이나 `bfq` 스케줄러를 선택하여 |
  |          |                  커널이 큐를 정렬(Elevator)하고 병합(Merge)하게 |
  |          |                  만들어 물리적 탐색 시간(Seek Time)을 극한으로 방어|
  |          +- 아니오 (SSD, NVMe, USB 메모리 등 낸드 플래시 기반이다)       |
  |                |                                                  |
  |                v                                                  |
  |      [스케줄러 오버헤드 박살 내기 (Bypass)]                             |
  |      - 대책: 스케줄러를 `none` 또는 `kyber` (단순 통제용)로 세팅.          |
  |      - SSD는 무작위 접근(Random Access) 속도가 순차 접근과 똑같으므로,       |
  |        OS는 정렬 따위 신경 끄고 최대한 많은 큐(Multi-queue)를 뚫어서        |
  |        비동기로 마구 쏟아붓는 것이 압도적으로 빠르다.                       |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** "[디스크 스케줄링](/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/)(SCAN)은 구시대의 유물인가?" 절반만 맞다. 낸드 플래시 시대에 OS 단의 엘리베이터 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 버려졌지만, 이 웅장한 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 거대한 <strong>테이프 <a href="/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/">백업</a>(LTO) 아카이빙 로봇</strong>이나, 하드웨어 <strong><a href="/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/">SSD</a> 컨트롤러 칩셋 내부의 <a href="/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/">FTL</a>(<a href="/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/">Flash Translation Layer</a>) 웨어 레벨링 로직</strong>으로 숨어 들어가 여전히 1초에 수억 번씩 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 정렬하며 살아 숨 쉬고 있다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong>NCQ (Native <a href="/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/">Command</a> Queuing)</strong>: [SATA](/studynote/01_computer_architecture/08_io_storage_systems/341_sata/) 시절부터 도입된 이 기술은, OS가 스케줄링을 대충 해서 디스크에 던져도([FCFS](/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/)), <strong>"디스크 하드웨어 컨트롤러(<a href="/studynote/02_operating_system/01_overview_architecture/032_firmware/">펌웨어</a>)" 자체가 스스로 큐를 분석해 엘리베이터(LOOK) <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a>으로 헤드 궤적을 실시간으로 재정렬</strong>해 버리는 마법이다. OS 튜닝보다 하드웨어 NCQ 활성화가 [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 성능에 100배 더 중요함을 이해하고 있는가?

- **📢 섹션 요약 비유**: 택배 기사(디스크 헤드)가 길을 모를 때는 회사(OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))에서 완벽한 최적화 동선(SCAN)을 짜서 종이로 줘야만 했습니다. 하지만 요즘 택배 기사([SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/), NCQ)는 날아다니는 아이언맨이거나 자체 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 내비게이션을 들고 있어서, 회사는 동선 짜느라 머리 아파하지 말고 그냥 물건([FCFS](/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/))만 냅다 던져주는 게 훨씬 빠릅니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [SSTF](/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/) (이기적 최단 거리) | SCAN (엘리베이터) | 개선 효과 |
|:---|:---|:---|:---|
| **정성 (공평성/기아)**| 멀리 있는 요청은 영구적 기아([Starvation](/studynote/02_operating_system/05_deadlock/314_starvation_prevention/)) | **끝까지 밀고 가므로 기아 100% 방지**| 응답 시간의 상한선(Upper Bound) 보장 |
| <strong>정량 (<a href="/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/">탐색 시간</a>)</strong> | 가장 짧음 (이론적 최적에 근접) | 약간 길어지지만 매우 우수함 | 물리적 기계 마모 감소 및 안정적 I/O |
| **정성 (대기 시간 편차)**| 극도로 심함 (복불복) | **가운데가 빠르고 양끝이 느림 (한계)**| 예측 가능한 레이턴시 범위 제공 (C-SCAN으로 진화) |

### 미래 전망
- <strong>Key-Value 스토리지 전용 인터페이스 (KV-<a href="/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/">SSD</a>)</strong>: 블록(실린더, 섹터) 단위로 디스크를 쪼개고 OS가 스케줄링하던 낡은 블록 스토리지 개념을 버리고, 아예 앱이 "이 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장해"라고 던지면 [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 컨트롤러가 알아서 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 저장하는 객체 기반 스토리지([Object Storage](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)) 하드웨어가 클라우드 벤더(AWS 등)를 중심으로 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 스토리지의 미래를 재편하고 있다.

### 결론
SCAN (엘리베이터) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 인간의 일상적인 발명품(엘리베이터)이 컴퓨터의 가장 깊숙한 하드웨어 최적화 로직으로 완벽하게 이식된 컴퓨터 과학의 낭만적인 사례다. "가장 가까운 이익([SSTF](/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/))만 쫓다가는 누군가 영원히 소외(기아)된다. 조금 돌아가고 비효율적이더라도, 정해진 궤도를 묵묵히 완주(SCAN)하는 것이 결국 전체 시스템을 가장 평화롭고 안정적으로 이끄는 길이다"라는 철학은 비단 디스크 헤드의 궤적뿐만 아니라, 모든 시스템 스케줄링이 지향해야 할 거시적 안목을 웅변한다. 비록 플래터와 헤드의 물리적 시대는 저물고 있지만, 엘리베이터의 묵직한 오름과 내림의 궤적은 영원한 고전으로 남을 것이다.

- **📢 섹션 요약 비유**: 엘리베이터(SCAN)는 내가 탄 층에서 문을 닫고 목적지로 가는 도중에, 다른 층에서 버튼을 누르면 멈춰서 그 사람을 태워줍니다. 직행([SSTF](/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/))보다 내 도착 시간은 몇 초 늦어지겠지만, 건물 전체의 모든 사람이 화내지 않고 목적지에 도착하게 만드는 위대한 발명품입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/) ([Thrashing](/studynote/02_operating_system/04_synchronization/257_thrashing/)) CPU 이용률 저하 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) ([Working Set](/studynote/02_operating_system/04_synchronization/265_working_set/)) 메모리 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/) [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 회전 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [SSTF](/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/) 기아 현상 ([가운데 편중](/studynote/02_operating_system/11_exam_summary/729_sstf_starvation_middle_bias/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[워킹 셋 (Working Set) 메모리]
    |
    v
[디스크 스케줄링 SCAN 엘리베이터 (Disk Scheduling Scan Elevator)]
    |
    +---> [C-SCAN 단방향 회전]
    +---> [SSTF 기아 현상 (가운데 편중)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 넓은 운동장에 쓰레기가 100개 흩어져 있어요. 철수는 쓰레기를 주울 때 "지금 서 있는 곳에서 제일 가까운 쓰레기"만 계속 찾아다녔어요 ([SSTF](/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/)).
2. 그랬더니 철수는 운동장 한가운데서만 맴돌고, 운동장 구석에 있는 쓰레기는 밤이 될 때까지 영원히 안 주웠답니다 (기아 현상 발생).
3. 빗자루 차(SCAN)가 출동했어요! 빗자루 차는 가까운 걸 찾는 게 아니라, 벽 끝에서부터 반대쪽 벽 끝까지 똑바로 쭈우욱~ 전진하면서 눈에 걸리는 쓰레기를 한 번에 싹 다 밀어버려요! 구석 쓰레기도 절대 놓치지 않는 엘리베이터 같은 완벽한 청소법이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 727 / 800

<- **이전**: [726. 워킹 셋 (Working Set) 메모리](/studynote/02_operating_system/11_exam_summary/726_working_set_memory_locality/)
**다음**: [728. C-SCAN 단방향 회전 (C Scan Circular Elevator)](/studynote/02_operating_system/11_exam_summary/728_c_scan_circular_elevator/) ->

---
