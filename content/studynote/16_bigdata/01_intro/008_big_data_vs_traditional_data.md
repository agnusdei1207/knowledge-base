---
title: 8. 빅데이터 vs 전통적 데이터 — RDBMS 한계(수평 확장 불가, 고정 스키마)
date: '2024-05-20'
description: RDBMS의 수평 확장 한계와 고정 스키마의 제약을 극복하기 위한 빅데이터 아키텍처 패러다임 비교
tags:
- bigdata
---

# 빅데이터 vs 전통적 [[001_dikw_pyramid|데이터]] (Big [[001_dikw_pyramid|Data]] vs Traditional [[001_dikw_pyramid|Data]])

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 전통적 [[001_dikw_pyramid|데이터]] 환경(RDBMS)이 '[[442_consistency_integrity|무결성 보장]]을 위한 수직 확장([[621_scale_up_system_bus|Scale-Up]])'에 의존했다면, 빅데이터 환경은 '유연성과 [[452_availability|가용성]]을 위한 수평 확장([[202_scale_out_distributed_horizontal_expansion|Scale-Out]])'을 근간으로 한다.
> 2. **가치**: [[005_schema|스키마]]리스(Schemaless)와 [[136_variance|분산]] 처리 아키텍처를 도입하여 페타바이트급 [[004_unstructured_data|비정형 데이터]]의 처리 비용을 획기적으로 낮추었다.
> 3. **융합**: [[191_transaction_concept_states|트랜잭션]] 중심의 RDBMS를 대체하는 것이 아니라, 워크로드의 특성에 맞게 두 기술을 혼용하는 [[308_pgvector|폴리글랏 퍼시스턴스]]([[132_polyglot_persistence|Polyglot Persistence]]) 체계로 융합되고 있다.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

과거 수십 년간 기업의 [[001_dikw_pyramid|데이터]] 저장 표준이었던 RDBMS(Relational [[501_database|Database]] [[372_management|Management]] System)는 ACID([[193_atomicity_all_or_nothing|원자성]], [[194_consistency_database_integrity|일관성]], [[443_isolation_concurrency_control|고립성]], 지속성) [[191_transaction_concept_states|트랜잭션]]을 엄격히 보장하며 금융, [[081_erp_enterprise_resource_planning|ERP]] 등 핵심 시스템의 근간이 되었다. 그러나 2010년대 이후 스마트폰과 IoT의 보급으로 [[001_dikw_pyramid|데이터]]의 형태가 텍스트, 이미지, [[568_logs_distributed_logging_elk_fluentd|로그]] 등 비정형으로 급변하고 그 양이 기하급수적으로 폭증했다.

이 시점에서 RDBMS는 두 가지 치명적인 한계에 직면했다. 첫째, 조인([[521_join|Join]]) 연산과 [[191_transaction_concept_states|트랜잭션]] [[003_integrity|무결성]]을 유지하기 위해 [[001_dikw_pyramid|데이터]]가 단일 서버(또는 소수의 강력한 서버)에 집중되어야 했으므로 확장에 물리적/비용적 한계(Scale-Up의 한계)가 뚜렷했다. 둘째, [[001_dikw_pyramid|데이터]]가 유입되기 전에 반드시 테이블 [[005_schema|스키마]]가 정의되어 있어야 하는 '[[010_schema_on_write|스키마 온 라이트]]([[010_schema_on_write|Schema-on-Write]])' 구조 탓에 다변하는 [[001_dikw_pyramid|데이터]] 포맷을 실시간으로 수용할 수 없었다. 이 두 가지 병목을 해결하기 위해 등장한 것이 바로 [[553_distributed_file_system|분산 파일 시스템]]([[013_hdfs|HDFS]])과 NoSQL로 대표되는 빅데이터 아키텍처다.

