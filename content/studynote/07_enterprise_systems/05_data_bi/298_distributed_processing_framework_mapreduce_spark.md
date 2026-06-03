---
title: 298. 빅데이터 분산 처리 프레임워크 (MapReduce vs Spark)
date: '2026-03-04'
tags:
- studynote-enterprise
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 수많은 서버(노드)에 [[001_dikw_pyramid|데이터]]를 나누어 저장하고 [[430_index_fast_full_scan|병렬]]로 처리하여, 단일 서버로는 불가능한 초거대 [[001_dikw_pyramid|데이터]]를 분석 가능하게 만드는 소프트웨어 환경이다.
> 2. **가치**: [[018_mapreduce|맵리듀스]]([[018_mapreduce|MapReduce]])는 디스크 기반의 안정적인 대량 처리를, 스파크(Spark)는 인메모리(In-Memory) 기반의 [[148_5g_embb_urllc_mmtc|초고속]] 반복 연산과 실시간 처리를 지원한다.
> 3. **판단 포인트**: 단순 배치 작업은 [[018_mapreduce|맵리듀스]]가 경제적일 수 있으나, 현대의 복잡한 [[241_machine_learning_basics|머신러닝]], 대화형 [[298_qkv_attention|쿼리]], 실시간 분석에는 스파크가 압도적인 표준으로 자리 잡았다.

---

## Ⅰ. 개요 및 필요성

[[001_dikw_pyramid|데이터]]가 테라바이트(TB)를 넘어 페타바이트(PB) 수준이 되면, 아무리 고성능인 단일 서버라도 [[001_dikw_pyramid|데이터]]를 읽고 처리하는 데 한계에 직면한다. 이를 해결하기 위해 수십~수백 대의 저렴한 범용 서버를 연결해 하나의 거대한 컴퓨터처럼 사용하는 **[[136_variance|분산]] 컴퓨팅**이 필수적이게 되었다.

구글의 논문에서 시작된 [[018_mapreduce|맵리듀스]]는 빅데이터 시대의 포문을 열었으며, 이후 [[282_performance_tactics|성능]] 한계를 극복하기 위해 등장한 [[206_spark_inmemory_rdd_lazy_evaluation_lineage|아파치 스파크]]([[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]])는 현대 [[001_dikw_pyramid|데이터]] 공학의 핵심 인프라가 되었다.

- **📢 섹션 요약 비유**: 혼자서 수만 장의 시험지를 채점(Single Server)하는 대신, 수백 명의 보조 교사에게 시험지를 나누어 주고 각자 채점하게 한 뒤 점수를 합치는(Distributed Framework) 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[136_variance|분산]] 처리 프레임워크는 [[001_dikw_pyramid|데이터]]를 나누는 **Map(분할)** 과정과 결과를 합치는 **Reduce(병합)** 과정을 핵심 메커니즘으로 사용한다.

```text
[입력 데이터] ──▶ [분할/Map] ──▶ [셔플/Shuffle] ──▶ [병합/Reduce] ──▶ [최종 결과]
     │               │               │                │
 (거대 파일)      (노드별 처리)     (데이터 재정렬)     (결과 요약)
```

### [[018_mapreduce|맵리듀스]] ([[018_mapreduce|MapReduce]]) 특징
- **디스크 기반**: 각 단계의 중간 결과를 디스크에 저장한다. 장애 [[658_ir_recovery|복구]]에는 유리하지만 I/O 오버헤드로 인해 속도가 느리다.
- **배치 지향**: 정해진 시간에 대량의 [[001_dikw_pyramid|데이터]]를 한 번에 처리하는 데 적합하다.

### 스파크 (Spark) 특징
- **인메모리 기반**: 중간 결과를 메모리에 유지한다. [[018_mapreduce|맵리듀스]]보다 최대 100배 빠르며, 반복적인 [[241_machine_learning_basics|머신러닝]] [[001_algorithm_definition|알고리즘]]에 매우 효율적이다.
- **다양한 [[192_module_independence|모듈]]**: SQL(분석), Streaming(실시간), MLlib([[241_machine_learning_basics|머신러닝]]), GraphX([[070_graph_datastructure|그래프]]) 등 통합 [[057_stack|스택]]을 제공한다.

- **📢 섹션 요약 비유**: [[018_mapreduce|맵리듀스]]는 요리 단계마다 설거지를 하고 재료를 정리하며 천천히 요리하는 것이라면, 스파크는 모든 재료를 싱크대 위에 펼쳐두고 빛의 속도로 요리하는 것과 같다.

---

## Ⅲ. 비교 및 연결

[[018_mapreduce|맵리듀스]]와 스파크는 세대 교체 [[083_relationship_in_er_model|관계]]에 가깝지만, 인프라의 안정성 측면에서 여전히 [[018_mapreduce|맵리듀스]]가 쓰이는 영역이 있다.

| 항목 | [[843_hadoop_rack_awareness_data_replication_topology|하둡]] [[018_mapreduce|맵리듀스]] ([[018_mapreduce|MapReduce]]) | [[206_spark_inmemory_rdd_lazy_evaluation_lineage|아파치 스파크]] (Spark) |
|:---|:---|:---|
| 처리 속도 | 느림 (디스크 I/O 병목) | 매우 빠름 (인메모리 연산) |
| 처리 방식 | 배치(Batch) 전용 | 배치 + 스트리밍 + 대화형 |
| 장애 [[658_ir_recovery|복구]] | 매우 강력 (디스크에 결과 보존) | 강력 ([[310_audit|RDD]] 계보를 통한 재계산) |
| 난이도 | 상대적으로 높음 (Java 위주) | 낮음 (Python, Scala, SQL 지원) |
| 주요 용도 | [[215_etl_vs_elt_pipeline|ETL]], 대규모 [[568_logs_distributed_logging_elk_fluentd|로그]] 보관 및 집계 | 실시간 분석, [[190_ai_llm_requirements_specification|AI]]/[[241_machine_learning_basics|머신러닝]], BI |

