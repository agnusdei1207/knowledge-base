---
title: "Space-Based Architecture"
date: "2026-04-21"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스페이스 기반 아키텍처([SBA](/studynote/06_ict_convergence/02_iot_mobility/151_sba_service_based_architecture_5g/), Space-Based [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/))는 요청 처리 경로에서 중앙 DB ([Database](/studynote/05_database/04_transactions_concurrency/501_database/)) 병목을 제거하기 위해 처리 로직과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 인메모리 공간으로 끌어올린 고확장성 패턴이다.
> 2. **가치**: 트래픽이 순간적으로 폭증하는 업무에서 처리 유닛(Processing Unit)을 수평 확장해 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간과 처리량을 동시에 개선할 수 있다.
> 3. **판단 포인트**: [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 이득의 대가로 최종 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)([Eventual Consistency](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)), 비동기 영속화, 장애 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 설계를 함께 감당할 수 있을 때만 SBA의 장점이 현실화된다.

---

## Ⅰ. 개요 및 필요성

스페이스 기반 아키텍처는 애플리케이션 서버와 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공간을 결합해 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스를 실시간 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 경로의 중심에서 밀어내는 아키텍처다. 전통적인 3계층 구조는 웹 서버와 애플리케이션 서버는 손쉽게 늘릴 수 있지만, 상태와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 중앙 DB에 집중되면서 결국 확장의 천장이 DB에서 생긴다. 읽기 캐시를 붙여도 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 집중 구간에서는 병목이 남고, [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 관리가 더 복잡해진다.

SBA는 이 문제를 “요청을 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 있는 곳으로 보내는 것”으로 풀지 않고, “[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 처리를 함께 가진 단위를 여러 개 두는 것”으로 푼다. 즉 처리 유닛이 웹 로직, 비즈니스 로직, 인메모리 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)까지 함께 보유하고, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 인메모리 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 그리드(IMDG, In-Memory [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Grid)에 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 저장된다. 그 결과 순간 부하가 매우 큰 주문·경매·게임·실시간 이벤트 시스템에서 중앙 저장소 병목을 크게 낮출 수 있다.

중요한 전제는 모든 시스템이 SBA를 필요로 하지는 않는다는 점이다. CRUD 중심 업무나 강한 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)이 절대적인 시스템이라면, 전통 구조에 캐시·읽기 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)·[CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) ([Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) Query Responsibility Segregation)를 조합하는 편이 더 단순하고 안정적일 수 있다.

- **📢 섹션 요약 비유**: SBA는 손님이 몰릴 때마다 중앙 창고에 뛰어가는 가게를 없애고, 각 매장이 자주 쓰는 물건을 자기 뒤 창고에 바로 쌓아두는 방식과 같다. 빨라지지만, 각 매장 재고를 맞추는 일이 새 숙제가 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SBA의 핵심 구성요소는 처리 유닛, [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 미들웨어, [튜플](/studynote/05_database/02_modeling_normalization/063_relation_tuple_cardinality/) 스페이스(Tuple Space) 또는 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공간, 그리고 비동기 영속화 계층이다. 처리 유닛은 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 코드와 해당 업무 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 지역 캐시를 함께 갖는다. [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 미들웨어는 요청을 적절한 처리 유닛으로 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)하고, 인메모리 공간은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)과 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)에 따라 배치한다.

아래 그림은 SBA의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로를 압축한다. 사용자의 요청은 먼저 처리 유닛에 도달하고, 처리 유닛은 메모리 공간을 우선 조회한다. 영속 저장소는 즉시 동기식으로 두드리는 대상이 아니라, [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)와 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적을 위한 후행 저장소로 밀려난다.

```text
+-----------------------------------------------------------------------------+
|                 스페이스 기반 아키텍처의 요청 처리 흐름                    |
+-----------------------------------------------------------------------------+
| Client Request                                                             |
|      |                                                                     |
|      v                                                                     |
| [Virtualized Middleware]                                                   |
|      |           라우팅/파티션/장애조치                                    |
|      +------------------+------------------+------------------+            |
|      v                  v                  v                  v            |
| [PU-A]              [PU-B]              [PU-C]          ... [PU-N]         |
|  |                  |                  |                                   |
|  +- Web/API         +- Web/API         +- Web/API                          |
|  +- Business Logic  +- Business Logic  +- Business Logic                   |
|  +- Local Cache     +- Local Cache     +- Local Cache                      |
|      |                  |                  |                                 |
|      +--------------+---+--------------+---+                                 |
|                     v                  v                                     |
|              [Tuple Space / IMDG Partitioned Grid]                          |
|                     |                  |                                     |
|                     +------- Async Write-Behind --------> [Database]         |
+-----------------------------------------------------------------------------+
```

