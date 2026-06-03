---
title: 7. 빅데이터 생태계 — 수집→저장→처리→분석→시각화→활용
date: '2024-05-20'
description: 수집, 저장, 처리, 분석, 시각화로 이어지는 빅데이터 파이프라인의 전체 아키텍처와 실무 적용 전략
tags:
- bigdata
---

# 빅데이터 생태계 (Big [[001_dikw_pyramid|Data]] Ecosystem)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[001_dikw_pyramid|데이터]]가 발생하여 가치를 창출하기까지의 전체 생명주기(수집→저장→처리→분석→[[003_bigdata_7v|시각화]])를 매끄럽게 연결하는 [[136_variance|분산]] 컴퓨팅 기술들의 집합이다.
> 2. **가치**: 단일 기술이 아닌 [[192_module_independence|모듈]]화된 계층형 구조를 통해, 각 단계의 확장성(Scalability)과 내결함성([[800_system_architecture_fault_tolerance_dual|Fault Tolerance]])을 보장하며 [[001_dikw_pyramid|데이터]] [[002_silo_hyeonhyung|사일로]]를 타파한다.
> 3. **융합**: 과거의 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[031_에코_반향|에코]]시스템을 넘어, 현재는 [[531_cloud_native_architecture|클라우드 네이티브]](Cloud-Native) 환경과 스트리밍([[179_kafka_flink_watermark_time_window|Kafka]], Flink) 기술이 융합된 실시간 [[178_modern_data_stack|모던 데이터 스택]]으로 진화하고 있다.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

빅데이터 생태계 (Big [[001_dikw_pyramid|Data]] Ecosystem)는 폭발적으로 증가하는 다양한 형식의 [[001_dikw_pyramid|데이터]]를 안정적으로 수용하고, 이를 비즈니스 인사이트로 전환하기 위해 결합된 [[191_oss_license_compliance|오픈소스]] 및 상용 플랫폼들의 유기적인 네트워크다. 과거에는 [[001_dikw_pyramid|데이터]]가 부서별로 분절되어 저장되는 [[001_dikw_pyramid|데이터]] [[002_silo_hyeonhyung|사일로]]([[001_dikw_pyramid|Data]] [[002_silo_hyeonhyung|Silo]]) 현상이 극심했으며, 전통적인 [[209_data_warehouse_schema_on_write|DW]]([[208_data_warehouse_schema_on_write_inmon|Data Warehouse]]) 시스템만으로는 [[004_unstructured_data|비정형 데이터]]의 수용과 실시간 처리에 한계가 명확했다.

이러한 문제를 해결하기 위해 [[001_dikw_pyramid|데이터]]를 발생지에서 끊임없이 끌어와 중앙 집중형 저장소에 담고, 이를 [[430_index_fast_full_scan|병렬]]로 처리한 뒤 사용자에게 전달하는 엔드투엔드([[401_transport_layer_role_end_to_end_multiplexing|End-to-End]]) [[645_data_pipeline_acceleration|데이터 파이프라인]]이 필수적이게 되었다. 이 [[123_pipe|파이프]]라인은 어떤 한 구간이라도 병목이 발생하면 전체 시스템의 [[015_지연_데이터_관점|지연]]으로 직결되기 때문에, 단계별로 철저하게 [[136_variance|분산]] 처리 아키텍처가 적용되어야 한다.