스파크는 [[843_hadoop_rack_awareness_data_replication_topology|하둡]]의 저장소([[013_hdfs|HDFS]])나 자원 관리자([[020_yarn|YARN]]) 위에서 동작할 수 있으므로, [[843_hadoop_rack_awareness_data_replication_topology|하둡]] 생태계를 대체하기보다는 보완하며 발전해왔다.

- **📢 섹션 요약 비유**: [[018_mapreduce|맵리듀스]]는 튼튼하고 느린 '화물 열차'이고, 스파크는 빠르고 유연한 'KTX' 혹은 '개인용 승용차'와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 **비용 대비 [[282_performance_tactics|성능]]**을 고려해야 한다. 스파크는 메모리를 많이 사용하므로 하드웨어 비용이 높다. 따라서 실시간성이 필요 없는 단순 대량 집계는 [[018_mapreduce|맵리듀스]]가 경제적일 수 있다.

### [[435_checklist_based_testing|체크리스트]]
1. 1분 이내의 실시간 응답이 필요한 분석인가? (Spark 선택)
2. [[241_machine_learning_basics|머신러닝]]처럼 같은 [[001_dikw_pyramid|데이터]]를 수십 번 반복해서 읽어야 하는가? (Spark 선택)
3. 메모리 자원이 부족하고, [[001_dikw_pyramid|데이터]] 유실 시 [[658_ir_recovery|복구]]가 매우 중요한 초대용량 작업인가? ([[018_mapreduce|MapReduce]] 고려)

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 작은 [[001_dikw_pyramid|데이터]]를 처리하면서 스파크 클러스터를 띄우는 것. [[136_variance|분산]] 처리의 오버헤드가 실제 연산 시간보다 길어져서 오히려 단일 서버보다 느려질 수 있다.

- **📢 섹션 요약 비유**: 옆집에 심부름 갈 때는 자전거(Single Server)가 빠르지, 굳이 비행기(Distributed Cluster)를 준비하느라 시간을 허비할 필요는 없다.

---

## Ⅴ. 기대효과 및 결론

[[136_variance|분산]] 처리 프레임워크는 기업의 **[[001_dikw_pyramid|데이터]] 한계**를 제거했다. [[001_dikw_pyramid|데이터]]가 아무리 많아져도 서버를 추가([[202_scale_out_distributed_horizontal_expansion|Scale-out]])하기만 하면 분석이 가능해졌기 때문이다. 현재는 스파크가 주류를 이루고 있지만, 향후 레이(Ray)나 더 최신 프레임워크들이 [[190_ai_llm_requirements_specification|AI]] 연산에 특화되어 등장하고 있다.

결론적으로, [[018_mapreduce|맵리듀스]]와 스파크의 원리를 이해하는 것은 빅데이터 엔지니어링의 기초이며, 이를 통해 [[001_dikw_pyramid|데이터]] 규모의 경제를 실현할 수 있다.

- **📢 섹션 요약 비유**: 개미 떼가 힘을 합쳐 커다란 먹이를 옮기는 것처럼, 작은 컴퓨터들이 힘을 합쳐 거대한 지식의 산을 옮기는 것이 [[136_variance|분산]] 처리의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[013_hdfs|HDFS]] | [[018_mapreduce|맵리듀스]]와 스파크가 [[001_dikw_pyramid|데이터]]를 읽고 쓰는 [[843_hadoop_rack_awareness_data_replication_topology|하둡]]의 [[553_distributed_file_system|분산 파일 시스템]] |
| [[310_audit|RDD]] ([[025_spark_rdd_resilient_distributed_dataset|Resilient Distributed Dataset]]) | 스파크의 핵심 [[001_dikw_pyramid|데이터]] 구조, 장애 시 다시 계산하는 [[369_logic_bomb|논리]]적 계보 |
| [[020_yarn|YARN]] / [[205_kubernetes_container_orchestration|Kubernetes]] | [[136_variance|분산]] 처리 프레임워크에 자원을 할당해주는 관리자 |

### 📈 관련 키워드 및 발전 흐름도

```
단일 서버 배치 처리 한계 (TB급 데이터)
    │
    ▼
Google MapReduce 논문 (2004) - 분산 처리 패러다임
    │
    ▼
Hadoop MapReduce 오픈소스 구현 (디스크 I/O 병목)
    │
    ▼
Apache Spark - 인메모리 DAG 실행 엔진 (100x 빠름)
    │
    ▼
Spark Structured Streaming + Delta Lake 통합
```

> **키워드**: [[018_mapreduce|MapReduce]], [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]], [[401_bayesian_network_dag_causality|DAG]], In-Memory Processing, [[013_hdfs|HDFS]], [[310_audit|RDD]], DataFrame, [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]]

### 👶 어린이를 위한 3줄 비유 설명
1. 엄청나게 많은 사탕을 혼자 세려면 하루 종일 걸려요.
2. 그래서 친구 10명에게 사탕을 나누어 주고 각자 몇 개인지 세게 했어요.
3. 친구들이 알려준 숫자를 다 더하니까 금방 사탕의 개수를 알 수 있게 되었답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 298 / 482

← **이전**: [[297_data_virtualization|297. 데이터 가상화 (Data Virtualization)]]
**다음**: [[299_spark_rdd_resilient_distributed_dataset|299. 스파크 RDD (Resilient Distributed Dataset)]] →

---
