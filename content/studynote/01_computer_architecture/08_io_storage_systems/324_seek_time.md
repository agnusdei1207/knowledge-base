+++
title = "324. 탐색 시간 (Seek Time)"
date = 2026-03-27

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 탐색 시간 ([Seek Time](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/))은 [하드 디스크 드라이브](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) (Hard Disk Drive, [HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/))에서 헤드 (Head)가 현재 트랙 (Track)에서 목표 트랙으로 이동해 읽기 준비를 마칠 때까지의 <strong>기계적 위치 맞춤 시간</strong>이다.
> 2. **가치**: 이 시간은 [회전 지연](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/325_rotational_latency/) ([Rotational Latency](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/325_rotational_latency/)), [전송 시간](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/326_transfer_time/) ([Transfer Time](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/326_transfer_time/))보다 자주 더 큰 병목이어서, HDD의 랜덤 접근 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 초당 입출력 횟수 (IOPS, Input/Output Operations Per Second)를 사실상 결정한다.
> 3. **판단 포인트**: 탐색 시간은 하드웨어만의 문제가 아니라 요청 순서, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 배치, 캐시, [솔리드 스테이트 드라이브](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/475_ssd_structure/) ([Solid State Drive](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/), [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/)) 전환 전략까지 좌우하는 시스템 설계 판단 기준이다.

---

## Ⅰ. 개요 및 필요성