```text
이 도식은 부서별로 고립된 기존의 데이터 사일로 환경과, 수집부터 활용까지 단일한 파이프라인으로 연결된 빅데이터 생태계의 패러다임 변화를 비교하여 보여준다.

[과거: 데이터 사일로 (Data Silo)]
CRM System ──> (고립된 RDB) ──x──> (분석 불가)
Web Logs   ──> (고립된 File) ──x──> (통합 불가)
                           ▲ 병목 지점: 통합 부재로 인한 인사이트 손실

[현재: 통합 빅데이터 파이프라인 (Data Pipeline)]
CRM (DB) ──(CDC)───┐   ┌──> (배치/스트리밍 처리) ──> BI 시각화
Web Logs ──(Kafka)─┴─> Data Lake (저장)
                       (분리된 스토리지)         (확장 가능한 컴퓨팅)
```
이 흐름의 핵심은 이기종의 소스 시스템에서 발생하는 [[001_dikw_pyramid|데이터]]를 중앙의 '[[208_data_lake_schema_on_read|Data Lake]]'로 모으고, 이를 독립적인 처리 엔진을 통해 가공한다는 점이다. 과거에는 [[001_dikw_pyramid|데이터]]의 저장과 처리가 하나의 시스템(예: [[188_pl_sql_t_sql_procedural|Oracle]] Exadata)에 종속되었으나, 빅데이터 생태계는 저장과 연산을 분리([[391_storage_compute_separation|Storage-Compute Separation]])하여 각각 필요에 따라 [[202_scale_out_distributed_horizontal_expansion|스케일 아웃]]할 수 있도록 아키텍처를 혁신했다.

> 📢 **섹션 요약 비유**: 빅데이터 생태계는 마치 거대한 정수 처리장과 같습니다. 강물과 빗물(수집)을 모아 거대한 댐(저장)에 가두고, 정수 시설(처리)을 거쳐 깨끗한 물을 가정([[003_bigdata_7v|시각화]] 및 활용)에 끊임없이 공급하는 [[123_pipe|파이프]]라인 네트워크입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

빅데이터 생태계는 [[001_dikw_pyramid|데이터]]의 흐름에 따라 수집, 저장, 처리, 분석, [[003_bigdata_7v|시각화]]의 5단계 레이어로 구분된다. 각 레이어는 철저히 [[192_module_independence|모듈]]화되어 있어 벤더 락인([[254_cloud_vendor_lock_in_avoidance_portability_multi_cloud|Vendor Lock-in]]) 없이 최적의 도구를 선택할 수 있다.

| 단계 | 역할 | 주요 기술 [[057_stack|스택]] | 내부 동작 메커니즘 | 비유 |
|:---|:---|:---|:---|:---|
| **1. 수집 (Ingestion)** | [[001_dikw_pyramid|데이터]]의 유입 및 큐잉 | [[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]], Flume, Sqoop | 비동기 [[389_mesh_topology|메시]]지 [[454_buffering|버퍼링]] 및 [[179_table_partitioning_concept|파티셔닝]] 전송 | 택배 집하장 |
| **2. 저장 (Storage)** | 대규모 [[001_dikw_pyramid|데이터]]의 [[136_variance|분산]] 보관 | [[013_hdfs|HDFS]], Amazon S3, [[543_hbase|HBase]] | 블록 분할 및 3중 [[016_replication_factor|복제]] ([[016_replication_factor|Replication]]) 기반 [[296_fault_tolerance_architecture|결함 허용]] | 초대형 물류 창고 |
| **3. 처리 (Processing)** | [[266_data_cleansing|데이터 정제]] 및 변환 ([[215_etl_vs_elt_pipeline|ETL]]) | [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]], Flink, [[018_mapreduce|MapReduce]] | 인메모리 [[136_variance|분산]] 연산 및 [[401_bayesian_network_dag_causality|DAG]] 최적화 처리 | 컨베이어 벨트 가공 |
| **4. 분석 (Analysis)** | 질의 및 기계학습 모델링 | [[544_hive|Hive]], Presto, MLlib | [[136_variance|분산]] SQL [[298_qkv_attention|쿼리]] 엔진 및 [[430_index_fast_full_scan|병렬]] ML [[001_algorithm_definition|알고리즘]] 수행 | 품질 검수 및 통계 |
| **5. [[003_bigdata_7v|시각화]] (Visualization)** | 인사이트 제공 | [[164_tableau|Tableau]], Superset, [[169_kibana|Kibana]] | 대시보드 렌더링 및 인터랙티브 필터링 | 최종 쇼룸 전시 |

[[001_dikw_pyramid|데이터]]는 이 생태계를 거치며 원시 상태([[225_raw|Raw]])에서 가치 있는 상태(Gold)로 전이된다. 이 과정에서 아키텍처의 핵심은 중앙의 리소스 관리자와 각 노드 간의 코디네이션(Coordination)이다.

