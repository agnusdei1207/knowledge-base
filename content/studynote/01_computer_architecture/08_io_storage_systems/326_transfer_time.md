---
title: "326. 전송 시간 (Transfer Time)"
date: "2026-03-27"
tags:
  - "studynote-computer-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 전송 시간 (Transfer Time)은 헤드가 이미 목표 위치를 찾은 뒤, 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 저장 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)에서 호스트 메모리 쪽으로 흘러가는 순수한 이동 시간이다.
> 2. **가치**: [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/) ([Seek Time](/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/))과 [회전 지연](/studynote/01_computer_architecture/08_io_storage_systems/325_rotational_latency/) ([Rotational Latency](/studynote/01_computer_architecture/08_io_storage_systems/325_rotational_latency/))이 "찾는 비용"이라면, 전송 시간은 요청 크기와 전송률에 비례하는 "실제 운반 비용"이므로 대용량 순차 입출력 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 지배한다.
> 3. **판단 포인트**: 전송 시간을 줄이려면 인터페이스 명칭보다 먼저 내부 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 전송률, 기록 밀도, 순차성, [버퍼링](/studynote/02_operating_system/08_storage_and_io_systems/454_buffering/) 구조를 봐야 하며, 특히 [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) (Hard Disk Drive)는 바깥 트랙과 안쪽 트랙의 속도 차이까지 고려해야 한다.

---

## Ⅰ. 개요 및 필요성

전송 시간 (Transfer Time)은 저장장치가 찾은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 실제로 읽거나 써서 시스템으로 넘기는 데 걸리는 시간이다. 디스크 접근 시간 ([Disk Access Time](/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/))을 `탐색 시간 + 회전 지연 + 전송 시간`으로 나누면, 앞의 두 항목은 위치를 맞추는 준비 동작이고 마지막 항목만이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 양에 따라 길어지는 본 작업이다. 따라서 4KB처럼 작은 블록에서는 전송 시간이 거의 묻히지만, 1GB [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이나 대규모 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 스캔처럼 긴 순차 읽기에서는 이 항목이 전체 체감 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 사실상 결정한다.

이 개념이 중요한 이유는 저장장치 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 단순히 "빠르다/느리다"로 보면 병목을 잘못 짚기 쉽기 때문이다. 예를 들어 7,200 RPM (Revolutions Per Minute) HDD는 한 번 자리를 잡은 뒤에는 초당 150~250MB 수준으로 연속 전송할 수 있지만, 위치를 자주 바꾸면 그 능력을 거의 쓰지 못한다. 반대로 대용량 미디어 서버나 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) 스캔 작업은 위치 맞추기보다 "얼마나 끊기지 않고 계속 흘려보내느냐"가 핵심이므로 전송 시간 중심으로 설계해야 한다.

아래 그림은 전송 시간이 "디스크 표면 -> 장치 버퍼 -> 시스템 메모리"의 연속 흐름에서 결정된다는 점을 보여준다.

```text
+----------------------------------------------------------------------+
|              전송 시간의 실제 경로: 찾은 뒤에 얼마나 빨리 옮기나     |
+----------------------------------------------------------------------+
| [Platter/낸드 플래시] -- 내부 읽기 ---> [Device Buffer] -- 인터페이스 ---> |
|                                                            주기억장치    |
|      |                         |                            |        |
|      |                         |                            +- DMA    |
|      |                         +- 버스트 전송·프리패치                 |
|      +- 기록 밀도·회전수·채널 수가 좌우                                |
|                                                                      |
| 핵심 병목                                                             |
| - HDD: 플래터에서 읽어내는 내부 전송률                                |
| - SSD: 낸드 채널 병렬도와 컨트롤러 처리량                             |
+----------------------------------------------------------------------+
```

핵심은 케이블 표기 속도가 곧 실제 전송 시간이 아니라는 점이다. [SATA](/studynote/01_computer_architecture/08_io_storage_systems/341_sata/) ([Serial ATA](/studynote/01_computer_architecture/08_io_storage_systems/341_sata/)) 3.0이 6Gb/s를 지원하더라도 [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 내부 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)가 초당 200MB밖에 못 읽으면 체감 전송 시간은 내부 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 속도에 묶인다. 그래서 저장장치를 평가할 때는 인터페이스 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 전송률, 요청 크기를 함께 봐야 한다.

- **📢 섹션 요약 비유**: 전송 시간은 택배 상자를 찾은 뒤 트럭에 실어 목적지로 보내는 시간과 같다. 창고 위치를 찾는 시간이 아무리 빨라도, 상자를 싣는 벨트가 느리면 대량 배송은 결국 늦어진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

