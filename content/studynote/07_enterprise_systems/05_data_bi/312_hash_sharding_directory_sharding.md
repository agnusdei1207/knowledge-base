+++
title = "312. 해시 샤딩 및 디렉토리 샤딩 분산 DB 스케일 아웃 (Hash Sharding vs Directory Sharding)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-enterprise-systems"]

[extra]
tags = ["studynote-enterprise-systems"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)([Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/))은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 여러 DB 노드에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장해 단일 노드 한계를 넘는 수평 확장([Scale-Out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))을 실현하는 핵심 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) DB 기법이다.
> 2. **가치**: [Consistent Hashing](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/244_consistent_hashing_ring_distribution/) ([일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 해싱)은 노드 추가·제거 시 전체 키의 `1/N`만 재배치해 리샤딩 비용을 O(N)에서 O(1/N)으로 혁신적으로 줄인다.
> 3. **판단 포인트**: [해시 샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/282_embedded_document_pattern/)은 균등 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)에 강하지만 범위 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)에 약하고, 범위 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)은 범위 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)에 강하지만 핫스팟 위험이 있다.

## Ⅰ. 개요 및 필요성

단일 DB 서버는 CPU·메모리·디스크·네트워크 한계가 있어, 수TB 이상 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 초당 수십만 TPS를 처리할 수 없다.
[샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)([Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/))은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [샤드 키](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/281_nosql_modeling_strategy/)(Shard [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) 기준으로 여러 DB 노드(샤드)에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장하는 수평 확장 기법이다.

주요 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/):
- <strong><a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/282_embedded_document_pattern/">해시 샤딩</a> (<a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/282_embedded_document_pattern/">Hash Sharding</a>)</strong>: hash([key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) % N 으로 샤드 결정
- <strong>범위 <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/">샤딩</a> (Range <a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/">Sharding</a>)</strong>: 키 범위(예: A-M → 샤드1, N-Z → 샤드2)
- <strong>디렉토리 <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/">샤딩</a> (<a href="/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/">Directory</a> <a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/">Sharding</a>)</strong>: 별도 룩업 테이블로 샤드 매핑

[Consistent Hashing](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/244_consistent_hashing_ring_distribution/) ([일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 해싱)은 [해시 샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/282_embedded_document_pattern/)의 리샤딩 문제를 해결한다.
가상 링(Ring) 위에 노드와 키를 배치하여, 노드 추가·제거 시 전체의 `1/N` 키만 이동한다.

📢 **섹션 요약 비유**: [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)은 우체국이 우편번호 앞자리로 편지를 각 지역 우체국에 분배하는 것이다. 각 지역 우체국이 샤드다.

## Ⅱ. 아키텍처 및 핵심 원리

### [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 비교

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 균등성 | 범위 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | 리샤딩 비용 | 핫스팟 |
|:---|:---|:---|:---|:---|
| [Hash Sharding](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/282_embedded_document_pattern/) | 우수 (균일) | 불가 (전체 스캔) | 높음 (N개 키 이동) | 낮음 |
| [Consistent Hashing](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/244_consistent_hashing_ring_distribution/) | 우수 | 불가 | 낮음 (1/N 키 이동) | 낮음 |
| Range [Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/) | 불균일 가능 | 우수 | 낮음 | 높음 (인기 범위) |
| [Directory](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) [Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/) | 설계에 따름 | 가능 | 유연 | 제어 가능 |

### [Consistent Hashing](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/244_consistent_hashing_ring_distribution/) 가상 노드 (Virtual Node)

단순 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 해싱은 노드 수에 따라 불균등 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 가능 → 가상 노드(VNode)로 해결.
각 물리 노드를 100~150개 가상 노드로 링에 배치 → 균등 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 보장.

```
Cassandra: 기본 256 VNode/노드
DynamoDB: 내부 가상 노드 자동 관리
```

### [ASCII](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램: [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 해시 링



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Consistent Hash Ring</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">0</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">315</div><div class="kb-diagram-cell">45</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(VB)</div><div class="kb-diagram-cell">(VA)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Ring</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">270 (VC)</div><div class="kb-diagram-cell">(0~360)</div><div class="kb-diagram-cell">90 (VA)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">225</div><div class="kb-diagram-cell">135</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(VB) (VC)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">180</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Node A: VNode @ 45, 90, 180</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Node B: VNode @ 135, 225, 315</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Node C: VNode @ 270, (...)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Key "user123" → hash → 200 → 시계방향 첫 VNode →</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">225(VB) → Node B에 저장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Node C 추가 시: hash(C) 위치 이전 키만 재배치 (1/N)</div></div>
</div>
</div>



### [Directory](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) [Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/) 구조

| 키 범위 | 담당 샤드 | 비고 |
|:---|:---|:---|
| user_id 1~10M | Shard-1 | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) |
| user_id 10M~50M | Shard-2 | 성장 후 |
| user_id 50M+ | Shard-3 | 최신 |
| 특정 기업 고객 | Shard-VIP | 특수 처리 |

유연하지만 룩업 테이블 자체가 [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) (Single Point of Failure) 및 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목이 됨.

📢 **섹션 요약 비유**: Consistent Hashing은 원형 달력이다. 새 달이 추가되면 그 달 앞 며칠치 행사만 재배정하면 된다. 전체 달력을 다시 짜지 않아도 된다.

## Ⅲ. 비교 및 연결

### 실제 DB [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) 구현 비교

