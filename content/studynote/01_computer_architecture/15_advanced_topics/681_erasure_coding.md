+++
title = "681. Erasure Coding (삭제 코딩) HW 연산"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: EC (Erasure Coding)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 여러 조각과 패리티 조각으로 분해해, 일부 장치가 사라져도 수학적으로 원본을 복원하는 저장 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 기술이다.
> 2. **가치**: 3중 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)보다 훨씬 적은 용량 오버헤드로 같은 수준의 장애 허용성을 얻을 수 있어, 대규모 스토리지의 비용 구조를 크게 낮춘다.
> 3. **판단 포인트**: EC가 절감한 디스크 비용만큼 인코딩·[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 연산, 네트워크 재구성 트래픽, 작은 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 감당할 수 있는 HW (Hardware) 가속 체계를 갖췄는지가 실무 성패를 가른다.

---

## Ⅰ. 개요 및 필요성

EC는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 `k`개의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 조각과 `m`개의 패리티 조각으로 나누어 저장하고, 전체 중 최대 `m`개 손실까지 복원하도록 설계한 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 방식이다. 가장 단순한 대안인 3중 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)는 구현이 쉽지만, 12 테라바이트(TB) 유효 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 지키려면 36 TB의 물리 용량이 필요하다. 페타바이트(PB)급 객체 스토리지나 분석 클러스터로 규모가 커지면, 이 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 오버헤드는 디스크 구매비뿐 아니라 전력, 랙 공간, 재동기화 시간까지 함께 키운다.

그래서 대형 스토리지는 “같은 안전성을 더 적은 디스크로 얻는 방법”을 찾았고, 그 답이 EC였다. 예를 들어 `8+2` 구성은 10조각 중 2조각 손실을 허용하면서 저장 효율이 80%다. 반면 3중 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)의 저장 효율은 약 33%에 머무르므로, 장애 허용성을 유지하면서도 훨씬 높은 밀도를 확보할 수 있다.

하지만 EC는 디스크를 아끼는 대신 계산을 더 쓰는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다. 즉, “저장은 싸게, [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)는 똑똑하게”라는 철학이므로, 연산 자원이 부족한 환경에서는 오히려 병목이 될 수 있다.

- **📢 섹션 요약 비유**: 같은 계약서를 세 군데 복사해 보관하는 대신, 원본 조각 몇 개와 복원 공식을 따로 보관해 두는 방식이 EC다. 종이는 덜 쓰지만, 잃어버렸을 때는 계산기를 꺼내 다시 맞춰야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

대표적인 구현인 RS (Reed-Solomon) 코드는 GF (Galois Field) 위의 행렬 연산으로 패리티를 만든다. 단순한 XOR (Exclusive OR) 패리티에 가까운 [RAID](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) (Redundant [Array](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) of Independent Disks)보다 일반성이 높아, 두 개 이상 조각 손실도 복원할 수 있다. 대신 패리티 생성과 복원 시 곱셈·역행렬 계산이 필요하므로, 연산량이 갑자기 커진다.

아래 그림은 EC의 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 경로와 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 경로를 함께 보여준다.

```text
┌──────────────────────────────────────────────────────────────────┐
│ EC write / rebuild pipeline                                     │
├──────────────────────────────────────────────────────────────────┤
│ Write path                                                      │
│   User data -> [Stripe Buffer] -> [RS Encoder] -> D0 D1 D2 D3  │
│                                               \-> P0 P1        │
│                                                  │             │
│                                                  └-> 6 devices │
│                                                                  │
│ Rebuild path (if D2 is lost)                                     │
│   D0 D1 D3 P0 P1 -> [GF Decoder] -> rebuilt D2                   │
└──────────────────────────────────────────────────────────────────┘
```

이 구조에서 핵심은 스트라이프 단위다. 컨트롤러는 먼저 같은 스트라이프에 들어갈 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 조각을 모은 뒤 패리티를 계산하고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 서로 다른 디스크나 노드에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 기록한다. 장애가 나면 남은 조각들을 다시 읽어 디코더에 넣고, 사라진 조각만 재생성한다.

