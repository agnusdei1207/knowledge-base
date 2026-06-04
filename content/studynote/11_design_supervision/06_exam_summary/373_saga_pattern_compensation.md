+++
title = "373. 사가 패턴과 보상 트랜잭션 (Saga Pattern and Compensating Transaction)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)과 [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) ([Saga Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/948_saga_pattern/) and [Compensating Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/))은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서 긴 비즈니스 흐름을 여러 로컬 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)과 보상 동작으로 완결하는 방식이다.
> 2. **가치**: 강결합 [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) 없이도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 자율성을 유지하면서 업무 흐름을 연결할 수 있다.
> 3. **판단 포인트**: [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)은 실패 시 “원복이 가능한가”와 “중간 상태를 허용할 수 있는가”를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

[사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)과 [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) ([Saga Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/948_saga_pattern/) and [Compensating Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/))은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서 긴 비즈니스 흐름을 여러 로컬 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)과 보상 동작으로 완결하는 방식이다. MSA에서는 전통적 2단계 커밋이 성능과 결합 측면에서 부담이 커져 다른 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 전략이 필요해졌다. 이 개념이 필요한 이유는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 업무 흐름을 보상 가능하게 설계하는 일을 시스템 수준의 규칙으로 끌어올리기 위해서다. 반대로 이를 무시하면 일부 단계만 성공한 채 남아 주문, 결제, 재고 상태가 불일치하게 된다.

아래 그림은 왜 이 주제가 “문제 인식 -> 설계 규칙 -> 안정화 결과”의 흐름으로 이해되어야 하는지를 압축한다.

```text
+------------+   +------------+   +------------+
|  Request   |--->|    Saga    |--->|   Stable   |
+------------+   +------------+   +------------+
```

이 흐름의 핵심은 기능 하나를 설명하는 것이 아니라, 어떤 압력이 들어와도 구조가 흔들리지 않게 만드는 기준을 세우는 데 있다.

- **📢 섹션 요약 비유**: 도시를 구획 없이 확장하면 길과 배관이 엉키는 것처럼, 구조 원칙이 없으면 시스템도 빨리 혼잡해진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)과 [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) ([Saga Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/948_saga_pattern/) and [Compensating Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/))의 핵심 원리는 "[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 업무 흐름을 보상 가능하게 설계하는 일"을 구현 규칙으로 고정하는 데 있다. 실제 설계에서는 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 로컬 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 수행하고 실패 시 반대 의미의 보상 동작을 [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) 또는 코레오그래피로 실행한다. 동시에 보상 정의가 복잡하고 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 창이 존재하므로 비즈니스 규칙을 세밀히 분석해야 한다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 문제 | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 업무 흐름을 보상 가능하게 설계하는 일 | 이 축이 흔들리면 설계 목적이 사라진다 |
| 구현 방식 | 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 로컬 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 수행하고 실패 시 반대 의미의 보상 동작을 [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) 또는 코레오그래피로 실행한다 | 코드·계층·배포 단위에 일관되게 반영해야 한다 |
| 트레이드오프 | 보상 정의가 복잡하고 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 창이 존재하므로 비즈니스 규칙을 세밀히 분석해야 한다 | 복잡도와 운영 비용을 함께 관리해야 한다 |

다음 그림은 입력, 경계, 핵심 규칙, 결과가 어디서 갈리는지 보여 준다.

```text
+----------+   +----------+   +----------+   +----------+
|  Client  |--->| Boundary |--->|   Core   |--->|  Infra   |
+----------+   +----------+   +----------+   +----------+
```

이때 중요한 것은 도구 이름보다 경계와 책임의 방향이다. 동일한 기술을 써도 이 방향이 다르면 [유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/), 테스트성, 운영 난도가 크게 달라진다.

- **📢 섹션 요약 비유**: 도로망과 관제 센터가 분리된 도시처럼, 경계와 흐름을 함께 설계해야 운영이 안정된다.

---

## Ⅲ. 비교 및 연결

