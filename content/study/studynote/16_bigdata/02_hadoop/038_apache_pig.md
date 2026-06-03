---
title: 16. 아파치 피그 (Apache Pig) - 하둡 데이터 흐름 스크립팅
date: '2026-03-04'
tags:
- hadoop
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
- 아파치 피그(Apache Pig)는 복잡한 [[018_mapreduce|맵리듀스]]([[018_mapreduce|MapReduce]]) 자바 코드를 직접 짜는 대신, 'Pig Latin'이라는 고수준 스크립트 언어로 [[001_dikw_pyramid|데이터]] 흐름을 정의하는 플랫폼임.
- 비개발자(분석가)도 조인([[521_join|Join]]), 필터링, [[535_grouping_counting_free_space|그룹화]] 등의 복잡한 [[001_dikw_pyramid|데이터]] 변환 작업을 직관적으로 수행할 수 있도록 [[198_abstraction_control_data_process|추상화]] 계층을 제공함.
- 대규모 [[004_unstructured_data|비정형 데이터]]의 [[215_etl_vs_elt_pipeline|ETL]](추출, 변환, 적재) [[123_pipe|파이프]]라인 구축에 최적화되어 있으며, [[298_qkv_attention|쿼리]] 최적화기를 통해 효율적인 [[018_mapreduce|맵리듀스]] [[166_execution_plan_optimizer_navigation_tree|실행 계획]]을 자동 [[087_process_state_transition|생성]]함.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
[[843_hadoop_rack_awareness_data_replication_topology|하둡]]의 [[459_quic_fec_forward_error_correction|초기]] [[018_mapreduce|맵리듀스]]는 자바(Java) 언어로 수백 줄의 코드를 짜야 하는 높은 진입 장벽이 있었다. 특히 여러 [[001_dikw_pyramid|데이터]]를 합치거나 복잡한 연산을 수행할 때마다 맵(Map)과 리듀스(Reduce) 로직을 일일이 설계하는 것은 매우 고통스러운 작업이었다. 야후(Yahoo!)는 이를 해결하기 위해 마치 SQL과 유사하면서도 절차적인 흐름을 표현할 수 있는 Pig Latin 언어를 개발했다. 이는 "돼지(Pig)는 무엇이든 먹는다"는 이름처럼 정형/비정형 모든 [[001_dikw_pyramid|데이터]]를 가리지 않고 처리하겠다는 철학을 담고 있다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

아파치 피그는 사용자의 스크립트를 분석하여 최적화된 [[018_mapreduce|맵리듀스]] 잡(Job)으로 변환하는 컴파일러 역할을 수행한다.

```text
[ Apache Pig Execution Architecture ]

  +-----------------------+
  |  Pig Latin Script     |  (User Input: LOAD, FILTER, GROUP...)
  +-----------+-----------+
              |
  +-----------v-----------+
  |  Pig Engine (Parser)  |  (Syntax Check & Logical Plan)
  +-----------+-----------+
              |
  +-----------v-----------+
  |  Optimizer (Planner)  |  (Optimization: Pushdown, Join Opt)
  +-----------+-----------+
              |
  +-----------v-----------+
  |  Execution Engine     |  (Compile to MapReduce / Tez / Spark)
  +-----------+-----------+
              |
  +-----------v-----------+
  |   Hadoop Cluster      |  (HDFS Data Processing)
  +-----------------------+

[ Bilingual Comparison ]
- Pig Latin: 피그 전용 데이터 흐름 언어.
- Grunt Shell: 피그 스크립트를 대화식으로 실행하는 셸 환경.
- Multi-Query Optimization: 여러 단계의 쿼리를 통합하여 중복 스캔 최소화.
- UDF (User Defined Function): 표준 연산 외에 자바 등으로 직접 짠 사용자 정의 함수.
```

