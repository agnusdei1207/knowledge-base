+++
weight = 117
title = "117. 물리 데이터베이스 설계 (Physical DB Design) - 인덱스·파티셔닝·스토리지 최적화"
date = "2026-04-19"
[extra]
categories = "studynote-database"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 물리 설계는 [[369_logic_bomb|논리]] 설계의 [[061_relation_schema_instance|릴레이션]] 스키마를 **특정 DBMS의 물리적 저장 구조([[154_database_index_b_tree_search_optimization|인덱스]]·[[179_table_partitioning_concept|파티셔닝]]·테이블스페이스·[[111_denormalization_performance_tradeoff|역정규화]])**로 변환하여 **[[282_performance_tactics|성능]]을 최적화**하는 단계다.
> 2. **가치**: [[369_logic_bomb|논리]]적으로 완벽한 [[105_third_normal_form_3nf_transitive|3NF]] 스키마도 물리 설계 없이 구현하면 **Full Table Scan·[[510_lock|Lock]] 경합·I/O 병목**으로 [[282_performance_tactics|성능]]이 100배 이상 저하될 수 있다.
> 3. **판단 포인트**: [[154_database_index_b_tree_search_optimization|인덱스]] 설계([[064_b_tree|B-Tree]]/Hash/Covering)·[[179_table_partitioning_concept|파티셔닝]](Range/Hash/List)·[[111_denormalization_performance_tradeoff|역정규화]](테이블 병합/분할/중복 컬럼)의 **세 가지 핵심 최적화**와 그 트레이드오프를 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    물리 설계 핵심 활동                                 │
├───────────────────────────────────────────────────────┤
│  1. 인덱스 설계                                       │
│     WHERE·JOIN·ORDER BY 컬럼에 B-Tree 인덱스         │
│     고카디널리티 컬럼 우선                            │
│  2. 파티셔닝                                          │
│     대용량 테이블 → Range/Hash/List 분할              │
│     I/O 분산, Partition Pruning                       │
│  3. 역정규화                                          │
│     자주 JOIN하는 테이블 → 병합/중복 컬럼 추가        │
│     읽기 성능 ↑, 쓰기 복잡도 ↑                       │
│  4. 스토리지 배치                                     │
│     테이블스페이스·데이터 파일·RAID 레벨              │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[369_logic_bomb|논리]] 설계가 건물 평면도(방 배치)라면, 물리 설계는 콘크리트 두께·배관 위치·에어컨 위치를 정하는 시공 도면이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[154_database_index_b_tree_search_optimization|인덱스]] 유형

| [[154_database_index_b_tree_search_optimization|인덱스]] | 적합 | 비적합 |
|:---|:---|:---|
| **[[064_b_tree|B-Tree]]** | 범위 검색, 정렬 | 저카디널리티 |
| **Hash** | 등가 검색 (=) | 범위 검색 |
| **Bitmap** | 저카디널리티 (성별, Y/N) | [[327_hint_handoff|OLTP]] ([[083_dml|DML]] 빈번) |
| **Covering** | [[520_select|SELECT]] 컬럼 전부 포함 | 넓은 [[154_database_index_b_tree_search_optimization|인덱스]] |

### [[179_table_partitioning_concept|파티셔닝]] 유형

| 유형 | 기준 | 예 |
|:---|:---|:---|
| **Range** | 날짜·숫자 범위 | 주문(월별) |
| **Hash** | [[667_hash_function_integrity_one_way|해시 함수]] | 균등 분배 |
| **List** | 특정 값 목록 | 지역코드별 |

