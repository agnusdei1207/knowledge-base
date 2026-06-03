+++
title = "132. Polyglot Persistence - MSA 서비스별 최적 DB 선택"
date = 2026-04-19

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Polyglot Persistence는 <strong>각 마이크로서비스가 자신의 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 특성에 가장 적합한 DB 기술을 독립적으로 선택</strong>하는 패턴이며, DB per Service의 자연스러운 확장이다.
> 2. **가치**: 모든 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 같은 RDBMS를 사용하면 <strong><a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/">그래프</a> <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>에 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a> 지옥, 시계열에 비효율 <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a></strong>가 발생하지만, Polyglot은 <strong>주문=RDB, 추천=<a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/">그래프</a>DB, <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a>=시계열DB</strong>로 최적화한다.
> 3. **판단 포인트**: 운영 복잡도(다양한 DB 관리)가 증가하므로, <strong>관리형 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>(RDS·<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/">DynamoDB</a>·Neptune)</strong>로 운영 부담을 줄이는 것이 현실적이다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">주문 서비스 → PostgreSQL (관계형, ACID)</div>
<div class="kb-diagram-note">카탈로그 → MongoDB (문서형, 유연 스키마)</div>
<div class="kb-diagram-note">추천 → Neo4j (그래프, 관계 탐색)</div>
<div class="kb-diagram-note">캐시 → Redis (인메모리, 고속)</div>
<div class="kb-diagram-note">로그 → InfluxDB (시계열)</div>
</div>
</div>



- **📢 섹션 요약 비유**: Polyglot은 <strong>요리마다 최적의 칼(도구)을 쓰는 것</strong>이다. 모든 요리에 식빵 칼만 쓸 순 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유형 | 최적 DB |
|:---|:---|
| **관계형** | PostgreSQL, MySQL |
| **문서** | [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/">그래프</a></strong> | Neo4j |
| **키-값** | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/), [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) |
| **시계열** | [InfluxDB](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/255_time_series_rollup_retention_compression/), TimescaleDB |

---

## Ⅲ~Ⅴ. 결론

Polyglot Persistence는 <strong>MSA의 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 최적화 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>이며, 관리형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 운영 부담을 줄이는 것이 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Polyglot** | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 최적 DB |
| <strong>DB per <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a></strong> | Polyglot의 전제 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/">NoSQL</a></strong> | 비관계형 DB |
| <strong>관리형 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a></strong> | 운영 부담 감소 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/">CAP</a> 정리</strong> | DB 선택 기준 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">단일 RDBMS (모노리스)</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">NoSQL 등장 (2010s)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Polyglot Persistence (MSA, 2014~)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">관리형 서비스 (AWS RDS/DynamoDB)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">현재: NewSQL + Polyglot — 최적 조합</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. Polyglot은 <strong>요리마다 최적의 칼</strong>을 쓰는 거예요. 빵에는 빵 칼, 고기에는 고기 칼!
2. 모든 요리에 **식빵 칼만 쓰면** 비효율적이에요.
3. 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 <strong>가장 잘 맞는 DB</strong>를 골라주면 성능이 좋아진답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 131 / 371

← **이전**: [131. Database per Service - MSA 데이터 분리 패턴](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/131_database_per_service/)
**다음**: [133. 2PC 한계와 MSA 분산 트랜잭션 - 왜 Saga가 필요한가](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/133_2pc_limitations/) →

---
