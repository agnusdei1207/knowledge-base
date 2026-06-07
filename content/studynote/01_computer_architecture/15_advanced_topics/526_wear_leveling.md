---
title: "Wear Leveling"
date: "2026-05-08"
tags:
  - "studynote-computer-architecture"
weight: 526
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/) ([Wear Leveling](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/))는 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)·소거 횟수가 제한된 비휘발성 메모리에서 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 주소를 계속 다른 물리 블록으로 재매핑해, 가장 먼저 닳는 블록의 등장을 늦추는 수명 관리 기법이다.
> 2. **가치**: 사용자에게는 연속 주소 공간처럼 보이지만, 내부적으로는 컨트롤러가 핫 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 [콜드 데이터](/studynote/01_computer_architecture/15_advanced_topics/676_cold_data_archiving/)를 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 배치해 [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) ([Solid State Drive](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/)) 수명과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보존 신뢰성을 지켜 준다.
> 3. **판단 포인트**: 수명을 크게 늘리려면 정적 이동이 필요하지만, 그만큼 [WAF](/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/) ([Write Amplification](/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/) Factor)와 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 커지므로 워크로드의 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 편향, 여유 블록, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 목표를 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

[마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)는 비휘발성 메모리의 수명이 "전체 평균"이 아니라 "가장 먼저 닳은 물리 블록"에 의해 결정된다는 문제에서 출발한다. 특히 NAND 플래시 ([NAND Flash](/studynote/01_computer_architecture/06_memory_hierarchy_cache/257_nand_flash/))는 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 단위로 쓰고 블록 단위로 지우며, 이때 산화막이 반복적으로 스트레스를 받아 P/E (Program/Erase) 사이클 한계에 가까워진다. 일부 [SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/) (Storage Class Memory) 계열도 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 내구도 한계가 있으므로, 주소를 고정된 셀에 그대로 매핑하면 특정 영역만 먼저 죽는다.

문제는 실제 워크로드가 균등하지 않다는 점이다. [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/), 저널, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 인덱스처럼 자주 갱신되는 영역은 극단적인 핫스폿이 되기 쉽다. 이때 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 주소를 물리 주소에 고정하면 장치 전체 용량은 멀쩡해도 몇 개 블록의 조기 마모 때문에 전체 신뢰성이 붕괴한다. 결국 [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)는 "모든 셀을 오래 쓰는 기술"이 아니라, <strong><a href="/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 편향을 흡수해 장치 수명을 예측 가능하게 만드는 기술</strong>이다.

이 그림은 왜 평균 여유 수명이 아니라 최악 블록이 장치 운명을 좌우하는지를 보여준다.

```text
+----------------------------------------------------------------------------+
|           마모 평준화가 없으면 수명은 평균이 아니라 최악 블록이 결정       |
+----------------------------------------------------------------------------+
| LBA 0~15  (메타데이터) ----------------> Block 03 : P/E 2,980               |
| LBA 16~31 (저널)     ----------------> Block 04 : P/E 2,910               |
| LBA 32~95 (거의 안 변함) ------------> Block 18 : P/E   27                |
| LBA 96~... (거의 안 변함) -----------> Block 19 : P/E   14                |
+----------------------------------------------------------------------------+
| 전체 여유 공간이 많아도 Block 03/04가 먼저 소진되면 장치 신뢰성이 흔들린다. |
+----------------------------------------------------------------------------+
```

즉 [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)의 목표는 "많이 남은 블록을 더 쓰게 하고, 많이 닳은 블록을 쉬게 한다"가 아니다. 오히려 장치 전체가 비슷한 속도로 늙도록 만들어, 특정 블록의 조기 사망이 전체 장애로 번지지 않게 하는 데 있다.

- **📢 섹션 요약 비유**: [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)는 자동차 타이어 위치 교환과 같다. 앞바퀴만 계속 닳게 두면 차 전체를 못 쓰게 되지만, 주기적으로 앞뒤를 바꾸면 네 바퀴가 비슷하게 늙어 차를 더 오래 탈 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

실제 구현은 보통 저장장치 컨트롤러 내부의 [FTL](/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/) ([Flash Translation Layer](/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/))이 맡는다. FTL은 LBA (Logical Block Address)를 PBA (Physical Block Address)로 바꾸는 매핑 테이블을 갖고 있으며, 여기에 erase count 테이블, free block pool, spare block, bad block 목록을 함께 관리한다. 즉 [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)는 단독 기능이 아니라, 주소 변환과 공간 회수 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 위에 올라탄 수명 제어 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이다.