| 단계 | 무엇을 하는가 | 병목 포인트 |
| :--- | :--- | :--- |
| 스트라이프 [버퍼링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/454_buffering/) | 같은 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 그룹으로 묶을 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 정렬 | 작은 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 많으면 버퍼 대기 증가 |
| 패리티 인코딩 | RS 행렬로 패리티 계산 | 벡터 연산량 증가 |
| [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 기록 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 패리티를 다른 실패 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 저장 | 네트워크와 디스크 동시 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |
| 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | 살아남은 조각을 읽어 손실 조각 재구성 | 읽기 [팬인](/knowledge-base/studynote/04_software_engineering/04_testing_quality/197_fan_in_fan_out/)([Fan-in](/knowledge-base/studynote/04_software_engineering/04_testing_quality/197_fan_in_fan_out/))과 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간 증가 |

그래서 실무 제품은 보통 [SIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/) (Single [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Multiple [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 벡터 명령, ISA-L (Intelligent Storage Acceleration [Library](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)), 전용 [RAID](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 엔진, 또는 [DPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/436_dpu/) ([Data Processing Unit](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/229_dpu_ipu_infrastructure_accelerator_offloading/)) [오프로딩](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)으로 인코딩·디코딩을 가속한다. 즉 EC는 소프트웨어 알고리즘이지만, 실제 성능은 하드웨어 파이프라인 품질에 강하게 좌우된다.

- **📢 섹션 요약 비유**: 여러 퍼즐 조각으로 원본 그림을 만들고, 여기에 “잃어버린 조각을 계산해 내는 [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/) 카드”를 추가로 넣어 두는 셈이다. [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/) 카드를 만드는 과정이 복잡해서 손빠른 조수나 전용 기계가 있으면 훨씬 유리하다.

---

## Ⅲ. 비교 및 연결

EC를 이해할 때는 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)와 [RAID](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 계열 패리티를 함께 비교해야 경계가 분명해진다. [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)는 단순하고 읽기 성능이 좋지만 용량 비효율이 크다. [RAID 6](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/488_raid_6_dual_parity/) (Redundant [Array](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) of Independent Disks 6)은 한 장비 내부 디스크 이중 고장에 강하지만, 노드·랙 단위 장애까지 넓히려면 별도 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 설계가 필요하다. EC는 이 패리티 개념을 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 스토리지 전체로 확장한 형태에 가깝다.

| 구분 | 3중 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | [RAID 6](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/488_raid_6_dual_parity/) | EC |
| :--- | :--- | :--- | :--- |
| [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 방식 | 동일 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 3벌 저장 | [이중 패리티](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/335_raid_6/) | 다중 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 조각 + 패리티 |
| 저장 효율 | 낮음 | 중간 | 높음 |
| 장애 범위 | 노드 단위 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)에 유리 | 단일 어레이 내부에 최적 | 노드·랙 단위 확장 용이 |
| [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 특성 | 단순 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | 패리티 계산 필요 | 인코딩·[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 필요 |
| 적합한 부하 | 뜨거운 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 빠른 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | 로컬 스토리지 | 대용량 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장, 아카이브 |

[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템과 객체 스토리지는 이 차이를 적극 활용한다. 자주 갱신되는 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)나 소량 랜덤 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 구간은 여전히 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)를 유지하고, 크고 차가운 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록은 EC로 내려 비용을 줄이는 식이다. 즉 EC는 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)를 완전히 대체하기보다, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 온도와 접근 패턴에 따라 섞어 쓰는 기술이다.

- **📢 섹션 요약 비유**: [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)는 같은 우산을 세 개 사 두는 방식이고, RAID는 한 집 안에서 우산 살을 보강하는 방식이다. EC는 동네 여러 창고에 우산 부품과 수리 설명서를 나눠 둬서, 창고 몇 곳이 망가져도 다시 조립하는 방식에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

EC는 대용량 객체 스토리지, [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 저장소, 분석 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레이크처럼 “용량이 크고 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 패턴이 비교적 순차적”인 환경에서 특히 효과적이다. 반대로 짧은 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 시간이 중요한 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 서버, 작은 랜덤 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 많은 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 핫 티어에서는 인코딩 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시 읽기 증폭이 부담이 된다.

설계 시에는 단순히 `4+2`, `8+2`, `10+4` 같은 숫자만 고를 것이 아니라, 장애 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 배치까지 함께 봐야 한다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 조각과 패리티 조각이 같은 랙에 몰리면 랙 장애를 버티지 못하고, [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 대역폭이 부족하면 장애 창구가 길어져 두 번째 장애에 취약해진다. 또한 작은 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 많은 시스템에서는 스트라이프 전체를 읽고 다시 계산하는 읽기-수정-[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 패턴 때문에 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 커질 수 있다.

실무 체크 포인트는 명확하다. 첫째, 인코딩 경로에 충분한 가속 장치가 있는가. 둘째, 열화 모드에서 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간과 사용자 읽기 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 허용 범위 안인가. 셋째, 스크러빙과 재빌드가 백그라운드에서 돌아도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 대역폭을 잠식하지 않는가. 이 세 가지를 확인하지 않으면 “용량은 아꼈는데 장애 때 더 위험한 시스템”이 된다.

- **📢 섹션 요약 비유**: EC 도입은 창고 임대료를 줄이는 대신, 분실 시 재조립팀을 더 똑똑하게 꾸리는 결정이다. 평소에는 절약이 되지만, 사고가 났을 때 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)팀이 느리면 절약한 돈보다 손해가 더 커질 수 있다.

---

## Ⅴ. 기대효과 및 결론

EC의 가장 큰 효과는 저장 효율 향상이다. 같은 내구성을 더 적은 디스크로 제공하므로, 대규모 시스템일수록 절감 효과가 누적된다. 여기에 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 수 감소로 전력과 랙 공간도 함께 줄어, 총소유비용 관점에서 매력적이다.

반면 한계도 분명하다. 패리티 계산과 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [팬인](/knowledge-base/studynote/04_software_engineering/04_testing_quality/197_fan_in_fan_out/) 때문에 연산 자원과 네트워크 자원이 부족하면 성능이 쉽게 흔들린다. 그래서 최근에는 LRC (Local Reconstruction [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/))처럼 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시 읽어야 할 조각 수를 줄이는 변형 코드와, [DPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/436_dpu/) 기반 [오프로딩](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)처럼 계산을 저장 경로 밖으로 밀어내는 방향이 함께 발전하고 있다.

결국 EC는 “디스크 대신 수학을 쓰는 저장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)”으로 기억하면 된다. 저장 비용을 줄이는 기술이지만, 진짜 경쟁력은 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)를 빠르고 예측 가능하게 만드는 아키텍처 완성도에서 나온다.

- **📢 섹션 요약 비유**: EC는 창고를 덜 빌리는 대신 수리 매뉴얼을 더 정교하게 만드는 선택이다. 공간 절약만 보고 도입하면 반쪽짜리고, 사고 났을 때 빨리 복원할 체계까지 갖춰야 진짜 가치가 난다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 3중 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | 구현은 단순하지만 용량 오버헤드가 가장 큰 비교 대상 |
| RS (Reed-Solomon) | 범용적인 EC 구현 방식으로 다중 조각 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)를 지원 |
| GF (Galois Field) | 패리티 인코딩과 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 연산이 수행되는 수학적 기반 |
| LRC (Local Reconstruction [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/)) | 전체 스트라이프 대신 국소 조각만 읽어 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 비용을 줄이는 확장 기법 |
| [DPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/436_dpu/) ([Data Processing Unit](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/229_dpu_ipu_infrastructure_accelerator_offloading/)) | 인코딩·디코딩 부하를 호스트 밖으로 [오프로딩](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)하는 가속 장치 |

### 📈 관련 키워드 및 발전 흐름도

```text
3중 복제
    │  용량 낭비 문제
    ▼
RAID 패리티
    │  로컬 디스크 보호 확장
    ▼
EC (Erasure Coding)
    │  복구 트래픽 최적화
    ▼
LRC (Local Reconstruction Code)
    │  계산 오프로딩
    ▼
DPU 기반 가속 저장 경로
```

이 흐름은 “단순 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) → 패리티 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) → [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 코드화 → [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 최적화 → 하드웨어 [오프로딩](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)”으로 발전하는 저장 기술의 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 큰 그림을 여러 조각으로 나눠 친구들에게 맡기고, 잃어버린 조각을 찾는 비밀 [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)도 같이 나눠 주는 게 EC예요.
2. 친구 몇 명이 조각을 잃어버려도 남은 조각과 [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)로 다시 그림을 만들 수 있어요.
3. 대신 [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)를 만들고 맞추는 계산이 어려워서, 똑똑한 계산기나 빠른 도우미가 필요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 682 / 803

← **이전**: [680. HDFS (Hadoop Distributed File System)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/680_hdfs/)
**다음**: [682. 데이터 중복 제거 (Data Deduplication)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/682_data_deduplication/) →

---