```text
이 도식은 데이터가 유입되어 최종 시각화되기까지의 각 계층별 오픈소스 생태계 아키텍처와, 이를 조율하는 분산 코디네이터의 역할을 보여준다.

┌─────────────────────────────────────────────────────────┐
│        [Management & Governance (Atlas, Ranger)]        │
├─────────┬──────────┬───────────┬────────────┬───────────┤
│ 1.수집  │ 2.저장   │ 3.처리    │ 4.분석     │ 5.시각화  │
│ Kafka   │ HDFS     │ Spark     │ Hive / DB  │ Tableau   │
│ Sqoop   │ AWS S3   │ Flink     │ Presto     │ Superset  │
│ Flume   │ HBase    │ MapReduce │ MLlib      │ Kibana    │
├─────────┴──────────┴───────────┴────────────┴───────────┤
│        [Resource Management (YARN, Kubernetes)]         │
├─────────────────────────────────────────────────────────┤
│        [Distributed Coordination (ZooKeeper)]           │
└─────────────────────────────────────────────────────────┘
```
이 구조도의 핵심은 [[001_dikw_pyramid|데이터]]가 좌에서 우로 흐르는 동안, 하단의 ZooKeeper와 [[020_yarn|YARN]](또는 [[205_kubernetes_container_orchestration|Kubernetes]])이 전체 클러스터의 [[012_metadata|메타데이터]]와 CPU/메모리 자원을 동적으로 할당하고 관리한다는 점이다. 개별 Worker 노드가 죽더라도 리소스 매니저가 즉시 다른 노드에 [[150_task|태스크]]를 재할당하여 중단 없는 [[123_pipe|파이프]]라인을 유지한다. 실무에서는 이러한 코디네이션 계층의 장애(예: [[798_distributed_lock_zookeeper_consensus|ZooKeeper]] [[257_ensemble_learning|앙상블]] 붕괴)가 전체 생태계의 마비로 이어지므로 해당 계층의 고가용성(HA) 구성이 가장 우선시된다.

처리(Processing) 계층에서의 가장 큰 혁신은 MapReduce의 디스크 기반 I/O 병목을 제거한 Apache Spark의 인메모리(In-Memory) [[310_audit|RDD]]([[025_spark_rdd_resilient_distributed_dataset|Resilient Distributed Dataset]]) 구조다. 연산 중간 결과를 메모리에 유지함으로써, 반복적인 분석 및 기계학습 작업에서 속도를 [[489_raid_10_hybrid|10]]~100배 향상시켰다.

> 📢 **섹션 요약 비유**: 빅데이터 생태계는 각자의 역할이 명확히 나뉜 '오케스트라'와 같습니다. 수집은 타악기, 저장은 현악기, 처리는 관악기처럼 제 역할을 수행하며, YARN과 ZooKeeper라는 지휘자가 전체의 화음을 맞추어 냅니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

빅데이터 생태계를 구성할 때 가장 중요한 의사결정은 [[001_dikw_pyramid|데이터]]의 '시간 가치(Time-to-Value)'에 따라 [[123_pipe|파이프]]라인 아키텍처를 어떻게 설계하느냐이다. 대표적인 두 아키텍처인 [[216_lambda_kappa_architecture_batch_realtime|람다]]([[216_lambda_kappa_architecture_batch_realtime|Lambda]])와 카파([[235_kappa|Kappa]]) 아키텍처는 각각의 트레이드오프를 가진다.

