+++
title = "268. 수평 분할 (Horizontal Fragmentation)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 수평 분할 (Horizontal [Fragmentation](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/))은 [튜플](/knowledge-base/studynote/05_database/02_modeling_normalization/063_relation_tuple_cardinality/)(행) 단위 분할, 셀렉트 연산에 초점을 맞춘 개념이다.
> 2. **가치**: 수평 확장과 유연한 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)이 필요할 때는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장과 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 먼저 설계해야 한다.
> 3. **판단 포인트**: 판단 포인트는 수평 분할을 어디에 적용해야 효과가 크고, 어떤 비용이나 제약이 따라오는지 함께 보는 데 있다.

---

## Ⅰ. 개요 및 필요성

수평 분할 (Horizontal [Fragmentation](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/))은 [튜플](/knowledge-base/studynote/05_database/02_modeling_normalization/063_relation_tuple_cardinality/)(행) 단위 분할, 셀렉트 연산에 초점을 맞춘 개념이다. 수평 확장과 유연한 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)이 필요할 때는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장과 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 먼저 설계해야 한다. [샤드 키](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/281_nosql_modeling_strategy/)와 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 잘못 정하면 핫스팟과 재배치 비용이 급증한다.

```text
┌──────────────────────────────────────────────────────────────┐
│ Client -> Router -> Current concept -> Shard/Replica         │
├──────────────────────────────────────────────────────────────┤
│ Traffic growth -> distribution -> scale-out                  │
└──────────────────────────────────────────────────────────────┘
```

이 그림은 수평 분할을 독립 기능이 아니라 전체 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름에서 특정 통제 지점을 맡는 구조로 이해해야 한다는 점을 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해 보여 준다.

- **📢 섹션 요약 비유**: 수평 분할은 도시를 구역별로 나눠 창고를 배치하는 일에 가깝다. 중요한 것은 순서를 정하고 책임 범위를 분명히 하는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

수평 분할은 결국 "언제 보고, 어디에서 적용하고, 무엇을 보장할 것인가"를 정하는 메커니즘이다. 특히 `데이터 분할 기법`과 `수직 분할` 사이에서 현재 주제가 맡는 책임을 분리해 보면 구조가 더 또렷해진다.