```text
이 도식은 데이터가 폭증하는 상황에서 전통적 데이터베이스가 겪는 물리적 한계(스케일업)와, 빅데이터 시스템의 스케일아웃 방식을 비교하여 보여준다.

[전통적 RDBMS: 스케일업(Scale-Up)의 한계]
[CPU/RAM ↑] ──(비용 기하급수적 증가)──> [Super Server] ──(물리적 임계점 도달)──> 시스템 마비
                                            ▲ 병목 지점: 특정 성능 이상 확장이 불가능함

[빅데이터 플랫폼: 스케일아웃(Scale-Out)의 유연성]
[Commodity PC 1] ┐
[Commodity PC 2] ┼──(선형적 비용 증가)──> [Distributed Cluster] ──(무한 확장 가능)
[Commodity PC N] ┘                          ▲ 이점: 저렴한 장비 추가만으로 성능 향상
```
이 비교의 핵심은 '비용과 [[282_performance_tactics|성능]]의 상관곡선'이다. 스케일업은 하이엔드 장비를 도입해야 하므로 [[282_performance_tactics|성능]]이 조금만 올라가도 비용이 수십 배 상승하는 반면, 빅데이터의 스케일아웃 구조는 저렴한 범용 x86 서버(Commodity Hardware)를 수백, 수천 대 연결하여 비용을 선형적으로 유지하면서도 무한한 확장을 가능하게 한다.

> 📢 **섹션 요약 비유**: RDBMS의 확장이 천재 요리사 한 명에게 점점 더 크고 비싼 주방 도구를 사주는 것(결국 한계에 부딪힘)이라면, 빅데이터의 확장은 평범한 요리사 수십 명을 고용해 역할을 분담시키는 것(무한한 생산성)과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

전통적 [[001_dikw_pyramid|데이터]] 시스템과 빅데이터 시스템의 구조적 차이는 [[001_dikw_pyramid|데이터]]를 저장하고 공유하는 저변의 아키텍처에서 비롯된다. RDBMS는 보통 'Shared-Disk' 아키텍처를 사용하여 여러 연산 노드가 하나의 스토리지를 공유하지만, 빅데이터는 'Shared-Nothing' 아키텍처를 채택한다.

| 구성 요소 | 전통적 RDBMS ([[188_pl_sql_t_sql_procedural|Oracle]] 등) | 빅데이터 / [[035_nosql|NoSQL]] ([[013_hdfs|HDFS]], [[541_cassandra|Cassandra]]) | 비유 (차이점) |
|:---|:---|:---|:---|
| **저장 아키텍처** | Shared-Disk (디스크 공유) | Shared-Nothing (완전 분리/로컬 저장) | 공용 창고 vs 각자의 개인 창고 |
| **[[136_variance|분산]] 방식** | 수직 확장 ([[621_scale_up_system_bus|Scale-Up]] 중심) | 수평 확장 ([[202_scale_out_distributed_horizontal_expansion|Scale-Out]] 중심) | 건물 층수 올리기 vs 옆 건물 짓기 |
| **[[005_schema|스키마]] 적용** | [[010_schema_on_write|Schema-on-Write]] (입력 시 [[005_schema|스키마]] 강제) | [[009_schema_on_read|Schema-on-Read]] (조회 시 구조 해석) | 규격 상자만 허용 vs 일단 넣고 꺼낼때 해석 |
| **[[001_dikw_pyramid|데이터]] [[003_integrity|무결성]]** | ACID (강력한 [[194_consistency_database_integrity|일관성]]) | BASE (최종적 [[194_consistency_database_integrity|일관성]], [[452_availability|가용성]] 우선) | 절대 오차 불허 vs 일단 받되 나중에 맞춤 |
| **[[083_relationship_in_er_model|관계]] 연산** | 복잡한 [[521_join|JOIN]] 최적화 | [[521_join|JOIN]] 배제, [[111_denormalization_performance_tradeoff|역정규화]](De-[[093_normalization|normalization]]) | 복잡한 거미줄 vs 독립된 서류뭉치 |

Shared-Nothing 아키텍처는 각 노드가 자신만의 CPU, 메모리, 디스크를 가지며 네트워크를 통해서만 [[001_dikw_pyramid|데이터]]를 주고받는다. 이 구조는 노드 간 상태 공유를 최소화하여 락([[510_lock|Lock]]) 경합을 없애고 선형적 확장을 가능하게 한다.