```text
이 도식은 배치 처리와 실시간 처리를 병행하는 람다 아키텍처와, 스트리밍 하나로 통합한 카파 아키텍처의 데이터 흐름 구조를 비교한다. 시스템의 복잡도와 실시간성 요구사항에 따라 아키텍처를 선택해야 한다.

[Lambda Architecture]
                  ┌──> (Batch Layer: Hadoop/Spark) ─────┐
(Data Source) ────┤                                     ├──> (Serving Layer) ──> BI
                  └──> (Speed Layer: Storm/Flink) ──────┘
                  ▲ 병목: 두 개의 다른 코드베이스를 유지보수해야 하는 복잡성 증가

[Kappa Architecture]
(Data Source) ──> (Kafka: 무한 버퍼 보관) ──> (Stream Layer: Flink/Spark Streaming) ──> BI
                  ▲ 이점: 단일 로직으로 과거 배치와 실시간 처리를 모두 수행
```
이 비교의 핵심은 '로직의 파편화' 방지다. [[095_lambda_architecture|람다 아키텍처]]는 대규모 과거 [[001_dikw_pyramid|데이터]](Batch)와 최근 실시간 [[001_dikw_pyramid|데이터]](Speed)를 결합하여 정확도를 높이지만, 개발자가 배치 코드와 스트리밍 코드를 각각 짜야 하는 운영 복잡성을 낳는다. 반면 [[096_kappa_architecture|카파 아키텍처]]는 "모든 [[001_dikw_pyramid|데이터]]는 스트림이다"라는 철학 하에, Kafka의 보관 주기를 무한대로 늘려 스트리밍 엔진 하나만으로 재처리와 실시간 처리를 통합한다. 실무에서는 시스템 운영 인력이 부족할 경우 [[096_kappa_architecture|카파 아키텍처]] 기반의 [[178_modern_data_stack|모던 데이터 스택]]을 우선적으로 고려해야 한다.

| 비교 항목 | [[216_lambda_kappa_architecture_batch_realtime|람다]]([[216_lambda_kappa_architecture_batch_realtime|Lambda]]) 아키텍처 | 카파([[235_kappa|Kappa]]) 아키텍처 | 기술사적 판단 기준 |
|:---|:---|:---|:---|
| **코어 엔진** | Spark(배치) + Flink(실시간) | Flink / [[179_kafka_flink_watermark_time_window|Kafka]] Streams | 단일 엔진 통합 여부 |
| **운영 복잡도** | 매우 높음 (코드 중복) | 낮음 (단일 [[007_codebase|코드베이스]]) | 유지보수 리소스 여력 |
| **재처리 비용** | HDFS에서 배치 재수행 (빠름) | Kafka에서 처음부터 Replay | 네트워크/디스크 I/O 비용 |
| **정합성** | 배치 레이어가 최종 정합성 보장 | 스트리밍 엔진의 Exactly-Once 의존 | [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]]의 중요도 |

> 📢 **섹션 요약 비유**: [[095_lambda_architecture|람다 아키텍처]]가 꼼꼼한 회계사(배치)와 빠른 속보 기자(스트리밍) 두 명을 고용하여 일을 더블 체크하는 것이라면, [[096_kappa_architecture|카파 아키텍처]]는 기억력이 완벽한 천재 기자 한 명(통합 스트리밍)에게 모든 것을 맡기는 것과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

