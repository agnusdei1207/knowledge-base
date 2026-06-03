+++
weight = 55
title = "04. Spark SQL & DataFrame — 정형 데이터 처리 및 최적화"
date = "2026-04-14"
[extra]
categories = "studynote-bigdata"
+++

# [[056_spark_sql|Spark SQL]] & DataFrame - [[002_structured_data|정형 데이터]] 처리 및 Catalyst 최적화

> ⚠️ 이 문서는 RDD의 한계([[005_schema|스키마]] 부재, 최적화 어려움)를 극복하고 대규모 [[002_structured_data|정형 데이터]]를 SQL과 DataFrame API로 [[148_5g_embb_urllc_mmtc|초고속]] 처리하는 Spark SQL의 핵심 아키텍처, Catalyst [[163_optimizer_sql_execution_plan_generator|옵티마이저]], 그리고 Tungsten 실행 엔진의 물리적 최적화 메커니즘을 기술사 수준에서 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Spark SQL은 [[310_audit|RDD]] 위에 [[001_dikw_pyramid|데이터]] [[005_schema|스키마]]([[505_schema|Schema]]) 레이어를 추가하여, 사용자가 SQL이나 DataFrame API로 작성한 [[369_logic_bomb|논리]]적 의사를 Catalyst [[163_optimizer_sql_execution_plan_generator|옵티마이저]]를 통해 최적화된 물리적 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]으로 자동 변환해주는 고수준 [[002_structured_data|정형 데이터]] 처리 엔진이다.
> 2. **가치**: 개발자가 직접 [[179_table_partitioning_concept|파티셔닝]]이나 조인 방식을 고민하지 않아도 '카탈리스트(Catalyst)'가 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]을 최적화하고, '텅스텐(Tungsten)' 엔진이 자바 객체 오버헤드를 제거한 바이너리 수준의 메모리 관리를 수행하여 [[310_audit|RDD]] 대비 압도적인 [[282_performance_tactics|성능]]과 생산성을 제공한다.
> 3. **융합**: 외부 [[001_dikw_pyramid|데이터]] 소스([[178_parquet_rle_encoding_columnar_compression|Parquet]], Avro, JDBC, [[343_json|JSON]])와 결합하여 [[208_data_lake_schema_on_read|데이터 레이크]]의 [[004_unstructured_data|비정형 데이터]]와 DW의 [[002_structured_data|정형 데이터]]를 하나의 [[298_qkv_attention|쿼리]]로 통합 분석하며, 현대 [[210_data_lakehouse_delta_lake|데이터 레이크하우스]]([[146_lakehouse|Lakehouse]]) 아키텍처의 핵심 연산 표준으로 자리 잡았다.

---

## Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

### 1. RDD의 한계와 Spark SQL의 탄생
[[459_quic_fec_forward_error_correction|초기]] 스파크의 RDD는 강력한 [[136_variance|분산]] 처리 기능을 제공했지만, 두 가지 결정적인 숙제가 있었습니다.
- **[[005_schema|스키마]]의 부재**: [[310_audit|RDD]] 내부 [[001_dikw_pyramid|데이터]]는 단순한 자바/파이썬 객체로 취급되어 스파크가 [[001_dikw_pyramid|데이터]] 내부 구조(컬럼 명, 타입)를 알 수 없었습니다. 이로 인해 특정 컬럼만 필터링하거나 조인할 때 불필요한 [[149_serial_communication_rs232_rs485|직렬]]화/역직렬화 오버헤드가 발생했습니다.
- **최적화의 어려움**: 사용자가 작성한 [[310_audit|RDD]] 코드는 스파크 입장에서 블랙박스와 같아, 더 효율적인 실행 순서가 있어도 스파크가 마음대로 로직을 바꿀 수 없었습니다.

### 2. Spark SQL의 목적
Spark SQL은 이러한 RDD의 한계를 넘어서기 위해 탄생했습니다.
- **선언적 프로그래밍**: "어떻게(How)" 연산할지가 아니라 "무엇(What)"을 얻고 싶은지를 SQL로 선언하면 스파크가 최적의 경로를 찾습니다.
- **통합 [[001_dikw_pyramid|데이터]] 인터페이스**: 하이브([[544_hive|Hive]]) 메타스토어와 호환되며, 다양한 포맷의 [[001_dikw_pyramid|데이터]]를 동일한 DataFrame 객체로 [[198_abstraction_control_data_process|추상화]]하여 처리합니다.

