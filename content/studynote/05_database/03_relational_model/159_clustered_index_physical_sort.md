---
title: "PK"
date: "2026-05-05"
tags:
  - "studynote-database"
---

## 핵심 인사이트

> 1. **본질**: 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) (Clustered [Index](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/))는 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 위치만 가리키는 구조가 아니라, <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">페이지</a> 자체를 <a href="/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a> 키 순서로 정렬해 저장하는 테이블의 물리적 뼈대</strong>다.
> 2. **가치**: 범위 검색과 정렬이 많은 질의에서는 관련 행이 같은 방향으로 모여 있어 랜덤 입출력 (Random I/O)을 줄이고, 연속 읽기 효율을 높인다.
> 3. **판단 포인트**: 물리적 정렬은 테이블당 한 기준만 가질 수 있으므로 보통 [기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/) (PK, Primary [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))에 걸리며, 키 선택을 잘못하면 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 분할 ([Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Split)과 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 병목이 커진다.

---

## Ⅰ. 개요 및 필요성

클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터베이스 관리 시스템](/studynote/05_database/01_db_architecture_relational/003_dbms_database_management_system/) (RDBMS, Relational [Database](/studynote/05_database/04_transactions_concurrency/501_database/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/) System)에서 행이 디스크나 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)에 배치되는 순서를 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 키 순서와 맞추는 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 구조다. 일반 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 "찾아가는 길"이라면, 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 아예 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 서 있는 줄" 자체를 다시 세운다. 그래서 `BETWEEN`, `ORDER BY`, 최근 범위 조회처럼 인접 값들을 묶어서 읽는 작업에 특히 강하다.

이 구조가 필요한 이유는 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목이 단순 계산보다 저장장치 접근 패턴에서 자주 발생하기 때문이다. 값은 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로 인접하지만 실제 행이 여기저기 흩어져 있으면, [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 많은 랜덤 접근을 해야 한다. 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 이 문제를 줄이기 위해 <strong>자주 읽는 순서대로 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 모아 두는 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>으로 등장했다.

즉 핵심은 "[인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 하나 더 만든다"가 아니라 "테이블의 기본 정렬 기준을 정한다"는 데 있다. 그래서 보통 테이블당 하나만 허용되고, 어떤 컬럼을 그 기준으로 잡을지가 설계 품질을 좌우한다.

- **📢 섹션 요약 비유**: 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 서랍 안 물건 위치를 적은 메모지가 아니라, 물건 자체를 색깔순으로 다시 정리한 수납장과 같다. 찾기는 빨라지지만 정리 기준은 하나만 고를 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)의 핵심은 B+트리 (B+Tree) 리프 노드가 별도 주소 목록이 아니라 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)라는 점이다. 상위 노드는 탐색 경로를 잡고, 리프 구간에는 키 순서대로 정렬된 행이 들어 있다. 따라서 한 번 리프에 도착하면 인접 범위를 옆 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)로 이어 읽기 쉽다.

아래 그림은 논클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)와 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)의 차이를 저장 관점에서 보여준다.

```text
+--------------------------------------------------------------------+
|      클러스터드 인덱스의 저장 구조와 범위 조회 흐름              |
+--------------------------------------------------------------------+
| [논클러스터드 인덱스]                                             |
| index leaf: 10->RID A, 11->RID Z, 12->RID C                          |
|                       |                                            |
|                       +- 실제 행은 흩어져 있어 추가 랜덤 접근      |
|                                                                    |
| [클러스터드 인덱스]                                                |
| root/branch ---> leaf(data page)                                    |
|                 +--------------------------------------+           |
|                 | 10 | 주문10 | ...                    |           |
|                 | 11 | 주문11 | ...                    |           |
|                 | 12 | 주문12 | ...                    |           |
|                 +--------------------------------------+           |
|                           |                                        |
|                           +- 다음 페이지도 13, 14, 15 순서로 연결   |
|                                                                    |
| 결과: 범위 조회 시 "찾고 다시 점프"보다 "찾고 이어 읽기"가 쉬움   |
+--------------------------------------------------------------------+
```

이 구조 덕분에 `WHERE id BETWEEN 1000 AND 1999` 같은 질의는 첫 위치만 찾은 뒤 연속 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 따라 읽을 수 있다. 반면 중간 키에 새 행이 자주 삽입되면 빈 공간이 부족한 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)에서 분할이 일어나고, 인접 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 재배치와 트리 재조정 비용이 발생한다. 그래서 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 읽기 효율을 얻는 대신 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 재배치 비용을 감수하는 구조다.

