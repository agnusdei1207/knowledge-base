+++
title = "Tungsten Engine"
date = 2024-03-23

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
- Tungsten은 Spark의 하드웨어 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 극한으로 끌어올리기 위한 실행 엔진 최적화 프로젝트로, 메모리 관리와 CPU 효율성에 집중한다.
- JVM 객체 오버헤드를 피하기 위해 자체적인 Off-[heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/) 메모리 관리와 바이너리 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포맷을 사용한다.
- Whole-stage [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) Generation을 통해 런타임에 최적화된 [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)코드를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하여 가상 [함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/) 오버헤드를 제거한다.

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
- **정의**: Spark의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 속도를 개선하기 위해 하드웨어 아키텍처(CPU, RAM)를 최대한 활용하도록 설계된 엔진 계층이다.
- **배경**: Spark의 병목 현상이 네트워크/디스크 I/O에서 CPU와 메모리로 이동함에 따라, Java 객체의 높은 메모리 사용량과 GC([Garbage Collection](/knowledge-base/studynote/02_operating_system/06_memory_management/380_garbage_collection/)) 부하를 해결하기 위해 등장했다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- <strong><a href="/knowledge-base/studynote/09_security/uncategorized/610_memory_management/">Memory Management</a> &amp; Binary Processing</strong>: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 Java 객체로 변환하지 않고 바이너리 형태로 메모리에 직접 저장한다. Unsafe Row 형식을 사용하여 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 비용을 최소화한다.
- **Cache-aware Computation**: CPU 캐시(L1/L2/L3)의 지역성(Locality)을 고려한 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 사용하여 캐시 미스를 줄인다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Tungsten CPU &amp; Memory Optimization</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Standard JVM Approach</div><div class="kb-diagram-node">Tungsten Approach</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Java Object (Rich)</div><div class="kb-diagram-cell">Binary Data (Row format)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Metadata, Padding)</div><div class="kb-diagram-cell">&lt;----&gt;</div><div class="kb-diagram-cell">(Compact, No Metadata)</div></div>
<div class="kb-diagram-note">High GC Pressure Direct Memory Access</div>
<div class="kb-diagram-note">High Cache Misses Cache-aware Algorithms</div>
</div>
</div>



### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 최적화 기법 | 주요 내용 | 기대 효과 |
| :--- | :--- | :--- |
| <strong>Off-<a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/">heap</a> Memory</strong> | JVM 힙 외부에서 메모리 직접 관리 | GC 부하 제거 및 대용량 메모리 효율성 |
| **Binary Row Format** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 바이너리 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 형태로 유지 | 메모리 사용량 감소 (객체 오버헤드 제거) |
| **Whole-stage CodeGen** | 여러 연산([Select](/knowledge-base/studynote/05_database/04_transactions_concurrency/520_select/), Filter 등)을 하나의 코드로 병합 | 가상 [함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/) 제거 및 루프 최적화 |
| **Vectorized Processing** | [SIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/)(Single [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Multiple [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 활용 | CPU 연산 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)) 극대화 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- <strong>메모리 <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a></strong>: `spark.memory.offHeap.enabled=true` [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 통해 Tungsten의 Off-[heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/) 기능을 활성화하여 GC 이슈가 잦은 대규모 워크로드를 안정화할 수 있다.
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 구조 선택</strong>: RDD보다는 Tungsten의 혜택을 100% 받을 수 있는 DataFrame/Dataset [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 사용을 강력히 권고한다. RDD는 Java 객체 오버헤드를 그대로 가지기 때문이다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- Tungsten은 Spark를 단순한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 프레임워크를 넘어 고성능 분석 엔진으로 진화시켰다. 최신 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)의 Spark에서는 벡터화된 실행(Vectorized Execution) 범위가 더욱 넓어지고 있으며, 이는 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 가속(RAPIDS) 및 차세대 하드웨어와의 융합으로 이어지는 토대가 되고 있다.

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **부모 개념**: [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/)
- **자식 개념**: Off-[heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/) Memory, Whole-stage [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) Generation
- **연관 개념**: [Catalyst Optimizer](/knowledge-base/studynote/16_bigdata/03_spark/057_catalyst_optimizer/), GC([Garbage Collection](/knowledge-base/studynote/02_operating_system/06_memory_management/380_garbage_collection/)), [SIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/)

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">RDD</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">DataFrame</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Tungsten 엔진</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">코드 생성 (Code Generation)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Photon 엔진</div></div>
</div>
</div>



Spark의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 표현이 RDD에서 DataFrame으로 발전하고 Tungsten 최적화를 거쳐 하드웨어 가속 엔진으로 이어지는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
- 컴퓨터가 일을 할 때 메모장(Java 객체)을 예쁘게 꾸미느라 시간을 낭비하지 않고, 암호 같은 숫자(바이너리)로 바로바로 일하게 하는 거예요.
- 가방에 물건을 넣을 때 하나하나 포장하지 않고, 차곡차곡 빈틈없이 쌓아서 더 많이 넣고 빨리 꺼내는 기술과 비슷해요.
- 덕분에 아주 많은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 처리할 때도 컴퓨터가 지치지 않고 엄청 빠르게 일할 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 58 / 262

← **이전**: [Catalyst Optimizer](/knowledge-base/studynote/16_bigdata/03_spark/057_catalyst_optimizer/)
**다음**: [적응형 쿼리 실행 (Adaptive Query Execution, AQE)](/knowledge-base/studynote/16_bigdata/03_spark/059_adaptive_query_execution_aqe/) →

---