- **📢 섹션 요약 비유**: RDD가 요리사에게 "칼을 들고, 양파를 5mm 간격으로 썰고, 팬을 180도로 달궈라"라고 일일이 지시하는 수동 요리라면, Spark SQL은 "제일 맛있는 양파 볶음 하나 내와"라고 주문하는 **'최고급 레스토랑의 키오스크'**와 같습니다. 주방장(Catalyst)이 가장 신선한 재료를 골라 최적의 순서로 요리해 줍니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 ([[319_architecture|Architecture]] & Mechanism)

Spark SQL의 [[282_performance_tactics|성능]]을 결정짓는 두 핵심 기둥은 **Catalyst [[163_optimizer_sql_execution_plan_generator|옵티마이저]]**와 **Tungsten 실행 엔진**입니다.

### 1. Catalyst [[163_optimizer_sql_execution_plan_generator|옵티마이저]] (Query Optimization [[082_pipeline|Pipeline]])
사용자가 던진 SQL은 4단계의 엄격한 최적화 과정을 거쳐 실행됩니다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                 [ Catalyst Optimizer 실행 파이프라인 ]                      │
│                 [ Catalyst Optimization Pipeline ]                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [ Unresolved Logical Plan ] ──▶ [ Analysis (Analyzer) ] ──▶ [ Resolved LP ]│
│  (구문 분석 전 계획)              (카탈로그 참조/바인딩)      (확정된 논리 계획)│
│                                                                   │         │
│  ┌────────────────────────────────────────────────────────────────┘         │
│  ▼                                                                          │
│  [ Logical Optimization ] ──▶ [ Optimized Logical Plan ]                    │
│  (Rule-based: 필터 푸시다운 등) (최적화된 논리 계획)                        │
│                                         │                                   │
│  ┌──────────────────────────────────────┘                                   │
│  ▼                                                                          │
│  [ Physical Planning ] ──▶ [ Cost Model ] ──▶ [ Selected Physical Plan ]    │
│  (여러 물리적 경로 생성)     (비용 기반 선택)     (최종 실행 계획 선정)      │
│                                                         │                   │
│  ┌──────────────────────────────────────────────────────┘                   │
│  ▼                                                                          │
│  [ Code Generation (Whole-Stage Codegen) ] ──▶ [ Java Bytecode Execution ]  │
│  (런타임 최적화 코드 생성)                      (실제 분산 실행)            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

- **Filter Pushdown**: [[001_dikw_pyramid|데이터]]를 다 읽은 후 거르는 것이 아니라, [[001_dikw_pyramid|데이터]] 소스 수준에서 미리 필터링하여 네트워크 전송량을 최소화합니다.
- **Projection [[435_pruning_hardware|Pruning]]**: 필요한 컬럼만 선택하여 메모리 낭비를 줄입니다.

### 2. Tungsten 실행 엔진 (Physical Optimization)
소프트웨어 수준의 최적화를 넘어 하드웨어 효율을 극한으로 끌어올립니다.
- **Off-[[078_heap_datastructure|heap]] Memory Mgmt**: 자바 객체(JVM [[078_heap_datastructure|Heap]]) 대신 바이너리 [[001_dikw_pyramid|데이터]]를 직접 관리하여 GC([[380_garbage_collection|Garbage Collection]]) 부하를 제거합니다.
- **Cache-aware Computation**: CPU 캐시 계층을 고려한 [[001_algorithm_definition|알고리즘]] 설계로 메모리 [[140_bandwidth|대역폭]] 병목을 해결합니다.
- **Whole-Stage [[082_process_memory_structure|Code]] Generation**: 여러 연산 단계를 하나의 거대한 자바 함수로 합쳐서 실행하여 [[294_function_calling_tool_use|함수 호출]] 오버헤드를 압살합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### DataFrame vs SQL 연산 비교