| 구성 요소 | 역할 | 설계상 의미 |
| :--- | :--- | :--- |
| 루트/브랜치 노드 | 탐색 경로 안내 | 원하는 키 범위까지 빠르게 도달 |
| 리프 노드 | 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 저장 | 리프가 곧 테이블 본문 |
| [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 연결 | 인접 리프 순차 이동 | 범위 스캔과 정렬 출력에 유리 |
| [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 분할 | 중간 삽입 시 재배치 | [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 부하와 [단편화](/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/) 원인 |

일부 엔진은 힙 테이블 위에 클러스터링 [힌트](/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)만 제공하고, 일부 엔진은 InnoDB처럼 기본적으로 [기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/)를 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)로 사용한다. 구현은 달라도 공통 철학은 같다. <strong>자주 읽는 순서대로 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 가까이 둔다</strong>는 것이다.

- **📢 섹션 요약 비유**: 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 주소록만 정리하는 것이 아니라, 아파트 입주민을 동·호수 순서대로 실제 건물에 다시 배치하는 일과 같다. 순서대로 방문하기는 편하지만 중간에 새 입주민이 끼면 이사 비용이 생긴다.

---

## Ⅲ. 비교 및 연결

클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 이해하려면 힙 테이블 ([Heap](/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/) Table), 논클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) (Non-Clustered [Index](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/))와의 차이를 함께 봐야 한다. 힙 테이블은 삽입은 단순하지만 행이 특정 순서로 모이지 않는다. 논클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 여러 개 만들 수 있지만, 리프가 보통 행 주소를 가리키므로 본문 접근이 한 번 더 필요하다. 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 그 대신 <strong>본문 자체를 정렬</strong>한다.

| 항목 | 힙 테이블 | 논클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) | 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) |
| :--- | :--- | :--- | :--- |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 순서 | 무정렬 | 원본 테이블과 별개 | [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 키 순서로 정렬 |
| 개수 | 테이블 1개 | 여러 개 가능 | 보통 테이블당 1개 |
| 범위 조회 | 불리 | 주소 추적 비용 존재 | 매우 유리 |
| 삽입 비용 | 낮음 | 보통 | 중간 삽입 시 높음 |
| 대표 용도 | 단순 적재 | 보조 검색 경로 | PK 기반 기본 저장 구조 |

이 차이는 다른 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과도 연결된다. 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 위에 보조 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 만들면, 보조 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 실제 행 주소 대신 클러스터드 키를 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하는 경우가 많다. 따라서 [기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/)가 너무 길면 모든 보조 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)도 함께 비대해질 수 있다. 그래서 실무에서는 "클러스터드 키는 짧고, 안정적이며, 증가형에 가깝게" 잡으려는 경향이 강하다.

즉 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 단독 기능이 아니라 전체 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 설계의 중심축이다. [기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/) 선택, 보조 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 크기, [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) [단편화](/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/), 조인 접근 경로까지 모두 이 기준의 영향을 받는다.

- **📢 섹션 요약 비유**: 힙은 창고에 물건을 들어오는 대로 쌓는 방식이고, 논클러스터드는 위치표를 여러 장 붙이는 방식이며, 클러스터드는 창고 선반 자체를 물건 번호순으로 짜는 방식이다. 편의와 유연성의 균형이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 주문번호, 시계열 증가 키, 계정 ID처럼 범위 검색과 정렬 기준으로 자주 쓰이는 컬럼에 적합하다. 특히 증가형 정수 키는 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 끝에 주로 삽입되므로 분할 부담이 상대적으로 작다. 반대로 무작위 UUID (Universally Unique [Identifier](/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/)) 같은 값은 중간 삽입을 자주 유발해 [단편화](/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)와 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 비용을 키울 수 있다.

