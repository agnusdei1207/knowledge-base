---
title: "C Scan Circular Elevator"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/)([Circular SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/))은 디스크 헤드가 엘리베이터처럼 왕복하는 SCAN [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 치명적 단점인 <strong>'양 끝단 트랙의 대기 시간 차별'을 완벽하게 해결하기 위해 고안된 <a href="/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/">단방향</a>(Circular) <a href="/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/">디스크 스케줄링</a> 기법</strong>이다.
> 2. **메커니즘**: 헤드는 디스크의 한쪽 끝에서 다른 쪽 끝으로 전진하며 모든 I/O 요청을 처리한다. 끝에 도달하면 방향을 바꿔 역주행(Reverse)하며 처리하는 것이 아니라, <strong>반대쪽 끝으로 빛의 속도로 휙 날아간 뒤(처리 없이 복귀) 다시 똑같은 방향으로만 전진</strong>하며 처리한다.
> 3. **가치**: 반대쪽으로 날아갈 때 발생하는 기계적 복귀 시간(Return Time)이라는 페널티를 감수하더라도, 모든 실린더 위치에 대해 <strong>가장 균일하고 예측 가능한 대기 시간(<a href="/studynote/08_algorithm_stats/08_stats/136_variance/">Variance</a> of Wait Time = 0에 수렴)</strong>을 보장하여 현대 자기 디스크([HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/)) 스케줄링의 표준 뼈대가 되었다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/">C-SCAN</a> (<a href="/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/">Circular SCAN</a>)</strong>: 디스크 암(Arm)이 항상 0번에서 199번 한쪽 방향으로만 움직이며 요청을 처리하고, 199번에 도달하면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 처리하지 않고 곧바로 0번으로 복귀하여 다시 0번부터 처리를 시작하는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/). 마치 디스크가 끝과 끝이 연결된 원형(Circular)인 것처럼 다룬다.

- **필요성 (SCAN의 불공평성 극복)**:
  - SCAN [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)(엘리베이터)은 10층을 찍고 내려가면서 9층, 8층 사람을 바로 태운다.
  - 1층에 있는 사람은 엘리베이터가 10층을 찍고 내려와서 2층까지 다 태운 뒤에야 탈 수 있다(가장 오래 기다림).
  - 즉, 가운데 트랙은 빗자루가 자주 지나가서 금방 처리되지만, 양 끝단 트랙은 빗자루가 한 번 떠나면 다시 올 때까지 시스템에서 가장 긴 대기 시간을 견뎌야 하는 <strong>지리적 차별(불공평성)</strong>이 존재했다.
  - **해결책**: "내려갈 땐 아무도 태우지 말고 그냥 1층으로 뚝 떨어지자! 그리고 무조건 올라갈 때만 태우자!" 이렇게 하면 모든 층의 사람이 1층에서 10층으로 가는 똑같은 주기(Cycle)마다 한 번씩 공평하게 탈 수 있다.

  - **SCAN (양방향 제설차)**: 골목길을 왼쪽에서 오른쪽으로 쓸고 간 뒤, 오른쪽 끝에서 바로 왼쪽으로 다시 쓸면서 온다. 오른쪽 끝에 사는 사람은 방금 눈을 치웠는데 또 치워주는 반면, 왼쪽 끝에 사는 사람은 제설차가 왕복할 때까지 하루 종일 기다려야 한다.
  - <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/">C-SCAN</a> (<a href="/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/">단방향</a> 제설차)</strong>: 골목길을 왼쪽에서 오른쪽으로 싹 쓸고 나면, 빗자루를 위로 번쩍 들고(처리 안 함) 빛의 속도로 왼쪽 끝으로 돌아간다. 그리고 다시 왼쪽에서 오른쪽으로 쓴다. 모든 집이 똑같은 시간 간격으로 눈을 치우게 된다.

- **발전 과정**:
  1. <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/">SSTF</a></strong>: 가까운 놈만 챙겨서 기아([Starvation](/studynote/02_operating_system/05_deadlock/314_starvation_prevention/)) 발생.
  2. **SCAN**: 기아는 막았으나 양 끝단이 차별받음.
  3. <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/">C-SCAN</a></strong>: 한쪽으로만 쓸어버려서 차별마저 없앰. 대기 시간 편차 최소화.
  4. **C-LOOK**: C-SCAN에서 끝(199번)까지 가지 않고 마지막 요청에서 턴(Turn)하는 실용적 최적화.

- **📢 섹션 요약 비유**: LP판의 바늘을 생각하면 됩니다. 1번 트랙부터 끝 트랙까지 노래를 다 들었으면, 바늘을 징~ 하고 거꾸로 긁으면서(SCAN) 노래를 거꾸로 듣는 게 아니라, 바늘을 번쩍 들어 올려서 다시 1번 트랙으로 휙 돌려놓는 것([C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/))이 정상적인 오디오 재생법입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 시뮬레이션

디스크 실린더가 0번부터 199번까지 있다.
현재 헤드 위치: **50번 ([진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 방향: 우측 $\rightarrow$ 199번 방향)**
요청 큐: `[98, 183, 37, 122, 14, 124, 65, 67]`

```text
  +-------------------------------------------------------------------+
  |                 C-SCAN (단방향 회전) 알고리즘 이동 궤적 시뮬레이션       |
  +-------------------------------------------------------------------+
  |                                                                   |
  |  [ 헤드 이동 방향: 무조건 우측(0 ---> 199)으로만 처리함! ]                |
  |                                                                   |
  |   1. 현재 위치: 50                                                  |
  |   2. 50보다 큰 요청들을 오름차순으로 스윕(Sweep)하며 처리!                |
  |      50 ---> 65 ---> 67 ---> 98 ---> 122 ---> 124 ---> 183             |
  |   3. SCAN과 마찬가지로 디스크의 끝(199)까지 계속 직진함.                  |
  |      183 ---> 199 (끝점 도달)                                         |
  |                                                                   |
  |  [ 199 도착! 역주행 처리 금지! 빛의 속도로 0번으로 복귀(Return) ]          |
  |                                                                   |
  |   4. 199에서 **아무것도 처리하지 않고** 0번 실린더로 점프!                  |
  |      199 ---> 0  (이동 거리: 199)                                    |
  |                                                                   |
  |  [ 0 도착! 다시 우측으로 가면서 남은 요청을 처리 ]                       |
  |                                                                   |
  |   5. 0 ---> 14 ---> 37 (처리 완료)                                   |
  |                                                                   |
  |  ★ 총 이동 거리 (Total Head Movement):                              |
  |     (199 - 50) + (199 - 0) + (37 - 0) = 149 + 199 + 37 = **385** |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** C-SCAN의 총 이동 거리(385)는 일반 SCAN의 이동 거리(334)보다 훨씬 길다. 왜냐하면 199번에서 0번으로 "허공을 가르며 날아오는 시간(Return Time)"이 추가되었기 때문이다. 하지만 [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 헤드가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽고 쓰면서 천천히 이동하는 속도에 비해, 그냥 빈 공간을 휙 하고 날아가는 복귀 속도는 하드웨어적으로 훨씬 빠르다. 즉, <strong>"약간의 이동 거리를 손해 보더라도, 모든 프로세스가 균등한 시간에 I/O를 보장받게 만들겠다"</strong>는 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 강력한 공정성(Fairness) 철학이 반영된 것이다.

---

### C-LOOK [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) (C-SCAN의 완성형)

[C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/) 역시 "무조건 끝(199)과 끝(0)을 찍어야 한다"는 멍청한 규칙이 있다. 183이 마지막인데 왜 199까지 가야 하는가?

- **C-LOOK**: 우측으로 가다가 `183`에서 요청이 끝나면 199까지 안 가고 멈춘다. 그리고 `0`으로 날아가는 게 아니라, 반대쪽에서 가장 작은 요청인 `14`번으로 바로 날아간다.
- **결과**: 공평성([Variance](/studynote/08_algorithm_stats/08_stats/136_variance/) = 0)은 그대로 유지하면서, 쓸데없이 디스크 끝까지 가는 공회전 오버헤드를 완벽하게 잘라냈다. 오늘날 HDD의 [펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/)(NCQ)나 리눅스의 `Deadline` 기반 [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 사용하는 내부 로직의 근간이다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 대기 시간 편차 ([Variance](/studynote/08_algorithm_stats/08_stats/136_variance/) of Wait Time) 비교

C-SCAN의 존재 이유는 오직 이 '편차([분산](/studynote/08_algorithm_stats/08_stats/136_variance/))'를 죽이기 위함이다.

| [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 평균 대기 시간 (Mean) | 대기 시간 편차 ([Variance](/studynote/08_algorithm_stats/08_stats/136_variance/)) | 공평성 평가 |
|:---|:---|:---|:---|
| <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/">SSTF</a></strong> | 매우 짧음 (가장 우수) | **극도로 높음 (누구는 1초, 누구는 1시간)** | 0점 (기아 발생) |
| **SCAN** | 짧음 | **높음 (가운데 트랙은 2번씩 혜택, 양끝은 소외됨)** | 50점 (기아는 없으나 차별 존재) |
| <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/">C-SCAN</a></strong>| 약간 길어짐 (복귀 시간 추가) | **0에 수렴 (모든 트랙이 한 사이클마다 1번씩 공평하게 기회를 얻음)** | **100점 (완벽한 공평성)** |

### 과목 융합 관점

- <strong>컴퓨터구조 (<a href="/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/">CA</a>) / 디스크 물리학</strong>: [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 원판(Platter)의 구조를 보면 0번 실린더는 원판의 가장 바깥쪽(Outer)이고, 199번은 가장 안쪽(Inner)이다. 각속도 일정(CAV) 방식이나 선속도 일정(ZBR) 방식 모두, 바깥쪽 트랙이 안쪽 트랙보다 섹터가 더 많아서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 밀도가 높고 전송 속도가 훨씬 빠르다. 따라서 OS는 페이징을 할 때 0번 근처(가장자리)를 가장 많이 쓴다. C-SCAN은 한 바퀴 돌 때마다 이 빠르고 자주 쓰이는 0번 트랙을 무조건 새롭게 시작점으로 잡아주기 때문에 하드웨어 친화적이다.
- **소프트웨어공학 (SE) / UX**: 사용자는 "평균적으로 빠른 앱"보다 <strong>"예측 가능하게 반응하는 앱"</strong>을 좋아한다. C-SCAN은 꼬리 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)(Tail [Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/), P99)을 완벽하게 잘라버린다. 100번 눌러서 99번은 0.1초 만에 켜지지만 1번은 10초 걸리는 앱([SSTF](/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/))보다, 무조건 1초 안에 켜지는 앱([C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/))이 사용자 경험과 [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/)([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 협약)를 만족시키는 엔터프라이즈 아키텍처의 정답이다.

- **📢 섹션 요약 비유**: 평균 점수(Mean)의 함정입니다. 반 평균이 90점인데 100점짜리 9명과 0점짜리 1명([SSTF](/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/))이 있는 반보다, 반 평균이 80점이라도 모두가 80점을 맞은 반([C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/))이 훨씬 더 건강하고 예측 가능한 교실입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — <a href="/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> (RDBMS) 디스크 I/O <a href="/studynote/04_software_engineering/02_requirements_analysis/129_spike_agile_technical_investigation/">스파이크</a> 방어</strong>: [Oracle](/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) DB에서 무거운 `SELECT * (Full Table Scan)` [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)가 돌고 있을 때, 다른 사용자의 가벼운 `UPDATE` [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)들이 응답 불능에 빠졌다.
   - **원인 분석**: 구형 [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)([SSTF](/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/))는 Full Scan을 하느라 헤드가 연속된 특정 실린더 구역(예: 100~120번)에서 옴짝달싹하지 않는다. 이때 10번 트랙에 업데이트를 하려는 가벼운 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)가 들어오면, 헤드가 10번으로 가지 않기 때문에 영원히 락이 걸리며 DB 커넥션 풀이 마비된다 (I/O 기아 현상).
   - <strong>아키텍처 적용 (<a href="/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/">C-SCAN</a> 계열 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/">스케줄러</a>)</strong>: [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 I/O [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)를 [C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/) 방식으로 튜닝(리눅스의 `mq-deadline` 등)해두면, 아무리 100~120번 트랙에 수만 개의 요청이 쏟아져도 헤드는 한 번 120번을 훑고 지나가면 미련 없이 199번을 찍고 0번으로 날아간다. 돌아오는 길에 반드시 10번 트랙의 업데이트를 처리해 주므로, 무거운 스캔 작업 중에도 가벼운 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)들이 무조건 '일정 시간(1 스윕 사이클)' 안에는 응답을 받게 된다.

2. **시나리오 — 실시간 오디오/비디오 스트리밍 서버의 끊김 방지**: 넷플릭스 엣지 서버([HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 시절)에서 1만 명에게 동영상을 쏴주는데, 특정 사용자들의 영상이 5초씩 멈추는 [버퍼링](/studynote/02_operating_system/08_storage_and_io_systems/454_buffering/)(Jitter)이 발생.
   - **원인 분석**: SCAN [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 썼다. 영상 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 디스크 양 끝단에 저장되어 있던 사용자들은, 헤드가 반대쪽으로 갔다가 돌아오는 왕복 시간(Round-trip Time) 내내 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 받지 못해 버퍼가 언더런(Under-run)난 것이다. 중간 트랙 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보는 사람들은 헤드가 자주 지나가서 버퍼가 넘쳐났다.
   - **기술사적 가이드**: 미디어 스트리밍 서버에서는 모든 클라이언트가 <strong>'일정한 주기'</strong>로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 수급받는 것이 생명이다. [C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/)([단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 회전)을 적용하면 헤드가 한 바퀴를 도는 주기가 시스템 전체에 걸쳐 동일해지므로, 버퍼 사이즈를 그 주기에 딱 맞게(예: 1 Sweep 주기 = 1초 분량 버퍼) 계산하여 할당할 수 있게 된다. 끊김 없는 스트리밍 인프라의 숨은 일등 공신이다.

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 HDD 블록 I/O 스케줄러(Elevator) 선택 플로우             |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [베어메탈 서버(하드디스크 탑재)에 대용량 애플리케이션 설치 및 튜닝]            |
  |                |                                                  |
  |                v                                                  |
  |      해당 서버의 워크로드가 극단적인 실시간성(Soft Real-time)을 요구하는가?   |
  |      (예: 오디오 스트리밍, 예측 가능한 응답 시간이 필요한 결제 서버)             |
  |          +- 예 ------> [C-SCAN / C-LOOK 기반의 스케줄러 선택]       |
  |          |            (리눅스 `deadline` 스케줄러: Read 요청에 엄격한    |
  |          |             타임아웃 기한을 두어 C-SCAN 궤적 안에서 기아를 완벽 봉쇄)|
  |          +- 아니오 (전체 백업, 딥러닝 데이터 전처리, 하둡 등)               |
  |                |                                                  |
  |                v                                                  |
  |      전체 시스템의 처리량(Throughput)과 대역폭 극대화가 우선인가?             |
  |          +---> [CFQ (Completely Fair Queuing) 또는 BFQ 스케줄러]     |
  |          |    (프로세스별로 큐를 따로 두고, C-SCAN을 기본으로 하되 프로세스  |
  |          |     우선순위에 따라 I/O 타임 슬라이스를 분배하는 고도화 알고리즘)  |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** C-SCAN은 순수하게 하드웨어의 '[탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/)([Seek Time](/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/))'을 줄이기 위한 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. 하지만 소프트웨어 개발자 입장에서는 "디스크가 얼마나 도는지"보다 "내 앱의 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)가 언제 끝나는지"가 중요하다. 그래서 현대 리눅스는 C-SCAN의 뼈대 위에, 각 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)(BIO)마다 마감 시간([Deadline](/studynote/02_operating_system/11_exam_summary/766_realtime_scheduling_deadline/), 예: Read는 500ms)을 걸어두고 [C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/) 궤적을 그리다 마감 시간이 임박한 놈이 생기면 궤적을 꺾어서라도 먼저 처리해 주는 `mq-deadline`을 엔터프라이즈 DB 서버의 표준으로 삼고 있다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong><a href="/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/">SSD</a> 환경에서의 <a href="/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/">C-SCAN</a> 무용론</strong>: 현재 세팅하는 인스턴스의 디스크 스토리지가 [NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) SSD나 클라우드 EBS인가? 그렇다면 [C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/) 튜닝을 하려고 `sysfs`를 뒤질 필요가 없다. SSD는 원판도 헤드도 없기 때문에 [C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 자체가 CPU만 잡아먹는 잉여 로직이 된다. 무조건 `none`이나 `mq-deadline`의 껍데기만 남긴 상태로 Bypass 시켜야 한다.

- **📢 섹션 요약 비유**: C-SCAN은 훌륭한 지하철 순환선(2호선)입니다. 아무리 멀리 있는 역이라도 1시간(1주기)만 기다리면 무조건 열차가 1번씩 공평하게 옵니다. 예측 불가능한 지옥철([SSTF](/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/))을 예측 가능한 출퇴근 수단으로 탈바꿈시킨 도시 공학의 정수입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | SCAN (양방향 엘리베이터) | [C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/) ([단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 엘리베이터) | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (평균 대기 시간)**| 짧은 편 | 약간 더 김 (Return 시간 낭비) | (트레이드오프) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 살짝 내어주고 평화를 얻음 |
| <strong>정량 (대기 시간 <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>)</strong>| **매우 큼** (가운데는 짧고, 양끝은 김) | **거의 0에 수렴 (모든 위치가 균일함)**| P99 Max [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 시간의 완벽한 컷오프 (Predictability) |
| **정성 (UX)** | 재수 없으면 렉(Lag)이 심하게 걸림 | 어떤 상황에서도 1주기 안에 응답 보장 | 실시간 스트리밍 및 엔터프라이즈 환경 표준 충족 |

### 미래 전망
- <strong>디스크 <a href="/studynote/02_operating_system/01_overview_architecture/032_firmware/">펌웨어</a> 레벨로의 하강 (NCQ/TCQ)</strong>: [C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 더 이상 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(OS)의 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 소스 코드에 존재하지 않는다. WD나 Seagate 같은 하드디스크 제조사들이 아예 [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 칩셋 내부의 [마이크로컨트롤러](/studynote/01_computer_architecture/03_architecture_basics_performance/130_microcontroller/)([펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/)) 안에 이 로직을 하드코딩해 넣었다. OS는 큐 정렬 따위 신경 안 쓰고 그냥 막 던지고, 하드웨어가 스스로 C-LOOK 궤적을 그려서 원판을 긁는 '[오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)([Offloading](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/))' 시대로 완전히 넘어갔다.

### 결론
[C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/)([단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 회전) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 컴퓨터 과학에서 <strong>"최고의 <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>(<a href="/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/">SSTF</a>)이 항상 최고의 시스템을 의미하지는 않는다"</strong>는 것을 증명하는 교과서적인 사례다. 전체 트랙을 이동하고 허공을 가르며 처음으로 복귀하는 낭비(Overhead)를 스스로 짊어짐으로써, 시스템에 존재하는 모든 프로세스에게 "네 위치가 어디든, 차별 없이 똑같은 시간 안에 요청을 처리해 주겠다"는 완벽한 공정성(Fairness)을 선물했다. 불확실성을 예측 가능성으로 바꾼 이 위대한 수학적 합의는, 우리가 대용량 시스템 아키텍처를 설계할 때 무엇을 가장 우선시해야 하는지에 대한 변하지 않는 이정표다.

- **📢 섹션 요약 비유**: 가장 맛있는 피자를 만들기 위해 도우 가운데에만 토핑을 몰아넣는 것([SSTF](/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/), SCAN)은 빵 테두리를 먹는 사람을 불행하게 합니다. 도우 끝에서 끝까지 토핑을 한 방향으로 치우침 없이 골고루 뿌리는 것([C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/))이야말로 셰프([운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))가 갖춰야 할 최고의 장인정신입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) ([Working Set](/studynote/02_operating_system/04_synchronization/265_working_set/)) 메모리 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [디스크 스케줄링](/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/) SCAN 엘리베이터 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [SSTF](/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/) 기아 현상 ([가운데 편중](/studynote/02_operating_system/11_exam_summary/729_sstf_starvation_middle_bias/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [RAID 0](/studynote/02_operating_system/08_storage_and_io_systems/484_raid_0_striping/), 1, 5, 6 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[디스크 스케줄링 SCAN 엘리베이터]
    |
    v
[C-SCAN 단방향 회전 (C Scan Circular Elevator)]
    |
    +---> [SSTF 기아 현상 (가운데 편중)]
    +---> [RAID 0, 1, 5, 6 성능 신뢰성]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 1층부터 10층까지 있는 건물에서 'SCAN 엘리베이터'는 올라갈 때도 태우고, 내려올 때도 태웠어요. 그러니까 중간인 5층 사람들은 하루에 두 번이나 타는데, 1층 사람은 엘리베이터가 한참 뒤에나 돌아와서 화가 났죠.
2. 그래서 '[C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/) 엘리베이터'를 도입했어요! 이 엘리베이터는 무조건 "올라갈 때([단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/))"만 사람을 태워요.
3. 10층에 도착하면 아무도 안 태우고 번지점프를 하듯 1층으로 0.1초 만에 휙! 떨어집니다. 그리고 다시 1층부터 태우면서 올라가요. 덕분에 모든 층 사람들이 완벽하게 똑같은 시간만 기다리면 엘리베이터를 탈 수 있게 되었답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 728 / 800

<- **이전**: [727. 디스크 스케줄링 SCAN 엘리베이터 (Disk Scheduling Scan Elevator)](/studynote/02_operating_system/11_exam_summary/727_disk_scheduling_scan_elevator/)
**다음**: [729. SSTF 기아 현상 (가운데 편중) (Sstf Starvation Middle Bias)](/studynote/02_operating_system/11_exam_summary/729_sstf_starvation_middle_bias/) ->

---
