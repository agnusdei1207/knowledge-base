+++
title = "Spark Broadcast Join"
date = 2026-03-04

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
- Broadcast Join은 조인 대상 중 작은 테이블을 모든 워커 노드의 메모리에 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)하여, 네트워크를 통한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재분배(Shuffle) 없이 로컬에서 즉시 조인을 수행하는 기법이다.
- 대량의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 간 조인 시 발생하는 셔플 오버헤드를 원천적으로 차단하므로, 스파크에서 가장 강력한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상 도구 중 하나로 꼽힌다.
- 기본적으로 스파크 [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)가 테이블 크기를 판단하여 자동 적용하지만, [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)(`broadcast()`)를 통해 명시적으로 유도할 수 있다.

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서 두 테이블을 조인하려면 보통 동일한 키를 가진 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 같은 노드로 모으는 '셔플 [해시 조인](/knowledge-base/studynote/05_database/03_relational_model/174_hash_join/)(Shuffle [Hash Join](/knowledge-base/studynote/05_database/03_relational_model/174_hash_join/))'이 발생한다. 하지만 하나는 수십억 건이고 다른 하나는 수천 건 정도라면, 작은 쪽을 모든 노드에 뿌려버리는 것이 전체 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 섞는 것보다 훨씬 효율적이다. 이것이 Broadcast Join의 핵심 아이디어다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
Broadcast Join은 <strong>작은 테이블의 수집(Collect)</strong>과 **전체 배포(Broadcast)** 과정을 거친다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Broadcast Join Architecture / 브로드캐스트 조인 아키텍처</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Driver</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Local Memory</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Executor 1</div><div class="kb-diagram-node">Executor 2</div><div class="kb-diagram-note">...</div></div>
<div class="kb-diagram-note">(Local Join) (Local Join)</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Big Data A</div><div class="kb-diagram-node">Big Data B</div></div>
<div class="kb-diagram-note">1. Collect: Driver fetches the small table from executors.</div>
<div class="kb-diagram-note">2. Broadcast: Driver pushes the small table to every executor using BitTorrent-like protocol.</div>
<div class="kb-diagram-note">3. Execution: Each executor performs a hash join locally with its portion of big data.</div>
<div class="kb-diagram-note">4. Advantage: No Shuffle for the big table.</div>
</div>
</div>



- <strong>임계값 <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a>:</strong> `spark.sql.autoBroadcastJoinThreshold` (기본값 10MB) 이하의 테이블은 자동으로 브로드캐스트 조인 대상이 된다.
- **작동 조건:** 한쪽 테이블이 드라이버와 각 익스큐터의 메모리에 충분히 들어갈 수 있을 만큼 작아야 한다. 너무 크면 `OutOfMemory(OOM)` 오류가 발생할 수 있다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | Shuffle [Hash Join](/knowledge-base/studynote/05_database/03_relational_model/174_hash_join/) | Broadcast [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) |
| :--- | :--- | :--- |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 이동</strong> | 두 테이블 모두 셔플 발생 | <strong>작은 테이블만 <a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/">복제</a>, 큰 테이블 이동 없음</strong> |
| **네트워크 부하** | 매우 높음 (N:N 이동) | 낮음 (1:N [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)) |
| **메모리 요구사항** | 중간 | 익스큐터마다 작은 테이블을 담을 메모리 필요 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> (대:소 조인)</strong> | 느림 | **매우 빠름** |
| **권장 상황** | 두 테이블 모두 대용량일 때 | 한쪽 테이블이 수십 MB 이내로 작을 때 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a> 주의:</strong> 브로드캐스트 조인은 드라이버 메모리를 거쳐 전송되므로 드라이버 메모리 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)(`spark.driver.memory`)이 충분해야 한다. 또한 익스큐터들이 동시에 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본을 유지하므로 익스큐터 메모리 부하도 고려해야 한다.
- **기술사적 통찰:** AQE(Adaptive Query Execution)를 활성화하면, 스파크가 런타임에 통계를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하여 셔플 조인을 브로드캐스트 조인으로 자동 전환(Demote to Broadcast)해준다. 이는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통계가 부정확한 상황에서도 안정적인 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 보장하는 핵심 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
Broadcast Join은 '[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 연산보다 이동 비용이 비싸다'는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅의 진리를 가장 잘 활용한 기술이다. 실무에서는 [차원 테이블](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/)([Dimension Table](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/))과 사실 테이블([Fact Table](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/)) 간의 조인에서 표준으로 사용된다. 향후에는 메모리 가격 하락과 네트워크 기술([RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) 등)의 발전에 따라 더 큰 규모의 테이블도 브로드캐스트 방식으로 처리될 가능성이 높다.

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념:** 조인 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) ([Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) Strategies), [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅 최적화
- **핵심 기술:** 브로드캐스트 변수 (Broadcast Variable), [해시 조인](/knowledge-base/studynote/05_database/03_relational_model/174_hash_join/)
- **연관 기술:** AQE, Shuffle [Hash Join](/knowledge-base/studynote/05_database/03_relational_model/174_hash_join/), [Sort Merge Join](/knowledge-base/studynote/05_database/03_relational_model/173_sort_merge_join/)

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">셔플 해시 조인 (Shuffle Hash Join) — 양쪽 테이블 전체 셔플, 네트워크 비용 O(N+M)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">소트 병합 조인 (Sort-Merge Join) — 정렬 후 병합, 대용량 대용량 조인 기본 전략</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">브로드캐스트 조인 (Broadcast Join) — 소규모 테이블 전 노드 복사, 셔플 제로</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">버킷 조인 (Bucket Join) — 사전 버킷팅으로 셔플 없이 로컬 조인, 반복 조인 최적화</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">AQE (Adaptive Query Execution) — 런타임 통계 기반 동적 조인 전략 전환</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">DPP (Dynamic Partition Pruning) — 브로드캐스트 필터로 대규모 테이블 파티션 제거</div></div>
</div>
</div>


이 흐름은 대용량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 조인의 네트워크 셔플 비용을 줄이기 위해 브로드캐스트 조인이 도입되고, 런타임 적응형 실행과 동적 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 제거로 진화하는 [Spark SQL](/knowledge-base/studynote/16_bigdata/03_spark/056_spark_sql/) 최적화 기법의 발전을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
- 커다란 도화지(큰 테이블)에 그림을 그리는데, 참고할 작은 사진(작은 테이블)이 한 장밖에 없어서 친구들이 서로 빌려 쓰려고 줄을 서는 상황이에요.
- 줄 서는 게 너무 힘들어서 선생님이 그 사진을 복사해서 모든 친구의 책상 위에 한 장씩 놓아주는 게 브로드캐스트 조인이에요.
- 이제 친구들은 자기 자리에서 사진을 보며 그림을 바로 그릴 수 있어서 훨씬 빨리 끝낼 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 68 / 262

← **이전**: [Spark 데이터 직렬화 (Data Serialization)](/knowledge-base/studynote/16_bigdata/03_spark/067_spark_data_serialization/)
**다음**: [18. Skew Join — 데이터 쏠림 조인 최적화](/knowledge-base/studynote/16_bigdata/03_spark/069_skew_join/) →

---
