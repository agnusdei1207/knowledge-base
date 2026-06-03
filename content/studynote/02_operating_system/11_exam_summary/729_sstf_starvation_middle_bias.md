+++
title = "729. SSTF 기아 현상 (가운데 편중) (Sstf Starvation Middle Bias)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/)(Shortest [Seek Time](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/) First)는 디스크 헤드가 현재 위치에서 <strong>"가장 이동 거리(<a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/">Seek Time</a>)가 짧은(가까운) 요청부터 먼저 처리"</strong>하는 극단적 이기주의 스케줄링 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.
> 2. **치명적 문제 (기아 현상)**: 가운데 트랙(예: 50번)에서 요청이 쉴 새 없이 쏟아지면, 헤드는 40~60번 사이만 미친 듯이 맴돌게 된다. 그 결과, 구석(예: 0번, 199번)에서 하염없이 기다리는 요청은 <strong>영원히 헤드가 오지 않아 굶어 죽는 기아(<a href="/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/">Starvation</a>) 상태</strong>에 빠진다.
> 3. <strong>가치/<a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/659_ir_lessons_learned/">교훈</a></strong>: 디스크 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))과 평균 [탐색 시간](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/)에서는 수학적으로 거의 완벽에 가까운 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 내지만, 이 끔찍한 "[응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)의 불공평성" 때문에 현대 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 순수 SSTF를 버리고, 이를 보완한 엘리베이터(SCAN/[C-SCAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/)) 계열의 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 발전하게 되었다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/">SSTF</a> (Shortest <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/">Seek Time</a> First)</strong>: 디스크 큐에 쌓인 요청 중, 현재 헤드 위치에서 물리적으로 가장 가까운(실린더 번호 차이가 가장 적은) 요청을 1순위로 서비스하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/). CPU 스케줄링의 [SJF](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/175_sjf_scheduling/)([Shortest Job First](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/175_sjf_scheduling/))와 완전히 동일한 철학을 갖는다.

- **필요성 (FCFS의 미친 낭비 극복)**: 
  - [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [디스크 스케줄링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/)인 [FCFS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/)(선입선출)는 요청이 들어온 순서대로 헤드를 움직였다. 
  - 1번 $\rightarrow$ 199번 $\rightarrow$ 2번 $\rightarrow$ 198번. 헤드가 자동차 와이퍼처럼 양 끝을 미친 듯이 왕복하느라, [탐색 시간](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/)([Seek Time](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/))에만 수 초가 소모되고 물리적 기계 마모도 심각했다.
  - **해결책**: "어차피 모여있는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)들, 이왕 가는 김에 가까운 애들부터 싹 다 처리하고 넘어가자!"라는 지극히 상식적이고 합리적인 아이디어가 SSTF를 탄생시켰다.

  - <strong><a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/">FCFS</a> (멍청한 택시기사)</strong>: 강남역에 있는데, 첫 번째 콜이 부산에서 왔다고 부산에 갔다가, 두 번째 콜이 다시 강남이라고 강남으로 돌아오는 기사.
  - <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/">SSTF</a> (이기적인 택시기사)</strong>: 강남역에 있다. 콜이 10개 쌓였는데, 9개는 강남역 근처고 1개는 부산이다. 기사는 무조건 강남역 근처의 9명만 계속 태우고 빙빙 돈다. **부산 손님은 밤새도록 택시를 못 탄다 (기아 현상).**

- **발전 과정**:
  1. <strong><a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/">FCFS</a></strong>: 공평하지만 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최악.
  2. <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/">SSTF</a></strong>: [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 최고지만 공평성 최악 (기아 발생).
  3. <strong>SCAN / <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/">C-SCAN</a></strong>: [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 조금 양보하고, 기아를 100% 없앤 절충안.

- **📢 섹션 요약 비유**: 눈앞에 보이는 맛있는 반찬(가까운 트랙)만 편식해서 계속 집어 먹는 아이와 같습니다. 밥그릇(디스크)이 비워지는 속도는 제일 빠르겠지만, 멀리 있는 맛없는 반찬(가장자리 트랙)은 영원히 버려지는 편중 현상이 발생합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/) 이동 궤적 시뮬레이션

디스크 실린더가 0번부터 199번까지 있다. 
현재 헤드 위치: **50번**
요청 큐: `[98, 183, 37, 122, 14, 124, 65, 67]`

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 SSTF 알고리즘 이동 궤적 및 탐색 거리 계산              │
  ├───────────────────────────────────────────────────────────────────┤
  │  [ 현재 위치: 50 ]                                                  │
  │                                                                   │
  │   1. 50에서 제일 가까운 건? -> [37] (거리 13)                        │
  │      50 ──▶ 37                                                    │
  │                                                                   │
  │   2. 37에서 제일 가까운 건? (14 vs 65) -> [14] (거리 23)             │
  │      37 ──▶ 14                                                    │
  │                                                                   │
  │   3. 14에서 제일 가까운 건? -> [65] (거리 51)                        │
  │      14 ──▶ 65                                                    │
  │                                                                   │
  │   4. 65에서 제일 가까운 건? -> [67] (거리 2)                         │
  │      65 ──▶ 67                                                    │
  │                                                                   │
  │   5. 67에서 제일 가까운 건? -> [98] (거리 31)                        │
  │      67 ──▶ 98                                                    │
  │                                                                   │
  │   6. 98 -> 122 -> 124 -> 183 (순차적으로 제일 가까움)                │
  │                                                                   │
  │  ★ 총 이동 거리 (Total Head Movement):                              │
  │     (50 - 14) + (183 - 14) = 36 + 169 = **205 실린더**              │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** FCFS의 총 이동 거리가 640이었던 것에 비하면, SSTF의 205는 무려 <strong>3배나 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>이 향상된 기적의 수치</strong>다. 헤드의 궤적을 보면 50에서 시작해 14로 튕겼다가 다시 183으로 우상향하는 'V자 형태'를 그린다. 전체 이동 거리(평균 [탐색 시간](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/))만 놓고 보면 SSTF를 이길 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 거의 존재하지 않는다.

---

### 가운데 편중과 [Starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/) (기아 현상) 발동 원리

하지만 실무 환경에서 디스크 요청은 한 번에 8개만 들어오는 게 아니라, 1초에 수천 개씩 쏟아진다(Continuous Input).

1. 현재 헤드가 <strong>50번</strong>에 있다.
2. 0번 쪽에 요청 1개가 있고, 40~60번 사이에 요청이 1,000개 쏟아진다.
3. SSTF는 50번 주변의 1,000개를 0.1초 만에 다 쳐낸다. 
4. 이제 0번으로 가려는데, 그 0.1초 사이에 **또다시 40~60번 사이에 1,000개의 요청이 새로 들어왔다.**
5. SSTF는 "어? 또 가까운 곳에 먹을 게 생겼네!" 하면서 0번으로 가지 않고 다시 40~60번 사이만 미친 듯이 왕복한다.
6. **결과**: 양 끝단(0번, 199번)에 있는 요청은 시스템이 종료될 때까지 단 한 번도 헤드를 구경하지 못하고 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)([Timeout](/knowledge-base/studynote/02_operating_system/05_deadlock/319_timeout_prevention/))으로 터져버린다. 이것이 SSTF의 악명 높은 <strong><a href="/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/">Starvation</a>(기아)</strong>이다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### CPU 스케줄링([SJF](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/175_sjf_scheduling/)) vs [디스크 스케줄링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/)([SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/))의 평행이론

두 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 타겟 하드웨어만 다를 뿐, 철학과 부작용이 소름 돋게 일치한다.

| 비교 항목 | CPU 스케줄링: [SJF](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/175_sjf_scheduling/) ([Shortest Job First](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/175_sjf_scheduling/)) | [디스크 스케줄링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/): [SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/) (Shortest [Seek Time](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/) First) |
|:---|:---|:---|
| **최적화 목표** | 평균 대기 시간 (Wait Time) 최소화 | 평균 [탐색 시간](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/) ([Seek Time](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/)) 최소화 |
| **우선순위 척도** | 다음번 CPU 연산(Burst)이 가장 **짧은** 놈 | 현재 위치에서 거리가 가장 **가까운** 놈 |
| **치명적 부작용** | 실행 시간이 **긴** 프로세스의 <strong>기아(<a href="/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/">Starvation</a>)</strong> | 양 **끝단(Edge)** 트랙 요청의 <strong>기아(<a href="/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/">Starvation</a>)</strong> |
| **현대 OS 대안** | [MLFQ](/knowledge-base/studynote/02_operating_system/11_exam_summary/691_mlfq_multi_level_feedback_queue/) ([다단계 피드백 큐](/knowledge-base/studynote/02_operating_system/11_exam_summary/691_mlfq_multi_level_feedback_queue/)), CFS | SCAN, [C-SCAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/) (엘리베이터) |

### 과목 융합 관점

- <strong>자료구조 / <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>: SSTF는 [탐욕 알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/)([Greedy Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/))의 전형이다. 현재 상태에서 가장 이득이 되는 선택(최단 거리)을 하지만, 그것이 글로벌 최적해(전체 이동 거리의 절대적 최소화)를 항상 보장하지는 못하며, 오히려 로컬 옵티마(Local Optima)에 빠져 구석에 있는 노드들을 영원히 탐색하지 못하는 한계를 지닌다.
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> (DB)</strong>: DB의 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 옵티마이저가 인덱스를 탈 때, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 물리적으로 디스크의 한가운데(자주 쓰이는 [핫 데이터](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/675_hot_data_caching/))에 몰려 있으면 [SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/) 하에서 극강의 퍼포먼스를 낸다. 하지만 과거의 아카이브 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([콜드 데이터](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/676_cold_data_archiving/))를 조회하는 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 날리면, SSTF의 편중 현상 때문에 이 콜드 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)는 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)이 터져 영원히 응답받지 못할 수 있다.

