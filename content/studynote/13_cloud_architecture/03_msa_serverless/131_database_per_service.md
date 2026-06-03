+++
title = "131. Database per Service - MSA 데이터 분리 패턴"
date = 2026-04-19

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per Service는 **각 마이크로서비스가 독립적인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스를 소유**하여 다른 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 직접 DB에 접근하지 못하고 **오직 API로만 통신**하는 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 패턴이다.
> 2. **가치**: 공유 DB에서는 한 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변경이 **다른 모든 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 영향**을 주지만, DB per Service는 **독립 배포·독립 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)·기술 다양성([Polyglot Persistence](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/132_polyglot_persistence/))**을 보장한다.
> 3. **판단 포인트**: [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 JOIN이 불가능해지므로 **[Saga](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)([분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/))·[CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/)([쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 분리)·[이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)**이 함께 필요하며, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 **[Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)**로 관리한다.

---

## Ⅰ. 개요 및 필요성

```text
공유 DB: 서비스 A·B·C → 같은 DB (커플링)
DB per Service: A→DB_A, B→DB_B, C→DB_C (독립)
  서비스 간: API·이벤트로만 통신
```

- **📢 섹션 요약 비유**: 공유 DB는 **공동 냉장고**(한 사람이 정리하면 다른 사람 물건이 밀려남), DB per Service는 **각자 냉장고**(독립 관리).

---

## Ⅱ. 아키텍처 및 핵심 원리

| 비교 | 공유 DB | DB per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |
|:---|:---|:---|
| **커플링** | 높음 | **낮음** |
| **배포** | 종속 | **독립** |
| **[JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/)** | 가능 | **불가 → [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)/이벤트** |
| **[일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)** | Strong | **Eventual** |

---

## Ⅲ~Ⅴ. 결론

DB per Service는 **MSA의 [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/) 핵심 원칙**이며, [Saga](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)·[CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/)·[이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)과 함께 적용해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **DB per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)** | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 독립 DB |
| **[Saga](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)** | [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) 패턴 |
| **[CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/)** | 명령/[쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 분리 |
| **[Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)** | 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |
| **[Polyglot Persistence](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/132_polyglot_persistence/)** | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 다른 DB 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
[공유 DB (모노리스)] → [DB per Service (MSA, 2014~)]
    → [Saga 패턴 (분산 트랜잭션)]
    → [CQRS + Event Sourcing (2016~)]
    → [현재: 데이터 메시 — 도메인별 데이터 소유]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 공유 DB는 **공동 냉장고**예요. 한 사람이 정리하면 **다른 사람 물건이 밀려나요**.
2. DB per Service는 **각자 냉장고**예요. 자기 냉장고를 **독립적으로 관리**해요.
3. 대신 남의 냉장고 물건이 필요하면 **부탁([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/))**해야 한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 130 / 371

← **이전**: [130. Bulkhead 패턴 - 격벽으로 장애 격리](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/130_bulkhead_pattern/)
**다음**: [132. Polyglot Persistence - MSA 서비스별 최적 DB 선택](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/132_polyglot_persistence/) →

---
