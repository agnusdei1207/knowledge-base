+++
weight = 133
title = "133. 2PC 한계와 MSA 분산 트랜잭션 - 왜 Saga가 필요한가"
date = "2026-04-19"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[549_2pc_two_phase_commit_limitations_msa|2PC]]([[549_2pc_two_phase_commit_limitations_msa|Two-Phase Commit]])는 **[[248_distributed_transaction_multiple_nodes|분산 트랜잭션]]의 원자성을 보장하는 [[295_protocol_field_tcp_udp_icmp|프로토콜]](Prepare→Commit/[[313_rollback|Rollback]])**이지만, MSA에서는 **[[090_service_kubernetes_network_load_balancing|서비스]] 자율성 침해·[[282_performance_tactics|성능]] 저하·[[454_spof|단일 장애점]]([[250_coordinator_participant_2pc_roles|Coordinator]])** 문제로 부적합하다.
> 2. **가치**: 2PC는 DB 간 [[191_transaction_concept_states|트랜잭션]]에서는 동작하지만, MSA의 **[[461_http_stateless_connection_oriented|HTTP]]/[[479_grpc_protobuf_http2|gRPC]] [[090_service_kubernetes_network_load_balancing|서비스]] 간에는 [[098_rollback_strategy_pipeline_error_threshold|롤백]]이 불가능**하고, 하나의 [[090_service_kubernetes_network_load_balancing|서비스]]가 느려지면 전체가 블로킹되므로 **[[305_saga|Saga]] 패턴**이 대안이다.
> 3. **판단 포인트**: [[553_choreography_saga_event_driven|Choreography Saga]](이벤트 기반, 각 [[090_service_kubernetes_network_load_balancing|서비스]] 독립)와 [[552_orchestration_saga_centralized_control|Orchestration Saga]](중앙 오케스트레이터)를 구분하고, [[551_compensating_transaction_logical_rollback|보상 트랜잭션]]([[551_compensating_transaction_logical_rollback|Compensating Transaction]])이 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
2PC: Coordinator → Prepare(모든 참여자) → Commit/Rollback
  한계: 블로킹, 단일 장애점, MSA에 부적합

Saga: 서비스별 로컬 트랜잭션 + 실패 시 보상 트랜잭션
  주문 성공 → 결제 실패 → 주문 취소(보상)
```

- **📢 섹션 요약 비유**: 2PC는 단체 행동(전원 동시 출발), Saga는 릴레이(각자 달리고, 실패 시 되돌아옴)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 비교 | [[549_2pc_two_phase_commit_limitations_msa|2PC]] | [[305_saga|Saga]] |
|:---|:---|:---|
| **[[194_consistency_database_integrity|일관성]]** | Strong | **Eventual** |
| **블로킹** | 있음 | **없음** |
| **[[098_rollback_strategy_pipeline_error_threshold|롤백]]** | DB [[098_rollback_strategy_pipeline_error_threshold|롤백]] | **[[551_compensating_transaction_logical_rollback|보상 트랜잭션]]** |
| **[[619_msa_traffic_hardware|MSA]]** | 부적합 | **적합** |

---

## Ⅲ~Ⅴ. 결론

MSA에서는 **[[549_2pc_two_phase_commit_limitations_msa|2PC]] 대신 [[305_saga|Saga]] 패턴으로 [[650_eventual_consistency|Eventual Consistency]]**를 달성하며, [[551_compensating_transaction_logical_rollback|보상 트랜잭션]] 설계가 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[549_2pc_two_phase_commit_limitations_msa|2PC]]** | [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] (한계) |
| **[[305_saga|Saga]]** | [[619_msa_traffic_hardware|MSA]] 대안 패턴 |
| **Choreography** | 이벤트 기반 [[305_saga|Saga]] |
| **[[073_container_orchestration_tools|Orchestration]]** | 중앙 조율 [[305_saga|Saga]] |
| **[[551_compensating_transaction_logical_rollback|보상 트랜잭션]]** | 실패 시 되돌리기 |

### 📈 관련 키워드 및 발전 흐름도

```text
[2PC (X/Open DTP, 1990s)] → [MSA 등장 → 2PC 한계 인식]
    → [Saga 패턴 (Garcia-Molina, 1987 → MSA 재발견)]
    → [이벤트 소싱 + CQRS (2016~)]
    → [현재: Temporal/Cadence — Saga 오케스트레이션 프레임워크]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 2PC는 **단체 줄넘기**예요. 한 명이 실패하면 **전원 다시** 해야 해요.
2. Saga는 **릴레이**예요. 각자 달리고, 실패하면 **그 구간만 되돌아와요**.
3. MSA에서는 릴레이([[305_saga|Saga]])가 더 빠르고 **문제가 적어서** 많이 사용해요!