[마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)는 크게 동적 방식과 정적 방식으로 나뉜다. 동적 방식은 새로 들어오는 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 가장 덜 닳은 가용 블록 쪽으로 보낸다. 정적 방식은 여기에 한 걸음 더 나아가, 거의 변하지 않는 [콜드 데이터](/studynote/01_computer_architecture/15_advanced_topics/676_cold_data_archiving/)를 낮은 마모 블록에서 더 많이 닳은 블록으로 일부러 옮겨 와서, "새것 같은 블록"을 미래의 핫 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 쓰도록 비워 둔다.

| 구분 | 동적 [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/) | 정적 [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/) |
| :--- | :--- | :--- |
| 대상 | 새로 쓰이는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 이미 저장된 [콜드 데이터](/studynote/01_computer_architecture/15_advanced_topics/676_cold_data_archiving/)까지 포함 |
| 장점 | 구현 단순, [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 오버헤드 작음 | 전체 블록의 수명 편차를 더 작게 만듦 |
| 약점 | [콜드 데이터](/studynote/01_computer_architecture/15_advanced_topics/676_cold_data_archiving/)가 차지한 저마모 블록은 방치될 수 있음 | 내부 복사와 erase가 늘어 [WAF](/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/) 상승 |
| 적합한 환경 | 모바일·클라이언트 중심 | 엔터프라이즈·고신뢰성 중심 |

이 그림은 [FTL](/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/) 내부에서 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)와 정적 이동이 어떻게 이어지는지 보여준다.

```text
+----------------------------------------------------------------------------+
|                   FTL 안에서의 마모 평준화 동작 흐름                       |
+----------------------------------------------------------------------------+
| Host Write (LBA 42)                                                       |
|        |                                                                  |
|        v                                                                  |
| [FTL] -- old PBA invalid 표시 ---> 낮은 erase count free block 선택        |
|   |                                                                       |
|   +- mapping table: LBA42 -> PBA901 갱신                                   |
|   +- erase count / wear histogram 갱신                                    |
|   +- background thread: wear gap 확인                                     |
|                                   |                                       |
|                                   +- 임계치 초과 -> cold data migration    |
|                                                      v                     |
|                                        저마모 블록을 future hot write용 확보|
+----------------------------------------------------------------------------+
```

이때 핵심 비용 지표가 WAF다. `WAF = 실제 낸드에 기록된 데이터량 / 호스트가 요청한 데이터량`이므로, 정적 [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)가 과도하면 수명을 늘리려다 오히려 내부 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 폭증시키는 역설이 생긴다. 따라서 좋은 설계는 단순히 wear gap을 줄이는 것이 아니라, <strong>wear gap 감소량 대비 추가 <a href="/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 비용이 합리적인가</strong>를 계속 계산하는 쪽에 가깝다.

- **📢 섹션 요약 비유**: 동적 방식은 손님이 들어올 때마다 가장 한산한 테이블에 앉히는 식이고, 정적 방식은 오래 앉아 있는 손님까지 일부 재배치해서 가게 전체 좌석이 골고루 쓰이게 만드는 식이다.

---

## Ⅲ. 비교 및 연결

[마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)는 흔히 [가비지 컬렉션](/studynote/02_operating_system/06_memory_management/380_garbage_collection/)과 혼동되지만 목적이 다르다. [가비지 컬렉션](/studynote/02_operating_system/06_memory_management/380_garbage_collection/)은 무효 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 모아 free block을 만드는 공간 확보 작업이고, [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)는 블록 간 소거 횟수 편차를 줄이는 수명 균등화 작업이다. 실제 장치에서는 둘이 긴밀히 엮여 움직이지만, 설계 의도는 분리해서 이해해야 한다.

