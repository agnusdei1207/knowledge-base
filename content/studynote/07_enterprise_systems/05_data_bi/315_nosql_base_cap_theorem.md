+++
title = "315. NoSQL BASE 결과적 일관성 CAP 정리 트레이드오프 (NoSQL BASE CAP Theorem)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-enterprise-systems"]

[extra]
tags = ["studynote-enterprise-systems"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템이 [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)([일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)), [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)([가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)), [Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) Tolerance(분단 내성) 셋 중 둘만 동시에 완전히 보장할 수 있다는 이론이다.
> 2. **가치**: BASE (Basically Available, Soft [state](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/), Eventually consistent)는 CAP의 [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 선택 결과로, 높은 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)과 수평 확장을 택하는 대신 일시적 불일관성을 허용한다.
> 3. **판단 포인트**: 금융 거래·재고 관리는 ACID/CP가 필수이고, 소셜 피드·장바구니는 BASE/AP로 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 우선이 적합하다.

## Ⅰ. 개요 및 필요성

단일 서버 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB는 ACID ([Atomicity](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/), [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/), [Durability](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/)) [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)으로 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 보장한다.
그러나 수평 확장이 필요한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서는 네트워크 분단([Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))이 반드시 발생하므로, Eric Brewer가 2000년에 발표한 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리에 따라 C 또는 A 중 하나를 타협해야 한다.

[CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 3 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/):
- <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">Consistency</a> (C)</strong>: 모든 노드가 동일 시점에 동일 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 봄
- <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">Availability</a> (A)</strong>: 모든 요청이 응답을 받음 (오류 없이)
- <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/">Partition</a> Tolerance (P)</strong>: 네트워크 분단 상황에서도 동작 지속

실제 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서 P는 포기할 수 없으므로 [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 또는 AP를 선택한다.

📢 **섹션 요약 비유**: CAP는 "맛있고, 빠르고, 저렴한" 식당의 삼각형이다. 세 가지를 동시에 모두 갖추기는 불가능하다.

## Ⅱ. 아키텍처 및 핵심 원리

### [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) vs [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 시스템 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)

| [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 특징 | 대표 DB |
|:---|:---|:---|
| [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) ([일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)+분단 내성) | 분단 시 응답 거부, [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 보장 | [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/), [Zookeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/), [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/)(w:majority) |
| [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) ([가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)+분단 내성) | 분단 시에도 응답, 일시적 불일관성 | [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/), CouchDB |
| [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) (이론적 구분) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 아닌 단일 서버 | 전통 RDBMS (MySQL, PostgreSQL) |

### BASE vs ACID 비교

| 항목 | ACID | BASE |
|:---|:---|:---|
| [Atomicity](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/) | 전체 성공 or 전체 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) | 최선의 결과 시도 |
| [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 후 항상 일관 | [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) (Eventually) |
| [Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 간 완전 격리 | 약한 격리 ([동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 증가) |
| [Durability](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/) vs Soft [state](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) | 영속 보장 | 일시적 상태 허용 |
| 확장성 | 수직 확장 한계 | 수평 확장 용이 |

### [ASCII](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램: [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 삼각형과 DB 배치



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CAP 삼각형</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Consistency (C)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">△</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CP 영역 / \ (불가능 영역)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">HBase / \ MongoDB</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Zookeeper ● ● (default)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">/ ×전부 \</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">/ (이론상 불가) \</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Partition ● ● Availability</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Tolerance \ AP 영역 / (A)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(P) \ /</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">\ Cassandra /</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">● DynamoDB ● /</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">\ CouchDB /</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">● ●</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">RDBMS (MySQL, PostgreSQL): 단일 서버 → CA 영역 (P 포기)</div></div>
</div>
</div>



### [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 레벨 스펙트럼

| 레벨 | 설명 | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 사용 예 |
|:---|:---|:---|:---|
| Strong (강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) | 모든 노드 즉시 동일 | 높음 | 금융 잔액 |
| Bounded Staleness | N초 이내 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 보장 | 중간 | 재고 조회 |
| [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) | 같은 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 내 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 낮음 | 사용자 프로필 |
| Eventual ([결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)) | 언젠가 일관 (수ms~수초) | 매우 낮음 | 소셜 피드, 장바구니 |

📢 **섹션 요약 비유**: [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)은 소문이다. 처음엔 사람마다 다르게 알지만, 시간이 지나면 모두 같은 내용을 알게 된다.

## Ⅲ. 비교 및 연결

### [PACELC](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 확장 정리

CAP의 한계를 보완한 [PACELC](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) ([Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) → [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) or [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/), Else → [Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) or [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)):
- **분단 시 (P)**: A([가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) vs C([일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) 선택
- **정상 시 (E)**: L([지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)) vs C([일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) 트레이드오프

| DB | 분단 시 | 정상 시 |
|:---|:---|:---|
| [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) | [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) | EL ([지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 최소화) |
| [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) | [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) | EL |
| [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/) | [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) | EC ([일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 강조) |
| [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) | [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) (default) | EC |

📢 **섹션 요약 비유**: PACELC는 CAP보다 현실적인 지도다. 평상시 운전 규칙(Else)과 사고 시 대응([Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))을 모두 다룬다.

## Ⅳ. 실무 적용 및 기술사 판단

### [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 모델 선택 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [ ] [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 금전적 가치가 있는가? (은행 잔액 → [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/)/ACID 필수)
- [ ] 일시적 불일관성이 비즈니스에 허용 가능한가? (좋아요 수 → [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)/BASE OK)
- [ ] 지리적 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 배포 필요 여부 ([멀티 리전](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/100_multi_region_deployment_pipeline_disaster_recovery/) → [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 선호)
- [ ] 99.99% 이상 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 요건 → [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 우선 고려

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

| [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) | 문제 | 해결 방법 |
|:---|:---|:---|
| 재고 차감에 [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) | 동시 구매 시 재고 초과 판매 | [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) DB ([HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/), [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) SETNX) 사용 |
| 모든 NoSQL에 ACID 기대 | Cassandra는 [Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) | LWT (Light-[weight](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) [Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)) 사용 |

📢 **섹션 요약 비유**: 재고 차감에 [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) DB를 쓰는 건 여러 계산대에서 동시에 마지막 상품을 판매하는 것이다. 손님 2명이 같은 물건을 사고 집에 가면 한 명은 빈손이다.

## Ⅴ. 기대효과 및 결론

### BASE 설계 적합 영역

| [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 모델 | 이유 |
|:---|:---|:---|
| 소셜 피드, 댓글 | BASE/[AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) | 좋아요 수 수초 차이 무방 |
| 장바구니 | BASE/[AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) | 임시 불일관성 허용 |
| 재고 관리 | ACID/[CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) | 초과 판매 불가 |
| 금융 이체 | ACID/[CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) | [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/) 필수 |

📢 **섹션 요약 비유**: 은행 계좌는 ACID(금고), 소셜 피드는 BASE(게시판)다. 금고는 느려도 확실해야 하고, 게시판은 빠르되 잠깐 틀려도 괜찮다.

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 | 이론 기반 | C/A/P 셋 중 둘만 보장 |
| ACID | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 모델 | [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 계열 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 보장 |
| BASE | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 모델 | [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 계열 [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) |
| [PACELC](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) | 확장 이론 | 정상 시 [Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) vs [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |
| [Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) | 상태 | 시간 경과 후 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수렴 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">RDB ACID 트랜잭션 - 분산 환경 확장 한계</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">CAP 정리 - 일관성·가용성·분할내성 동시 불가</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">NoSQL BASE - 결과적 일관성으로 가용성 극대화</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">CP 계열 (HBase, ZooKeeper) vs AP 계열 (Cassandra)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">NewSQL (CockroachDB, Spanner) - ACID + 수평 확장</div>
</div>
</div>



> **키워드**: [CAP Theorem](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/219_cap_pacelc_distributed_tradeoff/), BASE, ACID, [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/), [Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/), [Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) Tolerance, [NewSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/058_newsql_google_spanner_truetime_distributed_transaction/), [CockroachDB](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/292_etl_process/)

### 👶 어린이를 위한 3줄 비유 설명

1. CAP는 "맛있고 빠르고 저렴한 식당"처럼 세 가지를 동시에 다 가질 수 없다는 법칙이에요.
2. ACID는 은행 금고처럼 느리지만 확실한 것, BASE는 소문처럼 빠르지만 잠깐 틀릴 수 있는 것이에요.
3. Eventual Consistency는 "나중엔 다 같아져요"라는 약속이에요. 지금 당장은 달라도 괜찮아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 315 / 482

← **이전**: [314. 텔레메트리 빅데이터 파싱 수집 엔진 (Telemetry Big Data Parsing)](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/314_telemetry_bigdata_parsing/)
**다음**: [316. Redis 캐시와 Thundering Herd 장애 회피 전략](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/316_redis_thundering_herd/) →

---
