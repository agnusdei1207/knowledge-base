+++
title = "253. CAP 정리 (CAP Theorem)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 ([CAP Theorem](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/219_cap_pacelc_distributed_tradeoff/))은 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)([Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)), [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)([Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)), 분단 허용성([Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) Tolerance) 3가지를 동시 만족 불가 ([분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) DB 이론)에 초점을 맞춘 개념이다.
> 2. **가치**: [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서는 지연과 네트워크 분할이 상수이므로 단일 DB의 사고방식만으로는 부족하다.
> 3. **판단 포인트**: 판단 포인트는 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리를 어디에 적용해야 효과가 크고, 어떤 비용이나 제약이 따라오는지 함께 보는 데 있다.

---

## Ⅰ. 개요 및 필요성

[CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 ([CAP Theorem](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/219_cap_pacelc_distributed_tradeoff/))은 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)([Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)), [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)([Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)), 분단 허용성([Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) Tolerance) 3가지를 동시 만족 불가 ([분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) DB 이론)에 초점을 맞춘 개념이다. [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서는 지연과 네트워크 분할이 상수이므로 단일 DB의 사고방식만으로는 부족하다. 정합성·[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)·지연시간을 동시에 최대로 잡으려 하면 설계가 모순된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Client -&gt; Coordinator -&gt; Current concept -&gt; Replica result</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Network delay -&gt; rule -&gt; consistency outcome</div></div>
</div>
</div>



이 그림은 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리를 독립 기능이 아니라 전체 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름에서 특정 통제 지점을 맡는 구조로 이해해야 한다는 점을 압축해 보여 준다.

- **📢 섹션 요약 비유**: [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 여러 지점 창고 재고를 맞추는 일에 가깝다. 중요한 것은 순서를 정하고 책임 범위를 분명히 하는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 결국 "언제 보고, 어디에서 적용하고, 무엇을 보장할 것인가"를 정하는 메커니즘이다. 특히 `Saga 패턴`과 `CP 시스템 / AP 시스템 / CA 시스템` 사이에서 현재 주제가 맡는 책임을 분리해 보면 구조가 더 또렷해진다.

| 관점 | 설명 | 설계 포인트 |
| :--- | :--- | :--- |
| 핵심 대상 | [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 `CAP 정리 (CAP Theorem)`의 역할과 적용 범위를 규정한다. | 이름보다 입력·출력 경계를 먼저 정의해야 한다. |
| 작동 원리 | 핵심은 현재 개념을 어떤 시점에 평가하고 어떤 범위에 적용하느냐에 있다. | 언제 평가하고 언제 확정하는지가 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 정합성을 가른다. |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 영향 | [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/), 지연시간, 운영 복잡도 중 적어도 하나에 직접 영향을 준다. | 이득과 비용을 같이 보지 않으면 과설계가 된다. |
| 운영 주의 | `Saga 패턴`·`CP 시스템 / AP 시스템 / CA 시스템`과 경계를 혼동하면 적용 위치가 어긋난다. | 장애 시 관찰할 지표와 우회 전략을 미리 준비해야 한다. |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Prepare -&gt; sync -&gt; current concept -&gt; final decision</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Local success -&gt; global agreement -&gt; atomicity</div></div>
</div>
</div>



핵심은 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리를 단순 옵션이 아니라 입력 조건, 처리 순서, 결과 보장을 함께 묶는 설계 규칙으로 보는 것이다. 그래서 구현 전에 평가 시점·충돌 지점·[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 가능성을 먼저 정리해야 한다.

- **📢 섹션 요약 비유**: [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 택배 허브에서 승인 신호를 모으는 일에 가깝다. 중요한 것은 순서를 정하고 책임 범위를 분명히 하는 일이다.

---

## Ⅲ. 비교 및 연결

[CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 종종 `Saga 패턴` 또는 `CP 시스템 / AP 시스템 / CA 시스템`과 같은 묶음으로 설명되지만, 세 개념의 관심사는 다르다. [Saga](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/) 패턴이 준비 단계나 전제에 가깝다면, [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 실제 통제 지점을 잡고, [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 시스템 / [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 시스템 / [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 시스템은 그 결과를 더 강하게 만들거나 다른 방향으로 확장한다. 이 차이를 구분해야 시험 답안에서도 경계와 선택 이유를 설득할 수 있다.

| 비교 축 | [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 | [Saga](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/) 패턴 | [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 시스템 / [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 시스템 / [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 시스템 |
| :--- | :--- | :--- | :--- |
| 초점 | 현재 주제가 직접 통제하는 병목과 제약에 집중한다. | 바로 앞 단계나 전제를 다룬다. | 후속 확장 또는 보완 역할이 강하다. |
| 적용 시점 | 현재 개념이 요구되는 순간에 핵심 제어점으로 작동한다. | 준비·선행 판단에서 먼저 등장한다. | 세부 최적화나 확장에서 더 자주 등장한다. |
| 주된 위험 | 과신하면 비용 대비 효과가 줄어든다. | 부족하면 현재 개념도 안정적으로 성립하지 않는다. | 무작정 적용하면 복잡도와 운영 부담이 커질 수 있다. |

또한 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 단순 정의 암기로 끝나는 개념이 아니라, 실제로는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·정합성·운영성 중 무엇을 우선할지 결정하는 기준점으로 연결된다.

- **📢 섹션 요약 비유**: [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 본사와 지점 규칙을 조율하는 일에 가깝다. 중요한 것은 순서를 정하고 책임 범위를 분명히 하는 일이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리를 문법이나 이론 용어로만 이해하면 부족하다. 여러 리전에 걸친 주문·결제 서비스에서는 이 개념이 곧 응답시간, 충돌 빈도, 운영 복잡도 차이로 드러난다. 따라서 채택 여부를 결정할 때는 현재 개념이 병목을 줄이는지, 아니면 단지 구조만 복잡하게 만드는지부터 확인해야 한다.

### 기술사 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 워크로드에서 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리가 해결하는 병목이 실제로 존재하는가?
2. `Saga 패턴`나 `CP 시스템 / AP 시스템 / CA 시스템`으로 더 단순하게 풀 수 없는가?
3. 장애·튜닝·모니터링 시 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리를 관찰할 지표와 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 전략이 준비되어 있는가?

결론적으로 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 "무조건 채택"의 대상이 아니라, 보장 가치와 운영 비용을 함께 따져 선택해야 하는 설계 포인트다.

- **📢 섹션 요약 비유**: [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 해외 지사 결재선을 맞추는 일에 가깝다. 중요한 것은 순서를 정하고 책임 범위를 분명히 하는 일이다.

---

## Ⅴ. 기대효과 및 결론

[CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리를 올바르게 적용하면 구조를 단순화하고, 정합성을 높이거나 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 안정화하며, 장애 대응 속도까지 개선할 수 있다. 반대로 적용 위치를 잘못 잡으면 중복 설계와 불필요한 복잡도만 늘어난다. 그래서 이 주제는 정의 하나보다도 "어디에 두어야 하는가"라는 배치 감각으로 기억하는 것이 중요하다.

특히 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 독립 개념처럼 보이지만 실제로는 `Saga 패턴`과 `CP 시스템 / AP 시스템 / CA 시스템` 사이의 연결점으로 이해해야 오래 남는다. 시험에서는 정의·비교·판단 기준을 함께 말하고, 실무에서는 지표와 운영 시나리오까지 연결할 수 있어야 완성도 있는 답안이 된다.

- **📢 섹션 요약 비유**: [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 멀리 떨어진 팀 릴레이를 맞추는 일에 가깝다. 중요한 것은 순서를 정하고 책임 범위를 분명히 하는 일이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [3단계 커밋](/knowledge-base/studynote/05_database/04_transactions_concurrency/251_three_phase_commit_3pc_blocking_solution/) (3PC, Three-Phase Commit) | 앞뒤 맥락에서 현재 주제의 경계를 선명하게 해 주는 인접 개념이다. |
| [Saga](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/) 패턴 | 앞뒤 맥락에서 현재 주제의 경계를 선명하게 해 주는 인접 개념이다. |
| [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) ([Replication](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)과 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 논의를 실제 구조로 연결한다. |
| 합의 (Consensus) | 여러 노드가 하나의 결과에 도달하는 메커니즘이다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Saga 패턴</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">CAP 정리</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">CP 시스템 / AP 시스템 / CA 시스템</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">PACELC 정리</div></div>
</div>
</div>



[Saga](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/) 패턴에서 출발한 논점이 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리에서 핵심 판단으로 모이고, 이후 [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 시스템 / [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 시스템 / [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 시스템·[PACELC](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 정리 같은 확장 주제로 이어지는 흐름을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 컴퓨터가 일을 헷갈리지 않게 하려고 만든 약속이에요.
2. 이 약속을 잘 지키면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 많아도 더 안전하고 빠르게 움직일 수 있어요.
3. 그래서 언제 이 방법을 쓰고 언제 다른 방법을 써야 하는지 아는 것이 중요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 253 / 600

← **이전**: [252. Saga 패턴 (Saga Pattern)](/knowledge-base/studynote/05_database/04_transactions_concurrency/252_saga_pattern/)
**다음**: [254. CP 시스템 / AP 시스템 / CA 시스템 (HBase, MongoDB 기본)](/knowledge-base/studynote/05_database/04_transactions_concurrency/254_cp_ap_systems/) →

---
