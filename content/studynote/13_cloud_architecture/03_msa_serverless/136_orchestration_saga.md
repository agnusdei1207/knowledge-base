+++
title = "136. Orchestration Saga - 중앙 오케스트레이터 기반 분산 트랜잭션"
date = 2026-04-19

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [Orchestration](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) Saga는 **중앙 오케스트레이터([Coordinator](/knowledge-base/studynote/05_database/04_transactions_concurrency/250_coordinator_participant_2pc_roles/))가 각 서비스에 명령을 보내고 응답을 받아 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 흐름을 제어**하며, 실패 시 보상 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 순차적으로 호출한다.
> 2. **가치**: Choreography 대비 **[트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 흐름이 한 곳(오케스트레이터)에 집중**되어 복잡한 비즈니스 로직의 이해·디버깅·모니터링이 쉽다.
> 3. **판단 포인트**: Temporal(구 Cadence)·Camunda·Step Functions가 대표 프레임워크이며, **Durable Execution(내구성 실행)**이 핵심 특성으로 프로세스 상태가 장애에도 보존된다.

---

## Ⅰ. 개요 및 필요성

```text
오케스트레이터 → 주문 서비스: "주문 생성" → 성공
오케스트레이터 → 결제 서비스: "결제 처리" → 실패
오케스트레이터 → 주문 서비스: "주문 취소" (보상)
```

- **📢 섹션 요약 비유**: Orchestration은 **교향곡 지휘자**이다. 지휘자가 각 악기에 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 보내 연주를 조율한다.

---

## Ⅱ~Ⅴ. 결론

[Orchestration](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) Saga는 **복잡한 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 비즈니스 흐름의 표준**이며, Temporal의 Durable Execution이 핵심 기술이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[Orchestration](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)** | 중앙 제어 [Saga](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/) |
| **Temporal** | Durable Execution 프레임워크 |
| **Choreography** | 대안 (이벤트 기반) |
| **Durable Execution** | 장애에도 상태 보존 |
| **Step Functions** | AWS [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[2PC (1990s)] → [Choreography Saga (2014~)]
    → [Cadence (Uber, 2017)] → [Temporal (2020~ 오픈소스)]
    → [현재: Durable Execution 표준화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Orchestration은 **교향곡 지휘자**예요. 지휘자가 **각 악기에 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)**를 보내요.
2. 한 악기가 틀리면 지휘자가 **"다시!"** 하고 보상(되돌리기)해요.
3. 재즈(Choreography)보다 **복잡한 곡(비즈니스)**에 적합해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 135 / 371

← **이전**: [135. Choreography Saga - 이벤트 기반 분산 트랜잭션](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/135_choreography_saga/)
**다음**: [137. Transactional Outbox 패턴 - 이벤트 발행의 원자성 보장](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/137_transactional_outbox_pattern/) →

---
