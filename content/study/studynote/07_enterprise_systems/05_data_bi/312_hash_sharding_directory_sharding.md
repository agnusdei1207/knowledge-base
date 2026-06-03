---
title: 312. 해시 샤딩 및 디렉토리 샤딩 분산 DB 스케일 아웃 (Hash Sharding vs Directory Sharding)
date: '2026-04-21'
tags:
- studynote-enterprise-systems
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[280_sharding|샤딩]]([[243_sharding_horizontal_scaling_database|Sharding]])은 [[001_dikw_pyramid|데이터]]를 여러 DB 노드에 [[136_variance|분산]] 저장해 단일 노드 한계를 넘는 수평 확장([[202_scale_out_distributed_horizontal_expansion|Scale-Out]])을 실현하는 핵심 [[136_variance|분산]] DB 기법이다.
> 2. **가치**: [[244_consistent_hashing_ring_distribution|Consistent Hashing]] ([[194_consistency_database_integrity|일관성]] 해싱)은 노드 추가·제거 시 전체 키의 `1/N`만 재배치해 리샤딩 비용을 O(N)에서 O(1/N)으로 혁신적으로 줄인다.
> 3. **판단 포인트**: [[282_embedded_document_pattern|해시 샤딩]]은 균등 [[136_variance|분산]]에 강하지만 범위 [[298_qkv_attention|쿼리]]에 약하고, 범위 [[280_sharding|샤딩]]은 범위 [[298_qkv_attention|쿼리]]에 강하지만 핫스팟 위험이 있다.

## Ⅰ. 개요 및 필요성

단일 DB 서버는 CPU·메모리·디스크·네트워크 한계가 있어, 수TB 이상 [[001_dikw_pyramid|데이터]]와 초당 수십만 TPS를 처리할 수 없다.
[[280_sharding|샤딩]]([[243_sharding_horizontal_scaling_database|Sharding]])은 [[001_dikw_pyramid|데이터]]를 [[281_nosql_modeling_strategy|샤드 키]](Shard [[067_db_key_uniqueness_minimality|Key]]) 기준으로 여러 DB 노드(샤드)에 [[136_variance|분산]] 저장하는 수평 확장 기법이다.

주요 [[280_sharding|샤딩]] [[268_strategy_pattern|전략]]:
- **[[282_embedded_document_pattern|해시 샤딩]] ([[282_embedded_document_pattern|Hash Sharding]])**: hash([[067_db_key_uniqueness_minimality|key]]) % N 으로 샤드 결정
- **범위 [[280_sharding|샤딩]] (Range [[243_sharding_horizontal_scaling_database|Sharding]])**: 키 범위(예: A-M → 샤드1, N-Z → 샤드2)
- **디렉토리 [[280_sharding|샤딩]] ([[506_directory_structure_symbol_table|Directory]] [[243_sharding_horizontal_scaling_database|Sharding]])**: 별도 룩업 테이블로 샤드 매핑

[[244_consistent_hashing_ring_distribution|Consistent Hashing]] ([[194_consistency_database_integrity|일관성]] 해싱)은 [[282_embedded_document_pattern|해시 샤딩]]의 리샤딩 문제를 해결한다.
가상 링(Ring) 위에 노드와 키를 배치하여, 노드 추가·제거 시 전체의 `1/N` 키만 이동한다.

📢 **섹션 요약 비유**: [[280_sharding|샤딩]]은 우체국이 우편번호 앞자리로 편지를 각 지역 우체국에 분배하는 것이다. 각 지역 우체국이 샤드다.

## Ⅱ. 아키텍처 및 핵심 원리

### [[280_sharding|샤딩]] [[268_strategy_pattern|전략]] 비교

| [[268_strategy_pattern|전략]] | [[136_variance|분산]] 균등성 | 범위 [[298_qkv_attention|쿼리]] | 리샤딩 비용 | 핫스팟 |
|:---|:---|:---|:---|:---|
| [[282_embedded_document_pattern|Hash Sharding]] | 우수 (균일) | 불가 (전체 스캔) | 높음 (N개 키 이동) | 낮음 |
| [[244_consistent_hashing_ring_distribution|Consistent Hashing]] | 우수 | 불가 | 낮음 (1/N 키 이동) | 낮음 |
| Range [[243_sharding_horizontal_scaling_database|Sharding]] | 불균일 가능 | 우수 | 낮음 | 높음 (인기 범위) |
| [[506_directory_structure_symbol_table|Directory]] [[243_sharding_horizontal_scaling_database|Sharding]] | 설계에 따름 | 가능 | 유연 | 제어 가능 |

### [[244_consistent_hashing_ring_distribution|Consistent Hashing]] 가상 노드 (Virtual Node)