| DB | [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) 방식 | 특징 |
|:---|:---|:---|
| [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) | Range+Hash (자동 밸런싱) | Chunk 자동 분할·이동 |
| [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) | [Consistent Hashing](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/244_consistent_hashing_ring_distribution/) (VNode) | 토큰 기반 자동 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) |
| [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) | [Consistent Hashing](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/244_consistent_hashing_ring_distribution/) (내부) | 완전 관리형 |
| MySQL (Vitess) | Range+Hash (수동 설계) | 유튜브에서 개발 |
| [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) Cluster | Hash Slot (16384) | 슬롯 기반 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) |

📢 **섹션 요약 비유**: MongoDB의 Chunk 자동 이동은 창고 재고가 한 구역에 넘치면 직원이 자동으로 다른 구역으로 옮기는 스마트 창고다.

## Ⅳ. 실무 적용 및 기술사 판단

### [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) 설계 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [ ] [샤드 키](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/281_nosql_modeling_strategy/) 선정: 고카디널리티 + 균등 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) + 애플리케이션 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 패턴
- [ ] 핫스팟 방지: 타임스탬프를 [샤드 키](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/281_nosql_modeling_strategy/)로 쓰면 최신 샤드 집중 → 피해야 함
- [ ] Cross-Shard Query 최소화: 샤드 간 JOIN은 네트워크 비용 높음
- [ ] VNode 수 결정: 150 VNode/노드([Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) 기본) → 균등 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)
- [ ] 리밸런싱 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/): 피크 타임 외 자동 리밸런싱 [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)링

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

| [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) | 문제 | 해결 방법 |
|:---|:---|:---|
| 타임스탬프를 [샤드 키](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/281_nosql_modeling_strategy/)로 | 최신 샤드에 모든 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 집중 | UUID or 복합 키 사용 |
| 샤드 수 너무 많음 | [메타데이터 관리](/knowledge-base/studynote/16_bigdata/10_governance/203_metadata_management/) 복잡, 오버헤드 | 샤드당 100GB~1TB 목표 |
| Cross-Shard [Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) | [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) 오버헤드, [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 저하 | 애플리케이션 설계로 회피 |

📢 **섹션 요약 비유**: 타임스탬프 [샤드 키](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/281_nosql_modeling_strategy/)는 모든 새 소포를 항상 가장 최근에 만든 우체국으로만 보내는 것이다. 그 우체국은 항상 바쁘고 나머지는 한가하다.

## Ⅴ. 기대효과 및 결론

### 기대효과

| 항목 | 단일 DB | [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) 후 |
|:---|:---|:---|
| 최대 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) | ~수천 TPS | 샤드 N × 수천 TPS |
| 스토리지 | 단일 서버 한계 | 이론상 무제한 수평 확장 |
| 장애 격리 | 전체 영향 | 1개 샤드 장애 = N분의 1 영향 |
| [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 복잡도 | 단순 | Cross-Shard [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 복잡 |

### 한계 및 선결 과제

- Cross-Shard [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/), Transaction은 매우 복잡 → 애플리케이션 설계로 최소화
- 샤드 재설계 필요 시 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마이그레이션 필요
- 운영 복잡도 급격 증가 → 완전 관리형 DB([DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/), Cosmos DB) 검토
- ACID [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 보장 어려움 → [Saga](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/) 패턴 등 보완 설계 필요

📢 **섹션 요약 비유**: [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)은 회사 확장과 같다. 지사가 늘수록 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)은 늘지만, 본사와 지사 간 협업(Cross-Shard)이 복잡해진다.

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/) | 기법 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수평 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) |
| [Consistent Hashing](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/244_consistent_hashing_ring_distribution/) | [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 리샤딩 비용 최소화 |
| Virtual Node | 최적화 | 균등 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 보장 |
| Shard [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | 핵심 설계 | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 기준 키 |
| Hotspot | 문제 | 특정 샤드 쏠림 |
| [Directory](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) [Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/) | [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 룩업 테이블 기반 유연 매핑 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">단일 DB 서버 한계 - 수평 분할(Sharding) 필요</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Range Sharding - 핫스팟 문제 발생</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Hash Sharding - 균등 분산, 범위 조회 불리</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Directory Sharding - 룩업 테이블 기반 유연한 재분배</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Consistent Hashing + Virtual Node - 확장성 극대화</div>
</div>
</div>



> **키워드**: [Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/), [Hash Sharding](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/282_embedded_document_pattern/), [Directory](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) [Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/), [Consistent Hashing](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/244_consistent_hashing_ring_distribution/), Virtual Node, Horizontal Scaling, Hotspot

### 👶 어린이를 위한 3줄 비유 설명

1. [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)은 반을 나눠 각 반에 선생님을 배정하는 것이에요. 학생이 늘면 반을 더 만들어요.
2. Consistent Hashing은 원형 좌석 배치예요. 새 학생이 오면 옆 친구 자리만 바꾸면 돼요.
3. [Directory](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) Sharding은 안내 데스크가 "3반 학생은 3번 교실로 가세요"라고 알려주는 방식이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 312 / 482

← **이전**: [311. 컬럼 지향 저장소 Parquet ORC 압축 효율 RLE 메커니즘 (Columnar Storage Compression)](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/311_parquet_orc_rle_compression/)
**다음**: [313. HTAP 하이브리드 트랜잭션 분석 처리 인메모리 아키텍처 (HTAP In-Memory Architecture)](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/313_htap_in_memory_architecture/) →

---