| 비교 항목 | DataFrame [[014_api_posix|API]] | [[056_spark_sql|Spark SQL]] |
| :--- | :--- | :--- |
| **언어 인터페이스** | Python, Scala, Java (DSL 방식) | 표준 SQL (String 기반) |
| **[[333_readability_vs_efficiency|가독성]]** | 프로그래밍 로직과 융합 시 유리 | [[001_dikw_pyramid|데이터]] 분석가 및 기존 SQL 유저 친화적 |
| **컴파일 타임 체크** | Syntax 체크 가능 (Typed Dataset인 경우) | 런타임에 구문 에러 발견 가능성 높음 |
| **[[282_performance_tactics|성능]] (Catalyst)** | **동일함 (결국 같은 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]으로 변환됨)** | **동일함** |

### [[002_structured_data|정형 데이터]] 포맷 비교 ([[234_columnar_storage_parquet_orc|Columnar Storage]] 시너지)

| 포맷 | 특징 | Spark SQL과의 궁합 |
| :--- | :--- | :--- |
| **CSV / [[343_json|JSON]]** | 행(Row) 기반, 텍스트 형식 | [[005_schema|스키마]] 추론 오버헤드 발생, 분석 속도 느림 |
| **[[178_parquet_rle_encoding_columnar_compression|Parquet]]** | **컬럼(Column) 기반**, 바이너리 저장 | **최상**. 필요한 컬럼만 읽기([[435_pruning_hardware|Pruning]]) 및 [[347_compaction|압축]] 최적화 |
| **Avro** | [[005_schema|스키마]] 포함 행 기반 저장 | [[001_dikw_pyramid|데이터]] 수집(Ingestion) 및 [[149_serial_communication_rs232_rs485|직렬]]화에 유리 |

- **📢 섹션 요약 비유**: RDD가 모든 [[001_dikw_pyramid|데이터]]를 무거운 '나무 상자(Java Object)'에 담아 옮기는 것이라면, DataFrame과 Tungsten은 [[001_dikw_pyramid|데이터]]를 아주 얇은 '슬림한 비닐 팩(Binary)'에 담아 컨베이어 벨트에 올리는 것과 같습니다. 상자를 뜯는 시간도 안 걸리고, 컨베이어 벨트(CPU)에 훨씬 더 많이 올릴 수 있습니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

### 기술사적 판단: [[056_spark_sql|Spark SQL]] 튜닝 및 의사결정 시나리오

**시나리오 1: 1TB 테이블과 1GB 테이블의 조인([[521_join|Join]]) [[282_performance_tactics|성능]] 문제**
- **판단**: 일반적인 Shuffle Hash Join은 모든 [[001_dikw_pyramid|데이터]]를 네트워크로 보내야 하므로 매우 느리다. 1GB 테이블은 모든 익제큐터 메모리에 올릴 수 있으므로 **'Broadcast [[174_hash_join|Hash Join]]'**을 강제(`broadcast` [[167_sql_hint_optimizer_override|힌트]])한다. 이를 통해 네트워크 셔플을 원천 차단하고 로컬 조인으로 [[282_performance_tactics|성능]]을 10배 이상 개선한다.

**시나리오 2: 하이브([[544_hive|Hive]])에서 스파크로 대규모 마이그레이션**
- **판단**: 기존 [[544_hive|Hive]] SQL [[298_qkv_attention|쿼리]]를 그대로 가져오되, [[001_dikw_pyramid|데이터]] 저장 포맷을 반드시 **[[178_parquet_rle_encoding_columnar_compression|Parquet]]**나 **ORC**로 전환한다. 또한 `spark.sql.shuffle.partitions` 값을 기본값(200)에서 [[001_dikw_pyramid|데이터]] 규모에 맞게 수천 개로 조정하여 리소스 [[452_availability|가용성]]을 극대화한다.