| 관점 | 설명 | 설계 포인트 |
| :--- | :--- | :--- |
| 핵심 대상 | 수평 분할은 `수평 분할 (Horizontal Fragmentation)`의 역할과 적용 범위를 규정한다. | 이름보다 입력·출력 경계를 먼저 정의해야 한다. |
| 작동 원리 | 핵심은 현재 개념을 어떤 시점에 평가하고 어떤 범위에 적용하느냐에 있다. | 언제 평가하고 언제 확정하는지가 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 정합성을 가른다. |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 영향 | 수평 분할은 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/), [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간, 운영 복잡도 중 적어도 하나에 직접 영향을 준다. | 이득과 비용을 같이 보지 않으면 과설계가 된다. |
| 운영 주의 | `데이터 분할 기법`·`수직 분할`과 경계를 혼동하면 적용 위치가 어긋난다. | 장애 시 관찰할 지표와 우회 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 미리 준비해야 한다. |

```text
┌──────────────────────────────────────────────────────────────┐
│ Shard key -> route -> current concept -> rebalance           │
├──────────────────────────────────────────────────────────────┤
│ Partition choice -> hotspot risk -> expansion cost           │
└──────────────────────────────────────────────────────────────┘
```

핵심은 수평 분할을 단순 옵션이 아니라 입력 조건, 처리 순서, 결과 보장을 함께 묶는 설계 규칙으로 보는 것이다. 그래서 구현 전에 평가 시점·충돌 지점·[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 가능성을 먼저 정리해야 한다.

- **📢 섹션 요약 비유**: 수평 분할은 인기 매장을 여러 지점으로 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)하는 일에 가깝다. 중요한 것은 순서를 정하고 책임 범위를 분명히 하는 일이다.

---

## Ⅲ. 비교 및 연결

수평 분할은 종종 `데이터 분할 기법` 또는 `수직 분할`과 같은 묶음으로 설명되지만, 세 개념의 관심사는 다르다. [데이터 분할 기법](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/267_data_fragmentation/)이 준비 단계나 전제에 가깝다면, 수평 분할은 실제 통제 지점을 잡고, [수직 분할](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/269_vertical_fragmentation/)은 그 결과를 더 강하게 만들거나 다른 방향으로 확장한다. 이 차이를 구분해야 시험 답안에서도 경계와 선택 이유를 설득할 수 있다.

| 비교 축 | 수평 분할 | [데이터 분할 기법](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/267_data_fragmentation/) | [수직 분할](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/269_vertical_fragmentation/) |
| :--- | :--- | :--- | :--- |
| 초점 | 현재 주제가 직접 통제하는 병목과 제약에 집중한다. | 바로 앞 단계나 전제를 다룬다. | 후속 확장 또는 보완 역할이 강하다. |
| 적용 시점 | 현재 개념이 요구되는 순간에 핵심 제어점으로 작동한다. | 준비·선행 판단에서 먼저 등장한다. | 세부 최적화나 확장에서 더 자주 등장한다. |
| 주된 위험 | 과신하면 비용 대비 효과가 줄어든다. | 부족하면 현재 개념도 안정적으로 성립하지 않는다. | 무작정 적용하면 복잡도와 운영 부담이 커질 수 있다. |

또한 수평 분할은 단순 정의 암기로 끝나는 개념이 아니라, 실제로는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·정합성·운영성 중 무엇을 우선할지 결정하는 기준점으로 연결된다.

- **📢 섹션 요약 비유**: 수평 분할은 택배 물량을 [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)별로 나누는 일에 가깝다. 중요한 것은 순서를 정하고 책임 범위를 분명히 하는 일이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 수평 분할을 문법이나 이론 용어로만 이해하면 부족하다. 글로벌 트래픽과 대량 이벤트 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 함께 처리하는 플랫폼에서는 이 개념이 곧 응답시간, 충돌 빈도, 운영 복잡도 차이로 드러난다. 따라서 채택 여부를 결정할 때는 현재 개념이 병목을 줄이는지, 아니면 단지 구조만 복잡하게 만드는지부터 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 한다.

### 기술사 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 워크로드에서 수평 분할이 해결하는 병목이 실제로 존재하는가?
2. `데이터 분할 기법`나 `수직 분할`으로 더 단순하게 풀 수 없는가?
3. 장애·튜닝·[모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 시 수평 분할을 관찰할 지표와 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 준비되어 있는가?

결론적으로 수평 분할은 "무조건 채택"의 대상이 아니라, 보장 가치와 운영 비용을 함께 따져 선택해야 하는 설계 포인트다.

- **📢 섹션 요약 비유**: 수평 분할은 지도 위에 매장을 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 배치하는 일에 가깝다. 중요한 것은 순서를 정하고 책임 범위를 분명히 하는 일이다.

---

## Ⅴ. 기대효과 및 결론

수평 분할을 올바르게 적용하면 구조를 단순화하고, 정합성을 높이거나 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 안정화하며, 장애 대응 속도까지 개선할 수 있다. 반대로 적용 위치를 잘못 잡으면 중복 설계와 불필요한 복잡도만 늘어난다. 그래서 이 주제는 정의 하나보다도 "어디에 두어야 하는가"라는 배치 감각으로 기억하는 것이 중요하다.

특히 수평 분할은 독립 개념처럼 보이지만 실제로는 `데이터 분할 기법`과 `수직 분할` 사이의 연결점으로 이해해야 오래 남는다. 시험에서는 정의·비교·판단 기준을 함께 말하고, 실무에서는 지표와 운영 시나리오까지 연결할 수 있어야 완성도 있는 답안이 된다.

- **📢 섹션 요약 비유**: 수평 분할은 큰 행사장에서 줄을 여러 개로 나누는 일에 가깝다. 중요한 것은 순서를 정하고 책임 범위를 분명히 하는 일이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 병행 투명성 ([Concurrency](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/266_other_transparency/)) / 장애 투명성 (Failure) / 지역 사상 투명성 (Local [Mapping](/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/)) | 앞뒤 맥락에서 현재 주제의 경계를 선명하게 해 주는 인접 개념이다. |
| [데이터 분할 기법](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/267_data_fragmentation/) ([Fragmentation](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)) | 앞뒤 맥락에서 현재 주제의 경계를 선명하게 해 주는 인접 개념이다. |
| [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) ([Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/)) | 수평 확장과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 배치를 결정하는 핵심 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다. |
| [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) ([Replication](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)) | 장애 대응과 읽기 확장을 현실화한다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 분할 기법]
    │
    ▼
[수평 분할]
    │
    ├──▶ [수직 분할]
    └──▶ [복제]
```

[데이터 분할 기법](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/267_data_fragmentation/)에서 출발한 논점이 수평 분할에서 핵심 판단으로 모이고, 이후 [수직 분할](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/269_vertical_fragmentation/)·[복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 같은 확장 주제로 이어지는 흐름을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 수평 분할은 컴퓨터가 일을 헷갈리지 않게 하려고 만든 약속이에요.
2. 이 약속을 잘 지키면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 많아도 더 안전하고 빠르게 움직일 수 있어요.
3. 그래서 언제 이 방법을 쓰고 언제 다른 방법을 써야 하는지 아는 것이 중요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 268 / 600

← **이전**: [267. 데이터 분할 기법 (Fragmentation)](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/267_data_fragmentation/)
**다음**: [269. 수직 분할 (Vertical Fragmentation)](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/269_vertical_fragmentation/) →

---
