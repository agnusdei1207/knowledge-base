+++
title = "개방 주소법 (Open Addressing)"
date = 2024-05-22

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++

## 핵심 인사이트 (3줄 요약)
- 개방 주소법은 [해시 충돌](/knowledge-base/studynote/05_database/04_transactions_concurrency/563_hash_collision_chaining_linear_probing/) 발생 시 [해시 테이블](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/067_hash_table/) 내부의 <strong>다른 빈 버킷(Empty Bucket)</strong>을 찾아 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저장하는 충돌 해결 기법이다.
- 포인터를 사용하는 [체인법](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/069_chaining/)과 달리 테이블 내부 공간만을 활용하므로 캐시 효율(Cache Locality)이 높고 오버헤드가 적다.
- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 삭제 시 가짜 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([Dummy](/knowledge-base/studynote/04_software_engineering/11_testing_validation/459_dummy_test_double/)/[Tombstone](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/300_schema_on_write_vs_read/)) 처리가 필요하며, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 밀집되는 클러스터링([Clustering](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)) 현상을 제어하는 것이 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 관건이다.

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
- **배경**: 해시 함수가 완벽하지 않아 동일한 인덱스에 여러 키가 할당되는 충돌이 발생할 때, 별도의 외부 메모리([Linked List](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/) 등)를 쓰지 않고 테이블 자체에서 해결하려는 시도에서 시작되었다.
- **정의**: 충돌 발생 시 정해진 규칙(Probing)에 따라 다음 빈 공간을 탐색하여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저장하는 방식이다.
- **특징**: 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 [해시 테이블](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/067_hash_table/) [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 내부에 직접 저장되므로 'Closed Hashing'이라고도 불린다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
```text
[ 개방 주소법 탐사 기법 / Open Addressing Probing ]

  Index  [0]  [1]  [2]  [3]  [4]  [5]
  Table +----+----+----+----+----+----+
        | K1 |    | K2 | K3 |    |    |
        +----+----+----+----+----+----+
          ^         |    |
          |         +----+ (Collision at [2]!)
          |         |
          +---------+ (Linear Probing: Find next empty [3]... occupied! -> [4] OK!)

1. 선형 탐사 (Linear Probing): h(k, i) = (h(k) + i) % m. 고정 폭만큼 이동.
2. 이차 탐사 (Quadratic Probing): h(k, i) = (h(k) + c1*i + c2*i^2) % m. 제곱수만큼 이동.
3. 이중 해싱 (Double Hashing): h(k, i) = (h1(k) + i * h2(k)) % m. 제2의 해시 함수 사용.
```
- **탐사(Probing)**: 충돌 시 다음 저장 위치를 결정하는 함수이다.
- <strong>클러스터링(<a href="/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/">Clustering</a>)</strong>: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)들이 특정 구역에 뭉쳐서 탐사 시간이 길어지는 현상이다. 일차 클러스터링(선형 탐사 시)과 이차 클러스터링(이차 탐사 시)이 있다.
- **삭제 처리(Deletion)**: 단순히 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 지우면 탐색 경로가 끊기므로 'Deleted' 마킹([Tombstone](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/300_schema_on_write_vs_read/))을 통해 경로를 유지해야 한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 구분 | 개방 주소법 (Open Addressing) | [체인법](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/069_chaining/) ([Chaining](/knowledge-base/studynote/12_it_management/03_ea_isp/103_chaining/)) |
| :--- | :--- | :--- |
| **저장 공간** | [해시 테이블](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/067_hash_table/) 내부 (Internal) | 외부 링크드 리스트 (External) |
| **메모리 효율** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 적을 때 유리, 포인터 오버헤드 없음 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 많아도 유연, 포인터 저장 공간 필요 |
| <strong>캐시 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> | **높음 (연속된 메모리)** | 낮음 (포인터 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 오버헤드) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 저하</strong> | 적재율 $\[alpha](/knowledge-base/studynote/14_data_engineering/02_math_mining/068_significance_level_alpha_p_value_hypothesis/)$가 1에 가까워지면 급격히 저하 | $\[alpha](/knowledge-base/studynote/14_data_engineering/02_math_mining/068_significance_level_alpha_p_value_hypothesis/)$가 1을 넘어도 비교적 완만함 |
| **최악 시간** | 테이블 전체 탐색 (O(M)) | 리스트 전체 탐색 (O(N)) |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- <strong>적재율 <a href="/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/">임계치</a></strong>: 개방 주소법은 적재율이 0.5~0.7 수준을 넘지 않도록 관리해야 한다. [임계치](/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)를 넘으면 클러스터링으로 인해 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 기하급수적으로 떨어진다.
- <strong>탐사 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> 선택</strong>: 선형 탐사는 구현이 쉽지만 클러스터링에 취약하므로, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 중요한 경우 이중 해싱을 통해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포를 균등하게 가져가는 것이 바람직하다.
- **결정적 시스템**: 메모리 할당이 제한적인 임베디드 시스템이나 실시간 시스템에서 외부 메모리 할당의 불확실성을 피하기 위해 개방 주소법을 선호하는 경우가 많다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 포인터 연산을 줄여 CPU 캐시 히트율을 높이고 메모리 파편화를 방지할 수 있다.
- **결론**: 개방 주소법은 공간의 제약과 속도의 조화를 꾀하는 기법이다. 기술사는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 양과 삭제 빈도를 고려하여 [체인법](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/069_chaining/)과의 Trade-off를 결정할 수 있는 안목을 갖춰야 한다.

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념**: [해시 충돌](/knowledge-base/studynote/05_database/04_transactions_concurrency/563_hash_collision_chaining_linear_probing/) 해결 기법([Collision](/knowledge-base/studynote/05_database/04_transactions_concurrency/563_hash_collision_chaining_linear_probing/) Resolution)
- **핵심 기술**: 선형 탐사, 이차 탐사, 이중 해싱, [Tombstone](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/300_schema_on_write_vs_read/)
- **연관 개념**: 캐시 지역성(Cache Locality), 적재율(Load Factor)


