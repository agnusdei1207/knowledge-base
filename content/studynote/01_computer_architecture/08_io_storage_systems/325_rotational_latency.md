---
title: "325. 회전 지연 (Rotational Latency)"
date: "2026-03-27"
tags:
  - "studynote-computer-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) (Rotational [Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))은 [하드 디스크 드라이브](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) (Hard Disk Drive, [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/))에서 헤드가 올바른 트랙에 도착한 뒤에도, 원하는 섹터가 헤드 아래로 회전해 들어올 때까지 기다리는 순수한 기계적 대기 시간이다.
> 2. **가치**: 이 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/) ([Seek Time](/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/))과 함께 디스크 접근 시간 ([Disk Access Time](/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/))을 결정하며, 순차 입출력보다 랜덤 입출력에서 [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 성능을 급격히 떨어뜨리는 핵심 원인이다.
> 3. **판단 포인트**: 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 완전히 제거할 수 없는 물리 한계이므로, 설계자는 RPM (Revolutions Per Minute), 스케줄링, 캐시, [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) ([Solid State Drive](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/)) 전환 중 무엇으로 대응할지 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 플래터가 계속 회전하는 구조 때문에 생기는 대기 시간이다. 헤드가 이미 목표 트랙 위에 정확히 올라왔더라도, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 기록된 섹터가 아직 헤드 위치까지 오지 않았다면 읽기와 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)는 시작될 수 없다. 즉 저장장치는 "찾는 시간"과 "도착을 기다리는 시간"을 모두 가진다.

이 개념이 중요한 이유는 많은 학습자가 디스크 성능을 [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/)만으로 이해하기 쉽기 때문이다. 그러나 실제 랜덤 접근에서는 헤드 이동이 끝난 뒤에도 평균 수 밀리초(ms)를 더 기다려야 하며, 이 누적 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/), [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 서버, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 저장 같은 워크로드의 응답성을 크게 떨어뜨린다. 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 이해해야 왜 HDD가 대용량 순차 처리에는 강하지만 작은 요청이 많은 환경에서는 약한지 설명할 수 있다.

다음 그림은 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 언제 발생하는지 보여준다. 핵심은 헤드 위치가 맞아도, 섹터의 각도 위치가 맞지 않으면 바로 접근할 수 없다는 점이다.

```text
+------------------------------------------------------------------------------+
|           회전 지연 발생 시점: 트랙은 맞았지만 섹터가 아직 안 옴            |
+------------------------------------------------------------------------------+
|  1) 탐색 완료                                                               |
|     헤드 ----------> [목표 트랙 도착]                                         |
|                                                                              |
|  2) 하지만 목표 섹터는 다른 각도에 있음                                      |
|                                                                              |
|                 +------------ Platter 회전 방향 ------------+                |
|                 v                                           |                |
|            +--------------------------------------+         |                |
|            |   ○  ○  ○  [목표 섹터]  ○  ○  ○      |         |                |
|            +--------------------------------------+         |                |
|                         ^                                    |                |
|                       [Head]                                 |                |
|                                                                              |
|  3) 목표 섹터가 Head 아래로 올 때까지 대기 = Rotational Latency             |
+------------------------------------------------------------------------------+
```

이 그림은 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 "위치를 못 찾은 문제"가 아니라 "타이밍이 아직 안 맞은 문제"라는 점을 강조한다. 그래서 디스크 접근 시간은 단순 거리 문제가 아니라, 반지름 방향의 이동과 원주 방향의 대기가 합쳐진 2차원적 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 구조로 이해해야 한다.

- **📢 섹션 요약 비유**: 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 회전초밥집에서 자리에 앉는 것과 초밥이 내 앞에 오는 것을 구분하는 일과 같다. 자리에 앉는 데 성공해도, 내가 원하는 접시는 레일이 한 바퀴 더 돌아와야 먹을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)의 계산은 단순하지만 매우 중요하다. 플래터가 1분에 몇 바퀴 도는지를 나타내는 RPM만 알면, 한 바퀴 도는 최대 시간과 평균 대기 시간을 구할 수 있다. 임의의 섹터는 원판 어디에나 있을 수 있으므로 평균적으로는 반 바퀴를 기다린다고 본다.