| 기능 | 핵심 목적 | [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) | [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)와의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
| :--- | :--- | :--- | :--- |
| [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/) | 블록 수명 편차 감소 | wear gap 확대 | 수명 예측 가능성 확보 |
| [가비지 컬렉션](/studynote/02_operating_system/06_memory_management/380_garbage_collection/) ([Garbage Collection](/studynote/02_operating_system/06_memory_management/380_garbage_collection/), GC) | free block 회수 | 빈 블록 부족 | 수행 시 어떤 블록을 고를지 WL [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)과 연계 |
| 배드 블록 관리 | 고장 블록 격리 | 오류 정정 코드 (Error Correcting [Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/), [ECC](/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/)) 실패·P/E 한계 초과 | WL이 실패한 뒤의 최후 방어선 |
| TRIM 명령 | 무효 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [힌트](/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/) 제공 | 운영체제의 삭제 통지 | 불필요한 이동을 줄여 WL과 GC를 돕는다 |

또한 [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)는 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 특성에 따라 구현 방식이 달라진다. NAND 플래시는 [erase-before-write](/studynote/02_operating_system/08_storage_and_io_systems/476_flash_memory_limitations/) 제약이 강해서 블록 단위 이동과 GC가 복잡하지만, SCM은 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 또는 [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) 단위 갱신이 가능해 더 세밀한 wear [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)이 가능하다. 그럼에도 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 편향을 완화해야 한다는 본질은 같으므로, [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)가 달라도 "핫 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 특정 셀을 빨리 늙게 만든다"는 문제 구조는 유지된다.

운영체제와의 연결도 중요하다. [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 삭제 정보를 컨트롤러가 빨리 알수록 불필요한 [콜드 데이터](/studynote/01_computer_architecture/15_advanced_topics/676_cold_data_archiving/) 이동이 줄고, Over-Provisioning (OP) 영역이 넉넉할수록 wear leveling은 더 적은 충돌로 실행된다. 즉 수명 관리는 [펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/) 알고리즘만의 문제가 아니라, 호스트 [힌트](/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)와 여유 공간 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)까지 합친 시스템 문제다.

- **📢 섹션 요약 비유**: [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)가 운동장 바닥이 골고루 닳게 학생들을 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)시키는 일이라면, [가비지 컬렉션](/studynote/02_operating_system/06_memory_management/380_garbage_collection/)은 운동장에 흩어진 쓰레기를 치워 빈 공간을 만드는 일이다. 둘 다 학교 운영에 필요하지만 맡은 역할은 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "어떤 장치에 얼마만큼 공격적으로 적용할 것인가"가 핵심 판단이다. 엔터프라이즈 SSD는 긴 보증 수명과 Drive Writes Per Day (DWPD) 목표가 중요하므로 정적 [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)와 큰 OP 영역을 선호한다. 반대로 모바일 기기나 임베디드 장치는 전력과 즉시 응답성이 더 중요해, 동적 방식을 기본으로 하고 정적 이동은 유휴 시간에만 제한적으로 수행하는 편이 유리하다.

