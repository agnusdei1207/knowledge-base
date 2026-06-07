---
title: "134. Saga Pattern"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 134
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Saga는 <strong>여러 마이크로서비스에 걸친 비즈니스 <a href="/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a>을 로컬 <a href="/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a>의 시퀀스로 분해</strong>하고, 실패 시 <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/">보상 트랜잭션</a>(<a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/">Compensating Transaction</a>)</strong>으로 롤백하는 패턴이다.
> 2. **가치**: 2PC의 블로킹·[단일 장애점](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 문제 없이 <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 자율성을 유지</strong>하면서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)([Eventual Consistency](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/))을 달성한다.
> 3. **판단 포인트**: <strong>Choreography(이벤트 기반, 각 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 독립)</strong> vs <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/">Orchestration</a>(중앙 오케스트레이터)</strong> — [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수가 적으면 Choreography, 복잡하면 [Orchestration](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)(Temporal/Cadence).

---

## Ⅰ. 개요 및 필요성

```text
Choreography: 주문->이벤트->결제->이벤트->배송 (각자 독립)
Orchestration: 오케스트레이터->주문, ->결제, ->배송 (중앙 제어)
실패 시: 보상 트랜잭션 (주문 취소, 결제 환불)
```

- **📢 섹션 요약 비유**: Choreography는 재즈 즉흥(각자 연주), Orchestration은 교향곡(지휘자 지휘)이다.

---

## Ⅱ~Ⅴ. 결론

Saga는 <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a> <a href="/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/">분산 트랜잭션</a>의 사실상 표준</strong>이며, Temporal/Cadence가 [Orchestration](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) Saga의 대표 프레임워크이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/12_it_management/05_security_compliance/305_saga/">Saga</a></strong> | [분산 트랜잭션](/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) 패턴 |
| **Choreography** | 이벤트 기반 (독립) |
| <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/">Orchestration</a></strong> | 중앙 제어 (Temporal) |
| <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/">보상 트랜잭션</a></strong> | 실패 시 되돌리기 |
| <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/">Eventual Consistency</a></strong> | 최종 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[2PC (1990s)] -> [Saga 이론 (Garcia-Molina, 1987)]
    -> [MSA Saga 재발견 (2014~)]
    -> [Choreography (Kafka 이벤트)]
    -> [Orchestration (Temporal/Cadence, 2020~)]
    -> [현재: Durable Execution — Saga 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Saga는 <strong>릴레이 달리기</strong>예요. 각 선수가 자기 구간을 달리고 **바톤을 넘겨요**.
2. 한 선수가 넘어지면(실패) <strong>그 구간만 다시 달려요(<a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/">보상 트랜잭션</a>)</strong>.
3. 전원이 동시에 출발하는 것([2PC](/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/))보다 <strong>빠르고 안전</strong>하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 133 / 371

<- **이전**: [133. 2PC 한계와 MSA 분산 트랜잭션 - 왜 Saga가 필요한가](/studynote/13_cloud_architecture/03_msa_serverless/133_2pc_limitations/)
**다음**: [135. Choreography Saga - 이벤트 기반 분산 트랜잭션](/studynote/13_cloud_architecture/03_msa_serverless/135_choreography_saga/) ->

---
