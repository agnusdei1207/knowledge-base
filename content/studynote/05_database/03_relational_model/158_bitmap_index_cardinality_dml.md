+++
title = "158. 비트맵 인덱스 (Bitmap Index) - 분포도(Cardinality)가 나쁜(성별 등) 컬럼에 적합, DML 성능 저하 큼"
date = 2026-05-05

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트

> 1. **본질**: [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) (Bitmap [Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/))는 컬럼 값마다 행 존재 여부를 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)로 기록해, 저카디널리티 조건을 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 연산으로 합성하는 분석형 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)다.
> 2. **가치**: `성별='F' AND 지역='서울' AND 등급='VIP'`처럼 여러 조건을 동시에 거는 질의에서, [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 단위 `AND/OR` 계산으로 후보 행을 빠르게 줄여 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)에 특히 강하다.
> 3. **판단 포인트**: 읽기 위주 환경에서는 강력하지만, [DML](/knowledge-base/studynote/12_it_management/02_itsm_itil/867_dml/) ([Data Manipulation Language](/knowledge-base/studynote/05_database/01_db_architecture_relational/021_dml/))이 잦은 [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) (Online [Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Processing) 테이블에 쓰면 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 갱신 비용과 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 저하 때문에 오히려 병목이 된다.

---

## Ⅰ. 개요 및 필요성

[비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 카디널리티 (Cardinality, 서로 다른 값의 개수)가 낮은 컬럼을 효율적으로 검색하기 위한 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 구조다. 전통적인 [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 `주문번호`, `주민번호`처럼 값이 고르게 퍼진 컬럼에는 강하지만, `성별`, `상태코드`, `지역구분`처럼 같은 값이 대량 반복되는 컬럼에는 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)가 낮아 이점이 급격히 줄어든다.

문제는 분석 질의가 이런 "반복 값 많은 컬럼"을 여러 개 동시에 조건으로 건다는 점이다. [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)에서는 단건 조회보다 집계와 필터 조합이 많기 때문에, 값의 순서를 찾는 능력보다 "해당 행이 조건을 만족하는가"를 대량으로 판별하는 능력이 더 중요하다. [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 바로 이 지점을 공략해, 값별 포함 여부를 0과 1로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 저장하는 방식으로 등장했다.

즉 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)의 출발점은 "값이 적게 종류가 나뉘는 컬럼도 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)로 잘 활용할 수 없을까"라는 질문이다. 이 질문에 대해 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 정렬 트리 대신 <strong>행 단위 포함 지도</strong>를 만들자는 답을 내놓는다.

- **📢 섹션 요약 비유**: [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 명단을 이름순으로 찾는 전화번호부가 아니라, 교실 벽에 붙은 체크보드에 "여학생", "1반", "회장단" 스티커를 각각 붙여 두고 겹치는 칸만 바로 찾는 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)의 핵심은 값마다 하나의 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)열을 만든다는 점이다. 각 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 위치는 테이블의 한 행을 뜻하고, 해당 값이면 `1`, 아니면 `0`을 기록한다. 질의가 들어오면 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)는 필요한 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)열을 읽어 `AND`, `OR`, `NOT` 같은 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 연산을 수행한 뒤, 최종적으로 `1`이 남은 행 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/), 즉 ROWID (Row [Identifier](/knowledge-base/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/))만 실제 테이블에서 읽는다.

아래 그림은 세 개의 저카디널리티 조건을 결합하는 과정을 보여준다.

```text
+--------------------------------------------------------------------+
| Bitmap filtering flow                                             |
+--------------------------------------------------------------------+
| Row ID      1  2  3  4  5  6                                      |
| Gender=F    1  0  1  0  1  0                                      |
| City=SEOUL  1  1  0  0  1  0                                      |
| VIP=Y       0  1  1  0  1  0                                      |
| ----------------------------------------------------------------  |
| AND result   0  0  0  0  1  0  -> Row 5                           |
|                                                                    |
| Read path: bitmap scan -> bitwise AND/OR -> candidate ROWID read  |
+--------------------------------------------------------------------+
```

이 그림의 의미는 "조건별 후보를 따로 찾은 뒤 합치는 것"이 아니라, <strong>행 전체를 한 번에 <a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/">마스</a>킹한다</strong>는 데 있다. CPU (Central Processing Unit)는 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 연산에 매우 강하므로, [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)된 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 여러 장을 메모리에서 빠르게 결합할 수 있다. 특히 조건이 늘어날수록 B-Tree는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 병합 비용이 커질 수 있지만, [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵은 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)열 조합이 오히려 자연스럽다.