사용자가 `LOAD 'data' -> FILTER -> GROUP -> STORE`와 같은 흐름을 정의하면, 피그 엔진은 이를 [[369_logic_bomb|논리]]적 계획(Logical Plan)으로 세우고, 실제 [[843_hadoop_rack_awareness_data_replication_topology|하둡]]에서 돌아가는 물리적 계획(Physical Plan)으로 변환하여 실행한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 아파치 피그 (Apache Pig) | 아파치 하이브 ([[028_apache_hive|Apache Hive]]) |
| :--- | :--- | :--- |
| **언어 형태** | Pig Latin (절차적/[[001_dikw_pyramid|데이터]] 흐름 지향) | HiveQL (선언적/SQL 기반) |
| **주요 사용자** | [[001_dikw_pyramid|데이터]] 엔지니어, 프로그래머 | [[001_dikw_pyramid|데이터]] 분석가, 비즈니스 분석가 |
| **적합한 작업** | **복잡한 [[215_etl_vs_elt_pipeline|ETL]], [[645_data_pipeline_acceleration|데이터 파이프라인]]** | 리포팅, [[002_structured_data|정형 데이터]] [[298_qkv_attention|쿼리]], [[209_data_warehouse_schema_on_write|DW]] |
| **[[005_schema|스키마]]** | 선택적 ([[505_schema|Schema]]-free 성격 강함) | 필수 (테이블 구조 미리 정의) |
| **[[198_abstraction_control_data_process|추상화]] 수준** | 중간 (절차를 세세히 제어 가능) | 높음 (결과만 선언) |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
- **(절차적 제어의 강점)** 하이브([[544_hive|Hive]])는 "결과(What)"를 묻는다면, 피그(Pig)는 "과정(How)"을 기술한다. [[266_data_cleansing|데이터 정제]] 과정에서 중간 단계의 [[001_dikw_pyramid|데이터]] 형태를 세밀하게 제어해야 하는 복잡한 [[215_etl_vs_elt_pipeline|ETL]] 작업에는 피그가 훨씬 유연하다.
- **([[282_performance_tactics|성능]] 최적화)** 피그는 [[018_mapreduce|맵리듀스]]의 고질적인 문제인 '디스크 I/O'를 줄이기 위해 여러 연산을 하나의 잡으로 묶어주는 기능을 제공한다. 그러나 현재는 스파크(Spark)의 등장으로 피그 역시 [[843_hadoop_rack_awareness_data_replication_topology|하둡]] 위에서 Tez나 Spark 엔진을 백엔드로 사용하도록 [[009_config|설정]]하여 속도를 개선하는 추세다.
- **(UDF의 활용)** 기본 제공 함수로 해결되지 않는 특수한 로직(예: 이미지 [[012_metadata|메타데이터]] 추출)은 자바로 UDF를 작성하여 피그 스크립트에 포함시킴으로써 확장성을 확보한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
아파치 피그는 [[018_mapreduce|맵리듀스]]의 복잡성을 획기적으로 낮춰 빅데이터 분석의 대중화를 이끈 선구적인 도구다. 비록 현재는 스파크(Spark)나 하이브([[544_hive|Hive]])에 밀려 사용 비중이 줄었으나, '[[001_dikw_pyramid|데이터]] 흐름([[001_dikw_pyramid|Data]] Flow)' 관점에서 [[123_pipe|파이프]]라인을 설계하는 철학은 현대의 에어플로우(Airflow)나 dbt 같은 도구들에 큰 영향을 주었다. 기술사는 과거의 유산인 피그의 설계를 이해함으로써 현대적 [[123_pipe|파이프]]라인 최적화의 원천 기술을 파악할 수 있다.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **[[395_hadoop_mapreduce_disk_bottleneck|Hadoop MapReduce]]**: 피그가 돌아가는 기저 엔진
- **Pig Latin**: 피그의 전용 언어
- **[[028_apache_tez|Apache Tez]]**: 피그의 실행 속도를 높여주는 차세대 엔진
- **[[215_etl_vs_elt_pipeline|ETL]] (Extract, Transform, Load)**: 피그의 주된 임무


### 📈 관련 키워드 및 발전 흐름도

```text
[Raw MapReduce (Java) — 낮은 수준 API, 반복적 보일러플레이트 코드]
    │
    ▼
[Apache Pig (Pig Latin) — 데이터 흐름 스크립팅 언어, MapReduce 자동 변환]
    │
    ▼
[Apache Hive (HiveQL) — SQL 기반 배치 질의, 메타스토어 스키마 관리]
    │
    ▼
[Apache Spark (DataFrame / SQL) — 인메모리 처리로 Pig/Hive 대비 10~100배 가속]
    │
    ▼
[Apache Flink / Beam — 스트림·배치 통합 파이프라인, Pig 역할의 현대적 계승]
```
이 흐름은 저수준 [[018_mapreduce|MapReduce]] 코드를 단순화하기 위해 등장한 Pig Latin이 [[001_dikw_pyramid|데이터]] 변환 [[123_pipe|파이프]]라인의 [[459_quic_fec_forward_error_correction|초기]] 표준이 되고, 이후 인메모리 처리와 스트림 통합 요건에 의해 Spark·Flink로 계승되는 [[843_hadoop_rack_awareness_data_replication_topology|하둡]] 생태계 [[001_dikw_pyramid|데이터]] 처리 [[198_abstraction_control_data_process|추상화]]의 발전을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
- 아주 어려운 수학 문제를 풀 때, 공식을 매번 증명해서 풀려면 너무 힘들겠지? (자바 [[018_mapreduce|맵리듀스]])
- 피그는 선생님이 미리 만들어둔 '만능 계산기'에 문제 순서만 입력하면 답을 내주는 도구야.
- 복잡한 요리 재료들을 순서대로 씻고, 썰고, 볶으라고 레시피만 적어주면 로봇이 요리해 주는 것과 같단다!
