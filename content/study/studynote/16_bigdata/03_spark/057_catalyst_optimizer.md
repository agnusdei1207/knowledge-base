+++
weight = 57
title = "Catalyst Optimizer"
date = "2024-03-23"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
- Catalyst는 [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] SQL의 핵심 [[298_qkv_attention|쿼리]] 최적화 엔진으로, Scala의 [[324_functional_programming_core|함수형 프로그래밍]] 특성을 활용해 [[298_qkv_attention|쿼리]] [[166_execution_plan_optimizer_navigation_tree|실행 계획]]을 자동으로 개선한다.
- [[369_logic_bomb|논리]]적 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]을 물리적 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]으로 변환하는 과정에서 Rule-based 및 Cost-based 최적화를 수행하여 [[136_variance|분산]] 처리 [[282_performance_tactics|성능]]을 극대화한다.
- 확장 가능한 구조를 가지고 있어, [[001_dikw_pyramid|데이터]] 소스 개발자들이 자신만의 최적화 규칙을 쉽게 추가할 수 있는 유연성을 제공한다.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
- **정의**: Spark SQL과 DataFrame/Dataset API의 하단에서 작동하는 확장 가능한 [[298_qkv_attention|쿼리]] [[163_optimizer_sql_execution_plan_generator|옵티마이저]] 프레임워크다.
- **배경**: 개발자가 작성한 SQL이나 DataFrame 코드는 항상 최적의 [[282_performance_tactics|성능]]을 보장하지 않는다. Catalyst는 이를 분석하여 [[001_dikw_pyramid|데이터]] 필터링 시점 최적화(Predicate Pushdown), 필요한 열만 선택(Projection [[435_pruning_hardware|Pruning]]) 등을 자동으로 수행한다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

```text
[ Catalyst Optimization Pipeline ]

 (Unresolved)     (Resolved)      (Optimized)      (Physical)
 Logical Plan --> Logical Plan --> Logical Plan -->  Plans  --> [Code Generation]
      |               |               |               |              |
  [Analyzer]      [Catalyst]      [Optimizer]    [Cost Model]    [Tungsten]
      |               |               |               |              |
  Catalog info    Standard Rules   CBO/RBO        Selection       Java Bytecode
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 단계 | 주요 역할 | 최적화 예시 |
| :--- | :--- | :--- |
| **Analysis** | [[012_metadata|메타데이터]]([[394_catalog_metadata|Catalog]])를 [[316_reference_pattern_nosql|참조]]해 테이블/컬럼 존재 [[396_validation|확인]] | 잘못된 컬럼명 체크 및 바인딩 |
| **Logical Optimization** | [[369_logic_bomb|논리]]적인 [[038_relational_algebra|관계 대수]] 최적화 (RBO) | Predicate Pushdown (필터링 우선 수행) |
| **Physical Planning** | 실제 실행 가능한 여러 계획 [[087_process_state_transition|생성]] 및 CBO 적용 | Broadcast [[521_join|Join]] vs Shuffle [[521_join|Join]] 선택 |
| **[[082_process_memory_structure|Code]] Generation** | 런타임에 최적화된 Java [[074_byte|바이트]]코드 [[087_process_state_transition|생성]] | 전체 [[298_qkv_attention|쿼리]]를 하나의 함수처럼 실행 (Whole-stage CodeGen) |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
- **CBO(Cost-Based [[088_optimizer|Optimizer]]) 활성화**: [[001_dikw_pyramid|데이터]] 통계 정보가 최신일 때 최적의 [[282_performance_tactics|성능]]을 낸다. `ANALYZE TABLE` 명령을 통해 통계를 [[087_process_state_transition|생성]]하면 Catalyst가 [[176_join_order_optimization|조인 순서]]를 더 지능적으로 결정한다.
- **디버깅 [[268_strategy_pattern|전략]]**: `explain(true)` 명령을 사용하면 분석 전(Parsed), 분석 후(Analyzed), 최적화 후(Optimized), 물리적(Physical) 계획을 모두 [[396_validation|확인]]하여 병목 지점을 파악할 수 있다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- Catalyst 덕분에 Spark는 언어(Python, Scala, SQL)에 상관없이 동일한 고성능을 보장할 수 있게 되었다. 최근에는 기계 학습 모델을 [[298_qkv_attention|쿼리]] 최적화에 도입하거나, 런타임 상황에 따라 계획을 수정하는 AQE(Adaptive Query Execution)와 결합되어 더욱 진화하고 있다.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **부모 개념**: [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]], [[056_spark_sql|Spark SQL]]
- **자식 개념**: RBO(Rule-Based), CBO(Cost-Based), [[082_process_memory_structure|Code]] Generation
- **연관 개념**: [[058_tungsten_engine|Tungsten Engine]], AQE, DataFrame [[014_api_posix|API]]

### 📈 관련 키워드 및 발전 흐름도

```text
[논리 계획 (Logical Plan)]
    │
    ▼
[물리 계획 (Physical Plan)]
    │
    ▼
[Catalyst Optimizer (Catalyst Optimizer)]
    │
    ▼
[코드 생성 (Code Generation)]
```

이 흐름도는 [[369_logic_bomb|논리]] 계획이 물리 계획을 거쳐 Catalyst Optimizer와 코드 [[087_process_state_transition|생성]]으로 구체화되는 흐름을 보여준다.
### 👶 어린이를 위한 3줄 비유 설명
- 우리가 시장에 가서 물건을 살 때, "어느 가게를 먼저 들러야 제일 빨리 끝날까?"를 미리 생각하는 똑똑한 비서예요.
- 어려운 수학 숙제를 할 때, 더 쉬운 풀이 방법이 없는지 찾아내서 계산 시간을 줄여준답니다.
- 이 비서 덕분에 우리가 어떻게 명령해도 컴퓨터는 가장 빠른 길로 일을 처리해요.