| 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 처리 유닛 (Processing Unit) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근을 한 단위로 묶음 | 무상태가 아니라 “로컬 상태를 가진 확장 단위” |
| [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 미들웨어 | [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/), 장애 조정 | Hot key와 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 중요 |
| [튜플](/studynote/05_database/02_modeling_normalization/063_relation_tuple_cardinality/) 스페이스 / IMDG | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 메모리 저장소 | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키, [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 수, [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 노드 설계 |
| 비동기 영속화 | Write-Behind, [Snapshot](/studynote/02_operating_system/10_security/637_zfs_snapshot_cow_architecture/), Event Log | 유실 허용 범위와 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 방식 정의 |
| [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 엔진 | 처리 유닛 간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복사 | [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준과 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간의 균형 |

SBA가 빠른 이유는 단순히 메모리가 디스크보다 빨라서만이 아니다. <strong>확장 단위가 “웹 서버 따로, 앱 서버 따로, DB 따로”가 아니라 “처리와 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>가 묶인 유닛 전체”</strong>이기 때문이다. 따라서 노드를 추가할수록 계산 능력과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 능력이 함께 늘어난다. 반면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/), 재시작 시 warm-up, 메모리 장애 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)는 훨씬 더 신중하게 설계해야 한다.

- **📢 섹션 요약 비유**: 각 점포가 계산대, 재고, 간단한 창고를 한몸처럼 들고 있는 프랜차이즈 매장이라고 생각하면 쉽다. 점포 수를 늘리면 판매대와 재고처리 능력이 동시에 늘어나지만, 재고 복사와 마감 정산 체계가 허술하면 전체 체인이 흔들린다.

---

## Ⅲ. 비교 및 연결

SBA를 이해하려면 전통 3계층 구조, 단순 캐시 확장, 이벤트 기반 구조와의 경계를 함께 봐야 한다. 3계층 구조는 이해와 운영이 쉽고 강한 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 확보하기 좋지만, 중앙 DB 병목을 피하기 어렵다. 캐시를 붙인 구조는 읽기는 빨라지지만 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 경합과 캐시 무효화가 계속 문제로 남는다. SBA는 이 두 구조보다 더 과감하게 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 메모리 쪽으로 이동시킨다.

| 비교 축 | 전통 3계층 | 캐시 보강 구조 | [SBA](/studynote/06_ict_convergence/02_iot_mobility/151_sba_service_based_architecture_5g/) |
| :--- | :--- | :--- | :--- |
| 병목 위치 | 중앙 DB | DB + 캐시 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) | 메모리 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)·영속화 |
| 확장 단위 | 웹/앱 서버 위주 | 앱 서버 + 캐시 계층 | 처리 유닛 전체 |
| [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 강한 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 유리 | 캐시 불일치 가능 | 최종 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 전제 |
| [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 | DB I/O 의존 | 읽기만 빠른 경우 많음 | 읽기·[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 모두 메모리 우선 처리 |
| 적합 업무 | 일반 업무 시스템 | 읽기 편중 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 실시간 고동시성 시스템 |

SBA는 [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/), [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)([Event Sourcing](/studynote/12_it_management/05_security_compliance/307_event_sourcing/)), LMAX Disruptor와도 연결된다. 이들은 모두 “중앙 동기식 병목을 줄이고 메모리·이벤트 중심으로 처리한다”는 방향성을 공유한다. 다만 SBA는 시스템의 <strong>배치 단위 자체를 바꾸는 아키텍처 패턴</strong>이고, 다른 개념들은 저장/명령/[동시성](/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 처리의 세부 기법이라는 점에서 범위가 다르다.

- **📢 섹션 요약 비유**: 3계층 구조가 중앙 창고형 백화점이라면, 캐시 보강 구조는 빠른 임시 창고를 붙인 형태다. SBA는 아예 작은 매장을 여러 개 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)해 손님을 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)시키는 동네형 네트워크에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

SBA는 순간 트래픽 스파이크가 크고, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 패턴이 비교적 지역적이며, 일부 최종 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 수용할 수 있는 환경에서 적합하다. 실시간 경매, 게임 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 처리, 광고 입찰, [초고속](/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 주문 처리처럼 “DB를 매번 찍는 순간 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 폭증하는” 업무가 대표적이다. 반대로 정산, 회계, 핵심 원장처럼 강한 정합성이 절대적인 업무는 SBA만으로 처리하기 어렵다.

### 채택 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 일부 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)와 비동기 저장을 수용할 수 있는가?
2. 업무 키를 기준으로 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 안정적으로 나눌 수 있는가?
3. 노드 장애 시 재복구 시간과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) warm-up 비용을 감당할 수 있는가?
4. 메모리 사용량이 경제적으로 유지되는가?
5. 운영팀이 장애 조치, 재분배, [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)·[복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 이해하고 있는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 단순 CRUD [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 과도하게 도입해 운영 복잡도만 키우는 경우
- [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키가 잘못돼 일부 노드만 과부하되는 Hot Spot 구조
- 비동기 영속화 실패를 가볍게 보고 재처리·재동기화 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 준비하지 않는 경우

기술사 답안에서는 “DB 병목 제거”만 강조하면 절반짜리다. 반드시 <strong><a href="/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/">영속성</a>, <a href="/studynote/14_data_engineering/01_infrastructure/016_replication_factor/">복제</a>, 장애 <a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a>, 정합성 수준</strong>을 함께 적어야 SBA를 입체적으로 설명한 답안이 된다. 고성능은 장점이지만, 그 장점을 유지하는 운영 체계까지 포함해야 패턴의 완성도가 나온다.

- **📢 섹션 요약 비유**: SBA는 손님이 몰리는 놀이공원에 입구를 많이 만드는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 같다. 입장은 빨라지지만, 분실물 보관과 마감 정산까지 같이 설계하지 않으면 운영이 더 혼란스러워질 수 있다.

---

## Ⅴ. 기대효과 및 결론

SBA의 기대효과는 [초고속](/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 응답, 선형에 가까운 수평 확장, 그리고 DB 의존도 감소다. 특히 피크 트래픽이 매우 불규칙한 환경에서 큰 효과를 낸다. 처리 유닛을 늘리면 웹 계층만이 아니라 실질 처리 용량도 함께 늘어나므로, [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측과 확장 계획이 단순해진다.

그러나 이 효과는 메모리 공간을 잘게 나누고 안전하게 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)할 수 있을 때만 유지된다. 메모리 기반 구조는 매우 빠르지만, 장애와 정합성 문제에 더 민감하다. 따라서 SBA는 “DB를 없애는 패턴”이 아니라, <strong>DB를 실시간 경로에서 뒤로 물리고 메모리-<a href="/studynote/14_data_engineering/01_infrastructure/016_replication_factor/">복제</a>-영속화 설계를 전면에 세우는 패턴</strong>으로 기억하는 것이 정확하다.

- **📢 섹션 요약 비유**: SBA는 고속도로 차선을 늘리는 공사와 비슷하다. 잘 설계하면 정체가 크게 줄지만, 합류 구간과 사고 처리 체계까지 준비해야 진짜로 빨라진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| IMDG (In-Memory [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Grid) | SBA의 핵심 저장·[복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 기반 |
| [튜플](/studynote/05_database/02_modeling_normalization/063_relation_tuple_cardinality/) 스페이스 (Tuple Space) | 공유 메모리형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 상호작용 모델 |
| Write-Behind | 비동기 영속화의 대표 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| [Eventual Consistency](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) | SBA가 흔히 수용하는 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 모델 |
| [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) ([Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) Query Responsibility Segregation) | 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 부담 분리와 연결 |
| LMAX Disruptor | 인메모리 초저지연 패턴의 연관 개념 |
| Hot Spot [Partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 설계 실패 시 대표 장애 원인 |

### 📈 관련 키워드 및 발전 흐름도

```text
3계층 구조의 DB 병목
    |
    v
분산 캐시 · IMDG
    |
    v
스페이스 기반 아키텍처
    |
    +---------------> Tuple Space 파티셔닝 · 복제
    |
    +---------------> Eventual Consistency · Write-Behind
                           |
                           v
                 초저지연 이벤트 처리 · 실시간 확장 패턴
```

이 흐름은 “DB 최적화 -> 메모리 전진 배치 -> 아키텍처 수준의 재구성”으로 진화하는 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 손님이 많을 때마다 중앙 창고에 뛰어가면 너무 느려져요.
2. 그래서 각 가게가 자주 쓰는 물건을 자기 옆 창고에 두고 바로 꺼내 쓰는 게 스페이스 기반 아키텍처예요.
3. 대신 여러 가게의 물건 수를 맞추고 마지막에 큰 창고에 기록하는 규칙을 잘 정해야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 242 / 530

<- **이전**: [185. 피어투피어 아키텍처 (Peer-to-Peer Architecture)](/studynote/11_design_supervision/10_patterns_antipatterns/185_peer_to_peer_architecture/)
**다음**: [186. 스페이스 기반 아키텍처 투플 맵핑 구조 (Space-Based Tuple Mapping)](/studynote/11_design_supervision/10_patterns_antipatterns/657_space_based_tuple_mapping/) ->

---
