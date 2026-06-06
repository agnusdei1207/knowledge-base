---
title: "Spanner"
date: "2026-04-10"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NewSQL은 SQL과 ACID를 유지하면서도 수평 확장을 가능하게 하려는 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 관계형 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 계열이다.
> 2. **가치**: [구글 스패너](/studynote/05_database/05_distributed_nosql_newsql/291_ods/)(Spanner)는 TrueTime으로 글로벌 [분산 트랜잭션](/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/)의 순서를 안정적으로 맞춘다.
> 3. **판단 포인트**: 강한 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 잠금, [샤딩](/studynote/05_database/05_distributed_nosql_newsql/280_sharding/), 합의 알고리즘을 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

기존 RDBMS는 정합성은 강하지만 수평 확장이 어렵고, NoSQL은 확장은 쉽지만 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 약한 경우가 많았다.

NewSQL은 이 둘 사이의 딜레마를 풀기 위해 등장했다. SQL과 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 유지하면서도 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)으로 확장하려는 시도다.

- **📢 섹션 요약 비유**: 빠른 자동차와 튼튼한 안전벨트를 같이 갖추려는 시도다.

---

## Ⅱ. NewSQL의 핵심

NewSQL은 기본적으로 관계형 모델을 유지한다.

- SQL을 쓸 수 있다.
- 조인과 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 가능하다.
- 수평 확장을 염두에 둔다.

이 점이 전통적인 RDBMS와 가장 큰 차이다.

- **📢 섹션 요약 비유**: 익숙한 언어로 말하면서도, 여러 나라를 동시에 오가는 통역 시스템이다.

---

## Ⅲ. [구글 스패너](/studynote/05_database/05_distributed_nosql_newsql/291_ods/)와 TrueTime

Google Spanner는 글로벌 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서 시간의 순서를 맞추기 위해 TrueTime을 활용한다.

```text
클라이언트 요청
   v
분산 노드
   v
TrueTime 기반 순서 결정
   v
트랜잭션 커밋
```

이 구조 덕분에 멀리 떨어진 데이터센터에서도 강한 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 제공할 수 있다.

- **📢 섹션 요약 비유**: 여러 사람이 동시에 적는 공책에, 같은 시계를 맞춰 쓰는 것과 같다.

---

## Ⅳ. [분산 트랜잭션](/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/)과 [샤딩](/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)

NewSQL은 데이터를 여러 조각으로 나누어 저장하면서도, 하나의 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)처럼 보이게 만든다.

- [샤딩](/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)으로 저장을 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)한다.
- 합의 알고리즘으로 순서를 맞춘다.
- [분산 트랜잭션](/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/)으로 정합성을 보장한다.

이 때문에 금융, 글로벌 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), [멀티 리전](/studynote/15_devops_sre/02_cicd_gitops/100_multi_region_deployment_pipeline_disaster_recovery/) 시스템에 적합하다.

- **📢 섹션 요약 비유**: 여러 창고에 물건을 나눠 두되, 한 장부로 정확히 관리하는 방식이다.

---

## Ⅴ. 실무 적용과 한계

NewSQL은 강력하지만 만능은 아니다.

- 복잡한 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 환경을 설계해야 한다.
- 운영 난이도가 높다.
- 지연과 비용을 함께 고려해야 한다.

그럼에도 SQL과 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 포기하지 않으면서 확장하려는 환경에서는 매우 강한 선택지다.

- **📢 섹션 요약 비유**: 넓은 집을 얻으려면 집 구조를 더 복잡하게 지어야 하는 것과 같다.

---

## 관련 개념 맵

```text
RDBMS / NoSQL 딜레마
   v
NewSQL
   v
TrueTime / 합의 / 샤딩
   v
분산 트랜잭션
```

---

## 관련 키워드 및 발전 흐름도

1. 전통 RDBMS -> 강한 정합성, 낮은 확장성
2. [NoSQL](/studynote/14_data_engineering/01_infrastructure/035_nosql/) -> 높은 확장성, 약한 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)
3. NewSQL -> 둘의 장점 결합 시도
4. Spanner / TrueTime -> 글로벌 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 해법
5. [분산 트랜잭션](/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) 아키텍처 -> 현대 대규모 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 기반

---

## 어린이를 위한 3줄 비유 설명

NewSQL은 여러 장난감 상자를 한꺼번에 관리하면서도 하나의 규칙을 지키는 거예요.
멀리 떨어진 상자라도 같은 시계로 맞춰서 정리해요.
그래서 커져도 헷갈리지 않게 관리할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 58 / 258

<- **이전**: [57. 시계열 데이터베이스 (Time-Series Database, TSDB) - 다운샘플링과 보존 정책](/studynote/14_data_engineering/01_infrastructure/057_tsdb_downsampling_retention_policy/)
**다음**: [59. 블룸 필터 (Bloom Filter) - 디스크 I/O 최적화 확률적 검색](/studynote/14_data_engineering/01_infrastructure/059_bloom_filter_false_positive_disk_io/) ->

---
