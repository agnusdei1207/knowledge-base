---
title: "117. Physical Database Design Indexing"
date: "2026-04-19"
tags:
  - "studynote-database"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 물리 설계는 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 설계의 [릴레이션](/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) 스키마를 <strong>특정 DBMS의 물리적 저장 구조(<a href="/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a>·<a href="/studynote/05_database/03_relational_model/179_table_partitioning_concept/">파티셔닝</a>·테이블스페이스·<a href="/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/">역정규화</a>)</strong>로 변환하여 <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>을 최적화</strong>하는 단계다.
> 2. **가치**: [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로 완벽한 [3NF](/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/) 스키마도 물리 설계 없이 구현하면 <strong>Full Table Scan·<a href="/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a> 경합·I/O 병목</strong>으로 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 100배 이상 저하될 수 있다.
> 3. **판단 포인트**: [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 설계([B-Tree](/studynote/08_algorithm_stats/04_datastructure/064_b_tree/)/Hash/Covering)·[파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/)(Range/Hash/List)·[역정규화](/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/)(테이블 병합/분할/중복 컬럼)의 <strong>세 가지 핵심 최적화</strong>와 그 트레이드오프를 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    물리 설계 핵심 활동                                 |
+-------------------------------------------------------+
|  1. 인덱스 설계                                       |
|     WHERE·JOIN·ORDER BY 컬럼에 B-Tree 인덱스         |
|     고카디널리티 컬럼 우선                            |
|  2. 파티셔닝                                          |
|     대용량 테이블 -> Range/Hash/List 분할              |
|     I/O 분산, Partition Pruning                       |
|  3. 역정규화                                          |
|     자주 JOIN하는 테이블 -> 병합/중복 컬럼 추가        |
|     읽기 성능 ^, 쓰기 복잡도 ^                       |
|  4. 스토리지 배치                                     |
|     테이블스페이스·데이터 파일·RAID 레벨              |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 설계가 건물 평면도(방 배치)라면, 물리 설계는 콘크리트 두께·배관 위치·에어컨 위치를 정하는 시공 도면이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 유형

| [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) | 적합 | 비적합 |
|:---|:---|:---|
| <strong><a href="/studynote/08_algorithm_stats/04_datastructure/064_b_tree/">B-Tree</a></strong> | 범위 검색, 정렬 | 저카디널리티 |
| **Hash** | 등가 검색 (=) | 범위 검색 |
| **Bitmap** | 저카디널리티 (성별, Y/N) | [OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) ([DML](/studynote/12_it_management/02_itsm_itil/867_dml/) 빈번) |
| **Covering** | [SELECT](/studynote/05_database/04_transactions_concurrency/520_select/) 컬럼 전부 포함 | 넓은 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) |

### [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/) 유형

| 유형 | 기준 | 예 |
|:---|:---|:---|
| **Range** | 날짜·숫자 범위 | 주문(월별) |
| **Hash** | [해시 함수](/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/) | 균등 분배 |
| **List** | 특정 값 목록 | 지역코드별 |

- **📢 섹션 요약 비유**: [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 교과서 맨 뒤 색인이고, [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/)은 도서관 서가를 주제별로 나누는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 없음 | [B-Tree](/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) | 커버링 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) |
|:---|:---|:---|:---|
| **검색** | Full Scan | <strong><a href="/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">Index</a> Scan</strong> | <strong><a href="/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">Index</a> Only Scan</strong> |
| **속도** | O(N) | O(log N) | **O(log N), I/O 최소** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 설계 가이드
1. **WHERE 절 빈출 컬럼**: 반드시 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/).
2. <strong>복합 <a href="/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a> 순서</strong>: 카디널리티 높은 컬럼 선두.
3. <strong><a href="/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a> 과다 주의</strong>: INSERT [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 ([인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 유지 비용).

---

## Ⅴ. 기대효과 및 결론

| 지표 | 물리 설계 미적용 | 물리 설계 적용 | 개선 |
|:---|:---|:---|:---|
| 검색 속도 | Full Scan (초) | <strong><a href="/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">Index</a> Scan (ms)</strong> | 100×+ |
| 대용량 관리 | 단일 테이블 | <strong><a href="/studynote/05_database/03_relational_model/179_table_partitioning_concept/">파티셔닝</a></strong> | 관리·[성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상 |

물리 설계는 <strong><a href="/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a>적 <a href="/studynote/16_bigdata/01_intro/002_bigdata_5v/">정확성</a>(<a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a>) 위에 <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 최적화를 얹는 단계</strong>이며, 클라우드 DB([Aurora](/studynote/05_database/06_dw_olap_trends/390_aurora_serverless_quorum_write/), Spanner)에서는 자동 [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/)·[인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 추천이 제공되고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/08_algorithm_stats/04_datastructure/064_b_tree/">B-Tree</a> <a href="/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a></strong> | 가장 범용적인 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 구조 |
| <strong><a href="/studynote/05_database/03_relational_model/179_table_partitioning_concept/">파티셔닝</a></strong> | 대용량 테이블 I/O [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) |
| <strong><a href="/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/">역정규화</a></strong> | 읽기 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 ([정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 일부 해제) |
| **테이블스페이스** | 물리 저장 공간 관리 |
| <strong>Covering <a href="/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">Index</a></strong> | [SELECT](/studynote/05_database/04_transactions_concurrency/520_select/) 컬럼을 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)에 포함, I/O 최소화 |

### 📈 관련 키워드 및 발전 흐름도

```text
[단일 테이블 + Full Scan (초기)]
    |
    v
[B-Tree 인덱스 (1970s) — O(log N) 검색]
    |
    v
[파티셔닝 (1990s) — 대용량 테이블 분할]
    |
    v
[Covering Index / Index Organized Table (2000s)]
    |
    v
[현재: AI 기반 인덱스 자동 추천 (AutoIndex)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 교과서 맨 뒤 <strong>색인</strong>이에요. "광합성"을 찾으려면 색인에서 페이지를 찾아 바로 가요.
2. [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/)은 도서관 **서가를 주제별로 나누는** 거예요. 수학 책은 수학 서가에만 있으니 찾기 쉽죠.
3. [역정규화](/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/)는 자주 쓰는 정보를 **가까이에 복사해 놓는** 거예요. 빨리 찾지만 정리가 좀 지저분해져요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 117 / 600

<- **이전**: [116. 매핑 규칙 (ERD->릴레이션 매핑) - 엔터티·관계·속성의 체계적 변환](/studynote/05_database/02_modeling_normalization/116_mapping_rule_erd_to_relation/)
**다음**: [118. 차원 모델링 (Dimensional Modeling) - 스타 스키마·스노우플레이크·팩트/디멘전](/studynote/05_database/02_modeling_normalization/118_dimensional_modeling_star_schema/) ->

---