실무에서 빅데이터 생태계를 구축할 때 직면하는 가장 큰 문제는 [[061_on_premise_legacy_infrastructure|온프레미스]]([[061_on_premise_legacy_infrastructure|On-Premise]]) [[191_oss_license_compliance|오픈소스]] 직접 구축([[183_iaas_infrastructure_as_a_service|IaaS]])과 클라우드 관리형 [[090_service_kubernetes_network_load_balancing|서비스]]([[184_paas_platform_as_a_service|PaaS]]/[[309_saas|SaaS]]) 간의 선택이다. [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 중심의 복잡한 [[191_oss_license_compliance|오픈소스]]를 직접 운영하는 것은 극심한 운영 오버헤드를 유발한다.

```text
이 의사결정 트리는 새로운 빅데이터 플랫폼 도입 시, 조직의 보안 규제와 운영 역량을 바탕으로 적절한 생태계 호스팅 방식을 결정하는 플로우를 보여준다.

[빅데이터 생태계 도입 플로우]
           ↓
(망분리 및 강력한 데이터 주권 규제가 있는가?)
   ├── Yes ──> 온프레미스 구축 (Hadoop 기반 CDP 등 도입) -> 인프라 운영팀 필수
   │
   └── No ───> (데이터 처리량이 간헐적이며 폭증하는가?)
                  ├── Yes ──> Serverless Cloud 생태계 (AWS Athena, BigQuery)
                  └── No  ──> Managed Cloud 생태계 (AWS EMR, Databricks)
```
이 흐름의 핵심은 [[016_tco|TCO]](Total Cost of Ownership)의 관점 변화다. 과거에는 [[459_quic_fec_forward_error_correction|초기]] 하드웨어 투자(CAPEX)가 중심이었으나, 현재는 사용한 만큼만 지불하는(OPEX) 클라우드 환경으로 완전히 넘어왔다. 인프라 운영 인력이 없는 상태에서 섣불리 [[191_oss_license_compliance|오픈소스]] [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[031_에코_반향|에코]]시스템을 직접 구축하면 [[282_performance_tactics|성능]] 튜닝 실패와 노드 장애 [[658_ir_recovery|복구]] [[015_지연_데이터_관점|지연]]으로 인해 [[123_pipe|파이프]]라인이 멈추는 대형 사고를 겪게 된다.

**도입 [[435_checklist_based_testing|체크리스트]] 및 [[128_water_scrum_fall_anti_pattern|안티패턴]]**:
1. **[[002_silo_hyeonhyung|사일로]]화된 도구 도입 ([[161_anti_pattern|Anti-pattern]])**: 각 부서가 편하다는 이유로 한쪽은 Spark, 한쪽은 다른 [[215_etl_vs_elt_pipeline|ETL]] 툴을 무분별하게 도입하면 [[052_data_governance_framework|데이터 거버넌스]]가 붕괴된다. 반드시 단일화된 [[213_data_catalog_metadata|데이터 카탈로그]](예: Apache Atlas)로 [[012_metadata|메타데이터]]를 통제해야 한다.
2. **저장-컴퓨팅 강결합 유지**: 클라우드로 이관했음에도 불구하고 HDFS처럼 저장과 컴퓨팅 노드를 같이 [[249_scaling_normalization_standardization|스케일링]]하는 아키텍처를 유지하면 비용이 기하급수적으로 증가한다. S3/GCS에 [[001_dikw_pyramid|데이터]]를 두고 연산 노드만 On/Off 하도록 아키텍처를 재설계해야 한다.
3. **네트워크 [[189_egress|Egress]] 비용**: 클라우드 간 또는 리전 간 [[001_dikw_pyramid|데이터]]를 이동시킬 때 발생하는 전송 비용을 간과하여 "[[001_dikw_pyramid|데이터]] 이동 배보다 배꼽이 큰" 상황이 없는지 [[395_verification_process_review|검증]]해야 한다.

> 📢 **섹션 요약 비유**: 빅데이터 생태계 구축은 거대한 공장을 짓는 것과 같습니다. 무턱대고 직접 모든 부품([[191_oss_license_compliance|오픈소스]])을 조립하려다 유지보수에 짓눌리기보다는, 예산과 인력에 맞춰 [[166_smart_factory|스마트 팩토리]] 임대(클라우드 매니지드)를 [[268_strategy_pattern|전략]]적으로 선택해야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

빅데이터 생태계의 완성은 기업의 의사결정 속도를 수 주일 단위에서 밀리초 단위의 실시간으로 단축시켰다.

| 기대효과 영역 | 도입 전 (Legacy [[209_data_warehouse_schema_on_write|DW]]) | 도입 후 (Big [[001_dikw_pyramid|Data]] Ecosystem) | 비즈니스 파급력 |
|:---|:---|:---|:---|
| **처리 한계** | [[002_structured_data|정형 데이터]] 수십 TB 한계 | 페타바이트급 [[004_unstructured_data|비정형 데이터]] 수용 | [[190_ai_llm_requirements_specification|AI]]/ML [[123_pipe|파이프]]라인 완벽 지원 |
| **운영 유연성** | 라이선스 비용 및 스케일업 한계 | [[191_oss_license_compliance|오픈소스]] 기반 무한 스케일아웃 | 스토리지 비용 70% 이상 절감 |
| **확장성** | 일체형 시스템 병목 | 처리, 저장, 수집 계층의 독립적 확장 | 피크 트래픽 시 탄력적 대응 |

미래의 빅데이터 생태계는 단일한 거대 [[208_data_lake_schema_on_read|데이터 레이크]]에 모든 것을 집중시키는 중앙집중형 방식에서 벗어나, [[064_relation_domain|도메인]]별로 [[001_dikw_pyramid|데이터]] 소유권과 책임을 [[136_variance|분산]]하는 **[[211_data_mesh_domain_ownership|데이터 메시]]([[320_data_mesh|Data Mesh]])** 패러다임으로 진화하고 있다. 각 [[064_relation_domain|도메인]] 팀이 자신의 [[001_dikw_pyramid|데이터]]를 '제품([[154_data_product|Data Product]])'으로서 표준화된 생태계 API를 통해 제공하고, 중앙은 거버넌스와 인프라만 제공하는 형태다.

또한 물리적인 [[001_dikw_pyramid|데이터]] 이동을 최소화하고 흩어진 시스템들을 [[012_metadata|메타데이터]] 기반으로 가상으로 연결하는 **[[212_data_fabric_virtualization|데이터 패브릭]]([[212_data_fabric_virtualization|Data Fabric]])** 기술이 차세대 표준 아키텍처로 부상하고 있다. 결국 빅데이터 생태계의 진화는 기술의 복잡성을 뒤로 감추고, 누구나 쉽게 [[001_dikw_pyramid|데이터]]를 융합하고 분석할 수 있는 진정한 [[010_data_democratization|데이터 민주화]]를 향해 나아가고 있다.

> 📢 **섹션 요약 비유**: 빅데이터 생태계는 과거의 무거운 중앙 통제식 기차망을 넘어, 이제는 각 출발지와 목적지를 스스로 찾아가는 자율주행 자동차 네트워크([[211_data_mesh_domain_ownership|데이터 메시]]/패브릭)로 영리하고 가볍게 진화하고 있습니다.
### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **수집 (Ingestion)** | [[179_kafka_flink_watermark_time_window|Kafka]], Flume, Sqoop 등으로 외부 [[001_dikw_pyramid|데이터]]를 끌어오는 관문 |
| **저장 (Storage)** | [[013_hdfs|HDFS]], S3, HBase로 대용량 [[001_dikw_pyramid|데이터]]를 [[136_variance|분산]] 보관하는 계층 |
| **처리 (Processing)** | Spark, Flink로 [[001_dikw_pyramid|데이터]]를 변환하고 정제하는 계산 계층 |
| **분석·[[003_bigdata_7v|시각화]] (Analysis & Visualization)** | [[544_hive|Hive]], Superset, Kibana로 의사결정을 돕는 활용 계층 |

### 📈 관련 키워드 및 발전 흐름도

```text
[관계형 데이터베이스 (RDBMS)]
    │
    ▼
[하둡 분산 파일 시스템 (HDFS, Hadoop Distributed File System)]
    │
    ▼
[빅데이터 생태계 (Big Data Ecosystem)]
    │
    ▼
[스파크 (Apache Spark)]
    │
    ▼
[데이터 레이크하우스 (Data Lakehouse)]
    │
    ▼
[데이터 메시 (Data Mesh)]
```

전통적인 RDBMS 한계를 극복하기 위해 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 기반 빅데이터 생태계가 형성되고 Spark·[[146_lakehouse|레이크하우스]]·[[211_data_mesh_domain_ownership|데이터 메시]]로 진화하는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

1. 빅데이터 생태계는 커다란 물류센터 같아요.
2. 한 곳에서 물건만 모으는 게 아니라, 저장하고, 가공하고, 진열까지 이어져요.
3. 각 공정이 잘 맞아야 물건([[001_dikw_pyramid|데이터]])을 빨리 찾고 쓸 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 7 / 262

← **이전**: [[006_semi_structured_data|6. 반정형 데이터 — JSON/XML/HTML/CSV — 스키마 부분 보유]]
**다음**: [[008_big_data_vs_traditional_data|8. 빅데이터 vs 전통적 데이터 — RDBMS 한계(수평 확장 불가, 고정 스키마)]] →

---