또한 수명만 보고 공격적으로 블록을 옮기면 운영 품질이 나빠진다. 내부 복사가 늘면 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간이 튀고, 전원 장애 시 매핑 정보가 꼬일 위험도 커진다. 그래서 실무 설계에서는 [Power](/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Loss [Protection](/studynote/02_operating_system/10_security/571_protection_vs_security/) (PLP), wear histogram 모니터링, TRIM 활용률, GC와의 충돌 시간대까지 함께 봐야 한다.

### 적용 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 최대 erase count와 최소 erase count의 차이가 지속적으로 커지는가?
2. OP 비율이 현재 워크로드의 write burst를 흡수할 만큼 충분한가?
3. TRIM이 제대로 전달되어 불필요한 migration을 줄이고 있는가?
4. 정적 [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)가 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 민감 구간이 아닌 [idle](/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/) window에 수행되는가?
5. PLP와 매핑 저널링이 있어 이동 중 전원 차단에도 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 가능한가?

### 피해야 할 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- SSD에 주기적 조각 모음을 수행해 불필요한 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 만드는 운영
- 평균 wear만 보고 최댓값 블록의 임계 근접을 놓치는 모니터링
- 정적 [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)를 실시간 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 경로 한복판에서 과도하게 수행하는 설계

기술사 답안에서는 "수명 연장"만 쓰면 얕다. 더 좋은 답은 <strong>수명 연장과 <a href="/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/">WAF</a> 상승이 서로 맞물린다</strong>는 점, 그리고 <strong><a href="/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/">매체</a>·워크로드·OP·PLP를 함께 설계해야 한다</strong>는 점까지 연결하는 것이다.

- **📢 섹션 요약 비유**: 공장 관리자가 기계를 오래 쓰고 싶다고 해서 근무 시간마다 자리 바꾸기만 시키면 생산성이 무너진다. 중요한 것은 쉬는 시간과 작업량을 보며 가장 덜 아프게 부하를 나누는 운영이다.

---

## Ⅴ. 기대효과 및 결론

[마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)가 잘 설계되면 저장장치는 블록별 편차가 작은 예측 가능한 수명을 갖게 된다. 이는 보증 수명 계산, 장애 대응, 품질 관리 측면에서 큰 의미가 있다. 또한 더 저렴한 셀 구조를 사용하더라도 컨트롤러 지능으로 일정 수준의 신뢰성을 확보할 수 있어, 비용 대비 용량 경쟁력도 높아진다.

하지만 이 기술은 노화를 없애는 마법이 아니다. 전체 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)량이 계속 누적되면 언젠가는 장치 전체가 닳고, 정적 이동이 많을수록 내부 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)와 전력 소모도 함께 증가한다. 앞으로는 [ZNS](/studynote/01_computer_architecture/15_advanced_topics/703_zns_ssd/) (Zoned [Namespaces](/studynote/01_computer_architecture/15_advanced_topics/700_nvme_namespaces/))처럼 호스트가 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 패턴을 더 명시적으로 알려 주는 구조, [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 기반 hot/cold 예측, SCM까지 포괄하는 계층형 wear 관리가 중요해질 가능성이 크다.

결론적으로 [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)는 "비휘발성 메모리의 짧은 수명을 늘리는 기술"이라기보다, <strong>불균등한 <a href="/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 패턴을 균등한 노화로 바꾸는 제어 기술</strong>로 기억하는 것이 정확하다. 장치가 오래 가는 이유는 셀이 강해져서가 아니라, 컨트롤러가 편향된 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 골고루 흩어 주기 때문이다.

- **📢 섹션 요약 비유**: 결국 [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)는 한 권의 공책을 맨 앞 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)만 쓰지 않고 끝 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)까지 골고루 쓰게 만드는 습관과 같다. 종이의 품질을 바꾸지 않아도, 쓰는 방식을 바꾸면 공책은 훨씬 오래 간다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [FTL](/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/) ([Flash Translation Layer](/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/)) | [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 주소를 물리 블록에 재매핑하며 [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)를 실행한다. |
| P/E (Program/Erase) 사이클 | 셀 수명을 결정하는 직접 제약 조건이다. |
| [WAF](/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/) ([Write Amplification](/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/) Factor) | 수명 연장 과정에서 발생하는 추가 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 비용을 수치화한다. |
| OP (Over-Provisioning) | wear leveling과 GC가 충돌 없이 움직일 작업 공간을 제공한다. |
| TRIM | 무효 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [힌트](/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)로 불필요한 이동을 줄여 준다. |
| 배드 블록 관리 | 수명 한계를 넘긴 블록을 격리하는 후속 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 기법이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
고정 논리-물리 매핑 기반 플래시 사용
        |
        v
핫스폿 블록 조기 마모 문제
        |
        v
FTL 기반 동적 마모 평준화
        |
        v
정적 마모 평준화 · OP 확대 · GC 연계
        |
        v
웨어 히스토그램 기반 예측형 컨트롤러
        |
        v
ZNS / SCM까지 확장되는 호스트-장치 협력 수명 관리
```

이 흐름은 단순 주소 변환에서 시작해, 장치 내부 통계와 호스트 [힌트](/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)를 함께 사용하는 방향으로 수명 관리가 고도화되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)는 공책의 한 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)만 계속 쓰지 않고 여러 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 돌아가며 쓰는 방법이에요.
2. 그래서 어떤 한 장만 먼저 찢어지지 않고 공책 전체를 오래 사용할 수 있어요.
3. 대신 가끔은 사진이 붙어 있는 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)도 옮겨야 해서 정리하는 수고가 조금 더 생겨요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 526 / 803

<- **이전**: [525. 메인 메모리 압축 기술 (Main Memory Compression)](/studynote/01_computer_architecture/15_advanced_topics/525_main_memory_compression/)
**다음**: [527. 가상화 오버헤드 감소 (하드웨어 보조)](/studynote/01_computer_architecture/15_advanced_topics/527_hardware_assisted_virtualization/) ->

---
