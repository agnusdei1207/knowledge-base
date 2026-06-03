+++
weight = 182
title = "182. 리스트 파티셔닝 (List Partitioning) - 명시적 특정 값(지역명 등) 기준"
date = "2026-05-06"
[extra]
categories = "studynote-database"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 리스트 [[179_table_partitioning_concept|파티셔닝]] (List [[179_table_partitioning_concept|Partitioning]])은 지역, 채널, 등급처럼 **의미가 분명한 이산 값**을 미리 정한 목록으로 매핑해, 업무 [[104_classification_analysis|분류]] 자체를 물리 저장 경계로 바꾸는 [[179_table_partitioning_concept|파티셔닝]] 기법이다.
> 2. **가치**: 동등 조건 조회에서 [[184_partition_pruning|파티션 프루닝]] ([[184_partition_pruning|Partition Pruning]])이 직관적으로 잘 작동하고, 지역별 삭제·[[555_backup_and_restore_strategy|백업]]·권한 통제를 [[514_partition_slice_volume|파티션]] 단위로 수행하기 쉬워 운영 설명력이 높다.
> 3. **판단 포인트**: 값 종류가 적고 안정적일수록 강하지만, 새 코드가 자주 추가되거나 특정 값으로 [[001_dikw_pyramid|데이터]]가 심하게 몰리면 DEFAULT [[514_partition_slice_volume|파티션]]과 재분산 [[268_strategy_pattern|전략]] 없이는 오히려 관리 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]가 커진다.

---

## Ⅰ. 개요 및 필요성

리스트 [[179_table_partitioning_concept|파티셔닝]]은 [[514_partition_slice_volume|파티션]] 키 ([[514_partition_slice_volume|Partition]] [[067_db_key_uniqueness_minimality|Key]]) 값이 사전에 정의된 특정 목록에 속하는지 [[396_validation|확인]]한 뒤, 해당 목록과 연결된 [[514_partition_slice_volume|파티션]]에 행을 저장하는 방식이다. [[180_range_partitioning|레인지 파티셔닝]] ([[180_range_partitioning|Range Partitioning]])이 값의 순서와 경계를 활용하고, [[181_hash_partitioning|해시 파티셔닝]] ([[181_hash_partitioning|Hash Partitioning]])이 균등 [[136_variance|분산]]을 우선한다면, 리스트 [[179_table_partitioning_concept|파티셔닝]]은 **업무 코드의 의미**를 그대로 물리 구조에 반영한다.

이 방식이 필요한 이유는 모든 [[001_dikw_pyramid|데이터]]가 시간 축이나 해시 분포로 설명되지 않기 때문이다. 예를 들어 `region_code`, `sales_channel`, `tenant_tier`, `country_code`처럼 값의 종류는 많지 않지만 구분 의미가 분명한 컬럼은, 어느 그룹이 어느 저장 영역에 있어야 하는지가 설계에서 중요하다. 이런 경우 리스트 [[179_table_partitioning_concept|파티셔닝]]을 쓰면 "서울 [[001_dikw_pyramid|데이터]]는 서울 [[514_partition_slice_volume|파티션]]", "제휴 채널 [[001_dikw_pyramid|데이터]]는 제휴 [[514_partition_slice_volume|파티션]]"처럼 업무 설명과 저장 구조가 일치해진다.

