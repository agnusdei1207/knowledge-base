---
title: "730. RAID 0, 1, 5, 6 성능 신뢰성 (RAID Levels Performance Reliability)"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/)(Redundant [Array](/studynote/08_algorithm_stats/04_datastructure/055_array/) of Independent Disks)는 작고 값싼 여러 개의 디스크를 묶어 하나의 거대한 논리적 디스크처럼 사용함으로써, <strong>용량 확장, <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>(I/O 속도) 향상, <a href="/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/">신뢰성</a>(장애 <a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a>) 확보</strong>라는 세 마리 토끼를 잡기 위한 하드웨어/소프트웨어 스토리지 아키텍처다.
> 2. **레벨별 특성**: [RAID 0](/studynote/02_operating_system/08_storage_and_io_systems/484_raid_0_striping/)([스트라이핑](/studynote/01_computer_architecture/08_io_storage_systems/332_raid_0/))은 속도 올인(안정성 포기), [RAID 1](/studynote/02_operating_system/08_storage_and_io_systems/485_raid_1_mirroring/)([미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/))은 안정성 올인(비용 2배), [RAID 5](/studynote/02_operating_system/08_storage_and_io_systems/487_raid_5_distributed_parity/)([분산 패리티](/studynote/01_computer_architecture/08_io_storage_systems/334_raid_5/))는 3개 이상의 디스크를 써서 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 안정성의 가성비를 맞춘 표준이며, [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 6는 패리티를 2개 두어 디스크 2개가 동시에 죽어도 살아남는 엔터프라이즈의 마지노선이다.
> 3. **가치/한계**: 단일 하드디스크의 I/O 병목을 부숴버린 기적의 기술이지만, 패리티 연산(Write Penalty)으로 인한 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하와 리빌딩(Rebuilding) 시의 극심한 부하 때문에 최근 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 환경에서는 HDFS나 Ceph 같은 소프트웨어 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템으로 대체되는 추세다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong><a href="/studynote/01_computer_architecture/08_io_storage_systems/332_raid_0/">스트라이핑</a> (Striping)</strong>: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 여러 조각(Block)으로 쪼개서 여러 디스크에 흩뿌려 동시에 저장하는 기술. ([성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상)
  - <strong><a href="/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/">미러링</a> (Mirroring)</strong>: 똑같은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 두 개 이상의 디스크에 쌍둥이처럼 똑같이 복사해 두는 기술. ([신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 향상)
  - **패리티 (Parity)**: 디스크가 고장 났을 때, 나머지 디스크에 있는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 패리티(XOR 연산 값)를 조합해 죽은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 살려내는([복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)) 마법의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 조각.

- **필요성 (CPU 속도와 디스크 속도의 엄청난 갭)**:
  - 1980년대, CPU는 미친 듯이 빨라지는데 하드디스크의 물리적 회전 속도는 제자리걸음이었다(I/O [Bottleneck](/studynote/02_operating_system/10_security/617_io_bottleneck/)).
  - 아무리 좋은 CPU를 달아도 하드디스크가 읽어올 때까지 기다리느라 컴퓨터가 느렸다.
  - "비싸고 거대한 디스크 1개를 쓰는 대신, 싸구려 디스크 10개를 달아서 <strong>10명이 동시에 읽고 쓰게(<a href="/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a> 처리)</strong> 만들면 속도가 10배 빨라지지 않을까?" 하는 발상에서 RAID가 탄생했다 (1987년 캘리포니아 버클리 대학).

  - 책 100권을 도서관 서가에 꽂아야 한다.
  - <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/484_raid_0_striping/">RAID 0</a> (<a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 올인)</strong>: 알바생 10명을 고용해 책 10권씩 나눠주고 동시에 꽂으라고 한다. 속도는 10배 빠르지만, 한 명이라도 책을 잃어버리면 전체 시리즈가 망가진다.
  - <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/485_raid_1_mirroring/">RAID 1</a> (안정성 올인)</strong>: 책 100권을 똑같이 2세트 준비해서, 알바생 2명에게 각자 똑같이 100권씩 꽂으라고 한다. 1명이 책을 통째로 불태워도 남은 1명이 멀쩡하니 안전하다. (돈이 2배 듦)
  - <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/487_raid_5_distributed_parity/">RAID 5</a> (가성비)</strong>: 알바생 4명에게 책 33권씩 주는데, 마지막 4번째 알바생에게는 앞의 3명이 무슨 책을 꽂았는지 요약본(패리티)을 적게 한다. 누가 책을 잃어버리면 이 요약본을 보고 잃어버린 책을 다시 써낸다.

- **발전 과정**:
  1. <strong><a href="/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> 스토리지</strong>: 단일 대용량 SLED(Single Large Expensive Disk). 비싸고 고장 나면 끝.
  2. <strong>하드웨어 <a href="/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/">RAID</a></strong>: [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 컨트롤러 카드(칩셋)가 CPU 몰래 캐시 배터리와 함께 묶어줌.
  3. <strong>소프트웨어 <a href="/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/">RAID</a> / <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> FS</strong>: OS(ZFS, LVM)나 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 스토리지(Ceph)가 네트워크를 넘어 RAID의 철학을 구현함.

- **📢 섹션 요약 비유**: 마차 한 대(단일 디스크)를 끌기 위해 집채만 한 [돌연변이](/studynote/04_software_engineering/10_trends_pm_quality/638_mutation_testing_test_case_verification/) 말 한 마리를 키우는 건 비효율적입니다. 조랑말 4마리([RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/))를 밧줄로 잘 묶어서 끌게 하면, 힘도 4배 세지고 한 마리가 지쳐 쓰러져도 마차는 계속 굴러갈 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 주요 [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 레벨 비교 시뮬레이션

| 레벨 | 디스크 개수 | 저장 방식 (예: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) A, B, C, D) | 장애 허용 ([Fault Tolerance](/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/)) | 공간 효율성 |
|:---|:---:|:---|:---:|:---:|
| <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/484_raid_0_striping/">RAID 0</a></strong> | 2개 이상 | Disk 1: `A, C` <br> Disk 2: `B, D` | **0개** (1개 죽으면 다 날아감) | 100% |
| <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/485_raid_1_mirroring/">RAID 1</a></strong> | 2개 이상 (짝수) | Disk 1: `A, B, C, D` <br> Disk 2: `A, B, C, D` | **1개** (절반이 죽어도 생존) | 50% |
| <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/487_raid_5_distributed_parity/">RAID 5</a></strong> | 3개 이상 | Disk 1: `A, D, Parity` <br> Disk 2: `B, Parity, E` <br> Disk 3: `Parity, C, F` | **1개** | $(N-1)/N$ |
| <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/488_raid_6_dual_parity/">RAID 6</a></strong> | 4개 이상 | Disk 1: `A, P1, P2` <br> Disk 2: `B, C, P1` <br> Disk 3: `P1, D, P2` <br> Disk 4: `P2, P1, E` | **2개** | $(N-2)/N$ |

*(※ 패리티 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/): 특정 디스크에만 패리티를 몰아넣는 [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 4의 병목을 막기 위해, 패리티 블록을 모든 디스크에 돌아가며 저장하는 것이 [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 5의 핵심이다.)*

---

### 마법의 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 수식: XOR 패리티 (Parity) 연산

[RAID 5](/studynote/02_operating_system/08_storage_and_io_systems/487_raid_5_distributed_parity/)/6는 어떻게 디스크가 죽었는데 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 살려낼까? 2진수의 마법 **XOR(배타적 논리합)** 덕분이다.

<strong><a href="/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">데이터 [쓰기</a> 및 패리티 생성]</strong>
[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) `A = 0101`, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) `B = 1100`, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) `C = 1010` 이라 하자.
패리티 $P = A \oplus B \oplus C$
$0101 \oplus 1100 \oplus 1010 = \mathbf{0011}$ (이것이 패리티 $P$다. 디스크 4에 저장)

<strong><a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">디스크 B가 불타서 날아갔을 때 ([복구</a>)]</strong>
살아남은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) $A, C, P$를 몽땅 다시 XOR 해본다!
[복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)된 $B = A \oplus C \oplus P$
$0101 \oplus 1010 \oplus 0011 = \mathbf{1100}$ (죽었던 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) $B$가 완벽하게 부활했다!)