```text
이 도식은 RDBMS의 병목인 Shared-Disk 구조와 빅데이터의 확장성 근간인 Shared-Nothing 분산 구조의 메모리/디스크 레이아웃을 비교한다.

[전통적 DB: Shared-Disk Architecture]
[Node A (CPU/RAM)] ──┐                    ┌──> 락 경합(Lock Contention) 발생
[Node B (CPU/RAM)] ──┼──> [SAN Storage] ──┤ 
[Node C (CPU/RAM)] ──┘                    └──> 디스크 I/O 대역폭 병목

[빅데이터: Shared-Nothing Architecture]
[Node A (CPU/RAM + Local Disk)] ──(네트워크)──┐
[Node B (CPU/RAM + Local Disk)] ──(네트워크)──┼──> [Distributed Coordination (ZooKeeper)]
[Node C (CPU/RAM + Local Disk)] ──(네트워크)──┘
 ▲ 이점: 데이터가 위치한 노드에서 직접 연산 수행 (Data Locality), 락 경합 없음
```
이 도식의 핵심은 '[[019_data_locality|데이터 지역성]]([[019_data_locality|Data Locality]])'이다. 빅데이터 아키텍처에서는 연산을 위해 [[001_dikw_pyramid|데이터]]를 네트워크로 끌어오는 대신, [[001_dikw_pyramid|데이터]]가 저장된 노드(Local Disk)로 [[159_opcode|연산 코드]]를 보내어 실행한다. 따라서 디스크가 분리되어 있어도 네트워크 병목을 최소화할 수 있다. 반면 Shared-Disk 구조는 노드가 추가될수록 중앙 스토리지의 I/O 병목과 [[191_transaction_concept_states|트랜잭션]] [[275_lock_contention_monitoring|락 경합]]이 심화되어 확장성이 멈추게 된다.

> 📢 **섹션 요약 비유**: Shared-Disk가 수십 명의 직원이 하나의 캐비닛을 같이 쓰느라 서로 줄을 서서 기다리는 구조라면, Shared-Nothing은 각 직원에게 전용 서랍장을 지급하여 [[275_lock_contention_monitoring|락 경합]] 없이 동시에 일하게 만드는 구조입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

빅데이터 아키텍처가 항상 전통적 RDBMS보다 우월한 것은 아니다. [[136_variance|분산]] 환경의 필연적 한계인 [[341_process|CAP]] 정리([[194_consistency_database_integrity|Consistency]], [[452_availability|Availability]], [[514_partition_slice_volume|Partition]] Tolerance)에 따라, 빅데이터 시스템은 네트워크 분할(P)을 견디고 [[452_availability|가용성]](A)을 유지하기 위해 [[194_consistency_database_integrity|일관성]](C)을 어느 정도 희생(BASE 원칙)한다.

```text
이 매트릭스는 RDBMS와 빅데이터 시스템을 데이터의 무결성(일관성)과 확장성 측면에서 비교하여, 시스템 목적에 따른 데이터베이스 선택 기준을 제시한다.

┌────────────┬──────────────────────────┬─────────────────────────┬──────────────┐
│ 비교 항목  │ 전통적 데이터 (RDBMS)    │ 빅데이터 플랫폼 (NoSQL) │ 실무 판단    │
├────────────┼──────────────────────────┼─────────────────────────┼──────────────┤
│ 철학       │ ACID (무결성 최우선)     │ BASE (가용성 최우선)    │ 데이터의 종류│
│ 스키마     │ 고정 (DDL 변경 어려움)   │ 유연함 (Schema-less)    │ 기획 변경 빈도
│ 확장성     │ Scale-Up 위주 (수천 TPS) │ Scale-Out 위주 (수백만) │ 트래픽 규모  │
│ 트랜잭션   │ 복잡한 다중 테이블 트랜잭│ 단일 레코드 트랜잭션    │ 정산/결제 여부
│ 장애 대응  │ Active-Standby Failover  │ N-Way 복제 (Replication)│ 다운타임 허용도
└────────────┴──────────────────────────┴─────────────────────────┴──────────────┘
```
이 표의 핵심은 '[[194_consistency_database_integrity|일관성]]의 강도'와 '[[139_throughput|처리량]]'의 트레이드오프다. 은행의 계좌 이체처럼 단 1원의 오차도 허용되지 않는 시스템은 [[191_transaction_concept_states|트랜잭션]]이 [[015_지연_데이터_관점|지연]]되더라도 철저하게 락을 거는 RDBMS(ACID)가 필수적이다. 반면, SNS의 '좋아요' 수나 클릭스트림 [[568_logs_distributed_logging_elk_fluentd|로그]]처럼 몇 초 정도 업데이트가 늦거나 수치가 조금 틀려도 [[090_service_kubernetes_network_load_balancing|서비스]]에 지장이 없고 트래픽이 폭증하는 시스템은 빅데이터 아키텍처(BASE)를 선택해야 장애 없이 버틸 수 있다.