또한 "클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 무조건 PK"라고 암기만 하면 부족하다. 비즈니스에서 가장 자주 읽는 경로가 무엇인지, 보조 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 얼마나 많은지, 키 길이가 시스템 전체에 주는 부담이 어떤지를 함께 봐야 한다. SQL Server의 Fill Factor, InnoDB의 [기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/) 설계, [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)과 재구성 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)도 이 맥락에서 판단해야 한다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 범위 조회와 정렬이 잦은 컬럼인가?
2. 키 값이 짧고, 안정적이며, 자주 변경되지 않는가?
3. 삽입 패턴이 증가형인가, 아니면 무작위인가?
4. 보조 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 수가 많아 클러스터드 키 길이의 파급 효과가 큰가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 의미 없는 긴 복합 키를 클러스터드 키로 잡아 모든 보조 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 비대하게 만드는 설계
- 무작위 키를 [기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/)로 택하고 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 분할 비용을 무시하는 설계
- 범위 조회는 거의 없는데도 관성적으로 클러스터드 구조만 고집하는 설계

- **📢 섹션 요약 비유**: 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 선택은 출입구 옆에 인기 상품을 둘지, 창고 번호순으로 둘지 정하는 매장 배치와 같다. 손님 동선을 잘 읽으면 효율이 오르지만, 기준을 잘못 잡으면 정리 비용만 커진다.

---

## Ⅴ. 기대효과 및 결론

클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)의 기대효과는 분명하다. 범위 검색, 정렬 결과 반환, 인접 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스캔에서 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 지역성 (Locality)을 높여 읽기 효율을 끌어올린다. 특히 온라인 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 처리 ([OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/), Online [Transaction](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Processing)에서도 [기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/) 중심 조회가 반복될 때 체감 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이가 크다.

하지만 이 장점은 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 비용과 맞바꾼 결과다. 물리적 정렬은 테이블당 하나만 허용되고, 중간 삽입과 키 변경에는 구조 재배치가 따른다. 따라서 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 "가장 빠른 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)"가 아니라, <strong>테이블의 대표 접근 경로를 저장 구조 수준에서 고정하는 선택</strong>으로 이해해야 한다.

결론적으로 이 개념은 "PK라서 자동으로 좋은 것"이 아니라, 읽기 패턴·삽입 패턴·보조 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 구조를 함께 고려해 설계해야 하는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 배치 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다. 즉 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 기억할 때의 핵심 문장은 이것이다. <strong><a href="/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a> 하나를 더 다는 것이 아니라, 테이블 자체를 어떤 기준으로 줄 세울지 결정하는 일</strong>이다.

- **📢 섹션 요약 비유**: 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 책갈피를 꽂는 일이 아니라 책 본문을 다시 인쇄하는 일과 같다. 한 번 잘 잡으면 읽기 편하지만, 기준을 바꾸는 대가는 크다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [기본 키](/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/) (PK, Primary [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) | 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 기준으로 자주 선택되는 컬럼 |
| B+트리 (B+Tree) | 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)의 대표 구현 구조 |
| [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 분할 ([Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Split) | 중간 삽입 시 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하를 만드는 핵심 현상 |
| 논클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) | 클러스터드 키를 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하는 보조 검색 경로 |
| 지역성 (Locality) | 범위 조회 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 좋아지는 근본 이유 |

### 📈 관련 키워드 및 발전 흐름도

```text
Heap Table
    |
    v
보조 인덱스 도입
    |
    v
클러스터드 인덱스
    |   +- 범위 스캔 최적화
    |   +- 정렬 비용 절감
    |   +- 페이지 분할 · 단편화 관리 필요
    v
기본 키 설계 · 보조 인덱스 설계 · 저장 구조 최적화
```

이 흐름도는 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 설계가 단순 검색 속도 향상을 넘어, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 순서와 전체 테이블 구조 최적화로 확장되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 클러스터드 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 친구 이름표만 붙이는 게 아니라, 친구들을 이름순으로 줄 세워 앉히는 거예요.
2. 그래서 비슷한 이름 친구들을 한꺼번에 찾기는 쉬워져요.
3. 하지만 중간에 새 친구가 오면 자리를 다시 옮겨야 해서 정리 비용이 들어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 159 / 600

<- **이전**: [158. 비트맵 인덱스 (Bitmap Index) - 분포도(Cardinality)가 나쁜(성별 등) 컬럼에 적합, DML 성능 저하](/studynote/05_database/03_relational_model/158_bitmap_index_cardinality_dml/)
**다음**: [160. 넌클러스터드 인덱스 (Non-Clustered Index / 보조 인덱스) - 리프 노드가 실제 데이터 포인터 보유, 여러 개](/studynote/05_database/03_relational_model/160_non_clustered_index_secondary/) ->

---