<strong>★ <a href="/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/">RAID</a> 5의 Write Penalty (<a href="/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 페널티)</strong>:
여기서 치명적인 단점이 발생한다. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) A를 조금 수정(Update) 하려면 어떻게 해야 할까?
단순히 A만 쓰면 끝이 아니다. **A를 읽고, 기존 P를 읽고, 바뀐 A'로 새로운 P'를 계산해서, A'를 쓰고, P'를 써야 한다! (Read 2번 + Write 2번 = 총 4번의 I/O 발생)**. 이것을 [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 5의 <strong>Write Penalty</strong>라 부르며, DB 서버에서 [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 5를 꺼리는 이유가 된다.

- **📢 섹션 요약 비유**: 퍼즐 10조각을 맞추고, 마지막 11번째 조각(패리티)을 '나머지 10조각의 모양을 다 합친 역방향 모양'으로 깎아냅니다. 중간에 한 조각을 잃어버려도, 남은 조각들을 다 맞춰보면 비어있는 구멍의 모양이 정확히 나오기 때문에 똑같은 조각을 다시 만들어 낼 수 있는 원리입니다.

---

## Ⅲ. 비교 및 연결

### 실무 아키텍처: Nested [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) ([RAID 10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) vs [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 50)

단일 RAID의 한계를 극복하기 위해, 현대 서버는 RAID를 겹쳐 쓴다(Nested).

| 조합명 | 구성 원리 ([Bottom-up](/studynote/04_software_engineering/12_testing_maintenance/403_bottom_up_integration/)) | 특징 및 장단점 | 실무 용도 |
|:---|:---|:---|:---|
| <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/485_raid_1_mirroring/">RAID 1</a>+0 (<a href="/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/">10</a>)</strong>| 디스크 2개씩 거울([RAID 1](/studynote/02_operating_system/08_storage_and_io_systems/485_raid_1_mirroring/))로 묶고, 그 세트들을 다시 [스트라이핑](/studynote/01_computer_architecture/08_io_storage_systems/332_raid_0/)([RAID 0](/studynote/02_operating_system/08_storage_and_io_systems/484_raid_0_striping/))으로 묶음 | <strong><a href="/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 페널티(Parity 연산)가 없어 DB <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 최강.</strong> 단, 디스크 용량이 50% 날아감 (돈이 많이 듦) | [Oracle](/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/), MySQL 등 <strong><a href="/studynote/05_database/06_dw_olap_trends/327_hint_handoff/">OLTP</a> <a href="/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> 메인 스토리지</strong> |
| <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/484_raid_0_striping/">RAID 0</a>+1 (01)</strong>| [스트라이핑](/studynote/01_computer_architecture/08_io_storage_systems/332_raid_0/)(0)으로 묶고, 그걸 통째로 거울(1) 복사 | 한쪽 그룹 디스크 하나 죽으면 그룹 전체가 마비되어 재빌딩 시간이 너무 김 | 거의 쓰이지 않음 |
| <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/487_raid_5_distributed_parity/">RAID 5</a>+0 (50)</strong>| [RAID 5](/studynote/02_operating_system/08_storage_and_io_systems/487_raid_5_distributed_parity/) 세트 여러 개를 모아 다시 [스트라이핑](/studynote/01_computer_architecture/08_io_storage_systems/332_raid_0/)(0) | [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 5보다 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 좋고 용량 가성비도 훌륭함 | 빅데이터 저장소, 스트리밍 서버, [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 서버 |

### 과목 융합 관점

- <strong><a href="/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> (DB)</strong>: DBA에게 "DB 스토리지로 [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 5를 써도 될까요?"라고 물으면 쌍욕을 먹는다. [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 발생할 때마다 [Redo](/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/)/[Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/) 로그를 디스크에 미친 듯이 쏟아내는데, [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 5의 Write Penalty(1 Write -> 4 I/O)가 걸리면 DB [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 1/4로 토막 나기 때문이다. DB는 무조건 무식하게 비싸고 빠른 <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/">RAID 10</a></strong>이 진리다.
- <strong>클라우드 / <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 시스템 (Cloud)</strong>: AWS S3나 Ceph 같은 오브젝트 스토리지는 물리적 [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 컨트롤러를 쓰지 않는다. 대신 서버 3대에 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쪼개어 패리티를 네트워크 너머로 저장하는 <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/681_erasure_coding/">Erasure Coding</a> (이레이저 코딩)</strong> 기법을 쓴다. RAID의 소프트웨어적/[분산](/studynote/08_algorithm_stats/08_stats/136_variance/)적 진화형으로, [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 1개가 통째로 불타도 살아남는다.

- **📢 섹션 요약 비유**: [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 5는 가성비가 좋아서 '일반 승용차'에 적합하지만 'F1 레이싱카(DB 서버)'에 달면 무거운 짐(패리티) 때문에 꼴등을 합니다. 레이싱카에는 돈이 두 배로 들더라도 부품을 무식하게 2배로 때려 박은 [RAID 10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 엔진을 달아야 합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — <a href="/studynote/02_operating_system/08_storage_and_io_systems/487_raid_5_distributed_parity/">RAID 5</a> 리빌딩(Rebuilding) 도중의 2차 붕괴 (URE 재앙)</strong>: 8TB 디스크 5개로 [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 5를 구성한 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 서버. 디스크 1개가 고장 나서 새 디스크로 갈아 끼우고 리빌드([복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/))를 시작했다. 리빌드 도중 또 다른 디스크가 뻗으면서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 통째로 증발했다.
   - **원인 분석**: 8TB짜리 4개를 100% 읽어들여 패리티 연산을 하려면 디스크 풀(Full) 부하 상태로 2~3일이 걸린다. 이 미친듯한 부하(Stress)를 견디지 못하고 평소 수명이 간당간당하던 다른 늙은 디스크 하나가 리빌딩 도중에 뻗어버린 것이다 (Unrecoverable Read Error, URE). [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 5는 디스크 1개 고장만 버티므로, 2개가 죽는 순간 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) 전체가 산산조각 난다.
   - **대응 (기술사적 가이드)**: 디스크 용량이 테라바이트(TB) 단위로 커진 현대 환경에서 <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/">RAID</a> 5는 사실상 사망 선고</strong>를 받았다. 용량이 큰 엔터프라이즈 환경에서는 디스크 2개가 동시에 죽어도 버틸 수 있는 <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/488_raid_6_dual_parity/">RAID 6</a> (패리티 2개)</strong> 구조나, ZFS의 [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/)-Z2/Z3 같은 차세대 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템으로 무조건 아키텍처를 교체해야 한다.

2. <strong>시나리오 — 하드웨어 <a href="/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/">RAID</a> 카드 캐시 배터리(<a href="/studynote/01_computer_architecture/15_advanced_topics/688_bbu/">BBU</a>) 방전 사고</strong>: 5천만 원짜리 물리 서버가 정전으로 꺼졌다가 켜졌는데, [DBMS](/studynote/05_database/04_transactions_concurrency/502_dbms/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 깨져서 DB가 올라오지 않음.
   - **원인 분석**: 고성능 하드웨어 [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 컨트롤러는 느린 디스크 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 덮기 위해, 자체적으로 <strong>수 GB 크기의 Write Cache (RAM)</strong>를 갖고 있다. OS가 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 써!"라고 하면, 디스크에 안 쓰고 램 캐시에만 담아둔 뒤 "다 썼다!"고 OS에 사기를 친다. 그런데 정전이 나서 이 캐시 램의 전원이 날아갔고, OS는 썼다고 믿었던 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 디스크에 없으니 DB가 박살 났다.
   - **아키텍처 적용**: 하드웨어 RAID를 쓸 때는 컨트롤러에 반드시 <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/688_bbu/">BBU</a> (Battery <a href="/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/">Backup</a> Unit) 또는 FBWC (Flash-Based Write Cache)</strong>가 장착되어 있고 배터리 상태가 정상인지 모니터링해야 한다. 정전이 나도 배터리로 캐시 메모리의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 버티다가 다시 전기가 들어오면 디스크로 Flush 해주는 최후의 생명줄이다.

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 엔터프라이즈 스토리지 RAID 아키텍처 선정 플로우             |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [서버 구매 시 용도에 맞는 디스크 구성(RAID 레벨)을 설계해야 함]              |
  |                |                                                  |
  |                v                                                  |
  |      절대 데이터가 날아가면 안 되면서, Write(쓰기)가 미친 듯이 일어나는가?      |
  |      (예: 금융권 DBMS, 초고속 결제 트랜잭션)                            |
  |          +- 예 ------> [RAID 10 (1+0) 강제 선택]                      |
  |          |            비용은 비싸지만 패리티 연산 페널티가 없어 IOPS 방어 완벽. |
  |          +- 아니오 (Read 위주거나, 데이터 유실이 큰 문제 없는 서버임)        |
  |                |                                                  |
  |                v                                                  |
  |      서버의 용도가 단순한 캐시(Cache), 휘발성 데이터 저장, 혹은 임시 렌더링인가?|
  |          +- 예 ------> [RAID 0 (스트라이핑) 선택]                      |
  |          |            성능과 용량 극대화. 죽으면 그냥 서버 버리고 다시 띄움.     |
  |          +- 아니오 (대용량의 파일, 아카이빙, 백업 데이터를 영구 보관해야 함)  |
  |                |                                                  |
  |                v                                                  |
  |      [RAID 6 (패리티 2개) 또는 RAID 50 선택]                           |
  |      - RAID 5는 요즘 같은 10TB+ 디스크 시대에 리빌딩 중 2차 붕괴 위험이 높아 |
  |        엔터프라이즈 표준에서 탈락했음을 유의할 것.                          |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 클라우드 엔지니어가 베어메탈 서버를 세팅할 때 제일 처음 맞닥뜨리는 화면이 [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) BIOS 화면이다. 이때 비용을 아끼겠다고 DB 서버를 [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 5로 묶는 순간 그 프로젝트는 오픈 첫날 DB I/O 병목으로 망하게 된다. 아키텍트는 하드웨어 비용(Disk $)과 소프트웨어 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)(TPS)의 환율을 계산하여 자본주의적인 최적의 밸런스를 맞춰야 한다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong>소프트웨어 <a href="/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/">RAID</a> (LVM / ZFS / mdadm)</strong>: 옛날엔 수백만 원짜리 [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 카드가 필수였지만, 요즘은 CPU 코어가 너무 남아돌아서(64코어) 패리티 계산쯤은 CPU가 소프트웨어로 해버려도 전혀 무리가 없다. AWS EBS나 K8s 로컬 스토리지 볼륨들이 하드웨어가 아닌 순수 OS 소프트웨어 RAID로 묶여서 완벽하게 동작하고 있다는 사실([Software Defined Storage](/studynote/01_computer_architecture/15_advanced_topics/632_sds/))을 인지하고 있는가?

- **📢 섹션 요약 비유**: 얇은 유리판(디스크) 한 장은 쉽게 깨지지만, 유리판 여러 장을 겹치고 그 사이에 충격 방지 필름(패리티)을 넣으면 방탄유리([RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/))가 됩니다. 방탄유리가 두꺼울수록([RAID 6](/studynote/02_operating_system/08_storage_and_io_systems/488_raid_6_dual_parity/)) 안전하지만, 그만큼 무거워서 자동차(서버) 속도는 떨어질 수밖에 없습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 단일 거대 디스크 (SLED) | 다중 디스크 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) ([RAID 10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) / 5) | 개선 효과 |
|:---|:---|:---|:---|
| <strong>정량 (I/O <a href="/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">대역폭</a>)</strong> | 디스크 1개의 스핀들 모터 속도 한계 | N개의 디스크가 동시 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) R/W | 디스크 I/O 속도 선형적(N배) 증가 |
| <strong>정성 (무중단 <a href="/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a>)</strong>| 디스크 뻑나면 서버 즉시 다운 | <strong>고장 나도 OS 모르게(투명하게) <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 유지</strong>| 24/365 엔터프라이즈 [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/)(99.99%) 달성 |
| <strong>정량 (<a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 시간)</strong> | [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 테이프에서 수동 복원 (수 일) | 핫스왑(Hot-swap) 후 자동 리빌딩 (수 시간)| 운영자의 수면권 보장 및 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 다운타임 제로 |

### 미래 전망
- <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/">NVMe</a> RAID의 한계와 VROC</strong>: [NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 4개를 RAID로 묶으려니, 이제는 디스크가 너무 빨라서 하드웨어 [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 컨트롤러 칩셋 자체가 병목([Bottleneck](/studynote/02_operating_system/10_security/617_io_bottleneck/))이 되어 속도를 깎아 먹는다. 그래서 인텔은 <strong>VROC (Virtual <a href="/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/">RAID</a> on CPU)</strong> 기술을 내놓아, 별도 칩셋 없이 메인 CPU와 [PCIe](/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) 버스에 직접 [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 연산을 박아버리는 괴물 같은 아키텍처로 진화하고 있다.
- **Erasure Coding의 천하 통일**: 랙(Rack)과 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)를 넘나드는 클라우드에서는 디스크 묶음([RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/))의 개념이 무의미하다. $K$개의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 조각을 $N$개(예: 8+4)로 뻥튀기 암호화([Erasure Coding](/studynote/01_computer_architecture/15_advanced_topics/681_erasure_coding/))하여 클라우드 노드 여기저기에 뿌려두면, 노드 4대가 동시에 벼락을 맞아도 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 살려내는 극강의 수학적 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 스토리지 아키텍처가 미래를 지배하고 있다.

### 결론
[RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 아키텍처는 "싸고 불안정한 것들을 모아, 비싸고 완벽한 하나를 창조한다"는 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅의 가장 위대하고 철학적인 1세대 산물이다. 느린 회전 속도를 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성(Striping)으로 극복하고, 언제든 고장 날 수 있는 기계적 한계를 정보의 중복(Mirroring/Parity)으로 방어해 냈다. 클라우드와 소프트웨어 정의 스토리지([SDS](/studynote/01_computer_architecture/15_advanced_topics/632_sds/))의 거대한 파도 속에서 하드웨어 칩셋으로서의 RAID는 서서히 모습을 감추고 있지만, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쪼개고 XOR 연산을 통해 죽은 목숨을 살려내는 그 경이로운 뼈대([Algorithm](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))만큼은 영원히 인류의 디지털 유산을 지키는 방패로 남을 것이다.

- **📢 섹션 요약 비유**: 나무젓가락 1개(단일 디스크)는 쉽게 부러지지만, 10개를 묶으면([RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/)) 부러지지 않습니다. 심지어 1개가 썩어서 부러지더라도, 남은 9개를 보고 부러진 1개의 원래 길이를 깎아내어 새로 채워 넣는 기적의 묶음 기술입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/) [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 회전 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [SSTF](/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/) 기아 현상 ([가운데 편중](/studynote/02_operating_system/11_exam_summary/729_sstf_starvation_middle_bias/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [SSD FTL](/studynote/02_operating_system/11_exam_summary/731_ssd_ftl_flash_translation_layer/) ([Flash Translation Layer](/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [가비지 컬렉션](/studynote/02_operating_system/06_memory_management/380_garbage_collection/) 블록 지우기 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[SSTF 기아 현상 (가운데 편중)]
    |
    v
[RAID 0, 1, 5, 6 성능 신뢰성 (RAID Levels Performance Reliability)]
    |
    +---> [SSD FTL (Flash Translation Layer)]
    +---> [가비지 컬렉션 블록 지우기]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 철수는 보물 지도([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 1장을 잃어버릴까 봐 너무 무서웠어요. (단일 디스크의 공포)
2. 그래서 지도를 반으로 쫙 찢은 다음, 왼쪽 반쪽은 영희한테, 오른쪽 반쪽은 민수한테 맡겼어요. ([RAID 0](/studynote/02_operating_system/08_storage_and_io_systems/484_raid_0_striping/): 이렇게 하면 지도를 2배 빨리 읽을 수 있지만, 한 명이라도 잃어버리면 지도를 못 봐요!)
3. 그래서 지도를 1장 더 똑같이 복사([RAID 1](/studynote/02_operating_system/08_storage_and_io_systems/485_raid_1_mirroring/))하거나, 영희와 민수가 가진 지도의 글자를 섞은 '비밀 요약본(패리티, [RAID 5](/studynote/02_operating_system/08_storage_and_io_systems/487_raid_5_distributed_parity/))'을 짱구에게 맡겼어요! 이제 영희가 지도를 잃어버려도 짱구의 요약본을 보고 똑같이 그려낼 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 730 / 800

<- **이전**: [729. SSTF 기아 현상 (가운데 편중) (Sstf Starvation Middle Bias)](/studynote/02_operating_system/11_exam_summary/729_sstf_starvation_middle_bias/)
**다음**: [731. SSD FTL (Flash Translation Layer)](/studynote/02_operating_system/11_exam_summary/731_ssd_ftl_flash_translation_layer/) ->

---
