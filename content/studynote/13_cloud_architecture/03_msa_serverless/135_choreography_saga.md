---
title: "135. Choreography Saga - 이벤트 기반 분산 트랜잭션"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Choreography Saga는 <strong>중앙 오케스트레이터 없이 각 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>가 이벤트를 발행·구독하여 자율적으로 <a href="/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a>을 <a href="/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/">진행</a></strong>하는 [분산 트랜잭션](/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) 패턴이다.
> 2. **가치**: 중앙 제어점([단일 장애점](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/))이 없어 <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 자율성·독립 배포·느슨한 결합</strong>이 유지되지만, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수가 많아지면 이벤트 흐름 추적이 어려워진다(디버깅 복잡도^).
> 3. **판단 포인트**: [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 3~5개 이하면 Choreography, 복잡한 비즈니스 흐름이면 [Orchestration](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)(Temporal)이 적합하며, [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)·RabbitMQ가 이벤트 브로커이다.

---

## Ⅰ. 개요 및 필요성

```text
주문 서비스 -> "주문 생성" 이벤트 발행
결제 서비스 <- 구독 -> 결제 처리 -> "결제 완료" 이벤트 발행
배송 서비스 <- 구독 -> 배송 시작
실패 시: "결제 실패" 이벤트 -> 주문 서비스 -> 보상(주문 취소)
```

- **📢 섹션 요약 비유**: Choreography는 <strong>재즈 즉흥 연주</strong>이다. 지휘자 없이 각 연주자가 서로의 소리를 듣고 자율적으로 연주한다.

---

## Ⅱ~Ⅴ. 결론

Choreography는 <strong>소규모 MSA의 <a href="/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/">분산 트랜잭션</a>에 적합</strong>하며, 이벤트 브로커([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/))가 핵심 인프라이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Choreography** | 이벤트 기반 자율 |
| **이벤트 브로커** | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)·RabbitMQ |
| <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/">보상 트랜잭션</a></strong> | 실패 시 되돌리기 |
| <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/">Orchestration</a></strong> | 대안 (중앙 제어) |
| <strong><a href="/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/">이벤트 소싱</a></strong> | 이벤트 저장·재생 |

### 📈 관련 키워드 및 발전 흐름도

```text
[2PC (모노리스)] -> [Choreography Saga (MSA, 2014~)]
    -> [Kafka 이벤트 기반 (2016~)]
    -> [Orchestration 대안 (Temporal, 2020~)]
    -> [현재: 하이브리드 — Choreography + Orchestration 혼합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Choreography는 <strong>재즈 즉흥</strong>이에요. 지휘자 없이 **서로 듣고 맞춰** 연주해요.
2. 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 "나 끝났어!" **이벤트를 보내면** 다음 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 시작해요.
3. 연주자([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))가 적으면 좋지만, 많으면 <strong>교향곡(<a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/">Orchestration</a>)</strong>이 더 좋아요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 134 / 371

<- **이전**: [134. Saga 패턴 - MSA 분산 트랜잭션의 표준 솔루션](/studynote/13_cloud_architecture/03_msa_serverless/134_saga_pattern/)
**다음**: [136. Orchestration Saga - 중앙 오케스트레이터 기반 분산 트랜잭션](/studynote/13_cloud_architecture/03_msa_serverless/136_orchestration_saga/) ->

---
