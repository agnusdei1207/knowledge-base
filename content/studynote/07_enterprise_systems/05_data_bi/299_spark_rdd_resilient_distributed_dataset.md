---
title: 299. 스파크 RDD (Resilient Distributed Dataset)
date: '2026-03-04'
tags:
- studynote-enterprise
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[206_spark_inmemory_rdd_lazy_evaluation_lineage|아파치 스파크]]의 가장 기본적인 [[001_dikw_pyramid|데이터]] 구조로, 여러 노드에 흩어져 있는 [[001_dikw_pyramid|데이터]]를 하나의 불변([[298_immutable|Immutable]]) 객체처럼 다룰 수 있게 해주는 [[369_logic_bomb|논리]]적 [[001_dikw_pyramid|데이터]] 집합이다.
> 2. **가치**: [[001_dikw_pyramid|데이터]]를 물리적으로 [[016_replication_factor|복제]]하여 장애에 대비하는 대신, [[001_dikw_pyramid|데이터]]가 [[087_process_state_transition|생성]]된 과정(Lineage)을 기억함으로써 장애 발생 시 해당 부분만 즉시 재계산하여 [[658_ir_recovery|복구]]하는 고효율 [[571_resiliency_fault_tolerance_patterns|탄력성]]을 제공한다.
> 3. **판단 포인트**: 현대 스파크 개발은 상위 수준의 DataFrame이나 Dataset API를 권장하지만, 세밀한 [[514_partition_slice_volume|파티션]] 제어나 [[001_dikw_pyramid|데이터]] 변환의 근본 원리를 최적화하기 위해서는 RDD의 동작 방식을 반드시 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

기존의 [[018_mapreduce|맵리듀스]]는 [[001_dikw_pyramid|데이터]] 처리 중간 단계를 디스크에 기록했다. 이는 안정적이지만 연산 속도를 크게 떨어뜨리는 원인이 되었다. [[206_spark_inmemory_rdd_lazy_evaluation_lineage|아파치 스파크]]는 **"메모리에서 연산하되, [[001_dikw_pyramid|데이터]] 유실 위험은 어떻게 막을 것인가?"**라는 질문에 대한 답으로 RDD를 제시했다.

RDD는 [[001_dikw_pyramid|데이터]]를 메모리에 올려 [[148_5g_embb_urllc_mmtc|초고속]]으로 처리하면서도, 장애가 나면 **리니지(Lineage, 계보)**를 추적해 유실된 [[001_dikw_pyramid|데이터]]만 다시 만들어내는 '탄력적(Resilient)'인 특성을 갖는다.

- **📢 섹션 요약 비유**: 요리 과정을 매번 사진 찍어 보관(Disk I/O)하는 대신, 레시피(Lineage)를 기억하고 있다가 요리를 망치면 그 단계부터 다시 요리(Re-computation)하는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

RDD는 3가지 핵심 특징을 가진다: **Resilient(장애 [[658_ir_recovery|복구]] 가능), Distributed([[136_variance|분산]] 저장), Dataset([[001_dikw_pyramid|데이터]] 집합).**

```text
[원본 데이터 (HDFS 등)] ──▶ [RDD 1 (Filter)] ──▶ [RDD 2 (Map)] ──▶ [RDD 3 (Reduce)]
                                ▲
                                │ (Lineage 기록: RDD1에서 거른 뒤 Map을 적용함)
                                └───────────────────────────────────┘
```

| 주요 메커니즘 | 설명 | 특징 |
|:---|:---|:---|
| 불변성 (Immutability) | 한 번 [[087_process_state_transition|생성]]된 RDD는 수정 불가 | [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]] 유지 및 장애 [[658_ir_recovery|복구]] 단순화 |
| [[023_lazy_evaluation|지연 평가]] ([[023_lazy_evaluation|Lazy Evaluation]]) | 연산 요청 시 즉시 실행하지 않고 기록만 함 | 실제 결과가 필요할 때(Action) 최적의 경로로 한꺼번에 실행 |
| 리니지 (Lineage) | [[001_dikw_pyramid|데이터]] [[087_process_state_transition|생성]] 과정의 방향성 비순환 [[070_graph_datastructure|그래프]]([[401_bayesian_network_dag_causality|DAG]]) | 체크포인트 없이도 장애 노드의 [[001_dikw_pyramid|데이터]] 재생성 가능 |
| [[179_table_partitioning_concept|파티셔닝]] ([[179_table_partitioning_concept|Partitioning]]) | [[001_dikw_pyramid|데이터]]를 여러 노드에 나누어 저장 | [[430_index_fast_full_scan|병렬]] 처리의 기본 단위 |

- **📢 섹션 요약 비유**: 영화를 처음부터 끝까지 다 찍어두는 게 아니라, 대본(Lineage)만 가지고 있다가 배우(Node)가 실수하면 그 장면([[514_partition_slice_volume|Partition]])만 다시 찍는 원리다.

---

## Ⅲ. 비교 및 연결

RDD는 스파크의 1세대 API이며, 현재는 [[282_performance_tactics|성능]] 최적화가 가미된 DataFrame과 Dataset으로 진화했다.

