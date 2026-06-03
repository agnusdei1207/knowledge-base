---
title: 165. 비용 기반 옵티마이저 (CBO, Cost Based Optimizer) - 시스템 통계 정보 기반, 디스크 I/O 등 최소 비용
  계산 (현대 RDBMS)
date: '2026-05-05'
tags:
- studynote-database
---

## 핵심 인사이트

> 1. **본질**: 비용 기반 [[163_optimizer_sql_execution_plan_generator|옵티마이저]] (CBO, Cost Based [[088_optimizer|Optimizer]])는 SQL (Structured Query Language)을 실행할 때 테이블 통계와 비용 모델을 이용해 가장 저렴한 [[166_execution_plan_optimizer_navigation_tree|실행 계획]] ([[166_execution_plan_optimizer_navigation_tree|Execution Plan]])을 고르는 [[002_database_definition|데이터베이스]]의 판단 엔진이다.
> 2. **가치**: 같은 조건식이라도 [[170_selectivity_cardinality_distribution_tuning|선택도]] ([[170_selectivity_cardinality_distribution_tuning|Selectivity]]), 카디널리티 (Cardinality), [[154_database_index_b_tree_search_optimization|인덱스]] 구조에 따라 [[154_database_index_b_tree_search_optimization|인덱스]] 스캔과 전체 테이블 스캔의 유불리가 달라지므로, CBO는 대용량 환경에서 응답시간과 자원 사용량을 크게 좌우한다.
> 3. **판단 포인트**: CBO는 똑똑하지만 만능은 아니어서 통계가 낡거나 [[001_dikw_pyramid|데이터]] 분포가 치우치면 오판할 수 있으므로, 실무에서는 통계 품질·[[166_execution_plan_optimizer_navigation_tree|실행 계획]] [[395_verification_process_review|검증]]·[[167_sql_hint_optimizer_override|힌트]] 사용 절제를 함께 관리해야 한다.

---

## Ⅰ. 개요 및 필요성

비용 기반 [[163_optimizer_sql_execution_plan_generator|옵티마이저]] (CBO, Cost Based [[088_optimizer|Optimizer]])는 [[003_dbms_database_management_system|데이터베이스 관리 시스템]] ([[502_dbms|DBMS]], [[501_database|Database]] [[372_management|Management]] System)이 SQL을 실제로 어떻게 읽고 조인할지 결정할 때, **고정 규칙이 아니라 예상 비용**을 기준으로 판단하는 최적화 방식이다. 즉 개발자가 "무엇을 구할지"를 적으면, CBO가 그 결과를 가장 적은 입출력 (I/O, Input/Output)과 중앙처리장치 (CPU, Central Processing Unit) 자원으로 얻는 길을 선택한다.

이 방식이 중요해진 이유는 [[001_dikw_pyramid|데이터]] 규모와 [[298_qkv_attention|쿼리]] 조합이 너무 커졌기 때문이다. 소규모 시스템에서는 [[154_database_index_b_tree_search_optimization|인덱스]]가 있으면 타는 단순 규칙도 어느 정도 통했지만, 수천만 건 테이블과 복합 조인이 늘어나자 같은 규칙이 오히려 대형 병목을 만들기 시작했다. 특히 조건에 맞는 행이 많을 때는 [[154_database_index_b_tree_search_optimization|인덱스]]의 랜덤 I/O가 순차적인 전체 스캔보다 더 비싸질 수 있어, 실제 비용을 계산하지 않으면 안정적인 [[282_performance_tactics|성능]]을 기대하기 어렵다.