```text
┌─────────────────────────────────────────────────────────────┐
│               [ Spark SQL Tuning Checklist ]                │
│               [ 스파크 SQL 성능 튜닝 체크리스트 ]           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. [Data Format]   : Parquet/ORC 사용 및 Partitioning 적용 │
│  2. [Join Strategy] : 소량 데이터는 Broadcast Join 활용     │
│  3. [Bucketing]     : 잦은 Join 키는 미리 버케팅하여 저장   │
│  4. [Caching]       : 반복 사용 DataFrame은 .cache() 처리   │
│  5. [Plan Check]    : .explain()으로 Shuffle 발생 지점 확인 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### [[056_spark_sql|Spark SQL]] 도입의 정량적 가치
1. **[[282_performance_tactics|성능]] 향상**: [[310_audit|RDD]] 대비 복잡한 조인 연산에서 5~10배 이상의 스루풋([[139_throughput|Throughput]]) 개선.
2. **생산성 증대**: SQL만 알면 빅데이터 엔지니어가 아니어도 수천억 건의 [[001_dikw_pyramid|데이터]]를 직접 분석 가능.

### 미래 전망: [[210_data_lakehouse_delta_lake|데이터 레이크하우스]]와 [[087_process_state_transition|생성]]형 [[190_ai_llm_requirements_specification|AI]]
Spark SQL은 이제 단순 [[298_qkv_attention|쿼리]] 엔진을 넘어, **[[147_delta_lake|Delta Lake]]**나 **[[148_apache_iceberg|Apache Iceberg]]**와 결합하여 [[208_data_lake_schema_on_read|데이터 레이크]] 위에서 ACID [[191_transaction_concept_states|트랜잭션]]을 보장하는 '[[210_data_lakehouse_delta_lake|데이터 레이크하우스]]'의 심장이 되었습니다. 또한 텍스트로 질문하면 SQL을 [[087_process_state_transition|생성]]해주는 AI와의 결합을 통해 [[010_data_democratization|데이터 민주화]]를 더욱 가속화할 것입니다.

- **📢 섹션 요약 비유**: Spark SQL은 빅데이터 세상의 **'공용어(English)'**가 되었습니다. 사투리([[310_audit|RDD]] 고유 로직)를 몰라도 세계 표준(SQL)만 알면 누구나 거대한 [[001_dikw_pyramid|데이터]]의 바다를 항해할 수 있게 된 것입니다.

---

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **[[057_catalyst_optimizer|Catalyst Optimizer]]**: [[298_qkv_attention|쿼리]] 최적화의 두뇌 (Rule/Cost Based)
- **Tungsten**: 메모리/CPU 효율 극대화의 심장
- **Broadcast [[521_join|Join]]**: 네트워크 셔플을 피하는 조인 기술
- **[[210_data_lakehouse_delta_lake|Data Lakehouse]]**: [[208_data_lake_schema_on_read|데이터 레이크]]와 DW의 장점을 결합한 차세대 아키텍처

---

### 📈 관련 키워드 및 발전 흐름도

```text
[Catalyst Optimizer: 쿼리 최적화의 두뇌 (Rule/Cost Based)]
    │
    ▼
[Tungsten: 메모리/CPU 효율 극대화의 심장]
    │
    ▼
[Broadcast Join: 네트워크 셔플을 피하는 조인 기술]
    │
    ▼
[Data Lakehouse: 데이터 레이크와 DW의 장점을 결합한 차세대 아키텍처]
```

이 흐름도는 [[057_catalyst_optimizer|Catalyst Optimizer]]: [[298_qkv_attention|쿼리]] 최적화의 두뇌 (Rule/Cost Based)에서 출발해 [[210_data_lakehouse_delta_lake|Data Lakehouse]]: [[208_data_lake_schema_on_read|데이터 레이크]]와 DW의 장점을 결합한 차세대 아키텍처까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. Spark SQL은 아주 똑똑한 **'[[001_dikw_pyramid|데이터]] 도서관 사서'** 선생님이에요.
2. 우리가 "빨간 책 중에서 작년에 나온 것만 찾아주세요"라고 SQL로 말하면, 사서 선생님이 도서관을 다 뒤지지 않고 가장 빠른 길로 가서 딱 필요한 책만 가져다줘요.
3. 선생님 덕분에 우리는 어려운 도서 번호를 몰라도 쉽고 빠르게 공부하고 싶은 내용을 찾을 수 있답니다!