| 항목 | [[310_audit|RDD]] (Low-level) | DataFrame / Dataset (High-level) |
|:---|:---|:---|
| [[001_dikw_pyramid|데이터]] 타입 | 일반 자바/파이썬 객체 (Type-[[093_safe_scaled_agile_framework_art_pi|safe]]) | [[005_schema|스키마]]가 정의된 행(Row) 객체 |
| 최적화 엔진 | 개발자의 코드 실력에 의존 | Catalyst Optimizer가 [[166_execution_plan_optimizer_navigation_tree|실행 계획]] 자동 최적화 |
| 사용 편의성 | 복잡한 [[216_lambda_kappa_architecture_batch_realtime|람다]]식 필요 | SQL 스타일의 직관적인 [[014_api_posix|API]] 제공 |
| 권장 용도 | [[004_unstructured_data|비정형 데이터]] 처리, 세밀한 제어 필요 시 | 대부분의 비즈니스 로직 및 [[002_structured_data|정형 데이터]] 분석 |

비록 상위 API를 주로 쓰더라도, 셔플(Shuffle)이나 [[514_partition_slice_volume|파티션]] 수 조정 같은 튜닝 작업 시에는 결국 [[310_audit|RDD]] 레벨의 이해가 필요하다.

- **📢 섹션 요약 비유**: RDD는 수동 변속기 자동차(정밀 제어 가능)이고, DataFrame은 자동 변속기 자동차(운전 편의성 및 효율 극대화)와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[310_audit|RDD]] 관련 가장 큰 이슈는 **셔플(Shuffle)**과 **[[001_dikw_pyramid|데이터]] 스큐([[001_dikw_pyramid|Data]] Skew)**다. 특정 노드에 [[001_dikw_pyramid|데이터]]가 몰리거나, 노드 간 [[001_dikw_pyramid|데이터]] 이동이 빈번해지면 [[282_performance_tactics|성능]]이 급격히 떨어진다.

### [[435_checklist_based_testing|체크리스트]]
1. 메모리 부족([[157_oom_killer|OOM]]) 장애가 빈번한가? -> `persist()`나 `cache()` [[268_strategy_pattern|전략]] [[396_validation|확인]] 필요.
2. 특정 단계에서 연산이 너무 오래 걸리는가? -> [[001_dikw_pyramid|데이터]] 리티션(Re-[[514_partition_slice_volume|partition]])이나 셔플링 최소화 여부 [[396_validation|확인]].
3. 장애 [[658_ir_recovery|복구]] 시간이 너무 긴가? -> 리니지가 너무 길어지면 중간에 `checkpoint`를 [[009_config|설정]]했는지 [[396_validation|확인]].

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 모든 중간 결과를 무분별하게 `cache()` 하는 것. 메모리 자원을 낭비하여 오히려 전체 시스템 속도를 늦출 수 있다.

- **📢 섹션 요약 비유**: 레시피가 너무 길면 중간에 요리 과정을 사진 찍어둬야(Checkpoint) 기억하기 쉽지, 머리(Memory)만 믿고 있다가는 과부하가 올 수 있다.

---

## Ⅴ. 기대효과 및 결론

RDD는 빅데이터 처리의 패러다임을 '기록'에서 '계산'으로 바꾼 혁신적인 아이디어다. 이를 통해 스파크는 [[843_hadoop_rack_awareness_data_replication_topology|하둡]]보다 압도적인 [[282_performance_tactics|성능]]을 낼 수 있었고, 현재의 [[190_ai_llm_requirements_specification|AI]] 및 실시간 분석 시대를 여는 초석이 되었다.

결론적으로 RDD는 스파크의 심장이며, [[136_variance|분산]] 컴퓨팅 환경에서 **[[282_performance_tactics|성능]]과 안정성**이라는 두 마리 토끼를 잡기 위한 가장 영리한 설계 방식이다.

- **📢 섹션 요약 비유**: 도미노를 하나씩 세우는 것보다, 넘어진 곳부터 다시 세우는 규칙을 잘 정해두는 것이 전체 도미노 쇼를 성공시키는 비결인 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 변환 (Transformation) | `map`, `filter` 등 새로운 RDD를 만드는 [[015_지연_데이터_관점|지연]] 연산 |
| 액션 (Action) | `count`, `collect` 등 실제 계산을 수행하고 결과를 반환하는 연산 |
| [[401_bayesian_network_dag_causality|DAG]] ([[255_apache_airflow_dag|Directed Acyclic Graph]]) | [[310_audit|RDD]] 간의 의존 [[083_relationship_in_er_model|관계]]를 나타내는 [[166_execution_plan_optimizer_navigation_tree|실행 계획]] 지도 |

### 📈 관련 키워드 및 발전 흐름도

```
Hadoop MapReduce - 디스크 기반 중간 결과 저장
    │
    ▼
Spark RDD - 인메모리 분산 데이터셋 추상화
    │
    ▼
Transformation (지연 평가) + Action (실행 트리거)
    │
    ▼
DataFrame/Dataset API - 스키마 기반 최적화
    │
    ▼
Catalyst Optimizer + Tungsten 메모리 관리
```

> **키워드**: [[310_audit|RDD]], [[025_spark_rdd_resilient_distributed_dataset|Resilient Distributed Dataset]], Spark, [[023_lazy_evaluation|Lazy Evaluation]], Lineage, DataFrame, Catalyst

### 👶 어린이를 위한 3줄 비유 설명
1. 거대한 퍼즐을 친구들이 나누어서 맞추고 있어요.
2. 조각 하나를 잃어버려도, "어디서 온 조각인지" 적힌 설명서가 있어서 금방 새로 만들 수 있어요.
3. 처음부터 퍼즐을 다시 다 맞출 필요가 없어서 아주 빠르게 완성할 수 있답니다!