이 그림은 CBO가 단순 문법 해석기가 아니라, 통계와 비용 모델을 바탕으로 물리 경로를 정하는 의사결정기임을 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                CBO의 기본 역할: SQL을 비용 기반으로 해석            │
├──────────────────────────────────────────────────────────────────────┤
│ SQL Text                                                            │
│   │                                                                  │
│   ▼                                                                  │
│ Parse / Rewrite ──▶ Statistics Check ──▶ Candidate Plans             │
│                                   │                 │                │
│                                   ▼                 ▼                │
│                         Selectivity / Cardinality   Cost Compare     │
│                                                      │               │
│                                                      ▼               │
│                                               Best Execution Plan    │
└──────────────────────────────────────────────────────────────────────┘
```

핵심은 CBO가 "[[154_database_index_b_tree_search_optimization|인덱스]]가 있느냐"만 보는 것이 아니라, **그 [[154_database_index_b_tree_search_optimization|인덱스]]를 타는 편이 정말 싼가**를 따진다는 점이다. 그래서 현대 SQL 튜닝은 문법 암기보다 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]과 통계를 읽는 능력이 더 중요해졌다.

- **📢 섹션 요약 비유**: CBO는 종이 지도만 보는 길안내가 아니라, 현재 교통량과 통행료까지 계산해 가장 덜 힘든 길을 추천하는 내비게이션과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CBO는 보통 **통계 수집 결과 [[316_reference_pattern_nosql|참조]] → 후보 계획 [[087_process_state_transition|생성]] → 비용 추정 → 최종 선택** 순서로 동작한다. 통계에는 테이블 행 수, 블록 수, [[154_database_index_b_tree_search_optimization|인덱스]] 깊이, 값 분포, 히스토그램 (Histogram) 같은 정보가 포함된다. 이 정보가 있어야 특정 조건이 전체의 0.1%를 읽는지, 30%를 읽는지 예측할 수 있고, 그 예측값으로 접근 경로와 [[176_join_order_optimization|조인 순서]]를 계산할 수 있다.

| 단계 | CBO가 하는 일 | 핵심 판단 기준 |
| :--- | :--- | :--- |
| 통계 [[316_reference_pattern_nosql|참조]] | 테이블·[[154_database_index_b_tree_search_optimization|인덱스]]·분포 정보 [[396_validation|확인]] | 최신성, [[001_dikw_pyramid|데이터]] 편향 |
| 접근 경로 선택 | [[154_database_index_b_tree_search_optimization|인덱스]] 범위 스캔, 전체 스캔 등 비교 | [[170_selectivity_cardinality_distribution_tuning|선택도]], 클러스터링 |
| 조인 계획 [[087_process_state_transition|생성]] | [[176_join_order_optimization|조인 순서]]·구동 테이블·조인 방식 결정 | 예상 결과 건수 |
| 비용 계산 | I/O, CPU, 메모리 비용 추정 | 비용 모델, 시스템 특성 |
| 계획 확정 | 최소 비용 경로 채택 | 전체 예상 비용 |

아래 그림은 하나의 SQL이 여러 후보 계획으로 갈라졌다가, 비용 비교를 통해 하나로 수렴하는 과정을 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                  후보 계획 생성과 비용 비교 흐름                    │
├──────────────────────────────────────────────────────────────────────┤
│ Query                                                                │
│  │                                                                   │
│  ▼                                                                   │
│ Rewrite                                                               │
│  ├─ Plan A: Index Range Scan + Nested Loop                           │
│  ├─ Plan B: Full Table Scan + Hash Join                              │
│  └─ Plan C: Index Scan + Sort Merge Join                             │
│                 │        │        │                                   │
│                 └────────┴────────┴──▶ Cost Estimation               │
│                                         │                             │
│                                         ▼                             │
│                                   Lowest Cost Plan                    │
└──────────────────────────────────────────────────────────────────────┘
```

예를 들어 주문 테이블 1,000만 건 중 100건만 찾는다면 [[154_database_index_b_tree_search_optimization|인덱스]] 범위 스캔이 유리할 수 있다. 반대로 300만 건을 읽어야 한다면, [[154_database_index_b_tree_search_optimization|인덱스]]를 따라가며 행마다 테이블 블록을 다시 찾는 랜덤 I/O가 오히려 더 무거워져 전체 테이블 스캔이 더 경제적일 수 있다. CBO의 핵심 원리는 바로 이런 **손익분기점**을 기계적으로 계산하는 데 있다.

또한 조인에서도 같은 원리가 적용된다. 소량 조회에는 [[172_nl_join_nested_loop|중첩 루프 조인]] ([[431_nested_loop_join|Nested Loop Join]])이 효율적일 수 있지만, 대량 결합에는 [[174_hash_join|해시 조인]] ([[174_hash_join|Hash Join]])이 더 유리하다. 그래서 CBO는 단순히 빠른 연산자를 찾는 것이 아니라, **현재 [[001_dikw_pyramid|데이터]]량에 맞는 연산 [[268_strategy_pattern|전략]]**을 고른다.

- **📢 섹션 요약 비유**: CBO는 식당 주방에서 주문량을 보고 냄비 하나로 할지 대형 조리기로 돌릴지 결정하는 총괄 셰프와 같다.

---

## Ⅲ. 비교 및 연결