- **📢 섹션 요약 비유**: [[154_database_index_b_tree_search_optimization|인덱스]]는 교과서 맨 뒤 색인이고, [[179_table_partitioning_concept|파티셔닝]]은 도서관 서가를 주제별로 나누는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[154_database_index_b_tree_search_optimization|인덱스]] 없음 | [[064_b_tree|B-Tree]] [[154_database_index_b_tree_search_optimization|인덱스]] | 커버링 [[154_database_index_b_tree_search_optimization|인덱스]] |
|:---|:---|:---|:---|
| **검색** | Full Scan | **[[154_database_index_b_tree_search_optimization|Index]] Scan** | **[[154_database_index_b_tree_search_optimization|Index]] Only Scan** |
| **속도** | O(N) | O(log N) | **O(log N), I/O 최소** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[154_database_index_b_tree_search_optimization|인덱스]] 설계 가이드
1. **WHERE 절 빈출 컬럼**: 반드시 [[154_database_index_b_tree_search_optimization|인덱스]].
2. **복합 [[154_database_index_b_tree_search_optimization|인덱스]] 순서**: 카디널리티 높은 컬럼 선두.
3. **[[154_database_index_b_tree_search_optimization|인덱스]] 과다 주의**: INSERT [[282_performance_tactics|성능]] 저하 ([[154_database_index_b_tree_search_optimization|인덱스]] 유지 비용).

---

## Ⅴ. 기대효과 및 결론

| 지표 | 물리 설계 미적용 | 물리 설계 적용 | 개선 |
|:---|:---|:---|:---|
| 검색 속도 | Full Scan (초) | **[[154_database_index_b_tree_search_optimization|Index]] Scan (ms)** | 100×+ |
| 대용량 관리 | 단일 테이블 | **[[179_table_partitioning_concept|파티셔닝]]** | 관리·[[282_performance_tactics|성능]] 향상 |

물리 설계는 **[[369_logic_bomb|논리]]적 [[002_bigdata_5v|정확성]]([[093_normalization|정규화]]) 위에 [[282_performance_tactics|성능]] 최적화를 얹는 단계**이며, 클라우드 DB([[390_aurora_serverless_quorum_write|Aurora]], Spanner)에서는 자동 [[179_table_partitioning_concept|파티셔닝]]·[[154_database_index_b_tree_search_optimization|인덱스]] 추천이 제공되고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[064_b_tree|B-Tree]] [[154_database_index_b_tree_search_optimization|인덱스]]** | 가장 범용적인 [[154_database_index_b_tree_search_optimization|인덱스]] 구조 |
| **[[179_table_partitioning_concept|파티셔닝]]** | 대용량 테이블 I/O [[136_variance|분산]] |
| **[[111_denormalization_performance_tradeoff|역정규화]]** | 읽기 [[282_performance_tactics|성능]] 최적화 ([[093_normalization|정규화]] 일부 해제) |
| **테이블스페이스** | 물리 저장 공간 관리 |
| **Covering [[154_database_index_b_tree_search_optimization|Index]]** | [[520_select|SELECT]] 컬럼을 [[154_database_index_b_tree_search_optimization|인덱스]]에 포함, I/O 최소화 |

### 📈 관련 키워드 및 발전 흐름도

```text
[단일 테이블 + Full Scan (초기)]
    │
    ▼
[B-Tree 인덱스 (1970s) — O(log N) 검색]
    │
    ▼
[파티셔닝 (1990s) — 대용량 테이블 분할]
    │
    ▼
[Covering Index / Index Organized Table (2000s)]
    │
    ▼
[현재: AI 기반 인덱스 자동 추천 (AutoIndex)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[154_database_index_b_tree_search_optimization|인덱스]]는 교과서 맨 뒤 **색인**이에요. "광합성"을 찾으려면 색인에서 페이지를 찾아 바로 가요.
2. [[179_table_partitioning_concept|파티셔닝]]은 도서관 **서가를 주제별로 나누는** 거예요. 수학 책은 수학 서가에만 있으니 찾기 쉽죠.
3. [[111_denormalization_performance_tradeoff|역정규화]]는 자주 쓰는 정보를 **가까이에 복사해 놓는** 거예요. 빨리 찾지만 정리가 좀 지저분해져요!
