+++
title = "940. 로컬 트랜잭션 (Local Transaction) vs 분산 트랜잭션 (Distributed Transaction)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) ([Local Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/)) vs [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) ([Distributed Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/))은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

한 DB 안에서는 ACID ([Atomicity](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/), [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/), [Durability](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/))를 비교적 쉽게 지킬 수 있다. 여러 서비스에 걸치면 같은 보장을 얻기 어려워진다.

- **📢 섹션 요약 비유**: 한 가게 계산은 쉽지만, 여러 가게를 동시에 계산하는 건 훨씬 어렵다.

---

다음은 [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) (Local Trans의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
+-------------------------------------------------------------+
|                  로컬 트랜잭션 (Local Trans                        |
+-------------------------------------------------------------+
|                                                             |
|  [입력/요구사항] ---> [핵심 처리 과정] ---> [출력/결과물]  |
|       |                    |                    |          |
|       v                    v                    v          |
|   요구 분석           설계·적용           품질 검증        |
|                                                             |
+-------------------------------------------------------------+
```

이 다이어그램은 [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) (Local Trans가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

[로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/)은 단일 자원에 커밋/롤백을 적용한다. [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/)은 네트워크 너머의 여러 자원을 함께 맞춘다.

```text
Local:  App -> DB
Dist.:  App -> DB1 + DB2 + MQ
```

| 구분 | 로컬 | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) |
|:---|:---|:---|
| 범위 | 단일 자원 | 다중 자원 |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 높음 | 낮음 |
| 복잡도 | 낮음 | 높음 |

- **📢 섹션 요약 비유**: 한 접시 정리와 여러 접시를 동시에 정리하는 차이다.

---

---

---

---

## Ⅲ. 비교 및 연결

[분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/)은 [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) ([Two-Phase Commit](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/)) 같은 프로토콜로 구현할 수 있지만, 장애와 지연에 민감하다. 그래서 [사가](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/)([Saga](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)) 패턴이나 eventual consistency를 선택하기도 한다.

| 구분 | Local | Distributed |
|:---|:---|:---|
| [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 강함 | 설계 필요 |
| 네트워크 의존 | 낮음 | 높음 |
| 장애 대응 | 단순 | 복잡 |

- **📢 섹션 요약 비유**: 같은 방 정리는 바로 되지만, 여러 방 연락은 시간이 걸린다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 정말 필요한 경우만 [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/)을 쓰고, 가능하면 경계를 줄이거나 비동기 보상 처리로 바꾼다.

점검 포인트는 다음과 같다.
1. 꼭 동시에 성공해야 하는가?
2. 네트워크 실패 시 어떻게 복구하는가?
3. 운영 복잡도를 감당할 수 있는가?

- **📢 섹션 요약 비유**: 하나라도 틀리면 전부 멈추는 구조는 손이 많이 간다.

---

---

---

---

## Ⅴ. 기대효과 및 결론

[로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/)은 단순하고 빠르며, [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/)은 범위가 넓지만 비용이 높다.

결론적으로 이 항목은 "단일 자원 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)과 다중 자원 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)의 선택 문제"다.

- **📢 섹션 요약 비유**: 집안일은 혼자 하면 쉽고, 여러 집 일을 동시에 맡으면 더 어렵다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) ([Local Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/)) vs [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) ([Distributed Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/))의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) ([Local Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/)) vs [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) ([Distributed Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/))은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) ([Local Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/)) vs [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) ([Distributed Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/)) 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) ([Local Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/)) vs [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) ([Distributed Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/))에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    |
    v
로컬 트랜잭션 (Local Transaction) vs 분산 트랜잭션 (Distributed Transaction) 개념 정립
    |
    v
표준화 및 방법론 체계화 (ISO, CMMI, Agile)
    |
    v
클라우드 네이티브·AI 기반 확장 적용
    |
    v
지속적 개선 및 DevOps·MLOps 통합
```

이 흐름은 [소프트웨어 위기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 -> 체계적 방법론 개발 -> 표준화 -> 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [로컬 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) ([Local Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/)) vs [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) ([Distributed Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/))은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 687 / 973

<- **이전**: [547. 트래픽 라우팅 및 카나리 배포 제어 (Service Mesh의 역할)](/knowledge-base/studynote/04_software_engineering/11_testing_validation/939_traffic_routing_and_canary_deployment_control/)
**다음**: [548. 로컬 트랜잭션 (Local Transaction) vs 분산 트랜잭션 (Distributed Transaction)](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) ->

---