CBO를 이해하려면 [[164_rbo_rule_based_optimizer|규칙 기반 옵티마이저]] (RBO, Rule Based [[088_optimizer|Optimizer]])와 비교하는 것이 가장 효과적이다. RBO는 고정 규칙 덕분에 예측은 쉬웠지만 [[001_dikw_pyramid|데이터]] 변화에 둔감했다. 반면 CBO는 통계와 비용 모델을 이용해 적응적으로 판단하므로, 대규모 [[001_dikw_pyramid|데이터]]와 복잡한 조인에서 훨씬 현실적인 계획을 만든다.

| 항목 | RBO | CBO |
| :--- | :--- | :--- |
| 판단 기준 | 사전 정의 규칙 순서 | 통계 기반 비용 계산 |
| [[001_dikw_pyramid|데이터]] 변화 대응 | 낮음 | 높음 |
| 장점 | 예측 용이, 단순함 | 대용량·복합 [[298_qkv_attention|쿼리]]에 강함 |
| 약점 | 비효율 고착 가능 | 통계 오류에 민감 |
| 실무 위치 | 레거시 이해용 | 현대 RDBMS의 기본 |

CBO는 [[154_database_index_b_tree_search_optimization|인덱스]] 설계, 히스토그램, [[166_execution_plan_optimizer_navigation_tree|실행 계획]], [[167_sql_hint_optimizer_override|힌트]]와도 긴밀히 연결된다. [[170_selectivity_cardinality_distribution_tuning|선택도]]가 높은 조건은 [[154_database_index_b_tree_search_optimization|인덱스]] 친화적이고, [[001_dikw_pyramid|데이터]] 편향이 큰 컬럼은 히스토그램이 있어야 정확한 예측이 가능하다. 반대로 통계가 부정확하면 CBO는 계산을 잘해도 입력이 틀려 잘못된 결론을 낼 수 있다.

즉 CBO의 한계는 [[001_algorithm_definition|알고리즘]]보다 **관측 [[001_dikw_pyramid|데이터]]의 품질**에 더 가깝다. 이 점에서 CBO는 [[002_database_definition|데이터베이스]] 내부 기술이면서도 운영 자동화, 배치 통계 수집, [[609_performance_monitoring|성능 모니터링]]과 연결되는 실무형 주제다.

- **📢 섹션 요약 비유**: RBO가 규정집만 보고 사람을 배치하는 관리자라면, CBO는 오늘 손님 수와 주방 상태를 보고 인력을 다시 짜는 점장에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 CBO는 특히 **[[001_dikw_pyramid|데이터]] 성장 속도가 빠른 [[090_service_kubernetes_network_load_balancing|서비스]]**에서 중요하다. 예를 들어 프로모션 직후 주문 [[001_dikw_pyramid|데이터]]가 평소보다 50배 늘었는데 통계가 갱신되지 않으면, [[163_optimizer_sql_execution_plan_generator|옵티마이저]]는 여전히 과거의 작은 테이블로 착각해 비효율적인 [[154_database_index_b_tree_search_optimization|인덱스]] 경로를 고를 수 있다. 이 경우 SQL 자체보다 통계 최신화가 더 직접적인 해결책이 된다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. [[166_execution_plan_optimizer_navigation_tree|실행 계획]]의 예상 행 수와 실제 행 수가 크게 어긋나지 않는가?
2. 테이블·[[154_database_index_b_tree_search_optimization|인덱스]] 통계가 최근 적재량과 분포 변화를 반영하는가?
3. 히스토그램이 필요한 편향 컬럼을 단순 평균값으로 처리하고 있지 않은가?
4. [[154_database_index_b_tree_search_optimization|인덱스]]를 강제로 태우는 [[167_sql_hint_optimizer_override|힌트]]보다 SQL 구조와 통계를 먼저 점검했는가?
5. [[176_join_order_optimization|조인 순서]] 변경, 서브쿼리 변환, 조건 푸시다운이 계획에 어떤 영향을 주는지 [[396_validation|확인]]했는가?

### 판단 원칙

- **우선 채택**: 통계가 신뢰 가능하고 일반적인 조회 패턴이라면 CBO의 선택을 기본적으로 신뢰한다.
- **보완 필요**: 계획이 흔들리면 [[167_sql_hint_optimizer_override|힌트]]보다 통계 갱신, [[154_database_index_b_tree_search_optimization|인덱스]] 재설계, SQL 재작성을 먼저 검토한다.
- **주의 상황**: 배치 적재 직후, [[001_dikw_pyramid|데이터]] 편향이 심한 컬럼, [[190_bind_variable_soft_parsing|바인드 변수]] 분포 차이가 큰 구간은 오판 가능성이 높다.