- **📢 섹션 요약 비유**: 우버 택시 기사가 매일 강남역(가운데)에서만 맴돌며 1km짜리 기본요금 손님만 100명을 태우는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)([SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/))입니다. 기사의 수입([처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))은 최고지만, 파주(가장자리)에서 콜을 부른 손님은 평생 택시를 타지 못합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — 구형 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 센터에서의 특정 <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> 무한 멈춤(Hang) 사태</strong>: Linux 2.4 이하의 구형 커널을 쓰던 시절, 트래픽이 몰릴 때마다 꼭 밤 12시에 도는 일일 배치(Batch) 프로그램의 DB [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 작업이 10시간 넘게 멈춰버리는 현상.
   - **원인 분석**: 웹 서버의 실시간 트래픽([Hot Data](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/675_hot_data_caching/))은 주로 디스크의 특정 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)(가운데)에 집중되어 있었다. 디스크 스케줄러가 <strong>SSTF와 유사한 최단 거리 우선 로직</strong>으로 동작하고 있었기 때문에, 디스크 헤드는 웹 서버의 실시간 요청만 미친 듯이 쳐내느라, 디스크 맨 끝 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)에 저장된 배치 프로그램의 I/O 요청을 완전히 무시(기아)해 버렸다.
   - **대응 (아키텍처 가이드)**: 기아 현상을 막으려면 <strong>"아무리 멀어도 언젠가는 반드시 간다"</strong>는 보장이 필요하다. 디스크 스케줄러를 무조건 직진하는 `SCAN(Elevator)` [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 교체하여, 헤드가 한 번 스윕(Sweep)할 때 구석에 처박힌 배치 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 I/O도 무조건 한 번은 처리하고 넘어가도록 OS 레벨의 정책을 바꿔야 한다.

2. <strong>시나리오 — <a href="/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/">SSD</a> 환경에서의 <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/">SSTF</a> 부활 (No <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/">Seek Time</a>)</strong>: 최신 AWS EC2 인스턴스에 [NVMe](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) SSD를 달았다. 
   - **기술사적 반전**: SSTF의 기아 현상은 헤드가 플래터의 '물리적인 위치'를 이동할 때 생기는 문제다. 그런데 **SSD는 물리적으로 움직이는 헤드가 없다.**
   - 50번 셀을 읽든, 구석에 있는 199번 셀을 읽든 전자 신호가 도달하는 시간은 똑같이 0.1ms로 동일하다. 즉, [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 환경에서는 <strong>"누가 더 가깝냐"는 물리적 거리의 개념(<a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/">Seek Time</a>) 자체가 완전히 증발</strong>한다.
   - 따라서 [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 컨트롤러 내부에서는 OS가 굳이 SCAN으로 궤적을 예쁘게 정렬해주지 않아도, FCFS나 [SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/)(논리적 최적화) 형태의 매우 단순한 큐잉을 통해 비동기로 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리(Multi-[queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/))하는 방식으로 기술의 역행(회귀)이 일어나고 있다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 I/O 대기 시간의 분산(Variance) 통제 아키텍처 플로우       │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [디스크 읽기/쓰기의 응답 시간(Latency) 불균형이 매우 심한 서버 환경]          │
  │                │                                                  │
  │                ▼                                                  │
  │      전체 시스템의 절대적인 처리량(Throughput) 극대화만이 유일한 목표인가?      │
  │          ├─ 예 ─────▶ [SSTF 류의 최적화 (가운데 편중 용인) 선택]       │
  │          │            (로그를 무작위로 쑤셔 박는 서버 등, 일부 쿼리가 10초씩 │
  │          │             지연되어도 전체 건수만 많으면 장땡인 시스템)          │
  │          └─ 아니오 (특정 유저의 쿼리가 타임아웃 나는 것을 절대 막아야 함)     │
  │                │                                                  │
  │                ▼                                                  │
  │      응답 시간의 예측 가능성(Predictability)과 기아 방지가 우선인가?         │
  │          ├──▶ [C-SCAN / Deadline 스케줄러 도입 필수]                  │
  │          │    - 억울한 놈이 없도록, 가장자리 트랙에도 무조건 주기적으로 헤드를 │
  │          │      강제 배차하여 P99.9의 꼬리 지연(Tail Latency)을 방어함.    │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 초보자는 "무조건 빠른 게 최고다"라며 SSTF의 짧은 이동 거리에 환호한다. 시니어 아키텍트는 "100명 중 99명이 0.1초 만에 응답받고 1명이 10초 만에 응답받는 시스템([SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/))"보다, <strong>"100명 모두가 1초 만에 응답받는 시스템(<a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/">C-SCAN</a>)"</strong>을 더 훌륭한 시스템으로 평가한다. 시스템의 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)은 최고 속도가 아니라 최악의 속도(Worst-case)에 의해 결정되기 때문이다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/">VFS</a> 계층의 <a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/">에이징</a>(<a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/182_aging/">Aging</a>)</strong>: 스케줄러가 SSTF의 속도적 이점을 포기하지 못하겠다면, 구석에서 오래 대기한 요청의 우선순위를 강제로 높여주는([Aging](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/182_aging/)) [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 큐가 결합되어 있는가? (리눅스의 `mq-deadline` 스케줄러가 정확히 이 역할을 수행한다. SSTF로 최단 거리를 돌되, Read 요청이 500ms 이상 큐에서 썩으면 거리를 무시하고 무조건 1순위로 쳐낸다.)

- **📢 섹션 요약 비유**: SSTF는 평균 배송 시간을 줄이겠다고 서울(가운데) 배송만 미친 듯이 하고 제주도(가장자리) 배송은 기약 없이 미루는 악덕 택배사입니다. 고객 불만(에러)을 막으려면, 며칠이 지나면 손해를 보더라도 반드시 제주도행 트럭([Aging](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/182_aging/), [Deadline](/knowledge-base/studynote/02_operating_system/11_exam_summary/766_realtime_scheduling_deadline/))을 띄워야만 합니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [FCFS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/) (무지성) | [SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/) (이기적 최적화) | SCAN/[C-SCAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/) (대안) |
|:---|:---|:---|:---|
| <strong>정량 (<a href="/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/">탐색 시간</a>)</strong> | 최악 (디스크 양끝 왕복) | **최상 (이동 거리 극소화)** | 우수 (직진 궤적 유지) |
| **정성 (기아 현상)** | 발생 안 함 | **발생 (가운데 트랙 편중)** | 발생 안 함 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/">응답 시간</a> <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a></strong> | 낮음 | **매우 높음 (복불복 심함)** | 낮음 (예측 가능) |

### 미래 전망
- **객체 스토리지와 지능형 디스크**: 앞서 말했듯 [HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 시대의 유물인 실린더(Cylinder) 기반의 탐색은 점차 클라우드의 S3 같은 객체 스토리지나 플래시 메모리에 자리를 내어주고 있다. 물리적인 바늘(헤드)의 궤적을 튜닝하던 OS의 책무는, 이제 네트워크 대역폭과 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 큐([Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/))를 관리하는 I/O [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)([io_uring](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/464_io_uring/))로 완전히 패러다임이 시프트 되었다.

### 결론
[SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/)(Shortest [Seek Time](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/) First)는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 가장 맹목적인 탐욕(Greedy)이 시스템의 공정성을 어떻게 파괴하는지를 보여주는 가장 완벽한 교보재다. 전체 이동 거리(평균)를 줄였다는 달콤한 착시 뒤에는, 양 끝단에 갇혀 영원히 실행되지 못하는 프로세스들의 비명이 숨겨져 있었다. [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 이 잔인한 기아 현상을 해결하기 위해 엘리베이터(SCAN)라는 기계적이고 우직한 직진 궤도를 발명해야만 했다. 효율성을 추구하되, 시스템의 단 하나의 요소도 벼랑 끝([Starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/))으로 내몰지 않는 것, 그것이 바로 컴퓨터 공학이 추구하는 진정한 조화(Harmony)의 예술이다.

- **📢 섹션 요약 비유**: 앞만 보고 가장 가까운 과녁만 쏘아 맞히는 명사수([SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/))는 점수는 높을지언정 전장을 구하지 못합니다. 진짜 훌륭한 장군([운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))은 조금 느리더라도 전선 끝에서 끝까지(SCAN) 모든 적을 훑어내며 소외된 아군([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 없도록 챙기는 사람입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [디스크 스케줄링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/) SCAN 엘리베이터 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [C-SCAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/) [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 회전 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [RAID 0](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/484_raid_0_striping/), 1, 5, 6 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [SSD FTL](/knowledge-base/studynote/02_operating_system/11_exam_summary/731_ssd_ftl_flash_translation_layer/) ([Flash Translation Layer](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[C-SCAN 단방향 회전]
    │
    ▼
[SSTF 기아 현상 (가운데 편중) (Sstf Starvation Middle Bias)]
    │
    ├──▶ [RAID 0, 1, 5, 6 성능 신뢰성]
    └──▶ [SSD FTL (Flash Translation Layer)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 철수는 심부름을 할 때 무조건 <strong>"지금 내가 있는 곳에서 제일 가까운 심부름(<a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/">SSTF</a>)"</strong>만 먼저 하기로 했어요.
2. 거실에 있는데, 계속 거실(가운데 트랙)에서만 동생이 심부름을 시켰어요. 철수는 거실에서만 100번 넘게 심부름을 했죠.
3. 그런데 저기 멀리 화장실(가장자리 트랙)에 있던 아빠는, 철수가 화장실 근처로 아예 오질 않아서 하루 종일 수건을 못 받고 갇혀 있어야 했답니다! 이걸 '기아 현상'이라고 불러요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 729 / 800

← **이전**: [728. C-SCAN 단방향 회전 (C Scan Circular Elevator)](/knowledge-base/studynote/02_operating_system/11_exam_summary/728_c_scan_circular_elevator/)
**다음**: [730. RAID 0, 1, 5, 6 성능 신뢰성 (RAID Levels Performance Reliability)](/knowledge-base/studynote/02_operating_system/11_exam_summary/730_raid_levels_performance_reliability/) →

---
