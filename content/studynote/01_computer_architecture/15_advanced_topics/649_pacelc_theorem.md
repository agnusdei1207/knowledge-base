---
title: "Pacelc Theorem"
date: "2026-05-08"
tags:
  - "studynote-computer-architecture"
weight: 649
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [PACELC](/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) ([Partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/), [Availability](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/), [Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), Else, [Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/), [Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) 정리는 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 저장소가 장애 시에는 [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)/[일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), 정상 시에는 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간/[일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 사이에서 무엇을 우선할지 함께 설명하는 확장 프레임이다.
> 2. **가치**: [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 ([CAP Theorem](/studynote/14_data_engineering/05_exam_keywords/219_cap_pacelc_distributed_tradeoff/))가 "망가졌을 때의 선택"을 보여줬다면, PACELC는 시스템이 대부분의 시간을 보내는 평상시의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비용까지 드러내어 더 현실적인 설계 기준을 제공한다.
> 3. **판단 포인트**: 글로벌 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 거리, 정족수 (Quorum) 크기, 사용자 허용 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간이 크면 PA/EL 계열이 유리하고, 금전·[메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)처럼 단 한 번의 오류도 치명적이면 [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)/EC 계열이 맞다.

---

## Ⅰ. 개요 및 필요성

[PACELC](/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 정리는 [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리를 보완한 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 설계 원리다. [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)), [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) ([Availability](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)), 분단 허용성 ([Partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) tolerance) 사이의 선택을 설명하지만, 초점이 네트워크 분단이라는 비정상 상황에 맞춰져 있다. 실제 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 대부분의 시간을 분단이 없는 정상 상태로 보내므로, 아키텍트는 "망가지면 어떻게 할까?"만이 아니라 "멀쩡할 때 얼마나 빨라야 할까?"까지 판단해야 한다.

바로 이 지점에서 PACELC의 두 번째 축이 생긴다. 분단이 발생하면 P-A/C를 고르고, 분단이 없으면 E-L/C를 고른다는 뜻이다. 즉 여러 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본이 살아 있는 평상시에도, 여러 노드의 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)을 기다리면 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간이 늘고, 로컬 응답을 먼저 주면 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)이 약해진다. 지역 간 왕복 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 ([Round Trip Time](/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/), [RTT](/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/))이 50~150ms에 이르는 [멀티 리전](/studynote/15_devops_sre/02_cicd_gitops/100_multi_region_deployment_pipeline_disaster_recovery/) 환경에서는 이 차이가 곧 사용자 경험과 장애 대응 방식을 함께 바꾼다.

- **📢 섹션 요약 비유**: PACELC는 비 오는 날 우산을 고르는 법만 알려주는 것이 아니라, 맑은 날에도 운동화를 신을지 구두를 신을지까지 정해 주는 생활 규칙과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

PACELC의 핵심은 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 경로에서 "언제 응답을 주느냐"다. [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))을 우선하는 구조는 리더와 팔로어, 혹은 정족수 노드의 커밋 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)을 받은 뒤 응답한다. 반대로 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 ([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))을 우선하는 구조는 로컬 커밋 후 즉시 응답하고, 나머지 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)는 비동기식으로 뒤따르게 한다. 그래서 PACELC는 이론이 아니라, [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 승인 시점과 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 토폴로지를 설명하는 운영 모델에 가깝다.

아래 그림은 PACELC가 실제 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 경로를 어떻게 갈라놓는지 보여 준다.

```text
+----------------------------------------------------------------------------+
|              PACELC decision path in a replicated storage system          |
+----------------------------------------------------------------------------+
| Client Write                                                              |
|      |                                                                    |
|      v                                                                    |
| Partition detected?                                                       |
|      +-- Yes ---> choose A or C                                            |
|      |            +- A: accept local write, sync later                    |
|      |            +- C: reject or block until agreement                   |
|      |                                                                    |
|      +-- No  ---> choose L or C                                            |
|                   +- L: local ack first, async replication                |
|                   +- C: quorum or leader commit before ack                |
+----------------------------------------------------------------------------+
```

| [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 분단 시 선택 | 정상 시 선택 | 동작 특성 | 대표적 활용 |
| :--- | :--- | :--- | :--- | :--- |
| PA/EL | [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 우선 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 우선 | 로컬 응답 후 비동기 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | 장바구니, 피드, [로그 수집](/studynote/09_security/13_secops_ir_forensics/626_log_collection/) |
| PA/EC | [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 우선 | [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 우선 | 분단 때는 버티되 평상시 정족수를 강하게 둠 | 튜닝형 문서/[키-값 저장소](/studynote/14_data_engineering/01_infrastructure/036_key_value/) |
| [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)/EL | [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 우선 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 우선 | 분단 때 차단하지만 평상시 일부 로컬 읽기 최적화 | 혼합형 리더-팔로어 구조 |
| [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)/EC | [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 우선 | [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 우선 | 평상시에도 합의 후 응답 | 계좌, 락 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) |

하드웨어와 네트워크가 빨라질수록 EL과 EC의 간격은 줄어든다. 예를 들어 원격 [직접 메모리 접근](/studynote/02_operating_system/08_storage_and_io_systems/450_dma_direct_memory_access/) (Remote [Direct Memory Access](/studynote/01_computer_architecture/08_io_storage_systems/318_dma/), [RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/)), 빠른 [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/), 정밀 시계 동기화는 합의와 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 비용을 낮춰 준다. 그러나 물리적 거리와 광속 한계는 사라지지 않으므로, PACELC는 여전히 "빠르게 맞출 것인가, 정확하게 기다릴 것인가"를 묻는 유효한 틀이다.

- **📢 섹션 요약 비유**: PACELC는 택배센터 운영 규칙과 같다. [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 도장을 다 받고 보내면 정확하지만 느리고, 일단 출발시키면 빠르지만 나중에 오배송 정리가 필요하다.

---

## Ⅲ. 비교 및 연결

[CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리가 장애 상황의 선택을 설명한다면, PACELC는 그 위에 평상시 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비용을 한 층 더 얹는다. 그래서 둘 다 "[AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 계열"로 보이는 시스템도 PACELC로 보면 PA/EL과 PA/EC처럼 서로 다른 성격으로 갈라진다. 같은 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)형 저장소라도 정족수 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), 리더-팔로어 구조, 지역 캐시 정책에 따라 정상 상태의 체감이 크게 달라지기 때문이다.

| 관점 | [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 ([CAP Theorem](/studynote/14_data_engineering/05_exam_keywords/219_cap_pacelc_distributed_tradeoff/)) | [PACELC](/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 정리 |
| :--- | :--- | :--- |
| 중심 질문 | 분단 시 무엇을 포기할 것인가 | 분단 시 무엇을 포기하고, 평상시 무엇을 우선할 것인가 |
| 고려 범위 | 장애 시나리오 중심 | 장애 + 정상 운영 전체 |
| [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 해석 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 비용이 드러나지 않음 | [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 비용과 응답시간을 명시적으로 노출 |
| 실무 연결 | [CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/)/[AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 대분류 | 정족수, 글로벌 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), 읽기 정책까지 세분화 |

이 개념은 [결과적 일관성](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) ([Eventual Consistency](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)), 정족수 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) (Quorum [Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)), 리더리스 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) (Leaderless [Replication](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)), 글로벌 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) (Geo-[replication](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)) 같은 주제와 직접 연결된다. 예를 들어 [멀티 리전](/studynote/15_devops_sre/02_cicd_gitops/100_multi_region_deployment_pipeline_disaster_recovery/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스에서 지역 간 RTT가 커질수록 EC 선택의 비용이 커지고, 사용자 가까운 곳에서 읽기를 우선하면 EL 성향이 강해진다. 결국 PACELC는 <strong><a href="/studynote/14_data_engineering/01_infrastructure/016_replication_factor/">복제</a> 토폴로지와 네트워크 물리 조건을 <a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a> 모델과 묶어서 해석하는 언어</strong>다.

- **📢 섹션 요약 비유**: CAP이 비상구 위치만 표시한 건물 안내도라면, PACELC는 평소 사람 흐름이 어디서 막히는지까지 보여 주는 동선 설계도와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 PACELC는 단순 이론 암기가 아니라 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 등급 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 도구다. 예를 들어 전 세계 사용자의 '좋아요' 수나 장바구니는 몇 초의 불일치를 허용해도 비즈니스가 유지되므로 PA/EL 계열이 유리하다. 반면 계좌 잔액, [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 잠금, [네임노드](/studynote/14_data_engineering/01_infrastructure/014_namenode/) [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)처럼 잘못된 응답 한 번이 전체 시스템을 무너뜨리는 영역은 [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)/EC가 맞다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 사용자가 허용할 수 있는 최대 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간은 몇 ms인가?
2. 잘못된 값 1회가 "불편"인지 "사고"인지 구분했는가?
3. [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 노드가 같은 랙인지, 다른 가용영역인지, 다른 대륙인지에 따라 RTT를 계산했는가?
4. `W + R > N` 같은 정족수 설계로 EL과 EC 사이 중간 지점을 조절할 수 있는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- CAP만 외우고 평상시 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 비용을 무시하는 설계
- 금전 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 PA/EL을 적용해 "나중에 맞추면 된다"고 보는 태도
- [멀티 리전](/studynote/15_devops_sre/02_cicd_gitops/100_multi_region_deployment_pipeline_disaster_recovery/) 합의 비용을 측정하지 않고 EC를 선언하는 문서 중심 설계

PACELC는 설계자에게 "무엇을 포기할지"만 묻지 않는다. <strong>무엇을 언제까지 기다릴지</strong>도 묻는다. 따라서 기술사 답안에서는 장애 상황과 정상 상황의 선택을 분리해서 써야 설계 의도가 선명해진다.

- **📢 섹션 요약 비유**: [PACELC](/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 판단은 병원 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)처럼 응급실과 외래를 나누는 일과 같다. 모두를 같은 속도와 같은 엄격함으로 처리하면 오히려 전체 시스템이 막힌다.

---

## Ⅴ. 기대효과 및 결론

PACELC를 적용하면 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 저장소를 "무조건 강한 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)"이나 "무조건 빠른 시스템" 같은 감성 언어 대신, 장애 시 선택과 평상시 선택으로 분해해 설명할 수 있다. 이 덕분에 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준, [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), 사용자 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 예산을 같은 표에서 비교할 수 있고, 결과적으로 아키텍처 설명과 의사결정이 훨씬 명확해진다.

다만 PACELC는 만능 공식이 아니다. 실제 시스템은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 종류별로 서로 다른 정책을 섞고, 읽기와 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), 캐시 계층까지 함께 고려해야 한다. 따라서 이 정리는 "정답을 주는 공식"이 아니라 <strong><a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 저장소의 숨은 비용을 드러내는 해석 프레임</strong>으로 기억하는 것이 가장 정확하다.

- **📢 섹션 요약 비유**: PACELC는 옷장 정리표와 같다. 자주 입는 옷과 중요한 옷을 같은 기준으로 다루지 않게 해 주기 때문에, 필요한 순간에 가장 맞는 선택을 빠르게 꺼낼 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 ([CAP Theorem](/studynote/14_data_engineering/05_exam_keywords/219_cap_pacelc_distributed_tradeoff/)) | 분단 시 선택이라는 PACELC의 출발점이다. |
| [결과적 일관성](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) ([Eventual Consistency](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)) | EL 성향 시스템이 자주 채택하는 사후 수렴 방식이다. |
| 정족수 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) (Quorum [Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) | EC와 EL 사이 균형을 조절하는 대표 메커니즘이다. |
| 리더리스 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) (Leaderless [Replication](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)) | PA/EL 계열 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 저장소에서 자주 쓰이는 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 구조다. |
| 글로벌 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) (Geo-[replication](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)) | 리전 간 RTT가 PACELC의 L/C 비용을 직접 키우는 환경 조건이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
CAP 정리 (Consistency / Availability / Partition tolerance)
    |
    v
PACELC 정리
: Partition 시 A/C, Else 시 L/C를 함께 고려
    |
    +---> 결과적 일관성 (Eventual Consistency) · 비동기 복제
    |
    +---> 정족수 (Quorum) · 리더 기반 합의
    |
    v
지리 분산 데이터베이스 · 저지연 네트워크 · 시간 동기화 기반 일관성 최적화
```

### 👶 어린이를 위한 3줄 비유 설명

1. PACELC는 컴퓨터들이 "고장 났을 때는 무엇을 지키고, 멀쩡할 때는 무엇을 먼저 할지" 정하는 약속이에요.
2. 어떤 컴퓨터는 빨리 대답하는 걸 더 좋아하고, 어떤 컴퓨터는 느려도 틀리지 않는 걸 더 좋아해요.
3. 그래서 좋은 설계자는 모든 문제를 한 가지 규칙으로 풀지 않고, 상황에 맞는 약속을 골라 준답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 650 / 803

<- **이전**: [648. 캡 정리 (CAP Theorem)와 분산 스토리지](/studynote/01_computer_architecture/15_advanced_topics/648_cap_theorem_storage/)
**다음**: [650. 결과적 일관성 (Eventual Consistency)](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) ->

---
