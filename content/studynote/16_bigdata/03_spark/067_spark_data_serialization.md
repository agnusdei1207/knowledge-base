+++
title = "Spark 데이터 직렬화 (Data Serialization)"
date = 2026-03-04

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화는 메모리 내 객체를 네트워크 전송이나 디스크 저장에 적합한 바이너리 포맷으로 변환하는 과정으로, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 결정짓는 핵심 요소다.
- 스파크는 기본 Java Serialization의 느린 속도와 큰 용량 문제를 해결하기 위해 고성능 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)인 <strong>Kryo</strong>를 적극 권장한다.
- 효율적인 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화는 네트워크 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 절감뿐만 아니라 메모리 사용량 최적화([Tungsten Engine](/knowledge-base/studynote/16_bigdata/03_spark/058_tungsten_engine/) 연동)를 통해 전체 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 극대화한다.

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템인 스파크에서 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 노드 간 이동(셔플) 시 반드시 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화되어야 한다. [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 효율이 낮으면 전송 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 양이 늘어나 네트워크 병목이 생기고, 역직렬화 시 CPU 부하가 증가한다. 따라서 어떤 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 방식을 선택하느냐는 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 아키텍처의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 기반이 된다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
스파크는 두 가지 주요 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 방식을 지원하며, 내부적으로는 텅스텐 엔진을 통해 최적화한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Data Serialization Concept / 데이터 직렬화 개념</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Memory Object</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Binary Data / Byte Stream</div></div>
<div class="kb-diagram-note">(Java Objects) &lt;---(Deserialize)--- (Network/Disk)</div>
<div class="kb-diagram-note">1. Java Serialization: Default, flexible but slow and large footprint.</div>
<div class="kb-diagram-note">2. Kryo Serialization: Fast, compact, but requires manual registration.</div>
<div class="kb-diagram-note">3. Tungsten Engine: Uses off-heap memory and binary format directly to skip</div>
<div class="kb-diagram-note">heavy serialization/deserialization overhead.</div>
</div>
</div>



- **Java Serialization:** 모든 `Serializable` 객체를 처리할 수 있어 편리하지만, [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 정보가 많이 포함되어 결과물이 크고 느리다.
- **Kryo Serialization:** 자바 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화보다 10배 이상 빠르고 콤팩트하다. 스파크 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)(`spark.serializer`)에서 명시적으로 지정해야 하며, 사용자 정의 클래스는 등록([register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)) 과정을 거쳐야 최상의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 나온다.
- <strong><a href="/knowledge-base/studynote/16_bigdata/03_spark/058_tungsten_engine/">Tungsten Engine</a> (Internal):</strong> 스파크 내부 연산 시에는 객체를 자바 객체 형태로 유지하지 않고, 바이너리 행 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 직접 메모리에 배치하여 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 비용을 거의 제로에 가깝게 줄인다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | Java Serialization | Kryo Serialization |
| :--- | :--- | :--- |
| **속도** | 느림 | **매우 빠름** |
| **바이너리 크기** | 큼 (용량 낭비) | **작음 (효율적)** |
| **사용 편의성** | 높음 (디폴트) | 보통 (클래스 등록 권장) |
| **안정성** | 높음 (자바 표준) | 높음 (스파크 권장) |
| <strong>최적화 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong> | 기본 사용 | `spark.kryo.registrationRequired` [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)으로 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 극대화 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 튜닝 포인트:</strong> 대량의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 처리하는 셔플 작업이나 [RDD](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/310_audit/) [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)(`MEMORY_ONLY_SER`) 시 Kryo 사용은 필수적이다. 기술사로서 아키텍처 설계 시 네트워크 병목이 예상된다면 가장 먼저 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 방식과 버퍼 크기(`spark.kryo.capacity`)를 점검해야 한다.
- <strong><a href="/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/">직렬</a>화 대상 제한:</strong> 가능하면 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화가 필요 없는 기본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타입(Int, String 등)을 사용하고, 복잡한 사용자 정의 객체는 최소화하여 오버헤드를 줄이는 설계가 필요하다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅의 숨은 공신이다. 스파크가 텅스텐 엔진과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)프레임(DataFrame)으로 진화하면서 사용자가 직접 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화를 고민해야 하는 비중은 줄었으나, 로우 레벨 최적화가 필요한 임무에서는 여전히 Kryo 튜닝이 강력한 무기가 된다. 향후에는 Arrow와 같은 언어 불가지론적(Agnostic) 메모리 포맷이 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리의 표준 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 계층으로 자리 잡을 전망이다.

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념:** [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리, 네트워크 I/O
- **핵심 기술:** Kryo Serializer, Java Serializer, [Tungsten Engine](/knowledge-base/studynote/16_bigdata/03_spark/058_tungsten_engine/)
- **연관 기술:** Apache Arrow, Protobuf, Avro, Shuffle


### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Java 기본 직렬화 (Java Serialization) — 느리고 무거운 리플렉션 기반, Spark 기본값</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Kryo 직렬화 — 수동 등록 필요하나 Java 대비 10배 빠름, Spark 권장</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Apache Avro — 스키마 진화 지원, Kafka 메시지 직렬화 표준</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Apache Parquet — 컬럼 지향 파일 포맷, 스키마 내장·압축 최적화</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Apache Arrow — 인메모리 컬럼 포맷, 직렬화 없는 Zero-copy 공유, Spark 4.x+ 내부 표준</div></div>
</div>
</div>


이 흐름은 Spark 내부 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동의 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 오버헤드를 줄이기 위해 Java→Kryo→Avro/Parquet를 거쳐 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 자체를 없애는 [Zero-copy](/knowledge-base/studynote/02_operating_system/09_file_system/566_mmap_zero_copy_sendfile/) Arrow 포맷으로 수렴하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 기술의 발전을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
- 커다란 레고 성(메모리 객체)을 다른 집으로 보낼 때, 그대로 보낼 수 없으니 다 분해해서 상자(바이너리)에 담는 과정이에요.
- 상자에 담을 때 대충 담으면 상자가 너무 많아지는데(Java), 아주 꾹꾹 잘 눌러 담으면 상자 수를 줄일 수 있어요(Kryo).
- 상자가 적을수록 트럭(네트워크)에 한 번에 많이 실을 수 있어서 이사 속도가 빨라진답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 67 / 262

← **이전**: [Spark Shuffle 최적화 (Shuffle Optimization)](/knowledge-base/studynote/16_bigdata/03_spark/066_spark_shuffle_optimization/)
**다음**: [Spark Broadcast Join](/knowledge-base/studynote/16_bigdata/03_spark/068_spark_broadcast_join/) →

---