최근에는 두 세계의 장점을 결합하기 위한 시너지 시도들이 활발하다. [[002_database_definition|데이터베이스]] 엔진 수준에서 [[136_variance|분산]] 처리를 지원하면서도 ACID를 보장하는 [[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]](예: [[292_etl_process|CockroachDB]], [[293_elt_process|TiDB]])이 등장했으며, 클라우드 [[209_data_warehouse_schema_on_write|DW]] 진영([[541_cassandra|Snowflake]], [[263_storage_compute_separation_bigquery|BigQuery]])에서는 RDBMS의 SQL 편의성과 빅데이터의 스케일아웃을 완벽히 융합하여 제공하고 있다.

> 📢 **섹션 요약 비유**: RDBMS가 느리지만 한 치의 오차도 없는 꼼꼼한 은행 금고라면, 빅데이터 NoSQL은 장부가 조금 늦게 맞춰지더라도 물건을 쉴 새 없이 받아내는 거대한 물류 창고와 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

실무에서 [[104_da_as_is_analysis|데이터 아키텍처]]를 설계할 때는 RDBMS와 빅데이터 저장소를 양자택일하는 것이 아니라, 워크로드의 특성에 따라 최적의 저장소를 혼용하는 **[[308_pgvector|폴리글랏 퍼시스턴스]]([[132_polyglot_persistence|Polyglot Persistence]])** [[268_strategy_pattern|전략]]을 채택해야 한다. [[213_msa_microservices_architecture|마이크로서비스 아키텍처]]([[619_msa_traffic_hardware|MSA]])에서는 각 [[090_service_kubernetes_network_load_balancing|서비스]]가 자신의 [[064_relation_domain|도메인]]에 맞는 DB를 선택한다.

```text
이 의사결정 트리는 신규 서비스 구축 시 데이터의 성격(트랜잭션, 로그, 검색)에 따라 RDBMS와 빅데이터 저장소(NoSQL, 검색엔진)를 어떻게 분배할지 결정하는 아키텍처 플로우다.

[신규 서비스 데이터 스토어 설계 플로우]
           ↓
(복잡한 조인과 100% 무결성이 필요한가? 예: 주문, 결제, 회원)
   ├── Yes ──> RDBMS (MySQL, PostgreSQL) 할당
   │              └──> (단, 성능 분산을 위해 CQRS/Read Replica 적용)
   │
   └── No ───> (데이터의 형태가 비정형이며 쓰기량이 폭증하는가?)
                  ├── Yes ──> (실시간 로그/센서) ──> NoSQL (Cassandra, MongoDB)
                  └── No  ──> (텍스트 전문 검색) ──> Search Engine (Elasticsearch)
```
이 흐름의 핵심은 [[064_relation_domain|도메인]] 분리다. 트래픽 폭증이 예상되는 [[064_relation_domain|도메인]]에 무리하게 RDBMS를 끼워 맞추면 전체 시스템이 다운된다. 반대로 [[191_transaction_concept_states|트랜잭션]] 정합성이 중요한 결제 시스템을 [[541_cassandra|Cassandra]] 같은 NoSQL로 구현하면, 애플리케이션 레벨에서 [[191_transaction_concept_states|트랜잭션]]을 수동으로 관리하느라 코드가 비대해지고 정합성 버그가 쏟아진다.

