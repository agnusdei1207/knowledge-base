+++
title = "BASE 원칙 (Basically Available, Soft State, Eventual Consistency)"
date = 2024-05-22

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
- <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a> 우선(<a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">Availability</a> First):</strong> [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 엄격한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)(ACID)을 희생하더라도, 대규모 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서 중단 없는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 제공하는 NoSQL의 핵심 철학임.
- <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/">결과적 일관성</a>(<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/">Eventual Consistency</a>):</strong> 실시간으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 일치하지 않을 수 있지만, 일정 시간이 지나면 모든 노드가 동일한 값을 갖게 됨을 보장함.
- **확장성 극대화:** [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템의 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리에서 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)(A)과 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 감내(P)를 선택하여 전 세계 사용자에게 빠른 응답 속도를 제공함.

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
1. **RDBMS의 한계:** 전통적인 ACID([원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/), [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [고립성](/knowledge-base/studynote/05_database/07_exam_summary/443_isolation_concurrency_control/), 지속성)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 보장하지만, 수천 개의 서버가 연결된 빅데이터 환경에서는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하와 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 하락을 유발함.
2. **BASE의 탄생:** 대규모 웹 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(Amazon, Google)에서 수평 확장([Scale-out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))을 위해 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 "결과적"으로 타협하되, [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 극대화하는 새로운 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 모델이 필요하게 됨.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- <strong>BASE Principle Workflow &amp; Distributed <a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/">Replication</a></strong>


<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Data Write (Node A)</div><div class="kb-diagram-node">Propagation Delay</div><div class="kb-diagram-node">Data Read (Node B)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Value = 10 (Update)</div><div class="kb-diagram-cell">--- (Asynchronous Sync) ---&gt;</div><div class="kb-diagram-cell">Value = 5 (Soft State)</div></div>
<div class="kb-diagram-note">v</div>
<div class="kb-diagram-note">(Eventually Consistency)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">+--------------&gt;</div><div class="kb-diagram-cell">Value = 10 (Synced)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Key Pillars of BASE</div></div>
<div class="kb-diagram-note">1. BA: Basically Available (기본적 가용성)</div>
<div class="kb-diagram-note">2. S : Soft State (소프트 스테이트)</div>
<div class="kb-diagram-note">3. E : Eventual Consistency (결과적 일관성)</div>
</div>
</div>



1. <strong>Basically Available (<a href="/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/">BA</a>):</strong>
   - 시스템의 일부분에 장애가 발생하더라도, 전체 시스템이 멈추지 않고 기본적인 응답을 제공함. 완벽한 응답은 아니더라도 가용한 상태를 유지함.
2. <strong>Soft <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/">State</a> (S):</strong>
   - [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 상태가 외부의 입력 없이도 시간이 지남에 따라 변할 수 있음. 노드 간 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)가 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중일 때, 특정 시점의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 "확정된 상태"가 아닐 수 있음을 의미함.
3. <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/">Eventual Consistency</a> (E):</strong>
   - 특정 시간 동안 새로운 업데이트가 없다면, 결국 모든 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본(Replica)은 동일한 값으로 수렴함. 일시적인 불일치를 허용하여 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목을 제거함.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | ACID (RDBMS) | BASE ([NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/)) | 융합 분석 |
| :--- | :--- | :--- | :--- |
| **핵심 가치** | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) | [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) ([Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) | ACID는 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/), BASE는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) |
| **시스템 상태** | 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) (Strong) | [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) (Eventual) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중요도에 따라 혼용 |
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a> 관리</strong> | 비관적 락 (Pessimistic) | 낙관적 방식 (Optimistic) | [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 제어 방식의 차이 |
| **확장성** | 수직 확장 ([Scale-up](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)) | 수평 확장 ([Scale-out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)) | 빅데이터 처리는 수평 확장이 대세 |
| **사용 사례** | 금융, 결제, 인사 관리 | SNS, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 카트, 댓글 | 정합성 vs 실시간성 선택 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
1. <strong>비즈니스 <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a>별 선택 (<a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">Strategy</a>):</strong>
   - **SNS 뉴스피드:** 친구의 글이 1초 늦게 보여도 문제없으므로 BASE가 적합함.
   - **계좌 이체:** 1원이라도 틀리면 치명적이므로 반드시 ACID를 유지해야 함.
2. **기술사적 판단:** 현대 아키텍처는 "[Polyglot Persistence](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/132_polyglot_persistence/)"를 지향함. 주문 정보는 RDBMS(ACID)에, 대량의 상품 조회 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/)(BASE)에 저장하여 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 안전성을 동시에 확보하는 것이 핵심 설계 역량임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
1. **기대효과:** 전 지구적 규모의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템(Global Distribution)에서 [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))을 최소화하고, 무한한 확장을 가능하게 하여 현대 인터넷 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 기술적 근간이 됨.
2. **결론:** BASE는 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 포기한 것이 아니라, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 위해 "[일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)의 시점"을 늦춘 지혜로운 타협임. [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터베이스 설계자](/knowledge-base/studynote/05_database/01_db_architecture_relational/027_database_designer/)는 BASE 원칙을 통해 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)의 [임계치](/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)를 돌파할 수 있음.

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념:** [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/), [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/)
- **하위 개념:** [결과적 일관성](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/), [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) ([Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))
- **연관 개념:** [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리, [PACELC](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 이론, ACID

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">상위 개념: 분산 데이터베이스, NoSQL</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">하위 개념: 결과적 일관성, 가용성 (Availability)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">연관 개념: CAP 정리, PACELC 이론, ACID</div></div>
</div>
</div>



이 흐름도는 상위 개념: [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/), NoSQL에서 출발해 연관 개념: [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리, [PACELC](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 이론, ACID까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
- **ACID 식당:** 주방장이 모든 테이블의 요리를 완벽하게 다 만들 때까지 손님을 한 명도 안 들여보내는 깐깐한 식당이에요.
- **BASE 식당:** 일단 손님을 다 받고 음식을 조금씩 주면서, 나중에는 모두가 맛있는 요리를 배부르게 먹을 수 있게 조절하는 인기 식당이에요.
- **결론:** 처음엔 조금 복잡해 보일 수 있어도, 결국에는 모두가 행복해지는 마법 같은 순서 맞추기랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 124 / 262

← **이전**: [NoSQL 아키텍처와 분산 데이터 모델링 (NoSQL Architecture)](/knowledge-base/studynote/16_bigdata/06_nosql/123_nosql_architecture/)
**다음**: [CAP 정리 (CAP Theorem)](/knowledge-base/studynote/16_bigdata/06_nosql/125_cap_theorem_distributed_db/) →

---