- 최대 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/): `60 / RPM` 초
- 평균 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/): `30 / RPM` 초
- 예: 7,200 RPM HDD의 평균 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 `30 / 7200 ≈ 0.00417초 = 4.17ms`

| [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 회전 속도 | 1회전 시간 | 평균 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 해석 |
| :--- | :---: | :---: | :--- |
| 5,400 RPM | [11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/).[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/) ms | 5.56 ms | 저전력·대용량 중심 |
| 7,200 RPM | 8.33 ms | 4.17 ms | 일반 [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)·[NAS](/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/) 표준 |
| [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000 RPM | 6.00 ms | 3.00 ms | 고성능 워크로드 대응 |
| 15,000 RPM | 4.00 ms | 2.00 ms | 엔터프라이즈 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 최소화 |

다음 그림은 디스크 접근 시간이 어떻게 합쳐지는지 보여준다. 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 전송 전에 반드시 끼어드는 중간 대기 구간이며, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)량이 작을수록 상대적으로 더 아프게 느껴진다.

```text
+------------------------------------------------------------------------------+
|                 디스크 접근 시간의 구성: 찾고, 기다리고, 전송한다           |
+------------------------------------------------------------------------------+
|  요청 발생                                                                   |
|     |                                                                        |
|     +--> Seek Time                 : 헤드가 목표 트랙으로 이동                |
|     |      <------ 3 ~ 10 ms ------>                                         |
|     |                                                                        |
|     +--> Rotational Latency        : 목표 섹터가 Head 아래로 올 때까지 대기   |
|     |      <------ 2 ~ 6 ms ------->                                         |
|     |                                                                        |
|     +--> Transfer Time             : 실제 데이터 읽기/쓰기                    |
|            <-- 데이터 크기에 비례 -->                                        |
|                                                                              |
|  총 접근 시간 = Seek Time + Rotational Latency + Transfer Time              |
+------------------------------------------------------------------------------+
```

여기서 설계상의 함정은 RPM을 높여도 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 선형으로 조금씩만 줄어든다는 점이다. 7,200 RPM에서 15,000 RPM으로 거의 두 배 이상 빨라져도 평균 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 4.17ms에서 2.00ms로 줄어드는 수준이다. 이 때문에 제조사는 더 높은 RPM을 위해 발열, 진동, 소음, 베어링 마모를 감수해야 하고, 결국 기계식 저장장치의 한계가 드러난다.

- **📢 섹션 요약 비유**: 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 놀이공원 회전목마의 빈 말이 내 앞에 올 때까지 기다리는 시간과 같다. 회전목마를 더 빨리 돌리면 조금 일찍 탈 수는 있지만, 너무 빨리 돌리면 기계가 버티지 못한다.

---

## Ⅲ. 비교 및 연결

회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 제대로 이해하려면 [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/), [전송 시간](/studynote/01_computer_architecture/08_io_storage_systems/326_transfer_time/), 그리고 SSD의 무회전 특성과 함께 비교해야 한다. [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/)은 반지름 방향 이동이고, 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 원주 방향 대기이며, [전송 시간](/studynote/01_computer_architecture/08_io_storage_systems/326_transfer_time/)은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 실제로 흘러가는 시간이다. 즉 세 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 모두 원인이 다르므로 최적화 방법도 달라진다.

| 비교 항목 | 원인 | 줄이는 방법 | 병목이 두드러지는 상황 |
| :--- | :--- | :--- | :--- |
| [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/) ([Seek Time](/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/)) | 헤드의 기계적 이동 | [디스크 스케줄링](/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/), 숏 스트로킹 | 트랙 간 점프가 많을 때 |
| 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) (Rotational [Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) | 섹터의 각도 위치 대기 | 높은 RPM, 요청 재정렬, 캐시 | 랜덤 소량 입출력 |
| [전송 시간](/studynote/01_computer_architecture/08_io_storage_systems/326_transfer_time/) ([Transfer Time](/studynote/01_computer_architecture/08_io_storage_systems/326_transfer_time/)) | 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송량 | 높은 밀도, 인터페이스 향상 | 대용량 순차 전송 |
| [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 접근 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 전기적 주소 해석 | 컨트롤러·병렬성 개선 | HDD보다 매우 작음 |

[운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 관점에서는 [디스크 스케줄링](/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/)이 [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/)뿐 아니라 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)에도 간접적으로 영향을 준다. 예를 들어 요청을 재정렬해 헤드가 이동한 직후 근처 섹터를 읽도록 만들면, 운 좋게 회전 대기까지 줄일 수 있다. [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 관점에서는 [버퍼 캐시](/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/)와 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 배치 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(batch write)가 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 숨기는 대표 전략이며, 스토리지 아키텍처 관점에서는 이 한계 때문에 SSD와 [NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) ([Non-Volatile Memory Express](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/))로의 전환이 가속되었다.

결국 HDD는 순차 접근에서 강하고 랜덤 접근에서 약하다는 말의 절반은 [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/), 나머지 절반은 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 설명한다. 특히 작은 4KB 블록을 자주 읽는 워크로드에서는 [전송 시간](/studynote/01_computer_architecture/08_io_storage_systems/326_transfer_time/)보다 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/)이 압도적으로 커져 IOPS (Input/Output Operations Per Second)가 급락한다.

- **📢 섹션 요약 비유**: [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/)은 도서관에서 원하는 책장이 있는 방으로 걸어가는 시간이고, 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 그 방 안에서 자동 회전 서가가 내가 찾는 책등을 내 앞으로 돌려 보내는 시간이다. SSD는 아예 서가를 돌리지 않고 책 번호를 누르면 바로 서랍이 열리는 방식에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 "HDD를 어디까지 써도 되는가"를 가르는 판단 기준이다. 대용량 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), 미디어 아카이브, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 적재 후 배치 분석처럼 순차 처리 비중이 높은 환경에서는 HDD가 여전히 경제적이다. 반대로 온라인 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 처리, [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 조회, 가상머신 이미지 다중 호스팅처럼 작은 랜덤 입출력이 많은 환경에서는 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 체감 성능을 무너뜨리므로 SSD가 사실상 필수다.

### 설계 체크포인트

1. 요청 패턴이 순차 중심인지 랜덤 중심인지 구분했는가?
2. 평균 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 중요한지, 최대 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 꼬리 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)(Tail [Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))이 중요한지 판단했는가?
3. 캐시, 배치 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), 프리페치로 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 숨길 수 있는가?
4. RPM 상승 비용보다 [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 전환 비용이 더 합리적인가?

### 대표 시나리오

- <strong><a href="/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a> 장치</strong>: 짧은 동기 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 요청이 연속 발생하면 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 누적되어 커밋 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 급증한다. 이 영역은 10K/15K HDD로 버티기보다 [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 또는 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 캐시 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 장치가 달린 스토리지가 더 적합하다.
- <strong>대용량 <a href="/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/">백업</a> 저장소</strong>: 한 번에 긴 스트림으로 쓰고 읽는다면 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)의 영향은 상대적으로 작다. 이때는 용량당 비용이 더 중요한 의사결정 축이 된다.
- <strong><a href="/studynote/13_cloud_architecture/01_virtualization/015_virtualization/">가상화</a> 환경의 공유 스토리지</strong>: 여러 가상머신이 서로 다른 블록을 동시에 두드리면 랜덤 접근이 폭증한다. 이런 환경에서 [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 기반 어레이는 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/)이 동시에 겹쳐 급격히 느려진다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 작은 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 `fsync()`와 함께 연속으로 기록하는 설계
- [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 위에서 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 랜덤 조회가 많은 서비스에 캐시 없이 직접 접근시키는 설계
- 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 문제인데 인터페이스 대역폭만 올리면 해결된다고 오해하는 설계

- **📢 섹션 요약 비유**: 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 손님이 한 명씩 와서 주문을 바꾸는 식당과 같다. 주방이 아무리 커도 접시가 한 바퀴씩 돌 때마다 기다려야 하면, 회전이 많은 주문은 빨라지지 않는다.

---

## Ⅴ. 기대효과 및 결론

회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 정확히 이해하면 저장장치 성능을 더 현실적으로 판단할 수 있다. 단순한 용량이나 인터페이스 속도보다, 실제 서비스의 입출력 패턴이 기계식 대기에 얼마나 취약한지를 먼저 보게 되기 때문이다. 이는 스토리지 선택, 캐시 계층 설계, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 배치 방식, [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 투자 우선순위를 정하는 데 직접 도움이 된다.

또한 이 개념은 컴퓨터 구조 전반의 교훈도 준다. 처리장치가 빨라져도 시스템 전체 성능은 가장 느린 기계적 병목에 묶일 수 있으며, 그래서 캐시, 큐잉, 스케줄링, 비동기화 같은 구조적 대응이 필요하다. 저장장치의 진화가 HDD의 고RPM 경쟁에서 SSD의 무회전 구조로 넘어간 이유도 결국 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이라는 물리 한계를 우회하기 위해서였다.

기억해야 할 결론은 단순하다. 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 "디스크가 느리다"는 막연한 표현을 수치와 구조로 바꿔 주는 개념이며, HDD를 써도 되는 곳과 SSD로 넘어가야 하는 곳을 구분하게 만드는 핵심 판단 잣대다.

- **📢 섹션 요약 비유**: 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 느린 요리사가 아니라, 음식이 컨베이어벨트를 타고 내 자리까지 오는 시간을 뜻한다. 벨트가 본질적 병목이라면, 주방을 조금 개선하는 것보다 아예 서빙 방식 자체를 바꾸는 편이 더 큰 효과를 낸다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/) ([Seek Time](/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/)) | 헤드가 트랙을 찾는 이동 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)으로, 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 함께 [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 랜덤 성능을 결정한다. |
| 디스크 접근 시간 ([Disk Access Time](/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/)) | [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/), 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), [전송 시간](/studynote/01_computer_architecture/08_io_storage_systems/326_transfer_time/)을 합친 전체 응답 시간이다. |
| RPM (Revolutions Per Minute) | 플래터 회전 속도로, 평균 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 직접 계산하게 해 주는 핵심 지표다. |
| [버퍼 캐시](/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/) ([Buffer Cache](/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/)) | 반복 읽기와 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 배치를 통해 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 메모리 계층에서 숨긴다. |
| [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) ([Solid State Drive](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/)) | 기계적 회전이 없어 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 개념 자체를 사실상 제거한 저장장치다. |