기술사 답안에서는 "CBO가 자동으로 최적화한다"고만 쓰면 부족하다. 통계 기반이라는 장점과 함께, 통계 불일치 시 잘못된 계획이 나올 수 있다는 한계를 같이 설명해야 설계 판단이 살아난다.

- **📢 섹션 요약 비유**: CBO 튜닝은 운전대를 억지로 꺾는 일이 아니라, 내비게이션 지도가 최신인지 먼저 [[396_validation|확인]]하는 일과 같다.

---

## Ⅴ. 기대효과 및 결론

잘 동작하는 CBO는 같은 하드웨어에서도 더 적은 I/O와 더 짧은 응답시간을 만들어 낸다. 이는 단순한 [[298_qkv_attention|쿼리]] 속도 향상을 넘어, [[228_batch_processing_hadoop_spark|배치 처리]] 시간 단축, 피크 시간대 서버 안정성 개선, 인프라 증설 [[015_지연_데이터_관점|지연]] 같은 효과로 이어진다. 특히 복합 조인과 대용량 분석이 늘수록 CBO의 가치가 더 커진다.

다만 CBO는 "자동 [[282_performance_tactics|성능]] 보장 장치"가 아니다. 비용 모델은 결국 통계에 의존하고, 통계는 현실 [[001_dikw_pyramid|데이터]]를 완벽히 [[016_replication_factor|복제]]하지 못한다. 따라서 CBO는 맹신의 대상이 아니라, [[166_execution_plan_optimizer_navigation_tree|실행 계획]]과 통계 품질을 함께 관리할 때 힘을 발휘하는 **적응형 의사결정 엔진**으로 기억하는 것이 정확하다.

앞으로는 적응형 [[298_qkv_attention|쿼리]] 처리, 실행 중 재최적화, 피드백 기반 카디널리티 보정 같은 기능이 더 중요해질 가능성이 크다. 그래도 본질은 변하지 않는다. CBO는 SQL의 문장 모양이 아니라, **물리적으로 가장 싼 길을 찾는 계산기**다.

- **📢 섹션 요약 비유**: 좋은 CBO는 가장 짧은 길만 찾는 사람이 아니라, 차가 막혀도 연료를 가장 적게 쓰며 목적지에 도착하게 만드는 숙련 기사와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[166_execution_plan_optimizer_navigation_tree|실행 계획]] ([[166_execution_plan_optimizer_navigation_tree|Execution Plan]]) | CBO가 최종적으로 선택하는 물리 경로 |
| [[170_selectivity_cardinality_distribution_tuning|선택도]] ([[170_selectivity_cardinality_distribution_tuning|Selectivity]]) | [[154_database_index_b_tree_search_optimization|인덱스]] 사용 여부를 좌우하는 핵심 지표 |
| 카디널리티 (Cardinality) | 각 단계에서 예상되는 결과 행 수 |
| 히스토그램 (Histogram) | [[001_dikw_pyramid|데이터]] 편향을 반영해 비용 예측 정확도를 높임 |
| [[167_sql_hint_optimizer_override|힌트]] ([[167_sql_hint_optimizer_override|Hint]]) | CBO 판단을 강제로 유도하는 최후 수단 |
| RBO (Rule Based [[088_optimizer|Optimizer]]) | CBO와 대비되는 과거 최적화 방식 |

### 📈 관련 키워드 및 발전 흐름도

```text
고정 규칙 기반 최적화
    │
    ▼
RBO (Rule Based Optimizer)
    │
    ▼
통계 수집 · 선택도 · 카디널리티
    │
    ▼
CBO (Cost Based Optimizer)
    │
    ▼
히스토그램 · 적응형 최적화 · 실행 중 재최적화
```

이 흐름은 [[002_database_definition|데이터베이스]] 최적화가 "규칙 암기"에서 "통계 기반 적응"으로 발전해 온 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. CBO는 장난감을 찾을 때 어디부터 보면 제일 빨리 찾을지 먼저 계산해 주는 똑똑한 도우미예요.
2. 조금만 찾으면 서랍을 열고, 많이 찾아야 하면 상자를 통째로 뒤지는 게 더 빠를 수도 있어요.
3. 그래서 컴퓨터는 무조건 한 방법만 쓰지 않고, 그때그때 가장 덜 힘든 방법을 고른답니다.