단순 [[194_consistency_database_integrity|일관성]] 해싱은 노드 수에 따라 불균등 [[136_variance|분산]] 가능 → 가상 노드(VNode)로 해결.
각 물리 노드를 100~150개 가상 노드로 링에 배치 → 균등 [[136_variance|분산]] 보장.

```
Cassandra: 기본 256 VNode/노드
DynamoDB: 내부 가상 노드 자동 관리
```

### [[103_ascii|ASCII]] 다이어그램: [[194_consistency_database_integrity|일관성]] 해시 링

```
  ┌─────────────────────────────────────────────────────┐
  │              Consistent Hash Ring                   │
  │                     0                               │
  │              ┌──────┴──────┐                        │
  │         315  │             │  45                    │
  │        (VB)  │             │  (VA)                  │
  │              │    Ring     │                        │
  │   270 (VC)   │  (0~360)   │  90 (VA)               │
  │              │             │                        │
  │        225   │             │  135                   │
  │        (VB)  └──────┬──────┘  (VC)                 │
  │                    180                              │
  │                                                     │
  │  Node A: VNode @ 45, 90, 180                        │
  │  Node B: VNode @ 135, 225, 315                      │
  │  Node C: VNode @ 270, (...)                         │
  │                                                     │
  │  Key "user123" → hash → 200 → 시계방향 첫 VNode →   │
  │  225(VB) → Node B에 저장                            │
  │                                                     │
  │  Node C 추가 시: hash(C) 위치 이전 키만 재배치 (1/N) │
  └─────────────────────────────────────────────────────┘
```

### [[506_directory_structure_symbol_table|Directory]] [[243_sharding_horizontal_scaling_database|Sharding]] 구조

| 키 범위 | 담당 샤드 | 비고 |
|:---|:---|:---|
| user_id 1~10M | Shard-1 | [[459_quic_fec_forward_error_correction|초기]] |
| user_id 10M~50M | Shard-2 | 성장 후 |
| user_id 50M+ | Shard-3 | 최신 |
| 특정 기업 고객 | Shard-VIP | 특수 처리 |

유연하지만 룩업 테이블 자체가 [[454_spof|SPOF]] (Single Point of Failure) 및 [[282_performance_tactics|성능]] 병목이 됨.

📢 **섹션 요약 비유**: Consistent Hashing은 원형 달력이다. 새 달이 추가되면 그 달 앞 며칠치 행사만 재배정하면 된다. 전체 달력을 다시 짜지 않아도 된다.

## Ⅲ. 비교 및 연결

### 실제 DB [[280_sharding|샤딩]] 구현 비교

| DB | [[280_sharding|샤딩]] 방식 | 특징 |
|:---|:---|:---|
| [[540_mongodb|MongoDB]] | Range+Hash (자동 밸런싱) | Chunk 자동 분할·이동 |
| [[541_cassandra|Cassandra]] | [[244_consistent_hashing_ring_distribution|Consistent Hashing]] (VNode) | 토큰 기반 자동 [[136_variance|분산]] |
| [[545_dynamodb|DynamoDB]] | [[244_consistent_hashing_ring_distribution|Consistent Hashing]] (내부) | 완전 관리형 |
| MySQL (Vitess) | Range+Hash (수동 설계) | 유튜브에서 개발 |
| [[542_redis|Redis]] Cluster | Hash Slot (16384) | 슬롯 기반 [[136_variance|분산]] |

📢 **섹션 요약 비유**: MongoDB의 Chunk 자동 이동은 창고 재고가 한 구역에 넘치면 직원이 자동으로 다른 구역으로 옮기는 스마트 창고다.

## Ⅳ. 실무 적용 및 기술사 판단

### [[280_sharding|샤딩]] 설계 [[435_checklist_based_testing|체크리스트]]

- [ ] [[281_nosql_modeling_strategy|샤드 키]] 선정: 고카디널리티 + 균등 [[136_variance|분산]] + 애플리케이션 [[298_qkv_attention|쿼리]] 패턴
- [ ] 핫스팟 방지: 타임스탬프를 [[281_nosql_modeling_strategy|샤드 키]]로 쓰면 최신 샤드 집중 → 피해야 함
- [ ] Cross-Shard Query 최소화: 샤드 간 JOIN은 네트워크 비용 높음
- [ ] VNode 수 결정: 150 VNode/노드([[541_cassandra|Cassandra]] 기본) → 균등 [[136_variance|분산]]
- [ ] 리밸런싱 [[268_strategy_pattern|전략]]: 피크 타임 외 자동 리밸런싱 [[208_schedule_history_transaction_execution_order|스케줄]]링

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