**실무 [[128_water_scrum_fall_anti_pattern|안티패턴]] ([[161_anti_pattern|Anti-pattern]])**:
전통적 DW에 익숙한 설계자가 빅데이터 환경(HBase나 [[541_cassandra|Cassandra]])에 [[001_dikw_pyramid|데이터]]를 적재하면서, RDBMS 시절의 [[093_normalization|정규화]]([[093_normalization|Normalization]])된 테이블 구조를 그대로 가져와 설계하는 패턴이다. NoSQL은 조인 기능이 매우 취약하거나 아예 없으므로, [[093_normalization|정규화]]된 테이블을 조회하려면 수십 번의 네트워크 호출이 발생하여 [[282_performance_tactics|성능]]이 궤멸한다. 실무에서는 조회 패턴에 맞춰 [[001_dikw_pyramid|데이터]]를 중복 저장하더라도 합쳐서 저장하는 [[111_denormalization_performance_tradeoff|역정규화]](De-[[093_normalization|normalization]]) 설계가 필수적이다.

> 📢 **섹션 요약 비유**: [[308_pgvector|폴리글랏 퍼시스턴스]]는 집을 지을 때 뼈대는 단단한 철근(RDBMS)으로 세우고, 넓은 거실은 유연한 목재([[035_nosql|NoSQL]])로, 창문은 투명한 유리(검색엔진)로 각각 목적에 맞는 재료를 혼용하는 것과 같습니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

빅데이터 아키텍처의 도입은 기업이 '저장 공간 부족'이라는 물리적 제약에서 벗어나, [[087_process_state_transition|생성]]되는 모든 [[001_dikw_pyramid|데이터]]를 자산화할 수 있는 토대를 마련했다. 

| 지표 | 전통적 [[001_dikw_pyramid|데이터]] 환경 | 빅데이터 중심 환경 | 파급 효과 |
|:---|:---|:---|:---|
| **저장 단가 (TB당)** | 수만 달러 (상용 스토리지) | 수십 달러 ([[191_oss_license_compliance|오픈소스]]+범용 서버) | 전체 [[001_dikw_pyramid|데이터]] 무기한 보관 실현 |
| **[[005_schema|스키마]] 유연성** | 1주~1개월 ([[020_ddl|DDL]] 작업 대기) | 실시간 수용 ([[009_schema_on_read|Schema-on-Read]]) | [[004_agile_relation|애자일]] 개발 및 빠른 타임투마켓 |
| **[[452_availability|가용성]] 보장** | [[483_active_vs_passive_ftp|Active]]-Standby 한계 | N중 [[016_replication_factor|복제]] 기반 무중단 [[090_service_kubernetes_network_load_balancing|서비스]] | 시스템 장애 시에도 100% [[090_service_kubernetes_network_load_balancing|서비스]] |

미래의 [[002_database_definition|데이터베이스]] 아키텍처는 RDBMS와 빅데이터의 경계가 완전히 허물어지는 방향으로 진화하고 있다. [[191_transaction_concept_states|트랜잭션]] 처리([[327_hint_handoff|OLTP]])와 대용량 분석([[316_olap|OLAP]])을 단일 [[136_variance|분산]] 시스템에서 동시에 처리하는 **[[294_oltp_vs_olap|HTAP]] (Hybrid Transactional/Analytical Processing)** 기술이 대세로 떠오르고 있다. 

또한 [[208_data_lake_schema_on_read|데이터 레이크]]의 유연성과 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]](RDBMS)의 ACID [[191_transaction_concept_states|트랜잭션]] 및 [[282_performance_tactics|성능]]을 결합한 **[[146_lakehouse|레이크하우스]]([[146_lakehouse|Lakehouse]], 예: [[147_delta_lake|Delta Lake]])**가 표준으로 자리잡으면서, 우리는 다시 '하나의 통합된 고성능 [[001_dikw_pyramid|데이터]] 플랫폼'으로 회귀하는 나선형 발전을 목격하고 있다. 기술사는 시스템의 제약을 이유로 기술을 거부할 것이 아니라, RDBMS와 빅데이터 생태계가 제공하는 최적의 교집합을 찾아내어 아키텍처를 설계하는 안목을 가져야 한다.