기술사 답안에서는 [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)과 [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) ([Saga Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/948_saga_pattern/) and [Compensating Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/))을 단독 정의보다 대안 구조와 함께 써야 경계가 살아난다. 여기서는 **구조 적용 상태** 와 **경계 혼재 상태** 를 대비해 핵심 차이를 정리한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 변경 대응 | 구조 적용 상태는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 업무 흐름을 보상 가능하게 설계하는 일에 맞춰 영향 범위를 줄인다 | 경계 혼재 상태는 변경이 주변 모듈로 번지기 쉽다 |
| 구조 안정성 | 구조 적용 상태는 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 로컬 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 수행하고 실패 시 반대 의미의 보상 동작을 [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) 또는 코레오그래피로 실행한다 | 경계 혼재 상태는 책임과 의존이 섞여 규칙이 흐려진다 |
| 운영 결과 | 구조 적용 상태는 강결합 [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) 없이도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 자율성을 유지하면서 업무 흐름을 연결할 수 있다 | 경계 혼재 상태는 일부 단계만 성공한 채 남아 주문, 결제, 재고 상태가 불일치하게 된다 |

연결 개념으로는 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) 같은 주변 주제를 함께 써 주면, 단순 암기보다 적용 맥락이 살아난다.

- **📢 섹션 요약 비유**: 계획도시와 무계획 확장을 비교해 보면 어디서 비용이 커지는지 바로 드러난다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)과 [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) ([Saga Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/948_saga_pattern/) and [Compensating Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/))을 무조건 채택하기보다 [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)은 실패 시 “원복이 가능한가”와 “중간 상태를 허용할 수 있는가”를 함께 판단해야 한다. 아래 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)는 설계 감리 시 최소한으로 확인해야 할 질문이다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 경계와 책임이 코드·문서·배포 단위에서 일치하는가?
2. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유권과 장애 전파 경로가 명확한가?
3. 관찰가능성, 보안, 배포 전략이 구조와 함께 설계되었는가?
4. 도입 복잡도가 조직 규모와 팀 성숙도에 맞는가?

답안을 마무리할 때는 “어디에 쓰는가”만이 아니라 “언제 과한가”를 함께 적어야 한다. 그래야 설계 원칙, 패턴, 아키텍처가 구호가 아니라 의사결정 기준으로 읽힌다.

- **📢 섹션 요약 비유**: 관제실의 운영 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)처럼, 경계·장애 전파·관찰가능성을 같이 봐야 한다.

---

## Ⅴ. 기대효과 및 결론

[사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)과 [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) ([Saga Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/948_saga_pattern/) and [Compensating Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/))의 기대효과는 분명하다. 강결합 [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) 없이도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 자율성을 유지하면서 업무 흐름을 연결할 수 있다. 다만 보상 정의가 복잡하고 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 창이 존재하므로 비즈니스 규칙을 세밀히 분석해야 한다. 결국 기억할 관점은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 업무 흐름을 보상 가능하게 설계하는 일을 구조 규칙으로 만드는 데 있다는 점이다.

- **📢 섹션 요약 비유**: 도시 운영 규정집처럼, 좋은 아키텍처는 기술보다 판단 기준을 오래 남긴다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)과 [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) ([Saga Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/948_saga_pattern/) and [Compensating Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) | [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)과 [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) ([Saga Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/948_saga_pattern/) and [Compensating Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| 코레오그래피 | [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)과 [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) ([Saga Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/948_saga_pattern/) and [Compensating Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) | [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)과 [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) ([Saga Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/948_saga_pattern/) and [Compensating Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/))을 설계하고 감리할 때 함께 보는 연관 개념 |

### 📈 관련 키워드 및 발전 흐름도
[분산 동기 트랜잭션] -> [사가 패턴] -> [보상 중심 업무 흐름]

### 👶 어린이를 위한 3줄 비유 설명
1. [사가 패턴](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/)과 [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) ([Saga Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/948_saga_pattern/) and [Compensating Transaction](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/))은 친구들과 릴레이 심부름을 하다가 누가 못 하면 앞사람부터 차례로 되돌리는 것처럼 약속을 먼저 정하는 거예요.
2. 그러면 서로 다른 사람이 해도 같은 규칙으로 움직일 수 있어요.
3. 그래서 규모가 커질수록 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 업무 흐름을 보상 가능하게 설계하는 일이 더 중요해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 451 / 530

<- **이전**: [372. 서비스 메시 (Service Mesh)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/372_service_mesh_summary/)
**다음**: [374. DDD의 바운디드 컨텍스트와 애그리게이트 (Domain-Driven Design Bounded Context and Aggregate)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/374_ddd_bounded_context_aggregate/) ->

---