### 📈 관련 키워드 및 발전 흐름도

```text
[직접 주소 테이블 (Direct Address Table) — 키를 인덱스로 직접 사용, 공간 낭비]
    |
    v
[체인법 (Chaining) — 충돌 시 연결 리스트로 분리, 외부 메모리 할당]
    |
    v
[개방 주소법 — 선형 탐사 -> 이차 탐사 -> 이중 해싱, 테이블 내부 배치]
    |
    v
[로빈 후드 해싱 (Robin Hood Hashing) — 탐사 거리 편차를 균등화하는 개선판]
    |
    v
[쿠쿠 해싱 (Cuckoo Hashing) — 최악 O(1) 조회 보장, 두 테이블 교차 배치]
```
이 흐름은 [해시 충돌](/knowledge-base/studynote/05_database/04_transactions_concurrency/563_hash_collision_chaining_linear_probing/)을 외부 자료구조에 위임하는 [체인법](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/069_chaining/)의 포인터 오버헤드를 줄이기 위해 테이블 내부에서 탐사를 수행하는 개방 주소법이 등장하고, 클러스터링 문제를 해결하는 방향으로 점진적으로 정교화되는 [해시 충돌](/knowledge-base/studynote/05_database/04_transactions_concurrency/563_hash_collision_chaining_linear_probing/) 해결 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 발전을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
- [해시 테이블](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/067_hash_table/)은 <strong>'주차장'</strong>과 같아요.
- 내가 주차하려는 자리([Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/))에 이미 차가 있다면, <strong>그 옆의 빈자리</strong>를 찾아서 주차하는 방식이 개방 주소법이에요.
- 자리가 너무 꽉 차면 빈자리를 찾느라 주차장 전체를 뱅뱅 돌아야 할 수도 있으니 주의해야 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 68 / 175

<- **이전**: [15. 해시 테이블 (Hash Table) — 해시 함수, 충돌 처리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/067_hash_table/)
**다음**: [17. 체인법 (Chaining) — 연결 리스트 충돌 처리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/069_chaining/) ->

---