| 구성 요소 | 역할 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)상 의미 |
| :--- | :--- | :--- |
| 값별 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 | 각 값에 대한 행 포함 여부 기록 | 저카디널리티일수록 구조가 단순해짐 |
| [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 기법 | 긴 0 구간을 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 저장 | 저장 공간과 I/O 절감 |
| [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 연산 | `AND/OR/NOT`로 조건 결합 | 다중 조건 분석 질의에 강함 |
| 최종 ROWID 접근 | 남은 후보 행만 실제 읽기 | 불필요한 테이블 접근 감소 |

다만 이 구조는 갱신에 약하다. 행 하나가 바뀌면 해당 값의 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵뿐 아니라, 이전 값과 새 값에 연결된 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 위치를 함께 수정해야 한다. 그래서 대량 조회에는 유리하지만, 빈번한 삽입·수정·삭제가 있는 환경에서는 유지 비용과 잠금 비용이 크게 드러난다.

- **📢 섹션 요약 비유**: [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 사람을 한 명씩 불러 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 방식이 아니라, 운동장 전체 학생에게 색깔 카드들을 들게 하고 조건에 맞는 카드만 남을 때까지 겹쳐 보는 방식이다. 많이 찾을수록 더 빛난다.

---

## Ⅲ. 비교 및 연결

[비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 이해하려면 [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/), [해시 인덱스](/knowledge-base/studynote/05_database/03_relational_model/157_hash_index_equal_search/) ([Hash Index](/knowledge-base/studynote/05_database/03_relational_model/157_hash_index_equal_search/))와의 경계를 분명히 봐야 한다. B-Tree는 정렬과 범위 검색에 강하고, [해시 인덱스](/knowledge-base/studynote/05_database/03_relational_model/157_hash_index_equal_search/)는 동등 비교에 빠르다. 반면 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 <strong>낮은 카디널리티 + 다중 조건 결합</strong>이라는 특정 상황에서 가장 큰 장점을 낸다.

| 항목 | [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) | [해시 인덱스](/knowledge-base/studynote/05_database/03_relational_model/157_hash_index_equal_search/) | [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) |
| :--- | :--- | :--- | :--- |
| 강한 질의 유형 | 범위 검색, 정렬 | 동등 검색 | 다중 조건 분석 검색 |
| 유리한 카디널리티 | 높음 | 높음 | 낮음 |
| [DML](/knowledge-base/studynote/12_it_management/02_itsm_itil/867_dml/) 적합성 | 높음 | 보통 | 낮음 |
| 대표 환경 | [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) | 키 기반 조회 | [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) ([Online Analytical Processing](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/211_olap_drill_down_roll_up_surrogate_key/)) |

이 차이는 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)링에도 영향을 준다. [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/) ([Star Schema](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/296_star_schema/))의 [팩트 테이블](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/210_fact_dimension_table_snowflake_schema/)은 `성별`, `상품군`, `지역`, `캠페인`처럼 반복 값이 많은 차원 키를 자주 필터링하므로 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)와 궁합이 좋다. 반대로 주문 처리 시스템처럼 상태가 계속 바뀌는 테이블은 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 유지 비용이 커져, [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)의 이점이 상쇄된다.

즉 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 "B-Tree의 대체품"이 아니라 "워크로드가 다른 별도 도구"에 가깝다. 어떤 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 더 고급인가가 아니라, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포와 갱신 패턴이 무엇인가가 선택 기준이다.

- **📢 섹션 요약 비유**: B-Tree가 책장에서 한 권을 빨리 꺼내는 사서라면, [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 벽면 현황판에서 여러 조건 스티커를 겹쳐 대상 집단을 골라내는 조사관에 가깝다. 일의 종류가 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 배치 적재 후 장시간 조회하는 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/), 리포팅 시스템, 집계 마트에서 주로 고려한다. 특히 야간 적재 후 주간 조회가 많은 구조, [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/) 기반 분석, 다중 필터 집계 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)가 많은 환경이라면 좋은 선택이 된다.

반대로 실시간 주문, 계좌 이체, 게시판, [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 저장처럼 DML이 계속 발생하는 시스템에는 매우 신중해야 한다. [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 작은 수정도 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)열 여러 곳에 영향을 줄 수 있어 잠금 경합과 유지 비용이 커진다. 따라서 "조건 컬럼이 저카디널리티인가"만 보고 채택하면 안 되고, <strong>읽기/<a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 비율과 <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/">동시성</a> 요구</strong>를 함께 봐야 한다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 컬럼 카디널리티가 충분히 낮고 반복 값이 많은가?
2. 질의가 단건 조회보다 다중 조건 집계·분석 중심인가?
3. 테이블이 배치 적재 위주이고 실시간 [DML](/knowledge-base/studynote/12_it_management/02_itsm_itil/867_dml/) 비중이 낮은가?
4. [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)로는 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 한계 때문에 이점이 작았는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) 핵심 거래 테이블에 저카디널리티라는 이유만으로 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 거는 것
- 잦은 상태 변경 컬럼에 적용해 잠금 경합을 키우는 것
- [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)만 믿고 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/), 집계 설계, [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 생략하는 것

- **📢 섹션 요약 비유**: [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 조용한 도서관에서 자료를 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)할 때는 훌륭하지만, 사람들이 계속 들고 나가고 다시 꽂는 편의점 진열대에는 맞지 않는다. 정적 환경에서 강한 도구다.

---

## Ⅴ. 기대효과 및 결론

[비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)의 기대효과는 명확하다. 낮은 카디널리티 컬럼을 활용한 복합 필터 검색이 빨라지고, 다차원 분석 질의에서 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 결합 효율이 크게 높아진다. 특히 CPU 친화적인 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 연산과 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 저장 덕분에 대용량 분석 환경에서 높은 효율을 낼 수 있다.

하지만 이 장점은 읽기 중심이라는 전제 위에서만 성립한다. DML이 잦아지면 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 유지 비용, 잠금 범위, [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) 변동성이 동시에 문제로 떠오른다. 따라서 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 "저카디널리티면 무조건 정답"이 아니라, <strong>저카디널리티 + 분석형 워크로드 + 낮은 갱신 빈도</strong>가 함께 맞을 때 채택해야 하는 도구로 기억하는 것이 맞다.

최근 컬럼형 저장소와 벡터화 실행 엔진이 확산되면서 비슷한 아이디어를 다른 계층에서 구현하기도 하지만, [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 보여 준 핵심 원리는 여전히 유효하다. 분석 질의의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 결국 "값을 정렬해 찾는가"보다 "조건 집합을 얼마나 싸게 결합하는가"에 달려 있다는 점이다.

- **📢 섹션 요약 비유**: [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 만능 열쇠가 아니라, 문은 적고 사람은 많은 건물에서 출입 대상을 색깔 팔찌로 한 번에 통제하는 시스템에 가깝다. 조건 조합이 많을수록 진가가 난다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 카디널리티 (Cardinality) | [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 채택 여부를 가르는 핵심 기준 |
| [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) ([Selectivity](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)) | [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) 대비 효율 차이를 판단하는 지표 |
| [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) | 범위 검색과 OLTP에 더 적합한 대표 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) |
| [스타 스키마](/knowledge-base/studynote/05_database/06_dw_olap_trends/334_star_schema/) ([Star Schema](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/296_star_schema/)) | [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 자주 쓰이는 분석 모델 |
| [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) | 다중 조건 집계 질의가 많은 대표 적용 환경 |

### 📈 관련 키워드 및 발전 흐름도

```text
Full Scan
    |
    v
B-Tree Index
    |
    +- Equality focus -> Hash Index
    |
    +- Low-cardinality analytics -> Bitmap Index
                                |
                                v
Star Schema / Data Warehouse optimization
```

이 흐름도는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 선택이 "더 최신 구조"의 문제가 아니라, 질의 패턴과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포에 따라 갈라지는 설계 분기임을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 친구들 이름을 한 줄씩 읽는 대신, 조건마다 불이 켜지는 전구판을 만드는 거예요.
2. 그래서 "모자 쓰고, 안경 쓰고, 빨간 옷 입은 친구"를 전구 겹치기만으로 금방 찾을 수 있어요.
3. 하지만 친구들이 자꾸 자리를 바꾸면 전구판도 계속 고쳐야 해서, 자주 움직이는 곳에서는 힘들어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 158 / 600

<- **이전**: [157. 해시 인덱스 (Hash Index) - 동등(=) 검색에 빠름, 범위(Range) 검색 불가](/knowledge-base/studynote/05_database/03_relational_model/157_hash_index_equal_search/)
**다음**: [159. 클러스터드 인덱스 (Clustered Index) - 물리적 데이터 정렬 기준, 테이블당 1개 (보통 PK)](/knowledge-base/studynote/05_database/03_relational_model/159_clustered_index_physical_sort/) ->

---
