---
title: "087. Fp Growth Algorithm Frequent Pattern Tree"
date: "2026-03-04"
tags:
  - "math-mining"
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)

    > 1. **본질**: FP-Growth (Frequent Pattern Growth)는 후보집합을 대량 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하지 않고 Frequent Pattern Tree (FP-tree)를 통해 빈발 항목집합을 찾는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.
    > 2. **가치**: 거래 수가 많고 항목이 자주 함께 등장할수록 FP-tree [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 효과가 커져 Apriori보다 빠르게 동작한다.
    > 3. **판단 포인트**: 최소 [지지도](/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/) (Minimum [Support](/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/))가 너무 낮으면 트리와 조건부 트리가 폭발할 수 있으므로, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 밀도와 메모리를 함께 봐야 한다.

    ---

    ## Ⅰ. 개요 및 필요성

    FP-Growth (Frequent Pattern Growth)은 [연관 규칙](/studynote/16_bigdata/05_analysis/106_association_rules/) 학습에서 빈발 항목집합을 찾는 대표적인 방법이다. Apriori처럼 후보를 여러 단계로 만들어 검증하지 않고, 거래를 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)한 FP-tree를 한 번 구성한 뒤 [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/)적으로 조건부 패턴을 찾는다.

이 방식이 필요한 이유는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 커질수록 후보집합 폭발이 심해지기 때문이다. 특히 장바구니처럼 서로 자주 같이 등장하는 항목이 많은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서는 반복 스캔보다 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 구조가 훨씬 유리하다.

    - **📢 섹션 요약 비유**: 장바구니를 일일이 다시 보는 대신, 공통으로 겹치는 물건 묶음을 한 상자에 정리하는 방법이다.

    ---

    ## Ⅱ. 아키텍처 및 핵심 원리

    FP-Growth의 흐름은 1차 스캔으로 항목 빈도를 세고, 2차 스캔으로 정렬된 거래를 FP-tree에 넣는 것이다. 그다음 Header Table을 따라 특정 항목의 조건부 패턴 베이스를 만들고, 조건부 FP-tree를 [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/)적으로 파고든다.

| 단계 | 역할 | 산출물 |
| :-- | :-- | :-- |
| 빈도 집계 | 최소 [지지도](/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/) 이하 항목 제거 | 빈발 항목 목록 |
| 정렬 삽입 | 거래를 빈도순으로 삽입 | FP-tree |
| Header Table | 동일 항목 노드 연결 | 탐색 포인터 |
| 조건부 패턴 베이스 | 특정 항목의 접두 경로 수집 | 조건부 입력 |
| [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/) 확장 | 더 작은 FP-tree로 분해 | 빈발 항목집합 |

```text
root
 +- f:4 - a:3 - c:2
 |        +- m:2
 +- c:3 - b:2 - p:1

Header Table: f -> a -> c -> m -> b -> p
```

[압축](/studynote/02_operating_system/06_memory_management/347_compaction/)의 핵심은 같은 접두사를 공유하는 거래를 한 노드 경로로 묶는 데 있다. 그래서 트리는 단순 저장소가 아니라 탐색 공간 자체를 줄이는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조가 된다.

    - **📢 섹션 요약 비유**: 같은 앞부분을 가진 줄넘기 명단을 한 번에 묶어 적는 것처럼, 반복되는 시작점을 합쳐 저장한다.

    ---

    ## Ⅲ. 비교 및 연결

    Apriori와 비교하면 차이가 분명하다.

| 항목 | Apriori | FP-Growth |
| :-- | :-- | :-- |
| 후보 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 단계별로 대량 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하지 않음 |
| DB 스캔 | 여러 번 반복 | 보통 2회 중심 |
| 메모리 | 후보집합 관리 부담 | 트리 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 부담 |
| 적합 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 희소하고 단순한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 밀집하고 반복 패턴이 많은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |

FP-Growth는 [연관 규칙](/studynote/16_bigdata/05_analysis/106_association_rules/)에서 빈발 항목집합을 먼저 찾고, 그 뒤 confidence와 lift를 계산하는 흐름과 잘 맞는다. 즉 "규칙을 바로 찾는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)"이 아니라, 규칙의 재료가 되는 패턴을 효율적으로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)해 주는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.

    - **📢 섹션 요약 비유**: 한 장씩 계산표를 만드는 대신, 자주 쓰는 첫 글자를 묶은 색인표로 찾는 방식과 비슷하다.

    ---

    ## Ⅳ. 실무 적용 및 기술사 판단

    실무에서는 다음 조건이면 FP-Growth를 먼저 검토한다. 거래 수가 많고, 각 거래의 길이가 길며, 자주 함께 사는 조합이 반복될 때다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 항목 정렬 기준을 빈도 내림차순으로 고정했는가?
2. 최소 [지지도](/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/)를 너무 낮게 잡아 폭발하지 않는가?
3. 조건부 트리 메모리를 감당할 수 있는가?
4. 빈발 패턴 이후 규칙 평가를 따로 수행하는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 희소한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 무조건 FP-Growth를 쓰는 것
- 정렬과 [가지치기](/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/)를 생략해 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 효과를 잃는 것
- [지지도](/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/)만 보고 규칙 품질을 판단하는 것

    - **📢 섹션 요약 비유**: 너무 드문 물건까지 다 세려고 하면 상자가 터지니, 자주 나오는 것부터 고르는 게 중요하다.

    ---

    ## Ⅴ. 기대효과 및 결론

    FP-Growth는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스를 더 많이 읽지 않으면서도 의미 있는 반복 패턴을 찾게 해 준다. 그래서 시장 바구니 분석, 추천 후보 추출, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 패턴 탐색에 모두 유용하다.

다만 트리가 작다고 항상 빠른 것은 아니다. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포가 매우 다양하면 조건부 트리가 다시 커질 수 있으므로, FP-Growth는 "[압축](/studynote/02_operating_system/06_memory_management/347_compaction/)이 잘 먹히는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조"를 만났을 때 가장 빛난다.

    - **📢 섹션 요약 비유**: 같은 도장을 찍은 쪽지를 한 줄로 이어 붙여 두면, 나중에 찾을 일이 훨씬 빨라진다.

    ---

    ### 📌 관련 개념 맵

    | 개념 | 연결 포인트 |
| :-- | :-- |
| Frequent Pattern Tree (FP-tree) | 거래 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)을 위한 핵심 구조 |
| Header Table | 동일 항목 노드 연결 |
| Conditional Pattern Base | 조건부 패턴 추출 재료 |
| Minimum [Support](/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/) | 빈발성 판단 기준 |
| [Association Rule](/studynote/14_data_engineering/02_math_mining/083_association_rule_apriori_market_basket/) Mining | 빈발 항목집합 이후의 규칙 분석 |

    ### 📈 관련 키워드 및 발전 흐름도

    거래 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)
    |
    v
항목 빈도 집계 / [가지치기](/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/)
    |
    v
FP-tree 구성
    |
    v
조건부 패턴 베이스
    |
    v
빈발 항목집합과 [연관 규칙](/studynote/16_bigdata/05_analysis/106_association_rules/)

    ### 👶 어린이를 위한 3줄 비유 설명

    1. 장바구니를 매번 처음부터 세지 말고, 비슷한 것끼리 묶어 보면 쉬워요.
    2. 공통된 길을 먼저 그려 두면, 숨은 패턴을 더 빨리 찾을 수 있어요.
    3. 그래서 FP-Growth는 같은 시작점을 모아 지도를 만드는 방법이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 87 / 258

<- **이전**: [86. 향상도 (Lift) - 연관 규칙의 유의성 검증 지표](/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/)
**다음**: [88. 머신러닝 교차 검증 (K-Fold Cross Validation) - 모델 일반화 성능 측정](/studynote/14_data_engineering/02_math_mining/088_k_fold_cross_validation_overfitting_generalization/) ->

---
