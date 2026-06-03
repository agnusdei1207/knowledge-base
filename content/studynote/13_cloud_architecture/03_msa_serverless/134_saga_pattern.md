---
title: 134. Saga 패턴 - MSA 분산 트랜잭션의 표준 솔루션
date: '2026-04-19'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Saga는 **여러 마이크로서비스에 걸친 비즈니스 [[191_transaction_concept_states|트랜잭션]]을 로컬 [[191_transaction_concept_states|트랜잭션]]의 시퀀스로 분해**하고, 실패 시 **[[551_compensating_transaction_logical_rollback|보상 트랜잭션]]([[551_compensating_transaction_logical_rollback|Compensating Transaction]])**으로 롤백하는 패턴이다.
> 2. **가치**: 2PC의 블로킹·[[454_spof|단일 장애점]] 문제 없이 **[[090_service_kubernetes_network_load_balancing|서비스]] 자율성을 유지**하면서 [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]]([[650_eventual_consistency|Eventual Consistency]])을 달성한다.
> 3. **판단 포인트**: **Choreography(이벤트 기반, 각 [[090_service_kubernetes_network_load_balancing|서비스]] 독립)** vs **[[073_container_orchestration_tools|Orchestration]](중앙 오케스트레이터)** — [[090_service_kubernetes_network_load_balancing|서비스]] 수가 적으면 Choreography, 복잡하면 [[073_container_orchestration_tools|Orchestration]](Temporal/Cadence).

---

## Ⅰ. 개요 및 필요성

```text
Choreography: 주문→이벤트→결제→이벤트→배송 (각자 독립)
Orchestration: 오케스트레이터→주문, →결제, →배송 (중앙 제어)
실패 시: 보상 트랜잭션 (주문 취소, 결제 환불)
```

- **📢 섹션 요약 비유**: Choreography는 재즈 즉흥(각자 연주), Orchestration은 교향곡(지휘자 지휘)이다.

---

## Ⅱ~Ⅴ. 결론

Saga는 **[[619_msa_traffic_hardware|MSA]] [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]]의 사실상 표준**이며, Temporal/Cadence가 [[073_container_orchestration_tools|Orchestration]] Saga의 대표 프레임워크이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[305_saga|Saga]]** | [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] 패턴 |
| **Choreography** | 이벤트 기반 (독립) |
| **[[073_container_orchestration_tools|Orchestration]]** | 중앙 제어 (Temporal) |
| **[[551_compensating_transaction_logical_rollback|보상 트랜잭션]]** | 실패 시 되돌리기 |
| **[[650_eventual_consistency|Eventual Consistency]]** | 최종 [[194_consistency_database_integrity|일관성]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[2PC (1990s)] → [Saga 이론 (Garcia-Molina, 1987)]
    → [MSA Saga 재발견 (2014~)]
    → [Choreography (Kafka 이벤트)]
    → [Orchestration (Temporal/Cadence, 2020~)]
    → [현재: Durable Execution — Saga 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Saga는 **릴레이 달리기**예요. 각 선수가 자기 구간을 달리고 **바톤을 넘겨요**.
2. 한 선수가 넘어지면(실패) **그 구간만 다시 달려요([[551_compensating_transaction_logical_rollback|보상 트랜잭션]])**.
3. 전원이 동시에 출발하는 것([[549_2pc_two_phase_commit_limitations_msa|2PC]])보다 **빠르고 안전**하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 133 / 371

← **이전**: [[133_2pc_limitations|133. 2PC 한계와 MSA 분산 트랜잭션 - 왜 Saga가 필요한가]]
**다음**: [[135_choreography_saga|135. Choreography Saga - 이벤트 기반 분산 트랜잭션]] →

---