아래 그림은 리스트 [[179_table_partitioning_concept|파티셔닝]]이 **업무 [[104_classification_analysis|분류]] 축을 그대로 저장 경계로 고정**한다는 점을 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Business code becomes a physical boundary                          │
├────────────────────────────────────────────────────────────────────┤
│ region = SEOUL      -> P_CAPITAL                                   │
│ region = BUSAN      -> P_SOUTH                                     │
│ region = GANGWON    -> P_EAST                                      │
│ region = others     -> P_DEFAULT                                   │
│                                                                    │
│ effect: query, archive, access policy follow the same code axis    │
└────────────────────────────────────────────────────────────────────┘
```

핵심은 이 구조가 단순한 [[104_classification_analysis|분류]]표가 아니라는 점이다. [[514_partition_slice_volume|파티션]] 단위 [[555_backup_and_restore_strategy|백업]], [[514_partition_slice_volume|파티션]] 단위 삭제, 특정 [[514_partition_slice_volume|파티션]]만 대상으로 한 통계 수집과 [[154_database_index_b_tree_search_optimization|인덱스]] 관리가 가능해지므로, 리스트 [[179_table_partitioning_concept|파티셔닝]]은 [[282_performance_tactics|성능]]뿐 아니라 운영 거버넌스 수단이 되기도 한다.

- **📢 섹션 요약 비유**: 리스트 [[179_table_partitioning_concept|파티셔닝]]은 사물함을 날짜순으로 늘어놓는 것이 아니라, "서울", "부산", "기타"라고 이름표를 붙여 두는 방식과 같다. 물건이 어디에 들어갈지 한눈에 보이고, 특정 이름표 서랍만 열어보면 되니 찾기와 정리가 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[003_dbms_database_management_system|데이터베이스 관리 시스템]] ([[501_database|Database]] [[372_management|Management]] System, [[502_dbms|DBMS]])은 새 행이 들어오면 먼저 [[514_partition_slice_volume|파티션]] 키 값을 읽고, 그 값이 어느 `VALUES` 목록에 속하는지 [[396_validation|확인]]한다. 일치하는 목록이 있으면 그 [[514_partition_slice_volume|파티션]]으로 [[339_routing_overview_best_path_selection|라우팅]]하고, 없으면 `DEFAULT` [[514_partition_slice_volume|파티션]]으로 보내거나 오류를 발생시킨다. 즉 리스트 [[179_table_partitioning_concept|파티셔닝]]의 내부 원리는 복잡한 계산보다 **명시적 [[116_mapping_rule_erd_to_relation|매핑 규칙]]**에 가깝다.

```sql
CREATE TABLE sales_region (
    order_id     NUMBER,
    region_code  VARCHAR2(20),
    order_amount NUMBER
)
PARTITION BY LIST (region_code) (
    PARTITION p_capital VALUES ('SEOUL', 'GYEONGGI'),
    PARTITION p_south   VALUES ('BUSAN', 'GYEONGNAM'),
    PARTITION p_east    VALUES ('GANGWON'),
    PARTITION p_default VALUES (DEFAULT)
);
```

아래 그림은 입력 시점과 조회 시점에 리스트 [[179_table_partitioning_concept|파티셔닝]]이 어떻게 동작하는지 [[347_compaction|압축]]한 것이다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Insert routing in list partitioning                                │
├────────────────────────────────────────────────────────────────────┤
│ incoming row                                                       │
│    │                                                               │
│    ▼                                                               │
│ read partition key = region_code                                   │
│    │                                                               │
│    ├─ value in explicit list? ─ Yes ─▶ target partition            │
│    │                                                               │
│    └─ No ─▶ P_DEFAULT or insert error                              │
│                                                                    │
│ query region_code = 'BUSAN' -> prune all unrelated partitions      │
└────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| [[514_partition_slice_volume|파티션]] 키 ([[514_partition_slice_volume|Partition]] [[067_db_key_uniqueness_minimality|Key]]) | 행을 어떤 목록에 넣을지 판단하는 기준 컬럼 | 업무 의미가 뚜렷하고 값 종류가 비교적 안정적인 컬럼이 적합 |
| 명시적 값 목록 | 각 [[514_partition_slice_volume|파티션]]이 담당할 코드 집합 | 값 누락이 없도록 관리 체계를 가져야 함 |
| DEFAULT [[514_partition_slice_volume|파티션]] | 신규 코드나 예외 값의 안전판 | 없으면 예기치 않은 입력 실패가 발생할 수 있음 |
| [[184_partition_pruning|파티션 프루닝]] ([[184_partition_pruning|Partition Pruning]]) | 조건에 맞는 [[514_partition_slice_volume|파티션]]만 읽게 하는 최적화 | `=`·`IN` 조건에서 특히 효과적 |
| 로컬 [[154_database_index_b_tree_search_optimization|인덱스]] (Local [[154_database_index_b_tree_search_optimization|Index]]) | [[514_partition_slice_volume|파티션]]별 [[154_database_index_b_tree_search_optimization|인덱스]] 유지보수 단순화 | [[514_partition_slice_volume|파티션]] 교체·삭제 작업과 함께 관리하기 좋음 |
| 행 이동 (Row Movement) | [[514_partition_slice_volume|파티션]] 키 변경 시 다른 [[514_partition_slice_volume|파티션]]으로 재배치 | 상태값처럼 자주 바뀌는 컬럼은 비용이 커질 수 있음 |

리스트 [[179_table_partitioning_concept|파티셔닝]]은 사람이 이해하기 쉬운 대신, 값 집합을 사람이 책임지고 유지해야 한다. 따라서 신규 코드가 자주 생기는 조직이라면 `DEFAULT` [[514_partition_slice_volume|파티션]] [[229_monitor|모니터]]링과 코드 [[104_classification_analysis|분류]] 재배치 절차가 반드시 뒤따라야 한다.

- **📢 섹션 요약 비유**: 안내 데스크 직원이 방문 목적을 보고 "영업", "개발", "고객지원" 창구로 직접 보내는 것과 같다. 규칙이 명확하면 빠르지만, 새 부서가 생겼는데 표지판을 안 바꾸면 손님이 전부 임시 창구로 몰린다.

---

## Ⅲ. 비교 및 연결

리스트 [[179_table_partitioning_concept|파티셔닝]]의 장점은 다른 방식과 비교할 때 더 선명해진다. [[180_range_partitioning|레인지 파티셔닝]]은 기간 관리에, [[181_hash_partitioning|해시 파티셔닝]]은 균등 [[136_variance|분산]]에, 리스트 [[179_table_partitioning_concept|파티셔닝]]은 코드 의미 보존에 강하다. 따라서 "어떻게 고르게 나눌까"보다 "어떤 업무 경계를 저장 구조에 반영할까"가 중요한 경우 리스트가 우세하다.

| 방식 | 강한 지점 | 약한 지점 | 대표 활용 |
| :--- | :--- | :--- | :--- |
| [[180_range_partitioning|레인지 파티셔닝]] ([[180_range_partitioning|Range Partitioning]]) | 기간별 조회, 보관 주기, [[514_partition_slice_volume|파티션]] 단위 삭제 | 최신 구간 집중 현상 | 일자별 주문, 월별 [[568_logs_distributed_logging_elk_fluentd|로그]] |
| 리스트 [[179_table_partitioning_concept|파티셔닝]] (List [[179_table_partitioning_concept|Partitioning]]) | 지역·채널·조직 코드 분리, 규제 경계 반영 | 코드 추가 관리, 값 집중 시 쏠림 | 국가별, 채널별, 등급별 [[001_dikw_pyramid|데이터]] |
| [[181_hash_partitioning|해시 파티셔닝]] ([[181_hash_partitioning|Hash Partitioning]]) | 균등 [[136_variance|분산]], [[014_concurrency|동시성]] 높은 입력 | 업무 의미 약화, 범위 조회 약함 | 고객번호, 계정번호 |
| 복합 [[179_table_partitioning_concept|파티셔닝]] ([[183_composite_partitioning|Composite Partitioning]]) | 의미와 [[136_variance|분산]], 기간과 코드 분리를 동시에 확보 | 설계·운영 복잡도 증가 | 월별 + 지역별, 국가별 + 해시 |

특히 리스트 [[179_table_partitioning_concept|파티셔닝]]은 규제나 권한 모델과 잘 연결된다. 예를 들어 국가 코드별 [[001_dikw_pyramid|데이터]] 보관 위치가 달라야 하거나, 사업부별로 독립 [[555_backup_and_restore_strategy|백업]] [[164_policy|정책]]을 가져야 할 때는 리스트 [[514_partition_slice_volume|파티션]]이 설계 설명력에서 큰 이점을 준다. 반대로 `status`처럼 값은 적어 보여도 변경이 자주 일어나는 컬럼은 행 이동 비용이 커져 부적절할 수 있다.

또한 리스트 [[179_table_partitioning_concept|파티셔닝]] 하나로 모든 문제를 해결하려 해서는 안 된다. 월별 보관과 지역별 분리를 함께 원하면 `Range + List`, 특정 지역 안에서 [[001_dikw_pyramid|데이터]]가 과도하게 몰리면 `List + Hash`처럼 복합 구조로 확장하는 편이 현실적이다.

- **📢 섹션 요약 비유**: 레인지는 달력 서랍, 해시는 번호표 [[136_variance|분산]]함, 리스트는 이름표 서랍에 가깝다. 어떤 기준으로 꺼내 보고 어떤 기준으로 버릴지를 생각하면, 왜 리스트가 "의미 있는 코드 분리"에 강한지 바로 보인다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 리스트 [[179_table_partitioning_concept|파티셔닝]]은 **업무 코드가 작고 안정적이며, 그 코드로 자주 조회하거나 관리해야 하는 테이블**에 먼저 검토한다. 예를 들어 국내/해외 고객 [[001_dikw_pyramid|데이터]] 분리, 제휴/직영 채널 주문 분리, Bronze·Silver·Gold 같은 [[090_service_kubernetes_network_load_balancing|서비스]] 등급별 관리처럼 코드 자체가 운영 [[164_policy|정책]]과 연결될 때 적합하다.

반대로 아래 조건이면 신중해야 한다. 첫째, 코드 체계가 자주 바뀌면 `ALTER TABLE` 성격의 유지보수가 잦아진다. 둘째, 특정 값에 [[001_dikw_pyramid|데이터]]가 80~90% 몰리면 한 [[514_partition_slice_volume|파티션]]만 비대해지는 [[001_dikw_pyramid|데이터]] 쏠림 ([[001_dikw_pyramid|Data]] Skew)이 생긴다. 셋째, [[514_partition_slice_volume|파티션]] 키 값이 자주 수정되면 사실상 대량 행 재배치 작업이 발생한다.

### 기술사 판단 [[435_checklist_based_testing|체크리스트]]

1. 주요 조회가 특정 코드값에 대한 동등 조건 또는 `IN` 조건 중심인가?
2. 코드 종류가 충분히 안정적이며 변경 절차가 관리 가능한가?
3. 예외 값을 흡수할 `DEFAULT` [[514_partition_slice_volume|파티션]]과 정리 절차가 준비되어 있는가?
4. 특정 값 집중으로 인한 대형 [[514_partition_slice_volume|파티션]] 발생을 감당하거나 보완할 방법이 있는가?
5. [[514_partition_slice_volume|파티션]] 키 변경이 잦지 않아 행 이동 비용이 통제 가능한가?

### 자주 나오는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 신규 코드가 생길 수 있는데도 `DEFAULT` [[514_partition_slice_volume|파티션]] 없이 운영하는 경우
- `user_id`처럼 값 종류가 너무 많은 컬럼을 리스트 [[179_table_partitioning_concept|파티셔닝]]으로 억지 [[104_classification_analysis|분류]]하는 경우
- 값 분포 [[395_verification_process_review|검증]] 없이 "지역별로 나누면 보기 좋다"는 이유만으로 적용하는 경우
- [[632_state_transition_diagram_testing|상태 전이]]가 잦은 컬럼을 [[514_partition_slice_volume|파티션]] 키로 잡아 갱신 때마다 행 이동을 유발하는 경우

기술사 답안에서는 "지역별로 나누기 쉽다"에서 멈추면 부족하다. **프루닝 이점, 규제/권한 분리, DEFAULT 안전판, [[001_dikw_pyramid|데이터]] 쏠림과 행 이동 위험**을 함께 설명해야 실제 설계 판단으로 이어진다.

- **📢 섹션 요약 비유**: 도시를 구별로 나누어 행정 [[090_service_kubernetes_network_load_balancing|서비스]]를 하는 것은 효율적이지만, 인구가 한 구에만 몰리거나 행정구역 이름이 자주 바뀌면 오히려 창구가 더 혼잡해진다. 리스트 [[179_table_partitioning_concept|파티셔닝]]도 이름표가 명확할수록 좋지만, 이름표 체계가 흔들리면 관리 부담이 급격히 커진다.

---

## Ⅴ. 기대효과 및 결론

리스트 [[179_table_partitioning_concept|파티셔닝]]이 잘 맞으면 [[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]]과 운영 설명력이 함께 올라간다. 특정 코드값 조회에서 읽어야 할 물리 영역이 줄어들고, [[514_partition_slice_volume|파티션]] 단위로 [[555_backup_and_restore_strategy|백업]]·삭제·이관·권한 통제를 수행하기 쉬워진다. 즉 단순히 [[001_dikw_pyramid|데이터]]를 쪼개는 것이 아니라 **업무 [[104_classification_analysis|분류]]를 저장 구조에 정착시키는 효과**가 생긴다.

하지만 장점만 있는 것은 아니다. 코드 체계가 변하면 [[514_partition_slice_volume|파티션]] 정의도 따라 바뀌어야 하고, 특정 값 집중은 곧 특정 [[514_partition_slice_volume|파티션]] 집중으로 이어진다. 또한 시간 축 관리나 균등 [[136_variance|분산]]이 더 중요하다면 레인지나 해시, 또는 복합 [[179_table_partitioning_concept|파티셔닝]]이 더 적절할 수 있다.

결론적으로 리스트 [[179_table_partitioning_concept|파티셔닝]]은 "값의 의미를 잃지 않고 저장 구조를 나누는 방법"으로 기억하는 편이 맞다. 업무 코드 자체가 설계의 주인공일 때 선택해야 하며, 값 집합 관리와 예외 처리 [[268_strategy_pattern|전략]]까지 준비될 때 가장 큰 힘을 발휘한다.

- **📢 섹션 요약 비유**: 잘 정리된 도서관은 책을 아무렇게나 흩뿌리지 않고, 분야 이름표에 따라 서가를 나눈다. 리스트 [[179_table_partitioning_concept|파티셔닝]]도 [[001_dikw_pyramid|데이터]]를 그렇게 다루되, 새 분야 책이 들어왔을 때 어느 서가에 둘지 미리 준비해 두는 설계다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[514_partition_slice_volume|파티션]] 키 ([[514_partition_slice_volume|Partition]] [[067_db_key_uniqueness_minimality|Key]]) | 행이 어느 목록에 속하는지 결정하는 기준 컬럼 |
| 명시적 값 목록 | [[514_partition_slice_volume|파티션]]별 담당 코드 집합을 사람이 설계하는 규칙 |
| DEFAULT [[514_partition_slice_volume|파티션]] | 미분류 값과 신규 코드를 흡수하는 운영 안전판 |
| [[184_partition_pruning|파티션 프루닝]] ([[184_partition_pruning|Partition Pruning]]) | 조건에 맞는 [[514_partition_slice_volume|파티션]]만 읽어 동등 조회를 줄이는 최적화 |
| [[001_dikw_pyramid|데이터]] 쏠림 ([[001_dikw_pyramid|Data]] Skew) | 특정 값에 [[001_dikw_pyramid|데이터]]가 몰려 [[514_partition_slice_volume|파티션]] 크기와 [[282_performance_tactics|성능]]이 불균형해지는 현상 |
| 행 이동 (Row Movement) | [[514_partition_slice_volume|파티션]] 키 변경 시 다른 [[514_partition_slice_volume|파티션]]으로 물리 재배치가 일어나는 동작 |
| 복합 [[179_table_partitioning_concept|파티셔닝]] ([[183_composite_partitioning|Composite Partitioning]]) | 리스트의 의미 분리와 레인지·해시의 강점을 결합하는 확장 방식 |

### 📈 관련 키워드 및 발전 흐름도

```text
업무 코드 분리 필요
        │
        ▼
명시적 값 목록 설계
        │
        ▼
리스트 파티셔닝 (List Partitioning)
        │
        ├──────────────► 동등 조건 프루닝
        ├──────────────► 지역별/채널별 독립 관리
        ├──────────────► DEFAULT 파티션 운영
        └──────────────► Range + List / List + Hash 확장
```

### 👶 어린이를 위한 3줄 비유 설명

1. 리스트 [[179_table_partitioning_concept|파티셔닝]]은 장난감을 "자동차 상자", "인형 상자", "기타 상자"처럼 이름표 붙은 상자에 넣는 방법이에요.
2. 그래서 자동차만 찾고 싶으면 자동차 상자만 열어보면 되고, 다른 상자는 안 뒤져도 돼요.
3. 하지만 새 장난감 종류가 생기면 기타 상자에만 쌓이지 않게 이름표를 다시 정리해야 해요.