탐색 시간은 [HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 헤드가 원하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 들어 있는 트랙 위로 이동하는 데 걸리는 시간이다. 메모리처럼 전기 신호만으로 즉시 주소를 열어보는 구조가 아니라, 실제 금속 암 (Actuator Arm)이 움직여야 하므로 밀리초(ms) 단위의 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 발생한다. 이 한 번의 기계 동작이 CPU (Central Processing Unit)와 주기억장치보다 훨씬 느리기 때문에 저장장치 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 이해할 때 반드시 따로 떼어 봐야 한다.

이 개념이 중요한 이유는 HDD가 "용량은 크지만 위치에 따라 속도가 달라지는 장치"이기 때문이다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 인접해 있으면 헤드가 거의 움직이지 않아 빠르게 읽을 수 있지만, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 흩어져 있거나 작은 요청이 연속해서 들어오면 헤드가 계속 왕복한다. 결국 탐색 시간은 단순한 세부 스펙이 아니라, 왜 HDD가 순차 접근에는 강하고 랜덤 접근에는 약한지를 설명하는 핵심 열쇠다.

아래 그림은 [HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 접근 과정에서 탐색 시간이 어디에 끼어드는지 보여준다. 핵심은 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽기 전, 먼저 위치를 맞추는 물리 이동이 선행된다"는 점이다.

```text
+------------------------------------------------------------------------------+
|                 HDD 접근의 첫 단계: 헤드가 먼저 트랙을 찾아간다              |
+------------------------------------------------------------------------------+
| 요청 발생                                                                     |
|    |                                                                          |
|    +- 현재 Head 위치 확인                                                     |
|    |                                                                          |
|    +- Seek Time                                                               |
|    |   [Track 12] ----------------> [Track 87]                                 |
|    |        헤드 이동 + 가속/감속 + 안착                                      |
|    |                                                                          |
|    +- Rotational Latency                                                      |
|    |   목표 섹터가 Head 아래로 올 때까지 대기                                 |
|    |                                                                          |
|    +- Transfer Time                                                           |
|        실제 데이터 읽기/쓰기                                                  |
+------------------------------------------------------------------------------+
```

탐색 시간이 먼저 길어지면 뒤의 [회전 지연](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/325_rotational_latency/)과 [전송 시간](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/326_transfer_time/)을 최적화해도 체감 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 크게 좋아지지 않는다. 그래서 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)는 "얼마나 빨리 읽느냐" 이전에 "얼마나 적게 움직이게 하느냐"를 먼저 고민한다.

📢 섹션 요약 비유: 탐색 시간은 거대한 서고에서 원하는 책장이 있는 줄까지 사서가 직접 걸어가는 시간과 같다. 책을 펼쳐 읽는 속도보다, 먼저 그 위치에 도착하는 시간이 전체 대기의 시작을 결정한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

탐색 시간은 단순히 "거리만큼 비례"해서 늘어나는 값이 아니다. 헤드를 움직이는 보이스 코일 모터 (Voice Coil Motor, VCM)는 먼저 팔을 가속하고, 목표 위치 근처에서 감속하며, 마지막에는 미세 진동을 멈추고 정확히 안착해야 한다. 그래서 가까운 트랙으로 이동할 때와 먼 트랙으로 이동할 때의 차이는 선형적이지 않으며, 특히 마지막 정착 구간이 안정성을 좌우한다.

보통 [HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 제조사는 세 가지 탐색 시간을 제시한다. 트랙 간 탐색 (Track-to-Track Seek)은 바로 옆 트랙으로 이동하는 최소 시간이고, 평균 탐색 시간 (Average [Seek Time](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/))은 임의 두 위치 사이 이동의 평균값이며, 풀 스트로크 탐색 (Full Stroke Seek)은 가장 안쪽에서 가장 바깥쪽까지 가는 최대 수준의 시간이다. 시험과 실무에서는 대개 평균 탐색 시간이 대표 지표로 쓰이지만, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 민감 워크로드는 꼬리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 보려면 풀 스트로크 조건도 함께 봐야 한다.

| 구분 | 의미 | 대략적 범위 | 왜 중요한가 |
| :--- | :--- | :--- | :--- |
| 트랙 간 탐색 | 인접 트랙 1칸 이동 | 1ms 안팎 | 최소 이동 비용 파악 |
| 평균 탐색 시간 | 임의 위치 간 평균 이동 | 3~10ms | 일반적 체감 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 지표 |
| 풀 스트로크 탐색 | 디스크 전역 최대 이동 | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~20ms 이상 | 최악 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 안정성 판단 |

다음 그림은 탐색 시간이 내부적으로 어떤 단계로 나뉘는지 보여준다.

```text
+------------------------------------------------------------------------------+
|                    Seek Time의 내부 4단계와 병목 위치                         |
+------------------------------------------------------------------------------+
| [1] 가속                [2] 이동                [3] 감속       [4] 안착       |
|     +-------+              +--------------+         +------+      +------+    |
| Head|  출발  +------------->| 목표 근처 접근 |--------->| 속도v |------>| 진동v |    |
|     +-------+              +--------------+         +------+      +------+    |
|         ^                        ^                       ^             ^        |
|         |                        |                       |             |        |
|     모터 구동                거리 영향 큼            오버슈트 방지   트랙 정밀도 |
|                                                                              |
| Seek Time = 가속 + 이동 + 감속 + Settling Time                              |
+------------------------------------------------------------------------------+
```

이 그림이 말하는 핵심은, 탐색 시간의 병목이 단순 이동 거리보다 "정확히 멈추는 과정"에도 있다는 점이다. 따라서 [HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 논할 때는 RPM (Revolutions Per Minute)만 볼 것이 아니라, 평균 탐색 시간, 캐시 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 요청 패턴을 함께 봐야 한다.

📢 섹션 요약 비유: 탐색 시간은 자동차가 목적지까지 달려가는 시간만이 아니다. 출발할 때 속도를 올리고, 도착 직전에 브레이크를 밟고, 주차선 안에 흔들림 없이 정확히 세우는 전 과정을 모두 포함한 시간이다.

---

## Ⅲ. 비교 및 연결

탐색 시간을 제대로 이해하려면 [회전 지연](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/325_rotational_latency/), [전송 시간](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/326_transfer_time/), SSD와 함께 비교해야 한다. 탐색 시간은 반지름 방향의 "헤드 이동"이고, [회전 지연](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/325_rotational_latency/)은 원주 방향의 "섹터 대기"이며, [전송 시간](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/326_transfer_time/)은 실제 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 운반"이다. 세 요소는 모두 접근 시간에 포함되지만 원인이 다르기 때문에, 병목 상황과 대응 전략도 서로 다르다.

| 비교 항목 | 발생 원인 | 크게 문제 되는 상황 | 주요 대응 |
| :--- | :--- | :--- | :--- |
| 탐색 시간 ([Seek Time](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/)) | 헤드의 트랙 이동 | 작은 랜덤 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 다발 | 요청 재정렬, 연속 배치, [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 전환 |
| [회전 지연](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/325_rotational_latency/) ([Rotational Latency](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/325_rotational_latency/)) | 섹터가 아직 안 돌아옴 | 랜덤 I/O, 낮은 RPM | 고RPM, 캐시, [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 전환 |
| [전송 시간](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/326_transfer_time/) ([Transfer Time](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/326_transfer_time/)) | 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)량 전송 | 대용량 순차 처리 | 높은 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), 큰 블록, [버퍼링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/454_buffering/) |
| [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 접근 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 전기적 주소 해석 | 상대적으로 작음 | 컨트롤러 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성 최적화 |

[운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 [디스크 스케줄링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/)도 탐색 시간과 직접 연결된다. 선입선출 ([FCFS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/), First-Come, First-Served)은 공정하지만 헤드가 멀리 왕복할 수 있고, 최단 탐색 우선 ([SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/), Shortest [Seek Time](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/) First)은 이동을 줄이지만 특정 요청이 오래 기다릴 수 있다. SCAN 계열은 엘리베이터처럼 한 방향으로 쭉 처리하며 이동 낭비와 기아를 균형 있게 줄이려는 절충안이다.

또한 SSD는 탐색 시간이 거의 의미 없는 구조라는 점에서 HDD와 결정적으로 다르다. HDD는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 "위치"가 곧 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이지만, SSD는 위치보다 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 채널, 플래시 변환 계층 ([Flash Translation Layer](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/), [FTL](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/)), 가비지 컬렉션이 더 중요하다. 그래서 저장장치 기술의 진화는 탐색 시간을 소프트웨어로 완화하던 시대에서, 아예 기계 이동 자체를 없애는 시대로 넘어갔다고 볼 수 있다.

📢 섹션 요약 비유: 탐색 시간은 큰 마트에서 원하는 진열대로 걸어가는 시간이고, [회전 지연](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/325_rotational_latency/)은 직원이 창고 벨트에서 물건을 내 앞으로 보내 줄 때까지 기다리는 시간이다. SSD는 아예 걸어갈 필요 없이 화면에서 품목을 누르면 바로 꺼내 주는 자동 창고에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 탐색 시간은 "HDD를 어디에 써도 되는가"를 가르는 판단 기준이다. [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 색인 조회, 가상머신 부팅 디스크, [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 서버처럼 작은 랜덤 I/O가 많은 환경에서는 탐색 시간이 쌓이면서 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간과 꼬리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 급격히 나빠진다. 반대로 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 아카이브, 대용량 미디어 저장처럼 순차 접근 중심인 경우에는 한 번 자리만 잡으면 길게 읽을 수 있어 탐색 시간의 손해가 상대적으로 작다.

### 설계 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요청이 순차적인가, 아니면 작은 랜덤 블록이 반복되는가?
2. [HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 위 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 연속 배치되어 있는가, 아니면 파편화 ([Fragmentation](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/))되어 있는가?
3. [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)나 스토리지 컨트롤러가 요청 순서를 재정렬하고 있는가?
4. 캐시, 배치 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), 읽기 선행 ([Read-Ahead](/knowledge-base/studynote/02_operating_system/09_file_system/537_read_ahead_delayed_write/))으로 탐색을 숨길 수 있는가?
5. 고RPM [HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 튜닝보다 [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 또는 티어링 전환이 더 경제적인가?

### 대표 적용 시나리오

- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> 테이블 파편화</strong>: 인덱스와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 페이지가 흩어지면 조회 한 번마다 헤드 이동이 커져 응답시간이 급증한다. 이때 재구성, 클러스터링, 캐시 확장이 효과적이다.
- **숏 스트로킹 (Short Stroking)**: 디스크의 바깥쪽 일부 구간만 사용해 헤드 이동 범위를 줄이면 평균 탐색 시간을 낮출 수 있다. 저장 용량은 희생하지만 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간을 줄이는 전형적 트레이드오프다.
- **하이브리드 스토리지**: 자주 접근하는 핫 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 SSD에, 장기 보관 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 HDD에 두면 탐색 시간의 약점을 비용 효율적으로 우회할 수 있다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 작은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수만 개를 HDD에 랜덤하게 직접 기록하는 설계
- 요청 재정렬 없이 실시간 순서만 고집해 헤드를 디스크 전역으로 왕복시키는 설계
- 인터페이스 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)만 높이면 랜덤 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)도 좋아질 것이라 착각하는 설계

기술사 답안에서는 "탐색 시간은 헤드 이동 시간"에서 멈추면 부족하다. 어떤 workload에서 병목이 되는지, 어떤 완화 기법이 있으며, 언제 SSD로 넘어가야 하는지까지 연결해야 실무 판단이 된다.

📢 섹션 요약 비유: 탐색 시간 관리는 배달 기사 동선을 짜는 일과 같다. 주문을 받은 순서대로 무조건 보내면 공정해 보여도 길 위에서 시간을 다 잃고, 가까운 곳끼리 묶고 자주 가는 동네는 거점 창고를 두어야 전체 배송이 빨라진다.

---

## Ⅴ. 기대효과 및 결론

탐색 시간을 정확히 이해하면 저장장치 병목을 훨씬 현실적으로 해석할 수 있다. 그 결과 설계자는 단순히 "디스크가 느리다"가 아니라, 위치 이동이 문제인지, 회전 대기가 문제인지, 순차 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)이 문제인지 구분할 수 있다. 이 구분이 있어야 캐시 확대, 스케줄링 조정, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재배치, [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 전환 같은 대책도 올바르게 선택된다.

또한 이 개념은 컴퓨터 구조의 중요한 교훈을 준다. 시스템 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 가장 빠른 부품이 아니라 가장 느린 병목에 의해 결정되며, [HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 시대에는 그 대표 병목이 바로 헤드 이동이었다. 그래서 프리페치, [버퍼 캐시](/knowledge-base/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/), [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 구조화, [RAID](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) (Redundant [Array](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) of Independent Disks), 계층형 스토리지 같은 많은 기법이 탐색 시간을 직접 줄이거나 우회하는 방향으로 발전했다.

결국 탐색 시간은 오래된 디스크 지표가 아니라, <strong>물리 구조가 소프트웨어 설계까지 규정한다</strong>는 사실을 보여주는 대표 개념이다. 오늘날 SSD가 주류가 되었어도, 병목을 분해하고 계층적으로 숨기는 사고방식은 여전히 이 개념 위에서 배울 수 있다.

📢 섹션 요약 비유: 탐색 시간은 공연장 전체를 뛰어다니며 필요한 악보를 찾는 시간과 같다. 좋은 시스템은 연주자를 더 빨리 뛰게 만들기보다, 악보를 가까이 두고 순서를 정리해 공연이 끊기지 않게 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 트랙·섹터·실린더 | 탐색 시간은 이 물리 위치 체계 위에서 헤드가 어느 반지름으로 이동하느냐에 의해 결정된다. |
| [회전 지연](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/325_rotational_latency/) ([Rotational Latency](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/325_rotational_latency/)) | 탐색이 끝난 뒤에도 남는 대기 시간으로, 둘을 합쳐 [HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 랜덤 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 커진다. |
| [디스크 스케줄링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/) ([Disk Scheduling](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/)) | 요청 순서를 조정해 헤드 이동 총량을 줄이는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 측 완화 기법이다. |
| [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) ([Solid State Drive](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/)) | 기계적 헤드 이동이 없어 탐색 시간 개념을 사실상 제거한 저장장치다. |
| 파편화 ([Fragmentation](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 흩어질수록 헤드 왕복이 늘어나 평균 탐색 시간이 체감상 더 커진다. |
| [스토리지 티어링](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/674_storage_tiering/) ([Storage Tiering](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/674_storage_tiering/)) | 탐색 시간에 민감한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 그렇지 않은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다른 매체에 분리 배치한다. |

### 📈 관련 키워드 및 발전 흐름도

```text
자기 디스크 기반 위치 접근
        |
        v
트랙 (Track) · 헤드 (Head) · 실린더 (Cylinder)
        |
        v
탐색 시간 (Seek Time) + 회전 지연 (Rotational Latency)
        |
        v
디스크 스케줄링 · 파편화 관리 · 버퍼 캐시
        |
        v
숏 스트로킹 · RAID · 계층형 스토리지
        |
        v
SSD (Solid State Drive) · NVMe (Non-Volatile Memory Express)
```

이 흐름은 저장장치 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 논의가 단순한 위치 이동의 이해에서 시작해, 소프트웨어적 완화와 아키텍처 분화, 그리고 결국 기계 이동 제거로 발전해 온 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 탐색 시간은 큰 책장 앞에서 로봇 팔이 내가 원하는 칸까지 움직여 가는 시간이야.
2. 책을 읽는 시간보다, 먼저 그 칸까지 가는 시간이 더 오래 걸릴 때가 많아.
3. 그래서 컴퓨터는 로봇 팔이 덜 움직이게 책을 가까이 모아 두거나, 아예 바로 꺼낼 수 있는 더 빠른 상자를 쓰는 거야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 325 / 803

<- **이전**: [323. 트랙, 섹터, 실린더](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/323_track_sector_cylinder/)
**다음**: [325. 회전 지연 (Rotational Latency)](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/325_rotational_latency/) ->

---