### 📈 관련 키워드 및 발전 흐름도

```text
자기 디스크 기반 저장
    |
    v
탐색 시간 (Seek Time) + 회전 지연 (Rotational Latency)
    |
    v
디스크 스케줄링 · 버퍼 캐시 · 배치 쓰기
    |
    v
고RPM HDD (10K/15K) · 엔터프라이즈 최적화
    |
    v
SSD (Solid State Drive) · NVMe (Non-Volatile Memory Express)
```

이 흐름은 기계적 대기를 관리하던 시대에서, 아예 회전 자체를 제거하는 방향으로 스토리지가 진화해 왔음을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 회전 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 빙글빙글 도는 놀이기구에서 내가 탈 말이 내 앞에 올 때까지 기다리는 시간이야.
2. 말이 빨리 돌면 조금 빨리 탈 수 있지만, 너무 빨리 돌리면 기계가 힘들어져.
3. 그래서 컴퓨터는 기다리는 시간을 줄이려고 더 빠른 놀이기구를 만들거나, 아예 돌지 않는 새 장치를 만든 거야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 326 / 803

<- **이전**: [324. 탐색 시간 (Seek Time)](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/)
**다음**: [326. 전송 시간 (Transfer Time)](/studynote/01_computer_architecture/08_io_storage_systems/326_transfer_time/) ->

---
