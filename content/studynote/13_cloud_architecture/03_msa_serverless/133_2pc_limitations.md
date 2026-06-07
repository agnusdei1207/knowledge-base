---
title: "2Pc Limitations"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 133
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [2PC](/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/)([Two-Phase Commit](/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/))는 <strong><a href="/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/">분산 트랜잭션</a>의 원자성을 보장하는 <a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a>(Prepare->Commit/<a href="/studynote/02_operating_system/05_deadlock/313_rollback/">Rollback</a>)</strong>이지만, MSA에서는 <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 자율성 침해·<a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 저하·<a href="/studynote/01_computer_architecture/13_reliability_power_management/454_spof/">단일 장애점</a>(<a href="/studynote/05_database/04_transactions_concurrency/250_coordinator_participant_2pc_roles/">Coordinator</a>)</strong> 문제로 부적합하다.
> 2. **가치**: 2PC는 DB 간 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)에서는 동작하지만, MSA의 <strong><a href="/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a>/<a href="/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/">gRPC</a> <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 간에는 <a href="/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a>이 불가능</strong>하고, 하나의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 느려지면 전체가 블로킹되므로 <strong><a href="/studynote/12_it_management/05_security_compliance/305_saga/">Saga</a> 패턴</strong>이 대안이다.
> 3. **판단 포인트**: [Choreography Saga](/studynote/04_software_engineering/09_cloud_native_ai_architecture/553_choreography_saga_event_driven/)(이벤트 기반, 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 독립)와 [Orchestration Saga](/studynote/04_software_engineering/09_cloud_native_ai_architecture/552_orchestration_saga_centralized_control/)(중앙 오케스트레이터)를 구분하고, [보상 트랜잭션](/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/)([Compensating Transaction](/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/))이 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
2PC: Coordinator -> Prepare(모든 참여자) -> Commit/Rollback
  한계: 블로킹, 단일 장애점, MSA에 부적합

Saga: 서비스별 로컬 트랜잭션 + 실패 시 보상 트랜잭션
  주문 성공 -> 결제 실패 -> 주문 취소(보상)
```

- **📢 섹션 요약 비유**: 2PC는 단체 행동(전원 동시 출발), Saga는 릴레이(각자 달리고, 실패 시 되돌아옴)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 비교 | [2PC](/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) | [Saga](/studynote/12_it_management/05_security_compliance/305_saga/) |
|:---|:---|:---|
| <strong><a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a></strong> | Strong | **Eventual** |
| **블로킹** | 있음 | **없음** |
| <strong><a href="/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a></strong> | DB [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) | <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/">보상 트랜잭션</a></strong> |
| <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a></strong> | 부적합 | **적합** |

---

## Ⅲ~Ⅴ. 결론

MSA에서는 <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/">2PC</a> 대신 <a href="/studynote/12_it_management/05_security_compliance/305_saga/">Saga</a> 패턴으로 <a href="/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/">Eventual Consistency</a></strong>를 달성하며, [보상 트랜잭션](/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) 설계가 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/">2PC</a></strong> | [분산 트랜잭션](/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) (한계) |
| <strong><a href="/studynote/12_it_management/05_security_compliance/305_saga/">Saga</a></strong> | [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 대안 패턴 |
| **Choreography** | 이벤트 기반 [Saga](/studynote/12_it_management/05_security_compliance/305_saga/) |
| <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/">Orchestration</a></strong> | 중앙 조율 [Saga](/studynote/12_it_management/05_security_compliance/305_saga/) |
| <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/">보상 트랜잭션</a></strong> | 실패 시 되돌리기 |

### 📈 관련 키워드 및 발전 흐름도

```text
[2PC (X/Open DTP, 1990s)] -> [MSA 등장 -> 2PC 한계 인식]
    -> [Saga 패턴 (Garcia-Molina, 1987 -> MSA 재발견)]
    -> [이벤트 소싱 + CQRS (2016~)]
    -> [현재: Temporal/Cadence — Saga 오케스트레이션 프레임워크]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 2PC는 <strong>단체 줄넘기</strong>예요. 한 명이 실패하면 **전원 다시** 해야 해요.
2. Saga는 <strong>릴레이</strong>예요. 각자 달리고, 실패하면 **그 구간만 되돌아와요**.
3. MSA에서는 릴레이([Saga](/studynote/12_it_management/05_security_compliance/305_saga/))가 더 빠르고 **문제가 적어서** 많이 사용해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 132 / 371

<- **이전**: [132. Polyglot Persistence - MSA 서비스별 최적 DB 선택](/studynote/13_cloud_architecture/03_msa_serverless/132_polyglot_persistence/)
**다음**: [134. Saga 패턴 - MSA 분산 트랜잭션의 표준 솔루션](/studynote/13_cloud_architecture/03_msa_serverless/134_saga_pattern/) ->

---