> 📢 **섹션 요약 비유**: 전통적 RDBMS와 빅데이터 시스템은 오랫동안 서로 다른 길([[003_integrity|무결성]] vs 확장성)을 걸어왔으나, 이제는 두 기술의 장점만 결합한 차세대 하이브리드 자동차([[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]], [[146_lakehouse|Lakehouse]])로 진화하여 [[001_dikw_pyramid|데이터]] 고속도로를 달리고 있습니다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] |
|:---|:---|
| **3V ([[001_bigdata_3v_5v|Volume]]/Velocity/Variety)** | 빅데이터를 전통 [[001_dikw_pyramid|데이터]]와 구분하는 3대 특성으로, 이후 Veracity·Value를 포함한 5V로 확장 |
| **[[013_hdfs|HDFS]] ([[203_hadoop_hdfs_block_replication_fault_tolerance|Hadoop Distributed File System]])** | 수천 대의 범용 서버에 [[001_dikw_pyramid|데이터]]를 [[136_variance|분산]] 저장하여 [[454_spof|단일 장애점]]([[454_spof|SPOF]])을 제거하는 빅데이터 핵심 인프라 |
| **[[308_pgvector|폴리글랏 퍼시스턴스]] ([[132_polyglot_persistence|Polyglot Persistence]])** | RDBMS, [[035_nosql|NoSQL]], 검색엔진 등 [[064_relation_domain|도메인]] 특성에 맞는 이종 DB를 함께 사용하는 아키텍처 [[268_strategy_pattern|전략]] |
| **[[009_schema_on_read|Schema-on-Read]]** | [[001_dikw_pyramid|데이터]]를 저장할 때는 [[005_schema|스키마]]를 강제하지 않고 조회할 때 해석하는 빅데이터 레이크의 유연성 원칙 |
| **[[294_oltp_vs_olap|HTAP]] (Hybrid Transactional/Analytical Processing)** | OLTP와 OLAP을 단일 시스템에서 동시 처리하여 RDBMS와 빅데이터의 경계를 허무는 차세대 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
[전통적 RDBMS (관계형 DB) — ACID, 정형 데이터]
    │
    ▼
[빅데이터 (Big Data) — 3V: Volume/Velocity/Variety]
    │
    ▼
[NoSQL / 분산 파일 시스템 (HDFS)]
    │
    ▼
[폴리글랏 퍼시스턴스 (Polyglot Persistence)]
    │
    ▼
[HTAP / 레이크하우스 (Lakehouse) — 통합 플랫폼]
```

[[001_dikw_pyramid|데이터]] 저장 기술이 전통적 [[083_relationship_in_er_model|관계]]형 모델에서 빅데이터 생태계를 거쳐 [[294_oltp_vs_olap|HTAP]] 통합 플랫폼으로 수렴하는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

1. 전통적 DB는 정리가 아주 잘 된 서랍장이에요 — 물건을 넣을 때 규칙을 지켜야 하지만 찾을 때는 빠르죠.
2. 빅데이터는 창고처럼 뭐든 다 던져 넣을 수 있어요 — 사진, 동영상, [[389_mesh_topology|메시]]지까지! 대신 찾을 때 좀 더 복잡해요.
3. [[146_lakehouse|레이크하우스]]는 서랍장의 편리함과 창고의 넉넉함을 합친 꿈의 공간이에요 — 양쪽의 장점을 모두 가졌답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 8 / 262

← **이전**: [[007_big_data_ecosystem|7. 빅데이터 생태계 — 수집→저장→처리→분석→시각화→활용]]
**다음**: [[009_data_explosion_factors|9. 데이터 폭증 요인 — IoT/SNS/모바일/센서/영상 CCTV]] →

---