| [[128_water_scrum_fall_anti_pattern|안티패턴]] | 문제 | 해결 방법 |
|:---|:---|:---|
| 타임스탬프를 [[281_nosql_modeling_strategy|샤드 키]]로 | 최신 샤드에 모든 [[289_cqrs_db|쓰기]] 집중 | UUID or 복합 키 사용 |
| 샤드 수 너무 많음 | [[203_metadata_management|메타데이터 관리]] 복잡, 오버헤드 | 샤드당 100GB~1TB 목표 |
| Cross-Shard [[191_transaction_concept_states|Transaction]] | [[549_2pc_two_phase_commit_limitations_msa|2PC]] 오버헤드, [[452_availability|가용성]] 저하 | 애플리케이션 설계로 회피 |

📢 **섹션 요약 비유**: 타임스탬프 [[281_nosql_modeling_strategy|샤드 키]]는 모든 새 소포를 항상 가장 최근에 만든 우체국으로만 보내는 것이다. 그 우체국은 항상 바쁘고 나머지는 한가하다.

## Ⅴ. 기대효과 및 결론

### 기대효과

| 항목 | 단일 DB | [[280_sharding|샤딩]] 후 |
|:---|:---|:---|
| 최대 [[139_throughput|처리량]] | ~수천 TPS | 샤드 N × 수천 TPS |
| 스토리지 | 단일 서버 한계 | 이론상 무제한 수평 확장 |
| 장애 격리 | 전체 영향 | 1개 샤드 장애 = N분의 1 영향 |
| [[298_qkv_attention|쿼리]] 복잡도 | 단순 | Cross-Shard [[298_qkv_attention|쿼리]] 복잡 |

### 한계 및 선결 과제

- Cross-Shard [[521_join|Join]], Transaction은 매우 복잡 → 애플리케이션 설계로 최소화
- 샤드 재설계 필요 시 대규모 [[001_dikw_pyramid|데이터]] 마이그레이션 필요
- 운영 복잡도 급격 증가 → 완전 관리형 DB([[545_dynamodb|DynamoDB]], Cosmos DB) 검토
- ACID [[191_transaction_concept_states|트랜잭션]] 보장 어려움 → [[305_saga|Saga]] 패턴 등 보완 설계 필요

📢 **섹션 요약 비유**: [[280_sharding|샤딩]]은 회사 확장과 같다. 지사가 늘수록 [[139_throughput|처리량]]은 늘지만, 본사와 지사 간 협업(Cross-Shard)이 복잡해진다.

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| [[243_sharding_horizontal_scaling_database|Sharding]] | 기법 | [[001_dikw_pyramid|데이터]] 수평 [[136_variance|분산]] |
| [[244_consistent_hashing_ring_distribution|Consistent Hashing]] | [[001_algorithm_definition|알고리즘]] | 리샤딩 비용 최소화 |
| Virtual Node | 최적화 | 균등 [[136_variance|분산]] 보장 |
| Shard [[067_db_key_uniqueness_minimality|Key]] | 핵심 설계 | [[136_variance|분산]] 기준 키 |
| Hotspot | 문제 | 특정 샤드 쏠림 |
| [[506_directory_structure_symbol_table|Directory]] [[243_sharding_horizontal_scaling_database|Sharding]] | [[268_strategy_pattern|전략]] | 룩업 테이블 기반 유연 매핑 |

### 📈 관련 키워드 및 발전 흐름도

```
단일 DB 서버 한계 - 수평 분할(Sharding) 필요
    │
    ▼
Range Sharding - 핫스팟 문제 발생
    │
    ▼
Hash Sharding - 균등 분산, 범위 조회 불리
    │
    ▼
Directory Sharding - 룩업 테이블 기반 유연한 재분배
    │
    ▼
Consistent Hashing + Virtual Node - 확장성 극대화
```

> **키워드**: [[243_sharding_horizontal_scaling_database|Sharding]], [[282_embedded_document_pattern|Hash Sharding]], [[506_directory_structure_symbol_table|Directory]] [[243_sharding_horizontal_scaling_database|Sharding]], [[244_consistent_hashing_ring_distribution|Consistent Hashing]], Virtual Node, Horizontal Scaling, Hotspot

### 👶 어린이를 위한 3줄 비유 설명

1. [[280_sharding|샤딩]]은 반을 나눠 각 반에 선생님을 배정하는 것이에요. 학생이 늘면 반을 더 만들어요.
2. Consistent Hashing은 원형 좌석 배치예요. 새 학생이 오면 옆 친구 자리만 바꾸면 돼요.
3. [[506_directory_structure_symbol_table|Directory]] Sharding은 안내 데스크가 "3반 학생은 3번 교실로 가세요"라고 알려주는 방식이에요.