전송 시간은 기본적으로 <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 크기 / 실효 전송률</strong>로 계산된다. 가장 단순하게는 `T_transfer = B / R`이며, 여기서 `B`는 전송 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 수, `R`은 초당 전송 가능한 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 수다. HDD에서는 `R`이 회전 속도와 트랙당 저장량에 의해 결정되어 `R ≈ r × N`으로 볼 수 있다. 여기서 `r`은 RPS (Revolutions Per Second, 초당 회전수), `N`은 한 바퀴 동안 헤드 아래를 지나가는 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 양이다.

즉 [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 전송 시간을 줄이는 방법은 크게 두 가지다. 첫째, 회전 속도를 높여 같은 시간 동안 더 많은 섹터를 통과시키는 것이다. 둘째, 같은 회전수에서도 트랙 하나에 더 많은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 싣도록 기록 밀도를 높이는 것이다. 오늘날에는 발열과 진동 때문에 RPM 상승 여지가 작아졌으므로, 실제 경쟁력은 ZBR (Zoned [Bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) Recording)처럼 바깥 트랙에 더 많은 섹터를 배치해 `N`을 키우는 방식에서 많이 나온다.

| 요소 | 전송 시간에 미치는 영향 | 설계 포인트 |
| :--- | :--- | :--- |
| 요청 크기 | 클수록 전송 시간 증가 | 작은 요청 다발은 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 지배, 큰 요청은 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 지배 |
| 회전 속도 (RPM) | 높을수록 [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 연속 전송률 증가 | 소음, 전력, 발열 한계 존재 |
| 기록 밀도 | 높을수록 1회전당 전송량 증가 | 바깥 트랙이 더 유리 |
| 버퍼/캐시 | 실제 체감 전송 시간 단축 | 프리패치, [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 병합, [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)트 전송 |
| 인터페이스 | 장치 외부 병목 여부 결정 | [SATA](/studynote/01_computer_architecture/08_io_storage_systems/341_sata/), SAS, PCIe는 상한선 역할 |

아래 그림은 ZBR이 왜 전송 시간에 직접 영향을 주는지 보여준다.

```text
+----------------------------------------------------------------------+
|                 ZBR이 전송 시간을 줄이는 이유                        |
+----------------------------------------------------------------------+
| 안쪽 트랙 (둘레 짧음)      같은 1회전        바깥 트랙 (둘레 김)      |
| [ o o o o o o ]        ---------------->    [ o o o o o o o o o ]     |
|   적은 섹터 수                                    많은 섹터 수        |
|                                                                      |
| 7,200RPM이 동일해도                                                   |
| - 안쪽 트랙: 1회전에 읽는 양이 적음                                   |
| - 바깥 트랙: 1회전에 읽는 양이 많음                                   |
| => 같은 시간에 더 많은 바이트를 넘기므로 전송 시간이 짧아짐           |
+----------------------------------------------------------------------+
```

이 차이 때문에 HDD는 같은 제품 안에서도 LBA (Logical Block Address) 위치에 따라 초반 영역이 후반 영역보다 빠르다. 반면 [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) ([Solid State Drive](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))는 회전 구조가 없으므로 위치별 차이보다 컨트롤러, 낸드 플래시 채널, [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성, [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 증폭이 전송 시간을 좌우한다. 따라서 전송 시간을 이해할 때는 단순 공식만 외우기보다 "[매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)가 한 단위 시간에 몇 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)를 연속으로 뽑아낼 수 있는가"를 구조적으로 보는 것이 중요하다.

- **📢 섹션 요약 비유**: 같은 속도로 도는 회전문이라도 바깥쪽 칸이 더 넓으면 한 번 돌 때 더 많은 사람이 지나간다. HDD의 전송 시간도 결국 한 바퀴에 얼마나 많은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 태우느냐의 싸움이다.

---

## Ⅲ. 비교 및 연결

전송 시간은 HDD와 SSD를 비교할 때 가장 직관적으로 차이가 드러나는 지점이다. HDD는 단일 헤드가 지나가는 면적에서 순차적으로 읽는 구조라서 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성이 약하고, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 위치에 따라 속도가 달라진다. SSD는 여러 낸드 채널과 패키지에서 동시에 읽어 들일 수 있어, [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 자체를 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 키우는 방향으로 발전했다.

| 비교 항목 | [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) | [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) |
| :--- | :--- | :--- |
| 전송 메커니즘 | 플래터 회전 + 헤드 판독 | 낸드 플래시 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 읽기 |
| 전송률 결정 요인 | RPM, 기록 밀도, ZBR | 채널 수, 컨트롤러, [PCIe](/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) |
| 위치별 편차 | 큼, 바깥 트랙이 유리 | 상대적으로 작음 |
| 강한 workload | 대용량 순차 스캔 | 순차/랜덤 모두 강함 |
| 대표 병목 | 내부 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 전송률 | 컨트롤러·열 스로틀링 |

또한 전송 시간은 운영체제와 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 개념과도 연결된다. 운영체제는 읽기 선행([Read-Ahead](/studynote/02_operating_system/09_file_system/537_read_ahead_delayed_write/))과 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 결합(Write Coalescing)으로 자잘한 요청을 큰 순차 요청처럼 바꿔 전송 시간을 유리하게 만든다. [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템은 연속 블록 배치와 조각화 억제를 통해 [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/)을 줄일 뿐 아니라, 한 번 읽기 시작하면 긴 구간을 쉬지 않고 흘려보내도록 만들어 전송 시간 효율을 높인다. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스와 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이 큰 블록 크기를 선호하는 이유도 결국 "찾는 횟수"보다 "한 번에 오래 전송하는 구간"을 늘리기 위해서다.

즉 저장장치 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간과 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)의 줄다리기다. [OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) (Online [Transaction](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Processing)처럼 작은 랜덤 요청이 많은 환경은 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간이 중요하지만, [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)·[복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)·[ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) (Extract, Transform, Load)처럼 큰 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 오래 흘리는 환경은 전송 시간이 전체 완료 시간을 좌우한다. 그래서 같은 저장장치라도 workload에 따라 좋고 나쁨이 달라진다.

- **📢 섹션 요약 비유**: HDD는 한 줄로 서서 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 한 대에 차례로 타는 방식이고, SSD는 여러 탑승구에서 동시에 비행기에 태우는 방식과 비슷하다. 둘 다 사람을 옮기지만, 대량 이동에서는 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 탑승이 훨씬 유리하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 전송 시간을 다룰 때 가장 중요한 질문은 "이 시스템이 지금 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 병목인가, [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 병목인가"이다. 예를 들어 영상 스트리밍 서버, [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 저장소, [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 스캔 서버는 한 번 읽기 시작하면 수백 MB 이상을 길게 흘리는 경우가 많다. 이런 환경에서는 짧은 탐색 최적화보다 높은 순차 전송률, 넉넉한 버퍼, [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) [스트라이핑](/studynote/01_computer_architecture/08_io_storage_systems/332_raid_0/), 큰 I/O 크기가 더 직접적인 효과를 낸다.

반대로 작은 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수만 개를 읽는 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 중심 서비스라면 전송 시간을 아무리 줄여도 체감 개선이 제한적이다. 이런 환경에서 HDD를 계속 쓰면서 인터페이스만 SATA에서 SAS로 바꿔도 큰 차이가 없는 이유가 여기에 있다. 병목이 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 전송이 아니라 탐색과 회전 대기라면, 저장장치 교체 또는 캐시 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 변경이 더 먼저다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. <strong>요청 크기 <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>: 4KB 랜덤 중심인지, 1MB 이상 순차 중심인지 분리해서 본다.
2. <strong>실효 <a href="/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">대역폭</a> 측정</strong>: 인터페이스 스펙이 아니라 실제 MB/s를 측정한다.
3. **배치 위치 고려**: HDD라면 빈번한 순차 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 빠른 외곽 영역에 배치하는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 검토한다.
4. <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/454_buffering/">버퍼링</a> 활용</strong>: 읽기 선행, [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 캐시, [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) ([Direct Memory Access](/studynote/01_computer_architecture/08_io_storage_systems/318_dma/))를 통해 CPU 개입과 잔단위 전송을 줄인다.
5. <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a> 제거</strong>: 대용량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 잘게 쪼개 자주 동기화하는 구조를 피한다.

### 대표 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 대용량 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 4KB 이하 조각으로 잘라 매번 즉시 flush하는 설계
- [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 기반 분석 서버에서 조각난 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 스캔하도록 만들어 헤드 이동만 폭증시키는 설계
- 인터페이스 숫자만 보고 실제 플래터 전송률이나 낸드 열 스로틀링을 무시하는 설계

결론적으로 전송 시간을 최적화한다는 말은 "더 큰 덩어리를, 더 연속적으로, 더 적은 중단으로 흘리게 만든다"는 뜻에 가깝다. 시험 답안에서도 단순 정의보다 workload 구분과 병목 판별 기준까지 써야 기술사다운 판단이 된다.

- **📢 섹션 요약 비유**: 물탱크를 채울 때는 컵으로 천 번 붓는 것보다 굵은 호스로 한 번에 흘려보내는 편이 훨씬 낫다. 전송 시간 최적화도 결국 흐름을 끊지 않게 만드는 일이다.

---

## Ⅴ. 기대효과 및 결론

전송 시간을 올바르게 이해하면 저장장치 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 "응답 속도"와 "[처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)"으로 나누어 해석할 수 있다. 그 결과 시스템 설계자는 작은 요청 위주의 서비스에는 SSD와 캐시를, 긴 순차 작업에는 높은 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)과 연속 배치를 우선하는 식으로 더 정확한 선택을 할 수 있다. 특히 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), 미디어 처리, 대규모 분석, [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 작업에서는 전송 시간이 짧아질수록 작업 완료 시간과 전력 낭비를 함께 줄일 수 있다.

다만 전송 시간만 보고 저장장치를 평가하면 오판할 수 있다. [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)이 높아도 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간이 나쁘면 사용자 체감은 떨어질 수 있고, [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 역시 열 스로틀링이나 가비지 컬렉션이 시작되면 지속 전송률이 내려갈 수 있다. 따라서 전송 시간은 단독 지표가 아니라 접근 패턴, 캐시 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/), 인터페이스, [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 특성과 함께 해석해야 한다.

결국 전송 시간은 저장장치의 "실제 운반 능력"을 보여주는 지표다. 찾는 데 걸리는 시간을 줄이는 것도 중요하지만, 한 번 찾은 뒤 얼마나 길고 안정적으로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 흘려보낼 수 있는가가 대용량 시스템의 승부를 가른다.

- **📢 섹션 요약 비유**: 좋은 창고 시스템은 물건을 빨리 찾는 것에서 끝나지 않는다. 찾은 뒤 지게차가 멈추지 않고 끝까지 실어 나를 수 있어야 진짜 생산성이 나온다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 접근 시간 (Access Time) | 전송 시간은 [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/), [회전 지연](/studynote/01_computer_architecture/08_io_storage_systems/325_rotational_latency/)과 함께 전체 I/O 응답시간을 완성한다. |
| ZBR (Zoned [Bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) Recording) | 바깥 트랙에 더 많은 섹터를 넣어 HDD의 순차 전송률을 높인다. |
| [Read-Ahead](/studynote/02_operating_system/09_file_system/537_read_ahead_delayed_write/) | 다음 블록을 미리 읽어 버퍼에 쌓아 실제 체감 전송 시간을 줄인다. |
| [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) ([Direct Memory Access](/studynote/01_computer_architecture/08_io_storage_systems/318_dma/)) | 장치와 메모리 사이 전송을 CPU 개입 없이 처리해 대용량 I/O 효율을 높인다. |
| [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) (Redundant [Array](/studynote/08_algorithm_stats/04_datastructure/055_array/) of Independent Disks) Striping | 여러 디스크에 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 나눠 써 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 전송률을 키우는 방식이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
탐색 시간·회전 지연 인식
        |
        v
전송 시간 (Transfer Time) 분리 측정
        |
        v
ZBR (Zoned Bit Recording) · Read-Ahead · DMA
        |
        v
RAID Striping · 대용량 순차 I/O 최적화
        |
        v
SSD 병렬 채널 · NVMe (Non-Volatile Memory Express) 기반 고대역폭 스토리지
```

이 흐름은 저장장치 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 논의가 "위치 찾기"에서 시작해, 점차 "얼마나 많이 동시에 옮길 수 있는가"로 확장되어 왔음을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 전송 시간은 장난감 상자를 찾은 뒤, 그 안의 블록들을 하나씩 책상으로 옮기는 시간이에요.
2. 블록이 많을수록 오래 걸리고, 넓은 미끄럼틀로 보내면 더 빨리 옮길 수 있어요.
3. 그래서 컴퓨터는 한 번 찾은 뒤에는 멈추지 않고 쭉 많이 보내도록 똑똑하게 길을 만들어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 327 / 803

<- **이전**: [325. 회전 지연 (Rotational Latency)](/studynote/01_computer_architecture/08_io_storage_systems/325_rotational_latency/)
**다음**: [327. SSD (Solid State Drive)](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) ->

---
